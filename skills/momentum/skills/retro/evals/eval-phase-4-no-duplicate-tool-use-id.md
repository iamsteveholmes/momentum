# Eval: Phase 4 Cannot Replicate Agents (Workflow-managed spawns)

## Scenario

Phase 4 of retro performs its auditor work via the dynamic audit Workflow — a **single** Workflow-tool
invocation — rather than the main loop hand-emitting multiple parallel `Agent` tool calls.

## Expected Behavior

Phase 4 makes exactly one Workflow-tool call. Every auditor, refuter, and the synthesizer is spawned
by the Workflow runtime (the `agent()` calls inside `audit-workflow.js`), which assigns each its own
managed spawn — two agents cannot share a `tool_use_id`. The historical single-call replication defect
(8–10 documenters sharing one `tool_use_id` on sprint-2026-04-08 / 04-10) is **structurally
impossible**, because the main loop no longer hand-emits a batch of `Agent` calls for Phase 4.

## Verification

1. `retro/workflow.md` Phase 4 contains a single Workflow-tool call and **no** foreground `Agent`
   fan-out for auditors/synthesizer.
2. In a real run, Phase-4 subagents appear under the Workflow runtime, each with a distinct identity;
   no two share a `tool_use_id`.

## Pass Condition

Phase 4 is a single Workflow invocation, and no two Phase-4 agents share a `tool_use_id`.

## Fail Condition

`retro/workflow.md` re-introduces hand-emitted parallel `Agent` spawns for Phase 4 (the configuration
that originally allowed single-call replication), or any two Phase-4 agents share a `tool_use_id`.

## Rationale

The original eval guarded against a main-loop footgun (multiple agents produced from one API call).
Moving Phase 4 into the Workflow tool removes the footgun by construction; this eval now asserts that
the Workflow-tool boundary is preserved and the hand-rolled fan-out is not reintroduced.
