---
content_origin: claude-code-subagent-verification
date: 2026-04-26
sub_question: "BMAD multi-agent deployment mechanism — primary source verification against actual repo source code"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
verification_targets: ["bmad-multi-agent-deployment.md description A", "format-translation-patterns.md description B", "gemini-deep-research-output.md description C", "v6.4.0 release status"]
---

# BMAD Multi-Agent Deployment — Source-Verified

## Canonical repo and current version

The canonical repository is **`bmad-code-org/BMAD-METHOD`** on GitHub. The legacy alias `bmadcode/bmad-method` returns a 301 redirect (verified via `curl https://api.github.com/repos/bmadcode/bmad-method` → `"Moved Permanently"`), so any research citing the old org name was reading documentation that may pre-date a transfer.

The current released version is **`v6.5.0`**, released 2026-04-26. The developer's hypothesis that "v6.4.0 may now be released" is confirmed and superseded — `v6.4.0` shipped 2026-04-24 and was followed two days later by `v6.5.0`. None of Descriptions A/B/C mentions v6.5.0, which is the correct current head.

Verification commands (output edited to relevant lines):

```
$ git tag -l | tail -5
v6.3.0
v6.4.0
v6.5.0
$ cat package.json | grep '"version"'
  "version": "6.5.0",
```

`[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/v6.5.0/package.json]`

## Commit SHA inspected

All findings below are pinned to the v6.5.0 release tag at commit SHA **`69cbeb4d07f318180c3d610c511381b9f494e786`** ("chore(release): v6.5.0 [skip ci]").

## Source-of-truth format

The atomic unit is a **`SKILL.md` file with YAML frontmatter inside a directory** — the Claude Skills convention. The `find` invocation `find . -name SKILL.md -not -path "./node_modules/*"` returns 42 files at v6.5.0 (across `src/core-skills/`, `src/bmm-skills/`, and embedded module workflows).

There are **no `*.agent.yaml` files in the canonical agent path**. The only `.agent.yaml` instances anywhere in the repo's full history (`git log --all --diff-filter=A`) are inside `docs/sample-custom-modules/`, `example-custom-content/`, and a `bmd/agents/` directory — i.e., sample/custom-content templates demonstrating how third parties might author content, not BMAD's own agents.

Example skill source (`src/core-skills/bmad-help/SKILL.md`, lines 1-4):

```yaml
---
name: bmad-help
description: 'Analyzes current state and user query to answer BMad questions or recommend the next skill(s) to use. Use when user asks for help, bmad help, what to do next, or what to start with in BMad.'
---
```

`[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/src/core-skills/bmad-help/SKILL.md]`

This frontmatter shape (just `name` + `description`) is exactly the Anthropic Skills format that Claude Code, Cursor, Codex, etc. read directly — no compile step, no XML wrapper, no YAML→Markdown translation.

## Multi-agent projection mechanism

The mechanism is **a single `ConfigDrivenIdeSetup` class driven by a YAML platform registry plus a generated CSV manifest**. There are no per-IDE adapter classes at v6.5.0 — `ls tools/installer/ide/*.js` returns only three files: `_config-driven.js`, `manager.js`, `platform-codes.js` (37 lines, just the YAML loader). All hand-rolled adapter files were deleted.

**Files of record (all pinned to SHA `69cbeb4d`):**

| File | Size | Role |
|---|---|---|
| `tools/installer/ide/platform-codes.yaml` | 306 lines, 42 platforms | Source-of-truth registry: per-platform `target_dir`, `global_target_dir`, `preferred` flag |
| `tools/installer/ide/_config-driven.js` | 568 lines | Single class that handles install/cleanup for every platform |
| `tools/installer/ide/manager.js` | 324 lines | Loads handlers; one `ConfigDrivenIdeSetup` instance per registry entry |
| `tools/installer/core/manifest-generator.js#L400-L419` | — | Writes `_bmad/_config/skill-manifest.csv` listing every skill's canonicalId, name, description, module, source path |

