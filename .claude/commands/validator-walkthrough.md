# Project-Specify Workflow Validation Prompt

> **Give this prompt to an AI agent (Claude Code, Cursor, etc.) along with the required files**

---

## Agent Instructions

You are tasked with performing a comprehensive validation of the **project-specify** codebase—a refactored fork of GitHub's spec-kit. This validation includes environment setup, CLI testing, workflow verification, and multi-agent API testing to ensure cross-agent compatibility.

**Your goal**: Execute each phase, document results, and generate a final validation report.

**Environment**: This validation is designed for **WSL (Windows Subsystem for Linux) Ubuntu**.

---

## WSL-Specific Notes

Before running, be aware of these WSL considerations:

| Issue | Solution |
|-------|----------|
| **mise/pyenv conflicts** | Always use `poetry run python ...` instead of just `python` |
| **Slow I/O on /mnt/c** | Keep projects on native WSL filesystem (`~/projects/`) |
| **Symlink failures** | Enable Windows Developer Mode, or work on native WSL filesystem |
| **Line endings** | Run `git config --global core.autocrlf input` |
| **SSL/Certificate errors** | Set `REQUESTS_CA_BUNDLE` and `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH` |

---

## Required Inputs (Provide These to the Agent)

Before starting, the human must provide:

```
PROJECT_SPECIFY_PATH: [absolute path to project-specify repository]
MULTI_AGENT_PATH: [absolute path to multi-agent-testing framework]
ANTHROPIC_API_KEY: [your Anthropic API key]
OPENAI_API_KEY: [your OpenAI API key]  
GOOGLE_API_KEY: [your Google Gemini API key]
GITHUB_TOKEN: [optional - GitHub token for Copilot]
```

**WSL Recommendation**: Use native Linux paths like `~/projects/project-specify`, NOT `/mnt/c/...`

---

## Execution Instructions

Execute each phase in order. For each phase:
1. Run the specified commands/scripts
2. Capture all output
3. Note any failures or warnings
4. Continue to next phase (don't stop on non-critical failures)

**Important**: In WSL with mise/pyenv, always prefix Python commands with `poetry run`:
```bash
# Instead of: python run_validation.py
# Use:        poetry run python run_validation.py
```

---

## PHASE 0: Prerequisites Validation

**Objective**: Verify the environment is ready for validation.

### 0.1 System Requirements

Execute this script and capture output:

```bash
#!/bin/bash
echo "=== PREREQUISITES CHECK (WSL) ==="

# Check if WSL
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "✓ Running in WSL"
else
    echo "○ Not in WSL (some checks may not apply)"
fi

# Python version
echo ""
echo -n "Python: "
python3 --version 2>/dev/null || echo "NOT FOUND"
python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null && echo "  ✓ Version OK (3.11+)" || echo "  ✗ Requires 3.11+"

# Poetry
echo ""
echo -n "Poetry: "
poetry --version 2>/dev/null || echo "NOT FOUND"

# Required tools
echo ""
echo "Required tools:"
for tool in bash git grep find readlink; do
    command -v $tool &>/dev/null && echo "  ✓ $tool" || echo "  ✗ $tool MISSING"
done

# Symlink capability
echo ""
echo -n "Symlinks: "
TEST_DIR=$(mktemp -d)
ln -s /tmp "$TEST_DIR/test" 2>/dev/null && echo "✓ Can create" || echo "✗ Cannot create (Windows: enable Developer Mode)"
rm -rf "$TEST_DIR"

# Write permissions
echo ""
echo "Permissions:"
touch /tmp/.test-$$ 2>/dev/null && echo "  ✓ /tmp writable" && rm /tmp/.test-$$
touch ~/.test-$$ 2>/dev/null && echo "  ✓ Home writable" && rm ~/.test-$$

# API Keys (check if set)
echo ""
echo "API Keys:"
[ -n "$ANTHROPIC_API_KEY" ] && echo "  ✓ ANTHROPIC_API_KEY" || echo "  ○ ANTHROPIC_API_KEY not set"
[ -n "$OPENAI_API_KEY" ] && echo "  ✓ OPENAI_API_KEY" || echo "  ○ OPENAI_API_KEY not set"
[ -n "$GOOGLE_API_KEY" ] && echo "  ✓ GOOGLE_API_KEY" || echo "  ○ GOOGLE_API_KEY not set"

echo ""
echo "=== PREREQUISITES CHECK COMPLETE ==="
```

### 0.2 Set Environment Variables

```bash
# Set these with actual values provided by the human
export PROJECT_SPECIFY_PATH="/path/to/project-specify"
export MULTI_AGENT_PATH="/path/to/multi-agent-testing"
export VALIDATION_OUTPUT="/tmp/ps-validation-$(date +%Y%m%d_%H%M%S)"
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="..."

mkdir -p "$VALIDATION_OUTPUT"
echo "Validation output: $VALIDATION_OUTPUT"
```

### 0.3 Install project-specify

```bash
cd "$PROJECT_SPECIFY_PATH"
pip install -e ".[dev]"
project-specify --version
project-specify check
```

**Record**: Note the version and check output.

---

## PHASE 1: Repository Structure Validation

**Objective**: Verify all required components exist.

### 1.1 Directory Structure

```bash
cd "$PROJECT_SPECIFY_PATH"

echo "=== REPOSITORY STRUCTURE ==="

# Check required directories
for dir in "src/specify_cli" "src/specify_cli/agents" "src/specify_cli/templates" "src/specify_cli/scripts"; do
    [ -d "$dir" ] && echo "✓ $dir" || echo "✗ $dir MISSING"
done

# Check required files
for file in "pyproject.toml" "src/specify_cli/__init__.py" "src/specify_cli/symlink_manager.py" "src/specify_cli/monorepo.py" "src/specify_cli/mcp_discovery.py"; do
    [ -f "$file" ] && echo "✓ $file" || echo "✗ $file MISSING"
done

# Count agents
echo ""
echo "Agents found: $(ls -1 src/specify_cli/agents/ | wc -l)"
ls -1 src/specify_cli/agents/
```

### 1.2 Python Imports

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, f"{__import__('os').environ['PROJECT_SPECIFY_PATH']}/src")

