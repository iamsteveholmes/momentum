---
title: Impetus Session-Start Staleness Check — Detect Plugin Cache Skew and Prompt Update+Restart
story_key: plugin-cache-staleness-detection
story_type: practice
status: ready-for-dev
epic_slug: impetus-core
priority: critical
depends_on: []
touches:
  - skills/momentum/skills/impetus/SKILL.md
  - skills/momentum/skills/impetus/references/orient.md
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/skills/impetus/references/staleness-warning.md
  - skills/momentum/skills/impetus/evals/
change_type: skill-instruction + script-code
source: retro sprint-2026-04-14 action item #1 (rescoped from "high" to "critical" headline systemic finding)
---

# Plugin Cache Staleness Detection — Impetus Session-Start Skew Warning

## Story

**As** the developer running Momentum workflows from a working copy of the momentum repo,
**I want** Impetus to detect at session start when the active Claude Code plugin cache version
of momentum has drifted from the source-tree version,
**so that** I am warned before invoking workflows that would silently execute stale
`workflow.md` content frozen in the plugin cache, and pointed at the exact remedy
(`/plugin marketplace update momentum` then session restart).

## Description

The sprint-2026-04-14 retro identified plugin-cache staleness as the **headline systemic
defect** of the sprint: the Claude Code plugin cache contains a frozen snapshot of momentum
at install/update time, and edits to the source tree do not become live until both
`/plugin marketplace update momentum` is run AND a fresh Claude Code session is started.
Until then, every workflow dispatched through `/momentum:*` runs against the cached
`workflow.md` files — including `momentum:distill`, which writes to source-tree skill files
that the running session will not see, silently invalidating the distill.

