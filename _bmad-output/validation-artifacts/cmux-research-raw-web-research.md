# Raw Research: CMUX Web Research (February–March 2026)

## Source Agent: Explore agent — Web research on CMUX + Claude Code
## Purpose: Map the CMUX ecosystem, integration patterns, community usage, and alternatives

> **AVFL Validation Applied (2026-03-22).** This document has been through an adversarial validation pass. Claims flagged `[UNVERIFIED]` or `[VERIFY]` require direct confirmation before use in downstream artifacts. No source URLs were provided by the research agent — all claims should be traced to primary sources before citation. See Section 10 for adjusted confidence levels.

---

## 1. What is CMUX?

CMUX is a native macOS terminal application launched in February 2026, specifically designed for orchestrating multiple AI coding agents. It is a completely independent, native macOS app written in Swift and using AppKit — not a tmux fork or clone.

**Key characteristics:**
- Built on Ghostty's libghostty rendering engine for GPU-accelerated terminal rendering
- Launched February 2026, reportedly hit #2 on Hacker News and gained 7,700+ GitHub stars in first month [UNVERIFIED — exact metrics need confirmation from GitHub/HN directly]
- Free, open-source (AGPL-3.0-only), and always will be
- Supports Ghostty configuration compatibility (themes, fonts, colors migrate seamlessly)

**Who built it:** Multiple sources reference manaflow-ai as a primary source, with repositories at `github.com/manaflow-ai/cmux`, though there are also references to `github.com/craigsc/cmux` and others, suggesting either multiple implementations or community contributions. [UNRESOLVED — canonical repo and authorship unclear; feature claims in Sections 2–6 may not all apply to the same implementation. Verify which repo is canonical before relying on specific feature claims.]

## 2. Core Features

**UI Components:**
- Vertical sidebar tabs showing git branch, linked PR status/number, working directory, listening ports, latest notification text per workspace
- Split panes for isolating parallel agent tasks
- GPU-accelerated rendering via libghostty — stays smooth even with 5+ agents dumping output simultaneously
- Embedded browser with scriptable API for form-filling, element interaction, JS evaluation, and accessibility tree snapshots [VERIFY — claimed as "Chromium-based" but a native Swift/AppKit app would more typically use WKWebView/WebKit; rendering engine needs confirmation]
- Notification system with visual rings on tabs, unread badges, notification popovers, and macOS desktop notifications
- Socket API for programmatic control via JSON messages over Unix socket
- Session management with window/workspace/pane/surface/panel hierarchy

**Works with multiple agents:** Claude Code, Codex, Aider, Gemini CLI, Cline, Cursor Agent, Goose, and any CLI tool. [PARTIALLY VERIFIED — Claude Code, Codex, Aider, Gemini CLI, Cline, Cursor Agent, and Goose are known tools. "OpenCode", "Kiro", and "Amp" could not be independently verified and may be fabricated or very new/niche — verify before citing.]

## 3. MCP Integration & Server Support

**Primary MCP Servers:**

1. **cmuxlayer** (Glama MCP Hosting)
   - Serves as terminal multiplexer MCP server for orchestrating parallel AI agents
   - Provides a large set of tools for workspace management, pane manipulation, cross-agent communication [UNVERIFIED — "80+" is a suspiciously round number; verify against actual MCP server tool list]
   - Tools include: `send_input`, `read_screen`, `spawn_agent`, `stop_agent`, workspace management commands
   - Returns raw terminal text + structured parsed agent metadata for common CLI agents
   - Supports Claude Channels with `CMUXLAYER_ENABLE_CLAUDE_CHANNELS=1`

2. **cmux-agent-mcp** (Glama)
   - Programmable terminal control plane for multi-agent AI workflows
   - Remote-controllable terminal multiplexer

3. **terminal-controller-mcp** (general purpose terminal MCP)

**Terminal Control Protocol:**
- Structured JSON messages over Unix socket (typed, versioned, self-describing)
- Command categories: workspace management, pane/surface management, interaction (send text/key presses), browser control, feedback (notifications, status, progress)
- Detection via environment variables: `CMUX_WORKSPACE_ID`, `CMUX_SURFACE_ID`, `CMUX_SOCKET_PATH`

## 4. Notification & Hook System

- **OSC escape sequences** (OSC 9/99/777) — RXVT protocol with title/body, Kitty protocol
- **CLI command**: `cmux notify --title "Title" --body "Message"`
- **Claude Code hooks** — wire into agent hooks for "Stop" and "PostToolUse" event types
- Visual indicators: green (complete), yellow (waiting for input), red (errors)

## 5. Claude Code Skills & Workflow Integration

**setup-cmux Skill** (GitHub Gist by jbasdf)
- Configures cmux terminal multiplexer workspaces for Claude Code projects
- Generates `.vscode/terminals.json` for workspace setup
- Creates organized workspaces:
  - **AI Workflow**: 8 numbered step tabs (plan-stories → plan-sweep → review-open-prs → fix-pr-issues → merge-approved-prs → cleanup-merged → docs-maintain → status) plus console, reminder, plans tabs
  - **App workspace**: Application servers, database, tests (configured by tech stack)
  - **Development workspace**: Multiple Claude sessions + console
- Teaches agents topology awareness (window > workspace > pane > surface hierarchy)
- Updates project CLAUDE.md with Terminal Interaction section

