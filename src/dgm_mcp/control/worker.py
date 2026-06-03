from .task_manager import TaskManager
from ..core.runtime import MCPRuntime

class Worker:
    def __init__(self, runtime: MCPRuntime, task_manager: TaskManager):
        self.runtime = runtime
        self.task_manager = task_manager
        self.running = False

    def start(self):
        self.running = True
        print("Worker iniciado e à espera de tarefas...")

    def stop(self):
        self.running = False
