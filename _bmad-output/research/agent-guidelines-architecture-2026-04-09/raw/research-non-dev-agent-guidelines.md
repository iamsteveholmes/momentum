---
content_origin: claude-code-subagent
date: 2026-04-09
sub_question: "How do non-dev agents (QA, E2E, PM, SM) best consume their role-specific guidelines — and how does the optimal delivery mechanism differ by role complexity?"
topic: "Agent-specific guidelines architecture in Claude Code"
---

# Non-Dev Agent Guidelines: Optimal Delivery Mechanisms by Role

## Overview

In multi-role agentic engineering workflows, every agent carries distinct domain knowledge requirements. A QA agent checking for antipatterns has fundamentally different information needs from a PM agent generating acceptance criteria or an SM agent triaging sprint impediments. The question of *how* to deliver those guidelines — as always-loaded system prompt content, file-based rules, progressively-disclosed skills, or JIT prompts — is not uniform. This research examines how each non-dev role category best consumes its guidelines and why.

## The Core Delivery Primitives

Before examining roles, it helps to establish what delivery primitives exist in Claude Code as of April 2026 [OFFICIAL]:

**Subagent system prompt (always-loaded):** Defined in the Markdown body of a `.claude/agents/` file. Injected at subagent creation and active for the entire subagent session. Subagents receive only this prompt plus basic environment details — they do not inherit the parent conversation's system prompt. [source: code.claude.com/docs/en/sub-agents]

**Skills (on-demand):** Filesystem-based packages with a `SKILL.md` file. At startup, only the skill's metadata (~100 tokens of name + description) is pre-loaded. The full instruction body loads when Claude determines the skill is relevant. Supporting files load only when Claude reads them. [source: claude.com/blog/skills-explained]

