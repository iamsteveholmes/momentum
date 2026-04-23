---
content_origin: claude-code-subagent
date: 2026-04-22
sub_question: "What cross-agent skill/extension installers and registries actually exist as of April 2026?"
topic: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements — addendum"
---

# Cross-Agent Skill Installer & Registry Ecosystem — April 2026

Source tags: **[OFFICIAL]** = primary source (npm registry, vendor docs, vendor GitHub), **[PRAC]** = practitioner/third-party report with URL, **[UNVERIFIED]** = claim I could not confirm from a primary source.

---

## 1. `npx skills` — what is it?

**[OFFICIAL]** The `skills` npm package is real, live, and active as of April 2026.

- **Package name:** `skills` (unscoped)
- **npm page:** https://www.npmjs.com/package/skills
- **Latest version:** `1.5.1`, published 2026-04-17 (per npm registry metadata)
- **Maintainers on npm registry:** `rauchg` (Guillermo Rauch, Vercel CEO) and `quuu` (Andrew Qu)
- **Repository:** https://github.com/vercel-labs/skills (15.5k stars, 1.3k forks as of April 2026)
- **License:** MIT
- **Binaries installed:** `skills` and `add-skill` (both point to `bin/cli.mjs`)
- **Engines:** Node >=18
- **Description (npm):** "The open agent skills ecosystem"
- **Announced:** January 20, 2026 via Vercel changelog (https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem). Note: the changelog page credits "Andrew Qu" as author; the `vercel-labs` GitHub org is the canonical home.

### Supported targets (verified from npm package keywords list)

The npm `keywords` array lists the following agent targets explicitly:

```
amp, antigravity, augment, bob, claude-code, openclaw, cline, codebuddy,
codex, command-code, continue, cortex, crush, cursor, deepagents, droid,
firebender, gemini-cli, github-copilot, goose, junie, iflow-cli, kilo,
kimi-cli, kiro-cli, kode, mcpjam, mistral-vibe, mux, opencode, openhands,
pi, qoder, qwen-code, replit, roo, trae, trae-cn, warp, windsurf,
zencoder, neovate, pochi, adal, universal
```

That's ~45 named agents plus a `universal` fallback. **[OFFICIAL]**

### Commands (verified from README via GitHub raw fetch)

- `npx skills add <owner/repo>` — install from a GitHub/GitLab/git URL/local path
- `npx skills list` (alias `ls`) — list installed skills
- `npx skills find` — interactive/keyword search
- `npx skills update` — upgrade skills
- `npx skills remove` (alias `rm`) — uninstall
- `npx skills init` — scaffold a new skill

### Registry model

**[OFFICIAL — per skills.sh directory page]** The registry is GitHub itself: any public GitHub repo with a `SKILL.md` at root is a valid skill source. There is no separate package index — the directory at `skills.sh` is a curated browsing surface over GitHub-hosted skills.

---

## 2. `skills.sh` — real domain?

**[OFFICIAL]** Yes, live at https://skills.sh/.

