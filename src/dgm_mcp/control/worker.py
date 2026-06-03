from __future__ import annotations
import time
from typing import TYPE_CHECKING
from rich.console import Console

if TYPE_CHECKING:
    from ..core.runtime import MCPRuntime
    from .task_manager import TaskManager

console = Console()

class Worker:
    def __init__(self, runtime: MCPRuntime, task_manager: TaskManager):
        self.runtime = runtime
        self.task_manager = task_manager
        self.running = False
        self.interval = 2  # segundos

    def start(self):
        self.running = True
        console.print("[bold blue]👷 Worker iniciado[/bold blue]")

        while self.running:
            pending_tasks = [t for t in self.task_manager.tasks.values() if t.status == "pending"]
            for task in pending_tasks:
                console.print(f"[dim]Processando tarefa: {task.id}[/dim]")
                self.runtime.agent.analyze_task(task.id)
                task.status = "in_progress"

            time.sleep(self.interval)
            if not self.running: break

    def stop(self):
        self.running = False
