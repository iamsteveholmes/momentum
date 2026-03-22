# Story 1.3: First `/momentum` Invocation Completes Setup

Status: ready-for-dev

## Story

As a developer,
I want invoking `/momentum` for the first time to automatically configure my environment,
so that I never have to run a separate setup command or manually edit config files.

## Acceptance Criteria

**AC1 — First install detection and consent:**
Given a developer has run `npx skills add` but `.claude/momentum/installed.json` does not exist in the project,
When they invoke `/momentum` for the first time,
Then Impetus reads `momentum-versions.json` from its own bundled `references/` directory
And detects the absence of `installed.json` — identifies this as a first install
And presents the developer with a summary of all files that will be written before taking any action
And waits for explicit developer approval before proceeding
And if the developer declines [S], Impetus explains that setup is required for full functionality, offers to run it again later, and proceeds to session orientation in a degraded state

**AC2 — First install execution:**
Given the developer approves the setup summary,
When Impetus executes the first-install actions,
Then rules files are written to `~/.claude/rules/` from bundled `references/rules/`
And hooks config is **merged** into `.claude/settings.json` — existing keys are preserved, only Momentum-specific hook entries are added, no existing hooks are overwritten or removed
And `.mcp.json` is written from bundled `references/mcp-config.json`
And `showTurnDuration: true` is set in `.claude/settings.json`
And `.claude/momentum/installed.json` is written recording `momentum_version`, `installed_at`, and a hash for each written component (see Dev Notes Task 5 for precise schema — only `rules-global` carries a hash; `hooks` and `mcp` carry version only)
And Impetus confirms to the developer exactly which files were written

**AC3 — Idempotence:**
Given setup is run again (e.g. developer deleted `installed.json` to force re-setup),
When Impetus executes the first-install actions a second time,
Then the result is identical to the first run — no duplicate hook entries, no file corruption

**AC4 — Post-setup session behavior:**
Given setup completes,
When the developer starts a new Claude Code session,
Then rules in `~/.claude/rules/` auto-load in every session including subagents
And always-on hooks (PostToolUse lint, PreToolUse file protection, Stop gate) are active in `.claude/settings.json`

**AC5 — Version-match skip:**
Given `.claude/momentum/installed.json` already exists and its version matches `current_version` in `momentum-versions.json`,
When `/momentum` is invoked,
Then Impetus skips setup entirely and proceeds directly to session orientation

**AC6 — Team member joining:**
Given a second team member clones a project where Impetus has already run setup,
When they run `npx skills add` and invoke `/momentum`,
Then Impetus reads the existing `installed.json` committed to the repo
And detects that project-level config is already present
And only runs global setup steps (rules to `~/.claude/rules/`) if those are missing from the new machine
And does not re-write project-level config already committed to the repo

**AC7 — installed.json git tracking:**
Given setup has completed and `.claude/momentum/installed.json` has been written,
When the developer inspects the project's version control state,
Then `.claude/momentum/installed.json` is tracked in git (not gitignored)
And `.gitignore` does not contain an entry excluding `.claude/momentum/installed.json`

## Tasks / Subtasks

- [ ] Task 1: Implement `skills/momentum/workflow.md` — the Impetus first-install workflow (AC: 1–7)
  - [ ] 1.1: Write Step 1 — startup routing: read `momentum-versions.json` and `installed.json`; determine: first-install | version-mismatch | current; dispatch accordingly
  - [ ] 1.2: Write Step 2 — first-install consent: compose pre-consent summary from version 1.0.0 actions; display in UX Journey 0 format; wait for [Y]/[S]
  - [ ] 1.3: Write Step 3 — action execution: iterate `versions["1.0.0"].actions`; execute `write_file` and `write_config` actions; report each with ✓; surface restart notice if any action has `requires_restart: true`
  - [ ] 1.4: Write Step 4 — `write_config` merge logic: read existing `.claude/settings.json`; merge Momentum hook entries under existing `hooks` object (add missing keys, never overwrite existing); set `showTurnDuration: true`; write result
  - [ ] 1.5: Write Step 5 — write `installed.json`: record `momentum_version`, `installed_at` (ISO 8601), and per-component hash using `git hash-object <file>` for each written file
  - [ ] 1.6: Write Step 6 — team member joining path: detect that `installed.json` exists but global rules (`~/.claude/rules/*.md`) are absent from this machine; run only global setup steps; skip project-level config that is already committed
  - [ ] 1.7: Write Step 7 — [S] decline path: explain what's missing, offer to re-run, proceed to session orientation with degraded enforcement

