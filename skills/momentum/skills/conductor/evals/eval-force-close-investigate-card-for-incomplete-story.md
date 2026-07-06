# Eval: Force-close-or-investigate card for every incomplete story

**Skill under test:** `momentum:conductor` (Phase 5 end-gate renderer, §04 decision cards)
**Renderer spec:** `skills/momentum/skills/conductor/references/endgate-report-renderer.md`

## Scenario

**Given (blocked sprint):** A sprint build completes with 4 stories merged and 1 story blocked
(`event-logging`). The blocked story could not complete due to a persistent dependency failure.
The build ledger contains a `story-terminal` row for `event-logging` with `outcome: "blocked"`.

**Given (clean sprint):** A second scenario: all 4 stories merged. No `story-terminal` rows with
non-merged outcomes.

**When:** The Conductor renders the end-gate HTML at Phase 5.

**Then (blocked sprint):**

1. The `event-logging` story surfaces a **force-close-or-investigate** decision card in §04.
2. The card carries **what** (the story did not merge; the specific blocker is stated), **why-it-matters**
   (the capability is unshipped; dependent work may be blocked), and **evidence** (build ledger outcome
   and failure reason — inline, not a "see the ledger" deferral).
3. The card offers exactly **two options**: Option A = Force-close as `closed-incomplete`; Option B = Investigate.
4. No option is pre-selected.
5. The gate's approve control remains disabled until this card is acknowledged and an option is selected.

**Then (clean sprint):**

6. No force-close-or-investigate card is rendered for incomplete stories.
   §04 either states "No decisions required" or contains only stakes-class finding cards (if any).

## Pass Criteria

- Every non-shipped story generates a decision card with all three fields (what, why, evidence) present inline
- Each card offers exactly Force-close (A) and Investigate (B), nothing pre-selected
- A clean sprint renders no incomplete-story cards
- Approve is blocked until each incomplete-story card is acknowledged with an option selected

## Fail Criteria

- A non-shipped story has no decision card
- A card is missing what, why, or evidence (dev must open a separate file to understand it)
- Approve submits without card acknowledgment
- The card offers only one option, or has a pre-selected default
- A clean sprint renders spurious incomplete-story cards

## Verification Note

Verified by inspecting the renderer spec §3 spine and §5 decision-card data contract: the
force-close card type must be specified with what/why/evidence fields and the two-option structure
(A = Force-close, B = Investigate). The paint() function must reference these cards. The clean-sprint
path must be explicitly stated. This eval does not require a live run — spec inspection is sufficient.
