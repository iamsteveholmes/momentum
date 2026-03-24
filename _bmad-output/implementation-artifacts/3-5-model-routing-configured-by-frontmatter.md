# Story 3.5: Model Routing Configured by Frontmatter

Status: ready-for-dev

**FRs Covered:** FR23 (model routing via `model:` and `effort:` frontmatter)
**Cross-story contract:** This story elaborates the model-routing-guide stub created in Story 2.1, and replaces the model-routing rule placeholder deployed in Story 1.3. The guide becomes the source of truth; SKILL.md frontmatter and the rule both derive from it.

## Story

As a developer,
I want every Momentum skill and agent to have its model and effort level set by frontmatter,
So that the right model is used for every task automatically — no manual overrides needed.

## Acceptance Criteria

**AC1 — Routing guide documents the full decision framework (FR23):**
Given the model routing guide exists at `skills/momentum/references/model-routing-guide.md`,
When a contributor creates a new Momentum skill or agent,
Then they set `model:` and `effort:` frontmatter according to the routing guide,
And the routing guide documents the default strategy: Sonnet 4.6 at `normal` effort for general skills; Opus for outputs without automated downstream validation (cognitive-hazard tasks) or for orchestration roles where correctness cannot be automatically verified; Haiku for constrained tasks with downstream automated validation; exceptions (e.g. Impetus at `high` effort despite Sonnet) documented per-skill with explicit rationale.
**Note:** The effort vocabulary is `normal|high|low` — not `medium`. Story 2.1 created the stub; Story 3.5 elaborates it into the full decision framework. [Source: `_bmad-output/planning-artifacts/epics.md` — Story 3.5 Note]

**AC2 — Frontmatter is the default model setting (FR23):**
Given a Momentum skill's `model:` and `effort:` frontmatter is set,
When Claude Code invokes the skill,
Then the `model:` frontmatter value is used as the default model for that skill's execution,
And higher-priority settings (e.g. `CLAUDE_CODE_SUBAGENT_MODEL` env var, `availableModels` project configuration) take precedence if set — frontmatter is the default, not an absolute guarantee,
And no developer override is required in the normal case to get correct model behavior.

**AC3 — Guide is source of truth for model updates (FR23):**
Given the model routing guide is updated (e.g. a new model tier releases),
When the guide is applied to existing skills,
Then all Momentum SKILL.md files have their `model:` frontmatter updated to reflect the new guidance,
And the guide is reviewed as the source of truth — changes to model names happen first in the guide, then propagate to frontmatter.

**AC4 — Graceful degradation in non-Claude Code tools (NFR6):**
Given a Momentum skill is deployed in a non-Claude Code tool,
When the tool parses `model:` and `effort:` frontmatter,
Then it either respects them (if supported) or silently ignores them,
And the skill functions correctly in both cases.

**AC5 — Model routing rule replaces placeholder (FR23):**
Given Story 1.3 deployed a model routing rule placeholder to `~/.claude/rules/model-routing.md`,
When Story 3.5 is implemented,
Then the placeholder content is replaced with the full model routing rule derived from the routing guide,
And the rule auto-loads in every Claude Code session and is active for all unspecified routing decisions.

## Tasks / Subtasks

- [ ] Task 1: Elaborate `skills/momentum/references/model-routing-guide.md` into the full decision framework (AC: 1, 3)
  - [ ] 1.1: Replace the stub content with the full routing guide. Required sections:
    - **Default Strategy** — Sonnet 4.6 at `normal` effort for general orchestration and workflow skills
    - **Cognitive Hazard Rule** — Opus 4.6 required for outputs without automated downstream validation; list what qualifies (verifiers, code reviewers, architecture guards, root cause analysis)
    - **Constrained Task Rule** — Haiku for tasks that are simple, deterministic, and followed by automated validation (e.g. consolidators, parsers)
    - **Effort Vocabulary** — explicitly document: `normal` (default), `high` (elevated for complex/unvalidated outputs), `low` (lightweight, explicitly constrained tasks)
    - **Current Assignments table** — list every Momentum skill with `model:`, `effort:`, and one-line rationale
    - **Exception Documentation** — document Impetus (`high` effort despite Sonnet) with explicit rationale
  - [ ] 1.2: Fix the current assignments table: rename `momentum-vfl` → `momentum-avfl` (the skill was renamed); replace all `medium` effort values with `normal`
  - [ ] 1.3: Include full model IDs (`claude-sonnet-4-6`, `claude-opus-4-6`, `claude-haiku-4-5-20251001`) — not short names like `sonnet`

