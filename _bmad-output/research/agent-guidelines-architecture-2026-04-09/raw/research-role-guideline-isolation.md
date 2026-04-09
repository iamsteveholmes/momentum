---
content_origin: claude-code-subagent
date: 2026-04-09
sub_question: "What patterns prevent guideline bleed between co-existing roles on the same project, where different agents need radically different knowledge domains?"
topic: "Agent-specific guidelines architecture in Claude Code"
---

# Role Guideline Isolation in Multi-Agent Claude Code Projects

## Overview

When a project hosts a Kotlin Compose frontend dev, a backend API dev, a QA agent, an E2E agent, and a PM agent simultaneously, each needs dense, role-specific behavioral guidelines. The challenge is surgical: how do you ensure the Compose dev never loads QA antipattern checklists, the QA agent never drowns in backend API call conventions, and the PM agent never receives Kotlin syntax guidance at all?

This research documents the mechanisms Claude Code offers for guideline isolation, their actual limits (which differ from documented behavior), and the community patterns that work around those limits as of April 2026.

---

## How CLAUDE.md Files Are Delivered — The Foundational Constraint

Understanding why guideline bleed happens requires understanding how CLAUDE.md content reaches Claude in the first place.

**CLAUDE.md is injected as a user message, not a system-level directive.** The content is delivered after the system prompt as advisory context. Claude Code wraps the content in a system reminder instructing the model to "ignore instructions that aren't relevant to the current task." This means Claude exercises judgment about which instructions to apply — it is not forced to process all of them. [OFFICIAL: https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026]

