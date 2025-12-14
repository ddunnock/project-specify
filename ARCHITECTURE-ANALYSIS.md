# Spec-Kit Architecture Analysis

## Executive Summary

**Specify CLI** is a Python-based bootstrapping tool for the **GitHub Spec Kit** framework. It downloads agent-specific templates from GitHub releases and initializes projects with Spec-Driven Development (SDD) workflow support. The CLI is a single-file Python script that uses Typer for command-line interfaces and Rich for interactive TUI.

**Key Insight**: This is NOT a traditional CLI application. It's a **project template installer** that:
1. Downloads pre-packaged templates from GitHub releases (not a template engine)
2. Extracts them into new or existing directories
3. Provides agent-specific slash commands for 18+ AI assistants
4. Uses bash/PowerShell scripts for workflow automation

---

## CLI Structure

### Entry Point
- **File**: `src/specify_cli/__init__.py` (1369 lines, single-file architecture)
- **Package**: `specify-cli` (version 0.0.22)
- **Commands**: `init`, `check`, `version`
- **Runtime**: Python 3.11+, uses `uv` for execution (`uvx` or `uv tool install`)

### Single-File Design Rationale
The entire CLI is a single Python file that can be:
- Executed directly via `uvx` without installation
- Installed globally via `uv tool install`
- Embedded in PEP 723 script metadata for dependency management

This design eliminates packaging complexity and provides instant execution.

---

## Core Architecture Components

### 1. Agent Configuration System (`AGENT_CONFIG`)

**Location**: Lines 126-229 in `__init__.py`

**Design**: Dictionary-based configuration serving as **single source of truth** for all agent metadata.

```python
AGENT_CONFIG = {
    "agent-key": {  # MUST match actual CLI tool name
        "name": "Display Name",
        "folder": ".agent-folder/",
        "install_url": "https://..." or None,
        "requires_cli": True/False
    }
}
```

**18 Supported Agents**:
- **CLI-based** (12): claude, gemini, cursor-agent, qwen, opencode, codex, auggie, codebuddy, qoder, q, amp, shai
- **IDE-based** (6): copilot, windsurf, kilocode, roo, bob (no CLI tool checks)

**Critical Design Decision**: Agent keys MUST match actual executable names (e.g., `"cursor-agent"` not `"cursor"`) to eliminate special-case mappings in tool checking logic.

### 2. Template Download & Distribution System

**GitHub Release Workflow**:
```
1. GitHub repo: github/spec-kit
2. Release assets: spec-kit-template-{agent}-{script}.zip
3. CLI downloads latest via GitHub API
4. Extracts to project directory
```

**Key Functions**:
- `download_template_from_github()` (lines 637-749): Fetches release metadata, validates assets, handles rate limiting
- `download_and_extract_template()` (lines 751-898): Downloads, extracts, handles directory flattening
- Rate limit detection with detailed error messages (lines 68-123)

**Agent × Script Matrix**:
- Each agent has **TWO** template packages: `-sh` (bash) and `-ps` (PowerShell)
- Total packages per release: **18 agents × 2 script types = 36 zip files**

### 3. Interactive Selection System

**Technology**: `readchar` library for cross-platform keyboard input

**Components**:
- `StepTracker` class (lines 245-328): Hierarchical step rendering with live updates
- `select_with_arrows()` (lines 350-423): Arrow key navigation for options
- `Live` rendering from Rich library for non-blocking UI updates

**User Flow**:
1. Select AI assistant (if not specified via `--ai`)
2. Select script type (if not specified via `--script`, defaults to OS-appropriate)
3. Live progress display during download/extraction

### 4. Git Integration

**Functions**:
- `is_git_repo()` (lines 515-533): Checks if directory is in git worktree
- `init_git_repo()` (lines 535-568): Initializes repo, stages all files, creates initial commit
- `check_feature_branch()` in `common.sh`: Validates branch naming convention (`###-feature-name`)

**Behavior**:
- Optional (can be disabled with `--no-git`)
- Skipped if existing repo detected
- Supports **non-git workflows** via `SPECIFY_FEATURE` environment variable fallback

---

## Template System

### Template File Structure

**Location**: `templates/` directory

**Core Templates**:
1. **spec-template.md**: Feature specification template
   - User scenarios with **priority ordering** (P1, P2, P3)
   - **Independent testability** requirement for each story
   - Acceptance criteria in Given-When-Then format
   - Functional requirements with NEEDS CLARIFICATION markers
   - Success criteria (measurable outcomes)

