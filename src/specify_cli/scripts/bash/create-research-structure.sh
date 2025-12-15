#!/bin/bash
# Create .specify/research directory structure for project mode
#
# Creates:
#   .specify/research/technical/
#   .specify/research/domain/
#   .specify/research/user/
#   .specify/research/constraints/
#
# Usage:
#   ./create-research-structure.sh [project_dir]
#
# Exit Codes:
#   0 - Success
#   1 - Error

# Get project directory (default to current directory)
PROJECT_DIR="${1:-.}"
RESEARCH_DIR="$PROJECT_DIR/.specify/research"

echo "Creating research directory structure..."

# Create category directories
for category in technical domain user constraints; do
    CATEGORY_DIR="$RESEARCH_DIR/$category"

    if mkdir -p "$CATEGORY_DIR"; then
        echo "✓ Created $CATEGORY_DIR"
    else
        echo "✗ Failed to create $CATEGORY_DIR"
        exit 1
    fi
done

echo ""
echo "Research directory structure created successfully!"
echo ""
echo "Directory structure:"
echo "  .specify/research/"
echo "  ├── technical/"
echo "  ├── domain/"
echo "  ├── user/"
echo "  └── constraints/"
echo ""
echo "Next steps:"
echo "  1. (Optional) Copy seed templates from templates/research-seeds/ to .specify/research-seeds/"
echo "  2. Run /speckit.research to generate research documents"

exit 0
