---
research_date: 2026-03-30
agent_focus: CMUX capabilities and architecture in Claude Code agentic workflows
sources_consulted:
  - https://github.com/manaflow-ai/cmux
  - https://cmux.com/
  - https://www.mintlify.com/manaflow-ai/cmux/introduction
  - https://betterstack.com/community/guides/ai/cmux-terminal/
  - https://agmazon.com/blog/articles/technology/202603/cmux-terminal-ai-guide-en.html
  - https://zench-aine.io/en/media/cmux-ide-vol3-official-skills
  - https://github.com/boundsj/agent-skills/blob/main/cmux/SKILL.md
  - https://glama.ai/mcp/servers/multiagentcognition/cmux-agent-mcp
  - https://lobehub.com/skills/manaflow-ai-manaflow-cmux
  - https://www.claude-hub.com/resource/github-cli-manaflow-ai-cmux-cmux/
  - https://skillsllm.com/skill/cmux
search_queries_used:
  - "CMUX Claude Code terminal multiplexer 2025 2026"
  - "Claude Code browser pane multiplexer agentic workflow"
  - "cmux manaflow-ai browser MCP tools accessibility tree screenshot agent"
  - "cmux agent skills SKILL.md Claude Code cmux-browser skill"
  - "cmux iOS simulator Android emulator desktop app support 2025 2026"
  - '"cmux" "iOS" OR "Android" OR "simulator" OR "emulator" site:github.com OR site:cmux.com'
last_verified: 2026-03-30
---

# CMUX: Capabilities Research Report

## Executive Summary

CMUX is a real, actively maintained open-source project: a native macOS terminal application purpose-built for AI coding agent orchestration. It is not a tmux wrapper or an Electron app — it is a Swift/AppKit application using libghostty for GPU-accelerated terminal rendering. Its defining features are a split-pane layout system, an integrated WebKit browser with a full scriptable CLI API, and a notification/status layer for agent feedback. It has a Claude Code skill (`cmux` and `cmux-browser`) and a third-party MCP server (`cmux-agent-mcp`). It has no story for iOS Simulator, Android Emulator, or desktop (native macOS app) targets — its browser integration is WebKit-based and targets web dev servers only.

---

## 1. What Is CMUX?

**Confidence: High**

