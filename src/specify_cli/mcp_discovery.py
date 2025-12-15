"""
MCP Server Discovery for project-specify

Detects available MCP (Model Context Protocol) servers from various sources
and generates context files that commands can reference.
"""

from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from .errors import MCPDiscoveryError


@dataclass
class MCPServer:
    """Represents a discovered MCP server."""
    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    source: str = ""  # Where it was discovered
    description: str = ""
    capabilities: list[str] = field(default_factory=list)


@dataclass
class ProjectTechnology:
    """Detected project technology stack."""
    primary_language: str
    framework: Optional[str] = None
    package_manager: Optional[str] = None
    database: Optional[str] = None
    monorepo_type: Optional[str] = None
    detected_services: list[str] = field(default_factory=list)


# Known MCP servers and their typical capabilities
KNOWN_MCP_SERVERS = {
    "filesystem": {
        "description": "Read/write files and directories",
        "capabilities": ["read_file", "write_file", "list_directory", "search_files"],
    },
    "git": {
        "description": "Git repository operations",
        "capabilities": ["git_status", "git_diff", "git_log", "git_commit"],
    },
    "github": {
        "description": "GitHub API operations",
        "capabilities": ["create_issue", "create_pr", "search_repos", "get_file_contents"],
    },
    "postgres": {
        "description": "PostgreSQL database operations",
        "capabilities": ["query", "list_tables", "describe_table"],
    },
    "sqlite": {
        "description": "SQLite database operations",
        "capabilities": ["query", "list_tables", "describe_table"],
    },
    "puppeteer": {
        "description": "Browser automation and web scraping",
        "capabilities": ["navigate", "screenshot", "click", "fill"],
    },
    "brave-search": {
        "description": "Web search via Brave Search API",
        "capabilities": ["web_search", "local_search"],
    },
    "fetch": {
        "description": "HTTP fetch operations",
        "capabilities": ["fetch_url", "fetch_html", "fetch_json"],
    },
}


def get_mcp_config_paths() -> dict[str, Path]:
    """Get paths to MCP configuration files for various tools."""
    system = platform.system()
    home = Path.home()
    
    paths = {}
    
    if system == "Darwin":  # macOS
        paths["claude_desktop"] = home / "Library/Application Support/Claude/claude_desktop_config.json"
        paths["claude_code"] = home / ".claude/mcp_servers.json"
        paths["cursor"] = home / ".cursor/mcp.json"
    elif system == "Windows":
        appdata = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
        paths["claude_desktop"] = appdata / "Claude/claude_desktop_config.json"
        paths["claude_code"] = home / ".claude/mcp_servers.json"
        paths["cursor"] = appdata / "Cursor/mcp.json"
    else:  # Linux
        config_home = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        paths["claude_desktop"] = config_home / "Claude/claude_desktop_config.json"
        paths["claude_code"] = home / ".claude/mcp_servers.json"
        paths["cursor"] = config_home / "cursor/mcp.json"
    
    return paths


def discover_mcp_servers(project_dir: Optional[Path] = None) -> list[MCPServer]:
    """Discover all available MCP servers from various sources."""
    if project_dir is None:
        project_dir = Path.cwd()
    
    servers = []
    
    config_paths = get_mcp_config_paths()
    
    for source, path in config_paths.items():
        if path.exists():
            try:
                servers.extend(_parse_mcp_config(path, source))
            except Exception as e:
                # Log but don't fail - a single corrupted config shouldn't break discovery
                import logging
                logging.debug(f"Failed to parse MCP config from {source}: {e}")
    
    # Check for project-local MCP config
    local_configs = [
        project_dir / ".mcp/servers.json",
        project_dir / "mcp.json",
        project_dir / ".mcp.json",
    ]
    
    for config_path in local_configs:
        if config_path.exists():
            try:
                servers.extend(_parse_mcp_config(config_path, "project"))
            except Exception as e:
                # Project-local config errors should be visible
                import logging
                logging.warning(f"Failed to parse project MCP config at {config_path}: {e}")
    
    # Deduplicate by name, preferring project > claude_code > claude_desktop > others
    return _deduplicate_servers(servers)