The primary mitigation is **operator discipline** (`feedback_fresh_session_before_major_workflows`):
update the marketplace and start a fresh session before any major Momentum workflow. Operators
forget. This story is the **safety net** — a session-start detector that catches the skew
when discipline lapses, names it explicitly, and points at the remedy. It does not replace
the operator-discipline rule; it reinforces it.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Plugin Cache Staleness Detection at Impetus Session Start

  Background:
    Given the Momentum plugin is installed via Claude Code's plugin marketplace
    And the developer is invoking /momentum:impetus from inside a momentum source-tree checkout

  Scenario: Cache version matches source-tree version — silent pass
    Given the active plugin cache version equals the source-tree plugin.json version
    When Impetus runs its session-start preflight
    Then no staleness warning is surfaced
    And the orientation greeting proceeds normally
    And no extra latency is added beyond reading two small JSON files

  Scenario: Cache version is older than source-tree version — warn
    Given the active plugin cache version is "0.17.0"
    And the source-tree plugin.json version is "0.18.0"
    When Impetus runs its session-start preflight
    Then a prominent warning is surfaced before the orientation greeting
    And the warning names both versions explicitly (cache 0.17.0 vs source 0.18.0)
    And the warning explains that workflows running under the stale cache will silently use outdated workflow.md content
    And the warning instructs the developer to run /plugin marketplace update momentum and start a fresh session
    And the warning reinforces (does not replace) the operator-discipline rule for fresh sessions before major workflows

  Scenario: Cache version is newer than source-tree version — warn
    Given the active plugin cache version is "0.18.0"
    And the source-tree plugin.json version is "0.17.0"
    When Impetus runs its session-start preflight
    Then a staleness warning is surfaced naming the version mismatch
    And the warning indicates the source tree is behind the cache (the developer is on an older branch or has not pulled)
    And the warning suggests verifying the working branch and pulling the latest source

  Scenario: Multiple cache versions present — highest version is treated as active
    Given the cache directory contains versions 0.16.0, 0.17.1, and 0.17.2
    And the source-tree plugin.json version is "0.17.2"
    When Impetus runs its session-start preflight
    Then the active cache version is detected as 0.17.2
    And no warning is surfaced because the active cache matches source

  Scenario: Plugin cache directory does not exist — silent pass
    Given the plugin cache directory ~/.claude/plugins/cache/momentum/momentum/ does not exist
    When Impetus runs its session-start preflight
    Then no warning is surfaced
    And no error is raised
    And the orientation greeting proceeds normally
    And the situation is treated as "developer is not running through the plugin install — nothing to compare against"

  Scenario: Source-tree plugin.json not resolvable — silent pass
    Given Impetus is invoked outside any momentum source-tree checkout
    When Impetus runs its session-start preflight
    Then no warning is surfaced
    And no error is raised
    And the orientation greeting proceeds normally

  Scenario: Cache plugin.json is malformed JSON — silent pass with diagnostic
    Given the active cache directory's plugin.json is unparseable JSON
    When Impetus runs its session-start preflight
    Then no crash occurs
    And the staleness check exits cleanly without surfacing a false-positive warning
    And the diagnostic note is recorded for the session log (so the issue is debuggable later)

  Scenario: Source plugin.json is missing the version field — silent pass
    Given the source-tree plugin.json exists but has no "version" key
    When Impetus runs its session-start preflight
    Then no crash occurs
    And the staleness check exits cleanly without surfacing a false-positive warning

  Scenario: Cache directory has no version subdirectories — silent pass
    Given ~/.claude/plugins/cache/momentum/momentum/ exists but contains no version directories
    When Impetus runs its session-start preflight
    Then no warning is surfaced
    And no error is raised
    And the orientation greeting proceeds normally

  Scenario: Comparison helper is invokable from momentum-tools CLI
    Given the developer wants to verify the staleness check manually
    When they run `python3 skills/momentum/scripts/momentum-tools.py session plugin-cache-check`
    Then a JSON object is printed to stdout
    And the JSON contains keys: cache_version, source_version, status (one of "match", "skew-cache-behind", "skew-cache-ahead", "no-cache", "no-source", "indeterminate")
    And the exit code is 0 even when status indicates skew (so callers parse the JSON, not exit codes)

  Scenario: Latency budget is preserved
    Given the staleness check is the first action in the Impetus preflight
    When Impetus runs from a cold session
    Then the staleness check adds no more than the cost of two small JSON file reads (no git, no network, no subprocess except an optional CLI call)
    And the check completes in under 50ms in the typical case (per feedback_impetus_startup_latency)

  Scenario: Warning copy preserves operator-discipline framing
    Given any version skew is detected
    When the warning is rendered
    Then the warning explicitly names the operator-discipline rule (fresh session before major workflows) as the primary mitigation
    And the warning frames itself as a safety net, not a replacement
    And the warning does not introduce sycophantic or apologetic language
