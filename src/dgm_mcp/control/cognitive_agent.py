from __future__ import annotations
import json
from typing import Dict, TYPE_CHECKING
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
            result = self.execute_step(step, task.role)
            results.append(result)

            if not result.get("success", False):
                console.print(f"[red]   ✗ Step falhou: {result.get('message')}[/red]")
                break

        is_success = all(r.get("success", False) for r in results)
        task.status = "completed" if is_success else "failed"
        self.runtime.observability.record_task(success=is_success)

        return {"success": True, "results": results}

    def execute_step(self, step: dict, role: str = "developer"):
        tool_name = step.get("tool")

        # Validar permissões (RBAC)
        allowed_tools = self.runtime.config.roles.get(role, [])
        if tool_name not in allowed_tools and tool_name != "thinking":
            return {
                "success": False,
                "message": f"Acesso negado: o papel '{role}' não tem permissão para a tool '{tool_name}'"
            }

        if tool_name in self.tools:
            tool = self.tools[tool_name]

            needs_approval = (
                step.get("needs_approval") is True or
                step.get("risk_level") in ["medium", "high"] or
                any(x in str(step).lower() for x in ["write", "delete", "commit", "patch"])
            )

            if needs_approval:
                approved = self.approval.request_approval(
                    action_description=step.get("description", tool_name),
                    details=f"Tool: {tool_name} | Step: {step}",
                    risk_level=step.get("risk_level", "medium")
                )
                if not approved:
                    return {"success": False, "message": "Ação rejeitada pelo utilizador"}
                self.runtime.observability.approvals += 1

            self.runtime.observability.record_tool_call(tool_name)
            result = tool.execute(**step)
            return result.model_dump() if hasattr(result, "model_dump") else {"success": result.success, "message": result.message}
        else:
            if tool_name == "thinking":
                return {"success": True, "message": "Thinking completed"}
            return {"success": False, "message": f"Tool '{tool_name}' não encontrada"}

    def stream_response(self, prompt: str, system_prompt: str = None):
        console.print("[bold magenta]🤖 LLM pensando...[/bold magenta]")
        response = self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt or Prompts.SYSTEM_ENGINEER
        )
        if response.success:
            console.print(f"[green]Resposta do {response.model}:[/green]")
            console.print(response.content[:800] + "..." if len(response.content) > 800 else response.content)
        return response
