# Eval: Input Fuzzy Match

## Setup

Impetus has just presented a workflow step with a continue option. Test each of these developer inputs independently:

1. "yeah let's keep going"
2. "sure"
3. "yep, proceed"
4. "ok"

## Expected Behavior

For each input above, Impetus interprets it as C (continue) and proceeds to the next step without asking for clarification. All fuzzy-continue variants are treated equivalently.

## Fail Conditions

- Impetus asks what the user means or treats any of the above inputs as ambiguous
- Impetus fails to continue and instead re-presents the current step
- Impetus asks a clarifying question about the intent for any recognized fuzzy-continue phrase
- Impetus treats some fuzzy variants differently than others (e.g., proceeds for "yes" but asks about "yep")
