---
content_origin: claude-code-subagent
date: 2026-08-24
sub_question: "DEC-035 revisit-clause scoring: out-of-session and multi-Conductor triggers — assembled evidence and verdict"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

## Headline

**Neither DEC-035 revisit trigger has fired.** The corpus establishes that Gas City *would partially support* an out-of-session goal — with two load-bearing gaps still open — and this file's new research establishes that Gas City *can* run concurrent lanes over one rig but was never designed for multiple peer orchestrators: its bundled control-dispatcher is a declared singleton per graph-owning scope, and its one mutual-exclusion primitive (`member_access = "exclusive"`) was **advisory rather than enforcing** until a fix that is still unmerged as of 2026-08-24.

DEC-035 D2's clause is conditioned on a **goal appearing**, not on a capability existing: *"revisit only if/when an out-of-session or multi-Conductor goal appears."* Every fact below is a fact about Gas City. None of them is a fact about Momentum's goals. The corpus was commissioned to *produce the evidentiary basis* for exercising the clause; what it actually produces is the evidentiary basis for **deciding whether to pursue such a goal** — which is the prior question, and Steve's to answer.

## What the clause actually says

DEC-035 D2 (2026-05-30), verbatim:

> Execution substrate = the in-session dynamic Workflow tool. **Gas City is deferred** — this supersedes DEC-032's adoption of Gas City as *the* dispatcher; revisit only if/when an out-of-session or multi-Conductor goal appears.

And its rationale, which is the part that scores the triggers:

> Gas City's sole advantage over dynamic Workflows is out-of-session dispatch, which the developer is explicitly not pursuing yet; in-session it adds maturity tax (Dolt, MCP-not-ready, open wedge/race bugs) for near-zero value and contradicts DEC-030 Gate 1. Beads' headline win — atomic `--claim` against concurrent dispatchers — **only matters out-of-session / multi-Conductor**; for a solo, single in-session Conductor the frontier is trivially computable from `depends_on`.

Two things follow. First, the decision already names the *test*: does the developer want away-from-keyboard dispatch, or more than one Conductor? Second — easily missed — DEC-035 names **beads**, not Gas City, as the thing multi-Conductor would pull in. The multi-Conductor trigger, if it fires, does not automatically point at Gas City; it points at atomic claim semantics, which beads provides on its own gates under DEC-028.

The decision's summary also records the deciding input in the developer's own words: *"high throughput with deep delegation … and explicitly **no out-of-session / away-from-keyboard dispatch yet**."* [OFFICIAL] (`dec-035-conduct-execution-engine-in-session-workflows-2026-05-30.md`, Summary + D2)

## Trigger 1 — Out-of-session: what the corpus says Gas City buys

This section is assembly, not new research. Every claim is cited to a corpus file and section.

**What lands.** Out-of-session cycle dispatch is the one thing Gas City genuinely does that the in-session dynamic Workflow tool cannot:

- **The orchestrator drives the graph outside any agent session**, and an order's timeout covers only initial dispatch — *"compiling the formula, materializing its work beads, and routing them to the pool. … the order timeout never kills work mid-flight."* A conduct phase can therefore run for hours as a formula step [OFFICIAL] (`research-cycle-orchestration-fit.md` §5, §9).
- **Cadence triggers exist**: `cooldown`, `cron`, `condition`, `event`, `manual`, on a 30-second tick [OFFICIAL] (`research-cycle-orchestration-fit.md` §5).
- **Durable parking across days** is a real CLI surface — `gc session wait --sleep --on-beads`, backed by `gc wait list|inspect|cancel|ready`, with the shipped packs' gate prose explicitly defending against idle-reaping [OFFICIAL] (`research-cycle-orchestration-fit.md` §8).
- **Gate blocking works**, reproduced end-to-end on two throwaway cities and two bd versions: a `[steps.gate]` step stays out of `bd ready`, refuses `bd close`, and releases the downstream graph the instant the gate bead closes [EMPIRICAL] (`research-gate-mechanics-handson.md`, Headline, Q1–Q4).
- **Per-phase model tiering and routing are native** — `opt_model` step metadata and `gc.run_target` → `gc.routed_to` [OFFICIAL] (`research-cycle-orchestration-fit.md` §3, §4).
- **The notification substrate exists**: a typed event bus with `bead.created` carrying the full record, payload-level filtering, resumable SSE with cursors, and a writable bead REST surface [OFFICIAL] (`research-notification-watcher-layer.md`, Bottom line).

