# Project-Specify Implementation Package

This folder contains everything you need to fork and customize GitHub's spec-kit into your own `project-specify` tool.

## Contents

### Documentation

| File | Description |
|------|-------------|
| `PROJECT-SPECIFY-IMPLEMENTATION-GUIDE.md` | Complete implementation guide with all phases |
| `QUICK-START-CHECKLIST.md` | Day-by-day checklist for quick implementation |

### Implementation Files

| File | Description |
|------|-------------|
| `src/symlink_manager.py` | Core symlink management module (drop into `src/specify_cli/`) |
| `src/pyproject.toml.example` | Example pyproject.toml with required modifications |
| `src/agents/claude/commands/speckit.scan.md` | New codebase scanner command |

## Quick Start

1. **Fork spec-kit:** https://github.com/github/spec-kit
2. **Read the guide:** Start with `QUICK-START-CHECKLIST.md` for a fast overview
3. **Deep dive:** Use `PROJECT-SPECIFY-IMPLEMENTATION-GUIDE.md` for detailed instructions
4. **Copy implementation files:** Move files from `src/` to your fork

## Installation (After Implementation)

```bash
# Install your custom version
uv tool install project-specify-cli --from git+https://github.com/YOUR_USERNAME/project-specify.git

# Use in any project
cd your-project
project-specify init . --ai all

# Or specific agents (multiple --ai flags)
project-specify init . --ai claude --ai cursor --ai copilot

# Or comma-separated
project-specify init . --ai claude,cursor,copilot
```

## Key Differences from spec-kit

| Feature | spec-kit | project-specify |
|---------|----------|-----------------|
| Command storage | Copied to each project | Symlinked from `~/.project-specify` |
| Multi-agent support | One agent per init | `--ai all` or `--ai claude --ai cursor` |
| Focus | Feature specifications | Project plans & tasks |
| New commands | — | `/speckit.scan`, `/speckit.research` |
| Monorepo support | Limited | Built-in workspace detection |
| **MCP Integration** | — | **Auto-discovers MCP servers & injects into commands** |

## MCP Server Discovery

On initialization, project-specify automatically:

1. **Discovers MCP servers** from Claude Desktop, Claude Code, Cursor, and project configs
2. **Detects project technology** (language, framework, database, services)
3. **Generates context files** that AI agent commands reference

```bash
# Run discovery on existing project
project-specify discover

# Skip discovery during init (faster)
project-specify init . --ai all --no-mcp-discovery
```

Output files:
- `.specify/context/mcp-servers.md` — Human-readable MCP context
- `.specify/context/project-context.json` — Machine-readable context

Commands like `/speckit.plan` automatically reference these files to leverage available MCP capabilities.

## Support

- Original spec-kit: https://github.com/github/spec-kit
- Your fork issues: https://github.com/YOUR_USERNAME/project-specify/issues