"""Init command for project-specify CLI."""

import os
import shutil
import shlex
import sys
from pathlib import Path
from typing import Optional, List, Set
from dataclasses import dataclass, field

import typer
from rich.panel import Panel
from rich.live import Live

from ..config import AGENT_CONFIG, SCRIPT_TYPE_CHOICES
from ..ui import console, StepTracker, show_banner, select_with_arrows
from ..system_tools import check_tool
from ..git_operations import is_git_repo, init_git_repo
from ..template_download import ensure_executable_scripts
from ..errors import SymlinkError, GitOperationError, MCPDiscoveryError


@dataclass
class InitializationState:
    """Track created resources for rollback on failure."""
    created_directories: Set[Path] = field(default_factory=set)
    created_symlinks: Set[Path] = field(default_factory=set)
    created_git_repo: bool = False
    project_path: Optional[Path] = None
    was_empty_directory: bool = True

    def track_directory(self, path: Path) -> None:
        """Track a directory that was created."""
        if path.exists():
            self.created_directories.add(path)

    def track_symlink(self, path: Path) -> None:
        """Track a symlink that was created."""
        if path.exists() or path.is_symlink():
            self.created_symlinks.add(path)

    def rollback(self, console_obj, verbose: bool = True) -> None:
        """Rollback all created resources on failure."""
        if verbose:
            console_obj.print("\n[yellow]Rolling back changes...[/yellow]")

        # Remove symlinks first
        for symlink in self.created_symlinks:
            try:
                if symlink.exists() or symlink.is_symlink():
                    symlink.unlink()
                    if verbose:
                        console_obj.print(f"  [dim]Removed symlink: {symlink}[/dim]")
            except Exception as e:
                if verbose:
                    console_obj.print(f"  [yellow]Warning: Could not remove {symlink}: {e}[/yellow]")

        # Remove created directories (in reverse order)
        for directory in sorted(self.created_directories, reverse=True):
            try:
                if directory.exists():
                    shutil.rmtree(directory)
                    if verbose:
                        console_obj.print(f"  [dim]Removed directory: {directory}[/dim]")
            except Exception as e:
                if verbose:
                    console_obj.print(f"  [yellow]Warning: Could not remove {directory}: {e}[/yellow]")

        # Remove project directory if it was empty and we created it
        if self.project_path and self.was_empty_directory and self.project_path.exists():
            try:
                shutil.rmtree(self.project_path)
                if verbose:
                    console_obj.print(f"  [dim]Removed project directory: {self.project_path}[/dim]")
            except Exception as e:
                if verbose:
                    console_obj.print(f"  [yellow]Warning: Could not remove {self.project_path}: {e}[/yellow]")

        if verbose:
            console_obj.print("[yellow]Rollback complete[/yellow]\n")


def parse_ai_callback(value: List[str]) -> List[str]:
    """
    Callback to parse --ai values, supporting multiple formats:
    - Multiple flags: --ai claude --ai cursor
    - Comma-separated: --ai claude,cursor,copilot
    - All agents: --ai all
    """
    if not value:
        return ["claude"]  # Default
    from ..symlink_manager import parse_ai_argument
    return parse_ai_argument(value)


