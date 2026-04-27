---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "BMAD-method's multi-agent deployment internals (April 2026) — repo structure, installer flow, format adapters, what's shared vs. per-agent."
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
---

# BMAD-Method v6 Multi-Agent Deployment Internals

## Overview

BMAD-METHOD v6 (`6.0.0-beta.0` on the `v6-alpha` branch as of late 2025; v6 stays the active line into 2026) is a Node.js (≥20) CLI distributed via npm as `bmad-method`. It implements multi-agent deployment by treating the installed `bmad/` directory as a **canonical source of truth** containing module-organized agents/tasks/tools/workflows, and treating each supported coding tool (Claude Code, Codex CLI, Cursor, Gemini CLI, OpenCode, Windsurf, Cline, Roo, KiloCode, Trae, Crush, iFlow, Qwen, Auggie, GitHub Copilot) as a **format adapter** that materializes that tree into the tool's native command/rule/agent shape under a tool-specific dot-directory in the user's project. [OFFICIAL — `package.json`, `tools/cli/installers/lib/ide/`]

The architectural shape: one source → N adapter writers → N on-disk projections. Adapters share a base class (`BaseIdeSetup`), share artifact-discovery helpers (`shared/bmad-artifacts.js`, `getAgentsFromBmad`, `getTasksFromBmad`), share a workflow-command-template (`workflow-command-template.md`), but each adapter owns its own filename layout, frontmatter dialect, slash-command convention, and any tool-specific runtime hooks. This pattern — *write once, project many* — is the dominant insight worth pulling forward into Momentum, with caveats noted in §Limitations. [OFFICIAL — `tools/cli/installers/lib/ide/_base-ide.js`, `claude-code.js`, `codex.js`]

## Repo Structure

Top-level layout of `bmad-code-org/BMAD-METHOD@v6-alpha` (commit `24a2271`, 2025-10-27): [OFFICIAL — local clone, `git log -1` and `ls`]

```
BMAD-METHOD/
├── bmad/                    # Self-installed copy (the repo eats its own dog food)
├── bmd/                     # BMad Designer (separate concern; not the installer)
├── docs/                    # Alpha release notes, v4-to-v6 upgrade guide
├── package.json             # bin: { bmad, bmad-method } -> tools/bmad-npx-wrapper.js
├── src/
│   ├── core/                # Lean core: agents, tasks, tools, workflows, _module-installer
│   │   ├── agents/          #   bmad-master.agent.yaml, bmad-web-orchestrator.agent.xml
│   │   ├── tasks/           #   workflow.xml etc. — the "OS" for workflow execution
│   │   ├── tools/
│   │   └── workflows/
│   ├── modules/             # Pluggable modules; each is a domain pack
│   │   ├── bmm/             #   BMad Method (agile AI dev — the flagship)
│   │   │   ├── agents/      #     pm.agent.yaml, sm.agent.yaml, dev.agent.yaml, …
│   │   │   ├── workflows/   #     1-analysis, 2-plan, 3-solutioning, 4-implementation
│   │   │   └── sub-modules/ #     IDE-specific extensions (e.g., claude-code/)
│   │   ├── bmb/             #   BMad Builder — module/workflow authoring
│   │   └── cis/             #   Creative Intelligence Suite
│   └── utility/
│       ├── models/          # Shared template fragments (agent-activation-ide.xml,
│       │                    #   agent-config-template.md, agent.customize.template.yaml)
│       └── templates/
├── tools/
│   ├── bmad-npx-wrapper.js  # npx entry shim
│   ├── cli/
│   │   ├── bmad-cli.js      # commander.js entry point
│   │   ├── commands/        # install, build, list, status, uninstall, update
│   │   ├── installers/lib/
│   │   │   ├── core/        # installer.js, detector.js, manifest-generator.js,
│   │   │   │                #   dependency-resolver.js, config-collector.js
│   │   │   ├── ide/         # 16 adapter files — one per supported tool
│   │   │   └── modules/     # manager.js: per-module installer hooks
│   │   ├── lib/             # xml-handler, yaml-xml-builder, file-ops, ui, …
│   │   └── bundlers/        # bundle-web.js (web bundle for Codex Web etc.)
│   └── platform-codes.yaml  # Catalogue of supported platforms / aliases
└── test/
```