2. **plan-template.md**: Implementation plan template
   - Technical context with NEEDS CLARIFICATION markers
   - Constitution Check gates
   - Project structure options (single/web/mobile)
   - Phased execution model (Phase 0: Research, Phase 1: Design, Phase 2: Tasks)

3. **tasks-template.md**: Task breakdown format
4. **checklist-template.md**: Quality validation checklists
5. **agent-file-template.md**: Agent context file template

### Command Templates

**Location**: `templates/commands/` directory

**Command Files**:
- `specify.md`: Baseline specification creation
- `plan.md`: Implementation planning workflow
- `tasks.md`: Task generation
- `implement.md`: Execution guidance
- `analyze.md`: Cross-artifact consistency analysis
- `checklist.md`: Quality checklist generation
- `clarify.md`: Ambiguity resolution
- `constitution.md`: Project principles establishment
- `taskstoissues.md`: Issue tracker integration

**Command File Format** (Markdown with YAML frontmatter):
```yaml
---
description: "Command description"
handoffs:
  - label: "Next Step"
    agent: speckit.next-command
    prompt: "Context for handoff"
scripts:
  sh: scripts/bash/setup-script.sh --json
  ps: scripts/powershell/setup-script.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input
$ARGUMENTS

## Outline
[Command workflow]
```

**Placeholder Substitution**:
- `{SCRIPT}`: Replaced with agent-appropriate script path
- `{AGENT_SCRIPT}`: Replaced with agent context update script
- `__AGENT__`: Replaced with actual agent name
- `$ARGUMENTS`: User input placeholder

---

## Script System

### Bash Scripts (`scripts/bash/`)

**Core Scripts**:
1. **common.sh** (156 lines): Shared functions library
   - `get_repo_root()`: Finds repository root with non-git fallback
   - `get_current_branch()`: Gets branch name with `SPECIFY_FEATURE` env fallback
   - `get_feature_paths()`: Returns all spec-related paths as eval-able string
   - `find_feature_dir_by_prefix()`: Supports multiple branches per spec (e.g., `004-fix-bug`, `004-add-feature` both map to `specs/004-*`)
   - `check_feature_branch()`: Validates `###-` naming convention

2. **setup-plan.sh** (61 lines):
   - Parses `--json` flag for structured output
   - Copies `plan-template.md` to feature directory
   - Returns paths: FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH

3. **create-new-feature.sh**: Feature branch creation workflow

4. **update-agent-context.sh**: Updates agent-specific context files with technology stack

5. **check-prerequisites.sh**: Validates tool availability

### PowerShell Scripts (`scripts/powershell/`)

**Parallel Implementation**: All bash scripts have PowerShell equivalents with identical interfaces

**Design Principle**: Scripts are **self-contained** and can be called independently from any AI agent, not just via Specify CLI.

---

## Current Directory Logic (`--here` and `.`)

### Implementation (lines 985-1025)

**Three Invocation Methods**:
```bash
specify init --here         # Flag-based
specify init .              # Argument-based (converted to --here internally)
specify init project-name   # Traditional new directory
```

**Behavior**:
1. If `project_name == "."`: Set `here = True`, clear `project_name`
2. If `here == True`: 
   - Set `project_name` to current directory name
   - Set `project_path` to current working directory
3. **Safety Check**: Warns if directory non-empty, requires confirmation (unless `--force`)
4. **Merge Strategy**: Uses temporary directory extraction + file-by-file copy
5. **Special Case**: `.vscode/settings.json` gets **deep-merged** instead of overwritten

### Template Extraction Logic (lines 788-898)

**For Current Directory (`is_current_dir=True`)**:
```python
1. Extract to temporary directory
2. Flatten nested structure if needed
3. Copy/merge files one-by-one:
   - Directories: Merge with existing
   - Files: Overwrite (except settings.json)
   - .vscode/settings.json: Deep merge JSON
```

**For New Directory (`is_current_dir=False`)**:
```python
1. Create new directory
2. Extract directly to target
3. Flatten if extracted to single nested directory
```

---

## Agent-Specific File Generation

### How Commands Are Generated

**NOT DONE BY SPECIFY CLI**: The CLI does NOT generate command files. It downloads pre-built packages from GitHub releases.

**Actual Generation**:
1. GitHub release scripts (`create-release-packages.sh`) generate templates
2. For each agent+script combination, a ZIP is created
3. ZIP contains:
   - Agent folder (e.g., `.claude/commands/`)
   - Command files with placeholders replaced
   - Scripts directory (`.specify/scripts/`)
   - Template files (`.specify/templates/`)
   - Memory directory (`/memory/`)

**Agent-Specific Variations**:

| Agent Type | Directory Pattern | File Format | Argument Style |
|------------|------------------|-------------|----------------|
| Claude | `.claude/commands/` | Markdown | `$ARGUMENTS` |
| Gemini | `.gemini/commands/` | TOML | `{{args}}` |
| Copilot | `.github/agents/` | Markdown | `$ARGUMENTS` |
| Cursor | `.cursor/commands/` | Markdown | `$ARGUMENTS` |
| Windsurf | `.windsurf/workflows/` | Markdown | `$ARGUMENTS` |
| Amp | `.agents/commands/` | Markdown | `$ARGUMENTS` |

---

## Key Functions to Understand

### 1. `init()` Command (lines 945-1241)

**Purpose**: Main command that orchestrates entire initialization

**Workflow**:
```
1. Parse arguments (project_name, ai_assistant, script_type)
2. Validate options and check for conflicts
3. Detect git availability
4. Interactive selection (if not provided via flags)
5. Agent CLI tool validation (if requires_cli=True)
6. Create StepTracker for live progress
7. Download & extract template
8. Set script execute permissions (Unix only)
9. Initialize git repo (if enabled and not existing)
10. Display next steps and enhancement commands
```

**Key Parameters**:
- `--here`: Initialize in current directory
- `--force`: Skip confirmation for non-empty directory
- `--ignore-agent-tools`: Bypass CLI tool checks
- `--no-git`: Skip git initialization
- `--skip-tls`: Disable SSL verification (not recommended)
- `--debug`: Verbose diagnostic output
- `--github-token`: GitHub API authentication (rate limit increase: 60/hr → 5000/hr)

### 2. `download_and_extract_template()` (lines 751-898)

**Critical Function**: Handles template acquisition and directory merging

**Features**:
- Progress tracking via StepTracker
- Temporary directory for current-dir merging
- Nested directory flattening
- .vscode/settings.json deep merge
- Cleanup of temporary files

### 3. `ensure_executable_scripts()` (lines 901-944)

**Purpose**: Recursively set execute permissions on bash scripts

**Logic**:
```python
1. Skip on Windows (os.name == "nt")
2. Find all .sh files in .specify/scripts/
3. Check if file starts with shebang (#!)
4. Add execute bits based on read bits
5. Track updated/failed scripts
```

**Permission Strategy**:
- If readable by owner → make executable by owner
- If readable by group → make executable by group
- If readable by others → make executable by others
- Always ensure owner execute bit is set

### 4. `get_feature_paths()` in common.sh (lines 127-152)

**Purpose**: Central function for all spec-related path resolution

**Returns**:
```bash
REPO_ROOT='/absolute/path'
CURRENT_BRANCH='001-feature-name'
HAS_GIT='true/false'
FEATURE_DIR='/absolute/path/specs/001-feature-name'
FEATURE_SPEC='/absolute/path/specs/001-feature-name/spec.md'
IMPL_PLAN='/absolute/path/specs/001-feature-name/plan.md'
TASKS='/absolute/path/specs/001-feature-name/tasks.md'
RESEARCH='/absolute/path/specs/001-feature-name/research.md'
DATA_MODEL='/absolute/path/specs/001-feature-name/data-model.md'
QUICKSTART='/absolute/path/specs/001-feature-name/quickstart.md'
CONTRACTS_DIR='/absolute/path/specs/001-feature-name/contracts'
```

**Usage in Commands**:
```bash
eval $(get_feature_paths)
# Now all variables are available
```

---

## Non-Git Workflow Support

### Design Philosophy
Spec Kit DOES NOT require git. All scripts support non-git repositories.

### Fallback Mechanisms

**Branch Name Resolution** (priority order):
1. `SPECIFY_FEATURE` environment variable
2. `git rev-parse --abbrev-ref HEAD` (if git available)
3. Latest numbered directory in `specs/` (e.g., highest `###-` prefix)
4. `"main"` as final fallback

**Feature Directory Resolution**:
- **With Git**: Use branch name directly
- **Without Git**: Search `specs/` for directories matching numeric prefix

**Validation**:
- **With Git**: Enforce `###-feature-name` branch naming
- **Without Git**: Warning message, continue without validation

---

## File Organization and Naming Conventions

### Project Structure After `init`

