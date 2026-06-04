# Canonical Normalized Finding Schema

**Version:** 1.0 — established with DEC-035 + DEC-036 (stakes-class escalation amendment)

This is the single shared finding schema that every reviewer (code-review, AVFL, qa-reviewer) and the fixer speak. Reviewers normalize their raw output into this shape before the fixer sees it. The fixer reads only this shape. The report and the end-gate render only this shape. No finding travels the conduct directed-fix chain in any other format.

---

## Base Fields

Every finding carries all of the following fields.

| Field | Type | Meaning |
|---|---|---|
| `story_slug` | string | The slug of the story the finding is against. Ties the finding to a specific unit of work. |
| `source` | string | Which reviewer produced the finding — e.g. `bmad-code-review`, `avfl`, `qa-reviewer`, `architecture-guard`, `e2e-validator`, `simplify`. Open string; listed values are non-exhaustive examples. |
| `verdict` | string | The reviewer's raw verdict on this issue — e.g. `PASS`, `FAIL`, `BLOCKED`. Distinct from `disposition` (disposition is what happens to the finding; verdict is what the reviewer assessed). Open string; listed values are non-exhaustive examples. |
| `severity` | string | The reviewer's severity assessment — e.g. `blocker`, `critical`, `major`, `minor`, `low`. Orthogonal to `stakes_class` — see below. Open string; listed values are non-exhaustive examples. |
| `type` | string | Category of issue — e.g. `correctness`, `security`, `spec-compliance`, `style`, `test-coverage`. |
| `location` | string | Where in the artifact the issue appears — file path, line range, function name, or step reference. |
| `summary` | string | One-sentence plain-English description of the problem. Used in collapsed views and report headers. |
| `detail` | string | Full explanation: what is wrong, why it matters, and what the expected state is. |
| `evidence` | string | The concrete artifact excerpt (code snippet, spec quote, test output) that substantiates the finding. |
| `ac_id` | string or null | Acceptance criterion identifier this finding maps to, if any. Null when the finding is not tied to a specific AC. |
| `legitimate` | boolean | Whether the reviewer judges the finding to be a genuine issue (true) or a false positive (false). Drives the auto-fix invariant — see Disposition Rules below. |
| `suggested_fix` | string or null | The reviewer's proposed remediation, if one is available. The fixer uses this as a starting point; null when the reviewer offers none. |

---

## Stakes Class

```
stakes_class: security-auth-isolation | irreversible-destructive | high-blast-radius-architecture | routine
```

**Default:** `routine`

`stakes_class` is **orthogonal to `severity`**. A finding has both independently. A finding may be low-severity yet stakes-class (e.g., a small insecure default in an auth path), or high-severity yet routine (e.g., a major logic bug in a UI component with no blast radius beyond that component). Severity measures the magnitude of the problem in isolation; stakes class measures the consequences of mis-handling it.

Reviewers assign `stakes_class` alongside `severity`. When a finding does not meet any of the three stakes criteria below, `stakes_class` is `routine`.

### Defined Stakes Classes

**`security-auth-isolation`**
Security, authentication, or isolation findings. Covers XSS, injection, privilege escalation, auth bypass, leaked credentials, inadequate sandboxing, and any finding where a mistake opens an exploit path or breaks a trust boundary.

**`irreversible-destructive`**
Actions that cannot be undone or that destroy data/state with no safe rollback. Concrete examples: schema migrations, data deletes, force-pushes, production deploys, destructive file operations, and any change whose failure mode involves permanent loss.

**`high-blast-radius-architecture`**
Changes with wide downstream effect — architectural decisions, cross-cutting concerns, shared interfaces, or design patterns that, if wrong, cascade across many consumers or require large-scale rework to correct.

**`routine`**
Any finding that does not meet the criteria of the three stakes classes above. This is the common case. Routine findings follow the always-auto-fixed path (see Disposition Rules).

---

## Disposition

```
disposition: fixed | dismissed | triaged-out | escalated
```

The disposition records what happened to the finding after the fixer processed it.

| Value | Meaning |
|---|---|
| `fixed` | The fixer applied a fix. The finding is resolved. |
| `dismissed` | The fixer judged the finding not worth acting on. **Requires a non-empty rationale** — see Required-Rationale Rule below. |
| `triaged-out` | The finding is valid but out of scope for this story (e.g., belongs to a different component, tracked separately). Triaged-out findings appear in the report's out-of-scope section; they are not silently dropped. |
| `escalated` | The finding was raised for human attention rather than quietly resolved by the auto-fix path. This is the disposition for stakes-class legitimate findings. The finding travels to the end-gate (or, under the narrow mid-flight bar, to an immediate escalation point) as a decision card. |

### No Deferred Disposition

`deferred` is not a valid disposition value. Findings are never parked in a deferred state. Every finding that enters the fixer receives one of the four dispositions above before the fix loop exits. A finding that cannot be fixed, dismissed, or triaged-out is escalated.

---

## Required-Rationale Rule

When `disposition` is `dismissed`, the finding **must** carry a non-empty `dismissal_rationale` string. A dismissal with a missing or empty rationale is invalid by schema and must be treated as a schema violation. The legible auto-fix record (per DEC-035 D5) is only as good as its dismissal explanations — empty wave-offs defeat its purpose.

