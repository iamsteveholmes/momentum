# Story 3.2: PreToolUse File Protection Hooks Active

Status: ready-for-dev

**FRs Covered:** FR19, FR21 (PreToolUse file protection)
**Cross-story contract:** This hook shares the PreToolUse slot in `hooks-config.json` with the placeholder written during Story 1.3. This story defines the `protected_paths` extension point in `project-config.json` — Story 7.1 will populate it, but the schema originates here. The hook reads the file if it exists; Story 7.1 creates it.

## Story

As a developer,
I want Momentum to block writes to acceptance tests and protected configuration files,
so that test integrity and critical config are preserved automatically — no accidental overwrites.

## Acceptance Criteria

**AC1 — Blocks writes to default protected paths (UX-DR3):**
Given Momentum hooks are installed,
When a Claude Code tool attempts to write to any path matching `tests/acceptance/`, `**/*.feature`, `.claude/rules/`, or `_bmad-output/planning-artifacts/*.md`,
Then the PreToolUse hook fires and blocks the write before it executes,
And returns an explanation of what was blocked and why.
**Note:** `.claude/rules/` here is the project-scoped path. Global `~/.claude/rules/` is outside project PreToolUse scope — protected by the authority hierarchy rule instead (Decision 2a). Impetus's own writes to `.claude/rules/` during install/upgrade are permitted — the hook includes an allowlist for the Momentum install workflow.

**AC2 — Block output format:**
Given a PreToolUse hook blocks a write (UX-DR3),
When the hook fires,
Then it outputs: `[file-protection] ✗ blocked write to [path] — [policy]: [reason]`,
And the policy name and reason are specific (e.g. "acceptance-test-dir: no modification after ATDD phase begins", "planning-artifacts: spec files are read-only during implementation").
**Note:** Pass output is suppressed for allowed writes — UX-DR3's "never silent" principle applies when the hook has something meaningful to report (a block). Routine pass-through on non-protected paths is silent.

**AC3 — Project-specific protected paths:**
Given a project defines additional protected paths in `.claude/momentum/project-config.json` under a `protected_paths` array,
When the PreToolUse hook evaluates a write,
Then it enforces the project-specific paths in addition to Momentum defaults,
And project overrides are additive — they cannot remove Momentum default protected paths.
**Note:** Custom protected paths use `project-config.json` (created in Story 7.1), not `installed.json` (which tracks version/component state only per Decision 5c). If `project-config.json` does not exist, the hook proceeds with Momentum defaults only. The `protected_paths` field schema is defined by this story (3.2) — Story 7.1 will add project-level configuration tooling but does not independently define this schema; Story 3.2 owns the extension point.

## Tasks / Subtasks

- [ ] Task 1: Create the PreToolUse file protection hook script (AC: 1, 2, 3)
  - [ ] 1.1: Create `skills/momentum/references/hooks/file-protection.sh` — bash script implementing the file protection logic
  - [ ] 1.2: Implement Momentum default protected paths check:
    - `tests/acceptance/` — policy: `acceptance-test-dir`
    - `**/*.feature` — policy: `acceptance-test-dir`
    - `.claude/rules/` — policy: `project-rules`
    - `_bmad-output/planning-artifacts/*.md` — policy: `planning-artifacts`
  - [ ] 1.3: Implement Momentum install allowlist: if the write is initiated by the Momentum install/upgrade workflow, permit the write and exit 0 silently. **Open decision at implementation time:** verify whether Impetus sets `MOMENTUM_INSTALLING=1` in its install/upgrade workflow. If yes, use env var check. If env vars don't survive process boundaries, use filesystem sentinel (`.claude/momentum/.impetus-installing`). See "Momentum Install Allowlist" in Dev Notes.
  - [ ] 1.4: Implement project-config.json reader: if `.claude/momentum/project-config.json` exists and contains `protected_paths` array, append those paths to the protected list — never remove Momentum defaults
  - [ ] 1.5: On block: output `[file-protection] ✗ blocked write to [path] — [policy]: [reason]` and exit with non-zero code to prevent the write
  - [ ] 1.6: On allow: exit 0 silently (no output)
  - [ ] 1.7: Make script executable: `chmod +x skills/momentum/references/hooks/file-protection.sh`

- [ ] Task 2: Replace PreToolUse placeholder in hooks-config.json (AC: 1)
  - [ ] 2.1: Read `skills/momentum/references/hooks-config.json` — existing PreToolUse entry is a placeholder pointing to an `echo` command
  - [ ] 2.2: Replace the PreToolUse placeholder command with the actual `file-protection.sh` command
  - [ ] 2.3: Preserve the `"Edit|Write|NotebookEdit"` matcher from the existing placeholder — this is the correct scope
  - [ ] 2.4: Validate hooks-config.json parses without error after edit (`jq . hooks-config.json`)

