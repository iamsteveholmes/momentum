---
title: AVFL Corpus Mode — Multi-Document Cross-Validation for momentum-avfl
story_key: 8-1-avfl-corpus-mode
status: done
epic_slug: research-knowledge-management
depends_on: []
touches:
  - skills/momentum-avfl/SKILL.md
  - skills/momentum-avfl/references/framework.json
  - skills/momentum-avfl/sub-skills/fixer/SKILL.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/planning-artifacts/epics.md
    relationship: derives_from
    section: "Epic 8: Research & Knowledge Management"
  - path: ~/.claude/plans/fancy-plotting-beaver.md
    relationship: derives_from
    section: "Story 1: AVFL Corpus Mode"
---

# AVFL Corpus Mode — Multi-Document Cross-Validation

## Goal

Extend `momentum-avfl` with first-class corpus mode: the ability to validate a set of
related documents together, so that cross-document contradictions, consistency gaps, and
corpus-level completeness issues are caught before synthesis. Today AVFL validates a single
document; this story adds a `corpus: true` path that accepts an array of file paths and
activates two new validation dimensions.

Extends FR48 (AVFL) with corpus validation mode. Backward compatible: `corpus: false` is the default and
all single-document behavior is unchanged.

## Acceptance Criteria (Plain English)

### Corpus Mode Activation
1. When `corpus: true` is passed, `output_to_validate` accepts an array of file paths
2. When `corpus` is omitted or `corpus: false`, all existing single-document behavior is
   unchanged — existing callers are not affected

### Validator Behavior in Corpus Mode
3. All validators receive all corpus files in their prompts and produce cross-document
   findings
4. Two new dimensions are active only in corpus mode:
   - `cross_document_consistency` — tier 3, coherence lens: detects contradictions,
     conflicting definitions, and version skew across files
   - `corpus_completeness` — tier 2, structural lens: detects coverage gaps where no file
     addresses a required topic or concern
5. Finding `location` field uses `{filename}:{section}` format in corpus mode (e.g.,
   `architecture.md:Data Model`)

### Fixer Behavior in Corpus Mode
6. Fixer receives all files and produces per-file output blocks in its response — one block
   per file in the corpus
7. When `authority_hierarchy` is provided (ordered list of file paths, high to low), fixer
   resolves cross-document contradictions in favor of the higher-authority file and
   annotates fixes with `resolved_by: authority_hierarchy`
8. When no `authority_hierarchy` is provided, contradictions are flagged as
   `unresolved_contradiction` in the fix log (the fixer does not guess)

### Backward Compatibility
9. All existing single-document behavior is unchanged — `corpus: false` is default; no
   existing caller is affected by this change

### EDD — Evals Written Before Implementation
10. Three behavioral evals are written before any skill file is modified:
    - `eval-corpus-cross-document-dimensions.md` — verifies cross_document_consistency and
      corpus_completeness are active and produce cross-file findings
    - `eval-corpus-backward-compatible.md` — verifies single-document invocation is
      unchanged when corpus is omitted
    - `eval-corpus-fixer-authority-resolution.md` — verifies fixer resolves contradictions
      using authority_hierarchy and annotates correctly

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: write before touching any skill file) (AC: 10)
  - [ ] Create `~/.agents/skills/momentum-avfl/evals/eval-corpus-cross-document-dimensions.md`
  - [ ] Create `~/.agents/skills/momentum-avfl/evals/eval-corpus-backward-compatible.md`
  - [ ] Create `~/.agents/skills/momentum-avfl/evals/eval-corpus-fixer-authority-resolution.md`

- [ ] Task 2 — Update `framework.json` with corpus mode additions (AC: 3, 4, 5, 7, 8)
  - [ ] Add `corpus` (bool, default false) and `authority_hierarchy` (ordered file list, optional) to `parameters` object in framework.json
  - [ ] Add `cross_document_consistency` dimension to `tier_3_contextual` under coherence lens with `corpus_only: true`
  - [ ] Add `corpus_completeness` dimension to `tier_2_compositional` under structural lens with `corpus_only: true`
  - [ ] Add 4 corpus prompt template variants: `validator_system_corpus`, `validator_task_corpus`, `consolidator_corpus`, `fixer_corpus`
  - [ ] Update finding schema `location` description for `{filename}:{section}` corpus format
  - [ ] Update finding schema to include optional `resolved_by` field

- [ ] Task 3 — Update `~/.agents/skills/momentum-avfl/SKILL.md` (AC: 1, 2, 3, 4, 5)
  - [ ] Add `corpus` parameter (default: false) to the Parameters table
  - [ ] Add `authority_hierarchy` parameter (optional, default: null) to the Parameters table
  - [ ] Add "Corpus Mode" section after the Parameters section explaining array input,
    activated dimensions, and `{filename}:{section}` location format
  - [ ] Update Phase 1 (VALIDATE) to branch on `corpus: true`: pass all files to
    validators, reference corpus prompt templates from framework.json
  - [ ] Update Phase 4 (FIX) to branch on `corpus: true`: produce per-file output blocks,
    apply authority_hierarchy if provided, emit `unresolved_contradiction` if not

- [ ] Task 4 — Update `~/.agents/skills/momentum-avfl/sub-skills/fixer/SKILL.md` (AC: 6, 7, 8)
  - [ ] Add "Corpus Mode" section describing per-file output block format
  - [ ] Add authority_hierarchy resolution instructions: resolve toward higher-authority
    file, annotate with `resolved_by: authority_hierarchy`
  - [ ] Add unresolved_contradiction instruction: when no authority_hierarchy, flag
    contradiction in fix log as `unresolved_contradiction` rather than guessing

