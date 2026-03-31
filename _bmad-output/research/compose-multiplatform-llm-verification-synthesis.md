---
synthesis_date: 2026-03-30
source_documents:
  - _bmad-output/research/A1-ios-simulator.md
  - _bmad-output/research/A2-android-emulator.md
  - _bmad-output/research/A3-jetbrains-ai-mcp.md
  - _bmad-output/research/A4-compose-web-proxy.md
  - _bmad-output/research/A5-computer-use-visual.md
  - _bmad-output/research/A6-cross-platform-frameworks.md
  - _bmad-output/research/gemini-session.md
  - docs/research/LLM Agent Compose Multiplatform Verification.md
synthesizer: Claude Sonnet 4.6 (synthesis agent)
avfl_passes_completed: 5
---

# Compose Multiplatform LLM-Agent Verification — Synthesis
## Research Date: March 30, 2026

---

## Executive Summary

**iOS Simulator:** Start with `joshuayoes/ios-simulator-mcp` v1.5.2 (npx) for live MCP interaction; use Compose UI Test (`./gradlew iosSimulatorArm64Test`) for scripted assertions. CMP 1.10.3 fixes the iOS flat accessibility hierarchy regression (#2848). Avoid Maestro for CMP iOS (friction — issue #1549 still open). The Apple Claude Agent SDK (Xcode 26.3) offers headless Xcode Preview capture but is not yet widely available as of March 30, 2026. [Single source — verify independently]

**Android Emulator:** `adb` for lifecycle and input, `adb shell uiautomator dump` for accessibility tree (requires `testTagsAsResourceId = true` in app), and `mobile-mcp` or Maestro 2.3.0 for MCP-native agent interaction. Android is the most reliable CMP automation target.

**Desktop (macOS/JVM):** Pure Gradle via `./gradlew :YOUR_MODULE:jvmTest` is the cleanest headless path. Compose Hot Reload (`./gradlew :YOUR_MODULE:hotRunJvm`) enables rapid iterative verification. The JetBrains IntelliJ MCP server (IDE must be open) provides build and code-analysis tools to Claude Code. (Note: substitute your actual Gradle module name for `:YOUR_MODULE:` — standard CMP templates use `:composeApp:`.)

**Compose for Web:** Viable proxy for business logic, navigation, and form flows. Playwright against the Compose accessibility overlay works for annotated composables but fails silently for unannotated elements. Not appropriate for platform-API-heavy apps or pixel-fidelity testing. Requires 15–90 second Kotlin recompilation per change (no hot reload on web).

As of March 2026, no single tool spans all four platforms without trade-offs. The best cross-cutting approach is a layered stack: `mobile-mcp` or `ios-simulator-mcp` for iOS/Android live interaction, Compose UI Test via Gradle CLI for semantic-precise assertions, and Playwright for the Web proxy. Computer Use API (macOS launch March 23, 2026) provides a universal fallback for any platform but at higher cost and latency. Note: `mobile-mcp` CMP iOS compatibility is inferred from its accessibility-tree approach, not officially documented — see the Cross-Cutting Recommendation for the full caveat before committing to it for CMP iOS.

---

## How to Read This Document

Provenance conventions used throughout:

- `[Source: URL, accessed 2026-03-30]` — primary source citation carried from agent reports
- `[Gemini R1 Q#]` or `[Gemini R2 Q#]` — verified in Gemini Deep Research follow-up round 1 or 2
- `[Single source — verify independently]` — only one source located; treat with caution
- `[Conflicting sources — see note]` — conflict between agents surfaced and resolved inline
- **Confidence ratings** appear at the end of each platform section: High / Medium / Low with rationale

The **Key Conflict Resolutions** section at the end of this document is the authoritative summary of all resolved conflicts. Inline `[Conflicting sources — see note]` tags are shorthand pointers; refer to that section for the complete resolution.

---

## Platform Recommendations

### iOS Simulator

#### Recommended Stack

**Layer 1 — Simulator Lifecycle (`xcrun simctl`)**

Ships with Xcode. No extra dependencies. Handles boot, install, launch, and screenshots.

```sh
xcrun simctl boot "iPhone 16"
xcrun simctl install booted /path/to/CMP.app
xcrun simctl launch booted com.example.myapp
xcrun simctl io booted screenshot /tmp/screen.png
```

[Source: https://www.iosdev.recipes/simctl/, accessed 2026-03-30]

**Layer 2 — Touch and Accessibility (`idb-companion` via Homebrew)**

`fb-idb` v1.1.7 (PyPI) is **non-functional as of March 30, 2026** for many users — it crashes with `ImportError` in `companion_spawner` (Issue #902, late March 2026). The `idb-companion` Homebrew package continues to receive updates. Use the companion via MCP wrappers rather than the raw Python CLI.

[Gemini R2 Q3]

**Layer 3 — MCP Integration (primary recommendation)**

`joshuayoes/ios-simulator-mcp` v1.5.2 is the recommended primary MCP server. It wraps `xcrun simctl` and `idb-companion`, is featured in Anthropic's Claude Code Best Practices blog, and exposes 13 tools including `ui_describe_all`, `ui_tap`, `ui_swipe`, `ui_type`, `screenshot`, `launch_app`.

[Source: https://github.com/joshuayoes/ios-simulator-mcp, accessed 2026-03-30] [Gemini R2 Q4]

**Security note:** CVE-2025-52573 affects versions < 1.3.3 (command injection in `ui_tap`). Always use 1.3.3+. [Source: https://nvd.nist.gov/vuln/detail/CVE-2025-52573, accessed 2026-03-30] [Single source — verify independently]

Add to Claude Code's MCP configuration:

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

**Alternative MCP options:**

- `InditexTech/mcp-server-simulator-ios-idb` v1.0.1 (April 2025) — enterprise-grade idb wrapper; may be more reliable than raw fb-idb Python client [Gemini R2 Q3]
- `callstackincubator/agent-device` — platform-agnostic CLI daemon using OS accessibility layer; inferred to work with CMP via native accessibility projection, not RN-only [Gemini R1 Q6; Source: https://github.com/callstackincubator/agent-device, accessed 2026-03-30]
- `riwsky/iosef` — XCTest-based alternative with short-lived CLI invocations [Source: https://github.com/riwsky/iosef, accessed 2026-03-30]
- Appium 3.2.2 + XCUITest driver — standard XCTest XML output, mature tooling; high setup complexity but reported CMP iOS support via forum discussions. [Source: https://github.com/appium/appium/releases, accessed 2026-03-30] [Gemini R2 Q2] [Single source — verify independently] (Appium uses WebDriver protocol, not MCP — included here as a non-MCP alternative for iOS XCTest-based testing)
- `whitesmith/ios-simulator-mcp` — community fork of the joshuayoes MCP server with additional tools. [Source: https://github.com/whitesmith/ios-simulator-mcp, accessed 2026-03-30] [Single source — verify independently]

#### CMP 1.10.3 iOS Accessibility — Critical Finding

CMP 1.10.3 **fixes** the iOS flat accessibility hierarchy regression: "Traversal groups now convert into an additional node in the accessibility hierarchy #2848." This regression existed from CMP 1.8.1 through 1.9.0 (the only 1.9.x release). [Single source — verify independently; regression start version 1.8.1 is from the issue tracker, not independently confirmed in release notes]

[Source: https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.3, accessed 2026-03-30] [Gemini R2 Q1]

[Conflicting sources — see Key Conflict Resolutions, Conflict 1]

**Maestro friction remains despite structural fix:** Maestro 2.3.0 issue #1549 is still open. Maestro Studio has random crashes on CMP iOS screen transitions and still sometimes requires coordinate fallbacks (`tapOn: point: 50%,81%`). The accessibility tree projection is correct; Maestro's internal tooling hasn't caught up. Do not rely on Maestro for CMP iOS semantic element selection until #1549 is closed.

[Gemini R2 Q9; Source: https://github.com/mobile-dev-inc/maestro/issues/1549, accessed 2026-03-30]

#### Semantic Property Mapping (CMP → iOS)

| CMP annotation | iOS accessibility attribute |
|---|---|
| `Modifier.testTag("foo")` | `accessibilityIdentifier = "foo"` |
| `Modifier.semantics { contentDescription = "bar" }` | `accessibilityLabel = "bar"` |

[Source: https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html, accessed 2026-03-30]

Note: The mapping above describes the CMP → iOS system accessibility attribute layer. The idb JSON key used to surface `accessibilityIdentifier` in `idb ui describe-all` output is a separate question — see Gap Map #2 (idb field names unresolved).

**idb JSON field names for `ui describe-all` are unresolved.** Whether `testTag` maps to `AXLabel`, `AXIdentifier`, or another field in idb's JSON output cannot be asserted without live testing against a booted simulator. Do not hardcode field names until empirically verified. To investigate empirically: boot a simulator with a CMP 1.10.3 app installed and run `idb ui describe-all` to inspect the raw JSON output and identify which field carries the `testTag` value.

[Gemini R2 Q7]

#### Future path: Apple Claude Agent SDK (Xcode 26.3, not yet widely available)

This path is not available in most environments today — Xcode 26.3 is not yet widely available as of March 30, 2026. Treat as a near-future option, not a current fallback.

Apple's official Claude Agent SDK in Xcode 26.3 (announced February 3, 2026) supports headless Xcode Preview capture via a CLI flag — see Anthropic's announcement for exact syntax. [Single source — verify independently]

This is a lighter-weight verification path for individual CMP components that have `#Preview` definitions. It does not replace full Simulator interaction for end-to-end flows.

[Gemini R1 Q2; Source: https://www.anthropic.com/news/apple-xcode-claude-agent-sdk, accessed 2026-03-30] [Single source — verify independently]

#### Known iOS Gaps

1. **idb field names unresolved** — `idb ui describe-all` JSON key for `accessibilityIdentifier` is not confirmed; AXLabel vs. AXIdentifier unknown without live testing (see Gap Map #2)
2. **Maestro Studio friction** — Issue #1549 remains open; screen streaming instability and coordinate fallbacks still required for CMP iOS elements despite #2848 fix
3. **ACP + IDE bridge required** — No headless ACP path to iOS Simulator without a JetBrains IDE running as MCP bridge
4. **Xcode 26.3 not yet widely available** — Apple Claude Agent SDK (see "Future path: Apple Claude Agent SDK (Xcode 26.3, not yet widely available)" section above) cannot be used in most environments today

**Confidence: Medium.** MCP ecosystem is active and well-documented. idb Python client is broken (ImportError); MCP wrappers provide a more reliable path than raw idb. CMP 1.10.3 structural fix is confirmed. Remaining uncertainty: (1) idb JSON field names unresolved; (2) Maestro iOS friction persists (#1549 still open); (3) ACP + iOS requires a JetBrains IDE open as bridge — no standalone headless path; (4) Apple Claude Agent SDK (Xcode 26.3) not yet widely available.

---

### Android Emulator

#### Recommended Stack

**Layer 1 — Emulator Lifecycle and Input (`adb` + `emulator`)**

```bash
# Launch headlessly (no window, no audio)
~/Library/Android/sdk/emulator/emulator @Pixel8_API_35 -no-window -no-audio -no-boot-anim

# Wait for boot
adb wait-for-device && adb shell getprop sys.boot_completed  # returns "1"

# Screenshot
adb exec-out screencap -p > screen.png

# Touch input
adb shell input tap 540 960
adb shell input swipe 300 800 300 200 500
adb shell input text "hello"

# Kill
adb emu kill
```

[Source: https://developer.android.com/tools/adb, accessed 2026-03-30] [Source: https://developer.android.com/studio/run/emulator-commandline, accessed 2026-03-30]

Android Emulator latest stable: 36.4.9 (released February 10, 2026). [Source: https://developer.android.com/studio/releases/emulator, accessed 2026-03-30] [Single source — verify independently]

**Layer 2 — Accessibility Tree (`adb shell uiautomator dump`)**

```bash
adb exec-out uiautomator dump /dev/tty    # direct to stdout
```

**Critical app precondition:** CMP Android elements appear in the dump only when `testTagsAsResourceId = true` is set at the root composable. Without it, the entire Compose UI collapses to a single `<node class="androidx.compose.ui.platform.ComposeView">` with no children.

```kotlin
Scaffold(
    modifier = Modifier.semantics { testTagsAsResourceId = true }
) { /* all Modifier.testTag(...) composables */ }
```

[Source: https://developer.android.com/develop/ui/compose/testing/interoperability, accessed 2026-03-30]

**Layer 3 — MCP Integration**

Primary: `mobile-next/mobile-mcp` (`@mobilenext/mobile-mcp` via npm/npx; version not confirmed at research date — pin via npm lock file). Provides `mobile_list_elements_on_screen` (accessibility tree or screenshot fallback), plus tap, swipe, type, launch, install. Explicit Android Emulator support on macOS/Linux/Windows confirmed.

[Source: https://github.com/mobile-next/mobile-mcp, accessed 2026-03-30]

Alternative: `CursorTouch/Android-MCP` — lightweight, ADB + Android Accessibility API, no CV pipeline required; `SCREENSHOT_QUANTIZED` env var reduces image token cost. [Source: https://github.com/CursorTouch/Android-MCP, accessed 2026-03-30]

**Layer 4 — Maestro for scripted E2E (Android only)**

Maestro 2.3.0 (March 10, 2026) has solid Android CMP support. Write YAML flows, execute with `maestro test flow.yaml`. Maestro MCP server (`maestro mcp`) exposes flows directly as Claude tools.

```yaml
appId: com.example.myapp
---
- launchApp
- tapOn:
    id: "loginButton"     # matches testTag when testTagsAsResourceId=true
- inputText: "user@example.com"
- assertVisible:
    text: "Welcome"
- takeScreenshot: "post_login"
```

[Source: https://maestro.dev/, accessed 2026-03-30; https://github.com/mobile-dev-inc/maestro/releases, accessed 2026-03-30]

**Layer 5 — Compose UI Test via Gradle (highest semantic precision)**

For scripted assertions with full Compose semantics tree access (no `testTagsAsResourceId` required):

```bash
./gradlew :composeApp:connectedAndroidTest
```

Results in `build/test-results/` (JUnit XML) and `build/reports/tests/` (HTML). The agent reads XML output for pass/fail.

[Source: https://kotlinlang.org/docs/multiplatform/compose-test.html, accessed 2026-03-30]

#### Known Android Gaps

1. **`testTagsAsResourceId` required** — Entire Compose UI collapses to a single node without this flag in your app's debug build; must be added to app code before semantic testing works
2. **`mobile-mcp` version unconfirmed** — No pinned version available at research date; pin via npm lock file
3. **`agent-device` Android CMP unverified** — Inferred from OS accessibility approach; not specifically tested with CMP Android [Gemini R1 Q6]
4. **`connectedAndroidTest` requires a running device** — `./gradlew :composeApp:connectedAndroidTest` requires a running emulator or connected physical device; it does not start one automatically

**Confidence: High.** Android is the most reliable CMP automation target. All claims sourced from official Android documentation. The `testTagsAsResourceId` requirement is well-documented and the mechanism is stable.

---

### Desktop (macOS/JVM)

#### Recommended Stack

**Layer 1 — Pure Gradle (no IDE required)**

```bash
./gradlew :composeApp:jvmTest          # unit + compose UI tests
./gradlew :composeApp:desktopTest      # desktop-specific targets
./gradlew :composeApp:hotRunJvm        # start app with Hot Reload
./gradlew :composeApp:hotRunJvm --auto # continuous Hot Reload on file change
```

Compose Hot Reload became stable and bundled with the CMP Gradle plugin in CMP 1.10.0 (January 2026). It does not require a running IDE. Kotlin 2.1.20+ required.

[Source: https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/, accessed 2026-03-30]

**Layer 2 — JetBrains IntelliJ MCP Server (IDE required)**

IntelliJ IDEA 2025.2+ ships a built-in MCP server. Claude Code is officially listed as a supported client. Auto-configure from within the IDE at `Settings | Tools | MCP Server → Enable → Auto-Configure → Claude Code`.

Exposes 25+ tools including `execute_run_configuration`, `get_file_problems`, `execute_terminal_command`, `rename_refactoring`, and `search_in_files_by_regex`.

This path requires a running IntelliJ instance with the project open. There is no headless mode.

[Source: https://www.jetbrains.com/help/idea/mcp-server.html, accessed 2026-03-30]

**Layer 3 — Junie CLI (headless, beta March 2026)**

JetBrains' standalone coding agent, LLM-agnostic (supports Anthropic), runs from terminal without IDE. Useful for delegating JetBrains-specific code generation and analysis tasks from Claude Code via subprocess.

[Source: https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/, accessed 2026-03-30] [Single source — verify independently]

#### Desktop Accessibility Note

CMP 1.10.3 also fixes desktop (macOS/JVM) accessibility: VoiceOver wrong-button-click bugs (#2720, #2680) and `TextField` `contentDescription` now properly mapped to accessible name. Desktop Compose UI Test via `./gradlew :composeApp:jvmTest` (substitute your module name) works with `ComposeTestRule` (JUnit4 runner).

[Gemini R2 Q1; Source: https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.3, accessed 2026-03-30]

#### Known Desktop Gaps

1. JetBrains IntelliJ MCP Server requires a running IDE instance — not usable in headless CI pipelines (see Gap Map #12)
2. Junie CLI is in beta as of March 2026 — not production-stable
3. Computer Use API requires a live macOS display; headless/virtual display workarounds are not officially documented (cross-cutting — see also Gap Map #5)
4. No Linux target coverage in this synthesis — CMP Desktop on Linux is a valid target but no tools were evaluated

**Confidence: High.** Gradle-based testing is a well-established pattern. Hot Reload stable since CMP 1.10.0. IntelliJ MCP server is documented and shipped.

---

### Compose for Web

#### Recommended Stack (Proxy Strategy)

Compose for Web is used as a **verification proxy** for business logic and navigation, not as a native automation target. It has no single "recommended stack" equivalent to iOS/Android/Desktop because the Playwright + accessibility-overlay approach depends heavily on what the app annotates. The recommended proxy workflow:

1. Start the dev server: `./gradlew wasmJsBrowserDevelopmentRun` (available at `http://localhost:8080`)
2. Point Playwright + `@playwright/mcp` at the running app
3. Use `page.getByRole()` and `page.getByText()` for annotated elements (semantic access via accessibility overlay)
4. Screenshot fallback for unannotated elements

See the sections below for Playwright compatibility details, viability by app category, and known gaps.

[Source: https://playwright.dev/docs/accessibility-testing, accessed 2026-03-30]

#### Status (March 2026)

Web (Kotlin/Wasm) target is **Beta**, not Stable, in the current stable release (CMP 1.10.3). CMP 1.11.0 is also in Beta. The web target has been Beta since CMP 1.9.0 (September 2025). [Source: https://kotlinlang.org/docs/multiplatform/supported-platforms.html, accessed 2026-03-30] [Source: https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/, accessed 2026-03-30] Beta means: most APIs available, adoption encouraged for small-to-medium apps, breaking changes minimized but possible.

#### How Playwright Works Against Compose for Web

Compose for Web renders to a Skia canvas, not native DOM elements. Standard CSS/XPath selectors do not work. However, CMP 1.9.0 enabled an accessibility overlay by default. Playwright can query this overlay:

```javascript
// Works (if composable has contentDescription or text set)
page.getByRole('button', { name: 'Submit' })
page.getByText('Hello')
page.getByLabel('Search')

// Does NOT work
page.locator('button')       // no button DOM nodes exist
page.locator('#element-id')  // no Compose elements have DOM IDs
```

**The `testTag` → `data-testid` mapping is unconfirmed.** Whether `Modifier.testTag("my-tag")` exposes a `data-testid` attribute in the accessibility DOM for Playwright's `getByTestId()` is not documented in official sources.

[Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

#### Running the Dev Server for Agent Workflows

```bash
./gradlew wasmJsBrowserDevelopmentRun           # start at http://localhost:8080
./gradlew wasmJsBrowserDevelopmentRun --watch-fs -t  # with file-watch recompile
```

Compose Hot Reload does **not** support web targets. Each code change requires 15–90 second Kotlin recompilation. This is a significant agent workflow friction.

[Source: https://github.com/JetBrains/compose-hot-reload, accessed 2026-03-30]

Playwright headless Chromium can connect to the dev server at `http://localhost:8080` without special configuration. The `@playwright/mcp` server is compatible with Claude Code and operates on the accessibility tree. [Source: https://www.npmjs.com/package/@playwright/mcp, accessed 2026-03-30]

#### Viability by App Category

| Category | Web Proxy Viability | Notes |
|---|---|---|
| CRUD / forms / lists | High | Shared ViewModels, state, navigation all work |
| Navigation flows | High | Navigation 3 (CMP 1.10.0) supports web with browser back/forward |
| Architecture / ViewModel state | High | Identical across platforms |
| UI-heavy / animations | Medium | Logic proxy only; pixel rendering differs (Skia vs native) |
| Platform-API-heavy (camera, GPS, biometrics) | Low | Web `actual` implementations behave differently or throw `NotImplementedError` |

#### Known Web Gaps

1. Accessibility for scrollable containers and sliders: not yet supported
2. Traversal indexes: not yet supported on web
3. No Compose Hot Reload for web (JVM-only)
4. 5MB Wasm+Skia bundle download before first render — use `waitForLoadState('networkidle')` in CI
5. `testTag` → `data-testid` DOM mapping: unconfirmed [Single source — verify independently]
6. No community examples of Compose for Web used as a CI proxy for iOS/Android — strategy is novel

#### Fallback Options

- Computer Use API (`computer-use-2025-11-24`) — works against any visible browser window showing Compose for Web; visual-only approach, no semantic element access
- Compose UI Test via `wasmJsTest` Gradle task — semantic approach, but requires Kotlin/Wasm headless browser support (in development as of March 2026). [Source: https://kotlinlang.org/docs/multiplatform/compose-test.html, accessed 2026-03-30] [Single source — verify independently]

**Confidence: Medium.** Canvas rendering architecture and accessibility overlay are well-documented. Playwright automation viability is inferred from accessibility overlay behavior and Flutter Web analogies; no official Compose for Web + Playwright documentation exists as of March 2026. Real-world proxy strategy has no confirmed practitioners in the CMP community.

---

## Cross-Cutting Recommendation

**The recommended path that works across the most targets:**

| Target | Primary tool | Semantic access | Headless |
|---|---|---|---|
| iOS Simulator | `ios-simulator-mcp` v1.5.2 | Partial — tree available; testTag field names unresolved (Gap Map #2) | Yes |
| Android Emulator | `mobile-mcp` + `adb` | uiautomator dump (`testTagsAsResourceId`) | Yes |
| Desktop (JVM) | `./gradlew jvmTest` + Hot Reload (prefix `:composeApp:` for module-specific run) | Full Compose semantics | Yes (Gradle path) |
| Web (proxy) | Playwright + `@playwright/mcp` | Accessibility overlay | Yes |

For a single-tool answer that spans iOS and Android with the least setup: **`mobile-mcp` (`@mobilenext/mobile-mcp`)**. It supports iOS Simulator, Android Emulator, iOS Real Device, and Android Real Device with a single MCP configuration. It uses native accessibility trees as primary, screenshot fallback as secondary.

> **⚠️ CMP iOS caveat:** mobile-mcp's Compose Multiplatform iOS compatibility is inferred from its accessibility-tree approach, not officially documented as of March 2026. Verify before committing to this path for CMP iOS. [Single source — verify independently]

**For semantic precision on shared code:** Compose UI Test via Gradle CLI is the highest-fidelity option: `./gradlew iosSimulatorArm64Test` (requires a booted Simulator: `xcrun simctl boot "iPhone 16"` or `xcrun simctl boot <UDID>`), `./gradlew connectedAndroidTest` (requires a running emulator or connected device), `./gradlew jvmTest` (Desktop — no device needed; substitute `:composeApp:` or your module name). It operates directly on the Compose semantics tree without requiring `testTagsAsResourceId`. The limitation: it produces batch test reports rather than a live MCP tool stream, making it better for scripted regression testing than exploratory agent sessions.

**Computer Use API as universal fallback:** Launched for macOS on March 23, 2026 (research preview). [Single source — verify independently] API version `computer-use-2025-11-24` for Claude 4.6 models as of March 2026. Works for any macOS app without special setup — iOS Simulator, Android Emulator, Desktop all visible to Computer Use. Limitations: requires a live macOS display (not headless CI), pixel-coordinate only (no semantic element awareness), multiple seconds per action cycle.

[Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool, accessed 2026-03-30] [Gemini R1 Q5]

---

## Tool Landscape

| Tool | Platforms | Semantic / Visual | Headless | Maturity | Setup Complexity |
|---|---|---|---|---|---|
| `xcrun simctl` | iOS | Visual (screenshot only) | Yes | Stable (ships with Xcode) | Minimal |
| `idb-companion` (Homebrew) | iOS | Semantic (JSON tree) | Yes | Active (companion); Python client broken | Medium (companion only — skip Python CLI) |
| `joshuayoes/ios-simulator-mcp` v1.5.2 | iOS | Semantic + visual | Yes | Active | Low (npx) |
| `whitesmith/ios-simulator-mcp` | iOS | Semantic + visual | Yes | Active (fork) | Low (npx) |
| `InditexTech/mcp-server-simulator-ios-idb` v1.0.1 | iOS | Semantic + visual | Yes | Active (April 2025) | Medium |
| `callstackincubator/agent-device` | iOS + Android | Semantic (OS accessibility) | Yes | Active | Medium |
| `riwsky/iosef` | iOS | Semantic (XCTest) | Yes | Active (98 commits) | Medium |
| Appium 3.2.2 + XCUITest | iOS | Semantic (XCTest XML) | Yes | Active | High |
| `adb` + `uiautomator dump` | Android | Partial semantic (requires `testTagsAsResourceId`) | Yes | Stable | Low |
| `mobile-next/mobile-mcp` | iOS + Android | Semantic + visual fallback | Yes | Active (version unconfirmed — pin via lock file) | Low (npx) |
| `CursorTouch/Android-MCP` | Android | Semantic (Accessibility API) | Yes | Active | Low |
| Maestro 2.3.0 | Android + iOS (friction) | Semantic (`maestro hierarchy`) | Yes | Active | Low |
| Compose UI Test (Gradle) | All platforms | Full Compose semantics | Yes | Stable (official) | Low |
| IntelliJ MCP Server (2025.2+) | Desktop (requires IDE) | Build / code analysis | No (IDE required) | Stable (official) | Low (auto-config) |
| Junie CLI | Any (code agent) | Code generation | Yes | Beta (March 2026) | Medium |
| Playwright + `@playwright/mcp` | Web | Accessibility overlay | Yes | Stable | Low |
| Computer Use API (`computer-use-2025-11-24`) | All (macOS display) | Visual only | No | Research preview (March 2026) | Low |
| Apple Claude Agent SDK (Xcode 26.3) | iOS (Previews only) | Visual (Xcode Previews) | Yes (CLI flag — see announcement) | Not yet widely available | Requires Xcode 26.3 |

_Note: agent-device iOS CMP compatibility is inferred from its OS accessibility layer approach [Gemini R1 Q6]; Android CMP compatibility is unverified._

_Note: Maestro has experimental Web support but CMP for Web compatibility was not evaluated in this research._

_Note: Appium supports Android as well; this evaluation focused on iOS XCTest integration for CMP._

---

## Gap Map

The following capabilities are **not solved** as of March 30, 2026:

**1. fb-idb Python client v1.1.7 is non-functional as of March 30, 2026.**
Use idb-companion via MCP wrappers instead of the raw Python CLI. See iOS Simulator Layer 2 for full detail.
[Gemini R2 Q3]

**2. idb JSON field names are unresolved.**
The exact field names in `idb ui describe-all` JSON output — particularly whether `testTag` appears as `AXLabel`, `AXIdentifier`, or another key — cannot be confirmed from available 2025/2026 documentation. Requires live testing.
[Gemini R2 Q7]

**3. Maestro 2.3.0 + CMP iOS friction.**
CMP 1.10.3 fixes the structural accessibility tree projection, but Maestro Studio crashes randomly on CMP iOS screen transitions, sometimes requires coordinate fallbacks. Issue #1549 remains open. Maestro is not reliable for semantic CMP iOS element selection today.
[Gemini R2 Q9; Source: https://github.com/mobile-dev-inc/maestro/issues/1549, accessed 2026-03-30]

**4. iOS Simulator requires macOS. No Linux path to iOS Simulator automation exists.**
Every iOS Simulator automation tool requires macOS. Apple does not provide iOS Simulator for Linux.
[Single source — verify independently; Apple does not provide an official iOS Simulator for Linux as of March 2026]

**5. Computer Use API requires live display.**
The Computer Use API is not usable in headless CI environments. It requires a live macOS display session.
[Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool, accessed 2026-03-30]

**6. Compose for Web has no Playwright documentation.**
No official or community documentation exists for Playwright + Compose for Web integration. Automation viability is inferred from the accessibility overlay documentation and Flutter Web analogies. The `testTag` → `data-testid` mapping is unconfirmed. This gap is inferred from the absence of official Compose for Web + Playwright documentation as of March 30, 2026.
[Single source — verify independently]

**7. JetBrains Central is not available.**
JetBrains Central was announced March 24, 2026, but is in EAP Q2 2026 for design partners only. It is not publicly accessible as of March 30, 2026. Any workflow depending on it cannot be built today.
[Gemini R2 Q6; Source: https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/, accessed 2026-03-30]

**8. ACP + iOS Simulator requires a JetBrains IDE open as bridge. No standalone headless path via ACP alone.**
iOS Simulator tools via ACP require a JetBrains IDE open and configured to pass custom MCP servers to the agent. While Claude Code can connect to ACP headlessly via `acp.json` [Source: https://www.jetbrains.com/help/ai-assistant/acp.html, accessed 2026-03-30], iOS tools only flow through when the IDE is present as the MCP bridge. There is no standalone headless iOS path via ACP alone.
[Gemini R2 Q8]

(See also: Key Conflict Resolutions, Conflict 3 for full resolution of this constraint.)

**9. Compose Web accessibility is "initial."**
Accessibility for scrollable containers and sliders is not yet supported on the web target. Traversal indexes are not supported. Complex nested component accessibility may be incomplete. This is a structural gap, not a tooling gap.
[Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

**10. No cross-platform interactive agent tool stream.**
Compose UI Test provides the best semantic precision but produces batch reports, not a live MCP tool stream. No tool combines: (a) live MCP interaction, (b) full Compose semantics tree access, and (c) coverage of all four CMP platforms (iOS, Android, Desktop, Web) simultaneously.
[Single source — verify independently; synthesized from evaluation of all tools in this research]

**11. Apple Claude Agent SDK (Xcode 26.3) is not yet widely available.**
Xcode 26.3 is not yet available in most environments as of March 30, 2026. The Apple Claude Agent SDK's headless Xcode Preview capture capability is a near-future option only. Monitor availability before including this in a production verification pipeline.
[Gemini R1 Q2; Source: https://www.anthropic.com/news/apple-xcode-claude-agent-sdk, accessed 2026-03-30] [Single source — verify independently]

See also: iOS platform section → "Future path: Apple Claude Agent SDK (Xcode 26.3, not yet widely available)."

**12. IntelliJ MCP Server requires a running IDE instance. It is not usable in headless CI pipelines.**
The JetBrains IntelliJ MCP Server (2025.2+) requires an active IntelliJ instance with the project open. It cannot be used in headless CI pipelines or without an open IDE. The Junie CLI (Layer 3) is the headless JetBrains alternative, but it is in Beta as of March 2026. See also: Known Desktop Gaps #1.
[Source: https://www.jetbrains.com/help/idea/mcp-server.html, accessed 2026-03-30]

---

## Key Conflict Resolutions

**Conflict 1: CMP iOS flat hierarchy — fixed or not?**
A1 and A6 reported the regression as INCOMPLETE (accurate for CMP 1.8.1 through 1.9.0 (the only 1.9.x release — the regression was introduced in 1.8.1 and fixed in 1.10.3)). Gemini Round 2 Q1 confirms the structural fix landed in CMP 1.10.3 via issue #2848. **Resolution: fixed in CMP 1.10.3; use 1.10.3+. Maestro tooling friction (#1549) is a separate, still-open issue.**

**Conflict 2: JetBrains Central availability**
A3 described JetBrains Central launch on March 24, 2026 and implied it was usable. Gemini Round 2 Q6 confirms it is NOT publicly available — EAP Q2 2026 for design partners only. **Resolution: do not plan any workflow around JetBrains Central today.**

**Conflict 3: ACP headless + iOS**
A3 implied Claude Code could access iOS via ACP alone using `acp.json`. Gemini Round 2 Q8 corrects: iOS Simulator tools require a JetBrains IDE open AND configured to pass custom MCP servers to the agent. **Resolution: iOS Simulator tools require a JetBrains IDE open AND configured to pass custom MCP servers to the agent. There is no standalone headless ACP path for iOS Simulator control.**

**Conflict 4: idb viability**
A1 assessed idb as viable with caveats (stale Python client). Gemini Round 2 Q3 reveals `fb-idb` v1.1.7 is non-functional — see iOS Simulator Layer 2 for full detail. **Resolution: do not use raw `fb-idb` Python CLI. Use idb-companion via MCP wrappers instead.**

**Conflict 5: Maestro iOS CMP support**
A2 said Maestro has good Android CMP support; A6 said iOS was partial. **Resolution: Android is solid (confirmed). iOS works structurally with CMP 1.10.3 but Maestro Studio has friction, crashes, and coordinate fallbacks still needed per Gemini R2 Q9. Use Maestro for Android; use ios-simulator-mcp for iOS.**

**Conflict 6: Appium version**
A1 cited 3.2.1 (March 8, 2026); A6 cited "3.2.1 or 3.2.2 [conflicting sources]." Gemini Round 2 Q2 confirms **Appium 3.2.2, released March 9, 2026**.

---

## Sources

All URLs referenced in this research. Entries with corresponding inline `[Source: URL]` citations in the body are directly cited; additional entries are background references from underlying research sessions.

- JetBrains GitHub Releases, CMP 1.10.3 Changelog — https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.3
- CMP Supported Platforms — https://kotlinlang.org/docs/multiplatform/supported-platforms.html
- CMP iOS Accessibility — https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html
- CMP What's New 1.9.0 — https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html
- CMP What's New 1.10.0 (blog) — https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/
- CMP 1.9.0 Release (web Beta) — https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/
- CMP 1.8.0 Release (iOS Stable) — https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/
- CMP Compose Test API — https://kotlinlang.org/docs/multiplatform/compose-test.html
- CMP Accessibility (Android/common) — https://kotlinlang.org/docs/multiplatform/compose-accessibility.html
- CMP Hot Reload GitHub — https://github.com/JetBrains/compose-hot-reload
- Appium 3 launch blog — https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/
- Appium releases — https://github.com/appium/appium/releases
- Appium XCUITest driver installation — https://appium.github.io/appium-xcuitest-driver/10.11/installation/
- Appium Discuss forum: Compose KMP iOS — https://discuss.appium.io/t/compose-kmp-ios/45724
- Maestro — https://maestro.dev/
- Maestro releases — https://github.com/mobile-dev-inc/maestro/releases
- Maestro issue #1549 (CMP iOS hierarchy) — https://github.com/mobile-dev-inc/maestro/issues/1549
- Maestro 2.0.0 blog — https://maestro.dev/blog/introducing-maestro-2-0-0
- Maestro Jetpack Compose docs — https://docs.maestro.dev/get-started/supported-platform/android/jetpack
- joshuayoes/ios-simulator-mcp — https://github.com/joshuayoes/ios-simulator-mcp
- ios-simulator-mcp npm — https://www.npmjs.com/package/ios-simulator-mcp
- CVE-2025-52573 — https://nvd.nist.gov/vuln/detail/CVE-2025-52573
- whitesmith/ios-simulator-mcp — https://github.com/whitesmith/ios-simulator-mcp
- InditexTech/mcp-server-simulator-ios-idb — https://github.com/InditexTech/mcp-server-simulator-ios-idb
- riwsky/iosef — https://github.com/riwsky/iosef
- callstackincubator/agent-device — https://github.com/callstackincubator/agent-device
- mobile-next/mobile-mcp — https://github.com/mobile-next/mobile-mcp
- CursorTouch/Android-MCP — https://github.com/CursorTouch/Android-MCP
- android Debug Bridge docs — https://developer.android.com/tools/adb
- Android Emulator command-line — https://developer.android.com/studio/run/emulator-commandline
- Android Emulator releases — https://developer.android.com/studio/releases/emulator
- Android Compose testing interoperability — https://developer.android.com/develop/ui/compose/testing/interoperability
- Android Compose accessibility/semantics — https://developer.android.com/develop/ui/compose/accessibility/semantics
- facebook/idb — https://github.com/facebook/idb
- fbidb.io commands — https://fbidb.io/docs/commands/
- fbidb.io accessibility — https://fbidb.io/docs/accessibility/
- Computer Use API docs — https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- Apple Xcode Claude Agent SDK announcement — https://www.anthropic.com/news/apple-xcode-claude-agent-sdk
- JetBrains IntelliJ MCP Server — https://www.jetbrains.com/help/idea/mcp-server.html
- JetBrains AI Assistant ACP — https://www.jetbrains.com/help/ai-assistant/acp.html
- JetBrains Central announcement — https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/
- Junie CLI beta announcement — https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/
- JetBrains Koog — https://github.com/JetBrains/koog/
- Playwright docs (browsers) — https://playwright.dev/docs/browsers
- Playwright accessibility testing — https://playwright.dev/docs/accessibility-testing
- @playwright/mcp (Microsoft) — https://www.npmjs.com/package/@playwright/mcp
- simctl recipes — https://www.iosdev.recipes/simctl/
