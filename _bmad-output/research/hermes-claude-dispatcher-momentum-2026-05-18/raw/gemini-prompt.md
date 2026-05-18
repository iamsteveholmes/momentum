Research Topic: Hermes (Nous Research agent) as a 24/7 dispatcher/delegate working with Claude Code as the planner, and Hermes Kanban + worker lanes integration with an agentic engineering practice ("Momentum").

I need a comprehensive analysis of whether Hermes can run as an always-on delegate/executor while Claude Code remains the planner/"brains", and whether the Hermes Kanban board and worker lanes can map onto a sprint/epic/story/wave + dependency-graph workflow.

Research Goals: Decide whether to adopt Hermes-as-delegate vs a Claude-native beads+Channel/SDK background dispatcher, and whether the Hermes Kanban/lanes model fits a Claude-Code-skill-centric practice. Constraints: local-only preference, cost sensitivity.

Key questions to investigate:

1. What is Hermes (Nous Research's agent) — runtime architecture, models, local-vs-hosted deployment, 24/7 autonomy model, license, and cost?
2. How does the Hermes Kanban board work — board/column/card model, task lifecycle, creation/claim/progress, persistence? (see https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban and https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial )
3. What are Hermes worker lanes — definition, parallelism, lane assignment, dependency/ordering semantics? (see https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes )
4. What is Hermes's external integration and callback surface — APIs, webhooks, events, MCP, CLI — for an external system to start tasks and for Hermes to communicate back on significant change; is it local-capable?
5. Is a "Claude Code plans/brains, Hermes delegates/executes 24/7, Hermes signals back on significant change" contract feasible — handoff protocol, state ownership, the significant-change trigger, failure modes?
6. Can Hermes Kanban + worker lanes map onto a sprint/epic/story/wave + dependency-graph + intake-queue model — structural/semantic fit, impedance mismatches, source-of-truth ownership?
7. How does a Hermes-based dispatcher compare to a Claude-native background dispatcher on local-only operation, cost, autonomy, capability, operational risk, and maturity?
8. Cost, deployment, maturity, and risk of Hermes — local vs cloud, who pays inference, model requirements, project maturity (use commit cadence/contributors/downloads, NOT GitHub stars), data-governance, solo-dev viability?

Desired output: A structured report organized by question, with specific actionable recommendations, example integration patterns where relevant, citations with URLs for every factual claim, and an honest assessment of current limitations and gaps.

Date context: Today is 2026-05-18. Prioritize current and recent sources.
