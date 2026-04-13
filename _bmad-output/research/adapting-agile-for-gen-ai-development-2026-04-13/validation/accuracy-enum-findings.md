# Factual Accuracy — Enumerator Findings

**Lens:** Factual Accuracy
**Reviewer:** Enumerator (systematic, section-by-section claim verification)
**Skepticism Level:** 3 (Aggressive)
**Artifact Stage:** Final

## Summary

| Severity | Count |
|---|---|
| Critical | 3 |
| High | 8 |
| Medium | 11 |
| Low | 4 |
| **Total** | **26** |

**Overall assessment:** The corpus is substantively well-researched and internally consistent across the 8 sub-question files. The Gemini deep-research output (file 1) is the primary source of attribution and factual problems — it makes several unsupported or misattributed claims not corroborated in the sub-question files. Several statistics appear with high precision but no traceable primary source. Named tools and frameworks (Bloom, DeepEval, agentevals, Kiro, MIT Project NANDA) require closer scrutiny. The cross-file consistency is generally good: where the same claim appears in multiple files, it is usually stated consistently.

---

## Findings

---

### ACCURACY-001
- **id:** ACCURACY-001
- **severity:** critical
- **dimension:** correctness
- **location:** `gemini-deep-research-output.md:## Frameworks for the Agentic Era`
- **description:** The "Harness Engineering" concept is attributed to "Martin Fowler and Birgitta Böckeler" in the Gemini output. However, file 2 (`research-thought-leader-frameworks-agile-ai.md`) — which explicitly sources Fowler's site — attributes the "Humans in/on/outside the loop" framework to **Kief Morris** (not Birgitta Böckeler). The Red Hat Developer source in file 6 (`research-feature-unit-user-value.md`) attributes a "harness engineering" article to developers.redhat.com, not to Fowler/Böckeler as authors. The OpenAI "Harness Engineering" article cited in file 9 (`research-ceremony-rhythm-alternatives.md`) is explicitly from **OpenAI's Codex team**, not from Fowler or Böckeler. The Gemini file conflates these distinct uses of "harness engineering" and misattributes authorship.
- **evidence:** Gemini file states: "Martin Fowler and Birgitta Böckeler have introduced 'Harness Engineering' as a mental model for managing coding agents." File 2 says the most significant contribution is "Kief Morris's article on human-agent collaboration loops." File 9 cites: "OpenAI's Harness Engineering model, documented in February 2026, describes how the Codex team operates." The martinfowler.com source list in file 2 does not include a Böckeler article about "harness engineering" — it references Böckeler only for the SDD tools analysis (Kiro, spec-kit, Tessl).
- **suggestion:** Disambiguate: the "human on the loop" framework is Kief Morris's (on Fowler's site). OpenAI's "Harness Engineering" is the Codex team's model. Birgitta Böckeler is correctly credited for the SDD tools analysis. Remove the claim that Fowler and Böckeler jointly introduced "Harness Engineering."

---

### ACCURACY-002
- **id:** ACCURACY-002
- **severity:** critical
- **dimension:** correctness
- **location:** `gemini-deep-research-output.md:## Solving the 'Spec-Correct, Value-Zero' Problem`
- **description:** The Gemini file attributes "The Agentic Manifesto" to Casey West and characterizes it as proposed "in early 2026," framing it as advocating "a clean break" and "verification to validation" shift. However, file 2 (`research-thought-leader-frameworks-agile-ai.md`) cites Casey West's Agentic Manifesto as published in **2025** (not early 2026), and characterizes it as proposing an "Agentic Delivery Lifecycle (ADLC) as a wrapper around the traditional SDLC" — explicitly **not** a replacement. File 2 states: "It does not replace SDLC but adds a governance layer." The Gemini file's characterization — "a direct response to Agile friction" advocating "a clean break from 'human-pacing'" — is an overstatement contradicted by the more carefully sourced file 2.
- **evidence:** Gemini: "The 'Agentic Manifesto,' proposed by Casey West in early 2026..." File 2: "Casey West's Agentic Manifesto (2025) proposes an Agentic Delivery Lifecycle (ADLC) as a wrapper around the traditional SDLC [PRAC — caseywest.com, 2025]. It does not replace SDLC but adds a governance layer for non-deterministic behavior." The date discrepancy (2026 vs. 2025) and the "clean break" vs. "wrapper" framing are directly contradictory.
- **suggestion:** Correct date to 2025. Correct characterization from "clean break" to "governance wrapper for SDLC." The verification-to-validation shift framing is accurate but should not be conflated with an anti-Agile position.

