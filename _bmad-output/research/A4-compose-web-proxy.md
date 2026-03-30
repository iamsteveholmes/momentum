---
research_date: 2026-03-30
agent_focus: Compose for Web as verification proxy for LLM agents
sources_consulted:
  - https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/
  - https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/
  - https://blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/
  - https://blog.jetbrains.com/kotlin/2025/05/present-and-future-kotlin-for-web/
  - https://kotlinlang.org/docs/multiplatform/supported-platforms.html
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html
  - https://kotlinlang.org/docs/multiplatform/compose-accessibility.html
  - https://kotlinlang.org/docs/multiplatform/compose-test.html
  - https://kotlinlang.org/docs/wasm-get-started.html
  - https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.0
  - https://github.com/JetBrains/compose-hot-reload
  - https://bitspittle.dev/blog/2024/c4w
  - https://www.kmpship.app/blog/kotlin-wasm-and-compose-web-2025
  - https://www.kmpship.app/blog/is-kotlin-multiplatform-production-ready-2026
  - https://www.getautonoma.com/blog/flutter-playwright-testing-guide
  - https://medium.com/@ragnorak-dev/my-first-feelings-with-compose-multiplatform-for-web-js-kotlin-wasm-91de8022d093
  - https://slack-chats.kotlinlang.org/t/27562635/
  - https://blog.jetbrains.com/amper/2025/10/amper-update-october-2025/
  - https://github.com/MohamedRejeb/Calf
  - https://playwright.dev/docs/browsers
search_queries_used:
  - "Compose Multiplatform Wasm stable 2025 2026 release"
  - "Compose for Web Playwright automation 2025"
  - "Compose Multiplatform web target feature parity limitations 2025"
  - "Compose for Web canvas DOM rendering Playwright accessibility ARIA 2025"
  - "Kotlin Wasm Compose browser automation accessibility tree 2025"
  - "Compose Multiplatform web skia canvas rendering DOM elements testing automation"
  - "Compose Multiplatform web accessibility screen reader semantic tree 2025 ARIA"
  - "Compose for Web Playwright testing canvas automation 2024 2025"
  - "Compose Multiplatform web ComposeViewport vs CanvasBasedWindow deprecated accessibility DOM 2025"
  - "Compose Multiplatform web wasmJsBrowserDevelopmentRun hot reload HMR dev server 2025"
  - "Compose Multiplatform web navigation API missing features limitations 2025 2026"
  - "Compose Multiplatform 1.10 web Kotlin/JS deprecated Wasm only 2026"
  - "Compose Multiplatform web missing APIs camera sensor platform permissions 2025"
  - "Flutter web Playwright automation canvas accessibility testing strategy proxy mobile 2025"
  - "Compose Multiplatform web stable release date 2026 timeline roadmap"
  - "Compose for Web beta limitations real world production apps 2025 2026 review"
  - "Compose Multiplatform web rendering DOM elements accessibility overlay ARIA how it works technical 2025"
  - "Compose Multiplatform web Playwright getByRole getByText testTag canvas accessibility works 2025"
last_verified: 2026-03-30
---

# A4: Compose for Web as LLM Verification Proxy
## Research Date: March 30, 2026

## How to Read This Document

Two confidence signals are used throughout:
- **Inline ⚠️ markers** — appear at the point of a specific claim to flag a gap, unverified detail, or source-quality concern. Read them where they appear.
- **Section-level `Confidence:` ratings** — appear at the end of major sections and summarize the overall evidential quality of that section (High / Medium / Low).

These are complementary: a section rated "Medium" overall may still contain individual claims with ⚠️ markers for specific gaps.

---

## Executive Summary

Compose for Web (Kotlin/Wasm) reached Beta status in September 2025 with version 1.9.0. As of March 2026, the latest stable release is **1.10.3** and **1.11.0** is in Beta — the web target remains in Beta status across the 1.10.x series. The framework renders primarily to a Skia-based canvas element, not the browser DOM. This is the single most consequential architectural fact for LLM agent verification: standard Playwright DOM selectors cannot query UI elements inside the canvas. However, Compose 1.9.3 enabled accessibility support by default, creating a semantic overlay tree that Playwright can query via role- and label-based locators — provided the app uses `ComposeViewport` (not the deprecated `CanvasBasedWindow`). ⚠️ Note: the exact Playwright behavior against Compose's accessibility DOM is not directly documented in official sources; confidence is based on accessibility overlay documentation and Flutter Web analogies (see Playwright Compatibility section).

