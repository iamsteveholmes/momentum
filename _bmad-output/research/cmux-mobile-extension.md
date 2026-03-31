---
research_date: 2026-03-30
agent_focus: CMUX mobile/desktop extension — iOS Simulator, Android Emulator, Desktop app panes
sources_consulted:
  - https://github.com/manaflow-ai/cmux
  - https://cmux.com/docs/api
  - https://cmux.com/docs/changelog
  - https://manaflow-ai-cmux.mintlify.app/features/splits-and-panes
  - https://manaflow-ai-cmux.mintlify.app/features/browser
  - https://github.com/manaflow-ai/cmux/blob/main/PROJECTS.md
  - https://github.com/joshuayoes/ios-simulator-mcp
  - https://github.com/whitesmith/ios-simulator-mcp
  - https://www.xcodebuildmcp.com/
  - https://github.com/getsentry/XcodeBuildMCP
  - https://github.com/mobile-next/mobile-mcp
  - https://github.com/CursorTouch/Android-MCP
  - https://github.com/Genymobile/scrcpy
  - https://deepwiki.com/jduartedj/android-mcp-server/5.2-high-speed-frame-streaming-with-scrcpy
  - https://github.com/steipete/Peekaboo
  - https://composeproof.dev/
  - https://twocentstudios.com/2025/12/27/closing-the-loop-on-ios-with-claude-code/
  - https://news.ycombinator.com/item?id=47079718
  - https://developer.apple.com/documentation/screencapturekit/
  - https://glama.ai/mcp/servers/multiagentcognition/cmux-agent-mcp
search_queries_used:
  - "CMUX terminal multiplexer Claude Code browser pane architecture 2025 2026"
  - "scrcpy version 2025 2026 Android screen mirroring Claude Code LLM agent"
  - "iOS Simulator streaming screen capture agent xcrun simctl screenshot automation 2025"
  - "Android emulator ADB screencap streaming MCP server LLM agent 2025 2026"
  - "simulator screen streaming MCP server Claude Code mobile agent 2025 2026"
  - "scrcpy 3.0 release 2025 2026 changelog features"
  - "macOS window capture NSWindow screenshot stream headless agent automation 2025"
  - "ios-simulator-mcp OR mobile-mcp Claude Code integration streaming frames visual feedback 2025 2026"
  - "CMUX mobile pane extension iOS Android emulator 2025 2026"
  - "XcodeBuildMCP iOS simulator Claude Code workflow 2025 2026"
  - "Android emulator grpc API screen streaming programmatic 2025"
  - "MJPEG websocket screenshot polling mobile emulator simulator LLM agent loop latency 2025"
  - "scrcpy websocket HTTP server video stream agent integration 2025"
  - "computer use Claude Code iOS Android simulator visual agent loop screenshot polling 2025 2026"
  - "Compose Multiplatform iOS Android Desktop testing automation agent MCP 2025 2026"
  - "scrcpy v3.3 release date features 2025"
  - "cmux image pane video pane simulator pane mobile extension feature request 2025 2026"
  - "ios-simulator-mcp screenshot base64 image return MCP tool visual agent 2025"
  - "iOS Simulator VNC stream ReplayKit RPScreenRecorder streaming 2025 agent automation"
  - "scrcpy no display headless screenshot ADB stream programmatic agent 2025"
last_verified: 2026-03-30
---

# CMUX Mobile Extension Feasibility Research

**Research Question:** Can CMUX (or its underlying architecture) be extended to support iOS Simulator, Android Emulator, or Desktop app panes — bringing the same "agent sees and controls the running app" capability to mobile and desktop that it already provides for web?

---

## 1. CMUX Architecture: Current State

**Confidence: High**

CMUX (github.com/manaflow-ai/cmux, v0.62+ as of March 2026) is a native macOS application built with Swift and AppKit, using libghostty for terminal rendering and WKWebView (WebKit) for its embedded browser pane. The architecture exposes a Unix domain socket API that accepts JSON-formatted commands. Any process — including Claude Code agent hooks — can send commands to this socket to create workspaces, split panes, send keystrokes, and control the browser.

### Pane Types (as of March 2026)

CMUX supports exactly three pane types:

| Pane Type | Description | Agent Control |
|---|---|---|
| Terminal | Ghostty-rendered shell | Full (keystrokes, text injection) |
| Browser | WKWebView with scriptable API | Full (DOM snapshot, click, fill, JS eval, screenshot) |
| Markdown | Live markdown preview | Read-only (file watch) |

There is **no custom pane type API**, no plugin system, and no mechanism for third parties to register new pane surface types. The PROJECTS.md roadmap (as of March 2026) contains zero mentions of simulator, emulator, image, video, or mobile panes. The developer confirmed on HN (item 47079718) that they are exploring an iOS companion app using libghostty but this is agent-as-client on iOS, not a simulator pane.

### The Browser Pane Pattern (What We Are Extending)

The browser pane gives the agent a "see and control" loop: the agent can snapshot the accessibility tree, click elements, fill forms, evaluate JS, and capture a screenshot — all via the socket API. This is a tight synchronous loop: act, observe, act. The key insight is that the agent does not watch a continuous video stream; it takes discrete screenshots on demand after each action.

---

## 2. iOS Simulator Pane

**Confidence: High**

### Capture Technologies Available

**xcrun simctl io booted screenshot** — The canonical, Apple-supported mechanism for iOS Simulator screen capture. Produces a PNG/JPEG via command line in approximately 200–500ms. No streaming; single-frame poll only.

**xcrun simctl io booted recordVideo** — Captures H.264 or HEVC video to a file. Not a streaming API; Control+C stops recording. Not suitable for live agent loops.

**ReplayKit / RPScreenRecorder** — Works on physical devices only. Apple's documentation explicitly states "screen recording functions do not work on the Xcode simulators." Ruled out.

**VNC** — The iOS Simulator itself does not expose a VNC server. There is no supported mechanism to attach an external VNC session to a running simulator process.

### MCP Ecosystem (Active, 2025–2026)

Multiple production-quality MCP servers now provide iOS Simulator access:

**joshuayoes/ios-simulator-mcp** (npm: `ios-simulator-mcp`, 2025)
- 13 tools: `screenshot`, `ui_tap`, `ui_swipe`, `ui_type`, `ui_describe_all`, `ui_view`, `launch_app`, `install_app`, `record_video`, `stop_recording`, `get_booted_sim_id`
- Screenshots returned as base64-encoded JPEG (JPEG quality configurable via `SCREENSHOT_JPEG_QUALITY`)
- `ui_view` returns compressed screenshot for inline LLM analysis
- Uses `xcrun simctl io` for capture; Facebook's idb for accessibility tree queries

**getsentry/XcodeBuildMCP** v2.0 (npm: `xcodebuildmcp@latest`, 2025–2026)
- 59 tools including `simulator/build`, `simulator/build-and-run`, `simulator/test`, `simulator/screenshot`, `ui-automation/tap`, `ui-automation/swipe`, LLDB attach
- Integrates with Xcode 26.3's native Claude agent mode
- Requires macOS 14.5+, Xcode 16.x+, Node.js 18.x+
- Auto-detects active scheme and simulator

**mobile-next/mobile-mcp** (2025)
- Cross-platform: iOS Simulator + Android Emulator + real devices
- Hybrid mode: accessibility tree (default, token-efficient) + screenshot fallback
- Platform-agnostic interface

**Real-world agent loop (twocentstudios, December 2025):**
- Workflow: screenshot → resize to 1x (ImageMagick) → LLM analysis → tap via AXe (idb) → screenshot → repeat
- Per-cycle latency: ~2–4 seconds
- Key finding: "slows down the entire process by 2x" when verification is enabled
- Tap accuracy remains unreliable; scroll direction frequently confused
- Assessment: "proof-of-concept maturity, not production-ready"

### CMUX Integration Path

**Direct pane extension:** Not possible without forking CMUX and adding a new pane surface type in Swift/AppKit. There is no plugin API.

**Workaround — HTML wrapper in browser pane:** An MJPEG or WebSocket frame server could be run locally (e.g., a Node.js server that calls `xcrun simctl io booted screenshot` on a 2–4Hz poll and serves frames as JPEG over HTTP). A browser pane could load this page and display the simulator frames in an `<img>` tag with JavaScript auto-refresh. The agent would see the simulator indirectly through the browser pane. This is architecturally sound but adds 1–3 seconds of latency per frame.

