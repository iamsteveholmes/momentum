---
title: Feature Artifact Schema — Define features.json and Populate Initial Instances
story_key: feature-artifact-schema
status: review
epic_slug: feature-orientation
depends_on: []
touches:
  - _bmad-output/planning-artifacts/features.json
change_type: config-structure
priority: critical
derives_from:
  - path: _bmad-output/planning-artifacts/decisions/dec-002-feature-visualization-and-orientation-2026-04-11.md
    relationship: derives_from
    section: "D1: Introduce the Feature Artifact"
---

# Feature Artifact Schema — Define features.json and Populate Initial Instances

## Story

As a developer using Momentum,
I want a `features.json` artifact with a defined schema and populated initial
instances for both Nornspun and Momentum,
so that I can track user-observable capabilities as persistent, finite units with
acceptance conditions, status, and story links — giving me a clear view of what
is working and what sprint work is required to advance each feature.

## Description

Stories and epics complete, but no user-facing capabilities complete. The feature
artifact is the missing layer between PRD functional requirements and stories. A
Feature is a finite, user-observable capability with a finite set of duties and a
clear working/not-working acceptance condition. Granularity does not determine what
counts as a feature — end-to-end flows are features.

Features and epics are orthogonal: epics group by theme, features group by
user-observable capability. The `features.json` file uses the same keyed-object
pattern as `stories/index.json` — each entry keyed by `feature_slug`.

The two projects needing initial instances are:
- **Nornspun** — a product project requiring 3–5 representative features that cover
  the feature type taxonomy (flow, connection, quality)
- **Momentum** — a practice project whose features map to skill capabilities and
  SDLC coverage areas

Source decision: DEC-002 D1 at
`_bmad-output/planning-artifacts/decisions/dec-002-feature-visualization-and-orientation-2026-04-11.md`

## Acceptance Criteria

### AC1: features.json Schema Is Defined

- A `features.json` file exists at `_bmad-output/planning-artifacts/features.json`
- The file is an object keyed by `feature_slug` (same pattern as `stories/index.json`)
- Each feature entry contains all required fields from the DEC-002 D1 schema:
  `feature_slug`, `name`, `type`, `description`, `acceptance_condition`, `status`,
  `prd_section`, `stories`, `stories_done`, `stories_remaining`, `last_verified`,
  `notes`
- `type` is one of: `flow`, `connection`, `quality`
- `status` is one of: `working`, `partial`, `not-working`, `not-started`
- `stories` is an array of story slugs (may be empty)
- `stories_done` and `stories_remaining` are integers
- `last_verified` is an ISO date string or null
- `notes` is a string or null
- The file parses as valid JSON

### AC2: Nornspun Initial Instances Populated (3–5 features)

- The `features.json` contains 3–5 representative feature instances for the Nornspun
  project, covering at least two of the three feature types (flow, connection, quality)
- Each Nornspun feature has a meaningful `acceptance_condition` — a concrete,
  working/not-working statement a user could evaluate (not a vague description)
- Each Nornspun feature has a `prd_section` reference pointing to the relevant
  Nornspun PRD section (or `null` if not yet linked)
- Status reflects current known state — use `not-started` if unknown

### AC3: Momentum Initial Instances Populated (3–5 features)

- The `features.json` contains 3–5 representative feature instances for the Momentum
  project, covering skill capabilities and SDLC coverage areas
