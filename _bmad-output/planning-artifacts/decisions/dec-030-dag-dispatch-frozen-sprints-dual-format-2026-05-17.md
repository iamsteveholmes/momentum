---
id: DEC-030
title: Dependency-Driven Execution Model — DAG Dispatch, Closeable Value-Groupings, Frozen-Scope Sprints, and the Dual-Format Integrity Split
date: '2026-05-17'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-17'
  - path: docs/research/hermes-kanban-discovery-2026-05-17.md
    type: prior-research
    date: '2026-05-17'
  - path: docs/research/beads-vs-momentum-tracker-evaluation-2026-05-16.md
    type: prior-research
    date: '2026-05-16'
  - path: docs/research/beads-dual-write-spike-findings-2026-05-16.md
    type: prior-research
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-028 (Beads as Tracker/Dependency/Memory Substrate — this decision sharpens its §3 epic/feature consolidation, reframed through the category-vs-finishable distinction, and leans on `bd ready` + atomic `--claim` as the deterministic DAG state engine)
  - DEC-029 (Method-Routed Acceptance Validation — DEC-029 explicitly sequenced "the full sprint-dev rewrite" as a downstream decision/epic; this decision is the planning-side execution model that rewrite realizes, composing with DEC-029 D9/D10/D11)
architecture_decisions_affected:
  - UNDETERMINED — story-level and architecture-decision (AD-N) impact is explicitly not assessed; the developer's instruction was that determining blast radius requires a dedicated discovery effort (see "Required Discovery Before Implementation")
---

# DEC-030: Dependency-Driven Execution Model — DAG Dispatch, Closeable Value-Groupings, Frozen-Scope Sprints, and the Dual-Format Integrity Split

## Summary

A working session, seeded by a comparative discovery of the Hermes Kanban board and grounded
in the prior beads evaluation and dual-write spike, traced four artificial-serialization
defects in Momentum's current execution model back to a single root cause: **coarse
containers (waves, serial epics, epic-mapped sprints) imposed as sequencing units on top of a
finer-grained dependency reality.** The net direction is to let the dependency graph schedule
and demote every container to a backward-looking, frozen-scope certification cut. Concretely:
sprint-dev's barrier-synchronized wave fan-out is replaced by **continuous DAG-driven
dispatch** (beads `bd ready` + atomic `--claim` is the deterministic state engine; Momentum
builds the dispatcher loop on top); the dual epic/feature taxonomy collapses into **one
closeable, M:N value-grouping** that certifies a frozen scope, with discovered work flowing
past via `discovered-from` rather than being silently absorbed; the sprint is redefined as a
**frozen-story-scope verification epoch** with an asymmetric (subtract-and-perturb, never-add)
freeze and a behavior/AC-level — not implementation-level — scope boundary; and the
human-in-the-loop "wall of text"/spec-fatigue problem is addressed by a **dual-format
principle with a two-class integrity split** (Class 1 structured-core deterministic
projection; Class 2 narrative verified-non-determinism with a hard decorrelation requirement).
The front-loaded planning cost this implies is accepted as a deliberate trade, and one piece
of net-new tooling — a design-fidelity validator distinct from code review — is committed as
implied scope. The model is decided; its precise story/architecture blast radius is
explicitly **undetermined pending a discovery effort**, and two load-bearing sub-questions
(what hosts the always-on dispatch loop; the how-vs-what adjudication) plus the DEC-028 beads
gamble are recorded as gates rather than resolved here.

---

## Decisions

### D1: Replace barrier-synchronized wave fan-out with DAG-driven continuous dispatch — ADOPTED

**Developer framing:** sprint-dev currently fans out an entire wave at once and must wait for
*every* story in the wave to finish before the next wave; one failure stalls the whole thing.
Kanban gives a DAG that is managed without an agent — agents are incapable of managing the
DAG — so once a story's dependencies finish, the next story can run.

**Decision:** sprint-dev's wave/barrier model is replaced by continuous dependency-driven
dispatch. A story becomes workable the moment its dependencies complete; a failed story
blocks only its transitive dependents, not the sprint. Beads (`bd ready` + atomic `--claim`)
supplies the deterministic DAG state engine — the "DAG without an agent managing it";
Momentum builds the dispatcher loop on top. The always-on-process question (what hosts the
loop, given Momentum has no Hermes-style gateway) is the load-bearing unresolved sub-question
(see Decision Gates).

**Rationale:**
Agents cannot reliably manage a dependency DAG; making the ready-set a deterministic
computation (`bd ready`) removes that failure mode entirely. Continuous dispatch eliminates
the single-failure-stalls-everything defect that motivated the whole inquiry. This continues
the path started by DEC-028 and is the planning-side counterpart of DEC-029's sequenced
sprint-dev rewrite.

---

### D2: Collapse epic + feature into a single closeable, frozen-scope value-grouping — ADOPTED

**Developer framing:** There are two senses of "epic" — a long-lived category, and a serial
finishable body of work — and the serial sense was always closer to a feature. The real pain
is "when is it actually done?": an epic planned with 6 stories grows to 20, never cleanly
finishes, and intake gets jammed into Epic 1 or Epic 2 because the container is treated as a
serial sequencing concept even though the real dependencies are far finer-grained than the
epic level.

