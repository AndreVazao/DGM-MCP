from __future__ import annotations
import base64
from typing import Any, TypeVar, Generic, Sequence

T = TypeVar("T")

class Paginator(Generic[T]):
    def __init__(self, items: Sequence[T], default_page_size: int = 50):
        self.items = items
        self.default_page_size = default_page_size

    def get_page(self, cursor: str | None = None) -> tuple[list[T], str | None]:
        offset = 0
        if cursor:
            try:
                decoded = base64.b64decode(cursor).decode("utf-8")
                offset = int(decoded)
            except (ValueError, TypeError, base64.binascii.Error):
                offset = 0

        page = self.items[offset : offset + self.default_page_size]
        next_offset = offset + self.default_page_size

        next_cursor = None
        if next_offset < len(self.items):
            next_cursor = base64.b64encode(str(next_offset).encode("utf-8")).decode("utf-8")

        return list(page), next_cursor
