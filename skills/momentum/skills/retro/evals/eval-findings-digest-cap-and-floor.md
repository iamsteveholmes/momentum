# Eval: Retro findings digest respects the cap and carries the self-sufficiency floor

**Surface under test:** Phase 4-5 findings presentation — the findings the developer reviews for approval as story stubs.

**Standard:** Decision-Grade Presentation Standard (`skills/momentum/references/rules/decision-grade-presentation.md`)

## Scenario

**Given:** A retrospective has completed the transcript audit (Phase 4) and produced findings. The findings include at least one actionable finding (something the developer should approve as a story stub) and multiple routine findings (process observations, minor inefficiencies, already-resolved items).

**When:** The skill presents the findings to the developer for stub approval (Phase 5 of the workflow).

**Then:**

1. **Cap respected:** The developer-facing findings digest surfaces ≤ 7 actionable findings. Routine and clean findings are collapsed to a count rather than itemized ("N routine observations not actioned").
2. **Floor present (actionable findings):** Every finding presented for stub approval carries all three inline — what it is, why it matters to the practice, and the evidence from the audit. The developer can approve or reject the stub without reading the full audit document.
3. **Exec-summary-first:** Each finding leads with the headline (what it is and its suggested action). Supporting detail follows.
4. **Routine findings collapsed:** Findings that do not require a story stub are summarized as a count, not listed individually.

## Pass Criteria

- The digest surfaces ≤ 7 actionable findings (countable)
- Routine findings appear as a count line, not itemized
- Each actionable finding carries what / why-it-matters / evidence inline
- Headlines precede supporting detail in each finding

## Fail Criteria

- The digest lists more than 7 actionable findings without collapsing any routine items
- Routine findings are itemized rather than counted
- An actionable finding is presented without its what, or without its why-it-matters, or without its evidence — requiring the developer to read the audit document to understand it
- Supporting detail precedes the headline

## Verification Note

This eval is verified by inspection of the skill output in a representative retro session. The verifier identifies the Phase 5 approval surface and confirms:
- Count the actionable findings (must be ≤ 7)
- Confirm routine findings are collapsed to a count, not listed
- For each actionable finding: confirm all three of what/why/evidence are present inline

This eval does NOT check exact wording — it checks the structure and completeness of the required elements.
