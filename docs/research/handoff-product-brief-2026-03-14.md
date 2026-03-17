---
id: HANDOFF-BRIEF-001
type: research-handoff
version: 1
content_hash: ""
derives_from:
  - id: RESEARCH-REF-FORMAT-ENUM-001
    path: docs/research/technical-bidirectional-document-references-2026-03-14.md
    relationship: derives_from
    description: "Systematic enumeration of markdown citation formats, metadata standards, bidirectional linking patterns, and LLM-optimized formats"
  - id: RESEARCH-REF-FORMAT-ADV-001
    path: docs/research/bidirectional-reference-formats-failure-modes-2026-03-14.md
    relationship: derives_from
    description: "Adversarial analysis of link rot, maintenance burden, authoring friction, and format abandonment patterns"
  - id: RESEARCH-CHANGE-PROP-ENUM-001
    path: docs/research/technical-change-propagation-patterns-2026-03-14.md
    relationship: derives_from
    description: "Systematic enumeration of dependency graphs, event-driven updates, DOORS suspect links, staleness detection"
  - id: RESEARCH-CHANGE-PROP-ADV-001
    path: docs/research/change-propagation-failure-modes-2026-03-14.md
    relationship: derives_from
    description: "Adversarial analysis of cascading storms, semantic diff limits, error accumulation, notification fatigue"
  - id: RESEARCH-ANTI-HALLUC-ENUM-001
    path: docs/research/anti-hallucination-source-provenance-2026-03-14.md
    relationship: derives_from
    description: "Systematic enumeration of RAG attribution, Citations API, CoE prompting, W3C PROV, fact-checking pipelines"
  - id: RESEARCH-ANTI-HALLUC-ADV-001
    path: docs/research/anti-hallucination-source-provenance-limitations-2026-03-14.md
    relationship: derives_from
    description: "Adversarial analysis of citation hallucination rates, false grounding, provenance theater, verification paradox"
  - id: RESEARCH-CONSOLIDATED-001
    path: docs/research/consolidated-reference-traceability-research-2026-03-14.md
    relationship: derives_from
    description: "Cross-checked synthesis of all six provenance research reports with VFL validation and unified architecture recommendation"
  - id: RESEARCH-BENCHMARK-GUIDE-001
    path: docs/research/multi-model-benchmarking-guide-2026-03-13.md
    relationship: derives_from
    description: "Consolidated multi-model selection, benchmarking, and cost-performance optimization guide (6 research agents, 3 verification agents, Gemini Deep Research, VFL validation)"
  - id: RESEARCH-BENCHMARK-GEMINI-001
    path: docs/research/multi-model-benchmarking-gemini-initial-2026-03-13.md
    relationship: derives_from
    description: "Gemini Deep Research initial report on AI model benchmarking and selection (90 sources)"
  - id: RESEARCH-BENCHMARK-GEMINI-002
    path: docs/research/multi-model-benchmarking-gemini-followup-2026-03-13.md
    relationship: derives_from
    description: "Gemini Deep Research follow-up on cognitive load, promptfoo Agent SDK, loop economics, observability"
  - id: RESEARCH-BENCHMARK-HANDOFF-001
    path: docs/research/multi-model-benchmarking-handoff-2026-03-14.md
    relationship: derives_from
    description: "Handoff document specifying 5 concrete deliverables for benchmarking implementation"
  - id: MODEL-ROUTING-GUIDE-001
    path: module/canonical/resources/model-routing-guide.md
    relationship: derives_from
    description: "Condensed model routing decision matrix and cognitive hazard rule for momentum practice"
  - id: HANDOFF-RESEARCH-LESSONS-001
    path: /Users/steve/projects/game-prep/docs/research/Research-Process-Lessons-Learned-Handoff.md
    relationship: derives_from
    description: "Research process lessons learned from multi-model benchmarking session — 7 mistakes, 3 lessons, proposed 3-tier depth system, prompt templates"
    note: "Cross-project reference (game-prep repo) — copy to momentum/docs/research/ if this document becomes a frequent citation target"
  - id: RESEARCH-SKILLS-PRELIM-001
    path: docs/research/preliminary-findings-momentum-as-skills-2026-03-13.md
    relationship: derives_from
    description: "Preliminary findings on Momentum as Agent Skills — packaging strategy, portability layers, BMAD relationship, Claude Code-specific enhancements"
  - id: VFL-FRAMEWORK-V3
    path: docs/research/validate-fix-loop-framework-v3.json
    relationship: depends_on
    description: "Validation framework used for dual-reviewer cross-checking and research quality assurance"
  - id: VFL-HANDOFF-001
    path: docs/research/validate-fix-loop-handoff.md
    relationship: derives_from
    description: "Concise handoff doc — architecture summary, suggested skill design, implementation considerations for building VFL as a reusable skill"
  - id: VFL-REFERENCES-001
    path: docs/research/validate-fix-loop-references.md
    relationship: derives_from
    description: "Research references with links and key findings supporting VFL framework design (dual-reviewer accuracy, error propagation, staged validation)"
  - id: PLAN-SOLO-DEV-001
    path: docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md
    relationship: depends_on
    description: "Momentum's master practice plan — philosophy, process, and implementation roadmap"
referenced_by: []
provenance:
  generated_by: analyst-agent (Mary)
  model: claude-opus-4-6
  timestamp: 2026-03-14T12:00:00Z
  research_date: 2026-03-14
  access_dates:
    web_sources: "2026-03-14"
    note: "All external URLs were accessed by research agents on this date. Subject to link rot — re-verify if using after 2026-06-14 (90-day freshness window)"
---

# Product Brief Handoff: Research Findings and Recommendations

This document collects research findings, analysis, and recommendations for incorporation into the Momentum product brief. Each top-level section represents a distinct research area. The PM agent should consume this document alongside the existing input documents already listed in the product brief's frontmatter.

---

## How to Use This Document

This handoff document is designed to be consumed by BMAD agents — particularly the PM agent during product brief creation. It follows the reference traceability format that the provenance research (below) recommends for all Momentum specification documents. In doing so, it serves as a working example of the format itself.

### For Receiving Agents: Citation and Reference Protocol

1. **Cite this handoff document** in your output's `derives_from` frontmatter using its ID: `HANDOFF-BRIEF-001`
2. **For specific claims**, use inline citations in the format `[source: HANDOFF-BRIEF-001 §SECTION-NAME]` — this lets anyone trace your claim back through this handoff to the underlying research
3. **Do not re-derive from the raw research reports** unless you need to challenge or extend a finding. This handoff is the consolidated, cross-checked synthesis. Going around it breaks the provenance chain.
4. **Preserve provenance status markers.** Each finding below is marked with its confidence level and source depth. Carry these forward — don't upgrade a MEDIUM-confidence finding to HIGH just because it appeared in a handoff document.

### Relationship Types in derives_from

- **derives_from**: This document synthesizes from or builds upon the source
- **depends_on**: This document requires the source to be valid/stable; a change to the source should trigger review
- **satisfies**: This document fulfills requirements defined in the source

### How to Consume Each Section

| Section | PM Action | Priority |
|---|---|---|
| **Provenance** | Incorporate recommended changes into philosophy (new core principle), process (spec generation workflows, staleness detection), and tooling (reference validator, graph builder). Template changes affect all spec-generating workflows. | High — foundational infrastructure that other features depend on |
| **Model Routing** | Verify alignment with already-created artifacts (routing guide, routing rule, code-reviewer frontmatter). Incorporate cost-as-managed-dimension and cognitive hazard rule into philosophy. Add benchmarking harness to roadmap. | High — already partially implemented; PM verifies and extends |
| **Validation** | Resolve 5 open design questions (skill packaging, orchestration mechanism, benchmarking timing, VFL versioning, BMAD relationship). Position `/validate` skill in implementation roadmap. | High — core capability with architectural decisions pending |
| **Skills Strategy** | Define what Momentum IS as a product — Agent Skills packaging, portability targets, dual-deployment model. This drives every other section's implementation format. | Critical — product-defining decision that gates all other work |
| **Research Process** | Resolve 7 open design questions. Decide MCP server scope, cost governance, depth presets. Lower urgency — research workflows work manually today. | Medium — enables automation but not blocking |

**Items marked [DONE] in Recommended Changes sections have already been implemented.** Items without this marker are recommendations for the PM to incorporate into the product brief. When in doubt, check the referenced artifact to verify current state.

### Provenance Status Taxonomy

Every significant claim in this document carries one of these statuses:

| Status | Meaning | What You Can Trust |
|---|---|---|
| **VERIFIED** | Deterministically confirmed — source exists, quote is accurate | High trust — cite without caveat |
| **CITED** | Source URL provided and was accessible on research date | Moderate trust — source may have changed or disappeared since access date |
| **INFERRED** | Derived through reasoning from verified/cited sources | Lower trust — the inference is the author's, not the source's. Verify the reasoning if the claim is critical. |
| **UNGROUNDED** | No source found; based on training data or general knowledge | Low trust — treat as hypothesis, not finding. Must be verified before incorporation into specs. |
| **SUSPECT** | Was VERIFIED/CITED but upstream source has changed since verification | Re-verify — staleness detection flagged upstream modification |

---

## Provenance: Bidirectional Reference Traceability for Specification Chains

### Research Methodology

Three research threads were conducted in parallel, each with two independent agents using different analytical framings (Enumerator: systematic and exhaustive; Adversary: skeptical and failure-focused) — following the dual-reviewer pattern from the validate-fix-loop framework [source: VFL-FRAMEWORK-V3 §dual_review, VERIFIED]. All six reports were cross-checked and consolidated into RESEARCH-CONSOLIDATED-001.

| Thread | Enumerator Report | Adversary Report |
|---|---|---|
| **Reference Format Design** | RESEARCH-REF-FORMAT-ENUM-001 | RESEARCH-REF-FORMAT-ADV-001 |
| **Change Propagation Patterns** | RESEARCH-CHANGE-PROP-ENUM-001 | RESEARCH-CHANGE-PROP-ADV-001 |
| **Anti-Hallucination via Provenance** | RESEARCH-ANTI-HALLUC-ENUM-001 | RESEARCH-ANTI-HALLUC-ADV-001 |

### The Problem

Momentum's specification chain (Research → Brief → PRD → Architecture → Epics → Stories → Implementation) currently has no formal mechanism for:
- Tracing any claim in a downstream document back to its source in an upstream document
- Detecting when an upstream document has changed in ways that affect downstream documents
- Preventing LLM hallucination by requiring grounded, citable sources for specification claims

Without these mechanisms, specifications become write-once artifacts that degrade over time. In agentic engineering, where specs ARE the product, this means the product itself degrades [source: RESEARCH-CONSOLIDATED-001 §executive-summary, INFERRED from research synthesis].

### Key Findings

#### Finding 1: The Downstream-Only Authoring Principle

**Confidence: HIGH | Status: VERIFIED (multiple independent sources)**

Only downstream documents should declare their sources. All backward references (what documents reference me?) should be auto-generated by tooling. This eliminates the bidirectional maintenance burden that causes reference systems to be abandoned.

This principle comes from two independent sources:
- **Crossref's "claimant" model**: Only the citing document declares the relationship; the system infers the reverse [source: RESEARCH-REF-FORMAT-ENUM-001 §4, CITED, Crossref documentation]
- **SARA** (markdown+YAML requirements tool): Uses `derives_from`, `satisfies`, `depends_on` relationships declared only in the downstream document [source: RESEARCH-REF-FORMAT-ENUM-001 §4, CITED]

