# Agentic Architecture: BMAD Agents vs Claude Code Native Agents

**Date:** 2026-03-07
**Researcher:** Mary (Business Analyst Agent)
**Status:** Complete
**Related:** [Subagent Permissions Reference](./technical-subagent-permissions-reference-2026-03-07.md)

---

## The Core Question

> "Many of my BMAD agents use subagents, but I might have Verdandi call Urd — is that even a real thing?"

**Short answer: No.** BMAD agents cannot call each other as Claude Code subagents. They're fundamentally different systems that serve different purposes. This document explains exactly what's happening at each layer.

---

## Two Completely Different Agent Systems

### System 1: BMAD Agents (Persona Directors)

**What they are:** Markdown files with XML blocks that instruct Claude to adopt a persona, display a menu, and orchestrate workflows. They run **in your main conversation** — they're not separate processes.

**Location:** `_bmad/*/agents/*.md` (e.g., `_bmad/nornspun/agents/verdandi.md`)

**Format:**
```xml
<agent name="Verdandi" title="Session Architect" icon="fire">
  <activation>... load config, greet user, show menu ...</activation>
  <persona>... role, identity, communication style ...</persona>
  <menu>... numbered list of workflows ...</menu>
  <rules>... behavioral constraints ...</rules>
</agent>
```

**How activation works:** When you run `/bmad-agent-nornspun-verdandi`, Claude Code:
1. Reads the markdown file
2. Injects it into the current conversation as instructions
3. Claude adopts the persona and follows the activation steps
4. **The same Claude instance** that was talking to you is now "Verdandi"

**Critical insight:** There is no separate process, no subprocess, no isolated context. Verdandi IS Claude, following instructions.

### System 2: Claude Code Native Agents (Worker Subprocesses)

**What they are:** Markdown files with YAML frontmatter that define specialized subagents spawned by the `Agent` tool. They run as **isolated subprocesses** with their own context window.

**Location:** `.claude/agents/**/*.md` (e.g., `.claude/agents/bmad-research/market-researcher.md`)

**Format:**
```yaml
---
name: bmm-market-researcher
description: Conducts comprehensive market research...
tools: Read, Grep, Glob, WebFetch, WebSearch
model: sonnet
---

You are a Market Research Specialist...
```

**How they work:** When Claude calls `Agent(subagent_type="bmm-market-researcher")`:
1. A **new Claude subprocess** is spawned
2. It gets a **fresh, isolated context** (no parent conversation history)
3. It gets the markdown body as its system prompt
4. It gets the project's CLAUDE.md files (auto-loaded)
5. It does its work and returns a single result to the parent
6. The subprocess ends

### The Fundamental Difference

