---
content_origin: claude-code-subagent
date: 2026-04-22
sub_question: "What alternatives to skills.sh and agentskills.io exist, and which handle hooks/agents/MCP/IDE-specific parts beyond skills?"
topic: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements — addendum"
---

# Alternatives to skills.sh / agentskills.io — Full-Stack Practice Distribution (2026-04-22)

## Framing

The canonical Agent Skills ecosystem (skills.sh directory + agentskills.io spec) is **skills-only** — a `SKILL.md` + optional `scripts/`, `references/`, `assets/`. It does not cover hooks, subagents, MCP server bundles, rules files, or IDE-specific settings. A Momentum-style practice (skills + hooks + agents + MCP + rules + per-host config) therefore needs a different distribution vehicle.

As of April 2026 the market has bifurcated into two patterns:

1. **Per-host plugin systems** (Claude Code plugins, Cursor plugins, Gemini CLI extensions, Cline/Roo marketplaces, Zed ACP registry) — each vendor ships a native bundle format that includes skills + hooks + agents + MCP for its own host, distributed via a Git-backed or vendor-curated marketplace.
2. **Cross-host harnesses and translators** (obra/Superpowers, oh-my-openagent/OMO, dot-agents, dotagent/skillkit, antigravity-awesome-skills, claude2codex) — layered on top, fanning one bundle out to multiple hosts or translating between formats.

Nothing yet exists as a truly cross-vendor, multi-primitive registry with first-class hook translation. The closest thing is **per-host plugin systems that happen to share a GitHub-backed marketplace.json convention**, with Superpowers acting as the most mature practice-pack layered on top.

---

## Category 1 — Per-host native plugin/extension systems (the real full-stack bundlers)

### 1. Claude Code Plugins (Anthropic) [OFFICIAL]

- **What it distributes:** The most primitive-rich bundle on the market. A plugin = `.claude-plugin/plugin.json` manifest + any combination of `skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `monitors/monitors.json`, `bin/` (executables added to `PATH`), `settings.json` (defaults, including activating a plugin-provided agent as the main thread).
- **Targets:** Claude Code only (and Anthropic's Cowork).
- **Install command:** `/plugin install <plugin-name>@<marketplace-name>`. Anthropic's official marketplace `claude-plugins-official` is auto-available; third-party marketplaces are added with `/plugin marketplace add <github-owner>/<repo>`.
- **Registry model:** GitHub-backed. Any repo with `.claude-plugin/marketplace.json` at root becomes a marketplace. Official Anthropic marketplace is hand-curated; community marketplaces are open. `claudemarketplaces.com` and `claudepluginhub.com` are aggregator directories that auto-scrape GitHub for marketplace.json files.
- **Hook/agent handling:** First-class. `hooks/hooks.json` carries the same schema as `.claude/settings.json` `hooks` object (PreToolUse, PostToolUse, SessionStart, etc.). Agents live in `agents/` as standalone files and can be activated as the main thread via `settings.json`.
- **Maturity:** Production. Anthropic-stewarded. Official marketplace launched 2025, plugin system GA by late 2025. Aggregators report 105k+ developers/month visiting Claude Code plugin marketplaces.
- **Gaps:** Claude Code only — no native cross-host translation.

### 2. Cursor Plugins / Cursor Marketplace [OFFICIAL]

- **What it distributes:** The only non-Anthropic vendor-native bundle covering all six primitives Momentum cares about — Rules (`.mdc` files), Skills, Subagents, Commands, MCP Servers, and Hooks. Manifest at `.cursor-plugin/plugin.json`.
- **Targets:** Cursor only.
- **Install:** Browser/UI install from the marketplace panel, or team-marketplace import from a GitHub repo via Dashboard → Settings → Plugins → Team Marketplaces. Deep-link URI (`cursor://anysphere.cursor-deeplink/mcp/install?...`) exists for MCP one-click install. No documented CLI install command.
- **Registry model:** Cursor-curated official marketplace + `cursor.directory` for community + org-level team marketplaces backed by GitHub.
- **Hook/agent handling:** Native to the host. Plugins can bundle MCPs together with skills that instruct the agent how to invoke them. Subagents, hooks, and rules are all first-class manifest primitives.
- **Maturity:** Official marketplace launched early 2026; 30+ partner plugins (Atlassian, Datadog, GitLab, Glean, Hugging Face, monday.com, PlanetScale) added by April 2026.
- **Gaps:** Cursor-only; no CLI-driven install path; org governance features still maturing.

