# Eval: Rehydration skips a partial ledger line

## Scenario

Given a build ledger at `.momentum/sprints/sprint-2026-07-13/build-ledger.jsonl` holding N complete, valid JSON rows documenting stories `story-a` and `story-b` fully merged, followed by one final line that is truncated mid-object (e.g. `{"event":"finding-disposit`) — the shape a crash mid-`printf`/mid-write would leave — when the developer resumes the Conductor against this same sprint, step 2.0 rehydration should read past the malformed line without aborting, and the build should reach a normal completion.

## Expected behavior

1. Step 2.0 reads all lines from the ledger in order. The first N lines each parse successfully as JSON and rebuild `{{build_log}}` and the other Conductor-scoped accumulators normally (per the existing event-type routing).
2. The final truncated line fails JSON parsing. Rehydration does NOT abort, raise a fatal error, or halt the resume on encountering it.
3. The malformed line is skipped: it is not added to `{{build_log}}` and does not feed any accumulator as if it were a valid row.
4. A `conductor-warning` row is appended — both to `{{build_log}}` and to the ledger file itself (this is a new live event, not a replayed row, so the REHYDRATION EXEMPTION does not apply to it) — carrying a `line_no` field equal to the truncated line's 1-indexed position in the ledger, and whose `reason` field names that line number and quotes the truncated content (e.g. `"unparseable ledger line skipped during rehydration — line 47: {\"event\":\"finding-disposit"`).
5. Rehydration continues to completion after skipping the line: the dependency frontier is computed, `{{merged}}` is seeded from story statuses, and the build resumes from the last validly recorded state (i.e., only stories not yet at `review`/`done` re-enter the frontier).
6. The resumed build proceeds to a normal final summary (end-gate report or equivalent), which is otherwise complete — story counts, findings, and escalations for `story-a` and `story-b` are intact — as if the truncated line had simply been set aside.
7. The visible output of the resumed build (ledger contents or terminal report) contains a distinct, discoverable warning identifying the truncated/malformed content — the developer is never left unaware that a line was set aside, and the content is never silently discarded nor silently treated as valid.

## Second scenario — dedup across a further resume (idempotency)

Given the ledger from the first scenario now also contains the `conductor-warning` row appended above (i.e. the truncated line is still present at the same line number, unmodified, because the ledger is append-only and the defect was never fixed), when the developer resumes the Conductor a second time against this same sprint:

8. The pre-scan collects the prior `conductor-warning` row's `line_no` into `{{warned_unparseable_lines}}` before replay begins.
9. Rehydration encounters the same truncated line at the same line number, fails to parse it, and skips it exactly as before — but because that line number is already in `{{warned_unparseable_lines}}`, it does NOT append a second `conductor-warning` row for it.
10. The ledger file, after this second resume, contains exactly one `conductor-warning` row for this truncated line — not two — confirming the persistent defect is surfaced once, not on every resume.
11. If a DIFFERENT line in the ledger is separately unparseable (a distinct `line_no`), it still gets its own warning — the dedup is scoped to the exact line number, not a blanket suppression of all unparseable-line warnings.