def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ai_assistant: List[str] = typer.Option(
        None,
        "--ai",
        help="AI agents to set up. Use multiple times, 'all', or comma-separated.",
        callback=parse_ai_callback,
    ),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
    workspace: Optional[str] = typer.Option(None, "--workspace", help="Initialize in a specific workspace package (for monorepos)"),
    no_mcp_discovery: bool = typer.Option(False, "--no-mcp-discovery", help="Skip MCP server discovery during initialization"),
    copy: bool = typer.Option(False, "--copy", help="Copy command files instead of creating symlinks (useful on Windows without Developer Mode)"),
):
    """
    Initialize a new project-specify project with symlinked commands.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant(s) or use --ai all
    3. Set up central installation at ~/.project-specify
    4. Create symlinks (or copies with --copy) to agent commands in project directory
    5. Initialize .specify/ directory structure (project-specific)
    6. Initialize a fresh git repository (if not --no-git and no existing repo)

    Examples:
        project-specify init my-project
        project-specify init my-project --ai claude
        project-specify init my-project --ai claude --ai cursor --ai copilot
        project-specify init my-project --ai claude,cursor,copilot
        project-specify init my-project --ai all
        project-specify init . --ai all         # Initialize in current directory
        project-specify init .                  # Initialize in current directory (interactive AI selection)
        project-specify init --here --ai all    # Alternative syntax for current directory
        project-specify init --here --force     # Skip confirmation when current directory not empty
        project-specify init my-project --ai claude --copy  # Copy files instead of symlinks (Windows without Dev Mode)
    """

    show_banner()

    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)

    # Handle monorepo workspace detection
    from ..monorepo import detect_monorepo_type, get_workspace_packages

    monorepo_type = detect_monorepo_type(Path.cwd())
    workspace_path = None

    if workspace:
        if not monorepo_type:
            console.print("[yellow]Warning:[/yellow] --workspace specified but no monorepo detected")
        else:
            packages = get_workspace_packages(Path.cwd(), monorepo_type)
            # Find matching workspace
            matching = [p for p in packages if workspace in str(p) or p.name == workspace]
            if matching:
                workspace_path = matching[0]
                console.print(f"[cyan]Monorepo detected:[/cyan] {monorepo_type}")
                console.print(f"[cyan]Workspace:[/cyan] {workspace_path}")
            else:
                console.print(f"[yellow]Warning:[/yellow] Workspace '{workspace}' not found in monorepo")

    if here:
        project_name = Path.cwd().name
        if workspace_path:
            project_path = workspace_path
        else:
            project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
            else:
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        if workspace_path:
            project_path = workspace_path
        else:
            project_path = Path(project_name).resolve()
        if project_path.exists() and not workspace_path:
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Specify Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # Parse agents list
    if ai_assistant:
        # ai_assistant is already parsed by callback
        selected_agents = ai_assistant
    else:
        # Create options dict for selection (agent_key: display_name)
        ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
        selected_key = select_with_arrows(
            ai_choices,
            "Choose your AI assistant:",
            "copilot"
        )
        selected_agents = [selected_key]

    # Validate all agents
    invalid_agents = [a for a in selected_agents if a not in AGENT_CONFIG]
    if invalid_agents:
        console.print(f"[red]Error:[/red] Invalid AI assistant(s): {', '.join(invalid_agents)}. Choose from: {', '.join(AGENT_CONFIG.keys())}")
        raise typer.Exit(1)

    # Check CLI tools for agents that require them
    if not ignore_agent_tools:
        missing_tools = []
        for agent_key in selected_agents:
            agent_config = AGENT_CONFIG.get(agent_key)
            if agent_config and agent_config["requires_cli"]:
                install_url = agent_config["install_url"]
                if not check_tool(agent_key):
                    missing_tools.append((agent_key, agent_config["name"], install_url))

        if missing_tools:
            error_lines = []
            for agent_key, agent_name, install_url in missing_tools:
                error_lines.append(f"[cyan]{agent_key}[/cyan] ({agent_name}) not found")
                error_lines.append(f"  Install from: [cyan]{install_url}[/cyan]")
                error_lines.append("")

            error_lines.append("Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check")

            error_panel = Panel(
                "\n".join(error_lines),
                title="[red]Agent Detection Error[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    # Script type is no longer needed for symlink architecture
    # Keep for backward compatibility but don't use it
    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[yellow]Warning:[/yellow] Script type '{script_type}' ignored (not used with symlink architecture)")

    if len(selected_agents) == 1:
        console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_agents[0]}")
    else:
        console.print(f"[cyan]Selected AI assistants:[/cyan] {', '.join(selected_agents)}")

    # Initialize state tracking for rollback
    state = InitializationState(
        project_path=project_path,
        was_empty_directory=(here and not existing_items) or not here
    )

    tracker = StepTracker("Initialize Specify Project")

    sys._specify_tracker_active = True

    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant(s)")
    if len(selected_agents) == 1:
        tracker.complete("ai-select", f"{selected_agents[0]}")
    else:
        tracker.complete("ai-select", f"{len(selected_agents)} agents")
    for key, label in [
        ("central-install", "Set up central installation"),
        ("symlinks", "Create agent symlinks"),
        ("specify-dir", "Create .specify directory"),
        ("chmod", "Ensure scripts executable"),
        ("git", "Initialize git repository"),
        ("final", "Finalize")
    ]:
        tracker.add(key, label)

    # Track git error message outside Live context so it persists
    git_error_message = None

    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            # Import symlink manager
            from ..symlink_manager import (
                ensure_central_installation,
                create_agent_symlinks,
            )

            # Set up central installation
            tracker.start("central-install")
            ensure_central_installation(force_update=False)
            tracker.complete("central-install", "~/.project-specify ready")

            # Create agent symlinks (or copies if --copy flag used)
            tracker.start("symlinks")
            symlink_results = create_agent_symlinks(
                project_path,
                selected_agents,
                force=force,
                verbose=False,
                use_copy=copy
            )

            # Track created symlinks for rollback
            for agent_key in selected_agents:
                agent_config = AGENT_CONFIG.get(agent_key)
                if agent_config and symlink_results.get(agent_key):
                    # Track the symlink/directory for this agent
                    agent_path = project_path / agent_config["folder"]
                    if agent_path.exists() or agent_path.is_symlink():
                        state.track_symlink(agent_path)

            successful = [agent for agent, success in symlink_results.items() if success]
            failed = [agent for agent, success in symlink_results.items() if not success]
            if failed:
                error_msg = f"{len(successful)}/{len(selected_agents)} created"
                tracker.error("symlinks", error_msg)
                if failed:
                    raise SymlinkError(
                        f"Failed to create symlinks for: {', '.join(failed)}. "
                        f"Check permissions and ensure Developer Mode is enabled on Windows."
                    )
            else:
                tracker.complete("symlinks", f"{len(successful)} agent(s) linked")

            # Create .specify directory structure (project-specific, not symlinked)
            tracker.start("specify-dir")
            specify_dir = project_path / ".specify"

            # Track if .specify didn't exist before
            created_specify = not specify_dir.exists()
            specify_dir.mkdir(exist_ok=True)
            if created_specify:
                state.track_directory(specify_dir)

            # Create subdirectories and track them
            for subdir_name in ["memory", "specs", "scripts", "templates", "context"]:
                subdir = specify_dir / subdir_name
                created_subdir = not subdir.exists()
                subdir.mkdir(exist_ok=True)
                if created_subdir:
                    state.track_directory(subdir)

            # Copy scripts from package (these are project-specific)
            # TODO: In Phase 2, we'll copy scripts from package resources
            # For now, just create the structure

            tracker.complete("specify-dir", "project structure created")

            # MCP discovery (optional)
            if not no_mcp_discovery:
                try:
                    from ..mcp_discovery import (
                        discover_mcp_servers,
                        detect_project_technology,
                        generate_mcp_context,
                    )

                    tracker.add("mcp-discovery", "Discover MCP servers")
                    tracker.start("mcp-discovery")

                    servers = discover_mcp_servers(project_path)
                    tech = detect_project_technology(project_path)
                    generate_mcp_context(project_path, servers, tech)

                    tracker.complete("mcp-discovery", f"{len(servers)} server(s) found")
                except MCPDiscoveryError as e:
                    # MCP errors are non-fatal during init
                    tracker.skip("mcp-discovery", f"error: {str(e)[:50]}")
                except Exception as e:
                    tracker.skip("mcp-discovery", f"skipped: {e}")

            ensure_executable_scripts(project_path, tracker=tracker)

            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    success, error_msg = init_git_repo(project_path, quiet=True)
                    if success:
                        state.created_git_repo = True
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                        # Git errors are non-fatal, store for later display
                        git_error_message = error_msg
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except SymlinkError as e:
            tracker.error("final", "symlink creation failed")
            error_msg = str(e)

            # Check if we're on Windows to provide platform-specific guidance
            import platform
            if platform.system() == "Windows":
                recovery_msg = (
                    "\n[bold yellow]Windows Symlink Support Required[/bold yellow]\n\n"
                    "[bold]Option 1 (Recommended):[/bold] Enable Developer Mode\n"
                    "  1. Open Settings → Privacy & Security → For developers\n"
                    "  2. Enable 'Developer Mode'\n"
                    "  3. Run this command again\n\n"
                    "[bold]Option 2:[/bold] Use --copy flag (copies files instead of symlinks)\n"
                    f"  project-specify init {project_name or '.'} --ai {','.join(selected_agents)} --copy\n"
                    "  Note: Copies use more disk space and won't auto-update\n\n"
                    "[bold]Option 3:[/bold] Run as Administrator (not recommended for daily use)\n"
                    "  Right-click Terminal → Run as Administrator\n"
                )
            else:
                recovery_msg = (
                    "\n[bold]Recovery Options:[/bold]\n"
                    "1. Check file permissions and try again\n"
                    "2. Use --copy flag to copy files instead of symlinking\n"
                    f"   project-specify init {project_name or '.'} --ai {','.join(selected_agents)} --copy"
                )

            console.print(Panel(
                f"{error_msg}{recovery_msg}",
                title="[red]Symlink Error[/red]",
                border_style="red"
            ))
            state.rollback(console, verbose=debug)
            raise typer.Exit(1)
        except GitOperationError as e:
            tracker.error("final", "git initialization failed")
            console.print(Panel(
                f"{str(e)}\n\n[bold]Recovery:[/bold]\nYou can initialize git manually later with:\n"
                f"  cd {project_path if not here else '.'}\n"
                f"  git init && git add . && git commit -m 'Initial commit'",
                title="[red]Git Error[/red]",
                border_style="red"
            ))
            state.rollback(console, verbose=debug)
            raise typer.Exit(1)
        except Exception as e:
            tracker.error("final", str(e))
            error_type = type(e).__name__
            console.print(Panel(
                f"[bold]{error_type}:[/bold] {e}\n\n"
                "[bold]The initialization has been rolled back.[/bold]\n"
                "Check the error message above for details.",
                title="[red]Initialization Failed[/red]",
                border_style="red"
            ))
            if debug:
                import traceback
                console.print("\n[bold]Stack Trace:[/bold]")
                console.print(traceback.format_exc())
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))

            # Perform rollback
            state.rollback(console, verbose=debug)
            raise typer.Exit(1)
        finally:
            pass

    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")

    # Show git error details if initialization failed
    if git_error_message:
        console.print()
        git_error_panel = Panel(
            f"[yellow]Warning:[/yellow] Git repository initialization failed\n\n"
            f"{git_error_message}\n\n"
            f"[dim]You can initialize git manually later with:[/dim]\n"
            f"[cyan]cd {project_path if not here else '.'}[/cyan]\n"
            f"[cyan]git init[/cyan]\n"
            f"[cyan]git add .[/cyan]\n"
            f"[cyan]git commit -m \"Initial commit\"[/cyan]",
            title="[red]Git Initialization Failed[/red]",
            border_style="red",
            padding=(1, 2)
        )
        console.print(git_error_panel)

    # Agent folder security notice
    agent_folders = set()
    for agent_key in selected_agents:
        agent_config = AGENT_CONFIG.get(agent_key)
        if agent_config:
            agent_folders.add(agent_config["folder"])

    if agent_folders:
        folders_list = ", ".join([f"[cyan]{f}[/cyan]" for f in sorted(agent_folders)])
        security_notice = Panel(
            f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
            f"Consider adding {folders_list} (or parts of them) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
            title="[yellow]Agent Folder Security[/yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print()
        console.print(security_notice)

    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    # Add Codex-specific setup step if needed
    if "codex" in selected_agents:
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"

        steps_lines.append(f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]")
        step_num += 1

    steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")

    steps_lines.append("   2.1 [cyan]/speckit.constitution[/] - Establish project principles")
    steps_lines.append("   2.2 [cyan]/speckit.specify[/] - Create baseline specification")
    steps_lines.append("   2.3 [cyan]/speckit.plan[/] - Create implementation plan")
    steps_lines.append("   2.4 [cyan]/speckit.tasks[/] - Generate actionable tasks")
    steps_lines.append("   2.5 [cyan]/speckit.implement[/] - Execute implementation")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

    enhancement_lines = [
        "Optional commands that you can use for your specs [bright_black](improve quality & confidence)[/bright_black]",
        "",
        f"○ [cyan]/speckit.clarify[/] [bright_black](optional)[/bright_black] - Ask structured questions to de-risk ambiguous areas before planning (run before [cyan]/speckit.plan[/] if used)",
        f"○ [cyan]/speckit.analyze[/] [bright_black](optional)[/bright_black] - Cross-artifact consistency & alignment report (after [cyan]/speckit.tasks[/], before [cyan]/speckit.implement[/])",
        f"○ [cyan]/speckit.checklist[/] [bright_black](optional)[/bright_black] - Generate quality checklists to validate requirements completeness, clarity, and consistency (after [cyan]/speckit.plan[/])"
    ]
    enhancements_panel = Panel("\n".join(enhancement_lines), title="Enhancement Commands", border_style="cyan", padding=(1,2))
    console.print()
    console.print(enhancements_panel)
