"""Project mode detection and management.

This module provides utilities to detect and manage project mode (PRD-style) vs
feature mode (user story-driven) workflows.

Project Mode: Uses .specify/research/ and .specify/spec.md (single project PRD)
Feature Mode: Uses .specify/specs/###-feature-name/ (multiple feature specs)
"""

from pathlib import Path
from typing import Literal, Optional

ProjectMode = Literal["project", "feature", "unknown"]


def detect_project_mode(project_dir: Optional[Path] = None) -> ProjectMode:
    """
    Detect if project uses Project Mode (PRD) or Feature Mode (user stories).

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Returns:
        "project" - Has .specify/research/ and/or .specify/spec.md (PRD mode)
        "feature" - Has .specify/specs/ with numbered features (legacy mode)
        "unknown" - Neither pattern detected (new/uninitialized project)

    Examples:
        >>> detect_project_mode()  # Checks current directory
        'project'

        >>> detect_project_mode(Path('/path/to/project'))
        'feature'
    """
    if project_dir is None:
        project_dir = Path.cwd()

    specify_dir = project_dir / ".specify"

    # If .specify doesn't exist at all, it's unknown
    if not specify_dir.exists():
        return "unknown"

    # Check for project mode indicators
    research_dir = specify_dir / "research"
    research_readme = research_dir / "README.md"
    project_spec = specify_dir / "spec.md"

    # If either research exists or project-level spec exists, it's project mode
    if research_readme.exists() or project_spec.exists() or research_dir.exists():
        return "project"

    # Check for feature mode indicators
    specs_dir = specify_dir / "specs"
    if specs_dir.exists():
        # Check if there are any numbered feature directories
        feature_dirs = list(specs_dir.glob("[0-9]*-*/"))
        if feature_dirs:
            return "feature"

    # No clear indicators found
    return "unknown"


def is_project_mode(project_dir: Optional[Path] = None) -> bool:
    """
    Check if project is in Project Mode.

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Returns:
        True if in project mode, False otherwise.

    Examples:
        >>> is_project_mode()
        True
    """
    return detect_project_mode(project_dir) == "project"


def is_feature_mode(project_dir: Optional[Path] = None) -> bool:
    """
    Check if project is in Feature Mode.

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Returns:
        True if in feature mode, False otherwise.

    Examples:
        >>> is_feature_mode()
        False
    """
    return detect_project_mode(project_dir) == "feature"


def get_research_documents(project_dir: Optional[Path] = None) -> dict[str, list[Path]]:
    """
    Get all research documents organized by category.

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Returns:
        Dictionary mapping category names to lists of research document paths.
        Categories: technical, domain, user, constraints

    Examples:
        >>> docs = get_research_documents()
        >>> docs['technical']
        [Path('.specify/research/technical/data-research.md'), ...]
    """
    if project_dir is None:
        project_dir = Path.cwd()

    research_dir = project_dir / ".specify" / "research"

    if not research_dir.exists():
        return {
            "technical": [],
            "domain": [],
            "user": [],
            "constraints": [],
        }

    return {
        "technical": sorted((research_dir / "technical").glob("*.md")) if (research_dir / "technical").exists() else [],
        "domain": sorted((research_dir / "domain").glob("*.md")) if (research_dir / "domain").exists() else [],
        "user": sorted((research_dir / "user").glob("*.md")) if (research_dir / "user").exists() else [],
        "constraints": sorted((research_dir / "constraints").glob("*.md")) if (research_dir / "constraints").exists() else [],
    }


def get_research_seed_files(project_dir: Optional[Path] = None) -> dict[str, list[Path]]:
    """
    Get all research seed files organized by category.

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Returns:
        Dictionary mapping category names to lists of seed file paths.

    Examples:
        >>> seeds = get_research_seed_files()
        >>> seeds['technical']
        [Path('.specify/research-seeds/technical/data-research.seed.md'), ...]
    """
    if project_dir is None:
        project_dir = Path.cwd()

    seeds_dir = project_dir / ".specify" / "research-seeds"

    if not seeds_dir.exists():
        return {
            "technical": [],
            "domain": [],
            "user": [],
            "constraints": [],
        }

    return {
        "technical": sorted((seeds_dir / "technical").glob("*.seed.md")) if (seeds_dir / "technical").exists() else [],
        "domain": sorted((seeds_dir / "domain").glob("*.seed.md")) if (seeds_dir / "domain").exists() else [],
        "user": sorted((seeds_dir / "user").glob("*.seed.md")) if (seeds_dir / "user").exists() else [],
        "constraints": sorted((seeds_dir / "constraints").glob("*.seed.md")) if (seeds_dir / "constraints").exists() else [],
    }