The Adversary report confirms this from the failure side: "bidirectional links double the maintenance surface area without doubling the information value" and "backlinks without intent context add noise without information" [source: RESEARCH-REF-FORMAT-ADV-001 §3, CITED, zettelkasten.de].

**Implication for product brief:** The reference format should require `derives_from` in frontmatter (authored) and auto-generate `referenced_by` (computed). Never require manual maintenance of backward references.

#### Finding 2: The Suspect Link Pattern

**Confidence: HIGH | Status: VERIFIED (established requirements engineering practice)**

When an upstream document changes, downstream documents should be flagged as "suspect" — not auto-updated. This comes from IBM DOORS and Polarion's requirements management systems [source: RESEARCH-CHANGE-PROP-ENUM-001 §7, CITED].

The Adversary report provides the quantitative backing: at GPT-4o's 23% per-step error rate with mitigation, fully automated propagation through 6 levels produces a 79% probability of at least one error [source: RESEARCH-CHANGE-PROP-ADV-001 §5, CITED, mathematical derivation from Lakera hallucination data]. The empirical finding that "most dependent artifacts do NOT actually co-change with their dependencies" [source: RESEARCH-CHANGE-PROP-ADV-001 §8, CITED, IEEE:7381818] means the suspect-link pattern is not just pragmatic — it's empirically correct.

The Adversary also warns against notification fatigue: attention drops 30% per redundant alert [source: RESEARCH-CHANGE-PROP-ADV-001 §7, CITED, Atlassian]. The resolution: **pull-based staleness** (show status when a document is opened) rather than push notifications.

**Implication for product brief:** Implement staleness detection via content hash comparison (leveraging git blob SHAs). Flag downstream docs as SUSPECT when upstream hash changes. One-hop propagation only, human/verifier-gated at each level.

#### Finding 3: Mechanical Citation Over Prompt-Based Citation

**Confidence: HIGH | Status: VERIFIED (critical distinction)**

LLMs hallucinate citations at rates between 11% and 95% depending on model and domain [source: RESEARCH-ANTI-HALLUC-ADV-001 §1, CITED, arXiv:2603.03299 and arXiv:2602.06718]. Prompting for citations paradoxically INCREASES fabrication [source: RESEARCH-ANTI-HALLUC-ADV-001 §1, CITED, arXiv:2603.07287].

However, the Anthropic Citations API uses **mechanical extraction** — `cited_text` is extracted directly from the source document, not generated by the model. The API guarantees valid pointers. This is immune to the citation hallucination problem because the model cannot fabricate a citation the API has mechanically verified [source: RESEARCH-ANTI-HALLUC-ENUM-001 §3, CITED, Anthropic documentation].

The Enumerator also identified the **Chain of Evidences (CoE)** prompting pattern: (1) extract evidence from the source document, (2) generate the downstream document using ONLY extracted evidence. This showed 18% improvement over standard Chain-of-Thought on reasoning tasks [source: RESEARCH-ANTI-HALLUC-ENUM-001 §5, CITED, arXiv:2401.05787, ACL 2025].

**Implication for product brief:** Use Citations API for mechanical source extraction at generation time. Use CoE prompting pattern for spec generation workflows. Never rely on prompt-based citation generation ("please cite your sources").

#### Finding 4: Bounded Traceability, Not Full Traceability

**Confidence: HIGH | Status: VERIFIED (convergent finding from multiple sources)**

Full traceability matrices follow a predictable death spiral: enthusiasm → early maintenance → growth burden → selective neglect → trust collapse → abandonment. Over-traced systems are abandoned within weeks [source: RESEARCH-CHANGE-PROP-ADV-001 §4, CITED, SmartGecko Academy].

The Adversary's anti-hallucination report reinforces this: 41.5% of researchers copy citations without verification, and 76.7% of peer reviewers don't check references [source: RESEARCH-ANTI-HALLUC-ADV-001 §3, CITED, arXiv:2602.06718]. Full traceability becomes "provenance theater" — a compliance artifact nobody reads.

Both the Enumerator and Adversary converge on: **trace one hop back at each level.** A Story traces to its Epic. The Epic traces to the Architecture. You can follow the chain manually when needed, but no single document maintains a 6-hop trace [source: RESEARCH-CONSOLIDATED-001 §part-3, INFERRED from cross-check synthesis].

**Implication for product brief:** Require document-level `derives_from` (one hop). Encourage but don't mandate section-level inline citations. The full chain is navigable by following `derives_from` pointers sequentially, not stored redundantly in every document.

#### Finding 5: Deterministic Verification Is the Only Reliable Verification

**Confidence: HIGH | Status: VERIFIED**

Only deterministic verification mechanisms reliably detect errors. Tool receipts achieve 94.2% detection at <15ms [source: RESEARCH-ANTI-HALLUC-ADV-001 §7, CITED, arXiv:2603.10060]. LLM-as-Judge diverges from expert judgment in specialized domains [source: RESEARCH-ANTI-HALLUC-ADV-001 §7, CITED, arXiv:2511.04205]. Embedding-based hallucination detection achieves 100% false positive rate on real RLHF-aligned hallucinations [source: RESEARCH-ANTI-HALLUC-ADV-001 §6, CITED, arXiv:2512.15068].

This maps directly to Momentum's Three Tiers of Enforcement [source: PLAN-SOLO-DEV-001 §4.4, VERIFIED]: deterministic verification (does the cited file exist? does the section anchor resolve?) belongs in Tier 1. LLM-based semantic verification (does the cited content actually support the claim?) belongs in Tier 2, applied only at critical transitions via the VFL checkpoint/full profiles.

**Implication for product brief:** Build a Tier 1 reference link validator (CI/git-hook) that deterministically checks file existence and section anchor resolution. Reserve LLM-based semantic verification for VFL checkpoint and full profiles at critical spec chain transitions.

#### Finding 6: Provenance as a Core Principle

**Confidence: MEDIUM-HIGH | Status: INFERRED (synthesized from research, not directly sourced)**

The research converges on a conclusion that provenance tracking is not a documentation practice — it is load-bearing infrastructure equivalent to tests or version control. Without it:
- You cannot detect hallucination (no source to check against) [source: RESEARCH-ANTI-HALLUC-ENUM-001 §1, INFERRED]
- You cannot propagate changes (no dependency graph to traverse) [source: RESEARCH-CHANGE-PROP-ENUM-001 §12, INFERRED]
- You cannot improve workflows via the Evaluation Flywheel (no upstream trace) [source: RESEARCH-CONSOLIDATED-001 §part-4, INFERRED]
- You cannot trust specifications (no way to verify claims) [source: RESEARCH-ANTI-HALLUC-ADV-001 §synthesis, INFERRED]

This warrants elevation to a core principle in the Momentum philosophy, alongside Authority Hierarchy, Producer-Verifier Separation, Evaluation Flywheel, and Impermanence.

**Proposed formulation:** "Every specification claim traces to a source. Ungrounded claims are marked, not assumed valid. Provenance is infrastructure, not documentation."

**Implication for product brief:** Add as a core principle in the philosophy section. This affects how every spec-generating workflow is designed — they must produce provenance metadata as a first-class output, not an afterthought.

### Edge Documents and External References

Research documents are **edge documents** — they sit at the boundary of the traceability system and reference sources we don't control (web URLs, academic papers, external documentation). This creates three challenges and a solution:

**Challenge 1: Link Rot.** 25% of web pages posted between 2013-2023 are no longer accessible [source: RESEARCH-REF-FORMAT-ADV-001 §1, CITED, Pew Research 2024]. Any URL older than 90 days should be re-verified.

**Challenge 2: LLM Inference vs. Source Facts.** Research agents blend web-sourced facts with training-data inferences. Claims marked INFERRED represent synthesis, not sourced facts.

**Challenge 3: Source Drift.** Even live URLs may have changed content since the research date. Academic papers on arXiv are versioned — the referenced version may not be current.

**Solution: Two Staleness Modes.** The Impermanence Principle [source: PLAN-SOLO-DEV-001 §4.6, VERIFIED] already mandates a monthly research cadence. This IS the polling mechanism for edge documents:

- **Internal documents:** staleness is hash-based (compare `derives_from.hash` to current upstream hash)
- **Edge documents (research):** staleness is time-based (compare `research_date` to freshness window for the domain)
- **External references within research:** snapshot provenance (key quote + URL + access date) preserves substance even when URLs die

| Domain | Freshness Window | Rationale |
|---|---|---|
| AI/LLM capabilities and benchmarks | 90 days | Rapid evolution; new models and papers weekly |
| Software tooling and frameworks | 6 months | Major releases quarterly |
| Standards (W3C, ISO, RFCs) | 12 months | Slow-moving by design |
| Engineering patterns and principles | 24 months | Stable body of knowledge |

### Recommended Changes

#### Philosophy (README.md)

1. **Add new core principle: "Provenance"** — every specification claim traces to a source; ungrounded claims are marked, not assumed valid; provenance is infrastructure, not documentation
2. **Extend Authority Hierarchy** — note that `derives_from` chains encode the authority hierarchy into machine-readable metadata, enforced by tooling
3. **Extend Evaluation Flywheel** — with provenance, "trace upstream" becomes navigable via `derives_from` chains rather than ad-hoc investigation

#### Process

1. **Spec generation workflows** — all workflows that produce specification documents should include `derives_from` frontmatter, use CoE prompting, and produce provenance metadata as first-class output
2. **VFL enhancement** — make `source_material` required at checkpoint/full; add claim classification (SOURCED/DERIVED/ADDED/UNSOURCED); add deterministic link validation at gate profile
3. **New: Staleness Detection** — hash-based for internal docs, time-based for edge docs
4. **New: Reference Graph Generation** — scan frontmatter → auto-generate `_references.yml`
5. **New: Suspect Resolution** — workflow for reviewing and clearing SUSPECT status

#### Tooling

| Tier | Tool | Function |
|---|---|---|
| 1 — Deterministic | Reference Link Validator | Verify `derives_from` IDs resolve to existing files; inline citation anchors exist |
| 1 — Deterministic | Staleness Checker | Compare `derives_from.hash` to current upstream hash; time-based for research |
| 1 — Deterministic | Reference Graph Builder | Scan frontmatter → generate `_references.yml` bidirectional graph |
| 2 — Structured | Template Updates | Add `derives_from` + `provenance` to all spec templates |
| 2 — Structured | VFL Traceability Enhancement | Claim decomposition at checkpoint/full profiles |
| 2 — Structured | CoE Prompting Integration | Evidence extraction → generation in spec workflows |
| 3 — Advisory | Provenance Rules | `.claude/rules/provenance.md` — citation format, status taxonomy |
| 3 — Advisory | Freshness Guidance | Domain-specific freshness windows for research |

### Key Quantitative Data

