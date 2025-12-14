"""
MCP Server Discovery for project-specify

Detects available MCP (Model Context Protocol) servers from various sources:
1. Claude Desktop configuration
2. Claude Code configuration  
3. Cursor MCP configuration
4. VS Code MCP extensions
5. Local MCP server installations
6. Project-specific MCP configurations

Then generates context files that commands can reference to know what
tools are available for the AI agent to use.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


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
        "relevant_for": ["all"],
    },
    "git": {
        "description": "Git repository operations",
        "capabilities": ["git_status", "git_diff", "git_log", "git_commit"],
        "relevant_for": ["all"],
    },
    "github": {
        "description": "GitHub API operations",
        "capabilities": ["create_issue", "create_pr", "search_repos", "get_file_contents"],
        "relevant_for": ["all"],
    },
    "postgres": {
        "description": "PostgreSQL database operations",
        "capabilities": ["query", "list_tables", "describe_table"],
        "relevant_for": ["python", "nodejs", "rust", "go"],
    },
    "sqlite": {
        "description": "SQLite database operations",
        "capabilities": ["query", "list_tables", "describe_table"],
        "relevant_for": ["python", "nodejs", "rust"],
    },
    "puppeteer": {
        "description": "Browser automation and web scraping",
        "capabilities": ["navigate", "screenshot", "click", "fill"],
        "relevant_for": ["nodejs", "typescript"],
    },
    "brave-search": {
        "description": "Web search via Brave Search API",
        "capabilities": ["web_search", "local_search"],
        "relevant_for": ["all"],
    },
    "fetch": {
        "description": "HTTP fetch operations",
        "capabilities": ["fetch_url", "fetch_html", "fetch_json"],
        "relevant_for": ["all"],
    },
    "memory": {
        "description": "Persistent memory/knowledge graph",
        "capabilities": ["store", "retrieve", "search_memory"],
        "relevant_for": ["all"],
    },
    "sequential-thinking": {
        "description": "Step-by-step reasoning assistance",
        "capabilities": ["think_step", "plan", "reflect"],
        "relevant_for": ["all"],
    },
    "slack": {
        "description": "Slack workspace operations",
        "capabilities": ["send_message", "read_channel", "search_messages"],
        "relevant_for": ["all"],
    },
    "linear": {
        "description": "Linear issue tracking",
        "capabilities": ["create_issue", "update_issue", "search_issues"],
        "relevant_for": ["all"],
    },
    "sentry": {
        "description": "Sentry error tracking",
        "capabilities": ["get_issues", "resolve_issue", "get_event"],
        "relevant_for": ["all"],
    },
    "docker": {
        "description": "Docker container operations",
        "capabilities": ["list_containers", "run_container", "logs"],
        "relevant_for": ["all"],
    },
    "kubernetes": {
        "description": "Kubernetes cluster operations",
        "capabilities": ["get_pods", "get_services", "apply_manifest"],
        "relevant_for": ["all"],
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
        paths["vscode"] = home / ".vscode/mcp.json"
    elif system == "Windows":
        appdata = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
        localappdata = Path(os.environ.get("LOCALAPPDATA", home / "AppData/Local"))
        paths["claude_desktop"] = appdata / "Claude/claude_desktop_config.json"
        paths["claude_code"] = home / ".claude/mcp_servers.json"
        paths["cursor"] = appdata / "Cursor/mcp.json"
        paths["vscode"] = appdata / "Code/User/mcp.json"
    else:  # Linux
        config_home = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        paths["claude_desktop"] = config_home / "Claude/claude_desktop_config.json"
        paths["claude_code"] = home / ".claude/mcp_servers.json"
        paths["cursor"] = config_home / "cursor/mcp.json"
        paths["vscode"] = config_home / "Code/User/mcp.json"
    
    return paths


def discover_mcp_servers() -> list[MCPServer]:
    """Discover all available MCP servers from various sources."""
    servers = []
    
    config_paths = get_mcp_config_paths()
    
    for source, path in config_paths.items():
        if path.exists():
            try:
                servers.extend(_parse_mcp_config(path, source))
            except Exception as e:
                print(f"Warning: Could not parse {path}: {e}")
    
    # Check for project-local MCP config
    local_configs = [
        Path(".mcp/servers.json"),
        Path("mcp.json"),
        Path(".mcp.json"),
    ]
    
    for config_path in local_configs:
        if config_path.exists():
            try:
                servers.extend(_parse_mcp_config(config_path, "project"))
            except Exception:
                pass
    
    # Check for globally installed MCP servers via npx/uvx
    servers.extend(_discover_installed_servers())
    
    # Deduplicate by name, preferring project > claude_code > claude_desktop > others
    return _deduplicate_servers(servers)


def _parse_mcp_config(path: Path, source: str) -> list[MCPServer]:
    """Parse an MCP configuration file."""
    servers = []
    
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return servers
    
    # Handle different config formats
    mcp_servers = data.get("mcpServers", data.get("servers", data))
    
    if isinstance(mcp_servers, dict):
        for name, config in mcp_servers.items():
            if isinstance(config, dict):
                server = MCPServer(
                    name=name,
                    command=config.get("command", ""),
                    args=config.get("args", []),
                    env=config.get("env", {}),
                    source=source,
                )
                
                # Add known capabilities if we recognize the server
                if name in KNOWN_MCP_SERVERS:
                    server.description = KNOWN_MCP_SERVERS[name]["description"]
                    server.capabilities = KNOWN_MCP_SERVERS[name]["capabilities"]
                
                servers.append(server)
    
    return servers


def _discover_installed_servers() -> list[MCPServer]:
    """Check for commonly installed MCP servers."""
    servers = []
    
    # Check for npx-available servers
    npx_servers = [
        ("@modelcontextprotocol/server-filesystem", "filesystem"),
        ("@modelcontextprotocol/server-git", "git"),
        ("@modelcontextprotocol/server-github", "github"),
        ("@modelcontextprotocol/server-postgres", "postgres"),
        ("@modelcontextprotocol/server-sqlite", "sqlite"),
        ("@modelcontextprotocol/server-puppeteer", "puppeteer"),
        ("@modelcontextprotocol/server-brave-search", "brave-search"),
        ("@modelcontextprotocol/server-fetch", "fetch"),
        ("@modelcontextprotocol/server-memory", "memory"),
        ("@modelcontextprotocol/server-sequential-thinking", "sequential-thinking"),
    ]
    
    # Quick check if npx is available
    npx_available = subprocess.run(
        ["which", "npx"], capture_output=True
    ).returncode == 0
    
    if npx_available:
        for package, name in npx_servers:
            # We don't actually run them, just note they're available via npx
            if name in KNOWN_MCP_SERVERS:
                servers.append(MCPServer(
                    name=name,
                    command="npx",
                    args=["-y", package],
                    source="npx",
                    description=KNOWN_MCP_SERVERS[name]["description"],
                    capabilities=KNOWN_MCP_SERVERS[name]["capabilities"],
                ))
    
    # Check for uvx-available servers (Python MCP servers)
    uvx_servers = [
        ("mcp-server-fetch", "fetch"),
        ("mcp-server-sqlite", "sqlite"),
    ]
    
    uvx_available = subprocess.run(
        ["which", "uvx"], capture_output=True
    ).returncode == 0
    
    if uvx_available:
        for package, name in uvx_servers:
            if name in KNOWN_MCP_SERVERS and not any(s.name == name for s in servers):
                servers.append(MCPServer(
                    name=name,
                    command="uvx",
                    args=[package],
                    source="uvx",
                    description=KNOWN_MCP_SERVERS[name]["description"],
                    capabilities=KNOWN_MCP_SERVERS[name]["capabilities"],
                ))
    
    return servers


def _deduplicate_servers(servers: list[MCPServer]) -> list[MCPServer]:
    """Deduplicate servers, preferring more specific sources."""
    priority = {"project": 0, "claude_code": 1, "claude_desktop": 2, "cursor": 3, "vscode": 4, "npx": 5, "uvx": 6}
    
    by_name: dict[str, MCPServer] = {}
    for server in servers:
        if server.name not in by_name:
            by_name[server.name] = server
        else:
            existing = by_name[server.name]
            if priority.get(server.source, 99) < priority.get(existing.source, 99):
                by_name[server.name] = server
    
    return list(by_name.values())


def detect_project_technology(project_dir: Path) -> ProjectTechnology:
    """Detect the technology stack of a project."""
    tech = ProjectTechnology(primary_language="unknown")
    
    # Detect primary language and package manager
    if (project_dir / "package.json").exists():
        tech.primary_language = "nodejs"
        tech.package_manager = _detect_node_package_manager(project_dir)
        
        # Check for TypeScript
        if (project_dir / "tsconfig.json").exists():
            tech.primary_language = "typescript"
        
        # Detect framework
        tech.framework = _detect_node_framework(project_dir)
        
    elif (project_dir / "Cargo.toml").exists():
        tech.primary_language = "rust"
        tech.package_manager = "cargo"
        tech.framework = _detect_rust_framework(project_dir)
        
    elif (project_dir / "go.mod").exists():
        tech.primary_language = "go"
        tech.package_manager = "go"
        
    elif (project_dir / "pyproject.toml").exists() or (project_dir / "requirements.txt").exists():
        tech.primary_language = "python"
        tech.package_manager = _detect_python_package_manager(project_dir)
        tech.framework = _detect_python_framework(project_dir)
        
    elif (project_dir / "pom.xml").exists():
        tech.primary_language = "java"
        tech.package_manager = "maven"
        
    elif (project_dir / "build.gradle").exists() or (project_dir / "build.gradle.kts").exists():
        tech.primary_language = "java"  # or kotlin
        tech.package_manager = "gradle"
    
    # Detect database
    tech.database = _detect_database(project_dir)
    
    # Detect monorepo type
    tech.monorepo_type = _detect_monorepo(project_dir)
    
    # Detect services (Docker, K8s, etc.)
    tech.detected_services = _detect_services(project_dir)
    
    return tech


def _detect_node_package_manager(project_dir: Path) -> str:
    """Detect Node.js package manager."""
    if (project_dir / "pnpm-lock.yaml").exists():
        return "pnpm"
    elif (project_dir / "yarn.lock").exists():
        return "yarn"
    elif (project_dir / "bun.lockb").exists():
        return "bun"
    elif (project_dir / "package-lock.json").exists():
        return "npm"
    return "npm"


def _detect_node_framework(project_dir: Path) -> Optional[str]:
    """Detect Node.js framework from package.json."""
    try:
        pkg = json.loads((project_dir / "package.json").read_text())
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        
        frameworks = [
            ("next", "Next.js"),
            ("nuxt", "Nuxt"),
            ("@remix-run/react", "Remix"),
            ("astro", "Astro"),
            ("svelte", "SvelteKit"),
            ("express", "Express"),
            ("fastify", "Fastify"),
            ("hono", "Hono"),
            ("@nestjs/core", "NestJS"),
            ("react", "React"),
            ("vue", "Vue"),
            ("@angular/core", "Angular"),
        ]
        
        for dep, name in frameworks:
            if dep in deps:
                return name
    except Exception:
        pass
    return None


def _detect_rust_framework(project_dir: Path) -> Optional[str]:
    """Detect Rust framework from Cargo.toml."""
    try:
        content = (project_dir / "Cargo.toml").read_text()
        frameworks = [
            ("actix-web", "Actix Web"),
            ("axum", "Axum"),
            ("rocket", "Rocket"),
            ("warp", "Warp"),
            ("tauri", "Tauri"),
            ("leptos", "Leptos"),
            ("yew", "Yew"),
        ]
        for dep, name in frameworks:
            if dep in content:
                return name
    except Exception:
        pass
    return None


def _detect_python_package_manager(project_dir: Path) -> str:
    """Detect Python package manager."""
    if (project_dir / "poetry.lock").exists():
        return "poetry"
    elif (project_dir / "Pipfile.lock").exists():
        return "pipenv"
    elif (project_dir / "uv.lock").exists():
        return "uv"
    elif (project_dir / "pdm.lock").exists():
        return "pdm"
    return "pip"


def _detect_python_framework(project_dir: Path) -> Optional[str]:
    """Detect Python framework."""
    files_to_check = ["pyproject.toml", "requirements.txt", "setup.py"]
    content = ""
    
    for f in files_to_check:
        path = project_dir / f
        if path.exists():
            content += path.read_text()
    
    frameworks = [
        ("fastapi", "FastAPI"),
        ("django", "Django"),
        ("flask", "Flask"),
        ("starlette", "Starlette"),
        ("litestar", "Litestar"),
        ("streamlit", "Streamlit"),
        ("gradio", "Gradio"),
    ]
    
    for dep, name in frameworks:
        if dep in content.lower():
            return name
    return None


def _detect_database(project_dir: Path) -> Optional[str]:
    """Detect database from project files."""
    # Check for common database indicators
    indicators = {
        "postgres": ["postgres", "postgresql", "psycopg", "asyncpg", "pg"],
        "mysql": ["mysql", "pymysql", "mysqlclient"],
        "sqlite": ["sqlite", "sqlite3", "better-sqlite3"],
        "mongodb": ["mongodb", "mongoose", "pymongo"],
        "redis": ["redis", "ioredis"],
        "supabase": ["supabase", "@supabase/supabase-js"],
        "prisma": ["prisma", "@prisma/client"],
        "drizzle": ["drizzle-orm"],
    }
    
    files_to_check = [
        "package.json", "requirements.txt", "pyproject.toml", 
        "Cargo.toml", "docker-compose.yml", "docker-compose.yaml",
        ".env.example", ".env",
    ]
    
    content = ""
    for f in files_to_check:
        path = project_dir / f
        if path.exists():
            try:
                content += path.read_text().lower()
            except Exception:
                pass
    
    for db, keywords in indicators.items():
        if any(kw in content for kw in keywords):
            return db
    
    return None


def _detect_monorepo(project_dir: Path) -> Optional[str]:
    """Detect monorepo type."""
    if (project_dir / "pnpm-workspace.yaml").exists():
        return "pnpm"
    elif (project_dir / "lerna.json").exists():
        return "lerna"
    elif (project_dir / "nx.json").exists():
        return "nx"
    elif (project_dir / "turbo.json").exists():
        return "turborepo"
    elif (project_dir / "package.json").exists():
        try:
            pkg = json.loads((project_dir / "package.json").read_text())
            if "workspaces" in pkg:
                return "npm-workspaces"
        except Exception:
            pass
    elif (project_dir / "Cargo.toml").exists():
        try:
            if "[workspace]" in (project_dir / "Cargo.toml").read_text():
                return "cargo"
        except Exception:
            pass
    return None


def _detect_services(project_dir: Path) -> list[str]:
    """Detect infrastructure services."""
    services = []
    
    if (project_dir / "Dockerfile").exists():
        services.append("docker")
    if (project_dir / "docker-compose.yml").exists() or (project_dir / "docker-compose.yaml").exists():
        services.append("docker-compose")
    if (project_dir / "kubernetes").is_dir() or any(project_dir.glob("k8s/**/*.yaml")):
        services.append("kubernetes")
    if (project_dir / ".github/workflows").is_dir():
        services.append("github-actions")
    if (project_dir / ".gitlab-ci.yml").exists():
        services.append("gitlab-ci")
    if (project_dir / "vercel.json").exists():
        services.append("vercel")
    if (project_dir / "netlify.toml").exists():
        services.append("netlify")
    if (project_dir / "fly.toml").exists():
        services.append("fly.io")
    if (project_dir / "railway.json").exists():
        services.append("railway")
    if (project_dir / "terraform").is_dir() or any(project_dir.glob("*.tf")):
        services.append("terraform")
    if (project_dir / "pulumi").is_dir() or (project_dir / "Pulumi.yaml").exists():
        services.append("pulumi")
    
    return services


def generate_mcp_context(
    project_dir: Path,
    servers: list[MCPServer],
    technology: ProjectTechnology,
) -> str:
    """Generate MCP context markdown for commands to reference."""
    
    lines = [
        "# MCP Server Context",
        "",
        "This file documents the available MCP servers and project technology context.",
        "AI agents should reference this when planning implementations.",
        "",
        "## Available MCP Servers",
        "",
    ]
    
    if servers:
        lines.append("| Server | Description | Capabilities | Source |")
        lines.append("|--------|-------------|--------------|--------|")
        for server in servers:
            caps = ", ".join(server.capabilities[:3])
            if len(server.capabilities) > 3:
                caps += f" (+{len(server.capabilities) - 3} more)"
            lines.append(f"| {server.name} | {server.description} | {caps} | {server.source} |")
    else:
        lines.append("*No MCP servers detected. Consider configuring MCP servers for enhanced capabilities.*")
    
    lines.extend([
        "",
        "## Project Technology Stack",
        "",
        f"- **Primary Language:** {technology.primary_language}",
    ])
    
    if technology.framework:
        lines.append(f"- **Framework:** {technology.framework}")
    if technology.package_manager:
        lines.append(f"- **Package Manager:** {technology.package_manager}")
    if technology.database:
        lines.append(f"- **Database:** {technology.database}")
    if technology.monorepo_type:
        lines.append(f"- **Monorepo Type:** {technology.monorepo_type}")
    if technology.detected_services:
        lines.append(f"- **Services:** {', '.join(technology.detected_services)}")
    
    lines.extend([
        "",
        "## Recommended MCP Servers for This Project",
        "",
    ])
    
    # Recommend servers based on technology
    recommendations = _get_server_recommendations(technology, servers)
    if recommendations["configured"]:
        lines.append("### Already Configured ✅")
        for rec in recommendations["configured"]:
            lines.append(f"- **{rec['name']}**: {rec['reason']}")
        lines.append("")
    
    if recommendations["suggested"]:
        lines.append("### Suggested Additions")
        for rec in recommendations["suggested"]:
            lines.append(f"- **{rec['name']}**: {rec['reason']}")
            if rec.get("install"):
                lines.append(f"  - Install: `{rec['install']}`")
        lines.append("")
    
    lines.extend([
        "## Usage in Commands",
        "",
        "When implementing features, consider leveraging these MCP capabilities:",
        "",
    ])
    
    # Add usage hints based on available servers
    for server in servers:
        if server.name == "filesystem":
            lines.append("- Use **filesystem** MCP for file operations instead of shell commands when appropriate")
        elif server.name == "git":
            lines.append("- Use **git** MCP for repository operations with better error handling")
        elif server.name == "github":
            lines.append("- Use **github** MCP to create issues, PRs, and interact with GitHub API")
        elif server.name in ("postgres", "sqlite"):
            lines.append(f"- Use **{server.name}** MCP for database queries and schema inspection")
        elif server.name == "puppeteer":
            lines.append("- Use **puppeteer** MCP for browser automation and E2E testing")
        elif server.name == "fetch":
            lines.append("- Use **fetch** MCP for HTTP requests to external APIs")
    
    lines.extend([
        "",
        "---",
        f"*Generated by project-specify*",
    ])
    
    return "\n".join(lines)


def _get_server_recommendations(
    technology: ProjectTechnology,
    configured_servers: list[MCPServer],
) -> dict:
    """Get server recommendations based on project technology."""
    configured_names = {s.name for s in configured_servers}
    
    configured = []
    suggested = []
    
    # Universal recommendations
    universal = [
        ("filesystem", "File operations for all projects"),
        ("git", "Version control operations"),
    ]
    
    for name, reason in universal:
        rec = {"name": name, "reason": reason}
        if name in configured_names:
            configured.append(rec)
        else:
            rec["install"] = f"npx -y @modelcontextprotocol/server-{name}"
            suggested.append(rec)
    
    # Database recommendations
    if technology.database:
        db_servers = {
            "postgres": ("postgres", "npx -y @modelcontextprotocol/server-postgres"),
            "sqlite": ("sqlite", "npx -y @modelcontextprotocol/server-sqlite"),
            "supabase": ("postgres", "npx -y @modelcontextprotocol/server-postgres"),
        }
        if technology.database in db_servers:
            name, install = db_servers[technology.database]
            rec = {"name": name, "reason": f"Database operations for {technology.database}"}
            if name in configured_names:
                configured.append(rec)
            else:
                rec["install"] = install
                suggested.append(rec)
    
    # Framework-specific recommendations
    if technology.framework in ("Next.js", "Remix", "Astro", "Nuxt"):
        rec = {"name": "puppeteer", "reason": "Browser testing for web framework"}
        if "puppeteer" in configured_names:
            configured.append(rec)
        else:
            rec["install"] = "npx -y @modelcontextprotocol/server-puppeteer"
            suggested.append(rec)
    
    # GitHub for all projects with .github
    if "github-actions" in technology.detected_services:
        rec = {"name": "github", "reason": "GitHub API for CI/CD integration"}
        if "github" in configured_names:
            configured.append(rec)
        else:
            rec["install"] = "npx -y @modelcontextprotocol/server-github"
            suggested.append(rec)
    
    return {"configured": configured, "suggested": suggested}


def run_discovery(project_dir: Path) -> tuple[list[MCPServer], ProjectTechnology, str]:
    """
    Run full MCP and technology discovery.
    
    Returns:
        Tuple of (servers, technology, context_markdown)
    """
    servers = discover_mcp_servers()
    technology = detect_project_technology(project_dir)
    context = generate_mcp_context(project_dir, servers, technology)
    
    return servers, technology, context


def write_context_files(project_dir: Path) -> None:
    """Write discovery results to project context files."""
    servers, technology, context_md = run_discovery(project_dir)
    
    # Create context directory
    context_dir = project_dir / ".specify" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)
    
    # Write MCP context
    (context_dir / "mcp-servers.md").write_text(context_md)
    
    # Write technology context as JSON for programmatic access
    tech_data = {
        "primary_language": technology.primary_language,
        "framework": technology.framework,
        "package_manager": technology.package_manager,
        "database": technology.database,
        "monorepo_type": technology.monorepo_type,
        "detected_services": technology.detected_services,
        "mcp_servers": [
            {
                "name": s.name,
                "description": s.description,
                "capabilities": s.capabilities,
                "source": s.source,
            }
            for s in servers
        ],
    }
    (context_dir / "project-context.json").write_text(
        json.dumps(tech_data, indent=2)
    )
    
    print(f"✅ Wrote MCP context to {context_dir / 'mcp-servers.md'}")
    print(f"✅ Wrote project context to {context_dir / 'project-context.json'}")