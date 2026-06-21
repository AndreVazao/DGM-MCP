from dgm_mcp.mcp.pagination import Paginator
from dgm_mcp.mcp.tool_registry import ToolRegistry
from dgm_mcp.mcp.resources import ResourceRegistry, PromptRegistry
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.config.config_manager import ConfigManager

def test_paginator_basic():
    items = list(range(100))
    paginator = Paginator(items, default_page_size=30)

    page1, cursor1 = paginator.get_page()
    assert len(page1) == 30
    assert page1 == list(range(30))
    assert cursor1 is not None

    page2, cursor2 = paginator.get_page(cursor1)
    assert len(page2) == 30
    assert page2 == list(range(30, 60))
    assert cursor2 is not None

    page3, cursor3 = paginator.get_page(cursor2)
    assert len(page3) == 30
    assert page3 == list(range(60, 90))

    page4, cursor4 = paginator.get_page(cursor3)
    assert len(page4) == 10
    assert page4 == list(range(90, 100))
    assert cursor4 is None

def test_tool_registry_pagination():
    registry = ToolRegistry()
    for i in range(10):
        registry.register(f"tool_{i:02d}", f"desc {i}", {})

    tools, next_cursor = registry.list_tools()
    assert len(tools) == 10
    assert next_cursor is None
    assert tools[0]["name"] == "tool_00"
    assert tools[-1]["name"] == "tool_09"

def test_resource_and_prompt_pagination():
    config = ConfigManager().load()
    runtime = MCPRuntime(config)
    res_registry = ResourceRegistry(runtime)
    prompt_registry = PromptRegistry()

    resources, res_cursor = res_registry.list_resources()
    assert len(resources) >= 6
    assert res_cursor is None

    prompts, prompt_cursor = prompt_registry.list_prompts()
    assert len(prompts) >= 2
    assert prompt_cursor is None