---

### ACCURACY-003
- **id:** ACCURACY-003
- **severity:** critical
- **dimension:** traceability
- **location:** `gemini-deep-research-output.md:## Limitations and Risks`
- **description:** The Gemini file claims: "Research by Anthropic and others suggests a concerning divergence: while AI increases productivity, it can erode deep comprehension. Junior engineers who use AI to 'generate code' rather than as a 'thinking partner' score significantly lower on comprehension tests." No source is cited for this specific claim about Anthropic research or comprehension test scoring. This is a precise empirical claim (scoring differential, characterization of a research finding) with no traceable attribution.
- **evidence:** The text reads: "Research by Anthropic and others suggests a concerning divergence...Junior engineers who use AI to 'generate code' rather than as a 'thinking partner' score significantly lower on comprehension tests." No footnote, URL, or author attribution is provided in the Sources section for this claim. The METR research (cited in files 3 and 8) discusses productivity *decreases* for *experienced* developers — not comprehension test performance for juniors.
- **suggestion:** Either provide the specific Anthropic publication this references, or flag it as unverified. The METR finding about experienced developers taking 19% longer is a real study but covers a different population and outcome than claimed here.

---

### ACCURACY-004
- **id:** ACCURACY-004
- **severity:** high
- **dimension:** correctness
- **location:** `gemini-deep-research-output.md:## Follow-up Q1:## 2. Casey West`
- **description:** The follow-up section re-states the Casey West claim and adds that the Agentic Manifesto is "proposed in early 2026 as a direct response to Agile friction." This is the same date error identified in ACCURACY-002, now repeated in a different section. Additionally, the follow-up section mentions an "agenticmanifesto.org" URL in file 2's source list, but attributes authorship of that manifesto to Casey West. File 2 lists both "caseywest.com/the-agentic-manifesto/" AND "agenticmanifesto.org" as separate sources, suggesting these may be two distinct manifestos or that the agenticmanifesto.org is a separate artifact — yet the Gemini file treats them as one entity authored by West.
- **evidence:** Gemini follow-up Q1: "Casey West: The 'Agentic Manifesto' — Proposed in early 2026 as a direct response to Agile friction." File 2 sources list: "[The Agentic Manifesto — Casey West] (https://caseywest.com/the-agentic-manifesto/) [PRAC]" and separately "[Agentic Manifesto — agenticmanifesto.org] (https://www.agenticmanifesto.org/) [PRAC]" — two separate URLs, suggesting two potentially different documents.
- **suggestion:** Clarify whether agenticmanifesto.org is Casey West's manifesto or a separate community document. Correct the date to 2025.

---

### ACCURACY-005
- **id:** ACCURACY-005
- **severity:** high
- **dimension:** traceability
- **location:** `research-cognitive-load-inversion.md:## The Inversion Problem in Concrete Terms`
- **description:** The file states: "Developers using AI complete 21% more tasks and merge 98% more PRs — but PR review time increases 91% in the same period." This is a very specific trio of statistics. The source cited is "newsletter.eng-leadership.com/p/code-review-is-the-new-bottleneck" — a newsletter article, not a primary research publication. The 98% and 91% figures are precise enough to suggest they derive from a specific dataset, but the newsletter is a secondary source. The primary research origin of these figures is not identified.
- **evidence:** "Developers using AI complete 21% more tasks and merge 98% more PRs — but PR review time increases 91% in the same period. [PRAC: https://newsletter.eng-leadership.com/p/code-review-is-the-new-bottleneck]"
- **suggestion:** Identify the primary research source behind these statistics. The newsletter likely cites a specific LinearB, GitHub, or DORA study. Flag as "unverified — needs primary citation" if the underlying source cannot be identified.

---

