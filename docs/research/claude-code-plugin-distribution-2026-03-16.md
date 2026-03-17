# Claude Code Plugin Distribution & Installation -- Research Findings

**Date:** 2026-03-16
**Status:** Research complete
**Confidence:** High for official Anthropic mechanisms; moderate for third-party tools (community projects move fast)

---

## 1. The Official Plugin Marketplace System

Claude Code's native plugin system is built around **marketplaces** -- JSON catalogs that list plugins and where to fetch them. This is the primary, Anthropic-supported distribution mechanism.

### How It Works

1. A marketplace is a git repo (or URL) containing `.claude-plugin/marketplace.json`
2. Users register a marketplace: `/plugin marketplace add owner/repo`
3. Users install individual plugins from it: `/plugin install plugin-name@marketplace-name`
4. Plugins are copied to a local cache at `~/.claude/plugins/cache`

### The Official Anthropic Marketplace

- **Name:** `claude-plugins-official`
- **Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- **Auto-included:** Yes, available by default in every Claude Code installation
- **Submission:** Via [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit) or [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)
- **Categories:** Code intelligence (LSP), external integrations (GitHub, Jira, Slack, etc.), development workflows, output styles

There is also a **demo marketplace** at `anthropics/claude-code` (the main Claude Code repo) with example plugins.

**Scale (as of Jan 2026):** Community tracking reports ~43 marketplaces with ~834 total plugins across the ecosystem.

