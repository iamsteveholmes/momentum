---
title: Render conduct's end-gate decision cards (wire end_gate_escalations into the step-5 report)
story_key: conduct-endgate-decision-card-rendering
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: high
depends_on: []
---

# Render conduct's end-gate decision cards (wire end_gate_escalations into the step-5 report)

## Story
Follow-up from the conduct core-build slice (`sprint-2026-06-02-conduct-core`). Render conduct's end-gate decision cards (wire end_gate_escalations into the step-5 report).

## Why this exists
conduct collects stakes-class escalations into {{end_gate_escalations}} but the step-5 template that renders them as decision cards ({{stakes_findings}}) is HOLLOW. conduct's single human surface cannot yet show a stakes decision. The hand-built report for sprint-2026-06-02-conduct-core is the stand-in for this screen.

## What's needed
- Wire {{end_gate_escalations}} (and AVFL/E2E leftovers) into the step-5 decision-card section.
- Build the report to the captured Format & Voice spec: plain-language voice, risk-organized, 5-beat divergence narrative, per-item review panel (testing-first + rationale+refs + diff), the honesty/completeness section, anti-rubber-stamp gate, screenshots-for-UI.
- Use the committed worked example + reference generator as the bar.

## References
- Format & Voice spec (build to this): _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- Worked example: .momentum/handoffs/sprint-2026-06-02-conduct-core-hitl-report.html
- Reference impl: .momentum/gen-endgate-report.py
- DEC-036 D2/D3/D4/D5; conduct spec §9
