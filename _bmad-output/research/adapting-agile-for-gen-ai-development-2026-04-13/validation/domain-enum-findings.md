# Domain Fitness — Enumerator Findings

**Summary:** 11 findings — 1 critical, 3 high, 5 medium, 2 low

---

## Dimension 1: Domain Rule Compliance — Agile/XP/LLM Concepts

### DOMAIN-001
- **id:** DOMAIN-001
- **severity:** critical
- **dimension:** domain_rule_compliance
- **location:** `research-spec-correct-value-zero.md:Solution Pattern 5`
- **description:** MIT Project NANDA statistic stated without qualification. The file cites "MIT Project NANDA finding that 95% of corporate AI projects show no measurable return" as practitioner-level evidence for the spec-to-value problem. This figure is extraordinary and the citation is unattributed — the footnote points only to `bcg.com` and the BCG "Widening AI Value Gap" report, which is about enterprise ROI from GenAI broadly, not about spec-to-value failure at the story level. MIT Project NANDA cannot be located via publicly known sources as of this writing, and no URL is provided. Using a non-verifiable 95% failure-rate claim as though it validates the "spec-correct, value-zero" pattern conflates AI-adoption ROI disappointment with the specific spec-to-behavioral-value gap under research. This misleads on causality.
- **evidence:** "The MIT Project NANDA finding that 95% of corporate AI projects show no measurable return suggests the spec-to-value problem is widespread at the organizational level, not just the story level." (research-spec-correct-value-zero.md, "What Practitioners Report Is Not Working")
- **suggestion:** Either supply a verifiable URL and verify the figure applies specifically to spec-completeness failures (not general AI ROI), or remove the claim. The BCG finding already supports the broader ROI point adequately and is cited with a URL.

---

### DOMAIN-002
- **id:** DOMAIN-002
- **severity:** high
- **dimension:** domain_rule_compliance
- **location:** `research-acceptance-criteria-ai-literal.md:BDD and Gherkin`
- **description:** The file conflates BDD with Gherkin syntax throughout the BDD section, and the Paul Duvall "ATDD-for-AI" section uses ATDD and BDD as synonyms without distinguishing them. ATDD (Acceptance Test-Driven Development) is a practice where acceptance tests drive development from the outside in; BDD (Behavior-Driven Development) is a collaboration practice with a specific vocabulary (Given/When/Then). Gherkin is the DSL that BDD tools (Cucumber, Behave) use. These are related but distinct: ATDD can use Gherkin but need not; BDD does not require that tests be written before code in the way TDD/ATDD prescribe. The document treats all three as interchangeable, which will mislead readers trying to select or implement specific practices.
- **evidence:** "Paul Duvall's ATDD-for-AI framework addresses this by making acceptance tests the **primary specification mechanism** rather than a downstream verification artifact... 'no implementation file is created without a corresponding BDD feature file.'" (research-acceptance-criteria-ai-literal.md, "BDD and Gherkin") — here ATDD framework is described via a BDD artifact requirement, collapsing distinct practices.
- **suggestion:** Clarify the hierarchy: BDD is the collaboration practice; Gherkin is the format; ATDD is the test-first discipline. Note that the Duvall pattern is specifically an ATDD enforcement rule (tests first), implemented using Gherkin-format BDD scenarios. Three sentences would disambiguate without restructuring the section.

---

### DOMAIN-003
- **id:** DOMAIN-003
- **severity:** high
- **dimension:** domain_rule_compliance
- **location:** `gemini-deep-research-output.md:Test-Driven AI (TDA) and the 'Red' Phase`
- **description:** The "Test-Driven AI (TDA)" framing attributed to Kent Beck is domain-inaccurate. The corpus attributes TDA to "Kent Beck and others" as if Beck coined or endorses the term "Test-Driven AI." Beck's documented position is that he applies TDD discipline to AI-assisted coding — specifically, using the classic red-green-refactor cycle to constrain AI output. He does not use the term "TDA" in his published writing (Tidy First substack, Pragmatic Engineer interview), and the term implies a new methodology distinct from TDD, which misrepresents Beck's actual position. Renaming TDD as "TDA" to make it sound AI-specific creates semantic drift without substance. The file `research-thought-leader-frameworks-agile-ai.md` correctly describes Beck's position without the TDA label — the Gemini synthesis has overstated and relabeled.
- **evidence:** "Kent Beck and others have emphasized that Test-Driven Development (TDD) is a 'superpower' in the age of AI agents. However, the methodology has evolved into 'Test-Driven AI' (TDA)." (gemini-deep-research-output.md, "Test-Driven AI (TDA) and the 'Red' Phase")
- **suggestion:** Refer to this practice as "TDD applied to AI-assisted development" or "AI-constrained TDD" — terms grounded in what Beck actually advocates. If "TDA" is a distinct practitioner coinage from a third party, attribute it correctly and do not link it to Beck.

