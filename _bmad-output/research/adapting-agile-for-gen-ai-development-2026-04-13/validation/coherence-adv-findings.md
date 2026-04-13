# Coherence & Craft — Adversary Findings

**Lens:** Coherence & Craft (Adversary, Skepticism Level 3)
**Stage:** Final
**Mode:** Corpus (9 files)
**Date:** 2026-04-13

## Summary

| Severity | Count |
|---|---|
| Critical | 2 |
| High | 6 |
| Medium | 6 |
| Low | 4 |
| **Total** | **18** |

The corpus has narrative drift between the Gemini synthesis and the eight subagent files on three load-bearing concepts: **Harness Engineering** (three different attributions), **AI-DLC operating model** (Mob rituals vs. Validators vs. three-phase Inception/Construction/Operations), and **Shape Up adoption** (Gemini claims a real adopter that the ceremony file says does not exist in the literature). The Casey West Agentic Manifesto is dated inconsistently (2025 vs. early 2026). The Gemini file also internally contradicts itself on AI-DLC rituals. Several editorial seams remain (a "the researcher's 'Feature' concept" reference, promotional ™ marks, three different paraphrases of the same Sonya Siderova quote). EARS notation — central to the acceptance-criteria file — is entirely absent from the Gemini synthesis that purports to summarize the corpus.

---

## Findings

- id: COHERENCE-001
- severity: critical
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Harness Engineering and the Cybernetic Governor" / research-ceremony-rhythm-alternatives.md:"Harness Engineering: A Practitioner Model from OpenAI" / research-feature-unit-user-value.md:"AI-Native Development: Amplifying the Gap"
- description: The term "Harness Engineering" is attributed to three different originators across the corpus, and a reader comparing the documents will not be able to determine who actually coined or owns the concept. The Gemini synthesis credits Fowler/Böckeler; the ceremony file credits OpenAI's Codex team; the feature-unit file credits Red Hat Developer. None of the three files acknowledges the others' attribution.
- evidence:
  - Gemini: "Martin Fowler and Birgitta Böckeler have introduced 'Harness Engineering' as a mental model for managing coding agents. This approach externalizes the implicit skills and 'aesthetic disgust' humans bring to code... into a structured 'harness' that surrounds the AI model."
  - Ceremony file: "OpenAI's Harness Engineering model, documented in February 2026, describes how the Codex team operates with AI agents as the primary contributors."
  - Feature-unit file: "The Red Hat Developer article on harness engineering (April 2026) points toward a specific enforcement mechanism for AI-native development: structured harnesses that require acceptance criteria to be grounded in measurable outcomes..."
- suggestion: Unify attribution across the corpus. If Fowler/Böckeler coined "Harness Engineering" and OpenAI/Red Hat later adopted/extended it, say so explicitly. If they are independent uses of the same phrase, flag the terminology collision. The current state will confuse any reader who reads more than one file.

- id: COHERENCE-002
- severity: critical
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Mob Elaboration and Construction" / research-ceremony-rhythm-alternatives.md:"AWS AI-DLC: An Official Framework to Replace Agile Phases"
- description: The two files describe AWS's AI-DLC framework with mutually exclusive operational models. Gemini says AI-DLC's primary rituals are "Mob Elaboration" and "Mob Construction" (full-team synchronous events). The ceremony file describes AI-DLC as having three top-level phases (Inception, Construction, Operations) with no mob rituals and explicitly says "Human oversight embedded at decision points, not at calendar intervals." A reader cannot tell whether AI-DLC is mob-based or phase-based.
- evidence:
  - Gemini: "The AI-Driven Development Lifecycle (AI-DLC) recommends 'Mob Elaboration' and 'Mob Construction' rituals to manage this load... | Mob Elaboration | Product Owner, Devs, QA, Stakeholders | Proposes breakdown of 'Intent' into Stories and Units. | Validates business accuracy..."
  - Ceremony file: "The framework has three top-level phases: 1. **Inception** — planning and architecture (AI + human collaborative) 2. **Construction** — design and implementation (AI-primary, human oversight) 3. **Operations** — deployment and monitoring (AI-continuous, human governance) Critical differences from Agile: No fixed sprint cadences..."
- suggestion: Reconcile the two descriptions. If Mob Elaboration/Construction are layered inside the Inception/Construction phases, say so. If one source is from AWS's prescriptive guidance and the other from the open-source aidlc-workflows repo, distinguish them explicitly.

