---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Slash commands, prompts, rules — format translation patterns — actual code patterns and drift prevention from real cross-agent installers."
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
---

# Format Translation Patterns: How Cross-Agent Installers Compile One Source to Many Targets

This report analyzes seven real implementations of "compile one logical artifact to N agent formats." For each project I cite source-of-truth format, build/translation approach, an actual code excerpt, output verification strategy, and drift-prevention mechanism. Tags: **[OFFICIAL]** = repo source; **[PRAC]** = community blog/forum; **[UNVERIFIED]** = inference.

## Inline Summary

Three patterns dominate as of 2026-04-26: (1) **manifest-driven config + per-agent adapter classes** (BMAD-METHOD, claude-task-master), where a YAML/JSON registry maps platform codes to target paths and lifecycle hooks; (2) **frontmatter-aware AST/regex transforms** (continuedev/rules, claude-task-master rule-transformer), where a single source markdown is parsed and reserialized per target; and (3) **convention-only with symlinks** (AGENTS.md spec, Nottlespike script), which skips translation entirely and relies on the AGENTS.md universal file. The most borrowable pattern for Momentum is the BMAD `platform-codes.yaml` registry combined with a `ConfigDrivenIdeSetup` adapter — it scales linearly with new agents added (just append a YAML entry) and uses verbatim copy where formats agree (the `.agents/skills/` standard), reserving custom adapter logic only for outliers (GitHub Copilot's `.github/instructions/*.instructions.md` shape, Roo's tool-name remapping). Drift is prevented at three layers: (a) per-profile integration tests that exercise the converter with goldens, (b) a `RULE_PROFILES` constants array as single source of truth referenced by both code and tests, and (c) CI that runs both formatter check and unit suite on every PR.

## BMAD-METHOD v6 — Manifest-Driven Verbatim Skill Distribution

### Source-of-truth format

Single canonical input: a `_bmad/_config/skill-manifest.csv` listing every BMAD skill with a `canonicalId` and a relative `path` to its `SKILL.md`. The skill bodies themselves are markdown-with-frontmatter living under `_bmad/<module>/...`. Platform targets are defined in a separate YAML registry — `tools/installer/ide/platform-codes.yaml` — that maps each supported agent to its install directory **[OFFICIAL]**.

### Translation/build approach

**Manifest-driven, no transformation.** A single class `ConfigDrivenIdeSetup` reads the YAML, then for each platform copies the skill source directory verbatim into the platform's target directory. This is the pure "manifest-driven" pattern with a fallback to "per-agent adapter" only for tools that need post-processing (GitHub Copilot, Kilo, Rovo Dev). 30+ agents are supported as of v6.3.0 by populating the registry alone — no code change required for a new IDE that uses the standard `.agents/skills/` directory **[OFFICIAL]**.

### Code excerpt

The registry — `tools/installer/ide/platform-codes.yaml` — is purely declarative. Many tools share the cross-tool standard `.agents/skills/` so the `target_dir` is identical for amp, cursor, codex, github-copilot, gemini, opencode, windsurf, and others **[OFFICIAL]**:

```yaml
# tools/installer/ide/platform-codes.yaml
platforms:
  claude-code:
    name: "Claude Code"
    preferred: true
    installer:
      target_dir: .claude/skills
      global_target_dir: ~/.claude/skills
  cursor:
    name: "Cursor"
    preferred: true
    installer:
      target_dir: .agents/skills
      global_target_dir: ~/.agents/skills
  github-copilot:
    name: "GitHub Copilot"
    preferred: true
    installer:
      target_dir: .agents/skills
      global_target_dir: ~/.agents/skills
```

The adapter — `tools/installer/ide/_config-driven.js` (JavaScript / Node) — is a single class that handles every config-driven platform. Loading is dynamic via `manager.js` **[OFFICIAL]**:

```javascript
// tools/installer/ide/manager.js (lines 53–68)
async loadConfigDrivenHandlers() {
  const { loadPlatformCodes } = require('./platform-codes');
  const platformConfig = await loadPlatformCodes();
  const { ConfigDrivenIdeSetup } = require('./_config-driven');

  for (const [platformCode, platformInfo] of Object.entries(platformConfig.platforms)) {
    if (!platformInfo.installer) continue;
    const handler = new ConfigDrivenIdeSetup(platformCode, platformInfo);
    handler.setBmadFolderName(this.bmadFolderName);
    this.handlers.set(platformCode, handler);
  }
}
```

The actual write is verbatim copy from manifest CSV — no template engine, no regex transforms **[OFFICIAL]**:

