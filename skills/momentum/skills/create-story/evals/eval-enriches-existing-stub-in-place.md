# Eval: Enriches an existing Momentum slug-stub in place (does not create-from-epic)

## Scenario

Given an existing Momentum story file `.momentum/stories/build-guidelines-skill.md` that is an
intake stub — it already contains a rich `## Description`, DRAFT `## Acceptance Criteria` with
decision references (e.g., DEC-038 AC1–AC4), a `### References` subsection, and frontmatter:

```yaml
---
title: "Build-Guidelines Skill — Gen-2 Agent Guidelines"
story_key: build-guidelines-skill
status: backlog
epic_slug: agent-team-model            # STALE — left over from an epic move
depends_on:
  - constitution-builder-write-mode-parameterization
touches:
  - skills/momentum/skills/build-guidelines/SKILL.md
---
```

And `.momentum/stories/index.json` has an entry for `build-guidelines-skill` with
`epic_slug: momentum-agent-composition-pipeline` (the authoritative value), and `epics.json`
contains a record keyed by `momentum-agent-composition-pipeline` but **no** record for
`agent-team-model`.

The skill `momentum:create-story` is invoked on `build-guidelines-skill`.

## Expected behavior

The skill should select **enrich mode** (not create-from-epic) and enrich the story IN PLACE:

1. It detects `.momentum/stories/build-guidelines-skill.md` already exists and sets mode = enrich.
2. It does **NOT** invoke `bmad-create-story` and does **NOT** initialize the file from a template
   or relocate it — the existing Description, decision-referenced ACs, and References are preserved.
3. It reconciles epic membership from the authoritative index: `epic_slug` becomes
   `momentum-agent-composition-pipeline` (the index value), and the stale frontmatter
   `agent-team-model` is corrected to match. The epic-record lookup therefore succeeds rather
   than halting on a missing `agent-team-model` epic.
4. It rewrites the DRAFT acceptance criteria into validated, testable, observable ACs (preserving
   their intent and decision references) and removes "DRAFT" / "INTAKE STUB" markers.
5. It adds a `## Tasks / Subtasks` breakdown and populates `## Dev Notes`, preserving the existing
   `### References`.
6. It classifies change types and writes `change_type` to the story **frontmatter as a YAML list**.
7. It writes `change_type` to **`stories/index.json` as a string** (e.g.,
   `"skill-instruction"`), so `momentum-tools sprint compute-verification-method` returns a real
   method rather than the empty-change_type fallback `document-review`.
8. The pre-existing `depends_on` edge (`constitution-builder-write-mode-parameterization`) survives
   into the index entry — it is unioned, never dropped in favor of an epic-derived `[]`.
9. Frontmatter `status` becomes `ready-for-dev`.

## What This Tests

- Enrich vs create mode selection keys off whether the slug-story file already exists
- Existing rich content (Description, decision-referenced ACs, References) is preserved, not overwritten
- Stale `epic_slug` frontmatter is self-healed from the authoritative index
- `change_type` lands in BOTH frontmatter (list) and index (string) so downstream routing works
- A real `depends_on` edge declared in the story file is never lost during indexing

## Notes

This eval realizes the create-vs-enrich contract added to Step 1 of the workflow, the change_type
persistence added to Steps 4 and 7, and the depends_on/touches union added to Step 7. If that
mode-selection or persistence logic changes, update this eval in lockstep.
