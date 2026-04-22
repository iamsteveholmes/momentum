---
title: "ForgeCode Fit Analysis — Where ForgeCode Fits in Momentum's Architecture"
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
  - path: raw/verification-forgecode-hooks-and-version.md
    relationship: verified_by
supplements: research/forgecode-agentic-tools-eval-2026-04-21
---

# ForgeCode Fit Analysis — Where ForgeCode Fits in Momentum's Architecture

## Executive Summary

ForgeCode is **specialized as a single-task code-execution harness, not a practice-layer host.** It is architecturally opinionated about *inside-the-task* (Sage/Muse/Forge role separation, tool allowlists, plan-file handoff, `todo_write` enforcement) and deliberately silent about *outside-the-task* (sprints, stories, team coordination, retros). This means ForgeCode is appropriate for exactly one layer of Momentum's architecture — the dev-agent layer inside `sprint-dev` and `quick-fix` — and inappropriate for the orchestration, planning, validation, and practice layers above it.

Two verified findings make the dev-agent integration smaller in scope than initially estimated:

1. **Skill format compatibility is explicit and documented.** ForgeCode's official documentation states: *"Skills are fully compatible with Claude Code. The SKILL.md format is identical — no conversion needed."* This means Momentum skills can be copied directly into `.forge/skills/` with minimal rework — the load-bearing work shrinks to auditing skill prompts for Claude-specific tool references and hook-dependent claims.

2. **Worktree isolation is a first-class ForgeCode primitive** (`--sandbox <name>`). Its existence means ForgeCode and Momentum have the same architectural conviction about worktree-per-agent-work isolation, and it composes cleanly with Momentum's existing per-story worktree pattern in one of two clear configurations.

This analysis recommends proceeding with a dev-agent integration as a bounded ~1-week v1 effort, with the worktree composition resolved in favor of Momentum retaining worktree authority (Option A below). It also recommends borrowing ForgeCode's "sandbox-by-default" architectural primitive into Momentum's own dev-agent conventions regardless of whether Momentum ever runs on ForgeCode — the structural enforcement is a real safety improvement.

## 1. Layer-by-Layer Fit

The Momentum practice layer comprises roughly ten named skills / agent roles. ForgeCode is appropriate for exactly one of them.

| Momentum layer | Purpose | Is ForgeCode appropriate? | Rationale |
|---|---|---|---|
| **impetus** (orchestrator) | Session orientation, workflow dispatch, exclusive-write authority over its own file scopes | No | Needs broad tool access, slash-command dispatch, auto-memory, TeamCreate. ForgeCode's architectural bet is the opposite — single-task containment. |
| **intake** | Classify observations into 6 triage classes; write intake-queue.jsonl | No (poor fit) | Could work mechanically but needs access to the triage taxonomy and the intake-queue event log. No advantage over Claude Code; loses hook-based queue writes. |
| **create-story** | Structured story spec with injected EDD/TDD guidance | No | Depends on Momentum's change-type classifier, mid-generation AVFL, authority-hierarchy rules, sprint-manager state. Heavy orchestration that ForgeCode does not try to do. |
| **sprint-planning** | Story selection, team composition, Gherkin ATDD, activation | No | State-heavy (stories/index.json, sprints/index.json), dependency-graph traversal, multi-output generation. ForgeCode's single-task model is the wrong shape. |
| **sprint-dev** (orchestrator) | Dependency-driven dispatch across stories, post-merge AVFL, team review | No | Needs to spawn parallel dev subagents and coordinate post-merge validation. TeamCreate-style patterns. |
| **dev / dev-frontend / dev-build / dev-skills** | Per-story implementation | **Yes — this is ForgeCode's sweet spot** | Single-task Plan-First-Then-Act is exactly what ForgeCode is designed for. Sage/Muse/Forge maps almost 1:1 onto "explore → plan → implement." |
| **quick-fix** | Single-story flow (define → specify → implement → validate → merge) | **Yes (partially)** | The implement step is a clean ForgeCode fit. The define/specify/validate/merge steps stay in Momentum. |
| **avfl** | Adversarial multi-lens validation | No | Needs structured parallel subagents per lens, consolidator, fixer. ForgeCode's agents do not support this coordination pattern. |
| **retro** | Transcript audit + auditor team dialogue + findings | No | TeamCreate + SendMessage dependency; DuckDB transcript queries; no analog in ForgeCode. |
| **distill / decision / triage / research / assessment** | High-level orchestration skills | No | These are workflow-authored skills with their own phase vocabularies. ForgeCode has no equivalent abstractions. |

