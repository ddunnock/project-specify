---
description: Conduct comprehensive project research OR targeted implementation research
---

# Research Assistant

Conduct research to inform project planning and implementation decisions.

**Two Research Modes:**
1. **Project Research** - Foundational research BEFORE specification (new)
2. **Implementation Research** - Targeted research for specific technologies/patterns (legacy)

---

## Project Research Mode (Primary Workflow)

> **When to use:** At project inception, after constitution, BEFORE creating specification
> **Output:** `.specify/research/` with categorized research documents
> **Next step:** `/speckit.specify` to create project-level PRD

### Purpose

Establish comprehensive project understanding across four research dimensions:
- **Technical:** Data, architecture, technology stack
- **Domain:** Business domain, rules, workflows
- **User:** User needs, personas, journeys
- **Constraints:** Compliance, security, performance

### Workflow

#### Step 1: Detect Project Mode

Run mode detection:
```bash
bash scripts/bash/detect-project-mode.sh
```

- If "project" or "unknown" → Use Project Research workflow
- If "feature" → Use Implementation Research workflow (legacy)

#### Step 2: Check for Research Seed Files

Look for `.specify/research-seeds/` directory and check for seed files:

```bash
ls -la .specify/research-seeds/technical/
ls -la .specify/research-seeds/domain/
ls -la .specify/research-seeds/user/
ls -la .specify/research-seeds/constraints/
```

**Found seed files?**
- Read each seed file to understand user's input
- Note which sections are filled vs. blank
- Use seed content as foundation for research

**No seed files?**
- Proceed with interactive clarification (Step 3)
- Guide user through research needs

#### Step 3: Determine Research Scope

Ask the user which research areas are relevant:

```
Which research categories are needed for this project?

Technical Research:
- [ ] Data Research (entities, relationships, storage)
- [ ] Architecture Research (components, integration, deployment)
- [ ] Tech Stack Research (languages, frameworks, infrastructure)

Domain Research:
- [ ] Domain Research (business domain, concepts, terminology)
- [ ] Business Rules Research (validation, calculations, workflows)
- [ ] Workflow Research (processes, decision points, actors)

User Research:
- [ ] User Research (user needs, pain points, goals)
- [ ] Personas Research (user roles, characteristics, motivations)
- [ ] Journey Maps Research (user journeys, touchpoints, emotions)

Constraints Research:
- [ ] Compliance Research (regulations, audit requirements)
- [ ] Security Research (authentication, authorization, threats)
- [ ] Performance Research (scalability, latency, availability)

Select the categories relevant to your project.
```

#### Step 4: Gather Information

For each selected research category:

**If seed file exists:**
1. Read seed file content
2. Identify filled sections (user provided input)
3. Identify blank sections (need clarification)
4. Ask targeted follow-up questions (max 5 per category)

**If no seed file:**
1. Reference seed template prompts from `templates/research-seeds/`
2. Ask key questions for this category (max 5-7 questions)
3. Guide user through what information is needed

**Example Questions (Data Research):**
```
For Data Research:
1. What are the main data entities your system will manage?
2. How do these entities relate to each other?
3. Where should data be stored? (Database type, file storage, etc.)
4. Are there regulatory requirements for data storage?
5. What is the expected data volume?
```

**Note:** Mark any research as "deferred" if user doesn't have answers yet. This can be filled in later with `/speckit.research --update [category]`.

#### Step 5: Generate Research Documents

For each selected research category, create comprehensive research document in `.specify/research/[category]/`:

**Document Structure (following templates from `templates/research-templates/`):**

```markdown
# [Category] Research

> **Status:** Complete | Partial | Deferred
> **Last Updated:** YYYY-MM-DD HH:MM
> **Version:** X.X

---

## Document Purpose

[What this research document covers]

---

## Research Foundation

### Seed File Input

[If seed file was provided, quote relevant sections:]

> **User Input:**
> [Quoted content from seed file]

### Clarifying Questions & Answers

**Q1:** [Question asked]
**A1:** [User's answer]

**Q2:** [Question asked]
**A2:** [User's answer]

---

## AI Analysis

### Key Findings

1. **Finding 1:** [Analysis based on user input]
   - Implication:
   - Recommendation:

2. **Finding 2:** [Analysis]
   - Implication:
   - Recommendation:

---

## Recommendations

### Primary Recommendations

1. **Recommendation:** [Specific recommendation]
   - **Rationale:** [Why this is recommended]
   - **Alternatives Considered:** [Other options]
   - **Trade-offs:** [Pros and cons]

2. **Recommendation:** [Specific recommendation]
   - **Rationale:**
   - **Alternatives Considered:**
   - **Trade-offs:**

---

## Technical Details

[Category-specific technical content]

For Data Research:
- Entity relationship diagram
- Data dictionary
- Storage recommendations

For Architecture Research:
- Component diagram
- Integration patterns
- Deployment architecture

For Tech Stack Research:
- Technology comparison matrix
- Version recommendations
- Dependency analysis

---

## Implementation Guidance

- Implementation notes specific to this project
- Integration points with other research
- Validation criteria

---

## Risks & Considerations

1. **Risk:** [Identified risk]
   - **Mitigation:** [How to address]

2. **Risk:** [Identified risk]
   - **Mitigation:**

---

## References

- [Documentation links]
- [Industry standards]
- [Best practices]

---

## Cross-References

This research informs:
- [Link to related research document]
- [Link to specification sections]

This research depends on:
- [Link to prerequisite research]

---

## Version History

| Date | Version | Changes | Status |
|------|---------|---------|--------|
| YYYY-MM-DD | 1.0 | Initial research | Complete |

---

## Deferred Items

[Items marked for later research or requiring more information]

1. [Item to research later]
2. [Item needing stakeholder input]

```

