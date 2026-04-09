---
title: "Agent-Specific Guidelines Architecture in Claude Code — Research Report"
date: 2026-04-09
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: true
derives_from:
  - path: raw/research-claude-code-scoping-mechanisms.md
    relationship: synthesized_from
  - path: raw/research-guideline-volume-adherence.md
    relationship: synthesized_from
  - path: raw/research-dense-domain-guidelines-structure.md
    relationship: synthesized_from
  - path: raw/research-non-dev-agent-guidelines.md
    relationship: synthesized_from
  - path: raw/research-generic-agent-injection-patterns.md
    relationship: synthesized_from
  - path: raw/research-role-guideline-isolation.md
    relationship: synthesized_from
  - path: raw/gemini-deep-research-output.md
    relationship: synthesized_from
  - path: validation/avfl-report.md
    relationship: validated_by
  - path: raw/practitioner-notes.md
    relationship: informed_by
---

# Agent-Specific Guidelines Architecture in Claude Code

## Executive Summary

The central challenge for Momentum's agent-guidelines architecture is delivering dense, role-specific behavioral knowledge to generic agents without context dilution or cross-role bleed — across six or more distinct roles (dev variants, QA, E2E, PM, SM, skill-dev) that may coexist on a single project. This report synthesizes findings from six targeted research files, a Gemini Deep Research session, AVFL validation, and practitioner notes to produce actionable architectural guidance for the skill redesign.

The research establishes three foundational facts. First, **subagents spawned via the Agent tool do not reliably inherit CLAUDE.md or `.claude/rules/` files** — this is confirmed by GitHub issue #29423 (open April 2026), corroborated by #8395 (closed "not planned"), and documented through concrete failure cases where subagents missed violations because they operated without project rules [PRAC]. The only guaranteed delivery channels to a subagent are its system prompt body, explicitly listed `skills:` in frontmatter, and the Agent tool's spawn prompt string [OFFICIAL]. Second, **guideline adherence degrades non-linearly with instruction volume** — reasoning-class models maintain near-perfect compliance through approximately 100-150 simultaneous instructions before entering steep degradation, while Sonnet-class models show linear decay from the start [OFFICIAL]. Anthropic's own guidance caps CLAUDE.md at 200 lines and names "the over-specified CLAUDE.md" as an antipattern [OFFICIAL]. Third, **path-scoped rules (`paths:` frontmatter) have a documented regression** (GitHub #16299, open February 2026) that causes all rules to load globally rather than conditionally on file access, negating the JIT benefit that makes the mechanism architecturally valuable [PRAC].

These three facts converge on a single design imperative: Momentum must adopt **explicit injection as the primary delivery mechanism** for role-specific guidelines, with `.claude/rules/` path-scoped files as a secondary ambient layer for the main CLI session. The current architecture — which generates `.claude/rules/` files and relies on inheritance for subagent delivery — has a confirmed gap for every role except `dev` (which already receives guidelines via an explicit `guidelines` parameter). The redesigned skill must close this gap for QA, E2E, PM, SM, and skill-dev agents by generating role-specific guideline files that are explicitly injected at spawn time.

---

## 1. Scoping Mechanisms: What Actually Reaches Each Agent Role

**Sub-question:** What Claude Code mechanisms most effectively scope guidelines to specific agent roles — CLAUDE.md hierarchy, paths: frontmatter rules, subagent system prompts, worktree isolation — and what are their tradeoffs across all role types?

### The Delivery Hierarchy

Claude Code provides five mechanisms for delivering guidelines to agents, ranked by delivery reliability:

| Mechanism | Reliability | Scope | Role-Targetable? |
|---|---|---|---|
| Subagent system prompt body | Highest — always in context | Per-agent definition | Yes |
| `skills:` frontmatter injection | High — injected at startup | Per-agent definition | Yes |
| Agent tool spawn prompt | Medium-high — ephemeral per invocation | Per-task | Yes |
| CLAUDE.md hierarchy | Medium — loads for main session, unreliable for subagents | Project-wide | No |
| `paths:` frontmatter rules | Conditional — JIT on file access (when working) | File-pattern | No |

[OFFICIAL] The subagent system prompt body replaces the default Claude Code system prompt entirely. A subagent receives: (1) its own system prompt, (2) environment details, (3) skills listed in its `skills:` frontmatter, and (4) the Agent tool's prompt string. It does NOT receive the parent's conversation history, prior tool results, or the parent's system prompt.

[OFFICIAL] CLAUDE.md content is delivered as a **user message** after the system prompt, not as part of the system prompt itself. Anthropic's documentation explicitly states: "Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions."

### The Subagent Inheritance Problem

This is the most consequential finding for the skill redesign. Three sources in the research corpus make contradictory claims about whether subagents inherit project CLAUDE.md:

1. The scoping mechanisms research states: "in the interactive CLI, project CLAUDE.md does load for subagents" [OFFICIAL]
2. The role-guideline-isolation research documents GitHub #29423: "Task subagents do NOT load CLAUDE.md, .claude/rules/, or ~/.claude/CLAUDE.md" — with a concrete failure case of 5 missed violations [PRAC]
3. The Gemini deep research claims: "subagents inherit the root CLAUDE.md" [SUSPECT — no citation]

**Reconciliation:** The behavior likely differs between interactive CLI sessions (where CLAUDE.md may load as part of the session environment) and Task/SDK-spawned subagents (where #29423 documents non-loading). The safe architecture is to treat CLAUDE.md inheritance as unreliable and embed all required conventions in each agent's system prompt or inject them explicitly at spawn time [PRAC].

### Mechanism Tradeoffs by Role Type

**Path-scoped rules** target file types, not agent roles. A QA agent reviewing `src/ui/HomeScreen.kt` loads Compose rules — useful if the QA agent needs them, harmful if it does not. Path scoping serves technology specialization, not role specialization [OFFICIAL].

**Worktree isolation** prevents file conflicts in parallel execution. It does NOT change which guidelines load — worktrees share the same `.claude/` directory structure. Worktrees solve a concurrency problem, not a guidelines scoping problem [OFFICIAL].

**The `skills:` frontmatter field** provides the cleanest path for the generic-agent + injected-guidelines pattern. Skills listed in subagent frontmatter are injected in full at startup — not lazily loaded, not discoverable. However, this field does NOT apply when a subagent runs as a teammate in Agent Teams [OFFICIAL]. For Agent Teams, specialization must flow through CLAUDE.md and path-scoped rules (which teammates load automatically) or through the spawn prompt.

### Momentum-Specific Constraint

Momentum agents are NOT registered in `.claude/agents/`. They are defined in `skills/momentum/agents/*.md` and spawned via the Agent tool with their markdown bodies used as system prompts [PRAC]. This means the `skills:` frontmatter field is not available — guidelines must flow through either the agent definition body itself or the spawn prompt's parameters.

---

## 2. Guideline Volume, Placement, and Adherence Quality

**Sub-question:** What is the empirical relationship between guideline volume, placement in context, and adherence quality — when does adding more guidelines degrade rather than improve results?

### The Degradation Curve

Empirical research identifies three distinct degradation patterns across model classes [OFFICIAL — "How Many Instructions Can LLMs Follow at Once?", OpenReview 2025]:

**Threshold decay** (reasoning models — o3, Gemini 2.5 Pro): Performance remains near-perfect through 100-150 instructions, then transitions to steeper degradation. At 500 instructions, accuracy drops to 62-69%.

**Linear decay** (Claude Sonnet, GPT-4.1): Steady, predictable accuracy decline across the full spectrum. No safe threshold, but no sudden cliff. Claude 3.7 Sonnet reaches 52.7% at 500 instructions.

**Exponential decay** (Claude Haiku, Llama): Rapid early degradation, stabilizing at accuracy floors of 7-15%.

[SUSPECT] The Gemini deep research claims a "19-rule ceiling" as an empirical threshold. This figure has no citation and contradicts the IFScale study's 100-150 instruction threshold. The AVFL validation flagged this as ACCURACY-001. **Use 100-150 as the planning reference for reasoning-class models; expect earlier degradation for Sonnet.**

### The Practical Zones

| Zone | Effective Instructions | Risk Level | Behavior |
|---|---|---|---|
| 1 | 1-50 | Low | High adherence across all frontier models |
| 2 | 50-150 | Moderate | Reasoning models hold; Sonnet shows 10-20% decline |
| 3 | 150-300 | High | All models show meaningful omission errors |
| 4 | 300+ | Breakdown | Uniform failure — adding more provides zero benefit |

[OFFICIAL] Anthropic's guidance: keep CLAUDE.md under 200 lines. The diagnostic: "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."

### Positional Effects

[OFFICIAL — Liu et al., TACL 2024] The "lost in the middle" effect: LLM accuracy drops 30+ percentage points when relevant information moves from the beginning to the middle of a long context. Performance partially recovers at the end. The cause is architectural — Rotary Position Embedding creates natural attention decay for mid-sequence tokens.

[PRAC — Chroma 2025] Adding even a single distractor document degrades performance. Semantically adjacent but irrelevant content (related-but-not-applicable rules) may be MORE harmful than completely unrelated noise, because the model attempts to reconcile relevance.

### Design Principles Derived from Evidence

1. **Budget by effective instruction count, not line count.** A 200-line file with 50 distinct behavioral rules is Zone 1. The same line count with 200 distinct rules is Zone 2-3. [INFERRED]
2. **Place critical rules first.** Attention sinks favor early context. Never-break prohibitions belong at the top. [OFFICIAL]
3. **Emphasis markers work but erode.** "NEVER", "IMPORTANT", "YOU MUST" improve individual rule adherence — but if everything is emphasized, the markers lose signal value. [OFFICIAL]
4. **Momentum working limit: 100 lines per always-loaded rules file.** This keeps effective instruction density in Zone 1-2 and leaves headroom for the agent definition body and spawn prompt. [PRAC — practitioner notes]

---

## 3. Structural Patterns for Dense Domain-Specific Guidelines

**Sub-question:** What structural patterns work best for delivering dense, domain-specific technical guidelines (library APIs, mandatory/forbidden patterns, antipattern lists) to specialist agents across any domain?

### The Three-Layer Progressive Disclosure Architecture

The dominant pattern across Claude Code, GitHub Copilot Agent, Cursor, and the AGENTS.md standard converges on three tiers [PRAC]:

**Layer 1 — Always-Loaded Rules (30-100 lines per file)**
Behavioral anchors: version pins, critical prohibitions, non-obvious environment quirks. Ask for each line: "Would removing this cause the agent to make mistakes?" If not, cut it. [OFFICIAL]

**Layer 2 — JIT Reference Documents (100-500 lines per domain)**
Dense domain content: library API patterns, testing conventions, antipattern checklists. Loaded on-demand. In Claude Code, this maps to skills or subdirectory CLAUDE.md files. Token economics justify this separation — Microsoft's agent-skills research reports 50-100 tokens per skill at metadata level, vs. 500-2,000 tokens for full skill bodies [PRAC].

**Layer 3 — Reference Files Loaded On Demand (unlimited)**
Full API specifications, comprehensive antipattern catalogs, worked code examples. The compose-skill exemplar uses 17 separate markdown guides plus 6 actual source code files from the androidx codebase [PRAC]. An agent searching for state management guidance loads that guide; it does not load all 23 files.

### Prohibition-First Ordering

The evidence does NOT support pure prohibition-first ordering. Instead, effective files use a three-tier boundary framework [PRAC]:

- **Never** — Hard constraints (security, breaking changes)
- **Ask First** — Judgment calls requiring confirmation
- **Always** — Permitted autonomously

Critical prohibitions belong near the top of their section (not buried in the middle), but the file should lead with tech stack anchors and version pins, then never-do constraints, then positive conventions [PRAC].

### Version Pinning

[OFFICIAL — Amazon Science 2024] Code LLMs achieve 93.66% accuracy on high-frequency APIs but only 38.58% on low-frequency ones. Libraries under active development contain many low-frequency APIs in training data. A 5-token version annotation (`Compose 1.7 — use AnimatedVisibility not deprecated AnimatedVisibleContent`) prevents pages of correction.

### Structural Formatting for Agent Consumption

[OFFICIAL] Structured formats outperform prose for compliance tasks:
- **Comparison tables** for antipatterns: Wrong column | Right column forces the agent to see both the violation and the correction
- **H2 anchors** as navigation layer: "Coroutine cancellation" not "Section 4" — agents grep for domain terms
- **One concept per H2** for self-contained sections that can be read without surrounding context
- **Worked code examples only for counterintuitive patterns** — standard conventions that match training data do not need examples. Human-curated examples justify their ~19% inference overhead; auto-generated examples show negative returns [PRAC]

---

## 4. Non-Dev Agent Guidelines: Delivery by Role Complexity

**Sub-question:** How do non-dev agents (QA, E2E, PM, SM) best consume their role-specific guidelines — and how does the optimal delivery mechanism differ by role complexity?

### Role Complexity Hierarchy

"Complexity" here refers to **guidelines density** — how dense and domain-specific the required guidelines are. This is distinct from task complexity. [PRAC]

| Role | Guidelines Density | Primary Content Type | Delivery Pattern |
|---|---|---|---|
| QA/Code-Review | Highest | Antipattern checklists, review methodology | Always-loaded in system prompt; preloaded skills for multi-language |
| E2E/Testing | High | BDD methodology, domain vocabulary, example library | System prompt for constraints; progressive-disclosure skills for reference |
| PM | Medium | Output templates, quality gates, domain vocabulary | Moderate system prompt; project-context skill for domain terms |
| SM | Lowest | Process rules, sprint health criteria | Compact system prompt; JIT sprint data at invocation |

### QA Agents — Densest Guidelines Package

QA agents perform adversarial checking against enumerable violation lists. Their information needs are: antipattern checklists, coding conventions, test quality criteria. Antipattern checklists must be **preloaded into the system prompt** rather than supplied as JIT prompts — QA review is a uniform task where the checklist defines the review criteria for the entire session [PRAC].

[PRAC] Developer-authored context files reduced output tokens by 16-20% and execution time by 20-28% compared to agents without such files. LLM-generated guideline files showed marginally negative effects (-3%) — QA guidelines must be human-curated, not auto-generated.

[PRAC] Semi-formal reasoning prompting techniques that force agents to state premises, trace execution paths, and derive conclusions improved code review accuracy to 93%. QA agents need behavioral-constraint-style instructions (step-by-step methodology), not informational reference docs.

Tool scope for QA: read-only tools enforce the domain boundary structurally — a QA agent that cannot write files cannot accidentally implement a fix instead of flagging it [PRAC].

### E2E Agents — Behavioral + Reference Split

E2E agents need BDD/Gherkin syntax knowledge, behavioral specificity constraints, domain vocabulary, and Gherkin antipatterns. The system prompt carries behavioral constraints ("Never use UI element IDs in scenario steps", "Each scenario tests one behavior"). Reference material (domain vocabulary, example library) belongs in progressively-disclosed skill files [PRAC].

[PRAC] Non-ambiguous prompts and separate agents for each distinct testing task prevented context contamination — suggesting one agent for Gherkin generation and another for execution, rather than a single E2E agent doing both.

### PM Agents — Format-Driven, Lower Density

PM agents produce human-reviewed artifacts, not executable code. Their guidelines focus on format, framing, and completeness rather than prohibitions. Domain vocabulary and project context should flow through a dedicated project-context reference file rather than consuming always-loaded context budget [PRAC].

### SM Agents — Lightest Profile

SM agents need the least dense guidelines. Agile process rules are stable and well-represented in training data. The primary customization is sprint-specific data (velocity, current goals, impediment log), which is volatile and should be JIT-injected at invocation — not preloaded [PRAC].

### The Constraint vs. Reference Dimension

| Information Type | Delivery Mechanism | Rationale |
|---|---|---|
| Behavioral constraints | Agent system prompt (always-loaded) | Must be active on every turn; omission is a defect |
| Antipattern checklists | System prompt or preloaded reference | Density justifies preload; never appropriate to skip |
| Reference docs | JIT-loaded files | High token cost; only needed for specific tasks |
| Sprint/session data | Spawn prompt injection | Volatile; stale data causes worse outputs than no data |
| Domain vocabulary | Separate reference file | Large and project-specific; should not occupy core context |

---

## 5. The Generic-Agent + Injected-Guidelines Pattern

**Sub-question:** What are the best architectural patterns for the generic-agent + injected-guidelines = specialized-agent model — how should project-specific guidelines be structured, stored, and delivered?

### The Composition Model

The pattern solves a fundamental tension: roles are stable (Dev, QA, E2E, PM, SM), but the knowledge each role needs varies radically by project. A "Dev" agent on a Kotlin Compose project needs Kotlin 2.3.20 APIs; the same "Dev" role on a Python FastAPI project needs entirely different knowledge. Embedding all possible knowledge in the agent definition produces bloat; embedding none means the agent operates on stale training data [PRAC].

The solution: **generic_agent + project_guidelines = specialized_agent**, composed at runtime.

### The Three-Layer Architecture for Momentum

**Layer 1 — Path-Scoped Rules (`.claude/rules/`, 30-80 lines per file)**

Short, high-signal files loaded on file access. One technology per file. Content: version pins, prohibition-format corrections, critical antipatterns. This is the primary mechanism for **technology specialization** in the main CLI session. A generic Dev agent working in `src/ui/HomeScreen.kt` automatically receives Compose UI guidelines without explicit injection [PRAC].

```
.claude/rules/
  kotest.md        (paths: ["**/*Test.kt", "**/*Spec.kt"])
  compose-ui.md    (paths: ["**/ui/**/*.kt", "**/*Screen.kt"])
  kmp-project.md   (paths: ["**/build.gradle.kts"])
```

**Layer 2 — Reference Docs (per-project storage, 100-300 lines)**

On-demand reference material containing worked examples and patterns the agent's training data gets wrong. Layer 1 rules point here: "For Navigation 3 patterns, read `docs/references/navigation3-patterns.md`." Zero context cost unless accessed [PRAC].

**Layer 3 — Skills (unlimited)**

Full procedural workflows for complex, multi-step tasks. Setup procedures, migration guides, domain-specific workflows. Loaded when explicitly invoked or when injected via spawn prompt [OFFICIAL].

### The Project-Level Override Pattern

The Claude Code authority hierarchy enables clean layered specialization [OFFICIAL]:

1. **Global base** (`~/.claude/CLAUDE.md`, `~/.claude/rules/`): Momentum practice defaults — commit conventions, workflow rules. All projects.
2. **Project layer** (`.claude/rules/*.md`, `./CLAUDE.md`): Stack-specific guidelines. This project, all agents.
3. **Story layer** (spawn prompt): Task-specific constraints. One-time, ephemeral.

Later-loaded files have higher effective priority. A project rule overrides a global default without modifying global rules [OFFICIAL].

### Delivery Decision Tree

1. Applies to all work on this project, regardless of role? --> CLAUDE.md
2. Applies only when working with specific file types? --> Path-scoped `.claude/rules/{technology}.md`
3. Role-specific (only Dev needs it, not QA)? --> Injected via spawn prompt `guidelines` parameter
4. Story-specific context? --> Spawn prompt direct injection
5. Requires worked examples the agent reads on demand? --> Layer 2 reference doc
6. Complex multi-step workflow? --> Layer 3 skill

### Key Tradeoff: Don't Over-Specialize

[PRAC] For tightly scoped domains with stable behavior, a single compressed system prompt may outperform a modular multi-layer architecture. Progressive loading is not automatically superior — match architecture complexity to actual domain complexity.

---

## 6. Preventing Guideline Bleed Between Co-Existing Roles

**Sub-question:** What patterns prevent guideline bleed between co-existing roles on the same project, where different agents need radically different knowledge domains?

### Why Bleed Happens

CLAUDE.md is injected as advisory context. The system wraps it with a reminder to "ignore instructions that aren't relevant to the current task." But this is heuristic, not structural. Compliance degrades with rule density. **You cannot prevent an agent from seeing a rule file — you can only influence whether it attends to it.** [PRAC]

The fundamental problem: as instruction count grows, the model does not just ignore new instructions — it starts ignoring ALL instructions uniformly. Every low-value rule dilutes compliance probability for every high-value rule in a zero-sum attention budget [PRAC].

### The Five-Layer Isolation Architecture

**Layer 1: Root CLAUDE.md — Cross-cutting project identity only.**
Under 100 lines. Include: repo structure map, commit format, tech stack names, one-line role registry. NO role-specific guidelines. [PRAC]

**Layer 2: Agent definition bodies — Self-contained role guidelines.**
Each agent file embeds all guidelines for its role. Include cross-cutting conventions verbatim — do not rely on inheritance. Include explicit negative-space declarations: "You do NOT write tests. Delegate to the QA agent." [PRAC]

**Layer 3: Subdirectory CLAUDE.md — On-demand domain knowledge.**
`src/compose-ui/CLAUDE.md` for Compose patterns. Loads only when an agent works in that directory. Provides ambient reinforcement for whichever agent visits [OFFICIAL].

**Layer 4: Path-scoped rules — File-pattern constraints.**
Mechanical constraints (file naming, import ordering) that trigger on file read. Accept the known limitation that these don't fire on Write operations [PRAC — GitHub #23478, closed NOT_PLANNED].

**Layer 5: Tool restrictions — Structural enforcement.**
QA agents get `tools: [Read, Grep, Glob, Bash]` — no Write/Edit. This prevents the most dangerous bleed failure mode: a QA agent implementing a fix instead of flagging it. Tool restrictions are the only hard enforcement mechanism — everything else is advisory [OFFICIAL].

### Documented Antipatterns

1. **All role guidelines in root CLAUDE.md.** Every agent loads the root file. A QA checklist in root CLAUDE.md is visible to every agent. This is the most common antipattern [PRAC].
2. **Relying on `paths:` frontmatter for role isolation.** Path scoping is activity-based, not identity-based. A QA agent working in `src/ui/` still loads Compose rules [PRAC].
3. **Expecting subagents to inherit project conventions.** The CLAUDE.md inheritance gap means subagents may receive none of the project rules. Teams discover this through incorrect behavior, not error messages [PRAC].
4. **Dense multi-role CLAUDE.md files.** A 500-line file covering all five roles causes Claude to follow none reliably [PRAC].

### Effective Isolation Patterns

- **Artifact-based handoffs** between agents: structured documents (JSON, Markdown) rather than conversation transcripts. Agent B sees Agent A's decisions, not its reasoning [PRAC].
- **Scoped tooling**: each role gets a minimal viable toolset. PM/Architect: Read, Glob, Grep. Developer: Edit, Write, Bash. QA: Read, Bash (for tests). [PRAC]
- **Negative instructions**: explicit "You are NOT responsible for X" statements in each role's prompt reinforce boundaries [PRAC].

---

## Cross-Cutting Themes

### Theme 1: Explicit Injection Beats Inheritance

Every research file, the AVFL validation, and the practitioner notes converge on the same finding: the only guaranteed delivery channel to a subagent is its system prompt body and the spawn prompt. CLAUDE.md inheritance is unreliable. Path-scoped rule inheritance is unreliable. The `skills:` frontmatter field is unavailable for Momentum's prompt-injected agents. **Explicit injection is the only safe architecture.** [PRAC, OFFICIAL]

### Theme 2: The Attention Budget is the Binding Constraint

Context windows are large (200K+ tokens), but effective attention is far smaller. The practical constraint is not "how much can I load" but "how much will the model reliably attend to." Every rule loaded into context competes with every other rule for attention. Path scoping and JIT loading are not optimizations — they are requirements for maintaining guideline adherence at any density above Zone 1 (50 instructions). [OFFICIAL, PRAC]

### Theme 3: Human-Curated Guidelines Outperform Generated Ones

[PRAC] LLM-generated AGENTS.md files offer no benefit and can marginally reduce success rates (~3%). The agent-guidelines skill can automate discovery and formatting, but the content must be human-authored or human-verified. Auto-generating "write clean code" guidelines is actively harmful — it consumes attention budget while providing zero behavioral signal.

### Theme 4: The Role-Technology Matrix

Guideline bleed has two dimensions: role bleed (QA seeing dev rules) and technology bleed (Compose rules loading during API work). These require different solutions. Role bleed is solved by **agent isolation** (separate system prompts, separate tool scopes). Technology bleed is solved by **path scoping** (`.claude/rules/` with `paths:` frontmatter). A complete architecture addresses both dimensions. [INFERRED]

### Theme 5: Structural Enforcement Over Advisory Rules

Guidelines are advisory. Tool restrictions are structural. Hooks are deterministic. For critical constraints, layer enforcement: the guideline says "prefer functional programming"; the PreToolUse hook blocks deletion of security files; the tool scope prevents the QA agent from writing source code. As agent autonomy increases, structural enforcement becomes more important relative to advisory guidelines. [PRAC]

---

## Recommendations for Momentum agent-guidelines Skill Redesign

This section provides specific, actionable changes for the `momentum:agent-guidelines` skill.

### R1: Keep `.claude/rules/` Generation AND Add Explicit Injection

**Do not replace the current `.claude/rules/` generation. Extend it.**

The skill must generate guidelines in **two forms**:

1. **`.claude/rules/` path-scoped files** — for the main CLI session. These provide ambient, technology-scoped guidelines that load on file access. They serve the orchestrator (Impetus, sprint-dev) and any main-session work. Keep the current behavior.

2. **Role-specific guideline reference files** — stored in a project location (see R4) and explicitly injected via the spawn prompt's `guidelines` parameter when spawning each role's agent. This closes the gap for QA, E2E, PM, SM, and skill-dev agents that currently receive no project-specific guidelines.

The `dev.md` agent already accepts a `guidelines` parameter and reads it explicitly in Step 1. Extend this pattern to ALL agent definitions: QA, E2E, PM, SM, and skill-dev must each accept and consume a `guidelines` parameter. The sprint-dev orchestrator must pass the appropriate guideline file path when spawning each role.

### R2: Handle 6+ Role Types with Role-Specific Guideline Files

Generate separate guideline files per role, not one monolithic file:

| Role | File | Content Focus | Max Lines |
|---|---|---|---|
| Dev (per-variant) | `guidelines-dev-{stack}.md` | Version pins, critical prohibitions, framework patterns | 80-100 |
| QA | `guidelines-qa.md` | Antipattern checklist, review methodology, output format | 80-100 |
| E2E | `guidelines-e2e.md` | BDD constraints, domain vocabulary pointer, Gherkin antipatterns | 60-80 |
| PM | `guidelines-pm.md` | Output templates, quality gates, domain vocabulary pointer | 40-60 |
| SM | `guidelines-sm.md` | Process deviations from standard Scrum (if any) | 20-40 |
| Skill-dev | `guidelines-skill-dev.md` | Skill structure standards, frontmatter conventions | 40-60 |

For projects with multiple dev stacks (Kotlin frontend + Python backend), generate separate dev guideline files per stack. The sprint-dev orchestrator selects the appropriate variant based on the story's `change_type` or technology scope.

### R3: Apply the Three-Layer Architecture Per Role

Each role's guidelines should use progressive disclosure:

**Always-loaded (in spawn prompt injection, max 100 lines):**
- Version pins for the role's relevant technologies
- Critical prohibitions in NEVER format
- Output format requirements
- Tool scope reminders (what this role does NOT do)

**JIT reference docs (loaded by agent when needed, 100-300 lines):**
- Worked code examples for counterintuitive patterns
- Comprehensive antipattern catalogs (for QA)
- Domain vocabulary glossary (for E2E, PM)
- Framework migration guides

**On-demand (full reference files, unlimited):**
- Full API specifications
- Upstream source code examples ("receipts")
- Architecture decision records

The always-loaded layer is the role-specific guideline file (R2). The JIT and on-demand layers are reference files that the always-loaded layer points to: "For Navigation 3 patterns, read `docs/references/navigation3-patterns.md`."

### R4: Store Guidelines Per-Project in a Consistent Location

```
{project}/
  .claude/
    rules/
      {technology}.md              # Layer 1 path-scoped rules (main CLI session)
    guidelines/
      guidelines-dev-{stack}.md    # Role-specific guideline files for injection
      guidelines-qa.md
      guidelines-e2e.md
      guidelines-pm.md
      guidelines-sm.md
    references/
      {technology}-patterns.md     # Layer 2 JIT reference docs
      {technology}-antipatterns.md
  CLAUDE.md                        # Cross-cutting project identity only (<100 lines)
```

The `.claude/guidelines/` directory is the new storage location for role-specific guideline files. These are NOT `.claude/rules/` files (they would load into the main session context). They are standalone reference files read explicitly by agents when injected via the `guidelines` parameter.

The `.claude/references/` directory stores Layer 2 content that guideline files point to. Agents read these on demand.

### R5: Handle the `paths:` Regression Safely

The `paths:` frontmatter regression (GitHub #16299) means path-scoped rules may load globally. The safe architecture:

1. **Continue generating path-scoped `.claude/rules/` files.** The architectural intent is sound and will work correctly when the bug is fixed.
2. **Keep each rules file under 80 lines.** If all rules load globally due to the bug, the total context cost is manageable (N files x 80 lines).
3. **Verify with `InstructionsLoaded` hook.** Add a validation step that uses the hook to confirm actual loading behavior. Log which files load at session start vs. on file access.
4. **Do not rely on path scoping for role isolation.** Use explicit injection (R1) as the primary role-scoping mechanism. Path scoping provides ambient technology reinforcement, not role boundaries.
5. **Accept the Write-operation limitation.** Path rules don't fire on file creation (GitHub #23478, closed NOT_PLANNED). For technologies where new file creation is common, include the most critical rules in the unconditional Layer 1 set.

### R6: Concrete Changes to the Skill Workflow

The redesigned `agent-guidelines` skill workflow should:

**Step 1 — Discover (keep, refine)**
Parallel subagents scan build files, existing rules, test configs, source patterns. **New:** also scan existing agent definition files to identify which roles are used in this project.

**Step 2 — Research (keep, refine)**
Focused web searches per detected technology. Prohibition format. Version-pinned. **New:** research should be scoped to the roles identified in Step 1 — QA-specific antipatterns only if a QA role exists.

**Step 3 — Consult (keep)**
Interactive decisions on scope, path patterns, content depth.

**Step 4 — Generate (restructure)**
Current: generates path-scoped Layer 1 rules only.
New: generates THREE artifact types in parallel:

- **Path-scoped `.claude/rules/` files** (30-80 lines each) — technology-specific, ambient loading
- **Role-specific `.claude/guidelines/` files** (40-100 lines each) — one per role, for explicit injection
- **Reference `.claude/references/` docs** (100-300 lines each) — JIT, pointed to by guideline files

Each role-specific guideline file must:
- Start with the role's relevant version pins
- Follow with critical prohibitions in NEVER format
- Include comparison tables for antipatterns (Wrong | Right)
- End with pointers to Layer 2 reference docs
- Stay under 100 lines total

**Step 5 — Validate (keep, extend)**
AVFL checkpoint on all artifacts. **New:** validate that each generated guideline file is under 100 lines and that role-specific content does not appear in `.claude/rules/` files (which would cause cross-role bleed in the main session).

**Step 6 — Wire (new)**
Update the sprint-dev orchestrator configuration to map role types to their guideline file paths. This ensures that when sprint-dev spawns a QA agent, it passes `guidelines: .claude/guidelines/guidelines-qa.md`. The skill should output a summary of which roles have guidelines and which guideline file maps to which agent.

### R7: Content Quality Standards for Generated Guidelines

Based on empirical evidence:

- **Don't document the inferable.** If the agent can read it from `build.gradle.kts`, don't repeat it. Guidelines correct what training data gets wrong [PRAC].
- **Pin versions explicitly.** Every library mentioned must include its version. Low-frequency APIs have ~40% hallucination rates without anchors [OFFICIAL].
- **Use comparison tables for antipatterns.** Wrong | Right format outperforms prose for compliance tasks [PRAC].
- **Include worked examples only for counterintuitive patterns.** Standard conventions that match training data do not need examples [OFFICIAL].
- **Human curation required.** The skill can draft, but a human must review. Auto-generated guidelines have negative ROI [PRAC].
- **Cap emphasis markers.** Use "NEVER" and "IMPORTANT" for at most 20% of rules. If everything is critical, nothing is [OFFICIAL].

---

## Known Limitations and Open Questions

### Confirmed Limitations

1. **Subagent CLAUDE.md inheritance is unreliable.** GitHub #29423 (open April 2026) documents concrete failures. GitHub #8395 (closed "not planned") confirms automatic rule propagation is not on the roadmap. [PRAC]

2. **`paths:` frontmatter has a regression.** GitHub #16299 (open February 2026) — rules load globally regardless of path patterns. [PRAC]

3. **Path rules don't fire on Write operations.** GitHub #23478 (closed NOT_PLANNED). Rules scoped to file patterns only activate on Read, not on file creation. [PRAC]

4. **`paths:` frontmatter does not work in user-level rules.** GitHub #21858 — only functions in project-level `.claude/rules/`. [PRAC]

5. **Subagents cannot spawn subagents.** Hierarchical delegation requires the orchestrator to remain the top-level spawner. [OFFICIAL]

6. **`skills:` frontmatter does not apply in Agent Teams.** Teammates load skills from project/user settings, not from the teammate definition's `skills:` field. [OFFICIAL]

7. **Subagents do not inherit PreToolUse hooks.** GitHub #27661. Hooks in `.claude/settings.json` do not propagate. [PRAC]

### Open Questions

1. **What is the actual CLAUDE.md inheritance behavior in CLI vs. SDK/Task contexts?** The research corpus contains contradictory claims. Definitive resolution requires controlled testing with the `InstructionsLoaded` hook across both contexts.

2. **When will the `paths:` regression be fixed?** The JIT loading architecture is sound and would significantly improve the guidelines model. Momentum should monitor GitHub #16299 and test periodically.

3. **Should guidelines be regenerated per sprint or persist across sprints?** Technology guidelines are relatively stable; sprint-specific constraints are volatile. The answer is likely: regenerate when the tech stack changes (new dependency, major version bump), not every sprint.

4. **How should guidelines handle multi-stack stories?** A story that touches both Kotlin frontend and Python backend needs guidelines from both stacks. The spawn prompt can inject multiple guideline files, but the combined volume must stay within Zone 1-2 (under 150 effective instructions).

5. **Can the `InstructionsLoaded` hook be used programmatically?** If so, the skill could verify at generation time that its output actually loads as expected — providing a feedback loop on the `paths:` regression.

---

## Sources

### Official Documentation

- Anthropic. "How Claude remembers your project (memory.md)." Claude Code Documentation, 2025-2026. [OFFICIAL]
- Anthropic. "Best Practices for Claude Code." Claude Code Documentation, 2025-2026. [OFFICIAL]
- Anthropic. "Create custom subagents." Claude Code Documentation. [OFFICIAL]
- Anthropic. "Orchestrate teams of Claude Code sessions." Claude Code Documentation. [OFFICIAL]
- Anthropic. "Effective context engineering for AI agents." Anthropic Engineering Blog, 2024. [OFFICIAL]
- Anthropic. "Modifying system prompts (SDK)." Claude Code Documentation. [OFFICIAL]
- Liu et al. "Lost in the Middle: How Language Models Use Long Contexts." TACL 2024. [OFFICIAL]
- "How Many Instructions Can LLMs Follow at Once?" OpenReview, 2025. [OFFICIAL]
- Amazon Science. "On Mitigating Code LLM Hallucinations with API Documentation." 2024. [OFFICIAL]
- JetBrains. "Write Modern Go Code With Junie and Claude Code." February 2026. [OFFICIAL]
- Google Developers Blog. "Developer's guide to multi-agent patterns in ADK." [OFFICIAL]
- CrewAI Docs. "Agents." [OFFICIAL]
- Cursor. "Rules Documentation." [OFFICIAL]

### Practitioner Sources

- GitHub Issue #8395: User-Level Agent Rules and Rule Propagation (closed NOT_PLANNED). [PRAC]
- GitHub Issue #16299: Path-scoped rules load globally (open February 2026). [PRAC]
- GitHub Issue #23478: Path rules not loaded on Write (closed NOT_PLANNED). [PRAC]
- GitHub Issue #21858: paths: frontmatter ignored in user-level rules. [PRAC]
- GitHub Issue #27661: Subagents should inherit parent session hooks. [PRAC]
- GitHub Issue #29423: Task subagents do not load project CLAUDE.md (open April 2026). [PRAC]
- GitHub Issue #32910: Subagents can discover project skills via filesystem. [PRAC]
- Chroma Research Team. "Context Rot: How Increasing Input Tokens Impacts LLM Performance." 2025. [PRAC]
- Osmani, A. "The Code Agent Orchestra." addyosmani.com. [PRAC]
- "How to Write a Great agents.md: Lessons from over 2,500 Repositories." github.blog. [PRAC]
- "How to Build Your AGENTS.md." augmentcode.com, 2026. [PRAC]
- compose-skill (aldefy/compose-skill). GitHub. [PRAC]
- awesome-android-agent-skills (new-silvermoon). GitHub. [PRAC]
- wshobson/agents: Multi-agent orchestration for Claude Code. GitHub. [PRAC]
- "How I Split Claude Code Into 12 Specialized Sub-Agents." dev.to. [PRAC]
- "Progressive Disclosure Pattern." deepwiki.com/microsoft/agent-skills. [PRAC]
- "Stop Stuffing Your System Prompt: Build Scalable Agent Skills in LangGraph." Medium, February 2026. [PRAC]
- "On the Impact of AGENTS.md Files on AI Coding Agent Efficiency." arxiv, January 2025. [PRAC]
- "On the Use of Agentic Coding Manifests: Empirical Study of Claude Code." arxiv, September 2025. [PRAC]
- Various Claude Code community guides: claudefa.st, paddo.dev, morphllm.com, buildcamp.io, shareuhack.com, eesel.ai, pubnub.com. [PRAC]

### Validation

- AVFL Validation Report, 2026-04-09. Initial score 65, post-fix score 92. Key flags: unsourced 19-rule ceiling, CLAUDE.md inheritance contradiction, four unverified Q1 2026 Gemini feature claims. [VALIDATED]

### Practitioner Input

- Steve Holmes, Practitioner Notes, 2026-04-09. Confirmed: Momentum agents are prompt-injected (not registered in .claude/agents/); dev.md has guidelines parameter, other roles lack it; design limit of 100 lines per always-loaded file; four Gemini Q1 2026 claims excluded as confabulations. [PRAC]