- Self-describes as "The Agent Skills Directory"
- **Installation model:** `npx skills add <owner/repo>` (i.e., it delegates to the Vercel-maintained CLI above)
- Hosted on Vercel infrastructure
- Reports ~91,000 total installations tracked across all time (as of the directory visit)
- **Named publishers with install counts visible on the page:**
  - Vercel Labs — 1.2M+ installs across their skills
  - Anthropic — 326.9K installs for `frontend-design` alone
  - Microsoft — 4.3M+ total across Azure skills
  - Supabase, Firebase, Expo — platform-specific skills
  - Community contributors (e.g., "Obra" — this is Jesse Vincent's `obra/superpowers`, confirmed via a separate DeepWiki hit)

**Relationship to `npx skills`:** `skills.sh` is the directory; the CLI is the installer. Same Vercel Labs orbit; they are designed together.

---

## 3. `agentskills.io` — real spec site?

**[OFFICIAL]** Yes, live at https://agentskills.io/home and https://agentskills.io/specification.

### Governance & ownership (carefully read)

- The site says verbatim: *"The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products. The standard is open to contributions from the broader ecosystem."*
- **Hosted at:** https://github.com/agentskills/agentskills (the `agentskills` GitHub org — this is a **separate org**, not `anthropics/`)
- Repo stats: ~16.9k stars, ~995 forks; Apache 2.0 code, CC-BY-4.0 docs
- **Anthropic is the originator and current maintainer** of the spec, per README language, but the repo lives under a neutral `agentskills` org — parallel to MCP's evolution. Simon Willison's Dec 19 2025 post (https://simonwillison.net/2025/Dec/19/agent-skills/) notes the spec *"may eventually move to the Agentic AI Foundation (AAIF)"* — this AAIF move is **[UNVERIFIED]** as of April 2026; I could not find evidence it has actually moved.

### Release date

**[OFFICIAL — corroborated by Unite.AI coverage + Simon Willison post]**
- Anthropic formally released Agent Skills as an open standard on **December 18, 2025** (Unite.AI article date-of-event). Simon Willison's post-on-it is dated Dec 19, 2025.

### Named adopters (from agentskills.io homepage client carousel, verified)

A partial list extracted directly from the page source (each with link to their own skills docs):

Junie (JetBrains), Gemini CLI, Autohand Code CLI, OpenCode, OpenHands, Mux (Coder), Cursor, Amp (Sourcegraph), Letta, Firebender, Goose (Block), GitHub Copilot, VS Code, Claude Code, Claude, OpenAI Codex, Piebald, Factory, pi (shittycodingagent.ai), Databricks Genie Code, Agentman, TRAE (ByteDance), Spring AI, Roo Code, Mistral AI Vibe, Command Code, Ona, VT Code, Qodo, Laravel Boost, Emdash, Snowflake Cortex Code, Kiro, Workshop, Google AI Edge Gallery, nanobot, fast-agent.

**~36+ named client products** — this is the industry adoption claim and it appears substantive, not hand-wavy.

### Spec content (extracted verbatim from agentskills.io/specification)

Required frontmatter fields: `name` (≤64 chars, lowercase alphanum + hyphens, must match parent dir), `description` (≤1024 chars).
Optional: `license`, `compatibility` (≤500 chars), `metadata` (key/value map), `allowed-tools` (experimental, space-separated tool allowlist).
Directories: `scripts/`, `references/`, `assets/` — all optional.
Progressive disclosure model: metadata at startup (~100 tok) → SKILL.md body on activation (<5000 tok recommended) → referenced files on demand.
Validation tool: `skills-ref` at github.com/agentskills/agentskills/tree/main/skills-ref.

---

## 4. `SKILL.md` standard — is there an actual cross-agent spec?

**[OFFICIAL]** Yes — the spec at https://agentskills.io/specification is the cross-agent spec.

- Anthropic's own reference repo at https://github.com/anthropics/skills explicitly defers to agentskills.io for the standard: *"For information about the Agent Skills standard itself, see agentskills.io."* The `anthropics/skills` repo implements the standard — it does not define it.
- **Adoption is not just claimed; it's documented.** Codex docs (https://developers.openai.com/codex/skills) state: *"A skill is a directory with a `SKILL.md` file plus optional scripts and references… build[s] on the open agent skills standard."*
- OpenCode docs (https://opencode.ai/docs/skills/) implement the same frontmatter rules (name 1–64 chars, description 1–1024, etc.) — verbatim constraint match with the spec.
- VS Code docs (https://code.visualstudio.com/docs/copilot/customization/agent-skills) also follow the same format.

**Verdict:** The SKILL.md standard is real, narrow, genuinely portable, and genuinely adopted. You are not hallucinating this.

---

## 5. Alternative installers (April 2026)

### 5a. Agent-native skill installers (not via `npx skills`)

**[OFFICIAL] `$skill-installer` in OpenAI Codex CLI**
- Source: https://developers.openai.com/codex/skills
- Syntax: `$skill-installer <skill-name>` (e.g., `$skill-installer linear`)
- Discovers skills from `.agents/skills` walking up the directory tree
- Does **not** integrate with `npx skills`; it's a parallel installer internal to Codex

**[OFFICIAL] OpenCode's native `skill` tool**
- Source: https://opencode.ai/docs/skills/
- Loads from `.opencode/skills/` and `~/.config/opencode/skills/`
- **No install command** — filesystem discovery only. Users either use `npx skills add` (third-party) or drop folders manually.

**[OFFICIAL] Crush (Charmbracelet)**
- Source: https://github.com/charmbracelet/crush
- Skills support: spec-compliant, loads from `$CRUSH_SKILLS_DIR`, `$XDG_CONFIG_HOME/agents/skills`, `$XDG_CONFIG_HOME/crush/skills`
- **No dedicated `crush skill install` subcommand** found in docs — installation is filesystem-level. The third-party `clawhub` CLI (on npm) offers `clawhub install crush-…` as an alternative install path **[PRAC]** (https://lobehub.com/skills/).

**[OFFICIAL] Cursor plugin installer**
- Source: https://cursor.com/docs/plugins
- In-editor: `/add-plugin` command
- Plugin structure carries a `skills/` subdirectory following SKILL.md spec
- Also installable via `npx skills add` because Cursor is listed as a target in the `skills` keywords

### 5b. Cross-agent installers competing with `npx skills`

From npm search on "agent-skills", several competitor/peer packages exist — **[OFFICIAL, per npm registry listings]**:

| Package | Description (from npm) |
|---|---|
| `openskills` | "Universal skills loader for AI coding agents" (github.com/numman-ali/openskills) |
| `clawhub` | "ClawHub CLI — install, update, search, and publish skills plus OpenClaw pac…" |
| `clawdhub` | "ClawdHub CLI — install, update, search, and publish agent skills" |
| `skvlt` | "The CLI for backing up and restoring Agent Skills" |
| `ctx7` | "Context7 CLI — Manage AI coding skills and documentation context" |
| `@iceinvein/agent-skills` | "Install agent skills into AI coding tools" |
| `@tech-leads-club/agent-skills` | "The secure, validated skill registry for professional AI coding agents" |
| `antigravity-awesome-skills` | "1,431+ agentic skills for Claude Code, Gemini CLI, Cursor, Antigravity & more" |

`skills` (Vercel Labs) dominates by stars, install count, and keyword breadth — it's the default. But there is a competitor ecosystem. **[PRAC]**

### 5c. Curated lists / awesome repos

- `VoltAgent/awesome-agent-skills` — "1000+ agent skills from official dev teams and community, compatible with Claude Code, Codex, Gemini CLI, Cursor, and more" **[OFFICIAL github]**
- `tech-leads-club/agent-skills` — "secure, validated skill registry for professional AI coding agents" **[OFFICIAL github]**
- `skillmatic-ai/awesome-agent-skills` — awesome list **[OFFICIAL github]**

### 5d. Competing directory sites

- `skills.sh` — Vercel Labs official directory **[OFFICIAL]**
- `askill.sh` — community registry; scores skills on Safety/Clarity/Reusability/Completeness/Actionability; maintained by "avibe-bot/askill" per page content; claims 270k results and "40+ agents" **[OFFICIAL site content, but maintainer identity is thin; tag as [PRAC] on identity]**
- `skillsmp.com` — "independent community project" per its FAQ; aggregates ~973k skills from GitHub; **explicitly not affiliated with Anthropic or OpenAI**; credits "@God_I_13" **[OFFICIAL site, [PRAC] on maintainer identity]**
- `skillsdirectory.com` — "Secure, Verified Agent Skills for Claude AI" **[PRAC]** (search result; not fetched directly)

### 5e. `AGENTS.md` — orthogonal, not a skills installer

**[OFFICIAL]** AGENTS.md is a separate (but complementary) open standard at https://agents.md/ and https://github.com/agentsmd/agents.md. It defines a project-level instructions file (like a README for agents), not an installable skill format. Adopted by Copilot coding agent, Codex, Cursor, Amp, Factory, RooCode, Zed, Warp, and others. **60,000+ open-source projects use it** per GitHub search data cited in multiple practitioner posts **[PRAC]** (https://prpm.dev/blog/agents-md-deep-dive, https://tessl.io/blog/). Do not conflate AGENTS.md with SKILL.md — they solve different problems.

---

## 6. Package registries for agent skills

**Dominant distribution mechanism:** **GitHub repositories themselves**, not a dedicated package registry.

- `npx skills` treats GitHub repos as the atomic unit. Spec: https://agentskills.io
- **No `@agent-skills/*` or `@agentskills/*` npm scope is in broad use.** Searching npm for `@agent-skills` returns zero hits; `@agentskills` scope likewise not a major distribution path. **[OFFICIAL — verified via npm search API]**
- Some npm scoped packages **do** exist (e.g., `@elizaos/plugin-agent-skills`, `@willbooster/agent-skills`, `@vibe-agent-toolkit/agent-skills`, `@iceinvein/agent-skills`) but these are individual vendor publications, not a coordinated scope convention.
- Skills directories (`skills.sh`, `askill.sh`, `skillsmp.com`) are **search/browse layers over GitHub**, not independent registries with their own storage.

**Verdict:** GitHub is the distribution backend; CLIs are thin clients that `git clone` or fetch archive tarballs. This is functionally similar to how `gh extension install` and `go install` work — the VCS is the registry.

---

## 7. Cross-agent runtime adapters ("LiteLLM for agents")

### 7a. AgentAPI (Coder) — closest match **[OFFICIAL]**

- Repo: https://github.com/coder/agentapi
- Maintainer: Coder (the company behind cloud dev environments)
- **Stated goal:** *"make AgentAPI a universal adapter to control any coding agent, so a developer using AgentAPI can switch between agents without changing their code."*
- **Mechanism:** Runs an in-memory terminal emulator, translates REST API calls to terminal keystrokes, parses agent output into messages
- **Supported agents:** Claude Code, AmazonQ, OpenCode, Goose, Aider, Gemini, GitHub Copilot, Sourcegraph Amp, Codex, Auggie, Cursor CLI
- **Interface:** REST — `GET/POST /messages`, `GET /status`, `GET /events` (SSE)

This is the best-fit "LiteLLM for agents" as of April 2026.

### 7b. LiteLLM itself

- Repo: https://github.com/BerriAI/litellm
- **Scope is LLM providers, not agents.** It normalizes OpenAI/Anthropic/Gemini/Bedrock/etc. into the OpenAI API shape. It does **not** normalize Claude Code vs Codex vs OpenCode tool-call schemas.
- LiteLLM integrates *with* agent frameworks (OpenAI Agents SDK, Google ADK) as a backend, not as a peer.

### 7c. cc-switch (farion1231) **[PRAC]**

- Repo: https://github.com/farion1231/cc-switch
- "Cross-platform desktop All-in-One assistant tool for Claude Code, Codex, OpenCode, openclaw & Gemini CLI"
- Focus: managing configs/API keys/MCP across tools — **not a runtime normalization layer**. Closer to a switchboard UI than an adapter API.

### 7d. Other candidates — not adapters in the strict sense

- `oh-my-claudecode` — multi-agent orchestration *within* Claude Code; not cross-agent
- `swarmclaw` — self-hosted multi-agent runtime; parallel architecture, not an adapter

**Verdict:** `coder/agentapi` is the only project explicitly aiming at the "LiteLLM for agents" role. LiteLLM solves the LLM layer; AgentAPI aspires to solve the agent layer. These are complementary.

---

## What doesn't exist (verified absences)

Items I checked for and could not confirm as existing / live / meaningful as of 2026-04-22:

1. **No `@agent-skills` or `@agentskills` npm scope as a distribution convention.** Searching npm returns zero `@agent-skills/*` results; `@agentskills/*` has only a smattering of unrelated packages. The ecosystem standard is unscoped `skills` + GitHub URLs, not a scoped namespace.
2. **No "aider install" or `aider plugin install` CLI command.** Aider has no plugin/hook system. The `aider-skills` PyPI package (libraries.io page exists) is a third-party shim that uses aider's `/run` and `--read` flags — it is **not** first-party.
3. **No `codex skill add` command.** Codex's installer is `$skill-installer <name>` (invoked from within the Codex CLI as a slash-prefixed command), not a standalone `codex skill add` subcommand.
4. **No `cursor install` command-line skill installer.** Cursor's in-editor command is `/add-plugin`; there is no documented shell-level `cursor install` binary. Users either use `npx skills add` or drop files into `$HOME/.cursor/plugins/`.
5. **No dedicated central package registry (à la npmjs.com) for skills.** Every "registry" surfaces GitHub-hosted skills. There is no `registry.skills.io` or equivalent storage backend.
6. **The Agentic AI Foundation (AAIF) housing the SKILL.md spec — not confirmed.** Simon Willison mentioned this as a possibility in Dec 2025; no primary source confirms the move has actually happened by April 2026. Spec remains at `github.com/agentskills/agentskills`.
7. **Anthropic does not own or directly host `agentskills.io`.** The site and repo live under a neutral `agentskills` GitHub org. Anthropic is the originating author and current maintainer per README, but legal/org ownership is structured neutrally — mirroring the MCP playbook. Do **not** assert "Anthropic's site agentskills.io" — it's the cross-vendor standard's site.
8. **No unified cross-agent tool-call adapter with wide adoption.** AgentAPI is the best candidate but is still early (no equivalent to LiteLLM's 100+-provider maturity). Most projects still treat each agent as a discrete integration.

---

## Sources (primary, fetched during this research)

- https://www.npmjs.com/package/skills (+ direct npm registry JSON)
- https://github.com/vercel-labs/skills
- https://skills.sh/
- https://agentskills.io/home
- https://agentskills.io/specification
- https://github.com/agentskills/agentskills
- https://github.com/anthropics/skills
- https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem
- https://developers.openai.com/codex/skills
- https://opencode.ai/docs/skills/
- https://github.com/charmbracelet/crush
- https://github.com/coder/agentapi
- https://cursor.com/docs/plugins
- https://agents.md/ (orthogonal standard)
- https://simonwillison.net/2025/Dec/19/agent-skills/ (practitioner commentary)
- https://www.unite.ai/anthropic-opens-agent-skills-standard-continuing-its-pattern-of-building-industry-infrastructure/
- https://askill.sh/
- https://skillsmp.com/
- npm search API: `/-/v1/search?text=agent-skills`
