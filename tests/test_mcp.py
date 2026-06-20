from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.mcp.stdio import StdioMCPServer


def test_tools_list_and_call():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = StdioMCPServer(runtime)

    server.handle({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
    server.handle({"jsonrpc": "2.0", "method": "initialized"})
    listed = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert listed["result"]["tools"]
    assert any(tool["name"] == "shell" for tool in listed["result"]["tools"])

    response = server.handle(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "shell", "arguments": {"command": "echo hello"}},
        }
    )
    assert response["result"]["isError"] is False
