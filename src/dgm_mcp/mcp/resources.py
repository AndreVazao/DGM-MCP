from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from datetime import datetime
from jsonschema import validate

from ..llm.prompts import Prompts
from .pagination import Paginator


@dataclass
class MCPResource:
    uri: str
    name: str
    description: str
    mimeType: str


class ResourceRegistry:
    def __init__(self, runtime):
        self.runtime = runtime

    def list_resources(self, cursor: str | None = None) -> tuple[list[dict[str, Any]], str | None]:
        resources = [
            {
                "uri": "dgm://config",
                "name": "config",
                "description": "Runtime configuration snapshot",
                "mimeType": "application/json",
            },
            {
                "uri": "dgm://logs",
                "name": "logs",
                "description": "Recent runtime log file",
                "mimeType": "text/plain",
            },
            {
                "uri": "dgm://tools",
                "name": "tools",
                "description": "List of available tools and their schemas",
                "mimeType": "application/json",
            },
            {
                "uri": "dgm://metrics",
                "name": "metrics",
                "description": "Real-time system performance metrics",
                "mimeType": "application/json",
            },
            {
                "uri": "dgm://sessions",
                "name": "sessions",
                "description": "Active MCP sessions status",
                "mimeType": "application/json",
            },
            {
                "uri": "dgm://runtime",
                "name": "runtime",
                "description": "Runtime engine status and health",
                "mimeType": "application/json",
            },
        ]
        sorted_resources = sorted(resources, key=lambda x: x["uri"])
        paginator = Paginator(sorted_resources)
        return paginator.get_page(cursor)

    def read_resource(self, uri: str) -> dict[str, Any]:
        if uri == "dgm://config":
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": self.runtime.config.model_dump_json(indent=2),
                    }
                ]
            }

        if uri == "dgm://logs":
            log_path = Path("logs") / "dgm_mcp.log"
            text = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "text/plain",
                        "text": text[-8000:],
                    }
                ]
            }

        if uri == "dgm://tools":
            tools = [
                {"name": t.name, "description": t.description}
                for t in self.runtime.tools.values()
            ]
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(tools, indent=2),
                    }
                ]
            }

        if uri == "dgm://metrics":
            obs = self.runtime.observability
            metrics = {
                "tasks_total": obs.tasks_total,
                "tasks_success": obs.tasks_success,
                "tasks_failed": obs.tasks_failed,
                "tool_calls": obs.tool_calls,
                "mcp_requests_total": obs.mcp_requests_total,
                "mcp_tool_calls_total": obs.mcp_tool_calls_total,
                "average_latency": obs.average_tool_latency,
                "uptime": str(datetime.now() - self.runtime.observability.start_time)
            }
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(metrics, indent=2, default=str),
                    }
                ]
            }

        if uri == "dgm://sessions":
            sessions_info = []
            if self.runtime.mcp_sessions:
                for s in self.runtime.mcp_sessions.sessions.values():
                    sessions_info.append(asdict(s))
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(sessions_info, indent=2, default=str),
                    }
                ]
            }

        if uri == "dgm://runtime":
            status = {
                "running": self.runtime.running,
                "llm_provider": self.runtime.llm_manager.current_provider.name if self.runtime.llm_manager.current_provider else None,
                "tools_count": len(self.runtime.tools)
            }
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(status, indent=2),
                    }
                ]
            }

        raise KeyError(f"Unknown resource: {uri}")


class PromptRegistry:
    def __init__(self):
        self._prompts = {
            "system_engineer": {
                "name": "system_engineer",
                "description": "Base system prompt for the engineering agent",
                "version": "1.0.0",
                "tags": ["core", "system"],
                "arguments": [],
                "argument_schema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            },
            "task_analysis": {
                "name": "task_analysis",
                "description": "Prompt template for planning a task",
                "version": "1.0.0",
                "tags": ["planning"],
                "arguments": [
                    {
                        "name": "task_description",
                        "description": "Detailed description of the task to analyze",
                        "required": True
                    }
                ],
                "argument_schema": {
                    "type": "object",
                    "properties": {
                        "task_description": {"type": "string"}
                    },
                    "required": ["task_description"],
                    "additionalProperties": False
                }
            },
        }

    def list_prompts(self, cursor: str | None = None) -> tuple[list[dict[str, Any]], str | None]:
        prompt_list = []
        for p in self._prompts.values():
            prompt_list.append({
                "name": p["name"],
                "description": p["description"],
                "arguments": p["arguments"],
            })
        sorted_prompts = sorted(prompt_list, key=lambda x: x["name"])
        paginator = Paginator(sorted_prompts)
        return paginator.get_page(cursor)

    def get_prompt(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        prompt_def = self._prompts.get(name)
        if not prompt_def:
            raise KeyError(f"Unknown prompt: {name}")

        args = arguments or {}
        # Validation
        validate(instance=args, schema=prompt_def["argument_schema"])

        if name == "system_engineer":
            return {"description": "Base system prompt", "messages": [{"role": "system", "content": Prompts.SYSTEM_ENGINEER.strip()}]}

        if name == "task_analysis":
            return {
                "description": "Task analysis prompt",
                "messages": [
                    {
                        "role": "user",
                        "content": Prompts.TASK_ANALYSIS.format(
                            task_description=args.get("task_description", "")
                        ).strip(),
                    }
                ],
            }
        raise KeyError(f"Implementation missing for prompt: {name}")
