---
content_origin: claude-code-subagent
date: 2026-04-22
sub_question: "What cross-agent portability patterns, adapters, and tooling actually exist as of April 2026?"
topic: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements — addendum"
---

# Cross-Agent Portability Patterns for AI Coding Agent Practices — April 2026

## Evidence Tags

- **[OFFICIAL]** — Primary source: project repo, maintainer blog, or official spec
- **[PRAC]** — Practitioner report: blog post, case study, dev.to article with identifiable author
- **[UNVERIFIED]** — Aggregator article, commentary, or secondhand claim not confirmed at primary source

## Executive Snapshot

The cross-agent portability story in April 2026 is dominated by **one format (SKILL.md) and two installers (skills.sh / npx skills, and npx antigravity-awesome-skills)**. AGENTS.md is the convergent project-instructions standard, now stewarded by the Agentic AI Foundation under the Linux Foundation. Runtime adapters at the "LiteLLM for agents" level do not exist as general-purpose tools — LiteLLM itself has moved into agent-adjacent territory (A2A protocol, OpenAI Agents SDK compat), but the "normalized coding-agent harness" layer is conspicuously absent. Instead, the portability pattern is: write once in SKILL.md + AGENTS.md, install via a cross-agent CLI, accept that hooks/plugins/subagents are host-specific.

---

## 1. Agent Runtime Adapters — "LiteLLM for Agents"

**Verdict: No general-purpose coding-agent runtime adapter exists.** The closest analogs operate at different layers of the stack.

### 1.1 LiteLLM — Model Gateway, Not Agent Harness **[OFFICIAL]**

- LiteLLM remains a **model-provider gateway** (one OpenAI-format interface to 100+ LLMs), not a coding-agent harness. It can back the OpenAI Agents SDK and Claude Agent SDK as the LLM provider, but it does not translate Claude Code skills → opencode plugins or similar.
- LiteLLM added **A2A (Agent-to-Agent) Protocol** support — invocation endpoints for LangGraph, Vertex AI Agent Engine, Azure AI Foundry, Bedrock AgentCore, Pydantic AI. This is agent-to-agent *invocation*, not harness-to-harness *skill portability*.
- Source: https://docs.litellm.ai/docs/a2a and https://docs.litellm.ai/docs/agent_sdks

### 1.2 Superpowers (obra) — Per-Runtime Bootstrap, Shared Skills **[OFFICIAL] [PRAC]**

Jesse Vincent's Superpowers framework (github.com/obra/superpowers, v5.0.7 as of March 31 2026) is the closest-to-real "cross-agent runtime adapter" in production use. Its approach:

- **Shared skill layer**: one set of SKILL.md files lives in the repo.
- **Per-runtime bootstrap**: separate install scripts and adapter shims for Claude Code, Codex CLI, Cursor, OpenCode, GitHub Copilot CLI, and Gemini CLI. Each shim builds a "translation table" from Claude-native primitives (TodoWrite, Task, Skill tool) to the host's equivalents.
- **Technique for hostless runtimes**: for Codex (no subagents, no plugin system, no hooks), the adapter writes a startup instruction to `~/.codex/AGENTS.md` that tells the agent to shell out to a `superpowers-codex` script for skill discovery. It synthesizes the missing primitives by instruction-injection rather than code.
- Source: https://blog.fsck.com/2025/11/24/Superpowers-for-OpenCode/ and https://blog.fsck.com/2025/10/27/skills-for-openai-codex/

This is **not a unified runtime API** — it's a carefully maintained per-host adapter set. It validates the pattern but also reveals the cost: the maintainer writes and maintains N adapters, and host feature deltas (subagents, plugins, hooks) are mapped by hand.

### 1.3 No LangChain/LlamaIndex/CrewAI Equivalent **[UNVERIFIED]**

No evidence that LangChain, LlamaIndex, or CrewAI has shipped a normalized coding-agent harness wrapper. They remain application-level frameworks for building agents, not portability layers across Claude Code / opencode / Codex CLI.

---

## 2. AGENTS.md Ecosystem

### 2.1 Adoption — 24+ tools, ~60k+ projects **[OFFICIAL]**

From https://agents.md/ (canonical site):

