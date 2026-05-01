---
title: Impetus Feature Status Cache — Hash-Based Staleness Detection in Greeting
story_key: impetus-feature-status-cache
status: review
epic_slug: feature-orientation
depends_on:
  - feature-status-skill
touches:
  - skills/momentum/skills/impetus/workflow.md
  - skills/momentum/skills/impetus/SKILL.md
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
change_type: skill-instruction + code
priority: high
---

# Impetus Feature Status Cache — Hash-Based Staleness Detection in Greeting

## User Story

As a developer using Impetus, I want the session greeting to show me a cached
feature status summary so I know the state of user-facing capabilities at a
glance — without slowing down session startup — so I can orient quickly and
focus on the right work.

## Description

After `momentum:feature-status` is built (dependency: `feature-status-skill`),
its output needs to surface in the Impetus greeting. The challenge: running a
full feature-status evaluation at session start would add minutes of latency —
unacceptable for a greeting.

The solution (DEC-002 D3): Impetus shows a **cached** feature status summary.
Cache validity is determined by hashing the inputs to feature-status. If the
hash matches, show the cached summary silently. If not, show it with a staleness
flag. The developer explicitly triggers a refresh; Impetus never recomputes live
on startup.

This story covers only the **read** side of the cache in Impetus. The **write**
side (generating and storing the cache after feature-status runs) belongs to the
`feature-status-skill` story.

### Cache Design

The cache IS the feature-status output file. `momentum:feature-status` writes its rendered output to `.claude/momentum/feature-status.md`. That file includes YAML frontmatter with hash and summary — no separate cache JSON needed.

- **Output file:** `.claude/momentum/feature-status.md`
  - Frontmatter fields: `input_hash` (string), `summary` (string — one-line feature status), `generated_at` (ISO 8601)
  - Body: full rendered feature-status output (for developer reference)
- **Hash inputs:** `features_file_content + ":" + stories_file_content` (raw UTF-8, SHA-256)
- **Hash command:** `momentum-tools feature-status-hash` — new command, returns `{ "hash": "...", "features_present": true|false }` — used by `momentum:feature-status` when writing the file
- **Written by:** `momentum:feature-status` after each run (out of scope for this story)
- **Read by:** `startup-preflight` command in momentum-tools.py (added in this story) — reads frontmatter only

### Greeting Rendering Rules

Four distinct cases (evaluated in order by `startup-preflight`):

| Condition | Greeting line |
|---|---|
| `features.json` absent | `? No features defined yet — run feature-artifact-schema to plan features.` |
| Output file absent | `? No feature status yet — run feature-status to generate one.` |
| Hash match (cache fresh) | `· {summary}` (summary from output file, no staleness flag) |
| Hash mismatch (cache stale) | `· {summary}  ! may be out of date — run feature-status to refresh` |

The feature status line appears as the last line of the greeting narrative,
immediately before the menu. It must not alter the menu or closer.

### NFR20 Compliance (Load-Bearing)

Startup tool call count must not increase vs baseline. The happy path currently
makes exactly **one** Bash call (`startup-preflight`). This story adds the
feature status hash check and cache read inside `startup-preflight` itself —
zero additional Bash calls at session start. The feature status fields are
returned in the existing `greeting` payload.

## Acceptance Criteria (Plain English)

1. A new `feature-status-hash` command exists in momentum-tools.py that reads
   `_bmad-output/planning-artifacts/features.json` and
   `_bmad-output/implementation-artifacts/stories/index.json`, computes SHA-256
   of the concatenated string `features_file_content + ":" + stories_file_content`
   (raw UTF-8 text, not pre-hashed), and returns
   `{ "hash": "<hex digest>", "features_present": true }`. If
   `features.json` does not exist, returns `{ "hash": "", "features_present": false }`.

2. The `startup-preflight` command is extended to compute the feature status
   fields and include them in the `greeting` payload when `route == "greeting"`.
   The computation: read `.claude/momentum/feature-status.md` frontmatter (treat
   as absent if file missing or frontmatter unparseable); run the hash logic from
   AC1 inline (no separate subprocess call); compare computed hash to `input_hash`
   from frontmatter.

