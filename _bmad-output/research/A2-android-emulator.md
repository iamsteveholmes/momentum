---
research_date: 2026-03-30
agent_focus: Android Emulator automation for LLM agents
sources_consulted:
  - https://developer.android.com/tools/adb
  - https://developer.android.com/studio/run/emulator-commandline
  - https://developer.android.com/studio/releases/emulator
  - https://developer.android.com/develop/ui/compose/testing/interoperability
  - https://developer.android.com/develop/ui/compose/accessibility/semantics
  - https://github.com/CursorTouch/Android-MCP
  - https://github.com/AlexGladkov/claude-in-mobile
  - https://github.com/minhalvp/android-mcp-server
  - https://github.com/watabee/mcp-server-adb
  - https://github.com/mobile-next/mobile-mcp
  - https://github.com/openatx/uiautomator2
  - https://github.com/mobile-dev-inc/maestro
  - https://github.com/mobile-dev-inc/maestro/releases
  - https://maestro.dev/
  - https://docs.maestro.dev/maestro-cli/maestro-cli-commands-and-options
  - https://docs.maestro.dev/get-started/supported-platform/android/jetpack
  - https://maestro.dev/blog/introducing-maestro-2-0-0
  - https://pypi.org/project/uiautomator2/
  - https://malinskiy.github.io/adam/docs/emu
  - https://gist.github.com/mrk-han/fa5c6e8951919b7efc1ba99fcd10496e
  - https://kotlinlang.org/docs/multiplatform/compose-accessibility.html
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-180.html
  - https://lobehub.com/mcp/benoberkfell-android-a11y-mcp
  - https://github.com/flutter/flutter/issues/74197
  - https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/
  - https://kotlinlang.org/docs/multiplatform/compose-test.html
  - https://medium.com/androiddevelopers/accessing-composables-from-uiautomator-cf316515edc2
  - https://www.repeato.app/extracting-layout-and-view-information-via-adb/
  - https://www.blog.brightcoding.dev/2025/08/24/control-android-devices-with-ai-using-adb-and-natural-language/
  - https://dev.to/tiagodanin/creating-an-ai-agent-in-claude-code-to-control-my-smartphone-1e3e
  - https://developer.android.com/studio/test/managed-devices
  - https://composeproof.dev/
  - https://android-developers.googleblog.com/2025/11/gemini-3-is-now-available-for-ai.html
  - https://developer.android.com/studio/gemini/overview
search_queries_used:
  - "adb Android Debug Bridge screenshot input automation LLM agent 2025 2026"
  - "UIAutomator2 Python Compose Multiplatform 2025 2026"
  - "Maestro mobile testing Compose Multiplatform 2025 2026"
  - "Android emulator gRPC API automation 2025 2026"
  - "MCP server Android adb Claude LLM 2025 2026"
  - "Compose UI Test headless emulator CLI gradlew connectedAndroidTest 2025"
  - "adb uiautomator dump Compose semantic tree accessibility 2025"
  - "Android Studio Gemini AI API programmatic access outside IDE 2025 2026"
  - "Compose Multiplatform Android accessibility semantic tree UIAutomator accessibility node"
  - "Maestro headless mode CLI YAML flow LLM agent generate run 2025"
  - "android emulator headless mode -no-window command line macOS 2025"
  - "Compose Multiplatform uiautomator dump accessibility tree resource-id testTag 2025"
  - "watabee mcp-server-adb GitHub Android adb MCP server 2025 2026"
  - "android-mcp-server OR android MCP Compose Multiplatform screenshot accessibility 2025 2026"
  - "Espresso Compose UI test run without Android Studio headless emulator CI 2025"
  - "Maestro mobile testing 2025 latest version Android Compose support changelog features"
  - "Android emulator start headless macOS avdmanager sdkmanager command line 2025"
  - "Compose Multiplatform 1.8 release date 2025 accessibility testing Android"
  - "Compose Multiplatform 1.9 release 2025 Android testing accessibility semantic tree"
  - "Maestro version 2.3.0 release notes March 2026 changelog"
  - "Compose Multiplatform vs Jetpack Compose uiautomator dump differences accessibility tree 2024 2025"
  - "gradle managed devices android test headless 2025 API level"
last_verified: 2026-03-30
---

# A2: Android Emulator Automation for LLM Agents
## Research Date: March 30, 2026

---

## Executive Summary

An LLM agent running inside Claude Code CLI on macOS can fully automate a Compose Multiplatform Android app in the Android Emulator using a layered tool chain — no Android Studio GUI required. As of March 2026, the options range from raw `adb` shell commands (zero dependencies, screenshot + coordinate-based input) through UIAutomator2 Python wrapper (programmatic UI element inspection), Maestro YAML flows (high-level E2E test runner with black-box Compose support), and a rich ecosystem of MCP servers that expose all of this through the Model Context Protocol.

The single most important insight for Compose Multiplatform (CMP) on Android: the app's semantic/accessibility tree **is** available via `adb shell uiautomator dump` and UIAutomator, but Compose elements only surface as named, findable nodes in that dump if the app sets `testTagsAsResourceId = true` and applies `Modifier.testTag(...)`. Without this, the dump contains only top-level container nodes for the Compose surface, with no individual UI element breakdown. This is identical behavior for CMP and native Jetpack Compose on Android; CMP uses the same underlying Compose runtime.

**Recommended base layer for a shell-based LLM agent:** `adb` for emulator lifecycle, screenshots, and raw input; UIAutomator dump (via `adb shell uiautomator dump`) for structural inspection when testTags are set; and an MCP server to wrap all of this in Claude Code's native tool protocol. **Primary MCP recommendation: `mobile-mcp`** (explicit Android emulator support on macOS, structured accessibility + screenshot fallback, active maintenance). **Alternative: `CursorTouch/Android-MCP`** (lightweight, Accessibility API-based, no CV pipeline).

