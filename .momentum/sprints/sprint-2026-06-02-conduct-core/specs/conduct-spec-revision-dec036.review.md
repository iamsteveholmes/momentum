# conduct-spec-revision-dec036 — Document Review Contract

```yaml
story_slug: conduct-spec-revision-dec036
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-02-conduct-core/specs/conduct-spec-revision-dec036.review.md
how_dev_self_checks: |
  Before you signal done, open the revised spec
  (_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md) and confirm each Required
  Claim below is literally readable in the produced text. Check four sections were revised
  (binding decisions, fixer schema, gate model, report model) plus the added reconciliation
  note. Confirm the spec no longer says "zero intermediate gates" or "ALWAYS auto-fixed" as
  an absolute, that the new mid-flight tier is bounded to exactly two conditions
  (irreversible-and-imminent OR build-invalidating), that the new `escalated` disposition and
  the timing-tier marker both appear, that a non-empty rationale is required for dismissals,
  and that dismissed findings are rendered. If any claim is not present in the text, the work
  is not done.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/conduct-spec-revision-dec036.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

`_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` — the revised conduct design specification. The reviewer reads the binding-decisions section, the fixer-schema section, the gate-model section, the report-model section, and the added reconciliation note, and confirms each claim below by reading the produced text.

## Required Claims

A reviewer must be able to confirm each of the following by READING the revised spec:

- [ ] The binding-decisions section states that a single human end-gate at the end of the build is the DEFAULT gate model.
- [ ] The binding-decisions section states that a narrow, high-bar, stakes-gated mid-flight escalation tier is permitted as the SOLE exception to the single end-gate.
- [ ] The binding-decisions section states the mid-flight bar explicitly: a finding may escalate mid-flight ONLY if it is irreversible-and-imminent OR build-invalidating, and no other condition is named.
- [ ] The binding-decisions section states that routine findings are still ALWAYS auto-fixed silently.
- [ ] The binding-decisions section states that stakes-class legitimate findings are RAISED (escalated/surfaced), not silently auto-fixed.
- [ ] The fixer-schema section no longer asserts that a legitimate finding is "ALWAYS auto-fixed" as an absolute tied to decision 1; the disposition instead depends on the finding's stakes class and timing tier.
- [ ] The fixer-schema section names three stakes classes: security / auth-isolation; irreversible / destructive (with examples such as migration, delete, force-push, prod deploy); and high-blast-radius / architecture.
- [ ] The fixer-schema section names a default "routine" class for findings outside the three stakes classes.
- [ ] The fixer-schema section documents the disposition set including the NEW `escalated` disposition (raised, not silently fixed) alongside `fixed`, `dismissed`, and `triaged-out`.
- [ ] The fixer-schema section documents a timing-tier marker with two values: `end-gate-expanded` (default) and `mid-flight` (narrow exception).
- [ ] The fixer-schema section states that a non-empty rationale is REQUIRED when a finding's disposition is `dismissed`.
- [ ] The gate-model section documents the mid-flight escalation tier ALONGSIDE the single human end-gate and restates the narrow bar (irreversible-and-imminent OR build-invalidating only).
- [ ] The gate-model section makes clear the end-gate is the default and the mid-flight tier is the rare exception (end-gate expansion is the norm / safety net).
- [ ] The report-model section states that dismissed findings are RENDERED in the report (dismissed-rendering / D3).
- [ ] The report-model section documents an anti-rubber-stamp end-gate forcing function (D4) so the human cannot trivially rubber-stamp the gate.
- [ ] The report-model section documents decision-grade presentation caps and a self-sufficiency floor (D5) — bounding how much is presented and guaranteeing enough context to decide without leaving the report.
- [ ] A reconciliation note is present that maps each spec change to DEC-035 binding decision #1 and to DEC-036, mirroring the DEC-036 Reconciliation table.
- [ ] The revised text preserves the anti-firehose / narrow-bias intent: routine findings stay always auto-fixed and the mid-flight tier is not widened beyond the two named conditions.

## Required Sections

The revised spec must contain revised content in each of these areas, identifiable by the reviewer:

- The binding-decisions section (the section that previously stated the single-end-gate / zero-intermediate-gates absolute).
- The fixer-schema section (the section that previously stated legitimate findings are always auto-fixed).
- The gate-model section (the section describing the human gate(s)).
- The report-model section (the section describing the build report presented at the gate).
- A reconciliation note tying the changes to DEC-035 binding decision #1 and DEC-036.

## Pass Criteria

- Every Required Claim above is confirmable by reading the revised `sprint-dev-redesign-spec.md`.
- All five Required Sections show revised content consistent with the claims.
- The mid-flight bar in the revised text is bounded to exactly the two named conditions (irreversible-and-imminent OR build-invalidating) with no third condition introduced.
- The reconciliation note maps each change to its source decision (DEC-035 binding decision #1 and DEC-036).

## Fail Criteria

- The spec still asserts "zero intermediate gates" or "ALWAYS auto-fixed" as an unqualified absolute.
- Any one of the stakes classes, the `escalated` disposition, the timing-tier marker, the required non-empty dismissal rationale, the dismissed-rendering requirement, the anti-rubber-stamp forcing function, or the decision-grade caps + self-sufficiency floor is absent from the revised text.
- The mid-flight tier is widened beyond irreversible-and-imminent / build-invalidating, or routine findings are no longer stated to be always auto-fixed.
- The reconciliation note is missing or fails to map changes to both DEC-035 binding decision #1 and DEC-036.
