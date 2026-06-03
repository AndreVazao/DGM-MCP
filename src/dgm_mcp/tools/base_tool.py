from abc import ABC, abstractmethod
from pydantic import BaseModel
from ..security.path_guard import PathGuard

class ToolResult(BaseModel):
    success: bool
    message: str
    data: dict = {}

class BaseTool(ABC):
    name: str
    description: str

    def __init__(self, path_guard: PathGuard):
        self.path_guard = path_guard

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        pass
