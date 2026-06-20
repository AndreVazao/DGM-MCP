from __future__ import annotations

from dataclasses import dataclass
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
class JSONRPCPayloadError:
    code: int
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message}


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
    if not isinstance(payload, dict):
        raise TypeError("JSON-RPC payload must be an object")
    if payload.get("jsonrpc") != "2.0":
        raise ValueError("Invalid JSON-RPC version")
    method = payload.get("method")
    if not isinstance(method, str) or not method:
        raise ValueError("Invalid method")
    return JSONRPCRequest(
        jsonrpc=payload["jsonrpc"],
        method=method,
        id=payload.get("id"),
        params=payload.get("params"),
    )


def make_error(id_: int | str | None, code: int, message: str, data: Any | None = None) -> JSONRPCResponse:
    return JSONRPCResponse(id=id_, error=JSONRPCError(code=code, message=message, data=data))


def invalid_request(id_: int | str | None = None) -> JSONRPCResponse:
    return make_error(id_, -32600, "Invalid Request")


def parse_error() -> JSONRPCResponse:
    return make_error(None, -32700, "Parse error")


def method_not_found(id_: int | str | None) -> JSONRPCResponse:
    return make_error(id_, -32601, "Method not found")


def invalid_params(id_: int | str | None = None, data: Any | None = None) -> JSONRPCResponse:
    return make_error(id_, -32602, "Invalid params", data)


def internal_error(id_: int | str | None = None, data: Any | None = None) -> JSONRPCResponse:
    return make_error(id_, -32603, "Internal error", data)
