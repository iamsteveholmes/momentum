---
title: AVFL Scan Profile — Discovery-Only Validation for Team Handoff
story_key: avfl-scan-profile
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum-avfl/SKILL.md
  - skills/momentum-avfl/references/framework.json
  - skills/momentum/workflows/sprint-dev.md
change_type: skill-instruction + config-structure
---

# AVFL Scan Profile — Discovery-Only Validation for Team Handoff

## Goal

Add a fourth AVFL profile called "scan" that performs maximum-intensity discovery with
zero fix iterations. The scan profile activates all available lenses with dual reviewers
(Enumerator + Adversary per lens), uses maximum skepticism, and produces a scored,
consolidated findings list ready for handoff to a fix team.

This enables the hybrid sprint-dev model: AVFL handles adversarial discovery, an Agent
Team handles concurrent resolution, and an E2E Validator handles running-behavior
verification. The scan profile's output is the bridge between discovery and resolution.

Scan is orthogonal to corpus mode (8-1-avfl-corpus-mode): scan controls the review
intensity and fix loop; corpus controls single-document vs. multi-document input. Scan
can run with `corpus: false` (single file) or `corpus: true` (multi-document set). The
two features compose independently.

## Acceptance Criteria (Plain English)

- A new "scan" profile exists in AVFL alongside gate, checkpoint, and full; scan composes
  with corpus mode (can be invoked with `corpus: true` or `corpus: false` independently)
- Scan profile activates all available lenses with dual reviewers (Enumerator + Adversary
  per lens)
- Scan profile uses maximum skepticism (level 3)
- Scan profile performs consolidation with cross-check confidence tagging and severity
  scoring
- Scan profile performs ZERO fix iterations — output is the consolidated findings list
  only; no fixer agent is spawned
- The findings list includes severity, confidence, lens, dimension, evidence, and location
  for each finding
- The scan profile's output format is designed for handoff to a team: structured,
  actionable, and prioritized by severity then confidence
- Sprint-dev workflow is updated to use the hybrid model: AVFL scan (discovery) → team
  receives findings alongside story ACs and Gherkin specs → concurrent fix / verify / E2E
- When sprint-dev invokes AVFL, it passes `profile: scan`
- The team spawn prompt in sprint-dev includes the AVFL findings list as explicit context
- E2E Validator role is clearly distinguished from AVFL in sprint-dev instructions: AVFL
  validates file content against source material; E2E Validator validates running behavior
  against Gherkin specs using external tools — these roles are complementary and do not
  overlap

## Dev Notes

### What exists today

**AVFL profiles and framework (post 8-1-avfl-corpus-mode):**

`momentum-avfl` has three profiles defined in `references/framework.json`:
- `gate` — single agent per lens, pass/fail, no fix loop
- `checkpoint` — single agent per lens, one fix attempt on fail
- `full` — dual reviewers (Enumerator + Adversary) per lens, up to 4 fix iterations

The `validation_profiles` section of `framework.json` uses a heterogeneous schema —
not all fields appear in all profiles:

- **Common to all profiles:** `agents`, `dual_review`, `lenses_active`, `fix_loop`
- **gate only:** `dimensions_focus`, `on_fail`
- **checkpoint only:** `max_fix_attempts`, `on_fail_after_fix`
- **full only:** `max_iterations`, `pass_threshold`

Note: `max_fix_attempts` is a checkpoint-only field; it does not appear in the gate or
full profiles. Each profile uses only the fields relevant to its behavior.

`framework.json` already contains a `parameters` section (extended by 8-1 with `corpus`,
`authority_hierarchy`), `validation_profiles`, `prompts` (including corpus prompt
templates added by 8-1), and `dimension_taxonomy` (including corpus-only dimensions
`cross_document_consistency` and `corpus_completeness` added by 8-1). The scan profile
adds a new entry to `validation_profiles` alongside the existing three — it does not
modify any section added by 8-1.

`SKILL.md` references the active profile to configure Phase 1 (VALIDATE), Phase 2
(CONSOLIDATE), Phase 3 (EVALUATE), and Phase 4 (FIX). When `fix_loop: false`, Phase 3
(EVALUATE) exits the pipeline before reaching Phase 4, returning the consolidated
findings list directly — the fixer is never reached. SKILL.md also has a "Corpus Mode"
section added by 8-1 describing array input, activated dimensions, and
`{filename}:{section}` location format.

**momentum-research (8-2):** The research skill uses corpus-mode AVFL in its VERIFY
phase. This is an existing consumer of AVFL — the scan profile does not affect it
(research uses `profile: full` with `corpus: true`).

**Sprint-dev workflow:**

Sprint-dev (`skills/momentum/workflows/sprint-dev.md`) currently runs a single AVFL
pass in Phase 4 (Post-merge quality gate) without specifying a profile. It sequentially
runs AVFL then spawns a Team Review (QA, E2E Validator, Architect Guard) with findings
from the AVFL pass fed into the review phase.

### What to create / change

