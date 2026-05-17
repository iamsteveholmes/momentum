---
title: "Routing Table Schema and Implementation"
story_key: routing-table-schema-and-implementation
status: ready-for-dev
story_type: feature
epic_slug: agent-team-model
feature_slug: momentum-agent-composition-pipeline
change_type: [config-structure, skill-instruction]
depends_on: [agent-builder-skill]
touches:
  - momentum/agents.json
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/skills/sprint-dev/workflow.md
---

# Routing Table Schema and Implementation

## Story

As a Momentum skill orchestrating agent spawning,
I need to resolve the correct agent(s) for a given set of file paths by consulting a machine-readable routing table (`momentum/agents.json`),
so that every spawning skill produces correct domain-scoped agents without hardcoding agent names.

## Description

This story establishes `momentum/agents.json` — the load-bearing schema layer for the agent composition pipeline (DEC-023). Without this table, all downstream stories in the `agent-team-model` epic (specialist-classify-multi-result, change-type-routing-in-sprint-dev) cannot function.

The routing table has two sections:

- **`defaults` block** — ships with the Momentum plugin; one entry per universal role, pointing to `skills/momentum/agents/{role}.md`. Nine roles total: architect, pm, ux, analyst, researcher, dev, sm, qa-reviewer, e2e-validator.
- **`project` array** — written by `agent-builder` at composition time; one entry per role × domain combination with file patterns and write_permissions.

Resolution algorithm: given a list of file paths, match against project entries (glob patterns) and return 1..N `{slug, agent_path, write_permissions}` groups. When no project entry matches a path, fall back to the role's defaults entry.

The resolution helper is added to `momentum-tools.py` as `agent-resolve`, replacing the existing `specialist-classify` command's single-result logic.

`sprint-dev/workflow.md` Phase 2 (dev wave) is updated to call `agent-resolve` instead of the current manual specialist resolution (steps 2.3a–2.3d). Phase 5 (team review) agent paths are updated to read from the defaults block instead of hardcoded paths.

## Acceptance Criteria

**AC-1: `momentum/agents.json` exists with correct top-level structure**
Given the Momentum plugin is installed,
when the file `momentum/agents.json` is read,
then it contains exactly two top-level keys: `"defaults"` (object) and `"project"` (array).

**AC-2: `defaults` block contains all 9 universal roles**
Given `momentum/agents.json` is read,
when inspecting the `defaults` object,
then it contains keys for all nine roles: `architect`, `pm`, `ux`, `analyst`, `researcher`, `dev`, `sm`, `qa-reviewer`, `e2e-validator`,
and each value is the string path `"skills/momentum/agents/{role}.md"`.

**AC-3: `project` array is initially empty**
Given `momentum/agents.json` ships with the plugin (before any project runs `build-agents`),
when `project` is read,
then it is an empty array `[]` — agent-builder populates it per project.

**AC-4: each project entry has the required fields**
Given `agent-builder` has added a project entry,
when that entry is read from the `project` array,
then it contains: `role` (string matching a defaults key), `slug` (kebab-case string), `agent` (file path string), `patterns` (non-empty array of glob strings), `write_permissions` (array of glob strings, may be empty for read-only roles).

