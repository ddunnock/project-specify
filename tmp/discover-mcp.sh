#!/bin/bash
#
# MCP Server Discovery Script for project-specify
# 
# Discovers available MCP servers and project technology, then writes
# context files that AI agent commands can reference.
#
# Usage:
#   ./discover-mcp.sh [project_dir]
#
# Output:
#   .specify/context/mcp-servers.md
#   .specify/context/project-context.json
#

set -e

PROJECT_DIR="${1:-.}"
CONTEXT_DIR="$PROJECT_DIR/.specify/context"

mkdir -p "$CONTEXT_DIR"

echo "🔍 Discovering MCP servers and project context..."

# ============================================================================
# MCP Server Discovery
# ============================================================================

discover_mcp_configs() {
    local configs=()
    
    # Claude Desktop config locations
    case "$(uname)" in
        Darwin)
            configs+=("$HOME/Library/Application Support/Claude/claude_desktop_config.json")
            ;;
        Linux)
            configs+=("$HOME/.config/Claude/claude_desktop_config.json")
            ;;
        MINGW*|MSYS*|CYGWIN*)
            configs+=("$APPDATA/Claude/claude_desktop_config.json")
            ;;
    esac
    
    # Claude Code config
    configs+=("$HOME/.claude/mcp_servers.json")
    
    # Cursor config
    configs+=("$HOME/.cursor/mcp.json")
    
    # Project-local configs
    configs+=("$PROJECT_DIR/.mcp/servers.json")
    configs+=("$PROJECT_DIR/mcp.json")
    configs+=("$PROJECT_DIR/.mcp.json")
    
    for config in "${configs[@]}"; do
        if [ -f "$config" ]; then
            echo "$config"
        fi
    done
}

extract_mcp_servers() {
    local config_file="$1"
    local source="$2"
    
    if [ -f "$config_file" ]; then
        # Extract server names from mcpServers or servers key
        jq -r '
            (.mcpServers // .servers // .) 
            | to_entries[] 
            | "\(.key)|\((.value.command // "unknown"))|\((.value.args // []) | join(" "))"
        ' "$config_file" 2>/dev/null || true
    fi
}

# ============================================================================
# Technology Detection
# ============================================================================

detect_language() {
    if [ -f "$PROJECT_DIR/package.json" ]; then
        if [ -f "$PROJECT_DIR/tsconfig.json" ]; then
            echo "typescript"
        else
            echo "nodejs"
        fi
    elif [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        echo "rust"
    elif [ -f "$PROJECT_DIR/go.mod" ]; then
        echo "go"
    elif [ -f "$PROJECT_DIR/pyproject.toml" ] || [ -f "$PROJECT_DIR/requirements.txt" ]; then
        echo "python"
    elif [ -f "$PROJECT_DIR/pom.xml" ]; then
        echo "java"
    elif [ -f "$PROJECT_DIR/build.gradle" ] || [ -f "$PROJECT_DIR/build.gradle.kts" ]; then
        echo "java"
    else
        echo "unknown"
    fi
}

detect_framework() {
    local lang="$1"
    
    case "$lang" in
        typescript|nodejs)
            if [ -f "$PROJECT_DIR/package.json" ]; then
                local deps=$(cat "$PROJECT_DIR/package.json" | jq -r '(.dependencies // {}) + (.devDependencies // {}) | keys[]' 2>/dev/null)
                
                echo "$deps" | grep -q "^next$" && echo "Next.js" && return
                echo "$deps" | grep -q "^nuxt$" && echo "Nuxt" && return
                echo "$deps" | grep -q "^@remix-run" && echo "Remix" && return
                echo "$deps" | grep -q "^astro$" && echo "Astro" && return
                echo "$deps" | grep -q "^express$" && echo "Express" && return
                echo "$deps" | grep -q "^fastify$" && echo "Fastify" && return
                echo "$deps" | grep -q "^hono$" && echo "Hono" && return
                echo "$deps" | grep -q "^@nestjs" && echo "NestJS" && return
                echo "$deps" | grep -q "^react$" && echo "React" && return
                echo "$deps" | grep -q "^vue$" && echo "Vue" && return
            fi
            ;;
        python)
            local content=""
            [ -f "$PROJECT_DIR/pyproject.toml" ] && content+=$(cat "$PROJECT_DIR/pyproject.toml")
            [ -f "$PROJECT_DIR/requirements.txt" ] && content+=$(cat "$PROJECT_DIR/requirements.txt")
            
            echo "$content" | grep -qi "fastapi" && echo "FastAPI" && return
            echo "$content" | grep -qi "django" && echo "Django" && return
            echo "$content" | grep -qi "flask" && echo "Flask" && return
            ;;
        rust)
            if [ -f "$PROJECT_DIR/Cargo.toml" ]; then
                local content=$(cat "$PROJECT_DIR/Cargo.toml")
                echo "$content" | grep -q "axum" && echo "Axum" && return
                echo "$content" | grep -q "actix-web" && echo "Actix Web" && return
                echo "$content" | grep -q "tauri" && echo "Tauri" && return
            fi
            ;;
    esac
    
    echo ""
}

