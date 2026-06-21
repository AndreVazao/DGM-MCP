from fastapi import FastAPI, Request
import uvicorn
from rich.console import Console

from ..core.runtime import MCPRuntime
from ..web.rate_limiter import RateLimitMiddleware

console = Console()

class MCPServer:
    def __init__(self, runtime: MCPRuntime):
        self.runtime = runtime
        self.app = FastAPI(title="DGM-MCP")
        self.app.add_middleware(RateLimitMiddleware, req_per_second=5, req_per_minute=50)
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

        @self.app.get("/health")
        async def health():
            return {
                "status": "ok",
                "runtime": self.runtime.running,
                "tools": len(self.runtime.tools),
                "llm_provider": self.runtime.llm_manager.current_provider.name.lower() if self.runtime.llm_manager.current_provider else "none"
            }

        @self.app.get("/metrics")
        async def metrics():
            obs = self.runtime.observability
            return {
                "tasks_total": obs.tasks_total,
                "tasks_success": obs.tasks_success,
                "tasks_failed": obs.tasks_failed,
                "tool_calls": obs.tool_calls
            }

    def start(self):
        console.print("🟢 MCP Server em http://127.0.0.1:8000")
        uvicorn.run(self.app, host="127.0.0.1", port=8000, log_level="info")
