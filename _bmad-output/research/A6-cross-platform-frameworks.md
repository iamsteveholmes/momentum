---
research_date: 2026-03-30
agent_focus: Cross-platform UI testing frameworks for LLM agents (Compose Multiplatform)
sources_consulted:
  - https://maestro.dev/
  - https://github.com/mobile-dev-inc/maestro/releases
  - https://github.com/mobile-dev-inc/maestro/blob/main/CHANGELOG.md
  - https://deepwiki.com/mobile-dev-inc/maestro-docs/7.3-model-context-protocol-(mcp)
  - https://docs.maestro.dev/maestro-flows/workspace-management/ai-test-analysis
  - https://maestro.dev/blog/best-practices-for-cross-platform-maestro-ui-testing-for-android-and-ios
  - https://github.com/mobile-dev-inc/maestro/issues/1549
  - https://www.linkedin.com/posts/maestro-dev_maestro-mcp-is-here-the-usb-c-for-activity-7343712555686629376-T_Uc
  - https://github.com/wix/Detox/releases
  - https://wix.github.io/Detox/blog/2024/10/09/detox-copilot-is-out/
  - https://github.com/KasperskyLab/Kaspresso/releases
  - https://kasperskylab.github.io/Kaspresso/Wiki/Jetpack_Compose/
  - https://github.com/appium/appium/releases
  - https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/
  - https://discuss.appium.io/t/compose-kmp-ios/45724
  - https://kotlinlang.org/docs/multiplatform/compose-test.html
  - https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html
  - https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/
  - https://carrion.dev/en/posts/cmp-ui-testing/
  - https://kmpship.app/blog/kotlin-multiplatform-testing-guide-2025
  - https://github.com/mobile-next/mobile-mcp
  - https://github.com/mobile-next/mobile-mcp/blob/main/README.md
  - https://ieeexplore.ieee.org/document/11198676/
  - https://dl.acm.org/doi/10.1145/3715763
  - https://medium.com/bumble-tech/automating-android-jetpack-compose-using-appium-edb760fe79b9
  - https://wix.github.io/Detox/docs/20.x/guide/running-on-ci/
  - https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/
  - https://www.browserstack.com/guide/maestro-testing
  - https://testguild.com/top-model-context-protocols-mcp/
search_queries_used:
  - "Maestro mobile testing Compose Multiplatform 2025 2026"
  - "Maestro AI LLM integration mobile testing 2025"
  - "Maestro MCP model context protocol LLM testing 2025"
  - "Maestro version 2.3 2025 release notes changelog Compose iOS Android"
  - "Maestro semantic tree accessibility hierarchy element inspection 2025"
  - "Maestro iOS Compose Multiplatform support test tag semantic 2025"
  - "Maestro CLI headless mode CI 2025 commands run test emulator"
  - "Maestro 'Compose Multiplatform' OR 'KMP' iOS working 2025 accessibility hierarchy fixed"
  - "Detox Compose Multiplatform support 2025"
  - "Detox Compose support Android Jetpack Compose 2024 2025"
  - "Detox Copilot AI LLM testing 2024 2025 features"
  - "Detox 20 React Native support headless CI gray box testing 2025"
  - "Detox version 2025 headless CI semantic tree accessibility"
  - "Kaspresso AI testing Compose Multiplatform 2025 2026"
  - "Kaspresso 2025 2026 releases update version"
  - "Kaspresso KaspreskyLab 2025 update android test framework"
  - "Kaspresso AI LLM test generation 2024 2025 features"
  - "Appium 2 Compose Multiplatform iOS Android 2025 2026"
  - "Appium latest version 2025 2026 accessibility tree semantic Compose"
  - "Appium 3.0 release 2025 features W3C WebDriver accessibility"
  - "Appium UiAutomator2 Compose semantic tree 2025 element inspection"
  - "Compose UI Test multiplatform iOS CLI 2025"
  - "Compose Multiplatform UI test iOS semantic composeTestRule CLI headless 2025"
  - "cross platform UI testing framework LLM agent 2025 2026"
  - "new mobile testing framework 2025 LLM semantic tree accessibility"
  - "new mobile UI testing framework 2025 built Compose Multiplatform KMP"
  - "mobile UI testing framework MCP model context protocol 2025 semantic tree"
  - "mobile-mcp mobile next iOS Android accessibility tree Compose 2025"
last_verified: 2026-03-30
---

# A6: Cross-Platform UI Testing Frameworks for LLM Agents
## Research Date: March 30, 2026

## Executive Summary

This report evaluates five major UI testing frameworks for their suitability in LLM-agent-driven testing of Compose Multiplatform (CMP) apps on iOS and Android. The core question is: which frameworks can be driven from shell commands, expose structured semantic/accessibility trees (not just screenshots), and support Compose Multiplatform across both platforms?

**Key findings:**

