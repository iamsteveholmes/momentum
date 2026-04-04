---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments: []
workflowType: 'research'
lastStep: 6
research_type: 'technical'
research_topic: 'Agent Guidelines Authoring for Claude Code'
research_goals: 'How to create effective agent guidelines documents for technologies poorly represented in training data, using KMP/CMP/Kotest as a concrete lens'
user_name: 'Steve'
date: '2026-04-03'
web_research_enabled: true
source_verification: true
---

# Agent Guidelines Authoring for Claude Code

## How to Create Effective Technology Reference Documents for AI Coding Agents — Especially for Technologies Poorly Represented in Training Data

**Date:** 2026-04-03
**Author:** Steve
**Research Type:** Technical

---

## Research Overview

This research investigates a foundational question in agentic engineering: **How do you provide high-quality, usable reference material to an AI coding agent for technologies where the model's training data is stale, incomplete, or absent?**

The investigation uses three fast-moving Kotlin ecosystem technologies as a concrete lens — Kotlin Multiplatform (KMP), Compose Multiplatform (CMP), and Kotest — all of which have undergone breaking changes between typical training data cutoffs and April 2026.

The research draws on six parallel investigation tracks: Claude Code's guideline loading mechanisms, community best practices for agent instructions, current KMP/CMP/Kotest state and breaking changes, and evidence-based anti-patterns. All claims are sourced from 2025-2026 publications with inline provenance.

---

## 1. The Instruction Budget: A Hard Constraint

The single most important finding across all research tracks is that **the number of instructions an LLM can reliably follow is finite and relatively small**. Every rule added competes with every other rule for compliance.

### The Science

The "Curse of Instructions" paper (October 2024) demonstrates that an LLM's probability of following ALL instructions drops exponentially as count rises: **P(all followed) = P(individual)^n**. At 10 simultaneous instructions, instruction-level chain-of-thought improved GPT-4o from 15% to 31% and Claude 3.5 Sonnet from 44% to 58%. ([Curse of Instructions — OpenReview](https://openreview.net/forum?id=R6q67CDBCH))