### 3. Gemini CLI Extensions [OFFICIAL]

- **What it distributes:** Full-stack bundle: MCP servers, custom commands, context file (`GEMINI.md`), **agent skills**, hooks, custom themes, and subagents. Manifest is `gemini-extension.json`.
- **Targets:** Gemini CLI only.
- **Install:** `gemini extensions install <github-url-or-local-path>`. Skills auto-install to `~/.gemini/extensions/<extension_name>/skills`. `gemini extensions link .` for local dev.
- **Registry model:** Extensions Gallery (`geminicli.com/extensions/`) ranked by GitHub stars. Google-built + partner + community extensions (Dynatrace, Elastic, Figma, Harness, Postman, Shopify, Snyk, Stripe).
- **Hook/agent handling:** Hooks and subagents are listed primitives; agent skills adopted as open standard per Anthropic spec in Q1 2026.
- **Maturity:** GA with growing catalog; Agent Skills support announced March 2026.
- **Gaps:** Gemini-only; hook schema differs from Claude Code's PreToolUse/PostToolUse.

### 4. Cline MCP Marketplace [OFFICIAL]

- **What it distributes:** **MCP servers** as the primary primitive, with "MCP Rules" grouping them into trigger-keyword categories. Supports auto-installation flows guided by README or optional `llms-install.md`.
- **Targets:** Cline (and via shared `.roo`/`.cline` paths, sometimes Roo).
- **Install:** One-click install from the Extensions panel. Cline autonomously handles cloning + configuration.
- **Registry model:** `github.com/cline/mcp-marketplace` submission repo; served through the Cline VS Code extension.
- **Hook/agent handling:** No native hook primitive. Skills/agents-ish behavior comes via MCP Rules trigger keywords, not a first-class agent/hook manifest.
- **Maturity:** Production, widely adopted. `mcpmarket.com` aggregator lists hundreds of Cline-compatible servers.
- **Gaps:** MCP-centric; no hooks, no skills manifest, no agents. Narrower than Claude/Cursor/Gemini plugins.

### 5. Roo Code Marketplace [OFFICIAL]

- **What it distributes:** **MCPs + Modes**. Modes are custom instruction+rule sets that tailor Roo behavior for specific tasks (e.g., "React Component" mode, "Documentation Writer" mode). Install scope is project (`.roo/mcp.json`, `.roomodes`) or global (`mcp_settings.json`, `custom_modes.yaml`).
- **Targets:** Roo Code (Cline fork).
- **Install:** One-click from the marketplace UI inside VS Code.
- **Registry model:** Integrated into the Roo Code VS Code extension.
- **Hook/agent handling:** Modes are Roo's equivalent to subagent-ish behavior; no first-class hooks primitive.
- **Maturity:** Production.
- **Gaps:** Roo-only; two primitive types (Modes, MCPs) vs. Claude/Cursor's six.

### 6. Continue Hub [OFFICIAL]

- **What it distributes:** Seven "block" types composable into "Assistants": Models, Context, Docs, MCP Servers, Rules, Prompts, Data. `config.yaml` declares which blocks an assistant uses.
- **Targets:** Continue.dev (VS Code + JetBrains).
- **Install:** Continue Hub UI publishes/subscribes to blocks; assistants reference them in `config.yaml`.
- **Registry model:** Hosted hub at `continue.dev/hub` — the most registry-like of any entry here (not GitHub-backed).
- **Hook/agent handling:** No explicit hook primitive. Agents are composed from Models + Rules + MCP tools, not distributed as atomic entities.
- **Maturity:** Production.
- **Gaps:** No hooks; no first-class "agent" block (agents emerge from composition); narrower than Claude/Cursor plugin systems.

