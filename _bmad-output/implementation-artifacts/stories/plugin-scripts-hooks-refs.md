---
title: Plugin Scripts, Hooks, and References — Consolidate at Plugin Root
story_key: plugin-scripts-hooks-refs
status: ready-for-dev
epic_slug: plugin-migration
depends_on:
  - plugin-migrate-skills
touches:
  - skills/momentum/hooks/
  - skills/momentum/hooks/hooks.json
  - skills/momentum/scripts/
  - skills/momentum/references/
change_type: config-structure + rule-hook
---

# Plugin Scripts, Hooks, and References — Consolidate at Plugin Root

## Goal

Consolidate scripts, hooks, and references at the plugin root level. Scripts and
references already live at `skills/momentum/` — verify their placement matches the
target layout. Create the hooks directory with `hooks.json` for always-on hooks that
activate on plugin install.

## Acceptance Criteria (Plain English)

1. `skills/momentum/scripts/momentum-tools.py` exists at the plugin root level
   (already there — verify, do not move)
2. `skills/momentum/references/` exists at the plugin root level with all current
   reference files (already there — verify, do not move)
3. `skills/momentum/hooks/hooks.json` exists with the always-on hook definitions
   that should activate on plugin install
4. The hooks.json file follows the Claude Code hooks schema and defines at minimum
   the hooks that Momentum requires to be always-active
5. Any skill-specific references that were in satellite skill directories before
   migration (e.g., `avfl/references/framework.json`) remain inside their skill
   directory — only shared/global references live at plugin root
6. The `workflows/` directory at plugin root (sprint-dev.md, sprint-planning.md)
   is evaluated: if these are consumed by skills that have moved into
   `skills/momentum/skills/`, they should move to the consuming skill's directory
   or remain at root if shared across multiple skills

## Dev Notes

### Current state (after plugin-migrate-skills)

```
skills/momentum/                      <- Plugin root
├── .claude-plugin/plugin.json
├── skills/                           <- All 11 skills nested here
│   ├── impetus/
│   ├── avfl/                         <- Has its own references/framework.json
│   ├── dev/
│   └── ...
├── references/                       <- Already at plugin root (15 files)
├── scripts/                          <- Already at plugin root (3 files)
└── workflows/                        <- sprint-dev.md, sprint-planning.md
```

### Target state

```
skills/momentum/                      <- Plugin root
├── .claude-plugin/plugin.json
├── skills/                           <- All 11 skills
├── hooks/
│   └── hooks.json                    <- NEW: always-on hooks
├── references/                       <- VERIFY: shared references stay here
├── scripts/                          <- VERIFY: momentum-tools.py stays here
└── workflows/                        <- EVALUATE: move to consuming skills or keep shared
```

### hooks.json content

The hooks that Momentum should activate on install. Review existing hook
configurations in the project to determine which hooks are always-on vs.
workflow-specific. At minimum:

- Any PostToolUse hooks that enforce quality checks
- Any PreToolUse hooks that protect files

Reference the current `.claude/settings.json` for existing hook patterns.

### workflows/ directory decision

`sprint-dev.md` and `sprint-planning.md` are consumed by Impetus workflow.md
which references them. If they're only consumed by Impetus, they should move
into `skills/impetus/workflows/`. If shared across skills, keep at root.
Check the consuming references before deciding.

### What NOT to change

- Do not modify reference file contents — only verify placement
- Do not modify script contents
- Do not update cross-references — that's story #4

### Requirements Coverage

- Architecture: Plugin Model (Decision 32) — hooks/, scripts/, references/ at plugin root
- Master Plan: Plugin Migration Phase 3

## Tasks / Subtasks

- [ ] Task 1 — Verify scripts and references placement (AC: 1–2, 5)
  - [ ] Confirm momentum-tools.py at plugin root scripts/
  - [ ] Confirm all 15 reference files at plugin root references/
  - [ ] Confirm skill-specific references (avfl/references/) stayed in skill dir

- [ ] Task 2 — Create hooks directory and hooks.json (AC: 3–4)
  - [ ] Create `skills/momentum/hooks/` directory
  - [ ] Analyze existing hook configurations to determine always-on hooks
  - [ ] Write `hooks.json` following Claude Code hooks schema

- [ ] Task 3 — Evaluate and resolve workflows/ placement (AC: 6)
  - [ ] Trace references to sprint-dev.md and sprint-planning.md
  - [ ] Move to consuming skill directory or document why they stay at root

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → config-structure (direct — verification only)
- Task 2 → rule-hook (functional verification)
- Task 3 → config-structure (direct — file move decision)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection.

**DoD items for config-structure tasks:**
- [ ] Scripts and references verified at correct locations
- [ ] No orphaned or misplaced files
- [ ] Changes documented in Dev Agent Record

### rule-hook Tasks: Functional Verification

1. **Write the hooks.json** per Claude Code hooks schema
2. **State expected behavior** for each hook as a testable condition
3. **Verify functionally:** confirm hooks.json parses, hook entries match required format
4. **Document** verification result in Dev Agent Record

**DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as testable condition
- [ ] hooks.json parses without error
- [ ] Hook entries match Claude Code hooks schema
- [ ] Format matches established patterns

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