- [ ] Task 2: Replace model routing rule placeholder (AC: 5)
  - [ ] 2.1: Update `skills/momentum/references/rules/model-routing.md` — replace the placeholder comment and one-line stub with the full rule derived from the routing guide. The rule should instruct Claude Code on which model tier to use when not otherwise specified, and reference the routing guide for per-skill assignments.
  - [ ] 2.2: Update `~/.claude/rules/model-routing.md` (the deployed copy) with the same content — this is the live rule that auto-loads in every session. Both the source bundle and the deployed copy must be updated in sync.
  - [ ] 2.3: Add a `replace` action entry to `skills/momentum/references/momentum-versions.json` under a new version entry. First check the current highest version in the file (currently `1.0.0` — use `e.g. 1.1.0` as the next semver increment) so future Impetus installs/upgrades deploy the updated rule:
    ```json
    {
      "action": "replace",
      "group": "rules",
      "scope": "global",
      "source": "rules/model-routing.md",
      "target": "~/.claude/rules/model-routing.md"
    }
    ```

- [ ] Task 3: Audit and fix all Momentum SKILL.md frontmatter (AC: 1, 2, 3)
  - [ ] 3.1: Fix skills using abbreviated model names or wrong effort vocabulary. Confirmed issues (read current state before editing in case changes were made):
    - `skills/momentum-create-story/SKILL.md`: `model: sonnet` → `model: claude-sonnet-4-6`; `effort: medium` → `effort: normal`
    - `skills/momentum-dev/SKILL.md`: `model: sonnet` → `model: claude-sonnet-4-6`; `effort: medium` → `effort: normal`
    - `skills/momentum-plan-audit/SKILL.md`: `model: sonnet` → `model: claude-sonnet-4-6`; `effort: medium` → `effort: normal`
    - `skills/momentum-avfl/sub-skills/fixer/SKILL.md`: `effort: medium` → `effort: normal`
    - `skills/momentum-avfl/sub-skills/validator-enum/SKILL.md`: `effort: medium` → `effort: normal`
  - [ ] 3.2: Verify all other SKILL.md files already use correct full model IDs and vocabulary (no remaining `medium` or short names)
  - [ ] 3.3: Add a cross-reference comment to each corrected SKILL.md pointing to the routing guide: `# Authoritative source: skills/momentum/references/model-routing-guide.md — must match` (use the absolute-style path — `references/model-routing-guide.md` is only meaningful relative to `skills/momentum/` and won't resolve for other skill directories)

- [ ] Task 4: Verify full routing is correct (AC: all)
  - [ ] 4.1: Read `skills/momentum/references/model-routing-guide.md`; verify every Momentum skill appears in the assignments table and no `medium` effort values remain
  - [ ] 4.2: Read `~/.claude/rules/model-routing.md`; verify placeholder comment is gone and full rule content is present
  - [ ] 4.3: Grep all SKILL.md files for `effort: medium` and `model: sonnet` (short name); confirm zero matches
  - [ ] 4.4: Verify `momentum-versions.json` parses without error (`jq . skills/momentum/references/momentum-versions.json`)

## Dev Notes

### What Story 2.1 Created (Existing Stub)

`skills/momentum/references/model-routing-guide.md` currently contains:
- A current assignments table listing 8 skills with model/effort/rationale
- A "Story 3.5 will elaborate this guide" note

Issues in the stub to fix:
- References `momentum-vfl` (old name — renamed to `momentum-avfl`)
- Uses `medium` for effort on 3 skills in the assignments table — wrong vocabulary per architecture (`normal|high|low` only); Task 1.2 replaces all occurrences with `normal`
- No decision framework, just a flat table
- No effort vocabulary definition

### Effort Vocabulary (Architecture Decision — CRITICAL)

Architecture line 634: `effort: normal  # normal | high | low`

The valid values are: `normal`, `high`, `low`. **`medium` is not a valid value.** Any SKILL.md using `effort: medium` must be corrected to `effort: normal`.

### Model ID Format (Architecture Pattern)

Always use full model IDs in frontmatter:
- `claude-sonnet-4-6` (NOT `sonnet`)
- `claude-opus-4-6` (NOT `opus`)
- `claude-haiku-4-5-20251001` (NOT `haiku`)

Short names like `model: sonnet` are informal references — the frontmatter requires the full model ID so Claude Code can resolve it unambiguously.

### Cognitive Hazard Rule

Source: architecture line 661: `model: claude-opus-4-6  # verifiers get flagship — cognitive hazard rule`

Rule: Skills that produce outputs without automated downstream validation get Opus. Rationale: errors in these outputs flow directly to the developer/user with no further catch. Examples:
- `momentum-code-reviewer` — produces a review the human acts on
- `momentum-architecture-guard` — produces a guard finding the human acts on
- `momentum-avfl` (orchestrator) — orchestration role: orchestrates validators and produces a final report the human acts on; no automated system validates the orchestration logic itself
- `momentum-avfl/sub-skills/validator-adv` — adversary validator; findings go to consolidator (automated), so Opus is still appropriate for recall quality

Contrast with consolidator (haiku): the consolidator's output is checked by the human-visible report, so errors are visible. Haiku is appropriate for deterministic merge/score operations.

### Rule Deployment Architecture

`skills/momentum/references/rules/model-routing.md` is the source bundle. Impetus deploys it to `~/.claude/rules/model-routing.md` on install/upgrade via the `add`/`replace` action in `momentum-versions.json`.

For Story 3.5: update the source bundle AND the currently deployed copy (since this is the dev environment where Impetus has already run). Future installations will get the new version via the `replace` action added in Task 2.3.

The global `~/.claude/rules/` path ensures the rule auto-loads in every Claude Code session including subagents — this is by design (authority hierarchy).

### Current SKILL.md Frontmatter State (at time of story creation)

Skills with correct frontmatter (no changes needed):
| Skill | model | effort | Status |
|---|---|---|---|
| momentum (Impetus) | claude-sonnet-4-6 | high | ✓ correct |
| momentum-avfl | claude-opus-4-6 | high | ✓ correct |
| momentum-code-reviewer | claude-opus-4-6 | high | ✓ correct |
| momentum-architecture-guard | claude-opus-4-6 | high | ✓ correct |
| momentum-upstream-fix | claude-opus-4-6 | high | ✓ correct |
| momentum-avfl/consolidator | claude-haiku-4-5-20251001 | low | ✓ correct |
| momentum-avfl/validator-adv | claude-opus-4-6 | high | ✓ correct |

Skills needing fixes:
| Skill | Current | Required fix |
|---|---|---|
| momentum-create-story | `model: sonnet`, `effort: medium` | `model: claude-sonnet-4-6`, `effort: normal` |
| momentum-dev | `model: sonnet`, `effort: medium` | `model: claude-sonnet-4-6`, `effort: normal` |
| momentum-plan-audit | `model: sonnet`, `effort: medium` | `model: claude-sonnet-4-6`, `effort: normal` |
| momentum-avfl/fixer | `effort: medium` | `effort: normal` |
| momentum-avfl/validator-enum | `effort: medium` | `effort: normal` |

**Verify these before editing** — the state may have changed since story creation.

### momentum-versions.json Action Schemas

Existing actions in momentum-versions.json (for reference):
- `"action": "add"` — copies source to target if target doesn't exist
- `"action": "replace"` — overwrites target with source (introduced in Task 2.3 of this story — not yet present)
- `"action": "migration"` — runs a complex migration described in a separate markdown file

For Task 2.3, use `"action": "replace"` (not `"add"`) because the target already exists as a placeholder and must be overwritten.

### Project Structure

Files to modify:
- `skills/momentum/references/model-routing-guide.md` — elaborate stub (MODIFY)
- `skills/momentum/references/rules/model-routing.md` — replace placeholder (MODIFY)
- `~/.claude/rules/model-routing.md` — replace deployed placeholder (MODIFY)
- `skills/momentum/references/momentum-versions.json` — add replace action for model-routing.md (MODIFY)
- 5× SKILL.md files — frontmatter corrections (MODIFY)

Files to read (no modification):
- `_bmad-output/planning-artifacts/architecture.md` lines 625–666 — SKILL.md structural patterns and cognitive hazard rule

### Dependencies

- **Depends on:** Story 2.1 (created model-routing-guide.md stub) — file already exists
- **Depends on:** Story 1.3 (deployed model-routing.md placeholder) — placeholder already exists at `~/.claude/rules/model-routing.md`
- **Soft dependency:** Story 3.4 (dropped) — NFR8 protocol compliance audit moved to Story 7.3; no action needed here

### Testing Standards

This story is `specification` + `skill-instruction` + `config-structure` change types. No unit tests apply. Verify by inspection:
1. `jq . skills/momentum/references/momentum-versions.json` — must parse without error
2. `grep -r "effort: medium" skills/` — must return zero matches
3. `grep -r "model: sonnet\b" skills/` (without version suffix) — must return zero matches
4. Read `~/.claude/rules/model-routing.md` — verify placeholder comment is gone, full rule is present
5. Read `skills/momentum/references/model-routing-guide.md` — verify all skills listed, no `medium` effort, no `momentum-vfl`

### References

- FR23: `_bmad-output/planning-artifacts/epics.md` line 95 (model routing via frontmatter)
- Architecture SKILL.md structural patterns: `_bmad-output/planning-artifacts/architecture.md` lines 625–666
- Architecture model routing decisions: line 78 (model routing principle), line 135 (Impetus routing rationale)
- momentum-versions.json action schemas: `skills/momentum/references/momentum-versions.json`
- Story 2.1 (stub creation): `_bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md`
- Story 1.3 (rule placeholder deployment): `_bmad-output/implementation-artifacts/1-3-first-momentum-invocation-completes-setup.md`

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 (`model-routing-guide.md`) → `specification` (direct authoring)
- Task 2 (`model-routing.md` rule + momentum-versions.json) → `specification` + `config-structure`
- Task 3 (SKILL.md frontmatter fixes) → `skill-instruction` (frontmatter-only corrections — inspect, no EDD needed for value fixes)
- Task 4 (verification) → `config-structure` (inspect)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

1. **Write or update the spec** per acceptance criteria
2. **Verify cross-references:** All references to other documents, files, sections, or identifiers must resolve correctly
3. **Verify format compliance:** The routing guide should follow the pattern established in the existing stub; the rule file should follow the format of `authority-hierarchy.md` and `anti-patterns.md`
4. **Document** what was written or updated in the Dev Agent Record

**Additional DoD items for specification tasks:**
- [ ] All cross-references resolve (model IDs match architecture doc, skill names match actual directories)
- [ ] No `medium` effort values remain in the routing guide
- [ ] `momentum-vfl` removed from guide (renamed to `momentum-avfl`)
- [ ] Rule file placeholder comment removed; full rule content present in both source and deployed copy

---

### skill-instruction Tasks: Frontmatter Value Corrections

These are value corrections, not behavioral additions — EDD does not apply to changing `sonnet` → `claude-sonnet-4-6`. Verify by inspection:

1. **Edit** each SKILL.md's frontmatter per the corrections table in Dev Notes
2. **Verify by inspection:**
   - Full model ID format (`claude-sonnet-4-6` not `sonnet`)
   - Effort vocabulary (`normal` not `medium`)
   - Cross-reference comment present: `# Authoritative source: skills/momentum/references/model-routing-guide.md — must match`
3. **Document** in Dev Agent Record

**DoD items for skill-instruction tasks (frontmatter corrections only):**
- [ ] All 5 corrected SKILL.md files use full model IDs and `normal|high|low` vocabulary
- [ ] No `effort: medium` remains in any SKILL.md under `skills/`
- [ ] Cross-reference comment added to corrected files (or already present)

---

### config-structure Tasks: Direct Implementation

`momentum-versions.json` new version entry — implement directly and verify by inspection:

1. **Add** the new version entry with the `replace` action for `model-routing.md`
2. **Verify by inspection:**
   - `jq . skills/momentum/references/momentum-versions.json` — must parse without error
   - New version entry present with correct `action: replace` (not `add`)
   - `source` and `target` paths match the expected values
3. **Document** in Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] `momentum-versions.json` parses without error
- [ ] New version entry present with `replace` action for `model-routing.md`
- [ ] Version number incremented correctly from current `1.0.0`

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List
