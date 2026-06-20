import json
import pytest
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.mcp.stdio import StdioMCPServer

def test_security_audit():
    config = ConfigManager().load()
    runtime = MCPRuntime(config, quiet=True)
    runtime.start()
    server = StdioMCPServer(runtime)

    # 1. Invalid payload
    resp = server.handle({"invalid": "jsonrpc"})
    assert resp["error"]["code"] == -32600

    # 2. Handshake
    server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
    server.handle({"jsonrpc": "2.0", "method": "initialized"})

    # 3. Path Traversal attempt via filesystem tool
    resp = server.handle({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "filesystem", "arguments": {"action": "read", "path": "../../../etc/passwd"}}
    })
    # PathGuard should block it
    assert resp["result"]["isError"] is True
    assert "Path não permitido" in resp["result"]["content"][0]["text"]

    # 4. Invalid Tool Schema
    resp = server.handle({
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "shell", "arguments": {"invalid_arg": "echo 1"}}
    })
    # jsonschema validation should fail
    assert resp["error"]["code"] == -32602

    with open("SECURITY_AUDIT_V2.md", "w") as f:
        f.write("# SECURITY AUDIT V2\n\n")
        f.write("## 1. JSON-RPC Fuzzing\n- Status: SECURE\n- Details: Invalid payloads correctly return -32600.\n\n")
        f.write("## 2. Path Traversal\n- Status: SECURE\n- Details: PathGuard correctly blocks access outside allowed paths.\n\n")
        f.write("## 3. Schema Validation\n- Status: SECURE\n- Details: Invalid tool arguments return -32602 (Invalid Params).\n")

if __name__ == "__main__":
    test_security_audit()