detect_package_manager() {
    local lang="$1"
    
    case "$lang" in
        typescript|nodejs)
            [ -f "$PROJECT_DIR/pnpm-lock.yaml" ] && echo "pnpm" && return
            [ -f "$PROJECT_DIR/yarn.lock" ] && echo "yarn" && return
            [ -f "$PROJECT_DIR/bun.lockb" ] && echo "bun" && return
            echo "npm"
            ;;
        python)
            [ -f "$PROJECT_DIR/poetry.lock" ] && echo "poetry" && return
            [ -f "$PROJECT_DIR/uv.lock" ] && echo "uv" && return
            [ -f "$PROJECT_DIR/Pipfile.lock" ] && echo "pipenv" && return
            echo "pip"
            ;;
        rust)
            echo "cargo"
            ;;
        go)
            echo "go"
            ;;
        java)
            [ -f "$PROJECT_DIR/pom.xml" ] && echo "maven" && return
            echo "gradle"
            ;;
        *)
            echo ""
            ;;
    esac
}

detect_database() {
    local content=""
    
    # Collect content from various files
    for f in package.json requirements.txt pyproject.toml Cargo.toml docker-compose.yml docker-compose.yaml .env.example; do
        [ -f "$PROJECT_DIR/$f" ] && content+=$(cat "$PROJECT_DIR/$f" 2>/dev/null)
    done
    
    content=$(echo "$content" | tr '[:upper:]' '[:lower:]')
    
    echo "$content" | grep -qE "postgres|postgresql|psycopg|asyncpg" && echo "postgres" && return
    echo "$content" | grep -qE "mysql|pymysql" && echo "mysql" && return
    echo "$content" | grep -qE "sqlite|better-sqlite" && echo "sqlite" && return
    echo "$content" | grep -qE "mongodb|mongoose|pymongo" && echo "mongodb" && return
    echo "$content" | grep -qE "supabase" && echo "supabase" && return
    echo "$content" | grep -qE "prisma" && echo "prisma" && return
    
    echo ""
}