### ACCURACY-006
- **id:** ACCURACY-006
- **severity:** high
- **dimension:** traceability
- **location:** `research-cognitive-load-inversion.md:## The Inversion Problem in Concrete Terms`
- **description:** The LinearB claim is stated as: "agentic AI PRs sit idle 5.3× longer before anyone picks them up for review, and AI-assisted PRs wait 2.47× longer than unassisted ones — even though once review begins, AI PRs are reviewed 2× faster." These are again highly precise statistics. The source is cited as "linearb.io/resources/engineering-benchmarks." This is plausible (LinearB does publish benchmark reports), but the "5.3x longer" and "2.47x longer" figures appear also in the Gemini file's comparison table ("5.3x longer wait") suggesting they propagated from the same source — but neither file identifies the specific report edition, date, or methodology.
- **evidence:** "agentic AI PRs sit idle 5.3× longer before anyone picks them up for review, and AI-assisted PRs wait 2.47× longer than unassisted ones [PRAC: https://linearb.io/resources/engineering-benchmarks]"
- **suggestion:** Cite the specific report edition and date (the "2026 Software Engineering Benchmarks Report" is named later in sources — confirm this is the specific source for both statistics). Note the sample characteristics: "8.1 million PRs across 4,800 engineering teams in 42 countries" is stated later in the same file, which provides useful context but should be co-located with the statistics.

---

### ACCURACY-007
- **id:** ACCURACY-007
- **severity:** high
- **dimension:** correctness
- **location:** `research-spec-correct-value-zero.md:## What Practitioners Report Is Not Working`
- **description:** The file states: "the MIT Project NANDA finding that 95% of corporate AI projects show no measurable return suggests the spec-to-value problem is widespread at the organizational level." "MIT Project NANDA" is a specific, named MIT research project. This is an extraordinary claim (95% failure rate) attributed to a specific project. However, no URL or publication citation is provided for MIT Project NANDA in the sources section. The BCG Widening AI Value Gap report is cited separately. Without a source URL for this specific MIT claim, it cannot be verified.
- **evidence:** "the MIT Project NANDA finding that 95% of corporate AI projects show no measurable return" — no source URL or publication reference appears in the sources section for this specific claim.
- **suggestion:** Add the specific MIT Project NANDA publication URL and date, or flag as unverified. The 95% figure and "Project NANDA" name should be verified as they do not appear in other corpus files and cannot be cross-checked internally.

---

### ACCURACY-008
- **id:** ACCURACY-008
- **severity:** high
- **dimension:** correctness
- **location:** `gemini-deep-research-output.md:## Follow-up Q1:## 4. Shape Up as the "New Meta"`
- **description:** The Gemini file attributes a hybrid "Shape Up + NASA's Technology Readiness Levels (TRL)" approach to a company called "Silken Net." This is a very specific corporate attribution that cannot be cross-checked from other corpus files, and no source URL is provided for this claim. "Silken Net" does not appear in any other corpus file. The claim that they "completely overhauled their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels" is precise and verifiable, but no source is given.
- **evidence:** "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)." No URL or source citation accompanies this claim in the Gemini file.
- **suggestion:** Provide a source URL for the Silken Net claim, or flag as unverified. This reads as a specific practitioner case study but has no citation backing.

---

### ACCURACY-009
- **id:** ACCURACY-009
- **severity:** high
- **dimension:** correctness
- **location:** `gemini-deep-research-output.md:## Follow-up Q1:## 5. The Kinetic Enterprise`
- **description:** The Gemini file states: "Researchers at Deloitte and others have introduced the Kinetic Enterprise doctrine." The "Kinetic Enterprise" is attributed to Deloitte researchers, but no publication, URL, or date is provided. In the sub-question files, "Kinetic Enterprise" does not appear in any of the 8 research files. The claim about "fluid Team Topologies that form and dissolve based on real-time telemetry" is presented as a Deloitte research output with no verifiable citation.
- **evidence:** "Researchers at Deloitte and others have introduced the Kinetic Enterprise doctrine: From Labor to Compute... fluid Team Topologies that form and dissolve based on real-time telemetry." No source URL, report name, author, or date is provided. The term "Kinetic Enterprise" does not appear in any of the 8 sub-question research files.
- **suggestion:** Provide the specific Deloitte publication (title, URL, date) for the "Kinetic Enterprise" concept. If this cannot be sourced, flag as unverified and remove specific attribution to Deloitte.

---

