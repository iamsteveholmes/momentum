# Story 3.1: PostToolUse Lint and Format Hook Active

Status: ready-for-dev

## Story

As a developer,
I want code to be automatically linted and formatted every time I edit a file,
so that formatting violations never accumulate and I never have to run a separate format step.

## Acceptance Criteria

**AC1 — Hook fires on every code file edit:**
Given Momentum hooks are installed in `.claude/settings.json` (via Story 1.3),
When a developer edits any code file using a Claude Code tool (Write, Edit, or NotebookEdit),
Then the PostToolUse hook fires automatically,
And it runs the project's configured lint/format command (e.g. `prettier --write`, `eslint --fix`, `black`),
And the hook executes within the same tool response cycle — before the developer sees the final result.

**AC2 — Clean output (no issues):**
Given the PostToolUse hook runs and finds no issues,
When the hook completes (UX-DR3),
Then it outputs exactly one line: `[lint] ✓ checked [file path] — clean`,
And no additional output appears.

**AC3 — Auto-fix output:**
Given the PostToolUse hook runs and finds auto-fixable issues,
When the hook auto-fixes them (UX-DR3),
Then it outputs exactly one line: `[lint] ✓ auto-fixed [N issue(s)] in [file path]`.

**AC4 — Non-fixable issues output:**
Given the PostToolUse hook runs and finds issues that cannot be auto-fixed,
When the hook completes (UX-DR3),
Then it outputs: `[lint] ✗ [N issues] — [file:line of first] — [likely cause]`,
And the output is specific enough for the developer to act without opening a separate tool.

**AC5 — No lint tool configured:**
Given the project has no lint/format tool configured,
When the PostToolUse hook fires,
Then it outputs: `[lint] ◦ skipped — no lint tool configured`,
And exits successfully — no false failure.

