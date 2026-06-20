from rich.console import Console
from rich.table import Table
from datetime import datetime
from typing import Dict, List
import time

console = Console()

class Observability:
    def __init__(self):
        self.start_time = datetime.now()
        self.tasks_total = 0
        self.tasks_success = 0
        self.tasks_failed = 0
        self.approvals = 0
        self.tool_calls: Dict[str, int] = {}

        self.mcp_requests_total = 0
        self.mcp_tool_calls_total = 0
        self.mcp_tool_failures_total = 0
        self.mcp_sessions_created = 0
        self.mcp_protocol_errors = 0
        self.mcp_tool_latencies: List[float] = []

    def record_task(self, success: bool):
        self.tasks_total += 1
        if success:
            self.tasks_success += 1
        else:
            self.tasks_failed += 1

    def record_tool_call(self, tool_name: str, latency: float | None = None, success: bool = True):
        self.tool_calls[tool_name] = self.tool_calls.get(tool_name, 0) + 1
        self.mcp_tool_calls_total += 1
        if not success:
            self.mcp_tool_failures_total += 1
        if latency is not None:
            self.mcp_tool_latencies.append(latency)

    def record_mcp_request(self):
        self.mcp_requests_total += 1

    def record_mcp_session(self):
        self.mcp_sessions_created += 1

    def record_mcp_error(self):
        self.mcp_protocol_errors += 1

    @property
    def average_tool_latency(self) -> float:
        if not self.mcp_tool_latencies:
            return 0.0
        return sum(self.mcp_tool_latencies) / len(self.mcp_tool_latencies)

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

        table.add_section()
        table.add_row("[bold]MCP Metrics[/bold]", "")
        table.add_row("Requests Total", str(self.mcp_requests_total))
        table.add_row("Sessions Criadas", str(self.mcp_sessions_created))
        table.add_row("Tool Calls (MCP)", str(self.mcp_tool_calls_total))
        table.add_row("Tool Failures (MCP)", str(self.mcp_tool_failures_total))
        table.add_row("Avg Latency (s)", f"{self.average_tool_latency:.4f}")
        table.add_row("Protocol Errors", str(self.mcp_protocol_errors))

        for tool, count in self.tool_calls.items():
            table.add_row(f"Tool: {tool}", str(count))

        console.print(table)
