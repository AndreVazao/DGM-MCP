from __future__ import annotations

import json
import sys
import time
from typing import Any

from .adapter import ToolAdapter
from .jsonrpc import (
    JSONRPCResponse,
    make_error,
    internal_error,
    invalid_params,
    invalid_request,
    method_not_found,
    parse_error,
    parse_request,
)
from .resources import PromptRegistry, ResourceRegistry
from .state import MCPState
from .tool_registry import ToolRegistry
from .session_manager import SessionManager


class StdioMCPServer:
    def __init__(self, runtime):
        self.runtime = runtime
        self.adapter = ToolAdapter(runtime)
        self.registry = ToolRegistry()
        self.resources = ResourceRegistry(runtime)
        self.prompts = PromptRegistry()
        self.sessions = SessionManager()
        self.runtime.mcp_sessions = self.sessions
        self.current_session = None
        self.state = MCPState.CREATED
        self.protocol_version = "2025-06-18"
        self._sync_registry()

    def _sync_registry(self) -> None:
        for tool in self.runtime.tools.values():
            self.registry.register(tool.name, tool.description, self.adapter._schema_for(tool.name))

    def _ensure_initialized(self, request) -> dict[str, Any] | None:
        if request.method in {"initialize", "shutdown"}:
            return None
        if self.state != MCPState.INITIALIZED:
            return make_error(request.id, -32000, "Server not initialized").to_dict()
        return None

    def _negotiate_protocol_version(self, requested: str | None) -> str:
        supported = ["2025-06-18", "2025-03-26", "2024-11-05"]
        if requested in supported:
            return requested
        return supported[0]

    def handle(self, payload: dict[str, Any], session_id: str | None = None) -> dict[str, Any] | None:
        self.runtime.observability.record_mcp_request()
        try:
            request = parse_request(payload)
        except (TypeError, ValueError):
            self.runtime.observability.record_mcp_error()
            return invalid_request(None).to_dict()

        if session_id:
            session = self.sessions.get_session(session_id)
            if not session:
                session = self.sessions.create_session(session_id)
                self.runtime.observability.record_mcp_session()
            self.current_session = session
        elif self.current_session is None:
             self.current_session = self.sessions.create_session("default-stdio")
             self.runtime.observability.record_mcp_session()

        self.current_session.touch()

        if request.id is None:
            if request.method == "initialized":
                self.state = MCPState.INITIALIZED
            return None

        if request.method == "initialize":
            self.state = MCPState.INITIALIZING
            params = request.params or {}
            requested_version = params.get("protocolVersion") if isinstance(params, dict) else None
            self.protocol_version = self._negotiate_protocol_version(requested_version)
            if self.current_session:
                self.current_session.protocol_version = self.protocol_version
                if isinstance(params, dict):
                    self.current_session.capabilities = params.get("capabilities", {})
                    self.current_session.client_info = params.get("clientInfo", {})
            return JSONRPCResponse(
                id=request.id,
                result={
                    "protocolVersion": self.protocol_version,
                    "serverInfo": {"name": "dgm-mcp", "version": "0.2.0-rc1"},
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {"subscribe": False, "listChanged": False},
                        "prompts": {"listChanged": False},
                    },
                },
            ).to_dict()

        gate = self._ensure_initialized(request)
        if gate is not None:
            return gate

        if request.method == "tools/list":
            params = request.params or {}
            cursor = params.get("cursor") if isinstance(params, dict) else None
            tools, next_cursor = self.registry.list_tools(cursor)
            result = {"tools": tools}
            if next_cursor:
                result["nextCursor"] = next_cursor
            return JSONRPCResponse(id=request.id, result=result).to_dict()

        if request.method == "tools/call":
            params = request.params or {}
            try:
                start_time = time.time()
                tool_name = params.get("name", "")
                result = self.adapter.call_tool(tool_name, params.get("arguments"))
                latency = time.time() - start_time
                self.runtime.observability.record_tool_call(tool_name, latency=latency, success=not result.get("isError", False))
                return JSONRPCResponse(id=request.id, result=result).to_dict()
            except Exception as exc:
                self.runtime.observability.record_mcp_error()
                return invalid_params(request.id, str(exc)).to_dict()

        if request.method == "resources/list":
            params = request.params or {}
            cursor = params.get("cursor") if isinstance(params, dict) else None
            resources, next_cursor = self.resources.list_resources(cursor)
            result = {"resources": resources}
            if next_cursor:
                result["nextCursor"] = next_cursor
            return JSONRPCResponse(id=request.id, result=result).to_dict()

        if request.method == "resources/read":
            params = request.params or {}
            return JSONRPCResponse(id=request.id, result=self.resources.read_resource(params.get("uri", ""))).to_dict()

        if request.method == "prompts/list":
            params = request.params or {}
            cursor = params.get("cursor") if isinstance(params, dict) else None
            prompts, next_cursor = self.prompts.list_prompts(cursor)
            result = {"prompts": prompts}
            if next_cursor:
                result["nextCursor"] = next_cursor
            return JSONRPCResponse(id=request.id, result=result).to_dict()

        if request.method == "prompts/get":
            params = request.params or {}
            result = self.prompts.get_prompt(params.get("name", ""), params.get("arguments"))
            return JSONRPCResponse(id=request.id, result=result).to_dict()

        if request.method == "shutdown":
            self.state = MCPState.SHUTDOWN
            return JSONRPCResponse(id=request.id, result={"ok": True}).to_dict()

        self.runtime.observability.record_mcp_error()
        return method_not_found(request.id).to_dict()

    def serve(self) -> None:
        try:
            for line in sys.stdin:
                raw = line.strip()
                if not raw: continue
                try:
                    payload = json.loads(raw)
                    response = self.handle(payload)
                except json.JSONDecodeError:
                    response = parse_error().to_dict()
                except Exception as exc:
                    response = internal_error(None, str(exc)).to_dict()
                if response is not None:
                    sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                    sys.stdout.flush()
        except KeyboardInterrupt:
            return