print("=== IMPORT VERIFICATION ===")

tests = [
    ("specify_cli", "Main package"),
    ("specify_cli.symlink_manager", "Symlink manager"),
    ("specify_cli.monorepo", "Monorepo detection"),
    ("specify_cli.mcp_discovery", "MCP discovery"),
]

for module, desc in tests:
    try:
        __import__(module)
        print(f"✓ {desc}")
    except Exception as e:
        print(f"✗ {desc}: {e}")

# Check key exports
from specify_cli.symlink_manager import SUPPORTED_AGENTS
print(f"\nSupported agents: {len(SUPPORTED_AGENTS)}")
```

### 1.3 Agent Command Completeness

```bash
cd "$PROJECT_SPECIFY_PATH"

echo "=== AGENT COMMAND CHECK ==="

REQUIRED="speckit.constitution.md speckit.specify.md speckit.plan.md speckit.tasks.md speckit.implement.md"

for agent_dir in src/specify_cli/agents/*/; do
    agent=$(basename "$agent_dir")
    commands_dir="$agent_dir/commands"
    
    if [ ! -d "$commands_dir" ]; then
        echo "✗ $agent: No commands directory"
        continue
    fi
    
    missing=""
    for cmd in $REQUIRED; do
        [ ! -f "$commands_dir/$cmd" ] && missing="$missing $cmd"
    done
    
    [ -z "$missing" ] && echo "✓ $agent: All required commands" || echo "⚠ $agent: Missing$missing"
done
```

**Record**: List any missing agents or commands.

---

## PHASE 2: CLI Functionality Testing

**Objective**: Verify all CLI commands work correctly.

### 2.1 Basic Commands

```bash
mkdir -p "$VALIDATION_OUTPUT/phase2"
cd "$VALIDATION_OUTPUT/phase2"

echo "=== CLI BASIC COMMANDS ==="

# Version
echo "Testing: --version"
project-specify --version && echo "✓ Version command works"

# Help
echo ""
echo "Testing: --help"
project-specify --help > /dev/null && echo "✓ Help command works"

# Check
echo ""
echo "Testing: check"
project-specify check && echo "✓ Check command works"
```

### 2.2 Init Command Variations

```bash
cd "$VALIDATION_OUTPUT/phase2"

echo "=== INIT COMMAND TESTS ==="

# Test 1: Single agent
echo ""
echo "Test: Single agent (--ai claude)"
mkdir -p test1 && cd test1
project-specify init . --ai claude --force --no-git --no-mcp-discovery
[ -d ".claude" ] && [ -d ".specify" ] && echo "✓ Passed" || echo "✗ Failed"
cd ..

# Test 2: Multiple agents (separate flags)
echo ""
echo "Test: Multiple agents (--ai claude --ai cursor)"
mkdir -p test2 && cd test2
project-specify init . --ai claude --ai cursor --force --no-git --no-mcp-discovery
[ -d ".claude" ] && [ -d ".cursor" ] && echo "✓ Passed" || echo "✗ Failed"
cd ..

# Test 3: Comma-separated
echo ""
echo "Test: Comma-separated (--ai claude,cursor,copilot)"
mkdir -p test3 && cd test3
project-specify init . --ai claude,cursor,copilot --force --no-git --no-mcp-discovery
[ -d ".claude" ] && [ -d ".cursor" ] && echo "✓ Passed" || echo "✗ Failed"
cd ..

# Test 4: All agents
echo ""
echo "Test: All agents (--ai all)"
mkdir -p test4 && cd test4
project-specify init . --ai all --force --no-git --no-mcp-discovery
AGENT_COUNT=$(find . -maxdepth 1 -type d -name ".*" ! -name ".specify" | wc -l)
echo "Agent directories created: $AGENT_COUNT"
[ $AGENT_COUNT -ge 10 ] && echo "✓ Passed" || echo "⚠ Fewer agents than expected"
cd ..

# Test 5: --here flag
echo ""
echo "Test: --here flag"
mkdir -p test5 && cd test5
project-specify init --here --ai claude --force --no-git --no-mcp-discovery
[ -d ".specify" ] && echo "✓ Passed" || echo "✗ Failed"
cd ..
```

### 2.3 Symlink Verification

```bash
cd "$VALIDATION_OUTPUT/phase2/test4"

echo "=== SYMLINK VERIFICATION ==="

for agent_dir in .claude .cursor .github .gemini .windsurf; do
    [ ! -d "$agent_dir" ] && continue
    
    if [ -L "$agent_dir/commands" ]; then
        target=$(readlink "$agent_dir/commands")
        [ -e "$agent_dir/commands" ] && echo "✓ $agent_dir/commands → $target" || echo "✗ $agent_dir/commands BROKEN"
    elif [ -d "$agent_dir/commands" ]; then
        echo "○ $agent_dir/commands (directory, not symlink)"
    fi
done

echo ""
echo "Central installation:"
[ -d ~/.project-specify/agents ] && echo "✓ ~/.project-specify/agents exists" || echo "✗ Central install missing"
```

### 2.4 MCP Discovery

```bash
cd "$VALIDATION_OUTPUT/phase2/test1"

echo "=== MCP DISCOVERY ==="

project-specify discover

[ -f ".specify/context/project-context.json" ] && echo "✓ project-context.json created" || echo "○ project-context.json not created"
[ -f ".specify/context/mcp-servers.md" ] && echo "✓ mcp-servers.md created" || echo "○ mcp-servers.md not created"

# Show detected technology if available
[ -f ".specify/context/project-context.json" ] && cat .specify/context/project-context.json
```

**Record**: Note any command failures.

---

## PHASE 3: Workflow Sequence Validation

**Objective**: Verify command templates and dependencies.

### 3.1 Command Chain Verification

```bash
cd "$PROJECT_SPECIFY_PATH"

echo "=== WORKFLOW COMMAND CHAIN ==="
echo ""
echo "Expected flow: constitution → specify → plan → tasks → implement"
echo ""

COMMANDS_DIR="src/specify_cli/agents/claude/commands"

for cmd in constitution specify plan tasks implement; do
    FILE="$COMMANDS_DIR/speckit.$cmd.md"
    echo "[$cmd]"
    
    if [ -f "$FILE" ]; then
        echo "  ✓ File exists"
        
        # Check for script references
        grep -q "scripts/" "$FILE" && echo "  ✓ References scripts"
        
        # Check for template references
        grep -q "templates/" "$FILE" && echo "  ✓ References templates"
        
        # Check for MCP awareness
        grep -qi "mcp\|project-context" "$FILE" && echo "  ✓ MCP-aware"
    else
        echo "  ✗ File missing"
    fi
    echo ""
done
```

### 3.2 Template Validation

```bash
cd "$PROJECT_SPECIFY_PATH/src/specify_cli/templates"

echo "=== TEMPLATE VALIDATION ==="

for template in *.md; do
    echo "[$template]"
    WORDS=$(wc -w < "$template")
    HEADERS=$(grep -c "^#" "$template")
    echo "  Words: $WORDS, Headers: $HEADERS"
    [ $WORDS -gt 50 ] && [ $HEADERS -gt 2 ] && echo "  ✓ Valid structure" || echo "  ⚠ May need review"
done
```

**Record**: Note any missing dependencies.

---

## PHASE 4: Multi-Agent API Testing

**Objective**: Test workflow outputs across multiple AI providers.

> **Skip this phase** if API keys are not configured. Note in report: "Phase 4 skipped - API keys not configured"

### 4.1 Setup Multi-Agent Framework

```bash
cd "$MULTI_AGENT_PATH"

echo "=== MULTI-AGENT FRAMEWORK SETUP ==="

# Verify Poetry is installed
poetry --version

# Install dependencies with Poetry
poetry install

# Configure API keys
cat > config/api_keys.env << EOF
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
OPENAI_API_KEY=$OPENAI_API_KEY
GOOGLE_API_KEY=$GOOGLE_API_KEY
GITHUB_TOKEN=$GITHUB_TOKEN
EOF

# Verify configuration
poetry run python run_validation.py check-config
poetry run python run_validation.py list-agents
```

### 4.2 Test API Connections

```bash
cd "$MULTI_AGENT_PATH"

echo "=== API CONNECTION TEST ==="

poetry run python run_validation.py test-connections
```

**Record**: Which agents connected successfully.

### 4.3 Run Minimal Test (Quick Validation)

```bash
cd "$MULTI_AGENT_PATH"

echo "=== MINIMAL TEST SCENARIO ==="

poetry run python run_validation.py run -s minimal-test -o "$VALIDATION_OUTPUT/phase4-minimal"

# Check results
RESULT_DIR=$(ls -td "$VALIDATION_OUTPUT/phase4-minimal"/*/ 2>/dev/null | head -1)
[ -f "$RESULT_DIR/validation_report.md" ] && cat "$RESULT_DIR/validation_report.md"
```

### 4.4 Run Full Cross-Agent Test

```bash
cd "$MULTI_AGENT_PATH"

