---
title: Practice-wide decision-grade presentation standard
story_key: decision-grade-presentation-standard
status: ready-for-dev
epic_slug: ad-hoc
feature_slug:
story_type: practice
change_type:
  - rule-hook
  - skill-instruction
  - specification
verification_method: EDD eval
depends_on: []
touches:
  - skills/momentum/references/rules/
  - skills/momentum/skills/assessment/
  - skills/momentum/skills/decision/
  - skills/momentum/skills/conductor/
  - skills/momentum/skills/retro/
  - skills/momentum/skills/impetus/
---

# Practice-wide decision-grade presentation standard

## Story

As a developer reviewing AI-produced output at every human gate,
I want a practice-wide decision-grade presentation standard with measurable output caps and a self-sufficiency floor,
so that my cognitive budget is spent on decision-relevant content — tight on the irrelevant, complete on the decision-relevant.

## Description

**What:** Establish a practice-wide standard governing human-facing output across Momentum: measurable verbosity **caps** (≤N bullets, word/line budgets per surface type), executive-summary-first ordering, positive-concision phrasing, and named output schemas — **paired** with a hard **self-sufficiency floor**: every decision-relevant item (finding, decision card, divergence, pause-ask, recommendation) carries its **what / why-it-matters / evidence inline**, never sending the human to open a file, recall prior context, or read other material to make the call. The standard codifies one convention: **`effort` drives work depth; explicit caps govern output verbosity** — the two are orthogonal and a skill that does deep work still presents it tightly.

The standard lands as a new **enforced rule** (the caps half is the new, currently-ownerless contract) and is **wired into** the conduct end-gate report and the live conversational skills (assessment, decision, conduct/sprint-dev, retro, impetus).

**The two halves — distinguish them clearly:**

- **CAPS half (NEW — currently ownerless).** Verbosity ceiling. Today no rule, validator, or skill owns "how much is too much" at a human gate. AES-004 Finding 6 flagged this gap directly: conduct's self-sufficiency mandate is good but has *no concision counterweight*. This story creates that counterweight — measurable caps that cut Specification-Fatigue material (collapse the routine, summarize clean items to a line, depth-on-demand via collapsibles). The caps cut **irrelevant** material only.

- **SELF-SUFFICIENCY floor (EXISTS — already enforced).** Completeness floor. Already enforced in the conduct lineage: the conductor's **Pause-Ask Surface Contract** (`skills/momentum/skills/conductor/references/escalation.md` §"Pause-Ask Surface Contract (DEC-036 D5 Self-Sufficiency Floor)") requires every pause-ask to carry what/why/evidence inline, and the conduct report spec (`_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md` §9) names the floor as "never cut." This story does **not** re-invent the floor — it (a) generalizes the floor's wording from conduct-only to practice-wide, and (b) adds the missing caps counterweight so the two are stated together as one standard: **"tight on the irrelevant, complete on the decision-relevant."**

**Why:** "Specification Fatigue" — the cognitive exhaustion of spending review budget on irrelevant content (`docs/research/spec-fatigue-research-2026-03-21.md`). DEC-036 D5 adopted the decision-grade presentation standard *with* a self-sufficiency floor, and its Phase 4 explicitly marks the practice-wide application as **separable from the conduct build** (can proceed in parallel; does not block the engine stories). The conduct-specific instance already exists as a reference standard; this story generalizes it so assessment, decision, retro, and impetus output is governed by the same caps-and-floor contract — not just the conduct report.

**Source decision:** DEC-036 D5 / Phase 4 (`_bmad-output/planning-artifacts/decisions/dec-036-conduct-hitl-calibration-2026-06-01.md`). Connects to prior `spec-fatigue-research-2026-03-21`. Conduct-specific instance: `conduct-endgate-report-format-and-voice.md` §9.

## Acceptance Criteria

1. A new enforced rule file exists at `skills/momentum/references/rules/decision-grade-presentation.md` (the canonical source that deploys to `.claude/rules/`), following the established Momentum rule format (frontmatter with `title`, `applies_to`, `status`, `source_decisions: DEC-036 D5`), and is self-sufficient — an agent loading only this file has complete guidance to apply the standard without reading any other document.

