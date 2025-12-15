#!/bin/bash
# Detect if project is in Project Mode or Feature Mode
#
# Returns:
#   "project" - Project mode (PRD-style with research)
#   "feature" - Feature mode (user story-driven features)
#   "unknown" - No .specify structure detected
#
# Exit Codes:
#   0 - Project Mode
#   1 - Feature Mode
#   2 - Unknown Mode

# Get project directory (default to current directory)
PROJECT_DIR="${1:-.}"
SPECIFY_DIR="$PROJECT_DIR/.specify"

# Check if .specify exists
if [ ! -d "$SPECIFY_DIR" ]; then
    echo "unknown"
    exit 2
fi

# Check for project mode indicators
RESEARCH_DIR="$SPECIFY_DIR/research"
RESEARCH_README="$RESEARCH_DIR/README.md"
PROJECT_SPEC="$SPECIFY_DIR/spec.md"

# If research directory, README, or project spec exists → Project Mode
if [ -d "$RESEARCH_DIR" ] || [ -f "$RESEARCH_README" ] || [ -f "$PROJECT_SPEC" ]; then
    echo "project"
    exit 0
fi

# Check for feature mode indicators
SPECS_DIR="$SPECIFY_DIR/specs"

if [ -d "$SPECS_DIR" ]; then
    # Check if there are any numbered feature directories (###-*)
    if ls "$SPECS_DIR"/[0-9]*-*/ >/dev/null 2>&1; then
        echo "feature"
        exit 1
    fi
fi

# No clear indicators found
echo "unknown"
exit 2
