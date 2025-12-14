"""
Symlink Manager for project-specify

Handles creation and management of symlinks from project directories
to the central ~/.project-specify installation.

This is the core differentiator from spec-kit: instead of copying
command files to each project, we symlink them from a central location.
This means:
1. Update commands once, all projects get the update
2. Smaller project footprint (just symlinks)
3. Consistent command versions across all projects
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Optional, TypedDict
from importlib import resources


# Central installation location
CENTRAL_DIR = Path.home() / ".project-specify"
AGENTS_DIR = CENTRAL_DIR / "agents"
VERSION_FILE = CENTRAL_DIR / "version.txt"


class AgentConfig(TypedDict, total=False):
    """Configuration for an AI agent's command structure."""
    source: str           # Relative path in AGENTS_DIR
    target: str           # Relative path in project directory
    files: list[str]      # If set, symlink specific files instead of directory


# Agent directory mappings
# Maps agent name -> how to set up symlinks
AGENT_CONFIGS: dict[str, AgentConfig] = {
    # Directory-based agents (symlink entire commands/ directory)
    "claude": {
        "source": "claude/commands",
        "target": ".claude/commands",
    },
    "cursor": {
        "source": "cursor/commands",
        "target": ".cursor/commands",
    },
    "windsurf": {
        "source": "windsurf/commands",
        "target": ".windsurf/commands",
    },
    "qwen": {
        "source": "qwen/commands",
        "target": ".qwen/commands",
    },
    "opencode": {
        "source": "opencode/commands",
        "target": ".opencode/commands",
    },
    "codex": {
        "source": "codex/commands",
        "target": ".codex/commands",
    },
    "kilocode": {
        "source": "kilocode/commands",
        "target": ".kilocode/commands",
    },
    "auggie": {
        "source": "auggie/commands",
        "target": ".auggie/commands",
    },
    "roo": {
        "source": "roo/commands",
        "target": ".roo/commands",
    },
    "codebuddy": {
        "source": "codebuddy/commands",
        "target": ".codebuddy/commands",
    },
    "amp": {
        "source": "amp/commands",
        "target": ".amp/commands",
    },
    "shai": {
        "source": "shai/commands",
        "target": ".shai/commands",
    },
    "q": {
        "source": "q/commands",
        "target": ".q/commands",
    },
    "bob": {
        "source": "bob/commands",
        "target": ".bob/commands",
    },
    "qoder": {
        "source": "qoder/commands",
        "target": ".qoder/commands",
    },
    # File-based agents (symlink specific files)
    "copilot": {
        "source": "copilot",
        "target": ".github",
        "files": ["copilot-instructions.md"],
    },
    "gemini": {
        "source": "gemini",
        "target": ".",
        "files": ["GEMINI.md"],
    },
}

# List of all supported agents (for --ai all)
SUPPORTED_AGENTS = list(AGENT_CONFIGS.keys())


def get_package_version() -> str:
    """Get the current package version."""
    try:
        from importlib.metadata import version
        return version("project-specify-cli")
    except Exception:
        return "0.0.0-dev"


def ensure_central_installation(force_update: bool = False) -> bool:
    """
    Ensure the central ~/.project-specify directory exists with current commands.
    
    This copies the bundled agent commands from the installed package to
    the user's home directory, where projects will symlink to.
    
    Args:
        force_update: If True, overwrite existing installation
        
    Returns:
        True if installation was created/updated, False if already current
    """
    current_version = get_package_version()
    
    # Check if update is needed
    if CENTRAL_DIR.exists() and not force_update:
        if VERSION_FILE.exists():
            installed_version = VERSION_FILE.read_text().strip()
            if installed_version == current_version:
                return False  # Already up to date
    
    # Create directory structure
    CENTRAL_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(exist_ok=True)
    
    # Copy agent commands from package resources
    # The agents/ directory should be included in the package
    try:
        package_agents = Path(__file__).parent / "agents"
        if package_agents.exists():
            # Remove old agents and copy new
            if AGENTS_DIR.exists():
                shutil.rmtree(AGENTS_DIR)
            shutil.copytree(package_agents, AGENTS_DIR)
    except Exception as e:
        print(f"Warning: Could not copy package agents: {e}")
        # Create empty structure if copy fails
        for agent in SUPPORTED_AGENTS:
            config = AGENT_CONFIGS[agent]
            (AGENTS_DIR / config["source"]).mkdir(parents=True, exist_ok=True)
    
    # Write version file
    VERSION_FILE.write_text(current_version)
    
    return True


