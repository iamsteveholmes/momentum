---
title: Verification Standard
applies_to: All Momentum stories
status: Active
cascade: global → project → path-scoped
source_decisions: DEC-029 D1, D3, D6, D7; DEC-040 D7 (amends DEC-029 D7 — re-keys §1 to assembled surface, demotes change_type to inference, adds §5 reachability DoD)
---

# Verification Standard

This rule is authoritative and self-sufficient. Agents loading only this file have
complete enforcement guidance — no other document is required to apply it.

---

## 1. Method Routing Table

Every story's verification method is keyed on its **assembled surface** — where a user
actually meets the behavior in the running, assembled product. The validator reads this
table and applies the mapped method for the story's declared (or inferred) surface.

**What "assembled surface" means:** the assembled surface is the point where an ordinary
user, who has read no code, meets the behavior in the running product. It is a property
of the *product*, not of the *diff*. A story's `change_type` describes which files an
implementation touched; it says nothing about how a human actually exercises the
resulting capability.

**Governing example:** a conversational behavior that a user meets by typing into a chat
UI is verified by driving the chat UI — even when every line of its diff touched only
backend files. Routing that story to `curl` because its diff happened to be backend-only
is the exact defect this table exists to prevent.

| Assembled Surface | Required Verification Method |
|---|---|
| `chat-ui` | `smoke` |
| `application-ui` | `smoke` |
| `http-endpoint` | `curl` |
| `cli` | `bash` |
| `skill-invocation` | `skill-invoke` |
| `hook-trigger` | `behavioral-trigger` |
| `artifact` | `document-review` |

The method values above are the closed enum that equals the `driver_bindings` keys in
`momentum/verification-harness.json`. Use these exact tokens (hyphenated, lowercase, no spaces)
in `harness_profile` fields and routing decisions — never free-text descriptions. No new
method token is introduced by this table and none is removed or renamed.

**Method token meanings:**
- `skill-invoke` — invoke the skill or agent directly; observe routing, response, and halt behavior
- `behavioral-trigger` — create the trigger condition; observe that expected behavior fires
- `bash` — run the script or CLI command with representative inputs; observe output matches spec
- `curl` — exercise the endpoint via HTTP; observe that response matches spec
- `smoke` — automated build + launch + drive via Maestro or Playwright; human residual review for visible correctness
- `document-review` — confirm the artifact satisfies all ACs by inspection and cross-reference (no automated driver)

**`curl` applies only when the HTTP endpoint is itself the surface its consumer meets** — a
public API a client calls directly. It is never the default for backend work whose
behavior is actually exercised through an application or chat surface; that work routes
to `smoke` via `application-ui` or `chat-ui` above. There is no unconditional
`backend → curl` mapping anywhere in this standard, its Python mirror, its agent copies,
or its harness config — see the inference table below for how a surface-less
`backend`-typed story now resolves.

### `change_type` — inference fallback, not the routing key

`change_type` supplies a **starting guess** at the surface, consulted **only** when a
story declares no `surface`. A declared surface always wins over this inference — the
inference can never override a declared surface, and a reader of this section alone can
tell which field is the routing key (`surface`) and which is the fallback (`change_type`).

| `change_type` | Inferred Surface |
|---|---|
| `skill-instruction` | `skill-invocation` |
| `agent-definition` | `skill-invocation` |
| `rule-hook` | `hook-trigger` |
| `script-code` | `cli` |
| `script-cli` | `cli` |
| `backend` | `application-ui` |
| `app-ui` | `application-ui` |
| `research-spike` | `artifact` |
| `specification` | `artifact` |
| `config-structure` | `artifact` |

Note that `backend` infers to `application-ui` (→ `smoke`), not `http-endpoint` (→
`curl`). A backend-only diff whose actual consumer is a raw HTTP client (no UI in front
of it) must declare `surface: http-endpoint` explicitly (or use the §2 override) to route
to `curl` — the inference no longer assumes it by default. This is the mechanism that
eliminates the unconditional `backend → curl` misroute.

A story with multiple `change_type` values first resolves to a single type via the
existing precedence order (`CHANGE_TYPE_PRECEDENCE` in `momentum-tools.py`, highest-weight
type wins), then that type's inferred surface applies. A story with no declared surface
and no recognized `change_type` resolves to `artifact` → `document-review` (the safe
default that never fabricates unearned confidence about running behavior).

**Visibility — never silent:** every story's governing surface is recorded, not implied.
A declared `surface` lives on the story's frontmatter and its `stories/index.json` entry
— it routes directly, without consulting `change_type`. An inferred surface (no `surface`
declared) is written into the frozen contract's Part-A header `surface:` field at
contract-authoring time (see `contract-format-guide.md`), so a reader can always see,
after the fact, which surface a story was actually verified against.