2. The rule states the **core convention** explicitly: `effort` drives work *depth*; explicit caps govern output *verbosity*. The two are orthogonal — a skill running at high effort still presents its result within the caps; a skill is never permitted to widen its output because it did more work.

3. The rule defines the **CAPS half** as measurable, enforceable ceilings — not vague guidance. At minimum it specifies: (a) a bullet cap per list (≤N bullets, N a concrete number), (b) a per-surface budget (e.g., word or line budget for a situational report vs. a finding card vs. a section), (c) executive-summary-first ordering (the decision/headline leads; supporting detail follows), and (d) positive-concision phrasing (state what *is*, not lengthy what-isn't). Each cap is stated as a checkable condition a reviewer or validator could verify against an output.

4. The rule defines **output schemas / surface types** the caps apply to — naming the recurring human-facing surfaces in the practice (e.g., situational report, finding/divergence card, decision card, pause-ask, end-gate report section) and giving each its applicable cap. A surface type without a defined cap is a gap the rule flags, not silently exempt.

5. The rule states the **SELF-SUFFICIENCY floor** as the non-negotiable counterweight, generalized practice-wide (not conduct-only): every decision-relevant item carries **what / why-it-matters / evidence inline**; the human is never sent to open a file, recall prior context, or read other material to make the call. A missing field is a **defect**, not a permitted blank.

6. The rule makes the **caps-vs-floor boundary** unambiguous: caps cut **irrelevant** material only; caps **never** trim a decision-relevant what/why/evidence field. Where the two appear to conflict, the floor wins (completeness on the decision-relevant is not negotiable; concision applies to the irrelevant). The rule states this resolution explicitly as "tight on the irrelevant, complete on the decision-relevant."

7. The rule explicitly cross-references the **existing** floor enforcement so the new rule does not contradict or duplicate it: it names the conductor Pause-Ask Surface Contract (`skills/momentum/skills/conductor/references/escalation.md`) and the conduct report spec §9 (`conduct-endgate-report-format-and-voice.md`) as the conduct-specific instances the practice-wide rule generalizes — the rule is the umbrella, those are instances under it.

8. The standard is **wired into** each live conversational skill that produces human-facing output — assessment, decision, conduct/sprint-dev (conductor), retro, and impetus — such that each skill's instructions reference the decision-grade-presentation rule and constrain their developer-facing output to its caps while honoring its floor. Wiring is concrete (the skill's SKILL.md / workflow.md / references point at the rule and apply a named cap to a named surface), not a passing mention.

9. For impetus specifically, the standard is applied to the **session situational report** (the 1–2 sentence Impetus voice greeting): the cap confirms the report stays at its stated brevity and the floor confirms the honest ledger counts / recurring-pattern signal it must carry are present inline — caps and floor both demonstrably govern the same surface.

10. The conduct end-gate report standard (`conduct-endgate-report-format-and-voice.md` §9, "Decision-grade presentation (DEC-036 D5)") is reconciled with the new practice-wide rule: §9 either references the practice-wide rule as its parent or is confirmed consistent with it, so there is one standard with conduct as an instance — not two divergent statements of the same DEC-036 D5 mandate.

11. The story's work is demonstrably **separable from and non-blocking on the conduct build** (DEC-036 Phase 4): nothing in the rule or the wiring requires the conduct engine stories to be merged first, and the rule does not modify the conduct engine pipeline — only the presentation layer (`depends_on: []` holds).

12. Each piece of wiring is verified behaviorally — for at least one representative surface per touched skill, running the skill (or an eval scenario of it) produces output that (a) stays within the declared cap and (b) carries the self-sufficiency floor's what/why/evidence inline for any decision-relevant item. A skill whose output violates either is a failing wiring, not a passing one.

## Tasks / Subtasks

