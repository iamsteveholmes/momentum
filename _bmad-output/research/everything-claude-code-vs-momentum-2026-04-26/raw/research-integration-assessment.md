---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Integration assessment — should Momentum integrate parts of everything-claude-code?"
topic: "everything-claude-code vs Momentum — comparative analysis"
---

# Integration Assessment — Should Momentum Integrate Parts of everything-claude-code?

## Inline Summary

Of ECC's surface, only three components clear the bar for adoption: `silent-failure-hunter` (drop-in adversarial agent), `repo-scan` (cross-stack codebase audit, kept as a community import), and the `post-edit-format` / `post-edit-console-warn` hook patterns (port the *idea*, not the JS). The strategic recommendation is **stay independent and cherry-pick aggressively**: ECC is a horizontally-scoped toolkit (38 agents, 156 skills, ~40 hook scripts / ~14 hook IDs, 79 commands) and Momentum is a vertically-scoped agentic-engineering practice; integrating broadly would dilute Momentum's sprint discipline and sole-writer guarantees. Treat ECC as a quarry — mine specific stones, never adopt the whole structure. [PRAC]

---

## What Was Verified Live in the ECC Repo

Before classifying anything, the live state of `affaan-m/everything-claude-code` (commit shallow-cloned 2026-04-26) was inspected directly. Confirmed present: [OFFICIAL]

- `agents/` — 48 markdown agent definitions (e.g. `code-reviewer.md`, `silent-failure-hunter.md`, `tdd-guide.md`, `planner.md`, `loop-operator.md`, `harness-optimizer.md`, `security-reviewer.md`, plus per-language reviewers and build-resolvers).
- `skills/` — 183 directories under `skills/`. Plugin manifest at `.claude-plugin/plugin.json` advertises `version: 1.10.0`, "38 agents, 156 skills" (the directory count is higher because some are scaffolds).
- `hooks/hooks.json` — Single registration file that delegates to Node scripts under `scripts/hooks/` (e.g. `pre-bash-dispatcher.js`, `post-edit-format.js`, `post-edit-console-warn.js`, `pre-bash-dev-server-block.js`).
- `mcp-configs/mcp-servers.json` — Single file with ~20 MCP server templates (jira, github, firecrawl, supabase, sequential-thinking, vercel, omega-memory, etc.).
- `manifests/` — `install-profiles.json`, `install-modules.json`, `install-components.json` — ECC's selective-install architecture.
- `scripts/` — Node-based installer (`install-plan.js`, `install-apply.js`), hook bootstrappers, codex/opencode adapters, dashboards.
- `commands/` — 79 slash-command markdown files including a `hookify` family.
- `ecc2/` — A Rust crate (`ecc-tui`, `ratatui` + `rusqlite` + `git2`) — alpha control-plane. Real code, not a phantom.
- `tests/` — 95+ `.test.js` / `test_*.py` files across `tests/ci/`, `tests/hooks/`, `tests/integration/`, etc.
- `the-security-guide.md` references `affaan-m/agentshield` as a **separate** repository. AgentShield is **not** part of ECC — it is a sibling project. The "1,282 tests in AgentShield" claim from the prior report cannot be verified from inside ECC. [UNVERIFIED]
- `Hookify` exists, but it is a slash-command + skill (`commands/hookify.md`, `skills/hookify-rules/`), not a "conversational config" wizard. It is a frontmatter-driven rule generator. [OFFICIAL]

What was **not** found and should be treated as nonexistent for integration purposes: any single test directory totalling 1,282 tests; any "AgentShield" component shipped inside ECC; any TypeScript build pipeline (ECC ships JS-only via Node `>=18`). [UNVERIFIED]

---

## Adopt-as-Is

These are the only ECC artifacts worth dropping in unchanged.

### `agents/silent-failure-hunter.md` → Momentum AVFL roster

**What it is.** A 40-line adversarial agent prompt with one job: hunt empty catch blocks, swallowed errors, dangerous fallbacks, and lost stack traces. Tools: Read/Grep/Glob/Bash. Model: sonnet. [OFFICIAL — `agents/silent-failure-hunter.md`]

