---
title: "Semantic versioning v2 enforcement and momentum:version release skill"
story_key: semver-v2-version-release-skill
status: backlog
epic_slug: ad-hoc
feature_slug: 
story_type: feature
depends_on: []
touches:
  - .claude/rules/version-on-release.md
  - skills/momentum/skills/version/
---

# Semantic versioning v2 enforcement and momentum:version release skill

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want an explicit semver v2 rule and a `/version` skill that analyzes commits, determines the correct version bump, tags the release, and pushes to GitHub,
so that every release is versioned correctly per semver v2 with zero manual steps and no risk of over- or under-bumping.

## Description

Three parts in one story:

**Part 1 — Update version-on-release.md rule**
Explicitly adopt semantic versioning v2 (https://semver.org/spec/v2.0.0.html). Document the major version policy (what constitutes a breaking change for this plugin, what triggers 1.0.0). The rule currently describes minor/patch heuristics without naming the spec. It should reference semver v2 directly and clarify that breaking changes bump major even in 0.x territory.

**Part 2 — Build momentum:version skill**
A skill invocable as `/version` that automates the full release cycle:

1. Find the most recent git tag (last released version)
2. Collect all commits since that tag
3. Classify each commit by conventional commit prefix:
   - `feat:` or `feat(scope):` → minor bump candidate
   - `fix:` or `fix(scope):` → patch bump candidate
   - `BREAKING CHANGE:` in body, or `!` suffix (e.g. `feat!:`, `fix!:`) → major bump candidate
   - All other commits (chore, docs, refactor, style, ci, etc.) → ignored for versioning
4. Determine the single highest bump level across all commits
5. Apply exactly one increment to plugin.json:
   - major: increment MAJOR, reset MINOR=0, PATCH=0
   - minor: increment MINOR, reset PATCH=0 (MAJOR unchanged)
   - patch: increment PATCH only (MAJOR, MINOR unchanged)
6. Commit the plugin.json change with: `chore(plugin): bump version to X.Y.Z`
7. Create an annotated git tag: `vX.Y.Z`
8. Push all commits and the tag to GitHub: `git push && git push --tags`

**The core invariant:** Version is incremented exactly once per `/version` run, regardless of how many commits exist since the last tag. Three fix commits + one feat commit = one minor bump total. Never additive.

**Part 3 — Edge cases the skill must handle:**
- No commits since last tag → inform developer, do nothing
- No git tags exist → treat 0.0.0 as the baseline, first bump produces 0.1.0 (or 0.0.1 for pure fixes)
- Commits exist but none are conventional → inform developer no versioning commits found, do nothing
- Unpushed changes exist when skill runs → include them in the push
- GitHub remote not configured → halt with clear error before touching plugin.json

**Pain context:** Currently the release process is entirely manual — the developer must remember to bump plugin.json, write the commit with the right format, push, and tag. There is no explicit declaration of semver v2, no documented major version policy, and no protection against inconsistent bumping (e.g. bumping patch three times for three fix commits instead of once). The `/version` skill makes release a one-command operation.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `version-on-release.md` explicitly references semver v2 (https://semver.org/spec/v2.0.0.html)
- `version-on-release.md` documents the major version policy for this plugin
- `momentum:version` skill exists and is invocable as `/version`
- Skill finds the most recent git tag as the baseline version
- Skill classifies commits: `feat`→minor, `fix`→patch, `BREAKING CHANGE`/`!` suffix→major
- Non-conventional commits (chore, docs, refactor, etc.) are ignored for bump classification
- Exactly one version increment applied regardless of commit count — the highest classification wins
- Major bump: MAJOR+1, MINOR=0, PATCH=0
- Minor bump: MINOR+1, PATCH=0 (MAJOR unchanged)
- Patch bump: PATCH+1 (MAJOR, MINOR unchanged)
- `plugin.json` version field updated to new version
- Commit created: `chore(plugin): bump version to X.Y.Z`
- Annotated tag created: `vX.Y.Z`
- All commits and tag pushed to GitHub
- Edge case: no commits since last tag → no-op with clear message
- Edge case: no tags exist → baseline is 0.0.0
- Edge case: commits exist but none are conventional → no-op with clear message
- Edge case: no GitHub remote → halt before modifying plugin.json

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Architecture Compliance
_DRAFT_

### Testing Requirements
_DRAFT_

### Implementation Guide
_DRAFT_

### Project Structure Notes
_DRAFT_

### References

- Semantic Versioning 2.0.0: https://semver.org/spec/v2.0.0.html
- Conventional Commits: https://www.conventionalcommits.org/
- Current rule: `.claude/rules/version-on-release.md`
- Current plugin.json: `skills/momentum/.claude-plugin/plugin.json`

## Dev Agent Record

_DRAFT — populated by dev agent after create-story enrichment._

### Agent Model Used
### Debug Log References
### Completion Notes List
### File List
