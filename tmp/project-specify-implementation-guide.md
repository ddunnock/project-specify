# Project-Specify Implementation Guide

A comprehensive guide for forking GitHub's spec-kit, customizing it for project planning and task management, adding monorepo support, enhanced research capabilities, and distributing it as an installable package.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Phase 1: Repository Setup](#2-phase-1-repository-setup)
3. [Phase 2: Architecture Analysis](#3-phase-2-architecture-analysis)
4. [Phase 3: Core Modifications](#4-phase-3-core-modifications)
5. [Phase 4: Command System (Symlink Architecture)](#5-phase-4-command-system-symlink-architecture)
6. [Phase 5: Template Customization](#6-phase-5-template-customization)
7. [Phase 6: New Capabilities](#7-phase-6-new-capabilities)
8. [Phase 7: Testing & Validation](#8-phase-7-testing--validation)
9. [Phase 8: Package Distribution](#9-phase-8-package-distribution)
10. [Appendix: File Reference](#10-appendix-file-reference)

---

## 1. Project Overview

### 1.1 Goals

Transform GitHub's spec-kit into `project-specify` with these enhancements:

| Original (spec-kit) | Modified (project-specify) |
|---------------------|----------------------------|
| Feature-driven specifications | Project plan & task-driven specifications |
| Single AI agent per project | All AI agents simultaneously (`--ai all`) |
| Commands duplicated per project | Symlinked commands from central installation |
| Feature-focused templates | Project planning templates with milestones |
| Basic implementation workflow | Enhanced research & codebase scanning |
| Single-package projects | Monorepo/workspace support |

### 1.2 Target Command Interface

```bash
# Install once globally
uv tool install project-specify-cli --from git+https://github.com/YOUR_USERNAME/project-specify.git

# Initialize in any repo with all AI IDE support
project-specify init . --ai all

# Multiple specific agents (Typer style - multiple flags)
project-specify init . --ai claude --ai cursor --ai copilot

# Also supports comma-separated
project-specify init . --ai claude,cursor,copilot

# Monorepo support
project-specify init . --ai all --workspace packages/core
```

### 1.3 Symlink Architecture Overview

```
~/.project-specify/                    # Central installation (your fork)
├── agents/
│   ├── claude/commands/               # Slash commands for Claude Code
│   ├── cursor/commands/               # Slash commands for Cursor
│   ├── copilot/commands/              # Slash commands for Copilot
│   ├── windsurf/commands/             # Slash commands for Windsurf
│   └── .../                           # All other agents
└── version.txt                        # For update detection

~/any-project/
├── .claude/commands -> ~/.project-specify/agents/claude/commands
├── .cursor/commands -> ~/.project-specify/agents/cursor/commands
├── .github/copilot-instructions.md -> ~/.project-specify/agents/copilot/...
├── .specify/                          # Generated fresh (NOT symlinked)
│   ├── memory/constitution.md         # Project-specific
│   ├── scripts/                       # Helper scripts
│   ├── specs/                         # Project specifications
│   └── templates/                     # Spec templates
└── PROJECT-SPECIFY.md                 # Project-level agent instructions
```

---

## 2. Phase 1: Repository Setup

### 2.1 Fork the Repository

```bash
# Navigate to https://github.com/github/spec-kit
# Click "Fork" button in upper right
# Select your account as destination
# Uncheck "Copy the main branch only" to get all branches/tags
```

### 2.2 Clone Your Fork Locally

```bash
cd ~/repos  # or your preferred location
git clone https://github.com/YOUR_USERNAME/spec-kit.git project-specify
cd project-specify

# Add upstream remote for syncing updates
git remote add upstream https://github.com/github/spec-kit.git

# Verify remotes
git remote -v
# origin    https://github.com/YOUR_USERNAME/spec-kit.git (fetch)
# origin    https://github.com/YOUR_USERNAME/spec-kit.git (push)
# upstream  https://github.com/github/spec-kit.git (fetch)
# upstream  https://github.com/github/spec-kit.git (push)
```

### 2.3 Create Development Branch

```bash
git checkout -b feature/project-specify-customization
```

### 2.4 Rename Repository (Optional but Recommended)

On GitHub:
1. Go to repository Settings
2. Under "General", find "Repository name"
3. Change from `spec-kit` to `project-specify`
4. Update local remote:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/project-specify.git
```

---

## 3. Phase 2: Architecture Analysis

Before modifying, systematically examine the existing structure.

### 3.1 Directory Structure Inspection

```bash
# Get complete tree structure
find . -type f -name "*.py" -o -name "*.md" -o -name "*.sh" -o -name "*.ps1" | \
  grep -v __pycache__ | grep -v .git | sort

# Expected key paths:
# ./src/specify_cli/main.py          - CLI entry point
# ./src/specify_cli/__init__.py      - Package init
# ./pyproject.toml                   - Package configuration
# ./templates/                       - Spec templates
# ./scripts/                         - Helper scripts (sh/ps1)
# ./base/                            - Base agent configurations
```

### 3.2 CLI Analysis Checklist

Examine `src/specify_cli/main.py` and document:

- [ ] How `--ai` argument is parsed and validated
- [ ] Where agent-specific files are determined
- [ ] How templates are fetched (GitHub releases vs local)
- [ ] Where files are written during `init`
- [ ] How `--here` and `.` current directory logic works
- [ ] Git initialization logic

### 3.3 Template Analysis Checklist

Examine files in `templates/`:

- [ ] `spec-template.md` - What sections exist? What's feature-specific?
- [ ] `plan-template.md` - Technical planning structure
- [ ] `tasks-template.md` - Task breakdown format
- [ ] Any agent-specific template variations

### 3.4 Agent Configuration Analysis

For each supported agent, document:

- [ ] Where slash commands are stored
- [ ] File naming conventions
- [ ] How commands reference scripts
- [ ] Any agent-specific quirks

```bash
# Find all agent-related directories
find . -type d -name "*claude*" -o -name "*cursor*" -o -name "*copilot*" \
  -o -name "*gemini*" -o -name "*windsurf*" 2>/dev/null
```

### 3.5 Create Analysis Document

```bash
# Create a findings document as you analyze
cat > ARCHITECTURE-ANALYSIS.md << 'EOF'
# Spec-Kit Architecture Analysis

## CLI Structure
- Entry point: `src/specify_cli/main.py`
- [Document findings here]

## Template System
- Location: `templates/`
- [Document template structure]

## Agent Configurations
- Claude: [path and structure]
- Cursor: [path and structure]
- [Continue for each agent]

## Key Functions to Modify
1. [Function name] - [purpose] - [modification needed]
2. [Continue listing]
EOF
```

---

## 4. Phase 3: Core Modifications

### 4.1 Rename Package and Entry Point

**File: `pyproject.toml`**

```toml
[project]
name = "project-specify-cli"
version = "1.0.0"
description = "Project planning toolkit with spec-driven development for all AI IDEs"
# ... rest of metadata

[project.scripts]
project-specify = "specify_cli.main:main"
# Keep original for backwards compatibility if desired
# specify = "specify_cli.main:main"

[project.urls]
Homepage = "https://github.com/YOUR_USERNAME/project-specify"
Documentation = "https://github.com/YOUR_USERNAME/project-specify#readme"
Repository = "https://github.com/YOUR_USERNAME/project-specify.git"
```

### 4.2 Extend AI Agent Support

**File: `src/specify_cli/main.py`**

The original spec-kit uses **Typer** (not argparse). Add support for `--ai all` and multiple `--ai` flags:

```python
from typing import List, Optional
import typer
from .symlink_manager import parse_ai_argument, SUPPORTED_AGENTS

app = typer.Typer()

def parse_ai_callback(value: List[str]) -> List[str]:
    """
    Callback to parse --ai values, supporting multiple formats:
    - Multiple flags: --ai claude --ai cursor
    - Comma-separated: --ai claude,cursor,copilot
    - All agents: --ai all
    """
    if not value:
        return ["claude"]  # Default
    return parse_ai_argument(value)

@app.command()
def init(
    project_name: Optional[str] = typer.Argument(None),
    ai: List[str] = typer.Option(
        ["claude"],
        "--ai",
        help="AI agents to set up. Use multiple times or 'all'.",
        callback=parse_ai_callback,
    ),
    here: bool = typer.Option(False, "--here"),
    force: bool = typer.Option(False, "--force"),
    no_git: bool = typer.Option(False, "--no-git"),
):
    """Initialize a new project-specify project."""
    # ai is already parsed by callback
    agents = ai
    # ... rest of init logic
```

**Usage Examples:**
```bash
# Single agent (default)
project-specify init my-project

# Multiple agents (Typer style - multiple flags)
project-specify init my-project --ai claude --ai cursor --ai copilot

# Multiple agents (comma-separated)
project-specify init my-project --ai claude,cursor,copilot

# All supported agents
project-specify init my-project --ai all

# Current directory with all agents
project-specify init . --ai all
project-specify init --here --ai all
```

**Note:** Typer's `List[str]` option type requires multiple `--ai` flags by default. The `parse_ai_callback` function extends this to also support comma-separated values and the `all` keyword, giving users flexibility in how they specify agents.

### 4.3 Add Symlink Manager Module

**File: `src/specify_cli/symlink_manager.py`**

```python
"""
Symlink Manager for project-specify

Handles creation and management of symlinks from project directories
to the central ~/.project-specify installation.
"""

import os
import shutil
from pathlib import Path
from typing import Optional

# Central installation location
CENTRAL_DIR = Path.home() / ".project-specify"
AGENTS_DIR = CENTRAL_DIR / "agents"

# Agent directory mappings
AGENT_PATHS = {
    "claude": {
        "source": "claude/commands",
        "target": ".claude/commands",
    },
    "cursor": {
        "source": "cursor/commands",
        "target": ".cursor/commands",
    },
    "copilot": {
        "source": "copilot",
        "target": ".github",
        "files": ["copilot-instructions.md"],  # Specific files, not whole dir
    },
    "gemini": {
        "source": "gemini",
        "target": ".",
        "files": ["GEMINI.md"],
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
}


def ensure_central_installation(force_update: bool = False) -> bool:
    """
    Ensure the central ~/.project-specify directory exists with current commands.
    
    Returns True if installation was created/updated, False if already current.
    """
    if CENTRAL_DIR.exists() and not force_update:
        # Check version to see if update needed
        version_file = CENTRAL_DIR / "version.txt"
        if version_file.exists():
            # TODO: Compare with package version
            return False
    
    # Create or update central installation
    CENTRAL_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(exist_ok=True)
    
    # Copy agent commands from package resources
    # This will be populated from the package's bundled agents directory
    package_agents = Path(__file__).parent / "agents"
    if package_agents.exists():
        shutil.copytree(package_agents, AGENTS_DIR, dirs_exist_ok=True)
    
    return True


def create_agent_symlinks(
    project_dir: Path,
    agents: list[str],
    force: bool = False,
) -> dict[str, bool]:
    """
    Create symlinks from project directory to central installation.
    
    Args:
        project_dir: The project directory to set up
        agents: List of agent names to create symlinks for
        force: If True, overwrite existing files/symlinks
        
    Returns:
        Dict mapping agent name to success status
    """
    results = {}
    
    for agent in agents:
        if agent not in AGENT_PATHS:
            results[agent] = False
            continue
            
        config = AGENT_PATHS[agent]
        source = AGENTS_DIR / config["source"]
        target = project_dir / config["target"]
        
        if not source.exists():
            print(f"Warning: Source not found for {agent}: {source}")
            results[agent] = False
            continue
        
        # Handle file-specific symlinks vs directory symlinks
        if "files" in config:
            # Symlink specific files
            target.mkdir(parents=True, exist_ok=True)
            for filename in config["files"]:
                src_file = source / filename
                tgt_file = target / filename
                results[agent] = _create_symlink(src_file, tgt_file, force)
        else:
            # Symlink entire directory
            target.parent.mkdir(parents=True, exist_ok=True)
            results[agent] = _create_symlink(source, target, force)
    
    return results


def _create_symlink(source: Path, target: Path, force: bool) -> bool:
    """Create a single symlink, handling existing files."""
    try:
        if target.exists() or target.is_symlink():
            if force:
                if target.is_dir() and not target.is_symlink():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            else:
                print(f"Skipping {target} (already exists, use --force to overwrite)")
                return False
        
        target.symlink_to(source)
        return True
    except OSError as e:
        print(f"Error creating symlink {target} -> {source}: {e}")
        return False


def verify_symlinks(project_dir: Path, agents: list[str]) -> dict[str, str]:
    """
    Verify symlink status for agents in a project.
    
    Returns dict mapping agent to status: "valid", "broken", "missing", "file"
    """
    status = {}
    
    for agent in agents:
        if agent not in AGENT_PATHS:
            status[agent] = "unknown"
            continue
            
        config = AGENT_PATHS[agent]
        target = project_dir / config["target"]
        
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
```

### 4.4 Modify Main CLI to Use Symlinks

**File: `src/specify_cli/main.py`** (continued modifications)

```python
# Add import at top
from .symlink_manager import (
    ensure_central_installation,
    create_agent_symlinks,
    SUPPORTED_AGENTS,
)

# Modify the init command handler
def handle_init(args):
    """Handle the init command with symlink support."""
    
    # Parse agents
    agents = parse_ai_argument(args.ai) if args.ai else ["claude"]  # Default
    
    # Ensure central installation exists
    ensure_central_installation()
    
    # Determine project directory
    if args.here or args.project_name == ".":
        project_dir = Path.cwd()
    else:
        project_dir = Path.cwd() / args.project_name
        project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create .specify directory structure (NOT symlinked)
    create_specify_structure(project_dir)
    
    # Create agent symlinks
    results = create_agent_symlinks(project_dir, agents, force=args.force)
    
    # Report results
    print(f"\n✅ Initialized project-specify in {project_dir}")
    print(f"\nAgent symlinks created:")
    for agent, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {agent}")
    
    # Git init if requested
    if not args.no_git:
        init_git(project_dir)
```

### 4.5 Add Monorepo Detection

**File: `src/specify_cli/monorepo.py`**

```python
"""
Monorepo detection and workspace support for project-specify.
"""

from pathlib import Path
from typing import Optional
import json
import tomllib


def detect_monorepo_type(project_dir: Path) -> Optional[str]:
    """
    Detect the type of monorepo structure.
    
    Returns: "pnpm", "npm", "yarn", "lerna", "nx", "turborepo", or None
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
            data = json.loads(package_json.read_text())
            if "workspaces" in data:
                return "npm"  # or yarn, they use same format
        except json.JSONDecodeError:
            pass
    
    # Check Cargo.toml for Rust workspaces
    cargo_toml = project_dir / "Cargo.toml"
    if cargo_toml.exists():
        try:
            data = tomllib.loads(cargo_toml.read_text())
            if "workspace" in data:
                return "cargo"
        except tomllib.TOMLDecodeError:
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
    import yaml  # requires pyyaml
    
    workspace_file = project_dir / "pnpm-workspace.yaml"
    if not workspace_file.exists():
        workspace_file = project_dir / "pnpm-workspace.yml"
    
    if not workspace_file.exists():
        return []
    
    try:
        data = yaml.safe_load(workspace_file.read_text())
        patterns = data.get("packages", [])
        return _expand_glob_patterns(project_dir, patterns)
    except Exception:
        return []


def _get_npm_workspaces(project_dir: Path) -> list[Path]:
    """Parse package.json workspaces field."""
    package_json = project_dir / "package.json"
    if not package_json.exists():
        return []
    
    try:
        data = json.loads(package_json.read_text())
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
        data = json.loads(lerna_json.read_text())
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
        data = tomllib.loads(cargo_toml.read_text())
        members = data.get("workspace", {}).get("members", [])
        return _expand_glob_patterns(project_dir, members)
    except Exception:
        return []


def _expand_glob_patterns(base_dir: Path, patterns: list[str]) -> list[Path]:
    """Expand glob patterns to actual directories."""
    from glob import glob
    
    results = []
    for pattern in patterns:
        # Handle negation patterns
        if pattern.startswith("!"):
            continue
        
        matches = glob(str(base_dir / pattern))
        for match in matches:
            path = Path(match)
            if path.is_dir():
                results.append(path)
    
    return sorted(set(results))
```

---

## 5. Phase 4: Command System (Symlink Architecture)

### 5.1 Create Centralized Command Structure

Create the `agents/` directory in your package that will be installed to `~/.project-specify/agents/`:

```bash
mkdir -p src/specify_cli/agents/{claude,cursor,copilot,gemini,windsurf}/commands
```

### 5.2 Core Command Files

Each agent needs these core commands. The content is nearly identical, with minor syntax adjustments per agent.

**File: `src/specify_cli/agents/claude/commands/speckit.constitution.md`**

```markdown
---
description: Create or update project constitution with governing principles
---

# Constitution Creation

Create a project constitution that establishes non-negotiable principles for development.

## Instructions

1. Read the user's requirements for project principles
2. Create or update `.specify/memory/constitution.md`
3. Include sections for:
   - Core Principles
   - Technical Standards
   - Quality Requirements
   - Security Guidelines
   - Testing Requirements

## Template

```markdown
# Project Constitution

## Core Principles
[User-defined principles]

## Technical Standards
- Code style and formatting requirements
- Documentation standards
- Version control practices

## Quality Requirements
- Testing coverage expectations
- Performance benchmarks
- Accessibility standards

## Security Guidelines
- Authentication/authorization requirements
- Data handling policies
- Dependency management

## Testing Requirements
- Unit testing expectations
- Integration testing approach
- E2E testing strategy
```

When complete, confirm the constitution has been created and summarize the key principles established.
```

**File: `src/specify_cli/agents/claude/commands/speckit.specify.md`**

```markdown
---
description: Create project specification from requirements
---

# Project Specification

Transform project requirements into a structured specification document.

## Instructions

1. Read the user's project description
2. Run the feature branch creation script:
   ```bash
   bash .specify/scripts/create-new-feature.sh "<feature-name>"
   ```
3. Create specification in `.specify/specs/<branch-name>/spec.md`
4. Include:
   - Project Overview
   - User Stories (with acceptance criteria)
   - Functional Requirements
   - Non-Functional Requirements
   - Milestones and Deliverables
   - Success Criteria
   - Review Checklist

## Key Principles

- Focus on WHAT and WHY, not HOW
- Mark ambiguities with `[NEEDS CLARIFICATION: question]`
- Each user story should be independently valuable
- Requirements should be testable

## User Story Format

```markdown
### US-001: [Story Title]

**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Priority:** [High/Medium/Low]
**Milestone:** [Milestone name]
```

After creating the spec, summarize the user stories and ask if any clarifications are needed.
```

**File: `src/specify_cli/agents/claude/commands/speckit.plan.md`**

```markdown
---
description: Create technical implementation plan from specification
---

# Technical Planning

Create a comprehensive technical implementation plan based on the specification.

## Instructions

1. Read the current specification from `.specify/specs/<current-branch>/spec.md`
2. Read the constitution from `.specify/memory/constitution.md`
3. Run the plan setup script:
   ```bash
   bash .specify/scripts/setup-plan.sh
   ```
4. Create implementation plan in `.specify/specs/<current-branch>/plan.md`

## Plan Structure

```markdown
# Technical Implementation Plan

## Architecture Overview
[High-level architecture description]

## Technology Stack
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| [Component] | [Tech] | [Why] |

## Component Breakdown

### Component 1: [Name]
- **Purpose:** [Description]
- **Dependencies:** [List]
- **Interfaces:** [API/contracts]

## Data Models
[Entity definitions and relationships]

## API Contracts
[Endpoint specifications]

## Implementation Phases
1. **Phase 1:** [Foundation] - [Timeline estimate]
2. **Phase 2:** [Core features] - [Timeline estimate]
3. **Phase 3:** [Enhancement] - [Timeline estimate]

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

## Dependencies and Prerequisites
- [External dependencies]
- [Required tools/services]
```

## Validation

Before finalizing, verify:
- [ ] All user stories are addressed
- [ ] Architecture aligns with constitution
- [ ] Dependencies are clearly identified
- [ ] Timeline is realistic
```

**File: `src/specify_cli/agents/claude/commands/speckit.tasks.md`**

```markdown
---
description: Generate actionable task breakdown from implementation plan
---

# Task Generation

Break down the implementation plan into specific, actionable tasks.

## Instructions

1. Read the plan from `.specify/specs/<current-branch>/plan.md`
2. Create task breakdown in `.specify/specs/<current-branch>/tasks.md`
3. Organize tasks by user story and implementation phase

## Task Format

```markdown
# Implementation Tasks

## Phase 1: Foundation

### User Story: US-001

#### Task 1.1.1: [Task Title]
- **Description:** [What needs to be done]
- **Files:** [Paths to create/modify]
- **Dependencies:** [Prerequisite tasks]
- **Acceptance:** [How to verify completion]
- **Estimate:** [Time estimate]
- **Parallel:** [Yes/No - can run with other tasks]

#### Task 1.1.2: [Next Task]
...

### Checkpoint: Phase 1 Validation
- [ ] [Verification item 1]
- [ ] [Verification item 2]

## Phase 2: Core Features
...
```

## Task Principles

1. **Atomic:** Each task should be completable in one session
2. **Testable:** Clear acceptance criteria
3. **Ordered:** Respect dependencies
4. **Parallelizable:** Mark tasks that can run concurrently with `[P]`
5. **Sized:** No task should exceed 2-4 hours of work

## Dependency Rules

- Models before services
- Services before endpoints
- Core utilities before consumers
- Tests can be written before or after (based on TDD preference)
```

**File: `src/specify_cli/agents/claude/commands/speckit.implement.md`**

```markdown
---
description: Execute implementation tasks systematically
---

# Implementation Execution

Execute the task breakdown to build the project.

## Instructions

1. Read tasks from `.specify/specs/<current-branch>/tasks.md`
2. Execute tasks in order, respecting dependencies
3. For each task:
   - Announce the task being started
   - Implement the changes
   - Run relevant tests
   - Mark task complete
   - Commit changes with descriptive message

## Execution Protocol

```
For each phase:
  For each user story:
    For each task (respecting dependencies):
      1. Announce: "Starting Task X.Y.Z: [Title]"
      2. Review: Check dependencies are met
      3. Implement: Make the required changes
      4. Validate: Run tests, lint, type-check
      5. Commit: git commit with task reference
      6. Report: "Completed Task X.Y.Z ✅"
    
    Run checkpoint validation
  
  Report phase completion
```

## Error Handling

If a task fails:
1. Report the error clearly
2. Suggest potential fixes
3. Ask user whether to:
   - Retry with modifications
   - Skip and continue
   - Stop implementation

## Progress Tracking

Maintain implementation state:
```markdown
## Implementation Progress

- [x] Task 1.1.1: Setup project structure
- [x] Task 1.1.2: Configure dependencies
- [ ] Task 1.2.1: Create data models (IN PROGRESS)
- [ ] Task 1.2.2: Implement repository layer
```
```

### 5.3 New Custom Commands

**File: `src/specify_cli/agents/claude/commands/speckit.scan.md`**

```markdown
---
description: Scan and analyze existing codebase structure
---

# Codebase Scanner

Analyze an existing codebase to understand its structure, patterns, and conventions.

## Instructions

Execute a comprehensive codebase analysis:

### 1. Project Structure Analysis
```bash
# Get directory tree (excluding common noise)
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" \
  -o -name "*.rs" -o -name "*.java" -o -name "*.cs" \) \
  | grep -v node_modules | grep -v __pycache__ | grep -v .git | grep -v dist \
  | head -100
```

### 2. Dependency Analysis
```bash
# Node.js
cat package.json 2>/dev/null | jq '.dependencies, .devDependencies'

# Python
cat requirements.txt pyproject.toml 2>/dev/null

# Rust
cat Cargo.toml 2>/dev/null

# Go
cat go.mod 2>/dev/null
```

### 3. Pattern Detection

Identify:
- **Architecture:** Monolith, microservices, modular monolith
- **Patterns:** MVC, Clean Architecture, Hexagonal, etc.
- **Testing:** Unit, integration, e2e test structure
- **Code Style:** Naming conventions, file organization

### 4. Generate Report

Create `.specify/scans/codebase-analysis.md`:

```markdown
# Codebase Analysis Report

Generated: [timestamp]

## Project Overview
- **Type:** [Web app, CLI, Library, etc.]
- **Primary Language:** [Language]
- **Framework:** [Framework if applicable]

## Architecture
[Description of architectural patterns]

## Directory Structure
```
[Annotated tree structure]
```

## Key Components
| Component | Location | Purpose |
|-----------|----------|---------|

## Dependencies
### Production
[List key dependencies]

### Development
[List dev dependencies]

## Patterns Identified
- [Pattern 1]: [Where used]
- [Pattern 2]: [Where used]

## Testing Structure
- Unit tests: [Location]
- Integration: [Location]
- E2E: [Location]

## Recommendations
[Suggestions for the project]
```

## When to Use

- Before adding new features to existing projects
- When onboarding to unfamiliar codebases
- Before major refactoring efforts
- To document project for team members
```

**File: `src/specify_cli/agents/claude/commands/speckit.research.md`**

```markdown
---
description: Research technologies, patterns, and best practices for implementation
---

# Research Assistant

Conduct targeted research to inform implementation decisions.

## Instructions

When research is requested:

### 1. Identify Research Topics

From the specification or plan, identify areas needing research:
- New/unfamiliar technologies
- Best practices for specific patterns
- Version-specific API changes
- Performance optimization techniques
- Security considerations

### 2. Conduct Research

For each topic:

```markdown
## Research: [Topic]

### Question
[Specific question to answer]

### Sources Consulted
- [Official documentation]
- [Authoritative guides]
- [Version changelogs]

### Findings
[Detailed findings]

### Recommendations
[Specific recommendations for this project]

### Code Examples
```[language]
[Relevant code examples]
```

### Caveats
- [Version-specific notes]
- [Known issues]
- [Deprecation warnings]
```

### 3. Update Research Document

Append findings to `.specify/specs/<current-branch>/research.md`

### 4. Cross-Reference with Plan

After research:
- Update plan.md with refined technical decisions
- Note any specification changes needed
- Flag potential risks discovered

## Research Types

### Technology Research
- Framework capabilities and limitations
- Library comparison and selection
- API design patterns

### Implementation Research
- Algorithm selection
- Data structure optimization
- Caching strategies

### Integration Research
- Third-party API integration
- Authentication flows
- Data migration approaches

## Quality Criteria

Good research should be:
- **Specific:** Answers concrete questions
- **Current:** Uses up-to-date sources
- **Actionable:** Provides clear recommendations
- **Verified:** Code examples are tested
```

**File: `src/specify_cli/agents/claude/commands/speckit.clarify.md`**

```markdown
---
description: Systematic clarification of underspecified requirements
---

# Structured Clarification

Systematically identify and resolve ambiguities in the specification.

## Instructions

### 1. Scan for Ambiguities

Review the specification for:
- `[NEEDS CLARIFICATION: ...]` markers
- Vague requirements ("should be fast", "user-friendly")
- Missing acceptance criteria
- Undefined edge cases
- Unstated assumptions

### 2. Generate Clarification Questions

For each ambiguity, create a structured question:

```markdown
## Clarification #[N]

**Location:** [Section/User Story reference]
**Current Text:** "[Quoted ambiguous text]"

**Question:** [Specific question]

**Options:**
A. [Option 1]
B. [Option 2]
C. [Other - please specify]

**Default Assumption:** [What we'll assume if not clarified]
**Impact:** [Why this matters for implementation]
```

### 3. Collect Responses

Present questions one at a time or as a batch. Record answers.

### 4. Update Specification

For each clarification received:
1. Remove the `[NEEDS CLARIFICATION]` marker
2. Update the requirement with specific details
3. Add to Clarifications section of spec

```markdown
## Clarifications Log

| # | Question | Answer | Updated Section |
|---|----------|--------|-----------------|
| 1 | [Question] | [Answer] | [Section ref] |
```

## Coverage Areas

Ensure clarification coverage for:

- [ ] User roles and permissions
- [ ] Data validation rules
- [ ] Error handling expectations
- [ ] Performance requirements (specific numbers)
- [ ] Browser/platform support
- [ ] Accessibility requirements
- [ ] Security requirements
- [ ] Integration points
- [ ] Deployment environment
```

### 5.4 Copy Commands for Other Agents

The commands are nearly identical across agents. Create a script to generate them:

**File: `scripts/generate-agent-commands.sh`**

```bash
#!/bin/bash

# Generate command files for all agents based on Claude templates

AGENTS_DIR="src/specify_cli/agents"
CLAUDE_COMMANDS="$AGENTS_DIR/claude/commands"

# Agents that use identical command format
IDENTICAL_AGENTS=(
    "cursor"
    "windsurf"
    "qwen"
    "opencode"
    "codex"
    "kilocode"
    "auggie"
    "roo"
    "codebuddy"
    "amp"
    "shai"
    "qoder"
)

for agent in "${IDENTICAL_AGENTS[@]}"; do
    mkdir -p "$AGENTS_DIR/$agent/commands"
    cp "$CLAUDE_COMMANDS"/*.md "$AGENTS_DIR/$agent/commands/"
    echo "Generated commands for $agent"
done

# Handle special cases
# Copilot uses different structure
mkdir -p "$AGENTS_DIR/copilot"
# Combine commands into copilot-instructions.md format
# ...

# Gemini uses GEMINI.md
mkdir -p "$AGENTS_DIR/gemini"
# Create GEMINI.md with embedded commands
# ...

echo "Command generation complete"
```

---

## 6. Phase 5: Template Customization

### 6.1 Project Plan Template (replaces spec-template)

**File: `src/specify_cli/templates/project-plan-template.md`**

```markdown
# Project Specification: [PROJECT_NAME]

> Generated by project-specify on [DATE]
> Branch: [BRANCH_NAME]

## Executive Summary

[Brief description of the project, its goals, and expected outcomes]

## Project Scope

### In Scope
- [Deliverable 1]
- [Deliverable 2]

### Out of Scope
- [Excluded item 1]
- [Excluded item 2]

### Assumptions
- [Assumption 1]
- [Assumption 2]

## Milestones

| Milestone | Description | Target Date | Dependencies |
|-----------|-------------|-------------|--------------|
| M1 | [Foundation] | [Date] | None |
| M2 | [Core Features] | [Date] | M1 |
| M3 | [Polish & Deploy] | [Date] | M2 |

## User Stories

### Epic: [Epic Name]

#### US-001: [Story Title]

**As a** [user type]
**I want** [capability]  
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Priority:** [High/Medium/Low]
**Milestone:** [M1/M2/M3]
**Story Points:** [Estimate]

[NEEDS CLARIFICATION: Mark any ambiguities here]

---

#### US-002: [Next Story]
...

## Functional Requirements

### FR-001: [Requirement Title]
- **Description:** [Detailed description]
- **Related Stories:** US-001, US-002
- **Validation:** [How to verify]

## Non-Functional Requirements

### Performance
- [Response time requirements]
- [Throughput requirements]
- [Resource constraints]

### Security
- [Authentication requirements]
- [Authorization model]
- [Data protection]

### Reliability
- [Availability targets]
- [Recovery requirements]
- [Backup strategy]

### Scalability
- [Expected load]
- [Growth projections]
- [Scaling approach]

## Success Criteria

| Criterion | Metric | Target |
|-----------|--------|--------|
| [Criterion 1] | [How measured] | [Target value] |

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Strategy] |

## Review Checklist

### Requirements Quality
- [ ] All user stories have acceptance criteria
- [ ] No ambiguous language remains
- [ ] All stakeholders represented
- [ ] Edge cases documented

### Completeness
- [ ] All milestones defined
- [ ] Dependencies identified
- [ ] Success criteria measurable
- [ ] Risks assessed

### Feasibility
- [ ] Technical approach validated
- [ ] Resource requirements estimated
- [ ] Timeline is realistic
- [ ] Constraints are documented
```

### 6.2 Technical Implementation Template

**File: `src/specify_cli/templates/implementation-plan-template.md`**

```markdown
# Technical Implementation Plan

> Project: [PROJECT_NAME]
> Branch: [BRANCH_NAME]
> Created: [DATE]

## Architecture Overview

### System Context
```
[High-level system context diagram - describe components]
```

### Architecture Style
- **Pattern:** [Monolith/Microservices/Serverless/etc.]
- **Rationale:** [Why this approach]

### Key Design Decisions

| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| [Decision 1] | [A, B, C] | [B] | [Why B] |

## Technology Stack

### Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Runtime | [e.g., Node.js] | [20.x] | [Application runtime] |
| Framework | [e.g., Next.js] | [14.x] | [Web framework] |
| Database | [e.g., PostgreSQL] | [16.x] | [Data persistence] |
| Cache | [e.g., Redis] | [7.x] | [Session/cache store] |

### Development Tools

| Tool | Purpose |
|------|---------|
| [Tool 1] | [Purpose] |

## Component Architecture

### Component: [Name]

**Purpose:** [What this component does]

**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]

**Interfaces:**
```typescript
// Define key interfaces
interface [ComponentInterface] {
  // ...
}
```

**Dependencies:**
- [Internal dependency]
- [External dependency]

---

### Component: [Next Component]
...

## Data Architecture

### Entity Relationship

```
[Describe entities and relationships]
```

### Data Models

#### Entity: [Name]

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| [field] | [type] | [constraints] | [description] |

## API Design

### Endpoints Overview

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /api/[resource] | List resources | Required |
| POST | /api/[resource] | Create resource | Required |

### API Contract: [Endpoint]

**Request:**
```json
{
  "field": "type"
}
```

**Response:**
```json
{
  "data": {},
  "meta": {}
}
```

## Implementation Phases

### Phase 1: Foundation (Milestone M1)

**Objectives:**
- [Objective 1]
- [Objective 2]

**Deliverables:**
- [Deliverable 1]
- [Deliverable 2]

**Exit Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Phase 2: Core Features (Milestone M2)
...

### Phase 3: Polish & Deploy (Milestone M3)
...

## Infrastructure

### Development Environment
- [Local setup requirements]
- [Dev dependencies]

### Staging Environment
- [Staging configuration]

### Production Environment
- [Production architecture]
- [Scaling configuration]

## Testing Strategy

### Unit Testing
- **Framework:** [Jest/Vitest/pytest/etc.]
- **Coverage Target:** [80%+]
- **Location:** `[test directory]`

### Integration Testing
- **Approach:** [API testing, DB testing]
- **Tools:** [Supertest, Testcontainers, etc.]

### E2E Testing
- **Framework:** [Playwright/Cypress]
- **Scope:** [Critical user flows]

## Security Considerations

### Authentication
- [Auth mechanism]

### Authorization
- [Authz model]

### Data Protection
- [Encryption approach]
- [PII handling]

## Monitoring & Observability

### Logging
- [Logging approach]

### Metrics
- [Key metrics to track]

### Alerting
- [Alert conditions]

## Dependencies & Prerequisites

### External Services
- [Service 1]: [Purpose]

### Required Credentials
- [Credential 1]: [How to obtain]

### Setup Steps
1. [Step 1]
2. [Step 2]
```

### 6.3 Task Breakdown Template

**File: `src/specify_cli/templates/tasks-template.md`**

```markdown
# Implementation Tasks

> Project: [PROJECT_NAME]
> Branch: [BRANCH_NAME]
> Generated: [DATE]

## Overview

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| Phase 1: Foundation | [N] | [H] |
| Phase 2: Core | [N] | [H] |
| Phase 3: Polish | [N] | [H] |
| **Total** | **[N]** | **[H]** |

## Task Legend

- `[P]` - Can be parallelized with other `[P]` tasks in same group
- `[B]` - Blocking - must complete before dependent tasks
- `[T]` - Requires tests first (TDD)

---

## Phase 1: Foundation

### Setup & Configuration

#### Task 1.0.1: Initialize Project Structure [B]
- **Description:** Create base project structure with tooling
- **Files:**
  - `package.json` (create)
  - `tsconfig.json` (create)
  - `.eslintrc.js` (create)
  - `src/` (create directory)
- **Commands:**
  ```bash
  pnpm init
  pnpm add typescript @types/node -D
  ```
- **Acceptance:**
  - [ ] Project initializes without errors
  - [ ] TypeScript compiles successfully
  - [ ] Linting passes
- **Estimate:** 30 min
- **Dependencies:** None

#### Task 1.0.2: Configure Development Environment [P]
- **Description:** Set up development scripts and hot reload
- **Files:**
  - `package.json` (modify scripts)
  - `.env.example` (create)
- **Acceptance:**
  - [ ] `pnpm dev` starts development server
  - [ ] Hot reload works
- **Estimate:** 20 min
- **Dependencies:** 1.0.1

---

### User Story: US-001 - [Story Title]

#### Task 1.1.1: [Task Title] [B]
- **Description:** [Detailed description]
- **Files:**
  - `src/[path]` (create/modify)
- **Acceptance:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
- **Estimate:** [X] hr
- **Dependencies:** [Task IDs]

#### Task 1.1.2: [Task Title] [P]
...

### Checkpoint: Phase 1 Validation
- [ ] All Phase 1 tasks complete
- [ ] All tests passing
- [ ] Code review completed
- [ ] Foundation demo successful

---

## Phase 2: Core Features

### User Story: US-002 - [Story Title]

#### Task 2.1.1: [Task Title]
...

### Checkpoint: Phase 2 Validation
- [ ] Core features functional
- [ ] Integration tests passing
- [ ] Performance baseline met

---

## Phase 3: Polish & Deploy

### User Story: US-00N - [Story Title]

#### Task 3.1.1: [Task Title]
...

### Checkpoint: Phase 3 Validation
- [ ] All acceptance criteria met
- [ ] Documentation complete
- [ ] Deployment successful
- [ ] Stakeholder sign-off

---

## Dependency Graph

```
1.0.1 ─┬─> 1.0.2
       └─> 1.1.1 ──> 1.1.2 ──> 2.1.1
                              │
                    1.1.3 ────┘
```

## Progress Tracking

Update as tasks complete:

| Task | Status | Completed | Notes |
|------|--------|-----------|-------|
| 1.0.1 | ⬜ | | |
| 1.0.2 | ⬜ | | |
| 1.1.1 | ⬜ | | |
```

---

## 7. Phase 6: New Capabilities

### 7.1 Codebase Scanner Script

**File: `src/specify_cli/scripts/scan-codebase.sh`**

```bash
#!/bin/bash
#
# Codebase Scanner for project-specify
# Analyzes project structure, dependencies, and patterns
#

set -e

OUTPUT_DIR="${1:-.specify/scans}"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
REPORT_FILE="$OUTPUT_DIR/codebase-analysis-$TIMESTAMP.md"

echo "# Codebase Analysis Report" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "Generated: $(date)" >> "$REPORT_FILE"
echo "Directory: $(pwd)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Detect project type
detect_project_type() {
    if [ -f "package.json" ]; then
        echo "nodejs"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        echo "python"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        echo "java"
    elif [ -f "*.csproj" ] || [ -f "*.sln" ]; then
        echo "dotnet"
    else
        echo "unknown"
    fi
}

PROJECT_TYPE=$(detect_project_type)

echo "## Project Type" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "Detected: **$PROJECT_TYPE**" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Directory structure
echo "## Directory Structure" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
find . -type d \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/dist/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/target/*" \
    -not -path "*/.next/*" \
    -not -path "*/build/*" \
    | head -50 \
    | sed 's/[^-][^\/]*\//  /g' \
    >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# File statistics
echo "## File Statistics" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| Extension | Count |" >> "$REPORT_FILE"
echo "|-----------|-------|" >> "$REPORT_FILE"

find . -type f \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    | sed 's/.*\.//' \
    | sort \
    | uniq -c \
    | sort -rn \
    | head -20 \
    | while read count ext; do
        echo "| .$ext | $count |" >> "$REPORT_FILE"
    done

echo "" >> "$REPORT_FILE"

# Dependencies based on project type
echo "## Dependencies" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

case $PROJECT_TYPE in
    nodejs)
        if [ -f "package.json" ]; then
            echo "### Production Dependencies" >> "$REPORT_FILE"
            echo '```json' >> "$REPORT_FILE"
            cat package.json | jq '.dependencies // {}' 2>/dev/null >> "$REPORT_FILE" || echo "{}" >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
            echo "" >> "$REPORT_FILE"
            echo "### Development Dependencies" >> "$REPORT_FILE"
            echo '```json' >> "$REPORT_FILE"
            cat package.json | jq '.devDependencies // {}' 2>/dev/null >> "$REPORT_FILE" || echo "{}" >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
        fi
        ;;
    python)
        if [ -f "requirements.txt" ]; then
            echo '```' >> "$REPORT_FILE"
            cat requirements.txt >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
        elif [ -f "pyproject.toml" ]; then
            echo '```toml' >> "$REPORT_FILE"
            grep -A 100 '\[project.dependencies\]' pyproject.toml 2>/dev/null | head -30 >> "$REPORT_FILE" || echo "No dependencies section found" >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
        fi
        ;;
    rust)
        if [ -f "Cargo.toml" ]; then
            echo '```toml' >> "$REPORT_FILE"
            grep -A 50 '\[dependencies\]' Cargo.toml | head -30 >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
        fi
        ;;
    go)
        if [ -f "go.mod" ]; then
            echo '```' >> "$REPORT_FILE"
            cat go.mod >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
        fi
        ;;
esac

echo "" >> "$REPORT_FILE"

# Pattern detection
echo "## Detected Patterns" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check for common patterns
if [ -d "src/controllers" ] || [ -d "src/routes" ] || [ -d "app/controllers" ]; then
    echo "- **MVC Pattern** detected (controllers/routes directory)" >> "$REPORT_FILE"
fi

if [ -d "src/domain" ] || [ -d "src/entities" ]; then
    echo "- **Domain-Driven Design** elements detected" >> "$REPORT_FILE"
fi

if [ -d "src/services" ] || [ -d "src/usecases" ]; then
    echo "- **Service/Use Case Layer** detected" >> "$REPORT_FILE"
fi

if [ -d "src/repositories" ] || [ -d "src/data" ]; then
    echo "- **Repository Pattern** detected" >> "$REPORT_FILE"
fi

if [ -d "tests" ] || [ -d "__tests__" ] || [ -d "spec" ]; then
    echo "- **Test Directory** found" >> "$REPORT_FILE"
fi

if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
    echo "- **Docker Compose** configuration found" >> "$REPORT_FILE"
fi

if [ -f "Dockerfile" ]; then
    echo "- **Dockerfile** found" >> "$REPORT_FILE"
fi

if [ -d ".github/workflows" ]; then
    echo "- **GitHub Actions** CI/CD found" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "Report saved to: $REPORT_FILE" >> "$REPORT_FILE"

echo "✅ Codebase analysis complete: $REPORT_FILE"
```

### 7.2 Monorepo Detection Script

**File: `src/specify_cli/scripts/detect-monorepo.sh`**

```bash
#!/bin/bash
#
# Monorepo Detection Script for project-specify
#

set -e

detect_monorepo() {
    local result=""
    local packages=""
    
    # Check pnpm
    if [ -f "pnpm-workspace.yaml" ] || [ -f "pnpm-workspace.yml" ]; then
        result="pnpm"
        packages=$(cat pnpm-workspace.yaml pnpm-workspace.yml 2>/dev/null | grep -E "^\s*-" | sed 's/.*- //' | tr '\n' ',')
    fi
    
    # Check npm/yarn workspaces
    if [ -z "$result" ] && [ -f "package.json" ]; then
        if grep -q '"workspaces"' package.json; then
            result="npm-workspaces"
            packages=$(cat package.json | jq -r '.workspaces[]? // .workspaces.packages[]?' 2>/dev/null | tr '\n' ',')
        fi
    fi
    
    # Check lerna
    if [ -z "$result" ] && [ -f "lerna.json" ]; then
        result="lerna"
        packages=$(cat lerna.json | jq -r '.packages[]?' 2>/dev/null | tr '\n' ',')
    fi
    
    # Check nx
    if [ -z "$result" ] && [ -f "nx.json" ]; then
        result="nx"
    fi
    
    # Check turborepo
    if [ -z "$result" ] && [ -f "turbo.json" ]; then
        result="turborepo"
    fi
    
    # Check Cargo workspace
    if [ -z "$result" ] && [ -f "Cargo.toml" ]; then
        if grep -q '\[workspace\]' Cargo.toml; then
            result="cargo"
            packages=$(grep -A 20 '\[workspace\]' Cargo.toml | grep -E '^\s*"' | tr -d ' ",' | tr '\n' ',')
        fi
    fi
    
    if [ -n "$result" ]; then
        echo "MONOREPO_TYPE=$result"
        echo "MONOREPO_PACKAGES=${packages%,}"  # Remove trailing comma
        return 0
    else
        echo "MONOREPO_TYPE=none"
        return 1
    fi
}

# Run detection
detect_monorepo

# If called with --json flag, output JSON
if [ "$1" == "--json" ]; then
    eval $(detect_monorepo)
    echo "{\"type\": \"$MONOREPO_TYPE\", \"packages\": \"$MONOREPO_PACKAGES\"}"
fi
```

### 7.3 Enhanced Update Script

**File: `src/specify_cli/scripts/update-project-specify.sh`**

```bash
#!/bin/bash
#
# Update project-specify commands via symlinks
# This refreshes the central installation and verifies symlinks
#

set -e

CENTRAL_DIR="$HOME/.project-specify"
VERSION_FILE="$CENTRAL_DIR/version.txt"

echo "🔄 Updating project-specify..."

# Get current version
if [ -f "$VERSION_FILE" ]; then
    CURRENT_VERSION=$(cat "$VERSION_FILE")
    echo "Current version: $CURRENT_VERSION"
fi

# Update via uv
echo "Fetching latest version..."
uv tool install project-specify-cli --force --from git+https://github.com/YOUR_USERNAME/project-specify.git

# Verify symlinks in current directory if .specify exists
if [ -d ".specify" ]; then
    echo ""
    echo "Verifying symlinks in current project..."
    
    for agent_dir in .claude .cursor .copilot .gemini .windsurf; do
        if [ -L "$agent_dir/commands" ]; then
            if [ -e "$agent_dir/commands" ]; then
                echo "  ✅ $agent_dir/commands - valid"
            else
                echo "  ❌ $agent_dir/commands - broken symlink"
            fi
        elif [ -d "$agent_dir/commands" ]; then
            echo "  ⚠️  $agent_dir/commands - regular directory (not symlinked)"
        fi
    done
fi

echo ""
echo "✅ Update complete!"
```

---

## 8. Phase 7: Testing & Validation

### 8.1 Manual Testing Checklist

Create a test project and verify each capability:

```bash
# Create test directory
mkdir -p ~/test-project-specify
cd ~/test-project-specify

# Test 1: Basic initialization with single agent
project-specify init . --ai claude
# Verify:
# - [ ] .specify/ directory created
# - [ ] .claude/commands is a symlink
# - [ ] Symlink points to ~/.project-specify/agents/claude/commands
# - [ ] Commands are accessible

# Test 2: Multi-agent initialization (multiple --ai flags - Typer style)
rm -rf .specify .claude
project-specify init . --ai claude --ai cursor --ai copilot
# Verify:
# - [ ] All three agent directories have command symlinks
# - [ ] Each symlink points to correct central location

# Test 3: Multi-agent initialization (comma-separated)
rm -rf .specify .claude .cursor .github
project-specify init . --ai claude,cursor,copilot
# Verify:
# - [ ] Same result as multiple flags

# Test 4: All agents
rm -rf .specify .claude .cursor .github
project-specify init . --ai all
# Verify:
# - [ ] All supported agents have symlinks

# Test 5: Monorepo detection
# Create a pnpm workspace
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - 'packages/*'
  - 'apps/*'
EOF
mkdir -p packages/core apps/web
project-specify init . --ai claude
# Verify:
# - [ ] Monorepo detected
# - [ ] Appropriate workspace handling
```

### 8.2 Command Verification

Test each slash command works in your AI IDE:

```
# In Claude Code or similar:
/speckit.constitution Create a basic constitution for a web application
# Verify: constitution.md created

/speckit.specify Build a todo application with user authentication
# Verify: spec.md created with user stories

/speckit.plan Use Next.js with Prisma and PostgreSQL
# Verify: plan.md created with technical details

/speckit.tasks
# Verify: tasks.md created with actionable items

/speckit.scan
# Verify: codebase analysis report generated

/speckit.research Research Next.js App Router best practices
# Verify: research.md updated
```

### 8.3 Symlink Integrity Tests

**File: `tests/test_symlinks.py`**

```python
"""Tests for symlink functionality."""

import os
import tempfile
from pathlib import Path
import pytest

from specify_cli.symlink_manager import (
    create_agent_symlinks,
    verify_symlinks,
    ensure_central_installation,
    CENTRAL_DIR,
)


@pytest.fixture
def temp_project():
    """Create a temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def central_install():
    """Ensure central installation exists."""
    ensure_central_installation()
    yield CENTRAL_DIR


def test_create_single_agent_symlink(temp_project, central_install):
    """Test creating symlink for a single agent."""
    results = create_agent_symlinks(temp_project, ["claude"])
    
    assert results["claude"] is True
    
    symlink_path = temp_project / ".claude" / "commands"
    assert symlink_path.is_symlink()
    assert symlink_path.resolve().exists()


def test_create_multiple_agent_symlinks(temp_project, central_install):
    """Test creating symlinks for multiple agents."""
    agents = ["claude", "cursor", "windsurf"]
    results = create_agent_symlinks(temp_project, agents)
    
    for agent in agents:
        assert results[agent] is True


def test_verify_valid_symlinks(temp_project, central_install):
    """Test symlink verification."""
    create_agent_symlinks(temp_project, ["claude"])
    
    status = verify_symlinks(temp_project, ["claude"])
    assert status["claude"] == "valid"


def test_verify_missing_symlinks(temp_project):
    """Test detection of missing symlinks."""
    status = verify_symlinks(temp_project, ["claude"])
    assert status["claude"] == "missing"


def test_force_overwrite(temp_project, central_install):
    """Test force flag overwrites existing directories."""
    # Create a regular directory
    (temp_project / ".claude" / "commands").mkdir(parents=True)
    (temp_project / ".claude" / "commands" / "test.md").touch()
    
    # Without force, should skip
    results = create_agent_symlinks(temp_project, ["claude"], force=False)
    assert results["claude"] is False
    
    # With force, should overwrite
    results = create_agent_symlinks(temp_project, ["claude"], force=True)
    assert results["claude"] is True
    assert (temp_project / ".claude" / "commands").is_symlink()
```

### 8.4 Integration Test Script

**File: `tests/integration_test.sh`**

```bash
#!/bin/bash
#
# Integration tests for project-specify
#

set -e

TEST_DIR=$(mktemp -d)
echo "Running integration tests in: $TEST_DIR"

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

cd "$TEST_DIR"

# Test 1: Install from source
echo "Test 1: Installing project-specify..."
uv tool install project-specify-cli --from /path/to/your/project-specify
echo "✅ Installation successful"

# Test 2: Check command
echo "Test 2: Running check..."
project-specify check
echo "✅ Check command works"

# Test 3: Init with single agent
echo "Test 3: Init with Claude..."
mkdir test-single && cd test-single
project-specify . --ai claude --no-git
[ -L ".claude/commands" ] || { echo "❌ Symlink not created"; exit 1; }
cd ..
echo "✅ Single agent init works"

# Test 4: Init with all agents
echo "Test 4: Init with all agents..."
mkdir test-all && cd test-all
project-specify . --ai all --no-git
# Verify several agents
[ -L ".claude/commands" ] || { echo "❌ Claude symlink missing"; exit 1; }
[ -L ".cursor/commands" ] || { echo "❌ Cursor symlink missing"; exit 1; }
cd ..
echo "✅ All agents init works"

# Test 5: Verify .specify structure
echo "Test 5: Verifying .specify structure..."
cd test-all
[ -d ".specify/memory" ] || { echo "❌ memory dir missing"; exit 1; }
[ -d ".specify/scripts" ] || { echo "❌ scripts dir missing"; exit 1; }
[ -d ".specify/templates" ] || { echo "❌ templates dir missing"; exit 1; }
cd ..
echo "✅ .specify structure correct"

echo ""
echo "========================================="
echo "All integration tests passed! ✅"
echo "========================================="
```

---

## 9. Phase 8: Package Distribution

### 9.1 GitHub Package Registry Setup

Since you have a GitHub Student account, you can use GitHub Packages to distribute your tool.

#### Option A: Direct Git Installation (Simplest)

Users install directly from your GitHub repo:

```bash
uv tool install project-specify-cli --from git+https://github.com/YOUR_USERNAME/project-specify.git
```

This is the approach spec-kit uses and requires no additional setup.

#### Option B: GitHub Releases

Create tagged releases for version management:

```bash
# Tag a release
git tag -a v1.0.0 -m "Initial release of project-specify"
git push origin v1.0.0

# Users can then install specific versions:
uv tool install project-specify-cli --from git+https://github.com/YOUR_USERNAME/project-specify.git@v1.0.0
```

#### Option C: PyPI Publication (More Discoverable)

For maximum discoverability, publish to PyPI:

**1. Create PyPI Account**
- Go to https://pypi.org/account/register/
- Verify your email

**2. Create API Token**
- Go to https://pypi.org/manage/account/token/
- Create a token scoped to your project (or all projects for first upload)
- Save the token securely

**3. Configure Publishing**

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
# Enter __token__ as username
# Enter your API token as password
```

**4. Users Install via pip/uv**

```bash
# Via uv
uv tool install project-specify-cli

# Via pip
pip install project-specify-cli
```

### 9.2 Release Workflow

**File: `.github/workflows/release.yml`**

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
      
      # Optional: Publish to PyPI
      # - name: Publish to PyPI
      #   env:
      #     TWINE_USERNAME: __token__
      #     TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      #   run: twine upload dist/*
```

### 9.3 Installation Documentation

Create clear installation docs for your users:

**File: `docs/INSTALLATION.md`**

```markdown
# Installing project-specify

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Git

## Quick Install

### Using uv (Recommended)

```bash
# Install globally
uv tool install project-specify-cli --from git+https://github.com/YOUR_USERNAME/project-specify.git

# Verify installation
project-specify --version
project-specify check
```

### Using pip

```bash
pip install git+https://github.com/YOUR_USERNAME/project-specify.git

# Or if published to PyPI:
pip install project-specify-cli
```

## Usage

### Initialize a New Project

```bash
# With all AI IDE support
project-specify init my-project --ai all

# With specific agents (multiple --ai flags - Typer style)
project-specify init my-project --ai claude --ai cursor --ai copilot

# With specific agents (comma-separated also works)
project-specify init my-project --ai claude,cursor

# In current directory
project-specify init . --ai all

# Using --here flag
project-specify init --here --ai all
```

### Available Commands

After initialization, your AI IDE will have these commands:

| Command | Description |
|---------|-------------|
| `/speckit.constitution` | Create project principles |
| `/speckit.specify` | Create project specification |
| `/speckit.plan` | Create technical plan |
| `/speckit.tasks` | Generate task breakdown |
| `/speckit.implement` | Execute implementation |
| `/speckit.scan` | Analyze existing codebase |
| `/speckit.research` | Research technologies |
| `/speckit.clarify` | Clarify requirements |

## Updating

```bash
# Update to latest version
uv tool install project-specify-cli --force --from git+https://github.com/YOUR_USERNAME/project-specify.git

# Or with specific version
uv tool install project-specify-cli --force --from git+https://github.com/YOUR_USERNAME/project-specify.git@v1.1.0
```

## Uninstalling

```bash
uv tool uninstall project-specify-cli

# Also remove central installation
rm -rf ~/.project-specify
```
```

### 9.4 Keeping Your Fork Updated

Periodically sync with upstream spec-kit:

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream main into your main
git checkout main
git merge upstream/main

# Resolve any conflicts, then push
git push origin main

# Rebase your feature branch if needed
git checkout feature/project-specify-customization
git rebase main
```

---

## 10. Appendix: File Reference

### 10.1 Complete Directory Structure

```
project-specify/
├── .github/
│   └── workflows/
│       └── release.yml
├── docs/
│   ├── INSTALLATION.md
│   └── COMMANDS.md
├── src/
│   └── specify_cli/
│       ├── __init__.py
│       ├── main.py                    # Modified CLI entry point
│       ├── symlink_manager.py         # New: symlink handling
│       ├── monorepo.py                # New: monorepo detection
│       ├── agents/                    # New: centralized commands
│       │   ├── claude/
│       │   │   └── commands/
│       │   │       ├── speckit.constitution.md
│       │   │       ├── speckit.specify.md
│       │   │       ├── speckit.plan.md
│       │   │       ├── speckit.tasks.md
│       │   │       ├── speckit.implement.md
│       │   │       ├── speckit.scan.md         # New
│       │   │       ├── speckit.research.md     # New
│       │   │       └── speckit.clarify.md
│       │   ├── cursor/
│       │   │   └── commands/
│       │   │       └── [same as claude]
│       │   ├── copilot/
│       │   │   └── copilot-instructions.md
│       │   ├── windsurf/
│       │   │   └── commands/
│       │   └── [other agents...]
│       ├── scripts/                   # Bundled scripts
│       │   ├── scan-codebase.sh
│       │   ├── detect-monorepo.sh
│       │   └── update-project-specify.sh
│       └── templates/                 # Modified templates
│           ├── project-plan-template.md
│           ├── implementation-plan-template.md
│           └── tasks-template.md
├── tests/
│   ├── test_symlinks.py
│   ├── test_monorepo.py
│   └── integration_test.sh
├── scripts/
│   └── generate-agent-commands.sh
├── pyproject.toml                     # Modified package config
├── README.md                          # Updated documentation
├── LICENSE                            # MIT (inherited)
└── ARCHITECTURE-ANALYSIS.md           # Your analysis notes
```

### 10.2 Key Modifications Summary

| File | Change Type | Purpose |
|------|-------------|---------|
| `pyproject.toml` | Modified | Rename package, update entry point |
| `src/specify_cli/main.py` | Modified | Add --ai all, symlink integration |
| `src/specify_cli/symlink_manager.py` | New | Central symlink management |
| `src/specify_cli/monorepo.py` | New | Workspace detection |
| `src/specify_cli/agents/` | New | Centralized command files |
| `src/specify_cli/templates/` | Modified | Project-focused templates |
| `src/specify_cli/scripts/` | New | Helper scripts |

### 10.3 Verification Commands

```bash
# Verify installation
project-specify --version
project-specify check

# Verify symlinks in a project
ls -la .claude/commands
readlink .claude/commands

# Verify central installation
ls -la ~/.project-specify/agents/

# Test command availability (in Claude Code)
# Type /speckit. and verify autocomplete shows all commands
```

---

## Next Steps Checklist

- [ ] Fork spec-kit repository
- [ ] Clone and set up development environment
- [ ] Complete architecture analysis (Phase 2)
- [ ] Implement core modifications (Phase 3)
- [ ] Create symlink manager (Phase 4)
- [ ] Create all command files (Phase 4)
- [ ] Customize templates (Phase 5)
- [ ] Add new capabilities (Phase 6)
- [ ] Run all tests (Phase 7)
- [ ] Set up GitHub release workflow (Phase 8)
- [ ] Document and share with friends

---

*This guide was created for the project-specify customization project. Update this document as you make progress and discover new requirements.*