**Why adopt.** Momentum's AVFL framework already runs paired adversarial reviewers per lens (`skills/momentum/skills/avfl/SKILL.md`). Silent-failure-hunting is an established blind spot in the Coherence/Accuracy lenses and a perfect pluggable adversary. The prompt is short, model-agnostic, and free of ECC-specific tooling.

**Where it slots.** `/Users/steve/projects/momentum/skills/momentum/skills/avfl/agents/silent-failure-hunter.md` (or as a referenced sub-prompt invoked from the corpus-mode validator template in `references/framework.json`).

**Integration cost.** ~30 minutes. Convert ECC's tools array `["Read","Grep","Glob","Bash"]` to Momentum's preferred frontmatter (`allowed-tools: Read, Grep, Glob, Bash`), strip the model line (Momentum routes through model frontmatter conventions per `~/.claude/rules/model-routing.md`), commit as `feat(skills): avfl — add silent-failure-hunter adversary`. [PRAC]

**Conflicts.** None. The agent is read-only and does not touch sprint state.

### `skills/repo-scan/SKILL.md` → Momentum onboarding for brownfield codebases

**What it is.** A `community`-origin skill that classifies every file in a repo as project / third-party / build-artifact, detects 50+ embedded libraries, and produces a four-level verdict (Core Asset / Extract & Merge / Rebuild / Deprecate) with an HTML report. ECC ships only the SKILL.md pointer — the implementation lives at `https://github.com/haibindev/repo-scan` pinned to commit `2742664`. [OFFICIAL — `skills/repo-scan/SKILL.md`]

**Why adopt.** Momentum has no equivalent. `momentum:assessment` evaluates *product state*, not *codebase asset composition*. When Momentum is dropped onto a brownfield project — which is increasingly common as the practice spreads — there is currently no skill that answers "what fraction of this repo is even ours?" before sprint planning starts.

**Where it slots.** `/Users/steve/projects/momentum/skills/momentum/skills/repo-scan/` as a standalone skill, **invoked by `assessment`**, not by Impetus directly. Tag with `origin: community` to preserve attribution.

**Integration cost.** ~1 hour to copy SKILL.md, add a Momentum frontmatter (`model: claude-sonnet-4-6`, `effort: medium`, `user-invocable: false`), and wire one optional step into `assessment`'s workflow.md. The runtime install instructions stay pointing at the upstream haibindev repo. [PRAC]

**Conflicts.** Minor philosophical: it depends on a third-party scanner being installed on the host. Mitigation — make the skill print "scanner not installed; skipping" rather than failing.

---

## Adopt-with-Modification

These are *ideas* worth taking. The implementations should be re-built in Momentum's idiom.

### Hook ideas: `post-edit-format` + `post-edit-console-warn`

**What ECC ships.** `scripts/hooks/post-edit-format.js` auto-detects Biome vs. Prettier from project config and runs the formatter on the edited file (`scripts/hooks/post-edit-format.js`, ~150 lines of Node). `scripts/hooks/post-edit-console-warn.js` greps for `console.log` after each Edit and prints line numbers as a non-blocking warning. [OFFICIAL]

**Why the idea is good.** Both hooks address a class Momentum's PostToolUse hook (`/Users/steve/projects/momentum/skills/momentum/hooks/hooks.json`) already covers conceptually — `lint-format.sh` runs after Edit/Write — but Momentum's implementation is a single bash dispatcher that delegates to a project-local `.claude/momentum/hooks/lint-format.sh`. The console-warn hook is a missing complement.

**What to take.** The *behavior* (formatter auto-detect; non-blocking debug-statement warnings). Not the JS. [PRAC]

**What to modify.** Re-implement as a small bash addition to the existing Momentum hook chain. Keep the project-local override pattern. Avoid adding Node as a runtime dependency for hooks — Momentum has stayed bash-only and that simplicity is a feature.

**Cost.** ~2 hours to write a `post-edit-debug-warn.sh` and extend `lint-format.sh`'s formatter detection. Stories: backlog under `_bmad-output/implementation-artifacts/stories/` (no in-flight overlap visible in `index.json`).

