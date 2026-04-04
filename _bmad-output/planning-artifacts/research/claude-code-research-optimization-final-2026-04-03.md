# Optimizing Claude Code for Deep Research — A Practitioner's Guide

**Date:** 2026-04-03
**Type:** Technical Research — Final Consolidated Report
**Status:** Complete
**Sources:** 7 research documents, 8-validator AVFL review, practitioner interviews

## Executive Summary

Claude Code is a terminal-native agentic system that can be configured into a powerful deep research platform. Unlike purpose-built research tools (Perplexity, Gemini Deep Research), Claude Code requires deliberate architecture — subagent orchestration, context management, tool chain configuration, and prompt engineering — to produce research-grade output. The reward for this investment is something no other tool offers: research findings that integrate directly into development artifacts within the same session.

This document synthesizes findings from six Claude Code subagent research sessions, one Gemini Deep Research report, an 8-validator adversarial quality review (AVFL), and practitioner interviews. It covers the full research stack: how to decompose research tasks across subagents, manage the 1M context window and its compaction behavior, optimize tool chains for web and codebase research, engineer effective prompts for research subagents, maintain memory across sessions, achieve genuine research depth, and manage the cost and rate-limit constraints that make multi-agent research economically viable.

The central finding is that research depth emerges not from better individual searches but from structured multi-step workflows that plan, execute, verify, and iterate. Treating the model as a generator inside a verification loop — not as an oracle — is the key to reliable research output. Multi-agent research outperforms single-agent by approximately 90% on Anthropic's own benchmarks, primarily because parallel exploration of independent threads enables broader coverage before synthesis ([Anthropic Engineering: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)).

This guide is for practitioners who use Claude Code (CLI or SDK) and want to push beyond surface-level search-and-summarize into genuine analytical research.

---

## 1. The Research Architecture

### 1.1 How Claude Code Enables Research

Claude Code operates as a local terminal agent with filesystem access, command execution, web search, web fetch, and the ability to spawn subagents. It is not a chat interface with bolted-on browsing. It reads and writes files, runs shell commands, searches the web, and delegates work to isolated child agents — all within a single session.

For research, this means Claude Code can:
- Search the web and fetch page content (WebSearch, WebFetch)
- Explore codebases using fast pattern matching (Glob, Grep, Read)
- Run arbitrary CLI tools via Bash (curl, git log, jq, etc.)
- Spawn subagents that investigate sub-questions in isolated context windows
- Write structured findings to files that persist across compaction and sessions
- Coordinate multi-agent workflows where specialized agents handle distinct research threads

