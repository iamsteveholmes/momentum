---
title: Markdown Formatting for Skill Output Templates
story_key: markdown-formatting-skill-output-templates
status: ready-for-dev
epic_slug: ad-hoc
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/quick-fix/workflow.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/create-story/workflow.md
  - skills/momentum/skills/research/workflow.md
  - skills/momentum/skills/assessment/workflow.md
  - skills/momentum/skills/decision/workflow.md
  - skills/momentum/skills/distill/workflow.md
  - skills/momentum/skills/refine/workflow.md
  - skills/momentum/skills/feature-breakdown/workflow.md
  - skills/momentum/skills/feature-grooming/workflow.md
  - skills/momentum/skills/epic-grooming/workflow.md
  - skills/momentum/skills/plan-audit/workflow.md
  - skills/momentum/skills/intake/workflow.md
  - skills/momentum/skills/triage/workflow.md
  - skills/momentum/skills/agent-guidelines/workflow.md
  - skills/momentum/skills/dev/workflow.md
change_type: skill-instruction
---

# Markdown Formatting for Skill Output Templates

## Goal

Add proper markdown formatting to `<output>` blocks in Momentum skill workflow.md files.
Claude Code renders markdown (bold, headers, blockquotes) in terminal output, so output
templates that use `##` headers, `**bold**`, `>` blockquotes, and inline `` `code` `` give
developers real visual hierarchy that makes output scannable at a glance.

## Acceptance Criteria (Plain English)

### AC1: Section Headers
- Multi-section outputs use `##` headers to separate logical sections (e.g., `## Summary`,
  `## Next Steps`, `## Findings`, `## AVFL Result`)
- Single-line status messages do not add headers — headers apply only when output has two
  or more distinct logical sections

### AC2: Bold for Key Items
- Story slugs, skill names, file paths, and sprint slugs that appear in output prose are
  wrapped in `**bold**`
- Recommended items (e.g., the recommended next story, the recommended action) are bold
- Status values (`ready-for-dev`, `done`, `blocked`) are bold where they appear in
  summary lines

### AC3: Blockquotes for Warnings and Callouts
- Warning messages, gate failures, and "halt" conditions use `>` blockquote formatting
- Informational callouts that deserve visual separation (e.g., "AVFL found N issues")
  use blockquote formatting
- Normal flow output (status lines, lists of items) does not use blockquotes

### AC4: Inline Code for Slugs, Paths, and Commands
- File paths and directory paths are wrapped in backtick inline code
- Story slugs, sprint slugs, and skill invocation names (`momentum:dev`, `momentum:avfl`)
  are wrapped in inline code
- Shell commands shown in output (e.g., `git merge`) use inline code

### AC5: Coverage — Priority Flows
- All `<output>` blocks in the following skills are updated: `sprint-planning`,
  `sprint-dev`, `quick-fix`, `retro`, `create-story`, `research`, `assessment`,
  `decision`, `distill`, and `refine`
- Remaining skills (`feature-breakdown`, `feature-grooming`, `epic-grooming`,
  `plan-audit`, `intake`, `triage`, `agent-guidelines`, `dev`) are updated as a
  second pass within the same story
- No `<output>` block is made worse — existing content is preserved and formatted,
  not rewritten

### AC6: No Behavioral Change
- Only `<output>` block text is modified — no workflow logic, step ordering, action
  elements, or conditional checks are changed
- Variable placeholders (e.g., `{{story_key}}`, `{{avfl_result}}`) are preserved
  exactly as-is

## Tasks / Subtasks

