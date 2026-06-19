from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..llm.prompts import Prompts


@dataclass
class MCPResource:
    uri: str
    name: str
    description: str
    mimeType: str


class ResourceRegistry:
    def __init__(self, runtime):
        self.runtime = runtime

    def list_resources(self) -> list[dict[str, Any]]:
        return [
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
        ]

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

        raise KeyError(f"Unknown resource: {uri}")


class PromptRegistry:
    def list_prompts(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "system_engineer",
                "description": "Base system prompt for the engineering agent",
                "arguments": [],
            },
            {
                "name": "task_analysis",
                "description": "Prompt template for planning a task",
                "arguments": [{"name": "task_description", "required": True}],
            },
        ]

    def get_prompt(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        arguments = arguments or {}
        if name == "system_engineer":
            return {"description": "Base system prompt", "messages": [{"role": "system", "content": Prompts.SYSTEM_ENGINEER.strip()}]}
        if name == "task_analysis":
            return {
                "description": "Task analysis prompt",
                "messages": [
                    {
                        "role": "user",
                        "content": Prompts.TASK_ANALYSIS.format(
                            task_description=arguments.get("task_description", "")
                        ).strip(),
                    }
                ],
            }
        raise KeyError(f"Unknown prompt: {name}")

