---
title: Widen document-review verification to scan the whole document for contradictions
story_key: widen-document-review-whole-doc-contradiction-scan
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: critical
depends_on: []
---

# Widen document-review verification to scan the whole document for contradictions

## Story
The document-review verification method must scan the entire document for contradictions against the changed claims — not only the story-named sections.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): on `conduct-spec-revision-dec036` the document-review QA verifier returned PASS (18/18 claims verified, all 5 named sections present) on the same dev-pass diff where the parallel adversarial reviewer found 1 critical + 2 contradictions in sections the story did **not** name (§2/§3/§6/§10). The claim-checklist is structurally blind outside story-named sections; only the adversarial reviewer caught the cross-section contradictions. Without it a self-contradicting spec would have shipped.

## What's needed
- For document-review stories, adversarial review is mandatory and non-skippable.
- The claim-checklist scans the full document for contradictions against the changed claims, not only the story-named sections.
- A QA PASS is invalid if a parallel adversarial reviewer returns critical findings on the same diff.

## References
- Retro findings: `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related (dedup, converge rather than duplicate): `architecture-guard-cross-section-check` (adjacent — architecture-edit coherence), `qa-reviewer-rescope-per-story-contract` (done — narrows scope per-story; this widens the verifier)