echo "=== FULL CROSS-AGENT TEST ==="
echo ""
echo "This test runs:"
echo "  1. Anthropic (Claude) → Creates constitution"
echo "  2. OpenAI (GPT-4) → Creates specification from constitution"
echo "  3. Google (Gemini) → Creates plan from specification"
echo "  4. Anthropic (Claude) → Creates tasks from plan"
echo ""

poetry run python run_validation.py run -s user-auth-feature -o "$VALIDATION_OUTPUT/phase4-full"

# Display results
RESULT_DIR=$(ls -td "$VALIDATION_OUTPUT/phase4-full"/*/ 2>/dev/null | head -1)

if [ -d "$RESULT_DIR" ]; then
    echo ""
    echo "=== GENERATED FILES ==="
    find "$RESULT_DIR/.specify" -name "*.md" -exec echo "✓ {}" \;
    
    echo ""
    echo "=== VALIDATION REPORT ==="
    cat "$RESULT_DIR/validation_report.md"
fi
```

### 4.5 Cross-Agent Compatibility Test

```bash
cd "$MULTI_AGENT_PATH"

echo "=== CROSS-AGENT COMPATIBILITY TEST ==="

poetry run python run_validation.py run -s cross-agent-compat -o "$VALIDATION_OUTPUT/phase4-compat"

RESULT_DIR=$(ls -td "$VALIDATION_OUTPUT/phase4-compat"/*/ 2>/dev/null | head -1)
[ -f "$RESULT_DIR/validation_report.md" ] && cat "$RESULT_DIR/validation_report.md"
```

**Record**:
- Which agents succeeded
- Token usage
- Quality scores
- Any failures

---

## PHASE 5: Error Handling Validation

**Objective**: Verify graceful error handling.

```bash
mkdir -p "$VALIDATION_OUTPUT/phase5"
cd "$VALIDATION_OUTPUT/phase5"

