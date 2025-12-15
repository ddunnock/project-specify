"""Tests for monorepo detection and workspace support."""

import json
from pathlib import Path
import pytest

from specify_cli.monorepo import (
    detect_monorepo_type,
    get_workspace_packages,
    _get_pnpm_workspaces,
    _get_npm_workspaces,
    _get_lerna_packages,
    _get_cargo_members,
    _expand_glob_patterns,
)


# =============================================================================
# Monorepo Type Detection Tests
# =============================================================================


def test_detect_pnpm_workspace(mock_monorepo_pnpm):
    """Test detection of pnpm workspace."""
    result = detect_monorepo_type(mock_monorepo_pnpm)
    assert result == "pnpm"


def test_detect_pnpm_workspace_yml_extension(temp_project):
    """Test detection of pnpm workspace with .yml extension."""
    (temp_project / "pnpm-workspace.yml").write_text("packages:\n  - 'packages/*'\n")
    result = detect_monorepo_type(temp_project)
    assert result == "pnpm"


def test_detect_npm_workspaces(mock_monorepo_npm):
    """Test detection of npm workspaces."""
    result = detect_monorepo_type(mock_monorepo_npm)
    assert result == "npm"


def test_detect_yarn_workspaces(temp_project):
    """Test detection of yarn workspaces (same as npm format)."""
    package_json = temp_project / "package.json"
    package_json.write_text(json.dumps({
        "name": "test-yarn",
        "workspaces": {
            "packages": ["packages/*"]
        }
    }))
    result = detect_monorepo_type(temp_project)
    assert result == "npm"  # Yarn uses same format, returns "npm"


def test_detect_lerna(mock_monorepo_lerna):
    """Test detection of Lerna monorepo."""
    result = detect_monorepo_type(mock_monorepo_lerna)
    assert result == "lerna"


def test_detect_nx(mock_monorepo_nx):
    """Test detection of Nx monorepo."""
    result = detect_monorepo_type(mock_monorepo_nx)
    assert result == "nx"


def test_detect_turborepo(temp_project):
    """Test detection of Turborepo."""
    turbo_json = temp_project / "turbo.json"
    turbo_json.write_text(json.dumps({
        "pipeline": {
            "build": {"outputs": ["dist/**"]}
        }
    }))
    result = detect_monorepo_type(temp_project)
    assert result == "turborepo"


def test_detect_cargo_workspace(mock_monorepo_cargo):
    """Test detection of Cargo workspace."""
    result = detect_monorepo_type(mock_monorepo_cargo)
    assert result == "cargo"


def test_no_monorepo_detected(temp_project):
    """Test that None is returned for non-monorepo projects."""
    # Create a regular project with package.json but no workspaces
    package_json = temp_project / "package.json"
    package_json.write_text(json.dumps({
        "name": "regular-project",
        "version": "1.0.0"
    }))
    result = detect_monorepo_type(temp_project)
    assert result is None


def test_invalid_package_json(temp_project):
    """Test handling of malformed package.json."""
    package_json = temp_project / "package.json"
    package_json.write_text("{ invalid json }")
    result = detect_monorepo_type(temp_project)
    assert result is None


def test_invalid_cargo_toml(temp_project):
    """Test handling of Cargo.toml without workspace section."""
    cargo_toml = temp_project / "Cargo.toml"
    cargo_toml.write_text("[package]\nname = \"test\"\nversion = \"0.1.0\"\n")
    result = detect_monorepo_type(temp_project)
    assert result is None


# =============================================================================
# Workspace Package Retrieval Tests
# =============================================================================


def test_get_pnpm_workspace_packages(temp_project):
    """Test getting workspace packages from pnpm-workspace.yaml."""
    # Create workspace file
    (temp_project / "pnpm-workspace.yaml").write_text("""packages:
  - 'packages/*'
  - 'apps/*'
""")

    # Create actual package directories
    (temp_project / "packages" / "core").mkdir(parents=True)
    (temp_project / "packages" / "utils").mkdir(parents=True)
    (temp_project / "apps" / "web").mkdir(parents=True)
    (temp_project / "apps" / "api").mkdir(parents=True)

    packages = _get_pnpm_workspaces(temp_project)

    # Should find 4 packages
    assert len(packages) == 4
    assert any("core" in str(p) for p in packages)
    assert any("utils" in str(p) for p in packages)
    assert any("web" in str(p) for p in packages)
    assert any("api" in str(p) for p in packages)