3. When `features.json` is absent, `startup-preflight` sets
   `greeting.feature_status` to `{ "state": "no-features" }`. The greeting shows:
   `? No features defined yet — run feature-artifact-schema to plan features.`

4. When `features.json` is present but `.claude/momentum/feature-status.md`
   does not exist (or has no parseable frontmatter), `startup-preflight` sets
   `greeting.feature_status` to `{ "state": "no-cache" }`. The greeting shows:
   `? No feature status yet — run feature-status to generate one.`

5. When `features.json` is present and the `input_hash` in
   `feature-status.md` frontmatter matches the computed hash, `startup-preflight`
   sets `greeting.feature_status` to
   `{ "state": "fresh", "summary": "<frontmatter summary>" }`. The greeting shows
   `· {summary}` with no staleness indicator.

6. When `features.json` is present and the `input_hash` in
   `feature-status.md` frontmatter does not match the computed hash,
   `startup-preflight` sets `greeting.feature_status` to
   `{ "state": "stale", "summary": "<frontmatter summary>" }`. The greeting shows
   `· {summary}  ! may be out of date — run feature-status to refresh`

7. The Impetus SKILL.md happy-path greeting block is updated to render the
   feature status line using `{{greeting.feature_status}}` per the rendering
   rules above. The line appears immediately before the menu. The menu items and
   closer are unchanged.

8. The `momentum-tools session greeting-state` command is extended to return
   a `feature_status` field in its payload, computed with the same logic as
   AC2–AC6 (same four states: no-features, no-cache, fresh, stale). The Impetus
   workflow.md Step 7 greeting rendering block is updated identically to AC7,
   rendering `{{greeting.feature_status}}` from the `greeting-state` output.
   Both the SKILL.md happy-path block and workflow.md Step 7 render feature
   status consistently using the same field name and rendering rules.

9. The `startup-preflight` command's existing behavior is fully preserved:
   routing logic, hash drift detection, journal thread check, and all existing
   `greeting` payload fields (`state`, `narrative`, `planning_context`, `menu`,
   `closer`, `momentum_completions`) remain unchanged. `feature_status` is
   added; nothing is removed.

10. The Impetus greeting tool call count does not increase. The happy path still
    makes exactly one Bash call (`startup-preflight`) from session start to
    greeting display. The feature status cache read is internal to
    `startup-preflight`.

11. All new and modified commands have passing unit tests in
    test-momentum-tools.py following the existing subprocess-based pattern.

## Tasks

### Task 1: [x] Implement `feature-status-hash` command in momentum-tools.py

Add `cmd_feature_status_hash` to momentum-tools.py. This command:

- Reads `_bmad-output/planning-artifacts/features.json` relative to project root
- Reads `_bmad-output/implementation-artifacts/stories/index.json`
- If `features.json` does not exist: returns `{ "hash": "", "features_present": false }`
- If `features.json` exists but `stories/index.json` does not: uses empty string for stories content
- Computes SHA-256 (or `hashlib.sha256`) of: `features_content + ":" + stories_content`
- Returns `{ "hash": "<hex digest>", "features_present": true }`
- Registers as top-level subcommand: `momentum-tools feature-status-hash`

#### Subtask 1a: [x] Hash computation logic

Implement the file reading and SHA computation. Use `hashlib.sha256` —
consistent with the existing hash patterns in the codebase.

#### Subtask 1b: [x] CLI registration

Register `feature-status-hash` as a top-level command (alongside `session`,
`sprint`, etc.) with `set_defaults(func=cmd_feature_status_hash)`.

### Task 2: [x] Extend `startup-preflight` to include feature status fields

Extend `cmd_session_startup_preflight` to compute feature status inline when
`route == "greeting"`. This runs inside the existing function — no new Bash
subprocess:

- Resolve `features.json` path: `{project_dir}/_bmad-output/planning-artifacts/features.json`
- Resolve `stories/index.json` path: `{project_dir}/_bmad-output/implementation-artifacts/stories/index.json`
- Resolve output file path: `{claude_project_dir}/.claude/momentum/feature-status.md`
- If `features.json` does not exist: `feature_status = { "state": "no-features" }`
- Else:
  - Read features content (or empty string if unreadable)
  - Read stories content (or empty string if unreadable)
  - Compute hash: `hashlib.sha256((features_content + ":" + stories_content).encode()).hexdigest()`
  - Read `feature-status.md` frontmatter (treat as absent if file missing or frontmatter unparseable)
  - If file/frontmatter absent: `feature_status = { "state": "no-cache" }`
  - Elif `frontmatter["input_hash"] == computed_hash`: `feature_status = { "state": "fresh", "summary": frontmatter.get("summary", "") }`
  - Else: `feature_status = { "state": "stale", "summary": frontmatter.get("summary", "") }`
- Add `feature_status` to the `greeting` dict before the `result(...)` call

#### Subtask 2a: [x] Extract `_compute_feature_status` shared helper

Extract the feature status computation into a standalone module-level helper
function: `_compute_feature_status(project_dir: Path, claude_project_dir: Path) -> dict`.
This helper is called by both `startup-preflight` and `greeting-state` (Task 4)
to keep the logic DRY. The function always returns a dict with a `state` key —
one of `no-features`, `no-cache`, `fresh`, or `stale`.

#### Subtask 2b: [x] Feature status inline computation

Call `_compute_feature_status(project_dir, claude_project_dir)` inside
`cmd_session_startup_preflight` when `route == "greeting"`. Store the result
as `feature_status`. Import `hashlib` at the top of the function or file if
not already present — check existing imports first.

#### Subtask 2c: [x] Payload extension

Extend the `greeting` dict with `"feature_status": feature_status`. Ensure
`feature_status` is `None` (not absent) when `features.json` is absent so the
greeting template can test for it safely.

### Task 3: [x] Update SKILL.md happy-path greeting block

Update the happy-path `<check if="preflight.route == 'greeting' AND preflight.has_open_threads == false">` block in `skills/momentum/skills/impetus/SKILL.md` to render the feature status line:

```
  {{greeting.narrative}}
  {{greeting.planning_context — include only if non-null, on its own line}}
  {{feature_status line — render per rules below, omit if greeting.feature_status is null}}

  {{greeting.menu — each item on its own line}}

  {{greeting.closer}}
```

Feature status rendering rules (inline in SKILL.md):
- `state == "no-features"` → `? No features defined yet — run feature-artifact-schema to plan features.`
- `state == "no-cache"` → `? No feature status yet — run feature-status to generate one.`
- `state == "fresh"` → `· {greeting.feature_status.summary}`
- `state == "stale"` → `· {greeting.feature_status.summary}  ! may be out of date — run feature-status to refresh`

### Task 4: [x] Extend `greeting-state` command and update workflow.md Step 7

#### Subtask 4a: [x] Extend `cmd_session_greeting_state`

Call `_compute_feature_status(project_dir, claude_project_dir)` (extracted in
Subtask 2a) inside `cmd_session_greeting_state` and add `feature_status` to its
return payload. This is the data source for workflow.md Step 7 rendering.

#### Subtask 4b: [x] Update workflow.md Step 7 greeting rendering

Update the `<output>` block in Step 7 of `skills/momentum/skills/impetus/workflow.md`
to render the feature status line identically to the SKILL.md update in Task 3.
Step 7 reads `{{greeting}}` from `momentum-tools session greeting-state` output —
the `{{greeting.feature_status}}` field is now available via Subtask 4a.

### Task 5: [x] Unit tests for `feature-status-hash` and preflight extension

Add tests in test-momentum-tools.py following the existing subprocess-based
pattern. All tests must pass; no regressions in existing suite.

