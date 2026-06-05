# Eval: Correct audit-Workflow composition passes silently

## Scenario

A retro reaches Phase 4 with prepared audit-extracts and a non-empty session set (the Phase 2
zero-session HALT has already passed). The main loop invokes the dynamic audit Workflow.

## Expected Behavior

A correctly composed audit Workflow runs end-to-end with no friction and no developer prompt:

1. `Discover` — `parallel()` lens auditors (human, execution, review, efficiency, coordination) plus
   one per-story analyst per `args.sprint_stories` entry.
2. `Verify` — `pipeline(findings, f => parallel([...skeptics]))`: each candidate finding flows through
   a per-finding refute panel; majority-refute drops it.
3. `Synthesize` — a single `agent()` that writes `retro-transcript-audit.md` (all eight sections) and
   returns `{ priority_action_items, handoff_candidates, metrics, doc_path, synthesize_status }`.

The retro main loop invokes the Workflow **once**, binds the structured return, and advances to
Phase 5 — which reads `priority_action_items` from the return — with no developer prompt about
composition and no diagnostic block.

## Pass Condition

All three phases run; exactly one synthesizer writes the doc; the structured return is consumed by
Phase 5 (`priority_action_items`) and Phase 5.5 (`handoff_candidates`); no halt, no diagnostic, no
developer prompt about composition.

## Fail Condition

Any phase missing, the synthesizer multiplexed, the main loop failing to consume the structured
return, or a developer prompt/diagnostic about team composition appearing.

## What This Tests

- The intended composition is the Workflow's three-phase structure, not a 4-member team config.
- A correct composition produces zero friction (no confirmation prompt, no halt).
- Phase 4 hands a structured return to the downstream gates, which proceed unchanged.

## Rationale

The "pass silently on correct composition" intent is preserved; the composition being verified is now
the audit Workflow's `Discover → Verify → Synthesize` structure rather than a team `config.json`.
