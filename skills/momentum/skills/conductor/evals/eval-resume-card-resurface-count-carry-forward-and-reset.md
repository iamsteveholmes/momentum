# Eval: resurface_count carries forward across a same-question refresh and resets on a new question

**Surface under test:** The Conductor's RESUME-CARD REFRESH sites in `workflow.md` and the
shared-write rule for `resurface_count` in `references/resume-card.md`.

**Invariant guarded:** A refresh that rewrites the card for the SAME question (mid-build story
merge, avfl-on-merge phase label, e2e phase label) never zeroes the wait history Impetus has
accumulated in `resurface_count`; a transition to a NEW question (build -> end-gate approval,
end-gate -> closure verdict, request-changes redispatch -- the redispatch is a fresh waiting period per resume-card.md Resolution #2) starts a fresh wait ONLY on the FIRST
transition into that question: `resurface_count` is 0 and `waited_since` is re-bound. Re-entering
a new-question site while the card already holds that same question (a resumed end-gate, a repeat
closure refusal) is a same-question write and preserves both fields.

## Scenario

**Given:** A pending card for the question "Resume the sprint build" (`phase: "build"`) that
Impetus has surfaced twice, so `resurface_count: 2` and `waited_since` is a fixed timestamp T0.

**When (carry-forward):** The Conductor, still mid-build, merges another story and executes its
RESUME-CARD REFRESH (full-file overwrite), then later advances the phase label to `avfl-on-merge`
and `e2e` with further refreshes.

**Then:**

1. After each of these refreshes `resurface_count` still reads 2 and `waited_since` still reads T0.
2. Only `phase`, `merged`, and `blocked` change.

**When (reset):** The build finishes and the Conductor writes the end-gate question
("Approve merge to main and push to origin, or request changes?").

**Then:**

3. `resurface_count` reads 0 and `waited_since` is a fresh `NOW()`, later than T0 (the card's
   prior `question.text` differed, so this is the first transition into the end-gate question).
4. The same first-transition reset holds for the closure-verdict question when it replaces the
   end-gate question on the card, and for the request-changes redispatch re-write (the prior
   instance of the end-gate question was resolved "changes-requested").

**Given (same-question re-entry):** The card already holds the end-gate question, pending, with
`resurface_count: 2` and `waited_since` T1 (the session died at the ask and Impetus resurfaced it
twice). The Conductor resumes and re-reaches the end-gate RESUME-CARD REFRESH. Likewise, a card
that already holds the closure question with `resurface_count: 2` and `waited_since` T2, and the
Conductor re-attempts tier-2 closure on resume and is refused again.

**Then:**

5. `resurface_count` still reads 2 and `waited_since` is unchanged (T1 / T2) after the re-write.
6. Only fields that legitimately changed (e.g. `merged`/`blocked` slugs) differ.

**Given (resume after merged, repeat closure refusal):** The merge gate already recorded a
`merged` outcome. The card holds the closure question, pending, `resurface_count: 2`,
`waited_since` T2 (tier-2 closure was refused once; Impetus resurfaced it twice). A new session
resumes into Phase 5 and then re-attempts tier-2 closure, which is refused again.

**Then:**

7. The end-gate RESUME-CARD REFRESH is skipped (the MERGED-ON-RECORD GUARD): the card is not
   overwritten with the end-gate question, not re-pended, and no stale `waited_since` is carried.
8. The repeat closure refusal compares against the closure question already on the card, treats it
   as the SAME question, and leaves `resurface_count` at 2 and `waited_since` at T2.
9. A card already resolved "approved" stays resolved across this resume.

## Pass Criteria

Every same-question refresh -- including re-entry at an end-gate or closure site whose question is
already on the card -- preserves `resurface_count` and `waited_since` exactly; only the first
transition into a genuinely new question sets `resurface_count: 0` and a fresh `waited_since`.

## Fail Criteria

Any same-question refresh (including a resumed end-gate or repeat closure refusal) resets or
alters `resurface_count` or `waited_since`; any first transition into a new question carries a
prior count forward or reuses the old `waited_since`.

## Verification Method

Inspection of each RESUME-CARD REFRESH site in `workflow.md` for an explicit carry-forward
(same question) or reset-to-0 (new question) statement citing `references/resume-card.md`.
Subagent walkthrough: simulate the sequence against a fixture card and diff the file after each
write.
