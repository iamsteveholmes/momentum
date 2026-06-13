---
title: Harden stage-2 QA normalization — validate stakes_class and field-merge on dedup
story_key: conduct-qa-normalization-stakes-validation-and-dedup-merge
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: defect
priority: medium
change_type:
  - skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
---

# Harden stage-2 QA normalization — validate stakes_class and field-merge on dedup

## Story

As the maintainer of the conduct stage-2 review seam,
I want the QA-normalization to default and validate `stakes_class`, and the QA/code-review dedup to merge fields rather than keep one record wholesale,
so that a missing or mistyped stakes value cannot slip a stakes-class finding past escalation, and a dedup collision cannot silently drop a remediation or a security label.

## Why this exists (two stakes-class escalations from sprint-2026-06-10, end-gate D4)

Both are defensive gaps in the new normalization seam — they bite only on malformed or conflicting reviewer output (which did not occur during sprint-2026-06-10), which is why the developer's disposition was backlog rather than fix-now.

**ad-s1 (high-blast-radius-architecture).** The stage-2 normalization carries `stakes_class` through unchanged (`conductor/workflow.md:709`) with no default and no enum-validation. The qa-reviewer's own AC table permits a dash for that column, so a missing or mistyped value would match neither the auto-fix rule (`== routine`) nor the escalate rule (membership in the three stakes classes) — a stakes-class finding could slip past the DEC-036 escalation it should trigger.

**ad-s2 (high-blast-radius-architecture).** The merge that combines QA findings with code-review findings keeps the higher-severity record **wholesale** when both describe the same location/issue. That discards the other record's `suggested_fix` (which the fixer uses as its starting point and the end-gate decision card requires) and can drop a `security-auth-isolation` label if the two reviewers classified the same issue differently.

## Acceptance Criteria

1. The stage-2 normalization applies finding-schema.md's declared default (`routine`) when the producer `stakes_class` is absent, and validates any carried value against the four-class enum (`security-auth-isolation | irreversible-destructive | high-blast-radius-architecture | routine`); an off-enum value is treated as a malformed finding (reviewer-failure path), not carried through.
2. The QA/code-review dedup performs a **field-level merge** on a same-location/same-issue collision: keep max severity, union the non-null fields (preserving a non-null `suggested_fix`), and retain the **most-severe** `stakes_class` across the colliding records — rather than keeping one record wholesale.

## Tasks / Subtasks
- [ ] Add the routine-default + enum-validation rule to the stage-2 `stakes_class` mapping bullet. (AC 1)
- [ ] Replace the keep-higher-severity-wholesale dedup with a field-level merge (max severity, union non-null fields, most-severe stakes_class). (AC 2)

## Dev Notes
- Belt-and-suspenders hardening of the seam delivered by `conduct-qa-reviewer-normalization-adapter` (sprint-2026-06-10); no active failure, defensive only.

## Dev Agent Record
