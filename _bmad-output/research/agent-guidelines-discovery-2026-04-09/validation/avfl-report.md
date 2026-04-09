---
validation_type: AVFL
corpus: agent-guidelines-discovery-2026-04-09
validator: claude-sonnet-4-6
date: 2026-04-09
---

# AVFL Validation Report — Agent Guidelines Discovery Research Corpus

**Overall Score: 62 / 100**

Score reflects: 1 confirmed factual contradiction (C2 self-contradicts on -3% vs -0.5/-2%), 2 potentially hallucinated model names in C1, 1 unsupported claim (B2 Chroma study), 1 unsupported sweeping attribution claim (B2 70% error figure), 1 currency flag (A2 Context7 release date same as research date), and 1 generalizability flag (C2 positive framing citation from safety context). No cross-pair contradictions that destroy conclusions, but the internal C2 contradiction is a real accuracy problem and the model names in C1 are a credibility risk.

---

## ACCURACY Findings

### ACC-1 — CRITICAL: C2 self-contradicts on the -3% figure
**Files:** lens-c2-determining-factors.md (Section 1) vs. lens-c2-determining-factors.md (Cross-Cutting Summary Table)
**Finding:** In the same document, C2 reports two different values for the ETH Zurich finding on LLM-generated guidelines:
- Section 1, first bullet: "LLM-generated: -3% success rate (note: C1 found actual values are -0.5% SWE-bench and -2% AGENTbench)"
- Cross-Cutting Summary Table row "LLM-generated vs. human-written": correctly states "-0.5-2%"

The parenthetical acknowledgment in Section 1 confirms the agent was aware of the discrepancy but retained the wrong number in the body text rather than correcting it. This is not a rounding difference — "-3%" rounds up both benchmarks together in a way that overstates both measured effects. The correct values are -0.5% and -2% per C1's direct reading of arXiv:2602.11988.

**This is the same error that C1 explicitly corrects from the prior corpus.** C2 repeats the corrected figure in its summary table while retaining the erroneous figure in its body text — meaning a downstream reader who reads Section 1 without reading the table will leave with the wrong number.

**Recommended fix:** Replace "-3% success rate" in C2 Section 1 body text with "-0.5% on SWE-bench Lite and -2% on AGENTbench". Remove the parenthetical correction and make the body text accurate directly.

---

### ACC-2 — HIGH: C1 cites suspicious model names for ETH Zurich study agents
**File:** lens-c1-guidelines-quality-study.md (Section 3, "Agents / Models tested")
**Finding:** C1 lists the following models as tested in the ETH Zurich study:
- "Claude Code with Sonnet 4.5" — non-standard model designation
- "Codex with GPT-5.2 and GPT-5.1 mini" — "GPT-5.2" and "GPT-5.1 mini" do not match any documented OpenAI model naming convention

"GPT-5.2" is not a known model. OpenAI's naming convention uses "GPT-4o", "GPT-4o mini", "o1", "o3" — not decimal-suffixed GPT-5 variants. "Codex" as an agent product name was retired by OpenAI in 2022, though OpenAI released a new "Codex" agent CLI in 2025. The model names "GPT-5.2" and "GPT-5.1 mini" are highly suspicious and may be fabricated or hallucinated by the C1 research agent.

The ETH Zurich paper was submitted February 12, 2026. If these model names appear in the actual paper, they would be frontier models; if they do not, C1 has hallucinated the model specifications for the study it is reporting on — a critical accuracy problem.

**Recommended fix:** The actual model names used in arXiv:2602.11988 must be verified against the paper directly. Until verified, these model names should be presented as "models unverified — see paper" rather than stated as fact.

---

### ACC-3 — MEDIUM: B2 attributes empirical findings to "Chroma 2025 study" without citation
**File:** lens-b2-context-engineering-ecosystem.md (Section 4, "Context rot problem")
**Finding:** "Chroma 2025 study testing 18 frontier models found every model performed worse as context length increased, some dropping from 95% to 60% accuracy past a threshold."

No arXiv ID, URL, paper title, or author is provided. The claim is specific (18 models, 95% to 60% drop) — specific enough to appear to be citing a real paper — but no citation is given. "Chroma" as an organization primarily produces a vector database product; it is unclear whether they published a formal study meeting research standards or whether this refers to a blog post, technical report, or informal benchmark. Without a citation, this claim cannot be verified or attributed.

**Recommended fix:** Add the full citation (paper title, URL, or arXiv ID). If this is a blog post or technical report rather than a peer-reviewed study, downgrade the framing accordingly.

---

### ACC-4 — MEDIUM: B2 cites "over 70% error attribution" to "multiple sources" without any citation
**File:** lens-b2-context-engineering-ecosystem.md (Section 4)
**Finding:** "Multiple 2025-2026 sources cite that over 70% of errors in production LLM applications stem from incomplete, irrelevant, or poorly structured context — not insufficient model capability."

