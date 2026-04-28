---
content_origin: claude-code-subagent-verification
date: 2026-04-26
sub_question: "Disambiguating AGENTS.md / Agent Skills / Claude Code Skills / Skills.sh — primary-source verification of specs, governance, frontmatter, distribution"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
verification_targets: ["AGENTS.md governance/AAIF", "agentskills.io reality", "Claude Code Skills frontmatter delta", "Skills.sh as discovery vs format"]
---

# Verification: AGENTS.md, Agent Skills, Claude Code Skills, Skills.sh

The corpus assembled by upstream subagents conflated four distinct but overlapping artifacts. Direct fetches of the canonical specs, repos, and the AAIF / Linux Foundation press release resolve the relationships definitively. The short answer up front: **AGENTS.md and Agent Skills are two different specs that solve two different problems, both now travelling under the AAIF umbrella but with different maintainers; Claude Code Skills is a superset of the open Agent Skills spec; and `npx skills` is a discovery+install CLI for that same Agent Skills format, not a format of its own.**

---

## 1. AGENTS.md

### Canonical sources (verified)

- Site: `https://agents.md` (returns HTTP 200, served by Vercel; Next.js)
- Repo: `https://github.com/agentsmd/agents.md` (GitHub API confirms owner type `Organization`, name `agentsmd`, **not** `openai`)
- Repo description: *"AGENTS.md — a simple, open format for guiding coding agents"*
- License: MIT
- Stars: ~20,666 (as of 2026-04-27)
- Repo created: 2025-08-19

The corpus prompt's `github.com/openai/agents.md` reference is incorrect. While OpenAI Codex was a founding contributor, the canonical repo lives under the neutral `agentsmd` GitHub org.

### Spec contents (quoted, ≤15 words per chunk)

From `agents.md`:

- *"Think of AGENTS.md as a README for agents"*
- *"a dedicated, predictable place to provide the context and instructions"*
- *"AGENTS.md is just standard Markdown"*
- *"Use any headings you like; the agent simply parses the text you provide"*

### Frontmatter / required fields

**There are no required fields and no formal frontmatter.** AGENTS.md is plain Markdown with conventional (but optional) section headings. The example on the homepage suggests:

| Section | Required? | Purpose |
|---|---|---|
| Project overview | Optional | Orient the agent |
| Build / test commands | Optional | Reproducible commands |
| Code style | Optional | Style guidance |
| Testing instructions | Optional | How to run tests |
| Security considerations | Optional | What not to touch |
| Commit / PR guidelines | Optional | How to ship changes |
| Deployment steps | Optional | How to deploy |

Resolution rule: agents read the closest AGENTS.md to the file being edited (monorepos may nest them).

### Governance

The agents.md homepage states: *"AGENTS.md is now stewarded by the Agentic AI Foundation (AAIF) under the Linux Foundation."* AAIF was announced **December 9, 2025** with three founding project contributions: **MCP (Anthropic), Goose (Block), and AGENTS.md (OpenAI Codex et al.)**. Founding Platinum members: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI. Pre-AAIF, AGENTS.md was assembled by OpenAI Codex, Amp (Sourcegraph), Jules (Google), Cursor, and Factory.

### Adoption

Homepage cites 60,000+ open-source projects using AGENTS.md, plus first-class support across Codex, Jules, Gemini CLI, Cursor, Zed, VS Code, Warp, Aider, Devin, Windsurf, Copilot, Junie, Factory, goose, opencode, Roo Code, Augment Code, and others.

---

## 2. Agent Skills (open spec)

### Canonical sources (verified)

- Site: `https://agentskills.io` (Mintlify-hosted, redirects `/` → `/home`)
- Repo: `https://github.com/agentskills/agentskills` (GitHub API confirms owner `agentskills`, type `Organization`)
- Repo description: *"Specification and documentation for Agent Skills"*
- License: Apache-2.0 (code), CC-BY-4.0 (docs)
- Stars: ~17,255
- Repo created: 2025-12-16 (one week after AAIF launch)
- Discord: `https://discord.gg/MKPE9g8aUy`

