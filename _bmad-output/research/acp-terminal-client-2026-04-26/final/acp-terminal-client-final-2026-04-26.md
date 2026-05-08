---
research_date: 2026-04-26
topic: ACP terminal-based client — protocol landscape, Rust viability, Zed SDK, CMUX role
researcher: goose (session research)
status: complete
confidence: high
sources:
  - https://agentclientprotocol.com/
  - https://agentcommunicationprotocol.dev/
  - https://github.com/agentclientprotocol/agent-client-protocol
  - https://github.com/agentclientprotocol/rust-sdk
  - https://crates.io/crates/agent-client-protocol
  - https://github.com/i-am-bee/acp (archived)
  - https://github.com/i-am-bee/acp-mcp
  - https://github.com/a2aproject/a2a
  - https://github.com/qntx/ra2a
  - https://github.com/xenodium/acp.el
  - https://github.com/ratatui/ratatui
  - Zed blog posts on ACP
---

# Research Report: ACP Terminal Client

## Executive Summary

There is no off-the-shelf terminal/TUI client for any ACP variant today. However, the landscape is far more ready than it appears. The critical finding is that **"ACP" refers to two completely different protocols**, and the one that matters for a terminal client is Zed's **Agent Client Protocol** — which has an official Rust SDK, stdio transport, and is already spoken by Claude Code, Gemini CLI, Codex CLI, and GitHub Copilot CLI. CMUX cannot serve as an ACP client directly (it's a multiplexer, not a protocol client), but it would be an ideal host environment for a Rust TUI client built on the official `agent-client-protocol` crate.

---

## 1. The Two ACPs — A Critical Distinction

| | **Agent Client Protocol** (Zed) | **Agent Communication Protocol** (IBM/BeeAI) |
|---|---|---|
| **Creator** | Zed Industries + JetBrains | IBM / BeeAI |
| **GitHub** | `agentclientprotocol/agent-client-protocol` | `i-am-bee/acp` (archived Aug 2025) |
| **Purpose** | Client ↔ Agent (editor ↔ agent) | Agent ↔ Agent |
| **Analogy** | LSP for AI agents | HTTP for agents |
| **Transport** | JSON-RPC over **stdio** (local), HTTP/WS (remote) | REST over HTTP |
| **Rust SDK** | ✅ Official — `agent-client-protocol` crate | ❌ None |
| **Status** | Active, growing fast | Archived → merged into Google A2A |

**For a terminal-based human-facing client, Zed's ACP is the correct target.** It's designed for exactly the client→agent interaction pattern a TUI needs. IBM's ACP (now A2A) is agent-to-agent — the wrong layer.

### A2A (Google/Linux Foundation) — The Successor to IBM's ACP

IBM's ACP was archived and merged into Google's A2A protocol, now under the Linux Foundation:
- v1.0 released March 2026, 23.4k GitHub stars
- Transport: JSON-RPC 2.0 over HTTP(S), REST, gRPC
- Official SDKs: Python, JS/TS, Go, Java, .NET
- Community Rust SDK: `ra2a` (164 stars, full v1.0 spec, on crates.io)
- Official Rust SDK: `a2a-rs` (19 stars, very early)
- No terminal client exists

A2A remains relevant for multi-agent orchestration, but for a human-facing TUI that talks to local coding agents, Zed's ACP is the right protocol.

---

## 2. Zed's ACP — What the Rust SDK Provides

### Official Crate

```toml
[dependencies]
agent-client-protocol = "x.y.z"
```

