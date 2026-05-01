---
title: Triage Skill — Multi-Item Batch Classification and Routing
story_key: triage-skill
status: backlog
epic_slug: impetus-epic-orchestrator
feature_slug: momentum-backlog-refinement
story_type: practice
priority: medium
depends_on: []
touches:
  - skills/momentum/skills/triage/SKILL.md
  - skills/momentum/skills/triage/workflow.md
  - skills/momentum/skills/triage/evals/
  - skills/momentum/skills/intake/references/stub-template.md
  - skills/momentum/skills/intake/workflow.md
  - skills/momentum/skills/impetus/workflow.md
  - skills/momentum/skills/impetus/SKILL.md
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/references/model-routing-guide.md
  - _bmad-output/implementation-artifacts/intake-queue.jsonl
change_type: skill-instruction + script-code + specification
derives_from:
  - path: _bmad-output/planning-artifacts/decisions/dec-005-cycle-redesign-feature-first-practice-2026-04-14.md
    relationship: implements
    section: "D1 (feature_slug), D2 (DDD epics), D5 (story_type), D6 (terminal states), D10 (no gap-check in triage)"
  - path: _bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md
    relationship: implements
    section: "D1 — unified intake-queue.jsonl with source/kind discriminators"
  - path: _bmad-output/planning-artifacts/features.json
    relationship: belongs_to
    section: "momentum-backlog-refinement"
---

# Triage Skill — Multi-Item Batch Classification and Routing

## Story

As a developer using Momentum,
I want a `momentum:triage` skill that processes multiple observations at once and routes each to the correct downstream (story stub, practice distillation, decision document, or durable-watch queue),
so that I can clear a session's backlog of half-formed ideas in one pass — without either losing them or prematurely committing each to a full story.

## Description

The `[3] Triage` menu item in Impetus has always been a placeholder (`impetus/workflow.md:403` outputs "Triage is coming in the next phase."). Two prior story stubs existed for this work — `triage-skill` (a 4-line dead stub) and `retro-triage-handoff` (a pre-DEC-005 stub) — and both were invalidated by **DEC-005 (2026-04-14)**, which reshaped the feature/epic/story model and excluded gap-check from triage (D10).

**The structural gap this story fills:** `momentum:intake` is single-item by design (one idea → one stub, no batching), but real-world triage is inherently multi-item. A retro produces N findings. A conversation surfaces M observations. An assessment yields K recommendations. None of this fits intake's one-at-a-time contract, so today those items either get force-fit into intake (creating premature story stubs), are verbally discussed and lost, or are force-fit into the developer's working memory.

`momentum:triage` is the missing **orchestrator** that sits between upstream sources (conversation, retro Priority Action Items, assessment recommendations) and the per-item executors (`momentum:intake`, `momentum:distill`, `momentum:decision`). It:

1. **Enumerates** observations as a numbered list.
2. **Classifies** each into one of six classes: ARTIFACT / DISTILL / DECISION / SHAPING / DEFER / REJECT.
3. **Enriches** ARTIFACT items with `feature_slug` (DEC-005 D1), `story_type` (D5), suggested epic (D2 — DDD sub-domain aware), priority, and proposed dependencies.
4. **Batch-approves** with the developer using the same UX pattern as `momentum:refine` Step 9 (consolidated findings list; accept/modify/reject per item; batch operations when N ≥ 5).
5. **Executes** approved actions by delegating — spawns `momentum:intake` per ARTIFACT, `momentum:distill` per DISTILL, `momentum:decision` per DECISION. Writes `intake-queue.jsonl` inline via `momentum-tools` CLI for SHAPING / DEFER / REJECT (per DEC-007).
6. **Reports** a summary of what was stubbed, distilled, flagged, deferred, or rejected.

### Classification taxonomy (six classes)

| Class     | Meaning                                                        | Capture target                                             | Executor                           |
|-----------|----------------------------------------------------------------|------------------------------------------------------------|------------------------------------|
| ARTIFACT  | Worth a story stub now                                         | `stories/{slug}.md` + `stories/index.json` entry            | delegates to `momentum:intake`     |
| DISTILL   | Practice improvement — apply now                               | target practice file (rule / skill / reference)             | delegates to `momentum:distill`    |
| DECISION  | Needs a written decision                                       | `planning-artifacts/decisions/dec-NNN-*.md`                 | delegates to `momentum:decision`   |
| SHAPING   | Needs more thinking — capture without committing to a story    | `intake-queue.jsonl` event with `kind: "shape"`             | triage writes inline via CLI       |
| DEFER     | Watch; revisit later                                           | `intake-queue.jsonl` event with `kind: "watch"`             | triage writes inline via CLI       |
| REJECT    | Not doing this                                                 | `intake-queue.jsonl` event with `kind: "rejected"` + reason | triage writes inline via CLI       |

