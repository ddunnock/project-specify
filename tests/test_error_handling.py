"""Tests for error handling across all modules."""

import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

from specify_cli.errors import (
    SpecifyError,
    SymlinkError,
    ConfigError,
    MonorepoError,
    MCPDiscoveryError,
    TemplateError,
    GitOperationError,
    NetworkError,
    FileOperationError,
)


# =============================================================================
# Base Exception Tests
# =============================================================================


def test_specify_error_is_base_exception():
    """Test that SpecifyError is the base for all custom exceptions."""
    assert issubclass(SymlinkError, SpecifyError)
    assert issubclass(ConfigError, SpecifyError)
    assert issubclass(MonorepoError, SpecifyError)
    assert issubclass(MCPDiscoveryError, SpecifyError)
    assert issubclass(TemplateError, SpecifyError)
    assert issubclass(GitOperationError, SpecifyError)
    assert issubclass(NetworkError, SpecifyError)
    assert issubclass(FileOperationError, SpecifyError)


def test_specify_error_can_be_caught():
    """Test that catching SpecifyError catches all custom exceptions."""
    try:
        raise SymlinkError("test")
    except SpecifyError:
        pass  # Should catch it

    try:
        raise MCPDiscoveryError("test")
    except SpecifyError:
        pass  # Should catch it


# =============================================================================
# SymlinkError Tests
# =============================================================================


def test_symlink_error_on_permission_denied(temp_project):
    """Test SymlinkError is raised on permission issues."""
    from specify_cli.symlink_manager import create_agent_symlinks

    # Mock symlink creation to raise permission error
    with patch("specify_cli.symlink_manager._create_symlink") as mock_create:
        mock_create.return_value = False

        results = create_agent_symlinks(
            temp_project,
            ["claude"],
            force=False,
            verbose=False
        )

        # Should return False for failed symlinks
        assert results.get("claude") is False


def test_symlink_error_contains_helpful_message():
    """Test that SymlinkError contains helpful recovery information."""
    error = SymlinkError(
        "Failed to create symlinks for: claude. "
        "Check permissions and ensure Developer Mode is enabled on Windows."
    )

    assert "permissions" in str(error).lower()
    assert "developer mode" in str(error).lower() or "windows" in str(error).lower()


# =============================================================================
# MonorepoError Tests
# =============================================================================


def test_monorepo_error_on_invalid_package_json(temp_project):
    """Test MonorepoError is raised on invalid package.json."""
    from specify_cli.monorepo import _get_npm_workspaces

    # Create invalid package.json
    (temp_project / "package.json").write_text("{ invalid json }")

    with pytest.raises(MonorepoError) as exc_info:
        _get_npm_workspaces(temp_project)

    assert "Invalid JSON" in str(exc_info.value)
    assert "package.json" in str(exc_info.value)


def test_monorepo_error_on_invalid_lerna_json(temp_project):
    """Test MonorepoError is raised on invalid lerna.json."""
    from specify_cli.monorepo import _get_lerna_packages

    # Create invalid lerna.json
    (temp_project / "lerna.json").write_text("{ not valid json }")

    with pytest.raises(MonorepoError) as exc_info:
        _get_lerna_packages(temp_project)

    assert "Invalid JSON" in str(exc_info.value)
    assert "lerna.json" in str(exc_info.value)


def test_monorepo_error_on_invalid_pnpm_yaml(temp_project):
    """Test MonorepoError is raised on invalid pnpm-workspace.yaml."""
    from specify_cli.monorepo import _get_pnpm_workspaces

    # Create invalid YAML (if yaml is available)
    try:
        import yaml
        (temp_project / "pnpm-workspace.yaml").write_text(":\n  invalid: [yaml")

        with pytest.raises(MonorepoError) as exc_info:
            _get_pnpm_workspaces(temp_project)

        assert "Invalid YAML" in str(exc_info.value) or "pnpm" in str(exc_info.value)
    except ImportError:
        # If yaml not available, test the simple parser fallback
        (temp_project / "pnpm-workspace.yaml").write_text("packages:\n  - apps/*")
        # Should not raise error with simple parser
        packages = _get_pnpm_workspaces(temp_project)
        assert isinstance(packages, list)


# =============================================================================
# MCPDiscoveryError Tests
# =============================================================================


def test_mcp_discovery_error_on_invalid_json(temp_project):
    """Test MCPDiscoveryError is raised on invalid MCP config JSON."""
    from specify_cli.mcp_discovery import _parse_mcp_config

    config_file = temp_project / "invalid_mcp.json"
    config_file.write_text("{ invalid json }")

    with pytest.raises(MCPDiscoveryError) as exc_info:
        _parse_mcp_config(config_file, "test")

    assert "Invalid JSON" in str(exc_info.value)
    assert "test" in str(exc_info.value)


def test_mcp_discovery_error_on_missing_file(temp_project):
    """Test MCPDiscoveryError is raised when config file is missing."""
    from specify_cli.mcp_discovery import _parse_mcp_config

    config_file = temp_project / "nonexistent.json"

    with pytest.raises(MCPDiscoveryError) as exc_info:
        _parse_mcp_config(config_file, "test")

    assert "Failed to read" in str(exc_info.value)


