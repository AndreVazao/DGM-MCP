import json
from fastapi import FastAPI, Request
import uvicorn
from ..core.runtime import MCPRuntime
from ..control.task_manager import TaskManager
from ..control.cognitive_agent import CognitiveAgent

class MCPServer:
    def __init__(self, runtime: MCPRuntime):
        self.runtime = runtime
        self.app = FastAPI(title="DGM-MCP Server")
        self.task_manager = TaskManager()
        self.agent = CognitiveAgent(runtime, self.task_manager)

        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/mcp/task")
        async def create_task(request: Request):
            data = await request.json()
            description = data.get("description", "Sem descrição")

            task = self.task_manager.create_task(description)
            result = self.agent.analyze_task(task.id)

            return {
                "status": "success",
                "task_id": task.id,
                "message": "Tarefa criada e analisada",
                "plan": result.get("plan")
            }

    def start(self):
        print("🟢 MCP Server iniciado em http://127.0.0.1:8000")
        uvicorn.run(self.app, host="127.0.0.1", port=8000)
