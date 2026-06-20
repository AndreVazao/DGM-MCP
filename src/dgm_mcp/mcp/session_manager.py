from __future__ import annotations
import uuid
import time
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class MCPSession:
    id: str
    protocol_version: str | None = None
    capabilities: Dict[str, Any] = field(default_factory=dict)
    client_info: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    requests_count: int = 0

    def touch(self):
        self.last_seen = time.time()
        self.requests_count += 1

class SessionManager:
    def __init__(self, expiration_seconds: int = 3600):
        self.sessions: Dict[str, MCPSession] = {}
        self.expiration_seconds = expiration_seconds

    def create_session(self, session_id: str | None = None) -> MCPSession:
        sid = session_id or str(uuid.uuid4())
        session = MCPSession(id=sid)
        self.sessions[sid] = session
        return session

    def get_session(self, session_id: str) -> MCPSession | None:
        session = self.sessions.get(session_id)
        if session:
            if time.time() - session.last_seen > self.expiration_seconds:
                del self.sessions[session_id]
                return None
            session.touch()
        return session

    def list_active_sessions(self) -> list[MCPSession]:
        self._cleanup()
        return list(self.sessions.values())

    def _cleanup(self):
        now = time.time()
        expired = [sid for sid, s in self.sessions.items() if now - s.last_seen > self.expiration_seconds]
        for sid in expired:
            del self.sessions[sid]

    def get_stats(self) -> Dict[str, Any]:
        self._cleanup()
        return {
            "total_created": len(self.sessions),
            "active_sessions": len(self.sessions)
        }
