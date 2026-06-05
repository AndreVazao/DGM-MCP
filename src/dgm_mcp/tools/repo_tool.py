from .base_tool import BaseTool, ToolResult
from pathlib import Path
import subprocess

class RepoTool(BaseTool):
    name = "repo"
    description = "Gestão geral do repositório (clone, init, etc.)"

    def execute(self, action: str, path: str = ".", url: str = None, **kwargs) -> ToolResult:
        try:
            safe_path = self.path_guard.validate_path(path)

            if action == "init":
                safe_path.mkdir(parents=True, exist_ok=True)
                subprocess.run(["git", "init"], cwd=safe_path, check=True)
                return ToolResult(success=True, message="Repositório Git inicializado")

            elif action == "clone" and url:
                subprocess.run(["git", "clone", url, str(safe_path)], check=True)
                return ToolResult(success=True, message=f"Repositório clonado de {url}")

            return ToolResult(success=False, message=f"Ação não suportada: {action}")
        except Exception as e:
            return ToolResult(success=False, message=str(e))