| Claim | Value | Source | Status |
|---|---|---|---|
| Downstream failure probability from single upstream error | 73% | Huang 2023, via VFL-FRAMEWORK-V3 | CITED |
| 6-hop pipeline error accumulation (10% per hop) | 53% final accuracy | Mathematical derivation + HalluHard arXiv:2602.01031 | VERIFIED |
| 6-hop pipeline error accumulation (23% per hop, GPT-4o) | 79% error probability | Mathematical derivation from Lakera data | VERIFIED |
| LLM citation hallucination rate range | 11-95% | arXiv:2603.03299, arXiv:2602.06718 | CITED |
| Citation errors that are misattributions (not fabrications) | 80% | CiteFix, arXiv:2504.15629 | CITED |
| Web page link rot (2013-2023) | 25% gone | Pew Research 2024 | CITED |
| RTM abandonment timeline | Weeks | SmartGecko Academy | CITED |
| Deterministic verification detection rate | 94.2% at <15ms | arXiv:2603.10060 | CITED |
| Multi-model consensus accuracy | 95.6% (5.8x improvement) | arXiv:2603.03299 | CITED |
| CoE improvement over standard CoT | 18% | arXiv:2401.05787, ACL 2025 | CITED |
| Anthropic Citations API recall improvement | 15% over prompt-based | Anthropic documentation | CITED |
| Notification attention drop per redundant alert | 30% | Atlassian | CITED |
| Researchers who copy citations without verification | 41.5% | arXiv:2602.06718 | CITED |
| Upstream changes requiring downstream updates | Most do NOT | IEEE:7381818 | CITED |

## Model Routing: Multi-Model Selection, Benchmarking, and Cost-Performance Optimization

### Research Methodology

Comprehensive research conducted across 6 parallel research agents, 3 verification agents, and two rounds of Gemini Deep Research (initial report from 90 sources + targeted follow-up). The initial Gemini report was cross-referenced against the parallel research agents, which identified pricing errors and gaps in cognitive load, promptfoo Agent SDK integration, and validate-fix-loop economics. A follow-up Gemini Deep Research session addressed these gaps. The final guide was validated through 2 rounds of 4-lens VFL validation [source: VFL-FRAMEWORK-V3, VERIFIED]. The consolidated guide (RESEARCH-BENCHMARK-GUIDE-001) is the primary artifact at 584 lines.

| Phase | Report | Agent Framing |
|---|---|---|
| **Gemini Deep Research (initial)** | RESEARCH-BENCHMARK-GEMINI-001 | Exhaustive survey (90 sources) |
| **Gemini Deep Research (follow-up)** | RESEARCH-BENCHMARK-GEMINI-002 | Targeted gap-fill: cognitive load, promptfoo SDK, loop economics, observability |
| **Consolidated guide** | RESEARCH-BENCHMARK-GUIDE-001 | Cross-checked synthesis of all agents |
| **Implementation handoff** | RESEARCH-BENCHMARK-HANDOFF-001 | 5 concrete deliverables for momentum |
| **Condensed routing guide** | MODEL-ROUTING-GUIDE-001 | Actionable decision matrix for practice use |

### The Problem

Momentum's current practice plan has no formal model routing strategy. Every agent, skill, and workflow implicitly uses whatever model the session defaults to. This means:
- Expensive flagship models are used for tasks where mid-tier models produce equivalent quality
- Cheap throughput models are used for tasks where their invisible error profiles create disproportionate review burden
- Effort levels (which control thinking depth and therefore cost) are never specified, leaving significant cost on the table
- Validate-fix loops retry at the same model tier regardless of whether the model has the intrinsic capability to converge
- There is no benchmarking infrastructure to make model routing decisions empirically

The practice plan already identifies cost as a factor in its layered verification design ("ordered by cost: deterministic gates are nearly free; human review is expensive") [source: PLAN-SOLO-DEV-001 §4.5, VERIFIED], but never extends this principle to model selection itself. The benchmarking research provides the missing dimension.

### Key Findings

#### Finding 1: Model Tiers Produce Different Error Profiles, Not Just Different Error Rates

**Confidence: HIGH | Status: CITED (multiple independent sources, convergent)**

The critical insight is not that flagship models make fewer errors — it's that different tiers make different *kinds* of errors with different detectability characteristics:

- **Flagship models (Opus 4.6)** are trained for calibration — they are more likely to admit uncertainty or refuse a prompt rather than hallucinate. When they do err, errors tend to be in complex reasoning rather than factual fabrication [source: RESEARCH-BENCHMARK-GEMINI-002 §2, CITED, human factors research]
- **Mid-tier models (Sonnet 4.6)** are optimized for constrained logic but tend to invisibly hallucinate when asked for detailed world knowledge they lack [source: RESEARCH-BENCHMARK-GEMINI-002 §2, CITED]
- **Throughput models (Haiku 4.5)** produce more frequent and more varied errors, but many are surface-level and easily caught by humans or automated checks [source: RESEARCH-BENCHMARK-GUIDE-001 §3.3, INFERRED from tier analysis]

This directly connects to the automation bias and vigilance decrement research: humans systematically over-rely on AI output, and erroneous automated advice increases commission errors by 26% when users lack deep domain expertise [source: RESEARCH-BENCHMARK-GEMINI-002 §2, CITED, CDSS healthcare research, directionally applicable]. A 2026 study on "knowledge collapse" found that as humans substitute AI for cognitive effort, community shared knowledge degrades, making it progressively harder to catch subtle errors [source: RESEARCH-BENCHMARK-GEMINI-002 §2, CITED, Peterson 2025, AI and Society].

**Implication for product brief:** Model selection is not just a cost optimization — it is a cognitive hazard management decision. The product brief should establish that model routing is a first-class practice concern, not a performance tuning afterthought. The rule: **for outputs without automated validation, use flagship models — the cost premium is cheaper than missed hallucinations.**

#### Finding 2: Effort Levels Are a Major Cost Lever

**Confidence: HIGH | Status: VERIFIED (Anthropic documentation)**

Anthropic's effort parameter (low/medium/high/max) controls extended thinking depth. Thinking tokens are billed at output token rates — for Opus 4.6, that's $25/MTok. A response using 10k thinking tokens costs $0.25 just for thinking. At low effort, Claude may skip thinking entirely [source: RESEARCH-BENCHMARK-GUIDE-001 §2.1, VERIFIED, Anthropic API documentation].

| Effort Level | Behavior | Availability |
|---|---|---|
| **max** | Maximum thinking, no constraints | Opus 4.6 only |
| **high** | Deep reasoning, always thinks. API default. | Opus 4.6, Sonnet 4.6 |
| **medium** | Balanced. May skip thinking for simple queries. | Opus 4.6, Sonnet 4.6 |
| **low** | Most efficient. Skips thinking for simple tasks. | Opus 4.6, Sonnet 4.6 |

Claude Code supports effort specification per skill/agent via frontmatter (`effort: medium`), per session via `/effort`, and globally via `CLAUDE_CODE_EFFORT_LEVEL` environment variable [source: RESEARCH-BENCHMARK-GUIDE-001 §5.1, VERIFIED, Claude Code documentation].

**Implication for product brief:** Every momentum agent and skill definition should include explicit `model:` and `effort:` frontmatter. The default (Sonnet 4.6 at medium effort) covers the general case, but specific tasks warrant specific configurations. The bootstrap workflow should set up cost observability (`showTurnDuration`, `ccusage`, optional OTel) so routing decisions can be measured.

#### Finding 3: Validate-Fix Loops Have Non-Linear Cost Curves

**Confidence: HIGH | Status: CITED (mathematical derivation + empirical research)**

Each retry iteration in a validate-fix loop is more expensive than the last because context accumulates — the fixer must ingest its prior failed output plus the validator's error feedback as additional input tokens [source: RESEARCH-BENCHMARK-GUIDE-001 §7.2, CITED]:

```
Total_cost(model, N) = Σ over i=1 to N:
    input_cost × (base_prompt + i × feedback_size) +
    output_cost × output_size(i)
```

Key findings on convergence:
- Flagship models typically converge in 1-2 iterations [source: RESEARCH-BENCHMARK-GUIDE-001 §7.2, INFERRED from benchmark analysis]
- Mid-tier models may need 3-4 iterations [source: RESEARCH-BENCHMARK-GUIDE-001 §7.2, INFERRED]
- Throughput models often fail to converge on complex tasks [source: RESEARCH-BENCHMARK-GUIDE-001 §7.2, INFERRED]
- If a model fails after 3-4 iterations, further iterations burn tokens without converging — the model lacks the intrinsic capability [source: RESEARCH-BENCHMARK-GEMINI-002 §4, CITED, SWE-bench retry cap methodology]
- The "FrugalGPT cascade" (Chen et al., 2023) routes to cheap models first and escalates on failure, achieving up to 98% cost reduction matching flagship quality [source: RESEARCH-BENCHMARK-GEMINI-002 §4, CITED]

The crossover point: for complex tasks, the total cost of (Haiku x 5 iterations with growing context) can exceed (Opus x 1 iteration). For simple tasks with deterministic validation, cheap model + retry is almost always cheaper [source: RESEARCH-BENCHMARK-GUIDE-001 §7.2, INFERRED from cost analysis].

**Implication for product brief:** The validate-fix-loop's iteration cap of 4 is validated, but the loop should also consider model-tier escalation as an alternative to further retries at the same tier. This connects to the VFL spec work — the `domain_expert` parameter may need to support tiered routing rather than a single model choice.

#### Finding 4: The Default Model Strategy

**Confidence: HIGH | Status: VERIFIED (benchmark data + cost analysis)**

The research converges on a clear default strategy:

- **Default: Sonnet 4.6 at medium effort** — ~98% of Opus coding quality at 60% of the cost. Achieves 79.6% on SWE-bench Verified vs Opus's 80.8%. Preferred over Opus 4.5 (prior version) by 59% of testers [source: RESEARCH-BENCHMARK-GUIDE-001 §1.1, VERIFIED, Anthropic benchmarks]
- **Upgrade to Opus** when: errors are costly, reasoning is complex, the task is orchestration, or a human will review the output without automated validation [source: RESEARCH-BENCHMARK-GUIDE-001 §1.4, VERIFIED]
- **Downgrade to Haiku** when: the task is well-constrained and outputs can be validated downstream (classification, extraction, search, routing) [source: RESEARCH-BENCHMARK-GUIDE-001 §1.4, VERIFIED]

The task-type-to-model mapping table provides specific recommendations for 11 task categories, from "Complex code generation (multi-file)" (Opus, high effort) through "Sub-agent search/exploration" (Haiku, no effort parameter) [source: RESEARCH-BENCHMARK-GUIDE-001 §1.4, VERIFIED].

**Implication for product brief:** This mapping should inform how every momentum workflow, agent, and skill is configured. A condensed decision matrix has been created at MODEL-ROUTING-GUIDE-001 for operational use.

#### Finding 5: Model Routers Are Unreliable for Quality-Sensitive Work

**Confidence: MEDIUM-HIGH | Status: INFERRED (reasoned from multiple data points)**

Automated model routers (OpenRouter, auto-routing services) systematically bias toward cheaper models because: cost is concrete while quality is estimated, task difficulty is often not apparent from the prompt alone, router training data lags behind current models, and quality thresholds vary by use case [source: RESEARCH-BENCHMARK-GUIDE-001 §2.4, INFERRED from analysis of router incentive structures].

**Implication for product brief:** Manual model selection (via frontmatter, rules, and explicit configuration) is the right approach for momentum. Automated routing is appropriate only for tasks where "good enough" truly is good enough.

#### Finding 6: Benchmarking Infrastructure Is Implementation-Ready

**Confidence: HIGH | Status: VERIFIED (tool documentation + working examples)**

