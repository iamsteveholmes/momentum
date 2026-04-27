---
topic: "Multi-agent deployment strategies for agentic engineering practice modules — how leading projects deploy skills/workflows/rules/hooks/tools across Claude Code, OpenCode, Codex, Gemini, Goose, ForgeCode, and beyond, as of April 26 2026"
goals: "Inform a potential significant refactor of Momentum to support multi-agent deployment. Primary push: how it's being done technically (file layouts, install scripts, format adapters, manifest formats, invocation lifecycles) — not abstract recommendations. Recency-critical: April 2026 state of the art."
profile: heavy
date: 2026-04-26
sub_questions:
  - "AGENTS.md standard adoption and authoring patterns — Which tools emit/consume AGENTS.md in April 2026, what's in the manifest, what behavior does it actually drive, who writes it (humans vs. tooling)?"
  - "Skill/extension contracts per agent (technical) — For each of Claude Code, OpenCode, Codex CLI, Gemini CLI, Goose, ForgeCode: extension points (skills/commands/rules/hooks/tools/MCP), manifest formats, invocation lifecycle, permissions, sandboxing."
  - "Cross-agent installation architectures (case studies) — How concrete projects beyond BMAD/ECC physically deploy to multiple agents: file layouts, install scripts, format adapters, version pinning. Targets: Aider plugins, Continue, Cody, Roo Code, Cline, plus 3-5 less-obvious examples."
  - "BMAD-method's multi-agent deployment internals (April 2026) — Repo structure, the v6 BMM/BMB/installer, how skills compile to per-agent formats, what's shared vs. per-agent."
  - "everything-claude-code (ECC) as exemplar — What it actually does technically, what's reusable, where it's Claude-Code-specific vs. portable, install/update flow."
  - "Hook/automation parity across agents — How 'automated behaviors on event X' are implemented per agent (Claude Code hooks vs. OpenCode/Goose/Codex equivalents). Where parity is impossible and what fallbacks projects use."
  - "Slash commands, prompts, and rules — format translation — Concrete adapters projects use to translate one logical artifact (a 'skill' or 'workflow') to N agents. Code-level patterns: templating, codegen, runtime detection."
  - "Emerging cross-agent standards — ACP (Zed/JetBrains AIR), Skills.sh, MCP-as-distribution, Devstral/AGENTS.md ecosystem moves. What's authorable today vs. consume-only. Realistic 6-month trajectory."
---

# Research Scope: Multi-agent deployment strategies for agentic engineering practice modules

**Date:** 2026-04-26
**Profile:** heavy
**Goals:** Inform a potential significant refactor of Momentum to support multi-agent deployment. Primary push: **how it's being done technically** (file layouts, install scripts, format adapters, manifest formats, invocation lifecycles) — not abstract recommendations. Recency-critical: April 2026 state of the art.

## Background

Momentum currently targets Claude Code exclusively. Recent research on `everything-claude-code` (ECC) revealed a well-developed pattern for distributing practice modules to a single agent. The user wants Momentum to deploy to no fewer than: Claude Code, OpenCode, Codex (CLI), Gemini (CLI), Goose, and ForgeCode — recognizing that each agent will have different levels of integration depth.

The user emphasizes recency (April 26 2026) and prefers concrete technical implementation detail over theory. They are open to a significant Momentum refactor and want to understand industry patterns from projects beyond BMAD-method and ECC. ACP (Agent Client Protocol from JetBrains AIR/Zed) is acknowledged but flagged as consume-only — does not give the user authoring power.

## Sub-Questions

1. **AGENTS.md standard adoption and authoring patterns** — Which tools emit/consume AGENTS.md in April 2026, what's in the manifest, what behavior does it actually drive, who writes it (humans vs. tooling)?
2. **Skill/extension contracts per agent (technical)** — For each of Claude Code, OpenCode, Codex CLI, Gemini CLI, Goose, ForgeCode: extension points (skills/commands/rules/hooks/tools/MCP), manifest formats, invocation lifecycle, permissions, sandboxing.
3. **Cross-agent installation architectures (case studies)** — How concrete projects beyond BMAD/ECC physically deploy to multiple agents: file layouts, install scripts, format adapters, version pinning. Targets: Aider plugins, Continue, Cody, Roo Code, Cline, plus 3-5 less-obvious examples.
4. **BMAD-method's multi-agent deployment internals (April 2026)** — Repo structure, the v6 BMM/BMB/installer, how skills compile to per-agent formats, what's shared vs. per-agent.
5. **everything-claude-code (ECC) as exemplar** — What it actually does technically, what's reusable, where it's Claude-Code-specific vs. portable, install/update flow.
6. **Hook/automation parity across agents** — How "automated behaviors on event X" are implemented per agent (Claude Code hooks vs. OpenCode/Goose/Codex equivalents). Where parity is impossible and what fallbacks projects use.
7. **Slash commands, prompts, and rules — format translation** — Concrete adapters projects use to translate one logical artifact (a "skill" or "workflow") to N agents. Code-level patterns: templating, codegen, runtime detection.
8. **Emerging cross-agent standards** — ACP (Zed/JetBrains AIR), Skills.sh, MCP-as-distribution, Devstral/AGENTS.md ecosystem moves. What's authorable today vs. consume-only. Realistic 6-month trajectory.
