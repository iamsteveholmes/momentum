# Eval: Plan Gate — Anti-Rubber-Stamp Sign-Off and Genuine Fork Cards

**ID:** eval-plan-gate-anti-rubber-stamp-and-fork-cards
**Change-type:** skill-instruction
**Phase:** developer review (Step 7) — sign-off gate + decision card content

## Scenario A: Gate with genuine forks — blanket approve is insufficient

Given a plan gate that contains 2 genuine forks (stories with unresolved AVFL warnings or
same-wave touch overlaps)

When the developer attempts to approve by selecting the "Approve" radio without filling in any
per-fork verdict text

Then:
1. The submit/copy button remains disabled (cannot be activated)
2. A hint message indicates the missing per-fork verdicts
3. The gate does NOT proceed to activation until both fork verdict fields carry written text

When the developer fills in a one-line verdict for each fork AND selects "Approve"

Then:
1. The submit button enables
2. The decision text includes both fork verdicts (not just "APPROVE")

## Scenario B: Clean plan path — zero forks enables batch approve without per-fork forcing

Given a plan gate where AVFL returned CLEAN and no genuine forks were detected
(all stories are `✓ batch`)

When the developer reviews the gate

Then:
1. No per-fork verdict text fields are rendered (nothing to fill in)
2. Selecting "Approve" radio enables the submit button without requiring any additional written text
3. The gate is not artificially forced when there are no genuine decisions

## Scenario C: Genuine fork card carries all five required fields inline

Given a plan gate with one genuine fork (e.g., two stories touch the same file in Wave 1)

When a reader inspects the decision card for that fork

Then:
1. The card contains a `What` field stating the concrete thing at stake (no bare "per story-a" handle)
2. The card contains a `Why it matters` field explaining the stakes if unaddressed
3. The card contains an `Evidence` field with a checkable detail (file path or story slug count)
4. The card contains a `Recommendation` field stating the defaulted call in one line
5. The card contains an `Options` field listing the resolution paths (e.g., Approve as specified /
   Modify scope / Remove from sprint)
6. ALL five fields are present; none are blank or omitted

## Scenario D: The gate links to story files rather than inlining them

Given a plan gate for a 3-story sprint

When a reader looks for the full detail of story `my-story-slug`

Then:
1. The gate contains an `<a href="file://…/my-story-slug.md">` or `<a href="file://…/my-story-slug.*">` link
2. The full body of `my-story-slug.md` (its ACs, Dev Notes, Tasks) does NOT appear as inline text in the gate
3. The machine band detail is reachable via the link, not embedded in the review surface

## Pass Criteria

- With forks: submit button disabled when fork verdict fields are empty
- With forks: submit button enables after all fork verdicts are filled
- Zero forks: submit button enables on radio selection alone (no blank-filling required)
- Each fork card has all five fields: What, Why it matters, Evidence, Recommendation, Options
- Story links point to canonical `.md` files; story body is not inlined

## Fail Criteria

- Gate can be approved in one click without any written text when genuine forks exist
- A fork card is missing one or more of the five required fields
- Fork card references a decision by handle only ("per DEC-036") without inlining the substance
- Full story AC text appears inline in the gate body
