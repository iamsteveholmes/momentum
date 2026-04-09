---
content_origin: agent-research
lens: B2
topic: Context Engineering Ecosystem
date: 2026-04-09
---

# Lens B2: Context Engineering Ecosystem Research

---

## 1. Implementations of Karpathy-Style Knowledge Bases

**llmwiki** (github.com/lucasastorian/llmwiki)
- Open-source implementation connecting Claude via MCP
- Claude reads sources, writes wiki pages, maintains cross-references
- Ships with llmwiki.app hosted version

**LLM Wiki v2** (gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)
- Extends original with memory lifecycle management (confidence scoring, supersession, Ebbinghaus-curve forgetting)
- Typed knowledge graph entities with structured relationships
- Hybrid BM25 + vector + graph-traversal search
- Event-driven automation hooks, auto-healing
- Treats schema document as "most important file in the system"

**Codified Context — Production Reference Implementation** (arxiv.org/html/2602.20478v1)
- 70-day study on real C# codebase — the closest thing to a validated reference implementation
- **Three-tier architecture:**
  - **Tier 1 (Hot Memory / Constitution):** ~660-line markdown file loaded into every session. Trigger tables mapping file patterns to specialist agents, code quality standards, known failure modes, architectural pattern summaries pointing to Tier 3.
  - **Tier 2 (Specialist Agents):** 19 domain-expert agent specifications (~9,300 lines total). More than half of each agent's content is domain knowledge, not behavioral instruction.
  - **Tier 3 (Cold Memory / Knowledge Base):** 34 on-demand specification documents (~16,250 lines), machine-readable. Symptom-cause-fix tables distilled from debugging sessions. Retrieved via MCP keyword search.
- **Empirical results:** 283 sessions, 108,256 lines of application code, 2,801 prompts. Infrastructure overhead: 26,200 lines (24.2% of codebase).
- Four case studies documented: cross-session consistency, prevention of repeated trial-and-error, collaborative debugging on subtle distributed systems issues.

**Critical divergence from Karpathy:** Production systems universally split knowledge into hot (always-loaded) and cold (on-demand retrieved) tiers. Karpathy's flat wiki is the right mental model for personal knowledge management but does NOT map directly to agent context engineering, where token budget pressure forces selective loading.

---

## 2. "Sleep-Time Compute" as a Pattern

**Primary paper:** "Sleep-time Compute: Beyond Inference Scaling at Test-time" (arxiv.org/html/2504.13171v1, Kevin Lin et al., Letta / UC Berkeley, April 2025)

**What preprocessing involves:** Model receives only context (no query) during sleep-time. Uses function-calling loop (`rethink_memory`, `finish_rethinking`, up to 10 iterations) to predict likely queries and produce re-represented context with intermediate deductions, structured summaries, cached chain-of-thought. At inference time, agent receives preprocessed context rather than raw input.

**Empirical results:**
- ~5x reduction in test-time compute to achieve same accuracy on mathematical reasoning tasks
- 2.5x reduction in average cost per query when 10+ related questions share the same preprocessed context
- Outperforms pass@k at equal test-time budgets on Stateful GSM-Symbolic and Stateful AIME

**Documented failure modes:**
- Performs poorly when queries are unpredictable from context — preprocessing cannot anticipate the right angle
- On SWE-bench-style software tasks with generous test-time compute budgets, standard approaches outperformed sleep-time
- High test-time budgets sometimes render preprocessing irrelevant

**The conceptual link to Karpathy:** Karpathy's Ingest/Lint operations are the human-supervised equivalent of sleep-time compute applied to a persistent knowledge base.

---

## 3. Context Engineering for Coding Agents

**Anthropic's engineering approach** (anthropic.com/engineering/effective-context-engineering-for-ai-agents):
- "Just-in-time retrieval" over pre-loading: maintain lightweight identifiers and dynamically load content at runtime via tools
- Progressive disclosure: agents incrementally discover relevant context through exploration
- System prompts should find "right altitude" — specific enough to guide, flexible enough for heuristics
- Tools should be minimal and unambiguous