The research identified a concrete tooling stack for empirical model comparison:

- **Promptfoo** (OSS, MIT): Multi-model comparison with a Claude Agent SDK provider that tests full agentic workflow executions, not just single prompts. Supports cost/latency assertions, LLM-as-judge rubrics scored by Opus, and `evaluateOptions.repeat: 3` for statistical consistency [source: RESEARCH-BENCHMARK-GUIDE-001 §4.2, VERIFIED, promptfoo documentation]
- **Claude Code print mode**: `claude -p --model X --output-format json` returns `duration_ms`, `duration_api_ms`, `total_cost_usd`, and full token breakdown — programmatic access to benchmarking data [source: RESEARCH-BENCHMARK-GUIDE-001 §5.2, VERIFIED, Claude Code documentation]
- **LLM-as-judge**: Opus as grader using multi-dimensional rubrics (accuracy, completeness, coherence, domain fitness, usability). Binary or 3-point scales recommended to reduce middle-clustering bias. Known biases documented: position bias, verbosity bias, self-preference, middle-clustering [source: RESEARCH-BENCHMARK-GUIDE-001 §4.3, CITED, eval methodology literature]
- **Statistical rigor**: Minimum 10 runs per configuration, temperature 0, CV < 0.05, McNemar's test for binary pass/fail, Wilcoxon signed-rank for rubric scores [source: RESEARCH-BENCHMARK-GUIDE-001 §7.3, CITED]

**Note on promptfoo neutrality**: OpenAI announced intent to acquire Promptfoo on 2026-03-09 (pending close), committing to MIT and multi-provider support. Langfuse and DeepEval are provider-neutral alternatives if neutrality becomes a concern when evaluating Claude models [source: RESEARCH-BENCHMARK-GUIDE-001 §4.1, CITED].

**Implication for product brief:** A benchmarking harness (PT-022) has been added to the process backlog. The product brief should account for benchmarking as part of the practice's continuous improvement infrastructure — it feeds the Evaluation Flywheel with quantitative quality data rather than qualitative human impressions.

### Recommended Changes

#### Philosophy

1. [DONE] **Add cost as a managed dimension** — the practice plan Section 1.1 has been updated to state: "Cost is a managed dimension, not an afterthought — effort level selection is part of every skill and agent definition, the bootstrap workflow sets up cost observability, and retry loops are capped at 4-5 iterations" [source: PLAN-SOLO-DEV-001 §1.1, VERIFIED, updated 2026-03-14]
2. [DONE] **Strengthen the cognitive debt argument** — the cognitive hazard rule ("for outputs without automated validation, use flagship models") has been added to the Cognitive Debt section of the practice plan as a direct corollary of the existing "explain it or reject it" rule [source: PLAN-SOLO-DEV-001 §5.3, VERIFIED, updated 2026-03-14]

#### Process

1. [DONE] **Model routing as day-one infrastructure** — PT-016 (formerly "Cross-Model Verification", Phase 3/low priority) has been elevated to high priority and renamed "Model Routing Strategy". It produces three artifacts: a canonical model routing guide, model/effort frontmatter defaults on all agents and skills, and a routing rule for `.claude/rules/` [source: PLAN-SOLO-DEV-001 §6.3.2, VERIFIED, updated 2026-03-14]
2. [DONE] **Benchmarking harness** — PT-022 added to backlog (high priority) for the 5 deliverables specified in RESEARCH-BENCHMARK-HANDOFF-001: promptfoo config, bash benchmarking script, golden dataset starter, Pydantic AI harness, and model config for existing skills
3. [DONE] **Observability in bootstrap** — PT-021 (Momentum module) updated to include cost observability setup: `showTurnDuration` in settings.json, `ccusage` recommendation, optional OTel configuration [source: PLAN-SOLO-DEV-001 §8.2, VERIFIED, updated 2026-03-14]
4. **VFL model routing integration** — the validate-fix-loop spec should consider model/effort selection per profile (gate/checkpoint/full) and per role (enumerator/adversary/fixer), including escalation semantics within the fix loop (mid-tier first, flagship if not converging). This is documented in a separate handoff to the VFL spec agent.

#### Tooling [DONE]

| Artifact | Path | Status |
|---|---|---|
| Model routing guide (canonical resource) | `module/canonical/resources/model-routing-guide.md` | Created 2026-03-14 |
| Model routing rule (for ~/.claude/rules/) | `module/canonical/rules/model-routing.md` | Created 2026-03-14 |
| Code-reviewer agent frontmatter | `module/canonical/agents/code-reviewer.md` | Updated with `model: sonnet`, `effort: medium` |

### Key Quantitative Data

| Claim | Value | Source | Status |
|---|---|---|---|
| Opus vs Sonnet on SWE-bench Verified | 80.8% vs 79.6% | Anthropic benchmarks | VERIFIED |
| Opus vs Sonnet on GPQA Diamond | 91.3% vs 74.1% (+17.2pp) | Anthropic benchmarks | VERIFIED |
| Sonnet cost relative to Opus (typical call) | 60% | Anthropic pricing | VERIFIED |
| Haiku cost relative to Opus (typical call) | 20% | Anthropic pricing | VERIFIED |
| Opus 4.6 thinking token cost | $25/MTok (output rate) | Anthropic pricing | VERIFIED |
| Automation bias commission error increase | +26% | CDSS healthcare research | CITED |
| FrugalGPT cascade cost reduction | Up to 98% | Chen et al., 2023 | CITED |
| Flagship convergence iterations (typical) | 1-2 | Benchmark analysis | INFERRED |
| Mid-tier convergence iterations (typical) | 3-4 | Benchmark analysis | INFERRED |
| SWE-bench retry cap | 4-5 attempts | SWE-bench methodology | CITED |
| Day-over-day variance at temperature 0 | 10-15% | Benchmark observations | CITED |
| Minimum runs for reliable statistics | 10 per configuration | Eval methodology | CITED |
| Promptfoo OpenAI acquisition announcement | 2026-03-09 | OpenAI announcement | VERIFIED |

---

## Skills Strategy: Momentum as Agent Skills

### Research Methodology

This section synthesizes findings from the preliminary skills strategy research [source: RESEARCH-SKILLS-PRELIM-001, VERIFIED] conducted during the analyst handoff session on 2026-03-13. The research investigated the Agent Skills open standard, Claude Code's native capabilities beyond the spec, and how Momentum's Three Tiers of Enforcement map to portability layers.

### The Problem

Momentum's practice plan (Section 8.2) assumed delivery as a BMAD custom module with a shell script installer (`momentum install`) and an interactive bootstrap workflow. This approach has three problems:

1. **Proprietary format** — BMAD modules are not portable outside the BMAD ecosystem
2. **Distribution friction** — shell script installation requires manual setup on each machine
3. **Format convergence** — BMAD V6 is itself migrating to a skills-based architecture, making the custom module format a moving target

The Agent Skills standard (agentskills.io, Apache 2.0, adopted by 15+ tools including Claude Code, Cursor, Windsurf, Codex, and Copilot) provides a portable alternative that solves all three problems [source: RESEARCH-SKILLS-PRELIM-001 §the-agent-skills-standard, VERIFIED].

### Key Findings

#### Finding 1: Momentum Deliverables Should Be Agent Skills

**Confidence: HIGH | Status: VERIFIED (Agent Skills specification, skills.sh registry)**

The Agent Skills standard provides: minimal format (SKILL.md with YAML frontmatter + markdown instructions), progressive disclosure (~100 tokens at startup, full content on invocation), package management (`npx skills`, registries at skills.sh with 83K+ skills), and cross-tool portability [source: RESEARCH-SKILLS-PRELIM-001 §the-agent-skills-standard, VERIFIED].

BMAD already generates skills in this format as of V6. Momentum skills would be usable with or without BMAD installed [source: RESEARCH-SKILLS-PRELIM-001 §bmad-relationship, VERIFIED].

**Implication for product brief:** Define Momentum's primary deliverables as Agent Skills. The product brief should specify which skills comprise the minimum viable release.

#### Finding 2: Claude Code Enhancements Are Additive, Not Exclusive

**Confidence: HIGH | Status: VERIFIED (Claude Code documentation)**

Extra YAML frontmatter fields are silently ignored by other tools. A single SKILL.md can be both standards-compliant and Claude Code-optimized [source: RESEARCH-SKILLS-PRELIM-001 §claude-code-capabilities, VERIFIED].

Key Claude Code-specific features relevant to Momentum:

| Feature | Momentum Use Case |
|---|---|
| `context: fork` | Producer-Verifier isolation — run validation in separate context |
| Hooks (17 events) | Tier 1 deterministic enforcement — test gates, file protection |
| `~/.claude/rules/` | Auto-loaded practice rules every session |
| Sub-agents (`~/.claude/agents/`) | Code-reviewer with restricted read-only tool access |
| `model` field in frontmatter | Route review to Opus, routine tasks to Haiku |

**Implication for product brief:** Design each skill with a portable core (works everywhere) and Claude Code enhancements (works better with Claude Code). The dual-deployment model is additive, not a fork.

#### Finding 3: Three Tiers Map to Portability Layers

**Confidence: HIGH | Status: INFERRED (synthesis of enforcement tiers + skills spec capabilities)**

| Enforcement Tier | Portable (all tools) | Enhanced (Claude Code) |
|---|---|---|
| Tier 1 — Deterministic | Skill instructions say "run tests" | Hooks enforce it automatically |
| Tier 2 — Structured | Workflow steps in skill body | `context: fork` for isolation |
| Tier 3 — Advisory | `references/` loaded by skills | `~/.claude/rules/` auto-loaded every session |

This mapping means Momentum skills degrade gracefully: in Claude Code they get full enforcement; in other tools they get the same instructions without automatic enforcement. The philosophy is portable; the automation is Claude Code-specific [source: RESEARCH-SKILLS-PRELIM-001 §three-tiers-map, INFERRED].

**Implication for product brief:** Document the portability layer mapping. Each skill's SKILL.md should note which behaviors are portable and which require Claude Code.

### Recommended Changes

#### Philosophy

1. **Package as Agent Skills** — Momentum's deliverables are standard Agent Skills, not a proprietary module format. This is a product-level decision that affects every implementation task.
2. **Dual-deployment model** — portable skills for the ecosystem + Claude Code-specific supplements (rules, agents, hooks) for enhanced enforcement. One skill serves both audiences.

#### Process

1. **Redefine PT-021** (Momentum module) — the "module" is now a collection of Agent Skills + Claude Code supplements, not a BMAD custom module with shell script installer. The bootstrap workflow scaffolds project-specific config; the skills themselves are distributed via skills registries.
2. **Minimum viable skill set** — the PM should define which skills comprise "Momentum v0.1" — likely: `/validate`, practice rules (as a skill that installs to `~/.claude/rules/`), and the code-reviewer agent.

### Key Quantitative Data

| Claim | Value | Source | Status |
|---|---|---|---|
| Agent Skills adopter count | 15+ tools | agentskills.io specification | VERIFIED |
| skills.sh registry size | 83K+ skills | skills.sh | VERIFIED |
| skillsmp.com registry size | 96K+ skills | skillsmp.com | VERIFIED |
| SKILL.md startup token cost | ~100 tokens (metadata only) | Agent Skills spec | VERIFIED |

### Open Design Questions (for PM to resolve)