No citation is provided. "Multiple sources" is not a citation. This claim is used to validate the context engineering framing and appears as empirical grounding, but without citations it is anecdotal. The specific "70%" figure implies measurement — if it comes from a survey, a benchmark study, or a vendor report, that provenance matters for assessing reliability.

**Recommended fix:** Either supply citations for the specific sources being referenced, or reframe as practitioner consensus with appropriate confidence downgrade (e.g., "Practitioner framing" rather than "empirical result").

---

## CONSISTENCY Findings

### CON-1 — HIGH: C2 Section 1 body text contradicts C1's explicit correction (cross-lens consistency failure within Pair C)
**Files:** lens-c1-guidelines-quality-study.md (Section 2, "What the Paper Actually Found") vs. lens-c2-determining-factors.md (Section 1)
**Finding:** C1 is entirely organized around correcting the -3% figure from the prior corpus. Its Section 2 header is "What the Paper Actually Found (vs. the Prior Corpus Claim)" and explicitly states "The prior corpus claim was WRONG." C2 then opens Section 1 by citing "-3%" — the exact wrong figure C1 corrected — in the body text of the same lens pair.

The two agents in Pair C contradict each other on the primary corrective finding of the pair. This is a consistency failure at the pair level. A reader synthesizing C1 and C2 without reading carefully would encounter conflicting signals about whether the correct figure is -3%, -0.5%, or -2%.

This is also structurally related to ACC-1 — the same error appears in both the accuracy and consistency registers.

**Recommended fix:** Same as ACC-1. The body text of C2 Section 1 must be corrected.

---

### CON-2 — MEDIUM: B1 and B2 present the Karpathy wiki model with different framing that could mislead synthesis readers
**Files:** lens-b1-karpathy-direct.md vs. lens-b2-context-engineering-ecosystem.md
**Finding:** B1 concludes: "The most actionable takeaway: The knowledge delivery format should be pre-synthesized, not raw. Store as a maintained wiki where 'use X not Y' decisions are already baked in, organized for index-first navigation. The agent reads the index, identifies relevant pages, reads synthesized content — never re-derives the convention from raw material."

B2 explicitly diverges: "Critical divergence from Karpathy: Production systems universally split knowledge into hot (always-loaded) and cold (on-demand retrieved) tiers. Karpathy's flat wiki is the right mental model for personal knowledge management but does NOT map directly to agent context engineering, where token budget pressure forces selective loading."

These framings are not contradictory at the factual level — B2 is making a valid critique of direct extrapolation from B1's findings. However, B1's synthesis section does not acknowledge this limitation at all. A reader of B1 in isolation receives an unqualified recommendation to adopt the wiki model; the critical caveat about hot/cold split is only in B2. For a corpus that is being synthesized together, this asymmetry is a consistency issue: the limitation of B1's recommendations is not flagged in B1.

**Recommended fix:** B1's synthesis section should add a caveat: "Note: direct application of this model to agent context delivery requires a hot/cold split — see context engineering ecosystem research for production architecture constraints."

---

### CON-3 — LOW: B2 describes Codified Context with 19 specialist agents; claim is internally consistent but unusually specific
**File:** lens-b2-context-engineering-ecosystem.md (Section 1)
**Finding:** B2 states Tier 2 has "19 domain-expert agent specifications (~9,300 lines total)." The 9,300 / 19 ratio gives ~490 lines per agent specification. B2 also says "more than half of each agent's content is domain knowledge, not behavioral instruction" — so ~245+ lines of domain knowledge per agent. This is internally consistent.

The paper is real (arXiv:2602.20478) and these numbers should appear in the paper. No contradiction identified, but the precision (19 agents, 9,300 lines, 34 documents, 16,250 lines, 26,200 lines overhead) warrants noting that these figures have not been independently verified by the validation pass. Flagged for awareness, not as a finding requiring correction.

**Recommended fix:** None required. Note for future verification against source paper.

---

## CURRENCY Findings

### CUR-1 — HIGH: A2 cites Context7 "latest release April 9, 2026" — same date as research
**File:** lens-a2-llm-doc-tooling.md (Section 1, Context7 entry)
**Finding:** "52,100 stars, latest release April 9, 2026 — actively maintained"

The research corpus is dated April 9, 2026. A tool having its latest release on the exact same day the research was conducted is possible but suspicious — it could mean the agent captured a release that happened hours before the research was written, or it could mean the agent echoed back the research date when reporting the tool's release date. Star counts (52,100) and release dates for GitHub repositories can change rapidly; this figure was current at most as of the moment of the research query and may already be stale.

