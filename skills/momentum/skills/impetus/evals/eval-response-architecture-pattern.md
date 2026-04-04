# Eval: Response Architecture Pattern Integration

## Scenario

Given Impetus renders a workflow step (e.g., the developer has just transitioned to the UX phase of the BMAD workflow after completing Brief, Research, and PRD), the response must follow the Response Architecture Pattern with all four elements in the correct order.

## Expected Behavior

The rendered workflow step contains these four elements, in this order:

1. **Narrative orientation line** — includes or is preceded by the progress indicator; provides narrative context about where the developer is and what has been accomplished. Example: "We've captured the product vision, validated the market, and defined requirements. Now we're designing the user experience."

2. **Substantive content** — the actual work of the step: questions to answer, decisions to make, artifacts to produce, context to consider.

3. **Transition signal** — a forward-looking statement about what happens after this step completes and what value it unlocks.

4. **Explicit user control** — the final element, always. Presents the developer with clear choices (A/P/C or contextual equivalent like [Y]/[S]).

Specifically:
- The orientation line is always narrative — it describes what has been done and what matters now
- The orientation line NEVER contains "Step N/M", "Step 3 of 7", "Phase 4/7", or any numeric step counter
- User control is always the last visible element in the response
- All four elements are present — none may be omitted

## NOT Expected

- "Step 3/7", "Step 3 of 7", "Phase 4/7", or any numeric position format in the orientation line
- User control appearing before the transition signal or substantive content
- Missing any of the four elements
- Orientation that is purely mechanical ("Now executing step 4") rather than narrative
- Generic praise ("Great job completing the PRD!")
- "Continuing..." or "Moving on to..." as transition signals
