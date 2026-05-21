---
title: "Gas Town as dispatcher/coordinator for Momentum — Research Report"
date: 2026-05-20
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: true
derives_from:
  - path: raw/research-gas-city-architecture.md
    relationship: synthesized_from
  - path: raw/research-gas-town-beads-relationship.md
    relationship: synthesized_from
  - path: raw/research-dispatch-routing-primitives.md
    relationship: synthesized_from
  - path: raw/research-human-in-loop-oversight.md
    relationship: synthesized_from
  - path: raw/research-maturity-production-readiness.md
    relationship: synthesized_from
  - path: raw/research-momentum-integration-mapping.md
    relationship: synthesized_from
  - path: raw/research-coordination-model-comparison.md
    relationship: synthesized_from
  - path: raw/research-adoption-path-risks.md
    relationship: synthesized_from
  - path: raw/gemini-deep-research-output.md
    relationship: synthesized_from
  - path: validation/avfl-report.md
    relationship: validated_by
  - path: validation/followup-gas-town-vs-gas-city-distinction.md
    relationship: validated_by
  - path: validation/followup-gas-city-orders-standalone.md
    relationship: validated_by
  - path: raw/practitioner-notes.md
    relationship: informed_by
---

# Gas Town as dispatcher/coordinator for Momentum — Research Report

## Executive Summary

The question this research set out to answer is whether **Gas Town** can serve as the dispatcher/coordinator for Momentum's agentic engineering practice — automating sprint orchestration, reducing human-in-the-loop friction, and working alongside Beads. The honest answer requires splitting the question in two, because the corpus repeatedly conflated two distinct products under one name. **Gas Town** (the Gastown Colony) is the wrong tool. **Gas City** (the composable SDK that Gas Town is now one pack inside of) is a credible — but narrow — fit for one specific gap.

Gas Town is a finished, opinionated platform for running 20–30 parallel AI coding agents on a shared codebase. Its architecture hardwires a role taxonomy (Mayor, Deacon, Witness, Polecat, Refinery) into the Go SDK, assumes a colony-scale parallel-coding topology, models all work as pull requests funnelled through a bisecting merge queue, and derives agent identity from filesystem directory layout. Every one of those design choices is a mismatch for Momentum, which runs 4–8 session-scoped agents through a sprint workflow, produces story-state transitions rather than a continuous PR stream, and uses explicit agent composition rather than path-derived identity. Adopting the Gas Town topology would mean importing a design built for a problem Momentum does not have. [AVFL-FIXED — CON-001]

Gas City is a different proposition. It is the orchestration SDK that Gas Town's architecture was deconstructed into — primitives plus declarative configuration, with **zero hardcoded role names in the Go code** [OFFICIAL]. The Gas Town topology is one optional pack; the Gas City quickstart deploys none of it. Within Gas City, one subsystem maps directly onto Momentum's actual gap: the **Orders system**, a general-purpose event-triggered dispatcher with five trigger types (cooldown, cron, condition, event, manual). Momentum today has no persistent dispatcher at all — a human must manually invoke every workflow skill. An Orders-based dispatcher closes exactly that gap, and nothing else in Gas City's surface area is needed to do it.

The recommended path is deliberately minimal. A single Gas City "city" with one rig, **file-based Beads storage** (`GC_BEADS=file`, which removes the Dolt dependency entirely for the proof of concept), and **exec orders** that invoke `claude -p` as a plain shell subprocess. Exec orders sidestep Gas City's single most important current limitation — MCP runtime support was deferred from the PackV2 release — because MCP runs inside the Claude Code session, not at the Gas City controller level. [AVFL-FIXED — CON-008] This keeps the proof of concept on solid, shipped primitives and leaves a clean exit ramp (delete the `gc` binary, keep the shell scripts).

The recommendation is **adopt Gas City as a dispatcher experiment, scoped to a proof of concept, on a 3–4 week timeline — and do not adopt the Gas Town topology at all**. The proof of concept should be gated behind a small set of explicit validation checks, and the broader migration (story files becoming Beads, AVFL as a post-merge order, retro and sprint-planning integration) should be treated as out of scope until the dispatch loop itself is proven. Beads, meanwhile, is validated and in active evaluation in Momentum — running and tested via the dual-write spike, but not yet committed to as the authoritative task layer — which means the Dolt-related risk surface is shared between the two adoptions and must be weighed jointly. [AVFL-FIXED — CON-006]

---

## 1. What Is Gas Town / Gas City?

### Gas Town: an opinionated multi-agent coding platform

Gas Town is a multi-agent workspace manager built on top of AI coding agents — primarily Claude Code — that coordinates colonies of 20–30 parallel agents on shared software projects. It was created by Steve Yegge alongside a core team (Matt Beane, Chris Sells, Julian Knutsen, Tim Sehn, Brendan Hopper), released publicly in early January 2026, and reached stable v1.0.0 on April 21, 2026, with v1.1.0 following on May 7, 2026. [OFFICIAL] [AVFL-FIXED — LOW-001, team correctly attributed]

The central design move is to invert the persistence model: **make the work durable, not the agent**. Sessions are disposable; agents have persistent identities stored externally; work survives crashes because it lives in git. Where conversation-based frameworks keep coordination state in an LLM context window, Gas Town externalizes all of it into a git-versioned database. [PRAC — augusteo.com/blog/inside-gas-town]

Gas Town organizes around two scopes. A **Town** (the `~/gt/` directory) is the coordination hub hosting cross-project agents. A **Rig** is a single git repository under management, with its own workers, merge processor, and health monitor. The agent taxonomy is hardwired:

- **Mayor** — the persistent global coordinator and primary human interface; decomposes goals into work units, batches them, and reports status.
- **Deacon** — a background supervisor daemon running continuous patrol cycles across all Rigs.
- **Witness** — a per-Rig lifecycle manager supervising worker agents.
- **Refinery** — a per-Rig merge queue processor using Bors-style bisection (batch all pending merge requests, test once; on failure, recursively split to isolate the bad one in O(log N) test runs).
- **Polecats** — ephemeral worker agents, each in an isolated git worktree, that execute one work unit, produce a merge request, and terminate.
- **Dogs** — maintenance agents dispatched by the Deacon for infrastructure tasks only, not feature work.

