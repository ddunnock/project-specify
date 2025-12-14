---
description: Research technologies, patterns, and best practices for implementation
---

# Research Assistant

Conduct targeted research to inform implementation decisions.

## Instructions

When research is requested:

### 1. Identify Research Topics

From the specification or plan, identify areas needing research:
- New/unfamiliar technologies
- Best practices for specific patterns
- Version-specific API changes
- Performance optimization techniques
- Security considerations

### 2. Conduct Research

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

### 3. Update Research Document

Append findings to `.specify/specs/<project-name>/research.md` or `.specify/specs/<milestone>/research.md`

### 4. Cross-Reference with Plan

After research:
- Update plan.md with refined technical decisions
- Note any specification changes needed
- Flag potential risks discovered

## Research Types

### Technology Research
- Framework capabilities and limitations
- Library comparison and selection
- API design patterns

### Implementation Research
- Algorithm selection
- Data structure optimization
- Caching strategies

### Integration Research
- Third-party API integration
- Authentication flows
- Data migration approaches

## Quality Criteria

Good research should be:
- **Specific:** Answers concrete questions
- **Current:** Uses up-to-date sources
- **Actionable:** Provides clear recommendations
- **Verified:** Code examples are tested

