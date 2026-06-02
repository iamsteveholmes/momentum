---
title: Repoint sprint-dev code-review calls to the adapter
story_key: code-review-adapter-repoint-sprint-dev
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - code-review-adapter-retire-stub
  - conduct-skill-scaffold-and-spine
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
---

# Repoint sprint-dev code-review calls to the adapter

## Story

As the maintainer of the Momentum sprint-dev workflow,
I want the sprint-dev per-story code-review step to call the bmad-code-review adapter instead of the retired code-reviewer stub,
so that sprint-dev produces the same adapter-normalized findings that conduct relies on, and there is exactly one code-review entry point across the practice.

## Description

The conduct rewrite standardizes code review behind a single adapter (the bmad-code-review adapter), which normalizes review output into a consistent findings shape that downstream stages (triage, auto-fix, escalation, end-gate reporting) depend on. As part of that standardization, the legacy `momentum:code-reviewer` stub is being retired in a separate story (`code-review-adapter-retire-stub`).

The sprint-dev workflow still wires its per-story review step to that legacy invocation. This story repoints every code-review call inside the sprint-dev workflow so it invokes the adapter instead of the retired stub. After this change, running the sprint-dev per-story review yields adapter-normalized findings — the same observable output shape the rest of the practice expects.

**What:** Update `skills/momentum/skills/sprint-dev/workflow.md` so the code-review step invokes the bmad-code-review adapter, replacing the retired stub invocation.

**Why:** Without this repoint, sprint-dev would either call a stub that no longer exists (breaking the workflow) or emit findings in a non-normalized shape that downstream consumers cannot process. A single adapter entry point is what gives the practice one consistent findings contract.

**Pain context:** Two divergent review paths — one for conduct, one stale in sprint-dev — would mean two findings shapes, two places to maintain, and silent drift between what conduct sees and what sprint-dev sees. The retire-stub story removes the old entry point; this story makes sure the surviving caller points at the adapter.

**Source decisions:** This is pure call-site wiring. It is **unchanged by DEC-036** — the mid-flight escalation tier, dispositions, timing tiers, and report-rendering amendments introduced by DEC-036 do not alter how a caller reaches the adapter. DEC-035 establishes the single-adapter, single-end-gate direction this repoint serves. Governing spec sections: section 4 ("replace every momentum:code-reviewer invocation") and section 12.

## Acceptance Criteria

1. The sprint-dev code-review step invokes the bmad-code-review adapter as its code-review entry point.
2. The sprint-dev workflow no longer invokes the retired code-reviewer stub anywhere; every former stub invocation in the workflow has been replaced with an adapter invocation.
3. Running the sprint-dev per-story review produces adapter-normalized findings — the same findings shape the adapter emits when invoked directly.
4. The repoint changes only the code-review call site(s) in the sprint-dev workflow; the surrounding per-story review flow (when review runs, what it reviews, how its result feeds the next step) continues to behave as before, now sourced from the adapter.
5. Because this story is pure call-site wiring, it introduces no mid-flight escalation behavior, no disposition handling, and no end-gate or report-rendering logic; those DEC-036 concerns are out of scope and the repoint leaves them untouched (this story is unchanged by DEC-036).
6. After the repoint, a sprint-dev run that reaches the code-review step completes that step without referencing the retired stub and without error attributable to a missing review entry point.

## Tasks / Subtasks

- [ ] Locate every code-review invocation in `skills/momentum/skills/sprint-dev/workflow.md` (the per-story review step and any other place review is triggered).
- [ ] Replace each located invocation so it calls the bmad-code-review adapter instead of the retired code-reviewer stub (spec section 4).
- [ ] Confirm no remaining reference to the retired stub exists anywhere in the sprint-dev workflow file.
- [ ] Preserve the surrounding per-story review flow: the trigger conditions, the inputs handed to review, and how the review result is consumed downstream stay the same — only the callee changes.
- [ ] Verify by invocation that a sprint-dev per-story review run returns adapter-normalized findings (consistent with what the adapter emits when invoked directly).
- [ ] Confirm the repoint adds no escalation/disposition/end-gate logic — scope is wiring only (DEC-036 out of scope here).

## Dev Notes

This story is a **call-site repoint** inside `skills/momentum/skills/sprint-dev/workflow.md`. The behavioral contract is black-box: after the change, the sprint-dev review step must reach the bmad-code-review adapter and yield adapter-normalized findings. The internal mechanics of how the adapter normalizes are owned by the adapter stories, not here.

**Governing spec sections (cited by number from the authoring brief):**
- **Section 4** — "replace every momentum:code-reviewer invocation": the mandate to swap each legacy stub call for an adapter call. This story executes that mandate for the sprint-dev workflow specifically.
- **Section 12** — call-site wiring scope for repointing callers onto the adapter.

**Unchanged by DEC-036.** DEC-036 amends DEC-035 to permit a narrow, stakes-gated mid-flight escalation tier and to require legible dispositions and an anti-rubber-stamp end-gate. None of that touches call-site wiring: a caller still simply invokes the adapter. This story therefore inherits no escalation, disposition (fixed / dismissed / triaged-out / escalated), or timing-tier (end-gate-expanded / mid-flight) behavior. Those live in the adapter and conduct-spine stories. Keep this change scoped strictly to swapping the callee.

**Dependencies and why they exist:**
- `code-review-adapter-retire-stub` — the retired stub must be gone (or superseded) before/as this repoint lands, so there is no surviving path back to the legacy entry point. This is the entry point this story repoints *away from*.
- `conduct-skill-scaffold-and-spine` — per the breakdown repoint, the conduct skill scaffold/spine establishes the orchestration context into which the single-adapter convention is wired; this story's repoint aligns sprint-dev with that established spine.

**Repo nature:** Markdown/bash practice repo. The change is an edit to a skill workflow markdown file (`change_type: skill-instruction`); there is no app/UI/backend lane. Verification is by skill invocation (`verification_method: skill-invoke`): run the sprint-dev review step and observe that it reaches the adapter and returns normalized findings.

### References

- Epic: `momentum-sprint-orchestration` — from `_bmad-output/planning-artifacts/epics.json` (the sprint orchestration epic under which conduct/sprint-dev work is grouped).
- Decision: **DEC-035** — adopt conduct; single adapter / single human end-gate direction that motivates one code-review entry point.
- Decision: **DEC-036** — narrow stakes-gated mid-flight escalation amendment; explicitly **does not** apply to this call-site wiring story (noted here to record that the exemption was considered and is intentional).
