from pathlib import Path
import yaml
import os
from pydantic import BaseModel
from typing import Optional, Any, Dict

class MCPConfig(BaseModel):
    allowed_paths: list[str] = ["./", "../projects", "."]
    max_workers: int = 4
    log_level: str = "INFO"
    enable_approval: bool = True
    default_llm: str = "Claude"
    ollama_model: str = "llama3.2"
    ollama_url: str = "http://localhost:11434"
    max_tool_execution_seconds: int = 30
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    google_key: Optional[str] = None
    xai_key: Optional[str] = None

    # RBAC: role -> list of tool names
    roles: Dict[str, list[str]] = {
        "reader": ["filesystem"],
        "developer": ["filesystem", "git", "patch"],
        "admin": ["filesystem", "git", "patch", "shell", "repo"]
    }

class ConfigManager:
    def __init__(self):
        self.config_path = Path("config/config.yaml")

    def load(self) -> MCPConfig:
        data = {}
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

        config = MCPConfig(**data)
        self._override_from_env(config)
        return config

    def _override_from_env(self, config: MCPConfig):
        env_map = {
            "DGM_ALLOWED_PATHS": "allowed_paths",
            "DGM_MAX_WORKERS": "max_workers",
            "DGM_LOG_LEVEL": "log_level",
            "DGM_ENABLE_APPROVAL": "enable_approval",
            "DGM_DEFAULT_LLM": "default_llm",
            "OLLAMA_MODEL": "ollama_model",
            "OLLAMA_URL": "ollama_url",
            "MAX_TOOL_EXECUTION_SECONDS": "max_tool_execution_seconds",
            "OPENAI_API_KEY": "openai_key",
            "ANTHROPIC_API_KEY": "anthropic_key",
            "GOOGLE_API_KEY": "google_key",
            "XAI_API_KEY": "xai_key",
        }

        for env_var, attr in env_map.items():
            val = os.getenv(env_var)
            if val is not None:
                if attr == "allowed_paths":
                    setattr(config, attr, val.split(","))
                elif attr in ["max_workers", "max_tool_execution_seconds"]:
                    setattr(config, attr, int(val))
                elif attr == "enable_approval":
                    setattr(config, attr, val.lower() in ["true", "1", "yes"])
                else:
                    setattr(config, attr, val)

    def _create_default(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        default = MCPConfig()
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(default.model_dump(), f, default_flow_style=False)
