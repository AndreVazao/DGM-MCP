from __future__ import annotations
from typing import TYPE_CHECKING
from .approval_manager import ApprovalManager
from rich.console import Console

if TYPE_CHECKING:
    from .task_manager import TaskManager
    from ..core.runtime import MCPRuntime

console = Console()

class CognitiveAgent:
    def __init__(self, runtime: MCPRuntime, task_manager: TaskManager):
        self.runtime = runtime
        self.task_manager = task_manager
        self.approval = ApprovalManager()
        self.tools = {}

    def register_tool(self, tool):
        self.tools[tool.name] = tool

    def analyze_task(self, task_id: str):
        task = self.task_manager.get_task(task_id)
        if not task:
            return {"success": False, "message": "Task não encontrada"}

        console.print(f"[bold blue]🤖 Analisando tarefa:[/bold blue] {task.description}")

        # Plano mais inteligente
        plan = {
            "steps": [
                {"tool": "filesystem", "action": "read", "description": "Analisar estrutura atual"},
                {"tool": "git", "action": "status", "description": "Ver estado do repositório"},
                {"tool": "thinking", "description": "Pensar na melhor abordagem"}
            ]
        }

        task.plan = plan
        task.status = "planned"

        return {"success": True, "plan": plan}

    def execute_step(self, step: dict):
        if step.get("tool") == "git" or "write" in str(step):
            if not self.approval.request_approval(step["description"]):
                return {"success": False, "message": "Ação rejeitada pelo utilizador"}

        return {"success": True, "message": "Step executado"}
