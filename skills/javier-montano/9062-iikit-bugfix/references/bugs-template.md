# Bug Reports: <feature-name>

## BUG-NNN

**Reported**: YYYY-MM-DD
**Severity**: critical | high | medium | low
**Status**: reported
**GitHub Issue**: #number or _(none)_

**Description**: One-line bug summary

**Reproduction Steps**:
1. Step one
2. Step two
3. Observe the issue

**Root Cause**: _(empty until investigation)_

**Fix Reference**: _(empty until implementation)_

---

## Field Definitions

| Field | Purpose | Required |
|-------|---------|----------|
| BUG-NNN | Unique sequential identifier per feature | Yes [EXPLICIT] |
| Reported | Date bug was first observed (ISO 8601) | Yes [EXPLICIT] |
| Severity | Impact classification: critical (system down), high (major feature broken), medium (workaround exists), low (cosmetic) | Yes [EXPLICIT] |
| Status | Lifecycle state: reported → investigating → fixing → verified → closed | Yes [EXPLICIT] |
| GitHub Issue | Cross-reference to issue tracker for traceability | When available [EXPLICIT] |
| Description | Single sentence summarizing the observable defect behavior | Yes [EXPLICIT] |
| Reproduction Steps | Minimal deterministic steps to reproduce the bug | Yes [EXPLICIT] |
| Root Cause | Technical explanation of why the bug occurs (filled during investigation) | After triage [EXPLICIT] |
| Fix Reference | Link to commit, PR, or branch containing the fix | After implementation [EXPLICIT] |
