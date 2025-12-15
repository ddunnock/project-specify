# MCP (Model Context Protocol) Setup Guide

This guide explains how project-specify integrates with MCP servers to enhance AI capabilities and provide better context-aware development.

## What is MCP?

**Model Context Protocol (MCP)** is a standard for providing AI models with structured access to external tools and data sources. MCP servers expose specific capabilities (like database access, file operations, or API integrations) that AI assistants can use during development.

### Why MCP Matters for Project-Specify

Project-specify can automatically discover your installed MCP servers and:

1. **Generate relevant context files** (`.mcp/context.md`) that inform AI assistants about available capabilities
2. **Suggest technology-specific MCP servers** based on your project structure
3. **Enable smarter AI recommendations** by understanding what tools are available

## How MCP Discovery Works

When you run `specify init`, project-specify:

1. **Scans for MCP configuration files** in standard locations:
   - Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
   - Claude Desktop: `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
   - Claude Code: `~/.claude/config.json`
   - Cursor: `.cursorrules` and Cursor settings
   - Project-local: `.mcp/servers.json`

2. **Detects project technology** by analyzing files:
   - `package.json` → Node.js/TypeScript project
   - `requirements.txt`, `pyproject.toml` → Python project
   - `Cargo.toml` → Rust project
   - Database files or configs → Database usage

3. **Generates context files** that describe:
   - Available MCP servers and their capabilities
   - Suggested servers based on project type
   - How AI assistants can leverage these tools

## Supported MCP Server Locations

### Claude Desktop

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Example configuration:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/projects"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Claude Code

**Location:**
```
~/.claude/config.json
```

**Example configuration:**

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/username/projects"]
      },
      "sqlite": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"]
      }
    }
  }
}
```

### Cursor

Cursor MCP integration is configured through `.cursorrules` files and Cursor settings.

**Example `.cursorrules`:**

```yaml
mcp:
  servers:
    - name: filesystem
      command: npx
      args: ["-y", "@modelcontextprotocol/server-filesystem", "./"]
```

### Project-Local MCP Servers

You can define project-specific MCP servers in `.mcp/servers.json`:

**Location:**
```
your-project/.mcp/servers.json
```

**Example:**

```json
{
  "mcpServers": {
    "project-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "./data/project.db"]
    },
    "api-client": {
      "command": "node",
      "args": ["./tools/api-mcp-server.js"]
    }
  }
}
```

## Common MCP Servers and Their Use Cases

### Filesystem MCP Server

**Purpose:** Provides structured file access and search capabilities

**Best for:**
- Reading/writing project files
- Searching across codebases
- File tree navigation

**Install:**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Configuration:**
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
  }
}
```

### GitHub MCP Server

**Purpose:** Interact with GitHub repositories, issues, and PRs

**Best for:**
- Creating issues and PRs from AI conversations
- Searching GitHub code
- Repository analysis

**Install:**
```bash
npm install -g @modelcontextprotocol/server-github
```

**Configuration:**
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "ghp_your_token_here"
    }
  }
}
```

### PostgreSQL MCP Server

**Purpose:** Direct database access for schema inspection and queries

**Best for:**
- Database-driven applications
- SQL query generation
- Schema migrations

**Install:**
```bash
npm install -g @modelcontextprotocol/server-postgres
```

**Configuration:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost/dbname"]
  }
}
```

### SQLite MCP Server

**Purpose:** Lightweight database access for SQLite databases

**Best for:**
- Local-first applications
- Development databases
- Testing environments

**Install:**
```bash
npm install -g @modelcontextprotocol/server-sqlite
```

**Configuration:**
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"]
  }
}
```

## Technology-Specific Recommendations

### Python Projects

**Recommended MCP servers:**
- `filesystem` - Code navigation and file operations
- `github` - Repository integration
- `postgres` or `sqlite` - Database access (if applicable)

**Example setup:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token"
      }
    }
  }
}
```

### Node.js/TypeScript Projects

**Recommended MCP servers:**
- `filesystem` - Package and source code access
- `github` - NPM package search and repository access
- Database server based on your stack

**Example setup:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token"
      }
    }
  }
}
```

### Rust Projects

**Recommended MCP servers:**
- `filesystem` - Cargo.toml and source access
- `github` - Crates.io search and docs

**Example setup:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token"
      }
    }
  }
}
```

### Full-Stack Web Applications

**Recommended MCP servers:**
- `filesystem` - Frontend and backend code access
- `postgres` or `mysql` - Database operations
- `github` - Repository and deployment integration

**Example setup:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/app_db"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token"
      }
    }
  }
}
```

## Disabling MCP Discovery

If you don't want project-specify to scan for MCP servers, use the `--no-mcp-discovery` flag:

```bash
specify init my-project --ai claude --no-mcp-discovery
```

This skips all MCP detection and context file generation.

## Troubleshooting MCP Issues

### MCP Servers Not Detected

**Symptom:** `.mcp/context.md` not generated or empty

**Solutions:**
1. Verify MCP config files exist at the standard locations
2. Check JSON syntax in configuration files
3. Ensure file paths in config are absolute, not relative
4. Run `specify init` with `--debug` flag for detailed logs

**Example debug command:**
```bash
specify init my-project --ai claude --debug
```

### Wrong MCP Servers Suggested

**Symptom:** Suggested servers don't match your project type

**Solutions:**
1. Check project structure - project-specify uses file detection
2. Add missing technology indicator files (e.g., `package.json` for Node.js)
3. Manually configure `.mcp/servers.json` in your project
4. Use `--no-mcp-discovery` and configure manually

### MCP Server Commands Failing

**Symptom:** AI assistant can't use MCP capabilities

**Solutions:**
1. Verify MCP server packages are installed globally
2. Check that `npx` is available in PATH
3. Test MCP server commands manually:
   ```bash
   npx -y @modelcontextprotocol/server-filesystem /path/to/project
   ```
4. Check environment variables (e.g., `GITHUB_TOKEN`) are set correctly

### Environment Variable Expansion

MCP configurations support environment variable expansion:

**Example:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
  }
}
```

**Troubleshooting:**
1. Ensure environment variables are set before AI assistant starts
2. Use absolute values for testing:
   ```json
   "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/test"]
   ```

## Best Practices

1. **Start minimal** - Add MCP servers as needed, don't install everything upfront
2. **Use project-local configs** for project-specific tools (`.mcp/servers.json`)
3. **Use global configs** for universal tools (filesystem, github)
4. **Secure sensitive data** - Use environment variables for tokens and passwords
5. **Test individually** - Verify each MCP server works before adding to config
6. **Document custom servers** - Add README or comments explaining project-specific MCP setups

## Example Complete Setups

### Minimal Setup (Filesystem Only)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    }
  }
}
```

### Standard Web App Setup

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

### Full-Featured Setup

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    },
    "redis": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-redis", "redis://localhost:6379"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    }
  }
}
```

## Learn More

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Building Custom MCP Servers](https://modelcontextprotocol.io/docs/guides/building-servers)

## Related Documentation

- [Windows Setup Guide](./windows-setup.md)
- [Monorepo Guide](./monorepo-guide.md)
- [Main README](../README.md)
