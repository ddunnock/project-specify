"""Discover command for project-specify CLI."""

from pathlib import Path
from typing import Optional

import typer

from ..ui import console


def discover(
    project_path: Optional[Path] = typer.Argument(None, help="Project directory (default: current directory)"),
    skip_mcp: bool = typer.Option(False, "--skip-mcp", help="Skip MCP server discovery"),
):
    """Discover MCP servers and generate project context."""
    from ..mcp_discovery import (
        discover_mcp_servers,
        detect_project_technology,
        generate_mcp_context,
    )

    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path).resolve()

    console.print("[cyan]Discovering MCP servers and project context...[/cyan]")

    if not skip_mcp:
        servers = discover_mcp_servers(project_path)
        console.print(f"[green]Found {len(servers)} MCP server(s)[/green]")
        for server in servers:
            console.print(f"  • {server.name} ({server.source})")
    else:
        servers = []

    tech = detect_project_technology(project_path)
    console.print(f"\n[cyan]Project Technology:[/cyan]")
    console.print(f"  Language: {tech.primary_language}")
    if tech.framework:
        console.print(f"  Framework: {tech.framework}")
    if tech.package_manager:
        console.print(f"  Package Manager: {tech.package_manager}")
    if tech.database:
        console.print(f"  Database: {tech.database}")
    if tech.monorepo_type:
        console.print(f"  Monorepo: {tech.monorepo_type}")

    generate_mcp_context(project_path, servers, tech)
    console.print(f"\n[green]Context files generated in .specify/context/[/green]")
