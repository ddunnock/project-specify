# Project-Specify Quick Start Checklist

## Day 1: Fork & Analyze

### Step 1: Fork Repository
```bash
# On GitHub: Fork https://github.com/github/spec-kit to your account
# Then clone:
git clone https://github.com/YOUR_USERNAME/spec-kit.git project-specify
cd project-specify
git remote add upstream https://github.com/github/spec-kit.git
```

### Step 2: Analyze Structure
```bash
# Examine CLI entry point
cat src/specify_cli/main.py

# Examine how agents are handled
find . -type d -name "*commands*" 2>/dev/null

# Examine templates
ls -la templates/

# Check pyproject.toml for entry points
cat pyproject.toml | grep -A5 "\[project.scripts\]"
```

### Step 3: Create Development Branch
```bash
git checkout -b feature/project-specify-v1
```

---

## Day 2-3: Core Implementation

### Step 4: Modify pyproject.toml
Change package name and entry point:
- `name = "project-specify-cli"`
- `project-specify = "specify_cli.main:main"`

### Step 5: Create symlink_manager.py
Key functions needed:
- `ensure_central_installation()` - Sets up ~/.project-specify
- `create_agent_symlinks()` - Creates symlinks in project
- `verify_symlinks()` - Checks symlink health

### Step 6: Modify main.py
- Add `parse_ai_callback()` for Typer to support "all" and comma-separated
- Integrate symlink manager into init command
- Add `--workspace` flag for monorepo support
- Use `List[str]` type annotation for `--ai` option

---

## Day 4-5: Commands & Templates

### Step 7: Create agents/ Directory Structure
```bash
mkdir -p src/specify_cli/agents/{claude,cursor,copilot,windsurf,gemini}/commands
```

### Step 8: Create Core Commands
For each agent, create:
- speckit.constitution.md
- speckit.specify.md
- speckit.plan.md
- speckit.tasks.md
- speckit.implement.md
- speckit.scan.md (new)
- speckit.research.md (new)
- speckit.clarify.md

### Step 9: Customize Templates
Modify templates/ for project planning focus:
- project-plan-template.md (replaces spec-template.md)
- implementation-plan-template.md
- tasks-template.md

---

## Day 6: Testing

### Step 10: Manual Testing
```bash
# Install your version
uv tool install project-specify-cli --from /path/to/project-specify

# Test initialization
mkdir ~/test-ps && cd ~/test-ps
project-specify init . --ai all

# Test multiple --ai flags (Typer style)
rm -rf .specify .claude .cursor .github
project-specify init . --ai claude --ai cursor --ai copilot

# Test comma-separated (also supported)
rm -rf .specify .claude .cursor .github
project-specify init . --ai claude,cursor,copilot

# Verify symlinks
ls -la .claude/commands
readlink .claude/commands
```

### Step 11: Test in AI IDE
- Open project in VS Code / Cursor
- Type `/speckit.` and verify commands appear
- Run through full workflow

---

## Day 7: Distribution

### Step 12: Create Release
```bash
git add .
git commit -m "feat: project-specify v1.0.0 with symlink architecture"
git tag -a v1.0.0 -m "Initial project-specify release"
git push origin feature/project-specify-v1
git push origin v1.0.0
```

### Step 13: Share Installation Command
```bash
# Friends install via:
uv tool install project-specify-cli --from git+https://github.com/YOUR_USERNAME/project-specify.git
```

---

## Key Files Quick Reference

| Priority | File | Purpose |
|----------|------|---------|
| 1 | `pyproject.toml` | Package config - rename first |
| 2 | `src/specify_cli/symlink_manager.py` | Core symlink logic |
| 3 | `src/specify_cli/main.py` | CLI modifications |
| 4 | `src/specify_cli/agents/claude/commands/*.md` | Command definitions |
| 5 | `src/specify_cli/templates/*.md` | Project templates |

---

## Gotchas to Watch For

1. **Windows Symlinks**: May need admin privileges or developer mode
2. **Agent Path Variations**: Some agents use different structures (Copilot uses `.github/`)
3. **Central Dir Permissions**: `~/.project-specify` needs to be readable
4. **Template Placeholders**: Watch for `[PROJECT_NAME]`, `[DATE]`, `[BRANCH_NAME]` replacements
5. **Git Integration**: The original spec-kit creates branches - decide if you want this
6. **Typer List Options**: Use `callback=parse_ai_callback` to support comma-separated values in a single `--ai` flag; otherwise Typer requires multiple `--ai` flags

---

## Validation Checklist

Before v1.0.0 release:

- [ ] `project-specify init . --ai claude` works
- [ ] `project-specify init . --ai claude --ai cursor --ai copilot` works (multiple flags)
- [ ] `project-specify init . --ai claude,cursor,copilot` works (comma-separated)
- [ ] `project-specify init . --ai all` creates all symlinks
- [ ] Symlinks point to `~/.project-specify/agents/*/commands`
- [ ] `.specify/` directory is NOT symlinked (project-specific)
- [ ] All 8 slash commands work in Claude Code
- [ ] Commands work in at least one other IDE (Cursor recommended)
- [ ] `project-specify check` shows installed agents
- [ ] Friends can install via git URL