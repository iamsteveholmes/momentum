# Story 0.2: Sprint-Status Decomposition

Status: done

## Story

As a developer,
I want `sprint-status.yaml` decomposed into a `stories/` folder and a `sprints/` folder,
so that story records and sprint records are individually addressable files rather than entries in a monolithic YAML.

## Acceptance Criteria

1. **Given** the existing `sprint-status.yaml` (keys already in slug format from Story 0.1)
   **When** the decomposition runs
   **Then** a `stories/` folder exists containing an `index.json` with one entry per story
   **And** each entry in `stories/index.json` has: slug, status, title, epic_slug, depends_on, touches
   **And** a stub `.md` file exists in `stories/` for each story (named `{slug}.md`)
   **And** a `sprints/` folder exists containing an `index.json`
   **And** `sprint-status.yaml` is marked deprecated and retained temporarily for backward compatibility
   **And** no story data is lost -- all status values, dependencies, touches, and epic memberships are preserved

2. **Given** stories in `sprint-status.yaml` grouped under epic comment headers
   **When** they are extracted into `stories/index.json`
   **Then** each story entry's `epic_slug` reflects the epic it belongs to (derived from the comment group it appeared under)
   **And** epic membership is carried in `stories/index.json`, not in `epics.md`

3. **Given** `epics.md` currently contains or may contain story lists
   **When** the decomposition runs
   **Then** `epics.md` is updated to contain only epic names, slugs, and descriptions
   **And** any story lists in `epics.md` are removed (epic membership is now authoritative in `stories/index.json`)

4. **Given** no active sprint currently defined in the old schema
   **When** the decomposition runs
   **Then** `sprints/index.json` is created with an empty active sprint and a placeholder planning entry
   **And** any active or planning sprint data from the old schema is preserved in `sprints/index.json`

5. **Given** a schema reference document is needed for downstream skills
   **When** the decomposition completes
   **Then** a schema reference document is created at `skills/momentum/references/sprint-status-schema.md` describing the `stories/index.json` structure, `sprints/index.json` structure, field types, valid status values, and example entries

6. **Given** skills that currently read from `sprint-status.yaml`
   **When** the decomposition is complete
   **Then** those skills are updated to read story status and metadata from `stories/index.json`
   **And** those skills are updated to read sprint data from `sprints/index.json`
   **And** no skill reads from the deprecated `sprint-status.yaml` after this story

## Tasks / Subtasks

