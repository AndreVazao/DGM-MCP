from .base_tool import BaseTool, ToolResult
from pathlib import Path
from rich.console import Console
import difflib
import time

console = Console()

class PatchTool(BaseTool):
    name = "patch"
    description = "Cria, visualiza e aplica patches com preview seguro"

    def execute(self, action: str, file_path: str, content: str = None, **kwargs) -> ToolResult:
        start_time = time.time()
        success = False
        error = None
        result = None

        try:
            safe_path = self.path_guard.validate_path(file_path)

            if action == "preview_write":
                old_content = safe_path.read_text(encoding="utf-8") if safe_path.exists() else ""

                console.print(f"\n[bold yellow]📄 Preview: {safe_path.name}[/bold yellow]")
                diff = difflib.unified_diff(
                    old_content.splitlines(keepends=True),
                    (content or "").splitlines(keepends=True),
                    fromfile="original",
                    tofile="novo",
                    lineterm=""
                )
                console.print("".join(list(diff)[:30]))

                result = ToolResult(
                    success=True,
                    message="Preview gerado",
                    data={"path": str(safe_path), "has_changes": old_content != content}
                )

            elif action == "write":
                safe_path.parent.mkdir(parents=True, exist_ok=True)
                safe_path.write_text(content or "", encoding="utf-8")

                result = ToolResult(
                    success=True,
                    message=f"Ficheiro escrito com sucesso: {safe_path.name}",
                    data={"path": str(safe_path)}
                )
            else:
                result = ToolResult(success=False, message=f"Ação inválida: {action}")

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
                details={"file_path": file_path}
            )

        return result