- [ ] **Task 1 — Author the enforced rule.** Create `skills/momentum/references/rules/decision-grade-presentation.md`. (Satisfies AC 1–7.)
  - [ ] Write frontmatter (`title`, `applies_to: All Momentum human-facing output`, `status: Active`, `source_decisions: DEC-036 D5`, `cascade: global → project → path-scoped`), matching the format of sibling rules in `references/rules/` (e.g., `verification-standard.md`).
  - [ ] State the `effort` drives depth / caps govern verbosity convention (AC 2).
  - [ ] Define the measurable CAPS: bullet cap, per-surface budgets, exec-summary-first, positive-concision — each as a checkable condition (AC 3).
  - [ ] Enumerate the output schemas / surface types and their per-surface caps (AC 4).
  - [ ] State the SELF-SUFFICIENCY floor, generalized practice-wide, with "missing field = defect" (AC 5).
  - [ ] State the caps-vs-floor boundary and the "tight on the irrelevant, complete on the decision-relevant" resolution (AC 6).
  - [ ] Cross-reference the existing conductor Pause-Ask Surface Contract and conduct report §9 as instances the rule generalizes (AC 7).
- [ ] **Task 2 — Wire the standard into the live skills.** Update each skill to reference the rule and apply a named cap to a named developer-facing surface while honoring the floor. (Satisfies AC 8.)
  - [ ] `skills/momentum/skills/assessment/` — constrain its developer-facing findings/validation output.
  - [ ] `skills/momentum/skills/decision/` — constrain the adopt/reject/defer presentation; ensure each decision carries what/why/evidence inline.
  - [ ] `skills/momentum/skills/conductor/` — confirm/align the report + pause-ask surfaces reference the practice-wide rule (the floor already lives here; add the caps reference).
  - [ ] `skills/momentum/skills/retro/` — constrain the findings-document / digest presentation.
  - [ ] `skills/momentum/skills/impetus/` — constrain the session situational report (AC 9).
- [ ] **Task 3 — Reconcile the conduct report spec.** Update `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md` §9 to reference the practice-wide rule as its parent (or confirm consistency), so conduct is an instance of the one standard. (Satisfies AC 10, specification change.)
- [ ] **Task 4 — Author behavioral evals for the wiring.** For at least one representative surface per touched skill, write an eval scenario under that skill's `evals/` asserting the output stays within the declared cap AND carries the floor's what/why/evidence inline. Run them. (Satisfies AC 12; provides the EDD verification per the change-type guide.)
- [ ] **Task 5 — Confirm non-blocking separability.** Verify `depends_on: []` holds, the rule touches only the presentation layer, and nothing requires the conduct engine stories to merge first. (Satisfies AC 11.)

## Dev Notes

### Context: two halves, one standard, one of them already enforced

The single most important thing to get right: **this story adds the caps counterweight; it does not re-invent the self-sufficiency floor.** The floor already ships and is already enforced in the conduct lineage:

- **Conductor Pause-Ask Surface Contract** — `skills/momentum/skills/conductor/references/escalation.md`, section "Pause-Ask Surface Contract (DEC-036 D5 Self-Sufficiency Floor)". It mandates every mid-flight pause-ask carry **what / why / evidence inline** so the developer decides without leaving the surface. There is a concrete pause-ask output template there — match its what/why/evidence triple when generalizing the floor.
- **Conduct report spec §9** — `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md`, section 9 "Decision-grade presentation (DEC-036 D5) — tight on the irrelevant, complete on the decision-relevant." It already states BOTH halves *for the conduct report*: caps ("collapse routine, summarize clean items to a line, collapsibles for depth-on-demand") and the floor ("every finding/decision/divergence carries what / why-it-matters / evidence inline. A missing field is a defect, not a blank card. The caps never trim these.").

So §9 is effectively the conduct-specific *prototype* of the practice-wide rule this story writes. **Lift its language as the rule's spine, generalize the scope from "the conduct report" to "all Momentum human-facing output," then add per-skill wiring.** Do not contradict §9; reconcile it (Task 3 / AC 10) so there is one standard with conduct as an instance.

### Where the rule lives and how it deploys

Enforced practice rules live in `skills/momentum/references/rules/` (canonical sources) and deploy to `.claude/rules/`. The siblings there — `verification-standard.md`, `workflow-fidelity.md`, `anti-patterns.md`, `model-routing.md`, `cmux.md`, `authority-hierarchy.md` — are the format template. `verification-standard.md` is the closest model: it is self-sufficient ("Agents loading only this file have complete enforcement guidance"), has a routing table, and cites `source_decisions`. Mirror that self-sufficiency and frontmatter shape. This is a `rule-hook` change (it is a `.claude/rules/`-bound rule file), not a `specification` change.