**AC6 — Re-entrancy suppression:**
Given the PostToolUse hook auto-fixes a file,
When the auto-fixed write completes,
Then the PostToolUse hook does not re-fire for the lint-initiated write — hook re-entrancy is suppressed (e.g. via environment variable guard or lint tool's own exit-on-fix flag).
**Note:** The exact mechanism must be verified against Claude Code's hook invocation model. If hooks run in separate processes, an env var guard will not survive process boundaries — a filesystem lockfile (e.g. `.claude/momentum/.lint-running`) or relying on the lint tool's idempotency would be required instead. Confirm the invocation model before choosing the implementation approach.

**AC7 — Session state file written:**
Given the PostToolUse hook fires after a Write or Edit tool use,
When it completes (whether lint ran or was skipped),
Then it appends the modified file path to `.claude/momentum/session-modified-files.txt`,
And duplicate paths are acceptable — the Stop hook (Story 3.3) reads this file to determine whether any code was modified during the session.
**Note:** The Stop hook deletes this file after reading. The PostToolUse hook (Story 3.1) writes; the Stop hook (Story 3.3) reads and deletes.

## Tasks / Subtasks

- [ ] Task 1: Create the PostToolUse lint/format hook script (AC: 1, 2, 3, 4, 5, 6, 7)
  - [ ] 1.1: Create `skills/momentum/references/hooks/lint-format.sh` — bash script implementing the lint/format hook logic
  - [ ] 1.2: Implement re-entrancy guard: check `$MOMENTUM_LINT_RUNNING` at entry; export and set to 1 before invoking lint tool; unset on exit
  - [ ] 1.3: Implement lint tool detection: check `package.json` for `prettier`/`eslint` scripts, check for `.prettierrc`/`.eslintrc`/`pyproject.toml`/`setup.cfg`; if none found output `[lint] ◦ skipped — no lint tool configured` and exit 0
  - [ ] 1.4: Implement output format per AC2/AC3/AC4: capture lint tool exit code and output; produce exactly one line per spec
  - [ ] 1.5: Implement session state append: after lint runs (or is skipped), append `$MODIFIED_FILE` to `.claude/momentum/session-modified-files.txt`; create parent dirs if absent
  - [ ] 1.6: Make script executable: `chmod +x skills/momentum/references/hooks/lint-format.sh`

- [ ] Task 2: Register hook in hooks-config.json (AC: 1)
  - [ ] 2.1: Read `skills/momentum/references/hooks-config.json` (or create if absent)
  - [ ] 2.2: Add PostToolUse hook entry targeting `lint-format.sh` for `Write`, `Edit`, and `NotebookEdit` tool events (matching the existing template scope); hook receives the file path via environment variable — verify the correct env var name by checking existing hooks in `.claude/settings.json`
  - [ ] 2.3: Confirm hook matcher is `"Edit|Write|NotebookEdit"` to match the existing hooks-config.json template scope

- [ ] Task 2b: Define hook script deployment path (AC: 1) — CRITICAL
  - [ ] 2b.1: The hook script is authored at `skills/momentum/references/hooks/lint-format.sh` (bundled with the momentum skill) but must be executed from the project's `.claude/momentum/hooks/lint-format.sh` path at runtime (where Impetus deploys it)
  - [ ] 2b.2: Add an `add` action entry to `skills/momentum/references/momentum-versions.json` under the current version's `actions` array so Impetus copies `lint-format.sh` on install/upgrade. Use the same schema as the existing rules entries:
    ```json
    {
      "action": "add",
      "group": "hooks",
      "scope": "project",
      "source": "references/hooks/lint-format.sh",
      "target": ".claude/momentum/hooks/lint-format.sh"
    }
    ```
    Note: `source` is relative to the skill's directory (`${CLAUDE_SKILL_DIR}`); `target` is relative to the project root.
  - [ ] 2b.3: Add an AC-level verification step: confirm `.claude/momentum/hooks/lint-format.sh` exists and is executable after Impetus install — without this, the hook command silently fails at runtime

- [ ] Task 3: Verify hook integration (AC: all)
  - [ ] 3.1: Confirm `.claude/settings.json` in the project has the PostToolUse hook registered (Impetus writes this from hooks-config.json; this story adds the hook to the template so the next install/upgrade picks it up)
  - [ ] 3.2: Verify `.claude/momentum/` directory creation path is handled gracefully (mkdir -p)
  - [ ] 3.3: Manual smoke test: edit a file with a known lint violation, confirm correct output line appears

**FRs Covered:** FR18 (auto-lint and auto-format on every file edit)
**Cross-story contract:** Session state file `.claude/momentum/session-modified-files.txt` — Story 3.1 (PostToolUse) writes; Story 3.3 (Stop gate) reads and deletes.

## Dev Notes

### Hook Architecture (CRITICAL — read before implementing)

**Deployment path:** This is an always-on hook. Always-on hooks are:
1. Defined as a template in `skills/momentum/references/hooks-config.json`
2. Written to `.claude/settings.json` by Impetus on first `/momentum` invocation
3. Never deployed by `npx skills add` — that's SKILL.md files only

The hook script lives in `skills/momentum/references/hooks/lint-format.sh`. Impetus writes it to the project `.claude/` directory on install. [Source: `_bmad-output/planning-artifacts/architecture.md` — Hook Infrastructure section]

**Hook registration format** (`.claude/settings.json` PostToolUse entry):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PROJECT_DIR}/.claude/momentum/hooks/lint-format.sh \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```
**IMPORTANT — two unresolved items before implementation:**
1. **Env var for file path:** `$CLAUDE_TOOL_INPUT_FILE_PATH` is provisional. Verify the exact env var name by checking existing hooks in `.claude/settings.json` — it may be a different name in practice. [Source: `_bmad-output/planning-artifacts/architecture.md` — lines 518, 619]
2. **Deploy path:** The hook command points to `.claude/momentum/hooks/lint-format.sh` (the deployed path), but the script is authored at `skills/momentum/references/hooks/lint-format.sh`. Task 2b covers the deployment mechanism. Do not write the hook command until the deploy path is confirmed. [Source: `_bmad-output/planning-artifacts/architecture.md` — Hook Infrastructure section]

**Two deployment paths for hooks:**
- **Always-on (this story):** `skills/momentum/references/hooks-config.json` template → Impetus writes to `.claude/settings.json`
- **Skill-lifecycle:** defined in SKILL.md `hooks:` frontmatter — not used here

### Re-entrancy Suppression Pattern

**OPEN TECHNICAL QUESTION — resolve before implementing Task 1.2:**

Does Claude Code invoke PostToolUse hook commands as separate processes (one per hook fire), or within a shared process context?

- **If separate processes:** Environment variable guards (`export MOMENTUM_LINT_RUNNING=1`) will NOT work — env vars do not survive separate subprocess invocations. Use a **filesystem lockfile** instead:
  ```bash
  LOCKFILE="${CLAUDE_PROJECT_DIR}/.claude/momentum/.lint-running"
  if [ -f "$LOCKFILE" ]; then exit 0; fi
  touch "$LOCKFILE"
  trap "rm -f '$LOCKFILE'" EXIT
  ```
- **If shared process context OR Claude Code deduplicates writes in the same cycle:** An env var guard works, OR rely on the lint tool's idempotency (most lint tools exit 0 with no output if the file has no issues after auto-fix).

**Recommended:** Use the filesystem lockfile approach regardless — it is process-boundary-safe and adds minimal overhead. Clean up the lockfile with `trap ... EXIT` to handle unexpected exits.

Env var approach (only if shared-process confirmed):
```bash
#!/bin/bash
if [ "${MOMENTUM_LINT_RUNNING}" = "1" ]; then
  exit 0
