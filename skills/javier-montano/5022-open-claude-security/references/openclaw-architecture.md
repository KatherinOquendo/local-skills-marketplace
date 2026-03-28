---
name: openclaw-architecture-security
description: OpenClaw Gateway→Core→Tools architecture security patterns, Docker isolation templates, network policies, and personal deployment security profiles
type: reference
---

# OpenClaw Architecture Security Reference

Security patterns specific to the OpenClaw 3-layer architecture: Gateway (messaging adapters), Core (agent engine), and Tools (File System, Terminal, Browser, APIs). [EXPLICIT]

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GATEWAY LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ WhatsApp │  │  Slack   │  │ Telegram │  │ HTTP API │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       └──────────────┴──────────────┴──────────────┘         │
│                         │                                    │
│                    Local & Private                            │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────────┐     │
│  │              CORE LAYER                             │     │
│  │  ┌──────────────┐  ┌──────────────┐                │     │
│  │  │ Agent Engine  │  │ Security     │                │     │
│  │  │ (LLM Loop)   │  │ Checkpoints  │                │     │
│  │  └──────────────┘  └──────────────┘                │     │
│  │  ┌──────────────┐  ┌──────────────┐                │     │
│  │  │ Memory       │  │ Config       │                │     │
│  │  │ (SQLite WAL) │  │ (.env, JSON) │                │     │
│  │  └──────────────┘  └──────────────┘                │     │
│  └──────┬──────────┬──────────┬──────────┬────────────┘     │
│         │          │          │          │                    │
│         ▼          ▼          ▼          ▼                    │
│  ┌──────────┐ ┌────────┐ ┌─────────┐ ┌──────┐              │
│  │  File    │ │Terminal│ │ Browser │ │ APIs │  TOOL LAYER   │
│  │  System  │ │  Bash  │ │  MCP    │ │ MCP  │              │
│  └──────────┘ └────────┘ └─────────┘ └──────┘              │
└─────────────────────────────────────────────────────────────┘
```

[EXPLICIT]

---

## 2. Gateway Layer Security

### 2.1 Sender Authentication

| Platform | Auth Method | Personal Deploy Pattern |
|----------|-------------|------------------------|
| Telegram | Bot token + chat_id allowlist | Only respond to your own chat_id [EXPLICIT] |
| WhatsApp | Business API + phone number allowlist | Only respond to your own number [EXPLICIT] |
| Slack | Bot token + workspace verification | Only respond in your personal workspace [EXPLICIT] |
| HTTP API | API key + IP allowlist | Localhost only (127.0.0.1) [EXPLICIT] |

### 2.2 Message Sanitization

Before passing messages to the Core, sanitize:
- Strip HTML/markdown that could be interpreted as agent instructions [EXPLICIT]
- Limit message length (prevent context window flooding) [EXPLICIT]
- Log sender identity for audit trail (not message content for privacy) [EXPLICIT]
- Rate limit: max 10 messages/minute per sender for personal deploy [INFERRED]

### 2.3 Gateway-to-Core Trust Boundary

The Gateway must validate before forwarding to Core:

| Validation | Check | Block If |
|------------|-------|----------|
| Sender identity | chat_id or phone in allowlist | Unknown sender [EXPLICIT] |
| Message size | Length < 10,000 chars | Oversized payload [INFERRED] |
| Rate limit | < 10 msg/min per sender | Flood attempt [INFERRED] |
| Content screening | No system-prompt-like patterns | Injection attempt [EXPLICIT] |

---

## 3. Core Layer Security

### 3.1 Security Checkpoints (3-Layer Defense)

The OpenClaw Core implements 3 security checkpoints in the agent loop. [EXPLICIT]

```
User Message → [CP1: Sanitize] → LLM Processing → [CP2: Harden] → Tool Call → [CP3: Validate] → Response
```

| Checkpoint | Purpose | Implementation |
|------------|---------|----------------|
| CP1: Sanitize | Clean input of injection patterns | Regex-based content filter on inbound messages [EXPLICIT] |
| CP2: Harden | Validate tool call parameters before execution | PreToolUse hook with pattern matching [EXPLICIT] |
| CP3: Validate | Verify tool results before including in response | PostToolUse hook with content screening [EXPLICIT] |

### 3.2 Memory Security (SQLite)

| Concern | Risk | Control |
|---------|------|---------|
| Memory size | Unbounded growth → disk exhaustion | 32KB per conversation guard [EXPLICIT] |
| SQL injection | Malicious content in conversation stored unsafely | Prepared statements only (no string interpolation) [EXPLICIT] |
| Data persistence | Conversation history contains sensitive data | WAL mode for integrity; periodic cleanup for privacy [EXPLICIT] |
| File permissions | SQLite file readable by other processes | chmod 600 on memory.db [EXPLICIT] |

### 3.3 Config Security

| File | Risk | Control |
|------|------|---------|
| .env | Plaintext secrets | File permissions 600, gitignored, Docker env-file [EXPLICIT] |
| config.ts | Env loading order manipulation | Fail-fast on missing required vars [EXPLICIT] |
| CLAUDE.md | Instruction injection | See main SKILL.md S2 [EXPLICIT] |

---

## 4. Tool Layer Security

### 4.1 File System Tool

| Risk | Attack | Control |
|------|--------|---------|
| Path traversal | Agent reads files outside project directory | Bind mount only workspace dir in Docker [EXPLICIT] |
| Sensitive file access | Agent reads .env, .ssh, credentials | PreToolUse hook blocks sensitive paths [EXPLICIT] |
| Write to system files | Agent modifies /etc/hosts, crontab | read_only Docker + cap_drop ALL [EXPLICIT] |

**Personal deploy file allowlist**:
```
ALLOW: /app/workspace/**  (project files)
BLOCK: /app/.env, /root/.ssh/*, /etc/*, /var/*
```
[EXPLICIT]

### 4.2 Terminal/Bash Tool

| Risk | Attack | Control |
|------|--------|---------|
| Arbitrary execution | Agent runs `rm -rf /`, `curl | sh` | PreToolUse hook with command blocklist [EXPLICIT] |
| Network access | Agent exfiltrates data via curl/wget | Docker network internal:true [EXPLICIT] |
| Package installation | Agent installs malicious packages | Block npm/pip install in production [INFERRED] |
| Process spawning | Agent spawns background processes | PID limits in Docker [INFERRED] |

**Bash command blocklist for personal deploy:**
```python
BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/",           # destructive delete
    r"curl.*\|\s*(sh|bash)",    # download and execute
    r"eval\s+",                 # arbitrary eval
    r"nc\s+-l",                 # netcat listener
    r"chmod\s+777",             # world-writable
    r">(>)?\s*/etc/",           # write to system
    r"ssh\s+",                  # SSH connections
    r"scp\s+",                  # secure copy
]
```
[EXPLICIT]

### 4.3 Browser MCP Tool

| Risk | Attack | Control |
|------|--------|---------|
| Malicious page content | Page contains prompt injection | Content isolation rules [EXPLICIT] |
| Credential capture | Agent fills in passwords on fake sites | Block credential input actions [EXPLICIT] |
| Data exfiltration | Agent uploads sensitive data via browser | Network egress control [EXPLICIT] |
| Session hijacking | Agent accesses saved sessions/cookies | Isolated browser profile [INFERRED] |

### 4.4 API MCP Tools

| Risk | Attack | Control |
|------|--------|---------|
| Unvetted API endpoints | MCP connects to unknown services | MCP vetting checklist [EXPLICIT] |
| Data classification breach | Sensitive data sent to wrong API | Data flow mapping per MCP [EXPLICIT] |
| Token exposure | API tokens in MCP config | Environment variable references only [EXPLICIT] |
| Response injection | API returns instruction-like content | Treat all MCP responses as untrusted [EXPLICIT] |

---

## 5. Docker Isolation Templates

### 5.1 Personal Deploy (Maximum Isolation)

```yaml
version: "3.8"
services:
  openclaw:
    build:
      context: .
      dockerfile: Dockerfile
    security_opt:
      - "no-new-privileges:true"
    read_only: true
    tmpfs:
      - /tmp:size=100m
    cap_drop:
      - ALL
    mem_limit: "2g"
    cpus: "2.0"
    pids_limit: 100
    volumes:
      - ./workspace:/app/workspace
    env_file:
      - .env
    networks:
      - isolated
    restart: unless-stopped

