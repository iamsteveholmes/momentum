# Default Synthesis Output Structure

The synthesis agent (Phase 5) should adapt this structure based on the research topic and scope. The sub-questions from Phase 1 drive the main sections — this template provides the framing.

---

## Frontmatter Template

```yaml
---
title: "{{topic}} — Research Report"
date: {{date}}
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: {{true if Q&A ran, false for light profile}}
derives_from:
  {{#each raw_files}}
  - path: {{this}}
    relationship: synthesized_from
  {{/each}}
  {{#if gemini_output}}
  - path: raw/gemini-output.md
    relationship: synthesized_from
  {{/if}}
  {{#if avfl_report}}
  - path: validation/avfl-report.md
    relationship: validated_by
  {{/if}}
  {{#if practitioner_notes}}
  - path: raw/practitioner-notes.md
    relationship: informed_by
  {{/if}}
---
```

## Document Structure

```markdown
# {{topic}} — Research Report

## Executive Summary
[3-4 paragraphs: scope, key findings, who this is for]

## 1. [Sub-question 1 title]
[Findings synthesized from all raw sources addressing this question]

## 2. [Sub-question 2 title]
[...]

## N. [Sub-question N title]
[...]

## Cross-Cutting Themes
[Patterns that span multiple sub-questions]

## Recommendations
[Actionable guidance based on the findings]

## Known Limitations
[What the research does not cover, weak evidence areas, open questions]

## Sources
[Consolidated, deduplicated source list — only verified sources that are actually cited]
```

## Evidence Notation in Final Document

Carry forward evidence notation from raw sources:
- `[OFFICIAL]` → VERIFIED claims (highest trust)
- `[PRAC]` → CITED claims (community-sourced, has URL)
- `[UNVERIFIED]` → INFERRED claims (flag clearly)
- Claims flagged by AVFL → SUSPECT (note the AVFL finding)
- Claims with no attribution → UNGROUNDED (remove or flag)

## Adaptation Guidelines

- If the topic is a comparison (A vs B), use a comparison table in each section
- If the topic is a technology evaluation, include a decision framework
- If the topic is exploratory, use the sub-questions as-is for section headers
- The structure should serve the reader, not the template — adapt freely
