---
content_origin: claude-code-subagent-verification
date: 2026-04-26
sub_question: "Goose Recipes deep-dive + does any framework compile workflows to Recipes (not just skills)?"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
verification_targets: ["Goose Recipe schema (full)", "Frameworks that emit Recipes vs Skills only", "Momentum→Recipe compilation feasibility"]
---

# Goose Recipes — Deep Verification

Pinned source SHAs:

- `block/goose` — `96fa25bce88613b0ed018612688d73328a912e8b` (HEAD `main`, 2026-04-28) [OFFICIAL-SOURCE]
- `github/spec-kit` — `171b65ac33a3bf51c23b9f7a5287032ed1ae72ba` (HEAD `main`, 2026-04-24) [OFFICIAL-SOURCE]
- `bmad-code-org/BMAD-METHOD` — `7ee5fa3` (HEAD `main`, install-time platform table) [OFFICIAL-SOURCE]

## 1. Goose Recipe Schema (Verbatim From Source)

The canonical Recipe type lives in `crates/goose/src/recipe/mod.rs:41-86` (block/goose @ `96fa25b`) [OFFICIAL-SOURCE]:

```rust
#[derive(Serialize, Deserialize, Debug, Clone, ToSchema)]
pub struct Recipe {
    #[serde(default = "default_version")]
    pub version: String,                            // file format semver
    pub title: String,                              // short title
    pub description: String,                        // longer description
    #[serde(skip_serializing_if = "Option::is_none")]
    pub instructions: Option<String>,               // model instructions
    #[serde(skip_serializing_if = "Option::is_none")]
    pub prompt: Option<String>,                     // session-start prompt
    #[serde(...)]
    pub extensions: Option<Vec<ExtensionConfig>>,   // MCP extensions
    #[serde(skip_serializing_if = "Option::is_none")]
    pub settings: Option<Settings>,                 // provider/model/temperature/max_turns
    #[serde(skip_serializing_if = "Option::is_none")]
    pub activities: Option<Vec<String>>,            // Desktop activity pills
    #[serde(skip_serializing_if = "Option::is_none")]
    pub author: Option<Author>,                     // contact + metadata
    #[serde(skip_serializing_if = "Option::is_none")]
    pub parameters: Option<Vec<RecipeParameter>>,   // typed parameters
    #[serde(skip_serializing_if = "Option::is_none")]
    pub response: Option<Response>,                 // structured-output JSON schema
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sub_recipes: Option<Vec<SubRecipe>>,        // delegated sub-workflows
    #[serde(skip_serializing_if = "Option::is_none")]
    pub retry: Option<RetryConfig>,
}
```

Required fields: `title`, `description`, plus at least one of `instructions` or `prompt` (enforced in `RecipeBuilder::build`, `mod.rs:409-415`). `version` defaults to `"1.0.0"`.

**`Settings`** (`mod.rs:97-110`): `goose_provider`, `goose_model`, `temperature` (`f32`), `max_turns` (`usize`) — all optional. Lets a recipe pin its own provider/model independent of the user's global config.

**`Response`** (`mod.rs:112-116`): a single optional `json_schema: serde_json::Value`. The agent is forced to emit JSON conforming to that schema as the final turn — validated via `jsonschema::validator_for` in `validate_recipe.rs:21-26`.

**`RecipeParameter`** (`mod.rs:196-206`):

```rust
pub struct RecipeParameter {
    pub key: String,
    pub input_type: RecipeParameterInputType, // String|Number|Boolean|Date|File|Select
    pub requirement: RecipeParameterRequirement, // Required|Optional|UserPrompt
    pub description: String,
    pub default: Option<String>,
    pub options: Option<Vec<String>>, // for Select
}
```

`File` parameters cannot have defaults — explicit comment at `mod.rs:181`: "File parameter that imports content from a file path. Cannot have default values to prevent importing sensitive user files." `UserPrompt` means "ask interactively at run time."

**`SubRecipe`** (`mod.rs:118-128`):

```rust
pub struct SubRecipe {
    pub name: String,                             // tool-name identifier
    pub path: String,                             // path to subrecipe yaml
    pub values: Option<HashMap<String, String>>,  // pinned param overrides
    pub sequential_when_repeated: bool,           // serialize multi-invocation
    pub description: Option<String>,
}
```

