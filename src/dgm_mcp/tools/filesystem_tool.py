from .base_tool import BaseTool, ToolResult
from pathlib import Path

class FilesystemTool(BaseTool):
    name = "filesystem"
    description = "Ler, escrever e manipular ficheiros e pastas"

    def execute(self, action: str, path: str, content: str = None, **kwargs) -> ToolResult:
        try:
            safe_path = self.path_guard.validate_path(path)

            if action == "read":
                if safe_path.exists():
                    return ToolResult(
                        success=True,
                        message="Ficheiro lido com sucesso",
                        data={"content": safe_path.read_text(encoding="utf-8")}
                    )
                return ToolResult(success=False, message="Ficheiro não encontrado")

            elif action == "write":
                safe_path.parent.mkdir(parents=True, exist_ok=True)
                safe_path.write_text(content or "", encoding="utf-8")
                return ToolResult(success=True, message="Ficheiro escrito com sucesso")

            return ToolResult(success=False, message=f"Ação desconhecida: {action}")

        except Exception as e:
            return ToolResult(success=False, message=str(e))
