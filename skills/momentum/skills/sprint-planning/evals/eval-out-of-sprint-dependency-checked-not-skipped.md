# Eval: Cross-Story Seam Coherence — Out-of-Sprint Dependency Is Checked, Not Skipped

**ID:** eval-out-of-sprint-dependency-checked-not-skipped
**Change-type:** skill-instruction
**Phase:** Step 3.6 (cross-story seam coherence check)

## Scenario A — out-of-sprint producer, done, delivers the named input

Given a one-story sprint where the sole selected story names a config key it expects from
producer story `producer-outside-sprint`, which is NOT among the sprint's selected stories.
`producer-outside-sprint`'s recorded status in `stories/index.json` is `done`, and either its
completed-sprint contract record or its story file's Acceptance Criteria show it delivers
exactly that config key.

When Step 3.6 runs

Then:
1. The edge to `producer-outside-sprint` is enumerated — not skipped for being outside the
   sprint
2. `producer-outside-sprint`'s recorded status and deliverable are read (per
   `references/coherence-gate.md` §3b) rather than the edge being treated as automatically
   satisfied or automatically ignored
3. The edge is recorded as satisfied — no coherence failure raised

## Scenario B — out-of-sprint producer, not done (or done without the deliverable)

Given the same shape, but `producer-outside-sprint`'s recorded status is NOT `done` (still
`backlog` or `in-progress`) — OR its status is `done` but neither its completed-sprint
contract record nor its story file shows it delivering the named config key.

When Step 3.6 runs

Then:
1. The edge to `producer-outside-sprint` is enumerated — not skipped
2. A coherence failure is raised naming both the consumer and `producer-outside-sprint`
3. The failure states what is missing or why it is not satisfied (either "producer not
   complete" or the specific undelivered config key)
4. This failure appears as a mandatory genuine fork at Step 7 and blocks activation at Step 8
   under the same rules as an in-sprint mismatch

## Pass Criteria

- Both scenarios show the out-of-sprint edge counted in `{{coherence_edges}}` /
  `coherence-report.md` — never silently absent
- Scenario A: no failure raised; edge marked satisfied with the checked evidence noted
- Scenario B: a failure is raised naming both story identifiers and the unmet condition
  (incomplete status or missing deliverable)

## Fail Criteria

- The out-of-sprint edge is omitted from the enumeration or from `coherence-report.md`
  entirely
- Scenario A raises a failure despite the out-of-sprint story's recorded delivery matching
  what was named
- Scenario B raises no failure despite the out-of-sprint story being incomplete or not
  delivering the named input
- The edge is treated as automatically satisfied purely because the producer is outside the
  sprint (no status/deliverable check performed)
