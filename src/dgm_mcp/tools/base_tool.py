from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional, Any
from ..security.path_guard import PathGuard
from ..security.audit_logger import AuditLogger

class ToolResult(BaseModel):
    success: bool
    message: str
    data: dict[str, Any] = {}

class BaseTool(ABC):
    name: str
    description: str

    def __init__(self, path_guard: PathGuard, audit: Optional[AuditLogger] = None):
        self.path_guard = path_guard
        self.audit = audit

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        pass