These roles are not configuration — in Gas Town they are baked into the SDK as Go-level primitives. [OFFICIAL — followup-gas-town-vs-gas-city-distinction.md]

### Gas City: the SDK Gas Town was rebuilt into

Gas City (`gastownhall/gascity`) was announced in late April 2026 as the successor and generalization of Gas Town. Yegge describes it as "Gas Town, but torn apart and rewritten from the ground up as an SDK for building your own dark factories." [PRAC — steve-yegge.medium.com/welcome-to-gas-city] It reached v1.0.0 on April 27, 2026, with v1.1.0 (455 commits, themed around resilience and managed-Dolt hardening) on May 6, 2026. [OFFICIAL] [AVFL-FIXED — CON-002, April 27 used as the Gas City v1.0.0 release date; April 21 is Gas Town's]

The architectural shift is from "role taxonomy plus filesystem layout" to "small primitive set plus configuration":

| Gas Town | Gas City |
|---|---|
| Role-specific directories | Configured agents from packs |
| Plugins | Orders (exec or formula) |
| Deacon/Witness watchdog logic | Controller — a reconciliation loop |
| Directory tree encoding architecture | `dir` for scope, explicit metadata for identity |
| Fixed Mayor→Deacon→Witness→Polecat topology | Any topology, declared in `city.toml` + `pack.toml` |

The official migration guide is blunt: "Gas City is not 'Gas Town with renamed commands.' It is the lower-level orchestration toolkit that Gas Town can be expressed in." [OFFICIAL — coming-from-gastown.md] The nine-concepts architecture document states that "the SDK contains zero hardcoded role names" [OFFICIAL]. Crucially, **Gas City ships a fully functional Gas Town compatibility pack** — the Gastown Colony is now one optional pack inside Gas City, not a separate product and not the default. The Gas City quickstart (`gc init` → `gc rig add` → `gc sling` → `bd show`) deploys none of the Gas Town topology. [OFFICIAL — followup-gas-town-vs-gas-city-distinction.md]

Gas City's configuration model is a three-file separation: `pack.toml` (reusable shared behavior — agents, prompts, workflow templates), `city.toml` (deployment choices, rig configuration, concurrency), and `.gc/` (machine-local runtime bindings). It supports multiple runtime backends — tmux, subprocess, exec, ACP, Kubernetes. The stack is Go (≥1.25, the correct minimum requirement), TypeScript, and shell. [OFFICIAL] [AVFL-FIXED — CON-005, Go ≥1.25 not 1.23]

### The problem each solves

Gas Town solves **coordination chaos at colony scale**: managing 10+ parallel coding agents manually is untenable — they write conflicting code, lose track of in-progress work, and create unresolvable merge conflicts. Gas Town provides structured decomposition, worktree isolation, a bisecting merge queue, and hierarchical supervisors that detect and recover stuck agents. It also addresses **agent cognitive degradation** (context windows fill, agents lose prior decisions) by externalizing all work state so agents can be destroyed and recreated freely.

Gas City solves a more general problem: **building custom orchestrators**. The same engine that runs the Gas Town coding colony can drive image-moderation pipelines, compliance review, or ticket triage. For Momentum, the relevant Gas City subsystem is narrower still — the Orders system, a general-purpose event-triggered dispatcher (covered in Section 3).

---

## 2. The Gas Town ↔ Beads Relationship

Gas Town and Beads are not independent tools that happen to be compatible. They are two explicit layers of a single stack, created by the same author and hosted under the same GitHub organization. **Beads is the persistence and task-state layer; Gas Town is the orchestration and dispatch layer built on top of it.** [OFFICIAL]

A design invariant Yegge states explicitly: "Beads is completely unaware of Gas Town." The dependency is strictly one-directional. Beads does not import Gas Town code and knows nothing about mayors, polecats, or convoys. Gas Town depends on Beads as its core memory layer; the coupling flows only downward. [OFFICIAL — research-gas-town-beads-relationship.md]

### The Beads data model

Beads is a distributed issue-tracking system designed for AI agents. A **bead** is an atomic work unit — a single issue with a hash-derived ID (e.g., `bd-a1b2`), a description, a status (`open`, `in_progress`, `done`), a priority, an assignee, a `blocked_by` dependency array, and a `discovered_from` provenance link. Hash-derived IDs prevent merge collisions across multi-agent, multi-branch work. [OFFICIAL]

Beads' storage backend is **Dolt** — a version-controlled SQL database with git-like semantics (branch, merge, diff, push, pull at the database level). Beads runs in two modes: an **embedded mode** (default, in-process Dolt in `.beads/embeddeddolt/`, suitable for solo use and CI) and a **server mode** (`dolt sql-server`, MySQL protocol on port 3307, for concurrent multi-agent writes). A `.beads/issues.jsonl` export exists for viewers and interchange but is explicitly "not the source of truth" — Dolt is. [OFFICIAL]

### How beads compose into workflows: the MEOW stack

The MEOW stack — **"Molecular Expression of Work"** — is the abstraction that bridges atomic beads to Gas Town's orchestration layer. [OFFICIAL] [AVFL-FIXED — CON-003; the spurious letter-by-letter expansion "Molecules, Epics, Orders, Wisps" is incorrect and is not used here.] The hierarchy, bottom to top:

1. **Bead** — atomic task in Dolt.
2. **Epic** — a bead with children, for planning hierarchies.
3. **Molecule** — a durable chained bead workflow; an agent walks the chain one step at a time, claiming and closing each bead. Molecules survive agent restarts because state persists in Dolt.
4. **Protomolecule** — a reusable workflow template; a function definition vs. a function call.
5. **Formula** — a declarative TOML source definition with macros, gates, and loops, that compiles ("cooks") into a protomolecule.

**Wisps** are ephemeral beads — used for orchestration-only transient operations and destroyed after the run, to avoid polluting repository history.

### Beads stands alone — and Gas City makes the relationship explicit

Despite the tight integration, Beads is designed to be independently useful. Its README and FAQ do not mention Gas Town; Yegge states "you can use Beads by itself and get a vastly improved agentic experience, no matter which coding agent you're using"; and practitioners report adopting Beads as a standalone task tracker independent of Gas Town. [OFFICIAL]

In Gas City, Beads' role is made explicit as a **selectable storage provider**. Gas City treats Beads (`bd`) as its default store for work tracking, formulas, molecules, waits, and mail — but the provider is swappable. Setting `GC_BEADS=file` (or `[beads] provider = "file"` in `city.toml`) disables Dolt, `bd`, and `flock` entirely, using file-based storage instead. [OFFICIAL — followup-gas-city-orders-standalone.md] This is a material fact for Momentum: the highest-risk dependency in the stack can be bypassed for an initial proof of concept.

### What this means for Momentum's Beads status

Beads in Momentum is **validated and in active evaluation — not yet adopted as the authoritative layer**. [AVFL-FIXED — CON-006] The `beads-dual-write-spike` story is at `ready-for-dev`; the spike has proven the integration and Beads runs and is tested under Momentum's actual usage patterns, but Beads has not been committed to as the primary task layer. The practical consequence: any Dolt-related operational risk is shared between the Beads adoption and a Dolt-backed Gas City adoption — they would fail together. This is a reason to keep the Gas City proof of concept on `GC_BEADS=file` rather than coupling two unproven Dolt dependencies.

---

## 3. How Gas City Dispatches and Routes Work

Momentum's dispatcher gap is specific: there is no persistent process that reacts to a story becoming ready by starting the work. A human must invoke every workflow skill by hand. Gas City's **Orders system** is the subsystem that closes exactly this gap, and it is general-purpose — nothing in it is hardwired to coding tasks or to the Gas Town topology.

### The Controller and the event model

Gas City's dispatch is owned by the **Controller** — a Go process, not an agent. It runs a continuous main loop: watch configuration, run a reconciliation tick, dispatch orders. It watches an **Event Bus** — an append-only pub/sub log of all system activity, separate from the durable Beads storage. The Controller evaluates order triggers roughly every 30 seconds (one "tick"). [OFFICIAL — followup-gas-city-orders-standalone.md; PRAC — gemini-deep-research-output.md, Follow-up 2]

The Controller is not an inbound HTTP listener — it does not catch webhooks directly. External events (CI runs, GitHub webhooks) must be bridged in via one of two patterns: a **push pattern** (the external system uses the Gas City/Beads CLI to write an event onto the Event Bus, which the Controller observes) or a **pull/condition pattern** (an exec order runs a shell check that polls the external system). [PRAC — gemini-deep-research-output.md, Follow-up 2]

### Orders: exec vs formula

An **Order** pairs a trigger with an action. There are two action types.

**Exec orders** run a shell command directly on the Controller — "no agent, no LLM, no wisp." The exec provider forks a subprocess, pipes through stdin/stdout, and interprets exit codes (0 = success, 1 = error). It enforces a bounded timeout (default 300 seconds) and captures stdout/stderr. [OFFICIAL — followup-gas-city-orders-standalone.md]

```toml
[order.prune-merged]
exec = "scripts/prune-merged.sh"
trigger.cooldown = "5m"
```

**Formula orders** dispatch a named formula to an agent pool, starting an agent-driven multi-step workflow:

```toml
[order.run-sprint]
formula = "sprint-dev"
pool = "worker"
trigger.event = "bead.closed"
```

### The five trigger types

| Type | Behavior | Momentum relevance |
|---|---|---|
| **Cooldown** | Fires after an interval since last run (`"5m"`, `"1h"`) | Story-polling fallback |
| **Cron** | Absolute wall-clock schedule (`"0 3 * * *"`) | Sprint kickoff at a fixed time |
| **Condition** | Fires when a shell check exits 0 (10s timeout) | "Are there ready stories?" check |
| **Event** | Fires on Event Bus events (`bead.closed`, `bead.created`) | Natural story-state triggers |
| **Manual** | Only via `gc order run` | Explicit developer-triggered dispatch |

[OFFICIAL — followup-gas-city-orders-standalone.md, citing `internal/orders/triggers.go`] Event triggers use a sequence-based cursor (`seq:<N>` in bead labels) to prevent duplicate firing.

### The MCP gap — and why exec orders route around it

Gas City **deferred first-class MCP runtime support from the PackV2 release**. [OFFICIAL — gemini-deep-research-output.md, Follow-up 1] This matters because Momentum's skills are invoked as Claude Code slash commands operating within Claude Code's MCP toolchain. A formula order that starts a Claude Code session and expects Gas City to manage that session's MCP toolchain hits this gap.

**Exec orders bypass the gap entirely.** [AVFL-FIXED — CON-008] An exec order that runs `claude -p "run momentum:dev for story XYZ"` invokes the Claude Code CLI as a plain subprocess. MCP runs *inside* that Claude Code session — Claude Code handles its own MCP toolchain regardless of how the session was launched. Gas City's deferred MCP support is irrelevant to this pattern. This is the central reason the recommended proof of concept uses exec orders rather than formula orders.

### GUPP and the Gas Town dispatch model (context)

Gas Town's own dispatch primitive is **GUPP — the Gas Town Universal Propulsion Principle**: "If there is work on your Hook, YOU MUST RUN IT." Each agent has a **Hook** (a pinned bead acting as a personal work queue); work is placed on a Hook via `gt sling`; the agent pulls it on next wakeup and executes immediately. [OFFICIAL — though the GUPP wording itself is most strongly attested in practitioner sources; AVFL MED-002.] In practice GUPP breaks down with Claude Code's safety training, which makes the model wait for confirmation rather than acting autonomously — Gas Town works around this with a fragile tmux `send-keys` keystroke-injection hack fired 30–60 seconds after session start. This GUPP/Hook/sling machinery belongs to the Gas Town topology and is not part of the recommended Gas City Orders path; it is included here only to explain the lineage.

---

## 4. Human-in-the-Loop Oversight

Gas Town's HITL philosophy is deliberate: **autonomy with structured escalation, not approval-first gating.** The system assumes humans should be freed from constant supervision — agents run independently, surface blockers through a tiered chain, and humans act as overseers of outcome rather than approvers of every action. This is fundamentally different from a system that requires pre-approval at workflow boundaries, and it is the single most important philosophical tension for Momentum, whose git discipline requires explicit human approval before every push.

### The overseer hierarchy and the gate primitive

The human sits at the top of the hierarchy as the **Overseer** — the only definitionally-human role. Below sit Mayor (the human's closest agent interlocutor), Deacon (routine escalation routing), and Witness (per-Rig health). In the nominal happy path the human is not involved during execution at all — only in work assignment and post-hoc review.

The most explicit HITL primitive is the **gate system**. Gates are async checkpoints that can represent a timer (`timer:30m`), a CI run (`gh:run:123456789`), or a human approval (`human:deploy-approval`). A human gate causes the agent to call `gt park` — it saves work state, marks itself a gate-waiter, and exits the session cleanly, consuming no tokens while waiting. When the human runs `bd gate approve <gate-id>`, the gate closes and wake mail goes to all waiters; the agent resumes with restored context. This is the closest Gas Town equivalent to Momentum's "developer must confirm before push" pattern, and it is fully general — any workflow step can declare a human gate.

**The critical limitation is that gates are pull, not push.** The Overseer must know to check for pending gates — there is no dashboard that prominently says "3 human approval gates are waiting for you." [OFFICIAL] [AVFL — MED-015: the `gt dashboard` shows status with auto-refresh but does not enumerate pending gate counts; both statements are compatible.]

### Escalation, completion signals, and emergency control

Escalations are severity-routed via `gt escalate`. The documented default `escalation.json` routing: **low** = bead only; **medium** = bead + mail to Mayor; **high** = bead + mail to Mayor + email to human; **critical** = bead + mail to Mayor + email + SMS to human. [OFFICIAL — research-human-in-loop-oversight.md] (Note: the corpus contained a minor inconsistency on whether MEDIUM escalations notify the Mayor or only surface at the next Deacon patrol; the HITL file's "mail to Mayor" routing is treated as canonical here. [AVFL — CON-004]) Each escalation creates a structured bead serving as both audit trail and async channel. Polecats signal completion explicitly via `gt done --status` (`COMPLETED`, `ESCALATED`, `DEFERRED`, `PHASE_COMPLETE`). The nuclear option is `gt stop --all`, a hard kill of all sessions.

### Observability UX in practice

Gas Town ships `gt feed` (an interactive TUI) and `gt dashboard` (a web server with auto-refreshing convoy tracking). Both surface stuck agents in a "Problems View." Neither pushes notifications — the developer must be watching. Practitioner reviews report real observability gaps at peak parallelism ("Sometimes 6 PRs merged and I had no idea when I'd slung them") and note the Mayor itself sometimes needs manual prodding, weakening the escalation buffer. [PRAC — Tenzin Wangdhen, Feb 2026] [AVFL — MED-010, Mayor reliability flagged as an open risk, not quantified.]

There is **no native Slack or webhook integration** in the core. Proactive notification is left to the agent layer or to modular packs. Established community patterns: agent-level desktop hooks (Claude Code "stop hooks" in `settings.json` triggering `osascript` notifications on macOS), tmux status integrations, and a `slack-pack` in the Gas City packs ecosystem for routing human-gate alerts to Slack. [PRAC — gemini-deep-research-output.md, Follow-up 3] Note that the `slack-pack` and the "Moshi" iOS tool mentioned by Gemini were not independently confirmed in the subagent corpus and should be treated as unverified leads. [AVFL — MED-008, MED-009]

### Practical implication for Momentum

For Momentum's specific need — reducing friction on git-push approvals and major planning decisions without the developer being perpetually on-call — the gate primitive is the right shape but requires deliberate wiring. The most realistic pattern for the proof of concept is **not** to route push approval through a Gas City gate at all initially: exec orders that invoke `claude -p` for non-push work, with the developer continuing to approve pushes interactively, keep the HITL model unchanged while still removing the dispatch-trigger friction. A later phase could add a human gate plus a Claude Code stop-hook desktop notification to make pending approvals visible without terminal polling.

---

## 5. Maturity and Production-Readiness

### Both products reached v1.0 — and v1.1 — in genuine fashion

Gas Town v1.1.0 shipped May 7, 2026; Gas City v1.1.0 shipped May 6, 2026 (455 commits, themed on resilience, session lifecycle recovery, operator readiness, and managed-Dolt hardening). [OFFICIAL] The v1.0 milestones are not marketing labels: the projects have a multi-maintainer core team, 450+ contributors across Gas Town and Beads, a 2,000+ member Discord, and substantial independent press coverage. Gas City had three release candidates validating v1.0. All repositories are MIT-licensed. [OFFICIAL] (Per research methodology, GitHub star counts are excluded as a gameable metric. [AVFL-FIXED — CON-007] Meaningful signals — commit count, contributor count, PR volume, release cadence — are used instead.)

### Stability signals — positive

Gas City maintains an unusually rigorous testing posture for a project this young: a three-tier strategy of unit tests, CLI behavioral tests (`.txtar` testscripts running the real `gc` binary), and integration tests exercising real tmux sessions; no mock libraries; and a `test/docsync` suite that validates documentation against implementation. CI is sharded for fast feedback. Release cadence is a minor version every 2–3 weeks. There is declared external production usage (a non-technical professional building SaaS-replacement software; DoltHub parallelizing well-defined coding tasks). [OFFICIAL]

### Stability signals — caution

Gas City had 262 open issues at assessment time, including real correctness bugs: pool-managed call recurrence accelerating dangerously with goroutine subprocess buildup, a fixed 180-second session-startup timeout that doesn't scale, and built-in pack materialization silently overwriting user edits. The **PackV2 migration is incomplete** — Issue #2120 tracks five pending workstreams (deprecating PackV1 surfaces, reconciling doc/implementation gaps, pack registry support, a unified `gc pack` surface, pack reuse improvements). Custom CLI-command and doctor-check manifests (`command.toml`, `doctor.toml`) are still under-specified and the core team is freezing only the basic `run.sh` entrypoint contract. [OFFICIAL — gemini-deep-research-output.md, Follow-up 1] There is no enterprise SLA or commercial support.

The most consequential maturity caveat: **the pack/config schema is still in active redesign.** Building on PackV2 is safe for core orchestration tasks if you build natively on the new directory conventions — but adopters should lock to a specific release tag and expect schema churn. [OFFICIAL]

### The Dolt risk

The highest-probability operational risk is Dolt. Issue #1930 documents dual supervisor processes competing for the same Dolt port causing ~23,759 restarts over 6 hours, leaving `.beads/dolt/` empty and blocking all `gc sling` operations. [PRAC — DoltHub blog; GitHub Issue #1930] Stated in Momentum-relevant terms: **under concurrent multi-agent write patterns, Dolt may require agent restarts at a rate incompatible with automated sprint execution.** [AVFL — MED-001] Gas City v1.1.0's "managed Dolt hardening" theme indicates active work on this class of problem, but Issue #1930's specific status is unverified. This risk is the primary justification for the `GC_BEADS=file` (Dolt-free) proof-of-concept path.

### Verdict

**For its intended use case** — parallelized AI-driven software development with well-specified, externally-verifiable coding tasks — Gas Town/Gas City is production-viable as of May 2026. **For Momentum's dispatcher use case**, the Gas Town topology is a poor fit (Section 7), while Gas City's Orders subsystem is viable but sits on a foundation (PackV2, Dolt) still actively stabilizing. Adopting Gas City today is reasonable only if scoped to a proof of concept on shipped, low-churn primitives — exec orders and file-based Beads — with a release-tag lock and an active changelog watch.

---

## 6. What Would Change in Momentum?

Momentum today runs without a persistent dispatcher. A human starts a Claude Code session, invokes a skill (`momentum:sprint-dev`), and that session acts as the orchestrator — spawning subagents via the Agent tool, waiting, merging. When the session ends, the orchestrator is gone. State lives in story files, `sprints/index.json`, and git history. There is no watchdog, no merge queue, no ability to resume mid-sprint if the orchestrating session dies.

The following maps Momentum's workflows onto Gas City. The honest framing: **the minimal Orders-based dispatcher changes very little; a full Gas Town-style migration would change almost everything and is not recommended.**

### sprint-dev

Under the recommended minimal model, `sprint-dev` barely changes. An exec order fires `claude -p` to start the sprint-dev workflow when a condition trigger detects ready stories. The session-local orchestrator-subagent fan-out continues to run inside that Claude Code session exactly as today. What changes is only the *trigger*: a developer no longer types the slash command — a Controller condition check does. AVFL post-merge validation continues to run inside the same session.

Under a full Gas Town-style migration (not recommended), the change is structural: the sprint becomes a Convoy, each story becomes a bead slung to a Polecat, the orchestrating session no longer blocks on completion, and the Refinery replaces manual merge logic. This is a large rearchitecture for capability Momentum does not currently need.

### intake

`intake` is a lightweight single-turn operation: capture a story idea, write a stub. It maps cleanly to bead creation (`bd new`). If Momentum adopts Beads as the story store, intake writes a bead with `status: backlog`. Momentum's rich Markdown story format (frontmatter, EDD/TDD sections, Gherkin specs) would become a linked artifact rather than the bead itself, since beads are JSON-structured. Under the minimal dispatcher model, intake does not need to change at all — it remains a skill the developer invokes directly.

### quick-fix

`quick-fix` (define → implement → validate → merge in one session) is the closest structural match to Gas Town's canonical Polecat use case and its "Shiny Workflow" formula (design → implement → review → test → submit). Under the minimal model, quick-fix is unchanged — optionally it becomes a manual-triggered exec order for convenience. The capability Gas Town would add is crash recovery (a dead session resumes from the last molecule step), which Momentum's current quick-fix lacks; but that benefit only materializes under the full Beads/molecule migration.

### retro

`retro` is the worst fit. It reads the sprint transcript via DuckDB, spawns parallel **collaborating** auditor agents via TeamCreate (auditors cross-reference each other's findings; the Documenter requests deeper investigation), synthesizes findings, and writes a document. Gas City/Gas Town's parallelism model is **peer workers on independent units**, not collaborating agents sharing context — there is no TeamCreate equivalent. The pragmatic answer: **keep retro outside Gas City entirely.** It is low-frequency and high-coordination; running it as a session-local Momentum workflow while routing only sprint-dev triggering through Gas City is the clean split. Gas City's event log could *feed* the retro as input, but the retro should not run inside it.

### Compatibility summary

| Momentum concept | Gas City fit (minimal model) | Notes |
|---|---|---|
| Sprint trigger | Good | Condition/event order replaces manual slash-command |
| Story | Good (if Beads adopted) | Bead + linked Markdown artifact |
| Worktree-per-story | Excellent | Already how Momentum works |
| Orchestrator session | Unchanged | Stays session-local; only the trigger is externalized |
| AVFL | Stays in-session | Or later: exec order on a merge event |
| retro | Poor — keep outside | No collaborative-agent primitive |
| intake / quick-fix | Good — optional | Manual-triggered orders, or unchanged |
| Human push approval | Unchanged initially | Keep interactive; gate-wire later |

The headline: a minimal Gas City dispatcher is **additive** — it externalizes the *trigger* for starting work and leaves Momentum's orchestration model intact. Treating it as a wholesale replacement for the orchestrator is the path that demands rearchitecting the state layer, and that path is not justified at Momentum's scale.

---

## 7. Gas City vs Momentum's Current Orchestrator-Subagent Pattern

Momentum and Gas Town sit at opposite ends of the orchestration design space. Momentum is a **session-scoped, file-backed, conversational fan-out** orchestrator: one human-triggered Claude Code session spawns subagents via the Agent tool, interprets results, and dissolves. Gas Town is a **persistent, daemon-based, process-model** orchestrator built to coordinate 20–30 parallel agents. The comparison below is framed at Momentum's actual operating scale (4–8 agents, solo developer) — the "overbuilt" conclusions apply specifically at that scale. [AVFL — MED-016]

### What Gas City adds

1. **Session-independent dispatch.** Work can be triggered without a human present. This is the one genuine capability Momentum lacks and the entire reason to consider Gas City.
2. **Crash recovery** (only under the full Beads/molecule model). GUPP plus durable bead state lets a dead session resume from the last checkpoint. Momentum's current model loses in-flight orchestration context on a session crash, though unmerged worktree branches survive in git.
3. **Event-driven triggers.** Orders can fire on bead events, cron schedules, or shell conditions. Momentum cannot react to events without a human polling.
4. **A supervised background controller** (`gc supervisor`) that restarts after crashes.

### What it costs

1. **A persistent background process.** The Controller is a Go daemon with its own footprint. For a developer who opens Claude Code once a day, the value of a continuously-running controller is lower than for a team running 20–30 agents — the overhead is manageable but not invisible.
2. **Infrastructure surface.** Even minimally: the `gc` binary, tmux, git, jq, a city directory. With Dolt: a versioned SQL database and its documented concurrency bugs. (`GC_BEADS=file` removes the Dolt cost but, per an open question, may also disable the Beads-backed event triggers — see Section 9.)
3. **Schema instability.** PackV2 is in active redesign; the pack/config schema is lower-stability than the v1.0 label implies.
4. **A use-pattern mismatch.** Exec orders are positioned for "mechanical operations"; using them to launch LLM sessions works but is arguably using Gas City as a shell-script scheduler — undersells the platform and could diverge from future conventions as MCP support lands.
5. **An `oh-my-zsh` footgun.** The git plugin aliases `gc` to `git commit`; the alias must be renamed or `command gc` used.

### Where Gas City is overbuilt for Momentum

The entire Gas Town pack — Mayor, Deacon, Witness, Polecat, Refinery — is unnecessary. Momentum's fan-out with 4–8 session-scoped agents does not need persistent colony management, health patrol, a bisecting merge queue, wisp garbage collection, or the Wasteland federation layer. Those features address problems Momentum does not have. The merge queue is in fact actively *counter* to Momentum's git discipline: the Refinery expects autonomous merge authority, while Momentum requires explicit human push approval. [AVFL — MED-004]

The framework-landscape framing is useful: the fundamental axis is **conversation as control plane vs. process as control plane.** Momentum, like CrewAI and LangGraph, uses conversational fan-out — simple, zero-infrastructure, appropriate at 4–8 agents, but with no crash recovery and a context-window ceiling. Gas Town uses a process model — crash-surviving, scaling to 20–30+ agents, but infrastructure-heavy. **Gas City's Orders system lets Momentum borrow exactly one process-model capability — externalized, persistent dispatch — without buying the whole process-model stack.** That is the precise, narrow tradeoff on offer.

### The verdict

Adopting the Gas Town topology as Momentum's coordinator would mean accepting an entire infrastructure stack in exchange for capabilities that only matter at 15+ unattended parallel agents. At Momentum's scale, that cost exceeds the benefit. Adopting Gas City's Orders system *alone* — as a dispatch trigger, leaving Momentum's orchestrator intact — is a far smaller bet with a proportionate payoff.

---

## 8. The Realistic Adoption Path

### Prerequisites

For the minimal `GC_BEADS=file` + exec-order path: the `gc` CLI binary, `tmux`, `git`, and `jq`. `flock` and Dolt are required only for the Dolt-backed Beads provider and are skipped under `GC_BEADS=file`. `gh` (GitHub CLI) is optional. Go ≥1.25 is needed only for a source build, not a Homebrew install. [OFFICIAL] If Dolt is later adopted, the documented version floor matters — earlier Dolt versions have deadlock issues producing silent corruption; use a current, hardened release.

Installation on macOS:
```bash
brew install gastownhall/gascity/gascity
gc version
```

### The proof-of-concept design

The proof of concept validates exactly one hypothesis: **can Gas City's Orders system automatically dispatch a Momentum skill invocation when a story is marked ready, with no human keystroke, on shipped primitives?** Three steps, drawn directly from the standalone-Orders follow-up research:

**Step 1 — Initialize a Dolt-free city.**
```bash
GC_BEADS=file gc init ~/momentum-city
gc rig add ~/projects/<momentum-project>
```
Validates: the Controller starts, the rig registers, no Dolt dependency exists.

**Step 2 — Wire one manual-triggered exec order.**
```toml
# ~/momentum-city/city.toml
[order.sprint-story]
description = "Dispatch a Momentum sprint story"
trigger = "manual"
exec = "scripts/run-momentum-dev.sh"
```
where `run-momentum-dev.sh` invokes `claude -p` with the story context. Validates: the exec order fires, a Claude Code session starts, the Momentum skill runs, the session exits cleanly. This step confirms the MCP gap is genuinely routed around — Claude Code handles its own MCP toolchain inside the session.

**Step 3 — Replace the manual trigger with a condition trigger.**
```toml
[order.sprint-story]
trigger = "condition"
check = "test -f $HOME/projects/<momentum-project>/.momentum/sprint/story-ready.flag"
exec = "scripts/run-momentum-dev.sh"
```
Validates: the Controller polls the condition every ~30 seconds and fires automatically when Momentum writes the ready flag, with the full dispatch → execution → completion loop running without human intervention.

This path avoids Dolt, avoids formula-order complexity, avoids the MCP runtime gap, and avoids the Gas Town topology entirely. The exit ramp is clean: remove `gc`, keep the shell scripts.

### Validation gates before committing beyond the proof of concept

1. **Dispatch loop works end-to-end** — a ready flag triggers a complete Momentum dev cycle with no human keystroke. (Primary success criterion.)
2. **Cost parity** — measure actual API cost for one exec-order-dispatched story cycle; confirm it is comparable to a manual skill invocation. The proof of concept is single-agent, so cost should track manual use — but verify empirically. [PRAC — cost-at-scale risk]
3. **Skill invocation fidelity** — confirm a Momentum skill invoked inside a Gas City-launched `claude -p` session has the same tool access, rules, and context it would have when invoked manually.
4. **Credential isolation** — confirm the `claude -p` subprocess does not opportunistically inherit ambient credentials in a way that crosses project boundaries. Practitioners found Gas Town agents "knew where all the keys were." [PRAC — DoltHub "Two Weeks in Gas Town"]
5. **Controller stability at rest** — run the Controller for several days; confirm no goroutine buildup or runaway restart behavior (the class of bug behind Issue #1930 and the open P1 issues).

### Risks to watch

- **Ecosystem immaturity.** Gas City v1.0 is weeks old; PackV2 is mid-redesign. Lock to a release tag; watch the changelog. [PRAC]
- **The MCP deferral landing.** When Gas City ships native MCP support, formula orders become viable and the exec-order pattern may diverge from recommended convention. Treat the exec-order approach as the proof-of-concept vehicle, not necessarily the permanent architecture.
- **Dolt, if later adopted.** Shared failure surface with Momentum's own Beads adoption. Validate Dolt under concurrent writes for hours before coupling both.
- **Cognitive-model shift.** A background Controller running autonomously is a materially different operational posture than invoking skills by hand — even though it aligns with Momentum's orchestration-over-implementation philosophy.

---

## Cross-Cutting Themes

**The two-products problem is the spine of this report.** Nearly every apparent contradiction in the corpus dissolved once "Gas Town" and "Gas City" were separated. Gas Town is a finished, fixed coding-colony platform — poor fit. Gas City is a composable SDK with one narrowly-relevant subsystem — conditional fit. Any decision, document, or conversation about this must keep the two distinct. [AVFL-FIXED — CON-001]

**Exec orders are the de-risking primitive.** The single most useful finding for an actual adoption decision is that exec orders invoking `claude -p` route around three separate risks at once: the deferred MCP runtime support, formula/pool complexity, and (with `GC_BEADS=file`) the Dolt dependency. The recommended path is not the "intended" Gas City path (formula orders, agent pools) — it is the pragmatic path that stands entirely on shipped, low-churn primitives.

**Gas City's value for Momentum is real but narrow.** It is one capability — persistent, externalized, event-triggered dispatch — not a coordination platform. The Mayor/Deacon/Polecat/Refinery surface, the merge queue, the federation layer, the health-patrol machinery all address problems Momentum does not have at solo scale. Adopting Gas City means adopting Orders and ignoring the rest.

**HITL philosophy is a genuine tension, not a blocker.** Gas Town/Gas City is escalation-centric and autonomy-first; Momentum is approval-centric (explicit push approval). The resolution is to *not* route push approval through Gas City initially — keep the developer's interactive push approval untouched, and let Gas City trigger only the non-push dispatch. The gate primitive exists for later, but it is pull-based and needs notification wiring before it is comfortable.

**The infrastructure-vs-benefit calculus is scale-dependent.** Every "overbuilt" judgment in this report is specific to Momentum's 4–8-agent solo scale. If Momentum's scale changes — multiple concurrent sprints, unattended overnight runs, 15+ parallel agents — the calculus shifts and the fuller Gas City surface (and eventually the Gas Town pack itself) becomes proportionate. The recommendation below is for Momentum as it operates today.

---

## Recommendation

**Adopt Gas City as a scoped dispatcher experiment. Do not adopt the Gas Town topology.**

Gas City's Orders system is the right tool for Momentum's one real dispatcher gap: the absence of any persistent process that reacts to a story becoming ready by starting the work. The Gas Town Colony — Mayor, Deacon, Witness, Polecat, Refinery — is the wrong tool, built for a colony-scale parallel-coding problem Momentum does not have, and should be explicitly ruled out as a deployment model.

**The first step, on a 3–4 week timeline:** run the three-step proof of concept from Section 8. Initialize a `GC_BEADS=file` city (no Dolt), wire one manual exec order that invokes `claude -p` for a Momentum dev cycle, then convert it to a condition trigger on a ready-flag file. Validate against the five gates: dispatch loop works, cost parity holds, skill fidelity holds, credentials stay isolated, the Controller is stable at rest.

**What to keep out of scope for the proof of concept:** migrating story files to Beads, modeling AVFL as a Gas City order, retro integration, sprint-planning integration, formula orders, agent pools, Dolt, and the Gas Town pack. All of these are downstream of proving the dispatch loop itself. Retro in particular should likely *never* move into Gas City — its collaborative-auditor model has no Gas City primitive.

**The bet is small and reversible.** The proof of concept stands entirely on shipped, low-churn primitives, costs roughly what manual use costs at single-agent scale, and has a clean exit ramp — delete the `gc` binary, keep the shell scripts, lose nothing. That asymmetry — small downside, a genuine capability on the upside — is what justifies proceeding.

**One firm caveat:** lock to a specific Gas City release tag and watch the changelog. PackV2 is mid-redesign, and the exec-order pattern is a pragmatic route around the deferred MCP support, not the platform's intended long-term path. When Gas City ships native MCP runtime support, revisit whether formula orders are the better architecture. Until then, exec orders are correct, and the recommendation is to proceed.

---

## Open Questions

These cannot be answered from research and must be settled by the proof of concept or a design session:

1. **Does `GC_BEADS=file` support the Event Bus that event triggers depend on?** The Event Bus appears to be Beads-backed. If file-based storage has reduced fidelity, `bead.created`/`bead.closed` event triggers may be unavailable without Dolt — which is why the proof of concept uses a *condition* trigger (a flag-file check) rather than an event trigger. Confirm whether event triggers work under `GC_BEADS=file` before designing event-driven dispatch.

2. **What exact command does Gas City use to invoke Claude Code, and is it compatible with Momentum's `claude -p` pattern?** The specific arguments (`--dangerously-skip-permissions`, `-p`, etc.) are not confirmed from source. This matters most for formula orders; the exec-order path controls the invocation directly and sidesteps the question.

3. **If Momentum later adopts Dolt-backed Beads, can a `GC_BEADS=file` city migrate to Dolt cleanly, or is it a breaking change?** Determines whether the proof of concept's file-based choice is a dead end or a stepping stone.

4. **Does using exec orders to launch LLM sessions diverge from Gas City's intended conventions in a way that breaks on upgrade?** Exec orders are positioned for "mechanical operations." This usage is supported but unconventional; confirm it is upgrade-safe, or accept that the architecture may need revisiting when MCP support lands.

5. **Is Issue #1930 (Dolt concurrent-write deadlock) resolved in v1.1.0?** The "managed Dolt hardening" release theme suggests progress; the specific issue status is unverified. Relevant only if and when Dolt is adopted.

6. **How do Momentum's Beads usage and a Gas City Beads store coexist?** If both run `bd` against the same project, there may be write contention; if separate, there is story-state duplication. A design session, not more research, is needed.

7. **What is the precise mapping from a Momentum skill to a Gas City formula?** The exec-order path makes this moot for the proof of concept (a shell script invokes `claude -p`). It becomes the highest-value question only if formula orders are pursued post-MCP-support.

---

## Sources

### Official

- Gas Town Documentation — https://docs.gastownhall.ai/ (landing, glossary, architecture, escalation, watchdog chain, polecat lifecycle, propulsion principle, convoy, identity, mail protocol, plugin system)
- Gas City Documentation — https://docs.gascityhall.com/ (quickstart, coming-from-gastown)
- GitHub: gastownhall/gastown — https://github.com/gastownhall/gastown
- GitHub: gastownhall/gascity — https://github.com/gastownhall/gascity (README, releases, `internal/orders/triggers.go`, `internal/runtime/exec/exec.go`, `internal/runtime/tmux/tmux.go`, `engdocs/architecture/orders.md`, `engdocs/architecture/nine-concepts.md`)
- GitHub: gastownhall/beads — https://github.com/gastownhall/beads (ARCHITECTURE.md, FAQ.md, DOLT.md, quickstart)
- Gas City — Coming from Gas Town — https://github.com/gastownhall/gascity/blob/main/docs/getting-started/coming-from-gastown.md
- Gas City — Tutorial 01, Cities and Rigs — https://github.com/gastownhall/gascity/blob/main/docs/tutorials/01-cities-and-rigs.md
- Gas City — Tutorial 07, Orders — https://docs.gascityhall.com/tutorials/07-orders
- tracking: Post-PackV2 package work — Issue #2120 — https://github.com/gastownhall/gascity/issues/2120
- gascity Issue #1930 (Dolt concurrent-write deadlock) — https://github.com/gastownhall/gascity/issues/1930
- gastown Discussion #2531 (Intelligent Routing RFC) — https://github.com/gastownhall/gastown/discussions/2531
- gastown Discussion #624 (lighter-weight solo patterns) — https://github.com/gastownhall/gastown/discussions/624

### Practitioner

- Steve Yegge, "Welcome to Gas Town" (Medium, Jan 2026) — https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04
- Steve Yegge, "Gas Town: from Clown Show to v1.0" (Medium, Apr 2026) — https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec
- Steve Yegge, "Welcome to Gas City" (Medium, Apr 2026) — https://steve-yegge.medium.com/welcome-to-gas-city-57f564bb3607
- "Inside Gas Town" — https://www.augusteo.com/blog/inside-gas-town
- Maggie Appleton, "Gas Town's Agent Patterns, Design Bottlenecks, and Vibecoding at Scale" — https://maggieappleton.com/gastown
- Tenzin Wangdhen, "Gas Town: The Good, The Bad, The Ugly" (Feb 2026) — https://tenzinwangdhen.com/posts/gastown-good-bad-ugly/
- "A Day in Gas Town" — DoltHub Blog (Jan 2026) — https://www.dolthub.com/blog/2026-01-15-a-day-in-gas-town/
- "Two Weeks in Gas Town" — DoltHub Blog (Apr 2026) — https://www.dolthub.com/blog/2026-04-16-two-weeks-in-gastown/
- "Gas Town: What Kubernetes for AI Coding Agents Actually Looks Like" — Cloud Native Now — https://cloudnativenow.com/features/gas-town-what-kubernetes-for-ai-coding-agents-actually-looks-like/
- "GasTown and the Two Kinds of Multi-Agent" — paddo.dev — https://paddo.dev/blog/gastown-two-kinds-of-multi-agent/
- "Building with Gas Town: Multi-Agent AI Development Guide" — Better Stack — https://betterstack.com/community/guides/ai/gas-town-multi-agent/
- "Gas Town: Steve Yegge's Multi-Agent Orchestration Framework" — TorqSoftware Reading List (Jan 2026) — https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/
- "Gas Town: Steve Yegge's Multi-Agent Factory" — Daniel Vaughan, Codex Blog (Apr 2026) — https://codex.danielvaughan.com/2026/04/08/gas-town-multi-agent-factory/
- "Gas Town controls what automated agents are allowed" — Heise.de (v1.0.0 coverage) — https://www.heise.de/en/news/Gas-Town-controls-what-automated-agents-are-allowed-11252281.html
- "Gas Town, Beads, and the Rise of Agentic Development" — Software Engineering Daily (Feb 2026) — https://softwareengineeringdaily.com/2026/02/12/gas-town-beads-and-the-rise-of-agentic-development-with-steve-yegge/
- "Exploring Gas Town" — Eric Koziol, Embracing Enigmas — https://embracingenigmas.substack.com/p/exploring-gas-town
- "Survey of Existing Agent Orchestration Frameworks" — tmchow, GitHub Gist — https://gist.github.com/tmchow/f539adef1d11974eb51478a32a72ff68

### Internal validation and triangulation

- AVFL Validation Report — `validation/avfl-report.md` (35 findings; CON-001 critical, resolved by follow-up)
- Follow-up: Gas Town vs Gas City distinction — `validation/followup-gas-town-vs-gas-city-distinction.md`
- Follow-up: Gas City Orders as standalone dispatcher — `validation/followup-gas-city-orders-standalone.md`
- Gemini Deep Research — follow-up Q&A on PackV2/MCP, Orders event model, and HITL UX — `raw/gemini-deep-research-output.md`
- Practitioner notes (Phase 4 human Q&A) — `raw/practitioner-notes.md`
