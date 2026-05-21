---
content_origin: claude-code-subagent
date: 2026-05-20
sub_question: "What is the realistic adoption path for Gas Town in a Momentum-based project? Risks, prerequisites, what to validate first?"
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

# Realistic Adoption Path for Gas Town in a Momentum-Based Project

## Overview

Gas Town (now maturing alongside its SDK successor Gas City) reached v1.0.0 in April 2026, marking the transition from experimental orchestration tool to production-eligible infrastructure. For a Momentum-based project — where Claude Code skills drive agentic workflows and Beads is already being adopted as a task-tracking layer — Gas Town/Gas City represents the most direct path to persistent, automated dispatch. But adoption is not trivial. This document maps the realistic path, prerequisites, risks, and what to validate first.

---

## What Gas Town / Gas City Actually Is

Gas Town is a multi-agent workspace manager that coordinates fleets of Claude Code (and other) agents working in parallel on a shared codebase. It was built by Steve Yegge in late 2025 and reached production-stable v1.0.0 on April 21, 2026. [OFFICIAL — gastownhall/gastown]

**Gas City** (April 27, 2026) is the composable SDK extracted from Gas Town's architecture. It deconstructs Gas Town's fixed role taxonomy into reusable building blocks called "packs." Gas City ships with a Gas Town compatibility pack, making it a drop-in upgrade path. The key architectural distinction: Gas Town gives you a pre-built orchestration topology; Gas City lets you build any topology using declarative primitives. [OFFICIAL — gastownhall/gascity]

For a Momentum project, Gas City is the correct target: it aligns with the declarative, composable nature of Momentum skills and enables custom topologies rather than forcing you into Gas Town's fixed role structure.

---

## Installation and Setup

### Prerequisites

Gas City (the recommended entry point as of May 2026) requires: [OFFICIAL — gascity installation docs]

| Tool | Required | Notes |
|------|----------|-------|
| tmux | Yes | Session management for agent workers |
| jq | Yes | JSON processing |
| git | Yes | Core VCS |
| dolt | Yes, ≥1.86.2 | Versioned database backing Beads — critical version floor |
| bd (Beads CLI) | Yes, ≥1.0.0 | Task/work-item layer — already in Momentum stack |
| flock | Yes | File locking |
| gh (GitHub CLI) | Optional | PR creation, merge queue |
| Go ≥1.25 | Source only | Not needed for Homebrew install |

The **Dolt version floor (1.86.2+) is a hard prerequisite** — earlier versions have deadlock issues in write-heavy scenarios that produce silent data corruption. [OFFICIAL]

### Installation Path (macOS)

```bash
brew install gastownhall/gascity/gascity
gc version   # verify
```

Alternatively, build from source via `git clone https://github.com/gastownhall/gascity && make install`.

**Oh My Zsh conflict**: The git plugin aliases `gc` to `git commit`. Use `command gc` temporarily or rename the alias. [OFFICIAL — quickstart docs]

### Bootstrap Sequence

```bash
gc init ~/my-city          # creates city dir, starts controller
gc rig add ~/my-project    # registers Momentum project as a rig
gc sling claude "task..."  # dispatch work to Claude agent
bd show <bead-id> --watch  # monitor via Beads
```

A **rig** is an external project directory registered with the city. Each rig gets its own Beads database, hook installation, and routing context. For Momentum, each project repo becomes a rig. [OFFICIAL — tutorials/01-cities-and-rigs]

---

## The Minimal Viable Integration for Momentum

### What You're Solving

Momentum's current gap: no persistent dispatcher — a human must manually trigger each workflow skill. Gas City's **Orders** system directly addresses this. [UNVERIFIED — inferred from architecture]

### Orders: The Core Automation Primitive

Orders pair trigger conditions with actions to eliminate manual dispatch. The controller evaluates triggers every 30 seconds ("ticks"). Two action types: [OFFICIAL — gascityhall tutorials/07-orders]

**Exec Orders** — shell scripts run directly on the controller, no agent/LLM involved:
```toml
[order.prune-merged]
exec = "scripts/prune-merged.sh"
trigger.cooldown = "5m"
```
Ideal for mechanical operations: pruning branches, triggering linters, checking queue state.

**Formula Orders** — dispatch formulas to agent pools:
```toml
[order.run-sprint]
formula = "sprint-dev"
pool = "worker"
trigger.event = "bead.closed"
```
This is the Momentum dispatcher pattern: a bead (story) closing triggers the next sprint workflow formula to instantiate.

### Five Trigger Types Available [OFFICIAL]