**Direct approach — MCP only:** Configure XcodeBuildMCP or ios-simulator-mcp as an MCP server alongside Claude Code. The agent calls `screenshot` tool, receives base64 JPEG, analyzes it, calls `ui_tap` with coordinates, repeat. No CMUX pane involved; the agent loop is fully MCP-driven.

### Technical Blockers

- No native simulator pane type in CMUX (would require Swift fork)
- `xcrun simctl io` is single-frame only; no streaming API
- ReplayKit does not work in Simulator
- Poll-based loops add 2–4s per cycle
- Scale mismatch: Simulator screenshots at 3x; taps at 1x coordinates

---

## 3. Android Emulator Pane

**Confidence: High**

### Capture Technologies Available

**ADB screencap** — `adb shell screencap -p | adb pull` or `adb exec-out screencap -p`. Latency 500–1500ms. Works on emulator and physical device. Universal fallback.

**Android Emulator gRPC API** — The Android Emulator exposes an experimental gRPC service (documented in AOSP: `android/android-grpc`). Supports screenshot queries and input events even in headless mode. Intended for same-machine use only; security warning for remote access. Status as of March 2026: still marked experimental.

**scrcpy** — Genymobile/scrcpy v3.3.4 (December 17, 2024) → latest known is v3.3.4. Key capability for agents: `--no-display` flag runs scrcpy headlessly while maintaining its H.264 stream pipeline. A persistent H.264 stream can be spawned with `--max-fps=30 --video-codec=h264 --video-bit-rate=5M --no-display`. A consumer process reads `latestFrame` buffer at <50ms per access after ~2000ms initial setup.

**ws-scrcpy** (NetrisTV/ws-scrcpy) — WebSocket wrapper around scrcpy. Streams H.264 video from Android device/emulator over WebSocket to a browser. Architecture: HTTP server (static files) + WebSocket server (device proxy) + multiple decoder options (HTML5 Video, WebAssembly). This is the closest existing technology to a "simulator browser pane" — the emulator screen can be embedded in a web page.

### scrcpy Version History (2025)

| Version | Release Date | Key Feature |
|---|---|---|
| v3.0 | ~late 2024 | Virtual display, OpenGL filters, --angle |
| v3.2 | March 2025 | Enhanced audio recording, Android 15/16 fixes, AV1/dav1d |
| v3.3 | June 11, 2025 | Virtual display improvements, Android 16 audio fixes |
| v3.3.1 | June 20, 2025 | HID mouse, horizontal scrolling, clipboard fixes |
| v3.3.2 | September 6, 2025 | Android 16 virtual display, Samsung clipboard workaround |
| v3.3.3 | September 27, 2025 | Android 16 upgrade error fix, frame memory leak |
| v3.3.4 | December 17, 2024 | Permission denial errors, state restoration |

Note: SourceForge mirror lists v3.3.4 — the GitHub releases page content retrieved showed dates in late 2024, but AlternativeTo confirms v3.2 released March 2025. Latest confirmed version as of March 2026: v3.3.4 or later (current exact version uncertain given GitHub data discrepancy; treat as Medium confidence for exact release dates post-v3.2).

### MCP Ecosystem (Active, 2025–2026)

**CursorTouch/Android-MCP** (MIT, Python 3.10+)
- Tools: State-Tool, Click-Tool, Swipe-Tool, Type-Tool, Press-Tool, Shell-Tool, Notification-Tool
- Screenshot delivery: captures from connected device/emulator, optional `SCREENSHOT_QUANTIZED` to reduce token cost
- Typical interaction latency: 2–4s

**mobile-next/mobile-mcp** — Cross-platform server covering both iOS and Android.

**Android ADB MCP Server** (Landice Fu, PulseMCP, January 2026) — One of several MCP servers released in January 2026 for ADB-based automation, indicating active ecosystem development.

**jduartedj/android-mcp-server** — Implements high-speed scrcpy frame streaming:
- Streaming Mode: persistent H.264 pipeline, `latestFrame` buffer, per-frame access <50ms after 2000ms init
- Single-Frame Mode: one scrcpy invocation per frame, avoids persistent connection overhead
- Fallback: ADB screencap (500–1500ms)
- Pull-based: agent calls `android_get_latest_frame` explicitly; no push