**1. Add `scan` profile to `framework.json`**

Insert into the existing `validation_profiles` section alongside gate/checkpoint/full:

```json
"scan": {
  "agents": "2 per active lens (up to 8 parallel)",
  "dual_review": true,
  "lenses_active": "All 4 lenses",
  "fix_loop": false,
  "on_fail": "return_findings",
  "output_format": "structured_handoff"
}
```

Notes on this schema:
- `agents` matches the full profile's format: "2 per active lens (up to 8 parallel)".
- `skepticism_level` is NOT a profile field. The AVFL pipeline controls skepticism at
  the pipeline level: iteration 1 runs at level 3, iterations 2+ run at level 2. Scan
  runs a single pass only (no fix loop), so it inherently always runs at maximum
  skepticism (level 3) per the existing pipeline logic — no field needed.
- `output_format: structured_handoff` is a **NEW field** being added to the profile
  schema by this story (not an existing field). It signals the consolidator to emit a
  prioritized findings list ordered by severity (critical → high → medium → low) then
  confidence (high → medium → low). Each finding entry must include: `id`, `severity`,
  `confidence`, `lens`, `dimension`, `location`, `description`, `evidence`, `suggestion`.

Note: `corpus` and `authority_hierarchy` are caller-supplied parameters (from 8-1), not
profile fields. A caller can invoke `profile: scan, corpus: true` to get maximum-intensity
corpus validation with no fix loop — the profile and corpus mode compose at call time.

**2. Update `SKILL.md` to document the scan profile**

- Add `scan` to the Profiles table with its characteristics
- Add a note in Phase 4 (FIX): when `fix_loop: false`, the fixer is not spawned and the
  consolidated findings list is returned as the final output
- Add a "Scan Profile Handoff Format" section describing the structured output: ordered
  list of findings with all required fields, suitable for direct use as team input context

**3. Update `skills/momentum/workflows/sprint-dev.md`**

Replace the Phase 4 (Post-merge quality gate) invocation and Phase 5 (Team Review) with
the hybrid model:

**Phase 4 (revised): AVFL Scan — Adversarial Discovery**
1. Invoke AVFL with `profile: scan` against the full post-merge codebase
2. Receive structured findings list (no fix loop runs)
3. Present findings summary to developer: count by severity, top findings preview
4. Developer may dismiss individual findings or mark as accepted risk — log decisions
5. Log scan results via `momentum-tools log`

**Phase 5 (revised): Hybrid Team — Concurrent Resolution + E2E**
1. Spawn team agents in parallel on main branch, each receiving:
   - Their role-specific guidelines from the sprint record
   - The story ACs for their assigned stories
   - The Gherkin specs from `sprints/{sprint-slug}/specs/`
   - The AVFL scan findings list (full structured output)
