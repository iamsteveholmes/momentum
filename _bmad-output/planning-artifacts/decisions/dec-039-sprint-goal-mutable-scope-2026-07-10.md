---
id: DEC-039
title: Sprint Goal + Goal-Criticality Scope Mutability — Amending the DEC-030 Never-Add Freeze
date: '2026-07-10'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-07-10'
prior_decisions_reviewed:
  - DEC-030 (Dependency-Driven Execution Model — D3 frozen-story-scope verification epoch, amended by this decision; D2 discovered-from/never-silently-absorbed mechanism preserved)
  - DEC-036 (Conduct HITL Calibration — pause-ask surface contract reused as the escalation vehicle for tier-c routing)
architecture_decisions_affected:
  - DEC-030 — AMENDED — D3's asymmetric freeze ("scope may not be added") no longer holds for goal-critical work admitted via the D2 routing matrix; subtract-and-perturb, the behavior/AC-level scope boundary, how-vs-what adjudication, and D2's discovered-from linkage all stand.
  - DEC-036 — COMPOSES — the pause-ask surface contract (what/why/evidence + options) is the escalation vehicle for tier (c)/(d) routing; no change to the contract itself.
---

# DEC-039: Sprint Goal + Goal-Criticality Scope Mutability — Amending the DEC-030 Never-Add Freeze

## Summary

