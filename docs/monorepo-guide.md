# Monorepo Usage Guide

This guide explains how to use project-specify in monorepo projects with multiple workspaces or packages.

## Supported Monorepo Types

Project-specify automatically detects and supports these monorepo configurations:

| Tool | Configuration File | Detection Method |
|------|-------------------|------------------|
| **pnpm workspaces** | `pnpm-workspace.yaml` | Parses workspace patterns |
| **npm workspaces** | `package.json` | Reads `workspaces` field |
| **Yarn workspaces** | `package.json` | Reads `workspaces` field |
| **Lerna** | `lerna.json` | Reads `packages` field |
| **Nx** | `nx.json` | Detects Nx workspace structure |
| **Turborepo** | `turbo.json` | Detects Turbo configuration |
| **Cargo workspaces** | `Cargo.toml` | Reads `[workspace]` section |

## Monorepo Detection

When you run `specify init` in a monorepo, project-specify:

1. **Scans for workspace configuration files** starting from the current directory and moving up
2. **Parses workspace patterns** (e.g., `packages/*`, `apps/*`)
3. **Resolves workspace packages** by expanding glob patterns
4. **Suggests workspace-specific initialization** if appropriate

## Initialization Strategies

###  Strategy 1: Root-Level Initialization

Initialize project-specify at the monorepo root to share commands across all workspaces.

**Use when:**
- All workspaces use the same AI assistant
- You want centralized spec-driven development commands
- Workspaces share common development principles

**Example:**

```bash
cd my-monorepo
specify init . --ai claude --here
```

**Result:**
```
my-monorepo/
├── .claude/
│   └── commands/        # Shared across all workspaces
├── .specify/            # Root-level specs
├── packages/
│   ├── frontend/
│   └── backend/
└── pnpm-workspace.yaml
```

**Pros:**
- ✅ Single source of truth for commands
- ✅ Consistent tooling across workspaces
- ✅ Easier to maintain

**Cons:**
- ❌ Less flexibility for workspace-specific needs
- ❌ Specs may become cluttered with multi-workspace concerns

### Strategy 2: Workspace-Specific Initialization

Initialize project-specify in individual workspace packages for independent development.

**Use when:**
- Workspaces have different tech stacks (e.g., React + Python API)
- Teams work independently on different workspaces
- Workspaces have different AI assistant preferences

**Example:**

```bash
# Option A: Use --workspace flag from root
cd my-monorepo
specify init . --workspace packages/frontend --ai claude

# Option B: Navigate to workspace directly
cd my-monorepo/packages/frontend
specify init . --ai claude --here
```

**Result:**
```
my-monorepo/
├── packages/
│   ├── frontend/
│   │   ├── .claude/
│   │   │   └── commands/    # Frontend-specific
│   │   └── .specify/        # Frontend specs
│   └── backend/
│       ├── .claude/
│       │   └── commands/    # Backend-specific
│       └── .specify/        # Backend specs
└── pnpm-workspace.yaml
```

**Pros:**
- ✅ Workspace independence
- ✅ Technology-specific commands
- ✅ Clearer separation of concerns

**Cons:**
- ❌ Duplication of commands across workspaces
- ❌ More maintenance overhead
- ❌ Potential inconsistency between workspaces

### Strategy 3: Hybrid Approach

Combine root-level and workspace-specific initialization for maximum flexibility.

**Use when:**
- Some commands are shared (root level)
- Some workspaces need custom commands (workspace level)
- You want both consistency and flexibility

**Example:**

```bash
# Root level for shared principles
cd my-monorepo
specify init . --ai claude --here

# Workspace-specific for custom needs
cd packages/mobile-app
specify init . --ai cursor-agent --here --force
```

**Result:**
```
my-monorepo/
├── .claude/
│   └── commands/        # Shared base commands
├── .specify/            # Shared principles
├── packages/
│   ├── frontend/        # Uses root .claude
│   ├── backend/         # Uses root .claude
│   └── mobile-app/
│       ├── .cursor/     # Workspace-specific
│       │   └── commands/
│       └── .specify/    # Mobile-specific specs
└── pnpm-workspace.yaml
```

