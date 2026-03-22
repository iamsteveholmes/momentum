---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments: []
workflowType: 'research'
lastStep: 6
research_type: 'technical'
research_topic: 'CMUX integration with Claude Code'
research_goals: 'Understand how developers are using CMUX capabilities within Claude Code skills and workflows, identify real-world integration patterns, cross-repo management, tool/process management, anti-patterns, and community examples'
user_name: 'Steve'
date: '2026-03-22'
web_research_enabled: true
source_verification: true
---

# CMUX Integration with Claude Code: Technical Research

**Date:** 2026-03-22
**Author:** Steve
**Research Type:** Technical

---

## Research Overview

This report investigates how developers are integrating CMUX — a purpose-built macOS terminal for AI agent orchestration — with Claude Code as of March 2026. The research covers three dimensions: (1) what CMUX is and how the community uses it, (2) integration patterns, use cases, and anti-patterns, and (3) whether Momentum should integrate CMUX as an optional feature.

Methodology: web research with adversarial validation (AVFL Gate 1 on raw research, verification pass on all high-risk claims). All facts below have been traced to primary sources unless marked otherwise. See Section 7 for the full source registry and confidence assessment.

---

## 1. Executive Summary

CMUX (manaflow-ai/cmux) is a native macOS terminal launched in February 2026, purpose-built for orchestrating multiple AI coding agents. Built on Ghostty's libghostty for GPU-accelerated rendering, it has gained rapid adoption (~9,400 GitHub stars within its first two months). Its core value lies in visual session awareness, cross-repo visibility, and external process monitoring — not in agent orchestration, which Claude Code's native subagent model handles more effectively.

The community has produced two notable Claude Code skills (setup-cmux, bounds.dev cmux) and one MCP server (cmuxlayer with 10 tools). Integration patterns cluster around workspace configuration and environment-aware agent behavior — agents detect CMUX via environment variables and adapt their output accordingly. Cross-session agent orchestration via CMUX is an identified anti-pattern; subagents are simpler and share context natively.

For Momentum, CMUX integration is architecturally aligned with Epic 7 ("Bring Your Own Tools") as a concrete binding of a `terminal-multiplexer` protocol type. It should be optional, never a dependency, and deferred until Epic 7's protocol infrastructure exists. The primary Momentum use cases are worktree-to-terminal binding (auto-create CMUX tabs per story session) and cross-repo operations (installing Momentum in target repos while watching progress).

**Key Findings:**

| Finding | Confidence |
|---------|------------|
| CMUX is a real, actively-maintained macOS terminal with strong community adoption | HIGH |
| The MCP ecosystem is small (1 primary server, 10 tools) — not the "80+ tools" initially reported | HIGH (verified) |
| Cross-session orchestration via CMUX is inferior to Claude Code subagents | HIGH (architectural analysis) |
| CMUX's real value = visibility + cross-repo + process monitoring | HIGH |
| Epic 7 BYOT is the correct integration mechanism for Momentum | HIGH (architectural fit) |

**Recommendations:**

1. Integrate CMUX as an optional Epic 7 protocol binding — never a dependency
2. Define a `terminal-multiplexer` protocol contract as part of Epic 7 design
3. Implement three bindings: CMUX (macOS), tmux (cross-platform), null (default)
4. Do not build any CMUX-specific code before Epic 7 protocol infrastructure exists

---

## 2. What is CMUX

### 2.1 Origin and Architecture