```
my-project/
├── .specify/
│   ├── scripts/
│   │   ├── bash/          # Bash workflow scripts
│   │   └── powershell/    # PowerShell equivalents
│   └── templates/
│       ├── spec-template.md
│       ├── plan-template.md
│       ├── tasks-template.md
│       ├── checklist-template.md
│       ├── agent-file-template.md
│       └── commands/       # Command workflow templates
├── .{agent}/              # Agent-specific directory (e.g., .claude/)
│   └── commands/          # or workflows/, rules/, prompts/, etc.
│       ├── speckit.constitution.md
│       ├── speckit.specify.md
│       ├── speckit.plan.md
│       ├── speckit.tasks.md
│       ├── speckit.implement.md
│       ├── speckit.analyze.md
│       ├── speckit.checklist.md
│       ├── speckit.clarify.md
│       └── speckit.taskstoissues.md
├── memory/
│   └── constitution.md     # Project principles
├── specs/                  # Feature specifications
│   └── 001-feature-name/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md     # Phase 0 output
│       ├── data-model.md   # Phase 1 output
│       ├── quickstart.md   # Phase 1 output
│       ├── contracts/      # Phase 1 output
│       └── tasks.md        # Phase 2 output
├── spec-driven.md          # SDD methodology overview
├── .gitignore
└── README.md
```

### Naming Conventions

**Branch/Feature Naming**: `###-descriptive-name`
- First 3 digits: Feature number (e.g., `001`, `002`, `003`)
- Hyphen separator
- Descriptive slug (lowercase, hyphens)
- **Examples**: `001-user-auth`, `042-api-versioning`, `100-performance-tuning`

**Spec Directory**: Maps to numeric prefix (not exact branch name)
- Allows multiple branches per spec
- **Example**: `004-fix-bug` and `004-add-test` both use `specs/004-*/`

---

## Agent Context Update System

### Purpose
Maintains agent-specific context files with current technology stack and project conventions.

### Files Updated
Each agent has a context file that gets updated during planning:
- Claude: `.claude/rules/specify-rules.md`
- Cursor: `.cursor/rules/specify-rules.md`
- Gemini: `.gemini/rules/specify-rules.md`
- etc.

### Update Mechanism

**Invocation**: Called during Phase 1 of `/speckit.plan` command

**Script**: `scripts/bash/update-agent-context.sh __AGENT__`

**Behavior**:
1. Detects agent type (from argument or auto-detect)
2. Reads current technology stack from plan
3. Updates agent context file
4. Preserves manual additions between `<!-- BEGIN ... -->` and `<!-- END ... -->` markers

---

## Security Considerations

### Agent Folder Security Notice

**Displayed After Init** (lines 1186-1198):
```
Some agents may store credentials, auth tokens, or other identifying
and private artifacts in the agent folder within your project.

Consider adding {agent_folder} to .gitignore to prevent accidental
credential leakage.
```

### SSL/TLS Verification

**Default**: Uses `truststore` library for system certificate verification

**Override**: `--skip-tls` flag disables verification (not recommended)

### GitHub Token Handling

**Sources** (priority order):
1. `--github-token` CLI argument
2. `GH_TOKEN` environment variable
3. `GITHUB_TOKEN` environment variable

**Rate Limits**:
- Unauthenticated: 60 requests/hour
- Authenticated: 5,000 requests/hour

**Error Messages**: Detailed rate limit information with troubleshooting tips (lines 96-123)

---

## Codex-Specific Features

### Environment Variable Setup

**Special Case** (lines 1208-1218): Codex agent requires `CODEX_HOME` environment variable

**Platform-Specific Commands**:
- **Windows**: `setx CODEX_HOME "C:\path\to\.codex"`
- **Unix**: `export CODEX_HOME=/path/to/.codex`

**Displayed in Next Steps**: Automatic instruction generation after project initialization

---

## VS Code Settings Merge Logic

### Deep Merge Strategy (lines 594-635)

**Purpose**: Prevent overwriting user's custom VS Code settings

**Algorithm**:
```python
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
```

**Behavior**:
- New keys → Added
- Existing keys with dict values → Recursively merged
- Existing keys with non-dict values → Replaced
- Lists and primitives → Replaced (not merged)

---

## Testing Strategy

### Built-in Tool Checking

**`check` Command** (lines 1243-1283):
- Validates git installation
- Checks all 18 agent CLI tools (where applicable)
- Tests VS Code variants (`code`, `code-insiders`)
- Uses StepTracker for live progress display

**Tool Detection Logic** (lines 484-513):
```python
def check_tool(tool: str, tracker: StepTracker = None) -> bool:
    # Special case for Claude CLI after migrate-installer
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists():  # ~/.claude/local/claude
            return True
    
    # Standard PATH lookup
    found = shutil.which(tool) is not None
    return found
```

**Claude Special Case**: After running `claude migrate-installer`, the original executable is removed from PATH and replaced with an alias at `~/.claude/local/claude`

