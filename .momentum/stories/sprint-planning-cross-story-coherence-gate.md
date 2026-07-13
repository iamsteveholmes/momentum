---
title: Sprint-planning cross-story coherence gate for depends_on deliverables
story_key: sprint-planning-cross-story-coherence-gate
status: ready-for-dev
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: feature
change_type:
  - skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-planning/references/coherence-gate.md
  - skills/momentum/skills/sprint-planning/evals/
priority: critical
verification_method_advisory: skill-invoke
---

# Sprint-planning cross-story coherence gate for depends_on deliverables

## Story

As a developer,
I want sprint-planning (once the full sprint story set is visible and every per-story
contract is frozen) to validate every `depends_on` edge — asserting that each input a
consumer story names is actually delivered by the producer story's contract deliverables,
so that a sprint cannot activate with two halves embodying contradictory architectures,
where each story passes its own gates while the seam between them belongs to no one.

## Description

Root-caused from the nornspun campaign-init sprint (sprint-2026-05-30). The client story
`campaign-init-offered-suggestion-list-render-and-routes` instructed "source the copy from
the backend payload... not a hardcoded client string" with
`depends_on: backend-campaign-init-add-offered-suggestion-list-copy`. But that backend
story only edited the Urd **system prompt** — it delivered no payload, no endpoint, no
schema. The consumer's named input ("backend payload") did not exist on the producer side.

No gate could see this: create-story runs one story at a time, and its AVFL checkpoint
validates each story against its own epic record. The incoherence existed only *between*
stories. The result: backend stories all assumed the campaign-init conversation flowed
through Urd chat; client stories all assumed client-local rendering; no story owned the
wiring; the dev hardcoded "fallback" constants and the sprint shipped a scripted
client-side performance.

Sprint-planning is the altitude where all frozen contracts are visible together — the
cheapest, highest-leverage place for the check: for every `depends_on` edge in the sprint,
the consumer's referenced external inputs must map to a concrete deliverable (artifact,
endpoint, schema, constant, file) in the producer's contract. Unmatched edges block
activation or force an explicit wiring story.

**Pain context:** A 15-story sprint was internally consistent story-by-story and globally
incoherent; the gap cost a full build + end-gate cycle before live Phase-4 caught it.
Recurs on any sprint whose stories span a producer/consumer seam (client/backend,
skill/config, agent/harness). Discovered during sprint-2026-05-30 root-cause analysis
(2026-06-10).

## Acceptance Criteria

1. **Edge enumeration at the coherence altitude.** After per-story contracts are frozen
   (Step 3.5) and before activation (Step 8), a dedicated deterministic step enumerates
   every `depends_on` edge among the sprint's selected story set. A planning run over a
   sprint containing N `depends_on` edges reports having examined all N edges (in-sprint and
   out-of-sprint edges are both counted, none dropped silently).

2. **Consumer input extraction.** For each `consumer → producer` edge, the gate extracts the
   consumer story's *externally-sourced inputs* — the concrete things the consumer names as
   originating in another story (a backend payload field, an endpoint path, a schema, a
   config key, an emitted constant, a signal from a sibling story). Observable: on a consumer
   that says "source the copy from the backend payload," the gate lists that payload field as
   a required input for the edge.

3. **Producer deliverable matching.** Each extracted input is matched against the producer
   story's frozen contract deliverables (the Part-A header plus the contract body's
   ACs/deliverables). An input with a corresponding producer deliverable marks the edge
   satisfied. Observable: given a producer contract that delivers the payload field the
   consumer names, the edge passes.

4. **Coherence failure is surfaced and named (regression anchor).** An edge whose
   consumer-named input has NO matching producer deliverable is reported as a coherence
   failure that names BOTH story slugs, the specific missing deliverable, and the seam.
   Replaying the nornspun pair —
   `campaign-init-offered-suggestion-list-render-and-routes` depends_on
   `backend-campaign-init-add-offered-suggestion-list-copy`, where the producer delivers only
   a system-prompt edit and no payload — makes the gate surface a failure naming both slugs
   and the missing backend payload/endpoint/schema deliverable.

