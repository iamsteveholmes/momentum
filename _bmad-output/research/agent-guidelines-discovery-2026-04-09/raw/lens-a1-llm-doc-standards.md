---
content_origin: agent-research
lens: A1
topic: LLM-Readable Documentation Standards
date: 2026-04-09
---

# Lens A1: LLM-Readable Documentation Standards

## The BMAD `llms-full.txt` File

**URL:** https://docs.bmad-method.org/llms-full.txt

A 2,826-line Markdown concatenation of the entire BMAD documentation site, generated 2026-04-08, labeled "Complete documentation for AI consumption." It is NOT a BMAD invention — it implements the llms.txt convention (see below).

**Structural conventions:**
- File header block: H1 title, blockquote summary with generation date and repo URL (canonical llms.txt format)
- Document concatenation: Each page wrapped in `<document path="relative/path.md">` XML-like tags (BMAD-specific, not part of spec)
- Full Markdown content preserved (tables, code fences, callout blocks, links, headings)
- No navigation chrome — clean prose and structured Markdown only

**Companion file:** `https://docs.bmad-method.org/llms.txt` — lightweight index (H1 + blockquote + H2 sections listing URLs with one-line descriptions), the standard "navigation index" variant.

**Is it a one-off?** No. BMAD follows the two-file pattern established across the industry.

---

## The `llms.txt` Proposal — Status April 2026

**Proposed by:** Jeremy Howard (co-founder of Answer.AI / fast.ai), published September 3, 2024.

**Canonical spec:** https://llmstxt.org/

**What it specifies:** A Markdown file at `/llms.txt` with:
1. H1 with project/site name (only required element)
2. Blockquote with short summary
3. Optional Markdown sections (no H2 headings) with extended background
4. Zero or more H2-delimited "file list" sections with `[name](url): optional notes` entries

**Companion pattern:** `llms-full.txt` is a community convention (not in spec) for serving full content. Two-file pattern is now standard.

**Formal status:** Not an RFC, not W3C Recommendation. Community proposal at https://github.com/AnswerDotAI/llms-txt. W3C strategy issue #506 exists but no formal track initiated.

**Adoption scale:** BuiltWith tracked 844,000+ websites implementing llms.txt as of October 2025. No major LLM provider has officially documented reading these files at crawl/inference time.

---

## Major Tech Company LLM-Readable Documentation

### JetBrains / Kotlin — VERIFIED

**kotlinlang.org/llms.txt:** Confirmed 200. 458 lines. Per-topic `.txt` files at `https://kotlinlang.org/docs/_llms/[topic].txt`. Every Kotlin doc page has an LLM-optimized text version.

Includes Compose-specific content: `compose-compiler-migration-guide.txt`, `compose-compiler-options.txt`, etc.

JetBrains separately publishes `.junie/guidelines.md` conventions for their Junie AI agent and maintains a community `junie-guidelines` repository with per-technology coding guidelines.

### Google Android / Firebase

- **developer.android.com:** 404 for `/llms.txt` and `/llms-full.txt`. Google has NOT published llms.txt for Android developer docs as of April 2026.
- **Firebase:** 404. No implementation.
- **Google ADK (adk.dev):** HAS full implementation. Auto-generates both `llms.txt` and `llms-full.txt`.

### Other Notable Adopters (verified 200 responses)

| Site | URL | Notes |
|---|---|---|
| Anthropic | https://docs.anthropic.com/llms.txt | Mintlify-generated; 8,364 tokens index / 481,349 token full |
| Stripe | https://stripe.com/llms.txt | H2-sectioned by product |
| Cloudflare | https://developers.cloudflare.com/llms.txt | 20+ products |
| Next.js | https://nextjs.org/llms.txt | Versioned docs |
| Expo | https://docs.expo.dev/llms.txt | Includes dedicated `/skills` page for AI agents |
| Supabase | https://supabase.com/llms.txt | Delegates to per-SDK files |
| React | https://react.dev/llms.txt | Confirmed 200 |
| Kotlin | https://kotlinlang.org/llms.txt | Per-topic `.txt` files |

### Not Yet Adopted (verified 404)
- `developer.android.com` — no llms.txt
- `developer.apple.com` — no llms.txt
- `developer.mozilla.org` — no llms.txt
- `firebase.google.com` — no llms.txt

---

## Community Standardization as of April 2026

**Documentation platform auto-generation:**
- Mintlify — zero-config, auto-regenerates on every deploy (first major platform)
- GitBook — added llms.txt (Jan 2025) then llms-full.txt + `.md` URL extension (Jun 2025)
- Fern — built-in support
- VitePress — via `vitepress-plugin-llms` community plugin
- Docusaurus — via `docusaurus-plugin-llms` plugin

**`.md` URL extension pattern:** GitBook, Next.js, and Stripe support appending `.md` to any documentation URL to get clean Markdown.

**AGENTS.md / CLAUDE.md Standard:**
- AGENTS.md donated to Agentic AI Foundation (AAIF, Linux Foundation) in December 2025
- Cross-tool convergence: Claude Code reads `CLAUDE.md`, Copilot reads `AGENTS.md`, Cursor reads `.cursorrules`, JetBrains Junie reads `.junie/guidelines.md`
- Canonical spec: https://agents.md/

---

## Synthesis

The industry has converged on TWO distinct complementary patterns:

**Pattern 1: llms.txt** — Library/framework documentation discovery for *external* docs (SDKs, frameworks, APIs). Mature enough that Kotlin, Expo, Next.js, Stripe, Cloudflare, Anthropic, Supabase all publish it.

**Pattern 2: AGENTS.md / CLAUDE.md** — Project-specific agent instructions for *project-specific* conventions. AGENTS.md is the cross-tool standard as of late 2025.

**What you do NOT need to create from scratch:** Framework reference documentation. Kotlin, Expo, Next.js, Supabase all publish authoritative, maintained, LLM-optimized docs. The work is curation, not authoring.

---

## Key URLs
- https://llmstxt.org/ — canonical spec
- https://github.com/AnswerDotAI/llms-txt — spec repository
- https://github.com/thedaviddias/llms-txt-hub — aggregator directory
- https://kotlinlang.org/llms.txt — JetBrains/Kotlin live implementation
- https://agents.md/ — AGENTS.md cross-tool standard
