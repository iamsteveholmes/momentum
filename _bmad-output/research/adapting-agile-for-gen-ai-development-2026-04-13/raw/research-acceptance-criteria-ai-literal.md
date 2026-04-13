---
content_origin: claude-code-subagent
date: 2026-04-13
sub_question: "What replaces or augments acceptance criteria when AI agents implement specifications literally — without the developer judgment that historically filled the unstated requirements gap?"
topic: "Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps"
---

# Acceptance Criteria in the Age of AI Literal Implementation

## The Core Problem: AI Does Not Fill Gaps, It Guesses

The foundational issue is well-documented by 2025: AI coding agents implement specifications literally rather than inferring unstated requirements the way experienced developers do. As one analysis summarizes, "there is a gap in the level of abstraction between English and code, leading to incomplete or ambiguous specifications. This issue becomes more pronounced in longer programs, where the number of ambiguous decision points increases, and choices traditionally made by humans are instead implicitly embedded in the LLM's generated code." [OFFICIAL — arxiv.org/html/2503.22625v1]

A concrete example from a paper studying real-world AI coding tasks illustrates this sharply: developers working on a file format library implicitly understood that "implementing file format support" requires both a reader and a writer (the serializer-deserializer pattern). This was never stated explicitly. AI agents evaluated on the same task implemented only the read method — they followed the literal scope of the issue rather than inferring the architectural convention. [OFFICIAL — arxiv.org/html/2503.22625v1]

The large-scale production evidence is damning. A 2026 study found that AI-introduced issues surviving in production repositories had risen to over 110,000 by February 2026, characterized as "long-term maintenance technical debt" — the accumulated cost of guesses embedded into code. [PRAC — cited in github.blog and augmentcode.com analysis]

Addy Osmani's widely-cited formulation captures the practical shape of the problem: "LLMs are astonishingly good at pattern completion but terrible at guessing unstated requirements; asking an AI to 'add photo sharing' leads it to invent file limits, permissions models, storage backends, and security assumptions — all plausible, many wrong." [PRAC — addyosmani.com/blog/ai-coding-workflow/]

This is not just a prompting problem. It is a structural problem: acceptance criteria, as traditionally written for human developers, are incomplete by design. They rely on the developer's judgment, experience, and ability to ask clarifying questions to fill in the remainder. When the implementor is an AI agent, that judgment disappears.

## Categories of Implicit Requirements That Disappear

Research on human-AI coding collaboration identifies several systematic categories of knowledge that live outside specifications and that human developers handle silently: [OFFICIAL — arxiv.org/html/2503.22625v1]

**Style and convention constraints.** Codebases carry inherited patterns — naming conventions, error-handling idioms, class organization — that developers absorb from the existing codebase without being told. AI agents lack this contextual absorption unless it is explicitly surfaced.

**Design trade-offs.** Whether to prefer readability over performance, scalability over simplicity, or security over convenience is context-dependent and rarely captured in acceptance criteria. Humans navigate these based on project maturity and organizational norms.

**Domain-specific patterns.** An academic website "should" include publications and contact info — not because this is stated, but because it is convention. Any domain-specific implicit knowledge must be externalized for AI.

**Semantic range of inputs.** AI treats `null`, `undefined`, `empty`, and `missing` as distinct cases; humans think conceptually of "no data provided." If contracts do not define what absence means, the AI will make an arbitrary choice — often a fragile one. [PRAC — dev.to/asmaa-almadhoun]

## Spec-Driven Development: The Emerging Response

By 2025, the dominant practitioner response to the specification completeness problem is **spec-driven development (SDD)** — treating the specification not as passive documentation but as the primary executable artifact that governs what AI agents do. [OFFICIAL — thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices]

SDD shifts the intellectual work upstream: "The intellectual work happens at the spec level — clarifying requirements, resolving ambiguities, defining edge cases, setting acceptance criteria. The coding work becomes a translation problem, and translation is exactly what AI excels at." [PRAC — resultsense.com/insights/2025-09-12-spec-driven-ai-development]

