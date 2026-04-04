# Eval: Tiered Review Depth

## Scenario

Given subagent findings arrive or a workflow step completes and presents results for review, Impetus must lead with a micro-summary of key decisions and outcomes, then offer tiered review depth. The full finding list is never the default presentation.

## Expected Behavior

- Findings presentation leads with a micro-summary: 1-3 sentences covering key decisions and outcomes
- After the micro-summary, Impetus offers three tiers:
  - **Quick scan** — summary only, no expansion (the micro-summary serves this purpose)
  - **Full review** — expand all findings with details
  - **Trust & continue** — accept findings and move forward without reviewing
- The tier choice is presented as a natural question, not a menu of codes
- Full findings are only expanded when the developer explicitly requests "full review"
- The developer is never overwhelmed with an unprompted full artifact dump

## NOT Expected

- Full finding list presented as the default without offering tiers
- Micro-summary absent — jumping straight to detailed findings
- Only two options offered instead of three
- Forced review — no option to trust and continue
- Menu-style presentation with letter codes for tier selection