```javascript
// tools/installer/ide/_config-driven.js (lines 146–195)
async installVerbatimSkills(projectDir, bmadDir, targetPath, config) {
  const csvPath = path.join(bmadDir, '_config', 'skill-manifest.csv');
  if (!(await fs.pathExists(csvPath))) return 0;
  const records = csv.parse(await fs.readFile(csvPath, 'utf8'),
                            { columns: true, skip_empty_lines: true });
  let count = 0;
  for (const record of records) {
    const canonicalId = record.canonicalId;
    if (!canonicalId) continue;
    const sourceDir = path.dirname(path.join(bmadDir, record.path));
    if (!(await fs.pathExists(sourceDir))) continue;
    const skillDir = path.join(targetPath, canonicalId);
    await fs.remove(skillDir);
    await fs.ensureDir(skillDir);
    await fs.copy(sourceDir, skillDir, { filter });   // verbatim copy
    count++;
  }
  return count;
}
```

### Output verification

`test/test-installation-components.js` plus per-IDE marker tests verify the install. The CI workflow `.github/workflows/quality.yaml` runs prettier, eslint, markdownlint, and the install component tests on every PR — explicit comment: "Keep this workflow aligned with `npm run quality` in `package.json`." **[OFFICIAL]**.

### Drift prevention

**Single source of truth: the YAML registry + the CSV manifest.** Skills are not duplicated per IDE; they live once under `_bmad/<module>/` and are copied verbatim. A `removals.txt` file at the project root and per-module lets the installer know which legacy entries to clean up — explicit migration log rather than diff inference. Skills that need different content per IDE simply aren't supported: the design choice is "if it can't be verbatim, don't ship it cross-IDE." This is drift prevention by **eliminating compilation entirely** for the common case.

## claude-task-master — Per-Agent Adapter Factory + Regex Rule Transformer

### Source-of-truth format

`assets/rules/*.mdc` — Cursor's native format chosen as canonical. Five files: `cursor_rules.mdc`, `dev_workflow.mdc`, `self_improve.mdc`, `taskmaster.mdc`, `taskmaster_hooks_workflow.mdc`. The "Cursor first, others derive" choice is intentional: every reference to "cursor.so", "Cursor", `.mdc`, `mdc:` link protocol gets rewritten by the transformer per profile **[OFFICIAL]**.

### Translation/build approach

**Per-agent adapter classes** (one file each: `claude.js`, `cursor.js`, `roo.js`, `cline.js`, `windsurf.js`, `opencode.js`, etc. — 13 profiles in `src/profiles/`) **plus** a regex-based rule transformer (`src/utils/rule-transformer.js`) that consumes per-profile `conversionConfig` objects. Every profile is created via a `createProfile()` factory in `base-profile.js` that returns a standardized config + lifecycle hooks (`onAdd`, `onRemove`, `onPostConvert`). Language: JavaScript / Node ESM **[OFFICIAL]**.

### Code excerpt

The factory — `src/profiles/base-profile.js` (lines 74–94) — accepts a declarative editor config and returns a profile object **[OFFICIAL]**:

```javascript
// src/profiles/base-profile.js
export function createProfile(editorConfig) {
  const {
    name, displayName = name, url, docsUrl,
    profileDir = `.${name.toLowerCase()}`,
    rulesDir = `${profileDir}/rules`,
    mcpConfig = true,
    fileExtension = '.mdc',
    targetExtension = '.md',
    toolMappings = {},
    customReplacements = [],
    fileMap = {},
    onAdd, onRemove, onPostConvert
  } = editorConfig;
  // ...builds conversionConfig with regex patterns...
}
```

A profile declaration is then 30 lines or fewer. Roo Code (which has a non-standard tool vocabulary) uses the `ROO_STYLE` mapping constant to tell the transformer that `edit_file` should become `apply_diff`, `search` becomes `search_files`, etc. **[OFFICIAL]**:

```javascript
// src/profiles/base-profile.js (lines 313–326)
export const COMMON_TOOL_MAPPINGS = {
  STANDARD: {},
  ROO_STYLE: {
    edit_file: 'apply_diff',
    search: 'search_files',
    create_file: 'write_to_file',
    run_command: 'execute_command',
    use_mcp: 'use_mcp_tool'
  }
};

// src/profiles/roo.js (lines 160–170)
export const rooProfile = createProfile({
  name: 'roo',
  displayName: 'Roo Code',
  url: 'roocode.com',
  docsUrl: 'docs.roocode.com',
  toolMappings: COMMON_TOOL_MAPPINGS.ROO_STYLE,
  onPostConvert: onPostConvertRulesProfile,
});
```

