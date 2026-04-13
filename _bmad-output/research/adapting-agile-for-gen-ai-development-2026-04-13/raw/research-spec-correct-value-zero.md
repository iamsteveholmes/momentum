---
content_origin: claude-code-subagent
date: 2026-04-13
sub_question: "How are practitioners solving the spec-correct, value-zero problem — where code passes all criteria but delivers no user value because the specification was incomplete?"
topic: "Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps"
---

# Spec-Correct, Value-Zero: How Practitioners Are Closing the Gap Between Passing Criteria and Delivering User Value

## The Problem Defined

The "spec-correct, value-zero" failure is not new, but AI-assisted development has compressed its feedback cycle from months to days and amplified its frequency dramatically. When a human developer received an incomplete spec, they exercised judgment — walking over to a product manager's desk, asking clarifying questions, applying contextual knowledge about what users actually need. AI coding agents do no such thing. They implement exactly what is written, faithfully and literally, and produce plausible-looking output that satisfies every stated criterion while missing the unstated intent entirely.

The CloudGeometry analysis of the evolving PM role frames this directly: "Your acceptance criteria are no longer a communication tool between you and a developer who will apply judgment. They are a functional specification that an AI system will execute literally." [PRAC] The article identifies the opening scenario as an AI pull request that "has technically met every acceptance criterion you wrote but built something you did not actually want." [PRAC]

This is the structural problem: human developers historically "read between the lines" and filled contextual gaps through experience and product sense. That safety net is gone. Specification quality now directly determines product quality.

A peer-reviewed paper on specification as quality gate makes the circularity explicit: when AI reviews AI-generated code without external specifications, "review checks code against itself, not against intent." Both the generating agent and the reviewing agent reason from the same artifact, sharing training distribution and therefore sharing blind spots. [OFFICIAL, arxiv.org/html/2603.25773]

## Why the Gap Exists at Scale

Three root causes drive the spec-correct, value-zero failure pattern in AI-native development:

**1. Literal Execution Without Contextual Judgment**

The arxiv paper on spec-driven development (February 2026) identifies the foundational issue: vague prompts force LLMs to make unstated assumptions. When a developer asks an AI to "Add photo sharing to my app," the system must guess at storage location, compression standards, permission models, and size limits. Each guess is a potential divergence from user intent. [OFFICIAL, arxiv.org/html/2602.00180v1]

**2. The Verification-Validation Collapse**

Practitioners are drawing a sharp distinction — borrowed from safety engineering — between verification (did it do what I said?) and validation (did it do what I wanted?). Traditional agile assumed developers would catch the gap between these two. The InfoQ report on the AI and Agile Manifesto debate quotes Sonya Siderova: "the bottleneck moved from 'how do humans collaborate to build' to 'how do humans decide what to build and validate it actually works.'" [PRAC, infoq.com/news/2026/02/ai-agile-manifesto-debate]

**3. Correlated AI Review Failures**

The arxiv quality gate study demonstrates empirically that AI-on-AI review creates correlated failures. In tests of domain-specific conventions, AI review accuracy ranged from 0–100% depending on whether domain knowledge appeared in training data. For log-linear interest rate interpolation — a genuine business rule — all AI reviewers scored 0/5. They didn't flag uncertainty; they confidently asserted incorrect rules. BDD specifications caught the same defects deterministically. [OFFICIAL]

## Solution Pattern 1: Spec-Driven Development (SDD)

The most prominent practitioner response to the spec-correct, value-zero problem is Spec-Driven Development, which inverts the traditional workflow by treating the specification as the source of truth rather than a prompt for code generation.

Thoughtworks designated SDD as "one of 2025's key new AI-assisted engineering practices." Their definition: "a development paradigm that uses well-crafted software requirement specifications as prompts, aided by AI coding agents, to generate executable code." [OFFICIAL, thoughtworks.com] The specification must explicitly define external behavior including "input/output mappings, preconditions/postconditions, invariants, constraints, interface types, integration contracts, and sequential logic/state machines." General intent is insufficient; machine-executable precision is required.

