# Docker Security Patterns for OpenClaw Isolation

Reference material for `5023-openclaw-isolation`. Covers Dockerfile hardening, Docker Compose security options, network driver configurations, volume mount patterns, seccomp profiles, and AppArmor integration. [EXPLICIT]

---

## 1. Dockerfile Hardening Patterns

### 1.1 Multi-Stage Build Pattern

Multi-stage builds separate the build environment from the runtime environment. The builder stage installs compilers, dev dependencies, and source code. The runtime stage copies only compiled artifacts. This eliminates build tools from the final image, reducing attack surface by 60-80% compared to single-stage builds. [EXPLICIT]

```dockerfile
# Builder: full toolchain
FROM node:22-alpine AS builder
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY . .
RUN npm run build && npm prune --production

# Runtime: minimal
FROM node:22-alpine AS runtime
WORKDIR /app
COPY --from=builder /build/dist ./dist
COPY --from=builder /build/node_modules ./node_modules
```

**Key rules:**
- Never install dev dependencies in the runtime stage [EXPLICIT]
- Use `npm ci` (not `npm install`) for deterministic builds [EXPLICIT]
- Run `npm prune --production` before copying to runtime [EXPLICIT]
- Use `.dockerignore` to exclude `.git/`, `node_modules/`, `.env`, test files [EXPLICIT]

### 1.2 Base Image Selection

| Base Image | Size | Packages | Use Case | Security Rating |
|------------|------|----------|----------|-----------------|
| `alpine:3.20` | ~7MB | musl libc, busybox | Minimal containers | Highest [EXPLICIT] |
| `node:22-alpine` | ~130MB | Node.js + alpine | Node.js agents | High [EXPLICIT] |
| `debian:bookworm-slim` | ~80MB | glibc, apt-minimal | glibc-dependent apps | Medium [EXPLICIT] |
| `node:22` | ~900MB | Full Debian + Node | Development only | Low [EXPLICIT] |
| `ubuntu:24.04` | ~78MB | systemd, apt | Legacy compatibility | Medium [INFERRED] |

**Rules:**
- Always pin by digest: `node:22-alpine@sha256:abc123...` [EXPLICIT]
- Never use `:latest` tag — it changes unpredictably [EXPLICIT]
- Scan base images with `docker scout cves` or `trivy image` before use [EXPLICIT]
- Update base image monthly to get security patches [INFERRED]

### 1.3 Non-Root User Pattern

Running containers as root means a container escape gives root on the host (if user namespaces are not configured). Always create and switch to a dedicated user. [EXPLICIT]

```dockerfile
# Create user with explicit UID/GID
RUN addgroup -g 1001 openclaw \
    && adduser -u 1001 -G openclaw -s /bin/false -D openclaw

# Set ownership on app directory
COPY --chown=openclaw:openclaw . /app

# Switch to non-root before CMD
USER openclaw
```

**Rules:**
- Use UID >= 1000 to avoid collision with system users [EXPLICIT]
- Set shell to `/bin/false` or `/sbin/nologin` to prevent interactive login [EXPLICIT]
- Ensure all application files are owned by the non-root user [EXPLICIT]
- `USER` directive must appear before `CMD`/`ENTRYPOINT` [EXPLICIT]

### 1.4 Secret Exclusion Pattern

Docker image layers are append-only and inspectable. Any secret placed in a layer persists even if deleted in a later layer. [EXPLICIT]

**Forbidden patterns:**
```dockerfile
# NEVER DO THIS
COPY .env /app/.env
ARG API_KEY=sk-ant-xxxx
ENV SECRET_KEY=my-secret
RUN curl -H "Authorization: Bearer $SECRET" https://api.example.com
```

**Correct patterns:**
- Mount secrets at runtime via `docker run --env-file .env` [EXPLICIT]
- Use Docker secrets (`docker secret create`) for Swarm deployments [EXPLICIT]
- Use BuildKit secrets for build-time secrets: `RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci` [EXPLICIT]

---

## 2. Docker Compose Security Options

### 2.1 security_opt

