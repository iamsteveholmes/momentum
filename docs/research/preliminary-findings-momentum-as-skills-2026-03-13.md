# Preliminary Findings: Momentum as Agent Skills

**Date:** 2026-03-13
**Status:** Preliminary — needs product brief and architecture to formalize

## Context

During the analyst handoff session, research into the Agent Skills open standard and Claude Code's native capabilities revealed that Momentum's packaging strategy should shift from BMAD modules to Agent Skills. This document captures the findings before formal planning begins.

## Strategic Direction

Momentum is primarily a **philosophy and process** for agentic engineering. The implementation uses BMAD V6.x (with its planned skills architecture, agents, and workflows) as the development framework, but Momentum's own deliverables should be:

1. **Standard Agent Skills** — compliant with the [Agent Skills specification](https://agentskills.io/specification), publishable to [skills.sh](https://skills.sh), portable across Claude Code, Cursor, Windsurf, Codex, Copilot, and other adopters
2. **Claude Code optimized** — leveraging Claude Code-specific frontmatter and infrastructure for enhanced enforcement where available

## Key Findings

### The Agent Skills Standard

- Open spec maintained by Anthropic (Apache 2.0), adopted by 15+ tools
- Minimal format: `SKILL.md` with YAML frontmatter + markdown instructions, optional `scripts/`, `references/`, `assets/` directories
- Progressive disclosure: metadata (~100 tokens) loaded at startup, full content loaded on invocation
- Package manager exists: `npx skills` (Vercel), registries at skills.sh (83K+ skills) and skillsmp.com (96K+)
- BMAD already generates skills in this format as of V6

### Claude Code Capabilities Beyond the Spec

Extra YAML frontmatter fields are silently ignored by other tools, so a single SKILL.md can be both compliant and optimized.

| Claude Code Feature | Momentum Use Case |
|---|---|
| `context: fork` | Producer-Verifier isolation — run code review in separate context |
| Hooks (17 events) | Tier 1 deterministic enforcement — test gates, file protection |
| `~/.claude/rules/` | Auto-loaded practice rules every session (PT-001a output) |
| Sub-agents (`~/.claude/agents/`) | Code-reviewer with restricted read-only tool access (PT-003) |
| `model` field | Route review to Opus, routine tasks to Haiku |
| `disable-model-invocation` | Prevent auto-triggering of heavyweight skills |
| Plugins | Future: bundle skills + agents + hooks + MCP + settings |

### Complementary Standards Landscape

- **Agent Skills** = procedures layer (what to do and how)
- **MCP** = capabilities layer (tools and data access)
- **ACP** (Agent Client Protocol by JetBrains/Zed) = agent-to-IDE communication (needs further research — see TR)

### Three Tiers Map to Portability Layers

| Enforcement Tier | Portable (all tools) | Enhanced (Claude Code) |
|---|---|---|
| Tier 1 — Deterministic | Skill instructions say "run tests" | Hooks enforce it automatically |
| Tier 2 — Structured | Workflow steps in skill body | `context: fork` for isolation |
| Tier 3 — Advisory | `references/` loaded by skills | `~/.claude/rules/` auto-loaded every session |

### BMAD Relationship

- BMAD V6.x is the development framework — its agents, workflows, and planning processes are used to BUILD Momentum
- Momentum's deliverables are Agent Skills that encode the agentic engineering practice
- BMAD is moving to skills architecture natively, so these will converge
- Momentum skills can be used with or without BMAD installed

## What Changed From the Original Plan

The practice plan (2026-03-07) Section 8.2 assumed Momentum would be a BMAD custom module with:
- `momentum install` shell script deploying to `~/.claude/`
- `momentum bootstrap` interactive workflow
- Module manifest with `version: null, source: custom`

This is now partially outdated:
- **Shell script install may be unnecessary** — BMAD's Centralized Skills and the skills ecosystem handle distribution
- **Module manifest format is changing** — BMAD is migrating to skills-based architecture
- **The packaging is Agent Skills** — not a proprietary module format
- **Claude Code-specific content** (rules, agents, hooks) supplements the portable skills

## Open Questions

1. How does ACP (Agent Client Protocol) affect our portability strategy? (TR in progress)
2. Should Momentum be a skills.sh package? A BMAD module that generates skills? Both?
3. How do we handle the dual deployment — skills for portability, plus `~/.claude/rules/` and `~/.claude/agents/` for Claude Code enforcement?
4. Does Momentum need a product brief and architecture doc before building, or can we iterate on PT-001a (practice rules) while planning?
5. What is the minimal viable skill set for a "Momentum v0.1" release?

## Next Steps

- [ ] Technical research on ACP and its implications
- [ ] Product brief defining Momentum as a skills-based product
- [ ] Architecture decision: skill structure, dual-deployment strategy, BMAD integration
- [ ] Then resume implementation starting with practice content (PT-001a, PT-003)
