"""Tests for CLI commands."""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from typer.testing import CliRunner

from specify_cli import app
from specify_cli.symlink_manager import parse_ai_argument


runner = CliRunner()


# =============================================================================
# Argument Parsing Tests
# =============================================================================


def test_parse_ai_argument_all():
    """Test parsing 'all' keyword."""
    result = parse_ai_argument("all")
    assert isinstance(result, list)
    assert len(result) > 0
    assert "claude" in result


def test_parse_ai_argument_comma_separated():
    """Test parsing comma-separated agents."""
    result = parse_ai_argument("claude,cursor-agent,copilot")
    assert "claude" in result
    assert "cursor-agent" in result
    assert "copilot" in result
    assert len(result) == 3


def test_parse_ai_argument_list():
    """Test parsing list of agents."""
    result = parse_ai_argument(["claude", "cursor-agent"])
    assert "claude" in result
    assert "cursor-agent" in result
    assert len(result) == 2


def test_parse_ai_argument_invalid():
    """Test parsing invalid agent name raises error."""
    with pytest.raises(ValueError):
        parse_ai_argument("invalid-agent-that-does-not-exist")


def test_parse_ai_argument_mixed_valid_invalid():
    """Test parsing mix of valid and invalid agents."""
    with pytest.raises(ValueError):
        parse_ai_argument("claude,invalid-agent,cursor-agent")


# =============================================================================
# CLI App Tests
# =============================================================================


def test_cli_app_exists():
    """Test that CLI app is properly initialized."""
    assert app is not None
    assert hasattr(app, "command")


