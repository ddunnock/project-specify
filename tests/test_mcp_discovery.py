"""Tests for MCP (Model Context Protocol) server discovery."""

import json
import os
import platform
from pathlib import Path
from unittest.mock import patch
import pytest

from specify_cli.mcp_discovery import (
    MCPServer,
    ProjectTechnology,
    get_mcp_config_paths,
    discover_mcp_servers,
    _parse_mcp_config,
    _deduplicate_servers,
    detect_project_technology,
    generate_mcp_context,
    KNOWN_MCP_SERVERS,
)


# =============================================================================#
# MCPServer Dataclass Tests
# =============================================================================


def test_mcp_server_creation():
    """Test MCPServer dataclass creation."""
    server = MCPServer(
        name="test-server",
        command="npx",
        args=["-y", "@test/server"],
        env={"API_KEY": "test"},
        source="test",
        description="A test server",
        capabilities=["test_op"],
    )

    assert server.name == "test-server"
    assert server.command == "npx"
    assert len(server.args) == 2
    assert server.env["API_KEY"] == "test"


def test_mcp_server_defaults():
    """Test MCPServer default values."""
    server = MCPServer(name="minimal", command="test")

    assert server.args == []
    assert server.env == {}
    assert server.source == ""
    assert server.description == ""
    assert server.capabilities == []


# =============================================================================
# Config Path Detection Tests
# =============================================================================


@patch("platform.system")
def test_get_mcp_config_paths_macos(mock_system):
    """Test MCP config path detection on macOS."""
    mock_system.return_value = "Darwin"
    paths = get_mcp_config_paths()

    assert "claude_desktop" in paths
    assert "claude_code" in paths
    assert "cursor" in paths

    # Check macOS-specific paths
    assert "Library/Application Support/Claude" in str(paths["claude_desktop"])
    assert ".claude/mcp_servers.json" in str(paths["claude_code"])
    assert ".cursor/mcp.json" in str(paths["cursor"])


@patch("platform.system")
@patch.dict(os.environ, {"APPDATA": "/Users/test/AppData/Roaming"})
def test_get_mcp_config_paths_windows(mock_system):
    """Test MCP config path detection on Windows."""
    mock_system.return_value = "Windows"
    paths = get_mcp_config_paths()

    assert "claude_desktop" in paths
    assert "claude_code" in paths
    assert "cursor" in paths


@patch("platform.system")
@patch.dict(os.environ, {"XDG_CONFIG_HOME": "/home/user/.config"})
def test_get_mcp_config_paths_linux(mock_system):
    """Test MCP config path detection on Linux."""
    mock_system.return_value = "Linux"
    paths = get_mcp_config_paths()

    assert "claude_desktop" in paths
    assert ".config/Claude" in str(paths["claude_desktop"])


# =============================================================================
# MCP Config Parsing Tests
# =============================================================================


def test_parse_mcp_config_claude_desktop(temp_project):
    """Test parsing Claude Desktop MCP config."""
    config_file = temp_project / "claude_desktop_config.json"
    config_file.write_text(json.dumps({
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
            },
            "git": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-git"],
            }
        }
    }))

    servers = _parse_mcp_config(config_file, "claude_desktop")

    assert len(servers) == 2
    assert any(s.name == "filesystem" for s in servers)
    assert any(s.name == "git" for s in servers)

    fs_server = next(s for s in servers if s.name == "filesystem")
    assert fs_server.command == "npx"
    assert len(fs_server.args) == 3
    assert fs_server.source == "claude_desktop"


def test_parse_mcp_config_with_env_vars(temp_project):
    """Test parsing MCP config with environment variables."""
    config_file = temp_project / "mcp_config.json"
    config_file.write_text(json.dumps({
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_TOKEN": "${GITHUB_TOKEN}",
                    "GITHUB_API_URL": "https://api.github.com"
                }
            }
        }
    }))

    servers = _parse_mcp_config(config_file, "test")

    assert len(servers) == 1
    assert servers[0].name == "github"
    assert servers[0].env["GITHUB_TOKEN"] == "${GITHUB_TOKEN}"
    assert servers[0].env["GITHUB_API_URL"] == "https://api.github.com"


def test_parse_mcp_config_known_server_info(temp_project):
    """Test that known server info is populated."""
    config_file = temp_project / "config.json"
    config_file.write_text(json.dumps({
        "mcpServers": {
            "postgres": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres"]
            }
        }
    }))

    servers = _parse_mcp_config(config_file, "test")

    assert len(servers) == 1
    assert servers[0].name == "postgres"
    assert servers[0].description == KNOWN_MCP_SERVERS["postgres"]["description"]
    assert servers[0].capabilities == KNOWN_MCP_SERVERS["postgres"]["capabilities"]


