from typing import Dict, Any
import json
from pathlib import Path
from datetime import datetime

class Memory:
    """Memória persistente simples do DGM-MCP"""

    def __init__(self, runtime):
        self.runtime = runtime
        self.memory_path = Path("memory/dgm_memory.json")
        self.memory_path.parent.mkdir(exist_ok=True)
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict:
        if self.memory_path.exists():
            try:
                return json.loads(self.memory_path.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def save(self):
        self.memory_path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def store(self, key: str, value: Any):
        self.data[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self.save()

    def get(self, key: str, default=None):
        return self.data.get(key, {}).get("value", default)
