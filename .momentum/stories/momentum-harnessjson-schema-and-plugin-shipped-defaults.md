---
title: momentum/verification-harness.json schema and plugin-shipped defaults
story_key: momentum-harnessjson-schema-and-plugin-shipped-defaults
status: ready-for-dev
epic_slug: bring-your-own-tools
feature_slug: momentum-protocol-based-integration
story_type: practice
depends_on: []
change_type: [config-structure, skill-instruction]
touches:
  - momentum/verification-harness.json
  - skills/momentum/skills/agent-builder/workflow.md
  - skills/momentum/skills/agent-guidelines/workflow.md
  - _bmad-output/planning-artifacts/architecture.md
---

# momentum/verification-harness.json schema and plugin-shipped defaults

## Story

As a developer using Momentum on any project,
I want a `momentum/verification-harness.json` file (plugin-shipped defaults, project-overridable) that declares how acceptance validation is driven,
so that the e2e-validator and sprint-planning contract authors can read project-specific tooling from config rather than hard-coding stack assumptions.

## Acceptance Criteria

1. A file `momentum/verification-harness.json` exists in the plugin root, structurally parallel to `momentum/agents.json`: a top-level JSON object with exactly two keys — `"defaults"` (object, plugin-shipped) and `"project"` (array, initially empty).

2. The `defaults` object contains the following top-level keys, each described below:
   - `"env"`: an object declaring how to start the project environment and how to verify it is ready, with at minimum keys `"startup"` (string command or null) and `"readiness_probe"` (string command or null). Both may be null for projects with no running environment.
   - `"execution_surfaces"`: an object keyed by change-type slug (`"skill-instruction"`, `"script-code"`, `"rule-hook"`, `"config-structure"`, `"specification"`) whose values declare which execution surface handles validation for that change type. Each value is a string surface name or the keyword `"skip"` (trivial-smoke escape hatch — see AC 5).
   - `"drivers"`: an object mapping driver names to their invocation strategy. Must include entries for `"cmux"`, `"skill"`, `"maestro"`, `"playwright"`, and `"curl"`. Each entry contains at minimum `"enabled"` (boolean) and `"description"` (string).
   - `"platform_targets"`: an array of platform/target objects. Each entry has `"platform"` (string, e.g., `"macos"`, `"android"`, `"ios"`, `"web"`) and `"enabled"` (boolean). The defaults block ships with all platforms enabled false (opt-in).
   - `"human_review_carveouts"`: an array of change-type slugs whose validation requires human review as the final gate regardless of automated results. The defaults block ships this as an empty array.
   - `"trivial_smoke_escape"`: an object with `"enabled"` (boolean, default false) and `"applies_to"` (array of change-type slugs). When enabled for a change type, the e2e-validator skips full automated validation for stories of that type and substitutes only a minimal smoke check.

3. The `"project"` key is an initially-empty array. Its entries (written by `agent-builder` and `agent-guidelines`) override or extend any field in `defaults` for specific project contexts. The schema for each project entry is not fully specified in this story — that is the consuming story's concern — but the array must be present and empty in the plugin-shipped file.

4. The plugin-shipped `defaults` block uses safe, broadly applicable values: `env.startup` and `env.readiness_probe` are both null; all `execution_surfaces` entries map to `"skip"` (the trivial-smoke escape hatch is project-specific; projects that need real validation must override in the `project` block); all drivers have `"enabled": false`; all platform targets have `"enabled": false`; `human_review_carveouts` is `[]`; `trivial_smoke_escape.enabled` is false.

5. The trivial-smoke escape hatch is a first-class schema element. When `execution_surfaces["<change-type>"]` is `"skip"`, the e2e-validator treats stories of that change type as needing only a trivial smoke check (e.g., "file exists and parses"). This is the plugin default — all validation is opt-in at the project level. Note: the sentinel value `"skip"` is a short key name for the trivial-smoke escape (per DEC-029 D3 "trivial-smoke escape hatch"); it does NOT mean validation is entirely bypassed — a minimal file-exists-and-parses check still runs.

6. The `agent-builder` workflow is updated so that when it writes a new agent's routing entry to `momentum/agents.json`, it also emits a corresponding harness `project` entry to `momentum/verification-harness.json`. The emitted entry need not be fully populated — it must at minimum set the `"role"` field matching the agent being built; all other fields may be omitted entirely (not set to null). The update is additive: existing entries in `momentum/verification-harness.json` are never deleted by agent-builder.