```

## Tasks / Subtasks

- [ ] **Task 1 — Add `session plugin-cache-check` subcommand to `momentum-tools.py`** (AC: 10, 11)
  - [ ] 1.1 Implement a new `cmd_session_plugin_cache_check(args)` function in `skills/momentum/scripts/momentum-tools.py`
  - [ ] 1.2 Register the subcommand under the existing `session` command group (alongside `session startup-preflight`, `session greeting-state`, etc.)
  - [ ] 1.3 Resolve the active cache directory: scan `~/.claude/plugins/cache/momentum/momentum/` for version subdirectories, sort using semver-aware ordering (or lexicographic if all components are numeric), pick the highest as active. If the directory is missing or empty, return `status: "no-cache"`.
  - [ ] 1.4 Read `<active-cache>/.claude-plugin/plugin.json` and extract the `version` field. On malformed JSON or missing field, return `status: "indeterminate"` with a diagnostic key naming which file failed.
  - [ ] 1.5 Resolve the source-tree plugin.json: use `resolve_project_dir()` (already in the script) to find the momentum repo, then read `<project-dir>/skills/momentum/.claude-plugin/plugin.json`. If the file does not exist, return `status: "no-source"`. If malformed or missing version, return `status: "indeterminate"`.
  - [ ] 1.6 Compare versions semantically: equal → `match`; cache < source → `skew-cache-behind`; cache > source → `skew-cache-ahead`. Print a JSON object with `{cache_version, source_version, active_cache_dir, status, diagnostic?}` to stdout. Exit 0 in all cases.
  - [ ] 1.7 Use `packaging.version` if already imported, otherwise compare as tuples of integers split on `.`; tolerate non-numeric segments by falling back to string comparison and including a diagnostic note.

- [ ] **Task 2 — Add unit tests for the new subcommand** (AC: 1–9, 10)
  - [ ] 2.1 Add tests to `skills/momentum/scripts/test-momentum-tools.py` covering: match, skew-cache-behind, skew-cache-ahead, no-cache, no-source, indeterminate (malformed cache JSON), indeterminate (malformed source JSON), missing version field, multiple cache versions (highest selected).
  - [ ] 2.2 Use `tmp_path` fixtures to construct realistic cache and source-tree directory layouts.
  - [ ] 2.3 Assert that `status` is correct, `cache_version`/`source_version` are reported accurately (or null when absent), and exit code is 0 in every case.

- [ ] **Task 3 — Wire the staleness check into Impetus preflight** (AC: 1, 2, 3, 4, 5, 6, 11, 12)
  - [ ] 3.1 In `skills/momentum/skills/impetus/SKILL.md`, add a step in the **On Activation** sequence that runs **before** sanctum loading (or for First Breath, before the greeting): invoke `python3 {project-root}/skills/momentum/scripts/momentum-tools.py session plugin-cache-check`. Parse the JSON output.
  - [ ] 3.2 If `status == "match"` or `status == "no-cache"` or `status == "no-source"`, proceed silently with no output to the developer.
  - [ ] 3.3 If `status == "skew-cache-behind"` or `status == "skew-cache-ahead"`, surface a prominent warning **before** the orientation greeting using the copy template defined in Task 4.
  - [ ] 3.4 If `status == "indeterminate"`, treat as silent pass for the developer but record the diagnostic in the session log per `references/memory-guidance.md`.
  - [ ] 3.5 Update `skills/momentum/skills/impetus/references/orient.md` if the warning placement requires preserving the silent-read principle ("Never narrate the reads") — the staleness warning is the one explicit exception and must be documented as such.

- [ ] **Task 4 — Author warning-copy template** (AC: 2, 3, 12)
  - [ ] 4.1 Add a Warning Templates section (or a new `references/staleness-warning.md`) inside `skills/momentum/skills/impetus/references/` containing two parameterized warning templates: one for `skew-cache-behind` (cache older), one for `skew-cache-ahead` (cache newer).
  - [ ] 4.2 Each template names both versions, explains the silent-failure mode (workflows run against stale workflow.md content), instructs the remedy (`/plugin marketplace update momentum` then session restart for cache-behind; verify branch + pull for cache-ahead), and reinforces the operator-discipline rule as the primary mitigation.
  - [ ] 4.3 Voice must conform to the established Impetus identity (Optimus Prime conviction + KITT attentive service, per `skills/momentum/skills/impetus/SKILL.md`) — direct, grounded, no sycophancy, no apologies for the warning itself.

- [ ] **Task 5 — EDD evals for the staleness-warning behavior** (AC: 1, 2, 3, 7, 12)
  - [ ] 5.1 Add `skills/momentum/skills/impetus/evals/eval-staleness-warning-on-cache-behind.md` — given a cache version older than source, Impetus surfaces the warning with both versions named, the remedy, and the operator-discipline reinforcement.
  - [ ] 5.2 Add `skills/momentum/skills/impetus/evals/eval-staleness-silent-on-match.md` — given matching versions, no staleness warning appears in the orientation output.
  - [ ] 5.3 Add `skills/momentum/skills/impetus/evals/eval-staleness-tolerant-of-missing-cache.md` — given the cache directory does not exist, Impetus does not surface a warning and does not crash.
  - [ ] 5.4 Run the evals via the Agent tool per the EDD pattern in `skills/momentum/skills/create-story/references/change-types.md` skill-instruction template.

- [ ] **Task 6 — Documentation cross-references** (AC: 12)
  - [ ] 6.1 Add a one-paragraph note in `skills/momentum/skills/impetus/SKILL.md` (or in a new section of `references/orient.md`) flagging the staleness check as the one explicit exception to the "never narrate the reads" rule, with a cross-reference to the operator-discipline memory.
  - [ ] 6.2 Confirm `_bmad-output/planning-artifacts/architecture.md` does not need a new Decision entry — this is an orchestrator behavior addition, not a new architectural concept (operator-discipline mitigation is already implicit). If the team review judges otherwise, add a short note under the Impetus row of the architecture's Read/Write Authority table.

## Dev Notes

### What exists today

- `skills/momentum/skills/impetus/SKILL.md` (43 lines) — minimal orchestrator file. The **On Activation** section already routes between First Breath (no sanctum) and Rebirth (sanctum exists). There is no preflight step before sanctum loading today.
- `skills/momentum/skills/impetus/references/orient.md` — defines the silent-read principle ("Never narrate the reads. Ever."). This story introduces the **one explicit exception** (the staleness warning), so `orient.md` should be updated to document this exception.
- `skills/momentum/scripts/momentum-tools.py` (1922 lines) — the deterministic CLI. Already has a `cmd_session_startup_preflight` function (line 965) that does version comparison for momentum-versions.json (a different concern — module-content version vs plugin-package version). The new `session plugin-cache-check` lives alongside it and follows the same JSON-out-on-stdout, exit-0 contract used throughout the file.
- `skills/momentum/scripts/test-momentum-tools.py` — pytest-style tests using tmp_path fixtures. Pattern: construct synthetic project dirs, invoke command functions directly, assert on returned data or stdout JSON.
- `skills/momentum/.claude-plugin/plugin.json` — source-tree plugin manifest. Currently version `0.17.2`.
- `~/.claude/plugins/cache/momentum/momentum/<version>/.claude-plugin/plugin.json` — installed plugin cache. Multiple version directories may coexist (e.g., 0.16.0, 0.17.0, 0.17.1, 0.17.2 all observed in current cache); the **highest** is the active one.

### Why this is critical

From the sprint-2026-04-14 retro summary (`_bmad-output/implementation-artifacts/sprints/sprint-2026-04-14/sprint-summary.md`): "**plugin-cache staleness silently invalidates every distill to a plugin-installed workflow.md** — mitigated by operator discipline; detector is a belt-and-suspenders." This was the single highest-impact finding of the sprint because it invalidates a feedback loop the practice depends on (distill → improved skills → better next session). Operator discipline (memory `feedback_fresh_session_before_major_workflows`) is the primary mitigation; this story is the safety net.

### What to change — architectural placement

The staleness check is a **session-start preflight**. It must run before the orientation greeting (so the developer sees the warning before deciding what to do) and before any other workflow dispatch. The cleanest placement is in `skills/momentum/skills/impetus/SKILL.md` **On Activation**, as a new step **before** the sanctum-existence check. Both First Breath and Rebirth paths must include it.

Implementation strategy: keep the comparison logic in `momentum-tools.py` (deterministic, testable, reusable) and have Impetus invoke the CLI and parse the JSON. This matches the existing pattern (Impetus already calls `momentum-tools` for sprint state, feature-status hash, journal status, etc.) and keeps Impetus's SKILL.md prompt-only, no Python-version-comparison logic embedded in markdown.

### What NOT to change

- Do not modify the existing `cmd_session_startup_preflight` function — that handles a different concern (module-content version drift via momentum-versions.json + installed.json). The new check is plugin-package version drift via the plugin cache directory.
- Do not add the staleness warning to `momentum:dev`, `momentum:distill`, `momentum:sprint-dev`, or any non-orientation skill. The check is a **session-start** safety net; embedding it in every skill would introduce noise and duplicate the operator-discipline reminder.
- Do not block, halt, or hard-fail on skew. The check warns and continues. The developer chooses the remedy.

### Determinism boundary

- `momentum-tools.py session plugin-cache-check` is the deterministic primitive. It produces machine-readable JSON.
- Impetus parses the JSON and renders the warning in its own voice. The warning copy lives in `references/` so it can be tuned without touching SKILL.md.

### Cache version detection — version sort

The cache directory may contain multiple version subdirectories. Use semver-aware ordering: split on `.`, compare components as integers when numeric, fall back to string comparison otherwise. Highest wins. Example: with `[0.16.0, 0.17.0, 0.17.1, 0.17.2]`, the active version is `0.17.2`. If a non-semver directory name appears (e.g., `dev`, `0.17.2-rc1`), include it in sort but flag in the diagnostic if it ends up being selected.

### Latency budget

Per `feedback_impetus_startup_latency`, Impetus startup must minimize tool calls. The staleness check is **two file reads** in the typical case (one cache plugin.json, one source plugin.json) plus a directory listing. No git operations, no network, no recursive walks. Well under 50ms typical. The CLI subprocess invocation is the main cost; this is acceptable because Impetus already invokes `momentum-tools` for other preflight reasons and these can be batched if latency becomes an issue (out of scope for this story; see future-work note below).

### Tolerance — degrade gracefully, never crash

Every failure mode (missing cache dir, missing source plugin.json, malformed JSON, missing version field, no version subdirectories) must result in **silent pass** for the developer (no false-positive warning) and a clean JSON output with `status: "indeterminate"` or `status: "no-cache"` / `"no-source"` plus a `diagnostic` key naming the failure. The check is a safety net — it must never itself become a source of friction.

### Warning copy — voice and framing

The warning is the one explicit exception to `orient.md`'s "never narrate the reads" rule. It must:
1. Name both versions explicitly (cache X.Y.Z vs source A.B.C).
2. Explain the silent-failure mode in one sentence (workflows will run against stale `workflow.md` content from the plugin cache).
3. State the remedy in one line (`/plugin marketplace update momentum` then start a fresh Claude Code session).
4. Reinforce the operator-discipline rule (fresh session before major workflows is the primary mitigation; this is a safety net).
5. Be in Impetus's voice — direct, grounded, no apologies, no sycophancy.

### Project Structure Notes

This story creates no new directories. It adds:
- One new function in `skills/momentum/scripts/momentum-tools.py`
- One new subcommand registration in the same file
- New tests in `skills/momentum/scripts/test-momentum-tools.py`
- New EDD eval files in `skills/momentum/skills/impetus/evals/`
- A modified `On Activation` step in `skills/momentum/skills/impetus/SKILL.md`
- Updated `skills/momentum/skills/impetus/references/orient.md` documenting the explicit exception
- A new `skills/momentum/skills/impetus/references/staleness-warning.md` (or inline in SKILL.md if short)

All paths follow the established Momentum repository structure (architecture.md Repository Structure section).

### Out of scope for this story

- **Auto-update / auto-restart.** This story warns; it does not perform `/plugin marketplace update` or restart the session on the developer's behalf. Both actions are developer-mediated.
- **Per-workflow staleness rechecks.** The check runs once at session start. If the developer ignores the warning and runs `momentum:distill` anyway, the distill itself does not re-warn. (Future work, if telemetry shows this is a real failure mode.)
- **Detection of cache hash drift below the version field** — e.g., a cache directory that has the right version number but stale content. Out of scope; the version field is the contract.
- **Replacing operator discipline.** This story is explicitly the safety net.

### References

- Source decision: sprint-2026-04-14 retro summary (`_bmad-output/implementation-artifacts/sprints/sprint-2026-04-14/sprint-summary.md`, Unresolved Issues section)
- Operator-discipline memory: `feedback_fresh_session_before_major_workflows`
- Latency constraint memory: `feedback_impetus_startup_latency`
- Impetus identity contract: `skills/momentum/skills/impetus/SKILL.md` (The Three Laws, Sacred Truth, voice)
- Silent-read principle: `skills/momentum/skills/impetus/references/orient.md`
- Existing preflight pattern: `skills/momentum/scripts/momentum-tools.py` `cmd_session_startup_preflight` (line 965)
- Architecture context: `_bmad-output/planning-artifacts/architecture.md` (Plugin model, Impetus orchestrating agent, Read/Write Authority table)
- Epic membership: Epic 10 — Impetus Core Infrastructure (`_bmad-output/planning-artifacts/epics.md` lines 642–658)
- Change-type template: `skills/momentum/skills/create-story/references/change-types.md` (skill-instruction + script-code mixed story)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → script-code (TDD)
- Tasks 3, 4, 5, 6 → skill-instruction (EDD)

This is a mixed-type story. The deterministic primitive (Python CLI subcommand + tests) follows TDD via bmad-dev-story. The orchestrator wiring and warning-copy authoring follow EDD with behavioral evals.

---

### script-code Tasks: TDD via bmad-dev-story (Tasks 1, 2)

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum/skills/[name]/scripts/` or `skills/momentum/scripts/`. Follow the pattern in existing Momentum scripts for language choice and structure. The new subcommand belongs in the existing `momentum-tools.py` (single CLI tool, one subcommand among many) — do not create a new script file.