1. **Distribution channel:** Should Momentum skills be published to skills.sh? Distributed as a BMAD module that generates skills? Both?
2. **Dual-deployment packaging:** How do we handle the split between portable skills and Claude Code-specific content (`~/.claude/rules/`, `~/.claude/agents/`, hooks)?
3. **Minimum viable skill set:** What skills comprise "Momentum v0.1"? Proposed: `/validate`, practice rules, code-reviewer agent.
4. **ACP implications:** How does the Agent Client Protocol (JetBrains/Zed) affect the portability strategy? (Technical research in progress)

---

## Validation: The Validate-Fix-Loop as a Reusable Skill

### Research Methodology

This section synthesizes three sources: (1) the validate-fix-loop framework v3 [source: VFL-FRAMEWORK-V3, VERIFIED], a JSON document (~670 lines) defining a research-backed validation framework with dimension taxonomy, validation profiles, dual-reviewer system, scoring, and fix loop mechanics; (2) the VFL handoff document [source: VFL-HANDOFF-001, VERIFIED], which translates the framework into skill design recommendations and implementation considerations; and (3) design decisions reached through analyst review cross-referencing the VFL against the provenance research [source: RESEARCH-CONSOLIDATED-001], benchmarking research [source: RESEARCH-BENCHMARK-GUIDE-001], and existing Momentum practice plan [source: PLAN-SOLO-DEV-001].

The VFL framework draws from ISO 25010, Wang & Strong, Microsoft Azure AI Evaluation Metrics, DeepEval, and existing BMAD validation patterns [source: VFL-FRAMEWORK-V3 §sources, VERIFIED].

### The Problem

Momentum's practice plan defines a layered verification architecture: deterministic hooks (Tier 1), structured BMAD workflows (Tier 2), and advisory CLAUDE.md rules (Tier 3). Within Tier 2, the plan calls for adversarial sub-agents (PT-003 code-reviewer, PT-011 architecture-guard), BMAD Code Review (PT-006), and the Evaluation Flywheel. But these are separate mechanisms with no shared framework for:

- **What to validate** — each reviewer invents its own checklist. There is no shared dimensional taxonomy telling validators what to look for while letting the domain determine how.
- **How intensely to validate** — there is no concept of validation profiles. Every review gets the same treatment whether it's a quick structural sanity check or a final deliverable audit.
- **How to prevent validator hallucination** — the plan addresses producer hallucination extensively but does not address the problem of reviewers manufacturing findings. A false positive sends the fixer on a wild goose chase and wastes more time than a missed issue.
- **How to validate non-code artifacts** — the verification architecture is heavily code-centric (ATDD, code-reviewer, test automation). But BMAD workflows produce PRDs, architecture docs, research reports, UX specs, and product briefs that currently rely on ad-hoc review workflows with no unified quality framework.

The VFL framework fills all four gaps with a single reusable engine.

### What the VFL Framework Provides

The VFL v3 JSON [source: VFL-FRAMEWORK-V3, VERIFIED] is the complete framework definition. The VFL handoff document [source: VFL-HANDOFF-001] provides a concise architectural summary the PM should read before proceeding. Below is a brief orientation; the handoff has the full details.

**Core components:**
- **15-dimension validation taxonomy** (4 tiers: Universal → Compositional → Contextual → Domain-Specific) — defines WHAT to validate; validators derive domain-specific checks from these dimensions [source: VFL-FRAMEWORK-V3 §dimension_taxonomy, VERIFIED]
- **Three validation profiles** — gate (1 agent, pass/fail), checkpoint (1 per lens, 1 fix attempt), full (2 per lens with dual review, up to 4 fix iterations) [source: VFL-FRAMEWORK-V3 §validation_profiles, VERIFIED]
- **Staged application** ("bookend + critical gates") — gate at input/middle steps, checkpoint at first interpretation and penultimate step, full at final output [source: VFL-FRAMEWORK-V3 §staged_application, VERIFIED]
- **Dual-reviewer system** (full profile only) — Enumerator (systematic) + Adversary (skeptical) with cross-check confidence tagging [source: VFL-FRAMEWORK-V3 §dual_review, VERIFIED]
- **Calibration principles** — every finding requires evidence; no minimum quotas; conservative flagging; scope discipline [source: VFL-FRAMEWORK-V3 §calibration, VERIFIED]

For the dimension taxonomy details, validation profile specifications, scoring system, and domain variation examples, see VFL-HANDOFF-001.

### Key Findings

#### Finding 1: `/validate` Is a Full Loop Engine, Not a Single Pass

**Confidence: HIGH | Status: CITED (VFL-FRAMEWORK-V3 §validation_profiles, VFL-HANDOFF-001 §suggested-skill-design)**

The skill executes the complete validate-fix-loop cycle based on the profile parameter:

- **Gate**: validate once → pass or halt. Binary. No fix attempt.
- **Checkpoint**: validate → if issues found, send consolidated findings to fixer → one fix attempt → continue with warning. No re-validation.
- **Full**: validate → consolidate → score → if below 95, send findings to fixer → fixer fixes → re-validate → loop up to 4 iterations or until clean.

The fix loop is integral to the skill, not a separate mechanism. The **fixer** is the `domain_expert` — the same agent type that produced the output. This maintains the Producer-Verifier pattern: the skill orchestrates verification, then hands findings back to the producer type for remediation, then re-verifies [source: VFL-HANDOFF-001 §suggested-skill-design, VERIFIED, extended by analyst review].

**Implication for product brief:** `/validate` is a core skill that any workflow can invoke. It is not a review workflow — it is the engine underneath review workflows. The product brief should position it as foundational infrastructure, similar to how the reference format and staleness detection are foundational for provenance.

#### Finding 2: `domain_expert` Defines Agent Type, Not Model

**Confidence: HIGH | Status: INFERRED (analyst design decision, grounded in practice plan)**

The `domain_expert` parameter specifies the agent **type** — BMAD SM, BMAD Analyst, code-reviewer sub-agent, etc. — not the model. If a BMAD SM produced the output, a BMAD SM persona validates and a BMAD SM persona fixes. If a Claude Code sub-agent produced the code, the same type of sub-agent validates and fixes.

Model routing is a separate layer. The same BMAD SM persona can run on Sonnet for validation and Opus for escalated fixing. This separation means agent types are portable across model tiers, and model routing decisions can change without redefining agent roles [source: analyst review, INFERRED from practice plan's agent architecture + benchmarking research's model routing findings].

**Implication for product brief:** The skill's parameter design should separate "who validates" (agent type) from "what model runs the validation" (routing configuration). This allows model routing to be tuned independently via the model routing guide [source: MODEL-ROUTING-GUIDE-001] without changing skill invocations.

#### Finding 3: Model Routing Per Profile and Role

**Confidence: HIGH | Status: INFERRED (synthesized from benchmarking research + VFL design + traceability research constraints)**

Cross-referencing the benchmarking research's task-type-to-model mapping [source: RESEARCH-BENCHMARK-GUIDE-001 §1.4, VERIFIED], the cognitive hazard rule [source: RESEARCH-BENCHMARK-GUIDE-001 §3, CITED], the FrugalGPT cascade pattern [source: RESEARCH-BENCHMARK-GUIDE-001 §7.2, CITED], and the traceability research's constraint on citation verification model tier [source: RESEARCH-CONSOLIDATED-001 §part-6, CITED, arXiv:2509.08803], the following routing defaults emerge:

| Profile | Role | Model | Effort | Rationale |
|---|---|---|---|---|
| **Gate** | Structural validator | Haiku | low/N/A | Deterministic checks, well-constrained. Benchmarking guide: "Haiku for structural, Sonnet for semantic" |
| **Checkpoint** | Validators (1 per lens) | Sonnet | medium | Good reasoning at lower cost. Guide: "Code review / validation → Sonnet medium" |
| **Checkpoint** | Fixer | Producer's model tier | medium | Match producer — start where the output was generated |
| **Full** | Enumerator reviewers | Sonnet | medium | Systematic, mechanical — doesn't need flagship reasoning |
| **Full** | Adversary reviewers | Sonnet | high | Holistic reasoning needs deeper thinking; framing diversity (Meta-Judge) and model diversity (PoLL) both contribute to accuracy — Sonnet with high effort is the cost-efficient default, subject to empirical validation |
| **Full** | Consolidator | Opus | high | This is the intelligence step — dedup, cross-check confidence, false positive removal. Guide: "Multi-agent orchestrator → Opus high" |
| **Full** | Fixer (iterations 1-2) | Producer's model tier | medium | Start where the producer was; escalate to high effort if fix is complex |
| **Full** | Fixer (iterations 3-4) | Escalate one tier | high | FrugalGPT cascade — if not converging, escalate rather than burn tokens with growing context |

**Key constraint from traceability research:** "Do not use a smaller/cheaper model as citation verifier — the Dunning-Kruger effect for AI: smaller models are more confident in wrong answers" [source: RESEARCH-CONSOLIDATED-001 §part-6, CITED, arXiv:2509.08803]. This applies specifically to the **Factual Accuracy lens** — the lens that checks traceability and correctness. Haiku is fine for the Structural Integrity lens (checking "does this file exist"), but Sonnet minimum for any lens involving semantic judgment.

**Key insight from benchmarking research on escalation:** Each retry iteration is more expensive than the last due to context accumulation [source: RESEARCH-BENCHMARK-GUIDE-001 §7.2, CITED]. At iteration 3, the context includes the original output + 2 rounds of findings + 2 fix attempts. Escalating to a higher model tier at iteration 3 may be cheaper than running iterations 3 and 4 at the same tier, because the flagship model is more likely to converge in 1 iteration than the mid-tier model is to converge in 2 [source: RESEARCH-BENCHMARK-GUIDE-001 §7.2, INFERRED from convergence rate data].

**These are defaults, not prescriptions.** The routing should be configurable and eventually validated empirically via the benchmarking harness (PT-022). Two research findings are relevant: Meta-Judge (2025) showed different framings on same-model reviewers improve accuracy ~8pp absolute. PoLL (2024) showed cross-family model panels beat single flagships. The Sonnet dual-reviewer default leverages Meta-Judge's framing diversity finding; the PoLL cross-family benefit would require mixing model families (e.g., one Claude reviewer + one Gemini reviewer via MCP), which is a future optimization. Both are testable via the benchmarking harness (PT-022).

**Implication for product brief:** Model routing for `/validate` should be specified as configurable defaults informed by research, not hardcoded. The benchmarking harness should include `/validate` routing as one of its test configurations. Include effort levels as a first-class parameter — the cost difference between Opus at effort: low vs effort: high is significant ($25/MTok for thinking tokens).

#### Finding 4: Source Material Is Required at Checkpoint and Full

**Confidence: HIGH | Status: CITED (VFL-FRAMEWORK-V3 §parameters) + INFERRED (requirement recommendation from traceability research)**

The VFL framework v3 lists `source_material` as optional with a default of null [source: VFL-FRAMEWORK-V3 §parameters, VERIFIED]. The traceability research argues this should be **required** at checkpoint and full profiles: without source material, the traceability lens has nothing to check against, and reviewers are evaluating claims without ground truth — which is exactly where reviewer hallucination thrives [source: RESEARCH-CONSOLIDATED-001 §part-5, INFERRED].

At gate profile, source material remains optional — structural checks (does the JSON parse? are required fields present?) don't need ground truth.

