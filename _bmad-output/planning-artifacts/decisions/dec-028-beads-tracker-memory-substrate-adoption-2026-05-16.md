---
id: DEC-028
title: Beads as Tracker/Dependency/Memory Substrate — Adoption Under Momentum via Dual-Write Spike
date: '2026-05-16'
status: decided
source_research:
  - path: docs/research/beads-vs-momentum-tracker-evaluation-2026-05-16.md
    type: prior-research
    date: '2026-05-16'
---

# DEC-028: Beads as Tracker/Dependency/Memory Substrate — Adoption Under Momentum via Dual-Write Spike

## Summary

Evaluated beads v1.0.4 (Dolt-powered issue tracker) as a replacement for Momentum's hand-built work-item store, dependency graph, and persistent memory model. The verdict is a "build-on" decision, not a build-vs-buy replacement: beads is clearly superior for the tracker, dependency, and memory substrate layers — specifically `bd ready` + `--claim` for dependency-aware scheduling, `discovered-from` for intake, and `bd prime` for compaction-resilient memory. Momentum's enforced workflow fidelity, FSM transitions, approval-SHA gates, and quality practice (AVFL, code-reviewer, retro audit, distill) have no equivalent in beads and must remain unchanged on top. Adoption proceeds via a one-sprint dual-write spike (not big-bang migration), with explicit go/no-go criteria before flipping beads to authoritative. Epics consolidate cleanly into bd's native epic+parent-child model; features survive as relate-linked epic-beads preserving M:N semantics. The molecules/formulas/gates DAG engine is deferred — least mature surface, overlaps sprint orchestration already owned by Momentum.

---

## Decisions

### D1: Adopt Beads as Tracker/Dependency/Memory Substrate — ADAPTED

**Research recommended:** Adopt beads underneath Momentum as the state/dependency/memory engine. The single biggest win is `bd ready` + atomic `--claim` replacing the bespoke dependency graph in sprint-dev Phases 1–3. Secondary wins: `discovered-from` collapses intake-queue triage, `bd remember`/`bd prime` addresses compaction amnesia by design, and hash IDs + claim/lease/merge-slot provide real multi-agent concurrency safety that Momentum currently lacks.

**Decision:** Adopted in adapted form — proceed via a one-sprint dual-write spike rather than immediate full migration. Sprint-manager dual-writes to both `index.json` (authoritative) and beads during the spike. `index.json` remains authoritative until 3 of 4 post-spike gate criteria are met.

**Rationale:**
Beads' dependency and memory primitives are decisively better than what Momentum hand-builds. But the Dolt infrastructure dependency and the risk of data leaving the reviewable git tree are real. The spike proves value before committing. If the gate criteria aren't met, the spike still yields a better dependency engine for sprint-dev regardless of the broader migration outcome.

---

### D2: Keep Momentum's Enforced Orchestration and Quality Practice on Top — ADOPTED

**Research recommended:** Momentum's enforced workflow fidelity is the moat — skills as sole writers, FSM-validated transitions, approval-SHA gates, and the full quality practice (AVFL, code-reviewer, qa-reviewer, e2e-validator, architecture-guard, retro DuckDB audit, distill). Beads has no enforcement model. The integration is advisory by design. Adopting beads does not import enforcement; it presumes Momentum supplies it.

**Decision:** Adopted. Sprint-manager becomes a thin enforcing wrapper over `bd` calls, not retired. All quality practice skills remain unchanged. Beads is the substrate; Momentum remains the practice.

**Rationale:**
The entire value proposition of Momentum is that it enforces quality that agents would otherwise skip. Beads explicitly does not provide this. Retaining the enforcement layer is non-negotiable regardless of substrate adoption.

---

### D3: Keep Story Spec Prose in Git Tree — ADOPTED

**Research recommended:** Do not move story `.md` spec files into Dolt. Beads tracks the work item; the markdown stays the contract. Keep `.momentum/stories/*.md` as the spec of record and link via `--spec-id`/`--external-ref`. Moving spec prose into a gitignored Dolt DB removes it from PR review, the git diff, and the working tree.

**Decision:** Adopted. Story `.md` files remain in the git tree permanently. Beads beads are linked to story specs via `--spec-id`, not used as the spec store.

**Rationale:**
Story specs are the reviewable contract — they need to be in PR diffs and `git log`. Dolt history is a supplemental audit layer, not a substitute for in-tree reviewability. This is the clearest constraint in the evaluation and not a close call.

