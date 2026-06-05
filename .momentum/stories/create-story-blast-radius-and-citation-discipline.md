---
title: Harden create-story blast-radius and citation discipline
story_key: create-story-blast-radius-and-citation-discipline
status: backlog
epic_slug: momentum-backlog-refinement
story_type: feature
priority: high
depends_on: []
---

# Harden create-story blast-radius and citation discipline

## Story
create-story must scan for the full blast radius of a change (all sections/files duplicating the text being changed) and forbid cite-by-number into unopened spec sections.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): three high-severity findings originated in story authoring, not dev. `dev-strip-merge-cleanup-authority` cited spec section 12 (a file inventory) five times for rationale that actually lives in section 6 — seeded by the story's own Dev Notes ("cited by number from the brief — not opened") — and omitted SKILL.md from its touches list, leaving a stale public description advertising the worktree creation being removed. `conduct-spec-revision-dec036` scoped to §1/§4/§8/§9 while the absolutism it relaxed was duplicated across §2/§3/§6/§10. The dev faithfully propagated each spec defect.

## What's needed
- create-story runs a blast-radius scan that finds all sections/files duplicating the text being changed and adds them to scope/touches.
- Cite-by-number is forbidden unless the referenced section is opened and verified.
- The touches list is validated against the actual surfaces the change invalidates (e.g. public SKILL.md descriptions).

## References
- Retro findings: `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related (dedup, adjacent — different concerns): `create-story-update`, `create-story-advanced-elicitation`, `inject-constitution-md-path-into-create-story-flesh-out-prompts`. NOTE: `dag-dispatch-blast-radius-discovery` reuses the term "blast-radius" but is about DAG dispatch host resolution — not this.
