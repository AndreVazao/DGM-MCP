import pytest
from unittest.mock import MagicMock, patch
from dgm_mcp.tools.git_tool import GitTool
from dgm_mcp.security.path_guard import PathGuard
from pathlib import Path
import subprocess

def test_git_tool_status_success():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path(".").resolve()

    tool = GitTool(pg)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["git", "status"],
            returncode=0,
            stdout="On branch main",
            stderr=""
        )

        result = tool.execute("status")
        assert result.success is True
        assert "On branch main" in result.data["output"]

def test_git_tool_status_failure():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path(".").resolve()

    tool = GitTool(pg)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["git", "status"],
            returncode=128,
            stdout="",
            stderr="fatal: not a git repository"
        )

        result = tool.execute("status")
        assert result.success is False
        assert "Git status falhou" in result.message

def test_git_tool_commit_success():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path(".").resolve()

    tool = GitTool(pg)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["git", "add", "."],
            returncode=0
        )

        result = tool.execute("commit", message="Test commit")
        assert result.success is True
        assert "Commit efetuado" in result.message

def test_git_tool_commit_failure_add():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path(".").resolve()

    tool = GitTool(pg)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["git", "add", "."],
            returncode=1,
            stderr="error: could not add files"
        )

        result = tool.execute("commit")
        assert result.success is False
        assert "Git add falhou" in result.message

def test_git_tool_unsupported_action():
    pg = MagicMock(spec=PathGuard)
    pg.validate_path.return_value = Path(".").resolve()

    tool = GitTool(pg)
    result = tool.execute("push")

    assert result.success is False
    assert "Ação git não suportada" in result.message