The Web target shares the same Compose API surface as Android/iOS for business logic and pure UI composition, but lacks platform APIs (camera, sensors, permissions), has incomplete accessibility coverage, does not support Compose Hot Reload on web (JVM/desktop only), and requires `./gradlew wasmJsBrowserDevelopmentRun` with manual file-watch flags for live development. For an LLM agent verifying shared business logic and UI state transitions, the Web target is a viable but imperfect proxy — best suited for data-heavy apps, form flows, and navigation verification; least suited for platform-API-heavy apps or pixel-fidelity testing.

---

## Compose for Web — Current Status (March 2026)

### Kotlin/Wasm Target

**Status: Beta (not Stable) as of March 2026**

JetBrains released Compose Multiplatform 1.9.0 in September 2025, officially promoting the web target from Alpha to Beta. Version 1.10.0 followed in January 2026, adding Navigation 3 support and stable Compose Hot Reload (desktop only). The latest stable release as of March 2026 is **1.10.3**, with **1.11.0** in Beta; the web (Kotlin/Wasm) target remains Beta across the entire 1.10.x series. The official stability matrix as of March 2026:

| Platform | Core KMP | Compose Multiplatform |
|----------|----------|-----------------------|
| Android  | Stable   | Stable                |
| iOS      | Stable   | Stable (since 1.8.0, May 2025) [¹] |
| Desktop (JVM) | Stable | Stable              |
| Web (Kotlin/JS) | Stable | N/A (no Compose UI) |
| Web (Kotlin/Wasm) | Beta | Beta               |

