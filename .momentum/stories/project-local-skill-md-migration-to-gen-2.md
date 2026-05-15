---
title: Project-Local SKILL.md Migration to Gen-2 Composed Agent Files
story_key: project-local-skill-md-migration-to-gen-2
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: maintenance
depends_on:
  - build-guidelines-skill
  - constitution-builder-write-mode-parameterization
  - sprint-dev-composed-file-spawn-wiring
touches:
  - nornspun-client/.claude/skills/frontend-dev/SKILL.md
  - nornspun-client/.claude/guidelines/agents/dev-kotlin-compose.md
---

# Project-Local SKILL.md Migration to Gen-2 Composed Agent Files

<!-- INTAKE STUB: Captured during feature-grooming pass 2026-05-12. Run
     momentum:create-story to enrich before development. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a documented migration path from project-local `.claude/skills/{role}-{domain}/SKILL.md` prototypes to gen-2 composed agent files at `.claude/guidelines/agents/{role}-{domain}.md`,
so that hand-rolled experimental skills (like nornspun-client's `frontend-dev`) are retired cleanly once `build-guidelines` can produce equivalent or better composed bodies.

## Description

Several project-local SKILL.md files exist today as hand-rolled prototypes of what gen-2 composed agents will produce. The clearest example: `nornspun-client/.claude/skills/frontend-dev/SKILL.md` — author-built with `## Permissions` + `## Standing Rules` + `## Quick Routing` sections, validated via benchmark (2026-05-09 to 2026-05-10) to confirm the wiki-query preflight pattern works.

Once `build-guidelines-skill` ships, the project-local prototypes become **redundant** — `build-guidelines` will produce `.claude/guidelines/agents/dev-kotlin-compose.md` from the same plugin base body + nornspun's project manifest, generating the same kind of constitution sections via `constitution-builder`. Without an explicit migration story, the two systems will live in parallel and developers will not know which one sprint-dev actually consumes.

This story documents the migration:

1. Identify all project-local SKILL.md files that are gen-2 precursors
2. Run `build-guidelines` against each affected project to produce the equivalent composed agent file
3. Diff the generated composed body against the hand-rolled SKILL.md content
4. Reconcile any drift (the hand-rolled version may have improvements that need to be folded into the agent manifesto or KB)
5. Retire the project-local SKILL.md (or convert it into a thin pointer that says "see .claude/guidelines/agents/...")
6. Update any callers (slash-command users, sprint-dev wiring) to point to the composed file

**Pain context:** The benchmark work we did on `frontend-dev` SKILL.md validated the wiki-query preflight pattern that build-guidelines will produce. Without a migration story, that prototype will sit indefinitely, drift from the gen-2 output, and confuse future developers about which file is the "real" frontend-dev agent.

## Known Affected Prototypes

- `nornspun-client/.claude/skills/frontend-dev/SKILL.md` — validated 2026-05-09 to 2026-05-10; first migration candidate

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Rough draft ACs:

- A documented migration procedure exists (in the build-guidelines workflow.md or a separate reference doc)
- The procedure includes: discovery, generation, diff, reconcile, retire, update-callers
- For each known affected prototype, the migration is executed and the project-local SKILL.md is removed (or converted to a pointer)
- The generated composed file passes the same benchmark suite that validated the project-local prototype (regression safety)
- No active sprint-dev workflow references the retired project-local SKILL.md path

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- `build-guidelines-skill` story (the generator that produces the replacement)
- `constitution-builder-write-mode-parameterization` story (enables composed_agent_file mode)
- `sprint-dev-composed-file-spawn-wiring` story (the consumer that needs the migrated file)
- Benchmark report (forthcoming) — frontend-dev wiki-query preflight validation 2026-05-09 to 2026-05-10

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._
