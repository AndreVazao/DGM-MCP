import click
from rich.console import Console
import time
import threading

from .core.runtime import MCPRuntime
from .config.config_manager import ConfigManager

console = Console()

@click.group()
def cli():
    pass

@cli.command()
def start():
    """Inicia o DGM-MCP Server completo"""
    console.print("[bold green]🚀 Iniciando DGM-MCP...[/bold green]")

    config = ConfigManager().load()
    runtime = MCPRuntime(config)

    # Iniciar o worker numa thread separada
    worker_thread = threading.Thread(target=runtime.start, daemon=True)
    worker_thread.start()

    from .bridge.mcp_server import MCPServer
    server = MCPServer(runtime)

    try:
        server.start()
    except KeyboardInterrupt:
        console.print("[yellow]Encerrando DGM-MCP...[/yellow]")
        runtime.stop()
    except Exception as e:
        console.print(f"[bold red]Erro crítico: {e}[/bold red]")

@cli.command()
def tools():
    """Lista todas as ferramentas disponíveis"""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime._register_tools()
    console.print("\n[bold]🔧 Ferramentas Disponíveis:[/bold]")
    for name, tool in runtime.tools.items():
        console.print(f"   • [cyan]{name:15}[/cyan] → {tool.description}")

@cli.command()
def status():
    """Mostra o estado atual do runtime"""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    console.print("\n[bold]📊 Status do DGM-MCP:[/bold]")
    console.print(f"   Running: [green]{runtime.running}[/green]")
    console.print(f"   Allowed Paths: [cyan]{config.allowed_paths}[/cyan]")

@cli.command()
def test():
    """Executa um teste rápido do sistema"""
    console.print("[bold]🧪 Executando teste rápido...[/bold]")
    config = ConfigManager().load()
    runtime = MCPRuntime(config)

    # Iniciar numa thread para podermos interagir
    worker_thread = threading.Thread(target=runtime.start, daemon=True)
    worker_thread.start()

    time.sleep(1) # Esperar inicialização

    task = runtime.task_manager.create_task("Testar criação de ficheiro e git status")
    result = runtime.agent.analyze_task(task.id)

    console.print("[green]✅ Teste concluído com sucesso![/green]")
    console.print(f"Task ID: {task.id}")

    runtime.stop()

if __name__ == "__main__":
    cli()
