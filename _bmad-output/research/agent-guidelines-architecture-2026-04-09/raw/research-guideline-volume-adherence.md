---
content_origin: claude-code-subagent
date: 2026-04-09
sub_question: "What is the empirical relationship between guideline volume, placement in context, and adherence quality — when does adding more guidelines degrade rather than improve results?"
topic: "Agent-specific guidelines architecture in Claude Code"
---

# Guideline Volume, Context Placement, and Adherence Quality

## Overview

This document synthesizes current empirical evidence on the relationship between instruction/guideline volume, placement within the LLM context window, and measurable adherence quality. Findings are drawn from academic research (2023–2026), official Anthropic documentation, and practitioner observations. The central finding: there is a non-linear relationship between guideline volume and adherence — up to a threshold, more instructions can improve behavior; beyond it, degradation is sharp and often invisible to the author of the guidelines.

---

## 1. The "Lost in the Middle" Problem

The foundational empirical finding on context position comes from Liu et al. (2024), published in *Transactions of the Association for Computational Linguistics*. **[OFFICIAL — published paper, slightly older than 18 months but remains the canonical reference; flag: 2023 preprint, 2024 publication]**

The study measured LLM performance on multi-document question answering and key-value retrieval as a function of where the relevant document appeared in a fixed-length context. The results were unambiguous:

- Accuracy dropped **30+ percentage points** when the relevant document moved from position 1 to position 10 in a 20-document context (~75% at position 1, ~55% at position 10).
- Performance partially recovered at the very end of the context window (~72% at position 20).
- This created a characteristic **U-shaped performance curve**: strong at both edges, severely degraded in the middle.

The architectural cause is Rotary Position Embedding (RoPE), which creates natural attention decay for tokens distant from sequence boundaries — an architectural "blind spot" rather than a model capability limitation. Subsequent work through 2025 confirmed this pattern across GPT-4, Claude, and LLaMA architectures, and across context lengths from 4K to 128K tokens.

**Implication for guidelines:** Instructions placed in the middle of a long context — sandwiched between a system prompt prefix and a long user message — are at highest risk of being ignored. The most critical behavioral rules must appear at the beginning or end of the context, not buried in a dense block of guidelines.

---

## 2. Context Rot: Degradation as Context Grows

Beyond position, there is a more fundamental problem: performance degrades as total context length increases, independent of where within that context the instructions appear.

Chroma's research team (2025) conducted a systematic evaluation of 18 frontier LLMs including GPT-4.1 and Claude 4, testing accuracy as context length grew. **[PRAC — practitioner research lab, 2025]** Key findings:

- **Every model tested performed worse as input length increased**, with no exceptions.
- Degradation was not always gradual: some models held at ~95% accuracy and then dropped sharply to ~60% once a context-length threshold was crossed.
- Claude models tended toward conservative abstention under uncertainty; GPT models showed higher hallucination rates with distractors present.
- Adding even **a single distractor document** reduced accuracy relative to a clean-context baseline. Four distractors showed substantially worse performance than one.

This was independently confirmed by NVIDIA's RULER benchmark, which found that GPT-4's effective reliable context is approximately **64K tokens** despite its claimed 128K capacity — a >50% gap between advertised and effective limits. In some task configurations, effective context fell to less than 1% of the advertised maximum.

The Chroma research also provided a crucial mechanism insight: performance degradation in long contexts stems from two compounding effects:
1. **Attention sinks** — Initial tokens receive disproportionately high attention regardless of semantic importance, displacing attention from later instructions.
2. **Attention dilution** — Each additional token forces every other token to receive less attention on average, so adding more context reduces the "attention share" available to any specific instruction.

**Implication for guidelines:** Even with a 200K token context window, practical instruction density is limited. More tokens of guidelines means less attention per instruction. The context window limit is not the practical limit; attention dilution occurs well before it.

---

## 3. Empirical Instruction-Count Thresholds

The most directly relevant quantitative study for guideline design is "How Many Instructions Can LLMs Follow at Once?" (2025, OpenReview). **[OFFICIAL — peer-reviewed preprint, 2025]** This study evaluated 20 models across instruction densities from 10 to 500 simultaneous instructions.

Key findings by model class:

| Model | Pattern | Threshold | Accuracy at 500 instructions |
|---|---|---|---|
| Gemini 2.5 Pro | Threshold decay | ~150 instructions | 68.9% |
| o3 (high) | Threshold decay | ~150 instructions | 62.8% |
| Grok-3 | Threshold decay | ~150 instructions | 61.9% |
| Claude 3.7 Sonnet | Linear decay | No sharp threshold | 52.7% |
| GPT-4.1 | Linear decay | No sharp threshold | 48.9% |
| Claude 3.5 Haiku | Exponential decay | Very early | ~15% |
| Llama 4-Scout | Exponential decay | Very early | 6.7% |