5. **Remediation choices offered.** Each coherence failure presents three explicit
   resolutions: amend the producer's contract to deliver the named input, amend the consumer
   so it no longer requires it, or add an owning wiring story. Observable: the failure card
   lists all three options.

6. **A coherent pair passes silently.** A sprint whose every `depends_on` edge has its
   consumer inputs matched to producer deliverables produces no coherence-failure output — the
   gate passes without prompting the developer. Observable: a coherent fixture pair reaches
   activation with no coherence flag raised.

7. **Activation blocked while failures are open.** Open coherence failures block sprint
   activation at the Step 8 pre-activation gate unless the developer issues an explicit
   override; the block-or-override decision is surfaced at the Step 7 visual companion plan
   gate as a genuine fork (not auto-resolved). Observable: with an open failure and no
   override, `momentum-tools sprint activate` is not called; with an override, activation
   proceeds and the override is recorded.

8. **Out-of-sprint edges are checked, not skipped.** An edge whose producer is NOT in the
   current sprint is checked against the producer's recorded status and deliverables (a done
   story's frozen contract / its index deliverables), not silently skipped. Observable: an
   edge to a done out-of-sprint story that carries the required deliverable passes; an edge to
   an out-of-sprint story that lacks it — or is not `done` — is flagged.

9. **Deterministic, with non-colliding vocabulary.** The gate is a dedicated deterministic
   edge-enumeration step, not another generic AVFL prompt (Step 6's whole-sprint AVFL is the
   gate that demonstrably missed the nornspun edge). Its wording avoids "contract-freeze"
   (reserved for the per-story sha256 integrity machinery); the check is named for cross-story
   *seam coherence*. Observable: the step runs its enumeration regardless of the AVFL outcome,
   and the workflow text uses "seam coherence"/"cross-story coherence" — never "contract-freeze"
   — for this check.

## Tasks / Subtasks

- [ ] **Task 1 — Add the deterministic seam-coherence step to the workflow (AC1, AC9).**
  Insert a new dedicated step in `skills/momentum/skills/sprint-planning/workflow.md`
  positioned after Step 3.5 (per-story contracts frozen and visible) and before Step 8
  (activation). The step enumerates every `depends_on` edge among the selected story set. Use
  non-colliding vocabulary ("cross-story seam coherence"); never "contract-freeze". Make the
  step deterministic (edge enumeration + matching), explicitly NOT an AVFL prompt.

- [ ] **Task 2 — Implement input extraction + deliverable matching (AC2, AC3).** For each
  edge, extract the consumer's externally-sourced inputs and match them against the producer's
  frozen contract deliverables (Part-A header + contract body). Extract the matching
  heuristics (what counts as an "externally-sourced input", how a producer deliverable is
  recognized) into `skills/momentum/skills/sprint-planning/references/coherence-gate.md` and
  reference it from the workflow step, keeping `workflow.md` within its size budget.

- [ ] **Task 3 — Author the coherence-failure report format (AC4, AC5).** Define the failure
  card: both story slugs, the specific missing deliverable, the seam description, and the
  three remediation choices (amend producer / amend consumer / add wiring story).

- [ ] **Task 4 — Wire the result into the plan gate and activation gate (AC6, AC7).** Surface
  open coherence failures at Step 7's visual companion plan gate as a genuine fork; block
  activation at Step 8's pre-activation gate while failures are open, allowing an explicit
  developer override that is recorded. A sprint with no open failures passes silently (no
  developer prompt).

- [ ] **Task 5 — Handle out-of-sprint producer edges (AC8).** Resolve edges whose producer is
  not in the current sprint against the producer's recorded status and deliverables (done
  story's frozen contract / index entry); flag when the deliverable is absent or the producer
  is not `done`, rather than skipping.