A separate study, "How Many Instructions Can LLMs Follow at Once?" (July 2025), scaled this to 500 keyword instructions via IFScale and found frontier models achieve only **68% accuracy**. Three degradation patterns were identified: threshold decay (reasoning models like o3, Gemini 2.5 Pro), linear decay (claude-sonnet-4, GPT-4.1), and exponential decay (GPT-4o, Llama-4-Scout). ([IFScale — arxiv](https://arxiv.org/html/2507.11538v1))

### The Practical Budget

For Claude Code specifically:

| Budget Item | Token/Instruction Cost | Source |
|---|---|---|
| System prompt overhead | ~14,300 tokens (HumanLayer estimates ~50 instruction slots) | [DEV.to: Token Tracing](https://dev.to/slima4/where-do-your-claude-code-tokens-actually-go-we-traced-every-single-one-423e) |
| MCP server overhead | 5,000-10,000 tokens per 20-tool server | [DEV.to: Token Tracing](https://dev.to/slima4/where-do-your-claude-code-tokens-actually-go-we-traced-every-single-one-423e) |
| Total pre-conversation overhead | ~30,000-40,000 tokens (estimated) | [MorphLLM: CLAUDE.md Examples](https://www.morphllm.com/claude-md-examples) |
| **Available user instruction slots** | **100-150 instructions** | [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |

This means a technology guideline document competes directly with project rules, coding conventions, and workflow instructions for those 100-150 slots.

### Recommendation

**Technology guidelines must be ruthlessly concise.** Every line must earn its place by answering: "Would removing this cause the agent to make a mistake it couldn't recover from by reading the code?" If not, cut it.

---

## 2. Claude Code's Guideline Loading Architecture

Understanding how Claude Code loads, prioritizes, and budgets guidelines is essential before writing them.

### Loading Hierarchy (Priority Order)

Files load from broadest to most specific scope. **Later-loaded files have higher effective priority** because they are the last thing Claude reads at each level.

| Priority | Location | Scope |
|---|---|---|
| 1 (lowest) | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Managed policy (IT/DevOps) |
| 2 | `~/.claude/CLAUDE.md` | Personal global |
| 3 | `~/.claude/rules/*.md` | Personal global rules |
| 4 | Ancestor `CLAUDE.md` files (root down to CWD) | Project hierarchy |
| 5 | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project instructions |
| 6 | `./.claude/rules/*.md` (no `paths` frontmatter) | Unconditional project rules |
| 7 | `./CLAUDE.local.md` | Personal project-local |
| 8 (highest) | `.claude/rules/*.md` with matching `paths:` | Conditional project rules |

Source: [Official docs: Memory](https://code.claude.com/docs/en/memory), [ClaudeFast: Rules Directory](https://claudefa.st/blog/guide/mechanics/rules-directory)

### Key Loading Behaviors

- **Subdirectory CLAUDE.md files load lazily** — only when Claude reads files in those directories. Not at launch. ([Official docs: Memory](https://code.claude.com/docs/en/memory))
- **Path-scoped rules** trigger when Claude reads files matching a glob pattern, not on every tool use. ([Official docs: Memory](https://code.claude.com/docs/en/memory))
- **CLAUDE.md survives `/compact`** — it is re-read from disk and re-injected fresh. The only content guaranteed to survive compaction. ([Official docs: Memory](https://code.claude.com/docs/en/memory))
- **HTML comments are stripped** — saves tokens. Comments inside code blocks are preserved. ([Official docs: Memory](https://code.claude.com/docs/en/memory))
- **`@path/to/file` import syntax** — maximum recursion depth of 5 hops. Enables modular composition. ([Official docs: Memory](https://code.claude.com/docs/en/memory))
- **Prompt caching** — CLAUDE.md content benefits from Anthropic's prompt caching on cache-read hits in subsequent turns (10x cheaper for Opus-tier pricing). ([DEV.to: Token Tracing](https://dev.to/slima4/where-do-your-claude-code-tokens-actually-go-we-traced-every-single-one-423e))

### Mechanism Selection Guide

| Mechanism | Enforcement | Load Timing | Best For |
|---|---|---|---|
| CLAUDE.md | Advisory (not deterministic) | Every session | Universal project conventions |
| `.claude/rules/` (unconditional) | Advisory (not deterministic) | Every session | Domain rules that always apply |
| `.claude/rules/` (path-scoped) | Advisory (not deterministic) | On file access | **Technology-specific guidelines** |
| Skills | On-demand | When invoked | Reusable workflows, deep domain knowledge |
| Hooks | Deterministic (100%) | On specific events | Must-happen enforcement |

Source: [Official docs: Best Practices](https://code.claude.com/docs/en/best-practices)

### Implication for Technology Guidelines

**Path-scoped rules are the ideal delivery mechanism for technology guidelines.** A `kotest-guidelines.md` with `paths: ["**/*Test.kt", "**/*Spec.kt"]` loads only when the agent is working with test files — zero cost when it isn't. A `compose-guidelines.md` with `paths: ["**/ui/**/*.kt", "**/*Screen.kt"]` loads only during UI work.

This keeps the always-loaded instruction budget free for universal rules while delivering dense technology knowledge exactly when needed.

---

## 3. What Makes Guidelines Effective: Evidence-Based Principles

### 3.1 Concise Rules Over Verbose Explanations

Anthropic's official guidance: target **under 200 lines per CLAUDE.md file**. "Longer files consume more context and reduce adherence." Community practitioners report effective files as short as **60 lines**. ([Official docs: Memory](https://code.claude.com/docs/en/memory), [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md))

An analysis of dozens of agent rules files found a typical 28-rule file contained only **3 essential rules** that actually changed behavior, 10 helpful rules, and 15 that were redundant or belonged in linters. After trimming to 11 rules, the file shrank 60% with no loss of function. ([DEV Community: Rules Analysis](https://dev.to/alexefimenko/i-analyzed-a-lot-of-ai-agent-rules-files-most-are-making-your-agent-worse-2fl))

### 3.2 Prohibitions Over Aspirations

"Never use `as any` to bypass type errors" outperforms "Write type-safe code" in every study. Explicit prohibitions with alternatives are the most reliably followed instruction format:

- "Never use `@AutoScan` — it was removed in Kotest 6.0. Register extensions explicitly via `ProjectConfig`."
- "Do not use `androidTarget {}` — it is deprecated. Use the `com.android.kotlin.multiplatform.library` plugin with `androidLibrary {}` (AGP < 8.12) or `android {}` (AGP 8.12+)."
- "Never use `createComposeRule()` in commonTest — it requires JUnit. Use `runComposeUiTest {}` instead."

Source: [Cursor Best Practices](https://cursor.com/blog/agent-best-practices), [Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules)

### 3.3 Exact Versions Prevent Hallucinated APIs

"AI models contain knowledge of multiple incompatible versions of the same library. Without version pins, they guess — and guess inconsistently." Include parenthetical notes answering follow-up questions: `Kotest 6.1.9 (not 5.x — the APIs are incompatible)`. ([Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules))

### 3.4 Examples Beat Prose — But Inline Sparingly

One clean code example conveys more than paragraphs of explanation. However, **do not inline code snippets that exist in the codebase** — they become outdated. Use `file:line` references to point Claude to authoritative source files instead. ([HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md))

For technology patterns that don't exist in the codebase yet (bootstrapping a new project), short inline examples are appropriate — they are the only source of truth.

### 3.5 Emphasis Markers Work

Adding "IMPORTANT", "CRITICAL", "YOU MUST", and ALL-CAPS "NEVER" improves adherence for critical rules. Use sparingly — if everything is critical, nothing is. ([Anthropic Best Practices](https://code.claude.com/docs/en/best-practices), [Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules))

### 3.6 Architecture Overviews Don't Help

The ETH Zurich SRI Lab study ("Evaluating AGENTS.md", early 2026) found that architectural overviews and repo structure documentation **did not reduce time spent locating relevant files**. Agents explore the filesystem regardless. LLM-generated context files actually **decreased** task success rate by 3% and increased costs by 20%+. Human-written files improved success by only 4% while increasing costs by 19%. ([InfoQ: Agents Context File](https://www.infoq.com/news/2026/03/agents-context-file-value-review/), [MarkTechPost](https://www.marktechpost.com/2026/02/25/new-eth-zurich-study-proves-your-ai-coding-agents-are-failing-because-your-agents-md-files-are-too-detailed/))

**Don't describe your project structure. Describe what the agent would get wrong without your help.**

### 3.7 Priority Ordering Matters

LLM attention is not uniform across context. Information at the beginning and end has the most impact; information in the middle gets de-prioritized ("lost in the middle" effect). Put critical rules first. ([DEV Community](https://dev.to/sachinchaurasiya/the-1-skill-most-developers-miss-when-using-ai-coding-agents-37h0))

Recommended ordering within a technology guideline file:
1. Version pins and critical prohibitions (what NOT to do)
2. Breaking changes from previous versions (what the agent thinks it knows but is wrong)
3. Correct patterns with minimal examples
4. Setup/configuration specifics

---

## 4. Anti-Patterns: What Doesn't Work

### 4.1 Context Rot

Research from Chroma tested 18 LLMs and found performance degrades non-uniformly as input length grows. **Claude models showed the largest gap** between focused (~300 token) and full (~113K token) prompts. Counterintuitively, **logically structured content performed worse than shuffled content** — models over-indexed on structure and got confused by plausible-but-wrong nearby content. ([Chroma Research: Context Rot](https://www.trychroma.com/research/context-rot))

Practitioner reports suggest context rot becomes measurable around **20-30 conversation turns** and accelerates beyond **40 turns**. ([MindStudio](https://www.mindstudio.ai/blog/context-rot-ai-coding-agents-explained) — note: these are practitioner heuristics, not findings from the Chroma study itself)

**Implication:** Technology guidelines that load on every session, even when irrelevant, accelerate context rot. Path-scoped loading is not optional — it's essential.

### 4.2 The Six Named Anti-Patterns

From BSWEN's analysis of real-world agent usage. While some of these concern session conduct rather than guidelines content directly, they compound the problems that well-structured guidelines aim to solve:

1. **The Kitchen Sink Session** — mixing requirements, architecture, code, debugging, and review in one conversation
2. **The Abstract Principle Dump** — "clean code," "DRY," "SOLID" without concrete examples
3. **Pushing Through Context Decay** — continuing past 80%+ context window fill
4. **The Mega-Session** — attempting exploration, planning, implementation, debugging, and review in one session
5. **Log Vomit** — pasting 2000+ lines of output when the actual error is in 50 lines
6. **The Verbal Repetition Loop** — restating constraints every session instead of persisting them in rules files

Source: [BSWEN: AI Coding Anti-Patterns](https://docs.bswen.com/blog/2026-03-25-ai-coding-anti-patterns/)

### 4.3 Contradictory Instructions

"Use server components by default" combined with "Always wrap data fetching in useEffect hooks" are fundamentally incompatible. The agent produces inconsistent, broken output. When writing technology guidelines, **audit for internal contradictions** — especially between generic rules and technology-specific rules. ([Cursor Best Practices](https://cursor.com/blog/agent-best-practices))

### 4.4 Documenting the Inferable

Agents can read your `build.gradle.kts`, your `package.json`, your `tsconfig.json`. Rules that restate what's already in configuration files are pure waste. Technology guidelines should cover **what the agent would get wrong despite having access to the code** — stale API knowledge, deprecated patterns it might reach for, version-specific gotchas. ([Stack Overflow Blog](https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/))

---

## 5. The Recommended Architecture: A Layered Approach

Based on the evidence, the optimal structure for technology guidelines is a **three-layer architecture**:

### Layer 1: Concise Rules (`.claude/rules/`, path-scoped)

Short, high-signal files that load only when relevant. These are the **prohibitions and corrections** — what the agent would get wrong from stale training data.

**Target: 30-80 lines per file. One technology per file.**

Example structure:
```
.claude/rules/
  kotest.md          (paths: ["**/*Test.kt", "**/*Spec.kt"])
  compose-ui.md      (paths: ["**/ui/**/*.kt", "**/*Screen.kt", "**/*Composable.kt"])
  kmp-project.md     (paths: ["**/build.gradle.kts", "**/settings.gradle.kts"])
```

Content format for each file:
```markdown
---
paths:
  - "**/*Test.kt"
  - "**/*Spec.kt"
---
# Kotest 6.1 Guidelines

**Version:** Kotest 6.1.9, Kotlin 2.3.20

## CRITICAL — Breaking Changes from 5.x

- NEVER use `@AutoScan` — removed in 6.0. Register extensions via ProjectConfig.
- NEVER use `override fun extensions()` — changed to `override val extensions`.
- NEVER use `InstancePerTest` or `InstancePerLeaf` — deprecated. Use `InstancePerRoot`.
- NEVER use `kotest-framework-datatest` dependency — merged into core.
- ProjectConfig MUST be at `io.kotest.provided.ProjectConfig`.

## Test Style Conventions

- Use `FunSpec` for unit tests, `BehaviorSpec` for acceptance tests.
- Use `shouldBe` infix assertions. Use `assertSoftly` for multi-property checks.
- Use `withTests` (FunSpec) or `withData` or style-specific `withXXX` variants (BehaviorSpec) for data-driven tests.

## KMP Setup

- JVM: `kotest-runner-junit5` + `useJUnitPlatform()`
- Non-JVM: `kotest-framework-engine` + KSP plugin + `io.kotest` Gradle plugin
```

### Layer 2: Reference Examples (Project docs or dedicated reference files)

Longer files containing **worked examples** that the agent reads on demand via `@` imports or when Claude accesses the directory. These exist in the project's `docs/` or a dedicated `references/` directory.

**Target: 100-300 lines. Pattern-focused, not tutorial-style.**

These are referenced from Layer 1 rules: "For Kotest TDD patterns, read `docs/references/kotest-tdd-patterns.md`."

Content: concrete code examples showing the correct way to do things that the agent's training data gets wrong — specifically for patterns not yet present in the codebase or that the agent cannot infer from existing files (per Section 3.4). No prose explanations — just annotated code blocks with brief context.

### Layer 3: Skills (`.claude/skills/`)

For complex, multi-step workflows like project setup, migration, or architectural patterns. Skills load on demand, have their own context, and can include extensive procedural knowledge without polluting the always-loaded context.

**Target: Unlimited length (loads only when invoked).**

Example: A `compose-multiplatform-setup` skill that walks through creating a new CMP project with the correct April 2026 configuration, including AGP 9 migration, Navigation 3 setup, and Kotest integration.

### Why Three Layers?

| Layer | Budget Impact | When Loaded | What It Contains |
|---|---|---|---|
| Rules | Low (30-80 lines, path-scoped) | On file access | Prohibitions, version pins, corrections |
| References | Zero (read on demand) | When agent chooses to read | Worked examples, patterns |
| Skills | Zero (invoked explicitly) | On invocation | Complex workflows, setup procedures |

This architecture keeps the always-loaded instruction budget (~100-150 slots) free for universal project rules while delivering dense technology knowledge exactly when the agent needs it.

---

## 6. Case Study: What an Agent Gets Wrong in KMP/CMP/Kotest (April 2026)

To make the guidelines architecture concrete, here is what an agent with training data from 2024 or early 2025 would get wrong across the three example technologies. This is the exact content that belongs in Layer 1 rules files.

### 6.1 Kotlin Multiplatform — Stale Knowledge

| What the Agent Thinks | What's Actually True (April 2026) | Source |
|---|---|---|
| `androidTarget {}` is the KMP Android target DSL | Deprecated. Switch to `com.android.kotlin.multiplatform.library` plugin with `androidLibrary {}` block (AGP 9.0+). Note: `iosX64` is being kept at tier 3; `macosX64`/`tvosX64`/`watchosX64` are deprecated for removal. | [AGP 9 migration](https://kotlinlang.org/docs/multiplatform/multiplatform-project-agp-9-migration.html) |
| `ios()`, `watchos()`, `tvos()` shortcuts exist | Removed in Kotlin 2.2.0. Declare targets individually: `iosArm64()`, `iosSimulatorArm64()` | [Compatibility guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html) |
| `withJava()` is needed for Java interop | Deprecated. Java source sets created by default since 2.1.20 | [What's new in 2.3.0](https://kotlinlang.org/docs/whatsnew23.html) |
| `fromPreset()` API works | Removed in Kotlin 2.2.0 | [Compatibility guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html) |
| x86_64 Apple targets are supported | `macosX64`/`tvosX64`/`watchosX64` deprecated for removal; `iosX64` kept at tier-3 | [What's new in 2.3.0](https://kotlinlang.org/docs/whatsnew23.html) |
| Minimum iOS is 12.0 | Raised to 14.0 (tvOS 14.0, watchOS 7.0) | [What's new in 2.3.0](https://kotlinlang.org/docs/whatsnew23.html) |
| Compose compiler is a separate artifact | Built into Kotlin compiler since Kotlin 2.0 | [CMP 1.10.0 blog](https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/) |
| Current Kotlin is 2.0.x or 2.1.x | Current stable is **Kotlin 2.3.20** (March 16, 2026) | [Kotlin releases](https://kotlinlang.org/docs/releases.html) |

### 6.2 Compose Multiplatform — Stale Knowledge

| What the Agent Thinks | What's Actually True (April 2026) | Source |
|---|---|---|
| iOS support is Alpha/Beta | **Stable since May 2025** (CMP 1.8.0) | [CMP 1.8.0 blog](https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/) |
| Web support is Alpha | **Beta since Sep 2025** (CMP 1.9.0) | [CMP 1.9.0 blog](https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/) |
| Separate `@Preview` per platform | **Unified `@Preview`** in commonMain (CMP 1.10+) | [CMP 1.10.0 blog](https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/) |
| Navigation uses Navigation 2 only | **Navigation 3** available on all CMP platforms (CMP 1.10+); uses `NavKey` interface, not routes | [Navigation 3 docs](https://kotlinlang.org/docs/multiplatform/compose-navigation-3.html) |
| Hot Reload is experimental/nonexistent | **Stable 1.0**, bundled by default for JVM/Desktop only (CMP 1.10+) | [Hot Reload docs](https://kotlinlang.org/docs/multiplatform/compose-hot-reload.html) |
| UI testing is desktop-only | Common `runComposeUiTest` works across all targets | [CMP testing docs](https://kotlinlang.org/docs/multiplatform/compose-test.html) |
| Use `createComposeRule()` for tests | Only on desktop/JUnit. Use `runComposeUiTest {}` in commonTest | [CMP testing docs](https://kotlinlang.org/docs/multiplatform/compose-test.html) |
| Web target is `jsMain` with DOM API | **`wasmJsMain`** with Wasm as primary | [CMP compatibility](https://kotlinlang.org/docs/multiplatform/compose-compatibility-and-versioning.html) |
| Current CMP version is 1.5.x-1.7.x | Current stable is **CMP 1.10.3** (1.10.0 released January 2026, 1.10.3 patch February 2026) | [GitHub releases](https://github.com/JetBrains/compose-multiplatform/releases) |

### 6.3 Kotest — Stale Knowledge

| What the Agent Thinks | What's Actually True (April 2026) | Source |
|---|---|---|
| `@AutoScan` discovers extensions | Removed in 6.0. Register explicitly via ProjectConfig | [Kotest 6.0 release](https://kotest.io/docs/next/release6/) |
| `kotest-framework-datatest` is a separate dep | Merged into core framework | [Kotest 6.0 release](https://kotest.io/docs/next/release6/) |
| `override fun extensions()` | Changed to `override val extensions` | [Kotest 6.0 release](https://kotest.io/docs/next/release6/) |
| Compiler plugin for multiplatform | Replaced with KSP | [Setup docs](https://kotest.io/docs/framework/project-setup.html) |
| `InstancePerTest` / `InstancePerLeaf` | Deprecated. Use `InstancePerRoot` | [Kotest 6.0 release](https://kotest.io/docs/next/release6/) |
| ProjectConfig auto-discovered anywhere | Must be at `io.kotest.provided.ProjectConfig` | [Kotest 6.0 release](https://kotest.io/docs/next/release6/) |
| Current Kotest is 5.x | Current stable is **Kotest 6.1.9** (March 25, 2026) | [GitHub releases](https://github.com/kotest/kotest/releases) |
| JDK 8 is supported | Requires JDK 11 minimum, Kotlin 2.2 minimum | [Kotest 6.0 release](https://kotest.io/docs/next/release6/) |

---

## 7. Worked Example: Technology Guidelines Set (Layer 1 Complete, Layers 2-3 Described)

Applying all the principles from this research, here is what a complete guidelines set for a KMP + CMP + Kotest project would look like in April 2026.

### 7.1 Path-Scoped Rule: `.claude/rules/kmp-project.md`

```markdown
---
paths:
  - "**/build.gradle.kts"
  - "**/settings.gradle.kts"
  - "**/gradle/**"
---
# Kotlin Multiplatform Project Guidelines

**Versions:** Kotlin 2.3.20, CMP 1.10.3, AGP 9.0.28+, Gradle 9.x

## CRITICAL — Do NOT Use Deprecated APIs

- NEVER use `androidTarget {}` — switch to `com.android.kotlin.multiplatform.library` plugin with `androidLibrary {}` (AGP < 8.12) or `android {}` (AGP 8.12+)
- NEVER use `ios()`, `watchos()`, `tvos()` shortcuts — removed in Kotlin 2.2.0. Declare targets individually: `iosArm64()`, `iosSimulatorArm64()`
- NEVER use `withJava()` — Java source sets are created by default since 2.1.20
- NEVER use `fromPreset()` — API was removed in Kotlin 2.2.0
- NEVER target `macosX64`, `tvosX64`, `watchosX64` — deprecated for removal. `iosX64` remains at tier-3 but prefer arm64
- The Compose compiler is built into Kotlin since 2.0 — do NOT add a separate compose compiler dependency

## Version Compatibility

- Kotlin 2.3.20 requires Gradle 7.6.3-9.3.0, AGP 8.2.2-9.0.0, Xcode 16.x
- CMP 1.10.x requires Kotlin 2.1.20+ minimum
- Kotlin/Wasm requires Kotlin 2.3.10+
- Minimum iOS/tvOS deployment target: 14.0, watchOS: 7.0
```

### 7.2 Path-Scoped Rule: `.claude/rules/compose-ui.md`

```markdown
---
paths:
  - "**/ui/**/*.kt"
  - "**/*Screen.kt"
  - "**/*Component.kt"
  - "**/*Composable*.kt"
---
# Compose Multiplatform UI Guidelines

**Version:** CMP 1.10.3 — iOS is Stable, Web is Beta

## Navigation

Use Navigation 3 (NOT Navigation 2):
- Manage back stack directly via `SnapshotStateList`
- Use `NavDisplay` composable and `rememberNavBackStack()`
- Back stack keys implement `NavKey` and must be `@Serializable`
- Non-JVM platforms require polymorphic serialization via `SavedStateConfiguration`

## Preview

Use the unified `@Preview` annotation from `androidx.compose.ui.tooling.preview.Preview` in commonMain.
Do NOT use the deprecated `org.jetbrains.compose.ui.tooling.preview.Preview`.

## Platform Notes

- iOS: Stable, production-ready. Use native text input opt-in for `BasicTextField` if IME issues arise.
- Web: Beta. Target is `wasmJsMain` (NOT `jsMain`). JS compatibility mode available as fallback.
- Desktop/JVM: Compose Hot Reload is stable and enabled by default (JVM only — not available on iOS, Android, or Web).
```

### 7.3 Path-Scoped Rule: `.claude/rules/kotest.md`

````markdown
---
paths:
  - "**/*Test.kt"
  - "**/*Spec.kt"
  - "**/*Tests.kt"
  - "**/test/**/*.kt"
  - "**/commonTest/**/*.kt"
---
# Kotest 6.1 Guidelines

**Version:** Kotest 6.1.9, requires Kotlin 2.2+, JDK 11+

## CRITICAL — Breaking Changes from 5.x

- NEVER use `@AutoScan` — removed. Register extensions via ProjectConfig at `io.kotest.provided.ProjectConfig`
- NEVER use `override fun extensions()` — changed to `override val extensions`
- NEVER use `InstancePerTest` or `InstancePerLeaf` — deprecated, use `InstancePerRoot`
- NEVER add `kotest-framework-datatest` dependency — merged into core
- NEVER use the old compiler plugin — replaced by KSP for multiplatform

## Dependencies

- JVM: `kotest-runner-junit5` + `useJUnitPlatform()`
- Non-JVM (KMP): `kotest-framework-engine` + KSP plugin + `io.kotest` Gradle plugin
- Both: `kotest-assertions-core` for matchers

## Test Style

- Use `FunSpec` for unit tests, `BehaviorSpec` for acceptance/BDD tests
- Use `shouldBe` infix assertions, `assertSoftly` for multi-property checks
- Use `withTests` (FunSpec) or `withData` or style-specific `withXXX` variants (BehaviorSpec) for data-driven tests
- Every test body is a suspend function by default — no `runTest` wrapper needed
- Enable `coroutineTestScope = true` for virtual time control

## CMP UI Testing

Use `runComposeUiTest {}` in commonTest (NOT `createComposeRule()` which is JUnit-only):

```kotlin
@OptIn(ExperimentalTestApi::class)
class MyScreenTest {
    @Test
    fun buttonUpdatesText() = runComposeUiTest {
        setContent { MyScreen() }
        onNodeWithText("Click me").performClick()
        onNodeWithText("Clicked!").assertExists()
    }
}
```

Add to commonTest dependencies:

```kotlin
@OptIn(org.jetbrains.compose.ExperimentalComposeLibrary::class)
implementation(compose.uiTest)
```
````

### 7.4 Reference Document: `docs/references/kotest-tdd-patterns.md`

This would be a longer document (100-300 lines) containing worked examples of TDD patterns with Kotest — FunSpec unit test cycles, BehaviorSpec acceptance tests, property-based testing, data-driven testing. The agent reads it on demand when referenced from the rules file or when working in the test directory.

### 7.5 Skill: `compose-multiplatform-setup`

A skill for bootstrapping a new CMP project with the correct April 2026 configuration. Contains step-by-step procedural knowledge: Gradle configuration, AGP 9 setup, source set structure, Kotest integration, Navigation 3 wiring. Loads only when invoked, unlimited length.

---

## 8. Maintenance and Staleness Management

### The Core Problem

Fast-moving technologies make guidelines stale quickly. Kotlin has a 6-month language release cadence (2.x.0 every June/December). CMP releases every 3-4 months. Kotest iterates rapidly within major versions.

### Strategies

**1. Version-pin everything.** Every guideline file should declare exact versions at the top. When versions change, the file is visibly outdated and can be updated systematically.

**2. Date-stamp files.** Include a `Last verified:` date. Establish a review cadence (e.g., quarterly, or on every major version bump).

**3. Separate volatile from stable.** Version numbers and API specifics change frequently. Architectural principles ("use FunSpec for unit tests") are more stable. Structure files so the volatile parts are easy to update without rewriting the whole file.

**4. Use the agent to check itself.** When starting a session, an agent can be instructed: "Before writing Gradle configuration, verify the current Kotlin and CMP versions by checking `gradle/libs.versions.toml`." This turns the project's own version catalog into the source of truth rather than the guidelines file.

**5. Iterative refinement.** Start with 5 rules. Add one per week when you observe a repeated mistake. Prune monthly. A mature project's guidelines should get shorter over time, not longer. ([Medium: CLAUDE.md That Works](https://medium.com/@martin_50671/how-to-write-a-claude-md-that-actually-works-76a184042444))

**6. Diagnostic for ignored rules.** If Claude ignores a rule from a guidelines file, paste it directly into the conversation. If Claude follows it there but not from the file, the problem is delivery-layer (file too long, rule buried). If Claude still ignores it, rewrite the rule to be more specific. ([ShareUHack](https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026))

---

## 9. Cross-Tool Applicability

While this research focuses on Claude Code, the principles extend to other AI coding agents:

| Principle | Claude Code | Cursor | GitHub Copilot | Windsurf |
|---|---|---|---|---|
| Concise rules file | CLAUDE.md (<200 lines) | `.cursorrules` | `.github/copilot-instructions.md` | `.windsurfrules` |
| Path-scoped rules | `.claude/rules/` with `paths:` | Not natively supported | Not natively supported | Not natively supported |
| On-demand reference | `@import` + lazy subdirectory loading | Manual `@file` references | N/A | Manual references |
| Deterministic hooks | Pre/Post tool hooks | N/A | N/A | N/A |
| Skills/workflows | `.claude/skills/` | N/A | N/A | N/A |

Claude Code's path-scoped rules and layered loading architecture provide the most granular control. For other tools, the same principles apply but must be compressed into a single flat file — making conciseness even more critical.

---

## 10. Summary: The Guidelines for Writing Guidelines

### The Golden Rules

1. **Budget is finite.** You have ~100-150 effective instruction slots. Every technology guideline line competes with every project rule line.

2. **Correct stale knowledge, don't teach from scratch.** Guidelines should fix what the agent gets wrong, not explain what it already knows. "NEVER use `@AutoScan`" is worth 100x more than "Kotest is a testing framework for Kotlin."

3. **Use prohibitions, not aspirations.** "NEVER use X — use Y instead" is the single most effective instruction format.

4. **Path-scope everything possible.** Technology guidelines should load only when the agent is working with relevant files. Zero cost when irrelevant.

5. **Three layers: Rules (concise, scoped) -> References (examples, on-demand) -> Skills (workflows, invoked).** Keep the always-loaded budget clean.

6. **Pin versions explicitly.** Eliminate the "which version does the agent think it knows?" ambiguity.

7. **Put critical prohibitions first.** The beginning and end of a document get the most attention. Bury nothing important in the middle.

8. **Don't document the inferable.** If the agent can learn it by reading the code, don't waste a rule on it.

9. **Date and version-stamp everything.** Guidelines without dates are guidelines that rot silently.

10. **Start small, grow from mistakes.** Begin with 5 rules. Add one when you observe a repeated mistake. Prune monthly.

### The Mental Model

Write technology guidelines as if briefing **an incredibly capable engineer who has read every programming book published before 2025 but hasn't seen any release notes since then**. They know all the patterns but they're wrong about which APIs exist, which are deprecated, and what the current best practice is. Your job is to give them the delta — quickly, precisely, and with no filler.

---

## Sources

### Claude Code Mechanisms
- [Official: How Claude Remembers Your Project](https://code.claude.com/docs/en/memory)
- [Official: Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Official: Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Anthropic Blog: Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [ClaudeFast: Rules Directory](https://claudefa.st/blog/guide/mechanics/rules-directory)
- [ClaudeFast: 1M Context Window](https://claudefa.st/blog/guide/mechanics/1m-context-ga)
- [DEV.to: Where Do Your Claude Code Tokens Actually Go](https://dev.to/slima4/where-do-your-claude-code-tokens-actually-go-we-traced-every-single-one-423e)
- [MorphLLM: CLAUDE.md Examples and Best Practices 2026](https://www.morphllm.com/claude-md-examples)
- [How Anthropic Teams Use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)

### Guidelines Best Practices
- [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Medium: Stop Stuffing Everything into One CLAUDE.md](https://medium.com/@richardhightower/claude-code-rules-stop-stuffing-everything-into-one-claude-md-0b3732bca433)
- [Agent Rules Builder: How to Write AI Coding Rules](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules)
- [Builder.io: How to Write a Good CLAUDE.md File](https://www.builder.io/blog/claude-md-guide)
- [Medium: How to Write a CLAUDE.md That Actually Works](https://medium.com/@martin_50671/how-to-write-a-claude-md-that-actually-works-76a184042444)
- [Ran Isenberg: Claude Code Best Practices](https://ranthebuilder.cloud/blog/claude-code-best-practices-lessons-from-real-projects/)
- [Addy Osmani: How to Write a Good Spec for AI Agents](https://addyosmani.com/blog/good-spec/)
- [GitHub Blog: Spec-Driven Development](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/)

### Academic Research
- [Curse of Instructions (OpenReview)](https://openreview.net/forum?id=R6q67CDBCH)
- [IFScale: How Many Instructions Can LLMs Follow? (arxiv)](https://arxiv.org/html/2507.11538v1)
- [ETH Zurich SRI Lab: "Evaluating AGENTS.md" — Context File Value Reassessed (InfoQ)](https://www.infoq.com/news/2026/03/agents-context-file-value-review/)
- [MarkTechPost: ETH Zurich Study on AGENTS.md Files](https://www.marktechpost.com/2026/02/25/new-eth-zurich-study-proves-your-ai-coding-agents-are-failing-because-your-agents-md-files-are-too-detailed/)
- [Context Rot Research (Chroma)](https://www.trychroma.com/research/context-rot)
- [Context Rot Explained (MindStudio)](https://www.mindstudio.ai/blog/context-rot-ai-coding-agents-explained)

### Anti-Patterns
- [DEV Community: The #1 Skill Most Developers Miss When Using AI Coding Agents](https://dev.to/sachinchaurasiya/the-1-skill-most-developers-miss-when-using-ai-coding-agents-37h0)
- [DEV Community: I Analyzed Dozens of AI Agent Rules Files](https://dev.to/alexefimenko/i-analyzed-a-lot-of-ai-agent-rules-files-most-are-making-your-agent-worse-2fl)
- [BSWEN: AI Coding Anti-Patterns](https://docs.bswen.com/blog/2026-03-25-ai-coding-anti-patterns/)
- [Stack Overflow Blog: Coding Guidelines for AI Agents](https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/)
- [Cursor: Best Practices for Coding with Agents](https://cursor.com/blog/agent-best-practices)
- [ShareUHack: Claude Code Setup Guide 2026](https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026)

### Kotlin Multiplatform (April 2026)
- [Kotlin Releases](https://kotlinlang.org/docs/releases.html)
- [What's New in Kotlin 2.3.0](https://kotlinlang.org/docs/whatsnew23.html)
- [Kotlin 2.3.20 Released](https://blog.jetbrains.com/kotlin/2026/03/kotlin-2-3-20-released/)
- [KMP Compatibility Guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html)
- [AGP 9 Migration Guide](https://kotlinlang.org/docs/multiplatform/multiplatform-project-agp-9-migration.html)
- [KMP Quickstart](https://kotlinlang.org/docs/multiplatform/quickstart.html)

### Compose Multiplatform (April 2026)
- [Compose Multiplatform 1.10.0 Blog](https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/)
- [CMP 1.8.0: iOS Stable](https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/)
- [CMP 1.9.0: Web Beta](https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/)
- [Navigation 3 Docs](https://kotlinlang.org/docs/multiplatform/compose-navigation-3.html)
- [Compose Hot Reload Docs](https://kotlinlang.org/docs/multiplatform/compose-hot-reload.html)
- [CMP Testing Docs](https://kotlinlang.org/docs/multiplatform/compose-test.html)
- [CMP Compatibility and Versioning](https://kotlinlang.org/docs/multiplatform/compose-compatibility-and-versioning.html)
- [Compose Multiplatform GitHub Releases](https://github.com/JetBrains/compose-multiplatform/releases)

### Kotest (April 2026)
- [Kotest GitHub Releases](https://github.com/kotest/kotest/releases)
- [Kotest 6.0 Release Notes](https://kotest.io/docs/next/release6/)
- [Kotest Setup / Project Configuration](https://kotest.io/docs/framework/project-setup.html)
- [Kotest Testing Styles](https://kotest.io/docs/framework/testing-styles.html)
- [Kotest Core Matchers](https://kotest.io/docs/assertions/core-matchers.html)
- [Kotest Property-Based Testing](https://kotest.io/docs/proptest/property-based-testing.html)
- [Kotest Data-Driven Testing](https://kotest.io/docs/framework/datatesting/data-driven-testing.html)
- [Setting up Kotest on KMP](https://alyssoncirilo.com/blog/kotest-kmp-setup/)
- [Kotest Coroutine Test Dispatcher](https://kotest.io/docs/framework/coroutines/test-coroutine-dispatcher.html)
