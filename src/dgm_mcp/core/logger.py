from rich.console import Console
from rich.logging import RichHandler
import logging
from pathlib import Path

console = Console()


class DGMLogger:
    def __init__(self, quiet: bool = False):
        self.logger = logging.getLogger("dgm_mcp")
        self.logger.setLevel(logging.INFO)

        if not quiet:
            handler = RichHandler(console=console, show_time=True, show_path=False)
            self.logger.addHandler(handler)

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "dgm_mcp.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(file_handler)

        self.logger.propagate = False

    def info(self, msg: str):
        self.logger.info(msg)

    def success(self, msg: str):
        self.logger.info(f"OK {msg}")

    def warning(self, msg: str):
        self.logger.warning(f"WARN {msg}")

    def error(self, msg: str):
        self.logger.error(f"ERR {msg}")
