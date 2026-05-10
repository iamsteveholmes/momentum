---
source: agentcommunicationprotocol.dev
fetched: 2026-04-26
confidence: high
note: This protocol (IBM/BeeAI ACP) is now archived and merged into Google A2A. Not the same as Zed's ACP.
---

# Raw: IBM/BeeAI ACP — Agent Communication Protocol

## Status: ARCHIVED (August 2025) → merged into A2A under Linux Foundation

## Architecture

ACP (Agent Communication Protocol) provides a standardized interface for agent communication:
- **ACP Client**: makes requests to an ACP server
- **ACP Server**: hosts one or more ACP agents, exposes REST interface over HTTP

Patterns supported:
1. Basic single-agent (client → server → agent)
2. Multi-agent single server
3. Distributed multi-server
4. Advanced multi-agent orchestration (router pattern)

## MCP Adapter

The `acp-mcp` adapter bridges ACP → MCP:
- Exposes ACP agents as MCP resources and tools
- Allows MCP clients to discover and run ACP agents
- Transport: stdio
- Run: `uvx acp-mcp <acp-server-url>` or `docker run ghcr.io/i-am-bee/acp-mcp`

## Key Distinction from Zed's ACP

| | IBM ACP (this) | Zed ACP |
|---|---|---|
| Full name | Agent Communication Protocol | Agent Client Protocol |
| Purpose | Agent ↔ Agent | Client ↔ Agent (editor ↔ agent) |
| Transport | REST over HTTP | JSON-RPC over stdio |
| SDKs | Python, TypeScript | Rust, Kotlin, Java, Python, TS |
| Status | Archived → A2A | Active, growing |
