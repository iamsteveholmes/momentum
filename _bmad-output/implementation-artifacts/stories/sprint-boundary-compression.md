---
title: Sprint-Boundary Context Compression — Structured Sprint Summary at Retro Close
story_key: sprint-boundary-compression
status: ready-for-dev
epic_slug: feature-orientation
depends_on: []
touches:
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
change_type: skill-instruction
priority: high
---

# Sprint-Boundary Context Compression — Structured Sprint Summary at Retro Close

## Description

Each sprint completes with a retro, but the next sprint starts without a structured record of
what the previous sprint actually accomplished. Sprint-planning must reconstruct context from
raw stories/index.json entries and logs — there is no concise, human-readable artifact that
captures which features advanced, which stories completed vs. were planned, which decisions
were made, and what issues remain unresolved.

Per DEC-002 D4, the retro orchestrator should produce a `sprint-summary.md` at retro close.
Sprint planning Step 1 loads the most recent sprint summary to inform its recommendations.
This keeps both developer and agent oriented at cycle boundaries — sprint-boundary compression
tells us what happened and what matters without re-reading raw sprint history.

The summary is written by the retro orchestrator directly (no separate agent spawn). It is
capped at 500 words to enforce orientation, not reporting.

## Acceptance Criteria (Plain English)

1. At the end of Phase 6 (Sprint Closure) of the retro workflow, after calling
   `momentum-tools sprint retro-complete`, the retro orchestrator writes a `sprint-summary.md`
   file to `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/sprint-summary.md`.

2. The sprint summary contains the following sections:
   - **Features Advanced** (conditional — only present if
     `_bmad-output/implementation-artifacts/features.json` exists): lists features that had at
     least one story move to `done` during this sprint, with the feature name and updated status.
   - **Stories Completed vs. Planned**: count of stories that reached `done` out of the stories
     originally planned for the sprint, plus names of any stories closed as `closed-incomplete`
     or still in progress at retro time.
   - **Key Decisions**: a bulleted list of decisions (from `_bmad-output/planning-artifacts/decisions/`)
     whose `date` falls within the sprint date range (i.e., created or updated during this sprint).
     If none, section reads "No decisions recorded this sprint."
   - **Unresolved Issues**: any story stubs created during Phase 5 of the retro that were added
     to backlog, plus any stories closed as `closed-incomplete`. If none, reads "None."
   - **Narrative**: a single paragraph (3–5 sentences) summarising what the sprint accomplished,
     the primary focus, and what changed in the practice or product as a result.

3. The sprint summary is under 500 words total. If a draft exceeds 500 words, the retro
   orchestrator trims the narrative and story/decision lists to the most significant items.

4. Sprint planning Step 1 reads the most recent sprint summary before synthesising
   recommendations. "Most recent" is determined by finding the latest sprint in the `completed`
   array of `_bmad-output/implementation-artifacts/sprints/index.json` with a `retro_run_at`
   value, then reading
   `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/sprint-summary.md` from that
   sprint's directory. If no summary file exists for the most recent completed sprint, sprint
   planning continues without it (the step is non-blocking) and shows a notice: "No sprint
   summary found for {sprint-slug} — context from previous sprint unavailable."

5. The sprint-summary.md file follows this exact structure (sections in this order):
   ```
   # Sprint Summary — {sprint-slug}

   **Sprint completed:** {sprint_completed}
   **Retro date:** {retro_date}

   {## Features Advanced — ONLY include this heading and content if features.json exists}

   ## Stories Completed vs. Planned
   ...

   ## Key Decisions
   ...

   ## Unresolved Issues
   ...

   ## Narrative
   [single paragraph]
   ```

6. The retro completion summary shown to the developer (the final output of Phase 6) includes a
   line confirming the sprint summary was written:
   `Sprint summary: _bmad-output/implementation-artifacts/sprints/{sprint-slug}/sprint-summary.md`

7. No separate agent spawn is used to write the sprint summary. The retro orchestrator writes
   it directly, using state already gathered during the retro (sprint stories, story statuses,
   decision scan, story stubs created in Phase 5).

## Dev Notes

### Retro workflow changes (Phase 6)

The sprint summary is produced at the end of Phase 6, after the `sprint retro-complete` call,
before presenting the final summary output. The orchestrator has all necessary state at this
point:

- `{{sprint_slug}}`, `{{sprint_started}}`, `{{sprint_completed}}` — from Phase 1
- `{{verified_stories}}`, `{{incomplete_stories}}`, `{{force_closed_slugs}}` — from Phase 3
- Story stubs created (approved_count, stub titles) — from Phase 5
- `{{today}}` — current date for retro_date field

