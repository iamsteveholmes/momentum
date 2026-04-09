# Eval: Intake Skill Captures Conversational Context

## Purpose

Verify that the `momentum:intake` skill captures a story idea from conversation into a
stub file with unambiguous draft markers and writes a valid index entry — without running
the heavyweight create-story pipeline.

## Scenario

A developer has just described a story idea in conversation:

> "We should add a `/momentum:intake` command so I can quickly throw a story into the
> backlog while we're talking without spinning up the full create-story pipeline. It
> comes up every sprint — I think of something, but I lose the context by the time I
> formally create the story. The workaround is manually editing stories/index.json which
> loses all the why. I'd say it belongs in the impetus-core epic, medium priority."

The developer then invokes `/momentum:intake`.

## Expected Behaviors

### B1: Context Extraction

The skill extracts without asking unnecessary questions:

- **Title:** Derived from conversation (e.g., "Intake Skill — Lightweight Story Capture")
- **Description:** Captures the "why" — lost context, sprint recurrence, workaround pain
- **User story:** Generated as a proper "As a / I want / so that" statement
- **Rough ACs:** Captured conversationally — not polished, not researched
- **Pain context:** Recurrence ("every sprint"), workaround burden (manual JSON edit),
  forgetting risk (context lost by next session)
- **Epic:** `impetus-core` (from user's explicit suggestion)
- **Priority:** `medium` (from user's explicit suggestion)

### B2: Slug Generation

- Slug is derived from title: lowercased, spaces to hyphens, special chars stripped
- Example: "Intake Skill — Lightweight Story Capture" → `intake-skill-lightweight-story-capture`
  (or similar reasonable truncation)
- Skill checks stories/index.json for slug conflict before writing
- If conflict found: reports it and asks for an alternative slug

### B3: Stub File Contents

The stub file at `_bmad-output/implementation-artifacts/stories/<slug>.md` must:

- Have frontmatter with `status: backlog` (NOT `ready-for-dev`)
- Contain both an HTML comment and visible inline text draft marker in every section
  that was not populated by intake
- Sections that MUST have draft markers: Acceptance Criteria (even if rough ACs captured,
  the section is marked as requiring refinement), Dev Notes, architecture compliance,
  testing requirements, implementation guide, Tasks/Subtasks, Dev Agent Record
- Sections that must NOT be marked as draft: story key/slug, title, description, user story
- Draft markers are unambiguous — both machine-readable (`<!-- DRAFT: ... -->`) and
  human-readable (`_DRAFT — requires rewrite via create-story before this story is dev-ready._`)

### B4: Draft Marker Clarity

A simulated create-story agent reading the stub file should have zero ambiguity:

- Status field is `backlog` — machine-readable signal
- HTML comments are present on every draft section — agent-readable signal
- Visible inline text is present — human-readable signal
- No section looks "complete" when it is actually a stub

### B5: Index Entry Written via CLI

The skill writes the index entry using `momentum-tools sprint story-add` (not by
directly editing `stories/index.json`):

- `status`: `backlog`
- `title`: from captured context
- `epic_slug`: `impetus-core` (from user suggestion)
- `story_file`: `true`
- `priority`: `medium` (from user suggestion)
- `depends_on`: `[]`
- `touches`: `[]`

### B6: Minimal Tool Calls

The skill completes with:

- 1 read of stories/index.json (slug conflict check)
- 1 write of the stub file
- 1 CLI call to add the index entry
- No subagent spawns, no web searches, no parallel discovery

### B7: Epic Determination

If the user had NOT mentioned an epic, the skill reads the epic list and recommends
the best fit, then asks the user to confirm — it does NOT silently default to a
placeholder like `unknown` or `tbd`.

### B8: What Should NOT Happen

- No call to `bmad-create-story`
- No artifact analysis or architecture deep-dive
- No AVFL checkpoint
- No web research
- No change-type classification
- No implementation guide injection
- Status in stub is NEVER `ready-for-dev`

## Pass Criteria

All of B1–B8 must be satisfied. A failure on any behavioral expectation is a failing eval.