echo "=== ERROR HANDLING TESTS ==="

# Test 1: Invalid agent name
echo ""
echo "Test: Invalid agent name"
if project-specify init t1 --ai invalid-agent-xyz 2>&1 | grep -qiE "invalid|error|unknown|not found"; then
    echo "✓ Correctly rejected invalid agent"
else
    echo "✗ Should have rejected invalid agent"
fi

# Test 2: Conflicting arguments
echo ""
echo "Test: Conflicting arguments"
if project-specify init my-project --here 2>&1 | grep -qiE "error|conflict|cannot"; then
    echo "✓ Correctly rejected conflicting arguments"
else
    echo "⚠ May have allowed conflicting arguments"
fi

# Test 3: Broken symlink recovery
echo ""
echo "Test: Broken symlink detection"
mkdir -p t3 && cd t3
project-specify init . --ai claude --force --no-git --no-mcp-discovery 2>/dev/null
# Simulate broken symlink by removing target
rm -rf ~/.project-specify/agents/claude/commands 2>/dev/null
project-specify status 2>&1 | grep -qi "broken\|invalid\|missing" && echo "✓ Detects broken symlinks" || echo "○ May not report broken symlinks"
cd ..

# Restore central install
cd "$PROJECT_SPECIFY_PATH"
pip install -e ".[dev]" -q
```

**Record**: Error handling test results.

---

## PHASE 6: Output Quality Validation

**Objective**: Score the quality of generated outputs.

```python
#!/usr/bin/env python3
import os
import re
from pathlib import Path

