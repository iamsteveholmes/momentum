---
title: "Fixture: Add hello-skill output file"
story_key: fixture-add-hello-skill
status: ready-for-dev
epic_slug: ad-hoc
story_type: feature
priority: low
change_type: script-cli
depends_on: []
_fixture_note: >
  Trivial fixture story for conduct-e2e end-to-end testing.
  Intended to be built by the conductor against the sprint-fixture-conduct-e2e sprint.
  The "implementation" is adding a single output file.
---

# Fixture: Add hello-skill output file

## What

Create a trivial output file at `.momentum/fixtures/sprint-fixture-conduct-e2e/output/hello-skill-output.txt`
with the content `hello from fixture-add-hello-skill`.

This is a minimal fixture story to exercise the conductor's per-story build pipeline.

## Why

Provides a concrete, verifiable world-change for end-to-end conductor testing.
After the conductor builds this story, the output file must exist on disk.

## Acceptance criteria

- [ ] File `.momentum/fixtures/sprint-fixture-conduct-e2e/output/hello-skill-output.txt` exists.
- [ ] File contains the text `hello from fixture-add-hello-skill`.
