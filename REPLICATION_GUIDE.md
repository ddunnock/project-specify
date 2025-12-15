# Replication Guide: Research-Driven Workflow Implementation

## Overview

This guide documents how to replicate the research-driven, project-centric workflow changes from the **Claude agent** to all other agents in the project-specify system.

**Reference Implementation**: `src/specify_cli/agents/claude/commands/`

**Agents to Update**:
- amp
- auggie
- bob
- codebuddy
- codex
- cursor-agent
- kilocode
- opencode
- q
- qoder
- roo
- shai
- windsurf

Total: **13 agents** (Claude already complete)

---

## What Changed

The implementation adds a **research phase** that runs BEFORE specification, creating foundational project understanding through structured research documents. This transforms the workflow from feature-centric to project-centric.

**New Workflow**:
```
constitution → research → specify (PRD) → plan → tasks → implement
```

**Backward Compatibility**: Feature-centric workflow still supported via mode detection.

---

## Files Modified Per Agent

For each agent in `src/specify_cli/agents/{agent}/commands/`, update these 4 files:

### 1. `speckit.constitution.md`
**Changes**: Add "Next Steps: Preparing for Research Phase" section
**Location**: After step 8, before "Formatting & Style Requirements"
**Size**: +65 lines

### 2. `speckit.research.md`
**Changes**: Complete rewrite with Project Research Mode + Implementation Research Mode
**Location**: Entire file
**Size**: 90 lines → 633 lines (+543 lines)

### 3. `speckit.specify.md`
**Changes**: Add Project Mode workflow + mode detection
**Location**: After "## Outline" heading, before feature workflow
**Size**: +270 lines

### 4. `speckit.plan.md`
**Changes**: Add research-aware planning + mode detection
**Location**: Update "Pre-Planning: Context Loading" and "Phase 0"
**Size**: +145 lines

---

## Detailed Replication Steps

### Step 1: Update `speckit.constitution.md`

#### Location to Insert
Find the line:
```markdown
8. Output a final summary to the user with:
```

After this step (after the suggested commit message), insert the following section BEFORE "Formatting & Style Requirements":

#### Content to Add

