"""File operation utilities for project-specify."""

import json
import shutil
from pathlib import Path

from .errors import FileOperationError


def handle_vscode_settings(sub_item: Path, dest_file: Path, rel_path: str, verbose: bool = False, tracker=None) -> None:
    """Handle merging or copying of .vscode/settings.json files.

    Args:
        sub_item: Source settings file path.
        dest_file: Destination settings file path.
        rel_path: Relative path for logging.
        verbose: Whether to print detailed logs.
        tracker: Optional StepTracker for status updates.
    """
    from .ui import console  # Import here to avoid circular dependency

    def log(message, color="green"):
        if verbose and not tracker:
            console.print(f"[{color}]{message}[/] {rel_path}")

    try:
        with open(sub_item, 'r', encoding='utf-8') as f:
            new_settings = json.load(f)

        if dest_file.exists():
            merged = merge_json_files(dest_file, new_settings, verbose=verbose and not tracker)
            with open(dest_file, 'w', encoding='utf-8') as f:
                json.dump(merged, f, indent=4)
                f.write('\n')
            log("Merged:", "green")
        else:
            shutil.copy2(sub_item, dest_file)
            log("Copied (no existing settings.json):", "blue")

    except json.JSONDecodeError as e:
        log(f"Warning: Invalid JSON, copying instead: {e}", "yellow")
        try:
            shutil.copy2(sub_item, dest_file)
        except Exception as copy_err:
            raise FileOperationError(
                f"Failed to handle VS Code settings at {dest_file}: {copy_err}"
            ) from copy_err
    except Exception as e:
        log(f"Warning: Could not merge, copying instead: {e}", "yellow")
        try:
            shutil.copy2(sub_item, dest_file)
        except Exception as copy_err:
            raise FileOperationError(
                f"Failed to copy VS Code settings to {dest_file}: {copy_err}"
            ) from copy_err


def merge_json_files(existing_path: Path, new_content: dict | Path, verbose: bool = False) -> dict:
    """Merge new JSON content into existing JSON file.

    Performs a deep merge where:
    - New keys are added
    - Existing keys are preserved unless overwritten by new content
    - Nested dictionaries are merged recursively
    - Lists and other values are replaced (not merged)

    Args:
        existing_path: Path to existing JSON file.
        new_content: New JSON content to merge in (as dict or Path to JSON file).
        verbose: Whether to print merge details.

    Returns:
        Merged JSON content as dict.
    """
    from .ui import console  # Import here to avoid circular dependency

    # Load new_content from file if it's a Path
    if isinstance(new_content, Path):
        try:
            with open(new_content, 'r', encoding='utf-8') as f:
                new_content = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If new content file doesn't exist or is invalid, return existing or empty
            try:
                with open(existing_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

    try:
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing_content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, just use new content
        return new_content

    def deep_merge(base: dict, update: dict) -> dict:
        """Recursively merge update dict into base dict."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = deep_merge(result[key], value)
            else:
                # Add new key or replace existing value
                result[key] = value
        return result

    merged = deep_merge(existing_content, new_content)

    if verbose:
        console.print(f"[cyan]Merged JSON file:[/cyan] {existing_path.name}")

    return merged