7. The `agent-guidelines` workflow is updated symmetrically: when it generates project-specific guidelines, it checks whether a harness entry exists for the relevant role and, if none exists, writes a stub entry. If an entry already exists, it leaves it unchanged.

8. The architecture document (`_bmad-output/planning-artifacts/architecture.md`) is updated to record: (a) `momentum/verification-harness.json` in the Plugin Root Layout table alongside `momentum/agents.json`, (b) the Read/Write Authority entry for `momentum/verification-harness.json` (sole writers: `agent-builder`, `agent-guidelines`; plugin ships defaults block), and (c) a Decision entry summarizing DEC-029 D3 schema choices.

9. The `momentum/verification-harness.json` file parses as valid JSON with no errors. All required keys described in AC 2 are present in the `defaults` block. The `project` array is present and empty.

10. No existing test, workflow, or configuration file outside `momentum/verification-harness.json`, `skills/momentum/skills/agent-builder/workflow.md`, `skills/momentum/skills/agent-guidelines/workflow.md`, and `_bmad-output/planning-artifacts/architecture.md` is modified by this story.

## Tasks / Subtasks

- [ ] **Task 1 — Create `momentum/verification-harness.json` with plugin-shipped defaults block** (`config-structure`)
  - Create `momentum/verification-harness.json` as a sibling to `momentum/agents.json`
  - Top-level structure: `{ "defaults": { ... }, "project": [] }`
  - Populate the `defaults` object with all required keys per AC 2 and AC 4:
    - `env.startup`: null, `env.readiness_probe`: null
    - `execution_surfaces`: all five change-type slugs mapped to `"skip"`
    - `drivers`: entries for cmux, skill, maestro, playwright, curl — all `enabled: false` with description strings
    - `platform_targets`: entries for macos, android, ios, web — all `enabled: false`
    - `human_review_carveouts`: `[]`
    - `trivial_smoke_escape`: `{ "enabled": false, "applies_to": [] }`
  - Validate with `jq . momentum/verification-harness.json` — must exit 0 and produce clean output

- [ ] **Task 2 — Update `agent-builder` workflow to write harness project entries** (`skill-instruction`)
  - Read the full `skills/momentum/skills/agent-builder/workflow.md` before editing
  - Locate the step that writes the routing entry to `momentum/agents.json`
  - Immediately after that write, add a step that reads `momentum/verification-harness.json`, checks whether a `project` entry with the matching `"role"` already exists, and if not, appends a stub: `{ "role": "{{role}}", "domain": "{{domain}}" }` to the `project` array
  - The append must be additive — existing entries are never removed
  - The step must document what it writes in the agent's output (same convention as the agents.json write step)
  - Write 2 behavioral evals in `skills/momentum/skills/agent-builder/evals/` (create dir if absent):
    - `eval-harness-stub-appended-on-new-role.md`
    - `eval-harness-unchanged-when-role-already-present.md`
  - Run evals, confirm behaviors match before marking done

- [ ] **Task 3 — Update `agent-guidelines` workflow to write harness project entries** (`skill-instruction`)
  - Read the full `skills/momentum/skills/agent-guidelines/workflow.md` before editing
  - Locate the step(s) that write project-specific outputs
  - Add a check: does `momentum/verification-harness.json` contain a `project` entry with the relevant `"role"`? If no entry exists, write a stub (same shape as Task 2). If entry exists, leave it unchanged
  - Write 2 behavioral evals in `skills/momentum/skills/agent-guidelines/evals/` (create dir if absent):
    - `eval-harness-stub-written-when-role-absent.md`
    - `eval-harness-unchanged-when-role-present.md`
  - Run evals, confirm behaviors match before marking done

- [ ] **Task 4 — Update architecture.md to document `momentum/verification-harness.json`** (`specification`)
  - Read `_bmad-output/planning-artifacts/architecture.md` before editing
  - In the Plugin Root Layout table, add a row for `momentum/verification-harness.json` directly below the `momentum/agents.json` row
  - In the Read/Write Authority table, add a row for `momentum/verification-harness.json`: description "Validation harness profile — `defaults` block (plugin-shipped) + `project` block (per-project overrides)"; sole writers: agent-builder, agent-guidelines; plugin ships defaults block
  - Add a new Decision entry in the Architecture Decisions section, sequentially after the last existing Decision entry (currently Decision 57 / DEC-028). Title it "Decision 58 (DEC-029 D3): verification-harness.json Validation Harness Profile". Content summary: momentum/verification-harness.json is a sibling to agents.json, uses the same defaults/project schema pattern, plugin ships safe defaults (all surfaces "skip"), project block written by agent-builder/agent-guidelines, consumed by e2e-validator and sprint-planning.
  - Verify all cross-references resolve: the agents.json row in both tables, the DEC-029 reference, the path `momentum/verification-harness.json`