| Aspect | BMAD Agent (Persona) | Claude Code Agent (Worker) |
|--------|---------------------|---------------------------|
| **Runtime** | Same Claude instance as you | Separate subprocess |
| **Context** | Shares your full conversation | Fresh, isolated context |
| **Activation** | Slash command injects persona | `Agent` tool spawns process |
| **Persistence** | Lives until dismissed or replaced | Lives until task complete |
| **Interactivity** | Menu-driven, conversational | Task-in, result-out |
| **Tool permissions** | None (instructional only) | Yes (`tools:`, `disallowedTools:`) |
| **Can call Agent tool** | Yes (it's your main session) | **No** (subagents cannot nest) |
| **Can show menus** | Yes | No |
| **Can use slash commands** | Yes | No |

---

## Can Verdandi Call Urd? What Actually Happens

### What You Might Expect

You might imagine Verdandi saying "I need campaign data, let me spin up Urd as a subagent to get it." This would mean:
1. Verdandi (running in your session) calls `Agent(subagent_type="urd")`
2. Urd runs as a subprocess, loads campaign data
3. Urd returns results to Verdandi
4. Verdandi continues with the data

### Why This Doesn't Work

1. **BMAD agents aren't registered as Claude Code native agents.** There's no file at `.claude/agents/urd.md` with `name: urd`. Urd lives at `_bmad/nornspun/agents/urd.md` — Claude Code's Agent tool doesn't look there.

2. **Even if you created one, it wouldn't be Urd.** A Claude Code native agent gets the markdown body as a system prompt but has no menus, no activation sequence, no config loading, no slash command access. It would be a stripped-down version that merely has Urd's personality text.

3. **BMAD agents are designed for interactive sessions, not task-in/result-out.** Urd's activation sequence expects to greet the user, show a menu, and wait for input. That interaction model doesn't work inside a subprocess that needs to do a task and return a result.

### What BMAD Actually Does Instead

BMAD agents communicate through **three patterns**, none of which involve spawning each other:

#### Pattern 1: Warm Redirects (Tell the User to Switch)

When Verdandi or Skuld can't proceed because no campaign exists, they redirect the user:

```
Verdandi: "The workbench is ready, but there's no campaign to prepare for, Spinner.
Let Urd help you establish your campaign first — then we'll make magic together."
```

This is a **message to you**, not a function call. You manually switch to Urd.

#### Pattern 2: Shared Living Memory (Data Layer Communication)

The Norns communicate through shared files:

```
Urd writes:    tracker.json, campaign-index.json, npcs/index.json
Verdandi reads: tracker.json, campaign-index.json, npcs/index.json
Skuld reads:    tracker.json, campaign-index.json
Skuld writes:   adventure-index.json
```

This is **asynchronous, data-mediated communication**. Urd doesn't call Verdandi — Urd writes data that Verdandi later reads. They share a context-loader protocol (`_bmad/nornspun/shared/context-loader.md`) to ensure consistency.

#### Pattern 3: Party Mode (Orchestrated Multi-Persona Conversation)

Party Mode is the only mechanism for agents to "talk to each other." But it's not subagent delegation — it's **one Claude instance rapidly switching personas** in a single conversation:

```
Facilitator: "What are your thoughts on the temple encounter?"
Verdandi: "The haunt mechanics need to be..."
Skuld: "Building on what Verdandi said, the creature balance..."
Urd: "Looking at the session history, the party tends to..."
```

All of this is the same Claude instance, in one conversation, roleplaying as multiple agents sequentially. No subprocesses are involved.

---

## What BMAD Workflows Mean by "Use Subagents"

When BMAD workflow files say:

> **"UTILIZE SUBPROCESSES AND SUBAGENTS"**: Use research subagents, subprocesses or parallel processing if available to thoroughly analyze different areas simultaneously.

They mean **Claude Code native worker agents** — the files in `.claude/agents/`:

- `bmm-market-researcher` — for market research tasks
- `bmm-codebase-analyzer` — for codebase analysis
- `bmm-data-analyst` — for quantitative analysis
- `bmm-technical-evaluator` — for tech feasibility
- etc.

These are lightweight, focused specialists. They're NOT BMAD persona agents. The naming (`bmm-` prefix) shows they were installed by the BMM module specifically as Claude Code native agents.

---

## The Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│  YOUR CLAUDE CODE SESSION                           │
│  (permissions from settings.local.json)             │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │  BMAD AGENT (Persona Layer)                   │  │
│  │  e.g., Verdandi, Urd, Mary, Morgan            │  │
│  │                                               │  │
│  │  - Loaded via slash command                   │  │
│  │  - Runs as instructions in THIS session       │  │
│  │  - Has menus, persona, activation steps       │  │
│  │  - CAN use the Agent tool (it's your session) │  │
│  │  - CANNOT call other BMAD agents as subagents │  │
│  │                                               │  │
│  │  When workflows say "use subagents":          │  │
│  │  ┌─────────────────────┐ ┌─────────────────┐  │  │
│  │  │ CC Native Agent     │ │ CC Native Agent  │  │  │
│  │  │ bmm-market-researcher│ │ Explore         │  │  │
│  │  │ (subprocess)        │ │ (subprocess)     │  │  │
│  │  │ - isolated context  │ │ - isolated ctx   │  │  │
│  │  │ - returns result    │ │ - returns result │  │  │
│  │  │ - CANNOT nest       │ │ - CANNOT nest    │  │  │
│  │  └─────────────────────┘ └─────────────────┘  │  │
│  │                                               │  │
│  │  Agent-to-agent communication:                │  │
│  │  - Warm redirects (tell user to switch)       │  │
│  │  - Shared data files (living memory)          │  │
│  │  - Party Mode (same session, persona cycling) │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  Settings: Read, Glob, Grep, Agent = allowed        │
│  Deny: rm -rf, force push, hard reset               │
│  Ask: rm, git push                                  │
└─────────────────────────────────────────────────────┘
```

---

## Comparison with Kiro-Code

In Kiro-Code, you explicitly name subagents to make them behave as BMAD agents — the subagent system supports adopting full personas with menus and interactive behavior.

Claude Code's subagent system is different:

| Capability | Kiro-Code | Claude Code |
|-----------|-----------|-------------|
| Subagent adopts full BMAD persona | Yes (by name) | No (stripped-down only) |
| Subagent has menus/interactivity | Yes | No (task-in, result-out) |
| Subagent can spawn subagents | Varies | No (hard constraint) |
| Subagent shares parent context | Configurable | No (always isolated) |
| Agent-to-agent calls | Direct | Not supported |
| Persona switching in session | N/A | Yes (BMAD agents replace each other) |

Claude Code subagents are **workers**, not **personas**. They're designed for parallel task execution (research, analysis, code review), not for interactive role-based workflows.

---

## Practical Implications for Your Agents

### What Works Today
- BMAD agents orchestrating Claude Code native workers (market researcher, codebase analyzer, etc.)
- BMAD agents reading shared data written by other BMAD agents (living memory pattern)
- Party Mode for multi-agent creative discussion
- Warm redirects telling the user to switch agents

### What Doesn't Work
- One BMAD agent calling another BMAD agent as a subprocess
- Subagents spawning their own subagents (no nesting)
- Subagents running interactive menus or activation sequences
- Subagents executing slash commands

### Design Recommendations
1. **Keep BMAD agents as directors** — they orchestrate, interact, and guide
2. **Keep Claude Code native agents as workers** — they do focused tasks and return results
3. **Use living memory for cross-agent communication** — this is BMAD's actual inter-agent protocol
4. **Don't try to make subagents into BMAD agents** — the interaction models are incompatible
5. **If you need an agent's knowledge in a subagent**, extract the relevant knowledge into a shared resource file and reference it from the worker agent's prompt, rather than trying to load the full BMAD persona