Stories with multiple `change_type` values apply the precedence-resolved type's method to
the task(s) of that type, per the table above.

---

## 2. Method Override

A story's required verification method — mapped from its assembled surface above, or
from the `change_type` inference fallback when no surface is declared — may be
substituted **only** through this single declared exception mechanism. There is no
second, differently-worded override path anywhere in this standard.

The exception is valid only when the story's frozen contract names **all three**:

1. **Surface** — the surface (declared or inferred) whose required method is being
   overridden.
2. **Reason** — why that method cannot be applied to this story (e.g., the surface
   cannot be driven in the available environment, or the required method is inapplicable
   to this story's actual behavior).
3. **Substitute method** — the method token, drawn from the closed six-token enum, applied
   instead.

**Authorship constraint:** the exception is authored by the story's creator or the
product owner, at plan time, **never by the validator**. The validator reads the
exception; it cannot write, infer, or backfill one.

**Invalid declaration:** an exception missing any of the three fields is invalid. When no
valid exception exists, the surface's (or inference's) required method applies and
cannot be substituted.

**Visibility:** the exception is recorded in the story's frozen contract alongside the
`surface` Part-A header field (§1), so a reader can see both which surface governs and,
when overridden, why.

---

## 3. Harness Profile Requirement

Every verified change **must** declare a harness-profile reference before verification
begins. The harness-profile reference names the entry in `momentum/verification-harness.json` that
governs:

- Execution environment (runtime, OS, tool versions)
- Driver binding (which verification driver executes the method)
- Readiness probes (how to confirm the environment is ready before verification runs)

**Non-compliance condition:** A verification that proceeds without a declared
harness-profile is non-compliant. The validator must reject it and request a
harness-profile declaration before continuing.

The harness-profile reference is declared in the story file or in the frozen contract.
It is a name (string key) — `momentum/verification-harness.json` defines the schema and defaults.

---

## 4. Adversarial Anti-Insider-Knowledge Guard

Any frozen contract whose verification steps require insider or application knowledge
is **rejected** at contract-authoring time and at validation time.

**Insider knowledge** is any fact not available to an ordinary user of the system:

- Implementation details not stated in the story spec
- Source code internals (variable names, function names, file paths internal to the
  implementation)
- Test fixture values or internal test setup
- Internal API names not part of the public interface
- Any fact about *how* the code is structured rather than *what it does*

**Ordinary-user knowledge** (permitted) is:

- What the skill/agent does (its stated purpose)
- What inputs it accepts (per its spec or UI)
- What observable outputs it produces
- What the story's Acceptance Criteria state
- What a user sees when they invoke the skill/agent normally

**Enforcement:** The validator applies this guard to every contract step. If a step
cannot be executed using only ordinary-user knowledge, the step is flagged and the
contract is returned for revision. Validation does not proceed on a flagged contract.

Surface-based routing (§1) strengthens this guard by construction: driving a behavior
through the surface an ordinary user actually meets it at can never require insider
knowledge — the surface itself is the definition of ordinary-user reach.

---

## 5. Definition of Done — Reachability

Every story, regardless of `change_type` or assembled surface, carries one universal
Definition-of-Done item:

**The capability is reachable from the application's entry point by a user who has read
no code.**

This is stated once, here, as a universal requirement. It is never repeated per change
type or per surface, and no per-type checklist may substitute a narrower or missing
version of it. A story cannot be marked done while the capability it claims to deliver is
unreachable by an end user — a no-op settings control, an unused enum value with no
caller, and an API with zero callers all fail this item regardless of how many other
checks pass.

---

## 6. Cascade Order

This rule cascades in the following order:

```
global:  ~/.claude/rules/verification-standard.md
project: .claude/rules/verification-standard.md
path:    .claude/rules/<path-scoped>/verification-standard.md
```

**What can be overridden at lower scope:**

- Harness-profile reference (Section 3) — project and path scopes may specify a
  different default harness profile for their context.
- Method override justification (Section 2) — project scope may declare standing
  justifications for recurring override patterns.

**What cannot be overridden at any lower scope:**

- The routing table (Section 1) — global only. Project and path scopes may not
  replace, remove, or redefine the surface-to-method mapping or the change_type
  inference table.
- The reachability Definition of Done item (Section 5) — global only. It applies to
  every story; no project or path scope may remove, narrow, or waive it.
- The adversarial anti-insider-knowledge guard (Section 4) — global only. The guard
  applies uniformly; no project or path exception is valid.

Lower scopes that attempt to override non-overridable sections are ignored.
The global rule takes precedence.
