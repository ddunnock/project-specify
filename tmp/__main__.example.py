"""
Example Typer-based main.py modifications for project-specify

This shows the key changes needed to support multiple --ai arguments in Typer.
Typer handles List[str] options by accepting the flag multiple times:
    project-specify . --ai claude --ai cursor --ai copilot

Or you can use a callback to support comma/space-separated in a single flag:
    project-specify . --ai "claude cursor copilot"
    project-specify . --ai "claude,cursor,copilot"

Apply these changes to src/specify_cli/main.py in your fork.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from .symlink_manager import (
    parse_ai_argument,
    ensure_central_installation,
    create_agent_symlinks,
    print_symlink_status,
    SUPPORTED_AGENTS,
)

app = typer.Typer(
    name="project-specify",
    help="Project planning toolkit with spec-driven development for all AI IDEs",
    no_args_is_help=True,
)
console = Console()


def parse_ai_callback(value: List[str]) -> List[str]:
    """
    Callback to parse --ai values, supporting multiple formats:
    - Multiple flags: --ai claude --ai cursor
    - Comma-separated: --ai claude,cursor,copilot
    - Space-separated in quotes: --ai "claude cursor copilot"
    - Mixed: --ai claude,cursor --ai copilot
    - All agents: --ai all
    """
    if not value:
        return ["claude"]  # Default
    
    return parse_ai_argument(value)


@app.command()
def init(
    project_name: Optional[str] = typer.Argument(
        None,
        help="Project directory name. Use '.' for current directory.",
    ),
    ai: List[str] = typer.Option(
        ["claude"],
        "--ai",
        help=(
            "AI agents to set up. Can be specified multiple times (--ai claude --ai cursor), "
            "comma-separated (--ai claude,cursor), or use 'all' for all agents. "
            f"Available: {', '.join(sorted(SUPPORTED_AGENTS))}"
        ),
        callback=parse_ai_callback,
    ),
    here: bool = typer.Option(
        False,
        "--here",
        help="Initialize in current directory instead of creating new one",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force overwrite existing files and symlinks",
    ),
    no_git: bool = typer.Option(
        False,
        "--no-git",
        help="Skip git repository initialization",
    ),
    no_mcp_discovery: bool = typer.Option(
        False,
        "--no-mcp-discovery",
        help="Skip MCP server and project technology discovery",
    ),
    script: str = typer.Option(
        "sh",
        "--script",
        help="Script variant to use: 'sh' (bash/zsh) or 'ps' (PowerShell)",
    ),
    ignore_agent_tools: bool = typer.Option(
        False,
        "--ignore-agent-tools",
        help="Skip checks for AI agent tools like Claude Code",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable detailed debug output",
    ),
):
    """
    Initialize a new project-specify project.
    
    Examples:
        # Single agent (default is claude)
        project-specify init my-project
        
        # Multiple agents
        project-specify init my-project --ai claude --ai cursor --ai copilot
        
        # Comma-separated
        project-specify init my-project --ai claude,cursor,copilot
        
        # All agents
        project-specify init my-project --ai all
        
        # Current directory
        project-specify init . --ai all
        project-specify init --here --ai all
        
        # Skip MCP discovery (faster init)
        project-specify init . --ai claude --no-mcp-discovery
    """
    # Determine project directory
    if here or project_name == ".":
        project_dir = Path.cwd()
    elif project_name:
        project_dir = Path.cwd() / project_name
    else:
        console.print("[red]Error:[/red] Specify a project name or use --here")
        raise typer.Exit(1)
    
    # ai is already parsed by callback
    agents = ai
    
    console.print(f"\n[bold]Initializing project-specify[/bold]")
    console.print(f"  Directory: {project_dir}")
    console.print(f"  Agents: {', '.join(agents)}")
    console.print()
    
    # Ensure central installation exists
    updated = ensure_central_installation()
    if updated:
        console.print("[green]✓[/green] Updated central installation (~/.project-specify)")
    
    # Create project directory if needed
    if not project_dir.exists():
        project_dir.mkdir(parents=True)
        console.print(f"[green]✓[/green] Created directory: {project_dir}")
    
    # Create .specify directory structure (NOT symlinked - project-specific)
    _create_specify_structure(project_dir, debug=debug)
    console.print("[green]✓[/green] Created .specify/ structure")
    
    # Create agent symlinks
    console.print("\n[bold]Creating agent symlinks:[/bold]")
    results = create_agent_symlinks(project_dir, agents, force=force, verbose=True)
    
    # Run MCP and project discovery
    if not no_mcp_discovery:
        _run_mcp_discovery(project_dir, debug=debug)
    
    # Summary
    success_count = sum(1 for v in results.values() if v)
    console.print(f"\n{'─' * 40}")
    console.print(f"[bold green]✓[/bold green] Initialized {success_count}/{len(agents)} agents")
    
    # Git initialization
    if not no_git:
        if not (project_dir / ".git").exists():
            _init_git(project_dir)
            console.print("[green]✓[/green] Initialized git repository")
        else:
            console.print("[dim]ℹ[/dim] Git repository already exists")
    
    # Check if MCP context was created
    mcp_context = project_dir / ".specify" / "context" / "mcp-servers.md"
    if mcp_context.exists():
        console.print("[green]✓[/green] Generated MCP and project context")
    
    console.print(f"\n[bold]Next steps:[/bold]")
    console.print(f"  1. cd {project_dir}")
    console.print(f"  2. Open in your AI IDE (Claude Code, Cursor, etc.)")
    console.print(f"  3. Use /speckit.constitution to establish principles")
    console.print(f"  4. Use /speckit.specify to create your project spec")


@app.command()
def check():
    """Check for installed AI coding tools and dependencies."""
    import shutil
    
    console.print("\n[bold]Checking installed tools:[/bold]\n")
    
    tools = [
        ("git", "Git version control"),
        ("claude", "Claude Code CLI"),
        ("cursor", "Cursor IDE CLI"),
        ("code", "VS Code CLI"),
        ("windsurf", "Windsurf IDE"),
        ("gemini", "Gemini CLI"),
        ("python", "Python runtime"),
        ("uv", "uv package manager"),
    ]
    
    for tool, description in tools:
        found = shutil.which(tool) is not None
        status = "[green]✓[/green]" if found else "[red]✗[/red]"
        console.print(f"  {status} {tool}: {description}")
    
    console.print()


@app.command()
def status(
    ai: Optional[List[str]] = typer.Option(
        None,
        "--ai",
        help="Specific agents to check (default: all configured)",
    ),
):
    """Show symlink status for the current project."""
    project_dir = Path.cwd()
    
    if not (project_dir / ".specify").exists():
        console.print("[yellow]Warning:[/yellow] No .specify/ directory found.")
        console.print("Run 'project-specify init' to initialize this project.")
        raise typer.Exit(1)
    
    agents_to_check = ai if ai else None  # None means check all
    print_symlink_status(project_dir, agents_to_check)


@app.command()
def update():
    """Update the central installation with latest commands."""
    console.print("[bold]Updating central installation...[/bold]")
    
    updated = ensure_central_installation(force_update=True)
    
    if updated:
        console.print("[green]✓[/green] Central installation updated")
    else:
        console.print("[dim]ℹ[/dim] Already up to date")


@app.command()
def discover(
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable detailed debug output",
    ),
):
    """
    Run MCP server and project technology discovery.
    
    This detects available MCP servers and analyzes the project's technology
    stack, then generates context files that AI agent commands can reference.
    
    Output files:
        .specify/context/mcp-servers.md     - Human-readable MCP context
        .specify/context/project-context.json - Machine-readable context
    
    Run this command:
        - After configuring new MCP servers
        - When the project's tech stack changes
        - To refresh context for AI agents
    """
    project_dir = Path.cwd()
    
    # Check if .specify exists
    if not (project_dir / ".specify").exists():
        console.print("[yellow]Warning:[/yellow] No .specify/ directory found.")
        console.print("Run 'project-specify init' first, or create .specify/ manually.")
        
        create_anyway = typer.confirm("Create .specify/context/ anyway?")
        if not create_anyway:
            raise typer.Exit(1)
        
        (project_dir / ".specify" / "context").mkdir(parents=True, exist_ok=True)
    
    _run_mcp_discovery(project_dir, debug=debug)
    
    # Show summary of what was discovered
    context_file = project_dir / ".specify" / "context" / "project-context.json"
    if context_file.exists():
        import json
        try:
            context = json.loads(context_file.read_text())
            
            console.print("\n[bold]Discovered Context:[/bold]")
            console.print(f"  Language: {context.get('primary_language', 'unknown')}")
            
            if context.get('framework'):
                console.print(f"  Framework: {context['framework']}")
            if context.get('database'):
                console.print(f"  Database: {context['database']}")
            if context.get('mcp_servers'):
                console.print(f"  MCP Servers: {', '.join(context['mcp_servers'])}")
            if context.get('detected_services'):
                services = [s for s in context['detected_services'] if s]
                if services:
                    console.print(f"  Services: {', '.join(services)}")
        except Exception as e:
            if debug:
                console.print(f"[dim]Could not parse context: {e}[/dim]")
    
    console.print("\n[bold]Commands can now reference:[/bold]")
    console.print("  .specify/context/mcp-servers.md")
    console.print("  .specify/context/project-context.json")


def _create_specify_structure(project_dir: Path, debug: bool = False) -> None:
    """Create the .specify directory structure (not symlinked)."""
    specify_dir = project_dir / ".specify"
    
    # Create directories
    dirs = ["memory", "scripts", "specs", "templates", "scans", "context"]
    for d in dirs:
        (specify_dir / d).mkdir(parents=True, exist_ok=True)
    
    # TODO: Copy templates and scripts from package resources
    # This is where you'd copy the non-symlinked project files
    # from importlib.resources or pkg_resources
    
    if debug:
        console.print(f"[dim]Created: {specify_dir}[/dim]")


def _run_mcp_discovery(project_dir: Path, debug: bool = False) -> None:
    """
    Run MCP server and project technology discovery.
    
    This detects:
    1. Available MCP servers from Claude Desktop, Claude Code, Cursor configs
    2. Project technology stack (language, framework, database, etc.)
    3. Generates context files that commands can reference
    """
    try:
        from .mcp_discovery import write_context_files
        
        console.print("\n[bold]Discovering MCP servers and project context...[/bold]")
        write_context_files(project_dir)
        
    except ImportError:
        # Fall back to shell script if Python module not available
        import subprocess
        
        script_path = Path(__file__).parent / "scripts" / "discover-mcp.sh"
        if script_path.exists():
            console.print("\n[bold]Discovering MCP servers and project context...[/bold]")
            result = subprocess.run(
                ["bash", str(script_path), str(project_dir)],
                capture_output=True,
                text=True,
            )
            if debug:
                console.print(f"[dim]{result.stdout}[/dim]")
            if result.returncode != 0:
                console.print(f"[yellow]Warning:[/yellow] MCP discovery failed: {result.stderr}")
        else:
            if debug:
                console.print("[dim]MCP discovery not available[/dim]")
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] MCP discovery failed: {e}")


def _init_git(project_dir: Path) -> None:
    """Initialize a git repository."""
    import subprocess
    
    result = subprocess.run(
        ["git", "init"],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    
    if result.returncode != 0:
        console.print(f"[yellow]Warning:[/yellow] git init failed: {result.stderr}")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()