The transformer applies regex passes in a fixed order — `src/utils/rule-transformer.js` (lines 144–165) — with a "super aggressive failsafe pass" of global replacements at the end **[OFFICIAL]**:

```javascript
// src/utils/rule-transformer.js
function transformRuleContent(content, conversionConfig, globalReplacements) {
  let result = content;
  result = updateFileReferences(result, conversionConfig);
  result = replaceBasicTerms(result, conversionConfig);
  result = replaceToolReferences(result, conversionConfig);
  result = updateDocReferences(result, conversionConfig);
  // Failsafe pass to catch variations
  globalReplacements.forEach((pattern) => {
    result = result.replace(pattern.from, pattern.to);
  });
  return result;
}
```

For non-rule files (MCP server config), each profile has bespoke transformers. Claude rewrites `mcpServers` to add `type: "stdio"` first; OpenCode rewrites the whole shape to match the OpenCode schema **[OFFICIAL]**:

```javascript
// src/profiles/opencode.js (lines 12–53)
function transformToOpenCodeFormat(mcpConfig) {
  const openCodeConfig = { $schema: 'https://opencode.ai/config.json' };
  if (mcpConfig.mcpServers) {
    openCodeConfig.mcp = {};
    for (const [name, server] of Object.entries(mcpConfig.mcpServers)) {
      const t = { type: 'local' };
      if (server.command && server.args) t.command = [server.command, ...server.args];
      else if (server.command) t.command = [server.command];
      t.enabled = true;
      if (server.env) t.environment = server.env;     // env → environment
      openCodeConfig.mcp[name] = t;
    }
  }
  return openCodeConfig;
}
```

Claude profile is special — it does **not** copy rules into a `.claude/rules/` directory (the plugin marketplace handles that now). Instead it appends an `@./.taskmaster/CLAUDE.md` import line into a top-level `CLAUDE.md`, demonstrating a **content-injection** strategy alongside file copying **[OFFICIAL]**:

```javascript
// src/profiles/claude.js (lines 41–106)
function onAddRulesProfile(targetDir, assetsDir) {
  const sourceFile = path.join(assetsDir, 'AGENTS.md');
  const userClaudeFile = path.join(targetDir, 'CLAUDE.md');
  const taskMasterClaudeFile = path.join(targetDir, '.taskmaster', 'CLAUDE.md');
  const importLine = '@./.taskmaster/CLAUDE.md';
  fs.copyFileSync(sourceFile, taskMasterClaudeFile);
  if (fs.existsSync(userClaudeFile)) {
    const content = fs.readFileSync(userClaudeFile, 'utf8');
    if (!content.includes(importLine)) {
      fs.writeFileSync(userClaudeFile, content.trim() + '\n' + importSection + '\n');
    }
  }
}
```

### Output verification

Per-profile unit + integration tests in `tests/unit/profiles/rule-transformer-{cursor,roo,windsurf,...}.test.js` and `tests/integration/profiles/{cline,codex,gemini,...}-init-functionality.test.js`. Tests are **per-IDE**, mock `fs`, feed sample Cursor source content, and assert the transformed output contains the expected per-profile substitutions. Example structure: each `rule-transformer-{ide}.test.js` tests `convertRuleToProfileRule(source.mdc, target.md, {ide}Profile)` against canonical inputs. The general `rule-transformer.test.js` asserts that `RULE_PROFILES` array (a constant) contains every expected profile and that every entry has the required structural properties (`profileName`, `conversionConfig`, `fileMap`, `rulesDir`, `profileDir`) **[OFFICIAL]**.

### Drift prevention

Three mechanisms **[OFFICIAL]**:

1. **`RULE_PROFILES` constant in `src/constants/profiles.js`** — single array referenced by `isValidProfile()`, by `getRulesProfile()`, and by every test suite. Adding a profile requires touching this list.
2. **Procedural generation comment block** atop `rule-transformer.js`: *"This module procedurally generates `.{profile}/rules` files from `assets/rules` files, eliminating the need to maintain both sets of files manually."*
3. **CI workflow `.github/workflows/ci.yml`** runs format-check + Jest tests on every PR; tests catch any regression in the regex pipeline against checked-in expected outputs.

## continuedev/rules — Frontmatter-Aware AST Transformer in Go

### Source-of-truth format

`.rules/*.md` — markdown with YAML frontmatter using a canonical schema (`description`, `globs`, `alwaysApply`). The CLI tool (binary name `rules`) renders these to nine target formats **[OFFICIAL]**.

### Translation/build approach

