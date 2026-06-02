# directed-fix-finding-schema — Document Review Contract

```yaml
story_slug: directed-fix-finding-schema
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-02-conduct-core/specs/directed-fix-finding-schema.review.md
how_dev_self_checks: |
  Before you signal done, open skills/momentum/references/finding-schema.md and confirm a reader
  with no access to the implementation could verify every claim below just by reading it:
  - All twelve base fields are named and explained: story_slug, source, verdict, severity, type,
    location, summary, detail, evidence, ac_id, legitimate, suggested_fix.
  - stakes_class is defined, stated as orthogonal to severity, defaults to routine, and lists exactly
    security-auth-isolation | irreversible-destructive | high-blast-radius-architecture | routine,
    with the migration/delete/force-push/prod-deploy examples on irreversible-destructive.
  - disposition lists exactly fixed | dismissed | triaged-out | escalated; escalated reads as
    "raised, not silently fixed"; an explicit note says there is NO deferred disposition.
  - timing_tier lists exactly end-gate-expanded (default) | mid-flight, and the mid-flight bar is
    documented as narrow: irreversible-and-imminent OR build-invalidating only, must not be widened,
    with end-gate-expanded as the safety net.
  - dismissed requires a non-empty rationale (empty/missing rationale is invalid).
  - The relaxed invariant is explicit: routine legitimate findings are always auto-fixed (fixed);
    stakes-class legitimate findings are escalated, not auto-fixed; the routine fall-through is stated.
  If any of these is missing or ambiguous in the document, it is not done.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/directed-fix-finding-schema.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

`skills/momentum/references/finding-schema.md` — the canonical normalized finding-schema document produced by this story. All claims below are confirmed by reading this single artifact.

## Required Claims

- [ ] The document presents itself as the single canonical finding schema that code-review, AVFL, qa-reviewer, and the fixer all speak (one shared finding shape).
- [ ] The document defines all twelve base fields, each with a plain-English meaning: `story_slug`, `source`, `verdict`, `severity`, `type`, `location`, `summary`, `detail`, `evidence`, `ac_id`, `legitimate`, `suggested_fix`.
- [ ] The document defines a `stakes_class` field and states it is **orthogonal to `severity`** (a finding has both independently).
- [ ] `stakes_class` lists exactly these values: `security-auth-isolation`, `irreversible-destructive`, `high-blast-radius-architecture`, `routine`.
- [ ] The document states `stakes_class` **defaults to `routine`**.
- [ ] The document names the three non-routine values as the stakes classes and describes each: security / auth-isolation; irreversible / destructive (with examples migration, delete, force-push, prod deploy); high-blast-radius / architecture.
- [ ] The document defines a `disposition` field whose allowed values are exactly `fixed`, `dismissed`, `triaged-out`, `escalated`.
- [ ] The document documents `escalated` as a distinct disposition meaning **"raised, not silently fixed."**
- [ ] The document states explicitly that there is **no `deferred` disposition** (deferred is not valid; findings are never parked in a deferred state).
- [ ] The document defines a `timing_tier` marker with exactly `end-gate-expanded` and `mid-flight`, and names `end-gate-expanded` as the default.
- [ ] The document documents the `mid-flight` tier's narrow bar: **irreversible-and-imminent OR build-invalidating only**, states the bar must not be widened, and names `end-gate-expanded` as the safety net.
- [ ] The document requires a **non-empty rationale** when `disposition` is `dismissed` (empty/missing rationale is invalid by schema).
- [ ] The document encodes the relaxed auto-fix invariant: a **routine** legitimate finding is **always auto-fixed** (`fixed`); a **stakes-class** legitimate finding is **escalated**, not silently auto-fixed.
- [ ] The document states the routine fall-through explicitly: a legitimate finding with `stakes_class: routine` follows the always-auto-fixed path (anti-firehose intent preserved for the common case).
- [ ] The document presents `severity` and `stakes_class` as independent axes (e.g. a finding may be low-severity yet stakes-class, or high-severity yet routine).

## Required Sections

- A header/intro establishing the schema as the single shared finding shape for code-review, AVFL, qa-reviewer, and the fixer.
- A base-fields section enumerating and explaining the twelve base fields.
- A `stakes_class` section: enum values, default `routine`, orthogonality to `severity`, per-class descriptions with examples.
- A `disposition` section: the four-value enum, the `escalated` definition, and the explicit no-`deferred` note.
- A `timing_tier` section: the two-value enum, default, and the narrow mid-flight bar with the no-widening statement.
- A disposition-rules / invariants section covering the required dismissed-rationale and the relaxed auto-fix invariant (routine → fixed; stakes-class → escalated) plus the routine fall-through.

## Pass Criteria

Every checkbox in **Required Claims** is confirmed by reading `skills/momentum/references/finding-schema.md`, and every section in **Required Sections** is present. In particular, the four DEC-036 amendments are all visible in the document: (a) `stakes_class` enum orthogonal to severity with `routine` default; (b) `escalated` disposition added and `deferred` explicitly excluded; (c) `timing_tier` with the narrow mid-flight bar; (d) required non-empty dismissed-rationale and the relaxed "routine always-fixed / stakes-class escalated" invariant.

## Fail Criteria

Any of the following fails the contract:
- The schema document is missing, or is not at `skills/momentum/references/finding-schema.md`.
- Any base field is omitted or undefined.
- `stakes_class` is missing, lacks any of the four values, omits the `routine` default, or is not stated as orthogonal to severity.
- `disposition` omits `escalated`, includes `deferred`, or lacks the explicit no-deferred note.
- `escalated` is present but not described as "raised, not silently fixed."
- `timing_tier` is missing, omits either value, fails to mark `end-gate-expanded` as default, or fails to constrain `mid-flight` to the narrow irreversible-and-imminent OR build-invalidating bar (including the no-widening statement).
- The dismissed-rationale requirement is missing or does not require a non-empty rationale.
- The relaxed auto-fix invariant is missing, contradicts "routine legitimate → always auto-fixed," or fails to state that stakes-class legitimate findings are escalated rather than auto-fixed.
