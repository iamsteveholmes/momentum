# Coherence & Craft — Enumerator Findings

**Lens:** Coherence & Craft  
**Reviewer:** ENUMERATOR — systematic dimension-by-dimension validation  
**Corpus:** 9 files — 1 Gemini Deep Research output + 8 subagent research files  
**Date validated:** 2026-04-13  

## Summary

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 5 |
| Medium | 8 |
| Low | 6 |
| **Total** | **19** |

---

## Dimension 1: Consistency (within-document)

---

- id: COHERENCE-001
- severity: high
- dimension: consistency
- location: gemini-deep-research-output.md:Follow-Up Q1
- description: The Gemini document attributes "Harness Engineering" solely to Fowler and Böckeler in the main body, but the ceremony file attributes a detailed Harness Engineering model to OpenAI (Codex team). The two uses of "Harness Engineering" describe fundamentally different things — Fowler/Böckeler's model is a metaphor for constraining AI output; OpenAI's is an operational workflow model for a specific engineering team — yet both are called "Harness Engineering" within the corpus without disambiguation, creating a false impression of a unified concept.
- evidence: gemini-deep-research-output.md body: "Martin Fowler and Birgitta Böckeler have introduced 'Harness Engineering' as a mental model for managing coding agents." — research-ceremony-rhythm-alternatives.md: "OpenAI's Harness Engineering model, documented in February 2026, describes how the Codex team operates with AI agents as the primary contributors."
- suggestion: In the synthesis or final document, disambiguate: Fowler/Böckeler's "Harness Engineering" is a conceptual framework; OpenAI's is a specific team workflow. They share a name but describe different things. A note in at least one of the files clarifying the naming collision would prevent readers from conflating them.

---

- id: COHERENCE-002
- severity: medium
- dimension: consistency
- location: research-thought-leader-frameworks-agile-ai.md:Casey West section
- description: The document says Casey West's Agentic Manifesto was proposed in "2025" (under the heading "Casey West's Agentic Manifesto") and attributes the framework to "caseywest.com, 2025." The Gemini document says the Agentic Manifesto was "proposed by Casey West in early 2026." These are contradictory dates for the same named artifact.
- evidence: research-thought-leader-frameworks-agile-ai.md: "Casey West's Agentic Manifesto (2025) proposes an Agentic Delivery Lifecycle (ADLC)... [PRAC — caseywest.com, 2025]" — gemini-deep-research-output.md: "The 'Agentic Manifesto,' proposed by Casey West in early 2026, argues for a fundamental shift from verification to validation."
- suggestion: Verify the actual publication date of the Agentic Manifesto against the source (caseywest.com). One of these is wrong. Correct the incorrect file and apply the verified date consistently.

---

## Dimension 2: Relevance (document addresses its stated sub-question)

---

- id: COHERENCE-003
- severity: medium
- dimension: relevance
- location: research-feature-unit-user-value.md:sections 3–9
- description: The sub-question asks specifically "how do leading teams define and enforce a done state at the value-delivery level." Sections 3–9 (Outcome-Based Roadmaps, Progressive Delivery, Impact Mapping, JTBD, PLG, VSM, DORA) provide broad survey coverage of outcome-measurement frameworks in general. Only the Red Hat Harness Engineering reference (section 10) and the AWS definition (section 2) actually provide evidence of teams enforcing a value-level done gate in practice. The middle six sections read as background context on product management frameworks rather than evidence of how "leading teams" actually enforce done. The scope drifts from "how do teams enforce" to "what frameworks exist."
- evidence: Section heading states sub-question is "how do leading teams define and enforce a done state at the value-delivery level." Section 7 (PLG) opens: "Product-Led Growth (PLG) organizations have developed the most operationalized version of value-based done" — but the section content describes the PLG model generically, not AI-native team practice specifically.
- suggestion: Tighten sections 3–9 by adding a connecting sentence per section that explicitly links each framework to the sub-question: how does this framework change when AI accelerates delivery? Without this, the sections answer "what frameworks exist for outcome measurement" rather than "how AI-native teams enforce value-delivery done."