**Pros:**
- ✅ Best of both worlds
- ✅ Flexibility where needed
- ✅ Consistency where desired

**Cons:**
- ❌ More complex setup
- ❌ Requires understanding of command resolution

## Common Monorepo Setups

### pnpm Workspaces

**Configuration:** `pnpm-workspace.yaml`

```yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - 'tools/*'
```

**Initialization:**

```bash
# Root level
pnpm specify init . --ai claude --here

# Specific workspace
pnpm --filter frontend specify init . --ai claude --here

# Or navigate directly
cd packages/frontend
specify init . --ai claude --here
```

### npm Workspaces

**Configuration:** `package.json`

```json
{
  "name": "my-monorepo",
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

**Initialization:**

```bash
# Root level
npm run specify init . --ai claude --here

# Specific workspace
cd packages/frontend
specify init . --ai claude --here
```

### Yarn Workspaces

**Configuration:** `package.json` (same as npm)

**Initialization:**

```bash
# Root level
yarn specify init . --ai claude --here

# Specific workspace
yarn workspace frontend specify init . --ai claude --here
```

### Lerna

**Configuration:** `lerna.json`

```json
{
  "packages": [
    "packages/*"
  ],
  "version": "independent"
}
```

**Initialization:**

```bash
# Root level
npx lerna exec --scope=my-package -- specify init . --ai claude --here

# Or navigate directly
cd packages/my-package
specify init . --ai claude --here
```

### Nx

**Configuration:** `nx.json`

**Initialization:**

```bash
# Root level
nx run-many --target=specify --all

# Specific project
cd apps/my-app
specify init . --ai claude --here
```

### Turborepo

**Configuration:** `turbo.json`

**Initialization:**

```bash
# Root level
turbo run specify init . --ai claude --here

# Specific workspace
cd apps/web
specify init . --ai claude --here
```

### Cargo Workspaces (Rust)

**Configuration:** `Cargo.toml`

```toml
[workspace]
members = [
    "crates/*",
    "tools/*"
]
```

**Initialization:**

```bash
# Root level
cargo specify init . --ai claude --here

# Specific crate
cd crates/my-library
specify init . --ai claude --here
```

## Command Resolution in Monorepos

When an AI assistant looks for commands in a monorepo, it searches in this order:

1. **Current workspace directory** (`.claude/commands/`, etc.)
2. **Parent directories** up to the repository root
3. **Central installation** (`~/.project-specify/agents/`)

### Example Resolution

```
my-monorepo/
├── .claude/commands/        # (2) Root-level commands
├── packages/
│   └── frontend/
│       └── .claude/commands/  # (1) Workspace-specific commands
```

When working in `packages/frontend/`:
1. AI checks `packages/frontend/.claude/commands/` first
2. Falls back to root `.claude/commands/` if command not found
3. Falls back to `~/.project-specify/agents/claude/commands/`

**This allows:**
- Workspace-specific commands override root commands
- Root commands provide fallback defaults
- Central commands provide ultimate fallback

## Shared vs. Workspace-Specific Specs

### Shared Specs (Root Level)

**Location:** `<monorepo-root>/.specify/`

**Use for:**
- Project-wide principles and constitution
- Architectural guidelines
- Cross-workspace integration specs
- Shared infrastructure and tooling

**Example:** `.specify/constitution.md`

```markdown
# My Monorepo Principles

## Consistency
- All workspaces use TypeScript strict mode
- Shared ESLint and Prettier configurations
- Consistent testing approach (Vitest)

## Architecture
- Frontend packages communicate via REST APIs
- Backend packages use shared database layer
- All packages follow clean architecture principles
```

### Workspace-Specific Specs

**Location:** `<workspace>/.specify/`

**Use for:**
- Workspace-specific features
- Local implementation details
- Workspace-focused user stories

**Example:** `packages/frontend/.specify/features/001-user-dashboard/spec.md`

```markdown
# User Dashboard Feature