VALIDATION_OUTPUT = os.environ.get("VALIDATION_OUTPUT", "/tmp/ps-validation")

print("=== OUTPUT QUALITY SCORING ===\n")

# Find multi-agent results
result_dirs = sorted(Path(f"{VALIDATION_OUTPUT}/phase4-full").glob("*/"), reverse=True) if Path(f"{VALIDATION_OUTPUT}/phase4-full").exists() else []

if not result_dirs:
    print("⚠ No multi-agent results found. Run Phase 4 first.")
    exit(0)

result_dir = result_dirs[0]
print(f"Analyzing: {result_dir}\n")

def score_document(path, checks):
    """Score a document based on checks."""
    if not path.exists():
        return None, "File not found"
    
    content = path.read_text()
    scores = {}
    
    for name, (pattern, weight) in checks.items():
        if callable(pattern):
            scores[name] = pattern(content) * weight
        else:
            matches = len(re.findall(pattern, content, re.IGNORECASE))
            scores[name] = min(1.0, matches / 3) * weight
    
    return sum(scores.values()) / sum(c[1] for c in checks.values()), scores

# Define scoring criteria
doc_checks = {
    "constitution": {
        "principles": (r"principle|guideline", 1.0),
        "standards": (r"standard|requirement", 1.0),
        "length": (lambda c: min(1.0, len(c.split()) / 200), 1.0),
    },
    "spec": {
        "user_stories": (r"[Aa]s a.*[Ii] want", 1.5),
        "acceptance": (r"acceptance|given.*when.*then", 1.0),
        "length": (lambda c: min(1.0, len(c.split()) / 300), 0.5),
    },
    "plan": {
        "architecture": (r"architect|design|structure", 1.0),
        "technology": (r"technolog|framework|library", 1.0),
        "phases": (r"phase|milestone|stage", 1.0),
    },
    "tasks": {
        "task_ids": (r"\[T\d+\]", 1.5),
        "file_refs": (r"src/|tests/|\.py|\.ts", 1.0),
        "dependencies": (r"depend|require|after|block", 0.5),
    },
}