More importantly: if the "April 9, 2026" release date is fabricated (the agent filled in today's date), it undermines the credibility of the "actively maintained" characterization.

**Recommended fix:** Verify the actual latest release date from github.com/upstash/context7/releases independently of the research agent's output. If the date is accurate, note it with a "as of research date" qualifier. If fabricated, correct and restate maintenance status from verifiable evidence.

---

### CUR-2 — LOW: A1 and A2 report kotlinlang.org llms.txt coverage "as of April 2026" — generally acceptable
**Files:** lens-a1-llm-doc-standards.md, lens-a2-llm-doc-tooling.md
**Finding:** Both lenses report live URL verification for kotlinlang.org (200 responses, specific file counts). A2 states "47 dedicated entries" for Compose Multiplatform and "80+ entries" for KMP. These figures are consistent between lenses and the currency limitation is appropriately framed ("as of April 2026"). No issue with the framing; the limitation is documented.

**No fix required.** Flagged for completeness.

---

## UNSUPPORTED Findings

### UNS-1 — HIGH: C2 cites arXiv:2506.02357 for positive vs. negative framing claim; generalizability to coding guidelines is not established
**File:** lens-c2-determining-factors.md (Section 2, "Markdown vs. XML" and Cross-Cutting Summary Table)
**Finding:** C2 cites "Positive vs. negative framing — Positive achieves 'near-perfect adherence' vs. high variance for negative" with source "arXiv:2506.02357" and confidence "Medium — safety context."

C2 correctly flags the safety-context limitation ("Medium — safety context"). However, the finding appears in the summary table without any body text explaining what the paper actually studied or why the safety context limitation applies. A reader consulting the summary table only sees the claim and the "Medium" confidence — not the critical caveat that the study was conducted in a safety/alignment context where instruction-following dynamics may differ substantially from software engineering task contexts.

The paper arXiv:2506.02357 (June 2025 by arXiv numbering) is cited without a title, author, or institution — making it impossible to assess without looking it up. In a corpus where other citations include full titles and institutions, this is an outlier.

**Recommended fix:** Add a brief note in Section 2 (not just the summary table) explaining the paper's context, what "positive framing" means in it, and why generalization to coding agent guidelines may or may not hold. The summary table confidence notation is appropriate but insufficient on its own.

---

### UNS-2 — MEDIUM: C2 states ~95 tokens achieves "near-optimal accuracy gains" — claim needs precision
**File:** lens-c2-determining-factors.md (Section 3)
**Finding:** "~95 tokens of 'API Description + Specification' achieves near-optimal accuracy gains vs. 685 tokens for full documentation."

The Amazon Science paper (arXiv:2407.09726) is cited as the source, and the claim is supported. However, the corpus should acknowledge that:
1. This finding is specific to API accuracy tasks in the Amazon Science setup, not generalized across task types
2. "Near-optimal" is a relative claim — near-optimal relative to 685 tokens, but this doesn't establish 95 tokens as a global sweet spot for all content types in agent guidelines
3. The 95-token figure appears in the specificity section with strong framing but lacks the caveat that it was measured on API signature tasks specifically

C1 does not mention this 95-token figure at all, even though C1 covers the same ETH Zurich study domain. The figure originates in the Amazon Science paper which is a C2 source. This is not a contradiction but a completeness gap — the C pair doesn't cross-validate this specific finding.

**Recommended fix:** Add a scoping sentence: "This 95-token efficiency finding applies specifically to API function specification tasks; the optimal token budget for other content types (architectural constraints, build commands, testing requirements) has not been empirically established."

---

### UNS-3 — LOW: B2's ACE Framework results (+10.6%, +8.6%, 82-92%) cited from arXiv:2510.04618 without paper title or author
**File:** lens-b2-context-engineering-ecosystem.md (Section 3)
**Finding:** The ACE Framework results are specific and quantitative but cited only by arXiv ID without title, author, or institution. The ID resolves to October 2025. The claim is specific enough to be verifiable but the citation format is less complete than other citations in the corpus. Not a blocking issue — the arXiv ID is sufficient for lookup — but inconsistent with citation standards elsewhere in the corpus.

**Recommended fix:** Add paper title and primary author to the ACE Framework citation for consistency with other citations.

---

## Cross-Lens Integration Assessment

### Pair A (A1 + A2) — CONSISTENT
A1 and A2 are well-integrated. Both verify kotlinlang.org (200 responses, consistent coverage claims). A1 establishes the two-file pattern (llms.txt + llms-full.txt); A2 confirms it and applies it to the specific Kotlin/CMP sourcing problem. A2's finding that Compose Multiplatform-specific llms.txt returns 404 is consistent with A1's more general treatment. No contradictions found within Pair A.

### Pair B (B1 + B2) — CONSISTENT WITH CAVEAT
B1 and B2 cover different aspects of the same ecosystem and do not directly contradict on facts. B2 explicitly acknowledges B1's model and explains why direct application to agent context delivery requires adaptation (hot/cold split). The critical divergence is flagged and is a valid finding, not a contradiction. The caveat noted in CON-2 — that B1's synthesis does not acknowledge this limitation — is a presentation issue rather than a factual error.

The conceptual link B2 draws between Karpathy's Ingest/Lint operations and "sleep-time compute" is consistent with B1's description of those same operations as "compilation." B2 adds the empirical grounding from the sleep-time compute paper (arXiv:2504.13171) that B1 does not cite — this is additive, not contradictory.

### Pair C (C1 + C2) — INCONSISTENT ON PRIMARY FINDING
As documented in ACC-1 and CON-1. C1's central corrective finding — that the "-3%" figure is wrong — is undermined by C2's Section 1 body text retaining the wrong figure. The summary table in C2 is correct; the body text is not. This is the most significant finding in the report.

C1 and C2 are otherwise well-integrated: both cite arXiv:2602.11988 as the primary source, both report the +2.7% improvement when markdown/docs are removed, both attribute the failure mechanism to redundancy (not inherent LLM limitation), and both report the +4% / +19% cost findings for human-written files consistently.

### Cross-Pair Integration
- A-to-C: No contradictions. A-pair findings about llms.txt and official doc availability are orthogonal to C-pair findings about guideline effectiveness.
- A-to-B: No contradictions. Both pairs agree that pre-synthesized, structured, LLM-ready content is valuable.
- B-to-C: Potential tension between B2's critique of auto-generated knowledge files (citing ETH Zurich as a challenge to Karpathy's unvalidated automation) and C1/C2's finding that the ETH Zurich failure mechanism is specifically redundancy. B2 correctly identifies the issue as a quality problem requiring human supervision — consistent with C1/C2's analysis. No contradiction at the conclusion level.