[OFFICIAL — direct directory listing of `/Users/steve/projects/BMAD-METHOD`]

Two key facts from the repo map:

1. **There are no SKILL.md files.** BMAD's atomic units are `<name>.agent.yaml` source files plus `workflow.yaml` directories, not Anthropic-style Skills. Compilation goes YAML → an XML-flavored Markdown agent file, then per-adapter projection. [OFFICIAL — `src/modules/bmm/agents/sm.agent.yaml`]
2. **A module declares its own IDE-specific overlays via `sub-modules/<ide>/`.** For example `src/modules/bmm/sub-modules/claude-code/` contains `injections.yaml`, a `sub-agents/` directory, and `config.yaml` — these are Claude Code–only enhancements that the Claude Code adapter reads during install. Other adapters ignore them. [OFFICIAL — `src/modules/bmm/sub-modules/claude-code/injections.yaml`]

## Installer Walkthrough

Entry point is `npx bmad-method install` (or `npx bmad install`). The npx wrapper hands off to `tools/cli/bmad-cli.js`, which uses `commander` to register every file in `tools/cli/commands/` as a subcommand. The `install` action calls `Installer.install(config)` after `UI.promptInstall()` collects the choice tree. [OFFICIAL — `package.json` `bin` block; `tools/cli/bmad-cli.js`; `tools/cli/commands/install.js`]

Step-by-step (from `installer.js` lines ~153–692, edited for clarity): [OFFICIAL — `tools/cli/installers/lib/core/installer.js`]