`manager.js#L45-L69` shows the loader has no branching — every platform gets the same handler class:

```javascript
async loadConfigDrivenHandlers() {
  const { loadPlatformCodes } = require('./platform-codes');
  const platformConfig = await loadPlatformCodes();
  const { ConfigDrivenIdeSetup } = require('./_config-driven');
  for (const [platformCode, platformInfo] of Object.entries(platformConfig.platforms)) {
    if (!platformInfo.installer) continue;
    const handler = new ConfigDrivenIdeSetup(platformCode, platformInfo);
    if (typeof handler.setBmadFolderName === 'function') {
      handler.setBmadFolderName(this.bmadFolderName);
    }
    this.handlers.set(platformCode, handler);
  }
}
```

`[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/ide/manager.js#L45-L69]`

The actual install operation is verbatim directory copy from each skill's source dir into `<target_dir>/<canonicalId>/`. From `_config-driven.js#L146-L194`:

```javascript
async installVerbatimSkills(projectDir, bmadDir, targetPath, config) {
  const csvPath = path.join(bmadDir, '_config', 'skill-manifest.csv');
  if (!(await fs.pathExists(csvPath))) return 0;
  const csvContent = await fs.readFile(csvPath, 'utf8');
  const records = csv.parse(csvContent, { columns: true, skip_empty_lines: true });
  for (const record of records) {
    const canonicalId = record.canonicalId;
    if (!canonicalId) continue;
    const sourceFile = path.join(bmadDir, relativePath);
    const sourceDir = path.dirname(sourceFile);
    const skillDir = path.join(targetPath, canonicalId);
    await fs.remove(skillDir);
    await fs.ensureDir(skillDir);
    await fs.copy(sourceDir, skillDir, { filter });
    count++;
  }
  return count;
}
```

`[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/ide/_config-driven.js#L146-L194]`

No frontmatter rewriting. No XML compile. No agent activation prompt synthesis. The source `SKILL.md` lands at the destination byte-for-byte.

## Actual Claude Code emission target

`platform-codes.yaml#L52-L57`:

```yaml
claude-code:
  name: "Claude Code"
  preferred: true
  installer:
    target_dir: .claude/skills
    global_target_dir: ~/.claude/skills
```

`[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/ide/platform-codes.yaml#L52-L57]`

The installer writes to **`.claude/skills/`** (or `~/.claude/skills/` for global). The strings `.claude/commands` and `.claude/agents` appear in the codebase only as **legacy cleanup targets** — `tools/installer/core/legacy-warnings.js#L16` lists `.claude/commands` among directories the installer should warn the user about so stale pre-v6.3 BMAD entries can be removed. There is no code path that writes to `.claude/commands/` or `.claude/agents/` at v6.5.0.

## Resolution table