### The caps must be measurable, not advisory

AES-004 Finding 6's whole point is that exhortations to "be concise" do not work without a counterweight that bites. Make every cap a **checkable condition**: a bullet count, a word/line budget, an ordering requirement. "Be brief" is not a cap; "≤7 bullets per list; situational report ≤2 sentences; finding card lead-in ≤1 sentence then collapsible detail" is a cap. The eval in Task 4 must be able to mechanically check at least the structural caps.

### The convention is the load-bearing idea

`effort` (a frontmatter parameter many skills already carry — see `research`, `epic-breakdown`, `create-story`) governs how much *work* a skill does. The caps govern how much it *says*. Keep them orthogonal in the rule's wording: a high-`effort` retro still presents a tight findings digest; it does not earn a longer report by having worked harder. This directly answers the developer's Specification-Fatigue rationale in DEC-036 D5.

### Self-sufficiency floor — Gherkin/eval generality reminder

When wiring the floor into skills and writing evals, keep the behavioral assertion **general**: "any decision-relevant item carries what/why/evidence inline" — not "the decision card contains exactly these three hardcoded sentences." Test the *presence and self-sufficiency* of the context, not exact output text. Over-specifying couples the eval to wording and defeats the point.

### Separability (DEC-036 Phase 4)

DEC-036's phased plan marks Phase 4 (practice-wide application of D5) as "Separable from the conduct build; can proceed in parallel." This story must hold `depends_on: []` and touch only the presentation layer. It must NOT modify the conduct engine pipeline (stakes classification, fixer schema, gate model) — those are the sibling conduct-build stories (`conduct-spec-revision-dec036`, `conduct-stakes-timing-escalation-mechanism`). Touching §9's *report-presentation* language is in scope; touching §4/§8 *engine* language is out of scope.

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → `rule-hook` (functional / behavioral verification)
- Task 2 → `skill-instruction` (EDD)
- Task 3 → `specification` (direct authoring + cross-reference)
- Task 4 → `skill-instruction` (EDD — the eval authoring itself)
- Task 5 → verification/audit task (no new artifact; inspection)

**Verification method (frozen-contract override justification):** This story spans `rule-hook` + `skill-instruction` + `specification` change types, which the routing table maps to behavioral-trigger, EDD-eval, and document-review respectively. Per `verification-standard.md` §2 (Method Override) and the create-story routing rule that `specification` tasks are subsumed by the dominant deliverable's method, the governing method for this story is **EDD eval**: the standard's caps and floor are only meaningfully verified by running each touched skill (or an eval scenario of it) and observing that its developer-facing output (a) stays within the declared cap and (b) carries the self-sufficiency floor inline. Static document review of the rule file is necessary but not sufficient — the rule's value is realized only in the skills' produced output, which is behavioral. The rule file's own internal-consistency check (AC 1–7) is performed by inspection as part of the EDD setup.

---

### rule-hook Tasks: Functional Verification

The rule (`decision-grade-presentation.md`) is declarative — no unit test. Verify functionally:

1. **Write the rule** per the established format in existing `skills/momentum/references/rules/` files (use `verification-standard.md` as the structural model — self-sufficient, frontmatter with `source_decisions`, checkable conditions).
2. **State the expected behavior** as a testable condition: "Given any Momentum human-facing surface, the standard caps verbosity to its declared budget AND guarantees what/why/evidence inline for every decision-relevant item."
3. **Verify functionally:** confirm all required sections are present (caps, surface schemas, floor, caps-vs-floor boundary, cross-references), the rule is internally consistent, and the caps are each phrased as a checkable condition (not vague guidance). Confirm the rule contradicts neither the conductor Pause-Ask Surface Contract nor conduct report §9.
4. **Document** the verification result in the Dev Agent Record.

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as a testable condition (in Dev Agent Record)
- [ ] Functional verification performed and documented
- [ ] Format matches established `references/rules/` patterns (frontmatter, self-sufficiency)
- [ ] No contradiction with the existing self-sufficiency floor enforcement (escalation.md, report §9)

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md / workflow.md / references files.** Skill instructions are non-deterministic LLM prompts. Use EDD:

**Before writing the wiring into a skill:**
1. Write a behavioral eval in that skill's `evals/` directory (create `evals/` if absent):
   - Format: "Given [the skill produces its developer-facing surface], the output should [stay within the declared cap] AND [carry what/why/evidence inline for every decision-relevant item]."
   - Test the behavior (cap respected + floor present), not exact output text — keep it general.

**Then implement:**
2. Add the wiring: the skill's SKILL.md / workflow.md / references reference the `decision-grade-presentation` rule, apply a named cap to a named surface, and honor the floor.

**Then verify:**
3. Run each eval via an Agent-tool subagent: give it the eval scenario plus the skill's instructions as context; observe whether the produced surface respects the cap and carries the floor.
4. All evals match → task complete. Any fail → diagnose the wiring gap, revise, re-run (max 3 cycles; surface if still failing).

**NFR compliance — mandatory for every skill-instruction edit:**
- Any SKILL.md `description` touched must stay ≤150 characters (NFR1)
- `model:` and `effort:` frontmatter must remain present
- SKILL.md body stays under 500 lines / 5000 tokens; overflow → `references/` (NFR3)
- Skills keep the `momentum:` namespace prefix (NFR12)

**Additional DoD items for skill-instruction tasks:**
- [ ] 1+ behavioral eval per touched skill written in its `evals/`
- [ ] EDD cycle ran — cap-respected + floor-present confirmed for each touched skill (or failures documented)
- [ ] Any edited SKILL.md description ≤150 characters confirmed
- [ ] `model:`/`effort:` frontmatter intact on edited skills
- [ ] AVFL checkpoint on the produced artifacts documented (momentum:dev runs this automatically)

### specification Tasks: Direct Authoring with Cross-Reference Verification

Task 3 (reconciling conduct report §9) is a `specification` change validated by AVFL against its upstream (DEC-036 D5 + the new practice-wide rule):

1. **Update §9** of `conduct-endgate-report-format-and-voice.md` so it references the practice-wide rule as its parent (or is confirmed consistent).
2. **Verify cross-references:** the reference to the new rule path resolves; the DEC-036 D5 citation resolves; no other §9 cross-reference is broken.
3. **Verify format compliance:** the spec keeps its existing section structure and voice.
4. **Document** the change in the Dev Agent Record.

**Additional DoD items for specification tasks:**
- [ ] All cross-references resolve (new rule path, DEC-036 D5, conductor escalation.md)
- [ ] §9 reads as an instance of one standard, not a divergent second statement of it
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

**Gherkin note:** Gherkin `.feature` specs for this sprint (if any) live in `sprints/{sprint-slug}/specs/` and are **off-limits to the dev agent** — implement against the plain-English ACs in this story file only, never against `.feature` files (Decision 30 black-box separation). The ACs above are intentionally plain-English; Gherkin is authored separately by the planner.

### References

- Source decision: `_bmad-output/planning-artifacts/decisions/dec-036-conduct-hitl-calibration-2026-06-01.md` — D5 (decision-grade presentation, adopted with self-sufficiency floor) and Phase 4 (practice-wide, separable from conduct build).
- Upstream assessment: `_bmad-output/planning-artifacts/assessments/aes-004-hitl-altitude-design-gaps-2026-06-01.md` — Finding 6 (self-sufficiency mandate lacks concision counterweight) and Rec 5.
- Conduct-specific instance (caps + floor prototype): `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md` §9.
- Existing floor enforcement: `skills/momentum/skills/conductor/references/escalation.md` — "Pause-Ask Surface Contract (DEC-036 D5 Self-Sufficiency Floor)".
- Pain-context research: `docs/research/spec-fatigue-research-2026-03-21.md`.
- Rule-format model: `skills/momentum/references/rules/verification-standard.md`.
- Epic context: `ad-hoc` (from _bmad-output/planning-artifacts/epics.json)
