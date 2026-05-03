---
content_origin: gemini-thinking
date: 2026-05-02
topic: "TeamCreate Real-World Usage Patterns"
method: claude-in-chrome, Thinking mode
---

# Gemini Thinking Mode Response: TeamCreate Real-World Use Cases

## 1. Documented Use Cases & Official Spec

The TeamCreate and Agent Teams functionality represents the shift from "parallel execution" to "collaborative multi-agent choreography" within the Anthropic Agent SDK and Claude Code. As of early 2026, this feature is primarily accessed via the experimental flag `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

Unlike simple "fan-out" (where a lead spawns isolated agents that return a final string), TeamCreate builds a shared state environment where agents persist as long-lived processes.

**Shared Infrastructure:** TeamCreate generates a scaffolding under `.claude/teams/<team_id>/`. This includes a `mailbox/` for inter-agent messages and a `task_list.json` for shared state.

**The "Debate" Use Case:** The docs explicitly recommend teams for "deep debugging with multiple hypotheses." Instead of one agent looking for a bug, you spawn three: one to investigate logs, one to trace network state, and one to verify the fix — allowing them to debate findings via sendMessage before reporting back.

**Official Guidance (Team vs. Fan-out):**
- **Fan-out (Isolated Agent calls):** For deterministic, independent sub-tasks (e.g., "Summarize these 10 files")
- **Teams (TeamCreate):** For tasks requiring dynamic delegation. If Agent A finds a bug in the database schema while investigating a slow query, it can message Agent B (the DB specialist) to adjust the schema immediately rather than waiting to report back to the Lead.

## 2. Real-World & Production Examples

While still "experimental," several high-profile projects have moved past toy examples:

**Anthropic's "C-Compiler" Case Study:** The flagship proof-of-concept involved 16 agents working in a single team to build a Rust-based C compiler from scratch. They produced ~100,000 lines of code. The key was the "Coordinator-Janitor" pattern: the Lead coordinated, while "Janitor" teammates continuously ran test suites and sent `sendMessage` alerts to "Developer" teammates when a build broke.

**MOAI-ADK (Modu-AI):** An open-source Agentic Development Kit built on top of Claude Code. It uses TeamCreate to implement a "TDD Quality Gate." One teammate writes the spec/test, and another writes the implementation. They iterate via the team mailbox until the test passes, without human intervention.

**+1GSD (Get Shit Done):** A project management layer that uses TeamCreate for "Large Cross-Repo Merges." It spawns a team to analyze upstream changes across 10+ repos simultaneously, using a shared finding doc to ensure variable name changes are consistent across all agents' worktrees.

## 3. Known Failure Modes & Practical Gotchas

**The "Permission Deadlock":** A major discovered bug is that when a teammate requests permission for a tool (like Write), the Team Lead's UI can crash or hang. The teammate waits indefinitely for approval that the Lead's UI cannot render. Workaround: Many developers currently run teams in `teammateMode: "tmux"`, which isolates the UI panes and prevents a single-process crash from killing the whole team.

**Context Fragmentation:** Teammates do not inherit the Lead's full conversation history — only what is provided in the Task spawn prompt. This can lead to "amnesia" where a teammate makes a decision that contradicts a previous human instruction given to the Lead.

**Orphaned Processes:** Because teams spawn separate Claude instances and often utilize the Model Context Protocol (MCP), a session crash often leaves "zombie" `node.exe` or `python` processes running. On Windows, this frequently leads to memory exhaustion after 3–4 failed team sessions.

**Lack of Tool Isolation:** Currently, teammates inherit the Lead's full permission set. There is no native way yet to spawn a "Read-Only Researcher" alongside a "Full-Access Implementer" within the same TeamCreate call; they all technically have the same "keys to the house."

---

*NOTE: Gemini Thinking mode may hallucinate specific project names, GitHub repos, and case study details. The MOAI-ADK and +1GSD projects require independent verification. The C-Compiler case study may be conflated with Anthropic's internal research.*
