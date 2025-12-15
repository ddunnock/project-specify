# Project-Specify Codebase Assessment

> **Date**: December 14, 2025  
> **Repository**: Refactored fork of github/spec-kit  
> **Purpose**: Project-driven specification toolkit with monorepo and MCP support

---

## Executive Summary

This repository represents a substantial and well-architected evolution of GitHub's spec-kit. The refactoring transforms a feature-driven specification tool into a **project-driven development toolkit** with three major enhancements:

1. **Project-Centric Workflow** — Shifts focus from individual features to holistic project planning
2. **Monorepo Support** — Native detection and workspace handling for modern repository structures
3. **MCP Integration** — Auto-discovers Model Context Protocol servers to enhance AI agent capabilities

The implementation quality is generally high, with thoughtful architectural decisions around symlink-based command distribution and multi-agent support. However, there are opportunities for improvement in code organization, test coverage, and cross-platform consistency.

---

## Architecture Analysis

### Core Design Decisions

| Decision | Implementation | Assessment |
|----------|----------------|------------|
| Symlink-based commands | Commands symlinked from `~/.project-specify` | ✅ Excellent — reduces duplication, simplifies updates |
| Single-file CLI | Main logic in `__init__.py` (~1400 lines) | ⚠️ Functional but becoming unwieldy |
| Multi-agent support | `--ai all` and callback-based parsing | ✅ Well-implemented with Typer |
| MCP discovery | Dual implementation (Python + bash) | ⚠️ Redundant — risk of drift |
| Monorepo detection | Pattern matching for 6+ monorepo types | ✅ Comprehensive coverage |

### Component Structure

```
src/specify_cli/
├── __init__.py           # Main CLI (1400+ lines) — needs refactoring
├── main.py               # Entry point wrapper
├── symlink_manager.py    # ✅ Clean, well-separated
├── monorepo.py           # ✅ Clean, well-separated  
├── mcp_discovery.py      # ✅ Clean, well-separated
├── agents/               # Agent-specific command templates
│   ├── claude/commands/
│   ├── cursor/commands/
│   ├── copilot/commands/
│   └── [15+ more agents]
├── templates/            # Project templates
└── scripts/              # Bash/PowerShell automation
```

### Data Flow

```
project-specify init . --ai all
        │
        ▼
┌───────────────────────────────────┐
│  1. Ensure Central Installation   │
│     ~/.project-specify/agents/    │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│  2. Detect Monorepo Type          │
│     (pnpm/npm/lerna/cargo/etc)    │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│  3. Create .specify/ Structure    │
│     (project-specific, not        │
│      symlinked)                   │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│  4. Create Agent Symlinks         │
│     .claude/commands →            │
│     ~/.project-specify/agents/    │
│     claude/commands/              │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│  5. MCP Discovery (optional)      │
│     Writes to:                    │
│     .specify/context/             │
│       ├── mcp-servers.md          │
│       └── project-context.json    │
└───────────────────────────────────┘
```

---

## Strengths

### 1. Symlink Architecture (Score: 9/10)

The symlink-based command distribution is the standout architectural decision:

**Benefits:**
- Single source of truth for command updates
- Disk space efficiency across multiple projects
- Atomic updates (update central, all projects benefit)
- Clear separation of concerns (shared vs. project-specific)

**Implementation Quality:**
- Proper symlink verification with status tracking
- Windows Developer Mode detection and helpful error messages
- Fallback handling for broken symlinks

### 2. MCP Integration (Score: 8/10)

The MCP discovery system is comprehensive and forward-thinking:

**Capabilities:**
- Cross-platform config path detection
- Multiple source support (Claude Desktop, Claude Code, Cursor, project-local)
- Technology stack auto-detection
- Context file generation for AI consumption

**Command Integration:**
Commands like `/speckit.plan` include MCP-aware sections:
```markdown
### If `postgres` MCP is available:
- Use MCP for database queries during implementation
- Plan schema inspection via MCP tools
```