networks:
  isolated:
    driver: bridge
    internal: true  # NO internet access
```
[EXPLICIT]

### 5.2 Personal Deploy (Controlled Egress)

```yaml
version: "3.8"
services:
  openclaw:
    build: .
    security_opt: ["no-new-privileges:true"]
    read_only: true
    tmpfs: ["/tmp:size=100m"]
    cap_drop: ["ALL"]
    mem_limit: "2g"
    cpus: "2.0"
    volumes:
      - ./workspace:/app/workspace
    env_file: [".env"]
    networks:
      - controlled

networks:
  controlled:
    driver: bridge
    # NOT internal — allows egress, but use iptables/firewall rules
    # to restrict to specific IPs/domains
```

Add iptables rules or Docker network plugin to allow only:
- Anthropic API (api.anthropic.com)
- Specific MCP endpoints (documented with justification)
[EXPLICIT]

---

## 6. Subagent vs Agent Team Security Patterns

### 6.1 Subagent Pattern Security

```
Main Agent (full permissions)
  ├── Spawn Subagent A (read-only)  → Work → Result
  ├── Spawn Subagent B (read-only)  → Work → Result
  └── Spawn Subagent C (bash-only)  → Work → Result
                                              ↓
                                         Main aggregates
                                         (deterministic)
```

Security properties:
- Each subagent gets restricted allowed-tools (not parent's full set) [EXPLICIT]
- Results flow back to main agent only (no lateral communication) [EXPLICIT]
- Main agent validates results before acting on them [EXPLICIT]
- Depth limit prevents recursive spawning (depth=1) [EXPLICIT]

### 6.2 Agent Team Pattern Security

```
Team Lead (orchestrator permissions)
  → Shared Task List (access-controlled)
     ← Teammate A (code-review tools) claims & works
     ← Teammate B (test-writing tools) claims & works
     ← Teammate C (deploy tools) claims & works
     (teammates can communicate via shared list)
```

Security properties:
- Task list is the only communication channel (no direct agent-to-agent) [INFERRED]
- Each teammate has role-specific allowed-tools [INFERRED]
- Team lead validates completed tasks before aggregation [INFERRED]
- Shared task list requires write-access control (who can add tasks) [INFERRED]

### 6.3 Which Pattern for Personal Deploy?

| Criterion | Subagent | Agent Team |
|-----------|----------|------------|
| Security complexity | Lower (tree structure) | Higher (mesh communication) |
| Permission control | Per-subagent easy | Per-teammate + shared list |
| Attack surface | One parent, N isolated workers | N peers with communication |
| Best for personal | Simple tasks, parallel research | Complex workflows needing coordination |

**Recommendation**: Start with Subagent pattern. Graduate to Agent Team only when peer communication provides measurable value. [INFERRED]
