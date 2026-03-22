# Story 1.2: Skills Installable via `npx skills add`

Status: ready-for-dev

## Story

As a developer,
I want to install all Momentum skills with a single command,
so that Impetus and all supporting skills are available in my Claude Code environment immediately.

## Acceptance Criteria

**AC1:** Given a developer has Claude Code installed, when they run `npx skills add momentum/momentum -a claude-code`:
- All Momentum SKILL.md files are installed to `.claude/skills/`
- Each skill's `references/` content is bundled and accessible at runtime
- Momentum skill names are prefixed `momentum-` (except the entry point `momentum`) so no naming collision with BMAD skills is possible

**AC2:** Given the installed skills, when Claude Code starts:
- Each Momentum skill description is ≤150 characters
- The correct Momentum skill is invoked on first attempt when tested manually alongside BMAD skills (validated by spot-check during dogfooding per NFR16)

**AC3:** Given the installed skills in a non-Claude Code tool (e.g. Cursor), when the tool parses the SKILL.md files:
- All SKILL.md files parse without error as valid Agent Skills standard files
- Claude Code-specific frontmatter (`context: fork`, `model:`, `effort:`) is silently ignored and does not cause parse failure

## Tasks / Subtasks

- [ ] Task 1: Create `package.json` at repo root for `npx skills add` compatibility (AC: 1)
  - [ ] 1.1: Write `package.json` with `name`, `version`, `skills` directory pointer (or equivalent field per vercel-labs/skills spec)
  - [ ] 1.2: Verify via `npx skills list` (or equivalent dry-run) that the skills package is discoverable

- [ ] Task 2: Create stub SKILL.md files for planned skills not yet implemented (AC: 1, 2, 3)
  - [ ] 2.1: Create `skills/momentum-vfl/SKILL.md` — stub (full implementation Epic 4)
  - [ ] 2.2: Create `skills/momentum-code-reviewer/SKILL.md` — stub, `context: fork`, `allowed-tools: Read` (full implementation Epic 4)
  - [ ] 2.3: Create `skills/momentum-architecture-guard/SKILL.md` — stub, `context: fork`, `allowed-tools: Read` (full implementation Epic 4)
  - [ ] 2.4: Create `skills/momentum-upstream-fix/SKILL.md` — stub (full implementation Epic 4)

- [ ] Task 3: Audit all existing SKILL.md files for Agent Skills standard compliance (AC: 2, 3)
  - [ ] 3.1: For each SKILL.md in `skills/*/`, verify: `name` and `description` fields present (required by standard)
  - [ ] 3.2: Verify each description is ≤150 characters — count precisely
  - [ ] 3.3: Verify `model:` and `effort:` frontmatter present on all Momentum skills (Momentum NFR, not Agent Skills standard)
  - [ ] 3.4: Verify file size ≤500 lines / 5000 tokens per skill (NFR3)
  - [ ] 3.5: Verify `context: fork` and `allowed-tools: Read` present on momentum-code-reviewer and momentum-architecture-guard

- [ ] Task 4: Verify naming convention compliance for all skills (AC: 1)
  - [ ] 4.1: Confirm all skills follow `momentum-[concept]` pattern except entry point `momentum` (bare name exception)
  - [ ] 4.2: Confirm no name conflicts with installed BMAD skills (BMAD skills use `bmad-*` prefix — no collision possible)

## Dev Notes

### What Story 1.1 Provides (Do Not Recreate)

**Dependency note:** This story depends on Story 1.1 (`1-1-repository-structure-established`) being merged first. Before starting Task 2, verify that `skills/momentum/SKILL.md` exists — if it doesn't, Story 1.1 has not been implemented yet.

Story 1.1 creates:
- `skills/momentum/SKILL.md` — Impetus entry-point stub (bare name `momentum`)
- `skills/momentum/references/momentum-versions.json`, `hooks-config.json`, `mcp-config.json`
- `version.md`, `mcp/findings-server/`

Three skills already exist and are fully implemented (not stubs):
- `skills/momentum-create-story/SKILL.md` — description 128 chars, model/effort present ✓
- `skills/momentum-dev/SKILL.md` — description 99 chars, model/effort present ✓
- `skills/momentum-plan-audit/SKILL.md` — description 100 chars, model/effort present ✓

### Task 1: `package.json` for `npx skills add`

The `npx skills` CLI (by Vercel, github.com/vercel-labs/skills) installs Agent Skills packages from GitHub repos using the format `npx skills add <org>/<repo> -a <agent>`. The command `npx skills add momentum/momentum -a claude-code` means: fetch github.com/momentum/momentum repo, install to `.claude/skills/`.

The CLI requires a `package.json` at the repo root. Based on the vercel-labs/skills README (verified 2026-03-19), the relevant fields are:

```json
{
  "name": "momentum",
  "version": "1.0.0",
  "description": "Momentum — practice system for agentic engineering",
  "skills": "./skills",
  "keywords": ["agent-skills", "momentum", "agentic-engineering"]
}
```

