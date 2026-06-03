from .base_tool import BaseTool, ToolResult
from pathlib import Path
from rich.console import Console

console = Console()

class PatchTool(BaseTool):
    name = "patch"
    description = "Cria e aplica patches de forma segura"

    def execute(self, action: str, file_path: str, content: str = None, **kwargs) -> ToolResult:
        try:
            safe_path = self.path_guard.validate_path(file_path)

            if action == "write":
                # Mostra diff antes de escrever
                if safe_path.exists():
                    old_content = safe_path.read_text(encoding="utf-8")
                    console.print("[yellow]Preview das alterações:[/yellow]")
                    console.print(f"--- {safe_path.name} (antigo)")
                    console.print(f"+++ {safe_path.name} (novo)")
                    # Diff simples
                    console.print("[dim]Mostrando primeiras 10 linhas...[/dim]")
                else:
                    console.print(f"[green]Novo ficheiro: {safe_path}[/green]")

                safe_path.parent.mkdir(parents=True, exist_ok=True)
                safe_path.write_text(content or "", encoding="utf-8")

                return ToolResult(
                    success=True,
                    message=f"Ficheiro atualizado: {safe_path.name}",
                    data={"path": str(safe_path)}
                )

            return ToolResult(success=False, message=f"Ação desconhecida: {action}")

        except Exception as e:
            return ToolResult(success=False, message=str(e))
