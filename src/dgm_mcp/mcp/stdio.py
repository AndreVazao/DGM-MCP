from __future__ import annotations

import json
import sys
from typing import Any

from .adapter import ToolAdapter
from .jsonrpc import JSONRPCResponse, make_error, parse_request
from .resources import PromptRegistry, ResourceRegistry
from .tool_registry import ToolRegistry


class StdioMCPServer:
    def __init__(self, runtime):
        self.runtime = runtime
        self.adapter = ToolAdapter(runtime)
        self.registry = ToolRegistry()
        self.resources = ResourceRegistry(runtime)
        self.prompts = PromptRegistry()
        self._sync_registry()

    def _sync_registry(self) -> None:
        for tool in self.runtime.tools.values():
            self.registry.register(tool.name, tool.description, self.adapter._schema_for(tool.name))

    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        request = parse_request(payload)

        if request.method == "initialize":
            return JSONRPCResponse(
                id=request.id,
                result={
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "dgm-mcp", "version": "0.1.5"},
                    "capabilities": {"tools": {"listChanged": False}},
                },
            ).to_dict()

        if request.method == "tools/list":
            return JSONRPCResponse(id=request.id, result={"tools": self.adapter.list_tools()}).to_dict()

        if request.method == "tools/call":
            params = request.params or {}
            return JSONRPCResponse(
                id=request.id,
                result=self.adapter.call_tool(params.get("name", ""), params.get("arguments")),
            ).to_dict()

        if request.method == "resources/list":
            return JSONRPCResponse(id=request.id, result={"resources": self.resources.list_resources()}).to_dict()

        if request.method == "resources/read":
            params = request.params or {}
            return JSONRPCResponse(id=request.id, result=self.resources.read_resource(params.get("uri", ""))).to_dict()

        if request.method == "prompts/list":
            return JSONRPCResponse(id=request.id, result={"prompts": self.prompts.list_prompts()}).to_dict()

        if request.method == "prompts/get":
            params = request.params or {}
            return JSONRPCResponse(
                id=request.id,
                result=self.prompts.get_prompt(params.get("name", ""), params.get("arguments")),
            ).to_dict()

        return make_error(request.id, -32601, f"Method not found: {request.method}").to_dict()

    def serve(self) -> None:
        for line in sys.stdin:
            raw = line.strip()
            if not raw:
                continue
            try:
                payload = json.loads(raw)
                response = self.handle(payload)
            except Exception as exc:
                response = make_error(None, -32603, "Internal error", str(exc)).to_dict()
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
