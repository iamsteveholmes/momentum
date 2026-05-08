---
source: web research synthesis
fetched: 2026-04-26
confidence: high
---

# Raw: Rust TUI Viability for ACP Client

## The Stack

| Layer | Rust Option | Maturity | Notes |
|-------|-------------|----------|-------|
| ACP SDK | `agent-client-protocol` crate | ⭐⭐⭐⭐⭐ | **Official**, powers Zed itself |
| A2A SDK | `ra2a` | ⭐⭐⭐⭐ | Community, full v1.0 spec |
| HTTP Client | `reqwest` | ⭐⭐⭐⭐⭐ | Industry standard |
| Async Runtime | `tokio` | ⭐⭐⭐⭐⭐ | Default choice |
| TUI Framework | `ratatui` (20.1k stars) | ⭐⭐⭐⭐⭐ | Undisputed king of Rust TUI |
| Terminal Backend | `crossterm` | ⭐⭐⭐⭐⭐ | Cross-platform, bundled with ratatui |
| Markdown Rendering | `pulldown-cmark` | ⭐⭐⭐ | Needed for agent markdown output |
| SSE Parsing | `reqwest` + `eventsource-stream` | ⭐⭐⭐ | For A2A streaming |
| Serialization | `serde` + `serde_json` | ⭐⭐⭐⭐⭐ | JSON-RPC → serde is perfect |

## Where Rust Shines

1. **ACP's stdio transport is a natural fit** — spawn agent subprocess, pipe JSON-RPC over stdin/stdout, no HTTP needed
2. **Single binary distribution** — `cargo install acp-tui`, no runtime needed
3. **Smooth streaming** — no GC pauses, efficient rendering for token-by-token agent output
4. **Official ACP SDK** — `agent-client-protocol` crate is production-grade, used by Zed

## Where Rust Adds Friction

1. **TUI development is slower** — ratatui is a widget framework, not a pre-built chat UI. You build scrollable history, text input, markdown rendering from scratch
2. **Compile times** — slower iteration than Python/Textual
3. **No pre-existing chat TUI template** for ACP — you're building the application layer

## Rust vs Python vs Go

| Criterion | Rust | Python | Go |
|-----------|------|--------|-----|
| ACP SDK | Official ✅ | Official ✅ | Community |
| TUI Framework | ratatui (best-in-class) | textual (excellent) | bubbletea (excellent) |
| Distribution | Single binary ✅ | Needs Python + venv ❌ | Single binary ✅ |
| Streaming Perf | Best (no GC) ✅ | Good | Good |
| Dev Speed | Slowest | Fastest ✅ | Middle |

## Recommended Architecture

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
│   │   ├── client.rs     # agent-client-protocol client wrapper
│   │   ├── transport.rs  # stdio subprocess management
│   │   └── handler.rs    # Handle incoming agent requests (fs, permissions)
│   ├── event.rs          # Terminal events → app events
│   └── config.rs         # ~/.config/acp-tui/config.toml
```

Key pattern: tokio channel bridge

```
ACP Agent subprocess
    │
    ▼ (JSON-RPC over stdio)
agent-client-protocol crate ──► tokio::mpsc ──► App State ──► Ratatui Render
    │                            (events)       (update)        (draw)
    │
    └── Streaming tokens ──► tokio::mpsc ──► incremental UI updates
```
