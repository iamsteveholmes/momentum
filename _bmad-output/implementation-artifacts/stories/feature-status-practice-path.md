---
title: Feature Status Practice Path — Skill Topology and SDLC Coverage Map for Momentum
story_key: feature-status-practice-path
status: ready-for-dev
epic_slug: feature-orientation
depends_on:
  - feature-status-skill
touches:
  - skills/momentum/skills/feature-status/workflow.md
change_type: skill-instruction
priority: high
derives_from:
  - path: _bmad-output/planning-artifacts/decisions/dec-002-feature-visualization-and-orientation-2026-04-11.md
    relationship: derives_from
    section: "D5: Differentiate Product and Practice Visualization Paths — ADOPT"
---

# Feature Status Practice Path — Skill Topology and SDLC Coverage Map for Momentum

## Story

As a developer working on Momentum (a practice project),
I want `momentum:feature-status` to detect that I am in a practice project
and render a skill topology view with SDLC coverage mapping,
so that I can see which SDLC phases have skill coverage, how skills hand off
to each other, and where gaps or redundancies exist.

## Description

The base `feature-status-skill` (its dependency) implements the product project
rendering path: feature type taxonomy, acceptance condition tracking, and
story-to-feature coverage mapping. That path is designed for UI/API products
like Nornspun.

Momentum is a practice project — its "features" are skills, workflows, and
lifecycle coverage. A product-style rendering would be useless: there are no
user-observable UI flows to track. What matters is: which SDLC phases have
coverage, how skills hand off to each other, and where the practice is blind.

This story adds the practice project rendering path to `feature-status`
workflow.md. The product path must remain completely unaffected.

### Project Type Detection

Practice project detection is automatic, based on artifact structure:
- Presence of `skills/` directory containing at least one `*/SKILL.md`
- AND presence of `_bmad-output/planning-artifacts/`

If both conditions hold, render the practice path. Otherwise render the
product path. No manual config flag needed.

### Skill Discovery

Glob `skills/momentum/skills/*/SKILL.md`. Read each file's frontmatter for
`name` and `description`. Build the skill inventory from this scan — do not
hardcode skill names.

### Rendering: Three Views

**1. Skill topology** — which skills exist and how they connect/hand off.
Hand-off relationships to detect:
- sprint-planning → sprint-dev (sprint-dev consumes sprint-planning output)
- sprint-dev → retro (retro runs after sprint-dev completes)
- retro → sprint-planning (next cycle starts from retro findings)
- assessment → decision (assessment feeds decision records)
- decision → create-story (decisions produce story stubs)
- create-story → dev (dev executes stories)
- intake → sprint-planning (intake queue feeds sprint planning)

Render as ASCII block. Example format (topology adapts to actual skills found):

```
  intake ──────────────────────────────────────────┐
                                                    ▼
  assessment ──► decision ──► create-story ──► sprint-planning
                                                    │
                                               sprint-dev
                                                    │
                                                  retro ──► (next cycle)
```

**2. SDLC coverage map** — which SDLC phases have Momentum skill coverage.
Phases to evaluate: Discovery, Planning, Specification, Implementation,
Review, Retrospective, Orientation/Onboarding, Quality/Validation.

Map each discovered skill to one or more phases based on its name and
description. Flag phases with no coverage as gaps.

Render as compact table:

```
  Phase                  Skills                         Status
  ──────────────────────────────────────────────────────────────
  Discovery              research, assessment           covered
  Planning               sprint-planning, intake        covered
  Specification          create-story, decision         covered
  Implementation         dev, quick-fix                 covered
  Review                 code-reviewer, avfl            covered
  Retrospective          retro                          covered
  Orientation            impetus, feature-status        covered
  Quality/Validation     architecture-guard, avfl       covered
```

**3. Redundancy detection** — skills that overlap significantly in SDLC
phase or scope. Flag pairs where two skills cover the same phase with
similar descriptions. Report as a short list under the coverage map:
"Possible overlap: X and Y both cover [phase]." Only flag when evidence
is clear — do not over-flag.

### Output Constraint

Total output under 40 lines. Do not produce a full graph or lengthy
narrative. Topology + coverage table + any redundancy flags — that is the
complete output.

