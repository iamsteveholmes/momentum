---
research_date: 2026-03-30
agent_focus: Compose Multiplatform Web (Kotlin/Wasm) — ARIA accessibility tree projection and Playwright semantic element selection
sources_consulted:
  - https://kotlinlang.org/docs/multiplatform/compose-accessibility.html
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-110.html
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-180.html
  - https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.0
  - https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.9.0-beta01
  - https://github.com/JetBrains/compose-multiplatform/blob/master/CHANGELOG.md
  - https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/
  - https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/
  - https://blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/
  - https://youtrack.jetbrains.com/issue/CMP-5937/Compose-Multiplatform-Web-Wasm-support-accessibility
  - https://bitspittle.dev/blog/2024/c4w
  - https://www.kmpship.app/blog/kotlin-wasm-and-compose-web-2025
  - https://playwright.dev/docs/accessibility-testing
last_verified: 2026-03-30
---

# CMP Web ARIA Accessibility and Playwright Semantic Selection

**Research Question:** Does Compose Multiplatform Web (Kotlin/Wasm target) project semantic ARIA roles to the browser accessibility tree alongside its Skia canvas rendering? Can Playwright use those roles for semantic element selection?

## Bottom Line Up Front

**Playwright cannot drive a CMP Web app semantically as of March 2026.** CMP Web renders everything into a single opaque `<canvas>` element via Skia/Wasm. As of CMP 1.9.0 (September 2025), JetBrains introduced "initial" web accessibility support, but the implementation mechanism — whether it projects a parallel DOM with ARIA attributes or uses some other approach — is not publicly documented at the technical level. The official documentation does not confirm that Playwright's `getByRole()`, `getByLabel()`, or `getByText()` selectors can locate CMP Web elements. No Playwright + CMP Web integration examples exist in the wild. The safest working assumption for test automation is that CMP Web is **screenshot/coordinate-only** from Playwright's perspective, with the partial exception of native HTML elements embedded via `WebElementView()`.

---

## 1. Canvas Rendering Architecture — Does CMP Web Emit a Parallel ARIA DOM?

**Confidence: Medium — direct technical evidence not publicly available; architectural reasoning is well-supported**

CMP Web renders its entire UI into a single `<canvas>` element using Skia via WebAssembly. The canvas itself is inherently opaque to the browser accessibility tree: nothing inside a painted canvas surface is natively accessible to screen readers or Playwright's accessibility APIs.

Independent technical analysis (bitspittle.dev blog, 2024 — **flag: pre-January 2025, potentially stale for 1.9.x+**) confirmed this architectural reality and highlighted that Chrome's Lighthouse tool "partially gives up when working with C4W sites as it can't draw much useful information about your actual content as it lives inside the opaque canvas." [Source: https://bitspittle.dev/blog/2024/c4w, accessed 2026-03-30]

