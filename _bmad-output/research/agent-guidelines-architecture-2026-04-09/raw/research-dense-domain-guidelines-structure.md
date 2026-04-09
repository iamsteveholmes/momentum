---
content_origin: claude-code-subagent
date: 2026-04-09
sub_question: "What structural patterns work best for delivering dense, domain-specific technical guidelines (library APIs, mandatory/forbidden patterns, antipattern lists) to specialist agents across any domain?"
topic: "Agent-specific guidelines architecture in Claude Code"
---

# Structural Patterns for Dense Domain-Specific Technical Guidelines in Specialist Agents

## Executive Summary

Delivering hundreds of highly specific guidelines to specialist agents — library APIs, forbidden patterns, antipattern checklists — is a solved problem in practice, but the solution is not a single large rules file. The evidence consistently points to a three-layer progressive disclosure architecture: always-loaded rules (concise, high-signal), JIT reference documents loaded when the domain is active, and skill-level workflows. Within each layer, specific structural choices — prohibition prominence, version pinning, H2 anchors for grep-ability, and worked code examples — measurably affect whether agents follow guidelines or ignore them.

---

## The Three-Layer Architecture: How It Works in Practice

The dominant pattern across Claude Code, GitHub Copilot Agent, Cursor, and the emerging AGENTS.md standard is a three-tier progressive disclosure model. This was formalized most explicitly in the Microsoft agent-skills documentation and corroborated by Anthropic's own Claude Code best practices documentation.

**Tier 1 — Always-Loaded Rules (30-100 lines)**

The always-loaded layer contains only what must be true in every context: build commands, the tech stack with exact versions, critical forbidden patterns, and non-obvious environmental quirks. Anthropic's official best-practices documentation is explicit: keep CLAUDE.md under 200 lines, and for each line ask "Would removing this cause Claude to make mistakes?" If not, cut it. The documentation identifies "the over-specified CLAUDE.md" as an antipattern by name: "If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."

Research from ETH Zurich cited in the Augment Code guide found that architectural overviews in agent instruction files "do not reduce navigation time" and actually increase inference costs. The implication: Tier 1 is not a knowledge dump. It is a behavioral anchor layer — a small set of rules that must fire in every session.

**Tier 2 — JIT Reference Documents (100-500 lines per domain)**

The JIT layer contains dense domain-specific content: library API patterns, testing framework conventions, antipattern checklists for QA agents, framework-specific rules. This content is loaded on-demand, not on every invocation. Claude Code implements this via skills (`SKILL.md` files) and child-directory `CLAUDE.md` files, which are pulled in "on demand when working with files in those directories" [OFFICIAL, code.claude.com/docs/en/best-practices].

The token economics justify this architecture. The Microsoft agent-skills progressive disclosure documentation reports that at Tier 1 (metadata only), roughly 50-100 tokens per skill are consumed at startup — loading 133 skills costs only 7,000-13,000 tokens total. Full skill bodies (Tier 2) run 500-2,000 tokens each. Tier 3 reference files vary by size. Loading everything simultaneously causes "context rot — diluted attention and conflated patterns" [OFFICIAL, deepwiki.com/microsoft/agent-skills].

**Tier 3 — Reference Files Loaded On Demand**

For truly dense reference content — full API specifications, comprehensive antipattern catalogs, worked examples with real source code — the pattern is external files linked from skills, not inlined. The Jetpack Compose agent skill (`aldefy/compose-skill`) implements this as 17 separate markdown guides covering distinct topics, plus 6 files of actual source code from the androidx codebase. An agent searching for state management guidance loads that guide; it does not load all 23 files at once.

This mirrors the RAG paradigm, which the 2025-2026 community increasingly describes as "progressive disclosure." As one 2026 practitioner article notes: "Retrieval-Augmented Generation (RAG) is fundamentally a progressive disclosure pattern. Instead of fine-tuning a model with all relevant knowledge, RAG systems retrieve only the chunks relevant to the current query." [PRAC, medium.com/@martia_es/progressive-disclosure]

---

## Prohibition-First Ordering: Evidence and Practice

The question of whether NEVER-DO-THIS rules should precede positive conventions has both empirical and practical dimensions.

**The "lost in the middle" research base**: A well-replicated finding from Liu et al. (2024), published in Transactions of the Association for Computational Linguistics, established that LLM performance degrades significantly when relevant information appears in the middle of long contexts. The effect was measured as a 30%+ accuracy drop on multi-document QA tasks when the answer moved from position 1 to position 10 in a 20-document context. The technical cause is the decay effect of Rotary Position Embedding (RoPE), which makes models attend more strongly to tokens at the beginning and end of sequences. [OFFICIAL, aclanthology.org/2024.tacl-1.9]

