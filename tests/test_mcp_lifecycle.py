from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.mcp.stdio import StdioMCPServer


def test_shutdown_and_notifications():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = StdioMCPServer(runtime)

    assert server.handle({"jsonrpc": "2.0", "method": "tools/list"}) == {}

    shutdown = server.handle({"jsonrpc": "2.0", "id": 1, "method": "shutdown"})
    assert shutdown["result"]["ok"] is True
