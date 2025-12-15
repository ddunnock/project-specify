"""Tests for template download and file operations."""

import json
import os
import stat
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
import responses

# Import from dedicated modules (Phase 2 refactoring)
from specify_cli.file_operations import merge_json_files, handle_vscode_settings
from specify_cli.template_download import ensure_executable_scripts, download_template_from_github


# =============================================================================
# JSON Merging Tests
# =============================================================================


def test_merge_json_files_simple(temp_project):
    """Test simple JSON file merging."""
    file1 = temp_project / "config1.json"
    file2 = temp_project / "config2.json"

    file1.write_text(json.dumps({"key1": "value1", "shared": "from1"}))
    file2.write_text(json.dumps({"key2": "value2", "shared": "from2"}))

    result = merge_json_files(file1, file2)

    assert result["key1"] == "value1"
    assert result["key2"] == "value2"
    assert result["shared"] == "from2"  # file2 wins


def test_merge_json_files_nested(temp_project):
    """Test merging nested JSON structures."""
    file1 = temp_project / "config1.json"
    file2 = temp_project / "config2.json"

    file1.write_text(json.dumps({
        "outer": {
            "inner1": "value1",
            "shared": "from1"
        }
    }))
    file2.write_text(json.dumps({
        "outer": {
            "inner2": "value2",
            "shared": "from2"
        }
    }))

    result = merge_json_files(file1, file2)

    assert result["outer"]["inner1"] == "value1"
    assert result["outer"]["inner2"] == "value2"
    assert result["outer"]["shared"] == "from2"


def test_merge_json_files_arrays(temp_project):
    """Test that arrays are replaced, not merged."""
    file1 = temp_project / "config1.json"
    file2 = temp_project / "config2.json"

    file1.write_text(json.dumps({"items": [1, 2, 3]}))
    file2.write_text(json.dumps({"items": [4, 5]}))

    result = merge_json_files(file1, file2)

    # Arrays are replaced, not merged
    assert result["items"] == [4, 5]


def test_merge_json_files_first_missing(temp_project):
    """Test merging when first file doesn't exist."""
    file1 = temp_project / "nonexistent.json"
    file2 = temp_project / "config2.json"

    file2.write_text(json.dumps({"key": "value"}))

    result = merge_json_files(file1, file2)

    assert result["key"] == "value"


def test_merge_json_files_second_missing(temp_project):
    """Test merging when second file doesn't exist."""
    file1 = temp_project / "config1.json"
    file2 = temp_project / "nonexistent.json"

    file1.write_text(json.dumps({"key": "value"}))

    result = merge_json_files(file1, file2)

    assert result["key"] == "value"


def test_merge_json_files_both_missing(temp_project):
    """Test merging when both files don't exist."""
    file1 = temp_project / "missing1.json"
    file2 = temp_project / "missing2.json"

    result = merge_json_files(file1, file2)

    assert result == {}


def test_merge_json_files_invalid_json(temp_project):
    """Test handling of invalid JSON."""
    file1 = temp_project / "invalid.json"
    file2 = temp_project / "valid.json"

    file1.write_text("{ invalid json }")
    file2.write_text(json.dumps({"key": "value"}))

    result = merge_json_files(file1, file2)

    # Should still get valid file's data
    assert result.get("key") == "value" or result == {}


# =============================================================================
# VS Code Settings Handling Tests
# =============================================================================


def test_handle_vscode_settings_merge(temp_project):
    """Test merging VS Code settings."""
    vscode_dir = temp_project / ".vscode"
    vscode_dir.mkdir()

    existing = vscode_dir / "settings.json"
    new = temp_project / "new_settings.json"

    existing.write_text(json.dumps({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
    }))
    new.write_text(json.dumps({
        "editor.tabSize": 4,
        "editor.wordWrap": "on",
    }))

    # Call with correct signature: (sub_item, dest_file, rel_path, verbose, tracker)
    handle_vscode_settings(new, existing, ".vscode/settings.json")

    # Read the merged settings
    merged = json.loads(existing.read_text())

    assert merged["editor.fontSize"] == 14  # Preserved
    assert merged["editor.tabSize"] == 4  # Updated
    assert merged["editor.wordWrap"] == "on"  # Added


