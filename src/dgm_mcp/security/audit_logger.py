from pathlib import Path
import json
from datetime import datetime
from typing import Optional, Any

class AuditLogger:
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = Path(log_file)

    def log(
        self,
        tool: str,
        action: str,
        success: bool,
        duration: float,
        error: Optional[str] = None,
        details: Optional[dict[str, Any]] = None
    ):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "tool": tool,
            "action": action,
            "success": success,
            "error": error,
            "duration_seconds": round(duration, 4),
            "details": details or {},
        }

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False))
                f.write("\n")
        except Exception as e:
            # Fallback to printing if file writing fails
            print(f"FAILED TO WRITE AUDIT LOG: {e}")
