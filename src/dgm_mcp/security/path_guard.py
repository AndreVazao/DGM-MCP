from pathlib import Path
from typing import List

class PathGuard:
    """Protege o sistema contra acessos fora das pastas permitidas"""

    def __init__(self, allowed_paths: List[str]):
        self.allowed_paths = [Path(p).resolve() for p in allowed_paths]

    def validate_path(self, path: str | Path) -> Path:
        """Valida e retorna o path absoluto se for seguro"""
        abs_path = Path(path).resolve()

        for allowed in self.allowed_paths:
            if str(abs_path).startswith(str(allowed)):
                return abs_path

        raise PermissionError(f"Path não permitido: {abs_path}")

    def is_safe(self, path: str | Path) -> bool:
        try:
            self.validate_path(path)
            return True
        except PermissionError:
            return False
