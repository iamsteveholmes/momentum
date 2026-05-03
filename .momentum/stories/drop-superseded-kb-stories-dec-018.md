---
title: Drop Superseded KB Stories — DEC-018 Wiki Skills Replace KB/Vault Story Suite
story_key: drop-superseded-kb-stories-dec-018
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-practice-knowledge-base
story_type: maintenance
depends_on: []
touches: []
---

# Drop Superseded KB Stories — DEC-018 Wiki Skills Replace KB/Vault Story Suite

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to transition superseded KB/vault backlog stories to "dropped" status with a DEC-018 reference,
so that the backlog accurately reflects which stories are no longer needed following the installation of the Obsidian wiki skill suite.

## Description

DEC-018 (dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md) decided that the installed Obsidian wiki skill suite supersedes six KB/vault stories that were previously in the backlog. These stories described capabilities that the wiki skills already provide:

- `kb-init` — superseded by `wiki-setup`
- `kb-ingest` — superseded by `wiki-ingest`
- `kb-raw-ingest-spike` — superseded by installed wiki skills
- `vault-claudemd-navigation-contract-spec` — superseded by wiki skill suite contracts
- `vault-indexmd-registry-format-and-update-protocol` — superseded by wiki skill suite
- `wiki-page-schema-and-frontmatter-formalization` — superseded by wiki skill suite

This maintenance task updates `stories/index.json` to mark all six stories as `dropped`, records the superseding decision (DEC-018) in each entry, and removes any sprint references. No story files need to be deleted — the records simply transition status.

**Pain context:** Stale backlog stories with `backlog` status create false planning signals — they appear as work to be done when the decision has already been made to drop them. DEC-018 was recorded 2026-05-03 and the stories haven't been updated, so any sprint-planning or feature-status run will surface them as open work. Left unresolved, these will recur as noise in every planning cycle.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- All six stories (`kb-init`, `kb-ingest`, `kb-raw-ingest-spike`, `vault-claudemd-navigation-contract-spec`, `vault-indexmd-registry-format-and-update-protocol`, `wiki-page-schema-and-frontmatter-formalization`) have `status: dropped` in `stories/index.json`
- Each dropped entry includes a `dropped_reason` field or note citing DEC-018 as the superseding decision
- No sprint references remain on any of the six entries
- `momentum-tools` or `sprint story-add` are used to update entries (not direct JSON edits outside the tool)
- Feature status report no longer surfaces these stories as open/planned work

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. This section MUST be populated by
     create-story, which will break down the work based on architecture analysis and
     implementation guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture analysis,
     implementation guide, technical requirements, and Momentum-specific guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

<!-- DRAFT: Architecture compliance has not been assessed for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

<!-- DRAFT: Testing requirements have not been defined for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

<!-- DRAFT: No implementation guide has been generated. Create-story will inject
     Momentum-specific guidance based on change-type classification. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Key reference: `dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md` — the decision document that authorizes these drops.

The `momentum-tools.py sprint story-add` command does not yet support a `status: dropped` transition; the dev agent should check whether a `story-drop` subcommand exists or whether direct momentum-tools invocation handles this, and document the approach in the implementation guide.

### Project Structure Notes

<!-- DRAFT: File paths, skill directories, and structural alignment have not been
     analyzed. Create-story will populate this based on the relevant epic and
     existing codebase structure. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Affected file: `.momentum/stories/index.json`

### References

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Decision: `_bmad-output/planning-artifacts/decisions/dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md`
- Stories to drop: `kb-init`, `kb-ingest`, `kb-raw-ingest-spike`, `vault-claudemd-navigation-contract-spec`, `vault-indexmd-registry-format-and-update-protocol`, `wiki-page-schema-and-frontmatter-formalization`

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
