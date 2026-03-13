# Technical Research: Agent Client Protocol (ACP)

**Date:** 2026-03-13
**Status:** Complete
**Context:** Implications for Momentum's Agent Skills portability strategy

## Summary

ACP is an open standard (Apache 2.0) by JetBrains and Zed that standardizes communication between code editors and AI coding agents. It is analogous to LSP but for AI agents. ACP operates at the transport/integration layer — below the skills layer where Momentum operates. Skills are invisible to ACP and require zero adaptation.

## The Three Standards Stack

| Standard | Layer | What It Does |
|---|---|---|
| **Agent Skills** | Procedures | Tells the agent *what to do and how* |
| **MCP** | Capabilities | Connects agents to *tools and data* |
| **ACP** | Integration | Connects agents to *editors* |

These are complementary. When Claude Code runs inside JetBrains via ACP: ACP handles the editor-agent connection, MCP servers are passed through ACP's session setup, and Agent Skills are read by the agent from its own skill directories — invisible to ACP.

## Protocol Details

- **Spec:** [agentclientprotocol.com](https://agentclientprotocol.com), [GitHub](https://github.com/agentclientprotocol/agent-client-protocol)
- **Version:** v0.11.2 (March 11, 2026), 33 releases, pre-1.0
- **License:** Apache 2.0
- **Governance:** Joint JetBrains + Zed, targeting independent foundation. RFD-driven evolution. Biweekly core maintainer meetings.
- **Transport:** JSON-RPC over stdio (HTTP/WebSocket planned for remote agents)
- **SDKs:** Python, TypeScript, Kotlin, Java, Rust

## Adoption

**Editors:** JetBrains IDEs (2025.3+), Zed, Neovim, Emacs, marimo, Eclipse (prototype)

**Agents in registry (45+):** Claude Code, GitHub Copilot CLI, Gemini CLI, Junie, Goose, Auggie, Kimi CLI, Cline, Cursor, Codex CLI, Amp, Kiro (AWS), OpenCode, Qwen Code

**Corporate backers:** JetBrains, Zed, Google, GitHub/Microsoft, Docker, Block, Augment Code, Moonshot AI, Alibaba, AWS

## Skills Portability Through ACP

Skills are agent-internal. ACP has no concept of skills — it only knows about sessions, prompts, tool calls, file operations, and terminal commands. A skill written to the Agent Skills standard works identically whether the agent runs standalone or through ACP.

Junie CLI confirms this: it reads `.junie/skills/` and auto-detects/imports from `.claude/skills/`, `.cursor/skills/`, `.codex/skills/`.

## Implications for Momentum

1. **No ACP-specific work required** — skills are invisible to the protocol
2. **Strategy validated** — portable Agent Skills + Claude Code enhancements works across the entire ecosystem
3. **Expanded reach** — ACP means Momentum skills reach developers in JetBrains IDEs via their agent of choice
4. **Do not depend on IDE MCP tools** — IntelliJ's built-in MCP server is powerful but IDE-specific
5. **Test against Junie** — good portability validation target beyond Claude Code

## Timeline

| Date | Event |
|---|---|
| August 2025 | ACP formalized with Zed's "Bring Your Own Agent" |
| October 2025 | JetBrains joins ACP collaboration |
| December 2025 | ACP support ships in JetBrains IDEs 2025.3+ |
| January 2026 | ACP Agent Registry launches; Copilot CLI ACP preview |
| March 2026 | v0.11.2; 45+ agents; Junie CLI beta |