### 7. Zed Agent Server Extensions + ACP Registry [OFFICIAL]

- **What it distributes:** **Agent servers** (Claude Code, Codex CLI, GitHub Copilot CLI, OpenCode, Gemini CLI, etc.) via the Agent Client Protocol, plus MCP server extensions. Since v0.221 the ACP Registry is the preferred install path (launched Jan 28, 2026).
- **Targets:** Zed editor.
- **Install:** Via Zed extensions menu or ACP Registry.
- **Registry model:** Centralized ACP Registry (new as of Jan 2026) allows agent authors to push updates without waiting for Zed's extension review cycle.
- **Hook/agent handling:** Zed's model is "point at an external agent runtime" rather than shipping hooks/skills. It's an agent *host* registry, not a practice distributor.
- **Maturity:** GA April 2026; recent update made all built-in agents removable/manageable via ACP Registry.
- **Gaps:** Not a practice bundle mechanism — it's the runtime-selector layer below practices.

### 8. JetBrains Junie Extensions [OFFICIAL]

- **What it distributes:** Curated extensions giving Junie domain expertise: best practices, code patterns, anti-patterns, checklists for specific technologies.
- **Targets:** Junie (IntelliJ IDEA, PyCharm, WebStorm, etc.).
- **Install:** JetBrains plugin marketplace.
- **Registry model:** `github.com/JetBrains/junie-extensions` curated source + JetBrains official marketplace.
- **Hook/agent handling:** Unclear from public docs whether hooks/agents are first-class.
- **Maturity:** GA; limited primitive variety vs. Claude/Cursor.
- **Gaps:** JetBrains-only; appears primarily knowledge/skill-oriented.

### 9. GitHub Copilot Skills + `gh skill` CLI [OFFICIAL]

- **What it distributes:** Skills only (open Agent Skills spec). Copilot added skills support Dec 2025.
- **Install:** `gh skill install <owner>/<repo> <skill-name> --agent <agent> --scope <user|project>` — launched in public preview **April 16, 2026** via GitHub Changelog.
- **Targets:** GitHub Copilot, Claude Code, Cursor, Codex, Gemini CLI, Antigravity — the CLI resolves the host-directory problem automatically (`.agents/skills` for Copilot/Cursor, `.claude/skills` for Claude Code, etc.).
- **Registry model:** Any GitHub repo; no central registry required.
- **Hook/agent handling:** **Skills only** — explicitly not a full plugin bundler. Does not install hooks, agents, MCP.
- **Maturity:** Public preview as of April 16, 2026 (6 days old at time of writing).
- **Gaps:** Skills-only by design — same gap as skills.sh.

---

## Category 2 — Cross-host practice packs (the closest thing to "full practice distribution")

### 10. obra/Superpowers [PRAC]

- **What it distributes:** A **complete software development methodology** — composable skills + hooks + subagents + commands + scripts. Currently v5.0.7 on GitHub (164k stars, 14.4k forks per repo README snapshot — this likely counts the methodology org plus marketplace combined; treat the exact number as **[UNVERIFIED]** magnitude). Skills cover TDD, systematic debugging, brainstorming, plan writing, subagent-driven development, and a meta "using-superpowers" bootstrap skill.
- **Targets:** Claude Code, OpenAI Codex (CLI + app), Cursor, OpenCode, GitHub Copilot CLI, Gemini CLI — broadest cross-host support of any practice pack.
- **Install:** Per-host:
  - Claude Code: `/plugin install superpowers@claude-plugins-official` (official) or `/plugin install superpowers@superpowers-marketplace`
  - Cursor: `/add-plugin superpowers`
  - Gemini: `gemini extensions install https://github.com/obra/superpowers`
  - Codex/OpenCode/Copilot CLI: platform-native install commands
