from __future__ import annotations

from enum import Enum, auto


class MCPState(Enum):
    CREATED = auto()
    INITIALIZING = auto()
    INITIALIZED = auto()
    SHUTDOWN = auto()