- [ ] Task 2b: Define hook script deployment path (AC: 1) — CRITICAL
  - [ ] 2b.1: The hook script is authored at `skills/momentum/references/hooks/file-protection.sh` (bundled with the momentum skill) but must execute from `.claude/momentum/hooks/file-protection.sh` at runtime
  - [ ] 2b.2: Add an `add` action entry to `skills/momentum/references/momentum-versions.json` under the current version's `actions` array so Impetus copies `file-protection.sh` on install/upgrade. Use the same schema as the existing rules entries:
    ```json
    {
      "action": "add",
      "group": "hooks",
      "scope": "project",
      "source": "references/hooks/file-protection.sh",
      "target": ".claude/momentum/hooks/file-protection.sh"
    }
    ```
    Note: `source` is relative to the skill's directory (`${CLAUDE_SKILL_DIR}`); `target` is relative to the project root.
  - [ ] 2b.3: Verify `.claude/momentum/hooks/file-protection.sh` exists and is executable after install before considering this story done

- [ ] Task 3: Verify hook integration (AC: all)
  - [ ] 3.1: Attempt to write to `tests/acceptance/test.feature`; confirm hook blocks with correct output format
  - [ ] 3.2: Attempt to write to `.claude/rules/some-rule.md`; confirm block
  - [ ] 3.3: Attempt to write to `_bmad-output/planning-artifacts/prd.md`; confirm block
  - [ ] 3.4: Write to a non-protected path (e.g. `src/index.js`); confirm silent pass-through (no output)
  - [ ] 3.5: If `project-config.json` exists with `protected_paths`, confirm custom path is also blocked
  - [ ] 3.6: Simulate Momentum install workflow allowlist: confirm Impetus writes to `.claude/rules/` are not blocked
  - [ ] 3.7: Verify path matching works for both absolute paths (e.g. `/Users/user/project/tests/acceptance/foo.feature`) and relative paths (e.g. `tests/acceptance/foo.feature`) — hook may receive either form depending on how Claude Code invokes it; confirm which form is received and that matching handles it correctly

## Dev Notes

### Hook Architecture (CRITICAL — read before implementing)

**Hook type:** PreToolUse (always-on). Fires BEFORE a tool executes, allowing the hook to block the tool entirely by exiting non-zero.

**Deployment path:** Same as Story 3.1 — always-on hooks are:
1. Defined as a template in `skills/momentum/references/hooks-config.json`
2. Written to `.claude/settings.json` by Impetus on first `/momentum` invocation
3. Script authored at `skills/momentum/references/hooks/file-protection.sh`, deployed to `.claude/momentum/hooks/file-protection.sh` by Impetus

**Existing hooks-config.json PreToolUse entry (placeholder to replace):**
```json
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
```
Replace the `echo` command with the actual `file-protection.sh` invocation. Preserve the `"Edit|Write|NotebookEdit"` matcher. [Source: `skills/momentum/references/hooks-config.json`]

**Hook command format (after replacement):**
```json
{
  "matcher": "Edit|Write|NotebookEdit",
  "hooks": [
    {
      "type": "command",
      "command": "bash ${CLAUDE_PROJECT_DIR}/.claude/momentum/hooks/file-protection.sh \"$CLAUDE_TOOL_INPUT_FILE_PATH\"",
      "timeout": 5
    }
  ]
}
```
**Note:** Verify the exact env var for the target file path (`$CLAUDE_TOOL_INPUT_FILE_PATH` is provisional — check existing hooks in `.claude/settings.json` for the confirmed name at implementation time).

### How PreToolUse Blocking Works

A PreToolUse hook blocks the tool by exiting with a non-zero exit code. The tool does not execute. The output from the hook (stdout or stderr) is shown to Claude Code as the reason for the block.

```bash
# Block pattern
echo "[file-protection] ✗ blocked write to ${FILE_PATH} — ${POLICY}: ${REASON}"
exit 1  # Non-zero = block the tool
```

```bash
# Allow pattern (silent)
exit 0  # Zero = allow tool to proceed; no output
```

This is distinct from PostToolUse (Story 3.1) which cannot prevent the tool — it only runs after.

### Default Protected Paths and Policy Names