- [ ] Task 1: Update output blocks in priority-flow skills (`sprint-planning`,
  `sprint-dev`, `quick-fix`, `retro`, `create-story`) — AC1–AC6
  - [ ] 1.1: `skills/momentum/skills/sprint-planning/workflow.md` — apply markdown
    formatting to all `<output>` blocks
  - [ ] 1.2: `skills/momentum/skills/sprint-dev/workflow.md` — apply markdown
    formatting to all `<output>` blocks
  - [ ] 1.3: `skills/momentum/skills/quick-fix/workflow.md` — apply markdown
    formatting to all `<output>` blocks
  - [ ] 1.4: `skills/momentum/skills/retro/workflow.md` — apply markdown formatting
    to all `<output>` blocks
  - [ ] 1.5: `skills/momentum/skills/create-story/workflow.md` — apply markdown
    formatting to all `<output>` blocks

- [ ] Task 2: Update output blocks in knowledge-flow skills (`research`, `assessment`,
  `decision`, `distill`, `refine`) — AC1–AC6
  - [ ] 2.1: `skills/momentum/skills/research/workflow.md`
  - [ ] 2.2: `skills/momentum/skills/assessment/workflow.md`
  - [ ] 2.3: `skills/momentum/skills/decision/workflow.md`
  - [ ] 2.4: `skills/momentum/skills/distill/workflow.md`
  - [ ] 2.5: `skills/momentum/skills/refine/workflow.md`

- [ ] Task 3: Update output blocks in remaining skills (`feature-breakdown`,
  `feature-grooming`, `epic-grooming`, `plan-audit`, `intake`, `triage`,
  `agent-guidelines`, `dev`) — AC1–AC6
  - [ ] 3.1: `skills/momentum/skills/feature-breakdown/workflow.md`
  - [ ] 3.2: `skills/momentum/skills/feature-grooming/workflow.md`
  - [ ] 3.3: `skills/momentum/skills/epic-grooming/workflow.md`
  - [ ] 3.4: `skills/momentum/skills/plan-audit/workflow.md`
  - [ ] 3.5: `skills/momentum/skills/intake/workflow.md`
  - [ ] 3.6: `skills/momentum/skills/triage/workflow.md`
  - [ ] 3.7: `skills/momentum/skills/agent-guidelines/workflow.md`
  - [ ] 3.8: `skills/momentum/skills/dev/workflow.md`

## Dev Notes

### What Exists Today

All Momentum skill workflow.md files contain `<output>` blocks that define what the
skill prints to the developer during execution. These blocks currently produce flat plain
text — no markdown formatting. Example of current state in `create-story/workflow.md`:

```
<output>Story {{story_key}} is yours to review.

Produced: {{story_file}}
Sprint tracking: stories/index.json (status: ready-for-dev, metadata: written)
Change types: {{change_types_summary}}
AVFL checkpoint: {{avfl_result}}
...
</output>
```

Claude Code renders markdown in terminal output. `**bold**`, `## headers`,
`> blockquotes`, and `` `inline code` `` all render with visual hierarchy. This means
a simple update to `<output>` text transforms developer-facing output from a wall of
text into a scannable summary.

### What to Change

Apply formatting rules to `<output>` block text only. The workflow XML structure,
`<action>` elements, `<check>` conditionals, and `<step>` elements are NOT touched.

**Formatting rules (from ACs):**
1. Multi-section outputs get `##` section headers
2. Story slugs, skill names, sprint slugs, and file paths → `**bold**` in prose, or
   `` `inline code` `` when they appear as identifiers/commands
3. Warning/gate-failure outputs → `> blockquote`
4. Shell commands and invocation names → `` `inline code` ``
5. Status summary lines: use bold for the status value when highlighted
   (e.g., `Status: **ready-for-dev**`)

**Priority areas for highest-impact formatting:**
- Completion signals (end-of-workflow outputs) — most frequently seen by developers
- Gate failure outputs — these need to stand out as warnings
- "Here's what was produced" summaries — slug + path + next-steps bundles

### What NOT to Change

- Do not modify `<action>`, `<check>`, `<critical>`, `<note>`, or `<ask>` elements
- Do not change variable placeholder syntax — `{{story_key}}` stays as-is
- Do not add markdown to workflow.md prose outside of `<output>` blocks
- Do not change the logical content of any output — formatting only
- Do not add emojis (even where existing outputs have them — preserve existing style;
  do not add new ones)

