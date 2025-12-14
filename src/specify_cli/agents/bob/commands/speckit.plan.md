---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Planning: Context Loading

Before creating the plan, load the project context:

1. **Read MCP Context** (if available):
   ```
   .specify/context/mcp-servers.md
   .specify/context/project-context.json
   ```

2. **Read Project Context**:
   - Constitution from `.specify/memory/constitution.md`
   - Specification from `.specify/specs/<current-branch>/spec.md` or `.specify/specs/<project-name>/spec.md`

3. **Note Available Capabilities**:
   - Which MCP servers are configured?
   - What's the detected tech stack?
   - What database is available?
   - What services (Docker, K8s, CI/CD) are in use?

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC, `/memory/constitution.md`, and MCP context files if available. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Reference MCP servers from context files if available
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

## MCP-Aware Planning

When creating the plan, leverage MCP capabilities:

### If `filesystem` MCP is available:
- Use MCP for file operations instead of shell commands
- Reference file reading/writing via MCP tools

### If `git` MCP is available:
- Plan git operations through MCP for better error handling
- Use for branch management, commits, diffs

### If `github` MCP is available:
- Plan GitHub issue creation for tracking
- Consider PR automation in CI/CD section
- Use for fetching existing issues/discussions

### If `postgres` or `sqlite` MCP is available:
- Use MCP for database queries during implementation
- Plan schema inspection via MCP tools
- Include database migration strategy using MCP

### If `puppeteer` MCP is available:
- Plan E2E tests using browser automation
- Include visual regression testing considerations

### If `fetch` MCP is available:
- Use for external API integration testing
- Plan health checks for external dependencies

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
