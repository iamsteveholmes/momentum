# Model Routing

## Default

Use Sonnet 4.6 at medium effort unless the task matches an override below.

## When to use Opus

- Multi-file refactoring or complex code generation
- Multi-agent orchestration (orchestrator role)
- Novel reasoning or analysis requiring high accuracy
- Outputs that a human will review without automated validation (the cognitive hazard rule: invisible errors cost more than the price premium)

## When to use Haiku

- Data extraction, classification, simple routing decisions
- Sub-agent search and exploration tasks
- Any well-constrained task with deterministic downstream validation

## Effort Levels

- **max**: Opus only. Hardest reasoning problems.
- **high**: Complex tasks, agentic workflows. API default for both Opus and Sonnet.
- **medium**: General-purpose balance. Recommended starting point for Sonnet.
- **low**: Simple lookups, classification, high-volume sub-agent calls.

## Retry Economics

Cap retry loops at 4-5 iterations. If a model fails to converge after 3-4 attempts, escalate to the next tier rather than burning tokens at the same tier. Context accumulation makes later iterations more expensive, not less.

## Reference

See module/canonical/resources/model-routing-guide.md for the full decision matrix, task-type mapping, cost comparison, and cognitive hazard evidence.
