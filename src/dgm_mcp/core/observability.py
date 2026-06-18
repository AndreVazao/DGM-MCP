from rich.console import Console
from rich.table import Table
from datetime import datetime
from typing import Dict

console = Console()

class Observability:
    def __init__(self):
        self.start_time = datetime.now()
        self.tasks_total = 0
        self.tasks_success = 0
        self.tasks_failed = 0
        self.approvals = 0
        self.tool_calls: Dict[str, int] = {}

    def record_task(self, success: bool):
        self.tasks_total += 1
        if success:
            self.tasks_success += 1
        else:
            self.tasks_failed += 1

    def record_tool_call(self, tool_name: str):
        self.tool_calls[tool_name] = self.tool_calls.get(tool_name, 0) + 1

    def show_dashboard(self, runtime):
        table = Table(title="DGM-MCP • Dashboard", style="cyan")
        table.add_column("Métrica", style="dim")
        table.add_column("Valor", justify="right")

        uptime = datetime.now() - self.start_time

        table.add_row("Uptime", str(uptime).split(".")[0])
        table.add_row("Tasks Total", str(self.tasks_total))
        table.add_row("Tasks Sucesso", str(self.tasks_success))
        table.add_row("Tasks Falhas", str(self.tasks_failed))
        table.add_row("Aprovações", str(self.approvals))
        table.add_row("LLM Ativo", runtime.llm_manager.current_provider.name if runtime.llm_manager.current_provider else "Nenhum")
        table.add_row("Tools Carregadas", str(len(runtime.tools)))

        for tool, count in self.tool_calls.items():
            table.add_row(f"Tool: {tool}", str(count))

        console.print(table)
