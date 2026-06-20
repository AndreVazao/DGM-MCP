import json
import pytest
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.mcp.stdio import StdioMCPServer

def test_full_mcp_lifecycle_stdio():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = StdioMCPServer(runtime)

    # 1. Initialize
    resp = server.handle({
        "jsonrpc": "2.0", "id": "req-1", "method": "initialize",
        "params": {"protocolVersion": "2025-06-18"}
    })
    assert resp["id"] == "req-1"
    assert resp["result"]["protocolVersion"] == "2025-06-18"

    # 2. Initialized
    server.handle({"jsonrpc": "2.0", "method": "initialized"})

    # 3. List tools
    resp = server.handle({"jsonrpc": "2.0", "id": "req-2", "method": "tools/list"})
    assert "tools" in resp["result"]

    # 4. Call tool
    resp = server.handle({
        "jsonrpc": "2.0", "id": "req-3", "method": "tools/call",
        "params": {"name": "shell", "arguments": {"command": "echo hello"}}
    })
    assert resp["result"]["isError"] is False

    # 5. List resources
    resp = server.handle({"jsonrpc": "2.0", "id": "req-4", "method": "resources/list"})
    assert "resources" in resp["result"]

    # 6. Read resource
    resp = server.handle({
        "jsonrpc": "2.0", "id": "req-5", "method": "resources/read",
        "params": {"uri": "dgm://config"}
    })
    assert "contents" in resp["result"]

    # 7. List prompts
    resp = server.handle({"jsonrpc": "2.0", "id": "req-6", "method": "prompts/list"})
    assert "prompts" in resp["result"]

    # 8. Get prompt
    resp = server.handle({
        "jsonrpc": "2.0", "id": "req-7", "method": "prompts/get",
        "params": {"name": "task_analysis", "arguments": {"task_description": "test"}}
    })
    assert "messages" in resp["result"]

    # 9. Shutdown
    resp = server.handle({"jsonrpc": "2.0", "id": "req-8", "method": "shutdown"})
    assert resp["result"]["ok"] is True