## Dev Notes

### Architecture Compliance

This story creates a new config file that slots cleanly into the established `momentum/agents.json` pattern (Decision 55 / DEC-023). The schema mirrors the `defaults`/`project` split exactly:

- `momentum/agents.json` shape:
  ```json
  { "defaults": { "<role>": "<path>" }, "project": [] }
  ```
- `momentum/verification-harness.json` shape (this story):
  ```json
  { "defaults": { "<section>": { ... } }, "project": [] }
  ```

The `momentum/` directory currently contains only `agents.json`. This story adds `verification-harness.json` as its only sibling. No other files in that directory are touched.

**Write authority** (per architecture Read/Write Authority table): agent-builder is the sole authorized writer to `momentum/agents.json` project block; by extension (per DEC-029 D3), agent-builder and agent-guidelines are the co-writers of `momentum/verification-harness.json` project block. Plugin ships the defaults block. No other skill writes to either file.

**Gate status:** DEC-029 states that Phase 1 (which includes this story) is gated on `routing-table-schema-and-implementation` landing `momentum/agents.json`. That story is **done** (status: done in stories/index.json). Gate 1 is clear — this story may proceed.

**Driver key naming:** DEC-029 D3 uses the term "Skill-invoke" for the skill-invocation driver. In `momentum/verification-harness.json`, this driver is keyed as `"skill"` (a shorter canonical key name). These are the same driver; the key name `"skill"` is the authoritative verification-harness.json identifier.

### Testing Requirements

- **Task 1 (config-structure):** No unit tests. Verify with `jq . momentum/verification-harness.json` (must parse clean). Inspect all required fields manually per AC 9.
- **Tasks 2–3 (skill-instruction):** EDD — 2 behavioral evals each, per the Momentum Implementation Guide below.
- **Task 4 (specification):** No tests. Verify all cross-references resolve (linked rows in both tables, DEC-029 reference, path).

### Implementation Guide

**`momentum/verification-harness.json` draft structure** (write this exactly, then validate with jq):

```json
{
  "defaults": {
    "env": {
      "startup": null,
      "readiness_probe": null
    },
    "execution_surfaces": {
      "skill-instruction": "skip",
      "script-code": "skip",
      "rule-hook": "skip",
      "config-structure": "skip",
      "specification": "skip"
    },
    "drivers": {
      "cmux": { "enabled": false, "description": "cmux terminal multiplexer pane management" },
      "skill": { "enabled": false, "description": "Momentum skill invocation via Agent tool" },
      "maestro": { "enabled": false, "description": "Maestro mobile/web UI test runner" },
      "playwright": { "enabled": false, "description": "Playwright browser automation" },
      "curl": { "enabled": false, "description": "curl HTTP endpoint smoke check" }
    },
    "platform_targets": [
      { "platform": "macos", "enabled": false },
      { "platform": "android", "enabled": false },
      { "platform": "ios", "enabled": false },
      { "platform": "web", "enabled": false }
    ],
    "human_review_carveouts": [],
    "trivial_smoke_escape": {
      "enabled": false,
      "applies_to": []
    }
  },
  "project": []
}
```

**agent-builder write step (Task 2):** After the `momentum/agents.json` write step in agent-builder's workflow, add a step that:
1. Reads `momentum/verification-harness.json`
2. Checks `project` array for any entry with `"role": "{{role}}"`
3. If absent: appends `{ "role": "{{role}}", "domain": "{{domain}}" }` (no other fields) and saves
4. If present: logs "harness entry already exists for role {{role}} — no change" and continues

**agent-guidelines write step (Task 3):** Same pattern. The check happens at whatever step currently writes project-specific outputs for the relevant role. If no such step exists, add a dedicated "Update verification-harness.json project entry" step.

### Project Structure Notes

Files modified by this story:
- `momentum/verification-harness.json` — NEW (create)
- `skills/momentum/skills/agent-builder/workflow.md` — UPDATE (add harness write step)
- `skills/momentum/skills/agent-guidelines/workflow.md` — UPDATE (add harness check/write step)
- `_bmad-output/planning-artifacts/architecture.md` — UPDATE (add rows + decision entry)