2. Team roles:
   - **Fixer agents** (one per finding cluster or story scope): address AVFL findings;
     cross-reference with ACs to avoid over-fixing
   - **E2E Validator**: validates running behavior against Gherkin specs using external
     tools (not file content review — this is distinct from AVFL's role); produces a
     scenario-by-scenario pass/fail report
   - **Architect Guard**: checks for pattern drift against architecture decisions;
     receives AVFL findings as additional signal
3. Consolidate findings from all team agents: AVFL scan residuals + E2E failures +
   architecture drift findings
4. Present consolidated fix queue to developer
5. Targeted fix loop: spawn fix agents for accepted items, re-run affected reviewers
   until clean or developer accepts remaining
6. Unresolved items become follow-up stories or backlog entries

### Key distinction: AVFL vs. E2E Validator

This distinction must be explicit in sprint-dev workflow instructions:

| Aspect | AVFL (scan profile) | E2E Validator (team role) |
|---|---|---|
| What it validates | File content against source material (ACs, specs, architecture) | Running behavior against Gherkin scenarios using external tools |
| Agent type | Adversarial file reviewers (Enumerator + Adversary) | Black-box behavior tester with tool access |
| Output | Structured findings list (severity, confidence, dimension) | Scenario pass/fail report |
| Fix loop | None (scan profile) | N/A — surfaces failures for fixer agents |
| Overlap | None | None |

These are complementary gates: AVFL catches content drift before running; E2E Validator
catches behavioral failures that only appear when the system runs.

### Profile comparison (for SKILL.md Profiles table)

| Profile | Agents | Skepticism | Fix Iterations | Purpose |
|---|---|---|---|---|
| gate | 1 per lens | 3 | 0 (pass/fail) | Lightweight CI gate |
| checkpoint | 1 per lens | 3 (iter 1) / 2 (iter 2+) | 1 | Mid-story quality check |
| full | 2 per lens (dual) | 3 (iter 1) / 2 (iter 2+) | up to 4 | End-of-story deep validation |
| scan | 2 per lens (dual) | 3 | 0 | Discovery-only; findings for team handoff |

Note: The pipeline runs iteration 1 at skepticism level 3 for all profiles. Profiles with
a fix loop (checkpoint, full) run subsequent iterations at level 2. Gate and scan each
run a single pass only, so they always operate at level 3.

### What NOT to change

- Do not add a fix loop to scan — zero iterations is the defining characteristic
- Do not modify the gate, checkpoint, or full profiles — scan is purely additive
- Do not change the AVFL sub-skills (validator-enum, validator-adv, consolidator) — scan
  uses them as-is; the difference is `dual_review: true`, `lenses_active: all`, and
  skipping the fixer (scan's single pass inherently runs at maximum skepticism level 3
  per the existing pipeline logic — no sub-skill changes needed)
- Do not modify 8-1 corpus mode additions (corpus parameters, corpus prompt templates,
  corpus-only dimensions in framework.json, Corpus Mode section in SKILL.md) — scan is
  orthogonal to corpus and must not alter corpus behavior
- Do not give dev agents access to Gherkin specs — the black-box boundary is maintained
- Do not give the E2E Validator access to implementation files — it validates behavior only

### Error handling

- If AVFL scan returns zero findings: log as clean, proceed to Team Review with empty
  findings list — do not skip the team phase
- If AVFL scan times out or errors: surface to developer, offer retry or proceed without
  scan (developer explicitly accepts the risk)
- If E2E Validator cannot reach a required external tool: log the gap, mark affected
  scenarios as `unverified` (not failed), surface to developer

### Requirements Coverage

- FR48: AVFL — extends the validate-fix loop skill with a fourth profile (scan)
- FR73: AVFL Scan Profile — defines the scan profile configuration and structured handoff output format
- FR74: Hybrid Resolution Team — sprint-dev spawns fixer agents + E2E Validator + Architect Guard concurrently with AVFL findings as context
- FR64: Sprint-Level AVFL — scan profile replaces the unqualified AVFL invocation in
  Phase 4, making the quality gate maximally adversarial
- Architecture: AVFL Profiles (gate/checkpoint/full) — adds scan as a fourth profile
  with zero fix iterations and maximum dual-reviewer intensity; builds on the
  framework.json structure established by 8-1-avfl-corpus-mode
- Architecture: Sprint Execution Flow — updates Phase 4 and Phase 5 of sprint-dev to
  implement the hybrid discovery-then-resolution model

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: write before touching any skill file)
  - [ ] Create `skills/momentum-avfl/evals/eval-scan-profile-no-fix-loop.md` — verifies
    scan profile runs dual reviewers on all lenses and returns findings without invoking
    fixer
  - [ ] Create `skills/momentum-avfl/evals/eval-scan-profile-structured-output.md` —
    verifies output is ordered by severity then confidence and includes all required fields
  - [ ] Create `skills/momentum-avfl/evals/eval-scan-profile-existing-profiles-unchanged.md`
    — verifies gate/checkpoint/full behave identically when scan is not selected

- [ ] Task 2 — Update `framework.json` with scan profile (AC: 1–7)
  - [ ] Add `scan` profile entry with `agents: "2 per active lens (up to 8 parallel)"`,
    `dual_review: true`, `lenses_active: "All 4 lenses"`, `fix_loop: false`,
    `on_fail: return_findings`, `output_format: structured_handoff` (new field)
  - [ ] Add `output_format` field to profile schema documentation comment
  - [ ] Add `structured_handoff` output format description: findings ordered by severity
    then confidence, all required fields present

- [ ] Task 3 — Update `SKILL.md` (AC: 1–7)
  - [ ] Add `scan` row to the Profiles table
  - [ ] Add note in Phase 4 (FIX): when `fix_loop: false`, skip fixer; return consolidated
    findings list as final output
  - [ ] Add "Scan Profile Handoff Format" subsection documenting the structured output
    format and field requirements

- [ ] Task 4 — Update `skills/momentum/workflows/sprint-dev.md` (AC: 8–11)
  - [ ] Replace Phase 4 AVFL invocation to use `profile: scan`
  - [ ] Rewrite Phase 5 (Team Review) as the hybrid model: fixer agents + E2E Validator +
    Architect Guard, all receiving AVFL findings list as context
  - [ ] Add explicit AVFL vs. E2E Validator distinction section to the workflow

- [ ] Task 5 — Run evals and verify (EDD cycle)
  - [ ] Run each eval using subagent per EDD protocol
  - [ ] Confirm all three eval behaviors match expectations or iterate (max 3 cycles)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum-avfl/evals/` (Task 1 above):
   - One `.md` file per eval, named descriptively
   - Format each eval as: "Given [describe the input and context], the skill should
     [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify `framework.json`, `SKILL.md`, and `sprint-dev.md` (Tasks 2–4)

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the
   eval's scenario as its task, and (2) the SKILL.md and workflow.md contents as context.
   Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3
   cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in
  `references/` with clear load instructions (NFR3)
- Skill names prefixed `momentum-` (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written in `skills/momentum-avfl/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented)
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] AVFL checkpoint on produced artifacts documented

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