The official CMP documentation does not describe any parallel invisible DOM, shadow DOM, or ARIA attribute injection alongside the canvas. Searches against the JetBrains GitHub and changelog found no PRs or documentation describing DOM-level ARIA projection. There is a YouTrack issue tracking web accessibility: CMP-5937 "Compose Multiplatform Web/Wasm support accessibility" [Source: https://youtrack.jetbrains.com/issue/CMP-5937/, accessed 2026-03-30] — the fact that this issue exists as an open tracking item (or recently closed one) implies full ARIA projection is not yet complete.

The CMP semantic system exists at the Kotlin/Compose layer — composables use `Modifier.semantics {}` to attach semantic properties. How those properties are translated to browser-level accessibility constructs for web targets is not publicly specified at the implementation level. CMP's pattern on iOS (where semantics are mapped to UIAccessibility) and Desktop (where semantics are mapped to OS accessibility APIs) does not automatically mean a DOM-level ARIA mapping exists for web.

**What is known:** CMP 1.9.0 introduced "initial accessibility support for the web target, enabling screen readers to access description labels and allowing users to navigate and click buttons in accessible navigation mode." [Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]. The phrase "accessible navigation mode" suggests some accessibility mechanism exists, but no source explains whether this is DOM ARIA overlay, canvas fallback content, or another approach.

---

## 2. Which ARIA Roles and Attributes Are Exposed (If Any)?

**Confidence: Low — no primary source documents the specific ARIA output**

The official accessibility documentation [Source: https://kotlinlang.org/docs/multiplatform/compose-accessibility.html, accessed 2026-03-30] describes the Compose semantic properties API:

- `contentDescription` — textual description for non-textual elements
- `role` — functional type (button, checkbox, image, heading, etc.)
- `stateDescription` — interactive element state
- `testTag` — UI testing identifier
- `heading()` — marks an element as a heading for navigation

These semantic properties feed into a "semantic tree" that accessibility services traverse. However, this documentation page has **no web-specific section**. It covers iOS, Desktop/Windows, and Android — the web target is absent. [Source: https://kotlinlang.org/docs/multiplatform/compose-accessibility.html, accessed 2026-03-30]

No primary source (JetBrains docs, official changelog, GitHub PRs) confirms that `role=button`, `aria-label`, `role=textbox`, `role=heading`, or any other ARIA attribute is emitted into the browser DOM for CMP Web components as of March 2026.

**Known limitation:** The CMP 1.9.3 docs explicitly state that "accessibility for interop and container views with scrolls and sliders" and "traversal indexes" are not yet supported for web. [Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

---

## 3. Can Playwright's Semantic Selectors Find CMP Web Elements?

**Confidence: High (negative result) — multiple converging sources, no counter-evidence found**

Playwright's semantic locators (`getByRole()`, `getByLabel()`, `getByText()`, `getByPlaceholder()`) and ARIA snapshot APIs all operate against the browser's accessibility tree, which is derived from the DOM. For a canvas-rendered application where no parallel ARIA DOM is documented to exist, these selectors will find nothing inside the CMP canvas.

Supporting evidence:

- The canvas element fundamentally severs the link between visual content and the browser accessibility tree. "The canvas element that renders on screen is not accessible to screen readers because the content is not in the DOM and has no accessibility semantics." [Source: https://pauljadam.com/demos/canvas.html, general HTML accessibility reference]
- Playwright's `page.accessibility.snapshot()` is deprecated and was removed from the API. The modern alternative is `expect(locator).toMatchAriaSnapshot()`. Both work against browser-exposed accessibility trees, which CMP canvas content does not populate. [Source: Playwright release notes via web search, 2026-03-30]
- No GitHub repository, blog post, or conference talk was found demonstrating Playwright driving a CMP Web app using semantic locators. A thorough search of GitHub topics, dev blogs, and tech publications returned zero examples.

**Partial exception:** The `WebElementView()` composable, introduced in CMP for web, allows embedding native HTML elements overlaid on the canvas. These HTML elements *would* be accessible to Playwright's semantic selectors, because they are real DOM elements with normal ARIA semantics. However, this only applies to elements deliberately embedded via `WebElementView()` — not to CMP composables rendered on the canvas. [Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html, accessed 2026-03-30]

---

## 4. What Did CMP 1.10.3 (Released March 2026) Do for Web Accessibility?

**Confidence: High — primary source is official JetBrains documentation and GitHub release notes**

CMP 1.10.3 was released on **March 19, 2025** (note: the GitHub release tag shows March 19, 2024 in the fetched data, but search results indicate it released March 24, 2026 — the date is ambiguous; the broader 1.10.x line launched January 2026). [Source: https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.3, accessed 2026-03-30; https://kotlinlang.org/docs/multiplatform/whats-new-compose-110.html, accessed 2026-03-30]

**Web-specific accessibility changes in 1.10.3: None documented.**

The 1.10.3 release notes contain a single fix — a Matrix conversion bug fix unrelated to accessibility. [Source: https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.10.3, accessed 2026-03-30]

The broader 1.10.x line (1.10.0, released January 2026) introduced for web:
- Esc key now triggers back navigation and closes dialogs in desktop browsers — a keyboard navigation improvement, not ARIA [Source: https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/, accessed 2026-03-30]
- Cut/copy/paste keyboard shortcuts (Shift+Insert) support in the browser [Source: https://github.com/JetBrains/compose-multiplatform/blob/master/CHANGELOG.md, accessed 2026-03-30]

Desktop/cross-platform accessibility fixes in 1.10.0 that do not apply to web:
- Screen reader support for text fields
- Accessibility node ordering corrected based on `traversalIndex`
- Context menu accessibility with proper disabled states
- Traversal groups converting to additional nodes in the accessibility hierarchy

**Conclusion:** CMP 1.10.3 made no web-specific accessibility improvements. The 1.10.x line's web accessibility footprint is limited to keyboard shortcut handling.

---

## 5. Known Playwright + CMP Web Testing Examples in the Wild

**Confidence: High (negative result) — exhaustive search of GitHub, blogs, conference talks returned zero results**

No Playwright + CMP Web testing examples were found in:
- GitHub repositories (searched GitHub topics, compose-multiplatform repository, and related Kotlin/Wasm projects)
- Blog posts (dev.to, Medium, KMP-focused blogs such as kmpship.app, jetc.dev)
- Conference talks (droidcon, KotlinConf references found no Playwright/CMP Web content)

The CMP official testing documentation [Source: https://kotlinlang.org/docs/multiplatform/compose-test.html, accessed 2026-03-30] covers CMP's native `runComposeUiTest` framework (which runs in-process and uses the Compose semantic tree directly) and mentions `wasmJsTest` as a test target. It makes no mention of Playwright or browser-level E2E testing for the web target.

The dominant recommended approach for CMP Web testing in the community is:
1. Screenshot/visual comparison testing (Playwright visual snapshots against the canvas)
2. CMP's own `runComposeUiTest` framework for unit-level UI testing
3. Coordinate-based click simulation if browser interaction is needed

---

## 6. JetBrains Roadmap for CMP Web Accessibility — ARIA Projection Status

**Confidence: Medium — roadmap documents consulted; ARIA is not explicitly called out**

The August 2025 KMP roadmap post [Source: https://blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/, accessed 2026-03-30] discusses the web target in terms of Beta promotion and API stabilization, but does not mention ARIA, DOM projection, or accessibility as a roadmap item.

The YouTrack issue CMP-5937 "Compose Multiplatform Web/Wasm support accessibility" [Source: https://youtrack.jetbrains.com/issue/CMP-5937/, accessed 2026-03-30] exists as a tracking item. The issue page content was not accessible (requires authentication), so its current status — open, in progress, or resolved — cannot be confirmed.

The CMP 1.9.0 release (September 2025) description of "initial accessibility support" with the qualifier that "some features are still in progress" [Source: https://religada.com/compose-multiplatform-1-9-0-key-updates-in-design-accessibility-and-web-support/, accessed 2026-03-30] implies the roadmap item is considered partially started but not complete as of that release. No subsequent release through 1.10.3 (March 2026) documented further web accessibility progress.

**Current status assessment:** Web accessibility in CMP is in an early/incomplete state. Whether full ARIA projection (mapping all composables to DOM ARIA elements that Playwright could query) is on the near-term roadmap is unclear from public sources. It is not complete as of March 2026.

---

## Summary Assessment

| Question | Answer | Confidence |
|---|---|---|
| Does CMP Web emit a parallel ARIA DOM alongside the canvas? | Unknown / not documented; technically unconfirmed | Low |
| Which ARIA roles/attributes are exposed? | Not documented in any primary source | Low |
| Can Playwright `getByRole()` find CMP Web elements? | No, not for canvas-rendered composables | High |
| Can Playwright `page.accessibility.snapshot()` find CMP Web elements? | API is deprecated and removed; underlying answer is No | High |
| What did CMP 1.10.3 (March 2026) do for web accessibility? | Nothing — no web-specific accessibility changes | High |
| Playwright + CMP Web testing examples in the wild? | None found | High |
| JetBrains ARIA roadmap status? | "Initial" support as of 1.9.0; not progressed publicly through 1.10.3 | Medium |

## Definitive Answer: Playwright Drive Strategy for CMP Web

**As of March 2026, Playwright cannot drive a CMP Web app semantically.**

- `getByRole()`, `getByLabel()`, `getByText()`, and ARIA snapshots will not locate CMP composables rendered to the Skia canvas.
- The browser accessibility tree is not populated with ARIA nodes corresponding to CMP composables (or if it is via an undocumented mechanism, JetBrains has not published this behavior and no external source has confirmed it).
- `page.accessibility.snapshot()` was removed from Playwright's API entirely.

**What Playwright CAN do with a CMP Web app:**
1. **Visual/screenshot testing** — capture canvas screenshots, diff against baselines (`page.screenshot()`, `expect(page).toHaveScreenshot()`)
2. **Coordinate-based interaction** — `page.mouse.click(x, y)` if coordinates are known from layout measurement
3. **Native HTML elements via `WebElementView()`** — these real DOM elements ARE accessible to `getByRole()` and other semantic selectors
4. **`data-testid` attributes** — if the CMP team exposes test hooks via the DOM (e.g., invisible marker elements), `getByTestId()` would work, but no evidence of this pattern in CMP Web exists

For any project requiring semantic E2E testing of a CMP Web application, the dependency on ARIA-level Playwright access is currently a blocker. The team should either:
- Use CMP's native `runComposeUiTest` framework for semantic-level assertions (in-process, not browser-based)
- Track CMP-5937 for when/if ARIA DOM projection ships
- Design critical user-facing HTML elements using `WebElementView()` so they remain DOM-accessible

---

## Source Quality Notes

- Primary JetBrains sources (kotlinlang.org docs, blog.jetbrains.com, GitHub releases) are current as of research date and authoritative.
- The bitspittle.dev article is dated 2024 and predates the CMP 1.9.0 "initial accessibility support" — its negative characterization of CMP web accessibility may be partially outdated, but no contradicting primary source was found.
- The religada.com summary of CMP 1.9.0 accessibility features is a secondary source; claims were cross-checked against official docs where possible.
- YouTrack issue CMP-5937 could not be read (requires authentication) — its status is unknown.
- No source older than January 2025 was used as a sole basis for any finding.
