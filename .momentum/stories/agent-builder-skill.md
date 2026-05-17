---
title: agent-builder-skill
story_key: agent-builder-skill
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-composition-pipeline
story_type: feature
depends_on: []
touches: []
---

# agent-builder-skill

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a per-agent composer skill that accepts base_body, manifesto context, and permissions scope to produce a composed Tier 2 agent file and a matching agents.json routing entry,
so that build-agents can orchestrate one composition pass per role × domain pair without bespoke composition logic.

## Description

New skill: per-agent composer (base_body + manifesto + permissions → composed agent file + routing entry). Wraps skill-creator with an agent-specific template. This is the skill that runs for each role × domain pair to produce a composed Tier 2 agent file and a matching entry in momentum/agents.json. build-agents orchestrates agent-builder once per role × domain pair. Per DEC-026 D2, this replaces the old build-guidelines skill's composition responsibilities. Accepts: base_body_path, project_manifesto_context, permissions_scope → outputs: composed agent file + agents.json routing entry. The constitution-builder narrows to domain knowledge only; routing moves here.

**Pain context:** Per DEC-026 D2, composition responsibilities currently scattered across build-guidelines and related skills need a single dedicated composer skill. Without this, build-agents has no clean delegation target and the constitution-builder carries responsibilities it shouldn't. Source: triage handoff agent-architecture-triage-2026-05-16.md.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Given base_body_path, project_manifesto_context, and permissions_scope inputs, when agent-builder-skill runs, then it produces a composed Tier 2 agent file at the expected output path
- Given the above inputs, when agent-builder-skill runs, then it writes a matching routing entry into momentum/agents.json
- Given build-agents orchestrating multiple role × domain pairs, when it invokes agent-builder-skill once per pair, then each invocation is independent and produces correct output
- Given the new skill, when the constitution-builder is reviewed, then its composition responsibilities have been removed and it handles domain knowledge only
- Given the new skill wraps skill-creator, when it runs, then it uses an agent-specific template appropriate for Tier 2 agent composition

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

### Project Structure Notes

<!-- DRAFT: File paths, skill directories, and structural alignment have not been
     analyzed. Create-story will populate this based on the relevant epic and
     existing codebase structure. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- DEC-026 D2 — agent-architecture-triage-2026-05-16.md (triage source)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6 (dev-skills specialist)

### Debug Log References

None — implementation proceeded directly from DEC-026 D3 and DEC-027 D3 decision documents.

### Completion Notes List

- Story was an intake stub; enriched in-place from DEC-026 D3 (agent-builder decision) and agent-architecture-triage-2026-05-16.md
- Created SKILL.md with correct frontmatter: user-invocable, allowed-tools, model=sonnet, effort=medium
- Created workflow.md with 4-phase execution: Elicit → Compose → Validate via skill-creator → Write outputs
- Workflow follows DEC-026 D3 inputs (base_body_path, constitution excerpt, manifesto_context, permissions_scope)
- Workflow outputs composed Tier 2 agent file at `.claude/guidelines/agents/{role}-{domain}.md` and routing entry in `momentum/agents.json`
- Large File Handling section mandated in all composed agent files (per agent-skill-development-guide.md convention)
- skill-creator validation gate included in Phase 3 with fallback manual checklist

### File List

- `skills/momentum/skills/agent-builder/SKILL.md` (created)
- `skills/momentum/skills/agent-builder/workflow.md` (created)
