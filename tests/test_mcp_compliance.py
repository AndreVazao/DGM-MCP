from fastapi.testclient import TestClient

from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.mcp.http import StreamableHTTPMCPServer
from dgm_mcp.mcp.stdio import StdioMCPServer


def _runtime():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    return runtime


def test_jsonrpc_invalid_request_before_initialize():
    server = StdioMCPServer(_runtime())
    response = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert response["error"]["code"] == -32000
    assert response["error"]["message"] == "Server not initialized"


def test_jsonrpc_parse_error_from_invalid_payload():
    server = StdioMCPServer(_runtime())
    response = server.handle("not-a-dict")
    assert response["error"]["code"] == -32600


def test_initialize_and_initialized_state():
    server = StdioMCPServer(_runtime())
    init = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}})
    assert init["result"]["protocolVersion"] == "2025-03-26"
    assert server.handle({"jsonrpc": "2.0", "method": "initialized"}) == {}
    listed = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    assert "tools" in listed["result"]


def test_invalid_params_on_bad_tool_arguments():
    server = StdioMCPServer(_runtime())
    server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
    server.handle({"jsonrpc": "2.0", "method": "initialized"})
    response = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "shell", "arguments": "bad"}})
    assert response["error"]["code"] == -32602


def test_http_session_headers_and_version_negotiation():
    runtime = _runtime()
    server = StreamableHTTPMCPServer(runtime)
    client = TestClient(server.app)
    response = client.post(
        "/mcp",
        headers={"MCP-Protocol-Version": "2025-03-26"},
        json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}},
    )
    assert response.headers["mcp-session-id"]
    assert response.headers["mcp-protocol-version"] == "2025-03-26"
