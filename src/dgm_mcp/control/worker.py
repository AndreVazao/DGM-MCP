from __future__ import annotations
import time
import threading
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
        self.thread = None
        self.interval = 1.5

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        console.print("[bold blue]👷 Worker iniciado em background (thread)[/bold blue]")

    def _run_loop(self):
        while self.running:
            try:
                pending_tasks = [
                    t for t in self.task_manager.tasks.values()
                    if t.status in ["pending", "planned"]
                ]

                for task in pending_tasks[:3]:  # limita tarefas simultâneas
                    if task.status == "pending":
                        self.runtime.agent.analyze_task(task.id)
                    elif task.status == "planned":
                        self.runtime.agent.execute_plan(task.id)

            except Exception as e:
                console.print(f"[red]Erro no Worker: {e}[/red]")

            time.sleep(self.interval)

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=3)
        console.print("[yellow]Worker parado[/yellow]")
