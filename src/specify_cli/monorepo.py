"""
Monorepo detection and workspace support for project-specify.
"""

from pathlib import Path
from typing import Optional
import json
import glob


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
        except (json.JSONDecodeError, Exception):
            pass
    
    # Check Cargo.toml for Rust workspaces
    cargo_toml = project_dir / "Cargo.toml"
    if cargo_toml.exists():
        try:
            # Simple check for [workspace] section
            content = cargo_toml.read_text(encoding="utf-8")
            if "[workspace]" in content:
                return "cargo"
        except Exception:
            pass
    
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
    """Parse pnpm-workspace.yaml for package locations."""
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
    except Exception:
        return []


def _get_pnpm_workspaces_simple(project_dir: Path) -> list[Path]:
    """Simple parser for pnpm-workspace.yaml without yaml dependency."""
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
    except Exception:
        return []


def _get_npm_workspaces(project_dir: Path) -> list[Path]:
    """Parse package.json workspaces field."""
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
    except Exception:
        return []


def _get_lerna_packages(project_dir: Path) -> list[Path]:
    """Parse lerna.json for package locations."""
    lerna_json = project_dir / "lerna.json"
    if not lerna_json.exists():
        return []
    
    try:
        with open(lerna_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        patterns = data.get("packages", ["packages/*"])
        return _expand_glob_patterns(project_dir, patterns)
    except Exception:
        return []


def _get_cargo_members(project_dir: Path) -> list[Path]:
    """Parse Cargo.toml workspace members."""
    cargo_toml = project_dir / "Cargo.toml"
    if not cargo_toml.exists():
        return []
    
    try:
        content = cargo_toml.read_text(encoding="utf-8")
        # Simple extraction of members from [workspace] section
        members = []
        in_workspace = False
        in_members = False
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
                    # Simple extraction
                    import re
                    matches = re.findall(r'["\']([^"\']+)["\']', members_str)
                    members.extend(matches)
                continue
            if in_workspace and line_stripped.startswith("[") and not line_stripped.startswith("["):
                break
            if in_members and line_stripped.startswith("]"):
                break
        
        return _expand_glob_patterns(project_dir, members)
    except Exception:
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