# Score each document
files = {
    "constitution": result_dir / ".specify/memory/constitution.md",
    "spec": result_dir / ".specify/specs/user-auth/spec.md",
    "plan": result_dir / ".specify/specs/user-auth/plan.md",
    "tasks": result_dir / ".specify/specs/user-auth/tasks.md",
}

total_score = 0
scored_docs = 0

for doc_type, path in files.items():
    score, details = score_document(path, doc_checks.get(doc_type, {}))
    
    if score is None:
        print(f"[{doc_type.upper()}] ✗ {details}")
    else:
        status = "✓" if score >= 0.7 else "⚠" if score >= 0.4 else "✗"
        print(f"[{doc_type.upper()}] {status} Score: {score:.0%}")
        if isinstance(details, dict):
            for k, v in details.items():
                print(f"  - {k}: {v:.2f}")
        total_score += score
        scored_docs += 1

if scored_docs > 0:
    final = total_score / scored_docs
    print(f"\n{'='*50}")
    print(f"OVERALL QUALITY: {final:.0%}")
    print(f"STATUS: {'✓ PASS' if final >= 0.6 else '✗ FAIL'}")
```

**Record**: Quality scores for each document type.

---

## PHASE 7: Integration Test Suite

**Objective**: Run comprehensive integration tests.

```bash
mkdir -p "$VALIDATION_OUTPUT/phase7"
cd "$VALIDATION_OUTPUT/phase7"

echo "=== INTEGRATION TEST SUITE ==="
echo ""

PASSED=0
FAILED=0

test() {
    echo -n "  $1... "
    if eval "$2" >/dev/null 2>&1; then
        echo "✓"
        ((PASSED++))
    else
        echo "✗"
        ((FAILED++))
    fi
}

test "Init with single agent" "mkdir -p t1 && cd t1 && project-specify init . --ai claude --force --no-git --no-mcp-discovery && [ -d .claude ]"
test "Init with multiple agents" "mkdir -p t2 && cd t2 && project-specify init . --ai claude --ai cursor --force --no-git --no-mcp-discovery && [ -d .claude ] && [ -d .cursor ]"
test "Init with all agents" "mkdir -p t3 && cd t3 && project-specify init . --ai all --force --no-git --no-mcp-discovery && [ -d .claude ]"
test "Symlinks are valid" "cd t1 && [ -L .claude/commands ] && [ -e .claude/commands ]"
test ".specify structure" "cd t1 && [ -d .specify/memory ] && [ -d .specify/specs ]"
test "Status command" "cd t1 && project-specify status"
test "Check command" "project-specify check"
test "Discover command" "cd t1 && project-specify discover"
test "Monorepo detection" "mkdir -p t-mono && cd t-mono && echo 'packages: [\"*\"]' > pnpm-workspace.yaml && project-specify init . --ai claude --force --no-git --no-mcp-discovery 2>&1 | grep -qi monorepo"
test "Invalid agent rejection" "! project-specify init t-invalid --ai fake-agent 2>&1 | grep -qi success"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: $PASSED passed, $FAILED failed"
echo "Status: $([ $FAILED -eq 0 ] && echo '✓ ALL TESTS PASSED' || echo '✗ SOME TESTS FAILED')"
```

**Record**: Pass/fail count.

---

## PHASE 8: Generate Final Report

**Objective**: Compile all results into a final report.

```bash
REPORT="$VALIDATION_OUTPUT/FINAL_VALIDATION_REPORT.md"

cat > "$REPORT" << 'EOF'
# Project-Specify Validation Report

## Summary

| Phase | Description | Status |
|-------|-------------|--------|
EOF

# Add phase results (agent should fill these based on actual results)
echo "| 0 | Prerequisites | [RESULT] |" >> "$REPORT"
echo "| 1 | Repository Structure | [RESULT] |" >> "$REPORT"
echo "| 2 | CLI Functionality | [RESULT] |" >> "$REPORT"
echo "| 3 | Workflow Sequence | [RESULT] |" >> "$REPORT"
echo "| 4 | Multi-Agent Testing | [RESULT] |" >> "$REPORT"
echo "| 5 | Error Handling | [RESULT] |" >> "$REPORT"
echo "| 6 | Output Quality | [RESULT] |" >> "$REPORT"
echo "| 7 | Integration Tests | [RESULT] |" >> "$REPORT"

