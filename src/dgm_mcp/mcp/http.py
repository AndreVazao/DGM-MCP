from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from .stdio import StdioMCPServer


class StreamableHTTPMCPServer:
    def __init__(self, runtime):
        self.runtime = runtime
        self.core = StdioMCPServer(runtime)
        self.app = FastAPI(title="DGM-MCP Streamable HTTP")
        self._setup_routes()

    def _setup_routes(self) -> None:
        @self.app.post("/mcp")
        async def mcp(request: Request):
            payload = await request.json()
            if payload.get("method") == "notifications/initialized":
                return JSONResponse(status_code=202, content=None)
            response = self.core.handle(payload)
            if not response:
                return JSONResponse(status_code=202, content=None)
            return JSONResponse(response)

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

