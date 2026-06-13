---
title: Retire momentum:sprint-dev — soft-deprecate, soak, then hard-remove the legacy builder
story_key: conduct-adoption-retire-sprint-dev
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: practice
priority: high
change_type:
  - skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/sprint-dev/
  - skills/momentum/skills/impetus/references/dispatch.md
  - skills/momentum/references/session-greeting.md
  - commands/sprint-dev.md
---

# Retire momentum:sprint-dev — soft-deprecate, soak, then hard-remove the legacy builder

## Story

As the maintainer of the Momentum build practice,
I want `momentum:sprint-dev` (the legacy wave-loop builder) formally retired in sequenced phases — stop routing to it, let conduct soak as the sole engine, then delete the skill entirely —
so that there is exactly one build engine of record, the dead legacy path can no longer be invoked or drift against the live dev-agent contract, and the skill directory is gone rather than lingering as a zombie forever.

This is the downstream adoption step that **DEC-037 already named** (`conduct-adoption-retire-sprint-dev`) but never created as a tracked item. It is unblocked: conduct completed its first live end-to-end run on 2026-06-12 (sprint-2026-06-10, five seam-fix stories, AVFL-converged 98/100, E2E-passed, merged to main), satisfying DEC-037's "once conduct is proven runnable end-to-end" gate.

## Why this exists (audit basis, 2026-06-12)

A four-surface deprecation audit (routing, tooling/agents, decisions/docs, capability-parity) concluded: **conduct is a confirmed functional superset of sprint-dev — zero capability gap — and keeping sprint-dev is itself a liability.** sprint-dev is already broken against the current dev-agent contract: dev agents no longer commit (DEC-035, the Conductor is sole git authority), but sprint-dev Phase 3 git-merges story branches with no staging step of its own, so a legacy run today would merge **empty** story branches. The wave-loop, mid-build fix-queue, sprint-level AVFL batching, and standalone architecture-guard leg are *intentionally retired* per DEC-035/036 — by-design behavioral changes, not missing capabilities.

The audit surfaced **one hard prerequisite** that must be closed before sprint-dev can be pulled, plus a clean edit surface.

## The one hard prerequisite (Phase 0 — must land first)

`momentum-tools sprint complete` — the transition that moves a sprint to `completed[]` and unsets `retro_run_at`, which `momentum:retro` keys on — is called **only** by sprint-dev (`skills/momentum/skills/sprint-dev/workflow.md:718`). The conductor workflow **never** calls it (verified: zero `sprint complete` hits in `conductor/workflow.md`). This is a latent conduct bug independent of deprecation: every conduct-built sprint is left un-completed and retro finds nothing to run. (The 2026-06-12 first live run compensated for this by hand — the Conductor ran `sprint complete` manually after merge.)

**Phase 0 task:** Port `momentum-tools sprint complete` into the conductor's Phase 5 APPROVE sequence (after the story `verify → done` transitions, before the push summary). Verify end-to-end that `momentum:retro` picks up a conduct-completed sprint with no manual step. Until this lands, do NOT remove sprint-dev.

## Acceptance Criteria

### Phase 0 — sprint-completion parity (blocking prerequisite)
1. The conductor Phase 5 APPROVE sequence calls `momentum-tools sprint complete` after transitioning stories to `done`, so a conduct build completes the sprint with no hand-compensation.
2. A conduct-completed sprint is observably picked up by `momentum:retro` (the `retro_run_at`/`completed[]` state the retro precondition reads is set by conduct, verified end-to-end).

### Phase 1 — soft-deprecate (stop routing, mark legacy, keep file as redirect stub)
3. No live routing surface dispatches a build to `momentum:sprint-dev`. Concretely: `impetus/references/dispatch.md` "legacy wave-loop" row removed or repointed; `.claude/rules/impetus.md` legacy line flipped to deprecated; `references/session-greeting.md:157-166` menu strings ("Run the sprint" / "Continue the sprint" / "Activate sprint") repointed to `momentum:conductor`.
4. `commands/sprint-dev.md` becomes a redirect stub: invoking `/momentum:sprint-dev` prints a deprecation notice and points the developer at `/momentum:conduct`; it does not run the legacy wave-loop.
5. `skills/momentum/skills/sprint-dev/SKILL.md` carries a `DEPRECATED` marker in its description and body; the workflow body is reduced to a deprecation-halt redirect (the `momentum:feature-status` stub pattern — registry entry retained, body halts with a pointer). The skill is inert but present.
6. sprint-planning Step 5.5 prose (the team-composition gate) is reworded so its rationale cites conduct's per-story-pipeline role requirements rather than sprint-dev's `<team-composition>` block; the gate continues to validate the same agent files (dev roles, qa-reviewer, e2e-validator, architecture-guard), which conduct also needs — so the gate stays valid, only the citation changes.
7. The impetus eval `eval-dispatch-uses-agent-not-skill.md` (which uses sprint-dev as its worked example) and the 5+ `skills/momentum/skills/sprint-dev/evals/` files are marked deprecated or dropped so CI/eval runs do not assert against a dead target.
8. Soft cosmetic sweep: `retro/workflow.md`, dev-agent definition lineage notes, and any remaining prose that says "sprint-dev Phase N parses it" are reworded to conduct (these are descriptive, not load-bearing — the `AGENT_OUTPUT_START/END` parse contract is mandated for conduct regardless).