**The ACE Framework** (arxiv 2510.04618, October 2025):
- Formalizes "evolving playbooks" — structured, itemized strategy collections growing incrementally
- Three-agent system: Generator produces trajectories, Reflector extracts lessons, Curator creates delta updates
- Results: +10.6% on AppWorld agent benchmark, +8.6% on financial reasoning, 82-92% reduction in adaptation latency

**Frequent Intentional Compaction (FIC) framework** (humanlayer/advanced-context-engineering-for-coding-agents):
- Split development into Research → Plan → Implement phases
- Compact deliberately at phase transitions rather than letting context accumulate
- Use subagents for discovery/grep/glob to avoid polluting main agent's working memory
- Target 40-60% context utilization
- Demonstrated on 300k LOC Rust codebase: 35k LOC feature shipped in ~7 hours

**Best practice consensus for guidelines files (April 2026):**
Include ONLY non-inferable details: custom build commands, non-standard tooling choices, project-specific coding constraints, testing requirements.
Do NOT include: architecture overviews, content duplicated from READMEs, general framework conventions the model already knows.
Structure: tech stack (exact versions), executable commands, coding conventions with code snippets for counterintuitive patterns, testing rules, permission boundaries.

---

## 4. Critique and Counter-Evidence

**Context rot problem:** Chroma "Context Rot" study (https://research.trychroma.com/context-rot) testing 18 frontier models (GPT-4.1, Claude 4, Gemini 2.5, Qwen3 families) found every model performed worse as context length increased, with performance growing "increasingly unreliable as input length grows." The specific claim of "dropping from 95% to 60% accuracy past a threshold" is [UNVERIFIED] — the study is confirmed real but those exact accuracy numbers could not be verified from available text; the study presents data primarily in charts.

**RAG vs. LLM wiki tradeoffs:** RAGFlow 2025 analysis argues dynamic, real-time context assembly outperforms static approaches for enterprise scenarios requiring current information, personalization, verified facts.

**Over 70% error attribution:** [UNVERIFIED] Multiple 2025-2026 sources cite that over 70% of errors in production LLM applications stem from incomplete, irrelevant, or poorly structured context — not insufficient model capability. No primary source could be identified for this specific statistic.

**Critique of Karpathy's pattern:** The closest empirical challenge is ETH Zurich evidence that auto-generated knowledge files hurt performance. The v2 extensions address this with quality scoring and confidence thresholds. The Ingest/Query/Lint loop must be human-supervised to produce quality-positive results, not automated.

---

## Key Design Implications

1. **Hot-cold knowledge split is mandatory.** Dense upfront injection degrades performance. Always-loaded content should be small (<150-200 lines), high-signal, containing only non-inferable facts.

2. **The "codified context" three-tier model is current state of the art.** Hot constitution → specialist agents with embedded domain knowledge → cold knowledge base. arxiv.org/html/2602.20478v1 is the reference implementation with empirical results.

3. **Karpathy's wiki pattern applies to knowledge base MAINTENANCE, not context DELIVERY.** The wiki is how you maintain the cold-storage knowledge base. The agent gets selective, retrieved slices of it, not the whole thing.

4. **Sleep-time compute** is validated for predictable query patterns. For agent guidelines, the relevant application is: pre-compile domain knowledge into structured, agent-consumable form during "offline" workflow steps.

---

## Key Sources
- https://arxiv.org/html/2602.20478v1 — Codified Context (production reference implementation)
- https://arxiv.org/html/2504.13171v1 — Sleep-time Compute paper
- https://arxiv.org/html/2510.04618v1 — ACE framework
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md
- https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2 — LLM Wiki v2
- https://research.trychroma.com/context-rot — Chroma Context Rot study (18 LLMs)