---

## Tool: adb (Android Debug Bridge)

### Overview

`adb` is the canonical command-line interface to Android devices and emulators, part of Android Platform Tools. It requires no Android Studio installation — only the Platform Tools package, available via `sdkmanager` or as a standalone download. As of March 2026, the latest stable Android Emulator is **36.4.9** (released February 10, 2026) [Source: https://developer.android.com/studio/releases/emulator, accessed 2026-03-30].

### Emulator Lifecycle (Headless, No Android Studio)

```bash
# List available AVDs
~/Library/Android/sdk/emulator/emulator -list-avds

# Launch emulator headlessly (no window, no audio, fast boot)
~/Library/Android/sdk/emulator/emulator @Pixel8_API_35 -no-window -no-audio -no-boot-anim

# Wait for device to finish booting
adb wait-for-device
adb shell getprop sys.boot_completed  # returns "1" when ready

# Kill emulator
adb emu kill
```

For CI or scripted workflows, the `emulator-headless` binary (introduced in emulator 28.0.25 — version per community documentation; verify against emulator release notes at https://developer.android.com/studio/releases/emulator) is the documented supported replacement for `-no-window`. In practice, all code examples in this document use `-no-window` as it is widely compatible and simpler for macOS shell agents. Either form achieves headless operation; use `emulator-headless` if deploying on Linux CI where it is the preferred form. On macOS (Apple Silicon), use `arm64-v8a` system images; on Intel Macs use `x86_64`. [Source: https://developer.android.com/studio/run/emulator-commandline, accessed 2026-03-30]

### Screenshot Capture

```bash
# Capture directly to local file (single pipeline, no temp file on device)
adb exec-out screencap -p > screen.png

# Alternate: capture to device, pull to host
adb shell screencap /sdcard/screen.png
adb pull /sdcard/screen.png
```

`adb exec-out screencap -p` is the preferred single-command form for scripted agents — it pipes raw PNG bytes directly to stdout with no intermediate file on device. [Source: https://developer.android.com/tools/adb, accessed 2026-03-30]

### Input Events

```bash
# Tap at pixel coordinates
adb shell input tap 540 960

# Swipe (x1 y1 x2 y2 duration_ms)
adb shell input swipe 300 800 300 200 500

# Type text (quote handling: double-quote wrapping for special chars)
adb shell input text "Hello"
adb shell input text "'quoted text'"

# Key events
adb shell input keyevent 4    # BACK
adb shell input keyevent 3    # HOME
adb shell input keyevent 82   # MENU

# Long press
adb shell input swipe 540 960 540 960 1000  # swipe to same coords = long press
```

[Source: https://developer.android.com/tools/adb, accessed 2026-03-30]

### UI Hierarchy Dump (UIAutomator via adb)

```bash
# Dump to device, retrieve
adb shell uiautomator dump /sdcard/hierarchy.xml
adb pull /sdcard/hierarchy.xml

# Direct to stdout (faster, no device file)
adb exec-out uiautomator dump /dev/tty
```

The resulting XML contains `<node>` elements with attributes: `resource-id`, `class`, `text`, `content-desc`, `bounds` (pixel rect), `clickable`, `scrollable`, `enabled`, `focused`, `checkable`, `checked`, `package`. For Compose elements, see the Compose Multiplatform section below for what appears (and what does not) in this dump. [Source: https://www.repeato.app/extracting-layout-and-view-information-via-adb/, accessed 2026-03-30]

### App Management

```bash
# Install APK
adb install -r path/to/app.apk

# Launch app by package/activity
adb shell am start -n com.example.app/.MainActivity

# Force stop
adb shell am force-stop com.example.app

# List installed packages
adb shell pm list packages -3   # third-party only
```

### Assessment

| Criterion | Rating |
|---|---|
| Status/maturity (March 2026) | Stable, part of Android Platform Tools; Emulator 36.4.9 stable |
| Headless operation | Yes — `-no-window` flag or `emulator-headless` binary |
| Semantic/accessibility tree | Partial — `uiautomator dump` gives XML tree; Compose elements require `testTagsAsResourceId` to be named |
| Setup complexity for shell agent | Low — install platform-tools only (`sdkmanager "platform-tools"`) |

**Confidence:** High — adb is the foundation of all Android automation; all claims sourced from official Android developer documentation.

---

## Tool: UIAutomator2 (Python Client)

### Overview

`uiautomator2` is an open-source Python library (maintained by the `openatx` organization) that wraps the Android UIAutomator framework via an HTTP RPC service running on the device. It installs an agent APK on the device that exposes UIAutomator operations over HTTP, allowing Python clients to drive the device remotely. [Source: https://github.com/openatx/uiautomator2, accessed 2026-03-30]

**Latest release:** 3.5.0 (October 30, 2025). Supports Python 3.8–3.13. [Source: https://pypi.org/project/uiautomator2/, accessed 2026-03-30]

### Key Capabilities

```python
import uiautomator2 as u2

# Connect to running emulator
d = u2.connect()  # or u2.connect("emulator-5554")

# Screenshot
d.screenshot("screen.png")
img = d.screenshot()  # PIL Image object

# Find element and interact
el = d(text="Login")
el.click()
d(resourceId="com.example.app:id/username").set_text("user@example.com")

# UI hierarchy dump (XML)
xml = d.dump_hierarchy()

# XPath-based element finding
d.xpath('//android.widget.Button[@text="Submit"]').click()
```

### Compose Multiplatform Compatibility

UIAutomator2 operates at the Android system UIAutomator layer — the same layer used by `adb shell uiautomator dump`. Therefore, CMP elements appear in the hierarchy only through the same mechanism: elements with `contentDescription`, displayed `text`, or `resource-id` (via `testTagsAsResourceId`) are findable. Elements with no semantic properties render as opaque `androidx.compose.ui.platform.ComposeView` containers with no children.

UIAutomator2 does not expose the Compose internal semantics tree directly; it uses the Android Accessibility API translation of it. The Python library itself has no Compose-specific documentation or special handling as of version 3.5.0.

### Headless Operation

Yes — UIAutomator2 operates fully headlessly against any running emulator. The device-side agent runs independently of any IDE.

### Assessment

| Criterion | Rating |
|---|---|
| Status/maturity (March 2026) | Active — v3.5.0 released Oct 2025, v3.4.x releases through Sep 2025 |
| Headless operation | Yes — connects to any running emulator via USB/TCP |
| Semantic/accessibility tree | Partial — same constraints as raw uiautomator dump; no Compose-specific semantics |
| Setup complexity for shell agent | Medium — requires Python, pip install, agent APK install on device |

**Confidence:** Medium — Library activity and version data sourced from PyPI (primary source). Compose compatibility inferred from UIAutomator layer behavior; no explicit UIAutomator2 + CMP documentation found as of March 2026.

---

## Tool: Maestro

### Overview

Maestro is an open-source, cross-platform E2E mobile testing framework using YAML-based "flows". It runs as a standalone CLI binary and does not require Android Studio. It operates as a black-box external tool using Android's system automation interfaces (AccessibilityService and UIAutomator), not app-internal instrumentation. [Source: https://maestro.dev/, accessed 2026-03-30]

**Current stable release:** CLI 2.3.0 (March 10, 2026). The major prior milestone was **CLI 2.0.0** (August 26, 2025), which upgraded the JavaScript engine to GraalJS and introduced Maestro Studio Desktop. [Source: https://github.com/mobile-dev-inc/maestro/releases, accessed 2026-03-30; https://maestro.dev/blog/introducing-maestro-2-0-0, accessed 2026-03-30]

### CLI Usage (No Android Studio Required)

```bash
# Install Maestro CLI
curl -Ls "https://get.maestro.mobile.dev" | bash

# Launch a device (Maestro can start its own, or use running emulator)
maestro start-device --platform=android --os-version=35

# Run a YAML flow against connected/running emulator
maestro test my-flow.yaml

# Run a test suite with reports
maestro test --format junit path/to/flows/
```

Maestro detects running emulators automatically via `adb devices`. If an emulator is already running (started via `emulator -no-window`), Maestro connects to it without any extra configuration.

### YAML Flow Example (Compose App)

```yaml
appId: com.example.myapp
---
- launchApp
- tapOn:
    text: "Login"
- inputText: "user@example.com"
- tapOn:
    id: "submit_button"   # matches resource-id or testTag (with testTagsAsResourceId)
- assertVisible:
    text: "Welcome"
- takeScreenshot: "post_login"
```

An LLM agent can generate these YAML flows from natural language and execute them immediately with `maestro test flow.yaml`. [Source: https://docs.maestro.dev/get-started/supported-platform/android/jetpack, accessed 2026-03-30]

### Jetpack Compose and CMP Support

Maestro explicitly lists "Jetpack Compose" as a supported platform [Source: https://maestro.dev/, accessed 2026-03-30]. It uses three matching strategies: visible text, `contentDescription` (accessibility label), and resource ID. For Compose elements:

- **Text-based matching** works without any app changes
- **contentDescription matching** works if the composable sets `contentDescription` in semantics
- **ID matching** (`id:` in YAML) works when the app sets `testTagsAsResourceId = true` and applies `Modifier.testTag(...)`

Compose Multiplatform on Android uses the same Compose runtime as native Jetpack Compose. Maestro's black-box approach means CMP apps are treated identically to native Compose apps — there is no CMP-specific documentation, and the same Compose support applies.

### Headless Mode Limitation

Maestro's `--headless` flag applies **only to web testing** (browser-based flows). For Android emulator flows, there is no headless flag — the emulator itself must be running (headlessly via `-no-window` is fine). Maestro attaches to the running emulator via ADB.

### MCP Integration

Maestro 2.0.0 improved MCP support (50%+ reduced output size per blog post — unverified against the source; better flow path resolution). Per the 2.0.0 blog post, Maestro exposes an MCP interface for AI tooling integration — this is stated in the blog but not independently confirmed from a separate primary source. [Source: https://maestro.dev/blog/introducing-maestro-2-0-0, accessed 2026-03-30]

### Assessment

| Criterion | Rating |
|---|---|
| Status/maturity (March 2026) | Active — 134+ releases, 10,800+ GitHub stars; 2.3.0 stable released March 10, 2026 |
| Headless operation | Yes — runs against headlessly-launched emulator; no Android Studio needed |
| Semantic/accessibility tree | No direct tree export; black-box interaction via text/contentDescription/resource-id |
| Setup complexity for shell agent | Low — single binary install; YAML flows trivially generated by LLM |

**Confidence:** High for Compose/Android support claims — sourced from official Maestro docs. High for current version — 2.3.0 stable confirmed March 10, 2026 from GitHub releases page.

---

## Tool: Android Emulator gRPC/Automation API

### Overview

The Android Emulator exposes an experimental gRPC service (introduced in emulator version 29.0.6 — per single community source only; not confirmed from official Android emulator release notes — treat this version number as unverified) for programmatic control. It runs as a separate server alongside the emulator process, accessible on a configurable port (default: 5556). [Source: https://gist.github.com/mrk-han/fa5c6e8951919b7efc1ba99fcd10496e, accessed 2026-03-30]

### Enabling the gRPC Service

```bash
# Launch emulator with gRPC enabled on port 5556
~/Library/Android/sdk/emulator/emulator @Pixel8_API_35 -no-window -grpc 5556
```

### Available Operations

Based on the protocol buffer definitions (emulator controller proto), the gRPC API supports:

- Sending input events (key events, touch events)
- Screenshot capture
- Mouse event handling
- VM state queries
- GPS configuration
- SMS injection
- Logcat streaming (Linux; status on macOS unconfirmed)

The Adam library (`malinskiy/adam`) bundles a gRPC client for this bridge, with specs generated from the emulator controller `.proto` file. [Source: https://malinskiy.github.io/adam/docs/emu, accessed 2026-03-30]

### Critical Caveats

- **Status as of March 2026:** Still marked experimental. No new gRPC API additions documented in the 2025-2026 emulator release notes (releases 36.x). [Source: https://developer.android.com/studio/releases/emulator, accessed 2026-03-30]
- **No authentication or TLS:** The gRPC server performs no authentication or authorization. Anyone with access to the port can control the emulator.
- **No UI hierarchy exposure:** The gRPC API does not expose a UI semantic or accessibility tree — it provides input events and screenshots only. For semantic inspection, `adb shell uiautomator dump` is still required.
- **Platform limitations:** The gist documentation references Linux as the primary deployment; macOS support for all features (e.g., logcat via gRPC) is not explicitly confirmed.

### Go HTTP Bridge Example

```bash
# With a Go HTTP bridge running on 8080 proxying gRPC on 5556:
curl -X POST -d '{"key": "30"}' http://localhost:8080/v1/key
```

### Assessment

| Criterion | Rating |
|---|---|
| Status/maturity (March 2026) | Experimental — no new updates in 2025-2026 emulator releases |
| Headless operation | Yes — runs as server process alongside headless emulator |
| Semantic/accessibility tree | No — screenshots and input events only |
| Setup complexity for shell agent | High — requires proto compilation, gRPC client setup, security caution |

**Confidence:** Medium — Feature existence confirmed from multiple sources. March 2026 status (still experimental, no new updates) inferred from absence in emulator release notes. macOS-specific behavior not fully confirmed.

---

## Tool: Espresso / Compose UI Test (Headless via Gradle)

### Overview

Espresso is Android's built-in instrumented UI testing framework. For Compose, JetBrains provides `androidx.compose.ui:ui-test-junit4` which builds on top of Espresso for in-process Compose testing with full semantic tree access. Tests run inside the app process on a connected device or emulator.

### Running Without Android Studio (CLI)

```bash
# With emulator already running (headlessly):
./gradlew :app:connectedAndroidTest

# Or for CMP shared module:
./gradlew :shared:connectedAndroidTest
```

No Android Studio GUI is required. The Gradle task handles APK build, install, test execution, and report generation. The emulator must already be running and registered with `adb`. [Source: https://kotlinlang.org/docs/multiplatform/compose-test.html, accessed 2026-03-30]

### Compose Semantic Tree Access (Full)

Unlike `adb shell uiautomator dump`, instrumented Compose tests have **full access to the Compose semantics tree** — including all `testTag` values, `contentDescription`, role, state, and custom semantics properties — without requiring `testTagsAsResourceId`. The `SemanticsNodeInteraction` API provides complete tree introspection:

```kotlin
// Full semantics tree access in instrumented tests
composeTestRule.onNodeWithTag("loginButton")
    .assertIsDisplayed()
    .performClick()

composeTestRule.onNodeWithContentDescription("Profile picture")
    .assertExists()

// Print full semantics tree to logcat
composeTestRule.onRoot().printToLog("TREE")
```

### Gradle-Managed Devices (Fully Headless, No Pre-Existing Emulator)

Gradle Managed Devices can create, run, and tear down emulators automatically without any pre-existing AVD:

```kotlin
// build.gradle.kts
android {
    testOptions {
        managedDevices {
            devices {
                create<ManagedVirtualDevice>("pixel5api35") {
                    device = "Pixel 5"
                    apiLevel = 35
                    systemImageSource = "google-atd"  // headless ATD image
                }
            }
        }
    }
}
```

```bash
# Run tests on managed device (fully automated, no manual emulator start)
./gradlew pixel5api35DebugAndroidTest
```

ATD (Automated Test Device) images are headless-optimized: hardware rendering is disabled, unnecessary apps removed. On Apple Silicon (ARM) Macs, only API 30 ATD images are available; x86 machines support API 27+. [Source: https://developer.android.com/studio/test/managed-devices, accessed 2026-03-30]

### Limitations for LLM Agent Use

The primary limitation is the **test-code build coupling**: every test must be written as Kotlin/Java source, compiled, and deployed as an instrumented APK. This makes it poorly suited for a runtime LLM agent that wants to dynamically issue ad-hoc commands. Espresso/Compose UI Test is ideal for pre-planned, committed test suites — not for exploratory, dynamic agent sessions.

### Assessment

| Criterion | Rating |
|---|---|
| Status/maturity (March 2026) | Stable — part of AndroidX Compose; Jetpack Compose UI 1.8.0 released April 2025 (unconfirmed — verify at https://developer.android.com/jetpack/androidx/releases/compose-ui) |
| Headless operation | Yes — via `connectedAndroidTest` against `-no-window` emulator; or fully automated with Gradle Managed Devices |
| Semantic/accessibility tree | Full — complete Compose semantics tree access, all testTags, no app changes needed |
| Setup complexity for shell agent | High for dynamic use — requires Kotlin code + build/deploy cycle per test change |

**Confidence:** High — all claims sourced from official Kotlin/Android documentation.

---

## Tool: MCP Servers for Android/adb

### Overview

As of March 2026, a substantial ecosystem of MCP servers has emerged that wrap Android/ADB capabilities for LLM agents, particularly for use with Claude. These servers expose device control as structured MCP tools, eliminating the need for shell command construction by the agent.

### Inventory of Active MCP Servers

**1. CursorTouch/Android-MCP**
[Source: https://github.com/CursorTouch/Android-MCP, accessed 2026-03-30]

- Language: Not specified in available content (multi-platform)
- Key tools: `State-Tool` (combined screenshot + interactive UI elements), `Click-Tool`, `Long-Click-Tool`, `Type-Tool`, `Swipe-Tool`, `Drag-Tool`, `Press-Tool`, `Wait-Tool`, `Notification-Tool`, `Shell-Tool`
- Distinguishing feature: Operates via ADB + Android Accessibility API, no CV model required; `SCREENSHOT_QUANTIZED` env var compresses images to reduce LLM token cost
- Typical action latency: 2–4 seconds between actions

**2. AlexGladkov/claude-in-mobile**
[Source: https://github.com/AlexGladkov/claude-in-mobile, accessed 2026-03-30]

- Language: Kotlin/Rust (native desktop companion in Rust)
- Key tools (30+): `screenshot`, `tap`, `long_press`, `swipe`, `input_text`, `press_key`, `launch_app`, `stop_app`, `install_app`, `get_ui`, `find_element`, `annotate_screenshot`, `wait_for_element`, `assert_visible`, `get_logs`, `shell`, `batch_commands`, `get_webview`, and others
- Distinguishing feature: Supports Android (ADB), iOS (simctl), Desktop (Compose Multiplatform native), and Aurora OS — the only server found with explicit CMP Desktop support; JSON accessibility tree output; annotated screenshots with numbered bounding boxes
- Released: January 12, 2026

**3. minhalvp/android-mcp-server**
[Source: https://github.com/minhalvp/android-mcp-server, accessed 2026-03-30]

- Language: Python
- Key tools: `get_packages`, `execute_adb_command`, `get_uilayout`, `get_screenshot`, `get_package_action_intents`
- Distinguishing feature: `get_uilayout` returns formatted string of all clickable elements with text, descriptions, bounds, and center coordinates; `execute_adb_command` provides arbitrary adb access
- GitHub stars: 713 (as of March 2026); 82 forks

**4. watabee/mcp-server-adb**
[Source: https://github.com/watabee/mcp-server-adb, accessed 2026-03-30]

- Language: TypeScript
- Key tools (17): `get-devices`, `list-packages`, `install-apk`, `uninstall-apk`, `clear-app-data`, `push`, `pull`, `screencap`, `grant-permission`, `revoke-permission`, `reset-permissions`, `start-activity`, `kill-server`, `start-server`, `help`, `input-text`, `rm`
- Created: February 23, 2025
- Limitation: No UI hierarchy inspection tool documented

**5. mobile-next/mobile-mcp**
[Source: https://github.com/mobile-next/mobile-mcp, accessed 2026-03-30]

- Language: Not specified
- Key tools: `mobile_list_available_devices`, `mobile_take_screenshot`, `mobile_list_elements_on_screen`, `mobile_click_on_screen_at_coordinates`, `mobile_double_tap_on_screen`, `mobile_long_press_on_screen_at_coordinates`, `mobile_swipe_on_screen`, `mobile_type_keys`, `mobile_press_button`, `mobile_open_url`, `mobile_launch_app`, `mobile_terminate_app`, `mobile_install_app`, `mobile_get_screen_size`
- Distinguishing feature: `mobile_list_elements_on_screen` provides both accessibility-based structured data AND screenshot fallback; explicit support for Android Emulators on Linux/Windows/macOS confirmed in docs
- Installation: `@mobilenext/mobile-mcp@latest` via npm/npx

**6. ComposeProof** (Compose Multiplatform specialized)
[Source: https://composeproof.dev/, accessed 2026-03-30]

- Language: Not specified
- Status: v1.1, actively developed; Multiplatform & CI wave planned as next release
- Key tools (40+): `render`, `list_previews`, `verify`, `render_batch`, `diff`, `device_interact` (tap/swipe/type/scroll), `generate_edge_cases`, `mock_api`, `inspect_ui_tree`, `inspect_permissions`, `inspect_navigation_graph`, and expert prompt tools (`compose-performance`, `ui-reviewer`, `spec-verifier`)
- Distinguishing feature: Headless Compose rendering without an emulator (renders composables at build time); in-process `inspect_ui_tree` with full Compose semantics; API mocking without code changes
- Limitation: "No emulator needed" means it tests composables in isolation, not full app integration

**7. benoberkfell/android-a11y-mcp** (Accessibility-focused)
[Source: https://lobehub.com/mcp/benoberkfell-android-a11y-mcp, accessed 2026-03-30 — note: 403 on direct fetch; data from LobeHub proxy]

- Uses WebSocket server on Android that exposes the Android Accessibility API
- Screenshot via `AccessibilityService.takeScreenshot()` (requires Android 11+)
- Exposes accessibility tree directly from the running accessibility service

### Comparison Table

| Server | Language | Screenshot | UI Tree | Input | Compose Specific | Last Active |
|---|---|---|---|---|---|---|
| CursorTouch/Android-MCP | Unknown | Yes | Via Accessibility API | Yes | No | 2025-2026 |
| AlexGladkov/claude-in-mobile | Kotlin/Rust | Yes (annotated) | JSON a11y tree | Yes | CMP Desktop | Jan 2026 |
| minhalvp/android-mcp-server | Python | Yes | Clickable elements | Via adb | No | Mar 2026 |
| watabee/mcp-server-adb | TypeScript | Yes | No | Yes (text only) | No | Feb 2025 |
| mobile-next/mobile-mcp | Unknown | Yes | Accessibility + vision | Yes | No | 2025-2026 |
| ComposeProof | Unknown | Yes | Full Compose semantics | Yes (in-process) | Yes (Android) | 2025-2026 |
| benoberkfell/android-a11y-mcp | Unknown | Yes (AccessibilitySvc) | Full a11y tree | No documented | No | 2025 |

**Confidence:** High for server existence and feature descriptions (all sourced from GitHub READMEs and project pages accessed March 2026). Medium for production maturity — most are community projects with no formal release SLAs.

---

## Tool: Android Studio Gemini AI (Programmatic Access)

**Out-of-scope negative result.** Android Studio's AI features (code generation, refactoring, test generation) are IDE plugins operating within the IntelliJ platform — they are not exposed as APIs or CLI tools and cannot be invoked from Claude Code or shell commands. The Gemini Developer API (Google AI Studio) is available externally but is a general-purpose model API unrelated to Android Studio automation. An LLM agent running in Claude Code is already Claude — there is no value in routing through Android Studio's Gemini integration. [Sources: https://developer.android.com/studio/gemini/overview; https://android-developers.googleblog.com/2025/11/gemini-3-is-now-available-for-ai.html — accessed 2026-03-30]

**Confidence:** High — conclusion is a direct inference from documented IDE constraints.

---

## Tool: Compose Multiplatform Android Accessibility

### How CMP Exposes Semantics on Android

Compose Multiplatform (CMP) on Android uses the same Compose runtime and rendering engine as native Jetpack Compose. There is no separate accessibility layer for CMP Android targets — the Compose semantic tree is generated by the same `Modifier.semantics { }` / `Modifier.testTag()` infrastructure and translated to Android `AccessibilityNodeInfo` objects by the same code path.

The key semantic properties available to external automation tools:

| Property | How set in CMP | How visible externally |
|---|---|---|
| `contentDescription` | `Modifier.semantics { contentDescription = "..." }` | `content-desc` attribute in uiautomator dump |
| `testTag` | `Modifier.testTag("id")` | `resource-id` in dump **only if** `testTagsAsResourceId = true` |
| `text` | Text composable content | `text` attribute in dump |
| `role` | `Modifier.semantics { role = Role.Button }` | Maps to AccessibilityNodeInfo class name |
| `stateDescription` | `Modifier.semantics { stateDescription = "..." }` | In AccessibilityNodeInfo extras |

[Source: https://kotlinlang.org/docs/multiplatform/compose-accessibility.html, accessed 2026-03-30; https://developer.android.com/develop/ui/compose/accessibility/semantics, accessed 2026-03-30]

### The testTagsAsResourceId Requirement

This is the single most important configuration decision for an LLM agent automating a CMP app on Android emulator.

**Without it:** `adb shell uiautomator dump` produces an XML where Compose UI shows as a single `<node class="androidx.compose.ui.platform.ComposeView">` with no children. All Compose UI structure is invisible to the dump.

**With it:** Each composable that has `Modifier.testTag("foo")` appears as a `<node resource-id="foo">` in the dump XML, traversable and findable by UIAutomator, Maestro (via `id:`), and all MCP servers.

**How to enable (app must set this once at the root):**

```kotlin
// In the top-level composable (e.g., App() function or main Scaffold)
Scaffold(
    modifier = Modifier.semantics {
        testTagsAsResourceId = true
    }
) {
    // All Modifier.testTag(...) composables in here will appear in uiautomator dump
}
```

Requires Jetpack Compose 1.2.0+ (stable since 2022; CMP 1.8+ aligns with Compose 1.8). Note: the 1.2.0 minimum version is inferred from available documentation — no primary source explicitly confirms this as the minimum. Verify against https://developer.android.com/jetpack/androidx/releases/compose-ui if precision is required. [Source: https://developer.android.com/develop/ui/compose/testing/interoperability, accessed 2026-03-30; https://medium.com/androiddevelopers/accessing-composables-from-uiautomator-cf316515edc2, accessed 2026-03-30]

### What the uiautomator dump XML Looks Like (CMP with testTagsAsResourceId)

With `testTagsAsResourceId = true` and appropriate `Modifier.testTag(...)` applied:

```xml
<hierarchy rotation="0">
  <node class="android.view.ViewRootImpl" ...>
    <node class="androidx.compose.ui.platform.ComposeView" package="com.example.app" ...>
      <node resource-id="loginScreen" class="android.view.View" clickable="false" ...>
        <node resource-id="emailField" class="android.widget.EditText" text=""
              bounds="[32,300][688,380]" clickable="true" .../>
        <node resource-id="passwordField" class="android.widget.EditText" text=""
              bounds="[32,400][688,480]" clickable="true" .../>
        <node resource-id="loginButton" class="android.widget.Button" text="Login"
              bounds="[200,520][520,600]" clickable="true" .../>
      </node>
    </node>
  </node>
</hierarchy>
```

Without `testTagsAsResourceId`, the entire inner hierarchy collapses to the single `ComposeView` node.

### Compose Multiplatform Version Context

- CMP 1.8.0 (released May 6, 2025) — iOS stable, major accessibility improvements on iOS. Android behavior unchanged from Compose 1.8.0 baseline.
- CMP 1.10.3 — latest stable release at research date. [Source: CMP release notes — verify at https://www.jetbrains.com/help/kotlin-multiplatform-dev/whats-new-compose-multiplatform.html]
- CMP 1.8.x (CMP 1.8.0 released May 6, 2025) — iOS stable milestone; Android behavior follows Compose 1.8.x baseline. [Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-180.html, accessed 2026-03-30]
- CMP 1.9.0 (released September 2025) — web beta; no Android accessibility breaking changes noted. [Source: https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/, accessed 2026-03-30]

**Confidence:** High — accessibility mechanism and `testTagsAsResourceId` behavior sourced from official Android documentation and Google Android Developers blog.

---

## Recommended Approach

For an LLM agent (Claude Code CLI on macOS) automating a CMP Android app in the emulator with no Android Studio GUI, the following layered tool chain is recommended:

### Layer 0: App Precondition (One-Time Setup)

The CMP app must enable `testTagsAsResourceId` at its root composable and apply `Modifier.testTag(...)` to all elements the agent needs to interact with. Without this, structural UI inspection is unavailable.

### Layer 1: Emulator Lifecycle (raw adb/emulator CLI)

```bash
# Create AVD (one-time) — Apple Silicon Mac:
~/Library/Android/sdk/cmdline-tools/latest/bin/sdkmanager \
  "system-images;android-35;google_apis;arm64-v8a"
~/Library/Android/sdk/cmdline-tools/latest/bin/avdmanager create avd \
  -n CMP_Test -k "system-images;android-35;google_apis;arm64-v8a" -d pixel_8

# Launch headlessly
~/Library/Android/sdk/emulator/emulator @CMP_Test -no-window -no-audio -no-boot-anim &

# Wait for ready
adb wait-for-device shell 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done'

# Install app
adb install -r app-debug.apk

# Launch app
adb shell am start -n com.example.myapp/.MainActivity
```

### Layer 2: Screenshot + UI Inspection (adb shell)

```bash
# Screenshot (fast, no device temp file)
adb exec-out screencap -p > /tmp/screen.png

# Semantic UI tree (XML)
adb exec-out uiautomator dump /dev/tty > /tmp/ui.xml

# Parse XML to find element bounds
# (agent reads XML, extracts resource-id="loginButton" bounds="[200,520][520,600]")
# Center of bounds: x = (200+520)/2 = 360, y = (520+600)/2 = 560
adb shell input tap 360 560
```

### Layer 3: MCP Server (Recommended for Claude Code)

For use directly inside Claude Code CLI, configure one of the following MCP servers in `~/.claude/settings.json` (or project `.claude/settings.json`):

**Recommended: `mobile-next/mobile-mcp`** — explicit Android emulator support on macOS, structured accessibility tree output, screenshot fallback, active maintenance.

```bash
# Install
npx @mobilenext/mobile-mcp@latest

# Or add to Claude Code MCP config:
# "mobile-mcp": { "command": "npx", "args": ["@mobilenext/mobile-mcp@latest"] }
```

**Alternative: `CursorTouch/Android-MCP`** — lightweight, uses Accessibility API directly (not just uiautomator dump), no CV pipeline required.

**Alternative: `AlexGladkov/claude-in-mobile`** — if the project also needs CMP Desktop automation in the same session; provides annotated screenshots and JSON accessibility trees.

### Layer 4: High-Level E2E Flows (Maestro, for pre-planned test scenarios)

When the agent needs to validate complete user flows (not just ad-hoc inspection), generate and run Maestro YAML:

```bash
# Agent generates this YAML and writes to flow.yaml, then runs:
maestro test flow.yaml
```

Maestro requires no app changes for text/contentDescription matching, and works with resource IDs (via testTagsAsResourceId) for `id:` matching.

### Agent Loop Pattern

```
1. adb exec-out screencap -p > /tmp/screen.png
   → Read visual state (LLM sees screenshot)

2. adb exec-out uiautomator dump /dev/tty > /tmp/ui.xml
   → Read structural state (LLM parses XML, finds element bounds)

3. adb shell input tap X Y   (or swipe/text/keyevent)
   → Execute action

4. Repeat from 1
```

If using an MCP server, steps 1–3 collapse to MCP tool calls: `mobile_take_screenshot`, `mobile_list_elements_on_screen`, `mobile_click_on_screen_at_coordinates`.

---

## Gaps and Limitations

1. **testTagsAsResourceId is not enabled by default.** All semantic-tree-based automation (uiautomator dump, UIAutomator2, Maestro ID matching) requires explicit app-side configuration. Coordinate-only automation (screenshot + tap at pixel) works without this, but is brittle to layout changes and resolution differences.

2. **Android Emulator gRPC API remains experimental as of March 2026.** No new gRPC features were documented in emulator 35.x or 36.x releases. The API covers input and screenshots but not UI tree inspection — it does not replace uiautomator dump.

3. **MCP server ecosystem is fragmented and community-driven.** The 7 servers catalogued have varying maturity levels; most have no formal versioning, no SLAs, and no dedicated Compose Multiplatform support. They should be evaluated in-project before committing.

4. **Coordinate-based input requires resolution awareness.** `adb shell input tap X Y` uses absolute pixel coordinates. Different AVD screen sizes/densities require different coordinates — the agent must parse `bounds` from the uiautomator dump rather than hardcode coordinates.

5. **UIAutomator dump can time out or produce incomplete output.** Known issue on some Compose apps: `adb shell uiautomator dump` can return a partially populated or empty XML if the app is mid-animation. The agent should retry or add a short delay after navigation actions.

6. **`adb shell uiautomator dump` StackOverflowError on deeply nested Compose UI.** Observed in analogous Flutter behavior [Source: https://github.com/flutter/flutter/issues/74197, accessed 2026-03-30] — verify whether this applies identically to Compose rather than Flutter specifically. Extremely deep composition trees can cause the dump to fail with `StackOverflowError`. Mitigation: use shallow composition, avoid excessive nesting, or use an MCP server that queries accessibility via the AccessibilityService instead.

7. **Apple Silicon ATD constraints.** Gradle Managed Devices with ATD (headless-optimized) images support only API level 30 on ARM Macs as of March 2026. For API 35 testing on Apple Silicon, use standard google_apis images with a regular (non-ATD) emulator.

8. **Android Studio Gemini is not an agent-accessible tool.** No external API access to IDE AI features exists as of March 2026.

9. **benoberkfell/android-a11y-mcp is community-unverified.** This server was sourced only from a LobeHub proxy page (which returned a 403 on direct fetch). No GitHub primary source was found. Feature descriptions and availability should be treated as unverified/community-sourced until confirmed from the primary repository.

---

## Sources

| URL | Source Name | Access Date |
|---|---|---|
| https://developer.android.com/tools/adb | ADB Official Docs — Android Developers | 2026-03-30 |
| https://developer.android.com/studio/run/emulator-commandline | Emulator Command Line — Android Developers | 2026-03-30 |
| https://developer.android.com/studio/releases/emulator | Emulator Release Notes — Android Developers | 2026-03-30 |
| https://developer.android.com/develop/ui/compose/testing/interoperability | Compose Testing Interoperability — Android Developers | 2026-03-30 |
| https://developer.android.com/develop/ui/compose/accessibility/semantics | Compose Semantics — Android Developers | 2026-03-30 |
| https://developer.android.com/studio/test/managed-devices | Gradle Managed Devices — Android Developers | 2026-03-30 |
| https://developer.android.com/studio/gemini/overview | Gemini in Android Studio — Android Developers | 2026-03-30 |
| https://android-developers.googleblog.com/2025/11/gemini-3-is-now-available-for-ai.html | Gemini 3 in Android Studio Blog Post — Android Developers Blog | 2026-03-30 |
| https://github.com/CursorTouch/Android-MCP | CursorTouch/Android-MCP — GitHub | 2026-03-30 |
| https://github.com/AlexGladkov/claude-in-mobile | AlexGladkov/claude-in-mobile — GitHub | 2026-03-30 |
| https://github.com/minhalvp/android-mcp-server | minhalvp/android-mcp-server — GitHub | 2026-03-30 |
| https://github.com/watabee/mcp-server-adb | watabee/mcp-server-adb — GitHub | 2026-03-30 |
| https://github.com/mobile-next/mobile-mcp | mobile-next/mobile-mcp — GitHub | 2026-03-30 |
| https://composeproof.dev/ | ComposeProof — Official Site | 2026-03-30 |
| https://github.com/openatx/uiautomator2 | openatx/uiautomator2 — GitHub | 2026-03-30 |
| https://pypi.org/project/uiautomator2/ | uiautomator2 — PyPI | 2026-03-30 |
| https://github.com/mobile-dev-inc/maestro | mobile-dev-inc/Maestro — GitHub | 2026-03-30 |
| https://github.com/mobile-dev-inc/maestro/releases | Maestro Releases — GitHub | 2026-03-30 |
| https://maestro.dev/ | Maestro Official Site | 2026-03-30 |
| https://docs.maestro.dev/maestro-cli/maestro-cli-commands-and-options | Maestro CLI Commands — Maestro Docs | 2026-03-30 |
| https://docs.maestro.dev/get-started/supported-platform/android/jetpack | Maestro Jetpack Compose Support — Maestro Docs | 2026-03-30 |
| https://maestro.dev/blog/introducing-maestro-2-0-0 | Maestro 2.0.0 Release Blog | 2026-03-30 |
| https://malinskiy.github.io/adam/docs/emu | Adam Emulator Docs | 2026-03-30 |
| https://gist.github.com/mrk-han/fa5c6e8951919b7efc1ba99fcd10496e | Android Emulator gRPC Guide — GitHub Gist | 2026-03-30 |
| https://kotlinlang.org/docs/multiplatform/compose-accessibility.html | CMP Accessibility — Kotlin Docs | 2026-03-30 |
| https://kotlinlang.org/docs/multiplatform/whats-new-compose-180.html | CMP 1.8.x What's New — Kotlin Docs | 2026-03-30 |
| https://www.jetbrains.com/help/kotlin-multiplatform-dev/whats-new-compose-multiplatform.html | CMP Release Notes (latest) — JetBrains Docs | 2026-03-30 |
| https://medium.com/androiddevelopers/accessing-composables-from-uiautomator-cf316515edc2 | Accessing Composables from UIAutomator — Android Developers Medium | 2026-03-30 |
| https://www.repeato.app/extracting-layout-and-view-information-via-adb/ | ADB UI Extraction — Repeato Blog | 2026-03-30 |
| https://www.blog.brightcoding.dev/2025/08/24/control-android-devices-with-ai-using-adb-and-natural-language/ | Control Android with AI/ADB — BrightCoding Blog (Aug 2025) | 2026-03-30 |
| https://dev.to/tiagodanin/creating-an-ai-agent-in-claude-code-to-control-my-smartphone-1e3e | AI Agent in Claude Code for Android — Dev.to | 2026-03-30 |
| https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/ | CMP 1.9.0 Release — JetBrains Blog (Sep 2025) | 2026-03-30 |
| https://lobehub.com/mcp/benoberkfell-android-a11y-mcp | benoberkfell/android-a11y-mcp — LobeHub proxy (403 on direct fetch; community-unverified) | 2026-03-30 |
| https://github.com/flutter/flutter/issues/74197 | Flutter uiautomator StackOverflowError issue — GitHub (analogous behavior; verify for Compose) | 2026-03-30 |
