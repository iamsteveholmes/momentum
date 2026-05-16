---
title: "Semantic versioning v2 enforcement and momentum:release skill"
story_key: semver-v2-version-release-skill
status: backlog
epic_slug: ad-hoc
feature_slug: 
story_type: feature
depends_on: []
touches:
  - .claude/rules/version-on-release.md
  - skills/momentum/skills/release/
---

# Semantic versioning v2 enforcement and momentum:release skill

<!-- INTAKE STUB: This story was captured by momentum:intake and scope-expanded via
     distill (sprint-2026-04-27 retro). It is a conversational stub, NOT a dev-ready
     story. All sections below marked DRAFT require full rewrite by create-story before
     any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want an explicit semver v2 rule and a `momentum:release` skill that analyzes commits, determines the correct version bump, updates plugin.json, commits the change, and asks me before pushing,
so that every release is versioned correctly per semver v2 with zero manual steps and a clear human gate before the push.

## Description

Two parts in one story:

**Part 1 — Update version-on-release.md rule**
Explicitly adopt semantic versioning v2 (https://semver.org/spec/v2.0.0.html). Document the major version policy (what constitutes a breaking change for this plugin, what triggers 1.0.0). The rule currently describes minor/patch heuristics without naming the spec. It should reference semver v2 directly and clarify that breaking changes bump major even in 0.x territory.

**Part 2 — Build momentum:release skill**
A skill invocable as `/momentum:release` that automates the complete release UX in exactly four steps:

**Step 1 — Compute semver bump**
Collect all commits since the last release (use the most recent `chore(plugin): bump version` commit as the baseline, or plugin.json current version if no such commit exists).
Classify each commit by conventional commit prefix:
- `feat:` or `feat(scope):` → minor bump candidate
- `fix:` or `fix(scope):` → patch bump candidate
- `BREAKING CHANGE:` in body, or `!` suffix (e.g. `feat!:`, `fix!:`) → major bump candidate
- All other commits (chore, docs, refactor, style, ci, etc.) → ignored for versioning

Determine the single highest bump level across all commits. Apply exactly one increment:
- major: increment MAJOR, reset MINOR=0, PATCH=0
- minor: increment MINOR, reset PATCH=0 (MAJOR unchanged)
- patch: increment PATCH only (MAJOR, MINOR unchanged)

Present the computed bump to the developer with a summary of the commits that drove it.

**Step 2 — Update plugin.json**
Write the new version string to `skills/momentum/.claude-plugin/plugin.json`.

**Step 3 — Create git commit**
Stage and commit the plugin.json change:
`chore(plugin): bump version to X.Y.Z — brief description`

**Step 4 — Ask developer before pushing**
Show the developer the commits that will be pushed (`git log @{u}..HEAD --oneline`).
Ask: "Push to remote? (Y/N)"
Only push if the developer explicitly confirms. **Push always requires approval — never push automatically.**

**The core invariant:** Version is incremented exactly once per `/momentum:release` run, regardless of how many commits exist since the last release. Three fix commits + one feat commit = one minor bump total. Never additive.

**Edge cases the skill must handle:**
- No commits since last release → inform developer, do nothing
- Commits exist but none are conventional → inform developer no versioning commits found, do nothing
- Unpushed changes exist when skill runs → they will be included in the push summary shown to developer
- GitHub remote not configured → halt with clear error before touching plugin.json
- Developer declines push → commits remain local; inform developer they can push manually when ready

**Pain context:** Currently the release process is entirely manual — the developer must remember to bump plugin.json, write the commit with the right format, and push. There is no explicit declaration of semver v2, no documented major version policy, and no protection against inconsistent bumping (e.g. bumping patch three times for three fix commits instead of once). The `momentum:release` skill makes release a one-command operation while keeping the developer in control of the final push.

**Scope note (distill 2026-05-16):** Original story included git tagging (`vX.Y.Z` annotated tags) and `git push --tags`. Retro finding removed tagging from scope — the release skill covers the 4-step UX only. Git tagging can be added as a separate story if needed.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation and refined
     via distill scope expansion (sprint-2026-04-27 retro). They have NOT been
     validated against architecture or verified for completeness. This section MUST be
     fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are draft ACs reflecting the full 4-step momentum:release flow:

**Part 1 — Rule update:**
- `version-on-release.md` explicitly references semver v2 (https://semver.org/spec/v2.0.0.html)
- `version-on-release.md` documents the major version policy for this plugin
- `version-on-release.md` clarifies that breaking changes bump major even in 0.x territory

**Part 2 — momentum:release skill — Step 1 (Compute bump):**
- Skill is invocable as `/momentum:release`
- Skill identifies the baseline version from the most recent `chore(plugin): bump version` commit, falling back to plugin.json current version
- Skill classifies commits: `feat`→minor, `fix`→patch, `BREAKING CHANGE`/`!` suffix→major
- Non-conventional commits (chore, docs, refactor, etc.) are ignored for bump classification
- Exactly one version increment applied regardless of commit count — the highest classification wins
- Major bump: MAJOR+1, MINOR=0, PATCH=0
- Minor bump: MINOR+1, PATCH=0 (MAJOR unchanged)
- Patch bump: PATCH+1 (MAJOR, MINOR unchanged)
- Developer is shown a summary of the commits that drove the computed bump before proceeding

**Part 2 — momentum:release skill — Step 2 (Update plugin.json):**
- `skills/momentum/.claude-plugin/plugin.json` version field updated to new version string
- No other files modified in this step

**Part 2 — momentum:release skill — Step 3 (Commit):**
- Commit created with message: `chore(plugin): bump version to X.Y.Z — brief description`
- Only plugin.json is staged for this commit

**Part 2 — momentum:release skill — Step 4 (Push gate):**
- Skill runs `git log @{u}..HEAD --oneline` and presents the output to the developer
- Skill explicitly asks "Push to remote? (Y/N)" — push never happens automatically
- Push proceeds only on explicit developer confirmation (Y)
- If developer declines (N), commits remain local and developer is told they can push manually
- The push-requires-approval rule is enforced unconditionally — no flags or options bypass it

**Edge cases:**
- Edge case: no commits since last release → no-op with clear message, no files modified
- Edge case: commits exist but none are conventional → no-op with clear message
- Edge case: no GitHub remote → halt before modifying plugin.json with clear error

> Note: The ACs above are draft captures. Create-story will replace them with
> validated, testable acceptance criteria.

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