**Implications for rule ordering**: The practical inference drawn by the 2025 agent-development community is to place the most critical rules at the beginning of any context block, not in the middle. LessWrong empirical testing of LLM agents on safety rules found that the single positively-framed principle ("Always do X") saw the highest adherence across all models, suggesting rule framing is "a significant and underexplored variable in agent compliance." [PRAC, lesswrong.com — article body inaccessible; summary from search result].

**The three-tier boundary framework**: The GitHub "How to write a great agents.md" analysis of 2,500+ repositories did not find evidence for pure prohibition-first ordering as the dominant pattern. Instead, effective files used what it calls a three-tier boundary framework:
- Always (permitted autonomously)
- Ask First (judgment calls requiring confirmation)
- Never (hard constraints)

This structure places prohibitions in a named section rather than at the very top, but makes them unambiguous and structurally distinct from positive conventions. The Augment Code guide corroborates this, recommending explicit "Never" sections to signal "non-negotiable constraints" as opposed to stylistic preferences. [PRAC, augmentcode.com/guides/how-to-build-agents-md]

**Practical recommendation derived from evidence**: The "lost in the middle" finding argues for critical prohibitions near the top of any section or document. The framing evidence suggests NOT leading with pure prohibition lists — the most-followed rules use positive framing. The resolution: lead with the tech stack anchors and the hardest Never-do constraints, then cover positive conventions, with nuanced judgment calls last. This mirrors the Augment Code six-section structure: Tech Stack → Commands → Coding Conventions → Testing Rules → Boundary Rules (with the three tiers) → Non-Standard Tooling.

---

## Version Pinning as a Guideline Strategy

Research on LLM API hallucination confirms that version anchoring is not optional when specialist agents must use specific library versions.

Amazon Science's 2024 paper "On Mitigating Code LLM Hallucinations with API Documentation" found that Code LLMs show dramatically different accuracy by API frequency: GPT-4o achieved 93.66% accuracy on high-frequency APIs but only 38.58% on low-frequency ones. [OFFICIAL, assets.amazon.science]. Libraries under active development (Jetpack Compose, new coroutines APIs, Kotlin 2.x features) contain many low-frequency APIs in training data.

The research further found that "API Description + Specification" at roughly 95 tokens per augmentation achieved near-optimal performance improvement, versus 685 tokens for full documentation. The practical implication: version-pinned API specifications (not full documentation) are the right approach for guideline files. A line like `// We use Compose 1.7 — use AnimatedVisibility not the deprecated AnimatedVisibleContent` encodes both the version anchor and the migration path in ~20 tokens.

The Augment Code community guide is explicit on this mechanism: "Without version anchors, agents default to whichever API conventions dominate training data — defeating the file's purpose." Specify versions "hard," treating them as non-negotiable constraints. [PRAC, augmentcode.com]

JetBrains' approach to this problem at the IDE plugin level is instructive: they created a plugin that provides "guidelines for AI agents like Junie and Claude Code that helps them generate modern code and ensures they use the latest features and follow best practices compatible with your current version." Their Go guidelines, for example, teach agents to use `slices.Contains()` introduced in Go 1.21, preventing fallback to older patterns. [OFFICIAL, blog.jetbrains.com/go/2026/02/20]

---

## The H2 Anchor Technique for Grep-able Reference Documents

When reference documents are too long to load in full, agents must navigate to the relevant section. The H2 anchor technique uses semantically specific section headers so agents can `Grep` for the precise domain keyword.

The Jetpack Compose agent skill (`aldefy/compose-skill`) demonstrates this pattern. Its section headers are specific and searchable: "State management", "Lists and scrolling", "Design-to-code", "Production crash playbook" — not generic headings like "Overview" or "Best Practices." An agent asked to write a lazy list component searches for "Lists and scrolling" rather than scanning 3,000 lines of prose. [PRAC, github.com/aldefy/compose-skill]

The Microsoft agent-skills documentation specifies the activation mechanism: the `description` field in YAML frontmatter "must encode: what the skill does, when to use it, trigger phrases." This applies at the skill level, but the same principle extends to section headers within a skill's reference documents — they are the trigger phrases for within-document navigation.

The Cursor rules documentation confirms this for cross-file routing: "Agents can decide from context whether to consider a rule useful based on its description, and if selected, the agent requests the full contents." Section headers function as the description layer within a file. [OFFICIAL, docs.cursor.com/context/rules]

