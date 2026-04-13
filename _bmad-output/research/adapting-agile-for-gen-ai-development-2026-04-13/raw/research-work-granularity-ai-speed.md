---
content_origin: claude-code-subagent
date: 2026-04-13
sub_question: "How have forward-thinking teams restructured work granularity when AI agents can complete traditional story-sized units of work 10-50x faster than a human developer?"
topic: "Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps"
---

# Work Granularity in AI-Native Development: How Teams Are Restructuring When AI Moves at Machine Speed

## The Core Problem: Story Sizing Built for Human Hands

Traditional Agile user stories were sized for a single developer working one to three days. The logic was sound in 2001: a story small enough to fit in a sprint implied a scope bounded enough to estimate, implement, and demonstrate within the two-week cycle. That assumption has collapsed.

By 2025, AI coding agents routinely complete what would have been a two-day story in under an hour. METR's July 2025 study of experienced open-source developers found that — counterintuitively — those developers took 19% *longer* to complete tasks when using AI assistance, not faster; the study's authors attribute this to friction in the human-AI collaboration loop rather than raw capability gaps. [OFFICIAL — METR research] Separately, machine learning benchmarks showed that the length of tasks AI can reliably complete has been doubling approximately every four months since 2024 — with supervised autonomous task horizons reaching roughly two hours as of late 2025 and projected to reach four days of unsupervised work by 2027. [OFFICIAL: METR research blog, 2025-07-10; MachineLearningMastery.com agentic trends 2026]

PwC's 2026 Agentic SDLC report adds a concrete enterprise data point: Pioneer teams — those using GenAI across six or more SDLC stages — now average approximately 74 releases per year, while less-augmented teams trail far behind. [OFFICIAL: PwC "Agentic SDLC in practice: the rise of autonomous software delivery," 2026]

When the bottleneck is no longer implementation time, the entire architecture of sprint-based planning breaks down. This document surveys how forward-thinking teams are responding.

---

## The Upstream Bottleneck Shift

The single most consistent insight across practitioners and researchers is that AI acceleration does not make planning obsolete — it relocates the constraint.

Sonya Siderova, writing on the InfoQ Agile Manifesto debate, frames it precisely: "Agile isn't dead. It's optimizing a constraint that moved." [PRAC: InfoQ, "Does AI Make the Agile Manifesto Obsolete?", February 2026]

The constraint has shifted from engineering capacity (how fast can we write the code?) to decision quality and intent clarity (how precisely can we define what to build?). This is not a subtle distinction. It means:

- Sprint planning ceremonies that previously spent 80% of time decomposing technical tasks now need to spend that time on outcome definition, boundary conditions, and acceptance criteria
- The bottleneck in delivering value is now upstream: product thinking, stakeholder alignment, governance, and validation — not implementation
- Estimation of implementation effort becomes nearly irrelevant, replaced by estimation of ambiguity and specification completeness

Giles Lindsay, writing in February 2026, articulates this well: "Engineering accelerates first. Governance, product thinking, and strategy lag behind." He argues that AI doesn't kill sprints — it exposes that many teams were using sprints as delivery throttles rather than learning cadences, and that learning cadences remain essential even when delivery is instant. [PRAC: Giles Lindsay, "AI Didn't Kill the Sprint — It Exposed What Sprints Were Really For," Medium, February 2026]

---

## What Replaces the User Story

Several distinct patterns are emerging to replace or restructure the traditional user story at the work-unit level.

### Pattern 1: Spec-Driven Development (SDD) — The Specification as the Unit

The most widely discussed replacement for user stories in AI-native contexts is the formal specification. Thoughtworks named spec-driven development as one of 2025's key new AI-assisted engineering practices. [OFFICIAL: Thoughtworks, "Spec-Driven Development: Unpacking 2025's Key New AI-Assisted Engineering Practices"]

In SDD, the unit of work shifts from a user story ("As a user, I want X so that Y") to a structured specification document that defines:

- Input/output mappings
- Preconditions and postconditions
- Invariants and constraints
- Interface types and integration contracts
- Sequential logic and state machines
- Given/When/Then acceptance scenarios

The specification itself becomes the artifact that the AI agent executes against. The GitHub blog announced an open-source SDD toolkit in 2025, and tools like Kiro (Amazon), spec-kit, and Tessl (as analyzed by Martin Fowler's team in March 2026) implement this pattern. [OFFICIAL: GitHub Blog, "Spec-Driven Development With AI: Get Started With a New Open Source Toolkit," 2025; OFFICIAL: Martin Fowler site, "Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl," 2026]

Martin Fowler's team raised a critical limitation: for small tasks, SDD creates excessive overhead. Kiro applied to a single bug fix generated four user stories with sixteen acceptance criteria — "using a sledgehammer to crack a nut." This suggests SDD is best applied at feature granularity, not bug/task granularity.

McKinsey QuantumBlack's published AI-native development model formalizes this further, using structured REQ/TASK artifacts with explicit state machines (draft → in-review → approved → complete) and hierarchical traceability. Their model enables teams to "run multiple complete cycles per day" and for a product manager to "kick off three competing feature experiments on Monday morning and review working implementations by afternoon." [PRAC: McKinsey QuantumBlack, "Agentic Workflows for Software Development," Medium, February 2026]

### Pattern 2: Agent Stories — Executable Work Units for AI Actors

Slava Kurilyak's "Agent Stories" framework (2025) proposes a direct adaptation of user stories for AI agent execution. [PRAC: Slava Kurilyak, "Agent Stories: Frameworks for AI Agents and Agentic Developers," Alpha Insights, 2025]

The template replaces the human actor with an AI agent and adds machine-verifiable output requirements:

```
As an [AI Agent + capability], 
I need [precise context package: files, APIs, standards, constraints], 
to deliver [business-value outcome visible to humans], 
so that [verification + integration path is clear].
```

Every Agent Story requires:
- A verification command (script/test that confirms completion)
- An integration specification (where the output plugs into the system)
- Explicit constraints (performance, security, compatibility bounds)
- A deterministic Definition of Done

The framework distinguishes two complementary types:
- **Agent Stories** (horizon: minutes to hours) — work AI agents execute autonomously
- **Agentic Developer Stories** (horizon: days to sprints) — human work to build the platforms, APIs, and guardrails agents rely on

This dual-horizon planning model is significant: it explicitly acknowledges that human planning operates at sprint scale while agent execution operates at sub-hour scale. The two tracks are parallel, not sequential.

The framework is grounded in a hard mathematical reality: with a 5% per-action error rate, a 10-step agent task has only a 59.9% success rate. Small, verifiable units are not a stylistic preference — they are a reliability requirement.

### Pattern 3: Intent Design — From Stories to Outcome Specifications

AWS proposed "Intent Design" as an alternative to sprint planning, framing architecture as scaffolding that defines roles, guardrails, and fallback mechanisms rather than prescribing implementation. [PRAC: InfoQ, AI Agile Manifesto debate coverage, February 2026]

The intent-driven.dev community has formalized this into Context Engineering and Spec-Driven Development, arguing the industry is moving from "code is the source of truth" to "intent is the source of truth." [PRAC: intent-driven.dev, 2025]

The intent framework emphasizes:
- Desired outcomes as observable states (not activities, but conditions that exist after work completes)
- Success evaluation criteria embedded in the work definition
- AI-DLC (AI-Driven Development Life Cycle) that adapts breadth and depth of development stages to the complexity of the stated intent

This is structurally closer to a problem statement with acceptance criteria than to a traditional user story.

---

## Sprint Cadence: Compression, Elimination, or Transformation?

Three distinct positions have emerged on what happens to sprint cadence when AI handles implementation in hours.

### Position 1: Sprints Compress but Survive

The Futurice AI-native operating model argues that the Build-Measure-Learn-Act cycle, once tied to a two-week rhythm, "is becoming near-instant as AI takes over continuous process optimization." [PRAC: Futurice, "AI-Native Operating Model: Evolving Beyond Agile with Culture, POM, and VSM," 2025]

In this view, sprints don't die — they compress. Daily release cadences replace biweekly ones, with human ceremonies becoming less about coordination and more about strategic alignment. Teams that previously shipped weekly are shipping multiple times per day.

The double/slash blog (Alexander König, 2025) argues this more forcefully: small batch workflows, CI/CD pipelines, and flow-based development are more important than timeboxes when AI can deliver features in hours. Flow metrics and cycle time replace sprint velocity as the primary measurement lens. [PRAC: double/slash blog, "AI delivers in hours. Why do we still plan in sprints?", 2025]

### Position 2: Continuous Flow Replaces Sprints

Several practitioners argue that Kanban-style continuous flow is more appropriate than sprint cadence for AI-native teams. The CIO article on agentic engineering (2025) notes that continuous flow is better suited for exploratory AI work where timelines are fluid. [OFFICIAL: CIO, "5 Ways Agentic Engineering Transforms Agile Practices," 2025]

Futurice's Product Operating Model (POM) and Value Stream Management (VSM) combination enables AI agents to handle "real-time backlog prioritization, dependency checks, and data visibility" in a pull-based model where work flows continuously rather than accumulating in sprint batches.

The invidelabs blog proposed the V-Bounce SDLC model — six phases (Input, AI Generation, Human Review, Refinement, Approval, Knowledge Capture) cycling multiple times daily rather than every two weeks. [PRAC: invidelabs, "The Death of the Two-Week Sprint," 2025]

### Position 3: Sprints Serve a Different Purpose — Keep Them

The Scrum.org perspective, echoed by Kent Beck and others, argues that sprints should not be abandoned because they serve learning functions that AI acceleration makes more important, not less. [OFFICIAL: Scrum.org, "AI Is Rewiring Scrum Teams, But Not Scrum," 2025]

Giles Lindsay's February 2026 analysis argues: "Speed without learning is not agility. It is activity." If AI makes implementation fast, the value of a sprint rhythm lies in enforcing the inspect-and-adapt cadence, reviewing assumptions, and validating that fast-built features actually deliver the intended outcomes.

Forrester's 2025 State of Agile Development report found 95% of professionals still affirm Agile's critical relevance — though critics note this may reflect institutional inertia as much as genuine utility. [PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage]

---

## Shape Up as an AI-Native Alternative

Basecamp's Shape Up methodology (Ryan Singer, 2019) is experiencing a significant renaissance in 2025-2026 as a framework for AI-native teams. [PRAC: Serge Bulaev, "Shape Up: The Product Development Method Having a Renaissance in the AI Era," 2025; LinkedIn article, 2025]

Shape Up's key differentiator is the separation of shaping (defining what to build and why) from building (implementing it). The "appetite" concept — a fixed time budget that constrains scope rather than estimating implementation — becomes even more powerful when the building phase can be handed to AI agents.

Ryan Singer articulated this directly: "Shaping is going upstream in the process. Instead of just working on how to effectively refine tickets, we're thinking about how to effectively frame the problem and outline the solution."

The Shape Up properties that make it AI-compatible:
- **Fixed time, variable scope** (appetite not estimate): when AI handles implementation, the variable is definition quality, not coding speed — Shape Up targets exactly that variable
- **Shaping phase produces fat markers, not tickets**: the shaped pitch describes the problem and outlines a solution without prescribing every implementation step — this is a better input for AI agents than a task list
- **Six-week cycles with two-week cooldown**: the rhythm is coarser than Scrum, but the cool down period maps well to validation and retrospection after AI-implemented features land
- **No backlog grooming ceremonies**: Shape Up explicitly rejects infinite backlog maintenance — it uses a betting table instead, which scales better when AI can execute faster than backlogs can be groomed

The synthesis emerging in 2025-2026 practice: Shape Up's shaping discipline + AI agent execution during the build phase + continuous deployment replaces the traditional sprint-based backlog-to-release pipeline.

---

## What Replaces Velocity

Velocity — story points completed per sprint — was never a great metric, but it served as a proxy for team throughput and sprint planning capacity. When AI can generate orders of magnitude more code per unit time, velocity becomes incoherent.

Practitioners are converging on several replacement metrics:

**Cycle time over story points**: How long does it take from intent-clear to production-deployed? This measures the whole pipeline, not just coding speed. [PRAC: LinearB, "AI-Driven Software Development: Navigating the Shift from Speed to Velocity," 2025]

**Specification quality metrics**: Given that AI execution quality depends on specification clarity, teams are tracking metrics like acceptance criteria completeness, spec revision cycles, and specification-to-implementation fidelity.

**Outcome metrics (DORA + product outcomes)**: The 2025 DORA Report reorganized core metrics into throughput (deployment frequency, lead time, rework rate) and stability (change failure rate, failed deployment recovery time). With AI amplifying both good and bad team habits, DORA metrics become more important as leading indicators. [OFFICIAL: DORA/Google, "2025 State of AI-Assisted Software Development Report"]

**Hypothesis validation rate**: Teams moving toward hypothesis-driven development measure what fraction of deployed experiments confirmed their hypotheses, focusing on learning velocity over delivery velocity. [PRAC: Statsig perspectives, Scrum.org HDD resources]

LinearB's research identifies a critical frame shift: the question moves from "How can we use AI to go faster?" to "Where do we want to go?" — making directional clarity (velocity in the physics sense, not the Agile sense) the primary planning concern. [PRAC: LinearB blog, 2025]

---

## Concrete Team Restructuring Patterns

Beyond theory, several concrete organizational patterns are emerging:

**The Orchestrator Model**: Engineers transition from code authors to AI orchestrators, spending time on system architecture definition, guardrail specification, and output validation. The CIO article on agentic workflows describes the 2026 engineer as spending "less time writing foundational code and more time orchestrating a dynamic portfolio of AI agents, reusable components and external services." [OFFICIAL: CIO, "How Agentic AI Will Reshape Engineering Workflows in 2026," 2026]

**Dual-Track Planning**: Some teams run two explicit planning tracks — a fast track (Agent Stories, hours to a day) and a slow track (platform and infrastructure stories, sprints). The McKinsey QuantumBlack model separates "multi-phase single-branch workflows cycling hourly" from human review cycles that happen at PR merge time.

**Platform Teams as Agent Keepers**: LinearB research identified that large companies' platform teams grew from 5 to 25 engineers in a single year as AI adoption scaled — their new role is managing, steering, and verifying AI agent workflows across development. This "agent keeper" function is a new organizational unit with no Agile analog.

**Expanded Story Scope for Remaining Human Stories**: The CIO agentic engineering article notes that when AI agents handle implementation, "stories can be larger in scope" — correlating with greater amounts of change without overwhelming team capacity. The appropriate human-facing story becomes a feature-level definition rather than a task-level implementation guide.

**The Betting Table at Feature Cadence**: Teams applying Shape Up report mapping the betting table to quarterly cycles with AI-compressed builds inside each six-week cycle, effectively multiplying throughput without changing the planning rhythm. [PRAC: multiple Shape Up practitioner reports, 2025]

---

## The Unresolved Tensions

This research identified several tensions that have not been satisfactorily resolved in current practice:

**Over-specification risk**: Spec-driven development can become a new form of waterfall if the specification process itself becomes heavyweight and disconnected from rapid feedback. Thoughtworks and Martin Fowler's team both flag this as an unsolved problem. [OFFICIAL: Thoughtworks SDD article, 2025; OFFICIAL: Martin Fowler site SDD tools analysis, 2026]

**The validation bottleneck**: If AI builds fast and humans validate slowly, the validation step becomes the new constraint. Teams risk accumulating a "validation backlog" analogous to the technical debt backlogs of the Agile era.

**Estimation remains necessary for stakeholder communication**: Even if teams don't need velocity for internal planning, business stakeholders still want predictability. Replacing story points with cycle time metrics requires organizational change beyond the engineering team.

**Context rot in long agent workflows**: Kent Beck's augmented coding work and the McKinsey QuantumBlack model both emphasize that architectural memory — preserving context across agent work sessions — is a first-class engineering concern, not just a nice-to-have. Without it, fast agent work creates a coherence debt that accumulates as fast as technical debt used to.

---

## Vocabulary Reconciliation: Seven Names for the Same Slot

The literature uses at least seven terms for the "work unit one level below Feature/Epic": **Bolts**, **Units of Work**, **Agent Stories**, **Agentic Developer Stories**, **Impact Loops**, **Context Capsules**, and **Super-Specs**. These are not synonyms, but they occupy related positions:

| Term | Framework | Scope | Primary purpose |
|---|---|---|---|
| Bolts | AI-DLC (practitioner label; see caveat in gemini report) | Hours to days | High-velocity execution cycle |
| Units of Work | AWS AI-DLC (primary docs) | Hours to days | Self-contained agent orchestration block |
| Agent Stories | Kurilyak / practitioner synthesis | Minutes to hours | Context-packaged implementation unit |
| Agentic Developer Stories | Academic/practitioner | Minutes to hours | Story format adapted for agent execution |
| Impact Loops | Brgr.one / KPI-based dev | Sprint-equivalent | Metric-movement measurement unit |
| Context Capsules | Crywolfe "Agentic Manifesto" | Session-scoped | Shared context artifact passed between agents |
| Super-Specs | AI/works™ / Thoughtworks SDD | Feature-level | Multi-dimensional spec anchoring AI generation |

**Taxonomy shortcut:** "Bolts / Units of Work / Agent Stories / Agentic Developer Stories" describe the same conceptual slot (implementation unit) from different frameworks. "Impact Loops" is a *measurement* unit, not an execution unit. "Context Capsules" are *knowledge transfer artifacts*, not work units. "Super-Specs" are *planning artifacts* that precede execution units.

---

## Synthesis: A Pragmatic Model for 2026

Based on the sources reviewed, the most coherent emerging model for forward-thinking teams combines elements of multiple approaches:

1. **Shape Up's shaping discipline** for the planning layer — appetite-bounded problem framing before any AI agent work begins *(structurally compatible; no empirical cases validated for AI-native teams as of April 2026)*
2. **Spec-driven development** as the handoff artifact from shaping to execution — formal specifications as inputs to AI agents
3. **Agent Stories format** for the execution layer — small, verifiable, context-packaged work units sized for AI execution horizons (minutes to hours)
4. **Continuous flow / CI/CD** replacing sprint-bounded releases — deploy when complete, not when the sprint ends
5. **Outcome metrics (DORA + hypothesis validation)** replacing velocity — measure what the fast-built things actually accomplish
6. **Human review at PR/merge granularity** rather than sprint ceremony granularity — humans review completed features, not daily progress

The two-week sprint is not dead but is evolving toward a governance cadence (review assumptions, reassess priorities) rather than a delivery cadence. The story is not dead but is bifurcating into shaped pitches (planning artifacts defining the problem) and Agent Stories (execution artifacts defining the work).

---

## Sources

- [5 Ways Agentic Engineering Transforms Agile Practices — CIO](https://www.cio.com/article/4086747/5-ways-agentic-engineering-transforms-agile-practices.html) [OFFICIAL]
- [How Agentic AI Will Reshape Engineering Workflows in 2026 — CIO](https://www.cio.com/article/4134741/how-agentic-ai-will-reshape-engineering-workflows-in-2026.html) [OFFICIAL]
- [Does AI Make the Agile Manifesto Obsolete? — InfoQ, February 2026](https://www.infoq.com/news/2026/02/ai-agile-manifesto-debate/) [PRAC]
- [AI Didn't Kill the Sprint — It Exposed What Sprints Were Really For — Giles Lindsay, Medium, February 2026](https://agiledelta.medium.com/ai-didnt-kill-the-sprint-it-exposed-what-sprints-were-really-for-7bdd3d1b5c4f) [PRAC]
- [The Death of the Two-Week Sprint — invidelabs blog, 2025](https://blog.invidelabs.com/the-death-of-the-two-week-sprint/) [PRAC]
- [AI Delivers in Hours. Why Do We Still Plan in Sprints? — double/slash blog](https://blog.doubleslash.de/en/software-technologien/devops/sprints-in-the-ai-age-ai-coding-agents/) [PRAC]
- [Augmented Coding: Beyond the Vibes — Kent Beck, Tidy First Substack, 2025](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes) [PRAC]
- [Spec-Driven Development Unpacking 2025's Key New AI-Assisted Engineering Practices — Thoughtworks](https://www.thoughtworks.com/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) [OFFICIAL]
- [Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl — Martin Fowler site, 2026](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) [OFFICIAL]
- [Spec-Driven Development with AI: Open Source Toolkit — GitHub Blog, 2025](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) [OFFICIAL]
- [Agent Stories: Frameworks for AI Agents and Agentic Developers — Slava Kurilyak, Alpha Insights, 2025](https://slavakurilyak.com/posts/agent-stories) [PRAC]
- [Shape Up: The Product Development Method Having a Renaissance in the AI Era — Serge Bulaev, 2025](https://www.bulaev.net/p/shape-up-the-product-development) [PRAC]
- [Shape Up: Why 37signals' Method Is Trending Again in 2025 — Serge Bulaev, LinkedIn](https://www.linkedin.com/pulse/shape-up-why-37signals-method-trending-again-2025-serge-bulaev-nxc4f) [PRAC]
- [AI-Native Operating Model: Evolving Beyond Agile with Culture, POM, and VSM — Futurice, 2025](https://www.futurice.com/blog/ai-native-operating-model) [PRAC]
- [Agentic Workflows for Software Development — McKinsey QuantumBlack, Medium, February 2026](https://medium.com/quantumblack/agentic-workflows-for-software-development-dc8e64f4a79d) [OFFICIAL]
- [AI-Driven Software Development: Navigating the Shift from Speed to Velocity — LinearB, 2025](https://linearb.io/blog/ai-driven-software-development-shift-speed-to-velocity) [PRAC]
- [2025 DORA State of AI-Assisted Software Development — Google/DORA](https://dora.dev/dora-report-2025/) [OFFICIAL]
- [DORA Report 2025 Summary — Scrum.org](https://www.scrum.org/resources/blog/dora-report-2025-summary-state-ai-assisted-software-development) [OFFICIAL]
- [Agentic SDLC in Practice: The Rise of Autonomous Software Delivery — PwC, 2026](https://www.pwc.com/m1/en/publications/rise-of-autonomous-software-delivery.html) [OFFICIAL]
- [The Agentic Organization: Contours of the Next Paradigm for the AI Era — McKinsey](https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-agentic-organization-contours-of-the-next-paradigm-for-the-ai-era) [OFFICIAL]
- [Intent Engineering Framework for AI Agents — ProductCompass](https://www.productcompass.pm/p/intent-engineering-framework-for-ai-agents) [PRAC]
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity — METR, July 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) [OFFICIAL]
- [7 Agentic AI Trends to Watch in 2026 — MachineLearningMastery.com](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/) [PRAC]
- [AI Is Rewiring Scrum Teams, But Not Scrum — David Sabine, Scrum.org](https://www.scrum.org/resources/blog/ai-rewiring-scrum-teams-not-scrum) [OFFICIAL]