**bounds.dev cmux Skill** (GitHub boundsj/agent-skills)
- Teaches agents to detect cmux environment (check `CMUX_WORKSPACE_ID`, etc.)
- Use `cmux set-progress` and `cmux notify` for progress reporting
- Open URLs in splits, interact with embedded browser
- Respect surface ownership (don't send input to surfaces user is typing in)
- No new protocol needed — just documentation of existing CLI patterns

**Key principle:** Environment awareness — agents that detect `CMUX_WORKSPACE_ID` can proactively split panes, report progress, and orchestrate their own terminal layout.

## 6. Cross-Repository & Workspace Management

- **Workspace** = isolated development environment backed by a git worktree
- **Project** = git repository containing zero or more workspaces
- Each workspace has independent filesystem tree (separate branch)
- Sidebar shows richer context: PR links, listening ports, git branches, working directories across all panes
- One orchestrator agent spawns, monitors, communicates with AI agents across multiple projects
- Different plans orchestrated to different agents in single call

## 7. CMUX vs tmux Comparison

| Dimension | CMUX (2026) | tmux (2007+) |
|-----------|-------------|--------------|
| Platform | macOS only | macOS, Linux, BSD, Solaris |
| Rendering | GPU-accelerated (libghostty) | Standard terminal |
| Agent optimization | Purpose-built | Community plugins |
| Session persistence | No restore on relaunch yet | Detach/reattach survives SSH disconnects |
| Visual feedback | Sidebar tabs, notification rings | Minimal native |
| Maturity | ~6 weeks old | 20 years battle-tested |

## 8. Alternatives

**Amux** (mixpeek/amux)
- tmux-based Claude Code agent multiplexer
- Run dozens of parallel AI coding agents unattended
- Self-healing watchdog, shared kanban board, agent-to-agent orchestration
- Reportedly a single large Python file with inline HTML/CSS/JS [UNVERIFIED — "23,000-line" is suspiciously precise; verify against actual repo]
- Web dashboard: session cards, live terminal peek, file explorer
- MIT + Commons Clause license

**Coder Mux** (coder/mux)
- Desktop & browser app for isolated, parallel agentic development
- Electron + React for macOS, Linux, Windows
- Custom agent loop inspired by Claude Code
- AGPL license

**dmux** (standardagents/dmux)
- Dev agent multiplexer for git worktrees and coding agents

## 9. Recent Articles & Resources (Feb-Mar 2026)

> **AVFL WARNING: HIGH HALLUCINATION RISK.** Web research agents routinely fabricate article titles, author names, and blog domains. Every entry below lacks a verifiable URL. Treat all titles and attributions as unverified until confirmed by direct web lookup. Several domains (claudefa.st, clauderc.com, vibecoding.app, rentierdigital.xyz, mejba.me, soloterm.com) could not be independently verified and may be fabricated.

### March 2026
- Watch Claude Code Agents Work Side by Side: A tmux Setup Guide (Medium, Karan Singh) [UNVERIFIED]
- cmux Review (2026): macOS Terminal for AI Coding Agents (vibecoding.app) [UNVERIFIED]
- Agentmaxxing: Run Multiple AI Agents in Parallel (vibecoding.app) [UNVERIFIED]
- Terminal Evolution 2026: Why AI Agents Changed Everything (rentierdigital.xyz) [UNVERIFIED]
- CMUX Terminal Turned My Mac Into an Agent Command Center (mejba.me) [UNVERIFIED]

### February 2026
- Claude Code Remote Control: Complete Setup Guide (claudefa.st) [UNVERIFIED]
- Why We Built Claude Remote on tmux (clauderc.com) [UNVERIFIED]
- I Turned My Phone Into a Claude Code Terminal (Medium, Abhiyan Khanal) [UNVERIFIED]
- Setting Up Claude Code Agent Teams on macOS (cuttlesoft.com) [UNVERIFIED]

### Technical Guides
- Teaching Coding Agents to Drive cmux (bounds.dev) [UNVERIFIED]
- cmux: Native macOS Terminal for AI Coding Agents (Better Stack) [UNVERIFIED]
- cmux vs tmux — Agent Terminal vs Terminal Multiplexer (soloterm.com) [UNVERIFIED]
- Calyx vs cmux: Choosing the Right Ghostty-Based Terminal (DEV Community) [UNVERIFIED]

## 10. Confidence Assessment

> **AVFL NOTE:** Confidence levels below have been adjusted from the original research agent output. The original assessment over-rated several claims as "Very High" when the underlying evidence was unverifiable metrics or potentially fabricated sources. Confidence should reflect verifiability, not just source count.

**High Confidence (Structurally consistent across multiple references):**
- CMUX is a native macOS terminal built on Ghostty's libghostty
- Launched February 2026
- Free, open-source (AGPL-3.0)
- Supports parallel AI agents with notification system
- Has MCP integration (cmuxlayer, cmux-agent-mcp servers)

**Moderate Confidence (Referenced in blogs/skills but not independently verified):**
- Rapid adoption and high GitHub star count [exact numbers unverified]
- setup-cmux skill exists and configures workspaces
- bounds.dev has published skill teaching agents to drive cmux
- Amux exists as tmux-based alternative for parallel agents

**Low Confidence (Needs direct verification):**
- Exact authorship/organization (multiple GitHub repos referenced, unclear canonical source)
- npm `@coder/cmux` package's relationship to manaflow-ai cmux (may be different implementations)
- Complete feature list (new features added regularly post-launch)
- All article titles, author names, and blog domains in Section 9
- Exact metrics: star counts, HN ranking, tool counts, line counts
- Agent compatibility for lesser-known tools (OpenCode, Kiro, Amp)
- Browser engine claim (Chromium vs. WebKit)

**Verification priority:** Before using this research in any downstream artifact, confirm (1) the canonical GitHub repo, (2) actual star count, (3) browser engine, and (4) at least 3 article URLs from Section 9.
