---
id: AES-001
title: Agent Guidelines Current State — Gen-1 vs. Gen-2 Target
date: '2026-04-09'
status: current
method: session analysis + codebase audit (April 9-11, 2026)
decisions_produced:
  - DEC-001
supersedes: []
---

# AES-001: Agent Guidelines Current State

## Purpose

Evaluate where Momentum's agent guidelines architecture currently stands against the
three-tier target architecture decided in DEC-001. Identify gaps that block sprint agents
from receiving correct, reliable guidelines.

---

## Current State (Gen-1)

### What exists today

**Gen-1 skill (`momentum:agent-guidelines`, status: done)**

Generates two artifact types when run on a project:

| Artifact | Location | Purpose |
|---|---|---|
| Path-scoped rules | `.claude/rules/{technology}.md` | Constraint-only: NEVER/ALWAYS rules, version pins |
| Wiki chunks / reference docs | `docs/guidelines/*.md` or `docs/references/` | Full patterns, worked examples |
| Registry index | `docs/guidelines/index.md` | Agent navigation aid |

**Live example: nornspun-client**

Running as of April 9, 2026:
```
.claude/rules/
  compose-ui.md         — CMP 1.10.3 constraints (path-scoped: **/ui/**/*.kt)
  kotlin-kmp.md         — KMP 2.3.20 constraints (path-scoped: **/*.kt)
  kotlin-testing.md     — Kotest 6.1.11 constraints (path-scoped: **/*Test.kt)
  kmp-build.md          — Gradle 9.4.1 constraints (path-scoped: **/build.gradle.kts)
  android-emulator.md   — Emulator + Maestro rules
  e2e-validation.md     — Black-box E2E rules
  cmux.md               — Terminal pane management
  team-communication.md — Inter-agent messaging

docs/guidelines/
  index.md
  compose-ui-patterns.md     (100-300 lines, domain knowledge)
  kmp-testing-stack.md
  kotlin-kmp-conventions.md
  ktor-sse-patterns.md
  gradle-agp-build.md
```

### Delivery path (gen-1)

```
Agent spawns
    ↓
CLAUDE.md: "Check docs/guidelines/index.md for your domain"
    ↓   (UNRELIABLE — subagents may not load CLAUDE.md: GitHub #29423)
index.md: "For Compose UI, read compose-ui-patterns.md"
    ↓   (CONTINGENT on CLAUDE.md loading)
compose-ui-patterns.md: full domain knowledge
    ↓
.claude/rules/compose-ui.md: hard constraints (path-triggered)
    ↓   (path-scoped regression: GitHub #16299 — may load globally)
Agent has guidelines
```

Every step in this chain is contingent or broken. The path-scoped rules are the most
reliable link but have a confirmed regression. CLAUDE.md inheritance is unreliable.

---

## Gap Analysis

### Gap 1 — No composed specialist agent files (Tier 2)

There are no `.claude/guidelines/agents/` composed files in any project. `sprint-dev`
spawns generic `skills/momentum/agents/dev.md` (or specialist variants) with no baked-in
project knowledge. Guidelines may or may not reach agents via the `.claude/rules/`
chain above.

**Impact:** Every agent spawned in every sprint runs without reliable project-specific
guidelines. Failures manifest as: deprecated API usage, wrong testing framework in wrong
source set, inconsistent commit format, scope creep (agent uses judgment instead of
following project conventions).

**Confirmed instance (nornspun D3 retro):** E2E validator read source code instead of
launching services — because no reliable guidelines delivery reached the agent.
User spent 2.5 hours establishing guidelines the hard way.

### Gap 2 — No hot constitution (Tier 1)

No `constitution.md` equivalent exists in any project. There is no always-guaranteed
cross-cutting context layer for spawned agents.

**Impact:** Critical cross-cutting rules (commit format, authority hierarchy) may not
reach agents. Agents improvise conventions instead of following project standards.

### Gap 3 — No cold KB (Tier 3)

`momentum_vault` exists as a manually built prototype but no tooling exists to scaffold
or maintain it. There is no `momentum:kb-init` or `momentum:kb-ingest` skill.

**Impact:** The `build-guidelines` skill (when built) would have no upstream source of
truth to distill from. Guidelines would be authored from scratch each time rather than
distilled from maintained, versioned, citation-backed knowledge.

### Gap 4 — QA, E2E, PM, SM agents have no guidelines at all

The gen-1 skill generates developer-focused rules (compose-ui, kotlin-kmp, etc.). No
`guidelines-qa.md`, `guidelines-e2e.md`, `guidelines-pm.md` files exist.

**Impact:** QA and E2E agents run entirely on generic training data. No project-specific
antipattern checklists. No Gherkin constraints. No domain vocabulary.

### Gap 5 — No sprint-dev integration

Even if composed agent files were generated, `sprint-dev` currently always spawns from
`skills/momentum/agents/*.md`. There is no detection logic to prefer
`.claude/guidelines/agents/` when present.

---

## Path to Gen-2

| Story | What it closes | Priority |
|---|---|---|
| `kb-init` | Gap 3 (no KB tooling) | high |
| `kb-ingest` | Gap 3 (no KB tooling) | high |
| `build-guidelines-skill` | Gaps 1, 2, 4, 5 | high |

The `dev-agent-definition-files` story (if it exists) and `guidelines-verification-gate`
(ready-for-dev) are complementary but do not close these gaps alone.

---

## What Gen-1 Gets Right

Gen-1 is not wasted work. The wiki chunks (`docs/guidelines/*.md`) and constraint rules
(`.claude/rules/*.md`) generated by gen-1 are:

1. **The correct format** for Tier 3 cold KB pages (they are already Karpathy-style
   pre-synthesized wiki pages with version tables and worked examples)
2. **Directly usable as input** to `kb-ingest` — they can be ingested into the cold KB
   vault as the first batch of domain knowledge
3. **The model for gen-2 reference docs** — the `refs/*.md` files that `build-guidelines`
   generates follow the same format

Gen-1 established the right content shape. Gen-2 fixes the delivery architecture.
