from __future__ import annotations

import uuid
import secrets
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from .jsonrpc import parse_error
from .stdio import StdioMCPServer


class StreamableHTTPMCPServer:
    def __init__(self, runtime):
        self.runtime = runtime
        self.core = StdioMCPServer(runtime)
        self.app = FastAPI(title="DGM-MCP Streamable HTTP")
        self.session_id: str | None = None
        self._setup_routes()

    def _setup_routes(self) -> None:
        @self.app.post("/mcp")
        async def mcp(request: Request):
            auth_error = self._authenticate(request)
            if auth_error is not None:
                return auth_error
            try:
                payload = await request.json()
            except Exception:
                return JSONResponse(parse_error().to_dict())
            protocol_version = request.headers.get("MCP-Protocol-Version")
            session_id = request.headers.get("MCP-Session-Id")
            role = self._role_for(request)
            if payload.get("method") == "initialize":
                response = self.core.handle(payload, role=role)
                self.session_id = session_id or str(uuid.uuid4())
                if response:
                    return JSONResponse(response, headers={"MCP-Session-Id": self.session_id, "MCP-Protocol-Version": protocol_version or self.core.protocol_version})
                return JSONResponse(status_code=202, content=None, headers={"MCP-Session-Id": self.session_id, "MCP-Protocol-Version": protocol_version or self.core.protocol_version})
            if self.session_id and session_id and session_id != self.session_id:
                return JSONResponse(status_code=400, content={"jsonrpc": "2.0", "id": payload.get("id"), "error": {"code": -32000, "message": "Server not initialized"}})
            if payload.get("method") == "notifications/initialized":
                self.core.handle(payload, role=role)
                return JSONResponse(status_code=202, content=None, headers={"MCP-Session-Id": self.session_id or str(uuid.uuid4()), "MCP-Protocol-Version": protocol_version or self.core.protocol_version})
            response = self.core.handle(payload, role=role)
            if not response:
                return JSONResponse(status_code=202, content=None, headers={"MCP-Session-Id": self.session_id or str(uuid.uuid4()), "MCP-Protocol-Version": protocol_version or self.core.protocol_version})
            headers = {"MCP-Session-Id": self.session_id or str(uuid.uuid4()), "MCP-Protocol-Version": protocol_version or self.core.protocol_version}
            return JSONResponse(response, headers=headers)

        @self.app.get("/mcp")
        async def mcp_stream(request: Request):
            auth_error = self._authenticate(request)
            if auth_error is not None:
                return auth_error
            async def event_stream():
                yield "event: endpoint\n"
                yield 'data: {"path": "/mcp"}\n\n'

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        @self.app.get("/health")
        async def health():
            return {"status": "ok", "transport": "streamable-http"}

    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.core.handle(payload)

    def _authenticate(self, request: Request) -> JSONResponse | None:
        config = self.runtime.config
        if not config.mcp_auth_required:
            return None
        expected = config.mcp_api_key
        if not expected:
            return JSONResponse(status_code=503, content={"error": "MCP authentication is required but no key is configured"})
        supplied = request.headers.get("x-dgm-key", "")
        auth = request.headers.get("authorization", "")
        if auth.lower().startswith("bearer "):
            supplied = auth[7:].strip()
        if secrets.compare_digest(supplied, expected):
            return None
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    def _role_for(self, request: Request) -> str:
        config = self.runtime.config
        if config.mcp_allow_role_header:
            requested = request.headers.get("x-dgm-role")
            if requested in config.roles:
                return requested
        return config.mcp_default_role