### DEC-005 alignment
- **D10** — triage performs NO value-floor gap-check. Classification only. (Gap-check lives at refinement, sprint-planning, and retro.)
- **D1** — `feature_slug` mandatory on ARTIFACT items.
- **D2** — epic boundary awareness follows DDD sub-domain model.
- **D5** — `story_type` (feature / maintenance / defect / exploration / practice) assigned per ARTIFACT, default `feature`.
- **D6** — terminal-state-aware for re-surface routing (items whose underlying feature is Abandoned or Rejected are auto-suggested for REJECT).

### DEC-007 alignment

SHAPING / DEFER / REJECT outcomes, plus retro→triage handoff items (Story B), land in a single unified `_bmad-output/implementation-artifacts/intake-queue.jsonl` event log. Schema uses `source` and `kind` discriminators so any future upstream (assessment, distill residue, conversation capture) can write the same artifact without schema branching.

### Agent topology

Triage is an **orchestrator** skill that runs inline in the main context (no subagent spawn for the classification judgment itself — it is context-dependent and cheap). Impetus is the entry-point orchestrator that dispatches to triage. Executor skills (`intake`, `distill`, `decision`) retain their existing model and effort settings.

Optional Explore subagents may be spawned for **enrichment** (duplicate detection against `stories/index.json`; feature-assignment suggestion against `features.json`) when observation count ≥ 5 or the developer explicitly requests deeper enrichment. For typical 2–3 observation sessions, triage does everything inline.

Elevated effort (`high`) is justified because triage outputs are unvalidated downstream — the developer batch-approves but there is no AVFL on the delegated intake/distill/decision calls within the triage flow. Matches the pattern used for `momentum:refine` and `momentum:sprint-planning`.

### Impetus integration

Replaces the Impetus `[3] Triage` menu placeholder (`skills/momentum/skills/impetus/workflow.md:403` and `skills/momentum/skills/impetus/SKILL.md:63`) with a real dispatch to `momentum:triage`. The greeting-state menus already reference "Triage" across multiple session states — their wording does not need to change, only the dispatch handler does. Impetus eval files that reference the menu item (`eval-feature-status-fresh-greeting.md`, `eval-2item-menu-returning-user-no-threads.md`) do not require updates for this story.

### Intake feature-awareness prerequisite (folded into this story)

Before triage can delegate correctly, `momentum:intake` must be extended to capture `feature_slug` (DEC-005 D1) and `story_type` (D5). The prerequisite scope is included in Story A rather than split out because:
- intake is the sole ARTIFACT executor triage calls — it must carry both fields before triage can produce dev-ready stubs;
- the `momentum-tools sprint story-add` CLI must persist both fields in `stories/index.json` entries;
- `intake/references/stub-template.md` must include both fields in frontmatter.

### Pain context

Today, observations captured mid-session either (a) go through intake one at a time (high friction for multi-item triage), (b) are verbally discussed and lost, or (c) are force-fit into the developer's working memory. The retro skill already generates multi-finding Priority Action Items that need downstream classification — currently that is also manual. Triage centralizes the pattern.

## Acceptance Criteria

_Plain English — no Gherkin in this file. Gherkin-style specs live in `sprints/{sprint-slug}/specs/` per Decision 30 black-box separation, and are authored by sprint-planning, not by create-story. The dev agent implements against the plain English ACs below only._

### AC1: Triage skill package exists with correct frontmatter

1. A skill directory exists at `skills/momentum/skills/triage/` containing at minimum `SKILL.md` and `workflow.md`.
2. `SKILL.md` frontmatter includes `name`, `description`, `model: claude-sonnet-4-6`, `effort: high`.
3. `SKILL.md` `description` is ≤150 characters (NFR1).
4. `SKILL.md` body is ≤500 lines / 5000 tokens (NFR3); overflow content lives in `references/` with clear load instructions.
5. Skill uses the `momentum:` namespace (NFR12 — no collision with BMAD skills).
6. `SKILL.md` body delegates to `./workflow.md` in the established Momentum pattern.

