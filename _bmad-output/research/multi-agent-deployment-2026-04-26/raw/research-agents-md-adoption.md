---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "AGENTS.md standard adoption and authoring patterns (April 2026) — Which tools emit AGENTS.md? Which consume it? What's actually in the manifest spec? What behavior does it drive? Who writes it (humans vs. tooling)? Show repo examples."
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
---

# AGENTS.md Standard Adoption and Authoring Patterns (April 2026)

## Executive Summary

As of 2026-04-26, AGENTS.md has effectively become the de-facto cross-tool context standard for AI coding agents. Originally introduced by OpenAI/Sourcegraph/Google/Cursor/Factory in mid-2025, it was contributed to the Linux Foundation's newly-formed Agentic AI Foundation (AAIF) on December 9, 2025, alongside Anthropic's Model Context Protocol (MCP) and Block's Goose ([Linux Foundation press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)) **[OFFICIAL]**. The spec is intentionally minimalist — plain Markdown, no required schema, no frontmatter — and adoption has accelerated to the point that virtually every major coding agent now reads AGENTS.md natively or via a documented fallback path. The primary tension in April 2026 is between (a) the spec's "just Markdown" purity and (b) growing pressure from tools and v1.1 proposals to standardize optional YAML frontmatter for scoping (`description`, `globs`, `alwaysApply`).

## The Spec Itself

### Format and Structure

