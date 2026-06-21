from datetime import datetime
import uuid

class Session:
    def __init__(self, session_id: str = None):
        self.id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.messages = []
        self.context = {}

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_context(self) -> str:
        return "\n".join([f"{m['role']}: {m['content'][:300]}" for m in self.messages[-10:]])
