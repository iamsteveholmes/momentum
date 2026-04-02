# Story 0.1: Story ID Migration

Status: ready-for-dev

## Story

As a developer,
I want all story keys renamed from `N-N-slug` format to plain kebab-case slugs,
so that stories can be re-categorized across epics without renaming and the ID format is globally unique.

## Acceptance Criteria

1. **Given** the existing `sprint-status.yaml` with story keys in `N-N-slug` format
   **When** the migration runs
   **Then** all story keys are renamed to plain kebab-case slugs (e.g., `1-1-repository-structure-established` -> `repository-structure-established`)
   **And** all references to the old keys in `sprint-status.yaml` are updated (`development_status`, `momentum_metadata`)
   **And** story implementation files in `_bmad-output/implementation-artifacts/` are renamed to match the new slug format
   **And** no data is lost -- all status values, dependencies, touches, and story_file paths are preserved
   **And** the output is still `sprint-status.yaml` with renamed keys -- decomposition into `stories/` and `sprints/` folders is Story 0.2's responsibility

2. **Given** two stories that would produce the same slug after removing the epic prefix
   **When** a collision is detected
   **Then** a qualifier suffix is added to disambiguate (e.g., append `-epic1` or a domain qualifier)

3. **Given** epic keys (e.g., `epic-1`, `epic-1b`) and retrospective keys (e.g., `epic-1-retrospective`)
   **When** the migration runs
   **Then** these keys are preserved unchanged -- they are not story keys and do not follow the `N-N-slug` pattern

4. **Given** process story keys (e.g., `p1-1-remove-git-mcp-server-dependency`)
   **When** the migration runs
   **Then** these are also migrated to plain kebab-case slugs (e.g., `remove-git-mcp-server-dependency`)

5. **Given** `momentum_metadata` entries reference old story keys in `depends_on` lists
   **When** the migration runs
   **Then** all `depends_on` references are updated to use the new slug format

6. **Given** `momentum_metadata` entries have `story_file` paths referencing old filenames
   **When** the migration runs
   **Then** all `story_file` paths are updated to reflect the renamed file basenames

## Tasks / Subtasks