- [ ] **Task 6 — EDD evals for the gate (AC4, AC6).** Before/with implementation, write
  behavioral evals in `skills/momentum/skills/sprint-planning/evals/`: (a) the nornspun
  incoherent pair surfaces and names the seam failure with both slugs and the missing
  deliverable; (b) a coherent pair passes silently. Run the EDD cycle and confirm both
  behaviors.

## Dev Notes

### Decision Authority

This story hardens `momentum:sprint-planning` itself — it is a developer-directed critical
ride-along on the "agent cohort goes live" sprint (sprint-2026-07-13). Scope authority: the
root-cause analysis of nornspun sprint-2026-05-30 (2026-06-10) and the dedup sweep binding
constraints recorded in the Triage Notes below. The gate and the existing Step 2 `depends_on`
presence/status check are **one coherent depends_on feature spanning two workflow steps**, not
two rival passes: Step 2 keeps its presence/status check unchanged; this story adds the missing
*semantic deliverable-matching* half as a **new deterministic step placed after Step 3.5** — the
first point in the workflow where the frozen per-story contracts (the producer-deliverable
source) exist to match against. It extends the depends_on feature across two steps; it does not
edit the Step 2 block in place, and it is not a second parallel dependency traversal. No new
architecture decision is required; the producer-deliverable source (frozen per-story contracts,
Step 3.5) already exists.

### Current State of Affected Files

- `skills/momentum/skills/sprint-planning/workflow.md` (~1258 lines). Relevant anchors:
  - **Step 2** (~line 229) — already runs a shallow `depends_on` check: for each selected
    story, confirms each `depends_on` slug is either `done` or in-sprint; emits a *presence*
    warning + developer override. It does NOT inspect whether the producer actually delivers
    what the consumer consumes. This is the check being extended (semantically), not replaced.
  - **Step 3.5** (~line 327) — authors and freezes one contract of record per story under
    `.momentum/sprints/{sprint-slug}/specs/{slug}.{ext}`, each with a mandatory Part-A header
    (`how_dev_self_checks`, `verification_method`, `harness_profile`, `contract_path`) plus a
    body of deliverables/ACs. These frozen contracts are the **machine-readable
    producer-deliverable source** the matcher reads. This is the structural anchor
    (`sprint-planning-frozen-per-story-contract-holistic-coverage`, done).
  - **Step 6** (~line 968) — whole-sprint AVFL. This is the gate that demonstrably failed to
    catch the nornspun seam; the new check must be deterministic, not a fifth AVFL lens.
  - **Step 7** (~line 1014) — visual companion plan gate. Open coherence failures surface here
    as a fork for developer sign-off.
  - **Step 8** (~line 1152) — pre-activation gate + `frozen_sha256` computation + `sprint
    activate`. Open coherence failures block here unless explicitly overridden.
- New: `skills/momentum/skills/sprint-planning/references/coherence-gate.md` — the extracted
  matching heuristics (keeps `workflow.md` within its size budget; loaded by the new step).
- Existing: `skills/momentum/skills/sprint-planning/evals/` (already holds the skill's ~21 eval
  files) — this story ADDS new behavioral eval files for the gate to that directory.

### Architecture Compliance

- **Producer-deliverable source is the frozen contract, not the epic record.** Read the
  Part-A header + contract body under `specs/` for producer deliverables. Frozen contracts are
  the DEC-029/DEC-030 machine-readable record of what each story ships;
  `conduct-planning-emit-contract-schema` (done) emits the machine-readable
  `story_assignments[].contract{}` at this same altitude and may be consumed as the producer
  source. Do NOT invent a parallel deliverable store.
- **Vocabulary hazard (binding).** "contract-freeze" already means temporal sha256 integrity
  of a single story's contract (`conduct-contract-freeze-check`, `frozen_sha256`). This
  cross-story semantic check must use distinct wording — "cross-story seam coherence."
- **Deterministic, not AVFL.** Step 6's AVFL is the demonstrated miss. Implement as a
  dedicated deterministic edge-enumeration step whose output feeds the Step 7 fork and Step 8
  block — not as another AVFL prompt.
