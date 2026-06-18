from .base_tool import BaseTool, ToolResult
import shlex
import subprocess
import time
from typing import Optional
from ..security.path_guard import PathGuard
from ..security.audit_logger import AuditLogger

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

    def __init__(self, path_guard: PathGuard, audit: Optional[AuditLogger] = None, default_timeout: int = 30):
        super().__init__(path_guard, audit)
        self.default_timeout = default_timeout

    def execute(self, command: str, cwd: str = ".", **kwargs) -> ToolResult:
        start_time = time.time()
        success = False
        error = None
        result = None
        action = command.split()[0] if command else "none"

        try:
            safe_cwd = self.path_guard.validate_path(cwd)
            tokens = shlex.split(command)

            if not tokens:
                result = ToolResult(success=False, message="Comando vazio")
            else:
                base_command = tokens[0]
                if base_command not in self.ALLOWED_COMMANDS:
                    result = ToolResult(
                        success=False,
                        message=f"Comando não permitido: {base_command}"
                    )
                else:
                    timeout = kwargs.get("timeout", self.default_timeout)
                    proc = subprocess.run(
                        tokens,
                        cwd=safe_cwd,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                        shell=False
                    )

                    result = ToolResult(
                        success=proc.returncode == 0,
                        message="Comando executado",
                        data={
                            "stdout": proc.stdout,
                            "stderr": proc.stderr,
                            "returncode": proc.returncode,
                        }
                    )

            success = result.success
            if not success:
                error = result.message

        except subprocess.TimeoutExpired:
            error = "Timeout"
            result = ToolResult(success=False, message=error)
            success = False
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
                details={"command": command, "cwd": cwd}
            )

        return result
