---
content_origin: claude-code-subagent
date: 2026-05-20
sub_question: "What human-in-the-loop oversight and approval primitives does Gas Town expose?"
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

## Overview

Gas Town takes a deliberate philosophical stance on human oversight: **autonomy with structured escalation, not approval-first gating.** The system is designed around the assumption that humans should be freed from constant supervision duty — agents run independently, surface blockers through a tiered escalation chain, and humans interact as overseers of outcome rather than approvers of every action. This makes Gas Town's HITL model fundamentally different from systems that require pre-approval at workflow boundaries.

For Momentum integration, the key question is whether Gas Town's approval primitives are expressive enough to cover Momentum's existing human-approval requirements (git push confirmation, major planning decisions) without requiring the developer to be perpetually on-call. The answer is nuanced: the primitives exist, but they require compositional wiring — Gas Town does not ship a "Momentum-shaped" approval UI out of the box.

---

## The Overseer Hierarchy

Gas Town's human-in-the-loop model is anchored in a three-tier agent hierarchy with an explicit human seat at the top.

**Overseer** — The human operator. This is the only role that is definitionally human. The Overseer assigns work, monitors fleet health, and receives escalations that no automated tier could resolve. The term appears in escalation routing as the final backstop: CRITICAL-severity escalations are routed to the Overseer via email and SMS in the default configuration. There is no UI for the Overseer beyond the CLI and whatever notification channels are configured in `escalation.json`. [OFFICIAL]

**Mayor** — The primary AI coordinator and the human's closest agent interlocutor. The Mayor is a Claude Code instance with full workspace context. Recommended workflow: the human describes objectives to the Mayor → Mayor breaks down to beads/convoys → polecats execute → Mayor surfaces results. The Mayor also receives HIGH and MEDIUM escalations, effectively serving as a buffer so that the Overseer only sees truly critical issues. In practice, reviewers note the Mayor itself sometimes needs manual prodding, weakening this buffer. [OFFICIAL, PRAC]

**Deacon** — An infrastructure-level patrol agent that handles the majority of routine escalation routing. Deacon receives most initial escalations, resolves what it can autonomously, and forwards upward. Deacon also runs the heartbeat watchdog chain and is the first tier a stuck polecat contacts. [OFFICIAL]

**Witness** — Rig-level health monitor for polecats. The Witness detects stalled or zombie polecats, nudges them, and recycles sessions. Witness does NOT interrupt mid-step execution — it can detect and nudge but cannot force-cancel a step in progress. Witness escalates to Mayor when it cannot recover a polecat autonomously. [OFFICIAL]

This chain means the Overseer (human) receives escalations only when: (a) Deacon couldn't resolve it, AND (b) Mayor couldn't resolve it. In the nominal happy path, the human is not involved at all during execution — only in work assignment and post-hoc review.

---

## Approval Primitives

### Gate-Based Human Approvals (`bd gate` / `gt park` / `gt gate wake`)

The most explicit HITL primitive is the **gate system**. Gates are async coordination checkpoints that can represent:

- `timer:30m` — wait for a time interval
- `gh:run:123456789` — wait for a CI run
- `human:deploy-approval` — wait for a human to explicitly approve

Human gates (`--await human:<label>`) cause the agent to call `gt park <gate-id>`, which saves the current work state, marks the agent as a gate-waiter, and exits the session cleanly. The agent does not consume LLM tokens or hold a session open while waiting. When the human is ready to unblock the work, they call `bd gate approve <gate-id>`, which closes the gate and sends wake mail to all waiters via `gt gate wake`. The agent resumes with `gt resume --handoff`, restoring parked context.

This is Gas Town's closest equivalent to Momentum's current "developer must confirm before push" pattern. It is fully general — any workflow step can declare a human gate before proceeding. The limitation is **pull, not push**: the human must know to check for pending gates. Gas Town does not currently expose a dashboard view that says "3 human approval gates are waiting for you." The Overseer must proactively run `bd gate list` or rely on escalation mail routing to discover pending gates. [OFFICIAL]

### Escalation Commands (`gt escalate`)

