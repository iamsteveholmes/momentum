# controlled-enums-and-stable-ledger-schema-finding-cards — Document Review Contract

```yaml
story_slug: controlled-enums-and-stable-ledger-schema-finding-cards
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/controlled-enums-and-stable-ledger-schema-finding-cards.review.md
how_dev_self_checks: |
  Before you signal done, open the two produced ledgers — the finding-cards ledger and the
  build-results ledger — and the schema document that governs them. Walk this checklist using only
  those artifacts. First: confirm the finding-card type field draws from a fixed, named set of allowed
  values (a controlled enum), not free text — there should be no near-duplicate strings like one value
  written two slightly different ways. Second: confirm the severity field likewise draws from a fixed
  named set. Third: confirm the build-results ledger uses ONE shape for every row across the whole run
  — every entry has the same fields; there is no mix of two different row shapes (e.g. some structured
  rows and some prose rows). Fourth: confirm both ledgers carry the same canonical key on each entry —
  the story slug — and that joining the two ledgers on that key loses no stories: every story present
  in one ledger resolves to a matching entry (or an explicit, intentional absence) in the other, with
  no entry keyed to something that is not a real story slug. You can do the join yourself by reading
  the story slugs out of each ledger and confirming the sets line up. If you can read the type/severity
  values, see one consistent row shape, and join the two ledgers on story slug with no story falling
  out, the work is done.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/controlled-enums-and-stable-ledger-schema-finding-cards.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

The schema/specification deliverable that governs the conduct finding-cards and build-results ledgers, together with the two produced ledger artifacts it governs (the finding-cards ledger and the build-results ledger). All claims below are confirmed by reading these artifacts and performing a join over them — no source code access required.

## Required Claims

- [ ] The finding-card `type` field is a controlled enum: its allowed values are an explicitly named, closed set, and every card's `type` is one of those values.
- [ ] No two enum values are near-duplicate spellings of the same concept (e.g. a value and "value / something-else" both present as distinct types) — the controlled set has eliminated the free-text near-duplicates.
- [ ] The finding-card `severity` field is a controlled enum: an explicitly named, closed set of severity values, and every card's `severity` is one of them.
- [ ] The build-results ledger uses one stable schema across all rounds of the run: every entry shares the same fields, with no mix of two row shapes (e.g. structured "gates" rows alongside prose "key" rows).
- [ ] Both ledgers carry a single canonical join key on each entry — the story slug.
- [ ] Joining the finding-cards ledger and the build-results ledger on story slug loses no stories: every story slug present in one ledger has a corresponding (or explicitly, intentionally absent) entry in the other.
- [ ] No ledger entry is keyed to a value that is not a real story slug (no non-story prose keys), and no real story is missing its key.

## Required Sections

- [ ] A definition of the controlled `type` enum with its named allowed values.
- [ ] A definition of the controlled `severity` enum with its named allowed values.
- [ ] A definition of the single stable build-results schema (the fields every row carries).
- [ ] A statement that story slug is the canonical join key for both ledgers.
- [ ] A statement that the two ledgers join on story slug with no lost stories.

## Pass Criteria

- All Required Claims are confirmable by reading the schema deliverable and the two ledger artifacts alone.
- All Required Sections are present.
- `type` and `severity` are each a closed, named enum with no near-duplicate values, and every ledger entry conforms.
- The build-results ledger shows one consistent row shape across the whole run.
- A join of the two ledgers on story slug resolves every story with no story dropped and no entry keyed to a non-story value.

## Fail Criteria

- The `type` or `severity` field still admits free-text values, or two near-duplicate values for the same concept remain.
- The build-results ledger mixes more than one row shape across the run.
- The two ledgers do not share a single canonical story-slug key, or a join on that key drops one or more stories.
- A ledger entry is keyed to a non-story value, or a real story is missing from one ledger with no explicit intentional absence.
