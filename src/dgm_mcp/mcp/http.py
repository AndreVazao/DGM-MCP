from __future__ import annotations

import uuid
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
            try:
                payload = await request.json()
            except Exception:
                return JSONResponse(parse_error().to_dict())
            protocol_version = request.headers.get("MCP-Protocol-Version")
            session_id = request.headers.get("MCP-Session-Id")
            if payload.get("method") == "initialize":
                response = self.core.handle(payload)
                self.session_id = session_id or str(uuid.uuid4())
                if response:
                    return JSONResponse(response, headers={"MCP-Session-Id": self.session_id, "MCP-Protocol-Version": protocol_version or self.core.protocol_version})
                return JSONResponse(status_code=202, content=None, headers={"MCP-Session-Id": self.session_id, "MCP-Protocol-Version": protocol_version or self.core.protocol_version})
            if self.session_id and session_id and session_id != self.session_id:
                return JSONResponse(status_code=400, content={"jsonrpc": "2.0", "id": payload.get("id"), "error": {"code": -32000, "message": "Server not initialized"}})
            if payload.get("method") == "notifications/initialized":
                self.core.handle(payload)
                return JSONResponse(status_code=202, content=None, headers={"MCP-Session-Id": self.session_id or str(uuid.uuid4()), "MCP-Protocol-Version": protocol_version or self.core.protocol_version})
            response = self.core.handle(payload)
            if not response:
                return JSONResponse(status_code=202, content=None, headers={"MCP-Session-Id": self.session_id or str(uuid.uuid4()), "MCP-Protocol-Version": protocol_version or self.core.protocol_version})
            headers = {"MCP-Session-Id": self.session_id or str(uuid.uuid4()), "MCP-Protocol-Version": protocol_version or self.core.protocol_version}
            return JSONResponse(response, headers=headers)

        @self.app.get("/mcp")
        async def mcp_stream():
            async def event_stream():
                yield "event: endpoint\n"
                yield 'data: {"path": "/mcp"}\n\n'

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        @self.app.get("/health")
        async def health():
            return {"status": "ok", "transport": "streamable-http"}

    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.core.handle(payload)