The traceability research also provides specific guidance on what validators should do with source material at each profile:
- **Gate:** Verify cited files/sections exist (deterministic, <15ms) [source: RESEARCH-CONSOLIDATED-001 §part-3, CITED, arXiv:2603.10060]
- **Checkpoint:** Atomic claim decomposition at critical transitions — classify each claim as SOURCED / DERIVED / ADDED / UNSOURCED [source: RESEARCH-CONSOLIDATED-001 §part-3, VERIFIED]
- **Full:** Dual-reviewer traceability audit with cross-check. Enumerator mechanically verifies every citation. Adversary looks for "citation washing" (real source, misrepresented claim) [source: RESEARCH-CONSOLIDATED-001 §part-3, VERIFIED]

**Implication for product brief:** The VFL's `source_material` parameter should be required at checkpoint and full profiles. Workflows invoking `/validate` must pass the original source material through the pipeline — not lossy intermediate representations.

#### Finding 5: Provenance Status Integrates Into Finding Schema

**Confidence: HIGH | Status: INFERRED (design synthesis from traceability research + VFL finding schema)**

The traceability research produced a provenance status taxonomy (VERIFIED / CITED / INFERRED / UNGROUNDED / SUSPECT) [source: RESEARCH-CONSOLIDATED-001 §part-3, VERIFIED]. This integrates directly into the VFL's finding schema as an additional field. When a finding involves a traceability issue, the finding should carry the provenance status of the claim in question — enabling downstream consumers to understand not just "what's wrong" but "how grounded was this claim to begin with."

The VFL's existing finding schema has fields: id, severity, dimension, location, description, evidence, suggestion, confidence [source: VFL-FRAMEWORK-V3 §finding_schema, VERIFIED]. Adding `provenance_status` for traceability-dimension findings connects the validation system to the provenance system.

**Implication for product brief:** The findings template should include provenance status as an optional field, populated when the finding's dimension is traceability, cross_reference_integrity, or correctness.

#### Finding 6: The Findings Template Needs Standard + Open Sections

**Confidence: MEDIUM-HIGH | Status: INFERRED (analyst design decision)**

The `/validate` skill should output a structured findings report with:

**Standard sections (always present):**
- Score (0-100) and grade (Clean/Good/Fair/Poor/Failing)
- Findings array (per VFL finding_schema, sorted by severity)
- Fix loop summary (iterations attempted, score progression, convergence status)
- Profile used and lenses activated
- Source material provided (yes/no, with reference)

**Open domain-specific sections (present when relevant):**
- Domain context (what domain-specific rules were applied)
- Domain-specific recommendations (beyond individual findings)
- Domain-specific severity rationale (why a domain expert rated something as critical vs high)

This structure allows the skill to produce consistent, comparable output across domains while giving domain experts room to add context that doesn't fit the finding schema.

**Implication for product brief:** Define the findings template as a product deliverable. It is a reusable output format spec consumed by the findings ledger (PT-008), by workflows that invoke `/validate`, and by the Evaluation Flywheel when tracing upstream.

#### Finding 7: `/validate` Connects to Most Existing Backlog Items

**Confidence: HIGH | Status: VERIFIED (cross-reference against process-backlog.json)**

| Existing Item | Connection to `/validate` |
|---|---|
| **PT-003** (code-reviewer sub-agent) | May invoke `/validate` internally with code-specific lenses, or use VFL dimension taxonomy to structure its own assessment. Design decision for PT-003 spec. |
| **PT-006** (BMAD Code Review pure verifier) | VFL finding schema provides the structured output format the pure verifier needs. Workflow can invoke `/validate` at its assessment step. |
| **PT-008** (Findings ledger) | Ledger schema should align with VFL finding_schema. Add `provenance_status` field per traceability research. |
| **PT-009** (Quality Rules) | VFL dimension taxonomy is the universal quality framework. PT-009 provides project-specific supplements that feed into the Domain Fitness lens. |
| **PT-015** (Pipeline Orchestrator) | VFL staged application guidance ("bookend + critical gates") directly informs where the orchestrator places validation points and which profile to use at each stage. |
| **PT-016** (Cross-Model Verification) | VFL dual-reviewer research shows framing diversity captures most of the accuracy gain (~8pp absolute improvement). Cross-model verification may add incremental benefit on top of dual-framing, but is no longer a prerequisite for effective multi-reviewer validation. Reassess priority. |

New backlog items implied:

| New Item | Priority | Description |
|---|---|---|
| **PT-023, PT-027** | | See Consolidated New Backlog Items section (PT-023, PT-027). |

**Implication for product brief:** `/validate` is a high-priority deliverable that unblocks or enhances 6 existing backlog items. It should be positioned early in the implementation roadmap — after PT-001a (practice rules) but before PT-003 (code-reviewer) and PT-006 (BMAD Code Review), since both can be built on top of it.

### Recommended Changes

#### Philosophy

1. **Strengthen Producer-Verifier with the validation engine concept** — the practice plan describes Producer-Verifier as a principle. `/validate` is the reusable implementation of the Verifier role. Note that the verifier is not a single agent — it is an orchestrated system of agents with different framings, different lenses, and a fix loop. The principle remains the same; the implementation is now formalized.

2. **Add calibration as a quality principle** — the VFL's calibration section addresses a failure mode the plan doesn't: validators hallucinating findings. "Every finding requires evidence. A false positive wastes more time than a missed issue." This should be a stated principle, not just an implementation detail.

#### Process

1. **`/validate` skill** — new high-priority backlog item. The VFL JSON is the specification; the skill is the implementation that makes it invocable from any workflow or standalone.

2. **VFL source_material required** — update the VFL framework to make `source_material` required at checkpoint and full profiles. This is a one-line change to the JSON but a significant design commitment — it means every workflow that invokes `/validate` at checkpoint or full must carry original source material through the pipeline.

3. **Findings template** — define the standard + open section template as a canonical resource in `module/canonical/resources/`.

4. **Model routing defaults for `/validate`** — add to the model routing guide [source: MODEL-ROUTING-GUIDE-001] with the per-role routing table from Finding 3. Mark as "research-informed defaults, subject to empirical validation via benchmarking harness."

5. **Backlog integration** — update PT-003, PT-006, PT-008, PT-009, PT-015, PT-016 descriptions to reference `/validate` as a design input. Reassess PT-016 priority given dual-reviewer findings.

#### Tooling

| Tier | Artifact | Function |
|---|---|---|
| Core | `/validate` skill (Agent Skill format) | The engine — orchestrates sub-agents, consolidates, scores, runs fix loop |
| Core | VFL framework v3 JSON | The specification — dimension taxonomy, profiles, scoring, calibration (already exists) |
| Core | Findings template | Standard output format for validation reports |
| Support | Model routing config for `/validate` roles | Defaults in model routing guide; configurable per invocation |
| Support | Benchmarking config for `/validate` | Promptfoo test cases to validate routing defaults empirically |

### Key Quantitative Data

*Model routing cost data is in the Model Routing section. This table covers validation-specific findings only.*

| Claim | Value | Source | Status |
|---|---|---|---|
| Dual-reviewer accuracy improvement | ~8pp absolute (77.26% vs 68.89%) | Meta-Judge 2025, arXiv:2504.17087 | CITED |
| 3rd reviewer effect | Decreased to 65.38% | Meta-Judge 2025 | CITED |
| Error propagation from single upstream error | 73% downstream failure probability | Huang 2023, via VFL-FRAMEWORK-V3 | CITED |
| Late-stage error damage multiplier | 3.5x (step 4/4 vs step 2/4) | ASCoT 2025, arXiv:2508.05282 | CITED |
| Process Reward Models vs outcome-only | >8% more accurate, 1.5-5x more compute-efficient | PRM survey, arXiv:2510.08049 | CITED |
| Per-step accuracy degradation (8 steps at 90%) | 43% overall accuracy | Compounding error analysis, wand.ai | CITED |
| VFL pass threshold | 95/100 | VFL-FRAMEWORK-V3 §config | VERIFIED |
| VFL max iterations | 4 | VFL-FRAMEWORK-V3 §config | VERIFIED |
| Smaller model citation verification risk | Dunning-Kruger effect — more confident in wrong answers | arXiv:2509.08803 | CITED |

### Open Design Questions (for PM/Architect to resolve)

1. **Skill packaging:** Should `/validate` be an Agent Skill (portable, SKILL.md format) or a Claude Code sub-agent (`.claude/agents/`, with tool restrictions)? The preliminary findings [source: docs/research/preliminary-findings-momentum-as-skills-2026-03-13.md] argue for Agent Skills as the delivery format. But the skill needs to *spawn* sub-agents (validators, fixers), which may require Claude Code-specific orchestration. Can an Agent Skill spawn sub-agents? This is an architect question.

2. **Sub-agent orchestration mechanism:** Does the skill use Claude Code's Agent tool to spawn validators and fixers? Or does it use direct API calls (e.g., via Pydantic AI)? The Agent tool provides built-in isolation and tool restrictions; API calls provide more control over model selection and effort. This affects whether `/validate` is a pure Claude Code skill or has a code component.

3. **Benchmarking before locking defaults:** Should the model routing defaults in Finding 3 be treated as provisional until empirically validated via the benchmarking harness? If so, the initial implementation should make routing easily configurable (not hardcoded) and the benchmarking harness (PT-022) should include `/validate` routing as a priority test configuration.

4. **VFL version management:** The VFL JSON is currently v3.0.0. As findings from this handoff are incorporated (source_material required, provenance_status in finding schema, model routing defaults), should the JSON be updated to v3.1.0 or should the skill implementation extend the framework without modifying the JSON? The JSON is a research artifact; the skill is the implementation.

5. **Relationship to BMAD validation workflows:** BMAD already has adversarial review, editorial review, edge-case hunting, and traceability validation workflows. Should `/validate` *replace* these (it covers their concerns via lenses and dimensions) or *complement* them (they remain as standalone workflows that can optionally invoke `/validate` internally)? The BMAD workflows have established UX and menu integration; replacing them is higher-risk but cleaner architecturally.

---

## Research Process: Multi-Model MCP Integration and Repeatable Research Workflows

### Research Methodology

This section synthesizes two inputs: (1) a lessons-learned handoff from a multi-model benchmarking research session [source: HANDOFF-RESEARCH-LESSONS-001, VERIFIED] that catalogued 7 mistakes, 3 lessons, and proposed a 3-tier research process with prompt templates; and (2) original MCP integration research conducted by 1 research agent + 1 verification agent (Pass 1 verification, 16 claims checked: 12 VERIFIED, 3 CITED (corrected), 0 FABRICATED). The MCP research used web search against primary sources (GitHub repos, official docs, vendor pricing pages) on 2026-03-14.

### The Problem

Momentum's practice plan (§7.1.4) already specifies a hybrid research methodology: internal Claude research + external Gemini Deep Research, combined via synthesis. However, this workflow is currently **manual** — the user must copy prompts to Gemini's consumer UI, wait, and paste results back. This makes the hybrid approach:
- Too expensive (in human time) for light/medium research
- Impossible to automate as part of a BMAD workflow
- Dependent on the consumer Gemini UI rather than a programmable interface

The lessons-learned handoff [source: HANDOFF-RESEARCH-LESSONS-001] confirms the hybrid approach produces superior results (Lesson 1: "Gemini + Claude together > either alone") but also documents that the manual relay creates failure points (Mistake 4: no freshness scout; Mistake 7: no structured human checkpoint; Step 4: wasted relay step when Gemini proceeded without waiting).

