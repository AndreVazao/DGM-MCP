from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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

    def list_tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema,
            }
            for tool in self.tools.values()
        ]

    def get(self, name: str) -> ToolDefinition | None:
        return self.tools.get(name)
