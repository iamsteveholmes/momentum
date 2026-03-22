# Raw Research: Momentum Project Architecture Exploration

## Source Agent: Explore agent — Momentum project structure analysis
## Purpose: Understand Momentum's architecture and extension points for CMUX integration assessment

---

## 1. What is Momentum?

Momentum is a **practice framework for agentic engineering** — a complete system for orchestrating AI agents as primary code producers while maintaining absolute quality standards and human accountability. It's implemented using the BMAD Method V6 and Claude Code, but the principles are tool-agnostic.

**Core Value Proposition:**
- Treats specifications as the primary artifact; code is verified, generated output
- Enforces an Authority Hierarchy: Specifications > Tests > Code (agents cannot modify specs/tests to make code pass)
- Implements Producer-Verifier separation (different contexts for writing vs. reviewing)
- Operates an Evaluation Flywheel that traces quality failures upstream to fix workflows, not just code
- Three tiers of enforcement: Deterministic (hooks/automated gates), Structured (workflows), Advisory (rules in context)

## 2. Skills Structure

Skills are YAML-frontmatter-tagged Markdown workflows at `/Users/steve/projects/momentum/skills/`.

**Skill Definition Format:**
```
---
name: <skill-name>
description: <one-liner>
model: <claude-opus-4-6|sonnet|haiku>
effort: <low|medium|high|max>
allowed-tools: [optional, restricts tool access]
context: <fork|omitted> [optional, fork = isolated subagent context]
---
```

**Existing Skills:**
- `momentum/` — Impetus practice orchestrator (session orientation, sprint awareness, workflow access, install/upgrade management)
- `momentum-dev/` — Story development workflow (git worktree management, AVFL quality gate)
- `momentum-create-story/` — Story creation
- `momentum-plan-audit/` — Plan spec impact validation
- `momentum-upstream-fix/` — Quality failure root cause analysis
- `momentum-code-reviewer/` — Adversarial code review (Producer-Verifier pattern)
- `momentum-architecture-guard/` — Architecture pattern enforcement
- `momentum-vfl/` — AVFL quality gate validation

## 3. Agent Definitions

Agents are canonical definitions in `module/canonical/agents/`. Currently minimal:
- **Code Reviewer** (`code-reviewer.md`): 6.7KB adversarial review role definition
- Sub-agents run in fresh context with restricted tool access to enforce isolation

## 4. Existing External Tool Integrations

**Git Worktree Management (momentum-dev):**
- Creates isolated worktrees at `.worktrees/story-{story_key}`
- Lock files for concurrent session safety
- Manages branch creation/deletion

**Skill Helper Scripts:**
- `skills/momentum/scripts/update-story-status.sh` — Story status updater
- `skills/momentum-plan-audit/scripts/check-plan-audited.sh` — PreToolUse hook for plan audit gate

**MCP Server for Findings Ledger (Planned, Epic 6):**
- `mcp/findings-server/` — placeholder, not yet implemented

**Hooks Infrastructure (`.claude/settings.json`):**
- PreToolUse: Blocks ExitPlanMode without Spec Impact, placeholder for file protection
- PostToolUse: Placeholder for linting/formatting
- Stop: Placeholder for quality gate checks

## 5. Module/Canonical Structure

```
module/canonical/
├── agents/
│   └── code-reviewer.md
├── claude-md/ (empty)
├── resources/
│   └── model-routing-guide.md
└── rules/
    └── model-routing.md
```

Canonical files are templates/reference implementations for projects using Momentum.

## 6. Epic 7 — "Bring Your Own Tools" (Critical for CMUX)

Epic 7 stories (currently backlog):
- **7-1:** Project configuration file defines protocol bindings
- **7-2:** Protocol gap resolution creates valid config entries
- **7-3:** Workflow steps resolve through protocol interfaces at invocation time
- **7-4:** Protocol substitution satisfies interface contract
- **7-5:** MCP provider registration and cursor tool ceiling compliance

