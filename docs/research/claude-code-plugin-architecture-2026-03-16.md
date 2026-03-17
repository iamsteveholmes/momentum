# Claude Code Plugin Architecture Patterns -- Research Findings (2026-03-16)

> Technical research on Claude Code plugin structure, skill composition, directory layout, and versioning patterns. All findings sourced from 2026-era documentation and community practice.

---

## 1. Plugin Architecture: Portable Skills + Claude Code-Specific Enforcement

### The Plugin Anatomy

A Claude Code plugin is a self-contained directory that bundles **portable Agent Skills** alongside **Claude Code-specific enforcement mechanisms** (hooks, agents, settings, MCP/LSP servers). The `.claude-plugin/plugin.json` manifest is the only file that goes inside `.claude-plugin/`; all other directories sit at the plugin root.

**Canonical directory layout** (from official docs):

```
enterprise-plugin/
├── .claude-plugin/
│   └── plugin.json           # Manifest metadata (only file inside .claude-plugin/)
├── skills/                   # Portable Agent Skills (SKILL.md per skill)
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       ├── reference.md
│       └── scripts/
├── agents/                   # Claude Code subagent definitions
│   ├── security-reviewer.md
│   └── compliance-checker.md
├── commands/                 # Legacy slash commands (still supported)
│   └── status.md
├── hooks/                    # Claude Code lifecycle hooks
│   └── hooks.json
├── settings.json             # Default settings (currently only `agent` key)
├── .mcp.json                 # MCP server configurations
├── .lsp.json                 # LSP server configurations
├── scripts/                  # Hook and utility scripts
│   └── format-code.py
├── LICENSE
└── CHANGELOG.md
```

