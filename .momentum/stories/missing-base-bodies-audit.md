---
title: Missing Base Bodies Audit — Verify DEC-020 Universal Agent Role Coverage
story_key: missing-base-bodies-audit
status: ready-for-dev
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: exploration
change_type: specification
depends_on: []
touches:
  - skills/momentum/agents/
  - .momentum/stories/
---

# Missing Base Bodies Audit — Verify DEC-020 Universal Agent Role Coverage

## Story

As a developer,
I want a one-time audit that confirms all 9 DEC-020 base body roles either have a file in `skills/momentum/agents/` or have a tracked story with a known slug,
so that I can verify universal agent model compliance with zero untracked gaps.

## Description

DEC-020 (2026-05-16) established nine canonical base body roles: architect, pm, ux, analyst, researcher, dev, sm, qa, e2e. This audit cross-references those nine roles against (a) files that exist in `skills/momentum/agents/` and (b) open stories in `.momentum/stories/`. It produces a gap report and closes when the gap count of untracked roles reaches zero.

This is a verification story, not an implementation story. It produces a gap report (written inline in the Dev Agent Record), not a new file. The audit can be completed without running any builds — it is a read-and-compare operation.

**Pre-run findings (as of 2026-05-16):**

Files in `skills/momentum/agents/` (excluding `evals/`):

| File | Role |
|---|---|
| dev.md | dev |
| dev-build.md | dev (specialization) |
| dev-frontend.md | dev (specialization) |
| dev-skills.md | dev (specialization) |
| e2e-validator.md | e2e |
| qa-reviewer.md | qa |

Roles with no file:

| Role | Tracked Story | Status |
|---|---|---|
| architect | architect-base-body | backlog |
| pm | pm-base-body | backlog |
| sm | sm-base-body | backlog |
| ux | ux-base-body | backlog |
| analyst | analyst-base-body | backlog |
| researcher | researcher-base-body | backlog |

All 6 missing roles have tracked backlog stories. Untracked gap count: **0**.

The roles closed by DEC-020 (code-reviewer, architect-guard, documenter, dev-fixer) have no files and no open stories, which is correct — they were explicitly closed by DEC-020 D2–D4.

## Acceptance Criteria

1. The dev agent reads `skills/momentum/agents/` and enumerates all `.md` files present (excluding `evals/`).
2. The dev agent reads all 9 required roles from DEC-020 (architect, pm, ux, analyst, researcher, dev, sm, qa, e2e) and compares against the files found.
3. For each role with no file, the dev agent confirms a tracked story exists in `.momentum/stories/index.json`.
4. The gap report is written to the Dev Agent Record below, listing covered roles, missing roles, and their story slug (or flagging any untracked gaps).
5. The story closes with a confirmed untracked gap count of 0. If any untracked gap is found, the dev agent creates an intake stub before closing.

## Tasks / Subtasks

- [ ] Read `skills/momentum/agents/` — enumerate all `.md` files excluding `evals/`
- [ ] Compare against the 9 DEC-020 required roles and produce a covered/missing table
- [ ] For each missing role, confirm a tracked story exists in `.momentum/stories/index.json`; flag any without a story
- [ ] Write the gap report to the Dev Agent Record
- [ ] If untracked gaps exist, call `momentum:intake` to stub a story before closing

## Dev Notes

### Audit Methodology

1. `ls skills/momentum/agents/*.md` — collect present files
2. Map filenames to canonical role names using this table:

   | Filename prefix | Canonical role |
   |---|---|
   | dev.md, dev-*.md | dev |
   | e2e-*.md | e2e |
   | qa-*.md | qa |
   | architect*.md | architect |
   | pm*.md | pm |
   | sm*.md | sm |
   | ux*.md | ux |
   | analyst*.md | analyst |
   | researcher*.md | researcher |

3. Compare against the 9 canonical roles from DEC-020.
4. For each missing role, `grep <story_key> .momentum/stories/index.json` to confirm tracked.

### Architecture Compliance

DEC-020 is the authoritative source of truth for the 9 required roles. Do not consult DEC-013 or DEC-016 directly — DEC-020 supersedes the taxonomy portions of those decisions.

The four closed roles (code-reviewer, architect-guard, documenter/retro-synthesizer, dev-fixer) should have no files and no open stories. If files exist for these roles, flag them as cleanup candidates — do not delete them in this story.

### Testing Requirements

This is a read-only audit story. No tests required. The gap report in the Dev Agent Record is the deliverable.

### References

- DEC-020: `_bmad-output/planning-artifacts/decisions/dec-020-universal-agent-role-taxonomy-2026-05-16.md`
- Agents directory: `skills/momentum/agents/`
- Stories index: `.momentum/stories/index.json`
- Handoff with prior findings: `.momentum/handoffs/agent-architecture-triage-2026-05-16.md`

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### Gap Report

_Populated by dev agent during execution._

### File List

_No files created or modified by this story — read-only audit._