fi
export MOMENTUM_LINT_RUNNING=1
```

### Session State Contract (CRITICAL — cross-story dependency)

`.claude/momentum/session-modified-files.txt` is the **inter-hook state contract** between this story (3.1) and the Stop gate (Story 3.3):
- **Story 3.1 (PostToolUse hook) WRITES:** appends file path per edit
- **Story 3.3 (Stop hook) READS:** checks if any file was modified this session; DELETES after reading

This file is how Story 3.3 detects code modifications without running `git diff`. Do not change this contract without also updating Story 3.3. [Source: `_bmad-output/planning-artifacts/epics.md` — Story 3.1 Note, line 1023]

### Output Format Spec (one line, always)

Per architecture UX-DR3 and hook announcement format:
- `[lint] ✓ checked [file path] — clean`
- `[lint] ✓ auto-fixed [N issue(s)] in [file path]`
- `[lint] ✗ [N issues] — [file:line of first] — [likely cause]`
- `[lint] ◦ skipped — no lint tool configured`

**Never output more than one line.** Silent hooks build no trust; verbose hooks create noise. [Source: `_bmad-output/planning-artifacts/architecture.md` — Hook announcement output section, line 710]

### Lint Tool Detection Heuristics

Check in order:
1. `package.json` `scripts.lint` or `scripts.format` key → use that command
2. `.prettierrc` / `.prettierrc.json` / `prettier.config.js` → `prettier --write "$FILE"`
3. `.eslintrc` / `.eslintrc.json` / `eslint.config.js` → `eslint --fix "$FILE"`
4. `pyproject.toml` with `[tool.ruff]` or `[tool.black]` → `ruff format "$FILE"` or `black "$FILE"`
5. `setup.cfg` with `[flake8]` → `flake8 "$FILE"` (linting only, no auto-fix)
6. None found → output skip message, exit 0

The hook is a **per-project auto-detection wrapper** — it doesn't hardcode a tool. Each project brings its own lint/format toolchain; this hook discovers and runs it.

### Project Structure

Files to create/modify:
- `skills/momentum/references/hooks/lint-format.sh` — the hook script (NEW)
- `skills/momentum/references/hooks-config.json` — add PostToolUse entry (CREATE or MODIFY)

Files the hook will interact with at runtime:
- `.claude/settings.json` — where the hook is registered (not modified by this story; modified by Impetus on install)
- `.claude/momentum/session-modified-files.txt` — written at runtime by the hook (created if absent)

### Testing Standards

This is a `rule-hook` change type — functional verification is the testing approach:
1. Register hook in `.claude/settings.json` locally for testing
2. Edit a file with a known lint violation; verify output is exactly one line matching the spec
3. Edit a clean file; verify `[lint] ✓ checked ... — clean`
4. Edit a file when no lint tool is configured; verify `[lint] ◦ skipped...` and exit 0
5. Trigger two consecutive edits; verify hook doesn't re-fire infinitely (re-entrancy guard works)
6. Check `.claude/momentum/session-modified-files.txt` is populated after each edit

### Dependencies

- **Depends on:** Story 1.3 (Momentum hooks installed in `.claude/settings.json`) — hook deployment mechanism must be in place
- **Depended on by:** Story 3.3 (Stop gate) reads `session-modified-files.txt` written by this hook

### Previous Story Patterns

Epic 2 stories established the `skills/momentum/references/` pattern for reference files loaded by Impetus. This story follows the same pattern — new files go in `skills/momentum/references/hooks/`. [Source: git log — recent Epic 2 work]

### Project Structure Notes

- Hook script: `skills/momentum/references/hooks/lint-format.sh` (new subdirectory `hooks/`)
- Config template: `skills/momentum/references/hooks-config.json` (may already exist from Story 1.3 — read it first before creating)
- Naming consistent with architecture naming patterns: kebab-case, no vendor prefix in hook script name [Source: `_bmad-output/planning-artifacts/architecture.md` — Naming Patterns section]

### References

- Epic 3 Story 3.1 spec: `_bmad-output/planning-artifacts/epics.md#Story-3.1`
- Hook Infrastructure: `_bmad-output/planning-artifacts/architecture.md#Hook-Infrastructure`
- Hook announcement format: `_bmad-output/planning-artifacts/architecture.md` line 710
- Session state contract: `_bmad-output/planning-artifacts/epics.md` line 1023 (Story 3.1 Note)
- Always-on hook deployment: `_bmad-output/planning-artifacts/architecture.md` line 158
- FR18 (auto-lint on edit): `_bmad-output/planning-artifacts/epics.md` line 90

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 (`lint-format.sh`) → `script-code` (TDD)
- Task 2 (`hooks-config.json`) → `config-structure` (direct + inspect)
- Task 3 (verification) → `rule-hook` (functional verification)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** The hook script (`lint-format.sh`) is a bash script. Use bats (Bash Automated Testing System) or a simple test script in `skills/momentum/references/hooks/tests/` if a test harness is appropriate. Alternatively, use functional integration testing per the rule-hook approach below — bash scripts for hooks are often better verified functionally than unit-tested.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies):**
- Tests written and passing (or functional verification documented if unit tests don't apply)
- No regressions in existing hook scripts
- Script is executable (`chmod +x`)

---

### rule-hook Tasks: Functional Verification

Hook configuration and the hook script itself (as a deployed hook) are verified functionally:

1. **Write the hook entry** in `hooks-config.json` per the established PostToolUse format
2. **State the expected behavior:** "Given a Write/Edit tool use fires, the lint-format hook should execute lint detection, run the tool if found, output exactly one line, and append the file path to session-modified-files.txt"
3. **Verify functionally:**
   - Register the hook in local `.claude/settings.json`
   - Edit a file with a known lint violation; confirm output is exactly one line matching the spec
   - Edit a clean file; confirm `[lint] ✓ checked ... — clean`
   - Edit a file with no lint tool configured; confirm `[lint] ◦ skipped...` and exit 0
   - Trigger two consecutive edits; confirm no infinite loop (re-entrancy guard works)
   - Confirm `.claude/momentum/session-modified-files.txt` is populated after edit
4. **Document** verification result in Dev Agent Record

**Format requirements:**
- Hook entry must follow the Agent Skills hooks schema in `.claude/settings.json`
- No duplicate PostToolUse hook entries — merge, don't append

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as testable condition (in Dev Agent Record)
- [ ] Functional verification performed and result documented
- [ ] Format matches established patterns (one-line output, exact format per spec)

---

### config-structure Tasks: Direct Implementation

`hooks-config.json` changes need no tests. Implement directly and verify by inspection:

1. **Write the JSON entry** for the PostToolUse hook into `skills/momentum/references/hooks-config.json`
2. **Verify by inspection:**
   - JSON must parse without error (`jq . hooks-config.json` or equivalent)
   - PostToolUse matcher covers Write and Edit tool events only
   - Command path resolves correctly relative to the project root
3. **Document** the hook entry structure in Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] `hooks-config.json` parses without error (validated with `jq`)
- [ ] PostToolUse hook entry present with correct matcher and command
- [ ] All referenced paths in the hook command resolve at runtime
- [ ] Changes documented in Dev Agent Record

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List
