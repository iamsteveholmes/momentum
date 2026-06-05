---
title: Key the retro audit-extract harvest on the build session IDs
story_key: retro-audit-extract-harvest-keys-on-build-session-id
status: backlog
epic_slug: momentum-sprint-retro
story_type: defect
priority: high
depends_on: []
---

# Key the retro audit-extract harvest on the build session IDs

## Story
The retro Phase 2 audit-extract harvest must select sessions by the sprint's concrete build session IDs, not by date-range + story-slug mention (which can capture the wrong wave).

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): `team-messages.jsonl` was empty and all 7 `agent-summaries.jsonl` records were from the 2026-05-31 assessment / planning wave, not the 2026-06-04 conduct build. The build artifacts (build-results.jsonl, finding-cards.json, story-diffs.json) came from a session whose transcript was absent from the extracts. A reviewer working only from these extracts has zero visibility into the build. This was caught live during the dynamic-workflow retro dogfood — the recorded sprint `started` date also undercounted the real build span (06-01→06-04 vs recorded 06-03).

`retro-transcript-extraction-hardening` (done) already added slug-membership filtering (its AC5), but slug-mention is too coarse: sessions from a prior wave that referenced the same slugs were harvested instead of the build sessions. This story extends that work with build-session-ID keying.

## What's needed
- Audit-extract selection is keyed to the sprint's build session IDs (captured at conductor/dev spawn time), with date/slug as fallback — not the prior planning wave.
- The harvest validates that captured agents/team-messages temporally overlap the build artifacts before filing.
- An empty `team-messages.jsonl` raises a harvest warning rather than silently producing an empty extract.
- (Related) sprint records should carry an accurate `started` reflecting the actual build span.

## References
- Retro findings: `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Extends: `retro-transcript-extraction-hardening` (done — AC5 slug-membership filter); related `retro-pipeline-idempotency`, `retro-session-analytics-phase-0`