- id: COHERENCE-003
- severity: high
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Follow-Up Q1: Arguments for Abandoning Agile Entirely" (Shape Up section) / research-ceremony-rhythm-alternatives.md:"Shape Up as an AI-Compatible Alternative"
- description: The Gemini follow-up cites a specific company (Silken Net) as having "completely overhauled their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels." The ceremony file directly contradicts this, saying no published cases exist of Shape Up applied to human-AI agent teams. One of the two claims must be wrong; both cannot be true.
- evidence:
  - Gemini: "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL). Because AI development is non-linear and prone to 'rabbit holes,' fixing the 'appetite' (time budget) is more effective than estimating tasks an AI might finish in seconds or struggle with for hours."
  - Ceremony file: "However, no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team. The fit is structural, not yet empirically validated in that context."
- suggestion: Verify the Silken Net claim. If unsubstantiated, remove it from the Gemini follow-up. If verified, update the ceremony file's "no published cases" claim. Either way, the corpus must speak with one voice on whether Shape Up has documented AI-team adoption.

- id: COHERENCE-004
- severity: high
- dimension: cross_document_consistency
- location: research-thought-leader-frameworks-agile-ai.md:"Casey West's Agentic Manifesto" (Sources line) / gemini-deep-research-output.md:"Solving the 'Spec-Correct, Value-Zero' Problem" and Q1
- description: The Casey West Agentic Manifesto is dated 2025 in the frameworks file (both inline header tag and source citation) and "early 2026" in the Gemini file. This is a clean temporal contradiction on the same artifact.
- evidence:
  - Frameworks file (Sources): "[The Agentic Manifesto — Casey West](https://caseywest.com/the-agentic-manifesto/) [PRAC]" with the section header "Casey West's Agentic Manifesto" and inline citation "[PRAC — caseywest.com, 2025]"
  - Frameworks file (header): "Casey West's **Agentic Manifesto** (2025)"
  - Gemini main text: "The 'Agentic Manifesto,' proposed by Casey West in early 2026, argues for a fundamental shift from verification to validation."
  - Gemini Q1: "Proposed in early 2026 as a direct response to Agile friction."
- suggestion: Determine the actual publication date and use it consistently. If the manifesto was published in 2025 and gained traction in early 2026, say "published 2025; gained mainstream attention early 2026" rather than mis-dating the proposal itself.

- id: COHERENCE-005
- severity: high
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Restructuring Work Granularity" + Q1 / research-feature-unit-user-value.md:"AI-Native Development: Amplifying the Gap"
- description: The corpus attributes the term "Bolts" to two different sources without acknowledging the discrepancy. Gemini claims it comes from AWS's AI-DLC prescriptive guidance. The feature-unit file traces it to a DEV Community article. This matters because "Bolts" is one of the most-cited replacement-for-sprints terms in the corpus — readers need to know whose vocabulary it is.
- evidence:
  - Gemini Q1: "AWS has released prescriptive guidance for the AI-Driven Development Lifecycle (AI-DLC)... From Sprints to Bolts: AI-DLC officially abandons the sprint in favor of 'Bolts' — high-velocity execution cycles measured in hours or days rather than weeks."
  - Feature-unit file: "The DEV Community analysis of AI-powered development workflows in 2026 identifies a specific structural change: 'Traditional 'sprints' are being replaced by 'bolts' — shorter, more intense work cycles measured in hours or days rather than weeks.' [PRAC — dev.to/devactivity/the-ai-powered-development-workflow-a-glimpse-into-2026-4h68]"
- suggestion: Clarify whether AWS uses "Bolts" in its official AI-DLC documentation or whether it is a community gloss. The ceremony file's AI-DLC section never uses the word "Bolts" while describing the same framework — strengthening the suspicion that this is community vocabulary, not AWS's.

