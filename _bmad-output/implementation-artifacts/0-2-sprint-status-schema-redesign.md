# Story 0.2: Sprint-Status Schema Redesign

Status: ready-for-dev

## Story

As a developer,
I want sprint-status.yaml restructured into three sections (stories, epics, sprints),
so that story tracking, epic membership, and sprint planning are cleanly separated and the schema supports wave-based execution.

## Acceptance Criteria

1. **Given** the existing `sprint-status.yaml` with `development_status` and `momentum_metadata` sections (keys already in slug format from Story 0.1)
   **When** the schema migration runs
   **Then** the file is restructured into three top-level sections: `stories` (flat registry), `epics` (category membership), `sprints` (active + planning)
   **And** each story entry in `stories` has: status, title, story_file (boolean), depends_on, touches
   **And** each epic entry in `epics` has: title, stories (list of story slugs)
   **And** the `sprints` section has: `active` (with locked, started, waves) and `planning` (with locked: false)
   **And** all existing story data is migrated without loss

2. **Given** the old `development_status` section with story status values
   **When** migrating to the `stories` section
   **Then** each story key becomes an entry with `status` (from development_status), `title` (derived from the slug, human-readable), `story_file` (boolean: true if a file exists in `_bmad-output/implementation-artifacts/`), `depends_on` (from momentum_metadata or empty list), `touches` (from momentum_metadata or empty list)

3. **Given** the old `development_status` section with epic keys and their statuses
   **When** migrating to the `epics` section
   **Then** each epic becomes an entry with `title` (human-readable, derived from the epic comment headers) and `stories` (list of story slugs that belong to that epic, in their original order)

4. **Given** no active sprint currently defined in the old schema
   **When** the migration runs
   **Then** the `sprints` section is created with `active: null` and a `planning` entry with `locked: false`

5. **Given** a schema reference document is needed for downstream skills
   **When** the migration completes
   **Then** a schema reference document is created at `skills/momentum/references/sprint-status-schema.md` describing the three-section structure, field types, valid status values, and example entries

6. **Given** skills that currently read `development_status` from sprint-status.yaml
   **When** the schema changes
   **Then** those skills are updated to read from `stories[slug].status` instead
   **And** any skill that reads `momentum_metadata[slug].depends_on` reads from `stories[slug].depends_on` instead
   **And** any skill that reads `momentum_metadata[slug].touches` reads from `stories[slug].touches` instead
   **And** any skill that reads `momentum_metadata[slug].story_file` reads from `stories[slug].story_file` instead

7. **Given** the old `momentum_metadata` section
   **When** the migration completes
   **Then** the `momentum_metadata` section is removed entirely (its data is merged into `stories` entries)

8. **Given** the old `development_status` section
   **When** the migration completes
   **Then** the `development_status` section is removed entirely (replaced by the `stories` section)

## Tasks / Subtasks