**What does not land — three load-bearing gaps.**

1. **The notify-the-human reflex is not in a released version.** A formula-cooked gate persists `await_type: null`, and Gas City's bundled human-gate reflexes filter on `await_type == "human"` — so a `type="human"` gate *blocks correctly and tells nobody* [EMPIRICAL] (`research-gate-mechanics-handson.md`, "The defect" / "The notification gap"). The two core-pack orders that would close this (`notify-on-human-gate-creation`, `renudge-stale-human-gates`) landed on `main` 2026-07-23 but ship only in the `edge` rolling pre-release the maintainers label not-for-production; they are in neither v1.4.0 nor v1.4.1. Even with them, the last mile terminates at a `human` mailbox nothing surfaces outside the city [OFFICIAL] (`research-notification-watcher-layer.md`, Bottom line). **For an out-of-session goal this gap is the whole point** — an unnotified gate is indistinguishable from a stalled cycle.

2. **The post-fan-out barrier has no reliable expression.** `waits_for` is inert (#2311), container `needs` does not gate children (#3451), and `[steps.tally]` was removed from the SDK. Momentum's results gate is exactly "wait for all of the conduct fan-out, then ask the human" [OFFICIAL] (`research-maturity-open-bugs.md`, "Momentum-relevant synthesis"). #3451's prescribed workaround — *"enumerate the children explicitly in `needs`"* — is unavailable to Momentum, because the story set is produced at sprint-planning and is runtime-discovered, not known when the formula is authored (`research-maturity-open-bugs.md`, "Container-gate gap #3451").

3. **Push/merge authority has no named gate.** Momentum's own rules require explicit human confirmation before `git push`, and mandate a version bump plus push at sprint completion — an unattended out-of-session cycle collides with both, and the corpus never checked its four HITL gates against them until this fix pass [OFFICIAL] (`research-cycle-orchestration-fit.md` §9b, DOMAIN-A-011). Either a fifth gate on the merge/push step, or an explicit statement that an out-of-session run terminates merged-but-unpushed, is required before this trigger could responsibly fire.

**Cost of entry, for completeness.** Adoption is *"not 'wrap conduct in a formula'. It is 're-express Momentum's phase orchestration as a pack'"* — a rewrite of the orchestration layer with Momentum's skills surviving as the pack payload, priced at **15–25 days** on top of a separate **6–9 day** gate-glue estimate [OFFICIAL] (`research-cycle-orchestration-fit.md` §9; `research-notification-watcher-layer.md` "Glue scope estimate"). Maintainer direction points away from HITL, and Gas City's own leadership reached for a GitHub ruleset rather than their own gate primitive when they needed a hard human gate [OFFICIAL] (`research-production-evidence.md`, Findings 4–5). **[Corrected during AVFL fix pass — the pre-CRIT-004 "does NOT force DEC-028" framing below is superseded.]** Adoption is not free on this axis: the *city's own* store must be bd/Dolt-backed for the `bd gate create`/`--set-metadata` primitives every gate finding in this corpus depends on — `GC_BEADS=file` is alive, documented, and the lightest-start path for a city's *non-gate* work, but the entire `gc bd` verb family is unconditionally blocked on it [OFFICIAL] (`research-beads-coupling-dec028.md`, Bottom Line and §7, resolved by live probe — `research-verification-probes.md` Probes 1–3). This is a narrower, city-scoped Dolt requirement, not a flip of Momentum's own `.momentum/*/index.json` — but it is real, and it **strengthens** this file's NOT-FIRED verdict below: even a fired out-of-session trigger would not get a Dolt-free adoption.

## Trigger 2 — Multi-Conductor: can two lanes run over one rig?

New research. Every claim tagged and sourced.

**Structurally, yes — and it happens by accident today.** The v2 spec is silent on multi-run concurrency: it declares no concurrent-instantiation limit, no serialization or isolation between runs, and no store-contention model, treating concurrency as a deployment concern rather than a formula-contract one [OFFICIAL] ([formula-spec-v2](https://docs.gascity.com/reference/specs/formula-spec-v2), absence of any such clause). What it does declare is that step beads are *"independently Ready-visible and routable"* and that the orchestrator *"drives orchestration outside any agent session"* [OFFICIAL] (same, §0.2/§1.3).

The empirical proof that concurrent workflows coexist over one rig is a bug report, not a feature doc. **#5511** (OPEN, `status/needs-triage`, filed 2026-08-22, v1.4.1) records one `gc sling` call minting **three complete live workflows** on a single rig, because a `bd create --graph` subprocess was killed at its client deadline *after* its Dolt transaction had already committed, and the transient-retry path re-applied the whole plan twice more. The consequence is the decisive sentence for this trigger: *"the pool reconciler spawned **three concurrent workers into the same non-isolated checkout**, which began editing the same files"* [OFFICIAL] ([#5511](https://github.com/gastownhall/gascity/issues/5511)).

**Concurrency controls exist but are the wrong knobs.** `max_dispatches_per_tick` — the field named in the task — *"caps how many orders the supervisor dispatches per tick. Unset keeps the built-in default of 4; set to 1 to drain overdue cooldown orders one-per-tick at cold start instead of firing several concurrent goroutines at once"* [OFFICIAL] (config reference, `[orders].max_dispatches_per_tick`). That bounds **order** dispatch, not concurrent formula runs. The knobs that actually bound concurrent work are session caps: `max_active_sessions` at workspace, rig, and agent level, where *"Nil means unlimited"* at workspace scope, plus `max_wakes_per_tick` (default 5) [OFFICIAL] (config reference). Convergence loops carry their own: `max_per_agent` default 2, and *"City/HQ and each bound rig enforce the limit independently"* [OFFICIAL] (config reference, `[converge]`).

## Trigger 2 — the singleton dispatcher, and what v1.4.0 actually requires

**v1.4.0's control-dispatcher requirement is a fan-out of scopes, not a fan-out of orchestrators.** The release note reads: *"Configure one store-scoped `control-dispatcher` for every graph-owning scope."* Formula control beads route to the dispatcher whose `Dir` matches the city or rig store owning the graph, and *"a rig-owned graph with no matching dispatcher fails before instantiation instead of falling back to a dispatcher that cannot read its work"* [OFFICIAL] ([v1.4.0 release notes](https://github.com/gastownhall/gascity/releases/tag/v1.4.0)). The spec's own framing is singular throughout: *"The orchestrator's control dispatcher processes every open control bead"* by kind [OFFICIAL] (formula-spec-v2 §3).

**The bundled dispatcher is an explicit singleton.** #3964 (OPEN, `kind/bug` `priority/p2`, filed 2026-07-06 against gc 1.3.2/1.3.3) reports that the core pack's `agents/control-dispatcher/agent.toml` ships `max_active_sessions = 1`, which trips Gas City's own advisory: *"max_active_sessions=1 creates a canonical singleton that drains when scale_check returns 0."* In the reporter's 5-rig city the advisory fires six times — once at city scope, once per rig — and the reporter notes *"drain-at-zero is the dispatcher's DESIGNED behavior, so the bundled pack ships a permanent advisory against itself in every city"* [OFFICIAL] ([#3964](https://github.com/gastownhall/gascity/issues/3964)). **This is the direct answer to whether anything in the design assumes a single orchestrator: one control-dispatcher per graph-owning scope, capped at one active session, by design.**

Three corroborating signals that this seam is still settling:

- **#4712** (OPEN, `priority/p3`, updated 2026-08-14): graph.v2 workflow roots are minted HQ-side, so *"the control dispatcher must be HQ-scoped to serve them. If it is not, roots are created and simply never processed, the workflow sits there with nothing obviously wrong."* Getting it right required `env_remove GC_BEADS_PREFIX`, `mode = "always"` on a dispatcher agent patch, and a matching `[[named_session]]` [OFFICIAL] ([#4712](https://github.com/gastownhall/gascity/issues/4712)).
- **#3892** (OPEN): *"control-dispatcher --follow serve loop never quiesces: multi-fork bd ready scan up to 12x/min per dispatcher on a fully idle city"* — per-dispatcher idle cost multiplies with scope count [OFFICIAL] ([#3892](https://github.com/gastownhall/gascity/issues/3892)).
- **#5547 / #5548** (both OPEN, updated 2026-08-23 — one day before this file): *"dispatch: class-bound control work is mis-scoped as rig demand"* and *"resolve class store refs as city control scope."* Dispatcher scoping is being corrected in the current week [OFFICIAL].
- **#4452** (OPEN): *"sweep rig stores from the city control dispatcher"* — another open dispatcher-scoping fix in the same current cluster [OFFICIAL].

## Trigger 2 — `member_access = "exclusive"` does not currently exclude

The spec advertises the primitive the task asked about: a drain's `member_access` is *"`read` (default) or `exclusive` (records a per-member `gc.exclusive_drain_reservation`; fails if another drain owns it)"* [OFFICIAL] (formula-spec-v2 §3, drain key table).

**In the shipped releases that stamp is advisory.** #4587 (OPEN, `kind/bug` `priority/p2` `status/reviewing`, filed 2026-07-23, updated 2026-08-15) documents a production incident in blunt terms: the reservation *"was read only by other drains (`reserveDrainMember`'s owner comparison). Nothing outside `internal/dispatch` consulted it, so a fresh/root formula dispatch … sailed straight past the reservation. Two lanes then drove one anchor (dip-3812vr) concurrently in one shared build tree … Result: duplicate ~450-line implementations, interleaved commits with unreliable git attribution, a mid-edit test captured into a real-Lakebase evidence receipt. **Exclusive did not exclude.**"* [OFFICIAL] ([#4587](https://github.com/gastownhall/gascity/issues/4587))

The fix is written, reproduction-proven (`red → green` by reverting only production code), race/vet/lint-clean, and adversarially reviewed twice — and it is **not merged**. The issue body records *"PR STAGED + HELD on fork for Chris's whole-solution go"*, the issue remains open, and a GitHub PR search for merged work on the exclusive-drain reservation returns only adjacent changes (#4153, CAS conditional writes *adopted at* the drain-reservation site, merged 2026-07-15; #2784, convoy-first drain support, merged 2026-06-01) — never #4587 itself [EMPIRICAL] (`gh api search/issues?q=repo:gastownhall/gascity+is:pr+exclusive+drain+reservation`, queried 2026-08-24; #4587 returns `merged: NOT MERGED`).

Two further limits matter even in the fixed world, stated by the fix's own author: *"Simultaneous-launch TOCTOU. The sling read-only check and the drain scan-then-CAS share no atomic fence, so a genuinely concurrent sling and drain launch (both observing 'clear' in the same instant) can still both proceed. … not full mutual exclusion. A complete fix needs a shared per-member dispatch lock"* [OFFICIAL] (#4587, Remaining Risks 1). And the primitive's scope is narrow regardless: it excludes a competing lane from **the same drain member**. It is not a general orchestrator mutex, and it says nothing about two independent workflows editing the same working tree — which is precisely the failure #5511 exhibits.

## Trigger 2 — multi-city topology on one machine

If "multi-Conductor" is read as "two cities on one box," the current answer is that basic multi-city operation is still breaking, on Steve's exact platform.

- **#4526 [Customer Zero #40]** (OPEN, `kind/bug` `priority/p2`, milestone **1.5** — due 2026-08-04, already past): *"With one city's managed dolt already running, `gc rig add` in a second city on the same machine dies with 'dolt server could not start' (port collision), points at a `dolt.log` that was never written, and leaves the rig half-added."* Environment: gc 1.4 built from source, **macOS Apple Silicon**, observed 2026-07-20. The reporter's own framing: *"Spinning up a scratch city to try a pack next to your real city is the exact registry-era flow 1.4 encourages; it shouldn't fail on rig creation with a misleading pointer."* Suggested fix — per-city dolt port allocation — is not implemented [OFFICIAL] ([#4526](https://github.com/gastownhall/gascity/issues/4526)).
- **#5244** *"fix: recognize dolt port collision messages"* — OPEN, `status/reviewing`, filed 2026-08-13 [OFFICIAL].
- **#3488** *"gc rig add on a keep-split city should provision a per-rig Dolt server (not land the new rig on the city port)"* — OPEN, `priority/p2` [OFFICIAL].
- **#907** *"Hardcoded 'hq' database name prevents multiple cities sharing a remote Dolt server"* — OPEN, `status/stale`, milestone `1.0+`, still updated 2026-08-06 [OFFICIAL].
- Momentum runs on Darwin arm64 [EMPIRICAL] (session environment, 2026-08-24), and milestone 1.5 also carries **#4521** *"Supervisor drift auto-restart broken on macOS — resolves executable via `/proc/<pid>/exe`"* and **#4522** *"gc status probe timeout renders a healthy launchd-managed city as '0/4 agents running'"* [OFFICIAL].

One mitigating note on isolation: Gas City does have per-bead git worktrees and pool `worker_dir` worktrees, with `auto_prune_worker_dir` defaulting true and per-rig disk thresholds (`worktree_rig_warn_size` 10GB, `worktree_rig_error_size` 50GB) [OFFICIAL] (config reference). Worktree isolation is available — but #5511 shows it is configuration, not a guarantee, and the failing case put three concurrent workers in one non-isolated checkout [OFFICIAL].

## Verdict

**Out-of-session trigger: NOT FIRED.** The corpus establishes capability, not goal. DEC-035 records the developer's explicit position — *"no out-of-session / away-from-keyboard dispatch yet"* — and no artifact in this research, in `.momentum/sprints/index.json`, or in any decision since 2026-05-30 records that position changing. What the corpus *does* establish is a qualified "Gas City would support this, with three holes and a cost": the out-of-session dispatch machinery is real and proven (orchestrator drives outside any session; hour-long steps; durable multi-day parking; gate blocking reproduced empirically), while the **notification last mile is unreleased**, the **post-fan-out barrier has no working expression** for a runtime-discovered story set, and **push/merge authority has no named gate** in the corpus's four-gate design. On top of those three gaps, adoption is not Dolt-free either: the city's own store needs a bd/Dolt-backed provider for the gate primitives every finding here depends on — a narrower, city-scoped cost than flipping Momentum's own ledger, but a real one (`research-beads-coupling-dec028.md` §7). Those gaps and that cost sit precisely where an out-of-session goal would put its weight, so even a fired trigger would not yield a clean adoption — it would yield a build.

**Multi-Conductor trigger: NOT FIRED, and the evidence weakens rather than strengthens the case.** Gas City can run concurrent lanes over one rig, but nothing in it is designed for peer orchestrators: the control-dispatcher is a per-scope singleton by bundled configuration, the sole mutual-exclusion primitive was advisory in every shipped release and its fix is unmerged with acknowledged TOCTOU remaining, and the one documented case of concurrent lanes over one anchor produced duplicated 450-line implementations. Note also that DEC-035's own rationale points the multi-Conductor case at **beads' atomic `--claim`**, not at Gas City. If Momentum ever wants two Conductors, the first substrate to evaluate is the one DEC-028 already has a spike for.

**A capability existing is not a goal appearing.** This is the honest statement of what the corpus can and cannot do. The corpus's ten research files cannot fire a clause whose condition is a fact about Momentum's intentions.

## What would have to be true for each trigger to fire

**Out-of-session fires when** Steve wants a cycle to advance while he is away from the keyboard — the concrete shapes being: an overnight autonomous conduct run he reviews in the morning; a cron-triggered triage or refine pass; or a cycle that chains retro → next triage without a human typing a slash command. **[COHERENCE2-A-007]** None of these shapes addresses push/merge authority — see Trigger 1's third gap above and §9b of `research-cycle-orchestration-fit.md`: an overnight run that reaches a push step still needs either a fifth gate or an explicit stop-before-push contract, and this list should not be read as complete without one. The test in DEC-035's own terms is whether removing "typing the slash command" is worth something. It was explicitly worth near-zero on 2026-05-30 ([OFFICIAL], D2 rationale). If it becomes worth something, the *first* question is not "adopt Gas City" but "does the notify-the-human reflex ship in a tagged release, and is #3451 landed?" — because without those, an out-of-session cycle stalls silently and its results gate unblocks early.

**Multi-Conductor fires when** Momentum wants two or more sprint builds executing at once — concurrent epics, or a long conduct run overlapping a quick-fix — such that two dispatchers could claim the same story. That is a real possibility once the story-count cap is gone (DEC-035 D4) and epics get large, but it is a *scheduling* choice Steve has not made. And when it fires, the requirement it generates is **atomic claim over the story frontier**, which today is a `depends_on` computation over `index.json` — solvable by beads' `--claim` (DEC-028, spike open) without importing an orchestrator whose own exclusive-access primitive is unmerged.

**Third possibility worth naming, since neither trigger covers it:** Steve may want Gas City for reasons DEC-035 did not anticipate — the run-centered dashboard shipped in v1.4.0, or the pack ecosystem as a distribution channel for Momentum. Those are not revisit triggers under D2's language. Treating them as such would be re-litigating DEC-035 rather than exercising it, and should go through a fresh decision instead.

## Sources

**Momentum artifacts**
- `_bmad-output/planning-artifacts/decisions/dec-035-conduct-execution-engine-in-session-workflows-2026-05-30.md` — D1, D2, D4, Summary, and the `architecture_decisions_affected` frontmatter carrying the revisit clause [OFFICIAL]
- `docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/scope.md` — corpus goals, including "produce the evidentiary basis for exercising DEC-035's revisit clause" [OFFICIAL]

**Corpus files cited (assembly, Trigger 1)**
- `research-cycle-orchestration-fit.md` §3, §4, §5, §8, §9 — orchestrator-outside-session, order-timeout semantics, cadence triggers, `gc session wait --sleep`, per-phase routing/tiering, adoption-cost characterization
- `research-gate-mechanics-handson.md` — Headline, Q1–Q4, "The defect", "The notification gap" — empirical gate blocking; `await_type: null`
- `research-maturity-open-bugs.md` — "Momentum-relevant synthesis", "Container-gate gap #3451", "Barrier race #2311" — the barrier problem and release/maturity profile
- `research-notification-watcher-layer.md` — Bottom line — event-bus substrate; the two core orders on `edge` only; the `human` mailbox last mile
- `research-production-evidence.md` — Findings 4, 5 — maintainer direction away from HITL
- `research-beads-coupling-dec028.md` — Bottom Line, §7 — `GC_BEADS=file` real for non-gate city work; partial DEC-028 decoupling, not clean — a scoped, city-local Dolt requirement remains for the `bd gate create` primitive
- `research-hitl-alternative-patterns.md`, `research-human-verdict-patterns.md` — Bottom line / Headline — the five HITL mechanisms and their maturity ranking (background)

**Gas City primary sources (new research, Trigger 2)**
- [Formula Specification v2](https://docs.gascity.com/reference/specs/formula-spec-v2) — drain `member_access` key table; control-dispatch prose; `context = separate|shared`; absence of any multi-run concurrency clause. Fetched 2026-08-24; source `docs/reference/specs/formula-spec-v2.md` on `main` via GitHub contents API [OFFICIAL]
- [Config Reference](https://docs.gascity.com/reference/config) — `max_dispatches_per_tick`, `max_active_sessions` (workspace/rig/agent), `max_wakes_per_tick`, `[converge].max_per_agent`, `formula_v2` control-dispatcher routing, worktree reap/prune and size thresholds. Fetched 2026-08-24 via GitHub contents API (`docs/reference/config.md`, 1027 lines) because the rendered page truncates [OFFICIAL] [EMPIRICAL]
- [Gas City v1.4.0 release notes](https://github.com/gastownhall/gascity/releases/tag/v1.4.0) — "Configure one store-scoped `control-dispatcher` for every graph-owning scope" [OFFICIAL]
- [#5511 — transient-retry mints duplicate workflows; one sling produced 3 live workflows](https://github.com/gastownhall/gascity/issues/5511) — OPEN, needs-triage, 2026-08-22, v1.4.1 [OFFICIAL]
- [#4587 — make the exclusive-drain reservation load-bearing across both dispatch entry points](https://github.com/gastownhall/gascity/issues/4587) — OPEN, p2, status/reviewing; "Exclusive did not exclude"; PR staged and held; Remaining Risk 1 TOCTOU [OFFICIAL]
- [#3964 — core pack control-dispatcher self-triggers the singleton advisory](https://github.com/gastownhall/gascity/issues/3964) — OPEN, p2; `max_active_sessions = 1` canonical singleton, fires once per scope [OFFICIAL]
- [#4712 — control-dispatcher HQ scoping for graph.v2 roots is undiscoverable](https://github.com/gastownhall/gascity/issues/4712) — OPEN, p3 [OFFICIAL]
- [#3892 — control-dispatcher --follow serve loop never quiesces](https://github.com/gastownhall/gascity/issues/3892) — OPEN [OFFICIAL]
- #5547 / #5548 — dispatch scoping corrections, both OPEN, updated 2026-08-23 [OFFICIAL]
- [#4452 — sweep rig stores from the city control dispatcher](https://github.com/gastownhall/gascity/issues/4452) — OPEN [OFFICIAL]
- [#4526 — [Customer Zero #40] second city on one machine dies on dolt port collision](https://github.com/gastownhall/gascity/issues/4526) — OPEN, p2, milestone 1.5, macOS Apple Silicon [OFFICIAL]
- #5244 (recognize dolt port collision messages, OPEN/reviewing), #3488 (per-rig Dolt server on keep-split city, OPEN), #907 (hardcoded `hq` database name blocks multiple cities on one remote Dolt, OPEN/stale), #4521, #4522 (macOS supervisor/status breakage, milestone 1.5) [OFFICIAL]
- PR merge-status check: `gh api search/issues?q=repo:gastownhall/gascity+is:pr+exclusive+drain+reservation`, queried 2026-08-24 — #4587 `NOT MERGED`; adjacent merged work #4153 (2026-07-15), #2784 (2026-06-01) [EMPIRICAL]
- Session environment: Darwin arm64 (Darwin 25.5.0), 2026-08-24 [EMPIRICAL]

All Gas City sources verified 2026-08-24 against the live repository and docs; issue states and merge statuses are as of that date.