- id: COHERENCE-006
- severity: high
- dimension: cross_document_consistency
- location: research-thought-leader-frameworks-agile-ai.md:"The InfoQ Debate" / research-spec-correct-value-zero.md:"The Verification-Validation Collapse" / research-work-granularity-ai-speed.md:"The Upstream Bottleneck Shift"
- description: Sonya Siderova is quoted from the same InfoQ piece in three files with three substantively different paraphrases/quotes. The frameworks and work-granularity files use the short epigram form; the spec-correct file uses a much longer "the bottleneck moved from..." quote that reads as a paraphrase but is presented in quotation marks. A reader cannot determine what Siderova actually said.
- evidence:
  - Frameworks file: "Sonya Siderova, Nave CEO): 'Agile isn't dead. It's optimizing a constraint that moved.' The bottleneck shifted from human collaboration to validation and decision-making."
  - Work-granularity file: "Sonya Siderova, writing on the InfoQ Agile Manifesto debate, frames it precisely: 'Agile isn't dead. It's optimizing a constraint that moved.'"
  - Spec-correct file: "the InfoQ report on the AI and Agile Manifesto debate quotes Sonya Siderova: 'the bottleneck moved from \"how do humans collaborate to build\" to \"how do humans decide what to build and validate it actually works.\"'"
- suggestion: Verify the actual Siderova quote and standardize. The third version is likely a paraphrase that has been wrapped in quotation marks — treat as paraphrase or excise.

- id: COHERENCE-007
- severity: high
- dimension: consistency
- location: gemini-deep-research-output.md:"The AI/works Platform and the 3-3-3 Model" vs "Mob Elaboration and Construction"
- description: Internal contradiction within the Gemini file on AI-DLC's operating model. The 3-3-3 table credits "Mob Elaboration" and "Mob Construction" as the primary rituals of the Thoughtworks 3-3-3 phases. Later, the same file credits "Mob Elaboration" and "Mob Construction" to AWS's AI-DLC. The follow-up Q1 then describes AI-DLC as "AI initiates by proposing plans, humans act as 'Validators'" — a single-validator model fundamentally different from a mob ritual. The same file therefore presents AI-DLC as both mob-based and validator-based, and presents Mob rituals as belonging to both Thoughtworks 3-3-3 and AWS AI-DLC.
- evidence:
  - Gemini 3-3-3 table: "| Concept Alignment | 3 Days | ... | Mob Elaboration | | Functional Prototype | 3 Weeks | ... | Mob Construction |"
  - Gemini AI-DLC section: "The AI-Driven Development Lifecycle (AI-DLC) recommends 'Mob Elaboration' and 'Mob Construction' rituals to manage this load."
  - Gemini Q1 on AI-DLC: "Reversed Direction: Unlike Agile's 'human-commands, AI-executes' model, AI-DLC operates where AI initiates by proposing plans, humans act as 'Validators' confirming intent and managing risk."
- suggestion: Disentangle the two frameworks. Mob Elaboration/Construction appear to be Thoughtworks vocabulary tied to 3-3-3, not AWS AI-DLC. Move them out of the AI-DLC section, or distinguish "AWS AI-DLC's recommended rituals" from "the AI-DLC pattern's recommended rituals" if those are different things.

- id: COHERENCE-008
- severity: high
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"The Specification-Completeness Problem" / research-acceptance-criteria-ai-literal.md:"EARS Notation: Structured Acceptance Criteria for Machine Parsing"
- description: The acceptance-criteria file makes EARS notation (Easy Approach to Requirements Syntax) load-bearing — it is presented as "the most concrete tooling response to specification completeness" with a full section. The Gemini synthesis, which is supposed to summarize the corpus on exactly this topic, never mentions EARS at all. A reader of the Gemini summary will miss what the subagent file presents as the central technical answer to the AC question.
- evidence:
  - Acceptance-criteria file: "The most concrete tooling response to specification completeness is the adoption of **EARS notation** (Easy Approach to Requirements Syntax) as the format for acceptance criteria in AI-assisted development. Amazon's Kiro IDE... made EARS central to its spec-driven workflow. EARS structures requirements as formal conditional statements: 'When [condition], the system shall [behavior].'"
  - Gemini covers the same topic ("Replacing Acceptance Criteria") and discusses Super-Specs, Intent Design, Executable Instruction tables — but does not mention EARS, Kiro, "When/shall," or property-based test generation from EARS.
- suggestion: Either add an EARS reference to the Gemini synthesis or flag explicitly that the synthesis omits EARS-based approaches. As written, the Gemini file misrepresents the corpus by silently dropping the most concrete tooling answer.

