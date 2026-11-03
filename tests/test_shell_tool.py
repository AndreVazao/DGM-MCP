from pathlib import Path
from unittest.mock import MagicMock

from dgm_mcp.security.path_guard import PathGuard
from dgm_mcp.tools.shell_tool import ShellTool


def test_shell_tool_allowed_command():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path.cwd()

    tool = ShellTool(pg)
    result = tool.execute("echo 'hello'")

    assert result.success is True
    assert "hello" in result.data["stdout"]

def test_shell_tool_disallowed_command():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path.cwd()

    tool = ShellTool(pg)
    result = tool.execute("rm -rf /")

    assert result.success is False
    assert "Comando não permitido" in result.message

def test_shell_tool_empty_command():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path.cwd()

    tool = ShellTool(pg)
    result = tool.execute("")

    assert result.success is False
    assert "Comando vazio" in result.message

def test_shell_tool_timeout():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path.cwd()

    tool = ShellTool(pg)
    import subprocess
    from unittest.mock import patch

    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="sleep 60", timeout=30)):
        result = tool.execute("pytest --version")
        assert result.success is False
        assert "Timeout" in result.message