---

- id: COHERENCE-004
- severity: low
- dimension: relevance
- location: research-behavioral-validation-ai-agents.md:Visual Regression Testing section
- description: Visual regression testing is presented as a behavioral validation layer with significant coverage. While peripherally related to "testing a running application," it primarily validates rendering fidelity, not the behavioral intent of AI-generated features. The sub-question focuses on approaches that test running application behavior against user value. Visual regression is more accurately a UI correctness tool than a behavioral validation approach for the "spec-correct, value-zero" problem.
- evidence: Sub-question: "behavioral validation and end-to-end testing approaches...that test a running application rather than validating code against spec." Section states: "Visual regression testing has matured into a behavioral validation layer that specifically tests what users see rather than what code produces." The claim that visual regression tests "behavioral" properties stretches the term beyond its normal meaning in the context of user-value validation.
- suggestion: Reframe the visual regression section as a complementary layer (UI correctness) rather than a primary behavioral validation approach, or add a sentence explicitly connecting visual regressions to user-value failures (e.g., a layout breakage that makes a feature unusable is a value failure even if the logic is correct).

---

## Dimension 3: Conciseness (padding, repetition, unnecessary restatement)

---

- id: COHERENCE-005
- severity: medium
- dimension: conciseness
- location: research-spec-correct-value-zero.md and research-acceptance-criteria-ai-literal.md
- description: Both files contain near-identical coverage of Spec-Driven Development (SDD), including the same Thoughtworks "key new AI-assisted engineering practice" quote, the same three-level spectrum (spec-first / spec-anchored / spec-as-source) from the February 2026 arxiv paper, and the same core framing of SDD as the primary solution. As standalone research documents this is expected, but the redundancy is significant enough to reduce the corpus's information density when read as a whole.
- evidence: research-spec-correct-value-zero.md: "The arxiv study (February 2026) proposes a three-level spectrum: Spec-First: Initial specs guide development...Spec-Anchored: Specifications evolve alongside code...Spec-as-Source: Humans edit specifications only..." — research-acceptance-criteria-ai-literal.md: The same document (research-thought-leader-frameworks-agile-ai.md) also contains a "three-level progression: Spec-first...Spec-anchored...Spec-as-source" from Birgitta Böckeler's 2026 article. All three files cover this spectrum from slightly different angles using the same source material.
- suggestion: In the synthesis/final document, present the three-level SDD spectrum once with cross-references. For the raw files as they stand, a brief note at the start of each file's SDD section acknowledging the cross-coverage would reduce reader confusion.

---

- id: COHERENCE-006
- severity: medium
- dimension: conciseness
- location: research-work-granularity-ai-speed.md:Synthesis section and research-ceremony-rhythm-alternatives.md:Synthesis section
- description: Both synthesis sections describe the same shift ("constraint has moved from implementation to decision-making/validation") using nearly identical framing, referencing the same sources (Siderova, Giles Lindsay). The repetition is structurally necessary given the files are standalone, but it adds significant word count without new information when read as a corpus.
- evidence: research-work-granularity-ai-speed.md Synthesis: "The two-week sprint is not dead but is evolving toward a governance cadence (review assumptions, reassess priorities) rather than a delivery cadence." — research-ceremony-rhythm-alternatives.md Synthesis: "The Bottleneck Has Moved. Multiple independent sources (Agile Delta, Futurice, longitudinal arXiv research) identify the same shift: AI removes implementation as the constraint and installs human decision-making bandwidth as the new constraint."
- suggestion: This is acceptable at the raw-file level. In the final synthesis document, merge these sections so the "constraint has moved" insight is stated once, prominently, rather than repeated in parallel files.

---

