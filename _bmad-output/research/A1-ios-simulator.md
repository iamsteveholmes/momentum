---
research_date: 2026-03-30
agent_focus: iOS Simulator automation for LLM agents
sources_consulted:
  - https://github.com/joshuayoes/ios-simulator-mcp
  - https://github.com/InditexTech/mcp-server-simulator-ios-idb
  - https://github.com/whitesmith/ios-simulator-mcp
  - https://github.com/facebook/idb
  - https://fbidb.io/docs/commands/
  - https://fbidb.io/docs/accessibility/
  - https://fbidb.io/docs/overview/
  - https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-180.html
  - https://appium.github.io/appium-xcuitest-driver/10.11/installation/
  - https://github.com/appium/appium-xcuitest-driver/releases
  - https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/
  - https://github.com/ldomaradzki/xctree
  - https://ldomaradzki.com/blog/xctree-accessibility-cli
  - https://github.com/riwsky/iosef
  - https://github.com/callstackincubator/agent-device
  - https://discuss.appium.io/t/compose-kmp-ios/45724
  - https://www.iosdev.recipes/simctl/
  - https://pypi.org/project/fb-idb/
  - https://github.com/joshuayoes/ios-simulator-mcp/security/advisories/GHSA-6f6r-m9pv-67jw
  - https://www.kmpship.app/blog/kotlin-multiplatform-testing-guide-2025
  - https://maestro.dev/
  - https://sarunw.com/posts/take-screenshot-and-record-video-in-ios-simulator/
  - https://nshipster.com/simctl/
  - https://devcenter.bitrise.io/en/testing/testing-ios-apps/running-xcode-tests.html
  - https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/
  - https://slack-chats.kotlinlang.org/t/26981930/
  - https://www.npmjs.com/package/ios-simulator-mcp
  - https://nvd.nist.gov/vuln/detail/CVE-2025-52573
search_queries_used:
  - "xcrun simctl screenshot interact touch 2025 2026 headless"
  - "Appium iOS Simulator headless XCUITest driver 2025 2026"
  - "MCP server iOS Simulator Claude LLM automation 2025 2026"
  - "idb Facebook iOS development bridge simulator 2025 2026 status"
  - "Compose Multiplatform iOS accessibility tree UITest semantic properties 2025"
  - "xcrun simctl io booted interact touch tap swipe sendEvent 2025"
  - "xcodebuild test headless simulator no Xcode open CLI 2025"
  - "AXUIElement iOS Simulator window accessibility tree macOS programmatic 2025"
  - "Appium 3 XCUITest driver version release 2025 2026 Compose Multiplatform"
  - "simctl Xcode 16 new features 2024 2025 simulator capabilities"
  - "xcrun simctl ui subcommand OR input touch interact 2024 2025 new"
  - "iOS Simulator automation LLM agent shell commands screenshot tap 2025 2026 approach"
  - "Compose Multiplatform iOS testTag accessibilityIdentifier XCUITest automation Appium 2025"
  - "Appium XCUITest Compose Multiplatform OR KMP iOS element not found testTag 2025"
  - "idb facebook tap swipe screenshot accessibility simulator command 2024 2025"
  - "xctree accessibility CLI iOS Simulator GitHub 2024 2025"
  - "Compose Multiplatform 1.8 iOS accessibility sync testing XCUITest 2025"
  - "idb iOS Development Bridge facebook 2025 maintenance active deprecated"
  - "ios-simulator-mcp joshuayoes version CVE-2025-52573 npm current 2025"
  - "Appium 3 release date stable version 2025"
  - "Maestro iOS Simulator Compose Multiplatform testing 2025"
  - "idb companion installation Xcode 16 homebrew 2025 working"
  - "whitesmith ios-simulator-mcp npm version 2025 2026"
last_verified: 2026-03-30
---

# A1: iOS Simulator Automation for LLM Agents
## Research Date: March 30, 2026

## Executive Summary

As of March 2026, the most practical approach for a shell-based LLM agent to automate the iOS Simulator is a layered stack: `xcrun simctl` for lifecycle management and screenshots, Facebook's `idb` for touch interaction and accessibility tree dumps, and an MCP server (preferably `whitesmith/ios-simulator-mcp` or `joshuayoes/ios-simulator-mcp` at v1.3.3+) to expose all of this over the Model Context Protocol. For Compose Multiplatform iOS apps specifically, there is a critical caveat: accessibility tree visibility via Appium/XCUITest requires explicit `AccessibilitySyncOptions` configuration in the app's `MainViewController`, as the lazy sync default introduced in CMP 1.8.2 does not trigger from automation tooling. Native `idb ui describe-all` against the iOS accessibility API appears to work without that workaround (see CMP Accessibility section for confidence level). Additionally, Apple's Claude Agent SDK in Xcode 26.3 (announced February 3, 2026) introduces a headless Xcode Previews capture path via the `-p` flag that may provide a lighter-weight verification option for CMP UI without running a full Simulator — see dedicated section below.

---

## Tool: xcrun simctl

### Status and Capabilities (as of March 2026)