---

### DOMAIN-004
- **id:** DOMAIN-004
- **severity:** high
- **dimension:** domain_rule_compliance
- **location:** `research-ceremony-rhythm-alternatives.md:Harness Engineering: A Practitioner Model from OpenAI`
- **description:** The "Harness Engineering" concept is attributed to OpenAI in this section, but the Fowler/Böckeler harness model — which is the primary usage of "Harness Engineering" throughout the corpus — originates from Martin Fowler's site and the Böckeler article. OpenAI's Codex team workflow is described as "OpenAI's Harness Engineering model," which muddles two distinct uses of the same phrase. The OpenAI content (as described) is about operational workflow for a specific AI-native team, not a named methodology. Using "Harness Engineering" for both creates false attribution and could mislead readers about the provenance and generality of each concept.
- **evidence:** "OpenAI's Harness Engineering model, documented in February 2026, describes how the Codex team operates with AI agents as the primary contributors." (research-ceremony-rhythm-alternatives.md, "Harness Engineering: A Practitioner Model from OpenAI")
- **suggestion:** Re-label this section "OpenAI Codex Team: Ceremony-Free Agent-First Workflow" or similar. Reserve "Harness Engineering" for the Fowler/Böckeler methodology. Note that OpenAI's described workflow is an application of harness-type thinking, not a separate methodology named "Harness Engineering."

---

### DOMAIN-005
- **id:** DOMAIN-005
- **severity:** medium
- **dimension:** domain_rule_compliance
- **location:** `research-feature-unit-user-value.md:Section 7 — Product-Led Growth`
- **description:** The "Aha Moment" concept is attributed to PLG broadly but in the PLG literature it is specifically associated with particular companies' activation metrics (e.g., Facebook's "7 friends in 10 days," Slack's "2,000 messages"). The corpus uses it as a generic, measurable "done" gate. This is a reasonable abstraction for the research purpose, but the claim that "a feature is not done when it ships — it is done when users demonstrably reach the Aha Moment" is not standard industry practice — it is an aspirational framing from PLG-oriented companies. Most development teams, even mature ones, do not have instrumented Aha Moments for each feature. The research should distinguish between "this is how PLG-mature companies operate" and "this is a workable model for typical teams."
- **evidence:** "In PLG teams, a feature is not done when it ships — it is done when users demonstrably reach the Aha Moment. This requires instrumentation to be part of the definition of done: a feature cannot be declared complete unless event tracking is in place to observe whether users reach the value milestone." (research-feature-unit-user-value.md, Section 7)
- **suggestion:** Qualify that this model requires PLG-level product instrumentation maturity. Acknowledge that for most teams, a feasible step toward this is "instrumentation must be in place before rollout" — which is achievable — rather than "Aha Moment confirmed" — which is a high bar that many teams cannot operationalize per story.

---

