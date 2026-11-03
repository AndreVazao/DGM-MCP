from __future__ import annotations

import time
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

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None, role: str | None = None) -> dict[str, Any]:
        tool = self.runtime.tools.get(name)
        if tool is None:
            return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

        args = arguments or {}
        schema = self._schema_for(name)
        validate(instance=args, schema=schema)
        allowed = self._authorize(name, args, role or self.runtime.config.mcp_default_role)
        if allowed is not None:
            return allowed
        result = tool.execute(**args)
        return {
            "isError": not result.success,
            "content": [{"type": "text", "text": result.message}],
            "structuredContent": result.data,
        }

    def _authorize(self, name: str, args: dict[str, Any], role: str) -> dict[str, Any] | None:
        config = self.runtime.config
        action = self._action_for(name, args)
        role_tools = config.roles.get(role, [])
        role_actions = config.tool_action_permissions.get(role, {})

        denied_reason = None
        if name not in role_tools:
            denied_reason = f"Role '{role}' cannot use tool '{name}'"
        elif action not in role_actions.get(name, []):
            denied_reason = f"Role '{role}' cannot perform '{action}' with tool '{name}'"
        elif self._is_high_risk(name, action) and not config.mcp_high_risk_enabled:
            denied_reason = f"High-risk action disabled: {name}.{action}"
        elif name in {"filesystem", "patch"} and action == "write":
            content = args.get("content") or ""
            if len(content.encode("utf-8")) > config.max_file_write_bytes:
                denied_reason = "Write payload exceeds configured limit"

        if denied_reason is None:
            return None

        self._audit_denied(name, action, role, denied_reason)
        return {
            "isError": True,
            "content": [{"type": "text", "text": denied_reason}],
            "structuredContent": {"denied": True, "role": role, "tool": name, "action": action},
        }

    def _action_for(self, name: str, args: dict[str, Any]) -> str:
        if name == "shell":
            return "execute"
        return str(args.get("action", ""))

    def _is_high_risk(self, name: str, action: str) -> bool:
        return (name, action) in {
            ("git", "commit"),
            ("repo", "init"),
            ("repo", "clone"),
            ("shell", "execute"),
        }

    def _audit_denied(self, name: str, action: str, role: str, reason: str) -> None:
        audit = getattr(self.runtime, "audit", None)
        if audit:
            audit.log(
                tool=name,
                action=action,
                success=False,
                duration=0.0,
                error=reason,
                details={"role": role, "denied": True},
            )

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
