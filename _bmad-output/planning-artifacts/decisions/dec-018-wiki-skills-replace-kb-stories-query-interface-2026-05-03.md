---
id: DEC-018
title: Obsidian Wiki Skills Replace Planned KB Stories — wiki-query as Cold KB Interface
date: '2026-05-03'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-03'
prior_decisions_reviewed:
  - DEC-001 (Three-Tier Agent Guidelines — establishes Tier 3 cold KB and its access pattern)
  - DEC-009 (KB Vault Orchestration — kb-init, kb-ingest, index-first navigation)
  - DEC-015 (KB Cold-Context Delivery — injection points, prescriptive constitution triggers, skills audit)
architecture_decisions_affected:
  - DEC-001 D3 — Tier 3 access mechanism updated: was "grep index.md + targeted read", now wiki-query
  - DEC-015 D2 — workflow injection points should invoke wiki-query, not manual index navigation
  - DEC-015 D3 — constitution triggers should name wiki-query with exact syntax, not generic KB lookup language
  - DEC-015 Phase 1 — kb-init/kb-ingest superseded by wiki-setup/wiki-ingest from installed skill suite
stories_affected:
  - kb-init
  - kb-ingest
  - kb-raw-ingest-spike
  - build-guidelines-skill
  - constitutionmd-generation-acceptance-criteria
  - skills-kb-query-injection-audit
  - nornspun-agent-constitution
  - vault-claudemd-navigation-contract-spec
  - vault-indexmd-registry-format-and-update-protocol
  - wiki-page-schema-and-frontmatter-formalization
---

# DEC-018: Obsidian Wiki Skills Replace Planned KB Stories — wiki-query as Cold KB Interface

## Summary

Two related decisions resolve the implementation gap in the three-tier KB architecture. First: the installed Obsidian wiki skill suite (from `github.com/Ar9av/obsidian-wiki` and `github.com/kepano/obsidian-skills`) replaces all planned custom KB infrastructure stories — kb-init, kb-ingest, and related scaffolding. The installed skills are more capable than what was planned, with provenance tracking already built in. Second: `wiki-query` is adopted as the standard Tier 3 cold KB access interface, replacing the manual index-first navigation pattern from DEC-001. Critically, the wiki-query interface (both modes) belongs in the hot constitution (Tier 1) — not only in per-workflow injection points — so every agent everywhere has it in context without relying on workflow-specific wiring.

---

## Decisions

### D1: Replace planned KB-ingest, KB-init, and related stories with installed wiki-* skill suite — ADAPTED

**Developer framing:** The Momentum backlog contains stories to build custom KB initialization and ingestion tooling (kb-init, kb-ingest, kb-raw-ingest-spike, and related vault schema stories). A production-ready Obsidian wiki skill suite has been installed that covers this ground.

**Decision:** Adopt the replace direction, adapted to name the specific source packages:
- `wiki-setup`, `wiki-ingest`, `wiki-rebuild`, `wiki-status`, `wiki-lint`, `wiki-research`, `wiki-synthesize`, `wiki-export`, `wiki-dashboard`, `wiki-capture`, `wiki-update`, `wiki-history-ingest` from **`github.com/Ar9av/obsidian-wiki`**
- `obsidian-cli`, `obsidian-markdown`, `obsidian-bases` from **`github.com/kepano/obsidian-skills`**

Stories `kb-init`, `kb-ingest`, `kb-raw-ingest-spike`, `vault-claudemd-navigation-contract-spec`, `vault-indexmd-registry-format-and-update-protocol`, and `wiki-page-schema-and-frontmatter-formalization` are superseded. Drop or close them.

**Rationale:**
The installed skills are better than what was planned — provenance tracking (extracted/inferred/ambiguous markers) is already built in, the ingest pipeline handles multiple source types, and the full synthesis/lint/rebuild lifecycle is covered. No need to build it ourselves.

---

### D2: wiki-query as standard Tier 3 cold KB interface, documented in the hot constitution — ADAPTED

**Developer framing:** DEC-001 established Tier 3 access as "index-first navigation — grep index.md, read targeted page." DEC-015 required this to be baked into workflow steps and prescriptive constitution triggers. Neither named the specific mechanism. wiki-query is that mechanism. The adaptation: the interface documentation belongs in the constitution (Tier 1 hot context), not only in individual workflow injection points.

**Decision:** Adopt `wiki-query` as the standard Tier 3 cold KB interface, and place the interface specification in the hot constitution so every agent has it without relying on per-workflow wiring.

**Two modes, exact agent syntax:**

- **Normal mode** (tiered retrieval — index scan → section grep → full page read as needed, cited with `[[wikilinks]]`):
  ```
  wiki-query [your question]
  ```

- **Fast / index-only mode** (answers from page summaries and index.md only — no page bodies opened; cheaper, good for factual lookups):
  ```
  wiki-query quick answer: [your question]
  ```
  Also triggered by: "just scan:", "don't read the pages:", "fast lookup:"

DEC-015 D2 injection points (explicit KB query steps in workflows) should invoke wiki-query using this syntax. DEC-015 D3 constitution triggers should name the exact invocation form for each scenario — not "consult the KB if needed" but "run `wiki-query [specific question]` before proceeding."

**Rationale:**
wiki-query is more capable than simple grep — it was built specifically for this retrieval pattern. Placing the interface in the constitution ensures every agent everywhere has it in hot context. Agents that receive the constitution don't need a separately wired workflow step to know how to query the KB.

---

## Phased Implementation Plan

| Phase | Focus | Key Stories |
|-------|-------|-------------|
| 1 | Drop superseded stories | Close/drop kb-init, kb-ingest, kb-raw-ingest-spike and related vault schema stories |
| 2 | Constitution update | Add wiki-query interface block (both modes, exact syntax) to constitution.md — `build-guidelines-skill`, `constitutionmd-generation-acceptance-criteria` |
| 3 | Skills audit update | Update `skills-kb-query-injection-audit` to target wiki-query invocations, not manual grep steps |
| 4 | Agent constitution | `nornspun-agent-constitution` includes wiki-query interface as part of Tier 1 delivery |