1. **Display logo + header.** `CLIUtils.displayLogo()` prints the BMAD ASCII banner.
2. **Legacy v4 detection.** `Detector.detectLegacyV4()` scans for old footprints (`.bmad-core/`, etc.) and runs a migration prompt before any writes.
3. **Module configuration prompts.** `ConfigCollector.collectAllConfigurations(modules, projectDir)` walks each module's `_module-installer/` config schema and asks the user any required questions (output folder, language, user name, technical level).
4. **Existing-installation handling.** `Detector.detect(bmadDir)` reads `bmad/_cfg/manifest.yaml` if present. If a prior install exists the user picks reinstall (destructive — confirm prompt) vs. update (preserves custom files). For updates, `readFilesManifest()` parses `bmad/_cfg/files-manifest.csv` and hashes every current file to classify as: untouched, modified-by-user (will be backed up to `.bak`), or wholly custom (preserved through the temp-backup/restore cycle).
5. **Tool selection prompt.** `collectToolConfigurations()` calls `UI.promptToolSelection()`. This asks a single multi-select inquirer checkbox: "Select tools to configure" — the choices are dynamically built from `IdeManager.getAvailableIdes()`, which scans `tools/cli/installers/lib/ide/*.js`, instantiates each handler, and reads its `name`, `displayName`, `preferred` properties. Preferred tools (Claude Code, Codex, Cursor, Gemini CLI, OpenCode, Windsurf, GitHub Copilot) appear under "── Recommended Tools ⭐ ──", everything else under "── Additional Tools ──", and previously configured tools (auto-checked) under "── Previously Configured ✅ ──". The result is a string array like `["claude-code", "codex", "cursor"]`. [OFFICIAL — `tools/cli/lib/ui.js` lines 89–179, `tools/cli/installers/lib/ide/manager.js` lines 18–97]
6. **Per-IDE config sub-prompts.** For IDEs whose handler exposes a `collectConfiguration()` method (`claude-code`, `github-copilot`, `roo`, `cline`, `auggie`, `codex`, `qwen`, `gemini`), the installer dynamically `require()`s the adapter and runs that method *before* any writes — e.g., Claude Code asks whether to install BMM subagents (all/selective/none) and where (`.claude/agents/` vs. `~/.claude/agents/`); Codex asks CLI vs. Web mode; Cline asks for rule-ordering strategy. Answers are cached in `ideConfigurations[ide]`. [OFFICIAL — `installer.js` lines 84–127; `claude-code.js` `collectConfiguration()`; `codex.js` `collectConfiguration()`]
7. **Dependency resolution.** `DependencyResolver.resolve(projectRoot, modules)` reads each module's manifest, walks references, and produces `resolution.byModule[moduleName] = { agents, tasks, tools, templates, data, other }`. Partial modules (only deps) get a slimmer install pass.
8. **Materialize `bmad/` source-of-truth tree.** `installCoreWithDependencies()` and `installModuleWithDependencies()` copy the dependency-filtered files into `<projectDir>/bmad/<module>/{agents,tasks,tools,workflows,templates,data}/`. During copy, `processAgentFiles(modulePath, moduleName)` does the **YAML → XML-Markdown agent compile** (see §Skill→Agent Compilation).
9. **Generate module configs.** `generateModuleConfigs(bmadDir, moduleConfigs)` writes one `bmad/<module>/config.yaml` per installed module, populated with the prompts from step 3.
10. **Generate manifests.** `ManifestGenerator.generateManifests()` produces four CSVs in `bmad/_cfg/`: `workflow-manifest.csv`, `agent-manifest.csv`, `task-manifest.csv`, `files-manifest.csv` (the latter with SHA hashes for update-time drift detection). [OFFICIAL — `manifest-generator.js`; CSV consumed by `WorkflowCommandGenerator` and `TaskToolCommandGenerator`]
11. **Per-IDE projection (the critical step for multi-agent deployment).** For each entry in `validIdes`, `IdeManager.setup(ideName, projectDir, bmadDir, options)` looks up the registered handler and calls `handler.setup(projectDir, bmadDir, { selectedModules, preCollectedConfig })`. Each adapter reads `bmad/` and writes its native projection. [OFFICIAL — `installer.js` lines 493–560; `ide/manager.js` lines 122–138]
12. **Save IDE config for future updates.** `IdeConfigManager.saveIdeConfig(bmadDir, ide, config)` persists the per-IDE answers under `bmad/_cfg/ide-configs/<ide>.yaml` so the next `update` re-uses them silently.
13. **Run module-specific post-install hooks.** `ModuleManager.runModuleInstaller('core', bmadDir, { installedIDEs })` and the same per user-selected module — these can do final wiring (e.g., copy IDE-specific docs).
14. **Custom-file restore.** Any files backed up in step 4 are written back; modified files land beside the new versions as `.bak`.
15. **Print summary.** The "Installation Complete!" output enumerates installed modules, configured tools, and the install path.

The installer is roughly 2,063 lines in one file. There is no parallelism — adapters run sequentially in a `for…of` loop. [OFFICIAL — `installer.js` `wc -l` = 2063]

## Skill→Agent Compilation

BMAD's compilation pipeline has two stages. **Stage 1** (source → installed `bmad/`) is run once during install. **Stage 2** (installed `bmad/` → per-IDE projection) is run once per selected IDE. Tracing the BMM Scrum Master agent (`sm`) through both stages:

### Stage 1: YAML source → XML-Markdown agent file

Source: `src/modules/bmm/agents/sm.agent.yaml`. Excerpt: [OFFICIAL — read directly]

```yaml
agent:
  metadata:
    id: bmad/bmm/agents/sm.md
    name: Bob
    title: Scrum Master
    icon: 🏃
    module: bmm
  persona:
    role: Technical Scrum Master + Story Preparation Specialist
    identity: …
    communication_style: …
    principles: [ … ]
  critical_actions:
    - "When running *create-story, run non-interactively: …"
  menu:
    - trigger: create-story
      workflow: "{project-root}/bmad/bmm/workflows/4-implementation/create-story/workflow.yaml"
      description: Create a Draft Story with Context
    - trigger: sprint-planning
      workflow: "{project-root}/bmad/bmm/workflows/4-implementation/sprint-planning/workflow.yaml"
      description: …
```

`Installer.processAgentFiles(modulePath, moduleName)` (lines 1121–1188) iterates `bmad/<module>/agents/*.agent.yaml` and for each file: [OFFICIAL — `installer.js` lines 1121–1188]