- id: COHERENCE-007
- severity: low
- dimension: conciseness
- location: research-cognitive-load-inversion.md:Empirical Data on the Trust Gap section
- description: The trust-gap statistics are reported in three separate sub-sections with overlapping data: "only 29% of developers trust AI output" (Stack Overflow), "96% of developers do not fully trust AI-generated code — yet only 48% always check it" (Talent500), and "only 26% of senior engineers would ship AI-generated code without review" (LogRocket). These are three data points making essentially the same point. The section could be condensed to one paragraph without losing substantive information.
- evidence: "A 2025 Stack Overflow survey found only 29% of developers trust AI output in 2025, down 11 percentage points from 2024. Separately, 96% of developers report they do not fully trust AI-generated code — yet only 48% say they always check it before committing... Only 26% of senior engineers would ship AI-generated code without review..."
- suggestion: Merge the three trust-gap data points into a single paragraph: "Multiple 2025 surveys confirm a trust-behavior gap: X% do not fully trust AI code (Talent500), only Y% check before committing, and only Z% of senior engineers would ship without review (LogRocket). The pattern holds across sources." This eliminates the repetitive structure without losing any data.

---

- id: COHERENCE-008
- severity: low
- dimension: conciseness
- location: research-behavioral-validation-ai-agents.md:Key Design Principles section
- description: Principle 1 ("Technical separation between builder and validator") is also fully covered in the preceding "Isolated Specification Testing: A Proven Architectural Pattern" section with more detail. The principles section largely restates points made in the body sections above it. At least three of the six principles are direct condensations of already-presented material.
- evidence: Principles section: "Technical separation between builder and validator. The agent that wrote the code must not be able to read the test artifacts..." — Isolated Specification Testing section: "A .claudeignore file prevents the coding agent from reading test scenarios, forcing it to implement against the specification... A settings.json permissions file explicitly denies the testing agent access to source code directories."
- suggestion: Principles sections in research documents serve as useful summaries. Either (a) mark this section explicitly as "Summary of principles from above" to signal its role, or (b) cut the body coverage of principles that are fully captured here and let the principles section be the primary treatment.

---

## Dimension 4: Clarity

---

- id: COHERENCE-009
- severity: high
- dimension: clarity
- location: gemini-deep-research-output.md:The Specification-Completeness Problem section
- description: The document uses "Intent Design" in two conflicting ways without flagging the ambiguity. In one instance it attributes "Intent Design" to AWS as a process for turning requirements into architecture: "This process is what AWS calls 'Intent Design'. In this model, architecture becomes 'scaffolding'." Later in the document and in Follow-Up Q2, "Intent Design" is used generically as a synonym for spec-driven development. The Gemini document doesn't reconcile these two uses.
- evidence: gemini-deep-research-output.md body: "This process is what AWS calls 'Intent Design'. In this model, architecture becomes 'scaffolding'." — research-work-granularity-ai-speed.md: "AWS proposed 'Intent Design' as an alternative to sprint planning, framing architecture as scaffolding that defines roles, guardrails, and fallback mechanisms." — gemini-deep-research-output.md Follow-Up Q2: describes "intent-driven.dev community" using "Intent Design" generically without noting this is different from AWS's specific term.
- suggestion: Use "AWS Intent Design" when referring specifically to AWS's prescriptive guidance, and "intent-driven development" generically. Flag that the term is used variably in the field.

---