### ACCURACY-010
- **id:** ACCURACY-010
- **severity:** high
- **dimension:** traceability
- **location:** `research-behavioral-validation-ai-agents.md:## Commercial AI QA Platforms`
- **description:** The file claims Anthropic's "Bloom" is "an open-source tool for automated behavioral evaluations." The citation is "[Introducing Bloom: open source tool for automated behavioral evaluations | Anthropic]." The claim is specific but "Bloom" is not a widely-known Anthropic tool in the public knowledge base. If this tool exists, the citation is appropriate; if it was hallucinated or confused with another tool, this is a significant factual error. No corroboration appears in other corpus files or in the Gemini file's sources section.
- **evidence:** "Anthropic's open-source tool Bloom (2025) implements automated behavioral evaluations at scale, applying LLM-based scoring to real interaction transcripts." Source: "https://www.anthropic.com/research/bloom"
- **suggestion:** Verify that anthropic.com/research/bloom exists and describes the tool as characterized. If the URL does not resolve or describes a different tool, this is a hallucinated citation and must be flagged as such. Mark as "unverified — needs URL verification."

---

### ACCURACY-011
- **id:** ACCURACY-011
- **severity:** high
- **dimension:** traceability
- **location:** `gemini-deep-research-output.md:## Follow-up Q2`
- **description:** The Gemini file describes "The OpenSpec 'Propose-Apply-Archive' Loop" as "developed by Fission-AI." No URL, date, or corroborating source is provided for this specific attribution. The tool "OpenSpec" appears again in the follow-up Q3 table as an open-source tool with a specific description. In neither place is a URL or verifiable source given. "Fission-AI" as the developer of OpenSpec is an unverifiable specific claim.
- **evidence:** "The OpenSpec 'Propose-Apply-Archive' Loop: This framework, developed by Fission-AI, uses a simple three-step cycle." No URL, GitHub repository, or publication is cited.
- **suggestion:** Provide a URL for OpenSpec (e.g., a GitHub repository or product website). Without this, the tool's existence as described and its attribution to Fission-AI are unverifiable. Flag as "unverified — needs citation."

---

### ACCURACY-012
- **id:** ACCURACY-012
- **severity:** medium
- **dimension:** correctness
- **location:** `gemini-deep-research-output.md:## Restructuring Work Granularity`
- **description:** The Gemini file attributes "Zones of Intent" as "AWS's 2026 prescriptive guidance." However, in the more carefully sourced sub-question files, the AWS Prescriptive Guidance is described as relating to value stream mapping and the AI-DLC framework (file 9 cites "AI-DLC" at re:Invent 2025 and the GitHub repo "awslabs/aidlc-workflows"). The specific term "Zones of Intent" does not appear in any of the 8 sub-question files as an AWS concept. This may be a paraphrase that has been presented as a specific named AWS concept.
- **evidence:** "AWS's 2026 prescriptive guidance introduces 'Zones of Intent' as the primary abstraction for managing work granularity." The term "Zones of Intent" does not appear in files 3, 4, 5, 6, 7, 8, or 9. The AWS AI-DLC material in file 9 uses different terminology ("Inception/Construction/Operations" phases, "Kiro Steering Files").
- **suggestion:** Verify whether "Zones of Intent" is an actual AWS term or a paraphrase. If it is a paraphrase, replace with the actual AWS terminology used. If it is a real concept, provide the specific AWS documentation URL.

---

### ACCURACY-013
- **id:** ACCURACY-013
- **severity:** medium
- **dimension:** traceability
- **location:** `research-cognitive-load-inversion.md:## Why Review Gets Harder`
- **description:** The file attributes a "Vibe-Check Protocol: Quantifying Cognitive Offloading in AI Programming" to arXiv paper 2601.02410. This paper is cited as an "[OFFICIAL]" source for the claim that "developers reviewing AI-generated code in recognition mode show reduced critical assessment capacity." The arXiv number (2601.02410) follows the convention YYMM.NNNNN, meaning it was submitted in January 2026 — which is plausible but should be noted. The title and core claims are specific enough to verify if the arXiv paper exists. No author attribution is given.
- **evidence:** "[OFFICIAL: https://www.arxiv.org/pdf/2601.02410]" — labeled as OFFICIAL despite being an arXiv preprint (which is not peer-reviewed). The finding "developers reviewing AI-generated code in recognition mode show reduced critical assessment capacity" is attributed to this paper.
- **suggestion:** Note that arXiv preprints are not peer-reviewed and should not be labeled "[OFFICIAL]." Change label to "[PREPRINT]" or "[ACADEMIC PRAC]." Verify the paper exists at that arXiv ID before treating it as confirmed.

