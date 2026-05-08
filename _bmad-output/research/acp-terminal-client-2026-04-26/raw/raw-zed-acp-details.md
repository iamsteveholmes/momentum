---
source: web research synthesis
fetched: 2026-04-26
confidence: high
---

# Raw: Zed ACP — Agent Client Protocol Details

## What Is Zed's ACP?

Agent Client Protocol is an open protocol created by Zed Industries (with JetBrains) for **editor/client ↔ agent** communication. It's analogous to LSP but for AI agents instead of language servers.

## Protocol Characteristics

- Transport: JSON-RPC over **stdio** (local agents) or HTTP/WebSocket (remote agents)
- Handshake: `initialize` → `authenticate` → `session/new` → `session/prompt`
- Agents can make requests back to the client: `fs/read_text_file`, `session/request_permission`, terminal access
- Supports streaming responses, tool calls, file system access, terminals, agent plans

## Agents That Speak ACP

- Claude Code (`claude-code-acp`)
- Gemini CLI (`gemini --experimental-acp`)
- Codex CLI
- GitHub Copilot CLI
- OpenCode

## Existing ACP Clients

| Client | Type | Status |
|--------|------|--------|
| Zed | Desktop editor (Rust/GPUI) | Production |
| JetBrains | Desktop IDE (Kotlin/Java) | Production |
| Neovim | Terminal editor (via CodeCompanion) | Community |
| Emacs | Terminal editor (`acp.el`, 145 stars) | Community |

## Key Insight for Terminal Client

The `acp.el` Emacs package proves the pattern for a terminal-based ACP client:
1. Spawn agent as subprocess
2. Communicate via JSON-RPC over stdio
3. Handle the standard handshake
4. Handle incoming requests from agent (fs access, permissions)
5. Render responses in the UI

A Rust TUI would follow the exact same pattern with `ratatui` instead of Emacs buffers.
