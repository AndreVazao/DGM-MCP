from __future__ import annotations
import json
from typing import Dict, Any, TYPE_CHECKING
from rich.console import Console
from .approval_manager import ApprovalManager
from ..llm.prompts import Prompts
from ..core.session import Session

if TYPE_CHECKING:
    from .task_manager import TaskManager
    from ..core.runtime import MCPRuntime

console = Console()

class CognitiveAgent:
    def __init__(self, runtime: MCPRuntime, task_manager: TaskManager):
        self.runtime = runtime
        self.task_manager = task_manager
        self.approval = ApprovalManager()
        self.llm = runtime.llm_manager
        self.tools = {}
        self.sessions: Dict[str, Session] = {}

    def register_tool(self, tool):
        self.tools[tool.name] = tool

    def create_session(self) -> str:
        session = Session()
        self.sessions[session.id] = session
        return session.id

    def get_session(self, session_id: str) -> Session:
        return self.sessions.get(session_id)

    def analyze_task(self, task_id: str):
        task = self.task_manager.get_task(task_id)
        if not task:
            return {"success": False, "message": "Task não encontrada"}

        console.print(f"[bold blue]🤖 CognitiveAgent analisando tarefa {task.id}[/bold blue]")

        # Preparar prompt
        prompt = Prompts.TASK_ANALYSIS.format(task_description=task.description)

        # Chamar LLM
        response = self.llm.generate(
            prompt=prompt,
            system_prompt=Prompts.SYSTEM_ENGINEER
        )

        if not response.success:
            console.print(f"[red]Erro no LLM: {response.content}[/red]")
            return {"success": False, "message": response.content}

        try:
            plan = json.loads(response.content)
            task.plan = plan
            task.status = "planned"

            console.print(f"[green]Plano gerado com {len(plan.get('steps', []))} passos[/green]")
            return {"success": True, "plan": plan, "llm_model": response.model}
        except Exception:
            console.print("[yellow]Resposta do LLM não foi JSON válido. Usando plano básico.[/yellow]")
            plan = {"steps": [{"tool": "thinking", "description": "Processar manualmente"}]}
            task.plan = plan
            return {"success": True, "plan": plan}

    def execute_plan(self, task_id: str):
        task = self.task_manager.get_task(task_id)
        if not task or not task.plan:
            return {"success": False, "message": "Plano não encontrado"}

        console.print(f"[bold]▶ Executando plano para task {task_id}...[/bold]")
        results = []

        for step in task.plan.get("steps", []):
            console.print(f"   → {step.get('description')}")
            result = self.execute_step(step)
            results.append(result)

            if not result.get("success", False):
                console.print(f"[red]   ✗ Step falhou: {result.get('message')}[/red]")
                break

        task.status = "completed" if all(r.get("success", False) for r in results) else "failed"
        return {"success": True, "results": results}

    def execute_step(self, step: dict):
        tool_name = step.get("tool")
        if tool_name in self.tools:
            tool = self.tools[tool_name]

            if step.get("needs_approval", False) or "write" in str(step).lower():
                approved = self.approval.request_approval(
                    action_description=step.get("description", ""),
                    details=f"Tool: {tool_name}"
                )
                if not approved:
                    return {"success": False, "message": "Ação rejeitada pelo utilizador"}

            # Executar tool (futuramente com parâmetros dinâmicos)
            result = tool.execute(**step)

            if hasattr(result, 'success'):
                return {"success": result.success, "message": result.message, "data": getattr(result, 'data', {})}
            return result
        else:
            if tool_name == "thinking":
                return {"success": True, "message": "Thinking completed"}
            return {"success": False, "message": f"Tool {tool_name} não encontrada"}