| Test Name | What It Verifies |
|---|---|
| `test_feature_status_hash_no_features_file` | Returns `features_present: false`, empty hash when `features.json` absent |
| `test_feature_status_hash_with_features_file` | Returns `features_present: true`, non-empty hash when file present |
| `test_feature_status_hash_deterministic` | Same inputs produce same hash on repeated calls |
| `test_feature_status_hash_changes_on_features_change` | Hash differs when `features.json` content changes |
| `test_feature_status_hash_changes_on_stories_change` | Hash differs when `stories/index.json` content changes |
| `test_preflight_feature_status_no_features` | `greeting.feature_status.state == "no-features"` when `features.json` absent |
| `test_preflight_feature_status_no_cache` | `greeting.feature_status.state == "no-cache"` when cache absent |
| `test_preflight_feature_status_fresh` | `state == "fresh"`, correct summary when hash matches |
| `test_preflight_feature_status_stale` | `state == "stale"`, correct summary when hash mismatches |
| `test_preflight_feature_status_invalid_cache_json` | Invalid cache JSON treated as absent (no-cache state) |
| `test_greeting_state_feature_status_no_features` | `greeting-state` returns `state == "no-features"` when `features.json` absent |
| `test_greeting_state_feature_status_no_cache` | `greeting-state` returns `state == "no-cache"` when cache absent |
| `test_greeting_state_feature_status_fresh` | `greeting-state` returns `state == "fresh"` with correct summary |
| `test_greeting_state_feature_status_stale` | `greeting-state` returns `state == "stale"` with correct summary |

## Dev Notes

### Output file format

`.claude/momentum/feature-status.md` is both the persistent output and the cache.
`momentum:feature-status` writes it; Impetus reads it. No separate JSON file.

```
---
input_hash: abc123...
summary: 4 features: 2 working · 1 partial · 1 not-started
generated_at: 2026-04-11T10:00:00
---

[full rendered feature-status output here]
```

The `summary` frontmatter field is a single line for the greeting. The body is
the full skill output for when the developer reads the file directly.
`momentum:feature-status` is responsible for keeping the summary concise (out
of scope here). Impetus reads only the frontmatter and renders `summary` verbatim.

### Hash algorithm

Use `hashlib.sha256`. The combined input string is:
`features_file_content + ":" + stories_file_content`

Read both files as raw UTF-8 text. Do not parse JSON before hashing — hash
the raw file bytes (as text). This is consistent with `git hash-object`-style
content addressing already used elsewhere in Impetus.

### Why not call `feature-status-hash` as a subprocess from `startup-preflight`?

NFR20: startup tool call count must not increase. Calling `feature-status-hash`
as a subprocess would add a second Bash call. Instead, extract the hash
computation into a shared Python helper `_compute_feature_status(project_dir,
claude_project_dir)` that both `startup-preflight` and `greeting-state` call
directly. The `feature-status-hash` CLI command exists as a standalone utility
for use by `momentum:feature-status` when it writes the cache — it is not
called by Impetus at startup.

### Greeting rendering position

The feature status line sits between `planning_context` (or `narrative` if no
`planning_context`) and the menu blank line. Leave one blank line before the
menu, matching the existing greeting format:

```
Sprint "sprint-name" is underway — steady ground.         ← narrative
"next-sprint" is taking shape behind it.                  ← planning_context (if any)
· 4 features: 2 working · 1 partial · 1 not-started      ← feature_status (fresh/stale/no-cache/no-features)

[1] Continue the sprint                                   ← menu (blank line before)
[2] Refine backlog
[3] Triage

Lead on.                                                  ← closer
```

### Impetus SKILL.md and workflow.md both need updating

Two places render the greeting:
1. **SKILL.md** (happy path) — the `<check if="route == 'greeting' AND has_open_threads == false">` block
2. **workflow.md Step 7** — used when the workflow file is loaded (after upgrade, hash-drift, etc.)

Both must render the feature status line consistently. The shared helper
`_compute_feature_status` ensures both `startup-preflight` (used by SKILL.md)
and `greeting-state` (used by workflow.md Step 7) return the same `feature_status`
payload.

### Downstream story: feature-status-skill owns the write side

This story only adds the **read** path. The `momentum:feature-status` skill
(story: `feature-status-skill`) is responsible for:
- Running the evaluation
- Composing the `summary` string
- Writing `.claude/momentum/feature-status.md` with frontmatter (`input_hash`,
  `summary`, `generated_at`) and the full rendered output as the body

Before `feature-status-skill` is implemented, the output file will never exist.
Impetus will show `? No feature status yet — run feature-status to generate one.`
consistently. This is the correct behavior and requires no special handling here.