def _parse_mcp_config(path: Path, source: str) -> list[MCPServer]:
    """Parse an MCP configuration file.

    Args:
        path: Path to MCP configuration file.
        source: Source identifier (e.g., "claude_desktop", "project").

    Returns:
        List of discovered MCP servers.

    Raises:
        MCPDiscoveryError: If the config file is malformed.
    """
    servers = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise MCPDiscoveryError(
            f"Invalid JSON in {source} MCP config at {path}: {e}"
        ) from e
    except Exception as e:
        raise MCPDiscoveryError(
            f"Failed to read {source} MCP config at {path}: {e}"
        ) from e
    
    # Handle different config formats
    mcp_servers = data.get("mcpServers") or data.get("servers") or {}
    
    for name, config in mcp_servers.items():
        if isinstance(config, dict):
            command = config.get("command", "")
            args = config.get("args", [])
            env = config.get("env", {})
            
            # Look up known server info
            known_info = KNOWN_MCP_SERVERS.get(name, {})
            
            server = MCPServer(
                name=name,
                command=command,
                args=args if isinstance(args, list) else [],
                env=env if isinstance(env, dict) else {},
                source=source,
                description=known_info.get("description", ""),
                capabilities=known_info.get("capabilities", []),
            )
            servers.append(server)
    
    return servers


def _deduplicate_servers(servers: list[MCPServer]) -> list[MCPServer]:
    """Deduplicate servers by name, preferring higher-priority sources."""
    source_priority = {
        "project": 0,
        "claude_code": 1,
        "claude_desktop": 2,
        "cursor": 3,
    }
    
    seen = {}
    for server in servers:
        name = server.name
        priority = source_priority.get(server.source, 99)
        
        if name not in seen or priority < source_priority.get(seen[name].source, 99):
            seen[name] = server
    
    return list(seen.values())


def detect_project_technology(project_dir: Path) -> ProjectTechnology:
    """Detect the project's technology stack."""
    primary_language = "unknown"
    framework = None
    package_manager = None
    database = None
    detected_services = []
    
    # Detect language
    if (project_dir / "package.json").exists():
        primary_language = "typescript" if (project_dir / "tsconfig.json").exists() else "nodejs"
        package_manager = "npm"
        if (project_dir / "yarn.lock").exists():
            package_manager = "yarn"
        elif (project_dir / "pnpm-lock.yaml").exists():
            package_manager = "pnpm"
        
        # Detect framework
        try:
            with open(project_dir / "package.json", "r", encoding="utf-8") as f:
                pkg_data = json.load(f)
                deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                if "next" in deps:
                    framework = "nextjs"
                elif "react" in deps:
                    framework = "react"
                elif "vue" in deps:
                    framework = "vue"
                elif "express" in deps:
                    framework = "express"
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            # Silently skip framework detection if package.json is invalid
            pass
    elif (project_dir / "Cargo.toml").exists():
        primary_language = "rust"
    elif (project_dir / "go.mod").exists():
        primary_language = "go"
    elif (project_dir / "pyproject.toml").exists() or (project_dir / "requirements.txt").exists() or (project_dir / "Pipfile").exists():
        primary_language = "python"
        package_manager = "pip"
        if (project_dir / "Pipfile").exists():
            package_manager = "pipenv"
        elif (project_dir / "poetry.lock").exists():
            package_manager = "poetry"
        
        # Detect framework
        try:
            if (project_dir / "pyproject.toml").exists():
                content = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
                if "django" in content.lower():
                    framework = "django"
                elif "flask" in content.lower():
                    framework = "flask"
                elif "fastapi" in content.lower():
                    framework = "fastapi"
        except (FileNotFoundError, UnicodeDecodeError):
            # Silently skip framework detection if file is unreadable
            pass
    elif (project_dir / "pom.xml").exists() or (project_dir / "build.gradle").exists():
        primary_language = "java"
        package_manager = "maven" if (project_dir / "pom.xml").exists() else "gradle"
    
    # Detect database
    if (project_dir / "docker-compose.yml").exists() or (project_dir / "docker-compose.yaml").exists():
        try:
            import yaml
            compose_file = project_dir / "docker-compose.yml"
            if not compose_file.exists():
                compose_file = project_dir / "docker-compose.yaml"
            if compose_file.exists():
                with open(compose_file, "r", encoding="utf-8") as f:
                    compose_data = yaml.safe_load(f)
                    services = compose_data.get("services", {})
                    for service_name, service_config in services.items():
                        image = service_config.get("image", "")
                        if "postgres" in image.lower():
                            database = "postgresql"
                        elif "mysql" in image.lower():
                            database = "mysql"
                        elif "mongodb" in image.lower():
                            database = "mongodb"
                        elif "redis" in image.lower():
                            detected_services.append("redis")
        except (ImportError, FileNotFoundError, yaml.YAMLError):
            # Silently skip docker-compose detection if yaml unavailable or file invalid
            pass
    
    # Detect services
    if (project_dir / "Dockerfile").exists():
        detected_services.append("docker")
    if (project_dir / ".github/workflows").exists():
        detected_services.append("github-actions")
    if (project_dir / "k8s").exists() or (project_dir / "kubernetes").exists():
        detected_services.append("kubernetes")
    
    # Detect monorepo
    from .monorepo import detect_monorepo_type
    monorepo_type = detect_monorepo_type(project_dir)
    
    return ProjectTechnology(
        primary_language=primary_language,
        framework=framework,
        package_manager=package_manager,
        database=database,
        monorepo_type=monorepo_type,
        detected_services=detected_services,
    )


