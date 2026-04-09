---
content_origin: claude-code-subagent
date: 2026-04-09
sub_question: "What are the best architectural patterns for the generic-agent + injected-guidelines = specialized-agent model — how should project-specific guidelines be structured, stored, and delivered?"
topic: "Agent-specific guidelines architecture in Claude Code"
---

# Generic Agent + Injected Guidelines = Specialized Agent: Architectural Patterns

**Date:** 2026-04-09
**Research type:** Technical — multi-source, web-verified

---

## 1. The Core Problem and Why It Matters

The generic-agent-plus-specialization model is the dominant pattern in production multi-agent systems as of April 2026. The problem it solves: you have well-defined roles (Dev, QA, E2E, PM, SM) with stable orchestration patterns, but those roles must produce radically different behavior depending on which project they are operating on. A "Dev" agent implementing a Kotlin Compose story needs to know Kotlin 2.3.20 APIs, CMP 1.10.3 navigation patterns, and Kotest 6.1.9 prohibitions. The same "Dev" agent implementing a Python FastAPI story needs entirely different knowledge. Embedding all of this in the generic agent definition produces context bloat and cross-domain interference ("guideline bleed"). Encoding nothing means the agent operates on stale training data.

The optimal solution is a composition at runtime: `generic_agent + project_guidelines = specialized_agent`. The architecture questions are: how should the guidelines be structured, where should they live, and what delivery mechanism minimizes context cost while maximizing adherence reliability?

---

## 2. Claude Code's Native Delivery Mechanisms

**[OFFICIAL]** Claude Code (as of v2.1.x, April 2026) provides five mechanisms for delivering guidelines to agents, each with different scope and cost characteristics.

### 2.1 CLAUDE.md Hierarchy

CLAUDE.md files load at session start and survive `/compact`. They exist at multiple scope levels:

| Level | Location | Scope |
|---|---|---|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Organization-wide |
| Personal global | `~/.claude/CLAUDE.md` | All projects, this user |
| Personal rules | `~/.claude/rules/*.md` | All projects, always loaded |
| Project | `./CLAUDE.md` | This project, every session |
| Project local | `./CLAUDE.local.md` | Personal, not committed |
| Project rules (unconditional) | `.claude/rules/*.md` (no `paths:`) | This project, always loaded |
| Project rules (path-scoped) | `.claude/rules/*.md` with `paths:` | This project, loaded on file match |
| Subdirectory | `./src/CLAUDE.md` | Loaded on demand when in that dir |

