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

## Key Corrections Summary (Follow-up Round 1)

| Item | Gemini Initial | Agent Finding | Correct Answer |
|---|---|---|---|
| CMP latest stable | 1.9.3 | 1.8.2 (A2) | **1.10.3** |
| Maestro version | 2.2.0 | 2.3.0 (A6) | **2.3.0** |
| Computer Use API version | 2025-01-24 | 2025-11-24 (A5) | **2025-11-24** |
| iOS flat hierarchy fix | Complete | Incomplete (A6) | **Incomplete as of 1.9.3 — see Round 2 Q1 for 1.10.3 status** |
| agent-device CMP support | Unclear | Not assessed | **Yes — OS accessibility layer** |
| ACP status | Announced | Not found (A3) | **Live today** |

---

## Follow-up Q&A Round 2

### Q1: CMP 1.10.3 — iOS Flat Hierarchy Fix Status

**Answer:**
- **FIXED in 1.10.3.** Official CMP 1.10.3 release notes (March 2026) explicitly state: "Traversal groups now convert into an additional node in the accessibility hierarchy #2848"
- This restores the expected nested parent-child structure on iOS
- Desktop (macOS/JVM) also saw significant accessibility fixes in 1.10.3: VoiceOver wrong-button-click bug (#2720, #2680), `TextField` `contentDescription` properly mapped to accessible name
- **Source:** JetBrains GitHub Releases, CMP 1.10.3 Changelog

**Impact on agent reports:** A6 and A1 stated the flat hierarchy regression was "INCOMPLETE" — this was accurate for CMP ≤1.9.3 but is no longer accurate for CMP 1.10.3. Synthesis must reflect the corrected status: fixed in 1.10.3.

### Q2: Appium Current Stable Version

**Answer:** **Appium 3.2.2**, released March 9, 2026
- GitHub: https://github.com/appium/appium/releases

**Corrections:** A1 cited 3.2.1 (March 8); Gemini initial Round 1 was silent. Correct answer: **3.2.2**

### Q3: facebook/idb Current Status

**Answer:**
- Repository not archived but **largely unmaintained** by Facebook/Meta
- `fb-idb` Python client v1.1.7 (PyPI) is **currently non-functional** for many users — crashes with `ImportError` in `companion_spawner` (Issue #902, late March 2026); fails to capture UI descriptions on iOS 26
- **Community MCP wrapper:** `InditexTech/mcp-server-simulator-ios-idb` v1.0.1 (April 2025) wraps idb into an MCP server for LLM control

**Corrections:** A1 assessed idb as viable with caveats. Updated assessment: idb is functionally broken for many users; community MCP wrapper may be more reliable path than raw idb.

### Q4: ios-simulator-mcp Version Confirmed

**Answer:** **v1.5.2 confirmed** as of March 30, 2026
- npm package by joshuayoes; GitHub: https://github.com/joshuayoes/ios-simulator-mcp/releases

### Q5: creavit.studio / node-mac-recorder

**Answer:** Real project, different organization than domain name implies:
- **GitHub URL:** https://github.com/aslanon/node-mac-recorder
- **npm package:** `node-mac-recorder`
- **Functionality:** Native macOS screen recording via Apple's `ScreenCaptureKit` (macOS 12.3+) and `AVFoundation`; captures full screens, specific application windows, or custom coordinate areas; multi-display support, audio/camera sync, cursor tracking; automatic overlay window exclusion

**Corrections:** A5 flagged creavit.studio as potentially hallucinated. It is a real project — `aslanon/node-mac-recorder` on GitHub. The domain association was unclear, hence the confusion.

### Q6: JetBrains Central — Availability Status

**Answer:**
- **Definition:** JetBrains Central is a "control and execution plane for agent-driven software production" — a platform/system, not a standalone IDE
- **NOT publicly available as of March 30, 2026** — scheduled for Early Access Program (EAP) in **Q2 2026** for a limited group of design partners only
- Integrates with ACP and MCP; designed to govern AI agents across IDEs, CLIs, CI/CD, collaboration tools
- Supports connecting agents from varying ecosystems (Claude Code, Gemini CLI, Codex, Junie) to a shared semantic layer
- **Announcement URL:** https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/

**Corrections:** A3 implied JetBrains Central was usable today. **It is not — EAP Q2 2026 only.** Significant correction.

### Q7: idb JSON Field Names

**Answer:** Gemini cannot definitively confirm the exact JSON field names from `idb ui describe-all` from available 2025/2026 documentation. The mapping of Compose `testTag` or `contentDescription` to idb JSON payload keys is unclear. macOS AppleScript APIs use `AXIdentifier` but this may not match idb's output schema.

**Status:** Unresolved — requires live testing against a booted simulator.

### Q8: ACP + iOS Simulator — Headless Path

**Answer:** ACP itself does **not** natively contain iOS Simulator tools. iOS access via ACP requires MCP pass-through from an IDE:
- In JetBrains IDEs: `Settings | Tools | AI Assistant | Agents` → enable "Pass custom MCP servers"
- If `ios-simulator-mcp` or `XcodeBuild MCP` is configured in the IDE, those tools are exposed to Junie or Claude Code ACP agent
- **No standalone headless path:** ACP → iOS requires IDE to be open and configured as bridge

**Impact on synthesis:** The headless ACP story for iOS does not work without an IDE running. Claude Code can connect to ACP headlessly, but iOS simulator tools only flow through if a JetBrains IDE is open and configured as the MCP bridge.

### Q9: Maestro 2.3.0 + CMP 1.10.3 iOS — Does #1549 Still Apply?

**Answer:**
- **CMP 1.10.3 fix is visible to Maestro:** The structural fix (#2848) correctly projects traversal groups as additional nodes into the iOS system accessibility layer, which Maestro reads via black-box accessibility APIs
- **Maestro issue #1549 remains open:** Still an active enhancement request — community requesting the same stability, Studio evaluation speed, and element distinction for CMP iOS that exists for Android Jetpack Compose and native SwiftUI
- **Practical friction persists in 2.3.0:**
  - Maestro Studio sometimes struggles to stream CMP iOS UI properly
  - Random crashes when navigating between CMP iOS screens
  - Coordinate-based fallbacks still sometimes required (e.g., `tapOn: point: 50%,81%`) rather than semantic element selection
- **Bottom line:** JetBrains fixed the accessibility tree projection; Maestro's internal tooling and Studio environment still need optimization for CMP iOS engine elements

**Impact on synthesis:** CMP 1.10.3 removes the accessibility layer blocker, but Maestro remains unreliable for CMP iOS in practice as of March 2026. Semantic selection is possible but not friction-free. Coordinate fallbacks are still a practical reality.

---

## Key Corrections Summary (Follow-up Round 2)

| Item | Prior Understanding | Correct Answer |
|---|---|---|
| CMP 1.10.3 iOS flat hierarchy | Incomplete (regression since 1.8.1) | **FIXED in 1.10.3 — #2848** |
| Appium latest stable | 3.2.1 | **3.2.2 (March 9, 2026)** |
| idb status | Viable with caveats | **Largely unmaintained; fb-idb crashes (ImportError); community MCP wrapper v1.0.1 available** |
| ios-simulator-mcp version | v1.5.2 (tentative) | **v1.5.2 confirmed** |
| creavit.studio / node-mac-recorder | Potentially hallucinated | **Real: github.com/aslanon/node-mac-recorder** |
| JetBrains Central availability | Available / usable today | **NOT available — EAP Q2 2026 only** |
| idb JSON field names | AXLabel (tentative) | **Unresolved — needs live testing** |
| ACP + iOS Simulator headless | Possible via acp.json | **Requires IDE open as MCP bridge — not standalone** |
| Maestro 2.3.0 + CMP 1.10.3 iOS | Not assessed | **Tree fix visible to Maestro; #1549 still open; Studio crashes + coordinate fallbacks still needed** |