**Conflicts.** None. Reinforces the existing single-bash-dispatcher pattern.

### `skills/skill-stocktake/` → Momentum skill quality eval

**What ECC ships.** A slash command + skill that scans `~/.claude/skills/` and `{cwd}/.claude/skills/` and runs an LLM-based quality eval against every SKILL.md, with a results cache (`skills/skill-stocktake/results.json`) and a Quick Scan diff mode. [OFFICIAL — `skills/skill-stocktake/SKILL.md`]

**Why the idea is good.** Momentum already has the in-flight story `impetus-eval-triage` (one of the two intake stubs from commit `b908520`) and runs `quality-analysis findings` on Impetus (commit `b64705c` — "stub 4 Impetus quality-analysis findings as backlog stories"). A skill-quality stocktake of the entire Momentum plugin is a natural next step.

**What to modify.** Run it under AVFL's `corpus: true` mode rather than as a standalone Quick-Scan harness. The corpus-mode infrastructure already enumerates files, distributes to validators, and consolidates findings; skill-stocktake's bespoke harness duplicates that. The judgment criteria and results-cache idea are the parts to keep.

**Cost.** Substantial — this is a small new skill, not a copy. ~1 sprint to wire `momentum:skill-stocktake` as a thin wrapper that sets up an AVFL corpus call over `skills/momentum/skills/**/SKILL.md` with the stocktake-specific dimensions injected.

**Conflicts.** Architectural — must respect Momentum's sole-writer pattern (sprint-manager owns `stories/index.json`); the stocktake skill must emit findings as story-stub files via `momentum:intake`, never write to indexes directly.

### `skills/strategic-compact/` → Momentum context-budget hint

**What ECC ships.** A skill plus a `suggest-compact.js` PreToolUse hook that counts tool calls and nudges the user to `/compact` at logical task boundaries (default threshold: 50 calls). [OFFICIAL — `skills/strategic-compact/SKILL.md`]

**Why the idea is good.** Momentum's `feedback_impetus_startup_latency` memory and the `agent-spawn-observability-metric` story both indicate the practice cares about long-session ergonomics. There is no equivalent compaction nudge today.

**What to modify.** Don't ship the JS hook. Instead extend Impetus's `Orient` phase to print a one-line context-pressure hint when the session shows tool-call accumulation patterns Impetus already inspects. Keep it inside the Momentum-orchestrator surface; don't introduce a new global hook.

**Cost.** Small — ~half a day inside an Impetus refinement story.

**Conflicts.** Minor — Momentum's hook policy is "single PostToolUse / PreToolUse / Stop dispatcher" (see `skills/momentum/hooks/hooks.json`). Adding a competing hook would violate that.

### `hooks/` matcher pattern → Momentum hook policy doc

**What ECC ships.** A `hooks.json` with one consolidated dispatcher per hook event (`pre:bash:dispatcher`, `post:edit:dispatcher`, etc.). [OFFICIAL — `hooks/hooks.json`]

**Why the idea is good.** Momentum already follows this pattern — a single bash dispatcher per event. ECC's `hooks.json` is more elaborate and demonstrates how to encode dispatcher routing data in the JSON itself (e.g. `id` and `description` fields per hook entry).

**What to modify.** Borrow the `id` / `description` annotation convention only. Document it as the canonical pattern in `references/hooks-config.json` so future hook contributions stay disciplined.

**Cost.** ~1 hour. [PRAC]

**Conflicts.** None.

---

## Watch-and-Learn

Don't integrate. Track for future relevance.

### `ecc2/` — the Rust TUI control plane

**What it is.** An alpha-quality Rust crate (`ratatui` + `rusqlite` + `git2`) that proposes a "session control plane above individual harness installs": multi-session state, observability, risk scoring, worktree-aware scaffolding. README states "alpha quality, not yet a public GA release." [OFFICIAL — `ecc2/README.md`]

**Why watch.** This is the most strategically interesting piece in the whole repo, and it's exactly the layer Momentum's `cmux-llm-marketplace-agents-2026-04-22` and `cmux-mobile-extension` research clusters are circling. Multi-agent-session orchestration with persisted state is a problem Momentum will hit when sprint-dev waves get bigger.

