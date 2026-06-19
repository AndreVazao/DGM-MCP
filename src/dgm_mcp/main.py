import click
from rich.console import Console

from .core.runtime import MCPRuntime
from .config.config_manager import ConfigManager

console = Console()

@click.group()
def cli():
    pass

@cli.command()
@click.option("--llm", default=None, help="Forçar LLM específico")
def start(llm: str = None):
    """Inicia o DGM-MCP Server"""
    console.print("[bold green]🚀 Iniciando DGM-MCP...[/bold green]")
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()

    if llm:
        if runtime.llm_manager.set_provider(llm):
            console.print(f"[green]Forçado LLM: {llm}[/green]")
        else:
            console.print(f"[red]Erro: LLM '{llm}' não encontrado ou não disponível.[/red]")
            return

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
def status():
    """Mostra status completo do sistema"""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    console.print("\n[bold]📊 DGM-MCP Status[/bold]")
    console.print(f"LLMs disponíveis: {runtime.llm_manager.list_available()}")
    console.print(f"LLM ativo: {runtime.llm_manager.current_provider.name if runtime.llm_manager.current_provider else 'Nenhum'}")

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

@cli.command()
def web():
    """Inicia interface web simples"""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    from .web.app import start_web
    start_web()


@cli.command("run-stdio")
def run_stdio():
    """Inicia o servidor MCP em STDIO."""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    from .mcp.stdio import StdioMCPServer
    StdioMCPServer(runtime).serve()


@cli.command("run-sse")
def run_sse():
    """Inicia o servidor MCP em SSE."""
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    from .mcp.sse import SSEMCPServer
    import uvicorn

    uvicorn.run(SSEMCPServer(runtime).app, host="127.0.0.1", port=8002, log_level="info")

if __name__ == "__main__":
    cli()