- **One depends_on feature, two steps — not a rival pass.** Step 2 keeps its presence/status
  check; this story adds the semantic deliverable-matching half as a new deterministic step
  after Step 3.5 (the first point where frozen contracts exist to match against). It is the
  same depends_on feature extended across two steps, not a second independent dependency
  traversal bolted beside Step 2.

### Testing Requirements

- **Method (advisory): `skill-invoke`.** The single change type is `skill-instruction`, which
  the verification-standard routing table maps to `skill-invoke`. Verification drives
  `momentum:sprint-planning` (or its coherence step) over crafted fixtures and observes
  behavior — static/textual review of the `workflow.md` diff alone is insufficient; the
  observable must be the *live planning run's output*, captured via the EDD eval spawns below.
- **EDD, not TDD** (skill-instruction — non-deterministic LLM prompt). Evals live in
  `skills/momentum/skills/sprint-planning/evals/`. Two anchor behaviors:
  1. **Incoherent pair (regression).** The nornspun pair — consumer
     `campaign-init-offered-suggestion-list-render-and-routes` naming a backend payload,
     producer `backend-campaign-init-add-offered-suggestion-list-copy` delivering only a
     system-prompt edit — must surface a coherence failure naming both slugs and the missing
     payload/endpoint/schema deliverable.
  2. **Coherent pair.** A pair whose producer contract delivers exactly the input the consumer
     names must pass silently (no coherence flag, no developer prompt).
- Both fixtures should be reproducible: a minimal two-story sprint with the relevant frozen
  contracts under `specs/`.

### Project Context Reference

Momentum practice module — see `CLAUDE.md`. This story modifies a Momentum skill (dev-skills
guidelines apply: `skills/momentum/references/agent-skill-development-guide.md` is the
authoritative source for SKILL/workflow structure and the 500-line body budget — the reason
the matching heuristics are extracted into `references/coherence-gate.md`).

### References

- Origin: nornspun sprint-2026-05-30 root-cause analysis — broken `depends_on`
  edge `campaign-init-offered-suggestion-list-render-and-routes` →
  `backend-campaign-init-add-offered-suggestion-list-copy` (AVFL held finding #7).
- Sibling per-story check: `create-story-dependency-deliverable-check` (backlog — the
  per-story half; this gate is the whole-sprint version run when all contracts are visible).
- Structural anchor: `sprint-planning-frozen-per-story-contract-holistic-coverage` (done —
  frozen per-story contracts at Step 3.5 are the producer-deliverable source for the matcher).
- Contract schema source: `conduct-planning-emit-contract-schema` (done — emits machine-readable
  `story_assignments[].contract{}` at planning altitude; consume its Part-A headers).
- Cross-references to carry: `avfl-cross-story-integration-lens` (backlog — merge-time
  backstop; `avfl/workflow-merge-review.md` already implements much of that lens, so the stub
  may be partially stale — flag to refine, do not absorb),
  `contract-seam-stories-two-sided-review-scope` (done — wiring stories this gate forces into
  existence inherit its two-sided review scope),
  `sprint-planning-pre-sprint-class-1-render-gate` (backlog — open coherence failures belong
  among its blocking flags; gate first if same sprint).
- Epic context: `momentum-sprint-planning-to-ready` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–6 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic
LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/sprint-planning/evals/` (the directory
   already exists with the skill's other evals — ADD new files here, do not recreate it):
   - One `.md` file per eval, named descriptively (e.g.,
     `eval-surfaces-seam-failure-on-incoherent-pair.md`,
     `eval-coherent-pair-passes-silently.md`).
   - Format each eval as: "Given [an incoherent / coherent two-story sprint with these frozen
     contracts], the skill should [observable behavior — surfaces + names the seam failure, or
     passes silently]."
   - Test behaviors and decisions, not exact output text.

**Then implement:**
2. Modify `skills/momentum/skills/sprint-planning/workflow.md` (new deterministic step) and add
   `skills/momentum/skills/sprint-planning/references/coherence-gate.md`.

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it the eval's
   scenario as its task and load the skill (SKILL.md + workflow.md contents, or invoke the
   installed skill). Observe whether behavior matches the eval's expected outcome.
4. If all evals match → task complete.
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3
   cycles; surface to developer if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field ≤150 characters (NFR1) — note: this story edits `workflow.md`
  and adds a `references/` doc; if the SKILL.md `description` is not touched, leave it
  unchanged, but confirm it still complies.
- `model:` and `effort:` frontmatter present on the skill (unchanged by this story — confirm).
- `workflow.md` body stays under 500 lines / 5000 tokens per section budget; the matching
  heuristics overflow into `references/coherence-gate.md` with a clear load instruction from
  the new step (NFR3). (`workflow.md` is already large — keep the added step lean and push
  detail to the reference doc.)
- Skill name keeps the `momentum:` namespace (NFR12).

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/sprint-planning/evals/`
- [ ] EDD cycle ran — both anchor behaviors (incoherent surfaces+names, coherent passes
      silently) confirmed (or failures documented with explanation)
- [ ] New step uses "cross-story seam coherence" vocabulary — no "contract-freeze" collision
- [ ] Matching heuristics live in `references/coherence-gate.md`, loaded by the new step
      (workflow.md kept within budget)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)

