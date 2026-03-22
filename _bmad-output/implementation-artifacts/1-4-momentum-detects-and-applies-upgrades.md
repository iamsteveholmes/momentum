# Story 1.4: Momentum Detects and Applies Upgrades

Status: review

## Story

As a developer,
I want Impetus to detect when my Momentum installation is out of date and guide me through upgrading,
so that I always have the latest rules, hooks, and config without manual intervention.

## Acceptance Criteria

**AC1 — Upgrade detection and execution:**
Given a developer runs `npx skills update` and the package `current_version` in `momentum-versions.json` advances,
When they next invoke `/momentum`,
Then Impetus compares `installed.json` `momentum_version` against `momentum-versions.json` `current_version`
And detects a version mismatch
And presents a summary of what changed in each intermediate version before applying anything
And on approval, applies version actions sequentially through each intermediate version (e.g. 1.0.0 → 1.1.0 → 1.2.0 — not a direct diff from installed to current)
And each intermediate version's actions are presented and confirmed as a group
And hook updates are merged into `.claude/settings.json` — existing non-Momentum hooks are never removed
And updates `installed.json` with the new version and updated component hashes

**AC2 — Hash drift detection:**
Given the hash of installed rules in `installed.json` differs from the hash of the bundled rules,
When `/momentum` is invoked,
Then Impetus surfaces a version-drift warning at session start
And offers to re-apply the rules — developer decides whether to proceed

## Tasks / Subtasks

- [x] Task 1: Extend `skills/momentum/workflow.md` — implement the version-mismatch upgrade path (AC: 1)
  - [x] 1.1: Implement version comparison logic: read `installed.json.momentum_version` and `momentum-versions.json.current_version`; detect mismatch
  - [x] 1.2: Implement multi-version gap resolution: collect all version entries between installed and current; order by version sequence using `from` field chain
  - [x] 1.3: Implement per-version action presentation: for each intermediate version, display description + action list in UX Journey 4 format; wait for [U]/[S] confirmation
  - [x] 1.4: Implement sequential action execution: iterate each intermediate version's actions; execute `write_file` (replace), `update_file` (replace), `write_config` (merge), `update_config` (merge); report each with ✓
  - [x] 1.5: Implement `installed.json` update: after all versions applied, update `momentum_version` to `current_version`, update `installed_at`, recompute component hashes
  - [x] 1.6: Implement [S] skip path: explain that current version continues to work with older config; proceed to session orientation; do NOT update `installed.json` (next invocation will offer again)

- [x] Task 2: Implement hash drift detection and warning (AC: 2)
  - [x] 2.1: At session start (after version-match confirmation), compute `git hash-object` of each installed rules file (`~/.claude/rules/*.md`)
  - [x] 2.2: Compare computed hashes against `installed.json.components.rules-global.hash`
  - [x] 2.3: If mismatch detected, surface warning: "Rules have been modified since Momentum installed them. Re-apply from package?" with [R] Re-apply / [K] Keep modified
  - [x] 2.4: If [R], re-execute the `write_file` actions for rules from the current version's action list; update hash in `installed.json`

## Dev Notes

### Prerequisite: Story 1.3 Provides the Foundation

This story extends the Impetus workflow created in Story 1.3. The startup routing logic in Story 1.3 (Step 1) already includes:

```
Check installed.json exists? → Yes → Compare versions
  Match → session orientation
  Mismatch → VERSION UPGRADE (this story implements)
```

Story 1.3 leaves the version-mismatch branch as a HALT with message. This story replaces that HALT with the full upgrade workflow.

**Before implementing:** Verify `skills/momentum/workflow.md` exists and contains the version-mismatch routing branch. If it doesn't, Story 1.3 is not yet merged — do not proceed.

### Task 1: Multi-Version Sequential Upgrade

The key design principle: **never skip intermediate versions.** If a project is on 1.0.0 and the package is now 1.2.0, Impetus applies 1.0.0 → 1.1.0 first, then 1.1.0 → 1.2.0 — each version's changes presented and confirmed as a group.

**Version chain resolution:**
1. Read `momentum-versions.json` from `${CLAUDE_SKILL_DIR}/references/`
2. Start at `installed.json.momentum_version` (e.g., `"1.0.0"`)
3. Find the next version: scan `versions` entries for one with `"from": "1.0.0"`
4. Repeat until reaching `current_version`
5. If the chain is broken (no entry has `from` matching the current step), surface an error and HALT — do not guess