### AC2: Triage is independently invocable and dispatched from Impetus

1. The skill is invocable via `/momentum:triage` from any session.
2. The Impetus workflow is updated to dispatch to `momentum:triage` when the developer selects the `[3] Triage` menu option. The placeholder output ("Triage is coming in the next phase.") is removed from both `skills/momentum/skills/impetus/workflow.md` and `skills/momentum/skills/impetus/SKILL.md`.
3. Triage can also be invoked with an explicit list of observations passed as arguments (e.g., by retro Phase 5 or sprint-planning backlog synthesis calling it programmatically).

### AC3: Observation enumeration

1. On invocation, triage presents a numbered list of observations to classify.
2. Observation sources supported: (a) explicit list passed as arguments; (b) the developer typing observations interactively into the session; (c) extracted from recent conversation context if the developer invokes without explicit input.
3. Pending items from `intake-queue.jsonl` — open events with `kind: shape` or `kind: watch` — are re-surfaced alongside new observations. Each pending item is visibly tagged with its age and original classification.

### AC4: Six-class classification

1. Each enumerated observation is classified into exactly one of: `ARTIFACT`, `DISTILL`, `DECISION`, `SHAPING`, `DEFER`, `REJECT`.
2. Classification is inline in the orchestrator's main context — no subagent spawn for the judgment step.
3. The classification output for each observation includes: class, one-sentence rationale, and (for ARTIFACT items) the enrichment fields described in AC5.

### AC5: ARTIFACT enrichment

For every observation classified as ARTIFACT, triage captures before approval:
1. `feature_slug` — suggested from `_bmad-output/planning-artifacts/features.json` by matching the observation against feature names and descriptions. Developer may override.
2. `story_type` — one of `feature`, `maintenance`, `defect`, `exploration`, `practice`. Default `feature`. Heuristic suggestion based on observation content (e.g., "fix the X bug" → `defect`; "upgrade Y library" → `maintenance`; "distill this pattern" → `practice`).
3. `epic_slug` — suggested epic using DDD sub-domain awareness (per DEC-005 D2). Developer may override.
4. `priority` — suggested from observation urgency cues; developer may override. Valid values: `critical`, `high`, `medium`, `low`.
5. `depends_on` — proposed dependencies on existing story slugs if any are detectable from observation content.

### AC6: Batch-approval UX matches refine Step 9

1. After classification and enrichment, triage presents a single consolidated findings list for developer review — not one-by-one prompts during classification.
2. When total items < 5: each finding is presented individually with `A` (approve) / `M` (approve with modifications) / `R` (reject) options, following the pattern in `skills/momentum/skills/refine/workflow.md` Step 9 (content `< 5`).
3. When total items ≥ 5: findings are presented grouped by class with batch operations first ("Approve all ARTIFACT?" / "Reject all DEFER?"), followed by individual override support ("override 3, 7-9") — matching refine Step 9 (content `≥ 5`).
4. `M` (modify) prompts the developer to adjust specific fields (class, feature_slug, story_type, priority, epic, dependencies) before approval.
5. No mutations happen before the full batch approval is complete.

### AC7: Delegation semantics — no direct story writes

1. For each approved ARTIFACT: triage invokes `momentum:intake` as a subagent, passing the enriched context (title, description, feature_slug, story_type, epic_slug, priority, depends_on). Triage does NOT write `stories/*.md` files or `stories/index.json` entries directly for ARTIFACT items.
2. For each approved DISTILL: triage invokes `momentum:distill`, passing the observation text as `learning_description` and the target practice file as `candidate_artifact` (matching the pattern in `retro/workflow.md` Phase 5 Tier 1 routing).
3. For each approved DECISION: triage invokes `momentum:decision`, passing the decision context.
4. Triage writes files directly ONLY for SHAPING / DEFER / REJECT outcomes, and ONLY to `intake-queue.jsonl` via the CLI (AC8).
5. The orchestrator-purity constraint is encoded as a `<critical>` block at the top of `workflow.md`: "Never use Write or Edit on story files, stories/index.json, decision documents, or practice artifacts. Only intake-queue.jsonl is written directly, and only via the momentum-tools CLI."