## Acceptance Criteria (Plain English)

### AC1: Practice Project Detection Is Automatic

- The workflow detects practice vs. product project by checking for
  `skills/` directory with `*/SKILL.md` files AND `_bmad-output/planning-artifacts/`
- No config flag or manual override required
- If both conditions hold → practice path; otherwise → product path

### AC2: Skill Discovery via Glob

- Skills are discovered by globbing `skills/momentum/skills/*/SKILL.md`
- Frontmatter `name` and `description` are read from each file
- The skill inventory is dynamic — adding a new skill directory makes it
  appear in the topology automatically

### AC3: Skill Topology Renders Correctly

- Output includes an ASCII topology showing skill hand-off relationships
- Detected hand-offs include at minimum: intake → sprint-planning,
  sprint-planning → sprint-dev, sprint-dev → retro, retro → sprint-planning,
  assessment → decision, decision → create-story
- Hand-off relationships are inferred from known workflow conventions, not
  from a hardcoded list that excludes newly added skills

### AC4: SDLC Coverage Map Renders Correctly

- Output includes a compact table mapping SDLC phases to covering skills
- Phases evaluated: Discovery, Planning, Specification, Implementation,
  Review, Retrospective, Orientation/Onboarding, Quality/Validation
- Phases with no covering skill are flagged as "gap"
- Each discovered skill is mapped to at least one phase

### AC5: Redundancy Detection Runs

- After the coverage map, the workflow checks for skills that overlap in
  phase with similar descriptions
- If overlaps are detected, they are listed concisely (one line per pair)
- If no clear overlaps exist, no redundancy section is shown

### AC6: Output Is Under 40 Lines

- The total rendered practice path output is under 40 lines
- No prose paragraphs — only ASCII topology, compact table, and short flags

### AC7: Product Path Is Unaffected

- When run on a product project (no `skills/` directory with SKILL.md files),
  the workflow follows the product rendering path exactly as implemented by
  the base `feature-status-skill`
- No regressions to the product path

### AC8: Workflow Integration Is Seamless

- The practice path branching is added to `feature-status/workflow.md`
- No new SKILL.md is created — this is an extension of the existing skill
- The workflow reads project type first, then branches to product or practice
  rendering

## Tasks / Subtasks

- [ ] Task 1 — Add project type detection to workflow.md (AC: 1)
  - [ ] Check for `skills/` directory containing `*/SKILL.md` files
  - [ ] Check for `_bmad-output/planning-artifacts/` existence
  - [ ] Branch: both present → practice path; otherwise → product path

- [ ] Task 2 — Implement skill discovery (AC: 2)
  - [ ] Glob `skills/momentum/skills/*/SKILL.md`
  - [ ] Read `name` and `description` from each file's frontmatter
  - [ ] Build dynamic skill inventory

- [ ] Task 3 — Implement skill topology rendering (AC: 3)
  - [ ] Define hand-off relationship rules from workflow conventions
  - [ ] Render ASCII topology from discovered skills + hand-off rules
  - [ ] Keep topology block under 12 lines

- [ ] Task 4 — Implement SDLC coverage map (AC: 4)
  - [ ] Map each discovered skill to one or more SDLC phases
  - [ ] Render compact table (phase | skills | status)
  - [ ] Flag phases with no covering skills as "gap"

- [ ] Task 5 — Implement redundancy detection (AC: 5)
  - [ ] Check for skills sharing a phase with similar descriptions
  - [ ] Emit one-line flags for detected overlaps
  - [ ] Suppress section entirely if no overlaps found

- [ ] Task 6 — Validate output constraint and product path (AC: 6, 7, 8)
  - [ ] Verify total practice path output is under 40 lines
  - [ ] Run against a product project to confirm product path is unaffected
  - [ ] Confirm no new SKILL.md was created

## Dev Notes

### Relationship to feature-status-skill

This story extends `skills/momentum/skills/feature-status/workflow.md` only.
The base skill (SKILL.md frontmatter, invocation, product path logic) is
implemented by `feature-status-skill`. Do not modify SKILL.md. Do not alter
the product rendering path. Branch early in the workflow and return after
the practice path renders.

### Hand-Off Convention