```markdown
## Next Steps: Preparing for Research Phase

After the constitution is established, you can optionally prepare for the `/speckit.research` phase by filling out research seed templates.

### Research Seed Templates Available

Optional seed file templates are provided to help guide comprehensive project research:
**Location:** `templates/research-seeds/`

**Categories Available:**

**Technical Research:**
- `technical/data-research.seed.md` - Data entities, relationships, storage requirements
- `technical/architecture-research.seed.md` - System architecture, components, integration
- `technical/tech-stack-research.seed.md` - Technologies, frameworks, infrastructure, tools

**Domain Research:**
- `domain/domain-research.seed.md` - Business domain, industry context, core concepts
- `domain/business-rules-research.seed.md` - Business rules, validation logic, calculations
- `domain/workflow-research.seed.md` - Business processes, workflows, decision points

**User Research:**
- `user/user-research.seed.md` - User needs, pain points, goals, context
- `user/personas-research.seed.md` - User roles, characteristics, motivations
- `user/journey-maps-research.seed.md` - User journeys, touchpoints, emotions

**Constraints Research:**
- `constraints/compliance-research.seed.md` - Regulatory requirements, audit needs
- `constraints/security-research.seed.md` - Security requirements, threat model
- `constraints/performance-research.seed.md` - Performance targets, scalability, SLAs

### How to Use Seed Templates

1. **Copy templates to your project** (optional):
   ```bash
   mkdir -p .specify/research-seeds/{technical,domain,user,constraints}
   cp templates/research-seeds/technical/*.seed.md .specify/research-seeds/technical/
   cp templates/research-seeds/domain/*.seed.md .specify/research-seeds/domain/
   cp templates/research-seeds/user/*.seed.md .specify/research-seeds/user/
   cp templates/research-seeds/constraints/*.seed.md .specify/research-seeds/constraints/
   ```

2. **Fill out relevant seed files** using a text editor:
   - Answer the prompting questions in each template
   - Fill in sections that are relevant to your project
   - Leave sections blank if not applicable or to be determined later

3. **Run `/speckit.research`**:
   - The AI will read your seed files
   - Ask clarifying questions for any gaps
   - Generate comprehensive research documents in `.specify/research/`

**Seed files are completely optional** - if you don't provide them, the AI will guide you through research interactively by asking questions. However, seed files allow you to prepare your thinking in advance and provide more structured input.

### Recommended Workflow

After completing the constitution:
1. **(Optional)** Fill out research seed templates that are relevant to your project
2. Run `/speckit.research` to conduct foundational project research
3. Run `/speckit.specify` to create project-level PRD (references research)
4. Run `/speckit.plan` to create technical implementation plan
5. Run `/speckit.tasks` to generate detailed task breakdown
6. Run `/speckit.implement` to begin execution

The research phase establishes a solid foundation of project understanding across technical, domain, user, and constraint dimensions that will inform all subsequent planning and implementation.
```

#### Validation
- [ ] Section appears after step 8 summary
- [ ] Section appears before "Formatting & Style Requirements"
- [ ] All 12 research seed templates are listed
- [ ] Bash commands for copying templates are correct

---

### Step 2: Replace `speckit.research.md`

#### Complete File Replacement

**Source**: `src/specify_cli/agents/claude/commands/speckit.research.md`
**Target**: `src/specify_cli/agents/{agent}/commands/speckit.research.md`

**Action**: Copy the entire contents of the Claude version to each agent.

#### Key Sections in New File
1. **Project Research Mode (Primary Workflow)** - Lines 15-436
   - Step 1: Detect Project Mode
   - Step 2: Check for Research Seed Files
   - Step 3: Determine Research Scope
   - Step 4: Gather Information
   - Step 5: Generate Research Documents
   - Step 6: Create Research Index
   - Step 7: Validate Research
   - Step 8: Summarize and Next Steps

2. **Iterative Research Updates** - Lines 439-462
   - `/speckit.research --update [category]` support

3. **Research Seed File Guide** - Lines 465-486

4. **Implementation Research Mode (Legacy)** - Lines 490-556
   - Backward compatible feature-level research

#### Validation
- [ ] File has ~633 lines
- [ ] "Project Research Mode" section exists
- [ ] "Implementation Research Mode (Legacy)" section exists
- [ ] Research seed file guidance included
- [ ] 8-step workflow documented
- [ ] 12 research categories listed (technical, domain, user, constraints)

---

### Step 3: Update `speckit.specify.md`

#### Location to Modify

Find the line:
```markdown
## Outline
```

Replace the entire section starting with "## Outline" through "Given that feature description, do this:" with the following:

#### Content to Replace With

```markdown
## Outline

This command supports two modes based on project structure:

- **Project Mode**: Creates a single project-level PRD (`.specify/spec.md`) that references research documents
- **Feature Mode**: Creates feature-specific specs (`.specify/specs/###-feature-name/spec.md`) - backward compatible

### Step 0: Detect Project Mode

Before proceeding, detect which mode to use:

```bash
bash scripts/bash/detect-project-mode.sh
```

**Mode Detection Logic:**
- If `.specify/research/README.md` exists OR `.specify/spec.md` exists → **Project Mode**
- If `.specify/specs/` exists with numbered feature directories → **Feature Mode**
- If neither exists → **Unknown** (default to Feature Mode or ask user)

**Based on detected mode:**
- **Project Mode** → Follow **Project Mode Workflow** (below)
- **Feature Mode** → Follow **Feature Mode Workflow** (original behavior)

---

## Project Mode Workflow

> **When to use**: After `/speckit.research` has generated foundational research documents
> **Output**: Single `.specify/spec.md` (PRD-style specification)
> **References**: Extensively links to `.specify/research/**/*.md` documents

### Purpose

Create a comprehensive Product Requirements Document (PRD) that serves as the single source of truth for the entire project, with features organized as chapters and all requirements validated against research documents.

### Execution Flow

#### 1. Load Research Foundation

Read all research documents to understand project context:

```bash
# Check research index
cat .specify/research/README.md