**AC-5: `momentum-tools agent-resolve` accepts file paths and returns 1..N results**
Given a comma-separated list of file paths is passed as `--touches`,
when `momentum-tools agent-resolve --touches "path1,path2"` is run,
then it exits 0 and prints JSON with a `results` array containing one object per distinct matching agent group, each object having fields: `slug`, `agent_path`, `write_permissions`, `file_scope` (the subset of input paths matched by this agent's patterns).

**AC-6: pattern matching uses glob semantics against project entries**
Given a project entry with `"patterns": ["**/src/**/ui/**", "**/*.kt"]`,
when `agent-resolve` receives paths including `src/main/kotlin/ui/Button.kt`,
then that path is matched by the project entry (not the defaults fallback).

**AC-7: unmatched paths fall back to the role defaults entry**
Given no project entry matches an input path,
when `agent-resolve` processes that path,
then the result includes the defaults entry for `dev` (slug `"dev"`, agent_path `"skills/momentum/agents/dev.md"`).

**AC-8: 1..N grouping — distinct matched agents each appear once**
Given input paths that match two different project entries (e.g., one `dev-ui` entry and one `dev-api` entry),
when `agent-resolve` processes them,
then the `results` array contains two objects (one per agent), each carrying only the paths matched by its patterns in `file_scope`.

**AC-9: `sprint-dev` Phase 2 resolves agents via `agent-resolve`**
Given `sprint-dev/workflow.md` is read,
when examining Phase 2 (dev wave) specialist resolution,
then steps 2.3a–2.3d (manual specialist file path construction) are replaced by a call to `momentum-tools agent-resolve --touches {story.touches}`, and the spawning loop iterates the returned `results` array to spawn one agent per group.

**AC-10: `sprint-dev` Phase 5 team review agent paths come from `defaults` block**
Given `sprint-dev/workflow.md` Phase 5 is read,
when examining the qa-reviewer and e2e-validator spawn instructions,
then the agent paths reference the `defaults` block lookup (`momentum/agents.json defaults.qa-reviewer` and `defaults.e2e-validator`) rather than hardcoded `skills/momentum/agents/qa-reviewer.md` strings.

**AC-11: write_permissions are surfaced per result entry**
Given a project entry with `"write_permissions": ["src/main/kotlin/**/ui/**"]`,
when `agent-resolve` matches that entry,
then the result object for that group includes `write_permissions: ["src/main/kotlin/**/ui/**"]`.
Read-only roles (qa-reviewer, e2e-validator, architect) have `write_permissions: []`.

**AC-12: agent-builder appends to `project` array without touching `defaults`**
Given `agent-builder` produces a new composed agent file,
when it writes the routing entry to `momentum/agents.json`,
then only the `project` array is modified — the `defaults` block is unchanged.

## Dev Notes

### Change-Type Classification

This story has two change types:

- **config-structure**: the creation of `momentum/agents.json` itself and the `agent-resolve` helper in `momentum-tools.py`. These are direct implementation artifacts — write the file, add the function.
- **skill-instruction**: the updates to `sprint-dev/workflow.md`. Workflow files are Momentum skill instructions — they tell Claude how to behave, not machine-executed code. Treat workflow edits as precise instruction rewrites with the same care as changing algorithm logic.

### `momentum/agents.json` — Full Schema with Example

The canonical initial file (defaults populated, project empty):

```json
{
  "defaults": {
    "architect": "skills/momentum/agents/architect.md",
    "pm": "skills/momentum/agents/pm.md",
    "ux": "skills/momentum/agents/ux.md",
    "analyst": "skills/momentum/agents/analyst.md",
    "researcher": "skills/momentum/agents/researcher.md",
    "dev": "skills/momentum/agents/dev.md",
    "sm": "skills/momentum/agents/sm.md",
    "qa-reviewer": "skills/momentum/agents/qa-reviewer.md",
    "e2e-validator": "skills/momentum/agents/e2e-validator.md"
  },
  "project": []
}
```

A project entry written by agent-builder looks like:

```json
{
  "role": "dev",
  "slug": "dev-cmp",
  "agent": ".claude/guidelines/agents/dev-cmp.md",
  "patterns": ["**/src/**/ui/**", "**/*.kt"],
  "write_permissions": ["src/main/kotlin/**/ui/**"]
}
```

Multiple project entries for the same role are valid — they represent different domains (e.g., `dev-ui` and `dev-api` both under role `dev`).

### Note on Defaults Body Files

The 9 paths in the `defaults` block reference agent body files. Status at sprint time:

- **Exist already**: `dev.md`, `qa-reviewer.md`, `e2e-validator.md` (and dev specialists `dev-build.md`, `dev-frontend.md`, `dev-skills.md`)
- **Being created this sprint**: `ux.md`, `analyst.md`, `researcher.md` (separate stories)
- **Exist as stubs or need creation**: `architect.md`, `pm.md`, `sm.md`

The `defaults` block in `momentum/agents.json` is written unconditionally with all 9 paths. Skills resolve the agent file at spawn time — if a body file is absent, the caller falls back (as today) or surfaces a warning. Do not gate the defaults block on whether body files exist.

### Resolution Algorithm — Pseudocode

```python
def agent_resolve(touches: list[str], agents_json: dict) -> list[dict]:
    """
    Returns a list of {slug, agent_path, write_permissions, file_scope} groups.
    """
    project_entries = agents_json.get("project", [])
    defaults = agents_json.get("defaults", {})

    # Track which paths have been claimed by a project entry
    claimed: dict[str, dict] = {}   # path -> project entry that claimed it
    unclaimed: list[str] = []

    for path in touches:
        matched = None
        for entry in project_entries:
            if any(fnmatch(path, pat) for pat in entry["patterns"]):
                matched = entry
                break   # first matching entry wins
        if matched:
            key = matched["slug"]
            if key not in claimed:
                claimed[key] = {"entry": matched, "file_scope": []}
            claimed[key]["file_scope"].append(path)
        else:
            unclaimed.append(path)

    results = []

    # Emit one result per matched project entry
    for slug, group in claimed.items():
        entry = group["entry"]
        results.append({
            "slug": slug,
            "agent_path": entry["agent"],
            "write_permissions": entry.get("write_permissions", []),
            "file_scope": group["file_scope"],
        })

    # Emit one result for unclaimed paths (defaults fallback)
    if unclaimed:
        results.append({
            "slug": "dev",
            "agent_path": defaults.get("dev", "skills/momentum/agents/dev.md"),
            "write_permissions": [],
            "file_scope": unclaimed,
        })

    # If touches was empty, return the base dev default
    if not results:
        results.append({
            "slug": "dev",
            "agent_path": defaults.get("dev", "skills/momentum/agents/dev.md"),
            "write_permissions": [],
            "file_scope": [],
        })

    return results
```

The CLI command signature:

```
momentum-tools agent-resolve --touches "path1,path2,path3"
```

Output (stdout, JSON):

```json
{
  "action": "agent_resolve",
  "success": true,
  "results": [
    {
      "slug": "dev-cmp",
      "agent_path": ".claude/guidelines/agents/dev-cmp.md",
      "write_permissions": ["src/main/kotlin/**/ui/**"],
      "file_scope": ["src/main/kotlin/ui/Button.kt"]
    },
    {
      "slug": "dev",
      "agent_path": "skills/momentum/agents/dev.md",
      "write_permissions": [],
      "file_scope": ["src/api/routes.py"]
    }
  ]
}
```

Follow the existing `result()` helper pattern used throughout `momentum-tools.py`.

### `momentum-tools.py` — Where to Add

Add `cmd_agent_resolve` adjacent to `cmd_specialist_classify` (line ~1694). Add the subcommand registration in `build_parser()` following the same pattern as `sprint specialist-classify`.

The new subcommand: `momentum-tools agent resolve --touches <csv>` (note: keep `specialist classify` in place — it is still referenced in sprint-planning; do not remove it in this story).

### `sprint-dev/workflow.md` — What to Change

**Phase 2, steps 2.3a–2.3d** currently reads:

```
3. Resolve specialist agent:
   a. Read {{team}}.story_assignments[slug].specialist (e.g., "dev-skills", "dev-build", "dev-frontend", or "dev")
   b. Resolve agent definition file: `skills/momentum/agents/{specialist}.md`
   c. If the specialist file exists, use it as the agent definition
   d. If the specialist file does NOT exist, log a warning and fall back to `skills/momentum/agents/dev.md`
```

Replace with:

```
3. Resolve agent(s) via routing table:
   a. Collect {{story_touches}} = the story's `touches` array
   b. Run: `momentum-tools agent resolve --touches "{{story_touches | join(',')}}"` 
   c. Parse the returned `results` array — each entry is {slug, agent_path, write_permissions, file_scope}
   d. If the routing table returns a single result: spawn one agent for this story (same as before)
   e. If the routing table returns multiple results (multi-domain story): spawn one agent per result,
      each scoped to its file_scope and carrying its write_permissions
   f. If agent_path does not exist on disk: log a warning and substitute `skills/momentum/agents/dev.md`
```

**Phase 5 (Team Review)** currently has hardcoded paths:

```
**QA Agent** — spawn via Agent tool with `skills/momentum/agents/qa-reviewer.md` definition
**E2E Validator** — spawn via Agent tool with `skills/momentum/agents/e2e-validator.md` definition
```

Update these to read from the routing table defaults block:

```
**QA Agent** — spawn via Agent tool; resolve agent path from routing table: `momentum-tools agent resolve --role qa-reviewer` (returns defaults.qa-reviewer path)
**E2E Validator** — spawn via Agent tool; resolve agent path from routing table: `momentum-tools agent resolve --role e2e-validator`
```

Add a `--role <role>` flag to `cmd_agent_resolve` that bypasses pattern matching and returns the defaults entry for the named role directly. This serves Phase 5's needs (role-based lookup without file paths).

### Project Structure Notes

- `momentum/agents.json` is a plugin-distributed file. It lives at the plugin root alongside `skills/`, not inside any skill subdirectory. When the plugin is installed, this file copies to the user's `~/.claude/plugins/momentum/` (or equivalent). Projects that run `build-agents` gain project entries written to a local `momentum/agents.json` in the project root.
- `momentum-tools.py` is at `skills/momentum/scripts/momentum-tools.py` — add `agent-resolve` as a top-level subcommand under a new `agent` subparser group, parallel to `sprint`, `session`, `story`.

### References

- DEC-023 — Agent Routing Table decision (primary)
- DEC-026 — Build Pipeline Redesign (agent-builder writes routing entries — D5)
- `skills/momentum/scripts/momentum-tools.py` — existing `cmd_specialist_classify` for pattern
- `skills/momentum/skills/sprint-dev/workflow.md` — Phase 2 and Phase 5 are the two callsites to update
- `skills/momentum/references/agent-skill-development-guide.md` — conventions for any agent file edits

## Tasks

- [ ] **Task 1 — Create `momentum/agents.json`**: Write the file with the full `defaults` block (all 9 roles) and an empty `project` array. Verify JSON is valid. This file is the sole config-structure deliverable.

- [ ] **Task 2 — Add `agent-resolve` to `momentum-tools.py`**: Implement `cmd_agent_resolve` following the pseudocode in Dev Notes. Add `--touches <csv>` and `--role <role>` flags. Register the subcommand under a new `agent` subparser group. Follow the `result()` helper pattern for stdout output. Do not remove `specialist-classify`.

- [ ] **Task 3 — Update `sprint-dev/workflow.md`**: Replace Phase 2 steps 2.3a–2.3d with the routing-table-driven resolution (see Dev Notes). Update Phase 5 QA Agent and E2E Validator spawn instructions to use `--role` lookup. Keep all other workflow steps unchanged.

- [ ] **Task 4 — Write 2 evals for routing behavior**: Create eval files in `skills/momentum/agents/evals/`:
  - `eval-agent-resolve-project-entry-match.md` — verifies that `agent-resolve` returns a project entry when a touches path matches a pattern, not the defaults fallback
  - `eval-agent-resolve-defaults-fallback.md` — verifies that `agent-resolve` returns the defaults `dev` entry when no project entry matches the input paths

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — implementation was direct from story spec and DEC-023.

### Completion Notes List

- `momentum/agents.json` created with all 9 defaults and empty project array
- `momentum-tools agent resolve` added as `agent` subcommand group with `resolve` subcommand; supports `--touches` (CSV paths) and `--role` (direct defaults lookup) flags
- `sprint-dev/workflow.md` Phase 2 steps 2.3a-2.3d replaced with routing-table-driven resolution (steps 0a-0f + updated steps 1-5)
- `sprint-dev/workflow.md` Phase 5 QA Agent and E2E Validator updated to use `--role` routing table lookup
- Phase 3 retry block updated to use routing table resolution
- `<team-composition>` comments updated to reflect routing-table model
- 2 evals created in `skills/momentum/agents/evals/`
- `specialist-classify` left in place — still referenced by sprint-planning

### File List

- `momentum/agents.json` — new
- `skills/momentum/scripts/momentum-tools.py` — modified (cmd_agent_resolve + build_parser agent group)
- `skills/momentum/skills/sprint-dev/workflow.md` — modified (Phase 2, Phase 3, Phase 5, team-composition)
- `skills/momentum/agents/evals/eval-agent-resolve-project-entry-match.md` — new
- `skills/momentum/agents/evals/eval-agent-resolve-defaults-fallback.md` — new
