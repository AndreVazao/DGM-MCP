from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import Optional

class MCPConfig(BaseModel):
    allowed_paths: list[str] = ["./", "../projects"]
    max_workers: int = 4
    log_level: str = "INFO"
    enable_approval: bool = True
    default_llm: str = "Claude"
    ollama_model: str = "llama3.2"

class ConfigManager:
    def __init__(self):
        self.config_path = Path("config/config.yaml")

    def load(self) -> MCPConfig:
        if not self.config_path.exists():
            self._create_default()

        with open(self.config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return MCPConfig(**data)

    def _create_default(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        default = MCPConfig()
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(default.model_dump(), f, default_flow_style=False)