The key structural insight is the separation of **what** from **how**. Specifications describe behavior without prescribing implementation. The AI handles the how; humans own the what and the constraints. [PRAC — cgi.com/en/blog/artificial-intelligence/spec-driven-development]

Thoughtworks characterizes SDD as "one of 2025's key new AI-assisted engineering practices," representing a meaningful departure from the earlier norm of natural-language prompting. [OFFICIAL — thoughtworks.com]

### What a Machine-Complete Specification Requires

Multiple practitioner frameworks converge on a similar anatomy for specs that are complete enough for AI implementation. A synthesis:

- **Explicit input/output contracts**: Required vs optional fields, type constraints, what absence means
- **Preconditions and postconditions**: What must be true before the agent acts; what must be true after
- **Invariants and constraints**: Properties that must hold across all states (not just happy path)
- **Negative bounds / anti-goals**: Explicit "shall not" constraints — what the system must never do
- **Concrete examples**: At least 2-3 representative scenarios including edge cases
- **Architecture and dependency decisions**: Which libraries, patterns, and integration points to use
- **Security and compliance constraints**: These are never inferred; must be explicit

[PRAC — oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/; addyosmani.com/blog/good-spec/; medium.com/@nprasads]

A practical negative-constraint pattern gaining traction is the **three-tier boundary system**: "Always do" (safe, autonomous actions), "Ask first" (high-impact changes needing human approval), and "Never do" (hard stops). This structure gives agents far clearer guardrails than flat rule lists or traditional acceptance criteria alone. [PRAC — oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/]

For safety and adversarial use cases, research confirms: "Using negative constraints are critical ('You cannot modify data', 'you cannot access external URLs', 'you cannot execute code'). A well-designed system prompt doesn't just say what the agent should do — it should explicitly say what it cannot do." [PRAC — dev.to/willvelida/preventing-agent-goal-hijack-in-ai-agents]

## EARS Notation: Structured Acceptance Criteria for Machine Parsing

The most concrete tooling response to specification completeness is the adoption of **EARS notation** (Easy Approach to Requirements Syntax) as the format for acceptance criteria in AI-assisted development.

Amazon's Kiro IDE, which launched public preview in July 2025, made EARS central to its spec-driven workflow. EARS structures requirements as formal conditional statements: "When [condition], the system shall [behavior]." This converts natural language acceptance criteria into machine-parseable contracts from which property-based tests can be automatically derived. [OFFICIAL — kiro.dev/docs/specs/]

Kiro's workflow enforces three phases before any implementation: Requirements (user stories with EARS-notation acceptance criteria), Design (architecture, schemas, sequence diagrams), and Tasks (discrete implementation steps). Nothing is handed to the AI coding agent until all three phases are complete and reviewed. [OFFICIAL — kiro.dev/blog/introducing-kiro/]

The EARS format also enables **property-based testing generation**: from a requirement like "For any authenticated user and any active listing, the user can view that listing," the system can automatically generate hundreds of test cases covering the input space — far more than any human would write manually. [OFFICIAL — kiro.dev/docs/specs/correctness/]

## Property-Based Testing as Specification Verification

**Property-based testing (PBT)** has emerged as the most technically robust response to the literal implementation problem. The core insight: if requirements express universal invariants ("at most one direction displays green"), those invariants can be tested across thousands of generated inputs, not just the few examples a human would write.

Kiro's architecture makes this explicit: specifications in EARS format are automatically converted into PBT cases. When an implementation fails, PBT's "shrinking" capability finds the minimal counterexample — giving the AI agent (and the developer) precise failure context rather than a complex failing integration test. [OFFICIAL — kiro.dev/blog/property-based-testing/]

The critical advantage: PBT tests properties derived directly from specifications, maintaining "a clear, traceable link between requirements and the tests that validate them." This solves the traditional acceptance criteria problem of tests drifting from intent over time. [OFFICIAL — kiro.dev/blog/property-based-testing/]