**File Naming:**
- `.specify/research/technical/data-research.md`
- `.specify/research/technical/architecture-research.md`
- `.specify/research/technical/tech-stack-research.md`
- `.specify/research/domain/domain-research.md`
- `.specify/research/domain/business-rules-research.md`
- `.specify/research/domain/workflow-research.md`
- `.specify/research/user/user-research.md`
- `.specify/research/user/personas-research.md`
- `.specify/research/user/journey-maps-research.md`
- `.specify/research/constraints/compliance-research.md`
- `.specify/research/constraints/security-research.md`
- `.specify/research/constraints/performance-research.md`

#### Step 6: Create Research Index

Generate `.specify/research/README.md` with overview of all research:

```markdown
# Project Research Index

> **Project:** [Project Name]
> **Last Updated:** YYYY-MM-DD
> **Research Status:** In Progress | Complete

---

## Research Overview

This directory contains comprehensive project research across four categories:

### Technical Research
Research about data, architecture, and technology choices.

| Document | Status | Last Updated | Summary |
|----------|--------|--------------|---------|
| [Data Research](technical/data-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |
| [Architecture Research](technical/architecture-research.md) | ⚠ Partial | YYYY-MM-DD | [Brief summary] |
| [Tech Stack Research](technical/tech-stack-research.md) | ○ Deferred | - | Not yet started |

### Domain Research
Research about business domain, rules, and workflows.

| Document | Status | Last Updated | Summary |
|----------|--------|--------------|---------|
| [Domain Research](domain/domain-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |
| [Business Rules Research](domain/business-rules-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |
| [Workflow Research](domain/workflow-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |

### User Research
Research about users, personas, and journeys.

| Document | Status | Last Updated | Summary |
|----------|--------|--------------|---------|
| [User Research](user/user-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |
| [Personas Research](user/personas-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |
| [Journey Maps Research](user/journey-maps-research.md) | ⚠ Partial | YYYY-MM-DD | [Brief summary] |

### Constraints Research
Research about compliance, security, and performance.

| Document | Status | Last Updated | Summary |
|----------|--------|--------------|---------|
| [Compliance Research](constraints/compliance-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |
| [Security Research](constraints/security-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |
| [Performance Research](constraints/performance-research.md) | ✓ Complete | YYYY-MM-DD | [Brief summary] |

---

## Key Findings Summary

### Critical Decisions
1. [Key decision from research]
2. [Key decision from research]

### Major Risks
1. [Risk identified in research]
2. [Risk identified in research]

### Deferred Research
- [Items deferred for later]

---

## Research Completeness

- Technical: [X/3] documents complete
- Domain: [X/3] documents complete
- User: [X/3] documents complete
- Constraints: [X/3] documents complete

**Overall:** [X/12] research documents complete

---

## How to Update Research

To update or add research:
```bash
/speckit.research --update [category]
```

Example:
```bash
/speckit.research --update data
```

---

## Next Steps

Once research is sufficient:
1. Run `/speckit.specify` to create project-level PRD
2. PRD will reference these research documents for validation
3. Plan will use research for technical decisions

```

#### Step 7: Validate Research

Check research for internal consistency:

1. **Cross-document consistency:**
   - Do tech stack choices align with architecture decisions?
   - Do business rules match workflow descriptions?
   - Are persona needs reflected in user research?

2. **Completeness check:**
   - Are there critical gaps in research?
   - Should additional categories be researched?
   - Are deferred items clearly marked?

3. **Quality check:**
   - Are recommendations specific and actionable?
   - Are trade-offs clearly explained?
   - Are risks identified with mitigations?

