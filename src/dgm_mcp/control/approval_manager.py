from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()

class ApprovalManager:
    def request_approval(self, action_description: str, details: str = "", risk_level: str = "medium") -> bool:
        console.print(Panel.fit(
            f"[bold yellow]⚠️  REQUER APROVAÇÃO HUMANA[/bold yellow]\n\n"
            f"[white]Ação:[/white] {action_description}\n"
            f"[white]Risco:[/white] [red]{risk_level.upper()}[/red]",
            title="DGM-MCP • Approval",
            border_style="yellow"
        ))

        if details:
            console.print(f"[dim]{details}[/dim]")

        console.print("\n[yellow]Esta ação vai modificar o sistema.[/yellow]")

        return Confirm.ask(
            "[bold]Deseja aprovar esta ação?[/bold]",
            default=False
        )
