---
content_origin: claude-code-subagent
date: 2026-08-21
sub_question: "Cycle orchestration fit: formulas + orders chaining triage→planning→conduct→retro via exec steps running claude -p /momentum:* — harness recipes for Claude Code as the agent runtime"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

## Headline

**The `claude -p` exec-step shape the sub-question assumes does not exist in Gas City, and the maintainers explicitly steer against building it.** A v2 formula step has no `exec` field: steps are work beads that agents claim and execute inside long-lived sessions. The only `exec` surfaces are (a) an **order**-level shell script that runs on the orchestrator with no agent and no pool, and (b) `[steps.check].check.mode = "exec"`, a verification script. Gas City's own `print_args = ["-p"]` provider field — literally `claude -p` — is wired only to `gc prompt synth` and title generation, never to work execution [[OFFICIAL]](https://docs.gascity.com/reference/config).

The shape Gas City *does* offer for Momentum is materially better than the assumed one, and it is the shape the shipped packs already use for BMAD: **Momentum's skills become a pack, its phases become formula steps routed per-step to Claude Code agents, and the human gates become "passive wait + mail" beads.** The cost is that Momentum's skills would have to be re-expressed as formula steps rather than shelled out to — which is a rewrite, not an integration.

## 1. Correcting the premise: no exec step in a v2 formula

