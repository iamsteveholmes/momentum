---
research_date: 2026-03-30
agent_focus: Compose Multiplatform Web functional/acceptance testing capabilities
sources_consulted:
  - https://kotlinlang.org/docs/multiplatform/compose-test.html
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-110.html
  - https://kotlinlang.org/docs/multiplatform/compose-accessibility.html
  - https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/
  - https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/
  - https://blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/
  - https://blog.jetbrains.com/kotlin/2025/05/present-and-future-kotlin-for-web/
  - https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.0
  - https://github.com/JetBrains/compose-multiplatform/issues/4167
  - https://slack-chats.kotlinlang.org/t/16636412/should-the-new-compose-ui-testing-functionality-work-with-wa
  - https://bitspittle.dev/blog/2024/c4w
  - https://playwright.dev/docs/accessibility-testing
  - https://youtrack.jetbrains.com/issue/CMP-5937
  - https://religada.com/compose-multiplatform-1-9-0-key-updates-in-design-accessibility-and-web-support
last_verified: 2026-03-30
---

# CMP Web Functional Testing: Research Report

**Research Date:** March 30, 2026
**Question:** What functional/acceptance testing capabilities exist for Compose Multiplatform Web apps as of March 2026? What can actually drive the running web app end-to-end?

---

## Executive Verdict

**No tool currently exists that meets the "actually using the app" bar for CMP Web.** The fundamental constraint is architectural: CMP Web renders into an HTML `<canvas>` element, not a standard DOM tree. This makes it opaque to every major browser automation tool (Playwright, Selenium, WebDriver). The partial mitigation introduced in CMP 1.9.0 — accessibility overlays enabled via `isA11YEnabled` — exposes limited semantic information to screen readers, and may allow Playwright's accessibility-tree-based locators to reach some elements. However, this is unvalidated as of March 2026, covers only "initial" accessibility, and is explicitly not yet ready for production use. `compose-ui-test` does run on the wasmJs target in a headless browser, but it drives Compose's internal semantic tree, not the app as a user experiences it in a real browser session. The gap between component-level harness and true E2E acceptance testing remains unresolved.

---

## 1. compose-ui-test for Web

**Confidence: Medium** (documented behavior, but browser depth is unclear)

### What the library does

Compose Multiplatform's common test API (`compose.ui.test`) supports a `wasmJs` target. The test entry point is `runComposeUiTest { }`, which does not use JUnit `TestRule` (no JUnit dependency on web). Instead it returns a `Promise` on web targets and executes the test body asynchronously with delays skipped.

