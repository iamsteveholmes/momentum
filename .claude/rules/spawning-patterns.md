# Spawning Patterns: Fan-Out vs TeamCreate

Two patterns exist for parallel agent work. Choose based on whether agents need to communicate during execution.

## Fan-Out (Individual Agent Spawns)

Use when agents work **independently** and return results to the orchestrator.

- Multiple `Agent` tool calls in a single message
- Each agent gets its own prompt, does its work, returns output
- Orchestrator collects results and decides next steps
- No inter-agent communication — agents don't know about each other

**When to use:**
- Dev wave: each story is independent
- AVFL validators: each lens validates independently
- Research queries: each question is independent
- Any "do N things in parallel and collect results"

## TeamCreate (Collaborative Team)

Use when agents need to **talk to each other** during execution via SendMessage.

- Single `TeamCreate` call, then spawn agents with `team_name`
- Agents communicate via `SendMessage` — iterative back-and-forth
- Agents can ask each other to dig deeper, clarify, or correlate findings
- Work product emerges from collaboration, not just collection

**When to use:**
- Retro auditor team: documenter asks auditors to investigate further
- Sprint review team: QA briefs E2E on spec changes mid-review
- Any "collaborate on a shared problem with iterative refinement"

## Decision Rule

> **Can each agent complete its work without talking to any other agent?**
> - Yes → Fan-out (individual Agent spawns)
> - No → TeamCreate

Do not default to TeamCreate because it was used earlier in the session. Each spawn point is an independent decision.