Two important auto-injection behaviors execute every time a recipe loads (`mod.rs:228-270`):

1. **`ensure_analyze_for_developer`** — if the recipe declares the legacy `developer` builtin extension but not `analyze`, the `analyze` platform extension is silently appended.
2. **`ensure_summon_for_subrecipes`** — if `sub_recipes` is non-empty, the `summon` platform extension is auto-injected. `summon` is the runtime that exposes each sub-recipe to the parent agent as a tool.

Recipe templates use **MiniJinja** (`crates/goose/src/recipe/template_recipe.rs:8-9`) — `{{ var }}` substitution with raw-fallback for unparseable expressions (`template_recipe.rs:67-90`). Parameters not declared in the recipe but referenced in templates are flagged by `validate_recipe.rs::validate_parameters_in_template`.

## 2. Where Recipes Live + How They're Invoked

Lookup order is implemented in `crates/goose/src/recipe/local_recipes.rs:21-46` [OFFICIAL-SOURCE]:

```
1. Current working directory (".")
2. $GOOSE_RECIPE_PATH (colon-separated on POSIX, semicolon on Windows)
3. ~/.config/goose/recipes/        (global, returned by Paths::config_dir())
4. ./.goose/recipes/                (project-local)
5. ./.agents/recipes/               (cross-tool convention)
6. ~/.agents/recipes/               (cross-tool global)
```

For a name like `code-review`, `load_recipe_file_from_dir` tries `code-review.yaml` then `code-review.json` in each directory (`local_recipes.rs:106-119`, `RECIPE_FILE_EXTENSIONS = &["yaml", "json"]` at `mod.rs:25`).

**GitHub remote registry**: when the config key `GOOSE_RECIPE_GITHUB_REPO` (e.g. `myorg/recipes`) is set, `crates/goose-cli/src/recipes/github_recipe.rs:34-67` shells out to `gh repo clone` into `$TMPDIR`, then `git archive origin/main:<recipe_name>` to extract the recipe folder. This is the closest thing Goose has to a public registry — there's no first-party hub.

**Invocation**:

- **CLI**: `goose run --recipe <name-or-path> --params key=value --params other=value [--sub-recipe extra-recipe.yaml]` (`crates/goose-cli/src/cli.rs:208-247`). `--explain` shows title/desc/params; `--render-recipe` prints the rendered YAML without running.
- **Recipe sub-command**: `goose recipe validate <name>`, `goose recipe deeplink <name> -p k=v`, `goose recipe open <name>` (Desktop), `goose recipe list` (`cli.rs:634-680`).
- **Schedule**: `goose schedule add --cron "<expr>" --recipe-source <path|base64>` runs a recipe on cron (`cli.rs:556-565`). Internally injects `--scheduled-job-id` so sessions are linked to the schedule.
- **Desktop deeplink**: a recipe + params encoded as a URL the Desktop client opens.
- **HTTP/ACP**: `block/goose` issue #7596 tracks first-class recipe support over the ACP server; today HTTP/server already accepts a recipe payload.

## 3. Sub-Recipes + Parameters Mechanics

Documented in `documentation/docs/guides/recipes/subrecipes.md` and implemented in `crates/goose/src/agents/platform_extensions/summon.rs` [OFFICIAL-SOURCE].

**Execution model** (`subrecipes.md:24-29`):

> When the main recipe is run, goose generates a tool for each subrecipe that:
> - Accepts parameters defined by the subrecipe
> - Executes the subrecipe in a separate session with its own context
> - Returns output to the main recipe
>
> Sub-recipe sessions run in isolation — they don't share conversation history, memory, or state with the main recipe or other subrecipes. Additionally, subrecipes cannot define their own subrecipes (no nesting allowed).

So `sub_recipes` are **one-level deep** by design — a parent fans out to children, children cannot fan out further. This is enforced implicitly: when `summon` loads a sub-recipe via `load_local_recipe_file` and reads its `sub_recipes` field for tool generation, the auto-injected child's own `summon` extension is unused because nothing is registered to delegate to.

**Parameter handling** (`subrecipes.md:31-38`):

1. `values` map on the parent's `SubRecipe` entry is locked — runtime cannot override (`summon.rs:583-606`, `add_subrecipes` builds the tool description from those pinned values).
2. Otherwise the parent agent extracts the params from conversation context and passes them as the tool call args.