A 2025 paper on agentic property-based testing demonstrates this at scale: an agent built on Claude Code autonomously tested open-source Python libraries using Hypothesis, finding a genuine bug in NumPy (numpy.random.wald sometimes returning negative numbers, violating the mathematical property of the Wald distribution) — a type of defect specification-based testing alone would not catch. [OFFICIAL — arxiv.org/html/2510.09907v1]

The paper from arxiv.org on spec-driven development confirms: "Property-based testing automatically verifies that invariants from specs are satisfied regardless of implementation variation, enabling confidence when AI generates multiple possible implementations from identical specifications." And empirically: "human-refined specs significantly improve LLM-generated code quality, with controlled studies showing error reductions of up to 50%." [OFFICIAL — arxiv.org/html/2602.00180v1]

## BDD and Gherkin: Partial Help, Real Risks

> **Note:** ATDD (Acceptance Test-Driven Development), BDD (Behavior-Driven Development), and Gherkin are related but distinct: ATDD is a test-first discipline; BDD is a collaboration practice for defining behavior in shared language; Gherkin is the DSL (Domain Specific Language) used to write BDD scenarios. In AI-native contexts, they often appear together but each plays a different role.

Behavior-Driven Development and Gherkin scenarios occupy contested ground in the AI literal implementation context. The structural strength of Given/When/Then is real — it forces requirements into a testable, example-grounded format that AI agents can act on more reliably than narrative prose. But the approach carries specific failure modes.

A 2025 practitioner study found that "AI understands concrete examples in Gherkin better than abstract generalisations" but that "AI-generated scenarios might be adequate as tests but fail to express desired behavior well for human readers." [PRAC — testquality.com/gherkin-bdd-cucumber-guide-to-behavior-driven-development/]

More critically, glue code quality degraded as example count grew: one team reported "duplicate state storage between steps" and architectural problems appearing in AI-generated step definitions, confirming that "AI cannot reliably write well-designed code that follows best practices" for the structural layer underneath Gherkin. [PRAC — urgo.medium.com/using-specification-by-example-to-drive-ai-95c19f0bb4ec]

The literal implementation trap surfaces here in a specific form: an AI agent accepted a test failure in one practitioner's experiment because the system returned a 401 status when the author expected 200 — the agent assessed the test as "correctly failing" rather than questioning whether the failure reason was conceptually correct. This is the specification completeness problem in miniature: the acceptance criterion was technically present but semantically incomplete. [PRAC — urgo.medium.com]

Paul Duvall's ATDD-for-AI framework addresses this by making acceptance tests the **primary specification mechanism** rather than a downstream verification artifact. The principle: "no implementation file is created without a corresponding BDD feature file." This turns the CI/CD pipeline into an enforcement mechanism for specification completeness — if no feature file exists, no code can be committed. [PRAC — paulmduvall.com/atdd-driven-ai-development-how-prompting-and-tests-steer-the-code/]

Gherkin's role is thus augmented rather than primary: it remains valuable for expressing behavioral intent, but must be coupled with executable step definitions and property-based invariants to close the literal implementation gap.

## Conformance Suites: Language-Independent Specification Contracts

An underused but powerful approach is the **conformance test suite** — a set of language-independent, YAML or JSON-based tests that specify expected inputs and outputs for any compliant implementation. Simon Willison advocates this pattern: "If you're building an API, the conformance suite specifies expected inputs/outputs, and the agent's code must satisfy all cases. This is more rigorous than ad-hoc unit tests because it's derived directly from the spec and can be reused across implementations." [PRAC — cited in augmentcode.com/guides/how-ai-enhances-spec-driven-development-workflows]

This approach treats the spec itself as testable: any implementation that passes the conformance suite is compliant; any that does not is wrong regardless of how the code looks. AI agents can generate implementations in any language or style, and the conformance suite will surface literal implementation errors before they reach production.

GitHub's open-source Spec Kit formalizes a related pattern: specifications become "the shared source of truth," with iterative validation at each phase of a four-stage workflow (Specify → Plan → Tasks → Implement). The key architectural insight is that incomplete specs are a design feature — ongoing refinement is expected rather than treated as failure. [OFFICIAL — github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/]

## Agent Stories: Restructured User Stories for Machine Execution