- [ ] Task 2: Implement `skills/momentum/references/practice-overview.md` — loaded by Impetus for session orientation (AC: 1, 5)
  - [ ] 2.1: Write brief (≤500 tokens) orientation content: what Momentum is, the eight principles, where to start for new developers

- [ ] Task 3: Implement `installed.json` schema at `.claude/momentum/installed.json` for the first test install (AC: 2, 7)
  - [ ] 3.1: After workflow.md is implemented and evals pass, run a test install in the repo itself (dogfooding NFR16) — confirm installed.json is written with correct schema
  - [ ] 3.2: Confirm `.claude/momentum/installed.json` is NOT in `.gitignore`
  - [ ] 3.3: Stage and note the file for commit (momentum-dev will propose the commit)

## Dev Notes

### Prerequisites: What Stories 1.1 and 1.2 Provide

This story implements the Impetus workflow. It depends on Story 1.1 having created:
- `skills/momentum/SKILL.md` (stub — this story replaces the body with a workflow.md reference)
- `skills/momentum/references/momentum-versions.json` — the action manifest Impetus reads
- `skills/momentum/references/hooks-config.json` — the hook template Impetus merges
- `skills/momentum/references/mcp-config.json` — the MCP template Impetus writes
- `skills/momentum/references/rules/` — the bundled advisory rule files

**Before implementing:** Verify `skills/momentum/references/momentum-versions.json` exists. If it doesn't, Story 1.1 is not yet merged — do not proceed until it is.

### Task 1: Impetus Workflow Architecture

Impetus is a **flat skill** (not `context: fork`) — it runs in the main context and persists persona across interactions. It must NOT spawn sub-contexts for setup operations; it performs all file operations itself via Write/Edit/Bash tools.

**Startup routing logic (Step 1):**

```
Read: ${CLAUDE_SKILL_DIR}/references/momentum-versions.json
  → current_version = manifest.current_version

Check: .claude/momentum/installed.json exists?
  No → First install (Step 2 — Journey 0)
  Yes → Compare installed.momentum_version vs current_version
    Match → Skip to session orientation (Step 7 / session ledger display)
    Mismatch → Version upgrade (Story 1.4 scope — HALT here with message)
```

**CRITICAL: `${CLAUDE_SKILL_DIR}`** — Impetus locates its own bundled references via the `CLAUDE_SKILL_DIR` environment variable, which Claude Code sets to the skill's installation directory (e.g., `.claude/skills/momentum/`). Never hardcode the path. Always use `${CLAUDE_SKILL_DIR}/references/...`.