---

### ACCURACY-014
- **id:** ACCURACY-014
- **severity:** medium
- **dimension:** traceability
- **location:** `research-cognitive-load-inversion.md:## Empirical Data on the Trust Gap`
- **description:** The file states: "96% of developers report they do not fully trust AI-generated code — yet only 48% say they always check it before committing." The source is cited as "talent500.com/blog/ai-generated-code-trust-and-verification-gap/" — a single blog post at a recruiting/staffing platform. A separate claim in the same section says "only 29% of developers trust AI output in 2025, down 11 percentage points from 2024" with Stack Overflow as the source. These two figures (96% distrust vs. 29% trust) are not inherently contradictory but appear to come from different surveys with different question framings, and presenting them adjacently without noting the methodological difference could mislead.
- **evidence:** "96% of developers report they do not fully trust AI-generated code" [talent500.com] vs. "only 29% of developers trust AI output in 2025" [stackoverflow.blog]. One measures "fully trust," the other measures "trust" without the qualifier — different survey questions producing superficially conflicting-looking numbers cited in the same paragraph.
- **suggestion:** Add a brief note that these figures measure different constructs (full trust vs. trust generally) and come from different survey populations. The talent500 figure should be checked for its original primary source.

---

### ACCURACY-015
- **id:** ACCURACY-015
- **severity:** medium
- **dimension:** correctness
- **location:** `research-ceremony-rhythm-alternatives.md:## AWS AI-DLC`
- **description:** The file states AWS "open-sourced the AI-Driven Development Lifecycle (AI-DLC) at re:Invent 2025." It then says enterprise customers include "Wipro, Dun & Bradstreet" with "reported 10-15x productivity gains." The 10-15x figure is extraordinary and the source for this specific claim is not separately cited beyond the general AWS DevOps blog URL. The 10-15x range should be verified against the actual AWS blog post rather than treated as established fact.
- **evidence:** "Adopted by enterprise customers (Wipro, Dun & Bradstreet) with reported 10-15x productivity gains" — no separate citation for this specific claim beyond the general AWS DevOps blog URL provided at the end of the section.
- **suggestion:** Locate the specific portion of the AWS DevOps blog post or press release where the 10-15x figure and customer names appear. If the source only mentions the customers without citing specific productivity numbers, revise the claim accordingly.

---

### ACCURACY-016
- **id:** ACCURACY-016
- **severity:** medium
- **dimension:** correctness
- **location:** `research-work-granularity-ai-speed.md:## The Core Problem`
- **description:** The file states: "METR's July 2025 research on experienced open-source developers found task completion times compressing dramatically, and machine learning benchmarks showed that the length of tasks AI can reliably complete has been doubling approximately every four months since 2024 — with supervised autonomous task horizons reaching roughly two hours as of late 2025 and projected to reach four days of unsupervised work by 2027." The "doubling every four months" claim and "four days by 2027" projection are cited to "METR research blog, 2025-07-10" — but the METR study is well-known for showing experienced developers actually took 19% *longer*, not faster, with AI assistance. The "task length doubling" and horizon projections are separate claims that need separate sourcing from the METR study.
- **evidence:** "METR's July 2025 research...found task completion times compressing dramatically" — this contradicts the METR finding cited in file 8: "The 2025 METR randomized controlled trial found experienced open-source developers working on their own repositories took 19% *longer* to complete tasks with AI tools." The "doubling every four months" claim is attributed to "MachineLearningMastery.com agentic trends 2026" — a practitioner blog, not primary research.
- **suggestion:** Correct the characterization of the METR study: it did NOT find task completion times compressing; it found the opposite for experienced developers. Separate the "autonomous task horizon" doubling claim (from ML benchmarks, not from the METR study) and attribute it precisely to its actual source.

---