**Action type semantics:**
- `write_file` / `update_file` — replace target file entirely with source content from `${CLAUDE_SKILL_DIR}/references/`
- `write_config` / `update_config` — merge source into target (add missing keys, preserve existing); same merge logic as Story 1.3's first-install config merge

These action types are defined in the `momentum-versions.json` manifest. The developer implementing this story should handle all four types, even though the current manifest example only uses `write_file`, `write_config`, `update_file`, and `update_config`.

[Source: architecture.md#Decision 5c — multi-version gaps, action types]

### Task 1.3: UX Journey 4 Display Format

Per UX spec, the upgrade display format:

```
  Momentum has been updated to 1.1.0 — your project is configured for 1.0.0.

  Here's what changed and what I need to do:

    · authority-hierarchy.md — revised authority precedence rules
      → update ~/.claude/rules/authority-hierarchy.md

    · mcp-config.json — Findings MCP updated to v2
      → update .mcp.json

  No restart needed for these changes — they take effect immediately.

  Update now, or continue with 1.0.0 for this session?
  [U] Update · [S] Skip for now
```

**Design principles (from UX spec Journey 4):**
- "What changed / what I need to do" pairing is non-negotiable — every action shows both reason and target
- Impetus reads instructions from the manifest; it never guesses what to do
- Skip is always available — older config continues to work
- Multi-version gaps present each version's changes as a group
- Restart signal (`!`) only if any action has `requires_restart: true`
- Upgrade state is never shown again once applied — `installed.json` updated immediately on success

After execution, display:
```
  Updating to Momentum 1.1.0...

  ✓  ~/.claude/rules/authority-hierarchy.md updated
  ✓  .mcp.json updated

  Project is now on Momentum 1.1.0.
```

When hooks config changes:
```
  ✓  .claude/settings.json — hooks updated

  !  Restart Claude Code for updated enforcement hooks to activate.
```

[Source: ux-design-specification.md#Journey 4: Version Upgrade]

### Task 2: Hash Drift Detection

Hash drift detection runs at EVERY session start where versions match (normal path), not just during upgrades. The check order is:

1. Versions match? Yes → check for hash drift BEFORE proceeding to session orientation
2. Compute `git hash-object ~/.claude/rules/authority-hierarchy.md` (and other rule files)
3. Compare against `installed.json.components["rules-global"].hash`
4. If mismatch → surface warning: "I see the rules installed by Momentum have been edited since installation."

**Why this matters:** A developer (or another tool) might manually edit `~/.claude/rules/authority-hierarchy.md`. If Impetus silently overwrites on next version, the developer's changes are lost. The warning gives them the choice.

**Warning format:**
```
  ! Rules modified since Momentum installed them.
    authority-hierarchy.md has been changed (hash mismatch).

  Re-apply from the Momentum package, or keep your edits?
  [R] Re-apply · [K] Keep modified
```

If [R] → re-execute the `write_file` actions for rules from the current version, update hash.
If [K] → proceed to session orientation; do not update hash (warning will recur next session).

[Source: architecture.md#Decision 5c — hash comparison; epics.md Story 1.4 AC2; epics.md Epic 1 Additional "version-drift warning"]

### `installed.json` Update After Upgrade

After all intermediate versions are applied:

```json
{
  "momentum_version": "1.1.0",
  "installed_at": "2026-03-21T15:30:00Z",
  "components": {
    "rules-global": { "version": "1.1.0", "hash": "<new-git-blob-sha>" },
    "hooks":        { "version": "1.0.0" },
    "mcp":          { "version": "1.1.0" }
  }
}
```

Each component's `version` advances only if the upgrade included an action targeting that component. `installed_at` always updates to reflect when the upgrade was applied. Hash is recomputed for `rules-global` using `git hash-object`.

[Source: architecture.md#Decision 5c]

### Project Structure Notes

This story modifies:
```
skills/momentum/
└── workflow.md        ← EXTENDED: add upgrade path + hash drift detection
```

No new files created — this story extends the workflow from Story 1.3. The `momentum-versions.json` format (with multi-version `from` chains) is already established by Story 1.1.

### Previous Story Intelligence

**From Story 1.3:**
- First-install workflow is the foundation; upgrade reuses the same `write_file` / `write_config` action execution functions
- `${CLAUDE_SKILL_DIR}` is the path resolution mechanism — never hardcode
- Merge semantics for `.claude/settings.json` and `.mcp.json` are defined (add missing keys, preserve existing)
- `installed.json` write logic exists — this story updates it, doesn't create it

**From Story 1.1:**
- `momentum-versions.json` schema established with `current_version` and `versions` object
- The 1.0.0 version entry serves as the only version initially — upgrade testing requires adding a 1.1.0 entry (or testing with the architecture's example manifest which has both)

### References

- [Source: epics.md#Story 1.4 — Acceptance Criteria]
- [Source: epics.md#Epic 1 Additional — version-drift warning at session start]
- [Source: architecture.md#Decision 5c — Installation & Upgrade Manifest (multi-version upgrade mechanism, hash comparison)]
- [Source: ux-design-specification.md#Journey 4: Version Upgrade]
- [Source: ux-design-specification.md#Component 9 Install/Upgrade Status]

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → skill-instruction (EDD) — extending `skills/momentum/workflow.md`

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md.** Use EDD:

**Before writing:**
1. Write 3 behavioral evals in `skills/momentum/evals/`:
   - `eval-upgrade-detection-and-execution.md` — Given installed version 1.0.0 and manifest current_version 1.1.0, skill should detect mismatch, present changes with "what changed / what I need to do" format, execute on [U], update installed.json
   - `eval-multi-version-sequential-upgrade.md` — Given installed version 1.0.0 and manifest current_version 1.2.0, skill should apply 1.0.0→1.1.0 then 1.1.0→1.2.0 sequentially (not direct diff), presenting each version as a group
   - `eval-hash-drift-warning.md` — Given installed version matches but rules file hash differs from installed.json hash, skill should warn about modification, offer [R]/[K], NOT silently overwrite

**Then implement:** Extend workflow.md with upgrade and drift detection steps

**Then verify:** Spawn subagent per eval, observe behavior. Max 3 fix cycles.

**NFR compliance:**
- workflow.md total body ≤500 lines (shared with Story 1.3's content — use `references/` for overflow)
- `model: claude-opus-4-6` and `effort: normal` (already set)

**Additional DoD items:**
- [ ] 3 behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all 3 eval behaviors confirmed
- [ ] Multi-version sequential upgrade verified (not direct diff)
- [ ] Hash drift detection tested (modified file triggers warning)
- [ ] [S] skip path verified (installed.json NOT updated, next session offers again)
- [ ] AVFL checkpoint documented

---

## Dev Agent Record

### Agent Model Used

claude-opus-4-6[1m]

### Debug Log References

None — implementation was straightforward; no debugging required.

### Completion Notes List

- Task 1 (AC1): Implemented step 9 (version upgrade) in workflow.md — replaces the previous placeholder GOTO with full upgrade logic. Chain resolution uses `from` field linking. Each intermediate version presented separately with [U]/[S] prompt. Actions execute in order with ✓ confirmation. `installed.json` updated per-version inside the loop (not after the full chain). [S] skip path preserves installed.json unchanged.
- Task 2 (AC2): Implemented step 10 (hash drift detection) in workflow.md. Runs on version-match path before session orientation. Computes `git hash-object` and compares against `installed.json.components.rules-global.hash`. [R] re-applies from package and updates hash. [K] proceeds without changes.
- EDD cycle: All 3 evals PASS on first implementation — no fix cycles needed.
- Dev Notes note on `installed.json` "mcp" component: disregarded — story p1.3 removed MCP from the install workflow; the installed.json schema no longer includes an "mcp" component.
- AVFL result: documented in step 7 of momentum-dev workflow.

### File List

- skills/momentum/workflow.md (modified — added steps 9 and 10, updated routing in step 1)
- skills/momentum/evals/eval-upgrade-detection-and-execution.md (created)
- skills/momentum/evals/eval-multi-version-sequential-upgrade.md (created)
- skills/momentum/evals/eval-hash-drift-warning.md (created)

## Change Log

- feat(skills): implement version upgrade detection and sequential execution in Impetus workflow (step 9) — 2026-03-22
- feat(skills): implement hash drift detection and warning in Impetus workflow (step 10) — 2026-03-22