The canonical spec at [agents.md](https://agents.md) and the official repo [agentsmd/agents.md](https://github.com/agentsmd/agents.md) ([OFFICIAL]) state explicitly:

> "AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide."

There are **no required fields**, **no predefined schema**, **no version field**, and **no frontmatter requirement**. The repo is MIT-licensed, sits at ~20.7k stars / 1.5k forks as of April 2026, and is implemented as a Next.js documentation site ([agentsmd/agents.md](https://github.com/agentsmd/agents.md)) **[OFFICIAL]**.

The spec recommends — but does not mandate — these conventional sections (drawn from analysis of 2,500+ real files):

- Project overview / repository structure
- Build and test commands
- Code style guidelines
- Testing instructions
- Security considerations / boundaries
- Commit and PR guidelines
- Dev environment tips

### Discovery and Precedence Semantics

The semantic rules — codified across implementations and being formalized in the v1.1 proposal ([Issue #135](https://github.com/agentsmd/agents.md/issues/135)) **[OFFICIAL]** — are:

1. **Jurisdiction:** an `AGENTS.md` governs its containing directory and all subdirectories.
2. **Accumulation:** guidance compounds across the directory tree; nested files extend ancestor guidance.
3. **Precedence:** when conflicts arise, locality wins — local files override ancestor files.
4. **Inheritance:** child files implicitly inherit parent guidance and need not restate it.

The standard precedence chain (per [DeepWiki AGENTS.md format docs](https://deepwiki.com/openai/agents.md/5-agents.md-format-documentation)) **[PRAC]**:

```
LLM System Prompt > Agent System Prompt > User Prompt > Local AGENTS.md > Ancestor AGENTS.md (nearest first)
```

### Version Trajectory

There is no formal "v1.0" stamp on the existing spec — it is intentionally treated as living docs. **[Issue #135](https://github.com/agentsmd/agents.md/issues/135) "AGENTS.md v1.1: Making Implicit Semantics Explicit"** (opened 2026-01-08, draft as of April 2026) is the first formal version proposal **[OFFICIAL]**. It would:

- Formally codify jurisdiction/accumulation/precedence/inheritance.
- Introduce **optional** YAML frontmatter (`description`, `tags`) for "progressive disclosure" — i.e., on-demand loading rather than always-on.
- Provide implementation guidance for agents/harnesses, including recommended index formats.

A separate, earlier issue [#10 "Frontmatter support"](https://github.com/agentsmd/agents.md/issues/10) (opened 2025-08-20, still open) proposed a Cursor-style frontmatter schema (`description`, `alwaysApply`, `globs`) **[OFFICIAL]**. As of April 2026 neither proposal has merged into the spec; the tools have begun shipping their own dialects.

## Governance: Linux Foundation / Agentic AI Foundation

On **December 9, 2025** the Linux Foundation announced the formation of the Agentic AI Foundation (AAIF), with three founding project contributions:

- **Anthropic's** Model Context Protocol (MCP)
- **Block's** Goose
- **OpenAI's** AGENTS.md

Platinum members include AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI ([Linux Foundation press](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)) **[OFFICIAL]**. By April 2026 AAIF reports 170+ member organizations and AGENTS.md adoption in "60,000+ open-source projects" (a figure cited consistently across the AAIF page, agents.md homepage, and ecosystem coverage from [AI Magazine](https://aimagazine.com/news/one-rule-for-all-agents-linux-foundation-launches-aaif) **[PRAC]**).

This matters for Momentum's deployment story: AGENTS.md is no longer a vendor standard — it is governed under the same neutral umbrella as MCP. Betting on it for cross-tool context distribution carries less platform-risk than tool-specific files.

## Tools That Consume AGENTS.md

Verified consumers as of April 2026 (with primary-source citations where available):

| Tool | Native? | Precedence Behavior | Source |
|---|---|---|---|
| **OpenAI Codex CLI** | Native (origin) | `AGENTS.override.md` > `AGENTS.md` at global (`~/.codex/`) and project scope; concatenates root-down with later files overriding | [OpenAI Codex docs](https://developers.openai.com/codex/guides/agents-md) **[OFFICIAL]** |
| **Sourcegraph Amp** | Native | `AGENTS.md` primary; `AGENT.md` backward-compat | [agents.md](https://agents.md) **[OFFICIAL]** |
| **OpenCode** | Native | Walks directory upward; falls back to `~/.config/opencode/AGENTS.md` then `~/.claude/CLAUDE.md`. Disable via `OPENCODE_DISABLE_CLAUDE_CODE` env vars | [OpenCode rules docs](https://opencode.ai/docs/rules/) **[OFFICIAL]** |
| **Google Antigravity** | Native (since v1.20.3, 2026-03-05) | 4-tier: System Rules > GEMINI.md > AGENTS.md > `.agent/rules/` | [antigravity.codes guide](https://antigravity.codes/blog/antigravity-agents-md-guide) **[PRAC]** |
| **Gemini CLI** | Configurable | Uses `GEMINI.md` by default; AGENTS.md via `.gemini/settings.json` `contextFileName` | [agents.md](https://agents.md) **[OFFICIAL]** |
| **Cursor** | Native | Reads `AGENTS.md` automatically alongside `.cursor/rules/`. Closest file wins | [Cursor rules docs](https://cursor.com/docs/rules) **[OFFICIAL]** |
| **Windsurf** | Native | Auto-discovered, fed into Rules engine. Root = always-on; subdir = glob `<dir>/**`. Plain Markdown, no frontmatter | [Windsurf AGENTS.md docs](https://docs.windsurf.com/windsurf/cascade/agents-md) **[OFFICIAL]** |
| **Roo Code** | Native | Loaded after mode-specific rules / `.rooignore`, before generic `~/.roo/rules`. Disable via `roo-cline.useAgentRules: false`. Falls back to `AGENT.md` | [Roo Code docs](https://docs.roocode.com/features/custom-instructions) **[OFFICIAL]** |
| **Kilo Code** | Native | Priority: agent prompt > project `kilo.jsonc` instructions > **AGENTS.md** > global instructions > skills. Write-protected | [Kilo Code docs](https://kilo.ai/docs/customize/agents-md) **[OFFICIAL]** |
| **Factory CLI** | Native | Discovery: `./AGENTS.md` > parent dirs to repo root > sub-folder files > `~/.factory/AGENTS.md` | [Factory docs](https://docs.factory.ai/cli/configuration/agents-md) **[OFFICIAL]** |
| **GitLab Duo** | Native | 3-tier: `~/.gitlab/duo/AGENTS.md` (user) + workspace + subdir, all combined | [GitLab Duo docs](https://docs.gitlab.com/user/duo_agent_platform/customize/agents_md/) **[OFFICIAL]** |
| **Aider** | Configured | Add `read: AGENTS.md` to `.aider.conf.yml` | [Aider config docs](https://aider.chat/docs/config/aider_conf.html) **[OFFICIAL]** |
| **GitHub Copilot** | Native (Coding Agent) | Reads AGENTS.md; also uses `.github/copilot-instructions.md` | [GitHub blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) **[OFFICIAL]** |
| **Devin (Cognition)** | Native | Confirmed reader per agents.md tool list **[OFFICIAL]** |
| **JetBrains Junie** | Tool-specific | Uses `.junie/guidelines.md`; AGENTS.md interop community-driven | [devalias gist](https://gist.github.com/0xdevalias/f40bc5a6f84c4c5ad862e314894b2fa6) **[PRAC]** |
| **Continue.dev** | Pending | [Issue #6716](https://github.com/continuedev/continue/issues/6716) marked Done July 2025; verification of full release semantics inconclusive from public thread | **[UNVERIFIED]** |
| **Cline** | Pending | [Issue #5033](https://github.com/cline/cline/issues/5033) and PR #5405 in progress; not officially shipped as of April 2026 | **[PRAC]** |
| **Block Goose** | Native (own dogfood) | Has its own AGENTS.md in repo; consumes per AAIF stewardship | [block/goose AGENTS.md](https://github.com/block/goose/blob/main/AGENTS.md) **[OFFICIAL]** |
| **Claude Code** | **Disputed / Workaround** | See dedicated section below | — |

### Claude Code: The Asymmetric Holdout

Claude Code is the most-watched holdout. The situation as of April 2026:

- **Open feature request [#34235](https://github.com/anthropics/claude-code/issues/34235)** (filed 2026-03-14) requests native AGENTS.md support; labeled `duplicate` / `enhancement` with no Anthropic resolution comment **[OFFICIAL — issue tracker]**.
- The widely-cited workaround across the ecosystem ([deployhq guide](https://www.deployhq.com/blog/ai-coding-config-files-guide), [hivetrail](https://hivetrail.com/blog/agents-md-vs-claude-md-cross-tool-standard), [aiengineerguide TIL](https://aiengineerguide.com/til/how-to-use-agents-md-in-claude-code/)) **[PRAC]** is to put `@AGENTS.md` inside `CLAUDE.md`, leveraging Claude Code's `@`-import syntax. This is the **pattern that `create-next-app` ships by default** (see "Tools That Emit" below).
- Some sources state Claude Code "reads AGENTS.md as a fallback if no CLAUDE.md is found" ([deployhq](https://www.deployhq.com/blog/ai-coding-config-files-guide), [hivetrail](https://hivetrail.com/blog/agents-md-vs-claude-md-cross-tool-standard)) **[PRAC]**, but this contradicts the open issue #34235. The most defensible interpretation: **native AGENTS.md support is not officially documented by Anthropic; the `@AGENTS.md` import remains the practical answer.**

## Tools That Emit AGENTS.md

This is the question with the most direct relevance to Momentum: who actually generates these files?

### Frameworks and Scaffolding

- **Next.js / `create-next-app`** is the most prominent emitter. Per [Next.js AI Agents guide](https://nextjs.org/docs/app/guides/ai-agents) (last updated 2026-04-23) **[OFFICIAL]**: "create-next-app generates AGENTS.md and CLAUDE.md automatically" since v16.2. Users can opt out with `--no-agents-md`. The emitted AGENTS.md is intentionally minimal:

  ```md
  <!-- BEGIN:nextjs-agent-rules -->
  # Next.js: ALWAYS read docs before coding
  Before any Next.js work, find and read the relevant doc in `node_modules/next/dist/docs/`.
  Your training data is outdated — the docs are the source of truth.
  <!-- END:nextjs-agent-rules -->
  ```

  Note the `BEGIN:`/`END:` comment markers — a managed-section pattern that lets the tool update its block without clobbering user content. The companion `CLAUDE.md` contains only `@AGENTS.md`. This is the **reference pattern for tool-emitted AGENTS.md**: emit a delimited tool-managed block, leave space for human authoring outside it.

- **Codemod path:** `npx @next/codemod@latest agents-md` retrofits the same files into existing projects (16.1 and earlier) **[OFFICIAL]**.

### Generator Tools (Ecosystem)

- **agents-md-generator** (Smithery skill) and **dirty-data/agents.md-generator** (LM Studio) — community-maintained generators that scan a repo and produce a starter AGENTS.md **[PRAC]**.
- **DevTk.AI AGENTS.md Generator**, **Gradually.ai builder**, **planetis-m gist starter** — web/CLI generators that produce starter files from project metadata **[PRAC]**.
- **Most coding agents themselves** can scaffold AGENTS.md on request — the agents.md homepage explicitly recommends asking your agent to draft one **[OFFICIAL]**.

### The "Don't Generate" Counter-Movement

Augment Code's [March 2026 guide](https://www.augmentcode.com/guides/how-to-build-agents-md) **[PRAC]** cites an ETH Zurich study finding that **LLM-generated context files reduced task success in 5 of 8 tested settings** while increasing cost 20–23%. Their recommendation: human-curated minimal files, focused on what agents *cannot* discover independently (custom build commands, non-standard tooling, counterintuitive patterns). This is the rising orthodoxy — auto-generation is viewed skeptically by serious practitioners.

## Real-World Examples

### OpenAI Codex (`openai/codex` repo)

The [official Codex AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md) **[OFFICIAL]** is a sophisticated, sectioned file functioning as an executable style guide:

- **Rust/codex-rs** — crate naming, format inlining, sandbox notes, clippy compliance, "Target Rust modules under 500 LoC, excluding tests"
- **The codex-core crate** — explicitly: *"resist adding code to codex-core!"*
- **TUI Style** — ratatui-specific styling, text wrapping
- **Tests** — snapshot tests via `insta`, `pretty_assertions::assert_eq`, integration patterns
- **App-server API** — payload naming (`*Params`/`*Response`), `#[serde(rename_all = "camelCase")]`, RPC method naming

This represents the "comprehensive" end of the AGENTS.md spectrum.

### Apache Airflow (`apache/airflow`)

[Airflow's AGENTS.md](https://github.com/apache/airflow/blob/main/AGENTS.md) **[OFFICIAL]** is structurally similar but emphasizes safety boundaries:

- **Environment & Setup:** *"Never run pytest, python, or airflow commands directly on the host"*
- **Architecture Boundaries:** scheduler must *"never run user code"*; workers must never access metadata DB directly
- **Coding standards:** *"Always format and check Python files with ruff immediately after writing"*
- **Boundaries section:** explicit "what requires approval" vs. "prohibited" classification

### Temporal Java SDK (`temporalio/sdk-java`)

The [Temporal SDK AGENTS.md](https://github.com/temporalio/sdk-java/blob/master/AGENTS.md) **[OFFICIAL]** is more concise (~58 lines) and closer to a contributor quickstart:

- Repository layout (8 modules)
- "Avoid changing public API signatures"
- Build/test gradle commands
- Test conventions (`SDKTestWorkflowRule`)
- Commit message and PR review checklist

### Vercel Next.js (`vercel/next.js`)

The [Next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md) **[OFFICIAL]** is symlinked as `CLAUDE.md`. It covers:

- Monorepo structure (pnpm + Turbopack)
- *"If you are changing Next.js source or integration tests, start `pnpm --filter=next dev` in a separate terminal session"*
- `NEXT_SKIP_ISOLATE=1` performance flags with explicit caveats
- Required HTML PR comment marker: `<!-- NEXT_JS_LLM_PR -->`

### Block Goose (`block/goose`)

[Goose's AGENTS.md](https://github.com/block/goose/blob/main/AGENTS.md) **[OFFICIAL]** focuses on test folders, feature validation via `goose-self-test.yaml`, error handling, provider implementations, and MCP extension patterns — interesting because Goose itself is *also* a consumer of AGENTS.md, so it dogfoods the format.

## Behavior Driven by AGENTS.md

The 2,500-repo GitHub Copilot analysis ([GitHub blog, 2025-11-19](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)) **[OFFICIAL]** identified **six core domains** that successful AGENTS.md files cover:

1. **Commands** (executable: `npm test`, `pytest -v`, `pnpm build`)
2. **Testing** (when, how, what to assert)
3. **Project structure** (where things live)
4. **Code style** (with snippets — *"One real code snippet beats three paragraphs"*)
5. **Git workflow** (commit conventions, PR rules)
6. **Boundaries** (always-do / ask-first / never-do)

The behavior these drive across implementations:

- **Tool selection steering** — Factory's docs **[OFFICIAL]** explicitly state: *"Folder and naming conventions steer tools like `edit_file` and `create_file`."*
- **Plan formation** — Codex and Factory **[OFFICIAL]** treat listed test/build commands as *"part of the execution plan"* — agents will run them after edits and try to fix failures.
- **Hallucination reduction** — Factory cites *"Gotchas and domain vocabulary improve reasoning and reduce hallucinations."*
- **Restraint** — explicit "never commit secrets," "never modify generated files," "ask before adding deps" patterns recur in 2,500-repo analysis.

What AGENTS.md does **not** drive (in the canonical spec):

- **Tool inventory / permissions** — those are tool-specific (`settings.json`, `permissions.allow`).
- **Skill registration** — skills are a separate concept (Claude Code's `.claude/skills/`, Antigravity Agent Skills, OpenAI Codex Skills) with their own SKILL.md files.
- **MCP server configuration** — separate `.mcp.json` / settings files.

This is important for Momentum: AGENTS.md is the *prose-instructions* layer, not the *capability-registration* layer. A multi-tool deployment story still needs separate adapters for skills, agents, hooks, and MCP servers.

## AGENTS.md vs. Tool-Specific Files: How They Coexist

The dominant 2026 pattern across [deployhq](https://www.deployhq.com/blog/ai-coding-config-files-guide), [hivetrail](https://hivetrail.com/blog/agents-md-vs-claude-md-cross-tool-standard), and [Augment](https://www.augmentcode.com/guides/how-to-build-agents-md) **[PRAC]**:

> Start with AGENTS.md. Add tool-specific files **only** when you have instructions that should not leak across tools.

Layering examples observed in the wild:

- **Cursor:** AGENTS.md for cross-tool rules + `.cursor/rules/*.mdc` for Cursor-specific scoped rules with frontmatter (`description`, `globs`, `alwaysApply`, activation modes).
- **Antigravity:** AGENTS.md as foundation + `GEMINI.md` for tool-specific overrides (GEMINI.md wins on conflict).
- **Claude Code:** `CLAUDE.md` containing `@AGENTS.md` import + Claude-specific additions outside the import.
- **Next.js:** managed `BEGIN:nextjs-agent-rules` block in AGENTS.md + freeform user content outside it; `CLAUDE.md` as a one-liner pointer.

The cross-tool standard is **AGENTS.md is the source of truth; tool-specific files are minimal overrides or pointers.**

## Trajectory and Open Questions

### Spec Evolution

The v1.1 proposal ([Issue #135](https://github.com/agentsmd/agents.md/issues/135)) **[OFFICIAL]** is the trajectory to watch. Its big bet — **optional YAML frontmatter for progressive disclosure** — would change the deployment calculus significantly:

```yaml
---
description: RPC service boilerplate
globs: ["**/*.go", "**/*.proto"]
alwaysApply: false
---
```

If this lands, AGENTS.md starts behaving more like Cursor's `.mdc` rules — file-glob-scoped, on-demand. This would let module authors ship a *family* of AGENTS.md files (one per skill / domain) that activate contextually rather than concatenate everything always. As of April 2026, the proposal is still draft; tools are individually shipping their own dialects (Cursor's `.cursor/rules/*.mdc`, JetBrains' `.junie/guidelines.md`).

### Adoption Frontiers

- **Claude Code native support** — the most-asked-for missing piece. Issue #34235 has no resolution; the `@AGENTS.md` workaround is the de-facto answer.
- **Cline / Continue.dev** — both have open feature-request threads (cline #5033, continue #6716), neither has shipped a clearly-documented native implementation as of April 2026 **[UNVERIFIED]**.
- **Schema vs. simplicity** — the AAIF stewardship will likely mediate the "should we add structure?" tension, but no formal RFC process has been published.

### Implication for Momentum

For a multi-agent deployment story, AGENTS.md is the **lowest-friction common denominator** for prose context. Specifically:

- **Emit AGENTS.md as the primary practice-instructions artifact**, with a managed `BEGIN:momentum-rules`/`END:momentum-rules` block (Next.js pattern) so user authoring isn't clobbered.
- **Pair with a tiny `CLAUDE.md` that contains `@AGENTS.md`** to cover Claude Code without duplication.
- **Do NOT depend on AGENTS.md for skill/agent/hook registration** — those need tool-specific adapters (`.claude/`, `~/.codex/`, `.windsurf/`, etc.). AGENTS.md is the prose layer only.
- **Watch v1.1** — if frontmatter-with-globs lands, Momentum could ship per-skill scoped AGENTS.md files instead of one monolith.
- **Be aware of the auto-generation backlash** — Augment/ETH evidence suggests human-curated minimal files outperform LLM-generated comprehensive ones. A Momentum scaffolder should generate a *minimum viable* AGENTS.md with `BEGIN`/`END` markers, not a wall of guesses.

## Sources

### Primary / Official
- [agents.md (canonical spec site)](https://agents.md)
- [agentsmd/agents.md GitHub repo](https://github.com/agentsmd/agents.md)
- [agentsmd/agents.md Issue #10 — Frontmatter support](https://github.com/agentsmd/agents.md/issues/10)
- [agentsmd/agents.md Issue #135 — v1.1 proposal](https://github.com/agentsmd/agents.md/issues/135)
- [OpenAI Codex Custom Instructions docs](https://developers.openai.com/codex/guides/agents-md)
- [openai/codex AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md)
- [Linux Foundation AAIF announcement (Dec 9 2025)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [OpenCode rules documentation](https://opencode.ai/docs/rules/)
- [Windsurf AGENTS.md docs](https://docs.windsurf.com/windsurf/cascade/agents-md)
- [Roo Code Custom Instructions docs](https://docs.roocode.com/features/custom-instructions)
- [Kilo Code AGENTS.md docs](https://kilo.ai/docs/customize/agents-md)
- [Factory CLI AGENTS.md docs](https://docs.factory.ai/cli/configuration/agents-md)
- [GitLab Duo AGENTS.md customization](https://docs.gitlab.com/user/duo_agent_platform/customize/agents_md/)
- [Cursor Rules docs](https://cursor.com/docs/rules)
- [Aider YAML config docs](https://aider.chat/docs/config/aider_conf.html)
- [Next.js AI Agents guide (2026-04-23)](https://nextjs.org/docs/app/guides/ai-agents)
- [vercel/next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md)
- [apache/airflow AGENTS.md](https://github.com/apache/airflow/blob/main/AGENTS.md)
- [temporalio/sdk-java AGENTS.md](https://github.com/temporalio/sdk-java/blob/master/AGENTS.md)
- [block/goose AGENTS.md](https://github.com/block/goose/blob/main/AGENTS.md)
- [GitHub Blog — How to write a great agents.md (2025-11-19)](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [anthropics/claude-code Issue #34235](https://github.com/anthropics/claude-code/issues/34235)
- [continuedev/continue Issue #6716](https://github.com/continuedev/continue/issues/6716)
- [cline/cline Issue #5033](https://github.com/cline/cline/issues/5033)

### Practitioner / Community
- [Augment Code — How to Build Your AGENTS.md (2026-03-31)](https://www.augmentcode.com/guides/how-to-build-agents-md)
- [Antigravity AGENTS.md guide](https://antigravity.codes/blog/antigravity-agents-md-guide)
- [DeployHQ — CLAUDE.md, AGENTS.md & Copilot Instructions guide](https://www.deployhq.com/blog/ai-coding-config-files-guide)
- [Hivetrail — AGENTS.md vs CLAUDE.md](https://hivetrail.com/blog/agents-md-vs-claude-md-cross-tool-standard)
- [aiengineerguide — How to use AGENTS.md in Claude Code (2025-10-27)](https://aiengineerguide.com/til/how-to-use-agents-md-in-claude-code/)
- [DeepWiki — AGENTS.md Format Documentation](https://deepwiki.com/openai/agents.md/5-agents.md-format-documentation)
- [Ischca/awesome-agents-md GitHub repo](https://github.com/Ischca/awesome-agents-md)
- [devalias gist — AI Agent Rule/Instruction file notes](https://gist.github.com/0xdevalias/f40bc5a6f84c4c5ad862e314894b2fa6)
- [AI Magazine — Linux Foundation launches AAIF](https://aimagazine.com/news/one-rule-for-all-agents-linux-foundation-launches-aaif)
- [Datadog Frontend Dev — Steering AI Agents in Monorepos with AGENTS.md](https://dev.to/datadog-frontend-dev/steering-ai-agents-in-monorepos-with-agentsmd-13g0)