1. Computes a customize-template path `bmad/_cfg/agents/<module>-<name>.customize.yaml` and copies the generic template `src/utility/templates/agent.customize.template.yaml` there if missing (this is the **update-safe customization layer** — users edit the customize file; it survives reinstalls).
2. Calls `XmlHandler.buildFromYaml(yamlPath, customizePath, { includeMetadata: true })`, which delegates to `YamlXmlBuilder.loadAndMergeAgent(yamlPath, customizePath)` and `convertToXml(merged, buildMetadata)`. The output is an XML-flavored Markdown file (`<agent name="Bob" title="Scrum Master" …><activation …/><persona>…</persona><cmds>…</cmds></agent>`) with file hashes embedded as comments for drift detection. The `{project-root}` placeholder is **left unresolved** — "LLMs understand this placeholder at runtime" per the inline comment.
3. Writes the result to `bmad/<module>/agents/<name>.md`, registers the file in `installedFiles[]` (used to build `files-manifest.csv`), then deletes the source `.agent.yaml` from the installed tree (it remains in the npm package's `src/`).
4. Activation injection: `XmlHandler.injectActivationSimple()` reads `src/utility/models/agent-activation-ide.xml` — a shared activation template — indents it 2 spaces, substitutes `{agent-filename}`, and inserts it as the first child of `<agent>`. Every agent gets the same activation block.

**What's shared vs. per-agent at this stage:**
- Shared (single source): the activation template, the customize template, the XML schema, the YAML→XML conversion logic.
- Per-agent: persona, role, critical_actions, menu — these come straight from the YAML.
- Per-user (customize layer): can override metadata, persona fields, critical_actions, and menu without editing source. The merge is field-level.

### Stage 2: installed `bmad/` agent.md → per-IDE projection

For Claude Code, `ClaudeCodeSetup.setup(projectDir, bmadDir, options)` (lines 90–172): [OFFICIAL — `tools/cli/installers/lib/ide/claude-code.js`]

1. Creates `<projectDir>/.claude/commands/bmad/`.
2. Calls `getAgentsFromBmad(bmadDir, options.selectedModules)` (shared helper) which walks `bmad/core/agents/`, `bmad/<module>/agents/` for each selected module, and `bmad/agents/` (standalone) for `*.md` files.
3. For each agent: ensures `<.claude/commands/bmad/<module>/agents/>` exists, calls `readAndProcess(agent.path, { module, name })` which runs the file through `BaseIdeSetup.processContent()`. Claude Code overrides `processContent` to *skip* the `{project-root}` substitution (preserves the placeholder). It writes the file as-is to `.claude/commands/bmad/<module>/agents/<name>.md`.
4. **Workflow command generation.** `WorkflowCommandGenerator.generateWorkflowCommands(projectDir, bmadDir)` reads `bmad/_cfg/workflow-manifest.csv`, filters to `standalone === 'true'`, and for each row renders the shared template `tools/cli/installers/lib/ide/workflow-command-template.md`: [OFFICIAL — `workflow-command-generator.js` lines 19–52, template file]

   ```
   ---
   description: '{{description}}'
   ---
   # {{name}}
   IT IS CRITICAL THAT YOU FOLLOW THESE STEPS — while staying in character …
   <steps CRITICAL="TRUE">
   1. Always LOAD the FULL {project-root}/bmad/core/tasks/workflow.xml
   2. READ its entire contents — this is the CORE OS for EXECUTING the specific workflow-config {{workflow_path}}
   3. Pass the yaml path {{workflow_path}} as 'workflow-config' parameter to the workflow.xml instructions
   4. Follow workflow.xml instructions EXACTLY as written
   5. Save outputs after EACH section …
   </steps>
   ```

   Each rendered file lands in `.claude/commands/bmad/<module>/workflows/<name>.md`. Claude Code's command discovery picks them up as `/bmad:<module>:workflows:<name>`. So **one workflow.yaml in `src/modules/<m>/workflows/<w>/` becomes one slash command in Claude Code** — a clean 1:1 mapping mediated entirely by the manifest.
5. **Module injections.** `processModuleInjections(projectDir, bmadDir, options)` reads each module's `src/modules/<m>/sub-modules/claude-code/injections.yaml` and applies content patches at `<!-- IDE-INJECT-POINT: <name> -->` markers in workflow instruction files (e.g., adding "Use `bmm-requirements-analyst` subagent" hints to `bmad/bmm/workflows/prd/instructions.md`). This is how BMAD layers Claude Code–specific guidance onto otherwise tool-neutral workflow instructions.
6. **Subagent copy.** Files under `src/modules/<m>/sub-modules/claude-code/sub-agents/<group>/<agent>.md` (already in Anthropic subagent frontmatter format — `name:`, `description:`, `tools:`) are copied to `.claude/agents/` (project) or `~/.claude/agents/` (user) per the prompt answer.

The **same source agent.md** (Stage 1 output) is the input for every other adapter. What differs is purely the projection.

## Per-Agent Adapters

All 16 adapters extend `BaseIdeSetup` (572 lines, the shared scanning/processing kernel). The base class provides `getAgents()`, `getTasks()`, `getTools()`, `getWorkflows()` (all with `standalone` filtering), `processContent()` (placeholder substitution + activation injection), and file I/O helpers. Subclasses override `setup()` and usually `processContent()`. [OFFICIAL — `_base-ide.js`, line counts: 16 adapters totalling 4,528 lines]

| Adapter (`name`) | Output dir | Filename pattern | Frontmatter dialect | Notes |
|---|---|---|---|---|
| `claude-code` | `.claude/commands/bmad/<module>/agents/` and `…/workflows/` | `<name>.md` | Claude Code slash-command MD with optional YAML frontmatter | Subagents copied to `.claude/agents/` per prompt; injections.yaml patches workflow instructions [OFFICIAL — `claude-code.js`] |
| `codex` | `~/.codex/prompts/` (HOME, not project) | `bmad-<module>-<kind>-<name>.md` (flattened) | Plain MD prompt with `{project-root}` resolved to actual `projectDir` | Slash commands like `/bmad-bmm-agents-pm`. CLI vs. Web mode is a UI prompt only — the file output is identical [OFFICIAL — `codex.js` lines 46–96, 176–195] |
| `gemini` | `.gemini/commands/agents/` and `.gemini/commands/tasks/` | `<name>.toml` | TOML (`description = "…"`, `prompt = """…@<relpath>…"""`) | TOML `prompt` uses `@<relpath>` Gemini-CLI file-reference syntax to lazy-load the agent body. Activation: `/bmad:agents:<name>` [OFFICIAL — `gemini.js`] |
| `opencode` | `.opencode/command/` (flat) | `bmad-agent-<module>-<name>.md`, `bmad-workflow-<module>-<name>.md`, `bmad-task-<module>-<name>.md` | YAML frontmatter, `mode: primary` injected for agents | OpenCode doesn't allow nested command dirs, so namespace is encoded in the filename [OFFICIAL — `opencode.js` lines 23–85, 125–139] |
| `cursor` | `.cursor/rules/bmad/<module>/{agents,tasks,tools,workflows}/` | `<name>.mdc` | MDC frontmatter (`description:`, `globs:`, `alwaysApply: false`) auto-prepended; type detected from XML content (`<agent`, `<task`, `<tool`, `workflow:`) | Manual rules — user references with `@bmad/<module>/agents/<name>`. An `index.mdc` master index is written. Does NOT modify `.cursorrules` [OFFICIAL — `cursor.js` lines 21–122, 238–289] |
| `windsurf` | `.windsurf/workflows/<module>/{agents,tasks,tools,workflows}/` | `<name>.md` | Windsurf frontmatter (`description:`, `auto_execution_mode: 1\|2\|3`) | Mode 3 for agents, 2 for tasks/tools, 1 for workflows. Triggered via Windsurf's workflow menu [OFFICIAL — `windsurf.js`] |
| `cline` | `.clinerules/` (flat) | `<NN>-<module>-<name>.md` (numeric prefix for ordering) | Plain MD | User chooses ordering strategy: by-module / by-importance / alphabetical / custom [OFFICIAL — `cline.js` lines 27–80] |
| `roo` | `.roomodes` (single JSON file) | one entry per agent | Roo custom-modes JSON (slug, name, fileRegex permissions) | Adapter rewrites the JSON file rather than scattering files. Asks for permission profile [OFFICIAL — `roo.js`] |
| `kilo` | `.kilocodemodes` (single file) | similar to Roo | KiloCode custom-modes format | KiloCode is a Roo fork; adapter is structurally similar [OFFICIAL — `kilo.js`] |
| `github-copilot` | `.github/chatmodes/` + `.vscode/settings.json` | `<name>.chatmode.md` | Copilot chat-mode MD; also patches VS Code settings | Most invasive — modifies repo-tracked `.github/` and `.vscode/` [OFFICIAL — `github-copilot.js`] |
| `auggie` | configurable: `.augment/commands/`, `~/.augment/commands/`, or custom | `<name>.md` | Plain MD | Three-way location prompt; can install to multiple locations in one run [OFFICIAL — `auggie.js`] |
| `iflow` | `.iflow/commands/bmad/` | `<name>.md` | iFlow CLI MD | Mirror of Claude Code shape with different dot-dir [OFFICIAL — `iflow.js`] |
| `qwen` | `.qwen/commands/BMad/` | `<name>.toml` | TOML (Gemini-style) | Qwen Code uses Gemini-CLI fork, so format mirrors Gemini [OFFICIAL — `qwen.js`] |
| `crush` | `.crush/commands/bmad/` | `<name>.md` | Plain MD | Generic Claude-Code-shaped projection [OFFICIAL — `crush.js`] |
| `trae` | `.trae/rules/` | `<name>.md` | Trae rules MD | Cursor-shaped projection [OFFICIAL — `trae.js`] |

### Detailed adapter notes

**Claude Code** is the reference adapter and gets the most special-casing — preserved `{project-root}` placeholder (lazy resolution), subagent system (the only adapter with a separate `/agents/` directory and selective install prompt), injection.yaml for workflow content patching. [OFFICIAL — `claude-code.js`]

**Codex CLI** writes to the user's HOME directory (`~/.codex/prompts/`) rather than the project, with a verbose console banner explaining "No `.codex` file was created in the project root." Filenames are flattened with module/kind separators: `bmad-<flattened-relpath>`. The CHANGELOG note for unreleased v6 says "Codex installer uses custom prompts in `.codex/prompts/`, instead of `AGENTS.md`" — so the v4/early-v6 approach was to write `AGENTS.md` (the de-facto Codex convention), and that has been deprecated in favor of slash-command prompts. [OFFICIAL — `codex.js` line 177; `CHANGELOG.md` Unreleased section]

**Gemini CLI** uniquely uses TOML and the `@<filepath>` reference convention. The TOML's `prompt` field doesn't *contain* the agent body — it `@`-references the file in the installed `bmad/` tree, so updates to the source flow through without re-running the installer. This is materially different from every other adapter, which copies content. [OFFICIAL — `gemini.js` lines 80–125]

**OpenCode** flattens everything because the tool doesn't support nested command directories. The namespace gets encoded in the filename prefix — `bmad-agent-…`, `bmad-workflow-…`, `bmad-task-…`, `bmad-tool-…`. Only standalone tasks/tools are exported (workflow-manifest filtering). The adapter parses existing frontmatter and injects `mode: primary` for agents. [OFFICIAL — `opencode.js` lines 91–118, 141–170]

**Cursor** is the most "rule-shaped" target — it writes MDC files into `.cursor/rules/bmad/`, auto-detects file type from XML content sniffing (`<agent`, `<task`, `<tool`), and generates a sibling `index.mdc` with a navigation map. Rules are `alwaysApply: false` (manual reference) by design. [OFFICIAL — `cursor.js` lines 127–221, 238–289]

**Windsurf** treats every BMAD artifact as a Windsurf "workflow" file with three execution-mode tiers. The adapter is unusual in that it doesn't process content (no XML activation injection, no `{project-root}` substitution) — it just prepends frontmatter. [OFFICIAL — `windsurf.js` lines 50–95]

**Roo and Kilo** are the only adapters that produce a *single config file* rather than a tree — `.roomodes` JSON / `.kilocodemodes` for the entire bmad install. This puts a hard structural ceiling on extensibility (one file rewrite per change) but is the price of those tools' design. [OFFICIAL — `roo.js`, `kilo.js`]

### Shared infrastructure across adapters

- `tools/cli/installers/lib/ide/_base-ide.js` — base class with shared scanning, content processing, file ops.
- `tools/cli/installers/lib/ide/shared/bmad-artifacts.js` — `getAgentsFromBmad`, `getTasksFromBmad` reused by Claude Code, Codex, OpenCode, Qwen.
- `tools/cli/installers/lib/ide/workflow-command-template.md` — single source-of-truth template for the "load workflow.xml and execute it" prompt; rendered by `WorkflowCommandGenerator` and reused by adapters that emit slash commands.
- `tools/cli/installers/lib/ide/workflow-command-generator.js` and `task-tool-command-generator.js` — manifest readers that emit per-tool command files.
- `tools/cli/installers/lib/ide/shared/module-injections.js` — `loadModuleInjectionConfig`, `shouldApplyInjection`, `filterAgentInstructions`, `resolveSubagentFiles` (used by Claude Code; the pattern is generalizable but currently Claude-Code-only).

What is **duplicated** across adapters: each adapter independently writes its console output, calls `getAgents`/`getTasks`, ensures dirs, loops and writes. There's no template-method pattern enforcing structure — each adapter is ~150–450 lines of mostly copy-pasted scaffolding around its unique projection logic. This is the main code-smell: a refactor opportunity that BMAD has not yet taken. [OBSERVATION based on side-by-side reading]

## Limitations & Gaps

1. **No SKILL.md primitive.** BMAD's source unit is a YAML agent definition + a directory containing `workflow.yaml` + `instructions.md` + `template.md` + `checklist.md`. There is no Anthropic-shaped SKILL.md anywhere. Momentum currently *is* SKILL.md-shaped; adopting BMAD's pattern wholesale would mean inventing a SKILL.md ↔ agent.yaml/workflow.yaml mapping, which is non-trivial. [OFFICIAL — `find … SKILL.md` returned zero results in the repo]
2. **Adapter duplication.** 16 adapters × ~150–450 lines each = ~5k lines of mostly parallel logic. There's no enforced template method, no schema-driven generation. Each new tool means hand-writing another 200-line adapter. [OBSERVATION — adapter line counts]
3. **Sequential-only.** All adapter writes run in a single `for…of` loop. With 5+ tools selected, the install can take meaningful wall time. No `Promise.all`. [OFFICIAL — `installer.js` line 513]
4. **Codex AGENTS.md deprecation just landed.** The CHANGELOG "Unreleased" note shows BMAD just *moved off* writing `AGENTS.md` to writing `.codex/prompts/` slash commands instead. This signals that even BMAD is still finding the right Codex shape. AGENTS.md has not stabilized as a cross-tool convention. [OFFICIAL — `CHANGELOG.md` Unreleased]
5. **The shared activation block is one-size-fits-all.** `src/utility/models/agent-activation-ide.xml` is the same for every IDE. There's no per-tool activation override; the adapter's only choice is "inject the universal block or don't." [OFFICIAL — `_base-ide.js` `processContent()`, `xml-handler.js` `injectActivationSimple()`]
6. **Update-time customization preservation is non-trivial machinery.** The hash-based files-manifest.csv plus temp-backup/restore plus `.bak` fallback plus the YAML customize layer is ~300 lines of edge-case handling. Worth it for end users, but a real implementation cost. [OFFICIAL — `installer.js` lines 270–365, 600–675]
7. **No automatic tool detection.** The user explicitly checks the boxes; BMAD does not autodetect e.g. "this project has `.cursor/`, install Cursor adapter." The `detect()` method per adapter exists but is only used to mark the "Previously Configured" UI section. [OFFICIAL — `ui.js` line 95]
8. **Hooks are not first-class.** None of the adapters install Claude Code hooks (PostToolUse, PreToolUse, SessionStart, etc.). The whole hook surface is invisible to BMAD. For Momentum, which leans heavily on hooks (commit checkpoint, plan-audit gate, etc.), BMAD's adapter pattern is undersized.
9. **The "everything is a slash command" assumption.** BMAD treats agents as slash commands, workflows as slash commands, tasks as slash commands. For tools where the natural shape is "rule that always applies" (Cursor `alwaysApply: true`, `.cursorrules`) BMAD explicitly opts out — "BMAD does not modify your `.cursorrules` file. You manage that separately." This sidesteps the question of *ambient context* entirely. [OFFICIAL — `cursor.js` line 144 in the index template]

## Where this generalizes — and where it doesn't — for Momentum

**Generalizes:** the source-of-truth-plus-projections pattern; per-adapter `setup(projectDir, bmadDir, options)` contract; manifest-driven slash-command generation with a single shared template; YAML customize layer for update-safe overrides. These are reusable architectural ideas independent of BMAD's specific source format.

**Doesn't generalize cleanly:** Momentum's atom is the SKILL.md (with frontmatter that drives discovery and triggering), not the agent.yaml. The Anthropic skill model conflates persona and workflow into one file; BMAD splits them. Mapping BMAD's projections onto a SKILL.md source would require either (a) treating each Momentum skill as both an "agent" and a "workflow" (probably emitting the skill body as a slash command and the description as a Cursor rule), or (b) enriching SKILL.md frontmatter with a `targets:` block that drives per-adapter behavior. The latter is closer to how Anthropic's first-party skills marketplace appears to be heading.

## Sources

All sources are direct reads of the local clone of `bmad-code-org/BMAD-METHOD` at commit `24a22715` (branch `v6-alpha`, 2025-10-27). The repo is the v6 line that flowed into the alpha→beta on npm as `bmad-method@6.0.0-beta.0`. No source older than 2 years; the most recent code reviewed is from October 2025, ~6 months before the cite-date 2026-04-26. [OFFICIAL]

Specific paths cited:

- `/Users/steve/projects/BMAD-METHOD/package.json` — entry points, version, scripts.
- `/Users/steve/projects/BMAD-METHOD/CHANGELOG.md` — release timeline, Codex deprecation note.
- `/Users/steve/projects/BMAD-METHOD/README.md` — architectural framing.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/bmad-cli.js` — commander entry.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/commands/install.js` — install action.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/core/installer.js` — main `Installer` class (2,063 lines).
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/manager.js` — dynamic adapter discovery.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/_base-ide.js` — adapter base class.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/claude-code.js` — Claude Code adapter.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/codex.js` — Codex CLI adapter.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/gemini.js` — Gemini CLI adapter.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/opencode.js` — OpenCode adapter.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/cursor.js` — Cursor adapter.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/windsurf.js` — Windsurf adapter.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/cline.js` — Cline adapter.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/{auggie,crush,iflow,kilo,qwen,trae,roo,github-copilot}.js` — additional adapters.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/workflow-command-generator.js` — manifest-driven slash-command emitter.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/workflow-command-template.md` — shared command template.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/installers/lib/ide/shared/bmad-artifacts.js` — agent/task discovery.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/lib/ui.js` — install/tool prompts.
- `/Users/steve/projects/BMAD-METHOD/tools/cli/lib/xml-handler.js` — YAML→XML agent compile.
- `/Users/steve/projects/BMAD-METHOD/src/modules/bmm/agents/sm.agent.yaml` — example source agent.
- `/Users/steve/projects/BMAD-METHOD/src/modules/bmm/sub-modules/claude-code/injections.yaml` — Claude Code injection points.
- `/Users/steve/projects/BMAD-METHOD/src/modules/bmm/sub-modules/claude-code/sub-agents/bmad-research/market-researcher.md` — example Claude Code subagent.
- `/Users/steve/projects/BMAD-METHOD/src/modules/bmm/workflows/4-implementation/create-story/workflow.yaml` — example workflow source.