SoftwareSeni's 2025 practitioner guide identifies the specific structural shift: specifications act as both the prompt and the acceptance criteria. Teams that adopted this approach describe "building the muscle memory for spec-driven development" as the key workflow change. [PRAC, softwareseni.com] The GitHub Blog's open-source spec-kit toolkit is evidence that this pattern has crossed from experimentation to tooling investment. [OFFICIAL, github.blog]

The arxiv study (February 2026) proposes a three-level spectrum:

- **Spec-First**: Initial specs guide development; code becomes primary post-implementation
- **Spec-Anchored**: Specifications evolve alongside code with automated enforcement through tests
- **Spec-as-Source**: Humans edit specifications only; machines generate and regenerate code

[OFFICIAL, arxiv.org/html/2602.00180v1]

The economic argument for SDD has strengthened because AI has reduced specification authoring costs substantially. Writing a thorough spec used to take proportionally longer than writing the code itself. Now AI-assisted specification drafting makes spec-first development rational at scale, not merely disciplined. [OFFICIAL, arxiv.org/html/2603.25773]

**Limitation:** SDD does not solve the problem where the spec itself is wrong — it only prevents the AI from diverging from the spec. If the spec fails to capture user value, SDD faithfully implements that failure at high speed.

## Solution Pattern 2: BDD as a Behavioral Contract

Behavior-Driven Development has found renewed purpose as a guard against spec-to-value divergence in AI-native workflows. The core argument: BDD forces teams to articulate *why* something matters (business intent) before *how* to build it (implementation), creating a structured contract that AI agents can execute against.

The Medium post "Why BDD Is Essential in the Age of AI Agents" states the risk directly: "If you don't tell your agents exactly what you want, they'll build exactly what you didn't need." [PRAC, medium.com/@meirgotroot] BDD's Given/When/Then syntax serves as a "contract with the AI" — not because AI requires Gherkin syntax, but because the process of writing Gherkin forces teams to surface implicit assumptions before they become implementation bugs.

A key advantage: product managers can write and modify BDD scenarios without developer assistance, creating a direct channel between user intent and verifiable behavior. This closes the PM-developer-AI chain that previously allowed value gaps to accumulate. [PRAC, momentic.ai]

The empirical support for BDD as a spec correctness mechanism is strong. The arxiv quality gate study found that BDD specifications caught domain-specific defects that AI review missed entirely. The study proposes a sequencing architecture:

1. Executable BDD specifications first
2. Deterministic verification pipeline (not AI)
3. AI review only for unarticulated architectural residuals
4. Runtime verification for operational defects
5. User feedback loops for requirements validation

[OFFICIAL, arxiv.org/html/2603.25773]

This sequencing ensures that the AI operates in a space where its outputs can be verified against external truth, not just against its own training distribution.

## Solution Pattern 3: Redefining "Definition of Done" to Include Value Signals

Practitioners are extending the traditional Definition of Done beyond technical and functional criteria to include explicit value-facing checkpoints.

The shift from output-based to outcome-based acceptance is being discussed at multiple levels:

**At the team level:** Casey West's proposed "Agentic Manifesto" shifts from "verification" (did it do what I said?) to "validation" (did it do what I wanted?). This signals recognition that the Agile concept of "working software" needs a behavioral update for AI contexts. [PRAC, infoq.com/news/2026/02/ai-agile-manifesto-debate]

**At the process level:** The Stack Overflow trust gap analysis recommends treating AI-generated code like junior developer work — requiring "comprehensive testing, perhaps even more comprehensive than for human-written code" — and emphasizing that this review must include human scrutiny of the underlying approach, not just the output. [OFFICIAL, stackoverflow.blog/2026/02/18]

**At the product level:** The XP2025 workshop research proposes "context-specific success criteria" that balance productivity with technical debt trends, developer satisfaction, and design decision latency — recognizing that passing tests is not a sufficient signal of value delivered. [OFFICIAL, arxiv.org/html/2508.20563v1]

The Qodo State of AI Code Quality report (2025) identified a key finding: developers distinguish between code that "compiles" and code that fits the codebase. 65% report AI misses context during refactoring — producing spec-correct changes that break behavioral invariants elsewhere. Teams using persistent context retention (AI tools with codebase indexing) saw this drop to 16%. [PRAC, qodo.ai]

