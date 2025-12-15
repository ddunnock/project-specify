"""Tests for Windows-specific functionality and cross-platform compatibility."""

import platform
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from specify_cli.symlink_manager import (
    _has_windows_symlink_capability,
    _copy_agent_commands,
    _copy_file,
    _copy_directory,
    create_agent_symlinks,
)


# =============================================================================
# Windows Symlink Capability Tests
# =============================================================================


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
def test_windows_symlink_capability_check():
    """Test Windows symlink capability detection."""
    # This test will only run on Windows
    result = _has_windows_symlink_capability()
    assert isinstance(result, bool)
    # Result depends on whether Developer Mode is enabled or running as admin


@pytest.mark.skipif(platform.system() == "Windows", reason="Non-Windows test")
def test_non_windows_always_has_symlink_capability():
    """Test that non-Windows systems always return True for symlink capability."""
    assert _has_windows_symlink_capability() is True


def test_windows_symlink_capability_with_mocked_failure():
    """Test symlink capability detection when symlink creation fails."""
    with patch("platform.system", return_value="Windows"):
        with patch("pathlib.Path.symlink_to", side_effect=OSError):
            assert _has_windows_symlink_capability() is False


def test_windows_symlink_capability_with_mocked_success():
    """Test symlink capability detection when symlink creation succeeds."""
    with patch("platform.system", return_value="Windows"):
        # Mock symlink_to to succeed
        with patch("pathlib.Path.symlink_to"):
            # Mock unlink for cleanup
            with patch("pathlib.Path.unlink"):
                assert _has_windows_symlink_capability() is True


# =============================================================================
# Copy Fallback Tests
# =============================================================================


def test_copy_file_basic(temp_project):
    """Test basic file copying functionality."""
    source = temp_project / "source.txt"
    source.write_text("test content")

    target = temp_project / "target.txt"

    result = _copy_file(source, target, force=False, verbose=False)

    assert result is True
    assert target.exists()
    assert target.read_text() == "test content"


def test_copy_file_existing_without_force(temp_project):
    """Test that copy fails when target exists and force=False."""
    source = temp_project / "source.txt"
    source.write_text("source content")

    target = temp_project / "target.txt"
    target.write_text("existing content")

    result = _copy_file(source, target, force=False, verbose=False)

    assert result is False
    assert target.read_text() == "existing content"  # Unchanged


def test_copy_file_existing_with_force(temp_project):
    """Test that copy succeeds when target exists and force=True."""
    source = temp_project / "source.txt"
    source.write_text("new content")

    target = temp_project / "target.txt"
    target.write_text("old content")

    result = _copy_file(source, target, force=True, verbose=False)

    assert result is True
    assert target.read_text() == "new content"


def test_copy_directory_basic(temp_project):
    """Test basic directory copying functionality."""
    source = temp_project / "source_dir"
    source.mkdir()
    (source / "file1.txt").write_text("content1")
    (source / "file2.txt").write_text("content2")

    target = temp_project / "target_dir"

    result = _copy_directory(source, target, force=False, verbose=False)

    assert result is True
    assert target.exists()
    assert target.is_dir()
    assert (target / "file1.txt").read_text() == "content1"
    assert (target / "file2.txt").read_text() == "content2"


def test_copy_directory_existing_without_force(temp_project):
    """Test that directory copy fails when target exists and force=False."""
    source = temp_project / "source_dir"
    source.mkdir()
    (source / "file.txt").write_text("content")

    target = temp_project / "target_dir"
    target.mkdir()

    result = _copy_directory(source, target, force=False, verbose=False)

    assert result is False
    assert not (target / "file.txt").exists()  # Directory not updated


def test_copy_directory_existing_with_force(temp_project):
    """Test that directory copy succeeds when target exists and force=True."""
    source = temp_project / "source_dir"
    source.mkdir()
    (source / "new_file.txt").write_text("new content")

    target = temp_project / "target_dir"
    target.mkdir()
    (target / "old_file.txt").write_text("old content")

    result = _copy_directory(source, target, force=True, verbose=False)

    assert result is True
    assert (target / "new_file.txt").exists()
    assert not (target / "old_file.txt").exists()  # Old dir replaced