**Why not integrate now.** (1) It's alpha-grade. (2) Momentum's substrate is cmux + Claude Code, not a bespoke TUI. (3) The Rust dependency is a step-change in Momentum's maintenance posture (currently markdown + bash + tiny Python CLI per `skills/momentum/scripts/`).

**Action.** Add a watch entry to the research cluster. Re-evaluate at GA. [PRAC]

### `skills/continuous-learning-v2/` and `skills/instinct-*` (`commands/instinct-export.md`, etc.)

**What it is.** ECC's session-end pattern-extraction system: a Stop hook captures "instincts" from completed sessions and saves them as learned skills. v2 supersedes v1. [OFFICIAL — `skills/continuous-learning/SKILL.md`]

**Why watch.** Momentum's `momentum:distill` skill occupies the same conceptual slot but operates on retro Tier 1 findings, not auto-extracted patterns. There is a real divergence here: Momentum prefers human-curated distillation (`feedback_autonomous_commits_enforced`, the retro flow), while ECC bets on auto-extraction. Watching how `instinct-*` plays out at scale is informative; adopting it would invert Momentum's curation philosophy.

**Action.** Track. If ECC publishes signal-vs-noise rates for auto-extracted skills, revisit.

### `skills/skill-comply/` — automated compliance measurement

**What it is.** A skill that auto-generates compliance scenarios at three prompt-strictness levels, runs `claude -p`, captures stream-json tool traces, and classifies whether agents actually follow rules/skills. [OFFICIAL — `skills/skill-comply/SKILL.md`]

**Why watch.** This is a more ambitious take on what Momentum's `avfl-fixture-*` stories (`avfl-fixture-declining-skepticism-convergence`, `avfl-fixture-enumeration-completeness-recall`) are sketching. The eval mechanism is essentially a compliance harness over real agent runs, with measurable strictness gradients.

**Why not integrate.** Momentum's micro-eval approach (DEC-010 — fixture-based regression testing as practice primitive) is heading the same direction with cleaner alignment to the practice. Skill-comply's reliance on running `claude -p` end-to-end against scenarios is heavyweight; the fixture pattern is lighter.

**Action.** Re-read skill-comply when DEC-010 implementation begins to harvest test-case ideas. [PRAC]

### `manifests/install-profiles.json` selective-install architecture

**What it is.** A manifest-driven install system (profiles → modules → components) with five canned profiles (`core`, `developer`, `security`, `research`, `full`) and a Node CLI (`scripts/install-plan.js`, `scripts/install-apply.js`). [OFFICIAL]

**Why watch.** If Momentum ever ships sub-profiles (e.g. "Momentum-Lite" without sprint-manager for solo experimentation), this is a battle-tested pattern. ECC's schema (`schemas/install-profiles.schema.json`) is well-formed.

**Why not integrate.** Momentum is a single coherent practice. Splitting the plugin into install profiles would let users skip the parts that make Momentum *Momentum* (sprint discipline, sole-writer pattern, AVFL gates). The complexity cost is high and the user benefit is low until the catalog grows much larger. The current approach — one plugin, opinionated whole — matches `feedback_momentum_install_obsolete` (use standard Agent Skills installation).

**Action.** Bookmark the schemas. Revisit only if the plugin grows past ~50 skills. [PRAC]

### `agents/loop-operator.md` and `commands/loop-start.md`

**What it is.** A "loop operator" agent that runs autonomous loops with stop conditions, observability, and recovery actions. Pairs with `commands/loop-start.md`. [OFFICIAL]

**Why watch.** Momentum's `sprint-dev` is its loop. The escalation triggers ECC encodes ("no progress across two consecutive checkpoints", "repeated failures with identical stack traces", "cost drift outside budget window") are exactly the kinds of guardrails Momentum will need when sprints grow beyond ~10 stories.

**Action.** Use the escalation list as a checklist when hardening sprint-dev. Don't ship the agent — Momentum has its own orchestrator (`impetus`) that should own loop semantics.

---

## Ignore

Components that don't fit Momentum's philosophy or duplicate existing capability.