Practical guidance for authoring grep-able reference docs:
- Use domain terms, not document terms. "Coroutine cancellation" not "Section 4."
- One concept per H2. Do not combine "Performance and Testing" in one section.
- Avoid synonym ambiguity. Pick one term (e.g., "ViewModel") and use it consistently.
- Keep each section self-contained enough to be read without surrounding context.

---

## Structuring Antipattern Lists for QA Agents

QA agents have a different consumption pattern from developer agents. A developer agent generates code; a QA agent reviews it against a checklist. This difference affects the optimal structure.

**Checklist vs. prose vs. code example**: Evidence from the AGENTS.md community analysis is clear: "One real code snippet showing your style beats three paragraphs describing it." [PRAC, github.blog]. For QA agents, this translates to contrast tables rather than prose descriptions. The compose-skill antipattern presentation uses exactly this format:

| Area | Wrong | Right |
|------|-------|-------|
| State | `remember { mutableStateOf() }` everywhere | Picks the right state primitive |

This format encodes both the incorrect pattern (what to catch) and the correct one (what to approve) in a structure a QA agent can scan in a single pass. [PRAC, github.com/aldefy/compose-skill]

**The structured specification advantage**: The Amazon Science hallucination research found that "API Specification" (structured argument lists) outperformed narrative documentation for Code LLM performance. This generalizes: structured, parseable formats (tables, numbered checklists, labeled pairs) outperform prose for compliance tasks because they reduce the parsing burden on the model.

**Ordering within antipattern lists**: Given the "lost in the middle" finding, the most critical antipatterns — those with highest severity or most frequent occurrence — should appear at the top of each section. Trivial style violations belong at the end or in a separate section. A QA agent that runs out of context budget will catch the dangerous patterns at least.

**Named categories for QA checklists**: Rather than a flat list of 100 antipatterns, effective QA checklists group them by domain (Security, Performance, State Management, Testing) and use consistent naming: each entry is `[CATEGORY]: pattern description`. This enables a QA agent to be invoked with a scoped instruction: "Check for PERFORMANCE antipatterns" and grep to the right section.

---

## Worked Code Examples: Evidence for Their Effectiveness

Multiple converging lines of evidence support prioritizing worked code examples over prose descriptions in domain-specific guidelines.

**Empirical evidence from prompting research**: A 2025 study found that "structural cues like I/O examples and method summaries strongly correlate with higher-quality outputs in code generation." A separate study found that prompt template formatting causes up to 40% performance variation across LLMs — Markdown-formatted examples outperform plain prose for code tasks. [OFFICIAL, arxiv.org/html/2411.10541v1]

**Few-shot example quality**: Research on few-shot code generation found that "LLM coding ability is shaped by which few-shot examples are included" — not just whether examples are present, but whether they are representative of the target domain. For a Kotlin specialist agent, a Compose few-shot example outperforms a generic Kotlin example. [OFFICIAL, arxiv.org/html/2412.02906v1]

**The "receipts" approach**: The compose-skill's "source code receipts" layer (6 files of actual Kotlin from androidx/androidx and compose-multiplatform-core) represents a sophisticated application of this principle. Rather than describing what patterns look like, it shows actual production code from the canonical upstream source. An agent cannot misinterpret a real `LazyColumn` implementation from the Compose source. [PRAC, github.com/aldefy/compose-skill]

**The token efficiency concern**: The Augment Code analysis notes that worked code examples in instruction files impose ~19% inference overhead. However, the same research found that auto-generated files incur the same cost with *negative* returns (−2% success rate). Human-curated, domain-specific examples justify the overhead; generic examples do not. The recommendation: include worked examples only for counterintuitive patterns — cases where prose would fail. Standard conventions that match training data do not need examples.

**Anthropic's own guidance**: "Examples are the 'pictures' worth a thousand words" and "diverse, canonical examples" are preferred over "exhaustive edge-case catalogs." [OFFICIAL, anthropic.com/engineering/effective-context-engineering-for-ai-agents]

---

## The `paths:` / `globs:` Frontmatter Pattern for Routing

Routing dense guidelines only to relevant file contexts is a first-class feature in multiple agent platforms.

**Claude Code** implements this through child-directory `CLAUDE.md` files. A `src/android/CLAUDE.md` is loaded automatically when Claude works in Android source files, and a `src/shared/CLAUDE.md` loads for shared module work. This is path-based routing without requiring any frontmatter syntax. [OFFICIAL, code.claude.com/docs/en/best-practices]

