Research Topic: CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements

I need a comprehensive analysis of which CLI coding agents (beyond Anthropic's Claude Code) could realistically replace Claude Code for agentic software engineering, specifically ones that (a) have first-class CMUX integration (native pane/tab control, not just "runs in a terminal"), (b) access LLM marketplaces like OpenRouter plus arbitrary OpenAI-compatible providers, and (c) offer comparable capabilities: sub-agents, slash commands or skills, hooks, MCP servers, tool use, and plan mode.

Research Goals: Identify the best CLI coding agents that could realistically replace Claude Code while preserving CMUX integration and multi-provider LLM flexibility. Known and explicitly excluded: Goose (Block), ForgeCode. Obvious candidates to evaluate: opencode (SST), pi (Pixel Inc / pi.new). The developer wants to know what else exists, how the candidates compare, and which is most viable as a Claude Code drop-in replacement today.

CMUX context: CMUX is a visual terminal multiplexer (https://github.com/cmux-dev/cmux or similar project name — it may also be known as "cmux" in SST/Vercel/Anthropic circles) providing terminal panes, browser surfaces, and markdown viewers that coding agents can manipulate programmatically via `cmux` CLI subcommands (new-split, send, capture-pane, browser open, etc.). "First-class CMUX support" means the agent can natively orchestrate panes — not just run inside a single pane.

Key questions to investigate:

1. Beyond opencode, pi, Goose, and ForgeCode, what other CLI coding agents exist in early 2026 that could serve as Claude Code replacements, and how deeply does each integrate with CMUX (native pane control vs. shell-wrapper vs. none)? Include emerging tools: Aider, Cline (CLI mode), Cursor CLI, Codex CLI (OpenAI's open-source agent), Zed's agentic mode, Continue CLI, Roo Code, Charm Crush, Gemini CLI's agent mode, GitHub Copilot CLI's agent mode, SWE-agent, OpenHands (ex-OpenDevin), Aichat, smol developer, plus anything else that fits the description.

2. How do opencode, pi, and any other viable candidates support LLM marketplaces — specifically OpenRouter, OpenAI-compatible endpoints (LiteLLM, Ollama, llama.cpp server, Together AI, Groq, Fireworks, Anyscale, Azure OpenAI), and arbitrary custom providers? What is the provider and model flexibility, and can routing be configured per-task or per-agent-role (e.g., cheap model for routine work, strong model for planning)?

3. How do these agents compare to Claude Code on feature parity across sub-agents (spawning specialist agents), slash commands / skills (reusable workflow invocations), hooks (pre/post-tool-use, session lifecycle), MCP servers (Model Context Protocol integration), tool use (built-in and custom tools), plan mode (read-only exploration before action), and overall ecosystem maturity (plugin marketplaces, community skills, documentation)?

Desired output: A structured report with findings organized by question, including:
- Specific actionable recommendations where available — ideally a shortlist of 2-3 agents ranked for the stated goal
- Example configuration snippets (OpenRouter wiring, provider config)
- Citations with URLs for every factual claim — official docs, GitHub repos, release notes, comparison articles
- A comparison table across agents × capabilities
- An honest assessment of current limitations and gaps — especially around CMUX integration depth, since most CLI agents "run in a terminal" but don't programmatically drive panes

Date context: Today is 2026-04-22. Prioritize current and recent sources from late 2025 and 2026.