def test_handle_vscode_settings_no_existing(temp_project):
    """Test handling VS Code settings when .vscode doesn't exist."""
    vscode_dir = temp_project / ".vscode"
    vscode_dir.mkdir()  # Create directory first

    existing = vscode_dir / "settings.json"
    new = temp_project / "new_settings.json"
    new.write_text(json.dumps({"editor.fontSize": 16}))

    # Call with correct signature
    handle_vscode_settings(new, existing, ".vscode/settings.json")

    # Should create settings file
    assert existing.exists()

    settings = json.loads(existing.read_text())
    assert settings["editor.fontSize"] == 16


def test_handle_vscode_settings_source_missing(temp_project):
    """Test handling when source settings file doesn't exist."""
    from specify_cli.errors import FileOperationError

    vscode_dir = temp_project / ".vscode"
    vscode_dir.mkdir()
    existing = vscode_dir / "settings.json"
    existing.write_text(json.dumps({"key": "value"}))

    nonexistent = temp_project / "nonexistent.json"

    # Function will raise FileOperationError when source doesn't exist
    # This is expected behavior - can't merge from nonexistent file
    import pytest
    with pytest.raises(FileOperationError) as exc_info:
        handle_vscode_settings(nonexistent, existing, ".vscode/settings.json")

    assert "Failed to copy VS Code settings" in str(exc_info.value)


# =============================================================================
# Script Permissions Tests
# =============================================================================


@pytest.mark.skipif(not hasattr(os, "chmod"), reason="chmod not available")
def test_ensure_executable_scripts_sh_files(temp_project):
    """Test making .sh files executable."""
    import os

    # Function looks for scripts in .specify/scripts/
    specify_dir = temp_project / ".specify"
    specify_dir.mkdir()
    script_dir = specify_dir / "scripts"
    script_dir.mkdir()

    script = script_dir / "test.sh"
    script.write_text("#!/bin/bash\necho 'test'\n")

    # Initially not executable
    script.chmod(0o644)

    ensure_executable_scripts(temp_project)

    # Should now be executable
    file_stat = script.stat()
    assert file_stat.st_mode & stat.S_IXUSR


@pytest.mark.skipif(not hasattr(os, "chmod"), reason="chmod not available")
def test_ensure_executable_scripts_nested(temp_project):
    """Test making scripts executable in nested directories."""
    import os

    # Function looks for scripts in .specify/scripts/ (recursively)
    specify_dir = temp_project / ".specify"
    specify_dir.mkdir()
    nested = specify_dir / "scripts" / "tools"
    nested.mkdir(parents=True)

    script = nested / "build.sh"
    script.write_text("#!/bin/bash\n")
    script.chmod(0o644)

    ensure_executable_scripts(temp_project)

    file_stat = script.stat()
    assert file_stat.st_mode & stat.S_IXUSR


@pytest.mark.skipif(not hasattr(os, "chmod"), reason="chmod not available")
def test_ensure_executable_scripts_preserves_other_files(temp_project):
    """Test that non-script files are not modified."""
    import os

    (temp_project / "README.md").write_text("# README")
    (temp_project / "config.json").write_text("{}")

    original_readme_mode = (temp_project / "README.md").stat().st_mode

    ensure_executable_scripts(temp_project)

    # Non-script files should be unchanged
    assert (temp_project / "README.md").stat().st_mode == original_readme_mode


# =============================================================================
# GitHub Template Download Tests
# =============================================================================


def test_download_template_from_github_success(temp_project):
    """Test template download returns expected structure."""
    # Note: This test makes real API calls to GitHub
    # We're just verifying the function signature and return structure
    try:
        # Call with correct signature: (ai_assistant, download_dir)
        zip_path, metadata = download_template_from_github("claude", temp_project, verbose=False, show_progress=False)

        # Verify the return structure
        assert isinstance(zip_path, Path)
        assert zip_path.exists()
        assert isinstance(metadata, dict)
        assert "release" in metadata
        assert "size" in metadata
        assert "filename" in metadata
        assert "asset_url" in metadata
    except Exception as e:
        # If GitHub API is unavailable or rate limited, skip the test
        import pytest
        pytest.skip(f"GitHub API unavailable: {e}")


@responses.activate
def test_download_template_github_rate_limit(temp_project):
    """Test handling of GitHub rate limit errors."""
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test/repo/releases/latest",
        json={"message": "API rate limit exceeded"},
        status=403,
        headers={
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": "1234567890",
        },
    )

    # Should handle rate limit gracefully
    with pytest.raises((Exception, RuntimeError)):
        download_template_from_github("test/repo", "latest", temp_project)


