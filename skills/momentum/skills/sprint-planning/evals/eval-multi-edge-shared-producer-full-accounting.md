# Eval: Cross-Story Seam Coherence — Multi-Edge Shared Producer, Full Accounting

**ID:** eval-multi-edge-shared-producer-full-accounting
**Change-type:** skill-instruction
**Phase:** Step 3.6 (cross-story seam coherence check), feeding Step 7

## Scenario — three consumers, one shared producer, mixed outcomes

Given a sprint with three consumer stories that all depend on the same producer story
`shared-producer`:

- Consumer `consumer-satisfied` — its Acceptance Criteria name a concrete external input: "the
  response field carrying the suggestion copy." `shared-producer`'s frozen contract states its
  endpoint's response now includes exactly that field.
- Consumer `consumer-mismatched` — its Acceptance Criteria name a DIFFERENT concrete external
  input: "an emitted config key controlling the suggestion threshold." `shared-producer`'s
  frozen contract says nothing about a config key anywhere — it only covers the response field
  above.
- Consumer `consumer-presence-only` — its Acceptance Criteria only say "build after
  shared-producer lands," with no concrete named input at all.

When Step 3.6 runs over this three-edge, one-producer sprint, following
`references/coherence-gate.md`

Then:
1. All three edges are enumerated — `{{edge_count}}` = 3, none dropped for sharing a producer
2. `consumer-satisfied`'s edge is matched against `shared-producer`'s deliverable text using
   ONLY `consumer-satisfied`'s own named input, and resolves SATISFIED
3. `consumer-mismatched`'s edge is matched against `shared-producer`'s deliverable text using
   ONLY `consumer-mismatched`'s own named input (the config key), independently of
   `consumer-satisfied`'s verdict, and resolves MISMATCH — a coherence failure — even though
   the same producer already satisfied a different consumer
4. `consumer-presence-only`'s edge is classified `presence-only` — no matching attempted,
   because no concrete input is named
5. `coherence-report.md` records all three edges independently and correctly: one under
   "## Satisfied / Presence-only" as satisfied (with evidence), one under "## Satisfied /
   Presence-only" as presence-only, and one under "## Open Coherence Failures" naming both
   `consumer-mismatched` and `shared-producer`
6. No edge's verdict is silently copied, cached, or inherited from another edge sharing the same
   producer

When this reaches Step 7 (developer review)

Then:
7. Exactly one mandatory genuine fork appears — for the `consumer-mismatched` ↔
   `shared-producer` mismatch — not zero, not two or three
8. `consumer-satisfied` and `consumer-presence-only` produce no fork cards; they appear only in
   the defaulted-choices collapsible

## Pass Criteria

- `{{edge_count}}` = 3; all three consumer slugs appear somewhere in `coherence-report.md`
- `consumer-satisfied` is recorded as satisfied; `consumer-mismatched` is recorded as an open
  coherence failure naming the config key it expects and `shared-producer` as the producer;
  `consumer-presence-only` is recorded as presence-only
- Exactly one genuine fork is created at Step 7, scoped to `consumer-mismatched` ↔
  `shared-producer` only

## Fail Criteria

- `consumer-mismatched`'s failure is missed or downgraded to satisfied because
  `shared-producer` already satisfied `consumer-satisfied`'s different, unrelated ask (a cached
  or merged verdict reused across edges sharing a producer)
- Any of the three edges is dropped from `{{coherence_edges}}` or from `coherence-report.md`
- `consumer-presence-only` is incorrectly matched/mismatched instead of classified
  presence-only, or `consumer-satisfied`/`consumer-mismatched` are incorrectly treated as
  presence-only
- Zero forks, or more than one fork, appear at Step 7 for this scenario