**Sources:**
- [Discover and install prebuilt plugins -- Claude Code Docs](https://code.claude.com/docs/en/discover-plugins)
- [Create and distribute a plugin marketplace -- Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [anthropics/claude-plugins-official (GitHub)](https://github.com/anthropics/claude-plugins-official)

---

## 2. Plugin Distribution Mechanisms (What Sources Are Supported)

The `marketplace.json` `source` field for each plugin supports **six source types**:

| Source Type | Format | Example |
|---|---|---|
| **Relative path** | String starting with `./` | `"./plugins/my-plugin"` |
| **GitHub repo** | Object with `source: "github"` | `{ "source": "github", "repo": "owner/repo", "ref": "v2.0.0" }` |
| **Git URL** | Object with `source: "url"` | `{ "source": "url", "url": "https://gitlab.com/team/plugin.git" }` |
| **Git subdirectory** | Object with `source: "git-subdir"` | `{ "source": "git-subdir", "url": "...", "path": "tools/plugin" }` |
| **npm package** | Object with `source: "npm"` | `{ "source": "npm", "package": "@acme/claude-plugin", "version": "^2.0.0" }` |
| **pip package** | Object with `source: "pip"` | `{ "source": "pip", "package": "my-plugin" }` |

### Can plugins be distributed via npm?

**Yes.** The `npm` source type is officially supported. You can publish a plugin as an npm package (public or private registry) and reference it in `marketplace.json`:

```json
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0",
    "registry": "https://npm.example.com"
  }
}
```

Claude Code runs `npm install` to fetch the package. Supports version ranges (`^2.0.0`, `~1.5.0`) and private registries.

### Can plugins be distributed via GitHub repos?

**Yes.** This is the most common and recommended approach. Plugins can be distributed as:
- Standalone repos: `{ "source": "github", "repo": "owner/plugin-repo" }`
- Subdirectories of monorepos: `{ "source": "git-subdir", "url": "...", "path": "..." }`
- Any git host (GitLab, Bitbucket, self-hosted): `{ "source": "url", "url": "https://..." }`

All git sources support pinning to branch, tag, or exact SHA.

### Can plugins be distributed via skills.sh?

**No, not directly.** [skills.sh](https://skills.sh) is a Vercel-operated discovery/browsing portal. It displays skill metadata, install metrics, and security audits. It does not host or distribute plugins itself. It links to GitHub repos and shows `npx skills add` commands. It is a catalog UI, not a distribution mechanism.

**Source:**
- [Plugins reference -- Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)
- [Plugin marketplaces -- Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [skills.sh](https://skills.sh/anthropics/claude-plugins-official/plugin-structure)

---

## 3. Skills vs Plugins: The Key Distinction

This is a critical architectural distinction in the Claude Code ecosystem:

### Skills

- A **SKILL.md** file (with optional supporting files) in a directory
- Essentially a reusable prompt that creates a `/slash-command`
- Runs inline in the main conversation (unless `context: fork` is set)
- Stored in `.claude/skills/<name>/SKILL.md` (project) or `~/.claude/skills/<name>/SKILL.md` (personal)
- Follows the open [Agent Skills](https://agentskills.io) standard (works across Claude Code, Cursor, Codex, etc.)

### Plugins

- A **container** that bundles skills, agents, hooks, MCP servers, and LSP servers
- Has a `.claude-plugin/plugin.json` manifest
- Distributed through marketplaces
- Installed/managed via `/plugin install`, `/plugin enable`, `/plugin disable`
- Can include multiple skills, multiple agents, hook configurations, MCP server configs

### When to use which

| Use Case | Mechanism |
|---|---|
| Single reusable prompt/command | Skill |
| Complex toolkit with multiple commands + hooks + MCP servers | Plugin |
| Cross-agent portable instruction (Cursor, Codex, etc.) | Skill |
| Team-wide distribution with versioning and auto-updates | Plugin (via marketplace) |

**Sources:**
- [Extend Claude with skills -- Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Claude Code Skills vs Plugins: What's the Difference? (LLBBL Blog)](https://llbbl.blog/2026/03/05/claude-code-skills-vs-plugins.html)
- [Understanding Claude Code: Skills vs Commands vs Subagents vs Plugins](https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins)

---

## 4. `npx skills add` -- Plugins vs Skills

### What `npx skills` does

`npx skills` is the **Vercel-maintained** open-source CLI ([vercel-labs/skills](https://github.com/vercel-labs/skills)) for installing SKILL.md files across 40+ agent platforms.

**Key commands:**
```bash
npx skills add vercel-labs/agent-skills          # Install from GitHub
npx skills add vercel-labs/agent-skills --skill frontend-design -a claude-code  # Specific skill, specific agent
npx skills list                                   # Show installed skills
npx skills find typescript                        # Search for skills
npx skills remove my-skill                        # Remove a skill
```

**Supported agents:** Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, Gemini CLI, OpenCode, Roo, Kiro, and 30+ others.

### Can `npx skills add` install a full plugin?

**No.** `npx skills add` installs **individual SKILL.md files** into the appropriate skills directory for each agent. It does not understand the plugin container format (`.claude-plugin/plugin.json`), does not install hooks, MCP servers, agents, or LSP servers, and does not interact with the marketplace system.

It operates at the skill level, not the plugin level.

### Installation modes

- **Project scope (default):** Installs to `.claude/skills/<name>/` in the current project
- **Global scope (`-g`):** Installs to `~/.claude/skills/<name>/`
- **Symlink (default)** or **copy** modes available

**Sources:**
- [vercel-labs/skills (GitHub)](https://github.com/vercel-labs/skills)
- [Introducing skills, the open agent skills ecosystem (Vercel Changelog)](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)
- [skills.sh](https://skills.sh)

---

## 5. Project-Scope vs Global-Scope Plugin Installation

### Three installation scopes

| Scope | Settings File | Who Sees It | CLI Flag |
|---|---|---|---|
| **User** (default) | `~/.claude/settings.json` | You, across all projects | `--scope user` |
| **Project** | `.claude/settings.json` | Everyone who clones the repo | `--scope project` |
| **Local** | `.claude/settings.local.json` (gitignored) | You, in this project only | `--scope local` |
| **Managed** | Managed settings (admin-controlled) | All users in org | N/A (read-only) |

### How `--scope project` works

```bash
claude plugin install formatter@my-marketplace --scope project
```

This writes the plugin reference to `.claude/settings.json` under `enabledPlugins`. Since `.claude/settings.json` is committed to version control, every team member who clones the repo gets the plugin. When they trust the repository folder, Claude Code prompts them to install the marketplace and its plugins.

### Scope precedence

Project scope takes precedence over user scope for the same plugin, allowing teams to enforce project-specific configurations while developers keep personal plugins active elsewhere.

### Team marketplace auto-configuration

Admins can add `extraKnownMarketplaces` and `enabledPlugins` to `.claude/settings.json` so team members are automatically prompted:

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": { "source": "github", "repo": "your-org/claude-plugins" }
    }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true
  }
}
```

### Known issues (as of March 2026)

Multiple bugs have been reported with scope handling:
- Plugins installed at project scope in one project are hidden from the marketplace in other projects ([#27795](https://github.com/anthropics/claude-code/issues/27795))
- Local scope plugin installation incorrectly checks global state ([#16205](https://github.com/anthropics/claude-code/issues/16205))
- Plugin installed at project scope cannot be reinstalled at user scope ([#29996](https://github.com/anthropics/claude-code/issues/29996))

**Sources:**
- [Plugins reference -- Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)
- [Discover and install plugins -- Claude Code Docs](https://code.claude.com/docs/en/discover-plugins)
- [GitHub Issues: plugin scope bugs](https://github.com/anthropics/claude-code/issues/26513)

---

## 6. Alternative Package Managers & Skill Installers

### Official mechanism

The **only Anthropic-supported** mechanism is the built-in `/plugin` system with marketplace.json catalogs. Everything else is third-party.

### Third-party alternatives

| Tool | Package | Scope | Key Feature |
|---|---|---|---|
| **npx skills** | `skills` (npm) | Skills only | Vercel-maintained, 40+ agents, most popular community tool |
| **npx add-skill** | `add-skill` (npm) | Skills only | Lightweight, 4 agents (Claude Code, Cursor, Codex, OpenCode) |
| **openskills** | `openskills` (npm) | Skills only | Universal SKILL.md loader, generates AGENTS.md XML blocks |
| **CCPI** | `@intentsolutionsio/ccpi` (npm) | Plugins | npm-style package manager for a specific community marketplace |
| **cpm** | `cpm` (npm) | Plugins | Per-project Claude plugin manager with UX improvements |
| **claude-manager** | Composer plugin | Skills | PHP/Composer-based skill manager |
| **npm boilerplate** | `@your-org/skill-name` | Skills | Publish skills as npm packages with install/uninstall scripts |

### CCPI (Claude Code Plugin Installer)

```bash
pnpm add -g @intentsolutionsio/ccpi
ccpi search devops
ccpi install devops-automation-pack
ccpi list --installed
ccpi update
```

CCPI reads from a versioned catalog published at claudecodeplugins.io and provides search, install, update, and validation. It targets the [claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) marketplace specifically (340+ plugins, 1367+ skills). Not a general-purpose plugin manager.

### OpenSkills

```bash
npx openskills install anthropics/skills
npx openskills sync        # Updates AGENTS.md
npx openskills list
npx openskills read <name>
```

Implements Anthropic's Agent Skills specification but is not affiliated with Anthropic. Supports Claude Code, Cursor, Windsurf, Aider, Codex. Focuses on SKILL.md portability across agents. Does NOT handle plugins, hooks, MCP servers, or marketplace management.

### npm-published skills (via boilerplate)

Using [neovateai/agent-skill-npm-boilerplate](https://github.com/neovateai/agent-skill-npm-boilerplate):

```bash
npm install -g @your-org/skill-name       # Global install -> ~/.claude/skills/
npm install --save-dev @your-org/skill-name  # Project install -> .claude/skills/
```

npm postinstall scripts auto-detect agent directories and copy SKILL.md files. Supports Claude Code, Cursor, Windsurf. Uses semantic versioning and private registries. This is skills-only; it does not create full plugins.

**Sources:**
- [vercel-labs/skills (GitHub)](https://github.com/vercel-labs/skills)
- [numman-ali/openskills (GitHub)](https://github.com/numman-ali/openskills)
- [add-skill.org](https://add-skill.org/)
- [jeremylongshore/claude-code-plugins-plus-skills (GitHub)](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)
- [neovateai/agent-skill-npm-boilerplate (GitHub)](https://github.com/neovateai/agent-skill-npm-boilerplate)
- [open-cli-collective/cpm (GitHub)](https://github.com/open-cli-collective/cpm)

---

## 7. Summary of Key Findings

### What is clear and well-documented

1. **The official distribution mechanism is marketplace-based.** Create a `marketplace.json`, host it in a git repo, users add and install via `/plugin marketplace add` and `/plugin install`.

2. **Plugins can be sourced from GitHub, git URLs, git subdirectories, npm packages, pip packages, or relative paths.** npm is a first-class source type.

3. **Skills and plugins are different things.** A skill is a SKILL.md file. A plugin is a container that can include skills, agents, hooks, MCP servers, and LSP servers. Most third-party tools only handle skills.

4. **Three installation scopes exist:** user (global), project (shared via VCS), and local (gitignored). The `--scope project` flag writes to `.claude/settings.json`.

5. **`npx skills add` installs skills, not plugins.** It cannot install hooks, agents, MCP servers, or any full plugin. It is skills-only and agent-agnostic.

6. **CCPI, openskills, add-skill, and cpm are all community tools.** None are Anthropic-supported. They fill gaps (bulk install, cross-agent compat, npm-style UX) but are not part of the official system.

### What to watch

- **Plugin scope bugs** are actively reported (March 2026). Cross-project scope detection has known issues.
- **No declarative plugin dependencies yet.** There is an open feature request ([#27113](https://github.com/anthropics/claude-code/issues/27113)) for declaring plugin dependencies at the project level.
- **The ecosystem is fragmented.** Multiple community tools (npx skills, openskills, add-skill, CCPI) do overlapping things. The Vercel `skills` CLI appears to have the most traction.
- **Managed marketplace restrictions** (`strictKnownMarketplaces`) exist for enterprise lockdown of which marketplaces users can add.

---

## Source Index

### Official Anthropic Documentation
- [Discover and install prebuilt plugins](https://code.claude.com/docs/en/discover-plugins)
- [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

### Official Repositories
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- [anthropics/claude-code (demo marketplace)](https://github.com/anthropics/claude-code)

### Community Tools
- [vercel-labs/skills (npx skills)](https://github.com/vercel-labs/skills)
- [skills.sh (discovery portal)](https://skills.sh)
- [numman-ali/openskills](https://github.com/numman-ali/openskills)
- [add-skill.org](https://add-skill.org/)
- [neovateai/agent-skill-npm-boilerplate](https://github.com/neovateai/agent-skill-npm-boilerplate)
- [jeremylongshore/claude-code-plugins-plus-skills (CCPI)](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)
- [open-cli-collective/cpm](https://github.com/open-cli-collective/cpm)

### Community Analysis
- [Claude Code Skills vs Plugins (LLBBL Blog)](https://llbbl.blog/2026/03/05/claude-code-skills-vs-plugins.html)
- [Claude Code's Plugin Marketplace: npm for AI-Assisted Development Workflows (Medium)](https://james-sheen.medium.com/claude-codes-plugin-marketplace-npm-for-ai-assisted-development-workflows-9685333bd400)
- [Understanding Claude Code: Skills vs Commands vs Subagents vs Plugins](https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins)
- [Vercel Changelog: Introducing skills](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)
- [Claude Code Plugins Review 2026: 9,000+ Extensions (AI Tool Analysis)](https://aitoolanalysis.com/claude-code-plugins/)

### Bug Reports (Plugin Scope Issues)
- [#26513: Plugin UI shows local-scoped plugin as installed in unrelated projects](https://github.com/anthropics/claude-code/issues/26513)
- [#16205: Local scope plugin installation incorrectly checks global state](https://github.com/anthropics/claude-code/issues/16205)
- [#27795: Plugins installed with local scope hidden from marketplace in other projects](https://github.com/anthropics/claude-code/issues/27795)
- [#29996: Plugin installed at project scope cannot be reinstalled at user scope](https://github.com/anthropics/claude-code/issues/29996)
- [#27113: Feature request -- declarative plugin dependencies](https://github.com/anthropics/claude-code/issues/27113)