- [ ] Task 5 — Run evals and verify behavior (AC: 10)
  - [ ] Run each eval in `evals/` using subagent per EDD protocol
  - [ ] Confirm all three eval behaviors match expectations or iterate (max 3 cycles)

## Dev Notes

### What exists today

`~/.agents/skills/momentum-avfl/SKILL.md` is the orchestration layer. It defines
parameters, profiles (gate/checkpoint/full), phases (VALIDATE → CONSOLIDATE → EVALUATE →
FIX), and role configuration (model/effort per subagent role). It currently accepts a
single `output_to_validate` value.

`~/.agents/skills/momentum-avfl/references/framework.json` is the complete framework
spec: dimension taxonomy (15 dimensions, 4 tiers, 4 lenses), prompt templates for
validators / consolidator / fixer, finding schema (id, severity, dimension, location,
description, evidence, suggestion), and scoring weights. This is where the two new
dimensions and corpus prompt templates must be added.

`~/.agents/skills/momentum-avfl/sub-skills/fixer/SKILL.md` reads its prompt from
`../../references/framework.json` → `prompts.fixer`. It currently produces a single
corrected artifact. The corpus extension requires it to produce per-file output blocks.

Sub-skills path: `~/.agents/skills/momentum-avfl/sub-skills/` contains:
`validator-enum/`, `validator-adv/`, `consolidator/`, `fixer/`

The `evals/` directory does not yet exist — create it.

### Corpus mode design constraints

- `corpus: false` is default. Any caller that does not pass `corpus: true` takes the
  existing code path with no changes.
- `output_to_validate` shifts from a single value to an array when `corpus: true`. The
  parameter description in the table should make this branching clear.
- The two new dimensions are **only active in corpus mode**. Do not add them to
  single-document lens assignments — that would alter existing scoring behavior.
- `{filename}:{section}` location format is a corpus-mode convention, not a schema change.
  Add it as a note/example in the finding schema section of framework.json rather than
  replacing the existing location field definition.
- Per-file output blocks in the fixer: use a clear delimited format so the caller can
  parse which fixed content belongs to which file. A reasonable convention:
  `### File: {path}\n{corrected_content}` — match whatever framework.json documents.
- `authority_hierarchy` is an ordered array of file paths (index 0 = highest authority).
  Fixer uses it to resolve cross-document contradictions deterministically.
- `unresolved_contradiction` is a log annotation, not a finding. The fixer should not
  invent a resolution when authority is ambiguous — surfacing the conflict is the correct
  output.

### Dimension additions in framework.json

New dimensions to insert in `dimension_taxonomy`:

```json
{
  "id": "cross_document_consistency",
  "tier": 3,
  "lens": "coherence",
  "corpus_only": true,
  "description": "All files in the corpus agree on shared concepts, definitions, version references, and decisions. No contradictions or conflicting statements between documents.",
  "questions": [
    "Does file A state something that file B contradicts?",
    "Are version numbers and API references consistent across all files?",
    "Do files share a consistent vocabulary for the same concepts?"
  ]
},
{
  "id": "corpus_completeness",
  "tier": 2,
  "lens": "structural",
  "corpus_only": true,
  "description": "The corpus collectively addresses all required topics. No critical concern is absent across all files.",
  "questions": [
    "Is there a required topic that no file in the corpus addresses?",
    "Are there implied dependencies or contracts that no file documents?"
  ]
}
```

### NFR compliance

- SKILL.md description field is currently 100 characters — well under the 150-character
  limit. Additions to the body must not push the file over 500 lines. Current SKILL.md is
  234 lines. The corpus additions (parameters, corpus mode section, phase 1 branch, phase 4
  branch) should fit within ~50 lines — total will be ~285 lines, within budget.
- framework.json has no line limit but should stay organized. Add corpus content in clearly
  labeled sections, not scattered inline edits.
- fixer/SKILL.md is 27 lines — plenty of budget for the corpus mode section.

### Testing/EDD approach

All tasks are skill-instruction (modifying SKILL.md files and framework.json). No unit
tests apply. Use EDD: write three behavioral evals first (Task 1), then implement (Tasks
2–4), then verify (Task 5).

The three evals are straightforward behavioral scenarios:
1. Given a corpus of two files with a contradiction in one dimension and a shared coverage
   gap, validators should produce findings with cross_document_consistency and
   corpus_completeness dimensions and `{filename}:{section}` locations.
2. Given a single-document invocation (no corpus param), the pipeline should run exactly
   as it does today — no corpus-specific behavior.
3. Given a corpus with an authority_hierarchy and a contradiction, the fixer should
   produce per-file blocks with the contradiction resolved toward the higher-authority
   file, annotated `resolved_by: authority_hierarchy`.

### Project Structure Notes

All files are under `~/.agents/skills/momentum-avfl/`. This is the installed skill
location. Changes go here directly — there is no separate source tree to sync.

The `evals/` directory must be created — it does not exist today. Other AVFL sub-skills
(`validator-enum/`, `validator-adv/`, `consolidator/`, `fixer/`) are siblings and are not
modified by this story.

### References

- Existing AVFL orchestrator: `~/.agents/skills/momentum-avfl/SKILL.md`
- Framework spec: `~/.agents/skills/momentum-avfl/references/framework.json`
- Fixer sub-skill: `~/.agents/skills/momentum-avfl/sub-skills/fixer/SKILL.md`
- Plan context: `/Users/steve/.claude/plans/fancy-plotting-beaver.md`
- Epic 8 in `_bmad-output/planning-artifacts/epics.md`

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum-avfl/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-corpus-cross-document-dimensions.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, or reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names prefixed `momentum-` (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 3 behavioral evals written in `skills/momentum-avfl/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this automatically — validates the implemented SKILL.md against story ACs)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

### File List
