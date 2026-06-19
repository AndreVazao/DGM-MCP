from __future__ import annotations

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
        async def sse():
            async def event_stream():
                yield "event: endpoint\n"
                yield 'data: {"path": "/mcp/message"}\n\n'
                yield "event: ready\n"
                yield 'data: {"status": "connected"}\n\n'

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        @self.app.post("/mcp/message")
        async def message(request: Request):
            payload = await request.json()
            response = self.core.handle(payload)
            return JSONResponse(response)

        @self.app.get("/health")
        async def health():
            return {"status": "ok", "transport": "sse"}

    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.core.handle(payload)