The parent's `summon` platform extension exposes the tool list — sub-recipe descriptions are auto-built (`summon.rs:608-630`) by reading the child recipe's `description` and appending `(params: <param_names>)`. The agent picks the tool, fills parameters, and `summon` runs `run_subagent_task` (`summon.rs:3` import) to execute the child in a sandboxed session via the same MCP runtime.

**`sequential_when_repeated`** (`SubRecipe.sequential_when_repeated`): if the parent invokes the same sub-recipe multiple times (e.g. one per file), this flag forces serial execution. Default `false` = parallel. This is the only built-in concurrency primitive on Recipes.

**Templating power**: MiniJinja gives recipes Jinja2-class branching/looping inside `instructions`, `prompt`, `activities`. The bundled `code-review-mentor.yaml` (`documentation/src/pages/recipes/data/recipes/code-review-mentor.yaml`) shows `{% if review_scope == "staged" %}` and `{% if "performance" in focus_areas %}` blocks driving entirely different prompt sections — i.e. a recipe is a *parameterized program*, not just a saved prompt.

## 4. Frameworks That Emit Recipes (vs Skills Only)

I read the source of every framework the user named plus the most-cited cross-tool installers. Each row records what the framework writes when "installing for Goose."

| Framework | Goose target | What it writes | Source |
|---|---|---|---|
| **github/spec-kit** | `.goose/recipes/speckit.<name>.yaml` | **Recipe YAML** — flat (header + prompt body), no params/sub-recipes | `src/specify_cli/integrations/goose/__init__.py:6-21` + `integrations/base.py:1116-1293` (`YamlIntegration`) |
| **bmad-code-org/BMAD-METHOD** | `.agents/skills/` and `~/.config/agents/skills/` | **Skill files** (SKILL.md) — never Recipes | `tools/installer/ide/platform-codes.yaml:136-141` |
| **vercel-labs/skills** | `.goose/skills/` and `~/.config/goose/skills/` | **Skill files** (SKILL.md) | README "Supported Agents" table |
| **numman-ali/openskills** | (no Goose recipe path) | Skills only — installer is Anthropic-spec; no recipe code path exists | DeepWiki SKILL.md spec page; no recipe writer |
| **rohitg00/skillkit** | Goose listed as supported, target paths are skill dirs | Skills only — `translate` command doesn't enumerate a Recipe target | README + `skillkit.sh/docs/agents` |
| **dyoshikawa/rulesync** | Issue #1115: proposed `.goose/skills/<skill>/SKILL.md` (open) | Skills only when implemented; separate issue #1112 for `.goosehints` rules | github.com/dyoshikawa/rulesync/issues/1115 |
| **Goldziher/ai-rulez** | (no goose preset listed) | 18 platform presets, Goose is **not** among them | github.com/Goldziher/ai-rulez README |
| **continuedev/rules** | (no Goose target) | Continue config; not a Goose generator | repo README |
| **eyaltoledano/claude-task-master** | (no Goose target) | Cursor/Lovable/Windsurf/Roo MCP — not a Goose generator | repo README |
| **mpazaryna/goose-recipes** (Smithery) | n/a | A *Claude Skill* that **helps a developer hand-write Goose Recipes** — a writing assistant, not a compiler from another spec | smithery.ai/skills/mpazaryna/goose-recipes |
| **block/goose recipe-cookbook-generator** | n/a | A Goose recipe that scans **Goose's own session history** and produces recipes for repetitive workflows. Not third-party; not a workflow-spec compiler | block.github.io/goose/blog/2025/10/08/recipe-cookbook-generator/ |

### How spec-kit's recipe compilation actually works

`integrations/base.py:1116-1293` — the `YamlIntegration` class. For each Markdown command template (`templates/commands/<name>.md`), `setup()`:

1. Parses the template's YAML frontmatter to extract `description` and `title`.
2. Runs `process_template()` to substitute `{ARGS}` → `{{args}}`, `__AGENT__` → `goose`, `$ARGUMENTS` placeholders, etc.
3. Splits frontmatter from body.
4. Calls `_render_yaml(title, description, body, source_id)` (`base.py:1196-1226`):

