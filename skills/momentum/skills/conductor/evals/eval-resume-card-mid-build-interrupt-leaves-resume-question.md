# Eval: An interrupted mid-build run leaves a resume-the-build card, not a stale gate question

**Surface under test:** The Phase 2 story-terminal-merged RESUME-CARD REFRESH and the
avfl-on-merge-complete / e2e-phase-complete phase-checkpoint refreshes (workflow.md), per
`references/resume-card.md`.

**Invariant guarded (AC 3):** A run interrupted anywhere before Phase 5 — including mid-build
between stories — leaves a card whose one pending question is to resume the build, not an
end-gate approval decision.

## Scenario

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

No card exists after the interrupt; the card poses an approval question for a gate never reached;
the card carries more than one question; the following session's greeting leads with anything other
than the resume-the-build question.

## Verification Method

Inspection of `workflow.md`'s three pre-end-gate RESUME-CARD REFRESH sites (Phase 2 story-terminal
merged, avfl-on-merge-complete, e2e-phase-complete) confirming each writes the same "Resume the
sprint build" question. Subagent walkthrough: run a fixture build through one story merge, kill it,
inspect the card, then start a fresh session and observe the greeting.
