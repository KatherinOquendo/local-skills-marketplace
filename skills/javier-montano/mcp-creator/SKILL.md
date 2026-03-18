---
name: mcp-creator
description: >
  This skill should be used when the user asks to "configure an MCP server", "connect Claude to
  an external tool", "set up a database MCP", "add an API integration via MCP", or "list MCP
  servers". Also triggers on mentions of Model Context Protocol, stdio transport, MCP JSON config,
  or remote tool connections. Use this skill even if the user only wants to check existing MCP
  configuration — the full setup and validation workflow applies.
argument-hint: <server-name> [transport: stdio|http]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# MCP Creator

Configure Model Context Protocol servers — the bridge between Claude Code and external tools, databases, APIs.

## Assumptions & Limits

- **Assumes** the target service exists and is accessible (this skill configures the connection, not the server)
- **Limit**: stdio servers run as child processes — they consume resources for the session duration
- **Limit**: SSE transport is deprecated — use HTTP for all new remote connections
- **Limit**: OAuth flows require browser access; headless environments need pre-configured tokens
- **Trade-off**: Local scope (default) = private but not shared; project scope = shared but exposes config to git

### When NOT to use MCP

| Situation | Better alternative |
|---|---|
| One-off API call | Bash with curl |
| File system operations | Built-in Read/Write/Glob tools |
| Git operations | Built-in Bash with git |
| Static data reference | CLAUDE.md or skill reference files |

## Usage

```
/mcp-creator my-database stdio        # local database server
/mcp-creator analytics-api http       # remote API
/mcp-creator project-tools            # interview mode
```

Parse `$1` as server name (kebab-case), `$2` as transport. If missing, ask:
1. What external system? (database, API, file service, custom tool)
2. Local process or remote endpoint?
3. Auth required? (API key, OAuth, none)

## Before Creating

1. **Check existing**: Run `claude mcp list` to see configured servers
2. **Read project MCP**: `Read .mcp.json` if it exists
3. **Verify no name collision**: Server names must be unique across all scopes

## Transport Types

### stdio (local processes — most common)

```json
{
  "mcpServers": {
    "{name}": {
      "type": "stdio",
      "command": "node",
      "args": ["./mcp-server/index.js"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

**When**: Server runs on the same machine. Typical for databases, local tools, custom scripts.
**Lifecycle**: Spawned on first tool use, killed on session end.

### HTTP (remote — recommended for cloud)

```json
{
  "mcpServers": {
    "{name}": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

**When**: Server is a remote endpoint. Stateless, no process management.

## Configuration Scopes

| Scope | Storage | Precedence | Use When |
|---|---|---|---|
| Local | `~/.claude.json` | Highest | Personal, current project |
| Project | `.mcp.json` (git tracked) | Medium | Team-shared servers |
| User | `~/.claude.json` | Lowest | Personal, all projects |
| Plugin | Plugin's `.mcp.json` | Plugin scope | Bundled with plugin |

**Decision logic**: If the whole team needs it → project scope. If only you → local. If across all your projects → user.

## Environment Variables

Use `${VAR}` in command, args, env, url, headers:

```json
{
  "env": {
    "API_KEY": "${MY_API_KEY}",
    "DB_URL": "${DATABASE_URL:-sqlite:///fallback.db}",
    "HOME_DIR": "${HOME}"
  }
}
```

- `${VAR}` — required, fails if missing
- `${VAR:-default}` — optional with fallback

**Security rule**: NEVER hardcode secrets. Always use env vars.

## Common Server Patterns

### PostgreSQL
```json
{
  "mcpServers": {
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

### Filesystem (sandboxed)
```json
{
  "mcpServers": {
    "files": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${PROJECT_DATA_DIR}"]
    }
  }
}
```

### Custom API with OAuth
```bash
claude mcp add --transport http my-api https://api.example.com/mcp \
  --client-id "${CLIENT_ID}" \
  --client-secret "${CLIENT_SECRET}" \
  --callback-port 3000
```
Then authenticate via `/mcp` in session.

### Plugin-bundled server
```json
{
  "mcpServers": {
    "my-tool": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/tool.js"]
    }
  }
}
```

## CLI Quick Reference

```bash
claude mcp add --transport stdio my-db -- node server.js   # Add stdio
claude mcp add --transport http my-api https://url.com      # Add HTTP
claude mcp list                                             # List all
claude mcp remove my-db                                     # Remove
```

**Flag order matters**: `--transport`, `--env`, `--scope` BEFORE server name. `--` separates name from command/args.

## Output Token Limits

| Threshold | Behavior |
|---|---|
| 10,000 tokens | Warning logged |
| 25,000 tokens | Default max (truncated) |
| Custom | `MAX_MCP_OUTPUT_TOKENS=50000` env var |

## MCP Tool Search (auto-discovery)

When MCP tools exceed 10% of context window, Claude auto-enables tool search — loading tool definitions on demand instead of all at once. Control with `ENABLE_TOOL_SEARCH`: `auto` (default), `true`, `false`.

## Edge Cases

- **Server crashes mid-session**: Claude retries once, then reports error. Add health check in server.
- **Port conflict on stdio**: Each server gets its own process; ports only conflict if servers bind the same port.
- **Large tool output**: Exceeding MAX_MCP_OUTPUT_TOKENS silently truncates. Paginate in server if possible.
- **Multiple servers, same API**: Valid — use for different auth contexts or rate limit isolation.

## Validation Gate

- [ ] Server name is kebab-case and unique across all scopes
- [ ] Transport type is `stdio` or `http` (not deprecated `sse`)
- [ ] For stdio: command exists (`which {command}`) and is executable
- [ ] For http: URL is valid format (https preferred)
- [ ] All secrets use `${ENV_VAR}` syntax, none hardcoded
- [ ] Config saved to correct scope (local/project/user)
- [ ] Server responds after config: `claude mcp list` shows it
- [ ] Env vars referenced in config are actually set in environment

---
**Author:** Javier Montaño | **Last updated:** 2026-03-12
