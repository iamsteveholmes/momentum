---
id: DEC-035
title: Conduct Execution Engine — In-Session Dynamic Workflows, Feature-Grained HITL, Gas City Deferred
date: '2026-05-30'
status: decided
source_research:
  - path: .momentum/handoffs/momentum-execution-architecture-brief-2026-05-29.html
    type: prior-research
    date: '2026-05-29'
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-30'
prior_decisions_reviewed:
  - DEC-028 (Beads as Tracker/Dependency/Memory Substrate — beads decoupled from conduct; the dual-write spike continues independently)
  - DEC-029 (Method-Routed Acceptance Validation — conduct realizes the unified validate-fix pipeline; uses the D11 ledger-abstracted fallback, no hard beads dependency)
  - DEC-030 (Dependency-Driven Execution Model — amended: HITL unit and story-count cap)
  - DEC-031 (Legibility-Before-Automation — amended: dispatcher reframed, plan-gate legibility sequenced separately)
  - DEC-032 (Gas City as Momentum's Dispatcher — superseded by this decision)
  - DEC-034 (Epic-Layer Consolidation — the finite-lived epic is the HITL unit)
architecture_decisions_affected:
  - DEC-032 — SUPERSEDED — Gas City demoted from "the dispatcher" to a deferred option; in-session dynamic Workflows are the execution substrate. Revisit Gas City only on an out-of-session / multi-Conductor goal.
  - DEC-030 — AMENDED — the unit the human plans-and-evaluates becomes a finite-lived epic / complete feature, not a sprint batch; the 2–8 story-count cap is removed; continuous DAG dispatch is realized in-session via dynamic Workflows (honors the Gate-1 in-session ruling).
  - DEC-031 — AMENDED — D8's deferred Claude-native dispatcher is reframed: the in-session Conductor IS the dispatcher; Gas City's Version-A out-of-session trigger stays deferred. Plan-gate legibility (D2 canvas Reviewer tab + sprint-planning plain-language output) is sequenced as its own separate epic, accepted as a known ordering tension with D1.
  - DEC-028 — COMPOSES (unaffected) — beads is not coupled to conduct; conduct uses the index.json/depends_on frontier. The beads dual-write spike proceeds on its own gates.
  - DEC-029 — COMPOSES — conduct is the in-session realization of the three-tier validate-fix pipeline; per D11 the loop does not hard-depend on beads before the spike verdict.
  - DEC-034 — COMPOSES — the finite-lived epic (forward-looking, carrying an acceptance_condition) is the unit conduct evaluates against.
---

# DEC-035: Conduct Execution Engine — In-Session Dynamic Workflows, Feature-Grained HITL, Gas City Deferred

## Summary

A 15-agent discovery → council → synthesis deliberation (full brief at
`.momentum/handoffs/momentum-execution-architecture-brief-2026-05-29.html`), followed by developer
ratification, settled the open question of how Momentum should execute work — reconciling the
conduct sprint-dev rewrite against the prior beads/Gas-City/DAG-dispatch decision line
(DEC-028/030/031/032). The deciding input was the developer's stated goal: **high throughput with
deep delegation** (agents handle what the developer won't), evaluated at the **bigger-picture /
complete-feature grain** rather than as a stream of small in-session steps — and explicitly **no
out-of-session / away-from-keyboard dispatch yet**.

That goal resolves the substrate question decisively. Gas City's only advantage over the dynamic
Workflow tool is out-of-session dispatch; in-session it reduces to "removes typing the slash
command" and contradicts DEC-030 Gate 1 (which ruled dispatch must be in-session because agent
spawning is a session-bound tool call). With out-of-session deferred, **conduct — built on the
in-session dynamic Workflow tool — is adopted as Momentum's execution engine**, Gas City is
deferred (superseding DEC-032's "Gas City as the dispatcher"), and beads is decoupled (kept as an
independent spike). The unit the human plans and evaluates becomes a **finite-lived epic / complete
feature** rather than a 2–8 story sprint batch, and the **arbitrary story-count cap is removed** —
the unit is whatever the feature requires. The end-gate report is organized by **user-facing
functionality and divergences from plan**, not by story count or implementation detail, and the
autonomous auto-fix loop must surface **what it changed and dismissed, human-readable, in full
context**. The decision is made; the conduct spec's own ten open questions, the Conductor
context-budget handling (a build implementation detail), and the rework-tail risk
(accept-and-adapt) are carried forward, not resolved here.

---

## Decisions

### D1: Adopt conduct as Momentum's execution engine — ADOPTED

**Recommended:** The council's modal lean (~60%) was "conduct-first, dispatcher-deferred" — ship the
in-session Conductor / dynamic-Workflows execution model: a top-level-session Conductor runs each
story's pipeline (dev → concurrent QA + `bmad-code-review` → fix → self-merge), then AVFL-on-merge,
E2E, and a single self-sufficient HTML end-gate, removing all intermediate gates.

**Decision:** Adopted. Conduct (the sprint-dev rewrite) is Momentum's execution engine, built on the
in-session dynamic Workflow tool, with one human gate at the end.

**Rationale:** It directly answers the developer's two goals — it collapses the in-session firehose
(5 asks + 2 fix-loop asks + 8 HALTs) into a single gate (the dominant pain: "a million little
steps"), and its autonomous build delegates the work the developer doesn't want to handle.
Throughput comes from fanning story pipelines out in-session — no out-of-session capability is
required to achieve it.

### D2: In-session dynamic Workflows are the substrate; Gas City deferred; beads decoupled — ADAPTED

**Recommended:** Reconcile the conduct approach against DEC-032 (Gas City) and DEC-028 (beads). The
brief found the three substrates compose at different layers (Workflows = in-session execution;
beads = persistent DAG/state; Gas City = out-of-session trigger) and flagged that conduct silently
hollowed out DEC-032 unless formally reconciled.

**Decision:** Adopted in adapted form. Execution substrate = the in-session dynamic Workflow tool.
**Gas City is deferred** — this supersedes DEC-032's adoption of Gas City as *the* dispatcher;
revisit only if/when an out-of-session or multi-Conductor goal appears. **Beads is decoupled from
conduct** — conduct uses the `index.json`/`depends_on` frontier (DEC-029 D11's ledger-abstracted
fallback); the beads dual-write spike continues independently on its own gates (DEC-028 unchanged).

**Rationale:** Gas City's sole advantage over dynamic Workflows is out-of-session dispatch, which the
developer is explicitly not pursuing yet; in-session it adds maturity tax (Dolt, MCP-not-ready,
open wedge/race bugs) for near-zero value and contradicts DEC-030 Gate 1. Beads' headline win —
atomic `--claim` against concurrent dispatchers — only matters out-of-session / multi-Conductor; for
a solo, single in-session Conductor the frontier is trivially computable from `depends_on`, so
coupling now would take on a mid-spike Dolt dependency for marginal gain.

### D3: The HITL plan-and-evaluate unit is a finite-lived epic / complete feature — ADAPTED

**Recommended:** The council's modal answer was SPRINT as the HITL unit (story for execution). The
devil's advocate and the synthesis showed the epic-as-unit option was dismissed on a verified-false
premise (DEC-034 makes finite-lived epics forward-looking, carrying a real `acceptance_condition`)
and that "sprint" silently bundled planning-grain and integration-review-grain.

**Decision:** Adopted in adapted form (amending DEC-030's sprint-as-unit framing). The unit the human
plans and evaluates is a **finite-lived epic / complete feature**, evaluated against its
`acceptance_condition` ("did the feature land?"). Story-grained continuous dispatch remains the
execution model *within* that unit.

**Rationale:** The developer's goal is to evaluate the bigger picture — one complete piece of
functionality — not a stream of fragments or a million little reviews. A finite-lived epic carries a
real acceptance condition a sprint lacks, making "did it land?" a more meaningful gate than "is this
changeset correct?"

### D4: Remove the arbitrary story-count cap — ADOPTED

**Recommended:** DEC-030 carried a 2–8 story bound on the planning/evaluation unit.

**Decision:** Adopted (amending DEC-030). The arbitrary story-count cap is removed. The unit is the
whole feature, however many stories that requires. A practical ceiling is revisited only if one is
hit in practice.

**Rationale:** If the unit is a complete feature, its size is whatever the feature needs — not a
number picked in advance. The scope is still established upstream at planning (out of conduct's
scope); conduct simply accepts the story set it is handed without an input-size limit.

### D5: The autonomous auto-fix loop must be legible in the report — ADOPTED

**Recommended:** Conduct's "always auto-fix every legitimate finding" loop moves the largest volume
of consequential judgment out of the human's view, in tension with the comprehension mandate.

**Decision:** Adopted. The auto-fix loop stays autonomous, but the end-gate report must show **what
the fixer changed and what it dismissed** — human-readable, full context — not just a curated
end-state.

**Rationale:** Hiding the fix/dismiss decisions would relocate the firehose into an invisible
autonomous span. Surfacing them legibly preserves comprehension while keeping the build autonomous.

### D6: The end-gate report is organized by user-facing functionality, not story detail — ADOPTED

**Recommended:** Report size and legibility were flagged as risks if the report dumps per-story
detail at uncapped scale.

**Decision:** Adopted. The report's spine is **user-facing functionality plus divergences from
plan**. Clean, on-plan stories collapse to a line; stories that diverged significantly expand with
full context and must be dealt with. Report length tracks the functionality surface, not story
volume.

**Rationale:** The developer should evaluate complete functionality without being bogged down in
detail. A feature with a small surface (e.g. campaign-init) yields a small report regardless of how
many stories built it; divergences are where attention is genuinely needed.

### D7: Plan-gate legibility is a separate, deferred epic — DEFERRED

**Recommended:** DEC-031 D1 names the plan-approval gate as the more porous one; the brief warned
that shipping execution automation while the plan gate stays illegible is the inversion DEC-031
forbids, and recommended folding plan-gate legibility (canvas Reviewer tab, sprint-planning
plain-language output) into the conduct work.

**Decision:** Deferred. Plan-gate legibility is its own epic, not part of the conduct build. Conduct
ships with end-gate (verification) report legibility; the canvas Planner/Reviewer legibility work
(DEC-031 D2) is sequenced separately.

**Rationale:** "We can't fix everything at once — planning is a different epic." The developer
accepts the known sequencing tension with DEC-031 D1; conduct is an executor and planning is
upstream and out of its scope.

### D8: Validate DEC-030 Gate 4 in the first real conduct run — ADOPTED

**Recommended:** DEC-030 Gate 4 (subtract-only freeze + drop-and-reenter prevents sprint stalls) is
OPEN and has never run on a real sprint; the brief asked whether to validate it on the current loop
before committing the rewrite.

**Decision:** Adopted. Gate 4 is validated *in the first real conduct run*, not via a separate sprint
on the old sprint-dev loop.

**Rationale:** Spending a sprint on the painful old model to test a narrow invariant is not worth it;
the first conduct run exercises the model directly and proves Gate 4 in context.

---

## Phased Implementation Plan

| Phase | Focus | Notes |
|-------|-------|-------|
| 0 — Reconcile (this decision) | Record DEC-035 superseding DEC-032 and amending DEC-030/031 | Done on the record so the practice's decision-legibility discipline holds |
| 1 — Ratify conduct's open questions | Walk the conduct spec's 10 open questions (`sprint-dev-redesign-spec.md` §13); several are now answered by D1–D8 | Especially Q6 (Conductor = top-level session — confirmed by D1/D2) |
| 2 — Story breakdown | Turn the (revised) conduct spec into the epic/story breakdown; build order per the spec's §10 gap map | The 3 P0 agents: Conductor, fixer-via-directed-`momentum:dev`, `code-reviewer`→`bmad-code-review` adapter |
| 3 — First conduct run | Execute one real feature under conduct; validate Gate 4 (D8) in context | Watch the Conductor context-budget (structured-output subagents + persisted data model) |

Plan-gate legibility (DEC-031 D2 canvas epic) and the beads dual-write spike (DEC-028) proceed as
independent, parallel efforts — neither gates the conduct build.

---

## Carried Forward (not decided here)

- **Conduct's 10 open questions** (spec §13) — to be ratified next; D1–D8 answer several.
- **Conductor context-budget** — treated as a build implementation detail, not a developer
  constraint: mitigated by subagents doing the heavy work in their own contexts and returning
  structured results, with the report rendered from a persisted data model rather than the session's
  accumulated memory. A checkpoint/compaction strategy is specified during the build.
- **Rework-tail risk** — accepted as a learn-in-practice concern; whether feature-grained evaluation
  helps or hurts the rework tail is revisited after the first real run.
