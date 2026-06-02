---
title: Add fix-mode to momentum:dev that branches on the stakes-class
story_key: dev-fix-mode-entry
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - agent-definition
verification_method: skill-invoke
depends_on:
  - directed-fix-invocation-contract
touches:
  - skills/momentum/agents/dev.md
  - skills/momentum/skills/dev/workflow.md
---

# Add fix-mode to momentum:dev that branches on the stakes-class

## Story

As the Conductor running the conduct build phase,
I want momentum:dev to accept a directed-fix payload and respond differently depending on the stakes-class of the finding,
so that routine findings are silently auto-fixed while stakes-class findings are raised back to me as escalations instead of being quietly committed.

## Description

momentum:dev currently has a single operating mode: green-field build, in which it takes a story and produces an implementation. The conduct rewrite needs momentum:dev to also act as the executor of *directed fixes* — small, targeted corrections handed to it by the Conductor's auto-fix loop after a finding has been raised against an existing build.

This story adds a **fix-mode** to momentum:dev that runs alongside the existing green-field build mode. Fix-mode accepts a directed-fix payload (the upstream invocation contract is delivered by `directed-fix-invocation-contract`, this story's dependency) and acts on it.

The load-bearing behavior this story introduces is the **stakes-class branch**. Per DEC-036 amendment D2, fix-mode must read the `stakes_class` field on the directed-fix payload and branch on it:

- A **routine** finding keeps the always-auto-fix behavior: dev edits the affected file(s) and commits the fix. This is unchanged from the conduct baseline and must never be slowed down.
- A **stakes-class** finding (security/auth-isolation; irreversible/destructive such as migration, delete, force-push, prod deploy; or high-blast-radius/architecture) does **not** get edited or committed by dev. Instead dev returns an **escalation** output carrying, inline, the what / why / evidence of the finding plus the timing tier the finding belongs to.

Without this branch the `stakes_class` field added upstream is inert — the schema change carries no behavior. This story is what makes the field do something: it routes the stakes-class findings out of the silent auto-fix path and turns them into raised escalations the Conductor can surface at the human gate (or, for the narrow mid-flight tier, immediately).

The escalation output is a *disposition*, not a fix: in conduct vocabulary, a stakes-class finding that dev declines to silently fix is dispositioned `escalated` (raised, not silently fixed), distinct from `fixed`, `dismissed`, and `triaged-out`.

**Why this matters / pain context:** The whole point of conduct (DEC-035) is one human gate at the end with a legible auto-fix loop — no firehose of mid-flight interruptions. DEC-036 narrowly amends that to permit a high-bar escalation tier so that genuinely dangerous findings (an irreversible-and-imminent action, or one that invalidates the build) are not silently auto-fixed and buried. If dev silently fixed *everything*, a stakes-class finding would be committed and lost in the noise; if dev escalated *everything*, conduct would become the firehose it was designed to eliminate. The stakes-class branch is the exact dividing line that keeps routine findings fast and silent while peeling off only the stakes-class ones into escalations.

**Source decisions:** DEC-035 (adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop). DEC-036 (narrow, high-bar, stakes-gated escalation tier amending DEC-035 binding decision #1; routine findings stay always auto-fixed; dispositions include `escalated`).

## Acceptance Criteria

1. momentum:dev accepts a directed-fix payload as an input mode, distinct from its existing green-field build invocation. Invoking dev with a directed-fix payload puts it in fix-mode and does not trigger a green-field build.

2. When fix-mode receives a finding whose stakes-class is **routine** and the finding is legitimate, dev applies the fix by editing the affected file(s) and produces a commit containing that fix. (Routine = always auto-fix, unchanged.)

3. When fix-mode receives a finding whose stakes-class is a **stakes class** (security/auth-isolation; irreversible/destructive — migration, delete, force-push, prod deploy; or high-blast-radius/architecture) and the finding is legitimate, dev makes **no edit and produces no commit** for that finding. Instead it returns an **escalation** output.

4. The escalation output produced for a stakes-class finding carries, inline (self-contained, no external lookup required to understand it): the **what** (a description of the finding), the **why** (the rationale / stakes that make it stakes-class), and the **evidence** (the concrete observation supporting the finding).

5. The escalation output also carries the **timing tier** the finding belongs to: either `end-gate-expanded` (the default tier, raised for the human end-gate) or `mid-flight` (the narrow tier, raised immediately). The tier value is present and is one of those two values.

6. The branch is driven by the stakes-class of the finding: a routine finding produces a fix+commit (AC 2) and a stakes-class finding produces an escalation with no fix+commit (AC 3–5). The two paths are mutually exclusive for a single finding — dev never both commits a fix and escalates the same finding.

7. When fix-mode dispositions a finding as **dismissed** (the finding is judged not to require a fix), dev records a **non-empty rationale** explaining the dismissal. A dismissal with an empty or missing rationale is not produced.

8. The existing green-field build mode is unaffected: invoking dev with a green-field story (no directed-fix payload) produces the same build behavior as before this story, with no escalation output and no fix-mode branching applied.

## Tasks / Subtasks

- [ ] Update `skills/momentum/agents/dev.md` to declare two operating modes — the existing green-field build mode and the new fix-mode — and the input that selects fix-mode (a directed-fix payload) (AC 1, AC 8)
- [ ] Update `skills/momentum/skills/dev/workflow.md` to add the fix-mode entry path that reads the directed-fix payload delivered by the upstream invocation contract (AC 1)
- [ ] Implement the stakes-class branch in fix-mode: read the `stakes_class` field and route on it (AC 6)
  - [ ] Routine branch: edit affected file(s) and commit the fix (AC 2)
  - [ ] Stakes-class branch: do NOT edit, do NOT commit; build and return the escalation output (AC 3)
- [ ] Define the escalation output shape so it carries inline what / why / evidence (AC 4) and the timing tier with allowed values `end-gate-expanded` | `mid-flight` (AC 5)
- [ ] Ensure mutual exclusivity for a single finding: a fix+commit OR an escalation, never both (AC 6)
- [ ] Implement the `dismissed` disposition path requiring a non-empty rationale; reject/avoid empty-rationale dismissals (AC 7)
- [ ] Confirm green-field build mode is untouched: a green-field invocation still produces the prior build behavior with no fix-mode branching and no escalation output (AC 8)
- [ ] Self-check fix-mode by invoking dev with a routine directed-fix payload, a stakes-class directed-fix payload, and a dismissed finding, and inspecting the resulting commits/outputs

## Dev Notes

**Technical grounding.** This is an `agent-definition` change: the work lands in the dev agent definition and its workflow, not in app/UI/backend code. The two touched files are `skills/momentum/agents/dev.md` (the agent definition declaring modes and inputs) and `skills/momentum/skills/dev/workflow.md` (the procedural workflow that branches). Verification is `skill-invoke`: behaviors are observed by invoking dev in fix-mode and inspecting its outputs and the commits it produces — black-box, no source inspection required.

**The stakes-class branch is the whole point.** Per DEC-036 amendment D2, the `stakes_class` field added by the upstream invocation contract is inert until something branches on it. This story is that something. The branch must be the dividing line: routine stays on the silent always-auto-fix path (fix + commit), and only stakes-class findings leave that path to become escalations. Bias toward keeping the routine path fast and unchanged.

**Stakes classes (vocabulary, fixed):** security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; default routine. A finding is stakes-class if it falls in any of the non-routine classes.

**Dispositions (vocabulary, fixed):** `fixed` | `dismissed` (REQUIRED non-empty rationale) | `triaged-out` | `escalated` (NEW — raised, not silently fixed). Fix-mode produces `fixed` on the routine branch, `escalated` on the stakes-class branch, and may produce `dismissed` (with mandatory rationale) when a finding does not warrant a fix.

**Timing tiers (vocabulary, fixed):** `end-gate-expanded` (default — the escalation waits for the single human end-gate) | `mid-flight` (the narrow tier — raised immediately). The mid-flight bar must stay narrow: irreversible-and-imminent OR build-invalidating ONLY. The escalation output names which tier the finding belongs to (AC 5); this story's responsibility is to *carry* the tier on the escalation, not to widen it.

**What dev must NOT do on the stakes-class branch:** no edit, no commit, no silent fix. The Conductor (not dev) owns surfacing the escalation; dev's job ends at returning a self-contained escalation payload (what/why/evidence/tier) so the Conductor can render it.

**Anti-firehose intent (preserved):** routine findings are ALWAYS auto-fixed. The escalation path exists only for the narrow stakes-class set. Do not let fix-mode escalate routine findings.

**Governing spec sections (cited by number from the authoring brief):** DEC-035 binding decision #1 (one human end-gate; routine findings auto-fixed; legible loop). DEC-036 amendment D2 (fix-mode branches on `stakes_class`; stakes-class → `escalated` + escalation payload instead of edit+commit; routine → unchanged always-auto-fix). DEC-036 disposition set (adds `escalated`; `dismissed` requires non-empty rationale). DEC-036 timing tiers (`end-gate-expanded` default | `mid-flight` narrow).

### References

- Epic: `momentum-sprint-orchestration` — `_bmad-output/planning-artifacts/epics.json` (the conduct / in-session per-story autonomous-build single-end-gate rewrite of sprint-dev under which this story sits).
- Decision: DEC-035 — adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop (what it changed AND dismissed).
- Decision: DEC-036 — narrow, high-bar, stakes-gated mid-flight escalation tier amending DEC-035 binding decision #1; amendment D2 (stakes-class branch in fix-mode); routine findings stay always auto-fixed; dispositions add `escalated`; `dismissed` requires non-empty rationale; timing tiers `end-gate-expanded` | `mid-flight`.
- Depends on: `directed-fix-invocation-contract` — delivers the directed-fix payload (including the `stakes_class` field) that fix-mode reads.