### ACCURACY-017
- **id:** ACCURACY-017
- **severity:** medium
- **dimension:** traceability
- **location:** `research-acceptance-criteria-ai-literal.md:## The Core Problem`
- **description:** The file cites "A 2026 study found that AI-introduced issues surviving in production repositories had risen to over 110,000 by February 2026" attributed to "cited in github.blog and augmentcode.com analysis." This is a secondary citation — the primary study is not identified. "Over 110,000" is a very specific figure that implies a specific dataset and methodology. Without knowing the primary source, the figure's definition (what counts as an "AI-introduced issue"?) and validity cannot be assessed.
- **evidence:** "A 2026 study found that AI-introduced issues surviving in production repositories had risen to over 110,000 by February 2026, characterized as 'long-term maintenance technical debt' — the accumulated cost of guesses embedded into code. [PRAC — cited in github.blog and augmentcode.com analysis]"
- **suggestion:** Identify the primary study behind this statistic. The citation currently points to secondary commentary, not the original research. Flag as "unverified — secondary citation only."

---

### ACCURACY-018
- **id:** ACCURACY-018
- **severity:** medium
- **dimension:** traceability
- **location:** `research-spec-correct-value-zero.md:## Solution Pattern 4`
- **description:** The file cites "Shopify's internal memo demanding teams 'demonstrate why they cannot get done using AI' before requesting headcount." This is attributed to "allstacks.com" — a secondary source blog post. Shopify's internal memo is widely reported but its exact wording varies across secondary sources. The specific phrasing "demonstrate why they cannot get done using AI" should be verified against the original Shopify communication or a primary source reporting it verbatim.
- **evidence:** "Shopify's internal memo demanding teams 'demonstrate why they cannot get done using AI' before requesting headcount signals a broader shift. [PRAC, allstacks.com]"
- **suggestion:** Verify the exact wording of the Shopify memo against a primary news source or official Shopify communication. Allstacks.com is an analytics blog, not a primary reporter. The substance is accurate (Shopify did issue such guidance) but the quoted phrasing may be paraphrased.

---

### ACCURACY-019
- **id:** ACCURACY-019
- **severity:** medium
- **dimension:** logical_soundness
- **location:** `gemini-deep-research-output.md:## Feature as a Unit of User Value`
- **description:** The Gemini file states: "Leading teams enforce a 'done' state not by checking off tickets, but by achieving a 'production-ready MVP' state within the 3-month window of the 3-3-3 model." This conflates the Thoughtworks 3-3-3 model's milestone definition with a general claim about "leading teams." The 3-3-3 model is a Thoughtworks/AI/works specific framework, not a general industry pattern. Presenting it as what "leading teams" do overgeneralizes a proprietary Thoughtworks platform behavior.
- **evidence:** "Leading teams enforce a 'done' state not by checking off tickets, but by achieving a 'production-ready MVP' state within the 3-month window of the 3-3-3 model." The file presents this as a general industry statement, but file 2 identifies AI/works and the 3-3-3 model as Thoughtworks-specific (tied to the AI/works platform launch).
- **suggestion:** Qualify this claim: "Thoughtworks' 3-3-3 model redefines 'done' as achieving a production-ready MVP..." rather than attributing it to "leading teams" generally.

---

### ACCURACY-020
- **id:** ACCURACY-020
- **severity:** medium
- **dimension:** traceability
- **location:** `research-feature-unit-user-value.md:## 1. The Core Problem`
- **description:** The file cites a claim: "'Done' means live in production, not just code complete." attributed to "nkdagility.com/resources/value-delivery/" with the explicit label "[UNVERIFIED — site content summarized, URL: nkdagility.com/resources/value-delivery/]." The file itself flags this as unverified. This is an appropriate transparency flag, but the finding still warrants noting in this review as the claim is then used as supporting evidence in the argument.
- **evidence:** "'Done' means live in production, not just code complete.' [UNVERIFIED — site content summarized, URL: nkdagility.com/resources/value-delivery/]"
- **suggestion:** Since the file itself correctly flags this as unverified, the synthesis section should not rely on it as a standalone supporting claim. Ensure the surrounding argument does not treat this as confirmed evidence.

---

