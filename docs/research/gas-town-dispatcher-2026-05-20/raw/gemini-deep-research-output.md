---
content_origin: gemini-deep-research
date: 2026-05-20
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
method: chrome-mcp
note: "Full report title: 'Comprehensive Evaluation of Gas Town and Gas City for Momentum Agentic Engineering Orchestration'. Main body (34,962 chars) extracted in-session but not persisted due to Chrome HTTPS→HTTP mixed-content policy blocking localhost writes. Key findings are captured in the 8 raw research files. Follow-up Q&A pairs fully captured below."
---

# Gemini Deep Research Output
## Gas Town / Gas City as Momentum Dispatcher

**Report title:** Comprehensive Evaluation of Gas Town and Gas City for Momentum Agentic Engineering Orchestration

**Note on extraction:** The main Deep Research report body (~35k chars) was successfully generated and verified in the Gemini session (tab: https://gemini.google.com/app/9a2fc01fb40ced5e). Chrome's Private Network Access policy blocked the localhost exfiltration approach, and the MCP tool response cap (~1000 chars) made chunk-by-chunk extraction impractical. All 8 sub-question findings are covered by the parallel subagent raw files in this directory, which cross-validate the Gemini findings.

---

## Follow-up Q&A

### Follow-up 1: PackV1 → PackV2 Migration Status

**Question:** The Gas City SDK currently has an incomplete PackV2 migration and 262 open issues. What specifically is changing between PackV1 and PackV2 in the Gas City architecture? What is the expected timeline or current state of PackV2 stabilization as of May 2026? Is it safe to build integrations on Gas City Pack primitives today, or should adopters wait for PackV2 to land before committing?

**Answer:**

Based on the current development state of the Gas City SDK as of May 2026, here is the breakdown of the PackV1 to PackV2 migration, its stabilization timeline, and recommendations for adoption.

**What is changing between PackV1 and PackV2?**

The transition to PackV2 represents a fundamental shift from a monolithic configuration file to a decentralized, convention-based directory layout.

The specific architectural changes include:

*Separation of State:* The legacy model where "everything lives in city.toml" is deprecated. Under PackV2, portable definition logic (reusable behavior) belongs in pack.toml and pack-owned directories, city.toml handles deployment and site-binding choices, and the .gc/ directory stores machine-local runtime bindings.

*Named Imports over Includes:* The composition model has changed from textual includes to stable "named imports" (e.g., using [imports.<name>] in pack.toml or [rigs.imports.<name>] in city.toml).

*Convention-Based Directories:* Agent definitions and artifacts must now sit in strict, predictable directory paths rather than inline configurations. For example, agents use agents/<name>/agent.toml and agents/<name>/prompt.template.md. Workflows are moved to formulas/<name>.toml and orders/<name>.toml.

*Explicit Bootstrapping:* The legacy implicit registry and bootstrap artifacts have been retired. The explicit `gc import install` command is now the required path for initializing importable packs.

**Current State and Timeline (May 2026)**

Gas City 1.0 has officially been released, making PackV2 the active and default layout for the ecosystem. If an older 0.14.x city attempts to upgrade, developers must use the `gc doctor --fix` migration tooling to convert their setups.

However, the migration is considered "incomplete" because several advanced capabilities were intentionally deferred to "Post-PackV2" workflows (e.g., Issue #2120) to push the 1.0 release out.

*CLI and Doctor Extensibility:* The metadata models for custom CLI commands (command.toml) and system checks (doctor.toml) are still under-specified. The core team is currently freezing the basic run.sh entrypoint contracts while they decide what those broader manifest shapes will permanently look like.

*Skills and MCP:* First-class, provider-native runtime support for Skills and the Model Context Protocol (MCP) was explicitly cut from the initial PackV2 rollout and deferred to follow-on work.

**Is it safe to build on Gas City today?**

Yes, it is safe to build, provided you build natively on the PackV2 standard. Because Gas City 1.0 establishes PackV2 as the active layout, waiting for the "entire" migration to clear is unnecessary for core orchestration tasks.

However, Momentum adopters should navigate the current gaps with specific guardrails:

- *Adopt the new directories immediately:* Start your integration using pack.toml, city.toml, and the new agents/ and formulas/ directory conventions. Do not attempt to build on the deprecated PackV1 city.toml monolith.
- *Avoid custom command manifests:* If you need to build custom Gas City CLI extensions or doctor checks, stick to the frozen default of dropping executable run.sh scripts into commands/<path>/ or doctor/<path>/. Avoid relying heavily on command.toml schemas until the core team finalizes their collision policies and long-term definitions.
- *Hold off on native MCP integration:* If your Momentum sub-agents rely heavily on standardized Model Context Protocol toolchains, be aware that Gas City does not yet offer full runtime support for them. You will need to handle MCP tool execution independently at the agent level (e.g., within Claude Code's native configuration) until Gas City ships its follow-on MCP updates.

---

### Follow-up 2: Orders System Event Model / External Triggers

**Question:** Can the Gas City Orders system be triggered by external events outside the Beads graph — such as GitHub webhooks, CI/CD pipeline events, file system watches, or HTTP callbacks? Or are Orders strictly triggered by internal Beads state changes (new beads created, status transitions, etc.)? What is the exact event model for Order dispatch?

**Answer:**

The Gas City Orders system is not strictly limited to internal Beads state changes, but it also does not natively act as an inbound listener for external HTTP webhooks or callbacks. Instead, it relies on an internal pub/sub model and a polling loop.

**The Controller and Event Bus**

The dispatch mechanism is managed by the Gas City Controller, which operates on a continuous main loop consisting of a config watch, a reconciliation tick, and order dispatch. The Controller watches the "Event Bus," which is an append-only pub/sub log of all system activity, separate from the durable Beads storage.

**Trigger Conditions**

An Order (whether it executes a shell script or an agent workflow formula) fires based on a defined "trigger condition" evaluated by the Controller. These triggers are not just reactive to the Beads graph; they can be based on:

- Specific event types occurring on the Event Bus
- Schedules (cron-like timing)
- Manual, explicit invocations

**Handling External Events (CI/CD, Webhooks)**

Because Gas City does not natively expose an HTTP endpoint to catch webhooks, external events must be bridged into the system using one of two patterns:

*The Push Pattern:* Your external CI/CD pipeline or webhook handler uses the Gas City/Beads CLI to push a state change or write an event directly into the system. The Controller's reconciliation tick observes this new system activity on the Event Bus and triggers the corresponding Order.

*The Pull/Condition Pattern (exec orders):* If you need Gas City to watch an external system (like a file system or an external API), you can define an exec order. An exec order runs controller-side shell logic directly without spinning up or consuming an AI agent session. You can use this to poll external endpoints or evaluate custom conditions; if the shell script condition is met, it triggers the workflow while retaining full execution history and controller ownership.

---

### Follow-up 3: Human Gate Observability / HITL UX

**Question:** The human gate system in Gas Town (bd gate create --await human:X / gt park / bd gate approve) is pull-based with no proactive dashboard. Are there any existing mechanisms, planned features, or community patterns for proactively notifying the developer when human gates are pending — such as TUI dashboards, email/Slack notifications, or terminal popups — so developers don't need to constantly poll the terminal? What does the current human oversight UX actually look like in practice?

**Answer:**

The current human oversight UX in Gas Town revolves primarily around asynchronous terminal commands and a web-based tracker, rather than proactive push notifications out-of-the-box. When a human gate is triggered, the agent parks its work and the developer must either check their in-system mail (`gt mail inbox`) or run `gt ready` to see what work is waiting for approval across the town. For continuous visual tracking, developers use the web-based convoy dashboard (`gt dashboard`), which auto-refreshes to show the real-time status and blockers of batched work.

Because Gas Town and Gas City use a loosely coupled architecture, they intentionally leave proactive, out-of-band notifications up to the agent layer or modular extensions. To prevent constant terminal polling, developers rely on a few established patterns:

*Agent-Level Desktop Hooks:* The most common practice is to configure notifications directly within the underlying coding agent. For example, Claude Code supports lifecycle "stop hooks" configured via its settings.json file. Developers use these to trigger native desktop notifications (e.g., using osascript on macOS) or sound alerts the exact moment the agent parks and waits for human input.

*Tmux Status Integrations:* Since Gas Town relies heavily on tmux for process isolation, power users often pair agent-level stop hooks with commands like `tmux display-message` to visually highlight the specific terminal window and pane that requires the Overseer's attention.

*Gas City Ecosystem Packs:* For team-wide notifications, the Gas City SDK modularizes this capability. The gascity-packs repository includes a slack-pack, allowing the orchestration layer to route notifications and human-gate alerts directly to Slack channels when an external condition requires intervention.

*Community Mobile Tools:* For remote oversight, community tools like Moshi (an iOS terminal built for agentic workflows) offer webhook-based push notifications, pinging the developer's phone when an agent finishes a task or hits a gate requiring human input.

In practice, a mature Momentum setup would likely combine the Convoy web dashboard for high-level sprint tracking with agent-level desktop hooks or the Gas City slack-pack to proactively alert the human "Overseer" when critical deployment gates or escalations require immediate approval.

**Sources cited by Gemini:**
- https://docs.gastownhall.ai/usage/diagnostics
- https://docs.gastownhall.ai/usage