### AC8: intake-queue.jsonl writes for SHAPING / DEFER / REJECT

1. A new `momentum-tools` CLI subcommand is available: `triage-queue append` — appends a single event to `_bmad-output/implementation-artifacts/intake-queue.jsonl`. File is created if it does not exist.
2. Event schema. Core discriminators per DEC-007: `source`, `kind`. Remaining fields defined by this story:
   - `source` — one of `triage`, `retro`, `assessment` (extensible for future upstreams)
   - `kind` — one of `shape`, `watch`, `rejected`, `handoff`
   - `id` — unique event id (ULID or timestamped slug)
   - `title` — short human-readable title for the observation
   - `description` — one-to-three-sentence summary of the observation
   - `rationale` — the developer-approved rationale (why shape / why defer / why reject)
   - `status` — one of `open` | `consumed` | `rejected` (initial write is always `open`; this is the primary open/closed discriminator)
   - `created_at` — ISO-8601 timestamp
   - `feature_slug` — optional, when known
   - `story_slug` — optional, when known
   - `resolved_at` — optional; recorded alongside status transitions (`consumed` or `rejected`) for provenance, but `status` is the canonical discriminator for whether an item is open or closed
3. The CLI validates `source` and `kind` against the allowed enums and returns a structured JSON result matching the pattern of existing `momentum-tools` commands.
4. A companion `momentum-tools triage-queue list` subcommand reads `intake-queue.jsonl` and returns open events (events with `status: "open"`). Supports optional `--kind` and `--source` filters.
5. A third subcommand `momentum-tools triage-queue update` mutates the status of an existing event. It accepts: an event id (required), `--status` (`consumed` or `rejected`), optional `--resolved-at` (ISO-8601 timestamp, defaults to now), and optional `--outcome-ref` (e.g., story slug or decision document id for provenance). Story B (`retro-triage-handoff`) depends on this subcommand for marking handoff items consumed or rejected after downstream action.
6. Triage writes one event per approved SHAPING/DEFER/REJECT item, with `source: "triage"` and `kind` mapped from class: SHAPING → `shape`, DEFER → `watch`, REJECT → `rejected`. Initial `status` is always `open`.

### AC9: Pending-item re-surfacing and re-classification

1. At the start of each triage invocation, the skill calls `momentum-tools triage-queue list` to load open events (those with `status: "open"`) and displays them alongside any new observations.
2. For each pending item, the developer may: promote to ARTIFACT (delegates to intake), continue watching (no change), reject (calls `triage-queue update --status rejected` with an optional outcome reference), or mark resolved (calls `triage-queue update --status consumed` with an optional outcome reference).
3. All status-mutation operations go through `triage-queue update` CLI — triage does not edit `intake-queue.jsonl` with Write or Edit tools.

### AC10: Intake feature-awareness prerequisite — stub template

1. `skills/momentum/skills/intake/references/stub-template.md` frontmatter includes `feature_slug` and `story_type` fields immediately after `epic_slug`.
2. Both fields are substituted from intake's workflow variables (AC11).

### AC11: Intake feature-awareness prerequisite — workflow capture

1. `skills/momentum/skills/intake/workflow.md` Step 1 (context extraction) captures `{{feature_slug}}` and `{{story_type}}` in addition to existing fields.
2. When a `feature_slug` is not explicitly provided by the user or caller, intake reads `features.json`, suggests the best-match feature, and confirms with the user before proceeding. The suggestion flow mirrors the epic-assignment flow already in Step 2.
3. When `story_type` is not explicitly provided, intake defaults to `feature` and applies a light heuristic suggestion (e.g., "fix" / "broken" → `defect`; "upgrade" / "bump" → `maintenance`; "distill" / "rule" / "practice" → `practice`; "spike" / "research" / "explore" → `exploration`).
4. Both fields are passed through to the CLI `story-add` call (AC12) and substituted into the stub template (AC10).

### AC12: Intake feature-awareness prerequisite — CLI flags

