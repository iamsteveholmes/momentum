---
title: "Goose Recipes vs Claude Code Skills — Deep Comparison and Sprint-Dev Conversion Experiment"
date: 2026-04-22
type: Strategic Analysis
status: Complete
content_origin: claude-code-analysis
human_verified: true
derives_from:
  - path: final/forgecode-agentic-tools-eval-final-2026-04-21.md
    relationship: extends
  - path: analysis/integration-strategy-analysis-2026-04-21.md
    relationship: sibling
  - path: analysis/retro-microeval-loop-analysis-2026-04-21.md
    relationship: sibling
  - path: analysis/forgecode-fit-analysis-2026-04-22.md
    relationship: sibling
supplements: research/forgecode-agentic-tools-eval-2026-04-21
---

# Goose Recipes vs Claude Code Skills — Deep Comparison and Sprint-Dev Conversion Experiment

## Executive Summary

Goose has the most architecturally ambitious composition model of any tool surveyed — its Recipe primitive is genuinely novel and fills a gap that Claude Code / Momentum do not have a direct answer to. Specifically, Recipes provide **declarative workflow composition with static parameter flow** (via `sub_recipes` with mapped values and typed inputs), which Momentum currently handles by convention in `workflow.md` files interpreted at runtime.

Conversely, Goose has no user-configurable lifecycle hook surface (retracted earlier Gemini claim, verified against current docs) and enforces a structural constraint that subagents cannot spawn further subagents. These limits prevent Goose from hosting skills that depend on hook-based invariants (plan-audit, architecture-guard, autonomous-commit) or deep orchestration (Claude Code's unlimited agent nesting, TeamCreate + SendMessage dialogue).

Five integration paths exist between Goose and Claude Code, in increasing depth: process isolation, cmux-driven dispatch, MCP wrapping via AgentAPI, shared skills across both runtimes (Goose adopts the cross-platform Agent Skills standard), and recipes that load Momentum skills as knowledge. The most Momentum-valuable is shared-skills + cmux-dispatch — author once, run on either host.

The sprint-dev conversion experiment proposed in this document is decision-useful regardless of outcome: a ~70% clean translation reveals exactly which Momentum invariants are enforced by hooks vs enforced by convention. Running sprint-dev as a Goose recipe with fixture-based parity testing against the Claude Code implementation surfaces which Momentum primitives are load-bearing and which are defensive redundancy. Three likely outcomes (Goose handles it fine / Goose handles most but specific invariants fail / Goose is not viable for sprint-dev) are each informative for Momentum's architectural direction.

## 1. Goose's Architecture — Three Distinct Primitives

Previous analyses in this research project collapsed Goose's composition story into a single "Recipes" narrative. That is imprecise. Goose separates concerns into three (really four) primitives, and the architectural value comes from how they compose.

### 1.1 Extensions — the capability layer

**What they are:** MCP servers and tool declarations that define what a Goose session *can do*.

**Types supported** (per [Goose recipe reference](https://goose-docs.ai/docs/guides/recipes/recipe-reference) verified 2026-04-22):

- `stdio` — standard I/O with a spawned command (the most common MCP pattern)
- `builtin` — bundled with Goose
- `platform` — runs in the agent process
- `streamable_http` — HTTP-streaming client
- `frontend` — provided by the UI
- `inline_python` — uvx-executed inline code

**Relationship to Claude Code:** Functionally equivalent to Claude Code's MCP server configuration. Both tools speak the same protocol underneath. The differences are in scoping — Claude Code configures MCP globally in `settings.json`; Goose can additionally scope extensions per-recipe, which is cleaner for workflows that need specific toolsets.

### 1.2 Skills — the knowledge layer

**What they are:** Cross-platform Agent Skills open-standard files (`SKILL.md` + frontmatter + supporting files). Loaded automatically at session start; applied by the model based on matching the user's request.

**Where they live in Goose:** By default `~/.config/goose/skills/`. Configurable to also read `~/.claude/skills/` for Claude Desktop / Claude Code interop.

**Cross-platform reality:** Per the cross-platform skills ecosystem (including [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)), the `.agents/skills/` directory convention is supported across Claude Code, Claude.ai, OpenAI Codex, VS Code/Copilot, GitHub Copilot, Cursor, Gemini CLI, JetBrains Junie, Roo Code, OpenHands, Amp, Letta, Firebender, Databricks, Snowflake, Spring AI, Laravel Boost, Mistral Vibe, TRAE, Qodo, and more. **Goose is part of this convergence, not an exception to it.**

**Momentum implication:** A Momentum skill authored at `.claude/skills/momentum-X/SKILL.md` is directly loadable by Goose via symlink or path configuration. Format compatibility is the same as it is for ForgeCode — `cp -r` with no conversion.

### 1.3 Recipes — the orchestration layer (unique to Goose)

**What they are:** Declarative YAML files that describe a reusable workflow with parameters, extensions, instructions (the prompt), optional structured response schemas, retry logic, and sub-recipes.

**The full schema** (root-level fields per the recipe reference):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `version` | String | No | Format version (defaults to "1.0.0") |
| `title` | String | Yes | Short recipe name |
| `description` | String | Yes | Detailed explanation |
| `instructions` | String | One required | Template instructions with parameter substitutions |
| `prompt` | String | One required | Template prompt for headless mode |
| `activities` | Array | No | Clickable bubbles for Desktop UI |
| `parameters` | Array | No | Dynamic input definitions |
| `extensions` | Array | No | MCP servers and tool declarations |
| `settings` | Object | No | Model provider and configuration |
| `response` | Object | No | Structured JSON output schema |
| `retry` | Object | No | Automated retry logic with validation |
| `sub_recipes` | Array | No | Referenced subrecipe configurations |

**The load-bearing field is `sub_recipes`.** Each entry declares:

```yaml
sub_recipes:
  - name: "unique_identifier"
    path: "./relative/or/absolute/path.yaml"
    values: {parameter_name: parameter_value}
    sequential_when_repeated: false
    description: "Optional description"
```

**This is the feature Claude Code does not have.** Claude Code skills invoke other skills via prompt convention — "now use the create-story skill" — interpreted at runtime by the model. Goose recipes declare composition explicitly, with typed parameter flow, enabling static analysis of skill dependency graphs.

**Parameter definition** also more rigorous than Claude Code's conventions:

```yaml
parameters:
  - key: "unique_id"
    input_type: "string|number|boolean|date|file|select"
    requirement: "required|optional|user_prompt"
    description: "Human-readable text"
    default: "value"
    options: []   # required for select
```

Typed inputs. Required/optional/prompted-at-invocation semantics. Structured output schemas. These are workflow-engine features that elevate Recipes above prompt-driven composition.

### 1.4 Subagents — the runtime primitive

**What they are:** Independent execution instances that run in parallel to the main session, with their own context and tool set, per [Goose subagents docs](https://goose-docs.ai/docs/guides/subagents) verified 2026-04-22.

**How they compose with the other primitives:**
- A subagent is a *runtime instance*, not a file artifact
- A subagent's *behavior profile* is defined by a recipe (the recipe configures what knowledge, tools, and instructions the subagent operates with)
- A subagent's *knowledge* comes from skills loaded into its context
- A subagent's *capabilities* come from extensions declared in its recipe

**Invocation:** Natural-language, either autonomous ("Goose decides to spawn subagents when beneficial") or explicit ("Use the security-auditor recipe to scan this endpoint"). Parallel execution triggered by keywords: "in parallel", "simultaneously", "at the same time", "concurrently".

**Hard structural constraints:**
- **Subagents cannot spawn additional subagents** (one level of nesting only)
- **Subagents cannot manage extensions** (they can browse but not enable them)
- **Subagents cannot create scheduled tasks**

These constraints are significant for sprint-dev conversion (see §5) — they mean the "sprint-dev spawns dev subagents which themselves invoke AVFL subagents" pattern doesn't fit Goose's one-level-deep rule.

## 2. Recipes vs Claude Code Primitives — The Real Comparison

Now the comparison maps cleanly across the architectural layers.

| Concern | Claude Code | Goose | Overlap / Difference |
|---|---|---|---|
| **Capability (tools)** | MCP servers configured globally in `settings.json` | Extensions declared per-recipe or globally | Same underlying substrate (MCP). Goose's per-recipe scoping is cleaner for workflows needing specific toolsets. |
| **Knowledge (skills)** | Skills at `.claude/skills/<name>/SKILL.md` | Skills at `~/.config/goose/skills/` (or `~/.claude/skills/`) | **Format-compatible** via the cross-platform Agent Skills open standard. |
| **Authoritative rules always in context** | `.claude/rules/*.md` + nested `CLAUDE.md` auto-loaded into system prompt | `AGENTS.md` (cross-vendor standard) | Different file conventions, converging. Goose is an AAIF founding contributor to AGENTS.md. |
| **Declarative workflow composition** | **None natively** — `workflow.md` files inside skills are prompts interpreted at runtime by convention | **Recipes** — first-class YAML with parameters, `sub_recipes`, structured response schemas | **This is Goose's unique advantage.** |
| **Lifecycle enforcement (hooks)** | First-class `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop` hooks via shell commands in `settings.json` | **Absent** (user-subscribable lifecycle hook surface does not exist) | **This is Claude Code's unique advantage.** |
| **Parallel execution** | Multiple `Agent` tool calls in one turn; `TeamCreate` for multi-agent dialogue | Subagents in parallel via natural-language trigger keywords | Both support parallel fan-out. Claude Code's is rigorous (explicit calls); Goose's is conversational. |
| **Inter-agent dialogue** | `TeamCreate` + `SendMessage` — agents talk iteratively | Not supported — subagents cannot coordinate peer-to-peer | Claude Code unique. Retro auditor-team style does not port. |
| **Subagent depth** | Unlimited nesting | **One level only** | Structural constraint in Goose. |
| **Structured output** | Free-form prose by default; skills can enforce structure via prompt | `response` schema field with typed JSON output | Goose advantage. Genuinely helpful for downstream parsing. |
| **Retry logic** | Skill-level prompt convention | First-class `retry` field with validation rules | Goose advantage for production workflows. |
| **Parameter flow across composition** | Prompt convention ("use skill X with these inputs") | `sub_recipes.values` mapping, typed at recipe definition time | Goose advantage. Static analyzable. |

### 2.1 Where Recipes Shine Beyond What Claude Code Has

Three specific primitives that are genuinely better in Goose:

**1. `sub_recipes` with mapped parameters.** Claude Code skills invoke other skills through prompt convention. Goose recipes declare composition as data. Static dependency analysis becomes possible — orphan recipes (declared but never invoked) are detectable, parameter flow is verifiable, version diffs are diffable at the composition-graph level, not just the prompt level.

**2. `response` schemas with structured output.** Claude Code's skill outputs are prose that downstream consumers have to parse probabilistically. Goose recipes can declare typed JSON schemas that the runtime enforces the output against. For workflows that produce artifacts consumed by other workflows (sprint reports, classification results, Gherkin specs), this is a substantial improvement.

**3. First-class `retry` logic with validation.** A recipe can declare "retry up to 3 times if validator X fails." Claude Code's skills rely on prompt-level retry convention — "if the output doesn't parse, try again" — which is fragile. Goose's retry is structural.

### 2.2 Where Recipes Fall Short of Claude Code Primitives

Three specific gaps:

**1. No hook-based lifecycle enforcement.** Momentum's hooks (plan-audit, architecture-guard, autonomous-commit, tab-rename, context-refresh) are enforceable at the agent's tool-call lifecycle. Goose has no equivalent. Recipes can describe workflow but cannot gate tool calls at runtime. Hook-dependent invariants must be rebuilt as model-discipline (in instructions) or external process monitoring.

**2. One-level subagent nesting.** Momentum's orchestration is deeper than one level — sprint-dev spawns dev subagents, which may spawn specialist subagents, which may invoke AVFL. Goose's one-level rule means this nesting must be flattened, with intermediate coordination happening at the top-level recipe rather than being pushed down.

**3. No inter-agent dialogue.** Momentum's retro uses TeamCreate + SendMessage for auditor-team conversation. Goose subagents can run in parallel but cannot coordinate peer-to-peer. Any workflow that depends on iterative agent dialogue must be re-expressed as sequential phases with consolidation — losing the back-and-forth refinement.

### 2.3 Complementary, Not Substitutable

The honest architectural read: **Goose Recipes are better at composition; Claude Code hooks are better at enforcement.** These are orthogonal concerns. A future Momentum could plausibly have both — recipe-style declarative composition *and* hook-based enforcement. Neither system has both today. Momentum's existing hook discipline is genuine leverage against Goose for enforcement-critical workflows; Goose's Recipe primitive is genuine leverage against Claude Code for composition-heavy workflows.

## 3. Integration Paths Between Goose and Claude Code

Five paths in increasing integration depth:

**Path 1 — Pure process isolation.** Claude Code in one cmux workspace, Goose in another. Shared git repo with per-tool worktrees. Human orchestrates. Zero integration code. This is the Momentum-flavored default from the [integration-strategy analysis](./integration-strategy-analysis-2026-04-21.md).

**Path 2 — cmux-driven dispatch.** Claude Code's sprint-dev skill spawns a cmux pane and runs `goose run --recipe <name> --params '{...}'` in it. Awaits filesystem sentinel. Reads result. Same pattern as ForgeCode dispatch. Uses Momentum's `momentum:dispatch-to-pane` skill. No MCP required.

**Path 3 — MCP wrapping via AgentAPI.** [coder/agentapi](https://github.com/coder/agentapi) wraps Goose (and Claude Code, Aider, etc.) into an HTTP API. That HTTP API can back an MCP server exposing Goose recipes as callable Claude Code tools. Higher integration cost; enables autonomous inline dispatch.

**Path 4 — Shared skills, different runtimes.** Because Goose reads the Agent Skills open standard, a Momentum skill authored once works on both Claude Code and Goose. Developer (or change-type classifier) chooses which runtime at invocation time. Cheapest path to letting both tools handle the same workloads.

**Path 5 — Goose recipe that loads Momentum skills.** A Goose recipe declares extensions and instructions; those instructions can reference skills available in the session's skill path. A recipe can be authored that "uses the momentum-create-story skill to draft a story from this issue" — the recipe-configured subagent invokes the Momentum skill during execution. Composes the two primitive models directly.

### Recommended combination for Momentum

**Path 4 + Path 2.** Author skills once (they load on both hosts via the cross-platform standard), dispatch specific runs to Goose via cmux when you want Goose-specific capabilities (local-model recipes, AAIF extension ecosystem, parallel subagents, structured recipe outputs). Get the best of both without writing integration shims.

## 4. The Sprint-Dev Conversion Experiment

### Why sprint-dev is the productive candidate

Sprint-dev has four characteristics that make it the highest-signal workflow to convert:

1. **Composition-heavy.** Sprint → waves → stories → dev subagents → (optional) post-merge AVFL. Recipes' native fit.
2. **Parameterized.** sprint_id, stories_index_path, worktree_root, wave_size. All clean typed parameters.
3. **Long-running and autonomous ("yolo").** The skill runs for tens of minutes to hours with limited human checkpoints. This is exactly the workload declarative composition protects against drift on.
4. **Not hook-critical.** Unlike `create-story` (plan-audit hook) or code-change skills (architecture-guard, autonomous-commit), sprint-dev's enforcement is mostly post-hoc (AVFL after merge). The hook gap matters less for sprint-dev than for other skills.

### Proposed recipe shape

A first-pass sketch, not final production code — the purpose is to make the conversion concrete enough to reason about.

**Top-level recipe:**

```yaml
# sprint-dev.yaml
version: "1.0.0"
title: sprint-dev
description: |
  Dependency-driven execution of a Momentum sprint. Topologically sorts
  story graph, dispatches per-story dev sub-recipes in waves, runs
  post-merge AVFL, produces sprint closure report.

parameters:
  - key: sprint_id
    input_type: string
    requirement: required
    description: Identifier of the sprint to execute
  - key: stories_index_path
    input_type: file
    requirement: required
    description: Path to stories/index.json with dependency graph
  - key: worktree_root
    input_type: string
    requirement: required
    description: Parent directory under which per-story worktrees are created
  - key: max_parallel_stories_per_wave
    input_type: number
    requirement: optional
    default: 4

instructions: |
  Execute sprint {{ sprint_id }}.

  1. Read {{ stories_index_path }} to get the story dependency graph.
  2. Topologically sort stories into waves (ready to execute in parallel).
  3. For each wave, in parallel (up to {{ max_parallel_stories_per_wave }}
     at once), invoke the dev-story sub-recipe per story.
  4. After all waves complete and stories merge, invoke post-merge-avfl
     sub-recipe once with all story diffs.
  5. Produce sprint-closure report with story outcomes, AVFL findings,
     retro-candidate items.

extensions:
  - type: stdio
    name: git-worktree
    cmd: momentum-git-worktree-mcp
    description: Worktree creation, branching, merge handling
  - type: stdio
    name: momentum-state
    cmd: momentum-state-mcp
    description: Reads/writes stories/index.json and sprints/index.json
  - type: builtin
    name: developer

sub_recipes:
  - name: dev-story
    path: ./recipes/dev-story.yaml
    description: Single-story execution subagent profile
  - name: post-merge-avfl
    path: ./recipes/post-merge-avfl.yaml
    sequential_when_repeated: true
    description: Multi-lens validation of merged story diffs

response:
  type: object
  properties:
    sprint_id: { type: string }
    outcomes: { type: array }
    avfl_findings: { type: array }
    retro_candidates: { type: array }
    status: { type: string, enum: [clean, warning, failed] }
```

**Per-story sub-recipe:**

```yaml
# recipes/dev-story.yaml
title: dev-story
description: Execute a single Momentum story in its own worktree

parameters:
  - key: story_path
    input_type: file
    requirement: required
  - key: worktree_path
    input_type: string
    requirement: required
  - key: change_type
    input_type: select
    requirement: required
    options: [feat, fix, refactor, docs, chore, test]
  - key: preferred_host
    input_type: select
    requirement: optional
    default: goose-native
    options: [claude-code, forge, goose-native]

instructions: |
  Read story at {{ story_path }}.
  Set working directory to {{ worktree_path }}.
  Implement per acceptance criteria in the story frontmatter.
  Change-type is {{ change_type }} — apply change-type-appropriate conventions.
  Commit atomically using conventional commits format; do not amend or rebase.

extensions:
  - type: stdio
    name: momentum-dev-tools

response:
  type: object
  properties:
    story_id: { type: string }
    commits: { type: array }
    tests_passed: { type: boolean }
    blockers: { type: array }
```

### What ports cleanly (~70%)

- **Dependency-graph traversal and wave dispatch.** Natural recipe composition; parallel subagent spawns are supported via natural-language triggers.
- **Per-story sub-recipe invocation.** Exactly the `sub_recipes` use case. Parameters flow explicitly. Static analyzable.
- **Worktree lifecycle.** A `git-worktree` MCP extension exposes create/remove/merge operations.
- **Story state read/write.** A `momentum-state` MCP extension wraps stories/index.json and sprints/index.json access, enforcing the sprint-manager contract.
- **Post-merge AVFL.** Itself becomes a sub-recipe declaring the four-lens structure, validators in parallel, consolidation.
- **Structured sprint closure report.** Goose's `response` schema makes this first-class — sprint closure is a typed JSON artifact, not free-form prose.

### What does NOT port cleanly (~30%)

- **Plan-audit hook on plan-mode transitions.** No Goose equivalent. Workaround: instructions say "before writing, produce a plan file and stop." Relies on model discipline, not enforcement.
- **Architecture-guard hook on file writes.** Same gap. Workaround: post-hoc MCP tool call that scans for drift — after drift has already occurred.
- **Autonomous-commit `PostToolUse` hook.** Workaround: instructions say "commit after every edit." Relies on model discipline.
- **Auditor-team dialogue for AVFL (TeamCreate + SendMessage).** Hard blocker for the iterative refinement. Workaround: run each auditor sequentially as a sub-recipe, consolidate outputs via a consolidator sub-recipe. Loses back-and-forth.
- **Subagent-spawning-subagent nesting.** If dev-story wants to invoke AVFL mid-task on its own output, can't. AVFL moves entirely to the top-level sprint-dev recipe.
- **Hook-based `UserPromptSubmit` tab-rename, reminders, state refresh.** Harness-level behaviors that don't map to the recipe model. External wrapper scripts are the workaround.

### Feasibility verdict

**~70% clean translation.** The composition layer ports well; hook-based enforcement doesn't; AVFL's team-dialogue pattern flattens to sequential. The translation exercise itself is valuable because it forces confrontation with exactly which Momentum invariants are enforced vs. merely suggested.

## 5. Eval Fixture Comparison Suite

Running fixtures against both implementations is the productive part. Applying the fixture-based testing pattern from the [retro → micro-eval analysis](./retro-microeval-loop-analysis-2026-04-21.md).

### What to measure

**Six axes of comparison:**

1. **Dependency resolution correctness.** Given identical stories/index.json with known graph, do both implementations produce identical topological order? How do they handle cycles, broken refs, missing stories?
2. **Parallelism fidelity.** Given a wave of 3 independent stories, do both implementations genuinely run them in parallel? Elapsed time? Token cost?
3. **Story-level correctness.** For a representative story, does each implementation produce a clean diff, passing tests, correctly-formatted commits? SWE-bench-style grading on the resulting diff.
4. **AVFL finding parity.** Post-merge AVFL on the same corpus — do both implementations produce similar findings, severities, confidence levels?
5. **Hook-invariant preservation.** Do hook-dependent invariants (conventional-commit format, plan-before-act ordering, architecture-boundary respect) hold in the Goose implementation despite the absence of hooks?
6. **Recovery behavior.** Inject known failures into stories. Does each implementation detect, report, retry appropriately?

### Fixture suite design

| Fixture | Input | Expected output | Assertion type | Sample count |
|---|---|---|---|---|
| **F1: topological order determinism** | Graph G with 10 stories, 7 edges | `topological_order(G)` | Equality | 1 run (near-deterministic) |
| **F2: story-level diff quality** | Story spec S | tests pass ≥ 90%, diff lines ∈ [X, Y], commits atomic | Probabilistic | 10 runs |
| **F3: parallelism** | 3-story independent wave | elapsed < 1.5 × max(individual story time) | Probabilistic | 5 runs |
| **F4: AVFL parity** | Diff D | Finding-class overlap ≥ 80%, severity distribution matches | Probabilistic | 5 runs |
| **F5: commit-format invariant** | N commits from a run | Each matches `type(scope): message` | Deterministic | 1 run (count-based) |
| **F6: plan-before-act invariant** | Session transcript | plan file exists before first write | Deterministic | 1 run (file check) |
| **F7: architecture-boundary invariant** | Diff D across directories | No writes outside story-declared scope | Deterministic | 1 run |
| **F8: recovery from injected failure** | Story with broken test | Implementation detects, reports, retries or escalates | Probabilistic | 5 runs |

Each fixture runs on **both implementations** (Claude Code sprint-dev and Goose recipe) and the comparison surfaces exactly where Goose's lack of hooks matters in practice.

### The three likely outcomes — each decision-useful

**Outcome A — Goose handles it fine.** Fixtures pass on both implementations with comparable rates. Hook-dependent invariants hold through model discipline alone. Cost of Momentum's hook layer is revealed to be lower than assumed. Momentum could simplify by promoting reliable invariants from hook-enforced to convention-documented.

**Outcome B — Goose handles most of it, but specific invariants fail reliably.** Commit-format invariant fails on Goose, passes on Claude Code. Plan-before-act invariant fails on Goose with temperature > 0.3. Architecture-boundary invariant holds because the model is well-behaved. This outcome tells you exactly which hooks are load-bearing and which are defensive redundancy. Informs where to invest enforcement effort: promote the failing ones from convention to structural-enforcement (either keep on Claude Code, or if moving to Goose, implement via external wrappers).

**Outcome C — Goose fails enough that recipes are not viable for sprint-dev.** Hook dependencies are deep; model discipline without enforcement is insufficient. You've empirically proven Momentum's hook layer is essential to sprint-dev specifically, and Goose is not a viable host for this workflow regardless of the rest of the primitives. Significant architectural finding.

Any outcome is decision-useful. Outcome B is the most likely and the most informative.

### What the experiment would produce as a durable artifact

A **named-invariant taxonomy** for Momentum — the list of specific invariants sprint-dev depends on, which ones are hook-enforced vs convention-documented, and empirical evidence on how each fares under convention-only execution. This taxonomy is valuable independently of Goose adoption — it becomes input to the retro → micro-eval loop's fixture library, and to future host-selection decisions for other workflows.

## 6. Composition With Sibling Analyses

This analysis composes with three sibling analyses in the research project:

**[Integration strategy analysis](./integration-strategy-analysis-2026-04-21.md)** — recommended three-layer integration strategy (process isolation baseline → cmux-driven dispatch → MCP only when inline autonomous loops required). The Path 2 recommendation in this document (cmux-driven dispatch) is an instance of that middle layer; the sprint-dev recipe conversion would be dispatched via `momentum:dispatch-to-pane`.

**[Retro → micro-eval loop analysis](./retro-microeval-loop-analysis-2026-04-21.md)** — the fixture-based testing pattern this analysis proposes for the sprint-dev comparison *is the retro → micro-eval pattern applied to a specific experiment*. Fixtures generated from the Goose/Claude-Code comparison become permanent regression coverage on both hosts. Cross-host fixture pass rates become a fitness matrix for the model routing / change-type dispatch decisions.

**[ForgeCode fit analysis](./forgecode-fit-analysis-2026-04-22.md)** — established that skill format compatibility is explicit in ForgeCode. The same holds for Goose via the cross-platform Agent Skills standard. This analysis establishes that **Recipes are the composition-layer primitive Claude Code doesn't have**, which is a distinct architectural finding from ForgeCode's structural-tool-allowlist approach. Together the three analyses map the peer-tool primitive landscape: ForgeCode offers structural enforcement of per-agent boundaries; Goose offers declarative workflow composition; Claude Code offers hook-based lifecycle enforcement. Each is a distinct contribution; none subsumes the others.

## 7. Decision-Ready Framings

### Decision A — Run the sprint-dev conversion experiment

**Framing:** Should Momentum invest ~2 sprints in converting sprint-dev to a Goose recipe and running the fixture comparison suite against the Claude Code implementation?

**Recommendation:** Yes, after the fixture infrastructure ships (per sequencing recommendation in §8).

**Evidence:** The experiment produces a durable named-invariant taxonomy regardless of outcome. Outcome B is the most likely and most informative — tells Momentum exactly which hooks are load-bearing. Cost (~2 sprints) is bounded. Result improves architectural decisions for every future host-selection question.

### Decision B — Adopt sub_recipes pattern for Momentum skill composition

**Framing:** Should Momentum adopt Goose's `sub_recipes` composition pattern in its own skill format, regardless of whether Momentum ever runs on Goose?

**Recommendation:** Yes. Formalize skill composition as machine-readable YAML frontmatter (e.g., a `composes: [sub-skill-name: {values: {...}}]` field in SKILL.md frontmatter). Enables static dependency analysis, orphan detection, parameter-flow verification for Momentum skills.

**Evidence:** Goose's `sub_recipes` is the single most interesting primitive surfaced in this research. Adopting the pattern is independent of Goose adoption — it improves Momentum's own composition rigor. Static analyzability catches skill-graph issues that currently only surface at runtime.

### Decision C — Adopt response-schema pattern for structured skill outputs

**Framing:** Should Momentum adopt Goose's `response` schema pattern for skill outputs that are consumed by other skills?

**Recommendation:** Yes, for skills whose outputs are structured artifacts (sprint closure reports, AVFL findings, change-type classifications, Gherkin specs). Declare a JSON schema in frontmatter; assert output against it at skill-exit.

**Evidence:** Currently Momentum skills produce prose outputs that downstream consumers parse probabilistically. Typed outputs with validated schemas make cross-skill composition more reliable. Independent of Goose adoption.

### Decision D — Author Momentum skills to the cross-platform standard from the start

**Framing:** Given the broad cross-platform convergence on Agent Skills open standard (Goose, ForgeCode, JetBrains Junie, Codex, Cursor, and many others), should Momentum author skills to the cross-platform standard from the start to maximize portability?

**Recommendation:** Yes. Continue authoring skills under `.claude/skills/` as the canonical location (since it is the de-facto path widely supported), ensure frontmatter uses only fields in the cross-platform standard, generate `AGENTS.md` symlinks/stubs at install time for tools that require that path. Makes every Momentum skill portable to every peer host without rework.

**Evidence:** Cross-platform skill portability is a market-led convergence, not a Momentum-internal concern. Authoring to the standard costs nothing extra today and eliminates porting work for every future host-adoption decision.

### Decision E — Integration pattern for Goose specifically

**Framing:** Which integration path (1-5 from §3) should Momentum use when invoking Goose?

**Recommendation:** Path 4 + Path 2 combined — author skills once under the cross-platform standard (they work on both hosts), dispatch specific runs to Goose via cmux when you want Goose-specific capabilities. Path 3 (MCP wrapping) remains an option if autonomous inline dispatch is ever required.

**Evidence:** Path 4 + Path 2 is the lowest-friction combination that gives Momentum access to Goose's differentiators (local-model recipes, AAIF extensions, parallel subagents, typed outputs) without locking into Goose-specific primitives. Matches the integration-strategy analysis's broader guidance.

## 8. Sequencing

Combining with sibling-analysis recommendations:

1. **First: fixture infrastructure** (per retro-microeval analysis Decision A). `momentum:micro-eval` runner + fixture schema. ~1 sprint.
2. **Second: `sub_recipes`-style composition pattern in Momentum skills** (Decision B above). Independent of any host integration; improves Momentum's own architectural rigor. ~1 sprint.
3. **Third: OpenCode parallel-track experiment** (per ForgeCode-fit analysis Decision E). Lowest setup cost because OpenCode reads `.claude/skills/` natively. ~1 week.
4. **Fourth: Sprint-dev conversion to Goose recipe + fixture comparison** (Decision A above). Benefits from the fixture infrastructure and composition-pattern work. ~2 sprints.
5. **Fifth: ForgeCode dev-agent integration** (per ForgeCode-fit analysis). Benefits from all prior learnings. ~1 week for v1.

This is a ~2-3 month roadmap covering all five open initiatives. Any of them can be promoted or deferred based on sprint-level priorities.

## 9. Open Questions Deferred to Implementation

- **Does Goose's `response` schema validation actually enforce output shape, or is it advisory?** Runtime behavior worth verifying before relying on it for downstream composition.
- **What is the cost of Goose's `retry` logic per retry in practice?** Affects whether production workflows should depend on it.
- **How does Goose's recipe marketplace handle versioning?** If Momentum publishes recipes to the AAIF marketplace, what is the version-compatibility story?
- **Can a Goose recipe load Momentum skills from `.claude/skills/` at session-scoped path configuration, or only from `~/.config/goose/skills/`?** Affects Path 5 (recipe-loads-Momentum-skills) viability.
- **Does Goose's subagent-cannot-spawn-subagent rule extend to skill-invoked-sub-skills, or only to programmatic subagent spawning?** Affects whether Momentum's deeply-nested skill compositions work inside a Goose recipe.
- **What is the `FORGE_DEBUG_REQUESTS`-equivalent in Goose for capturing session traces for fixture reconstruction?** Affects retro-loop integration.
- **How does Momentum's plugin distribution map to Goose's global-skills path?** Likely a small install-time mirror/symlink similar to the ForgeCode case.

## 10. Next Steps

1. **Commit this analysis.** Decision-ready framings captured; ready for backlog intake.
2. **Intake six backlog items** for `momentum:intake`:
   - **Story: `momentum:micro-eval` runner skill** (per retro-microeval analysis; dependency for the comparison experiment).
   - **Story: `sub_recipes`-style composition in SKILL.md frontmatter** (Decision B).
   - **Story: `response` schema validation for structured skill outputs** (Decision C).
   - **Spike: Sprint-dev conversion to Goose recipe** (the translation exercise).
   - **Story: Fixture comparison suite for sprint-dev on Claude Code vs Goose** (the experiment).
   - **Story: Author Momentum skills to cross-platform Agent Skills standard** (Decision D).
3. **Review sibling analyses for conflicts.** This analysis recommends Goose and ForgeCode dev-agent integration both; ensure sequencing (§8) is coherent with the ForgeCode-fit analysis's Decision E sequencing.

## Sources

Internal:
- [Integration strategy sibling analysis](./integration-strategy-analysis-2026-04-21.md)
- [Retro → micro-eval loop sibling analysis](./retro-microeval-loop-analysis-2026-04-21.md)
- [ForgeCode fit sibling analysis](./forgecode-fit-analysis-2026-04-22.md)
- [Consolidated research report](../final/forgecode-agentic-tools-eval-final-2026-04-21.md)

External (verified 2026-04-22):
- [Goose Recipes Reference](https://goose-docs.ai/docs/guides/recipes/recipe-reference) — full YAML schema
- [Goose Subagents documentation](https://goose-docs.ai/docs/guides/subagents) — parallel execution, invocation, constraints
- [Goose Recipes overview](https://goose-docs.ai/docs/guides/recipes/)
- [Goose ACP Providers](https://goose-docs.ai/docs/guides/acp-providers/) — subscription passthrough mechanics
- [aaif-goose/goose](https://github.com/aaif-goose/goose) — canonical repo, v1.31.1 as of 2026-04-20
- [Block — Goose open-source announcement](https://block.xyz/inside/block-open-source-introduces-codename-goose)
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) — cross-platform skills directory convention
- [coder/agentapi](https://github.com/coder/agentapi) — HTTP API wrapper (Path 3 integration primitive)
