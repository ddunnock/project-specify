"""
Monorepo detection and workspace support for project-specify.
"""

from pathlib import Path
from typing import Optional
import json
import glob

from .errors import MonorepoError


def detect_monorepo_type(project_dir: Path) -> Optional[str]:
    """
    Detect the type of monorepo structure.
    
    Returns: "pnpm", "npm", "yarn", "lerna", "nx", "turborepo", "cargo", or None
    """
    indicators = {
        "pnpm-workspace.yaml": "pnpm",
        "pnpm-workspace.yml": "pnpm",
        "lerna.json": "lerna",
        "nx.json": "nx",
        "turbo.json": "turborepo",
    }
    
    for filename, monorepo_type in indicators.items():
        if (project_dir / filename).exists():
            return monorepo_type
    
    # Check package.json for workspaces
    package_json = project_dir / "package.json"
    if package_json.exists():
        try:
            with open(package_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "workspaces" in data:
                return "npm"  # or yarn, they use same format
        except json.JSONDecodeError as e:
            # Invalid JSON in package.json - log but don't fail
            import logging
            logging.debug(f"Invalid JSON in package.json: {e}")
        except Exception as e:
            # Other errors reading package.json
            import logging
            logging.debug(f"Error reading package.json: {e}")
    
    # Check Cargo.toml for Rust workspaces
    cargo_toml = project_dir / "Cargo.toml"
    if cargo_toml.exists():
        try:
            # Simple check for [workspace] section
            content = cargo_toml.read_text(encoding="utf-8")
            if "[workspace]" in content:
                return "cargo"
        except (FileNotFoundError, UnicodeDecodeError) as e:
            # Cargo.toml unreadable - log but don't fail
            import logging
            logging.debug(f"Error reading Cargo.toml: {e}")
    
    return None


def get_workspace_packages(project_dir: Path, monorepo_type: str) -> list[Path]:
    """
    Get list of workspace package directories.
    """
    packages = []
    
    if monorepo_type == "pnpm":
        packages = _get_pnpm_workspaces(project_dir)
    elif monorepo_type in ("npm", "yarn"):
        packages = _get_npm_workspaces(project_dir)
    elif monorepo_type == "lerna":
        packages = _get_lerna_packages(project_dir)
    elif monorepo_type == "cargo":
        packages = _get_cargo_members(project_dir)
    # Add more as needed
    
    return packages


def _get_pnpm_workspaces(project_dir: Path) -> list[Path]:
    """Parse pnpm-workspace.yaml for package locations.

    Args:
        project_dir: Root directory of the monorepo.

    Returns:
        List of workspace package directories.

    Raises:
        MonorepoError: If workspace configuration is malformed.
    """
    try:
        import yaml
    except ImportError:
        # Fallback to simple parsing if yaml not available
        return _get_pnpm_workspaces_simple(project_dir)

    workspace_file = project_dir / "pnpm-workspace.yaml"
    if not workspace_file.exists():
        workspace_file = project_dir / "pnpm-workspace.yml"

    if not workspace_file.exists():
        return []

    try:
        with open(workspace_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        patterns = data.get("packages", [])
        return _expand_glob_patterns(project_dir, patterns)
    except yaml.YAMLError as e:
        raise MonorepoError(
            f"Invalid YAML in pnpm workspace config at {workspace_file}: {e}"
        ) from e
    except Exception as e:
        # For other errors, log but return empty list
        import logging
        logging.debug(f"Error parsing pnpm workspace: {e}")
        return []


def _get_pnpm_workspaces_simple(project_dir: Path) -> list[Path]:
    """Simple parser for pnpm-workspace.yaml without yaml dependency.

    Args:
        project_dir: Root directory of the monorepo.

    Returns:
        List of workspace package directories.
    """
    workspace_file = project_dir / "pnpm-workspace.yaml"
    if not workspace_file.exists():
        workspace_file = project_dir / "pnpm-workspace.yml"

    if not workspace_file.exists():
        return []

    try:
        content = workspace_file.read_text(encoding="utf-8")
        # Simple regex-like extraction
        patterns = []
        in_packages = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("packages:"):
                in_packages = True
                continue
            if in_packages and line.startswith("-"):
                pattern = line[1:].strip().strip('"').strip("'")
                if pattern:
                    patterns.append(pattern)
            elif in_packages and line and not line.startswith("#"):
                break
        return _expand_glob_patterns(project_dir, patterns)
    except (FileNotFoundError, UnicodeDecodeError) as e:
        # File unreadable - log but don't fail
        import logging
        logging.debug(f"Error reading pnpm workspace file: {e}")
        return []


def _get_npm_workspaces(project_dir: Path) -> list[Path]:
    """Parse package.json workspaces field.

    Args:
        project_dir: Root directory of the monorepo.

    Returns:
        List of workspace package directories.

    Raises:
        MonorepoError: If package.json is malformed.
    """
    package_json = project_dir / "package.json"
    if not package_json.exists():
        return []

    try:
        with open(package_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        workspaces = data.get("workspaces", [])

        # Handle both array and object format
        if isinstance(workspaces, dict):
            workspaces = workspaces.get("packages", [])

        return _expand_glob_patterns(project_dir, workspaces)
    except json.JSONDecodeError as e:
        raise MonorepoError(
            f"Invalid JSON in package.json at {package_json}: {e}"
        ) from e
    except Exception as e:
        # For other errors, log but return empty list
        import logging
        logging.debug(f"Error parsing npm workspaces: {e}")
        return []


def _get_lerna_packages(project_dir: Path) -> list[Path]:
    """Parse lerna.json for package locations.

    Args:
        project_dir: Root directory of the monorepo.

    Returns:
        List of workspace package directories.

    Raises:
        MonorepoError: If lerna.json is malformed.
    """
    lerna_json = project_dir / "lerna.json"
    if not lerna_json.exists():
        return []

    try:
        with open(lerna_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        patterns = data.get("packages", ["packages/*"])
        return _expand_glob_patterns(project_dir, patterns)
    except json.JSONDecodeError as e:
        raise MonorepoError(
            f"Invalid JSON in lerna.json at {lerna_json}: {e}"
        ) from e
    except Exception as e:
        # For other errors, log but return empty list
        import logging
        logging.debug(f"Error parsing lerna packages: {e}")
        return []


def _get_cargo_members(project_dir: Path) -> list[Path]:
    """Parse Cargo.toml workspace members.

    Args:
        project_dir: Root directory of the monorepo.

    Returns:
        List of workspace package directories.

    Raises:
        MonorepoError: If Cargo.toml is malformed.
    """
    cargo_toml = project_dir / "Cargo.toml"
    if not cargo_toml.exists():
        return []

    try:
        content = cargo_toml.read_text(encoding="utf-8")
        # Simple extraction of members from [workspace] section
        members = []
        in_workspace = False
        in_members = False
        import re

        for line in content.split("\n"):
            line_stripped = line.strip()
            if line_stripped == "[workspace]":
                in_workspace = True
                continue
            if in_workspace and line_stripped.startswith("members"):
                in_members = True
                # Extract from members = ["...", "..."]
                if "=" in line:
                    members_str = line.split("=", 1)[1].strip()
                    # Extract quoted strings from this line
                    matches = re.findall(r'["\']([^"\']+)["\']', members_str)
                    members.extend(matches)
                continue
            # Continue parsing members array if we're inside it
            if in_members:
                if line_stripped.startswith("]"):
                    in_members = False
                    break
                # Extract quoted strings from continuation lines
                matches = re.findall(r'["\']([^"\']+)["\']', line_stripped)
                members.extend(matches)
                continue
            # Stop if we hit another section
            if in_workspace and line_stripped.startswith("[") and line_stripped != "[workspace]":
                break

        return _expand_glob_patterns(project_dir, members)
    except (FileNotFoundError, UnicodeDecodeError) as e:
        # File unreadable - log but don't fail
        import logging
        logging.debug(f"Error reading Cargo.toml: {e}")
        return []


def _expand_glob_patterns(base_dir: Path, patterns: list[str]) -> list[Path]:
    """Expand glob patterns to actual directories."""
    results = []
    for pattern in patterns:
        # Handle negation patterns
        if pattern.startswith("!"):
            continue
        
        # Convert to absolute path pattern
        if pattern.startswith("/"):
            pattern = pattern[1:]
        
        # Use glob to find matches
        matches = glob.glob(str(base_dir / pattern))
        for match in matches:
            path = Path(match)
            if path.is_dir():
                results.append(path)
    
    # Remove duplicates and sort
    return sorted(set(results))

