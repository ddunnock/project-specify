# Technical Implementation Plan

> Project: [PROJECT_NAME]
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

## API Contracts
[Endpoint specifications]

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

