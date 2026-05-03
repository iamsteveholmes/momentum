---
content_origin: web-research
date: 2026-05-02
topic: "TeamCreate Real-World Usage Patterns"
sub_question: "Real-world examples with multi-turn agent communication"
---

# TeamCreate Real-World Usage: Research Findings

## Summary Verdict

Real production examples of **true multi-turn peer-to-peer agent communication via SendMessage** are nearly absent from the public record. What exists instead is: (1) official documentation describing the capability, (2) blog posts and repos that describe or scaffold the pattern without demonstrating it working, (3) a landmark Anthropic case study (the C compiler) that is widely cited as a TeamCreate success but did NOT use TeamCreate or SendMessage at all, and (4) multiple confirmed bugs that prevent the advertised peer-to-peer behaviour from functioning reliably in practice.

---

## 1. The Feature: What TeamCreate Promises

Released with Claude Opus 4.6 on 2026-02-05. Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings. Requires Claude Code v2.1.32+.

**Official documentation** (https://code.claude.com/docs/en/agent-teams) describes:
- `TeamCreate` — lead spawns a named team of independent Claude Code instances
- `SendMessage` — any teammate can send a message to any other teammate by name (peer-to-peer, not just hub-and-spoke)
- Shared task list at `~/.claude/tasks/{team-name}/` with dependency tracking
- Mailbox system: JSON inbox files at `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`
- Message types: `message`, `broadcast` (lead-only), `shutdown_request`, `shutdown_response`, `plan_approval_response`

**Official documentation example** of the key differentiator:
> "Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead."

**Documented use case for genuine P2P**: agents testing competing hypotheses and actively trying to disprove each other via SendMessage (the "scientific debate" pattern). No public reproduction of this pattern in working form was found.

---

## 2. The Anthropic C Compiler Case Study: What It Actually Is

**Widely cited claim**: "Anthropic validated TeamCreate by building a C compiler with 16 agents."

**Actual architecture** (confirmed by fetching https://www.anthropic.com/engineering/building-c-compiler and the InfoQ analysis):

- **16 Claude Opus 4.6 agents ran in parallel Docker containers** against a shared git repo (`https://github.com/anthropics/claudes-c-compiler`)
- **Coordination was git-based lock files**, not SendMessage or TeamCreate
- Agents wrote text files to `current_tasks/` as claim locks; git push forced conflict resolution
- **No orchestration agent**. Carlini explicitly chose NOT to use a central coordinator
- **No SendMessage calls**. The article states: "I haven't yet implemented any other method for communication between agents"
- **The repo README**: "With the exception of this one paragraph that was written by a human, 100% of the code and documentation in this repository was written by Claude Opus 4.6." — a single-agent showcase of code generation scale

**Researcher**: Nicholas Carlini, Anthropic Safeguards team

**Metrics**: ~2,000 Claude Code sessions, $20K API cost, ~2 weeks, 100K lines of Rust, 2B input tokens, 140M output tokens. Compiler compiles Linux 6.9 on x86/ARM/RISC-V, passes 99% of GCC torture tests, compiles QEMU/FFmpeg/SQLite/PostgreSQL/Redis.

**Conclusion on this case study**: The C compiler project is a legitimate Anthropic capability demonstration, but it is NOT a TeamCreate/SendMessage example. It is a parallel-agents-via-shared-git example. Any secondary source claiming this validated "agent teams" or "TeamCreate" is using imprecise language. The Anthropic engineering blog itself does not call it a TeamCreate example.

---

## 3. GitHub Repos: What Exists

### aws-samples/sample-claude-code-agent-team
URL: https://github.com/aws-samples/sample-claude-code-agent-team

**What it is**: Official AWS sample showing a fullstack-agent orchestrating three specialists (coding-agent, devops-agent, review-agent) through a spec-driven development process.

**Communication claim**: "Agents coordinate through shared tasks (`TaskCreate`/`TaskUpdate`/`TaskList`) and direct messaging."

**Evidence of actual P2P**: None. The README describes the intended architecture but contains no code showing actual `SendMessage` implementations, no working demos, no dialogue transcripts.

**Architecture**: Sequential handoffs (plan → build in parallel → review → loop), not iterative peer dialogue.

### cs50victor/claude-code-teams-mcp
URL: https://github.com/cs50victor/claude-code-teams-mcp

**What it is**: Reverse-engineered Claude Code agent teams protocol reimplemented as a standalone MCP server for any harness (Claude Code, OpenCode, etc.)

**Includes**: `send_message` tool described as enabling "DMs, broadcasts (lead only), shutdown/plan responses." Uses JSON inbox files and tmux for process spawning.

**Evidence of actual P2P**: No code examples showing multi-turn agent-to-agent dialogue. Architecture based on reverse-engineering, suggesting the inbox mechanism is understood but working peer dialogue is not demonstrated.

### 777genius/claude_agent_teams_ui
URL: https://github.com/777genius/claude_agent_teams_ui

**What it is**: Desktop kanban-board UI for orchestrating agent teams ("You're the CTO, agents are your team").

**Claims**: "Agents talk to each other — communicate, create and manage their own tasks, review, leave comments." "Agent-to-agent messaging: Native real-time mailbox."

**Evidence of actual P2P**: No code examples demonstrating the implementation. Whether this is true peer-to-peer or a mediated hub-and-spoke via the UI layer is not determinable from public docs.

### wshobson/agents
URL: https://github.com/wshobson/agents

**What it is**: 80-plugin, 185-agent collection with an `agent-teams` plugin offering 7 team presets.

**Evidence of actual P2P**: None. Orchestration model shows sequential handoffs, not peer dialogue. Uses plugin composition, not TeamCreate.

### barkain/claude-code-workflow-orchestration
URL: https://github.com/barkain/claude-code-workflow-orchestration

**What it is**: Multi-step workflow orchestration plugin with parallel agent execution and task decomposition.

**Evidence of actual P2P**: Not assessed in detail. No evidence found of multi-turn SendMessage peer dialogue.

---

## 4. Blog Posts and Articles: Pattern Assessment

### alexop.dev — "From Tasks to Swarms"
URL: https://alexop.dev/posts/from-tasks-to-swarms-agent-teams-in-claude-code/

**Honest finding from this article**: The QA swarm example shows 5 agents working in **parallel isolation** (pages, posts, links, SEO, accessibility). Each sends a structured report back to the lead. This is hub-and-spoke, not peer mesh. The article claims "The UI teammate can ask the API teammate to spin up a dev server" but provides no code example demonstrating it.

### Isaac Kargar / Medium — "Agent Teams with Claude Code and Claude Agent SDK"
URL: https://kargarisaac.medium.com/agent-teams-with-claude-code-and-claude-agent-sdk-e7de4e0cb03e

**Honest finding**: Execution logs show the lead agent using `Bash` `sleep` commands and checking file system state rather than receiving autonomous inter-agent messages. The one `SendMessage` example shown is a shutdown request (`{"type": "shutdown_request", "recipient": "architect", ...}`), not a peer content exchange.

### heeki.medium.com — "Collaborating with agents teams in Claude Code"
URL: https://heeki.medium.com/collaborating-with-agents-teams-in-claude-code-f64a465f3c11

**Honest finding**: No actual logs or transcripts showing peer-to-peer communication. Author quotes official Anthropic documentation as evidence of the capability. Author acknowledges "teammates get stuck and the team lead loses track of them" and that parallelism provided "minimal actual advantage" for their workloads.

### kieranklaassen Gist — "Claude Code Swarm Orchestration Skill"
URL: https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea

**Honest finding**: Describes `Teammate({ operation: "write", target_agent_id: ..., value: ... })` for lead-to-teammate messaging, and a diagram with a dotted line between teammates labeled "can message." The operational guidance consistently routes through the lead's inbox. Direct agent-to-agent exchange is unimplemented in the skill.

---

## 5. Confirmed Bugs Blocking Real P2P Usage

### Issue #48160 — Spawned subagents cannot originate SendMessage
URL: https://github.com/anthropics/claude-code/issues/48160

**Status**: Closed as duplicate (known issue)

**Impact**: Spawned subagents can **receive** SendMessage messages but **cannot send** them. `ToolSearch("select:SendMessage")` returns no match in subagent context. In one real test: parent "field-manager" spawned four named subagents; parent could call `SendMessage(to="indexes", ...)` successfully, but three of four subagents could not reciprocate. The claimed peer-to-peer architecture degrades to one-way broadcast.

### Issue #25135 — SendMessage silently succeeds when recipient name doesn't match
URL: https://github.com/anthropics/claude-code/issues/25135

**Status**: Open at time of research

**Impact**: `SendMessage` returns `{success: true, message: "Message sent to alice's inbox"}` even when no agent polls `alice.json`. The `validateInput()` implementation only checks for empty string in recipient field — no validation against actual team members. Messages written to orphaned inbox files are silently lost. Root cause: `InboxPoller` reads from a fixed registered name; arbitrary recipient names create unpolled files.

**Workaround available**: Always use `recipient: "team-lead"` explicitly; monitor `~/.claude/teams/` inbox files manually.

### Issue #27555 — Teammate messages render with `⏺ Human:` prefix
URL: https://github.com/anthropics/claude-code/issues/27555

**Impact**: SendMessage messages from teammates are visually indistinguishable from user input in the terminal. The `from` field in the inbox JSON is available but not surfaced to the display. This is a UI bug but also confirms the actual message routing mechanism: JSON inbox files, not a live message bus.

### Issue #1124 (claude-code-action) — TeamCreate/SendMessage unusable in SDK headless mode
URL: https://github.com/anthropics/claude-code-action/issues/1124

**Impact**: In SDK/headless environments (e.g., CI, GitHub Actions), the lead agent produces `end_turn` immediately after spawning teammates because the SDK session lifecycle has no keepalive. Teammates spawn as separate processes that return "The agent is now running and will receive instructions via mailbox" — but the session exits (typically after 10-11 turns) before they complete. A "watcher" subagent workaround is blocked by auto-enrollment: all agents spawned by an active team lead are auto-enrolled as teammates. No working workaround found; feature is effectively non-functional in headless SDK mode.

### Issue #32723 — TeamCreate available to standalone subagents but not to teammates
URL: https://github.com/anthropics/claude-code/issues/32723

**Impact**: Reveals the architectural constraint: only the team lead (the initial Claude Code session) can spawn and manage teammates. Standalone subagents have `TeamCreate` but not `Agent` tool, so they can create team shells but cannot populate them. Inside a team, teammates do not have `TeamCreate`/`TeamDelete`. This enforces hub-and-spoke: all team management must flow through the original lead process.

---

## 6. Vikrant Jain's "Taskbox" — An Alternative Approach
URL: https://vikrantjain.hashnode.dev/distributed-claude-code-agents-across-machines

**What it is**: An independently developed alternative to TeamCreate using SQLite in WAL mode as the coordination layer. Multiple Claude Code agents on different machines (or same machine) share a task queue via a thin Python CLI wrapper with no daemon, no server, standard library only.

**Relevance**: Shows the community working around TeamCreate limitations. Agents coordinate through `Taskbox` poll-and-claim semantics, not SendMessage. This is closer to the C compiler's git-lock approach than to the mailbox pattern.

---

## 7. MOAI-ADK and +1GSD

No results found for either "MOAI-ADK" or "+1GSD" in any public web search. These names do not appear in any indexed repo, blog post, paper, forum, or social media post. They should be treated as unverifiable until a primary source is identified.

---

## 8. YouTube / Conference Demos

Three YouTube videos found (titles suggest demos but content not verified):
- "How Anthropic's NEW Tool Let's You Create a 100+ AI Agent Team (Easily)" — https://www.youtube.com/watch?v=KQrZWI8K934
- "Anthropic Just KILLED The AI Agent Industry (Build 3 in 12 Min)" — https://www.youtube.com/watch?v=gWtAY8LxGtE
- "Anthropic drops Claude Managed Agents: here's an explanation and demo of what it actually is" — https://www.youtube.com/watch?v=5z1EX77_3po

None of these titles indicate they demonstrate actual multi-turn peer-to-peer SendMessage exchanges. No conference talk (e.g., ICLR, NeurIPS, SWEng conference) was found specifically presenting TeamCreate multi-turn communication in a research context.

---

## 9. What Actually Works vs What Is Claimed

| Capability | Documented | Demonstrated in Public | Confirmed Working |
|---|---|---|---|
| Lead spawning teammates via TeamCreate | Yes | Yes (basic examples) | Yes (CLI mode) |
| Lead sending messages to teammates (shutdown_request) | Yes | Yes (in blog logs) | Yes |
| Shared task list coordination | Yes | Yes (alexop.dev QA example) | Yes |
| Teammate messaging lead (shutdown_response) | Yes | Partially | Partially (bug #48160) |
| True peer-to-peer teammate↔teammate messaging | Yes (docs) | No real examples found | Unclear/Buggy |
| Multi-turn inter-agent dialogue (back-and-forth) | Yes (docs) | No real examples found | Not confirmed |
| Working in SDK/headless mode | No (docs warn against) | Not found | No (bug #1124) |
| Recipient name validation in SendMessage | No (docs omit) | N/A | No (bug #25135) |

---

## 10. Key Source URLs

- Official docs: https://code.claude.com/docs/en/agent-teams
- C compiler blog: https://www.anthropic.com/engineering/building-c-compiler
- C compiler repo: https://github.com/anthropics/claudes-c-compiler
- Bug #48160 (subagents can't send): https://github.com/anthropics/claude-code/issues/48160
- Bug #25135 (silent failure): https://github.com/anthropics/claude-code/issues/25135
- Bug #27555 (Human: prefix): https://github.com/anthropics/claude-code/issues/27555
- Bug #1124 SDK lifecycle: https://github.com/anthropics/claude-code-action/issues/1124
- Bug #32723 tool availability: https://github.com/anthropics/claude-code/issues/32723
- AWS sample: https://github.com/aws-samples/sample-claude-code-agent-team
- MCP reimplementation: https://github.com/cs50victor/claude-code-teams-mcp
- Kanban UI: https://github.com/777genius/claude_agent_teams_ui
- TechCrunch Opus 4.6 announcement: https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/
- InfoQ C compiler analysis: https://www.infoq.com/news/2026/02/claude-built-c-compiler/
