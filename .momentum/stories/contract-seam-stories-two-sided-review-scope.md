---
title: Give contract/seam stories a two-sided (producer + consumer) review scope
story_key: contract-seam-stories-two-sided-review-scope
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Give contract/seam stories a two-sided (producer + consumer) review scope

## Story
A story that defines a contract between two agents must declare BOTH sides as review scope, and the per-story gate must check field-shape compatibility across both sides — not only the produced artifact.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): `directed-fix-invocation-contract` passed its in-story document-review in isolation but needed two post-merge AVFL commits (8032578, 36712a6) to define `finding_id`, add join-back semantics, and codify the nested `timing_tier` seam — the same shape as the single escalated card ("the fixer and the Conductor built incompatible halves of the same hand-off contract"; `F.escalation.timing_tier` nested vs `F.timing_tier` flat made the routing branch unreachable). The per-story document-review gate is scoped to one artifact while the contract is inherently a multi-file seam.

## What's needed
- Stories that define a contract between two agents declare both sides (producer + consumer) as review scope.
- The per-story gate checks field-shape compatibility across both sides, not only the produced artifact.

## References
- Retro findings: `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related (dedup, adjacent): `sprint-planning-frozen-per-story-contract-holistic-coverage` (done), `qa-reviewer-rescope-per-story-contract` (done), `avfl-cross-story-integration-lens`