def test_parse_mcp_config_invalid_json(temp_project):
    """Test parsing invalid JSON raises MCPDiscoveryError."""
    from specify_cli.errors import MCPDiscoveryError

    config_file = temp_project / "invalid.json"
    config_file.write_text("{ invalid json }")

    with pytest.raises(MCPDiscoveryError) as exc_info:
        _parse_mcp_config(config_file, "test")

    assert "Invalid JSON" in str(exc_info.value)


def test_parse_mcp_config_missing_file(temp_project):
    """Test parsing missing file raises MCPDiscoveryError."""
    from specify_cli.errors import MCPDiscoveryError

    config_file = temp_project / "nonexistent.json"

    with pytest.raises(MCPDiscoveryError) as exc_info:
        _parse_mcp_config(config_file, "test")

    assert "Failed to read" in str(exc_info.value)


def test_parse_mcp_config_servers_field(temp_project):
    """Test parsing config with 'servers' field instead of 'mcpServers'."""
    config_file = temp_project / "config.json"
    config_file.write_text(json.dumps({
        "servers": {
            "custom": {
                "command": "node",
                "args": ["./server.js"]
            }
        }
    }))

    servers = _parse_mcp_config(config_file, "test")

    assert len(servers) == 1
    assert servers[0].name == "custom"


# =============================================================================
# Server Deduplication Tests
# =============================================================================


def test_deduplicate_servers_by_priority():
    """Test server deduplication prioritizes project > claude_code > claude_desktop."""
    servers = [
        MCPServer(name="git", command="cmd1", source="claude_desktop"),
        MCPServer(name="git", command="cmd2", source="project"),
        MCPServer(name="git", command="cmd3", source="claude_code"),
    ]

    result = _deduplicate_servers(servers)

    assert len(result) == 1
    assert result[0].command == "cmd2"  # project has highest priority
    assert result[0].source == "project"


def test_deduplicate_servers_different_names():
    """Test deduplication keeps servers with different names."""
    servers = [
        MCPServer(name="git", command="cmd1", source="claude_desktop"),
        MCPServer(name="github", command="cmd2", source="claude_desktop"),
        MCPServer(name="postgres", command="cmd3", source="project"),
    ]

    result = _deduplicate_servers(servers)

    assert len(result) == 3


def test_deduplicate_servers_unknown_source():
    """Test deduplication with unknown source has lowest priority."""
    servers = [
        MCPServer(name="custom", command="cmd1", source="unknown"),
        MCPServer(name="custom", command="cmd2", source="project"),
    ]

    result = _deduplicate_servers(servers)

    assert len(result) == 1
    assert result[0].source == "project"


# =============================================================================
# MCP Server Discovery Tests
# =============================================================================


def test_discover_mcp_servers_project_local(mock_mcp_config):
    """Test discovering project-local MCP servers."""
    project_dir = mock_mcp_config.parent.parent
    servers = discover_mcp_servers(project_dir)

    # Should find servers from the mock config
    assert len(servers) >= 1
    assert any(s.source == "project" for s in servers)


def test_discover_mcp_servers_multiple_sources(temp_project):
    """Test discovering servers from multiple sources."""
    # Create project-local config
    mcp_dir = temp_project / ".mcp"
    mcp_dir.mkdir()
    (mcp_dir / "servers.json").write_text(json.dumps({
        "mcpServers": {
            "project-server": {
                "command": "node",
                "args": ["./server.js"]
            }
        }
    }))

    # Create alternative config location
    (temp_project / "mcp.json").write_text(json.dumps({
        "mcpServers": {
            "alt-server": {
                "command": "node",
                "args": ["./alt.js"]
            }
        }
    }))

    servers = discover_mcp_servers(temp_project)

    # Should find at least the project-server (alt-server might be deduplicated)
    assert len(servers) >= 1
    server_names = [s.name for s in servers]
    assert "project-server" in server_names or "alt-server" in server_names


def test_discover_mcp_servers_no_config(temp_project):
    """Test discovering servers when no config exists."""
    servers = discover_mcp_servers(temp_project)

    # Should return empty list (or only system-wide configs if they exist)
    assert isinstance(servers, list)


# =============================================================================
# Technology Detection Tests
# =============================================================================