**Frozen verification contract reminder:** A frozen verification contract exists for this
sprint at `.momentum/sprints/{sprint-slug}/specs/sprint-planning-cross-story-coherence-gate.*`.
Before signaling done, read only the Part-A header (`how_dev_self_checks`,
`verification_method`, `harness_profile`) as a self-check. Do NOT read the verifier body
(Part B: scenarios, assertion scripts) beyond sections explicitly named by
`how_dev_self_checks`.

## Dev Agent Record

_This section is populated by the dev agent after enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List

## Triage Notes — dedup sweep 2026-06-11

Full-backlog dedup sweep (multi-agent, adversarially verified): **no duplicate — safe to
enrich.** Binding constraints for create-story enrichment:

- **Extend, don't duplicate:** `skills/momentum/skills/sprint-planning/workflow.md`
  (~line 229) already runs a depends_on presence/status check at selection time (warning +
  developer override). The semantic deliverable-matching half is the missing piece — extend
  that check rather than adding a second dependency pass. Step 3.5 (frozen per-story
  contracts) + Step 8 activation gate are the natural insertion point, and the frozen
  contracts are the machine-readable producer-deliverable source for the matcher.
- **Deterministic, not AVFL:** workflow Step 6's whole-sprint AVFL checkpoint is the gate
  that demonstrably failed to catch the nornspun edge — implement the gate as a dedicated
  deterministic edge-enumeration step, not another generic AVFL prompt.
- **Vocabulary hazard:** "contract-freeze" already means temporal sha256 integrity of one
  story's contract (`conduct-contract-freeze-check`, frozen_sha256 machinery). Choose
  non-colliding wording for cross-story semantic coherence.
- **Sequencing option:** `conduct-planning-emit-contract-schema` (backlog, critical) emits
  machine-readable story_assignments[].contract{} at the same planning altitude — if it
  lands first, consume its Part-A headers as the producer-deliverable source.
- **Cross-references to carry:** `avfl-cross-story-integration-lens` (backlog — merge-time
  backstop; note `avfl/workflow-merge-review.md` already implements much of that lens, so
  the lens stub may be partially stale — flag to refine, do not absorb),
  `contract-seam-stories-two-sided-review-scope` (done — wiring stories this gate forces
  into existence inherit its two-sided review scope),
  `sprint-planning-frozen-per-story-contract-holistic-coverage` (done — structural anchor),
  `sprint-planning-pre-sprint-class-1-render-gate` (backlog — open coherence failures
  belong among its blocking flags; gate first if same sprint), sibling
  `create-story-dependency-deliverable-check` (per-story half).
