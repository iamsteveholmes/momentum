# Story 1.1: Repository Structure Established

Status: ready-for-dev

## Story

As a Momentum contributor,
I want the repository to have the correct directory structure,
so that all components can be developed, tested, and packaged from the right locations.

## Acceptance Criteria

**AC1:** Given the Momentum repository is cloned, when the developer inspects the root directory, then:
- `skills/`, `rules/`, `mcp/`, `docs/` directories exist
- `version.md` exists at repo root as the single version source of truth
- No `plugin/` directory exists — all deployment is via `skills/`
- `skills/momentum/references/momentum-versions.json` exists and contains valid JSON with `current_version` string and `versions` object where each version entry has a non-empty `actions` array
- Each action in `momentum-versions.json` contains at minimum: `action` (string), `source` (string), `target` (string)
- `skills/momentum/references/hooks-config.json` exists and contains valid JSON with at least one hook entry
- `skills/momentum/references/mcp-config.json` exists and contains valid JSON

**AC2:** Given the repository structure, when a contributor adds a new Momentum skill:
- It is placed under `skills/momentum-[concept]/SKILL.md`
- Any content exceeding 500 lines or 5000 tokens goes in `skills/momentum-[concept]/references/`

## Tasks / Subtasks

- [ ] Task 1: Create `version.md` at repo root (AC: 1)
  - [ ] 1.1: Write `version.md` with initial version string `1.0.0` and brief description of its role as single version source
  - [ ] 1.2: Verify no `plugin/` directory exists (it doesn't; no action needed — just confirm)

- [ ] Task 2: Scaffold `skills/momentum/` — the Impetus entry-point skill directory (AC: 1)
  - [ ] 2.1: Create `skills/momentum/SKILL.md` as a minimal valid stub (full Impetus implementation is Story 2.1)
  - [ ] 2.2: Create `skills/momentum/references/` directory

- [ ] Task 3: Create `skills/momentum/references/momentum-versions.json` (AC: 1)
  - [ ] 3.1: Write JSON with `current_version: "1.0.0"` and `versions` object containing a `"1.0.0"` entry with non-empty `actions` array
  - [ ] 3.2: Each action must have `action`, `source`, `target` string fields
  - [ ] 3.3: Validate JSON parses without error

- [ ] Task 4: Create `skills/momentum/references/hooks-config.json` (AC: 1)
  - [ ] 4.1: Write JSON with at least one hook entry (use the always-on hook pattern from architecture: PostToolUse lint, PreToolUse file protection, Stop gate)
  - [ ] 4.2: Validate JSON parses without error

- [ ] Task 5: Create `skills/momentum/references/mcp-config.json` (AC: 1)
  - [ ] 5.1: Write JSON with MVP MCP servers: `@modelcontextprotocol/server-git` and a Momentum findings MCP placeholder
  - [ ] 5.2: Validate JSON parses without error

- [ ] Task 6: Scaffold remaining required reference stubs under `skills/momentum/references/` (AC: 1)
  - [ ] 6.1: Create `skills/momentum/references/rules/` directory (bundled advisory rules — written by Impetus on first `/momentum` run; content comes from Epic 3 stories, but the directory must exist now)
  - [ ] 6.2: Create `mcp/findings-server/` directory with a placeholder README so git tracks it

- [ ] Task 7: Verify naming convention compliance for existing skills (AC: 2)
  - [ ] 7.1: Confirm `momentum-create-story/`, `momentum-dev/`, `momentum-plan-audit/` all follow `momentum-[concept]/SKILL.md` pattern ✓ (already correct — no action needed beyond confirmation)
  - [ ] 7.2: Confirm each existing skill's overflow content is in `references/` subdir ✓

## Dev Notes

### What Already Exists (Do Not Recreate)

The following already exist in the repo — verify but do not overwrite:

```
skills/momentum-create-story/   ← Already scaffolded and implemented
skills/momentum-dev/            ← Already scaffolded and implemented
skills/momentum-plan-audit/     ← Already scaffolded and implemented
rules/                          ← Directory exists (has git-discipline.md)
docs/                           ← Directory exists
```

**What is missing and must be created:**
- `version.md` (root)
- `mcp/` (directory — does not exist yet)
- `skills/momentum/` (entire directory — Impetus entry point)
- `skills/momentum/references/momentum-versions.json`
- `skills/momentum/references/hooks-config.json`
- `skills/momentum/references/mcp-config.json`
- `skills/momentum/references/rules/` directory
- `mcp/findings-server/` directory (creates `mcp/` as parent)

### Task 1: `version.md` Format

`version.md` is the **single version source** for all skills. Architecture specifies it at repo root.
Standard git pre-commit hook (Husky/pre-commit framework — NOT a Claude Code hook) validates SKILL.md frontmatter consistency. Format:

```markdown
# Momentum Version

**Current version:** 1.0.0

This file is the authoritative version source for all Momentum skills.
Release tags version all skills together.
```

[Source: architecture.md#Version Management]

### Task 2: `skills/momentum/SKILL.md` Stub

This is the Impetus entry-point skill. **Full implementation is Story 2.1** — do NOT implement the Impetus workflow here. Create a minimal valid SKILL.md stub that satisfies the Agent Skills standard and NFR1 (≤150 char description).

Required frontmatter (from architecture.md#Structural Patterns):

```yaml
---
name: momentum
description: "Impetus — Momentum practice orchestrator. Session orientation, workflow access, install and upgrade management."
model: claude-opus-4-6
effort: normal
---
```

Description character count: 111 characters — within ≤150 limit ✓

Body can be minimal: a single line saying "Impetus orchestrating agent — full implementation in Story 2.1."

**Why `name: momentum` (not `name: momentum-momentum`):** The entry-point skill is the exception to the `momentum-` prefix rule. It uses bare `momentum` for the `/momentum` slash command UX. All OTHER skills use `momentum-[concept]`. [Source: architecture.md#Naming Patterns]

**Why `model: claude-opus-4-6`:** Impetus is an orchestrating agent making complex orchestration decisions — author's judgment that the cognitive hazard rule applies (flagship model for high-stakes outputs). Architecture shows `claude-opus-4-6` as the option for high-stakes outputs; Impetus qualifies as the system's central decision-maker. [Ref: architecture.md#Structural Patterns]

### Task 3: `momentum-versions.json` Schema

Schema from architecture.md Decision 5c, adapted for initial 1.0.0 state. **Do not deviate from the field structure — Impetus reads this file programmatically.**

```json
{
  "current_version": "1.0.0",
  "versions": {
    "1.0.0": {
      "description": "Initial release — repository structure established",
      "actions": [
        {
          "action": "write_file",
          "source": "rules/authority-hierarchy.md",
          "target": "~/.claude/rules/authority-hierarchy.md"
        },
        {
          "action": "write_file",
          "source": "rules/anti-patterns.md",
          "target": "~/.claude/rules/anti-patterns.md"
        },
        {
          "action": "write_file",
          "source": "rules/model-routing.md",
          "target": "~/.claude/rules/model-routing.md"
        },
        {
          "action": "write_config",
          "source": "hooks-config.json",
          "target": ".claude/settings.json",
          "requires_restart": true
        },
        {
          "action": "write_config",
          "source": "mcp-config.json",
          "target": ".mcp.json",
          "requires_restart": false
        }
      ]
    }
  }
}
```

**Validation requirements (AC1):**
- `current_version` must be a string (not number)
- `versions` must be an object
- Each version entry must have a non-empty `actions` array
- Each action must have `action` (string), `source` (string), `target` (string) — all three required

Note: The `rules/authority-hierarchy.md`, `rules/anti-patterns.md`, `rules/model-routing.md` source files don't exist yet (they're Epic 3 scope). That's OK — the version manifest declares what Impetus will deploy; the source files don't have to exist for the manifest to be valid. Impetus will check at runtime.

[Source: architecture.md#Decision 5c]

### Task 4: `hooks-config.json` Schema

This is the always-on hook configuration template Impetus writes to `.claude/settings.json` on first `/momentum` run. Use Claude Code hooks schema. Minimum one hook entry per AC1.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[momentum-lint] ✓ checked file edit — lint/format hook placeholder (Story 3.1 implements)'",
            "timeout": 5
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[momentum-protect] ✓ checked file protection — hook placeholder (Story 3.2 implements)'",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '[momentum-gate] ✓ checked stop conditions — quality gate placeholder (Story 3.3 implements)'",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**Why placeholder commands:** The actual lint and protection scripts are Epic 3 scope (Stories 3.1, 3.2). The hooks-config.json scaffolded here establishes structure; real hook commands are filled in by Impetus upgrade actions as Epic 3 stories complete.

[Source: architecture.md#Decision 5a, FR18-FR21]

### Task 5: `mcp-config.json` Schema

MVP MCP servers per architecture Decision 3c. Format must match `.mcp.json` structure expected by Claude Code.

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "."]
    },
    "momentum-findings": {
      "command": "node",
      "args": ["mcp/findings-server/index.js"],
      "description": "Momentum findings ledger MCP server — read/write findings-ledger.json as a structured resource (placeholder — server implemented in Epic 6)"
    }
  }
}
```

Note: `momentum-findings` server source lives at `mcp/findings-server/` (Epic 6 scope). The config placeholder establishes the structure; actual server implementation is later.

[Source: architecture.md#Decision 3c, Project Structure]

### Task 6: `skills/momentum/references/rules/` and `mcp/findings-server/`

These directories need to be git-trackable. Git doesn't track empty directories.

For `skills/momentum/references/rules/`: The architecture is unambiguous — `skills/momentum/references/rules/` holds **bundled copies** of the advisory rules. Impetus reads from this bundled location and writes them to `~/.claude/rules/` on first `/momentum` run. For Story 1.1, create the directory with a `.gitkeep` — the actual rule files (authority-hierarchy.md, anti-patterns.md, model-routing.md) are Epic 3 scope.

For `mcp/findings-server/`: Create the directory with a placeholder `README.md` noting this is the Momentum findings ledger MCP server, to be implemented in Epic 6.

### Project Structure Notes

**Existing structure is correct:**
- All three existing skills (`momentum-create-story`, `momentum-dev`, `momentum-plan-audit`) follow the `momentum-[concept]/SKILL.md` naming pattern ✓
- All three use `references/` for overflow content ✓
- No `plugin/` directory exists ✓

**Skills directory after this story:**
```
skills/
├── momentum/                    ← NEW: Impetus entry-point (stub, full impl Story 2.1)
│   ├── SKILL.md
│   └── references/
│       ├── momentum-versions.json   ← NEW
│       ├── hooks-config.json        ← NEW
│       ├── mcp-config.json          ← NEW
│       └── rules/                   ← NEW directory (.gitkeep)
├── momentum-create-story/       ← Existing ✓
├── momentum-dev/                ← Existing ✓
└── momentum-plan-audit/         ← Existing ✓
```

**Root after this story:**
```
momentum/
├── version.md         ← NEW
├── mcp/
│   └── findings-server/  ← NEW directory (README.md placeholder)
└── (rest unchanged)
```

### Validation: JSON Files Must Parse

**Do not rely on visual inspection.** Validate each JSON file with:
```bash
cat skills/momentum/references/momentum-versions.json | python3 -m json.tool
cat skills/momentum/references/hooks-config.json | python3 -m json.tool
cat skills/momentum/references/mcp-config.json | python3 -m json.tool
```

All three must exit 0 without errors.

### References

- [Source: epics.md#Story 1.1 — Acceptance Criteria]
- [Source: architecture.md#Deployment Structure — Repository Structure preview]
- [Source: architecture.md#Decision 5c — Installation & Upgrade Manifest (momentum-versions.json schema)]
- [Source: architecture.md#Decision 5a — Global Rules Deployment (hooks-config context)]
- [Source: architecture.md#Decision 3c — MCP Servers (mcp-config content)]
- [Source: architecture.md#Structural Patterns — SKILL.md frontmatter, naming patterns]
- [Source: architecture.md#Project Structure & Boundaries — full repo tree]
- [Source: architecture.md#Version Management — version.md role]

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 2 → skill-instruction (EDD)
- Tasks 1, 3, 4, 5, 6 → config-structure (direct)
- Task 7 → unclassified (verification only — no Momentum-specific guidance; standard bmad-dev-story DoD applies)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-creates-story-from-backlog.md`)
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
- Skill names prefixed `momentum-` (NFR12 — no naming collision with BMAD skills; exception: `skills/momentum/SKILL.md` uses bare `momentum` for entry-point slash command — see Task 2 notes)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this automatically — validates the implemented SKILL.md against story ACs)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write the config or create the directory structure** per the story's acceptance criteria
2. **Verify by inspection:**
   - JSON files: must parse without error (validate with a JSON linter, `jq`, or IDE — do not rely on manual visual inspection)
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

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

### File List