```
gt escalate "Description"                  # MEDIUM severity (default)
gt escalate -s CRITICAL "msg"              # P0 — email + SMS
gt escalate -s HIGH "msg" -m "Details"     # P1 — mail to Mayor
gt escalate -s MEDIUM "msg"               # P2 — mail to Deacon
```

Severity maps to notification routing via `escalation.json`. The default configuration documented is:

- **low**: bead only (no notification)
- **medium**: bead + mail to Mayor
- **high**: bead + mail to Mayor + email to human
- **critical**: bead + mail to Mayor + email + SMS to human

Each escalation creates a structured **bead** (Gas Town's immutable record type) that functions as both audit trail and async communication channel. Humans respond to escalations by commenting on the bead, and can reassign work to the original polecat afterward. [OFFICIAL]

**Acknowledgment workflow**: The human calls `gt escalate ack <bead-id>` to acknowledge receipt. This prevents re-escalation during investigation. If an escalation goes unacknowledged for 4 hours (configurable), the system automatically bumps severity and re-routes, creating pressure without polling. Closure is signaled via `gt escalate close <bead-id>` with an optional resolution note. [OFFICIAL]

### Work Completion Signals (`gt done --status`)

When a polecat completes a work unit, it signals completion status explicitly:

- `COMPLETED` — Work done, merge request submitted (default)
- `ESCALATED` — Hit a blocker requiring human intervention
- `DEFERRED` — Work paused, issue still open
- `PHASE_COMPLETE` — Phase done, waiting on a gate

The `ESCALATED` exit status is the formal signal that a polecat couldn't proceed without human judgment. It persists the escalation bead and leaves the issue open for human triage. [OFFICIAL]

### Mail with `--human` Routing (`gt mail send --human`)

The mail system supports explicit human routing via the `--human` address flag. Agents can send structured messages directly to the Overseer namespace, bypassing the Mayor/Deacon tiers entirely. Message types designed for human consumption include:

- `HELP` — Routes any→escalation target (usually Mayor), for guidance or expertise
- `REWORK_REQUEST` — Delivers specific git instructions (rebase, conflict resolution) to a human working with a polecat
- `MERGE_FAILED` — Notifies human when Refinery merge attempts fail

The human reads these via `gt mail inbox` and responds with `gt mail reply <id>`. No separate UI — it's pure CLI. [OFFICIAL]

---

## Monitoring and Observability for Human Operators

### Real-Time Dashboard (`gt feed` / `gt dashboard`)

Gas Town ships two monitoring surfaces:

**`gt feed`** — Interactive TUI combining three panels: agent tree (grouped by role), convoy status, and chronological event stream. Shows live activity across all agents. Not a web app — terminal-only.

**`gt dashboard`** — Web server with auto-refresh convoy tracking. Provides browser-based visibility into active work with status indicators. Does not appear to expose approval or intervention actions — observability only.

Both dashboards surface stuck agents in a "Problems View" that groups agents by health state: GUPP Violation, Stalled, Zombie, Working, Idle, or Intervention Needed. This is the primary mechanism for a human to discover which agents need attention without waiting for escalation mail. [OFFICIAL]

### Convoy Status (`gt convoy status` / `gt convoy list`)

Convoys are the primary "work batches" that humans track. The convoy list is described as "the primary attention view" — it shows active convoys, completion progress (e.g., "2/4 completed"), and which agents are assigned. Humans subscribe to convoy completion notifications via `--notify` flag when creating convoys, receiving alerts when all tracked issues close.

A "stranded convoy" — one with ready work but no assigned polecats — surfaces as an explicit intervention point requiring human action. [OFFICIAL]

### Audit Trail (`gt audit` / beads)

Every action in Gas Town is attributed to an actor via the `BD_ACTOR` environment variable. The `gt audit` command queries provenance data across git commits, beads, and events, producing a unified timeline of who did what and when. Bead records carry `created_by` and `updated_by` fields. Git commits are authored with agent identity (`GIT_AUTHOR_NAME`) while workspace ownership stays with the human email.

The `gt activity` command tracks activity events to `~/gt/.events.jsonl`, providing a flat log suitable for external processing. [OFFICIAL]

### Operational State Querying

Gas Town uses an event-sourced state model ("Events are the source of truth. Labels are the cache"). Current agent state can be queried via bead labels:

```
bd show role-deacon | grep patrol:
bd list --type=role --label=patrol:muted
bd list --type=event --target=<entity>
```

State history is fully queryable — the Overseer can reconstruct the sequence of events leading to any current state. [OFFICIAL]

---

## Emergency Intervention and Override

### Emergency Stop (`gt stop --all` / `gt stop --rig <name>`)

The nuclear option for human intervention: kills all sessions or all sessions on a specified rig. This is a hard stop — no graceful shutdown. Documented explicitly as an emergency control. [OFFICIAL]

### Manual Health Commands

Humans can trigger triage and health checks directly:

```
gt boot triage          # Force immediate triage evaluation
gt deacon health-check  # Send health check ping to deacon
gt deacon health-state  # Show health state for all agents
gt session kill         # Kill a zombie session
tail -f ~/gt/daemon/daemon.log  # Direct daemon log inspection
```

These bypass the automated watchdog chain and give humans direct access to the health infrastructure. [OFFICIAL]

### Mayor Approval Gates (v1.0.0+)

A specific governance feature introduced in v1.0.0 applies to polecats expanding their scope of action. Before accessing additional resources or system components beyond their initial mandate, polecats require Mayor approval. This is a **PreToolUse security guard** that blocks high-risk operations (specifically flagged: sudo calls, package installations, unsigned binary execution). The Mayor can approve or deny the expansion request. [OFFICIAL — Heise.de article on v1.0.0]

### Rate Limit Watchdog

A plugin introduced in v1.0.0 detects HTTP 429 responses and automatically halts affected processes. This is automated intervention rather than human intervention, but it prevents runaway cost-accruing loops and notifies the Overseer when triggered. [OFFICIAL]

---

## Checkpoint and Session Recovery

### `gt checkpoint`

Manages crash recovery by capturing current work state: molecule step, hooked bead, modified files. Designed for session continuity after crashes, not human review. However, checkpoint state is inspectable by humans for audit purposes. [OFFICIAL]

### `gt seance`

Enables querying predecessor sessions by spawning a Claude subprocess to resume and interrogate past agent context: `gt seance --talk <session-id> -p "Where is X?"`. This gives humans (and agents) retrospective visibility into what previous sessions did and decided. [OFFICIAL]

---

## Practical Limitations for HITL Workflows

### No Proactive Gate Discovery

The gate system requires the Overseer to pull for pending approvals — there is no dashboard that prominently displays "N human gates waiting." Escalation mail partially compensates, but only if the agent creating the gate explicitly sends escalation mail to the Overseer. This is a wiring decision left to the workflow author, not a built-in behavior.

### Observability Gaps Reported in Practice

A February 2026 practitioner review reported significant observability gaps: "Sometimes 6 PRs merged and I had no idea when I'd slung them." The reviewer also found the feed and monitoring tools insufficient for real-time awareness during peak parallel agent execution. Gas Town's monitoring tools are present but may not provide the granular visibility Momentum needs for confident sprint oversight. [PRAC — Tenzin Wangdhen, Medium/Long Context, Feb 2026]

### Manual Prodding Still Required

Despite the Witness and Deacon automation, the same reviewer reported needing to "constantly prod" agents and found that "the Witness seemed to need manual prodding to continue." This suggests the automated recovery chain does not fully eliminate human attention requirements. [PRAC — Tenzin Wangdhen, Feb 2026]

### `--dangerously-skip-permissions` Mode

Gas Town docs note that running with `--dangerously-skip-permissions` removes Claude Code's built-in approval prompts for all tool use. When used in that mode, Gas Town's gate-based approvals are the only HITL mechanism — the platform-level safety net is removed. This is an explicit trade-off documented in the framework. [OFFICIAL — propulsion-principle docs, practitioner observation]

### No Native Slack / Webhook Integration

Human notification channels are email and SMS via `escalation.json`. There is no documented native Slack, Teams, or webhook integration. Momentum's developer communication patterns (e.g., getting a push notification in a chat client when an agent needs approval) would require external plumbing. [UNVERIFIED — absence of evidence]

---

## Summary Assessment for Momentum Integration

| Capability | Gas Town Native | Notes |
|---|---|---|
| Human approval gate | Yes (`bd gate create --await human:X`) | Agent parks, resumes after `bd gate approve` |
| Severity-routed escalation | Yes (`gt escalate -s CRITICAL`) | Email/SMS for P0, mail for P1/P2 |
| Audit trail / provenance | Yes (beads + git attribution) | Queryable via `gt audit` |
| Real-time monitoring | Partial (`gt feed`, `gt dashboard`) | CLI/web dashboards, no push alerts |
| Emergency stop | Yes (`gt stop --all`) | Hard kill, no grace period |
| Proactive gate notification | No (pull-based only) | Must poll or configure escalation mail |
| Pre-action approval prompts | Limited (Mayor Approval Gates, v1.0.0+) | Only for scope expansion, not general workflow |
| Dashboard approval UI | No | CLI-only for approval actions |
| Slack/webhook notifications | No native support | External wiring required |

Gas Town's HITL model is **escalation-centric, not approval-centric**. It is optimized for human oversight of outcomes and blockers, not for granular pre-approval of individual agent actions. For Momentum's use case — specifically reducing friction on git push approvals and major planning decisions — the gate system provides the right primitive, but requires deliberate workflow composition to surface pending gates to the developer without requiring constant terminal monitoring.

---

## Sources

- [OFFICIAL] Gas Town Documentation — Overview and Navigation: https://docs.gastownhall.ai/
- [OFFICIAL] Gas Town Docs — Escalation Protocol: https://docs.gastownhall.ai/design/escalation/
- [OFFICIAL] Gas Town Docs — Escalation System Design: https://docs.gastownhall.ai/design/escalation-system/
- [OFFICIAL] Gas Town Docs — Watchdog Chain: https://docs.gastownhall.ai/design/watchdog-chain/
- [OFFICIAL] Gas Town Docs — Operational State: https://docs.gastownhall.ai/design/operational-state/
- [OFFICIAL] Gas Town Docs — Mail Protocol: https://docs.gastownhall.ai/design/mail-protocol/
- [OFFICIAL] Gas Town Docs — Convoy Lifecycle: https://docs.gastownhall.ai/design/convoy-lifecycle/
- [OFFICIAL] Gas Town Docs — Convoy Concepts: https://docs.gastownhall.ai/concepts/convoy/
- [OFFICIAL] Gas Town Docs — Identity & Attribution: https://docs.gastownhall.ai/concepts/identity/
- [OFFICIAL] Gas Town Docs — Polecat Lifecycle: https://docs.gastownhall.ai/concepts/polecat-lifecycle/
- [OFFICIAL] Gas Town Docs — Propulsion Principle: https://docs.gastownhall.ai/concepts/propulsion-principle/
- [OFFICIAL] Gas Town Docs — Work Management Commands: https://docs.gastownhall.ai/usage/work-management/
- [OFFICIAL] Gas Town Docs — Communication Commands: https://docs.gastownhall.ai/usage/communication/
- [OFFICIAL] Gas Town Docs — Diagnostics Commands: https://docs.gastownhall.ai/usage/diagnostics/
- [OFFICIAL] Gas Town Docs — Why These Features: https://docs.gastownhall.ai/other/why-these-features/
- [OFFICIAL] Gas Town Docs — Plugin System: https://docs.gastownhall.ai/design/plugin-system/
- [OFFICIAL] Gas Town Docs — Dog Pool Architecture: https://docs.gastownhall.ai/design/dog-pool-architecture/
- [OFFICIAL] Gas Town Docs — Federation Architecture: https://docs.gastownhall.ai/design/federation/
- [OFFICIAL] Gas Town GitHub Repository: https://github.com/gastownhall/gastown
- [PRAC] Tenzin Wangdhen — "Gas Town: The Good, The Bad, The Ugly" (Feb 2026): https://tenzinwangdhen.com/posts/gastown-good-bad-ugly/
- [PRAC] Torq Software Reading List — "Gas Town: Steve Yegge's Multi-Agent Orchestration Framework" (Jan 2026): https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/
- [PRAC] Heise.de — "Gas Town controls what automated agents are allowed" (v1.0.0 release coverage): https://www.heise.de/en/news/Gas-Town-controls-what-automated-agents-are-allowed-11252281.html
