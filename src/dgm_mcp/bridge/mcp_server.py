import json
from fastapi import FastAPI, Request
import uvicorn
from rich.console import Console

from ..core.runtime import MCPRuntime

console = Console()

class MCPServer:
    def __init__(self, runtime: MCPRuntime):
        self.runtime = runtime
        self.app = FastAPI(title="DGM-MCP")
        self.task_manager = runtime.task_manager
        self.agent = runtime.agent
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/mcp/task")
        async def create_task(request: Request):
            data = await request.json()
            description = data.get("description")
            session_id = data.get("session_id")

            if not description:
                return {"status": "error", "message": "description required"}

            task = self.task_manager.create_task(description)
            result = self.agent.analyze_task(task.id)

            return {
                "status": "success",
                "task_id": task.id,
                "session_id": session_id,
                "plan": result.get("plan"),
                "model": result.get("llm_model")
            }

    def start(self):
        console.print("🟢 MCP Server em http://127.0.0.1:8000")
        uvicorn.run(self.app, host="127.0.0.1", port=8000, log_level="info")
