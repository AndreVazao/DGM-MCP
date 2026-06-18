from pathlib import Path

import json
from datetime import datetime


class AuditLogger:

    def __init__(
        self,
        log_file: str = "audit.log"
    ):
        self.log_file = Path(log_file)

    def log(
        self,
        action: str,
        details: dict
    ):

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "details": details,
        }

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(
                    entry,
                    ensure_ascii=False
                )
            )

            f.write("\n")