- **Crate**: [`agent-client-protocol`](https://crates.io/crates/agent-client-protocol)
- **Repo**: [`agentclientprotocol/rust-sdk`](https://github.com/agentclientprotocol/rust-sdk)
- **Docs**: [docs.rs/agent-client-protocol](https://docs.rs/agent-client-protocol/latest/agent_client_protocol/)
- **Production use**: Powers Zed's own external agent integration

### Two Core Traits

| Trait | Purpose | For Building |
|-------|---------|-------------|
| `Agent` | Implement agent-side behavior | Agent servers (Claude Code, Gemini, etc.) |
| `Client` | Implement client-side behavior | **Client applications (TUI, editors, etc.)** |

For a TUI client, you implement the `Client` trait — handling incoming requests from the agent (file system access, permission prompts, terminal operations) and sending prompt turns.

### Example Binaries

The SDK ships with:
- `agent.rs` — example agent server
- `client.rs` — example client (the starting point for a TUI)

### Protocol Flow (What a TUI Client Must Implement)

```
1. Spawn agent subprocess (e.g., `claude-code-acp` or `gemini --experimental-acp`)
2. initialize        — capability negotiation
3. authenticate      — if required
4. session/new       — create a session
5. session/prompt    — send user message, receive streaming response
6. Handle incoming agent requests:
   - fs/read_text_file     — agent wants to read a file
   - fs/write_text_file    — agent wants to write a file
   - session/request_permission — agent asks for user approval
   - terminal/create       — agent wants terminal access
7. session/prompt    — next turn
```

---

## 3. Existing ACP Clients — Proof of Concept

| Client | Type | Language | Key Insight |
|--------|------|----------|-------------|
| **Zed** | Desktop editor | Rust (GPUI) | Production ACP client, uses the same `agent-client-protocol` crate |
| **JetBrains** | Desktop IDE | Kotlin/Java | Production, uses official JVM SDK |
| **Neovim** | Terminal editor | Lua (CodeCompanion) | Community, proves terminal editor integration works |
| **Emacs (`acp.el`)** | Terminal editor | Emacs Lisp | **145 stars, proves the TUI pattern end-to-end** |

### `acp.el` — The Reference Implementation for Terminal Clients

The Emacs `acp.el` package (github.com/xenodium/acp.el) is the closest existing analog to what a Rust TUI would do:

1. Spawns an agent as a subprocess
2. Communicates via JSON-RPC over stdio
3. Handles the standard ACP handshake
4. Handles incoming requests from the agent (fs access, permissions)
5. Renders responses in editor buffers

A Rust TUI would follow the exact same pattern, substituting `ratatui` widgets for Emacs buffers.

---

## 4. Agents That Speak ACP (Stdio)

These agents can be spawned as subprocesses and communicated with via stdio JSON-RPC:

| Agent | Command | Status |
|-------|---------|--------|
| Claude Code | `claude-code-acp` | Production |
| Gemini CLI | `gemini --experimental-acp` | Experimental |
| Codex CLI | ACP support | Available |
| GitHub Copilot CLI | ACP support | Available |
| OpenCode | ACP support | Available |

This is the target ecosystem for a TUI client — you get immediate access to all of these agents through one interface.

---

## 5. CMUX as ACP Client — Assessment

**Verdict: CMUX is not an ACP client, and shouldn't be. It's a terminal multiplexer.**

| Approach | Viable? | Verdict |
|----------|---------|---------|
| CMUX directly as ACP client | ❌ | CMUX doesn't speak ACP/A2A protocols |
| CMUX browser + A2A Inspector web UI | ⚠️ | Hack — still a web UI, just inside terminal panes |
| CMUX + Goose CLI + acp-mcp adapter | ✅ | Functional but indirect — Goose is the real client |
| CMUX as host for a Rust ACP TUI | ✅✅ | **Best fit** — CMUX provides multiplexing, TUI provides ACP |

The right relationship: **CMUX is the environment, the Rust TUI is the client.** You'd run `acp-tui` as a pane inside CMUX alongside your other agent terminals, browser surfaces, and development tools.

---

## 6. Rust Viability for ACP TUI Client

### The Stack Is Production-Ready

| Layer | Option | Maturity | Notes |
|-------|--------|----------|-------|
| **ACP SDK** | `agent-client-protocol` | ⭐⭐⭐⭐⭐ | Official, powers Zed |
| **Async Runtime** | `tokio` | ⭐⭐⭐⭐⭐ | Handles subprocess + stdio + channels |
| **TUI Framework** | `ratatui` (20.1k⭐) | ⭐⭐⭐⭐⭐ | Best-in-class Rust TUI |
| **Terminal Backend** | `crossterm` | ⭐⭐⭐⭐⭐ | Cross-platform, bundled with ratatui |
| **Serialization** | `serde` + `serde_json` | ⭐⭐⭐⭐⭐ | ACP is JSON-RPC — serde handles this natively |
| **Markdown** | `pulldown-cmark` | ⭐⭐⭐ | Agent output is markdown |

### Where Rust Wins

1. **Official ACP SDK is Rust** — the same crate that powers Zed
2. **Single binary distribution** — `cargo install acp-tui`, no runtime dependencies
3. **Stdio transport is trivial** — spawn subprocess, pipe stdin/stdout, no HTTP needed
4. **Smooth streaming** — no GC pauses for token-by-token rendering
5. **The `acp.el` pattern maps 1:1** — subprocess + stdio JSON-RPC + UI rendering

### Where Rust Adds Friction

1. **TUI development is slower** — ratatui is a widget framework, not a pre-built chat UI. You build scrollable history, text input, markdown rendering from scratch.
2. **Compile times** — slower iteration than Python/Textual for layout tweaks.
3. **No pre-existing chat TUI template** for ACP — you're building the application layer.

### Architecture

```
┌──────────────────────────────────┐
│         acp-tui (ratatui)        │
│                                  │
│  ┌──────────┐  ┌──────────────┐  │
│  │  Chat    │  │  Sessions    │  │
│  │  View    │  │  + Agents    │  │
│  │          │  │              │  │
│  └──────────┘  └──────────────┘  │
│  ┌──────────────────────────────┐│
│  │  Input Bar                   ││
│  └──────────────────────────────┘│
└──────────┬───────────────────────┘
           │ JSON-RPC over stdio
           │ (agent-client-protocol crate)
           ▼
┌──────────────────────────────────┐
│  Agent subprocess                │
│  (claude-code-acp, gemini, etc.) │
└──────────────────────────────────┘
```

```
a2a-tui/
├── Cargo.toml
├── src/
│   ├── main.rs           # Entry point, tokio + ratatui setup
│   ├── app.rs            # Application state machine
│   ├── ui/
│   │   ├── mod.rs
│   │   ├── chat.rs       # Chat view (messages, input)
│   │   ├── sidebar.rs    # Agent list, session list
│   │   ├── agent_card.rs # Agent info display
│   │   └── theme.rs      # Colors, styling
│   ├── acp/
│   │   ├── mod.rs
│   │   ├── client.rs     # agent-client-protocol Client trait impl
│   │   ├── transport.rs  # stdio subprocess management
│   │   └── handler.rs    # Handle incoming agent requests (fs, permissions)
│   ├── event.rs          # Terminal events → app events
│   └── config.rs         # ~/.config/acp-tui/config.toml
```

Key pattern: **tokio channel bridge**

```
ACP Agent subprocess
    │
    ▼ (JSON-RPC over stdio)
agent-client-protocol crate ──► tokio::mpsc ──► App State ──► Ratatui Render
    │                            (events)       (update)        (draw)
    │
    └── Streaming tokens ──► tokio::mpsc ──► incremental UI updates
```

---

## 7. Language Comparison for This Project

| Criterion | Rust | Python | Go |
|-----------|------|--------|-----|
| **ACP SDK** | ✅ Official (`agent-client-protocol`) | ✅ Official | Community |
| **TUI Framework** | ratatui (20k⭐, best-in-class) | textual (excellent) | bubbletea (excellent) |
| **Distribution** | Single binary ✅ | Needs Python + venv ❌ | Single binary ✅ |
| **Streaming Perf** | Best (no GC) ✅ | Good | Good |
| **Dev Speed** | Slowest | Fastest ✅ | Middle |
| **Community Fit** | Terminal tool devs love Rust ✅ | AI/ML ecosystem ✅ | CLI/SRE ecosystem ✅ |
| **Official SDK** | ✅ | ✅ | ❌ (ACP) / ✅ (A2A) |

**Verdict: Rust is the strongest long-term choice** given:
- The official ACP SDK is Rust
- Single-binary distribution is critical for a dev tool
- The `acp.el` pattern proves the architecture works
- The `agent-client-protocol` crate handles all protocol plumbing
- The missing piece is just the TUI application layer

---

## 8. Gaps and Opportunities

| Gap | What's Needed | Effort |
|-----|--------------|--------|
| **ACP TUI Client** | A ratatui-based interactive client — discover agents, manage sessions, chat, stream responses | Medium (SDK handles protocol; you build UI) |
| **Chat widget for ratatui** | Scrollable chat history, multiline input, markdown rendering | Medium |
| **ACP ↔ CMUX integration** | CMUX pane type or layout preset for `acp-tui` | Low (just run it in a pane) |
| **A2A → MCP bridge (v1.0)** | `acp-mcp` targets old ACP; updated A2A→MCP bridge would unlock Goose/CLI access | Medium |

---

## 9. Recommendations

### Primary: Build `acp-tui` in Rust on the Official ACP SDK

This is the highest-value path:
1. Use the `agent-client-protocol` crate for protocol handling
2. Use `ratatui` + `crossterm` for the TUI
3. Use `tokio` for async subprocess management and channel bridging
4. Target Zed's ACP (stdio JSON-RPC) — not A2A (HTTP JSON-RPC)
5. Get immediate access to Claude Code, Gemini CLI, Codex, Copilot as agent backends
6. Distribute as `cargo install acp-tui`

### Secondary: A2A Support as a Future Extension

If multi-agent orchestration becomes relevant:
- Add A2A connectivity using the `ra2a` crate
- This would allow the TUI to both talk to local agents (ACP/stdio) and remote agent networks (A2A/HTTP)
- But start with ACP — it's simpler, has the official Rust SDK, and covers the primary use case

### CMUX Role

Run `acp-tui` as a first-class pane inside CMUX alongside other development surfaces. No custom CMUX integration needed — it's just a terminal application in a pane.

---

## 10. Key References

| Resource | URL |
|----------|-----|
| ACP Spec | https://agentclientprotocol.com/ |
| ACP Rust SDK (crates.io) | https://crates.io/crates/agent-client-protocol |
| ACP Rust SDK (repo) | https://github.com/agentclientprotocol/rust-sdk |
| ACP Rust SDK (docs) | https://docs.rs/agent-client-protocol/latest/agent_client_protocol/ |
| ACP GitHub Org | https://github.com/agentclientprotocol |
| Emacs ACP Client (`acp.el`) | https://github.com/xenodium/acp.el |
| ratatui | https://github.com/ratatui/ratatui |
| A2A Protocol | https://github.com/a2aproject/a2a |
| `ra2a` (Rust A2A) | https://github.com/qntx/ra2a |
| ACP-MCP Adapter | https://github.com/i-am-bee/acp-mcp |
