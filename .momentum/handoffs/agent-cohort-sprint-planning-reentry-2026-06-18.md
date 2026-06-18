# Re-entry — Agent-Cohort Sprint-Planning (keystone-first)

**Date:** 2026-06-18
**Purpose:** Pick-up point for a **fresh session** to run keystone-first sprint-planning for the
agent cohort (Path A). The prior session ran a full `momentum:refine` pass that cleared the
runway; this doc captures what changed and what to plan. Per the fresh-session-before-major-
workflows practice: `/plugin marketplace update momentum` + restart, then run sprint-planning.

> Open re-entry — get your bearings from the state below, then **plan with the developer**.
> The scope is proposed, not fixed.

---

## What the last session did (a full `momentum:refine` pass)

All committed and pushed.

1. **Planning artifacts reconciled to DEC-038** — `architecture.md` (+9 edits: canonical
   manifesto = diagnostic-table definition for DEC-026 D4, per-agent routing ownership,
   wiki-query multi-KB cold interface / DEC-018 extended, project-scoped agents,
   `manifesto_inputs`→`manifesto`+`creed_anchors` split, repo-tree refresh) and `prd.md`
   (+11 edits: FR136/FR138 rewritten to diagnostic-table, **new FR142** multi-KB architecture,
   distill-removal + Impetus-always-on corrections, stale section-note refreshes). → commit `ab177aa`
2. **Epic restructuring** (epic-grooming found the DEC-038 cohort was *misfiled*, not legitimately
   split) — 37 story moves: 20 composition stories → `momentum-agent-composition-pipeline` (now
   **22 active**, was 2 stubs); 17 base-body/agent-definition stories → `momentum-agent-role-contracts`
   (now **18**, was 1). `momentum-agent-spawn-orchestration` is now true spawn-reliability scope
   (**31**, was 67). Also: merged `assessment-decision-pipeline` → `provenance-chain`; re-scoped
   `startup-performance` → benchmark-and-eval-harness (slug retained); reconciled `epics.json`
   counts to the live index. Dropped `multi-model-research-workflow-active` (superseded by 8-1/8-2/8-3);
   promoted `agent-spawn-observability-metric` low→medium. → commit `76f1d11`
3. **5 DEC-038 `stories_affected` aligned** to the manifesto-as-diagnostic-table definition (via
   targeted spec edits, not create-story). The keystone `build-guidelines-skill` now encodes
   **Gate G1** (write + register one composed agent in `agents.json`, validate vs the cmp-dev
   exemplar). → commit `28e10c7`
4. **3 conduct sub-skill fix stubs filed** (from the 2026-06-14 `conduct-subskills-audit`) in
   `momentum-sprint-orchestration` → commits `c37c969`, `dde4f5b`, `6d4f798`:
   - `conduct-assign-finding-id-before-directed-fix-invocation` **(critical)** — the contract bug:
     directed fixer invoked (`workflow.md:956`) with findings lacking `finding_id`.
   - `conduct-ledger-append-site-dedup-guards` **(high)** — 7 append sites skip the `:404`
     `(story_slug, event, finding_id)` dedup guard; `:404` also omits `stage3-mid-flight-escalation`.
   - `conduct-resume-and-rehydration-idempotency-hardening` **(high)** — REHYDRATION EXEMPTION not
     restated inline; avfl/e2e rehydration no dedup; Phase 5 has no completion checkpoint/event;
     `{{build_cross_artifact_notes}}` accumulator re-init unguarded.

## Next step — keystone-first sprint-planning

The decided path (developer): **story the conduct fixes (done), then plan.** Run
`momentum:sprint-planning` scoped **keystone-first** — prove the pipeline produces ONE composed
agent (Gate G1) before committing to the full 40-story cohort.

**Proposed sprint scope (refine in planning):**
- `build-guidelines-skill` **[C]** — the keystone (the missing build-agents orchestrator).
- Prerequisites to reach G1: `agent-manifesto-format-specification` **[H]**,
  `constitution-builder-write-mode-parameterization` **[M]**,
  `constitutionmd-generation-acceptance-criteria` **[H]**,
  `wiki-query-interface-block-for-hot-constitution` **[M]**, `nornspun-agent-constitution` **[M]**.
- The 3 conduct fixes (ride along): `conduct-assign-finding-id-before-directed-fix-invocation` **[C]**,
  `conduct-ledger-append-site-dedup-guards` **[H]**, `conduct-resume-and-rehydration-idempotency-hardening` **[H]**.

**Caveat for planning:** the cohort stories carry **no encoded `depends_on` edges** yet — "ready"
in the index means "no recorded blocker," not true independence. The real build order
(constitution-builder + manifesto-format before the keystone can prove G1) must be set during
planning. The 3 conduct stubs are intake stubs — `momentum:create-story` will enrich them to
dev-ready before/at planning.

## Open threads (unchanged or newly surfaced — explore, don't resolve)

- **G2 fork** (DEC-038): hand-authored vs. generate-then-curate manifesto. Gates Phase-3
  `manifesto-builder-skill-generate-then-curate`, **not** the keystone.
- **Is "SM" a real spawnable role?** `sm-base-body` now sits in `momentum-agent-role-contracts`.
- **Momentum's own KB** — `momentum-knowledge-base-buildout` (Phase 3) is what a manifesto's
  diagnostic table actually queries against.
- **DEC-028 beads → Dolt Migration Go/no-go** — refine flagged this gate as **ready** (spike done).
  Consequential, deserves its own decision moment.
- **Deferred refine item:** the `momentum-impetus-session-orientation` split (E3, ~70 stories — a
  second residue-catcher). Needs its own scoped pass; no moves enumerated yet.
- **Nits:** assessments `index.md` shows AES-003 `decisions_produced=[]` while the file lists
  `[DEC-033, DEC-034]` (stale index); 3 decision annotations name never-created stories
  (`architect-writer`, agent-guidelines retirement, `skill-agent-story-spec-mig-template`).

## How to begin

`/plugin marketplace update momentum`, restart, then run `momentum:sprint-planning` over the
proposed scope above — keystone-first. Follow the developer's lead on final scope.

---

### State as of session change
- Refine pass (planning artifacts, epic restructuring, 5 spec alignments) — committed & pushed.
- 3 conduct-fix stubs — committed & pushed.
- This handoff — committed & pushed.
- No active or planning sprint. Backlog: 280 active (278 + 3 new − 1 dropped).
