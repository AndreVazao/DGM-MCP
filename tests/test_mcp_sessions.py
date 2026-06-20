import pytest
import time
from dgm_mcp.mcp.session_manager import SessionManager
from dgm_mcp.mcp.stdio import StdioMCPServer
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.config.config_manager import ConfigManager

def test_session_manager_lifecycle():
    sm = SessionManager(expiration_seconds=1)
    session = sm.create_session("test-sid")
    assert session.id == "test-sid"

    retrieved = sm.get_session("test-sid")
    assert retrieved is session
    assert retrieved.requests_count == 1

    time.sleep(1.1)
    expired = sm.get_session("test-sid")
    assert expired is None

def test_stdio_session_integration():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    server = StdioMCPServer(runtime)

    server.handle({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "clientInfo": {"name": "client-a"},
            "capabilities": {"roots": {"listChanged": True}}
        }
    }, session_id="sid-a")

    assert server.sessions.get_session("sid-a").client_info["name"] == "client-a"
    assert server.sessions.get_session("sid-a").protocol_version == "2025-06-18"

    server.handle({
        "jsonrpc": "2.0", "id": 2, "method": "initialize",
        "params": {"clientInfo": {"name": "client-b"}}
    }, session_id="sid-b")

    assert server.sessions.get_session("sid-b").client_info["name"] == "client-b"
    assert len(server.sessions.list_active_sessions()) == 2

def test_session_statistics():
    sm = SessionManager()
    sm.create_session("s1")
    sm.create_session("s2")
    stats = sm.get_stats()
    assert stats["active_sessions"] == 2
