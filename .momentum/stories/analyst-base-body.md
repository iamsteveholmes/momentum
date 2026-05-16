---
title: analyst-base-body
story_key: analyst-base-body
status: ready-for-dev
epic_slug: agent-team-model
feature_slug: momentum-agent-role-contracts
story_type: feature
change_type: agent
depends_on: []
touches:
  - skills/momentum/agents/analyst.md
---

# analyst-base-body

## Story

As a Momentum sprint orchestrator,
I want a base body file for the analyst agent role at `skills/momentum/agents/analyst.md`,
so that the Momentum plugin ships a universal, unconditioned analyst agent that can be composed with project-specific context by the agent-composition-pipeline.

## Description

Create `skills/momentum/agents/analyst.md` — the base body definition for the analyst role in Momentum's nine-role universal taxonomy (DEC-020, D1 and D5). The analyst owns assessment documents, requirements analysis, and structured business analysis artifacts. Like all base bodies, this file defines the unconditioned role: role identity, behavioral constraints, output format contract, and document ownership scope. The agent-composition-pipeline adds project-specific context at spawn time.

The analyst is the Momentum equivalent of BMAD's analyst/Mary role — strategic business analysis, structured findings, and requirements elicitation — adapted for orchestrator-spawned (non-interactive) subagent use.

**Why this matters:** Without `analyst.md`, the agent-composition-pipeline has no canonical analyst definition to compose from. Assessment documents and requirements analysis would be produced by the wrong role or not at all, breaking the ownership model DEC-020 establishes.

## Acceptance Criteria

1. `skills/momentum/agents/analyst.md` exists and is valid YAML-frontmatter + markdown agent definition.
2. Frontmatter includes: `name: analyst`, a `description` under 250 characters that front-loads the use case (spawned by orchestrators for structured analysis tasks), a `model` setting, and a `tools` list scoped to read-only tools (Read, Glob, Grep, Bash, ToolSearch).
3. The system prompt opens with a clear role statement establishing the analyst as a strategic business analyst focused on structured findings, requirements clarity, and assessment quality — not implementation.
4. The system prompt declares behavioral constraints: the analyst does not write code, does not modify implementation files, and does not expand scope beyond the analysis task it receives.
5. The system prompt documents file ownership scope: assessment records (`.momentum/handoffs/assessment-*.md`), requirements analysis artifacts, and structured findings documents. The analyst does not own story files, sprint records, or implementation files.
6. The system prompt includes an output format contract describing the structured findings block the analyst emits so orchestrators can parse results reliably.
7. The system prompt includes the standard `## Large File Handling` section (required by agent-skill-development-guide.md) with offset/limit guidance, named large files, search-before-read pattern, and error recovery instruction — under 20 lines.
8. The evals at `skills/momentum/agents/evals/eval-analyst-role-identity.md` and `skills/momentum/agents/evals/eval-analyst-stays-in-scope.md` exist and pass against the implemented `analyst.md`.
9. The Large File Handling eval at `skills/momentum/agents/evals/eval-large-file-guidance-present.md` is updated to include `skills/momentum/agents/analyst.md` in its `files_to_check` list.

## Dev Notes

### Role Identity (per DEC-020 D5)

The analyst is a **strategic business analyst and requirements expert** — Momentum's equivalent of BMAD's Mary/analyst persona, adapted for non-interactive subagent spawning. Core identity elements to capture in the system prompt:

- Produces structured, evidence-backed findings — not opinions
- Elicits requirements through artifact analysis (reads specs, epics, stories, PRD, existing assessments) rather than interactive conversation
- Frames findings in business terms: impact, risk, priority, recommendation
- Writes in structured formats (tables, numbered lists, decision-ready summaries) that orchestrators can parse without ambiguity

The analyst does NOT coach, brainstorm interactively, or generate code. It reads, synthesizes, and structures.

### Behavioral Constraints to Encode

- **Write scope**: may only write to assessment/analysis artifact paths; never to story files, sprint indexes, or implementation files
- **Scope discipline**: executes the analysis task it receives; does not self-expand into adjacent investigations without explicit instruction
- **Neutrality**: presents findings with evidence and recommendations — does not advocate for a predetermined conclusion
- **Non-implementation**: does not produce code, diffs, or implementation suggestions; produces requirements, findings, and structured assessments

### Output Format Contract

