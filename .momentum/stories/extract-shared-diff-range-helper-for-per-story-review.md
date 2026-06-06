---
title: Extract a shared diff-range reference/helper for per-story review
story_key: extract-shared-diff-range-helper-for-per-story-review
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Extract a shared diff-range reference/helper for per-story review

## Story
Document one vetted diff-range pattern and cite it from every per-story review call site, so the same merge-boundary diff bug stops being re-authored.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): the same HIGH `pre_merge_sha` merge-boundary diff bug was re-authored in 2 repoint stories (`code-review-adapter-repoint-sprint-dev`, `code-review-adapter-repoint-quick-fix`) plus a 3rd qa-reviewer variant (`main...HEAD` over-scoping); one took 3 attempts (two empty three-dot diffs) to converge. Independent re-derivation of the same fix is a strong signal the pattern should be bundled once.

## What's needed
- A single vetted diff-range pattern is documented once (capture `pre_merge_sha` at the merge point; two-dot `{{pre_merge_sha}}..story/{slug}`) and cited by every per-story review call site.
- Fixes are validated against the workflow's concrete merge mechanics (rebase-then-ff), not the abstract git model.

## References
- Retro findings (v2): `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related: `code-review-adapter-repoint-sprint-dev`, `code-review-adapter-repoint-quick-fix`, `qa-reviewer-rescope-per-story-contract`