User story specific to the frontend workspace...
```

## Best Practices

### 1. Start at the Root

Initialize at the monorepo root first to establish shared principles:

```bash
cd my-monorepo
specify init . --ai claude --here
```

Then add workspace-specific initialization as needed.

### 2. Use Consistent AI Assistants

Choose one primary AI assistant for the monorepo to maintain consistency:

```bash
# All workspaces use Claude
specify init . --ai claude --here
```

Or document which workspaces use which assistants in your root README.

### 3. Share Common Configurations

Keep shared development principles at the root level:

```
my-monorepo/
├── .specify/
│   ├── constitution.md      # Shared principles
│   └── architecture.md      # Overall architecture
└── packages/
    └── frontend/
        └── .specify/
            └── features/     # Frontend-specific features
```

### 4. Document Monorepo Structure

Add a `MONOREPO.md` file explaining:
- Which workspaces exist and their purposes
- Where project-specify is initialized
- Which AI assistants are used where
- How specs are organized

### 5. Use Git Hooks Consistently

If using git hooks (like pre-commit, commit-msg), install them at the root level so they apply to all workspaces:

```bash
# Root level
cd my-monorepo
git config core.hooksPath .githooks
```

## Troubleshooting

### Workspace Not Detected

**Symptom:** `specify init` doesn't recognize monorepo structure

**Solutions:**
1. Verify workspace configuration file exists (e.g., `pnpm-workspace.yaml`)
2. Check glob patterns match your workspace directories
3. Use `--workspace` flag explicitly:
   ```bash
   specify init . --workspace packages/frontend --ai claude
   ```

### Commands Not Found in Workspace

**Symptom:** AI assistant can't find spec-kit commands in workspace

**Solutions:**
1. Check command resolution order (workspace → root → central)
2. Verify symlinks were created correctly
3. Navigate to workspace directory before starting AI assistant
4. Re-run initialization with `--force` flag:
   ```bash
   cd packages/frontend
   specify init . --ai claude --here --force
   ```

### Conflicting Initializations

**Symptom:** Multiple `.specify/` directories causing confusion

**Solutions:**
1. Choose one strategy (root-level OR workspace-specific)
2. Document your approach in root README
3. Remove conflicting `.specify/` directories:
   ```bash
   # Keep only root-level
   rm -rf packages/*/.specify
   ```
4. Or keep only workspace-level:
   ```bash
   rm -rf .specify
   ```

### Symlinking Issues on Windows

**Symptom:** Symlinks fail in monorepo workspaces

**Solutions:**
1. Use `--copy` flag for all initializations:
   ```bash
   # Root
   specify init . --ai claude --here --copy

   # Workspaces
   cd packages/frontend
   specify init . --ai claude --here --copy
   ```
2. See [Windows Setup Guide](./windows-setup.md) for detailed troubleshooting

## Example Workflows

### Frontend + Backend Monorepo

**Structure:**
```
my-app/
├── apps/
│   ├── web/              # React frontend
│   └── mobile/           # React Native
├── packages/
│   ├── api/              # Express backend
│   └── shared/           # Shared types
└── pnpm-workspace.yaml
```

**Initialization:**

```bash
# Root level for shared principles
cd my-app
specify init . --ai claude --here

# API workspace has Python (different from others)
cd packages/api
specify init . --ai claude --here --force
```

### Multi-Language Monorepo

**Structure:**
```
platform/
├── services/
│   ├── auth/             # Rust service
│   ├── api/              # Go service
│   └── worker/           # Python worker
└── Cargo.toml            # Rust workspace
```

**Initialization:**

```bash
# Each service independently (different languages)
cd services/auth
specify init . --ai claude --here

cd ../api
specify init . --ai claude --here

cd ../worker
specify init . --ai claude --here
```

### Shared Library Monorepo

**Structure:**
```
ui-library/
├── packages/
│   ├── components/       # React components
│   ├── icons/            # SVG icons
│   ├── themes/           # Theme configs
│   └── utils/            # Shared utilities
└── package.json          # npm workspaces
```

**Initialization:**

```bash
# Root level only (all workspaces share principles)
cd ui-library
specify init . --ai claude --here
```

## Related Documentation

- [Windows Setup Guide](./windows-setup.md)
- [MCP Setup Guide](./mcp-setup.md)
- [Main README](../README.md)