The pattern is unambiguous: **ForgeCode fits exactly one Momentum role — the dev agent that executes an individual story.**

## 2. Skill Compatibility — The Big Finding

### What ForgeCode's documentation explicitly claims

From [forgecode.dev/docs/skills/](https://forgecode.dev/docs/skills/) verified 2026-04-22:

> "Skills are fully compatible with Claude Code. The SKILL.md format is identical — no conversion needed."

> "If you already have skills in a Claude Code project, copy them straight into ForgeCode: `cp -r .claude/skills .forge/skills`. They work without any changes."

The skill location hierarchy is `project > agents > global > built-in` — meaning project-local skills at `.forge/skills/<name>/SKILL.md` and user-global skills at `~/.forge/skills/<name>/SKILL.md`. There is no plugin-manager-equivalent — Momentum's current distribution via the Claude Code plugin system (`~/.claude/plugins/cache/momentum/momentum/<version>/skills/`) does not have a direct analog.

### What this means concretely

A Momentum skill like `momentum:dev` can be copied to `.forge/skills/momentum-dev/SKILL.md` (and its `workflow.md`) with no format conversion. ForgeCode auto-discovers skills at session start and applies the relevant one based on the user prompt. The `name` field in frontmatter drives the invocation.

Slash-command invocation: the exact syntax is under-documented in what this research could pull directly. The `:skill` command lists available skills in the session. Per-skill invocation is analogous to Claude Code's slash-command pattern.

### Caveats — the work that is NOT zero

Format compatibility does not mean *behavioral* compatibility. Four caveats to audit before treating skills as drop-in-portable:

1. **Tool references inside skill prompts.** If a Momentum skill prompt says "spawn a subagent via the `Agent` tool" or "create a task list via `TaskCreate`," those tool names do not exist in ForgeCode. The analogs are `task` and `todo_write` respectively. Momentum has other Claude-Code-specific tool references (`SendMessage`, `TeamCreate`, `TaskUpdate`, `ScheduleWakeup`) that have no ForgeCode analog at all — skills that depend on these break silently under ForgeCode.

2. **Hook-dependent claims.** If a Momentum skill says "the PostToolUse hook will commit after each edit," the claim is structurally wrong under ForgeCode (no user-configurable hooks). The skill runs; the hook never fires; the invariant silently breaks. Audit all skill prompts for phrases like "the hook," "will fire on," "PostToolUse," "UserPromptSubmit," etc.

3. **Claude-specific frontmatter fields.** Claude Code's skill frontmatter supports fields like `disable-model-invocation`, `model`, `effort`. Whether ForgeCode honors all of them is not fully documented. Common fields (`name`, `description`) port cleanly. Edge fields may silently no-op.

4. **Plugin-based skill distribution.** Momentum ships via the Claude Code plugin marketplace. ForgeCode has no plugin system; skills live per-project or per-user-global. Momentum-on-ForgeCode requires either mirroring the plugin's skill tree into `~/.forge/skills/momentum/` on install, or copying relevant skills per-project into `.forge/skills/`. A small but real install delta.

### Audit scope estimate

For the dev-agent slice only (the skills Momentum would actually want ForgeCode to host):

- `momentum:dev`, `momentum:dev-frontend`, `momentum:dev-build`, `momentum:dev-skills` — core dev subagent skills.
- `momentum:quick-fix` — if quick-fix's implement step delegates to ForgeCode.
- Skills indirectly invoked by dev agents (e.g., a dev agent might invoke a helper skill mid-task).

The audit: read each skill's `SKILL.md` and `workflow.md` for mentions of `Agent`, `TaskCreate`, `SendMessage`, `TeamCreate`, `PostToolUse`, `PreToolUse`, `UserPromptSubmit`, `ScheduleWakeup`, `hook`, `settings.json`. Flag each occurrence. Translate or document as a break condition.

Rough estimate: the full audit is 1-2 days of reading; the translations are another 1-2 days. Total ~1 week for the audit + translation phase.

## 3. Dev-Agent Integration Shape

### How sprint-dev would dispatch to ForgeCode

1. **Story classification** (existing `create-story` output) gains a `preferred_host: forge` field on stories suitable for ForgeCode execution — typically bulk mechanical edits, scaffolding, boilerplate, CRUD, migration work. Architectural or hook-dependent stories retain `preferred_host: claude-code`.

2. **Dispatch flow in sprint-dev:**
   - Create git worktree (existing pattern — Momentum retains authority over worktree naming, branch creation, cleanup).
   - `cd` into the worktree.
   - Invoke `forge -p "<bootstrap prompt>"` where the bootstrap prompt loads the story.md path and the relevant Momentum rule context.
   - Await completion via filesystem sentinel (cmux-dispatch pattern from the integration-strategy analysis).
   - Read the resulting diff; decide merge / revise / escalate-to-AVFL.

3. **Guidance injection — four layers in combination:**
   - `AGENTS.md` at project root — mirrored from Momentum's `.claude/rules/*.md`. ForgeCode auto-loads this as persistent context.
   - `.forge/agents/momentum-dev.md` — custom agent with tool allowlist matching Momentum's dev subagent conventions and a system prompt encoding Momentum's authoring principles.
   - `.forge/skills/` — the relevant audited Momentum skills (`momentum-dev`, `momentum-dev-frontend`, etc.) copied per-project.
   - Runtime bootstrap prompt — at dispatch time, sprint-dev renders a prompt including story.md, change-type-specific guidance, worktree path, Gherkin acceptance criteria.

4. **Execution shape inside ForgeCode** (this is the value-add):
   - Muse reads the story, explores the codebase, produces a plan file at `.forge/plans/story-{id}.md`.
   - Forge reads the plan, creates a `todo_write` task list.
   - Forge executes each task; `verify_todos` enforces progress tracking; `DoomLoopDetector` catches stuck patterns; bounded-turn caps prevent runaway.
   - On completion, Forge writes a summary to a known path (e.g., `.momentum-dispatch/{story-id}-result.json`) and touches a sentinel file.

5. **Completion handoff back to Momentum:**
   - Sprint-dev detects the sentinel, reads the result summary, inspects the diff.
   - Applies its standard merge / revise / AVFL-escalation logic — unchanged from the native-dev-subagent path.

### What this composition buys

Three concrete benefits:

- **Token-efficient bulk work.** ForgeCode's compact-diff tool-call format combined with cheap-model routing (DeepSeek V3, Qwen3-Coder via OpenRouter) reduces mechanical dev task cost by a factor of ~4x vs Claude Opus, per the Morph token-efficiency analysis referenced in the main research.
- **Structural dev-agent safety.** ForgeCode's tool-allowlist enforcement gives Momentum dev agents a structural safety invariant (cannot write outside scope) that Momentum's current convention-driven approach does not. Harder to drift, easier to audit.
- **Plan-file materialization.** Muse's plan is written to disk before Forge acts. Git-committable, diffable, re-runnable. Momentum's stories have acceptance criteria but the implementation plan today lives in-session context — the materialized plan adds a durable artifact between the story spec and the final diff.

### What this composition does NOT buy

- **No replacement for sprint-dev itself.** Claude Code / Momentum still dispatches, coordinates, and handles merge decisions.
- **No replacement for dev skills with Claude-harness dependencies.** Skills that depend on TeamCreate + SendMessage, ScheduleWakeup, or auto-memory stay on Claude Code.
- **No reduction in Momentum's authoring burden.** Story specs, rules, hooks, AVFL, retro, etc. all remain Momentum-authored.

## 4. Worktree Composition

### What ForgeCode provides

ForgeCode has a first-class `--sandbox <name>` flag. Per the GitHub repo and third-party coverage verified 2026-04-22:

> "`forge --sandbox experiment-name` creates an isolated git worktree and branch, then starts there."

Session-scoped: when the session ends, the worktree persists until manually merged or deleted. The design assumption is "agent work should be sandboxed by default, and the developer should only promote what works." This is a stronger default than Momentum's convention-driven "dev agents should use worktrees" — ForgeCode's version is structural, not convention.

### Composition with Momentum's existing pattern

Momentum's `sprint-dev` already creates a per-story worktree at a sibling path with a story-id-named branch. When sprint-dev dispatches to ForgeCode, there is a choice about which tool owns the worktree.

**Option A — Momentum owns the worktree (recommended).**

```bash
# sprint-dev skill creates the worktree
git worktree add ../story-42 -b story/42-jwt-refactor
cd ../story-42
forge -p "$(cat story.md)"      # no --sandbox
# ForgeCode works in Momentum's worktree; commits to story/42-jwt-refactor
# Sprint-dev reads diff, decides merge / revise / AVFL
```

Advantages:
- Momentum retains worktree-naming, branch-creation, and cleanup authority — existing sprint-dev conventions unchanged.
- Branch naming follows Momentum conventions (`story/{id}-{slug}`).
- ForgeCode operates as a worker inside Momentum's worktree, not as an authoring peer.
- No second layer of isolation to confuse the filesystem.

Disadvantages: requires sprint-dev to create the worktree before invocation (existing behavior; no new code).

**Option B — ForgeCode owns the sandbox (simpler but less controlled).**

```bash
# sprint-dev invokes forge --sandbox directly
forge --sandbox story-42-jwt-refactor
# ForgeCode creates its own worktree at a path of its choosing
# Sprint-dev discovers the path after completion and reads diffs from it
```

Advantages: simpler dispatch (one command, no pre-setup).

Disadvantages:
- Momentum has to parse ForgeCode's sandbox path convention.
- Worktree lifecycle harder to integrate with sprint-dev's existing merge / AVFL flow.
- Branch naming may not match Momentum conventions.
- Loses Momentum's git-discipline authority over worktree management.

### Recommendation

**Option A** (Momentum owns the worktree). The Momentum practice is worktree-authoritative today and should stay that way. ForgeCode's `--sandbox` remains useful as a standalone developer feature — running `forge --sandbox try-something` manually for exploratory work outside sprint-dev's dispatch path — but for sprint-dev dispatch it's cleaner to treat the worktree as Momentum's and ForgeCode as the worker inside it.

### A Momentum primitive worth borrowing

ForgeCode's `--sandbox` default suggests Momentum should make worktree creation **structural** for dev-agent invocations rather than a sprint-dev convention. Concretely: a new `momentum:worktree-dispatch` skill (or an extension of `momentum:dispatch-to-pane`) that refuses to run without a worktree parameter. This adds a structural enforcement invariant to Momentum's current convention-driven practice — the same safety property ForgeCode has built in.

Worth considering as a separate intake story, independent of whether Momentum ever runs on ForgeCode.

## 5. Remaining Gaps and External Mitigations

The one Momentum capability lost by running dev on ForgeCode is **inline hook enforcement** — specifically:

- `PostToolUse` hooks (Momentum's autonomous checkpoint-commit reminder)
- `PreToolUse` hooks (plan-audit, architecture-guard)
- `UserPromptSubmit` hooks (tab rename, context refresh)
- `Stop` hooks (session-end review reminders)

Three mitigation paths:

**Path 1: Accept the gap.** ForgeCode's internal determinism (tool allowlists, `todo_write` enforcement, `DoomLoopDetector`, bounded turns) provides adjacent safety without hooks. For dev agents specifically, this may be sufficient — the loss is manageable. AVFL at the Momentum layer catches what internal determinism misses. **Recommended for v1.**

**Path 2: Hook externally.** Sprint-dev wraps the ForgeCode invocation in a monitor that polls the worktree state and runs hook-equivalent checks at boundaries (after Muse produces the plan, after Forge completes a task, after the whole session ends). Slower feedback than inline hooks but catches most regressions. **v2 if Path 1 proves insufficient.**

**Path 3: Contribute hooks upstream.** The five internal handlers exist in ForgeCode's Rust core (`CompactionHandler`, `DoomLoopDetector`, `PendingTodosHandler`, `TitleGenerationHandler`, `TracingHandler`). Exposing them as a plugin API would be a genuine upstream contribution. **Long-term improvement, not a v1 dependency.**

## 6. Revised Effort Estimate

With skill compatibility verified as native, the v1 scope shrinks to:

| Work item | Estimated effort |
|---|---|
| Skill audit — find Claude-specific tool references and hook-dependent claims across dev skills | 1-2 days |
| Skill translation — replace `Agent` → `task`, `TaskCreate` → `todo_write`, flag hook-dependent sections | 1-2 days |
| `AGENTS.md` mirror of Momentum's `.claude/rules/*.md` | 0.5 day (mostly concatenation + ordering) |
| `.forge/agents/momentum-dev.md` custom agent authoring | 0.5 day |
| `momentum:dispatch-to-forge` skill authoring | 2 days |
| Sprint-dev change-type routing extension | 0.5 day |
| Smoke test — run one story end-to-end through ForgeCode, compare output to native dev subagent | 1 day |

**Total: ~1 week for v1.** Down from the ~2-week earlier estimate, primarily because skill porting is largely a copy operation rather than a rewrite.

The audit is the biggest unknown — until someone actually reads through the dev-skill prompts, the translation scope isn't fully knowable. If any skill has heavy TeamCreate or SendMessage dependencies, that skill may simply not be portable to ForgeCode (stays on Claude Code). That's fine — preferred_host routing handles it.

## 7. Composition With the Other Analysis Documents

This analysis composes with two sibling analyses:

**Integration strategy analysis** ([`integration-strategy-analysis-2026-04-21.md`](./integration-strategy-analysis-2026-04-21.md)) — recommended three-layer integration strategy: process-isolation baseline, cmux-driven autonomous dispatch, MCP only for inline autonomous loops. The ForgeCode dev-agent integration proposed here is an instance of the middle layer (cmux-driven dispatch). The skill `momentum:dispatch-to-forge` is a specialization of the more general `momentum:dispatch-to-pane`.

**Retro → micro-eval loop analysis** ([`retro-microeval-loop-analysis-2026-04-21.md`](./retro-microeval-loop-analysis-2026-04-21.md)) — proposed fixture-based regression testing grown from retro findings. If Momentum runs dev agents on both native Claude Code and ForgeCode, the fixture suite tests skill behavior on both hosts. Cross-host fixture pass rates become a signal for routing decisions — e.g., "story types where ForgeCode dispatch passes reliably" vs "story types where only Claude Code dispatch passes." The two analyses compose: fixtures validate the routing decisions this analysis enables.

## 8. Decision-Ready Framings

### Decision A — Ship a ForgeCode dev-agent integration as a v1 effort

**Framing:** Should Momentum ship a `momentum:dispatch-to-forge` skill + `.forge/` artifacts + sprint-dev routing extension as a one-week v1?

**Recommendation:** Yes. The ROI is concrete (token-efficient bulk work, structural dev-agent safety, plan-file durability), the scope is bounded, and the skill compatibility finding materially reduces the porting effort. The remaining risks (hook gap, audit scope) are manageable via external mitigation and standard audit discipline.

**Evidence:**
- Skill format compatibility is explicit per ForgeCode's own documentation.
- Worktree composition has a clean answer (Option A — Momentum owns the worktree).
- The dev-agent slice is the only Momentum layer where ForgeCode fits — meaning the integration stays narrowly scoped.
- External mitigation for the hook gap (accept internal ForgeCode determinism for v1; add wrappers in v2 if needed) is straightforward.

### Decision B — Worktree composition pattern

**Framing:** Who owns the worktree when Momentum dispatches to ForgeCode — Momentum (Option A) or ForgeCode via `--sandbox` (Option B)?

**Recommendation:** Option A — Momentum creates the worktree, ForgeCode operates inside it without `--sandbox`.

**Evidence:** Option A preserves Momentum's existing worktree conventions (naming, branching, cleanup) and integrates cleanly with sprint-dev's merge / AVFL flow. Option B is simpler dispatch but requires Momentum to parse ForgeCode's sandbox path convention and loses git-discipline authority. The simplicity gain is not worth the coordination loss.

### Decision C — Hook gap mitigation

**Framing:** How does Momentum handle the loss of inline hook enforcement when dev agents run on ForgeCode?

**Recommendation:** Path 1 (accept the gap) for v1. Path 2 (external wrapping) as a v2 contingency if v1 reveals the gap is material. Path 3 (upstream contribution) as a long-term improvement independent of v1.

**Evidence:** ForgeCode's internal determinism (tool allowlists, `todo_write`, `DoomLoopDetector`, bounded turns) provides adjacent safety for the dev-agent use case. AVFL continues running at the Momentum layer to catch what internal determinism misses. The hook gap is real but not load-bearing for dev-agent work specifically.

### Decision D — Borrow ForgeCode's sandbox-by-default pattern into Momentum

**Framing:** Should Momentum make worktree creation structural (via a `momentum:worktree-dispatch` skill or equivalent) rather than a sprint-dev convention, regardless of whether Momentum runs on ForgeCode?

**Recommendation:** Yes, but as a separate intake story independent of the ForgeCode integration.

**Evidence:** ForgeCode's `--sandbox` design embodies the principle "agent work should be sandboxed by default, and the developer should only promote what works." This is a structurally stronger property than Momentum's current convention-driven "dev agents should use worktrees." Adopting the pattern independently gives Momentum the same safety invariant without requiring ForgeCode adoption.

### Decision E — Sequencing across the three open initiatives

**Framing:** Sequencing among the three analyses' proposals: (i) ForgeCode dev-agent integration (this doc), (ii) retro → micro-eval feedback loop, (iii) OpenCode parallel-track experiment.

**Recommendation:**
1. **First: Retro → micro-eval loop skeleton** (just the `momentum:micro-eval` runner + fixture schema; defer retro integration). Small scope (~1 sprint), enables the quality signals for (ii) and (iii).
2. **Second: OpenCode parallel-track experiment.** Smaller than ForgeCode integration because OpenCode reads `.claude/skills/` natively — less work to set up, produces direct evidence on whether Momentum can live off Claude Code at the practice layer.
3. **Third: ForgeCode dev-agent integration.** Benefits from fixtures (from #1) and from the practice-portability learning (from #2). ~1 week for v1.

**Evidence:** Fixtures and quality signals compose across the other two efforts. OpenCode's lower setup cost makes it a faster evidence-gathering experiment than ForgeCode. ForgeCode's dev-agent integration benefits from having the fixture infrastructure to validate routing decisions across hosts.

## 9. Open Questions Deferred to Implementation

- **Which specific dev-skill prompts reference Claude-Code-specific tools or hook-dependent invariants?** Audit scope; unknown until done.
- **Does ForgeCode honor the `model:` and `effort:` frontmatter fields?** Affects whether Momentum's per-role model assignments (Opus for Adversary, Sonnet for Enumerator, Haiku for Consolidator) transfer or need explicit handling in bootstrap prompts.
- **What is the exact slash-command invocation syntax in ForgeCode?** Documentation references `:skill` for listing; per-skill invocation syntax needs verification.
- **How does Momentum's plugin-based skill distribution (`~/.claude/plugins/cache/momentum/`) map to ForgeCode's `~/.forge/skills/` global location?** Install-flow question — likely a small shell script that mirrors or symlinks the plugin's skill tree into `~/.forge/skills/momentum/`.
- **Does ForgeCode's `FORGE_DEBUG_REQUESTS` environment variable provide the transcript capture needed for retro-loop fixture generation?** If yes, fixture capture works identically across Claude Code and ForgeCode. If no, retro's state-reconstruction phase needs host-specific adapters.
- **Data-egress default.** ForgeCode's semantic indexer uploads file content to `api.forgecode.dev` by default unless `FORGE_WORKSPACE_SERVER_URL` is overridden. Before running ForgeCode against the Momentum repo, either override to a local endpoint or self-host the workspace server. Sensitive-code gating worth flagging explicitly.

## 10. Next Steps

1. **Commit and push this analysis** (after developer approval).
2. **Intake five backlog items** for `momentum:intake`:
   - **Story: `momentum:dispatch-to-forge` skill** — v1 as scoped in §6.
   - **Story: `.forge/` artifacts for Momentum** — custom agent, AGENTS.md mirror, skill copies.
   - **Story: sprint-dev change-type routing extension** — `preferred_host` field and dispatch logic.
   - **Story: `momentum:worktree-dispatch` skill** (Decision D, independent of ForgeCode integration) — structural worktree-creation enforcement for dev-agent invocations.
   - **Spike: skill-audit for Claude-specific tool references and hook-dependent claims** — precedes the dispatch-to-forge story; reduces implementation uncertainty.
3. **After fixture infrastructure ships** (per Decision E sequencing), add fixture-based validation to the ForgeCode integration — cross-host pass rates inform routing decisions.

## Sources

Internal:
- [Integration strategy sibling analysis](./integration-strategy-analysis-2026-04-21.md)
- [Retro → micro-eval loop sibling analysis](./retro-microeval-loop-analysis-2026-04-21.md)
- [Consolidated research report](../final/forgecode-agentic-tools-eval-final-2026-04-21.md)
- [Direct ForgeCode repo verification](../raw/verification-forgecode-hooks-and-version.md) — hooks absence + determinism primitives verification against Rust source
- [Practitioner notes](../raw/practitioner-notes.md) — developer decisions on TermBench disclosure, hooks posture, version discrepancy

External (verified 2026-04-22):
- [ForgeCode — SKILL.md documentation](https://forgecode.dev/docs/skills/) — *"Skills are fully compatible with Claude Code. The SKILL.md format is identical — no conversion needed."*
- [ForgeCode — Custom Commands documentation](https://forgecode.dev/docs/custom-commands/)
- [ForgeCode — Plan First, Then Act guide](https://forgecode.dev/docs/plan-and-act-guide/)
- [tailcallhq/forgecode repo](https://github.com/tailcallhq/forgecode)
- [tailcallhq/forgecode/.forge/skills — built-in skills directory](https://github.com/tailcallhq/forgecode/tree/main/.forge/skills)
- [Liran Baba — ForgeCode vs Claude Code comparison with `--sandbox` coverage](https://liranbaba.dev/blog/forgecode-vs-claude-code/)
