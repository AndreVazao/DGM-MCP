from fastapi.testclient import TestClient

from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.mcp.sse import SSEMCPServer


def test_sse_transport_basic():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = SSEMCPServer(runtime)
    client = TestClient(server.app)

    response = client.get("/mcp/sse")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    client.post(
        "/mcp/message",
        json={"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
    )
    client.post("/mcp/message", json={"jsonrpc": "2.0", "method": "initialized"})

    message = client.post(
        "/mcp/message",
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
    )
    assert message.status_code == 200
    assert "tools" in message.json()["result"]