- **Tools adopting AGENTS.md (partial list on agents.md):** OpenAI Codex, Google Jules, Factory, Aider, goose, Zed, Warp, VS Code, Devin, UiPath Autopilot, JetBrains Junie, Cursor, RooCode, Gemini CLI, Phoenix, GitHub Copilot Coding Agent, Windsurf, plus 7+ others — **24 total listed**.
- **GitHub adoption metric:** "over 60k open-source projects" using AGENTS.md (per search on the live site).
- **Origin coalition:** emerged from OpenAI Codex, Amp, Google Jules, Cursor, and Factory.

### 2.2 Stewardship **[OFFICIAL]**

- AGENTS.md is now stewarded by the **Agentic AI Foundation under the Linux Foundation** — confirmed on agents.md landing page.

### 2.3 Formal Spec — Intentionally Minimal **[OFFICIAL]**

- There is **no formal schema**. Quote from agents.md: "AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide."
- **No validation tooling exists for AGENTS.md itself** — no linter, no schema validator.
- The convergence is organic: it's the filename and the location (repo root or `~/.config/opencode/AGENTS.md`) that carry meaning, not a structured schema.

### 2.4 Compatibility Fallback Pattern **[OFFICIAL]**

OpenCode explicitly documents fallback order: `AGENTS.md` → `CLAUDE.md` → `~/.config/opencode/AGENTS.md` → `~/.claude/CLAUDE.md`. This is the pattern most "new" coding agents adopt — read AGENTS.md preferentially, fall back to Claude-native filenames. Source: https://opencode.ai/docs/rules/

---

## 3. Community Installers / Bundlers

### 3.1 Antigravity Awesome Skills — Largest Cross-Compatible Installer **[OFFICIAL]**

- **Repo:** https://github.com/sickn33/antigravity-awesome-skills
- **Install command:** `npx antigravity-awesome-skills`
- **Tool-specific flags:** `--claude`, `--cursor`, `--gemini`, `--codex`, `--antigravity`, `--kiro`, `--path ./custom`
- **Filter flags:** `--category`, `--risk safe,none`, `--tags`
- **Scale:** 1,431+ skills (April 2026). Officially supports Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, Kiro CLI/IDE, GitHub Copilot (manual), OpenCode, AdaL CLI.
- **Bundle concept:** curated skill recommendations for roles (Essentials, Full-Stack, Security, DevOps & Cloud, QA & Testing, OSS Maintainer). Bundles are *recommendations*, not separate installs.
- **Repo structure:** `skills/` (1,431+ SKILL.md files), `.agents/plugins/`, `.claude-plugin/`, `skills_index.json`, `CATALOG.md`, `data/workflows.json`, `apps/web-app/`.

### 3.2 Superpowers (obra) — Curated Methodology Bundle **[OFFICIAL]**

- **Repo:** https://github.com/obra/superpowers, **v5.0.7** (March 31 2026)
- **OpenCode install:** tell OpenCode to "Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md" — or single-line opencode.json: `{ "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"] }`
- **Codex install:** paste instruction telling Codex to fetch `.codex/INSTALL.md` from the repo.
- **Claude Code install:** via official Anthropic plugin marketplace or Superpowers' own marketplace.
- **Positioning:** not just a skill pack — a "software development methodology" (brainstorming → writing-plans → execution), with opinionated workflow skills.

### 3.3 Skills.sh / vercel-labs/skills — Vercel's Package Manager **[OFFICIAL]**

- **Launch:** January 20, 2026 by Vercel.
- **Repo:** https://github.com/vercel-labs/skills
- **Directory:** https://skills.sh (directory + leaderboard)
- **Install:** `npx skills add <github-org>/<package>` (e.g. `npx skills add vercel-labs/agent-skills`)
- **Management:** `npx skills find "<query>"`, `npx skills check`, `npx skills update`
- **Publish model:** push a GitHub repo containing `SKILL.md` files; users install via CLI.
- **Supported agents (confirmed 18 on the launch page):** amp, antigravity, claude-code, clawdbot, codex, cursor, droid, gemini, gemini-cli, github-copilot, goose, kilo, kiro-cli, opencode, roo, trae, windsurf (plus one variant — some sources quote 19).
- **Adoption metrics [UNVERIFIED aggregator numbers]:** 20k installs in first 6 hours of top skill; 351,000+ packages by early March 2026; Stripe, Prisma, Supabase, Coinbase, Remotion, Microsoft shipped official skills in Q1 2026.

