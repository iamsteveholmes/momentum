---
title: verification-standard.md + contract-format-guide.md + create-story: align the verification_method vocabulary to the closed driver_bindings enum
story_key: conduct-verification-method-enum-alignment
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: maintenance
priority: high
depends_on: []
---

# verification-standard.md + contract-format-guide.md + create-story: align the verification_method vocabulary to the closed driver_bindings enum

## Classification
Blocking level: **refinement** · found by discovery lenses: planning-handoff, spec-audit, e2e-runnability


## What
Three coupled spec-document/skill fixes that supply the source-of-truth the planning producer suite computes from. (1) verification-standard.md §1 Method Routing Table maps change_type to FREE-TEXT method descriptions ('EDD eval — adversarial...', 'Document review — confirm...'), not to the closed enum keys (skill-invoke | behavioral-trigger | bash | smoke-ui | curl | document-review) that equal the driver_bindings keys — so the change_type→enum computation has no source table. (2) contract-format-guide.md's File-Extension 'Harness driver' column lists STALE values (shell-executor, hook-trigger, document-reviewer) that contradict the guide's OWN per-type body templates (which already say bash/behavioral-trigger/document-review); it must be rewritten to the real keys AND gain the mandatory Part-A header schema (currently absent, so planning has no authoring spec for the header dev/qa require). (3) create-story Step 5 still writes free-text verification_method in the LEGACY vocabulary (eval/trigger/smoke/review/gherkin/skip, plus space-containing strings like 'document review') to story frontmatter, and sprint-planning Step 4 branches on it — creating the two-signal ambiguity §7 set out to remove; create-story must stop writing it as a routing key (advisory only if retained).

## Why it's needed (what breaks without it)
The conductor and dev/qa select the verifier driver by harness_profile == verification_method == driver_bindings key. If the key is free text ('document review' not 'document-review') driver_bindings lookup fails and no verifier is selected. The stale guide column drives harness_profile values that won't match the harness JSON. And two competing verification_method definitions let the legacy value leak into routing and pick the wrong driver/extension. These three fixes are what make the producer suite's enum computation correct and unambiguous.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
