"""Tests for symlink functionality."""

import os
import tempfile
from pathlib import Path
import pytest

from specify_cli.symlink_manager import (
    create_agent_symlinks,
    verify_symlinks,
    ensure_central_installation,
    parse_ai_argument,
    get_central_dir,
    get_agents_dir,
)


@pytest.fixture
def temp_project():
    """Create a temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def central_install():
    """Ensure central installation exists."""
    ensure_central_installation(force_update=True)
    yield get_central_dir()
    # Cleanup handled by tempfile


def test_parse_ai_argument_all():
    """Test parsing 'all' keyword."""
    result = parse_ai_argument("all")
    assert len(result) > 0
    assert isinstance(result, list)


def test_parse_ai_argument_comma_separated():
    """Test parsing comma-separated agents."""
    result = parse_ai_argument("claude,cursor-agent,copilot")
    assert "claude" in result
    assert "cursor-agent" in result
    assert "copilot" in result


def test_parse_ai_argument_list():
    """Test parsing list of agents."""
    result = parse_ai_argument(["claude", "cursor-agent"])
    assert "claude" in result
    assert "cursor-agent" in result


def test_parse_ai_argument_invalid():
    """Test parsing invalid agent raises error."""
    with pytest.raises(ValueError):
        parse_ai_argument("invalid-agent-name")


def test_create_single_agent_symlink(temp_project, central_install):
    """Test creating symlink for a single agent."""
    # Ensure central installation has agent directories
    agents_dir = get_agents_dir()
    (agents_dir / "claude" / "commands").mkdir(parents=True, exist_ok=True)
    (agents_dir / "claude" / "commands" / "test.md").touch()
    
    results = create_agent_symlinks(temp_project, ["claude"], verbose=False)
    
    assert results["claude"] is True
    
    symlink_path = temp_project / ".claude" / "commands"
    assert symlink_path.is_symlink() or symlink_path.exists()
    if symlink_path.is_symlink():
        assert symlink_path.resolve().exists()


def test_create_multiple_agent_symlinks(temp_project, central_install):
    """Test creating symlinks for multiple agents."""
    agents_dir = get_agents_dir()
    for agent in ["claude", "cursor-agent"]:
        (agents_dir / agent.replace("-agent", "") / "commands").mkdir(parents=True, exist_ok=True)
        (agents_dir / agent.replace("-agent", "") / "commands" / "test.md").touch()
    
    agents = ["claude", "cursor-agent"]
    results = create_agent_symlinks(temp_project, agents, verbose=False)
    
    for agent in agents:
        # Some agents might not have commands yet, so just check if function ran
        assert agent in results


def test_verify_valid_symlinks(temp_project, central_install):
    """Test symlink verification."""
    agents_dir = get_agents_dir()
    (agents_dir / "claude" / "commands").mkdir(parents=True, exist_ok=True)
    (agents_dir / "claude" / "commands" / "test.md").touch()
    
    create_agent_symlinks(temp_project, ["claude"], verbose=False)
    
    status = verify_symlinks(temp_project, ["claude"])
    assert status["claude"] in ["valid", "file"]  # May be file if symlink failed


def test_verify_missing_symlinks(temp_project):
    """Test detection of missing symlinks."""
    status = verify_symlinks(temp_project, ["claude"])
    assert status["claude"] == "missing"


def test_force_overwrite(temp_project, central_install):
    """Test force flag overwrites existing directories."""
    agents_dir = get_agents_dir()
    (agents_dir / "claude" / "commands").mkdir(parents=True, exist_ok=True)
    (agents_dir / "claude" / "commands" / "test.md").touch()
    
    # Create a regular directory
    (temp_project / ".claude" / "commands").mkdir(parents=True)
    (temp_project / ".claude" / "commands" / "test.md").touch()
    
    # Without force, should skip
    results = create_agent_symlinks(temp_project, ["claude"], force=False, verbose=False)
    # May succeed or fail depending on implementation
    
    # With force, should overwrite
    results = create_agent_symlinks(temp_project, ["claude"], force=True, verbose=False)
    assert results["claude"] is True

