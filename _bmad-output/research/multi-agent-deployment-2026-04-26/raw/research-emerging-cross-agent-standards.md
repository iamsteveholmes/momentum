---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Emerging cross-agent standards (April 2026 trajectory) — ACP, Skills.sh, MCP-as-distribution, AGENTS.md ecosystem, etc.: what's authorable today vs. consume-only, 6-month trajectory."
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
---

# Emerging Cross-Agent Standards — April 2026 Trajectory

## TL;DR — The Safest Bets Right Now

For a practice module like Momentum to publish *once* and have *most conformant agents* consume it today, the unambiguous bet is the **Agent Skills open standard (`SKILL.md`)** for procedural knowledge plus **`AGENTS.md`** for repo-level guidance. Both are author-side standards — practice authors write plain markdown with minimal frontmatter and 30+ agents read it without translation. Everything else (ACP, MCP-as-skills-distribution, plugin marketplaces) is either consume-only from the practice author's viewpoint, vendor-flavored, or still in flight. A second-tier bet is the **Claude-Code plugin manifest (`.claude-plugin/marketplace.json`)** which `npx skills` and Cursor have adopted as a *de facto* secondary index over `SKILL.md` directories — meaning a practice authored against that schema gets multi-agent reach essentially for free.

---

## 1. ACP — Agent Client Protocol (Zed + JetBrains)

