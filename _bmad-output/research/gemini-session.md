---
research_date: 2026-03-30
source: Google Gemini Deep Research
session: Initial research + follow-up Q&A
last_verified: 2026-03-30
---

# Gemini Deep Research Session
## Compose Multiplatform LLM Agent Verification — March 30, 2026

## Initial Report

See: `/Users/steve/projects/momentum/docs/research/LLM Agent Compose Multiplatform Verification.md`

## Follow-up Q&A Answers

### Q1: CMP Version Conflict

**Answer:** Both agents were wrong. As of late March 2026:
- Jetpack Compose core: stable 1.10.6
- Compose Multiplatform: latest stable **1.10.3**
- CMP 1.11.0 is in Beta
- CMP 1.9.3 (cited in Gemini initial report) was an earlier feature release
- No evidence of active dual 1.8.x LTS release line

**Corrections:** Gemini initial report (1.9.3) and Agent A2 (1.8.2) both incorrect.

### Q2: Apple Claude Agent SDK in Xcode 26.3

**Answer:**
- **Official Apple product** built natively into Xcode 26.3, powered by Anthropic and OpenAI models
- **Headless/CLI:** Can be executed from terminal via `-p` flag (e.g., `claude -p`) with standard CLI options
- **URL:** `https://www.anthropic.com/news/apple-xcode-claude-agent-sdk` is real and confirmed
- **Advantages over mobile-mcp:** Deep native access to project file structure and Apple-specific frameworks (Swift Data). Can capture and verify **live Xcode Previews** (SwiftUI canvases) without compiling and booting a full iOS Simulator — closes the visual feedback loop at preview time

### Q3: JetBrains Central + ACP — Ship Status

**Answer:**
- **Status:** ACP is **fully live and usable today** via official ACP Agent Registry
- **Headless connection:** Claude Code can connect without IDE GUI by configuring `acp.json` with `agent_servers` block pointing to the agent executable
- **Exposed tools:** Semantic codebase search, file editing, shell command execution in integrated terminal
- **IntelliJ MCP relation:** ACP can explicitly expose the existing IntelliJ MCP server tools to the installed agent

### Q4: iOS Flat Accessibility Hierarchy Fix

**Answer:** Fix in CMP 1.9.3 is **incomplete**. Agent A6's concerns are valid:
- Regressions starting around CMP 1.8.1 where parent-child structure in iOS accessibility tree is lost
- Compound layouts (Card containing multiple Text elements) improperly merge inner components into parent on iOS
- **`mobile-mcp` and Maestro will still need to fall back to visual sensing for deeply nested CMP iOS elements**

### Q5: Computer Use API Version

**Answer:** Agent A5 is correct:
- `computer-use-2025-11-24` — current version for Claude 4.6 models (Opus 4.6, Sonnet 4.6)
- `computer-use-2025-01-24` — older version for 4.5 generation models
- macOS native computer use capability is confirmed rolled out

### Q6: agent-device (Callstack) — CMP Support

**Answer:** **Platform-agnostic, not RN-only.** Operates by extracting native OS-level accessibility tree snapshots (standard roles: windows, buttons, tables) from iOS and Android. Inherently supports any framework projecting semantic data to the OS accessibility layer, **including Compose Multiplatform**.

### Q7: Maestro Version

**Answer:** **Agent A6 is correct — Maestro 2.3.0**, published March 10, 2026. Gemini initial report citing 2.2.0 was slightly behind.

### Q8: Koog (JetBrains)

**Answer:**
- JVM-based framework (Kotlin DSL + Java APIs) for building custom AI agents — not an out-of-the-box CLI
- Can be compiled into a CLI application
- Natively supports MCP server integration and ACP-compliant agents
- Use case: Build custom Koog-based Kotlin verification logic, expose via MCP or ACP, invoke from Claude Code terminal

## Key Corrections Summary

| Item | Gemini Initial | Agent Finding | Correct Answer |
|---|---|---|---|
| CMP latest stable | 1.9.3 | 1.8.2 (A2) | **1.10.3** |
| Maestro version | 2.2.0 | 2.3.0 (A6) | **2.3.0** |
| Computer Use API version | 2025-01-24 | 2025-11-24 (A5) | **2025-11-24** |
| iOS flat hierarchy fix | Complete | Incomplete (A6) | **Incomplete — regressions since 1.8.1** |
| agent-device CMP support | Unclear | Not assessed | **Yes — OS accessibility layer** |
| ACP status | Announced | Not found (A3) | **Live today** |