- id: COHERENCE-009
- severity: medium
- dimension: tonal_consistency
- location: gemini-deep-research-output.md (multiple sections referencing AI/works™)
- description: The Gemini file repeatedly uses the trademark symbol "AI/works™" and adopts the vendor's promotional framing ("heralds a new era," "industrial-grade piece of technology," "ends the multi-million dollar cycle"). This breaks the research/analytic tone maintained by the eight subagent files, which describe the same product in measured terms.
- evidence:
  - Gemini: "Thoughtworks has codified this shift through the launch of AI/works™, an agentic development platform..."
  - Gemini: "AI/works™ extends that lineage into the AI era..."
  - Gemini: "Platforms like AI/works™ do not merely 'complete' a project; they continuously regenerate affected components..."
  - Gemini: "ship a production-ready, industrial-grade piece of technology into live environments"
  - Frameworks file (same product, measured): "In early 2026, Thoughtworks launched **AI/works**, an agentic development platform that operationalizes their emerging methodology... Ingests legacy codebases, reconstructs business logic, and generates validated as-is specifications before adding new code."
- suggestion: Strip ™ marks and vendor-promotional phrasing from the Gemini file. Match the analytic tone of the rest of the corpus.

- id: COHERENCE-010
- severity: medium
- dimension: clarity
- location: research-feature-unit-user-value.md:"Synthesis: What 'Feature as Unit of User Value' Requires in Practice" (final paragraph)
- description: Editorial scaffolding leak — the file's closing paragraph references "the researcher's 'Feature' concept" without context. This phrase belongs to the meta-conversation between the orchestrator and the subagent (the requester defined the concept of "Feature"), not to a research output. Any external reader will be confused by the unexplained "the researcher" and the capitalized 'Feature' as if it were a defined term in the document, which it is not.
- evidence:
  - Feature-unit file: "The notable absence in most current practice is a formal 'value validation gate' with explicit criteria for what constitutes confirmation that the outcome was achieved. Most teams have planning-side outcome statements but no production-side confirmation requirement before closing the feature. This is the gap the researcher's 'Feature' concept addresses directly."
- suggestion: Remove the closing sentence or rewrite to drop the meta-reference. The first two sentences of the paragraph stand on their own.