```python
header = {
    "version": "1.0.0",
    "title": title,
    "description": description,
    "author": {"contact": "spec-kit"},
    "extensions": [{"type": "builtin", "name": "developer"}],
    "activities": ["Spec-Driven Development"],
}
header_yaml = yaml.safe_dump(header, sort_keys=False, allow_unicode=True, default_flow_style=False).strip()
indented = "\n".join(f"  {line}" for line in body.split("\n"))
lines = [header_yaml, "prompt: |", indented, "", f"# Source: {source_id}"]
return "\n".join(lines) + "\n"
```

5. Writes `.goose/recipes/speckit.<name>.yaml`.

**What's emitted is a degenerate Recipe**: `version`, `title`, `description`, `author`, hard-coded `extensions: [{type: builtin, name: developer}]`, `activities: ["Spec-Driven Development"]`, and a `prompt:` block scalar. **No `parameters`. No `sub_recipes`. No `settings`. No `response`. No `retry`.** Each spec-kit slash-command (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`) becomes a separate flat recipe — sibling files in `.goose/recipes/`, not a parent-with-children composition.

This is meaningful: spec-kit is a workflow framework with multi-phase orchestration (specify → plan → tasks → implement), and it has the explicit data to express that as a single parent recipe with four `sub_recipes` and shared `parameters` like `feature_name` and `branch`. It chooses not to. The Goose target is treated as just another "slash-command sink" — exactly the same content shape it ships to Claude Code, Codex, OpenCode. Recipes here is **YAML packaging, not workflow composition**.

### Conclusion for Part B

**No public framework currently compiles practice workflows to Goose Recipes that exploit `parameters`, `sub_recipes`, `settings`, or `response`.** spec-kit is the only framework that emits to `.goose/recipes/` at all, and its output is a flat trivial recipe per command. Every other framework targets `.goose/skills/` or `.agents/skills/`. The only Goose-native generator that emits structured recipes (cookbook-generator) bootstraps from Goose session history, not from a third-party workflow spec.

## 5. Custom Distros Explained

`documentation/docs/guides/custom-distributions.md` defines them; the long-form spec is in `CUSTOM_DISTROS.md` at the repo root (830 lines) [OFFICIAL-DOCS]. A "Custom Distro" is **a fork of `block/goose` with org-specific defaults** — preconfigured providers, bundled MCP extensions, custom branding, optional alternate UI. From the docs:

> goose is designed to be forked and customized. You can create your own "distro" of goose preconfigured with specific providers, bundled extensions, custom branding, and tailored workflows for your organization or audience.

The `CUSTOM_DISTROS.md` table classifies "Create guided workflows" as **low complexity → Recipes (YAML-based task definitions)** and "Build complex multi-step workflows" as medium → "Recipes with sub-recipes and subagents." Section H ("Preconfigured Workflows with Recipes") explicitly recommends three distribution patterns:

1. Bundle recipes inside a forked Desktop app.
2. Share via URL — users import via the deeplink mechanism.
3. Create a recipe library — a directory of recipes for different use cases.

Section I ("Complex Workflows with Sub-Recipes and Subagents") confirms sub-recipes are *the* recommended primitive for multi-step org workflows in Custom Distros.

Custom Distros are **not a registry** — they're a fork-with-defaults model. There is no first-party "Goose Marketplace" for recipes. The closest thing is `GOOSE_RECIPE_GITHUB_REPO` pointing at an org-owned GitHub repo holding `<name>/recipe.yaml` directories.

## 6. Capability Gap — What a Great Recipe-Emitting Framework Would Look Like

Today every cross-tool installer treats Goose as "another skills sink." The **richer surface** Recipes expose (declared parameters with types/validation, structured `response` JSON schemas, sub-recipe composition, per-recipe `settings`, retry logic, MiniJinja templating) is unused by every third-party generator I read. A great Recipe-emitting framework would:

1. **Compile workflow steps as a parent + children** — not a flat command list. A spec-kit-style "specify → plan → tasks → implement" sequence compiles to one parent recipe with four `sub_recipes` and `sequential_when_repeated: true`.
2. **Lift workflow inputs to typed `parameters`** — feature names, paths, branches, modes become declared `RecipeParameter` entries with `input_type` and `requirement`, not Markdown placeholders.
3. **Materialize structured outputs as `response.json_schema`** — when a workflow phase produces a known artifact (e.g., a Story JSON, a Decision Document), the recipe `response` schema enforces it, giving downstream code a parseable contract.
4. **Pin model/provider in `settings`** — workflow phases that need cheap fast models vs. deep reasoning models can pin `goose_model` per recipe, reflecting model-routing decisions baked into the framework.
5. **Use `extensions` deliberately** — declare exactly the MCP servers each recipe needs, not a default `developer` builtin for everything.
6. **Emit a Custom-Distro-ready folder** — drop a complete `recipes/` tree the org can clone or `GOOSE_RECIPE_GITHUB_REPO` against.