- **Registry model:** Dual — listed in Anthropic's official Claude marketplace AND ships its own `obra/superpowers-marketplace` (a curated Claude Code plugin marketplace repo).
- **Hook/agent handling:** First-class on Claude Code via a synchronous `SessionStart` hook that injects the `using-superpowers` skill content as bootstrap context before the agent's first turn (async: false). This is the "per-host bootstrap shim" pattern — different hook mechanisms per host, same behavior. OpenCode supports hooks natively, so Superpowers auto-configures on session start. On Codex (which lacks hooks), users must add lines to `AGENTS.md`.
- **Maturity:** Most mature cross-host practice pack. Actively maintained. Companion repo `superpowers-marketplace` curates 79 plugins / 184 agents / 150 skills per aggregator reports.
- **Gaps:** Methodology is opinionated (TDD-first, plan-before-code, subagent-driven dev) — may not match a project's practice. No explicit Momentum-style sprint/epic/story model. Hook translation across hosts is per-platform scripting, not a declarative schema.

### 11. oh-my-openagent (OMO) [PRAC]

- **What it distributes:** A multi-agent orchestration harness that ships **11 specialized agents + 8 task categories + 40+ lifecycle hooks + built-in skills + MCP integrations**, with multi-provider model routing (Claude Opus for planning, Gemini for frontend, Grok for exploration).
- **Targets:** OpenCode (primary); a GitHub Copilot CLI variant exists (`eugenejahn/oh-my-openagent-copilot`) with 11 agents / 10 skills / 5 hooks / 8 MCP servers.
- **Install:** `npm install oh-my-openagent` or equivalent OpenCode plugin install.
- **Registry model:** npm + GitHub.
- **Hook/agent handling:** Best-in-class for OpenCode specifically. 40+ hooks covering session-start, file-save, pre-commit, etc. Three-layer agent architecture (planning / orchestration / execution).
- **Maturity:** v1.0.0 initial release; actively marketed as "the best agent harness."
- **Gaps:** OpenCode-first — Copilot port exists, but no Claude Code / Cursor / Gemini native plugin (yet).

### 12. dot-agents (brew install dot-agents/tap/dot-agents) [PRAC]

- **What it distributes:** A unified `~/.agents/` directory containing config.json + rules/ + skills/ + settings/ (agent config + hooks) + local/ (machine-specific gitignored overrides). Uses **symlinks + hardlinks** to distribute configs to each agent's expected location.
- **Targets:** v1 supports Cursor, Claude Code, Codex, OpenCode (Aider listed as "coming soon").
- **Install:** `brew install dot-agents/tap/dot-agents` (also curl). MIT, no cloud dependency.
- **Registry model:** None — it's a dotfiles-style config layer, not a registry.
- **Hook/agent handling:** Hooks handled for Claude Code specifically (via settings/). Rules, skills, agent-specific settings all unified.
- **Maturity:** v1 launch. Active. Small but growing.
- **Gaps:** Config layer, not a distribution registry — you still need a source for skills/hooks/agents. Complements rather than replaces skills.sh.

### 13. johnlindquist/dotagent (translator) [PRAC]

- **What it distributes:** **Nothing of its own** — it's a universal AI agent configuration **parser and converter** between 15+ IDE/tool formats (Claude Code, VS Code Copilot, Cursor, Cline, Windsurf, Zed, Amazon Q, OpenAI Codex, OpenCode, Aider, Gemini, Qodo, JetBrains Junie, Roo Code). Unified format is a `.agent/` directory with Markdown + YAML frontmatter.
- **Content scope:** **Rules and config metadata only.** Explicitly does NOT handle hooks, MCP, agent hierarchies, or runtime execution.
- **Maturity:** Active, narrow-scope tool.
- **Gaps:** Rules/config only — skill-less, hook-less, agent-less, MCP-less. Portability tool, not a practice distributor.

