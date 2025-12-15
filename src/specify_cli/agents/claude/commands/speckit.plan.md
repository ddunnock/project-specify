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

Before creating the plan, detect project mode and load appropriate context:

### Step 1: Detect Project Mode

```bash
bash scripts/bash/detect-project-mode.sh
```

**Mode Detection Logic:**
- If `.specify/research/README.md` exists OR `.specify/spec.md` exists → **Project Mode**
- If `.specify/specs/` exists with numbered feature directories → **Feature Mode**
- If neither exists → **Unknown** (default to Feature Mode)

### Step 2: Load Context Based on Mode

#### If Project Mode:

1. **Read Research Foundation**:
   ```bash
   # Research index
   cat .specify/research/README.md

   # Technical research
   cat .specify/research/technical/data-research.md
   cat .specify/research/technical/architecture-research.md
   cat .specify/research/technical/tech-stack-research.md

   # Domain research
   cat .specify/research/domain/domain-research.md
   cat .specify/research/domain/business-rules-research.md
   cat .specify/research/domain/workflow-research.md

   # User research
   cat .specify/research/user/user-research.md
   cat .specify/research/user/personas-research.md
   cat .specify/research/user/journey-maps-research.md

   # Constraints research
   cat .specify/research/constraints/compliance-research.md
   cat .specify/research/constraints/security-research.md
   cat .specify/research/constraints/performance-research.md
   ```

2. **Read Project Specification (PRD)**:
   ```bash
   cat .specify/spec.md
   ```

3. **Read Constitution**:
   ```bash
   cat .specify/memory/constitution.md
   ```

4. **Read MCP Context** (if available):
   ```bash
   cat .specify/context/mcp-servers.md
   cat .specify/context/project-context.json
   ```

5. **Extract Research Decisions for Planning**:

   From **Technical Research**, note:
   - **Data Model** (data-research.md): Entity relationships, storage architecture
   - **Architecture Decisions** (architecture-research.md): Component design, integration patterns, deployment architecture
   - **Tech Stack Choices** (tech-stack-research.md): Languages, frameworks, libraries, infrastructure, tools

   From **Domain Research**, note:
   - **Business Domain** (domain-research.md): Core concepts, terminology, domain rules
   - **Business Rules** (business-rules-research.md): Validation logic, calculations, workflow rules
   - **Workflows** (workflow-research.md): Process flows, decision points, actors

   From **Constraints Research**, note:
   - **Compliance** (compliance-research.md): Regulatory requirements, audit needs, data retention policies
   - **Security** (security-research.md): Authentication, authorization, data protection, threat model
   - **Performance** (performance-research.md): Performance targets, scalability requirements, SLAs

6. **Validate PRD Against Research**:

   Before planning, check that:
   - PRD features reference research documents correctly
   - No conflicts between PRD and research recommendations
   - All research decisions are reflected in PRD requirements

   If conflicts found, flag warnings in planning output.

#### If Feature Mode (Backward Compatible):

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

3. **Execute plan workflow**:

   **If Project Mode:**
   - Fill Technical Context from research documents (architecture-research.md, tech-stack-research.md)
   - Reference data model from data-research.md (no need to recreate)
   - Reference business rules from business-rules-research.md
   - Reference MCP servers from context files if available
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Reference existing research documents instead of generating new research.md
   - Phase 1: Cite data-research.md for data model (don't regenerate), generate contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design
   - **CRITICAL**: All technical decisions must cite specific research document sections (e.g., "Per architecture-research.md#component-design, we use microservices...")

   **If Feature Mode:**
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

#### If Project Mode:

**Prerequisites**: Research documents already exist from `/speckit.research` phase.

1. **Load Technical Context from Research**:
   - **Architecture**: Reference `.specify/research/technical/architecture-research.md`
   - **Tech Stack**: Reference `.specify/research/technical/tech-stack-research.md`
   - **Data Model**: Reference `.specify/research/technical/data-research.md`

2. **Extract Decisions for Implementation Plan**:

   From **architecture-research.md**:
   - Component architecture (monolith vs microservices vs serverless)
   - Integration patterns (REST, GraphQL, events, messaging)
   - Deployment architecture (cloud provider, containerization, orchestration)
   - Scalability strategy (horizontal, vertical, caching, CDN)

   From **tech-stack-research.md**:
   - Programming languages and versions
   - Frameworks and libraries
   - Database technology and ORM
   - Infrastructure and DevOps tools
   - Testing frameworks
   - Security tools

   From **data-research.md**:
   - Entity model (already designed in research)
   - Storage architecture (database type, schema design)
   - Data migration strategy
   - Data validation rules (cross-reference business-rules-research.md)

3. **Cite Research in Plan**:

   When filling implementation plan sections, reference research documents:
   ```markdown
   ## Technical Decisions

   ### Architecture
   **Decision**: Microservices architecture
   **Source**: [Architecture Research](.specify/research/technical/architecture-research.md#component-architecture)
   **Rationale**: Per research, microservices chosen for scalability and team autonomy

   ### Tech Stack
   **Languages**: Python 3.11, TypeScript 5.0
   **Frameworks**: FastAPI (backend), React 18 (frontend)
   **Source**: [Tech Stack Research](.specify/research/technical/tech-stack-research.md#recommendations)
   **Rationale**: Selected based on team expertise and ecosystem maturity

   ### Data Storage
   **Database**: PostgreSQL 15
   **ORM**: SQLAlchemy
   **Source**: [Data Research](.specify/research/technical/data-research.md#storage-recommendations)
   **Rationale**: ACID compliance required for financial transactions
   ```

4. **Validate Plan Against Research**:

   Check that plan decisions align with research:
   - [ ] Tech stack matches tech-stack-research.md recommendations
   - [ ] Architecture aligns with architecture-research.md design
   - [ ] Data model implements data-research.md entity relationships
   - [ ] Business logic reflects business-rules-research.md
   - [ ] Security implements security-research.md requirements
   - [ ] Performance targets match performance-research.md

   **If conflicts exist**: Flag as warnings and document justification for deviation.

**Output**: Implementation plan with extensive research citations, no separate research.md needed.

---

#### If Feature Mode (Backward Compatible):

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

#### If Project Mode:

**Prerequisites**: Research documents loaded from `/speckit.research` phase.

1. **Reference Data Model from Research**:
   - **Source**: `.specify/research/technical/data-research.md`
   - Do NOT create new data-model.md - reference existing research
   - Cross-reference business rules from `.specify/research/domain/business-rules-research.md`
   - Note any implementation-specific refinements needed

2. **Generate API Contracts** from PRD functional requirements:
   - Load features from `.specify/spec.md`
   - For each user action → endpoint design
   - Use patterns from `.specify/research/technical/architecture-research.md`
   - Output OpenAPI/GraphQL schema to `/contracts/`
   - **Cite research**: "API design follows REST patterns per architecture-research.md#integration-patterns"

3. **Generate Quickstart Guide**:
   - Reference tech stack from `.specify/research/technical/tech-stack-research.md`
   - Setup instructions for chosen technologies
   - Development environment configuration

4. **Agent Context Update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add technology from tech-stack-research.md
   - Preserve manual additions between markers

**Output**: /contracts/*, quickstart.md, agent-specific file
**Note**: No data-model.md created (use data-research.md instead)

---

#### If Feature Mode (Backward Compatible):

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