| Option | Effect | Recommendation |
|--------|--------|----------------|
| `no-new-privileges:true` | Prevents privilege escalation via setuid/setgid | Always enable [EXPLICIT] |
| `seccomp:custom.json` | Custom seccomp profile restricting syscalls | Use for high-security deployments [EXPLICIT] |
| `apparmor:openclaw-profile` | Custom AppArmor profile | Use on Ubuntu/Debian hosts [EXPLICIT] |

### 2.2 Capability Management

Linux capabilities split root privileges into discrete units. Docker grants a default set; best practice is to drop all and add back only what is needed. [EXPLICIT]

**Default Docker capabilities (always drop):**

| Capability | What It Allows | Risk If Kept |
|------------|----------------|--------------|
| `CHOWN` | Change file ownership | Ownership manipulation |
| `DAC_OVERRIDE` | Bypass file read/write/execute checks | File access bypass |
| `FSETID` | Set file set-user-ID bits | Privilege escalation |
| `KILL` | Send signals to other processes | Process interference |
| `SETGID` | Set group ID | Group escalation |
| `SETUID` | Set user ID | User escalation |
| `SETPCAP` | Modify process capabilities | Capability escalation |
| `NET_BIND_SERVICE` | Bind to ports < 1024 | Not needed for ports >= 1024 |
| `NET_RAW` | Raw socket access | Network sniffing, spoofing |
| `SYS_CHROOT` | Use chroot | Escape chroot jails |
| `MKNOD` | Create special device files | Device access |
| `AUDIT_WRITE` | Write to kernel audit log | Audit tampering |
| `SETFCAP` | Set file capabilities | Capability injection |

[EXPLICIT]

**Compose configuration:**
```yaml
cap_drop:
  - ALL
# Only add back if genuinely needed, with documented justification:
# cap_add:
#   - NET_BIND_SERVICE  # Justification: agent serves on port 443
```

### 2.3 Resource Limits

Resource limits prevent denial-of-service conditions where a container consumes all host resources. [EXPLICIT]

```yaml
deploy:
  resources:
    limits:
      cpus: "1.0"
      memory: 1024M
      pids: 100
    reservations:
      cpus: "0.25"
      memory: 256M
```

**Alternative (compose v3 without deploy):**
```yaml
mem_limit: 1024m
mem_reservation: 256m
cpus: "1.0"
pids_limit: 100
```

**Sizing guidelines:**
- Memory: 1GB for single-agent, 2GB for agent + tools, 4GB for agent + browser automation [INFERRED]
- CPU: 1 core for single-agent, 2 cores if running builds or code analysis [INFERRED]
- PIDs: 100 for single-agent, 200 for agent spawning subprocesses [INFERRED]
- Monitor with `docker stats` for 48 hours before finalizing limits [EXPLICIT]

### 2.4 Read-Only Root Filesystem

```yaml
read_only: true
tmpfs:
  - /tmp:size=64m,noexec,nosuid,nodev
  - /app/workspace:size=256m,noexec,nosuid,nodev
  - /app/.cache:size=128m,noexec,nosuid,nodev
```

**tmpfs flags:**
- `noexec` — Prevent execution of binaries from tmpfs [EXPLICIT]
- `nosuid` — Ignore setuid/setgid bits on files in tmpfs [EXPLICIT]
- `nodev` — Disallow creation of device files in tmpfs [EXPLICIT]
- `size=NNm` — Hard size limit; writes fail when exceeded [EXPLICIT]

---

## 3. Network Driver Configurations

### 3.1 Bridge Network (Default)

The default Docker bridge network (`docker0`) allows inter-container communication and internet access. This is insufficiently isolated for agent containers. [EXPLICIT]

### 3.2 User-Defined Bridge (Recommended)

User-defined bridges provide DNS resolution between containers by name and can be marked as `internal` to block all external traffic. [EXPLICIT]