1. `momentum-tools.py` `sprint story-add` subcommand accepts two new optional flags: `--feature-slug` and `--story-type`.
2. Default when not provided: `feature_slug` is `null`; `story_type` is `"feature"`.
3. `--story-type` is validated against the allowed enum: `feature`, `maintenance`, `defect`, `exploration`, `practice`. Invalid values produce a clear error and non-zero exit.
4. When provided, both fields are persisted in the resulting `stories/index.json` entry. Existing entries without these fields remain valid (treat missing as default).
5. The existing test suite (`skills/momentum/scripts/test-momentum-tools.py`) is extended with at least one test each for: feature_slug persistence, story_type persistence, invalid story_type rejection.

### AC13: Model-routing guide updated

1. `skills/momentum/references/model-routing-guide.md` gains a new table row for `momentum:triage` with model `claude-sonnet-4-6` and effort `high`, with a rationale entry matching the pattern of existing rows (e.g., "Orchestrator batch-classification — unvalidated downstream, elevated effort matches refine/sprint-planning").
2. The rationale entry cites DEC-005 alignment implicitly by listing the 6-class taxonomy scope.

### AC14: EDD — behavioral evals exist and are referenced

1. At least 3 behavioral evals exist under `skills/momentum/skills/triage/evals/`:
   - Eval A: correct taxonomy assignment (given a mixed set of observations, the skill produces the expected class for each).
   - Eval B: batch-approval fidelity (given 6+ observations, the skill presents grouped batch operations and honors developer overrides).
   - Eval C: delegation vs direct-write boundary (the skill delegates ARTIFACT/DISTILL/DECISION and writes only intake-queue.jsonl events directly).
2. Each eval file follows the format "Given [input and context], the skill should [observable behavior]" — testing decisions, not exact text.
3. The EDD cycle is run before merge: all evals confirmed passing, or failures documented in the Dev Agent Record with explanation.

## Tasks / Subtasks

- [ ] Task 1: Write behavioral evals for the triage skill (AC: 14)
  - [ ] 1.1: Create `skills/momentum/skills/triage/evals/` directory
  - [ ] 1.2: Write `eval-taxonomy-classification.md` — verify correct six-class assignment on a mixed observation set
  - [ ] 1.3: Write `eval-batch-approval-fidelity.md` — verify grouped batch UX when N≥5 and individual UX when N<5
  - [ ] 1.4: Write `eval-delegation-boundary.md` — verify ARTIFACT/DISTILL/DECISION are delegated, only intake-queue.jsonl written directly

- [ ] Task 2: Create the triage skill package (AC: 1, 2, 3, 4, 5, 6, 7, 9)
  - [ ] 2.1: Write `skills/momentum/skills/triage/SKILL.md` with frontmatter (name, description ≤150 chars, `model: claude-sonnet-4-6`, `effort: high`) and body delegating to `./workflow.md`
  - [ ] 2.2: Write `skills/momentum/skills/triage/workflow.md` implementing: initialization, observation enumeration (Step 1), pending-item re-surface via CLI list (Step 2), classification inline (Step 3), enrichment per ARTIFACT (Step 4), batch-approval UX matching refine Step 9 (Step 5), execute-per-class delegation and CLI queue writes (Step 6), summary report (Step 7)
  - [ ] 2.3: Include `<critical>` constraint at top: triage never uses Write/Edit on story files, index.json, decision docs, or practice files; only intake-queue.jsonl via CLI
  - [ ] 2.4: Run EDD cycle against the evals from Task 1; document results in Dev Agent Record

- [ ] Task 3: Extend momentum-tools CLI with triage-queue subcommands (AC: 8)
  - [ ] 3.1: Write failing test in `test-momentum-tools.py` for `triage-queue append` — event written with correct schema (including `id`, `title`, `description`, `status: "open"`), source/kind validation, auto-creation of file if missing
  - [ ] 3.2: Implement `cmd_triage_queue_append` in `momentum-tools.py`: arg parsing for `--source`, `--kind`, `--title`, `--description`, `--rationale`, optional `--feature-slug`, `--story-slug`; write append-only JSONL event with ISO timestamp and `status: "open"`
  - [ ] 3.3: Write failing test for `triage-queue list` — returns open events (`status: "open"`); honors `--kind` and `--source` filters
  - [ ] 3.4: Implement `cmd_triage_queue_list`: read JSONL, filter by `status == "open"`, return structured JSON
  - [ ] 3.5: Write failing test for `triage-queue update` — updates `status` to `consumed` or `rejected` by event id; persists optional `--resolved-at` and `--outcome-ref`; invalid status values produce an error
  - [ ] 3.6: Implement `cmd_triage_queue_update`: locate event by id, update `status`, write optional `resolved_at` and `outcome_ref`, persist back to JSONL
  - [ ] 3.7: Add all three subcommands to the argparse tree, matching the structure of existing `sprint` subcommand group
  - [ ] 3.8: Run tests; confirm green

