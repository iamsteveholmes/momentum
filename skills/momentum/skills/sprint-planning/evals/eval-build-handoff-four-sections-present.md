# Eval: Build Handoff Carries All Four Required Sections and Opens with the Ephemeral Notice

**ID:** eval-build-handoff-four-sections-present
**Change-type:** skill-instruction
**Phase:** Activate the sprint (Step 8, terminal step)

## Scenario

Given a sprint `sprint-2026-07-06` with 2 waves — Wave 1: `story-a`, `story-b`; Wave 2: `story-c`
(depends on `story-a`) — each with a frozen contract at
`.momentum/sprints/sprint-2026-07-06/specs/{slug}.*`, a coverage plan at
`.momentum/sprints/sprint-2026-07-06/coverage-plan.md`, a sprint-record `goal` value of
"Ship the widget importer end to end", and an AVFL result of CLEAN with no guard failures and no
developer-noted fork caveats.

When Step 8 writes the build handoff artifact for this sprint

Then, reading the artifact from top to bottom, a reader with no other context can find:

1. As the very first line (before any section heading), a notice stating the document is a
   use-then-discard build bridge for the next `/momentum:conduct` session and should be deleted
   once consumed.
2. A **Sprint Goal** section containing "Ship the widget importer end to end".
3. A **Stories by Wave** section listing Wave 1 (`story-a`, `story-b`) before Wave 2 (`story-c`),
   in execution order.
4. A **Contract / Spec Locations** section listing each story's resolved contract path plus the
   coverage-plan path `.momentum/sprints/sprint-2026-07-06/coverage-plan.md`.
5. A **Planning-Time Cautions** section. Since nothing was flagged during planning for this
   sprint, its body reads exactly "No planning-time cautions raised." — the section heading is
   still present, not dropped.

## Pass Criteria

- All four sections (Sprint Goal, Stories by Wave, Contract/Spec Locations, Planning-Time
  Cautions) are present, each identifiable by its own heading.
- The opening line carries the ephemeral-bridge notice ahead of every section.
- Waves render in execution order (Wave 1 before Wave 2), each with its assigned story slugs.
- The cautions section uses the exact "No planning-time cautions raised." wording rather than
  being blank or omitted, since no cautions arose during planning.

## Fail Criteria

- Any of the four sections is entirely absent from the document (not just empty — genuinely
  missing, with no heading at all).
- The ephemeral-bridge notice is missing, or appears after section content rather than as the
  first line.
- Wave order is reversed or story-to-wave assignment is wrong.
- The cautions section is blank or silently omitted instead of carrying the "No planning-time
  cautions raised." fallback line.