This is real. It is **not** a community fork.

### Origin and governance — the critical clarification

The agentskills.io homepage states: *"The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products. The standard is open to contributions from the broader ecosystem."* The repo README confirms: *"Agent Skills is an open format maintained by Anthropic and open to contributions from the community."*

**Governance status as of 2026-04-26:** Agent Skills is **not** under AAIF. It remains Anthropic-stewarded with community contributions. The AAIF press release lists only MCP, Goose, and AGENTS.md as founding contributions — Agent Skills was **not** part of the December 2025 AAIF launch. (This is a meaningful asymmetry: AGENTS.md is foundation-governed, Agent Skills is vendor-stewarded but openly licensed.)

### Frontmatter (verbatim from `agentskills.io/specification`)

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | Max 64 chars; lowercase a-z, digits, hyphens; no leading/trailing/consecutive hyphens; must match parent directory name |
| `description` | Yes | Max 1024 chars; non-empty; what + when to use |
| `license` | No | License name or reference to bundled file |
| `compatibility` | No | Max 500 chars; environment requirements |
| `metadata` | No | Arbitrary string-to-string map |
| `allowed-tools` | No | Space-separated tool list (**experimental**) |

Directory layout (verbatim from spec):

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...
```

### Progressive disclosure model (quoted from spec)

1. *"Metadata (~100 tokens): The name and description fields are loaded at startup"*
2. *"Instructions (< 5000 tokens recommended): The full SKILL.md body is loaded when the skill is activated"*
3. *"Resources (as needed): Files... are loaded only when required"*

Recommendation: keep `SKILL.md` under 500 lines.

### Validation tooling

The spec ships a reference validator: `skills-ref validate ./my-skill` (located at `github.com/agentskills/agentskills/tree/main/skills-ref`).

### Released

Released as an open standard in late 2025. Repo created 2025-12-16. Adopters listed on `/home` as of April 2026 include Junie, Gemini CLI, Cursor, OpenCode, OpenHands, Mux, Amp, Letta, Firebender, Goose, GitHub Copilot, VS Code, Claude Code, Claude.ai, OpenAI Codex, Factory, Databricks Genie, TRAE, Spring AI, Roo Code, Mistral Vibe, Ona, Kiro, Workshop, Laravel Boost, Snowflake Cortex Code, Emdash, fast-agent, and ~14 others.

---

## 3. Anthropic Claude Code Skills

### Canonical sources (verified)

- `https://docs.claude.com/en/docs/claude-code/skills` 301-redirects to `https://code.claude.com/docs/en/skills`
- Anthropic explicitly anchors this doc to the open spec: *"Claude Code skills follow the Agent Skills open standard, which works across multiple AI tools."*

### Storage locations (verbatim)

| Location | Path | Applies to |
|---|---|---|
| Enterprise | managed settings | All users in org |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled |

Override priority: enterprise > personal > project. Plugin skills are namespaced (`plugin-name:skill-name`).

### Frontmatter — Claude Code's superset

Claude Code's frontmatter is a strict **superset** of the open Agent Skills spec. All Agent Skills fields are accepted; Claude Code adds the following Claude-Code-only extensions (none of these appear in the agentskills.io specification):

| Field | Required | Claude-Code-only? | Description |
|---|---|---|---|
| `name` | No (defaults to dir) | No (open spec requires it) | Display name; max 64 chars; lowercase + hyphens |
| `description` | Recommended | No | What/when; combined with `when_to_use` capped at 1,536 chars in listing |
| `when_to_use` | No | **Yes** | Trigger phrases / examples; appended to description |
| `argument-hint` | No | **Yes** | Autocomplete hint, e.g. `[issue-number]` |
| `arguments` | No | **Yes** | Named positional args mapped to `$name` substitutions |
| `disable-model-invocation` | No | **Yes** | Prevent Claude from auto-loading; manual `/name` only |
| `user-invocable` | No | **Yes** | Hide from `/` menu (Claude-only invocation) |
| `allowed-tools` | No | Shared (open spec marks experimental; Claude Code productized) | Pre-approved tools |
| `model` | No | **Yes** | Override session model for the turn |
| `effort` | No | **Yes** | Effort level: low/medium/high/xhigh/max |
| `context` | No | **Yes** | `fork` runs the skill in a subagent context |
| `agent` | No | **Yes** | Subagent type (`Explore`, `Plan`, `general-purpose`, custom) |
| `hooks` | No | **Yes** | Skill-scoped lifecycle hooks |
| `paths` | No | **Yes** | Glob patterns to gate auto-activation |
| `shell` | No | **Yes** | `bash` (default) or `powershell` |