- [ ] Task 4: Extend momentum-tools CLI story-add with feature-slug and story-type flags (AC: 12)
  - [ ] 4.1: Write failing tests in `test-momentum-tools.py`: feature_slug persistence, story_type persistence (default `feature`), invalid story_type rejection
  - [ ] 4.2: Add `--feature-slug` (optional, default null) and `--story-type` (optional, default `"feature"`) to `story-add` argparse
  - [ ] 4.3: Add `VALID_STORY_TYPES` constant: `{"feature", "maintenance", "defect", "exploration", "practice"}`
  - [ ] 4.4: Update `cmd_story_add` to validate `story_type` and persist both fields in the entry dict
  - [ ] 4.5: Run tests; confirm green

- [ ] Task 5: Update intake skill for feature-awareness (AC: 10, 11)
  - [ ] 5.1: Update `skills/momentum/skills/intake/references/stub-template.md` frontmatter to include `feature_slug` and `story_type` placeholders
  - [ ] 5.2: Update `skills/momentum/skills/intake/workflow.md` Step 1 to extract `{{feature_slug}}` and `{{story_type}}` from context; Step 2 (or a new step) adds feature-slug suggestion flow reading `features.json`; Step 4 passes both fields through to CLI and template
  - [ ] 5.3: Add lightweight story_type heuristic in workflow (keyword mapping to suggested type)
  - [ ] 5.4: Verify intake's eval suite still passes; add one new eval if existing evals do not cover feature_slug and story_type propagation

- [ ] Task 6: Replace Impetus `[3] Triage` placeholder with real dispatch (AC: 2)
  - [ ] 6.1: Update `skills/momentum/skills/impetus/workflow.md` line ~403: replace placeholder output with "Triage → invoke momentum:triage" dispatch action
  - [ ] 6.2: Update `skills/momentum/skills/impetus/SKILL.md` line ~63 with the matching dispatch line
  - [ ] 6.3: Verify existing Impetus evals (`eval-feature-status-fresh-greeting.md`, `eval-2item-menu-returning-user-no-threads.md`) continue to pass; the menu wording is unchanged — only the dispatch handler changes

- [ ] Task 7: Update model-routing-guide.md (AC: 13)
  - [ ] 7.1: Add `momentum:triage` row to the Current Assignments table: `claude-sonnet-4-6` / `high` / rationale citing orchestrator pattern and unvalidated downstream
  - [ ] 7.2: Verify cross-references to the rationale pattern match existing rows (refine / sprint-planning)

## Dev Notes

### Architecture Compliance

This story implements decisions already made; the dev agent does not need to re-decide any of them.

- **DEC-005 (2026-04-14)** — feature-first practice cycle redesign:
  - **D1 (feature_slug mandatory)** — ARTIFACT enrichment (AC5) and intake prerequisite (AC10-12) propagate `feature_slug` through the chain. No ARTIFACT stub may be produced without it.
  - **D2 (DDD epics)** — triage's epic suggestions respect sub-domain boundaries (a practice story belongs in a practice epic, a feature story belongs in a feature's containing epic).
  - **D5 (story_type)** — the five-type enum is canonical: `feature`, `maintenance`, `defect`, `exploration`, `practice`. The CLI (AC12) and stub template (AC10) both enforce this enum.
  - **D6 (terminal states)** — when enriching an observation whose target feature is in a terminal state (`done`, `shelved`, `abandoned`, `rejected`), triage surfaces a warning in the approval UX; the developer may override but must explicitly do so.
  - **D10 (no gap-check at triage)** — triage's workflow must NOT include value-floor or here-to-there gap analysis. Classification only. Gap-check is the responsibility of refinement, sprint-planning, and retro.
- **DEC-007 (2026-04-14)** — unified `intake-queue.jsonl`:
  - Single append-only JSONL event log at `_bmad-output/implementation-artifacts/intake-queue.jsonl`.
  - `source` and `kind` discriminators; retro's `handoff` events (Story B) must fit the same schema without branching.
  - `triage-inbox.md` (from architecture.md ~lines 1671–1698) is retired — do NOT create it, do NOT reference it.