| Path Pattern | Policy Name | Reason |
|---|---|---|
| `tests/acceptance/` (any path under) | `acceptance-test-dir` | No modification after ATDD phase begins |
| `**/*.feature` | `acceptance-test-dir` | Gherkin feature files are acceptance test artifacts |
| `.claude/rules/` (any path under) | `project-rules` | Project rules are read-only during implementation |
| `_bmad-output/planning-artifacts/*.md` | `planning-artifacts` | Spec files are read-only during implementation |

**Pattern matching note:** Bash glob patterns and shell path matching are needed. For `**/*.feature`, use a recursive check across the full file path. For `_bmad-output/planning-artifacts/*.md`, match only direct children (one level), not subdirectories.

### Momentum Install Allowlist (CRITICAL)

Impetus writes to `.claude/rules/` during install and upgrade. The hook MUST NOT block these writes. Implementation options:

**Option A — Env var allowlist (preferred if reliable across process boundaries):**
Impetus sets `MOMENTUM_INSTALLING=1` before calling its write operations. The hook checks:
```bash
if [ "${MOMENTUM_INSTALLING}" = "1" ]; then
  exit 0  # Allow — Impetus install in progress
fi
```

**Option B — Caller path check:**
The hook checks if the write comes from a known Impetus workflow path (less reliable — depends on caller context).

**Option C — Explicit allowlist:**
Maintain a hardcoded list of paths Impetus is allowed to write to (brittle — requires updates when Impetus writes new paths).

**Recommended:** Option A, but verify that `MOMENTUM_INSTALLING=1` is already set by Impetus's install/upgrade workflow (or add it if not). If env vars don't survive process boundaries (see Story 3.1 re-entrancy note), use a filesystem sentinel file (`.claude/momentum/.impetus-installing`) instead.

### Project-Config Integration

`.claude/momentum/project-config.json` schema (relevant section — **schema defined by this story**; file created by Story 7.1):
```json
{
  "protected_paths": [
    "src/vendor/**",
    "contracts/*.json"
  ]
}
```

**Schema ownership note:** The `protected_paths` field is defined here (Story 3.2) as the extension point for project-specific protection. Story 7.1 creates the `project-config.json` file and populates it, but does not independently specify `protected_paths`. This story's AC3 is the authoritative spec for the field.

The hook reads this file only if it exists — graceful degradation if Story 7.1 hasn't been implemented yet. Project paths are appended to the default list; Momentum defaults cannot be removed by project config. [Source: `_bmad-output/planning-artifacts/epics.md` — Story 3.2 AC3 Note]

### Output Format (one line, per UX-DR3)

Blocked write:
```
[file-protection] ✗ blocked write to tests/acceptance/login.feature — acceptance-test-dir: no modification after ATDD phase begins
```

Allowed write: **silent** (no output at all).

This differs from the PostToolUse lint hook (Story 3.1) which always outputs one line. PreToolUse file protection is silent on pass-through — blocking is the meaningful event; routine allows are noise. [Source: `_bmad-output/planning-artifacts/architecture.md` — line 718 Hook announcement format note; `_bmad-output/planning-artifacts/epics.md` — Story 3.2 AC2 Note]

### Path Matching Implementation Notes

The hook receives the target file path as `$1` (or via env var — verify at implementation time). **Verify whether Claude Code passes absolute or relative paths** — this determines the matching strategy. Key matching considerations:

- **`tests/acceptance/`**: Match if the path contains `/tests/acceptance/` (handles both absolute and relative)
- **`**/*.feature`**: Any path ending in `.feature` anywhere in the tree — `[[ "$FILE_PATH" == *.feature ]]`
- **`.claude/rules/`**: Match if the path contains `/.claude/rules/` or starts with `.claude/rules/` (project-scoped only)
- **`_bmad-output/planning-artifacts/*.md`**: Direct children of `_bmad-output/planning-artifacts/` that end in `.md` (not subdirectory files) — use a pattern that matches the directory without matching subdirectories

Use bash `[[ $FILE_PATH == *pattern* ]]` for glob-style matching, or `case` statements for multiple patterns. Task 3.7 confirms the path form received at runtime.

### Project Structure

Files to create/modify:
- `skills/momentum/references/hooks/file-protection.sh` — the hook script (NEW; same directory as `lint-format.sh` from Story 3.1)
- `skills/momentum/references/hooks-config.json` — replace PreToolUse placeholder command (MODIFY)

Files the hook will interact with at runtime:
- `.claude/settings.json` — where the hook is registered (not modified by this story)
- `.claude/momentum/project-config.json` — read if exists (not created by this story; Story 7.1 creates it)

### Dependencies