**Schema-aware transformer with metadata translation per format.** Source is parsed with a hand-rolled scanner that splits frontmatter from body, then `TransformMetadata()` rewrites or strips fields based on the target schema (e.g., Windsurf turns `alwaysApply: true` into `trigger: always_on`; Copilot turns `globs` into `applyTo`; single-file formats like Claude/Codex/Amp drop frontmatter entirely and concatenate). Language: Go using `gopkg.in/yaml.v3` and `cobra` for the CLI **[OFFICIAL]**.

### Code excerpt

Format declaration is a value type — `internal/formats/formats.go` (lines 33–119) **[OFFICIAL]**:

```go
// internal/formats/formats.go
type Format struct {
    Name            string
    DirectoryPrefix string
    FileExtension   string
    IsSingleFile    bool
    SingleFilePath  string
    Description     string
}

func GetFormat(formatName string) Format {
    switch formatName {
    case "cursor":
        return Format{Name: "cursor", DirectoryPrefix: ".cursor/rules",
                      FileExtension: ".mdc", IsSingleFile: false}
    case "claude":
        return Format{Name: "claude", DirectoryPrefix: "",
                      FileExtension: ".md", IsSingleFile: true,
                      SingleFilePath: "CLAUDE.md"}
    case "copilot":
        return Format{Name: "copilot",
                      DirectoryPrefix: ".github/instructions",
                      FileExtension: ".instructions.md", IsSingleFile: false}
    // ... windsurf, codex, cline, cody, amp
    }
}
```

The metadata transformer is a per-format switch — `internal/formats/transform.go` (lines 191–263) **[OFFICIAL]**:

```go
// internal/formats/transform.go
func TransformMetadata(metadata RuleMetadata, format Format) (RuleMetadata, error) {
    transformed := RuleMetadata{}
    for k, v := range metadata { transformed[k] = v }

    switch format.Name {
    case "windsurf":
        if alwaysApply, ok := metadata["alwaysApply"]; ok {
            delete(transformed, "alwaysApply")
            if alwaysApply == true {
                transformed["trigger"] = "always_on"
            } else {
                transformed["trigger"] = "manual"
            }
        }
    case "copilot":
        if globs, ok := metadata["globs"]; ok {
            delete(transformed, "globs")
            transformed["applyTo"] = globs
        } else {
            transformed["applyTo"] = "**"
        }
    case "claude", "codex", "amp":
        return RuleMetadata{}, nil   // single-file: drop all frontmatter
    }
    return transformed, nil
}
```

Single-file formats (Claude, Codex, Amp) concatenate all rules with `alwaysApply: true` into one file with `## <title>` headings — `internal/formats/singlefile.go` (lines 12–79) **[OFFICIAL]**:

```go
// internal/formats/singlefile.go
func renderToSingleFile(sourceDir string, format Format) error {
    var combinedContent bytes.Buffer
    combinedContent.WriteString("# Rules\n\n")
    err := filepath.Walk(sourceDir, func(path string, info os.FileInfo, err error) error {
        if !strings.HasSuffix(path, ".md") { return nil }
        content, _ := os.ReadFile(path)
        if isAlwaysApply(content) {
            ruleName, _ := GetRuleName(path, sourceDir)
            title := ExtractRuleTitle(content)
            if title == "" { title = ruleName }
            combinedContent.WriteString(fmt.Sprintf("## %s\n\n", title))
            ruleContent := stripFrontmatter(content)
            combinedContent.Write(bytes.TrimRight(ruleContent, " \t\n\r"))
            combinedContent.WriteString("\n\n")
        }
        return nil
    })
    return os.WriteFile(format.SingleFilePath, combinedContent.Bytes(), 0644)
}
```

### Output verification

`internal/formats/render_test.go` (765 lines) and `internal/formats/transform_test.go` (372 lines) run against fixture inputs and golden expected outputs. The CLI itself supports `rules render <format>` for ad-hoc verification **[OFFICIAL]**.

### Drift prevention

**Render-on-demand model.** The .rules/ directory is the only canonical source. Per-tool directories (`.cursor/rules/`, `.windsurf/rules/`, etc.) are generated artifacts; the project's own `README.md` and CLI help describe them as derivatives. There is no standing committed copy of the rendered output — `rules render <format>` is run on demand, so by definition no drift can persist between source and target. This is the cleanest "edit source not compiled" enforcement: there is no compiled artifact in the repo.

## aichaku — Template Discovery + YAML Configuration-as-Code

### Source-of-truth format