This has a critical implication for guideline bleed: **you cannot prevent an agent from _seeing_ a rule file — you can only influence whether it attends to it**. The enforcement model is behavioral, not structural. Rules are suggestions with varying compliance rates, not hard boundaries. [PRAC: https://www.morphllm.com/claude-md-examples]

The practical consequence, documented empirically: "As instruction count grows, Claude doesn't just ignore the new ones; it starts ignoring all of them uniformly." Every low-value rule dilutes the compliance probability of every high-value rule in a zero-sum attention budget. [PRAC: https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026]

---

## `paths:` Frontmatter — Conditional Loading, Not Access Control

Claude Code 2.0.64 introduced `.claude/rules/` with YAML frontmatter path matching. The syntax:

```yaml
---
paths:
  - "src/ui/**/*.kt"
---
```

**What it does:** Rules with `paths:` frontmatter are only injected into context when Claude reads a file matching the pattern. Rules without `paths:` load unconditionally on every interaction. [OFFICIAL: https://paddo.dev/blog/claude-rules-path-specific-native/]

**What it does not do:** It does not prevent an agent from accessing the rule file. It does not create a hard wall that blocks an agent of the wrong role from receiving a rule. It is conditional loading based on file system activity, not role identity. Claude can verify which rules are active via `/memory`, confirming the transparency of the system. [PRAC: https://paddo.dev/blog/claude-rules-path-specific-native/]

**A confirmed bug with production impact:** Path-based rules only trigger on Read operations, not Write operations. A rule scoped to `**/*.md` will not fire when an agent creates a new `.md` file — only when it reads one. This was documented in GitHub issue #23478 (closed as NOT_PLANNED), with a workaround involving PreToolUse hooks to force a Read before every Write. [PRAC: https://github.com/anthropics/claude-code/issues/23478]

**Verdict:** `paths:` frontmatter provides weak isolation. It prevents incidental loading when an agent is working in a different area of the codebase, but a QA agent working in `src/ui/` would still load Compose-specific rules. It is a scoping convenience, not a role firewall.

---

## Subdirectory CLAUDE.md Files — On-Demand, Directory-Scoped Loading

Subdirectory CLAUDE.md files (e.g., `src/ui/CLAUDE.md`) exhibit a different loading behavior than the root file: **they load on demand, not at startup**. They only activate when Claude processes files within that specific directory.

The hierarchy of CLAUDE.md files is:

1. Managed policy (`/Library/Application Support/ClaudeCode/CLAUDE.md`) — organization-wide, cannot be overridden
2. User global (`~/.claude/CLAUDE.md`)
3. Project root (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
4. Subdirectory files (`./subdir/CLAUDE.md`)
5. Scoped rules (`./.claude/rules/*.md` with YAML frontmatter)

More specific files take precedence when rules conflict. If root says "use 2-space indentation" and `packages/api/CLAUDE.md` says "use 4-space indentation," Claude picks one — the behavior is not deterministic. `claudeMdExcludes` settings can exclude specific files from loading to manage this. [PRAC: https://www.morphllm.com/claude-md-examples]

**For role isolation, subdirectory CLAUDE.md files provide moderate benefit:** A `src/compose-ui/CLAUDE.md` containing Kotlin Compose guidelines would not load unless Claude is actively working in that directory. However, the root project CLAUDE.md is always loaded, so any guidelines placed there are visible to all agents. The pattern only works if you migrate role-specific content from the root file into subdirectory files and keep the root lean. [PRAC: https://www.buildcamp.io/guides/the-ultimate-guide-to-claudemd]

---

## Subagents — The Primary Mechanism for True Guideline Isolation

The most effective isolation mechanism in Claude Code is the subagent system. A subagent is a named Claude instance defined in `.claude/agents/` with its own YAML frontmatter and markdown body:

```yaml
---
name: compose-frontend-dev
description: Implements Kotlin Compose UI features and follows Material Design guidelines
model: sonnet
tools: [Read, Write, Edit, Bash, Glob, Grep]
---

You are a senior Kotlin Compose engineer...
[role-specific guidelines embedded here]
```

The markdown body becomes the system prompt. Critically, **the subagent's system prompt replaces the default Claude Code system prompt entirely** — it is not appended to it. This is the primary mechanism for delivering role-specific guidelines that do not bleed across roles. [OFFICIAL: https://code.claude.com/docs/en/sub-agents]

A subagent's context window contains exactly four things:
1. Its own system prompt (the markdown body)
2. The task prompt from the parent Agent tool call
3. Environment details (working directory, platform, shell)
4. Skills listed in its `skills` frontmatter field

It does not inherit the parent conversation history, prior tool calls, or other subagents' outputs. [OFFICIAL: https://www.morphllm.com/claude-subagents]

---

## The CLAUDE.md Inheritance Problem for Subagents — A Critical Gap

Here is where the documentation and reality diverge significantly.

**The official documentation states** that "CLAUDE.md files and project memory still load through the normal message flow" for subagents. This implies subagents do inherit project-level CLAUDE.md content.

**Community reports and GitHub issues tell a different story.** GitHub issue #29423 (filed Feb 27, 2026, still open with a `stale` label as of April 8, 2026) documents that Task subagents do **not** load:
- `CLAUDE.md` (project root)
- `.claude/rules/*.md` (project rule files)
- `~/.claude/CLAUDE.md` (user-level configuration)

A concrete failure case: a project with 15 rule files in `.claude/rules/` spawned 6 parallel Task subagents to audit 89 error-suppression patterns. Manual re-audit with rules in context found 5 additional violations, 4 logic bugs, and 1 missing error path that the subagents missed — because they applied generic interpretation instead of project-specific rules. [PRAC: https://github.com/anthropics/claude-code/issues/29423]

Additionally, subagents do not inherit PreToolUse hooks or permission rules defined in `.claude/settings.json`. [PRAC: https://github.com/anthropics/claude-code/issues/27661]

**For role isolation, this gap is actually a double-edged sword:**
- If your Compose dev subagent does not load project-level CLAUDE.md, it also doesn't get the QA antipattern checklists. Accidental isolation.
- But it also doesn't get the cross-cutting project conventions it legitimately needs (e.g., commit format, naming conventions), unless those are embedded in the subagent's own system prompt.

The recommended workaround from community practitioners: embed all critical project conventions verbatim in each subagent's system prompt. This is error-prone and doesn't scale as rule files change, but it is the current reliable approach. [PRAC: https://github.com/anthropics/claude-code/issues/29423]

**Cross-corpus reconciliation note:** This file's finding (subagents do NOT load CLAUDE.md, per issue #29423) conflicts with two other statements in this research corpus: (a) `research-claude-code-scoping-mechanisms.md` Section 1 states that "in the interactive CLI, project CLAUDE.md does load for subagents"; and (b) `gemini-deep-research-output.md` Follow-Up 3 states "subagents do not ignore CLAUDE.md. They inherit the root CLAUDE.md." The most specific evidence is issue #29423's concrete failure case. The reconciliation: the behavior may differ between interactive CLI sessions (where CLAUDE.md may load) vs. Task-spawned subagents in the API context (where #29423 documents non-loading). Until official documentation resolves this, the safe architecture is to embed needed conventions in each subagent's system prompt rather than relying on CLAUDE.md inheritance.

---

## Worktree-Based Isolation — Filesystem Separation, Not Rule Separation

Claude Code supports `isolation: worktree` in subagent frontmatter, which gives an agent its own git worktree — a separate copy of the repository where changes don't affect the working directory until merged. This is primarily filesystem isolation for preventing concurrent write conflicts in parallel execution.

**What worktree isolation does for guidelines:** Each worktree shares the same `.claude/` directory structure from the repository. Worktree isolation does not create different rule sets per agent role. A Compose dev agent in worktree A and a QA agent in worktree B would both read from the same `.claude/agents/` and `.claude/rules/` definitions. [PRAC: https://claudefa.st/blog/guide/development/worktree-guide]

The `--worktree` flag for the `claude` CLI creates isolated sessions for parallel human-driven development, not role-based rule isolation. This is not a solution to guideline bleed.

---

## Prompt-Based Isolation — The Most Reliable Pattern

Given that file-based mechanisms provide incomplete isolation, the most reliable approach is **embedding role-specific guidelines directly in the subagent system prompt**, with no reliance on CLAUDE.md inheritance.

The architecture:

```
.claude/agents/
  compose-dev.md        ← system prompt contains ALL Kotlin Compose guidelines
  backend-api-dev.md    ← system prompt contains ALL API/backend guidelines
  qa-agent.md           ← system prompt contains ALL QA antipattern checklists
  e2e-agent.md          ← system prompt contains E2E automation specifics
  pm-agent.md           ← system prompt contains PM workflow and spec guidelines
```

Each agent body is self-contained. It includes:
- Role identity and domain scope
- Stack-specific knowledge (Compose APIs, API contract conventions, etc.)
- Cross-cutting project conventions that apply to this role (embedded, not inherited)
- Explicit exclusions: "You do not write tests. Delegate to @qa-agent."

This approach mirrors the pattern used by practitioners who have built specialized multi-agent setups at scale. One documented implementation with 12 specialized agents used stack-specific knowledge in each agent's prompt — enum patterns, service layer structure, Zod schema factories — rather than relying on project-level CLAUDE.md inheritance. [PRAC: https://dev.to/matkarimov099/how-i-split-claude-code-into-12-specialized-sub-agents-for-my-react-project-3jh8]

The wshobson/agents repository (182 specialized agents across 77 plugins) uses a "progressive disclosure" architecture: skills load knowledge "only when activated," preventing irrelevant instructions from loading into any agent's context. Plugin isolation ensures installing one plugin loads only its specific agents and skills. [PRAC: https://github.com/wshobson/agents]

---

## The Negative Space Problem — Can Agents Be Told to Ignore Irrelevant Rules?

If you cannot prevent an agent from seeing a rule, can you at least ensure it ignores it?

The system already attempts this. Claude Code wraps CLAUDE.md content in a reminder to "ignore instructions that aren't relevant to the current task." But this is a heuristic, not a guarantee. Compliance degrades with rule density. [PRAC: https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026]

**Techniques that provide partial negative-space enforcement:**

1. **Role-scoped sections with explicit headers.** Structuring CLAUDE.md with `## For QA agents only` headers gives the model a signal to skip sections. Not enforced — but legible signals improve selective attention.

2. **Conditional rule tags.** Community practitioners have experimented with `<important if="agent_role == compose-dev">` tag syntax in CLAUDE.md to prevent Claude from ignoring domain-specific rules as files grow longer. This is an unofficial convention — Claude parses it as context, not a structural directive. [UNVERIFIED: pattern noted in community search results via https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026]

3. **Role-tagged rule filenames.** Naming conventions like `.claude/rules/compose-ui-guidelines.md` with a `paths: src/compose/**` frontmatter provide contextual signal even if not enforced. The name signals intent; the paths: frontmatter provides conditional loading.

4. **Negative instructions in subagent prompts.** Explicit "you are NOT responsible for X" statements in a role's system prompt reinforce boundaries. The QA agent prompt should explicitly disclaim Kotlin Compose knowledge, the Compose dev should disclaim E2E test authoring.

---

## `.claudeignore` — No Native Support, Multiple Workarounds Exist

There is no native `.claudeignore` mechanism in Claude Code as of April 2026. Multiple feature requests have been filed since early 2025 (issues #79, #579, #4160, #19875, #29455). Issue #19875 is the canonical tracking issue; most duplicates are closed pointing there. There is no official Anthropic response or implementation timeline visible in any of these threads. [PRAC: https://github.com/anthropics/claude-code/issues/29455]

The `permissions.deny` array in `settings.json` blocks tool access to file patterns (e.g., preventing Claude from reading `.env` files), but this is a security gate, not a guideline scoping mechanism.

Community workarounds:
- **claudeignore tool** by pg-creative: converts a `.claudeignore` file to Claude Code deny rules automatically.
- **li-zhixin/claude-ignore**: a PreToolUse hook that prevents Claude from reading files matching `.claudeignore` patterns, analogous to `.gitignore`. [PRAC: https://github.com/li-zhixin/claude-ignore]
- **Security caveat:** Claude Code has been documented as not consistently respecting deny rules. The Register reported in January 2026 that Claude could read `.env` files despite ignore entries. [PRAC: https://www.theregister.com/2026/01/28/claude_code_ai_secrets_files/]

None of these mechanisms apply to guideline/rule files specifically — they apply to file access generally.

---

## Conflicting Rules — Hierarchy and Resolution Behavior

When global, project, and directory-level CLAUDE.md files exist simultaneously, conflict resolution follows this precedence (highest to lowest):

1. `CLAUDE.local.md` (personal overrides, not committed)
2. `CLAUDE.md` (project root, committed)
3. `~/.claude/CLAUDE.md` (user global)
4. Managed policy (org-wide, lowest priority but cannot be overridden by agents)

More specific subdirectory files override root files for overlapping instructions. When a root CLAUDE.md and a subdirectory CLAUDE.md have genuinely conflicting instructions (not just additive), Claude resolves the conflict "arbitrarily" — meaning it is non-deterministic. [PRAC: https://www.morphllm.com/claude-md-examples]

For multi-role projects, this creates a risk: if you have a root CLAUDE.md with generic project conventions and per-subdirectory CLAUDE.md files with role-specific conventions, conflicts between them may resolve inconsistently across sessions.

---

## User-Level Rule Propagation — Requested, Not Planned

GitHub issue #8395 proposed a mechanism for user-level agent rules (`~/.claude/agent-rules.md`) that would propagate to all subagents, with optional per-subagent overrides via `inherit_rules: true/false` in frontmatter. This would have provided a shared cross-cutting rules layer that agents could opt out of. The issue was **closed as NOT_PLANNED** by Anthropic with no official comment. [PRAC: https://github.com/anthropics/claude-code/issues/8395]

The SubagentStart hook feature request (#23885) asked for `updatedPrompt` support to allow hooks to inject role-specific rules into a subagent's system prompt dynamically. This was closed as a duplicate of #20833 with no Anthropic response. Empirical data provided in the issue showed ~60% non-compliance on worktree rules and ~40% on review steps when rules were only in CLAUDE.md, driving the request for hard injection. [PRAC: https://github.com/anthropics/claude-code/issues/23885]

Both closures suggest Anthropic's current position is that the subagent system prompt (the agent file body) is the intended mechanism for role-specific guidelines — not a propagation system.

---

## Documented Antipatterns

**1. Putting all role guidelines in root CLAUDE.md.** Every agent loads the root file. A QA checklist in root CLAUDE.md is visible to the Compose dev, the PM, and every other agent. This is the most common antipattern.

**2. Relying on `paths:` frontmatter for role isolation.** Path scoping is activity-based, not identity-based. A QA agent working in the UI directory will still load Compose-specific path rules.

**3. Expecting subagents to inherit project conventions automatically.** The CLAUDE.md inheritance gap (issue #29423) means subagents may not receive project rules at all. Teams that rely on this discover it through incorrect agent behavior, not error messages.

**4. Long CLAUDE.md files with dense multi-role guidance.** Attention degradation is real. A 500-line CLAUDE.md covering all five roles will cause Claude to follow none of them reliably. The recommended ceiling is 150-200 lines per file. [PRAC: https://www.morphllm.com/claude-md-examples]

**5. Assuming deny rules provide hard enforcement.** `permissions.deny` and `.claudeignore` workarounds have documented compliance failures. Do not use them as security-critical boundaries.

---

## Synthesis: A Recommended Architecture for Five-Role Projects

Given the constraints above, the most effective architecture as of April 2026:

**Layer 1: Root CLAUDE.md — Cross-cutting project identity only.**
Keep this under 100 lines. Include: repo structure map, commit format, tech stack names, and one-line role registry ("@compose-dev handles all Kotlin UI"). No role-specific guidelines here.

**Layer 2: `.claude/agents/*.md` — One file per role, self-contained system prompts.**
Each agent file embeds all guidelines for that role. Include cross-cutting conventions (commit format, naming) verbatim — do not rely on inheritance. Use tool restriction in frontmatter to enforce domain boundaries:
```yaml
tools: [Read, Grep, Glob]   # QA: read-only by design
```

**Layer 3: Subdirectory CLAUDE.md files — On-demand domain knowledge.**
`src/compose-ui/CLAUDE.md` for Compose patterns. `src/api/CLAUDE.md` for API conventions. These load only when an agent works in that directory, providing ambient context reinforcement for whichever agent visits.

**Layer 4: `.claude/rules/` with `paths:` frontmatter — Enforceable file-pattern rules.**
Use for mechanical constraints (file naming, import ordering) that trigger on read. Accept the known limitation that these don't fire on Write operations — mitigate with PreToolUse hooks if critical.

**Layer 5: Explicit role exclusions in subagent prompts.**
Each agent body should state what it is *not* responsible for: "You do not write acceptance tests. You do not modify API contracts. Delegate to @qa-agent or @backend-api-dev." This is the negative-space declaration that the system cannot enforce structurally.

---

## Sources

- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents) [OFFICIAL]
- [Claude Code Gets Path-Specific Rules (Cursor Had This First)](https://paddo.dev/blog/claude-rules-path-specific-native/) [PRAC]
- [Path-based rules not loaded on Write tool — Issue #23478](https://github.com/anthropics/claude-code/issues/23478) [PRAC]
- [Task subagents do not load project CLAUDE.md — Issue #29423](https://github.com/anthropics/claude-code/issues/29423) [PRAC]
- [User-Level Agent Rules and Rule Propagation — Issue #8395 (closed NOT_PLANNED)](https://github.com/anthropics/claude-code/issues/8395) [PRAC]
- [SubagentStart hook updatedPrompt request — Issue #23885 (closed duplicate)](https://github.com/anthropics/claude-code/issues/23885) [PRAC]
- [.claudeignore feature request — Issue #29455](https://github.com/anthropics/claude-code/issues/29455) [PRAC]
- [Claude Code Subagents: How They Work, What They See & When to Use Them](https://www.morphllm.com/claude-subagents) [PRAC]
- [Claude Code Ignores Your CLAUDE.md? It's the Delivery Mechanism, Not a Bug](https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026) [PRAC]
- [CLAUDE.md Examples and Best Practices 2026](https://www.morphllm.com/claude-md-examples) [PRAC]
- [How I Split Claude Code Into 12 Specialized Sub-Agents](https://dev.to/matkarimov099/how-i-split-claude-code-into-12-specialized-sub-agents-for-my-react-project-3jh8) [PRAC]
- [GitHub - wshobson/agents: Multi-agent orchestration for Claude Code](https://github.com/wshobson/agents) [PRAC]
- [How and when to use subagents in Claude Code — Anthropic Blog](https://claude.com/blog/subagents-in-claude-code) [OFFICIAL]
- [The Ultimate Guide to CLAUDE.md in 2026 — Buildcamp](https://www.buildcamp.io/guides/the-ultimate-guide-to-claudemd) [PRAC]
- [Claude Code multiple agent systems: Complete 2026 guide — eesel AI](https://www.eesel.ai/blog/claude-code-multiple-agent-systems-complete-2026-guide) [PRAC]
- [Subagents should inherit parent session hooks — Issue #27661](https://github.com/anthropics/claude-code/issues/27661) [PRAC]
- [Claude Code ignores ignore rules meant to block secrets — The Register](https://www.theregister.com/2026/01/28/claude_code_ai_secrets_files/) [PRAC]
- [li-zhixin/claude-ignore: PreToolUse hook for .claudeignore patterns](https://github.com/li-zhixin/claude-ignore) [PRAC]
- [AGENTS.md vs CLAUDE.md: What's the Difference and When to Use Each](https://thepromptshelf.dev/blog/agents-md-vs-claude-md/) [PRAC]
- [Best practices for Claude Code sub-agents — PubNub Blog](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/) [PRAC]
- [How Claude Code Builds a System Prompt — dbreunig.com (April 2026)](https://www.dbreunig.com/2026/04/04/how-claude-code-builds-a-system-prompt.html) [PRAC]
- [Claude Code Agent Harness Architecture — WaveSpeed AI](https://wavespeed.ai/blog/posts/claude-code-agent-harness-architecture/) [PRAC]
- [GitHub - Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) [PRAC]