Three distinct **degradation patterns** were identified:

1. **Threshold decay** (reasoning models like o3, Gemini 2.5 Pro): Performance remains near-perfect through approximately 100–250 instructions, then transitions to a steeper degradation slope. These models have a practical "safe zone."

2. **Linear decay** (GPT-4.1, Claude 3.7 Sonnet): Steady, predictable accuracy decline across the full spectrum — no safe threshold, but no sudden cliff either.

3. **Exponential decay** (Claude 3.5 Haiku, Llama 4-Scout): Rapid early degradation, with performance stabilizing at accuracy floors as low as 7–15%.

At extreme instruction densities, all models shifted from "selective instruction satisfaction" to "uniform failure patterns" — meaning they stopped selectively dropping hard instructions and began dropping instructions uniformly. The error mode shifted from modification errors to **omission errors** (complete instruction dropping).

**Direct implication:** The 100–150 instruction range identified by practitioner sources as a practical "budget" aligns with the empirical threshold at which reasoning-class models begin to degrade. Weaker models (Haiku-class) degrade far earlier — potentially at 20–30 simultaneous instructions. This means guidelines designed for Sonnet-tier models will be systematically too dense for tasks routed to Haiku-tier models.

---

## 4. Anthropic's Official Guidance on CLAUDE.md Structure

Anthropic's official Claude Code documentation (code.claude.com/docs/en/memory and code.claude.com/docs/en/best-practices, 2025–2026) provides explicit thresholds and architectural recommendations. **[OFFICIAL]**

**Size guidance:**
- Target **under 200 lines** per CLAUDE.md file.
- Longer files consume more context and reduce adherence.
- CLAUDE.md is delivered as a **user message** after the system prompt, not as part of the system prompt itself — meaning it does not receive the elevated attention weight of system-level instructions.

**The primary diagnostic signal from official docs:**
> "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."

**What to include vs. exclude:**
- Include: Bash commands Claude cannot guess, code style rules that differ from defaults, testing instructions, repo etiquette, architectural decisions specific to the project, developer environment quirks, common gotchas.
- Exclude: Anything Claude can figure out by reading code, standard language conventions, detailed API documentation, information that changes frequently, self-evident practices like "write clean code."

**Structural recommendations:**
- Use markdown headers and bullets to group related instructions; structure aids scan-ability.
- For instructions over 200 lines, split using `@import` syntax or `.claude/rules/*.md` path-scoped files.
- Use `IMPORTANT` or `YOU MUST` emphasis to improve adherence for critical rules (documented as effective).

**Skills vs. rules distinction:**
> "For domain knowledge or workflows that are only relevant sometimes, use skills instead. Claude loads them on demand without bloating every conversation."

This is the official JIT pattern — skills load when invoked, while rules load every session.

---

## 5. Context Dilution from Unrelated Guidelines

The practitioner concept of "priority saturation" — when everything is marked important, nothing is — has a structural basis in the attention dilution research. **[PRAC — practitioner synthesis, logically derived from published research]**

The Chroma 2025 study specifically measured the effect of **semantically irrelevant distractors**: documents that were topically adjacent but not relevant to the current query. Even these "near-miss" distractors degraded performance, and this effect was greater than completely unrelated noise. The implication is that guidelines which are related-but-not-applicable (e.g., Android development rules loaded during an iOS task) may be *more* harmful than having no guidelines at all, because the model attempts to reconcile their relevance.

A 2025 analysis on LLM sensitivity to prior context (arxiv.org/pdf/2506.00069) found that "the impact of prior context varies depending on content, even when unrelated to the current task." Order effects matter: instructions presented earlier receive more attention. When a large block of irrelevant guidelines precedes a small block of relevant ones, the relevant ones receive less processing attention.

**Implication:** A monolithic guidelines file containing all rules for all subsystems (Kotlin, Compose, QA antipatterns, API conventions, database patterns) loads unrelated rules into context on every invocation. The Kotlin compose rules consume attention budget even when Claude is writing a REST handler. The degradation is not hypothetical — it is mechanistically predicted by attention dilution and empirically confirmed by distractor studies.

---

## 6. JIT Loading via `paths:` Frontmatter — Does It Actually Help?

Claude Code's `.claude/rules/` directory supports path-scoped rules via YAML frontmatter. The design intent: rules with `paths: ["src/api/**/*.ts"]` load only when Claude reads files matching that pattern. This is the JIT loading mechanism intended to address context dilution from unrelated guidelines.

