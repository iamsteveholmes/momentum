---
id: DEC-014
title: Composed Agent File Staleness — Discovery-Check Model, No Auto-Invalidation
date: '2026-05-02'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-02'
prior_decisions_reviewed:
  - DEC-001 (Three-Tier Agent Guidelines — originates the composed Tier 2 files)
  - DEC-008 (Composable Specialist Agents Architecture — governs Tier 2 file generation)
stories_affected:
  - build-guidelines-skill
  - citation-integrity-validation-in-build-guidelines-avfl
---

# DEC-014: Composed Agent File Staleness — Discovery-Check Model, No Auto-Invalidation

## Summary

Composed specialist agent files (`.claude/guidelines/agents/{role}-{domain}.md`) do not use automatic staleness invalidation. The default assumption is that they remain valid. A lightweight discovery-check command can be run on demand (or roughly monthly) to detect drift between current stack/guideline state and what was used to generate the files. The check surfaces findings; the developer decides whether to regenerate. This keeps the developer in control without requiring constant manual vigilance, and avoids the noise of trigger-based auto-invalidation.

---

## Decisions

### D1: Composed file staleness model — ADAPTED

**Developer framing:** Four trigger models were under consideration — stack-change, guideline-change, time-based auto-invalidation, or manual-only. The question was which triggers should automatically mark composed files as stale and force regeneration.

**Decision:** Adapt — none of the trigger models auto-invalidate. Composed files are assumed valid by default. Instead, a discovery-check mechanism (a command or skill step) detects drift between current conditions and what was used to generate the files, then surfaces findings to the developer. Regeneration is always a manual developer decision after reviewing check output.

**Rationale:**
Stack-change triggers are too noisy — most dependency bumps don't affect agent guidelines. Time-based auto-invalidation is wasteful because files are likely still valid. Guideline-change could be a useful signal but should surface as a suggestion, not force regeneration. The check-and-decide loop keeps the developer in control. The default assumption is the files are fine.

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | When `build-guidelines-skill` ships | Does the discovery-check model work in practice? | Developer can run the check, understand what drifted, and make a confident regeneration decision without excessive friction |