**Claude Code skills** with YAML frontmatter `description` fields achieve semantic routing — skills are invoked when the task description matches. The `disable-model-invocation: true` flag prevents automatic invocation for skills meant to be called explicitly. [OFFICIAL, code.claude.com/docs/en/best-practices]

**Cursor** uses `.cursor/rules/*.mdc` files with a `globs` frontmatter field. Effective Kotlin guidelines auto-attach to `*.kt` and `*.kts` files. The community has identified a limitation: combining types with `{}` in globs does not always work as expected, and combining `globs` with `description` in the same rule can cause unexpected behavior. [PRAC, docs.cursor.com/context/rules; cursor.com forums]

**Sourcegraph Amp** introduced the `globs` frontmatter pattern for AGENTS.md: "To provide guidance that only applies when working with certain files, you can specify `globs` in YAML front matter." [PRAC, gist.github.com/0xdevalias]

**GitHub Copilot Coding Agent** uses `applyTo` frontmatter in `.github/instructions/*.instructions.md` files to scope instructions to specific file patterns. [OFFICIAL, github.blog]

For Claude Code specifically: the skills architecture with YAML frontmatter `description` provides the most reliable routing, with path-based child `CLAUDE.md` files as a secondary mechanism for file-tree-scoped rules. Direct `paths:` frontmatter is available in third-party tools but not a Claude Code native pattern.

---

## Community Patterns for Kotlin/Android/Compose Stacks

The Kotlin/Android/Compose domain has become a reference case for agent guideline architecture due to its complexity: multiple library layers (Kotlin, AndroidX, Compose), frequent breaking changes, a large antipattern surface, and strong opinions about correct patterns.

**awesome-android-agent-skills** (github.com/new-silvermoon/awesome-android-agent-skills) organizes skills by domain category:
- Architecture (Clean Architecture, ViewModel, Data Layer)
- UI (Compose, Navigation, Accessibility)
- Migration (XML→Compose, RxJava→Coroutines)
- Performance, Concurrency, Testing, Build

This hierarchical categorization matches the three-tier architecture: a shared `Agent.md` root with per-domain skill files. The README identifies expert guidance areas including "Kotlin Concurrency Expert for reviewing Coroutines issues" and "Android Coroutines best practices" as separate specialist skills. [PRAC, github.com/new-silvermoon/awesome-android-agent-skills]

**compose-skill** (github.com/aldefy/compose-skill) is the most fully realized example of domain-specific agent skill architecture. It provides:
- 17 practical reference guides covering distinct Compose topics
- 6 "source code receipts" from actual androidx/androidx source
- Problem-solution mapping rather than prohibition lists
- Comparison tables for antipattern presentation
- Topic-per-file organization enabling selective loading

The README explicitly quantifies the value: comparison before/after for eight areas including state management, performance, and production crash debugging. [PRAC, github.com/aldefy/compose-skill]

**JetBrains coding guidelines plugin**: JetBrains' approach for Junie and Claude Code is version-aware guideline injection. Their Go language plugin teaches modern API usage (e.g., `slices.Contains()` vs legacy patterns) and is automatically applied for the correct version. This represents a production-proven version-pinning strategy at IDE scale. [OFFICIAL, blog.jetbrains.com/go/2026/02/20]

**The Compose Kotlin Compatibility Map**: Google maintains an official compatibility table at developer.android.com mapping Compose versions to Kotlin versions. A well-designed Compose skill would encode the current project's intersection of these versions as the version anchor — preventing the hallucination of APIs from incompatible library versions. [OFFICIAL, developer.android.com/jetpack/androidx/releases/compose-kotlin]

---

## Synthesis: Design Principles for Dense Domain Guideline Files

Drawing together the evidence, the following design principles emerge for delivering dense, domain-specific guidelines to specialist agents:

**1. Layer by load frequency, not by topic.** Always-loaded rules are behavioral anchors (<100 lines). Domain reference content is JIT. Exhaustive catalogs are on-demand. Never put all three in one file.

**2. Pin versions explicitly.** Every library mentioned in a guideline file should include its version. Low-frequency APIs (new Compose APIs, Kotlin 2.x features) have hallucination rates near 40% without version anchors. A 5-token version annotation prevents pages of correction.

**3. Put critical prohibitions near the top of their section.** The "lost in the middle" effect is real and documented. A prohibition at line 5 is more reliably followed than the same prohibition at line 50.

**4. Use the three-tier boundary framework for prohibitions.** Never / Ask First / Always is more effective than a flat NEVER list. It provides proportionality and prevents agents from treating trivial style notes with the same urgency as security prohibitions.