[Source: https://kotlinlang.org/docs/multiplatform/supported-platforms.html, accessed 2026-03-30]

> [¹] iOS Stable status: ⚠️ version (1.8.0) and date (May 2025) unverified — derived from a single source (supported-platforms.html). Treat as approximate.

The Beta designation means: most essential APIs are available, adoption is encouraged for early adopters, breaking changes are possible but minimized, migration assistance is provided. It explicitly does NOT carry the backward-compatibility guarantees of Stable. JetBrains stated in August 2025 that they "expect pioneers to ship small- to medium-sized apps to production" with the Beta. [Source: https://blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/, accessed 2026-03-30]

**Browser support (as of late 2024/2025):** All major modern browsers — Chrome, Firefox, Safari, Edge — support WebAssembly Garbage Collection (WasmGC), which is the key prerequisite for Kotlin/Wasm. Safari adopted WasmGC in December 2024. A Kotlin/JS compatibility fallback mode was introduced in 1.9.3 via the `composeCompatibilityBrowserDistribution` Gradle task, which packages both Wasm and JS distributions together so that older browsers fall back to JS automatically.

[Source: https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/, accessed 2026-03-30]

**Known limitations as of early 2026:**
- Kotlin 2.2 required for native and web platforms (enforced in 1.10.0)
- TextField: still maturing (fixes ongoing through 1.10.0)
- Accessibility for container views with scrolls/sliders: not yet supported
- Traversal indexes: not yet supported on web
- No Compose Hot Reload for web targets
- Initial Wasm load time: ~5MB bundle download before first render
- International text rendering: non-Latin character sets require large font downloads

[Sources: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.0, accessed 2026-03-30]

**Confidence:** High — based on official JetBrains release notes and stability matrix.

### Kotlin/JS Target

**Status: Stable (core KMP), but Compose UI does NOT run on Kotlin/JS**

This is a critical distinction. "Kotlin/JS is Stable" refers to using Kotlin to write business logic that compiles to JavaScript for web — NOT to running Compose UI in the browser. Compose Multiplatform's UI framework on web requires Kotlin/Wasm; there is no Kotlin/JS rendering path for Compose UI.

The Kotlin/JS fallback introduced in 1.9.3 is specifically for the Wasm runtime itself — when WasmGC is not available in a browser, the JS fallback provides equivalent execution of the compiled app, not a separate code path. Both targets run identical Kotlin code; the difference is in the execution environment.

JetBrains stated in May 2025 that neither Kotlin/JS nor Kotlin/Wasm faces planned deprecation. Their strategy is to maintain both: "Kotlin/JS for sharing business logic with native UIs; Kotlin/Wasm for multiplatform UI sharing via Compose." [Source: https://blog.jetbrains.com/kotlin/2025/05/present-and-future-kotlin-for-web/, accessed 2026-03-30]

A developer first-impressions post noted that Kotlin/JS loads 0.25–0.5 seconds faster initially than Kotlin/Wasm due to the Wasm initialization overhead. [Source: https://medium.com/@ragnorak-dev/my-first-feelings-with-compose-multiplatform-for-web-js-kotlin-wasm-91de8022d093, accessed 2026-03-30]

**Confidence:** High — distinction is clearly documented in official sources.

---

## Feature Parity: Web vs iOS/Android

### What IS Shared (High Parity)

Compose Multiplatform for web in 1.9.0/1.10.0 ships with the following capabilities shared with mobile:

- Full Compose UI API: all standard composables (Text, Button, Column, Row, LazyColumn, etc.)
- Material 3 components and theming
- Animations and transitions
- Navigation (via Navigation 3, added in 1.10.0 — [Source: https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/, accessed 2026-03-30])
- State management (ViewModel, StateFlow, remember, collectAsState)
- Dark mode / system preference detection
- Shared business logic (ViewModel, repositories, use cases)
- Resource system (shared fonts, images, strings)
- Coroutines and Flow
- Deep linking via browser navigation binding

### What is NOT Available on Web

The following categories are absent or incomplete on the web target as of March 2026:

**Platform APIs (not available in shared code without `expect/actual`):**
- Camera and gallery access
- Device sensors (accelerometer, gyroscope, GPS/location)
- Biometric authentication
- Push notifications
- Background services / background execution
- Bluetooth, NFC
- File system access (beyond web's limited File API)
- Platform permissions model (Android `ActivityResultContracts`, iOS `Info.plist`)

Community libraries like `Calf` provide some cross-platform wrappers for camera, file picker, and permissions, but these delegate to platform-specific implementations — on web they use the browser's native APIs, which behave differently than mobile. [Source: https://github.com/MohamedRejeb/Calf, accessed 2026-03-30]

**Compose-level gaps on web specifically:**
- `Modifier.drag()` / drag-and-drop on mobile browsers: not fully implemented
- Accessibility for scrollable containers and sliders: not yet supported
- Traversal index ordering: not yet supported
- `BasicTextField` IME interactions: improving but not complete

**System UI integration:**
- Status bar, navigation bar control: not applicable on web
- System back gesture / predictive back: web equivalent exists (browser Back), partially wired
- In-app review, in-app purchase: not applicable

**Notable: no official JetBrains "compatibility matrix" document** was found that exhaustively lists supported vs unsupported APIs per platform. The closest official source is the "What's new" changelog series.

[Sources: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.0, accessed 2026-03-30]

**Confidence:** Medium — based on release notes and changelog analysis; no comprehensive matrix exists, so gaps may be underdocumented.

---

## Browser Automation Compatibility

### Canvas vs DOM Rendering

This is the most critical architectural fact for agent-based verification.

Compose for Web (Kotlin/Wasm) renders via **Skia-based canvas**, not native DOM elements. The entry point `CanvasBasedWindow` (now deprecated as of 1.9.x) rendered everything into a single `<canvas>` element. The replacement `ComposeViewport` also renders Compose UI into a canvas, but with important differences:

1. It uses `document.body` (or a specified container) as the viewport, not a named canvas ID
2. It supports `WebElementView()` — a new API to embed native HTML elements as overlays on top of the canvas
3. It enables accessibility support (disabled in `CanvasBasedWindow`)

The practical DOM structure of a Compose for Web app running via `ComposeViewport` is approximately:
- A canvas element occupying the viewport (all Compose UI painted here as pixels)
- Optionally, native HTML overlays from `WebElementView()` (iframes, inputs, etc.)
- An accessibility semantic tree (invisible DOM elements that mirror the canvas content for screen readers)

[Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

The consequence: **browser DevTools' Elements panel is essentially useless** for inspecting Compose UI. The canvas contains opaque pixel data; there are no button, input, or text DOM nodes corresponding to Compose composables. [Source: https://bitspittle.dev/blog/2024/c4w, accessed 2026-03-30 — ⚠️ pre-2025 source; verify CanvasBasedWindow deprecation claims against current 1.10.x documentation]

This is architecturally identical to Flutter Web with CanvasKit rendering, where "CanvasKit renders everything inside a canvas element. That means there's no traditional HTML DOM for test automation tools to interact with." [Source: https://www.getautonoma.com/blog/flutter-playwright-testing-guide, accessed 2026-03-30]

### Playwright Compatibility

Playwright **can** interact with Compose for Web apps, but requires the accessibility-tree approach, not DOM selectors.

**What does NOT work:**
- CSS selectors (`.button-class`, `#element-id`): no Compose UI elements have DOM nodes with these
- XPath: same issue
- `page.locator('button')`: no button elements exist in the DOM
- `page.locator('input')`: no input DOM nodes (unless using `WebElementView`)

**What DOES work (with accessibility enabled):**
- `page.getByRole('button', { name: 'Submit' })` — works if the button has `contentDescription` or text set in Compose semantics
- `page.getByText('Hello')` — may work if the accessibility tree exposes text content
- `page.getByLabel('Search')` — works if TextField has `contentDescription`

**Unconfirmed / needs empirical testing:**
- `page.getByTestId('my-tag')` — potentially works if `Modifier.testTag()` maps to a `data-testid` attribute in the accessibility DOM (this mapping is not explicitly confirmed in official docs as of March 2026; see Gap 5)

The accessibility overlay was introduced in 1.9.3 and is enabled by default. It can be configured:
```kotlin
ComposeViewport(
    viewportContainer = document.body!!,
    configure = { isA11YEnabled = true } // introduced and enabled by default in 1.9.3
) { ... }
```

**Critical limitation:** The accessibility support as of 1.9.3/1.10.x is described as "initial" and "basic." Screen readers can access description labels and button navigation, but:
- Accessibility for container views with scrolls/sliders is NOT yet supported
- Traversal indexes are NOT yet supported
- Complex nested component accessibility may be incomplete

This maps directly to Playwright automation gaps: any composable that lacks explicit `contentDescription` or `semantics {}` configuration will be invisible to Playwright's accessibility-tree locators.

[Sources: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, https://kotlinlang.org/docs/multiplatform/compose-accessibility.html, accessed 2026-03-30]

For comparison, the Flutter/Playwright community's established solution is: "Add `Semantics` widgets to all interactive elements. This makes them accessible to screen readers and to your tests." [Source: https://www.getautonoma.com/blog/flutter-playwright-testing-guide, accessed 2026-03-30] — the identical approach applies to Compose for Web.

### Accessibility/ARIA Support

**⚠️ Partial — basic implementation only as of March 2026.**

What is confirmed working in 1.9.3/1.10.x:
- Screen readers can access `contentDescription` labels
- Button roles are exposed (users can navigate and click buttons in accessible navigation mode)
- `Modifier.semantics { heading() }` and similar semantic annotations are honored
- `TextField` `contentDescription` now used as accessible name/label (was broken in earlier 1.9.x)
- Right-to-left text direction support added in 1.8.2

What is NOT yet working:
- Accessibility for interop views (scrollable containers, sliders)
- Traversal index ordering
- Full WCAG compliance (not claimed by JetBrains)
- Chrome Lighthouse auditing is "significantly less useful" against canvas rendering

For the technical mechanism of how the ARIA overlay is implemented, see the Canvas vs DOM Rendering section above. The key implication here: elements WITH semantics are queryable; elements WITHOUT explicit semantics are invisible to automation. An agent operating against a Compose Web app needs well-annotated composables.

[Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

**Confidence:** Medium — core mechanism confirmed, but exact Playwright behavior against Compose's specific accessibility DOM structure is not directly documented. The Flutter Web analogy is strong but not identical.

---

## Dev Server for Agent Workflows

### Running the Dev Server

The standard command to start a Compose for Web development server:

```bash
./gradlew wasmJsBrowserDevelopmentRun
```

This starts a webpack dev server at `http://localhost:8080/` (port may vary). The app opens automatically in the default browser. An agent can instead point a headless browser (Playwright) at this port.

For continuous file watching (pseudo-HMR):
```bash
./gradlew wasmJsBrowserDevelopmentRun --watch-fs -t
```

The `-t` flag triggers continuous build mode. However, this only reloads static assets and recompiles on save — it is **not** true Hot Reload. The page blinks/reloads but code changes require full Kotlin recompilation before taking effect. [Source: https://slack-chats.kotlinlang.org/t/27562635/, accessed 2026-03-30 — ⚠️ community Slack thread, not official documentation; link stability not guaranteed. Treat as community-reported behavior pending official confirmation.]

### Hot Reload Status

**Compose Hot Reload does NOT support web targets as of March 2026.**

Compose Hot Reload (the JetBrains tool that reloads UI changes without restart) requires a JVM target. The GitHub repository explicitly states: "Compose Hot Reload needs a JVM target in your multiplatform project." Plans to support other targets are described as exploratory with no committed timeline. [Source: https://github.com/JetBrains/compose-hot-reload, accessed 2026-03-30]

The Amper build tool added Compose Hot Reload in October 2025 with `js` and `wasmJs` platform support in module definitions, but "cannot currently run these with `./amper run` because it doesn't install any JavaScript runtime or browser." [Source: https://blog.jetbrains.com/amper/2025/10/amper-update-october-2025/, accessed 2026-03-30]

### Implications for Agent Workflows

For an LLM agent operating in a code-change-then-verify loop:

1. Agent makes code change
2. Agent triggers recompilation — two sub-cases:
   - **Watch mode (recommended):** `./gradlew wasmJsBrowserDevelopmentRun --watch-fs -t` is already running in the background; file-system changes trigger an automatic recompile without re-invoking Gradle.
   - **Single-shot restart:** Agent re-runs `./gradlew wasmJsBrowserDevelopmentRun` from scratch; slower due to full Gradle startup overhead.
3. Kotlin recompiles (takes 15–90 seconds depending on project size and incremental cache state)
4. Webpack dev server reloads the page
5. Agent navigates Playwright to the updated app

The recompilation latency is a significant workflow friction. There is no sub-second hot reload equivalent for the web target. This makes rapid iterative verification slower than desktop/JVM targets where Compose Hot Reload achieves near-instant updates.

**Headless operation:** Playwright's headless Chromium can connect to the dev server at `http://localhost:8080/` without any special configuration. Playwright ships a `--only-shell` install option for CI that downloads only the headless shell without the full browser binary. [Source: https://playwright.dev/docs/browsers, accessed 2026-03-30]

**Confidence:** Medium — dev server mechanics are well-documented; exact Playwright headless + Wasm compatibility in CI is not explicitly documented in official sources.

---

## Is Web a Viable Verification Proxy?

### Category Analysis

#### Category 1: Data-heavy apps (CRUD, forms, lists, state management)
**Viability: HIGH**

If the app primarily consists of forms, lists, detail views, and state-driven UI updates — and uses shared ViewModels / repositories — the Web target is an excellent proxy. The shared business logic layer runs identically. UI state transitions (loading → data → error) can be verified. Form validation logic is identical. Navigation between screens works via Navigation 3 (stable in 1.10.0).

An LLM agent can:
- Fill in form fields via accessibility-tree locators (if `contentDescription` is set)
- Click buttons by role/label
- Assert text content of results
- Verify navigation transitions

**Caveat:** Every interactive element needs explicit semantic annotation. Forms without `contentDescription` on TextFields will be invisible to Playwright.

#### Category 2: UI-heavy apps (animations, custom renderers, visual effects)
**Viability: MEDIUM — logic proxy only, not visual proxy**

The Compose UI API surface is shared, but visual rendering differences exist:
- Fonts render via Skia on web; native renderer on iOS/Android — pixel-level differences guaranteed
- Compose for Web performance characteristics differ from Skia-JVM or mobile
- Custom `Canvas {}` drawing code shares the same API but may have browser-specific rendering behavior
- Animations run via the same coroutines/clock API — logically correct, visually potentially different

An LLM agent can verify: state transitions, which composables are shown/hidden, text content. It cannot verify: exact pixel output, font rendering quality, smooth animation frame rates.

#### Category 3: Platform-API-heavy apps (camera, sensors, auth, notifications)
**Viability: LOW**

Apps that rely heavily on `expect/actual` platform APIs — camera capture, GPS, biometrics, push notifications, background processing — cannot be verified via the Web target. The web `actual` implementations either use browser APIs (different behavior from native), throw `NotImplementedError`, or are absent.

For example: a photo upload flow that uses `CameraX` on Android or `UIImagePickerController` on iOS has no equivalent web implementation in the standard library. Community libraries like `Calf` provide browser file picker as the web actual, which is a fundamentally different UX and capability.

**Agent strategy for this category:** Test only the shared business logic layers (ViewModel state, repository behavior) via unit tests, NOT via browser automation.

#### Category 4: Navigation and routing
**Viability: HIGH (as of 1.10.0)**

Navigation 3 support was added in 1.10.0 (January 2026) for non-Android targets including web. The `navController.bindToBrowserNavigation()` API provides browser back/forward button integration. An LLM agent can:
- Click buttons to navigate between screens
- Use browser back button (Esc key triggers back navigation on web as of 1.10.0)
- Verify URL changes via deep links
- Test navigation guards and conditional routing

[Source: https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.0, accessed 2026-03-30]

#### Category 5: Architecture verification (ViewModel, state, events)
**Viability: HIGH**

The highest-value proxy use case. The ViewModel and state management layer is identical across all platforms. An LLM agent can trigger UI events (button clicks, form submissions), observe state changes reflected in the UI, and verify error handling — all of which exercises the shared architecture.

### Real-World Usage as Verification Proxy

No blog posts, talks, or community discussions were found (as of March 2026) specifically describing a strategy of using Compose for Web as a CI verification proxy for iOS/Android behavior. The known production apps running on Compose for Web are: Kotlin Playground, KotlinConf app, and Rijksmuseum Demo — all from JetBrains or partners. [Source: https://www.kmpship.app/blog/kotlin-wasm-and-compose-web-2025, accessed 2026-03-30 — ⚠️ third-party community blog, not official JetBrains source]

The strategy is novel and not documented in community practice. However, the analogous Flutter Web → mobile proxy strategy IS discussed in the Flutter community, and the technical parallels are strong. The Flutter community's recommendation: use HTML renderer (or equivalent DOM-accessible rendering) for testing; rely on semantic annotations for automation. [Source: https://www.getautonoma.com/blog/flutter-playwright-testing-guide, accessed 2026-03-30]

**Confidence:** Medium — category analysis is based on synthesis of feature parity data; real-world proxy strategy has no confirmed practitioners in the Compose community.

---

## Gaps and Limitations

### Gap 1: Canvas rendering is the primary obstacle
All Compose for Web UI is painted into a Skia canvas. The browser DOM has no semantic structure by default. This is NOT a solvable problem via clever Playwright selectors — it requires the accessibility layer. Every composable that must be automation-queryable needs explicit `contentDescription` or `semantics {}` annotation. Apps written without accessibility in mind will be nearly opaque to Playwright.

### Gap 2: Accessibility coverage is "initial" and "basic"
As of March 2026, the accessibility implementation in Compose for Web is described by JetBrains as "initial." Known gaps include scrollable containers, sliders, and traversal ordering. An agent attempting to automate a complex scrollable list may fail silently.

### Gap 3: No hot reload for web
The development loop for web requires full Kotlin recompilation per change. Expect 15–90 second cycles depending on project size. This is a significant agent workflow friction compared to desktop targets.

### Gap 4: Beta stability means breaking changes are possible
Compose for Web is Beta, not Stable. APIs may change. Gradle tasks, entry point APIs, and accessibility configuration may shift between 1.9.x and whatever version precedes Stable. Agent tooling built against the current API should be designed to be version-pinned and easily updated.

### Gap 5: `testTag` → `data-testid` mapping is undocumented
It is unconfirmed whether `Modifier.testTag("my-tag")` in Compose for Web exposes a `data-testid` DOM attribute that Playwright can use via `getByTestId()`. This mapping exists in Flutter Web (explicit Semantics wrapper required). The Compose for Web documentation covers `testTag` for the Compose Test API (`./gradlew wasmJsTest`), not for browser-level Playwright selectors. This is a significant unknown that would need empirical verification.

### Gap 6: No Playwright-specific documentation or community examples
No official or community documentation was found specifically addressing Playwright + Compose for Web integration as of March 2026. All evidence for automation viability is derived from: (a) accessibility overlay documentation, (b) Flutter Web analogies, and (c) general Playwright accessibility-tree capabilities.

### Gap 7: 5MB initial load in dev/test environments
The ~5MB Wasm+Skia bundle must download before the app renders. In CI/test environments with slow networks, this may cause timeouts unless Playwright's `waitForLoadState('networkidle')` or equivalent is used. Local dev server mitigates this significantly.

---

## Sources

- [What's Next for KMP and CMP – August 2025 Update | JetBrains](https://blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/) — accessed 2026-03-30
- [Compose Multiplatform 1.9.0 Released: Web Goes Beta | JetBrains](https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/) — accessed 2026-03-30
- [Compose Multiplatform 1.10.0: Navigation 3, @Preview, Hot Reload | JetBrains](https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/) — accessed 2026-03-30
- [Present and Future of Kotlin for Web | JetBrains](https://blog.jetbrains.com/kotlin/2025/05/present-and-future-kotlin-for-web/) — accessed 2026-03-30
- [Stability of supported platforms | Kotlin Documentation](https://kotlinlang.org/docs/multiplatform/supported-platforms.html) — accessed 2026-03-30
- [What's new in Compose Multiplatform 1.9.3 | Kotlin Documentation](https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html) — accessed 2026-03-30
- [Accessibility | Kotlin Multiplatform Documentation](https://kotlinlang.org/docs/multiplatform/compose-accessibility.html) — accessed 2026-03-30
- [Testing Compose Multiplatform UI | Kotlin Documentation](https://kotlinlang.org/docs/multiplatform/compose-test.html) — accessed 2026-03-30
- [Get started with Kotlin/Wasm and Compose Multiplatform | Kotlin Documentation](https://kotlinlang.org/docs/wasm-get-started.html) — accessed 2026-03-30
- [Release 1.10.0 · JetBrains/compose-multiplatform | GitHub](https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.0) — accessed 2026-03-30
- [Compose Hot Reload | GitHub](https://github.com/JetBrains/compose-hot-reload) — accessed 2026-03-30
- [Compose Multiplatform for Web: An Amazing Framework That Maybe You Shouldn't Use | bitspittle.dev](https://bitspittle.dev/blog/2024/c4w) — **⚠️ Pre-2025 source — verify current status for CanvasBasedWindow deprecation claims** — accessed 2026-03-30
- [Kotlin/Wasm & Compose for Web in 2025: Complete Guide | kmpship.app](https://www.kmpship.app/blog/kotlin-wasm-and-compose-web-2025) — accessed 2026-03-30
- [Is Kotlin Multiplatform production ready in 2026? | kmpship.app](https://www.kmpship.app/blog/is-kotlin-multiplatform-production-ready-2026) — accessed 2026-03-30
- [Flutter Web Testing with Playwright Guide | Autonoma AI](https://www.getautonoma.com/blog/flutter-playwright-testing-guide) — accessed 2026-03-30 (Flutter analogy, not Compose-specific)
- [Amper Update, October 2025 – Compose Hot Reload | JetBrains Amper Blog](https://blog.jetbrains.com/amper/2025/10/amper-update-october-2025/) — accessed 2026-03-30
- [Calf — cross-platform adaptive UI and permissions library | GitHub](https://github.com/MohamedRejeb/Calf) — accessed 2026-03-30
- [Playwright — Browser installation docs](https://playwright.dev/docs/browsers) — accessed 2026-03-30
- [Kotlin Slack — wasmJsBrowserDevelopmentRun --watch-fs -t discussion](https://slack-chats.kotlinlang.org/t/27562635/) — accessed 2026-03-30 (**⚠️ Community/Slack source — link stability not guaranteed**)
- [My first feelings with Compose Multiplatform for Web | Medium/@ragnorak-dev](https://medium.com/@ragnorak-dev/my-first-feelings-with-compose-multiplatform-for-web-js-kotlin-wasm-91de8022d093) — accessed 2026-03-30