```
dismissal_rationale: string   # required when disposition == "dismissed"; non-empty
```

---

## Disposition Rules — The Relaxed Auto-Fix Invariant

The fixer applies the following rules when processing a finding. These rules encode the DEC-036 amendment to DEC-035's binding decision #1.

**Rule 1 — Routine legitimate findings are always auto-fixed.**

When `legitimate` is `true` and `stakes_class` is `routine`, the fixer applies a fix and sets `disposition` to `fixed`. No human prompt; no escalation. This is the common-case path and preserves the anti-firehose intent: the vast majority of findings are handled autonomously without interrupting the human.

**Rule 2 — Stakes-class legitimate findings are escalated, not silently auto-fixed.**

When `legitimate` is `true` and `stakes_class` is one of `security-auth-isolation`, `irreversible-destructive`, or `high-blast-radius-architecture`, the fixer sets `disposition` to `escalated`. The finding is raised for human attention rather than quietly resolved. The timing tier (see below) determines whether escalation is immediate (mid-flight) or deferred to the end-gate.

This rule is the relaxation of DEC-035's absolutism ("legitimate issues are *always* fixed automatically"). The relaxation is narrow: only stakes-class findings leave the silent auto-fix path. Routine findings remain always auto-fixed.

**Rule 3 — Non-legitimate findings are dismissed.**

When `legitimate` is `false`, the fixer sets `disposition` to `dismissed` with a non-empty rationale. Non-legitimate findings are never fixed, triaged-out, or escalated.

**Rule 4 — Legitimate but out-of-scope findings are triaged-out.**

When `legitimate` is `true` but the finding is out of scope for this story (e.g., it belongs to a different component or requires work tracked separately), the fixer sets `disposition` to `triaged-out` and spins a backlog stub via momentum:triage. Triaged-out findings appear in the report's out-of-scope section; they are not silently dropped.

### Severity and Stakes Class Are Independent Axes

Severity and stakes class are assessed independently. The disposition rules reference `stakes_class`, not `severity`, as the escalation trigger. A critical-severity routine finding is still auto-fixed (Rule 1). A minor-severity security finding is still escalated (Rule 2). Both axes appear in the report and in the end-gate decision cards so the human has full context.

---

## Timing Tier

```
timing_tier: end-gate-expanded | mid-flight
```

**Default:** `end-gate-expanded`

The timing tier applies to `escalated` findings. It marks when the escalation is surfaced to the human.

| Value | Meaning |
|---|---|
| `end-gate-expanded` | The finding is held until the end-gate, where it appears as a decision card alongside the full conduct report. This is the default tier and the safety net — all escalated findings belong here unless they meet the narrow mid-flight bar. |
| `mid-flight` | The finding triggers an immediate escalation before the fix loop continues. This is reserved for findings that meet the high bar below. |

### The Narrow Mid-Flight Bar

The `mid-flight` tier applies **only** to escalated findings that meet **at least one** of the following conditions:

1. **Irreversible-and-imminent** — the finding describes an action that is both irreversible (cannot be undone) and about to be executed as part of the current build step. Continuing would make recovery impossible.
2. **Build-invalidating** — the finding reveals that the build as currently structured cannot produce a valid artifact and continuing would compound the invalid state (e.g., a foundational spec contradiction that makes all downstream stories invalid).

This bar is **intentionally narrow** and **must not be widened**. Urgency alone is not sufficient. Stakes class alone is not sufficient. The combination of irreversibility-or-build-invalidity with imminence is what triggers mid-flight. All other escalated findings — including all security, architecture, and destructive-action findings that do not meet this bar — belong to the default `end-gate-expanded` tier.

The end-gate-expanded tier is the safety net. When in doubt, the finding belongs there.

---

## Full Finding Shape (Reference)

```yaml
# Required base fields
story_slug: string
source: string                        # bmad-code-review | avfl | qa-reviewer | architecture-guard | e2e-validator | simplify | ... (open string)
verdict: string                       # PASS | FAIL | BLOCKED | ... (open string; reviewer's raw verdict)
severity: string                      # blocker | critical | major | minor | low | ... (open string)
stakes_class: security-auth-isolation | irreversible-destructive | high-blast-radius-architecture | routine
type: string                          # correctness | security | spec-compliance | style | test-coverage | ...
location: string
summary: string                       # one sentence
detail: string                        # full explanation
evidence: string                      # artifact excerpt
ac_id: string | null
legitimate: boolean
suggested_fix: string | null

# Fixer-assigned fields (set during fix loop, not by reviewer)
disposition: fixed | dismissed | triaged-out | escalated
dismissal_rationale: string           # required and non-empty when disposition == "dismissed"
timing_tier: end-gate-expanded | mid-flight   # set when disposition == "escalated"; defaults to end-gate-expanded
```

---

## Source Decisions

- **DEC-035** — Adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop showing what it changed AND what it dismissed.
- **DEC-036** — Amends DEC-035 binding decision #1 narrowly: stakes-and-timing escalation policy; stakes-class findings leave the silent auto-fix path; report renders dismissals; anti-rubber-stamp end-gate; routine findings stay always auto-fixed; anti-firehose intent preserved. The mid-flight bar stays narrow by design.