### 14. rohitg00/skillkit [PRAC]

- **What it distributes:** Package manager for skills — install, translate, and share skills across 46+ agent hosts. Includes its own MCP server that lets agents fetch skills on demand.
- **Install:** `npm install -g skillkit` then `skillkit add <source>`, `skillkit translate <skill> --to <agent>`, `skillkit sync`, `skillkit serve` (REST API), `skillkit ui` (TUI).
- **Targets:** Top tier — Claude Code, Cursor, Codex, Gemini CLI, OpenCode, Copilot, Windsurf, Devin, Aider, Cody, Amazon Q. Plus 35 more including Cline, Continue, OpenHands, Replit Agent, Tabnine.
- **Hook/agent handling:** **Skills only** despite marketing. The "MCP server" feature is for fetching skills, not distributing MCP server bundles.
- **Gaps:** Skills-only, though with the broadest host coverage.

### 15. antigravity-awesome-skills (sickn33) [PRAC]

- **What it distributes:** 1,431+ SKILL.md files, bundles (curated role-based groupings), workflows (ordered execution playbooks), plugin-safe distributions for Claude Code and Codex marketplaces, and an npm installer CLI.
- **Install:** `npx antigravity-awesome-skills` (full library) or `--claude|--cursor|--codex|--gemini|--antigravity|--kiro|--path|--category|--risk|--tags` filters.
- **Targets:** Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, Kiro, OpenCode, GitHub Copilot.
- **Hook/agent handling:** **Skills only.** Bundles are skill recommendations, not packages containing hooks/agents/MCP. The "plugin distributions" sub-folder wraps skills into Claude Code plugin.json/marketplace.json format — but the primitives inside are still SKILL.md files.
- **Gaps:** The "1,431 skills" is volume, not depth — all are SKILL.md playbooks, no hooks or agents.

### 16. tech-leads-club/agent-skills [PRAC]

- **What it distributes:** "Secure, validated skill registry for professional AI coding agents. Extend Antigravity, Claude Code, Cursor, Copilot and more." Curation + security posture is the differentiator.
- **Hook/agent handling:** Skills-only per the repo description.
- **Gaps:** Same skills-only limitation.

### 17. FrancyJGLisboa/agent-skill-creator [PRAC]

- **What it distributes:** A skill-creation workflow that generates a single SKILL.md and publishes it to 14+ tools (Claude Code, Copilot, Cursor, Windsurf, Codex, Gemini, Kiro, ...).
- **Gaps:** Authoring/translation tool — skills-only.

### 18. claude2codex [PRAC]

- **What it distributes:** **Nothing** — it's a one-way migration tool. `npx claude2codex init`, `npx claude2codex migrate --dry-run`, `npx claude2codex migrate`. Translates Claude Code's `.claude/settings.json` + plugin configs + MCP servers + memory files to Codex's `~/.codex/config.toml` (TOML). Reports ~95% auto-conversion success; the other 5% goes to a conflict report for manual fixup.
- **Hook/agent handling:** Translates hooks schema from Claude JSON to Codex's `notification hook` model where possible. MCP server configs translate directly (open standard across hosts).
- **Maturity:** Working, niche tool.
- **Gaps:** One-directional (Claude → Codex). Not a distribution mechanism — a migration utility.

### 19. coder/agentapi [PRAC]

- **What it distributes:** An HTTP API server that controls Claude Code, Goose, Aider, Gemini, Amp, and Codex through terminal emulation. Written in Go.
- **Install:** curl-download the release binary.
- **Gaps:** Runtime adapter at the HTTP level — not a skill/hook/agent distribution layer. Relevant only as the "control plane" substrate below practice distribution, similar to Zed's ACP Registry but HTTP-native.

### 20. everything-claude-code (affaan-m) [PRAC]