### 3. Monorepo Support (Score: 8/10)

Comprehensive detection for modern repository structures:

| Type | Detection Method | Status |
|------|------------------|--------|
| pnpm | `pnpm-workspace.yaml` | ✅ |
| npm/yarn | `package.json` workspaces | ✅ |
| lerna | `lerna.json` | ✅ |
| nx | `nx.json` | ✅ |
| turborepo | `turbo.json` | ✅ |
| cargo | `Cargo.toml` [workspace] | ✅ |

### 4. Multi-Agent Support (Score: 9/10)

Flexible agent configuration supporting 18+ AI assistants:

```python
# Multiple invocation styles supported:
project-specify init . --ai claude --ai cursor --ai copilot
project-specify init . --ai claude,cursor,copilot
project-specify init . --ai all
```

The Typer callback implementation cleanly handles all formats.

### 5. Spec-Driven Workflow (Score: 8/10)

Well-designed progression through development phases:

```
/speckit.constitution → Project principles
/speckit.specify      → Requirements & user stories
/speckit.plan         → Technical implementation plan
/speckit.tasks        → Actionable task breakdown
/speckit.implement    → Guided implementation
```

Enhancement commands (`/speckit.clarify`, `/speckit.analyze`, `/speckit.checklist`) add quality gates.

---

## Areas for Improvement

### 1. Code Organization (Priority: High)

**Problem:** The `__init__.py` file has grown to ~1400 lines, mixing:
- CLI command definitions
- Template download/extraction logic
- Git operations
- Step tracking UI
- JSON merging utilities
- Agent configuration

**Recommendation:** Split into focused modules:

```python
# src/specify_cli/cli.py
from .commands import init, check, discover, status
from .config import AGENT_CONFIG, SUPPORTED_AGENTS

# src/specify_cli/commands/init.py
@app.command()
def init(...):
    """Initialize command logic"""

# src/specify_cli/template.py
def download_template_from_github(...):
def download_and_extract_template(...):
def deep_merge_json(...):

# src/specify_cli/tracker.py
class StepTracker:
    """Progress tracking UI"""

# src/specify_cli/config.py
AGENT_CONFIG = {...}
SUPPORTED_AGENTS = [...]
```

### 2. Test Coverage (Priority: High)

**Problem:** Test infrastructure exists but implementation is sparse.

**Critical Test Areas:**

```python
# tests/test_symlinks.py
def test_create_single_agent_symlink():
def test_create_multiple_agent_symlinks():
def test_verify_valid_symlink():
def test_verify_broken_symlink():
def test_windows_developer_mode_required():

# tests/test_monorepo.py
def test_detect_pnpm_workspace():
def test_detect_npm_workspaces():
def test_detect_cargo_workspace():
def test_get_workspace_packages_pnpm():
def test_invalid_monorepo():

# tests/test_mcp_discovery.py
def test_discover_claude_desktop_config():
def test_discover_cursor_config():
def test_parse_mcp_config_with_env_vars():
def test_technology_detection():
def test_context_file_generation():

# tests/test_template.py
def test_template_extraction():
def test_deep_merge_json():
def test_vscode_settings_merge():
```

### 3. Error Handling Consistency (Priority: Medium)

**Problem:** Mixed error handling patterns:

```python
# Pattern 1: Silent failure
except Exception:
    pass

# Pattern 2: Print warning
except Exception as e:
    print(f"Warning: {e}")

# Pattern 3: Raise exception
except json.JSONDecodeError:
    raise ValueError("Invalid config")
```

**Recommendation:** Implement structured error handling:

```python
# src/specify_cli/errors.py
class SpecifyError(Exception):
    """Base exception for project-specify"""

class SymlinkError(SpecifyError):
    """Symlink creation/verification failed"""

class ConfigError(SpecifyError):
    """Configuration parsing failed"""

class MonorepoError(SpecifyError):
    """Monorepo detection/handling failed"""

class MCPDiscoveryError(SpecifyError):
    """MCP server discovery failed"""
```