- id: COHERENCE-011
- severity: medium
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:Summary intro paragraph / research-cognitive-load-inversion.md:"Empirical Data on the Trust Gap"
- description: The two files give incompatible framings of AI-vs-Agile compatibility evidence at the headline level. Gemini opens by asserting "structural bifurcation" and "obsolescence of the operational rituals." The cognitive-load file (and the frameworks file's Forrester citation) report 95% of professionals affirm Agile's relevance, and that the issue is process design rather than fundamental incompatibility. Gemini's framing is inconsistent with the evidence the other files present, and the synthesis section of Gemini never reconciles this.
- evidence:
  - Gemini intro: "the industry is witnessing a structural bifurcation where the deterministic foundations of traditional Agile... are being re-evaluated against the non-deterministic velocity of Large Language Model (LLM) agents... When an AI agent can complete a story-sized unit of work in minutes rather than days, the two-week sprint and the daily standup transform from coordination tools into bureaucratic bottlenecks."
  - Frameworks file: "Empirical counter-data: Forrester's 2025 State of Agile Development found 95% of professionals affirm Agile's relevance, with nearly half already leveraging generative AI within agile practices."
  - Cognitive-load file: "The implication: cognitive load inversion is not primarily a tooling problem. It is a process design and organizational capability problem."
- suggestion: Either soften Gemini's headline framing to match the more nuanced evidence in the corpus, or have Gemini explicitly cite and rebut the Forrester counter-evidence. Currently the synthesis presents the most extreme position as consensus.

- id: COHERENCE-012
- severity: medium
- dimension: relevance
- location: gemini-deep-research-output.md:"Limitations and Risks: The 'Lethal Trifecta' and Skill Erosion"
- description: The "Lethal Trifecta" section addresses LLM security architecture (prompt injection / data exfiltration) — a topic that does not map to any of the eight stated sub-questions (granularity, AC replacement, spec-correct-value-zero, feature-as-user-value, behavioral validation, cognitive load, ceremonies, frameworks). It is a digression into LLM security that distracts from the methodology focus the rest of the corpus maintains. None of the eight subagent files raises the Lethal Trifecta because it is not relevant to the research question.
- evidence:
  - Gemini: "The fundamental security weakness of LLMs is the inability to rigorously separate instructions from data. This leads to the 'Lethal Trifecta': Sensitive Data, Untrusted Content, External Communication."
  - Scope.md sub-questions cover frameworks, granularity, AC, spec-correct-value-zero, feature-as-user-value, behavioral validation, cognitive load, ceremonies — none mention agent security architecture.
- suggestion: Cut the Lethal Trifecta section from the Gemini synthesis, or move it to a clearly-marked "Out of scope but worth noting" appendix. As placed, it is scope drift.

- id: COHERENCE-013
- severity: medium
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Follow-up Q3" (Behavioral Harness tools table) / research-behavioral-validation-ai-agents.md (entire document)
- description: Gemini's follow-up answer on practical behavioral harness implementation cites a tool ecosystem (OpenSpec, DeepEval, agentevals, Inspect AI, MLflow) that does not overlap with the behavioral validation file's tool ecosystem (Codecentric isolated specification testing, Playwright Test Agents, Bloom, QA.tech, Momentic, Checksum, Amazon Nova Act, Applitools, Percy, Blok, Krkn-AI). The two answers to "what tools implement a behavioral harness" share approximately zero tools. A reader looking for the recommended toolchain will find two non-intersecting universes.
- evidence:
  - Gemini Q3 table: "OpenSpec | DeepEval | agentevals | Inspect AI | MLflow"
  - Behavioral-validation file: "Codecentric using Claude Code... Playwright 1.56 (October 2025)... Anthropic's open-source tool Bloom... QA.tech... Momentic ($15M Series A, November 2025)... Checksum (YC-backed)... Amazon Nova Act... Applitools Eyes... Percy (BrowserStack)... Blok (launched July 2025, $7.5M seed)... Krkn-AI (Red Hat, 2025)..."
- suggestion: Reconcile the two tool inventories. Either Gemini should explicitly cite and integrate the subagent file's tools, or the corpus should explain why two different harness toolchains exist (e.g., one for backend-agent eval, one for browser-driven E2E). Without this, the synthesis appears to have skipped the dedicated subagent file.

- id: COHERENCE-014
- severity: medium
- dimension: consistency
- location: gemini-deep-research-output.md (table in "Restructuring Work Granularity" section)
- description: The "Traditional Agile vs. Agentic/AI-DLC" comparison table includes "Bottleneck | Developer Capacity | Intent Specification & Validation" — but elsewhere the same Gemini file argues the bottleneck is the "Lethal Trifecta" security boundary, the "cognitive load inversion" review burden, and the "Skill Development Gap." The single-cell answer in the table is reductive given the file's own multi-bottleneck claims later in the same document.
- evidence:
  - Gemini table: "| Bottleneck | Developer Capacity | Intent Specification & Validation |"
  - Gemini "Cognitive Load Inversion" section: "the reality that AI can generate specifications and code at a volume humans cannot review"
  - Gemini "Skill Development Gap": "while AI increases productivity, it can erode deep comprehension"
- suggestion: Either expand the table cell to reflect the multi-bottleneck claim, or footnote that "Intent Specification & Validation" is the primary new bottleneck while review capacity and skill erosion are secondary.

- id: COHERENCE-015
- severity: low
- dimension: temporal_coherence
- location: research-thought-leader-frameworks-agile-ai.md:"Martin Fowler and the ThoughtWorks Practitioner Lens"
- description: The frameworks file references "[OFFICIAL — martinfowler.com, March 2026]" for the Agentic Flywheel article and "[OFFICIAL — martinfowler.com]" (no date) for several others. The research date is 2026-04-13 in the frontmatter, so March 2026 is recent enough — but mixing dated and undated [OFFICIAL] tags throughout makes it hard to know which sources are 2025 vs. 2026. Several pre-2026 articles are tagged simply [OFFICIAL] without year, blurring temporal context.
- evidence:
  - "[OFFICIAL — martinfowler.com, March 2026]"
  - "[OFFICIAL — martinfowler.com]" (used for "Context Engineering and Spec Design" article dated only as "A February 2026 article" inline)
  - "Fowler's 2025 article 'LLMs bring new nature of abstraction' [OFFICIAL]"
- suggestion: Add year tags to all citation labels for consistency: [OFFICIAL — martinfowler.com, 2026], [OFFICIAL — martinfowler.com, 2025], etc. The asymmetry between dated and undated tags reduces reader trust in the citation discipline.

- id: COHERENCE-016
- severity: low
- dimension: conciseness
- location: research-spec-correct-value-zero.md:"Synthesis: A Framework for Closing the Gap" (Layer 1-5)
- description: The five-layer synthesis at the end largely restates content already presented in the six numbered Solution Patterns above. Layer 1 = Pattern 5 (Prototype-First). Layer 2 = Pattern 1 + Pattern 4 (SDD + PM Governance). Layer 3 = Pattern 2 (BDD). Layer 4 = Pattern 6 (Human Exploratory Testing). Layer 5 has no clear pattern equivalent. The synthesis adds only modest new framing for substantial duplication.
- evidence:
  - Document structure: "## Solution Pattern 1: Spec-Driven Development" through "## Solution Pattern 6: Human Exploratory Testing as a Value Gate" followed by "## Synthesis: A Framework for Closing the Gap" with "Layer 1 — Discovery before specification... Layer 2 — Specification quality... Layer 3 — Deterministic verification... Layer 4 — Human exploratory testing... Layer 5 — Continuous feedback loops."
- suggestion: Either compress the synthesis to two-three sentences pointing back to the patterns, or tighten the patterns themselves to make the synthesis a true distillation rather than a restatement.

- id: COHERENCE-017
- severity: low
- dimension: clarity
- location: research-cognitive-load-inversion.md:"Empirical Data on the Trust Gap" (paragraph 2)
- description: Two trust statistics are presented adjacently with overlapping but inconsistent framings: "29% of developers trust AI output in 2025" and "96% of developers report they do not fully trust AI-generated code." 29% trust ≠ 4% who fully trust (if 96% don't fully trust). The numbers are from different sources but presented as if they are compatible data points; the reader is left to do the math and notice the inconsistency.
- evidence:
  - "A 2025 Stack Overflow survey found only 29% of developers trust AI output in 2025, down 11 percentage points from 2024."
  - "Separately, 96% of developers report they do not fully trust AI-generated code — yet only 48% say they always check it before committing."
- suggestion: Add a sentence explaining why the two statistics differ — e.g., "trust" vs. "fully trust" measure different things, or different survey methodologies — so the reader doesn't have to reconcile them silently.

- id: COHERENCE-018
- severity: low
- dimension: clarity
- location: research-acceptance-criteria-ai-literal.md:"Property-Based Testing as Specification Verification"
- description: The arxiv citation `arxiv.org/html/2602.00180v1` appears in this section attributed to "the paper from arxiv.org on spec-driven development" — but the same paper ID is cited differently elsewhere in the same file ("arxiv paper on spec-driven development (February 2026)") and again in the spec-correct file ("[OFFICIAL, arxiv.org/html/2602.00180v1]"). The repeated reference without a stable short title makes it hard to tell whether one paper is being cited multiple ways or different papers are being conflated.
- evidence:
  - Acceptance file: "the paper from arxiv.org on spec-driven development confirms..." (no stable title)
  - Acceptance file later: "Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants — arxiv" (sources list)
  - Spec-correct file: "the arxiv study (February 2026) proposes a three-level spectrum"
- suggestion: Use a consistent short title for repeated arxiv citations (e.g., "Spec-Driven Development: From Code to Contract" → "the Code-to-Contract paper") so the reader can track which study is being invoked.

---

## Cross-Cutting Observations

1. **The Gemini file behaves like an unfaithful synthesis.** It introduces concepts not present in the eight subagent files (Lethal Trifecta, Mob rituals attached to AI-DLC, Silken Net, the OpenSpec/DeepEval/MLflow tool stack) and omits concepts central to the subagent files (EARS notation, Kiro's spec-driven IDE, Codecentric's isolated specification testing, the Playwright agent triad). The follow-up Q3 in particular reads as if Gemini answered a different question with a different research base than the corpus the subagents produced.

2. **"Harness" is the most overloaded term in the corpus.** Across nine files it refers to: (a) Fowler/Böckeler's cybernetic governor pattern, (b) OpenAI's PR-based Codex workflow, (c) Red Hat Developer's structured workflow article, (d) the generic "behavioral harness" surrounding evaluation. Without disambiguation the term drifts between files.

3. **The 3-3-3 model and AI-DLC are the most contradicted frameworks.** Both appear in multiple files with materially different operational descriptions. A reader will leave the corpus unsure what either framework actually prescribes.

4. **No internal-notes/scaffolding leaks beyond COHERENCE-010.** The "[OFFICIAL]" / "[PRAC]" / "[UNVERIFIED]" tagging convention is used consistently. The eight subagent files appear to have been cleaned up adequately; the principal coherence problems concentrate in the Gemini synthesis and at the seams between Gemini and the subagent files.
