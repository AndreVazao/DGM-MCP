from .base_tool import BaseTool, ToolResult
import subprocess
import time

class GitTool(BaseTool):
    name = "git"
    description = "Executa comandos Git de forma segura"

    def execute(self, action: str, repo_path: str = ".", **kwargs) -> ToolResult:
        start_time = time.time()
        success = False
        error = None
        result = None

        try:
            safe_path = self.path_guard.validate_path(repo_path)

            if action == "status":
                proc = subprocess.run(
                    ["git", "status"],
                    cwd=safe_path,
                    capture_output=True,
                    text=True
                )

                if proc.returncode != 0:
                    result = ToolResult(
                        success=False,
                        message=f"Git status falhou: {proc.stderr}",
                        data={"returncode": proc.returncode}
                    )
                else:
                    result = ToolResult(
                        success=True,
                        message="Git status obtido",
                        data={"output": proc.stdout}
                    )

            elif action == "commit":
                msg = kwargs.get("message", "Commit automático DGM-MCP")

                # Add
                result_add = subprocess.run(
                    ["git", "add", "."],
                    cwd=safe_path,
                    capture_output=True,
                    text=True
                )
                if result_add.returncode != 0:
                    result = ToolResult(
                        success=False,
                        message=f"Git add falhou: {result_add.stderr}"
                    )
                else:
                    # Commit
                    result_commit = subprocess.run(
                        ["git", "commit", "-m", msg],
                        cwd=safe_path,
                        capture_output=True,
                        text=True
                    )
                    if result_commit.returncode != 0:
                        result = ToolResult(
                            success=False,
                            message=f"Git commit falhou: {result_commit.stderr}"
                        )
                    else:
                        result = ToolResult(
                            success=True,
                            message=f"Commit efetuado: {msg}"
                        )
            else:
                result = ToolResult(
                    success=False,
                    message=f"Ação git não suportada: {action}"
                )

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
                details={"repo_path": repo_path}
            )

        return result