### ACCURACY-021
- **id:** ACCURACY-021
- **severity:** medium
- **dimension:** traceability
- **location:** `research-behavioral-validation-ai-agents.md:## Playwright's Native Agent Architecture`
- **description:** The file describes "Playwright 1.56 (October 2025)" as introducing a native three-agent system (Planner, Generator, Healer). Playwright version numbers and release dates are verifiable facts. If "1.56" is the wrong version number, or if the three-agent architecture was introduced in a different version or under a different feature name, this would be a factual error. This specific versioning claim should be confirmed against Playwright's official release notes.
- **evidence:** "Playwright 1.56 (October 2025) introduced a native three-agent system that operates exclusively against live running applications."
- **suggestion:** Verify that Playwright 1.56 corresponds to October 2025 and that the three-agent "Test Agents" feature was introduced in that specific version. Check playwright.dev release notes. Flag as "unverified — needs version confirmation" if this cannot be confirmed.

---

### ACCURACY-022
- **id:** ACCURACY-022
- **severity:** medium
- **dimension:** correctness
- **location:** `research-thought-leader-frameworks-agile-ai.md:## DORA 2025`
- **description:** The file states "Forrester's 2025 State of Agile Development found 95% of professionals affirm Agile's relevance, with nearly half already leveraging generative AI within agile practices." The same statistic appears in file 3 ("Forrester's 2025 State of Agile Development report found 95% of professionals still affirm Agile's critical relevance"). However, the Forrester report cited in file 2's sources section is NOT listed in the sources — only DORA is. File 3 cites this as "[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage]" — a secondary reference. The 95% figure cannot be traced to the primary Forrester report in either file.
- **evidence:** File 2: "Forrester's 2025 State of Agile Development found 95% of professionals affirm Agile's relevance." File 3: "Forrester's 2025 State of Agile Development report found 95% of professionals still affirm Agile's critical relevance — though critics note this may reflect institutional inertia." Neither file includes the Forrester report in the Sources section.
- **suggestion:** Add the Forrester 2025 State of Agile Development report URL to sources in both files, or flag the 95% statistic as "unverified — needs primary citation." The fact that multiple files use this figure suggests it may be accurate but the primary source should be confirmed.

---

### ACCURACY-023
- **id:** ACCURACY-023
- **severity:** low
- **dimension:** correctness
- **location:** `research-work-granularity-ai-speed.md:## Shape Up as an AI-Native Alternative`
- **description:** The file attributes Shape Up to "Basecamp's Shape Up methodology (Ryan Singer, 2019)." Shape Up was indeed developed by Ryan Singer at Basecamp, but the publicly available book was released in 2019 and the company has since rebranded from Basecamp to 37signals (the parent company of Basecamp and HEY). The attribution "Basecamp's Shape Up" is technically correct as Shape Up is associated with the Basecamp product methodology, but subsequent references in file 9 correctly note "Basecamp (basecamp.com/shapeup)" and "37signals." This is a minor inconsistency, not a factual error.
- **evidence:** File 3: "Basecamp's Shape Up methodology (Ryan Singer, 2019)." File 9 sources: "Basecamp: Shape Up (original methodology) — basecamp.com/shapeup." The company that created Shape Up is 37signals; Basecamp is one of their products.
- **suggestion:** Minor clarification: attribute to "37signals/Basecamp's Shape Up methodology" or simply "Ryan Singer's Shape Up (Basecamp, 2019)" to acknowledge both the author and the product context.

---

### ACCURACY-024
- **id:** ACCURACY-024
- **severity:** low
- **dimension:** traceability
- **location:** `research-ceremony-rhythm-alternatives.md:## Harness Engineering: A Practitioner Model from OpenAI`
- **description:** The file describes "OpenAI's Harness Engineering model" and states the Codex team managed "approximately 1,500 pull requests in five months — 3.5 PRs per engineer per day." However, 1,500 PRs over five months with a "3-7 engineer" team would be approximately 3.5-7.1 PRs/engineer/day — the math is only consistent if the team was at the lower end (3 engineers). This arithmetic is not explicitly stated as a calculation and may reflect the original OpenAI source directly, but it warrants verification against the source.
- **evidence:** "The team of 3-7 engineers managed approximately 1,500 pull requests in five months — 3.5 PRs per engineer per day." 1,500 / (5 months × 21 working days) = ~14.3 PRs/day total. 14.3 / 4 engineers (midpoint) = 3.6 PRs/engineer/day. At 7 engineers: 2 PRs/engineer/day. The "3.5" figure is only consistent with a team of ~4 engineers, not the full 3-7 range.
- **suggestion:** Verify the "3.5 PRs per engineer per day" figure against the OpenAI source directly. If the source specifies a specific team size during that period, use that specific number. The stated range "3-7" and the per-engineer rate are arithmetically inconsistent.