### Per-language reviewer agents (`agents/python-reviewer.md`, `agents/go-reviewer.md`, `agents/rust-reviewer.md`, ~10 more)

**Why ignore.** Momentum's `code-reviewer` skill (`/Users/steve/projects/momentum/skills/momentum/skills/code-reviewer/SKILL.md`) is intentionally language-agnostic and adversarial-by-default, invoked through AVFL. ECC's per-language reviewers add 10+ files of overlap and force Momentum to maintain a language matrix. Conflicts directly with the "practice not toolkit" stance. [PRAC]

### Per-language build-resolver agents (`go-build-resolver`, `rust-build-resolver`, `dart-build-resolver`, etc.)

**Why ignore.** Build resolution belongs in `bmad-quick-dev` or per-project rules, not in the practice plugin. Momentum's `agent-guidelines` skill already discovers project stack and writes path-scoped rules — adding pre-canned per-language agents creates duplicate authority. [PRAC]

### `skills/healthcare-*`, `skills/customs-trade-compliance/`, `skills/energy-procurement/`, `skills/visa-doc-translate/`, etc.

**Why ignore.** ECC ships dozens of vertical-domain skills that have no place in an agentic-engineering practice module. They are the strongest evidence that ECC is a "battle-tested toolkit for many use-cases" while Momentum is "a practice for one workflow class." Importing any of these would fork Momentum's identity. [PRAC]

### `skills/tdd-workflow/` + `agents/tdd-guide.md`

**Why ignore.** Momentum has DEC-010 (fixture-based regression testing as practice primitive) and the `bmad-testarch-atdd` skill in the BMAD catalog. ECC's TDD pair is implementation-heavy ("80%+ coverage, npm test, edge cases list") and mismatches Momentum's behavior-not-implementation Gherkin stance (`feedback_gherkin_atdd_generality`). Adopting it would weaken the existing discipline, not strengthen it.

### `mcp-configs/mcp-servers.json`

**Why ignore.** It's a list of ~20 MCP servers (jira, github, firecrawl, supabase, etc.) with placeholder credentials. Momentum should not bundle an MCP catalog — that's a per-project decision driven by `.mcp.json`. The only valuable insight is the *names* of useful servers (sequential-thinking, omega-memory) which can be referenced in onboarding docs. [PRAC]

### `commands/hookify*` family

**Why ignore.** Hookify is ECC's user-facing hook authoring system (`hookify`, `hookify-configure`, `hookify-help`, `hookify-list`, `hookify-rules` skill). It generates `.claude/hookify.{rule}.local.md` files with frontmatter rules. Momentum's hook layer is intentionally minimal — three bash dispatchers — and is configured through the practice itself, not through end-user rule authoring. Hookify would invert Momentum's "practice-shaped, not user-shaped" design. [PRAC]

### `agents/code-reviewer.md` (ECC version)

**Why ignore.** Direct duplicate of Momentum's `code-reviewer` skill, but less rigorous. ECC's code-reviewer instructs the agent to "report findings >80% confident" with no fixer loop. Momentum's code-reviewer is invoked by AVFL and pairs with the fix loop and lens-based finding consolidation. The ECC version would weaken Momentum's quality posture if substituted. [PRAC]

### `examples/statusline.json`

**Why ignore.** A 1-line bash statusline. Useful as inspiration but not a Momentum responsibility. The practice doesn't own the developer's terminal aesthetics. [PRAC]

### Most ECC scripts under `scripts/`

**Why ignore.** ECC's installer (`install-apply.js`, `install-plan.js`, `lib/install/*`), session adapters (`lib/session-adapters/`), codex/opencode bridges, and `ecc_dashboard.py` (39KB Python dashboard) all serve ECC's "many harnesses" cross-portability mandate. Momentum is Claude-Code-first and has no equivalent need. [PRAC]

---

## Fork

Components worth tracking the source of without integrating.

### `ecc2/` (Rust control plane) — possibly fork-worthy when GA

If ECC2 reaches 1.0, it could become a layer Momentum sits *on top of* — i.e., Momentum sprints become first-class entities in an ECC2 session store. At that point a fork (or a contributed integration patch) becomes interesting. Until then: read the code, watch the issues. [PRAC]

