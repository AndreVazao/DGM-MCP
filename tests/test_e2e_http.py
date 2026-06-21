from fastapi.testclient import TestClient
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.mcp.http import StreamableHTTPMCPServer

def test_full_mcp_lifecycle_http():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = StreamableHTTPMCPServer(runtime)
    client = TestClient(server.app)

    # 1. Initialize
    resp = client.post("/mcp", json={
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18"}
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"]["protocolVersion"] == "2025-06-18"
    session_id = resp.headers.get("MCP-Session-Id")
    assert session_id is not None

    # 2. Initialized
    resp = client.post("/mcp", json={"jsonrpc": "2.0", "method": "initialized"},
                       headers={"MCP-Session-Id": session_id})
    assert resp.status_code == 202

    # 3. List tools
    resp = client.post("/mcp", json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                       headers={"MCP-Session-Id": session_id})
    assert resp.status_code == 200
    assert "tools" in resp.json()["result"]

    # 4. List resources
    resp = client.post("/mcp", json={"jsonrpc": "2.0", "id": 3, "method": "resources/list"},
                       headers={"MCP-Session-Id": session_id})
    assert resp.status_code == 200
    assert "resources" in resp.json()["result"]

    # 5. List prompts
    resp = client.post("/mcp", json={"jsonrpc": "2.0", "id": 4, "method": "prompts/list"},
                       headers={"MCP-Session-Id": session_id})
    assert resp.status_code == 200
    assert "prompts" in resp.json()["result"]

    # 6. Shutdown
    resp = client.post("/mcp", json={"jsonrpc": "2.0", "id": 5, "method": "shutdown"},
                       headers={"MCP-Session-Id": session_id})
    assert resp.status_code == 200
    assert resp.json()["result"]["ok"] is True