Source: [Create plugins -- Claude Code Docs](https://code.claude.com/docs/en/plugins), [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

### Portable vs. Claude Code-Specific Split

| Layer | Files | Portability |
|-------|-------|-------------|
| **Portable Skills** | `skills/*/SKILL.md` + supporting files | Follow the [Agent Skills](https://agentskills.io) open standard; work across Claude Code, Agent SDK, API, and claude.ai |
| **CC-Specific Enforcement** | `hooks/hooks.json`, `agents/*.md`, `.mcp.json`, `.lsp.json`, `settings.json` | Claude Code only |
| **Metadata** | `.claude-plugin/plugin.json` | Claude Code plugin system |

Skills are the portable unit. They use YAML frontmatter (`name`, `description`) and markdown body, following the Agent Skills open standard. Hooks, agents, MCP servers, and LSP configurations are Claude Code runtime features.

Source: [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### Namespacing and Conflict Prevention

Plugin skills are namespaced as `/plugin-name:skill-name`, preventing conflicts when multiple plugins define skills with the same name. Standalone skills in `.claude/skills/` use short names like `/deploy`.

Source: [Create plugins](https://code.claude.com/docs/en/plugins)

### Environment Variables for Portability

- `${CLAUDE_PLUGIN_ROOT}` -- absolute path to the plugin installation directory. Required in hooks, MCP configs, and scripts to ensure portability across installations.
- `${CLAUDE_SKILL_DIR}` -- path to the skill's own directory (useful for referencing bundled scripts).
- `${CLAUDE_SESSION_ID}` -- current session ID.

Source: [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

---

## 2. Skill Composition Patterns

### 2.1 Progressive Disclosure Architecture

Skills use a three-tier loading model to conserve context window tokens:

1. **Metadata loading (~100 tokens)**: Only `name` and `description` from YAML frontmatter are loaded at startup. The context budget scales at 2% of the context window (fallback: 16,000 chars).
2. **Full instructions (<5k tokens)**: `SKILL.md` body loads when the skill becomes relevant.
3. **Bundled resources (on demand)**: Supporting files (`reference.md`, `examples.md`, scripts) load only when Claude decides to read them.

Source: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Extend Claude with skills](https://code.claude.com/docs/en/skills)

### 2.2 Subagent-Skill Composition (Two Directions)

Skills and subagents compose in **two inverse directions**:

| Approach | System Prompt | Task/Content | Also Loads |
|----------|--------------|--------------|------------|
| **Skill with `context: fork`** | From agent type (`Explore`, `Plan`, etc.) | SKILL.md content becomes the prompt | CLAUDE.md |
| **Subagent with `skills:` field** | Subagent's markdown body | Claude's delegation message | Full skill content injected at startup + CLAUDE.md |

**Direction 1: Skill drives, agent executes.** A skill with `context: fork` and `agent: Explore` spawns an isolated subagent where the skill content becomes the task:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly...
```

**Direction 2: Agent drives, skills provide knowledge.** A subagent preloads skills via the `skills:` frontmatter field. Full skill content is injected into the subagent's context at startup:

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---
Implement API endpoints. Follow the conventions from the preloaded skills.
```

Source: [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Create custom subagents](https://code.claude.com/docs/en/sub-agents)

### 2.3 Chaining Patterns

**Sequential chaining** -- Claude orchestrates subagents in sequence from the main conversation. Each subagent completes its task and returns results, which Claude passes to the next:

```
Use the code-reviewer subagent to find performance issues,
then use the optimizer subagent to fix them
```

**Parallel spawning** -- Multiple subagents run concurrently for independent investigations:

```
Research the authentication, database, and API modules in parallel using separate subagents
```

**Skill-to-skill hints** -- Skills can reference other skills in their content, acting as emphasized hints. Claude's auto-discovery handles the resolution.

**Subagents cannot spawn other subagents.** This is a hard constraint. For nested delegation, chain subagents from the main conversation or use skills.

Source: [Create custom subagents](https://code.claude.com/docs/en/sub-agents)

### 2.4 The Compound Engineering Pattern (Real-World Example)

The [Compound Engineering Plugin](https://github.com/EveryInc/compound-engineering-plugin) from Every demonstrates a production composition pattern with 26 agents, 13 skills, and 23 commands:

| Phase | Command | Purpose |
|-------|---------|---------|
| Exploration | `/ce:brainstorm` | Requirements clarification via dialogue |
| Strategy | `/ce:plan` | Sub-agents research codebase in parallel, produce implementation roadmap |
| Execution | `/ce:work` | Worktrees, task tracking, code changes |
| Validation | `/ce:review` | Multi-agent code assessment (security, architecture, quality) |

**Composition hierarchy**: Commands invoke agents as entry points. Agents orchestrate multi-step workflows, calling skills as subtasks. Skills handle focused, repeatable operations. This separation enables skill reuse across multiple agents.

Source: [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin), [Compound Engineering: How Every Codes With Agents](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents)

### 2.5 Agentic Pattern Mapping

Anthropic's canonical agentic patterns map to Claude Code primitives:

| Agentic Pattern | Claude Code Primitive |
|-----------------|----------------------|
| Prompt Chaining | Plan mode + Skills |
| Routing | Conditional CLAUDE.md |
| Parallelization | Sub-agents / Agent Teams |
| Orchestrator-Workers | Agent tool (sub-agents) |
| Evaluator-Optimizer | Inline skill (`/evaluate`) |

Source: [4 Agentic AI Patterns You Already Use in Claude Code](https://wmedia.es/en/tips/claude-code-agentic-ai-five-patterns)

---

## 3. Directory Layout Best Practices (Real-World Examples)

### 3.1 Official Reference Implementation

The `anthropics/claude-code` repository contains a `plugins/` directory with example plugins demonstrating the standard layout. The official marketplace at `anthropics/claude-plugins-official` maintains a curated directory (12.1k stars, 131 commits) organized as:

```
claude-plugins-official/
├── /plugins                 # Anthropic-maintained plugins
├── /external_plugins        # Third-party approved plugins
├── .claude-plugin/
│   └── marketplace.json     # Marketplace catalog
└── README.md
```

Source: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), [anthropics/claude-code/plugins](https://github.com/anthropics/claude-code/tree/main/plugins)

### 3.2 Community Ecosystem Patterns (from awesome-claude-code)

The [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) curated list catalogs the ecosystem with these observed patterns:

- **Modular Skills**: Independent YAML files combining prompts, tools, and configurations
- **Hook-based Integration**: Trigger points at task planning, execution, validation lifecycle phases
- **MCP Server Integration**: External tool access through Model Context Protocol
- **Sub-agent Orchestration**: Specialized agents handling distinct workflow phases

**Notable architectures**:
- Hook SDKs with clean Python APIs (e.g., `cchooks`)
- Prompt injection scanning hooks (e.g., `parry`)
- Circuit breaker patterns in task runners
- Git worktree-based isolation for parallel execution

Source: [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

### 3.3 Skill Directory Patterns (from official best practices)

**Simple skill**: Just `SKILL.md`

**Skill with supporting files** (recommended for complex skills):
```
my-skill/
├── SKILL.md              # Main instructions (required, <500 lines)
├── reference.md          # Detailed API docs (loaded on demand)
├── examples.md           # Usage examples (loaded on demand)
└── scripts/
    └── validate.py       # Utility script (executed, not loaded)
```

**Domain-organized skill**:
```
bigquery-skill/
├── SKILL.md              # Overview and navigation
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

**Key rules**:
- Keep SKILL.md body under 500 lines
- Keep references one level deep from SKILL.md (avoid deeply nested references)
- Name files descriptively (`form_validation_rules.md`, not `doc2.md`)
- Use forward slashes only (even on Windows)
- Structure longer reference files with a table of contents

Source: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### 3.4 Plugin with Multiple Concerns

For plugins combining portable skills with enforcement:

```
my-practice-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/                    # PORTABLE: Agent Skills standard
│   ├── code-review/
│   │   ├── SKILL.md
│   │   └── checklist.md
│   └── test-strategy/
│       ├── SKILL.md
│       └── templates/
├── agents/                    # CC-SPECIFIC: subagent definitions
│   ├── security-reviewer.md
│   └── quality-gatekeeper.md
├── hooks/                     # CC-SPECIFIC: lifecycle enforcement
│   └── hooks.json
├── scripts/                   # CC-SPECIFIC: hook implementation
│   ├── lint-on-save.sh
│   └── block-force-push.sh
├── .mcp.json                  # CC-SPECIFIC: external tools
├── settings.json              # CC-SPECIFIC: default agent setting
└── README.md
```

Source: Synthesized from [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

---

## 4. Versioning, Updates, and Dependency Management

### 4.1 Semantic Versioning

Plugins use semantic versioning (`MAJOR.MINOR.PATCH`) in `plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes

Pre-release versions supported (e.g., `2.0.0-beta.1`).

**Critical**: Claude Code uses the version to determine whether to update. If you change code but don't bump the version, existing users won't see changes due to caching.

Source: [Plugins reference -- Version management](https://code.claude.com/docs/en/plugins-reference#version-management)

### 4.2 Version Resolution Between Manifest and Marketplace

Version can be set in either `plugin.json` or `marketplace.json`. **`plugin.json` always wins silently.** Best practice:
- For relative-path plugins (inside the marketplace repo): set version in `marketplace.json`
- For all other plugin sources (GitHub, npm, git): set version in `plugin.json`
- Avoid setting version in both places

Source: [Plugin marketplaces -- Version resolution](https://code.claude.com/docs/en/plugin-marketplaces)

### 4.3 Auto-Update Mechanism

Claude Code can automatically update marketplaces and their installed plugins at startup:

- **Official Anthropic marketplaces**: auto-update enabled by default
- **Third-party/local marketplaces**: auto-update disabled by default
- Toggle per-marketplace via `/plugin > Marketplaces > Enable/Disable auto-update`

Environment variable controls:
- `DISABLE_AUTOUPDATER=true` -- disables all auto-updates (Claude Code + plugins)
- `FORCE_AUTOUPDATE_PLUGINS=true` -- re-enables plugin auto-updates when autoupdater is disabled

Source: [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)

### 4.4 Plugin Caching

Installed marketplace plugins are copied to `~/.claude/plugins/cache/` (separate folders per version). Plugins cannot reference files outside their directory after installation -- paths like `../shared-utils` will fail. Workaround: create symbolic links within the plugin directory; symlinks are followed during the copy process.

Source: [Plugins reference -- Plugin caching](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)

### 4.5 Known Issues (March 2026)

- **Stale cache on update**: The update logic runs `git fetch` on the marketplace repo clone but historically did not always run `git merge`, leaving the working tree on old commits. Fixed in recent March 2026 releases.
- **Merge conflict on pinned refs**: `/plugin marketplace update` could fail with merge conflicts when the marketplace is pinned to a branch/tag ref. Also fixed recently.

Source: [Plugin update doesn't fetch new version (Issue #21995)](https://github.com/anthropics/claude-code/issues/21995), [Plugin update detection (Issue #31462)](https://github.com/anthropics/claude-code/issues/31462)

### 4.6 Release Channels

To support stable/latest channels, create two marketplace definitions pointing at different refs of the same repo:

```json
// stable-marketplace.json
{ "source": { "source": "github", "repo": "acme/plugin", "ref": "stable" } }

// latest-marketplace.json
{ "source": { "source": "github", "repo": "acme/plugin", "ref": "latest" } }
```

Assign different user groups to different marketplaces via managed settings. The `plugin.json` must declare a different `version` at each pinned ref.

Source: [Plugin marketplaces -- Release channels](https://code.claude.com/docs/en/plugin-marketplaces)

### 4.7 Dependency Management

There is **no formal dependency mechanism** between plugins. Claude Code's plugin system does not support:
- Plugin-to-plugin dependencies
- Skill-to-skill explicit imports
- Transitive dependency resolution

**Workarounds observed in practice**:
- Skills reference other skills by name in their content (hint-based, not enforced)
- Subagents preload specific skills via the `skills:` frontmatter field
- MCP servers provide external tool dependencies
- Plugin source types include `npm` (with `version` and `registry`) and `pip` for package-managed distribution, but this manages the plugin's own packaging, not inter-plugin deps

Source: [Plugin marketplaces schema](https://code.claude.com/docs/en/plugin-marketplaces), [Extend Claude with skills](https://code.claude.com/docs/en/skills)

### 4.8 Installation Scopes

| Scope | Settings File | Use Case |
|-------|--------------|----------|
| `user` | `~/.claude/settings.json` | Personal, all projects (default) |
| `project` | `.claude/settings.json` | Team-shared via version control |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | Managed settings (read-only) | Organization-wide enforcement |

Source: [Plugins reference -- Installation scopes](https://code.claude.com/docs/en/plugins-reference#plugin-installation-scopes)

---

## 5. Key Takeaways for Plugin Design

1. **Separate portable from platform-specific.** Skills (`skills/*/SKILL.md`) are portable across the Agent Skills ecosystem. Hooks, agents, MCP/LSP configs are Claude Code-specific. Design the boundary deliberately.

2. **Composition is hierarchical, not dependency-based.** There is no import system. Composition happens through: (a) subagents preloading skills, (b) skills forking into subagent contexts, (c) sequential chaining from the main conversation, and (d) hooks enforcing policy at lifecycle points.

3. **Progressive disclosure is the performance model.** Keep SKILL.md under 500 lines. Bundle reference material in separate files. Context tokens are a shared resource.

4. **Version management requires discipline.** Always bump `plugin.json` version when changing code. Prefer setting version in one place only. Use release channels for staged rollouts.

5. **No inter-plugin dependencies.** Design plugins as self-contained units. If shared knowledge is needed, preload it via the `skills:` field on subagents or reference it from skill content.

6. **The Compound Engineering pattern is the current state-of-the-art** for multi-phase workflows: Plan (parallel research) -> Work (execution with isolation) -> Review (multi-agent assessment) -> Compound (capture learnings). This pattern, with 26 agents and 13 skills, demonstrates production-grade skill composition.

---

## Sources

- [Create plugins -- Claude Code Docs](https://code.claude.com/docs/en/plugins)
- [Plugins reference -- Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)
- [Extend Claude with skills -- Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Hooks reference -- Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [Create custom subagents -- Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Discover and install plugins -- Claude Code Docs](https://code.claude.com/docs/en/discover-plugins)
- [Plugin marketplaces -- Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [Skill authoring best practices -- Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [anthropics/claude-plugins-official (GitHub)](https://github.com/anthropics/claude-plugins-official)
- [anthropics/claude-code/plugins (GitHub)](https://github.com/anthropics/claude-code/tree/main/plugins)
- [hesreallyhim/awesome-claude-code (GitHub)](https://github.com/hesreallyhim/awesome-claude-code)
- [EveryInc/compound-engineering-plugin (GitHub)](https://github.com/EveryInc/compound-engineering-plugin)
- [Plugin update Issue #21995](https://github.com/anthropics/claude-code/issues/21995)
- [Plugin update detection Issue #31462](https://github.com/anthropics/claude-code/issues/31462)
- [4 Agentic AI Patterns in Claude Code (wmedia.es)](https://wmedia.es/en/tips/claude-code-agentic-ai-five-patterns)
- [Compound Engineering: How Every Codes With Agents](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents)
- [Best Claude Code Plugins, Skills & MCP Servers 2026 (TurboDocx)](https://www.turbodocx.com/blog/best-claude-code-skills-plugins-mcp-servers)
- [A Mental Model for Claude Code: Skills, Subagents, and Plugins (Level Up Coding)](https://levelup.gitconnected.com/a-mental-model-for-claude-code-skills-subagents-and-plugins-3dea9924bf05)
- [Claude Code Hooks Guide 2026 (DEV Community)](https://dev.to/serenitiesai/claude-code-hooks-guide-2026-automate-your-ai-coding-workflow-dde)
- [Keeping Claude Code plugins up to date (workingbruno.com)](https://workingbruno.com/notes/keeping-claude-code-plugins-date)