### `skills/skill-comply/` reference implementation

Worth keeping a reference checkout for harvest of compliance test scaffolding when Momentum's micro-eval runner story (`micro-eval-runner-skill` from intake stubs `b7c40c7`) starts. [PRAC]

### `the-security-guide.md`

The 28KB security longform. Not a Momentum artifact, but a reference text to cite from `momentum:research` when security topics surface. Treat as a bookmarked source. [OFFICIAL]

---

## Recommended Strategic Outlook

**Stay independent. Cherry-pick three things. Watch one.**

1. **Adopt now (one sprint, three commits):**
   - `silent-failure-hunter.md` into AVFL's adversarial roster.
   - `repo-scan` (community-origin pointer) wired into `assessment`.
   - The `post-edit-format` / `post-edit-console-warn` *behavior* re-implemented as bash additions to the existing Momentum hook chain.

2. **Adopt next (queued):**
   - Skill-stocktake idea, but built as an AVFL-corpus-mode wrapper rather than as ECC's standalone harness. Tied to in-flight `impetus-eval-triage` and `quality-analysis` stories.
   - Strategic-compact's nudging behavior, folded into Impetus rather than added as a competing hook.

3. **Watch (no integration):**
   - `ecc2/` Rust control plane — re-evaluate at GA.
   - `continuous-learning-v2` / `instinct-*` — divergent philosophy from Momentum's curation.
   - `skill-comply` — informs the micro-eval runner story.
   - Selective-install manifest architecture — relevant only if Momentum's plugin grows >50 skills.

