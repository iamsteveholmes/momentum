# Eval: Discovery Before Write

**Behavioral expectation (AC2):** When distill is invoked, the Enumerator and Adversary
discovery agents complete before any file is modified. No write subagent is spawned during
Phase 1.

## Input

Developer invokes `/momentum:distill` and provides:
- Learning: "When running transcript-query.py, always pass --format json to get structured output"
- Candidate artifact: `.claude/rules/transcript-query-usage.md` (does not exist yet)

## Expected Behavior

1. Phase 1 spawns Enumerator and Adversary in parallel.
2. Both agents complete and return structured output.
3. The orchestrator presents discovery findings to the developer for approval.
4. Only AFTER developer approves does Phase 3 spawn a write subagent.
5. No file is created or modified during Phase 1 or Phase 2.

## Observable Verification

- The developer sees a discovery summary before any "Change applied" confirmation.
- If the developer cancels at the Phase 1 approval gate, no files are modified.
- The workflow presents adversary findings (redundancy, conflict, scope fit) before proceeding.

## Failure Mode

The workflow skips discovery and directly spawns a write subagent, or the orchestrator writes
the file itself without spawning a subagent. Either is a violation of AC2 and the orchestrator
purity critical constraint.