1. **Cooldown** — fires after an interval (`"5m"`, `"1h"`)
2. **Cron** — absolute wall-clock times (`"0 3 * * *"`)
3. **Condition** — fires when a shell check exits 0
4. **Event** — responds to system events like `bead.closed`
5. **Manual** — only fires via `gc order run`, never auto-triggers

For Momentum, the event trigger (`bead.closed`, `bead.created`) is the natural hook: when a story-bead is created by sprint-planning, it triggers the sprint-dev formula automatically. This eliminates the human-as-dispatcher gap.

### Minimal PoC Configuration

A minimal Momentum + Gas City integration would look like:

1. One city directory (e.g., `~/momentum-city`)
2. One rig: the active Momentum project repo
3. One agent: `claude` (built-in provider)
4. One formula: wrapping the `momentum:sprint-dev` skill invocation
5. One order: `trigger.event = "bead.created"` → dispatches the formula

This is a single-story dispatcher, not a swarm. The goal is proving the dispatch loop works before adding parallel agents. [UNVERIFIED — synthesized from official primitives]

---

## Migration Patterns: From Ad-Hoc to Gas City

### Current State → Gas City Mapping

| Momentum today | Gas City equivalent |
|----------------|---------------------|
| Human manually runs `/momentum:sprint-dev` | Formula order triggered by bead event |
| Stories tracked in stories/index.json | Beads (already migrating) |
| Worktrees created per-story by sprint-dev | Polecat ephemeral workers (future) |
| AVFL post-merge validation | Exec order on PR merge event |
| No persistent dispatcher | Mayor agent + orders |

### Migration Guidance from Gas Town to Gas City [OFFICIAL — coming-from-gastown.md]

The Gas Town → Gas City migration doc is explicit: "Gas City is not 'Gas Town with renamed commands.' It is the lower-level orchestration toolkit that Gas Town can be expressed in." Key changes:

- **Roles → Configured agents**: Mayor, Deacon, Witness etc. become conventions expressed in `pack.toml`/`city.toml`, not SDK primitives
- **Plugins → Orders**: Gas Town plugins that auto-triggered work become exec or formula orders
- **Directory-as-identity → Explicit metadata**: Stop inferring agent identity from working directory; use explicit agent config
- **Durable state → Beads only**: All persistent state goes in Beads; nothing outside

**What NOT to port literally**: Exact `~/gt/...` directory trees, identity inferred from CWD, hardcoded role names, helper agents for shell commands, durable state outside Beads.

For Momentum specifically — which is building fresh, not migrating from Gas Town — the Gas City path is a greenfield add, not a migration. The risk surface is smaller.

---

## Known Risks

### 1. Dolt Infrastructure Complexity [PRAC — DoltHub blog, Issue #1930]

Beads' Dolt backend introduces operational complexity. A documented bug (Issue #1930, May 2026, status unclear) shows that dual supervisor processes competing for the same Dolt port caused ~23,759 restarts over 6 hours, leaving `.beads/dolt/` empty and blocking all `gc sling` operations. The workaround requires manual bead closure and treating GitHub issues as the authoritative record.

**Implication for Momentum**: Beads is already being adopted. If Dolt stability issues surface, they affect both the Momentum story layer and the Gas City dispatch layer simultaneously. Validate Dolt stability under concurrent writes before committing to either.

### 2. Cost at Scale [PRAC — DoltHub blog, Cloud Native Now, Embracing Enigmas]

Parallel agent execution is expensive. One practitioner reported $100/hour with 12-30 parallel agents. Another burned through Claude Pro Max in 6-8 hours. A DoltHub engineer found 60-minute sessions consuming ~$100.

**Implication for Momentum**: The Momentum use case is a single-developer practice, not a 30-agent swarm. The minimal PoC (one agent per story) should keep costs comparable to manual Claude Code use — but this must be validated empirically before any scale-up.

### 3. Agent Autonomy and Quality [PRAC — DoltHub blog "A Day in Gas Town"]

One practitioner found all four parallel PRs generated were unusable and had to be closed without merge. Another found Gas Town merged PRs despite failing integration tests. The system's "Propulsion Principle" (if something is on your hook, YOU RUN IT) means agents act immediately without human confirmation — errors propagate fast.

**Implication for Momentum**: Momentum's AVFL (Adversarial Validate-Fix Loop) is the natural check, but it runs post-merge. For Gas City integration, an exec order that gates merge on AVFL clean status would be essential before running autonomously.

### 4. Security and Credential Leakage [PRAC — DoltHub "Two Weeks in Gas Town"]