- [ ] Task 1: Build migration mapping table (AC: #1, #2, #4)
  - [ ] 1.1: Read all story keys from `sprint-status.yaml` `development_status` section. For each key matching `N-N-slug` or `Na-N-slug` pattern (e.g., `1-1-repository-structure-established`, `2a-1-silent-pre-flight-and-deferred-stats-write`, `p1-1-remove-git-mcp-server-dependency`), strip the epic prefix to produce the new slug.
  - [ ] 1.2: Check for slug collisions. If two different old keys produce the same new slug, add a qualifier suffix per AC #2. (Pre-analysis confirms zero collisions exist in the current dataset -- but the check must still run.)
  - [ ] 1.3: Build a mapping dict: `{ old_key: new_slug }` for all story keys. Epic keys and retrospective keys are excluded from this mapping.

- [ ] Task 2: Rename story keys in `development_status` section (AC: #1, #3)
  - [ ] 2.1: Read `sprint-status.yaml` fully, preserving all comments and structure.
  - [ ] 2.2: For each entry in `development_status`, if the key exists in the migration mapping, replace the key with the new slug. Preserve the status value, comments, and section grouping.
  - [ ] 2.3: Leave epic keys (`epic-N`, `epic-Nb`) and retrospective keys (`epic-N-retrospective`) unchanged.

- [ ] Task 3: Rename story keys in `momentum_metadata` section (AC: #1, #5, #6)
  - [ ] 3.1: For each entry in `momentum_metadata`, if the key exists in the migration mapping, replace the key with the new slug.
  - [ ] 3.2: For each entry's `depends_on` list, replace any old key references with their new slugs using the migration mapping.
  - [ ] 3.3: For each entry's `story_file` path, update the filename portion to use the new slug (e.g., `_bmad-output/implementation-artifacts/1-1-repository-structure-established.md` -> `_bmad-output/implementation-artifacts/repository-structure-established.md`).

- [ ] Task 4: Rename implementation artifact files (AC: #1)
  - [ ] 4.1: For each story file in `_bmad-output/implementation-artifacts/` whose basename (without `.md`) matches an old key in the migration mapping, rename the file to use the new slug.
  - [ ] 4.2: Verify all renamed files exist at their new paths after renaming.

- [ ] Task 5: Write the updated sprint-status.yaml (AC: #1)
  - [ ] 5.1: Write the in-memory transformed `sprint-status.yaml` to disk, preserving ALL comments, section headers, and status definitions block.

- [ ] Task 6: Validate migration integrity (AC: #1)
  - [ ] 6.1: Re-read `sprint-status.yaml` from disk and confirm: no `N-N-slug` format keys remain in `development_status` or `momentum_metadata` (except epic and retrospective keys).
  - [ ] 6.2: Confirm total story count in `development_status` is unchanged before and after migration.
  - [ ] 6.3: Confirm all `story_file` paths in `momentum_metadata` point to files that actually exist on disk (post-Task-4 renames).
  - [ ] 6.4: Confirm all `depends_on` references in `momentum_metadata` resolve to valid keys in `development_status`.
  - [ ] 6.5: Confirm the written YAML parses without error.

## Dev Notes

### Scope and Approach

This is a data migration story -- no new features, no new skills, no new code artifacts. The work is a one-time transformation of `sprint-status.yaml` keys and corresponding file renames.

**Total story keys to migrate:** 67 unique story keys across `development_status` (some also appear in `momentum_metadata`). Zero slug collisions detected in pre-analysis.

**Key patterns being stripped:**
- `N-N-slug` (e.g., `1-1-repository-structure-established` -> `repository-structure-established`)
- `Na-N-slug` (e.g., `2a-1-silent-pre-flight-and-deferred-stats-write` -> `silent-pre-flight-and-deferred-stats-write`)
- `pN-N-slug` (e.g., `p1-1-remove-git-mcp-server-dependency` -> `remove-git-mcp-server-dependency`)

**Keys NOT migrated (preserved as-is):**
- Epic keys: `epic-1`, `epic-1b`, `epic-2`, `epic-2-refinement`, `epic-2a`, `epic-2b`, `epic-3`, `epic-4` through `epic-9`
- Retrospective keys: `epic-1-retrospective`, `epic-1b-retrospective`, etc.
- Non-story files: `avfl-integration-action-items.md`, `epic-1-retro-2026-03-22.md`, `epic-2-dogfood-findings.md`, `epic-2-refinement-proposal.md`

### Architecture Compliance

**Story ID format (Architecture, Story State Machine section):**
> Story ID format: Globally unique kebab-case slugs. No epic encoding.
> Good: `posttooluse-lint-hook`
> Bad: `3-1-posttooluse-lint-hook` -- encodes epic, breaks on re-categorization
[Source: _bmad-output/planning-artifacts/architecture.md#Story State Machine]

**Collision resolution (Architecture, Story State Machine section):**
> Collision resolution: add short qualifier suffix (`auth-refresh-api` vs `auth-refresh-ui`).
[Source: _bmad-output/planning-artifacts/architecture.md#Story State Machine]

**Migration note (Architecture, Sprint Tracking Schema section):**
> Migration from old schema: The `story-id-migration` and `sprint-status-schema-redesign` stories handle the transition from the old `development_status` + `momentum_metadata` flat-key format to this three-section schema. All existing story keys (`N-N-slug` format) will be renamed to plain kebab-case slugs.
[Source: _bmad-output/planning-artifacts/architecture.md#Sprint Tracking Schema]

### Critical Constraints

1. **Comment preservation:** `sprint-status.yaml` contains section header comments (`# Epic 1: Foundation & Bootstrap`), status definition comments, and metadata comments. All must be preserved exactly. Use a text-level find-and-replace approach rather than YAML parse-and-serialize to avoid comment loss.

2. **Atomic operation:** All five tasks must complete together. A partial migration (keys renamed but files not, or `development_status` renamed but `momentum_metadata` not) leaves the system inconsistent.

3. **No schema change:** This story only renames keys. It does NOT decompose `sprint-status.yaml` into the `stories/` and `sprints/` folder structure -- that is Story 0.2. After this story, the file still has `development_status` and `momentum_metadata` sections -- just with new key names.

4. **`epics.md` story references:** The epic descriptions in `epics.md` reference stories by their `N.N` identifiers (e.g., "Story 0.1", "Story 3.1") and by their old keys. These are NOT updated in this story -- they are specification documents, and their key references will become historical. The new `stories/index.json` and `sprints/` structure (Story 0.2) will use the new slugs.

### Project Structure Notes

- **sprint-status.yaml location:** `_bmad-output/implementation-artifacts/sprint-status.yaml`
- **Implementation artifact files:** `_bmad-output/implementation-artifacts/*.md` (32 story files to potentially rename, plus non-story files that are preserved)
- **File renames are git-tracked:** Use `git mv` for renames so git tracks the rename rather than treating it as delete+create.

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Story State Machine] -- new ID format, collision resolution
- [Source: _bmad-output/planning-artifacts/architecture.md#Sprint Tracking Schema] -- migration note, three-section target schema
- [Source: _bmad-output/planning-artifacts/epics.md#Epic 0: Redesign Foundation] -- story requirements, sequencing
- [Source: _bmad-output/implementation-artifacts/sprint-status.yaml] -- current data being migrated

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 5, 6 -> config-structure (direct)
- Task 4 -> specification (direct)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write the config or create the directory structure** per the story's acceptance criteria
2. **Verify by inspection:**
   - JSON files: must parse without error (validate with a JSON linter, `jq`, or IDE -- do not rely on manual visual inspection)
   - Required fields: each required field must be present with the correct type
   - Paths: all referenced paths must exist after creation
   - Version consistency: any version fields must be consistent with related version references
3. **Document** what was created in the Dev Agent Record

**No tests required** for pure config/structure changes.

**DoD items for config-structure tasks:**
- [ ] All JSON files parse without error (validated with a tool)
- [ ] All required fields present with correct types
- [ ] All referenced paths exist after creation
- [ ] Changes documented in Dev Agent Record

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (epic, PRD, or parent spec) -- not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per the story's acceptance criteria
2. **Verify cross-references:** All references to other documents, files, sections, or identifiers must resolve correctly. Check links, path references, and section names.
3. **Verify format compliance:** If the project has an established template or convention for this document type (e.g., ADR format, story frontmatter schema), confirm the output follows it.
4. **Document** what was written or updated in the Dev Agent Record

**No tests or evals required** for specification changes. AVFL checkpoint (run by momentum-dev) validates the spec against acceptance criteria.

**Additional DoD items for specification tasks:**
- [ ] All cross-references to other documents, files, or sections resolve correctly
- [ ] Document follows project template/format conventions if one exists
- [ ] AVFL checkpoint result documented (momentum-dev runs this automatically)

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