### 4. MCP Implementation Redundancy (Priority: Medium)

**Problem:** Both Python (`mcp_discovery.py`) and bash (`discover-mcp.sh`) implementations exist.

**Recommendation:**
1. Make Python implementation primary
2. Remove or deprecate bash script
3. If bash needed for CI/CD, generate it from Python

```python
# src/specify_cli/mcp_discovery.py
def generate_bash_script() -> str:
    """Generate bash script from Python implementation"""
    # Ensures single source of truth
```

### 5. Windows Support (Priority: Medium)

**Problem:** Symlink creation requires admin privileges or Developer Mode.

**Recommendations:**

1. **Add `--copy` fallback flag:**
```python
@app.command()
def init(
    copy_commands: bool = typer.Option(
        False, 
        "--copy", 
        help="Copy commands instead of symlinking (Windows fallback)"
    ),
):
```

2. **Improve error messages:**
```python
if not _check_windows_symlink_capability():
    console.print("""
    [yellow]Windows Symlink Support Required[/yellow]
    
    To create symlinks on Windows, enable one of:
    
    1. Developer Mode:
       Settings → Update & Security → For developers → Developer Mode
    
    2. Run as Administrator
    
    Or use --copy flag to copy commands instead of symlinking.
    """)
```

3. **Add documentation** in README for Windows users.

### 6. Placeholder URLs (Priority: Low)

**Problem:** Multiple files contain `YOUR_USERNAME` placeholders.

**Recommendation:** Create a configuration mechanism:

```python
# src/specify_cli/config.py
FORK_CONFIG = {
    "github_username": "YOUR_USERNAME",  # Set during installation
    "repo_name": "project-specify",
}

# Or use environment variable
import os
GITHUB_USERNAME = os.environ.get("SPECIFY_GITHUB_USERNAME", "YOUR_USERNAME")
```

### 7. MCP Runtime Validation (Priority: Low)

**Problem:** Commands reference MCP servers that may not exist.

**Recommendation:** Add validation before MCP-aware suggestions:

```python
def get_available_mcp_operations(project_dir: Path) -> dict:
    """Return only operations available with current MCP configuration"""
    servers = discover_mcp_servers(project_dir)
    server_names = {s.name for s in servers}
    
    operations = {}
    if "postgres" in server_names or "sqlite" in server_names:
        operations["database"] = ["query", "describe_table"]
    if "git" in server_names:
        operations["git"] = ["status", "diff", "commit"]
    # ...
    return operations
```

---

## Detailed Recommendations

### Recommendation 1: Module Refactoring

**Effort:** 2-3 days  
**Impact:** High (maintainability, testability)

Split `__init__.py` into focused modules:

```
src/specify_cli/
├── __init__.py              # Package exports only
├── main.py                  # Entry point
├── cli.py                   # Typer app and command registration
├── commands/
│   ├── __init__.py
│   ├── init.py              # init command
│   ├── check.py             # check command
│   ├── discover.py          # discover command
│   └── status.py            # status command
├── core/
│   ├── __init__.py
│   ├── config.py            # AGENT_CONFIG, constants
│   ├── errors.py            # Custom exceptions
│   ├── tracker.py           # StepTracker class
│   └── template.py          # Template operations
├── symlink_manager.py       # Already clean
├── monorepo.py              # Already clean
└── mcp_discovery.py         # Already clean
```

### Recommendation 2: Comprehensive Test Suite

**Effort:** 3-5 days  
**Impact:** High (reliability, confidence in changes)

Implement pytest-based test suite:

```python
# tests/conftest.py
import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_central_install(temp_project):
    central = temp_project / ".project-specify"
    central.mkdir()
    (central / "agents/claude/commands").mkdir(parents=True)
    return central

# tests/test_symlinks.py
def test_create_symlink_success(temp_project, mock_central_install, monkeypatch):
    monkeypatch.setattr("specify_cli.symlink_manager.CENTRAL_DIR", mock_central_install)
    
    result = create_agent_symlinks(temp_project, ["claude"])
    
    assert result["claude"] == True
    assert (temp_project / ".claude/commands").is_symlink()
```

### Recommendation 3: CI/CD Pipeline

**Effort:** 1 day  
**Impact:** Medium (quality assurance)

Add GitHub Actions workflow:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run tests
        run: pytest -v --cov=specify_cli
      
      - name: Run linting
        run: |
          ruff check .
          black --check .
```

### Recommendation 4: Documentation Improvements

**Effort:** 1-2 days  
**Impact:** Medium (user experience)

1. **Windows Setup Guide:**
    - Developer Mode enabling
    - Admin installation option
    - `--copy` fallback explanation

2. **MCP Configuration Guide:**
    - How to set up MCP servers
    - Which servers benefit which workflows
    - Troubleshooting connection issues

3. **Monorepo Usage Guide:**
    - Per-workspace initialization
    - Shared vs. workspace-specific specs

### Recommendation 5: Version Management

**Effort:** 0.5 days  
**Impact:** Low (developer experience)

Implement proper version tracking:

```python
# src/specify_cli/_version.py
__version__ = "0.1.0"

# Or use dynamic versioning with hatch-vcs
# pyproject.toml
[tool.hatch.version]
source = "vcs"
```

---

## Implementation Priority Matrix

| Priority | Recommendation | Effort | Impact | Dependencies |
|----------|---------------|--------|--------|--------------|
| 1 | Test Suite | 3-5d | High | None |
| 2 | Module Refactoring | 2-3d | High | Tests first |
| 3 | Error Handling | 1d | Medium | Refactoring |
| 4 | CI/CD Pipeline | 1d | Medium | Tests |
| 5 | Windows Improvements | 1d | Medium | None |
| 6 | Documentation | 1-2d | Medium | None |
| 7 | MCP Cleanup | 0.5d | Low | None |
| 8 | Version Management | 0.5d | Low | None |

---

## Conclusion

This is a well-designed refactoring of spec-kit that adds significant value through its project-centric approach, monorepo support, and MCP integration. The symlink architecture is particularly elegant.

**Immediate priorities should be:**
1. Adding comprehensive tests before making structural changes
2. Refactoring the monolithic `__init__.py` for maintainability
3. Improving Windows support for broader adoption

The codebase is production-ready for its current use case but would benefit from the recommended improvements before wider distribution or team adoption.

---

## Appendix: File Inventory

### Core Python Modules

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| `__init__.py` | ~1400 | Main CLI + utilities | Needs refactoring |
| `symlink_manager.py` | ~250 | Symlink operations | Clean |
| `monorepo.py` | ~150 | Monorepo detection | Clean |
| `mcp_discovery.py` | ~400 | MCP server discovery | Clean |

### Agent Command Files

Each of the 18+ agents has a `commands/` directory with these files:
- `speckit.constitution.md`
- `speckit.specify.md`
- `speckit.plan.md`
- `speckit.tasks.md`
- `speckit.implement.md`
- `speckit.clarify.md`
- `speckit.analyze.md`
- `speckit.checklist.md`

### Templates

| Template | Purpose |
|----------|---------|
| `spec-template.md` | Feature specification |
| `plan-template.md` | Implementation plan |
| `tasks-template.md` | Task breakdown |
| `checklist-template.md` | Quality checklists |
| `implementation-plan-template.md` | MCP-aware planning |

### Scripts

| Script | Purpose |
|--------|---------|
| `discover-mcp.sh` | MCP discovery (bash) |
| `setup-plan.sh` | Plan initialization |
| `create-new-feature.sh` | Feature branch setup |
| `update-agent-context.sh` | Agent context updates |
| `check-prerequisites.sh` | Tool validation |