The B2 framing "The v2 extensions address this with quality scoring and confidence thresholds. The Ingest/Query/Lint loop must be human-supervised to produce quality-positive results, not automated" is consistent with C1's conclusion that the ETH Zurich study "represents the floor of LLM-generated quality, not the ceiling." These are complementary, not contradictory.

---

## Findings Index

| ID | Severity | File | Description |
|----|----------|------|-------------|
| ACC-1 | CRITICAL | C2 Section 1 | Body text cites "-3%" after C1 corrected it to -0.5%/-2% |
| ACC-2 | HIGH | C1 Section 3 | "GPT-5.2" and "GPT-5.1 mini" are unrecognized model names; may be hallucinated |
| ACC-3 | MEDIUM | B2 Section 4 | "Chroma 2025 study" cited without any citation |
| ACC-4 | MEDIUM | B2 Section 4 | "70% error attribution" cited to "multiple sources" with no citations |
| CON-1 | HIGH | C2 vs C1 | C2 body contradicts C1's primary corrective finding |
| CON-2 | MEDIUM | B1 synthesis | B1 synthesis does not acknowledge hot/cold split limitation documented in B2 |
| CON-3 | LOW | B2 Section 1 | Codified Context figures (19 agents, 9,300 lines) are specific; unverified |
| CUR-1 | HIGH | A2 Section 1 | Context7 "latest release April 9, 2026" — same as research date; may be fabricated |
| CUR-2 | LOW | A1, A2 | kotlinlang.org figures appropriately framed as "as of April 2026" |
| UNS-1 | HIGH | C2 Section 2 | arXiv:2506.02357 cited without title/author; safety-context generalizability caveat buried in table only |
| UNS-2 | MEDIUM | C2 Section 3 | 95-token finding presented without scope limitation (API tasks only) |
| UNS-3 | LOW | B2 Section 3 | ACE Framework arXiv:2510.04618 cited without title/author |

---

## Required Fixes Before Corpus Use

1. **C2 Section 1 body text** — Replace "-3% success rate" with "-0.5% on SWE-bench Lite and -2% on AGENTbench." Remove the parenthetical.
2. **C1 Section 3 model names** — Verify "GPT-5.2" and "GPT-5.1 mini" against arXiv:2602.11988 directly. If not found in the paper, replace with "models as specified in paper" or the actual model names.
3. **A2 Context7 release date** — Verify against github.com/upstash/context7/releases. If "April 9, 2026" is not accurate, correct it.
4. **B2 Chroma citation** — Supply full citation or downgrade to "practitioner observation."
5. **B2 70% error attribution** — Supply citations or reframe as practitioner framing with appropriate confidence.
6. **C2 arXiv:2506.02357** — Add paper title, author, and a body-text explanation of the safety-context limitation.

---

## Recommended Fixes (Optional Quality)

7. **C2 Section 3** — Scope the 95-token finding to API specification tasks.
8. **B1 synthesis** — Add hot/cold split caveat pointing to B2.
9. **B2 ACE Framework** — Add paper title and primary author.