```yaml
networks:
  openclaw-internal:
    driver: bridge
    internal: true           # No external/internet access
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"  # Inter-container communication
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### 3.3 Egress Proxy Pattern

When the agent needs controlled internet access (e.g., Claude API calls), route traffic through an egress proxy that enforces domain allowlists. [EXPLICIT]

```yaml
services:
  egress-proxy:
    image: ubuntu/squid:latest
    networks:
      - openclaw-internal
      - openclaw-egress
    volumes:
      - ./squid.conf:/etc/squid/squid.conf:ro

  openclaw-agent:
    environment:
      - HTTP_PROXY=http://egress-proxy:3128
      - HTTPS_PROXY=http://egress-proxy:3128
    networks:
      - openclaw-internal  # Agent only on internal network

networks:
  openclaw-internal:
    internal: true
  openclaw-egress:
    driver: bridge
    # NOT internal — proxy needs internet access
```

**Squid allowlist template (`squid.conf`):**
```
acl allowed_domains dstdomain .anthropic.com
acl allowed_domains dstdomain .github.com
acl allowed_domains dstdomain .npmjs.org
http_access allow allowed_domains
http_access deny all
```

### 3.4 macvlan Network

Assigns a real MAC address to the container, making it appear as a physical device on the network. Useful for environments requiring layer-2 isolation. Not recommended for typical OpenClaw deployments due to complexity. [INFERRED]

---

## 4. Volume Mount Security Patterns

### 4.1 Bind Mount Rules

| Mount Target | Permission | Justification |
|-------------|------------|---------------|
| `./project:/app/project` | `:ro` | Agent reads source code, must not modify [EXPLICIT] |
| `./output:/app/output` | `:rw` | Agent produces deliverables [EXPLICIT] |
| `./config:/app/config` | `:ro` | Runtime configuration [EXPLICIT] |
| `./.env:/app/.env` | `:ro` | Environment variables (alternative to `env_file`) [EXPLICIT] |

### 4.2 Forbidden Mounts

These mounts must never appear in any OpenClaw Docker configuration. Each one represents a critical security boundary violation. [EXPLICIT]

| Mount | Risk | Severity |
|-------|------|----------|
| `/var/run/docker.sock` | Full Docker daemon control, equivalent to host root | Critical [EXPLICIT] |
| `/` or `/host` | Entire host filesystem exposed | Critical [EXPLICIT] |
| `~/.ssh/` | SSH private keys accessible to container | Critical [EXPLICIT] |
| `~/.aws/credentials` | AWS access keys exposed | Critical [EXPLICIT] |
| `~/.config/gcloud/` | GCP service account keys exposed | Critical [EXPLICIT] |
| `/etc/shadow` | Host password hashes accessible | Critical [EXPLICIT] |
| `/proc` (beyond Docker defaults) | Kernel process information leakage | High [EXPLICIT] |
| `/sys` (beyond Docker defaults) | Kernel subsystem control | High [EXPLICIT] |

### 4.3 Named Volumes vs Bind Mounts

Named volumes are managed by Docker and provide better permission handling than bind mounts. Use named volumes for persistent data that does not need direct host access. [EXPLICIT]

```yaml
volumes:
  agent-data:
    driver: local
    driver_opts:
      type: none
      device: /opt/openclaw/data
      o: bind

services:
  openclaw-agent:
    volumes:
      - agent-data:/app/data:rw
```

---

## 5. Seccomp Profiles

Seccomp (Secure Computing Mode) restricts the system calls a container can make. Docker's default seccomp profile blocks ~44 syscalls. A custom profile can restrict further. [EXPLICIT]

### 5.1 Default Docker Seccomp Profile

The default profile blocks dangerous syscalls including `reboot`, `kexec_load`, `mount`, `umount`, `ptrace`, `init_module`, and `swapon`. This is sufficient for most OpenClaw deployments. [EXPLICIT]

### 5.2 Custom Restrictive Profile

For high-security deployments, restrict to only the syscalls the agent actually needs. [EXPLICIT]

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_AARCH64"],
  "syscalls": [
    {
      "names": [
        "read", "write", "close", "fstat", "lseek", "mmap", "mprotect",
        "munmap", "brk", "ioctl", "access", "dup2", "nanosleep",
        "getpid", "socket", "connect", "sendto", "recvfrom",
        "bind", "listen", "accept", "getsockname", "getpeername",
        "clone", "execve", "wait4", "kill", "exit_group",
        "openat", "newfstatat", "getdents64", "fcntl",
        "epoll_create1", "epoll_ctl", "epoll_wait",
        "futex", "set_robust_list", "clock_gettime"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**Usage:**
```yaml
security_opt:
  - seccomp:./seccomp-openclaw.json
