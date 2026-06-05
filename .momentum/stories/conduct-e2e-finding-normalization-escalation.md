---
title: Normalize E2E findings to canonical schema and route them through escalation + decision cards
story_key: conduct-e2e-finding-normalization-escalation
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Normalize E2E findings to canonical schema and route them through escalation + decision cards

## Classification
Blocking level: **blocks-run** · found by discovery lenses: engine-hollows


## What
Phase 4 (E2E) spawns the e2e-validator and only STORES {{e2e_results}}, holding them for the report as a raw summary. E2E findings never become canonical findings, never get a stakes_class, never reach the escalation engine, and never become end-gate decision cards (parallel to the qa-reviewer normalization gap, but the qa adapter is folded into the per-story-dispatch item). Phase 3 (AVFL) partially routes its findings through escalation; E2E does neither normalization nor escalation routing.

## Why it's needed (what breaks without it)
Spec §9 section 03/04 require AVFL/E2E findings rendered as self-contained decision cards. A build-invalidating E2E failure cannot escalate and lands in the report only as a count — so integration defects surfaced post-merge are not actionable at the one human gate. (Note: for Momentum's own markdown/bash repo, E2E execution_surfaces are all 'skip', so E2E currently performs no live verification anyway — see the verification-harness item; this normalization gap bites the moment any project configures a real E2E driver.)

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
