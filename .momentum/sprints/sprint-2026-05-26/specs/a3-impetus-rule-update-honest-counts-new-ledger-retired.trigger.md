# a3-impetus-rule-update-honest-counts-new-ledger-retired — Hook Trigger Contract

**Harness Profile:** behavioral-trigger

## Trigger Condition

A developer opens a fresh top-level Claude Code session at the project root
of this repository. No prior session context. No prior in-session messages.
The session's first model turn fires the project's session-start orientation
behavior.

A second trigger: the same developer opens another fresh session within 24
hours of the first.

## Observable Outcome

After the first trigger fires, the developer sees an Impetus-voice
situational report in the first response that:

1. Includes a single, structured open-count line in the shape:
   `"N open entries (X this week, Y older than 30 days, Z near auto-close)"`
   with concrete integers substituted for N/X/Y/Z. No "last 5" enumeration.
   No row-by-row dump of ledger entries.
2. May include a recurring-pattern signal sentence (e.g., a `closed_stale`
   recurrence callout) when the underlying ledger contains such a pattern;
   otherwise this sentence is absent.
3. Is delivered in 1–2 sentences. No menus, no fill bars, no numbered
   progress indicators, no skill machinery surfaced.
4. Closes by yielding to the developer ("Lead on", "Give the word", or
   equivalent Impetus-voice closer) — does not auto-launch any workflow.

After the second trigger (within 24h), the developer sees an equivalent
situational report. The auto-close safety net produces no visible disruption
on the second invocation — no new "closed N stale entries" callout appears
beyond what the first invocation surfaced.

## Pass Criteria

A black-box reviewer confirms each of the following by reading the first
response of each session:

- [ ] The first-response text contains the substring pattern
  `open entries` together with the parenthetical age-bucket structure
  (`this week`, `30 days`, `auto-close`).
- [ ] The first-response text does NOT contain the substring `last 5` or
  any enumeration of ledger entry titles.
- [ ] The first-response text does NOT contain any of these substrings:
  `.momentum/intake-queue.jsonl`, `intake-queue`, `pending signals`,
  `.momentum/signals/`.
- [ ] The first-response text ends in a forward-motion closer in Impetus
  voice (one of: "Lead on", "Give the word", "When you're ready",
  "Where do we begin", "I'm with you") OR a semantically equivalent line.
- [ ] The observable proof that the rule fired is the practice-ledger
  itself: after the fresh session start, running
  `momentum-tools practice-ledger by-source momentum-tools-close-stale`
  returns at least one event whose timestamp is within the last 60 seconds.
- [ ] Across two sessions opened within 24h, the second session's response
  does not add a fresh "closed N stale entries" announcement beyond what
  the first session already surfaced (idempotency of the safety net is
  visible as a no-op on the second open).

## Fail Criteria

The contract fails if any of the following is observed:

- The first response enumerates individual ledger entries (more than the
  structured count line).
- The first response references the legacy filename, the legacy CLI
  subcommand `intake-queue`, the legacy `signals/` directory, or "last 5".
- The first response runs heavy orientation: multi-step workflow launch,
  menus, fill bars, structured option lists.
- After the fresh session start,
  `momentum-tools practice-ledger by-source momentum-tools-close-stale`
  returns no event newer than 60 seconds, OR the first agent response does
  not contain the substring `open` (the count surfaced by `summary`).
- The two-session idempotency check shows a duplicate close-stale
  announcement on the second invocation within 24h.