---

## Version Management

### Version Command (lines 1285-1362)

**Information Displayed**:
- CLI version (from package metadata or pyproject.toml)
- Latest template version (from GitHub API)
- Release date
- Python version
- Platform information
- OS version
- Architecture

**GitHub API Integration**: Fetches latest release tag from `github/spec-kit` repository

---

## Error Handling and Debugging

### Debug Mode (`--debug` flag)

**Features**:
- Extended error messages
- Environment information display
- HTTP response body snippets (truncated)
- Network diagnostic output

**Environment Context** (lines 1152-1159):
```python
_env_pairs = [
    ("Python", sys.version.split()[0]),
    ("Platform", sys.platform),
    ("CWD", str(Path.cwd())),
]
```

### Rate Limit Error Formatting (lines 96-123)

**Detailed Information**:
- HTTP status code
- Rate limit quota
- Remaining requests
- Reset time (with timezone conversion)
- Retry-After header
- Troubleshooting guidance

---

## Future Extension Points

### Adding New Agents

**Required Changes** (per AGENTS.md):
1. Add to `AGENT_CONFIG` dictionary
2. Update CLI help text in `init()` command
3. Update release package generation scripts
4. Update agent context update scripts (bash + PowerShell)
5. Update README documentation

**Automatic Behaviors** (no code changes):
- Tool checking (if `requires_cli: True`)
- Interactive selection menu
- Template download (if release packages exist)

### Adding New Commands

**Required Changes**:
1. Create command template in `templates/commands/{name}.md`
2. Add to release package generation
3. Agents will automatically receive command after re-init

---

## Dependencies

### Core Runtime Dependencies
```toml
typer          # CLI framework
rich           # Terminal UI
httpx[socks]   # HTTP client with SOCKS proxy support
platformdirs   # Cross-platform directory paths
readchar       # Cross-platform keyboard input
truststore     # System certificate store integration
```

### Why These Dependencies?

- **Typer**: Type-safe CLI with automatic help generation
- **Rich**: Modern terminal UI with live updates
- **httpx**: Async-capable HTTP with streaming support
- **readchar**: Non-blocking keyboard input for arrow navigation
- **truststore**: Handles SSL certificates across platforms

---

## Critical Design Decisions

### 1. Single-File Architecture
**Why**: Enables `uvx` execution without installation, simplifies distribution

### 2. Template as Release Assets
**Why**: Separates CLI code from template content, enables versioning

### 3. Agent Key = CLI Tool Name
**Why**: Eliminates special-case mappings in tool checking

### 4. Prefix-Based Feature Directory Resolution
**Why**: Allows multiple branches per feature spec (e.g., bug fixes, tests)

### 5. Deep Merge for VS Code Settings
**Why**: Preserves user customizations while adding new settings

### 6. Non-Git Workflow Support
**Why**: Enables usage in environments without git (e.g., restricted networks)

### 7. Dual Script System (Bash + PowerShell)
**Why**: Cross-platform support without Python dependencies in scripts

### 8. Live Progress UI with StepTracker
**Why**: Modern UX with non-blocking updates during long operations

---

## Workflow Execution Model

### Spec-Driven Development Phases

**Phase 0: Constitution & Specification**
```
/speckit.constitution → memory/constitution.md
/speckit.specify → specs/###-feature/spec.md
```

**Phase 1: Planning**
```
/speckit.plan → specs/###-feature/plan.md
              → specs/###-feature/research.md
              → specs/###-feature/data-model.md
              → specs/###-feature/quickstart.md
              → specs/###-feature/contracts/
```

**Phase 2: Task Generation**
```
/speckit.tasks → specs/###-feature/tasks.md
```

**Phase 3: Implementation**
```
/speckit.implement → (guided development)
```

**Enhancement Commands** (optional):
```
/speckit.clarify    → De-risk ambiguities before planning
/speckit.analyze    → Validate cross-artifact consistency
/speckit.checklist  → Generate quality checklists
```

---

## Key Takeaways for Modification

1. **Agent Addition**: Update `AGENT_CONFIG`, release scripts, and agent context scripts
2. **Command Addition**: Create template, update release packages
3. **Script Modification**: Update BOTH bash and PowerShell versions
4. **Template Changes**: Modify in templates repo, release new version
5. **CLI Logic Changes**: Single file modification (`src/specify_cli/__init__.py`)
6. **Path Resolution**: All paths flow through `get_feature_paths()` in common.sh
7. **Tool Checking**: Flows through `check_tool()` using `shutil.which()`
8. **Git Optional**: All features must work without git via fallback mechanisms
