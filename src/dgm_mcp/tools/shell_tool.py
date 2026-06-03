from .base_tool import BaseTool, ToolResult
import subprocess

class ShellTool(BaseTool):
    name = "shell"
    description = "Executa comandos shell de forma controlada"

    ALLOWED_COMMANDS = ["ls", "dir", "echo", "python", "pip", "pytest", "black", "ruff"]

    def execute(self, command: str, cwd: str = ".", **kwargs) -> ToolResult:
        try:
            safe_cwd = self.path_guard.validate_path(cwd)

            # Segurança básica
            cmd_base = command.split()[0] if command else ""
            if cmd_base not in self.ALLOWED_COMMANDS:
                return ToolResult(success=False, message=f"Comando não permitido: {cmd_base}")

            result = subprocess.run(command, shell=True, cwd=safe_cwd, capture_output=True, text=True, timeout=30)

            return ToolResult(
                success=result.returncode == 0,
                message="Comando executado",
                data={
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
            )
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, message="Comando excedeu o tempo limite")
        except Exception as e:
            return ToolResult(success=False, message=str(e))
