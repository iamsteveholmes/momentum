# Eval: Stub Does NOT Implement Impetus Workflow

## Scenario

Given a user invokes `/momentum` with a complex request (e.g., "orient me for this session"), the skill should NOT:

- Attempt to orchestrate session orientation (Story 2.1 scope)
- Claim to have run sprint-status checks
- Fabricate workflow steps that don't exist yet

The skill SHOULD:

- Acknowledge the invocation
- Clearly indicate it is a stub pending Story 2.1 implementation
- Suggest the user can still run individual skills directly (e.g., `/momentum:create-story`, `/momentum:dev`)

## Expected Behavior

The stub responds with a simple placeholder message. It does not hallucinate workflow steps or pretend to be the full orchestrator.
