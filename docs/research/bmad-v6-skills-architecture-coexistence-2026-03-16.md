# BMAD V6 Skills Architecture and Coexistence with Custom Skills in Claude Code

**Research Date:** 2026-03-16
**Scope:** How BMAD Method V6 packages skills, how they coexist with other skill sources, manifest formats, and conflict resolution

---

## 1. BMAD's Current Skills Architecture (V6.x)

### 1.1 Architectural Evolution: Everything Became a Skill

BMAD V6.1.0 (March 13, 2026) was described as "the biggest architectural overhaul since v6." The core change: **every workflow, agent, and task now installs as a unified skill** with standardized `SKILL.md` entrypoints. Legacy XML/YAML workflow engine plumbing was removed entirely. The npm package shrank 91% (6.2 MB to 555 KB) as a result.

V6.2.0 (March 15, 2026) continued the transformation with ~25+ workflows converted into native skill directory structures, a skill validator tool, and standardized path references using `{project-root}` syntax.

As of today (March 16, 2026), PR #2021 "Feat/conformant agent skills" merged, converting the remaining agent definitions from `.agent.yaml` files into conformant Agent Skills directories containing `SKILL.md`, `bmad-manifest.json`, and `bmad-skill-manifest.yaml`.

**Sources:**
- [BMAD-METHOD Releases](https://github.com/bmad-code-org/BMAD-METHOD/releases)
- [BMAD-METHOD CHANGELOG.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/CHANGELOG.md)
- [PR #2021: Feat/conformant agent skills](https://github.com/bmad-code-org/BMAD-METHOD/pull/2021)

### 1.2 How BMAD Packages Skills

BMAD uses a **module + installer** architecture:

1. **Modules** are the organizational unit. The local install at `/Users/steve/projects/momentum` has 5 modules:
   - `core` (v6.2.0, built-in) -- master agent, help, editorial tools, brainstorming
   - `bmm` (v6.2.0, built-in) -- the main method: analysts, architects, PMs, devs, workflows
   - `bmb` (v1.0.2, external npm: `bmad-builder`) -- builder tools for creating agents/workflows
   - `cis` (v0.1.8, external npm: `bmad-creative-intelligence-suite`) -- innovation, storytelling, design thinking
   - `tea` (v1.7.0, external npm: `bmad-method-test-architecture-enterprise`) -- test architecture workflows

2. **The installer** (`npx bmad-method install`) reads manifests for every selected module and writes one skill per agent, workflow, task, and tool. Each skill is a directory containing a `SKILL.md` file.

3. **Installation location** is IDE-specific. For Claude Code, skills are written to `.claude/skills/`. The directory name becomes the slash command (e.g., `.claude/skills/bmad-dev/` registers as `/bmad-dev`).

**Source:** [How to Install BMad](https://docs.bmad-method.org/how-to/install-bmad/), [BMAD Skills Reference](https://docs.bmad-method.org/reference/commands/)

### 1.3 Installed Skill Structure

The installed skills are **thin stubs** that reference source files in `_bmad/`. A typical installed skill:

```yaml
# .claude/skills/bmad-code-review/SKILL.md
---
name: bmad-code-review
description: 'Review code changes adversarially using parallel review layers...'
---

Follow the instructions in ./workflow.md.
```

The actual workflow logic lives in supporting files within the skill directory (e.g., `workflow.md`, `discover-inputs.md`, `checklist.md`). The stub + reference pattern keeps `SKILL.md` under the recommended 500-line / 5K-token limit per the Agent Skills spec's progressive disclosure model.

### 1.4 Skill Count

This project has **68 BMAD skills** installed to `.claude/skills/`, spanning:
- 13 agent personas (bmad-master, bmad-analyst, bmad-architect, bmad-dev, bmad-pm, etc.)
- ~30 workflow skills (create-prd, create-architecture, dev-story, code-review, etc.)
- ~12 task/tool skills (editorial-review, shard-doc, index-docs, etc.)
- 9 TEA test architecture skills
- 4 CIS creative intelligence skills

All use the `bmad-` prefix convention.

---

## 2. How BMAD Skills Coexist with Other Skill Sources

### 2.1 Claude Code Skill Discovery Hierarchy

Claude Code discovers skills from multiple locations with a defined priority order:

| Location | Path | Scope | Priority |
|----------|------|-------|----------|
| Enterprise | Managed settings | All users in org | Highest |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects | High |
| Project | `.claude/skills/<name>/SKILL.md` | This project only | Medium |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin enabled | Namespaced separately |
| Nested (monorepo) | `packages/X/.claude/skills/` | Subdirectory scope | Discovered contextually |
| Additional dirs | Via `--add-dir` | Session scope | Live reload supported |

**When skills share the same name across levels, higher-priority locations win:** enterprise > personal > project.

**Plugin skills use `plugin-name:skill-name` namespace**, so they **cannot** conflict with other levels. A plugin skill named `hello` in plugin `my-plugin` is invoked as `/my-plugin:hello`, never as `/hello`.

If both a `.claude/commands/` file and a `.claude/skills/` directory share the same name, the skill takes precedence.

**Source:** [Extend Claude with skills -- Claude Code Docs](https://code.claude.com/docs/en/skills)

### 2.2 BMAD's Coexistence Strategy

BMAD installs skills as **project-level skills** in `.claude/skills/`. This means:

- **No conflict with personal skills** at `~/.claude/skills/` -- personal skills take priority, so a user's personal `bmad-help` would override the project's
- **No conflict with plugin skills** -- plugins are namespaced (e.g., `/some-plugin:bmad-help` is distinct from `/bmad-help`)
- **Potential conflict with other project-level skills** -- if another framework also installs to `.claude/skills/` with the same name, last-write-wins at the filesystem level

BMAD mitigates project-level conflicts through its **`bmad-` prefix convention**. Every skill name starts with `bmad-`, making collisions with non-BMAD skills unlikely.

### 2.3 Third-Party BMAD Skills Packages

There are **three known approaches** to packaging BMAD for Claude Code, each with different coexistence implications:

| Package | Install Method | Skill Location | Namespace |
|---------|---------------|----------------|-----------|
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) (official) | `npx bmad-method install` | `.claude/skills/bmad-*/` | Flat, `bmad-` prefix |
| [aj-geddes/claude-code-bmad-skills](https://github.com/aj-geddes/claude-code-bmad-skills) (third-party) | Shell script installer | `~/.claude/skills/bmad/` | Under single `bmad/` directory |
| [PabloLION/bmad-plugin](https://github.com/PabloLION/bmad-plugin) (third-party) | Claude Code plugin format | Plugin `skills/` dir | `bmad:skill-name` |

The **official installer** creates flat directories (`bmad-code-review/`, `bmad-dev-story/`, etc.) at the project level. The **aj-geddes variant** installs to personal scope (`~/.claude/skills/bmad/`) and consolidates into a single directory. The **PabloLION plugin** uses native Claude Code plugin packaging with `.claude-plugin/plugin.json`, gaining automatic namespacing (`bmad:product-brief`).

**Sources:**
- [aj-geddes/claude-code-bmad-skills](https://github.com/aj-geddes/claude-code-bmad-skills)
- [PabloLION/bmad-plugin](https://github.com/PabloLION/bmad-plugin)

---

## 3. Plugin Format vs. Individual Skill Installation

### 3.1 BMAD Does NOT Use Plugin Format

The official BMAD installer (`npx bmad-method install`) installs skills **individually as project-level skills**, not as a plugin. There is no `.claude-plugin/plugin.json` created. This is a deliberate architectural choice documented in [BMAD-METHOD Issue #1629](https://github.com/bmad-code-org/BMAD-METHOD/issues/1629), which identifies key trade-offs:

**Why BMAD avoids the plugin format:**

1. **Agent persistence** -- BMAD agents operate in the main conversation context via prompt engineering ("menu loop"), maintaining character across interactions. Plugin agents run in isolated subprocess context and reset after returning summaries.

2. **Full tool access** -- BMAD agents in the main context can use all slash commands, MCP tools, Task tool, and built-in tools. Plugin agents have restricted tool availability.

3. **Workflow state tracking** -- BMAD's micro-file architecture enables resumable workflows with step-by-step progress, which is absent from native plugins.

4. **Deep namespace hierarchy** -- BMAD supports four-level nesting (`bmad:bmm:agents:pm`); native plugins support only two levels (`plugin:name`).

**What BMAD gives up:** no per-agent tool restrictions, no per-agent model selection, no context isolation (agent prompts consume main conversation memory).

**Source:** [Issue #1629: BMAD pattern vs native plugin](https://github.com/bmad-code-org/BMAD-METHOD/issues/1629)

### 3.2 The Plugin Alternative Exists (Third-Party)

PabloLION/bmad-plugin does package BMAD as a native Claude Code plugin, gaining automatic `bmad:` namespacing and plugin marketplace distribution. It includes 26 guided workflows as skills and models BMAD roles as agents with isolated context. However, it is a community fork, not the official approach.

---

## 4. Skill Name Conflict Resolution

### 4.1 Claude Code's Built-In Conflict Resolution

| Scenario | Resolution |
|----------|-----------|
| Same name at different levels (enterprise/personal/project) | Higher priority wins: enterprise > personal > project |
| Same name in a plugin vs. project | No conflict -- plugin skills are namespaced (`plugin:name`) |
| Same name in two different plugins | No conflict -- each plugin has its own namespace |
| Same name in `.claude/commands/` and `.claude/skills/` | Skill takes precedence |
| Same name at same level (e.g., two project skills) | Filesystem -- only one directory can exist with a given name |

### 4.2 BMAD-Specific Conflict Scenarios

- **Two BMAD installs at different levels:** If official BMAD is installed at project level (`.claude/skills/bmad-help/`) and aj-geddes variant at personal level (`~/.claude/skills/bmad/`), the personal level wins due to priority.

- **BMAD + bmad-plugin simultaneously:** The plugin version would be namespaced (`/bmad:help`) while the project version stays flat (`/bmad-help`). They coexist without conflict but create user confusion.

- **Custom non-BMAD skills:** The `bmad-` prefix makes collisions with other skill sources extremely unlikely unless another package also uses the `bmad-` prefix.

### 4.3 Known Bug: Plugin allowed-tools Namespacing

There is an [active bug (Issue #29360)](https://github.com/anthropics/claude-code/issues/29360) where `--plugin-dir` adds a `plugin_<name>_` prefix to MCP tool names at runtime but does NOT transform the `allowed-tools` declarations in skill frontmatter. This causes all MCP tool calls to prompt for manual approval, making skills with `allowed-tools` unusable when loaded via `--plugin-dir`. This affects the bmad-plugin approach but not the official BMAD installer (which doesn't use plugins).

**Source:** [Issue #29360: Plugin --plugin-dir namespacing breaks skill allowed-tools](https://github.com/anthropics/claude-code/issues/29360)

---

## 5. The bmad-skill-manifest.yaml Format

### 5.1 Purpose and Relationship to Agent Skills Standard

BMAD uses **two manifest layers** that serve different purposes:

1. **`SKILL.md`** (YAML frontmatter) -- the Agent Skills standard format. This is what Claude Code reads. It follows the [agentskills.io specification](https://agentskills.io/specification) with `name` and `description` as required fields.

2. **`bmad-skill-manifest.yaml`** -- a BMAD-internal metadata file that the BMAD installer reads to generate `SKILL.md` files and track skill relationships. It is NOT part of the Agent Skills standard.

### 5.2 bmad-skill-manifest.yaml Schema

Based on examination of files in this repository, the format varies by artifact type:

**For workflow/task skills (minimal form):**
```yaml
type: skill
```

**For agent skills (rich form):**
```yaml
type: agent
name: analyst
displayName: Mary
title: Business Analyst
icon: "chart-emoji"
capabilities: "market research, competitive analysis, requirements elicitation, domain expertise"
role: Strategic Business Analyst + Requirements Expert
identity: "Senior analyst with deep expertise..."
communicationStyle: "Speaks with the excitement of a treasure hunter..."
principles: "Channel expert business analysis frameworks..."
module: bmm
canonicalId: bmad-analyst
```

### 5.3 The bmad-manifest.json (New in V6.2/Conformant Skills)

As of PR #2021 (March 16, 2026), conformant agent skills also include a `bmad-manifest.json` that maps agent capabilities to BMAD skills:

```json
{
  "module-code": "bmm",
  "replaces-skill": "bmad-analyst",
  "persona": "Senior business analyst who treats every challenge like a treasure hunt...",
  "has-memory": false,
  "capabilities": [
    {
      "name": "brainstorm-project",
      "menu-code": "BP",
      "description": "Expert guided brainstorming facilitation...",
      "skill-name": "bmad-brainstorming"
    }
  ]
}
```

This bridges the gap between BMAD's agent persona system and the Agent Skills standard by keeping persona metadata and capability menus in a JSON sidecar while the `SKILL.md` handles Claude Code integration.

### 5.4 The skill-manifest.csv (Global Registry)

BMAD also maintains a global CSV at `_bmad/_config/skill-manifest.csv` that indexes all skills across modules:

```
canonicalId,name,description,module,path,install_to_bmad
"bmad-help","bmad-help","Analyzes what is done...","core","_bmad/core/skills/bmad-help/SKILL.md","true"
```

This CSV has 61 entries and serves as the installer's source of truth for what to deploy to `.claude/skills/`.

### 5.5 Relationship to Agent Skills Standard

The [Agent Skills specification](https://agentskills.io/specification) defines the `SKILL.md` format that Claude Code natively reads:

| Field | Required | Used by BMAD |
|-------|----------|-------------|
| `name` | Yes | Yes -- matches directory name, `bmad-` prefixed |
| `description` | Yes | Yes -- includes trigger phrases |
| `license` | No | Not observed |
| `compatibility` | No | Not observed |
| `metadata` | No | Not observed (BMAD uses separate sidecar files) |
| `allowed-tools` | No (experimental) | Not observed in installed stubs |

BMAD's installed `SKILL.md` files are **conformant with the Agent Skills standard** but deliberately minimal -- they use only `name` and `description` in frontmatter, delegating all other metadata to the BMAD-specific sidecar files (`bmad-skill-manifest.yaml`, `bmad-manifest.json`).

---

## 6. Key Findings and Implications

### 6.1 For Momentum's Practice Layer

- BMAD skills occupy the `bmad-` namespace by convention. Any Momentum-specific skills should use a different prefix (e.g., `momentum-` or `mtm-`) to avoid any collision.
- BMAD installs 68 skill directories to `.claude/skills/`. With Claude Code's skill description budget at 2% of context window (fallback 16,000 chars), this many skills may approach the budget. The `/context` command can check for excluded skills.
- BMAD's agent-as-skill architecture means agents run in the main conversation context, consuming conversation memory. This is intentional but means active BMAD agents affect available context for other work.

### 6.2 Coexistence Is Functional But Uncoordinated

- There is no registry, lock file, or coordination mechanism between BMAD and other skill sources at the project level.
- Claude Code's priority system (enterprise > personal > project) and plugin namespacing handle most conflicts automatically.
- The main risk is **skill description budget exhaustion** when many skills from multiple sources compete for context.

### 6.3 BMAD is Converging on the Agent Skills Standard

The V6.x releases show clear momentum toward full Agent Skills conformance: V6.1 made everything a skill, V6.2 added validation, and today's PR #2021 converted agents to conformant skill directories. The `bmad-skill-manifest.yaml` and `bmad-manifest.json` sidecars represent BMAD-specific extensions that do not conflict with the standard.

---

## Sources

- [BMAD-METHOD GitHub Repository](https://github.com/bmad-code-org/BMAD-METHOD)
- [BMAD-METHOD CHANGELOG.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/CHANGELOG.md)
- [BMAD-METHOD Releases](https://github.com/bmad-code-org/BMAD-METHOD/releases)
- [BMAD Method Documentation](https://docs.bmad-method.org/)
- [How to Install BMad](https://docs.bmad-method.org/how-to/install-bmad/)
- [BMAD Skills Reference](https://docs.bmad-method.org/reference/commands/)
- [PR #2021: Feat/conformant agent skills](https://github.com/bmad-code-org/BMAD-METHOD/pull/2021)
- [Issue #1629: BMAD pattern vs native plugin](https://github.com/bmad-code-org/BMAD-METHOD/issues/1629)
- [Extend Claude with skills -- Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Create plugins -- Claude Code Docs](https://code.claude.com/docs/en/plugins)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills GitHub (Anthropic)](https://github.com/anthropics/skills)
- [aj-geddes/claude-code-bmad-skills (third-party)](https://github.com/aj-geddes/claude-code-bmad-skills)
- [PabloLION/bmad-plugin (third-party)](https://github.com/PabloLION/bmad-plugin)
- [Issue #29360: Plugin namespacing breaks allowed-tools](https://github.com/anthropics/claude-code/issues/29360)
- [bmad-labs/skills](https://github.com/bmad-labs/skills)
- [BMAD npm package](https://www.npmjs.com/package/bmad-method)