Files created by this story:
- `skills/momentum/skills/agent-builder/evals/eval-harness-stub-appended-on-new-role.md` — NEW
- `skills/momentum/skills/agent-builder/evals/eval-harness-unchanged-when-role-already-present.md` — NEW
- `skills/momentum/skills/agent-guidelines/evals/eval-harness-stub-written-when-role-absent.md` — NEW
- `skills/momentum/skills/agent-guidelines/evals/eval-harness-unchanged-when-role-present.md` — NEW

**Preservation requirement:** Tasks 2–3 are additive updates to existing workflow files. Read the full file first. Never delete, reorder, or restructure existing steps — only add the new harness-write step in the correct location.

### References

- DEC-029 D3 (source decision): `_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md`
- DEC-023 (agents.json schema pattern, Decision 55 in architecture): `_bmad-output/planning-artifacts/architecture.md` — Decision 55
- `momentum/agents.json` (structural template): `momentum/agents.json`
- `skills/momentum/skills/agent-builder/workflow.md` (file to update, Task 2)
- `skills/momentum/skills/agent-guidelines/workflow.md` (file to update, Task 3)
- PRD FR34–FR38 (bring-your-own-tools capability): `_bmad-output/planning-artifacts/prd.md`

---

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1 → config-structure (direct implementation + jq validation)
- Tasks 2, 3 → skill-instruction (EDD — evals before writing, 2 evals each)
- Task 4 → specification (direct authoring + cross-reference verification)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. Write `momentum/verification-harness.json` per the draft structure in the Implementation Guide above
2. Verify by inspection:
   - JSON files: validate with `jq . momentum/verification-harness.json` — must exit 0
   - Required fields: all keys described in AC 2 must be present with correct types
   - Paths: `momentum/verification-harness.json` must exist alongside `momentum/agents.json`
   - The `"project"` key must be present and an empty array
3. Document what was created in the Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] `momentum/verification-harness.json` parses without error (`jq` exit 0)
- [ ] All required fields present with correct types (AC 2 checklist)
- [ ] `momentum/verification-harness.json` is a sibling to `momentum/agents.json`
- [ ] Changes documented in Dev Agent Record

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the workflow edit (Tasks 2 and 3 each):**
1. Write 2 behavioral evals in `skills/momentum/skills/agent-builder/evals/` and `skills/momentum/skills/agent-guidelines/evals/` respectively (create `evals/` if it doesn't exist):
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Edit the workflow.md file with the harness write step

**Then verify:**
3. For each eval file, spawn a subagent with the eval scenario and the workflow.md as context. Observe whether the behavior matches.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely (workflow.md edits do not affect SKILL.md description, but confirm it is unchanged)
- `model:` and `effort:` frontmatter fields must remain present (do not modify)
- workflow.md body must stay under 500 lines / 5000 tokens; if the edit pushes it over, move overflow content to `references/` (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12 — no change needed here, just confirm no regressions)

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/agent-builder/evals/` (Task 2)
- [ ] 2+ behavioral evals written in `skills/momentum/skills/agent-guidelines/evals/` (Task 3)
- [ ] EDD cycle ran for Tasks 2 and 3 — all eval behaviors confirmed (or failures documented)
- [ ] Existing workflow steps preserved (no deletions or reorders)
- [ ] workflow.md body ≤500 lines / 5000 tokens (check after edit)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source. Write directly and verify by inspection:

1. Update `_bmad-output/planning-artifacts/architecture.md` per Task 4 ACs
2. Verify cross-references: `momentum/verification-harness.json` path, `momentum/agents.json` row in both tables, DEC-029 decision reference, all section links
3. Verify format compliance: match the existing table and Decision entry format in architecture.md exactly
4. Document what was written in the Dev Agent Record

**Additional DoD items for specification tasks:**
- [ ] All cross-references to agents.json row, DEC-029, and `momentum/verification-harness.json` path resolve correctly
- [ ] New rows follow existing table format (column order, markdown syntax)
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

---

### Sprint Gherkin Specs Notice

Gherkin `.feature` files for this sprint will be authored by `sprint-planning` in `.momentum/sprints/{sprint-slug}/specs/`. Those files are the frozen, anti-gaming spec of done (DEC-029 D2/D6). The dev agent **must not read or reference `.feature` files** when implementing. Implement against the plain English ACs in this story file only. This is Decision 30 black-box separation — the dev agent never sees the validation contract it is being tested against.

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