---

### ACCURACY-025
- **id:** ACCURACY-025
- **severity:** low
- **dimension:** correctness
- **location:** `research-thought-leader-frameworks-agile-ai.md:## Spec-Driven Development`
- **description:** The file attributes the SDD tools analysis article to "Birgitta Böckeler's 2026 article on Kiro, spec-kit, and Tessl." However, the URL cited is "martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html" — which is in the "exploring-gen-ai" series. Kief Morris's authorship of the human-agent loops article is explicitly stated, but this SDD tools article is attributed to Böckeler without confirming her authorship. The martinfowler.com site hosts articles by multiple authors; attributing all "Fowler site" content to a specific author requires verification.
- **evidence:** "Birgitta Böckeler's 2026 article on Kiro, spec-kit, and Tessl [OFFICIAL — martinfowler.com, 2026] offers the most rigorous critical assessment of the SDD tool ecosystem." URL: "martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html" — authorship should be verified at the URL.
- **suggestion:** Verify that Birgitta Böckeler is the actual author of the sdd-3-tools article at martinfowler.com, or correct the attribution. The authorship of this specific article matters because Böckeler's name appears in the Gemini file's "Harness Engineering" misattribution (ACCURACY-001).

---

### ACCURACY-026
- **id:** ACCURACY-026
- **severity:** low
- **dimension:** logical_soundness
- **location:** `gemini-deep-research-output.md:## Conclusions:## 2. Adopt the 3-3-3 Model`
- **description:** The conclusion recommends "Adopt the 3-3-3 Model: Move away from indeterminate modernization timelines toward a structured 90-day path to value." This recommendation is presented as broadly applicable, but the 3-3-3 model is tied to the AI/works™ platform (as documented in files 1 and 2). Teams cannot simply "adopt the 3-3-3 model" as a standalone methodology without the AI/works platform infrastructure. The recommendation conflates a commercial platform's delivery model with a generic best practice.
- **evidence:** The recommendation says "Adopt the 3-3-3 Model" without qualifying that it is specific to the AI/works platform. File 2 states: "The 3-3-3 delivery model pairs with AI/works: product concept → prototype → MVP in production in 90 days." The model is milestone-and-spec-based but operationalized via AI/works tooling.
- **suggestion:** Qualify the recommendation: "Adopt the 3-3-3 model's milestone philosophy (concept → prototype → MVP in 90 days) as a delivery framework, noting that Thoughtworks operationalizes this via the AI/works platform." This preserves the useful guidance while being accurate about the context.

---

## Cross-File Consistency Notes

The following observations do not constitute additional findings but provide context for the findings above:

1. **The METR study contradiction** (ACCURACY-016) is the most significant internal inconsistency: file 3 says METR found "task completion times compressing dramatically" while file 8 correctly states experienced developers took "19% longer." These are the same study, opposite characterizations.

2. **Attribution consistency for Harness Engineering:** Three different "harness engineering" concepts appear across the corpus — Fowler/Böckeler/Morris (the agent loop framework), OpenAI (the Codex team model), and Red Hat (structured AI-assisted development). The Gemini file conflates all three under a single attribution to "Fowler and Böckeler." The sub-question files correctly treat them as separate concepts.

3. **Casey West date consistency:** File 2 says 2025; Gemini file says "early 2026" — in two separate places. This is a consistent error in the Gemini file, not a cross-file conflict, because file 2 sources the primary URL directly.

4. **Tool existence uncertainty:** DeepEval, agentevals, and Inspect AI are named in the gemini follow-up Q3 table. DeepEval is a real open-source Python testing library (confident-ai/deepeval on GitHub). Inspect AI from the UK AI Safety Institute is a real framework. "agentevals" as described (using OpenTelemetry) may refer to the LangChain agentevals library — real but the description should be checked for accuracy. These are marked medium-confidence, not flagged as findings, because they appear plausible with available external knowledge.
