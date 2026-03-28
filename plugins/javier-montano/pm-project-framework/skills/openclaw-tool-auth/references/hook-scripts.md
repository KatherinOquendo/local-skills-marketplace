# Hook Scripts Reference — openclaw-tool-auth

Production-ready hook script implementations for Claude Code PreToolUse and PostToolUse hooks. Each script is self-contained with logging, error handling, and fail-closed behavior. [EXPLICIT]

## Configuration Prerequisites

All scripts expect the following environment:

```bash
# Set by Claude Code automatically:
# TOOL_NAME  — name of the tool being invoked (e.g., "Bash", "Read")
# TOOL_INPUT — JSON string with tool parameters

# Set by user in shell profile or .env:
export PROJECT_ROOT="$(pwd)"
export TOOL_AUTH_MODE="enforce"       # enforce | audit-only
export TOOL_AUTH_LOG=".claude/logs/tool-auth.jsonl"
export GATEWAY_AUTH_CONFIG=".claude/gateway-auth.json"
```

Create the log directory before first use:

```bash
mkdir -p .claude/logs .claude/hooks
```

---

## 1. validate-bash.py — PreToolUse Hook for Bash

Validates Bash commands against a blocklist of dangerous patterns. Supports allowlist mode for strict environments. Logs all decisions. Fails closed on errors. [EXPLICIT]