CMUX is a native macOS terminal application created by Lawrence Chen (@lawrencecchen) and Austin Wang (@austinywang) under the manaflow-ai organization. It launched in late January 2026, gained rapid traction (reportedly hitting #2 on Hacker News), and had accumulated ~9,400 GitHub stars by mid-March 2026.

**Technical architecture:**
- Native Swift + AppKit application (macOS only)
- Terminal rendering via Ghostty's libghostty engine (GPU-accelerated)
- Embedded browser via WebKit/WKWebView (not Chromium as initially reported by research agent)
- Socket API for programmatic control via structured JSON over Unix socket
- Environment variable injection: `CMUX_WORKSPACE_ID`, `CMUX_SURFACE_ID`, `CMUX_SOCKET_PATH`
- Licensed AGPL-3.0

**Core UI features:**
- Vertical sidebar tabs showing git branch, linked PR status/number, working directory, listening ports, and notification text per workspace
- Split panes for isolating parallel agent tasks
- Notification system: visual rings on tabs, unread badges, popovers, macOS desktop notifications
- Session hierarchy: window > workspace > pane > surface > panel

**Supported agents:** Claude Code, Codex, Aider, Gemini CLI, Cline, Cursor Agent, Goose, and any CLI tool that runs in a terminal.

_Source: [github.com/manaflow-ai/cmux](https://github.com/manaflow-ai/cmux), [cmux.com](https://cmux.com)_

**Important disambiguation:** There is a separate, unrelated project also named "cmux" at github.com/craigsc/cmux (~415 stars). This is a Bash-based tool ("tmux for Claude Code") that manages git worktrees for parallel Claude Code sessions. It is not the same project as manaflow-ai/cmux.

### 2.2 The MCP Ecosystem

**cmuxlayer** ([glama.ai/mcp/servers/EtanHey/cmuxlayer](https://glama.ai/mcp/servers/EtanHey/cmuxlayer))
- Terminal multiplexer MCP server for AI agent orchestration
- Provides **10 MCP tools**: `list_surfaces`, `new_split`, `send_input`, `send_key`, `read_screen`, `rename_tab`, `set_status`, `set_progress`, `close_surface`, `browser_surface`
- Returns raw terminal text + structured parsed agent metadata
- Supports Claude Channels via `CMUXLAYER_ENABLE_CLAUDE_CHANNELS=1`
- Built by @EtanHey, Apache 2.0 licensed

**cmux-agent-mcp** ([glama.ai/mcp/servers/multiagentcognition/cmux-agent-mcp](https://glama.ai/mcp/servers/multiagentcognition/cmux-agent-mcp))
- Programmable terminal control plane for multi-agent AI workflows
- Remote-controllable terminal multiplexer

**Terminal Control Protocol:**
- Structured JSON messages over Unix socket (typed, versioned, self-describing)
- Command categories: workspace management, pane/surface management, interaction (send text/key presses), browser control, feedback (notifications, status, progress)

### 2.3 The Competitive Landscape

| Tool | Repo | Stars | Platform | Architecture | Primary Use Case |
|------|------|-------|----------|-------------|-----------------|
| **CMUX** | manaflow-ai/cmux | ~9,400 | macOS only | Native Swift/AppKit + libghostty | Visual AI agent orchestration terminal |
| **craigsc/cmux** | craigsc/cmux | ~415 | Any (Bash) | Shell script + tmux + git worktrees | Parallel Claude Code sessions via worktrees |
| **Amux** | mixpeek/amux | ~86 | Any (tmux) | Bash CLI (~680 lines) + Python web server | Unattended parallel agent execution with dashboard |
| **Coder Mux** | coder/mux | ~1,400 | macOS, Linux, Windows, Browser | TypeScript/Electron + React | Enterprise parallel agentic dev on governed infra |
| **dmux** | standardagents/dmux | ~1,200 | Any (tmux) | Shell + tmux + git worktrees | Dev agent multiplexer for coding agents |

**Key distinctions:**
- CMUX is the only native macOS app — others use tmux or Electron
- Coder Mux targets enterprise with governance and remote compute
- Amux and dmux target unattended parallel execution
- craigsc/cmux is the most lightweight (pure shell, worktree-focused)

_Sources: GitHub repos verified 2026-03-22_

### 2.4 Source Confidence Assessment

| Category | Confidence | Notes |
|----------|------------|-------|
| CMUX existence, authorship, license | HIGH | Verified against GitHub repo |
| Star count (~9,400) | HIGH | Verified via GitHub API, March 2026 |
| Feature set (sidebar, panes, notifications, socket API) | HIGH | Verified in repo README |
| Browser engine (WebKit, not Chromium) | HIGH | Corrected from initial research; native Swift app uses WKWebView |
| cmuxlayer tool count (10 tools) | HIGH | Verified on Glama; initial "80+" claim was fabricated |
| Alternative tools (Amux, Coder Mux, dmux) | HIGH | All repos verified |
| Community articles | MODERATE-HIGH | 4/4 spot-checked confirmed with live URLs |
| Amux architecture | MODERATE | Core CLI is Bash (not Python as initially claimed); has separate Python server |

---

## 3. Integration Patterns and Community Usage

### 3.1 The setup-cmux Skill (jbasdf)

The most comprehensive Claude Code + CMUX skill found is a GitHub Gist by jbasdf that configures CMUX workspaces for Claude Code projects.

**What it does:**
- Generates/updates `.vscode/terminals.json` for workspace setup
- Uses a Python script (`scripts/cmux.py`) to process config and create workspaces via the cmux CLI
- Creates organized workspaces with specialized tabs:
  - **AI Workflow workspace**: plan-stories, plan-sweep, review-open-prs, fix-pr-issues, merge-approved-prs, cleanup-merged, docs-maintain, status — plus console, reminder, and plans tabs
  - **App workspace**: application servers, database, tests (configured by tech stack)
  - **Development workspace**: multiple Claude Code sessions + console
- Teaches agents CMUX topology awareness (window > workspace > pane > surface)
- Updates project CLAUDE.md with a Terminal Interaction section

**Analysis:** This is a *static workspace layout* pattern. Each tab runs one Claude Code instance with a fixed prompt/purpose. The strength is visual organization of parallel agent activities. The weakness is no dynamic orchestration or cross-agent context sharing — each tab is an independent session.

_Source: [gist.github.com/jbasdf/2f31c6fc12dea4f739543ad41f564c86](https://gist.github.com/jbasdf/2f31c6fc12dea4f739543ad41f564c86)_

### 3.2 The bounds.dev Environment-Aware Agent Pattern

The bounds.dev skill takes a different approach: instead of configuring CMUX externally, it teaches agents to *detect and use* CMUX from within.

**What it does:**
- Agents check for `CMUX_WORKSPACE_ID`, `CMUX_SURFACE_ID`, `CMUX_SOCKET_PATH` environment variables
- If detected, agents can:
  - Report progress via `cmux set-progress`
  - Send notifications via `cmux notify`
  - Open URLs in split panes
  - Interact with the embedded browser
  - Respect surface ownership (don't send input to surfaces the user is typing in)

**Analysis:** This is the more sophisticated pattern. Agents become *CMUX-aware* rather than merely *CMUX-launched*. The key insight is **environment detection** — the same agent works with or without CMUX, adapting its behavior when CMUX is present. This is the pattern Momentum should emulate.

_Source: [github.com/boundsj/agent-skills/blob/main/cmux/SKILL.md](https://github.com/boundsj/agent-skills/blob/main/cmux/SKILL.md), [bounds.dev/posts/teaching-claude-code-to-drive-cmux/](https://www.bounds.dev/posts/teaching-claude-code-to-drive-cmux/)_

### 3.3 Cross-Agent Communication via MCP

cmuxlayer's MCP tools enable one agent to control another's terminal:
- `send_input`: type text into another surface
- `read_screen`: read terminal output from another surface
- `new_split`: create new panes programmatically
- Claude Channels support for structured agent-to-agent messaging

**Analysis:** Interesting but competes directly with Claude Code's native subagent model. When you need agent A to coordinate with agent B, subagents share context natively and don't require terminal socket communication. The MCP layer adds latency, loses structured data (everything becomes terminal text), and introduces failure modes (surface ownership conflicts, timing issues).

### 3.4 Anti-Patterns (Critical Finding)

**Anti-pattern 1: Cross-session orchestration via CMUX instead of subagents.**

Claude Code's subagent model (the `Agent` tool) provides:
- Native context sharing between parent and child
- Structured data exchange (not terminal text scraping)
- Automatic lifecycle management (child exits, parent gets result)
- Tool access control per agent
- Model routing per agent

CMUX cross-session orchestration requires:
- Terminal text parsing (lossy, fragile)
- Socket API communication (additional failure mode)
- Surface ownership management (who's typing where?)
- Manual lifecycle coordination
- No context sharing between sessions

**The verdict:** If you need agent orchestration, use subagents. CMUX adds value *alongside* subagents for visibility and process monitoring, not *instead of* them.

**Anti-pattern 2: CMUX as primary orchestrator.**

The setup-cmux skill's "AI Workflow" workspace pattern (8 numbered step tabs) treats CMUX as the orchestration layer — a human manually switches between tabs to advance a workflow. This is backwards: the workflow should be automated in a skill with subagents, with CMUX providing visibility into what's happening.

**Anti-pattern 3: Over-coupling to CMUX environment.**

Skills that *only work* inside CMUX violate portability. The bounds.dev pattern (detect and adapt) is correct; hard CMUX dependencies are not.

---

## 4. The Real Value Proposition

Given the anti-patterns above, where does CMUX actually add value that Claude Code cannot natively provide?

### 4.1 Cross-Repo Management

Claude Code sessions are single-repo. CMUX provides multi-repo visibility.

**Use case: Momentum installing itself in another repo.**
- Primary pane: Claude Code running in `~/projects/momentum`
- Secondary pane: CMUX tab showing `~/projects/target-repo`
- Momentum agent runs installation commands in the target repo via CMUX
- Developer watches both repos simultaneously

**Use case: Multi-repo development coordination.**
- Frontend repo in one workspace, backend API in another
- Agent making API changes can see frontend test output in adjacent pane
- No context-switching between terminal windows

**Why this matters:** Claude Code's `Bash` tool can run commands in other directories, but the developer has no persistent visual window into what's happening there. CMUX provides that persistent visual context.

### 4.2 External Process Monitoring

Claude Code can start processes but cannot persistently display their output alongside its own work.

**Use case: Simulator feedback loop (Nornspun).**
- Pane 1: Claude Code making code changes in `~/projects/nornspun`
- Pane 2: Simulator running, output visible to both developer and (via `read_screen`) to Claude Code
- Agent evaluates simulator output after each change
- Developer sees both code changes and simulator results in real-time

**Use case: Dev server + test runner.**
- Pane 1: Claude Code editing code
- Pane 2: Dev server with hot reload (output visible)
- Pane 3: Test runner watching for changes
- Developer monitors all three without tab-switching

**Why this matters:** Claude Code can `run_in_background` a process, but the output is only accessible via explicit tool calls. CMUX makes it visually persistent and ambient.

### 4.3 Visual Session Awareness

When running concurrent Momentum story sessions (the worktree-per-story model), visual awareness prevents the "out-of-the-loop" problem.

**Use case: Parallel story development.**
- 2-3 concurrent `momentum-dev` sessions, each in its own worktree
- CMUX sidebar shows: branch name, PR status, active ports per session
- Notification rings when a session completes or needs attention
- Developer can glance at sidebar to see all story statuses without checking each session

**Why this matters:** Momentum's `momentum-dev` workflow already supports concurrent worktrees with lock files for safety. CMUX adds the *visual* layer that lets developers monitor multiple sessions without active polling.

### 4.4 What CMUX Does NOT Replace

- **Momentum's worktree management** — `momentum-dev` already handles `.worktrees/story-{id}` creation, branch management, and lock files
- **Claude Code's subagent orchestration** — subagents are superior for coordinated work
- **MCP servers for structured tool access** — terminal text scraping via `read_screen` is not a substitute for structured API responses
- **Hook infrastructure for enforcement** — CMUX has no enforcement mechanism; Momentum's hooks are deterministic

---

## 5. Momentum Integration Assessment

### 5.1 Architectural Fit: Epic 7 BYOT Protocol

CMUX fits naturally as a concrete implementation of a terminal-multiplexer protocol type under Epic 7 ("Bring Your Own Tools").

**Epic 7 architecture (currently backlog, unimplemented):**
- Story 7-1: Project configuration file defines protocol bindings
- Story 7-2: Protocol gap resolution creates valid config entries
- Story 7-3: Workflow steps resolve through protocol interfaces at invocation time
- Story 7-4: Protocol substitution satisfies interface contract

**How CMUX would fit:**
- A project config would define a protocol binding for terminal multiplexing (exact syntax TBD — Epic 7 is unimplemented)
- Workflow steps would reference a generic interface (e.g., "create-pane", "send-to-pane", "read-from-pane", "detect-environment")
- At runtime: resolves to the configured provider (CMUX MCP server, tmux commands, or null/no-op)
- Zero CMUX-specific code in any workflow or skill

**This approach means:**
- CMUX users get terminal integration automatically
- tmux users get a cross-platform alternative
- Users without a multiplexer lose nothing (null binding)
- Workflows remain portable and testable

### 5.2 Concrete Integration Points

**Worktree-to-terminal binding (highest value):**
When `momentum-dev` creates `.worktrees/story-{id}`, a CMUX-aware binding could:
- Create a corresponding CMUX tab named `story/{id}`
- Set the tab's working directory to the worktree path
- Display the story's branch name in the sidebar
- Clean up the tab when the worktree is removed after merge

**Process monitoring skill:**
A new skill that launches an external process in a CMUX pane and reads its output. Directly enables the simulator feedback loop use case (Nornspun).

**Session dashboard:**
CMUX sidebar could display momentum sprint status, active story sessions, and their states. Maps to the concurrent session awareness need.

**Hook-to-notification bridge:**
PostToolUse hooks could send CMUX notifications when significant events occur (story completion, test failure, review needed). Uses `cmux notify` CLI.

### 5.3 What NOT to Build

- **No CMUX orchestration layer** — subagents handle this
- **No CMUX-required skills** — every skill must work without CMUX (bounds.dev pattern: detect and adapt)
- **No agent-to-agent messaging via CMUX** — use subagents or shared files
- **No CMUX installation/setup in Momentum core** — it's a user-provided tool
- **No CMUX-specific code in existing workflows** — all integration goes through Epic 7 protocols

### 5.4 Implementation Priority and Sequencing

**Not before Epic 7.** CMUX integration requires the BYOT protocol infrastructure. Building CMUX support without Epic 7 means hardcoding, which violates Momentum's architecture principle: "Every integration point is a configurable protocol. Implementations are substitutable without modifying workflows."

**Recommended sequence:**
1. Epic 7 Stories 7-1 through 7-3 (protocol infrastructure) — no CMUX dependency
2. Add `terminal-multiplexer` as a protocol type in the protocol registry
3. Define the protocol contract: `create-pane`, `send-to-pane`, `read-from-pane`, `detect-environment`, `notify`, `cleanup`
4. Implement CMUX binding as reference implementation (thin adapter over cmuxlayer MCP or cmux CLI)
5. Implement tmux binding as cross-platform alternative
6. Implement null binding (default — no terminal multiplexer)

**Effort:** Small. The binding itself is a thin adapter. The protocol contract design is the real work, and it's part of Epic 7 regardless of CMUX.

### 5.5 Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Platform lock-in** — CMUX is macOS-only | MEDIUM | Protocol abstraction; tmux binding for Linux; null binding for CI |
| **Maturity** — CMUX is ~2 months old; API may change | LOW | Protocol abstraction isolates Momentum from API changes; only the binding adapter needs updating |
| **Adoption** — not all developers will use CMUX | LOW | Optional by design; null binding is default; no workflow changes needed |
| **Maintenance burden** | LOW | Binding is small and isolated; Epic 7 protocols carry the complexity |
| **Feature dependency** — cmuxlayer has only 10 tools | LOW | 10 tools cover the core operations (pane management, I/O, notifications); sufficient for Momentum's needs |

### 5.6 Note on Skill Readiness

AVFL validation identified that several Momentum skills referenced as potential integration points (momentum-code-reviewer, momentum-architecture-guard, momentum-upstream-fix, momentum-vfl) are currently stubs with no workflow logic. CMUX integration should target implemented skills only — primarily `momentum-dev` (the worktree-based story development workflow) and the Impetus orchestrator (`momentum`).

---

## 6. Recommendations and Next Steps

### 6.1 Strategic Recommendation

**Yes, integrate CMUX — but only as an Epic 7 protocol binding, never as a dependency.**

CMUX provides genuine value for cross-repo visibility and process monitoring that Claude Code cannot natively provide. The anti-pattern (using CMUX for orchestration) is well-understood and should be documented as a Momentum practice anti-pattern.

### 6.2 Immediate Actions (Pre-Epic 7)

- **This research document** serves as the CMUX landscape reference
- Add `terminal-multiplexer` to the Epic 7 protocol type registry in architectural planning
- Add anti-pattern documentation: "Do not use CMUX for agent orchestration; use subagents"
- No code changes needed

### 6.3 Epic 7 Actions

- Define `terminal-multiplexer` protocol contract
- Implement CMUX binding (reference implementation)
- Implement tmux binding (cross-platform alternative)
- Implement null binding (default)

### 6.4 Post-Epic 7 Exploration

- Worktree-to-tab automation in `momentum-dev`
- Process monitoring skill for simulator feedback loops
- Sprint dashboard integration via CMUX sidebar
- Hook-to-notification bridge (PostToolUse → `cmux notify`)

---

## 7. Research Methodology and Sources

### 7.1 Methodology

1. **Initial research** — Two parallel agents: one exploring Momentum's architecture, one conducting web research on CMUX
2. **AVFL Gate 1** — Adversarial validation on both raw research outputs (skepticism 7-8). Caught: fabricated tool count (80+ → 10), wrong browser engine (Chromium → WebKit), incorrect Amux architecture, stale Epic 1 status, speculative Epic 7 syntax
3. **Verification pass** — Targeted web searches to confirm/deny 10 highest-priority claims. 9/10 confirmed, 1 partially confirmed with corrections
4. **Document consolidation** — Custom section structure following Momentum research conventions
5. **AVFL Gate 2** — Light (2-lens) validation on consolidated document (pending)

### 7.2 Source Registry

**Primary Sources (verified):**

| Source | URL | Accessed | Confidence |
|--------|-----|----------|------------|
| manaflow-ai/cmux GitHub | github.com/manaflow-ai/cmux | 2026-03-22 | HIGH |
| cmux.com official site | cmux.com | 2026-03-22 | HIGH |
| cmuxlayer on Glama | glama.ai/mcp/servers/EtanHey/cmuxlayer | 2026-03-22 | HIGH |
| bounds.dev cmux skill | github.com/boundsj/agent-skills/blob/main/cmux/SKILL.md | 2026-03-22 | HIGH |
| bounds.dev blog post | bounds.dev/posts/teaching-claude-code-to-drive-cmux/ | 2026-03-22 | HIGH |
| setup-cmux gist | gist.github.com/jbasdf/2f31c6fc12dea4f739543ad41f564c86 | 2026-03-22 | HIGH |
| Amux repo | github.com/mixpeek/amux | 2026-03-22 | HIGH |
| Coder Mux repo | github.com/coder/mux | 2026-03-22 | HIGH |
| dmux repo | github.com/standardagents/dmux | 2026-03-22 | HIGH |
| cmux-agent-mcp on Glama | glama.ai/mcp/servers/multiagentcognition/cmux-agent-mcp | 2026-03-22 | MODERATE |

**Community Sources (spot-checked):**

| Source | URL | Verified |
|--------|-----|----------|
| Better Stack CMUX guide | betterstack.com/community/guides/ai/cmux-terminal/ | YES |
| Medium tmux setup guide | ksingh7.medium.com/watch-claude-code-agents-work-side-by-side-... | YES |
| cmux vs tmux comparison | soloterm.com/cmux-vs-tmux | YES |

**Unverified Sources (from initial research, not independently confirmed):**

Articles from: claudefa.st, clauderc.com, vibecoding.app, rentierdigital.xyz, mejba.me, Medium/@abhiyan5588, cuttlesoft.com, DEV Community. These were flagged by AVFL as hallucination-risk. The 4 spot-checked articles above were confirmed; remaining articles may or may not exist.

### 7.3 Limitations

- CMUX is ~2 months old; community patterns are nascent and evolving rapidly
- macOS-only limits the generalizability of findings
- The MCP integration ecosystem is actively growing; tool counts may change
- No large-scale adoption data available; star counts are a proxy for interest, not production usage
- AVFL flagged that the initial web research agent fabricated specific metrics (tool counts, line counts) — all metrics in this document have been verified against primary sources

---

**Technical Research Completion Date:** 2026-03-22
**Source Verification:** All facts verified against primary sources unless marked otherwise
**AVFL Validation:** Gate 1 complete (raw research). Gate 2 pending (consolidated document).