---

### D4: Consolidate Epic/Feature Taxonomy into Beads — ADAPTED

**Research recommended:** Epics consolidate strictly better — `epic_slug` string field → real bd `epic` type with `--parent` children (dotted IDs), `bd epic status`, label inheritance. Features don't have to be deleted: model features as their own epic-type beads with `relates-to` edges to member stories (preserves M:N, `value_analysis`/`system_context` in bead body, stays queryable). Feature-grooming's 6-signal scan and feature-status/canvas rendering must be rebuilt against `bd query`/`bd sql`.

**Decision:** Adopted in adapted form. Epics adopt bd's native epic+parent-child model as specified. Features become epic-type beads with `relates-to` edges (not labels — the label approach loses feature-level prose). Feature-grooming rebuild is scoped as follow-on work after the spike succeeds; during the spike, features are dual-written but feature-grooming remains JSON-backed.

**Rationale:**
The epic consolidation is a genuine upgrade, not a compromise. For features, the relate-linked epic-bead model preserves the M:N semantics and prose without losing queryability. Rebuilding feature-grooming against `bd sql` is real work and shouldn't be in scope for a validation spike — defer that rebuild until beads is proven authoritative.

---

### D5: Defer Molecules/Formulas/Gates DAG Engine — DEFERRED

**Research recommended:** Do not adopt the molecules/formulas/gates DAG engine in the same move. It overlaps sprint-planning/sprint-dev orchestration already owned by Momentum, and it is the least mature surface in beads (phased rollout: human=P1, timer=P2, GitHub=P3, cross-rig bead=P4 signals it's newer and less battle-tested). Evaluate separately, later, only if the substrate adoption succeeds.

**Decision:** Deferred. Not in scope for the spike or the authoritative migration. Revisit only after beads substrate is proven.

**Rationale:**
Taking on the DAG engine and the substrate migration simultaneously would couple two uncertain bets. The molecules/formulas surface is the least mature part of beads and directly overlaps Momentum's core orchestration layer. The risk-reward calculus for the spike is better without it.

---

### D6: Wire `bd prime` with `--stealth`/`no-git-ops` — ADOPTED

**Research recommended:** Wire `bd prime` via SessionStart hook with a `.beads/PRIME.md` override carrying Momentum's protocol. Set `no-git-ops`/`--stealth` so beads never autonomously injects `bd dolt push` against the git-discipline rules. Momentum owns sync — beads must not bypass the push-approval gate.

**Decision:** Adopted. The SessionStart hook calls `bd prime` with a Momentum-specific `PRIME.md` override. `no-git-ops` mode is mandatory — Momentum controls all push operations per git-discipline rules.

**Rationale:**
`bd prime` injects "ALWAYS `bd dolt push` at session end" by default — exactly the autonomous push behavior the git-discipline rules prohibit. `--stealth`/`no-git-ops` is the designed mitigation. Not configuring this correctly would immediately violate the push-approval gate on every session that touches beads.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 1 — Spike | Dual-write spike: sprint-manager mirrors to beads; sprint-dev driven by `bd ready`; intake via `discovered-from`; `bd prime` with `--stealth` | Next sprint | beads-dual-write-spike |
| 2 — Gate Evaluation | Assess 4 gate criteria; decide: flip to authoritative or keep JSON model | After spike sprint | — |
| 3 — Authoritative Migration | Retire `index.json`; rebuild feature-grooming/feature-status/canvas over `bd query`; flip beads authoritative | Conditional on Gate 2 passing | TBD post-gate |

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | End of spike sprint | Did `bd ready` + `--claim` simplify sprint-dev Phases 1–3? | Hand-maintained graph logic measurably reduced; no regressions in story scheduling |
| Gate 2 | End of spike sprint | Did `discovered-from` eliminate intake-queue triage toil? | No items lost; triage hop eliminated for at least 1 sprint worth of discovered work |
| Gate 3 | End of spike sprint | Was Dolt sync manageable with git-discipline rules? | `--stealth` mode held; no spurious autonomous pushes; no Dolt/git ref conflicts |
| Gate 4 | End of spike sprint | Did `--spec-id` linkage hold without in-tree metadata loss? | Review/audit workflows unimpaired; story specs reviewable in PR diffs as before |
| Migration Go | After all gate scores | Proceed to authoritative migration? | 3 of 4 gates positive → flip; fewer than 3 → keep JSON model, retain spike's dependency engine only |