**DoD items for script-code tasks:**
- Tests written and passing
- No regressions in existing test suite (run `pytest skills/momentum/scripts/test-momentum-tools.py` end-to-end)
- All nine scenario classes from Task 2 covered
- JSON output schema documented inline in the function docstring

---

### skill-instruction Tasks: Eval-Driven Development (EDD) (Tasks 3, 4, 5, 6)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill changes:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/impetus/evals/` (already exists):
   - One `.md` file per eval, named descriptively (e.g., `eval-staleness-warning-on-cache-behind.md`, `eval-staleness-silent-on-match.md`, `eval-staleness-tolerant-of-missing-cache.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the `SKILL.md`, `references/orient.md`, and `references/staleness-warning.md` files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and reference contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely (the existing description is fine; this story does not change it)
- `model:` and `effort:` frontmatter fields must be present (already present in the existing SKILL.md)
- SKILL.md body must stay under 500 lines / 5000 tokens; the current file is 43 lines and adding the preflight step will keep it well under the cap. The warning-copy template lives in `references/staleness-warning.md`, not inline.
- Skill names use `momentum:` namespace prefix (NFR12) — Impetus is already namespaced as `momentum:impetus`.

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 3 behavioral evals written in `skills/momentum/skills/impetus/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (the existing value is preserved)
- [ ] `model:` and `effort:` frontmatter present and correct (preserved from existing file)
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] AVFL checkpoint on the modified Impetus skill documented (momentum:dev runs this automatically against story ACs)

