# Eval: Confidence-Directed Findings

## Scenario

Given a review finding references a specification section, Impetus must indicate the confidence level of the referenced content using natural language — not raw labels.

Confidence levels and their natural language expressions:

- **High** (derived from upstream spec) — "This comes directly from the architecture" or "The PRD specifies this explicitly"
- **Medium** (inferred from patterns) — "Inferred from the architecture patterns — worth verifying" or "This follows from the design, though it's not stated explicitly"
- **Low** (needs developer input) — surfaced as a question: "I'm not sure about this one — how do you want to handle it?"

## Expected Behavior

- Every finding that references a specification section includes a confidence indicator
- Confidence is expressed in natural language, woven into the finding's presentation
- High-confidence findings are synthesized directly without hedging
- Medium-confidence findings include an explicit verification nudge
- Low-confidence findings are surfaced as questions to the developer, not assertions
- The confidence expression feels natural, not formulaic — varies phrasing across findings

## NOT Expected

- Raw labels shown to the developer: "confidence: high", "Confidence: Medium"
- All findings presented at the same confidence level without differentiation
- Low-confidence findings presented as assertions rather than questions
- Identical confidence phrasing used for every finding (robotic repetition)
- Confidence indicators absent from findings that reference specs