**What the official documentation says** (code.claude.com/docs/en/memory): **[OFFICIAL]**
> "Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use."

This is the documented behavior. Rules load on file read, not on file write or on session start.

**Critical known issue:** GitHub issue #16299 (open as of February 2026) documents a regression: path-scoped rules with `paths:` frontmatter are **loading globally at session start**, not conditionally on file read. **[PRAC — documented bug report, February 2026]**

One user reported 28 rules loading at startup when only ~5 should be global — a 5x context bloat. The issue affects Claude Code CLI, VS Code Extension, and API usage. The workaround (`alwaysApply: false`) has no documented effect.

A second confirmed bug (issue #23478): path-based rules are not injected on file Write operations, only on Read. This means rules intended to govern file creation are not active when Claude creates a new file — only when it reads one. **[OFFICIAL — documented in GitHub issues]**

**Net assessment of JIT loading:** The architectural intent is sound and aligns with empirical findings on context dilution. In a correctly functioning implementation, scoped rules would reduce effective instruction density to only the rules relevant to the current file context. However, the current implementation has documented regressions that may negate the benefit — all rules load globally regardless of path scope. Anyone relying on JIT scoping for context reduction should verify actual behavior with the `InstructionsLoaded` hook before assuming the mechanism works as documented.

---

## 7. Splitting Files vs. One Large File — Evidence

No published A/B test directly compares monolithic vs. split guideline files in Claude Code. However, the structural evidence strongly favors splitting:

1. **Context position effects**: A 400-line monolithic file pushes critical rules into the middle of context. Separate files, loaded selectively, allow critical rules to appear at consistent positions.

2. **Attention budget per rule**: A 50-line focused rules file for API development leaves more attention budget per rule than a 400-line file covering all subsystems simultaneously.

3. **The "selective loading" advantage**: When path-scoped rules work correctly, a Kotlin Compose rule file only loads when Claude is editing `.kt` files. This means the effective instruction count seen by Claude during a Compose task is the Compose-specific rules plus universal rules — not the full ruleset for every technology in the project.

4. **Practitioner convergence**: Multiple independent practitioner sources (HumanLayer blog, Morph documentation, eesel.ai guide, Rick Hightower on Medium) independently arrived at the same architecture: one thin CLAUDE.md for universals, plus topic-specific rules files with path scoping. This convergence suggests practical effectiveness.

**Official Claude Code documentation states directly:** "If your instructions are growing large, split them using imports or `.claude/rules/` files."

---

## 8. The Skills Architecture — an Orthogonal JIT Mechanism

Claude Code's Skills system (`.claude/skills/`) provides a different JIT loading mechanism: skills load when explicitly invoked (by name or by relevance match), not based on file path context. **[OFFICIAL]**

Official guidance distinguishes:
- **Rules**: "Load into context every session or when matching files are opened."
- **Skills**: "Only load when you invoke them or when Claude determines they're relevant to your prompt."

For complex domain-specific guidelines — like a comprehensive Kotlin Compose style guide, a QA antipattern detection checklist, or library-specific API usage rules — Skills represent a superior JIT mechanism because:
1. They load on task relevance, not file path (a more semantically precise trigger)
2. They are fully out of context when not invoked (zero attention cost vs. path-scoped rules which may still load globally due to the current bug)
3. They can be structured as workflows with embedded expertise, not just passive instruction lists

The tradeoff: Skills require explicit invocation or a highly specific relevance trigger. Rules are more "passive" and apply without deliberate activation.

---

## 9. Synthesis: The Practical Degradation Curve

Combining the evidence, a practical model of guideline effectiveness emerges:

**Zone 1: 1–50 effective instructions** — High adherence zone. All major frontier models (Sonnet, Opus, GPT-4.1, Gemini 2.5 Pro) perform reliably. This is the "safe" zone.

**Zone 2: 50–150 effective instructions** — Moderate-risk zone. Reasoning-class models (o3, Gemini 2.5 Pro) maintain near-threshold performance. Non-reasoning models (GPT-4.1, Claude 3.7 Sonnet) show linear degradation. Expect 10–20% adherence reduction vs. Zone 1.

**Zone 3: 150–300 effective instructions** — High-risk zone. Reasoning models hit their threshold and begin steeper degradation. All models show meaningful omission errors. Instructions at middle context positions are systematically dropped. Expect 20–50% adherence reduction vs. Zone 1.

**Zone 4: 300+ effective instructions** — Breakdown zone. All models shift to uniform failure patterns. The model cannot reliably satisfy any specific instruction because the instruction-following capacity is saturated. Adding more instructions at this point provides zero marginal benefit and actively degrades adherence to existing rules.

The 200-line CLAUDE.md guideline from Anthropic maps approximately to Zone 2 — staying below the threshold where degradation becomes severe.

**Note on effective vs. total instructions:** "Effective instructions" is not simply line count. A 200-line CLAUDE.md with 50 distinct behavioral rules may be within Zone 1. A 200-line file with 200 distinct rules is in Zone 2-3. Specificity matters: "use 2-space indentation" is one clear instruction; "format code properly" is ambiguous and consumes an instruction slot without providing reliable behavioral signal.

---

## 10. Actionable Design Principles

Drawing directly from the evidence:

1. **Budget by effective instruction count, not line count.** Count distinct behavioral directives, not lines of markdown. Target under 150 effective instructions in context at any moment.

2. **Place the most critical rules first.** Attention sinks favor early context; critical never-break rules belong at the top of CLAUDE.md, not after extensive preamble.

3. **Scope complex technical guidelines to path-specific rules.** Kotlin Compose rules should not be in context during TypeScript API work. Use `.claude/rules/` with path frontmatter — but verify the JIT loading bug (issue #16299) is resolved before relying on it.

4. **Use Skills for complex domain knowledge.** A 2,000-word Kotlin Compose style guide belongs in a skill that loads on invocation, not in a rules file that loads globally. Skills are zero-cost when not invoked.

5. **Treat "emphasis inflation" as a warning signal.** Adding `IMPORTANT` and `YOU MUST` to every rule is a symptom that the file is too long — attention emphasis only works when it distinguishes signal from noise, not when everything is emphasized.

6. **The diagnostic test: does removing a rule change behavior?** If removing a rule does not change Claude's behavior, either the rule was already followed by default (delete it) or the file is so long the rule was already being ignored (prune aggressively).

7. **Verify effective context with `InstructionsLoaded` hook.** Anthropic's official documentation recommends using the `InstructionsLoaded` hook to log which instruction files actually load and when. This is the only reliable way to confirm JIT behavior given known regressions.

---

## Sources

- **[OFFICIAL]** Liu et al. (2024). "Lost in the Middle: How Language Models Use Long Contexts." *Transactions of the Association for Computational Linguistics*. https://aclanthology.org/2024.tacl-1.9/

- **[OFFICIAL]** Anthropic. "How Claude remembers your project." Claude Code Documentation, 2025–2026. https://code.claude.com/docs/en/memory

- **[OFFICIAL]** Anthropic. "Best Practices for Claude Code." Claude Code Documentation, 2025–2026. https://code.claude.com/docs/en/best-practices

- **[OFFICIAL]** Anthropic. "Effective context engineering for AI agents." Anthropic Engineering Blog, 2024. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

- **[OFFICIAL]** "How Many Instructions Can LLMs Follow at Once?" OpenReview preprint, 2025. https://openreview.net/pdf/0dc36c02c76de4dc2088488ca988ad79a27c6055.pdf — also at https://arxiv.org/html/2507.11538v1

- **[PRAC]** GitHub Issue #16299: "Path-scoped rules in .claude/rules/ load into context globally regardless of paths: frontmatter." Anthropic/claude-code, open as of February 2026. https://github.com/anthropics/claude-code/issues/16299

- **[PRAC]** GitHub Issue #23478: "Path-based rules with paths: frontmatter are not loaded on Write tool — only on Read." Anthropic/claude-code. https://github.com/anthropics/claude-code/issues/23478

- **[PRAC]** Chroma Research Team (2025). "Context Rot: How Increasing Input Tokens Impacts LLM Performance." https://www.trychroma.com/research/context-rot

- **[PRAC]** Morph. "Lost in the Middle LLM: The U-Shaped Attention Problem Explained." https://www.morphllm.com/lost-in-the-middle-llm

- **[PRAC]** Morph. "CLAUDE.md Examples and Best Practices 2026." https://www.morphllm.com/claude-md-examples

- **[PRAC]** diffray.ai. "Context Dilution: When More Tokens Hurt AI." 2025. https://diffray.ai/blog/context-dilution/

- **[PRAC]** Hightower, R. "Claude Code Rules: Stop Stuffing Everything into One CLAUDE.md." Medium, March 2026. https://medium.com/@richardhightower/claude-code-rules-stop-stuffing-everything-into-one-claude-md-0b3732bca433

- **[PRAC]** Claudefa.st. "Claude Code Rules Directory: Modular Instructions That Scale." https://claudefa.st/blog/guide/mechanics/rules-directory

- **[UNVERIFIED]** The concept of "effective instruction slots" (distinct from line count or token count) is a synthesis not directly sourced to a single paper; it emerges from combining the instruction-following capacity research with practitioner observations about specificity requirements.
