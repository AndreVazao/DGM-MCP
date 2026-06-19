from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.mcp.stdio import StdioMCPServer


def test_resources_and_prompts():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    runtime.start()
    server = StdioMCPServer(runtime)

    resources = server.handle({"jsonrpc": "2.0", "id": 10, "method": "resources/list"})
    assert any(item["uri"] == "dgm://config" for item in resources["result"]["resources"])

    config_resource = server.handle(
        {"jsonrpc": "2.0", "id": 11, "method": "resources/read", "params": {"uri": "dgm://config"}}
    )
    assert config_resource["result"]["contents"][0]["mimeType"] == "application/json"

    prompts = server.handle({"jsonrpc": "2.0", "id": 12, "method": "prompts/list"})
    assert any(item["name"] == "task_analysis" for item in prompts["result"]["prompts"])

    prompt = server.handle(
        {
            "jsonrpc": "2.0",
            "id": 13,
            "method": "prompts/get",
            "params": {"name": "task_analysis", "arguments": {"task_description": "Refatorar"}},
        }
    )
    assert "Refatorar" in prompt["result"]["messages"][0]["content"]
