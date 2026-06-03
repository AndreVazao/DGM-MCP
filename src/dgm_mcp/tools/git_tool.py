from .base_tool import BaseTool, ToolResult
from pathlib import Path
import subprocess

class GitTool(BaseTool):
    name = "git"
    description = "Executa comandos Git de forma segura"

    def execute(self, action: str, repo_path: str = ".", **kwargs) -> ToolResult:
        try:
            safe_path = self.path_guard.validate_path(repo_path)

            if action == "status":
                result = subprocess.run(["git", "status"], cwd=safe_path, capture_output=True, text=True)
                return ToolResult(
                    success=True,
                    message="Git status obtido",
                    data={"output": result.stdout}
                )

            elif action == "commit":
                msg = kwargs.get("message", "Commit automático DGM-MCP")
                subprocess.run(["git", "add", "."], cwd=safe_path, check=True)
                subprocess.run(["git", "commit", "-m", msg], cwd=safe_path, check=True)
                return ToolResult(success=True, message=f"Commit efetuado: {msg}")

            return ToolResult(success=False, message=f"Ação git não suportada: {action}")

        except Exception as e:
            return ToolResult(success=False, message=str(e))
