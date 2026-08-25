---
content_origin: claude-code-subagent
date: 2026-08-21
sub_question: "Gate mechanics hands-on: install gc, author a minimal v2 formula with a [steps.gate] step, and empirically verify the gate bead blocks downstream steps and manual closure releases the graph"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

## Headline

**The `[steps.gate]` mechanism works exactly as advertised for blocking and release — and its notification story is broken in a way that matters for Momentum.** Cooking a v2 formula whose step carries `[steps.gate] {type="human", id="test-gate"}` synthesizes a real bead of `issue_type: gate` titled `Gate: human test-gate`, wires a blocking edge from the gated step to it, keeps the gated step out of `bd ready`, and releases the whole downstream graph the instant the gate bead is closed. All of that was reproduced end-to-end on two independent throwaway cities and two bd versions. **[EMPIRICAL]** The gate additionally **refuses `bd close`** on the gated step while it is open — but that half was reproduced against a **timer** gate, not the human gate: the close-side enforcement lives in beads' dependency-closure check, which does not read gate `type`, so the claim is gate-type-agnostic by code path yet **[UNVERIFIED for `human` gates specifically]** (see Q2's bonus finding for the full scoping).

The defect: a formula-cooked gate persists `await_type: null`. Gas City's bundled human-gate notification reflexes filter on `await_type == "human"`, so they silently skip every gate a formula creates. A `[steps.gate] type="human"` blocks correctly and tells nobody. **[EMPIRICAL]** + **[OFFICIAL]** (code-read)

---

## Environment and versions

| Component | Version | How obtained |
|---|---|---|
| `gc` (Gas City) | **1.4.1** (`gc version` → `1.4.1`) | `mise use -g github:gastownhall/gascity@latest` — succeeded first try, with GitHub artifact attestations verified |
| `bd` (beads), pre-existing | **1.0.4** (`ce242a879`) | already installed via mise github backend |
| `bd` (beads), gc-pinned | **1.2.2** (`6c124203e`) | downloaded to scratchpad only, never onto PATH globally |
| mise | 2026.6.14 | pre-existing |
| Platform | darwin arm64 (macOS 25.5.0) | — |

Install command and result **[EMPIRICAL]**:

```
$ mise use -g github:gastownhall/gascity@latest
mise github:gastownhall/gascity@1.4.1    [1/3] install
mise github:gastownhall/gascity@1.4.1    [1/3] download gascity_1.4.1_darwin_arm64.tar.gz
mise github:gastownhall/gascity@1.4.1    [2/3] checksum gascity_1.4.1_darwin_arm64.tar.gz
mise github:gastownhall/gascity@1.4.1    [2/3] verify GitHub artifact attestations
mise github:gastownhall/gascity@1.4.1    [2/3] ✓ GitHub artifact attestations verified
mise github:gastownhall/gascity@1.4.1    [3/3] extract gascity_1.4.1_darwin_arm64.tar.gz
mise github:gastownhall/gascity@1.4.1  ✓ installed
```

