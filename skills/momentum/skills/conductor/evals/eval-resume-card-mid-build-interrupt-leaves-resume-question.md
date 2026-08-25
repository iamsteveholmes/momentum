# Eval: An interrupted mid-build run leaves a resume-the-build card, not a stale gate question

**Surface under test:** The step 2.1 INITIAL RESUME-CARD WRITE, the Phase 2
story-terminal-merged RESUME-CARD REFRESH, and the avfl-on-merge-complete / e2e-phase-complete
phase-checkpoint refreshes (workflow.md), per `references/resume-card.md`.

**Invariant guarded (AC 3):** A run interrupted anywhere before Phase 5 — including before the
first story ever merges, and mid-build between stories — leaves a card whose one pending question
is to resume the build, not an end-gate approval decision and not a missing card.

## Scenario 0: Interrupted before the first story merges

**Given:** A sprint build whose frontier is launched (step 2.1 dispatches at least one per-story
pipeline) but the session is killed before any story reaches a `story-terminal`/`outcome: "merged"`
ledger row — the failure case this story exists to close, distinct from Scenario 1 below.

**When:** The sprint's state directory is inspected after the interrupt, and a fresh session then
starts.

**Then:**

1. `resume-card.json` exists — it was written by step 2.1's INITIAL RESUME-CARD WRITE at launch,
   not left absent until the first merge.
2. `phase` reads `"build"`, `merged.count` and `blocked.count` both read `0`, and `merged.slugs` /
   `blocked.slugs` are both empty.
3. `question.text` reads "Resume the sprint build" and `question.options` names resuming the
   build — the same question identity as Scenario 1's pre-end-gate refreshes.
4. The next session's greeting leads with that resume-the-build question rather than a clean-start
   greeting — a session dying before story #1 merges must not read as "nothing was happening."

## Scenario 1: Interrupted between a merge and the next story's completion

**Given:** A multi-story sprint build that is interrupted (session killed) between one story's
merge and the next story's completion — i.e., after at least one `story-terminal`/`outcome:
"merged"` ledger row exists but before Phase 5 is ever reached.

**When:** The sprint's state directory is inspected after the interrupt, and a fresh session then
starts.

**Then:**

1. `resume-card.json` exists and its `phase` field names a pre-end-gate phase (`"build"`,
   `"avfl-on-merge"`, or `"e2e"` depending on exactly where the interrupt landed).
2. `merged`/`blocked` reflect the story state at the point of interruption, not zero and not the
   full sprint roster.
3. `question.text` reads as a build-resume question ("Resume the sprint build") — never the
   approve-or-request-changes text used at the end-gate.
4. `question.options` names resuming the build, not "Approve"/"Request changes".
5. The next session's greeting leads with that resume-the-build question, not a gate-approval
   question.

## Pass Criteria

The card's question identity is unambiguously the build-resume question at every pre-end-gate
checkpoint, and the following session surfaces exactly that question first.

## Fail Criteria

No card exists after the interrupt — including when the interrupt lands before the first story
merges (Scenario 0); the card poses an approval question for a gate never reached; the card carries
more than one question; the following session's greeting leads with anything other than the
resume-the-build question.

## Verification Method

Inspection of `workflow.md`'s four pre-end-gate RESUME-CARD write sites (step 2.1 INITIAL
RESUME-CARD WRITE, Phase 2 story-terminal merged, avfl-on-merge-complete, e2e-phase-complete)
confirming each writes the same "Resume the sprint build" question. Subagent walkthrough: run a
fixture build, kill it before any story merges and inspect the card (Scenario 0), then separately
run it through one story merge, kill it, inspect the card (Scenario 1), then start a fresh session
in each case and observe the greeting.