CMUX (stylized `cmux`) is an open-source, native macOS terminal application published by [manaflow-ai](https://github.com/manaflow-ai/cmux). The primary repository is `github.com/manaflow-ai/cmux`. A marketing/docs site exists at `cmux.com` with documentation hosted at mintlify (`mintlify.com/manaflow-ai/cmux`).

- **License**: AGPL (free, open source)
- **Platform**: macOS 14.0+ only (Apple Silicon and Intel)
- **Language**: Swift + AppKit (not Electron, not Tauri)
- **Rendering engine**: libghostty (same GPU-accelerated engine as the Ghostty terminal)
- **Config compatibility**: Reads `~/.config/ghostty/config` for fonts, themes, colors
- **Distribution**: DMG download or Homebrew, with Sparkle auto-updates

The project self-describes as "a primitive, not a solution" — it provides composable building blocks (terminal, browser, notifications, workspaces, splits, tabs, CLI) and explicitly leaves workflow design to the developer or agent.

The name "CMUX" in the question's context directly refers to this tool. There is a separate, older project at `github.com/craigsc/cmux` described as "tmux for Claude Code" but it is unrelated and minimal. The canonical CMUX for agentic workflows is `manaflow-ai/cmux`.

---

## 2. Core Capabilities

**Confidence: High**

CMUX uses a four-level hierarchy for all layout management:

```
Window → Workspace (sidebar tab) → Pane (split region) → Surface (terminal tab or browser)
```

Agents reference these levels using short notation: `workspace:1`, `pane:1`, `surface:2`.

### Terminal & Layout

- **Vertical tab sidebar**: Shows git branch, PR status/number, working directory, listening ports, and latest agent notification text per workspace
- **Split panes**: Horizontal and vertical splits via the Bonsplit layout system; panes can be resized, swapped, merged
- **Multiple surfaces per pane**: Each pane can have multiple terminal tabs ("surfaces")
- **Workspaces**: Isolated environments for parallel tasks in different directories
- **Keystroke injection**: Send text and special keys to any surface programmatically

### Agent Notification System

- Blue ring indicators flash around panes when an agent needs attention
- Notification panel (Cmd+I) consolidates all pending alerts with title/subtitle/body
- Desktop notifications (suppressed when window is focused)
- OSC terminal sequence support (9/99/777) for agent-generated notifications
- Sidebar "status pills" with icons, hex colors, and custom labels
- Progress bars (0.0–1.0) with labels
- Structured log entries with info/success/warning/error levels

### Multi-Agent Orchestration

- Run Claude Code, Codex CLI, Gemini CLI, OpenCode, Kiro, Aider, and any CLI tool in parallel
- Each workspace/pane can host an independent agent
- Agents can read terminal output from other surfaces (`cmux read-screen`)
- One agent can orchestrate others by injecting prompts via `cmux send`

---

## 3. Browser Integration

**Confidence: High**

The browser pane is a first-class citizen in CMUX. It is a **WebKit-based embedded browser** (same rendering engine as Safari) that can be split alongside terminal panes. The scriptable API is "ported from agent-browser."

### How It Works

The browser is a surface type within the standard pane hierarchy. Agents create a browser surface, then drive it through the `cmux browser <surface> <subcommand>` CLI pattern. There is no external Playwright process — the browser runs inside the CMUX process itself using WebKit.

**Known limitation**: The URL cannot be reliably set at surface creation time (`open-split --url` is unreliable). The recommended pattern is: create the split first, pause briefly, then navigate separately.

### What the Agent Can See

- **Accessibility tree snapshot**: `cmux browser <surface> snapshot` returns a text-based DOM representation with compact element references (e1, e2, e3...) assigned to every interactive element. No CSS selector guessing required.
- **Page text**: `cmux browser <surface> get text` extracts visible text content
- **Full HTML**: `cmux browser <surface> get html` returns page HTML
- **Element properties**: value, attribute values, bounding box, computed styles, visibility, enabled state, checked state
- **Console logs and page errors**: `cmux browser <surface> console list` / `errors list`
- **Network request history**: `cmux browser <surface> network requests`
- **Current URL and page title**
- **Screenshots**: `cmux browser <surface> screenshot [--out <path>]` captures the browser pane as an image

### What the Agent Can Do

**Navigation**:
- Navigate to URLs, go back/forward, reload
- Wait for selectors, text content, URL changes, load states (domcontentloaded, load, networkidle), or JavaScript conditions

**Element interaction**:
- Click, double-click, hover, focus, blur by selector or element reference
- Scroll page or scroll element into view
- Type (append) or fill (clear then fill) form inputs
- Check/uncheck checkboxes, select dropdown values
- Press keyboard keys (Enter, Tab, Escape, etc.)

**Finding elements**:
- By ARIA role and name
- By text content (exact or fuzzy)
- By label, placeholder, or test ID
- Positional (first, nth)

**JavaScript**:
- `cmux browser <surface> eval "js_code"` executes arbitrary JavaScript in the page context

**Storage/state**:
- Get/set cookies (with domain filtering)
- Get/set localStorage

**Emulation** (WebKit-only subset):
- `viewport <width> <height>` — resize viewport
- `offline true|false` — toggle offline mode
- `geolocation <lat> <lng>` — set location
- `network route <pattern>` — mock/abort network requests

**WebKit constraint**: Chrome DevTools Protocol features — viewport emulation beyond basic resize, network interception screencast recording — are **not supported**. These return `not_supported` from WebKit.

---

## 4. Tool Surface: What Is Exposed to Agents

**Confidence: High**

CMUX provides two tool surfaces: a CLI/skill layer and an MCP server layer.

### A. CLI + Agent Skills (Native)

Three official Agent Skills are published in the CMUX repository (`skills/` directory) and follow the universal Agent Skills standard. Agents install them to `~/.claude/skills/` or `.claude/skills/`.

| Skill | Purpose |
|---|---|
| `cmux` | Topology control — pane splitting, workspace management, surface navigation, status/progress reporting |
| `cmux-browser` | Browser automation — URL loading, DOM snapshot, form interaction, screenshots |
| `cmux-markdown` | Markdown viewer — live preview pane with automatic file-change detection |

**Detection**: Agents check `CMUX_WORKSPACE_ID` environment variable to confirm they're running inside CMUX. The CLI binary is at `/Applications/cmux.app/Contents/Resources/bin/cmux` and is on PATH within CMUX terminals.

A local Momentum installation also provides `cmux` and `cmux-browser` skills (visible in the skills system-reminder).

### B. cmux-agent-mcp (Third-Party MCP Server)

A third-party MCP server (`cmux-agent-mcp`, published by `multiagentcognition`) exposes **81 MCP tools** organized into 14 categories. This is a programmatic terminal control plane enabling any MCP-compatible client to orchestrate CMUX externally.

| Category | Tool Count | Examples |
|---|---|---|
| Status & Discovery | 6 | `cmux_status`, `cmux_tree`, `cmux_find`, `cmux_screenshot` |
| Workspace Management | 7 | Create, select, rename, reorder, close workspaces |
| Window Management | 6 | Create, focus, close, rename windows |
| Surface/Tab Management | 7 | Create/move/reorder terminal and browser tabs |
| Pane Operations | 12 | Split (left/right/up/down), merge, resize, swap |
| Text I/O | 6 | `cmux_send`, `cmux_send_submit`, `cmux_read_screen`, `cmux_capture_pane` |
| Bulk Operations | 8 | `cmux_broadcast` (all panes), `cmux_read_all`, `cmux_workspace_snapshot` |
| Sidebar Metadata | 8 | Status pills, progress bars, log entries |
| Notifications | 3 | Send/list alerts |
| Browser Automation | 13 | Navigate, snapshot DOM, eval JS, click/fill/type, wait, get page data, console logs |
| High-Level Launchers | 7 | `cmux_launch_agents` (grid of N agents), `cmux_orchestrate`, `cmux_launch_mixed` |
| Session Management | 3 | Save, recover, reconcile session state |

The MCP server enables external orchestrators to spawn and manage multiple parallel agent CLIs, inject prompts into running sessions, monitor progress across agents, and automate browser interactions.

---

## 5. Architecture

**Confidence: High**

| Component | Technology |
|---|---|
| App framework | Swift + AppKit (native macOS) |
| Terminal rendering | libghostty (GPU-accelerated) |
| Browser engine | WebKit (embedded, in-process) |
| Layout system | Bonsplit (flexible split/animation) |
| IPC | Unix domain socket at `/tmp/cmux.sock` |
| Config | JSON (`cmux.json`) per-project and global; reads Ghostty config for terminal theme |
| Distribution | DMG, Homebrew, Sparkle auto-update |

**Socket access modes**: Off / cmux-processes-only / allowAll. Many AI agents run in sandboxes that block socket access to `/tmp/cmux.sock` — the security tradeoff of enabling full agent control is disabling the sandbox.

**Session restore**: Layout, working directories, scrollback, and browser history are restored after restart. Live process state (running Claude Code sessions, vim instances, tmux sessions) is **not** restored.

---

## 6. Extensibility

**Confidence: Medium**

CMUX is not described as having a formal plugin or extension marketplace. Extensibility works through:

1. **CLI + socket API**: Any process can control CMUX programmatically. New automation can be built on top of these primitives.
2. **Agent Skills standard**: New skills can be written as SKILL.md files following the universal Agent Skills format and loaded by Claude Code.
3. **`cmux.json` configuration**: Per-project and global workspace layout definitions, custom commands.
4. **OSC escape sequences**: Terminal sequences (9/99/777) allow any terminal process to send notifications into the CMUX notification system.
5. **cmux-agent-mcp**: The MCP server layer is separately maintained and can be extended by the community.

There is no documented plugin API, no extension registry, and no pane type plugin system. Adding a new pane type (e.g., one that renders an iOS Simulator) would require modifying the CMUX application itself.

---

## 7. Known Gaps and Limitations

**Confidence: High**

### Platform Gaps

| Target | Status |
|---|---|
| Web (dev server in embedded browser) | Fully supported |
| iOS Simulator | No support — no pane type, no bridge to Xcode Simulator |
| Android Emulator | No support — no pane type, no bridge to ADB/AVD |
| Native macOS/desktop app | No support — browser pane only targets web pages |
| Linux | Not supported (macOS-only app) |
| Windows | Not supported |
| Remote/cloud | Announced for Founder's Edition (cloud VMs) — not yet available |

### Technical Limitations

- **WebKit-only browser**: No Chromium. Chrome DevTools Protocol features (`not_supported` from WebKit): screencast recording, full network interception, advanced viewport emulation.
- **No live process restore**: Restarting CMUX drops all running processes (Claude Code sessions, vim, tmux) — layout restores but processes do not.
- **Sandbox conflicts**: Agents sandboxed by Claude Code cannot reach `/tmp/cmux.sock` without sandbox modifications.
- **URL creation race**: `open-split --url` is unreliable — create split first, then navigate.
- **macOS 14.0+ minimum**: Older macOS versions are not supported.
- **AGPL license**: Enterprise use may require license review.

### Capability Gaps for Non-Web Targets

The browser pane has no analog for:

- **iOS Simulator**: Would need an XPC/Accessibility bridge to `Xcode.app` simulator processes, or integration with tools like `idb`, `simctl`, or Appium XCUITest driver.
- **Android Emulator**: Would need ADB bridge, accessibility service, or Espresso/UiAutomator integration.
- **Desktop app automation**: Would need macOS Accessibility API (AXUIElement) bridge — effectively building Applescript/AT-SPI support into a pane type.

None of these exist in CMUX. They are also not on any published roadmap.

---

## 8. Community Usage and Examples

**Confidence: Medium**

CMUX launched publicly and appeared on Product Hunt (`producthunt.com/products/cmux`). It has been covered in:

- [Better Stack Community Guide](https://betterstack.com/community/guides/ai/cmux-terminal/) — comprehensive walkthrough
- [Gardenee Blog](https://agmazon.com/blog/articles/technology/202603/cmux-terminal-ai-guide-en.html) — complete guide published March 2026
- [ZenChAIne Media — Official Skills Deep Dive](https://zench-aine.io/en/media/cmux-ide-vol3-official-skills) — detailed walkthrough of the three official skills
- [Claude Hub resource listing](https://www.claude-hub.com/resource/github-cli-manaflow-ai-cmux-cmux/)
- [SkillsLLM catalog entry](https://skillsllm.com/skill/cmux)
- Community skill repos: `boundsj/agent-skills`, `hashangit/cmux-skill`, `alirezarezvani/claude-skills`
- MCP server: `multiagentcognition/cmux-agent-mcp` on Glama

**Documented workflow examples**:

- Parallel testing: Create 3 splits → run unit/integration/e2e tests simultaneously → capture results → close panels → notify
- Multi-agent code analysis: Distribute codebase analysis across multiple Claude instances, main agent collects results
- Test-driven iteration: Launch test suite in one surface, parse failures, modify code, re-run tests
- Browser automation: Navigate to dev server → snapshot DOM → interact with form elements → validate result
- Google search example (from Better Stack): open browser pane → wait for load → get DOM snapshot → type into identified input → click button

---

## 9. Confidence Summary

| Section | Confidence | Basis |
|---|---|---|
| What CMUX is | High | Primary sources: GitHub repo, official docs, multiple guides |
| Core terminal capabilities | High | Official SKILL.md, cmux.com docs, mintlify docs |
| Browser integration | High | SKILL.md command reference, WebFetch of official docs |
| Tool surface (CLI skills) | High | SKILL.md extracted verbatim; three skills confirmed |
| Tool surface (MCP server) | High | Glama MCP catalog entry with full 81-tool listing |
| Architecture | High | Multiple independent sources consistent |
| Extensibility | Medium | Inferred from design philosophy; no official plugin docs found |
| iOS/Android/desktop gaps | High | Absence confirmed across all sources; no roadmap mentions these |
| Community usage | Medium | Multiple blog posts and skill repos found; no conference talks found |

---

## 10. Implications for Agentic Engineering Workflows

CMUX solves the "agent sees running web app" problem cleanly. The WebKit browser with DOM snapshot + element refs gives a Claude Code agent genuine read/write access to a running web dev server — it can verify UI state, fill forms, click buttons, read console logs, and take screenshots without any external Playwright process.

The gap is everything else. An agent doing mobile development has no equivalent visibility surface:

- iOS Simulator output is visual — the agent cannot see it without a separate screenshot pipeline (e.g., `xcrun simctl io booted screenshot`, analyzed via vision)
- Android Emulator output is visual — similar gap
- Desktop app output is visual — similar gap

Bridging these gaps would require either: (a) extending CMUX with new pane types backed by platform accessibility APIs, or (b) composing CMUX's terminal + notification primitives with separate MCP servers that handle mobile/desktop automation (e.g., `ios-simulator-mcp`, `idb`-backed tools, Appium). CMUX's socket API and skill model are open enough to support option (b) without changes to the application itself.