### Phase 2 — soak / safety gate (define the bar for deletion)
9. A documented soak condition gates Phase 3: at least **N consecutive successful conduct sprints** (recommend N=3) completed with no fallback to sprint-dev, AND confirmation that sprint-planning no longer emits or depends on wave-model artifacts (`wave_count`, wave-derived ordering) that only sprint-dev consumed. The soak bar is recorded in this story (or a linked decision) so Phase 3 is not executed prematurely.

### Phase 3 — hard removal (final retirement: delete the skill)
10. **The `skills/momentum/skills/sprint-dev/` directory is deleted in full** — SKILL.md, workflow.md, references, evals — once the Phase 2 soak condition is met.
11. `commands/sprint-dev.md` is deleted (the redirect stub is removed; `/momentum:sprint-dev` no longer resolves).
12. The dispatch.md legacy row and any remaining skill-registry/marketplace entry for sprint-dev are removed; the orphaned sprint-dev eval coverage is deleted (or its still-relevant assertions migrated to conduct evals).
13. The PRD requirements that defined sprint-dev (FR62, FR63, FR74, and the FR139/FR140 coexistence clauses) are marked retired/removed in `prd.md`, and `architecture.md`'s sprint-dev-specific sections (e.g. Decision 31 team-review contrast) are annotated as historical.
14. A final repo-wide grep confirms **no live reference resolves to the deleted skill**: `grep -rn "sprint-dev" skills/ commands/ .claude/` returns only archival/comment matches, none that route to or invoke it. Archival mentions under `.momentum/stories/`, `_bmad-output/`, and retros are left intact as the audit trail (no edits — they are history).
15. The plugin version is bumped (minor) on the soft-deprecate release and again on the hard-removal release, per the version-on-release rule.

## Tasks / Subtasks

- [ ] **Phase 0 (blocking):** Port `momentum-tools sprint complete` into conductor Phase 5 APPROVE; add an eval that a conduct-completed sprint satisfies the retro precondition. (AC 1, 2)
- [ ] **Phase 1:** Repoint all live routing (dispatch.md, impetus rule, session-greeting) to conductor; stub the slash command; mark SKILL.md deprecated + redirect-halt body; reword sprint-planning Step 5.5 citation; deprecate/drop sprint-dev + the one impetus eval; cosmetic prose sweep. (AC 3–8)
- [ ] **Phase 2:** Author the soak/safety-gate condition (N=3 successful conduct sprints + no wave-model dependence) and record it. (AC 9)
- [ ] **Phase 3:** Once soaked — delete `skills/momentum/skills/sprint-dev/` and `commands/sprint-dev.md`; remove registry/dispatch entries + orphaned evals; retire FR62/63/74/139/140 in PRD + annotate architecture.md; final grep gate; version bump. (AC 10–15)

## Dev Notes

- **Sequencing is mandatory.** Phase 0 before Phase 1 (else conduct builds silently stop completing sprints). Phase 1 before Phase 2 before Phase 3 (delete the safety net last). Phase 3 may be a separate story/sprint after the soak — split if grooming prefers, but the soft-deprecate phases (0–1) should ship together so the dead path stops being reachable promptly.
- **Soft-deprecate keeps the eval history and the inert file as a safety net; hard-remove is the deliberate end.** Do not collapse the two — the user explicitly wants the terminal deletion planned, not an indefinite zombie.
- **The ~240 archival mentions** (`.momentum/stories`, `_bmad-output`, retros, decisions) need NO edits in any phase — they are the audit trail of how the practice evolved.
- **Inverse-hazard note:** because sprint-dev is already broken against the dev no-commit contract, leaving it reachable is an active risk (an accidental `/momentum:sprint-dev` run merges empty branches). Phase 1 closes that risk; Phase 3 eliminates it.

### References
- DEC-037 (`_bmad-output/planning-artifacts/decisions/dec-037-conduct-invocation-model-standalone-skill-2026-06-04.md`) — names this step and the coexistence-then-retire sequencing.
- DEC-035 / DEC-036 — adopt conduct; Conductor sole git authority; behavioral changes that intentionally retire the wave-loop/stop-gate model.
- Deprecation audit, 2026-06-12 (this conversation) — four-surface analysis: no capability gap, one prerequisite (`sprint complete`), clean edit surface.
- Prerequisite evidence: `sprint-dev/workflow.md:718` (sole `sprint complete` caller); `conductor/workflow.md` (zero `sprint complete` calls).
- First-live-run proof (satisfies DEC-037 gate): sprint-2026-06-10 build ledger + end-gate report under `.momentum/sprints/sprint-2026-06-10/` and `.momentum/handoffs/`.

## Dev Agent Record
