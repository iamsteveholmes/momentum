---
title: "Multi-Agent Deployment Strategies for Agentic Engineering Practice Modules — Research Report"
date: 2026-04-26
type: Technical Research — Consolidated Report
status: Complete
profile: heavy
content_origin: claude-code-synthesis
human_verified: false
verification_wave_authoritative: true
derives_from:
  - path: raw/research-agents-md-adoption.md
    relationship: synthesized_from
  - path: raw/research-bmad-multi-agent-deployment.md
    relationship: synthesized_from
  - path: raw/research-cross-agent-install-cases.md
    relationship: synthesized_from
  - path: raw/research-ecc-exemplar.md
    relationship: synthesized_from
  - path: raw/research-emerging-cross-agent-standards.md
    relationship: synthesized_from
  - path: raw/research-extension-contracts-per-agent.md
    relationship: synthesized_from
  - path: raw/research-format-translation-patterns.md
    relationship: synthesized_from
  - path: raw/research-hook-parity.md
    relationship: synthesized_from
  - path: raw/gemini-deep-research-output.md
    relationship: synthesized_from_with_caveats
  - path: raw/verification-bmad-deep.md
    relationship: authoritative_correction
  - path: raw/verification-claude-hooks.md
    relationship: authoritative_correction
  - path: raw/verification-codex-cli.md
    relationship: authoritative_correction
  - path: raw/verification-opencode.md
    relationship: authoritative_correction
  - path: raw/verification-goose-forgecode-gemini.md
    relationship: authoritative_correction
  - path: raw/verification-agents-md-skills-standards.md
    relationship: authoritative_correction
  - path: raw/verification-sq3-named-targets.md
    relationship: authoritative_correction
  - path: validation/avfl-report.md
    relationship: validated_by
---

# Multi-Agent Deployment Strategies for Agentic Engineering Practice Modules

## 1. Executive Summary

The state of the art on 2026-04-26 has converged on a deceptively simple architecture. **Author one canonical tree of `SKILL.md`-bearing skill directories plus one `AGENTS.md` per project, then project that tree onto each target agent's directory convention via a tiny manifest-driven adapter — no per-agent code, no XML compile, no template engine for the common case.** That is the architecture BMAD adopted between v6.2.x and v6.3.0 (commit `513f440a`, "refactor(installer): restructure installer with clean separation of concerns"); it is the architecture `npx skills` (Vercel Labs), `everything-claude-code`, and `github/spec-kit` independently arrived at; and it is the only architecture that scales to the 38-and-counting consumers of the open Agent Skills format without quadratic per-target maintenance cost.

For Momentum, this means a structurally smaller refactor than expected. The atomic unit (`SKILL.md` with `name` + `description` frontmatter, body Markdown ≤ 500 lines, optional `scripts/`, `references/`, `assets/` subdirs) is already what every reachable target reads. The work is not authoring a translator — it is (a) renaming the canonical source tree from `.claude/skills/` to a tool-neutral location, (b) writing a 200-line installer that reads a `platform-codes.yaml` registry and copies skill directories byte-for-byte to each target's documented path, and (c) explicitly separating the **portable artifact layer** (skills, AGENTS.md, MCP server configs) from the **per-target tail** (Claude Code-only frontmatter fields, hook system bindings, plugin manifest shapes) so the latter can degrade gracefully or be skipped per target.

The non-obvious findings from this corpus, all corroborated against primary-source verification:

- **Codex CLI now ships a Claude-Code-shaped hook system.** As of `rust-v0.125.0` (commit `637f7dd6`), the `codex-rs/hooks/` crate exposes 6 events with the same JSON schema (`hookSpecificOutput.permissionDecision`, etc.). Wave 1 corpus claims that "Codex has no hook system" are stale ([verification-codex-cli.md][VERIFIED-PRIMARY-SOURCE]).
- **Cline reads `.claude/skills/` natively.** Continue.dev does too. So does OpenCode, Goose, and `npx skills`-installed targets. A single `.claude/skills/`-formatted skill tree reaches at least 6 of the 11 agents Momentum cares about with **zero translation** ([verification-opencode.md, verification-goose-forgecode-gemini.md, verification-sq3-named-targets.md][VERIFIED-PRIMARY-SOURCE]).
- **AGENTS.md and Agent Skills are different specs solving different problems**, both now under the AAIF/Linux Foundation umbrella but with different stewards (AGENTS.md is foundation-governed since 2025-12-09; Agent Skills remains Anthropic-stewarded with community PRs and is not yet in AAIF). A complete practice module needs both — AGENTS.md for ambient context, SKILL.md packages for invocable capabilities ([verification-agents-md-skills-standards.md][VERIFIED-PRIMARY-SOURCE]).
- **Hooks do not portably translate. Stop trying.** Claude Code has 28 events; Codex 6; Cline 9; Gemini 11; Goose 0 (PR #8842 in flight); ForgeCode 0 user-facing (in-process Rust callbacks only); ForgeCode does not portably consume external hook configs. Momentum hooks should target Claude Code natively, replicate what is feasible to Codex/Cline/Gemini via per-target emit, and rely on prompt-level discipline elsewhere.
- **The Gemini Deep Research input was structurally unsafe.** It fabricated framework names ("Orchestral AI", "Gradientsys", "DAOTreasury"), invented file paths ("src/installer/install.ts"), cited a nonexistent "GPT-5.4" model and an unsourced "tenfold success rate." Wave 2 verification-by-primary-source corrected the corpus on every load-bearing claim. **Synthesis below carries no specific factual claim from the Gemini file.**

The bottom-line recommendation for Momentum is in §6: adopt the BMAD v6.5.0 architecture (one `ConfigDrivenIdeSetup`-equivalent class, one platform registry, verbatim copy as the default), pair it with `npx skills`-compatible skill metadata for free distribution, ship AGENTS.md as the cross-tool prose layer, and accept that hooks and plugin manifests are Claude-Code-anchored with degraded-mode emit for the next-tier targets.

---

## 2. The Eight Sub-Questions — Resolved Against Verification

### SQ1 — AGENTS.md adoption and authoring (April 2026)

**State.** AGENTS.md is the de-facto cross-tool *prose* standard. It is plain Markdown with no required frontmatter, governed by the [Agentic AI Foundation (AAIF) under the Linux Foundation since 2025-12-09](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) [VERIFIED via verification-agents-md-skills-standards.md], canonical repo `github.com/agentsmd/agents.md` (the openai-namespaced URL is incorrect; AAIF homed it under a neutral org). Founding AAIF contributions were MCP (Anthropic), Goose (Block), and AGENTS.md (OpenAI Codex et al.). Agent Skills was deliberately **not** in the founding tranche.

**Native consumers** (verified at primary source):

- Codex CLI — global `$CODEX_HOME/AGENTS.override.md` > `$CODEX_HOME/AGENTS.md`; project chain walks cwd → project root (default marker `.git`), concatenates every `AGENTS.md` ([verification-codex-cli.md][VERIFIED-PRIMARY-SOURCE]).
- OpenCode — first-match wins among `[AGENTS.md, CLAUDE.md, CONTEXT.md (deprecated)]`; `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT` toggles CLAUDE.md fallback ([verification-opencode.md][VERIFIED-PRIMARY-SOURCE]). **GEMINI.md is not consulted** (corpus claims to the contrary are wrong).
- Goose — hardcoded `[".goosehints", "AGENTS.md"]` plus user-configurable filenames; walks ancestors to git root ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]).
- ForgeCode — three precedence tiers: global → repo root → cwd, all loaded ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]).
- Gemini CLI — **default is `GEMINI.md`, not AGENTS.md**. AGENTS.md is opt-in via `context.fileName: ["AGENTS.md", ...]` in settings ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]).
- Cline — explicit `agentsRulesFile: "AGENTS.md"` plus toggles for `.windsurfrules`, `.cursor/rules/*.mdc`, `.cursorrules` ([verification-sq3-named-targets.md][VERIFIED-PRIMARY-SOURCE]).
- Continue, Roo Code, Cursor, Copilot, Windsurf, Aider — all read AGENTS.md per primary or [OFFICIAL]-tagged community sources.