| Claim | Source | Verdict | Proof |
|---|---|---|---|
| "There are no SKILL.md files; atomic units are `*.agent.yaml`" | Description A | **FALSE** | 42 `SKILL.md` files at v6.5.0; 41 at v6.3.0; 4 at v6.0.0-Beta.6. No `*.agent.yaml` outside docs/sample-custom-modules/ ever. v6.0.0-alpha.0 used `.md` files in `src/core/agents/` (e.g. `bmad-master.md`), not yaml. |
| "16 hand-written adapters at `tools/cli/installers/lib/ide/` (~5k lines)" | Description A | **TRUE BUT STALE** | Was correct for v6.0.0-alpha.0 (`git ls-tree v6.0.0-alpha.0 -- tools/cli/installers/lib/ide/` shows claude-code.js, cline.js, codex.js, crush.js, cursor.js, gemini.js, github-copilot.js, iflow.js, kilo.js, qwen.js, roo.js, trae.js, windsurf.js, etc.). Deleted in commit `513f440a` "refactor(installer): restructure installer with clean separation of concerns" landing in v6.3.0. |
| "Installer at `tools/cli/installers/lib/core/installer.js` (2,063 lines)" | Description A | **STALE PATH** | That path existed through v6.2.x. At v6.5.0 the file is `tools/installer/core/installer.js` (1,607 lines). Same role, relocated by the v6.3.0 refactor. |
| "Per-IDE projection: `.claude/commands/bmad/<module>/agents/<name>.md`" | Description A | **FALSE for v6.3+** | Was the v6.0-alpha emission path (the deleted `claude-code.js` adapter wrote to `.claude/commands` and `.claude/agents` — see `git show v6.0.0-alpha.0:tools/cli/installers/lib/ide/claude-code.js#L13-L15`). Current target is `.claude/skills/<canonicalId>/`. |
| "YAML→XML-Markdown agent compile pipeline" | Description A | **FALSE for v6.3+** | The `.copy()` call in `_config-driven.js#L191` is byte-for-byte. Frontmatter is not rewritten. No XML wrapper is produced. |
| "Single `ConfigDrivenIdeSetup` class driven by `platform-codes.yaml` and `_bmad/_config/skill-manifest.csv`" | Description B | **TRUE** | Confirmed verbatim. See `_config-driven.js#L21` (`class ConfigDrivenIdeSetup`) and `#L149` (`csvPath = ... '_config', 'skill-manifest.csv'`). |
| "30+ agents supported by populating registry alone, no code change" | Description B | **TRUE — undercounted; now 42** | `platform-codes.yaml` has 42 `platforms:` entries at v6.5.0. v6.5.0 changelog: "Support for 18 new agent platforms... bringing total supported platforms to 42 (#2313)." Description B was written when count was ~24 (v6.3.0). |
| "Verbatim SKILL.md directory copying as the sole installation path" | Description B | **TRUE** | `installVerbatimSkills` is the only target-write path inside `installToTarget` (`_config-driven.js#L120-L134`). |
| "Targets `.claude/skills/` (not `.claude/commands/`)" | Description B | **TRUE** | `platform-codes.yaml#L56`. |
| "TypeScript installer at `src/installer/install.ts`" | Description C | **FALSE** | Installer is JavaScript, not TypeScript. Entry is `tools/installer/bmad-cli.js` (per `package.json#L25-L29` `bin` field). The path `src/installer/` does not exist in the repo. |
| "Config at `_bmad/custom/config.toml`" | Description C | **PARTIALLY TRUE** | `_bmad/custom/config.toml` is real — `manifest-generator.js#L425-L426` documents it as "User overrides live in `_bmad/custom/config.toml` and `_bmad/custom/config.user.toml` (never touched by installer)". So Description C correctly identified a real file path but mis-described it as the installer's primary config — the installer-owned files are `_bmad/config.toml` and `_bmad/config.user.toml`, with `custom/` reserved for user override. |
| "BMAD v6.4.0 is current" | developer hypothesis | **SUPERSEDED** | v6.4.0 shipped 2026-04-24; v6.5.0 shipped 2026-04-26 (today). |

## Architectural timeline (resolved)