---

### DoD additions specific to this story's change types

- [ ] Both Cache-behind and Cache-ahead skew scenarios produce a warning that names both versions explicitly
- [ ] All five tolerance scenarios (no-cache, no-source, malformed cache JSON, malformed source JSON, missing version field, no version subdirs) produce silent pass with no false-positive warning
- [ ] CLI subcommand returns exit code 0 in all cases (callers parse JSON, not exit codes) — verified by tests
- [ ] Latency overhead in the match-case (typical hot path) is no worse than the existing preflight cost — verified by inspection (no git, no network, two file reads max)
- [ ] Warning copy reinforces the operator-discipline rule explicitly (per AC scenario 12) — verified by EDD eval
- [ ] `references/orient.md` is updated to document the staleness warning as the one explicit exception to the silent-read rule

### Gherkin reminder for the dev agent

Gherkin specs may be generated for this sprint under `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-27/specs/` during sprint planning. Per Decision 30 (black-box separation), those `.feature` files are **off-limits to the dev agent**. The dev agent implements against the plain-English Acceptance Criteria in this story file only — never against `.feature` files. If a discrepancy is suspected between the story ACs and the Gherkin specs, surface the question; do not consult the specs directly.

## Dev Agent Record

### Agent Model Used

(to be filled by dev agent)

### Debug Log References

### Completion Notes List

### File List