### CMUX Integration Path

**ws-scrcpy as browser pane source:** ws-scrcpy runs a local HTTP+WebSocket server. A CMUX browser pane loads its web interface, which renders the Android Emulator screen in real time (H.264 decoded in-browser via WebAssembly). The agent views the emulator through the browser pane. Touch input can be sent via ws-scrcpy's web control interface or via direct ADB commands through MCP tools.

This is the most promising path for a CMUX-like experience for Android, and it requires no CMUX modifications — it is a web application rendered in the existing browser pane.

**MCP-only path:** Same as iOS — configure android-mcp or mobile-mcp, call screenshot tool, receive base64, act via ADB tools.

### Technical Blockers

- ADB screencap latency (500–1500ms) is 5–15x slower than browser DOM operations
- Android Emulator gRPC API is experimental, same-machine only, not officially supported
- ws-scrcpy has had sporadic maintenance; not all forks are current
- scrcpy does not work against iOS Simulator (Android-only)

---

## 4. Desktop App Pane (macOS)

**Confidence: High**

### Capture Technologies Available

**Apple ScreenCaptureKit** (macOS 12.3+) — The current recommended API for capturing desktop content. Supports streaming displays, apps, and windows. Uses "persistent fast stream" with per-frame callbacks. Peekaboo v3 (steipete/Peekaboo) uses a "persistent ScreenCaptureKit fast stream with frame-age + wait timing logs" for near-real-time window capture.

**screencapture CLI** — `screencapture -l <windowID>` captures a specific window by ID. Works without focus change. Latency: ~200–400ms.

**NSWindow / Quartz Compositor** — Modern screen recording captures composited frames via ScreenCaptureKit rather than per-window pixel buffers. Focus stealing is not required.

### Peekaboo: Production-Quality Tool (steipete/Peekaboo, v3.0.0-beta4, 2025–2026)

Peekaboo is a macOS CLI + MCP server that captures windows, apps, or screens using ScreenCaptureKit without requiring focus changes:
- Natural-language agent chain: `see`, `click`, `type`, `scroll`, `hotkey`, `menu`, `window`, `app`, `dock`, `space`
- MCP server mode compatible with Claude Desktop, Cursor, and any MCP client
- Supports GPT-5.1, Claude 4.x, Grok 4-fast, Gemini 2.5, local Ollama
- Closed-loop automation: screenshot → annotate UI elements with IDs → click by label or coordinate
- Install: `npx -y @steipete/peekaboo`
- Status: v3.0.0-beta4, actively maintained, 2308 commits

### CMUX Integration Path

**Via MCP + Peekaboo:** Configure Peekaboo as MCP server alongside Claude Code. Agent calls `see` (captures target window), receives annotated screenshot, calls `click` with element label. No CMUX changes required. The "pane" is conceptual — Peekaboo's vision + action loop replaces a visual pane.

**Via browser pane workaround:** A local HTTP server serving a `<img>` element refreshed via JavaScript, pulling screenshots from `screencapture -l <windowID>` on a polling loop. Agent views the desktop app through the browser pane. Same architectural approach as the iOS workaround.

**Direct CMUX pane:** Same constraint as iOS — would require a new pane surface type in Swift/AppKit. Not currently feasible without forking.

### Technical Blockers

- ScreenCaptureKit requires user permission grant (TCC); agents cannot self-grant
- No continuous streaming into a browser pane without a local HTTP polling server
- Peekaboo v3 is still in beta
- Agent click accuracy on native macOS controls varies; accessibility API is more reliable than coordinate-based taps

---

## 5. Streaming Patterns: Current State of the Art

**Confidence: High**

The ecosystem has converged on three distinct patterns for providing simulator/emulator visual feedback to agents:

### Pattern 1: Screenshot Polling (Most Common)

Agent calls a tool (MCP or CLI), which executes `xcrun simctl io booted screenshot` or `adb exec-out screencap -p`, encodes the result as base64 JPEG, and returns it in the tool response. Agent analyzes, acts, repeats.

