from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .pagination import Paginator

@dataclass
class ToolDefinition:
    name: str
    description: str
    inputSchema: dict[str, Any]

@dataclass
class ToolRegistry:
    tools: dict[str, ToolDefinition] = field(default_factory=dict)
    def register(self, name: str, description: str, input_schema: dict[str, Any]) -> None:
        self.tools[name] = ToolDefinition(name=name, description=description, inputSchema=input_schema)
    def list_tools(self, cursor: str | None = None) -> tuple[list[dict[str, Any]], str | None]:
        sorted_tools = sorted(self.tools.values(), key=lambda x: x.name)
        tool_dicts = [{"name": t.name, "description": t.description, "inputSchema": t.inputSchema} for t in sorted_tools]
        return Paginator(tool_dicts).get_page(cursor)
    def get(self, name: str) -> ToolDefinition | None:
        return self.tools.get(name)