### DOMAIN-006
- **id:** DOMAIN-006
- **severity:** medium
- **dimension:** domain_rule_compliance
- **location:** `research-behavioral-validation-ai-agents.md:Playwright's Native Agent Architecture`
- **description:** Playwright 1.56 is described as introducing a "native three-agent system" in October 2025. The description of the Planner, Generator, and Healer agents is structurally plausible given Playwright's direction, but the version number (1.56) and specific release date are unverifiable from the source citation alone, and the claim that the Generator "verifies selectors and assertions live as it performs the scenarios" merges what is typically two separate operations in standard Playwright (selector verification and assertion execution). The description of the Healer agent replaying "failing steps" and inspecting "current UI to locate equivalent elements" describes Playwright's test repair capabilities, but those may rely on code modification rather than pure runtime behavior — a meaningful distinction for the behavioral validation claim.
- **evidence:** "Playwright 1.56 (October 2025) introduced a native three-agent system that operates exclusively against live running applications... Generator Agent... 'verifies selectors and assertions live as it performs the scenarios,' meaning it executes interactions against the running UI rather than analyzing code statically." (research-behavioral-validation-ai-agents.md, "Playwright's Native Agent Architecture")
- **suggestion:** Verify the version and release date against Playwright's official changelog. Clarify whether "Healer" operates by modifying test source code (which would be a code change, not pure behavioral re-inspection) or by runtime inspection alone, as the distinction matters for the behavioral isolation argument the document makes.

---

### DOMAIN-007
- **id:** DOMAIN-007
- **severity:** medium
- **dimension:** domain_rule_compliance
- **location:** `research-cognitive-load-inversion.md:The Inversion Problem in Concrete Terms`
- **description:** The METR study finding is used in two contradictory ways across the corpus without reconciliation. In `research-cognitive-load-inversion.md`, the METR result is cited as: "experienced open-source developers working on their own repositories took 19% *longer* to complete tasks with AI tools — counter to the productivity narrative." In `research-work-granularity-ai-speed.md`, the same METR study is cited as showing "task completion times compressing dramatically." These two characterizations cannot both be accurate descriptions of the same study's primary finding. The granularity file uses METR to support the speed narrative; the cognitive load file uses it to challenge the speed narrative. This inconsistency — without a reconciling note — will confuse readers who follow both threads.
- **evidence:** Granularity file: "METR's July 2025 research on experienced open-source developers found task completion times compressing dramatically." (research-work-granularity-ai-speed.md, "The Core Problem") // Cognitive load file: "The 2025 METR randomized controlled trial found experienced open-source developers working on their own repositories took 19% *longer* to complete tasks with AI tools." (research-cognitive-load-inversion.md, "The Expertise Erosion Risk")
- **suggestion:** Reconcile by noting that METR's study had a nuanced result: aggregate task completion was longer with AI for these experienced developers on these specific task types. The granularity reference likely draws on the machine learning benchmark extrapolation (doubling horizon every four months) from a different data series, not the METR RCT directly. Clarify which data supports which claim and add a cross-reference between files.

---

## Dimension 2: Convention Adherence

### DOMAIN-008
- **id:** DOMAIN-008
- **severity:** medium
- **dimension:** convention_adherence
- **location:** `research-acceptance-criteria-ai-literal.md:The Core Problem`
- **description:** The primary citation for the "serializer-deserializer" example of AI literal implementation (a file format library implementing only a reader, not a writer) is marked `[UNVERIFIED — synthesized from arxiv.org/html/2503.22625v1]`. This same arxiv paper is then cited in the Sources section as `[OFFICIAL — arxiv.org/html/2503.22625v1]`. A finding marked UNVERIFIED in the body cannot be upgraded to OFFICIAL in the sources list without explicit verification happening between those two points. This is a citation integrity inconsistency — either the paper was verified and the body tag should say `[OFFICIAL]`, or it was not and the sources list must not mark it `[OFFICIAL]`.
- **evidence:** Body: "A concrete example from a paper studying real-world AI coding tasks illustrates this sharply... [UNVERIFIED — synthesized from arxiv.org/html/2503.22625v1]" // Sources: "- [Challenges and Paths Towards AI for Software Engineering — arxiv](https://arxiv.org/html/2503.22625v1) [OFFICIAL]" (research-acceptance-criteria-ai-literal.md)
- **suggestion:** Verify the paper and update the body tag to `[OFFICIAL]` with a read confirmation, or demote the sources entry to `[UNVERIFIED]` and add a note that the content was synthesized from search results about the paper, not from direct reading.

---