**Decision:** Epic and feature are demoted from execution/sequencing containers to
backward-looking **value-views**, and collapsed into one M:N grouping with an explicit
`acceptance_condition`. The grouping closes on a **frozen scope**; work discovered later is
born as a separate node linked `discovered-from` its origin and is never silently absorbed
into an open container. The DAG sequences; the container only reports value and certifies a
frozen scope.

**Rationale:**
"When is it done?" is unanswerable for a container that accretes scope freely; frozen scope
plus `discovered-from` makes it answerable and kills the partially-completed-frankenstein
failure mode. Once both epic and feature are demoted to value-views, maintaining two parallel
taxonomies is redundant. This sharpens DEC-028 §3 — reframed through the
category-vs-finishable lens the prior evaluation did not draw — and rewrites the sprint/epic
model carried in the Momentum redesign.

---

### D3: Redefine the sprint as a frozen-story-scope verification epoch — ADOPTED

**Developer framing:** Sprints shouldn't map to epics; a sprint is more "what you can verify
and close now" — it may close zero epics, one, or advance several. A sprint is story-scoped:
at planning we agree to a grouping of stories, all are created and vetted, and anything
outside that grouping is out of scope. We may drop or modify stories a bit during
implementation, but we cannot add scope outside the grouping.

**Decision:** The sprint is the verification-and-closure epoch of the enforced practice (the
boundary AVFL/review/e2e/retro/distill run against). During sprint planning a story grouping
is agreed; **all stories are created, vetted, and validation-clean before activation**. The
freeze is **asymmetric**: stories may be *dropped* or *perturbed*, scope may **not be added**.
Scope is frozen at the **behavior/AC level, not the implementation level** — a change to a
story's acceptance criteria/behavior is a new story, not a modification (the *how-vs-what*
boundary, adjudicated via change-type classification, enforced at `sprint-manager`). The
dispatcher claims from `bd ready ∩ the frozen sprint set`; a blocked story drops and re-enters
a future sprint via the DAG, so no story can stall a sprint.

**Rationale:**
Sprint-closure and epic-closure become orthogonal cuts on the same flowing DAG, which is what
makes "a sprint may close any number of epics" true rather than contradictory. The frozen,
subtract-only invariant is enforceable at `sprint-manager` — Momentum's enforcement moat;
beads is advisory — and applies, at the sprint level, the same frozen-scope discipline that
fixes epics in D2. Subtract-only plus DAG-reentry is the structural cure for the original
"one failure stalls everything" defect.

---

### D4: Adopt the dual-format principle with a two-class integrity split — ADOPTED

**Developer framing:** AI produces outputs faster than a human can read and reason about them
(spec-fatigue / wall-of-text). Wherever a human makes decisions they should see a
human-optimized format; wherever the LLM reads, it should be LLM-optimized — and it is on us
to own the mappings. Binding human approval to the dense LLM source defeats the entire purpose
of having a summary; the human only ever approves the human-readable format.

**Decision:** Artifacts at human-decision points get human-optimized projections;
LLM-consumed artifacts stay LLM-canonical; Momentum owns the mappings. Integrity is governed
by a **two-class split**:
- **Class 1 (structured/state — kanban / sprint / feature-status dashboards):** a
  format-neutral structured core is canonical; the human render *and* the LLM serialization
  are deterministic projections of it; approval binds to the render *because* it is a
  provable projection of the core (the existing feature-status/canvas pattern).
- **Class 2 (narrative/translation — e.g. HTML design ⇄ DESIGN.md):** no deterministic
  transform exists; accept permanent residual non-determinism and wrap it in
  generate → **decorrelated** verify → discrepancy → human-adjudicate → fix. **Hard
  requirement:** at least one verification leg must be mechanically decorrelated from the
  generator's HTML-comprehension weakness (a deterministic DOM/computed-style extraction as
  the intermediate). The highest-leverage gap-narrowing lever is a **token-driven authored
  design source** (the codebook present in the source).

**Rationale:**
The split is exactly the line Momentum's own change-propagation / bidirectional-reference
research already draws between the known-good and known-failure patterns. Class 2's
decorrelation requirement is what prevents adversarial verification from becoming
correlated-blind theatre where generator and verifier share the same blind spot. This
operationalizes the existing spec-fatigue research and is the evolution of DEC-006's
dual-audience-legibility direction.

---

### D5: Accept front-loaded human-in-the-loop as a deliberate cost — ADOPTED (cost accepted)

**Developer framing:** The price is legit and understood. I want to front-load the human in
the loop pre-sprint and again at verification time, and build tooling (canvas/feature-status
class) that helps the human in the pre-sprint planning phases.

**Decision:** The cost is accepted. The frozen-scope sprint (D3) requires full story
creation, vetting, and validation *before* activation — no starting a sprint with stubs and
fleshing out mid-stream. This concentrates the human-in-the-loop into two gates: **pre-sprint
planning** and **verification/close**. Heavier upfront definition is traded for zero in-sprint
scope creep. A sprint that drops heavily certifies little — a planning-quality signal retro
must surface.