### Architecture Compliance

All modified files are `skill-instruction` type — they are LLM prompt/workflow
instructions, not executable code. Changes are text-level formatting updates only.

The workflow XML parser in bmad-dev-story reads `<output>` blocks as literal text to
display — markdown within them renders correctly because Claude Code displays the
output text in a markdown-aware terminal context.

### Testing Requirements

This story uses EDD (Eval-Driven Development) — see Momentum Implementation Guide below.

### Project Structure Notes

All workflow.md files are under `skills/momentum/skills/{skill-name}/workflow.md`.
There are 18 files to update across Tasks 1–3.

No new files are created. No directory structure changes.

### References

- [Claude Code markdown rendering]: Claude Code renders markdown in stdout — `**bold**`,
  `## headers`, `` `code` ``, `> blockquotes` all apply visual formatting in the terminal
- [Existing story with formatted output]: `_bmad-output/implementation-artifacts/stories/8-3-gemini-deep-research-automation.md` — the completion signal in this story's `create-story/workflow.md` output block is an example of what good looks like
- [Epic Ad-Hoc]: `_bmad-output/planning-artifacts/epics.md` § "Epic Ad-Hoc: Ad-Hoc Work"

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → `skill-instruction` (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Skill instructions are non-deterministic LLM
prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the changes:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/create-story/evals/`
   (evals/ already exists — add to it, or create evals/ in the skill being changed):
   - One `.md` file per eval, named descriptively (e.g.,
     `eval-output-uses-markdown-headers.md`, `eval-output-warns-in-blockquote.md`)
   - Format each eval as: "Given [input and context], the skill should [observable
     behavior — what Claude does or produces]"
   - Test observable formatting behavior, not exact text

   **Suggested evals:**
   - `eval-output-uses-markdown-headers.md`: Given a sprint-planning workflow that
     completes successfully, the output should use `##` section headers to separate
     the sprint summary from the next-steps block, and story slugs should appear in
     bold or inline code
   - `eval-output-warns-in-blockquote.md`: Given a quick-fix workflow that encounters
     a gate failure (e.g., AVFL GATE_FAILED), the output should render the warning in
     a `>` blockquote so it stands out visually from surrounding text
   - `eval-no-behavior-change.md`: Given any workflow step where only `<output>` text
     was updated, the workflow's action sequence, conditional logic, and variable
     placeholders are unchanged — only the human-readable text gained formatting

**Then implement:**
2. Apply formatting to `<output>` blocks in each workflow.md, following the rules in
   Dev Notes above. Work through Tasks 1 → 2 → 3 in order.

**Then verify:**
3. Run evals: for each eval file, spawn a subagent. Give it the eval scenario and load
   the relevant workflow.md as context. Observe whether the subagent's behavior matches
   the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the formatting (e.g., blockquotes not used
   for warnings), revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in
  `references/` with clear load instructions (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12)

> **Note:** No SKILL.md files are modified in this story — only workflow.md output
> blocks. NFR1/NFR3 compliance checks are therefore not applicable to this story's
> deliverables. The NFR checklist below is adjusted accordingly.

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written (in `evals/` of an appropriate skill directory)
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented)
- [ ] All 18 workflow.md files have had their `<output>` blocks reviewed and updated
  where markdown formatting adds value
- [ ] No `<action>`, `<check>`, `<critical>`, `<note>`, or `<ask>` elements modified
- [ ] All variable placeholders (`{{...}}`) preserved unchanged
- [ ] Existing emojis preserved; no new emojis added
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

> **Gherkin specs note:** Gherkin specs for this sprint may exist in
> `sprints/{sprint-slug}/specs/`. The dev agent implements against the plain-English
> ACs in this story file only — never against `.feature` files (Decision 30
> black-box separation).

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