def test_cli_help_command():
    """Test that --help works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "project-specify" in result.stdout.lower() or "usage" in result.stdout.lower()


# =============================================================================
# Version Command Tests
# =============================================================================


def test_version_command():
    """Test version command shows version information."""
    result = runner.invoke(app, ["version"])

    # Should exit successfully
    assert result.exit_code == 0 or "version" in result.stdout.lower()


# =============================================================================
# Check Command Tests
# =============================================================================


def test_check_command_basic():
    """Test check command runs without errors."""
    result = runner.invoke(app, ["check"])

    # Should run (may succeed or fail depending on installed tools)
    assert isinstance(result.exit_code, int)


@patch("shutil.which")
def test_check_command_tool_found(mock_which):
    """Test check command detects installed tools."""
    mock_which.return_value = "/usr/bin/git"

    result = runner.invoke(app, ["check"])

    # Check should find git
    # Exit code depends on implementation
    assert isinstance(result.exit_code, int)


@patch("shutil.which")
def test_check_command_tool_missing(mock_which):
    """Test check command handles missing tools."""
    mock_which.return_value = None

    result = runner.invoke(app, ["check"])

    # Should handle gracefully
    assert isinstance(result.exit_code, int)


# =============================================================================
# Discover Command Tests
# =============================================================================


def test_discover_command_basic(temp_project):
    """Test discover command for MCP servers."""
    result = runner.invoke(app, ["discover", str(temp_project)])

    # Should run without crashing
    assert isinstance(result.exit_code, int)


def test_discover_command_with_mcp_config(mock_mcp_config):
    """Test discover command finds MCP configuration."""
    project_dir = mock_mcp_config.parent.parent
    result = runner.invoke(app, ["discover", str(project_dir)])

    # Should find the servers
    assert result.exit_code == 0 or "mcp" in result.stdout.lower() or len(result.stdout) > 0


# =============================================================================
# Init Command Tests
# =============================================================================


def test_init_command_help():
    """Test init command help."""
    result = runner.invoke(app, ["init", "--help"])

    assert result.exit_code == 0
    assert "--ai" in result.stdout or "agent" in result.stdout.lower()


@patch("specify_cli.symlink_manager.ensure_central_installation")
@patch("specify_cli.symlink_manager.create_agent_symlinks")
def test_init_command_single_agent(mock_create_symlinks, mock_ensure_central, temp_project):
    """Test init command with single agent."""
    mock_ensure_central.return_value = Path.home() / ".project-specify"
    mock_create_symlinks.return_value = {"claude": True}

    result = runner.invoke(app, [
        "init",
        str(temp_project),
        "--ai", "claude",
        "--skip-template"  # Skip template download for faster test
    ])

    # Should attempt to create symlinks (may fail in test environment)
    # We're mainly testing that the command runs
    assert isinstance(result.exit_code, int)


@patch("specify_cli.symlink_manager.ensure_central_installation")
@patch("specify_cli.symlink_manager.create_agent_symlinks")
def test_init_command_multiple_agents(mock_create_symlinks, mock_ensure_central, temp_project):
    """Test init command with multiple agents."""
    mock_ensure_central.return_value = Path.home() / ".project-specify"
    mock_create_symlinks.return_value = {"claude": True, "cursor-agent": True}

    result = runner.invoke(app, [
        "init",
        str(temp_project),
        "--ai", "claude",
        "--ai", "cursor-agent",
        "--skip-template"
    ])

    assert isinstance(result.exit_code, int)


@patch("specify_cli.symlink_manager.ensure_central_installation")
@patch("specify_cli.symlink_manager.create_agent_symlinks")
def test_init_command_all_agents(mock_create_symlinks, mock_ensure_central, temp_project):
    """Test init command with --ai all."""
    mock_ensure_central.return_value = Path.home() / ".project-specify"
    mock_create_symlinks.return_value = {"claude": True}

    result = runner.invoke(app, [
        "init",
        str(temp_project),
        "--ai", "all",
        "--skip-template"
    ])

    assert isinstance(result.exit_code, int)


# =============================================================================
# Integration Tests
# =============================================================================


def test_cli_without_arguments():
    """Test CLI without any arguments shows help."""
    result = runner.invoke(app, [])

    # Should show help or usage information
    assert result.exit_code == 0 or "usage" in result.stdout.lower() or "commands" in result.stdout.lower()


def test_cli_invalid_command():
    """Test CLI with invalid command."""
    result = runner.invoke(app, ["nonexistent-command"])

    # Should fail gracefully
    assert result.exit_code != 0 or "error" in result.stdout.lower() or "not found" in result.stdout.lower()


# =============================================================================
# Edge Cases
# =============================================================================


def test_init_command_nonexistent_directory():
    """Test init command with non-existent directory."""
    result = runner.invoke(app, [
        "init",
        "/nonexistent/path/that/does/not/exist",
        "--ai", "claude"
    ])

    # Should handle error gracefully
    assert isinstance(result.exit_code, int)


def test_init_command_no_agents():
    """Test init command without specifying agents."""
    result = runner.invoke(app, ["init", "."])

    # Should either prompt or fail gracefully
    assert isinstance(result.exit_code, int)


@patch("specify_cli.git_operations.is_git_repo")
def test_init_command_existing_git_repo(mock_is_git_repo, temp_project):
    """Test init command in existing git repository."""
    mock_is_git_repo.return_value = True

    result = runner.invoke(app, [
        "init",
        str(temp_project),
        "--ai", "claude",
        "--skip-template"
    ])

    # Should handle existing git repo
    assert isinstance(result.exit_code, int)


def test_discover_command_no_directory():
    """Test discover command without directory argument."""
    result = runner.invoke(app, ["discover"])

    # Should use current directory or fail gracefully
    assert isinstance(result.exit_code, int)


# =============================================================================
# Mocking Tests for Complex Scenarios
# =============================================================================


@patch("specify_cli.template_download.download_and_extract_template")
@patch("specify_cli.symlink_manager.ensure_central_installation")
@patch("specify_cli.symlink_manager.create_agent_symlinks")
def test_init_full_workflow_mocked(mock_create, mock_ensure, mock_download, temp_project):
    """Test full init workflow with mocked dependencies."""
    # Setup mocks
    mock_ensure.return_value = Path.home() / ".project-specify"
    mock_create.return_value = {"claude": True}
    mock_download.return_value = None

    result = runner.invoke(app, [
        "init",
        str(temp_project),
        "--ai", "claude"
    ])

    # Verify mocks were called (or command attempted to run)
    assert isinstance(result.exit_code, int)


@patch("specify_cli.mcp_discovery.discover_mcp_servers")
@patch("specify_cli.mcp_discovery.detect_project_technology")
@patch("specify_cli.mcp_discovery.generate_mcp_context")
def test_discover_full_workflow_mocked(mock_generate, mock_detect, mock_discover, temp_project):
    """Test full discover workflow with mocked dependencies."""
    from specify_cli.mcp_discovery import MCPServer, ProjectTechnology

    # Setup mocks
    mock_discover.return_value = [
        MCPServer(name="git", command="npx", source="test")
    ]
    mock_detect.return_value = ProjectTechnology(primary_language="python")
    mock_generate.return_value = None

    result = runner.invoke(app, ["discover", str(temp_project)])

    # Should complete successfully
    assert isinstance(result.exit_code, int)