- **Orchestrator-purity pattern** — matches `momentum:refine`, `momentum:sprint-planning`: orchestrator delegates all writes except its own narrow artifact (here, `intake-queue.jsonl`). Encoded as a `<critical>` block in workflow.md.
- **Momentum namespace (NFR12)** — skill at `skills/momentum/skills/triage/`, invoked as `/momentum:triage`.
- **Model-routing (FR23)** — skill frontmatter declares model and effort; `model-routing-guide.md` is updated to match (AC13). Source of truth consistency is a NFR.

### Testing Requirements

This story mixes three change types; each has its own verification approach.

- **skill-instruction tasks** (triage SKILL.md, workflow.md; intake workflow updates; Impetus dispatch; stub-template) — **EDD**. See the Momentum Implementation Guide below for the canonical EDD cycle. Evals are written first, skill implementation follows, then evals are run via subagent spawn to confirm behaviors match.
- **script-code tasks** (momentum-tools `triage-queue append/list` subcommands; `story-add --feature-slug / --story-type` flags) — **TDD** via bmad-dev-story. Tests first in `test-momentum-tools.py`, implement to green, refactor.
- **specification tasks** (model-routing-guide.md update) — direct authoring with cross-reference verification. Verify the new row's format matches existing rows, and the rationale phrasing is consistent.
- **AVFL checkpoint** — run automatically by `momentum:dev` against the produced artifact(s) before marking the story done. This story's ACs are the validation corpus.

### Project Structure Notes

- **New skill directory:** `skills/momentum/skills/triage/` — mirrors existing skill layout (`SKILL.md`, `workflow.md`, optional `references/`, required `evals/`). No changes to parent skill layout conventions.
- **Queue artifact path:** `_bmad-output/implementation-artifacts/intake-queue.jsonl` — append-only JSONL, sibling to `stories/index.json` and `sprints/index.json`. The file is created on first write if absent. Git-tracked.
- **Schema contract (DEC-007 core + story elaboration):** Core discriminators per DEC-007: `source`, `kind`. Remaining fields defined by this story: `{id, title, description, rationale, status, created_at, feature_slug?, story_slug?, resolved_at?}`. `status` (`open` | `consumed` | `rejected`) is the canonical open/closed discriminator; `resolved_at` is a provenance timestamp recorded alongside status transitions. Events are mutated via `triage-queue update` CLI only — never via direct file edit. Both Story A and Story B share this same schema without branching.
- **Retro handoff co-tenancy:** the schema MUST support `source: "retro"` + `kind: "handoff"` so that Story B (`retro-triage-handoff`) can write to the same file without schema changes. This is the primary reason for the `source` discriminator.
- **CLI extension points:** `momentum-tools.py` — add a new `triage-queue` subcommand group at the top-level parser, parallel to `sprint` and `session`. Append-style commands follow the existing `structured result JSON` pattern (see `cmd_story_add` at line ~1503 for the reference implementation).
- **Touches compatibility:** the additions to `story-add` (AC12) are backward-compatible — existing callers that do not pass the new flags continue to work; existing entries without the new fields remain valid.

### References

- **Approved plan:** `/Users/steve/.claude/plans/curious-crunching-crystal.md` — design rationale, agent topology, classification taxonomy, and split decision (Story A + Story B + SDR sequencing). This story is Story A.
- **Decisions:**
  - `_bmad-output/planning-artifacts/decisions/dec-005-cycle-redesign-feature-first-practice-2026-04-14.md` — D1, D2, D5, D6, D10 cited above.
  - `_bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md` — unified intake-queue.jsonl adoption.
- **Features:**
  - `_bmad-output/planning-artifacts/features.json` — parent feature `momentum-backlog-refinement` (feature_slug of this story).
- **Patterns to reuse:**
  - `skills/momentum/skills/refine/workflow.md` Step 9 — batch-approval UX (consolidated findings, batch operations when N≥5, individual overrides). Triage mirrors this exactly.
  - `skills/momentum/skills/retro/workflow.md` Phase 5 — classification + routing (Tier 1 → distill, Tier 2 → stub). Triage generalizes this pattern to six classes and non-retro inputs.
  - `skills/momentum/skills/intake/references/stub-template.md` — baseline frontmatter schema for story stubs; the updated template adds `feature_slug` and `story_type`.
  - `skills/momentum/skills/intake/workflow.md` — Step 1 context extraction and Step 2 epic assignment patterns are the templates for the new feature_slug suggestion flow.
