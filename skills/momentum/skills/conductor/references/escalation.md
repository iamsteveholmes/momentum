# Conductor Escalation Engine — Stakes-and-Timing Mid-Flight Escalation

**Reference for:** `skills/momentum/skills/conductor/workflow.md` step 2.F  
**Invoked by:** Build-phase frontier (step 2.2) and merge/conflict-resolution leg (step 2.2.M)  
**Governing decisions:** DEC-035 D1 (one end-gate; anti-firehose), DEC-036 D1 (two-tier timing model), D2 (stakes classes), D5 (self-sufficiency floor), Decision Gate (anti-firehose — never widen the bar)

---

## Purpose

This engine is the **single shared detection-and-pause primitive** for mid-flight escalation during a Conductor build run. It owns:
1. Reading the stakes finding-class and timing tier off a per-story pipeline or validation result
2. Evaluating the narrow, high-bar timing condition for mid-flight escalation
3. Raising exactly one developer-facing pause-ask when the bar is met
4. Resolving the developer's answer into one of three outcomes and resuming the build

Both the **build-phase frontier leg** (`conduct-build-phase-frontier`, step 2.2) and the **merge/conflict-resolution leg** (`conduct-merge-and-conflict-resolution`, step 2.2.M) route all mid-flight escalation decisions through this engine. Neither leg independently decides the bar or owns its own pause primitive. Detection-of-the-bar and the pause primitive live here once.

---

## Inputs

The engine receives a findings array from a per-story pipeline or validation result. Each finding carries:

| Field | Values | Source |
|---|---|---|
| `stakes_class` | `routine` \| `security-auth-isolation` \| `irreversible-destructive` \| `high-blast-radius-architecture` | Defined by the canonical finding schema (`skills/momentum/references/finding-schema.md`, authored by the directed-fix-finding-schema story) — the engine consumes this field, it does not define it |
| `timing_tier` | `end-gate-expanded` \| `mid-flight` | Defined by the canonical finding schema (`skills/momentum/references/finding-schema.md`) — `mid-flight` means the finding is irreversible-and-imminent or build-invalidating (encoded in the value's semantics per schema ACs 9–10); the engine consumes this field, it does not define it |
| `summary` | String | Human-readable description of the finding |
| `evidence` | String | Supporting evidence inline |
| `suggested_fix` | String | Recommended resolution |

---

## Bar Evaluation Rule — The Narrow Mid-Flight Condition

**The engine fires a mid-flight pause ONLY when a finding meets both of these conditions:**

1. `stakes_class` is one of: `security-auth-isolation`, `irreversible-destructive`, `high-blast-radius-architecture`  
   (i.e., NOT `routine`)
2. `timing_tier == mid-flight`  
   (The `mid-flight` value already encodes that the finding is irreversible-and-imminent or build-invalidating — this is the semantic definition of `mid-flight` per the canonical finding schema (`skills/momentum/references/finding-schema.md`). No separate reason field is required.)

**Everything else stays on the autonomous path — no mid-flight pause.**

### What does NOT trigger a mid-flight pause:

| Case | Disposition |
|---|---|
| `stakes_class == routine` (any timing) | Always-auto-fix path inside the pipeline; never escalated mid-flight |
| Stakes-class finding with `timing_tier == end-gate-expanded` | Silent; routed to end-gate-expanded; no mid-flight pause |
| Stakes-class finding with no timing qualifier | Treated as end-gate-expanded; no mid-flight pause |
| Any finding already resolved by the auto-fix loop | Already handled; no escalation |

**Routine findings are NEVER mid-flight escalated.** They remain on the always-auto-fix path and produce no developer-facing pause. This is the direct preservation of DEC-035 binding decision #1's anti-firehose intent: the build is not flooded with pauses for ordinary work.

### Anti-firehose guard

> **The explicit failure mode is over-escalation that re-creates the firehose.** Across a build with many routine and non-imminent findings and only a few true irreversible-and-imminent or build-invalidating findings: the number of mid-flight pauses MUST equal the number of bar-clearing findings and no more.
>
> The end-gate-expanded tier (DEC-036 D1 tier a) is the safety net for EVERYTHING that does not clear the mid-flight bar. Routine work goes there. Non-imminent stakes-class findings go there. The mid-flight tier is the exception; end-gate-expanded is the norm.
>
> **The bar must never be widened beyond `irreversible-and-imminent OR build-invalidating`.** Any pressure to widen the bar — adding timing conditions, adding stakes classes, adding "probably important" cases — must be resisted. If a finding seems important but does not meet the bar, it goes to end-gate-expanded. The end-gate provides the safety net.

---

## Engine Return Values

The engine returns one of two outcomes to the caller (step 2.2 or step 2.2.M):

| Return | Meaning |
|---|---|
| `{ outcome: "continue" }` | No finding in the array meets the mid-flight bar; proceed normally; any stakes-class findings are tagged for end-gate-expanded |
| `{ outcome: "pause-branch", finding: {...}, stakes_class, timing_tier }` | One bar-clearing finding detected; the engine raises the pause-ask to the developer for that finding |

**Multi-finding contract (K > 1 bar-clearing findings):** The engine raises one pause-ask at a time. If the findings array contains K bar-clearing findings, the caller invokes the engine once per bar-clearing finding, sequentially — each invocation surfaces exactly one pause-ask, and the developer resolves it before the next. The caller iterates until all bar-clearing findings have been surfaced. This preserves "one finding = one pause" (AC 11 / AC 5) without bundling multiple findings into a single pause card.

The Conductor (caller) does not classify findings itself. It invokes the engine and acts only on the engine's returned outcome.

---

## Pause-Ask Surface Contract (DEC-036 D5 Self-Sufficiency Floor)

When the bar is met, the engine raises **exactly one** developer-facing surface for that finding — a single decision card / pause-ask. It is never a stream of prompts. One finding = one pause.

The pause-ask carries **all three of these inline** — the developer can decide without leaving the surface to fetch context:

1. **What** — the change at stake: what is about to happen / what the finding describes
2. **Why** — the stakes class and why it is `irreversible-and-imminent` or `build-invalidating`
3. **Evidence** — the supporting detail from the pipeline result

### Pause-ask output template

```
## Mid-flight Escalation — Branch Paused

The build has paused story `{{S.slug}}` for a finding that meets the
stakes-and-timing bar (DEC-036 D1). Other stories continue building.

**Paused story:** `{{S.slug}}` — {{S.title}}
**Finding class:** {{stakes_class}}
**Timing tier:** mid-flight (irreversible-and-imminent or build-invalidating)

**What is at stake:**
{{finding.summary}}

**Why this qualifies (evidence):**
{{finding.evidence}}

**Recommended action:** {{finding.suggested_fix}}

**Options:**
- **Proceed** — apply the recommended resolution and resume this branch
- **Change** — alter the planned action (describe what you want instead)
- **Abort-that-branch** — stop this line of work; mark branch as abandoned
```

---

## Resolution Outcomes

The developer resolves the pause-ask with exactly one of three outcomes:

### Proceed
- Meaning: apply the recommended resolution and resume this branch
- Engine action: spawn a fix subagent scoped to the finding (Conductor commits the fix); return `"continue"` to the caller; merge and frontier re-evaluation proceed
- Disposition recorded: `escalated` (resolution: `fix-applied`)

### Change
- Meaning: alter the planned action — the developer describes a different resolution
- Engine action: receive the developer's alternative; spawn a fix subagent with the alternative instruction (Conductor commits); return `"continue"` to the caller; merge and frontier re-evaluation proceed
- Disposition recorded: `escalated` (resolution: `changed-action`, developer_instruction recorded)

### Abort-that-branch
- Meaning: stop this line of work; the branch is abandoned
- Engine action: abandon the branch; transition the story to `closed-incomplete`; append to `{{build_log}}` with outcome `"aborted"`; **continue the rest of the build** — other stories in `{{running}}` and `{{frontier}}` are unaffected; the build is NOT halted globally
- Disposition recorded: `escalated` (resolution: `branch-aborted`)
- Note: abort-that-branch stops one branch only; it does not halt the entire build phase. Other stories proceed unaffected.

**After any resolution** (Proceed, Change, or Abort-that-branch): no further mid-flight pause is raised for that resolved finding. The run is not left hung.

---

## Escalated Disposition

Any finding raised mid-flight via this engine is recorded with the **`escalated`** disposition.

**Disposition vocabulary:**

| Disposition | Assigned by | Meaning |
|---|---|---|
| `fixed` | Fixer (dev fix-mode) — routine path | Silently resolved; developer not involved |
| `dismissed` | Fixer (dev fix-mode) — requires non-empty rationale | Waved off by the fixer; rationale recorded |
| `triaged-out` | Fixer (dev fix-mode) | Outside scope; not actioned |
| `escalated` | Fixer (dev fix-mode) — per `finding-schema.md` Rule 2 and `directed-fix-invocation-contract.md` | Raised for human attention; not silently fixed |

The `escalated` disposition is **assigned by the fixer (dev fix-mode)** per the canonical finding schema (`skills/momentum/references/finding-schema.md` Rule 2) and the directed-fix invocation contract. This engine is the **sole owner of the mid-flight pause primitive** — it consumes already-`escalated` findings whose `timing_tier` is `mid-flight` and decides whether to raise a developer-facing pause-ask. Disposition assignment and mid-flight routing are distinct roles: the fixer assigns dispositions; this engine routes the mid-flight subset. The `escalated` disposition is visible in the end-gate report's "Mid-flight Escalations During Build" section so the developer can see what was raised and how it was resolved.

---

## Shared-Primitive Contract

This engine is the **only** place where mid-flight bar evaluation and the pause primitive live.

- `conduct-build-phase-frontier` (step 2.2) calls this engine for mid-flight escalation on the build leg
- `conduct-merge-and-conflict-resolution` (step 2.2.M) calls this engine for mid-flight escalation on the merge leg

Neither caller implements its own bar logic or its own pause prompt. Any apparent shortcut — "I'll just check the class inline here" or "I'll raise a quick prompt in the merge step" — violates the shared-primitive contract and risks fragmenting the narrow bar. Both callers must defer entirely to this engine.

---

## AVFL-Phase Routing

AVFL findings (Phase 3) carry the same `stakes_class` and `timing_tier` fields. After AVFL produces its findings array:

- Routine findings → end-gate report (no escalation check)
- Stakes-class findings with `timing_tier == end-gate-expanded` → end-gate-expanded decision cards (no mid-flight pause; AVFL runs after the build phase is complete)
- Stakes-class findings with `timing_tier == mid-flight` → invoke this engine; engine evaluates the bar; pause-ask fires if the bar is met

Note: AVFL runs after all stories are merged, so mid-flight escalations from AVFL are post-merge pauses, not in-build pauses. The bar evaluation and pause-ask contract are identical regardless of phase. **Resolution outcome differences in the post-merge phase:** Proceed = spawn fixer subagent and commit to the sprint branch; Change = fixer with developer's alternative instruction and commit. **Abort-that-branch does not apply post-merge** — there is no in-flight story branch to abandon. If a finding is post-merge and the developer wants to reject it, the outcome is "open a follow-up backlog story" (route to end-gate-expanded tracking) rather than branch-abort. The caller (workflow.md Phase 3) must adapt resolution outcome semantics accordingly.

---

## Summary: What This Engine Is NOT

| Boundary | Owned by |
|---|---|
| Terminal end-gate (single mandatory human gate at run close) | Conductor Phase 5 (a separate surface and separate story) |
| Stakes finding-class schema field (`stakes_class`, `timing_tier`) | Canonical finding schema at `skills/momentum/references/finding-schema.md` (upstream; this engine consumes those fields) |
| Anti-rubber-stamp forcing function (DEC-036 D4) | End-gate report (requires per-card acknowledgment; lives in Phase 5) |
| Routine auto-fix loop | Per-story pipeline internals (never routes through this engine) |
