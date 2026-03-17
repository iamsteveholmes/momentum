# Bidirectional Document Reference Formats for AI-Generated Specification Chains

**Date:** 2026-03-14
**Type:** Technical Research
**Status:** Complete

## Executive Summary

This report enumerates and evaluates all known approaches to bidirectional document referencing in markdown-based specification chains. The use case is an agentic engineering workflow where AI agents produce a chain of specifications (Research → Brief → PRD → Architecture → Epics → Stories → Implementation), and each document must cite its upstream sources while upstream documents must know what downstream documents reference them.

Six categories of approaches were investigated: (1) markdown citation/footnote standards, (2) document metadata standards, (3) knowledge graph/bidirectional linking tools, (4) specification cross-reference standards, (5) LLM-optimized citation formats, and (6) sidecar metadata patterns. The findings converge on a recommended hybrid approach combining YAML frontmatter for bidirectional metadata, Pandoc-style inline citations for granular references, and a sidecar registry for cross-document graph integrity.

---

## 1. Markdown Citation and Footnote Standards

### 1.1 Standard Markdown Footnotes

**Confidence:** HIGH

Standard markdown extended syntax supports footnotes using `[^identifier]` markers with corresponding definitions:

```markdown
This requirement derives from the stakeholder interview[^1].

[^1]: See Brief §3.2, "User needs analysis"
```

Named footnotes use descriptive identifiers rather than numbers:

```markdown
The authentication flow[^auth-flow] must complete within 200ms[^perf-req].

[^auth-flow]: Architecture Doc, Section 4.1 "Authentication Service"
[^perf-req]: PRD §2.3, NFR-007
```

Multi-line footnotes support complex references:

```markdown
[^complex]: This derives from multiple sources:
    - Brief §2.1 "Market Analysis"
    - Research Doc, Finding R-003
    - [External benchmark](https://example.com)
```

**Pros for our use case:**
- Universally supported in GitHub, GitLab, Jekyll, Hugo, MkDocs, and most markdown renderers
- Numbered automatically in output regardless of identifier naming
- Support backlinking (rendered footnotes link back to their reference point)
- Human-readable in raw markdown

**Cons for our use case:**
- Unidirectional only — the cited document has no knowledge of being cited
- No structured metadata — footnote content is free text, not machine-parseable
- No support for section-level granularity in the reference target
- No standardized way to express document IDs or section IDs

