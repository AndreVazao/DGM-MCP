from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class JSONRPCError:
    code: int
    message: str
    data: Any | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {"code": self.code, "message": self.message}
        if self.data is not None:
            payload["data"] = self.data
        return payload


@dataclass
class JSONRPCRequest:
    jsonrpc: str
    method: str
    id: int | str | None = None
    params: Any | None = None


@dataclass
class JSONRPCResponse:
    jsonrpc: str = "2.0"
    id: int | str | None = None
    result: Any | None = None
    error: JSONRPCError | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {"jsonrpc": self.jsonrpc, "id": self.id}
        if self.error is not None:
            payload["error"] = self.error.to_dict()
        else:
            payload["result"] = self.result
        return payload


def parse_request(payload: dict[str, Any]) -> JSONRPCRequest:
    return JSONRPCRequest(
        jsonrpc=payload.get("jsonrpc", ""),
        method=payload.get("method", ""),
        id=payload.get("id"),
        params=payload.get("params"),
    )


def make_error(id_: int | str | None, code: int, message: str, data: Any | None = None) -> JSONRPCResponse:
    return JSONRPCResponse(id=id_, error=JSONRPCError(code=code, message=message, data=data))