def parse_ai_argument(ai_args: str | list[str]) -> list[str]:
    """
    Parse the --ai argument, supporting 'all', space-separated, and comma-separated values.
    
    Args:
        ai_args: Either a list of agent names (from nargs='*') or a single string
        
    Returns:
        List of agent names to set up
        
    Raises:
        ValueError: If unknown agents are specified
        
    Examples:
        parse_ai_argument(['claude', 'cursor', 'copilot'])  # Space-separated from CLI
        parse_ai_argument(['all'])                           # All agents
        parse_ai_argument('claude,cursor,copilot')           # Comma-separated string
        parse_ai_argument('all')                             # All agents (string)
    """
    # Handle list input (from argparse nargs='*')
    if isinstance(ai_args, list):
        # Check for 'all' keyword
        if len(ai_args) == 1 and ai_args[0].lower() == "all":
            return SUPPORTED_AGENTS.copy()
        
        # Flatten any comma-separated values within the list
        agents = []
        for arg in ai_args:
            agents.extend(a.strip().lower() for a in arg.split(","))
    else:
        # Handle string input (backwards compatibility)
        if ai_args.lower() == "all":
            return SUPPORTED_AGENTS.copy()
        agents = [a.strip().lower() for a in ai_args.split(",")]
    
    # Remove empty strings and duplicates while preserving order
    seen = set()
    unique_agents = []
    for a in agents:
        if a and a not in seen:
            seen.add(a)
            unique_agents.append(a)
    agents = unique_agents
    
    # Validate agents
    invalid = [a for a in agents if a not in SUPPORTED_AGENTS]
    if invalid:
        raise ValueError(
            f"Unknown agent(s): {', '.join(invalid)}\n"
            f"Supported agents: {', '.join(sorted(SUPPORTED_AGENTS))}"
        )
    
    if not agents:
        raise ValueError("No agents specified. Use --ai followed by agent names or 'all'")
    
    return agents


def create_agent_symlinks(
    project_dir: Path,
    agents: list[str],
    force: bool = False,
    verbose: bool = True,
) -> dict[str, bool]:
    """
    Create symlinks from project directory to central installation.
    
    Args:
        project_dir: The project directory to set up
        agents: List of agent names to create symlinks for
        force: If True, overwrite existing files/symlinks
        verbose: If True, print status messages
        
    Returns:
        Dict mapping agent name to success status
    """
    results = {}
    
    for agent in agents:
        if agent not in AGENT_CONFIGS:
            if verbose:
                print(f"  ⚠️  Unknown agent: {agent}")
            results[agent] = False
            continue
            
        config = AGENT_CONFIGS[agent]
        source = AGENTS_DIR / config["source"]
        target = project_dir / config["target"]
        
        if not source.exists():
            if verbose:
                print(f"  ⚠️  Source not found for {agent}: {source}")
            results[agent] = False
            continue
        
        # Handle file-specific symlinks vs directory symlinks
        if "files" in config:
            # Symlink specific files
            target.mkdir(parents=True, exist_ok=True)
            all_success = True
            for filename in config["files"]:
                src_file = source / filename
                tgt_file = target / filename
                if src_file.exists():
                    success = _create_symlink(src_file, tgt_file, force, verbose)
                    all_success = all_success and success
                else:
                    if verbose:
                        print(f"  ⚠️  Source file not found: {src_file}")
                    all_success = False
            results[agent] = all_success
        else:
            # Symlink entire directory
            target.parent.mkdir(parents=True, exist_ok=True)
            results[agent] = _create_symlink(source, target, force, verbose)
    
    return results