Separately, the existing BMAD research workflows (`workflow-domain-research.md`, `workflow-market-research.md`, `workflow-technical-research.md`) are single-model, have no verification tier, no depth presets, and no date-anchoring enforcement — despite the practice plan (§7.1.3) requiring temporal focus. The gap between philosophy and implementation is significant.

### Key Findings

#### Finding 1: Multi-Model Research via MCP Is a Solved Problem

**Confidence: HIGH | Status: VERIFIED (GitHub repos, npm registry, official docs)**

Multiple mature MCP servers exist that wrap the Gemini and OpenAI APIs, installable with a single command from Claude Code:

| Server | Provider | Install | Tools | Status |
|---|---|---|---|---|
| `@rlabs-inc/gemini-mcp` | Gemini | `claude mcp add gemini -e GEMINI_API_KEY=key -- npx -y @rlabs-inc/gemini-mcp` | 37 (query, deep research, web search, code exec, doc analysis) | VERIFIED, npm v0.7.2 |
| `akiojin/openai-mcp-server` | OpenAI | Clone + build | 3 (chat_completion, list_models, generate_image) | VERIFIED, GitHub — defaults to GPT-4.1; GPT-5.4 (current flagship, released 2026-03-05) GPT-5.4 support: UNGROUNDED — not listed at time of research |
| `centminmod/gemini-cli-mcp-server` | Gemini + OpenRouter | Clone + build | 33 (includes 400+ model access via OpenRouter) | VERIFIED, GitHub |

Claude Code supports multiple simultaneous MCP servers with automatic Tool Search when many tools are loaded [source: Claude Code MCP docs, VERIFIED]. A research workflow can invoke both Gemini and OpenAI tools alongside Claude's native capabilities in a single session.

**Implication for product brief:** The hybrid research workflow (PT-020) is no longer blocked by manual relay. MCP integration transforms it from a manual process to a fully automatable BMAD workflow. This significantly changes its priority calculus.

#### Finding 2: Gemini Deep Research Is Programmable

**Confidence: HIGH | Status: CITED (with corrections — Interactions API confirmed; cost tier claim required clarification)**

Gemini Deep Research — the 90-source, multi-minute research capability that produced RESEARCH-BENCHMARK-GEMINI-001 — is available programmatically via the Interactions API (preview), powered by Gemini 3.1 Pro [source: Google AI docs, VERIFIED]. Cost: $2-$3/task (standard) or $3-$5/task (complex) [source: Google AI docs, CITED (corrected) — original research conflated the two tiers].

The `@rlabs-inc/gemini-mcp` server includes a Deep Research tool, meaning Claude Code could trigger a Gemini Deep Research session as an MCP tool call, wait for results, and integrate them — all without human intervention.

**Implication for product brief:** The "heavy" research depth preset from HANDOFF-RESEARCH-LESSONS-001 (currently requiring manual Gemini interaction at $0/task via consumer UI) could be automated at $2-$5/task via MCP. For the volume of research Momentum conducts, this is a negligible cost that buys significant automation.

#### Finding 3: Free-Tier Multi-Model Research Is Viable for Light/Medium Depth

**Confidence: HIGH | Status: VERIFIED (Google AI pricing docs)**

Gemini's free API tier provides:
- Gemini 2.5 Pro: 5 RPM, 100 requests/day [source: Google AI rate limits, VERIFIED]
- Gemini 2.5 Flash: 10 RPM, 250 requests/day [source: Google AI rate limits, VERIFIED]

A typical light research session (2-3 agents + 1 Gemini cross-check) consumes ~5 API calls. A medium session (4-5 agents + 2-3 Gemini queries) consumes ~10-15 calls. Both fit comfortably within the free tier's daily limits.

Paid tier pricing for supplementary queries:
- Gemini 2.5 Flash: ~$0.01/query (negligible)
- Gemini 2.5 Pro: ~$0.04/query
- GPT-5 Mini: ~$0.005/query [source: OpenAI pricing accessed 2026-03-14, VERIFIED] (GPT-5.4 is current flagship as of 2026-03-05; GPT-4.1 is now legacy)

**Implication for product brief:** Multi-model cross-checking is cheap enough to include by default in ALL research depths, not just "heavy." This fundamentally changes the economics of the 3-tier system proposed in HANDOFF-RESEARCH-LESSONS-001.

#### Finding 4: The Gemini CLI Subagent Pattern Is an Alternative to MCP

**Confidence: HIGH | Status: VERIFIED (documented tutorials)**

An alternative to MCP servers: create a Claude Code subagent file (e.g., `.claude/agents/gemini-researcher.md`) that invokes the Gemini CLI via Bash tool [source: egghead.io tutorial, aicodingtools.blog, VERIFIED]. This leverages Gemini's 1M token context window for large-context analysis.

Trade-offs vs MCP:

| Dimension | MCP Server | CLI Subagent |
|---|---|---|
| Setup | `claude mcp add` (one command) | Create agent markdown file |
| Tool integration | Native MCP tool calls | Bash command wrapping |
| Streaming | Supported | Not supported |
| Conversation management | Built into server | Manual |
| Dependency | npm package | Gemini CLI installed |
| Flexibility | Fixed tool set | Arbitrary prompts |

**Implication for product brief:** MCP is the better default for structured research workflows. The CLI subagent pattern may be useful for ad-hoc, exploratory research where the prompt structure isn't predetermined.

#### Finding 5: MCP Is Now Industry-Standard Infrastructure

**Confidence: HIGH | Status: VERIFIED (multiple primary sources)**

MCP has achieved critical mass as an interoperability standard:
- **March 2025:** OpenAI adopted MCP across Agents SDK, Responses API, ChatGPT desktop [source: Sam Altman tweet + TechCrunch, VERIFIED]
- **December 2025:** Anthropic donated MCP to the Agentic AI Foundation (Linux Foundation), co-founded by Anthropic, Block, and OpenAI as founding contributors [source: Linux Foundation press release, VERIFIED — date was Dec 9, 2025]
- **December 2025:** Google launched managed MCP servers for Cloud services (Maps, BigQuery, GCE, GKE) [source: TechCrunch, VERIFIED — Dec 10, 2025]

This means investing in MCP-based tooling is not a bet on a niche protocol — it's building on the shared infrastructure layer that all major AI providers have committed to.

**Implication for product brief:** MCP integration should be treated as core infrastructure, not an optional enhancement. It enables not just multi-model research but any future tool integration across the Momentum practice.

#### Finding 6: Research Process Lessons Are Implementation Details, Not Philosophy Changes

**Confidence: HIGH | Status: INFERRED (cross-reference of HANDOFF-RESEARCH-LESSONS-001 against PLAN-SOLO-DEV-001)**

Cross-referencing the 7 mistakes and 3 lessons from HANDOFF-RESEARCH-LESSONS-001 against Momentum's practice plan:

| Handoff Item | Already in Practice Plan? | Gap |
|---|---|---|
| Date anchoring (Mistakes 1-2, Lesson 3) | Yes — Temporal Focus rules, §7.1.3 | Implementation: research workflow prompts don't enforce it yet |
| Primary source verification (Mistake 3) | Partially — validate-fix-loop exists | Implementation: no "primary source" directive in research prompts |
| Non-overlapping agent topics (Mistake 4) | No | New: scoping step needed in research workflow |
| Treat external model output as unverified (Mistake 5) | No | New: source-tagging during consolidation |
| Two-pass verification (Mistake 6) | No | New: Pass 1 fact-check before consolidation, distinct from full VFL |
| Human checkpoint before consolidation (Mistake 7) | Conceptually yes | Implementation: not structured or mandatory |
| Hybrid research (Lesson 1) | Yes — §7.1.4 | Implementation: manual-only, no automation |
| Freshness lens for VFL (Lesson 2) | No | New: domain-specific validation lens |
| Freshness scout agent (Mistake 4 fix) | No | New: dedicated agent role for "what changed in 30 days" |

**No philosophy changes required.** Three genuinely new process concepts to absorb: two-pass verification, freshness scout role, and source-tagging. Everything else is implementation catch-up to existing philosophy.

**Implication for product brief:** The product brief should specify these three new concepts as process requirements. The research workflow (PT-020) should implement them alongside MCP integration.

### Recommended Changes

#### Philosophy

No changes. The practice plan's research philosophy (Temporal Focus, Hybrid Research, Impermanence Principle, Evaluation Flywheel) already covers the conceptual ground. The lessons learned validate the philosophy — the gap was in implementation, not thinking.

#### Process

1. **Elevate PT-020 (Hybrid Research Workflow) priority** — MCP integration removes the manual relay bottleneck. The workflow becomes: scope topics → launch parallel Claude research agents → launch parallel Gemini/GPT queries via MCP → Pass 1 verification → human checkpoint → consolidate → Pass 2 VFL validation. All automatable except the human checkpoint.

2. **Add 3-tier depth presets to research workflows** — Light (2-3 agents, Gemini cross-check via free tier, Pass 1 only, ~15-20min), Medium (4-5 agents + freshness scout, Gemini queries, Pass 1 + optional Pass 2, human checkpoint optional, ~30-45min), Heavy (6+ agents + freshness scout, Gemini Deep Research via Interactions API, Pass 1 + Pass 2 with freshness mandate, human checkpoint mandatory, ~60-90min). [source: HANDOFF-RESEARCH-LESSONS-001 §depth-presets, adapted with MCP integration]

3. **Add two-pass verification to VFL framework** — Pass 1 (fact-check): runs after research, before consolidation; focused on correctness + traceability; tags claims as VERIFIED/OUTDATED/FABRICATED/UNVERIFIABLE. Pass 2 (full VFL validation): runs after consolidation; all lenses including freshness for tech/AI topics. [source: HANDOFF-RESEARCH-LESSONS-001 §mistake-6]

4. **Formalize freshness scout as a canonical agent role** — Dedicated agent whose sole job is "what changed in the last 30 days in {domain}?" Deployed for tech/AI research at medium and heavy depths. [source: HANDOFF-RESEARCH-LESSONS-001 §mistake-4-fix]

5. **Enforce date-anchoring in research prompt templates** — Every research agent prompt includes `TODAY'S DATE: {date}` and instructions to cite source dates, verify currency, flag unverifiable claims. [source: HANDOFF-RESEARCH-LESSONS-001 §research-agent-prompt-template]

6. **Add source-tagging during consolidation** — Tag each claim's origin (internal research / Gemini / GPT / user input) so verifiers know what to scrutinize and the provenance chain remains navigable. [source: HANDOFF-RESEARCH-LESSONS-001 §mistake-5-fix]

#### Tooling

| Priority | Item | Description |
|---|---|---|
| **High** | Gemini MCP server | Install `@rlabs-inc/gemini-mcp` at user scope; add to Momentum bootstrap workflow |
| **High** | Research prompt templates | Canonical templates with date-anchoring, primary-source directives, non-overlap boundaries |
| **High** | Freshness scout agent | Canonical agent template in `module/canonical/agents/` |
| **Medium** | OpenAI MCP server | Install `akiojin/openai-mcp-server` for multi-model verification. GPT-5.4 is the current flagship (2026-03-05, $2.50/$15.00 per MTok); GPT-5 Mini ($0.125/$1.00) is cost-effective for cross-checks. Community MCP servers lag behind OpenAI releases — verify model ID support before relying on hardcoded lists. |
| **Medium** | Verification agent template | Canonical template for Pass 1 fact-checking |
| **Low** | Gemini Deep Research automation | Wrap Interactions API calls in research workflow for heavy-depth preset |
| **Low** | OpenRouter MCP | `centminmod/gemini-cli-mcp-server` for access to 400+ models; useful for benchmarking |

