---
topic: "ForgeCode and agentic tooling evaluation for Momentum"
goals: "Assess ForgeCode (forgecode.dev) as an integration point, parallel track, or partial replacement for parts of Momentum's Claude Code-centric stack. Compare with peer agentic tools (Goose AI, OpenCode, Qwen Code, Kilo Code, Aider, Cline, and any others surfaced by research). Evaluate model-routing / AI-market integration (OpenRouter and popular alternatives) and local-model support. Map each candidate against Momentum's core primitives (file-authoritative rules, skills/agents, hooks, deterministic workflows) and the existing Claude Code + BMAD + CMUX stack. Identify concrete pathways: (a) integrate as specialist co-processor, (b) run Momentum-equivalent practice in parallel on the tool, (c) migrate parts/all of Momentum. Flag maturity, licensing, community-health, and lock-in risks."
profile: medium
date: 2026-04-21
sub_questions:
  - "What is ForgeCode (forgecode.dev) — architecture, core capabilities, model support, CLI/IDE integration surface, pricing, target use cases — and where does it sit relative to Claude Code?"
  - "How do ForgeCode, Goose AI (block/goose), OpenCode (sst/opencode), Qwen Code, Kilo Code, Aider, Cline, and any notable peers discovered during research compare on model flexibility, orchestration primitives, extension model (agents/skills/hooks/MCP), and overall maturity?"
  - "Which model routers and AI marketplaces are popular in these communities — OpenRouter and its alternatives (Together, Groq, Fireworks, OpenAI-compatible gateways like LiteLLM/Helicone, direct provider APIs, Ollama/Llama.cpp/local)? For each tool, how first-class is the integration, what routing/fallback/cost-control primitives exist, and what does the cost/quality tradeoff look like for routine coding tasks?"
  - "Which of these tools support Momentum's core primitives — file-authoritative rules, skills/agents as first-class citizens, hooks, and deterministic workflows — well enough that a Momentum-equivalent practice could live on them, and which would require heavy glue?"
  - "For ForgeCode and the strongest peers, describe three concrete pathways: (a) plug in as a specialist co-processor alongside Claude Code (cheap model routing, parallel review, sandboxed sub-agent); (b) run Momentum-equivalent practice in parallel on the tool (as once imagined for Cursor); (c) migrate parts or all of Momentum onto it. What does each look like in practice, and what are the tradeoffs?"
  - "What are the known limitations, ecosystem health, community size, commercial model, licensing, and upgrade cadence of ForgeCode and the top peer tools? What would adoption cost Momentum in lock-in, practice drift, or rework?"
---

# Research Scope: ForgeCode and agentic tooling evaluation for Momentum

**Date:** 2026-04-21
**Profile:** medium
**Goals:** Assess ForgeCode (forgecode.dev) as an integration point, parallel track, or partial replacement for parts of Momentum's Claude Code-centric stack. Compare with peer agentic tools (Goose AI, OpenCode, Qwen Code, Kilo Code, Aider, Cline, and any others surfaced by research). Evaluate model-routing / AI-market integration (OpenRouter and popular alternatives) and local-model support. Map each candidate against Momentum's core primitives (file-authoritative rules, skills/agents, hooks, deterministic workflows) and the existing Claude Code + BMAD + CMUX stack. Identify concrete pathways: (a) integrate as specialist co-processor, (b) run Momentum-equivalent practice in parallel on the tool, (c) migrate parts/all of Momentum. Flag maturity, licensing, community-health, and lock-in risks.

## Sub-Questions

1. What is ForgeCode (forgecode.dev) — architecture, core capabilities, model support, CLI/IDE integration surface, pricing, target use cases — and where does it sit relative to Claude Code?
2. How do ForgeCode, Goose AI (block/goose), OpenCode (sst/opencode), Qwen Code, Kilo Code, Aider, Cline, and any notable peers discovered during research compare on model flexibility, orchestration primitives, extension model (agents/skills/hooks/MCP), and overall maturity?
3. Which model routers and AI marketplaces are popular in these communities — OpenRouter and its alternatives (Together, Groq, Fireworks, OpenAI-compatible gateways like LiteLLM/Helicone, direct provider APIs, Ollama/Llama.cpp/local)? For each tool, how first-class is the integration, what routing/fallback/cost-control primitives exist, and what does the cost/quality tradeoff look like for routine coding tasks?
4. Which of these tools support Momentum's core primitives — file-authoritative rules, skills/agents as first-class citizens, hooks, and deterministic workflows — well enough that a Momentum-equivalent practice could live on them, and which would require heavy glue?
5. For ForgeCode and the strongest peers, describe three concrete pathways: (a) plug in as a specialist co-processor alongside Claude Code (cheap model routing, parallel review, sandboxed sub-agent); (b) run Momentum-equivalent practice in parallel on the tool (as once imagined for Cursor); (c) migrate parts or all of Momentum onto it. What does each look like in practice, and what are the tradeoffs?
6. What are the known limitations, ecosystem health, community size, commercial model, licensing, and upgrade cadence of ForgeCode and the top peer tools? What would adoption cost Momentum in lock-in, practice drift, or rework?