- **Depends on:** Story 1.3 (Momentum hooks installed in `.claude/settings.json`) — hook deployment mechanism must be in place
- **Depends on (soft):** Story 3.1 completed for deploy path pattern established (`skills/momentum/references/hooks/`)
- **Depended on by:** Story 7.1 (`project-config.json` with `protected_paths` — this story already handles the case gracefully when 7.1 isn't done)

### Testing Standards

This is `rule-hook` + `script-code` change type — use functional verification:
1. Register hook in local `.claude/settings.json` for testing
2. Test each protected path pattern: confirm block with correct output format
3. Test a non-protected path: confirm silent pass (no output, tool proceeds)
4. Test Momentum install allowlist: confirm Impetus writes are not blocked
5. Test project-config.json custom paths: add a path and confirm it's enforced
6. Test project-config.json absent: confirm hook runs cleanly using only defaults

### Project Structure Notes

- Hook script follows naming pattern established in Story 3.1: `skills/momentum/references/hooks/[verb-noun].sh`
- `file-protection.sh` — kebab-case, descriptive, no vendor prefix (scripts don't use `momentum-` prefix) [Source: `_bmad-output/planning-artifacts/architecture.md` — Naming Patterns section]

### References

- Epic 3 Story 3.2 spec: `_bmad-output/planning-artifacts/epics.md#Story-3.2`
- Hook Infrastructure: `_bmad-output/planning-artifacts/architecture.md` — Hook Infrastructure section
- FR19 (PreToolUse acceptance test protection): `_bmad-output/planning-artifacts/epics.md` line 274
- FR21 (file protection via PreToolUse hook): `_bmad-output/planning-artifacts/epics.md` line 276
- Hook announcement format: `_bmad-output/planning-artifacts/architecture.md` line 710
- hooks-config.json placeholder: `skills/momentum/references/hooks-config.json`
- Story 3.1 (deploy path pattern): `_bmad-output/implementation-artifacts/3-1-posttooluse-lint-and-format-hook-active.md`

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 (`file-protection.sh`) → `script-code` (TDD / functional verification)
- Task 2 (`hooks-config.json` placeholder replacement) → `config-structure` (direct + inspect)
- Task 2b (deployment path) → `config-structure` (direct + inspect)
- Task 3 (verification) → `rule-hook` (functional verification)

---

### script-code Tasks: TDD / Functional Verification

The hook script is a bash file — use functional verification (unit tests for bash add test framework overhead not justified here):

1. **State the expected behavior per AC:** e.g., "Given write to `tests/acceptance/test.feature`, the hook exits 1 with output `[file-protection] ✗ blocked write to ...`"
2. **Implement the script** per acceptance criteria
3. **Verify functionally:**
   - Simulate hook invocation: `bash file-protection.sh "tests/acceptance/test.feature"` — confirm exit code 1 and correct output
   - Simulate allowed path: `bash file-protection.sh "src/index.js"` — confirm exit code 0 and no output
   - Simulate each protected path pattern separately
4. **Document** in Dev Agent Record

**DoD items for script-code tasks:**
- Functional verification performed for each AC scenario
- Script is executable (`chmod +x`)
- No regressions in Story 3.1 hook (`lint-format.sh`) — they coexist in the same `hooks/` directory

---

### config-structure Tasks: Direct Implementation

`hooks-config.json` placeholder replacement — implement directly and verify by inspection:

1. **Replace** the PreToolUse placeholder `echo` command with the `file-protection.sh` command
2. **Verify by inspection:**
   - `jq . skills/momentum/references/hooks-config.json` — must parse without error
   - PostToolUse entry (Story 3.1 placeholder) must remain untouched
   - Stop entry (Story 3.3 placeholder) must remain untouched
   - PreToolUse matcher must remain `"Edit|Write|NotebookEdit"`
3. **Document** the change in Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] `hooks-config.json` parses without error (validated with `jq`)
- [ ] All three hook entries present (PostToolUse, PreToolUse, Stop)
- [ ] Only the PreToolUse `command` field changed — matcher and other fields preserved
- [ ] Changes documented in Dev Agent Record

---

### rule-hook Tasks: Functional Verification

1. **Write the hook** per the established format
2. **State expected behavior:** "Given Claude Code attempts to write to a protected path, the PreToolUse hook blocks the write and outputs the block format; given a non-protected path, the hook exits silently"
3. **Verify functionally:** per the 6-step test plan in Testing Standards above
4. **Document** verification result in Dev Agent Record

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as testable condition (in Dev Agent Record)
- [ ] Functional verification performed for all 6 scenarios and result documented
- [ ] Format matches established patterns (output format exactly as specified)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List
