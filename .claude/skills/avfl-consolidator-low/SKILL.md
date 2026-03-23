---
name: avfl-consolidator-low
description: AVFL consolidator at low effort. Merges, cross-checks, deduplicates, and scores validator findings for benchmarking effort × role interactions.
effort: low
internal: true
---

# AVFL Consolidator / Low Effort

You consolidate findings from multiple validators into a single scored findings list.

Read the consolidator prompt template and scoring weights from:
`/Users/steve/projects/momentum/.claude/skills/avfl/references/framework.json`

Use:
- `prompts.consolidator` — your instruction template
- `scoring.severity_weights` — score deductions (critical −15, high −8, medium −3, low −1)
- `scoring.grades` — grade thresholds

Steps:
1. Tag confidence: HIGH (both reviewers in a lens found it) or MEDIUM (only one found it)
2. Merge all findings from all lenses
3. Deduplicate — same issue: keep most specific description, highest severity
4. Investigate MEDIUM-confidence findings against source material — keep if evidence supports, discard if hallucination
5. Remove findings without evidence
6. Calculate score starting at 100, sort by severity then location

You will receive the raw findings from all validators for the run.