[Source: kotlinlang.org/docs/multiplatform/compose-test.html, accessed 2026-03-30]
[Source: kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

The Gradle command to run wasmJs tests is:

```
./gradlew :composeApp:wasmJsTest
```

This was listed in official documentation without qualification. [Source: kotlinlang.org/docs/multiplatform/compose-test.html, accessed 2026-03-30]

### Does it run in a real browser?

**Unclear from official docs.** The documentation confirms the wasmJs target is supported and that the execution is Promise-based, but does not specify whether `wasmJsTest` executes in:
- A headless Chromium instance (via Karma or similar)
- A real browser session
- A Node.js-like Wasm runtime with no DOM

Kotlin/JS tests (which share infrastructure with wasmJs) have historically used Karma with headless Chrome. The wasmJs test task likely follows the same pattern — headless Chrome, driven by Karma. This would mean the Compose semantic tree is evaluated but there is no browser UI surface and no real user session.

### Is it acceptance-level or unit-level?

**Unit-level (component harness), not acceptance-level.**

The `runComposeUiTest` API instantiates components inside its own managed environment. It does not load a served URL, does not navigate a real browser, and does not exercise the app's actual entry point (`ComposeViewport`). Tests interact with Compose's semantic node tree directly, bypassing the canvas rendering and the browser DOM. You can find nodes by `testTag`, assert on content descriptions, and simulate clicks — but you are testing the Compose tree in isolation, not the running app.

This is equivalent to Espresso on Android: powerful for component verification, but not a substitute for driving the full deployed app through a browser.

### Version and status

The `runComposeUiTest` suspend-lambda API was finalized in CMP 1.9.3 (released alongside the 1.9.x Beta series, September 2025). The API is marked **Experimental** and may change. [Source: kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

CMP 1.10.0 (January 13, 2026) and 1.10.3 release notes contain no testing-related changes for web. [Source: github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.0, accessed 2026-03-30]

---

## 2. Playwright Integration

**Confidence: Low** (no documented CMP-specific patterns; inference only)

### Why Playwright faces a structural problem

CMP Web renders its entire UI into a single HTML `<canvas>` element. One independent technical analysis (bitspittle.dev, October 2024 — potentially stale) described the core issue:

> "what you are fundamentally doing is creating a simple HTML page that hosts a single, fullscreen canvas element"
> "any buttons, text, or other widgets that you create are not visible to search engines"
> "all styling happens inside the canvas" making browser DevTools "rendered useless"

[Source: bitspittle.dev/blog/2024/c4w, accessed 2026-03-30 — note: written October 2024, may not reflect 1.9.0+ changes]

Playwright's primary locator strategies (`getByRole`, `getByText`, `getByLabel`, `getByTestId`) all rely on the browser's DOM and accessibility tree. A single opaque `<canvas>` element exposes none of this. Playwright's `getByRole('button')` would return zero matches against a CMP Web app unless accessibility overlays are present.

### CMP 1.9.0 accessibility changes: partial mitigation

CMP 1.9.0 (September 2025) introduced `isA11YEnabled` on `ComposeViewport`, enabled by default:

```kotlin
ComposeViewport(
    viewportContainer = document.body!!,
    configure = { isA11YEnabled = false } // disable if needed
) { /* app content */ }
```

[Source: kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

The release notes state this "enables screen readers to access description labels and allows users to navigate and click buttons in accessible navigation mode." The implementation mechanism (shadow DOM, ARIA overlay, hidden DOM nodes) is not specified in official documentation.

**The critical unresolved question:** If `isA11YEnabled` causes CMP to emit ARIA-labeled DOM nodes alongside the canvas, then Playwright's `getByRole` and `getByLabel` locators *could* find and interact with them. This would make accessibility-tree-based Playwright testing feasible. If the accessibility support operates only via browser accessibility APIs (not DOM nodes), Playwright would still be blocked.

**No documented Playwright + CMP Web example or pattern exists as of March 2026.** No GitHub repositories, blog posts, or official JetBrains guidance on this combination was found during research.

### Coordinate-based Playwright as a fallback

Playwright supports `page.mouse.click(x, y)` for coordinate-based interaction. This can drive a canvas app, but:
- Coordinates are brittle and break with layout changes
- It provides no semantic assertions (cannot verify "the button labeled Login was clicked")
- Screenshot/visual comparison can validate outcomes, but is fragile and slow
- This is not acceptance-level testing in any meaningful sense

No CMP Web + coordinate-based Playwright examples were found in community sources.

---

## 3. Kotlin/Wasm Test Infrastructure

**Confidence: Medium**

### What runs wasmJs tests

The `wasmJsTest` Gradle task uses the Kotlin/Wasm browser test infrastructure, which as of Kotlin 2.1.x (current as of March 2026) runs tests in a headless browser environment. Based on Kotlin/JS precedent (which uses Karma + headless Chrome), wasmJs tests also execute in headless Chrome. Tests are executed as Wasm modules loaded in the browser VM.

This means:
- Tests **do run in a real browser engine** (Chromium, headless)
- Tests **do not load a served app URL**
- Tests exercise Compose's internal machinery, not the deployed application

### Kotest

Kotest supports the wasmJs target for unit/integration testing. [Source: kotest.io, accessed 2026-03-30] Kotest provides richer assertion DSLs and property-based testing, but operates at the same level as `runComposeUiTest` — component/unit level, not E2E.

### No dedicated E2E runner for CMP Web exists

No framework that: (a) serves the CMP Web app, (b) opens it in a real browser, (c) drives it through its actual UI using semantic identifiers has been documented or found in community sources as of March 2026.

---

## 4. End-to-End Testing Frameworks Validated Against CMP Web

**Confidence: High** (the answer is: none validated)

A search across JetBrains documentation, GitHub, community Slack archives, and technical blogs found **zero documented examples** of any E2E framework (Playwright, Selenium, Cypress, WebdriverIO, Maestro) validated against a running CMP Web/Wasm app.

General observations from community sources:

- The canvas-rendering architecture makes standard DOM-based E2E tools non-functional out of the box
- The new `WebElementView()` composable (CMP 1.9.0) allows embedding real HTML elements into the canvas, which *are* reachable by Playwright. But this is for embedding arbitrary HTML content, not for exposing CMP UI components
- No one in the Kotlin community appears to have published a working CMP Web + Playwright test suite

[Source: github.com/JetBrains/compose-multiplatform, github.com/topics/compose-testing, accessed 2026-03-30]

---

## 5. JetBrains Official Testing Guidance for CMP Web

**Confidence: High** (absence of guidance is itself a finding)

JetBrains' official documentation on testing Compose Multiplatform UI (kotlinlang.org/docs/multiplatform/compose-test.html) provides:
- The `wasmJsTest` Gradle command
- The `runComposeUiTest` API reference
- Platform-specific commands (iOS, Android, JVM, wasmJs)

It does **not** provide:
- Any guidance on E2E or acceptance testing for web
- Any mention of Playwright, Selenium, or browser automation for CMP Web
- Any statement about what the "wasmJsTest" task actually executes against (real browser vs headless vs VM)
- Any roadmap for E2E testing tooling

The August 2025 roadmap update (blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/) and the May 2025 "Present and Future of Kotlin for Web" post (blog.jetbrains.com/kotlin/2025/05/present-and-future-kotlin-for-web/) contain **no mention of testing infrastructure** for web targets.

JetBrains has filed accessibility issues (e.g., YouTrack CMP-5937: "Compose Multiplatform Web/Wasm support accessibility") but has not published testing guidance tied to those improvements.

**JetBrains' effective guidance: use `runComposeUiTest` for component-level testing, nothing more.** There is no official recommendation for "actually using the app" testing on the web target.

---

## 6. Known Limitations and Explicit Non-Starters

**Confidence: High**

### Approaches that do NOT work for CMP Web

| Approach | Why it Fails |
|---|---|
| `Playwright.getByRole()` / `getByText()` / `getByLabel()` | Canvas renders no DOM nodes for CMP UI elements; accessibility overlay status unclear |
| Selenium/WebDriver CSS or XPath selectors | Same reason: no DOM elements corresponding to CMP widgets |
| `Modifier.testTag` for Playwright selection | testTags exist in Compose semantic tree, not in browser DOM; no bridge exists |
| Cypress `cy.get()` / `cy.contains()` | DOM-based; same fundamental blocker |
| JUnit-based `compose.uiTestJUnit4` on wasmJs | JUnit rule architecture not available on web; `runComposeUiTest` is the only API |
| Android `connectedAndroidTest` configs | Web target only; no crossover |

### Approaches with significant caveats

| Approach | Caveat |
|---|---|
| `runComposeUiTest { }` on wasmJs | Component harness only; does not test deployed app; API is Experimental |
| Playwright coordinate-based click | Works mechanically but fragile, no semantic assertions, not acceptance-level |
| Playwright screenshot comparison | Can detect visual regressions; does not verify semantic behavior; slow, brittle |
| Playwright accessibility tree (if `isA11YEnabled` exposes DOM nodes) | Unverified as of March 2026; depends on implementation mechanism not yet documented; "initial" support only |

### What CMP Web specifically lacks that other platforms have

- **Android:** Espresso + instrumented tests drive the real running app. XCUITest on iOS similarly drives the live app. **CMP Web has no equivalent.**
- **React/Vue/Angular web apps:** Playwright's `getByRole` works because those frameworks render real DOM. CMP Web's canvas rendering opts out of the DOM.
- **Jetpack Compose (Android):** Full acceptance testing via Espresso in instrumented tests. No parallel exists for web.

---

## Summary Table

| Capability | Supported? | Level | Confidence |
|---|---|---|---|
| `compose-ui-test` on wasmJs target | Yes | Component harness (not app-level) | Medium |
| Tests run in real browser engine | Probably (headless) | Infrastructure only | Medium |
| Tests drive actual deployed app URL | No | — | High |
| Playwright with DOM/role locators | Not documented as working | Blocked by canvas architecture | High |
| Playwright with coordinate clicks | Mechanically possible | Fragile; not acceptance-level | High |
| Playwright with accessibility tree | Unverified; possible if a11y overlay exposes DOM | Experimental | Low |
| Selenium/WebDriver | Not documented as working | Blocked by canvas architecture | High |
| Any E2E framework validated against CMP Web | None found | — | High |
| JetBrains official E2E guidance | None exists | — | High |
| Testing roadmap for CMP Web | Not published | — | High |

---

## Provenance Notes

- CMP 1.9.0: released September 2025 — introduced accessibility support for web, Beta status. Primary source: JetBrains blog.
- CMP 1.10.0: released January 13, 2026 — no testing changes. Primary source: GitHub release notes.
- bitspittle.dev canvas analysis: written October 2024. May not reflect 1.9.0 accessibility changes. Flagged as potentially stale.
- Slack thread (slack-chats.kotlinlang.org/t/16636412): returned 403 during research; content summary from search snippet only.
- YouTrack CMP-5937: returned JavaScript-only content; full issue text unavailable.
- No source found documenting the internal mechanism (shadow DOM, ARIA, etc.) used by `isA11YEnabled`. This is the single most important open question for Playwright feasibility.
