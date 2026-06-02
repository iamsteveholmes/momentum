# stakes-classification-rubric — Document Review Contract

```yaml
story_slug: stakes-classification-rubric
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-02-conduct-core/specs/stakes-classification-rubric.review.md
how_dev_self_checks: |
  Before you signal done, open the rubric artifact you produced and confirm a fresh reader
  could verify each claim below by reading ONLY that file — no code or other docs.
  Walk the checklist: are all three stakes classes present with concrete signals; is the
  routine fall-through stated; are both timing tiers named; is the mid-flight test stated
  as irreversible-and-imminent OR build-invalidating ONLY with a never-widen guardrail and
  end-gate-expanded named as the safety net; does the rubric claim sole ownership of
  classification and instruct producers to reference (not fork) it; is the output vocabulary
  compatible with the finding schema's stakes_class field and timing-tier values?
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/stakes-classification-rubric.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

`skills/momentum/references/stakes-classification-rubric.md` — the shared, single-source stakes-classification rubric authored by this story. All claims below are confirmed by reading this artifact.

## Required Claims

- [ ] The artifact exists at `skills/momentum/references/stakes-classification-rubric.md` and presents itself as the single source for stakes classification (it is written to be referenced, not copied).
- [ ] Exactly three stakes classes are named: security/auth-isolation, irreversible/destructive, and high-blast-radius/architecture — plus one routine fall-through.
- [ ] The artifact states that the three classes plus routine are exhaustive and that every finding lands in exactly one.
- [ ] The security/auth-isolation class lists concrete signals (e.g., authentication, authorization, secret/credential handling, isolation/tenancy boundary, privilege escalation, access control).
- [ ] The irreversible/destructive class lists concrete signals and explicitly names migration, delete, force-push, and production deploy as exemplars described as not cheaply/safely undoable.
- [ ] The high-blast-radius/architecture class lists concrete signals (e.g., architecture-level structure, shared/cross-cutting contracts or interfaces, surfaces whose failure radiates widely).
- [ ] The routine fall-through rule is stated: a finding matching none of the three stakes-class signals is `routine` and stays on the always-on, silent auto-fix path (never escalated).
- [ ] Two timing tiers are named: `end-gate-expanded` (default) and `mid-flight` (narrow).
- [ ] The mid-flight test is stated as irreversible-and-imminent OR build-invalidating ONLY; all other findings — including stakes-class findings failing this test — default to `end-gate-expanded`.
- [ ] The artifact instructs the reader to bias narrow when in doubt and explicitly states the mid-flight bar must never be widened.
- [ ] The artifact names `end-gate-expanded` as the safety net that catches everything the mid-flight tier deliberately excludes.
- [ ] The artifact states it is consumed by every producer (code-review adapter, qa-reviewer, AVFL) and that producers carry only emission-wiring that references this rubric — they do not define their own classification logic.
- [ ] The rubric's classification output (stakes class + timing tier) is expressed in terms compatible with the finding schema's `stakes_class` field and timing-tier values (`end-gate-expanded`, `mid-flight`), so a producer can populate the schema directly without translation.

## Required Sections

- [ ] A purpose/overview statement establishing the rubric as the single source consumed by all producers.
- [ ] A stakes-classes section defining all three classes with their concrete signals.
- [ ] A routine fall-through statement.
- [ ] A timing-tier decision section naming both tiers and the narrow mid-flight test with the never-widen / safety-net guardrail.
- [ ] A consumption note describing how producers reference the rubric and the prohibition on forking their own classifier.

## Pass Criteria

- All Required Claims checkboxes are confirmable by reading the artifact alone.
- All Required Sections are present.
- The three stakes classes, the routine fall-through, and both timing tiers are unambiguously defined.
- The narrow mid-flight bar (irreversible-and-imminent OR build-invalidating ONLY), the never-widen guardrail, and end-gate-expanded as the safety net are all explicitly stated.
- The single-source / reference-not-fork property and schema-compatible output vocabulary are both stated.

## Fail Criteria

- The artifact is missing, or stakes-classification logic is defined somewhere other than this single artifact.
- Any of the three stakes classes lacks concrete signals, or the routine fall-through is absent.
- The mid-flight tier is described with a test broader than irreversible-and-imminent OR build-invalidating (e.g., "any stakes-class finding escalates mid-flight"), or the never-widen guardrail / safety-net statement is missing.
- Either timing tier is unnamed, or routing of non-qualifying findings to `end-gate-expanded` is not stated.
- The artifact authorizes or implies producers should define their own classification logic, or its output vocabulary cannot be mapped to the finding schema's `stakes_class` field and timing-tier values without translation.