- **CLI:**
  - `skills/momentum/scripts/momentum-tools.py` `cmd_story_add` (line ~1503) and `argparse` for `story-add` (line ~1627) — reference implementation for the new `--feature-slug` and `--story-type` flags.
  - `skills/momentum/scripts/momentum-tools.py` `build_parser` (line ~1565) — where the new `triage-queue` subcommand group is added.
  - `skills/momentum/scripts/test-momentum-tools.py` — test suite pattern to follow for new CLI tests.
- **Impetus integration points:**
  - `skills/momentum/skills/impetus/workflow.md:403` — menu dispatch placeholder to replace.
  - `skills/momentum/skills/impetus/SKILL.md:63` — mirror of the dispatch line.
- **Model routing:**
  - `skills/momentum/references/model-routing-guide.md` — add `momentum:triage` row.
- **Skill NFRs:**
  - `skills/momentum/references/agent-skill-development-guide.md` — frontmatter schema, invocation control, structure rules (body ≤500 lines, description ≤150 chars). Load before writing SKILL.md.
- **A note on sprint-level Gherkin:** This story's ACs are plain English. Gherkin specs for this story (if the sprint planner elects to produce any) live in `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/specs/` per Decision 30 black-box separation. The dev agent implements against the plain English ACs in THIS file and MUST NOT read the `.feature` files. Sprint-planning authors Gherkin at its discretion; create-story never does.

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 5, 6 → skill-instruction (EDD)
- Tasks 3, 4 → script-code (TDD)
- Task 7 → specification (direct authoring with cross-reference verification)

A note on the Gherkin boundary: Gherkin-style `.feature` files, if authored for this story, live in `sprints/{sprint-slug}/specs/` and are OFF-LIMITS to the dev agent. The dev agent implements against the plain English ACs in this story file only (Decision 30 black-box separation).

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/triage/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (`eval-taxonomy-classification.md`, `eval-batch-approval-fidelity.md`, `eval-delegation-boundary.md`).
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]".
   - Test behaviors and decisions, not exact output text.

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, and reference files.

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete.
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely.
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23).
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3).
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills).

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 3+ behavioral evals written in `skills/momentum/skills/triage/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct (`claude-sonnet-4-6` / `high`)
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (`momentum:dev` runs this automatically — validates the implemented SKILL.md and workflow.md against story ACs)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). `bmad-dev-story` handles TDD natively — the guidance below matches its standard approach:

1. **Red:** Write failing tests first for each acceptance criterion in Tasks 3 and 4. Confirm they fail before implementing.
2. **Green:** Implement the minimum code in `momentum-tools.py` to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Script locations:**
- New code goes in `skills/momentum/scripts/momentum-tools.py`.
- New tests go in `skills/momentum/scripts/test-momentum-tools.py`.
- Follow the existing pattern: one `cmd_*` function per subcommand, argparse wiring in `build_parser`, `result(...)` helper for structured JSON output, `error_result(...)` for failures.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies — listed here for reference):**
- [ ] Tests written first, confirmed failing before implementation
- [ ] All new tests passing
- [ ] No regressions in existing test suite
- [ ] Code quality checks pass if configured

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source — not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per AC13 — add the new row to `model-routing-guide.md`.
2. **Verify cross-references:** the row format and rationale phrasing match the pattern established by existing rows (`momentum:refine`, `momentum:sprint-planning`). Confirm `skills/momentum/skills/triage/SKILL.md` frontmatter `model` and `effort` match the values listed in the guide (single source of truth alignment).
3. **Verify format compliance:** table markdown is valid; column alignment preserved.
4. **Document** what was updated in the Dev Agent Record.

**No tests or evals required** for the spec update. AVFL checkpoint (run by `momentum:dev`) validates against ACs.

**Additional DoD items for specification tasks:**
- [ ] All cross-references resolve correctly (skill frontmatter ↔ model-routing-guide row)
- [ ] Table format preserved
- [ ] AVFL checkpoint result documented (`momentum:dev` runs this automatically)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
