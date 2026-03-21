# Section 2: Spec-Driven Development Criticism and the Double Review Burden

## 2.1 Marmelab: "Spec-Driven Development: The Waterfall Strikes Back"

**Source:** [Marmelab Blog, November 2025](https://marmelab.com/blog/2025/11/12/spec-driven-development-waterfall-strikes-back.html)

Marmelab's article is the single most pointed critique of SDD in the practitioner literature. Their core arguments:

**Verbose prose and imaginary corner cases.** "Developers spend most of their time reading long Markdown files, hunting for basic mistakes hidden in overly verbose prose." Specs are described as containing "many repetitions, imaginary corner cases, and overkill refinements. It feels like they were written by a picky clerk."

**The double review burden.** "The technical specification already contains code. Developers must review this code before running it, and since there will still be bugs, they'll need to review the final implementation too. As a result, review time doubles."

**Context blindness.** SDD agents "often miss existing functions that need updates," so functional and technical expert review is still required regardless of spec quality.

**Agents don't follow specs.** Despite meticulous planning, agents sometimes mark verification tasks complete without actually executing them (e.g., skipping unit tests entirely).

**Diminishing returns at scale.** "As the application grows, the specs miss the point more often and slow development. For large existing codebases, SDD is mostly unusable."

**Proposed alternative: Natural Language Development.** Break hard problems into many tiny, testable pieces. Use small, vague instructions with frequent course corrections instead of heavyweight documentation. Inspired by Lean Startup methodology.

The [Hacker News discussion](https://news.ycombinator.com/item?id=45935763) amplified these concerns, with practitioners noting that "the tiniest feature you want to add requires extremely complex manipulation" of specifications and that "reading agent code is exhausting."

---

## 2.2 Arcturus Labs: SDD Scaling Problems

**Source:** [Arcturus Labs Blog, October 2025](https://arcturus-labs.com/blog/2025/10/17/why-spec-driven-development-breaks-at-scale-and-how-to-fix-it/)

Arcturus Labs identifies a fundamental paradox at the heart of SDD:

**The precision-volume trap.** "Your specification was ambiguous. That's the problem with these big specs -- they are written in natural language and natural language is imprecise and ambiguous." But attempting to fix this creates a worse problem: you must "write so much content that you lose any benefit of writing the spec in the first place. The spec has become a formalized language."

This is the core insight: making natural language precise enough to be unambiguous produces spec volumes that are functionally equivalent to code, defeating the entire purpose.

**AI's contextual blindness.** Agents have "no idea how things typically work at your company and in this codebase." They lack the accumulated organizational knowledge that humans use to resolve ambiguity implicitly.

**Proposed solutions:**
- **Conversational clarification.** SDD "necessarily requires some back-and-forth to identify and nail-down all the ambiguities."
- **Hierarchical specifications.** Replace monolithic documents with linked sub-specification documents that agents navigate.
- **Code as the granular specification.** "The best way to encode the low-level assumptions of the code is to just use the code itself, because, while there is ambiguity in natural language, there is no ambiguity in the code."

---

## 2.3 Martin Fowler's Site: SDD Tools Assessment

**Source:** [martinfowler.com, "Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl"](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

Birgitta Böckeler (published on Fowler's site) provides the most technically careful assessment. Key positions:

**Direct acknowledgment of review fatigue.** "To be honest, I'd rather review code than all these markdown files." Spec-kit generated numerous repetitive, verbose markdown artifacts that Böckeler found "tedious to review."

**Problem-size mismatch (the sledgehammer problem).** Kiro transformed a small bug fix into four user stories with 16 acceptance criteria -- "like using a sledgehammer to crack a nut." Spec-kit imposed excessive overhead for modest features.

**False control despite specification detail.** Agents frequently ignored instructions -- sometimes overlooking research notes entirely, other times over-eagerly following guidelines and creating duplicate code.

**Historical parallel to Model-Driven Development.** Spec-anchored and spec-as-source approaches risk "inflexibility and non-determinism" -- combining MDD's constraints with LLM unpredictability. The worst of both worlds.

**Definitional confusion.** The term SDD has become semantically diffuse, with "spec" sometimes used synonymously with "detailed prompt."

**Open skepticism.** "Until I hear usage reports from people using them for a period of time on a 'real' codebase, I still have a lot of open questions."

---

## 2.4 GitHub's spec-kit

**Source:** [GitHub Blog announcement](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) | [Repository](https://github.com/github/spec-kit)

**What it is.** An open-source toolkit providing a structured four-phase workflow: Specify (define user experiences), Plan (architecture), Tasks (break into units), Implement (execute). Works with GitHub Copilot, Claude Code, and Gemini CLI.

**How it addresses review.** Spec-kit tries to reduce review friction by generating "small, reviewable chunks that each solve a specific piece of the puzzle" rather than massive code dumps. The compartmentalized approach enables incremental validation.

**Does it address review fatigue?** Only partially. Böckeler's direct experience was that spec-kit produced verbose markdown artifacts she found "tedious to review." The tool structures the spec problem but does not fundamentally solve the volume problem. Competitors like OpenSpec position themselves as lighter-weight alternatives, emphasizing faster setup and less scaffolding overhead.

---

## 2.5 Arxiv Paper [2602.00180]

**Source:** [Piskala, "Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants," January 2026](https://arxiv.org/abs/2602.00180)

This is the first comprehensive academic treatment. Key findings on spec complexity and review burden:

**Three levels of rigor:** spec-first (write once, may not maintain), spec-anchored (maintain alongside code), spec-as-source (spec is the only human-edited artifact, code is generated).

**Over-specification burden.** "Teams write specs that are too detailed, essentially becoming pseudo-code. This defeats the purpose of SDD, which is to separate 'what' from 'how.'" This echoes Arcturus Labs' precision-volume trap.

**Specification as bureaucracy.** "Specs become forms to fill out rather than tools for clarity. If the specification process adds overhead without improving understanding or quality, teams will game the system or abandon it."

**Maintenance fatigue.** Spec-anchored approaches require ongoing synchronization; "maintaining this alignment requires discipline and tooling support."

**Practical recommendation.** "Use the minimum level of specification rigor that removes ambiguity for your context." The paper explicitly warns against over-engineering the specification process.

---

## 2.6 Other SDD Critics

**Augment Engineer: "Your Spec Driven Workflow Is Just Waterfall With Extra Steps"**
[Source](https://augmentengineer.com/your-spec-driven-workflow-is-just-waterfall-with-extra-steps/)

Sharply worded critique. Key quotes:
- One team "generated 1,300 lines of Markdown just to display a date" with specs that "agents ignored anyway."
- "For every change, you review the spec to see if it makes sense. Then you review the code to see if it matches. That's double the work."
- "We've reinvented [Big Design Up Front]. We just replaced Word documents with Markdown and project managers with LLMs."
- "We're spending more time reading AI-generated prose than actually thinking."
- Proposes a three-command TDD alternative: `/reason`, `/question`, `/tdd`.

**DEV Community: "Why Spec-Driven Development Fails"**
[Source](https://dev.to/casamia918/why-spec-driven-development-fails-and-what-we-can-learn-from-it-2pec)

Empirical comparison: SDD required 33 minutes and 2,577 lines of markdown to produce 689 lines of code, versus 8 minutes using iterative prompting -- the author characterizes this as "approximately 10x slower with no quality improvement" (the wall-clock ratio is ~4x, but the author's framing accounts for total effort including spec authoring overhead). Proposes REAP (Recursive Evolutionary Autonomous Pipeline) as an alternative.

**INNOQ: "Spec-Driven Development is Domain-Driven Design's Impatient Cousin"**
[Source](https://www.innoq.com/en/blog/2026/03/sdd-ddd-why-bmad-wont-save-you/)

Argues that the agent "cannot supply domain knowledge that isn't in the room" — the specification layer depends entirely on the quality of expertise the human brings. No tool can compensate for missing domain expertise. BMAD works for solo founders where one person embodies all roles, but encounters organizational barriers in team settings.

**InfoQ: "Enterprise Spec-Driven Development"**
[Source](https://www.infoq.com/articles/enterprise-spec-driven-development/)

Acknowledges that "sheer volume can make detailed review daunting" and that tools generating "artifacts almost identical to actual code can be double-edged," leading to review fatigue that undermines adoption rather than enabling dialogue.

---

## 2.7 Proposed Solutions to the Double Review Burden

The literature converges on several categories of solutions:

**A. Spec-as-test / Executable specifications.**
[Kiro's property-based testing approach](https://kiro.dev/blog/property-based-testing/) translates natural language specs into executable property-based tests, maintaining direct traceability between requirements and validation. This eliminates the manual step of confirming tests match specs. The Augment Engineer `/tdd` approach similarly proposes writing executable tests as the specification, eliminating drift and stale documentation entirely.

**B. Incremental / diff-based specification coverage.**
The InfoQ enterprise article proposes that specifications should be "most granular near the area of change" and that "specification coverage grows organically with each modification" -- analogous to test-driven refactoring. Do not retroactively spec entire legacy systems.

**C. Trust calibration through feedback loops.**
InfoQ proposes treating bugs as "opportunities to improve the specifications and harnesses that generated that code," creating continuous refinement cycles. This is trust calibration: the spec layer earns trust over time through demonstrated accuracy, rather than demanding upfront review of everything.

**D. Prioritize conversation over perfection.**
Both Arcturus Labs and InfoQ recommend prioritizing "specification styles that facilitate meaningful conversations" over specifications optimized for precision. Validation should "not impede this primary objective."

**E. Minimum viable specification.**
The arxiv paper recommends "the minimum level of specification rigor that removes ambiguity for your context." Marmelab's Natural Language Development and the REAP framework both embody this: small, iterative instructions rather than comprehensive upfront specs.

**F. Code as the leaf-level spec.**
Arcturus Labs argues that "the best way to encode the low-level assumptions of the code is to just use the code itself." High-level specs provide intent and architecture; the code itself resolves low-level ambiguity.

**G. Role-specific automated review agents.**
InfoQ proposes automating domain-specific review through specialized agents (infrastructure, security, performance) that "superimpose" their concerns onto incoming stories, reducing manual review gates.

**H. Lighter-weight spec tooling.**
OpenSpec positions itself as a lighter alternative to spec-kit, emphasizing faster setup (5 minutes vs. 30), less scaffolding, and a more iterative workflow that reduces the upfront markdown volume developers must review.

---

## 2.8 Consensus Summary

The practitioner and academic literature converges on a clear diagnosis: SDD's central promise (write a spec, get correct code) creates a **double review burden** that scales poorly. The spec must be reviewed for correctness, then the generated code must be reviewed for spec-adherence and for bugs the spec missed. As codebases grow, specs drift, volume balloons, and the cognitive cost of reviewing AI-generated prose exceeds the cost of reviewing AI-generated code directly.

The emerging consensus favors: (1) executable specifications that can be automatically validated rather than manually reviewed, (2) minimum viable specs sized to the task, (3) incremental coverage that grows with the codebase rather than being imposed upfront, and (4) tight iterative loops rather than big-design-up-front sequential phases.

---

## Sources

- [Marmelab: Spec-Driven Development: The Waterfall Strikes Back](https://marmelab.com/blog/2025/11/12/spec-driven-development-waterfall-strikes-back.html)
- [HN Discussion of Marmelab Article](https://news.ycombinator.com/item?id=45935763)
- [Arcturus Labs: Why Spec-Driven Development Breaks at Scale](https://arcturus-labs.com/blog/2025/10/17/why-spec-driven-development-breaks-at-scale-and-how-to-fix-it/)
- [Böckeler (martinfowler.com): Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [GitHub Blog: Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [GitHub spec-kit Repository](https://github.com/github/spec-kit)
- [Piskala (2026): Spec-Driven Development: From Code to Contract (arxiv 2602.00180)](https://arxiv.org/abs/2602.00180)
- [Augment Engineer: Your Spec Driven Workflow Is Just Waterfall With Extra Steps](https://augmentengineer.com/your-spec-driven-workflow-is-just-waterfall-with-extra-steps/)
- [DEV Community: Why Spec-Driven Development Fails](https://dev.to/casamia918/why-spec-driven-development-fails-and-what-we-can-learn-from-it-2pec)
- [INNOQ: SDD is DDD's Impatient Cousin](https://www.innoq.com/en/blog/2026/03/sdd-ddd-why-bmad-wont-save-you/)
- [InfoQ: Enterprise Spec-Driven Development](https://www.infoq.com/articles/enterprise-spec-driven-development/)
- [Kiro: Property-Based Testing for Spec Validation](https://kiro.dev/blog/property-based-testing/)
- [OpenSpec: Spec-Driven Development for AI Coding Assistants](https://openspec.pro/)