The analyst emits a structured output block so orchestrators can parse results. Model it after the pattern used by qa-reviewer and e2e-validator — an `AGENT_OUTPUT_START` / `AGENT_OUTPUT_END` block containing JSON with at minimum: `status`, `artifact_written` (path or null), and `findings_summary`. The full human-readable findings document is written to the appropriate path; the structured block is for the orchestrator's consumption.

### Document Ownership Scope

Per DEC-020 D1 and D5, the analyst owns:
- Assessment records: `.momentum/handoffs/assessment-*.md`
- Requirements analysis artifacts (project-specific paths, resolved at spawn time)
- Structured findings documents produced during analysis tasks

The analyst does NOT own:
- Story files (`.momentum/stories/`)
- Sprint records (`sprints/index.json`, `stories/index.json`)
- Implementation files (anything in `src/`, `lib/`, `skills/` outside its artifact scope)
- Architecture decisions (owned by architect)

### File and Format Conventions

Follow the same frontmatter schema as existing base bodies (`dev.md`, `qa-reviewer.md`, `e2e-validator.md`):
- `name:` kebab-case
- `description:` < 250 chars, front-loaded with use case
- `model: sonnet` (standard for analysis roles)
- `effort: medium`
- `tools:` YAML list — Read-only set: Read, Glob, Grep, Bash, ToolSearch (analyst never needs Write or Edit for its base body; write access is granted by orchestrators per task)

System prompt structure (per agent-skill-development-guide.md):
1. Role statement ("You are...")
2. Scope/constraints ("You focus on...", "You do NOT...")
3. Key behaviors (process steps)
4. Input format (what the analyst receives when spawned)
5. Large File Handling (standard section, under 20 lines)
6. Output format contract

### Eval Format Reference

See existing evals in `skills/momentum/agents/evals/` for format. Each eval has:
- `## Scenario` — Given/When/Then in plain English (not Gherkin)
- `## Expected Behavior` — what correct behavior looks like
- `## Failure Indicators` — what a broken implementation would produce

The two new evals are:
1. **eval-analyst-role-identity.md** — verifies the file contains the required structural elements (role statement, constraints, file ownership, output format, Large File Handling section)
2. **eval-analyst-stays-in-scope.md** — verifies the behavioral constraint: when given an analysis task, the analyst does not attempt to write implementation files, modify story files, or expand scope beyond the task received

### Architecture Compliance

This story implements DEC-020 D5 (three new base bodies needed) for the analyst role. No architectural decisions are modified. The file joins the existing base body set in `skills/momentum/agents/` — no new directories, no changes to plugin manifest beyond including the new file.

### References

- `_bmad-output/planning-artifacts/decisions/dec-020-universal-agent-role-taxonomy-2026-05-16.md` — D1 (nine roles), D5 (three new base bodies)
- `skills/momentum/references/agent-skill-development-guide.md` — frontmatter schema, system prompt structure, Large File Handling requirement
- `skills/momentum/agents/dev.md` — format reference (base body with constraints + structured output)
- `skills/momentum/agents/qa-reviewer.md` — format reference (read-only base body with output contract)
- `skills/momentum/agents/evals/eval-large-file-guidance-present.md` — eval to update with analyst.md

## Tasks

- [ ] **Task 1 — Write evals (EDD first):** Create `skills/momentum/agents/evals/eval-analyst-role-identity.md` and `skills/momentum/agents/evals/eval-analyst-stays-in-scope.md`. These define what correct implementation looks like before any code is written. Do not create `analyst.md` yet.
- [ ] **Task 2 — Implement analyst.md:** Create `skills/momentum/agents/analyst.md` following the dev notes above. Use dev.md and qa-reviewer.md as structural references. Include all required sections: role statement, behavioral constraints, key behaviors, input format, Large File Handling, and output format contract.
- [ ] **Task 3 — Update eval-large-file-guidance-present.md:** Add `skills/momentum/agents/analyst.md` to the `files_to_check` list in the existing Large File Handling eval so the non-regression check covers the new file.
- [ ] **Task 4 — Validate evals pass:** Run the three evals against the implemented `analyst.md` (manually or via grep-based verification). Confirm eval-analyst-role-identity passes, eval-analyst-stays-in-scope passes, and eval-large-file-guidance-present passes with the updated file list.
- [ ] **Task 5 — Commit:** `feat(skills): add analyst base body agent — DEC-020 universal role taxonomy`

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
