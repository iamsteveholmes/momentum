# Claude Code Skills Testing, Validation, and Plugin Migration Research

**Date:** 2026-03-16
**Status:** Complete
**Focus:** Testing/validation frameworks, pre-commit hooks, plugin migration, plugin dev workflow, update management

---

## 1. Testing and Validating Claude Code Skills Before Deployment

### 1.1 The Dual Eval Problem

Skills require validation on two independent axes:

- **Output quality** -- Does the skill produce correct results when invoked?
- **Trigger precision** -- Does Claude actually activate the skill when it should (and avoid activating it when it should not)?

A skill can pass quality evals while failing trigger evals (great output, never invoked) or vice versa. Both must be tested independently.

Source: [Claude Code: How to Write, Eval, and Iterate on a Skill](https://www.mager.co/blog/2026-03-08-claude-code-eval-loop/)

### 1.2 Quality Evaluation with promptfoo

**promptfoo** is the primary open-source tool used for output quality testing. The workflow:

1. Create a `promptfooconfig.yaml` with test cases
2. Build a `prompt.cjs` loader that injects SKILL.md as system context
3. Define assertions using LLM-rubric evaluations

```yaml
# promptfooconfig.yaml example
tests:
  - description: "Gives opinionated button design advice"
    vars:
      message: "How should I style my primary CTA button?"
    assert:
      - type: llm-rubric
        value: "Gives specific, opinionated CSS or design direction..."
```

Commands:
- `npx promptfoo@latest eval` -- run the eval suite
- `npx promptfoo@latest view` -- view results in browser

Recommended minimum: 8+ test cases per skill.

Source: [Claude Code: How to Write, Eval, and Iterate on a Skill](https://www.mager.co/blog/2026-03-08-claude-code-eval-loop/)

### 1.3 Trigger Evaluation with Anthropic's run_eval.py

Anthropic's `skill-creator` plugin ships a Python eval system (`run_eval.py`) that tests whether Claude correctly routes prompts to your skill.

```bash
python run_eval.py \
  --eval-set /path/to/agents/eval-set.json \
  --skill-path /path/to/skills/my-skill \
  --runs-per-query 3 \
  --verbose
```

The eval-set format:
```json
{
  "query": "Design a card component for a music app",
  "should_trigger": true,
  "note": "core use case - UI component design"
}
```

The script measures trigger rate: what percentage of queries correctly activate (or correctly avoid) the skill across multiple runs.

Source: [Claude Code: How to Write, Eval, and Iterate on a Skill](https://www.mager.co/blog/2026-03-08-claude-code-eval-loop/)

### 1.4 Automated Description Optimization with run_loop.py

The `run_loop.py` tool iteratively improves skill descriptions using an LLM:

```bash
python run_loop.py \
  --eval-set agents/eval-set.json \
  --skill-path ./skills/my-skill \
  --max-iterations 5 \
  --holdout 0.4 \
  --model claude-opus-4-5
```

Key features:
- **Holdout validation** (`--holdout 0.4`): splits the eval set 60% training / 40% testing to prevent overfitting
- **LLM-driven improvement**: Claude analyzes failures and generalizes the description
- Reports iteration results with train/test scores

Source: [Claude Code: How to Write, Eval, and Iterate on a Skill](https://www.mager.co/blog/2026-03-08-claude-code-eval-loop/)

### 1.5 Anthropic's skill-creator Eval System (Skills 2.0)

As of March 3, 2026, Anthropic's `skill-creator` plugin includes built-in evaluation capabilities:

- **Benchmark mode**: Runs standardized assessments tracking eval pass rate, elapsed time, and token usage
- **Multi-agent support**: Independent agents execute tests in parallel with clean context, eliminating cross-contamination between runs
- **A/B comparisons**: Comparator agents judge outputs blindly, comparing two skill versions or skill-vs-baseline
- **Regression detection**: Running evals against new models gives early signal when behavior shifts
- **Trigger optimization**: Analyzes skill descriptions against sample prompts and suggests edits to reduce false positives and false negatives

Source: [Improving skill-creator: Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)

### 1.6 Recommended Eval Directory Structure

```
plugins/my-skill/
├── agents/eval-set.json          # Trigger eval cases
├── skills/my-skill/SKILL.md      # The skill itself
├── prompt.cjs                     # promptfoo loader
├── promptfooconfig.yaml           # Quality eval config
└── EVALUATION.md                  # Eval documentation
```

Both quality and trigger evals can serve as CI/CD gates before shipping.

Source: [Claude Code: How to Write, Eval, and Iterate on a Skill](https://www.mager.co/blog/2026-03-08-claude-code-eval-loop/)

### 1.7 Community Validation Approaches

The `claude-code-skills` collection (125+ skills) includes built-in validation:
- **Multi-Agent Validator**: 20 criteria across 8 groups with penalty-point scoring
- **Story Validator Hook**: Validates specifications before execution
- **Multi-Model Review**: Parallel validation through Claude, Codex, and Gemini with automatic fallback

Source: [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills)

---

## 2. Pre-Commit Hooks for Claude Code Configuration Validation

### 2.1 freddo1503/claude-pre-commit

A Rust-based CLI tool that validates Claude Code configuration files before they reach version control.

**What it validates:**
- SKILL.md files (YAML frontmatter + markdown structure)
- JSON configuration files: `settings.json`, `hooks.json`, `.mcp.json`
- Shell scripts (security analysis)

**CLI commands:**
- `claude-check check` -- validate all Claude Code files
- `claude-check check --scope global` -- validate global scope only
- `claude-check check --scope local` -- validate local/project scope only
- `claude-check fix` -- auto-fix common issues
- `claude-check install-hook` -- install git pre-commit hook

**Pre-commit framework integration:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/freddo1503/claude-pre-commit
    rev: v0.1.0
    hooks:
      - id: claude-check
```

**Installation (from source):**
```bash
git clone https://github.com/freddo1503/claude-pre-commit
cd claude-pre-commit
cargo build --release
```

**Current status:** v0.1.0 (experimental). Core validation engine and file discovery are complete. SKILL.md validation, JSON schema validation, and shell script security analysis are listed as in-progress features.

Source: [freddo1503/claude-pre-commit](https://github.com/freddo1503/claude-pre-commit)

### 2.2 Other Pre-Commit Approaches

- **pre-commit-skill** by julianobarbosa: A Claude Code skill itself that manages pre-commit hooks. Source: [playbooks.com/skills/julianobarbosa/claude-code-skills/pre-commit-skill](https://playbooks.com/skills/julianobarbosa/claude-code-skills/pre-commit-skill)
- **hooks-automation** by openclaw: Automates hook setup workflows. Source: [playbooks.com/skills/openclaw/skills/hooks-automation](https://playbooks.com/skills/openclaw/skills/hooks-automation)
- **Pre-commit Quality Gate** (Claudeable): Comprehensive pre-commit validation hook as a Claude Code hook (not a git hook). Source: [claudeable.co/hooks/pre-commit-quality-hook](https://claudeable.co/hooks/pre-commit-quality-hook)

### 2.3 Native Claude Code Validation

Claude Code provides built-in validation for plugin manifests:
- `claude plugin validate` (CLI) or `/plugin validate` (TUI) -- validates `plugin.json` syntax and structure
- `claude --debug` -- shows plugin loading details, manifest errors, and component registration

Source: [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)

---

## 3. Migrating from Manual .claude/ Setup to Plugin-Based Distribution

### 3.1 When to Migrate

| Use standalone `.claude/` | Use plugins |
|---|---|
| Personal workflows | Sharing with teammates |
| Project-specific customizations | Distributing to community |
| Quick experiments | Versioned releases |
| Short skill names (`/hello`) | Reusable across projects |

Anthropic's guidance: "Start with standalone configuration in `.claude/` for quick iteration, then convert to a plugin when you're ready to share."

Source: [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)

### 3.2 Migration Steps

**Step 1: Create plugin structure**
```bash
mkdir -p my-plugin/.claude-plugin
```

Create `my-plugin/.claude-plugin/plugin.json`:
```json
{
  "name": "my-plugin",
  "description": "Migrated from standalone configuration",
  "version": "1.0.0"
}
```

**Step 2: Copy existing files**
```bash
cp -r .claude/commands my-plugin/
cp -r .claude/agents my-plugin/
cp -r .claude/skills my-plugin/
```

**Step 3: Migrate hooks**
```bash
mkdir my-plugin/hooks
```
Copy the `hooks` object from `settings.json` or `settings.local.json` into `my-plugin/hooks/hooks.json`. The format is identical.

**Step 4: Test**
```bash
claude --plugin-dir ./my-plugin
```

Source: [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)

### 3.3 What Changes After Migration

| Standalone (`.claude/`) | Plugin |
|---|---|
| Available in one project only | Shared via marketplaces |
| Files in `.claude/commands/` | Files in `plugin-name/commands/` |
| Hooks in `settings.json` | Hooks in `hooks/hooks.json` |
| Must manually copy to share | Install with `/plugin install` |
| Short names: `/deploy` | Namespaced: `/my-plugin:deploy` |

**Important:** After migrating, remove the original files from `.claude/` to avoid duplicates. The plugin version takes precedence when loaded.

### 3.4 Structural Warnings

- **Never** put `commands/`, `agents/`, `skills/`, or `hooks/` inside `.claude-plugin/`. Only `plugin.json` goes there.
- All paths in manifest must be relative and start with `./`
- Custom paths supplement default directories; they do not replace them.
- Plugins cached at `~/.claude/plugins/cache` cannot reference files outside their directory (path traversal blocked). Use symlinks if needed.

Source: [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)

---

## 4. Plugin Development Workflow -- Local Development and Iteration

### 4.1 The --plugin-dir Flag

The primary local development mechanism. Loads a plugin directly without installation:

```bash
claude --plugin-dir ./my-plugin
```

Key behaviors:
- When a `--plugin-dir` plugin has the same name as an installed marketplace plugin, the local copy takes precedence (except for managed-settings force-enabled plugins)
- Multiple plugins can be loaded simultaneously:
  ```bash
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```

Source: [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)

### 4.2 Hot Reload During Development

**`/reload-plugins`** picks up changes to skills, agents, commands, and hooks without restarting Claude Code.

Exception: Changes to LSP server configuration require a full restart.

Source: [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)

### 4.3 Testing Checklist

When testing a plugin locally:
1. Try skills with `/plugin-name:skill-name`
2. Check that agents appear in `/agents`
3. Verify hooks trigger on expected events
4. Use `claude --debug` to see loading details and errors
5. Use `claude plugin validate` or `/plugin validate` to check manifest

Source: [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)

### 4.4 Debugging

`claude --debug` (or `/debug` within TUI) shows:
- Which plugins are being loaded
- Errors in plugin manifests
- Command, agent, and hook registration
- MCP server initialization

Common issues and fixes:

| Issue | Cause | Fix |
|---|---|---|
| Plugin not loading | Invalid `plugin.json` | `claude plugin validate` |
| Commands not appearing | Wrong directory structure | Ensure `commands/` at root |
| Hooks not firing | Script not executable | `chmod +x script.sh` |
| MCP server fails | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for all plugin paths |
| Path errors | Absolute paths used | Use relative paths starting with `./` |

Source: [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)

### 4.5 Distribution Path

1. Develop locally with `--plugin-dir`
2. Validate with `claude plugin validate`
3. Add `README.md`, `CHANGELOG.md`, `LICENSE`
4. Version with semantic versioning in `plugin.json`
5. Create/use a marketplace for distribution (see plugin marketplaces docs)
6. Submit to the official Anthropic marketplace via:
   - [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
   - [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

Source: [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)

---

## 5. Plugin Update and Version Management

### 5.1 How Versioning Works

Plugins follow semantic versioning (`MAJOR.MINOR.PATCH`):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

The version is set in `.claude-plugin/plugin.json`. If also set in the marketplace entry, `plugin.json` takes priority.

**Critical:** Claude Code uses the version to determine whether to update a plugin. If you change code but do not bump the version, existing users will not see changes due to caching.

Source: [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)

### 5.2 How Updates Work

**Manual update command:**
```bash
claude plugin update <plugin-name>
claude plugin update <plugin-name>@<marketplace-name>
claude plugin update <plugin-name> --scope project
```

**What happens under the hood:** When you install a plugin, Claude Code records the git commit hash. The `plugin update` command pulls the latest source from the marketplace repo.

Source: [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)

### 5.3 Auto-Update Status

The auto-update story is still maturing:

- **Version 2.0.70** (reported March 2026): Introduced native auto-update functionality for plugin marketplaces. Per-marketplace automatic updates can be enabled directly in Claude Code.
- **Before 2.0.70:** No built-in update detection. Plugins were pinned to their install-time commit SHA with no notification of available updates.
- **`/plugin marketplace update`** refreshes the marketplace catalog (what is available to install), not the installed plugins themselves. This is a common source of confusion.

Source: [Keeping Claude Code plugins up to date](https://workingbruno.com/notes/keeping-claude-code-plugins-date)

### 5.4 The Update Detection Gap

Even with recent improvements, there are known gaps:
- No dashboard or notification showing "N updates available"
- The community has proposed a SessionStart hook that compares `installed_plugins.json` commit SHAs against remote HEAD, cached to run at most once per 24 hours

A reference implementation exists as a community-contributed skill (`upgrade-plugins/SKILL.md`) that handles update detection, changelog display, user confirmation, build steps, and `installed_plugins.json` refresh.

Source: [Plugin update detection and upgrade workflow - Issue #31462](https://github.com/anthropics/claude-code/issues/31462)

### 5.5 Workaround: External Update Checker

For teams that need reliable update visibility, a bash script that runs outside Claude Code can:
1. Fetch latest marketplace repos
2. Compare installed commit SHAs against current HEAD
3. Display available versions and commit distances
4. Avoid consuming Claude tokens for infrastructure tasks

Source: [Keeping Claude Code plugins up to date](https://workingbruno.com/notes/keeping-claude-code-plugins-date)

### 5.6 Plugin Installation Scopes and Their Impact on Updates

| Scope | Settings file | Update behavior |
|---|---|---|
| `user` | `~/.claude/settings.json` | Default. Updated per-user. |
| `project` | `.claude/settings.json` | Shared via VCS. Team-wide. |
| `local` | `.claude/settings.local.json` | gitignored. Project-specific. |
| `managed` | Managed settings | Read-only. Update only via managed settings. |

Source: [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)

---

## 6. Key Findings and Recommendations for Momentum

### 6.1 Testing Strategy

For Momentum's skill/workflow portfolio:
1. **Adopt the dual-eval pattern**: Quality evals (promptfoo) + trigger evals (run_eval.py) for every skill
2. **Use holdout validation** (60/40 split) to prevent overfitting skill descriptions
3. **Make evals CI/CD gates** before merging skill changes
4. **Consider claude-pre-commit** for structural validation of SKILL.md and config files, though it is currently experimental (v0.1.0)

### 6.2 Migration Path

Momentum's current `.claude/commands/` structure is forward-compatible:
- Existing `.claude/commands/*.md` files continue to work as-is
- Skills (`.claude/skills/`) are the recommended new format but commands are not deprecated
- Migration to plugins makes sense when distribution across projects is needed
- Namespacing change (`/deploy` becomes `/momentum:deploy`) is the primary breaking change

### 6.3 Plugin Development

- Use `--plugin-dir` for local iteration; `/reload-plugins` for hot reload
- Use `claude --debug` for diagnostics
- Use `claude plugin validate` before distribution
- Bump `plugin.json` version on every change or users will not see updates

### 6.4 Update Management Gaps

- Auto-update was introduced in v2.0.70 but the UX for update visibility remains limited
- For team use, consider an external update-checker script or SessionStart hook
- Pin versions via commit SHA for reproducibility; use `claude plugin update` for explicit upgrades

---

## Sources

- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)
- [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code: How to Write, Eval, and Iterate on a Skill (mager.co)](https://www.mager.co/blog/2026-03-08-claude-code-eval-loop/)
- [Improving skill-creator: Test, measure, and refine Agent Skills (Anthropic blog)](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
- [freddo1503/claude-pre-commit (GitHub)](https://github.com/freddo1503/claude-pre-commit)
- [Plugin update detection and upgrade workflow - Issue #31462 (GitHub)](https://github.com/anthropics/claude-code/issues/31462)
- [Keeping Claude Code plugins up to date (workingbruno.com)](https://workingbruno.com/notes/keeping-claude-code-plugins-date)
- [levnikolaevich/claude-code-skills (GitHub)](https://github.com/levnikolaevich/claude-code-skills)
- [Best Claude Code Skills in 2026 (OpenAIToolsHub)](https://www.openaitoolshub.org/en/blog/best-claude-code-skills-2026)
- [Claude Code March 2026 Updates (Releasebot)](https://releasebot.io/updates/anthropic/claude-code)