```python
#!/usr/bin/env python3
"""
PreToolUse hook: Bash command authorization.

Validates commands against blocklist patterns and optional allowlist.
Exit 0 = allow, Exit 2 = block. Never exits 1 (fail-open).

Install:
  cp validate-bash.py .claude/hooks/
  # Add to .claude/settings.json hooks.PreToolUse with matcher "Bash"
"""
import os
import sys
import json
import re
import datetime
from pathlib import Path

# --- Configuration ---

MODE = os.environ.get("TOOL_AUTH_MODE", "enforce")
LOG_FILE = os.environ.get(
    "TOOL_AUTH_LOG",
    os.path.join(os.environ.get("PROJECT_ROOT", "."), ".claude", "logs", "tool-auth.jsonl")
)

# Blocklist: (regex_pattern, label, severity)
BLOCKLIST = [
    # Destructive operations
    (r'\brm\s+(-[rRf]+\s+)*/', "destructive-rm-absolute", "critical"),
    (r'\brm\s+-[rRf]*\s+\.\.\/', "destructive-rm-parent-traversal", "critical"),
    (r'\bmkfs\b', "filesystem-format", "critical"),
    (r'\bdd\s+if=', "raw-disk-operation", "critical"),
    (r'\b>\s*/dev/sd', "raw-device-write", "critical"),

    # Privilege escalation
    (r'\bsudo\b', "privilege-escalation-sudo", "critical"),
    (r'\bsu\s+-', "privilege-escalation-su", "critical"),
    (r'\bchmod\s+777\b', "world-writable-permission", "high"),
    (r'\bchown\s+root\b', "chown-root", "high"),

    # Network exfiltration
    (r'\bcurl\b.*\|\s*(sh|bash|python)', "pipe-to-shell-curl", "critical"),
    (r'\bwget\b.*\|\s*(sh|bash|python)', "pipe-to-shell-wget", "critical"),
    (r'\bnc\s+-[lp]', "netcat-listener", "critical"),
    (r'\b(bash|sh)\s+-i\s+>&\s*/dev/tcp/', "reverse-shell", "critical"),
    (r'\bscp\b.*@', "scp-remote-transfer", "high"),

    # Self-modification
    (r'dangerouslySkipPermissions', "self-modify-skip-permissions", "critical"),
    (r'\.claude/settings', "self-modify-settings", "high"),
    (r'\.claude/hooks', "self-modify-hooks", "high"),

    # Credential access
    (r'\bcat\s+.*\.env\b', "read-env-file", "high"),
    (r'\bcat\s+.*id_rsa', "read-ssh-key", "high"),
    (r'\bcat\s+.*id_ed25519', "read-ssh-key", "high"),
    (r'\bprintenv\b', "dump-environment", "medium"),
    (r'\bcat\s+.*/\.aws/', "read-aws-credentials", "high"),

    # Package installation (may introduce supply-chain risk)
    (r'\bnpm\s+install\s+-g\b', "global-npm-install", "medium"),
    (r'\bpip\s+install\b', "pip-install", "medium"),
    (r'\bapt\s+(install|remove)\b', "apt-modification", "medium"),
]

# Allowlist: only used when TOOL_AUTH_ALLOWLIST=true
ALLOWLIST_ENABLED = os.environ.get("TOOL_AUTH_ALLOWLIST", "false").lower() == "true"
ALLOWLIST = [
    r'^(ls|cat|head|tail|wc|sort|uniq|diff|file|stat)\b',
    r'^(grep|rg|find|fd)\b',
    r'^(echo|printf)\b',
    r'^git\s+(status|log|diff|show|branch|tag|remote)\b',
    r'^npm\s+(test|run\s+(lint|build|check|format))\b',
    r'^python3?\s+[\w./-]+\.py(\s|$)',
    r'^node\s+[\w./-]+\.(js|mjs|ts)(\s|$)',
    r'^(mkdir|cp|mv|touch)\b',           # basic file ops (blocked paths caught separately)
    r'^(date|whoami|hostname|uname)\b',   # info commands
]

# --- Logging ---

def log_decision(command: str, decision: str, reason: str = "", severity: str = ""):
    """Append structured log entry to JSONL file."""
    try:
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        entry = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "tool": "Bash",
            "command": command[:500],  # truncate to prevent log injection
            "decision": decision,
            "reason": reason,
            "severity": severity,
            "mode": MODE,
        }
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=True) + "\n")
    except Exception:
        pass  # logging failure must not affect hook decision

# --- Main ---

def main():
    try:
        raw_input = os.environ.get("TOOL_INPUT", "{}")
        tool_input = json.loads(raw_input)
        command = tool_input.get("command", "")

        if not command.strip():
            log_decision("", "BLOCKED", "empty-command", "low")
            print("BLOCKED by tool-auth: empty command", file=sys.stderr)
            sys.exit(2)

        # Phase 1: Blocklist check
        for pattern, label, severity in BLOCKLIST:
            if re.search(pattern, command, re.IGNORECASE):
                log_decision(command, "BLOCKED", label, severity)
                if MODE == "enforce":
                    print(f"BLOCKED by tool-auth: {label} [{severity}]", file=sys.stderr)
                    sys.exit(2)
                else:
                    # audit-only: log but allow
                    log_decision(command, "AUDIT-WOULD-BLOCK", label, severity)
                    sys.exit(0)

        # Phase 2: Allowlist check (if enabled)
        if ALLOWLIST_ENABLED:
            matched = False
            for pattern in ALLOWLIST:
                if re.search(pattern, command.strip(), re.IGNORECASE):
                    matched = True
                    break
            if not matched:
                log_decision(command, "BLOCKED", "not-in-allowlist", "medium")
                if MODE == "enforce":
                    print("BLOCKED by tool-auth: command not in allowlist", file=sys.stderr)
                    sys.exit(2)
                else:
                    log_decision(command, "AUDIT-WOULD-BLOCK", "not-in-allowlist", "medium")
                    sys.exit(0)

        # Passed all checks
        log_decision(command, "ALLOWED")
        sys.exit(0)

    except json.JSONDecodeError as e:
        log_decision("JSON_PARSE_ERROR", "BLOCKED", str(e), "high")
        print(f"BLOCKED by tool-auth: invalid JSON input: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        log_decision("UNEXPECTED_ERROR", "BLOCKED", str(e), "high")
        print(f"BLOCKED by tool-auth: hook error (fail-closed): {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

**Key design decisions:**
- Blocklist runs before allowlist — a blocklisted command is always blocked even if it matches an allowlist entry. [EXPLICIT]
- Command truncated to 500 chars in logs to prevent log injection and storage abuse. [EXPLICIT]
- All exceptions route to exit(2) — fail-closed behavior prevents accidental allow on crash. [EXPLICIT]
- Audit-only mode logs what would have been blocked but allows execution (for migration). [EXPLICIT]

---

## 2. validate-file-access.py — PreToolUse Hook for Read/Write/Edit

Validates file paths against project root boundaries, sensitive file patterns, and write-protected paths. [EXPLICIT]

```python
#!/usr/bin/env python3
"""
PreToolUse hook: File access authorization for Read, Write, Edit tools.

Validates file paths are within project root, not sensitive files,
and not in write-protected locations (for Write/Edit).
Exit 0 = allow, Exit 2 = block. Never exits 1.

Install:
  cp validate-file-access.py .claude/hooks/
  # Add to .claude/settings.json hooks.PreToolUse with matcher "Read|Write|Edit"
"""
import os
import sys
import json
import datetime
from pathlib import Path

