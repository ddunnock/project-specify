"""Shared pytest fixtures for project-specify tests."""

import json
import tempfile
from pathlib import Path
from typing import Generator
import pytest
import responses as responses_lib

from specify_cli.symlink_manager import ensure_central_installation, get_central_dir


# =============================================================================
# Project & Directory Fixtures
# =============================================================================


@pytest.fixture
def temp_project() -> Generator[Path, None, None]:
    """Create a temporary project directory.

    Yields:
        Path: Temporary project directory that will be cleaned up after test.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def central_install() -> Generator[Path, None, None]:
    """Ensure central installation exists and return the central directory.

    Yields:
        Path: The central installation directory (~/.project-specify).
    """
    ensure_central_installation(force_update=True)
    yield get_central_dir()
    # Cleanup handled by tempfile or user's home directory


# =============================================================================
# Monorepo Fixtures
# =============================================================================


@pytest.fixture
def mock_monorepo_pnpm(temp_project: Path) -> Path:
    """Create a mock pnpm workspace monorepo structure.

    Args:
        temp_project: Temporary project directory.

    Returns:
        Path: Project root with pnpm-workspace.yaml.
    """
    workspace_file = temp_project / "pnpm-workspace.yaml"
    workspace_file.write_text("""packages:
  - 'packages/*'
  - 'apps/*'
""")

    # Create package directories
    (temp_project / "packages" / "core").mkdir(parents=True)
    (temp_project / "packages" / "core" / "package.json").write_text(json.dumps({
        "name": "@test/core",
        "version": "1.0.0"
    }))

    (temp_project / "apps" / "web").mkdir(parents=True)
    (temp_project / "apps" / "web" / "package.json").write_text(json.dumps({
        "name": "@test/web",
        "version": "1.0.0"
    }))

    return temp_project


@pytest.fixture
def mock_monorepo_npm(temp_project: Path) -> Path:
    """Create a mock npm workspaces monorepo structure.

    Args:
        temp_project: Temporary project directory.

    Returns:
        Path: Project root with package.json workspaces.
    """
    package_json = temp_project / "package.json"
    package_json.write_text(json.dumps({
        "name": "test-monorepo",
        "version": "1.0.0",
        "workspaces": [
            "packages/*",
            "apps/*"
        ]
    }, indent=2))

    # Create package directories
    (temp_project / "packages" / "utils").mkdir(parents=True)
    (temp_project / "packages" / "utils" / "package.json").write_text(json.dumps({
        "name": "@test/utils",
        "version": "1.0.0"
    }))

    return temp_project


@pytest.fixture
def mock_monorepo_cargo(temp_project: Path) -> Path:
    """Create a mock Cargo workspace monorepo structure.

    Args:
        temp_project: Temporary project directory.

    Returns:
        Path: Project root with Cargo.toml workspace.
    """
    cargo_toml = temp_project / "Cargo.toml"
    cargo_toml.write_text("""[workspace]
members = [
    "crates/*",
]

[workspace.package]
version = "0.1.0"
edition = "2021"
""")

    # Create crate directories
    (temp_project / "crates" / "core").mkdir(parents=True)
    (temp_project / "crates" / "core" / "Cargo.toml").write_text("""[package]
