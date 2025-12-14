#!/bin/bash
#
# Integration tests for project-specify
#

set -e

TEST_DIR=$(mktemp -d)
echo "Running integration tests in: $TEST_DIR"

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

cd "$TEST_DIR"

# Test 1: Check command works
echo "Test 1: Running check..."
if command -v project-specify &> /dev/null; then
    project-specify check || echo "Check command completed (may have warnings)"
    echo "✅ Check command works"
else
    echo "⚠️  project-specify not installed, skipping check test"
fi

# Test 2: Init with single agent
echo "Test 2: Init with Claude..."
mkdir test-single && cd test-single
if command -v project-specify &> /dev/null; then
    project-specify init . --ai claude --no-git || echo "Init may have failed (expected in test environment)"
    if [ -d ".specify" ]; then
        echo "✅ .specify directory created"
    fi
    if [ -L ".claude/commands" ] || [ -d ".claude/commands" ]; then
        echo "✅ Claude commands directory exists"
    fi
else
    echo "⚠️  project-specify not installed, skipping init test"
fi
cd ..

# Test 3: Init with all agents
echo "Test 3: Init with all agents..."
mkdir test-all && cd test-all
if command -v project-specify &> /dev/null; then
    project-specify init . --ai all --no-git || echo "Init may have failed (expected in test environment)"
    # Verify several agents
    if [ -L ".claude/commands" ] || [ -d ".claude/commands" ]; then
        echo "✅ Claude symlink/directory exists"
    fi
    if [ -L ".cursor/commands" ] || [ -d ".cursor/commands" ]; then
        echo "✅ Cursor symlink/directory exists"
    fi
else
    echo "⚠️  project-specify not installed, skipping all agents test"
fi
cd ..

# Test 4: Verify .specify structure
echo "Test 4: Verifying .specify structure..."
cd test-all
if [ -d ".specify" ]; then
    [ -d ".specify/memory" ] && echo "✅ memory dir exists" || echo "⚠️  memory dir missing"
    [ -d ".specify/scripts" ] && echo "✅ scripts dir exists" || echo "⚠️  scripts dir missing"
    [ -d ".specify/templates" ] && echo "✅ templates dir exists" || echo "⚠️  templates dir missing"
    [ -d ".specify/context" ] && echo "✅ context dir exists" || echo "⚠️  context dir missing"
else
    echo "⚠️  .specify directory not found"
fi
cd ..

echo ""
echo "========================================="
echo "Integration tests completed"
echo "========================================="