`git log --reverse --follow tools/installer/ide/_config-driven.js` shows the file first appeared in commit `513f440a` "refactor(installer): restructure installer with clean separation of concerns" (PR #2129). `git tag --contains 513f440a` returns `v6.3.0, v6.4.0, v6.5.0` — meaning the **architectural transition happened between v6.2.2 and v6.3.0**.

However, the seed of the config-driven approach existed earlier: at v6.0.0-Beta.6, `_config-driven.js` and `platform-codes.yaml` were already present at `tools/cli/installers/lib/ide/`, **but alongside** several remaining hand-rolled adapters (`codex.js`, `kilo.js`, `kiro-cli.js`). The v6.3.0 PR `513f440a` (a) deleted the residual hand-rolled adapters, (b) moved the installer from `tools/cli/installers/lib/` to `tools/installer/`, and (c) made the config-driven path the only path.

So the timeline is:

- **v6.0.0-alpha.0 → v6.0.0-Beta.5** (Aug-Sep 2025): 16+ hand-rolled adapters; no SKILL.md files; agents are `.md` files in `src/core/agents/` and `src/modules/<m>/agents/`. **Description A's structural picture matches this era**, except its `*.agent.yaml` claim was always wrong (agents were `.md`, not yaml).
- **v6.0.0-Beta.6 → v6.2.2** (Oct 2025 – Mar 2026): Transitional. `_config-driven.js` introduced; SKILL.md format begins to land (4 files at Beta.6); legacy adapters being deleted incrementally. PR #2078 "remove legacy workflow, task, and agent IDE generators" lands in v6.2.x.
- **v6.3.0** (2026-04-09): Cutover. Hand-rolled adapters fully removed. SKILL.md count jumps to 41. Installer relocated to `tools/installer/`. **Description B's picture starts being accurate from here.**
- **v6.4.0** (2026-04-24): Maintenance release.
- **v6.5.0** (2026-04-26): 42 platforms. Adoption of cross-tool `.agents/skills/` standard for many platforms (per CHANGELOG.md).

Descriptions A and B are **not contradictory** — they are describing the same project at different points in a 7-month evolution. A captured a snapshot from v6.0-alpha; B captured v6.3+. Description C contains genuine errors (TypeScript path, file role) that no commit ever supported.

## Implications for Momentum's design choice

1. **The `*.agent.yaml` source-of-truth idea was never BMAD's mainstream design** — even at v6.0-alpha, agents were authored as `.md` files (e.g., `src/core/agents/bmad-master.md`). Any plan that adopts `*.agent.yaml` as canonical for Momentum would be modeling a phantom.
2. **A single config-driven class plus a YAML registry is enough to support 42 platforms** with no per-platform code. The marginal cost of a new platform is one YAML stanza (`target_dir`, `global_target_dir`).
3. **Verbatim SKILL.md copy is BMAD's verified strategy** — no compile, no transformation. This works because every supported tool (Claude Code, Cursor, Codex, Cline, Gemini CLI, etc.) has converged on directory-with-SKILL.md as the read format. Momentum can adopt this directly.
4. **Cleanup is non-trivial but localized** — `_config-driven.js` includes ~150 lines of cleanup logic (legacy directory removal, copilot-instructions stripping, kilocodemodes stripping, rovodev prompts.yml stripping). Any practice module that writes to multiple platform conventions will need similar cleanup hygiene if it expects to be uninstalled cleanly.

## Sources

All citations are primary source — the BMAD-METHOD repository at pinned commit SHA `69cbeb4d07f318180c3d610c511381b9f494e786` (tag `v6.5.0`, released 2026-04-26):

- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/package.json]` — version, bin field
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/bmad-cli.js]` — CLI entry (108 lines)
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/ide/platform-codes.yaml#L52-L57]` — Claude Code target_dir
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/ide/_config-driven.js#L21-L110]` — class definition
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/ide/_config-driven.js#L146-L194]` — verbatim copy implementation
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/ide/manager.js#L45-L69]` — handler loader (no per-IDE branching)
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/tools/installer/core/manifest-generator.js#L400-L419]` — skill-manifest.csv generation
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/src/core-skills/bmad-help/SKILL.md]` — SKILL.md frontmatter example
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/69cbeb4d/CHANGELOG.md]` — v6.3.0 / v6.4.0 / v6.5.0 release notes
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/blob/v6.0.0-alpha.0/tools/cli/installers/lib/ide/claude-code.js]` — historical hand-rolled adapter (for timeline confirmation)
- `[OFFICIAL-SOURCE — bmad-code-org/BMAD-METHOD/commit/513f440a]` — "refactor(installer): restructure installer with clean separation of concerns" — the v6.3.0 cutover commit

Verification was conducted by cloning `https://github.com/bmad-code-org/BMAD-METHOD` into `/tmp/bmad-verify`, checking out tag `v6.5.0`, and reading the listed files directly. No blogs, NPM page summaries, Medium articles, or release-note third-party summaries were consulted.