# --- Configuration ---

MODE = os.environ.get("TOOL_AUTH_MODE", "enforce")
LOG_FILE = os.environ.get(
    "TOOL_AUTH_LOG",
    os.path.join(os.environ.get("PROJECT_ROOT", "."), ".claude", "logs", "tool-auth.jsonl")
)
PROJECT_ROOT = os.path.realpath(os.path.abspath(
    os.environ.get("PROJECT_ROOT", os.getcwd())
))

# Patterns that should never be read or written
BLOCKED_FILE_PATTERNS = [
    ".env",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    "id_rsa",
    "id_ed25519",
    "id_ecdsa",
    "id_dsa",
    "credentials.json",
    "service-account",
    ".aws/credentials",
    ".aws/config",
    ".ssh/",
    ".gnupg/",
    "token.json",
    ".netrc",
]

# Additional paths blocked for Write/Edit only
WRITE_PROTECTED_PATTERNS = [
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".claude/hooks/",
    ".git/",
]

# Directories that must never be accessed
BLOCKED_DIRECTORIES = [
    os.path.expanduser("~/.ssh"),
    os.path.expanduser("~/.aws"),
    os.path.expanduser("~/.gnupg"),
    os.path.expanduser("~/.config/gcloud"),
    "/etc/shadow",
    "/etc/passwd",
]

# --- Logging ---

def log_decision(tool: str, path: str, decision: str, reason: str = ""):
    try:
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        entry = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "tool": tool,
            "path": path[:300],
            "decision": decision,
            "reason": reason,
            "mode": MODE,
        }
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=True) + "\n")
    except Exception:
        pass

# --- Validation ---

def extract_path(tool_name: str, tool_input: dict) -> str:
    """Extract the file path from tool input based on tool type."""
    if tool_name == "Read":
        return tool_input.get("file_path", "")
    elif tool_name == "Write":
        return tool_input.get("file_path", "")
    elif tool_name == "Edit":
        return tool_input.get("file_path", "")
    return ""


def validate_path(tool_name: str, file_path: str) -> tuple:
    """Validate a file path. Returns (allowed: bool, reason: str)."""
    if not file_path:
        return False, "empty-path"

    # Resolve symlinks and normalize
    try:
        resolved = os.path.realpath(os.path.abspath(file_path))
    except (OSError, ValueError) as e:
        return False, f"path-resolution-error: {e}"

    # Check: must be within project root
    if not resolved.startswith(PROJECT_ROOT + os.sep) and resolved != PROJECT_ROOT:
        return False, f"outside-project-root"

    # Check: blocked directories
    for blocked_dir in BLOCKED_DIRECTORIES:
        blocked_resolved = os.path.realpath(os.path.abspath(blocked_dir))
        if resolved.startswith(blocked_resolved):
            return False, f"blocked-directory: {blocked_dir}"

    # Check: blocked file patterns
    resolved_lower = resolved.lower()
    for pattern in BLOCKED_FILE_PATTERNS:
        if pattern in resolved_lower:
            return False, f"sensitive-file: {pattern}"

    # Check: write-protected paths (for Write and Edit only)
    is_write = tool_name in ("Write", "Edit")
    if is_write:
        rel_path = os.path.relpath(resolved, PROJECT_ROOT)
        for protected in WRITE_PROTECTED_PATTERNS:
            if rel_path.startswith(protected) or rel_path == protected.rstrip("/"):
                return False, f"write-protected: {protected}"

    return True, "OK"


# --- Main ---

