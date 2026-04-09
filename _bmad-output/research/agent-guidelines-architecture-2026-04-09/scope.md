---
topic: "Agent-specific guidelines architecture in Claude Code — optimal strategies for delivering complex, domain-specific behavioral guidelines to individual agents without context dilution"
goals: "Inform a replacement/redesign of the momentum:agent-guidelines skill; maximize guideline adherence for complex technical stacks and non-dev roles; prevent context dilution across agents; support the generic-agent + injected-guidelines = specialized-agent pattern across all Momentum roles"
profile: medium
date: 2026-04-09
sub_questions:
  - "What Claude Code mechanisms most effectively scope guidelines to specific agent roles — CLAUDE.md hierarchy, paths: frontmatter rules, subagent system prompts, worktree isolation — and what are their tradeoffs across all role types?"
  - "What is the empirical relationship between guideline volume, placement in context, and adherence quality — when does adding more guidelines degrade rather than improve results?"
  - "What structural patterns work best for delivering dense, domain-specific technical guidelines (library APIs, mandatory/forbidden patterns, antipattern lists) to specialist agents across any domain?"
  - "How do non-dev agents (QA, E2E, PM, SM) best consume their role-specific guidelines — and how does the optimal delivery mechanism differ by role complexity?"
  - "What are the best architectural patterns for the generic-agent + injected-guidelines = specialized-agent model — how should project-specific guidelines be structured, stored, and delivered?"
  - "What patterns prevent guideline bleed between co-existing roles on the same project, where different agents need radically different knowledge domains?"
---

# Research Scope: Agent-Specific Guidelines Architecture in Claude Code

**Date:** 2026-04-09
**Profile:** medium
**Goals:** Inform a replacement/redesign of the momentum:agent-guidelines skill; maximize guideline adherence for complex technical stacks and non-dev roles; prevent context dilution across agents; support the generic-agent + injected-guidelines = specialized-agent pattern across all Momentum roles

## Context

The core problem: Momentum uses generic agents (dev, QA, E2E, PM, SM, skill-dev, etc.) that get specialized for a specific project via injected guidelines. On the same project you may have backend devs, frontend devs, Kotlin Compose devs, skill devs — all with radically different required knowledge. QA agents need antipattern detection. E2E agents need behavior spec expertise. None of these can share guidelines without diluting each other's context.

The goal is NOT to figure out how to load files — it's to determine the optimal architecture for making generic agents reliably expert at complex, project-specific domains without context bloat or bleed between roles.

## Sub-Questions

1. What Claude Code mechanisms most effectively scope guidelines to specific agent roles — CLAUDE.md hierarchy, paths: frontmatter rules, subagent system prompts, worktree isolation — and what are their tradeoffs across all role types?

2. What is the empirical relationship between guideline volume, placement in context, and adherence quality — when does adding more guidelines degrade rather than improve results?

3. What structural patterns work best for delivering dense, domain-specific technical guidelines (library APIs, mandatory/forbidden patterns, antipattern lists) to specialist agents across any domain?

4. How do non-dev agents (QA, E2E, PM, SM) best consume their role-specific guidelines — and how does the optimal delivery mechanism differ by role complexity?

5. What are the best architectural patterns for the generic-agent + injected-guidelines = specialized-agent model — how should project-specific guidelines be structured, stored, and delivered?

6. What patterns prevent guideline bleed between co-existing roles on the same project, where different agents need radically different knowledge domains?
