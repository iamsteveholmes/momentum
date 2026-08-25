---
content_origin: claude-code-subagent
date: 2026-08-21
sub_question: "Maturity and open bugs: O3 status; wedge bugs #2131/#2168, barrier race #2311, container-gate gap #3451; release cadence and v1→v2 breaking changes since May 2026"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

## Headline

Gas City is shipping fast and is actively maintained, but **every mechanism Momentum would need to express a human gate at the end of a fan-out phase is either open, inert, or explicitly deferred.** The `[steps.gate]` construct produces a real blocking bead (usable), but its `type` vocabulary — including `human` — has *no runtime consumer* (#4399, open, P3, unowned). The barrier that would make a gate wait for a phase's children is broken two different ways: `waits_for = "children-of(X)"` does not gate readiness (#2311, open, no fix PR since 2026-05-29), and formulas-v2 `needs` on a parent does not gate its children (#3451, open, maintainer ruling 2026-06-28, "implementation tracking to follow" — still not landed as of 2026-08-21). The first-class HITL design (Orchestration v3, #1709) is written but unscheduled: no milestone, tracker stale since 2026-06-09. The two dispatcher-wedge bugs (#2131, #2168) are genuinely fixed and closed in the v1.2 window.

Verdict for Momentum: **structural gates are buildable today; typed/automatic gates and phase-barrier semantics are not.** Anything Gas City orchestrates for Momentum must express "wait for all of phase N, then ask the human" using `drain` + a check loop, not `waits_for` and not container `needs`.

---

## Project shape and release cadence (May–August 2026)

`gastownhall/gascity` is a Go, MIT-licensed repo created 2026-02-22, described as an "Orchestration-builder SDK for multi-agent coding workflows," 371 forks, ~1.76 GB checkout, last push 2026-08-22 [OFFICIAL] ([gh repo view](https://github.com/gastownhall/gascity)).

Release history since 1.0.0 (2026-04-21) [OFFICIAL] ([releases](https://github.com/gastownhall/gascity/releases)):

| Version | Date | Kind |
|---|---|---|
| v1.1.0 | 2026-05-06 | minor |
| v1.2.0 | 2026-05-29 | minor (breaking) |
| v1.2.1 | 2026-06-01 | hotfix |
| v1.3.0 | 2026-06-18 | minor (breaking) |
| v1.3.1 / v1.3.2 | 2026-06-19 / 06-22 | patch |
| v1.3.3 / v1.3.4 / v1.3.5 | 2026-07-02 / 07-10 / 07-14 | patch |
| v1.4.0 | 2026-07-24 | minor (breaking) |
| v1.4.1 | 2026-08-15 | patch (latest) |
| `edge` | rolling, tagged 2026-06-27 | rolling-main pre-release channel |

That is **11 releases in ~14 weeks — roughly one every 9–10 days, with four minor bumps in 3.5 months**, three of which carried a Breaking Changes section. This is a fast-moving pre-2.0-behaviour project despite the 1.x version string.

Commit activity is high and steady: weekly commit counts for the trailing 12 weeks are `[307, 189, 286, 99, 85, 106, 236, 251, 123, 148, 88, 93]` — mean ~168/week, no collapse [OFFICIAL] (`gh api repos/gastownhall/gascity/stats/participation`) [EMPIRICAL]. **2,402 pull requests merged since 2026-05-01** [OFFICIAL] (GitHub search API, `is:pr is:merged merged:>=2026-05-01`) [EMPIRICAL].

Issue hygiene is the weaker signal: **575 open issues** (query method fixed during AVFL fix pass — MAJ-004: this is the GitHub **search API** count, `is:issue is:open`, issues only, excluding PRs) against **380 issues closed from the May-onward cohort** [EMPIRICAL] (GitHub search API, 2026-08-21). Other files in this corpus report **1,011 open issues** — that is the `repos/…/open_issues_count` **repo-endpoint** figure, which bundles open issues *and* open PRs together; see `research-notification-watcher-layer.md` and `research-production-evidence.md`, and `avfl-consolidated.md` MAJ-004 for the full reconciliation. The two figures are not in conflict — they count different things — but neither document originally stated its method, so a reader could not tell. **[Comparison annotated during AVFL fix pass — DOMAIN3-A-005.]** Merge velocity outruns issue closure on the numbers above, but that comparison is **mixed-population** and must not be read as a like-for-like ratio: it sets 2,402 PRs merged since 2026-05-01 against 380 issues closed from that same May-onward cohort, while the 575 open figure is all-time. `research-production-evidence.md` struck exactly this mixed comparison under ACC-002. The **like-for-like** issue comparison is **575 open vs 718 closed — both all-time, both issue-only on the search API** — on which closed exceeds open by 143, and "intake outpaces resolution" does not hold. **Query-method hedge on the 718, propagated at iter4 (ACCURACY4-A-004) from `research-production-evidence.md`:185:** the raw query string was *not recorded* when the 718 count was taken. The `is:issue is:closed` all-time, PRs-excluded basis is stated as the method the like-for-like arithmetic *requires* (it is what makes 575 + 718 = 1,293 the issue-only corpus total), **not** as a re-run that was observed and logged. Read "both issue-only on the search API" as verified for 575 and inferred-from-arithmetic for 718. The `1.5` milestone (due 2026-08-04, already past) holds 11 open / 3 closed, dominated by a "Customer Zero" dogfooding series (#4362, #4365, #4519–#4526) recording real operator breakage — dolt port collisions on a second city, `gc status` probe timeouts misreporting healthy cities, macOS supervisor drift auto-restart broken [OFFICIAL] ([milestone 1.5 search](https://github.com/gastownhall/gascity/milestones?q=1.5) — ellipsis placeholder replaced during AVFL fix pass, STRUCTURAL-A-009; a search URL is used rather than a guessed numeric milestone id, since the id was not independently re-confirmed). That series is a good-faith maturity signal (they are eating their own dog food and filing) and simultaneously a warning (basic multi-city and macOS operation is still breaking in August).

### Contributor distribution (stars deliberately ignored)

The GitHub `stats/contributors` endpoint never finished computing across five retries (repo too large), so distribution was derived directly from the commit log [EMPIRICAL]:

| Window | Sampled commits | Top author | 2nd | Top-2 share |
|---|---|---|---|---|
| 2026-05-01 → 2026-07-01 | 600 | `julianknutsen` 52.2% | `quad341` 17.3% | **69.5%** |
| 2026-07-01 → 2026-08-21 | 1000 | `julianknutsen` 51.8% | `quad341` 14.5% | **66.3%** |

Long tail in the May–June window: `csells` 6.2%, `sjarmak` 5.8%, `iwata-1116` 3.5%, `bourgois` 2.8%, then ~15 contributors under 1.5% each. **Bus factor ≈ 1–2.** One engineer authors more than half of all commits, consistently across both windows. **[Cross-reference, COHERENCE2-A-010]:** `research-production-evidence.md` Finding 7 reports a higher **66.2%** all-time share for the same top author — not a contradiction, a different measure: this table samples recent commit windows (600–1000 commits each), while production-evidence's figure is cumulative over the repo's full 5,437-commit history. Both point the same direction (bus factor ≈1–2); read them as windowed-vs-cumulative, not as disagreeing counts. That is a real adoption risk for a dependency Momentum would put at the top of its cycle. (A search snippet claims a public Gas City dashboard showed non-maintainers authoring 32.1% of merged human PRs in the 30 days to 2026-08-07 — [UNVERIFIED], the dashboard URL was not fetched and the figure counts PRs, not commits.)

---

## v1 → v2 formula contract: migration state

**v2 is not "the version you get by default" — it is the recommended contract that every formula must opt into individually.** Two independent switches exist [OFFICIAL] ([formula-spec-v2 §5](https://docs.gascity.com/reference/specs/formula-spec-v2), file last modified 2026-08-19):

| Declaration | Where | Status |
|---|---|---|
| `[requires] formula_compiler = ">=2.0.0"` | formula TOML | **canonical v2 opt-in** |
| `contract = "graph.v2"` | formula TOML | deprecated; `gc doctor` warns |
| `[daemon] formula_v2` | `city.toml` | host switch, **default `true`** |

Since v1.3.0, `gc init` no longer writes the `[daemon] formula_v2` line because "Formula v2 is on by default"; `formula_v2 = false` (and its deprecated alias `graph_workflows = false`) are still honored [OFFICIAL] ([v1.3.0 release notes](https://github.com/gastownhall/gascity/releases/tag/v1.3.0)). But an undeclared formula still compiles under **v1 semantics** (compiler capability 1.0.0), and graph-only constructs fail validation:

> `requires: formulas that use graph-only constructs must declare [requires] formula_compiler = ">=2.0.0" or the deprecated contract = "graph.v2" explicitly` [OFFICIAL]

Graph-only constructs requiring the declaration: `check`, `retry`, `drain`, `on_complete`, and reserved `gc.*` step metadata. The authoring guide states plainly: *"For new work, choose v2. The opt-in is one table."* [OFFICIAL] ([understanding-formulas](https://docs.gascity.com/guides/understanding-formulas))

**v2 is explicitly not a strict superset of v1.** The spec intro on `main` still says so, naming two gaps: `gc converge` accepts only v1 formulas, and the container-dependency gap #3451 [OFFICIAL].

### Deprecations and removals that bite

- **`gc.output_json` (authored fan-out) is deprecated in v2.** `gc lint` warns: `gc.output_json is deprecated; use drain in v2 formulas (see: engdocs/drain-fanout.md)`. Important nuance: **the runtime keys remain live** — workers still write `gc.output_json`, and the compiler still sets `gc.output_json_required` for `on_complete` steps and check output sinks. Only *authored* fan-out via that metadata is deprecated [OFFICIAL] (formula-spec-v2 §3.4).
- **`[steps.tally]` is removed from the SDK.** Any formula declaring it now fails fast with `steps.tally was removed from the SDK`. The spec's guidance: "Use pack-level workflow logic to aggregate fan-out results if you need a synthetic pass/fail decision" [OFFICIAL] (§3.4). This directly removes the obvious primitive for "all N stories completed → produce one verdict for the results gate."
- **Unknown step keys are silently ignored.** The spec carries an explicit warning: *"A typo like `dependson` produces no diagnostic — the dependency simply vanishes."* Unknown keys inside `[requires]`, by contrast, are hard errors [OFFICIAL] (§1.3, §1.2). A silently-vanishing dependency in a formula that gates a human review is a serious failure mode for Momentum.
- The bundled packs have **not** finished migrating: #3462 *"gascity-packs: migrate the gascity pack's formulas to canonical v2 spelling"* is open and sits in the 1.5 milestone [OFFICIAL].

### Breaking changes since May 2026 (upgrade tax)

- **v1.2.0** — Pack V2 schema/layout enforcement becomes the supported authoring path (`schema = 2`, `[imports.*]`, conventional `agents/ formulas/ orders/ commands/` dirs). `[formulas].dir` and `[[rigs]].formulas_dir` become migration signals only. `gc import migrate` becomes a deprecated shim that **exits non-zero**. JSON contracts change: schema-versioned envelope objects, empty collections encode as `[]`, `gc sling --json` emits one JSONL record, `gc trace status`/`show` default to human output unless `--json`. `[[orders.overrides]]` rig matching is stricter (`rig = "*"` is now the explicit wildcard). `packs.lock` commit abbreviations must be ≥7 chars [OFFICIAL].
- **v1.2.1** — floor raised to Dolt ≥ 2.1.0 for managed bd/Dolt operation; older and pre-release Dolt builds are rejected [OFFICIAL]. *(Directly relevant to Momentum's beads/Dolt spike.)*
- **v1.3.0** — every provider reference must have a matching `[providers.<name>]` entry; built-in packs are no longer implicit and must be explicitly imported and pinned; `gc doctor --fix` owns these migrations via checks `provider-catalog`, `builtin-pack-imports`, `packv2-import-state` [OFFICIAL].
- **v1.4.0** — **"Configure one store-scoped `control-dispatcher` for every graph-owning scope."** Formula control beads route to the dispatcher whose `Dir` matches the store owning the graph; a rig-owned graph with no matching dispatcher now **fails before instantiation**. Also: run-centered dashboard/API, and new privacy-scoped command-usage telemetry (opt out via `DO_NOT_TRACK=1` or `GC_DISABLE_USAGE_METRICS=1`) [OFFICIAL].

Pattern: **every minor since 1.1 has required running `gc doctor --fix` against existing cities.** Momentum should assume a migration chore per minor, not per major.

---

## Orchestration v3 (#1709): designed, unscheduled

#1709 *"Proposal: Orchestration v3"* is **OPEN**, labels `priority/p2` / `kind/feature`, **no milestone**, opened 2026-05-05 by `csells`, 19 comments, **last updated 2026-06-01** [OFFICIAL] ([#1709](https://github.com/gastownhall/gascity/issues/1709)).

The proposal's core problem statement is the one Momentum would hit: slinging a convoy of N beads creates N independent runs, so verification phases see fragments. O3 makes a formula operate over a convoy as a whole, creating one Run. Crucially for this research:

> "the orchestrator has no first-class human-in-the-loop … Human-in-the-loop is a runtime disposition class with its own pause / notify / authorization machinery." [OFFICIAL]

Requirements that map onto Momentum's four gate types:

- **R4** — steps can enter a paused-awaiting-input state; independent steps continue; a Run with a HITL step is not a stale-Run GC candidate.
- **R12** — HITL is a runtime disposition alongside transient-fail and hard-fail, enterable by **author declaration (compile time)** or **agent transition (runtime)**.
- **R13** — pending HITL steps are surfaced to the assigned human via a durable notification source that survives controller restart.
- **R14** — approvers are subject to an authorization model verifiable at approval time; rejection terminates the Run via hard-fail.
- **S4/S5/S7** — planned checkpoint before irreversible actions; reactive mid-run escalation; a HITL pause surviving three days and two controller restarts.

Design detail **TC6** is the honest part: *"Humans aren't agents. Today there is no `human` type in the codebase — humans are modeled as agents with a `nudge` field."* Minimum viable HITL is an Approval Request — binary approve/reject plus optional comment — shaped as a discriminated union so choose-from-options / provide-data can be added later. **Single notification channel (dashboard)** for the initial release; multi-channel notification, presence detection, and escalation chains are **explicitly deferred** [OFFICIAL].

Migration story is friendly: the formula version field gates v3 behavior; existing v2 formulas execute unchanged; no data migration of molecules/convoys required [OFFICIAL].

**Status assessment.** The companion tracker #2503 *"Orchestration V3 Work Tracker"* is also OPEN, no milestone, **last updated 2026-06-09** — ten weeks stale [OFFICIAL] ([#2503](https://github.com/gastownhall/gascity/issues/2503)). Its most recent substance is a requirements crosswalk (PR #3259, `engdocs/design/orchv3-requirements-crosswalk.md`) which separates *covered semantics* from *remaining Gas City integration lanes* — and lists **HITL** among the remaining lanes, alongside Run persistence/recovery, operator intervention, and dashboard/event-stream integration [OFFICIAL]. Neither #1709 nor #2503 appears in the 1.4 or 1.5 milestones. What *has* shipped is the observability half: v1.4.0's run-centered dashboard and typed Run API partially deliver O3's R21 [OFFICIAL].

Useful history from `csells` (2026-05-06): *"we have two versions of formulas right now: v1 (as documented) and v2 (undocumented and blocked on semver for formulas #1760) … There was a silent O1 that predated GC 1.0, so GC 1.0 really shipped with O2."* [OFFICIAL]

**Bottom line: do not plan against O3 HITL. It is a well-specified proposal with no schedule, no milestone, and no visible implementation two and a half months after its last substantive update.**

---

## The gate surface today — the decisive finding (#4399)

The formula spec has a section titled **"4. Accepted But Inert"** for constructs the parser accepts but that have **no runtime consumer**. `[steps.gate]`'s type vocabulary is in it [OFFICIAL] (formula-spec-v2 §4, `main` as of 2026-08-19):

> **Gate `type` vocabulary.** `[steps.gate]` synthesizes a real gate bead that blocks its step until the gate bead is closed (manually or by an external watcher), but the `type` values `gh:run`, `gh:pr`, `timer`, `human`, and `mail` are doc-comment vocabulary in `internal/formula/types.go` — the parser never validates them and no bundled watcher acts on them. **Zero bundled formulas use `gate`.**

What *does* work is the structural half [OFFICIAL] (§2):

> A `[steps.gate]` table synthesizes a sibling gate bead (type `gate`, title `Gate: <type> <id>`) and a `blocks` edge from the gated step to it: **the step stays blocked until the gate bead is closed.**

I confirmed the vocabulary is source-level doc-comment only: a code search for `"gh:pr"` in Go across the repo hits exactly `internal/formula/types.go` and `internal/formula/parser_test.go` [EMPIRICAL]. A code search across `gastownhall/gascity-packs` for `steps.gate` returns **0** results, and for `waits_for` returns **0** — corroborating "zero bundled formulas use gate" [EMPIRICAL].

**#4399** (OPEN, `priority/p3` `kind/feature`, opened 2026-07-18, auto-triaged by a bot 2026-07-19, **no human maintainer ruling, no owner, no milestone**) documents the exact inconsistency [OFFICIAL] ([#4399](https://github.com/gastownhall/gascity/issues/4399)):

- **Ad-hoc** gates created with `bd gate create --type=timer|gh:run|gh:pr` *are* evaluated and auto-closed by the `bd gate check` watcher, which the bundled `gate-sweep` maintenance order runs on a cooldown.
- **Formula-synthesized** gates are never routed into that watcher path — the type lives in the bead *title* (`Gate: <type> <id>`), not in the condition path.
- Vocabulary drift: `mail` appears in the spec's `[steps.gate]` vocab but exists in neither `bd gate create --type` (`human`/`timer`/`gh:run`/`gh:pr`) nor `bd gate check --type` (`gh`/`gh:run`/`gh:pr`/`timer`/`bead`) — **documented but nonexistent everywhere**. `human` is in `create` but not `check` (correct by design — manual resolution). `bead` is the inverse.

**Corrected during AVFL fix pass — MAJ-011 / DOMAIN-A-004.** Momentum's four HITL point types are all *human* gates: triage approval, pre-sprint plan gate, mid-story tooling gate, post-sprint results gate. A `human` gate is *supposed* to be resolved manually — closing the gate bead **is** the approval, and that half genuinely costs nothing regardless of the inert `type` vocabulary. But "costs Momentum nothing" is too strong: `research-gate-mechanics-handson.md`'s "The defect" measures a second consumer of `type` beyond auto-resolution — **notification**. A formula-cooked gate persists `await_type: null`, while both bundled human-gate notify reflexes (`notify-on-human-gate-creation`, `renudge-stale-human-gates`) filter on `[ "$AWAIT_TYPE" = "human" ] || continue`. So a `[steps.gate] type="human"` blocks correctly and **tells nobody** — the inert vocabulary costs Momentum exactly the notification path it most needs, not "nothing." **[De-duplicated during AVFL fix pass — COHERENCE2-A-004.]** The gate bead is real, durable, addressable, and blocking, and remains a workable HITL primitive — but it is silent by default (Momentum's adoption plan must budget for the notify bolt-on described in `research-notification-watcher-layer.md`, not treat notification as free), unproductized, undocumented as a supported pattern, and used by zero bundled formulas: Momentum would be the first-party test case for both the primitive and its notification gap.

**No roadmap item productizes gate types.** #4399 is P3 with no owner; the only design work is inside the unscheduled O3 proposal. Do not expect `type = "human"` to acquire notification, authorization, or an approve/reject UI on any announced timeline.

---

## Barrier race #2311 — open, no fix, workaround regressed

**#2311** *"`waits_for = "children-of(X)"` does not gate `bd ready` when X uses `on_complete` bond fanout"* — **OPEN**, `kind/bug` `priority/p2`, opened 2026-05-17 against Gas City 1.1.1, **last activity 2026-05-29**, no fix PR, no maintainer ruling, no milestone [OFFICIAL] ([#2311](https://github.com/gastownhall/gascity/issues/2311)). Timeline shows only cross-references from #2320, #2321, #2947, #4399 — nothing implementing [EMPIRICAL].

Mechanism, as reported:

> `waits_for = "children-of(A)"` creates a tracking dep edge against step A at plan time (when no children exist yet). `bd ready` only gates on `blocks` edges, not `waits_for` edges, so: step B becomes ready as soon as step A closes; step A closes when the `on_complete` bond *schedules* its fanout (not when the children finish); result: **step B is claimable before any fanout children have run or written outputs.** [OFFICIAL]

The failure is silent — no logged error, just a worker running B's bash and failing on missing output files.

The spec independently confirms the root condition [OFFICIAL] (§4): *"`waits_for` compiles to a readiness-blocking `waits-for` dependency edge plus a recorded gate mode, but no current dispatcher logic interprets the `all-children` / `any-children` distinction. Zero bundled formulas use `waits_for`."*

Three workarounds are documented, and **the best one has since regressed**. A 2026-05-29 follow-up from the reporter on bd 1.0.4:

> The "add `needs = ["A"]` alongside `waits_for = "children-of(A)"`" workaround listed above is now **worse than insufficient** — on this toolchain it fails molecule instantiation outright… `bd create --graph` doesn't recognize that edge metadata and drops it: `warning: graph plan edge[N] has unknown field(s): [metadata] (silently dropped …)` [OFFICIAL]

Remaining workarounds: retry-with-sleep in the downstream step (brittle, tunable ceiling), or restructuring the consumer as a `[[steps.children]]` sibling (only possible when the producer is itself a `children` entry).

**Momentum impact:** a formula shaped "phase: conduct N stories in parallel → gate: human reviews the end-gate report" cannot use `waits_for` as the barrier. The gate would become claimable the moment the fan-out is *scheduled*, and the developer would be asked to approve a report that does not exist yet. Use `drain` (which owns its own convoy completion semantics) or a `check` loop that polls for completion.

---

## Container-gate gap #3451 — ruled on, not implemented

**#3451** *"formulas v2: `needs` on a parent step does not gate on its children (container-dependency parity with v1)"* — **OPEN**, `kind/bug` `priority/p2`, opened 2026-06-12 by `csells` [OFFICIAL] ([#3451](https://github.com/gastownhall/gascity/issues/3451)).

> Under the v1 contract, a step that declares `needs = ["parent"]` waits for the parent **and all of its children** … Under formulas v2, the graph compiler emits blocking dependency edges only and creates **no parent-child edges** (`internal/formula/compile.go` graph path), so the same `needs = ["parent"]` gates only on the parent step itself. [OFFICIAL]

`csells` frames it as *"the one authoring-semantics gap that keeps v2 from being a functional superset of v1"* (convergence being a consumer-side `gc converge` limitation, not a language one).

A **maintainer design decision was recorded 2026-06-28** by `sjarmak`: *"implement implicit parent-gating — compile the parent together with its descendants so a formulas-v2 `needs` on a parent gates the children. This restores the invisible-v1 parity contributors expect. Implementation tracking to follow."* [OFFICIAL]

**Nothing has landed in the ~8 weeks since.** The spec on `main` — last modified 2026-08-19, two days before this research — still carries the tracked-gap language in both the intro and §5, with the workaround intact [OFFICIAL]:

> **Container dependencies do not gate on children.** … This is a tracked gap ([#3451]), not a contract guarantee — **until it lands, enumerate the children explicitly in `needs`.**

`csells` also enumerated the three doc locations that must change when it ships (`understanding-formulas` "Choosing a Compiler Contract", `formula-spec-v2` §5, `formula-spec-v1` header + §5) — none have. A related verified constraint: the bd store enforces cross-type blocking rules (tasks can only block tasks, beads@v1.0.5 `internal/storage/issueops/dependencies.go:159-169`), which constrains the v1 form for epic-typed parents [OFFICIAL].

**Momentum impact — this is the load-bearing one.** The prescribed workaround is *"enumerate the children explicitly in `needs`."* Momentum's phase children are **runtime-discovered** — the story set is produced by sprint-planning, not known when the formula is authored. Explicit enumeration is therefore not available, and the workaround does not apply. A phase-then-gate cycle formula authored in v2 will not wait.

---

## #2947 — fan-out primitive: ruled, on_complete leaving beads

**#2947** *"design: the canonical way to fan out over a runtime-discovered set (on_complete vs drain)"* — **OPEN**, `kind/design` `priority/p2`, opened 2026-06-02 [OFFICIAL] ([#2947](https://github.com/gastownhall/gascity/issues/2947)).

The problem is two divergent `on_complete` dialects across two repos: beads' close-hook model (`output.<path>`, spec parses and validates but **has no runtime executor on beads `main` — every config is a silent no-op**, beads#3782; PR beads#3876 implements it) versus Gas City's dispatch-driven model (`gc.output_json` + `gc.fanout_state` control bead, `internal/dispatch/fanout.go`, gated into the graph.v2 contract). Plus `drain`, the graph-v2-native convoy-first primitive.

Two maintainer/lead positions [OFFICIAL]:
- `julianknutsen` (2026-06-02): *"I'd consider this pattern an orchestration primitive… beads can become really good at storing and creating dependencies of work and the orchestration layer can get really good at taking that work and executing it."*
- `sjarmak` (2026-06-28, design-triage ruling): *"scope `on_complete` out of beads (it is a silent no-op there and misleads). Keep the Gas City `on_complete` + drain primitive as the canonical runtime fan-out — we are not adding a second overlapping mechanism. Implementation tracking to follow."*

Combined with the `tally` removal, the resulting picture for Momentum: **`drain` is the sanctioned fan-out; there is no first-class aggregate/tally step to close a phase.** The spec's answer to "how do I turn N child outcomes into one verdict" is "use pack-level workflow logic."

---

## Wedge bugs #2131 and #2168 — both fixed

**#2131** *"order-tracking-sweep self-wedges, leading to full dispatcher wedge from 12+ ghost tracking beads"* — **CLOSED / COMPLETED 2026-05-23**, `kind/bug` `priority/p1` [OFFICIAL] ([#2131](https://github.com/gastownhall/gascity/issues/2131)).

Symptom: 12 ghost `order-tracking` beads accumulated over ~20h; every recurring order stopped firing; the city was "functionally inert." The self-wedge: `order-run:order-tracking-sweep` was itself one of the ghosts, so the self-healing sweep could not run. Two root causes emerged. First, a Beads `v1.0.4` **destructive server-mode write-startup bug**: non-read-only `bd` write commands could import a stale `.beads/issues.jsonl` into an already-populated Dolt database before applying the write, **rewinding newer Dolt-only state including status, assignee, labels, routing metadata, session metadata, and order-tracking close state** [OFFICIAL]. Second, the dispatcher's in-flight set was held in supervisor memory and not re-read per tick.

Fix shipped via **PR #2497**, merged 2026-05-23T04:56:21Z (merge commit `1e99deb8`), with required CI green: verifies order-tracking close durability through the same authority used by dispatch; expands stale tracking cleanup across rig target stores plus the legacy city fallback; preserves the open-tracking-bead duplicate-dispatch guard; adds `cmd/gc` regression coverage [OFFICIAL].

**#2168** *"order-tracking watchdog scope too narrow: cannot recover from multi-order tracking-bead jam without full city restart"* — **CLOSED / COMPLETED 2026-05-26** via commit `6c9af50`, cross-referenced PR #2619 [OFFICIAL] [EMPIRICAL] ([#2168](https://github.com/gastownhall/gascity/issues/2168)).

Mechanism: orphaned `order-tracking` beads block all future dispatches via the `hasOpenWorkStrict` gate (`cmd/gc/order_dispatch.go:312-318`); the recovery watchdog `runOrderTrackingSweepWatchdog` (`city_runtime.go:868`) was deliberately narrow — its `onlyOrders` filter swept only `order-tracking-sweep`'s own beads. On a single host with 19 always-on sessions and reconciler cycles of 50–200s, 20 open `order:*` beads sat for hours and every order stopped firing; only manual `gc order sweep-tracking --stale-after=30s` recovered.

**Both are genuinely resolved in the v1.2 window (v1.2.0, 2026-05-29).** Caveat: the bug *family* is still live. #2168 is referenced by commits as recently as 2026-08-15 (`ef4f4d2`), and tracker **#2903 "bead leak fixes and idle open-bead stability" remains open in milestone 1.5** [EMPIRICAL].

**Momentum impact:** the failure mode of this class is *silence*. A wedged dispatcher does not error — recurring orders simply stop firing. If Gas City drives Momentum's cycle on a schedule, cycle stalls will look identical to "nothing was due." Any adoption needs an external liveness check (e.g. `gc events --since` / `gc order history`) rather than trusting the orchestrator to complain.

---

## Momentum-relevant synthesis

| Momentum gate | Mechanism available today | State |
|---|---|---|
| (a) triage approval | `[steps.gate]` bead, closed manually | Works structurally; `type = "human"` inert — blocks correctly but tells nobody, both bundled notify reflexes filter it out (#4399; see correction above) |
| (b) pre-sprint plan gate | same | same; no notification/authorization machinery (O3 R13/R14, unscheduled) |
| (c) mid-story tooling gate | same, per-story gate bead | same; same silent-notification gap as (a)/(b), plus no reactive agent-raised HITL (O3 S5/R12, unscheduled) |
| (d) post-sprint results gate | **needs a barrier over the conduct phase** | **Blocked** — `waits_for` inert (#2311), container `needs` inert (#3451), `tally` removed |

The pattern: **gates are fine; barriers are not.** Gate (d) — and any gate that must follow a fan-out — has no reliable declarative expression in formulas v2 as of 2026-08-21. `drain` plus a `check` loop is the only sanctioned construction, and it is a different authoring shape from "phase, then gate."

Secondary risks worth carrying into the go/no-go: bus factor ≈1 (one author >50% of commits, both sampled windows); a breaking minor roughly every 5–6 weeks, each requiring `gc doctor --fix`; a hard Dolt ≥2.1.0 floor that interacts with Momentum's beads/Dolt dual-write spike; silently-dropped unknown step keys; and a 575-issue open backlog whose "Customer Zero" tranche shows basic multi-city and macOS operation still breaking in August 2026.

---

## Sources

- [gastownhall/gascity — repository](https://github.com/gastownhall/gascity) [OFFICIAL]
- [gastownhall/gascity — releases](https://github.com/gastownhall/gascity/releases) [OFFICIAL]
- [Gas City v1.2.0 release notes](https://github.com/gastownhall/gascity/releases/tag/v1.2.0) [OFFICIAL]
- [Gas City v1.2.1 release notes](https://github.com/gastownhall/gascity/releases/tag/v1.2.1) [OFFICIAL]
- [Gas City v1.3.0 release notes](https://github.com/gastownhall/gascity/releases/tag/v1.3.0) [OFFICIAL]
- [Gas City v1.3.3 release notes](https://github.com/gastownhall/gascity/releases/tag/v1.3.3) [OFFICIAL]
- [Gas City v1.4.0 release notes](https://github.com/gastownhall/gascity/releases/tag/v1.4.0) [OFFICIAL]
- [Gas City v1.4.1 release](https://github.com/gastownhall/gascity/releases/tag/v1.4.1) [OFFICIAL]
- [Formula Specification — v2 (docs)](https://docs.gascity.com/reference/specs/formula-spec-v2) [OFFICIAL]
- [`docs/reference/specs/formula-spec-v2.md` on `main`](https://github.com/gastownhall/gascity/blob/main/docs/reference/specs/formula-spec-v2.md) — fetched via GitHub contents API, file last modified 2026-08-19 (`ba85a40e`) [OFFICIAL]
- [Formula Specification — v1 (docs)](https://docs.gascity.com/reference/specs/formula-spec-v1) [OFFICIAL]
- [Understanding Formulas — Choosing a Compiler Contract](https://docs.gascity.com/guides/understanding-formulas) [OFFICIAL]
- [Gas City Docs — Overview](https://docs.gascity.com/) [OFFICIAL]
- [#1709 — Proposal: Orchestration v3](https://github.com/gastownhall/gascity/issues/1709) [OFFICIAL]
- [#2503 — Orchestration V3 Work Tracker](https://github.com/gastownhall/gascity/issues/2503) [OFFICIAL]
- [#2131 — order-tracking-sweep self-wedges (CLOSED)](https://github.com/gastownhall/gascity/issues/2131) [OFFICIAL]
- [PR #2497 — #2131 fix](https://github.com/gastownhall/gascity/pull/2497) [OFFICIAL]
- [#2168 — order-tracking watchdog scope too narrow (CLOSED)](https://github.com/gastownhall/gascity/issues/2168) [OFFICIAL]
- [#2311 — waits_for children-of does not gate bd ready (OPEN)](https://github.com/gastownhall/gascity/issues/2311) [OFFICIAL]
- [#2947 — canonical fan-out: on_complete vs drain (OPEN)](https://github.com/gastownhall/gascity/issues/2947) [OFFICIAL]
- [#3451 — formulas v2 needs on a parent does not gate children (OPEN)](https://github.com/gastownhall/gascity/issues/3451) [OFFICIAL]
- [#3462 — migrate gascity pack formulas to canonical v2 spelling (OPEN)](https://github.com/gastownhall/gascity/issues/3462) [OFFICIAL]
- [#4399 — [steps.gate] type vocabulary parsed-but-not-enforced (OPEN)](https://github.com/gastownhall/gascity/issues/4399) [OFFICIAL]
- [#2903 — Tracker: bead leak fixes and idle open-bead stability (OPEN)](https://github.com/gastownhall/gascity/issues/2903) [OFFICIAL]
- [Milestone 1.5 search](https://github.com/gastownhall/gascity/milestones?q=1.5) [OFFICIAL] (added during AVFL fix pass — STRUCTURAL-A-009)
- `research-verification-probes.md` — Probe 4 corroborates dashboard/port claims elsewhere in this corpus [EMPIRICAL] (added during AVFL fix pass)
- [gastownhall/gascity-packs](https://github.com/gastownhall/gascity-packs) [OFFICIAL]
- GitHub REST API — `repos/gastownhall/gascity/commits`, `.../stats/participation`, `search/issues`, `search/code`, `issues/{n}/timeline`, queried 2026-08-21 [EMPIRICAL]
- [Gas City - Software Factory Platform for Coding Agents](https://gascity.com/about-gas-city/) — marketing page listing "human gates" as a feature; page returned HTTP 404 on direct fetch, claim reached only via search snippet [UNVERIFIED]
- [Steve Yegge's AI agent orchestration project Gas Town comes to the cloud — The New Stack](https://thenewstack.io/steve-yegges-ai-agent-orchestration-project-gas-town-comes-to-the-cloud-and-brings-the-wasteland-with-it/) [PRAC] — background only, not used for any factual claim above