def main():
    try:
        tool_name = os.environ.get("TOOL_NAME", "")
        raw_input = os.environ.get("TOOL_INPUT", "{}")
        tool_input = json.loads(raw_input)

        file_path = extract_path(tool_name, tool_input)
        allowed, reason = validate_path(tool_name, file_path)

        if allowed:
            log_decision(tool_name, file_path, "ALLOWED")
            sys.exit(0)
        else:
            log_decision(tool_name, file_path, "BLOCKED", reason)
            if MODE == "enforce":
                print(f"BLOCKED by tool-auth: {reason}", file=sys.stderr)
                sys.exit(2)
            else:
                log_decision(tool_name, file_path, "AUDIT-WOULD-BLOCK", reason)
                sys.exit(0)

    except json.JSONDecodeError as e:
        log_decision("FileAccess", "JSON_ERROR", "BLOCKED", str(e))
        print(f"BLOCKED by tool-auth: invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        log_decision("FileAccess", "ERROR", "BLOCKED", str(e))
        print(f"BLOCKED by tool-auth: hook error (fail-closed): {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

**Key design decisions:**
- Symlinks are resolved before any check — prevents symlink-escape attacks. [EXPLICIT]
- Project root comparison uses `startswith(root + os.sep)` to prevent prefix confusion (e.g., `/app` vs `/application`). [EXPLICIT]
- Write-protected paths are a superset of read restrictions — settings and hooks cannot be modified by the agent. [EXPLICIT]
- Blocked directories use absolute paths from home directory expansion — works across platforms. [EXPLICIT]

---

## 3. audit-log.py — PostToolUse Hook for Logging

Logs every tool invocation after execution for audit trail. Captures tool name, input summary, duration, and exit status. [EXPLICIT]

```python
#!/usr/bin/env python3
"""
PostToolUse hook: Audit logging for all tool invocations.

Logs tool name, input summary, and execution metadata to JSONL file.
This hook should never block — it always exits 0.

Install:
  cp audit-log.py .claude/hooks/
  # Add to .claude/settings.json hooks.PostToolUse (no matcher = all tools)
"""
import os
import sys
import json
import datetime
import hashlib

LOG_FILE = os.environ.get(
    "TOOL_AUTH_LOG",
    os.path.join(os.environ.get("PROJECT_ROOT", "."), ".claude", "logs", "tool-auth.jsonl")
)

MAX_INPUT_LOG = 500   # chars
MAX_OUTPUT_LOG = 200  # chars


def sanitize_for_log(text: str, max_len: int) -> str:
    """Truncate and remove newlines for safe JSONL logging."""
    if not text:
        return ""
    sanitized = text.replace("\n", " ").replace("\r", "")
    if len(sanitized) > max_len:
        return sanitized[:max_len] + "...[truncated]"
    return sanitized


def compute_input_hash(raw_input: str) -> str:
    """SHA-256 hash of full input for correlation without storing content."""
    return hashlib.sha256(raw_input.encode("utf-8")).hexdigest()[:16]


def main():
    try:
        tool_name = os.environ.get("TOOL_NAME", "unknown")
        raw_input = os.environ.get("TOOL_INPUT", "{}")
        tool_output = os.environ.get("TOOL_OUTPUT", "")

        # Parse input for summary
        try:
            tool_input = json.loads(raw_input)
        except json.JSONDecodeError:
            tool_input = {"raw": raw_input[:200]}

        # Build input summary based on tool type
        if tool_name == "Bash":
            input_summary = sanitize_for_log(tool_input.get("command", ""), MAX_INPUT_LOG)
        elif tool_name in ("Read", "Write", "Edit"):
            input_summary = sanitize_for_log(tool_input.get("file_path", ""), MAX_INPUT_LOG)
        elif tool_name in ("Glob", "Grep"):
            input_summary = sanitize_for_log(
                tool_input.get("pattern", tool_input.get("query", "")), MAX_INPUT_LOG
            )
        else:
            input_summary = sanitize_for_log(str(tool_input), MAX_INPUT_LOG)

        entry = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "event": "tool_use",
            "tool": tool_name,
            "input_summary": input_summary,
            "input_hash": compute_input_hash(raw_input),
            "output_len": len(tool_output),
            "output_preview": sanitize_for_log(tool_output, MAX_OUTPUT_LOG),
        }

        log_dir = os.path.dirname(LOG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=True) + "\n")

    except Exception:
        pass  # audit logging must never affect tool execution

    sys.exit(0)  # PostToolUse hooks should always allow


if __name__ == "__main__":
    main()
```

**Key design decisions:**
- PostToolUse hooks always exit 0 — they log, never block. [EXPLICIT]
- Input hash provides correlation capability without storing full commands in the audit log. [EXPLICIT]
- Output preview is capped at 200 chars — enough for debugging, small enough for storage. [EXPLICIT]
- Tool-specific input summarization extracts the most relevant field per tool type. [EXPLICIT]
- All exceptions are silently caught — audit logging failure must never disrupt the agent. [EXPLICIT]

---

## 4. gateway-auth.py — Gateway Message Sender Verification

Verifies that incoming messages to the OpenClaw Gateway come from authorized senders. Supports Telegram, WhatsApp, Slack, and HTTP API authentication. [EXPLICIT]

```python
#!/usr/bin/env python3
"""
Gateway authentication: verifies message sender identity.

Reads sender identity from message payload, checks against platform-specific
allowlists, enforces rate limits, and logs all decisions.

Usage:
  Called by the Gateway adapter before passing messages to the Core agent.
  python3 gateway-auth.py --platform telegram --payload '{"chat_id": 123}'

Configuration:
  Set GATEWAY_AUTH_CONFIG to path of gateway-auth.json (see template below).
"""
import os
import sys
import json
import time
import datetime
import argparse
from pathlib import Path
from collections import defaultdict

# --- Configuration ---

CONFIG_PATH = os.environ.get("GATEWAY_AUTH_CONFIG", ".claude/gateway-auth.json")
LOG_FILE = os.environ.get(
    "TOOL_AUTH_LOG",
    os.path.join(os.environ.get("PROJECT_ROOT", "."), ".claude", "logs", "tool-auth.jsonl")
)
RATE_LIMIT_FILE = os.path.join(
    os.environ.get("PROJECT_ROOT", "."), ".claude", "logs", "rate-limits.json"
)

DEFAULT_CONFIG = {
    "telegram": {
        "allowed_chat_ids": [],
        "reject_unknown": True,
        "rate_limit_per_minute": 10,
        "rate_limit_per_hour": 100,
        "max_message_length": 4096
    },
    "whatsapp": {
        "allowed_numbers": [],
        "reject_unknown": True,
        "rate_limit_per_minute": 10,
        "rate_limit_per_hour": 100,
        "max_message_length": 4096
    },
    "slack": {
        "allowed_workspaces": [],
        "allowed_users": [],
        "reject_unknown": True,
        "rate_limit_per_minute": 20,
        "rate_limit_per_hour": 200,
        "max_message_length": 8192
    },
    "http": {
        "auth_type": "bearer",
        "token_env_var": "OPENCLAW_API_TOKEN",
        "rate_limit_per_minute": 30,
        "rate_limit_per_hour": 300,
        "max_message_length": 16384
    }
}


def load_config() -> dict:
    """Load gateway auth configuration."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_CONFIG
    except json.JSONDecodeError:
        log_event("config", "ERROR", "invalid-json-config")
        return DEFAULT_CONFIG


def log_event(platform: str, decision: str, reason: str = "",
              sender: str = ""):
    """Log authentication decision."""
    try:
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        entry = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "event": "gateway_auth",
            "platform": platform,
            "sender": sender[:100],
            "decision": decision,
            "reason": reason,
        }
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=True) + "\n")
    except Exception:
        pass


# --- Rate Limiting ---

def load_rate_state() -> dict:
    try:
        with open(RATE_LIMIT_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_rate_state(state: dict):
    try:
        os.makedirs(os.path.dirname(RATE_LIMIT_FILE), exist_ok=True)
        with open(RATE_LIMIT_FILE, "w") as f:
            json.dump(state, f)
    except Exception:
        pass


def check_rate_limit(sender_key: str, per_minute: int, per_hour: int) -> tuple:
    """Check if sender exceeds rate limits. Returns (allowed, reason)."""
    now = time.time()
    state = load_rate_state()

    if sender_key not in state:
        state[sender_key] = {"timestamps": []}

    timestamps = state[sender_key]["timestamps"]
    # Clean old entries (older than 1 hour)
    timestamps = [t for t in timestamps if now - t < 3600]
    timestamps.append(now)
    state[sender_key]["timestamps"] = timestamps
    save_rate_state(state)

    # Check per-minute
    last_minute = [t for t in timestamps if now - t < 60]
    if len(last_minute) > per_minute:
        return False, f"rate-limit-minute: {len(last_minute)}/{per_minute}"

    # Check per-hour
    if len(timestamps) > per_hour:
        return False, f"rate-limit-hour: {len(timestamps)}/{per_hour}"

    return True, "OK"


# --- Platform Auth ---

def auth_telegram(payload: dict, config: dict) -> tuple:
    """Authenticate Telegram message. Returns (allowed, reason, sender_id)."""
    chat_id = payload.get("chat_id") or payload.get("message", {}).get("chat", {}).get("id")
    if chat_id is None:
        return False, "missing-chat-id", "unknown"

    sender_key = f"telegram:{chat_id}"
    allowed_ids = config.get("allowed_chat_ids", [])

    if chat_id in allowed_ids:
        return True, "authorized-chat-id", sender_key
    elif config.get("reject_unknown", True):
        return False, "unknown-chat-id", sender_key
    else:
        return True, "unverified-allowed", sender_key


def auth_whatsapp(payload: dict, config: dict) -> tuple:
    """Authenticate WhatsApp message."""
    phone = payload.get("from") or payload.get("sender_number", "")
    if not phone:
        return False, "missing-phone-number", "unknown"

    sender_key = f"whatsapp:{phone}"
    allowed = config.get("allowed_numbers", [])

    if phone in allowed:
        return True, "authorized-number", sender_key
    elif config.get("reject_unknown", True):
        return False, "unknown-number", sender_key
    else:
        return True, "unverified-allowed", sender_key


def auth_slack(payload: dict, config: dict) -> tuple:
    """Authenticate Slack message."""
    workspace = payload.get("team_id", "")
    user = payload.get("user_id", "") or payload.get("event", {}).get("user", "")
    sender_key = f"slack:{workspace}:{user}"

    if not workspace:
        return False, "missing-workspace-id", sender_key

    allowed_workspaces = config.get("allowed_workspaces", [])
    allowed_users = config.get("allowed_users", [])

    if workspace not in allowed_workspaces:
        return False, "unknown-workspace", sender_key
    if allowed_users and user not in allowed_users:
        return False, "unknown-user", sender_key

    return True, "authorized-workspace-user", sender_key


def auth_http(payload: dict, config: dict) -> tuple:
    """Authenticate HTTP API request via bearer token."""
    token = payload.get("authorization", "").replace("Bearer ", "")
    sender_key = f"http:{token[:8]}..." if token else "http:no-token"

    token_env = config.get("token_env_var", "OPENCLAW_API_TOKEN")
    expected = os.environ.get(token_env, "")

    if not expected:
        return False, "no-expected-token-configured", sender_key
    if not token:
        return False, "missing-auth-token", sender_key
    if token == expected:
        return True, "valid-token", sender_key
    else:
        return False, "invalid-token", sender_key


PLATFORM_AUTH = {
    "telegram": auth_telegram,
    "whatsapp": auth_whatsapp,
    "slack": auth_slack,
    "http": auth_http,
}


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Gateway auth for OpenClaw")
    parser.add_argument("--platform", required=True,
                        choices=["telegram", "whatsapp", "slack", "http"])
    parser.add_argument("--payload", required=True, help="JSON message payload")
    parser.add_argument("--add-sender", help="Add sender to allowlist (e.g., telegram:123)")
    args = parser.parse_args()

    config = load_config()
    platform_config = config.get(args.platform, DEFAULT_CONFIG.get(args.platform, {}))

    # Handle --add-sender mode
    if args.add_sender:
        parts = args.add_sender.split(":", 1)
        if len(parts) == 2:
            plat, sender_id = parts
            if plat == "telegram":
                config.setdefault("telegram", {}).setdefault("allowed_chat_ids", [])
                try:
                    sid = int(sender_id)
                except ValueError:
                    sid = sender_id
                if sid not in config["telegram"]["allowed_chat_ids"]:
                    config["telegram"]["allowed_chat_ids"].append(sid)
            elif plat == "whatsapp":
                config.setdefault("whatsapp", {}).setdefault("allowed_numbers", [])
                if sender_id not in config["whatsapp"]["allowed_numbers"]:
                    config["whatsapp"]["allowed_numbers"].append(sender_id)
            elif plat == "slack":
                config.setdefault("slack", {}).setdefault("allowed_users", [])
                if sender_id not in config["slack"]["allowed_users"]:
                    config["slack"]["allowed_users"].append(sender_id)

            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=2)
            print(f"Added {args.add_sender} to allowlist")
            sys.exit(0)
        else:
            print("Format: --add-sender platform:id", file=sys.stderr)
            sys.exit(1)

    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError as e:
        log_event(args.platform, "BLOCKED", f"invalid-payload-json: {e}")
        print(f"REJECTED: invalid JSON payload", file=sys.stderr)
        sys.exit(2)

    # Check message length
    msg_content = payload.get("text", payload.get("message", ""))
    if isinstance(msg_content, dict):
        msg_content = json.dumps(msg_content)
    max_len = platform_config.get("max_message_length", 4096)
    if len(str(msg_content)) > max_len:
        log_event(args.platform, "BLOCKED", "message-too-long")
        print(f"REJECTED: message exceeds {max_len} chars", file=sys.stderr)
        sys.exit(2)

    # Authenticate sender
    auth_fn = PLATFORM_AUTH.get(args.platform)
    if not auth_fn:
        log_event(args.platform, "BLOCKED", "unsupported-platform")
        sys.exit(2)

    allowed, reason, sender_key = auth_fn(payload, platform_config)

    if not allowed:
        log_event(args.platform, "BLOCKED", reason, sender_key)
        print(f"REJECTED: {reason}", file=sys.stderr)
        sys.exit(2)

    # Check rate limits
    rpm = platform_config.get("rate_limit_per_minute", 10)
    rph = platform_config.get("rate_limit_per_hour", 100)
    rate_ok, rate_reason = check_rate_limit(sender_key, rpm, rph)

    if not rate_ok:
        log_event(args.platform, "RATE_LIMITED", rate_reason, sender_key)
        print(f"REJECTED: {rate_reason}", file=sys.stderr)
        sys.exit(2)

    # Authorized
    log_event(args.platform, "ALLOWED", reason, sender_key)
    print(json.dumps({"status": "authorized", "sender": sender_key}))
    sys.exit(0)


if __name__ == "__main__":
    main()
```

**Key design decisions:**
- Platform-specific auth functions extract the correct identity field per platform. [EXPLICIT]
- Rate limiting uses a simple file-based approach suitable for personal deployments. [EXPLICIT]
- `--add-sender` mode provides a CLI to manage allowlists without editing JSON manually. [EXPLICIT]
- Message length checks prevent oversized payloads before they reach the agent. [EXPLICIT]
- HTTP auth uses bearer tokens stored in environment variables, never hardcoded. [EXPLICIT]

---

## Installation Summary

```bash
# 1. Copy scripts
mkdir -p .claude/hooks .claude/logs
cp validate-bash.py .claude/hooks/
cp validate-file-access.py .claude/hooks/
cp audit-log.py .claude/hooks/

# 2. Set environment
export PROJECT_ROOT="$(pwd)"
export TOOL_AUTH_MODE="enforce"

# 3. Register in .claude/settings.json
# (see SKILL.md S1 for the hooks configuration)

# 4. Test hooks manually
TOOL_NAME=Bash TOOL_INPUT='{"command":"ls -la"}' python3 .claude/hooks/validate-bash.py
echo "Exit code: $?"

TOOL_NAME=Bash TOOL_INPUT='{"command":"rm -rf /"}' python3 .claude/hooks/validate-bash.py
echo "Exit code: $?"

# 5. Configure gateway auth
cp gateway-auth.json.template .claude/gateway-auth.json
# Edit with your platform IDs
```