Hand-offs are directional: skill A → skill B means B typically runs after A
and consumes A's output. The canonical cycle is:
`intake → sprint-planning → sprint-dev → retro → (repeat)`. Assessment and
decision form a sub-cycle feeding into sprint-planning. Impetus and
feature-status are orientation skills — they sit above the cycle, not in it.

### Phase Mapping Heuristics

| Skill name pattern       | Primary SDLC phase(s)                    |
|--------------------------|------------------------------------------|
| research                 | Discovery                                |
| assessment               | Discovery                                |
| decision                 | Specification                            |
| intake                   | Planning                                 |
| sprint-planning          | Planning                                 |
| create-story             | Specification                            |
| dev, quick-fix           | Implementation                           |
| code-reviewer, avfl      | Review, Quality/Validation               |
| retro                    | Retrospective                            |
| impetus, feature-status  | Orientation/Onboarding                   |
| architecture-guard       | Quality/Validation                       |
| refine                   | Planning, Specification                  |
| distill                  | Orientation/Onboarding                   |
| upstream-fix             | Review, Quality/Validation               |
| agent-guidelines         | Specification                            |

These are heuristics — the implementation should use skill `description`
to resolve ambiguous cases rather than hardcoding every skill name.

### Voice

Output is dry, direct, scannable. No prose explanations in the rendered
output. If a gap exists, label it "gap". If an overlap exists, name the
pair. The developer should be able to read the full output in under 10
seconds.

### References

- [Source: DEC-002 D5] — Decision authorizing practice project rendering path
- [Depends: feature-status-skill] — Base skill that this story extends

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1–6 → `skills/momentum/skills/feature-status/workflow.md` → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Workflow instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the workflow changes:**
1. Write 3 behavioral evals in `skills/momentum/skills/feature-status/evals/` (create `evals/` if it doesn't exist):
   - `eval-practice-path-topology-shows-handoffs.md`
     "Given a Momentum project with skills installed under `skills/momentum/skills/*/SKILL.md`,
     the skill renders an ASCII topology block showing the canonical cycle
     (intake → sprint-planning → sprint-dev → retro) and the assessment sub-cycle
     (assessment → decision → create-story), with all discovered skills appearing in at least one position."
   - `eval-practice-path-sdlc-coverage-flags-gaps.md`
     "Given skills covering Discovery, Planning, Specification, Implementation, Review,
     Retrospective, and Orientation but no skill mapped to Quality/Validation, the skill's
     SDLC coverage table marks Quality/Validation as 'gap' and marks covered phases with
     the relevant skill names."
   - `eval-product-path-unaffected-by-practice-extension.md`
     "Given a product project directory with no `skills/` directory containing SKILL.md files,
     the skill renders feature type groups (flow/connection/quality) with status and gap analysis.
     No topology block or SDLC coverage table appears in the output."

**Then implement:**
2. Add project type detection branch early in `feature-status/workflow.md`
3. Add skill discovery via glob and frontmatter read
4. Implement topology rendering, SDLC coverage map, and redundancy detection
5. Validate output is under 40 lines

**Then verify:**
6. Run evals: for each eval file, spawn a subagent, give it the eval scenario and the relevant
   workflow content as context. Observe whether the subagent's behavior matches the expected outcome.
7. If all evals match → task complete
8. If any eval fails → diagnose the gap, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- No new SKILL.md is created in this story — changes are to `feature-status/workflow.md` only.
  The existing SKILL.md at `skills/momentum/skills/feature-status/SKILL.md` must remain unmodified.
- `model:` and `effort:` frontmatter fields in feature-status/SKILL.md must not be altered.

**Additional DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written in `skills/momentum/skills/feature-status/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] feature-status/SKILL.md description ≤150 characters confirmed (unchanged — verify it still holds)
- [ ] `model:` and `effort:` frontmatter present in feature-status/SKILL.md
- [ ] Total practice-path output confirmed under 40 lines via eval run
- [ ] Product path confirmed unaffected via eval run

---

## Dev Agent Record

### Agent Model Used

_to be filled on completion_

### Debug Log References

None

### Completion Notes List

_to be filled on completion_

### File List

- skills/momentum/skills/feature-status/workflow.md
- _bmad-output/implementation-artifacts/stories/feature-status-practice-path.md
