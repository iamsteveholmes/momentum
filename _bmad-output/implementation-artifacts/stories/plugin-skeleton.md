---
title: Plugin Skeleton — Create Plugin Root and Manifest
story_key: plugin-skeleton
status: ready-for-dev
epic_slug: plugin-migration
depends_on: []
touches:
  - skills/momentum/.claude-plugin/plugin.json
  - skills/momentum/skills/impetus/SKILL.md
  - skills/momentum/skills/impetus/workflow.md
  - skills/momentum/SKILL.md
change_type: config-structure + skill-instruction
---

# Plugin Skeleton — Create Plugin Root and Manifest

## Goal

Establish the Claude Code plugin root at `skills/momentum/` with a proper
`.claude-plugin/plugin.json` manifest and move Impetus into the nested
`skills/impetus/` directory. This is Phase 1 of the 6-phase plugin migration
and unblocks all subsequent migration stories.

After this story, `skills/momentum/` is a valid Claude Code plugin root that
can be installed via `claude plugin add`. Impetus becomes
`/momentum:impetus` (currently it's just `/momentum`).

## Acceptance Criteria (Plain English)

1. A `.claude-plugin/plugin.json` file exists at `skills/momentum/.claude-plugin/plugin.json`
   with `"name": "momentum"` and valid plugin manifest schema
2. A nested `skills/` directory exists at `skills/momentum/skills/`
3. Impetus SKILL.md lives at `skills/momentum/skills/impetus/SKILL.md` with
   `name: impetus` (not `momentum`) — the plugin namespace prefixes it automatically
4. Impetus workflow.md lives at `skills/momentum/skills/impetus/workflow.md`
5. The old `skills/momentum/SKILL.md` and `skills/momentum/workflow.md` are removed
   (replaced by the nested versions)
6. Impetus evals are moved to `skills/momentum/skills/impetus/evals/`
7. The plugin can be validated with `claude plugin validate` (or manual inspection
   of manifest schema) — the manifest must reference at least the impetus skill
8. All other files in `skills/momentum/` (references/, scripts/, workflows/) remain
   in place — they will be reorganized in later stories

## Dev Notes

### Current state

`skills/momentum/` is currently a flat Agent Skills skill directory:

```
skills/momentum/
├── SKILL.md              <- name: momentum (Impetus orchestrator)
├── workflow.md           <- 59K, the main Impetus workflow
├── evals/                <- 59 eval files
├── references/           <- 15 files (practice-overview, model-routing, etc.)
├── scripts/              <- momentum-tools.py, tests, update-story-status.sh
└── workflows/            <- sprint-dev.md, sprint-planning.md
```

### Target state (this story only)

```
skills/momentum/                      <- Plugin root
├── .claude-plugin/
│   └── plugin.json                   <- { "name": "momentum" }
├── skills/
│   └── impetus/
│       ├── SKILL.md                  <- name: impetus (was: momentum)
│       ├── workflow.md               <- moved from parent
│       └── evals/                    <- moved from parent
├── references/                       <- UNCHANGED (stays at plugin root)
├── scripts/                          <- UNCHANGED (stays at plugin root)
└── workflows/                        <- UNCHANGED (stays at plugin root)
```

### plugin.json schema

Based on Claude Code plugin documentation:

```json
{
  "name": "momentum",
  "version": "0.1.0",
  "description": "Agentic engineering practice — sprint orchestration, quality gates, and workflow automation",
  "skills": ["skills/*/SKILL.md"]
}
```

The `name` field determines the namespace prefix — all skills become `/momentum:<skill-name>`.

### Key decisions

- Impetus SKILL.md `name` field changes from `momentum` to `impetus`. The plugin
  namespace handles the `momentum:` prefix automatically.
- The `description` field in SKILL.md must remain ≤150 characters (NFR1).
- References, scripts, and workflows stay at plugin root for now — they move in
  story `plugin-scripts-hooks-refs`.
- Satellite skills (momentum-avfl, momentum-dev, etc.) are NOT touched in this
  story — they move in `plugin-migrate-skills`.

### What NOT to change

- Do not move satellite skills (momentum-avfl, momentum-dev, etc.) — that's story #2
- Do not consolidate scripts/hooks/references — that's story #3
- Do not update cross-references in other skills — that's story #4
- Do not modify workflow.md content — only move it
- Do not modify any reference files — only move evals

### Error handling

- If `skills/momentum/skills/` already exists (from a prior attempt): check contents,
  warn developer, proceed if empty or offer to clean up
- If `plugin.json` already exists: compare with expected content, update if different

### Requirements Coverage

- Architecture: Plugin Model (Decision 32) — establishes the plugin root and manifest
- PRD FR71: Plugin manifest with `.claude-plugin/plugin.json`
- PRD FR72: `momentum:` namespace for all skills
- Master Plan: Plugin Migration Phase 1

## Tasks / Subtasks

- [ ] Task 1 — Create `.claude-plugin/plugin.json` manifest (AC: 1)
  - [ ] Create `skills/momentum/.claude-plugin/` directory
  - [ ] Write `plugin.json` with name, version, description, skills glob

- [ ] Task 2 — Create nested skills directory and move Impetus (AC: 2–6)
  - [ ] Create `skills/momentum/skills/impetus/` directory
  - [ ] Copy SKILL.md to `skills/momentum/skills/impetus/SKILL.md`
  - [ ] Update `name:` field from `momentum` to `impetus` in the new SKILL.md
  - [ ] Move `workflow.md` to `skills/momentum/skills/impetus/workflow.md`
  - [ ] Move `evals/` to `skills/momentum/skills/impetus/evals/`
  - [ ] Remove old `skills/momentum/SKILL.md` and `skills/momentum/workflow.md`

- [ ] Task 3 — Validate plugin structure (AC: 7–8)
  - [ ] Verify plugin.json parses correctly
  - [ ] Verify Impetus SKILL.md is discoverable at expected path
  - [ ] Verify references/, scripts/, workflows/ remain untouched
  - [ ] Verify no broken symlinks or dangling references within moved files

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → config-structure (direct)
- Tasks 2, 3 → config-structure (direct — file moves and directory creation)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write the config or create the directory structure** per the story's acceptance criteria
2. **Verify by inspection:**
   - JSON files: must parse without error (validate with `jq` or equivalent)
   - Required fields: each required field must be present with the correct type
   - Paths: all referenced paths must exist after creation
   - Version consistency: any version fields must be consistent with related version references
3. **Document** what was created in the Dev Agent Record

**No tests required** for pure config/structure changes.

**DoD items for config-structure tasks:**
- [ ] All JSON files parse without error (validated with a tool)
- [ ] All required fields present with correct types
- [ ] All referenced paths exist after creation
- [ ] Changes documented in Dev Agent Record

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
