# Eval: Decision cards respect the cap and carry the self-sufficiency floor

**Surface under test:** Step 2 decision card — each adopt/reject/defer item presented to the developer for a verdict.

**Standard:** Decision-Grade Presentation Standard (`skills/momentum/references/rules/decision-grade-presentation.md`)

## Scenario

**Given:** The decision skill is walking through a set of findings/recommendations for adopt/reject/defer decisions. The set includes at least one substantive item (one the developer genuinely needs to decide about, not a trivial or already-decided item).

**When:** Each item is presented to the developer for a decision (Step 2 of the workflow).

**Then:**

1. **Exec-summary-first:** The headline (what is being decided) appears first. The verdict or recommendation follows. Background rationale appears after the headline and verdict — never before.
2. **Cap respected:** The decision presentation is ≤ 5 lines of prose plus ≤ 3 supporting bullets. It does not expand beyond this budget by providing extensive context before the decision point.
3. **Floor present:** The decision item carries all three inline — what is at stake, why it matters for the project, and the evidence or reasoning behind the recommendation. The developer can make an informed adopt/reject/defer decision without opening the source document.
4. **Positive-concision:** The presentation states what IS the case (the finding, the recommendation) rather than leading with extensive framing of what isn't the case.

## Pass Criteria

- The headline (what is being decided) is the first content element — not background or setup prose
- The decision presentation stays within ≤ 5 prose lines + ≤ 3 bullets
- What / why-it-matters / evidence are all present inline — the developer is self-sufficient on this surface

## Fail Criteria

- The headline appears after multiple lines of background context
- The presentation exceeds its budget (> 5 prose lines or > 3 bullets for a single item)
- The developer must consult the source document to understand what is being decided or why it matters — any of what/why/evidence is missing from the surface

## Verification Note

This eval is verified by inspection. The verifier presents a decision scenario with at least one substantive finding, reads the Step 2 output for each item, and confirms:
- The headline comes first (not after setup prose)
- The prose block is ≤ 5 lines and bullet list is ≤ 3 items
- All three of what/why/evidence are present inline

This eval does NOT check exact wording — it checks ordering, budget, and completeness of the required elements.