4. **Ignore (do not import):**
   - Per-language reviewers and build-resolvers (10+ files of toolkit duplication).
   - Vertical-domain skills (healthcare, energy, customs, etc.).
   - ECC's TDD pair (philosophy mismatch).
   - Bundled MCP catalog (per-project decision).
   - Hookify family (inverts Momentum's hook policy).

### Architectural reasoning

Momentum's value is **constraint discipline**: sole-writer files (`stories/index.json`, `sprints/index.json`), AVFL gates, intake-queue.jsonl event log, sprint-manager validation of state transitions, sprint-dev's dependency-driven execution, and the rules cascade (global → project → session). Every constraint is a feature.

ECC's value is **breadth and battle-testing**: ~38 agents, ~156 skills, ~79 commands, hooks tested in a real CI matrix (95+ test files), a hardened Node installer, a Rust control plane in alpha, and a public marketplace presence. Every option is a feature.

Importing ECC broadly would replace a few hundred lines of constraint with thousands of lines of optional capability — exactly the inversion that broke earlier "kitchen-sink" practice modules. The three adoption candidates above are the rare cases where ECC's tested code matches a missing Momentum slot without dragging in the toolkit philosophy.

### Key conflict surfaces to keep watching

- **Sole-writer pattern.** Any imported skill that writes to `stories/index.json` or `sprints/index.json` directly violates Momentum's invariant (`/Users/steve/projects/momentum/skills/momentum/skills/sprint-manager/SKILL.md`). ECC's stocktake-style skills are flagged for this risk.
- **Hook count.** Momentum runs three bash dispatchers; ECC runs ~30 hook entrypoints across `scripts/hooks/`. Each new Momentum hook should be justified against the dispatcher pattern.
- **Runtime drift.** Momentum is markdown + bash + a small Python CLI (`skills/momentum/scripts/momentum-tools.py`). Adopting any ECC component that requires Node at runtime expands the dependency surface — reject unless the value is overwhelming.
- **Sprint discipline.** ECC's `loop-operator` and `continuous-learning-v2` are agent-driven autonomous loops; Momentum's loops run inside sprint-dev with explicit story state transitions. Don't blur the boundary.
- **AVFL authority.** AVFL is Momentum's quality gate. Imported review/eval skills must integrate *under* AVFL, not alongside it (per `feedback_avfl_post_merge_strategy`).

### One-line bottom line

ECC is a treasure of patterns wrapped in a toolkit philosophy Momentum should never adopt — quarry it carefully, ship the three small wins, and stay independent. [PRAC]

---

## Sources

1. `affaan-m/everything-claude-code` repository, shallow-clone 2026-04-26 (commit head as of clone) — `/tmp/ecc-research/` [OFFICIAL]
2. `everything-claude-code/.claude-plugin/plugin.json` — version 1.10.0, "38 agents, 156 skills, 72 legacy command shims" [OFFICIAL]
3. `everything-claude-code/.claude-plugin/marketplace.json` — author and category metadata [OFFICIAL]
4. `everything-claude-code/manifests/install-profiles.json` — five canned profiles (core/developer/security/research/full) [OFFICIAL]
5. `everything-claude-code/agents/silent-failure-hunter.md`, `agents/code-reviewer.md`, `agents/security-reviewer.md`, `agents/tdd-guide.md`, `agents/planner.md`, `agents/loop-operator.md`, `agents/harness-optimizer.md`, `agents/refactor-cleaner.md` [OFFICIAL]
6. `everything-claude-code/skills/repo-scan/SKILL.md`, `skills/skill-stocktake/SKILL.md`, `skills/skill-comply/SKILL.md`, `skills/strategic-compact/SKILL.md`, `skills/agentic-engineering/SKILL.md`, `skills/continuous-learning/SKILL.md`, `skills/deep-research/SKILL.md`, `skills/verification-loop/SKILL.md`, `skills/safety-guard/SKILL.md`, `skills/search-first/SKILL.md`, `skills/agent-eval/SKILL.md`, `skills/hookify-rules/SKILL.md` [OFFICIAL]
7. `everything-claude-code/hooks/hooks.json` and scripts under `everything-claude-code/scripts/hooks/` (post-edit-format.js, post-edit-console-warn.js, pre-bash-dev-server-block.js, pre-bash-dispatcher.js) [OFFICIAL]
8. `everything-claude-code/mcp-configs/mcp-servers.json` [OFFICIAL]
9. `everything-claude-code/ecc2/Cargo.toml`, `ecc2/README.md`, `ecc2/src/main.rs` — alpha Rust control-plane [OFFICIAL]
10. `everything-claude-code/REPO-ASSESSMENT.md`, `EVALUATION.md`, `SOUL.md`, `RULES.md`, `the-security-guide.md` [OFFICIAL]
11. `everything-claude-code/tests/` — 95+ test files across `ci/`, `hooks/`, `integration/` [OFFICIAL]
12. Momentum plugin manifest: `/Users/steve/projects/momentum/skills/momentum/.claude-plugin/plugin.json` (v0.17.0) [OFFICIAL]
13. Momentum AVFL skill: `/Users/steve/projects/momentum/skills/momentum/skills/avfl/SKILL.md` [OFFICIAL]
14. Momentum hook configuration: `/Users/steve/projects/momentum/skills/momentum/hooks/hooks.json` [OFFICIAL]
15. Momentum sprint-manager skill: `/Users/steve/projects/momentum/skills/momentum/skills/sprint-manager/SKILL.md` [OFFICIAL]
16. Momentum stories index: `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/index.json` (status distribution: 194 backlog, 96 done, 10 dropped) [OFFICIAL]
17. Momentum git log (last 50) — recent commits include Impetus rebuild (8e59814), feature-grooming refine (129bee9), DEC-010 fixture-based testing (f7802a0), DEC-011 project canvas foundations (52861ca) [OFFICIAL]
18. Momentum global rules: `~/.claude/rules/git-discipline.md`, `~/.claude/rules/workflow-fidelity.md`, `~/.claude/rules/spawning-patterns.md`, `~/.claude/rules/anti-patterns.md` [OFFICIAL]
19. Momentum project-scoped rules: `/Users/steve/projects/momentum/.claude/rules/dev-skills.md`, `version-on-release.md`, `plan-audit.md`, `workflow-fidelity.md` [OFFICIAL]
20. AgentShield reference (sibling project): `affaan-m/agentshield` cited in `everything-claude-code/the-security-guide.md` and `README.md` — exists as separate repo, not part of ECC [OFFICIAL for the reference; UNVERIFIED for "1,282 tests" claim]
