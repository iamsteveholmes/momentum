---
topic: "Can Hermes run as a 24/7 dispatcher/delegate with Claude Code as planner/brains, and can Hermes Kanban + worker lanes map onto Momentum?"
goals: "Decide whether to adopt Hermes-as-delegate vs the Claude-native beads+Channel/SDK dispatcher already designed, and whether the Hermes Kanban/lanes model fits Momentum's sprint/epic/story/wave + beads dependency graph + intake-queue. Constraints: local-only preference, cost sensitivity, Claude-Code-skill-centric practice."
profile: heavy
date: 2026-05-18
sub_questions:
  - "What is Hermes (Nous Research's agent) — runtime architecture, models, local-vs-hosted deployment, 24/7 autonomy model, license, and cost?"
  - "How does the Hermes Kanban board work — board/column/card model, task lifecycle, creation/claim/progress, and persistence?"
  - "What are Hermes worker lanes — definition, parallelism, lane assignment, and dependency/ordering semantics?"
  - "What is Hermes's external integration and callback surface — APIs, webhooks, events, MCP, CLI — for an external system (Claude Code) to start tasks and for Hermes to communicate back on significant change, and is it local-capable?"
  - "Is the 'Claude Code plans/brains, Hermes delegates/executes 24/7, Hermes signals back on significant change' contract feasible — concrete handoff protocol, state ownership, the significant-change trigger, and failure modes?"
  - "Can the Hermes Kanban board and worker lanes map onto Momentum's model (sprints/epics/stories/waves, beads dependency graph, intake-queue) — structural/semantic fit, impedance mismatches, source-of-truth ownership?"
  - "How does a Hermes-based dispatcher compare head-to-head with the Claude-native beads+Channel/SDK dispatcher (docs/research/claude-code-background-dispatcher-2026-05-17.md) on local-only, cost, autonomy, capability, operational risk, and maturity?"
  - "What are the cost, deployment, maturity, and risk realities of Hermes — local vs cloud, who pays inference, model requirements, project maturity (real signals not stars), data-governance, and solo-dev viability?"
---

# Research Scope: Hermes as a 24/7 dispatcher/delegate for a Claude-Code-planned Momentum practice

**Date:** 2026-05-18
**Profile:** heavy
**Goals:** Decide whether to adopt Hermes-as-delegate vs the Claude-native beads+Channel/SDK dispatcher already designed, and whether the Hermes Kanban/lanes model fits Momentum's sprint/epic/story/wave + beads dependency graph + intake-queue. Constraints: local-only preference, cost sensitivity, Claude-Code-skill-centric practice.

## Sub-Questions

1. What is Hermes (Nous Research's agent) — runtime architecture, models, local-vs-hosted deployment, 24/7 autonomy model, license, and cost?
2. How does the Hermes Kanban board work — board/column/card model, task lifecycle, creation/claim/progress, and persistence?
3. What are Hermes worker lanes — definition, parallelism, lane assignment, and dependency/ordering semantics?
4. What is Hermes's external integration and callback surface — APIs, webhooks, events, MCP, CLI — for an external system (Claude Code) to start tasks and for Hermes to communicate back on significant change, and is it local-capable?
5. Is the "Claude Code plans/brains, Hermes delegates/executes 24/7, Hermes signals back on significant change" contract feasible — concrete handoff protocol, state ownership, the significant-change trigger, and failure modes?
6. Can the Hermes Kanban board and worker lanes map onto Momentum's model (sprints/epics/stories/waves, beads dependency graph, intake-queue) — structural/semantic fit, impedance mismatches, source-of-truth ownership?
7. How does a Hermes-based dispatcher compare head-to-head with the Claude-native beads+Channel/SDK dispatcher (docs/research/claude-code-background-dispatcher-2026-05-17.md) on local-only, cost, autonomy, capability, operational risk, and maturity?
8. What are the cost, deployment, maturity, and risk realities of Hermes — local vs cloud, who pays inference, model requirements, project maturity (real signals not stars), data-governance, and solo-dev viability?