The v2 step key table is exhaustive: `id`, `title`, `description`, `description_file`, `notes`, `type`, `priority`, `tags`, `metadata`, `depends_on`, `needs`, `condition`, `children`, `assignee`, `expand`, `expand_vars`, `loop`, `waits_for`, `gate`, `check`, `retry`, `drain`, `on_complete`, `tally`, `timeout`. There is no `exec`, `command`, `run`, or `script` key [[OFFICIAL]](https://docs.gascity.com/reference/specs/formula-spec-v2).

A trap sits right underneath that table: **"Unknown step keys are silently ignored. A typo like `dependson` produces no diagnostic — the dependency simply vanishes."** [[OFFICIAL]](https://docs.gascity.com/reference/specs/formula-spec-v2). So authoring `exec = "claude -p /momentum:triage"` on a step compiles cleanly and does nothing — a silent no-op, not an error. This is the single highest-risk authoring hazard for anyone arriving with the exec-step mental model.

The execution split is normative:

> **The orchestrator executes every control bead.** … No agent participates in control execution.
> **Agents execute only plain work beads.** Step beads are independently Ready-visible and routable, so different steps of one workflow may be worked by different agents, pools, or providers. [[OFFICIAL]](https://docs.gascity.com/reference/specs/formula-spec-v2)

The three places a shell command can legitimately run:

| Surface | Where it runs | Timeout | Agent involved |
|---|---|---|---|
| `[order] exec = "scripts/x.sh"` | orchestrator process | 300s default, capped by `[orders] max_timeout` | no — `pool` is forbidden on exec orders |
| `[steps.check].check.path` | orchestrator, after each attempt closes | `check.timeout` (e.g. `"5m"`), else step `timeout` | no |
| `[order] check = "..."` (condition trigger) | orchestrator, every 30s tick | `check_timeout`, default 10s | no |

All three are bounded, synchronous, orchestrator-hosted probes. A 45-minute `claude -p /momentum:conduct` fits none of them. The condition check is worst: *"The check runs synchronously, so a slow one delays the rest of the tick"* [[OFFICIAL]](https://docs.gascity.com/tutorials/07-orders).

## 2. Where `claude` actually runs: the session, not a subprocess

Gas City runs Claude Code as a **long-lived interactive process in a tmux box**, primed with a prompt template, claiming beads in a loop. Tutorial 03 shows a session's first frames — the rendered prompt landing as the agent's first input, then `gc hook --claim --json`, `bd show`, `bd close` [[OFFICIAL]](https://docs.gascity.com/tutorials/03-sessions).

Two lifecycles [[OFFICIAL]](https://docs.gascity.com/tutorials/03-sessions):

| Flavor | Lifecycle | Declared by |
|---|---|---|
| **On-demand** | spun up to handle slung work, shut down when idle | nothing — the default |
| **Always-on** | kept alive so you can chat anytime | `[[named_session]] mode="always"` in the local pack |

For Momentum, on-demand is the right default for phase workers; always-on suits an Impetus-analogue you talk to. Note the observed cost profile: the always-on mayor had been up 10 hours and was burning nothing — idle sessions do not consume tokens.

Session reaping is the thing that will bite a long `conduct` run. `idle_timeout` is *"the maximum time an agent session can be inactive before the controller kills and restarts it"*, empty by default, and `claim_holder_stall_timeout` enables *"progress-aware recycling of a desired, alive session that holds in-progress work but has stopped making progress"*, clamped to a 5m floor [[OFFICIAL]](https://docs.gascity.com/reference/config). A conduct phase that goes quiet during a long tool call is exactly the case these knobs are tuned against — and the shipped human-gate assets have a purpose-built escape (§6) precisely because idle handling would otherwise recycle a waiting session.

**The one-shot mode exists but is not the work path.** The provider config carries `print_args`: *"CLI arguments that enable one-shot non-interactive mode. The provider prints its response to stdout and exits. … Examples: ["-p"] (claude, gemini), ["exec"] (codex)"* [[OFFICIAL]](https://docs.gascity.com/reference/config). Its consumers in the CLI reference are `gc prompt synth` (*"Spawns a one-shot subprocess of the configured provider; no Gas City agent is involved"*) and `title_model` for title generation [[OFFICIAL]](https://docs.gascity.com/reference/cli). No formula, order, or dispatch path reads it. Gas City knows how to run `claude -p`; it deliberately doesn't run *work* that way.

Corroborating this at the design level, the gascity-packs README instructs pack authors: *"if a raw skill says to spawn a subagent, dispatch a task tool, or invoke a plugin command, the pack should model that work as formula steps, expansion children, drains, or fanout/fanin lanes"* [[OFFICIAL]](https://github.com/gastownhall/gascity-packs/blob/main/README.md). Shelling out to a coding-agent CLI is the anti-pattern the packs exist to replace. A grep of the entire gascity-packs corpus finds **zero** invocations of `claude -p`, `claude --print`, or `codex exec` [[EMPIRICAL]] — `git clone --depth 1 https://github.com/gastownhall/gascity-packs && grep -rn "claude -p\|claude --print\|codex exec" .` returned nothing outside a `.claude/` gitignore line.

## 3. Harness recipe for Claude Code + rig registration

The Claude Code recipe itself is trivially short [[OFFICIAL]](https://docs.gascity.com/guides/harness-recipes):

```toml
# agents/dev/agent.toml — direct, using ambient login / ANTHROPIC_API_KEY
provider        = "claude"
option_defaults = { model = "sonnet" }     # opus · sonnet · haiku · opus-4-7 · fable-5
```

`provider = "claude"` reads `ANTHROPIC_BASE_URL` and `ANTHROPIC_API_KEY` (or `ANTHROPIC_AUTH_TOKEN`). *"Direct usually needs no upstream block at all"* — Gas City passes the ambient environment through. Custom endpoints go through a named `[upstreams.<name>]` with `$VAR` secret refs *"expanded from the controller's environment at launch — never inlined into `city.toml`"*.

Momentum's model-tiering rule maps cleanly: `option_defaults.model` sets a per-agent default, and **per-step `opt_model` metadata overrides it at dispatch** — *"Per-dispatch provider options ride `opt_*` step metadata (for example `opt_model`), validated against the provider's options schema at spawn"* [[OFFICIAL]](https://docs.gascity.com/reference/specs/formula-spec-v2). So Sonnet for triage steps and Fable for the planning step is a two-line metadata change, not a second agent.

**Registering Momentum as a rig** is one command [[OFFICIAL]](https://docs.gascity.com/tutorials/01-cities-and-rigs):

```
$ gc rig add ~/my-project
Adding rig 'my-project'...
  Prefix: mp
  Initialized beads database
  Generated routes.jsonl for cross-rig routing
```

Two consequences matter for Momentum. First, `gc rig add` **initializes a beads database in the rig** — Momentum already has `bd` 1.0.4 with a live dual-write spike, so this is a collision to plan for, not a clean add (the beads-coupling sub-question owns the detail). Second, the default `gc init` template imports a `bd` pack that transitively pulls a `dolt.dog` pool *"from the bundled `dolt` pack … It handles Dolt database housekeeping for the beads backend"* — Dolt arrives whether or not DEC-028 has been decided.

Also note the docs' own maturity caveat: *"the gascity installation … may not be enough to keep up with the changes we're making on the way to 1.0. Best practice right now is to build your own `gc` binary from HEAD"* [[OFFICIAL]](https://docs.gascity.com/tutorials/01-cities-and-rigs) — while the release feed shows **v1.4.1 published 2026-08-15** [[OFFICIAL]](https://github.com/gastownhall/gascity/releases). The tutorial's `gc version 1.1.1` transcript is stale relative to the shipping tag; treat prose version claims in the docs as unreliable.

## 4. How `/momentum:*` reaches the agent — skills, not slash commands

There is no "run this slash command" step construct. The mechanism is **skill materialization plus a description file**.

Packs ship a `skills/<name>/SKILL.md` tree, and `gc` materializes the visible set into the agent's vendor sink: *"inspect the `<scope-root>/.<vendor>/skills/` sink after `gc start`"* [[OFFICIAL]](https://docs.gascity.com/reference/cli). For a Claude Code agent that sink is `.claude/skills/` — the same place Momentum's plugin already lands its skills. The bmad pack does exactly this, shipping `bmad-prd`, `bmad-create-architecture`, `bmad-dev-story`, `bmad-code-review` and six more as pack skills [[EMPIRICAL]] (directory listing of the cloned `gascity-packs/bmad/skills`).

The step then routes to a role and points at prose:

```toml
[[steps]]
id = "plan-review"
title = "Approve implementation plan"
needs = ["plan"]
metadata = { "gc.run_target" = "gc.review-synthesizer" }
description_file = "../assets/workflows/planning-base/plan-review.md"
```
[[OFFICIAL]](https://github.com/gastownhall/gascity-packs/blob/main/gascity/formulas/planning-base.formula.toml)

`gc.run_target` is compile-time routing intent that the router resolves into `gc.routed_to` at dispatch [[OFFICIAL]](https://docs.gascity.com/reference/specs/formula-spec-v2). Momentum's four phases would each carry a different `gc.run_target`, so triage, planning, conduct, and retro can run on different agents, different models, and — if wanted — different harnesses.

**Watch the 4096-byte cliff.** *"Files larger than 4096 bytes are not inlined. The step's description is replaced by a generated pointer that directs the agent to read the file at its resolved path"* [[OFFICIAL]](https://docs.gascity.com/reference/specs/formula-spec-v2). Momentum's skill bodies are far past 4KB, so in practice every step description becomes a pointer and the agent does the reading — workable, but it means the step prose is a *dispatcher* to Momentum's real instructions, not a carrier of them.

## 5. Orders: chaining phases, and the event-trigger limitation

An order pairs a trigger with an action; the orchestrator *"wakes every 30 seconds — a tick — and evaluates each order's trigger"* and rescans the order set *"at most once per minute"* [[OFFICIAL]](https://docs.gascity.com/tutorials/07-orders). Five triggers: `cooldown`, `cron`, `condition`, `event`, `manual`.

**The event trigger is too coarse for "retro-closed fires next triage."** The order's only event field is `on = "<event type>"` — `bead.closed`, `bead.created`, `mail.sent`, `session.woke` [[OFFICIAL]](https://docs.gascity.com/reference/config, [events](https://docs.gascity.com/reference/events)). The `OrderOverride` field list confirms the surface: `enabled`, `trigger`, `gate`, `interval`, `schedule`, `check`, `on`, `pool`, `timeout`, `check_timeout`, `idempotent`, `env` — **no payload matcher** [[OFFICIAL]](https://docs.gascity.com/reference/config). Meanwhile `gc events` *does* have `--payload-match` (e.g. `--payload-match bead.issue_type=task`) [[OFFICIAL]](https://docs.gascity.com/reference/events). The filtering exists on the observation side and is absent on the trigger side. An `on = "bead.closed"` order therefore fires on *every* closed bead in the city.

Two workable substitutes:

1. **`condition` trigger with a selective check** — `check = "scripts/retro-closed.sh"`, exit 0 when the retro workflow root is closed and the next cycle hasn't started. This is precise, but runs synchronously inside the 30s tick under a `check_timeout` defaulting to 10s, and *"a check killed by its deadline never proves its condition, so the order would otherwise silently never fire."*
2. **Let the graph do it** — put the phases in one workflow so `needs` handles sequencing, and use an order only for the outer cadence.

Also relevant to chaining: **duplicate prevention fails closed.** *"Before dispatching, the orchestrator checks whether the order already has open (non-closed) work. If it does, the order is skipped even when the trigger says it's due"* — and if the store read times out the order is skipped [[OFFICIAL]](https://docs.gascity.com/tutorials/07-orders). For a Momentum cycle whose whole point is a single in-flight sprint, this default is a feature.

**Order timeouts do not bound the work.** *"For formula orders, the timeout covers only the initial dispatch — compiling the formula, materializing its work beads, and routing them to the pool. Once dispatched, the orchestrator drives a v2 formula's steps to completion at each agent's own pace; the order timeout never kills work mid-flight"* [[OFFICIAL]](https://docs.gascity.com/tutorials/07-orders). This is the decisive answer to the sub-question's timeout worry: **a phase can take hours, as long as it is a formula step rather than an exec order.** The default 30s formula-order timeout only has to cover compilation and routing.

`max_dispatches_per_tick` defaults to 4 [[OFFICIAL]](https://docs.gascity.com/reference/config) — a non-issue at Momentum's one-cycle-at-a-time volume.

## 6. One formula spanning phases, or one per phase? The shipped answer is: one composed formula

The bundled packs answer this decisively — **one formula spanning the whole cycle, assembled from per-phase bases via `extends`.** The gascity pack's build pipeline is *"a chain of `extends` bases — a `prepare → requirements → plan → plan-review → decompose → implement → review → finalize → publish` flow assembled across `build-base` and the `build-from-*-base` family"*, and the dispatched entrypoint `build-from-convoy` is *"21 lines with no `[[steps]]`"* [[OFFICIAL]](https://docs.gascity.com/guides/understanding-formulas).

The composition rule that makes phase-splicing work: *"a child's steps are appended to the parent's, but a child step that reuses a parent step's `id` overrides it in place, keeping its position"* — a descendant redeclares an inherited step id with a new `needs` list and the inserted steps land before it [[OFFICIAL]](https://docs.gascity.com/guides/understanding-formulas).

Momentum's triage→planning→conduct→retro maps onto this almost one-for-one, and BMAD is already mapped: `bmad-build` `extends = ["build-base"]` and swaps in `bmad-planning`, `bmad-decomposition`, `bmad-implementation`, `bmad-review`, `bmad-fix-loop` through vars, with a `bmad.readiness-reviewer` `implementation-readiness` step in the middle [[OFFICIAL]](https://github.com/gastownhall/gascity-packs/blob/main/bmad/formulas/bmad-build.formula.toml).

**Two composition warnings.** First: *"The formula resolved through `extends` drops `advice` and `pointcuts` entirely — including the child's own. And when both parent and child declare `compose` rules, the merge keeps only `bond_points`, `hooks`, `expand`, and `map`; `branch`, `gate`, and `aspects` rules from both sides are dropped"* [[OFFICIAL]](https://docs.gascity.com/reference/specs/formula-spec-v2). Second, `[requires]` composes as a safety constraint — every parent's constraint is collected, and non-overlapping sets fail before durable work is written.

The one-formula-per-phase-chained-by-orders alternative is *possible* but loses the graph: no `needs` edges across phases, no shared workflow root metadata, no `workflow-finalize`, and each order's own duplicate-prevention gate to reason about independently. Nothing in the docs or packs models a cycle that way.

## 7. Accepted-but-inert caveats that hit this shape

Spec §4 is explicitly *"accepted by the parser and compiler but have **no runtime consumer** in the current release"* [[OFFICIAL]](https://docs.gascity.com/reference/specs/formula-spec-v2). Three of the four land on Momentum's plan:

- **Gate `type` vocabulary is inert.** `[steps.gate]` *does* synthesize a real gate bead that blocks its step until closed — but the type values `gh:run`, `gh:pr`, `timer`, **`human`**, and `mail` *"are doc-comment vocabulary … the parser never validates them and no bundled watcher acts on them. Zero bundled formulas use `gate`."* So `type = "human"` conveys nothing to the runtime; the blocking is real, the semantics are decoration. (My grep of gascity-packs confirms: zero `[steps.gate]` and zero `waits_for` occurrences across all 20+ packs [[EMPIRICAL]].)
- **`waits_for` gate modes are inert** — the `all-children` / `any-children` distinction has no dispatcher consumer.
- **Until-loops run exactly once** — *"An `until` loop therefore runs exactly one iteration. Use `check` (section 3.1) for orchestrator-driven re-execution."*
- **`vars.<name>.type` is parsed but never enforced** — only `required`, `enum`, `pattern` are validated.

Two more gaps from §5 that bear on a phase-spanning formula:

- **`gc converge` rejects v2 formulas** outright: *"convergence wisps do not support v2 formula … use a v1 formula until convergence has an explicit input convoy target."* Iterate-until-verified in v2 means `[steps.check]`, nothing else.
- **Container dependencies do not gate on children** ([#3451](https://github.com/gastownhall/gascity/issues/3451)) — *"the v2 compiler creates no parent-child edges, so the same dependency gates only on the parent step itself. … until it lands, enumerate the children explicitly in `needs`."* A Momentum "conduct" phase that decomposes into per-story children must enumerate them, or "retro needs conduct" will unblock while stories are still open. This is the most dangerous silent-wrong-behavior gap for the cycle shape.

## 8. The gate pattern the packs actually ship: passive wait + mail

Since `[steps.gate]` is unused in production, the shipped human gate is an **ordinary work bead whose description tells the agent to park and wait**. The pattern appears verbatim in at least two packs — `gascity/assets/workflows/github-pr-review/human-gate-comment.md` and `superpowers/assets/workflows/superpowers-brainstorming/{target}.confirm-design-approval.md` [[OFFICIAL]](https://github.com/gastownhall/gascity-packs/blob/main/gascity/assets/workflows/github-pr-review/human-gate-comment.md):

1. Stamp workflow-root metadata `…_gate=waiting-human`, `…_gate_bead_id=<this bead>`.
2. Park the session so idle handling doesn't recycle it:
   ```bash
   gc session wait "$SESSION_TARGET" --sleep --on-beads "$GC_BEAD_ID" \
     --note "Waiting for human approval … Resume with: gc session attach $SESSION_NAME"
   ```
3. Send **exactly one** `gc mail send human …` with artifact paths, root id, bead id, and the response options (approve / request changes / reject), then set `…_gate_mail_sent=true`.
4. *"Wait for explicit human feedback … If the session idles, detaches, or restarts before the human responds, do not close this bead."*
5. Record exactly one terminal value: `approved`, `rejected`, or `revision_requested`. *"Close fail only for explicit rejection or abort, not for silence."*

`gc session wait` is a real CLI surface with `--on-beads`, `--any`, `--sleep`, `--note`, backed by durable waits (`gc wait list|inspect|cancel|ready`) [[OFFICIAL]](https://docs.gascity.com/reference/cli). This directly answers "does a phase step survive a human taking two days to review": yes, by design, and idle-reaping is explicitly defended against.

The complementary posture var is `interaction_mode` — `interactive` / `autonomous` / `headless`, described as *"human participation in planning and gates"* [[OFFICIAL]](https://github.com/gastownhall/gascity-packs/blob/main/README.md). In `headless` the gate prose says: *"never ask questions and stop blocked with a machine-readable `gc.blocked_reason` when approval input is missing."* Note the trap for Momentum: `review_mode = "interactive"` is **agent authority level** ("safe plan fixes may be applied directly"), not human involvement — those are two different axes with confusingly overlapping vocabulary.

## 9. Fit assessment against Momentum's cycle

| Momentum need | Gas City fit | Evidence |
|---|---|---|
| Out-of-session cycle chaining | **Strong.** v2 workflow driven by the orchestrator *"outside any agent session"*; order timeout never kills dispatched work | v2 spec §0.2, orders tutorial |
| Long-running phase (conduct) | **Strong as a step; broken as an exec order.** 300s exec cap vs. unbounded step | orders tutorial |
| Per-phase model tiering | **Native.** `opt_model` step metadata | v2 spec §2 |
| Per-phase agent/role routing | **Native.** `gc.run_target` → `gc.routed_to` | v2 spec §2 |
| HITL gates (plan gate, results gate) | **Works, but as convention not construct.** Passive wait + mail; `[steps.gate]` type vocab inert | packs assets; v2 spec §4 |
| retro-closed → next triage | **Weak as an event trigger** (no payload filter); use `condition` or one workflow | orders tutorial; config reference |
| `claude -p /momentum:<skill>` exec steps | **Not available, and steered against** | v2 spec §1.3; packs README |
| Reusing Momentum skills as-is | **Partial.** Skills materialize into `.claude/skills/`; step prose points at them; >4KB descriptions become pointers | `gc skill`; v2 spec §1.8 |
| conduct's per-story fan-out feeding a retro gate | **Hazard.** #3451 — parent `needs` does not gate on children | v2 spec §5 |

**The honest characterization of adoption cost:** this is not "wrap conduct in a formula." It is "re-express Momentum's phase orchestration as a pack," which is precisely what the bmad/superpowers/gstack packs are — each one a vendored methodology re-modeled as formula steps, expansions, drains, and fanout lanes. That is a real and proven path (five methodologies have walked it), and it is a rewrite of the orchestration layer, with Momentum's skills surviving as the pack's `skills/` payload.

**Rewrite-scope estimate (added during AVFL fix pass — MAJ-014).** The corpus prices the *gate glue* (~6–9 days, `research-notification-watcher-layer.md` "Glue scope estimate") but had left the orchestration rewrite itself unpriced. Using the five methodologies that walked this exact path as a size proxy — their formula + asset file counts, from this document's own §6/§9 sources and the `gascity-packs` repository structure:

| Methodology pack | Formula files | Notable asset scope |
|---|---|---|
| `bmad` | `bmad-build.formula.toml` `extends`-composed from `build-base` plus `bmad-planning`, `bmad-decomposition`, `bmad-implementation`, `bmad-review`, `bmad-fix-loop` — 6+ formula files | `skills/` tree with 10 pack skills (`bmad-prd`, `bmad-create-architecture`, `bmad-dev-story`, `bmad-code-review`, +6 more) plus workflow assets |
| `gascity` (core methodology pack) | `build-basic-review.formula.toml`, `planning-base.formula.toml`, `build-basic.formula.toml`, plus the `build-from-*-base` family | `assets/workflows/` prose per phase; multiple `assets/scripts/checks/*.sh` |
| `superpowers` | brainstorming/design-approval formula + workflow assets | `{target}.confirm-design-approval.md`-style per-target workflow prose |
| `gstack` | `gstack-build` formula family | `qa.md`, `plan-review.md` prompt assets |
| `pr-pipeline` / `contributing` | `mol-pr-start.formula.toml`, `mol-contributing-plan-implementation.formula.toml` | scorecard + gate prose assets |

Momentum's own cycle has four phases (triage, planning, conduct, retro) plus four HITL gates — comparable in shape to `bmad`'s build-base chain (`prepare → requirements → plan → plan-review → decompose → implement → review → finalize → publish`), which is the closest existing analogue at ~6 formula files plus 10 pack skills and their workflow assets. **Combined estimate: the orchestration rewrite is materially larger than the gate glue** — on the order of **15–25 days** to re-express triage/planning/conduct/retro as formula steps with per-phase `gc.run_target` routing, migrate Momentum's skill bodies into a pack's `skills/` tree (working around the 4096-byte description-file pointer cliff, §4), and re-derive the fan-out/barrier shape for conduct→retro against the #3451 container-gate gap (§7) — **on top of**, not instead of, the ~6–9 day gate-glue estimate. This is a rough sizing from analogous pack scope, not a bottom-up estimate; treat it as an order-of-magnitude floor for the go/no-go, not a committed number.

## 9a. What happens when a gate is never resolved (added during AVFL fix pass — DOMAIN-A-009)

The corpus never composed this failure mode in one place, even though the pieces sit in three different files and, assembled, describe a cycle that stops **permanently and silently** — with one of those files calling part of the mechanism "a feature."

**The composed sequence:** (1) §5 above: *"Before dispatching, the orchestrator checks whether the order already has open (non-closed) work. If it does, the order is skipped even when the trigger says it's due"* — glossed here as a feature for Momentum's single-in-flight-sprint case. (2) `research-gate-mechanics-handson.md`: a formula-cooked gate has no persisted `timeout`, so *"every gate a formula creates is a permanently-manual gate"* (framed there as *fail-safe*). (3) Per DOMAIN-A-005/notification findings elsewhere in this corpus, no tagged release notifies on a human gate, and even the vendored renudge order filters on `await_type == "human"`, which formula gates never set. **Composed:** an unresolved gate leaves its order's work open → the order that would chain to the next phase is skipped every tick, indefinitely → the cycle stops → nothing tells anyone. `research-maturity-open-bugs.md` names exactly this signature for the *wedge* bug class — *"the failure mode of this class is silence … cycle stalls will look identical to 'nothing was due.' Any adoption needs an external liveness check"* — but that prescription was never extended to the unresolved-gate case specifically, even though the mechanism is structurally the same (an order silently not firing).

**Prescription:** the external-liveness-check recommendation from the wedge-bug finding should be read as covering unresolved gates too. Concretely, a Momentum-side sweep of `bd gate list --status open` with an age threshold, run independently of any `gc order` (so it survives even a fully-wedged dispatcher), closes this gap. This is a different mechanism from the notify/renudge orders (§ elsewhere in this corpus) — those tell the human a gate exists; this tells *Momentum's own tooling* that a cycle has stalled, which matters for an out-of-session goal where nobody is watching the clock.

## 9b. Push/merge authority under out-of-session orchestration (added during AVFL fix pass — DOMAIN-A-011)

The corpus proposes chaining triage→planning→conduct→retro out of session with human gates at four named points, and — corpus-wide, across all 9 original files — never addresses two binding Momentum rules that an unattended cycle collides with: `git push` always requires explicit approval (`~/.claude/rules/git-discipline.md`: *"`git push` always requires explicit user confirmation"*), and sprint completion mandates a version bump plus push (`.claude/rules/version-on-release.md`). Momentum's conduct phase performs worktree→sprint-branch merges autonomously already, but terminates at a step — pushing the merged sprint branch — that by rule cannot run unattended.

**The gap concretely:** the corpus enumerates four HITL gates (triage, plan, mid-story tooling, results) where Momentum's own rules imply a **fifth** — a push/merge-authority gate — for any cycle that is meant to run without a human present to type `git push` and confirm it. This is not a Gas City limitation; it is a Momentum policy the corpus's out-of-session framing did not check against.

**Resolution options, either of which closes the gap:**
1. **A fifth gate** on the merge/push step, structurally identical to the other four `bd gate --type=human` gates this corpus recommends, blocking specifically on push confirmation.
2. **An explicit statement that the cycle terminates before push** — i.e. an out-of-session run produces a merged-but-unpushed sprint branch and hands off to the developer for the push step alone, rather than attempting end-to-end autonomy through publish.

Either is compatible with everything else in this corpus; neither was specified. Any synthesis or decision document built on this research should pick one explicitly rather than let it default silently.

## 10. Open questions for hands-on validation

1. **Does a Claude Code session survive a multi-hour step without `idle_timeout` firing?** Docs say `idle_timeout` is empty by default, but `claim_holder_stall_timeout` (5m floor) exists specifically to recycle stalled claim-holders. Untested here — `gc` was not installed on this machine during this sub-question's own research session (2026-08-21) [[EMPIRICAL, at that time]] (`which gc` → not found). **Environment note (MIN-005, added during AVFL fix pass):** a later probe session (2026-08-24) installed `gc` 1.4.1 globally and exercised it live in a throwaway city (`GC_BEADS=file`, no live formula run) — see `research-verification-probes.md`. That session did not run a multi-hour step or exercise `idle_timeout`/`claim_holder_stall_timeout`, so this specific open question remains genuinely open; only the "gc is not installed at all" framing is stale.
2. **Does `gc session wait --sleep` actually keep a Claude Code session parked**, and does an attach/nudge resume it into the same conversation? The packs' prose assumes yes; no doc states the guarantee.
3. **Does a `condition`-triggered order reliably fire within its 10s `check_timeout`** against a rig store also serving a live sprint?
4. **What does #3451 mean concretely for a drain-shaped conduct phase** feeding a results gate — does `needs = ["conduct"]` unblock early in practice?
5. **Whether `[steps.gate]`'s real blocking behavior is enough** for Momentum's gates without any watcher, given the type vocabulary is decorative. (Owned by the gate-mechanics sub-question.)

## Sources

- [Harness Recipes](https://docs.gascity.com/guides/harness-recipes) — fetched as `.md`, 2026-08-21; page lastmod 2026-08-07
- [Formula Specification v2](https://docs.gascity.com/reference/specs/formula-spec-v2) — lastmod 2026-08-19
- [Tutorial 03 — Sessions](https://docs.gascity.com/tutorials/03-sessions)
- [Tutorial 07 — Orders](https://docs.gascity.com/tutorials/07-orders)
- [Tutorial 01 — Cities and Rigs](https://docs.gascity.com/tutorials/01-cities-and-rigs)
- [Understanding Formulas](https://docs.gascity.com/guides/understanding-formulas) — lastmod 2026-08-11
- [Configuring an Agent](https://docs.gascity.com/guides/configuring-an-agent)
- [Config Reference](https://docs.gascity.com/reference/config) — lastmod 2026-08-15
- [CLI Reference](https://docs.gascity.com/reference/cli) — lastmod 2026-08-20
- [gc events Output Formats](https://docs.gascity.com/reference/events)
- [Exec Session Provider](https://docs.gascity.com/reference/exec-session-provider) — lastmod 2026-08-19
- [Set Up a Multi-Agent Engineering Environment](https://docs.gascity.com/guides/multi-agent-engineering-environment)
- [gascity-packs README](https://github.com/gastownhall/gascity-packs/blob/main/README.md)
- [planning-base.formula.toml](https://github.com/gastownhall/gascity-packs/blob/main/gascity/formulas/planning-base.formula.toml)
- [bmad-build.formula.toml](https://github.com/gastownhall/gascity-packs/blob/main/bmad/formulas/bmad-build.formula.toml)
- [human-gate-comment.md](https://github.com/gastownhall/gascity-packs/blob/main/gascity/assets/workflows/github-pr-review/human-gate-comment.md)
- [superpowers confirm-design-approval.md](https://github.com/gastownhall/gascity-packs/tree/main/superpowers/assets/workflows/superpowers-brainstorming)
- [gascity releases](https://github.com/gastownhall/gascity/releases) — v1.4.1 published 2026-08-15
- [gascity issue #3451](https://github.com/gastownhall/gascity/issues/3451) — container dependencies do not gate on children (cited by the v2 spec)

All sources current as of 2026-08-21; every doc page carries a sitemap `lastmod` within the past six weeks. No source older than two years was used.

**Corpus cross-references (added during AVFL fix pass)**
- `research-verification-probes.md` — live gc 1.4.1 probes, 2026-08-24 [[EMPIRICAL]]
- `research-gate-mechanics-handson.md` — gate `timeout` persistence, notification filter [[EMPIRICAL]]
- `research-maturity-open-bugs.md` — wedge-bug silence signature, #2311/#3451 barrier status [[OFFICIAL]]
- `~/.claude/rules/git-discipline.md`, `.claude/rules/version-on-release.md` — Momentum push/version-bump rules (DOMAIN-A-011) [local project artifacts]