### 3.4 n-skills — Curated Plugin Marketplace **[OFFICIAL]**

- **Repo:** https://github.com/numman-ali/n-skills
- "Curated plugin marketplace for AI agents - works with Claude Code, Codex, and openskills"
- Uses SKILL.md as universal format, AGENTS.md as universal discovery file, openskills as universal installer.

### 3.5 opencode-marketplace (NikiforovAll) — CLI Plugin Installer for OpenCode **[OFFICIAL]**

- **Repo:** https://github.com/NikiforovAll/opencode-marketplace
- **v0.5.0** (February 6, 2026), 39 commits — actively developed, not yet 1.0.
- **Install:** `bunx opencode-marketplace` or `bun install -g opencode-marketplace`
- **Discovery convention:** `.opencode/*` → `.claude/*` → `./command/` (tries OpenCode-native paths, then falls back to Claude-native paths). Components get namespaced prefixes (`my-plugin--reflect.md`), tracked in `~/.config/opencode/plugins/installed.json`.

### 3.6 Other Community Bundlers **[OFFICIAL]**

- **awesome-opencode/awesome-opencode** — curated list (not an installer).
- **malhashemi/opencode-skills** — skill pack.
- **zenobi-us/opencode-skillful** — "Allow your opencode agents to lazy load prompts on demand."
- **zenobi-us/opencode-plugin-template** — GitHub template for generating new OpenCode plugins (fork-and-fill pattern, primary scaffolding).

---

## 4. Distribution Patterns — What's Actually Working

### 4.1 `npx <name>` — The Dominant Install Verb **[OFFICIAL] [PRAC]**

The single clearest signal: **every serious cross-agent installer uses `npx` as the entry point.**

- `npx skills add <pkg>` (Vercel)
- `npx antigravity-awesome-skills` (sickn33)
- `npx claude2codex migrate` (TreeSoop)
- `npx skills` also aliased to openskills

The `npx` pattern wins because: (a) no global install required, (b) developers trust npm as a distribution channel, (c) the CLI can write to any per-agent directory (`~/.claude/skills/`, `~/.codex/skills/`, `~/.config/opencode/skills/`) with one invocation.

### 4.2 Fetch-and-Follow Bootstrap **[OFFICIAL]**

For agents without a plugin system (notably Codex), the pattern is:
- Tell the agent "Fetch `<URL>/INSTALL.md` and follow the instructions."
- The INSTALL.md script writes scripts into `~/.codex/` or similar and appends a block to `~/.codex/AGENTS.md`.

This is the **Superpowers Codex pattern** — instruction-level install via a fetched markdown playbook.

### 4.3 GitHub Template "Fork This Repo" **[OFFICIAL]**

- `zenobi-us/opencode-plugin-template` is a GitHub template repository — the fork-and-fill pattern for scaffolding new plugins.
- The Superpowers repo itself is frequently cloned as a template by teams who want to start from a known-good skill set.

### 4.4 Claude Code Plugin Marketplace (Private Enterprise) **[OFFICIAL]**

- **Anthropic official directory** (github.com/anthropics/claude-plugins-official) — 55+ curated plugins.
- **Community marketplaces** (wshobson/agents etc.) — 72+ plugins.
- **Private enterprise marketplaces**: enterprise admins can host `marketplace.json` registries with per-user provisioning, auto-install, visibility restrictions. This is the closest thing to "MDM for agent skills."
- **Source formats supported in marketplace.json:** GitHub repos, git URLs, local paths, npm packages.
- **Security gap [PRAC]:** "There's no binary signing for Claude plugins in 2026, and plugins run fully trusted code inside developers' sessions, with no sandboxing." — https://www.mpt.solutions/your-claude-plugin-marketplace-needs-more-than-a-git-repo/

### 4.5 OpenCode: plugin in opencode.json + plugins from npm **[OFFICIAL]**