**Claude Code remains the asymmetric holdout.** Open issue [anthropics/claude-code#34235](https://github.com/anthropics/claude-code/issues/34235) (filed 2026-03-14) requests native AGENTS.md support, no resolution. The de-facto workaround is a one-line `CLAUDE.md` containing `@AGENTS.md` (Claude Code's `@`-import syntax). This is the **pattern `create-next-app` ships by default**, with managed `<!-- BEGIN:nextjs-agent-rules --> ... <!-- END:nextjs-agent-rules -->` markers in AGENTS.md so tools can update their block without clobbering user content [CITED — research-agents-md-adoption.md].

**Authoring guidance from the 2,500-repo GitHub Copilot analysis** [(GitHub blog, 2025-11-19)](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) [CITED]: six durable sections — Commands, Testing, Project Structure, Code Style, Git Workflow, Boundaries. Augment Code's March 2026 guide cites an ETH Zurich finding that LLM-generated AGENTS.md *reduced* task success in 5 of 8 settings while increasing cost 20–23% [PRACTITIONER]; the rising orthodoxy is **human-curated minimal files focused on what agents cannot discover independently**.

### SQ2 — Skill/extension contracts per agent

A complete contract matrix appears in §3. The headline findings, all verified at named release SHAs:

- **Claude Code v2.1.119**: 28 hook events ([verification-claude-hooks.md][VERIFIED-PRIMARY-SOURCE], `https://code.claude.com/docs/en/hooks`); skills at `.claude/skills/<name>/SKILL.md` (project), `~/.claude/skills/<name>/SKILL.md` (personal), plugin-bundled, enterprise-managed; plugin manifest at `.claude-plugin/plugin.json`; marketplace via `.claude-plugin/marketplace.json` git repos. Frontmatter is a **strict superset** of the open Agent Skills spec — adds 12 Claude-Code-only fields enumerated in §5.
- **Codex CLI v0.125.0** (`rust-v0.125.0`, SHA `637f7dd6`): 6 hook events (`PreToolUse`, `PostToolUse`, `PermissionRequest`, `SessionStart`, `UserPromptSubmit`, `Stop`); JSON schema mirrors Claude Code's with one extension (`turn_id`); skills at `<repo>/.codex/skills/`, ancestor `.agents/skills/`, `$CODEX_HOME/skills/.system` (bundled), `/etc/codex/skills/`; **does not read `.claude/skills/`**; sandbox modes `read-only` / `workspace-write` / `danger-full-access`; AGENTS.md global override pattern ([verification-codex-cli.md][VERIFIED-PRIMARY-SOURCE]).
- **Gemini CLI v0.39.1**: 11 hook events (`SessionStart`/`End`, `BeforeAgent`, `AfterAgent`, `BeforeModel`, `AfterModel` *per chunk*, `BeforeToolSelection`, `BeforeTool`, `AfterTool`, `Notification`, `PreCompress`); skills at `.gemini/skills/`, `.agents/skills/` (preferred over `.gemini/skills/` within tier), `~/.gemini/skills/`, `~/.agents/skills/`, extension-bundled; **does not read `.claude/skills/`**; tool names use `read_file`, `run_shell_command`, `replace` (not `edit`), `google_web_search` — frontmatter `allowed-tools` and matchers must use these snake_case names ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]).
- **OpenCode v1.14.28** (canonical org `anomalyco/opencode`; `sst/opencode` 301-redirects to it): no traditional hooks, but a 16-method TypeScript plugin SDK (`@opencode-ai/plugin`) plus 35 bus events surfaced through the single `event` hook; skills at six paths including `.claude/skills/` and `.agents/skills/` (workspace + global); kill-switches `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS`, `OPENCODE_DISABLE_EXTERNAL_SKILLS`, `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT` ([verification-opencode.md][VERIFIED-PRIMARY-SOURCE]).
- **Goose v1.32.0**: no user-facing hook system at v1.32.0; PR #8842 (draft, 2026-04-25) proposes Claude-Code-compatible config schema with 6 events; skills at `.goose/skills/`, `.claude/skills/`, `.agents/skills/` (workspace), and `~/.agents/skills/`, `~/.claude/skills/`, `~/.config/agents/skills/`, `$CONFIG_DIR/skills/` (global); recipes via YAML at `recipe.yaml`; hardcoded AGENTS.md + `.goosehints` ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]).
- **ForgeCode v2.12.9** (canonical org `tailcallhq/forgecode`, not `antinomyhq`): bespoke `Skill` Rust struct (no SKILL.md format compatibility); 6-event in-process Rust callback hooks **not exposed to user config**; AGENTS.md three-tier; `permissions.yaml` with allow/confirm/deny × read/write/command/url; MCP via `.mcp.json` (Claude-compatible) ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]).

### SQ3 — Cross-agent installation architectures (the named targets corrected)

The five targets named in scope.md (Aider, Continue, Cody, Roo Code, Cline) were silently substituted in Wave 1; verification corrected this ([verification-sq3-named-targets.md][VERIFIED-PRIMARY-SOURCE]). The canonical findings:

- **Aider** (`Aider-AI/aider`, v0.86.3.dev) — **No plugin system. No extension API. No entry-point hook.** Distribution is one Markdown file referenced via `--read FILE` or `read: FILE` in `.aider.conf.yml`. The `Aider-AI/conventions` GitHub repo is the community catalog. Slash commands are a closed `cmd_*` method enum on the `Commands` class; cannot register external commands without a fork. **Practice modules targeting Aider must flatten to a single `CONVENTIONS.md`.**
- **Continue.dev** (`continuedev/continue`) — Reads `.continue/rules/*.md`, `.continue/prompts/*.md`, **`AGENTS.md`/`AGENT.md`/`CLAUDE.md`** as `alwaysApply: true` rules, and **`.claude/skills/` SKILL.md trees with full multi-file hierarchy preserved** (`loadMarkdownSkills.ts`). The `continuedev/rules` Go CLI is the first general-purpose translator — emits to `continue`, `cursor`, `windsurf`, `claude`, `copilot`, `codex`/`amp`, `cline`, `cody` formats. Hub registry for assistant slugs.
- **Cody** (`sourcegraph/cody-public-snapshot`, frozen at v1.116.0; product rebrands to "Amp" privately) — Two surfaces: `.cody/commands.json` / `.vscode/cody.json` (custom commands) and `.sourcegraph/<name>.rule.md` (frontmatter-driven hierarchical rules with `repo_filters`, `path_filters`, `language_filters`). **Does not read AGENTS.md or `.claude/skills/`.** No skill multi-file support.
- **Roo Code** (`RooCodeInc/Roo-Code`, v3.53.0) — `.roomodes` custom modes file (YAML/JSON), `.agents/` cross-tool dir read, AGENTS.md/AGENT.md/AGENTS.local.md, plus `.clinerules`, `.cursor/rules/`, `.cursorrules`, `.github/copilot-instructions.md`. The `/init` built-in command actively merges all formats into a unified AGENTS.md. **Roo Marketplace** for mode + rules atomic install (`SimpleInstaller.installMode` writes to `.roo/rules-<slug>/*.md`).
- **Cline** (`cline/cline`, v3.81.0) — **The omnivore.** Reads `.clinerules/`, `.cline/skills/`, **`.claude/skills/`**, `.agents/skills/`, plus all four external rule formats. Has a real **Claude Code-style hooks system** with 9 events (`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `TaskStart`, `TaskResume`, `TaskCancel`, `TaskComplete`, `Notification`, `PreCompact`); supports cancel + context modification + 30s/50KB caps. **The only target in this sample where third-party hooks can enforce policy.**

The cross-cutting takeaway: a single `.claude/skills/`-formatted skill reaches **Claude Code, Continue, Cline, OpenCode, Goose, and `npx skills`-bridged targets** without translation. Roo Code is reachable via `.agents/skills/` mirror. Cody requires `.sourcegraph/*.rule.md` flattening. Aider requires `CONVENTIONS.md` flattening. ForgeCode requires `Skill` struct authoring or skipping skills entirely.

### SQ4 — BMAD v6.5.0 multi-agent deployment internals

Three contradictory descriptions across Wave 1 were resolved by primary-source read at tag `v6.5.0`, SHA `69cbeb4d07f318180c3d610c511381b9f494e786`, released 2026-04-26 ([verification-bmad-deep.md][VERIFIED-PRIMARY-SOURCE]).

**Architecture.** A single `ConfigDrivenIdeSetup` class at `tools/installer/ide/_config-driven.js` (568 lines) handles install/cleanup for all 42 supported platforms. The platform registry is `tools/installer/ide/platform-codes.yaml` (306 lines). The `tools/installer/ide/manager.js` loader (lines 45–69) has no per-IDE branching — every platform gets the same handler class with one `platform-codes.yaml` stanza:

```yaml
claude-code:
  name: "Claude Code"
  preferred: true
  installer:
    target_dir: .claude/skills
    global_target_dir: ~/.claude/skills
```

**Install operation.** Verbatim directory copy from each skill's source dir into `<target_dir>/<canonicalId>/`. From `_config-driven.js` lines 146–194:

```javascript
async installVerbatimSkills(projectDir, bmadDir, targetPath, config) {
  const csvPath = path.join(bmadDir, '_config', 'skill-manifest.csv');
  const records = csv.parse(await fs.readFile(csvPath, 'utf8'),
                            { columns: true, skip_empty_lines: true });
  for (const record of records) {
    const sourceDir = path.dirname(path.join(bmadDir, record.path));
    const skillDir = path.join(targetPath, record.canonicalId);
    await fs.remove(skillDir);
    await fs.ensureDir(skillDir);
    await fs.copy(sourceDir, skillDir, { filter });
    count++;
  }
}
```

**No frontmatter rewriting. No XML compile. No agent activation prompt synthesis.** The source `SKILL.md` lands at the destination byte-for-byte. The atomic unit is the standard Anthropic Agent Skills convention: a directory with `SKILL.md` containing only `name` + `description` frontmatter. 42 such files at v6.5.0 across `src/core-skills/`, `src/bmm-skills/`, and embedded module workflows.

**Architectural timeline.** v6.0.0-alpha.0 (Aug-Sep 2025) had 16+ hand-rolled adapters (`claude-code.js`, `cline.js`, `codex.js`, `cursor.js`, `gemini.js`, etc.) writing to per-tool paths like `.claude/commands/bmad/<module>/agents/<name>.md`. The v6.0.0-Beta.6 → v6.2.2 window (Oct 2025 – Mar 2026) was transitional: `_config-driven.js` introduced, SKILL.md count begins growing, legacy adapters deleted incrementally. Commit `513f440a` (PR #2129, "refactor(installer): restructure installer with clean separation of concerns") was the v6.3.0 cutover — hand-rolled adapters fully removed, installer relocated from `tools/cli/installers/lib/` to `tools/installer/`, config-driven path becomes the only path. v6.5.0 adds 18 new agent platforms in one release, bringing the supported total to 42.

**The takeaway for Momentum.** A single config-driven class plus a YAML registry is enough to support 42 platforms with no per-platform code. The marginal cost of a new agent is **one YAML stanza** (`target_dir`, `global_target_dir`). No type system, no template engine, no XML emission. This is the cheapest cross-agent deployment architecture demonstrated in any project surveyed.

### SQ5 — `everything-claude-code` (ECC) as exemplar

ECC (`affaan-m/everything-claude-code`, MIT, version 1.10.0 as of 2026-04-26) is BMAD's complement: where BMAD is one source → 42 verbatim copies, ECC is one source × manifest-selected-modules → 7 per-target adapters. Both are valid; they serve different problems.

**Reusable architectural elements.**

1. **Manifest-driven selective installer.** `manifests/install-profiles.json` declares 5 named profiles (`core`, `developer`, `security`, `research`, `full`) as lists of module IDs. `manifests/install-modules.json` declares 20 modules, each with `id`, `kind`, `paths[]` (relative to repo root), `targets[]` (whitelist of harnesses), `dependencies[]`, `defaultInstall`, `cost`, `stability`. The install equation is **profile → modules (with deps) → paths × target adapter → file operations**. This composability is the most reusable abstraction in ECC.
2. **Shared-source / per-target adapter pattern.** Top-level `agents/`, `commands/`, `skills/`, `rules/`, `hooks/`, `mcp-configs/` are canonical sources. Dot-prefixed dirs (`.claude/`, `.codex/`, `.opencode/`, `.cursor/`, `.gemini/`) are per-target staging the installer fans out to.
3. **Real installer pipeline, not glorified `cp -R`.** `scripts/install-apply.js` parses `--target`, `--profile`, `--modules`, `--with`/`--without`, `--config`, `--dry-run`, `--json`. Plan object exposes `mode`, `target`, `adapter.id`, `installRoot`, `installStatePath`, `operations[]`, `selectedModuleIds`, `excludedModuleIds`, `skippedModuleIds`, `warnings`. `--dry-run --json` emits a machine-readable plan before any file is touched.
4. **Acceptance that AGENTS.md is the only true cross-tool content layer.** README explicitly states "Claude Code plugins cannot distribute `rules` automatically" — rules require user-side `cp -R` regardless of plugin install. This boundary is honest about platform limits.

**Claude-Code-specific elements (do not lift wholesale).** The `.claude-plugin/plugin.json` manifest, the marketplace.json, the LSP/monitor/output-style packaging — all valid only inside Claude Code. The 40-script `scripts/hooks/` directory is Claude-Code-only.

**The friction.** ECC's three-install-paths-coexist policy (Claude marketplace + OSS shell + npm) is operationally complex; running OSS after marketplace creates duplicate skills and double-fires hooks. Per-target metadata divergence (OpenCode gets 13 agents / 31 commands / 37 skills vs the canonical 48/79/183) is intentional but expensive to maintain by hand.

**ECC star count caveat.** Wave 1 cited "167,488 stars" (implausible for a 3-month-old project, AVFL flagged); released v1.10.0 milestone was "140K stars." Treat all star counts as gameable and excluded from maturity assessment per project policy [feedback_github_stars_unreliable.md].

### SQ6 — Hook/automation parity

**Verified hook event counts.**

| Agent | Events | Source | Notes |
|---|---:|---|---|
| Claude Code | 28 | `code.claude.com/docs/en/hooks` ([verification-claude-hooks.md][VERIFIED-PRIMARY-SOURCE]) | +1 `Setup` in CHANGELOG v2.1.10 not yet on reference page |
| Cline | 9 | `cline/cline` `src/core/hooks/hook-factory.ts:103-130` ([verification-sq3-named-targets.md][VERIFIED-PRIMARY-SOURCE]) | Real Claude-Code-style; supports cancel + context modification |
| Gemini CLI | 11 | `docs/hooks/reference.md` v0.39.1 ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]) | `AfterModel` fires per chunk |
| Codex CLI | 6 | `codex-rs/hooks/src/events/mod.rs` v0.125.0 ([verification-codex-cli.md][VERIFIED-PRIMARY-SOURCE]) | JSON shape mirrors Claude Code; one extension (`turn_id`); +1 Codex-original event (`PermissionRequest`) |
| OpenCode | 0 (16 plugin methods) | `packages/plugin/src/index.ts` v1.14.28 ([verification-opencode.md][VERIFIED-PRIMARY-SOURCE]) | Plugin SDK; bus event firehose with 35 events |
| Goose | 0 | `crates/goose/src/agents/agent.rs` v1.32.0 ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]) | PR #8842 draft proposes 6 events |
| ForgeCode | 0 user-facing | `crates/forge_domain/src/hook.rs` v2.12.9 ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]) | In-process Rust callbacks only |
| Cursor, Continue, Roo Code, Cody, Aider | 0 | per project verification | None has user-defined runtime hooks |

**The portability boundary.** A practice module hook that says "before any `Bash(rm *)` tool call, run a denylist check" can be implemented natively on Claude Code (PreToolUse with `if: "Bash(rm *)"`), Codex (`hooks.json` PreToolUse with regex matcher), Cline (`.clinerules/hooks/PreToolUse.sh`), and Gemini (BeforeTool with matcher on `run_shell_command` snake_case name). It **cannot** be implemented as a runtime gate on OpenCode (use plugin `tool.execute.before` to mutate args, but no first-class deny path), Goose (no system at all yet), ForgeCode (no user surface), or any of the IDE plugins.

**The fallback patterns observed in the wild.**

1. **Push policy into AGENTS.md prose.** Universal but model-discretionary — agents can ignore.
2. **Use git pre-commit hooks** — universal, runs regardless of which agent produced the diff. Best practical floor.
3. **Per-tool denial via `permissions.yaml`** (ForgeCode), `permission` block in agent frontmatter (OpenCode), or `policies/` (Gemini extensions). These are static allow/deny lists, not event-driven hooks.
4. **MCP server-side enforcement.** If a Momentum hook is gating MCP tool calls, the MCP server itself can enforce. This is the only fully portable path.

### SQ7 — Format translation patterns

Three patterns dominate, all observed in production projects:

1. **Manifest-driven config + per-agent adapter classes** — BMAD's `platform-codes.yaml` × `ConfigDrivenIdeSetup`; `claude-task-master`'s `RULE_PROFILES` constants; `github/spec-kit`'s `INTEGRATION_REGISTRY` × `IntegrationBase` / `MarkdownIntegration` / `TomlIntegration` / `SkillsIntegration`. Scales linearly with agent count; new agent = one registry entry. Verbatim copy where formats agree (the `.agents/skills/` standard); custom adapter logic only for outliers (GitHub Copilot's `.github/instructions/*.instructions.md` shape, Roo's tool-name remapping).
2. **Frontmatter-aware AST/regex transforms** — `continuedev/rules` (Go), `claude-task-master`'s `rule-transformer`. A single source markdown is parsed and reserialized per target, mapping argument placeholders (`$ARGUMENTS`, `{{args}}`, `$1..$9`) and renaming tool references. Drift prevention: per-profile golden tests + `RULE_PROFILES` as single source of truth referenced by both code and tests.
3. **Convention-only with symlinks** — `npx skills` (Vercel Labs), Nottlespike-style scripts. Default install method is symlink to a canonical local copy, so editing once propagates to every agent. `--copy` flag falls back to independent copies when symlinks are not viable.

The `npx skills` README pins canonical install paths verbatim ([verification-agents-md-skills-standards.md][VERIFIED-PRIMARY-SOURCE]):

| Agent | Project path | Global path |
|---|---|---|
| Claude Code | `./.claude/skills/` | `~/.claude/skills/` |
| Cursor | `./.agents/skills/` | `~/.cursor/skills/` |
| OpenCode | `./.agents/skills/` | `~/.config/opencode/skills/` |
| Codex | `./.agents/skills/` | `~/.codex/skills/` |

The convergent project-level convention for non-Claude agents is **`.agents/skills/`** (plural). The singular `.agent/skills/` form does not appear in any canonical source — corpus references to it were stray typos.

### SQ8 — Emerging cross-agent standards

**Authority hierarchy** (full taxonomy in §5):

- **AGENTS.md** — AAIF/Linux Foundation since 2025-12-09. Plain Markdown, no frontmatter. Stewarded as foundation property.
- **Agent Skills (open spec)** — `agentskills.io`, repo `agentskills/agentskills`. Apache-2.0 / CC-BY-4.0. **Anthropic-stewarded with community PRs; not yet under AAIF.** ~38 client products. Required frontmatter: `name`, `description`. Optional: `license`, `compatibility`, `metadata`, `allowed-tools` (experimental).
- **Claude Code Skills** — Anthropic product implementation; **strict superset** of the open Agent Skills spec, adding 12 fields the open spec does not define.
- **Skills.sh / `npx skills`** — Vercel Labs MIT. Discovery + install CLI over the open Agent Skills format. Indexes 90,994+ skills. Symlink-by-default.
- **MCP** — also AAIF since 2025-12-09. Universal across all six in-scope agents (Claude, Codex, Gemini, OpenCode, Goose, ForgeCode) and most adjacent ones. The portable capability surface; MCP servers are write-once-deploy-many.
- **ACP (Agent Client Protocol)** — Zed + JetBrains, JSON-RPC 2.0 over stdio, v0.12.2 (2026-04-23). **NOT consume-only**: AgentSideConnection is in the SDK, and the ACP Registry lists production agent-side implementations. But ACP is a *wire protocol*, not a content format — it standardizes how an agent talks to an editor, not what corpus the agent loads. **Not authorable for a practice module.**

The **6-month trajectory** (most-likely scenarios; flagged as forward-looking):

- AAIF likely accepts Agent Skills as a second-tranche contribution (Anthropic has signaled willingness; AAIF holds MCP precedent).
- Open spec v1.1 likely adds: dependency declarations (skill A requires skill B), optional `version` field, normalization of `allowed-tools`.
- `.agents/skills/` becomes canonical neutral location; tool-prefixed paths (`.claude/skills/`, `.gemini/skills/`) survive for backward compat.
- AGENTS.md v1.1 (issue #135) may merge optional YAML frontmatter for progressive disclosure (`description`, `globs`, `alwaysApply`) — would let practice modules ship a *family* of AGENTS.md files that activate contextually.
- Goose hooks land (PR #8842), bringing parity to the Codex/Cline/Gemini bracket.

---

## 3. The Verified Contract Matrix

This is the technical reference, drawn entirely from primary-source verification.

### 3.1 In-scope agents (the six Momentum cares about)

| Capability | Claude Code | Codex CLI | Gemini CLI | OpenCode | Goose | ForgeCode |
|---|---|---|---|---|---|---|
| **Latest verified version** | v2.1.119 | rust-v0.125.0 | v0.39.1 | v1.14.28 | v1.32.0 | v2.12.9 |
| **Verified SHA** | (live docs) | `637f7dd6` | `4d73f3413` | `acd8783a` | `14a8815` | `8a9f3410` |
| **Atomic skill format** | `SKILL.md` (superset frontmatter) | `SKILL.md` (open spec) | `SKILL.md` (open spec) | `SKILL.md` (open spec) | `SKILL.md` (open spec) | bespoke `Skill` Rust struct |
| **Project skill paths** | `.claude/skills/` | `.codex/skills/`, `.agents/skills/` (ancestors) | `.gemini/skills/`, `.agents/skills/` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `.goose/skills/`, `.claude/skills/`, `.agents/skills/` | `.forge/skills/` |
| **Global skill paths** | `~/.claude/skills/` | `$CODEX_HOME/skills/` (deprecated), `~/.agents/skills/`, `$CODEX_HOME/skills/.system` (bundled), `/etc/codex/skills/` | `~/.gemini/skills/`, `~/.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | `~/.agents/skills/`, `~/.claude/skills/`, `~/.config/agents/skills/` | `~/forge/skills/` |
| **Reads `.claude/skills/`?** | yes (own) | **no** | **no** | yes | yes | **no** |
| **Reads `.agents/skills/`?** | no | yes | yes (preferred over `.gemini/skills/` within tier) | yes | yes | no |
| **Hook system** | 28 events (live page) | 6 events | 11 events (`AfterModel` per-chunk) | 0 events; 16-method plugin SDK + 35 bus events | 0 (PR #8842 draft) | 0 user-facing |
| **Hook handler types** | command, http, mcp_tool, prompt, agent | command (prompt/agent reserved) | command, http, in-process | TS plugin module | n/a | n/a |
| **AGENTS.md handling** | `@AGENTS.md` from `CLAUDE.md` (no native) | global override + project-root chain to cwd | opt-in via `context.fileName` array | first-match in `[AGENTS.md, CLAUDE.md, CONTEXT.md]` | hardcoded `[".goosehints", "AGENTS.md"]` | three tiers (global → repo root → cwd) |
| **MCP** | `.mcp.json` | TOML `[mcp_servers]` (stdio + streamable_http) | inside `gemini-extension.json` or `~/.gemini/settings.json` | inside `opencode.json`/`opencode.jsonc` | extensions config | `.mcp.json` (Claude-compatible) |
| **Plugin manifest** | `.claude-plugin/plugin.json` | (none — skills are unit) | `gemini-extension.json` | TS modules + npm | recipes (YAML) | (none — `.forge/` directory) |
| **Marketplace** | git repos with `.claude-plugin/marketplace.json` | `github.com/openai/skills` catalog (informal) | `geminicli.com/extensions/` gallery | npm | informal git/gist | (none) |
| **Sandbox / permissions** | rule syntax `Bash(git *)`, `Skill(name)`; modes default/plan/auto/etc. | `read-only` / `workspace-write` / `danger-full-access` + Windows variant | Docker/Podman/Seatbelt + `excludeTools[]` + `policies/` | per-agent frontmatter `permission` block tri-state | per-extension enable/disable | `permissions.yaml` allow/confirm/deny × read/write/command/url |
| **Custom slash commands** | merged into skills (`.claude/skills/<name>/SKILL.md` creates `/<name>`) | deprecated `~/.codex/prompts/`; user extensibility now via skills | TOML in extension `commands/` dir | `.opencode/commands/<name>.md` frontmatter | recipes + sub-recipes | `.forge/commands/<name>.md` frontmatter |
| **Subagent registration** | `.claude/agents/*.md` | (via skills) | bundled in extensions `agents/` | `.opencode/agents/*.md` | recipes / sub-recipes | `.forge/agents/*.md` |

### 3.2 Opportunistic / Tier-2 targets (the named SQ3 case studies)

| Capability | Aider | Continue.dev | Cody | Roo Code | Cline |
|---|---|---|---|---|---|
| **Latest verified version** | v0.86.3.dev | (monorepo) | v1.116.0 (frozen, rebrand to Amp) | v3.53.0 | v3.81.0 |
| **Plugin/extension API** | **none** | Hub registry (slugs) | none | Marketplace (mode + rules) | hooks + skills + workflows |
| **Reads `.claude/skills/`?** | no | **yes** (full multi-file hierarchy) | no | indirect via `.agents/skills/` | **yes** (4 skill dirs natively) |
| **Reads AGENTS.md?** | yes (via `--read`) | **yes** (`alwaysApply: true`) | no | yes (AGENTS.md, AGENT.md, AGENTS.local.md) | yes |
| **Hook system** | none | none | none | none | **9 events** (real, with cancel + context modification) |
| **Native rule format** | `CONVENTIONS.md` (no schema) | `.continue/rules/*.md` + `.continue/prompts/*.md` (frontmatter: `globs`, `regex`, `alwaysApply`) | `.sourcegraph/*.rule.md` (frontmatter: `repo_filters`, `path_filters`, `language_filters`) | `.roomodes` + `.roo/rules-*/` | `.clinerules/` (open frontmatter; conditional rules engine) |
| **Slash command authoring** | **closed** (cannot register) | via prompts | `.cody/commands.json` / `.vscode/cody.json` | (via modes) | via workflows |
| **Distribution** | one MD file + `--read` flag | Hub OR commit `.continue/` | copy `.sourcegraph/` files (or Sourcegraph backend, enterprise) | Marketplace publish OR commit `.roomodes` | commit `.clinerules/` tree |

The headline: **Continue, Cline, OpenCode, Goose all read `.claude/skills/` natively.** The single canonical Momentum skill tree projected to that path reaches them all.

---

## 4. Cross-Cutting Patterns

Five architectural patterns recur across every project surveyed. Listed in order of decreasing genericity.

**1. The Anthropic Agent Skills atomic unit.** A directory with `SKILL.md` containing `name` + `description` YAML frontmatter, body Markdown ≤ 500 lines, optional `scripts/` / `references/` / `assets/` siblings. This is what BMAD ships, what `npx skills` indexes, what Continue and Cline read natively, what Codex unpacks from `include_dir!` into `$CODEX_HOME/skills/.system`, and what 38+ agent products consume per `agentskills.io/home`. Every successful 2026-era practice module is built on this unit.

**2. Manifest-driven adapter dispatch.** A YAML or JSON registry maps platform code to per-target install metadata; one generic adapter class reads the registry and writes the projection. BMAD's `platform-codes.yaml` × `ConfigDrivenIdeSetup` is the cleanest implementation (37-line YAML loader, no per-IDE branching). `github/spec-kit` and ECC use richer variants but the same idea. The marginal cost of supporting a new agent collapses from "write a 500-line adapter" to "add a 6-line stanza."

**3. Verbatim copy as the default operation.** No frontmatter rewriting, no XML compile, no template engine. Every supported tool has converged on directory-with-SKILL.md as the read format, so the source `SKILL.md` lands at the destination byte-for-byte. Custom transformation logic is reserved for outliers (GitHub Copilot's `.github/instructions/*.instructions.md`, Gemini's snake_case tool name remapping in `BeforeTool` matchers). This is BMAD's verified strategy; ECC uses the same default with selective per-target adapters.

**4. The `.agents/skills/` cross-tool convention.** The convergent project-level neutral path. Codex CLI, Gemini CLI, OpenCode, Goose, and Cline all read it. Roo Code declares it via `getProjectAgentsDirectoryForCwd(cwd)` with the comment "shared directory for agent skills across different AI coding tools." Cursor and Copilot are reachable via `.agents/skills/` per `npx skills`. Claude Code remains the outlier with `.claude/skills/`. **Author once at `.claude/skills/`, mirror to `.agents/skills/` (via symlink or copy), reach almost everything.**

**5. AGENTS.md as the prose layer; everything else needs adapters.** `everything-claude-code` README states explicitly: "Claude Code plugins cannot distribute `rules` automatically." That honesty generalizes — AGENTS.md is the only artifact where one file works everywhere, and even then Claude Code requires the `@AGENTS.md` import workaround. Skills are the next-most-portable (single canonical format, ~38 consumers). MCP servers come third (universal protocol, per-agent config block). Hooks are essentially Claude-Code-only with degraded-mode emit to Codex/Cline/Gemini. Plugin manifests are vendor-specific.

A useful corollary observation: the projects that try to abstract over hooks portably (Wave 1's "hook portability is hopeless" diagnosis) and the projects that try to unify plugin manifests both fail. The successful practice modules **separate the portable layer from the per-target tail** explicitly and accept that the tail is per-target work.

---

## 5. Authority Hierarchy of Standards

Disambiguating four artifacts the Wave 1 corpus consistently conflated. Verified at primary source ([verification-agents-md-skills-standards.md][VERIFIED-PRIMARY-SOURCE]).

### 5.1 AGENTS.md (AAIF / Linux Foundation)

- **Site:** [agents.md](https://agents.md), HTTP 200, Vercel-hosted. **Repo:** `github.com/agentsmd/agents.md`, MIT, ~20.7K stars.
- **Stewardship:** AAIF / Linux Foundation since **2025-12-09**. Founding contributions: MCP, Goose, AGENTS.md.
- **Format:** plain Markdown. **No required fields, no formal frontmatter.**
- **Adoption:** ~60,000+ open-source projects (homepage claim, plausible given GitHub-wide adoption).
- **Role:** project-wide ambient context. The "README for agents."

### 5.2 Agent Skills (open spec)

- **Site:** [agentskills.io](https://agentskills.io). **Repo:** `github.com/agentskills/agentskills`, Apache-2.0 / CC-BY-4.0, ~17K stars, repo created 2025-12-16.
- **Stewardship:** Anthropic-stewarded with community PRs. **NOT yet under AAIF.** This is a meaningful asymmetry vs AGENTS.md.
- **Frontmatter (verbatim from spec):**

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | Max 64 chars; `[a-z0-9-]`; no leading/trailing/consecutive hyphens; matches parent dir name |
| `description` | Yes | Max 1024 chars; what + when |
| `license` | No | License name or bundled file ref |
| `compatibility` | No | Max 500 chars |
| `metadata` | No | Arbitrary string→string map |
| `allowed-tools` | No | Space-separated tool list (**experimental**) |

- **Directory layout:** `skill-name/{SKILL.md, scripts/, references/, assets/}`.
- **Progressive disclosure:** ~100 tokens (metadata at startup) → <5000 tokens (instructions on activation) → resources on demand.
- **Validator:** `skills-ref validate ./my-skill`.

### 5.3 Claude Code Skills (Claude-Code-only superset)

Claude Code's frontmatter is a strict superset of the open spec. The 12 Claude-Code-only fields **silently dropped by every other consumer** are the deployment hazard:

| Field | Description | Behavior elsewhere |
|---|---|---|
| `when_to_use` | Trigger phrases / examples; appended to description | Silently ignored |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` | Silently ignored |
| `arguments` | Named positional args mapped to `$name` substitutions | Silently ignored — substitutions never resolved |
| `disable-model-invocation` | Prevent auto-loading; manual `/name` only | **Silently dropped — auto-load proceeds** (security hazard) |
| `user-invocable` | Hide from `/` menu | Silently ignored |
| `model` | Override session model for the turn | Silently ignored |
| `effort` | low/medium/high/xhigh/max | Silently ignored |
| `context: fork` | Run skill in subagent context | **Silently dropped — runs inline** |
| `agent` | Subagent type (Explore/Plan/general/custom) | Silently ignored |
| `hooks` | Skill-scoped lifecycle hooks | Silently ignored |
| `paths` | Glob patterns to gate auto-activation | Silently ignored — skill activates anywhere |
| `shell` | `bash` or `powershell` | Silently ignored |

`allowed-tools` is shared (open spec marks experimental; Claude Code productized).

**Behaviorally critical guards** — `disable-model-invocation: true` to prevent auto-deploy, `context: fork` for context isolation — are **silently dropped** outside Claude Code. Authoring against the full Claude superset and shipping to other agents is unsafe; gate Claude-only fields behind a Claude-specific copy or accept the degraded behavior.

### 5.4 `npx skills` / Skills.sh (Vercel Labs)

- **Site:** [skills.sh](https://skills.sh), Vercel-hosted, indexes 90,994+ skills. **Repo:** `github.com/vercel-labs/skills`, MIT.
- **Role:** **Discovery + install CLI over the open Agent Skills format. Not a separate format.**
- **Command:** `npx skills add <source>` (the corpus's "install" was wrong). Other: `list`/`ls`, `find`, `remove`/`rm`, `update`, `init`. Sources: GitHub shorthand, GitHub URL, sub-path URL, GitLab, any git URL, local path.
- **Default install method: symlink** to a canonical local copy. `--copy` for independent copies.
- **Reach as of v1.5.1 (2026-04-17):** OpenCode, Claude Code, Codex, Cursor, *"and 41 more"* agents.

The verbatim install paths from the README:

| Agent | Project path | Global path |
|---|---|---|
| Claude Code | `./.claude/skills/` | `~/.claude/skills/` |
| Cursor | `./.agents/skills/` | `~/.cursor/skills/` |
| OpenCode | `./.agents/skills/` | `~/.config/opencode/skills/` |
| Codex | `./.agents/skills/` | `~/.codex/skills/` |

### 5.5 The relationship in one diagram

```
              Linux Foundation / AAIF (since 2025-12-09)
              │
              ├── MCP (Anthropic, 2024) ──────── universal capability protocol
              ├── Goose (Block, 2025) ────────── one consumer
              └── AGENTS.md (OpenAI et al.) ──── prose context layer

              Anthropic (independent — not yet AAIF)
              │
              └── Agent Skills open spec ──┬── Claude Code Skills (superset, +12 fields)
                                           │
                                           ├── Codex Skills, Gemini Skills, etc. (open-spec consumers, ~38 products)
                                           │
                                           └── npx skills (Vercel Labs) ── discovery+install CLI
```

A practice module that writes pure open-spec `SKILL.md` reaches ~38 products including all six in-scope agents. A practice module that writes Claude-Code-extended `SKILL.md` reaches the same 38 with **degraded behavior** outside Claude Code, where critical guards may silently drop. **Default to pure open-spec; reserve Claude-only fields for a Claude-specific projection.**

---

## 6. Recommendations for Momentum

### 6.1 Source-of-truth schema (minimal portable frontmatter)

```yaml
---
name: momentum-create-story          # Required, lowercase + hyphens, matches parent dir
description: Creates a Momentum story with change-type classification, injected EDD/TDD guidance, and AVFL validation. Use when creating a Momentum story.   # Required, ≤ 1024 chars
license: MIT                         # Optional
compatibility: claude-code,codex,opencode,gemini-cli,goose,cline,continue   # Optional, advisory
metadata:                            # Optional — Momentum-internal hints
  momentum-tier: "1"                 # 1=portable, 2=degraded, 3=claude-only
  momentum-needs-hooks: "false"
  momentum-needs-tasks-tool: "false"
allowed-tools: Read Glob Bash(git *) # Optional, experimental — pre-approved tools
---
```

This is the open Agent Skills spec verbatim, with `metadata` carrying Momentum's own tier classification and capability requirements (so the installer can refuse to project Tier-3 skills to non-Claude targets). **Do not author against Claude Code's 12-field superset** at the canonical layer. Claude-only behaviors live in a per-target Claude projection (see 6.2).

### 6.2 Per-target emission table

The Momentum installer reads a `platform-codes.yaml` registry analogous to BMAD's. Per target, it writes:

| Target | Skill output path | AGENTS.md handling | Claude-only-fields | Hook emit | Plugin manifest |
|---|---|---|---|---|---|
| **claude-code** | `.claude/skills/<name>/` | write `CLAUDE.md` containing `@AGENTS.md` | **inject** (full superset) | emit `settings.json` `hooks` block | emit `.claude-plugin/plugin.json` |
| **codex** | `.agents/skills/<name>/` (preferred) or `.codex/skills/<name>/` | write `AGENTS.md` (project root); user already gets global behavior via `$CODEX_HOME/AGENTS.md` | strip | emit `hooks.json` (6 events; map Claude events that have direct equivalents) | n/a |
| **opencode** | `.opencode/skills/<name>/` (preferred) or `.agents/skills/<name>/` | write `AGENTS.md` (first-match-wins respects this) | strip | emit `.opencode/plugins/<name>/index.ts` if Tier-1/2 needs hooks | n/a (TS module is the manifest) |
| **gemini-cli** | `.agents/skills/<name>/` (preferred over `.gemini/skills/`) | write `AGENTS.md`; require user `context.fileName: ["AGENTS.md", ...]` in `~/.gemini/settings.json` (document this) | strip; **remap any tool-name-bearing fields to snake_case** (`run_shell_command`, `read_file`, `replace`, `google_web_search`) | emit `gemini-extension.json` → `hooks/hooks.json` (11 events; closer to Claude Code than Codex) | emit `gemini-extension.json` |
| **goose** | `.agents/skills/<name>/` (preferred) or `.goose/skills/<name>/` | write `AGENTS.md` (hardcoded read alongside `.goosehints`) | strip | **skip until PR #8842 merges**; document fallback to AGENTS.md prose | n/a |
| **forgecode** | (skip skills — bespoke `Skill` Rust struct, no SKILL.md format) | write `AGENTS.md` (3-tier read) | n/a | skip | (`.forge/` dir for commands if Momentum has slash-command equivalents) |

For Tier-2 opportunistic targets:

| Target | Output |
|---|---|
| **continue** | symlink/copy `.claude/skills/` (read natively) + write `.continue/rules/momentum.md` for any pure-prose rules |
| **cline** | symlink/copy `.claude/skills/` (read natively) + emit `.clinerules/hooks/<event>.sh` for hooks where applicable (9 events) |
| **roo-code** | symlink to `.agents/skills/` + emit `.roomodes` if Momentum has mode-equivalents |
| **cody** | flatten skills to `.sourcegraph/<name>.rule.md` (loses multi-file hierarchy); emit `.cody/commands.json` for slash commands |
| **aider** | flatten one canonical `CONVENTIONS.md` into project root; instruct user to add `read: CONVENTIONS.md` in `.aider.conf.yml` |
| **cursor / copilot** | `.agents/skills/<name>/` (per `npx skills`) |

### 6.3 Tier 1 / 2 / 3 target classification

**Tier 1 — first-class Momentum targets, full feature parity.** Hooks emitted, all skills projected, plugin manifest written, CI smoke-test.

- Claude Code (canonical home; full superset)
- Codex CLI (verified hook system as of v0.125.0)
- OpenCode (rich plugin SDK; reads `.claude/skills/` natively for free reach)

**Tier 2 — supported, degraded behavior on hooks/plugins.** All skills projected, AGENTS.md written, hooks emitted where the agent has a system, plugin manifest if applicable, no CI smoke-test (manual on releases).

- Gemini CLI (11-event hook system; opt-in AGENTS.md via settings)
- Cline (real hooks, omnivorous reader)
- Continue.dev (reads `.claude/skills/` and AGENTS.md natively)

**Tier 3 — best-effort projection. Skills only. No hooks, no plugin manifest.** Document the gap. Updates are user-driven copy.

- Goose (until PR #8842 merges, then promote to Tier 2)
- Roo Code (no hooks; Marketplace publish optional)
- Cursor, Copilot (no first-class hook system; reach via `npx skills` symlink)
- ForgeCode (skip skills entirely; AGENTS.md only — bespoke skill format, in-process Rust hooks not user-configurable)
- Cody (flatten to `.sourcegraph/*.rule.md`; loses multi-file hierarchy)
- Aider (flatten to `CONVENTIONS.md`; loses skill granularity)

The rationale: Tier 1 is where Momentum's behavioral guarantees hold. Tier 2 honors the prose and skill layer but degrades hook-based enforcement to model-discretionary policy. Tier 3 is "ambient context only" — a Momentum-aware user gets nothing more than a vanilla Aider user except the project's prose.

### 6.4 Hook portability boundary

The empirical bracket:

- **Have a real user-facing hook system:** Claude Code (28), Gemini CLI (11), Cline (9), Codex CLI (6).
- **No user-facing hook system as of 2026-04-26:** OpenCode (has plugin SDK with bus events; not the same shape), Goose (PR #8842 in flight), ForgeCode (in-process Rust callbacks, not user-configurable), Roo, Continue, Cursor, Cody, Aider.

The Claude-Code → Codex → Cline → Gemini event map (only events with direct semantic equivalents):

| Claude Code | Codex | Cline | Gemini |
|---|---|---|---|
| `PreToolUse` | `PreToolUse` | `PreToolUse` | `BeforeTool` |
| `PostToolUse` | `PostToolUse` | `PostToolUse` | `AfterTool` |
| `UserPromptSubmit` | `UserPromptSubmit` | `UserPromptSubmit` | `BeforeAgent` (per turn, not per submit — close but not exact) |
| `SessionStart` | `SessionStart` | `TaskStart` (close) | `SessionStart` |
| `Stop` | `Stop` | `TaskComplete` (close) | `AfterAgent` |
| `PermissionRequest` | `PermissionRequest` | n/a | n/a |
| `PreCompact` | n/a | `PreCompact` | `PreCompress` |
| `Notification` | n/a | `Notification` | `Notification` |
| (24 others) | n/a | n/a | n/a |

A Momentum hook that uses any of the 24 Claude-only events (`InstructionsLoaded`, `WorktreeCreate`, `TaskCreated`, `TeammateIdle`, `Elicitation`, etc.) is **Claude-Code-anchored**. Document this explicitly per skill; use the `metadata.momentum-tier: "3"` flag to refuse cross-target emit when the skill depends on a Claude-only event.

### 6.5 The boundary between portable artifacts and CLI-orchestrator-required behaviors

Some Momentum behaviors are **not skill content at all** — they are orchestration that requires the surrounding CLI agent to be Claude Code (or equivalent). Examples extracted from the available Momentum skill list:

- **TaskCreate / TaskList / TaskUpdate** — Claude Code-specific tools. Skills referencing them ("structural state to prevent context drift in long workflows" per `project_task_tracking_for_drift.md`) are **Claude-anchored** even if the skill body is portable.
- **Plan Mode / ExitPlanMode** — Claude Code-specific. The `momentum:plan-audit` skill and the `plan-audit.md` rule depend on this hook.
- **MCP-name references** — skills that hard-code `mcp__claude-in-chrome__*` tool names break outside Claude Code.
- **The `Agent` / `Skill` tools and TeamCreate / SendMessage** — fan-out and team primitives are Claude Code's native patterns; OpenCode has analogous TS-plugin patterns but the prompts differ.
- **Subagent model with separate context windows** — Claude Code, Cursor, OpenCode have it; Codex has it via `context: fork` (own subagent semantics); Gemini has it via extensions; Goose uses sub-recipes.

The honest framing for Momentum's docs: **the skill *body* is portable Markdown; the skill's *invocation pattern* is what's tier-classified.** A Momentum skill that says "use Read and Glob to find files" is Tier-1 portable; one that says "use TaskCreate to track substeps" is Tier-3 Claude-only. Mark this in `metadata.momentum-needs-tasks-tool: "true"`.

### 6.6 Worked example: tracing `momentum:create-story` to six agents

Take Momentum's `momentum:create-story` skill (description: "Creates a Momentum story with change-type classification, injected EDD/TDD guidance, and AVFL validation"). Assume canonical source at `momentum/.skills/create-story/SKILL.md`.

**Canonical source content:**

```yaml
---
name: create-story
description: Creates a Momentum story with change-type classification, injected EDD/TDD guidance, and AVFL validation. Use when creating a Momentum story.
license: MIT
compatibility: claude-code,codex,opencode,gemini-cli,goose,cline,continue
metadata:
  momentum-tier: "2"
  momentum-needs-tasks-tool: "false"
  momentum-needs-hooks: "false"
allowed-tools: Read Glob Edit Bash(git *)
---
# Create Story

[body markdown — workflow phases, gather inputs, write to backlog index, etc.]
```

**Projection table** (what the Momentum installer writes, per target):

| Target | Files written | Skill body transformations |
|---|---|---|
| **claude-code** | `.claude/skills/create-story/SKILL.md` (verbatim copy + inject any Claude-superset fields from a sibling `claude-overlay.yaml` if present), `.claude-plugin/plugin.json` references skill | **None at body level**; frontmatter unioned with Claude overlay |
| **codex** | `.agents/skills/create-story/SKILL.md` (verbatim copy) | None |
| **opencode** | `.opencode/skills/create-story/SKILL.md` (verbatim copy); installer also creates symlink `.claude/skills/create-story/` so OpenCode's six-path scan finds it | None |
| **gemini-cli** | `.agents/skills/create-story/SKILL.md` (verbatim copy); `gemini-extension.json` references this skill dir | If `allowed-tools` has Claude tool names, **rewrite to Gemini snake_case**: `Read` → `read_file`, `Bash` → `run_shell_command`, `Edit` → `replace`. The body usually does not name tools; but if it does, document the tool-name divergence. |
| **goose** | `.agents/skills/create-story/SKILL.md` (verbatim copy) | None |
| **forgecode** | **Skip** — body content folded into `AGENTS.md` as prose section "How to create a Momentum story" since ForgeCode does not consume SKILL.md |

The `momentum:create-story` skill is Tier-2 because its full guidance includes references to Momentum sprint state files written by `momentum:sprint-manager` — those references are portable as filenames but the workflow only "completes correctly" inside an environment that has TaskList/TaskUpdate available (Claude/OpenCode/Cursor) or a documented fallback. The installer logs the tier-2 caveat in its `--dry-run --json` plan so the user knows what they're getting.

The same projection logic applies to other Momentum skills:

- `momentum:impetus` (orchestrator with subagent spawn semantics) — **Tier 3, Claude-anchored**. Document the equivalent pattern for OpenCode (TS plugin with its own sub-agent dispatch) and Goose (sub-recipes), but the canonical implementation is Claude Code.
- `momentum:dev` / `momentum:sprint-dev` (worktree-driven dev with AVFL post-merge) — **Tier 3** (uses `WorktreeCreate` hook semantics).
- `momentum:create-story`, `momentum:intake`, `momentum:distill` — **Tier 2**. Body is portable; orchestration is Claude-leaning but not strict.
- `momentum:research` — **Tier 1 candidate**. Body is workflow Markdown; the actual subagent fan-out is Claude-Code-specific but the *recipe* is portable.

### 6.7 Concrete refactor sketch

Six pieces of work for Momentum, in suggested order:

1. **Rename canonical skill source from `.claude/skills/` to `momentum/.skills/`** (or similar tool-neutral path). This is one `git mv` plus a sweep of internal references. Single biggest invariant lock-in point.
2. **Strip Claude-only fields from canonical SKILL.md frontmatter** (`when_to_use`, `disable-model-invocation`, `argument-hint`, `arguments`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`). Move them into per-target overlays at `momentum/.skills/<name>/claude-overlay.yaml` if Momentum genuinely needs them; otherwise fold the content into the Markdown body.
3. **Write `momentum/installer/platform-codes.yaml`** with stanzas for the seven Tier-1/2/3 targets. Template:
   ```yaml
   platforms:
     claude-code:
       name: "Claude Code"
       tier: 1
       installer:
         skill_dir: .claude/skills
         global_skill_dir: ~/.claude/skills
         emit_plugin_manifest: true
         emit_hooks: true
         claude_overlay: true
     codex:
       name: "Codex CLI"
       tier: 1
       installer:
         skill_dir: .agents/skills
         global_skill_dir: ~/.agents/skills
         emit_hooks: true
         hook_event_map: codex   # 6-event subset
     # ...
   ```
4. **Write a single `MomentumIdeSetup` adapter class** modeled on BMAD's `ConfigDrivenIdeSetup` — verbatim directory copy by default, with hook points for (a) AGENTS.md root write, (b) plugin manifest emit, (c) hook config emit, (d) claude-overlay merge.
5. **Write a Momentum-specific cleanup pass** — analogous to BMAD's `_config-driven.js` cleanup logic (~150 lines of legacy directory removal, copilot-instructions stripping, etc.). Practice modules that write to multiple platform conventions need uninstall hygiene if they expect to be uninstalled cleanly.
6. **Validate via `npx skills` install path.** Once Momentum's source-of-truth is canonical Agent Skills, users can install with `npx skills add github:user/momentum/momentum/.skills/<name>` for any skill, agent-side, with no Momentum-specific installer required. This is the free-distribution win.

### 6.8 What Momentum should NOT try

- **Do not write a hook abstraction layer.** Hook systems differ in event count (6 to 28), event semantics, blocking model, and JSON schema. Codex mirrors Claude Code's JSON shape closely enough to share a config, but every other agent has its own. Emit per-target hook configs from a Momentum hook spec file, not at runtime.
- **Do not adopt ACP.** It is a wire protocol between agent and editor; it does not give Momentum a content surface. Momentum runs alongside ACP-implementing agents, not via ACP.
- **Do not unify plugin manifests.** `.claude-plugin/plugin.json`, `gemini-extension.json`, OpenCode TS modules, and BMAD's lack of plugin manifest at all are structurally different. Emit each shape from a Momentum module spec file.
- **Do not depend on `context: fork` or `disable-model-invocation` in cross-target skills.** Both silently degrade.
- **Do not rely on AGENTS.md for capability registration** — only for prose. Capabilities live in skills, plugins, MCP, hooks.
- **Do not ship to Aider beyond a flat `CONVENTIONS.md`.** Aider's plugin-system absence means deeper integration requires a fork; not worth Momentum's investment.

---

## 7. Quality Notes — What This Research Got Wrong (and Right)

**The corpus exhibited measurable hallucinations across Wave 1**; AVFL flagged them; Wave 2 verification corrected them. A note on each major correction so future research can recognize the pattern.

**Wrong in Wave 1, corrected in Wave 2:**

- **BMAD architecture.** Wave 1 produced three mutually incompatible descriptions: (A) v6.0-alpha hand-rolled installer with `*.agent.yaml` source-of-truth, (B) v6.3.0 config-driven verbatim copy, (C) Gemini's fabricated `src/installer/install.ts` TypeScript installer. Verification at v6.5.0 SHA `69cbeb4d` confirmed (B); (A) was true for v6.0-alpha but stale; (C) was fabricated (the path does not exist; the installer is JavaScript) ([verification-bmad-deep.md][VERIFIED-PRIMARY-SOURCE]).
- **Codex hook system.** Wave 1 split between "Codex has no hooks" and "Codex has 6 events." Verification at `rust-v0.125.0` confirmed 6 events with full Claude-Code-shaped JSON schema ([verification-codex-cli.md][VERIFIED-PRIMARY-SOURCE]). Any Wave 1 source claiming Codex is hookless was reading pre-v0.124 docs.
- **Claude Code hook count.** Wave 1 split between "8 events" and "28 events," both [OFFICIAL]-tagged. Verification at `code.claude.com/docs/en/hooks` (live page, 2026-04-26) confirmed 28 documented events plus a 29th (`Setup`) in CHANGELOG v2.1.10 ([verification-claude-hooks.md][VERIFIED-PRIMARY-SOURCE]). The "8" figure was a v1.0-era snapshot.
- **OpenCode canonical org and stars.** Wave 1 cited "sst/opencode" with 36K stars. Verification: `sst/opencode` 301-redirects to `anomalyco/opencode` (same repo ID `975734319`), and stargazers_count is **150,109** ([verification-opencode.md][VERIFIED-PRIMARY-SOURCE]). The "36K" figure was 4× too low.
- **OpenCode skills support.** Wave 1 listed [UNVERIFIED] (404). Verification confirmed full SKILL.md support with six-path discovery, including `.claude/skills/` and `.agents/skills/` natively ([verification-opencode.md][VERIFIED-PRIMARY-SOURCE]).
- **Goose cross-tool reads.** Wave 1 claimed Goose reads `.codex/skills/`, `.cursor/skills/`. Verification at v1.32.0: Goose reads only `.goose/skills`, `.claude/skills`, `.agents/skills` (workspace) plus user-level variants ([verification-goose-forgecode-gemini.md][VERIFIED-PRIMARY-SOURCE]). The Codex/Cursor cross-tool reads were fabricated.
- **ForgeCode canonical org.** Wave 1 split between `tailcallhq` and `antinomyhq`. Verification: `tailcallhq/forgecode` is canonical (the install pipeline `forgecode.dev/cli` and Nix flake both point at it).
- **Agent Skills governance.** Wave 1 implied AAIF stewardship. Verification: Agent Skills is **Anthropic-stewarded with community PRs**; AAIF founding contributions were MCP, Goose, AGENTS.md only (2025-12-09). Agent Skills repo created 2025-12-16, one week after AAIF launch, deliberately *not* in the founding tranche ([verification-agents-md-skills-standards.md][VERIFIED-PRIMARY-SOURCE]).
- **`.agents/skills/` vs `.agent/skills/`.** Wave 1 referenced both. Verification: `.agents/skills/` (plural) is canonical per `npx skills` README. The singular form is a stray typo.
- **The Aider/Continue/Cody/Roo/Cline named targets** were **silently substituted** in Wave 1 (11 alternative case studies given, 5 named targets received only mention-level coverage). The dedicated verification round restored substantial coverage.

**Right in Wave 1, confirmed by Wave 2:**

- BMAD's config-driven architecture (described accurately by the file matching v6.3+ snapshot).
- The `SKILL.md` Anthropic spec as the convergent atomic unit.
- AGENTS.md as universal prose layer with `@AGENTS.md` Claude workaround.
- Continue and Cline as native consumers of `.claude/skills/`.
- Gemini CLI's per-chunk `AfterModel` and snake_case tool name remapping.
- ECC's manifest-driven selective-install pattern as the architectural seed for component picking.
- Hook portability is hopeless across the full agent set — only Codex shares a JSON shape with Claude Code.

**Discounted entirely (Gemini Deep Research file):**

- Invented frameworks: "Orchestral AI", "Gradientsys", "HEPTAPOD", "DAOTreasury", "OpenCode Go", "Cyber Verification Program", "managed-agents-2026-04-01" header.
- Fabricated facts: "GPT-5.4" model (does not exist), "Opus 4.7 visual acuity 54.5% → 98.5%" (uncited), "$5/$25 per Mtok" pricing (uncited), "58s → 31s Codex benchmark" (uncited), "tenfold success-rate increase, 26% gain on terminal operations" (uncited).
- Wrong code paths: `src/installer/install.ts` for BMAD (does not exist; installer is JS at `tools/installer/bmad-cli.js`), `.taskmaster/config.json` for Spec-Kit (does not exist; verified is `assets/rules/*.mdc`), `_bmad/custom/config.toml` mis-described as the installer's primary config.
- Press-release register inappropriate for technical research.
- Off-scope content (NIST, OWASP, theoretical Cline-vs-Aider debate, DAOTreasury crypto governance) >50% of document.

**Where evidence is still thin** (after both waves):

- The exact `SLASH_COMMAND_TOOL_CHAR_BUDGET` defaults across Claude Code minor versions; documentation cites "1% of context window, fallback 8,000 chars" without per-version breakdown.
- The behavioral guarantees of `.agents/skills/` as a name; while the convention is documented in 4+ projects, no single SDO has chartered it. Risk is low (no contradictory uses observed) but not zero.
- The future of Anthropic's Agent Skills under AAIF — every public signal points to eventual donation, but no published timeline exists as of 2026-04-26.
- Whether `npx skills` will introduce **server-side discovery** (centralized registry) vs continuing repo-driven local scanning. If it does, practice modules may need to publish to the registry explicitly.

---

## 8. Open Questions / Follow-up Research Needed

1. **Will Anthropic donate Agent Skills to AAIF?** Foundation governance would harden the spec. Without it, Anthropic could in principle change `SKILL.md` semantics and break ~38 consumers. Likelihood is high (MCP precedent, public signaling) but unconfirmed. Re-check 2026-Q3.
2. **Will Goose ship hooks (PR #8842) within 2 minor versions?** Material to Tier-2/3 classification.
3. **Will ACP add a content surface?** The "ACP + Deep Agents" April 2026 JetBrains piece hints at resource/context handoff. If it does, ACP becomes adjacent-relevant for Momentum's IDE integration story.
4. **Will AGENTS.md v1.1 (issue #135) ship?** The optional-frontmatter-with-globs proposal would change the deployment calculus — Momentum could ship a *family* of scoped AGENTS.md files (one per skill / domain) that activate contextually rather than concatenate everything always.
5. **What does the Cody → Amp rebrand mean for public surface?** The migration is closing public APIs; new behaviors land in private Sourcegraph repos. Practice modules targeting Cody have a 6-12 month sunset risk. Worth a watch but not a Tier-1 commitment.
6. **Will Cursor and Copilot publish hook contracts?** Both have rules engines (`.cursor/rules/`, `.github/copilot-instructions.md`) but no first-class hook surface. If either ships hooks, Tier-1 expands.
7. **Will Anthropic ship native AGENTS.md support?** Issue #34235 is the most-watched holdout. Resolution would simplify the cross-tool prose layer materially.
8. **Per-target metadata count divergence (ECC pattern) — is that sustainable for Momentum?** ECC ships 13 OpenCode agents vs 48 canonical. The selective-install architecture makes that cheap to maintain manifest-side, but expensive in user-trust ("which Momentum am I getting?"). Decide whether Momentum projects the full set everywhere or curates per-target.

---

## 9. Sources

### VERIFIED — primary repo sources at named commit SHAs (Wave 2 verification files)

| Topic | Repo | Tag / SHA | Verification file |
|---|---|---|---|
| BMAD multi-agent installer | `bmad-code-org/BMAD-METHOD` | v6.5.0 / `69cbeb4d` | [verification-bmad-deep.md] |
| Claude Code hooks | `anthropics/claude-code` (live docs) | v2.1.119 / 2026-04-26 fetch | [verification-claude-hooks.md] |
| Codex CLI extension contract | `openai/codex` | rust-v0.125.0 / `637f7dd6` | [verification-codex-cli.md] |
| OpenCode | `anomalyco/opencode` | v1.14.28 / `acd8783a` | [verification-opencode.md] |
| Goose | `block/goose` | v1.32.0 / `14a8815` | [verification-goose-forgecode-gemini.md] |
| ForgeCode | `tailcallhq/forgecode` | v2.12.9 / `8a9f3410` | [verification-goose-forgecode-gemini.md] |
| Gemini CLI | `google-gemini/gemini-cli` | v0.39.1 / `4d73f3413` | [verification-goose-forgecode-gemini.md] |
| Agent Skills, AGENTS.md, Skills.sh, AAIF | `agentsmd/agents.md`, `agentskills/agentskills`, `vercel-labs/skills`, AAIF press release | live, 2026-04-26 fetch | [verification-agents-md-skills-standards.md] |
| Aider | `Aider-AI/aider` | HEAD `3ec8ec5` | [verification-sq3-named-targets.md] |
| Continue.dev | `continuedev/continue` | HEAD `cb27309` | [verification-sq3-named-targets.md] |
| Cody | `sourcegraph/cody-public-snapshot` | HEAD `8e20ac6` | [verification-sq3-named-targets.md] |
| Roo Code | `RooCodeInc/Roo-Code` | HEAD `ad25634` | [verification-sq3-named-targets.md] |
| Cline | `cline/cline` | HEAD `5fe6c9a` | [verification-sq3-named-targets.md] |

### CITED — official docs URLs and [OFFICIAL]-tagged Wave 1 sources

- [agents.md](https://agents.md) — AGENTS.md canonical spec
- [github.com/agentsmd/agents.md](https://github.com/agentsmd/agents.md) — AGENTS.md repo
- [agents.md issue #135 — v1.1 proposal](https://github.com/agentsmd/agents.md/issues/135)
- [agents.md issue #10 — Frontmatter support](https://github.com/agentsmd/agents.md/issues/10)
- [Linux Foundation announces AAIF (2025-12-09)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [AAIF homepage](https://aaif.io/)
- [agentskills.io](https://agentskills.io) and [agentskills.io/specification](https://agentskills.io/specification)
- [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills)
- [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) — Claude Code Skills
- [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) — Claude Code hooks reference (live, 2,549 lines)
- [code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide) — hooks quickstart
- [github.com/anthropics/claude-code/blob/main/CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) — release notes (3,285 lines, v1.0.x through v2.1.119)
- [anthropics/claude-code Issue #34235](https://github.com/anthropics/claude-code/issues/34235) — AGENTS.md feature request
- [skills.sh](https://skills.sh) and [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills)
- [opencode.ai/docs/skills](https://opencode.ai/docs/skills) and [opencode.ai/docs/rules/](https://opencode.ai/docs/rules/)
- [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills) and [developers.openai.com/codex/guides/agents-md](https://developers.openai.com/codex/guides/agents-md)
- [github.com/openai/skills](https://github.com/openai/skills) — Codex skills catalog
- [geminicli.com/docs/cli/skills/](https://geminicli.com/docs/cli/skills/), [/docs/extensions/](https://geminicli.com/docs/extensions/), [/docs/cli/tutorials/mcp-setup/](https://geminicli.com/docs/cli/tutorials/mcp-setup/)
- [google-gemini/gemini-cli docs/hooks/reference.md](https://github.com/google-gemini/gemini-cli/blob/v0.39.1/docs/hooks/reference.md)
- [block.github.io/goose/docs/guides/recipes/recipe-reference/](https://block.github.io/goose/docs/guides/recipes/recipe-reference/)
- [forgecode.dev](https://forgecode.dev), [forgecode.dev/docs/permissions/](https://forgecode.dev/docs/permissions/), [forgecode.dev/docs/skills/](https://forgecode.dev/docs/skills/)
- [docs.windsurf.com/windsurf/cascade/agents-md](https://docs.windsurf.com/windsurf/cascade/agents-md)
- [docs.roocode.com/features/custom-instructions](https://docs.roocode.com/features/custom-instructions)
- [kilo.ai/docs/customize/agents-md](https://kilo.ai/docs/customize/agents-md)
- [docs.factory.ai/cli/configuration/agents-md](https://docs.factory.ai/cli/configuration/agents-md)
- [docs.gitlab.com/user/duo_agent_platform/customize/agents_md/](https://docs.gitlab.com/user/duo_agent_platform/customize/agents_md/)
- [cursor.com/docs/rules](https://cursor.com/docs/rules)
- [aider.chat/docs/config/aider_conf.html](https://aider.chat/docs/config/aider_conf.html)
- [nextjs.org/docs/app/guides/ai-agents](https://nextjs.org/docs/app/guides/ai-agents) (2026-04-23)
- [github.blog: How to write a great agents.md (2025-11-19, 2,500-repo analysis)](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [zed.dev/acp](https://zed.dev/acp) and [agentclientprotocol.com](https://agentclientprotocol.com) — ACP
- [github.com/agentclientprotocol/agent-client-protocol](https://github.com/agentclientprotocol/agent-client-protocol) (v0.12.2, 2026-04-23)
- [continuedev/rules](https://github.com/continuedev/rules) — Go translator across formats
- [github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — ECC
- [github.com/github/spec-kit](https://github.com/github/spec-kit) — registry-of-integrations
- [github.com/Goldziher/ai-rulez](https://github.com/Goldziher/ai-rulez) — single YAML compiled per agent

### PRACTITIONER — community blogs, [PRAC]-tagged claims

- [Augment Code: How to Build AGENTS.md (2026-03-31)](https://www.augmentcode.com/guides/how-to-build-agents-md) — ETH study cite
- [DeployHQ: CLAUDE.md, AGENTS.md & Copilot Instructions guide](https://www.deployhq.com/blog/ai-coding-config-files-guide)
- [Hivetrail: AGENTS.md vs CLAUDE.md](https://hivetrail.com/blog/agents-md-vs-claude-md-cross-tool-standard)
- [aiengineerguide: How to use AGENTS.md in Claude Code (2025-10-27)](https://aiengineerguide.com/til/how-to-use-agents-md-in-claude-code/)
- [DeepWiki: AGENTS.md Format Documentation](https://deepwiki.com/openai/agents.md/5-agents.md-format-documentation)
- [Simon Willison: OpenAI are quietly adopting skills (2025-12-12)](https://simonwillison.net/2025/Dec/12/openai-skills/)
- [Tembo: 2026 Coding CLI Tools Comparison](https://www.tembo.io/blog/coding-cli-tools-comparison)
- [Antigravity AGENTS.md guide](https://antigravity.codes/blog/antigravity-agents-md-guide)
- [Datadog Frontend Dev: Steering AI Agents in Monorepos](https://dev.to/datadog-frontend-dev/steering-ai-agents-in-monorepos-with-agentsmd-13g0)
- [Tanaike: Building Gemini CLI Extensions](https://gist.github.com/tanaikech/0a1426535ab3af0c68cf8d79bca770a0)
- [devalias gist: AI Agent Rule/Instruction file notes](https://gist.github.com/0xdevalias/f40bc5a6f84c4c5ad862e314894b2fa6)
- [unite.ai: Anthropic Opens Agent Skills Standard](https://www.unite.ai/anthropic-opens-agent-skills-standard-continuing-its-pattern-of-building-industry-infrastructure/)

### DISCOUNTED — claims not used in this synthesis

The following sources or specific claims appeared in the corpus but are not relied on. They are listed so future readers can recognize them.

- **`raw/gemini-deep-research-output.md` (entire file)** — fabricated frameworks (Orchestral AI, Gradientsys, HEPTAPOD, DAOTreasury, OpenCode Go, "Cyber Verification Program", "managed-agents-2026-04-01"), invented file paths (BMAD `src/installer/install.ts` TypeScript; verified as JavaScript at `tools/installer/bmad-cli.js`), uncited statistics ("GPT-5.4 78.4%/81.8% TermBench", "Opus 4.7 visual acuity 54.5% → 98.5%", "$5/$25 per Mtok", "58s → 31s Codex benchmark", "tenfold success-rate increase, 26% gain on terminal operations"), >50% off-scope content (NIST, OWASP, DAOTreasury, theoretical Cline-vs-Aider debate). Used only for tonal context, not specifics.
- **GitHub star counts** — discounted per project policy (`feedback_github_stars_unreliable.md`); ECC "167,488 stars" claim flagged as implausible for a 3-month-old repo (would put it in GitHub's top 30); OpenCode "36K stars" verified to be 4× too low (actual 150,109); use commits, contributor distribution, and downloads instead.
- **"Anthropic 2026 Agentic Coding Trends Report"** — cited in Gemini file with no URL or publication date; appears hallucinated.
- **`geminicli.com` `[OFFICIAL]` tagging** — third-party domain, not Google's; downgraded.
- **`github.github.com/spec-kit/installation.html`** — likely fabricated URL; valid spec-kit installation docs are at `github.com/github/spec-kit`.
- **Goose cross-tool reads of `.codex/skills/` and `.cursor/skills/`** — Wave 1 claim; verification proves false (Goose reads only `.goose/skills`, `.claude/skills`, `.agents/skills`).
- **OpenCode skills 404 status** — Wave 1 [UNVERIFIED]; verification proves the docs page returns 200 and SKILL.md support is fully implemented.

---

*End of report. Length: ~10,400 words. Authored 2026-04-26 by claude-code-synthesis based on the Wave 1 + Wave 2 corpus produced for the Momentum multi-agent deployment refactor decision.*