**Rationale:**
This is the same trade that makes frozen-scope epics work: upfront definition buys a
downstream guarantee. The cost is not a separable choice — it is the price of the
scope-creep elimination in D2/D3 — and it is acceptable and understood.

---

### D6: Commit a design-fidelity validator as the net-new tooling the model implies — ADOPTED

**Developer framing:** Could we, not high priority, build a DOM → DESIGN.md transformer? The
discover/understand/validate step and the translate-to-real-components step should be broken
apart so problems are discoverable and fixable, accepting this isn't truly deterministic and
may never be.

**Decision:** The model implies one genuinely new tool: a **design-fidelity validator** for
the Class 2 first leg (HTML-design ⇄ DESIGN.md), distinct from code review (the
DESIGN.md → real-components leg is already covered by Momentum's existing
code-review/e2e/AVFL gates). Its mechanical verification leg is a **deterministic DOM →
structured-design-skeleton extractor** (headless browser; computed styles + layout + a11y
tree, sampled at declared breakpoints/states), buildable with existing chrome-devtools/browser
primitives — **low priority** but coherent as a sub-part of the validator, not a separate
initiative. Human-optimized pre-sprint planning and verification dashboards over beads
(canvas/feature-status class) are the Class 1 tooling surface. A full deterministic
DOM→DESIGN.md transformer is judged infeasible (DESIGN.md is an intent document; recovering
the codebook from rendered output is an under-determined inverse problem) — only the
deterministic extraction half is buildable; the intent half stays Class 2.

**Rationale:**
Without an auditable design-fidelity seam, the Class 2 pipeline has no enforced check and the
quality moat does not extend to design translation. The extractor is precisely the
decorrelation mechanism D4 requires, so it is not optional to the model — only its build
priority is.

---

## Required Discovery Before Implementation

The developer explicitly stated that the story-level and architecture-decision (AD-N) blast
radius of this model is **unknown and requires a dedicated discovery effort** — it must not be
asserted as "none." Treated as a hard precondition, not an afterthought:

- **Story impact** is undetermined. No backlog story slugs are claimed as affected. Discovery
  must enumerate which existing stories this execution-model change touches and which new
  stories it requires (per `feedback_spikes_as_stories`, the discovery itself should be a
  standard story with a committed research artifact, not an informal experiment).
- **Architecture-decision impact** is undetermined. Reconciliation against the inline
  architecture decisions and the related prior decisions — at minimum DEC-004 (feature
  value-first schema), DEC-005 (feature-first cycle), DEC-006 (dual-audience artifact
  legibility), DEC-012 (retired per-sprint state file), and DEC-029 (D9/D10/D11 pipeline and
  state ledger) — is part of the required discovery, not resolved here.
- The model is **decided**; its realization is **blocked on discovery** producing the story
  and architecture map.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 0 | Discovery: enumerate story + architecture-decision blast radius; resolve the always-on dispatch-host question and the how-vs-what adjudication policy | Before any build | (discovery spike — to be created) |
| 1 | DAG-driven dispatcher replacing wave/barrier fan-out (D1); frozen-scope sprint invariant at `sprint-manager` (D3); epic/feature collapse to one closeable value-grouping (D2) | After Phase 0 + gated on DEC-028 spike verdict | (defined by Phase 0) |
| 2 | Dual-format Class 1 tooling — pre-sprint planning + verification dashboards over beads (D4/D5) | After Phase 1 | (defined by Phase 0) |
| 3 | Design-fidelity validator + deterministic DOM-skeleton extractor (D6) | Low priority; after Phase 2 | (defined by Phase 0) |

This decision is the planning-side execution model that DEC-029's deliberately-sequenced
"full sprint-dev rewrite" downstream epic realizes; the two compose (DEC-029 D9/D10/D11 supply
the validate-fix pipeline and state-ledger abstraction this dispatch model runs within).

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | Phase 0 | What hosts the always-on dispatch loop? | A decision among in-session orchestrator loop / harness-level loop / external background process, with the context-drift and cost tradeoffs resolved — Momentum has no Hermes-style gateway, so this is net-new and load-bearing |
| Gate 2 | Phase 0 | How is "modification vs. new story" adjudicated? | The how-vs-what boundary specified as a change-type-classification policy enforced at `sprint-manager` (the one specified-but-tight sub-policy of D3) |
| Gate 3 | Before Phase 1 | Did the DEC-028 beads spike return go? | DEC-028 gate criteria met; the dispatcher leans on `bd ready` + `--claim`, but per the DEC-029 D11 boundary must not hard-depend on beads before the spike verdict — beads-backed if it lands, ledger-abstracted otherwise |
| Gate 4 | Phase 1 | Does subtract-only + DAG-reentry actually prevent sprint stalls on a real sprint? | One real sprint runs with continuous dispatch and a failed/blocked story drops and re-enters without stalling the sprint or growing its frozen scope |
