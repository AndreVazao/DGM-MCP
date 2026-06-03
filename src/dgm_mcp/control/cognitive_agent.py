from ..tools.base_tool import ToolResult
from .task_manager import TaskManager
from ..core.runtime import MCPRuntime

class CognitiveAgent:
    """Responsável pelo raciocínio e planeamento"""

    def __init__(self, runtime: MCPRuntime, task_manager: TaskManager):
        self.runtime = runtime
        self.task_manager = task_manager
        self.tools = {}

    def register_tool(self, tool):
        self.tools[tool.name] = tool

    def analyze_task(self, task_id: str):
        task = self.task_manager.get_task(task_id)
        if not task:
            return {"success": False, "message": "Task não encontrada"}

        print(f"[CognitiveAgent] Analisando tarefa: {task.description}")

        # Plano simples por agora (pode ser melhorado com LLM local no futuro)
        plan = {
            "steps": [
                {"action": "analyze", "description": "Entender requisitos"},
                {"action": "plan", "description": "Criar plano detalhado"},
                {"action": "execute", "description": "Executar com ferramentas"}
            ]
        }

        task.plan = plan
        task.status = "planned"

        return {"success": True, "plan": plan}