At the user story level, teams working with AI agents are adopting structurally different story formats. Research on production agentic teams identifies a bifurcation: [PRAC — slavakurilyak.com/posts/agent-stories]

**Machine-actionable stories** (for agents to execute autonomously) include: explicit ID, title, intent, acceptance criteria as binary-testable conditions, concrete examples with edge cases, explicit constraints, and metadata about dependencies and scope boundaries.

**Human-readable stories** (for developers building agent-facing surfaces) follow closer to traditional narrative but must define success criteria "that humans can evaluate without deep technical expertise."

The critical insight from practitioner experience: "When examples are added to acceptance criteria, most AI hallucinations disappear." This is specification by example as a guardrail — concrete cases constrain the space of valid implementations more effectively than abstract behavioral statements. [PRAC — prodmoh.com/blog/ai-user-stories; handsonai.info/product-engineering/user-stories/]

Traditional acceptance criteria formulations ("the user can filter results") must be replaced with quantified, concrete versions: "the user can filter results by date range, and the default range is the last 30 days." The specificity prevents the AI from inventing a plausible-but-wrong implementation. [PRAC — spin.atomicobject.com/user-story-as-prompt/]

## The Instruction Overload Trap

One counterintuitive finding with significant practical implications: adding more specification does not monotonically improve AI output. Research shows that model performance degrades significantly when given too many simultaneous requirements — the "curse of instructions." Monolithic specs can actually harm AI agent performance. [PRAC — oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/]

The solution is **modular, scoped delivery of specification**. Rather than providing an entire requirements document simultaneously, effective frameworks deliver specifications in small, focused chunks aligned with discrete implementation tasks. Kiro's task decomposition phase enforces this: each task receives only the specification relevant to that task, not the full spec. [OFFICIAL — kiro.dev/docs/specs/]

Martin Fowler observed this problem concretely in his evaluation of spec-driven tools: a small bug fix generated "4 user stories with 16 acceptance criteria" — excessive for the scope. The tooling's rigid workflow did not adapt to task size, and the specification overhead exceeded its value. He draws a parallel to Model-Driven Development's failure: the risk of combining "inflexibility and non-determinism" when specs become too prescriptive. [PRAC — martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html]

## What Human Judgment Was Actually Providing

The research clarifies what human developer judgment actually contributed when reading traditional acceptance criteria:

1. **Convention lookup**: Consulting implicit knowledge of patterns used elsewhere in the codebase
2. **Scope inference**: Expanding partial requirements to their implied full scope (reader → reader + writer)
3. **Tradeoff navigation**: Making context-appropriate decisions about competing constraints
4. **Ambiguity resolution**: Either asking questions or making documented judgment calls
5. **Semantic normalization**: Treating `null`, `undefined`, and `empty` as a unified concept when context warranted

Each of these must now be externalized if AI is to fill the implementation role. The implication is that human effort moves earlier in the workflow — into specification — and the specification artifact becomes substantially richer than traditional acceptance criteria.

Thoughtworks frames this as "intent competency" — the organizational capability to formalize requirements with the precision AI demands. The article notes: "Specifications are only as strong as the understanding behind them. Organizations risk embedding vulnerabilities if they rush to formal specifications without investing in design thinking and architecture first." [PRAC — cgi.com/en/blog/artificial-intelligence/spec-driven-development]

## Synthesis: What Actually Replaces Traditional Acceptance Criteria

Based on 2025 practitioner and research evidence, traditional acceptance criteria are being replaced or augmented by a layered system:

| Layer | What It Provides | Format |
|---|---|---|
| EARS-notation requirements | Machine-parseable behavioral contracts | When/shall structured statements |
| Concrete examples with edge cases | Constrain the implementation space | Given/When/Then + tabular examples |
| Explicit negative constraints | Define what AI must not do | "Shall not" statements, three-tier permission model |
| Property-based test invariants | Universal properties that hold across all inputs | Auto-generated from EARS requirements |
| Conformance suites | Language-independent contract tests | YAML/JSON input-output assertions |
| Architecture decisions record | Resolve implicit tradeoffs explicitly | Structured decision records in spec |
| Anti-goal statements | Bound optimization targets | "This system is not intended to..." clauses |