[Source: architecture.md#Decision 5a — "Impetus uses `${CLAUDE_SKILL_DIR}` to locate its own skill directory"]

### Task 2: Pre-Consent Summary Format (UX Journey 0)

The exact display format from UX spec (Journey 0):

```
  Momentum 1.0.0 — first time here

  Before we get started, I need to configure a few things for this project:

    · 3 global rules → ~/.claude/rules/
      (authority hierarchy, anti-patterns, model routing)
    · Enforcement hooks → .claude/settings.json
    · MCP servers → .mcp.json

  After setup, you'll need to restart Claude Code once for the
  enforcement hooks to activate. Rules and MCP are available immediately.

  Set up now?
  [Y] Yes · [S] I'll handle it manually
```

**Design principles (from UX spec):**
- Never install anything without showing what will happen and getting consent
- Each install action reported individually — no "done" without showing the work
- `!` restart signal is clear but not blocking; conversation continues
- Setup failure surfaces with specific diagnosis, not a generic error
- Impetus never uses "Step N/M" — always narrative

[Source: ux-design-specification.md#Journey 0: First-Time Install]

### Task 3: Action Execution — `write_file` and `write_config`

The `momentum-versions.json` actions list for version 1.0.0:

```json
{
  "action": "write_file",
  "source": "rules/authority-hierarchy.md",
  "target": "~/.claude/rules/authority-hierarchy.md"
}
```

**`write_file` implementation:**
- `source` is relative to `${CLAUDE_SKILL_DIR}/references/` — resolve to full path
- `target` supports `~` expansion — resolve `~` to `$HOME`
- Read source, write to target (create parent dirs if needed)
- Idempotent: re-writing the same file is safe; content is replaced

```json
{
  "action": "write_config",
  "source": "hooks-config.json",
  "target": ".claude/settings.json",
  "requires_restart": true
}
```

**`write_config` implementation for `.claude/settings.json` (MERGE, not overwrite):**
1. Read existing `.claude/settings.json` (or start with `{}` if absent)
2. Read `${CLAUDE_SKILL_DIR}/references/hooks-config.json`
3. For each hook event key in hooks-config.json (`PostToolUse`, `PreToolUse`, `Stop`):
   - If key does not exist in settings.json → add it entirely
   - If key exists → append only the Momentum entries that aren't already present (match by `command` value)
4. Set `showTurnDuration: true` at the root level of the settings object
5. Write the merged result back — do NOT remove any existing keys

**`write_config` implementation for `.mcp.json`:**
- `.mcp.json` uses `mcpServers` structure — same merge pattern: add missing keys, preserve existing
- Source: `${CLAUDE_SKILL_DIR}/references/mcp-config.json`
- **Note:** The source AC2 says `.mcp.json` is "written" — this is loose language. Architecture Decision 5c explicitly defines this action as `write_config` (not `write_file`), meaning merge semantics apply. The authoritative action definition is the manifest, not the AC wording.

**Idempotence test:** Running setup twice must produce identical output. For hooks, check by `command` string; for MCP, check by server name key. Never duplicate.

[Source: architecture.md#Decision 5a, architecture.md#Decision 5c; epics.md Story 1.3 AC2 "merged", AC3 "no duplicate hook entries"]

### Task 4: `showTurnDuration: true`

This is an **Epic 1 Additional Requirement** — no PRD FR backs it. Implementation authority: epics.md Epic 1 Additional section.

```json
{
  "showTurnDuration": true,
  "hooks": { ... }
}
```

Add `showTurnDuration: true` at the root of `.claude/settings.json` during the hooks merge step. It is a cost observability feature — shows API turn duration in the UI. Set it alongside hook config merge, not as a separate step.

[Source: epics.md Story 1.3 AC2 note; epics.md Epic 1 Additional section]

### Task 5: `installed.json` Schema

Written to `.claude/momentum/installed.json` after all actions complete:

```json
{
  "momentum_version": "1.0.0",
  "installed_at": "2026-03-21T00:00:00Z",
  "components": {
    "rules-global": { "version": "1.0.0", "hash": "<git-blob-sha>" },
    "hooks":        { "version": "1.0.0" },
    "mcp":          { "version": "1.0.0" }
  }
}
```

**Hash computation:** `git hash-object ~/.claude/rules/authority-hierarchy.md` — run via Bash tool. Record the SHA in `rules-global.hash`. Hooks and MCP don't get hashes in v1.0.0 (hash field omitted or null is acceptable).

**Git tracking:** `.claude/momentum/installed.json` MUST be tracked in git (committed, not gitignored). This enables team members who clone the repo to detect that project-level setup is already done (AC6). Verify by checking `.gitignore` does not exclude `.claude/momentum/`.

[Source: architecture.md#Decision 5c, epics.md Story 1.3 AC7]

### Task 6: Team Member Joining Path (AC6)

Detection logic:
1. `installed.json` exists → project-level config is present
2. Check if `~/.claude/rules/authority-hierarchy.md` exists on this machine
3. If global rules are absent → run only global setup steps (`write_file` actions targeting `~/.claude/rules/`)
4. Skip `write_config` actions (hooks already in `.claude/settings.json` in the repo) and `write_config` for `.mcp.json`

This path should NOT prompt with the full consent flow (confusing for a team member who didn't install). Instead: "I see you've cloned a project with Momentum configured. I need to set up a few global tools on your machine..." — abbreviated consent.

[Source: epics.md Story 1.3 AC6; FR5 in epics.md Requirements Inventory]

### Task 7: [S] Decline Path

When developer chooses [S]:
- Explain: "Setup is needed for enforcement hooks and rules. You can invoke `/momentum` again any time to complete it."
- Proceed to session orientation — Impetus still works, but Tier 1 enforcement (hooks) won't be active
- Do NOT write any files
- Do NOT write `installed.json` (so next invocation offers setup again)

[Source: ux-design-specification.md#Journey 0; epics.md Story 1.3 AC1 decline path]

### Impetus Voice Register

From architecture.md and UX spec:
- **Guide's voice**: oriented, substantive, forward-moving
- Synthesizes before delivering; returns agency at completion ("That's done — here's what was produced. What's next?")
- Acknowledges uncertainty honestly
- Never: generic praise ("Great!"), numeric progress ("Step 3/8"), visible machinery
- Symbol vocabulary: ✓ completed, → current, ◦ upcoming, ! warning, ✗ failed

[Source: architecture.md#Communication Patterns; ux-design-specification.md UX-DR18]

### Post-Confirmation Display Format (UX Component 9)

```
  Setting up Momentum 1.0.0...

  ✓  ~/.claude/rules/authority-hierarchy.md
  ✓  ~/.claude/rules/anti-patterns.md
  ✓  ~/.claude/rules/model-routing.md
  ✓  .claude/settings.json — enforcement hooks configured
  ✓  .mcp.json — Git MCP + Findings MCP configured

  !  Restart Claude Code when ready — hooks activate on restart.
     Rules and MCP are working now.

  What are you working on?
```

[Source: ux-design-specification.md#Journey 0 (after [Y]); ux-design-specification.md#Component 9 Install/Upgrade Status]

### Project Structure Notes

Files written BY this story's implementation:
```
skills/momentum/
├── workflow.md             ← NEW: the Impetus workflow
└── references/
    └── practice-overview.md ← NEW: loaded by Impetus for orientation

.claude/momentum/
└── installed.json          ← WRITTEN at test-install time (tracked in git)
```

Files READ by the workflow (created in Story 1.1):
```
skills/momentum/references/
├── momentum-versions.json  ← action manifest
├── hooks-config.json       ← hook template (merged into settings.json)
├── mcp-config.json         ← MCP template (merged into .mcp.json)
└── rules/                  ← rule files written to ~/.claude/rules/
    ├── authority-hierarchy.md
    ├── anti-patterns.md
    └── model-routing.md
```

**Note:** Story 1.1 creates placeholder/stub rule files. If those stubs don't contain real content yet, the test install will write empty or stub rules. That's acceptable for Story 1.3 — the real rule content is Epic 3 scope (Stories 3.4, 3.5). The mechanism is what matters here.

### References

- [Source: epics.md#Story 1.3 — All Acceptance Criteria]
- [Source: epics.md#Epic 1 Additional Requirements — showTurnDuration]
- [Source: architecture.md#Decision 5a — Rules Deployment via Impetus]
- [Source: architecture.md#Decision 5c — Installation & Upgrade Manifest (full schema)]
- [Source: ux-design-specification.md#Journey 0: First-Time Install]
- [Source: ux-design-specification.md#The /momentum Entry Point (routing table)]
- [Source: ux-design-specification.md#Component 9 Install/Upgrade Status]
- [Source: architecture.md#Communication Patterns — Impetus voice, symbol vocabulary]

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → skill-instruction (EDD) — `skills/momentum/workflow.md`
- Task 2 → skill-instruction (EDD) — `skills/momentum/references/practice-overview.md`
- Task 3 → config-structure (direct) — `installed.json` test install + git tracking verification

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the workflow:**
1. Write 3 behavioral evals in `skills/momentum/evals/`:
   - `eval-first-install-consent-and-execution.md` — Given no installed.json, skill should show pre-consent summary, wait for approval, execute actions, write installed.json, confirm each action
   - `eval-version-match-skip.md` — Given installed.json with version matching current_version, skill should skip setup and proceed to session orientation without prompting
   - `eval-decline-path.md` — Given no installed.json and developer declines [S], skill should NOT write any files, explain degraded state, proceed to orientation

**Then implement:** write workflow.md

**Then verify:** spawn a subagent per eval, pass the SKILL.md + workflow.md as context, observe behavior against expected outcome. Max 3 fix cycles per eval.

**NFR compliance — mandatory:**
- SKILL.md `description` ≤150 characters (NFR1) — already set in Story 1.1 stub; verify it still holds
- `model: claude-opus-4-6` and `effort: normal` present (Impetus = orchestrating agent, flagship model)
- workflow.md body ≤500 lines — this is a complex skill; use `references/` for lengthy content (step guides, schemas)
- Skill name `momentum` (bare, entry-point exception)

**Additional DoD items:**
- [ ] 3 behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all 3 eval behaviors confirmed (or failures documented)
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model: claude-opus-4-6` and `effort: normal` present
- [ ] workflow.md body ≤500 lines (overflow to references/ if needed)
- [ ] AVFL checkpoint documented (momentum-dev runs automatically)

---

### config-structure Tasks: Direct Implementation

For Task 3 (installed.json test install + git tracking):

1. **Run test install** — invoke the implemented Impetus skill in this repo itself (dogfooding) to confirm `installed.json` is written correctly
2. **Verify by inspection:**
   - `installed.json` parses as valid JSON: `cat .claude/momentum/installed.json | python3 -m json.tool`
   - Required fields: `momentum_version`, `installed_at`, `components` with at least `rules-global`, `hooks`, `mcp` keys
   - `installed_at` is ISO 8601 format
   - `components.rules-global.hash` is a non-empty string (git blob SHA)
3. **Verify git tracking:**
   - `cat .gitignore | grep installed.json` — should return nothing
   - `git status .claude/momentum/installed.json` — should show as tracked (new file or modified, not ignored)
4. **Document** in Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] `installed.json` parses without error (validated with a tool)
- [ ] All required fields present with correct types
- [ ] `installed.json` not in `.gitignore`
- [ ] Changes documented in Dev Agent Record

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

### File List
