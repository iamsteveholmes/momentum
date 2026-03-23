# Story 1.6: Fix `npx skills add` Experience

Status: done

## Story

As a developer,
I want `npx skills add` from the Momentum repo URL to show only the 8 Momentum skills,
so that the install experience matches what the README promises and I don't have to manually filter 90 skills.

## Acceptance Criteria

**AC1 — Correct skill count:**
Given a developer runs `npx skills add https://github.com/iamsteveholmes/momentum -a claude-code`
When the CLI scans the repository for available skills
Then exactly 8 Momentum skills are listed for installation
And no BMAD, AVFL, or other non-Momentum skills from the repository appear in the list

**AC2 — README install commands are correct:**
Given the Momentum README
When a developer reads the install instructions
Then the install command uses the correct CLI syntax (`npx skills add`, not `npx @anthropic-ai/claude-code skills add`)
And the repository URL matches the actual published location (`https://github.com/iamsteveholmes/momentum`)
And no shorthand aliases are used that assume a specific GitHub organization name

**AC3 — End-to-end install works:**
Given the install experience has been fixed
When a developer follows the README install instructions end-to-end on a clean environment
Then the installation completes without manual intervention or workarounds
And all 8 installed skills are functional when invoked via `/momentum`

## Tasks / Subtasks

- [ ] Task 1: Diagnose why `npx skills add` shows 90 skills instead of 8 (AC: 1)
  - [ ] 1.1: Investigate how the `skills` CLI discovers SKILL.md files in a repo — does it respect `package.json` `"skills"` field or does it scan the entire repo tree?
  - [ ] 1.2: Identify all SKILL.md files in the repo outside `skills/` (e.g., `.claude/skills/bmad-*/`, `_bmad/bmm/skills/`, etc.) that are being picked up
  - [ ] 1.3: Research whether `.skillsignore`, `.skillsrc`, or another mechanism exists to exclude paths from skill discovery
  - [ ] 1.4: Document the root cause and chosen fix approach in Dev Agent Record

- [ ] Task 2: Implement the fix to scope skill discovery to only Momentum skills (AC: 1)
  - [ ] 2.1: Apply the fix — either `.skillsignore` to exclude non-Momentum paths, restructure the repo, update `package.json` config, or whatever mechanism the CLI supports
  - [ ] 2.2: Verify exactly 8 skills are discovered: `momentum`, `momentum-architecture-guard`, `momentum-code-reviewer`, `momentum-create-story`, `momentum-dev`, `momentum-plan-audit`, `momentum-upstream-fix`, `momentum-vfl`
  - [ ] 2.3: Verify no BMAD skills (`bmad-*`), AVFL skills (`avfl`), or other non-Momentum SKILL.md files appear

- [ ] Task 3: Fix README install commands (AC: 2)
  - [ ] 3.1: Replace all instances of `npx @anthropic-ai/claude-code skills add momentum/momentum` with `npx skills add https://github.com/iamsteveholmes/momentum`
  - [ ] 3.2: Update all `-a claude-code` and `-a cursor` install commands to use the full repo URL
  - [ ] 3.3: Verify no shorthand aliases remain that assume a GitHub org name

- [ ] Task 4: End-to-end verification (AC: 3)
  - [ ] 4.1: Run `npx skills add https://github.com/iamsteveholmes/momentum -a claude-code` from a clean environment (or simulate by cloning to a temp directory)
  - [ ] 4.2: Confirm exactly 8 skills are listed and installed
  - [ ] 4.3: Invoke `/momentum` and confirm all 8 skills are functional
  - [ ] 4.4: Document verification results in Dev Agent Record

## Dev Notes

### Root Cause Context (from Epic 1 Retro)