The open Agent Skills fields **not** carried into Claude Code's docs explicitly: `compatibility`, `metadata` (these are honored as unknown-but-permitted via the open spec, but Claude Code's frontmatter reference does not document them).

### Claude Code-specific behaviors

- *"Custom commands have been merged into skills."* `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`.
- Live change detection inside `~/.claude/skills/`, project `.claude/skills/`, and `--add-dir` directories.
- String substitutions: `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_SKILL_DIR}`.
- Inline shell injection via `` !`<command>` `` and ` ```! ` blocks (preprocessing, not Claude execution). Disable globally with `disableSkillShellExecution: true`.
- Skill content lifecycle: rendered SKILL.md enters conversation as a single message and persists; auto-compaction re-attaches first 5,000 tokens of each invoked skill within a 25,000-token combined budget.
- Description budget: 1% of context window, fallback 8,000 chars; per-entry cap 1,536 chars. Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET`.

### Net Claude-Code-only delta

`when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`. A SKILL.md authored against pure agentskills.io will work in Claude Code; a SKILL.md authored against Claude Code's full frontmatter will be **partially honored** elsewhere — every other consumer must ignore unknown keys per the open spec's `metadata` philosophy, and most do.

---

## 4. Skills.sh / `npx skills`

### Canonical sources (verified)

- Site: `https://skills.sh` — Vercel-hosted Next.js, *"Made with love by Vercel"*. Indexes 90,994+ skills.
- Repo: `https://github.com/vercel-labs/skills` (raw README fetched verbatim)
- License: MIT
- Stars: ~16,163
- Repo created: 2026-01-14
- Latest release v1.5.1 (2026-04-17), 25 releases, 254 commits — actively maintained

### What it is (resolved)

**Discovery + install over the open Agent Skills format. Not a separate format.** The README opens: *"The CLI for the open agent skills ecosystem."* It supports OpenCode, Claude Code, Codex, Cursor, *"and 41 more"* agents.

### Command surface (verbatim from README)

