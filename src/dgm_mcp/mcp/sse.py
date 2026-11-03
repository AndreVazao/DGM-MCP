from __future__ import annotations

import secrets
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse

from .stdio import StdioMCPServer


class SSEMCPServer:
    def __init__(self, runtime):
        self.runtime = runtime
        self.core = StdioMCPServer(runtime)
        self.app = FastAPI(title="DGM-MCP SSE")
        self._setup_routes()

    def _setup_routes(self) -> None:
        @self.app.get("/mcp/sse")
        async def sse(request: Request):
            auth_error = self._authenticate(request)
            if auth_error is not None:
                return auth_error
            async def event_stream():
                yield "event: endpoint\n"
                yield 'data: {"path": "/mcp/message"}\n\n'
                yield "event: ready\n"
                yield 'data: {"status": "connected"}\n\n'

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        @self.app.post("/mcp/message")
        async def message(request: Request):
            auth_error = self._authenticate(request)
            if auth_error is not None:
                return auth_error
            payload = await request.json()
            if payload.get("method") == "shutdown":
                return JSONResponse({"jsonrpc": "2.0", "id": payload.get("id"), "result": {"ok": True}})
            response = self.core.handle(payload, role=self._role_for(request))
            return JSONResponse(response) if response else JSONResponse({"ok": True})

        @self.app.get("/health")
        async def health():
            return {"status": "ok", "transport": "sse"}

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
