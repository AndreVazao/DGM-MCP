from .base_tool import BaseTool, ToolResult
from pathlib import Path
from rich.console import Console
import difflib

console = Console()

class PatchTool(BaseTool):
    name = "patch"
    description = "Cria, visualiza e aplica patches com preview seguro"

    def execute(self, action: str, file_path: str, content: str = None, **kwargs) -> ToolResult:
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
                console.print("".join(list(diff)[:30]))  # mostra apenas primeiras linhas

                return ToolResult(
                    success=True,
                    message="Preview gerado",
                    data={"path": str(safe_path), "has_changes": old_content != content}
                )

            elif action == "write":
                safe_path.parent.mkdir(parents=True, exist_ok=True)
                safe_path.write_text(content or "", encoding="utf-8")

                return ToolResult(
                    success=True,
                    message=f"Ficheiro escrito com sucesso: {safe_path.name}",
                    data={"path": str(safe_path)}
                )

            return ToolResult(success=False, message=f"Ação inválida: {action}")

        except Exception as e:
            return ToolResult(success=False, message=str(e))