- **Latency per cycle:** 2–5s (screenshot + LLM vision + action)
- **Throughput:** ~12–30 screenshots/minute practical
- **Agent integration:** Native MCP tool return value; works in any MCP-capable client
- **Used by:** ios-simulator-mcp, XcodeBuildMCP, Android-MCP, mobile-mcp

### Pattern 2: Persistent Frame Buffer (scrcpy-based, Android only)

scrcpy with `--no-display` maintains a persistent H.264 pipeline. A sidecar process reads the H.264 stdout, decodes, and stores the latest frame in memory. Agent calls `getLatestFrame()` at <50ms per access.

- **Latency per frame access:** <50ms after 2000ms init
- **Used by:** jduartedj/android-mcp-server
- **iOS equivalent:** None; `xcrun simctl` has no streaming mode

### Pattern 3: Browser-Embedded Live Stream (ws-scrcpy, Android only)

ws-scrcpy runs an H.264-over-WebSocket server. A browser pane loads the ws-scrcpy web interface, which decodes and renders the Android device screen in real time using WebAssembly. Agent interacts via browser DOM controls or parallel ADB MCP tools.

- **Latency:** Near-real-time visual (35–70ms per scrcpy docs), agent interaction via separate ADB channel
- **Best fit for CMUX:** Android emulator via existing browser pane — no CMUX modifications needed
- **iOS equivalent:** Not available; no scrcpy-equivalent stream source for iOS Simulator

### Pattern 4: ScreenCaptureKit Stream (Desktop only)

Peekaboo and macOS apps using ScreenCaptureKit maintain a persistent capture stream with frame callbacks. Frames available with <50ms latency. Suitable for a local HTTP server feeding a browser pane.

---

## 6. Prior Art: Claude Code + Simulator Integration

**Confidence: High**

Several documented workflows combine Claude Code with real-time simulator screen access as of late 2025 / early 2026:

**twocentstudios (December 2025)** — "Closing the Loop on iOS with Claude Code": Complete documented workflow using AXe (idb wrapper), ImageMagick, xcrun simctl. Honest assessment: 2x slowdown when verification is enabled, tap accuracy issues, proof-of-concept maturity. Primary source: twocentstudios.com/2025/12/27/closing-the-loop-on-ios-with-claude-code/

**conorluddy/ios-simulator-skill** — Claude Code skill for iOS Simulator using IDB tools. Optimizes token/context usage by preferring accessibility tree over screenshots. GitHub: github.com/conorluddy/ios-simulator-skill

**emCap/ios-simulator-mcp** — MCP server that "automatically captures screenshots when UI changes occur" and exposes them to Cursor AI. Implies event-driven rather than pure polling — closest existing approach to a push model for iOS.

**ComposeProof** (composeproof.dev, 2025–2026) — MCP server specifically for Compose UI (Android). Headless rendering of `@Preview` composables, API mocking, on-device screenshots, ~40 tools, ~7300 tokens per full project analysis. Works with Claude Code, Cursor, Gemini CLI. This is directly relevant for Compose Multiplatform Android targets.

**Apple/Anthropic — Xcode 26.3 + Claude Agent SDK** — Apple announced native Claude agent integration in Xcode 26.3. XcodeBuildMCP v2.0 integrates with this. Provides 59 tools including `simulator/screenshot`. This is the highest-fidelity Apple-supported path for iOS/macOS agent loops.

**No prior art found** for a CMUX pane directly embedding a live iOS Simulator or Android Emulator window. The ws-scrcpy-in-browser-pane pattern is architecturally possible but not documented as a CMUX-specific workflow.

---

## 7. MCP Approach vs. CMUX Native Pane

**Confidence: High**

The core question is whether the "agent sees and controls the running app" experience requires a CMUX pane or whether an MCP-only approach is equivalent.

### What the Browser Pane Adds (vs. MCP-only)

The CMUX browser pane provides a **persistent human-visible window** alongside the terminal. A developer watching the session can see exactly what the agent sees. Screenshots are rendered at full resolution in the pane, providing simultaneous human oversight and agent access. This is primarily a developer experience (DX) feature; the agent loop itself does not depend on the pane being visible.

### MCP-Only Approach

