# Workflow Fidelity

When executing a Momentum workflow (sprint-planning, sprint-dev, quick-fix, retro, or any skill with a workflow.md), every step is binding — not advisory.

## Delegation Is Not Optional

If a workflow step says "spawn X", "invoke X", or "run X" — do that. Do not:

- Do the work directly because "I already have the context"
- Skip the delegation because "it's faster to do it myself"
- Partially follow the step (e.g., write the file yourself instead of spawning the skill that writes it)

The delegation exists for separation of concerns, consistent quality, and auditability. Bypassing it breaks the practice.

## Parallelism Is Expected

When a workflow step delegates work for multiple independent items (e.g., "for each story, spawn create-story"), launch them in parallel when possible. Sequential execution of independent items wastes time.

## When a Delegated Skill Doesn't Exist

If the skill or agent referenced in a workflow step doesn't exist yet, stop and flag it to the developer before proceeding. Do not silently substitute your own implementation.
