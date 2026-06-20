import pytest
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.mcp.stdio import StdioMCPServer

def test_mcp_metrics_collection():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = StdioMCPServer(runtime)

    obs = runtime.observability
    assert obs.mcp_requests_total == 0

    server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize"}, session_id="s1")
    assert obs.mcp_requests_total == 1
    assert obs.mcp_sessions_created == 1

    server.handle({"jsonrpc": "2.0", "method": "initialized"}, session_id="s1")
    assert obs.mcp_requests_total == 2

    server.handle({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "shell", "arguments": {"command": "echo 1"}}
    }, session_id="s1")

    assert obs.mcp_tool_calls_total == 1
    assert len(obs.mcp_tool_latencies) == 1
    assert obs.average_tool_latency > 0

    server.handle({"jsonrpc": "2.0", "id": 3, "method": "unknown_method"}, session_id="s1")
    assert obs.mcp_protocol_errors == 1
