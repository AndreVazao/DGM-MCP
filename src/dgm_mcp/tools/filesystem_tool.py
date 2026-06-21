from .base_tool import BaseTool, ToolResult
import time

class FilesystemTool(BaseTool):
    name = "filesystem"
    description = "Ler, escrever e manipular ficheiros e pastas"

    def execute(self, action: str, path: str, content: str = None, **kwargs) -> ToolResult:
        start_time = time.time()
        success = False
        error = None
        result = None

        try:
            safe_path = self.path_guard.validate_path(path)

            if action == "read":
                if safe_path.exists():
                    result = ToolResult(
                        success=True,
                        message="Ficheiro lido com sucesso",
                        data={"content": safe_path.read_text(encoding="utf-8")}
                    )
                else:
                    result = ToolResult(success=False, message="Ficheiro não encontrado")

            elif action == "write":
                safe_path.parent.mkdir(parents=True, exist_ok=True)
                safe_path.write_text(content or "", encoding="utf-8")
                result = ToolResult(success=True, message="Ficheiro escrito com sucesso")

            else:
                result = ToolResult(success=False, message=f"Ação desconhecida: {action}")

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
                details={"path": path}
            )

        return result