`agent-templates/<agent>/base.md` — markdown with YAML frontmatter and structured comments declaring the agent's *context requirements* (`Standards`, `Methodologies`, `Principles`, plus their `Required`, `Defaults`, `Conflicts` subsections). A separate `aichaku.json` per project records the user's selected methodologies, standards, principles, and agents **[OFFICIAL]**.

### Translation/build approach

**Templates discovered at runtime + YAML config injection.** Language: TypeScript (Deno). The `discoverAgentTemplates()` function walks the templates dir; `parseContextRequirements()` extracts the agent's "I need X standards / Y methodologies" from a structured comment block; `resolveContextItems()` intersects that with the user's `aichaku.json` selections and required/default fallbacks; `generateAgentWithFocusedContext()` composes the final agent file with focused YAML blocks. Multiple agent targets (Claude default, etc.) are generated by writing per-agent files into `.claude/agents/` with computed names **[OFFICIAL]**.

### Code excerpt

Template discovery walks the directory using Deno's filesystem API — `src/utils/agent-generator.ts` (lines 81–98) **[OFFICIAL]**:

```typescript
// src/utils/agent-generator.ts
async function discoverAgentTemplates(templateBase: string): Promise<string[]> {
  const agents: string[] = [];
  for await (const entry of Deno.readDir(templateBase)) {
    if (entry.isDirectory) {
      const basePath = join(templateBase, entry.name, "base.md");
      if (await exists(basePath)) {
        agents.push(entry.name);
      }
    }
  }
  return agents;
}
```

Generation composes YAML blocks from selections — `src/utils/agent-generator.ts` (lines 419–485) **[OFFICIAL]**:

```typescript
// src/utils/agent-generator.ts
function generateAgentWithFocusedContext(
  agentType, template, options
): string {
  const standardsToInclude = resolveContextItems(
    options.selectedStandards,
    contextRequirements.standards || [],
    contextRequirements.standardsRequired || [],
    contextRequirements.standardsDefaults || [],
    "standards",
  );
  // similarly methodologies, principles
  const standardsYaml = generateFocusedStandardsYaml(standardsToInclude, conflicts);
  const methodologyYaml = generateFocusedMethodologyYaml(methodologiesToInclude);
  const yamlFrontmatter = { ...yaml,
    name: yaml.name.startsWith(prefix) ? yaml.name : `${prefix}${yaml.name}`,
    methodology_aware: true };
  return `---\n${formatYamlFrontmatter(yamlFrontmatter)}\n---\n\n${[content.trim(), standardsYaml, methodologyYaml, principlesYaml].filter(Boolean).join("\n\n")}`;
}
```

### Output verification

`tests/agent-validation_test.ts` and `tests/agent-template-validation_test.ts` validate generated agents against schema; `installer_test.ts.old` retains historical install verification; the project also ships `--dry-run` mode in the `integrate` command **[OFFICIAL]**.

### Drift prevention

The user's selections are stored in `aichaku.json`. Re-running `integrate` reads selections, regenerates all agents, and overwrites — there is no manual edit window for the compiled artifacts. The `## Directives for Claude Code from Aichaku` marker plus `YAML_CONFIG_START`/`YAML_CONFIG_END` fences make the injected section identifiable and replaceable on subsequent runs (`src/commands/integrate.ts` lines 65–67) **[OFFICIAL]**.

## Nottlespike's setup-agent-guides.sh — Convention-Only via Symlinks

### Source-of-truth format

A single markdown file (defaults to `agent.md` or `AGENTS.md`). No frontmatter, no schema **[PRAC]**.

### Translation/build approach

**Symlink farm with copy fallback.** The script copies the source to `AGENTS.md`, then `ln -sfn AGENTS.md CLAUDE.md` and `ln -sfn AGENTS.md GEMINI.md`. If symlinks fail, three-tier fallback: `ln -sfn` → `ln -s` → `cp`. Updates `.gitignore` to ignore all three so the canonical file never shows up as a duplicate to reviewers. Language: bash **[PRAC]**.

### Code excerpt

```bash
# scripts/setup-agent-guides.sh
ensure_alias_file() {
  local canonical="$1"
  local alias_name="$2"
  if [[ -d "$alias_name" && ! -L "$alias_name" ]]; then
    echo "Error: '$alias_name' is a directory; expected a file path." >&2
    exit 1
  fi
  if ln -sfn "$canonical" "$alias_name" 2>/dev/null; then return 0; fi
  rm -f "$alias_name"
  if ln -s "$canonical" "$alias_name" 2>/dev/null; then return 0; fi
  cp "$canonical" "$alias_name"
  copy_fallback_aliases+=("$alias_name")
}

if [[ "$source_abs" != "$target_abs" ]]; then
  cp "$source_file" AGENTS.md
fi
ensure_alias_file AGENTS.md CLAUDE.md
ensure_alias_file AGENTS.md GEMINI.md
```

