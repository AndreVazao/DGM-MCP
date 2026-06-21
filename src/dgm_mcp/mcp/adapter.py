from __future__ import annotations

from typing import Any
from jsonschema import validate


class ToolAdapter:
    def __init__(self, runtime):
        self.runtime = runtime

    def list_tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": self._schema_for(tool.name),
            }
            for tool in self.runtime.tools.values()
        ]

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        tool = self.runtime.tools.get(name)
        if tool is None:
            return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

        args = arguments or {}
        schema = self._schema_for(name)
        validate(instance=args, schema=schema)
        result = tool.execute(**args)
        return {
            "isError": not result.success,
            "content": [{"type": "text", "text": result.message}],
            "structuredContent": result.data,
        }

    def _schema_for(self, name: str) -> dict[str, Any]:
        schemas = {
            "filesystem": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "action": {"type": "string", "enum": ["read", "write"]},
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["action", "path"],
            },
            "git": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "action": {"type": "string", "enum": ["status", "commit"]},
                    "repo_path": {"type": "string"},
                    "message": {"type": "string"},
                },
                "required": ["action"],
            },
            "shell": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "command": {"type": "string"},
                    "cwd": {"type": "string"},
                    "timeout": {"type": "integer"},
                },
                "required": ["command"],
            },
            "patch": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "action": {"type": "string", "enum": ["preview_write", "write"]},
                    "file_path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["action", "file_path"],
            },
            "repo": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "action": {"type": "string", "enum": ["init", "clone"]},
                    "path": {"type": "string"},
                    "url": {"type": "string"},
                },
                "required": ["action"],
            },
        }
        return schemas.get(name, {"type": "object", "properties": {}})
