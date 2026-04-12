---
title: Retro Transcript Extraction Hardening — Worktree Path Resolution and UTC Boundary Fix
story_key: retro-transcript-extraction-hardening
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Retro Transcript Extraction Hardening — Worktree Path Resolution and UTC Boundary Fix

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a retro workflow,
I want correctly resolve worktree paths and UTC day boundaries when extracting sprint session transcripts,
so that retro transcript analysis includes all sessions from the sprint, not just those in the main checkout path.

## Description

The retro transcript extraction misses sessions that ran in git worktrees (separate checkout directories). Additionally, sessions that span UTC midnight are attributed to the wrong sprint day. Also fixes a DuckDB serialization bug (repr vs json.dumps) that corrupts extracted data. Without this, retro analysis has partial coverage and produces misleading findings.

**Pain context:** Discovered in sprint-2026-04-08 retro. The worktree issue meant entire sprint stories were invisible to the transcript audit. UTC boundary issue caused ~1-3 sessions per sprint to be miscounted. DuckDB repr bug corrupted JSON-valued columns silently.

**Additional evidence (nornspun sprint-04-10 retro, 2026-04-12):** Three more issues folded in from this retro:

*Transcript path discovery (issue #7):* The retro skill's Phase 2 step referenced a relative path (`skills/momentum/scripts/`) that didn't exist in the working directory. User had to manually direct discovery, including pointing to the claude-code-guide agent and specifying global directories. The canonical script path is `~/.claude/plugins/cache/momentum/momentum/<version>/scripts/transcript-query.py` and should be resolved dynamically (glob for latest version).

*Sprint window alignment (issue #8):* The retro extract window for sprint-2026-04-10 captured sprint-04-08 execution and sprint-04-10 planning, but not sprint-04-10 dev execution. The HTTP/2 ktor fix, InMemoryAppPrefs AVFL catch, and quick-fix — the sprint's substantive development events — were entirely absent from the corpus. Root cause: same-day sprints (started and completed 2026-04-11) require the preprocessing to scope extraction to sessions containing the sprint's story slugs, not just date ranges. Recommend: DuckDB query filtering for messages mentioning story slugs to identify relevant sessions, OR sprint-dev Phase 7 writes session file IDs to the sprint index at close time.

*Large-file reads in long-lived agents (issue #10):* 106 of 238 tool errors (44%) in the retro were file-too-large variants. Affected agents: documenter, auditor, spec-impact-discovery. Affected files: agent-summaries.jsonl, errors.jsonl, prd.md, architecture.md, stories/index.json. Recovery worked but wasted 12+ turns per agent. Fix: encode peek-first convention (wc -l, then read in 500-line chunks) in the documenter and auditor agent prompts for known-large files.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Transcript extractor resolves worktree checkout paths (not just main repo path)
- UTC day boundaries handled correctly when attributing sessions to sprints
- DuckDB json.dumps used for JSON-valued columns (not repr)
- Extraction produces consistent results whether sessions ran in main or worktree

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

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