The Epic 1 retrospective (Action Item #1) identified:

> Running `npx skills add https://github.com/iamsteveholmes/momentum -a claude-code` shows 90 skills (all BMAD, AVFL, and Momentum skills in the repo) instead of 8 Momentum skills. The CLI scans the entire cloned repo for SKILL.md files rather than respecting the `skills` field in `package.json`.

**Current `package.json`:**
```json
{
  "name": "momentum",
  "version": "1.0.0",
  "description": "Momentum — practice system for agentic engineering",
  "skills": "./skills",
  "keywords": ["agent-skills", "momentum", "agentic-engineering"]
}
```

The `"skills": "./skills"` field points to the correct directory, but the CLI appears to ignore it and scan the entire repo tree. The repo contains many non-Momentum SKILL.md files:
- `.claude/skills/bmad-*/` — BMAD skills (local dev tooling)
- `.claude/skills/avfl/` — AVFL skill (local dev tooling)
- `_bmad/bmm/skills/` — BMM module skills
- Potentially others in nested directories

### The 8 Momentum Skills (canonical list)

These are the ONLY skills that should appear in the install:

| # | Skill Directory | Description |
|---|---|---|
| 1 | `skills/momentum/` | Impetus — the entry point orchestrator |
| 2 | `skills/momentum-architecture-guard/` | Architecture drift detection (context:fork) |
| 3 | `skills/momentum-code-reviewer/` | Adversarial code review (context:fork) |
| 4 | `skills/momentum-create-story/` | Story creation with change-type classification |
| 5 | `skills/momentum-dev/` | Development workflow orchestrator |
| 6 | `skills/momentum-plan-audit/` | Plan audit gate enforcement |
| 7 | `skills/momentum-upstream-fix/` | Upstream fix analysis |
| 8 | `skills/momentum-vfl/` | Validation findings ledger |

All live under `skills/` at repo root. No other SKILL.md files should be exposed to the installer.

### README Commands to Fix

The README currently uses incorrect CLI syntax in multiple locations:

**Current (wrong):**
```bash
npx @anthropic-ai/claude-code skills add momentum/momentum -a claude-code
```

**Correct:**
```bash
npx skills add https://github.com/iamsteveholmes/momentum -a claude-code
```

The `@anthropic-ai/claude-code` prefix is not required — `npx skills` is the correct invocation. The shorthand `momentum/momentum` assumes a GitHub org named `momentum` which doesn't exist — the full URL must be used.

Instances to fix in README.md (approximate line numbers — verify before editing):
- Quick Start section (Tier 1 install command)
- Quick Start section (Tier 2 install command)
- Tier 1 install summary line
- Tier 2 install summary line

### Research Required

Task 1 requires investigating the Agent Skills CLI behavior. Key questions:
1. Does `npx skills add` respect `package.json` `"skills"` field for scoping? (The current `"skills": "./skills"` suggests it should, but the retro says it doesn't.)
2. Is there a `.skillsignore` mechanism (similar to `.npmignore` or `.gitignore`)?
3. Does the CLI support a `"files"` or `"include"` field in `package.json`?
4. What is the latest documentation at https://github.com/vercel-labs/skills and https://agentskills.io?

Use web research to answer these questions before implementing.

### Architecture Compliance

- **Deployment model:** All skills deploy via `npx skills add` — no plugin, no separate installer [Source: architecture.md#Deployment Structure]
- **Install experience:** Single command install, then `/momentum` for setup [Source: architecture.md#Install Experience]
- **Skills directory:** `skills/` at repo root is the canonical location [Source: architecture.md#Repository Structure]

### Previous Story Intelligence

**From Story 1.2 (Skills Installable):** The original story acknowledged local-only verification: "Local install verification is by inspection (repo not yet published)." This was the gap that allowed the broken experience to ship.

**From Story 1.5 (Enforcement Tiers):** README was written with incorrect CLI commands. The tier documentation is correct conceptually but the install commands need fixing.

**From Epic 1 Retro:** "Validation was by inspection ('JSON parses, fields present') — nobody ran the actual install command from outside the repo."

### Dependencies

**Depends on Story 1.7** (Acceptance Testing Process and Standards) — this story needs the acceptance test standard to include an Acceptance Test Plan section. However, the implementation work (Tasks 1-4) can proceed independently. The Acceptance Test Plan will be backfilled once Story 1.7 defines the standard.

### Project Structure Notes

- `package.json` at repo root — controls npm/skills metadata
- `skills/` at repo root — the 8 Momentum skills
- `.claude/skills/` — local dev tooling (BMAD, AVFL) — must NOT be exposed to installer
- `_bmad/bmm/skills/` — BMM module skills — must NOT be exposed to installer
- `README.md` at repo root — install instructions to fix

### References

- [Source: epics.md#Story 1.6 — Fix `npx skills add` Experience]
- [Source: epics.md#Epic 1b — Foundation Fixes]
- [Source: epic-1-retro-2026-03-22.md#Challenges — Critical: End-to-end install experience never tested]
- [Source: epic-1-retro-2026-03-22.md#Action Item #1]
- [Source: architecture.md#Install Experience]
- [Source: architecture.md#Deployment Structure]
- [Source: architecture.md#Repository Structure]
- [Source: 1-5-enforcement-degrades-gracefully-across-tool-tiers.md — README structure and tier documentation]

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → unclassified (investigation/research — no Momentum-specific guidance; standard bmad-dev-story DoD applies)
- Task 2 → config-structure (package.json and/or .skillsignore config changes)
- Task 3 → unclassified (README documentation fix — standard bmad-dev-story DoD applies)
- Task 4 → unclassified (end-to-end verification — standard bmad-dev-story DoD applies)

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

### Debug Log References

### Completion Notes List

### File List