**Sources:**
- [Markdown Extended Syntax — Footnotes](https://www.markdownguide.org/extended-syntax/)
- [Advanced Markdown Footnotes and Reference Links Guide](https://blog.markdowntools.com/posts/markdown-advanced-footnotes-and-reference-links-guide)
- [GitHub Changelog: Footnotes in Markdown](https://github.blog/changelog/2021-09-30-footnotes-now-supported-in-markdown-fields/)

### 1.2 Pandoc Citeproc Citation Syntax

**Confidence:** HIGH

Pandoc's citation processor (citeproc) provides the most mature academic citation system for markdown. Citations use `@key` syntax with optional locators:

```markdown
---
bibliography: references.bib
csl: custom-style.csl
---

The authentication requirement [@PRD-2026, sec. 4.1] derives from
stakeholder interviews [@Brief-2026, pp. 12-15]. As noted by
@Architecture-2026 [chap. 3], the service boundary...

Suppressed author for parenthetical: [-@PRD-2026, sec. 2.3]

Multiple sources: [see @Brief-2026, sec. 2; also @Research-2026, finding R-003]
```

**Locator terms supported:** page/p./pp., chapter/chap., section/sec., volume/vol., figure/fig., paragraph/para., plus folio, line, verse, note, opus, and others.

**Inline bibliography via YAML frontmatter** (no external .bib file needed):

```yaml
---
references:
  - id: PRD-2026
    type: document
    title: "Product Requirements Document"
    author:
      - literal: "Agent: Claude"
    issued:
      date-parts:
        - [2026, 3, 10]
    URL: "./prd-auth-service.md"
  - id: Brief-2026
    type: document
    title: "Authentication Service Brief"
    URL: "./brief-auth-service.md"
---
```

**Pros for our use case:**
- Richest inline citation syntax available in markdown
- Section-level granularity via locators (sec., chap., §)
- Machine-parseable — structured bibliography in YAML or BibTeX
- Well-documented, actively maintained, very widely adopted in academia
- CSL (Citation Style Language) supports 10,000+ citation styles

**Cons for our use case:**
- Still unidirectional — cited documents do not know they are cited
- Requires Pandoc toolchain for rendering (raw markdown shows `@key` syntax which is not universally rendered)
- Overkill academic metadata model (authors, publishers, dates) for internal spec chains
- No native bidirectional linking support

**Sources:**
- [Pandoc Citation Syntax](https://pandoc.org/demo/example33/8.20-citation-syntax.html)
- [Pandoc User's Guide — Citations](https://pandoc.org/MANUAL.html)
- [Specifying Bibliographic Data](https://pandoc.org/demo/example33/9.1-specifying-bibliographic-data.html)

---

## 2. Document Metadata Standards

### 2.1 YAML Frontmatter Conventions

**Confidence:** HIGH

YAML frontmatter is the dominant metadata format for markdown documents, originally popularized by Jekyll and now supported by Hugo, Gatsby, Docusaurus, Obsidian, MkDocs, Pandoc, GitHub Pages, and virtually all modern static site generators and documentation tools.

Standard structure:

```yaml
---
title: "Authentication Service PRD"
id: PRD-AUTH-001
version: 1.2
date: 2026-03-10
status: approved
---
```

There is no formal standard for document-relationship metadata in YAML frontmatter. However, several tools have established conventions:

**Grafana's Writer's Toolkit** uses a `refs` field for reference definitions:
```yaml
---
refs:
  find-plugins:
    - pattern: /docs/grafana/
      destination: /docs/grafana-cloud/
---
```

**Zettlr** supports Pandoc-compatible frontmatter for bibliography references and allows arbitrary metadata keys.

**Sources:**
- [GitHub Docs: Using YAML Frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)
- [Hugo Front Matter](https://gohugo.io/content-management/front-matter/)
- [Grafana Writers' Toolkit — Front Matter](https://grafana.com/docs/writers-toolkit/write/front-matter/)
- [Zettlr YAML Front Matter](https://docs.zettlr.com/en/editor/yaml-frontmatter/)

### 2.2 Dublin Core Metadata in Markdown

**Confidence:** MEDIUM

Dublin Core provides 15 standardized metadata elements. The `dcterms:isPartOf`, `dcterms:references`, and `dcterms:relation` elements are directly relevant to document linking. A proposal exists for embedding Dublin Core in MultiMarkdown:

```markdown
Title: Authentication Service PRD
Date: 2026-03-10
Modified: 2026-03-12
Type: Specification
Author: Agent: Claude
Relation: brief-auth-service.md
IsPartOf: epic-auth-001
```

Dublin Core relationship properties include:
- `dcterms:references` — the described resource references the cited resource
- `dcterms:isReferencedBy` — the inverse (bidirectional pair)
- `dcterms:isPartOf` / `dcterms:hasPart` — containment hierarchy
- `dcterms:requires` / `dcterms:isRequiredBy` — dependency relationships
- `dcterms:isVersionOf` / `dcterms:hasVersion` — versioning
- `dcterms:source` — the resource from which this one is derived

**Pros for our use case:**
- Well-established vocabulary with precise semantics
- Bidirectional relationship pairs built into the standard
- Machine-parseable with defined semantics
- Internationally standardized (ISO 15836)

**Cons for our use case:**
- Not natively supported by any markdown renderer
- Verbose for simple spec chains
- Relationship granularity is document-level, not section-level
- MultiMarkdown metadata format differs from standard YAML frontmatter

**Sources:**
- [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- [Dublin Core Metadata Basics](https://www.dublincore.org/resources/metadata-basics/)
- [Embedding Dublin Core in MultiMarkdown](https://networkcultures.org/digitalpublishing/2013/10/09/embedding-a-custom-set-of-metadata-based-on-dublin-core-into-a-multimarkdown-document/)

### 2.3 JSON-LD for Document Linking

**Confidence:** MEDIUM

JSON-LD (JavaScript Object Notation for Linked Data) encodes linked data using JSON, with `@context`, `@id`, and `@type` directives for semantic linking. It could be embedded in YAML frontmatter or in a sidecar file:

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "@id": "PRD-AUTH-001",
  "name": "Authentication Service PRD",
  "isBasedOn": {
    "@id": "BRIEF-AUTH-001",
    "@type": "TechArticle",
    "name": "Authentication Service Brief"
  },
  "hasPart": [
    {"@id": "EPIC-AUTH-001"},
    {"@id": "EPIC-AUTH-002"}
  ]
}
```

**Pros for our use case:**
- Rich semantic vocabulary via Schema.org
- Bidirectional relationships expressible (`isBasedOn`/`isBasisFor`)
- Machine-parseable with well-defined semantics
- Web standard (W3C Recommendation)

**Cons for our use case:**
- Verbose and heavyweight for markdown spec chains
- Not renderable in markdown — would need to live in frontmatter or sidecar
- Primarily designed for web content, not document management
- Overkill unless integrating with external knowledge systems

**Sources:**
- [JSON-LD Official Site](https://json-ld.org/)
- [JSON-LD Wikipedia](https://en.wikipedia.org/wiki/JSON-LD)
- [Google Structured Data Introduction](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)

---

## 3. Knowledge Graph and Bidirectional Linking Approaches

### 3.1 Obsidian Wikilinks and Backlinks

**Confidence:** HIGH

Obsidian implements bidirectional linking through wikilinks (`[[]]`) with a metadata cache that tracks all link relationships:

**Link types:**

| Reference Type | Syntax | Example | Granularity |
|---|---|---|---|
| File link | `[[filename]]` | `[[PRD-Auth]]` | Document |
| Heading link | `[[file#heading]]` | `[[PRD-Auth#NFRs]]` | Section |
| Block link | `[[file#^blockid]]` | `[[PRD-Auth#^req-007]]` | Paragraph |
| Alias link | `[[file\|display]]` | `[[PRD-Auth\|the PRD]]` | Document |

**Backlinks system:** Obsidian's metadata cache automatically tracks:
- **Linked mentions**: Files containing explicit `[[current note]]` links
- **Unlinked mentions**: Text occurrences of note names not yet linked

**Aliases in frontmatter:**
```yaml
---
aliases:
  - PRD
  - Auth PRD
  - Authentication Requirements
---
```

**Pros for our use case:**
- Section and block-level granularity out of the box
- Automatic backlink detection (bidirectional without explicit reverse links)
- Human-readable in raw markdown (though `[[]]` is not standard markdown)
- Metadata cache enables fast graph queries

**Cons for our use case:**
- `[[wikilink]]` syntax is non-standard markdown — breaks in GitHub, most renderers
- Backlinks are computed at runtime, not stored in document metadata
- No structured relationship types (all links are generic "references")
- Requires Obsidian or compatible tooling for backlink resolution

**Sources:**
- [Obsidian Internal Links and Backlinks — DeepWiki](https://deepwiki.com/obsidianmd/obsidian-help/4.2-internal-links-and-backlinks)
- [Obsidian Backlinks Guide](https://devgodz.com/blog/obsidian-backlinks-your-guide-to-effortless-linking-1764804357)
- [Obsidian Complete Guide 2025](https://smartscope.blog/en/obsidian-complete-guide/)

### 3.2 Roam Research Block References

**Confidence:** MEDIUM

Roam Research treats every block (paragraph/bullet) as a uniquely addressable unit with its own ID. Block references use `(())` syntax:

- Page links: `[[Page Name]]` or `#PageName`
- Block references: `((block-uid))` — embeds the referenced block's content
- Bidirectional: All links automatically generate backlinks with context

**Key insight:** Every block has a unique ID, and block references create *transclusions* — the referenced content appears inline and stays synchronized if the source changes.

**Pros for our use case:**
- Finest-grained referencing (individual paragraphs/bullets)
- Automatic bidirectionality with context preservation
- Content transclusion eliminates duplication

**Cons for our use case:**
- Proprietary syntax, not markdown-compatible
- Requires Roam Research platform
- Block UIDs are opaque (not human-readable)
- No typed relationships

**Sources:**
- [Bi-directional Linked Notes & Blocks in Roam Research](https://eightify.app/summary/productivity-and-personal-development/bi-directional-linked-notes-blocks-in-roam-research)
- [Organizing Notes in Roam](https://www.zsolt.blog/2021/02/organizing-your-notes-in-roam.html)

### 3.3 Notion Relations and Backlinks

**Confidence:** HIGH

Notion provides two distinct bidirectional linking mechanisms:

**Database Relations:** Structured, typed connections between database records. When a relation is created, Notion automatically generates a mirror relation in the target database. Relations can be toggled between one-way and two-way.

**Page Backlinks:** Using `[[page name]]` syntax, Notion creates automatic backlinks displayed under the target page's title. Unlike relations, backlinks are unstructured mentions.

**Pros for our use case:**
- Relations provide typed, structured connections
- Automatic bidirectionality
- Rollup properties aggregate data across relations

**Cons for our use case:**
- Notion-proprietary, not portable to markdown files
- Requires Notion platform
- Not version-controllable in git

**Sources:**
- [Notion Explained: Relations & Rollups](https://www.notion.vip/insights/notion-explained-relations-rollups)
- [Notion Backlinks — Ness Labs](https://nesslabs.com/notion-backlinks)
- [Notion Relations & Rollups Help](https://www.notion.com/help/relations-and-rollups)

### 3.4 Zettelkasten Principles (Platform-Agnostic)

**Confidence:** HIGH

The Zettelkasten method provides foundational principles applicable to any implementation:

1. **Atomic notes**: Each document contains one idea/unit (maps to: each spec is a single deliverable)
2. **Unique identifiers**: Every note has a permanent address (maps to: document IDs like `PRD-AUTH-001`)
3. **Explicit links with context**: Links include WHY the connection exists, not just THAT it exists
4. **Bidirectional discovery**: Following links in either direction reveals the knowledge structure
5. **Folgezettel (sequence)**: Notes have hierarchical IDs indicating their position in thought sequences (e.g., `1a1b2`)

**Relevance to our use case:** The Zettelkasten ID scheme (`1`, `1a`, `1a1`) maps naturally to a specification hierarchy: `SPEC-001` (Research) → `SPEC-001a` (Brief derived from it) → `SPEC-001a1` (PRD derived from Brief).

**Sources:**
- [Zettelkasten Method for Developers: Digital Implementation](https://dasroot.net/posts/2026/01/zettelkasten-method-developers-digital-implementation/)
- [Zettelkasten Method Guide 2026 — Atlas Blog](https://www.atlasworkspace.ai/blog/zettelkasten-method-guide)
- [The Case for a Digital Folgezettel](https://forum.zettelkasten.de/discussion/976/the-case-for-a-digital-folgezettel)

---

## 4. Specification Cross-Reference Standards

### 4.1 DITA xref and olink

**Confidence:** HIGH

DITA (Darwin Information Typing Architecture) provides two cross-reference mechanisms:

**xref (within a document set):**
```xml
<xref href="prd-auth.dita#requirements/nfr-007" type="requirement">
  NFR-007: Authentication latency
</xref>
```

Key attributes:
- `href` — direct URI-based addressing (creates dependency on target existence)
- `keyref` — key-based addressing (indirection via key maps, enables context-dependent resolution)
- `xreflabel` — consistent reference text across all references to a target
- `xrefstyle` — template-based text generation (`template:`, `select:`)

**olink (across document boundaries):**
```xml
<olink targetdoc="architecture-doc" targetptr="auth-service-section">
  See Architecture §4.1
</olink>
```

**Pros for our use case:**
- Mature, standardized (OASIS)
- Section-level and element-level granularity
- Key-based indirection allows context-dependent resolution
- Cross-document linking via olink

**Cons for our use case:**
- XML-based, not markdown
- Heavy toolchain requirement
- Overly complex for our use case
- Still fundamentally unidirectional (target doesn't know about references)

**Sources:**
- [DITA xref specification](https://www.oxygenxml.com/dita/1.3/specs/langRef/base/xref.html)
- [DITA xref — OASIS](https://docs.oasis-open.org/dita/v1.2/os/spec/langref/xref.html)
- [DITA Cross References — I'd Rather Be Writing](https://idratherbewriting.com/cross_references/)
- [DocBook Olinking Between Documents](https://sagehill.net/docbookxsl/Olinking.html)

### 4.2 DocBook xref and olink

**Confidence:** HIGH

DocBook's cross-reference system is similar to DITA but with different syntax:

**xref (in-document):**
```xml
<xref linkend="auth-requirements"/>  <!-- auto-generates reference text -->
<xref linkend="nfr-007" endterm="nfr-007-title"/>  <!-- uses endterm's text -->
```

**olink (cross-document):**
```xml
<olink targetdoc="architecture" targetptr="auth-service">
  Authentication Service Architecture
</olink>
```

DocBook distinguishes between `xref` (cross-reference, text auto-generated) and `link` (hyperlink, text explicitly provided). The `xreflabel` attribute provides consistent reference text.

**Sources:**
- [DocBook xref — The Definitive Guide](https://tdg.docbook.org/tdg/5.0/xref.html)
- [DocBook Cross References](https://www.sagehill.net/docbookxsl/CrossRefs.html)
- [DocBook Olinking](https://sagehill.net/docbookxsl/Olinking.html)

### 4.3 OpenAPI $ref Pattern

**Confidence:** HIGH

OpenAPI/JSON Schema uses `$ref` for structured cross-references with JSON Pointer addressing:

```yaml
# Internal reference
$ref: "#/components/schemas/AuthRequest"

# Cross-file reference
$ref: "./auth-schemas.yaml#/AuthRequest"

# External reference
$ref: "https://api.example.com/schemas/auth.yaml"
```

**Key patterns:**
- References use JSON Pointer notation (`#/path/to/element`)
- Supports relative file paths and absolute URLs
- Override capability: `$ref` plus `summary`/`description` for context
- Circular references allowed for recursive structures

**Pros for our use case:**
- Clean, well-understood syntax for structured references
- Cross-file references with path + fragment
- Machine-parseable

**Cons for our use case:**
- Designed for schema composition, not document citation
- Unidirectional
- JSON/YAML only, no inline markdown syntax

**Sources:**
- [OpenAPI $ref Best Practices — Speakeasy](https://www.speakeasy.com/openapi/references)
- [How to Use JSON References — Redocly](https://redocly.com/learn/openapi/ref-guide)
- [Using $ref — Swagger](https://swagger.io/docs/specification/v3_0/using-ref/)

### 4.4 RFC Cross-Reference Format

**Confidence:** HIGH

IETF RFCs use bracketed reference notation with standardized identifiers:

```
See Section 3.2 of [RFC2119] for the definition of key words.
This document updates [BCP14] (comprising [RFC2119] and [RFC8174]).
```

References section format:
```
[RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
           Requirement Levels", BCP 14, RFC 2119,
           DOI 10.17487/RFC2119, March 1997,
           <https://www.rfc-editor.org/info/rfc2119>.
```

Cross-references by section number are preferred over page number. Sub-series documents (STD, BCP) group multiple RFCs under a single citation tag.

**Pros for our use case:**
- Simple, proven format used for decades
- Section-level granularity via "Section X of [REF]"
- Human-readable, grep-friendly

**Cons for our use case:**
- Unidirectional
- No machine-parseable structure (free text)
- No bidirectional metadata

**Sources:**
- [RFC Style Guide](https://www.ietf.org/archive/id/draft-flanagan-7322bis-07.html)
- [RFC Format Framework (RFC 7990)](https://datatracker.ietf.org/doc/html/rfc7990)

### 4.5 Crossref DOI Relationship Model

**Confidence:** HIGH

Crossref provides a comprehensive relationship vocabulary for scholarly documents, with **automatic bidirectional linking**:

When one DOI claims a relationship, the system automatically creates the reverse without requiring the target's metadata to contain it. Relationship types include:

**Inter-work relationships:**
- `references` / `isReferencedBy`
- `isBasedOn` / `isBasisFor`
- `isPartOf` / `hasPart`
- `isSupplementTo` / `isSupplementedBy`
- `documents` / `isDocumentedBy`
- `requires` / `isRequiredBy`
- `continues` / `isContinuedBy`
- `reviews` / `isReviewedBy`

```xml
<program xmlns="http://www.crossref.org/relations.xsd">
  <related_item>
    <inter_work_relation relationship-type="isBasedOn"
      identifier-type="doi">10.1234/brief-auth-001</inter_work_relation>
  </related_item>
</program>
```

**Key insight:** The "claimant" model — only one side needs to declare the relationship, and the system infers the reverse — is directly applicable to our use case. A downstream spec declares "I am based on X," and X automatically gains a "referenced by" entry.

**Sources:**
- [Crossref Relationships Documentation](https://www.crossref.org/documentation/schema-library/markup-guide-metadata-segments/relationships/)
- [Crossref Reference Linking](https://www.crossref.org/documentation/reference-linking/)
- [Relationships Between DOIs — Crossref Support](https://support.crossref.org/hc/en-us/articles/214357426-Relationships-between-DOIs-and-other-objects)

### 4.6 Requirements Traceability Matrix (RTM) Patterns

**Confidence:** HIGH

Requirements traceability is defined as "the ability to describe and follow the life of a requirement in both a forwards and backwards direction." Standard RTM implementations use a cross-reference table linking:

1. Requirements → Stakeholders (origin)
2. Requirements → Design specifications
3. Design → Code segments
4. Requirements → Test plans
5. Parent requirements → Child requirements

**Doorstop** (text-based RTM tool) stores each item as a YAML file with explicit links:
```bash
doorstop link HLTC001 SRD002  # links test case to requirement
```
Items form a tree hierarchy based on directory structure.

**SARA** (markdown-based requirements traceability) is the most directly relevant tool found. It uses YAML frontmatter with typed relationships:

```yaml
---
id: "SYSREQ-001"
type: system_requirement
name: "Authentication Response Time"
derives_from:
  - "SCENARIO-003"
satisfies:
  - "ARCH-007"
---
```

SARA supports relationship types: `derives_from`/`derives`, `satisfies`/`is_satisfied_by`, `depends_on`/`is_required_by`, `refines`/`is_refined_by`.

**Critical feature:** "You only need to define relationships in one direction. SARA will automatically infer the reverse links." This mirrors the Crossref claimant model.

SARA recognizes a document hierarchy: Solution → Use Case → Scenario → System Requirement → Architecture → Hardware/Software Requirements → Detailed Designs.

Validation via `sara validate` checks for broken references, orphaned items, and circular dependencies.

**Sources:**
- [SARA: A CLI Tool for Managing Markdown Requirements](https://dev.to/tumf/sara-a-cli-tool-for-managing-markdown-requirements-with-knowledge-graphs-nco)
- [Doorstop — Requirements Management Using Version Control](https://github.com/doorstop-dev/doorstop)
- [Requirements Traceability — Wikipedia](https://en.wikipedia.org/wiki/Requirements_traceability)
- [SARA on Hacker News](https://news.ycombinator.com/item?id=46752826)

### 4.7 MyST Markdown Cross-References

**Confidence:** HIGH

MyST (Markedly Structured Text) extends markdown with powerful cross-referencing:

**Syntax variants:**
```markdown
@target                          # shorthand auto-reference
[text](#target)                  # markdown link to label
[](#target)                      # auto-fill with title/number
[Sec. %s](#target)               # custom text with number placeholder
{ref}`target`                    # role-based reference
{ref}`custom text <target>`      # role with custom text
{numref}`Table %s <my-table>`    # numbered reference
{doc}`./other-file.md`           # document reference
```

**Labels on elements:**
```markdown
(my-section)=
## Section Title

:::{figure} image.png
:label: my-fig
:::
```

**Cross-project references via `xref:` protocol:**
```markdown
[Admonition](xref:spec#admonition)
```

**Frontmatter numbering control:**
```yaml
---
numbering:
  heading_1: true
  heading_2: true
  figure:
    continue: true
---
```

**Pros for our use case:**
- Rich, granular cross-referencing in markdown
- Cross-project linking via `xref:` protocol
- Labels on any element type (headings, figures, blocks)
- Standard markdown link syntax `[text](#target)` works alongside extended syntax

**Cons for our use case:**
- Requires MyST toolchain for rendering
- Still unidirectional — no automatic backlink generation
- MyST-specific extensions (`{ref}`, `{numref}`) not portable

**Sources:**
- [MyST Markdown — Cross-references Guide](https://mystmd.org/guide/cross-references)
- [MyST Markdown — References & Links Spec](https://mystmd.org/spec/references)
- [MyST Cross Reference Simplifications MEP](https://mep.mystmd.org/mep-0002/)

### 4.8 Hugo ref/relref Shortcodes

**Confidence:** HIGH

Hugo provides `ref` and `relref` shortcodes for cross-file markdown references:

```markdown
[Authentication Architecture]({{< relref "architecture-auth.md" >}})
[Specific Section]({{< relref "architecture-auth.md#service-boundaries" >}})
[Same-file anchor]({{< relref "#performance-requirements" >}})
```

Hugo auto-generates heading anchors and validates that reference targets exist at build time.

**Pros:** Build-time validation, cross-file support, heading-level granularity.
**Cons:** Hugo-specific, unidirectional, no metadata about relationships.

**Sources:**
- [Hugo Links and Cross References](https://gohugobrasil.netlify.app/content-management/cross-references/)

---

## 5. LLM-Optimized Citation Formats

### 5.1 Anthropic Claude Citations API

**Confidence:** HIGH

Claude's Citations API (released January 2025) provides structured, inline citations in API responses. When documents are provided with `citations.enabled: true`, the response interleaves text blocks with citation objects:

```json
{
  "content": [
    {"type": "text", "text": "According to the document, "},
    {
      "type": "text",
      "text": "the authentication flow must complete within 200ms",
      "citations": [
        {
          "type": "char_location",
          "cited_text": "Authentication flow must complete within 200ms.",
          "document_index": 0,
          "document_title": "PRD Auth Service",
          "start_char_index": 450,
          "end_char_index": 498
        }
      ]
    }
  ]
}
```

**Citation location types:**
- `char_location` — character index range (plain text documents, 0-indexed)
- `page_location` — page number range (PDF documents, 1-indexed)
- `content_block_location` — block index range (custom content documents, 0-indexed)

**Key design decisions:**
- `cited_text` is extracted, not generated — guaranteed accurate
- `cited_text` does not count toward output tokens (cost saving)
- Citations and Structured Outputs are mutually exclusive (cannot use both)
- Documents can be plain text, PDF, or custom-chunked content

**Relevance to our use case:** This API format demonstrates how an LLM naturally produces citations. Our reference format should be compatible with — or at least convertible to/from — this structure so that agent-generated specs can include provenance metadata automatically.

**Sources:**
- [Claude Citations API Documentation](https://platform.claude.com/docs/en/build-with-claude/citations)
- [Anthropic's new Citations API — Simon Willison](https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/)

### 5.2 RAG Citation Anchor Patterns

**Confidence:** MEDIUM

The citation-aware RAG approach embeds lightweight citation markers in text with spatial metadata stored separately:

**Inline anchor format:**
```
SMOTE creates a broader decision region <c>2.1</c>
CDSMOTE handles class imbalance <c>2.2</c>
```

**Associated metadata:**
```json
{
  "citations": {
    "2.1": {
      "page": 23,
      "bbox": {"x1": 12, "y1": 15, "x2": 149, "y2": 328}
    }
  }
}
```

**LLM output format with citations:**
```json
{
  "answer": "CDSMOTE reduces class imbalance by clustering...",
  "citations": ["2.1"]
}
```

The anchor notation uses `<c>[page_num].[reading_order]</c>` — compact, parseable, and separates citation metadata from content.

**Sources:**
- [Citation-Aware RAG — Tensorlake](https://www.tensorlake.ai/blog/rag-citations)

### 5.3 XML-Tagged Inline Citations for LLM Prompts

**Confidence:** MEDIUM

A pattern for getting LLMs to produce inline citations uses XML tags as boundary markers:

```markdown
Paul Graham suggests that <CIT chunk_id='2' sentences='1-2'>choosing work
should be based on curiosity</CIT>.
```

The tags include `chunk_id` and `sentences` attributes for granular source mapping. Post-processing extracts the tags and builds citation metadata.

A more general pattern uses document-level XML tagging:
```xml
<document>
  <document_content>Full text here...</document_content>
  <source>PRD-AUTH-001, Section 4.1</source>
</document>
```

**Pros for our use case:**
- XML tags are parseable by both LLMs and simple regex
- Attributes provide structured metadata inline
- Compatible with markdown (XML in markdown is valid)
- Can be stripped for clean rendering

**Cons for our use case:**
- Non-standard — no widely adopted specification
- Visual noise in raw markdown
- Fragile if LLMs don't consistently produce the tags

**Sources:**
- [Anthropic-Style Citations with Any LLM](https://medium.com/data-science-collective/anthropic-style-citations-with-any-llm-2c061671ddd5)
- [Use XML Tags to Structure Prompts — Claude Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)
- [AI Generated In-Text Citations — Exhaustively Explained](https://iaee.substack.com/p/ai-generated-in-text-citations-intuitively)

### 5.4 Structured Output for Specification Agents

**Confidence:** MEDIUM

Addy Osmani's research on AI agent specifications (published on O'Reilly) identifies key patterns for how agents consume and produce specifications:

- Specs use `.spec.md` files as "implementation-ready blueprints"
- A four-phase workflow: Specify → Plan → Tasks → Implement
- Hierarchical summarization: an "extended Table of Contents with summaries" that condenses sections into key points while referencing where full details exist
- Modular context management: provide only relevant spec portions to avoid "context overload"

**Relevance:** Agents work best with structured, labeled sections that have stable identifiers. Our reference format should use heading-level anchors and section IDs that agents can reliably target.

**Sources:**
- [How to Write a Good Spec for AI Agents — Addy Osmani](https://addyosmani.com/blog/good-spec/)
- [How to Write a Good Spec for AI Agents — O'Reilly](https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/)

---

## 6. Sidecar Metadata Files

### 6.1 Sidecar File Pattern

**Confidence:** HIGH

A sidecar file stores metadata alongside a primary file, with the same base name but different extension. This is a well-established pattern across photography (XMP), video editing, and digital asset management.

**Naming convention:** `document.md` → `document.meta.yml` or `document.xmp`

**Common formats:** XMP (XML), JSON, YAML, CSV

**Key properties:**
- Non-destructive: original file remains unchanged
- Same-name association: relationship is implicit via filename
- Format-independent: metadata schema is separate from content format

**Sources:**
- [Sidecar File — Wikipedia](https://en.wikipedia.org/wiki/Sidecar_file)
- [Sidecar Files in DAM](https://www.orangelogic.com/sidecar-in-digital-asset-management)
- [ExifTool Metadata Sidecar Files](https://exiftool.org/metafiles.html)

### 6.2 Sidematter Format Convention

**Confidence:** MEDIUM

The Sidematter format (by Josh Levy) defines a minimal convention for sidecar metadata and assets alongside any document:

**File naming:**
- `document.md` → `document.meta.yml` or `document.meta.json`
- Asset directory: `document.assets/`

**Metadata example:**
```yaml
title: Q3 Financial Analysis
author: Jane Doe
created_at: 2024-01-15
tags:
  - finance
  - quarterly
processing_history:
  - step: data_extraction
    timestamp: 2024-01-15T10:30:00Z
    tool: custom_extractor_v2.1
```

**Rules:**
- Only final extension is removed for sidecar naming (`data.tar.gz` → `data.tar.meta.yml`)
- JSON takes precedence when both JSON and YAML metadata exist
- Asset directory structure is free-form
- Validated schemas use a `$schema` key

**Pros for our use case:**
- Keeps documents clean — metadata doesn't clutter markdown content
- Git-friendly — metadata changes are separate commits from content changes
- Flexible schema — can store relationship data, processing history, anything
- Convention-based — no tooling required to understand the pattern

**Cons for our use case:**
- Two files per document adds complexity
- Metadata can drift out of sync with content
- No standard schema for relationships
- Less discoverable than inline metadata

**Sources:**
- [Sidematter Format — GitHub](https://github.com/jlevy/sidematter-format)

---

## 7. Comparison Matrix

| Approach | Bidirectional | Granularity | Markdown-Native | LLM-Parseable | Section-Level | Typed Relations | Tooling Required |
|---|---|---|---|---|---|---|---|
| **Markdown footnotes** | No | Document | Yes | Medium | No | No | None |
| **Pandoc citeproc** | No | Section (via locators) | Partial | High | Yes | No | Pandoc |
| **YAML frontmatter** | Manual (both sides) | Document | Yes | High | No | Custom | None |
| **Dublin Core** | Vocabulary exists | Document | No | High | No | Yes (standard) | Custom |
| **JSON-LD** | Vocabulary exists | Document | No | High | No | Yes (Schema.org) | Custom |
| **Obsidian wikilinks** | Yes (runtime) | Block | No | Medium | Yes | No | Obsidian |
| **Roam block refs** | Yes (runtime) | Block | No | Low | Yes | No | Roam |
| **Notion relations** | Yes (stored) | Document | No | Low | No | Yes | Notion |
| **DITA xref/olink** | No | Element | No | High | Yes | No | DITA toolchain |
| **DocBook xref/olink** | No | Element | No | High | Yes | No | DocBook toolchain |
| **OpenAPI $ref** | No | Element | No | High | Yes | No | OpenAPI tools |
| **RFC references** | No | Section | Yes (plain text) | Medium | Yes | No | None |
| **Crossref DOI** | Yes (claimant) | Document | No | High | No | Yes (rich) | Crossref |
| **SARA (RTM)** | Yes (inferred) | Document | Yes | High | No | Yes | SARA CLI |
| **MyST markdown** | No | Element | Partial | High | Yes | No | MyST toolchain |
| **Hugo relref** | No | Section | No (shortcodes) | Low | Yes | No | Hugo |
| **Claude Citations API** | No | Character/page/block | No (API) | Native | Yes | No | Claude API |
| **RAG citation anchors** | No | Sentence | Partial (XML tags) | High | Yes | No | Custom |
| **Sidecar YAML/JSON** | Manual (both sides) | Custom | Yes (separate file) | High | Custom | Custom | None |
| **Sidematter format** | Manual (both sides) | Custom | Yes (separate file) | High | Custom | Custom | None |

---

## 8. Synthesis and Recommendations

### 8.1 Requirements Recap

Our format must:
1. Allow inline references in downstream docs pointing to specific sections in upstream docs
2. Include metadata in upstream docs listing downstream references
3. Work in standard markdown (renderable on GitHub)
4. Be parseable by both humans AND LLMs
5. Support section-level granularity

### 8.2 Key Insights from Research

1. **No single existing format meets all five requirements.** Every approach excels at some criteria and fails others.

2. **The "claimant" model is the right bidirectional pattern.** Both Crossref and SARA demonstrate that the downstream document should declare its upstream sources, and a build/validation tool should infer the reverse links. Requiring both sides to manually maintain references is error-prone and will drift.

3. **YAML frontmatter is the best metadata container.** It is universally supported, machine-parseable, human-readable, and git-diff-friendly.

4. **Pandoc-style inline citations provide the best granular reference syntax** that works in markdown and is parseable by LLMs. The `[@DOC-ID, sec. X.Y]` format is concise, human-readable, and machine-extractable.

5. **LLMs (especially Claude) can reliably produce structured citations** when given the right format constraints. The Claude Citations API demonstrates that models can ground claims to specific source locations.

6. **SARA is the closest existing tool to what we need**, but it operates at document level only (no section-level inline references) and uses its own hierarchy model.

### 8.3 Recommended Hybrid Format

The recommended format combines three layers:

#### Layer 1: YAML Frontmatter (Document-Level Metadata)

Every specification document includes a standardized frontmatter block:

```yaml
---
id: PRD-AUTH-001
type: prd
title: "Authentication Service PRD"
version: 1.0
date: 2026-03-10
status: draft
# Upstream sources this document derives from
derives_from:
  - doc: BRIEF-AUTH-001
    type: brief
    sections: ["3.1", "3.2", "4.1"]
  - doc: RESEARCH-AUTH-001
    type: research
    sections: ["findings.F-003", "findings.F-007"]
# Downstream documents that reference this one (auto-populated by tooling)
referenced_by:
  - doc: ARCH-AUTH-001
    type: architecture
    sections_cited: ["2.1", "2.3", "4.1"]
  - doc: EPIC-AUTH-001
    type: epic
    sections_cited: ["3.1"]
---
```

#### Layer 2: Inline Citations (Section-Level Granularity)

Within the document body, use a Pandoc-compatible citation syntax adapted for our spec chain:

```markdown
## 2.1 Authentication Requirements

The system must support OAuth 2.0 and SAML 2.0 protocols
[source: BRIEF-AUTH-001 §3.2]. Response time must not exceed 200ms
for token validation [source: RESEARCH-AUTH-001 §F-003, BRIEF-AUTH-001 §4.1].

### 2.1.1 Token Validation

As established in the authentication research [source: RESEARCH-AUTH-001 §F-007],
JWT validation is preferred over opaque tokens due to reduced database load.
```

The `[source: DOC-ID §SECTION]` format is:
- Human-readable in raw markdown
- Machine-parseable via regex: `\[source:\s*([A-Z]+-[A-Z]+-\d+)\s*§([^\]]+)\]`
- Renderable as-is (appears as bracketed text) without special tooling
- Compatible with multiple citations: `[source: DOC-A §1.2, DOC-B §3.4]`

#### Layer 3: Reference Registry (Sidecar or Centralized)

A `_references.yml` file at the project root maintains the complete reference graph:

```yaml
# _references.yml — auto-generated, do not edit manually
documents:
  RESEARCH-AUTH-001:
    path: docs/research/auth-research.md
    type: research
    referenced_by:
      BRIEF-AUTH-001:
        sections_cited: ["findings.F-003", "findings.F-007"]
      PRD-AUTH-001:
        sections_cited: ["findings.F-003", "findings.F-007"]

  BRIEF-AUTH-001:
    path: docs/briefs/auth-brief.md
    type: brief
    derives_from:
      RESEARCH-AUTH-001:
        sections_used: ["findings.F-003", "findings.F-007"]
    referenced_by:
      PRD-AUTH-001:
        sections_cited: ["3.1", "3.2", "4.1"]
      ARCH-AUTH-001:
        sections_cited: ["3.2", "4.1"]

  PRD-AUTH-001:
    path: docs/specs/auth-prd.md
    type: prd
    derives_from:
      BRIEF-AUTH-001:
        sections_used: ["3.1", "3.2", "4.1"]
      RESEARCH-AUTH-001:
        sections_used: ["findings.F-003", "findings.F-007"]
    referenced_by:
      ARCH-AUTH-001:
        sections_cited: ["2.1", "2.3", "4.1"]
      EPIC-AUTH-001:
        sections_cited: ["3.1"]
```

### 8.4 Tooling Integration

The three-layer format supports progressive automation:

1. **Manual baseline**: Authors write `derives_from` in frontmatter and `[source: ...]` inline. This works with zero tooling.

2. **Validation**: A script (analogous to `sara validate`) parses all documents, extracts inline citations via regex, and validates that:
   - All referenced document IDs exist
   - All referenced sections exist in the target document
   - `derives_from` in frontmatter is consistent with inline citations
   - No orphaned documents exist in the chain

3. **Auto-population**: A script generates/updates `referenced_by` fields in upstream documents and regenerates `_references.yml`. Only `derives_from` and inline `[source: ...]` citations are authoritative; everything else is derived.

4. **Agent integration**: When an AI agent generates a specification, it:
   - Reads upstream documents
   - Populates `derives_from` in frontmatter
   - Includes `[source: DOC-ID §SECTION]` inline citations (grounded by the Claude Citations API or equivalent)
   - A post-generation hook runs validation and auto-populates reverse references

### 8.5 Why This Hybrid Over Alternatives

| Decision | Rationale |
|---|---|
| YAML frontmatter over sidecar files | One file per spec, git-friendly, universally supported |
| `[source: ...]` over `[@key]` | Renders on GitHub without Pandoc, more explicit about meaning |
| `[source: ...]` over `[[wikilinks]]` | Standard markdown, no Obsidian dependency |
| Centralized `_references.yml` over per-doc `referenced_by` only | Single source of truth for graph, cheaper to query |
| Claimant model over dual-entry | Only downstream docs need to cite sources; reverse links are auto-generated |
| Section notation with `§` | Human-readable, grep-friendly, unambiguous separator |
| Document IDs like `PRD-AUTH-001` | Unique, type-encoded, sortable, Zettelkasten-compatible |

---

## 9. Open Questions for Implementation

1. **Section ID format**: Should section references use heading numbers (`§3.2`), anchor slugs (`§authentication-requirements`), or custom IDs (`§REQ-007`)? Heading numbers are fragile to reordering; slugs are fragile to renaming; custom IDs require maintenance.

2. **Transclusion**: Should downstream documents be able to *embed* upstream content (like Roam block references), or only *reference* it? Transclusion reduces duplication but creates rendering complexity.

3. **Version pinning**: Should references point to a specific version of an upstream document, or always to the latest? Version pinning prevents drift but requires version management.

4. **Validation strictness**: Should broken references be warnings or errors? In a CI pipeline, errors block merges; warnings may be ignored.

5. **Graph visualization**: Should `_references.yml` support generating a visual dependency graph (like Obsidian's graph view or Zettelkasten visualizations)?

---

## Sources Index

### Markdown Citation/Footnote Standards
- [Markdown Extended Syntax — Footnotes](https://www.markdownguide.org/extended-syntax/)
- [Advanced Markdown Footnotes Guide](https://blog.markdowntools.com/posts/markdown-advanced-footnotes-and-reference-links-guide)
- [GitHub Footnotes Changelog](https://github.blog/changelog/2021-09-30-footnotes-now-supported-in-markdown-fields/)
- [Pandoc Citation Syntax](https://pandoc.org/demo/example33/8.20-citation-syntax.html)
- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [Pandoc Bibliographic Data](https://pandoc.org/demo/example33/9.1-specifying-bibliographic-data.html)
- [Markdown Citations Guide — MarkdownTools](https://blog.markdowntools.com/posts/markdown-citations-and-references-guide)

### Document Metadata Standards
- [GitHub Docs — YAML Frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)
- [Hugo Front Matter](https://gohugo.io/content-management/front-matter/)
- [Grafana Writers' Toolkit — Front Matter](https://grafana.com/docs/writers-toolkit/write/front-matter/)
- [Zettlr YAML Front Matter](https://docs.zettlr.com/en/editor/yaml-frontmatter/)
- [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- [Dublin Core Metadata Basics](https://www.dublincore.org/resources/metadata-basics/)
- [Dublin Core in MultiMarkdown](https://networkcultures.org/digitalpublishing/2013/10/09/embedding-a-custom-set-of-metadata-based-on-dublin-core-into-a-multimarkdown-document/)
- [JSON-LD Official Site](https://json-ld.org/)
- [JSON-LD Wikipedia](https://en.wikipedia.org/wiki/JSON-LD)
- [Google Structured Data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)

### Knowledge Graph / Bidirectional Linking
- [Obsidian Internal Links — DeepWiki](https://deepwiki.com/obsidianmd/obsidian-help/4.2-internal-links-and-backlinks)
- [Obsidian Backlinks Guide](https://devgodz.com/blog/obsidian-backlinks-your-guide-to-effortless-linking-1764804357)
- [Obsidian Complete Guide 2025](https://smartscope.blog/en/obsidian-complete-guide/)
- [Roam Research Bidirectional Links](https://eightify.app/summary/productivity-and-personal-development/bi-directional-linked-notes-blocks-in-roam-research)
- [Roam Notes Organization](https://www.zsolt.blog/2021/02/organizing-your-notes-in-roam.html)
- [Notion Relations & Rollups](https://www.notion.vip/insights/notion-explained-relations-rollups)
- [Notion Backlinks — Ness Labs](https://nesslabs.com/notion-backlinks)
- [Notion Help — Relations](https://www.notion.com/help/relations-and-rollups)
- [Zettelkasten for Developers 2026](https://dasroot.net/posts/2026/01/zettelkasten-method-developers-digital-implementation/)
- [Zettelkasten Guide 2026 — Atlas](https://www.atlasworkspace.ai/blog/zettelkasten-method-guide)
- [Digital Folgezettel Discussion](https://forum.zettelkasten.de/discussion/976/the-case-for-a-digital-folgezettel)

### Specification Cross-Reference Standards
- [DITA xref — OASIS](https://docs.oasis-open.org/dita/v1.2/os/spec/langref/xref.html)
- [DITA xref — Oxygen XML](https://www.oxygenxml.com/dita/1.3/specs/langRef/base/xref.html)
- [DITA Cross References — I'd Rather Be Writing](https://idratherbewriting.com/cross_references/)
- [DocBook xref — Definitive Guide](https://tdg.docbook.org/tdg/5.0/xref.html)
- [DocBook Cross References](https://www.sagehill.net/docbookxsl/CrossRefs.html)
- [DocBook Olinking](https://sagehill.net/docbookxsl/Olinking.html)
- [OpenAPI $ref — Speakeasy](https://www.speakeasy.com/openapi/references)
- [JSON References — Redocly](https://redocly.com/learn/openapi/ref-guide)
- [Using $ref — Swagger](https://swagger.io/docs/specification/v3_0/using-ref/)
- [RFC Style Guide](https://www.ietf.org/archive/id/draft-flanagan-7322bis-07.html)
- [RFC Format Framework](https://datatracker.ietf.org/doc/html/rfc7990)
- [Crossref Relationships](https://www.crossref.org/documentation/schema-library/markup-guide-metadata-segments/relationships/)
- [Crossref Reference Linking](https://www.crossref.org/documentation/reference-linking/)
- [Crossref DOI Relationships](https://support.crossref.org/hc/en-us/articles/214357426-Relationships-between-DOIs-and-other-objects)
- [Requirements Traceability — Wikipedia](https://en.wikipedia.org/wiki/Requirements_traceability)
- [SARA Requirements Tool](https://dev.to/tumf/sara-a-cli-tool-for-managing-markdown-requirements-with-knowledge-graphs-nco)
- [Doorstop — GitHub](https://github.com/doorstop-dev/doorstop)
- [MyST Cross-references](https://mystmd.org/guide/cross-references)
- [MyST References Spec](https://mystmd.org/spec/references)
- [Hugo Cross References](https://gohugobrasil.netlify.app/content-management/cross-references/)

### LLM-Optimized Formats
- [Claude Citations API](https://platform.claude.com/docs/en/build-with-claude/citations)
- [Anthropic Citations API — Simon Willison](https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/)
- [Citation-Aware RAG — Tensorlake](https://www.tensorlake.ai/blog/rag-citations)
- [Anthropic-Style Citations with Any LLM](https://medium.com/data-science-collective/anthropic-style-citations-with-any-llm-2c061671ddd5)
- [XML Tags for Prompts — Claude Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)
- [AI In-Text Citations — Substack](https://iaee.substack.com/p/ai-generated-in-text-citations-intuitively)
- [Good Specs for AI Agents — Addy Osmani](https://addyosmani.com/blog/good-spec/)
- [Good Specs for AI Agents — O'Reilly](https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/)

### Sidecar Metadata
- [Sidecar File — Wikipedia](https://en.wikipedia.org/wiki/Sidecar_file)
- [Sidecar Files in DAM](https://www.orangelogic.com/sidecar-in-digital-asset-management)
- [ExifTool Sidecar Files](https://exiftool.org/metafiles.html)
- [Sidematter Format — GitHub](https://github.com/jlevy/sidematter-format)

### Additional Context
- [SARA on Hacker News](https://news.ycombinator.com/item?id=46752826)
- [ContextGit — GitHub](https://github.com/Mohamedsaleh14/ContextGit)
- [Agentic Document Workflows — LlamaIndex](https://www.llamaindex.ai/blog/introducing-agentic-document-workflows)
- [Building Effective AI Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