Binary lands at `~/.local/share/mise/installs/github-gastownhall-gascity/latest/gc` (88 MB). No brew, no ubi fallback, no `docs.gascity.com` installer needed — **the mise github backend is the clean install path for this machine** ([Installation docs](https://docs.gascity.com/getting-started/installation)). **[EMPIRICAL]**

Note `gc --version` is **not** a valid flag; it is `gc version`. **[EMPIRICAL]**

Relevant version-skew note: gc 1.4.1's CHANGELOG entry for 2026-08-15 states "**beads pinned to v1.2.2 everywhere** (go.mod library, `deps.env` `BD_VERSION`, CI matrix…)" — i.e. gc 1.4.1 embeds the beads v1.2.2 library, while Momentum's machine-wide `bd` CLI is v1.0.4. Every finding below was reproduced under **both** CLIs, so none of them is a skew artifact. **[OFFICIAL]** (shipped `CHANGELOG.md`) + **[EMPIRICAL]**

---

## City setup: what gc actually requires

`gc init --template minimal --default-provider claude --no-start --name gatetest .` created the full scaffold (`.gc/`, `city.toml`, `pack.toml`, `agents/`, `formulas/`, `orders/`, …) then reported: **[EMPIRICAL]**

```
gc init: missing required dependencies:
  - tmux
  - dolt
  - flock
gc init: install the missing dependencies, then run 'gc start'
```

Two things matter here for Momentum:

1. **`gc init` is the enforcement point, and under the bd provider it demands tmux, an external `dolt` binary, and `flock` — all three, up front.** The transcript above is a `gc init` run (with `--no-start`), and it refuses on all three before any orchestrator starts; it enforces them at init precisely because `gc start` will need them. Running the *city* is a heavier dependency footprint than running the *graph*, and the out-of-session cycle layer Momentum is evaluating would pull in tmux-managed agent sessions. Under `GC_BEADS=file` the same `gc init` gate demands **tmux only** — not dolt, not bd (`research-verification-probes.md` Probe 1). **[Attribution corrected during AVFL fix pass — DOMAIN4-A-001 / COHERENCE4-A-004; this bullet previously credited the requirement to `gc start`, which the transcript at :52–56 directly contradicts.]**
2. **The graph layer does not.** Formula compilation, cooking, and all bead/readiness semantics ran fine with the city un-started, backed by a plain `bd init` store using **bd's own embedded Dolt** (`.beads/embeddeddolt/`) — no external dolt binary. That is the exact backing Momentum's dual-write spike already uses. **[EMPIRICAL]**

**`GC_BEADS=file` is real and functional in gc 1.4.1.** `gc init` under it requires only `tmux` as a missing-dependency blocker (not dolt, not bd), and once tmux is present, `gc doctor` reports every dolt-specific check `✓ skipped (file backend or GC_DOLT=skip)` and confirms `builtin bd/dolt pack family not required`. **[Corrected during AVFL fix pass — CRIT-004, resolved by live probe on gc 1.4.1; see `research-verification-probes.md` Probe 1.]** The text this section originally carried is **retracted**: it read "there is no `GC_BEADS=file` escape hatch in 1.4.1," citing `bd init --help`'s "Dolt is the default (and only supported) storage backend." That evidence is inapplicable — `bd init --help` describes **beads' own** storage backend selection, a different switch from Gas City's `GC_BEADS` provider selection. The corrected claim is the one stated first above.

However, the correction does not change this document's own bottom line, and in fact sharpens it: the **entire `gc bd` verb family — including `bd gate create --type=human`, the exact primitive this document exercises throughout §Q1–Q4 — is unconditionally blocked on a file-backed city.** `GC_BEADS=file gc bd gate create --type=human` fails with `gc bd: only supported for bd-backed beads providers`. So while `GC_BEADS=file` exists and boots a city with a lighter dependency footprint than this document's `gc init` run below (which found tmux/dolt/flock all missing), **the gate mechanics demonstrated in this document specifically require a bd/Dolt-backed store** — embedded Dolt, as used below, is sufficient for that store. **Scoped (ACCURACY2-A-001):** this document's own probe never ran `gc init`/`gc start` with the bd provider successfully — it bypassed gc's dependency gate entirely and used a plain `bd init` store directly. "Embedded Dolt is sufficient" describes that direct-`bd` graph layer; a `gc`-orchestrated bd-provider **city** still hits the `gc init` dependency check immediately below (tmux/dolt/flock all reported missing), regardless of embedded vs. external dolt. Embedded Dolt remains the low-ceremony option for direct gate operations against a bd store, and it is sufficient for that narrower case. **[EMPIRICAL]** / **[OFFICIAL]** (bd CLI help)

---

## The formula

Authored at `<city>/formulas/gatetest.toml`. Formula discovery is the well-known `formulas/` directory — city packs, then the city's own `formulas/`, then rig packs ([formula spec v2 §1.1](https://docs.gascity.com/reference/specs/formula-spec-v2)). **[EMPIRICAL]** + **[OFFICIAL]**

```toml
formula = "gatetest"
description = "Minimal HITL gate probe: A -> B(gated) -> C"

[requires]
formula_compiler = ">=2.0.0"

[[steps]]
id = "a"
title = "Step A: upstream work"
description = "Trivial upstream step. No gate."

[[steps]]
id = "b"
title = "Step B: gated on human approval"
description = "Downstream of A, blocked by a human gate."
needs = ["a"]

[steps.gate]
type = "human"
id = "test-gate"

[[steps]]
id = "c"
title = "Step C: after the gate"
description = "Must not become ready until B closes."
needs = ["b"]
```

No exec bodies, no agent, no provider — pure graph. `gc formula show gatetest`: **[EMPIRICAL]**

```
Formula: gatetest
Description: Minimal HITL gate probe: A -> B(gated) -> C

Steps (5):
  ├── gatetest.a: Step A: upstream work
  ├── gatetest.gate-b: Gate: human test-gate (gate)
  ├── gatetest.b: Step B: gated on human approval [needs: gatetest.gate-b, gatetest.a]
  ├── gatetest.c: Step C: after the gate [needs: gatetest.b]
  └── gatetest.workflow-finalize: Finalize workflow [needs: gatetest.c]
```

Three authored steps compile to five: the compiler injects `gate-b` **before** `b` in topological order and rewrites `b`'s needs to include it, then appends the `workflow-finalize` control bead. `gc formula cook gatetest`: **[EMPIRICAL]**

```
Root: gt-iit
Created: 6
gatetest -> gt-iit
gatetest.a -> gt-o86
gatetest.b -> gt-b3e
gatetest.c -> gt-h0c
gatetest.gate-b -> gt-crp
gatetest.workflow-finalize -> gt-d3m
```

---

## Q1 — Does a gate bead materialize?

**Yes.** `bd show gt-crp`: **[EMPIRICAL]**

```
○ gt-crp · Gate: human test-gate   [● P2 · OPEN]
Type: gate
DESCRIPTION
Async gate for step b
METADATA
  gc.continuation_group: pool-workflow
  gc.root_bead_id: gt-iit
  gc.root_store_ref: city:gatetest
  gc.routed_to:
  gc.session_affinity: require
  gc.step_ref: gatetest.gate-b
DEPENDS ON
  → ○ gt-iit: gatetest ● P2
BLOCKS
  ← ○ gt-b3e: Step B: gated on human approval ● P2
```

Title format is exactly `Gate: <type> <id>`, matching the compiler source: `gateTitle = fmt.Sprintf("Gate: %s %s", step.Gate.Type, step.Gate.ID)` in [`internal/formula/compile.go`](https://github.com/gastownhall/gascity/blob/main/internal/formula/compile.go) (lines ~523–560, which also set `Type: "gate"`, `Description: "Async gate for step %s"`, and the `DependsOnID: gateID` edge). **[OFFICIAL]** (code-read)

Two behaviours worth recording:

- **Gate beads are hidden from plain `bd list`.** `bd list` reported "Total: 5 issues" and omitted `gt-crp` entirely; `bd list --type gate` and `bd gate list` show it. A Momentum surface that enumerates work via `bd list` will not see its own gates. **[EMPIRICAL]**
- **Gate beads are never in `bd ready`.** With everything open, `bd ready` returned only Step A. The gate is not offered to any agent as work — correct for HITL. **[EMPIRICAL]**

---

## Q2 — Is the gated step excluded from ready while the gate is open?

**Yes, and the block is attributable solely to the gate.** After closing Step A: **[EMPIRICAL]**

```
$ bd close gt-o86 --reason "empirical probe: A done"
✓ Closed gt-o86 — Step A: upstream work: empirical probe: A done

$ bd ready
✨ No ready work found (all issues have blocking dependencies)

$ bd blocked
[● P2] gt-b3e: Step B: gated on human approval
  Blocked by 1 open dependencies: [gt-crp]
```

`bd show gt-b3e` lists three `DEPENDS ON` edges — the gate `gt-crp`, the workflow root `gt-iit`, and the (now closed) `gt-o86` — but `bd blocked` counts **one** blocking dependency, `gt-crp`. The root edge is structural, not readiness-blocking. **The gate is the exclusive blocker.** **[EMPIRICAL]**

**Bonus finding — the gate also blocks *closure*, not just readiness** (reproduced against a **timer** gate; **[UNVERIFIED for `human` gates specifically]** — see the scope note below). Attempting to close a gated step out from under its gate: **[EMPIRICAL]**

```
$ bd close gt-bvw --reason "attempting bypass"
cannot close gt-bvw: blocked by open issues [gt-2zt] (use --force to override)
```

**The claim stands: an open gate refuses `bd close` on the gated step, which is stronger than a readiness filter** — reproduced against a **timer** gate, **[UNVERIFIED for `human` gates specifically]**; see the scope paragraph immediately below. An agent cannot mark gated work done while the gate stands; `--force` is the documented, explicit override. For Momentum's mid-story tooling gates (type (c): developer must exercise nornspun/chorgi by hand before the story proceeds) this is precisely the property needed — an over-eager agent cannot self-certify past it without an audit-visible `--force`.

**Scope of the evidence for that claim.** The refusal was directly reproduced against a **timer** gate (`gt-bvw` blocked by `gt-2zt`), not against this section's human gate (`gt-b3e`/`gt-crp`). The close-side enforcement lives in beads' dependency-closure check, which does not distinguish gate `type`, so the claim is **gate-type-agnostic by code path** — but **[UNVERIFIED for `human` gates specifically]**, inferred from the shared path rather than independently re-run. A reader reproducing this for a `human` gate should expect the same refusal against `gt-b3e`/`gt-crp`-style IDs, not the ones shown above.

*Correction history: MAJ-009 / ACCURACY-A-012 (AVFL fix pass) — the transcript above was pasted from the timer-gate probe run later in this document (§"The defect", `[steps.gate] type="timer" id="auto-5s"`) rather than from the human-gate probe this section otherwise walks (`gatetest.a -> gt-o86 / gatetest.b -> gt-b3e / gatetest.gate-b -> gt-crp`); ACCURACY2-A-009 then added the human-gate scoping, and COHERENCE3-A-002 propagated it to this document's Headline and to `research-dec035-revisit-triggers.md`.*

---

## Q3 — Does manual closure release the graph?

**Yes, immediately.** **[EMPIRICAL]**

```
$ bd close gt-crp --reason "human approved: empirical probe"
✓ Closed gt-crp — Gate: human test-gate: human approved: empirical probe

$ bd ready
○ gt-b3e ● P2 Step B: gated on human approval
Ready: 1 issues with no active blockers
```

`bd gate resolve <id> --reason "..."` is the named equivalent (`bd gate resolve --help`: "This is equivalent to 'bd close <gate-id>' but with a more explicit name"). Reproduced on the second city under bd 1.2.2: **[EMPIRICAL]**

```
$ bd gate resolve g2-gea -r "developer verdict: fork-1 adopt; fork-2 change"
✓ Gate resolved: g2-gea
  Reason: developer verdict: fork-1 adopt; fork-2 change

$ bd ready
○ g2-uzx ● P2 Step B: gated on human approval
```

**The close reason is persisted on the gate bead** (`bd show g2-gea` → `Close reason: developer verdict: fork-1 adopt; fork-2 change`). This is a directly usable substrate for Momentum's anti-rubber-stamp requirement on the pre-sprint plan gate: the written per-fork verdict lands in the bead's audit trail, not just in a chat transcript. **[EMPIRICAL]**

---

## Q4 — Does the graph drive to completion?

**Yes.** Closing each released step in turn walked the whole DAG: **[EMPIRICAL]**

| Action | Next `bd ready` |
|---|---|
| close `gt-b3e` (Step B) | `gt-h0c` Step C |
| close `gt-h0c` (Step C) | `gt-d3m` Finalize workflow |
| close `gt-d3m` (finalize) | `gt-iit` gatetest (root) |

Final `bd list --all`: 5 issues, 4 closed, root open-and-ready. This matches the spec's stated v2 shape: "The root blocks on `workflow-finalize` and only becomes Ready when the workflow completes." In a *started* city the orchestrator's control dispatcher executes `workflow-finalize` itself — "The orchestrator executes every control bead… No agent participates in control execution" ([formula spec v2 §0.2](https://docs.gascity.com/reference/specs/formula-spec-v2)). Here I closed it by hand because the city was never started. **[EMPIRICAL]** + **[OFFICIAL]**

---

## The defect: `type` and `timeout` are not persisted

Spec §4 ("Accepted But Inert") warns that the gate `type` vocabulary "has no runtime consumer" and that "the parser never validates them and no bundled watcher acts on them. Zero bundled formulas use `gate`." **[OFFICIAL]** I measured what that actually costs.

Formula-cooked gate vs. ad-hoc `bd gate create` gate, same store: **[EMPIRICAL]**

```
$ bd show gt-crp --json | jq -c '{id,issue_type,title,await_type,await_id,status}'
{"id":"gt-crp","issue_type":"gate","title":"Gate: human test-gate","await_type":null,"await_id":null,"status":"open"}

$ bd show gt-cvl --json | jq -c '{id,issue_type,title,await_type,await_id,status}'
{"id":"gt-cvl","issue_type":"gate","title":"Gate: human","await_type":"human","await_id":null,"status":"open"}
```

`gt-cvl` came from `bd gate create --type=human --blocks gt-6xn --reason="Plan gate: developer must write per-fork verdicts"`. **The ad-hoc path persists `await_type`; the formula path does not.** The declared `type` survives only as text inside the title string, carrying no machine-readable identity any watcher or notifier can filter on. `bd show --json` on the formula gate persists a **null** `await_type` (softened during AVFL fix pass — LOW-001/ACCURACY-A-013: the `jq` transcript above shows `await_type: null`, which cannot by itself distinguish "key present with null value" from "key absent" — no `jq 'keys'` listing was run to settle it, and the distinction doesn't matter for the downstream argument either way, since the notifier filter `[ "$AWAIT_TYPE" = "human" ] || continue` fails identically on both). Reproduced identically on a fresh city under bd 1.2.2 (`{"id":"g2-gea",…,"await_type":null}`), so it is not a CLI-version artifact. **[EMPIRICAL]**

The compiler *does* carry the values into the recipe — `Gate: &RecipeGate{Type: step.Gate.Type, ID: step.Gate.ID, Timeout: step.Gate.Timeout}` in `internal/formula/compile.go` — so the loss happens on the cook/materialize path into the bead store, not at compile time. **[OFFICIAL]** (code-read)

`timeout` is lost the same way. I cooked a second formula with `[steps.gate] type="timer" id="auto-5s" timeout="5s"`, waited 7 seconds, and ran the watcher: **[EMPIRICAL]**

```
$ bd gate show gt-2zt
○ gt-2zt - Gate: timer auto-5s
  Status: open
  Await Type:
  Description: Async gate for step t

$ bd gate check
Checked 0 gates: 0 resolved, 0 escalated, 0 errors
```

Contrast with an ad-hoc timer gate, which works perfectly: **[EMPIRICAL]**

```
$ bd gate create --type=timer --blocks gt-qa6 --timeout=5s --reason="timer probe"
✓ Created gate gt-bj6 (type: timer)
$ sleep 7 && bd gate check
✓ gt-bj6: resolved - timer expired 2s ago
Checked 1 gates: 1 resolved, 0 escalated, 0 errors
$ bd ready
○ gt-qa6 ● P2 timer gate probe target
```

**Net effect: every gate a formula creates is a permanently-manual gate, regardless of declared type.** For Momentum's four HITL points this is *fail-safe* — no plan gate or results gate can silently auto-expire — but it means `[steps.gate]` cannot today express "gate on this PR merging" or "gate on this CI run", and it breaks notification (next section).

---

## The notification gap — the finding with real teeth

Gas City ships (on `main`) two core-pack orders that exist precisely to notify a human about an open human gate:

- `internal/bootstrap/packs/core/orders/notify-on-human-gate-creation.toml` — `trigger = "event"`, `on = "bead.created"`
- `internal/bootstrap/packs/core/orders/renudge-stale-human-gates.toml` — `trigger = "cooldown"`, `interval = "5m"`

Their own header comments state the problem they solve: "creating a `type=human` gate produces ZERO notification — the gate bead is built, the blocks edge is added, a line prints to stdout, and the human who must resolve it is never told (proven ABSENT in gascity/beads: gate creation has no post-create notify hook; the only gate watcher skips human gates entirely)." **[OFFICIAL]** ([notify-on-human-gate-creation.toml](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/notify-on-human-gate-creation.toml))

Both scripts gate on the same predicate. From [`notify-on-human-gate-creation.sh`](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/assets/scripts/notify-on-human-gate-creation.sh): **[OFFICIAL]** (code-read)

```bash
AWAIT_TYPE="$(printf '%s' "$GATE_JSON" | jq -r '.await_type // ""' 2>/dev/null)"
# Only OPEN human gates. …
[ "$AWAIT_TYPE" = "human" ] || continue
```

`renudge-stale-human-gates.sh` applies the identical filter ("keeps only `await_type == \"human\"` gates").

**Because formula-cooked gates carry `await_type: null`, both bundled reflexes skip them.** A `[steps.gate] type="human"` in a formula is the *one* construct that most needs the notify, and it is exactly the construct the notify cannot see. **[EMPIRICAL]** (the null) + **[OFFICIAL]** (the filter)

Two aggravating details:

1. **Neither order is in the 1.4.1 release.** `gc order list` on the freshly-initialized 1.4.1 city returned 20 orders including `gate-sweep`, `cascade-nudge-on-blocker-close`, `nudge-mail-sweep`, `orphan-sweep` — but **no** `notify-on-human-gate-creation` and **no** `renudge-stale-human-gates`. They exist only on `main` (repo `pushed_at` 2026-08-22). On the current release, a human gate notifies nobody by any path. **[EMPIRICAL]**
2. **`gate-sweep`, the one gate watcher that does ship in 1.4.1, deliberately excludes human gates.** Its script body is exactly two lines: `gc bd gate check --type=timer --escalate` and `gc bd gate check --type=gh --escalate || true`. I confirmed empirically that `bd gate check` returns "Checked 0 gates" even against a properly-typed *ad-hoc* `human` gate. **[EMPIRICAL]** + **[OFFICIAL]** (`gate-sweep.sh` from the local pack cache)

---

## Addressee routing is also constrained

I attempted to give a gated step a human assignee so the notify path (assignee → `gc.deferred_assignee` → `$GC_ESCALATION_RECIPIENT`) would have somewhere to land:

```toml
[[steps]]
id = "p"
title = "Assigned gated step"
assignee = "human"
[steps.gate]
type = "human"
id = "plan-gate"
```

Cook failed: **[EMPIRICAL]**

```
gc formula cook: decorate formulas v2 recipe: step gatetest3.p: assignee target "human"
did not resolve to a concrete session; use gc.run_target for config routing
```

`assignee` must resolve to a concrete *session*; "human" is not one. So the addressee for a formula gate necessarily falls through to `$GC_ESCALATION_RECIPIENT` (default `"human"`), which the mail path treats specially: `gc mail send --notify` "deliberately skips the tmux-nudge for the 'human' recipient (humans have no session; cmd_mail.go `to != \"human\"`)". Momentum would need to supply its own out-of-band notification (macOS notification, cmux nudge, Slack) for any gate a developer is expected to answer. **[EMPIRICAL]** + **[OFFICIAL]**

---

## Reopen semantics (the rejection path)

Reopening a gate after the gated step already closed does **not** claw the step back: **[EMPIRICAL]**

```
$ bd reopen gt-crp
↻ Reopened gt-crp
$ bd show gt-b3e
✓ gt-b3e · Step B: gated on human approval   [● P2 · CLOSED]
```

The gate is one-shot in the forward direction; reopening only re-blocks a step that has not yet closed. A "developer rejects the plan, send it back" flow must therefore either (a) reopen the gate *and* the downstream steps explicitly, or (b) model rejection as a distinct branch rather than a gate reopen.

---

## What this means for Momentum's four HITL points

| Momentum gate | Verdict | Basis |
|---|---|---|
| (a) triage approval | **Fits.** One gate bead blocking the "convert observations to work" step; batch approval = one `bd gate resolve`. | Q2/Q3 **[EMPIRICAL]** |
| (b) pre-sprint plan gate | **Fits with a notify bolt-on.** Blocking works; `--reason` persists the written verdict (anti-rubber-stamp substrate). But nothing tells the developer the gate opened, and the visual companion surface is out of scope for gc — gc holds the *state*, Momentum still renders the *surface*. | Q3 + notification gap **[EMPIRICAL]** |
| (c) mid-story tooling gates | **Best fit for the single-story case; the fan-out-feeding half is untested here.** The close-side enforcement (`cannot close … blocked by open issues`) is exactly "the agent may not declare done until a human exercised the tool," with `--force` as the audited override — that part is solid, with one scope note: it was reproduced against a **timer** gate and is gate-type-agnostic by code path, **[UNVERIFIED for `human` gates specifically]** (Q2 bonus finding). But this document's probe never exercised a fan-out or `drain`, so it cannot speak to a mid-story gate that must wait on multiple parallel children. | Q2 bonus **[EMPIRICAL]**; fan-out half **untested** |
| (d) post-sprint results gate | **[Corrected during AVFL fix pass — DOMAIN-A-003.] Blocked, not "Fits."** This document's probe was a 3-step linear chain (`A → B(gated) → C`) with no exec bodies, no agent, no fan-out, and every bead closed by hand on a city that was never started — it cannot demonstrate a barrier over a fanned-out phase, which is exactly what a results gate needs. `research-maturity-open-bugs.md`'s "Momentum-relevant synthesis" table has the load-bearing finding this row must defer to: `waits_for` is inert (#2311), container `needs` does not gate children (#3451), and `tally` was removed from the SDK — and #3451's prescribed workaround ("enumerate the children explicitly in `needs`") does not apply to Momentum, whose phase children are runtime-discovered. Gate *blocking and release*, demonstrated here, still holds once a barrier construction exists (`drain` + a check loop); it is the barrier itself that is unproven and, per that file, currently unreliable. | Q3 **[EMPIRICAL]** demonstrates blocking/release only; barrier is **Blocked** per `research-maturity-open-bugs.md` |

**Confidence propagated into this table (DOMAIN-A-003):** see "Confidence and limits" below — this probe never exercised fan-out, `drain`, or `[[steps.children]]`, so rows (c)'s fan-out half and (d) as stated should not be read as tested by this document alone.

**Design consequence, stated precisely: prefer `bd gate create` over `[steps.gate]` — but what that preference buys depends on gate type.** For `timer` / `gh:run` / `gh:pr` gates it is decisive: the ad-hoc path's persisted `await_type` is what makes them auto-resolvable at all. For `type=human` — which is all four of Momentum's gate points — it buys **notifiability, not auto-resolution**, and not today: `bd gate check` and `gate-sweep` skip human gates regardless of whether `type` is persisted (confirmed above — "Checked 0 gates" against a properly-typed ad-hoc human gate, and `gate-sweep`'s two-line body only ever calls `--type=timer` and `--type=gh`), so the *only* consumers of a persisted `await_type: "human"` are the notify/renudge orders, which are in no tagged release (`main`/`edge` only). Net for Momentum: the ad-hoc path yields a gate a vendored or future notifier can classify; the declarative `[steps.gate]` yields a blocker no watcher can classify at all. Both block correctly; neither notifies out of the box. **[Scoping from ACCURACY2-A-003; restructured conclusion-first during the AVFL fix pass — COHERENCE3-A-010, because the bolded takeaway read broader than the scoping that followed it.]** **[Corrected during AVFL fix pass — CRIT-005; see `research-cycle-orchestration-fit.md` §1.]** A v2 formula step has no `exec` field and cannot "shell out" to anything — steps are work beads that agents claim and execute inside sessions, not shell subprocesses. The construct that gets `bd gate create` run is a work step whose `description`/`description_file` instructs the claiming agent to run `bd gate create --type=human --blocks <downstream-step-bead-id>` as part of its work (or, on the orchestrator side with no agent involved, an order-level `exec` script, capped at 300s). Either way, `--blocks` must resolve to the **downstream** step's bead id — not the gate-creating step's own id — and that id is only knowable at cook time via `gc.root_bead_id` + `gc.step_ref` metadata on the materialized beads, not at formula-authoring time. Done that way, this gets a first-class, watcher-visible gate; the declarative `[steps.gate]` gets a blocker that no watcher can classify.

Dependency consequence for the open DEC-028 Dolt go/no-go: **the graph semantics tested here need only bd's embedded Dolt**, which Momentum already runs. Standing up a `gc` **city** is what adds tmux + an external `dolt` binary + `flock`, and `gc init` — not `gc start` — is where all three are enforced, up front and before any orchestrator runs (transcript at :52–56; `research-verification-probes.md` Probe 1). **[Attribution corrected during AVFL fix pass — DOMAIN4-A-001 / COHERENCE4-A-004.]** Gate mechanics can therefore be adopted incrementally without resolving the full Dolt question, but the *cycle-orchestration* layer cannot. Note also (CRIT-004, per Probe 1/2/3 above): `GC_BEADS=file` does not substitute for bd/Dolt here — the `bd gate create` primitive this whole document walks is unconditionally unavailable on a file-backed city, so "incrementally" means "on a bd/Dolt-backed city, even a minimal embedded one," not "on either provider."

---

## Reproduction script (condensed)

```bash
mise use -g github:gastownhall/gascity@latest        # → gc 1.4.1
gc version
mkdir -p /tmp/gc-city && cd /tmp/gc-city
gc init --template minimal --default-provider claude --no-start --name gatetest .
BD_NON_INTERACTIVE=1 bd init --prefix gt
# author formulas/gatetest.toml as shown above
gc formula show gatetest                              # 5 steps, gate-b injected
gc formula cook gatetest                              # Created: 6
bd ready                                              # only Step A
bd close <A> --reason "A done"
bd ready                                              # "No ready work found"
bd blocked                                            # B blocked by [<gate>]
bd show <gate> --json | jq '.[0].await_type'          # null   ← the defect
bd gate check                                         # "Checked 0 gates"
bd gate resolve <gate> -r "verdict text"
bd ready                                              # Step B released
```

---

## Confidence and limits

- Blocking, release, completion walk, `await_type` loss, reopen semantics: **directly observed, twice, on two bd versions.** High confidence.
- Close-side enforcement (`bd close` refused on a gated step): **directly observed, but against a `timer` gate only.** The enforcement lives in beads' dependency-closure check, which does not read gate `type`, so the claim is gate-type-agnostic by code path — **[UNVERIFIED for `human` gates specifically]**, inferred rather than re-run (Q2 bonus finding; ACCURACY2-A-009, propagated to the Headline and to `research-dec035-revisit-triggers.md` at iteration 3 under COHERENCE3-A-002).
- Orchestrator-side behavior with a **started** city (auto-execution of `workflow-finalize`, `gate-sweep` firing on its 30s cooldown, `gc mail send --notify` delivery) was **not** exercised — tmux/dolt/flock were absent by design (throwaway scratchpad, no system installs). Those claims rest on the shipped order definitions and spec text, tagged **[OFFICIAL]** code-read, not **[EMPIRICAL]**.
- The `notify-on-human-gate-creation` / `renudge-stale-human-gates` orders were read from `main` and confirmed **absent** from the 1.4.1 city's order list. Their behavior against a *properly typed* human gate is inferred from source, not run.

Cleanup: both throwaway cities live under the session scratchpad (`…/scratchpad/gc-city`, `…/scratchpad/gc-city2`) and the bd 1.2.2 binary under `…/scratchpad/bd122`. Nothing was written into any real project, and the global `bd` was never upgraded. `mise use -g github:gastownhall/gascity@1.4.1` did add a line to `~/.config/mise/config.toml`.

---

## Sources

- [Gas City Docs — Installation](https://docs.gascity.com/getting-started/installation) — **[OFFICIAL]**
- [Gas City Docs — Formula Specification v2](https://docs.gascity.com/reference/specs/formula-spec-v2) — **[OFFICIAL]**, "Last verified 2026-06-12"; §0.2 data model, §1.3 step field table (`gate` = "Async wait condition `{type, id, timeout}`"), §2 "Gates and waits_for", §4 "Accepted But Inert"
- [formula-spec-v2.md raw source](https://raw.githubusercontent.com/gastownhall/gascity/main/docs/reference/specs/formula-spec-v2.md) — **[OFFICIAL]**
- [Gas City Docs — How Gas City Works](https://docs.gascity.com/getting-started/how-gas-city-works) — **[OFFICIAL]**
- [Gas City Docs — Understanding Formulas](https://docs.gascity.com/guides/understanding-formulas) — **[OFFICIAL]**
- [Gas City Docs — Tutorial 06: Beads](https://docs.gascity.com/tutorials/06-beads) — **[OFFICIAL]**
- [gastownhall/gascity — internal/formula/compile.go](https://github.com/gastownhall/gascity/blob/main/internal/formula/compile.go) — gate synthesis, lines ~506–560 — **[OFFICIAL]** code-read
- [gastownhall/gascity — internal/formula/types.go](https://github.com/gastownhall/gascity/blob/main/internal/formula/types.go) — `type Gate struct { Type; ID; Timeout }`, doc-comment vocabulary `gh:run, gh:pr, timer, human, mail` — **[OFFICIAL]** code-read
- [gastownhall/gascity — orders/notify-on-human-gate-creation.toml](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/notify-on-human-gate-creation.toml) — **[OFFICIAL]**
- [gastownhall/gascity — assets/scripts/notify-on-human-gate-creation.sh](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/assets/scripts/notify-on-human-gate-creation.sh) — the `[ "$AWAIT_TYPE" = "human" ] || continue` filter — **[OFFICIAL]** code-read
- [gastownhall/gascity — orders/renudge-stale-human-gates.toml](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/renudge-stale-human-gates.toml) — **[OFFICIAL]**
- [gastownhall/gascity — assets/scripts/renudge-stale-human-gates.sh](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/assets/scripts/renudge-stale-human-gates.sh) — **[OFFICIAL]** code-read
- [gastownhall/gascity — orders/gate-sweep.toml](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/gate-sweep.toml) — **[OFFICIAL]**
- [gastownhall/beads — releases](https://github.com/gastownhall/beads/releases) — v1.2.2 (2026-08-15), v1.0.4 (2026-05-09) — **[OFFICIAL]**
- Shipped `CHANGELOG.md` in the gc 1.4.1 tarball, `[1.4.1] - 2026-08-15` entry ("beads pinned to v1.2.2 everywhere") — **[OFFICIAL]**
- Local CLI help output: `gc formula cook --help`, `gc init --help`, `bd init --help`, `bd gate --help`, `bd gate create --help`, `bd gate resolve --help` — **[EMPIRICAL]**
- All command transcripts in this document, run 2026-08-21 on darwin arm64 — **[EMPIRICAL]**
- `research-verification-probes.md` — Probes 1–3, 2026-08-24, the corrections applied above (GC_BEADS=file existence and its `gc bd` blockage) — **[EMPIRICAL]**
- `research-cycle-orchestration-fit.md` §1 — no `exec` step key in v2 formulas, cited for the CRIT-005 correction above — **[OFFICIAL]**
