# Story 3.3: Stop Gate Runs Conditional Quality Checks

Status: ready-for-dev

**FRs Covered:** FR20 (conditional quality gates before session end)
**Cross-story contract:** `.claude/momentum/session-modified-files.txt` — Story 3.1 (PostToolUse hook) writes; this story (Stop hook) reads and deletes. This story's Stop hook also shares the Stop slot in `hooks-config.json` with the placeholder written during Story 1.3.

## Story

As a developer,
I want quality gates to run automatically before my session ends,
So that I never close a session with failing tests or unresolved lint errors.

## Acceptance Criteria

**AC1 — Conditional lint and test execution (FR20, UX-DR3):**
Given a developer ends a Claude Code session,
When the Stop hook fires,
Then lint runs unconditionally — regardless of whether code was modified this session,
And tests run only if at least one code file was modified during the session,
And the Stop hook determines whether code was modified by reading `.claude/momentum/session-modified-files.txt` (written by the PostToolUse hook per Story 3.1) — not by running git diff or any external check,
And if no code was modified (session state file absent or empty), tests are skipped and the session ends cleanly,
And the Stop hook deletes the session state file after reading it.
**Note:** Unconditional lint at session end catches files modified outside Claude Code (e.g. by the developer's editor or IDE) that the PostToolUse hook never saw. Per-edit lint (Story 3.1) catches in-session edits; Stop lint is the safety net for external changes. [Source: Epic 3 Story 3.3 AC1 Note]

**AC2 — Lint clean output (UX-DR3):**
Given the Stop hook runs lint and finds no issues,
When the hook completes,
Then it outputs: `[stop-gate] ✓ checked lint — clean`,
And the session proceeds to close.

**AC3 — Lint failure output (UX-DR3):**
Given the Stop hook runs and finds lint failures,
When the hook completes,
Then it outputs: `[stop-gate] ✗ lint: [N issues] — [file:line of first] — fix before closing`,
And the hook exits with a non-zero exit code to signal Claude Code that session termination should not proceed.

**AC4 — Tests pass output (UX-DR3):**
Given the Stop hook runs tests and they pass,
When the hook completes,
Then it outputs: `[stop-gate] ✓ checked tests — [N] passed`.

**AC5 — Tests fail output (UX-DR3):**
Given the Stop hook runs tests and they fail,
When the hook completes,
Then it outputs: `[stop-gate] ✗ tests: [N failed] — [failing test name] — [failure summary]`,
And the hook exits with a non-zero exit code to signal Claude Code that session termination should not proceed.

**AC6 — No test runner configured (UX-DR3):**
Given the Stop hook runs and the project has no test runner configured,
When the test step would run (code was modified),
Then it outputs: `[stop-gate] ◦ tests — no test runner configured`,
And lint still runs regardless.

**AC7 — No lint tool configured (UX-DR3):**
Given the Stop hook runs and the project has no lint tool configured,
When the lint step would run,
Then it outputs: `[stop-gate] ◦ lint — no lint tool configured`,
And tests still run if code was modified (per the session state file).

## Tasks / Subtasks

- [ ] Task 1: Create the Stop gate hook script (AC: 1, 2, 3, 4, 5, 6, 7)
  - [ ] 1.1: Create `skills/momentum/references/hooks/stop-gate.sh` — bash script implementing the stop gate logic. The `hooks/` subdirectory does not yet exist; create it first (`mkdir -p skills/momentum/references/hooks/`)
  - [ ] 1.2: Implement session state reading: check if `.claude/momentum/session-modified-files.txt` exists and is non-empty; if absent or empty, set `CODE_MODIFIED=false`; if present and non-empty, set `CODE_MODIFIED=true`
  - [ ] 1.3: Delete the session state file after reading (regardless of whether it was empty or present)
  - [ ] 1.4: Implement lint tool detection (same heuristics as Story 3.1's `lint-format.sh`):
    - `package.json` `scripts.lint` or `scripts.format` → use that command (full-project invocation, not per-file)
    - `.prettierrc` / `.prettierrc.json` / `prettier.config.js` → `prettier --check .`
    - `.eslintrc` / `.eslintrc.json` / `eslint.config.js` → `eslint .`
    - `pyproject.toml` with `[tool.ruff]` or `[tool.black]` → `ruff check .` or `black --check .`
    - `setup.cfg` with `[flake8]` → `flake8 .`
    - None found → output `[stop-gate] ◦ lint — no lint tool configured` and skip lint
  - [ ] 1.5: Run lint (if tool found); capture exit code and issue count; output AC2 or AC3 format
  - [ ] 1.6: Implement test runner detection (only if `CODE_MODIFIED=true`):
    - `package.json` `scripts.test` → use that command
    - `jest.config.js` / `jest.config.ts` → `npx jest`
    - `vitest.config.js` / `vitest.config.ts` → `npx vitest run`
    - `pytest.ini` / `pyproject.toml` with `[tool.pytest]` → `pytest`
    - None found → output `[stop-gate] ◦ tests — no test runner configured` and skip tests
  - [ ] 1.7: Run tests if runner found and `CODE_MODIFIED=true`; capture exit code, pass/fail counts; output AC4 or AC5 format
  - [ ] 1.8: Exit with non-zero if lint or tests failed (so Claude Code blocks session close); exit 0 if all passed or only skipped
  - [ ] 1.9: Make script executable: `chmod +x skills/momentum/references/hooks/stop-gate.sh`

- [ ] Task 2: Replace Stop placeholder in hooks-config.json (AC: 1)
  - [ ] 2.1: Read `skills/momentum/references/hooks-config.json` — existing Stop entry is a placeholder pointing to an `echo` command
  - [ ] 2.2: Replace the Stop placeholder command with the actual `stop-gate.sh` command
  - [ ] 2.3: Stop hooks have no matcher — preserve the existing structure (no `"matcher"` field in Stop entry)
  - [ ] 2.4: Set timeout to 60 seconds (tests can take longer than the 5s PreToolUse timeout)
  - [ ] 2.5: Validate hooks-config.json parses without error after edit (`jq . hooks-config.json`)

- [ ] Task 2b: Define hook script deployment path (AC: 1) — CRITICAL
  - [ ] 2b.1: The hook script is authored at `skills/momentum/references/hooks/stop-gate.sh` (bundled with the momentum skill) but must execute from `.claude/momentum/hooks/stop-gate.sh` at runtime
  - [ ] 2b.2: Add an `add` action entry to `skills/momentum/references/momentum-versions.json` under the current version's `actions` array so Impetus copies `stop-gate.sh` on install/upgrade. Use the same schema as the existing rules entries (source + target fields):
    ```json
    {
      "action": "add",
      "group": "hooks",
      "scope": "project",
      "source": "references/hooks/stop-gate.sh",
      "target": ".claude/momentum/hooks/stop-gate.sh"
    }
    ```
    Note: `source` is relative to the skill's directory (`${CLAUDE_SKILL_DIR}`); `target` is relative to the project root.
  - [ ] 2b.3: Verify `.claude/momentum/hooks/stop-gate.sh` exists and is executable after install before considering this story done

- [ ] Task 3: Verify hook integration (AC: all)
  - [ ] 3.1: Simulate a session with code modified: create `.claude/momentum/session-modified-files.txt` with a path; run `bash stop-gate.sh`; confirm lint and tests both run (or skip correctly)
  - [ ] 3.2: Simulate a session with no code modified: ensure `.claude/momentum/session-modified-files.txt` is absent; confirm lint runs and tests are skipped with correct output
  - [ ] 3.3: Simulate lint failure: introduce a lint error; confirm exit non-zero and AC3 output format
  - [ ] 3.4: Simulate test failure: introduce a failing test; confirm exit non-zero and AC5 output format
  - [ ] 3.5: Confirm session state file is deleted after each run (not accumulating between sessions)
  - [ ] 3.6: Simulate no lint tool configured: confirm `[stop-gate] ◦ lint — no lint tool configured` and no crash
  - [ ] 3.7: Simulate no test runner configured: confirm `[stop-gate] ◦ tests — no test runner configured` and no crash

## Dev Notes

### Hook Architecture (CRITICAL — read before implementing)

**Hook type:** Stop (always-on). Fires BEFORE the Claude Code session closes. Unlike PreToolUse, the Stop hook does not receive tool input — it fires with no target file argument. Exit non-zero to block session close.

**Deployment path:** Same as Stories 3.1/3.2 — always-on hooks are:
1. Defined as a template in `skills/momentum/references/hooks-config.json`
2. Written to `.claude/settings.json` by Impetus on first `/momentum` invocation
3. Script authored at `skills/momentum/references/hooks/stop-gate.sh`, deployed to `.claude/momentum/hooks/stop-gate.sh` by Impetus

**Existing hooks-config.json Stop entry (placeholder to replace):**
```json
{
  "hooks": [
    {
      "type": "command",
      "command": "echo '[momentum-gate] ✓ checked stop conditions — quality gate placeholder (Story 3.3 implements)'",
      "timeout": 10
    }
  ]
}
```
Replace the `echo` command with the actual `stop-gate.sh` invocation. No `"matcher"` field — Stop hooks fire unconditionally. [Source: `skills/momentum/references/hooks-config.json`]

**Hook command format (after replacement):**
```json
{
  "hooks": [
    {
      "type": "command",
      "command": "bash ${CLAUDE_PROJECT_DIR}/.claude/momentum/hooks/stop-gate.sh",
      "timeout": 60
    }
  ]
}
```
**Note:** Stop hooks take no arguments — the script accesses the project root via `$CLAUDE_PROJECT_DIR` env var directly. Verify the env var name in existing hooks at `.claude/settings.json`.

### How Stop Hook Blocking Works

The Stop hook blocks the session close by exiting with a non-zero exit code. Unlike PostToolUse, there is no tool to "block" — the effect is that Claude Code shows the hook output to the user and does not proceed with session close.

```bash
# Block pattern (session close prevented)
echo "[stop-gate] ✗ lint: 3 issues — src/index.js:42 — fix before closing"
exit 1

# Allow pattern (session closes normally)
exit 0
```

### Session State Contract (CRITICAL — cross-story dependency)

`.claude/momentum/session-modified-files.txt` is the inter-hook state contract:
- **Story 3.1 (PostToolUse hook) WRITES:** appends file path per Write/Edit/NotebookEdit tool use
- **Story 3.3 (Stop hook, this story) READS and DELETES:** determines if tests should run; deletes after reading

**Delete the file regardless of whether it was empty or non-existent** — ensures clean state for the next session even if the Stop hook ran for an empty/absent file.

```bash
SESSION_FILE="${CLAUDE_PROJECT_DIR}/.claude/momentum/session-modified-files.txt"

CODE_MODIFIED=false
if [ -s "$SESSION_FILE" ]; then
  CODE_MODIFIED=true
fi

# Always clean up regardless
rm -f "$SESSION_FILE"
```

**Do not use `git diff` to detect changes** — the spec explicitly requires reading the session state file only (FR20). This is deliberate: the PostToolUse hook tracks what Claude Code touched; git diff would include external editor changes to unrelated files.

### Output Format (per UX-DR3)

All outputs are one line. Architecture hook format: `[hook-name] symbol result`.

| Scenario | Output | Exit |
|---|---|---|
| Lint clean | `[stop-gate] ✓ checked lint — clean` | 0 |
| Lint failures | `[stop-gate] ✗ lint: [N issues] — [file:line of first] — fix before closing` | 1 |
| Tests pass | `[stop-gate] ✓ checked tests — [N] passed` | 0 |
| Tests fail | `[stop-gate] ✗ tests: [N failed] — [failing test name] — [failure summary]` | 1 |
| No lint tool | `[stop-gate] ◦ lint — no lint tool configured` | 0 (continue) |
| No test runner | `[stop-gate] ◦ tests — no test runner configured` | 0 (continue) |

**Multiple outputs:** The Stop hook may output multiple lines (one for lint, one for tests). This is expected — each check gets its own output line. The "one line always" principle from architecture applies per-check, not per-hook-invocation.

**Exit code logic:** Exit non-zero if lint OR tests failed. If only lint ran (no tests) and lint was clean, exit 0. If lint was skipped (no tool) and tests passed, exit 0. Only a failure result causes non-zero.

### Lint Tool Detection (reuse Story 3.1 heuristics)

The Stop hook's lint detection follows the same heuristics as `lint-format.sh` (Story 3.1), but invokes the lint tool in **full-project mode** (not per-file):

| Config found | Command |
|---|---|
| `package.json` `scripts.lint` | `npm run lint` |
| `package.json` `scripts.format` | `npm run format -- --check` (or skip for format-only; project-specific) |
| `.prettierrc` / `prettier.config.js` | `prettier --check .` |
| `.eslintrc` / `eslint.config.js` | `eslint .` |
| `pyproject.toml` `[tool.ruff]` | `ruff check .` |
| `pyproject.toml` `[tool.black]` | `black --check .` |
| `setup.cfg` `[flake8]` | `flake8 .` |
| None | Skip with `◦ lint` message |

**Do not copy `lint-format.sh`'s code verbatim** — that hook is per-file and auto-fixes; this hook is whole-project and read-only (no auto-fix at session close, just report and block).

### Test Runner Detection

| Config found | Command |
|---|---|
| `package.json` `scripts.test` | `npm test` |
| `jest.config.js` / `jest.config.ts` | `npx jest --passWithNoTests` |
| `vitest.config.js` / `vitest.config.ts` | `npx vitest run` |
| `pytest.ini` / `pyproject.toml` `[tool.pytest.ini_options]` | `pytest` |
| `setup.cfg` `[tool:pytest]` | `pytest` |
| None | Skip with `◦ tests` message |

### Timeout Considerations

Tests can be slow. The Stop hook timeout is set to 60 seconds in Task 2.4. For projects with long test suites, this may not be enough — but 60s is a reasonable default. The developer can raise it in their local `.claude/settings.json` if needed.

### Project Structure

Files to create/modify:
- `skills/momentum/references/hooks/stop-gate.sh` — the hook script (NEW; same directory as `lint-format.sh` from Story 3.1 and `file-protection.sh` from Story 3.2)
- `skills/momentum/references/hooks-config.json` — replace Stop placeholder command (MODIFY)

Files the hook will interact with at runtime:
- `.claude/settings.json` — where the hook is registered (not modified by this story)
- `.claude/momentum/session-modified-files.txt` — read and deleted at runtime

### Dependencies

- **Depends on:** Story 1.3 (Momentum hooks installed in `.claude/settings.json`) — hook deployment mechanism must be in place
- **Depends on:** Story 3.1 (PostToolUse hook writes `session-modified-files.txt`) — without this, `CODE_MODIFIED` is always false and tests never run; this is graceful (not a crash), but tests will never trigger until Story 3.1 is live
- **Depends on (soft):** Stories 3.1/3.2 for deploy path pattern established (`skills/momentum/references/hooks/`)

### Testing Standards

This is `rule-hook` + `script-code` change type — use functional verification:
1. Register hook in local `.claude/settings.json` for testing
2. Test each AC scenario (see Task 3)
3. Verify session state file is deleted after each run
4. Verify exit codes: 0 for clean, 1 for failures

### Project Structure Notes

- Hook script follows naming pattern established in Stories 3.1/3.2: `skills/momentum/references/hooks/[verb-noun].sh`
- `stop-gate.sh` — kebab-case, descriptive, no vendor prefix [Source: `_bmad-output/planning-artifacts/architecture.md` — Naming Patterns section]

### References

- Epic 3 Story 3.3 spec: `_bmad-output/planning-artifacts/epics.md#Story-3.3`
- FR20: `_bmad-output/planning-artifacts/epics.md` line 92 (conditional quality gates, PostToolUse event tracking)
- Hook Infrastructure: `_bmad-output/planning-artifacts/architecture.md` — Hook Infrastructure section
- Hook announcement format: `_bmad-output/planning-artifacts/architecture.md` line 710
- hooks-config.json placeholder: `skills/momentum/references/hooks-config.json`
- Session state contract: `_bmad-output/planning-artifacts/epics.md` line 1023 (Story 3.1 Note)
- Story 3.1 (session state writer, lint heuristics): `_bmad-output/implementation-artifacts/3-1-posttooluse-lint-and-format-hook-active.md`
- Story 3.2 (deploy path pattern): `_bmad-output/implementation-artifacts/3-2-pretooluse-file-protection-hooks-active.md`

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 (`stop-gate.sh`) → `script-code` (TDD / functional verification)
- Task 2 (`hooks-config.json` placeholder replacement) → `config-structure` (direct + inspect)
- Task 2b (deployment path) → `config-structure` (direct + inspect)
- Task 3 (verification) → `rule-hook` (functional verification)

---

### script-code Tasks: TDD / Functional Verification

The hook script is a bash file — use functional verification (unit tests for bash add test framework overhead not justified here):

1. **State the expected behavior per AC:** e.g., "Given session-modified-files.txt is present, the hook reads it, runs tests, deletes the file, and exits based on test outcome"
2. **Implement the script** per acceptance criteria
3. **Verify functionally:**
   - Create a test session state file and run: `bash stop-gate.sh` — confirm tests execute
   - Run without session state file — confirm only lint runs, tests skipped
   - Simulate lint failure — confirm exit code 1 and AC3 format
   - Simulate test failure — confirm exit code 1 and AC5 format
   - After each run, confirm session state file is gone
4. **Document** in Dev Agent Record

**DoD items for script-code tasks:**
- Functional verification performed for each AC scenario
- Script is executable (`chmod +x`)
- No regressions in Story 3.1 hook (`lint-format.sh`) or Story 3.2 (`file-protection.sh`) — they coexist in the same `hooks/` directory
- Session state file is always deleted after reading (clean state for next session)

---

### config-structure Tasks: Direct Implementation

`hooks-config.json` Stop placeholder replacement — implement directly and verify by inspection:

1. **Replace** the Stop placeholder `echo` command with the `stop-gate.sh` command
2. **Verify by inspection:**
   - `jq . skills/momentum/references/hooks-config.json` — must parse without error
   - PostToolUse entry (Story 3.1) must remain untouched
   - PreToolUse entry (Story 3.2) must remain untouched
   - Stop entry: no `"matcher"` field (Stop hooks have no matcher), timeout 60
3. **Document** the change in Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] `hooks-config.json` parses without error (validated with `jq`)
- [ ] All three hook entries present (PostToolUse, PreToolUse, Stop)
- [ ] Only the Stop `command` and `timeout` fields changed — structure preserved
- [ ] Changes documented in Dev Agent Record

---

### rule-hook Tasks: Functional Verification

1. **Write the hook** per the established format
2. **State expected behavior:** "Given a Claude Code session ends, the Stop hook runs lint unconditionally, runs tests if code was modified this session, outputs one line per check, and exits non-zero if any check fails — blocking session close"
3. **Verify functionally:** per the 7-step test plan in Task 3
4. **Document** verification result in Dev Agent Record

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as testable condition (in Dev Agent Record)
- [ ] Functional verification performed for all 7 scenarios and result documented
- [ ] Format matches established patterns (output format exactly as specified)
- [ ] Session state file deleted after every run (verified)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List