### DOMAIN-009
- **id:** DOMAIN-009
- **severity:** low
- **dimension:** convention_adherence
- **location:** `research-feature-unit-user-value.md:Section 1`
- **description:** The nkdagility.com citation is marked `[UNVERIFIED — site content summarized, URL: nkdagility.com/resources/value-delivery/]` but the statement it supports ("'Done' means live in production, not just code complete") is a standard practitioner principle widely documented elsewhere in the corpus. The UNVERIFIED tag is appropriate given the site's access issues, but the finding is so widely corroborated (AWS Prescriptive Guidance, DORA, PLG sources elsewhere in the same file) that the UNVERIFIED single citation adds no unique weight and slightly undermines the credibility of a claim that is well-supported.
- **evidence:** "The nkdagility.com value delivery resource reinforces this: 'Done' means live in production, not just code complete. [UNVERIFIED — site content summarized, URL: nkdagility.com/resources/value-delivery/]" (research-feature-unit-user-value.md, Section 1)
- **suggestion:** Either drop this citation entirely since the point is amply supported by verified sources in the same section, or access the page directly to verify, or replace with the Scrum.org definition of Done which is an official, accessible source.

---

### DOMAIN-010
- **id:** DOMAIN-010
- **severity:** low
- **dimension:** convention_adherence
- **location:** `research-feature-unit-user-value.md:Section 2`
- **description:** The Marty Cagan product-vs-feature-teams citation is marked `[UNVERIFIED — widely attributed to SVPG; svpg.com/product-vs-feature-teams/ returned 403]`. This is a specific foundational concept — the product team vs. feature team distinction — that is core to the section's argument. Relying on an inaccessible URL for a load-bearing conceptual distinction is a convention adherence gap. SVPG material is widely mirrored and the book "Empowered" (2020) is the authoritative source. The section should cite the book or an accessible secondary source.
- **evidence:** "Marty Cagan's distinction between product teams and feature teams... [UNVERIFIED — widely attributed to SVPG; svpg.com/product-vs-feature-teams/ returned 403]" (research-feature-unit-user-value.md, Section 2)
- **suggestion:** Replace the inaccessible URL with a citation to Cagan's book "Empowered" (2020, Wiley) or the SVPG book content that is accessible. The Age of Product secondary source already cited in this section (`age-of-product.com/marty-cagan-product-operating-model/`) may serve as the accessible substitute.

---

## Dimension 3: Fitness for Purpose

### DOMAIN-011
- **id:** DOMAIN-011
- **severity:** high
- **dimension:** fitness_for_purpose
- **location:** `research-behavioral-validation-ai-agents.md` — entire document
- **description:** The behavioral validation document is the corpus's strongest response to scope.md's third core problem (behavioral validation gap — testing running app not code-against-spec). However, it conflates two distinct problems throughout: (1) validating that AI agents do not cheat on evaluations (the NIST/CAISI cheating problem), and (2) validating that a running application delivers user value independent of how it was built. The NIST cheating research is about benchmark integrity for AI model evaluation, not about testing a production application for user-value delivery. A development team lead reading this document needs to know: what do I run against my deployed app to validate user value? The cheating section answers a different question: how do I prevent my AI coding agent from gaming its own tests during development? These are both important but they are different problems, and mixing them obscures the actionable guidance for each.
- **evidence:** "NIST's Center for AI Standards and Innovation (CAISI) has documented a closely related failure mode: AI agents will cheat on evaluations if given the opportunity to do so." followed immediately by "The prevention principle that emerged from CAISI's research: **technical isolation is not optional**. The coding agent must not know how tests are performed; the testing agent must not know what the implementation looks like. Only then can the running application serve as the neutral ground of truth." (research-behavioral-validation-ai-agents.md, "The Cheating Problem") — NIST's cheating research is about benchmark evaluation integrity, not about validating production user value.
- **suggestion:** Restructure or annotate the document with two explicit sub-problems: (A) preventing the coding agent from gaming its own tests during development (the NIST cheating / Codecentric isolated testing pattern), and (B) validating that a deployed running application delivers user value (the Playwright, QA.tech, Blok, canary deployment patterns). Keep the NIST material but clearly scope it to problem A. This makes the document immediately actionable for a dev team lead who needs to answer "what do I actually run?"

---

*Re-examination note: After initial pass, one additional finding (DOMAIN-007) was identified on re-examination of cross-file consistency, and the DOMAIN-001 severity was escalated from high to critical based on the combination of unverifiable provenance and inflated causal claim. No finding quota was applied — findings reflect observed issues only.*
