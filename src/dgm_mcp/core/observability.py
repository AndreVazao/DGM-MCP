from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()

class Observability:
    def __init__(self):
        self.start_time = datetime.now()
        self.tasks_executed = 0
        self.approvals = 0
        self.errors = 0

    def show_dashboard(self, runtime):
        table = Table(title="DGM-MCP • Dashboard", style="cyan")
        table.add_column("Métrica", style="dim")
        table.add_column("Valor", justify="right")

        uptime = datetime.now() - self.start_time

        table.add_row("Uptime", str(uptime).split(".")[0])
        table.add_row("Tasks Executadas", str(self.tasks_executed))
        table.add_row("Aprovações", str(self.approvals))
        table.add_row("Erros", str(self.errors))
        table.add_row("LLM Ativo", runtime.llm_manager.current_provider.name if runtime.llm_manager.current_provider else "Nenhum")
        table.add_row("Tools Carregadas", str(len(runtime.tools)))

        console.print(table)
