from .base_tool import BaseTool, ToolResult

import shlex
import subprocess


class ShellTool(BaseTool):
    name = "shell"

    description = "Executa comandos permitidos"

    ALLOWED_COMMANDS = {
        "python",
        "pip",
        "pytest",
        "black",
        "ruff",
        "dir",
        "ls",
        "echo",
    }

    def execute(
        self,
        command: str,
        cwd: str = ".",
        **kwargs,
    ) -> ToolResult:

        try:
            safe_cwd = self.path_guard.validate_path(cwd)

            tokens = shlex.split(command)

            if not tokens:
                return ToolResult(
                    success=False,
                    message="Comando vazio"
                )

            base_command = tokens[0]

            if base_command not in self.ALLOWED_COMMANDS:
                return ToolResult(
                    success=False,
                    message=f"Comando não permitido: {base_command}"
                )

            result = subprocess.run(
                tokens,
                cwd=safe_cwd,
                capture_output=True,
                text=True,
                timeout=30,
                shell=False
            )

            return ToolResult(
                success=result.returncode == 0,
                message="Comando executado",
                data={
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                }
            )

        except subprocess.TimeoutExpired:

            return ToolResult(
                success=False,
                message="Timeout"
            )

        except Exception as e:

            return ToolResult(
                success=False,
                message=str(e)
            )
