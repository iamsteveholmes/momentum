# Eval: NL Gate "Yes" Dispatches Immediately Without Re-Triggering

## Setup

Impetus has presented the main menu. Developer types: "yeah let's pick up the test infra work". Impetus confirms: "Resuming the test infrastructure thread — correct?" Developer responds: "yes" (or "go ahead", "proceed", "sure").

## Expected Behavior

Impetus immediately dispatches to the identified workflow or thread. No second confirmation, no "are you sure?", no follow-up question. The fuzzy-continue words ("yes", "go ahead", "proceed", "sure") in response to a confirmation prompt confirm the action — they do not re-trigger the NL gate.

## Fail Conditions

- Impetus asks a second confirmation ("Are you sure?")
- Impetus treats the "yes" as new natural language input and re-triggers the gate
- Impetus asks any follow-up question before dispatching
- Impetus fails to dispatch after receiving confirmation