def _create_symlink(source: Path, target: Path, force: bool, verbose: bool) -> bool:
    """
    Create a single symlink, handling existing files.
    
    Args:
        source: The symlink target (what it points to)
        target: The symlink location (where it lives)
        force: If True, overwrite existing
        verbose: If True, print messages
        
    Returns:
        True if symlink was created successfully
    """
    try:
        # Check if target already exists
        if target.exists() or target.is_symlink():
            if target.is_symlink():
                # Check if it already points to the right place
                if target.resolve() == source.resolve():
                    if verbose:
                        print(f"  ✓ {target} (already linked)")
                    return True
            
            if force:
                if target.is_dir() and not target.is_symlink():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            else:
                if verbose:
                    print(f"  ⚠️  {target} exists (use --force to overwrite)")
                return False
        
        # Create the symlink
        # On Windows, we might need special handling
        if platform.system() == "Windows":
            success = _create_windows_symlink(source, target, verbose)
        else:
            target.symlink_to(source)
            success = True
        
        if success and verbose:
            print(f"  ✅ {target} -> {source}")
        
        return success
        
    except OSError as e:
        if verbose:
            print(f"  ❌ Error creating {target}: {e}")
        return False


def _create_windows_symlink(source: Path, target: Path, verbose: bool) -> bool:
    """
    Create symlink on Windows, handling potential permission issues.
    
    Windows symlinks require either:
    1. Administrator privileges
    2. Developer Mode enabled
    3. SeCreateSymbolicLinkPrivilege
    
    Falls back to junction points for directories if symlinks fail.
    """
    try:
        # Try regular symlink first
        target.symlink_to(source, target_is_directory=source.is_dir())
        return True
    except OSError:
        pass
    
    # For directories, try junction point as fallback
    if source.is_dir():
        try:
            # Junction points don't require special privileges
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(target), str(source)],
                check=True,
                capture_output=True,
            )
            if verbose:
                print(f"  ℹ️  Created junction point (symlinks require admin on Windows)")
            return True
        except subprocess.CalledProcessError:
            pass
    
    if verbose:
        print(f"  ❌ Windows symlink failed. Try running as Administrator or enable Developer Mode.")
    return False


def verify_symlinks(project_dir: Path, agents: list[str]) -> dict[str, str]:
    """
    Verify symlink status for agents in a project.
    
    Args:
        project_dir: The project directory to check
        agents: List of agent names to verify
        
    Returns:
        Dict mapping agent to status:
        - "valid": Symlink exists and points to valid target
        - "broken": Symlink exists but target is missing
        - "missing": No symlink or file exists
        - "file": Regular file/directory exists (not symlinked)
        - "unknown": Agent not in configuration
    """
    status = {}
    
    for agent in agents:
        if agent not in AGENT_CONFIGS:
            status[agent] = "unknown"
            continue
            
        config = AGENT_CONFIGS[agent]
        target = project_dir / config["target"]
        
        # For file-based agents, check the first file
        if "files" in config:
            target = target / config["files"][0]
        
        if not target.exists() and not target.is_symlink():
            status[agent] = "missing"
        elif target.is_symlink():
            if target.resolve().exists():
                status[agent] = "valid"
            else:
                status[agent] = "broken"
        else:
            status[agent] = "file"  # Regular file, not symlink
    
    return status


def print_symlink_status(project_dir: Path, agents: Optional[list[str]] = None) -> None:
    """
    Print a formatted status report of symlinks in a project.
    
    Args:
        project_dir: The project directory to check
        agents: Specific agents to check (default: all)
    """
    if agents is None:
        agents = SUPPORTED_AGENTS
    
    status = verify_symlinks(project_dir, agents)
    
    icons = {
        "valid": "✅",
        "broken": "🔗❌",
        "missing": "⬜",
        "file": "📄",
        "unknown": "❓",
    }
    
    print("\nAgent Symlink Status:")
    print("-" * 40)
    
    for agent, state in sorted(status.items()):
        icon = icons.get(state, "?")
        print(f"  {icon} {agent}: {state}")
    
    print("-" * 40)
    
    # Summary
    valid_count = sum(1 for s in status.values() if s == "valid")
    print(f"  {valid_count}/{len(agents)} agents linked")


def get_central_dir() -> Path:
    """Return the central installation directory path."""
    return CENTRAL_DIR


def get_agents_dir() -> Path:
    """Return the agents directory path."""
    return AGENTS_DIR


def is_central_installed() -> bool:
    """Check if the central installation exists."""
    return CENTRAL_DIR.exists() and AGENTS_DIR.exists()


def uninstall_central() -> bool:
    """
    Remove the central installation.
    
    Returns:
        True if successfully removed, False otherwise
    """
    try:
        if CENTRAL_DIR.exists():
            shutil.rmtree(CENTRAL_DIR)
        return True
    except Exception as e:
        print(f"Error removing central installation: {e}")
        return False