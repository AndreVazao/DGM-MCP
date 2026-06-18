from pathlib import Path
from typing import Iterable


class PathGuard:
    """
    Validação segura de caminhos.

    Impede:
    - path traversal
    - escapes para fora da whitelist
    - bypass via startswith()
    - symlink escapes (resolve())
    """

    def __init__(self, allowed_paths: Iterable[str]):
        self.allowed_paths = [
            Path(p).expanduser().resolve(strict=False)
            for p in allowed_paths
        ]

    def validate_path(self, path: str | Path) -> Path:
        candidate = Path(path).expanduser().resolve(strict=False)

        for allowed in self.allowed_paths:
            try:
                candidate.relative_to(allowed)
                return candidate
            except ValueError:
                continue

        raise PermissionError(
            f"Path não permitido: {candidate}"
        )

    def is_safe(self, path: str | Path) -> bool:
        try:
            self.validate_path(path)
            return True
        except PermissionError:
            return False
