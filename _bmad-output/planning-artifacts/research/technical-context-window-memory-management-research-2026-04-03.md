# Context Window and Memory Management for Research in Claude Code

**Date:** 2026-04-03
**Type:** Technical Research
**Status:** Complete

---

## 1. Context Compression Behavior

### How Auto-Compaction Works

Claude Code monitors context utilization continuously throughout a session. When usage reaches approximately 83.5% of the total context window, auto-compaction triggers automatically. The system takes the entire conversation history, sends it to a separate model call with a summarization prompt, and replaces the full history with a condensed summary. The model preserves architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs and verbose intermediate messages ([okhlopkov.com](https://okhlopkov.com/claude-code-compaction-explained/); [MindStudio](https://www.mindstudio.ai/blog/context-window-claude-code-manage-consistent-results)).

Claude Code reserves a buffer of approximately 33,000 tokens (16.5% of the window). With the 1M context window available on Opus 4.6 and Sonnet 4.6 (GA since March 13, 2026), this gives roughly 5x the usable space before auto-compaction triggers compared to smaller windows ([claudefa.st](https://claudefa.st/blog/guide/mechanics/context-buffer-management); [Anthropic](https://claude.com/blog/1m-context-ga)).

However, there is a known issue: some users report compaction firing as early as ~76K tokens even with the 1M window enabled, leaving 92% of the context unused. This has been filed as a bug ([GitHub #34332](https://github.com/anthropics/claude-code/issues/34332)). In earlier versions (late 2025), compaction sometimes triggered at 64-75% utilization to avoid failed compactions at the boundary ([Morph](https://www.morphllm.com/claude-code-auto-compact)).

### What Gets Preserved vs. Lost

Auto-compaction is lossy. Summaries preserve general continuity -- key code patterns, file states, and major decisions -- but lose detail. Specific variable names, nuanced design decisions, exact error codes, file paths, and edge-case constraints often do not survive compression. The agent begins working from a "memory" of past interactions rather than the full transcript, and this transition is invisible to the user ([Morph](https://www.morphllm.com/claude-code-auto-compact); [CometAPI](https://www.cometapi.com/what-is-auto-compact-in-claude-code/)).

Critically, **CLAUDE.md files are re-read from disk after every compaction** and re-injected into the session. This makes CLAUDE.md the only mechanism whose contents reliably survive compaction intact. Instructions given conversationally can and do get lost ([Steve Kinney](https://stevekinney.com/courses/ai-development/claude-code-compaction); [Morph](https://www.morphllm.com/claude-code-auto-compact)).

### Impact on Research Sessions

For long research sessions, compaction creates a specific failure mode: early findings, source URLs, nuanced distinctions, and methodological decisions degrade or vanish after compaction. The agent may repeat searches it already performed, lose track of which sources were already evaluated, or synthesize findings from a lossy summary rather than original data. This makes file-based persistence essential for research workflows.

### Customizing Compaction

You can add a "Compact Instructions" section to CLAUDE.md specifying what should be preserved during any compaction. For example: "When compacting, always preserve the full list of modified files and any test commands." You can also run `/compact` manually with a focus topic to compact proactively at ~60% utilization, before quality degradation occurs ([GitHub #14160](https://github.com/anthropics/claude-code/issues/14160); [MindStudio](https://www.mindstudio.ai/blog/claude-code-compact-command-context-management)).

---

## 2. File-Based Persistence Strategies

### When to Write Findings to Files vs. Return Inline

Anthropic's own guidance on context engineering favors a "just in time" approach: maintain lightweight identifiers (file paths, stored queries, web links) and dynamically load data at runtime rather than keeping everything in active context. For research specifically, this means writing findings to files and referencing them, rather than accumulating all results inline in the conversation ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**Write to files when:**
- Findings will be needed across compaction boundaries (anything accumulated over many turns)
- Results are large (search results, code analysis, data tables)
- Information must survive session boundaries or be used by other sessions/agents
- The research involves multiple phases where later phases reference earlier findings

**Keep inline when:**
- The finding is immediately actionable and won't be needed later
- The result is small and will be consumed in the next 2-3 turns
- You're in an early exploratory phase where most findings will be discarded

### Structuring File Output for Research

The recommended pattern is incremental structured output: write findings to a file as they accumulate, organized by topic or question, with source URLs inline. This serves dual purposes -- it persists findings against compaction loss, and it creates a deliverable artifact.

For multi-step research, a common pattern is maintaining a running research document that gets appended to as new findings arrive, rather than waiting to write everything at the end. This guards against session crashes or compaction-induced amnesia mid-research ([arxiv.org](https://arxiv.org/html/2508.08322v1)).

Anthropic's multi-agent research system demonstrates the pattern at scale: sub-agents perform focused searches with isolated context, write their results to structured output, and a lead agent synthesizes. The detailed search context stays isolated within sub-agents while the lead agent works only with synthesized results ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

---

## 3. Memory System

### Three Layers of Memory

Claude Code provides three distinct persistence mechanisms:

**1. CLAUDE.md files** -- Instructions you write for Claude. Loaded at session start and after every compaction. The most reliable persistence layer. Best for: project conventions, build commands, code style rules, architectural constraints, and any instruction that must be enforced throughout a session. Target under 200 lines per file to maintain adherence ([Claude Code Docs](https://code.claude.com/docs/en/memory); [builder.io](https://www.builder.io/blog/claude-md-guide)).

**2. Auto Memory** -- Notes Claude writes for itself. On by default. Claude records learnings, patterns, debugging insights, architecture notes, and workflow habits as it works. These accumulate in `~/.claude/` and project `.claude/` directories. Unlike CLAUDE.md, you don't write these -- Claude populates them based on corrections and discoveries during sessions ([Claude Code Docs](https://code.claude.com/docs/en/memory); [crunchtools.com](https://crunchtools.com/how-to-give-claude-code-persistent-memory/)).

**3. Session Memory** -- Automatic background system that watches conversations, extracts important parts, and saves structured summaries to disk. Each summary includes session title, current status, key results, and work log. Runs without user input ([claudefa.st](https://claudefa.st/blog/guide/mechanics/session-memory)).

### Leveraging Memory for Research

For research workflows, the key insight is that **CLAUDE.md is for invariant instructions, not accumulated findings**. Research findings should go into dedicated files in the project tree, not into CLAUDE.md or auto-memory. However, auto-memory can capture meta-learnings about research process: which search strategies worked, which sources were authoritative, which topics require follow-up.

An internal Anthropic evaluation found that combining the memory tool with context editing improved agent performance by 39% over baseline. In a 100-turn web search evaluation, context editing enabled agents to complete workflows that would otherwise fail due to context exhaustion, while reducing token consumption by 84% ([Anthropic Platform](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)).

### What to Save Where

| Finding Type | Where to Save |
|---|---|
| Project conventions, build commands | CLAUDE.md |
| Research findings, data, citations | Dedicated research file in project tree |
| Process learnings ("this search strategy works") | Auto-memory (via user corrections) |
| Session progress, what's done/remaining | Task tools or research file |
| Cross-session handoff state | CLAUDE.md or dedicated state file |

---

## 4. Session Structure for Long Research

### When to Continue vs. Start New

Use `claude --continue` to resume the most recent session in the current directory. Use `claude --resume` to pick from recent sessions or resume by name. Use `/clear` to start fresh within the same terminal session ([Claude Code Docs](https://code.claude.com/docs/en/common-workflows); [Steve Kinney](https://stevekinney.com/courses/ai-development/claude-code-session-management)).

**Continue an existing session when:**
- You're still working on the same research topic
- Context has not yet compacted (or compacted only once)
- The accumulated context is still useful, not just noise

**Start a new session when:**
- The previous session's context has compacted multiple times and quality has degraded
- You're pivoting to a substantially different research question
- You want a clean context for synthesis (importing findings from files rather than degraded conversation history)

### Checkpointing Strategies

Claude Code's checkpointing system automatically captures file state before each edit via Write, Edit, and NotebookEdit tools. Checkpoints persist across sessions and can be accessed via `/rewind`. However, checkpoints track file state, not conversation state -- they are a safety net for code changes, not a research progress mechanism ([Claude Code Docs](https://code.claude.com/docs/en/checkpointing); [skywork.ai](https://skywork.ai/skypage/en/claude-code-checkpoints-ai-coding/1976917740735229952)).

For research checkpointing, the effective strategy is **incremental file writes**: after each major finding or completed sub-question, write results to the research output file. This creates natural checkpoints that survive compaction, session crashes, and session transitions.

### Recommended Multi-Session Research Pattern

1. **Session 1 (Exploration):** Search broadly, write raw findings to a research file incrementally
2. **Compact proactively** at ~60% context utilization with a topic-focused prompt
3. **Session 2 (Synthesis):** Start fresh, read the research file, synthesize and structure
4. **Session 3 (Validation):** Start fresh, read the synthesis, verify claims, fill gaps

Each session starts with a clean context and loads only what it needs from files. This avoids the degradation that comes from a single session compacting repeatedly over hours of research.

---

## 5. Subagent Context Isolation

### Architecture

Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When the main agent spawns a subagent via the Task/Agent tool, a new `sub_messages` list is created initialized only with the task prompt. All tool calls executed by the subagent are appended to this isolated history, never the main agent's history ([Claude Code Docs](https://code.claude.com/docs/en/sub-agents); [RichSnapp.com](https://www.richsnapp.com/article/2025/10-05-context-management-with-subagents-in-claude-code)).

Subagents currently get a 200K-token context window each. Only the subagent's final message returns to the parent. Intermediate tool calls and results stay inside the subagent. This prevents context pollution -- verbose output from file reads, search results, and exploratory tool calls never enters the parent's context ([InfoQ](https://www.infoq.com/news/2025/08/claude-code-subagents/)).

### How This Helps Research

Subagents are ideal for research because they provide natural context isolation per sub-question. A parent agent can dispatch five sub-questions to five subagents, each searching independently with a clean 200K context. Each returns a focused summary. The parent synthesizes from five concise summaries rather than five sprawling search histories.

This matches Anthropic's own multi-agent research system design: "The detailed search context remains isolated within sub-agents, while the lead agent focuses on synthesizing and analyzing the results" ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

### Limitations

- Subagents **cannot access parent context** -- they receive only the prompt string passed to them
- There is no shared memory between parent and subagent beyond the prompt/response interface
- A feature request exists for an `isolated: true` parameter that would start subagents with zero parent context, useful for adversarial review scenarios ([GitHub #20304](https://github.com/anthropics/claude-code/issues/20304))
- Subagents cannot spawn their own subagents (no recursive delegation)
- The 200K subagent window is fixed and cannot be configured to use the full 1M window

### Information Passing

Information flows one way: parent sends a prompt string to the subagent, subagent returns its final response. To pass context to a subagent, the parent must include it in the prompt string or instruct the subagent to read specific files. To pass structured data back, the subagent's response can include structured formats that the parent parses.

---

## 6. CLAUDE.md and Project Context

### How CLAUDE.md Affects Research Context

CLAUDE.md files are loaded into the context window at the start of every session, consuming tokens alongside the conversation. They are also re-injected after every compaction event. This makes them uniquely persistent but also uniquely costly -- every line of CLAUDE.md reduces available context for actual research work ([Claude Code Docs](https://code.claude.com/docs/en/memory); [Anthropic blog](https://claude.com/blog/using-claude-md-files)).

### Using CLAUDE.md for Research State

CLAUDE.md can persist research state across sessions, but this is an anti-pattern for large or frequently-changing state. CLAUDE.md is best for:
- Research methodology instructions ("When researching, always cite URLs")
- Compaction preservation instructions ("When compacting, preserve all source URLs and finding summaries")
- Pointers to research files ("Current research output is in `_bmad-output/planning-artifacts/research/`")

It is **not** appropriate for:
- Accumulating research findings (use dedicated research files)
- Tracking which questions have been answered (use Task tools or a research file)
- Storing large datasets or search results

### Hierarchical CLAUDE.md

For larger projects, CLAUDE.md can be hierarchical. The `.claude/rules/` directory supports modular rule files that are automatically loaded alongside CLAUDE.md. This allows research-specific instructions to be isolated in their own rule file without bloating the main CLAUDE.md ([builder.io](https://www.builder.io/blog/claude-md-guide); [UX Planet](https://uxplanet.org/claude-code-project-structure-best-practices-5a9c3c97f121)).

---

## 7. Task Tools for State Tracking

### TaskCreate and TaskUpdate

TaskCreate creates a structured task list for the current session. Each task has a subject, description, status (`pending`, `in_progress`, `completed`), and optional dependency tracking via `blockedBy` and `blocks` fields. TaskUpdate changes task status or properties. Tasks provide visual progress indicators in the Claude Code UI ([GitHub - system prompts](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/tool-description-taskcreate.md); [claudefa.st](https://claudefa.st/blog/guide/development/task-management)).

### Cross-Session Coordination

Multiple Claude sessions can share a task list via environment variable configuration. When Session A completes a task, Session B sees the update immediately, enabling parallel research workstreams and resume functionality ([VentureBeat](https://venturebeat.com/orchestration/claude-codes-tasks-update-lets-agents-work-longer-and-coordinate-across)).

### Using Tasks for Research Progress

Tasks serve as structural state that prevents context drift in long workflows. For research, the pattern is:

1. Create tasks for each research question at session start
2. Mark tasks `in_progress` as work begins on each question
3. Mark tasks `completed` as findings are written to the output file
4. After compaction, the task list provides a quick visual of what's done and what remains

This is particularly valuable because task state is maintained by the harness, not by conversation history. Even after aggressive compaction, the task list accurately reflects progress.

### Multi-Agent Task Workflows

In multi-agent setups, a coordinator creates tasks, assigns them to subagents via TaskUpdate, and tracks overall progress. Subagents use TaskGet to fetch assignments and TaskUpdate to report completion. This enables parallel research with coordinated progress tracking ([Mintlify](https://www.mintlify.com/jackdog668/claude-code/tools/agent)).

---

## 8. Tool Result Clearing

A separate but related mechanism is **tool result clearing**, which Anthropic describes as "one of the safest, lightest touch forms of compaction." The `clear_tool_uses_20250919` API strategy clears old tool results when context grows beyond a configured threshold. Older tool results (file contents, search results) are no longer needed once processed. The API automatically clears the oldest results in chronological order ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents); [Platform docs](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)).

This is relevant for research because tool-heavy research sessions (many file reads, many web searches) accumulate massive tool result payloads. Clearing old tool results frees context for new searches without triggering full compaction.

---

## 9. Gaps and Limitations

### Compaction Threshold Inconsistency
The documented 83.5% threshold does not match observed behavior for all users. Some report compaction firing at 76K tokens on a 1M window (7.6%), which is a significant bug that wastes 92% of available context ([GitHub #34332](https://github.com/anthropics/claude-code/issues/34332)). Until this is resolved, research agents cannot rely on having the full 1M window available.

### No Compaction Transparency
Users cannot see what was preserved vs. lost during compaction. There is no diff, no log, and no way to audit what the summarized context contains. This makes it impossible to verify whether critical research findings survived compaction.

### Subagent Context Ceiling
Subagents are limited to 200K tokens regardless of the parent's context window configuration. For research sub-questions that require deep exploration (reading many files, performing many searches), 200K can be constraining. There is no mechanism to grant subagents larger context windows.

### No Recursive Subagents
Subagents cannot spawn their own subagents. This limits the depth of research delegation -- a coordinator can dispatch to researchers, but researchers cannot further delegate to specialized sub-tasks.

### Session Memory is Opaque
The automatic Session Memory system runs without user control over what it captures or how summaries are structured. Users cannot direct it to prioritize research findings over code changes or vice versa.

### Task Tool Limitations
Task tools provide state tracking but not data persistence. A task can be marked "completed" but the task system does not store the findings associated with that task -- those must be written to files separately.

### File-Based Memory Has No Search
Files written during research sessions are just files. There is no semantic search, no indexing, and no way to query across multiple research files. The agent must know the file path and read the file to access previous findings.

### Cross-Session Coordination is Primitive
While task lists can be shared across sessions via environment variables, there is no built-in mechanism for sessions to coordinate on research -- no shared scratchpad, no message passing, no pub/sub between concurrent sessions beyond file system reads/writes.

### Compaction Instructions Are Not Guaranteed
Adding "preserve X during compaction" to CLAUDE.md is a best-effort instruction, not a hard guarantee. The summarization model may still drop information the instruction asked it to preserve, especially under extreme context pressure.

---

## Sources

- [Claude Code Compaction Explained (okhlopkov.com)](https://okhlopkov.com/claude-code-compaction-explained/)
- [Context Window in Claude Code (MindStudio)](https://www.mindstudio.ai/blog/context-window-claude-code-manage-consistent-results)
- [Auto Compact in Claude Code (CometAPI)](https://www.cometapi.com/what-is-auto-compact-in-claude-code/)
- [/compact Command Guide (MindStudio)](https://www.mindstudio.ai/blog/claude-code-compact-command-context-management)
- [1M Context Window GA (claudefa.st)](https://claudefa.st/blog/guide/mechanics/1m-context-ga)
- [Context Buffer Management (claudefa.st)](https://claudefa.st/blog/guide/mechanics/context-buffer-management)
- [Effective Context Engineering (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context Windows (Claude API Docs)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [How Claude Remembers Your Project (Claude Code Docs)](https://code.claude.com/docs/en/memory)
- [Memory Tool (Claude API Docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Session Memory (claudefa.st)](https://claudefa.st/blog/guide/mechanics/session-memory)
- [Persistent Memory Guide (crunchtools.com)](https://crunchtools.com/how-to-give-claude-code-persistent-memory/)
- [Subagents (Claude Code Docs)](https://code.claude.com/docs/en/sub-agents)
- [Context Management with Subagents (RichSnapp.com)](https://www.richsnapp.com/article/2025/10-05-context-management-with-subagents-in-claude-code)
- [Subagent Context Isolation Feature Request (GitHub #20304)](https://github.com/anthropics/claude-code/issues/20304)
- [Claude Code Subagents (InfoQ)](https://www.infoq.com/news/2025/08/claude-code-subagents/)
- [Checkpointing (Claude Code Docs)](https://code.claude.com/docs/en/checkpointing)
- [Checkpoints Guide (skywork.ai)](https://skywork.ai/skypage/en/claude-code-checkpoints-ai-coding/1976917740735229952)
- [Common Workflows (Claude Code Docs)](https://code.claude.com/docs/en/common-workflows)
- [Session Management (Steve Kinney)](https://stevekinney.com/courses/ai-development/claude-code-session-management)
- [Best Practices (Claude Code Docs)](https://code.claude.com/docs/en/best-practices)
- [Writing a Good CLAUDE.md (builder.io)](https://www.builder.io/blog/claude-md-guide)
- [Using CLAUDE.md Files (Anthropic blog)](https://claude.com/blog/using-claude-md-files)
- [Claude Code Compaction (Steve Kinney)](https://stevekinney.com/courses/ai-development/claude-code-compaction)
- [Auto-Compact: What It Loses (Morph)](https://www.morphllm.com/claude-code-auto-compact)
- [TaskCreate System Prompt (GitHub)](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/tool-description-taskcreate.md)
- [Task Management (claudefa.st)](https://claudefa.st/blog/guide/development/task-management)
- [Tasks Update (VentureBeat)](https://venturebeat.com/orchestration/claude-codes-tasks-update-lets-agents-work-longer-and-coordinate-across)
- [Context Engineering Tools (Claude Platform)](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- [1M Context GA (Anthropic)](https://claude.com/blog/1m-context-ga)
- [Opus 4.6 Compaction Bug (GitHub #34332)](https://github.com/anthropics/claude-code/issues/34332)
- [Opus 4.6 Context Compaction (InfoQ)](https://www.infoq.com/news/2026/03/opus-4-6-context-compaction/)
- [Context Engineering for Multi-Agent Systems (arxiv)](https://arxiv.org/html/2508.08322v1)
- [Custom Compaction Instructions (GitHub #14160)](https://github.com/anthropics/claude-code/issues/14160)
