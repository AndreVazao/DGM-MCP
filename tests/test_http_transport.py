from fastapi.testclient import TestClient

from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.mcp.http import StreamableHTTPMCPServer


def test_streamable_http_transport():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = StreamableHTTPMCPServer(runtime)
    client = TestClient(server.app)

    response = client.get("/mcp")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    client.post(
        "/mcp",
        headers={"MCP-Protocol-Version": "2025-06-18"},
        json={"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
    )
    client.post("/mcp", headers={"MCP-Protocol-Version": "2025-06-18"}, json={"jsonrpc": "2.0", "method": "initialized"})

    post = client.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert post.status_code == 200
    assert "tools" in post.json()["result"]
