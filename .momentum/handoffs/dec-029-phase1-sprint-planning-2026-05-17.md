# Handoff: DEC-029 Phase 1 — Build Out via Sprint Planning (Fresh Session)

**Date:** 2026-05-17
**Branch:** main (no active sprint)
**Purpose:** Run `momentum:sprint-planning` to build the 5 DEC-029 Phase 1 backlog stubs into a ready, activated sprint.

---

**Status: COMPLETED — 2026-05-18**
Sprint `sprint-2026-05-17` is now **active**. 5 stories, 2 waves. Commit `9a40d1e`.
AVFL: CHECKPOINT_WARNING (score 65/100) — critical finding (missing `change_type` on stories 2+3) fixed at commit `3dec275`. Sprint activation proceeded.

---

---

## Before starting the new session

Major Momentum workflow → refresh the plugin cache and restart, per practice:

1. `/plugin marketplace update momentum`
2. **Full session restart** (`/reload-plugins` is insufficient).
3. Then paste the "Run this" prompt below.

## State (verified this session, 2026-05-17)

- **DEC-029 triage is done.** 5 net-new Phase 1 stubs are in the backlog (`status: backlog`), 1 refine-watch entry queued, all committed and pushed to `origin/main` (through `6011443`).
- **Gate 1 is CLEARED.** DEC-029 Gate 1 = "Does `agents.json` exist?" — both criteria met:
  - `routing-table-schema-and-implementation` → status `done`
  - `momentum/agents.json` present on disk (defaults/project schema)
  - → Phase 1 implementation is **unblocked**. No further gating before this sprint.
- **No active or planning sprint.** Last completed: `sprint-2026-05-16`. Clean slate for a new sprint.

## The 5 stubs to build out (this sprint's scope)

All are `story_type: practice`, source DEC-029 (`_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md`). Stubs are intentionally thin — sprint-planning/create-story enriches ACs, tasks, dev notes. That is expected, not a gap.

| slug | epic | prio |
|---|---|---|
| `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard` | quality-enforcement | high |
| `momentum-harnessjson-schema-and-plugin-shipped-defaults` | bring-your-own-tools | high |
| `sprint-planning-frozen-per-story-contract-holistic-coverage` | sprint-dev-workflow | high |
| `e2e-validator-agent-body-rewrite-de-gherkin-harness-driven` | agent-team-model | medium |
| `create-story-method-selection-step` | story-cycles | medium |

## Intra-batch dependency order (sprint-planning must honor)

These are not independent — sequence the sprint accordingly:

1. **Foundational, no intra-batch deps:** `enforced-verification-rule…` (the change-type→method routing rule + harness-profile requirement + anti-insider-knowledge guard) and `momentum-harnessjson-schema…` (the `harness.json` schema + plugin defaults).
2. **Consumes `harness.json`:** `e2e-validator-agent-body-rewrite…` (de-Gherkin, drives from `harness.json`).
3. **Routes off the verification rule:** `create-story-method-selection-step`.
4. **Consumes both the rule and `harness.json`:** `sprint-planning-frozen-per-story-contract-holistic-coverage` (frozen per-story contract + per-sprint coverage plan + adversarial guard).

## Then run

> Run `momentum:sprint-planning`. Build a single sprint from exactly these 5 DEC-029 Phase 1 backlog stubs:
> `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard`,
> `momentum-harnessjson-schema-and-plugin-shipped-defaults`,
> `sprint-planning-frozen-per-story-contract-holistic-coverage`,
> `e2e-validator-agent-body-rewrite-de-gherkin-harness-driven`,
> `create-story-method-selection-step`.
> Honor the intra-batch dependency order above. Gate 1 is cleared — no external blockers.

## Explicitly OUT of scope for this sprint

- **The 7 refine-watch stories** (queue id `iq-20260518032341-976884b5`): `acceptance-testing-process-and-standards`, `change-type-routing-in-sprint-dev`, and the e2e-validator cluster (`e2e-validator-black-box-hardening`, `e2e-validator-toolsearch-fix`, `e2e-and-qa-validator-prompts-branch-standalone-vs-team`, `e2e-client-side-coverage`, `e2e-validator-fixture-spec-sync-stale-reference-detection`). These need a `momentum:refine` reconciliation pass against DEC-029 first — do NOT pull stale-scoped versions into this sprint.
- **DEC-029 Phase 2** (full sprint-dev rewrite) and **Phase 3** (beads state ledger, gated on DEC-028) — separate downstream decisions/epics.

## Caveats / awareness

- `acceptance-testing-process-and-standards` shows `status: done`, but DEC-029 D7 **retires** its output (the standard). The new `enforced-verification-rule…` stub replaces it. A "done" story's concern reappearing as a fresh stub is expected here — not a mistake.
- **DEC-030 exists** (`Dependency-Driven Execution Model` — DAG dispatch, frozen-scope sprints; recorded 2026-05-17, commits `e5b9068`/`6011443`). It governs sprint *execution* mechanics. Sprint-planning for DEC-029 Phase 1 should not contradict DEC-030's frozen-scope/DAG model — skim DEC-030 before activating, and flag any conflict rather than planning around it silently.
- Side note carried forward (not this sprint): skill-dev-guide documents `model:` as short form (`opus|sonnet|haiku`) while all `skills/momentum/skills/*` use full IDs — worth its own triage item later.