- Momentum features map to skill-level capabilities (e.g., "Sprint planning produces
  a ready sprint from backlog stubs") or practice coverage areas (e.g., "Assessment
  → Decision → Story pipeline is end-to-end automated")
- Each Momentum feature has a meaningful `acceptance_condition`
- Story slugs in the `stories` array resolve to entries in `stories/index.json`
- `stories_done` and `stories_remaining` reflect the count of done vs. non-done stories
  in the `stories` array

### AC4: Feature Type Taxonomy Is Respected

- At least one `flow` feature exists across Nornspun and Momentum instances
  (an end-to-end user journey)
- At least one `connection` feature exists (an integration, handoff, or linkage
  between two subsystems or tools)
- At least one `quality` feature exists (a non-functional requirement observable by users)

### AC5: File Is Valid and Committed

- `_bmad-output/planning-artifacts/features.json` parses as valid JSON (validated with
  a tool such as `jq` or `python3 -m json.tool`)
- The file is committed to the repository

## Tasks / Subtasks

- [x] Task 1 — Define schema structure and write empty features.json (AC: 1)
  - [x] Create `_bmad-output/planning-artifacts/features.json` with keyed-object shape
  - [x] Confirm all required fields are present in schema documentation/comments
    (use a README-style schema comment block at the top if JSON5 not available;
    otherwise document schema in Dev Agent Record)
  - [x] Validate the file parses as valid JSON

- [x] Task 2 — Research Nornspun features and populate initial instances (AC: 2, 4)
  - [x] Read Nornspun PRD or known artifacts to identify 3–5 representative features
  - [x] Ensure coverage of at least two feature types (flow, connection, quality)
  - [x] Write concrete, working/not-working `acceptance_condition` for each
  - [x] Set `prd_section` references where available
  - [x] Set `status` to reflect current known state

- [x] Task 3 — Research Momentum features and populate initial instances (AC: 3, 4)
  - [x] Map Momentum skill capabilities and SDLC coverage areas to 3–5 features
  - [x] For each, look up relevant story slugs in `stories/index.json`
  - [x] Count `stories_done` (status: done) and `stories_remaining` (non-done)
  - [x] Write concrete `acceptance_condition` for each

- [x] Task 4 — Validate JSON and commit (AC: 5)
  - [x] Run `jq . _bmad-output/planning-artifacts/features.json` or equivalent to
    confirm valid JSON
  - [x] Confirm all required fields are present in every entry
  - [x] Commit the file

## Dev Notes

### Schema Reference

The minimal schema from DEC-002 D1:

```json
{
  "feature_slug": {
    "feature_slug": "string",
    "name": "string",
    "type": "flow | connection | quality",
    "description": "string",
    "acceptance_condition": "string — concrete working/not-working statement",
    "status": "working | partial | not-working | not-started",
    "prd_section": "string | null",
    "stories": ["story-slug-1", "story-slug-2"],
    "stories_done": 0,
    "stories_remaining": 0,
    "last_verified": "YYYY-MM-DD | null",
    "notes": "string | null"
  }
}
```

### Feature Type Definitions (DEC-002 D1)

| Type | Definition |
|---|---|
| `flow` | End-to-end user journey — a sequence of actions a user takes to accomplish a goal |
| `connection` | Integration or handoff between two subsystems, tools, or agents |
| `quality` | Non-functional requirement observable by users (speed, reliability, clarity) |

### Nornspun Feature Guidance

Nornspun is a product project. Features should be user-observable product capabilities.
Read available Nornspun planning artifacts (PRD, epics) to identify candidates. Good
candidates for each type:
- `flow`: user onboarding, content creation E2E, community post lifecycle
- `connection`: auth provider handoff, storage integration, notification pipeline
- `quality`: page load responsiveness, error message clarity, search relevance

### Momentum Feature Guidance

Momentum is a practice project. Features map to:
- **Skill capabilities** — e.g., "momentum:sprint-planning produces a ready sprint plan
  from backlog stubs with AVFL-validated stories"
- **SDLC coverage areas** — e.g., "Assessment → Decision → Story pipeline produces
  traceable planning artifacts in a single session"
- **Practice continuity** — e.g., "Impetus orients developer at session start with
  current sprint state and feature gaps"

For `stories` references: look up story slugs in
`_bmad-output/implementation-artifacts/stories/index.json`. Count
`stories_done` = stories with `status: "done"` in the array; `stories_remaining` = all others.

### File Location

`_bmad-output/planning-artifacts/features.json` — same directory as `epics.md`, `prd.md`,
and the `decisions/` subdirectory.

### Relationship to Downstream Stories

This story is a dependency for `feature-status-skill` — that skill reads `features.json`.
The schema defined here is the contract that the `momentum:feature-status` skill will
consume. Keep it minimal and machine-readable.

### JSON Format Convention

Use the same pattern as `stories/index.json`: a single top-level object with feature
slugs as keys, no arrays at the root level.

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → config-structure (direct implementation)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by
inspection:

1. **Write the config or create the directory structure** per the story's acceptance
   criteria
2. **Verify by inspection:**
   - JSON files: must parse without error (validate with a JSON linter, `jq`, or
     IDE — do not rely on manual visual inspection)
   - Required fields: each required field must be present with the correct type
   - Paths: all referenced paths must exist after creation
   - Version consistency: any version fields must be consistent with related version
     references
3. **Document** what was created in the Dev Agent Record

**No tests required** for pure config/structure changes.

**DoD items for config-structure tasks:**
- [ ] All JSON files parse without error (validated with a tool)
- [ ] All required fields present with correct types
- [ ] All referenced paths exist after creation
- [ ] Changes documented in Dev Agent Record

---

**Gherkin specs:** Gherkin `.feature` files exist for this sprint in
`sprints/{sprint-slug}/specs/`. These are off-limits to the dev agent — implement
against the plain English ACs in this story file only. Do not read or reference
`.feature` files during implementation (Decision 30 black-box separation).

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — direct config-structure implementation, no debug issues.

### Completion Notes List

- Created `_bmad-output/planning-artifacts/features.json` with 10 entries: 5 Nornspun and 5 Momentum features.
- Schema validated with `jq` — all 10 entries pass. All 12 required fields present in every entry. All `type` and `status` enum values valid.
- Feature type taxonomy satisfied: 4 flow, 4 connection, 2 quality features across both projects.
- Nornspun features (5): session-prep-loop (flow), post-session-capture (flow), living-memory-cross-agent (connection), document-ingestion-pipeline (connection), streaming-responsiveness (quality). All 5 use `not-started` status (no Nornspun stories in Momentum's story index). PRD section references point to FR numbers.
- Momentum features (5): sprint-planning-to-ready (flow, working), assessment-decision-story-pipeline (flow, partial), impetus-session-orientation (connection, partial), quality-gates-enforced (connection, partial), feature-status-visibility (quality, not-started). All Momentum story slugs validated against stories/index.json — all resolve.
- `stories_done` and `stories_remaining` computed by checking status of each story slug in stories/index.json. `feature-status-visibility` has stories_done=0, stories_remaining=4 since all 4 stories (including this one) are in-progress or ready-for-dev.
- Schema documented: field definitions and type/status enums are described in the story's Dev Notes section (schema reference block). The JSON file itself follows the same keyed-object pattern as stories/index.json.

### File List

- `_bmad-output/planning-artifacts/features.json` (created)
