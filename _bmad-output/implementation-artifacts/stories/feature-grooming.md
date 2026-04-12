---
title: Feature Grooming Skill — Holistic Feature Taxonomy Discovery and Refinement
story_key: feature-grooming
status: ready-for-dev
epic_slug: impetus-epic-orchestrator
depends_on: []
touches:
  - skills/momentum/commands/feature-grooming.md
  - skills/momentum/skills/feature-grooming/SKILL.md
  - skills/momentum/skills/feature-grooming/workflow.md
  - skills/momentum/skills/feature-grooming/evals/eval-bootstrap-synthesizes-feature-list.md
  - skills/momentum/skills/feature-grooming/evals/eval-refine-detects-unmapped-stories.md
  - skills/momentum/skills/feature-grooming/evals/eval-no-mutation-before-approval.md
change_type: skill-instruction
priority: high
---

# Feature Grooming Skill — Holistic Feature Taxonomy Discovery and Refinement

## Description

Create the `momentum:feature-grooming` skill — the holistic feature taxonomy discovery and refinement skill, analogous to `momentum:epic-grooming`. This skill synthesizes the complete feature set for a product from PRD, epics, architecture, and stories (bootstrap mode), and evaluates whether the existing feature set remains coherent and complete (refine mode).

The skill is an orchestrator. It spawns exactly 2 parallel haiku discovery subagents (PRD/epics agent + architecture/stories agent), then handles all synthesis, value analysis, developer interaction, and writing directly.

Key design principle: features are the unit of value delivery. Every feature must include a `value_analysis` (multi-paragraph: current value, full vision, gaps — not just pain removal) and a `system_context` (how it fits the overall product).

## Acceptance Criteria (Plain English)

### Discovery + Mode

1. Mode detection: the skill reports "bootstrap" or "refine" before analysis begins.

2. Parallel discovery: the skill spawns exactly 2 subagents in a single message (PRD/epics agent + architecture/stories agent); neither subagent runs before Phase 1 output is shown to the developer.

3. Bootstrap range: 8–25 features are synthesized in bootstrap mode, with a ! warning if the candidate count falls outside this range.

4. Orchestration: exactly 2 subagents spawned in parallel (haiku, quick) for discovery; orchestrator handles all synthesis, value analysis, and developer interaction directly.

### Value Analysis

5. `value_analysis` required: every proposed feature includes a multi-paragraph `value_analysis` covering (a) current value delivered, (b) full vision including new capabilities beyond pain removal, (c) known gaps; no feature is written to features.json without it.

6. `system_context` required: every proposed feature includes a `system_context` string explaining how it fits and enhances the overall product; no feature is written without it.

7. Value spectrum: `value_analysis` must not reduce to pain removal only; new capabilities, knowledge, and experience dimensions are explicitly considered.

8. Stepping-stone flagging: features with no current delivery or deferred value are flagged ⚠; the developer must explicitly confirm inclusion of each flagged feature.

9. Foundation docs: in bootstrap mode, the skill creates an aes-NNN (value gap assessment) and a dec-NNN (value-first schema decision) in `planning-artifacts/assessments/` and `decisions/` respectively before writing features.json.

### UX + Interaction

10. Acceptance conditions per feature: each follows "A developer can [action] and [observe outcome]" — binary and verifiable.

11. Holistic-first UX: the full candidate set with value analyses is shown before any per-feature gate; the developer gives free-form feedback first.

12. Three review questions asked: (1) feature coverage, (2) value accuracy, (3) deferred-value confirmation for ⚠ features.

13. Six refine signals checked: MERGE / SPLIT / DEDUP / NEW / RETIRE / UPDATE — all reported including zero counts.

### Write Safety

14. No write before approval: features.json is untouched until the Step 5 approval gate is passed.

15. `stories_done`/`remaining` accuracy: computed fresh from stories/index.json at write time; dropped/closed-incomplete stories excluded from remaining.

16. Field preservation in refine: rejected proposals leave their feature entry byte-identical.

17. Type validation: a `type` value outside {flow, connection, quality} is rejected before write.

### Output + Quality

18. Hash reported post-write: `momentum-tools feature-status-hash` is called; result included in final output.

19. Unmapped stories reported: count + slugs if >0 (non-dropped/non-done stories not assigned to any feature).

20. Sort order: written features.json is ordered flow→connection→quality, alpha within type.

21. Task tracking: 4 tasks created at start, each transitioned in-progress→completed as phases run.

22. Commit: conventional commit `docs(features): feature-grooming {bootstrap|refine} — N features, M proposals applied`.

## Tasks / Subtasks

- [ ] Task 1: Write behavioral evals in `skills/momentum/skills/feature-grooming/evals/` (AC: per EDD requirements)
  - [ ] 1.1: Write `eval-bootstrap-synthesizes-feature-list.md` — Given a project with PRD, epics, architecture, and stories but no features.json, the skill should synthesize 8–25 candidate features and present them with value_analysis and system_context before any write
  - [ ] 1.2: Write `eval-refine-detects-unmapped-stories.md` — Given features.json with some stories unassigned, the skill should report unmapped story count and slugs in its final output
  - [ ] 1.3: Write `eval-no-mutation-before-approval.md` — Given a developer who does not confirm the approval gate in Step 5, features.json remains unmodified

- [ ] Task 2: Create the dispatch command at `skills/momentum/commands/feature-grooming.md` (AC: 1–4)
  - [ ] 2.1: Write single dispatch line delegating to the SKILL.md

