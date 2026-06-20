from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.mcp.stdio import StdioMCPServer


def test_tool_schema_is_constrained():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = StdioMCPServer(runtime)

    server.handle({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
    server.handle({"jsonrpc": "2.0", "method": "initialized"})
    listed = server.handle({"jsonrpc": "2.0", "id": 99, "method": "tools/list"})
    shell_tool = next(tool for tool in listed["result"]["tools"] if tool["name"] == "shell")

    assert shell_tool["inputSchema"]["additionalProperties"] is False
    assert shell_tool["inputSchema"]["properties"]["command"]["type"] == "string"
