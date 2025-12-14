---
description: Scan and analyze existing codebase structure, patterns, and conventions
---

# Codebase Scanner

Analyze an existing codebase to understand its structure, patterns, dependencies, and conventions before planning new work.

## When to Use

- Before adding features to an existing project
- When onboarding to an unfamiliar codebase
- Before major refactoring efforts
- To document project architecture for team members
- To identify technical debt and improvement opportunities

## Instructions

Execute a comprehensive codebase analysis following these steps:

### 1. Project Structure Analysis

First, understand the high-level directory organization:

```bash
# Get directory tree (excluding common noise)
find . -type d \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/target/*" \
  -not -path "*/.next/*" \
  -not -path "*/build/*" \
  -not -path "*/.venv/*" \
  -not -path "*/vendor/*" \
  | head -50

# Count files by extension
find . -type f \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

### 2. Detect Project Type

Identify the primary technology stack:

```bash
# Check for project manifests
ls -la package.json Cargo.toml go.mod pyproject.toml requirements.txt \
  pom.xml build.gradle *.csproj *.sln composer.json Gemfile 2>/dev/null
```

### 3. Dependency Analysis

Based on project type, analyze dependencies:

**Node.js:**
```bash
cat package.json | jq '{
  name: .name,
  version: .version,
  dependencies: .dependencies,
  devDependencies: .devDependencies,
  scripts: .scripts
}'
```

**Python:**
```bash
cat pyproject.toml 2>/dev/null || cat requirements.txt 2>/dev/null
```

**Rust:**
```bash
cat Cargo.toml | grep -A 50 '\[dependencies\]'
```

**Go:**
```bash
cat go.mod
```

### 4. Architecture Pattern Detection

Look for common architectural patterns:

```bash
# MVC indicators
ls -d */controllers */routes */views */models 2>/dev/null

# Clean Architecture indicators
ls -d */domain */entities */usecases */adapters */infrastructure 2>/dev/null

# Service layer indicators
ls -d */services */repositories */handlers 2>/dev/null

# Component-based (React/Vue/etc)
ls -d */components */pages */hooks */store 2>/dev/null
```

### 5. Testing Structure

Identify testing approach:

```bash
# Find test directories and files
find . -type d \( -name "test" -o -name "tests" -o -name "__tests__" -o -name "spec" \) \
  -not -path "*/node_modules/*" 2>/dev/null

# Count test files
find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*.py" \) \
  -not -path "*/node_modules/*" | wc -l
```

### 6. Configuration & Infrastructure

Check for DevOps and configuration:

```bash
# Docker
ls -la Dockerfile docker-compose.yml docker-compose.yaml 2>/dev/null

# CI/CD
ls -la .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile .circleci/config.yml 2>/dev/null

# Environment configuration
ls -la .env.example .env.template *.env.* 2>/dev/null
```

### 7. Code Quality Tools

Identify linting and formatting:

```bash
# Linters and formatters
ls -la .eslintrc* .prettierrc* .pylintrc pyproject.toml \
  rustfmt.toml .golangci.yml .editorconfig 2>/dev/null
```

## Output Format

Generate a report in `.specify/scans/codebase-analysis.md`:

```markdown
# Codebase Analysis Report

**Generated:** [timestamp]
**Directory:** [project path]

## Executive Summary

[2-3 sentences summarizing the codebase]

## Project Profile

| Attribute | Value |
|-----------|-------|
| **Type** | [Web app, CLI, Library, API, etc.] |
| **Primary Language** | [Language] |
| **Framework** | [Framework if applicable] |
| **Architecture** | [Monolith, Microservices, etc.] |
| **Package Manager** | [npm, pip, cargo, etc.] |

## Directory Structure

```
[Annotated tree showing key directories]
```

## Technology Stack

### Runtime & Framework
- [Runtime]: [Version]
- [Framework]: [Version]

### Key Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| [dep] | [ver] | [purpose] |

### Development Tools
- Testing: [framework]
- Linting: [tool]
- Formatting: [tool]

## Architectural Patterns

### Identified Patterns
- **[Pattern Name]**: [Where/how it's used]

### Component Organization
[Description of how code is organized]

## Code Quality Assessment

### Strengths
- [Strength 1]
- [Strength 2]

### Areas for Improvement
- [Area 1]
- [Area 2]

### Technical Debt Indicators
- [Indicator 1]
- [Indicator 2]

## Testing Coverage

| Type | Location | Framework |
|------|----------|-----------|
| Unit | [path] | [framework] |
| Integration | [path] | [framework] |
| E2E | [path] | [framework] |

## Infrastructure

### Containerization
[Docker setup description]

### CI/CD
[Pipeline description]

### Deployment
[Deployment approach if detectable]

## Recommendations

### Before Adding Features
1. [Recommendation 1]
2. [Recommendation 2]

### Potential Improvements
1. [Improvement 1]
2. [Improvement 2]

## Entry Points

Key files to understand first:
1. `[file]` - [why important]
2. `[file]` - [why important]
```

## Integration with Workflow

After running `/speckit.scan`:

1. Review the generated analysis
2. Use insights to inform `/speckit.constitution` (project principles)
3. Reference patterns when creating `/speckit.plan`
4. Ensure new code follows identified conventions

## Notes

- This scan is non-destructive (read-only analysis)
- Large codebases may require focused scans on specific directories
- Update the scan periodically as the codebase evolves
- Share scan reports with team members for alignment