- [ ] Task 3: Create the feature-grooming SKILL.md at `skills/momentum/skills/feature-grooming/SKILL.md` (AC: 1–4)
  - [ ] 3.1: Write SKILL.md frontmatter: name, description (≤150 chars), model: claude-sonnet-4-6, effort: high
  - [ ] 3.2: Write SKILL.md body delegating to `./workflow.md`

- [ ] Task 4: Create the feature-grooming workflow at `skills/momentum/skills/feature-grooming/workflow.md` (AC: 1–22)
  - [ ] 4.1: Write Step 1 — Mode detection and task setup: detect bootstrap vs. refine, create 4 TaskCreate entries
  - [ ] 4.2: Write Step 2 — Parallel discovery: spawn exactly 2 haiku subagents (PRD/epics + arch/stories) in a single message
  - [ ] 4.3: Write Step 3 — Synthesis and value analysis: merge subagent findings, produce candidate feature list with value_analysis and system_context for each, flag ⚠ stepping-stone features
  - [ ] 4.4: Write Step 4 — Developer review UX: show full candidate set, ask three review questions, collect free-form feedback
  - [ ] 4.5: Write Step 5 — Approval gate: no writes before this gate; on approval, type-validate, sort, compute stories_done/remaining from index, write features.json; for bootstrap write aes-NNN and dec-NNN first
  - [ ] 4.6: Write Step 6 — Post-write: call momentum-tools feature-status-hash, report hash, report unmapped stories, commit with conventional message

## Dev Notes

### Workflow Phases

1. **Mode detection + task setup** — Check whether `features.json` exists to determine bootstrap vs. refine. Announce mode. Create 4 tasks via TaskCreate: (1) Discovery, (2) Synthesis + Value Analysis, (3) Developer Review, (4) Write + Post-write.

2. **Parallel discovery** — Spawn exactly 2 subagents in a single message (model: haiku, effort: quick):
   - Agent A: reads PRD and epics.md, extracts feature candidates and FR groupings
   - Agent B: reads architecture.md and stories/index.json, extracts capability clusters and story themes
   Both return structured lists. Orchestrator does NOT spawn additional agents.

3. **Synthesis + value analysis** — Merge Agent A and Agent B results. Deduplicate. Produce candidate feature list. For each candidate:
   - Write `value_analysis` (3 paragraphs: current value, full vision, known gaps)
   - Write `system_context` (1–2 sentences: how it fits the overall product)
   - Determine `type` (flow / connection / quality)
   - Draft acceptance conditions ("A developer can [action] and [observe outcome]")
   - Flag ⚠ if no current delivery or deferred value
   Validate count is 8–25; warn with ! if outside range.

4. **Developer review** — Present full candidate set with value analyses. Ask three questions:
   1. Are all important features covered, or are there gaps/redundancies?
   2. Do the value analyses accurately reflect each feature's value?
   3. (For ⚠ features only) Confirm each deferred-value feature for inclusion.
   Incorporate feedback before proceeding. For refine mode also report six signals: MERGE / SPLIT / DEDUP / NEW / RETIRE / UPDATE (with counts).

5. **Approval gate + write** — Require explicit approval. Do NOT write features.json before this gate. On approval:
   - Validate all types are in {flow, connection, quality}; reject invalid before write
   - In bootstrap mode: write aes-NNN to `_bmad-output/planning-artifacts/assessments/` and dec-NNN to `_bmad-output/planning-artifacts/decisions/`
   - Compute stories_done and remaining fresh from stories/index.json (exclude dropped/closed-incomplete)
   - Sort output: flow→connection→quality, alpha within type
   - In refine mode: leave rejected feature entries byte-identical

6. **Post-write** — Call `momentum-tools feature-status-hash`; include hash in output. Report unmapped stories (non-dropped/non-done stories not assigned to any feature): count + slugs. Commit: `docs(features): feature-grooming {bootstrap|refine} — N features, M proposals applied`.

### SKILL.md Frontmatter

```yaml
name: feature-grooming
description: "Feature grooming — holistic feature taxonomy discovery, value analysis, and features.json maintenance."
model: claude-sonnet-4-6
effort: high
```

### EDD Order (Mandatory)

Per the Momentum Implementation Guide for skill-instruction stories, evals MUST be written before any skill files. The order is:
1. Write 3 evals in `skills/momentum/skills/feature-grooming/evals/`
2. Implement SKILL.md and workflow.md
3. Run evals via Agent tool subagents; verify behaviors
4. Revise if needed (max 3 cycles)

### Bootstrap vs. Refine Detection

- Bootstrap: `_bmad-output/planning-artifacts/features.json` does not exist or is empty
- Refine: `features.json` exists with at least one feature entry

### features.json Schema Reference

Each feature entry must include at minimum:
- `slug` (string)
- `title` (string)
- `type` (flow | connection | quality)
- `value_analysis` (multi-paragraph string)
- `system_context` (string)
- `acceptance_conditions` (array of strings, "A developer can [action] and [observe outcome]" format)
- `stories_done` (integer, computed from index)
- `remaining` (integer, computed from index)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → skill-instruction (EDD)

---

#### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 3 behavioral evals in `skills/momentum/skills/feature-grooming/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, commands/feature-grooming.md, and workflow.md

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names prefixed `momentum-` or within `momentum:` namespace (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for this story:**
- [ ] 3 behavioral evals written in `skills/momentum/skills/feature-grooming/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] commands/feature-grooming.md dispatch line present
- [ ] AVFL checkpoint on produced artifact documented
