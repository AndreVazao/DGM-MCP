import click
from rich.console import Console

from .core.runtime import MCPRuntime
from .config.config_manager import ConfigManager

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

    from .bridge.mcp_server import MCPServer
    server = MCPServer(runtime)
    try:
        server.start()
    except KeyboardInterrupt:
        console.print("[yellow]Encerrando DGM-MCP...[/yellow]")
        runtime.stop()
    except Exception as e:
        console.print(f"[bold red]Erro: {e}[/bold red]")

@cli.command()
def tools():
    """Lista todas as ferramentas"""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    console.print("\n[bold]🔧 Ferramentas disponíveis:[/bold]")
    for name, tool in runtime.tools.items():
        console.print(f"   • [cyan]{name}[/cyan] → {tool.description}")

@cli.command()
def test():
    """Executa teste rápido"""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    task = runtime.task_manager.create_task("Teste rápido do sistema")
    result = runtime.agent.analyze_task(task.id)
    console.print("[green]✅ Teste concluído[/green]")

@cli.command()
def dashboard():
    """Mostra dashboard"""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    if hasattr(runtime, 'observability'):
        runtime.observability.show_dashboard(runtime)

if __name__ == "__main__":
    cli()