def test_get_npm_workspace_packages_array_format(temp_project):
    """Test getting workspace packages from package.json (array format)."""
    package_json = temp_project / "package.json"
    package_json.write_text(json.dumps({
        "name": "test-monorepo",
        "workspaces": ["packages/*"]
    }))

    # Create package directories
    (temp_project / "packages" / "lib1").mkdir(parents=True)
    (temp_project / "packages" / "lib2").mkdir(parents=True)

    packages = _get_npm_workspaces(temp_project)

    assert len(packages) == 2
    assert any("lib1" in str(p) for p in packages)
    assert any("lib2" in str(p) for p in packages)


def test_get_npm_workspace_packages_object_format(temp_project):
    """Test getting workspace packages from package.json (object format)."""
    package_json = temp_project / "package.json"
    package_json.write_text(json.dumps({
        "name": "test-monorepo",
        "workspaces": {
            "packages": ["libs/*", "apps/*"]
        }
    }))

    # Create package directories
    (temp_project / "libs" / "shared").mkdir(parents=True)
    (temp_project / "apps" / "frontend").mkdir(parents=True)

    packages = _get_npm_workspaces(temp_project)

    assert len(packages) == 2
    assert any("shared" in str(p) for p in packages)
    assert any("frontend" in str(p) for p in packages)


def test_get_lerna_packages(temp_project):
    """Test getting packages from lerna.json."""
    lerna_json = temp_project / "lerna.json"
    lerna_json.write_text(json.dumps({
        "version": "1.0.0",
        "packages": ["packages/*", "tools/*"]
    }))

    # Create package directories
    (temp_project / "packages" / "core").mkdir(parents=True)
    (temp_project / "tools" / "build").mkdir(parents=True)

    packages = _get_lerna_packages(temp_project)

    assert len(packages) == 2
    assert any("core" in str(p) for p in packages)
    assert any("build" in str(p) for p in packages)


def test_get_lerna_packages_default(temp_project):
    """Test that lerna defaults to packages/* if not specified."""
    lerna_json = temp_project / "lerna.json"
    lerna_json.write_text(json.dumps({"version": "1.0.0"}))

    # Create package directory
    (temp_project / "packages" / "lib").mkdir(parents=True)

    packages = _get_lerna_packages(temp_project)

    assert len(packages) == 1
    assert any("lib" in str(p) for p in packages)


def test_get_cargo_members(temp_project):
    """Test getting workspace members from Cargo.toml."""
    cargo_toml = temp_project / "Cargo.toml"
    cargo_toml.write_text("""[workspace]
members = [
    "crates/*",
    "examples/demo",
]

[workspace.package]
version = "0.1.0"
""")

    # Create crate directories
    (temp_project / "crates" / "core").mkdir(parents=True)
    (temp_project / "crates" / "utils").mkdir(parents=True)
    (temp_project / "examples" / "demo").mkdir(parents=True)

    packages = _get_cargo_members(temp_project)

    assert len(packages) == 3
    assert any("core" in str(p) for p in packages)
    assert any("utils" in str(p) for p in packages)
    assert any("demo" in str(p) for p in packages)


def test_get_workspace_packages_integration(mock_monorepo_pnpm):
    """Test the main get_workspace_packages function."""
    monorepo_type = detect_monorepo_type(mock_monorepo_pnpm)
    packages = get_workspace_packages(mock_monorepo_pnpm, monorepo_type)

    # Should find the packages created by the fixture
    assert len(packages) >= 2
    assert any("core" in str(p) for p in packages)
    assert any("web" in str(p) for p in packages)


def test_get_workspace_packages_unknown_type(temp_project):
    """Test that unknown monorepo types return empty list."""
    packages = get_workspace_packages(temp_project, "unknown-type")
    assert packages == []


# =============================================================================
# Glob Pattern Expansion Tests
# =============================================================================


def test_expand_glob_patterns_simple(temp_project):
    """Test expanding simple glob patterns."""
    (temp_project / "packages" / "lib1").mkdir(parents=True)
    (temp_project / "packages" / "lib2").mkdir(parents=True)

    patterns = ["packages/*"]
    result = _expand_glob_patterns(temp_project, patterns)

    assert len(result) == 2
    assert all(p.is_dir() for p in result)