def create_research_structure(project_dir: Optional[Path] = None) -> None:
    """
    Create .specify/research directory structure for project mode.

    Creates the following directories:
    - .specify/research/technical/
    - .specify/research/domain/
    - .specify/research/user/
    - .specify/research/constraints/

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Examples:
        >>> create_research_structure()
        # Creates .specify/research/{technical,domain,user,constraints}/
    """
    if project_dir is None:
        project_dir = Path.cwd()

    research_dir = project_dir / ".specify" / "research"

    for category in ["technical", "domain", "user", "constraints"]:
        category_dir = research_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)


def create_research_seeds_structure(project_dir: Optional[Path] = None) -> None:
    """
    Create .specify/research-seeds directory structure for user seed files.

    Creates the following directories:
    - .specify/research-seeds/technical/
    - .specify/research-seeds/domain/
    - .specify/research-seeds/user/
    - .specify/research-seeds/constraints/

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Examples:
        >>> create_research_seeds_structure()
        # Creates .specify/research-seeds/{technical,domain,user,constraints}/
    """
    if project_dir is None:
        project_dir = Path.cwd()

    seeds_dir = project_dir / ".specify" / "research-seeds"

    for category in ["technical", "domain", "user", "constraints"]:
        category_dir = seeds_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)


def get_project_spec_path(project_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Get path to project-level specification (PRD).

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Returns:
        Path to spec.md if in project mode and it exists, None otherwise.

    Examples:
        >>> get_project_spec_path()
        Path('.specify/spec.md')
    """
    if project_dir is None:
        project_dir = Path.cwd()

    spec_path = project_dir / ".specify" / "spec.md"

    if is_project_mode(project_dir) and spec_path.exists():
        return spec_path

    return None


def get_feature_specs(project_dir: Optional[Path] = None) -> list[Path]:
    """
    Get all feature specification directories in feature mode.

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Returns:
        List of paths to feature spec directories (###-feature-name/).

    Examples:
        >>> get_feature_specs()
        [Path('.specify/specs/001-user-auth/'), Path('.specify/specs/002-dashboard/')]
    """
    if project_dir is None:
        project_dir = Path.cwd()

    specs_dir = project_dir / ".specify" / "specs"

    if not specs_dir.exists():
        return []

    # Find all numbered feature directories
    feature_dirs = sorted(specs_dir.glob("[0-9]*-*/"))

    return feature_dirs


def get_research_index_path(project_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Get path to research index (README.md).

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Returns:
        Path to research/README.md if it exists, None otherwise.

    Examples:
        >>> get_research_index_path()
        Path('.specify/research/README.md')
    """
    if project_dir is None:
        project_dir = Path.cwd()

    index_path = project_dir / ".specify" / "research" / "README.md"

    if index_path.exists():
        return index_path

    return None


def get_mode_description(mode: ProjectMode) -> str:
    """
    Get human-readable description of project mode.

    Args:
        mode: Project mode type.

    Returns:
        Description of the mode.

    Examples:
        >>> get_mode_description("project")
        'Project Mode (PRD-style with research foundation)'
    """
    descriptions = {
        "project": "Project Mode (PRD-style with research foundation)",
        "feature": "Feature Mode (user story-driven feature specs)",
        "unknown": "Unknown (no .specify structure detected)",
    }
    return descriptions.get(mode, "Unknown mode")


# Convenience function for command-line usage
def print_project_mode(project_dir: Optional[Path] = None) -> None:
    """
    Print current project mode to stdout.

    Args:
        project_dir: Path to project directory. Defaults to current directory.

    Examples:
        >>> print_project_mode()
        Project Mode: project
        Description: Project Mode (PRD-style with research foundation)
        Research documents: 12 found
          - technical: 3
          - domain: 3
          - user: 3
          - constraints: 3
    """
    mode = detect_project_mode(project_dir)
    docs = get_research_documents(project_dir)

    print(f"Project Mode: {mode}")
    print(f"Description: {get_mode_description(mode)}")

    if mode == "project":
        total_docs = sum(len(doc_list) for doc_list in docs.values())
        print(f"Research documents: {total_docs} found")
        for category, doc_list in docs.items():
            if doc_list:
                print(f"  - {category}: {len(doc_list)}")

    elif mode == "feature":
        features = get_feature_specs(project_dir)
        print(f"Feature specs: {len(features)} found")
        for feature in features:
            print(f"  - {feature.name}")


if __name__ == "__main__":
    # Allow running as script: python -m specify_cli.project_mode
    print_project_mode()