The `"skills"` field points to the directory containing skill subdirectories. The CLI recursively finds all `SKILL.md` files under that directory and installs each `{skill-name}/` folder to the target agent's skills directory (`.claude/skills/` for Claude Code).

**Verification:** After creating `package.json`, run `npx skills list --local` or equivalent to confirm the skills are discoverable without publishing to the registry.

**Important:** The repo must be pushed to github.com/momentum/momentum for the install command to work against the live registry. For local testing, use the local path: `npx skills add ./` or however the CLI supports local installs — check the vercel-labs/skills README for the exact local install flag.

[Source: _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md#Layer 2, architecture.md#Install Experience]

### Task 2: Stub SKILL.md Files for Planned Skills

The architecture specifies these skills in the repo's `skills/` directory. Create minimal valid stubs now — full implementation is in later epics. Each stub must be Agent Skills standard compliant AND satisfy Momentum NFRs (≤150 char description, model, effort).

**momentum-vfl** (Epic 4 — Validate-Fix Loop):

```yaml
---
name: momentum-vfl
description: "Orchestrates validate-fix-loop quality validation. Spawns parallel reviewers across structural, accuracy, coherence, and domain lenses."
model: claude-opus-4-6
effort: high
---

Validate-Fix Loop orchestrator — full implementation in Story 4.X.
```

Description: 135 characters ✓

**momentum-code-reviewer** (Epic 4 — Adversarial Code Review):

```yaml
---
name: momentum-code-reviewer
description: "Adversarial code reviewer with read-only tools. Produces structured findings reports. Invoked by VFL — do not invoke directly."
model: claude-opus-4-6
context: fork
allowed-tools: Read
effort: high
---

Adversarial code reviewer subagent — full implementation in Story 4.X.
```

**momentum-architecture-guard** (Epic 4 — Pattern Drift Detection):

```yaml
---
name: momentum-architecture-guard
description: "Detects pattern drift against architecture decisions. Read-only enforcer. Invoked by Impetus — do not invoke directly."
model: claude-opus-4-6
context: fork
allowed-tools: Read
effort: high
---

Architecture guard subagent — full implementation in Story 4.X.
```

**momentum-upstream-fix** (Epic 4 — Upstream Fix):

```yaml
---
name: momentum-upstream-fix
description: "Traces quality failures upstream to spec, rule, or workflow root cause. Proposes fixes at the right level."
model: claude-opus-4-6
effort: high
---

Upstream fix skill — full implementation in Story 4.X.
```

**Why `model: claude-opus-4-6` for these stubs:**
- `momentum-vfl`: Orchestrates complex parallel validation — cognitive hazard rule applies
- `momentum-code-reviewer` and `momentum-architecture-guard`: Verifier subagents (`context: fork`) always get flagship model (cognitive hazard rule — invisible errors cost more than the price premium)
- `momentum-upstream-fix`: High-stakes root cause analysis

[Source: architecture.md#Structural Patterns, architecture.md#Skills Deployment Classification]

### Task 3: Agent Skills Standard Compliance Rules

The Agent Skills spec (agentskills.io) requires:
- `name`: lowercase + hyphens, max 64 characters (MANDATORY)
- `description`: max 1024 characters per spec, but Momentum NFR1 tightens this to ≤150 (MANDATORY for Momentum)
- SKILL.md file named exactly `SKILL.md` (case-sensitive)

Extra Claude Code frontmatter (`context: fork`, `model:`, `effort:`, `allowed-tools:`) is valid per the spec: "Extra YAML frontmatter fields are silently ignored by tools that don't understand them." [Source: research#Layer 1]

**Compliance checklist per skill:**

| Skill | Name ≤64 | Description ≤150 | model | effort | Notes |
|---|---|---|---|---|---|
| momentum | 8 ✓ | count | required | required | Bare name exception |
| momentum-create-story | 22 ✓ | 141 ✓ | sonnet ✓ | medium ✓ | |
| momentum-dev | 12 ✓ | 147 ✓ | sonnet ✓ | medium ✓ | |
| momentum-plan-audit | 20 ✓ | 132 ✓ | sonnet ✓ | medium ✓ | |
| momentum-vfl | 13 ✓ | count | required | required | stub |
| momentum-code-reviewer | 22 ✓ | count | required | required | context:fork |
| momentum-architecture-guard | 27 ✓ | count | required | required | context:fork |
| momentum-upstream-fix | 21 ✓ | count | required | required | stub |

Count description characters precisely for all stubs before finalizing. The descriptions in Task 2 are approximate — verify the actual character count of whatever description you write.

### Task 4: Naming Convention

No collision risk: BMAD skills use `bmad-*` names (e.g., `bmad-dev-story`, `bmad-create-story`). Momentum skills use `momentum-*`. The entry point `momentum` (bare) is the only exception.

The AC says "Momentum skill names are prefixed `momentum-`" — verify momentum-plan-audit's name field reads `momentum-plan-audit` (it does ✓).

**Note on momentum-dev vs momentum-dev-story:** The architecture spec lists `momentum-dev-story` as a planned skill, but the existing implementation is named `momentum-dev`. This is a deliberate naming choice — `momentum-dev` is the Momentum wrapper, while `bmad-dev-story` is the BMAD implementation it delegates to. No conflict.

### NFR Compliance Summary

- **NFR1 (≤150 chars):** All existing skills pass. Stub descriptions must be counted before committing.
- **NFR2 (≥95% skill matching accuracy):** Name prefix separation (`momentum-` vs `bmad-`) is the primary mechanism. Unique names + good descriptions satisfy this.
- **NFR3 (≤500 lines / 5000 tokens):** All existing SKILL.md files are 8 lines — trivially compliant. Monitor as stub implementations grow.
- **NFR4 (flat skills, no plugin namespacing):** All skills are flat `SKILL.md` files. No plugin directory. ✓
- **NFR5 (valid Agent Skills standard):** Enforced by Task 3 audit.
- **NFR6 (Claude Code frontmatter additive):** `context: fork`, `model:`, `effort:` are extra fields — spec-compliant. ✓

### Project Structure Notes

After this story, `skills/` should contain:
```
skills/
├── momentum/                    ← Entry point (stub from Story 1.1)
│   ├── SKILL.md
│   └── references/
├── momentum-create-story/       ← Implemented ✓
├── momentum-dev/                ← Implemented ✓
├── momentum-plan-audit/         ← Implemented ✓
├── momentum-vfl/                ← NEW stub
├── momentum-code-reviewer/      ← NEW stub (context: fork)
├── momentum-architecture-guard/ ← NEW stub (context: fork)
└── momentum-upstream-fix/       ← NEW stub
```

And repo root should contain:
```
package.json    ← NEW (npx skills add compatibility)
version.md      ← from Story 1.1
```

### References

- [Source: epics.md#Story 1.2 — Acceptance Criteria]
- [Source: _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md#Layer 1, Layer 2]
- [Source: architecture.md#Deployment Structure — Skills Deployment Classification]
- [Source: architecture.md#Implementation Patterns — Naming Patterns, Structural Patterns]
- [Source: architecture.md#Requirements Inventory — NFR1-NFR6]

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 2 → skill-instruction (EDD) — 4 stub SKILL.md files
- Task 1 → config-structure (direct) — `package.json`
- Tasks 3, 4 → unclassified (verification only — no Momentum-specific guidance; standard bmad-dev-story DoD applies)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skills:**
1. Write 2–3 behavioral evals in `skills/momentum-vfl/evals/` (and one eval each for the other stubs is optional since they're stubs — focus evals on the most complex one, momentum-vfl):
   - One `.md` file per eval, named descriptively (e.g., `eval-orchestrates-parallel-reviewers.md`)
   - Format: "Given [describe the input and context], the skill should [observable behavior]"
   - Test behaviors and decisions, not exact output text

**For stubs specifically:** Since Tasks 2.1–2.4 are stubs (not full implementations), the EDD cycle is simplified:
- Write 1 eval per stub asserting the stub's minimal behavior (e.g., "Given the skill is invoked, it should acknowledge it's a stub and explain it's not yet implemented")
- Create the SKILL.md, run the eval, confirm stub behavior matches
- Full EDD cycles run in the implementing epics (Epic 4) when the full workflows are written

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely, not approximately
- `model:` and `effort:` frontmatter fields must be present (FR23)
- `context: fork` and `allowed-tools: Read` must be present on momentum-code-reviewer and momentum-architecture-guard
- Skill names prefixed `momentum-` (NFR12 — no naming collision with BMAD skills; exception: `skills/momentum/SKILL.md` uses bare `momentum` for entry-point slash command)
- SKILL.md body must stay under 500 lines / 5000 tokens (stubs are trivially compliant)

**Additional DoD items for skill-instruction tasks:**
- [ ] 1+ behavioral eval written per stub skill (in respective `evals/` directory)
- [ ] EDD cycle ran — stub behavior confirmed
- [ ] All SKILL.md descriptions ≤150 characters confirmed (count actual characters)
- [ ] `model:` and `effort:` frontmatter present on all 4 stubs
- [ ] `context: fork` and `allowed-tools: Read` on momentum-code-reviewer and momentum-architecture-guard
- [ ] AVFL checkpoint documented (momentum-dev runs automatically)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write `package.json`** per the schema in Task 1 Dev Notes
2. **Verify by inspection:**
   - JSON must parse without error: `cat package.json | python3 -m json.tool`
   - `name`, `version`, `skills` fields present with correct types
   - `skills` field points to `"./skills"` directory
3. **Document** what was created in the Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] `package.json` parses without error (validated with a tool)
- [ ] Required fields present (`name`, `version`, `skills`)
- [ ] Changes documented in Dev Agent Record

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

### File List
