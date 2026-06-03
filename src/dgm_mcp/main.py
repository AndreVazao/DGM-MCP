import sys
import click
from rich.console import Console

from .core.runtime import MCPRuntime
from .config.config_manager import ConfigManager
from .bridge.mcp_server import MCPServer

console = Console()

@click.group()
def cli():
    pass

@cli.command()
def start():
    """Inicia o DGM-MCP Server"""
    console.print("[bold green]🚀 Iniciando DGM-MCP...[/bold green]")

    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()

    server = MCPServer(runtime)

    try:
        server.start()
    except KeyboardInterrupt:
        console.print("[yellow]Encerrando DGM-MCP...[/yellow]")
        runtime.stop()

if __name__ == "__main__":
    cli()