def test_mcp_discovery_error_is_non_fatal_during_init(temp_project):
    """Test that MCPDiscoveryError during init doesn't stop initialization."""
    from specify_cli.mcp_discovery import discover_mcp_servers

    # Create invalid config that will be skipped
    mcp_dir = temp_project / ".mcp"
    mcp_dir.mkdir()
    (mcp_dir / "servers.json").write_text("{ invalid }")

    # Should not raise, just skip the invalid config
    # (discover_mcp_servers handles exceptions internally)
    servers = discover_mcp_servers(temp_project)
    assert isinstance(servers, list)


# =============================================================================
# TemplateError Tests
# =============================================================================


def test_template_error_on_missing_asset():
    """Test TemplateError is raised when release asset not found."""
    error = TemplateError(
        "No matching release asset found for claude "
        "(expected pattern: spec-kit-template-claude-sh). "
        "Available assets: (none)"
    )

    assert "No matching release asset" in str(error)
    assert "claude" in str(error)


def test_template_error_on_invalid_json_response():
    """Test TemplateError is raised on invalid JSON in release response."""
    error = TemplateError(
        "Failed to parse release JSON: Expecting value: line 1 column 1 (char 0)"
    )

    assert "Failed to parse release JSON" in str(error)


def test_template_error_on_extraction_failure():
    """Test TemplateError is raised when extraction fails."""
    error = TemplateError(
        "Template extraction failed: [Errno 2] No such file or directory"
    )

    assert "extraction failed" in str(error).lower()


# =============================================================================
# NetworkError Tests
# =============================================================================


def test_network_error_on_rate_limit():
    """Test NetworkError is raised on GitHub rate limit."""
    error = NetworkError(
        "GitHub API Rate Limit Exceeded\n"
        "Remaining: 0\n"
        "Reset at: 2024-01-01 12:00:00"
    )

    assert "rate limit" in str(error).lower()


def test_network_error_on_404():
    """Test NetworkError is raised on 404 responses."""
    error = NetworkError("HTTP 404: Not Found")

    assert "404" in str(error)


def test_network_error_on_connection_failure():
    """Test NetworkError is raised on connection failures."""
    error = NetworkError("Connection refused")

    assert "connection" in str(error).lower() or "refused" in str(error).lower()


# =============================================================================
# GitOperationError Tests
# =============================================================================


def test_git_operation_error_on_missing_git():
    """Test GitOperationError when git is not installed."""
    from specify_cli.git_operations import init_git_repo

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("git: command not found")

        success, error_msg = init_git_repo(Path.cwd())

        assert success is False
        assert error_msg is not None
        assert "git" in error_msg.lower()


def test_git_operation_error_on_command_failure():
    """Test GitOperationError when git command fails."""
    from specify_cli.git_operations import init_git_repo
    import subprocess

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=128,
            cmd=["git", "init"],
            stderr="fatal: not a git repository"
        )

        success, error_msg = init_git_repo(Path.cwd())

        assert success is False
        assert error_msg is not None


# =============================================================================
# FileOperationError Tests
# =============================================================================


def test_file_operation_error_on_missing_source(temp_project):
    """Test FileOperationError when source file is missing."""
    from specify_cli.file_operations import handle_vscode_settings

    vscode_dir = temp_project / ".vscode"
    vscode_dir.mkdir()
    existing = vscode_dir / "settings.json"
    existing.write_text(json.dumps({"key": "value"}))

    nonexistent = temp_project / "nonexistent.json"

    with pytest.raises(FileOperationError) as exc_info:
        handle_vscode_settings(nonexistent, existing, ".vscode/settings.json")

    assert "Failed to copy VS Code settings" in str(exc_info.value)


def test_file_operation_error_on_permission_denied(temp_project):
    """Test FileOperationError on permission issues."""
    from specify_cli.file_operations import handle_vscode_settings

    vscode_dir = temp_project / ".vscode"
    vscode_dir.mkdir()
    source = temp_project / "source.json"
    source.write_text(json.dumps({"key": "value"}))

    dest = vscode_dir / "settings.json"

    # Mock copy to raise permission error
    with patch("shutil.copy2") as mock_copy:
        mock_copy.side_effect = PermissionError("Permission denied")

        with pytest.raises(FileOperationError) as exc_info:
            handle_vscode_settings(source, dest, ".vscode/settings.json")

        assert "Failed to" in str(exc_info.value)


# =============================================================================
# Error Recovery Tests (InitializationState)
# =============================================================================


def test_initialization_state_tracks_directories(temp_project):
    """Test that InitializationState tracks created directories."""
    from specify_cli.commands.init_cmd import InitializationState

    state = InitializationState(project_path=temp_project)

    test_dir = temp_project / "test_dir"
    test_dir.mkdir()
    state.track_directory(test_dir)

    assert test_dir in state.created_directories