def test_expand_glob_patterns_multiple(temp_project):
    """Test expanding multiple glob patterns."""
    (temp_project / "packages" / "core").mkdir(parents=True)
    (temp_project / "apps" / "web").mkdir(parents=True)
    (temp_project / "tools" / "cli").mkdir(parents=True)

    patterns = ["packages/*", "apps/*", "tools/*"]
    result = _expand_glob_patterns(temp_project, patterns)

    assert len(result) == 3


def test_expand_glob_patterns_negation(temp_project):
    """Test that negation patterns (starting with !) are skipped."""
    (temp_project / "packages" / "lib1").mkdir(parents=True)

    patterns = ["packages/*", "!packages/lib1"]
    result = _expand_glob_patterns(temp_project, patterns)

    # Should still find lib1 (negation is handled by package managers, not us)
    assert len(result) >= 1


def test_expand_glob_patterns_deduplicate(temp_project):
    """Test that duplicate paths are removed."""
    (temp_project / "packages" / "core").mkdir(parents=True)

    patterns = ["packages/*", "packages/core"]
    result = _expand_glob_patterns(temp_project, patterns)

    # Should only have one entry for core
    core_paths = [p for p in result if "core" in str(p)]
    assert len(core_paths) == 1


def test_expand_glob_patterns_files_excluded(temp_project):
    """Test that files (not directories) are excluded."""
    (temp_project / "packages").mkdir()
    (temp_project / "packages" / "lib").mkdir()
    (temp_project / "packages" / "README.md").write_text("# README")

    patterns = ["packages/*"]
    result = _expand_glob_patterns(temp_project, patterns)

    # Should only find the directory, not the file
    assert len(result) == 1
    assert result[0].name == "lib"


# =============================================================================
# Edge Cases and Error Handling
# =============================================================================


def test_detect_monorepo_empty_directory(temp_project):
    """Test detection in empty directory."""
    result = detect_monorepo_type(temp_project)
    assert result is None


def test_get_packages_missing_config_file(temp_project):
    """Test getting packages when config file doesn't exist."""
    packages = _get_pnpm_workspaces(temp_project)
    assert packages == []

    packages = _get_npm_workspaces(temp_project)
    assert packages == []

    packages = _get_lerna_packages(temp_project)
    assert packages == []

    packages = _get_cargo_members(temp_project)
    assert packages == []


def test_get_packages_invalid_json(temp_project):
    """Test handling of invalid JSON in config files raises MonorepoError."""
    from specify_cli.errors import MonorepoError

    # Invalid package.json raises MonorepoError
    (temp_project / "package.json").write_text("{ invalid }")
    with pytest.raises(MonorepoError) as exc_info:
        _get_npm_workspaces(temp_project)
    assert "Invalid JSON" in str(exc_info.value)

    # Invalid lerna.json raises MonorepoError
    (temp_project / "lerna.json").write_text("{ also invalid }")
    with pytest.raises(MonorepoError) as exc_info:
        _get_lerna_packages(temp_project)
    assert "Invalid JSON" in str(exc_info.value)


def test_pnpm_workspace_simple_parser_fallback(temp_project):
    """Test the simple YAML parser fallback for pnpm."""
    # This would be used if yaml module isn't available
    (temp_project / "pnpm-workspace.yaml").write_text("""packages:
  - 'packages/*'
  - "apps/*"
  # This is a comment
  - 'libs/*'
""")

    (temp_project / "packages" / "core").mkdir(parents=True)
    (temp_project / "apps" / "web").mkdir(parents=True)
    (temp_project / "libs" / "utils").mkdir(parents=True)

    # Test the simple parser directly
    from specify_cli.monorepo import _get_pnpm_workspaces_simple
    packages = _get_pnpm_workspaces_simple(temp_project)

    assert len(packages) == 3


def test_expand_glob_patterns_leading_slash(temp_project):
    """Test patterns with leading slash are handled correctly."""
    (temp_project / "packages" / "lib").mkdir(parents=True)

    patterns = ["/packages/*"]
    result = _expand_glob_patterns(temp_project, patterns)

    # Should still find packages despite leading slash
    assert len(result) == 1


def test_detect_monorepo_priority(temp_project):
    """Test detection priority when multiple indicators exist."""
    # Create multiple monorepo indicators
    (temp_project / "pnpm-workspace.yaml").write_text("packages:\n  - 'packages/*'\n")
    (temp_project / "lerna.json").write_text(json.dumps({"version": "1.0.0"}))

    result = detect_monorepo_type(temp_project)

    # pnpm should be detected first (based on indicators dict order)
    assert result == "pnpm"