cat >> "$REPORT" << 'EOF'

## Multi-Agent Test Results

### Agents Used
- Anthropic (Claude): [STATUS]
- OpenAI (GPT-4): [STATUS]
- Google (Gemini): [STATUS]
- GitHub Copilot: [STATUS]

### Cross-Agent Workflow
- Constitution generated: [YES/NO]
- Specification from constitution: [YES/NO]
- Plan from specification: [YES/NO]
- Tasks from plan: [YES/NO]

### Quality Scores
- Constitution: [SCORE]%
- Specification: [SCORE]%
- Plan: [SCORE]%
- Tasks: [SCORE]%
- **Overall**: [SCORE]%

## Issues Found

[List any issues discovered during validation]

## Recommendations

[List any recommendations for improvement]

## Conclusion

**Validation Status**: [PASS/FAIL]

**Production Readiness**: [YES/NO/CONDITIONAL]

---
*Generated: [DATE]*
*Validation Output: [PATH]*
EOF

echo "Report template created: $REPORT"
echo ""
echo "=== AGENT: Please update the report with actual results ==="
```

---

## Agent Checklist

Before completing, verify:

- [ ] Phase 0: Prerequisites passed (Python 3.11+, tools available)
- [ ] Phase 1: All imports succeed, 15+ agents found
- [ ] Phase 2: All CLI commands execute without error
- [ ] Phase 3: Command templates reference valid dependencies
- [ ] Phase 4: Multi-agent tests completed (or noted as skipped)
- [ ] Phase 5: Error cases handled gracefully
- [ ] Phase 6: Output quality ≥ 60%
- [ ] Phase 7: Integration tests pass ≥ 80%
- [ ] Phase 8: Final report generated and filled in

## Success Criteria

| Criteria | Minimum | Target |
|----------|---------|--------|
| CLI Commands Working | 100% | 100% |
| Agent Command Coverage | 90% | 100% |
| Integration Tests | 80% | 100% |
| Multi-Agent Quality | 60% | 80% |
| Error Handling | Pass | Pass |

**Overall Pass**: All minimum criteria met.

---

## Troubleshooting Reference (WSL)

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'typer'` | Use `poetry run python ...` instead of `python ...` (mise conflict) |
| `project-specify: command not found` | Use `poetry run project-specify` or `cd $PROJECT_SPECIFY_PATH && poetry install` |
| `Cannot create symlinks` | Enable Windows Developer Mode, or move project to native WSL filesystem (`~/`) |
| `SSL CERTIFICATE_VERIFY_FAILED` | Set `REQUESTS_CA_BUNDLE` and `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH` to your cert bundle |
| `No agents configured` | Check API keys in `config/api_keys.env` |
| `Rate limit exceeded` | Wait 1-2 min, retry |
| `gemini-1.5-pro not found` | Update `config/agents.yaml` to use `gemini-2.0-flash` |
| Phase 4 skipped | Set API keys, run setup |
| Import errors | Check `PROJECT_SPECIFY_PATH` is correct |
| Slow performance | Move project from `/mnt/c/` to `~/projects/` |
| Git line ending issues | Run `git config --global core.autocrlf input` |

### WSL Certificate Setup

If behind corporate proxy:
```bash
# Create combined cert bundle
cat /etc/ssl/certs/ca-certificates.crt ~/your-certs/*.crt > ~/certs/combined-bundle.crt

# Add to ~/.zshrc or ~/.bashrc
export CORP_CA_BUNDLE="$HOME/certs/combined-bundle.crt"
export REQUESTS_CA_BUNDLE="$CORP_CA_BUNDLE"
export SSL_CERT_FILE="$CORP_CA_BUNDLE"
export GRPC_DEFAULT_SSL_ROOTS_FILE_PATH="$CORP_CA_BUNDLE"
```

---

## Final Instructions

1. Execute all phases in order
2. **Always use `poetry run`** for Python commands in WSL
3. Record results as you go
4. Fill in the final report template
5. Present the completed report to the human
6. Highlight any critical issues found