### Key Quantitative Data

| Claim | Value | Source | Status |
|---|---|---|---|
| Gemini MCP server tools available | 37 | @rlabs-inc/gemini-mcp npm registry | VERIFIED |
| Gemini Deep Research API cost (standard) | $2-$3/task | Google AI docs (Interactions API) | VERIFIED |
| Gemini Deep Research API cost (complex) | $3-$5/task | Google AI docs (Interactions API) | VERIFIED |
| Gemini 2.5 Flash free tier | 10 RPM, 250 RPD | Google AI rate limits | VERIFIED |
| Gemini 2.5 Pro free tier | 5 RPM, 100 RPD | Google AI rate limits | VERIFIED |
| Gemini 2.5 Flash per-query cost | ~$0.01 | Google AI pricing | VERIFIED |
| GPT-5 Mini per-query cost | ~$0.005 | OpenAI pricing (accessed 2026-03-14) | VERIFIED |
| GPT-5.4 flagship pricing | $2.50 input / $15.00 output per MTok | OpenAI pricing (accessed 2026-03-14) | VERIFIED |
| GPT-5.4 release date | 2026-03-05 | OpenAI announcement | VERIFIED |
| MCP donated to Linux Foundation | Dec 9, 2025 | Linux Foundation press release | VERIFIED |
| OpenAI MCP adoption | March 26, 2025 | Sam Altman tweet, TechCrunch | VERIFIED |
| Google managed MCP servers launch | Dec 10, 2025 | TechCrunch, SiliconANGLE | VERIFIED |
| Claude Code MAX_MCP_OUTPUT_TOKENS default | 25,000 tokens | Claude Code MCP docs | VERIFIED |
| Research mistakes caught by Pass 1 verification | 8 (before consolidation) | HANDOFF-RESEARCH-LESSONS-001 | VERIFIED |
| Verification results (this section's research) | 12 VERIFIED, 3 CITED (corrected), 0 FABRICATED | Pass 1 verification, 16 claims | VERIFIED |

### Open Design Questions (for PM to resolve in product brief)

1. **MCP server scope:** Should Gemini/OpenAI MCP servers be installed at user scope (available everywhere) or project scope (per-project `.mcp.json`)? User scope is simpler; project scope enables team sharing.

2. **Cost governance:** With automated multi-model queries, research sessions accumulate API costs across providers. Should there be a cost cap or budget parameter per research session?

3. **Gemini Deep Research: API vs consumer UI?** The API costs $2-$5/task but enables automation. The consumer UI is "free" (within Gemini Advanced subscription) but requires manual relay. Should the heavy depth preset default to API (automation) or offer both paths?

4. **Human checkpoint UX:** The lessons handoff recommends a mandatory human checkpoint at heavy depth. In a BMAD workflow, what does this look like? A pause with a summary table? A separate approval step?

5. **VFL pass parameter:** Should two-pass verification be a modification to the existing VFL framework (adding a `pass: 1|2` parameter) or a separate "research verification" resource? The former is cleaner architecturally; the latter avoids scope creep on VFL.

6. **Multi-model verification pattern:** Should verification agents use a *different* model than the research agents? (e.g., Gemini verifies Claude's claims, Claude verifies Gemini's claims.) The lessons handoff's Mistake 5 suggests this has value, but it adds complexity and cost.

7. **Freshness scout frequency:** At medium depth, the freshness scout runs once. At heavy depth, should it run again before Pass 2 validation (to catch things that changed *during* the research session, as happened with Gemini 3.x)?

---

## Consolidated New Backlog Items

All new process tasks recommended by this handoff, with proposed IDs continuing from the current highest (PT-022). The PM should formalize these in `process-backlog.json` with full field sets (scope, agents, source, planReference, created).

| ID | Priority | Description | Source Section |
|---|---|---|---|
| **PT-023** | High | `/validate` skill — Build as Agent Skill. Implements full VFL validate-fix-loop cycle (gate/checkpoint/full profiles). Parameters: profile, domain_expert, task_context, output_to_validate, source_material, validation_focus. Configurable model routing with research-informed defaults. | Validation |
| **PT-024** | High | Traceability infrastructure — stable document IDs, `derives_from` in spec templates, reference scanner generating `_references.yml`, deterministic link validator. | Provenance |
| **PT-025** | Medium | Staleness detection — content hash comparison via git blob SHAs, suspect link reporter, pull-based staleness status. | Provenance |
| **PT-026** | Medium | Citations API + CoE integration — wire Anthropic Citations API into spec generation workflows, add Chain of Evidences prompting pattern. | Provenance |
| **PT-027** | Medium | Benchmarking config for `/validate` — Promptfoo test cases to empirically validate model routing defaults per profile/role. Part of PT-022 benchmarking harness. | Validation |
| **PT-028** | Medium | Gemini MCP server — install `@rlabs-inc/gemini-mcp` at user scope; add to bootstrap workflow. | Research Process |
| **PT-029** | Low | Research prompt templates — canonical templates with date-anchoring, primary-source directives, non-overlap boundaries, freshness scout role. | Research Process |

**Modifications to existing items:**

| ID | Change | Source Section |
|---|---|---|
| **PT-003** | Add note: may invoke `/validate` internally or use VFL dimension taxonomy | Validation |
| **PT-006** | Add note: VFL finding schema provides structured output format | Validation |
| **PT-008** | Add `provenance_status` field to ledger schema | Validation |
| **PT-009** | Note: VFL dimension taxonomy is the universal quality framework; PT-009 supplements it | Validation |
| **PT-015** | VFL staged application guides validation checkpoint placement | Validation |
| **PT-016** | [DONE] Elevated to high priority, renamed "Model Routing Strategy" | Model Routing |
| **PT-020** | Elevate priority — MCP removes manual relay bottleneck | Research Process |
| **PT-021** | Redefine as Agent Skills collection + Claude Code supplements (not BMAD custom module) | Skills Strategy |

---

## Source Document Index

### Provenance Research (produced 2026-03-14)

| ID | Document | Agent Framing | Key Focus |
|---|---|---|---|
| RESEARCH-REF-FORMAT-ENUM-001 | [technical-bidirectional-document-references-2026-03-14.md](technical-bidirectional-document-references-2026-03-14.md) | Enumerator | Citation formats, metadata standards, Crossref/SARA patterns, Citations API |
| RESEARCH-REF-FORMAT-ADV-001 | [bidirectional-reference-formats-failure-modes-2026-03-14.md](bidirectional-reference-formats-failure-modes-2026-03-14.md) | Adversary | Link rot, granularity tradeoffs, RTM death spiral, authoring friction |
| RESEARCH-CHANGE-PROP-ENUM-001 | [technical-change-propagation-patterns-2026-03-14.md](technical-change-propagation-patterns-2026-03-14.md) | Enumerator | DOORS suspect links, dependency DAGs, staleness detection, spec-chain.json |
| RESEARCH-CHANGE-PROP-ADV-001 | [change-propagation-failure-modes-2026-03-14.md](change-propagation-failure-modes-2026-03-14.md) | Adversary | Cascading storms, error accumulation, notification fatigue, good-enough problem |
| RESEARCH-ANTI-HALLUC-ENUM-001 | [anti-hallucination-source-provenance-2026-03-14.md](anti-hallucination-source-provenance-2026-03-14.md) | Enumerator | RAG attribution, Citations API, CoE prompting, W3C PROV, fact-checking pipelines |
| RESEARCH-ANTI-HALLUC-ADV-001 | [anti-hallucination-source-provenance-limitations-2026-03-14.md](anti-hallucination-source-provenance-limitations-2026-03-14.md) | Adversary | Citation hallucination rates, false grounding, provenance theater, verification paradox |
| RESEARCH-CONSOLIDATED-001 | [consolidated-reference-traceability-research-2026-03-14.md](consolidated-reference-traceability-research-2026-03-14.md) | Cross-checked synthesis | Unified architecture, principle stack, DO/DON'T recommendations |

### Multi-Model Benchmarking Research (produced 2026-03-13/14)

| ID | Document | Key Focus |
|---|---|---|
| RESEARCH-BENCHMARK-GUIDE-001 | [multi-model-benchmarking-guide-2026-03-13.md](multi-model-benchmarking-guide-2026-03-13.md) | Consolidated guide: model selection, effort levels, cognitive load, eval tooling, Claude Code/Pydantic AI specifics, testing methodology, quick reference |
| RESEARCH-BENCHMARK-GEMINI-001 | [multi-model-benchmarking-gemini-initial-2026-03-13.md](multi-model-benchmarking-gemini-initial-2026-03-13.md) | Gemini Deep Research initial survey (90 sources) |
| RESEARCH-BENCHMARK-GEMINI-002 | [multi-model-benchmarking-gemini-followup-2026-03-13.md](multi-model-benchmarking-gemini-followup-2026-03-13.md) | Follow-up: cognitive load, promptfoo SDK, loop economics, observability |
| RESEARCH-BENCHMARK-HANDOFF-001 | [multi-model-benchmarking-handoff-2026-03-14.md](multi-model-benchmarking-handoff-2026-03-14.md) | Implementation handoff: 5 concrete deliverables for momentum |
| MODEL-ROUTING-GUIDE-001 | [model-routing-guide.md](../../module/canonical/resources/model-routing-guide.md) | Condensed decision matrix, cognitive hazard rule, effort levels, cost comparison |

### Skills Strategy (produced 2026-03-13)

| ID | Document | Key Focus |
|---|---|---|
| RESEARCH-SKILLS-PRELIM-001 | [preliminary-findings-momentum-as-skills-2026-03-13.md](preliminary-findings-momentum-as-skills-2026-03-13.md) | Agent Skills packaging, portability layers, Claude Code enhancements, BMAD relationship |

### Research Process and MCP Integration (produced 2026-03-14)

| ID | Document | Key Focus |
|---|---|---|
| HANDOFF-RESEARCH-LESSONS-001 | [Research-Process-Lessons-Learned-Handoff.md](/Users/steve/projects/game-prep/docs/research/Research-Process-Lessons-Learned-Handoff.md) | 7 mistakes, 3 lessons, 3-tier depth system, prompt templates from multi-model benchmarking session. *Note: Cross-project reference (game-prep repo) — copy to momentum/docs/research/ if this document becomes a frequent citation target* |

### Upstream Dependencies (pre-existing)

| ID | Document | Relationship |
|---|---|---|
| VFL-FRAMEWORK-V3 | [validate-fix-loop-framework-v3.json](validate-fix-loop-framework-v3.json) | depends_on — validation methodology |
| PLAN-SOLO-DEV-001 | [AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md](../planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md) | depends_on — philosophy, process, implementation context |
| VFL-HANDOFF-001 | [validate-fix-loop-handoff.md](validate-fix-loop-handoff.md) | depends_on — VFL implementation context |
| VFL-REFERENCES-001 | [validate-fix-loop-references.md](validate-fix-loop-references.md) | depends_on — VFL source citations |