### Decision gates (DEC-002)

This story implements DEC-002 D3 (read side only). Per DEC-002:
- D3 cannot be fully activated before D2 (`feature-status-skill`) exists
- D2 cannot be activated before D1 (`feature-artifact-schema`) — `features.json` must exist
- This story's code can ship before D1/D2 are done because `features.json`
  absent → silent omission (AC3). No user-visible change until both D1 and D2
  are complete.

### Files

- `skills/momentum/scripts/momentum-tools.py` — add `feature-status-hash` command and extend `startup-preflight` + `greeting-state`
- `skills/momentum/scripts/test-momentum-tools.py` — add 10 unit tests
- `skills/momentum/skills/impetus/SKILL.md` — update happy-path greeting block (Task 3)
- `skills/momentum/skills/impetus/workflow.md` — update Step 7 greeting rendering (Task 4)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 5 → script-code (TDD)
- Tasks 3, 4 → skill-instruction (EDD)

> **Routing note:** Tasks 1, 2, and 5 are Python changes to `momentum-tools.py` and must be executed via `momentum:dev` (bmad-dev-story), which handles TDD natively — dev-skills alone is not sufficient for these tasks. Tasks 3 and 4 are skill-instruction changes that follow the EDD process below.

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum/skills/[name]/scripts/` or `skills/momentum/scripts/`. Follow the pattern in existing Momentum scripts for language choice and structure. The test file is `skills/momentum/scripts/test-momentum-tools.py`.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies — listed here for reference):**
- Tests written and passing
- No regressions in existing test suite
- Code quality checks pass if configured

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill changes:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/impetus/evals/` (one `.md` file per eval):
   - Format: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text
   - Examples: `eval-feature-status-fresh-greeting.md`, `eval-feature-status-stale-greeting.md`, `eval-feature-status-absent-omitted.md`

**Then implement:**
2. Modify SKILL.md and workflow.md

**Then verify:**
3. Run evals by spawning a subagent per eval, providing the scenario + skill content. Observe whether behavior matches the expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap, revise, re-run (max 3 cycles)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1)
- `model:` and `effort:` frontmatter fields must be present (NFR3/FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12)

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/impetus/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed

**Gherkin specs note:** Gherkin specs for this sprint live in `sprints/{sprint-slug}/specs/`. They are off-limits to the dev agent — implement against the plain English ACs in this story file only. Do not read or reference `.feature` files during implementation (Decision 30 black-box separation).

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None.

### Completion Notes List

- Implemented `_read_frontmatter()` helper to parse YAML-style frontmatter from markdown files (returns None if absent/unparseable)
- Implemented `_compute_feature_status(project_dir, claude_project_dir)` shared helper — four states: no-features, no-cache, fresh, stale
- Implemented `cmd_feature_status_hash` as a top-level subcommand returning `{ hash_result: { hash, features_present } }`
- Extended `cmd_session_startup_preflight`: calls `_compute_feature_status` when `route == "greeting"` and adds `feature_status` to the greeting dict
- Extended `cmd_session_greeting_state`: calls `_compute_feature_status` and adds `feature_status` to output payload
- Updated SKILL.md happy-path `<check>` block with inline feature status rendering rules (4 states) and updated output template
- Updated workflow.md Step 7 output block identically to SKILL.md
- EDD: wrote 3 behavioral evals in `evals/` — all behaviors confirmed by inspection
- TDD: wrote 14 unit tests (5 for feature-status-hash, 5 for preflight feature-status, 4 for greeting-state feature-status) — all pass; 386 total tests pass, 0 regressions

### File List

- skills/momentum/scripts/momentum-tools.py
- skills/momentum/scripts/test-momentum-tools.py
- skills/momentum/skills/impetus/SKILL.md
- skills/momentum/skills/impetus/workflow.md
- skills/momentum/skills/impetus/evals/eval-feature-status-fresh-greeting.md
- skills/momentum/skills/impetus/evals/eval-feature-status-stale-greeting.md
- skills/momentum/skills/impetus/evals/eval-feature-status-absent-omitted.md