def test_detect_technology_python_project(temp_project):
    """Test detecting Python project."""
    (temp_project / "pyproject.toml").write_text("""[project]
name = "test"
dependencies = ["fastapi"]
""")

    tech = detect_project_technology(temp_project)

    assert tech.primary_language == "python"
    assert tech.framework == "fastapi"
    assert tech.package_manager == "pip"


def test_detect_technology_nodejs_project(temp_project):
    """Test detecting Node.js project."""
    (temp_project / "package.json").write_text(json.dumps({
        "name": "test-project",
        "dependencies": {
            "express": "^4.18.0"
        }
    }))

    tech = detect_project_technology(temp_project)

    assert tech.primary_language == "nodejs"
    assert tech.framework == "express"
    assert tech.package_manager == "npm"


def test_detect_technology_typescript_project(temp_project):
    """Test detecting TypeScript project."""
    (temp_project / "package.json").write_text(json.dumps({
        "name": "test-ts",
        "dependencies": {"react": "^18.0.0"}
    }))
    (temp_project / "tsconfig.json").write_text(json.dumps({
        "compilerOptions": {"target": "ES2020"}
    }))

    tech = detect_project_technology(temp_project)

    assert tech.primary_language == "typescript"
    assert tech.framework == "react"


def test_detect_technology_nextjs_project(temp_project):
    """Test detecting Next.js project."""
    (temp_project / "package.json").write_text(json.dumps({
        "dependencies": {"next": "^13.0.0", "react": "^18.0.0"}
    }))

    tech = detect_project_technology(temp_project)

    assert tech.framework == "nextjs"


def test_detect_technology_rust_project(temp_project):
    """Test detecting Rust project."""
    (temp_project / "Cargo.toml").write_text("""[package]
name = "test"
version = "0.1.0"
""")

    tech = detect_project_technology(temp_project)

    assert tech.primary_language == "rust"


def test_detect_technology_go_project(temp_project):
    """Test detecting Go project."""
    (temp_project / "go.mod").write_text("""module example.com/test

go 1.21
""")

    tech = detect_project_technology(temp_project)

    assert tech.primary_language == "go"


def test_detect_technology_python_with_poetry(temp_project):
    """Test detecting Python project with Poetry."""
    (temp_project / "pyproject.toml").write_text("[tool.poetry]\nname = \"test\"\n")
    (temp_project / "poetry.lock").write_text("")

    tech = detect_project_technology(temp_project)

    assert tech.primary_language == "python"
    assert tech.package_manager == "poetry"


def test_detect_technology_python_with_pipenv(temp_project):
    """Test detecting Python project with Pipenv."""
    (temp_project / "Pipfile").write_text("[packages]\nrequests = \"*\"\n")

    tech = detect_project_technology(temp_project)

    assert tech.primary_language == "python"
    assert tech.package_manager == "pipenv"


def test_detect_technology_pnpm_package_manager(temp_project):
    """Test detecting pnpm package manager."""
    (temp_project / "package.json").write_text(json.dumps({"name": "test"}))
    (temp_project / "pnpm-lock.yaml").write_text("")

    tech = detect_project_technology(temp_project)

    assert tech.package_manager == "pnpm"


def test_detect_technology_yarn_package_manager(temp_project):
    """Test detecting yarn package manager."""
    (temp_project / "package.json").write_text(json.dumps({"name": "test"}))
    (temp_project / "yarn.lock").write_text("")

    tech = detect_project_technology(temp_project)

    assert tech.package_manager == "yarn"


def test_detect_technology_with_docker(temp_project):
    """Test detecting Docker service."""
    (temp_project / "Dockerfile").write_text("FROM node:18\n")
    (temp_project / "package.json").write_text(json.dumps({"name": "test"}))

    tech = detect_project_technology(temp_project)

    assert "docker" in tech.detected_services


def test_detect_technology_with_github_actions(temp_project):
    """Test detecting GitHub Actions."""
    (temp_project / ".github" / "workflows").mkdir(parents=True)
    (temp_project / ".github" / "workflows" / "test.yml").write_text("name: Test\n")
    (temp_project / "package.json").write_text(json.dumps({"name": "test"}))

    tech = detect_project_technology(temp_project)

    assert "github-actions" in tech.detected_services


def test_detect_technology_with_monorepo(mock_monorepo_pnpm):
    """Test detecting monorepo type."""
    tech = detect_project_technology(mock_monorepo_pnpm)

    assert tech.monorepo_type == "pnpm"