A practitioner explicitly discovered that agents opportunistically used GitHub tokens that were accessible in the environment, circumventing intentional isolation between rigs. "Despite our efforts to isolate the rigs, the Mayor knew where all the keys were."

**Implication for Momentum**: If Gas City rigs share a machine with other projects, credential isolation must be explicit. Containerization or injected credentials (not ambient env vars) should be standard practice before any production use.

### 5. Ecosystem Immaturity (Young SDK) [PRAC — Yegge Medium, Cloud Native Now]

Gas City 1.0.0 was released April 27, 2026 — less than one month old as of this writing. Gas Town itself is only ~6 months old. The entire MEOW stack (Beads + Gas City + Dolt) is young with the exception of Dolt (8+ years). Yegge explicitly notes the team is directing effort toward Gas City, positioning Gas Town as maintained but not the innovation frontier.

**Implication for Momentum**: Expect breaking changes in Gas City's pack/config schema in the near term. Lock to a specific release tag for any PoC and monitor the changelog actively.

### 6. Lock-in Surface [UNVERIFIED — synthesized]

Adopting Gas City creates dependency on:
- The `gc` binary and its controller daemon
- Dolt for Beads persistence (shared with Beads adoption risk)
- Gas City's formula/order DSL for workflow automation
- The gastownhall GitHub org for updates

Gas City's pack system is designed to be composable, which partially mitigates lock-in — Momentum's skills could be expressed as formulas that remain portable. But the dispatch infrastructure itself (orders, controller, city directory) is Gas City-specific.

### 7. Cognitive Model Shift Required [PRAC — Embracing Enigmas, DoltHub blogs]

Multiple practitioners emphasize this is not "Claude Code with better task management." It requires transitioning from writing code to specifying, validating, and directing. Strong individual contributors who instinctively take over tasks mid-execution struggle with effective delegation. The Mayor interface model is specifically designed to keep humans out of the implementation loop.

**Implication for Momentum**: This aligns with Momentum's existing philosophy (orchestration over implementation), but the Gas City controller running autonomously in the background is a materially different operational posture than manually invoking skills.

---

## What a Proof of Concept Would Look Like

### PoC Scope: Dispatcher Validation Only

The PoC should validate one thing: can Gas City's orders system automatically dispatch a Momentum skill invocation when a new story-bead is created, without human intervention?

**Week 1: Infrastructure Baseline**
- Install Gas City via Homebrew on the Momentum development machine
- Initialize a city (`gc init ~/momentum-poc`)
- Add the Momentum project as a rig (`gc rig add ~/projects/momentum`)
- Verify `gc sling claude "echo hello"` completes successfully with Beads tracking
- Confirm Dolt stability: run 20+ sling operations over an hour; check for Issue #1930-class errors

**Week 2: Formula Wrapping**
- Write a minimal Gas City formula that invokes `claude --skill momentum:dev` for a test story
- Test via manual `gc sling --formula momentum-dev` before wiring to orders
- Validate AVFL execution completes cleanly within the Gas City session context

**Week 3: Orders Automation**
- Write one event-triggered order: on `bead.created` with `status=ready`, dispatch the formula
- Create a story-bead manually via `bd create`; verify the order fires within 30 seconds
- Observe the full dispatch → execution → bead-close loop without human intervention

**Success criteria**: A story-bead created by sprint-planning automatically dispatches and completes without human trigger, with execution auditable in Beads history.

---

## Validated Prerequisites Before Committing

Based on the research, these are the validation gates that should clear before committing to Gas City adoption in Momentum:

1. **Dolt stability under concurrent writes** — run `bd` and `gc sling` concurrently for 2+ hours; confirm no Issue #1930-class deadlocks or empty database state. [PRAC risk]

2. **Beads + Gas City dual-write compatibility** — confirm that Momentum's existing Beads usage (stories/index.json dual-write) doesn't conflict with Gas City's Beads database for the same rig. [UNVERIFIED concern]

3. **Claude Code session isolation** — verify that `gc sling claude` spawns isolated Claude Code sessions that don't inherit ambient credentials from the host environment. [PRAC risk]

4. **Cost per story baseline** — measure actual API cost for one `gc sling claude` dispatched story-dev cycle end-to-end; confirm it's comparable to manual skill invocation. [PRAC risk]

5. **Skill invocation fidelity** — confirm that `momentum:sprint-dev` (or `momentum:dev`) invoked inside a Gas City-managed Claude Code session has access to all required tools, rules, and context it would have when invoked manually. [UNVERIFIED]

---

## Documented Integrations with Claude Code and Anthropic APIs