- OpenCode supports `"plugin": ["<git-url>"]` in opencode.json for one-line installs.
- Plugins can also be loaded from npm via the plugin option in config.
- Plugin directory convention: `.opencode/plugins/` (project) and `~/.config/opencode/plugins/` (global).

---

## 5. Cross-Agent Migration Case Studies — Practitioner Reports

### 5.1 obra / Jesse Vincent — "Porting Skills to OpenAI Codex" **[OFFICIAL] [PRAC]**

- URL: https://blog.fsck.com/2025/10/27/skills-for-openai-codex/
- Friction: **Codex's literal interpretation**. Quote: "Codex is very, very literal. If you say 'Any time you are running through a process, you must use your `TodoWrite` tool...it will not rest until it finds the `TodoWrite` tool.'"
- **Translation table built:**
  - `TodoWrite` → `update_plan`
  - `Task` tool (subagents) → manual workaround (no subagent primitive)
  - `Skill` tool → `~/.codex/superpowers/.codex/superpowers-codex use-skill` (custom script)
  - File operations map directly.
- **Structural gaps:** Codex has no plugin system, no hooks, no subagents — everything via bootstrap instruction injection.

### 5.2 obra — "Superpowers (and Skills) for OpenCode" **[OFFICIAL] [PRAC]**

- URL: https://blog.fsck.com/2025/11/24/Superpowers-for-OpenCode/
- Tool map: TodoWrite → update_plan, Task → @mention subagents, Skill → custom `use_skill` tool registered by the plugin.
- OpenCode provides hooks (unlike Codex), so Superpowers bootstraps automatically at session start and after compact operations.
- OpenCode "does not (yet) have native support for skills" — the plugin registers `use_skill` and `find_skills` as custom tools.

### 5.3 Thomas Wiegold — "I Switched From Claude Code to OpenCode" **[PRAC]**

- URL: https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/
- Practitioner narrative; migration friction and what worked. (Full text not fetched — title and URL confirm existence as a primary report.)

### 5.4 devashish.me — "Migrating from Claude Code to OpenCode" **[PRAC]**

- URL: https://www.devashish.me/p/migrating-from-claude-code-to-opencode
- Developer migrated all agents, skills, configs, MCPs to OpenCode over a week. Reported success.

### 5.5 Richard Hightower — "Claude Code Agents to OpenCode Agents" **[PRAC]**

- URL: https://gist.github.com/RichardHightower/827c4b655f894a1dd2d14b15be6a33c0
- Migration of 12 specialized agents; documented as "a single intensive day" effort; produced a framework.

### 5.6 shinpr — "Same Framework, Different Engine: Porting AI Coding Workflows from Claude Code to Codex CLI" **[PRAC]**

- URL: https://dev.to/shinpr/same-framework-different-engine-porting-ai-coding-workflows-from-claude-code-to-codex-cli-n3p
- Sub-agent workflow framework ported once Codex shipped subagent support; "took only an afternoon."

### 5.7 SmrutAI/opencode-migration — Migration Playbook Repo **[OFFICIAL]**

- URL: https://github.com/SmrutAI/opencode-migration
- Includes an installable OpenCode skill (`claude-migration-orchestrator`) that inventories Claude commands/agents/skills, creates OpenCode wrappers + symlinks, generates migration reports.
- **Does NOT translate hooks.json or settings.json** — scope is commands, agents, skills only.
- Install: `mkdir -p ~/.config/opencode/skill/claude-migration-orchestrator && cp claude-migration-orchestrator.md ~/.config/opencode/skill/claude-migration-orchestrator/SKILL.md`

---

## 6. Hook / Settings Translation Tools

### 6.1 claude2codex — Config Migrator **[OFFICIAL] [PRAC]**

The **only tool found** that translates Claude Code JSON config → another agent's config format.

- URL: https://dev.to/treesoop/claude2codex-migrate-claude-code-config-to-openai-codex-in-one-command-jlj
- Posted April 17, 2026 by TreeSoop (Korean AI-native dev agency); MIT licensed.
- **Install:** `npx claude2codex init` / `npx claude2codex migrate --dry-run` / `npx claude2codex migrate`
- **What it translates:**
  - `~/.claude/CLAUDE.md` → `~/.codex/config.md`
  - `~/.claude/settings.json` → `codex.toml`
  - `~/.claude/skills/*.md` → `~/.codex/prompts/*.md`
  - MCP server registrations (JSON → Codex-compatible format)
  - Harness trigger logic (ported with warnings)
