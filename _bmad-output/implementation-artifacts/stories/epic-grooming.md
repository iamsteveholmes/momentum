---
title: Epic Grooming — Holistic Epic Taxonomy and Story Organization
story_key: epic-grooming
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on: []
touches:
  - skills/momentum/skills/epic-grooming/SKILL.md
  - skills/momentum/skills/epic-grooming/workflow.md
  - skills/momentum/references/templates/epic-template.md
  - _bmad-output/planning-artifacts/epics.md
change_type: skill-instruction
---

# Epic Grooming — Holistic Epic Taxonomy and Story Organization

## Description

Momentum currently has 20 distinct `epic_slug` values across stories/index.json
but only 11 epics registered in epics.md. The remaining 9 slugs emerged
organically during sprint work — stories were assigned to epics that were never
formally defined. This creates taxonomy drift: some slugs overlap
(research-knowledge vs. research-knowledge-management), some represent work
that should fold into existing epics, and the epic list no longer reflects the
actual shape of the project.

The epic-grooming skill reads all stories, PRD, architecture, and epics.md,
then proposes a clean taxonomy — merging organic slugs, splitting where needed,
creating new epic definitions using a standard template, and reclassifying
stories. It uses `momentum-tools sprint epic-membership` for all story
reassignments.

Epics in Momentum are **categories** — long-lived groupings of related work
that never close. They are not bounded work packages. The grooming skill
must respect this: merging, splitting, and creating categories, not closing
or completing them.

Unregistered slugs requiring resolution: `agent-team-model` (5 stories),
`greeting-redesign` (4), `harden-epic-2-foundation` (5),
`impetus-core` (17), `plugin-migration` (6), `process-stories` (4),
`research-knowledge-management` (3).

## Acceptance Criteria (Plain English)

1. A skill exists at `skills/momentum/skills/epic-grooming/SKILL.md` that is
   independently invocable via `/momentum:epic-grooming`. The SKILL.md follows
   plugin conventions: description under 150 chars, `model:` and `effort:`
   frontmatter present, body delegates to `./workflow.md`.

2. An epic template exists at `skills/momentum/references/templates/epic-template.md`
   containing the standard epic definition format: slug, category, strategic
   intent, boundaries, FRs covered, NFRs covered, and current state fields.

3. The skill reads all stories from `stories/index.json`, the current
   `epics.md`, the PRD, and the architecture document to build a complete
   picture of epic usage — identifying every `epic_slug` in use, which are
   registered, which are orphaned, and where overlaps exist.

4. The skill proposes a revised epic taxonomy to the developer, presenting
   each proposed change (merge, split, create, rename) with rationale. No
   mutations happen without explicit developer approval of each change.

5. On approval, the skill updates `epics.md` with new or revised epic
   definitions using the epic template format, and reassigns stories to
   their new epic slugs via `momentum-tools sprint epic-membership`.

6. The skill logs all taxonomy decisions (merges, creates, reassignments)
   via `momentum-tools log` with structured entries that capture the old
   slug, new slug, and rationale for each change.

7. The workflow uses task tracking (TaskCreate/TaskUpdate) for its phases
   to maintain structural state across the analysis.

## Tasks / Subtasks

- [ ] Task 1: Create the epic template at `skills/momentum/references/templates/epic-template.md` (AC: 2)
  - [ ] 1.1: Write the template with all six fields: slug, category, strategic intent, boundaries, FRs covered, NFRs covered, current state
  - [ ] 1.2: Verify the template aligns with the existing epic format in epics.md (Epic List section)

- [ ] Task 2: Create the epic-grooming SKILL.md at `skills/momentum/skills/epic-grooming/SKILL.md` (AC: 1)
  - [ ] 2.1: Write SKILL.md frontmatter with name, description (under 150 chars), model, and effort
  - [ ] 2.2: Write SKILL.md body that delegates to `./workflow.md`

- [ ] Task 3: Create the epic-grooming workflow at `skills/momentum/skills/epic-grooming/workflow.md` (AC: 1, 3, 4, 5, 6, 7)
  - [ ] 3.1: Write Phase 1 — Data collection: read stories/index.json, epics.md, PRD, architecture; enumerate all epic_slug values; identify registered vs. orphaned slugs
  - [ ] 3.2: Write Phase 2 — Taxonomy analysis: identify overlaps, candidates for merge/split/create; draft revised taxonomy using the epic template
  - [ ] 3.3: Write Phase 3 — Developer review: present each proposed change with rationale; collect approval/rejection per change
  - [ ] 3.4: Write Phase 4 — Apply changes: update epics.md; call `momentum-tools sprint epic-membership` for each reassignment; log decisions via `momentum-tools log`

## Dev Notes

### Workflow phases

1. **Data collection** — Read `_bmad-output/implementation-artifacts/stories/index.json`
   to extract all unique `epic_slug` values with story counts. Read
   `_bmad-output/planning-artifacts/epics.md` Epic List section to identify
   registered epics. Cross-reference to produce: registered slugs, orphaned
   slugs, story counts per slug. Also read PRD and architecture for FR/NFR
   coverage context.

2. **Taxonomy analysis** — For each orphaned slug, determine whether it
   should: (a) merge into an existing registered epic, (b) become a new
   registered epic, or (c) split across multiple epics. Consider:
   - Story titles and descriptions for thematic grouping
   - FR/NFR coverage alignment
   - Epic boundaries — what belongs here vs. adjacent epics
   - Epic size — very large epics (impetus-core at 17 stories) may need splitting

3. **Proposal presentation** — Present the full proposed taxonomy to the
   developer in a structured format:
   - For merges: "Merge `old-slug` (N stories) into `target-slug` because..."
   - For new epics: show the full epic template filled out
   - For splits: show which stories move where and why
   The developer approves, rejects, or modifies each proposal individually.

4. **Apply approved changes** — For each approved change:
   - Update `epics.md` with new epic definitions (using the template)
   - Call `momentum-tools sprint epic-membership --story <slug> --epic <new-epic>`
     for each story reassignment
   - Call `momentum-tools log --type decision --message "..."` for each change
   - Present a final summary: epics created, stories reassigned, orphan count

### momentum-tools.py — no changes needed

The existing `sprint epic-membership` subcommand handles story reassignment.
The existing `log` subcommand handles decision logging. No new CLI code.

### SKILL.md frontmatter

```yaml
name: epic-grooming
description: "Epic grooming — holistic taxonomy analysis, orphan resolution, and story reclassification."
model: claude-sonnet-4-6
effort: high
```

### Epic template format

The template at `skills/momentum/references/templates/epic-template.md` uses
this structure for each epic:

```markdown
## Epic: {slug}
**Category:** {one-line — what kind of work lives here}
**Strategic intent:** {2-3 sentences — why this category exists, what product capability it builds}
**Boundaries:** {what belongs here vs. adjacent epics}
**FRs covered:** {list}
**NFRs covered:** {list}
**Current state:** {N done, M remaining}
```

### Files

- `skills/momentum/references/templates/epic-template.md` — reusable epic template
- `skills/momentum/skills/epic-grooming/SKILL.md` — skill definition
- `skills/momentum/skills/epic-grooming/workflow.md` — full workflow instructions

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → skill-instruction (EDD)

---

#### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/epic-grooming/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-identifies-orphaned-slugs.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md and workflow.md

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
- [ ] 2+ behavioral evals written in `skills/momentum/skills/epic-grooming/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] Epic template created at `skills/momentum/references/templates/epic-template.md`
- [ ] AVFL checkpoint on produced artifact documented

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