**Features Advanced section (conditional):**
Check whether `_bmad-output/implementation-artifacts/features.json` exists before writing this
section. If the file does not exist, omit the section entirely (no placeholder, no empty
heading). If it exists, read it and find features where any story in `stories` array has status
`done` in `stories/index.json` and was in the sprint's story list.

**Key Decisions scan:**
Read the decision files in `_bmad-output/planning-artifacts/decisions/`. The frontmatter `date`
field identifies when a decision was recorded. Include decisions whose date falls between
`{{sprint_started}}` and `{{sprint_completed}}` (inclusive). List as:
`- DEC-XXX: {title} ({date})`

**Word count enforcement:**
After drafting the summary, count words. If over 500, shorten the narrative paragraph first,
then trim decisions and story lists to the most significant items. The 500-word limit is a hard
cap — the summary is orientation, not a full report.

**Writing the file:**
Write to `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/sprint-summary.md`.
The sprint directory already exists by this point (created during sprint-dev and used in Phase 4
for audit extracts). Create the file directly using the Write tool.

### Sprint planning workflow changes (Step 1)

In Step 1 (Synthesize recommendations from master plan and backlog), add a sprint summary load
after reading the PRD and product brief, before the backlog staleness check:

1. Read `_bmad-output/implementation-artifacts/sprints/index.json`
2. Find the most recently completed sprint with `retro_run_at != null` (latest by `completed`
   date)
3. If found, read `_bmad-output/implementation-artifacts/sprints/{slug}/sprint-summary.md`
4. If the file exists, include its contents in the recommendation synthesis context — the
   "what happened last sprint" signal that informs prioritisation
5. If the file does not exist, show notice and continue

The sprint summary is used as additional context for the synthesis, not as a replacement for
PRD/backlog analysis. Its role is "what changed most recently" — features that advanced narrow
the high-priority candidates for this sprint.

### File locations

- `skills/momentum/skills/retro/workflow.md` — add sprint-summary writing to Phase 6
- `skills/momentum/skills/sprint-planning/workflow.md` — add sprint-summary load to Step 1

No new files or scripts are required. Both changes are workflow instruction edits only.

## Momentum Implementation Guide

**Change Types in This Story:**
- Retro Phase 6 change (retro/workflow.md) → skill-instruction (EDD)
- Sprint planning Step 1 change (sprint-planning/workflow.md) → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Workflow instructions are non-deterministic LLM
prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the workflow changes:**
1. Write 2–3 behavioral evals for the retro change in `skills/momentum/skills/retro/evals/`
   (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g.,
     `eval-produces-sprint-summary-at-retro-close.md`,
     `eval-sprint-summary-omits-features-section-when-no-features-json.md`)
   - Format: "Given [describe the input and context], the skill should [observable behavior —
     what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

2. Write at least 1 behavioral eval for the sprint-planning change in
   `skills/momentum/skills/sprint-planning/evals/` (create `evals/` if it doesn't exist):
   - Example: `eval-sprint-planning-loads-sprint-summary-when-available.md`
   - Cover: "Given a completed sprint with a sprint-summary.md file, sprint planning Step 1
     includes the summary content in its synthesis context"

**Then implement:**
3. Add the sprint-summary writing block to Phase 6 of `retro/workflow.md`
4. Add the sprint-summary load to Step 1 of `sprint-planning/workflow.md`

**Then verify:**
5. Run evals: for each eval file, spawn a subagent, give it the eval scenario and the relevant
   workflow content as context. Observe whether the subagent's behavior matches the expected
   outcome.
6. If all evals match → task complete
7. If any eval fails → diagnose the gap, revise, re-run (max 3 cycles; surface to user if
   still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- No new SKILL.md is created in this story — changes are to existing workflow.md files only.
  NFR1 (description ≤150 chars), NFR3 (body ≤500 lines), and NFR12 (namespace prefix) apply
  to the existing SKILL.md files — confirm they remain compliant after edits.
- `model:` and `effort:` frontmatter fields must remain present in retro/SKILL.md and
  sprint-planning/SKILL.md (do not remove or alter frontmatter during workflow edits)

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/retro/evals/`
- [ ] 1+ behavioral eval written in `skills/momentum/skills/sprint-planning/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] retro/SKILL.md description ≤150 characters confirmed (unchanged — verify it still holds)
- [ ] `model:` and `effort:` frontmatter present in both affected SKILL.md files
- [ ] Gherkin specs exist in `sprints/{sprint-slug}/specs/` for this sprint — dev agent must
  implement against plain English ACs above only, never against .feature files
  (Decision 30 black-box separation)

## Dev Agent Record

*(To be completed during implementation)*

### Completion Notes

### Change Log
