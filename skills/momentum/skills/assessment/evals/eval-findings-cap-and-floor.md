# Eval: Assessment finding cards respect the cap and carry the self-sufficiency floor

**Surface under test:** Step 3 finding presentation — each confirmed finding presented to the developer for validation.

**Standard:** Decision-Grade Presentation Standard (`skills/momentum/references/rules/decision-grade-presentation.md`)

## Scenario

**Given:** An assessment has completed discovery and produced findings, including at least one actionable finding (a gap or risk requiring developer attention) and at least one routine finding (a clean item with no action required).

**When:** The skill presents each finding to the developer for validation (Step 3 of the workflow).

**Then:**

1. **Cap respected:** Each finding presentation leads with a ≤ 1 sentence lead-in (the headline). Supporting detail follows — it does not precede the headline.
2. **Bullet cap respected:** If the finding includes a list, it contains ≤ 7 items. Routine or clean sub-items are collapsed to a count rather than itemized.
3. **Exec-summary-first:** The headline/point of the finding appears first. Background context appears after.
4. **Floor present (actionable findings only):** Every finding the developer must act on carries all three inline — what it is, why it matters, and the supporting evidence. The developer can understand and validate the finding without opening any file or recalling prior context.
5. **Routine findings collapsed:** Any finding that is clean or requires no action is summarized in ≤ 1 sentence rather than expanded.

## Pass Criteria

- The finding presentation leads with its headline (not background)
- Any actionable finding carries what / why-it-matters / evidence inline — all three present, none deferred
- Routine findings are collapsed to a short summary, not expanded

## Fail Criteria

- An actionable finding is presented without its what, or without its why-it-matters, or without its evidence — the developer must open a file or recall context to understand it
- A finding leads with background context before stating the headline
- A list within a finding exceeds 7 bullets without collapsing the routine items

## Verification Note

This eval is verified by inspection of the skill output in a representative session. The verifier presents an assessment scenario with at least one actionable and one routine finding, reads the Step 3 output, and confirms:
- Count the sentences in the lead-in (must be ≤ 1)
- Confirm what/why/evidence are all present inline for the actionable finding
- Confirm the routine finding is collapsed, not expanded

This eval does NOT check exact wording — it checks the presence and structure of the required elements.
