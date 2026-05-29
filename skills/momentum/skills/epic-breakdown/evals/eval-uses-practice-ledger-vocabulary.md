# Eval: Epic breakdown uses practice-ledger vocabulary and delegates all writes to triage

Given the epic-breakdown skill running end-to-end for any `epic_slug`, the skill's workflow and
final report should:

1. Delegate ALL persistence to `momentum:triage` — epic-breakdown never appends to, writes, or
   mutates the practice ledger itself. The skill's sole output to triage is a pre-enumerated
   candidate list; triage routes each item to intake / decision / practice-ledger.
2. Use the current practice-ledger vocabulary, NOT the retired intake-queue vocabulary:
   - References to where SHAPING / DEFER / REJECT items are parked say `practice-ledger.jsonl`,
     never `intake-queue.jsonl`.
   - No invocation of any `momentum-tools.py intake-queue …` subcommand appears anywhere in the workflow.
   - No structured `kind: <enum>` (shape | watch | rejected | handoff) field appears — the ledger's
     event-type taxonomy belongs to A1's CLI and is triage's concern, not epic-breakdown's.
3. In the Step 7 final report, route-outcome lines name `practice-ledger.jsonl` as the parking
   destination, e.g.:
   - `· SHAPING  → {{shaping_count}} (parked in practice-ledger.jsonl)`
   - `· DEFER    → {{defer_count}} (parked in practice-ledger.jsonl)`
   - `· REJECT   → {{reject_count}} (logged in practice-ledger.jsonl)`

This eval verifies vocabulary and the write-delegation boundary. It is distinct from
`eval-breakdown-for-epic-slug.md` (which verifies epic-slug context loading and gap enumeration)
and from `eval-triage-delegation-contract.md` (which verifies the exact triage invocation shape):
those evals must continue to pass independently of this one.

A discipline-grep confirms the boundary: `grep -rnE 'intake-queue|intake_queue|kind:\s*(shape|watch|rejected|handoff)' skills/momentum/skills/epic-breakdown/`
returns zero matches across the epic-breakdown workflow and evals.