- **Fidelity:** author claims "~95% of settings auto-converted and worked in Codex on first try." The remaining 5% surface as warnings in a conflict report.
- **Limitations:** No hooks.json → opencode plugin TS translator exists. This is a gap.

### 6.2 No hooks.json → opencode TypeScript translator found

- Searches for a Claude Code `hooks.json` → opencode plugin TypeScript converter returned no primary projects.
- The structural reason: Claude hooks are declarative JSON with event triggers; opencode plugins are imperative TypeScript modules exporting hook functions. Translation is non-trivial and no one has productized it.
- **Gap / opportunity** — the cleanest translation path for hooks is probably a generator that emits a TS plugin skeleton with TODO stubs, not a full round-trip converter.

---

## 7. Package Registries for Agent Skills

### 7.1 Skills.sh — The De-Facto Agent-Skill Registry **[OFFICIAL]**

- URL: https://skills.sh
- Launched by Vercel January 20, 2026.
- Directory + leaderboard + CLI (`npx skills`).
- Packages are **GitHub-repo-backed** (like Go modules); skills.sh aggregates metadata, downloads, leaderboards.
- **Not a full centralized registry** like npm — there's no separate registry server; GitHub is the backend.

### 7.2 npm — Still a Fallback Registry **[OFFICIAL]**