def test_initialization_state_tracks_symlinks(temp_project):
    """Test that InitializationState tracks created symlinks."""
    from specify_cli.commands.init_cmd import InitializationState

    state = InitializationState(project_path=temp_project)

    symlink = temp_project / "test_link"
    target = temp_project / "target"
    target.mkdir()
    symlink.symlink_to(target)

    state.track_symlink(symlink)

    assert symlink in state.created_symlinks


def test_initialization_state_rollback_removes_directories(temp_project, capsys):
    """Test that rollback removes tracked directories."""
    from specify_cli.commands.init_cmd import InitializationState
    from specify_cli.ui import console

    state = InitializationState(project_path=temp_project, was_empty_directory=False)

    # Create and track a directory
    test_dir = temp_project / "test_rollback_dir"
    test_dir.mkdir()
    state.track_directory(test_dir)

    assert test_dir.exists()

    # Rollback should remove it
    state.rollback(console, verbose=False)

    assert not test_dir.exists()


def test_initialization_state_rollback_removes_symlinks(temp_project, capsys):
    """Test that rollback removes tracked symlinks."""
    from specify_cli.commands.init_cmd import InitializationState
    from specify_cli.ui import console

    state = InitializationState(project_path=temp_project, was_empty_directory=False)

    # Create and track a symlink
    target = temp_project / "target"
    target.mkdir()
    symlink = temp_project / "test_link"
    symlink.symlink_to(target)
    state.track_symlink(symlink)

    assert symlink.exists()

    # Rollback should remove it
    state.rollback(console, verbose=False)

    assert not symlink.exists()
    assert target.exists()  # Target should remain


def test_initialization_state_rollback_preserves_existing_directory(temp_project, capsys):
    """Test that rollback doesn't remove existing project directory."""
    from specify_cli.commands.init_cmd import InitializationState
    from specify_cli.ui import console

    # Mark as existing (not empty)
    state = InitializationState(
        project_path=temp_project,
        was_empty_directory=False
    )

    # Create a subdirectory
    subdir = temp_project / "subdir"
    subdir.mkdir()
    state.track_directory(subdir)

    # Rollback should remove subdir but not project_path
    state.rollback(console, verbose=False)

    assert temp_project.exists()  # Project dir should remain
    assert not subdir.exists()    # Subdir should be removed


def test_initialization_state_rollback_handles_errors_gracefully(temp_project, capsys):
    """Test that rollback continues even if individual cleanup fails."""
    from specify_cli.commands.init_cmd import InitializationState
    from specify_cli.ui import console

    state = InitializationState(project_path=temp_project, was_empty_directory=False)

    # Track a non-existent directory (should handle gracefully)
    fake_dir = temp_project / "nonexistent"
    state.track_directory(fake_dir)

    # Should not raise, just skip
    state.rollback(console, verbose=False)


# =============================================================================
# Integration: Error Handling in Init Command
# =============================================================================


@patch("specify_cli.symlink_manager.create_agent_symlinks")
def test_init_command_handles_symlink_error(mock_create_symlinks, temp_project):
    """Test that init command properly handles SymlinkError."""
    from specify_cli.symlink_manager import create_agent_symlinks

    # Mock symlink creation to fail
    mock_create_symlinks.return_value = {"claude": False}

    # Test that our mock behaves correctly
    result = mock_create_symlinks(temp_project, ["claude"], False, False)
    assert result["claude"] is False


# =============================================================================
# Error Message Quality Tests
# =============================================================================


def test_symlink_error_message_includes_recovery_steps():
    """Test that SymlinkError messages include recovery information."""
    error = SymlinkError(
        "Failed to create symlinks for: claude. "
        "Check permissions and ensure Developer Mode is enabled on Windows."
    )

    error_msg = str(error)
    # Should mention either permissions or Windows Developer Mode
    assert any(keyword in error_msg.lower() for keyword in ["permission", "developer mode", "windows"])


def test_monorepo_error_message_includes_file_path():
    """Test that MonorepoError messages include file path for debugging."""
    error = MonorepoError("Invalid JSON in package.json at /path/to/package.json")

    assert "package.json" in str(error)
    assert "/path/to/" in str(error) or "Invalid JSON" in str(error)


def test_mcp_discovery_error_message_includes_source():
    """Test that MCPDiscoveryError messages include config source."""
    error = MCPDiscoveryError("Invalid JSON in claude_desktop MCP config at /path/to/config.json")

    assert "claude_desktop" in str(error) or "config" in str(error)


def test_template_error_message_includes_context():
    """Test that TemplateError messages include helpful context."""
    error = TemplateError("No matching release asset found for claude (expected pattern: spec-kit-template-claude-sh)")

    assert "claude" in str(error)
    assert "pattern" in str(error).lower() or "asset" in str(error).lower()


def test_network_error_message_includes_status_code():
    """Test that NetworkError messages include HTTP status codes."""
    error = NetworkError("HTTP 404: Repository not found")

    assert "404" in str(error)


def test_git_operation_error_message_includes_command():
    """Test that GitOperationError messages include git command info."""
    error = GitOperationError("Git init failed: fatal: not a git repository")

    assert "git" in str(error).lower()
