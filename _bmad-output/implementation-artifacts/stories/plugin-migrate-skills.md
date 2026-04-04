---
title: Plugin Migrate Skills — Move Satellite Skills into Plugin Structure
story_key: plugin-migrate-skills
status: ready-for-dev
epic_slug: plugin-migration
depends_on:
  - plugin-skeleton
touches:
  - skills/momentum/skills/
  - skills/momentum-avfl/
  - skills/momentum-dev/
  - skills/momentum-create-story/
  - skills/momentum-plan-audit/
  - skills/momentum-sprint-manager/
  - skills/momentum-agent-guidelines/
  - skills/momentum-code-reviewer/
  - skills/momentum-architecture-guard/
  - skills/momentum-upstream-fix/
  - skills/momentum-research/
change_type: config-structure
---

# Plugin Migrate Skills — Move Satellite Skills into Plugin Structure

## Goal

Move all 10 satellite Momentum skills from their current flat `skills/momentum-*/`
directories into the plugin's nested `skills/momentum/skills/*/` structure, stripping
the `momentum-` prefix from directory names. After this story, all Momentum skills live
inside the plugin root and are addressable as `/momentum:<skill-name>`.

## Acceptance Criteria (Plain English)

1. Each of the 10 satellite skills is moved into `skills/momentum/skills/<short-name>/`
   where `<short-name>` is the directory name with `momentum-` prefix stripped
2. Each moved SKILL.md has its `name:` field updated to the short name (e.g.,
   `momentum-avfl` → `avfl`, `momentum-dev` → `dev`)
3. The old `skills/momentum-*/` directories are removed after successful move
4. All sub-directories within each skill (evals/, references/, sub-skills/, scripts/)
   are preserved with their full contents
5. No SKILL.md content is modified beyond the `name:` field — workflow instructions,
   frontmatter (model, effort, description), and body remain identical
6. The plugin's `skills/*/SKILL.md` glob in plugin.json discovers all 11 skills
   (impetus + 10 satellites)

## Dev Notes

### Skills to move

| Current Path | New Path | New Name |
|---|---|---|
| `skills/momentum-avfl/` | `skills/momentum/skills/avfl/` | `avfl` |
| `skills/momentum-dev/` | `skills/momentum/skills/dev/` | `dev` |
| `skills/momentum-create-story/` | `skills/momentum/skills/create-story/` | `create-story` |
| `skills/momentum-plan-audit/` | `skills/momentum/skills/plan-audit/` | `plan-audit` |
| `skills/momentum-sprint-manager/` | `skills/momentum/skills/sprint-manager/` | `sprint-manager` |
| `skills/momentum-agent-guidelines/` | `skills/momentum/skills/agent-guidelines/` | `agent-guidelines` |
| `skills/momentum-code-reviewer/` | `skills/momentum/skills/code-reviewer/` | `code-reviewer` |
| `skills/momentum-architecture-guard/` | `skills/momentum/skills/architecture-guard/` | `architecture-guard` |
| `skills/momentum-upstream-fix/` | `skills/momentum/skills/upstream-fix/` | `upstream-fix` |
| `skills/momentum-research/` | `skills/momentum/skills/research/` | `research` |

### Skills with complex subdirectories

- `momentum-avfl`: has `sub-skills/` (4 sub-skills), `references/` (framework.json),
  `evals/` — all must move intact
- `momentum-research`: has `references/` — must move intact
- `momentum-agent-guidelines`: has `references/` — must move intact

### Move strategy

Use `git mv` for each directory to preserve git history. Process one skill at a time:
1. `git mv skills/momentum-avfl skills/momentum/skills/avfl`
2. Update `name:` in SKILL.md
3. Verify contents intact
4. Repeat for next skill

### What NOT to change

- Do not modify any SKILL.md content beyond the `name:` field
- Do not update cross-references between skills — that's story #4
- Do not move scripts/ or references/ at plugin root — that's story #3
- Do not modify sub-skill SKILL.md name fields — they follow their own naming

### Requirements Coverage

- Architecture: Plugin Model (Decision 32) — all skills under plugin root
- PRD FR72: `momentum:` namespace for all skills
- Master Plan: Plugin Migration Phase 2

## Tasks / Subtasks

- [ ] Task 1 — Move AVFL skill and verify (AC: 1–5)
  - [ ] `git mv skills/momentum-avfl skills/momentum/skills/avfl`
  - [ ] Update SKILL.md `name: avfl`
  - [ ] Verify sub-skills/, references/, evals/ intact

- [ ] Task 2 — Move remaining 9 skills (AC: 1–5)
  - [ ] Move each skill with `git mv`, update `name:` field
  - [ ] Verify each skill's subdirectories intact

- [ ] Task 3 — Verify plugin discovery (AC: 6)
  - [ ] Confirm all 11 skills discoverable via plugin.json glob
  - [ ] Confirm old `skills/momentum-*/` directories are gone

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → config-structure (direct — directory moves and name field updates)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Move each directory** using `git mv` to preserve history
2. **Update `name:` field** in each SKILL.md — the only content change allowed
3. **Verify by inspection:**
   - All subdirectories (evals/, references/, sub-skills/, scripts/) present after move
   - No orphaned files in old locations
   - Plugin glob matches all 11 skills
4. **Document** the full move list in the Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] All 10 skills moved to correct paths
- [ ] All `name:` fields updated
- [ ] All subdirectories preserved
- [ ] Old directories removed
- [ ] Changes documented in Dev Agent Record

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