detect_monorepo() {
    [ -f "$PROJECT_DIR/pnpm-workspace.yaml" ] && echo "pnpm" && return
    [ -f "$PROJECT_DIR/lerna.json" ] && echo "lerna" && return
    [ -f "$PROJECT_DIR/nx.json" ] && echo "nx" && return
    [ -f "$PROJECT_DIR/turbo.json" ] && echo "turborepo" && return
    
    if [ -f "$PROJECT_DIR/package.json" ]; then
        cat "$PROJECT_DIR/package.json" | jq -e '.workspaces' >/dev/null 2>&1 && echo "npm-workspaces" && return
    fi
    
    if [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        grep -q '\[workspace\]' "$PROJECT_DIR/Cargo.toml" && echo "cargo" && return
    fi
    
    echo ""
}

detect_services() {
    local services=()
    
    [ -f "$PROJECT_DIR/Dockerfile" ] && services+=("docker")
    [ -f "$PROJECT_DIR/docker-compose.yml" ] || [ -f "$PROJECT_DIR/docker-compose.yaml" ] && services+=("docker-compose")
    [ -d "$PROJECT_DIR/.github/workflows" ] && services+=("github-actions")
    [ -f "$PROJECT_DIR/.gitlab-ci.yml" ] && services+=("gitlab-ci")
    [ -f "$PROJECT_DIR/vercel.json" ] && services+=("vercel")
    [ -f "$PROJECT_DIR/netlify.toml" ] && services+=("netlify")
    [ -f "$PROJECT_DIR/fly.toml" ] && services+=("fly.io")
    [ -d "$PROJECT_DIR/kubernetes" ] && services+=("kubernetes")
    
    echo "${services[*]}"
}

# ============================================================================
# Generate Output
# ============================================================================

# Discover MCP servers
echo "  Checking MCP configurations..."
MCP_SERVERS=()
declare -A MCP_SOURCES

for config in $(discover_mcp_configs); do
    source=$(basename "$(dirname "$config")")
    servers=$(extract_mcp_servers "$config" "$source")
    
    while IFS='|' read -r name command args; do
        if [ -n "$name" ]; then
            MCP_SERVERS+=("$name")
            MCP_SOURCES["$name"]="$source"
        fi
    done <<< "$servers"
done

# Check for npx availability (means npm MCP servers can be used)
if command -v npx &> /dev/null; then
    echo "  npx available - npm MCP servers can be installed"
    NPX_AVAILABLE=true
else
    NPX_AVAILABLE=false
fi

# Detect project technology
echo "  Detecting project technology..."
LANGUAGE=$(detect_language)
FRAMEWORK=$(detect_framework "$LANGUAGE")
PACKAGE_MANAGER=$(detect_package_manager "$LANGUAGE")
DATABASE=$(detect_database)
MONOREPO=$(detect_monorepo)
SERVICES=$(detect_services)

echo "  Language: $LANGUAGE"
[ -n "$FRAMEWORK" ] && echo "  Framework: $FRAMEWORK"
[ -n "$DATABASE" ] && echo "  Database: $DATABASE"

# Generate mcp-servers.md
cat > "$CONTEXT_DIR/mcp-servers.md" << EOF
# MCP Server Context

This file documents the available MCP servers and project technology context.
AI agents should reference this when planning implementations.

## Available MCP Servers

EOF

if [ ${#MCP_SERVERS[@]} -gt 0 ]; then
    echo "| Server | Source |" >> "$CONTEXT_DIR/mcp-servers.md"
    echo "|--------|--------|" >> "$CONTEXT_DIR/mcp-servers.md"
    
    for server in "${MCP_SERVERS[@]}"; do
        echo "| $server | ${MCP_SOURCES[$server]:-unknown} |" >> "$CONTEXT_DIR/mcp-servers.md"
    done
else
    echo "*No MCP servers detected in configurations.*" >> "$CONTEXT_DIR/mcp-servers.md"
    
    if [ "$NPX_AVAILABLE" = true ]; then
        cat >> "$CONTEXT_DIR/mcp-servers.md" << 'EOF'

### Available via npx

The following MCP servers can be used via npx:
- `npx -y @modelcontextprotocol/server-filesystem` - File operations
- `npx -y @modelcontextprotocol/server-git` - Git operations  
- `npx -y @modelcontextprotocol/server-github` - GitHub API
- `npx -y @modelcontextprotocol/server-postgres` - PostgreSQL
- `npx -y @modelcontextprotocol/server-sqlite` - SQLite
- `npx -y @modelcontextprotocol/server-fetch` - HTTP fetch
EOF
    fi
fi

cat >> "$CONTEXT_DIR/mcp-servers.md" << EOF

## Project Technology Stack

- **Primary Language:** $LANGUAGE
EOF

[ -n "$FRAMEWORK" ] && echo "- **Framework:** $FRAMEWORK" >> "$CONTEXT_DIR/mcp-servers.md"
[ -n "$PACKAGE_MANAGER" ] && echo "- **Package Manager:** $PACKAGE_MANAGER" >> "$CONTEXT_DIR/mcp-servers.md"
[ -n "$DATABASE" ] && echo "- **Database:** $DATABASE" >> "$CONTEXT_DIR/mcp-servers.md"
[ -n "$MONOREPO" ] && echo "- **Monorepo Type:** $MONOREPO" >> "$CONTEXT_DIR/mcp-servers.md"
[ -n "$SERVICES" ] && echo "- **Services:** $SERVICES" >> "$CONTEXT_DIR/mcp-servers.md"

cat >> "$CONTEXT_DIR/mcp-servers.md" << EOF

## Recommendations

EOF

# Add recommendations based on detected tech
if [ -n "$DATABASE" ] && [ "$DATABASE" = "postgres" ]; then
    echo "- Consider configuring the **postgres** MCP server for database operations" >> "$CONTEXT_DIR/mcp-servers.md"
fi

if [ -n "$DATABASE" ] && [ "$DATABASE" = "sqlite" ]; then
    echo "- Consider configuring the **sqlite** MCP server for database operations" >> "$CONTEXT_DIR/mcp-servers.md"
fi

if echo "$SERVICES" | grep -q "github-actions"; then
    echo "- Consider configuring the **github** MCP server for GitHub API integration" >> "$CONTEXT_DIR/mcp-servers.md"
fi

cat >> "$CONTEXT_DIR/mcp-servers.md" << EOF

---
*Generated by project-specify on $(date)*
EOF

# Generate project-context.json
cat > "$CONTEXT_DIR/project-context.json" << EOF
{
  "primary_language": "$LANGUAGE",
  "framework": $([ -n "$FRAMEWORK" ] && echo "\"$FRAMEWORK\"" || echo "null"),
  "package_manager": $([ -n "$PACKAGE_MANAGER" ] && echo "\"$PACKAGE_MANAGER\"" || echo "null"),
  "database": $([ -n "$DATABASE" ] && echo "\"$DATABASE\"" || echo "null"),
  "monorepo_type": $([ -n "$MONOREPO" ] && echo "\"$MONOREPO\"" || echo "null"),
  "detected_services": [$(echo "$SERVICES" | sed 's/ /", "/g' | sed 's/^/"/' | sed 's/$/"/' | sed 's/^""$//')],
  "mcp_servers": [$(printf '"%s",' "${MCP_SERVERS[@]}" | sed 's/,$//')],
  "npx_available": $NPX_AVAILABLE,
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

echo ""
echo "✅ Discovery complete!"
echo "   - MCP context: $CONTEXT_DIR/mcp-servers.md"
echo "   - Project context: $CONTEXT_DIR/project-context.json"