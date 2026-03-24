# Eval: Input Fuzzy Match

## Setup

Impetus has just presented a workflow step with a continue option. Developer types: "yeah let's keep going"

## Expected Behavior

Impetus interprets the input as C (continue) and proceeds to the next step without asking for clarification.

## Fail Conditions

- Impetus asks what the user means or treats input as ambiguous
- Impetus fails to continue and instead re-presents the current step
- Impetus asks a clarifying question about the intent
