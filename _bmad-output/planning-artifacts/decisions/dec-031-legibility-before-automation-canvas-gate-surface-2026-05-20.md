---
id: DEC-031
title: Legibility-Before-Automation — Canvas Gate Surface, Pipeline Restructure, and Dispatcher Sequencing
date: '2026-05-20'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-20'
  - path: .momentum/handoffs/hermes-dispatcher-research-state-dispatch-2026-05-18.md
    type: prior-research
    date: '2026-05-18'
  - path: docs/research/hermes-claude-dispatcher-momentum-2026-05-18-final.md
    type: prior-research
    date: '2026-05-18'
  - path: docs/research/claude-code-background-dispatcher-2026-05-17.md
    type: prior-research
    date: '2026-05-17'
prior_decisions_reviewed:
  - DEC-005 (Momentum Cycle Redesign — D12 "Distill fires continuously on hooks" is overturned by D6)
  - DEC-006 (Artifact Redesign for Dual-Audience Legibility — D1/D2 extend the dual-audience lineage into the gate-review surface)
  - DEC-007 (Triage Capture Artifact / Intake-Queue JSONL — D5 adds retro as an additional triage caller)
  - DEC-011 (Project Canvas Implementation Foundations — D2 builds the Reviewer tab on the canvas DEC-011 founded)
  - DEC-017 (Momentum Practice Cycle Step Sequence — D3/D6 restructure sprint-dev internals and remove distill from the cycle description)
  - DEC-019 (Hono+HTMX+Bun Canvas Runtime Stack — context only; D2 builds new behavior on the unchanged stack)
  - DEC-027 (Skill-Creator Pipeline + Change-Type Routing in Sprint-Dev — D3 restructures the routing-target pipeline; D6's fix-as-story lane runs on it)
  - DEC-028 (Beads Adoption — context only; D2's epic/feature taxonomy merge touches beads-tracked items, DEC-028 itself unaffected)
  - DEC-029 (Method-Routed Acceptance Validation — DEC-029 D4 sequenced the sprint-dev rewrite as a downstream decision; DEC-031 is part of that downstream)
  - DEC-030 (DAG Dispatch, Frozen Sprints, Dual-Format Integrity Split — D2/D4/D8 operationalize its planning/verification touchpoints and dispatcher gate)
architecture_decisions_affected:
  - Decision 27 (Transcript Audit Retro) — AMENDED by D5/D6 — distill removed from retro Phase 5; retro becomes an additional caller of standalone triage
  - Decision 28 (Triage vs Refinement Distinction) — AMENDED by D5 and D6 — dedup/consolidation become mandatory triage behaviors and retro becomes a caller (D5); the DISTILL class loses its executor and needs redesign or removal (D6)
  - Decision 31 (AVFL at Sprint Level) — AMENDED by D3 — AVFL stays a subskill inside the single autonomous span alongside merge and the new E2E step
  - Decision 34 (AVFL Scan Profile and Hybrid Resolution Team) — AMENDED by D3/D4 — QA and code-review move into momentum:dev; E2E Validator restructured into the dev span and the verification gate
  - Decision 36 (Sprint Lifecycle State Machine) — AMENDED by D4 and D2 — verification becomes the hardest human gate (done→completed and push-on-verification mechanics restructured); canvas renders planning-state sprints
  - Decision 41 (Workflow Team Composition Declarations) — AMENDED by D3 — QA and code-review move into momentum:dev; Phase-5 team-review composition restructured
  - Decision 42 (Distill Execution Path and AVFL Profile) — SUPERSEDED by D6 — momentum:distill is removed entirely
  - Decision 43 (Retro Phase 0: Session Analytics and Regression Detection) — AMENDED by D6 — momentum:distill is removed as an authorized findings-ledger writer
  - Decision 49 (Feature Grooming Skill) — AMENDED by D2 — the epic/feature taxonomy merge touches feature-grooming's taxonomy ownership
  - Decision 53 (Canonical Momentum Cycle Step Sequence) — UNCHANGED — D3/D5/D6 restructure step internals; the canonical step sequence is unaffected
  - Decision 54 (Hono+HTMX+Bun Canvas Runtime Stack) — BUILT UPON by D2 — the Reviewer tab and new features run on the existing stack; the stack decision is unchanged
  - Decisions 45/46/48 (Feature Status skill / cache / practice project detection) — UNCHANGED — already superseded by DEC-019; D2 builds on the canvas
stories_affected:
  - epic-feature-collapse-closeable-grouping
  - change-type-routing-in-sprint-dev
  - code-reviewer-agent-definition
  - sprint-dev-composed-file-spawn-wiring
  - sprint-dev-phase-7-gate
  - sprint-dev-fixture-autonomous-commit-per-story
  - avfl-invoke-code-reviewer-via-skill-not-task
  - specialist-agents-avfl-and-quickfix-phase2a
  - avfl-migration-story-exhaustive-call-site-audit
  - dev-fixer-agent-definition
  - retro-prior-action-item-cross-ref
  - dag-dispatcher-loop
---

# DEC-031: Legibility-Before-Automation — Canvas Gate Surface, Pipeline Restructure, and Dispatcher Sequencing

## Summary

A working session, opened by the 2026-05-18 Hermes-dispatcher handoff and its question of where a background dispatcher should sit, reframed the whole inquiry: the bottleneck Momentum faces at its human-in-the-loop gates is not gate *placement* but gate *efficacy*. The gates already sit in the right places — the developer reviews create-story input, the sprint plan, and verification — but they are porous, because the gated artifacts are LLM-oriented (jargon-dense, GUID-like slugs, context-stripped) and the developer is fast-tracking through them without genuinely catching problems. The governing principle adopted is **legibility before automation**: making gated artifacts human-legible is the engineering deliverable, and automating execution before the gates are legible is explicitly disallowed because it would amplify the failure — delivering more unreviewable work, faster. The legibility layer is not a new artifact: the existing `momentum:canvas` evolves into the gate-review surface, restructured as a **Planner tab** (its original purpose) and a new **Reviewer tab** carrying an active "what you're attesting to" strip — an epic-sized initiative. Around that, the pipeline model is corrected: Sprint-Dev / Merge / AVFL / E2E form one autonomous span between two human gates, composed of distinct subskills, with QA and code-review pulled into `momentum:dev` so every caller inherits them; verification is named the hardest human gate and the true trigger for push, with its manual content project-defined rather than baked into Momentum. `momentum:triage` stays standalone and anytime-callable with retro added as a caller and dedup/consolidation made mandatory; `momentum:distill` is removed outright, its slowness-exposing absence accepted as a deliberate forcing function. Hermes-as-dispatcher is rejected on the prior research; the Claude-native dispatcher is deferred and explicitly blocked on the canvas legibility epic, to ship as Version A only when unblocked. Eight decisions, all decided; the dispatcher is the one deferred element, gated on the legibility epic.

---

## Decisions

### D1: Legibility-Before-Automation as the governing principle — ADOPTED

**Developer framing:** The danger at a human gate is not that an unreviewed artifact contains errors or poor decisions — it is that the human *does not catch them*. The gates exist and sit in the right places, but the developer is fast-tracking through things he cannot genuinely understand: stories built like GUIDs, unique but not meant for human consumption, full of jargon and assumptions, lacking context. The markdown artifacts are too LLM-oriented. Everywhere there is a human gate, there needs to be a better way to review.

**Decision:** Adopted as the governing principle for all downstream automation work. The engineering deliverable is the **legibility of gated artifacts** — not the placement of gates, which is already correct. Automating pipeline execution before the gates are legible is explicitly disallowed: it would amplify the failure mode rather than relieve it.

**Rationale:**
The gates are not mis-placed; they are porous because the artifacts are unreadable. Building automation that produces more such artifacts, faster, makes the catch-rate worse — a faster firehose of unreviewable work means more blind fast-tracking, not less. Legibility is therefore the strict prerequisite for any dispatcher or background-automation effort. This is the principle that orders the rest of this decision: D2 is the legibility layer, and D8 (the dispatcher) is explicitly sequenced behind it.

---

### D2: Canvas evolves into the gate-review surface — Planner + Reviewer tabs — ADOPTED

**Developer framing:** Reuse the existing `momentum:canvas` rather than build a new review artifact. The canvas is already a planner — that is what it was always meant to be — and it is good at looking at stories. Rethink it as both planner and reviewer, with two tabs: the first tab is the Planner; a second tab is the Reviewer. It must also be updated for the new epic/feature merge for beads, and must render a sprint that is in planning state, not just active or done. The "what's unusual / what you're attesting to" strip is in scope.

**Decision:** Adopted as an **epic**. `momentum:canvas` becomes the gate-review surface, restructured into two tabs — **Planner** (the canvas's original purpose) and **Reviewer** (new, the gate surface). The Reviewer-tab epic scope:
- Render **planning-state sprints** so a sprint can be reviewed mid-planning, not only when active or done.
- Absorb the **epic/feature taxonomy merge for beads** (the `epic-feature-collapse-closeable-grouping` story is the vehicle; touches `feature-grooming`'s taxonomy ownership).
- Surface **E2E plans** (at the sprint-plan gate) and **verification status** (at the verification gate).
- Carry a per-gated-item **"what's unusual / what you're attesting to" strip** — active review prompts, not passive rendering.
- `momentum:sprint-planning` grows a new output: a plain-language **"what this functionality is" description** per story, displayed on the canvas and consumed at both the plan-review and verification gates.

**Rationale:**
The legibility layer is reuse, not new machinery — the canvas already exists and is already good at stories. The Planner/Reviewer split cleanly separates the two modes of use. A canvas is passive, and passive scanning is exactly what lets problems slip (D1); the attestation strip is the cheap-but-correct fix — active prompts that state the baked-in assumptions and what approval certifies catch what passive rendering misses. The work is epic-sized because it spans the beads taxonomy merge, planning-sprint rendering, E2E/verification surfacing, the attestation strip, and `sprint-planning`'s new output contract.

---

### D3: Sprint-Dev / Merge / AVFL / E2E — one autonomous span, composed of distinct subskills — ADOPTED

**Developer framing:** These are obviously different phases of the workflow, not one monolithic step. Some may make sense as subskills or sub-workflows; AVFL is already a subskill. QA and code review should be steps on `momentum:dev` so they are also used in quick-fixes. (This corrects an earlier framing that called the four "one step" — that collapsed two different questions.)

**Decision:** Adopted, separating the two questions that were conflated:
- **Gate topology:** Sprint-Dev → Merge → AVFL → E2E sit in a single **autonomous span** between the sprint-plan-approval gate and the verification gate — no human intervention between them.
- **Skill decomposition:** they remain **distinct phases composed of subskills/steps**. AVFL stays its own subskill. **QA and code-review move into `momentum:dev`** so any flow that uses `dev` — sprint-dev, quick-fix, future callers — inherits the same quality steps. E2E is added (steps or a subskill within sprint-dev), with its automated portion running inside this span.

**Rationale:**
"One autonomous span between two human gates" is a property of how the developer experiences the pipeline; "distinct composable subskills" is an implementation property and a reuse opportunity. Collapsing them produced phantom seams and obscured the absence of E2E. Pulling QA and code-review into `momentum:dev` rather than leaving them as standalone pipeline phases means every dev-using flow gets the same quality gate for free, with no per-flow re-implementation.

---

### D4: Verification = the hardest human gate; manual content project-defined — ADAPTED

**Developer framing:** The human stamping approval on verification is the hardest gate of all — it is what defines whether the work is ready to merge to main and push. Verification is partly automatable, but parts cannot be: some require a human to look. The original framing named the manual portion as "look-and-feel across all three Compose Multiplatform surfaces" — but Compose Multiplatform is nornspun-specific, not Momentum in general.

**Decision:** Adopted with adaptation. Verification is the hardest human gate, structured Momentum-generally as **automated E2E + a manual human stamp**. Verification approval is the load-bearing gate; **push to main is the mechanical consequence** of the verification stamp, not itself the load-bearing gate. The **content of the manual portion is project-defined** — populated per story by `sprint-planning`'s plain-language "what this functionality is" description (D2) — not encoded into Momentum. For one project the manual portion is cross-platform visual look-and-feel; for another it is a CLI smoke test or a cross-browser pass. Momentum provides the gate slot, the attestation semantics, and the Reviewer-tab affordance; the checklist content comes from project configuration.

**Rationale:**
Momentum is the practice layer and must work for any project; encoding Compose-Multiplatform verification into the practice would couple it to one project's stack and break the abstraction. Naming verification (not push) as the load-bearing gate puts the human's attention on the right artifact — the running feature on the surfaces it must work on — and makes the manual check a first-class, non-optional gate step. Interim, "go look at it" is acceptable provided sprint-planning supplies a clear description of what is being verified.

---

### D5: Triage stays standalone and anytime-callable; retro becomes an additional caller; dedup + consolidation mandatory — ADOPTED

**Developer framing:** Triage should not be relocated into retro. Triage should *also* be used during the retro — it can also be used standalone, it can be used anytime. And triage requires dedup and consolidation; it does not currently dedup.

**Decision:** Adopted. `momentum:triage` remains a **standalone skill, invocable at any time from any context**. **Retro becomes an additional caller** of triage (one of its phases). **Dedup + consolidation against the existing backlog become mandatory behaviors of triage itself**, regardless of caller. Intake remains continuous — mid-sprint discoveries are still captured as stubs immediately; only the dedup/consolidate/classify judgment is what retro now invokes. This extends DEC-007 (retro joins the set of triage callers) and tightens triage's behavior contract.

**Rationale:**
Triage's value — the dedup/consolidate/classify operation — is independent of any single caller; forcing it into a single host (retro) would lose that flexibility. Making retro a caller ensures the backlog is groomed at retro time, when fresh observations land. Making dedup + consolidation mandatory in triage itself ensures every caller gets the same backlog hygiene, which is what stops the backlog accreting duplicates.

---

### D6: Remove momentum:distill entirely — ADOPTED

**Developer framing:** The distill step is not liked — it gets in the way of a bigger thing, normally just slows the whole process down, and requires a ton of human intervention. It has not been deduped. Mark it for removal. In its place, rely on the lighter-weight tooling already used to build and verify skills, rules, and hooks, but still make those fixes part of a sprint. If a sprint moves quickly, it should not be held up to distill a skill fix. Sometimes a sprint is slow — but mostly because it stumbles through a poorly built skill, and it is okay to feel that pain for a while so it gets fixed.

**Decision:** Adopted. `momentum:distill` is **removed entirely** — the skill directory is deleted and its Phase 5 invocation is removed from `momentum:retro`. Practice fixes (skills, rules, hooks, agents) become **ordinary sprint stories** built with the existing lightweight tooling (`skill-creator`, `agent-builder`, `constitution-builder`, etc.), or **`momentum:quick-fix`** when urgent. The slowness this exposes when a sprint stumbles through a poorly-built skill is **intentional** — a forcing function that surfaces the underlying problem rather than masking it with a distill fast-path. (Removal is being executed immediately as an ad-hoc `quick-fix`.)

**Rationale:**
Distill was an in-pipeline detour that demanded heavy human intervention for un-deduped output, blocking forward progress for what should be ordinary practice work. The two-lane disposition (normal story | quick-fix) uses tooling and skills that already exist — no new machinery. The pain of a slow sprint is the signal that drives properly fixing the bad skill; a distill fast-path would perpetuate the bad skill instead. The load-bearing assumption — that sprint cycle time is acceptable for non-urgent fixes — is explicit, and `quick-fix` backstops the urgent case.

---

### D7: Hermes-as-dispatcher — REJECTED

**Research recommended:** The 2026-05-18 Hermes-as-dispatcher research (`docs/research/hermes-claude-dispatcher-momentum-2026-05-18-final.md`) returned a verdict of DON'T ADOPT at high confidence (AVFL score 68/100). Hermes is good at fan-out dispatch to independent tasks and lightweight orchestration with no infrastructure overhead, but disqualified by: a state-ownership split-brain (Hermes owns its SQLite Kanban, Momentum owns `index.json` + beads, with no clean sync path); bypass of the `sprint-manager` FSM enforcement moat (an open Kanban lets any status be written, removing the enforcer); pre-1.0 maturity with biweekly breaking changes; and an MCP/ACP inversion in which the "parent-task-wakeup" callback initially assumed does not exist.

**Decision:** Rejected. Hermes is not adopted as a dispatcher or delegate for Momentum.

**Rationale:**
Adopting Hermes would create a second source of truth for state, dismantle the `sprint-manager` FSM enforcement the SoW model depends on, and pin the practice to a pre-1.0 tool with frequent breaking changes — for capabilities that, per D1, do not address Momentum's actual bottleneck. The bottleneck is comprehension at the gates, not dispatch throughput.

---

### D8: Claude-native dispatcher — DEFERRED, blocked on the D2 canvas epic — DEFERRED

**Developer framing / Research:** The Claude-native dispatcher (Agent SDK daemon tailing `intake-queue.jsonl`, with a Channel wake signal) described in `docs/research/claude-code-background-dispatcher-2026-05-17.md` is the right downstream move to replace the "manually trigger and babysit sprint-dev" pattern — but it cannot come first.

**Decision:** Deferred, with an explicit block: the **D2 canvas legibility epic is the prerequisite**. When unblocked, ship **Version A** — coarse queue events at pipeline-stage transitions (e.g. `sprint-activated`, `verification-stamped`). **Version B** — a per-story-step protocol — is **deferred indefinitely** as a routing optimization, decoupled from human-in-the-loop placement.

**Rationale:**
Per D1, building the dispatcher before the gates are legible would amplify the failure mode by delivering unreviewable work to the developer faster. The dispatcher accelerates the spans *between* gates; the bottleneck is comprehension *at* the gates, so speeding up execution first just makes the firehose worse. The prior research framed Versions A and B as coupled to the human-in-the-loop question; D1–D5 establish that they are not — the gates live at pipeline-stage transitions, which Version A's coarse events already cover. Locking in "Version A only, B indefinitely deferred" prevents a speculative-complexity trap when the work resumes.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 0 | Remove `momentum:distill` (D6) | Immediate — ad-hoc `quick-fix`, in progress | (ad-hoc quick-fix) |
| 1 | Canvas legibility epic (D2): Planner + Reviewer tabs, planning-state sprint rendering, epic/feature taxonomy merge, E2E/verification surfacing, attestation strip, sprint-planning functionality-description output | Next — the prerequisite for Phase 3 | epic-feature-collapse-closeable-grouping; new stories per the canvas epic |
| 2 | Pipeline restructure (D3, D4, D5): autonomous-span composition; QA/code-review into `momentum:dev`; E2E step; verification gate; triage standalone + retro caller + mandatory dedup | Parallel with or after Phase 1 | change-type-routing-in-sprint-dev, code-reviewer-agent-definition, sprint-dev-composed-file-spawn-wiring, sprint-dev-phase-7-gate, sprint-dev-fixture-autonomous-commit-per-story, avfl-invoke-code-reviewer-via-skill-not-task, specialist-agents-avfl-and-quickfix-phase2a, avfl-migration-story-exhaustive-call-site-audit, dev-fixer-agent-definition, retro-prior-action-item-cross-ref |
| 3 | Claude-native dispatcher, Version A (D8) | Blocked on Phase 1 | dag-dispatcher-loop |

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | Phase 1 done | Is the canvas legibility epic shipped and are the gates legible? | The Reviewer tab renders the plan-review and verification surfaces with the attestation strip; the developer can review a planning-state sprint and genuinely *catch* problems without fast-tracking. This is the hard precondition for Phase 3. |
| Gate 2 | Phase 3 start | Should the dispatcher proceed to Version A? | Gate 1 passed. Version A ships with coarse pipeline-stage queue events only; Version B is not built. |

---

## Affected Skill Surface

Beyond the story and architecture-decision blast radius, this decision changes a set of skill files directly. Recorded here as implementation surface (not a `stories_affected` field — these are skill artifacts):

| Sub-decision | Skill | Change |
|---|---|---|
| D2 | `canvas/` | Add Reviewer tab; planning-state sprint rendering; E2E/verification status surfacing; per-gated-item attestation strip; beads epic/feature taxonomy support. Planner tab unchanged. |
| D2 | `sprint-planning/` | Add a plain-language "what this functionality is" output per story, fed to the Reviewer tab. |
| D2 | `feature-grooming/` | Taxonomy-merge update to classification (taxonomy ownership). |
| D3 | `dev/` | QA and code-review move in; add E2E step; restructure into the autonomous-span model. |
| D3 | `code-reviewer/` | Invocation surface changes — spawned by `momentum:dev`, not directly by sprint-dev. |
| D3 | `sprint-dev/` | Restructure to a single autonomous span; QA/code-review delegation moves to the dev subskill; AVFL and E2E are named subskills within the span. |
| D3 | `quick-fix/` | Inherits QA + code-review by spawning `momentum:dev`. |
| D3 | `avfl/` | Wiring update — new caller is `momentum:dev`. |
| D5 | `triage/` | Add mandatory dedup + consolidation before classification; add retro as a valid caller path. |
| D5 / D6 | `retro/` | D5: add a triage-invocation step. D6: remove the Phase 5 distill invocation (≈18 references in `workflow.md`). |
| D6 | `distill/` | Delete the entire skill directory. |

---

## Provenance Note

Step 3 discovery for this decision (affected stories, architecture decisions, prior decisions) was produced by three parallel discovery agents and then validated by a full AVFL pass (8 dual-reviewer validators at skepticism 3). The first AVFL iteration scored failing — 21 findings, 4 critical — and the corrected discovery was folded into this document. Material corrections: four triage/retro stories were mis-statused as backlog (all are `done`, so D5/D6 changes there require new follow-on stories rather than edits); the DEC-019 / Decision 54 relationship was adjudicated as "built upon," not "amended" (the runtime stack is unchanged); Decisions 43 and 28 were added to the affected list; Decision 53 was corrected to unchanged.