# Load research by category
ls -la .specify/research/technical/*.md
ls -la .specify/research/domain/*.md
ls -la .specify/research/user/*.md
ls -la .specify/research/constraints/*.md
```

**Research Documents to Load:**

**Technical Research:**
- `.specify/research/technical/data-research.md` - Data entities, relationships, storage
- `.specify/research/technical/architecture-research.md` - System architecture, components
- `.specify/research/technical/tech-stack-research.md` - Technology choices, frameworks

**Domain Research:**
- `.specify/research/domain/domain-research.md` - Business domain, core concepts
- `.specify/research/domain/business-rules-research.md` - Business rules, validation logic
- `.specify/research/domain/workflow-research.md` - Business processes, workflows

**User Research:**
- `.specify/research/user/user-research.md` - User needs, pain points, goals
- `.specify/research/user/personas-research.md` - User roles, characteristics
- `.specify/research/user/journey-maps-research.md` - User journeys, touchpoints

**Constraints Research:**
- `.specify/research/constraints/compliance-research.md` - Regulatory requirements
- `.specify/research/constraints/security-research.md` - Security requirements
- `.specify/research/constraints/performance-research.md` - Performance targets, scalability

#### 2. Load PRD Template

Load the project specification template:

```bash
cat templates/project-spec-template.md
```

This template provides the structure for the project-level PRD with extensive research references.

#### 3. Extract User Input

Parse the user's specification request:
- If user provided specific features to add: Use those as starting features in the PRD
- If this is initial PRD creation: Generate comprehensive feature set based on research
- If updating existing PRD: Load `.specify/spec.md` and update specific sections

#### 4. Generate Executive Summary

Based on research documents, create:

**Vision Statement:**
- Extract from `.specify/research/user/user-research.md` - user goals and needs
- Synthesize with `.specify/research/domain/domain-research.md` - business domain context

**Business Objectives:**
- Reference `.specify/research/domain/workflow-research.md` - business processes
- Align with `.specify/memory/constitution.md` - project principles

**Target Users:**
- Summarize from `.specify/research/user/personas-research.md`
- Link to detailed persona research

**Success Criteria:**
- Extract from `.specify/research/user/user-research.md` - user success metrics
- Add performance targets from `.specify/research/constraints/performance-research.md`

#### 5. Document Research Foundation

Create "Research Foundation" section linking to all research documents:

```markdown
## Research Foundation

This specification is informed by comprehensive research across four dimensions:

### Technical Research
**Location:** `.specify/research/technical/`

- **[Data Research](./research/technical/data-research.md)** - [Brief summary from doc]
- **[Architecture Research](./research/technical/architecture-research.md)** - [Brief summary from doc]
- **[Tech Stack Research](./research/technical/tech-stack-research.md)** - [Brief summary from doc]

**Key Findings:**
[Extract 3-5 key technical decisions from research documents]

### Domain Research
**Location:** `.specify/research/domain/`
[Same pattern...]

### User Research
**Location:** `.specify/research/user/`
[Same pattern...]

### Constraints Research
**Location:** `.specify/research/constraints/`
[Same pattern...]
```

#### 6. Generate Functional Requirements

For each feature (provided by user or inferred from research):

```markdown
### Feature N: [Feature Name]

**Priority:** P1 (MVP) | P2 (Enhancement) | P3 (Future)

**Research References:**
- **Domain:** [Workflow Research](.specify/research/domain/workflow-research.md#section-name) - [Specific section]
- **User:** [User Research](.specify/research/user/user-research.md#need-reference) - [User need this addresses]
- **Technical:** [Architecture Research](.specify/research/technical/architecture-research.md#component-name) - [Architecture component]

**Description:**
[Feature description based on user input and research]

**User Stories:**

#### Story N.1: [Story Title]
**As a** [persona from personas-research.md],
**I want** [goal],
**So that** [benefit from user-research.md].

**Acceptance Criteria:**
- [ ] [Criterion 1 - reference business-rules-research.md if applicable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Validation Check:**
- **Business Rule:** [Business Rules Research](.specify/research/domain/business-rules-research.md#rule-id) - [Specific rule to validate against]
- **User Journey:** [Journey Maps Research](.specify/research/user/journey-maps-research.md#journey-id) - [Journey step this addresses]

**Dependencies:**
- [Dependencies from architecture-research.md]

**Assumptions:**
- [Assumptions - note any not covered in research]
```

**Important**:
- Every feature MUST reference at least one research document
- Acceptance criteria MUST link to business rules research when validation logic exists
- User stories MUST reference specific personas from personas-research.md
- Technical requirements MUST align with architecture-research.md decisions

#### 7. Generate Non-Functional Requirements

Extract from constraints research:

```markdown
## Non-Functional Requirements

> **Reference:** [Constraints Research](.specify/research/constraints/)

### Performance Requirements
**Source:** [Performance Research](.specify/research/constraints/performance-research.md)

[Table of performance targets from research]

### Security Requirements
**Source:** [Security Research](.specify/research/constraints/security-research.md)

- **Authentication:** [From security-research.md]
- **Authorization:** [From security-research.md]
- **Data Protection:** [From security-research.md]
- **Compliance:** See [Compliance Research](.specify/research/constraints/compliance-research.md)

### Scalability Requirements
**Source:** [Performance Research](.specify/research/constraints/performance-research.md#scalability)

[Scalability targets from research]

### Compliance Requirements
**Source:** [Compliance Research](.specify/research/constraints/compliance-research.md)

- **Regulations:** [From compliance-research.md]
- **Certifications:** [From compliance-research.md]
- **Audit Requirements:** [From compliance-research.md]
```

#### 8. Generate Technical Architecture Section

Summarize from architecture research:

```markdown
## Technical Architecture

> **Reference:** [Architecture Research](.specify/research/technical/architecture-research.md)

### High-Level Architecture

[Architecture diagram or description from architecture-research.md]

**Key Components:**
[List components from architecture-research.md]

**For detailed component design, see:** [Architecture Research](.specify/research/technical/architecture-research.md)

### Technology Stack

> **Reference:** [Tech Stack Research](.specify/research/technical/tech-stack-research.md)

[Table of technologies from tech-stack-research.md]

**For detailed technology decisions, see:** [Tech Stack Research](.specify/research/technical/tech-stack-research.md)
```

#### 9. Generate Data Model Section

Summarize from data research:

```markdown
## Data Model

> **Reference:** [Data Research](.specify/research/technical/data-research.md)

### Key Entities

[Entity summary from data-research.md]

**For complete entity relationships and data dictionary, see:** [Data Research](.specify/research/technical/data-research.md)
```

#### 10. Validate Against Research

Check that the PRD aligns with research:

1. **Cross-reference check:**
   - Do all features reference relevant research documents?
   - Are business rules from business-rules-research.md reflected in acceptance criteria?
   - Do personas match personas-research.md?
   - Do tech choices align with tech-stack-research.md recommendations?

2. **Consistency check:**
   - Are there conflicts between spec requirements and research recommendations?
   - Flag any spec decisions that contradict research findings

3. **Completeness check:**
   - Are there critical research findings not reflected in the spec?
   - Are there features in the spec that lack research foundation?

**Output validation report:**
```
PRD Validation Report:

✓ All features reference research documents
✓ Business rules aligned with business-rules-research.md
⚠ Warning: Feature X proposes technology not in tech-stack-research.md
⚠ Warning: No feature addresses user need Y from user-research.md

Recommend: Review warnings before proceeding to planning phase.
```

#### 11. Write PRD to .specify/spec.md

Apply the `templates/project-spec-template.md` with all generated content and research references.

Write the complete PRD to:
```
.specify/spec.md
```

#### 12. Create PRD Quality Checklist

Generate validation checklist at `.specify/checklists/prd-quality.md`:

```markdown
# PRD Quality Checklist

**Purpose**: Validate PRD completeness and research alignment
**Created**: [DATE]
**PRD**: [Link to .specify/spec.md]

## Research Alignment

- [ ] All features reference at least one research document
- [ ] Business rules match business-rules-research.md
- [ ] Personas match personas-research.md
- [ ] Architecture aligns with architecture-research.md
- [ ] Tech stack matches tech-stack-research.md recommendations
- [ ] NFRs sourced from constraints research

## Content Quality

- [ ] Executive summary is clear and compelling
- [ ] Vision statement aligns with user research
- [ ] Success criteria are measurable and technology-agnostic
- [ ] All mandatory sections completed
- [ ] Research references are specific (link to sections, not just documents)

## Feature Completeness

- [ ] Each feature has clear acceptance criteria
- [ ] User stories reference specific personas
- [ ] Validation checks link to business rules
- [ ] Dependencies identified from research
- [ ] Priorities assigned (P1/P2/P3)

## Validation

- [ ] No conflicts between spec and research
- [ ] All critical research findings reflected in spec
- [ ] No unvalidated assumptions (all should be in research)

## Notes

[Document any issues or warnings from validation]
```

#### 13. Report Completion

Output summary:
```
Project PRD Created!

Location: .specify/spec.md
Template: templates/project-spec-template.md

Research Documents Referenced:
- Technical: 3 documents
- Domain: 3 documents
- User: 3 documents
- Constraints: 3 documents

Features Specified: N features (P1: X, P2: Y, P3: Z)

Validation: [Pass/Warnings]
- [List any validation warnings]

Quality Checklist: .specify/checklists/prd-quality.md

Next Steps:
1. Review PRD and validation warnings
2. Run /speckit.plan to create technical implementation plan
3. Plan will reference research documents for technical decisions
```

---

## Feature Mode Workflow

> **When to use**: Legacy feature-centric workflow (backward compatible)
> **Output**: `.specify/specs/###-feature-name/spec.md`

The text the user typed after `/speckit.specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:
```

**Note**: After this section, the original feature mode workflow continues unchanged (steps 1-7 from the original file).

#### Validation
- [ ] Mode detection section added at top
- [ ] Project Mode Workflow section complete (13 steps)
- [ ] Feature Mode Workflow preserved
- [ ] Research document references included
- [ ] PRD validation logic present

---

### Step 4: Update `speckit.plan.md`

#### Part A: Replace "Pre-Planning: Context Loading" Section

Find the section starting with:
```markdown
## Pre-Planning: Context Loading
```

Replace it with:

```markdown
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
```

#### Part B: Update Step 3 in "Outline" Section

Find step 3 in the Outline section:
```markdown
3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
```

Replace with:

```markdown
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
```

#### Part C: Replace "Phase 0: Outline & Research" Section

Find the section:
```markdown
### Phase 0: Outline & Research
```

Replace the entire Phase 0 section with:

```markdown
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
```

#### Part D: Replace "Phase 1: Design & Contracts" Section

Find the section:
```markdown
### Phase 1: Design & Contracts
```

Replace the entire Phase 1 section with:

```markdown
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
```

#### Validation
- [ ] Pre-Planning section updated with mode detection
- [ ] Step 3 in Outline updated with dual workflows
- [ ] Phase 0 updated with research referencing
- [ ] Phase 1 updated to skip data-model.md in project mode
- [ ] Research citations format included

---

## Replication Script (Automated)

To automate the replication process, use this bash script:

```bash
#!/bin/bash
# Replicate research-driven workflow changes from Claude agent to all other agents

SOURCE_AGENT="claude"
TARGET_AGENTS=("amp" "auggie" "bob" "codebuddy" "codex" "cursor-agent" "kilocode" "opencode" "q" "qoder" "roo" "shai" "windsurf")

SOURCE_DIR="src/specify_cli/agents/$SOURCE_AGENT/commands"

echo "Replicating research-driven workflow from $SOURCE_AGENT to ${#TARGET_AGENTS[@]} agents..."

for agent in "${TARGET_AGENTS[@]}"; do
    TARGET_DIR="src/specify_cli/agents/$agent/commands"

    echo ""
    echo "Processing agent: $agent"

    # Copy complete research command
    echo "  - Copying speckit.research.md..."
    cp "$SOURCE_DIR/speckit.research.md" "$TARGET_DIR/speckit.research.md"

    # Copy updated commands (TODO: These need manual review for agent-specific differences)
    echo "  - Copying speckit.constitution.md..."
    cp "$SOURCE_DIR/speckit.constitution.md" "$TARGET_DIR/speckit.constitution.md"

    echo "  - Copying speckit.specify.md..."
    cp "$SOURCE_DIR/speckit.specify.md" "$TARGET_DIR/speckit.specify.md"

    echo "  - Copying speckit.plan.md..."
    cp "$SOURCE_DIR/speckit.plan.md" "$TARGET_DIR/speckit.plan.md"

    echo "  ✓ Completed $agent"
done

echo ""
echo "Replication complete!"
echo ""
echo "IMPORTANT: Please review each agent's files for agent-specific customizations."
echo "Some agents may have unique configurations that need to be preserved."
```

**Note**: This script does a direct copy. Review each agent afterward for any agent-specific configurations that may have been overwritten.

---

## Testing Checklist

After replicating changes to each agent, test the following:

### Per Agent Testing

For each agent in `{amp, auggie, bob, codebuddy, codex, cursor-agent, kilocode, opencode, q, qoder, roo, shai, windsurf}`:

#### 1. Constitution Command
- [ ] File exists: `src/specify_cli/agents/{agent}/commands/speckit.constitution.md`
- [ ] "Next Steps: Preparing for Research Phase" section present
- [ ] All 12 research seed templates listed
- [ ] Recommended workflow documented

#### 2. Research Command
- [ ] File exists: `src/specify_cli/agents/{agent}/commands/speckit.research.md`
- [ ] File is ~633 lines
- [ ] Project Research Mode section complete
- [ ] Implementation Research Mode section complete
- [ ] 8-step workflow documented
- [ ] Research seed file detection logic present

#### 3. Specify Command
- [ ] File exists: `src/specify_cli/agents/{agent}/commands/speckit.specify.md`
- [ ] Mode detection section at top
- [ ] Project Mode Workflow complete (13 steps)
- [ ] Feature Mode Workflow preserved
- [ ] Research document references throughout

#### 4. Plan Command
- [ ] File exists: `src/specify_cli/agents/{agent}/commands/speckit.plan.md`
- [ ] Pre-Planning section has mode detection
- [ ] Phase 0 references research documents in project mode
- [ ] Phase 1 skips data-model.md in project mode
- [ ] Research citation format included

### Integration Testing

Test the complete workflow with one agent:

1. **Test Project Mode Workflow**:
   ```bash
   # Initialize
   /speckit.constitution

   # Create research (with seed files)
   /speckit.research

   # Create PRD
   /speckit.specify

   # Create plan
   /speckit.plan
   ```

   Validate:
   - [ ] Research documents created in `.specify/research/`
   - [ ] PRD created at `.specify/spec.md`
   - [ ] PRD references research documents
   - [ ] Plan cites research documents
   - [ ] No data-model.md created (uses data-research.md)

2. **Test Feature Mode Workflow** (backward compatibility):
   ```bash
   # Initialize
   /speckit.constitution

   # Create feature spec
   /speckit.specify Add user authentication

   # Create plan
   /speckit.plan
   ```

   Validate:
   - [ ] Feature spec created in `.specify/specs/001-user-authentication/spec.md`
   - [ ] research.md created
   - [ ] data-model.md created
   - [ ] Original workflow unchanged

3. **Test Mode Detection**:
   ```bash
   bash scripts/bash/detect-project-mode.sh
   ```

   Validate:
   - [ ] Returns "project" when `.specify/research/README.md` exists
   - [ ] Returns "feature" when `.specify/specs/` exists
   - [ ] Returns "unknown" otherwise

---

## Common Issues and Solutions

### Issue 1: Agent-Specific Configurations Lost

**Problem**: Some agents have unique configurations in command files that get overwritten.

**Solution**:
- Before copying, diff each file: `diff src/specify_cli/agents/claude/commands/speckit.research.md src/specify_cli/agents/amp/commands/speckit.research.md`
- Manually merge agent-specific sections

### Issue 2: Script Paths Differ

**Problem**: Some agents may reference scripts differently.

**Solution**:
- Check script references in each command file
- Ensure paths are relative to project root

### Issue 3: Handoff Agents Differ

**Problem**: Different agents may hand off to different specialized agents.

**Solution**:
- Review `handoffs:` section in frontmatter
- Preserve agent-specific handoff configurations

---

## Rollback Procedure

If issues arise, rollback using git:

```bash
# Rollback specific agent
git checkout HEAD -- src/specify_cli/agents/{agent}/commands/

# Rollback all agents
git checkout HEAD -- src/specify_cli/agents/*/commands/
```

---

## Completion Checklist

- [ ] All 13 agents updated with 4 command files each (52 files total)
- [ ] Automated replication script tested
- [ ] Integration testing completed for at least 2 agents
- [ ] Mode detection validated
- [ ] Backward compatibility confirmed
- [ ] Documentation updated
- [ ] Changes committed to git

---

## Summary

**Files Modified**: 52 (13 agents × 4 commands)
**Lines Added**: ~1,023 lines per agent
**Total Lines Added**: ~13,299 lines

**Effort Estimate**:
- Automated copy: 5 minutes
- Manual review: 2-3 hours
- Testing: 1-2 hours
- **Total**: 3-5 hours

---

## Next Steps After Replication

1. Run full test suite
2. Update main README with new workflow documentation
3. Create example project demonstrating research phase
4. Update CLI help text
5. Publish release notes