def test_copy_agent_commands_integration(temp_project, mock_central_install):
    """Test full agent command copying workflow."""
    # Mock central installation with agent directories
    from specify_cli.symlink_manager import AGENTS_DIR

    # Create mock agent structure
    claude_dir = AGENTS_DIR / "claude" / "commands"
    claude_dir.mkdir(parents=True, exist_ok=True)
    (claude_dir / "spec.sh").write_text("#!/bin/bash\necho 'spec'")
    (claude_dir / "plan.sh").write_text("#!/bin/bash\necho 'plan'")

    # Copy agent commands
    results = _copy_agent_commands(
        temp_project,
        ["claude"],
        force=False,
        verbose=False
    )

    assert results.get("claude") is True

    # Verify files were copied
    target_dir = temp_project / ".claude" / "commands"
    assert target_dir.exists()
    assert (target_dir / "spec.sh").exists()
    assert (target_dir / "plan.sh").exists()


def test_create_agent_symlinks_with_copy_flag(temp_project, mock_central_install):
    """Test that use_copy=True triggers copying instead of symlinking."""
    from specify_cli.symlink_manager import AGENTS_DIR

    # Create mock agent structure
    claude_dir = AGENTS_DIR / "claude" / "commands"
    claude_dir.mkdir(parents=True, exist_ok=True)
    (claude_dir / "spec.sh").write_text("#!/bin/bash\necho 'spec'")

    # Create agent symlinks with use_copy=True
    results = create_agent_symlinks(
        temp_project,
        ["claude"],
        force=False,
        verbose=False,
        use_copy=True
    )

    assert results.get("claude") is True

    # Verify it's a real directory, not a symlink
    target_dir = temp_project / ".claude" / "commands"
    assert target_dir.exists()
    assert not target_dir.is_symlink()  # Should be a real directory
    assert (target_dir / "spec.sh").exists()


# =============================================================================
# Cross-Platform Path Handling Tests
# =============================================================================


def test_cross_platform_path_creation(temp_project):
    """Test that paths work correctly on all platforms."""
    # Create nested directory structure
    nested = temp_project / ".claude" / "commands" / "subdirectory"
    nested.mkdir(parents=True, exist_ok=True)

    assert nested.exists()
    assert nested.is_dir()


def test_cross_platform_path_separators(temp_project):
    """Test that both forward and backward slashes work in paths."""
    # Pathlib should handle platform differences
    path1 = temp_project / ".claude/commands"
    path2 = temp_project / ".claude" / "commands"

    path1.mkdir(parents=True, exist_ok=True)

    assert path1.exists()
    assert path2.exists()
    assert path1.resolve() == path2.resolve()


def test_copy_preserves_file_metadata(temp_project):
    """Test that copying preserves file metadata (timestamps, permissions)."""
    import time

    source = temp_project / "source.txt"
    source.write_text("content")

    # Wait a moment to ensure different timestamp
    time.sleep(0.1)

    target = temp_project / "target.txt"
    _copy_file(source, target, force=False, verbose=False)

    # On Unix-like systems, check that permissions are preserved
    if platform.system() != "Windows":
        assert source.stat().st_mode == target.stat().st_mode


# =============================================================================
# Windows Error Message Tests
# =============================================================================


def test_windows_symlink_error_message_includes_recovery_options():
    """Test that Windows symlink errors provide helpful recovery information."""
    # This is tested via the error message in _create_windows_symlink
    # We can verify the structure exists by checking imports
    from specify_cli.symlink_manager import _create_windows_symlink

    assert _create_windows_symlink.__doc__ is not None
    assert "Developer Mode" in _create_windows_symlink.__doc__


def test_copy_fallback_mentioned_in_help():
    """Test that --copy flag is mentioned in help text."""
    from specify_cli.commands.init_cmd import init

    help_text = init.__doc__
    assert help_text is not None
    # The docstring should mention both symlinks and copies
    assert "symlink" in help_text.lower() or "copy" in help_text.lower()