### Output verification

`ls -l` shows the symlink targets. The script also `grep -Fxq`s `.gitignore` to verify ignore entries are present **[PRAC]**.

### Drift prevention

**Symlinks make drift impossible** (when supported): `CLAUDE.md` *is* `AGENTS.md` at the inode level. On Windows or filesystems without symlink support, the copy fallback creates an immediate drift window — but the script reports `(copy fallback used)` so the user knows. `.gitignore` entries prevent committed divergence **[PRAC]**.

## Cursor Directory / "rule-porter" — Stand-Alone Cursor → Multi-Target Converter

### Source-of-truth format

`.cursor/rules/*.mdc` — Cursor's MDC format with `description`, `globs`, `alwaysApply` frontmatter **[PRAC]**.

### Translation/build approach

**Zero-dependency CLI** that reads the Cursor rules directory and emits CLAUDE.md, AGENTS.md, GitHub Copilot `.github/copilot-instructions.md`, and Windsurf rules **[PRAC]**. Per the dev.to and Cursor forum announcements, rule-porter is essentially a per-target single-file emitter — same semantics as continuedev/rules' `claude` and `codex` formats, but Cursor-source-specific.

### Code excerpt

I could not retrieve verbatim source from a public repo for rule-porter (the dev.to article describes behavior, not source). Reported behavior **[PRAC]**:

```
$ npx rule-porter --target claude
# reads .cursor/rules/*.mdc, emits CLAUDE.md
$ npx rule-porter --target agents
# emits AGENTS.md
$ npx rule-porter --target copilot
# emits .github/copilot-instructions.md
```

The pattern matches continuedev/rules' single-file emitter for Claude/Codex/Amp closely.

### Output verification

`UNVERIFIED` — repo not inspected directly.

### Drift prevention

`UNVERIFIED` — but per the dev.to writeup, rule-porter is run as a build step (or Husky pre-commit) **[PRAC]**.

## Sourcegraph "rules.so" CLI / continuedev/rules cousin — Format Registry as a Service

### Source-of-truth format

Same `.rules/*.md` schema as continuedev/rules; rules.so is a hosted registry plus the Go CLI **[PRAC]**.

### Translation/build approach

Identical to continuedev/rules (the project is the same `rules` Go binary distributed at rules.so). The hosted registry adds `rules add <package>` to download from a remote, then `rules render <format>` to emit. This adds a fourth axis: **package distribution**, not just translation **[PRAC]**.

### Code excerpt

Already covered under continuedev/rules. The `rules render` command implementation:

```go
// cmd/render.go (lines 30–63)
RunE: func(cmd *cobra.Command, args []string) error {
    formatName := args[0]
    if formatName == "default" {
        return fmt.Errorf("cannot render to default format as it is the source")
    }
    sourceDir, _ := formats.GetRulesDirectory("default")
    if _, err := os.Stat(sourceDir); os.IsNotExist(err) {
        return fmt.Errorf("source directory %s does not exist", sourceDir)
    }
    fmt.Printf("Rendering rules to %s format...\n", formatName)
    verbose, _ := cmd.Flags().GetBool("verbose")
    return formats.RenderRulesToFormat(sourceDir, formatName, verbose)
}
```

### Output verification & Drift prevention

Same as continuedev/rules **[OFFICIAL]**.

## Patterns Synthesis

### "One file, many outputs" via templating
Not observed in pure Handlebars/Mustache/Jinja form. The closest equivalent is **regex-driven content rewriting** (claude-task-master) or **frontmatter-aware schema rewrite** (continuedev/rules). Both projects deliberately avoid templating engines — markdown is the source, transformations are surgical. The reason: template engines force authors to write `{{tool_name}}` everywhere, which makes the source unreadable as a standalone document. Regex-after-the-fact lets the source be a perfect Cursor rule that happens to also compile to others.

### Symlink farm
Observed in Nottlespike's bash script (AGENTS.md ↔ CLAUDE.md ↔ GEMINI.md) **[PRAC]**. Also recommended by ClaudeLog and the Kedro project tracking issue #5408 **[PRAC]**. Limitation: symlinks fail on Windows without dev mode and on some Git hosts when checked out via HTTP/zip — the bash script's three-tier fallback is the canonical mitigation.