**How This Could Enable CMUX Integration (speculative — Epic 7 is unimplemented):**
- A project config would define a protocol binding for terminal multiplexing (exact syntax TBD)
- Workflow steps would reference a generic interface (e.g., "execute terminal operation X")
- At runtime: resolves to the configured provider (e.g., a CMUX MCP server)
- Other projects could bind to alternative providers without changing workflows

## 7. Epics Roadmap

| Epic | Status | Purpose |
|------|--------|---------|
| 1 | in-progress (all stories done, epic not formally closed) | Foundation & Bootstrap |
| 2 | in-progress | Stay Oriented with Impetus |
| 3 | backlog | Automatic Quality Enforcement |
| 4 | backlog | Complete Story Cycles |
| 5 | backlog | Trust Artifact Provenance |
| 6 | backlog | The Practice Compounds |
| 7 | **backlog** | **Bring Your Own Tools** |
| 8 | backlog | Research & Knowledge Management |
| 9 | backlog | Performance Validation |

## 8. CMUX Extension Points Identified

1. **Epic 7 Protocol Binding** (most architecturally aligned)
2. **New Skills Using Terminal Operations**
3. **Hook Extensions** (PreToolUse/PostToolUse for terminal sessions)
4. **Worktree-to-Terminal Binding** (spawn CMUX session per story worktree)
5. **Research/Benchmarking Support** (Epic 9)
6. **MCP Server Implementation** (alongside findings-server)

---

## AVFL Validation Report

**Profile:** checkpoint (skepticism 7, 2 iterations)
**Result:** CHECKPOINT_WARNING — 4 findings fixed inline, 1 advisory remaining

### Iteration 1 — Factual Accuracy + Hallucination Detection

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| F1 | MEDIUM | Frontmatter field `tools` does not exist; actual field is `allowed-tools`. Missing `context: fork` field. | **Fixed** — corrected field names in Section 2 |
| F2 | MEDIUM | Epic 1 status shown as "done" but `sprint-status.yaml` says `in-progress` (all stories done, epic not formally transitioned) | **Fixed** — corrected in Section 7 table |
| F3 | LOW | `claude-md/` called "template directory" with no evidence for that characterization | **Fixed** — removed speculative label |
| F4 | LOW | `update-story-status.sh` categorized as a "Hook Script" — it is a skill helper script at `skills/momentum/scripts/`, not a hook | **Fixed** — recategorized with correct path |
| F5 | MEDIUM | Epic 7 CMUX integration example fabricated specific syntax (`protocol.terminal-multiplexer: cmux-server-mcp`) for unimplemented feature | **Fixed** — rewritten with speculative caveat |
| F6 | MEDIUM | Momentum skill description omitted "sprint awareness" and "workflow access" from actual SKILL.md description | **Fixed** — aligned with actual description |

### Iteration 2 — Cross-reference Verification

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| F7 | CLEAN | Section 1 core value proposition claims verified against product-brief and PRD. Authority Hierarchy, Producer-Verifier, Evaluation Flywheel, three enforcement tiers — all confirmed in planning artifacts. | No action needed |
| F8 | CLEAN | All 8 skill directories verified as existing with correct names | No action needed |
| F9 | CLEAN | Module/canonical structure verified: agents/code-reviewer.md (6,759 bytes), resources/model-routing-guide.md, rules/model-routing.md all exist | No action needed |
| F10 | CLEAN | Epic 7 story IDs and descriptions match sprint-status.yaml exactly | No action needed |
| F11 | CLEAN | Hooks infrastructure in `.claude/settings.json` accurately described | No action needed |
| F12 | CLEAN | MCP findings-server exists as placeholder (README.md only) | No action needed |
| F13 | ADVISORY | Several skills (momentum-code-reviewer, momentum-architecture-guard, momentum-upstream-fix, momentum-vfl) are stubs with no implementation. The research does not distinguish implemented skills from stub/placeholder skills. Downstream consumers should be aware that ~50% of listed skills have no workflow logic yet. | Not fixed — editorial choice for final document author |

**No hallucinated features, file paths, or architectural capabilities detected.** All claims trace to real files. The primary issues were field-name inaccuracies in skill frontmatter and status discrepancies — typical of an agent reading structure but not reading file contents carefully.