Two consecutive product sprints (nornspun, chorgi) delivered the full scope of their stories
while failing to deliver anything useful — the chorgi sprint shipped an Android build broken
by a pre-existing overlay bug that was dispositioned `triaged-out` ("Outside scope; not
actioned", conductor escalation table) because it belonged to no story. The root cause is
structural: sprint-planning captures no sprint-level goal, and DEC-030 D3's asymmetric freeze
("stories may be dropped or perturbed, scope may **not** be added") makes goal-critical
discovered work inadmissible by definition. The result is a punt cascade — each sprint defers
newly discovered necessary work to the next, which also fails to deliver, and so on. This
decision introduces a sprint goal as the true definition of done, a four-tier goal-criticality
routing matrix for conduct-discovered work (including autonomous auto-pull for work the
upstream artifacts already account for), a dual end-gate verdict (stories delivered AND goal
delivered), and a standing preference to always deliver the full goal — punting only when the
work is unnecessary or impractical. DEC-030 D3's never-add invariant is amended accordingly;
its D2 mechanism (discovered work born as its own node, linked `discovered-from`, never
silently absorbed) is preserved — auto-pull is loud absorption, cited and end-gate-reported.

---

## Decisions

### D1: Sprint goal statement captured at planning — ADOPTED

**Developer framing:** Each sprint should be planned with a goal — something simple,
expressible in one to a few sentences, e.g. "This sprint will allow a user to create a
character limited to name, ancestry, class, class feature, and feats for first level."
Meeting each story's acceptance criteria is part of the goal, but there is a higher-level
goal the sprint answers to.

**Decision:** Every sprint gets a one-to-few-sentence goal captured during sprint-planning,
stored in the sprint record (`.momentum/sprints/index.json` entry), and approved at the
plan gate. Stories are the current best decomposition of the goal — not the definition of
done.

**Rationale:**
Nothing in the current cycle answers to a sprint-level outcome. A sprint whose every story
passes can still ship a broken product, and the system has no vocabulary to even express
that failure. The goal is what the developer actually approves at the plan gate; the story
set is the plan for reaching it.

---

### D2: Goal-criticality routing matrix for conduct-discovered work — ADOPTED

**Developer framing:** Small, low-risk stories where the decision has clearly already been
made — the design accounts for it, the architecture accounts for it, we just didn't have a
story — should be pulled in automatically. If we hadn't figured it out, or it requires a
significant change to upstream artifacts, that should be discussed with the developer. If
it's just too big, the developer ultimately decides. Bugs we discover that aren't necessary
to deliver the goal get punted.

**Decision:** Work discovered during conduct routes through a four-tier matrix keyed on two
questions — *is it needed for the goal?* and *is it already designed?*

| Tier | Condition | Route |
|---|---|---|
| (a) | Not goal-critical | Punt to backlog via triage, always — regardless of how easy the fix would be. Necessity, not convenience, earns entry into the sprint. |
| (b) | Goal-critical + already accounted for in design/architecture/PRD | Auto-pull autonomously. The conductor MUST cite the covering artifact section — no citation, no auto-pull. Story is born with a `discovered-from` edge and every pulled-in story is reported at the end-gate with its citation. |
| (c) | Goal-critical + undesigned, or requires upstream artifact changes (PRD/architecture/UX) | Pause-ask escalation (DEC-036 surface contract: what/why/evidence + size estimate). Developer rules. Design-on-the-fly is permitted when practical. |
| (d) | Goal-critical + too big (a huge undesigned mass) | Conductor recommends a new sprint, with a size estimate. Developer ultimately decides — if the developer says drive on, we drive. |

**Rationale:**
Admitting goal-critical work is a practical consideration: if we can design and execute on
the fly, we go for it; if it's a huge amount of undesigned work, it belongs in its own
sprint. The citation test in tier (b) is the guard against scope creep dressed up as
"clearly implied" — an agent that cannot point at the artifact that made the decision does
not get to claim the decision was made; it escalates instead.

---

### D3: End-gate dual verdict — stories delivered AND goal delivered — ADOPTED

**Developer framing:** If we weren't able to deliver the goal we would consider the sprint a
failure and try to determine why we missed such an enormous chunk of functionality needed to
deliver on the goal of the sprint.

**Decision:** The conduct end-gate renders two distinct verdicts: (1) stories delivered —
the existing per-story AC verdict — and (2) goal delivered. A sprint can pass the first and
fail the second. When goal-critical work is punted via tier (d), the sprint fails its goal
verdict and retro owes a root-cause analysis on how planning missed a goal-critical chunk
that large.

**Rationale:**
The chorgi case — broken build, all ACs green — is invisible today. Making goal delivery a
first-class verdict makes the sprint's actual purpose auditable and gives retro a concrete
failure to trace upstream.

---

### D4: Goal-delivery preference — sprint scope is mutable in service of the goal — ADOPTED (amends DEC-030 D3)

**Developer framing:** If the scope of a sprint has a HARD limit defined during sprint
planning then your sprints never deliver anything. The newly discovered scope gets punted to
the next sprint which has similar issues, and so on. The preference is ALWAYS to deliver the
full goal of the sprint — we punt only if necessary OR if it's really just not necessary.

**Decision:** The standing preference is always to deliver the full sprint goal. Sprint
scope may mutate during conduct when discovered work is judged necessary to deliver the goal,
via the D2 matrix. This amends DEC-030 D3's asymmetric freeze: "scope may **not** be added"
no longer holds for goal-critical work admitted through the matrix. The rest of DEC-030 D3
stands — subtract-and-perturb remains legal, the behavior/AC-level scope boundary and
how-vs-what adjudication remain, and DEC-030 D2's discovered-from linkage remains the birth
mechanism for all discovered work (auto-pulled or punted).

**Rationale:**
The frozen-scope invariant was the structural cure for "one failure stalls everything," but
applied as an absolute it produces the punt cascade: sprints that always complete and never
deliver. Mutability is bounded — only goal-critical work enters, the citation test gates
autonomy, the developer gates everything undesigned or large — so the original defect
(unbounded silent scope growth) does not return.

---

## Affected Surfaces

Implementation lands as stories (created at sprint-planning / triage, not here):

- **sprint-planning** — goal elicitation + storage in sprint record; goal on the plan gate surface
- **conductor** — D2 routing matrix in escalation flow (the `triaged-out` disposition gains the goal-criticality test); auto-pull machinery; end-gate dual verdict + pulled-in-story reporting with citations
- **sprint-manager** — sprint record schema gains `goal` field; admission of mid-sprint stories under tier (b)/(c)/(d) rulings
- **retro** — goal-verdict root-cause obligation when a sprint fails its goal