A framework that compiled to Recipes properly **and** to Claude Code skills/plugins **and** to Codex `AGENTS.md` directives **and** to OpenCode commands would be the first to fully cover the four primary harnesses with each one's native primitive. Today, even spec-kit — the closest to this ideal — falls back to "lowest common denominator: each command becomes a flat slash command in every harness."

## 7. Momentum → Recipe Sketch

Direct schema mapping from Momentum primitives to Goose Recipe primitives:

| Momentum primitive | Goose Recipe primitive | Notes |
|---|---|---|
| Skill (`SKILL.md`) | `Recipe` (one `recipe.yaml`) | Frontmatter `description` → `description`. Body → `instructions`. |
| Workflow ("specify → plan → execute") | Parent `Recipe` with `sub_recipes: [...]` | Each phase becomes a `SubRecipe { name, path, values }`. `sequential_when_repeated: true` for ordered phases. |
| Sub-skill spawn (`spawn impetus:create-story`) | `SubRecipe` entry | Parent agent invokes child as a tool. Child runs in isolated session. |
| Skill parameter (e.g. `epic_slug`, `story_id`) | `RecipeParameter` | Map Markdown `<input>` placeholders to `key/input_type/requirement/default/description`. `epic_slug` → `String/Required`. `mode` enum → `Select` with `options`. |
| Multi-step orchestration (sprint-planning Phase 1 → 2 → 3) | Parent recipe `instructions` field references child sub-recipes by name; agent calls them in sequence | The orchestrator prompt enumerates the phases as tool calls. |
| Decision/Assessment artifacts | `response.json_schema` on the recipe that produces them | Forces the final turn to validate against a schema (story.json, decision-document.json). |
| Architecture Guard, AVFL — heavy validation phases | `SubRecipe` per validator + `sequential_when_repeated: false` for parallel lenses | AVFL's "Structural / Accuracy / Coherence" lenses become three parallel sub-recipes. |
| Per-skill model routing | `Settings { goose_model, goose_provider, temperature, max_turns }` | A "deep reasoning" subagent pins Opus/Sonnet; a fast classifier pins Haiku. |
| Hooks (`PostToolUse`, `Stop`) | **Not supported** — no equivalent in Goose | Workaround: encode hook behavior as a final tool call inside the recipe's `instructions`, or as a separate scheduled recipe via `goose schedule add --cron`. The dev does not get true post-tool interception. |
| Rules (`~/.claude/rules/`) | **No equivalent** — Goose has no global cross-recipe rules | Workaround: ship rules as a file in `.goose/recipes/_rules.md` and have every recipe's `instructions` start with "Read .goose/recipes/_rules.md before proceeding." Or duplicate inline. |
| Plugin marketplace versioning (`/plugin marketplace update momentum`) | `GOOSE_RECIPE_GITHUB_REPO` org repo | Closest analogue. Updating means `cd $TMPDIR/<repo> && git pull` — handled implicitly by `fetch_origin` in `github_recipe.rs:169`. |

**A concrete worked sketch — `momentum:sprint-planning` as a Recipe**:

```yaml
version: "1.0.0"
title: "Momentum Sprint Planning"
description: "Story selection, team composition, Gherkin specs, and sprint activation"
author:
  contact: "momentum"
parameters:
  - key: epic_slug
    input_type: string
    requirement: required
    description: "Slug of the epic to plan a sprint for"
  - key: sprint_size
    input_type: select
    requirement: optional
    default: "medium"
    options: ["small", "medium", "large"]
    description: "Approximate sprint size"
settings:
  goose_model: claude-opus-4-7
  max_turns: 80
extensions:
  - type: builtin
    name: developer
sub_recipes:
  - name: select_stories
    path: ./momentum/sub/select-stories.yaml
    sequential_when_repeated: true
    description: "Walk stories/index.json, return ordered story_ids"
  - name: compose_team
    path: ./momentum/sub/compose-team.yaml
    sequential_when_repeated: true
  - name: write_gherkin
    path: ./momentum/sub/write-gherkin.yaml
    sequential_when_repeated: false   # parallelize per-story
  - name: avfl_validate
    path: ./momentum/sub/avfl-validate.yaml
    sequential_when_repeated: false
  - name: activate_sprint
    path: ./momentum/sub/activate-sprint.yaml
    sequential_when_repeated: true
response:
  json_schema:
    type: object
    required: [sprint_id, stories]
    properties:
      sprint_id: { type: string }
      stories:
        type: array
        items:
          type: object
          required: [story_id, status]
          properties:
            story_id: { type: string }
            status: { enum: [planned, blocked, deferred] }
prompt: |
  Plan a sprint for epic {{ epic_slug }} of size {{ sprint_size }}.
  Phase 1: invoke select_stories. Phase 2: compose_team. Phase 3: parallel write_gherkin per story. Phase 4: parallel avfl_validate per story. Phase 5: activate_sprint.
  Return JSON conforming to the response schema.
```

That recipe makes Goose drive Momentum sprint-planning natively — typed inputs, parallel sub-agent work, structured output. None of the existing Goose-targeting frameworks emit anything like this; they all emit a single flat recipe per skill/command.

## 8. Conclusion — Is Full-Coverage Multi-Harness Compilation an Open Opportunity?

**Yes, decisively.** Of the frameworks audited:

- **Targets Claude Code skills/plugins**: BMAD, vercel-labs/skills, openskills, skillkit, ai-rulez, rulesync, spec-kit — all yes.
- **Targets Codex (`AGENTS.md` / skills)**: BMAD, openskills, skillkit, ai-rulez, spec-kit — yes.
- **Targets OpenCode**: BMAD (yes), spec-kit (yes), several others.
- **Targets Goose Recipes (not just skills)**: **Only spec-kit**, and only as flat single-prompt recipes that don't use `parameters`, `sub_recipes`, `response`, or `settings`.

There is currently **zero overlap** between "framework with rich workflow primitives (multi-phase orchestration, typed parameters, structured outputs)" and "framework that compiles those primitives to Goose Recipes faithfully." Every cross-tool installer treats Goose as another file-drop target for SKILL.md, completely ignoring that Goose ships a richer container.

Momentum is uniquely positioned to be that framework. Its design — `momentum:impetus` orchestrating sub-skills, every skill having declared parameters, AVFL producing structured findings, sprint-planning being a multi-phase pipeline — maps almost line-for-line onto Recipe + sub_recipes + parameters + response. A Momentum-to-Recipe compiler would expose Momentum's full workflow shape natively to Goose users in a way no other framework currently does for any harness pair.

**Caveats / open questions to surface to the developer:**

- **Goose has no hook system.** PostToolUse / Stop hooks Momentum relies on (`scheduled_tasks.lock`, autosave/commit checkpoints) cannot be ported. Either degrade gracefully (no hooks on Goose) or move the hook behavior into recipes themselves as final tool calls / cron schedules.
- **Goose subrecipes don't nest** — Momentum's deep skill graphs (impetus → sprint-planning → create-story → avfl) collapse to one level. A compiler would need to flatten or split Momentum's skill tree into a fan of one-level-deep Recipes per workflow.
- **No global rules equivalent.** Either inline rules into every recipe's `instructions` header or rely on Goose's `goosehints` (project-scoped) — neither is as clean as Claude Code's `~/.claude/rules/` precedence.
- **No marketplace-equivalent** — distribution is via `GOOSE_RECIPE_GITHUB_REPO` or fork-with-bundle (Custom Distros). Versioning is whatever git gives you. Plan for `git tag`-driven release semantics, not a hub.
- **`response.json_schema` is enforced on the model only on the final turn** — not a full validation pipeline. AVFL-style multi-lens validation has to run as siblings/parallel sub-recipes that emit findings, then a coordinator sub-recipe rolls them up into the final-turn structured response.

The answer to "has anyone shipped great Goose Recipe coverage as part of Claude Code + Codex + OpenCode + Goose multi-harness deployment?" is **no**. The opportunity is real, validated by source-level reading of every plausible competitor, and Momentum's primitives map cleanly onto the Recipe primitives that no one else is exploiting.