**Rules files with `paths:` frontmatter (session-triggered):** `.claude/rules/` files with YAML frontmatter can include a `paths:` key with glob patterns. These were designed to load only when files matching those patterns are in context. However, as of February 2026, a confirmed open bug (GitHub issue #16299) causes these rules to load globally at session start regardless of path match. They function as early-loaded but technically unreliable filters. [source: github.com/anthropics/claude-code/issues/16299]

**Preloaded skills in subagents:** Subagents can declare a `skills:` array in frontmatter. Named skills are injected in full at subagent startup — not lazy-loaded. This is the inverse of the standard skill pattern and is used when a subagent always needs a skill's full content available. [source: code.claude.com/docs/en/sub-agents]

**Context cascade (CLAUDE.md hierarchy):** General guidelines flow from `~/.claude/CLAUDE.md` → project `CLAUDE.md` → subdirectory `CLAUDE.md`. This is always-loaded and session-wide. [source: code.claude.com/docs/en/best-practices]

## QA / Code-Review Agents

### Role Complexity

QA and code-review agents occupy the highest technical complexity among non-dev roles. Their function is adversarial checking — finding antipatterns, security issues, and violations of conventions that a dev agent may have missed. The information they need is:

1. **Antipattern checklists** — specific, enumerable violations to look for
2. **Coding conventions** — project-specific style and structure rules
3. **Test quality criteria** — what constitutes a good vs. bad test

### Always-Loaded vs. JIT for Antipattern Checklists

For QA agents, antipattern checklists are most effective when **preloaded into the subagent's system prompt** rather than supplied as JIT prompts. The reasoning is structural: QA review is a uniform task (review this code for issues), and the checklist defines the review criteria that shape the entire agent session. Omitting it from the system prompt would require the orchestrator to inject it on each delegation call, creating reliability risk.

The AGENTS.md research published in January 2025 [PRAC] demonstrated that well-structured always-available context files (containing coding conventions, architecture descriptions, and project structure) reduced output tokens by approximately 16–20% and wall-clock execution time by 20–28% compared to agents without such files [source: arxiv.org/html/2601.20404]. Critically, this study specifically highlighted that developer-written context files provided positive benefit while LLM-generated ones showed marginally negative effects — suggesting that QA guidelines must be thoughtfully curated, not auto-generated.

### File-Scoped Rules for QA

The `paths:` frontmatter mechanism was designed precisely for QA use cases — applying `**/*Test.kt` scoped rules only when Kotlin test files are in context. However, the current session-wide loading bug means QA teams cannot fully rely on this mechanism as a precision filter. A practical workaround until the bug is fixed [UNVERIFIED]: scope QA rule files to a dedicated QA subagent's system prompt rather than relying on session-level `paths:` triggers. This gives deterministic behavior regardless of the path-loading bug.

### Structural Guidelines for QA Agents

The 2025 Tricentis Agentic QA research [PRAC] confirmed that QA agents perform best with structured, checklist-based system prompts that define:
- What to check (specific antipatterns, categories)
- What evidence constitutes a finding
- How to format and prioritize output

[source: tricentis.com/learn/agentic-quality-assurance]

Meta's 2025 "semi-formal reasoning" research [UNVERIFIED, based on VentureBeat coverage] found structured prompting techniques that force agents to explicitly state premises, trace execution paths, and derive formal conclusions improved code review accuracy to 93% in some cases. This supports the view that QA agents need behavioral-constraint-style instructions (step-by-step checklist methodology) rather than informational reference docs.

### Model Routing for QA

QA agents benefit from Claude Opus for complex adversarial review or Sonnet for standard code review, with Haiku appropriate only for lightweight linting-style checks. The `model: opus` frontmatter field in subagent definitions supports this routing [OFFICIAL]. [source: code.claude.com/docs/en/sub-agents]

## E2E / Testing Agents (BDD/Gherkin)

### Role Complexity

E2E agents that generate or execute Gherkin-based acceptance tests occupy a distinct complexity class. They need:

1. **BDD/Gherkin syntax knowledge** — Given/When/Then structure, scenario anatomy
2. **Behavioral specificity constraints** — scenarios must stay behavioral and avoid coupling to implementation
3. **Domain vocabulary** — shared ubiquitous language for the project
4. **Antipatterns in Gherkin** — scenarios that are too specific, test multiple things, or embed technical detail

### Structuring Gherkin Guidelines for Agent Consumption

Academic research from 2025 on LLM-generated Gherkin specifications [PRAC] found that LLMs (including Claude) can derive well-formed Gherkin from domain descriptions, but the quality criteria that mattered most were:
- Relevance: does each scenario test meaningful behavior?
- Singularity: each scenario tests exactly one behavior
- Clarity: human-readable by domain experts

The research recommended including a brief BDD tutorial with worked examples in the agent's context, plus examples of antipatterns (incomplete scenarios, overly specific steps, nested scenarios). [source: arxiv.org/abs/2508.20744]

A 2025 study on agentic BDD test automation [PRAC] found that non-ambiguous prompts and separate agents for each distinct testing task prevented context contamination [source: scitepress.org/Papers/2025/133744]. This supports a subagent-per-concern pattern: one agent generates Gherkin, another executes it, rather than a single E2E agent doing both.

### Delivery Pattern: Progressive Disclosure via Skills

For E2E agents, behavioral spec guidelines are a natural fit for the **skill with progressive disclosure** pattern [OFFICIAL]. The SKILL.md should contain:
- Core BDD principles and the Given/When/Then grammar
- Navigation links to reference files: a Gherkin antipatterns guide, a worked examples file, a domain vocabulary glossary

The domain vocabulary file is particularly well-suited to a separate reference file — it is large, project-specific, and should not consume context tokens on every E2E invocation. The agent reads it only when generating scenarios that require domain-specific language. [source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices]

### Behavioral vs. Constraint Guidelines for E2E

E2E agents need both types:
- **Behavioral constraints**: "Never use UI element IDs in scenario steps," "Each scenario tests one behavior," "Steps must be readable by a non-technical stakeholder"
- **Reference docs**: the domain vocabulary, project feature hierarchy, existing scenario library (to avoid duplication)

The behavioral constraints should live in the subagent system prompt (always active). The reference docs belong in progressively-disclosed skill files.

## PM / Product Manager Agents

### Role Complexity

PM agents generate structured planning artifacts: PRD sections, acceptance criteria, user stories, feature decompositions. Their information needs are:

1. **Output templates** — the structure of a story, PRD section, epic
2. **Product framing rules** — how to express user value, what makes good acceptance criteria
3. **Backlog vocabulary** — project-specific terminology, stakeholder names, domain context

### Lighter Weight Than Technical Agents

PM agents are operationally simpler than QA or E2E agents in one critical respect: their outputs are human-reviewed artifacts rather than executable code. The failure mode is lower stakes (a badly framed user story is caught in review; a missed security antipattern may not be). This has two implications:

1. **Constraint density is lower** — PM agents don't need exhaustive antipattern checklists. Their guidelines focus on format, framing, and completeness rather than prohibitions.
2. **Reference docs matter more relative to constraints** — The PM agent's primary knowledge challenge is domain vocabulary and product context, which is project-specific and variable.

[UNVERIFIED] The 2026 StoriesOnBoard analysis of PM agent architectures noted that effective PM agents work best when given explicit output templates with acceptance criteria structure and quality gates, rather than lengthy procedural rules. [source: storiesonboard.com/blog/ai-agents-product-management-2026]

### Delivery Pattern: System Prompt with Output Templates

For PM agents, the most effective delivery pattern is a moderate-length subagent system prompt containing:
- Role statement: what artifacts the PM agent produces
- Output format templates: the exact structure of a story file, acceptance criteria format
- Quality gate rules: what makes criteria testable vs. vague

Domain vocabulary and project-specific context should flow through the CLAUDE.md cascade or a dedicated project-context skill that the PM agent preloads via `skills:` frontmatter. This separates the invariant methodology (how to write good acceptance criteria) from the variable context (what this specific project's terms mean).

The PubNub subagent best practices analysis [PRAC] specifically recommended that PM agents use read-heavy tool permissions (no write/bash access) since their primary function is analysis and generation, not execution. [source: pubnub.com/blog/best-practices-for-claude-code-sub-agents/]

## SM / Scrum Master Agents

### Role Complexity

SM agents manage sprint process: impediment detection, velocity analysis, sprint health reporting, story prioritization. Their knowledge requirements are process-oriented:

1. **Sprint health criteria** — what metrics indicate a sprint is on track vs. at risk
2. **Impediment patterns** — common blockers and how to surface them
3. **Agile process rules** — what belongs in a sprint, definition of done, story point norms

### The Lightest Guidelines Profile

Among the four non-dev roles, SM agents need the least dense guidelines package. Agile process rules are fairly stable, well-understood by the underlying model from training data, and not especially domain-specific. The primary customization layer is:
- Sprint-specific configuration: team velocity, current sprint goals, story point scale
- Project-specific process rules: any team deviations from standard Scrum

[UNVERIFIED] The Scrum.org Agile Prompt Engineering Framework (2025) emphasized that AI-assisted agile agents benefit most from clearly structured context blocks covering: Agile context definition, core task description, role assignment, output format, and any real/sample data. The role assignment and context components are often the only substantive additions to what the underlying model already knows. [source: scrum.org/resources/blog/agile-prompt-engineering-framework]

### Delivery Pattern: Minimal System Prompt + Sprint Data Injection

SM agents are best served by a compact subagent system prompt covering process rules, with sprint data (current stories, velocity, impediment log) injected at invocation time rather than preloaded. Sprint data is session-specific and rapidly stale, making it a poor candidate for static rules.

This is the sharpest contrast with QA agents: where QA guidelines are stable and should be always-loaded, SM data is volatile and should be JIT-supplied.

## The Constraint vs. Reference Doc Dimension

A critical design decision for each role is whether a given piece of information is:

- **A behavioral constraint** — a rule that must be followed regardless of context (e.g., "never reveal implementation details in Gherkin steps," "always include at least 3 acceptance criteria per story")
- **A reference doc** — knowledge the agent consults when making judgment calls (e.g., domain vocabulary, architecture patterns, example stories)

This distinction maps to delivery mechanism:

| Information Type | Delivery Mechanism | Rationale |
|---|---|---|
| Behavioral constraints | Subagent system prompt (always-loaded) | Must be active on every turn; failure to apply is a defect |
| Antipattern checklists | System prompt or preloaded skill | Checklist density justifies preload; never appropriate to skip |
| Reference docs | Progressive-disclosure skill files | High token cost; only needed for specific tasks |
| Sprint/session data | JIT injection | Volatile; stale data causes worse outputs than no data |
| Domain vocabulary | Project-context skill | Large and project-specific; should not occupy main context |

[OFFICIAL] The Claude skill authoring documentation explicitly encodes this principle: "High freedom" text-based instructions (where multiple approaches are valid) suit QA review and code analysis. "Low freedom" specific-script instructions (where consistency is critical) suit operations like database migrations. The degree-of-freedom setting is a proxy for the constraint vs. reference distinction. [source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices]

## Multi-Role Agent Contexts

When a single agent plays both dev and QA roles — common in smaller teams or quick-fix workflows — guidelines composition requires care. The BMAD multi-agent framework [PRAC] describes this pattern where agents shift roles across workflow steps [source: gist.github.com/seansilva-adam-bot/c57809f1ce4624edea977936de090763].

The most dangerous failure mode in multi-role agents is **role contamination**: dev-mode thinking bleeding into QA review (the agent self-approves its own work). The AddyOsmani "Code Agent Orchestra" analysis [PRAC] explicitly cited this as a reason to use dedicated reviewer agents with read-only tool permissions. A QA subagent that cannot write files cannot accidentally implement a fix in lieu of flagging it. [source: addyosmani.com/blog/code-agent-orchestra/]

For multi-role contexts where a single agent must serve both functions:
- Load dev guidelines and QA guidelines as separate named skills
- Use explicit mode-switching language in the workflow steps ("You are now in QA mode; apply the following checklist...")
- Accept lower quality on QA than a dedicated QA subagent would provide — this is a principled tradeoff

[UNVERIFIED] In practice, the multi-role anti-pattern is best avoided by routing to a dedicated QA subagent on every task completion. The architectural principle from AddyOsmani's analysis — that a Reviewer agent should "auto-trigger on every task completion" — provides the cleanest guarantee that QA is never skipped.

## Role Complexity → Delivery Mechanism Map

Synthesizing the findings above, role complexity and optimal delivery mechanism are correlated as follows:

**Note on complexity definition:** "Complexity" here refers to *guidelines density* — how dense and domain-specific the agent's required guidelines are. This is distinct from *task complexity* as used in some other frameworks. `gemini-deep-research-output.md` rates QA as "Low (Goal-heavy)" — this reflects QA's narrow task goal (find violations) rather than the density of knowledge it needs to do so. In this file's framing, QA requires the densest guidelines package of any non-dev role because its effectiveness depends entirely on comprehensive, curated antipattern checklists. Both framings are valid; they measure different dimensions.

**QA/Code-Review (highest guidelines density):**
- System prompt: dense antipattern checklist, review methodology, output format
- Preloaded skills: language-specific or framework-specific antipatterns when multi-language
- Tools: read-only (Glob, Grep, Read, Bash)
- Model: Sonnet (standard review), Opus (security-critical review)
- `paths:` scoping: desired but currently unreliable (open bug)

**E2E/Testing (high complexity, behavioral focus):**
- System prompt: BDD methodology, singularity/clarity constraints
- Progressive-disclosure skill: Gherkin reference, domain vocabulary, example library
- Tools: read-only plus test runner access if executing tests
- Model: Sonnet
- Separate subagents for generation vs. execution

**PM (medium complexity, format-driven):**
- System prompt: output templates, quality gates for acceptance criteria
- Preloaded skill: project-context (stakeholders, domain vocabulary, feature hierarchy)
- Tools: read-only
- Model: Haiku (standard story generation), Sonnet (PRD creation)

**SM (lowest complexity, process + data):**
- System prompt: process rules, sprint health criteria
- JIT injection: sprint data at invocation time
- Tools: read-only
- Model: Haiku (reporting), Sonnet (complex impediment analysis)

## Current State of `paths:` Frontmatter for File-Scoped QA Rules

The `paths:` frontmatter feature in `.claude/rules/` was designed to enable precision-scoped rules — applying Kotlin rules only to `.kt` files, test rules only to `*Test.kt` files. This is a compelling architecture for QA agents that should fire different checklists for different file types.

However, as of the open GitHub issue #16299 (reported and still open as of February 2026), the current implementation loads all rules globally at session start rather than triggering on path match. The issue affects projects with many directory-specific rules significantly — one user reported 28 rules loading when only ~5 should be global, causing context bloat. [source: github.com/anthropics/claude-code/issues/16299]

Additionally, GitHub issue #13905 [OFFICIAL] identified invalid YAML syntax requirements for the `paths:` field when glob patterns begin with `{` or `*` (both reserved YAML indicators requiring quoting). These are exactly the patterns most useful for file-type scoping. [source: github.com/anthropics/claude-code/issues/13905]

**Practical guidance until these bugs are fixed:** Move file-type-specific QA guidelines into dedicated QA subagents with tool restrictions rather than relying on `paths:` scoping. The subagent architecture gives deterministic, per-invocation isolation that `paths:` is intended but currently failing to provide.

## Evidence on System Prompts vs. File-Based Guidelines for Non-Dev Roles

The empirical literature on this question is indirect as of April 2026 — no study directly compares system prompt delivery vs. file-based delivery for PM or SM agents specifically. However, several lines of evidence converge:

1. **AGENTS.md efficiency study (2025)** [PRAC]: Developer-authored context files in the repository reduced token usage and execution time for coding agents. The benefit came from eliminating exploratory navigation. For non-dev roles like QA, this maps to antipattern checklists that guide review methodology — agents with checklists explore less and verify more systematically. [source: arxiv.org/html/2601.20404]

2. **BMAD manifest study (2025)** [PRAC]: Analysis of 253 Claude.md files found that testing content (60.5%) and implementation details (71.9%) were the most prevalent categories. Only 15.4% explicitly defined agent roles and responsibilities. This suggests the community has not yet fully adopted role-specific manifest design — most manifests remain developer-workflow-focused. [source: arxiv.org/html/2509.14744v1]

3. **Skill architecture design (2026)** [OFFICIAL]: The Claude skills documentation's principle of "progressive disclosure" provides the strongest framework for complex roles: load only metadata at startup, reveal full content on demand. For QA agents reviewing specific code, this means antipattern checklists are loaded exactly when review begins and not before, preventing context dilution in upstream planning phases. [source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices]

4. **Human-curated > LLM-generated guidelines** [PRAC]: The AddyOsmani analysis citing research on AGENTS.md found that "LLM-generated AGENTS.md files offer no benefit and can marginally reduce success rates (~3%)." This is a critical finding for non-dev roles: PM and SM agents whose guidelines were auto-generated by another agent perform worse than agents with no guidelines. Human-authored guidelines are required for reliable non-dev agent quality. [source: addyosmani.com/blog/code-agent-orchestra/]

## Sources

- [OFFICIAL] Create custom subagents — Claude Code Docs: https://code.claude.com/docs/en/sub-agents
- [OFFICIAL] Skill authoring best practices — Claude API Docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- [OFFICIAL] Agent Skills overview — Claude API Docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- [OFFICIAL] Best Practices for Claude Code — Claude Code Docs: https://code.claude.com/docs/en/best-practices
- [OFFICIAL] Skills explained — claude.com/blog: https://claude.com/blog/skills-explained
- [OFFICIAL] Bug: Path-scoped rules load globally #16299: https://github.com/anthropics/claude-code/issues/16299
- [OFFICIAL] Bug: Invalid YAML syntax in paths frontmatter #13905: https://github.com/anthropics/claude-code/issues/13905
- [OFFICIAL] How Claude Code Builds a System Prompt (April 2026): https://www.dbreunig.com/2026/04/04/how-claude-code-builds-a-system-prompt.html
- [PRAC] On the Impact of AGENTS.md Files on AI Coding Agent Efficiency (arxiv, Jan 2025): https://arxiv.org/html/2601.20404
- [PRAC] On the Use of Agentic Coding Manifests: Empirical Study of Claude Code (arxiv, Sept 2025): https://arxiv.org/html/2509.14744v1
- [PRAC] From Law to Gherkin: LLM-Generated Behavioural Specifications (arxiv, Aug 2025): https://arxiv.org/abs/2508.20744
- [PRAC] Agentic AI for BDD Testing Using LLMs (scitepress, 2025): https://www.scitepress.org/Papers/2025/133744/133744.pdf
- [PRAC] Agentic Quality Assurance Guide — Tricentis: https://www.tricentis.com/learn/agentic-quality-assurance
- [PRAC] Best practices for Claude Code subagents — PubNub: https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
- [PRAC] The Code Agent Orchestra — Addy Osmani: https://addyosmani.com/blog/code-agent-orchestra/
- [PRAC] 30 Tips for Claude Code Agent Teams: https://getpushtoprod.substack.com/p/30-tips-for-claude-code-agent-teams
- [PRAC] Claude Agent Skills: First Principles Deep Dive (Oct 2025): https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
- [PRAC] AI Agents In Product Management 2026 — StoriesOnBoard: https://storiesonboard.com/blog/ai-agents-product-management-2026
- [PRAC] Agile Prompt Engineering Framework — Scrum.org: https://www.scrum.org/resources/blog/agile-prompt-engineering-framework
- [PRAC] Some notes on AI Agent Rule / Instruction / Context files (0xdevalias gist): https://gist.github.com/0xdevalias/f40bc5a6f84c4c5ad862e314894b2fa6
- [PRAC] BMAD + Multi-Agent Orchestration gist: https://gist.github.com/seansilva-adam-bot/c57809f1ce4624edea977936de090763
- [PRAC] Regulating the Agency of LLM-based Agents (arxiv, Sept 2025): https://arxiv.org/html/2509.22735v1
- [PRAC] AI Agents for Project Management 2026 — Epicflow: https://www.epicflow.com/blog/ai-agents-for-project-management/
- [PRAC] State of Agent Engineering — LangChain 2025: https://www.langchain.com/state-of-agent-engineering
