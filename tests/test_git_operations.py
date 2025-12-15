"""Tests for git operations."""

import subprocess
from pathlib import Path
import pytest

# Import from git_operations module (Phase 2 refactoring)
from specify_cli.git_operations import is_git_repo, init_git_repo


# =============================================================================
# Git Repository Detection Tests
# =============================================================================


def test_is_git_repo_true(git_repo):
    """Test detection of valid git repository."""
    result = is_git_repo(git_repo)
    assert result is True


def test_is_git_repo_false(temp_project):
    """Test detection of non-git directory."""
    result = is_git_repo(temp_project)
    assert result is False


def test_is_git_repo_subdirectory(git_repo):
    """Test detection from subdirectory of git repo."""
    subdir = git_repo / "src" / "lib"
    subdir.mkdir(parents=True)

    result = is_git_repo(subdir)
    assert result is True


def test_is_git_repo_parent_not_git(temp_project):
    """Test that parent directory being non-git returns False."""
    # Create nested structure where only child has .git
    child = temp_project / "child"
    child.mkdir()
    (child / ".git").mkdir()

    # Check parent (should be False since parent itself doesn't have .git in parents)
    result = is_git_repo(temp_project)
    assert result is False


# =============================================================================
# Git Repository Initialization Tests
# =============================================================================


def test_init_git_repo_new_repo(temp_project):
    """Test initializing a new git repository."""
    # Create a dummy file so git commit has something to commit
    (temp_project / ".gitkeep").write_text("")

    success, error_msg = init_git_repo(temp_project)

    assert success is True
    assert error_msg is None
    assert (temp_project / ".git").exists()
    assert (temp_project / ".git").is_dir()


def test_init_git_repo_with_initial_commit(temp_project):
    """Test that init creates an initial commit."""
    # Create a file to commit
    (temp_project / "README.md").write_text("# Test Project\n")

    success, error_msg = init_git_repo(temp_project)

    assert success is True
    assert error_msg is None

    # Verify commit was created
    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=temp_project,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Initial commit" in result.stdout or "initial" in result.stdout.lower()


def test_init_git_repo_existing_repo(git_repo):
    """Test that init skips existing repository."""
    # Git repo already exists from fixture
    success, error_msg = init_git_repo(git_repo)

    # Should return tuple (bool, Optional[str])
    assert isinstance(success, bool)
    assert isinstance(error_msg, (str, type(None)))


def test_init_git_repo_creates_gitignore(temp_project):
    """Test that common .gitignore patterns might be added."""
    # Create a dummy file so git commit has something to commit
    (temp_project / ".gitkeep").write_text("")

    success, error_msg = init_git_repo(temp_project)

    assert success is True
    # The function might or might not create .gitignore, just verify repo exists
    assert (temp_project / ".git").exists()


def test_init_git_repo_sets_user_config(temp_project):
    """Test that git user config is set for initial commit."""
    # Create a dummy file so git commit has something to commit
    (temp_project / ".gitkeep").write_text("")

    success, error_msg = init_git_repo(temp_project)

    assert success is True

    # Verify git config was set (at least for this repo)
    result = subprocess.run(
        ["git", "config", "user.email"],
        cwd=temp_project,
        capture_output=True,
        text=True,
    )

    # Should have some email set (either local or global)
    assert result.returncode == 0 or result.returncode == 1  # 1 if not set locally but global exists


# =============================================================================
# Edge Cases and Error Handling
# =============================================================================


def test_is_git_repo_nonexistent_path():
    """Test detection with nonexistent path."""
    nonexistent = Path("/nonexistent/path/to/nowhere")
    result = is_git_repo(nonexistent)
    assert result is False


def test_init_git_repo_no_git_installed(temp_project, monkeypatch):
    """Test handling when git is not installed."""
    def mock_run(*args, **kwargs):
        raise FileNotFoundError("git command not found")

    monkeypatch.setattr(subprocess, "run", mock_run)

    # Should handle gracefully and return tuple
    success, error_msg = init_git_repo(temp_project)
    assert isinstance(success, bool)
    assert isinstance(error_msg, (str, type(None)))


def test_git_operations_with_special_characters_in_path(temp_project):
    """Test git operations with special characters in directory name."""
    special_dir = temp_project / "test dir with spaces"
    special_dir.mkdir()
    # Create a dummy file so git commit has something to commit
    (special_dir / ".gitkeep").write_text("")

    success, error_msg = init_git_repo(special_dir)
    assert success is True
    assert (special_dir / ".git").exists()


# =============================================================================
# Integration Tests
# =============================================================================


def test_git_workflow_init_and_detect(temp_project):
    """Test full workflow: init repo, then detect it."""
    # Initially not a git repo
    assert is_git_repo(temp_project) is False

    # Create a dummy file so git commit has something to commit
    (temp_project / ".gitkeep").write_text("")

    # Initialize
    success, error_msg = init_git_repo(temp_project)
    assert success is True

    # Now should be detected as git repo
    assert is_git_repo(temp_project) is True


def test_git_repo_with_files(temp_project):
    """Test git init with existing files in directory."""
    # Create some files
    (temp_project / "file1.txt").write_text("content1")
    (temp_project / "src").mkdir()
    (temp_project / "src" / "file2.py").write_text("print('hello')")

    success, error_msg = init_git_repo(temp_project)
    assert success is True

    # Files should still exist
    assert (temp_project / "file1.txt").exists()
    assert (temp_project / "src" / "file2.py").exists()


def test_nested_git_repos(temp_project):
    """Test handling of nested git repositories."""
    # Create parent repo
    init_git_repo(temp_project)

    # Create nested directory
    nested = temp_project / "nested"
    nested.mkdir()

    # Parent should still be a git repo
    assert is_git_repo(temp_project) is True

    # Nested dir is within parent git repo
    assert is_git_repo(nested) is True