name = "core"
version = "0.1.0"
edition = "2021"
""")

    return temp_project


@pytest.fixture
def mock_monorepo_lerna(temp_project: Path) -> Path:
    """Create a mock Lerna monorepo structure.

    Args:
        temp_project: Temporary project directory.

    Returns:
        Path: Project root with lerna.json.
    """
    lerna_json = temp_project / "lerna.json"
    lerna_json.write_text(json.dumps({
        "version": "1.0.0",
        "packages": [
            "packages/*"
        ]
    }, indent=2))

    # Create package directories
    (temp_project / "packages" / "lib").mkdir(parents=True)
    (temp_project / "packages" / "lib" / "package.json").write_text(json.dumps({
        "name": "@test/lib",
        "version": "1.0.0"
    }))

    return temp_project


@pytest.fixture
def mock_monorepo_nx(temp_project: Path) -> Path:
    """Create a mock Nx monorepo structure.

    Args:
        temp_project: Temporary project directory.

    Returns:
        Path: Project root with nx.json.
    """
    nx_json = temp_project / "nx.json"
    nx_json.write_text(json.dumps({
        "npmScope": "test",
        "affected": {
            "defaultBase": "main"
        },
        "workspaceLayout": {
            "appsDir": "apps",
            "libsDir": "libs"
        }
    }, indent=2))

    return temp_project


# =============================================================================
# MCP Configuration Fixtures
# =============================================================================


@pytest.fixture
def mock_mcp_config(temp_project: Path) -> Path:
    """Create a mock MCP configuration file.

    Args:
        temp_project: Temporary project directory.

    Returns:
        Path: Path to the MCP config file.
    """
    mcp_dir = temp_project / ".mcp"
    mcp_dir.mkdir()

    config_file = mcp_dir / "servers.json"
    config_file.write_text(json.dumps({
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
            },
            "git": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-git"]
            },
            "postgres": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres"],
                "env": {
                    "POSTGRES_CONNECTION_STRING": "postgresql://localhost/testdb"
                }
            }
        }
    }, indent=2))

    return config_file


@pytest.fixture
def mock_claude_desktop_config(tmp_path: Path) -> Path:
    """Create a mock Claude Desktop configuration.

    Args:
        tmp_path: pytest's built-in temporary directory fixture.

    Returns:
        Path: Path to the mock Claude Desktop config file.
    """
    config_dir = tmp_path / ".config" / "claude"
    config_dir.mkdir(parents=True)

    config_file = config_dir / "claude_desktop_config.json"
    config_file.write_text(json.dumps({
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
                }
            },
            "sqlite": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/db.sqlite"]
            }
        }
    }, indent=2))

    return config_file


# =============================================================================
# Project File Fixtures
# =============================================================================


@pytest.fixture
def sample_project_files(temp_project: Path) -> dict[str, Path]:
    """Create sample project files for testing.

    Args:
        temp_project: Temporary project directory.

    Returns:
        dict: Mapping of file types to their paths.
    """
    files = {}

    # Python project files
    (temp_project / "requirements.txt").write_text("requests>=2.28.0\npytest>=7.0.0\n")
    files["requirements"] = temp_project / "requirements.txt"

    (temp_project / "pyproject.toml").write_text("""[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests"]
""")
    files["pyproject"] = temp_project / "pyproject.toml"

    # Node.js project files
    (temp_project / "package.json").write_text(json.dumps({
        "name": "test-project",
        "version": "1.0.0",
        "dependencies": {
            "express": "^4.18.0"
        }
    }))
    files["package_json"] = temp_project / "package.json"

    # Git files
    (temp_project / ".git").mkdir()
    (temp_project / ".gitignore").write_text("node_modules/\n__pycache__/\n")
    files["gitignore"] = temp_project / ".gitignore"

    # README
    (temp_project / "README.md").write_text("# Test Project\n\nA test project.")
    files["readme"] = temp_project / "README.md"

    return files


# =============================================================================
# HTTP Mocking Fixtures
# =============================================================================


@pytest.fixture
def mock_github_api():
    """Mock GitHub API responses using responses library.

    Yields:
        responses.RequestsMock: Configured responses mock for GitHub API.
    """
    with responses_lib.RequestsMock() as rsps:
        # Mock rate limit endpoint
        rsps.add(
            responses_lib.GET,
            "https://api.github.com/rate_limit",
            json={
                "resources": {
                    "core": {
                        "limit": 5000,
                        "remaining": 4999,
                        "reset": 1234567890
                    }
                }
            },
            status=200
        )

        # Mock latest release endpoint
        rsps.add(
            responses_lib.GET,
            "https://api.github.com/repos/test/repo/releases/latest",
            json={
                "tag_name": "v1.0.0",
                "name": "Release 1.0.0",
                "zipball_url": "https://api.github.com/repos/test/repo/zipball/v1.0.0"
            },
            status=200
        )

        yield rsps


# =============================================================================
# Git Fixtures
# =============================================================================


@pytest.fixture
def git_repo(temp_project: Path) -> Path:
    """Initialize a git repository in the temp project.

    Args:
        temp_project: Temporary project directory.

    Returns:
        Path: Project root with initialized git repository.
    """
    import subprocess

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=temp_project,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=temp_project,
        check=True,
        capture_output=True
    )

    return temp_project


# =============================================================================
# Template Fixtures
# =============================================================================


@pytest.fixture
def mock_template_zip(tmp_path: Path) -> Path:
    """Create a mock template zip file for testing template extraction.

    Args:
        tmp_path: pytest's built-in temporary directory fixture.

    Returns:
        Path: Path to the mock zip file.
    """
    import zipfile

    # Create template directory structure
    template_dir = tmp_path / "template"
    template_dir.mkdir()

    (template_dir / ".specify").mkdir()
    (template_dir / ".specify" / "templates").mkdir()
    (template_dir / ".specify" / "templates" / "spec-template.md").write_text(
        "# Specification Template\n\nFeature: {{feature_name}}\n"
    )

    # Create zip file
    zip_path = tmp_path / "template.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in template_dir.rglob('*'):
            if file.is_file():
                zipf.write(file, file.relative_to(template_dir))

    return zip_path