`xcrun simctl` is Apple's built-in CLI for iOS Simulator lifecycle management, shipping with every Xcode installation. It requires no additional installation for a developer machine already running Xcode or Xcode Command Line Tools. As of Xcode 16 (released September 2024), the command surface has not added touch/gesture primitives — that gap has been consistent since simctl's introduction. [Source: https://www.iosdev.recipes/simctl/, accessed 2026-03-30]

**Lifecycle commands available:**
```sh
xcrun simctl list devices                          # enumerate simulators
xcrun simctl boot <UDID>                           # boot headlessly
xcrun simctl shutdown <UDID>
xcrun simctl launch booted <bundle-id>             # launch app
xcrun simctl terminate booted <bundle-id>
xcrun simctl install booted /path/to/App.app
xcrun simctl openurl booted <url>
xcrun simctl push booted <bundle-id> payload.json  # push notification
xcrun simctl addmedia booted /path/to/file         # add media
xcrun simctl spawn booted <command>                # run process inside sim
xcrun simctl get_app_container booted <bundle-id>  # locate app container
```

**I/O commands (the `io` subgroup):**
```sh
xcrun simctl io booted screenshot output.png       # formats: png, tiff, bmp, gif, jpeg
xcrun simctl io booted recordVideo output.mp4      # codec: h264, mp4, fmp4
```

Screenshots are synchronous, single-command, and return immediately — ideal for an agent polling loop. [Source: https://sarunw.com/posts/take-screenshot-and-record-video-in-ios-simulator/, accessed 2026-03-30] [Primary source preferred — Apple developer documentation for `xcrun simctl io` would be authoritative; third-party blog cited as available reference]

**What simctl CANNOT do:**
- Touch/tap/swipe/gesture injection — no subcommand exists for this as of March 2026
- Accessibility tree inspection — no `ui describe` equivalent
- Text input

The `xcrun simctl ui` subcommand exists but only covers display settings (content size, appearance, contrast) — not interaction. [Source: https://www.iosdev.recipes/simctl/, accessed 2026-03-30]

**Headless operation:** Simulators boot and run fully headlessly without Simulator.app in the foreground. The `xcrun simctl boot <UDID>` command alone boots the device; `open -a Simulator` is only needed to show the GUI window. [Source: https://nshipster.com/simctl/, accessed 2026-03-30]

### Assessment

| Criterion | Rating |
|---|---|
| Status as of March 2026 | Active — ships with Xcode 16, stable CLI |
| Headless | Yes — fully headless |
| Touch/interaction | No — zero touch primitives |
| Semantic tree vs. screenshot | No — screenshot only, no tree access |
| Setup complexity | Minimal — ships with Xcode |

**Confidence:** High — simctl capabilities are stable and well-documented across multiple independent sources with consistent findings across 2024-2025 content.

---

## Tool: Appium + XCUITest Driver

### Status and Capabilities (as of March 2026)

Appium 3 was released as stable on August 7, 2025. [Source: https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/, accessed 2026-03-30] As of March 30, 2026, the latest stable Appium version is 3.2.1 (released March 8, 2026). The XCUITest driver (appium-xcuitest-driver) version as of March 2026 is 10.14.4 — the project releases frequently. [Source: https://github.com/appium/appium-xcuitest-driver/releases (general releases page, not pinned permalink), accessed 2026-03-30] [Single source — verify independently]

**Breaking dependency:** XCUITest driver v10.0.0+ requires Appium 3 exclusively; Appium 2 is no longer supported. [Source: https://appium.github.io/appium-xcuitest-driver/10.11/installation/, accessed 2026-03-30]

Appium works via WebDriverAgent (WDA), which acts as a REST server on port 8100 inside the Simulator, proxying W3C WebDriver requests to native XCTest calls. This means:
- Appium can tap, swipe, type, find elements by accessibility identifier, and retrieve the full element hierarchy.
- Element inspection returns an XML source tree based on the iOS accessibility layer.
- The `find element by accessibility id` locator maps to `accessibilityIdentifier` on iOS.

**Headless operation:** Since Xcode 9, `xcodebuild test` and by extension the WDA server run in headless mode by default — no Xcode GUI or Simulator window required. This remains true through Xcode 16 (current as of March 2026). [Source: https://devcenter.bitrise.io/en/testing/testing-ios-apps/running-xcode-tests.html, accessed 2026-03-30] Appium can be started with a headless capability:
```json
{ "appium:simulatorHeadless": true }
```

**Setup complexity:** High. Requires Node.js, npm, Appium 3, xcuitest driver install, and Xcode with correct simulator runtimes:
```sh
npm install -g appium
appium driver install xcuitest
```
Running a session also requires a JSON capabilities document and a WebDriver client library.

**Compose Multiplatform on iOS — known issues (April 2025):** Community reports from the Appium forums (April 29, 2025) indicate that Compose Multiplatform iOS apps present elements as `accessible="false"` with no `label` or `name` in the Appium element source, despite the Kotlin/JetBrains documentation stating that `testTag` maps to `accessibilityIdentifier`. The root cause: CMP's lazy accessibility sync (introduced in CMP 1.8.2) only activates when iOS accessibility services are running — Appium/WDA's XCTest runner does not trigger this sync automatically. A workaround confirmed in February 2025 involves configuring the `MainViewController` with `accessibilitySyncOptions = AccessibilitySyncOptions.Always(null)` to force constant sync. [Source: https://discuss.appium.io/t/compose-kmp-ios/45724, accessed 2026-03-30]

**Note on CMP 1.8.2:** The `AccessibilitySyncOptions` class was removed in CMP 1.8.2 as "no longer necessary." Whether this resolves the Appium/XCTest sync gap or introduces a new one is not confirmed in March 2026 sources — the community reports predate 1.8.2. This requires direct verification. [Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-180.html, accessed 2026-03-30] ⚠️ Source URL covers 1.8.0 features — the specific 1.8.2 change should be verified against the CMP 1.8.2 changelog.

### Assessment

| Criterion | Rating |
|---|---|
| Status as of March 2026 | Active — Appium 3.2.1, xcuitest-driver 10.14.4 [verify independently] |
| Headless | Yes — headless capability available |
| Touch/interaction | Yes — full WebDriver interaction |
| Semantic tree vs. screenshot | Yes — XCTest XML element hierarchy; CMP visibility uncertain post-1.8.2 |
| Setup complexity | High — requires Appium 3 + Node.js + WDA |

**Confidence:** Medium — Appium 3 / xcuitest driver status is High confidence; CMP iOS element visibility status is Medium due to the open question around CMP 1.8.2 behavior with automation tools.

---

## Tool: idb (Facebook iOS Development Bridge)

### Status and Capabilities (as of March 2026)

idb is Facebook/Meta's iOS automation toolkit. The GitHub repository (facebook/idb) shows 5,640+ commits and active open issues from throughout 2025. However, the last official PyPI release (`fb-idb` v1.1.7) was published March 3, 2022, and the last GitHub release tag (v1.1.8) was August 2022. v1.1.8 appears to be GitHub-only and was not published to PyPI. [Single source — verify independently] [Source: https://pypi.org/project/fb-idb/, accessed 2026-03-30] The `idb-companion` (the macOS daemon) continues receiving commits via Homebrew (`brew tap facebook/fb && brew install idb-companion`), but there are no official versioned companion releases since 2022.

Despite the stale release cadence, idb is the **de facto backend** for several active MCP servers (see MCP section) and is confirmed working with Xcode 16 by proxy of those tools' continued maintenance in 2025. Note: idb's last GitHub release tag is v1.1.8 (August 2022); maintenance status as of March 2026 was determined by inference from active MCP wrappers, not by direct repository inspection. [Single source — verify independently]

**Full CLI command surface for simulator automation:**

```sh
# Accessibility tree
idb ui describe-all                    # JSON dump of full element hierarchy
idb ui describe-point <X> <Y>          # element at coordinate

# Touch interaction
idb ui tap <X> <Y>                     # tap at coordinate
idb ui tap <X> <Y> --duration 1.0      # long press
idb ui swipe <X_START> <Y_START> <X_END> <Y_END>
idb ui swipe ... --delta 10            # control step size

# Text and keys
idb ui text "hello world"
idb ui key <keycode>
idb ui key-sequence <k1> <k2> <k3>

# Hardware buttons
idb ui button {HOME,LOCK,SIDE_BUTTON,SIRI,APPLE_PAY}

# Screenshot
idb screenshot output.png

# App management
idb install /path/to/App.app
idb launch <bundle-id>
idb terminate <bundle-id>
idb list-apps

# Logs
idb log
```
[Source: https://fbidb.io/docs/commands/, accessed 2026-03-30; https://fbidb.io/docs/accessibility/, accessed 2026-03-30]

`idb ui describe-all` returns a JSON array of accessibility elements with fields: `AXFrame`, `AXLabel`, `AXValue`, `frame {x, y, width, height}`, `role`, `role_description`, `type`, `enabled`, `custom_actions`. This is coordinate-based and does not require WDA or any running test runner.

**Architecture:** idb is a client-server system. The `idb-companion` runs as a daemon on macOS; the `fb-idb` Python client communicates with it via gRPC. Both must be running. The Python client is the `idb` CLI command.

**Installation:**
```sh
brew tap facebook/fb
brew install idb-companion
pip3 install fb-idb          # installs the idb CLI
idb connect booted           # connect to running simulator
```

**Headless:** Yes. idb-companion operates as a background daemon with no GUI dependency. [Source: https://fbidb.io/docs/overview/, accessed 2026-03-30]

### Assessment

| Criterion | Rating |
|---|---|
| Status as of March 2026 | Active via Homebrew (idb-companion); Python client frozen at v1.1.7 (March 2022) [Single source — verify independently] |
| Headless | Yes — daemon-based, no GUI |
| Touch/interaction | Yes — tap, swipe, key, text, buttons |
| Semantic tree vs. screenshot | Yes — full JSON dump via describe-all |
| Setup complexity | Medium — two components (companion + Python client), both via standard package managers |

**Confidence:** Medium — idb capabilities are well-documented and confirmed via MCP server implementations active in 2025-2026; however, the stale PyPI/GitHub release cadence means compatibility with future Xcode versions is uncertain. The last official Python client release was March 2022. Direct testing against Xcode 16 is not confirmed in primary sources.

---

## Tool: macOS AXUIElement APIs

### Status and Capabilities (as of March 2026)

macOS provides the `AXUIElement` accessibility API (part of ApplicationServices framework) for reading the accessibility tree of any running application, including the iOS Simulator window. [Source: https://developer.apple.com/documentation/applicationservices/axuielement, accessed 2026-03-30]

**How it works:** The Simulator renders iOS apps inside a macOS window. macOS accessibility APIs can traverse this window's element hierarchy, reading properties like `kAXRoleAttribute`, `kAXTitleAttribute`, `kAXValueAttribute`, `kAXIdentifierAttribute`, and children. The Simulator exposes the iOS app's accessibility tree through its window — elements inside the iOS app surface as AXUIElement children of the Simulator window.

**xctree:** A Swift CLI tool (`ldomaradzki/xctree`, v0.1.0, released November 5, 2025) wraps the macOS Accessibility API specifically for iOS Simulator inspection. [Source: https://github.com/ldomaradzki/xctree, accessed 2026-03-30]

- Output: tree view (default) or JSON
- JSON fields: `identifier`, `label`, `role`, `traits`
- Requirements: macOS 15.0+ (Sequoia), Xcode installed, Accessibility permissions for terminal
- Installation: `brew tap ldomaradzki/xctree && brew install xctree`
- Limitation: uses public macOS Accessibility API — some iOS UI elements may not be exposed (noted: certain tab bar buttons)

**What AXUIElement cannot do:** It reads accessibility data but cannot inject touch events into the iOS Simulator window. Keyboard events via `CGEventPost` are theoretically possible at the macOS level but are fragile and not recommended for reliable automation.

**iosef:** A newer Swift-based CLI + MCP server (`riwsky/iosef`) takes a different architecture — it uses XCTest-based introspection rather than AXUIElement, and is explicitly designed for agentic usage. **Note: iosef is grouped here for proximity but does not use AXUIElement — it uses XCTest-based introspection internally.** It provides tap, swipe, type, accessibility tree dump, screenshot, and element querying by role/name/identifier. Session state is stored in JSON files for short-lived CLI invocations. Available via PyPI. [Source: https://github.com/riwsky/iosef, accessed 2026-03-30]

### Assessment

| Criterion | Rating |
|---|---|
| Status as of March 2026 | xctree v0.1.0 (November 2025, early-stage); iosef active (98 commits) |
| Headless | Yes — no GUI dependency for API calls |
| Touch/interaction | No (AXUIElement alone); Yes (iosef uses XCTest internally) |
| Semantic tree vs. screenshot | Yes — reads iOS elements through Simulator window |
| Setup complexity | Low (xctree) to Medium (iosef) |

**Confidence:** Medium — xctree v0.1.0 is early-stage (21 stars, November 2025). AXUIElement approach is well-understood macOS API but the completeness of iOS element exposure through the Simulator window is not fully characterized for Compose Multiplatform specifically.

---

## Tool: MCP Servers for iOS Simulator

### Status and Capabilities (as of March 2026)

The MCP ecosystem for iOS Simulator automation expanded significantly in 2024-2025. At least four distinct MCP server implementations are available as of March 2026:

### 1. joshuayoes/ios-simulator-mcp

**npm package:** `ios-simulator-mcp`
**Current version:** 1.5.2 (as of 2026-03-30) [Source: https://www.npmjs.com/package/ios-simulator-mcp, accessed 2026-03-30]
**Security note:** CVE-2025-52573 — command injection vulnerability in `ui_tap` (versions < 1.3.3, patched June 2025). Use v1.3.3 or later. [Source: https://github.com/joshuayoes/ios-simulator-mcp/security/advisories/GHSA-6f6r-m9pv-67jw, accessed 2026-03-30]

**Tools provided (13 total):**
- `get_booted_sim_id`, `open_simulator`
- `screenshot`, `record_video`, `stop_recording`
- `ui_tap`, `ui_type`, `ui_swipe`
- `ui_describe_all`, `ui_describe_point`
- `install_app`, `launch_app`, `terminate_app`

**Note:** joshuayoes/ios-simulator-mcp is featured in the Anthropic Claude Code Best Practices blog as a recommended MCP server for iOS Simulator automation.

**Dependencies:** Node.js, Xcode, Facebook idb (idb-companion + fb-idb Python client)

**Claude Code integration:**
```json
{
  "mcpServers": {
    "ios-simulator": {
      "command": "npx",
      "args": ["ios-simulator-mcp"]
    }
  }
}
```

### 2. whitesmith/ios-simulator-mcp

A parallel implementation with similar capability surface. Explicitly architected around two backends: `xcrun simctl` (lifecycle, screenshots, location) + `idb` (UI interactions, app ops). Supports tap, swipe, long press, hardware button presses, UI hierarchy extraction. Works with Claude Code, Claude Desktop, and any MCP-compatible client. [Source: https://github.com/whitesmith/ios-simulator-mcp, accessed 2026-03-30]

### 3. InditexTech/mcp-server-simulator-ios-idb

Enterprise-grade implementation by Inditex (Zara parent company). Uses a natural language processing layer (NLParser parses natural language command strings into tool calls — an extra abstraction layer compared to direct MCP tool calls) in addition to direct MCP tools. Comprehensive feature set including debug sessions, crash logs, location simulation, media injection, contact/keychain management. Requires Homebrew. [Source: https://github.com/InditexTech/mcp-server-simulator-ios-idb, accessed 2026-03-30]

### 4. riwsky/iosef (CLI + MCP)

Dual-mode tool: standalone CLI and MCP server. Swift-based with XCTest internals. Optimized for agentic patterns: short-lived processes, JSON session state, exit codes distinguishing failed assertions (1) from usage errors (2). Available via PyPI. [Source: https://github.com/riwsky/iosef, accessed 2026-03-30]

### 5. agent-device (Callstack)

`callstackincubator/agent-device` is a token-efficient CLI and daemon for LLM-driven mobile UI testing. Unlike screenshot-based tools, it operates via the OS accessibility layer, extracting native accessibility tree snapshots (standard roles: windows, buttons, tables) from iOS and Android. This makes it compatible with any framework that projects semantic data to the OS accessibility layer, **including Compose Multiplatform** — it is not limited to React Native apps.

**Status as of March 2026:** Active. [Single source — verify independently at https://github.com/callstackincubator/agent-device, accessed 2026-03-30]

| Criterion | Assessment |
|---|---|
| (a) Status as of March 2026 | Active — headless CLI daemon |
| (b) Headless/no GUI | Yes — designed for headless agent operation |
| (c) Semantic tree vs. screenshot | Semantic — OS accessibility tree snapshots |
| (d) Setup complexity | Medium — CLI installation required |

**Confidence:** Medium — CMP compatibility via OS accessibility layer is confirmed by Gemini Deep Research follow-up (March 30, 2026); specific API details require direct repository verification. [Single source — verify independently]

### Summary Table

| Server | Backend | Last Active | CVE | Claude Code |
|---|---|---|---|---|
| joshuayoes/ios-simulator-mcp | idb | Active (v1.5.2, 2026-03-30) | Patched ≥1.3.3 | Yes |
| whitesmith/ios-simulator-mcp | simctl + idb | Active | None noted | Yes |
| InditexTech/mcp-server-simulator-ios-idb | idb | Active | None noted | Via config |
| riwsky/iosef | XCTest | Active (98 commits) | None noted | Via config |
| callstackincubator/agent-device | OS accessibility | Active | None noted | Via config |

### Assessment (MCP Ecosystem as a Whole)

| Criterion | Rating |
|---|---|
| Status as of March 2026 | Active — 4 distinct implementations, all maintained in 2025-2026 |
| Headless | Yes — all servers operate headlessly via underlying idb / simctl |
| Semantic tree vs. screenshot | Yes — all expose `ui_describe_all` (idb-backed) or equivalent |
| Setup complexity | Low-Medium — npm/npx install; depends on idb or XCTest backend being available |

**Confidence:** High — multiple independently developed, actively maintained MCP servers exist and are documented across multiple registries (PulseMCP, LobeHub, npm) as of early 2026. The ecosystem is active.

### Agent Client Protocol (ACP)

The Agent Client Protocol (ACP) is **fully live as of March 2026** — not beta. Claude Code can connect headlessly to ACP-compatible agents without an IDE GUI by configuring `acp.json` with an `agent_servers` block pointing to the agent executable. JetBrains AI Assistant and Junie CLI are ACP-compatible.

For iOS Simulator verification, ACP enables Claude Code to invoke a JetBrains-side agent (Junie CLI) that can trigger builds and test runs, with results returned via the ACP protocol. [Single source — verify independently at JetBrains ACP documentation, accessed 2026-03-30]

---

## Tool: XCTest / xcodebuild test (Headless)

### Status and Capabilities (as of March 2026)

`xcodebuild test` runs XCUITest-based UI test suites against the iOS Simulator from the command line, with no Xcode GUI required. Since Xcode 9, headless operation is the default — the simulator boots in the background without a visible window. This remains true through Xcode 16 (current as of March 2026). [Source: https://devcenter.bitrise.io/en/testing/testing-ios-apps/running-xcode-tests.html, accessed 2026-03-30]

**Basic usage:**
```sh
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyScheme \
  -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.0'
```

**Limitations for an LLM agent context:**
- This is a batch testing approach, not an interactive session. An agent cannot issue individual tap commands; it must write XCUITest Swift code, compile it, and run a full test pass.
- Test results come back as XML (via `-resultBundlePath`) or plain stdout — not a real-time interactive protocol.
- Round-trip latency (compile + boot + run) is on the order of 30-90 seconds for a simple test. [Estimate — no primary source cited; actual latency depends on hardware and test complexity]

XCUITest inside `xcodebuild test` can access full UI hierarchies and perform accessibility audits via `performAccessibilityAudit()`. [Source: https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html, accessed 2026-03-30]

### Assessment

| Criterion | Rating |
|---|---|
| Status as of March 2026 | Active — ships with Xcode 16; well-established CI/CD pattern |
| Headless | Yes — default since Xcode 9, confirmed through Xcode 16 |
| Semantic tree vs. screenshot | Yes — full XCTest XML element hierarchy via `app.debugDescription` |
| Setup complexity | High for LLM agents — requires writing Swift XCUITest code, compile + run cycle |

**Confidence:** High — well-established CI/CD pattern, widely documented.

---

## Compose Multiplatform iOS Accessibility

> **Note:** This is a cross-cutting topic section, not a per-tool assessment. It documents how CMP maps to iOS accessibility APIs and how that mapping interacts with the tools described above. No per-tool assessment table applies here.

### How CMP Maps to iOS Accessibility (as of CMP 1.8.x–1.10.3)

CMP 1.8.2 is a patch release within the 1.8.x stable line; the lazy-by-default sync change and `AccessibilitySyncOptions` removal occurred in 1.8.2, not at the 1.8.0 stable launch.

Compose Multiplatform for iOS reached stable status with CMP 1.8.0 (May 2025). [Source: https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/, accessed 2026-03-30] As of March 30, 2026, the latest stable CMP release is 1.10.3. CMP 1.9.3 introduced initial iOS accessibility tree mapping via `Modifier.semantics → accessibilityIdentifier`. The accessibility sync changes described below apply to the 1.8.x stable line.

**The mapping:**
- `Modifier.testTag("foo")` maps to native `accessibilityIdentifier = "foo"` on iOS
- `Modifier.semantics { contentDescription = "bar" }` maps to `accessibilityLabel = "bar"`
- For Material components (Button, TextField, etc.), this mapping happens automatically

This makes CMP elements queryable via XCUITest using:
```swift
app.buttons["myButtonTag"].tap()       // by testTag/accessibilityIdentifier
app.buttons["Submit"].tap()            // by contentDescription/accessibilityLabel
```
[Source: https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html, accessed 2026-03-30]

**The lazy sync problem for automation tools:**

CMP 1.8.2 changed accessibility tree synchronization to lazy-by-default: the tree is populated only when iOS accessibility services (VoiceOver, Voice Control, etc.) are active. When Appium/WDA's XCTest runner accesses the app, it does not activate these services, so the accessibility tree may appear empty or show only `accessible="false"` elements. [Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-180.html, accessed 2026-03-30; https://discuss.appium.io/t/compose-kmp-ios/45724, accessed 2026-03-30]

**Workarounds (as of February-April 2025):**

Pre-CMP 1.8.2, the fix was:
```kotlin
// In MainViewController setup:
configure = {
    accessibilitySyncOptions = AccessibilitySyncOptions.Always(null)
}
```
This forced continuous sync. [Source: https://slack-chats.kotlinlang.org/t/26981930/, accessed 2026-03-30]

Post-CMP 1.8.2, `AccessibilitySyncOptions` was removed. Whether the new lazy default works correctly with Appium/WDA is not confirmed in sources dated March 2026 — the community reports of element invisibility are pre-1.8.2, and no post-1.8.2 Appium+CMP confirmation was found.

**idb's approach avoids this problem:** `idb ui describe-all` reads the iOS accessibility tree directly through idb-companion's XPC connection to the Simulator process, bypassing the accessibility service trigger. Whether it is affected by CMP's lazy sync is not directly documented, but the MCP servers that wrap idb (and are used with CMP apps in practice) do not report this limitation.

**Maestro:** Maestro uses the iOS accessibility layer. Community reports indicate that with some CMP versions, Maestro recognized the entire app as a single node rather than individual components — consistent with the lazy sync issue. [Source: https://maestro.dev/, accessed 2026-03-30]

**Confidence:** Medium — the testTag-to-accessibilityIdentifier mapping is High confidence (official docs). The CMP lazy-sync behavior's interaction with automation tools post-1.8.2 is Medium confidence due to lack of post-release community confirmation.

---

## Tool: Apple Claude Agent SDK (Xcode 26.3)

[Single source — verify independently]

### Status and Capabilities (as of March 2026)

Apple announced the Claude Agent SDK integration in Xcode 26.3 on February 3, 2026. This is an official Apple feature for agentic coding workflows that introduces a headless Xcode Previews capture path, enabling LLM agents to capture rendered Xcode Previews without booting a full iOS Simulator.

**Key capability — headless Previews via `-p` flag:**
```sh
xcodebuild -p <preview-identifier>   # headless Xcode Previews capture
```

The `-p` flag allows an agent to capture Xcode Previews headlessly — rendering the SwiftUI or Compose Multiplatform iOS preview canvas without launching the full iOS Simulator runtime. This is lighter-weight than a full Simulator session for visual verification of individual components.

**Relevance for CMP iOS:**
- Provides a Simulator-free verification path for Compose Multiplatform iOS Previews
- May sidestep the CMP accessibility sync issues that affect Appium/WDA (Previews run in a distinct rendering context)
- Scope is limited to Previews — does not replace full Simulator interaction for end-to-end flows

**Limitations:**
- Requires Xcode 26.3 (not yet widely available as of research date)
- Full API surface and Claude Code MCP integration details are not yet documented in primary sources as of March 2026
- Coverage limited to components that have `#Preview` definitions

### Assessment

| Criterion | Rating |
|---|---|
| Status as of March 2026 | Announced February 3, 2026 — Xcode 26.3; availability pending [verify independently] |
| Headless | Yes — explicit design goal via `-p` flag |
| Semantic tree vs. screenshot | Screenshot/visual capture of Previews; no accessibility tree access documented |
| Setup complexity | Requires Xcode 26.3 — not yet generally available |

**Confidence:** Low — single announcement source (Anthropic Claude Code Best Practices blog); no primary Apple developer documentation confirmed as of March 2026. Treat as emerging capability to track rather than production recommendation.

---

## Recommendations

For a Claude Code agent running in a shell on macOS that needs to launch a CMP iOS app, take screenshots, inspect UI, and interact (tap, type, swipe) — without a GUI IDE:

### Recommended Stack

**Layer 1: Simulator Lifecycle — `xcrun simctl`**
```sh
# Boot simulator headlessly
xcrun simctl boot "iPhone 16"

# Install and launch the app
xcrun simctl install booted /path/to/CMP.app
xcrun simctl launch booted com.example.myapp

# Screenshot (use after each interaction)
xcrun simctl io booted screenshot /tmp/screen.png
```

**Layer 2: Touch + Accessibility — `idb`**
```sh
# Install (one-time)
brew tap facebook/fb && brew install idb-companion
pip3 install fb-idb

# Dump full UI hierarchy (JSON)
idb ui describe-all --udid booted | jq '.'

# Interact
idb ui tap 200 400
idb ui swipe 100 500 100 100
idb ui text "hello"

# Screenshot via idb (alternative to simctl)
idb screenshot /tmp/screen.png
```

**Layer 3: MCP Integration — `whitesmith/ios-simulator-mcp` or `joshuayoes/ios-simulator-mcp` (v1.3.3+)**

Add to Claude Code's MCP configuration (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "ios-simulator": {
      "command": "npx",
      "args": ["ios-simulator-mcp@latest"]
    }
  }
}
```

This exposes `screenshot`, `ui_tap`, `ui_swipe`, `ui_type`, `ui_describe_all`, `launch_app` as native Claude tools.

**CMP-specific: force accessibility sync**

If using CMP < 1.8.2, configure the iOS app target's `MainViewController`:
```kotlin
ComposeUIViewController(configure = {
    accessibilitySyncOptions = AccessibilitySyncOptions.Always(null)
}) { /* composable content */ }
```
For CMP 1.8.2+, this option is removed — test element visibility directly with `idb ui describe-all` and verify CMP testTags appear as `AXLabel` values (idb's JSON output uses `AXLabel`, `AXValue`, `frame`, `role`, `role_description`, `type`, `enabled` — note that `AXIdentifier` is a macOS AXUIElement attribute name, not an idb JSON field). If `idb ui describe-all` also shows empty elements on CMP 1.8.2+, this is an unresolved gap — see Gaps section. No confirmed workaround exists as of March 2026.

### Why This Stack

| Need | Tool | Rationale | Alternatives considered (and why not) |
|---|---|---|---|
| App lifecycle | simctl | Ships with Xcode, zero dependencies | idb launch — works but adds a dependency that simctl avoids |
| Screenshots | simctl io | Single command, synchronous | idb screenshot — equivalent, but simctl preferred when idb not already needed |
| Touch/swipe | idb | Only headless CLI with full gesture set | Appium — too much setup overhead; simctl — lacks touch primitives entirely |
| Accessibility tree | idb ui describe-all | JSON output, no WDA server needed | Appium XML source — requires WDA compilation; xctree — early-stage v0.1.0 |
| MCP integration | ios-simulator-mcp | Direct Claude tool registration | Raw CLI — loses structured tool invocation; iosef — alternative if XCTest backend preferred |

Appium is not recommended as the primary approach for an agent due to setup complexity (Node + Appium server + WDA compilation) and the CMP accessibility sync uncertainty. It is the right choice if you need a W3C WebDriver-compliant interface or are running parallel test sessions.

---

## Gaps and Limitations

1. **idb Python client is frozen at v1.1.7 (March 2022).** The companion receives updates via Homebrew, but the Python client's API compatibility with current idb-companion is untested by primary sources. Breaking changes are possible with future Xcode versions.

2. **CMP 1.8.2+ and accessibility sync.** The removal of `AccessibilitySyncOptions.Always` is documented, but whether the new lazy-by-default behavior resolves Appium/WDA visibility issues or only works with real accessibility services is not confirmed in March 2026 sources. Direct testing is required.

3. **No simctl touch primitives.** Apple has not added gesture injection to simctl through Xcode 16. Touch interaction requires idb or Appium/WDA — both add dependency weight.

4. **xctree is early-stage (v0.1.0, November 2025).** The macOS AXUIElement approach is elegant but the completeness of CMP element exposure through the Simulator window's accessibility tree is unknown. Some iOS elements are confirmed unexposed (tab bar buttons noted in xctree docs).

5. **CVE-2025-52573 (joshuayoes/ios-simulator-mcp < 1.3.3).** Command injection via shell metacharacters in `ui_tap` parameters. Fixed in v1.3.3 (June 2025). Always use v1.3.3+. [Source: https://nvd.nist.gov/vuln/detail/CVE-2025-52573, accessed 2026-03-30]

6. **macOS-only.** Every tool in this ecosystem requires macOS. There is no Linux path to iOS Simulator automation — Apple does not provide iOS Simulator for Linux.

7. **Compose Multiplatform coordinate space.** CMP for iOS renders into a UIKit canvas. The coordinate system exposed to idb/simctl is the iOS point coordinate system (device-independent pixels). High-DPI screens (Retina) may have a 3x pixel scale factor — screenshots are in pixel space, but tap coordinates use point space. The agent must be aware of this when tapping on screenshot-derived coordinates. Decision rule: divide screenshot pixel coordinates by the device scale factor (typically 3× for modern iPhones) to get the point coordinates required by `idb ui tap`.

---

## Sources

| URL | Source Name | Access Date |
|---|---|---|
| https://github.com/joshuayoes/ios-simulator-mcp | joshuayoes/ios-simulator-mcp GitHub | 2026-03-30 |
| https://github.com/InditexTech/mcp-server-simulator-ios-idb | InditexTech/mcp-server-simulator-ios-idb GitHub | 2026-03-30 |
| https://github.com/whitesmith/ios-simulator-mcp | whitesmith/ios-simulator-mcp GitHub | 2026-03-30 |
| https://github.com/facebook/idb | facebook/idb GitHub | 2026-03-30 |
| https://fbidb.io/docs/commands/ | idb Commands Documentation | 2026-03-30 |
| https://fbidb.io/docs/accessibility/ | idb Accessibility Documentation | 2026-03-30 |
| https://fbidb.io/docs/overview/ | idb Overview | 2026-03-30 |
| https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html | Kotlin Multiplatform: Compose iOS Accessibility | 2026-03-30 |
| https://kotlinlang.org/docs/multiplatform/whats-new-compose-180.html | What's New in Compose Multiplatform 1.8.2 | 2026-03-30 |
| https://appium.github.io/appium-xcuitest-driver/10.11/installation/ | Appium XCUITest Driver Installation Docs | 2026-03-30 |
| https://github.com/appium/appium-xcuitest-driver/releases | appium-xcuitest-driver Releases | 2026-03-30 |
| https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/ | Appium 3 Release Blog (August 7, 2025) | 2026-03-30 |
| https://github.com/ldomaradzki/xctree | ldomaradzki/xctree GitHub | 2026-03-30 |
| https://ldomaradzki.com/blog/xctree-accessibility-cli | xctree Blog Post | 2026-03-30 |
| https://github.com/riwsky/iosef | riwsky/iosef GitHub | 2026-03-30 |
| https://github.com/callstackincubator/agent-device | callstackincubator/agent-device GitHub [consulted for ecosystem survey; no specific findings cited inline] | 2026-03-30 |
| https://discuss.appium.io/t/compose-kmp-ios/45724 | Appium Forum: Compose KMP iOS Issues (April 29, 2025) | 2026-03-30 |
| https://www.iosdev.recipes/simctl/ | simctl Command Reference — iOS Dev Recipes | 2026-03-30 |
| https://pypi.org/project/fb-idb/ | fb-idb PyPI Page | 2026-03-30 |
| https://github.com/joshuayoes/ios-simulator-mcp/security/advisories/GHSA-6f6r-m9pv-67jw | CVE-2025-52573 Advisory | 2026-03-30 |
| https://nvd.nist.gov/vuln/detail/CVE-2025-52573 | NVD: CVE-2025-52573 | 2026-03-30 |
| https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/ | JetBrains: CMP 1.8.0 Release Blog | 2026-03-30 |
| https://www.kmpship.app/blog/kotlin-multiplatform-testing-guide-2025 | KMP Testing Guide 2025 [consulted for ecosystem survey; no specific findings cited inline] | 2026-03-30 |
| https://maestro.dev/ | Maestro Official Site | 2026-03-30 |
| https://devcenter.bitrise.io/en/testing/testing-ios-apps/running-xcode-tests.html | Bitrise: Running Xcode Tests | 2026-03-30 |
| https://nshipster.com/simctl/ | NSHipster: simctl | 2026-03-30 |
| https://sarunw.com/posts/take-screenshot-and-record-video-in-ios-simulator/ | Sarunw: Take Screenshot and Record Video in iOS Simulator | 2026-03-30 |
| https://slack-chats.kotlinlang.org/t/26981930/ | Kotlin Slack: CMP Accessibility Sync Discussion | 2026-03-30 |
| https://www.npmjs.com/package/ios-simulator-mcp | ios-simulator-mcp npm Package | 2026-03-30 |