Source: [Official docs: Memory](https://code.claude.com/docs/en/memory), [Technical Agent Guidelines Authoring Research 2026-04-03](../../../planning-artifacts/research/technical-agent-guidelines-authoring-research-2026-04-03.md) [OFFICIAL]

CLAUDE.md supports `@path/to/file` import syntax (max recursion depth 5), enabling modular composition. Content is advisory — not deterministic — but benefits from Anthropic's prompt caching on re-reads.

### 2.2 Path-Scoped Rules (`.claude/rules/` with `paths:` frontmatter)

**This is the most important mechanism for technology-specific specialization** when functioning as intended. A rule file with `paths: ["**/*Test.kt", "**/*Spec.kt"]` loads only when Claude reads a file matching those patterns — zero cost when irrelevant. This enables "just-in-time" specialization: the Kotlin testing guidelines only appear when the agent is actually working with test files.

**Current reliability caveat:** `research-guideline-volume-adherence.md` in this corpus (Section 6) documents a confirmed bug (GitHub issue #16299, open as of February 2026) where path-scoped rules load globally at session start rather than conditionally on file read. This means the JIT benefit may not currently be realized. Verify actual behavior with the `InstructionsLoaded` hook before relying on this mechanism for context reduction. The architectural intent is sound; the current implementation has documented regressions.

```yaml
---
paths:
  - "**/*Test.kt"
  - "**/*Spec.kt"
---
# Kotest 6.1 Guidelines
...
```

**Known limitation:** Path-scoped rules trigger on Read operations only, not on Write or create operations. When creating a new file from scratch, the path-based rules do not inject. [PRAC: GitHub issue #23478, confirmed NOT_PLANNED status]. The workaround is a `PreToolUse` hook that forces a Read before Write, or unconditional rules for technologies where new file creation is common.

**Additional limitation:** `paths:` frontmatter does not work in user-level rules (`~/.claude/rules/`). It functions correctly only in project-level `.claude/rules/`. [PRAC: GitHub issue #21858]

Source: [GitHub issue #23478](https://github.com/anthropics/claude-code/issues/23478), [GitHub issue #21858](https://github.com/anthropics/claude-code/issues/21858) [PRAC]

### 2.3 Subagent `skills:` Frontmatter (Explicit Startup Injection)

Subagent definitions (`.claude/agents/*.md`) support a `skills:` field that injects the full content of specified skills into the subagent's context at startup — not just availability metadata, but the entire skill content. This is the explicit, guaranteed delivery path for subagent specialization.

```yaml
---
name: kotlin-dev
description: Implements Kotlin Multiplatform stories
skills:
  - kmp-project-guidelines
  - compose-ui-patterns
  - kotest-tdd-workflow
---
You are a senior Kotlin Multiplatform developer. Follow the preloaded skills for all implementation work.
```

The full content of each skill is injected, not just made available. The subagent does not need to discover or load them during execution — they arrive in the initial context. [OFFICIAL]

**Critical limitation for Agent Teams:** The `skills:` frontmatter field is NOT applied when a subagent definition runs as a teammate in an Agent Team. Teammates load skills from project and user settings, the same as a regular session. [OFFICIAL: agent-teams docs]. This means for Agent Teams, specialization must flow through CLAUDE.md/path-scoped rules (which teammates load automatically) rather than through subagent `skills:` injection.

Source: [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents), [Orchestrate teams — Claude Code Docs](https://code.claude.com/docs/en/agent-teams) [OFFICIAL]

### 2.4 Subagent Filesystem Discoverability (Undocumented but Verified)

Despite documentation stating "subagents don't inherit skills from the parent conversation," subagents with filesystem access can self-discover and invoke project skills by scanning `.claude/skills/*/SKILL.md` via Glob. This is not configuration — it's an emergent capability from file access.

The distinction matters:
- `skills:` frontmatter = startup injection into system context (guaranteed, no discovery needed)
- filesystem access = runtime discovery (requires the agent to scan)

A subagent without `skills:` cannot use skills immediately but can discover them. The `skills:` field controls injection timing, not access. To prevent a subagent from using specific skills, use `disallowedTools: Skill(skill-name)`.

Source: [GitHub issue #32910](https://github.com/anthropics/claude-code/issues/32910) [PRAC]

### 2.5 Spawn Prompt Direct Injection

When an orchestrator spawns a subagent via the Agent tool, the spawn prompt is the subagent's "first user turn." This is a direct channel for task-specific context: the spawning agent can include relevant guidelines, story context, and technology reminders inline. This is the most targeted delivery mechanism — content appears exactly once, for exactly this invocation.

Spawn prompt injection is the right layer for story-specific constraints ("This story uses Room 2.8 migrations — see the NEVER rules for Room 2.8 in the spawn context"). It complements, rather than replaces, persistent guidelines.

---

## 3. The Three-Layer Architecture: Evidence-Based Design

The Momentum architecture and external research converge on a three-layer model. [PRAC] This is not arbitrary — it maps directly to three different cost profiles:

### Layer 1: Path-Scoped Rules (`.claude/rules/`, 30-80 lines per file)

**What:** Short, high-signal files loaded on file access. One technology per file.
**Content:** Version pins, prohibition-format corrections, critical anti-patterns.
**Load timing:** On-demand, when agent reads matching files. Zero cost otherwise.
**Instruction budget impact:** Low. 30-80 lines, only loaded when relevant.

This is the primary mechanism for technology specialization. A generic Dev agent working in `src/ui/HomeScreen.kt` automatically receives Compose UI guidelines without any explicit injection — the path-scope wires it transparently.

Example from Momentum's own research (April 2026):
```
.claude/rules/
  kotest.md        (paths: ["**/*Test.kt", "**/*Spec.kt"])
  compose-ui.md    (paths: ["**/ui/**/*.kt", "**/*Screen.kt"])
  kmp-project.md   (paths: ["**/build.gradle.kts"])
```

### Layer 2: Reference Docs (`docs/references/`, 100-300 lines)

**What:** On-demand reference material containing worked examples.
**Content:** Correct patterns the agent's training data gets wrong, with code examples.
**Load timing:** When the agent explicitly reads the file (via `@`-import or direct reference from Layer 1).
**Instruction budget impact:** Zero (only when accessed).

Layer 1 rules point here: "For Navigation 3 patterns, read `docs/references/navigation3-patterns.md`."

### Layer 3: Skills (`.claude/skills/`, unlimited)

**What:** Full procedural workflows for complex, multi-step tasks.
**Content:** Setup procedures, migration guides, domain-specific workflows.
**Load timing:** When explicitly invoked or preloaded via `skills:` frontmatter.
**Instruction budget impact:** Zero unless injected at startup.

Source: [Agent Guidelines Authoring Research 2026-04-03](../../../planning-artifacts/research/technical-agent-guidelines-authoring-research-2026-04-03.md), [Momentum Architecture Decision 26](../../../planning-artifacts/architecture.md) [PRAC/OFFICIAL]

---

## 4. Specialization Transparency: Can the Agent Know?

A key design question: does the generic agent need to know it's being specialized, or can specialization be fully transparent?

**The answer is both, depending on the mechanism:**

**Transparent (file-system-driven, no explicit agent knowledge required):**
- Path-scoped rules in `.claude/rules/` inject automatically when matching files are accessed
- CLAUDE.md files at project level load for all agents in the project
- Teammates in Agent Teams load CLAUDE.md and project skills automatically
- The generic agent receives specialization as part of its context without any explicit recognition

**Explicit (spawn-time injection, agent knows what it has):**
- `skills:` frontmatter on subagent definitions
- Spawn prompt direct injection
- The orchestrating agent must intentionally wire the specialization

**Momentum's architecture (Decision 26) uses both:** the path-scoped rules provide transparent baseline specialization at the file access layer, while sprint planning's team composition decision explicitly wires role-specific guidelines into spawn prompts for story-level context. The generic agent doesn't need to understand what project it's on — the file-system delivers what it needs when it needs it.

This is the "composition through infrastructure" pattern: the agent's behavior is specialized not by teaching it about the project but by changing what knowledge appears in its context window when it works.

---

## 5. The Project-Level Override/Extension Pattern

The Claude Code authority hierarchy enables a clean layered specialization model:

1. **Global base layer** (`~/.claude/CLAUDE.md`, `~/.claude/rules/`): Momentum practice defaults — commit conventions, workflow rules, general coding standards. Applies to all projects.
2. **Project layer** (`.claude/rules/*.md`, `./CLAUDE.md`): Stack-specific guidelines — technology prohibitions, version pins, framework patterns. Applies to this project only, all agents.
3. **Story layer** (spawn prompt inline context): Task-specific constraints — the current story's AC, specific APIs to use or avoid, this iteration's scope. One-time, ephemeral.

**Later-loaded files have higher effective priority** because Claude reads the full hierarchy bottom-up. A project rule that says "Use Compose Navigation 3" overrides a global rule that says "Use standard Android navigation." This override mechanism is the correct way to extend Momentum's defaults for a project without modifying the global rules.

The extension pattern vs. the override pattern:
- **Extension**: project CLAUDE.md adds new rules for technologies the global layer doesn't cover (Kotlin, Compose, Kotest)
- **Override**: project `.claude/rules/` file explicitly corrects a global default for this stack

Both are valid and compose cleanly through the hierarchy.

---

## 6. How the `agent-guidelines` Skill Operationalizes This

Momentum's `momentum:agent-guidelines` skill is the tooling layer for the generic → specialized transformation. Its workflow (as implemented April 2026):

1. **Discover**: parallel subagents scan build files, existing rules, test configs, and source patterns
2. **Research**: focused web searches per detected technology (2-3 per tech, prohibition format)
3. **Consult**: interactive decisions on scope, path patterns, content depth
4. **Generate**: parallel generation of path-scoped Layer 1 rules (30-80 lines each), Layer 2 reference docs (100-300 lines), CLAUDE.md pointer updates
5. **Validate**: AVFL checkpoint on all artifacts

The key design choice: generic agents carry practice and workflow; generated project rules carry technology corrections. They compose automatically through the file system at runtime via path-scoped loading. The sprint planning phase then wires these together explicitly when building the team composition — matching story `change_type` to specialist role, then attaching the appropriate project guidelines for that role.

---

## 7. Patterns from Other Multi-Agent Systems

### 7.1 CrewAI — Role-Based System Prompt Construction

CrewAI generates agent system prompts from three fields combined: `role`, `backstory`, and `goal`. The generic pattern is:

```
"You are {role}. {backstory}. Your personal goal is: {goal}"
```

Specialization is achieved by varying these fields per agent instance, not by maintaining a generic class. CrewAI has no path-scoped loading — all specialization is explicit at agent definition time. [OFFICIAL: CrewAI docs]

**Implication for Claude Code:** The CrewAI model works when you always know which specialist you need. Claude Code's path-scoped approach enables dynamic specialization based on what files are being touched — more adaptive to the actual work rather than pre-declared role types.

### 7.2 LangGraph — Progressive Skill Loading

A February 2026 architectural pattern from LangGraph practitioners: avoid stuffing the system prompt with all domain knowledge upfront. Instead, use a three-tier progressive disclosure:

- **Tier 1**: lightweight skill catalog (~500 tokens) in the system prompt
- **Tier 2**: full skill instructions (~2,000 tokens) loaded on demand via `load_skill()` tool
- **Tier 3**: specific reference files loaded via `read_skill_file()` tool

This mirrors Claude Code's Layer 1/2/3 architecture but uses explicit tool calls rather than file-system path matching for triggering. [PRAC: "Stop Stuffing Your System Prompt" — Medium, Feb 2026]

The practical finding: "progressive loading is not automatically superior" for tightly scoped domains with stable behavior. A single compressed prompt may outperform modular architectures when the domain is known and bounded. This is a useful corrective — don't over-engineer when the agent will always need the same knowledge.

### 7.3 Google ADK — Instruction + Description Separation

Google's Agent Development Kit (2025-2026) separates two concerns:
- **Description**: metadata for routing (what tasks should reach this agent)
- **Instruction**: behavioral guidance (what the agent does)

Specialization flows through `session.state` using `output_key` templating: downstream agents reference prior outputs via `{raw_text}` in their instructions. This is a stateful composition model — agents are specialized not just at startup but by what has accumulated in the shared session state. [OFFICIAL: Google Developers Blog]

**Implication:** For Claude Code, the Agent tool's spawn prompt plays the `output_key` role — sprint planning's team composition decision embeds story-specific context that makes the generic Dev agent a specialized Kotlin Dev for this particular task.

### 7.4 AutoGen — Conversational Context Accumulation

AutoGen specializes agents through conversational negotiation — agents exchange messages to refine their understanding of a task. Specialization is emergent from dialogue rather than pre-configured. This trades reliability for flexibility: agents adapt to context they couldn't anticipate, but adherence to specific technical requirements is less guaranteed. [PRAC: various framework comparisons 2025-2026]

**Implication:** Claude Code's model is closer to LangGraph/CrewAI (pre-configured specialization with file-system adaptation) than AutoGen (emergent). For technical stack guidelines requiring precise prohibitions, pre-configured specialization via rules files is more reliable than emergent conversational specialization.

---

## 8. Guideline Content Principles (Evidence-Based)

These principles apply regardless of delivery mechanism:

**Prohibition format over aspiration:** "NEVER use `createComposeRule()` in commonTest — it requires JUnit. Use `runComposeUiTest {}` instead" outperforms "Write platform-portable test code" in adherence studies. [PRAC: "Curse of Instructions" paper, IFScale study]

**Critical-first ordering:** LLM attention follows a "lost in the middle" pattern. Critical rules must be at the top of the file. Order: version pins → critical prohibitions → conventions → setup. [PRAC: multiple sources]

**Version pins prevent hallucination:** Models hold multiple incompatible versions of APIs in training data. Without explicit `Kotlin 2.3.20 (not 2.0.x — the APIs are incompatible)`, the agent will pick arbitrarily. [PRAC: Agent Rules Builder guide]

**30-80 lines per rules file:** At 80 lines, the file is at the upper bound where rule density remains effective. Above this, split into multiple scoped files or move detail to Layer 2. [PRAC: HumanLayer, Momentum research]

**Don't document the inferable:** If the agent can read it from `build.gradle.kts`, don't repeat it in a rules file. Guidelines should correct what training data gets wrong — not restate what configuration files already say. [PRAC: Stack Overflow Blog, March 2026]

**Emphasis markers work but erode:** "NEVER", "IMPORTANT", "CRITICAL", "YOU MUST" improve adherence for individual rules. Use sparingly — if everything is critical, the markers lose their signal. [OFFICIAL: Anthropic best practices]

---

## 9. Practical Architecture for Momentum's Use Case

Synthesizing all research, the optimal architecture for Momentum's multi-project, multi-role generic agent model:

### Storage Layout

```
{project}/
  .claude/
    rules/
      {technology}.md           # Layer 1, path-scoped, 30-80 lines each
      {role}-unconditional.md    # Layer 1, unconditional, role-wide rules
    agents/
      kotlin-dev.md              # Subagent definition with skills: field for explicit injection
      kotlin-qa.md               # Different role, different skills
  docs/
    references/
      {technology}-patterns.md   # Layer 2, on-demand reference examples
  CLAUDE.md                     # Pointers to reference docs, high-level project context
```

### Delivery Decision Tree

1. **Does the guideline apply to all work on this project, regardless of role?** → CLAUDE.md
2. **Does the guideline apply only when working with specific file types?** → Path-scoped `.claude/rules/{technology}.md`
3. **Is the guideline role-specific (only the Dev needs it, not QA)?** → Subagent `skills:` field on the role's `.claude/agents/` definition
4. **Is this story-specific context (current task's scope)?** → Spawn prompt direct injection
5. **Does it require worked examples and patterns the agent reads on demand?** → `docs/references/{technology}-patterns.md` (Layer 2)
6. **Is it a complex multi-step workflow?** → Layer 3 skill

### Role Specialization via Subagent Definitions

For the Momentum multi-role model, each role gets its own subagent definition with role-appropriate skills pre-loaded:

```yaml
# .claude/agents/kotlin-dev.md
---
name: kotlin-dev
description: Implements Kotlin Multiplatform stories following TDD workflow
skills:
  - kmp-project-guidelines    # Layer 1 content in skill form for explicit injection
  - compose-ui-patterns
  - kotest-tdd-workflow
model: sonnet
---
You are a senior Kotlin Multiplatform developer. Implement the assigned story.
Follow the TDD workflow: write failing tests first, then implement.
```

```yaml
# .claude/agents/kotlin-qa.md
---
name: kotlin-qa
description: Reviews Kotlin implementation against acceptance criteria
skills:
  - kotest-assertions
  - compose-testing-patterns
model: sonnet
tools: Read, Grep, Glob, Bash
---
You are a QA engineer. Review the implementation against the story's ACs.
```

The generic "Dev" and "QA" roles become project-specific specialists through the skills field. Swapping this project's `skills:` list for a Python project's list produces a Python Backend Dev from the same generic role structure.

### Agent Teams Workaround

Because the `skills:` field does not apply in Agent Teams, specialization for teammates must flow through path-scoped rules and project CLAUDE.md. Teams naturally inherit all project context — the CLAUDE.md pointers to reference docs work. The workaround for team-specific knowledge injection is: include technology-specific instructions directly in the teammate's spawn prompt from the orchestrator, rather than relying on `skills:` frontmatter.

---

## 10. Key Tradeoffs and Gotchas

**Path-scoped rules don't fire on file creation.** If an agent creates a new file without first reading it, path rules don't load. Mitigate with a `PreToolUse` hook that creates the file empty first, forcing a subsequent Read → Edit pattern. [PRAC: GitHub #23478]

**`skills:` injection is subagent-only, not teammate.** Agent Teams (experimental as of April 2026) don't inherit the `skills:` field. This is a significant gap for the Momentum model if it moves to Agent Teams for multi-agent sprint work.

**Filesystem discovery is a fallback, not a replacement.** Subagents without explicit `skills:` can discover project skills by scanning `.claude/skills/`, but this requires the agent to take an action. The `skills:` field guarantees the content is present without any agent initiative. For time-sensitive, high-adherence requirements, explicit injection is required. [PRAC: GitHub #32910]

**The "Curse of Instructions" is real.** P(all rules followed) = P(individual)^n. At 150 instructions, adherence drops substantially even for strong models. Every rule file added to the always-loaded context competes with every other rule. Path-scoping is not optional — it is the fundamental mechanism that keeps the instruction budget usable. [PRAC: IFScale arxiv paper, "Curse of Instructions" paper]

**Don't over-specialize.** For tightly scoped domains with stable behavior, a single compressed system prompt in the subagent definition body may outperform a modular, multi-layer architecture. The LangGraph practitioner finding applies here: match architecture complexity to actual domain complexity. [PRAC: Medium article, Feb 2026]

---

## Sources

- [Official Claude Code Docs: Create custom subagents](https://code.claude.com/docs/en/sub-agents) [OFFICIAL]
- [Official Claude Code Docs: Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams) [OFFICIAL]
- [Official Claude Code Docs: Best Practices](https://code.claude.com/docs/en/best-practices) [OFFICIAL]
- [Official Claude Code Docs: Memory](https://code.claude.com/docs/en/memory) [OFFICIAL]
- [GitHub: Path-based rules not loaded on Write — Issue #23478](https://github.com/anthropics/claude-code/issues/23478) [PRAC]
- [GitHub: paths: frontmatter ignored in user-level rules — Issue #21858](https://github.com/anthropics/claude-code/issues/21858) [PRAC]
- [GitHub: Subagents can discover all project skills via filesystem — Issue #32910](https://github.com/anthropics/claude-code/issues/32910) [PRAC]
- [Stop Stuffing Your System Prompt: Build Scalable Agent Skills in LangGraph (Feb 2026)](https://pessini.medium.com/stop-stuffing-your-system-prompt-build-scalable-agent-skills-in-langgraph-a9856378e8f6) [PRAC]
- [Google Developers Blog: Developer's guide to multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) [OFFICIAL]
- [CrewAI Docs: Agents](https://docs.crewai.com/en/concepts/agents) [OFFICIAL]
- [Claude Code Agent Teams: Setup & Usage Guide 2026](https://claudefa.st/blog/guide/agents/agent-teams) [PRAC]
- [Trensee: Claude Code Skills, Fork, and Subagents (Mar 2026)](https://www.trensee.com/en/blog/explainer-claude-code-skills-fork-subagents-2026-03-31) [PRAC]
- [Claude Code Rules Directory: Modular Instructions That Scale](https://claudefa.st/blog/guide/mechanics/rules-directory) [PRAC]
- [Multi-Agent System Patterns: A Unified Guide](https://medium.com/@mjgmario/multi-agent-system-patterns-a-unified-guide-to-designing-agentic-architectures-04bb31ab9c41) [PRAC]
- [How Many Instructions Can LLMs Follow at Once? — IFScale (arxiv, July 2025)](https://arxiv.org/html/2507.11538v1) [PRAC]
- [Momentum Architecture — Decision 26: Two-Layer Agent Model](../../../planning-artifacts/architecture.md) [INTERNAL — relative path; validity unverified by this research pass]
- [Agent Guidelines Authoring Research 2026-04-03](../../../planning-artifacts/research/technical-agent-guidelines-authoring-research-2026-04-03.md) [INTERNAL — relative path; validity unverified by this research pass]
- [agent-guidelines workflow.md](../../../../skills/momentum/skills/agent-guidelines/workflow.md) [INTERNAL — relative path; validity unverified by this research pass]
