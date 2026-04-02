---
story_id: p1.4
status: done
type: process
epic: P1 — Process Sprint-1
title: Lightweight Story Status Update Tool
sprint: 1
touches:
  - "skills/momentum/scripts/"
  - "skills/momentum-plan-audit/workflow.md"
  - "skills/momentum-dev/workflow.md"
  - ".claude/skills/bmad-dev-story/workflow.md"
  - "skills/momentum-create-story/workflow.md"
  - "_bmad-output/planning-artifacts/architecture.md"
depends_on:
  - p1-1-remove-git-mcp-server-dependency
---

# Lightweight Story Status Update Tool

## User Story

As a Momentum developer,
I want story statuses to stay synchronized between sprint-status.yaml and story file frontmatter,
So that status tracking remains accurate regardless of which workflow path executes the work.

## Background

Story statuses in sprint-status.yaml and story file frontmatter drift apart. Process stories created by momentum-plan-audit get implemented during plan execution (outside momentum-dev), so no status transitions fire. Even product stories going through momentum-dev only update sprint-status.yaml, never story file frontmatter. Additionally, story file frontmatter uses `status: ready` while sprint-status.yaml uses `ready-for-dev` — inconsistent terminology.

## Acceptance Criteria

Given a valid story key and status,
When `update-story-status.sh <story-key> <status>` is called,
Then both sprint-status.yaml development_status and story file frontmatter status are updated to the given status.

Given the same status update is run twice,
When the second run executes,
Then it exits 0 with no duplicate edits (idempotent).

Given momentum-plan-audit creates a substantive process story,
When the plan executes and completes,
Then status transitions (in-progress → review → done) are injected into the plan and executed via the script.

Given momentum-dev or bmad-dev-story runs a product story,
When status transitions occur,
Then both sprint-status.yaml and story file frontmatter are updated via the centralized script.

## Definition of Done

- [ ] `skills/momentum/scripts/update-story-status.sh` — centralized dual-file status update script
- [ ] `skills/momentum-plan-audit/workflow.md` — injects status transition steps into substantive plans
- [ ] `skills/momentum-dev/workflow.md` — replaces inline status edits with script calls
- [ ] `.claude/skills/bmad-dev-story/workflow.md` — replaces inline status edits with script calls
- [ ] `skills/momentum-create-story/workflow.md` — uses `ready-for-dev` not `ready` in frontmatter

## Dev Notes

**Change types:**
- `skills/momentum/scripts/update-story-status.sh` → `script-code`
- `skills/momentum-plan-audit/workflow.md` → `skill-instruction`
- `skills/momentum-dev/workflow.md` → `skill-instruction`
- `.claude/skills/bmad-dev-story/workflow.md` → `skill-instruction`
- `skills/momentum-create-story/workflow.md` → `skill-instruction`