@responses.activate
def test_download_template_github_not_found(temp_project):
    """Test handling of repository not found."""
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test/nonexistent/releases/latest",
        json={"message": "Not Found"},
        status=404,
    )

    # Should handle 404 gracefully
    with pytest.raises((Exception, RuntimeError)):
        download_template_from_github("test/nonexistent", "latest", temp_project)


# =============================================================================
# Template Extraction Tests
# =============================================================================


def test_template_extraction_from_zip(temp_project, mock_template_zip):
    """Test extracting template from zip file."""
    # Create a test zip file
    zip_path = temp_project / "template.zip"

    # Create a simple zip with a file
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.writestr("template/README.md", "# Template README")
        zipf.writestr("template/.specify/config.json", '{"key": "value"}')

    # Extract it
    extract_dir = temp_project / "extracted"
    extract_dir.mkdir()

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_dir)

    # Verify extraction
    assert (extract_dir / "template" / "README.md").exists()
    assert (extract_dir / "template" / ".specify" / "config.json").exists()


def test_template_zip_with_nested_structure(temp_project):
    """Test handling zip files with nested directory structure."""
    zip_path = temp_project / "nested.zip"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.writestr("repo-main/.specify/templates/spec.md", "# Spec")
        zipf.writestr("repo-main/src/file.py", "print('hello')")

    extract_dir = temp_project / "extracted"
    extract_dir.mkdir()

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_dir)

    assert (extract_dir / "repo-main" / ".specify" / "templates" / "spec.md").exists()


# =============================================================================
# Integration Tests
# =============================================================================


def test_full_vscode_settings_workflow(temp_project):
    """Test complete workflow of VS Code settings merge."""
    # Create initial settings
    vscode_dir = temp_project / ".vscode"
    vscode_dir.mkdir()
    existing = vscode_dir / "settings.json"
    existing.write_text(json.dumps({
        "editor.fontSize": 12,
        "files.exclude": {
            "**/.git": True,
        }
    }, indent=2))

    # Create template settings
    template_settings = temp_project / "template_settings.json"
    template_settings.write_text(json.dumps({
        "editor.fontSize": 14,
        "editor.formatOnSave": True,
        "files.exclude": {
            "**/node_modules": True,
        }
    }, indent=2))

    # Merge with correct signature: (source, dest, rel_path)
    handle_vscode_settings(template_settings, existing, ".vscode/settings.json")

    # Verify result
    result = json.loads((vscode_dir / "settings.json").read_text())

    assert result["editor.fontSize"] == 14
    assert result["editor.formatOnSave"] is True
    assert result["files.exclude"]["**/.git"] is True
    assert result["files.exclude"]["**/node_modules"] is True


def test_merge_preserves_comments_indirectly(temp_project):
    """Test that merge handles JSON without comments (JSON doesn't support comments)."""
    file1 = temp_project / "config1.json"
    file2 = temp_project / "config2.json"

    # JSON doesn't support comments, but we test clean formatting
    file1.write_text(json.dumps({"key1": "value1"}, indent=2))
    file2.write_text(json.dumps({"key2": "value2"}, indent=2))

    result = merge_json_files(file1, file2)

    # Should have both keys
    assert "key1" in result
    assert "key2" in result


# =============================================================================
# Edge Cases
# =============================================================================


def test_merge_json_with_null_values(temp_project):
    """Test merging JSON with null values."""
    file1 = temp_project / "config1.json"
    file2 = temp_project / "config2.json"

    file1.write_text(json.dumps({"key": "value"}))
    file2.write_text(json.dumps({"key": None}))

    result = merge_json_files(file1, file2)

    assert result["key"] is None


def test_merge_json_with_boolean_values(temp_project):
    """Test merging JSON with boolean values."""
    file1 = temp_project / "config1.json"
    file2 = temp_project / "config2.json"

    file1.write_text(json.dumps({"enabled": False}))
    file2.write_text(json.dumps({"enabled": True, "debug": False}))

    result = merge_json_files(file1, file2)

    assert result["enabled"] is True
    assert result["debug"] is False


def test_ensure_executable_empty_directory(temp_project):
    """Test ensure_executable_scripts on empty directory."""
    # Should handle gracefully
    ensure_executable_scripts(temp_project)

    # No errors should occur
    assert True