Traditional acceptance criteria do not disappear — they evolve into this richer structure. The acceptance criterion "user can filter results" becomes an EARS statement, a table of concrete filter combinations, a property asserting that all valid filter combinations return results, and a negative constraint that filtering never reveals unauthorized data.

The net effect: specification effort increases substantially per story, but implementation ambiguity decreases substantially — and so does the rework cost of AI literal implementation errors.

---

## Sources

- [My LLM coding workflow going into 2026 — Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/)
- [How to write a good spec for AI agents — O'Reilly Radar](https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/)
- [How to write a good spec for AI agents — Addy Osmani](https://addyosmani.com/blog/good-spec/)
- [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants — arxiv](https://arxiv.org/html/2602.00180v1)
- [Spec-driven development: Unpacking one of 2025's key new AI-assisted engineering practices — Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Spec-driven development: From vibe coding to intent engineering — CGI](https://www.cgi.com/en/blog/artificial-intelligence/spec-driven-development)
- [Spec-driven development with AI: Get started with a new open source toolkit — GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl — Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Kiro IDE — Specs documentation](https://kiro.dev/docs/specs/)
- [Kiro IDE — Property-based testing](https://kiro.dev/blog/property-based-testing/)
- [Kiro IDE — Correctness with property-based tests](https://kiro.dev/docs/specs/correctness/)
- [Introducing Kiro — Kiro blog](https://kiro.dev/blog/introducing-kiro/)
- [Spec-Driven Development in the Age of AI: From "Specs as Documents" to "Specs as Executable Truth" — Medium](https://medium.com/@nprasads/spec-driven-development-in-the-age-of-ai-from-specs-as-documents-to-specs-as-executable-truth-9b9e066712b1)
- [Agentic Property-Based Testing: Finding Bugs Across the Python Ecosystem — arxiv](https://arxiv.org/html/2510.09907v1)
- [Using Specification by Example to Drive AI — Ürgo Ringo, Medium](https://urgo.medium.com/using-specification-by-example-to-drive-ai-95c19f0bb4ec)
- [ATDD-Driven AI Development: How Prompting and Tests Steer the Code — Paul Duvall](https://www.paulmduvall.com/atdd-driven-ai-development-how-prompting-and-tests-steer-the-code/)
- [Challenges and Paths Towards AI for Software Engineering — arxiv](https://arxiv.org/html/2503.22625v1)
- [AI Writes What You Ask. Architecture Survives What You Didn't Expect — DEV Community](https://dev.to/asmaa-almadhoun/ai-writes-what-you-ask-architecture-survives-what-you-didnt-expect-c9b)
- [User Stories & Acceptance Criteria — Hands-on AI Cookbook](https://handsonai.info/product-engineering/user-stories/)
- [Your Best Prompt Is a Well-Defined User Story — Atomic Object](https://spin.atomicobject.com/user-story-as-prompt/)
- [Agent Stories: Frameworks for AI Agents and Agentic Developers — Alpha Insights](https://slavakurilyak.com/posts/agent-stories)
- [A Benchmark for Evaluating Outcome-Driven Constraint Violations in Autonomous AI Agents — arxiv](https://arxiv.org/html/2512.20798v1)
- [Preventing Agent Goal Hijack in AI Agents — DEV Community](https://dev.to/willvelida/preventing-agent-goal-hijack-in-ai-agents-4eia)
- [Gherkin & Cucumber BDD: A TestQuality Guide for 2025](https://testquality.com/gherkin-bdd-cucumber-guide-to-behavior-driven-development/)
- [Agentic AI for Behavior-Driven Development Testing Using Large Language Models — SciTePress](https://www.scitepress.org/Papers/2025/133744/133744.pdf)
- [How AI Enhances Spec-Driven Development Workflows — Augment Code](https://www.augmentcode.com/guides/ai-spec-driven-development-workflows)
- [User Stories for AI Agents — Templates & Best Practices](https://prodmoh.com/blog/ai-user-stories)