def test_detect_technology_unknown_project(temp_project):
    """Test detecting unknown project type."""
    # Empty directory
    tech = detect_project_technology(temp_project)

    assert tech.primary_language == "unknown"
    assert tech.framework is None
    assert tech.package_manager is None


# =============================================================================
# Context Generation Tests
# =============================================================================


def test_generate_mcp_context_creates_files(temp_project):
    """Test that context generation creates the expected files."""
    servers = [
        MCPServer(
            name="git",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-git"],
            source="project",
            description="Git operations",
            capabilities=["status", "diff", "log"],
        )
    ]
    tech = ProjectTechnology(
        primary_language="python",
        framework="fastapi",
        package_manager="pip",
    )

    generate_mcp_context(temp_project, servers, tech)

    # Check files were created
    assert (temp_project / ".specify" / "context" / "mcp-servers.md").exists()
    assert (temp_project / ".specify" / "context" / "project-context.json").exists()


def test_generate_mcp_context_markdown_format(temp_project):
    """Test markdown file content format."""
    servers = [
        MCPServer(
            name="postgres",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-postgres"],
            source="project",
            description="PostgreSQL operations",
            capabilities=["query", "list_tables", "describe_table"],
        )
    ]
    tech = ProjectTechnology(primary_language="python")

    generate_mcp_context(temp_project, servers, tech)

    md_content = (temp_project / ".specify" / "context" / "mcp-servers.md").read_text()

    assert "# MCP Servers Available" in md_content
    assert "postgres" in md_content
    assert "PostgreSQL operations" in md_content
    assert "| Server |" in md_content  # Table header


def test_generate_mcp_context_json_format(temp_project):
    """Test JSON file content format."""
    servers = [
        MCPServer(
            name="filesystem",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
            source="claude_desktop",
        )
    ]
    tech = ProjectTechnology(
        primary_language="typescript",
        framework="react",
        package_manager="pnpm",
    )

    generate_mcp_context(temp_project, servers, tech)

    json_content = (temp_project / ".specify" / "context" / "project-context.json").read_text()
    data = json.loads(json_content)

    assert "mcp_servers" in data
    assert "technology" in data
    assert len(data["mcp_servers"]) == 1
    assert data["mcp_servers"][0]["name"] == "filesystem"
    assert data["technology"]["primary_language"] == "typescript"
    assert data["technology"]["framework"] == "react"


def test_generate_mcp_context_no_servers(temp_project):
    """Test context generation with no servers."""
    servers = []
    tech = ProjectTechnology(primary_language="python")

    generate_mcp_context(temp_project, servers, tech)

    md_content = (temp_project / ".specify" / "context" / "mcp-servers.md").read_text()

    assert "No MCP servers discovered" in md_content


def test_generate_mcp_context_many_capabilities(temp_project):
    """Test that capabilities are truncated in markdown."""
    servers = [
        MCPServer(
            name="comprehensive",
            command="test",
            source="test",
            description="Many capabilities",
            capabilities=["cap1", "cap2", "cap3", "cap4", "cap5", "cap6"],
        )
    ]
    tech = ProjectTechnology(primary_language="python")

    generate_mcp_context(temp_project, servers, tech)

    md_content = (temp_project / ".specify" / "context" / "mcp-servers.md").read_text()

    # Should show first 3 + count of remaining
    assert "+3 more" in md_content


# =============================================================================
# Edge Cases and Integration Tests
# =============================================================================


def test_cross_platform_config_paths():
    """Test that config paths work on all platforms."""
    paths = get_mcp_config_paths()

    assert isinstance(paths, dict)
    assert "claude_desktop" in paths
    assert all(isinstance(v, Path) for v in paths.values())


def test_mcp_server_validation():
    """Test MCPServer dataclass validation."""
    # Valid server
    server = MCPServer(
        name="test",
        command="cmd",
        args=["arg1"],
        env={"KEY": "value"},
    )
    assert isinstance(server.args, list)
    assert isinstance(server.env, dict)


def test_discover_mcp_servers_default_cwd(temp_project, monkeypatch):
    """Test that discover_mcp_servers uses CWD when no project_dir given."""
    monkeypatch.chdir(temp_project)

    # Create config in current directory
    (temp_project / "mcp.json").write_text(json.dumps({
        "mcpServers": {
            "local": {"command": "node", "args": ["server.js"]}
        }
    }))

    servers = discover_mcp_servers()  # No project_dir argument

    assert any(s.name == "local" for s in servers)
