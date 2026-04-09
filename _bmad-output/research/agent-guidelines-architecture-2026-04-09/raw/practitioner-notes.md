---
content_origin: human
date: 2026-04-09
topic: "Agent-specific guidelines architecture in Claude Code"
---

# Practitioner Notes — Steve Holmes, 2026-04-09

## Q1: Instruction count threshold (19-rule ceiling vs. 100-150)

Resolved by background research — no practitioner override needed. The "19-rule ceiling" from Gemini Deep Research is unsupported by cross-corpus evidence. The IFScale-grounded figure of 100–150 effective instruction slots applies to reasoning-class models; for Claude Sonnet-class agents (the primary Momentum workhorse), linear decay begins earlier. Anthropic's official guidance is "under 200 lines per file." Working design limit for Momentum: **100 lines per always-loaded rules file**, with overflow into JIT-referenced docs.

## Q2: CLAUDE.md inheritance by subagents — Architecture clarification

**Critical practitioner finding from setup inspection:**

Steve runs Claude Code CLI from Zsh terminal (`claude` command). All Momentum agents are spawned via the Agent tool with agent definition bodies (`skills/momentum/agents/*.md`) used as system prompts. There is NO `~/.claude/agents/` directory. Agents are NOT registered as pre-built Claude Code agents — they are prompt-injected at spawn time.

**How guidelines currently flow:**
- The main CLI session DOES load `.claude/rules/` files (path-scoped, JIT on file access)
- Subagents (dev, QA, E2E) receive their context via Agent tool prompt injection
- `dev.md` already accepts a `guidelines` parameter — "path to role-specific guidelines file, or null if none" — and reads it explicitly in Step 1
- QA, E2E, PM, SM agents have NO equivalent explicit guidelines injection — their role guidelines are hardcoded in the agent definition bodies

**Architectural gap identified:**
The current `agent-guidelines` skill generates `.claude/rules/` files. These load for the main CLI session but are NOT reliably inherited by Task/SDK-spawned subagents (confirmed by GitHub issues #8395 "not planned" and #29423 open April 2026). The dev agent works around this via explicit `guidelines` parameter injection, but all other roles lack this mechanism.

**Design implication for new skill:**
The new `agent-guidelines` skill must generate guidelines in TWO forms:
1. `.claude/rules/` path-scoped files for the main CLI session (current behavior — keep)
2. Role-specific reference files that can be injected via sprint-dev's `guidelines` parameter (or equivalent) when spawning each role's agent

Q1 2026 `paths:` regression (GitHub #16299): the path-scoped JIT loading may not be working correctly for some users — the safe fallback is always explicit injection.

## Q3: Q1 2026 unverified Gemini feature claims

Resolved by cross-corpus research — no practitioner override needed. Four features cited in Gemini follow-ups (`initialPrompt` field on subagents, Event-Driven System Reminders, `managed-settings.d/` drop-in configs, Artifact Channels) could not be corroborated across 6 independent research agents. These appear to be Gemini confabulations and should be excluded from the synthesis document. Do not base design decisions on them.

## Additional practitioner context

- Project uses `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` — Agent Teams are enabled
- Skills are loaded via the Momentum plugin (GitHub: iamsteveholmes/momentum)
- The agent-guidelines skill is the skill under review — sprint-dev passes `guidelines` to dev agents but NOT to QA, E2E, or other specialist agents
- The user's goal: "generic agents + injected guidelines = specialized agents" across ALL roles, not just dev
- `alwaysThinkingEnabled: true` and `effortLevel: high` are set globally