### Per-agent adapter classes
Dominant in claude-task-master (one `.js` file per IDE in `src/profiles/`), and in BMAD as a *fallback* for IDEs that need post-processing (Copilot, Kilo, Rovo Dev). Pattern: a `createProfile()` factory + bespoke `onAdd`/`onRemove`/`onPostConvert` lifecycle hooks per IDE. Trade-off: adapter code grows linearly with IDE count, but each adapter is small (30–250 lines) and self-contained.

### Manifest-driven
Dominant in BMAD-METHOD: `platform-codes.yaml` is a flat registry of 30+ platforms. Adding a new IDE that uses `.agents/skills/` as target_dir is a 4-line YAML PR. This scales best as the agent ecosystem fragments — and the cross-tool standard `.agents/skills/` (used by amp, cursor, codex, github-copilot, gemini, opencode, windsurf, etc. per BMAD's `platform-codes.yaml`) lets a single registry entry cover multiple IDEs.

### AGENTS.md as universal
Becoming the convention as of mid-2026. AGENTS.md spec repo + agents.md community standard **[PRAC]**. Continue.dev issue #6716 (open as of 2026) tracks adoption **[PRAC]**. Most agents that consume AGENTS.md as native (Codex, Amp, OpenCode) need no translation at all from a tool that produces AGENTS.md as primary output — only Claude (CLAUDE.md), Cursor (.cursor/rules/), Copilot (.github/instructions/), and Windsurf (.windsurf/rules/) require a translation step.

### Convention-only
The pure form: drop AGENTS.md and trust every agent to find it. `.gitignore` the per-agent variants. Used by smaller projects and demonstrated in the Nottlespike script. The pragmatic limitation as of 2026-04-26: not all agents read AGENTS.md natively yet, so most projects still ship at least a CLAUDE.md (often as a symlink).

### Hybrid approaches

- **BMAD**: manifest-driven for verbatim copy + per-agent post-processing for outliers
- **claude-task-master**: per-agent adapter factory + regex transform pipeline + content injection (Claude's `@./.taskmaster/CLAUDE.md` import line)
- **continuedev/rules**: schema-aware transformer + single-file concatenator for AGENTS.md-style targets
- **aichaku**: template discovery + YAML config-as-code injection + identifiable markers for re-runs

## Drift Mitigation — Cross-Project Patterns

1. **Single source of truth: a constants array**. claude-task-master uses `RULE_PROFILES` (in `src/constants/profiles.js`) referenced by validation, factory, and tests. BMAD uses `platform-codes.yaml`. Adding a profile requires touching this list, which forces tests and code to update together **[OFFICIAL]**.

2. **Per-target unit tests with mocked fs**. claude-task-master ships `rule-transformer-{cursor,roo,...}.test.js` (12 files) — each feeds a Cursor source through the transformer for that profile and asserts the output substitutions. BMAD ships `tests/integration/profiles/{cline,codex,gemini,...}-init-functionality.test.js` for the same purpose **[OFFICIAL]**.

3. **CI runs format-check + lint + tests on every PR**. Both BMAD (`.github/workflows/quality.yaml`) and claude-task-master (`.github/workflows/ci.yml`) run prettier, eslint, and the test suite. Neither ships a "compiled artifacts up to date" check — because compiled artifacts aren't committed.

4. **"Edit source not compiled" enforcement via convention + comments**. claude-task-master's `rule-transformer.js` opens with: *"This module procedurally generates `.{profile}/rules` files from `assets/rules` files, eliminating the need to maintain both sets of files manually."* continuedev/rules avoids the question entirely by not committing compiled output — the user runs `rules render <format>` on demand. BMAD writes per-IDE skills into `.agents/skills/`, `.claude/skills/`, etc. but those directories are gitignored or only present in installed projects, not in the BMAD repo itself.

5. **`removals.txt` migration log**. BMAD ships an explicit `removals.txt` listing entries that should be cleaned up on update — drift detection by explicit allowlist of "things that used to exist." This is rare across the projects studied but useful when you want to retire a skill cleanly **[OFFICIAL]**.

6. **Lifecycle hooks on the source side**. claude-task-master profiles can declare `onAdd` / `onRemove` / `onPostConvert` callbacks that run *after* the standard rule generation. This means custom per-target transforms live with the profile (one file), not in the transformer engine — preventing the engine from turning into a god object as IDE count grows **[OFFICIAL]**.

7. **Symlink-as-drift-elimination**. Where supported, the symlink approach makes drift impossible at the inode level. Used as a primary strategy by Nottlespike's bash script and recommended by AGENTS.md migration guides **[PRAC]**.

## Recommendations for Momentum

The shortest path to multi-agent deployment:

1. **Adopt a `platform-codes.yaml` registry** modeled on BMAD's. Map each agent code (claude-code, cursor, codex, etc.) to its target directory. Lean on the cross-tool `.agents/skills/` standard where possible — BMAD shows ~10+ IDEs share that path, so one registry entry covers all of them.
2. **Verbatim copy as default; per-agent adapter as escape hatch**. Most Momentum skills can ship as-is (Claude Code SKILL.md is already the de facto cross-tool format). Reserve adapter classes only for agents that need real schema transformation (Copilot's `.github/instructions/*.instructions.md`, Roo's tool-name remapping).
3. **Frontmatter-aware schema rewriter (Go or Node) for the few agents that diverge**. Borrow the continuedev/rules `TransformMetadata()` switch — straightforward and well-tested.
4. **Per-IDE integration tests + a `RULE_PROFILES`-style constant** as drift gates. Mirror claude-task-master's structure: one test file per supported agent, one constants array as enforcement point.
5. **Don't commit compiled artifacts**. Render-on-install (BMAD) or render-on-command (continuedev/rules) — never check in `.cursor/rules/` derived from `.rules/`. The diff cost is the drift cost.

## Sources

- [bmad-code-org/BMAD-METHOD on GitHub](https://github.com/bmad-code-org/BMAD-METHOD) — installer at `tools/installer/`, platform registry at `tools/installer/ide/platform-codes.yaml`, CI at `.github/workflows/quality.yaml` **[OFFICIAL]**
- [BMAD-METHOD v6.3.0 release notes](https://newreleases.io/project/github/bmad-code-org/BMAD-METHOD/release/v6.3.0) **[OFFICIAL]**
- [eyaltoledano/claude-task-master on GitHub](https://github.com/eyaltoledano/claude-task-master) — profiles at `src/profiles/`, transformer at `src/utils/rule-transformer.js`, factory at `src/profiles/base-profile.js`, tests at `tests/unit/profiles/` and `tests/integration/profiles/`, CI at `.github/workflows/ci.yml` **[OFFICIAL]**
- [continuedev/rules on GitHub](https://github.com/continuedev/rules) — Go CLI, `internal/formats/formats.go`, `internal/formats/transform.go`, `internal/formats/singlefile.go`, `cmd/render.go` **[OFFICIAL]**
- [RickCogley/aichaku on GitHub](https://github.com/RickCogley/aichaku) — `src/utils/agent-generator.ts`, `src/commands/integrate.ts` (Deno/TypeScript) **[OFFICIAL]**
- [Nottlespike's setup-agent-guides.sh gist](https://gist.github.com/Nottlespike/b2c34baff1d7ba7fa34a8b6df6d326cc) — bash script for AGENTS.md/CLAUDE.md/GEMINI.md symlinking **[PRAC]**
- [agents.md spec site](https://agents.md/) **[PRAC]**
- [Onur Solmaz: CLAUDE.md to AGENTS.md migration](https://solmaz.io/log/2025/09/08/claude-md-agents-md-migration-guide/) **[PRAC]**
- [tessl.io: Agents.md as open standard](https://tessl.io/blog/the-rise-of-agents-md-an-open-standard-and-single-source-of-truth-for-ai-coding-agents/) **[PRAC]**
- [continuedev/continue issue #6716 — AGENTS.md support](https://github.com/continuedev/continue/issues/6716) **[PRAC]**
- [kedro-org/kedro issue #5408 — AGENTS.md + symlinks](https://github.com/kedro-org/kedro/issues/5408) **[PRAC]**
- [Rules CLI docs at rules.so](https://rules.so) **[PRAC]**
- [dev.to: rule-porter announcement](https://dev.to/nedcodes/rule-porter-convert-cursor-rules-to-claudemd-agentsmd-and-copilot-4hjc) **[PRAC]**
- [Cursor forum: Rule-porter thread](https://forum.cursor.com/t/rule-porter-convert-your-mdc-rules-to-claude-md-agents-md-or-copilot/153197) **[PRAC]**
- [task-master-ai on npm](https://www.npmjs.com/package/task-master-ai) — supports 13 IDE profiles **[OFFICIAL]**
- [bmad-code-org/BMAD-METHOD DeepWiki: IDE Integration](https://deepwiki.com/bmad-code-org/BMAD-METHOD/2.2-ide-integration) **[OFFICIAL]**
- [RooCodeInc/Roo-Code on GitHub](https://github.com/RooCodeInc/Roo-Code) — YAML rule pack export/import **[OFFICIAL]**
- [Continue Docs: Rules](https://docs.continue.dev/customize/deep-dives/rules) **[OFFICIAL]**
