from pathlib import Path

from fastapi.testclient import TestClient

from dgm_mcp.config.config_manager import MCPConfig
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.mcp.http import StreamableHTTPMCPServer
from dgm_mcp.mcp.sse import SSEMCPServer
from dgm_mcp.mcp.stdio import StdioMCPServer


def initialized_server(config: MCPConfig) -> StdioMCPServer:
    runtime = MCPRuntime(config, quiet=True)
    runtime.start()
    server = StdioMCPServer(runtime)
    server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
    server.handle({"jsonrpc": "2.0", "method": "initialized"})
    return server


def call_tool(server: StdioMCPServer, name: str, arguments: dict, role: str = "developer"):
    return server.handle(
        {
            "jsonrpc": "2.0",
            "id": "tool-call",
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
        role=role,
    )


def test_developer_can_write_and_read_allowed_file(tmp_path: Path):
    config = MCPConfig(allowed_paths=[str(tmp_path)], default_llm="", mcp_default_role="developer")
    server = initialized_server(config)
    target = tmp_path / "note.txt"

    write = call_tool(server, "filesystem", {"action": "write", "path": str(target), "content": "hello"})
    assert write["result"]["isError"] is False

    read = call_tool(server, "filesystem", {"action": "read", "path": str(target)})
    assert read["result"]["structuredContent"]["content"] == "hello"


def test_reader_cannot_write(tmp_path: Path):
    config = MCPConfig(allowed_paths=[str(tmp_path)], default_llm="")
    server = initialized_server(config)

    response = call_tool(
        server,
        "filesystem",
        {"action": "write", "path": str(tmp_path / "blocked.txt"), "content": "nope"},
        role="reader",
    )

    assert response["result"]["isError"] is True
    assert "cannot perform 'write'" in response["result"]["content"][0]["text"]


def test_path_guard_blocks_outside_allowed_path(tmp_path: Path):
    config = MCPConfig(allowed_paths=[str(tmp_path)], default_llm="")
    server = initialized_server(config)

    response = call_tool(server, "filesystem", {"action": "read", "path": str(tmp_path.parent / "outside.txt")})

    assert response["result"]["isError"] is True
    assert "Path" in response["result"]["content"][0]["text"]


def test_developer_cannot_commit_or_clone_by_default(tmp_path: Path):
    config = MCPConfig(allowed_paths=[str(tmp_path)], default_llm="", mcp_default_role="developer")
    server = initialized_server(config)

    commit = call_tool(server, "git", {"action": "commit", "repo_path": str(tmp_path), "message": "no"})
    clone = call_tool(server, "repo", {"action": "clone", "path": str(tmp_path / "repo"), "url": "https://example.invalid/repo.git"})

    assert commit["result"]["isError"] is True
    assert clone["result"]["isError"] is True

    shell = call_tool(server, "shell", {"command": "echo should-not-run", "cwd": str(tmp_path)})
    assert shell["result"]["isError"] is True
    assert "cannot use tool 'shell'" in shell["result"]["content"][0]["text"]


def test_admin_shell_requires_high_risk_opt_in_and_python_is_not_allowlisted(tmp_path: Path):
    config = MCPConfig(allowed_paths=[str(tmp_path)], default_llm="", mcp_high_risk_enabled=False)
    server = initialized_server(config)

    blocked = call_tool(server, "shell", {"command": "echo blocked", "cwd": str(tmp_path)}, role="admin")
    assert blocked["result"]["isError"] is True
    assert "High-risk action disabled" in blocked["result"]["content"][0]["text"]

    config.mcp_high_risk_enabled = True
    enabled_server = initialized_server(config)
    allowed = call_tool(enabled_server, "shell", {"command": "echo allowed", "cwd": str(tmp_path)}, role="admin")
    assert allowed["result"]["isError"] is False

    python = call_tool(enabled_server, "shell", {"command": "python -c \"print(1)\"", "cwd": str(tmp_path)}, role="admin")
    assert python["result"]["isError"] is True
    assert "Comando não permitido: python" in python["result"]["content"][0]["text"]


def test_http_mcp_requires_auth_when_enabled(tmp_path: Path):
    config = MCPConfig(
        allowed_paths=[str(tmp_path)],
        default_llm="",
        mcp_auth_required=True,
        mcp_api_key="test-secret",
    )
    runtime = MCPRuntime(config, quiet=True)
    runtime.start()
    client = TestClient(StreamableHTTPMCPServer(runtime).app)

    unauthorized = client.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert unauthorized.status_code == 401

    authorized = client.post(
        "/mcp",
        headers={"Authorization": "Bearer test-secret"},
        json={"jsonrpc": "2.0", "id": 1, "method": "initialize"},
    )
    assert authorized.status_code == 200


def test_config_resource_redacts_secrets(tmp_path: Path):
    config = MCPConfig(allowed_paths=[str(tmp_path)], default_llm="", mcp_api_key="test-secret", openai_key="sk-testsecret")
    server = initialized_server(config)

    response = server.handle({"jsonrpc": "2.0", "id": 2, "method": "resources/read", "params": {"uri": "dgm://config"}})
    text = response["result"]["contents"][0]["text"]

    assert "test-secret" not in text
    assert "sk-testsecret" not in text
    assert "[configured]" in text


def test_sse_mcp_requires_auth_when_enabled(tmp_path: Path):
    config = MCPConfig(
        allowed_paths=[str(tmp_path)],
        default_llm="",
        mcp_auth_required=True,
        mcp_api_key="test-secret",
    )
    runtime = MCPRuntime(config, quiet=True)
    runtime.start()
    client = TestClient(SSEMCPServer(runtime).app)

    unauthorized = client.get("/mcp/sse")
    assert unauthorized.status_code == 401

    authorized = client.get("/mcp/sse", headers={"Authorization": "Bearer test-secret"})
    assert authorized.status_code == 200


def test_http_role_header_cannot_escalate_default_developer_role(tmp_path: Path):
    from starlette.requests import Request

    config = MCPConfig(
        allowed_paths=[str(tmp_path)],
        default_llm="",
        mcp_default_role="developer",
        mcp_allow_role_header=False,
        mcp_high_risk_enabled=True,
    )
    runtime = MCPRuntime(config, quiet=True)
    runtime.start()
    server = StreamableHTTPMCPServer(runtime)
    request = Request({
        "type": "http",
        "headers": [(b"x-dgm-role", b"admin")],
    })

    assert server._role_for(request) == "developer"