- id: COHERENCE-010
- severity: medium
- dimension: clarity
- location: research-ceremony-rhythm-alternatives.md:Harness Engineering section
- description: The section title is "Harness Engineering: A Practitioner Model from OpenAI" and attributes the model to OpenAI, yet the cited source is openai.com/index/harness-engineering/. The term "Harness Engineering" was introduced by Fowler and Böckeler (cited across multiple files). Attributing "Harness Engineering" to OpenAI as if they coined or own the term is misleading to the reader. OpenAI applied the concept; they did not originate it.
- evidence: research-ceremony-rhythm-alternatives.md: "[OFFICIAL] OpenAI's Harness Engineering model, documented in February 2026..." — research-thought-leader-frameworks-agile-ai.md: "The 'Humans On the Loop' model...is a direct application of 'shift left' thinking to AI governance" (Fowler's harness concept); gemini-deep-research-output.md: "Martin Fowler and Birgitta Böckeler have introduced 'Harness Engineering' as a mental model..."
- suggestion: Rename the section heading to "OpenAI's Harness-Engineering-Inspired Model" or "OpenAI: Applying Harness Engineering at Scale" and add a sentence noting that the harness engineering concept originates with Fowler/Böckeler, not OpenAI.

---

- id: COHERENCE-011
- severity: medium
- dimension: clarity
- location: research-acceptance-criteria-ai-literal.md:EARS Notation section
- description: The section states "Amazon's Kiro IDE, which launched public preview in July 2025, made EARS central to its spec-driven workflow." The Kiro IDE is attributed to Amazon throughout this file and research-work-granularity-ai-speed.md, but Kiro is described as an AWS product (kiro.dev). The company name alternates between "Amazon" and "AWS" across files, creating ambiguity about whether Kiro is an AWS service, an Amazon product division product, or a separate offering. Practitioners reading this as a reference would be confused about how to find or evaluate Kiro.
- evidence: research-acceptance-criteria-ai-literal.md: "Amazon's Kiro IDE" — research-work-granularity-ai-speed.md: "AWS's Kiro IDE (2025) implements spec-driven development as a three-stage pipeline" — research-thought-leader-frameworks-agile-ai.md: "AWS Kiro: Spec-Driven as IDE Philosophy" with source "aws.amazon.com, 2025"
- suggestion: Standardize to "AWS Kiro" throughout the corpus, or if the research establishes it is marketed as a standalone product at kiro.dev (not directly branded AWS), note that. Eliminate the "Amazon's Kiro" attribution variant.

---

## Dimension 5: Tonal Consistency

---

- id: COHERENCE-012
- severity: medium
- dimension: tonal_consistency
- location: research-cognitive-load-inversion.md:The "Vibe Coding" Failure Mode section
- description: The section contains an editorial aside that breaks research register: "Vibe coding is not the norm, but it illuminates the failure mode that review-light adoption slides toward when volume pressure wins." The phrase "slides toward when volume pressure wins" is editorial commentary on organizational behavior, not documented research finding. The surrounding text maintains research tone, making this aside jarring.
- evidence: "Vibe coding is not the norm, but it illuminates the failure mode that review-light adoption slides toward when volume pressure wins."
- suggestion: Rewrite as: "Vibe coding represents an extreme, but it documents the failure modes that emerge when review processes are not adapted to AI development velocity." This maintains the analytical observation without the opinion-laden "pressure wins" framing.

---

- id: COHERENCE-013
- severity: low
- dimension: tonal_consistency
- location: research-spec-correct-value-zero.md:What Practitioners Report Is Not Working section
- description: The section header "What Practitioners Report Is Not Working" uses informal voice inconsistent with the document's otherwise formal academic tone. Other section headers in the same document use gerund phrases or noun phrases ("Solution Pattern 1:", "Synthesis:"). This header stands out as informally constructed.
- evidence: Section header: "What Practitioners Report Is Not Working" — contrast with sibling headers: "Solution Pattern 1: Spec-Driven Development (SDD)", "The 'Working Software' Question", "Synthesis: A Framework for Closing the Gap"
- suggestion: Rename to "Documented Failure Patterns" or "Known Failure Modes in Practice" to maintain the research register.

---

- id: COHERENCE-014
- severity: low
- dimension: tonal_consistency
- location: research-feature-unit-user-value.md:Section 3
- description: The document uses a direct quote from a practitioner blog in an endorsing rather than analytical manner: "Steve Forbes (practitioner blog, 2025) captures the cultural flip: 'Feature-based roadmaps celebrate delivery dates. Outcome-led roadmaps celebrate movement in metrics.'" The word "captures" signals alignment with the quoted view rather than neutral citation. Most of the document uses neutral citation language ("argues," "identifies," "describes"). A few similar instances appear throughout.
- evidence: "Steve Forbes (practitioner blog, 2025) captures the cultural flip..." — contrast with surrounding citations: "Teresa Torres...describes how this enforces accountability", "Product School's treatment...describes the enforcement mechanisms"
- suggestion: Replace "captures" with "articulates" or "frames this as" to maintain analytical distance from the cited position.

---

## Dimension 6: Temporal Coherence

---

- id: COHERENCE-015
- severity: high
- dimension: temporal_coherence
- location: research-thought-leader-frameworks-agile-ai.md:Sources
- description: One source citation links to "martinfowler.com/articles/202508-ai-thoughts.html" — this URL contains "202508" suggesting an August 2025 publication date. This is consistent with the research cutoff and April 2026 date. However, the article title cited is "Some thoughts on LLMs and Software Development" — a generic title that could refer to several Fowler pieces. More critically, in the sources section this is listed under OFFICIAL but the main text never cites this article directly. A citation in the sources list that is never referenced in the body creates bibliographic padding.
- evidence: Sources section: "[Some thoughts on LLMs and Software Development — martinfowler.com](https://martinfowler.com/articles/202508-ai-thoughts.html) [OFFICIAL]" — scanning the document body, no section directly attributes a claim to this specific URL.
- suggestion: Either cite this article in the body for a specific claim it supports, or remove it from the sources list. Orphaned bibliography entries reduce credibility.

---

- id: COHERENCE-016
- severity: medium
- dimension: temporal_coherence
- location: research-ceremony-rhythm-alternatives.md:Shape Up section
- description: The section contains an unusual self-annotation: "Shape Up, developed by Basecamp and published by Ryan Singer in 2019 (note: original publication is older than two years, but adoption in AI contexts is being discussed in 2025-2026)." This parenthetical note, while technically accurate, reads as an artifact of the research process (the subagent defending its inclusion of older material) rather than a natural part of the document. It is an internal research note that leaked into the final text.
- evidence: "Shape Up, developed by Basecamp and published by Ryan Singer in 2019 (**note: original publication is older than two years, but adoption in AI contexts is being discussed in 2025-2026**)"
- suggestion: Remove the parenthetical note. Replace with a clean statement: "Shape Up (Basecamp, Ryan Singer, 2019) has attracted renewed practitioner interest in 2025-2026 as an AI-compatible alternative to Scrum." The temporal framing belongs in the narrative, not in a defensive aside.

---

## Dimension 7: Cross-Document Consistency

---

- id: COHERENCE-017
- severity: high
- dimension: cross_document_consistency
- location: research-thought-leader-frameworks-agile-ai.md:DORA 2025 section vs. research-cognitive-load-inversion.md:DORA reference
- description: The two files report different statistics from the same 2025 DORA report on AI adoption at work. The thought-leader-frameworks file reports "90% of respondents use AI at work; median 2 hours/day interacting with AI." The cognitive-load-inversion file does not contradict this, but attributes the DORA report to "nearly 5,000 technology professionals" (at the end of the document) while the feature-unit-user-value file says the 2025 DORA report had a different scope without specifying the sample size. More concretely, the cognitive-load-inversion file cites "a 2025 Stack Overflow survey found only 29% of developers trust AI output" as a distinct source, while the thought-leader-frameworks file's DORA section states "30% of respondents report little to no trust in AI-generated code." These are close but not identical figures, attributed to different sources (DORA vs. Stack Overflow), and presented as independent findings when they may describe the same population trend.
- evidence: research-thought-leader-frameworks-agile-ai.md: "30% of respondents report little to no trust in AI-generated code." [OFFICIAL, DORA 2025] — research-cognitive-load-inversion.md: "A 2025 Stack Overflow survey found only 29% of developers trust AI output in 2025, down 11 percentage points from 2024." [PRAC, Stack Overflow]
- suggestion: These are likely distinct surveys with coincidentally similar numbers. Add a brief note in whichever file appears in the synthesis stating that multiple 2025 surveys (DORA, Stack Overflow) independently converge on approximately 30% trust — this turns the near-coincidence into evidence of a robust finding rather than leaving readers to wonder if the same data is being double-counted.

---

- id: COHERENCE-018
- severity: high
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:Behavioral Validation section vs. research-behavioral-validation-ai-agents.md:TDA section
- description: The Gemini document describes "Test-Driven AI (TDA)" and its "red phase" as an evolution of TDD, attributing it to "Kent Beck and others." The subagent behavioral-validation file does not use the term "TDA" at all — it describes the same concept as "Red/Green TDA" only when citing the Gemini follow-up Q2, not as a standalone concept. The thought-leader-frameworks file attributes "TDD as a hard constraint" to Beck without naming TDA. The term "TDA" (Test-Driven AI) is introduced in the Gemini document as if it is an established named practice, but no other file validates or uses this term, making it appear to be either a Gemini-coined label or an obscure term. If it is a genuine named practice, it should appear consistently; if it is Gemini's framing, that should be flagged.
- evidence: gemini-deep-research-output.md: "However, the methodology has evolved into 'Test-Driven AI' (TDA). A critical component of TDA is the 'red' phase..." — research-behavioral-validation-ai-agents.md: Does not use "TDA" — uses "Red/Green TDA" only in a quote from the Gemini follow-up section, not as an independently validated term. — research-thought-leader-frameworks-agile-ai.md: "TDD as a hard constraint" (Kent Beck) — no mention of "TDA."
- suggestion: If TDA is a term appearing in the sources the Gemini document cited (thelaziest.dev, suchakjani.medium.com), note the source. If it is Gemini's framing of an unnamed practice, flag it as such in the synthesis. Either way, decide whether to use "TDA" consistently as a corpus term or avoid it as an unvalidated label.

---

- id: COHERENCE-019
- severity: medium
- dimension: cross_document_consistency
- location: research-work-granularity-ai-speed.md:Shape Up section vs. gemini-deep-research-output.md:Follow-Up Q1
- description: The two files describe Shape Up's "appetite" concept with subtly inconsistent characterizations. The work-granularity file describes appetite as "fixed time budget that constrains scope rather than estimating implementation" and notes it is a Ryan Singer concept from 2019. The Gemini follow-up Q1 describes Shape Up adoption as including "a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)" — attributed to "Silken Net" — but this hybrid is not mentioned in the work-granularity file's Shape Up section, which treats Shape Up as a standalone adoption. More significantly, the Gemini file says teams have "completely overhauled their architecture, abandoning Agile for a hybrid of Shape Up and NASA's TRL" — presenting it as a clean break from Agile. The work-granularity file's synthesis describes Shape Up as complementary: "Shape Up's shaping discipline + AI agent execution during the build phase + continuous deployment replaces the traditional sprint-based backlog-to-release pipeline" — a softer framing that does not describe abandonment of Agile.
- evidence: gemini-deep-research-output.md Q1: "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)." — research-work-granularity-ai-speed.md Synthesis: "Shape Up's shaping discipline + AI agent execution during the build phase + continuous deployment replaces the traditional sprint-based backlog-to-release pipeline." (no mention of NASA TRL hybrid)
- suggestion: In the synthesis or final document, note that Shape Up adoption ranges from partial integration (supplementing sprint-based planning) to full abandonment of Agile (Silken Net example). The spectrum of adoption should be stated explicitly rather than each file implying a uniform posture.

---

*End of findings. 19 total findings across 7 dimensions.*