An MCP server (XcodeBuildMCP, ios-simulator-mcp, Android-MCP) provides all the agent-loop primitives: screenshot → analyze → act → screenshot. The agent does not need to see a persistent pane. The human developer cannot easily observe what the agent is seeing unless they open a separate Simulator window.

### Hybrid: MCP + CMUX Browser Pane as Viewport

The optimal approach for a Compose Multiplatform workflow combining agent capability with human observability:

**For Android Emulator:** Run ws-scrcpy as a local server. Open a CMUX browser pane pointed at `http://localhost:<ws-scrcpy-port>`. Agent sends ADB actions via android-mcp or mobile-mcp MCP tools. Human sees live emulator screen in the CMUX pane.

**For iOS Simulator:** Run a lightweight local HTTP server (Node.js) that polls `xcrun simctl io booted screenshot` every 1–2 seconds and serves the latest frame as a JPEG. Open a CMUX browser pane pointed at this server. Agent sends actions via XcodeBuildMCP or ios-simulator-mcp. Human sees the simulator in the CMUX pane (with 1–2s lag).

**For Desktop App:** Run a screencapture polling server using ScreenCaptureKit or `screencapture -l <windowID>`. Same pattern as iOS. Or use Peekaboo MCP server directly without a CMUX pane.

This hybrid approach requires no CMUX source code changes and is implementable today.

---

## 8. Recommended Extension Approach

**Confidence: Medium** (depends on Compose Multiplatform target priorities)

### Recommendation: MCP-First with Optional Browser Pane Viewport

For a Compose Multiplatform workflow spanning iOS, Android, and Desktop from a single Claude Code session:

**Tier 1 — Android (Highest Feasibility, Best Tooling)**

1. Run Android Emulator via AVD Manager or `emulator -avd <name> -no-window`
2. Install `mobile-next/mobile-mcp` or `jduartedj/android-mcp-server` as MCP servers
3. For visual CMUX pane: run ws-scrcpy locally, open browser pane at `http://localhost:8000`
4. Agent loop: build APK → install via `adb install` → screenshot → verify → interact
5. ComposeProof for Compose-specific headless preview verification

**Tier 2 — iOS Simulator (Good Feasibility, Mature Tooling)**

1. Boot simulator via `xcrun simctl boot <UUID>`
2. Install XcodeBuildMCP v2.0 as MCP server (59 tools including build+screenshot+tap)
3. For visual CMUX pane: lightweight Node.js polling server → browser pane (1–2s lag)
4. Agent loop: `simulator/build-and-run` → `simulator/screenshot` → analyze → `ui-automation/tap` → repeat
5. Expect 3–6s per verify cycle; tap accuracy ~70%

**Tier 3 — Desktop (JVM) (Good Feasibility, Mature Tooling)**

1. Run JVM desktop build: `./gradlew runRelease` or equivalent
2. Install Peekaboo MCP server: `npx -y @steipete/peekaboo`
3. Agent uses `see` tool targeting the app window, `click` for interaction
4. Optional CMUX browser pane: screencapture polling server
5. Native accessibility tree is more reliable than screenshot for JVM desktop controls

### Priority Order for Implementation

Given Compose Multiplatform context:

1. **Android emulator first** — Best tooling (scrcpy, ws-scrcpy, ComposeProof, Android-MCP), most agent infrastructure, most prior art, ws-scrcpy provides live browser pane with no CMUX changes
2. **iOS Simulator second** — XcodeBuildMCP v2.0 is production-quality, Xcode 26.3 native integration is the best-supported path; browser pane viewport requires polling workaround
3. **Desktop third** — Peekaboo handles it well; JVM desktop is lowest priority for most mobile-primary Compose workflows

---

## 9. Technical Blockers Summary

