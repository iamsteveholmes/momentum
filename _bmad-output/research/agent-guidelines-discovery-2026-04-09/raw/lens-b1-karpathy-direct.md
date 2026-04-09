---
content_origin: agent-research
lens: B1
topic: Karpathy LLM Wiki Gist — Direct Analysis
date: 2026-04-09
source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
---

# Lens B1: Karpathy's "LLM Wiki" Gist — Direct Analysis

**Source:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
**Title:** "LLM Wiki — A pattern for building personal knowledge bases using LLMs"

---

## 1. Core Thesis

Direct attack on RAG as the dominant paradigm:

> "Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation."

His alternative: the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files.

> "The wiki is a persistent, compounding artifact. The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read."

**The problem he solves:** The accumulation problem. In standard RAG, knowledge doesn't compound. Every query starts from zero.

He frames the model as programmer: "The LLM makes edits based on our conversation, and I browse the results in real time. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

---

## 2. Structural Recommendations

**File format:** Plain markdown files. No database, no embeddings infrastructure at small-to-moderate scale.

**Three-layer architecture:**
- **Raw sources** — immutable, never modified by the LLM. Source of truth.
- **The wiki** — LLM-generated and LLM-maintained markdown files: summaries, entity pages, concept pages, comparisons, synthesis.
- **The schema** — a configuration document (CLAUDE.md or AGENTS.md equivalent) defining wiki structure, conventions, and workflows.

On the schema:
> "This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot."

**Index/manifest:** A dedicated `index.md` — a catalog of all wiki pages with links, one-line summaries, and optional metadata. Organized by category (entities, concepts, sources, etc.).

**Log file:** A separate `log.md` for chronological audit trail with parseable prefixes:
> "if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools"

**Header/anchor conventions:** Not explicitly prescribed. He says: "The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain."

---

## 3. Size and Scope Guidance

Scale reference: index-first approach "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure."

A single source ingest "might touch 10-15 wiki pages." This implies fine-grained, concept-level pages — not monolithic documents.

Individual pages are focused enough to be LLM-readable in one pass — but he doesn't quantify token limits.

---

## 4. Retrieval Recommendations

**Manifest-first retrieval:**
> "When answering a query, the LLM reads the index first to find relevant pages, then drills into them."

Grep/keyword-compatible — no embeddings required. For scale beyond "hundreds of pages," he recommends adding `qmd` (BM25/vector hybrid with LLM re-ranking, CLI + MCP server) — but defers this until actually needed.

**Filing answers back:**
> "good answers can be filed back into the wiki as new pages. A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do."

---

## 5. Pre-processing / "Compile-Time" Reasoning

Karpathy doesn't use the phrase "sleep time compute." However, the entire architecture is structurally a pre-processing model.

The wiki is the pre-processed artifact. At ingest time, LLM does the expensive work: reading sources, extracting key information, integrating into existing pages, flagging contradictions, updating cross-references. At query time, LLM reads structured, pre-synthesized content rather than raw sources.

He frames this as compilation:
> "The knowledge is compiled once and then kept current, not re-derived on every query."

**Lint operation** — a periodic health-check pass: checking for contradictions, stale claims, orphan pages, missing cross-references. Pre-processing in ongoing maintenance mode.

---

## 6. Direct Applicability to Agent Guidelines

The schema/CLAUDE.md layer is the direct analog.

For Kotlin Compose API patterns specifically:

**What RAG gives you:** Agent searches raw docs at query time, may or may not surface deprecation of `AnimatedVisibleContent`, has to rediscover the relationship every time.

**What the wiki model gives you:** A pre-compiled wiki page for "Animation — Compose 1.7" that already states: "Use `AnimatedVisibility`. `AnimatedVisibleContent` was deprecated in 1.6; do not use it. See also: `AnimatedContent`, `Crossfade`." The agent reads the index, finds the relevant page, reads a synthesized summary. No re-derivation.

**The three-layer model maps:**
- Raw sources = upstream library docs, changelogs, API references
- The wiki = synthesized, LLM-maintained guidelines pages
- The schema = CLAUDE.md defining how the agent navigates and applies guidelines

---

## 7. Surprising or Counterintuitive Claims

**RAG is not good enough, even though it dominates.** Critique isn't that RAG doesn't work but that it doesn't compound.

**The LLM should own and write the knowledge base entirely.** "You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it." Roles inverted: human as curator/questioner, LLM as sole maintainer of the structured artifact.

**Index-first beats embedding-based search at moderate scale.** Claims text-based index with one-line summaries "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)" — challenges assumption that you need vector search infrastructure.

**Answers should be filed back.** Treating query answers as first-class knowledge artifacts that belong in the wiki.

**The bottleneck is maintenance, not reading.** "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping." LLMs eliminate that cost asymmetry.

---

## Claims Requiring Independent Verification

- "~100 sources, ~hundreds of pages" as effective ceiling for index-only navigation — based on personal use, not systematic evaluation
- `qmd` recommendation — specific third-party tool, maturity unverified
- Implicit claim that LLM-generated cross-referencing at ingest time is reliable enough to trust — the gist does not discuss validation

---

## Summary for Agent Guidelines Design

**The most actionable takeaway:** The knowledge delivery format should be pre-synthesized, not raw. Store as a maintained wiki where "use X not Y" decisions are already baked in, organized for index-first navigation. The agent reads the index, identifies relevant pages, reads synthesized content — never re-derives the convention from raw material.