The architectural advantage over conversational AI is composability. Claude Code functions as a node in Unix-style pipelines: it accepts stdin, emits structured output, and chains with traditional tools ([Claude Code Docs: Overview](https://code.claude.com/docs/en/overview)).

### 1.2 Context Window Landscape (1M GA, 200K Subagent Ceiling)

The 1M-token context window became generally available on March 13, 2026, for Opus 4.6 and Sonnet 4.6 ([Anthropic: 1M Context GA](https://claude.com/blog/1m-context-ga)). This is not beta — it is the production default for these models.

Auto-compaction triggers at approximately 83.5% of the context window, with a reserved buffer of ~33,000 tokens. The system sends the entire conversation to a summarization model, replaces the full history with a condensed summary, and re-injects CLAUDE.md files from disk ([okhlopkov.com](https://okhlopkov.com/claude-code-compaction-explained/); [claudefa.st](https://claudefa.st/blog/guide/mechanics/context-buffer-management)).

**Known bug:** Compaction can fire as early as ~76K tokens on 1M windows, leaving 92% of context unused (GitHub [#34332](https://github.com/anthropics/claude-code/issues/34332)). Until this is resolved, research agents cannot rely on having the full 1M window available.

Subagents get a fixed 200K-token context window each. This cannot be configured to use the full 1M. The 200K ceiling is adequate for focused sub-questions but constraining for deep exploration requiring many file reads or web fetches ([Claude Code Docs: Subagents](https://code.claude.com/docs/en/sub-agents)).

### 1.3 The Subagent-as-Context-Fence Pattern

The single most important architectural pattern for research is using subagents as context fences. When a subagent searches the web, reads files, or explores a codebase, all intermediate tool calls and results stay inside the subagent's 200K context window. Only the subagent's final message returns to the parent ([InfoQ](https://www.infoq.com/news/2025/08/claude-code-subagents/)).

This prevents context pollution. A parent agent that dispatches five research questions to five subagents receives five concise summaries instead of five sprawling search histories. The parent synthesizes from clean signal rather than accumulated noise.

Anthropic's own multi-agent research system uses this pattern: "The detailed search context remains isolated within sub-agents, while the lead agent focuses on synthesizing and analyzing the results" ([Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

---

## 2. Subagent Orchestration

### 2.1 Built-in Agent Types (Explore, Plan, General-purpose)

Claude Code ships with three built-in subagent types ([Claude Code Docs: Subagents](https://code.claude.com/docs/en/sub-agents)):

| Type | Model | Tools | Best For |
|------|-------|-------|----------|
| **Explore** | Haiku (fast, cheap) | Read-only (Glob, Grep, Read) | Codebase search, file discovery, pattern mapping |
| **Plan** | Inherits parent | Read-only | Architecture research, understanding structure before changes |
| **General-purpose** | Inherits parent | All tools | Complex multi-step tasks requiring web search, file creation, or reasoning |

The Explore agent accepts thoroughness levels: `quick` (targeted lookups), `medium` (balanced exploration), `very thorough` (comprehensive analysis). It runs on Haiku at substantially lower cost than Sonnet/Opus. Use it for bounded codebase questions where speed matters and write access is unnecessary.

**Caveat:** Explore agent summaries are lossy. After an Explore pass returns file pointers, have the main agent read the actual files for full detail ([Sankalp: Guide to Claude Code 2.0](https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/)).

For research tasks that need web access, file creation, or multi-step reasoning, use the general-purpose agent. Custom subagents can also be created with specific tool sets — for example, a research agent with Read, Grep, Glob, Bash, and WebSearch but no Write or Edit.

### 2.2 Work Decomposition Strategies

**Decompose by subtopic** (strongest pattern). Each agent receives a non-overlapping research question. The C compiler project demonstrated this at scale: when tasks were perfectly independent, parallelization was trivial ([Anthropic Engineering: Building a C Compiler](https://www.anthropic.com/engineering/building-c-compiler)).

**Decompose by source type.** One agent searches the web, another explores the codebase, a third reads specific documents. Useful when triangulation across source types is the goal.

**Decompose by depth level.** An Explore agent maps the landscape, then specialized agents investigate specific findings in depth.

**Anti-pattern: decomposition too fine.** "Launching 10 parallel agents for a simple feature wastes tokens and creates coordination overhead" ([claudefa.st: Sub-Agent Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)). Group related micro-tasks rather than creating one agent per atomic question.

### 2.3 Optimal Agent Count by Task Complexity

Multiple independent sources converge on a sweet spot:

| Task Complexity | Recommended Agents | Tool Calls per Agent |
|----------------|-------------------|---------------------|
| Simple fact-finding | 1 | 3-10 |
| Direct comparisons | 2-4 | 10-15 each |
| Moderate research | 3-5 | 15-20 each |
| Complex multi-faceted research | 10+ | Clearly divided responsibilities |

([Anthropic: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system); [claudefa.st: Agent Teams](https://claudefa.st/blog/guide/agents/agent-teams); [Addy Osmani: The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/))

**Diminishing returns beyond 5.** Token costs scale linearly (a 3-agent team uses roughly 3-4x the tokens of a single session). Beyond 5-6 agents, synthesis overhead exceeds parallelism gains. The human review constraint also applies: more agents than you can meaningfully review produces unverified output.

**System stability limits.** On a 2vCPU/4GB RAM VPS, 24 parallel subagents caused a 17.3x disk I/O spike requiring a hard reboot. On a Mac mini M4 Pro (24GB RAM), 20+ agents caused a complete system freeze. There is no built-in `maxParallelAgents` setting (GitHub [#15487](https://github.com/anthropics/claude-code/issues/15487)).

### 2.4 Foreground vs Background Execution

**Foreground (blocking):** The main conversation waits. Use when the result is a prerequisite for the next step.

**Background (non-blocking):** The main conversation continues. Monitor with `/tasks`. Use for parallel research threads that will be synthesized after all complete.

**Best pattern for multi-topic research:** Launch all research agents as background tasks. Background agents batch permissions upfront, unlike foreground agents which prompt interactively. For research agents that only read, permission batching is trivial ([claudefa.st: Async Workflows](https://claudefa.st/blog/guide/agents/async-workflows)).

### 2.5 Result Aggregation: Inline vs File-Based

**Inline return** (default): The parent receives the subagent's final message directly. Zero file I/O overhead, immediate availability. Downside: consumes parent context.

**File-based aggregation:** Subagents write structured output (Markdown, JSON) to specific files. Parent reads files to aggregate. Persistent, survives compaction and session interruption, handles arbitrarily large outputs.

**Recommended hybrid:** Each research subagent writes detailed findings to a file (e.g., `/tmp/research-{topic}.md`) AND returns a brief summary inline. The parent gets summaries immediately for quick synthesis; detailed files are available for deep analysis. This preserves parent context while retaining detail ([PubNub: Best Practices](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)).

---

## 3. Tool Chain for Research

### 3.1 WebSearch: Capabilities and Costs

WebSearch is a server-side tool backed by Anthropic's search infrastructure (analysis suggests Brave Search as the backend). It operates through a secondary conversation that calls the search tool with up to 8 searches, processes results, and returns ~10 links with titles, URLs, and synthesized text blocks ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)).

**Parameters:** `query` (required), `allowed_domains` and `blocked_domains` (optional filtering). The `web_search_20260209` version adds dynamic filtering with Opus 4.6 and Sonnet 4.6, where Claude can write and execute code to filter search results before they reach the context window.

**Cost:** $10 per 1,000 searches on the API. Estimated ~$145 per 1,000 WebSearch calls in Claude Code when the main conversation uses Opus, accounting for cache creation tokens and search overhead ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)).

**Effective query crafting:** WebSearch uses lexical matching. Include specific terms, year references for recency, and quoted phrases for exact matches. Domain filtering via `allowed_domains` is valuable when researching specific documentation sites.

### 3.2 WebFetch: Architecture, Limitations, and Guardrails

WebFetch runs locally using Axios from the user's machine IP address — it does not route through Anthropic servers. The pipeline: Axios fetches the page (max ~10 MB), Turndown converts HTML to Markdown, content is truncated to ~100 KB, then a secondary conversation with Haiku processes the content with a 125-character maximum for direct quotes. The result is a processed summary, not raw content ([Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-web-tools/); [Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)).

**Key limitations:**
- No JavaScript rendering (SPAs and dynamically-generated content fail)
- No authentication support (no cookies, sessions, or credentials)
- Can only fetch URLs that have appeared in the conversation context
- Cross-host redirects require manual follow-up requests
- 15-minute cache TTL per URL

**Practitioner-verified guardrails for WebFetch:**
- **Timeout:** 3-hour hangs occur because WebFetch lacks internal timeout. Implement timeout via PreToolUse hooks (e.g., 30-second limit).
- **Serialization:** Serialize fetch requests to the same domain to avoid rate limiting.
- **Volume cap:** Limit WebFetch to 2-3 calls per task.
- **Fallback:** Use Bash with `curl --max-time 30` for reliable fetches. For consistently blocked sites, route through Gemini CLI, Firecrawl MCP, or Bright Data MCP.

### 3.3 Codebase Research: Glob, Grep, Read

These are the core tools for codebase research. Use them in sequence:

| Tool | When to Use | Key Feature |
|------|-------------|-------------|
| **Glob** | Know the filename pattern, not the location | Returns results sorted by modification time |
| **Grep** | Know what is inside the file, not which file | Ripgrep-powered; supports regex, file type filtering, context lines |
| **Read** | Know the exact file and location | Supports text, images, PDFs (with page ranges), Jupyter notebooks |

**Effective pipeline:** Glob (find entry points) -> Read (examine configurations) -> Grep (explore subsystems). For error investigation: Grep (locate pattern) -> Read (examine context) -> Glob (find related files).

**Context budget awareness:** Every tool call consumes context. Start specific, then broaden. Use file type filters (`type: "ts"`) to narrow searches. Read partial files with `offset`/`limit` instead of full files. Delegate exploration to subagents to keep the main conversation clean ([Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)).

### 3.4 Bash as Research Fallback

Bash makes every CLI tool on the system immediately available. Use it for:
- Git history analysis: `git log`, `git blame`, `git show`
- API exploration: `curl -s <endpoint> | jq '.data[]'`
- Statistical analysis: `wc -l`, `sort`, `uniq -c`
- Project-specific CLIs: `gh`, `aws`, `sentry-cli`

Prefer dedicated tools (Glob, Grep, Read) over their Bash equivalents (`find`, `grep`, `cat`) — the dedicated tools provide better context handling and user experience.

### 3.5 Tool Selection Decision Framework

```
Research Task
  |
  +-- Need external/web information?
  |     +-- Need search results? --> WebSearch
  |     +-- Have a specific URL? --> WebFetch
  |     +-- URL fails or needs JS? --> Bash (curl, Playwright)
  |
  +-- Need codebase information?
  |     +-- Know the filename pattern? --> Glob
  |     +-- Know what is inside the file? --> Grep
  |     +-- Know the exact file path? --> Read
  |     +-- Need git history? --> Bash (git log, git blame)
  |
  +-- Need multi-step investigation?
  |     +-- Will consume lots of context? --> Subagent
  |     +-- Simple pipeline? --> Chain tools directly
  |
  +-- Need structured data from APIs?
        +-- One-off query? --> Bash (curl | jq)
        +-- Repeated pattern? --> MCP server
```

---

## 4. Prompt Engineering for Research Agents

### 4.1 The Briefing Pattern

Treat subagent prompts like a briefing for a smart colleague who just walked into the room. The prompt string is the only channel from parent to subagent — the subagent receives no conversation history, no prior tool results, nothing except its system prompt plus your prompt string ([Claude Code Docs: Subagents](https://code.claude.com/docs/en/sub-agents)).

Anthropic's own research system learned this through failure. Simple instructions like "research the semiconductor shortage" caused subagents to misinterpret tasks or duplicate each other's work. In one case, one subagent explored the 2021 automotive chip crisis while two others duplicated work investigating current supply chains ([Anthropic: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)).

**What a good briefing includes:**

| Component | Purpose | Example |
|-----------|---------|---------|
| Objective | What specific question to answer | "Compare pino, winston, and console-based logging on cold start impact" |
| Output format | What the result should look like | "Return a comparison table and a recommendation with rationale" |
| Tool/source guidance | Which tools to prefer | "Use WebSearch for benchmarks, Grep for usage patterns in our codebase" |
| Task boundaries | What is in scope and out of scope | "We have already ruled out bunyan (unmaintained)" |
| Prior context | What has been tried or discovered | "Initial search found pino has the lowest cold start overhead" |

### 4.2 Context Provision: The Minimal-Sufficiency Principle

Anthropic frames this as finding "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." Every token competes for model attention, and as context grows, recall accuracy decreases ([Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**Practical guidelines:**
1. Include what you have already tried or ruled out — prevents the single most common failure mode (duplicated work).
2. Include file paths, error messages, or architectural decisions — concrete, low-token, high-signal items.
3. Do not dump entire conversation history — let the subagent do its own exploration with a clean 200K context.
4. Use progressive disclosure — maintain lightweight identifiers (file paths, stored queries, web links) and dynamically load data at runtime.
5. Describe the "why" behind the research — a subagent that understands motivation makes better judgment calls about relevance.

### 4.3 Output Format Specification

Use structured guidance over narrative instruction. Anthropic recommends "explicit sections and clear delineation (XML tags, Markdown headers)" and providing "structured examples showing expected format rather than describing it narratively" ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

| Scenario | Recommendation |
|----------|---------------|
| Findings that feed into further reasoning | Return inline to parent |
| Artifacts with independent value (specs, reports) | Write to a file |
| Structured data for comparison | Specify table/JSON format explicitly |
| Exploratory findings | Narrative inline with key takeaways highlighted |

### 4.4 Task Scoping: Narrow vs Broad

Give the subagent a clear objective and explicit boundaries, but leave the method flexible. Specify *what* to find and *what to exclude*, but let the agent decide *how* to search.

**Over-specification risk:** The agent follows instructions too literally, missing relevant adjacent information. Anthropic warns against "hardcoding complex, brittle logic in prompts" because this "creates fragility and increases maintenance complexity" ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**Under-specification risk:** The agent goes off track, duplicates work, or produces generic results. This was Anthropic's primary finding — vague instructions caused subagents to "misinterpret the task or perform the exact same searches as other agents."

### 4.5 Common Anti-Patterns

**Terse command-style prompts.** "Research X" produces shallow results. No boundaries, no exclusions, no output format, no prior context.

**Over-spawning.** Opus has a known tendency to delegate when a direct approach would be faster. Anthropic's research system found early versions creating "50 subagents for simple queries" ([Anthropic: Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system)).

**Context gatekeeping.** Creating specialized subagents can hide context from the main agent, which can no longer reason holistically ([ksred: Claude Code Agents](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)).

**Tool bloat.** Designing ambiguous tool sets where "if humans can't definitively choose which tool applies, agents can't either" ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**Lazy delegation.** The coordinator must synthesize findings before delegating further work. "Based on your findings, do X" without reviewing those findings creates a delegation chain where no agent takes responsibility for quality.

**Endless searching.** Without explicit effort bounds, agents "scour the web endlessly for nonexistent sources." Embed scaling rules that cap tool calls based on task complexity.

---

## 5. Context and Memory Management

### 5.1 Auto-Compaction: How It Works

When context usage reaches ~83.5% of the total window, Claude Code sends the entire conversation to a summarization model. The summary replaces the full history. The model preserves architectural decisions, unresolved issues, and key findings while discarding redundant tool outputs and verbose intermediate messages ([okhlopkov.com](https://okhlopkov.com/claude-code-compaction-explained/); [MindStudio](https://www.mindstudio.ai/blog/context-window-claude-code-manage-consistent-results)).

**What survives compaction:**
- General continuity — key patterns, file states, major decisions
- CLAUDE.md files — re-read from disk after every compaction

**What gets lost:**
- Specific variable names, exact error codes, nuanced design decisions
- File paths, source URLs, edge-case constraints
- The transition is invisible to the user

**Customizing compaction:** Add a "Compact Instructions" section to CLAUDE.md specifying what to preserve (e.g., "When compacting, always preserve the full list of source URLs and research findings"). Run `/compact` manually with a focus topic at ~60% utilization to compact proactively before quality degrades ([GitHub #14160](https://github.com/anthropics/claude-code/issues/14160)).

**Tool result clearing:** A separate, lighter mechanism. The API's `clear_tool_uses_20250919` strategy clears old tool results when context grows beyond a threshold. Older tool results (file contents, search results) are removed in chronological order. This frees context for new searches without triggering full compaction ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

### 5.2 The Three-Layer Memory Architecture

| Layer | What It Is | Who Writes It | Survives Compaction? | Best For |
|-------|-----------|---------------|---------------------|----------|
| **CLAUDE.md** | Static configuration and hard rules | You (the user) | Yes — re-read from disk | Project conventions, build commands, research methodology instructions, compaction preservation instructions |
| **Auto-memory (MEMORY.md)** | Concise static facts | Claude (automatically) | Yes — re-read from disk | Path locations, brief rules, discovered patterns. Truncated after ~200 lines |
| **learnings.md** | Dynamic project memory | Claude (at your instruction) | Only if re-read at session start | Failed approaches, codebase quirks, evolved understanding, accumulated knowledge |

**Critical distinction:** CLAUDE.md is for invariant instructions, not accumulated findings. Research findings should go into dedicated files in the project tree, not into CLAUDE.md or auto-memory.

**Best practice:** CLAUDE.md instructs the agent to read learnings.md at session start. The agent appends new observations before terminating. This creates a persistent knowledge base that grows across sessions.

### 5.3 The Handoff Protocol (learnings.md Pattern)

Before a context window fills, the agent generates a comprehensive handoff document: current findings, active hypotheses, retrieval state, and next steps. The operator terminates the session and starts a fresh one that reads the handoff document. This restores high-fidelity state awareness with a pristine context window and zero accumulated token debt.

**Recommended multi-session research pattern:**

1. **Session 1 (Exploration):** Search broadly, write raw findings to a research file incrementally.
2. **Compact proactively** at ~60% context utilization with a topic-focused prompt.
3. **Session 2 (Synthesis):** Start fresh, read the research file, synthesize and structure.
4. **Session 3 (Validation):** Start fresh, read the synthesis, verify claims, fill gaps.

Each session starts with a clean context and loads only what it needs from files. This avoids the degradation from a single session compacting repeatedly.

### 5.4 Task Tools for State Tracking

TaskCreate, TaskUpdate, and TaskList provide structural state that prevents context drift. Task state is maintained by the harness, not by conversation history. Even after aggressive compaction, the task list accurately reflects progress.

**Research pattern:**
1. Create tasks for each research question at session start.
2. Mark tasks `in_progress` as work begins.
3. Mark tasks `completed` as findings are written to the output file.
4. After compaction, the task list shows what is done and what remains.

Multiple Claude sessions can share a task list via environment variable configuration, enabling parallel research workstreams ([VentureBeat](https://venturebeat.com/orchestration/claude-codes-tasks-update-lets-agents-work-longer-and-coordinate-across)).

### 5.5 Session Structure for Long Research

**Continue an existing session when:**
- Same research topic, context has not compacted multiple times, accumulated context is still useful.

**Start a new session when:**
- Context has compacted multiple times and quality has degraded.
- Pivoting to a substantially different research question.
- You want a clean context for synthesis (importing from files, not degraded conversation history).

Use `claude --continue` to resume the most recent session. Use `claude --resume` to pick from recent sessions. Use `/clear` to start fresh within the same terminal session.

---

## 6. Research Depth Strategies

### 6.1 Progressive Refinement (Breadth-Then-Depth)

Effective deep research follows a progressive narrowing pattern. Anthropic's multi-agent system documents this explicitly: subagents employ "short, broad queries, evaluate what's available, then progressively narrow focus" using interleaved thinking after tool results to "evaluate quality, identify gaps, and refine their next query" ([Anthropic: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)).

**Practical steps:**
1. **Broad mapping** (3-5 general queries): Survey the landscape, identify key domains and sources.
2. **Targeted verification** (narrow subagents): Investigate specific claims, download full-text documents, extract verbatim evidence.
3. **Exhaustive analysis** (iterative loops): Continue exploring tighter conceptual bounds until token budget, time, or saturation is reached.

The advantage is fault tolerance. If a hard timeout occurs, the system falls back to the fully completed findings of the previous depth level — a weaker but structurally correct answer rather than half-searched garbage.

**Avoiding shallow loops:** The primary risk is the "Anchor Effect" — fixation on initial results that constrains subsequent queries. Research on hallucination in deep research agents found that over 57% of source errors occur early, with cascading downstream consequences ([arxiv: Why Your Deep Research Agent Fails?](https://arxiv.org/html/2601.22984v1)). Countermeasures: deliberate reframing with different terminology after initial results, breadth-first before depth-first, and explicit gap checking after each retrieval cycle.

### 6.2 Cross-Referencing and Triangulation

**Citation overlap analysis:** Identify sources cited by multiple independent searches (consensus) versus sources found by only one path (unique). Consensus sources indicate widely-recognized information; unique sources may contain novel insights or hallucinations.

**Multi-engine execution:** Deliberately use different search backends (web search, documentation sites, forum discussions, codebase analysis) for the same question. Each source type has different biases. Anthropic's testing found human testers "identified subtle biases (SEO-optimized sites over academic sources)" requiring explicit prompt corrections.

**Claim-level verification:** Extract individual claims from synthesized results and verify each against its source. About one-third of statements from AI search tools are not supported by their cited sources; for some models, the figure is 47% ([TechXplore](https://techxplore.com/news/2025-09-ai-tools-unreliable-overconfident-sided.html)).

### 6.3 Gap Analysis Techniques

**Silent omissions** — topics the research plan should cover but no source addresses.
**Shallow coverage** — topics mentioned but not explained in sufficient depth.
**Temporal gaps** — information that was accurate at publication but may be outdated.
**Perspective gaps** — viewpoints from specific stakeholder groups that are absent.

**Discovering unknown unknowns:**
- Negative space analysis: "What would I expect to find that I have not found?"
- Stakeholder rotation: Examine from each perspective (user, developer, operator, adversary).
- Analogical probing: What do related domains handle similarly?

**Saturation signal:** When two consecutive search iterations yield no new insights, the research is likely complete enough for its intended purpose ([PMC: Saturation in Qualitative Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC5993836/)).

### 6.4 Source Quality Assessment

| Tier | Source Type | Strengths | Risks |
|------|-----------|-----------|-------|
| 1 | Official documentation, API references | Authoritative, maintained | May lag behind implementation |
| 2 | Peer-reviewed papers, vendor engineering blogs | Rigorous, detailed | May be theoretical or vendor-biased |
| 3 | Conference talks, reputable tech blogs | Practical, current | Variable rigor |
| 4 | Forum discussions (GitHub Issues, Stack Overflow) | Real-world edge cases | Anecdotal, may be outdated |
| 5 | Tutorial posts, Medium articles | Accessible | Often derivative, SEO-optimized |

**Outdated information signals:** Version numbers that do not match current releases, API endpoints returning 404 or deprecation warnings, dates more than 12-18 months old for rapidly evolving technologies, features described as "upcoming" without confirmation of release.

### 6.5 Verification and Validation

The most effective pattern: stop treating the model as an oracle and start treating it as a generator operating inside a verification loop ([Morphik: Eliminate Hallucinations](https://www.morphik.ai/blog/eliminate-hallucinations-guide)).

**Practical verification strategies:**
- **Source tracing:** For every claim, verify the cited source actually says what is attributed.
- **Code testing:** Execute code examples rather than trusting them.
- **Version checking:** Verify APIs, features, or behaviors exist in the version being used.
- **Recency validation:** Check publication dates against technology evolution speed.
- **Cross-source confirmation:** Require at least two independent sources for critical claims.

**Critical finding:** Existing evaluations suffer from incomplete hallucination detection. Misleading intermediate hallucinations occur exclusively within intermediate steps and remain invisible to end-to-end checks. Verifying only the final output is insufficient ([arxiv: PIES Framework](https://arxiv.org/html/2601.22984v1)).

---

## 7. Rate Limits and Cost Management

### 7.1 The Sustain Limit (72-Hour Freeze Risk)

Beyond the visible per-message rate limits, there is an undocumented per-account restriction tracking compute over a rolling 7-day period. Practitioners call it the "Sustain Limit" or "Weighted Compute" leash. Hitting 5-hour burst caps repeatedly triggers a 72-hour account freeze — even if the UI shows "messages remaining." This is separate from the standard rate limit and is not documented in official rate limit pages.

If multiple subagents hit API rate limits simultaneously, the entire session can fail, scrapping progress without saving intermediate work. This makes file-based result persistence (Section 2.5) not just a convenience but a defensive necessity.

Anthropic acknowledged on Reddit that "people are hitting usage limits in Claude Code way faster than expected" and said a fix is their top priority ([The New Stack](https://thenewstack.io/claude-code-usage-limits/)).

### 7.2 Cost Economics of Multi-Agent Research

Each subagent maintains its own separate context window. Costs scale linearly with agent count:
- A 3-agent team uses roughly 3-4x the tokens of a single session doing the same work sequentially.
- Multi-agent workflows use 4-7x more tokens than single-agent sessions.
- A 15-agent multi-hour session can cost tens to hundreds of dollars on API.

Practitioners report the Max plan ($100-200/mo) caps financial liability but trades cost for Sustain Limit risk. Running sustained multi-agent research workflows on subscription plans is the fastest way to trigger the 72-hour freeze.

### 7.3 Model Routing for Cost Optimization

Route lighter models to subagents while maintaining the main session on Opus:
- **Explore agents** already run on Haiku (cheapest).
- **Research subagents** that primarily search and read can run on Sonnet.
- **Synthesis/aggregation** should stay on Opus for reasoning quality.

⚠️ Community observation: The environment variable `CLAUDE_CODE_SUBAGENT_MODEL` is reported by community members for routing subagent models, but this is not officially documented by Anthropic.

### 7.4 Monitoring Tools (/cost, toktrack, AI gateways)

| Tool | Scope | What It Shows |
|------|-------|---------------|
| `/cost` | Current session | Session cost summary |
| `toktrack` | Local monitoring | Real-time cost breakdowns |
| `npx straude` | Local monitoring | Real-time cost breakdowns |
| OpenRouter, LiteLLM | Enterprise gateways | Per-request logging, budget enforcement, rate limit management |

### 7.5 Strategies for Staying Productive Under Limits

1. **Write intermediate results to files.** If a session crashes due to rate limits, work is not lost.
2. **Stagger subagent launches.** Avoid firing all agents simultaneously.
3. **Use Explore (Haiku) agents** for codebase investigation — they consume far fewer tokens.
4. **Compact proactively** at ~60% to extend session life.
5. **Batch and push.** Do not push after every commit. Batch commits and push at logical milestones.
6. **Monitor with `/cost`** and set personal per-session budgets.
7. **For enterprise use:** Route through AI gateways (OpenRouter, LiteLLM) for per-request logging and hard budget enforcement.

---

## 8. Comparative Landscape

### 8.1 Claude Code vs Gemini Deep Research

| Dimension | Claude Code | Gemini Deep Research |
|-----------|------------|---------------------|
| **Architecture** | Terminal-native agent with filesystem access | Cloud-integrated autonomous research pipeline |
| **Strength** | Deep reasoning over sources, codebase integration, structured artifact production | Broad web coverage, multimodal analysis, real-time information, mathematical reasoning |
| **Source coverage** | Higher source count in benchmarks (261 sources in one test) | Fewer sources (62 in same test) but stronger data accuracy |
| **Speed** | Faster source throughput | Longer processing time (15+ min vs 6+ min) |
| **Research output** | Integrates directly into development workflows | Standalone research reports |
| **Best for** | Research requiring cross-referencing, codebase context, or artifact production | Broad web research, current events, scientific/mathematical reasoning |

On the DR-2T benchmark, both emerged as leading solutions. Claude led in indexed sources; Gemini excelled in data accuracy ([AIMultiple: AI Deep Research Comparison](https://aimultiple.com/ai-deep-research)).

### 8.2 Claude Code vs Perplexity

Perplexity and Claude Code solve fundamentally different problems.

| Dimension | Claude Code | Perplexity |
|-----------|------------|------------|
| **Type** | Agentic development environment extended for research | Research-first retrieval tool |
| **Citation** | Depends on configuration and workflow | Native inline citations on every answer |
| **Speed** | Multi-step sustained analysis | Ultra-fast lookups and concise summaries |
| **Real-time data** | Requires web search tool configuration | Native advantage for current events |
| **Research style** | Synthesis and reasoning across many steps | Quick factual retrieval |

On the DR-50 benchmark, Perplexity Sonar led for factual lookup tasks (34% accuracy). On agent-style research requiring synthesis and reasoning, Claude Code tied for the top position at 97% accuracy ([AIMultiple](https://aimultiple.com/ai-deep-research)).

### 8.3 When to Use Which Tool

| Research Need | Best Tool |
|---------------|-----------|
| Quick fact-checking, real-time data | Perplexity |
| Broad web research, current events, multimodal analysis | Gemini Deep Research |
| Deep reasoning over collected sources | Claude Code |
| Research integrated with codebase exploration | Claude Code |
| Research producing development artifacts (specs, configs, code) | Claude Code |
| Mathematical or scientific reasoning | Gemini |
| Citation-heavy academic research | Perplexity or dedicated academic tools |

---

## 9. Practical Patterns and Recipes

### 9.1 The Parallel Research Pattern (used in this study)

This study itself was produced using this pattern:

1. **Decompose** the research question into 6 non-overlapping subtopics.
2. **Spawn 6 subagents** in parallel, each investigating one subtopic with WebSearch-enabled general-purpose configuration.
3. **Each subagent writes** detailed findings to a dedicated file AND returns a summary inline.
4. **A separate Gemini Deep Research** session provides an external perspective on the same topic.
5. **AVFL quality gate** (8 parallel validators across 4 lenses) reviews all 7 documents adversarially.
6. **A consolidation agent** merges validated findings into this final report.

Total source documents processed: 7 research reports, 1 AVFL consolidation report, practitioner interview data.

### 9.2 The AVFL Quality Gate Pattern

After research is complete, run an adversarial validation pass before publishing. The pattern:

1. **Define lenses** (Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness).
2. **Spawn parallel reviewers** — one Enumerator (finds issues) and one Adversary (challenges the Enumerator's findings) per lens.
3. **Consolidate** findings with deduplication and severity scoring.
4. **Fix** identified issues, prioritizing critical and high severity.
5. **Re-validate** to confirm fixes landed.

This study's AVFL pass identified 67 deduplicated findings across the raw research corpus, including 4 critical factual errors. The correction layer in this document reflects those findings.

### 9.3 The Handoff-Loop Pattern for Multi-Session Research

For research spanning multiple sessions:

1. **End each session** by writing a handoff file: current findings, open questions, next steps.
2. **Start each new session** by reading the handoff file and the accumulated research output.
3. **Append** new findings to the running research file incrementally.
4. **Update** the task list to reflect completed and remaining questions.

This pattern works because each session starts with a clean context window and loads only what it needs. No information degrades through repeated compaction.

### 9.4 The Meta-Agent Factory Pattern

**Hard constraint:** Subagents cannot spawn subagents natively.

**Workaround 1 — Central Manager:** A single orchestrator creates and coordinates agents sequentially. Each round, the orchestrator reads the previous agent's output, decides what to investigate next, and spawns a new agent with refined instructions.

**Workaround 2 — Bash Child Spawning:** A subagent uses Bash to invoke `claude --agent`, spawning a CLI child process. The child gets NO parent context — only the prompt string plus CLAUDE.md/skills/MCP. The parent must write handoff files to the filesystem for the child to read.

**Warning:** The Bash child spawning approach can cause OOM crashes and is difficult to manage. Use the Central Manager pattern unless you specifically need recursive depth.

---

## 10. Known Limitations and Open Questions

### Hard Constraints
- **Subagents cannot spawn subagents.** No recursive delegation without the Bash workaround.
- **Subagent context window is fixed at 200K.** Cannot use the full 1M.
- **No `maxParallelAgents` setting.** Unbounded spawning is a system stability risk.
- **No structured failure metadata.** The orchestrator cannot distinguish successful completion from mid-execution crash (GitHub [#25818](https://github.com/anthropics/claude-code/issues/25818)).
- **Agent Teams are experimental.** Require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Resumption does not restore teammates.
- **WebFetch cannot render JavaScript.** SPAs and dynamically-generated content fail entirely.
- **WebFetch has no internal timeout.** Must be implemented via hooks.

### Known Bugs
- **Compaction fires too early on 1M windows** — as low as 76K tokens (GitHub [#34332](https://github.com/anthropics/claude-code/issues/34332)).
- **WebSearch rate limit errors** occur more frequently on subscription plans than with direct API keys (GitHub [#27074](https://github.com/anthropics/claude-code/issues/27074)).
- **Auto-delegation is unreliable.** Claude frequently handles tasks in the main session rather than delegating to defined agents, even when the agent description matches ([ksred](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)).

### Open Questions
1. Does research quality degrade with agent count? More agents produce more findings, but does synthesis quality drop when the parent integrates 8+ reports?
2. What is the optimal balance between agent count and agent depth (3 thorough agents at 20 turns each, or 6 quick agents at 8 turns each)?
3. When does the cost of additional verification exceed the value of increased confidence?
4. How should research depth scale with the stakes of the decision being informed?
5. How can agentic researchers detect their own blind spots in real time?

### Gaps in Available Evidence
- No controlled studies comparing decomposition strategies for research quality.
- No rigorous cost-per-research-task analysis across tools.
- No independent replication of Anthropic's "90.2% improvement" benchmark.
- Token cost data is approximate — practitioner estimates, not controlled measurements.
- Long-term multi-session research patterns are underexplored in the literature.

---

## Sources

### Official Anthropic Documentation
- [Claude Code Docs: Subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code Docs: Best Practices](https://code.claude.com/docs/en/best-practices)
- [Claude Code Docs: Overview](https://code.claude.com/docs/en/overview)
- [Claude Code Docs: Memory](https://code.claude.com/docs/en/memory)
- [Claude Code Docs: Common Workflows](https://code.claude.com/docs/en/common-workflows)
- [Claude Code Docs: Checkpointing](https://code.claude.com/docs/en/checkpointing)
- [Claude Code Docs: Tools Reference](https://code.claude.com/docs/en/tools-reference)
- [Anthropic: 1M Context Window GA](https://claude.com/blog/1m-context-ga)
- [Anthropic: Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [Anthropic API: Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
- [Anthropic API: Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)
- [Anthropic API: Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Anthropic API: Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Anthropic: Context Engineering Tools Cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

### Anthropic Engineering Blog
- [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Building a C Compiler with a Team of Parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)

### GitHub Issues (Verified)
- [#34332: Compaction fires early on 1M windows](https://github.com/anthropics/claude-code/issues/34332)
- [#15487: maxParallelAgents feature request / system stability](https://github.com/anthropics/claude-code/issues/15487)
- [#25818: Orchestrator lacks diagnostic context on subagent failure](https://github.com/anthropics/claude-code/issues/25818)
- [#27074: WebSearch rate limit bug](https://github.com/anthropics/claude-code/issues/27074)
- [#11650: WebFetch hanging](https://github.com/anthropics/claude-code/issues/11650)
- [#8331: WebFetch domain blocking](https://github.com/anthropics/claude-code/issues/8331)
- [#14160: Custom compaction instructions](https://github.com/anthropics/claude-code/issues/14160)
- [#20304: Isolated subagent context feature request](https://github.com/anthropics/claude-code/issues/20304)

### Community Guides and Practitioner Reports
- [Addy Osmani: The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)
- [claudefa.st: Sub-Agent Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)
- [claudefa.st: Agent Teams Guide](https://claudefa.st/blog/guide/agents/agent-teams)
- [claudefa.st: Async Workflows](https://claudefa.st/blog/guide/agents/async-workflows)
- [claudefa.st: Context Buffer Management](https://claudefa.st/blog/guide/mechanics/context-buffer-management)
- [ksred: Claude Code Agents & Subagents](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)
- [PubNub: Best Practices for Claude Code Sub-Agents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [Sankalp: Guide to Claude Code 2.0](https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/)
- [Boris Tane: How I Use Claude Code](https://boristane.com/blog/how-i-use-claude-code/)
- [Paddo: Three Ways to Build Deep Research with Claude](https://paddo.dev/blog/three-ways-deep-research-claude/)
- [builder.io: How to Write a Good CLAUDE.md](https://www.builder.io/blog/claude-md-guide)
- [okhlopkov.com: Claude Code Compaction Explained](https://okhlopkov.com/claude-code-compaction-explained/)
- [Steve Kinney: Claude Code Compaction](https://stevekinney.com/courses/ai-development/claude-code-compaction)
- [Mikhail Shilkov: Inside Claude Code's Web Tools](https://mikhail.io/2025/10/claude-code-web-tools/)
- [Quercle: How Claude Code Web Tools Work](https://quercle.dev/blog/claude-code-web-tools)
- [Morphik: Eliminate Hallucinations Guide](https://www.morphik.ai/blog/eliminate-hallucinations-guide)

### Research and Benchmarks
- [arxiv: Why Your Deep Research Agent Fails? (PIES Framework)](https://arxiv.org/html/2601.22984v1)
- [Perplexity Research: DRACO Benchmark](https://research.perplexity.ai/articles/evaluating-deep-research-performance-in-the-wild-with-the-draco-benchmark)
- [ByteBytego: How OpenAI, Gemini, and Claude Use Agents to Power Deep Research](https://blog.bytebytego.com/p/how-openai-gemini-and-claude-use)
- [AIMultiple: AI Deep Research Comparison](https://aimultiple.com/ai-deep-research)
- [TechXplore: AI Tools Often Unreliable](https://techxplore.com/news/2025-09-ai-tools-unreliable-overconfident-sided.html)
- [PMC: Saturation in Qualitative Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC5993836/)
- [NCBI: Framework for Determining Research Gaps](https://www.ncbi.nlm.nih.gov/books/NBK126702/)
- [JMIR: Deep Research Agents in Medical Research](https://www.jmir.org/2026/1/e88195)

### Industry Coverage
- [The New Stack: Claude Code Usage Limits](https://thenewstack.io/claude-code-usage-limits/)
- [VentureBeat: Claude Code Tasks Update](https://venturebeat.com/orchestration/claude-codes-tasks-update-lets-agents-work-longer-and-coordinate-across)
- [InfoQ: Claude Code Subagents](https://www.infoq.com/news/2025/08/claude-code-subagents/)
