from rich.console import Console
from rich.prompt import Confirm

console = Console()

class ApprovalManager:
    """Gerencia aprovações humanas para ações críticas"""

    def request_approval(self, action_description: str, details: str = "") -> bool:
        console.print(f"\n[bold yellow]⚠️  AÇÃO CRÍTICA DETETADA[/bold yellow]")
        console.print(f"Descrição: {action_description}")
        if details:
            console.print(f"Detalhes:\n{details}")

        return Confirm.ask("Deseja aprovar esta ação?", default=False)
