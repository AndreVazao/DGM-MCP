from rich.console import Console
from rich.logging import RichHandler
import logging
import sys

console = Console()

class DGMLogger:
    def __init__(self):
        self.logger = logging.getLogger("dgm_mcp")
        self.logger.setLevel(logging.INFO)

        handler = RichHandler(console=console, show_time=True, show_path=False)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)

        self.logger.handlers.clear()
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def info(self, msg: str):
        self.logger.info(f"[bold blue]ℹ[/bold blue] {msg}")

    def success(self, msg: str):
        self.logger.info(f"[bold green]✅[/bold green] {msg}")

    def warning(self, msg: str):
        self.logger.warning(f"[bold yellow]⚠[/bold yellow] {msg}")

    def error(self, msg: str):
        self.logger.error(f"[bold red]❌[/bold red] {msg}")