```

### 5.3 Generating a Custom Profile

Use `strace` or OCI runtime logging to discover which syscalls the agent uses, then build a profile that allows only those. [EXPLICIT]

```bash
# Record syscalls during normal operation
docker run --security-opt seccomp=unconfined \
  strace -ff -o /tmp/syscalls -- node dist/index.js

# Analyze unique syscalls
cat /tmp/syscalls.* | awk '{print $1}' | sort -u
```

---

## 6. AppArmor Integration

AppArmor provides mandatory access control (MAC) at the kernel level. Docker applies a default AppArmor profile (`docker-default`) that restricts mount operations, write access to `/proc` and `/sys`, and loading of kernel modules. [EXPLICIT]

### 6.1 Custom AppArmor Profile for OpenClaw

```
#include <tunables/global>

profile openclaw-agent flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  # Network access — restrict to TCP only
  network inet tcp,
  network inet6 tcp,
  deny network raw,
  deny network packet,

  # File system — read-only root with specific exceptions
  / r,
  /app/ r,
  /app/dist/** r,
  /app/node_modules/** r,
  /app/workspace/** rw,
  /tmp/** rw,

  # Deny sensitive paths
  deny /etc/shadow r,
  deny /etc/gshadow r,
  deny /root/** rwx,
  deny /home/*/.ssh/** rwx,
  deny /home/*/.aws/** rwx,
  deny /home/*/.gnupg/** rwx,

  # Deny mount and ptrace
  deny mount,
  deny ptrace,

  # Allow node execution
  /usr/local/bin/node ix,
  /app/dist/** ix,
}
```

### 6.2 Loading and Applying the Profile

```bash
# Install the profile
sudo apparmor_parser -r -W /etc/apparmor.d/openclaw-agent

# Use in Docker Compose
# security_opt:
#   - apparmor:openclaw-agent

# Verify profile is loaded
sudo aa-status | grep openclaw
```

### 6.3 AppArmor vs SELinux

| Feature | AppArmor | SELinux |
|---------|----------|---------|
| Configuration | Path-based profiles | Label-based policies |
| Default on | Ubuntu, Debian, SUSE | RHEL, Fedora, CentOS |
| Complexity | Lower | Higher |
| Granularity | File path level | Object label level |
| Docker support | Built-in | Via `--security-opt label` |

[EXPLICIT]

---

## 7. Container Scanning and Maintenance

### 7.1 Image Scanning

Scan built images for known vulnerabilities before deployment. [EXPLICIT]

```bash
# Docker Scout (built-in)
docker scout cves openclaw-agent:latest

# Trivy (open source)
trivy image openclaw-agent:latest

# Grype (open source)
grype openclaw-agent:latest
```

### 7.2 Runtime Monitoring

Monitor container behavior for anomalies. [INFERRED]

```bash
# Resource usage
docker stats openclaw-agent

# Process list inside container
docker top openclaw-agent

# File system changes (should be empty with read-only root)
docker diff openclaw-agent

# Logs
docker logs --tail 100 -f openclaw-agent
```

### 7.3 Periodic Maintenance Checklist

- [ ] Update base image monthly for security patches [EXPLICIT]
- [ ] Re-scan images after every rebuild [EXPLICIT]
- [ ] Review egress allowlist quarterly [INFERRED]
- [ ] Rotate secrets (API keys, tokens) per organization policy [EXPLICIT]
- [ ] Audit container logs for anomalous behavior weekly [INFERRED]
- [ ] Verify resource limits match actual usage via `docker stats` [EXPLICIT]
