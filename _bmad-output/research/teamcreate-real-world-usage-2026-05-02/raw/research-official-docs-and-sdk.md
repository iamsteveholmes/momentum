---
content_origin: claude-code-guide-agent
date: 2026-05-02
topic: "TeamCreate Real-World Usage Patterns"
method: claude-code-guide subagent, official docs lookup
---

# TeamCreate: Official Documentation & SDK Research

## Overview

TeamCreate is an agent coordination tool (experimental as of early 2026) that creates a named team container for managing multiple independent Claude Code sessions. Accessed via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

**Architecture:** One session acts as Team Lead. Teammates are full, independent Claude Code sessions with their own context windows. Communication is peer-to-peer via SendMessage, not only through the lead.

**Key distinction from subagents:**
- Subagents: Run within a single session, report back to main agent only
- Agent Teams: Each teammate is a full, independent Claude Code session with its own context window; they communicate peer-to-peer

---

## TeamCreate API Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team_name` | string | Yes | Unique identifier for the team (e.g., `"taskrunner-build"`). Links all team resources together on disk. |
| `description` | string | No | Text description of the team's purpose |

**On-disk storage:**
- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`

The `config.json` contains a `members` array with each teammate's name, agent ID, and agent type. **Do not edit these files manually** — auto-generated and maintained by Claude Code.

---

## SendMessage: Inter-Agent Communication

SendMessage is the peer-to-peer messaging tool available to all agents in a team.

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipient` | string | Name of the receiving teammate (or lead) |
| `message` | string | The message content |

### Delivery Model — CRITICAL DIFFERENCE

**Interactive mode (Claude Code CLI):**
- Messages arrive between turns as inline `<teammate-message>` blocks
- Automatic delivery; lead doesn't need to poll
- Full bidirectional communication works

**SDK mode (headless / ClaudeSDKClient):**
- **BROKEN**: Messages sent by teammates are never received by the lead
- Session terminates after lead's turn 1 before teammates' messages can be delivered
- No equivalent "next turn" mechanism in SDK to receive async messages
- **Impact: Agent teams are unusable in CI/CD, automation, or headless pipelines**

---

## Official Documented Use Cases

From official Claude Code docs — best for:

1. **Research & Review**: Multiple teammates investigate different aspects simultaneously, then share findings
2. **New Modules/Features**: Teammates each own separate pieces without file conflicts
3. **Debugging with Competing Hypotheses**: Teams test different theories in parallel, converge faster
4. **Cross-Layer Coordination**: Changes spanning frontend, backend, tests — each owned by different teammate

### Teams vs Fan-Out (Official Comparison)

| Aspect | Subagents (fan-out) | Agent Teams |
|--------|---------------------|-------------|
| Context | Own window; results return to caller | Own window; fully independent |
| Communication | Report back to main agent only | Teammates message each other directly |
| Coordination | Main agent manages all work | Shared task list with self-coordination |
| Best for | Focused tasks where only result matters | Complex work requiring discussion/collaboration |
| Token Cost | Lower: results summarized back | Higher: each teammate is separate Claude instance |

**Official decision rule:** "Use subagents when you need quick, focused workers that report back. Use agent teams when teammates need to share findings, challenge each other, and coordinate on their own."

---

## Known Issues & Failure Modes (GitHub)

### CRITICAL: SendMessage Broken in SDK Mode (Issue #577)

When using `ClaudeSDKClient`:
- Session terminates after lead's first turn when `receive_response()` yields `ResultMessage`
- Teammates' `SendMessage` calls never arrive
- **Workarounds:** Lead runs `sleep 5` to extend session; or teammate writes to file and lead polls

### Silent Process Exit (Issue #34614)

In Claude Code v2.1.76+:
- Teammate processes silently exit immediately after spawn
- Pane opens in tmux but process exits with no error output

### Undocumented Tool Availability (Issue #32723)

Counterintuitive tool availability matrix:

| Context | TeamCreate | TeamDelete | SendMessage | Agent Tool |
|---------|-----------|-----------|------------|-----------|
| Standalone Subagent | YES | YES | YES | NO |
| Teammate | NO | NO | YES | NO |

A standalone subagent can call TeamCreate and persist a team config but can't spawn teammates (no Agent tool). Creates orphaned "team shells."

### Other Known Issues

| Issue | Impact | Workaround |
|-------|--------|-----------|
| No session resumption | `/resume` doesn't restore teammates | Spawn new teammates post-resume |
| Task status lags | Teammates may fail to mark tasks complete | Manually nudge |
| Slow shutdown | Teammates don't terminate immediately | Give time |
| One team per session | Can't manage multiple teams | Clean up before new team |
| No nested teams | Teammates can't spawn their own teams | Only lead manages team |
| Model config not inherited | Teammates don't get custom model | Specify model explicitly |
| File conflicts | Parallel edits overwrite each other | Partition files by teammate |

---

## Real Multi-Turn Collaboration Examples

The official docs show **user→lead interactions**, not **teammate↔teammate multi-turn examples**. The competing-hypotheses example describes the *concept* but not the *implementation*.

From docs: "The debate structure is the key mechanism here. Sequential investigation suffers from anchoring: once one theory is explored, subsequent investigation is biased toward it. With multiple independent investigators actively trying to disprove each other, the theory that survives is much more likely to be the actual root cause."

This implies teammates *should* message each other directly, but SDK mode breaks this.

---

## Sources

- Claude Code Agent Teams Official Docs
- Claude Managed Agents Multiagent API  
- GitHub Issue #577: SendMessage SDK Failure
- GitHub Issue #32723: Undocumented Tool Availability
- GitHub Issue #34614: Silent Process Exit
- Medium: Agent Teams with Claude Code and Claude Agent SDK (kargarisaac)
