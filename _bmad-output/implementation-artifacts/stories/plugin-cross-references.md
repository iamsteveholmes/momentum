---
title: Plugin Cross-References — Update All Internal References
story_key: plugin-cross-references
status: ready-for-dev
epic_slug: plugin-migration
depends_on:
  - plugin-scripts-hooks-refs
touches:
  - skills/momentum/skills/*/SKILL.md
  - skills/momentum/skills/impetus/workflow.md
  - skills/momentum/references/
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/prd.md
change_type: skill-instruction + specification
---

# Plugin Cross-References — Update All Internal References

## Goal

Update all cross-references across Momentum to reflect the new plugin directory
structure. After this story, every path reference, skill name, spawn prompt, and
convention doc accurately reflects the post-migration layout. This is the final
plugin migration story — after this, Momentum is a fully valid, installable plugin.

## Acceptance Criteria (Plain English)

1. All SKILL.md files reference correct paths to their dependencies (e.g.,
   references/, scripts/, sub-skills/ using plugin-relative paths)
2. Impetus workflow.md references correct paths when spawning subagents or
   loading workflow files (sprint-dev.md, sprint-planning.md)
3. All spawn prompts in workflow files use the correct skill names (e.g.,
   `momentum:dev` not `momentum-dev`)
4. The momentum-tools.py script path references are correct in all files that
   invoke it
5. Architecture document plugin model section reflects actual directory structure
6. PRD plugin-related FRs (FR71, FR72) are consistent with actual implementation
7. No dead references — every path mentioned in a skill file resolves to an
   existing file
8. AVFL sub-skill references (validator-enum, validator-adv, consolidator, fixer)
   use correct paths relative to their new location
9. Eval files reference correct paths if they contain path-based assertions

## Dev Notes

### Categories of references to update

**1. Skill spawn names in workflow files:**
- Impetus workflow.md spawns agents by skill name — update from `momentum-dev`
  to `momentum:dev` (or whatever the correct invocation form is post-plugin)
- Sprint-dev workflow references other skills for AVFL, code-reviewer, etc.

**2. File path references:**
- `skills/momentum-avfl/references/framework.json` → `skills/momentum/skills/avfl/references/framework.json`
- `skills/momentum/scripts/momentum-tools.py` → path stays same (already at plugin root)
- Relative paths within skill files (e.g., `./references/framework.json`) should
  still work if the skill's internal structure didn't change

**3. Documentation references:**
- Architecture.md plugin layout diagram
- PRD skill directory listings
- Master plan plugin root layout (informational — may be retired)

### Search strategy

Use grep/ripgrep to find all references to old paths:
- `skills/momentum-` (old prefix pattern)
- `momentum-dev`, `momentum-avfl`, etc. (old skill names in spawn contexts)
- Any hardcoded paths that assume old layout

### What NOT to change

- Do not modify skill behavior or logic — only references and paths
- Do not modify architecture decisions or PRD requirements — only path/name references
- Do not rename the momentum-tools.py script itself

### Requirements Coverage

- Architecture: Plugin Model (Decision 32)
- PRD FR71, FR72: Plugin manifest and namespace
- Master Plan: Plugin Migration Phase 4

## Tasks / Subtasks

- [ ] Task 1 — Audit all cross-references (AC: 7)
  - [ ] Search for `skills/momentum-` pattern across entire repo
  - [ ] Search for old skill names in spawn/invoke contexts
  - [ ] Build a complete list of references that need updating

- [ ] Task 2 — Update skill file references (AC: 1–4, 8)
  - [ ] Update Impetus workflow.md spawn names and file paths
  - [ ] Update sprint-dev.md and sprint-planning.md references
  - [ ] Update AVFL sub-skill path references
  - [ ] Update any eval files with path assertions

- [ ] Task 3 — Update specification documents (AC: 5–6)
  - [ ] Update architecture.md plugin layout section
  - [ ] Update PRD plugin-related sections
  - [ ] Verify all path references in updated docs resolve

- [ ] Task 4 — Verify zero dead references (AC: 7, 9)
  - [ ] Run search for old patterns — should return zero results
  - [ ] Spot-check 5 critical paths resolve correctly

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 4 → skill-instruction (EDD)
- Task 3 → specification (direct authoring with cross-reference verification)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing changes:**
1. Write 2 behavioral evals in `skills/momentum/skills/impetus/evals/`:
   - `eval-plugin-skill-spawn-names.md` — verifies Impetus spawns skills using
     `momentum:<name>` format after migration
   - `eval-plugin-no-dead-references.md` — verifies no skill file references
     a path that doesn't exist

**Then implement:** Update all cross-references per task list.

**Then verify:** Run evals to confirm spawn names and path resolution.

**NFR compliance:**
- SKILL.md `description` fields must remain ≤150 characters
- `model:` and `effort:` frontmatter must be preserved

**DoD items for skill-instruction tasks:**
- [ ] 2 behavioral evals written
- [ ] EDD cycle ran — all eval behaviors confirmed
- [ ] No dead references remain (grep verification)

### specification Tasks: Direct Authoring with Cross-Reference Verification

1. Update architecture.md and PRD path references
2. Verify all cross-references resolve
3. AVFL checkpoint validates against acceptance criteria

**DoD items for specification tasks:**
- [ ] All cross-references resolve correctly
- [ ] Documents follow existing format conventions

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