1. **Maestro** (CLI 2.3.0, March 2026) is the strongest general-purpose choice for agent-driven mobile E2E testing. It has native MCP integration (launched circa Q1 2026), exposes an accessibility hierarchy via `maestro hierarchy`, and supports Jetpack Compose on Android reliably. **However, the iOS accessibility flat hierarchy fix is INCOMPLETE as of March 2026 — regressions have persisted since CMP 1.8.1 (Maestro issue #1549)**: the CMP framework does not expose a proper per-component accessibility hierarchy on iOS, causing Maestro Studio to see the entire CMP view as one element. This limits Maestro's iOS CMP utility to coordinate-based or screenshot-based interactions.

2. **Compose UI Test (JetBrains official)** is the most semantically correct framework for CMP — it operates directly on the Compose semantics tree and is runnable via Gradle CLI on iOS simulator, Android emulator, and desktop. It is the recommended approach for agent-driven semantic testing of CMP apps, but requires the agent to interpret Gradle test output (XML/HTML reports), not a live MCP tool stream.

3. **mobile-mcp** (npm `@mobilenext/mobile-mcp`) is a purpose-built MCP server for iOS/Android automation via accessibility trees. It integrates directly with Claude, Cursor, and other MCP clients as a live tool. It does not reference CMP explicitly, but because CMP on iOS now maps `testTag` to `accessibilityIdentifier` (stable since CMP 1.8.0, May 2025), mobile-mcp should work with CMP iOS apps when proper semantic tags are set (inferred from accessibility tree approach — not a confirmed vendor claim).

4. **Appium 3.x** (v3.2.1 or 3.2.2, March 8–9, 2026 [conflicting sources — verify at https://github.com/appium/appium/releases]) uses W3C WebDriver protocol and accesses the native accessibility tree. Android Compose support works via `testTagsAsResourceId`. iOS CMP support is partially functional — elements are exposed only with correct `testTag`→`accessibilityIdentifier` mapping. Known issues remain in the Appium Discuss forum.

5. **Detox** (v20.50.1, March 2026) is React Native-specific. It has no Compose Multiplatform support. Detox Copilot (launched October 2024) adds LLM-driven natural-language test steps, but the framework is not applicable to CMP apps.

6. **Kaspresso** (v1.6.0, January 2024; last confirmed activity January 2025) is Android-only and does not support iOS. It supports Jetpack Compose on Android via a `kaspresso-compose-support` module. No AI/LLM integration features were found. Minimal release activity since 2024.

**Recommended approach for Claude Code agent:** Use a layered strategy — Compose UI Test (via Gradle CLI) for semantic-precise assertions in shared code, supplemented by mobile-mcp (MCP tools) for live agent-driven interaction on iOS and Android, with Maestro YAML flows for scripted E2E journeys on Android where CMP accessibility is reliable.

---

## Framework: Maestro

**Latest version:** CLI 2.3.0 (stable, released March 10, 2026); preview builds 2.3.1-preview-1 and 2.3.1-preview-2 released March 16–19, 2026. [Source: https://github.com/mobile-dev-inc/maestro/releases, accessed 2026-03-30]

**What it is:** Open-source YAML-based E2E mobile and web testing framework. Tests written once in YAML, executed across Android and iOS. Over 10,800 GitHub stars as of March 2026. [Source: https://maestro.dev/, accessed 2026-03-30]

### Compose Multiplatform Support

**Android:** Full support. Maestro interacts with the Android accessibility/semantics tree, which Jetpack Compose populates automatically. Element discovery in Maestro Studio works reliably on CMP Android targets.

**iOS:** **Problematic.** GitHub issue #1549 ("Compose Multiplatform on iOS doesn't have the proper accessibility hierarchy") documents that CMP iOS apps expose a single monolithic accessibility node rather than per-component nodes, causing Maestro Studio to see the entire CMP view as one element. The Maestro maintainer classified this as an upstream issue in JetBrains' CMP framework. [Source: https://github.com/mobile-dev-inc/maestro/issues/1549, accessed 2026-03-30]

*Partial mitigation:* JetBrains improved CMP iOS accessibility in releases 1.8.0 (May 2025) and 1.8.2, including `testTag` → `accessibilityIdentifier` mapping. However, the iOS accessibility flat hierarchy fix is INCOMPLETE as of March 2026 — regressions have persisted since CMP 1.8.1 (Maestro issue #1549). The issue remains referenced as open/upstream.

### Headless / CI Operation

Yes. Maestro is designed for CI. `maestro test flow.yaml` runs against a connected emulator or simulator. No GUI required. Android: `--no-window` flag for headless emulator; iOS: simulator managed by `xcrun simctl`. [Source: https://docs.maestro.dev/getting-started/running-flows-on-ci, accessed 2026-03-30]

### Semantic Tree / Accessibility Exposure

Maestro exposes the accessibility tree via:
- `maestro hierarchy` CLI command — dumps a structured text/XML tree of all visible elements with properties: `text`, `accessibilityText`, `hintText`, `resource-id`, `clickable`, `bounds`, `enabled`, `focused`, `checked`, `selected`
- `maestro hierarchy > hierarchy.txt` — saves for programmatic consumption [Source: https://maestro.dev/blog/how-maestro-is-reinventing-mobile-test-automation, accessed 2026-03-30]

This output is LLM-consumable: an agent can invoke `maestro hierarchy`, parse the structured output, and make element selection decisions before writing YAML flow steps.

### LLM / AI Integration Features

**1. MCP Server (Maestro MCP) — launched Q1 2026:**
Maestro ships an MCP server (`maestro mcp`) that exposes its testing capabilities as MCP tools directly callable by LLMs. Announced on LinkedIn by Maestro as "the USB-C for AI." [Source: https://www.linkedin.com/posts/maestro-dev_maestro-mcp-is-here-the-usb-c-for-activity-7343712555686629376-T_Uc, accessed 2026-03-30]

Capabilities exposed via MCP:
- Run Maestro flows
- Auto-heal failing tests
- Suggest missing coverage
- Translate natural language to flow steps

Supported MCP clients: Claude Desktop, Cursor, Windsurf, VSCode, JetBrains IDEs. [Source: https://deepwiki.com/mobile-dev-inc/maestro-docs/7.3-model-context-protocol-(mcp), accessed 2026-03-30]

**2. AI-powered assertions in YAML flows:**
- `assertWithAI`: validates complex UI states using natural language descriptions
- `assertNoDefectsWithAI`: visual audit of the current screen for common defects
- `--analyze` flag: post-run analysis generating HTML insights report (UI regressions, spelling errors, layout issues)
Requires a Maestro Cloud account (free tier available). As of late 2025, AI commands are routed through Maestro Cloud's managed model. [Source: https://docs.maestro.dev/maestro-flows/workspace-management/ai-test-analysis, accessed 2026-03-30]

**3. MaestroGPT:** An AI assistant trained specifically on Maestro, capable of generating YAML flow commands. Available via the Maestro website.

**Can an LLM agent write Maestro YAML and execute via CLI?** Yes, fully. Agent writes `.yaml` flow files, runs `maestro test flow.yaml`, parses stdout. With MCP, the agent can invoke tools directly without writing intermediate files.

| Criterion | Assessment |
|---|---|
| (a) Status as of March 2026 | Active, v2.3.0 (released March 10, 2026) |
| (b) Headless/no GUI | Yes, `maestro test` via CLI; no GUI required |
| (c) Semantic tree vs. screenshot | Yes, `maestro hierarchy` dumps structured accessibility tree; `assertWithAI` for visual assertions |
| (d) Setup complexity | Low |

**Confidence:** High (Android); Medium (iOS CMP, due to upstream accessibility hierarchy limitation)

---

## Framework: Detox

**Latest version:** 20.50.1 (released March 23, 2026). [Source: https://github.com/wix/Detox/releases, accessed 2026-03-30]

**What it is:** Gray-box E2E testing framework by Wix. Originally designed for React Native. "Gray-box" means it synchronizes with the app's internal event loop (animations, timers, network), eliminating most test flakiness.

### Compose Multiplatform Support

**None.** Detox is React Native-specific and does not support Compose Multiplatform. On Android, Detox integrates with the React Native bridge. On iOS, it wraps XCUITest. There is no integration with Kotlin, Jetpack Compose, or CMP.

**Android Jetpack Compose:** Detox uses `testID` / `accessibilityLabel` props via React Native's accessibility layer, not Compose semantics. Not applicable to CMP apps.

### Headless / CI Operation

Yes. Detox is CI-native. Supports headless emulator/simulator operation. Android: `-no-window` emulator flag. iOS: XCUITest runner via `xcrun simctl`. [Source: https://wix.github.io/Detox/docs/20.x/guide/running-on-ci/, accessed 2026-03-30]

### Semantic Tree / Accessibility Exposure

Detox does not expose a standalone accessibility tree query. Element matching is via `by.id()`, `by.text()`, `by.type()`. Version 20.47.0 (January 2026) added semantic matching in `by.type()` functionality. No structured tree dump mechanism comparable to `maestro hierarchy`.

### LLM / AI Integration Features

**Detox Copilot** (launched October 9, 2024): LLM-powered natural language test steps. [Source: https://wix.github.io/Detox/blog/2024/10/09/detox-copilot-is-out/, accessed 2026-03-30]

- Interprets natural language instructions and generates Detox actions/assertions
- LLM-agnostic: connects to any LLM provider the team configures
- Uses combination of accessibility data and multimodal screenshot analysis for checks beyond standard element state (e.g., verifying text is bold, button visual state)
- API is still in active development; may change in future releases

**Limitation for CMP:** Copilot's underlying framework is still React Native-specific. Even if the LLM integration is sophisticated, it cannot target CMP apps.

| Criterion | Assessment |
|---|---|
| (a) Status as of March 2026 | Active, v20.50.1 |
| (b) Headless/no GUI | Yes, via CI (Android `-no-window`, iOS via `xcrun simctl`) |
| (c) Semantic tree vs. screenshot | No — no structured tree dump; React Native-only element matching |
| (d) Setup complexity | High (React Native only; not applicable to CMP) |

**Confidence:** High (React Native apps); Not applicable (Compose Multiplatform)

---

## Framework: Kaspresso

**Latest version:** 1.6.0 (released January 17, 2024). Maven artifact metadata timestamps from January 2025 reflect repository indexing activity, not a new release. Project appears stalled since January 2024. [Source: https://github.com/KasperskyLab/Kaspresso/releases, accessed 2026-03-30]

**What it is:** Android UI test framework by Kaspersky Lab, built on Espresso and UiAutomator. Provides DSL wrappers, interceptors for stability, and screenshot/reporting integrations. Open-source.

### Compose Multiplatform Support

**Android only — no iOS.** Kaspresso is Android-instrumented-test only. It runs on device/emulator via Android's instrumentation framework. There is no iOS support and no plans for cross-platform operation.

**Jetpack Compose on Android:** The `kaspresso-compose-support` module (available on Maven Central) allows writing Kaspresso tests for Jetpack Compose screens using the same DSL as View tests. [Source: https://kasperskylab.github.io/Kaspresso/Wiki/Jetpack_Compose/, accessed 2026-03-30]

**Compose Multiplatform Android target:** CMP apps running on Android should work with Kaspresso's compose support module, since the Android target of CMP uses standard Jetpack Compose semantics. However, no specific CMP documentation or test examples were found.

### Headless / CI Operation

Yes, via standard Android emulator in headless mode. Tests run with `./gradlew connectedAndroidTest`. No GUI required beyond the running emulator.

### Semantic Tree / Accessibility Exposure

Kaspresso uses UiAutomator2 under the hood, which reads the Android accessibility tree. The `kaspresso-compose-support` module accesses Compose semantics nodes. No dedicated hierarchy dump command was found comparable to `maestro hierarchy`.

### LLM / AI Integration Features

None found. No AI test generation, MCP server, or LLM integration features were found in any Kaspresso release through the research date. [Source: https://github.com/KasperskyLab/Kaspresso/releases, accessed 2026-03-30]

### Development Activity

Development is stalled. No substantive releases have occurred since v1.6.0 (January 2024). This project should not be selected for new work.

| Criterion | Assessment |
|---|---|
| (a) Status as of March 2026 | Stalled — last release v1.6.0, January 2024 |
| (b) Headless/no GUI | Yes, via Gradle (`./gradlew connectedAndroidTest`) |
| (c) Semantic tree vs. screenshot | Partial — via UiAutomator2 accessibility tree; `kaspresso-compose-support` for Compose semantics |
| (d) Setup complexity | Medium |

**Confidence:** Medium (Android only; low recent activity is a risk factor)

---

## Framework: Appium 3.x

**Latest version:** Appium 3.2.1 or 3.2.2 (March 8–9, 2026) [conflicting sources — verify at https://github.com/appium/appium/releases]. Appium 3.0 was released August 7, 2025. [Source: https://github.com/appium/appium/releases, accessed 2026-03-30]

**What it is:** Cross-platform mobile automation framework using the W3C WebDriver protocol. Appium 3 is the current major version, with a plugin architecture for drivers (UiAutomator2 for Android, XCUITest for iOS).

### Appium 3 Key Changes (vs 2.x)

- Full W3C WebDriver compliance; dropped legacy JSON Wire Protocol
- Node.js 20.19+ required
- Sensitive data masking in logs
- Inspector plugin now installable directly into Appium server (`appium plugin install inspector`)
- Feature flags now require driver prefix (e.g., `uiautomator2:adb_shell`)
[Source: https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/, accessed 2026-03-30]

### Compose Multiplatform Support

**Android:** Works with configuration. CMP Android apps use Compose semantics nodes (not View objects). UiAutomator2 can access the Compose semantics tree via accessibility services. The required configuration:
- Set `testTagsAsResourceId = true` in the Compose semantic tree — this makes `testTag` values available as `viewIdResourceName` in the accessibility tree, accessible to UiAutomator2/Appium via resource-id
- Without this flag, Compose elements may not be findable by ID
[Source: https://medium.com/bumble-tech/automating-android-jetpack-compose-using-appium-edb760fe79b9, accessed 2026-03-30]

**iOS:** **Partially working with caveats.** CMP iOS apps expose semantic data through the iOS accessibility tree when `testTag` is used (maps to `accessibilityIdentifier`). However, the Appium Discuss forum documents ongoing issues: elements set with `Modifier.semantics { contentDescription = "..." }` appear with no description in the accessibility tree, while `testTag` works more reliably. The recommendation from JetBrains documentation is to use `testTag` (not `contentDescription`) for testing on iOS. [Source: https://discuss.appium.io/t/compose-kmp-ios/45724, accessed 2026-03-30]

### Headless / CI Operation

Yes. Appium runs against Android emulators (headless with `-no-window`) and iOS simulators. `appium` server starts as a daemon; tests connect via WebDriver client. Fully CLI-operable.

### Semantic Tree / Accessibility Exposure

Appium exposes the full accessibility tree via the W3C WebDriver `getPageSource()` call, which returns an XML document of the accessibility tree. On Android+UiAutomator2, this includes Compose semantics nodes. On iOS+XCUITest, it includes XCUIElement hierarchy.

This XML output is directly consumable by an LLM agent — the agent can request the page source, parse the accessibility tree, identify target elements, and generate interaction commands.

### LLM / AI Integration Features

No native LLM/MCP integration in Appium itself. However, Appium's W3C WebDriver protocol makes it a natural backend for LLM agents: the agent scripts WebDriver calls programmatically. Third-party tools (e.g., mobile-mcp, AI test cloud platforms) wrap Appium for LLM-friendlier interfaces.

| Criterion | Assessment |
|---|---|
| (a) Status as of March 2026 | Active, v3.2.1 (March 8, 2026) [conflicting source: 3.2.2 also reported — verify at https://github.com/appium/appium/releases] |
| (b) Headless/no GUI | Yes, via WDA server; fully CLI-operable |
| (c) Semantic tree vs. screenshot | Yes — via UIAutomator2 (Android) and XCUITest (iOS); `getPageSource()` returns full accessibility tree XML |
| (d) Setup complexity | High (driver configuration complexity; `testTagsAsResourceId` required for CMP Android) |

**Confidence:** Medium (works on both platforms with correct semantic configuration; iOS CMP caveats remain)

---

## Framework: Compose UI Test (Official JetBrains)

**Latest version:** Ships with Compose Multiplatform. CMP 1.10.3 is the current stable release as of the research date (March 30, 2026). CMP 1.10.0 introduced Navigation 3 and bundled Compose Hot Reload; 1.10.3 is the latest patch. [Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html documents the 1.9.0 feature set; for 1.10.x release details verify at https://github.com/JetBrains/compose-multiplatform/releases, accessed 2026-03-30]

**What it is:** The official UI testing module for Compose Multiplatform, using the same API as Jetpack Compose testing (`ComposeTestRule`-style, using `runComposeUiTest` for multiplatform). Tests are written in `commonTest` using `compose.uiTest` and run on all targets. [Source: https://kotlinlang.org/docs/multiplatform/compose-test.html, accessed 2026-03-30]

**Status:** Experimental API (may change). iOS support is functional as of CMP 1.6.0 (February 2024) and improved with CMP 1.8.0 (May 2025).

### Compose Multiplatform Support

**Android:** Full support. Same as standard Jetpack Compose testing — complete semantic tree access.

**iOS:** Functional via `iosSimulatorArm64Test` Gradle target. CMP semantics map to the iOS accessibility tree. `testTag` maps to `accessibilityIdentifier`. `AccessibilitySyncOptions.Always` can be configured to ensure the accessibility tree is always synchronized (needed for testing without VoiceOver active). [Source: https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html, accessed 2026-03-30]

⚠️ **Note:** iOS accessibility hierarchy regressions persist since CMP 1.8.1 (flat parent-child structure issue). Compose UI Test on iOS may not see all elements in deeply nested CMP layouts — see Maestro issue #1549 for related upstream context.

**Desktop (JVM):** Full support via `jvmTest`. Desktop uses the JUnit-based `ComposeTestRule` API, not the `runComposeUiTest` function used for mobile/multiplatform targets. `ComposeTestRule` integrates with standard JUnit4 test runners and enables familiar test patterns on JVM.

**Web (WASM/JS):** In Beta as of CMP 1.9.0 (September 2025). [Source: https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/, accessed 2026-03-30]

### CLI Execution

Fully CLI-driven via Gradle:

| Platform | Command |
|---|---|
| iOS Simulator (arm64) | `./gradlew :composeApp:iosSimulatorArm64Test` |
| Android | `./gradlew :composeApp:connectedAndroidTest` |
| Desktop (JVM) | `./gradlew :composeApp:jvmTest` |
| Web (WASM) | `./gradlew :composeApp:wasmJsTest` |
| All tests | `./gradlew allTests` |

[Source: https://carrion.dev/en/posts/cmp-ui-testing/, accessed 2026-03-30]

### Semantic Tree Access

The Compose UI Test API operates directly on the Compose semantics tree — the most precise semantic access available. Key APIs:
- `onNodeWithTag("myTag")` — find by `testTag`
- `onNodeWithText("Submit")` — find by visible text
- `onNodeWithContentDescription("Icon")` — find by accessibility label
- `onNode(hasText("...") and isEnabled())` — compound matchers
- `printToLog("TAG")` — dumps the full semantics tree to logcat/stdout

The semantics tree exposes: text, tag, content description, role, enabled/disabled, selected, checked, focused, clickable, bounds, merge policy.

### Can outputs be consumed by an LLM agent?

Yes, with integration work. Approach:
1. Agent triggers `./gradlew :composeApp:connectedAndroidTest` or iOS equivalent
2. Results written to `build/reports/tests/` (HTML) and `build/test-results/` (JUnit XML)
3. Agent reads JUnit XML or HTML report to interpret pass/fail and assertions
4. For live element inspection (not test execution), `printToLog` output can be captured from ADB logcat

Limitation: Compose UI Test does not expose a live MCP tool stream. The agent cannot dynamically query the semantics tree mid-test without modifying the test source. This is best for scripted test execution, not exploratory/interactive agent testing.

| Criterion | Assessment |
|---|---|
| (a) Status as of March 2026 | Active, stable with CMP 1.10.3 |
| (b) Headless/no GUI | Yes, via Gradle CLI (`./gradlew iosSimulatorArm64Test`, `connectedAndroidTest`, etc.) |
| (c) Semantic tree vs. screenshot | Yes — Android reliable (direct Compose semantics tree); iOS experimental (regression risk since CMP 1.8.1) |
| (d) Setup complexity | Low (built into CMP; no additional framework installation required) |

**Confidence:** High (canonical CMP testing approach; best semantic precision; CLI-driven)

---

## New Frameworks (2025–2026)

### mobile-mcp (mobile-next)

**What it is:** An MCP server (`@mobilenext/mobile-mcp`) that enables AI agents and LLMs to interact with native iOS/Android apps via accessibility tree snapshots or coordinate-based screenshot taps. [Source: https://github.com/mobile-next/mobile-mcp, accessed 2026-03-30]

**Release:** Available on npm as `@mobilenext/mobile-mcp@latest`. Exact initial release date not found in documentation. Actively developed (299+ commits on main branch as of research date). Note: `@latest` resolves to different versions over time — verify the specific version at time of use with `npm view @mobilenext/mobile-mcp version`.

**Platform support:** iOS Real Device, iOS Simulator, Android Real Device, Android Emulator. All confirmed supported.

**Accessibility tree approach:** Uses native accessibility trees as the primary interaction mechanism. Falls back to screenshot-based coordinate taps when accessibility labels are unavailable. No computer vision model required for accessibility-based interactions — "LLM-friendly."

**MCP tools exposed (15+):**
- `mobile_list_elements_on_screen` — returns accessibility tree snapshot
- `mobile_click_on_screen_at_coordinates` — coordinate tap
- `mobile_take_screenshot` — screenshot capture
- `mobile_launch_app`, `mobile_terminate_app`, `mobile_install_app`
- `mobile_type_keys`, `mobile_press_button`, `mobile_open_url`
- `mobile_swipe_on_screen`, `mobile_long_press_on_screen_at_coordinates`
- `mobile_list_available_devices`, `mobile_get_screen_size`, `mobile_get_orientation`

**LLM integration:** Connects directly to Claude, Cursor, Windsurf, OpenAI ChatGPT, GitHub Copilot, Google AI Studio/Gemini via standard MCP protocol. Claude Code can invoke mobile-mcp tools natively once configured as an MCP server.

**Compose Multiplatform compatibility:** Not documented explicitly. Since CMP iOS now maps `testTag` → `accessibilityIdentifier` (stable since CMP 1.8.0), `mobile_list_elements_on_screen` should expose CMP elements on iOS when proper tags are set. Android CMP elements are accessible via UiAutomator-style accessibility tree. This is an inference, not a confirmed vendor claim.

| Criterion | Assessment |
|---|---|
| (a) Status as of March 2026 | Active (299+ commits; `@latest` version on npm — verify version at time of use) |
| (b) Headless/no GUI | Yes (iOS Simulator and Android Emulator both supported) |
| (c) Semantic tree vs. screenshot | Yes — OS accessibility layer via `mobile_list_elements_on_screen`; screenshot fallback available |
| (d) Setup complexity | Low (`npm install` + Claude Code MCP config) |

**Confidence:** Medium (strong MCP integration for agent use; CMP compatibility inferred from accessibility tree approach, not explicitly documented)

### LLMDroid (Academic / Research)

An academic framework (ACM 2025) that enhances automated mobile GUI testing with LLM guidance. Not a production-ready tool. Uses two-phase approach: autonomous exploration + LLM-guided coverage extension. Not directly applicable to CMP. [Source: https://dl.acm.org/doi/10.1145/3715763, accessed 2026-03-30]

### IEEE LLM Cross-Platform Framework (Research, 2025)

A research framework (IEEE 2025) using LLMs + computer vision for cross-platform UI testing, achieving 70% precision and 78% accuracy. Constructs cross-platform UI representations via semantic abstraction. Academic research, not a released tool. [Source: https://ieeexplore.ieee.org/document/11198676/, accessed 2026-03-30]

**Confidence:** Low (academic research, not production tools)

---

## Comparison Matrix

| Framework | CMP Android | CMP iOS | Headless CI | Semantic Tree | LLM Integration | CLI-driven |
|---|---|---|---|---|---|---|
| **Maestro** | Yes (full) | Partial ⚠️ | Yes | Via `maestro hierarchy` (accessibility tree dump) | MCP server + assertWithAI + Maestro Cloud AI | Yes (`maestro test`) |
| **Detox** | No | No | Yes | No (React Native-only) | Detox Copilot (RN only) | Yes |
| **Kaspresso** | Yes (with kaspresso-compose-support) [Android-only] | No | Yes (Android emulator) | Via UiAutomator2 accessibility | None found | Yes (Gradle) |
| **Appium 3.x** | Yes (with `testTagsAsResourceId`) | Partial ⚠️ | Yes | Via W3C `getPageSource()` XML | None native (3rd-party wrappers exist) | Yes (`appium` server + client) |
| **Compose UI Test** | Yes (full, canonical) | Yes (API experimental) | Yes | Direct semantics tree (onNodeWith* APIs) | None native | Yes (Gradle) |
| **mobile-mcp** | Inferred yes | Inferred yes | Yes (simulator/emulator) | Via accessibility tree snapshot MCP tool | Native MCP (Claude, Cursor, etc.) | Via MCP protocol |

**Legend for CMP iOS "Partial ⚠️":**
- Maestro: Upstream accessibility hierarchy issue means individual CMP components may not be distinguishable on iOS
- Appium 3.x: Works when `testTag` is consistently used; `contentDescription` does not reliably map on iOS

---

## Recommended Approach for Claude Code Agent

For an LLM agent in Claude Code testing Compose Multiplatform apps, a three-layer strategy is recommended:

### Layer 1: Compose UI Test (Semantic Precision Layer)

Use JetBrains' official `compose.uiTest` framework for assertions requiring semantic precision:
- Written in `commonTest` — one test suite runs on Android, iOS, and Desktop
- Triggered via `./gradlew :composeApp:connectedAndroidTest` (Android) or `./gradlew :composeApp:iosSimulatorArm64Test` (iOS)
- Results in JUnit XML at `build/test-results/` — parseable by agent
- Best for: regression tests, accessibility audits, behavioral assertions on stable features

**Agent workflow:**
1. Agent generates/modifies test files in `commonTest`
2. Agent triggers Gradle command
3. Agent reads JUnit XML report
4. Agent interprets failures and makes code or test adjustments

### Layer 2: mobile-mcp (Live Exploratory Layer)

Use mobile-mcp as an MCP server for live, interactive exploration of the running app:
- Configure as MCP server in Claude Code settings
- Use `mobile_list_elements_on_screen` to inspect the accessibility tree
- Use `mobile_click_on_screen_at_coordinates` or element-based tapping for interactions
- Use `mobile_take_screenshot` for visual verification

**Agent workflow:**
1. App running on simulator/emulator (launched via Gradle or Xcode)
2. Agent calls `mobile_list_elements_on_screen` to see current state
3. Agent identifies target elements from accessibility snapshot
4. Agent calls interaction tools, then re-inspects screen
5. Agent verifies outcomes and records observations

**Configuration (add to Claude Code MCP settings):**
```json
{
  "mcpServers": {
    "mobile-mcp": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@latest"]
    }
  }
}
```

**Prerequisite:** See Configuration Requirements below for the required `testTag` and `AccessibilitySyncOptions` setup for both platforms.

### Layer 3: Maestro YAML Flows (E2E Journey Layer)

Use Maestro for scripted E2E user journeys, primarily on Android where CMP accessibility is reliable:
- Agent writes YAML flow files
- `maestro hierarchy > hierarchy.txt` for element discovery
- `maestro test flow.yaml` for execution
- `assertWithAI` for complex visual assertions (requires Maestro Cloud account)
- Maestro MCP for direct agent integration without intermediate YAML files

**iOS CMP note:** Use Maestro on iOS only with caution. Until the upstream CMP iOS accessibility hierarchy issue is confirmed resolved, element selectors may fail. Coordinate-based taps and screenshot assertions are fallback options.

### Configuration Requirements for CMP App

For any external testing framework to work reliably with CMP:

```kotlin
// Android: Enable testTag → resourceId mapping
Modifier.semantics { testTagsAsResourceId = true }

// iOS: Enable always-on accessibility sync for testing
ComposeUIViewController(configure = {
    accessibilitySyncOptions = AccessibilitySyncOptions.Always(debugLogger = null)
}) { /* content */ }

// All platforms: Use testTag on interactive elements
Modifier.testTag("submit_button")
```

---

## Gaps and Limitations

1. **CMP iOS accessibility is not fully mature for external testing tools.** The iOS accessibility flat hierarchy fix is INCOMPLETE as of March 2026 — regressions have persisted since CMP 1.8.1 (Maestro issue #1549). External framework compatibility (Maestro, Appium) requires continued upstream improvement from JetBrains. This remains a known risk.

2. **No single framework provides live MCP tool access + full CMP semantic tree.** Compose UI Test has the best semantics but no live MCP stream. mobile-mcp has live MCP but relies on accessibility tree (not Compose semantics directly). A combined approach is necessary.

3. **Kaspresso is effectively stalled for new projects.** Last major release was January 2024, no AI features, Android-only. Not recommended for new CMP projects.

4. **Detox has no CMP path.** It is explicitly React Native-focused. No workaround exists.

5. **Appium 3.x requires `testTagsAsResourceId` configuration** on Android to reliably find Compose elements. Default CMP apps may need test-build-specific configuration changes, which complicates agent-driven testing without source code access.

6. **Maestro MCP is new (Q1 2026)** and limited production evidence exists for Claude Code integration specifically. The MCP spec integration is confirmed, but Claude Code CLI (not Claude Desktop) MCP configuration may require additional setup.

7. **Desktop (JVM) is the easiest target** for CMP UI testing. Desktop uses JUnit-based `ComposeTestRule` (not the experimental `runComposeUiTest` function), enabling familiar test patterns. If agent testing can be scoped to desktop for development feedback loops, complexity is significantly reduced.

8. **Web (WASM) CMP testing** is in Beta as of September 2025. Playwright/standard browser testing tools may be more appropriate for the web target than mobile frameworks.

---

## Sources

All sources accessed 2026-03-30 unless otherwise noted.

- [Maestro — End-to-End UI Testing for Mobile and Web](https://maestro.dev/)
- [Maestro GitHub Releases](https://github.com/mobile-dev-inc/maestro/releases)
- [Maestro CHANGELOG.md](https://github.com/mobile-dev-inc/maestro/blob/main/CHANGELOG.md)
- [Maestro MCP Deep Wiki](https://deepwiki.com/mobile-dev-inc/maestro-docs/7.3-model-context-protocol-(mcp))
- [Maestro AI Test Analysis Docs](https://docs.maestro.dev/maestro-flows/workspace-management/ai-test-analysis)
- [Maestro Cross-Platform Best Practices Blog](https://maestro.dev/blog/best-practices-for-cross-platform-maestro-ui-testing-for-android-and-ios)
- [Maestro GitHub Issue #1549 — CMP iOS Accessibility Hierarchy](https://github.com/mobile-dev-inc/maestro/issues/1549)
- [Maestro MCP LinkedIn Announcement](https://www.linkedin.com/posts/maestro-dev_maestro-mcp-is-here-the-usb-c-for-activity-7343712555686629376-T_Uc)
- [Detox GitHub Releases](https://github.com/wix/Detox/releases)
- [Detox Copilot Launch Blog Post](https://wix.github.io/Detox/blog/2024/10/09/detox-copilot-is-out/)
- [Detox Running on CI Docs](https://wix.github.io/Detox/docs/20.x/guide/running-on-ci/)
- [Kaspresso GitHub Releases](https://github.com/KasperskyLab/Kaspresso/releases)
- [Kaspresso Jetpack Compose Support Docs](https://kasperskylab.github.io/Kaspresso/Wiki/Jetpack_Compose/)
- [Appium GitHub Releases](https://github.com/appium/appium/releases)
- [Appium 3 Release Blog Post (August 7, 2025)](https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/)
- [Appium Discuss — Compose KMP iOS Issue](https://discuss.appium.io/t/compose-kmp-ios/45724)
- [Automating Android Jetpack Compose using Appium — Bumble Tech](https://medium.com/bumble-tech/automating-android-jetpack-compose-using-appium-edb760fe79b9)
- [Compose Multiplatform Testing Docs (JetBrains)](https://kotlinlang.org/docs/multiplatform/compose-test.html)
- [Compose Multiplatform iOS Accessibility Docs](https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html)
- [CMP 1.8.0 Stable Release Blog (May 2025)](https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/)
- [CMP 1.9.0 — Web Goes Beta (September 2025)](https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/)
- [Testing CMP from Common Code — Carrion.dev](https://carrion.dev/en/posts/cmp-ui-testing/)
- [KMP Testing Guide 2025 — kmpship.app](https://kmpship.app/blog/kotlin-multiplatform-testing-guide-2025)
- [mobile-mcp GitHub Repository](https://github.com/mobile-next/mobile-mcp)
- [mobile-mcp README](https://github.com/mobile-next/mobile-mcp/blob/main/README.md)
- [LLM-Powered Automated Testing for Multi-Scenario Mobile Apps — IEEE 2025](https://ieeexplore.ieee.org/document/11198676/)
- [LLMDroid: Enhancing Automated Mobile App GUI Testing — ACM 2025](https://dl.acm.org/doi/10.1145/3715763)
- [BrowserStack: What is Maestro Testing](https://www.browserstack.com/guide/maestro-testing)
- [Top MCP Servers for Test Automation — TestGuild](https://testguild.com/top-model-context-protocols-mcp/)
