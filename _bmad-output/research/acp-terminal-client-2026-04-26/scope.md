---
research_date: 2026-04-26
topic: ACP (Agent Client Protocol) terminal-based client — protocol landscape, Rust viability, and Zed's SDK
researcher: goose (session research)
status: complete
---

# Research Scope: ACP Terminal Client

## Question

Is there a way to use CMUX as an ACP client? If not, what are the options for building a terminal-based ACP client, and is Rust a good candidate?

## Sub-questions

1. What protocols exist under the "ACP" name, and which one does Zed use?
2. What SDKs and libraries exist for each ACP variant?
3. Can CMUX serve as an ACP client directly?
4. Is Rust viable for building an ACP TUI client?
5. What does Zed's Rust ACP SDK actually provide?

## Sources consulted

- https://agentclientprotocol.com/ (Zed's ACP — Agent Client Protocol)
- https://agentcommunicationprotocol.dev/ (IBM/BeeAI's ACP — Agent Communication Protocol, now archived → A2A)
- https://github.com/agentclientprotocol/agent-client-protocol
- https://github.com/agentclientprotocol/rust-sdk
- https://crates.io/crates/agent-client-protocol
- https://github.com/i-am-bee/acp (archived)
- https://github.com/i-am-bee/acp-mcp
- https://github.com/a2aproject/a2a (Google A2A, now Linux Foundation)
- https://github.com/a2aproject/a2a-go
- https://github.com/a2aproject/a2a-rs
- https://github.com/qntx/ra2a (community A2A Rust crate)
- https://github.com/xenodium/acp.el (Emacs ACP client)
- https://github.com/ratatui/ratatui
- https://zed.dev/blog/zed-ai-agent (Zed ACP announcement)
- https://zed.dev/blog/acp-claude-code (Claude Code ACP integration)
- https://zed.dev/blog/jetbrains-acp (JetBrains ACP announcement)

## Deliverables

- `final/acp-terminal-client-final-2026-04-26.md` — synthesis document
