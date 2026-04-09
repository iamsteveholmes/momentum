---
content_origin: agent-research
lens: A2
topic: LLM Doc Tooling and Sourcing
date: 2026-04-09
---

# Lens A2: Converting Technical Docs to LLM-Readable Format

## Question 1: Existing Open-Source Tools

### Tier 1 — Actively maintained, production-viable

**Context7** (github.com/upstash/context7)
- 52,100 stars, latest release April 9, 2026 — actively maintained
- MCP server: exposes `resolve-library-id` and `get-library-docs` tools pulling version-specific docs directly into LLM context
- Private crawling/parsing backend; frontend is open source
- Libraries submitted via GitHub URL at context7.com/add-library; `context7.json` config in repo root controls parsing behavior
- Kotlin listed in supported languages; Compose Multiplatform and Kotest NOT confirmed as indexed — cannot verify without live query
- **Most production-ready option for the "don't scrape yourself" path**

**microsoft/markitdown** (github.com/microsoft/markitdown)
- General-purpose file-to-markdown converter (PDFs, Office docs, HTML)
- Has MCP server mode; works for static content
- NOT designed for crawling doc sites — converts individual files, not doc trees

**supermemoryai/markdowner** (github.com/supermemoryai/markdowner)
- Cloudflare Browser rendering + Turndown for JS-heavy sites
- ~1,900 stars; last commit May 2024 — low maintenance activity
- API-based: `r.jina.ai/[url]` pattern for single-page conversion
- Handles JavaScript rendering; auto-crawling without sitemap

**amantus-ai/llm-codes** (github.com/amantus-ai/llm-codes)
- 313 stars; uses Firecrawl headless browser for JS-heavy docs
- Explicitly lists Kotlin as supported (69 total sites)
- Android and Compose NOT explicitly listed — coverage uncertain
- Converts rendered pages to clean LLM-optimized markdown

### Tier 2 — Functional but limited/stale

**alexfazio/devdocs-to-llm:** Jupyter notebook using Firecrawl; 102 stars; last commit August 2024. Starting-point recipe only.

**datalab-to/marker:** PDF/document-to-markdown with LLM-assisted cleanup. Only relevant for PDF sources.

**kolloldas/documentation-scraper:** Python scraper for developer.android.com; 3 stars; last commit 2017. Dead.

---

## Question 2: Kotlin Compose Multiplatform Documentation Sources

### THE KEY FINDING: JetBrains has already done the work

**kotlinlang.org/llms.txt — Verified working as of April 2026**
- Comprehensive feed covering core Kotlin, coroutines, collections, KMP, Compose Multiplatform, Gradle, Dokka, KSP, and all version release notes
- **Compose Multiplatform: 47 dedicated entries** under `https://kotlinlang.org/docs/multiplatform/_llms/{slug}.txt`
  - Covers: accessibility, adaptive layouts, Android-only components, compatibility/versioning, compiler, desktop components, drag-drop, hot reload, iOS/SwiftUI/UIKit integration, layout, lifecycle, localization, navigation, resources, viewmodel, web, and more
- **KMP: 80+ entries** at the same path pattern
- Individual page format: clean Markdown with H1/H2 headings, bullet lists, fenced Kotlin code blocks, cross-reference links
- **No Kotest entries** — Kotest is not covered in JetBrains' feed

**Why kotlinlang.org has such good coverage:** Built with JetBrains Writerside, which auto-generates both `llms.txt` and per-topic `_llms/*.txt` files on every deploy.

**Compose Multiplatform-specific llms.txt:** `https://kotlinlang.org/compose-multiplatform/llms.txt` returns 404. CMP docs are served through the main `kotlinlang.org/llms.txt` index.

### developer.android.com

- **No llms.txt** (404)
- robots.txt only disallows static assets and legacy SDK paths — documentation content paths NOT blocked
- JS-rendered SPA: content is invisible without a headless browser
- Sitemap available at `https://developer.android.com/sitemap.xml`
- Would require Firecrawl/Playwright for any content extraction

### JetBrains/compose-multiplatform GitHub

- Source code repo, not a doc repo
- Contains LLM-injectable API guidelines markdown:
  - `compose/docs/compose-api-guidelines.md`
  - `compose-component-api-guidelines.md`
- Not a substitute for reference docs but valuable for conventions

### Kotest

- No llms.txt (404 at kotest.io)
- Docs at `kotest.io/docs/` use standard hierarchical URL structure
- Not JS-heavy — a straightforward Firecrawl/markdowner pass should work
- No community-maintained LLM corpus found

---

## Question 3: Web Scraping vs. Official Feeds — Practical Tradeoffs

### developer.android.com scraping reality
- Requires JavaScript execution (SPA with empty HTML shell on raw fetch)
- Playwright/Puppeteer/Firecrawl required
- Sitemap at `https://developer.android.com/sitemap.xml` — use this for enumeration
- The `/reference` pages are highest-value; `/guide` pages also useful
- Rate limits: no explicit limit published; Google infrastructure will throttle aggressive crawling
- ToS risk for commercial use; low risk for internal agent tooling

### kotlinlang.org
- The llms.txt feed **eliminates the need to scrape** — use `_llms/*.txt` URLs directly
- Clean Markdown, no JS rendering required for the `_llms/` path
- This is the correct approach for Kotlin/KMP/CMP content

### Community-maintained corpora
- No verified community corpus found for Android/Kotlin/CMP in LLM-ready format as of April 2026
- Context7's private index may or may not include these libraries (cannot verify without live query)
- JetBrains KStack dataset exists but is a code corpus, not documentation

---

## Question 4: The llms.txt Ecosystem Tooling

**llms_txt2ctx** — Python CLI/library for parsing llms.txt and building context strings
**llmstxt-js** — JavaScript parser
**VitePress plugin** — auto-generates llms.txt from VitePress doc sites
**Docusaurus plugin** — same for Docusaurus (rachfop)

---

## Synthesis: Recommended Approach

| Source | Strategy | Effort |
|---|---|---|
| Kotlin/KMP/CMP | Use `kotlinlang.org/llms.txt` `_llms/*.txt` files directly | Zero — already LLM-ready |
| Kotest | Submit to Context7 OR Firecrawl pass on kotest.io/docs/ | Low |
| Android Jetpack (developer.android.com) | Context7 (if indexed) OR targeted sitemap + Firecrawl scrape | Medium |
| Any unlisted library | Context7 submission or Dokka processing from source | Medium |

**Context7 MCP is the most practical general solution** for libraries not covered by official feeds — de facto standard for on-demand doc injection as of April 2026.

---

## Key URLs
- https://github.com/upstash/context7
- https://kotlinlang.org/llms.txt
- https://llmstxt.org/
- https://www.jetbrains.com/help/writerside/generate-llms-txt.html
- https://github.com/amantus-ai/llm-codes