def generate_mcp_context(project_dir: Path, servers: list[MCPServer], tech: ProjectTechnology) -> None:
    """Generate MCP context files in .specify/context/."""
    context_dir = project_dir / ".specify" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate markdown summary
    md_file = context_dir / "mcp-servers.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# MCP Servers Available\n\n")
        f.write(f"**Generated:** {__import__('datetime').datetime.now().isoformat()}\n\n")
        
        if servers:
            f.write("## Discovered Servers\n\n")
            f.write("| Server | Source | Description | Capabilities |\n")
            f.write("|--------|--------|-------------|--------------|\n")
            for server in servers:
                caps = ", ".join(server.capabilities[:3])
                if len(server.capabilities) > 3:
                    caps += f" (+{len(server.capabilities) - 3} more)"
                f.write(f"| {server.name} | {server.source} | {server.description} | {caps} |\n")
        else:
            f.write("No MCP servers discovered.\n")
    
    # Generate JSON context
    json_file = context_dir / "project-context.json"
    context_data = {
        "mcp_servers": [asdict(s) for s in servers],
        "technology": asdict(tech),
    }
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(context_data, f, indent=2)


def get_available_mcp_operations(project_dir: Optional[Path] = None) -> dict[str, list[str]]:
    """
    Return only operations available with current MCP configuration.

    This function discovers installed MCP servers and maps them to available
    operations that AI assistants can use. Useful for validating that certain
    operations are possible before suggesting them to users.

    Args:
        project_dir: Project directory to scan (defaults to current directory)

    Returns:
        Dictionary mapping operation categories to available operations.
        Example: {"database": ["query", "describe_table"], "git": ["status", "diff"]}
    """
    if project_dir is None:
        project_dir = Path.cwd()

    servers = discover_mcp_servers(project_dir)
    server_names = {s.name.lower() for s in servers}

    operations = {}

    # Database operations
    if "postgres" in server_names or "postgresql" in server_names or "sqlite" in server_names:
        operations["database"] = [
            "query",
            "describe_table",
            "analyze_schema",
            "list_tables",
            "execute_sql"
        ]

    # Git operations
    if "git" in server_names:
        operations["git"] = [
            "status",
            "diff",
            "log",
            "blame",
            "show",
            "commit"
        ]

    # GitHub operations
    if "github" in server_names:
        operations["github"] = [
            "create_issue",
            "create_pr",
            "search_code",
            "list_issues",
            "comment_on_pr"
        ]

    # Filesystem operations
    if "filesystem" in server_names:
        operations["filesystem"] = [
            "read",
            "write",
            "search",
            "list",
            "delete"
        ]

    # HTTP/Fetch operations
    if "fetch" in server_names or "http" in server_names:
        operations["http"] = [
            "get",
            "post",
            "put",
            "delete"
        ]

    return operations

