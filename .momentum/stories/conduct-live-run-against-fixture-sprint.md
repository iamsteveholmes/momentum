---
title: Run /momentum:conduct live against the fixture sprint (the one un-executed acceptance clause)
story_key: conduct-live-run-against-fixture-sprint
status: backlog
epic_slug: momentum-conductor-core
feature_slug:
story_type: feature
priority: high
depends_on:
  - momentum-knowledge-base-buildout
  - manifesto-builder-skill-generate-then-curate
  - repair-phantom-story-file-entries-and-backfill-live-fixture-scope
touches: []
---

# Run /momentum:conduct live against the fixture sprint (the one un-executed acceptance clause)

<!-- PLANNING STUB: Seeded by sprint-planning 2026-07-13 to repair a phantom
     story_file:true index entry (the file never existed — see
     repair-phantom-story-file-entries-and-backfill-live-fixture-scope). All sections
     below marked DRAFT require full rewrite by create-story before development. -->

_This story is a planning-seeded stub. Run `momentum:create-story` on it to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the shipped gen-2 live E2E driver executed for real against a populated nornspun
fixture — agents.json project entries, `.claude/manifests/` manifestos, and composed agent
files produced via build-guidelines — with its observed PASS/FAIL output captured,
so that the compose → register → resolve → spawn pipeline is proven live instead of
merged "done" on structured status that masked a driver that has never passed.

## Description

THE proof story for the "cohort goes live" sprint goal. It discharges the escalated
residual from sprint-2026-06-28: `live-e2e-compose-register-resolve-gen-2-agent` merged
done with headline AC1/AC6 unmet — both recorded driver runs died at the first check
(`agents.json` not found; missing live fixture), and the same sprint's stage-1 dev agent
emitted structured `outcome: pass` while its prose admitted the run was deferred.

Scope: set the nornspun fixture (agents.json project entries, `.claude/manifests/`,
composed agents via build-guidelines), then execute the shipped E2E driver live against it.

**Verification hard rule (from the 2026-07-06 retro):** this story's acceptance is the
observed driver output — a PASS/FAIL verdict read from the driver's actual run against the
fixture. Structured status fields, prior "done" markers, and agent self-reports are NOT
acceptable evidence. The driver has never passed; only an observed passing run closes this.

## Acceptance Criteria

<!-- DRAFT: rough criteria captured at planning. This section MUST be fully rewritten by
     create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

1. The nornspun fixture is populated: agents.json project entries, `.claude/manifests/`
   manifesto instance(s), composed agent file(s) under `.claude/guidelines/agents/`.
2. The shipped E2E driver runs live against the fixture and its observed output shows PASS.
3. The observed run output (not structured status) is captured as the story's evidence
   artifact.

## References

- Handoff: next-sprint-cohort-review-2026-07-06 §4 Wave 2 (per-story caution on observed output)
- Sprint summary: .momentum/sprints/sprint-2026-06-28/sprint-summary.md (retro caveat)
- Ledger: retro-sprint-2026-06-28-live-e2e-compose-ac1-ac6-unmet-shipped-done
- Ledger: retro-sprint-2026-06-28-dev-agent-structured-status-vs-prose-admission-gap
