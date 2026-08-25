# Eval: A pending resume card leads the next session's greeting

**Surface under test:** Session-start behavior in `.claude/rules/impetus.md` — the resume-card scan
folded into the single session-start Bash call, and its rendering ahead of the N-of-M feature
headline.

**Standard:** DEC-040 D5, `skills/momentum/skills/conductor/references/resume-card.md`, and the
Decision-Grade Presentation Standard.

## Scenario

**Given:** A `resume-card.json` with `status: "pending"` and one pending question exists under
`.momentum/sprints/{some-sprint}/`, and that sprint is **not** the sprint `.momentum/sprints/
index.json` marks active.

**When:** A fresh session starts and Impetus runs its session-start behavior.

**Then:**

1. The pending question is the first thing in the situational report — ahead of the N-of-M feature
   headline, honest ledger counts, sprint name, and handoff mentions.
2. The card is found even though its sprint is not the active one (the scan is not gated on
   `sprints/index.json`'s active pointer).
3. The surfaced card stays within budget: a lead of at most two sentences, merged/blocked work
   rendered as count lines only (never enumerated story slugs), exactly one question with its
   options, and the end-gate report referenced by link/path rather than inlined.
4. The N-of-M feature headline still appears, immediately after the pending question, within the
   same overall budget.
5. After the greeting, the card file's `resurface_count` has been incremented by 1 and
   `waited_since` is unchanged from before the session.

## Pass Criteria

The pending question and its options are the first content element; merged/blocked appear only as
counts; the report is referenced by path; the feature headline still follows; the card file shows
an incremented counter and an unchanged `waited_since` after the greeting.

## Fail Criteria

The greeting opens with the feature headline, ledger counts, or anything other than the pending
question; the card is missed because its sprint is not active; the surface enumerates story slugs
or inlines the report; more than one question appears; `resurface_count` fails to increment or
`waited_since` is altered by the read.

## Verification Method

Inspection of `.claude/rules/impetus.md`'s session-start ordering and budget instructions,
cross-checked with a subagent walkthrough: place a fixture pending card under a non-active sprint
directory, start a fresh session, and inspect both the rendered greeting and the card file
before/after.