- [ ] Task 1: Build the new `stories` section from old data (AC: #1, #2)
  - [ ] 1.1: Read the full current `sprint-status.yaml` (post-Story-0.1, keys already in slug format).
  - [ ] 1.2: For each story key in `development_status`, create a `stories` entry with: `status` (from development_status value), `title` (convert slug to human-readable title -- capitalize words, replace hyphens with spaces), `story_file` (boolean -- check if `_bmad-output/implementation-artifacts/{slug}.md` exists), `depends_on` (from momentum_metadata entry if it exists, otherwise []), `touches` (from momentum_metadata entry if it exists, otherwise []).
  - [ ] 1.3: Epic keys and retrospective keys from `development_status` are NOT included in `stories` -- they move to the `epics` section (Task 2).

- [ ] Task 2: Build the new `epics` section from old data (AC: #1, #3)
  - [ ] 2.1: Parse the epic comment headers in `development_status` (e.g., `# Epic 1: Foundation & Bootstrap`) to identify epic groupings.
  - [ ] 2.2: For each epic, create an `epics` entry with only the fields defined in the architecture schema: `title` (from the comment header text) and `stories` (ordered list of story slugs that appear under that epic's comment block). Do NOT add `status` or `retrospective` fields -- the architecture schema for `epics` entries contains only `title` and `stories`.
  - [ ] 2.3: Epic status (from old `epic-N` keys) and retrospective status (from old `epic-N-retrospective` keys) are discarded during migration -- they are not part of the new `epics` schema. Epic completion is derivable from story statuses (all stories done = epic done).

- [ ] Task 3: Build the new `sprints` section (AC: #1, #4)
  - [ ] 3.1: Create the `sprints` section with `active: null` (no sprint currently defined in the old schema).
  - [ ] 3.2: Create a `planning` entry with `locked: false` as placeholder.

- [ ] Task 4: Write the restructured sprint-status.yaml (AC: #1, #7, #8)
  - [ ] 4.1: Assemble the complete new file with header metadata (generated, last_updated, project, etc.) followed by the three sections: `stories`, `epics`, `sprints`.
  - [ ] 4.2: Include a status definitions comment block at the top (updated to reflect the new schema -- story statuses now include `verify` stage per architecture).
  - [ ] 4.3: Remove the old `development_status` and `momentum_metadata` sections entirely.
  - [ ] 4.4: Validate the output is valid YAML (parse with a YAML tool).

- [ ] Task 5: Create schema reference document (AC: #5)
  - [ ] 5.1: Create `skills/momentum/references/sprint-status-schema.md` documenting: the three-section structure, field types for each section, valid status values (story: backlog, ready-for-dev, in-progress, review, verify, done, dropped, closed-incomplete; epic: backlog, in-progress, done, done-incomplete), example entries, and the write authority rule (momentum-sprint-manager is sole writer).
  - [ ] 5.2: Reference the architecture document's Sprint Tracking Schema section as the source of truth.

- [ ] Task 6: Update skills that read sprint-status.yaml (AC: #6)
  - [ ] 6.1: Update `skills/momentum-create-story/workflow.md` -- change references from `development_status[key]` to `stories[slug].status`.
  - [ ] 6.2: Update `skills/momentum/workflow.md` (Impetus) -- change sprint-status.yaml reading logic to use `stories` and `epics` sections.
  - [ ] 6.3: Update `skills/momentum-dev/workflow.md` -- change next-story selection to read from `stories[slug].status` and `stories[slug].depends_on`.
  - [ ] 6.4: Update `skills/momentum-plan-audit/workflow.md` -- change any sprint-status references to new schema.
  - [ ] 6.5: Update `skills/momentum/scripts/update-story-status.sh` -- this script is deprecated per architecture (momentum-sprint-manager replaces it in Story 0.3), but if still referenced, update or add deprecation notice.
  - [ ] 6.6: Update `.claude/skills/bmad-create-story/workflow.md` -- change references from `development_status` to `stories[slug].status`.
  - [ ] 6.7: Update `.claude/skills/bmad-sprint-status/workflow.md` -- change sprint-status reading logic to new schema.
  - [ ] 6.8: Update `.claude/skills/bmad-sprint-planning/workflow.md` -- change sprint-status writing/reading to new schema.

- [ ] Task 7: Validate migration integrity (AC: #1)
  - [ ] 7.1: Count total stories in old `development_status` vs new `stories` section -- must match.
  - [ ] 7.2: Count total epics in old schema vs new `epics` section -- must match.
  - [ ] 7.3: Verify every story slug appears in exactly one epic's `stories` list.
  - [ ] 7.4: Verify all `depends_on` references in `stories` resolve to valid story keys.
  - [ ] 7.5: Verify the output YAML parses without error.

## Dev Notes

### Scope and Approach

This story transforms the sprint-status.yaml schema from a flat two-section format (`development_status` + `momentum_metadata`) into a three-section normalized schema (`stories`, `epics`, `sprints`). It also updates all downstream skill files that read the old schema.

**Pre-condition:** Story 0.1 has already renamed all keys to kebab-case slugs. This story operates on the slug-format keys.

### Target Schema (from Architecture)

The architecture document defines the exact target schema at `architecture.md#Sprint Tracking Schema`:

```yaml
stories:
  posttooluse-lint-hook:
    status: in-progress
    title: PostToolUse lint and format hook
    story_file: true
    depends_on: []
    touches:
      - "skills/momentum/references/hooks/"

epics:
  quality-enforcement:
    title: "Automatic Quality Enforcement"
    stories:
      - posttooluse-lint-hook
      - pretooluse-file-protection

sprints:
  active:
    name: "Quality Hooks Sprint"
    slug: quality-hooks-sprint
    stories:
      - posttooluse-lint-hook
    locked: true
    started: 2026-03-30
    waves:
      - wave: 1
        stories:
          - posttooluse-lint-hook
  planning:
    name: "Impetus UX Sprint"
    slug: impetus-ux-sprint
    stories:
      - impetus-identity-redesign
    locked: false
```

[Source: _bmad-output/planning-artifacts/architecture.md#Sprint Tracking Schema]

### Schema Field Reference

**stories entry:**
| Field | Type | Description |
|---|---|---|
| status | string | backlog, ready-for-dev, in-progress, review, verify, done, dropped, closed-incomplete |
| title | string | Display title |
| story_file | boolean | Whether implementation file exists |
| depends_on | list | Story slugs that must be done first |
| touches | list | Paths this story creates or modifies |

[Source: _bmad-output/planning-artifacts/architecture.md#Sprint Tracking Schema]

### Epic Key Mapping

The old schema uses `epic-N` keys with comment headers. The new schema uses named epic slugs. Mapping:

| Old key | Comment header | New epic slug |
|---|---|---|
| epic-0 | Epic 0: Redesign Foundation | redesign-foundation |
| epic-1 | Epic 1: Foundation & Bootstrap | foundation-bootstrap |
| epic-1b | Epic 1b: Foundation Fixes | foundation-fixes |
| epic-2 | Epic 2: Stay Oriented with Impetus | stay-oriented-impetus |
| epic-2-refinement | Epic 2 Refinement: Harden Epic 2 Foundation | harden-epic-2-foundation |
| epic-2a | Epic 2a: Impetus UX Redesign | impetus-ux-redesign |
| epic-2b | Epic 2b: Impetus as Epic Orchestrator | impetus-epic-orchestrator |
| epic-3 | Epic 3: Automatic Quality Enforcement | quality-enforcement |
| epic-4 | Epic 4: Complete Story Cycles | story-cycles |
| epic-5 | Epic 5: Trust Artifact Provenance | artifact-provenance |
| epic-6 | Epic 6: The Practice Compounds | practice-compounds |
| epic-7 | Epic 7: Bring Your Own Tools | bring-your-own-tools |
| epic-8 | Epic 8: Research & Knowledge Management | research-knowledge |
| epic-9 | Epic 9: Performance Validation | performance-validation |

### Skills That Read sprint-status.yaml

The following files reference `sprint-status`, `development_status`, or `momentum_metadata` and need updating:

**Momentum skills (in `skills/`):**
- `skills/momentum-create-story/workflow.md` -- reads development_status for story status
- `skills/momentum/workflow.md` -- Impetus reads for session orientation and progress bar
- `skills/momentum-dev/workflow.md` -- reads for next-story selection
- `skills/momentum-plan-audit/workflow.md` -- reads for sprint context
- `skills/momentum/scripts/update-story-status.sh` -- writes development_status (deprecated by Story 0.3)

**BMAD skills (in `.claude/skills/`):**
- `.claude/skills/bmad-create-story/workflow.md` -- reads development_status for story discovery
- `.claude/skills/bmad-sprint-status/workflow.md` -- reads for status summary
- `.claude/skills/bmad-sprint-planning/workflow.md` -- reads/writes for sprint planning

### Architecture Compliance

**Write authority (Architecture, Architectural Boundaries section):**
> momentum-create-story reads sprint-status.yaml, epics.md; writes Story files in _bmad-output/implementation-artifacts/
> momentum-sprint-manager writes sprint-status.yaml (sole writer)
[Source: _bmad-output/planning-artifacts/architecture.md#Architectural Boundaries]

Note: After Story 0.3, momentum-create-story should no longer write to sprint-status.yaml directly -- it should delegate to momentum-sprint-manager. This story focuses on schema migration; the write authority change is Story 0.3's scope.

### Critical Constraints

1. **YAML validity:** The output must parse as valid YAML. Use a YAML parser to validate after writing.

2. **Data completeness:** Every story in the old `development_status` must appear in the new `stories` section. Every story must appear in exactly one epic's `stories` list.

3. **Backward compatibility period:** Skills are updated in the same story that changes the schema. There is no period where the old schema exists but skills expect the new one, or vice versa.

4. **Process stories:** Stories like `p1-1-remove-git-mcp-server-dependency` (now `remove-git-mcp-server-dependency` after Story 0.1) need an epic assignment. Create a `process-stories` epic for these.

### Project Structure Notes

- **sprint-status.yaml location:** `_bmad-output/implementation-artifacts/sprint-status.yaml`
- **Schema reference output:** `skills/momentum/references/sprint-status-schema.md` (new file)
- **Skills to update:** 8 workflow files across Momentum and BMAD skills

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Sprint Tracking Schema] -- target schema, field types, examples
- [Source: _bmad-output/planning-artifacts/architecture.md#Architectural Boundaries] -- read/write authority
- [Source: _bmad-output/planning-artifacts/architecture.md#Story State Machine] -- valid status values
- [Source: _bmad-output/planning-artifacts/epics.md#Epic 0: Redesign Foundation] -- story requirements, sequencing
- [Source: _bmad-output/implementation-artifacts/sprint-status.yaml] -- current data being migrated

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 7 -> config-structure (direct)
- Task 5 -> specification (direct)
- Task 6 -> skill-instruction (EDD)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write the config or create the directory structure** per the story's acceptance criteria
2. **Verify by inspection:**
   - YAML files: must parse without error (validate with a YAML parser -- do not rely on manual visual inspection)
   - Required fields: each required field must be present with the correct type
   - Paths: all referenced paths must exist after creation
   - Version consistency: any version fields must be consistent with related version references
3. **Document** what was created in the Dev Agent Record

**No tests required** for pure config/structure changes.

**DoD items for config-structure tasks:**
- [ ] All YAML files parse without error (validated with a tool)
- [ ] All required fields present with correct types
- [ ] All referenced paths exist after creation
- [ ] Changes documented in Dev Agent Record

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (epic, PRD, or parent spec) -- not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per the story's acceptance criteria
2. **Verify cross-references:** All references to other documents, files, sections, or identifiers must resolve correctly.
3. **Verify format compliance:** If the project has an established template or convention for this document type, confirm the output follows it.
4. **Document** what was written or updated in the Dev Agent Record

**Additional DoD items for specification tasks:**
- [ ] All cross-references to other documents, files, or sections resolve correctly
- [ ] Document follows project template/format conventions if one exists
- [ ] AVFL checkpoint result documented (momentum-dev runs this automatically)

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts -- unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2-3 behavioral evals in the relevant skill's `evals/` directory (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the workflow.md or reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it the eval's scenario and load the skill. Observe whether behavior matches.
4. If all evals match -> task complete
5. If any eval fails -> diagnose the gap in the skill instructions, revise, re-run (max 3 cycles)

**NFR compliance -- mandatory for every skill-instruction task:**
- SKILL.md `description` field must be <= 150 characters (NFR1)
- `model:` and `effort:` frontmatter fields must be present (FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens (NFR3)
- Skill names prefixed `momentum-` (NFR12)

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in relevant skill's `evals/`
- [ ] EDD cycle ran -- all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description <= 150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body <= 500 lines / 5000 tokens confirmed
- [ ] AVFL checkpoint on produced artifact documented

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