The installer command is **`npx skills add <pkg>`** (the corpus prompt's "`install`" was wrong). Other commands:

- `npx skills add <source>` — install from GitHub shorthand, GitHub URL, sub-path, GitLab URL, any git URL, or local path
- `npx skills list` (alias `ls`) — list installed
- `npx skills find [query]` — fzf-style or keyword search
- `npx skills remove [skills]` (alias `rm`)
- `npx skills update [skills]`
- `npx skills init [name]` — scaffold a new SKILL.md

Source formats accepted:
```
npx skills add vercel-labs/agent-skills
npx skills add https://github.com/vercel-labs/agent-skills
npx skills add https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines
npx skills add https://gitlab.com/org/repo
npx skills add git@github.com:vercel-labs/agent-skills.git
npx skills add ./my-local-skills
```

Key flags: `-g/--global`, `-a/--agent`, `-s/--skill`, `-l/--list`, `--copy` (vs. default symlink), `-y/--yes`, `--all`.

### Indexing model

No central registry. Discovery is repo-driven:
- Scans source repos for `SKILL.md` files at `skills/`, `skills/.curated/`, `.claude/skills/`, etc.
- Reads plugin manifests (`.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`)
- skills.sh acts as a portal/aggregator (90,994 skills indexed) but the CLI itself does local repo scanning, not registry calls

### Install paths — `.agents/skills/` vs `.agent/skills/` — resolved (verbatim from README)

| Agent | Project path | Global path |
|---|---|---|
| Claude Code | `./.claude/skills/` | `~/.claude/skills/` |
| Cursor | `./.agents/skills/` | `~/.cursor/skills/` |
| OpenCode | `./.agents/skills/` | `~/.config/opencode/skills/` |
| Codex | `./.agents/skills/` | `~/.codex/skills/` |

The convergent project-level convention for non-Claude agents is **`.agents/skills/`** (plural, with the `s`). The singular `.agent/skills/` form does not appear anywhere in the canonical README — that's a stray artifact in the corpus, likely a typo. Claude Code remains the outlier with `.claude/skills/`.

Default install method is **symlink** to a canonical local copy (so editing once propagates to every agent). `--copy` falls back to independent copies.

---

## Cross-resolution comparison

| Dimension | AGENTS.md | Agent Skills (open) | Claude Code Skills | Skills.sh / `npx skills` |
|---|---|---|---|---|
| **Governance** | AAIF / Linux Foundation (since 2025-12-09) | Anthropic-stewarded, Apache-2.0 / CC-BY-4.0, community PRs | Anthropic (Claude Code product team); follows open spec | Vercel Labs, MIT |
| **Canonical site** | agents.md | agentskills.io | code.claude.com/docs/en/skills | skills.sh |
| **Canonical repo** | github.com/agentsmd/agents.md | github.com/agentskills/agentskills | (closed product; no public spec repo) | github.com/vercel-labs/skills |
| **License** | MIT | Apache-2.0 + CC-BY-4.0 | Proprietary product, follows open spec | MIT |
| **File format** | Single `AGENTS.md` (plain Markdown, no frontmatter) | Directory + `SKILL.md` (YAML frontmatter + Markdown) | Directory + `SKILL.md` (superset of open spec) | Same as open Agent Skills (consumes, does not redefine) |
| **Required fields** | None | `name`, `description` | None required (`description` recommended) | N/A — operates over Agent Skills format |
| **Optional fields** | Conventional sections | `license`, `compatibility`, `metadata`, `allowed-tools` | 12+ Claude-Code-only fields (see §3) | N/A |
| **Distribution** | Commit a file in repo root | Commit a folder; share via repo | `.claude/skills/` (project / personal / plugin / managed) | Symlink or copy from any git source into agent-specific dirs |
| **Discovery** | Agent reads file at task start | Agent loads name+description at startup, body on activation | Same as open spec, plus `paths` glob gating, plus `disable-model-invocation` toggle | CLI scans repos, skills.sh portal aggregates |
| **Consumer role** | Agent reads passively as project context | Agent loads progressively, can execute scripts | Claude Code loads, can fork to subagent, can pre-approve tools, can inject shell output | CLI is producer-side; consumers are still the agents above |
| **Founded / released** | 2025-08 (repo); AAIF stewardship 2025-12-09 | Late 2025; repo 2025-12-16 | Late 2025 (Claude Code product release) | 2026-01-14 (repo), v1.5.1 in April 2026 |
| **Adoption count (claimed)** | 60,000+ projects | 38+ first-class clients | All Claude Code installs | 90,994 skills indexed; 45+ supported agents |

---

## If a practice author writes ONE SKILL.md today, who consumes it without modification?

**Setup:** A `SKILL.md` containing only the open Agent Skills frontmatter — `name`, `description`, optionally `license`, `compatibility`, `metadata`, `allowed-tools` — placed in a directory matching the `name`, with a Markdown body under 500 lines. No Claude-Code-only fields.

**Consumed without modification by every client listed on agentskills.io/home as of 2026-04-26**, citing per-client documentation links the agentskills.io page provides:

- **Claude Code** — *"Claude Code skills follow the Agent Skills open standard"* (code.claude.com/docs/en/skills)
- **Claude.ai** — platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **OpenAI Codex** — developers.openai.com/codex/skills/
- **Cursor** — cursor.com/docs/context/skills
- **GitHub Copilot** — docs.github.com/en/copilot/concepts/agents/about-agent-skills
- **VS Code** — code.visualstudio.com/docs/copilot/customization/agent-skills
- **Gemini CLI** — geminicli.com/docs/cli/skills/
- **JetBrains Junie** — junie.jetbrains.com/docs/agent-skills.html
- **Goose** (Block) — block.github.io/goose/docs/guides/context-engineering/using-skills/
- **OpenCode** — opencode.ai/docs/skills/
- **OpenHands** — docs.openhands.dev/overview/skills
- **Amp** — ampcode.com/manual#agent-skills
- **Letta**, **Firebender**, **Roo Code**, **Factory**, **Mistral Vibe**, **Spring AI**, **Snowflake Cortex Code**, **Databricks Genie Code**, **Kiro**, **Mux**, **Ona**, **TRAE**, **Workshop**, **Emdash**, **fast-agent**, **Laravel Boost**, **Qodo**, **Agentman**, **Command Code**, **Piebald**, **VT Code**, **pi**, **nanobot**, **Google AI Edge Gallery**, **Autohand Code CLI**

**Distribution paths the same single skill lands in (via `npx skills add`):**

- Claude Code: `./.claude/skills/<name>/` or `~/.claude/skills/<name>/`
- Cursor / OpenCode / Codex: `./.agents/skills/<name>/` (project) or per-agent global dir
- Other agents: each agent's documented skills directory, brokered by `npx skills` symlinks

**Not consumed by AGENTS.md-only tools** — AGENTS.md and Agent Skills are different specs solving different problems (project-wide context file vs. invocable capability bundle). For maximum reach, a practice module needs both: an AGENTS.md at repo root for ambient guidance, and one-or-more SKILL.md packages for invocable capabilities.

**Risk of writing only Claude-Code-extended SKILL.md:** Other agents will silently ignore Claude-Code-only fields (`disable-model-invocation`, `context: fork`, `agent`, `paths`, `model`, `effort`, `hooks`, `arguments`, `argument-hint`, `when_to_use`, `shell`, `user-invocable`). Behaviorally critical guards — e.g., `disable-model-invocation: true` to prevent auto-deploy — will be **silently dropped** outside Claude Code. A skill that depends on `context: fork` for isolation will run inline elsewhere. **For portable practice modules, gate Claude-Code-only fields behind a Claude-Code-specific copy of the SKILL.md or a plugin variant.**

---

## Source-of-truth question — resolved

**Is `agentskills.io` a separate document from Anthropic's Claude Code Skills docs, or a community fork?**

It is a **separate, real, Anthropic-maintained open-spec project** released alongside the Claude Code product. Repo and org (`agentskills/agentskills`) are public, Apache-2.0 licensed, accept community PRs, and are explicitly cited by Anthropic's own Claude Code documentation as the upstream standard. Claude Code Skills is a **superset implementation** of the open spec — Anthropic ships both the spec and its own extended consumer.

It is **not yet under AAIF**. The AAIF founding contributions (2025-12-09) were MCP, Goose, and AGENTS.md. Whether Agent Skills will be contributed to AAIF in a future tranche is unstated in any source fetched here.

---

## Citations (primary sources fetched)

- `https://agents.md` — homepage (HTTP 200, Vercel-hosted)
- `https://github.com/agentsmd/agents.md` — GitHub API metadata
- `https://agentskills.io/home` — overview + adopter list
- `https://agentskills.io/specification` — formal spec
- `https://github.com/agentskills/agentskills` — repo, README, GitHub API metadata
- `https://code.claude.com/docs/en/skills` — Claude Code Skills full docs
- `https://skills.sh` — directory portal (HTTP 200, Vercel)
- `https://github.com/vercel-labs/skills` — README fetched raw via `raw.githubusercontent.com`
- `https://aaif.io` — AAIF home, Linux Foundation branding confirmed
- `https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation` — AAIF founding press release
- WebSearch corroboration: PR Newswire, OpenAI announcement, Block announcement, Pure AI coverage (all consistent: AAIF founded 2025-12-09; founding contributions MCP+Goose+AGENTS.md)
