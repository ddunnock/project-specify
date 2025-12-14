---
description: Create technical implementation plan from specification with MCP awareness
---

# Technical Planning (MCP-Enhanced)

Create a comprehensive technical implementation plan based on the specification,
leveraging available MCP servers and detected project technology.

## Pre-Planning: Context Loading

Before creating the plan, load the project context:

1. **Read MCP Context** (if available):
   ```
   .specify/context/mcp-servers.md
   .specify/context/project-context.json
   ```

2. **Read Project Context**:
   - Constitution from `.specify/memory/constitution.md`
   - Specification from `.specify/specs/<current-branch>/spec.md`

3. **Note Available Capabilities**:
   - Which MCP servers are configured?
   - What's the detected tech stack?
   - What database is available?
   - What services (Docker, K8s, CI/CD) are in use?

## Instructions

1. Read all context files listed above
2. Run the plan setup script:
   ```bash
   bash .specify/scripts/setup-plan.sh
   ```
3. Create implementation plan in `.specify/specs/<current-branch>/plan.md`

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

## Plan Structure

```markdown
# Technical Implementation Plan

> Project: [PROJECT_NAME]
> Branch: [BRANCH_NAME]
> Created: [DATE]

## Project Context

### Technology Stack (Auto-Detected)
<!-- Reference .specify/context/project-context.json -->
- **Language:** [from context]
- **Framework:** [from context]
- **Package Manager:** [from context]
- **Database:** [from context]

### Available MCP Servers
<!-- Reference .specify/context/mcp-servers.md -->
| Server | Usage in This Project |
|--------|----------------------|
| [server] | [how we'll use it] |

## Architecture Overview

### System Context
[High-level architecture - informed by detected services]

### Architecture Style
- **Pattern:** [Monolith/Microservices/Serverless/etc.]
- **Rationale:** [Why this approach, considering available tools]

## Technology Decisions

| Decision | Options | Choice | Rationale |
|----------|---------|--------|-----------|
| [Decision] | [Options] | [Choice] | [Why - can reference MCP capabilities] |

## Component Architecture

### Component: [Name]
**Purpose:** [Description]
**Implementation Notes:**
- [Note how MCP servers will be used]
- [Reference detected framework patterns]

## Data Architecture

### Database: [Detected Database]
<!-- If postgres/sqlite MCP available, note query capabilities -->

**MCP Integration:**
- Schema inspection: Use [database] MCP `describe_table`
- Queries: Use [database] MCP `query` for data operations

### Data Models
[Entity definitions]

## Implementation Phases

### Phase 1: Foundation
**MCP Tools Used:**
- filesystem: Project scaffolding
- git: Repository setup

**Tasks:**
1. [Task leveraging available tools]

### Phase 2: Core Features
**MCP Tools Used:**
- [List relevant MCP servers]

**Tasks:**
1. [Tasks with MCP awareness]

## Testing Strategy

### Unit Testing
- Framework: [detected or chosen]
- Location: [standard for detected framework]

### Integration Testing
<!-- If database MCP available -->
- Database: Use [database] MCP for test queries
- API: [testing approach]

### E2E Testing
<!-- If puppeteer MCP available -->
- Browser automation via puppeteer MCP
- Visual regression testing

## DevOps & Infrastructure

### Detected Services
<!-- From project-context.json -->
- [List detected services: docker, k8s, github-actions, etc.]

### CI/CD Pipeline
<!-- If github MCP available -->
- Use github MCP for PR automation
- [Pipeline stages]

## MCP Integration Summary

| Phase | MCP Servers Used | Operations |
|-------|-----------------|------------|
| Setup | filesystem, git | Scaffolding, repo init |
| Development | [servers] | [operations] |
| Testing | [servers] | [operations] |
| Deployment | [servers] | [operations] |

## Dependencies & Prerequisites

### External Services
[Services with notes on MCP integration]

### Required Credentials
[Credentials, noting which MCP servers need them]
```

## Validation

Before finalizing, verify:
- [ ] All user stories are addressed
- [ ] Architecture aligns with constitution
- [ ] MCP capabilities are appropriately leveraged
- [ ] Plan accounts for detected technology stack
- [ ] Dependencies are clearly identified
- [ ] Timeline is realistic

## Notes

- If `.specify/context/` files don't exist, run `/speckit.scan` first
- MCP integration is optional but recommended where available
- Always fall back to standard approaches if MCP servers aren't configured