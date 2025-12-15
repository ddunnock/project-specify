---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `/templates/implementation-plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `/templates/project-plan-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

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

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `/memory/constitution.md` file.