- `antigravity-awesome-skills` ships via npm (findable at npmjs.com/package/antigravity-awesome-skills — though npm's web UI returned 403 in this session; package exists per search results).
- Many Claude plugins and OpenCode plugins use npm as their distribution channel referenced from marketplace.json.

### 7.3 Skilldex — Academic Proposal **[UNVERIFIED]**

- arxiv.org/html/2604.16911 — "Skilldex: A Package Manager and Registry for Agent Skill Packages with Hierarchical Scope-Based Distribution"
- Node.js 20+ npm package (skilldex-cli / skillpm / spm). TypeScript + Commander + simple-git + Zod.
- Unclear adoption as of April 2026 — appears to be an academic/exploratory proposal rather than a shipped registry.

### 7.4 Agent Skills Spec — Canonical Definition **[OFFICIAL]**

- **Canonical spec:** https://agentskills.io/specification
- **GitHub spec pointer:** https://github.com/anthropics/skills/blob/main/spec/agent-skills-spec.md (redirects to agentskills.io)
- **Released:** December 18, 2025 by Anthropic as an open standard.
- **Adopted by OpenAI** for Codex CLI and ChatGPT (confirmed in multiple sources; same SKILL.md format).

#### SKILL.md Required Fields

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | ≤64 chars, lowercase a-z, digits, hyphens only; no leading/trailing/consecutive hyphens; must match parent dir name |
| `description` | Yes | ≤1024 chars, non-empty, describes what + when to use |
| `license` | No | License name or bundled license file reference |
| `compatibility` | No | ≤500 chars, environment requirements |
| `metadata` | No | Arbitrary key-value map |
| `allowed-tools` | No | Space-separated tools (Experimental) |

#### Progressive-Disclosure Model (canonical)

- **Metadata (~100 tokens):** name + description loaded at startup for all skills
- **Instructions (< 5000 tokens recommended):** SKILL.md body loaded on activation
- **Resources (as needed):** `scripts/`, `references/`, `assets/` loaded only when required

#### Validation Tooling **[OFFICIAL]**

- `skills-ref validate ./my-skill` — reference validator at https://github.com/agentskills/agentskills/tree/main/skills-ref
- This IS a real validator; checks frontmatter + naming conventions.

---

## 8. Viable Patterns for Momentum Cross-Agent Distribution

Ranked by evidence of real-world adoption and success.

### Tier 1 — High Evidence, Low Risk

**1. `npx <package>` installer that writes SKILL.md files to per-agent directories**
- **Evidence:** Antigravity Awesome Skills (1,431 skills, broad agent support), Skills.sh (351k+ packages), claude2codex, openskills.
- **Pattern:** write one SKILL.md per skill, ship an npm package with a CLI that detects the installed agent(s) and copies files to the right directory with optional per-agent shims.
- **Effort for Momentum:** low-to-medium. Convert Momentum's current skill set to the SKILL.md spec (which it largely already matches — frontmatter + markdown body), add a thin CLI wrapper.
- **Momentum-specific wrinkle:** Momentum's hooks.json enforcement (plan-audit, autonomous commits) doesn't fit SKILL.md — needs a separate delivery path per host.

**2. AGENTS.md at repo root as universal project-instructions**
- **Evidence:** 60k+ repos, 24+ tools read it, Linux Foundation stewardship.
- **Pattern:** Momentum ships AGENTS.md (or CLAUDE.md with AGENTS.md symlink) with project conventions.
- **Effort:** trivial. This is the lowest-risk, highest-coverage portability move.

### Tier 2 — Medium Evidence, Some Risk

**3. Per-agent bootstrap adapter (Superpowers pattern)**
- **Evidence:** Superpowers v5.0.7 with 6 supported runtimes; obra has maintained it through multiple Claude Code + OpenCode + Codex revisions.
- **Pattern:** one adapter per host (Claude plugin, OpenCode plugin, Codex AGENTS.md bootstrap, Gemini CLI hook, etc.), shared SKILL.md layer underneath.
- **Effort:** medium-to-high. Each adapter requires host-specific knowledge; 3 hosts ≈ significant ongoing maintenance.
- **When to use:** when Momentum's value depends on primitives the host doesn't provide natively (subagents, hooks, slash commands). The adapter synthesizes those primitives.

**4. GitHub template repository (fork-and-fill)**
- **Evidence:** zenobi-us/opencode-plugin-template exists and is used. Superpowers itself is often cloned as a template.
- **Pattern:** publish a Momentum template repo; users click "Use this template" on GitHub.
- **Effort:** low. But gives weak per-user updates — forked repos drift from upstream.
- **When to use:** for teams that want to customize Momentum heavily; less good as a primary distribution channel.

### Tier 3 — Low Evidence or Structural Risk

**5. Runtime adapter / unified coding-agent harness**
- **Evidence:** none. No LiteLLM-for-coding-agents exists in production.
- **Risk:** you become the adapter maintainer for N hosts. Superpowers shows this is viable but costly.
- **When to use:** if Momentum's ambition is the practice-layer standard, building the adapter layer could be a moat. But the market hasn't validated the need — teams are mostly happy with per-agent installers.

**6. Private plugin marketplace (Claude enterprise pattern)**
- **Evidence:** Anthropic enterprise supports it; no cross-agent equivalent exists.
- **Pattern:** host a marketplace.json registry with curated Momentum components.
- **When to use:** when Momentum goes commercial / enterprise. Not helpful for open-source distribution today.

### Explicitly NOT Viable

- **Dedicated agent package registry (new)** — skills.sh and npm already cover this layer; no room for a Momentum-specific registry.
- **Hooks.json → opencode plugin TS translator** — doesn't exist; building it would be a side-project worth less than just writing a native OpenCode plugin.

### Recommended Composition for Momentum

A pragmatic layered approach based on the evidence:

1. **Baseline:** Ship AGENTS.md (symlinked from CLAUDE.md) — Tier 1, trivial cost, maximum coverage.
2. **Skill layer:** Convert all Momentum skills to spec-compliant SKILL.md with `skills-ref validate` in CI — Tier 1, medium cost.
3. **Installer:** Ship `npx momentum install` that writes to per-agent skill directories — Tier 1. Evaluate reusing Antigravity Awesome Skills' installer architecture as reference.
4. **Host-specific adapters:** Only for Claude Code (plugin + hooks for plan-audit enforcement) and OpenCode (plugin for hook equivalents). Skip Codex until there's clear demand — its lack of primitives makes the adapter thin anyway.
5. **Do NOT build:** a runtime adapter layer, a new registry, or a hooks.json translator. The leverage isn't there.

---

## Primary Sources

### Official — Project Repos & Spec Pages

- https://agents.md/ — AGENTS.md canonical site, Agentic AI Foundation / Linux Foundation stewardship
- https://agentskills.io/specification — Agent Skills specification (canonical)
- https://github.com/anthropics/skills — Anthropic Agent Skills repo
- https://github.com/agentskills/agentskills — skills-ref validator
- https://github.com/obra/superpowers — Superpowers framework (v5.0.7)
- https://github.com/sickn33/antigravity-awesome-skills — Antigravity Awesome Skills installer
- https://github.com/vercel-labs/skills — Vercel Skills CLI
- https://skills.sh — Vercel skills directory
- https://github.com/SmrutAI/opencode-migration — Claude → OpenCode migration orchestrator
- https://github.com/NikiforovAll/opencode-marketplace — OpenCode marketplace CLI (v0.5.0)
- https://github.com/numman-ali/n-skills — n-skills curated marketplace
- https://github.com/awesome-opencode/awesome-opencode — awesome list
- https://github.com/zenobi-us/opencode-plugin-template — GitHub template for plugins
- https://github.com/zenobi-us/opencode-skillful — OpenCode skills plugin
- https://github.com/malhashemi/opencode-skills — OpenCode skills repo
- https://github.com/anthropics/claude-plugins-official — Anthropic official plugin directory
- https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem — Skills launch
- https://vercel.com/docs/agent-resources/skills — Vercel agent skills docs
- https://opencode.ai/docs/plugins/ — OpenCode plugin docs
- https://opencode.ai/docs/rules/ — OpenCode rules (AGENTS.md fallback chain)
- https://opencode.ai/docs/skills/ — OpenCode agent skills
- https://code.claude.com/docs/en/plugin-marketplaces — Claude Code plugin marketplace docs
- https://code.claude.com/docs/en/skills — Claude Code skills docs
- https://developers.openai.com/codex/guides/agents-md — Codex AGENTS.md guide
- https://docs.litellm.ai/docs/a2a — LiteLLM Agent Gateway (A2A Protocol)
- https://docs.litellm.ai/docs/agent_sdks — LiteLLM Agent SDKs

### Official — Maintainer Blog Posts

- https://blog.fsck.com/2025/10/09/superpowers/ — Superpowers: how I'm using coding agents October 2025
- https://blog.fsck.com/2025/10/27/skills-for-openai-codex/ — Porting Skills (and Superpowers) to OpenAI Codex
- https://blog.fsck.com/2025/11/24/Superpowers-for-OpenCode/ — Superpowers (and Skills) for OpenCode
- https://blog.fsck.com/2026/03/09/superpowers-5/ — Superpowers 5
- https://blog.fsck.com/releases/2026/03/31/superpowers-v5-0-7/ — v5.0.7 Copilot CLI release
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — Anthropic skills engineering post

### Practitioner Reports

- https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/
- https://www.devashish.me/p/migrating-from-claude-code-to-opencode
- https://gist.github.com/RichardHightower/827c4b655f894a1dd2d14b15be6a33c0
- https://dev.to/shinpr/same-framework-different-engine-porting-ai-coding-workflows-from-claude-code-to-codex-cli-n3p
- https://dev.to/treesoop/claude2codex-migrate-claude-code-config-to-openai-codex-in-one-command-jlj
- https://workflowswithai.substack.com/p/how-to-migrate-from-claude-code-to
- https://johnoct.com/blog/2026/02/12/skills-sh-open-agent-skills-ecosystem/
- https://drmowinckels.io/blog/2026/dotfiles-coding-agents/
- https://medium.com/@sean.j.moran/effective-claude-code-workflows-in-2026-what-changed-and-what-works-now-c93ebc6f8f50
- https://www.mpt.solutions/your-claude-plugin-marketplace-needs-more-than-a-git-repo/

### Unverified / Aggregator

- https://www.infoq.com/news/2026/02/vercel-agent-skills/
- https://www.buildmvpfast.com/blog/agent-skills-npm-ai-package-manager-2026
- https://serenitiesai.com/articles/agent-skills-guide-2026
- https://www.aimadetools.com/blog/codex-cli-complete-guide/
- https://virtualuncle.com/agent-skills-marketplace-skills-sh-2026/
- https://arxiv.org/html/2604.16911 — Skilldex academic proposal