### What is it?
ACP is a **JSON-RPC 2.0 over stdio protocol** that standardizes the wire interface between an editor (the *client*) and a coding agent (the *server*). It is explicitly modeled on LSP — "the LSP moment for AI coding agents" — and is co-stewarded by Zed Industries and JetBrains. **[OFFICIAL]** ([zed.dev/acp](https://zed.dev/acp), [jetbrains.com/acp](https://www.jetbrains.com/acp/))

### Spec, version, repos
- Spec repo: `agentclientprotocol/agent-client-protocol`, latest release **v0.12.2 on 2026-04-23**. **[OFFICIAL]** ([github.com/agentclientprotocol/agent-client-protocol](https://github.com/agentclientprotocol/agent-client-protocol))
- Apache-2.0 license, 41 releases shipped, active issue tracker.
- Official SDKs: **Rust, TypeScript, Python, Java, Kotlin** under `agentclientprotocol` GitHub org. **[OFFICIAL]** ([github.com/agentclientprotocol](https://github.com/agentclientprotocol))
- npm: `@agentclientprotocol/sdk` exports both `AgentSideConnection` and `ClientSideConnection`. **[OFFICIAL]** ([npmjs.com/package/@agentclientprotocol/sdk](https://www.npmjs.com/package/@agentclientprotocol/sdk))

### Is this consumer-only? — **NO. The user's prior assumption was wrong.**
ACP has *both sides* of the protocol publicly documented and SDK-supported. The `AgentSideConnection` class in the TypeScript SDK is the explicit hook for building an agent backend that any ACP client (Zed, JetBrains AI Assistant, Kiro, OpenCode) can drive. **[OFFICIAL]** ([agentclientprotocol.com/libraries/typescript](https://agentclientprotocol.com/libraries/typescript))

The **ACP Registry**, launched January 2026, lists production agents that already implement the agent side: Claude Code, Codex CLI, GitHub Copilot CLI, OpenCode, Gemini CLI, Cline, and "many others." **[OFFICIAL]** ([blog.jetbrains.com — ACP Agent Registry Is Live](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/), [zed.dev/blog/acp-registry](https://zed.dev/blog/acp-registry))

### Who consumes
- Zed (built-in)
- JetBrains AI Assistant across IntelliJ IDEA, PyCharm, WebStorm, etc. **[OFFICIAL]** ([jetbrains.com/help/ai-assistant/acp.html](https://www.jetbrains.com/help/ai-assistant/acp.html))
- OpenCode **[OFFICIAL]** ([opencode.ai/docs/acp/](https://opencode.ai/docs/acp/))
- Kiro CLI **[OFFICIAL]** ([kiro.dev/docs/cli/acp/](https://kiro.dev/docs/cli/acp/))

### What can a practice author publish for ACP?
**Almost nothing directly.** ACP is a wire protocol between a runtime agent process and a host editor. It standardizes session lifecycle, multi-file edits, tool approvals, streaming results — *not* skills, prompts, or rules. A practice module is a bag of *content* (skills, rules, hooks, workflows). ACP cares about how an agent *talks to an editor*, not what corpus the agent loads.

### Gaps
- No content surface in the protocol — no `skills/list`, no rule injection, no hook spec.
- The agent process is responsible for loading its own context. So "ACP agent + Momentum" still means Momentum has to bind into the underlying agent (e.g., Claude Code, Gemini CLI) the same way it would without ACP.

### 6-month trajectory
ACP will likely add a **resource/context surface** so editors can hand workspace state and user-selected files to agents in a standard way (this is implied by "ACP + Deep Agents" article from JetBrains, April 2026). **[OFFICIAL]** ([blog.jetbrains.com — Using ACP + Deep Agents](https://blog.jetbrains.com/ai/2026/04/using-acp-deep-agents-to-demystify-modern-software-engineering/)). It will *not* become a skills-distribution standard — that role has been ceded to Agent Skills + skills.sh.

---

## 2. Agent Skills (SKILL.md) — The De Facto Cross-Agent Skill Format

### What is it?
A spec, governed at **agentskills.io**, originally drafted by Anthropic and released open in **December 2025**. A skill is a directory containing a `SKILL.md` file with YAML frontmatter and Markdown body. **[OFFICIAL]** ([agentskills.io/specification](https://agentskills.io/specification))

### The complete frontmatter schema (verbatim from spec, April 2026)

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | Max 64 chars, lowercase `[a-z0-9-]`, no leading/trailing/consecutive hyphens, must match parent dir name |
| `description` | Yes | 1–1024 chars, must explain what + when |
| `license` | No | License name or filename |
| `compatibility` | No | Max 500 chars; environment requirements |
| `metadata` | No | Arbitrary string→string map |
| `allowed-tools` | No | Space-separated pre-approved tools (experimental) |

Standard subdirectories: `scripts/`, `references/`, `assets/`. Progressive-disclosure model: ~100 tokens of metadata loaded at startup, full `SKILL.md` (<5000 tokens recommended) loaded on activation, scripts/refs/assets pulled on demand. **[OFFICIAL]** ([agentskills.io/specification](https://agentskills.io/specification))

### Governance
Currently sits at **agentskills.io / github.com/agentskills/agentskills**, *not yet* under the Linux Foundation's Agentic AI Foundation. AAIF (formed December 9 2025) holds MCP, Goose, and AGENTS.md but **Agent Skills was deliberately not included** in the founding contributions — long-term stewardship is open. **[OFFICIAL]** ([linuxfoundation.org press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation), [aaif.io](https://aaif.io/)) **[PRAC]** ([unite.ai analysis](https://www.unite.ai/anthropic-opens-agent-skills-standard-continuing-its-pattern-of-building-industry-infrastructure/))

### Adoption (April 2026)
The agentskills.io client showcase lists **38 agent products** consuming the format, including: Anthropic Claude / Claude Code, OpenAI Codex / Codex CLI, Google Gemini CLI, GitHub Copilot, VS Code, Cursor, OpenCode, OpenHands, Goose, JetBrains Junie, Roo Code, Factory, Amp, Letta, Kiro, Snowflake Cortex Code, Databricks Genie Code, Mistral Vibe, Spring AI, Laravel Boost, and more. **[OFFICIAL]** ([agentskills.io](https://agentskills.io))

OpenAI confirmed adoption December 12 2025 and ships skill loading in Codex CLI experimental. **[OFFICIAL]** ([developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)) **[PRAC]** ([Simon Willison — OpenAI are quietly adopting skills](https://simonwillison.net/2025/Dec/12/openai-skills/))

### Per-agent disk locations (the bit a practice installer needs)
- Claude Code: `.claude/skills/<name>/` and `~/.claude/skills/<name>/` **[OFFICIAL]** ([code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills))
- OpenAI Codex: `.agents/skills/`, `$REPO_ROOT/.agents/skills/`, `$HOME/.agents/skills/`, `/etc/codex/skills/` **[OFFICIAL]** ([developers.openai.com/codex/skills](https://developers.openai.com/codex/skills))
- Gemini CLI: `.gemini/skills/` or `.agents/skills/` (workspace), `~/.gemini/skills/` or `~/.agents/skills/` (user), extension-bundled **[OFFICIAL]** ([geminicli.com/docs/cli/skills/](https://geminicli.com/docs/cli/skills/))
- OpenCode: `.opencode/skills/`, `~/.config/opencode/skills/`, plus reads `.claude/skills/` and `.agents/skills/` for compatibility **[OFFICIAL]** ([opencode.ai/docs/skills/](https://opencode.ai/docs/skills/))

The **`.agents/skills/` convention** is the emerging neutral default — Codex, Gemini, and OpenCode all read it natively. **[OFFICIAL]**

### What can a practice author publish?
A directory tree of `SKILL.md` files. That single artifact is consumed unmodified by ~38 agents. This is the single most authorable, most portable practice deliverable in April 2026.

### Gaps
- **Hooks, slash commands, subagents, rules** are *not* part of the spec. Skills only cover instruction-bundle activation. Anything event-driven (Claude Code hooks, Cursor rules) requires per-agent escapes.
- `allowed-tools` is marked experimental — agents handle it inconsistently.
- No standard for skill *dependencies* (skill A requires skill B).
- No spec version field in frontmatter — implicit versioning only.

### 6-month trajectory
- Likely formal donation to AAIF or a dedicated governance body by Q3 2026 (Anthropic has signaled willingness; AAIF is the obvious home given MCP precedent). **[UNVERIFIED]**
- Spec v1.1 likely to add: dependency declarations, optional `version` field, normalize `allowed-tools`. **[UNVERIFIED]**
- `.agents/skills/` will likely become the canonical neutral location; `.claude/skills/`, `.gemini/skills/` etc. remain for backward compat.

---

## 3. AGENTS.md — Repo-Level Agent Guidance

### What is it?
A plain-Markdown file at repository root telling AI coding agents how to build, test, and contribute to the project. **No frontmatter, no JSON-LD, no schema** — deliberately minimal. **[OFFICIAL]** ([agents.md](https://agents.md/))

### Governance
Donated to **Linux Foundation / Agentic AI Foundation (AAIF)** on December 9 2025 alongside MCP and Goose. Formalized August 2025 by OpenAI, Google, Cursor, Factory, Sourcegraph. **[OFFICIAL]** ([linuxfoundation.org press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation), [openai.com/index/agentic-ai-foundation](https://openai.com/index/agentic-ai-foundation/))

### Adoption (April 2026)
- **60,000+ open-source projects** use AGENTS.md **[OFFICIAL]** ([agents.md](https://agents.md/))
- Native readers: OpenAI Codex, GitHub Copilot, Cursor, VS Code, Aider, Factory, Devin, Windsurf, JetBrains Junie, Google Jules + Gemini, Amp, Zed, RooCode, Semgrep, UiPath, Anthropic Claude. **[OFFICIAL]**
- Empirically: developer-written AGENTS.md improves task success rates by ~4% and reduces agent bugs 35–55% on rich files. **[PRAC]** ([Atlan guide](https://atlan.com/know/how-to-write-agents-md/))

### Nested precedence
For monorepos, agents read the closest AGENTS.md walking up the directory tree (LSP-style). **[OFFICIAL]**

### What can a practice author publish?
A single `AGENTS.md` plus optional nested files. Consumed by every major agent without translation. Limit: it's freeform prose — no machine-checkable structure.

### Gaps
- No spec for sections — different consumers privilege different content.
- No way to declare *behaviors* (hooks, lifecycle, sandboxing) — only static instructions.
- Doesn't replace skills; complements them.

### 6-month trajectory
- Possible structured-section convention (build/test/style/security headings) standardized via AAIF. **[UNVERIFIED]**
- Will remain consume-by-everyone, author-once. Stable bet.

---

## 4. MCP as Skill Distribution Channel

### Status: **Proposed and rejected, alternative still in flight.**

### The proposal that got shut down
**SEP-2076** — "Agent Skills as a First-Class MCP Primitive" — proposed adding `skills/list`, `skills/get`, a `skills` server capability, and `notifications/skills/list_changed`. **Closed without merging on 2026-02-24.** Author signaled preference for a different approach. **[OFFICIAL]** ([github.com/modelcontextprotocol/modelcontextprotocol#2076](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2076))

### What's actually happening
- The "Skills Over MCP Working Group" is exploring **skills exposed as Resources** under a `skill://` URI scheme. Experimental; no merged spec. **[OFFICIAL]** ([modelcontextprotocol blog 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/))
- The 2026 official MCP roadmap **does not list skills as a 2026 priority** — focus is transport scalability, agent communication (Tasks primitive), governance, enterprise readiness. **[OFFICIAL]**
- Community projects exist as bridges: `agentskills-mcp` (zouyingcao) wraps Anthropic-format skills as MCP servers; `mcpmarket.com/server/skills` lists skill-bundle servers. **[PRAC]** ([github.com/zouyingcao/agentskills-mcp](https://github.com/zouyingcao/agentskills-mcp))

### MCP Prompts capability — does it serve as a skills equivalent?
The MCP **Prompts primitive** does exist and is supported by most MCP servers — it lets a server expose reusable prompt templates. But: it is *not* progressive disclosure (server returns full prompt on `prompts/get`), has no metadata for "when to use", and isn't surfaced as discoverable capability lists in most clients the way skills are. **[OFFICIAL]** ([modelcontextprotocol.info/docs/concepts/prompts](https://modelcontextprotocol.info/docs/concepts/prompts/)) Prompts ≠ skills.

### What can a practice author publish today?
- **Tools and resources via an MCP server** — yes, mature, high-portability.
- **Prompts via MCP** — possible but rarely surfaced in coding-agent UIs.
- **Skills via MCP** — only via experimental community wrappers; not a stable cross-agent channel.

### Gaps
- No standard skill primitive merged.
- The "MCP server with prompts capability" path is supported by Claude Code and a handful of others, but not a substitute for the SKILL.md ecosystem.

### 6-month trajectory
A skills-as-resources approach may land in MCP **2026-Q4 spec revision** at earliest — the working group is exploratory. The likely steady state through Oct 2026: MCP for tools/resources, Agent Skills for procedural knowledge, no convergence of the two surfaces. **[UNVERIFIED]**

---

## 5. skills.sh — The Vercel-Run Skills Index and Installer

### What is it?
A **CLI installer + public directory + leaderboard** for Agent Skills, launched by **Vercel-Labs on 2026-01-20**. **[OFFICIAL]** ([vercel.com/changelog/introducing-skills](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem), [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills), [skills.sh](https://skills.sh/))

### Authoring
Skills.sh does **not introduce a new format**. It indexes Agent Skills (SKILL.md per the open standard) and `.claude-plugin/marketplace.json` declarations from any GitHub repo. Listing on skills.sh is automatic via install telemetry — no submission flow. **[OFFICIAL]**

### CLI surface
```
npx skills add <owner/repo>      # install from GitHub
npx skills add <git-url>
npx skills add <local-path>
npx skills list
npx skills find                  # interactive search
npx skills update
npx skills remove
npx skills init                  # scaffold a new skill
```
Flags: `--list`, `--skill <name>`, `-a <agent>`, `--all`, `-y`, `-g`. **[OFFICIAL]** ([github.com/vercel-labs/skills](https://github.com/vercel-labs/skills))

### Cross-agent installation behavior
The CLI **detects installed agents** on the dev's machine and **symlinks** the canonical skill directory into each agent's expected path (e.g., `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`). It does **not transform format** — this works precisely because the underlying SKILL.md is portable. Agent-specific features (e.g., `context: fork` Claude-only fields) are preserved as-is and ignored by other agents. **[OFFICIAL]**

### What can a practice author publish?
- A GitHub repo with `SKILL.md` files (and optionally `.claude-plugin/marketplace.json`).
- Users install with `npx skills add <yourorg>/<yourrepo>`.
- Auto-listed on skills.sh leaderboard once installs happen.

### Adoption snapshot
- **350,000+ skill packages** indexed within ~2 months of launch. **[PRAC]** ([virtualuncle.com](https://virtualuncle.com/agent-skills-marketplace-skills-sh-2026/))
- Vercel, Prisma, Supabase, Stripe, Remotion, Coinbase, Microsoft shipped official skills before end of Q1 2026. **[PRAC]** ([infoq.com/news/2026/02/vercel-agent-skills](https://www.infoq.com/news/2026/02/vercel-agent-skills/))
- Three competing/complementary marketplaces: skills.sh, SkillsMP (skillsmp.com), ClawHub — collective ~490k skills. **[PRAC]** ([Termdock](https://www.termdock.com/en/blog/agent-skills-guide))

### Gaps
- Vercel-controlled, not foundation-stewarded. Long-term neutrality risk.
- No quality signal beyond install count — easy to flood with low-quality packages.
- No skill-version locking (no `package-lock.json` equivalent yet).

### 6-month trajectory
- skills.sh likely the dominant install path through 2026; competing marketplaces (SkillsMP, ClawHub) likely consolidate. **[UNVERIFIED]**
- A version-pinning manifest is highly likely; expect a `skills.lock` or similar by Q3 2026.

---

## 6. OpenAI Agents SDK + Codex CLI Skills

OpenAI **adopted the Anthropic Agent Skills format unchanged** in Codex CLI on 2025-12-15 (experimental). By April 2026, skills-in-Codex is a documented mainstream feature with discovery hierarchy (`.agents/skills/` precedence chain shown above) and a built-in `$skill-creator` / `$skill-installer` UI. **[OFFICIAL]** ([developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)) **[PRAC]** ([Simon Willison](https://simonwillison.net/2025/Dec/12/openai-skills/))

OpenAI also publishes **`openai/skills`** — a Codex skills catalog — as a parallel to `anthropics/skills`. **[OFFICIAL]** ([github.com/openai/skills](https://github.com/openai/skills))

The **Agents SDK itself** (the OpenAI SDK for building agent applications) does not introduce a separate "skill" abstraction — skills here means the same SKILL.md files. Agents-SDK use cases (e.g., OSS-maintenance blog post) load skills via the Codex CLI integration. **[OFFICIAL]** ([developers.openai.com/blog/skills-agents-sdk](https://developers.openai.com/blog/skills-agents-sdk))

There is **no separate "OpenAI Skills" format**.

---

## 7. Google Gemini Extensions and Skills

Gemini CLI's plugin system has two layers:

1. **Gemini CLI Extensions** — package format that bundles **prompts, MCP servers, custom commands, themes, hooks, sub-agents, AND agent skills** into one installable unit. **[OFFICIAL]** ([geminicli.com/docs/extensions](https://geminicli.com/docs/extensions/))
2. **Agent Skills** within an extension or standalone — same SKILL.md format as the cross-agent open standard. **[OFFICIAL]** ([geminicli.com/docs/cli/skills](https://geminicli.com/docs/cli/skills/))

Discovery tiers (Workspace > User > Extension), with `.agents/skills/` taking precedence over `.gemini/skills/` for cross-agent compatibility. **[OFFICIAL]**

### What can a practice author publish for Gemini specifically?
- Skills (SKILL.md) — portable.
- A Gemini Extension package — Gemini-only, lets you bundle hooks/sub-agents/MCP/skills together.

### Gap vs. portability
The skills inside an extension are portable. The extension manifest itself (commands, hooks, sub-agents) is Gemini-CLI-specific and won't load in Codex or Claude Code.

---

## 8. Anthropic Claude Code — Plugins + Skills + Marketplace

The Claude Code stack has three nested concepts:

- **Skill** — `SKILL.md` directory, the cross-agent open-standard format. **[OFFICIAL]** ([code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills))
- **Subagent** — Claude-Code-specific, `agents/` directory in a plugin. **[OFFICIAL]**
- **Plugin** — bundles skills + subagents + hooks + slash commands + MCP servers. Manifest at `.claude-plugin/plugin.json`. **[OFFICIAL]** ([code.claude.com/docs/en/plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces))
- **Marketplace** — `.claude-plugin/marketplace.json` lists plugins from a repo. **[OFFICIAL]**

### marketplace.json fields (April 2026)
Each entry: `name`, `source`, plus optional `description`, `version`, `author`, `category`, `tags`, `strict`, plus all `plugin.json` manifest fields (commands, hooks, subagents). **[OFFICIAL]** ([buildwithclaude.com](https://buildwithclaude.com/), [hesreallyhim/claude-code-json-schema](https://github.com/hesreallyhim/claude-code-json-schema))

### Cross-agent leverage
The `.claude-plugin/marketplace.json` schema is **also read by skills.sh / `npx skills`** as a secondary index. So a practice authored as a Claude Code plugin gets multi-agent reach (skills install on every `npx skills add` target) for the *skill* portion — hooks/subagents/commands stay Claude-only. **[OFFICIAL]** ([github.com/vercel-labs/skills](https://github.com/vercel-labs/skills))

### What can a practice author publish?
- Plugin repo with `SKILL.md` files in `skills/` + `.claude-plugin/marketplace.json` → installs cleanly in Claude Code AND every skills.sh-aware agent.
- Hooks, subagents, slash commands → Claude-only.

### 6-month trajectory
Claude Code plugin manifest is unlikely to become a multi-vendor standard, but its *skills subset* is already cross-agent. Expect Cursor and OpenCode to continue reading the marketplace.json file as a discovery source. **[UNVERIFIED]**

---

## 9. Cursor Plugins (2.5+, Feb 2026)

Cursor 2.5 launched plugins on **2026-02-17**. **[OFFICIAL]** ([cursor.com/blog/marketplace](https://cursor.com/blog/marketplace), [cursor.com/docs/plugins](https://cursor.com/docs/plugins)) Format:

- `.cursor-plugin/` directory with `plugin.json` manifest
- Bundles: MCP servers, skills (`SKILL.md` per open standard), subagents, hooks, rules
- `marketplace.json` at root for plugin marketplaces

Skills inside Cursor plugins follow the open Agent Skills format **unchanged**. The wrapping plugin manifest is Cursor-specific. **[OFFICIAL]** ([cursor.com/docs/context/skills](https://cursor.com/docs/context/skills))

This is structurally identical to Claude Code's plugin architecture — same skills inside, different plugin wrapper outside.

---

## 10. Other / Adjacent Standards

### llms.txt — minor relevance
Plain-markdown summary at `/llms.txt` for crawlers. **No major AI platform reads it as first-class input as of April 2026.** Cursor, Continue, Aider read it when present. Search Engine Land found 8/9 sites saw no traffic change after adoption. **[PRAC]** ([Search Engine Land](https://searchengineland.com), summarized in [aeo.press](https://www.aeo.press/ai/the-state-of-llms-txt-in-2026)) Not a practice-distribution channel.

### .well-known/agents.json
**Does not exist as a recognized standard** as of April 2026. Mentioned in some blog posts as a future possibility; no production implementations.

### OpenAPI / openapi.yaml as agent description
OpenAPI is a **tool-description format**, not a skills/practice format. Agents (Claude Code MCP, Codex tool-use) consume OpenAPI to discover tool calls but it doesn't carry instruction bundles. Out of scope for practice-module distribution.

### SpecKit
Spec-driven development tooling (Speakeasy / Stainless competitors), not a cross-agent skills standard. Tangential.

### Plugin marketplaces beyond Claude/Cursor
- **Continue** — uses its own JSON config; no skill-as-folder format yet.
- **Goose** — under AAIF, MCP-native; no separate skills format, uses MCP extensions.
- **Roo Code** — adopted SKILL.md per agentskills.io showcase.
- **Junie / JetBrains** — adopted SKILL.md, AGENTS.md, and ACP.

---

## Authorable Today vs. Consume-Only — Decision Matrix

| Standard | Author publishes... | Consumed by | Authorable Today? | Stewardship |
|---|---|---|---|---|
| **Agent Skills (SKILL.md)** | Folder of SKILL.md files | 38+ agents (Claude, Codex, Gemini, Cursor, Copilot, OpenCode, Goose, Roo, Junie, etc.) | **YES — strong** | agentskills.io (informal) |
| **AGENTS.md** | Single markdown file at repo root | 20+ agents | **YES — strong** | Linux Foundation / AAIF |
| **`.agents/skills/` convention** | Same SKILL.md, neutral path | Codex, Gemini, OpenCode | **YES — emerging neutral default** | De facto |
| **skills.sh / `npx skills`** | GitHub repo of SKILL.md (no extra config) | Multi-agent installer | **YES — install path** | Vercel-Labs |
| **Claude Code plugin (skills subset)** | `.claude-plugin/marketplace.json` + SKILL.md | Claude Code + skills.sh-aware agents (skills only) | **YES — partial portability** | Anthropic |
| **Claude Code plugin (hooks/subagents/commands)** | hooks.json, agents/, commands/ | Claude Code only | YES but Claude-only | Anthropic |
| **Cursor plugin (full)** | `.cursor-plugin/plugin.json` | Cursor only | YES but Cursor-only | Cursor |
| **Gemini Extension (full)** | Extension manifest | Gemini CLI only | YES but Gemini-only | Google |
| **MCP server (tools/resources)** | MCP server binary or stdio process | Claude, Cursor, OpenAI, Goose, etc. | **YES — for tools, not skills** | LF / AAIF |
| **MCP server (prompts capability)** | Server with prompts/list | Few client UIs surface this | Partial — niche | LF / AAIF |
| **MCP skills primitive** | (SEP-2076 closed) | n/a | **NO — not a standard** | Working group only |
| **ACP agent server** | Run a JSON-RPC server using SDK | Zed, JetBrains AI, OpenCode, Kiro | **AUTHORABLE BUT NOT FOR PRACTICES** — wire protocol, not content | Zed + JetBrains, Apache-2.0 |
| **llms.txt** | /llms.txt at site root | Mostly ignored by major agents | YES but ineffective | Community |
| **.well-known/agents.json** | Not a thing | Not a thing | NO | n/a |

---

## 6-Month Trajectory Summary (April 2026 → October 2026)

1. **Agent Skills consolidates as *the* practice format.** Format is stable; spec v1.1 likely adds dependency declarations and a version field. **[UNVERIFIED]**
2. **`.agents/skills/` becomes the canonical neutral path.** Claude Code likely adds it as a recognized location alongside `.claude/skills/`. **[UNVERIFIED]**
3. **AAIF likely absorbs Agent Skills.** Anthropic donated MCP; donating Skills is the consistent next move. Watch Q3 2026. **[UNVERIFIED]**
4. **skills.sh dominates the install layer**, possibly with a lockfile by Q3.
5. **MCP-as-skills-channel will not ship in 2026.** SEP-2076 is dead; the resource-URI alternative is too early. Practices should not bet on MCP for skill distribution.
6. **ACP grows on the IDE side.** More editors will gain ACP support (likely VS Code via extension). The agent-side SDK becomes more mature, but ACP remains an editor↔agent wire protocol — irrelevant to practice content.
7. **AGENTS.md gains structured-section conventions.** AAIF stewardship will likely produce recommended headings for build/test/style/security but not enforce them.
8. **Plugin manifests stay vendor-flavored.** Hooks, subagents, slash commands will *not* converge across agents in 6 months. Cross-agent practices must accept lossy translation for these features.

### What to bet a practice module on, ranked

1. **SKILL.md** as the universal procedural-knowledge surface — every agent can read it.
2. **AGENTS.md** as the universal repo-guidance surface.
3. **`.claude-plugin/marketplace.json`** as a discovery file (free reach via skills.sh).
4. **Vendor-specific manifests** (Claude Code hooks, Cursor rules, Gemini extensions) for agent-specific automation, generated from a single source of truth in your build pipeline.
5. **Avoid betting on**: MCP skills primitive (dead), ACP for content (out of scope), llms.txt (no real adoption), .well-known/agents.json (not a standard).

---

## Sources

### [OFFICIAL]
- [Agent Skills Specification — agentskills.io](https://agentskills.io/specification)
- [Agent Skills Overview — agentskills.io](https://agentskills.io/)
- [anthropics/skills GitHub repo](https://github.com/anthropics/skills)
- [agentskills/agentskills GitHub repo](https://github.com/agentskills/agentskills)
- [Agent Client Protocol — zed.dev/acp](https://zed.dev/acp)
- [JetBrains ACP — jetbrains.com/acp](https://www.jetbrains.com/acp/)
- [JetBrains AI Assistant ACP docs](https://www.jetbrains.com/help/ai-assistant/acp.html)
- [agentclientprotocol/agent-client-protocol — GitHub](https://github.com/agentclientprotocol/agent-client-protocol)
- [agentclientprotocol/typescript-sdk](https://github.com/agentclientprotocol/typescript-sdk)
- [@agentclientprotocol/sdk on npm](https://www.npmjs.com/package/@agentclientprotocol/sdk)
- [TypeScript SDK docs](https://agentclientprotocol.com/libraries/typescript)
- [ACP Agent Registry Is Live — JetBrains AI Blog](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/)
- [The ACP Registry is Live — Zed Blog](https://zed.dev/blog/acp-registry)
- [Using ACP + Deep Agents — JetBrains AI Blog](https://blog.jetbrains.com/ai/2026/04/using-acp-deep-agents-to-demystify-modern-software-engineering/)
- [OpenCode ACP docs](https://opencode.ai/docs/acp/)
- [Kiro CLI ACP docs](https://kiro.dev/docs/cli/acp/)
- [agents.md homepage](https://agents.md/)
- [Custom instructions with AGENTS.md — OpenAI Codex](https://developers.openai.com/codex/guides/agents-md)
- [Linux Foundation press release — AAIF](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [OpenAI co-founds AAIF](https://openai.com/index/agentic-ai-foundation/)
- [MCP joins AAIF — modelcontextprotocol blog](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/)
- [Anthropic donates MCP](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [AAIF home — aaif.io](https://aaif.io/)
- [Block — AAIF launch](https://block.xyz/inside/block-anthropic-and-openai-launch-the-agentic-ai-foundation)
- [SEP-2076 — Skills as MCP primitive (closed)](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2076)
- [MCP 2026 Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP Prompts concept docs](https://modelcontextprotocol.info/docs/concepts/prompts/)
- [Agent Skills — Codex docs](https://developers.openai.com/codex/skills)
- [Codex CLI docs](https://developers.openai.com/codex/cli)
- [openai/skills GitHub](https://github.com/openai/skills)
- [Using skills to accelerate OSS maintenance — OpenAI](https://developers.openai.com/blog/skills-agents-sdk)
- [Codex Changelog](https://developers.openai.com/codex/changelog)
- [Anthropic Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude API Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [anthropics/skills marketplace.json](https://github.com/anthropics/skills/blob/main/.claude-plugin/marketplace.json)
- [Customize Claude Code with plugins](https://claude.com/blog/claude-code-plugins)
- [Gemini CLI Skills docs](https://geminicli.com/docs/cli/skills/)
- [Gemini CLI Creating Skills](https://geminicli.com/docs/cli/creating-skills/)
- [Gemini CLI Extensions](https://geminicli.com/docs/extensions/)
- [Gemini CLI Skills source — google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md)
- [Vercel changelog — Introducing skills](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)
- [Vercel agent-skills KB](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)
- [Vercel agent-resources skills](https://vercel.com/docs/agent-resources/skills)
- [vercel-labs/skills GitHub](https://github.com/vercel-labs/skills)
- [skills.sh directory](https://skills.sh/)
- [skills npm package](https://www.npmjs.com/package/skills)
- [OpenCode skills docs](https://opencode.ai/docs/skills/)
- [Cursor plugins blog](https://cursor.com/blog/marketplace)
- [Cursor plugins docs](https://cursor.com/docs/plugins)
- [Cursor skills context docs](https://cursor.com/docs/context/skills)
- [cursor/plugins GitHub](https://github.com/cursor/plugins)

### [PRAC]
- [Simon Willison — OpenAI are quietly adopting skills (Dec 2025)](https://simonwillison.net/2025/Dec/12/openai-skills/)
- [Simon Willison Substack — same](https://simonw.substack.com/p/openai-are-quietly-adopting-skills)
- [Atlan — How to Write an AGENTS.md File 2026](https://atlan.com/know/how-to-write-agents-md/)
- [Harness — The Agent-Native Repo](https://www.harness.io/blog/the-agent-native-repo-why-agents-md-is-the-new-standard)
- [Tessl — Rise of agents.md](https://tessl.io/blog/the-rise-of-agents-md-an-open-standard-and-single-source-of-truth-for-ai-coding-agents/)
- [Addo Zhang — AGENTS.md Medium](https://addozhang.medium.com/agents-md-a-new-standard-for-unified-coding-agent-instructions-0635fc5cb759)
- [InfoQ — Vercel introduces Skills.sh](https://www.infoq.com/news/2026/02/vercel-agent-skills/)
- [VirtualUncle — skills.sh guide 2026](https://virtualuncle.com/agent-skills-marketplace-skills-sh-2026/)
- [Termdock — Agent Skills Guide 2026](https://www.termdock.com/en/blog/agent-skills-guide)
- [Toolworthy — skills.sh review](https://www.toolworthy.ai/tool/skills-sh)
- [Unite.ai — Anthropic opens Agent Skills standard](https://www.unite.ai/anthropic-opens-agent-skills-standard-continuing-its-pattern-of-building-industry-infrastructure/)
- [VentureBeat — Anthropic launches enterprise Agent Skills](https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard)
- [Inference.sh — Agent Skills overview](https://inference.sh/blog/skills/agent-skills-overview)
- [Solo.io — AAIF announcement](https://www.solo.io/blog/aaif-announcement-agentgateway)
- [IntuitionLabs — AAIF guide](https://intuitionlabs.ai/articles/agentic-ai-foundation-open-standards)
- [ITECS — Codex CLI skills guide](https://itecsonline.com/post/codex-cli-agent-skills-guide-install-usage-cross-platform-resources-2026)
- [BrightCoding — Claude Skills Marketplace](https://www.blog.brightcoding.dev/2026/04/26/claude-skills-marketplace-the-essential-plugin-hub-for-developers)
- [DeepWiki — anthropics/skills marketplace and plugin system](https://deepwiki.com/anthropics/skills/2.3-marketplace-and-plugin-system)
- [hesreallyhim/claude-code-json-schema](https://github.com/hesreallyhim/claude-code-json-schema)
- [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills)
- [Joost — self-updating agent skills](https://joost.blog/self-updating-agent-skills/)
- [Cra.mr — MCP, Skills, and Agents](https://cra.mr/mcp-skills-and-agents/)
- [Nevo — Skills vs Plugins vs MCPs 2026](https://nevo.systems/blogs/nevo-journal/ai-agent-skill-vs-plugin-vs-mcp)
- [Cosmic JS — MCP vs Skills 2026](https://www.cosmicjs.com/blog/mcp-vs-skills-ai-coding-assistant-integrations-guide)
- [GetKnit — Future of MCP](https://www.getknit.dev/blog/the-future-of-mcp-roadmap-enhancements-and-whats-next)
- [Medium — ACP The LSP Moment](https://thamizhelango.medium.com/agent-client-protocol-acp-the-lsp-moment-for-ai-coding-agents-and-how-jetbrains-and-zed-nailed-e2a42f5defb0)
- [Medium — Mental Model for Claude Code](https://levelup.gitconnected.com/a-mental-model-for-claude-code-skills-subagents-and-plugins-3dea9924bf05)
- [Agensi — Claude Code Plugins vs Skills 2026](https://www.agensi.io/learn/claude-code-plugins-vs-skills-explained)
- [aeo.press — State of llms.txt in 2026](https://www.aeo.press/ai/the-state-of-llms-txt-in-2026)
- [zouyingcao/agentskills-mcp](https://github.com/zouyingcao/agentskills-mcp)