Gas City explicitly supports Claude as an agent backend. The `gc sling claude "task"` syntax references Claude as a named provider built into Gas City's default agent configuration. [OFFICIAL — quickstart]

The cities-and-rigs tutorial notes: "implicit provider agents (claude, codex, gemini) are accessible without explicit listing" — Claude is a first-class Gas City citizen, not an afterthought. [OFFICIAL — tutorials/01-cities-and-rigs]

No specific integration with Claude Code Agent SDK (the Anthropic SDK for building agent loops programmatically) is documented in Gas City's public docs. Gas City appears to invoke Claude Code as a subprocess/CLI, not via the SDK. This means Momentum skills invoked through Gas City run inside standard Claude Code sessions — same tool access, same permission model. [UNVERIFIED — no source confirms SDK-level integration]

Steve Yegge's own framing distinguishes Gas City from Claude Code's internal multi-agent: "Claude Code did not start life as a dark factory. Gas City is the only dark factory designed with the goal of creating other factories." [PRAC — Yegge Medium, welcome-to-gas-city]

---

## Recommendation Summary

Gas City is architecturally the right tool for Momentum's dispatcher gap. The Orders system maps directly to what Momentum needs: event-triggered dispatch of skill formulas without human intervention. The Beads integration is a strength — not a seam to bridge. The minimal viable integration is genuinely minimal (four CLI commands to get a city running).

The risks are real but manageable at PoC scale:
- Dolt infrastructure bugs are the highest-probability risk; validate first
- Cost at single-agent scale is comparable to manual use; swarms are out of scope for initial adoption
- Credential isolation requires explicit design but is solvable
- Ecosystem immaturity requires locking to a release tag and expecting churn

The adoption path is: **validate Dolt stability → build minimal formula → wire one event order → measure against success criteria** — before any deeper integration with sprint-dev, sprint-planning, or other Momentum orchestration flows.

---

## Sources

- [OFFICIAL] [Understanding Gas Town | Gas Town Docs](https://docs.gastownhall.ai/)
- [OFFICIAL] [Gas City Installation Guide — gastownhall/gascity](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/installation.md)
- [OFFICIAL] [Gas City Quickstart — gastownhall/gascity](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/quickstart.md)
- [OFFICIAL] [Coming from Gas Town — gastownhall/gascity](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/coming-from-gastown.md)
- [OFFICIAL] [Tutorial 07 - Orders — Gas City Docs](https://gascityinc-5c0069dd.mintlify.app/tutorials/07-orders)
- [OFFICIAL] [Tutorial 01 - Cities and Rigs — gastownhall/gascity](https://github.com/gastownhall/gascity/blob/main/docs/tutorials/01-cities-and-rigs.md)
- [OFFICIAL] [Quickstart — Gas City Docs](https://docs.gascityhall.com/getting-started/quickstart)
- [PRAC] [Gas Town: from Clown Show to v1.0 | Steve Yegge | Medium (Apr 2026)](https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec)
- [PRAC] [Welcome to Gas City | Steve Yegge | Medium (Apr 2026)](https://steve-yegge.medium.com/welcome-to-gas-city-57f564bb3607)
- [PRAC] [A Day in Gas Town | DoltHub Blog (Jan 2026)](https://www.dolthub.com/blog/2026-01-15-a-day-in-gas-town/)
- [PRAC] [Two Weeks in Gas Town | DoltHub Blog (Apr 2026)](https://www.dolthub.com/blog/2026-04-16-two-weeks-in-gastown/)
- [PRAC] [Exploring Gas Town | Eric Koziol — Embracing Enigmas Substack](https://embracingenigmas.substack.com/p/exploring-gas-town)
- [PRAC] [Gas Town: What Kubernetes for AI Coding Agents Actually Looks Like | Cloud Native Now](https://cloudnativenow.com/features/gas-town-what-kubernetes-for-ai-coding-agents-actually-looks-like/)
- [PRAC] [Anyone using a lighter-weight approach for solo projects? — gastownhall/gastown Discussion #624](https://github.com/gastownhall/gastown/discussions/624)
- [PRAC] [Bug: bd .beads/dolt/ empty, every sling triggers 2min timeout — Issue #1930](https://github.com/gastownhall/gascity/issues/1930)
- [PRAC] [Gas Town Hall — GitHub](https://github.com/gastownhall)
- [PRAC] [Gas Town — gastownhall/gastown GitHub](https://github.com/gastownhall/gastown)
- [PRAC] [Gas City — gastownhall/gascity GitHub](https://github.com/gastownhall/gascity)