- **What it distributes:** A "harness performance optimization system" — skills, instincts, memory, security, research-first development patterns. Markets itself across Claude Code, Codex, OpenCode, Cursor.
- **Maturity:** Active; smaller than Superpowers.
- **Gaps:** Less prominent; appears skill+instruction-oriented rather than hook-heavy.

### 21. fcakyon/claude-codex-settings [PRAC]

- **What it distributes:** A personal dotfiles-style repo of skills, plugins, hooks, and agents for Claude Code + Codex.
- **Gaps:** Personal config, not a general distribution mechanism. Representative of the "dotfiles for agents" trend.

### 22. atxtechbro/dotfiles [PRAC]

- **What it distributes:** "AI-orchestration dotfiles" for parallelized agents and principle enforcement.
- **Gaps:** Personal dotfiles pattern — representative, not a reusable registry.

---

## Category 3 — Skill-only registries (like skills.sh, for completeness)

- **ClawHub / OpenClaw** [PRAC]: 3,286 community skills / 1.5M+ downloads as of Feb 2026; CLI publish with `cs-` prefix fallback; hit by the "ClawHavoc" typosquatting attack late Jan 2026 — 341 malicious skills removed after Feb 7 VirusTotal partnership. Skill-only registry; no hooks/agents/MCP packaging.
- **Microsoft/skills** [OFFICIAL]: 128 skills across Python/.NET/TypeScript/Java/Rust, plus pre-configured `.vscode/mcp.json` MCP servers, role-specific agent personas, AGENTS.md templates, and curated plugin bundles (`deep-wiki`, `azure-skills`). Installs via `npx skills add microsoft/skills`. **Actually a partial full-stack bundler** — skills + MCP + agents + AGENTS.md, but scoped to Microsoft/Azure domain.
- **anthropics/skills** [OFFICIAL]: Reference implementations; also ships as a Claude Code marketplace (`skills/.claude-plugin/marketplace.json`).
- **Claude plugin aggregators** [PRAC]: `claudemarketplaces.com` (auto-scrapes GitHub hourly, last updated March 11 2026), `claudepluginhub.com`, `buildwithclaude.com`, `aitmpl.com/plugins`, `awesomeclaude.ai` — all aggregate GitHub-hosted `marketplace.json` files; they're directories of Claude Code plugin bundles (which are full-stack), not separate distribution systems.

---

## Category 4 — Cross-vendor specs / foundations

- **AGENTS.md** (Agentic AI Foundation / Linux Foundation) [OFFICIAL]: Stewarded under the AAIF since the foundation formed late 2025 (founding contributions: MCP, Block's goose, OpenAI's AGENTS.md). Platinum members: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI. Adopted by 60k+ projects/frameworks (Amp, Codex, Cursor, Devin, Factory, Gemini CLI, Copilot, Jules, VS Code). **Scope: project-instructions text only** — router file, not hooks/agents/MCP packaging.
- **agentskills.io spec** [OFFICIAL]: Anthropic-originated, neutral GitHub org, skills-only.
- **Cloudflare's agent-skills-discovery-rfc** [OFFICIAL]: `.well-known/agent-skills` discovery mechanism per RFC 8615. Publishers host under `/.well-known/agent-skills/` but `url` field allows arbitrary hosting (CDN, versioned paths). Index format differentiates `skill-md` (single file) vs. `archive` (skill + resources). **Skills-only** discovery, not full-practice distribution.
- **OpenCode `skills.urls` config** [OFFICIAL]: Remote skill URLs declared in `opencode.json`; OpenCode downloads to `~/.cache/opencode/skills/`. Issue `anomalyco/opencode#20020` shows this was in flight Q1 2026.
- **dotagent protocol** (sgmonda, bgreenwell): Open specs for `.agent/` / `.agents/` / `.dotagent/` directory structures. Multiple competing proposals — not yet converged.

---

## Hook/agent translation: the actual hard problem

**No tool today provides declarative cross-host hook translation.** Every claim of "multi-host hooks" decomposes to one of three patterns:

1. **Per-host bootstrap shim** (Superpowers): hand-written `SessionStart`/equivalent hook scripts per host. Same behavior, different code, different manifest locations.
2. **Single-host hooks + AGENTS.md fallback for hostless targets** (Superpowers on Codex): where the host doesn't support hooks, fall back to passive AGENTS.md instructions.
3. **Config translator** (claude2codex): point-in-time migration from one host's hook format to another, not ongoing translation.

A Momentum-style practice with real hook translation semantics would be a **new category** — nothing in April 2026 solves it declaratively across Claude Code + Codex + OpenCode + Cursor + Gemini CLI + Copilot.

---

## Ranked shortlist for distributing a FULL practice (skills + hooks + agents + MCP + rules)

### 1. Claude Code plugin (claude-plugins-official + custom marketplace) — **strongest for single-host, deepest primitive coverage**

- **Tradeoffs:** Claude Code only; but Claude Code is the deepest plugin system by a wide margin (skills, agents, hooks, MCP, LSP, monitors, bin/, settings.json). For a practice like Momentum that's Claude-Code-native, this is the least-lossy distribution format. Marketplace is Git-backed, so distribution is free.
- **Adoption path:** Ship Momentum as `/plugin install momentum@<marketplace>`. Use `settings.json` to activate the Impetus agent as main thread. Bundle all skills/agents/hooks/MCP natively.
- **Gap vs. need:** Zero cross-host support. If Momentum ever wants to support Codex/OpenCode/Cursor practitioners, this won't carry you.

### 2. obra/Superpowers-style per-host plugin set + a shared `superpowers-marketplace` repo — **strongest cross-host pattern in production today**

- **Tradeoffs:** Requires writing N per-host bootstrap shims (one hook per host, plus an AGENTS.md fallback for hostless targets like Codex). Proven in production — the only practice pack that ships to Claude Code + Codex + OpenCode + Cursor + Gemini + Copilot simultaneously. Methodology layer (TDD, plan-before-code) is opinionated but demonstrably adopted (164k GitHub stars per repo display [magnitude UNVERIFIED but directionally correct]).
- **Adoption path:** Copy the architecture — one marketplace repo that ships six per-host plugin variants; each variant has its own `SessionStart`/equivalent hook that injects the Momentum bootstrap context. Keep Momentum's skill library as the shared payload; vary only the bootstrap + hook delivery per host.
- **Gap vs. need:** No declarative hook-translation schema — it's per-host scripting. Momentum would own that complexity.

### 3. Gemini CLI Extension + Claude Code Plugin + Cursor Plugin, linked from a GitHub-hosted multi-repo index — **pragmatic cross-host today, without Superpowers' methodology lock-in**