**5. Use comparison tables for antipatterns, not prose.** Wrong column / Right column forces the agent to see both the pattern to catch and the correct replacement. Prose descriptions of antipatterns are easy to misparse.

**6. Choose counterintuitive examples.** Code examples cost tokens. Only include them for patterns that diverge from the training data baseline — the cases where prose would fail. Standard Kotlin idioms do not need examples. New Compose state APIs do.

**7. H2 headers are the navigation layer.** Section headers in reference documents are search keys. Make them match the terms agents will grep for. "Coroutine cancellation" and "LazyColumn performance" are better than "Advanced Topics Part 3."

**8. Use semantic skill activation.** The `description` field in YAML frontmatter is the activation trigger. Encode trigger phrases explicitly: "Use this skill when working with Jetpack Compose, @Composable functions, or LazyColumn." The activation mechanism must be in the metadata, not the body.

**9. Cap reference documents at 500 lines.** Above this threshold, split into topic-specific files. An agent searching for guidance on navigation should not have to wade through state management content to find it.

**10. One representative source code example per counterintuitive pattern.** The "receipts" approach (real upstream source code) is the strongest form. Where unavailable, a curated example from the actual codebase outperforms a contrived illustration.

---

## Sources

- [OFFICIAL] Best Practices for Claude Code — https://code.claude.com/docs/en/best-practices
- [OFFICIAL] Effective Context Engineering for AI Agents — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- [OFFICIAL] Create Custom Subagents — https://code.claude.com/docs/en/sub-agents
- [OFFICIAL] On Mitigating Code LLM Hallucinations with API Documentation (Amazon Science, 2024) — https://arxiv.org/html/2407.09726v1
- [OFFICIAL] Lost in the Middle: How Language Models Use Long Contexts (Liu et al., TACL 2024) — https://aclanthology.org/2024.tacl-1.9/
- [OFFICIAL] Coding Guidelines for Your AI Agents — https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/
- [OFFICIAL] Write Modern Go Code With Junie and Claude Code (JetBrains, 2026) — https://blog.jetbrains.com/go/2026/02/20/write-modern-go-code-with-junie-and-claude-code/
- [OFFICIAL] Compose to Kotlin Compatibility Map — https://developer.android.com/jetpack/androidx/releases/compose-kotlin
- [OFFICIAL] Cursor Rules Documentation — https://docs.cursor.com/context/rules
- [OFFICIAL] Does Prompt Formatting Have Any Impact on LLM Performance? (2024) — https://arxiv.org/html/2411.10541v1
- [OFFICIAL] Does Few-Shot Learning Help LLM Performance in Code Synthesis? (2024) — https://arxiv.org/html/2412.02906v1
- [PRAC] How to Write a Great agents.md: Lessons from over 2,500 Repositories — https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
- [PRAC] How to Build Your AGENTS.md (2026) — https://www.augmentcode.com/guides/how-to-build-agents-md
- [PRAC] Progressive Disclosure Pattern (Microsoft Agent Skills, DeepWiki) — https://deepwiki.com/microsoft/agent-skills/5.3-progressive-disclosure-pattern
- [PRAC] compose-skill: Jetpack Compose Agent Skill — https://github.com/aldefy/compose-skill
- [PRAC] awesome-android-agent-skills — https://github.com/new-silvermoon/awesome-android-agent-skills
- [PRAC] Some Notes on AI Agent Rule / Instruction / Context Files (0xdevalias gist) — https://gist.github.com/0xdevalias/f40bc5a6f84c4c5ad862e314894b2fa6
- [PRAC] Claude Code Best Practices: Lessons From Real Projects — https://ranthebuilder.cloud/blog/claude-code-best-practices-lessons-from-real-projects/
- [PRAC] Progressive Disclosure for AI Agents (2026) — https://medium.com/@martia_es/progressive-disclosure-the-technique-that-helps-control-context-and-tokens-in-ai-agents-8d6108b09289
- [PRAC] Managing AI Agents: Lessons Learned So Far (February 2026) — https://www.seanhenri.com/managing-ai-agents-lessons-learned
- [PRAC] Kotlin Cursor Rules: Android Development Best Practices — https://promptgenius.net/cursorrules/frameworks/mobile/kotlin
- [PRAC] Library Hallucinations in LLMs: Risk Analysis (2024) — https://arxiv.org/pdf/2509.22202
- [UNVERIFIED] The three-tier boundary framework (Always / Ask First / Never) is widely cited across the AGENTS.md community but lacks a single canonical source attributable to peer-reviewed research.
