from .base_tool import BaseTool, ToolResult
from pathlib import Path
import subprocess
import time

class RepoTool(BaseTool):
    name = "repo"
    description = "Gestão geral do repositório (clone, init, etc.)"

    def execute(self, action: str, path: str = ".", url: str = None, **kwargs) -> ToolResult:
        start_time = time.time()
        success = False
        error = None
        result = None

        try:
            safe_path = self.path_guard.validate_path(path)

            if action == "init":
                safe_path.mkdir(parents=True, exist_ok=True)
                subprocess.run(["git", "init"], cwd=safe_path, check=True)
                result = ToolResult(success=True, message="Repositório Git inicializado")

            elif action == "clone" and url:
                subprocess.run(["git", "clone", url, str(safe_path)], check=True)
                result = ToolResult(success=True, message=f"Repositório clonado de {url}")
            else:
                result = ToolResult(success=False, message=f"Ação não suportada: {action}")

            success = result.success
            if not success:
                error = result.message

        except Exception as e:
            error = str(e)
            result = ToolResult(success=False, message=error)
            success = False

        duration = time.time() - start_time
        if self.audit:
            self.audit.log(
                tool=self.name,
                action=action,
                success=success,
                duration=duration,
                error=error,
                details={"path": path, "url": url}
            )

        return result