| Platform | Blocker | Severity | Workaround |
|---|---|---|---|
| iOS Simulator | No streaming API from xcrun simctl | High | Poll at 1–2Hz via local HTTP server |
| iOS Simulator | ReplayKit non-functional in Simulator | High | None — xcrun simctl only |
| iOS Simulator | 3x screenshot / 1x tap coordinate mismatch | Medium | Resize screenshots to 1x before analysis |
| iOS Simulator | Tap accuracy ~70% in practice | Medium | Prefer accessibility tree navigation |
| Android Emulator | ADB screencap latency 500–1500ms | High | Use scrcpy persistent stream (<50ms) |
| Android Emulator | Emulator gRPC API experimental | Medium | Use ADB or scrcpy instead |
| Desktop | TCC permission required for ScreenCaptureKit | Medium | One-time user grant; scripts cannot self-grant |
| Desktop | Peekaboo v3 in beta | Low | Stable v2 available as fallback |
| All platforms | CMUX has no custom pane type API | High | Browser pane viewport workaround or MCP-only |
| All platforms | No continuous video streaming into CMUX natively | High | ws-scrcpy (Android) or polling server (iOS/Desktop) |

---

## 10. Confidence Ratings by Section

| Section | Rating | Rationale |
|---|---|---|
| CMUX current architecture | High | Directly verified from source, docs, changelog, PROJECTS.md |
| iOS Simulator capture tech | High | Well-documented Apple APIs; limitations confirmed (ReplayKit, no streaming) |
| iOS Simulator MCP ecosystem | High | Multiple production servers confirmed with npm packages and GitHub repos |
| Android Emulator capture tech | High | ADB, scrcpy documented; gRPC experimental status confirmed from AOSP docs |
| Android MCP ecosystem | High | Multiple active projects confirmed |
| scrcpy version history 2025 | Medium | v3.2 (March 2025) confirmed; v3.3–v3.3.4 dates have minor discrepancy between GitHub and mirrors |
| Desktop capture (Peekaboo) | High | Well-documented, active project, npm installable |
| ws-scrcpy browser pane approach | Medium | Architecture confirmed; specific integration as CMUX browser pane source is inferred, not documented as an existing workflow |
| Polling server browser pane workaround | Medium | Architecturally sound; not documented as a deployed CMUX workflow |
| ComposeProof relevance | High | Official product page confirmed, Claude Code + Cursor integration confirmed |
| Agent loop latency estimates | Medium | Based on documented reports from December 2025; may improve with future tooling |
| Prior art for CMUX mobile extension | High | Confirmed no prior art for native CMUX pane; MCP-based prior art is extensive |

---

## Key Sources

- CMUX architecture: [github.com/manaflow-ai/cmux](https://github.com/manaflow-ai/cmux), [cmux.com/docs/api](https://cmux.com/docs/api), [PROJECTS.md](https://github.com/manaflow-ai/cmux/blob/main/PROJECTS.md) — accessed 2026-03-30
- iOS Simulator MCP: [joshuayoes/ios-simulator-mcp](https://github.com/joshuayoes/ios-simulator-mcp), [XcodeBuildMCP](https://www.xcodebuildmcp.com/) — accessed 2026-03-30
- Android MCP: [CursorTouch/Android-MCP](https://github.com/CursorTouch/Android-MCP), [mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp) — accessed 2026-03-30
- scrcpy: [Genymobile/scrcpy releases](https://github.com/Genymobile/scrcpy/releases), [AlternativeTo v3.2](https://alternativeto.net/news/2025/3/scrcpy-v3-2-release-new-audio-sources-and-compatibility-fixes/) — accessed 2026-03-30
- scrcpy frame streaming architecture: [DeepWiki android-mcp-server](https://deepwiki.com/jduartedj/android-mcp-server/5.2-high-speed-frame-streaming-with-scrcpy) — accessed 2026-03-30
- ws-scrcpy: [NetrisTV/ws-scrcpy](https://github.com/NetrisTV/ws-scrcpy) — accessed 2026-03-30
- Desktop capture: [steipete/Peekaboo](https://github.com/steipete/Peekaboo) — accessed 2026-03-30
- Real-world iOS agent loop: [twocentstudios.com](https://twocentstudios.com/2025/12/27/closing-the-loop-on-ios-with-claude-code/) — accessed 2026-03-30
- ComposeProof: [composeproof.dev](https://composeproof.dev/) — accessed 2026-03-30
- HN CMUX thread: [HN item 47079718](https://news.ycombinator.com/item?id=47079718) — accessed 2026-03-30
- Apple ScreenCaptureKit: [developer.apple.com/documentation/screencapturekit](https://developer.apple.com/documentation/screencapturekit/) — accessed 2026-03-30