- [ ] Task 1: Build `stories/index.json` from old data (AC: #1, #2)
  - [ ] 1.1: Read the full current `sprint-status.yaml` (post-Story-0.1, keys already in slug format).
  - [ ] 1.2: For each story key in `development_status`, create a `stories/index.json` entry with: `slug` (the key), `status` (from development_status value), `title` (convert slug to human-readable title -- capitalize words, replace hyphens with spaces), `epic_slug` (derived from the epic comment block the story appeared under -- see Epic Slug Mapping in Dev Notes), `depends_on` (from momentum_metadata entry if it exists, otherwise []), `touches` (from momentum_metadata entry if it exists, otherwise []).
  - [ ] 1.3: Epic keys and retrospective keys from `development_status` are NOT included in `stories/index.json` -- they are not stories.
  - [ ] 1.4: Write `stories/index.json`. Validate it parses without error.

- [ ] Task 2: Create stub story files in `stories/` (AC: #1)
  - [ ] 2.1: For each story slug in the new `stories/index.json`, create a minimal stub file at `stories/{slug}.md` if one does not already exist. Stub content: `# {title}\n\nStatus: {status}\n`.
  - [ ] 2.2: If an existing story implementation file exists at `_bmad-output/implementation-artifacts/{slug}.md`, the stub is still created at `stories/{slug}.md` -- the implementation file at its current location is not moved in this story.

- [ ] Task 3: Build `sprints/index.json` (AC: #4)
  - [ ] 3.1: Create `sprints/index.json` with `active: null` (no sprint currently defined in the old schema) and a `planning` entry with `locked: false` as placeholder.
  - [ ] 3.2: If any sprint data exists in the old schema, preserve it in `sprints/index.json`.
  - [ ] 3.3: Validate `sprints/index.json` parses without error.

- [ ] Task 4: Update `epics.md` (AC: #3)
  - [ ] 4.1: Read the current `epics.md`.
  - [ ] 4.2: Remove any story lists from epic sections. Retain only: epic name, slug, and description.
  - [ ] 4.3: Write the updated `epics.md`.

- [ ] Task 5: Mark `sprint-status.yaml` deprecated (AC: #1)
  - [ ] 5.1: Add a comment header at the top of `sprint-status.yaml`: `# DEPRECATED: Decomposed into stories/index.json and sprints/index.json. This file is retained temporarily for backward compatibility and will be removed in a future story.`
  - [ ] 5.2: Do NOT delete the file -- backward compatibility period ends when all skills are updated.

- [ ] Task 6: Create schema reference document (AC: #5)
  - [ ] 6.1: Create `skills/momentum/references/sprint-status-schema.md` documenting: the `stories/index.json` structure (field names, types, valid status values), the `sprints/index.json` structure, example entries, and the write authority rule (momentum-sprint-manager is sole writer of these files). Valid story statuses: backlog, ready-for-dev, in-progress, review, verify, done, dropped, closed-incomplete.
  - [ ] 6.2: Reference the architecture document's Sprint Tracking Schema section as the source of truth.

- [ ] Task 7: Update skills that read sprint-status.yaml (AC: #6)
  - [ ] 7.1: Update `skills/momentum-create-story/workflow.md` -- change references from `development_status[key]` to `stories/index.json`.
  - [ ] 7.2: Update `skills/momentum/workflow.md` (Impetus) -- change sprint-status.yaml reading logic to use `stories/index.json` and `sprints/index.json`.
  - [ ] 7.3: Update `skills/momentum-dev/workflow.md` -- change next-story selection to read from `stories/index.json` (status, depends_on).
  - [ ] 7.4: Update `skills/momentum-plan-audit/workflow.md` -- change any sprint-status references to `stories/index.json` and `sprints/index.json`.
  - [ ] 7.5: Update `skills/momentum/scripts/update-story-status.sh` -- add deprecation notice (this script is deprecated by Story 0.3).
  - [ ] 7.6: Update `.claude/skills/bmad-create-story/workflow.md` -- change references from `development_status` to `stories/index.json`.
  - [ ] 7.7: Update `.claude/skills/bmad-sprint-status/workflow.md` -- change reading logic to `stories/index.json` and `sprints/index.json`.
  - [ ] 7.8: Update `.claude/skills/bmad-sprint-planning/workflow.md` -- change reading/writing to `stories/index.json` and `sprints/index.json`.

- [ ] Task 8: Validate decomposition integrity (AC: #1)
  - [ ] 8.1: Count total stories in old `development_status` vs entries in `stories/index.json` -- must match.
  - [ ] 8.2: Verify every story entry in `stories/index.json` has a non-empty `epic_slug`.
  - [ ] 8.3: Verify all `depends_on` references in `stories/index.json` resolve to valid slugs in the same file.
  - [ ] 8.4: Verify stub files exist in `stories/` for every slug in `stories/index.json`.
  - [ ] 8.5: Verify both `stories/index.json` and `sprints/index.json` parse without error.

## Dev Notes

### Scope and Approach

This story decomposes the monolithic `sprint-status.yaml` into a folder-based structure. The target output is:

```
stories/
  index.json          # flat registry: slug, status, title, epic_slug, depends_on, touches
  {slug}.md           # stub story file per story
sprints/
  index.json          # active sprint + planning sprint
epics.md              # names, slugs, descriptions only (no story lists)
```

**Pre-condition:** Story 0.1 has already renamed all keys to kebab-case slugs. This story operates on the slug-format keys.

**sprint-status.yaml is NOT deleted in this story.** It is marked deprecated and retained for the backward-compatibility window. Deletion is a future cleanup story.

### stories/index.json Structure

```json
{
  "stories": {
    "posttooluse-lint-hook": {
      "slug": "posttooluse-lint-hook",
      "status": "in-progress",
      "title": "PostToolUse Lint Hook",
      "epic_slug": "quality-enforcement",
      "depends_on": [],
      "touches": ["skills/momentum/references/hooks/"]
    }
  }
}
```

### sprints/index.json Structure

```json
{
  "active": null,
  "planning": {
    "locked": false
  }
}
```

When an active sprint exists:
```json
{
  "active": {
    "name": "Quality Hooks Sprint",
    "slug": "quality-hooks-sprint",
    "stories": ["posttooluse-lint-hook"],
    "locked": true,
    "started": "2026-03-30",
    "waves": [
      { "wave": 1, "stories": ["posttooluse-lint-hook"] }
    ]
  },
  "planning": {
    "name": "Impetus UX Sprint",
    "slug": "impetus-ux-sprint",
    "stories": ["impetus-identity-redesign"],
    "locked": false
  }
}
```

### Epic Slug Mapping

Stories are assigned `epic_slug` based on the comment group they appeared under in the old `development_status`:

| Comment header | epic_slug |
|---|---|
| Epic 0: Redesign Foundation | redesign-foundation |
| Epic 1: Foundation & Bootstrap | foundation-bootstrap |
| Epic 1b: Foundation Fixes | foundation-fixes |
| Epic 2: Stay Oriented with Impetus | stay-oriented-impetus |
| Epic 2 Refinement: Harden Epic 2 Foundation | harden-epic-2-foundation |
| Epic 2a: Impetus UX Redesign | impetus-ux-redesign |
| Epic 2b: Impetus as Epic Orchestrator | impetus-epic-orchestrator |
| Epic 3: Automatic Quality Enforcement | quality-enforcement |
| Epic 4: Complete Story Cycles | story-cycles |
| Epic 5: Trust Artifact Provenance | artifact-provenance |
| Epic 6: The Practice Compounds | practice-compounds |
| Epic 7: Bring Your Own Tools | bring-your-own-tools |
| Epic 8: Research & Knowledge Management | research-knowledge |
| Epic 9: Performance Validation | performance-validation |
| Process stories (pN-N-slug group) | process-stories |

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
> momentum-sprint-manager | stories/index.json, sprints/index.json (sole writer of status fields)
> momentum-create-story | writes story stub files in stories/
[Source: _bmad-output/planning-artifacts/architecture.md#Architectural Boundaries]

Note: After Story 0.3, momentum-sprint-manager becomes the sole writer of `stories/index.json` status fields and all of `sprints/index.json`. This story focuses on decomposition and skill updates; the strict write-authority enforcement is Story 0.3's scope.

### Critical Constraints

1. **JSON validity:** Both `stories/index.json` and `sprints/index.json` must parse as valid JSON. Validate after writing.

2. **Data completeness:** Every story in the old `development_status` must appear in `stories/index.json`. No story data is lost.

3. **epics.md stays clean:** Epic membership moves entirely to `stories/index.json`. `epics.md` becomes names/slugs/descriptions only.

4. **Backward compatibility period:** `sprint-status.yaml` is NOT deleted -- skills are updated in the same story, but the deprecated file remains for any tool that reads it outside of skills.

5. **Process stories:** Stories in the `pN-N-slug` group get `epic_slug: process-stories`.

### Project Structure Notes

- **New files:** `stories/index.json`, `stories/{slug}.md` (stubs), `sprints/index.json`
- **Updated files:** `epics.md` (trimmed), `sprint-status.yaml` (deprecated header added)
- **Schema reference output:** `skills/momentum/references/sprint-status-schema.md` (new file)
- **Skills to update:** 8 workflow files across Momentum and BMAD skills

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Sprint Tracking Schema] -- target structure, field types, examples
- [Source: _bmad-output/planning-artifacts/architecture.md#Architectural Boundaries] -- read/write authority
- [Source: _bmad-output/planning-artifacts/architecture.md#Story State Machine] -- valid status values
- [Source: _bmad-output/planning-artifacts/epics.md#Epic 0: Redesign Foundation] -- story requirements, sequencing
- [Source: _bmad-output/implementation-artifacts/sprint-status.yaml] -- current data being migrated

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5, 8 -> config-structure (direct)
- Task 6 -> specification (direct)
- Task 7 -> skill-instruction (EDD)

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
