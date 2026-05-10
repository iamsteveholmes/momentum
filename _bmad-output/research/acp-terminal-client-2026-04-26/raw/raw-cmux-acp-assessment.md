---
source: session research synthesis
fetched: 2026-04-26
confidence: high
---

# Raw: CMUX as ACP Client — Assessment

## Can CMUX Be Used as an ACP Client?

**Directly: No.** CMUX is a terminal multiplexer, not a protocol client.

CMUX provides:
- Split-pane terminal layout
- Integrated WebKit browser surfaces
- Notification/status layer
- Agent skill system (`cmux` and `cmux-browser` skills)
- MCP integration

CMUX does NOT provide:
- ACP/A2A protocol support
- JSON-RPC stdio communication with agents
- Agent session management

## Possible Indirect Paths

### 1. CMUX Browser Surface + A2A Inspector
- Use CMUX's browser surfaces to load the `a2a-inspector` web UI
- Still a web UI, just inside a terminal multiplexer
- **Verdict: Hack, not a real solution**

### 2. CMUX + Goose CLI + acp-mcp Adapter
- Run `uvx acp-mcp <acp-server-url>` as MCP server
- Configure Goose CLI to use it as an MCP extension
- Goose becomes a terminal-native proxy to ACP/A2A agents
- **Verdict: Functional but indirect — Goose is the client, CMUX is just the host**

### 3. CMUX as Host for a Rust ACP TUI
- Build `acp-tui` as a standalone Rust TUI
- Run it inside a CMUX pane alongside other agent terminals
- CMUX provides the multiplexing; `acp-tui` provides the ACP client
- **Verdict: Best fit — CMUX is the environment, not the client**

## Conclusion

CMUX is not an ACP client and shouldn't be. It's a terminal multiplexer — the right role is hosting an ACP TUI client as a first-class pane in its layout system. The TUI client itself should be a separate Rust application using the `agent-client-protocol` crate.
