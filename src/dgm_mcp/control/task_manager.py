from typing import Dict, Optional
from pydantic import BaseModel

class Task(BaseModel):
    id: str
    description: str
    status: str = "pending"
    plan: Optional[dict] = None

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def create_task(self, description: str) -> Task:
        task_id = f"task_{len(self.tasks) + 1}"
        task = Task(id=task_id, description=description)
        self.tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