## Solution Pattern 4: PM Governance as a Structural Corrective

Perhaps the most direct organizational response to the spec-correct, value-zero problem is repositioning the product manager as a governance role rather than a documentation role.

The CloudGeometry analysis argues that AI has "formalized work engineers performed implicitly all along." The PM's new workflow centers on five practices: [PRAC, cloudgeometry.com]

1. Auditing acceptance criteria for literal interpretability
2. Writing requirements assuming zero product context from readers
3. Eliminating coordination overhead as build cycles compress
4. Reviewing generated output continuously rather than in sprint cycles
5. Mapping irreplaceable human decision checkpoints for scope, trade-offs, ethics, and strategy

The Allstacks analysis of AI and product decisions cites Frederick Brooks' foundational insight — that complete software specifications are "really impossible" — and notes that 48% of project failures trace to "changing or poorly documented requirements." [PRAC, allstacks.com] AI doesn't eliminate this gap; it makes the gap immediately visible.

Companies are structuring around this. Shopify's internal memo demanding teams "demonstrate why they cannot get done using AI" before requesting headcount signals a broader shift: product judgment — determining what should exist — is being elevated as the primary human responsibility in AI-native development. [PRAC, allstacks.com]

The "full-stack product manager" role is emerging: someone who can do user research, UX design, write a spec, and then leverage AI to generate code and tests. The pull request becomes the living product spec in this model, with PMs reviewing at compressed cadence against user intent rather than waiting for sprint demos. [PRAC, medium.com/@david.bennell]

## Solution Pattern 5: Prototype-First and Assumption Testing Before Spec-Writing

A counter-movement to spec-first development argues that the real problem is writing detailed specs before user assumptions have been validated. If the spec itself is wrong, SDD just implements the wrong thing efficiently.

The practitioner response: use AI's speed to build validatable prototypes *before* finalizing acceptance criteria. AI prototyping tools have reduced typical 12-week cycles to 2–4 weeks (M Accelerator research, 2025). [PRAC, sketchflow.ai] The recommended sequence:

1. Prototype to test assumptions (validate that users want what you're building)
2. Run structured user testing on the prototype
3. Write specifications from validated assumptions
4. Generate code from specifications

This inverts the traditional spec-first approach but avoids the failure mode where SDD faithfully implements a specification that was wrong from the start. The validation research at LogRocket draws the distinction explicitly: a validation prototype answers whether the idea is worth building; an MVP tests whether the built version retains users. [PRAC, blog.logrocket.com]

Teresa Torres' Continuous Discovery Habits framework remains the strongest practitioner foundation for this approach — weekly customer touchpoints, opportunity solution trees connecting user needs to solutions, and assumption testing before commitment. Her guidance has been updated for AI development contexts, emphasizing that AI can accelerate prototyping and discovery cycles without replacing the fundamental human work of identifying what problems to solve. [PRAC, producttalk.org]

## Solution Pattern 6: Human Exploratory Testing as a Value Gate

Automated tests verify that code does what the spec says. They cannot verify that the spec said the right thing. This is the structural argument for preserving human exploratory testing as a value gate in AI-native development.

The TestingMind 2026 analysis argues for a balanced approach: AI for breadth coverage and repetitive regression validation; humans for domain-critical scenarios, usability evaluation, and creative edge-case exploration. [PRAC, testingmind.com] The TotalShiftLeft assessment identifies "business logic gaps" as the category that automated tests most reliably miss — because the tests were written from the same spec as the code.

Practically, this means dedicating exploratory testing sessions specifically to the question "does this deliver what the user actually needs?" rather than "does this match the acceptance criteria?" User Acceptance Testing (UAT) is being reframed as a value verification gate, not a final regression pass.

The Tricentis QA Trends for 2026 report identifies exploratory testing and edge case testing as "critical disciplines" specifically in the context of AI-generated code, noting that AI failures manifest differently from human coding failures — subtle logic errors and hallucinated API calls rather than obvious bugs — requiring different testing heuristics. [PRAC, tricentis.com]

## What Practitioners Report Is Not Working

Several failure modes are well-documented in the 2025–2026 practitioner literature:

**Circular AI review:** Using AI to review AI-generated code without external specifications produces correlated failures, not independent validation. The arxiv study demonstrates this experimentally across multiple model families. [OFFICIAL]

**Accepting "plausible-looking" code:** Stack Overflow's trust gap analysis names the "Uncanny Valley of Code" — code that is syntactically perfect and architecturally plausible but contains subtle functional defects requiring deep expertise to uncover. [PRAC]

**Treating spec completion as done:** The BCG Widening AI Value Gap report (September 2025) notes that despite tens of billions invested in generative AI, organizations still struggle to connect AI output to measurable business outcomes. [OFFICIAL, bcg.com]

> **[UNVERIFIED]** A figure cited as "MIT Project NANDA — 95% of corporate AI projects show no measurable return" appears in secondary sources but could not be traced to a verifiable primary MIT publication. The BCG "Widening AI Value Gap" report (cited above) provides well-sourced evidence for the same point and is preferred.

**Writing specs for developers:** Existing acceptance criteria were written as communication tools between humans who shared context. PM guidance has solidified around the insight that AI accepts no implicit context — every assumption must be explicit, every edge case must be named, and every "it should feel right" must be translated into verifiable behavior. [PRAC, cloudgeometry.com]

## The "Working Software" Question

Several practitioners and researchers have directly challenged whether the Agile Manifesto's definition of "working software" remains adequate in AI-native development contexts.

Steve Jones (Capgemini) argues that AI is "highly effective at building software that appears to work, or at least works for the very specific instructions it was given." He contends that technically running code generated by AI doesn't meet the traditional quality standard of working software when architectural implications are unaddressed. [PRAC, blog.metamirror.io]

Kent Beck's response — advocating "augmented coding" that maintains "clean code, comprehensive testing, and careful design" while using AI for implementation — suggests the original working software standard needs reinforcement rather than redefinition. [PRAC, infoq.com]

The InfoQ debate synthesis finds emerging consensus on a practical update: "working software" in AI-native development must be understood as software that has passed both verification (does it implement the spec?) and validation (does the spec represent what users need?). The former is automatable; the latter requires human judgment at the point of requirement authorship and output review. [PRAC]

## Synthesis: A Framework for Closing the Gap

The practitioner evidence from 2025–2026 converges on a layered defense:

**Layer 1 — Discovery before specification:** Validate user assumptions through prototypes and continuous discovery before writing detailed specs. Teresa Torres' framework, now being applied to AI contexts, ensures specs are built from validated user needs rather than designer assumptions. [PRAC]

**Layer 2 — Specification quality as a first-class practice:** Write specs assuming zero implicit context. Use BDD Given/When/Then format to force behavioral precision. Audit criteria for literal interpretability. PM as governor, not just documenter. [PRAC]

**Layer 3 — Deterministic verification against external truth:** Use executable BDD specs as the verification pipeline, not AI-on-AI review. Specifications convert vague requirements into governing constraints that make defects analyzable. [OFFICIAL]

**Layer 4 — Human exploratory testing for value validation:** Preserve UAT as a "does this actually deliver user value?" gate, not a regression pass. Focus human testing time on business logic gaps that automated tests cannot catch. [PRAC]

**Layer 5 — Continuous feedback loops:** Short release cycles with real user exposure surface spec gaps that escaped all prior layers. The feedback loop must be shorter than the spec-writing cycle, or failures compound. [PRAC]

No single layer is sufficient. The spec-correct, value-zero problem exists precisely because it survives individual controls — a spec can pass BDD review while still missing user intent, and a prototype can validate the wrong solution. Defense in depth, with humans at the value-facing gates, is the practitioner consensus.

> **Known Limitation — Structural Circularity:** This five-layer defense contains a structural circularity: Layer 4 (human exploratory testing for value validation) is load-bearing, yet the cognitive-load research in this corpus documents that humans cannot reliably serve as value-validation gates at AI velocity — senior engineers spend 4.3× longer reviewing AI code; PRs sit idle 5.3× longer; 96% don't fully trust AI code yet only 48% actually check it. The synthesis prescribes "humans at value-facing gates" as the solution to a problem that the same corpus shows those humans are already unable to handle. Proposed mitigations in the practitioner literature include moving human review earlier in the cycle (spec authorship at Layer 1–2 rather than output review at Layer 4), using synthetic-user simulation services for high-value paths, and third-party validation for production gates. This circularity is acknowledged as an open research problem — no published practice fully breaks it as of April 2026.

---

## Sources

- [Thoughtworks — Spec-Driven Development: Unpacking 2025's Key New AI-Assisted Engineering Practice](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [arxiv — Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants (February 2026)](https://arxiv.org/html/2602.00180v1)
- [arxiv — The Specification as Quality Gate: Three Hypotheses on AI-Assisted Code Review (March 2026)](https://arxiv.org/html/2603.25773)
- [arxiv — AI and Agile Software Development: A Research Roadmap from the XP2025 Workshop](https://arxiv.org/html/2508.20563v1)
- [InfoQ — Does AI Make the Agile Manifesto Obsolete? (February 2026)](https://www.infoq.com/news/2026/02/ai-agile-manifesto-debate/)
- [Stack Overflow Blog — Closing the Developer AI Trust Gap (February 2026)](https://stackoverflow.blog/2026/02/18/closing-the-developer-ai-trust-gap/)
- [CloudGeometry — What Happens to the Product Manager When AI Builds the Code](https://www.cloudgeometry.com/blog/what-happens-to-the-product-manager-when-ai-builds-the-code)
- [Allstacks — How AI Makes Every Software Engineer a Product Manager (2026)](https://www.allstacks.com/blog/ai-software-engineer-product-decisions-2026)
- [Qodo — State of AI Code Quality (2025)](https://www.qodo.ai/reports/state-of-ai-code-quality/)
- [BCG — The Widening AI Value Gap (September 2025)](https://media-publications.bcg.com/The-Widening-AI-Value-Gap-Sept-2025.pdf)
- [Medium — Why BDD Is Essential in the Age of AI Agents](https://medium.com/@meirgotroot/why-bdd-is-essential-in-the-age-of-ai-agents-65027f47f7f6)
- [SoftwareSeni — Spec-Driven Development in 2025: The Complete Guide](https://www.softwareseni.com/spec-driven-development-in-2025-the-complete-guide-to-using-ai-to-write-production-code/)
- [GitHub Blog — Spec-Driven Development with AI: Get Started with a New Open Source Toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [TestingMind — Manual vs Automation Testing in 2026: Why the Debate Is Wrong](https://www.testingmind.com/manual-vs-automation-testing-in-2026-guide/)
- [Tricentis — QA Trends for 2026: AI, Agents, and the Future of Testing](https://www.tricentis.com/blog/qa-trends-ai-agentic-testing)
- [Medium — AI Killed the Agile Manifesto. We Need a New Philosophy in Software](https://blog.metamirror.io/ai-killed-the-agile-manifesto-805ad9a639db)
- [Medium — Product Management in 2025: AI Tools Blurring the Line Between Roles](https://medium.com/@david.bennell/product-management-in-2025-dc3f1e1b4319)
- [Sketchflow — How to Validate a Startup Idea with AI Prototyping (2026)](https://www.sketchflow.ai/blog/guides/how-to-validate-a-startup-idea-with-ai-prototyping/)
- [Product Talk — Getting Started with Continuous Discovery (Teresa Torres)](https://www.producttalk.org/getting-started-with-discovery/)
- [LogRocket — Validation Research Techniques to Test Value and Viability Assumptions](https://blog.logrocket.com/ux-design/validation-research-techniques/)
- [Momentic — How AI Breathes New Life Into BDD](https://momentic.ai/blog/behavior-driven-development)
- [Digital.ai — 18th State of Agile Report (October 2025)](https://digital.ai/press-releases/digital-ais-18th-state-of-agile-report-marks-the-start-of-the-fourth-wave-of-software-delivery/)
