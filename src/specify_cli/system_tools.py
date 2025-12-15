"""System utilities for running commands and checking tools."""

import subprocess
import shutil
from typing import Optional
from pathlib import Path

from .config import CLAUDE_LOCAL_PATH


def run_command(
    cmd: list[str],
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False
) -> Optional[str]:
    """Run a shell command and optionally capture output.

    Args:
        cmd: Command and arguments as list of strings.
        check_return: Whether to check return code and raise on error.
        capture: Whether to capture and return stdout.
        shell: Whether to run command through shell.

    Returns:
        Captured stdout if capture=True, otherwise None.

    Raises:
        subprocess.CalledProcessError: If command fails and check_return=True.
    """
    from .ui import console  # Import here to avoid circular dependency

    try:
        if capture:
            result = subprocess.run(
                cmd,
                check=check_return,
                capture_output=True,
                text=True,
                shell=shell
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def check_tool(tool: str, tracker=None) -> bool:
    """Check if a tool is installed. Optionally update tracker.

    Args:
        tool: Name of the tool to check.
        tracker: Optional StepTracker to update with results.

    Returns:
        True if tool is found, False otherwise.
    """
    # Special handling for Claude CLI after `claude migrate-installer`
    # See: https://github.com/github/spec-kit/issues/123
    # The migrate-installer command REMOVES the original executable from PATH
    # and creates an alias at ~/.claude/local/claude instead
    # This path should be prioritized over other claude executables in PATH
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            if tracker:
                tracker.complete(tool, "available")
            return True

    found = shutil.which(tool) is not None

    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")

    return found
