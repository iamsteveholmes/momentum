Research Topic: Multi-agent deployment strategies for agentic engineering practice modules — how leading projects in April 2026 deploy skills/workflows/rules/hooks/tools across Claude Code, OpenCode, Codex CLI, Gemini CLI, Goose, ForgeCode, and beyond.

I need a comprehensive technical analysis of how the industry currently distributes and installs reusable practice modules — bundles of skills, workflows, rules, hooks, slash commands, sub-agents, and tools — across multiple AI coding agents. The goal is to inform a refactor of an existing single-agent practice module ("Momentum", currently Claude Code only) into a multi-agent module.

Recency is critical. Today is 2026-04-26. Prioritize sources from the last 6 months (October 2025 onward). Discard anything older than 12 months unless it is foundational standard documentation.

I am NOT looking for general theory or recommendations about "you should support multiple agents." I am looking for **concrete implementation detail**: file layouts, manifest formats, install scripts, format adapter code, version pinning strategies, plugin contracts, hook lifecycles, MCP configurations, and real repository structures. Show me exactly how it is done by people doing it well.

Research Goals:
- Catalog the technical extension contract of each target agent (Claude Code, OpenCode, Codex CLI, Gemini CLI, Goose, ForgeCode)
- Find concrete projects beyond BMAD-method and everything-claude-code that ship to multiple agents — describe their architectures
- Understand the AGENTS.md ecosystem in April 2026: who emits, who consumes, what's actually in the file, what behavior does it drive
- Understand hook/automation parity gaps and the fallback patterns projects use when an agent lacks a feature
- Understand format-translation patterns (one logical "skill" → N agent-specific artifacts): templating, codegen, runtime detection
- Surface emerging cross-agent standards: ACP (Agent Client Protocol from Zed/JetBrains AIR), Skills.sh, MCP-as-distribution, the AGENTS.md ecosystem — distinguishing authorable today vs. consume-only

Key questions to investigate:

1. **AGENTS.md standard adoption and authoring patterns (April 2026)** — Which tools emit AGENTS.md? Which consume it? What's actually in the manifest spec? What behavior does it drive (instructions only, or richer)? Who writes it — humans, codegen, or both? Show repo examples.

2. **Skill/extension contracts per agent (technical)** — For each of: Claude Code, OpenCode, Codex CLI, Gemini CLI, Goose, ForgeCode — document (a) what extension points exist (skills, commands, rules, hooks, tools, MCP, sub-agents, plugins, marketplaces), (b) the manifest format for each (frontmatter, JSON schema), (c) invocation lifecycle (how the agent decides to fire a skill), (d) permissioning and sandboxing model, (e) where it loads files from, (f) plugin/marketplace mechanics. Cite official docs and repo source.

3. **Cross-agent installation architectures (case studies beyond BMAD/ECC)** — Survey concrete projects that ship to more than one agent. Targets I want covered if they exist: Aider config sets, Continue.dev rule packs, Sourcegraph Cody prompt libraries, Roo Code, Cline, Kilo Code, OpenHands, plus any 3-5 less-obvious examples I haven't named. For each: file layout, install script, what's a single source of truth, what's compiled per-agent, version pinning, update mechanism.

4. **BMAD-method's multi-agent deployment internals (April 2026)** — The BMAD v6 BMM/BMB modules and installer. How does a single skill or agent definition compile to per-agent output? What is shared across agents vs. duplicated? How does it handle CLI agents (Claude Code, Codex, Gemini, OpenCode) vs. IDE agents (Cursor, Windsurf)? What does the installer do step by step? Show the relevant repo paths.

5. **everything-claude-code (ECC) as exemplar** — Walk through ECC's repo structure, install/update flow, what's distributable, what's Claude-Code-specific vs. potentially portable. What would have to change for ECC to ship to OpenCode or Codex?

6. **Hook/automation parity across agents** — Claude Code hooks (PreToolUse, PostToolUse, UserPromptSubmit, SessionStart, Stop, etc.) are powerful. What does each of OpenCode, Codex, Gemini CLI, Goose, ForgeCode offer for "automated behavior on event X"? Where there is no equivalent, what fallbacks do real projects use (system prompt instructions, MCP tools, post-process scripts, git hooks)? Be specific.

7. **Slash commands, prompts, rules — format translation patterns** — Concrete code patterns projects use to translate one logical artifact ("skill" or "workflow") into N agent formats. Specifically: templating engines, build steps, schema converters, runtime detection. Show me actual code from real installer scripts. How do they avoid drift between source and compiled artifacts?

8. **Emerging cross-agent standards (April 2026 trajectory)** — Status, adoption, and what's actually authorable: ACP (Zed/JetBrains AIR — is this still consumer-only?), Skills.sh, MCP-as-distribution channel for skills, the AGENTS.md ecosystem, OpenAI Agent SDK skills, Anthropic Agent Skills, Google Gemini Extensions. What can a practice author publish today that any conformant agent will consume? What's the realistic 6-month trajectory?

Desired output: A structured report with findings organized by question, including:
- Specific actionable patterns and implementations
- Example file layouts, manifest fragments, and install-script excerpts where available
- Repository links and file paths so I can read the source myself
- Citations with URLs for every factual claim — release notes, official docs, blog posts, GitHub commits dated 2025-Q4 to 2026-Q2 wherever possible
- An honest assessment of current limitations, gaps, and where the ecosystem is fragmented

Date context: Today is 2026-04-26. Prioritize current and recent sources. Flag any claim where you can only find dated sources, and label your confidence (high/medium/low) per question.