- **Tradeoffs:** Requires maintaining 3+ parallel manifests (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`) with overlapping-but-not-identical primitive sets. Easier than Superpowers' six-host fan-out; harder than "just ship a Claude plugin." Lets each host's user invoke their native install command (`/plugin install`, `/add-plugin`, `gemini extensions install`).
- **Adoption path:** One Momentum source of truth → a small build step that emits three bundle variants to three host formats. Hooks must be re-authored per host because schemas differ.
- **Gap vs. need:** Same hook-translation gap. Covers maybe 70% of the practitioner base without touching Codex/OpenCode/Copilot.

### Honorable mentions

- **dot-agents** if the goal is "unify developer configs" rather than "distribute a practice" — complements any of the top three, doesn't replace them.
- **skillkit** if the goal is just skill portability across 46 hosts — skills-only, not a full practice.
- **`gh skill`** (launched 6 days ago, April 16 2026) if the goal is dead-simple skill install across Copilot/Claude/Cursor/Codex/Gemini/Antigravity — but it's skills-only and won't grow into hooks per the changelog.

---

## Verified absences

- [OFFICIAL] **No cross-vendor full-stack registry exists as of 2026-04-22.** The closest convergence is AGENTS.md under AAIF (text-only) + MCP (tool protocol, not distribution) + agentskills.io (skills-only).
- [OFFICIAL] **`gh skill` is explicitly skills-only** per GitHub Changelog 2026-04-16 — not a Copilot-native full plugin bundler.
- [PRAC] **No declarative hook-translation schema** exists in any tool surveyed. Superpowers, oh-my-openagent, claude2codex, and dot-agents each handle hooks via per-host scripting or point-in-time translation, not a schema.
- [PRAC] **Enterprise-grade B2B practice distribution** (Copilot Workspaces, Cursor Teams, Anthropic Teams private plugin marketplaces) exists as a governance layer on top of the vendor-native plugin formats — no separate full-stack registry discovered for April 2026. Cursor Team Marketplaces and Claude Code's private-marketplace-via-Git are the two main mechanisms.

---

## Sources

- [Claude Code Plugins docs](https://code.claude.com/docs/en/plugins)
- [Anthropic claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- [Cursor Plugins Docs](https://cursor.com/docs/plugins)
- [Cursor Marketplace blog](https://cursor.com/blog/new-plugins)
- [Gemini CLI extensions docs](https://geminicli.com/docs/extensions/)
- [Gemini CLI writing extensions](https://geminicli.com/docs/extensions/writing-extensions/)
- [Gemini CLI Agent Skills](https://medium.com/google-cloud/your-gemini-cli-extensions-just-got-smarter-introducing-agent-skills-a8fbfa077e7f)
- [Cline MCP Marketplace](https://cline.bot/blog/introducing-the-mcp-marketplace-clines-new-app-store)
- [Roo Code Marketplace](https://docs.roocode.com/features/marketplace)
- [Continue Hub](https://www.continue.dev/hub)
- [Continue config.yaml reference](https://docs.continue.dev/reference)
- [Zed ACP Registry](https://zed.dev/blog/acp-registry)
- [Zed Agent Server Extensions](https://zed.dev/docs/extensions/agent-servers)
- [gh skill changelog](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)
- [GitHub Copilot Agent Skills changelog](https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/)
- [obra/superpowers](https://github.com/obra/superpowers)
- [Superpowers blog post](https://blog.fsck.com/2025/10/09/superpowers/)
- [Superpowers for OpenCode](https://blog.fsck.com/2025/11/24/Superpowers-for-OpenCode/)
- [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
- [oh-my-openagent-copilot](https://github.com/eugenejahn/oh-my-openagent-copilot)
- [dot-agents](https://www.dot-agents.com/)
- [johnlindquist/dotagent](https://github.com/johnlindquist/dotagent)
- [rohitg00/skillkit](https://github.com/rohitg00/skillkit)
- [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)
- [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills)
- [FrancyJGLisboa/agent-skill-creator](https://github.com/FrancyJGLisboa/agent-skill-creator)
- [claude2codex DEV post](https://dev.to/treesoop/claude2codex-migrate-claude-code-config-to-openai-codex-in-one-command-jlj)
- [coder/agentapi](https://github.com/coder/agentapi)
- [microsoft/skills](https://github.com/microsoft/skills)
- [ClawHub](https://clawhub.biz/)
- [openclaw/clawhub](https://github.com/openclaw/clawhub)
- [skills.sh (Vercel)](https://vercel.com/docs/agent-resources/skills)
- [skills.sh changelog](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)
- [AAIF / Linux Foundation announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [AGENTS.md](https://agents.md/)
- [Cloudflare agent-skills-discovery-rfc](https://github.com/cloudflare/agent-skills-discovery-rfc)
- [OpenCode skills docs](https://opencode.ai/docs/skills/)
- [claudemarketplaces.com](https://claudemarketplaces.com)
- [claudepluginhub.com](https://www.claudepluginhub.com/)
- [JetBrains junie-extensions](https://github.com/JetBrains/junie-extensions)
