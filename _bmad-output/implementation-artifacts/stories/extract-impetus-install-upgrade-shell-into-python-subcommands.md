---
title: Extract Impetus install / upgrade / hash-drift shell work into Python subcommands
story_key: extract-impetus-install-upgrade-shell-into-python-subcommands
status: backlog
epic_slug: impetus-core
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# Extract Impetus install / upgrade / hash-drift shell work into Python subcommands

<!-- INTAKE STUB -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready._

## Story

As a developer,
I want the Impetus `workflow.md` install / upgrade / hash-drift sections to call Python subcommands that do the shell work, instead of driving shell commands turn-by-turn through the LLM,
so that `workflow.md` shrinks back under budget, first-install and upgrade are fast and deterministic, and the agent spends tokens on reasoning rather than mutation.

## Description

Quality analysis flagged `workflow.md` as over-budget (currently 626 lines) and
observed that ~3500–5000 tokens are spent driving shell mutations through the
LLM across the install / upgrade / hash-drift flows. This is LLM-tax shell work:
deterministic operations (copying files, writing `installed.json`, computing
hashes, resolving version chains, mutating `.gitignore` with a regex) encoded as
natural-language step instructions. The LLM re-derives the same logic each
session and occasionally gets it wrong.

Proposed script extensions:
- `momentum-tools install execute` — perform the concrete install actions (copy files, set up `installed.json`, etc.) given a resolved action list
- `momentum-tools install record` — write the `installed.json` state atomically after a successful install/upgrade
- `momentum-tools install upgrade-plan` — resolve the full version chain between `installed_version` and `current_version` and return the ordered action list
- `momentum-tools install ensure-gitignore-tracking` — idempotent `.gitignore` regex mutation
- Extend preflight `hash_drift` payload so Step 10 of `workflow.md` does not need to re-run `git hash-object`
- Pre-render the `feature_status` line and journal-hygiene warning inside the preflight script (currently rendered LLM-side)

Also:
- Step 1 of `workflow.md` is ~40 lines of preamble that duplicates what the preflight already performed — replace with a one-paragraph note pointing to preflight
- Migration instruction files (natural-language-for-LLM) should be converted to Python migration modules per version

Expected outcome: `workflow.md` drops substantially below 500 lines; install/upgrade flows complete with fewer tool calls and less narration; migration behavior becomes testable in Python.

**Pain context:** Quality analysis (bmad-agent-builder, 2026-04-19, finding M4) classed this as MEDIUM but noted it's multi-day work. Primary benefit is testability and speed; secondary is LLM-token efficiency. Not user-visible warmth work — purely infrastructure cleanup — but unblocks future Impetus UX work by making `workflow.md` easier to reason about.

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `momentum-tools install execute` exists and is covered by unit tests
- `momentum-tools install record` exists and is covered by unit tests
- `momentum-tools install upgrade-plan` returns an ordered action list across the full version chain, covered by unit tests
- `momentum-tools install ensure-gitignore-tracking` is idempotent and unit tested
- `momentum-tools session startup-preflight` hash-drift payload is extended so Step 10 does not call `git hash-object` directly
- `momentum-tools session startup-preflight` pre-renders `feature_status` line and journal-hygiene warning strings
- `skills/momentum/skills/impetus/workflow.md` is reduced below the skill-length budget (≤500 lines) by delegating to the new subcommands
- Step 1 preamble is reduced to a one-paragraph reference to preflight
- Migration instruction files are converted to Python migration modules where appropriate
- First-install + upgrade flows pass existing evals (`eval-first-install-consent-and-execution`, `eval-multi-version-sequential-upgrade`, `eval-hash-drift-warning`, `eval-install-uses-bash-not-write`, etc.)

> Note: Rough starting points — create-story will validate.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Architecture Compliance

_DRAFT._

### Testing Requirements

_DRAFT._

### Implementation Guide

_DRAFT._

### Project Structure Notes

_DRAFT._

### References

Origin: bmad-agent-builder quality analysis report, `_bmad-output/reports/impetus/quality-analysis/2026-04-19-141047/quality-report.md`, opportunity M4 "workflow.md is over-budget and full of LLM-tax shell work that belongs in a script."

## Dev Agent Record

_DRAFT._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
