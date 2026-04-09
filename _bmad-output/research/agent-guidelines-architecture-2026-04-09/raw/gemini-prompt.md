Research Topic: Agent-specific guidelines architecture in Claude Code — optimal strategies for delivering complex, domain-specific behavioral guidelines to individual agents without context dilution

I need a comprehensive analysis of how to architect and deliver agent-specific behavioral guidelines in Claude Code for multi-role agentic engineering workflows.

Research Goals: Inform a replacement/redesign of the momentum:agent-guidelines skill; maximize guideline adherence for complex technical stacks and non-dev roles; prevent context dilution across agents; support the generic-agent + injected-guidelines = specialized-agent pattern across all Momentum roles (dev, QA, E2E, PM, SM, skill-dev)

Key questions to investigate:

1. What Claude Code mechanisms most effectively scope guidelines to specific agent roles — CLAUDE.md hierarchy, paths: frontmatter rules, subagent system prompts, worktree isolation — and what are their tradeoffs across all role types?

2. What is the empirical relationship between guideline volume, placement in context, and adherence quality — when does adding more guidelines degrade rather than improve results?

3. What structural patterns work best for delivering dense, domain-specific technical guidelines (library APIs, mandatory/forbidden patterns, antipattern lists) to specialist agents across any domain?

4. How do non-dev agents (QA, E2E, PM, SM) best consume their role-specific guidelines — and how does the optimal delivery mechanism differ by role complexity?

5. What are the best architectural patterns for the generic-agent + injected-guidelines = specialized-agent model — how should project-specific guidelines be structured, stored, and delivered?

6. What patterns prevent guideline bleed between co-existing roles on the same project, where different agents need radically different knowledge domains?

Desired output: A structured report with findings organized by question, including:
- Specific actionable recommendations where available
- Example patterns or implementations where relevant
- Citations with URLs for every factual claim
- An honest assessment of current limitations and gaps

Date context: Today is 2026-04-09. Prioritize current and recent sources.