**Output validation report:**
```
Research Validation Report:

✓ All selected research categories completed
✓ No conflicts detected between research documents
⚠ 2 items deferred for later research:
  - Performance testing strategy (deferred until MVP)
  - Internationalization requirements (deferred until Phase 2)

Ready to proceed to specification phase.
```

#### Step 8: Summarize and Next Steps

```
Research Phase Complete!

Generated Research Documents:
- Technical: 3 documents
- Domain: 3 documents
- User: 2 documents (1 deferred)
- Constraints: 3 documents

Total: 11 research documents created

Research Index: .specify/research/README.md

Next Steps:
1. Run /speckit.specify to create project-level PRD
2. PRD will reference research documents for:
   - Feature requirements validation
   - Technical architecture decisions
   - Non-functional requirements
   - Success criteria definition
```

---

## Iterative Research Updates

To update existing research or add deferred research:

```bash
/speckit.research --update [category]
```

**Examples:**
```bash
/speckit.research --update data        # Update data-research.md
/speckit.research --update performance # Add/update performance-research.md
/speckit.research --update all         # Review and update all research
```

**Update Workflow:**
1. Read existing research document
2. Show current content to user
3. Ask what needs to be updated
4. Update specific sections
5. Increment version number
6. Add entry to version history
7. Update research index

---

## Research Seed File Guide

To prepare for research, users can optionally fill out seed files BEFORE running `/speckit.research`.

**How to use seed files:**

1. Copy seed templates to project:
```bash
mkdir -p .specify/research-seeds/{technical,domain,user,constraints}
cp templates/research-seeds/technical/*.seed.md .specify/research-seeds/technical/
cp templates/research-seeds/domain/*.seed.md .specify/research-seeds/domain/
# ... etc
```

2. Fill out relevant seed files (text editor)

3. Run `/speckit.research`:
   - AI will read seed files
   - Ask clarifying questions for gaps
   - Generate comprehensive research docs

**Seed files are optional** - AI can guide you interactively without them.

---

## Implementation Research Mode (Legacy)

> **When to use:** During feature planning, for specific technology research
> **Output:** `.specify/specs/<feature-name>/research.md`
> **Context:** Feature-centric workflow (backward compatible)

### Purpose

Conduct targeted research for specific implementation questions:
- New/unfamiliar technologies
- Best practices for patterns
- Version-specific API changes
- Performance optimization techniques
- Security considerations

### Workflow

#### 1. Identify Research Topics

From spec or plan, identify areas needing research:
- Technology/library selection
- Implementation patterns
- Integration approaches
- Performance considerations

#### 2. Conduct Research

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

#### 3. Update Research Document

Append findings to `.specify/specs/<feature-name>/research.md`

#### 4. Cross-Reference with Plan

After research:
- Update plan.md with refined technical decisions
- Note any specification changes needed
- Flag potential risks discovered

---

## Research Quality Criteria

Good research should be:
- **Specific:** Answers concrete questions
- **Current:** Uses up-to-date sources (check version compatibility)
- **Actionable:** Provides clear recommendations with rationale
- **Validated:** Includes trade-off analysis
- **Referenced:** Cites sources for verification

---

## Common Research Categories

### Technical Research
- Framework capabilities/limitations
- Library comparison
- API design patterns
- Data structure optimization

### Domain Research
- Business domain concepts
- Industry standards
- Regulatory requirements
- Business rule formalization

### User Research
- User needs and pain points
- Persona characteristics
- User journey mapping
- Accessibility requirements

### Implementation Research
- Algorithm selection
- Caching strategies
- Authentication flows
- Data migration approaches

---

## Tips for Effective Research

1. **Start broad, then narrow:** Understand domain before diving into specifics
2. **Document assumptions:** Note what's assumed vs. validated
3. **Consider alternatives:** Compare at least 2-3 options with trade-offs
4. **Check versions:** Ensure compatibility with project tech stack
5. **Link to sources:** Provide references for verification
6. **Update iteratively:** Research can be refined as project evolves

---

## Research Outputs

**Project Mode:**
- `.specify/research/README.md` - Research index
- `.specify/research/technical/` - Technical research docs
- `.specify/research/domain/` - Domain research docs
- `.specify/research/user/` - User research docs
- `.specify/research/constraints/` - Constraints research docs

**Feature Mode:**
- `.specify/specs/<feature-name>/research.md` - Feature-specific research

---

## Next Commands

**After Project Research:**
- `/speckit.specify` - Create project-level PRD (uses research)
- `/speckit.plan` - Create implementation plan (references research)

**After Implementation Research:**
- `/speckit.plan` - Update implementation plan with findings
- `/speckit.implement` - Apply research recommendations in code
