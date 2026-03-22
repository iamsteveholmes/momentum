# Eval: Stub Accepts /momentum Invocation

## Scenario

Given a user invokes `/momentum` with no arguments in a Claude Code session where the `momentum` skill is installed, the skill should:

- Load without error (no missing required field)
- Respond to the user in a coherent, non-confusing way
- NOT attempt to run the full Impetus workflow (this is a stub — full implementation is Story 2.1)
- Communicate that Impetus is a placeholder pending Story 2.1

## Expected Behavior

The skill stub acknowledges the invocation and informs the user that the Impetus workflow will be available after Story 2.1 implementation. It does not crash, produce malformed output, or pretend to run the full orchestrator.
