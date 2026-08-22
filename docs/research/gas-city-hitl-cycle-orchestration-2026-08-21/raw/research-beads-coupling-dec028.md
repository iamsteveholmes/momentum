---
content_origin: claude-code-subagent
date: 2026-08-21
sub_question: "Beads coupling and DEC-028 implications: what Gas City requires of beads (Dolt vs GC_BEADS=file in current releases); what adoption forces on the open Dolt migration go/no-go"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

# Beads Coupling and DEC-028 Implications

## Bottom Line

**Gas City does not force Dolt, and adopting it for cycle orchestration does not force DEC-028's "flip beads authoritative" decision either way.** `GC_BEADS=file` survives intact in current main and in the v1.4.1-era docs — it is the documented lightest-start path, the CI/testscript default, and the remediation string the binary itself prints when `bd` is missing. What Gas City *does* force is a **second, separate work ledger** with its own lifecycle, because a city always keeps its own bead store regardless of provider. The genuinely new coupling risk is not Dolt-the-database — it is **Dolt-the-exclusive-write-lock**: Gas City refuses to start a managed Dolt against a `.beads/dolt` directory that a standalone `bd dolt start` already holds. Momentum's dual-write spike runs exactly such a store.

The DEC-028 implication is therefore **decoupling, not forcing**: Gas City adoption removes the last remaining argument that Momentum needs Dolt-authoritative beads to get dependency-driven dispatch, because the dispatcher can run its own file-backed ledger while `.momentum/*/index.json` stays authoritative. Conversely, it adds one new *reason* to flip — a single shared store would collapse Momentum's ledger and the city's ledger into one queryable substrate — at the price of importing the Dolt operational runbook.

---

## 1. The Provider Contract as It Stands Today

Gas City's bead store is a single Go interface with four implementations, selected at process start. The architecture doc names the interface's ten methods — "Create, Get, Update, Close, List, Ready, Children, ListByLabel, SetMetadata, and MolCook" — and the four backing stores ([gascity engdocs/architecture/beads.md](https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/beads.md)) **[OFFICIAL]**:

| Implementation | Backing | Notes |
|---|---|---|
| `BdStore` | `bd` CLI → Dolt | Production default; adds admin ops (Init, ConfigSet, Purge) not on the interface |
| `NativeDoltStore` | in-process Dolt via linked Go library | Selected in preference to `BdStore` when eligible (see §6) |
| `FileStore` | JSON file, atomic temp-file + `os.Rename` | Embeds `MemStore`; no Dolt, no `bd`, no `flock` |
| `MemStore` | in-memory slice | Test double; `SetMetadata` is a no-op |
| `exec.Store` | user script over JSON stdin/stdout | Forward-compatible: exit code 2 = unknown operation |

Resolution order is `GC_BEADS` env var → `[beads].provider` in `city.toml` → default `"bd"`. I verified this against the actual selection site rather than the prose. In `cmd/gc/main.go`, `openStoreResultAtForCityWithConfig` resolves the provider, then hands it to `beads.OpenStoreAtForCity`, whose first switch arm is literally **[OFFICIAL]**:

```go
switch {
case provider == "file":
    store, err := callStoreOpen("file store", opts.OpenFileStore)
    return opts.stampedResult(StoreOpenResult{Store: store,
        Diagnostic: BeadsDiagnostic{Store: storeNameFileStore}}, err)
```

([internal/beads/factory.go](https://github.com/gastownhall/gascity/blob/main/internal/beads/factory.go), fetched from `main` on 2026-08-21). The `file` branch short-circuits ahead of every native/Dolt eligibility check — there is no fall-through that could quietly re-introduce Dolt.

The exec provider is the escape hatch for anything else. Its contract page documents `provider = "exec:/path/to/script"` in `city.toml` (or `GC_BEADS=exec:...`) and the five variables Gas City sets before invoking the script: `GC_PROVIDER`, `GC_STORE_ROOT`, `GC_STORE_SCOPE` (`city` or `rig`), `GC_BEADS_PREFIX`, and `GC_RIG`/`GC_RIG_ROOT` for rig scope ([Exec Beads Provider reference](https://docs.gascity.com/reference/exec-beads-provider)) **[OFFICIAL]**. The page explicitly contemplates alternate engines — "`beads_rust` (SQLite + JSONL), Postgres, SQLite, flat files, or custom persistence with S3/git integration."

**What was removed:** the `"sqlite"`, `"sqlite-cgo"`, and `"coordstore"` providers now hard-error at store-open with a message naming `"doltlite"` as the migration target **[OFFICIAL]**. This matters only as evidence of churn on this seam — none of the three ever applied to Momentum.

---

## 2. `GC_BEADS=file` Is Alive, Documented, and Load-Bearing

DEC-032 D3 (2026-05-22) committed Momentum's Gas City PoC to `GC_BEADS=file` specifically to remove Dolt. Three months later that path is not merely surviving — it is referenced from five independent places in current `main` **[OFFICIAL]**:

1. **Quickstart prerequisites:** "You will need `gc`, `tmux`, `git`, `jq`, and a beads provider (`bd` + `dolt` by default, or set `GC_BEADS=file` to skip them)." ([quickstart.md](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/quickstart.md))
2. **FAQ dependency answer:** "The full runtime set is tmux, jq, git, dolt, bd (the beads CLI), and flock… For the lightest possible start, `GC_BEADS=file` skips the dolt + bd pair." ([faq.md](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/faq.md))
3. **The binary's own error string:** `requireBdBinaryForCity` returns `"bd not found in PATH (install beads or set GC_BEADS=file)"` (cmd/gc/main.go).
4. **CI/testscript default:** "Testscript defaults missing backend env vars to local fakes: `GC_SESSION=fake`, `GC_BEADS=file`, `GC_DOLT=skip`" ([TESTING.md](https://github.com/gastownhall/gascity/blob/main/TESTING.md)). The env-var fake table lists `GC_BEADS` values as `file`, `bd`, `(absent)`.
5. **Supply-chain opt-out (CHANGELOG 1.2.0, 2026-05-25):** when native bd store selection linked "the upstream Beads/Dolt Go library stack into `gc`… deployments that do not want that path can keep using `GC_BEADS_FORCE_FALLBACK=1` or `GC_BEADS=file`." **[OFFICIAL]**

The config reference confirms the enum in the schema: `provider` — `"bd"` (default, Dolt-backed), `"file"`, or `"exec:<script>"` ([config reference](https://docs.gascity.com/reference/config.md)) **[OFFICIAL]**.

`gc doctor` is provider-aware: `NewBinaryCheck` takes a `skipMsg` used "when the binary is not needed due to env config like `GC_BEADS=file`", and `BuiltinPackFamilyCheck` returns OK with "builtin bd/dolt pack family not required" when the provider does not use the bd/Dolt store ([internal/doctor/checks.go](https://github.com/gastownhall/gascity/blob/main/internal/doctor/checks.go)) **[OFFICIAL]**. So the file path is a first-class supported configuration, not a degraded mode the health checker complains about.

**What `file` costs.** Ordering semantics differ but do not degrade: "in-process stores (MemStore, FileStore) guarantee creation order for List and Ready," where `BdStore` returns bd's default sort **[OFFICIAL]**. `Ready` — the dependency-aware readiness query that is the whole point of beads for Momentum — is on the interface and implemented by FileStore. The concrete known gap is `SetMetadata`, a no-op on `MemStore`; the architecture doc says FileStore "embeds MemStore and adds JSON file persistence," and does not state that `SetMetadata` is overridden. **[UNVERIFIED]** — I could not confirm from the fetched material whether FileStore persists metadata; if Momentum's cycle relies on bead metadata key/value state under a file provider, this needs a hands-on check before it is assumed.

---

## 3. Storage Bindings and Split Storage Classes

The bigger structural change since May 2026 is that "the bead store" is no longer one thing. A city now stores **six semantic classes**: one **work ledger** (tasks, epics, bugs, convoys) and five **infrastructure** classes (execution graph, session lifecycle, messaging, orders, nudge queue). By default all six live in the work ledger ([Split Storage Classes runbook](https://docs.gascity.com/runbooks/split-storage-classes.md)) **[OFFICIAL]**.

```toml
[storage.classes]
work = "work"
graph = "infra"
sessions = "infra"
messaging = "infra"
orders = "infra"
nudges = "infra"

[storage.bindings.infra]
provider = "sqlite-beads"
path = ".gc/store"
```

Three constraints are load-bearing for any Momentum adoption plan **[OFFICIAL]**:

- **All-or-nothing.** "All six assignments are required once `[storage]` exists. This build serves the whole split or none of it: either every class names `work`, or work names `work` and all five infrastructure classes name one shared binding. Anything else is refused at startup rather than routed halfway."
- **Boot never migrates.** After the config swap, `gc start` deliberately *refuses* with a message naming `gc storage migrate --from-work`, which requires `gc stop` plus a `--fleet-stopped` operator attestation. The migration censuses rig scopes, refuses by id and rig if infrastructure beads sit in a rig scope, copies with dependency topology preserved, reopens the destination and proves field-level equality against bytes on disk, then records a convergence marker. The source is never mutated.
- **The `work` binding is reserved and synthesized.** Per `examples/storage/storage-bindings.toml`: "The reserved `work` binding is synthesized from the city's own work topology: it needs no definition here and must not be redefined." **[OFFICIAL]**

That last point is the one that answers the Dolt question cleanly. **The `[storage]` split does not change how the work ledger is stored** — the work ledger's engine is still whatever `[beads].provider` / `GC_BEADS` selects. So the split is orthogonal to the Dolt decision, and a fully Dolt-free city is expressible: `GC_BEADS=file` for work, `sqlite-beads` for the five infrastructure classes. The claimed payoff for splitting is real but scale-dependent: "130–250× lower latency for infrastructure-class reads" on a production-scale city, "because those reads stop competing with the work ledger's own traffic." At Momentum's volume that is a non-reason to split.

A third built-in provider appears only at the binding layer — `beads-workspace`, "the one provider whose backing store may itself be remote," taking a `url` plus an `auth` *reference* (`gasworks` or `env:NAME`, never an inline credential). Not relevant to a local solo practice, but it is the seam where a hosted future would arrive.

---

## 4. The Dolt Operational Burden, Quantified

Two runbooks exist because Dolt-backed cities have hurt people. Both are worth reading as the honest price list for the `bd`/Dolt provider.

**Dolt bloat.** Every write is an immutable chunk in `.dolt/noms/`; auto-GC triggers only at roughly **125 MB of new chunks**, so "during heavy write activity followed by quiescence, a database can balloon to peak size and remain there indefinitely because the threshold is never reached again." Symptoms: `gc doctor` flags `dolt-noms-size`; `.dolt/` exceeds **20 GB**; bead writes and `bd ready` slow; agents hit Dolt connection/timeout errors after startup. Recovery is `gc stop` → back up `.dolt/` → `dolt gc --archive-level=1` (**tens of minutes for 120 GB**) → `gc start` + `gc doctor`. Expected result: 120 GB commonly shrinks to **5–20 GB**; below 10% reduction means the history is legitimate and the case escalates. Prevention requires Dolt ≥ 2.1.0, a continuously-running embedded `mol-dog-compactor` order (which requests a **24-hour timeout** operators must not cap below), daily `gc doctor` via cron, and avoiding long-lived external `dolt sql` sessions ([dolt-bloat-recovery](https://docs.gascity.com/troubleshooting/dolt-bloat-recovery.md)) **[OFFICIAL]**.

**bd auto-backup accumulation.** `bd` maintains a Dolt-native backup under `<root>/.beads/backup/` on a remote named `backup_export`, and "there is no retention, rotation, or garbage-collection logic in the bd auto-backup path today." `gc doctor` warns at **5 GB** and errors at **15 GB**; a documented incident ("qlandia") reached **34 GB** and filled the disk, cascading into Dolt mmap write failures and supervisor reconciler failure. Least-invasive fix: `bd config set backup.enabled false && rm -rf .beads/backup/`. Diagnostic tell: `.darc` archives mean conjoin succeeded; many `nbs_table_*` files mean conjoin is failing ([bd-backup-cleanup](https://docs.gascity.com/troubleshooting/bd-backup-cleanup.md)) **[OFFICIAL]**.

**Calibration against Momentum's actual store [EMPIRICAL]** — measured 2026-08-21 in `/Users/steve/projects/momentum`:

```
$ du -sh .beads .beads/backup .beads/embeddeddolt
2.5M  .beads
608K  .beads/backup
1.8M  .beads/embeddeddolt
$ ls .beads/backup | head -1   →  0qh6bo2loaeti3bgcop2fbbg14igdh3i.darc   (20 files, all .darc)
```

Momentum's entire beads footprint is **2.5 MB against a 5 GB warning threshold** — roughly 0.05% — and every backup file is a `.darc` archive, the healthy conjoin signal. The Dolt operational runbook describes a failure mode that is real at fleet scale and effectively unreachable at solo-practice scale. **The burden is not a reason to avoid Dolt for Momentum; it is a reason to keep `bd config set backup.enabled false` in reach and run `gc doctor` on a cron if a city ever goes Dolt-backed.**

Note the asymmetry: the bloat runbook and the compactor prescription assume a **managed, long-lived Dolt server** run by a city. Momentum today runs bd's *embedded* Dolt (`.beads/embeddeddolt/`) with no server process, no `dolt` binary on PATH, and no continuous write load. Those are different operating regimes.

---

## 5. Coexisting With Momentum's Existing Standalone `bd` Database

This is the sharpest finding and it is not in the guides — it is in the changelog.

> "Managed bd provider startup now detects a bd-standalone dolt server running against the same `.beads/dolt` database before invoking the managed-bd lifecycle script, and refuses with a message naming `bd dolt stop` as the unblock. This covers `gc start`, `gc init`, and `gc rig add` provider convergence paths. Previously, running `bd dolt start` while a city was registered at the same path would leave the standalone dolt holding the exclusive write lock; the city-managed dolt could not acquire it and startup failed with a generic 'dolt server could not start via gc helper' error that did not point at the lock holder."
> — [gascity CHANGELOG](https://github.com/gastownhall/gascity/blob/main/CHANGELOG.md) **[OFFICIAL]**

**Read plainly: a Dolt-backed city and a standalone `bd dolt` server cannot share a `.beads/dolt` at the same time.** They contend on an exclusive write lock. Current gc detects it and refuses with a clear remediation instead of failing obscurely — an improvement, but the constraint stands. Momentum's dual-write spike keeps `.beads/` at the repo root (gitignored per `.gitignore:87`) with an embedded Dolt; registering `~/projects/momentum` as a rig in a Dolt-backed city puts these two on a collision course by design.

The topology doc explains why the collision is structural: "one shared Dolt server, with each scope's beads tagged by an `issue_prefix` that the `bd` CLI uses as a hard query filter." Only the city root runs Dolt; rigs inherit the endpoint via `gc.endpoint_origin: inherited_city`, while `managed_city` means the city runs local Dolt with the port in `.beads/dolt-server.port`. Isolation between rigs is **prefix scoping enforced at the bd query layer**, not separate databases ([beads-topology](https://docs.gascity.com/reference/internal/beads-topology.md)) **[OFFICIAL]**.

There is, however, a supported way out — an **externally-bound scope**. In `cmd/gc/bd_env.go`, `scopeStoreIsExternallyBound` is documented as "the single predicate for 'gc does not own this store': which bd binary to run, whether to project a Dolt environment, whether to manage or recover a Dolt runtime, and whether the scope needs a local Dolt identity are all the same question asked from different places." When a scope carries a complete storage binding, `bdContextCommandRunnerForCity` delegates to the workspace-pinned `bd` and explicitly sets `BEADS_DOLT_AUTO_START=0`, `BD_EXPORT_AUTO=false`, and blank `GC_RIG`/`GC_RIG_ROOT` **[OFFICIAL]**. That is precisely the "hands off, this store isn't yours" mode a pre-existing Momentum bd database would want. It also requires a configured absolute `workspace.env PATH` containing a `bd` executable, or gc errors: `"workspace.env PATH is configured but contains no executable bd at an absolute path"`.

**Practical recommendation:** the low-risk topology is a city whose *own* work ledger is `GC_BEADS=file`, with Momentum registered as a rig. That sidesteps the lock question entirely because no Dolt server exists on the city side. The externally-bound path is the fallback if the city later needs Dolt.

---

## 6. Version Coupling — the Constraint Nobody Would Predict

Momentum's installed toolchain, measured 2026-08-21 **[EMPIRICAL]**:

```
$ bd version   →  bd version 1.0.4 (ce242a879: sprint/sprint-2026-08-03@ce242a879678)
$ command -v gc dolt flock tmux   →  all NOT-INSTALLED
```

Gas City's stated floors: `dolt` **≥ 2.1.0**, `bd` **≥ 1.0.0**, plus tmux/jq/git/flock ([installation](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/installation.md)) **[OFFICIAL]**. The docs add: "Use a final Dolt 2.1.0 or newer. Gas City's managed Dolt checks reject older and pre-release builds… releases before 1.86.2 can also miss the upstream GC/writer deadlock fix in dolthub/dolt commit `ccf7bde206`, which can hang `dolt_backup sync` under heavy write load."

`deps.env` in current `main` is more revealing than the docs **[OFFICIAL]**:

```
DOLT_VERSION=2.1.7
BD_VERSION=v1.1.0
BD_PREV_VERSION=v1.0.4      # "the minimum-supported bd"
BD_CURRENT_VERSION=v1.1.1-0.20260805093327-bf97b73749ac
```

**Momentum sits exactly on `BD_PREV_VERSION` — the documented floor of Gas City's cross-version contract-test matrix.** That is the good news: bd 1.0.4 is explicitly tested, not merely tolerated. Gas City even carries a config knob for it: `[beads].bd_compatibility`, whose "Empty defaults to `bd-1.0.4`, which keeps claimable work history-backed and avoids bd ready/list flags that are unavailable or incomplete in bd 1.0.4" (enum: `bd-1.0.4`, `bd-1.0.5`) ([config reference](https://docs.gascity.com/reference/config.md)) **[OFFICIAL]**. So the default posture assumes Momentum's exact version, at a documented cost in `bd ready`/`bd list` flag surface.

Two adjacent facts belong in any DEC-028 re-evaluation **[OFFICIAL]**:

- **beads v1.0.5 was withdrawn for a data-corruption bug.** CHANGELOG 1.3.1: gascity "repins `beads` Go module and CI `bd` toolchain to v1.0.4 (avoiding withdrawn v1.0.5 with known data-corruption bug)." DEC-028's Gate 3 asked whether Dolt sync was manageable; an upstream withdrawn release for data corruption in the same window is direct evidence about the substrate's maturity, independent of Momentum's own experience.
- **Compare-and-swap writes are not yet available in any published bd.** `deps.env` states the capability boundary is one commit — `--if-assignee`/`--if-status` with exit 13 on a rejected precondition, landed on beads main in `6e8af8bf8` (beads#5008, 2026-07-24) — and that "the newest published release — v1.1.2 — was cut from the hotfix/v1.1.1 branch off v1.1.0 and predates both." Gas City's `[beads].conditional_writes` therefore defaults to `"off"`, with `"auto"` meaning "CAS where the store is capable, loud degrade otherwise." **Multi-agent write safety via CAS — one of DEC-028 D1's stated wins — is still not reachable from a published bd release as of 2026-08-21.**

One more coupling that touches Momentum's working tree: `[beads].event_hooks` defaults to **true**, installing `.beads/hooks/on_create,on_update,on_close` that shell out to `gc event emit` on every bead write. The reference notes these are removable ("set to false once the controller's native cache-events already observe bead changes — the `bd_hooks` doctor gate") and that git hooks are left untouched **[OFFICIAL]**. Momentum's `.beads/hooks/` currently holds only git hooks (`post-checkout`, `post-merge`, `pre-commit`, `pre-push`, `prepare-commit-msg`) **[EMPIRICAL]**, so gc would be adding files, not overwriting. Relatedly, `scopeHasExecutableBdHooks` in `factory.go` disqualifies the fast in-process `NativeDoltStore` when non-gc-stamped bd hooks exist — a performance-only consequence, and only under a Dolt provider.

---

## 7. What Adoption Forces or Unlocks for DEC-028

DEC-028's Migration Go criterion is: 3 of 4 gates positive → flip beads authoritative; fewer than 3 → keep the JSON model and retain only the spike's dependency engine. DEC-032 already recorded the linkage, listing "DEC-028 D3 — EXTENDED: Gas City is the event-driven trigger layer that makes Beads-driven DAG dispatch reactive; Beads remains standalone-capable as lifecycle state."

**Forced: nothing.** This is the headline. A Gas City cycle orchestrator can run on `GC_BEADS=file` and never touch Dolt, `bd`, or Momentum's `.beads/` at all. The city's beads are the city's own execution state — sessions, mail, convoys, formula steps, orders — and there is no requirement that Momentum's work items live there. Under the exec-order pattern DEC-032 D3 adopted (`claude -p /momentum:<skill>` as a shell subprocess), the phase step's payload is a story slug or a sprint slug; Momentum's own state stays wherever Momentum keeps it. **DEC-028's go/no-go remains fully open and independently decidable.**

**Unlocked (a) — the "we need Dolt for dispatch" argument dies.** DEC-028 D1's headline win was `bd ready` + atomic `--claim` replacing hand-built dependency logic. Gas City supplies its own claim protocol on top of *whatever* store: "`gc hook --claim` queries ready beads (blocked work stays invisible) and atomically claims unassigned tasks" ([tutorial 06](https://docs.gascity.com/tutorials/06-beads.md)) **[OFFICIAL]**, and `Ready` is on the Store interface every implementation satisfies. If the dependency engine is the thing Momentum actually wanted, it is reachable without Dolt-authoritative state. That materially weakens the case for the flip.

**Unlocked (b) — but a shared store becomes newly attractive.** If Momentum ever wants a single queryable substrate spanning practice work items *and* orchestration state — one `bd sql` reaching sprint stories, phase steps, and gate outcomes together — the aligned configuration is: flip beads authoritative (DEC-028 Phase 3), let the city use the `bd` provider, and register Momentum as a rig with prefix scoping. That is the only topology where the two ledgers are one. The `[storage]` split then gives the escape valve if the shared ledger gets hot: infrastructure classes move to `sqlite-beads`, work stays in Dolt.

**Constrained — the lock, not the database.** Whichever way DEC-028 goes, a Dolt-backed city cannot coexist with a live standalone `bd dolt` server on the same `.beads/dolt`. If Momentum flips authoritative *and* runs a Dolt city, the store must be unified or externally bound; two independent Dolt servers on one directory is not an available configuration.

**Re-scored against DEC-028's own gates:**

| Gate | New evidence from Gas City | Direction |
|---|---|---|
| G1 — did `bd ready`/`--claim` simplify scheduling? | `Ready` is provider-independent; `gc hook --claim` supplies it over FileStore too | Weakens the case for flipping — the win is obtainable without Dolt |
| G3 — was Dolt sync manageable under git-discipline? | v1.0.5 withdrawn for data corruption; bloat + unbounded backup runbooks exist; but Momentum's store is 2.5 MB / 0.05% of the warn threshold | Mixed; burden is real at fleet scale, negligible at solo scale |
| G4 — did `--spec-id` linkage hold without in-tree loss? | Unchanged by Gas City. D3's "story `.md` stays in the git tree" is untouched — Gas City stores *its* beads, not Momentum's prose | Neutral |
| Multi-agent write safety (D1 rationale) | CAS `--if-assignee`/`--if-status` unavailable in any published bd; `conditional_writes` defaults `off` | Weakens — the safety win is not yet purchasable |

**Recommended sequencing:** evaluate Gas City on `GC_BEADS=file` as DEC-032 D3 already specified, treat the city's ledger as disposable orchestration state, and let DEC-028 be decided on its own merits with the dispatch argument removed from its ledger. Revisit the shared-store topology only if a concrete cross-domain query need appears.

---

## 8. Open Questions and Unverified Points

- **FileStore metadata durability.** Whether `FileStore.SetMetadata` persists or inherits `MemStore`'s no-op is not stated in the fetched material **[UNVERIFIED]**. If Gas City's own gate/step bookkeeping rides on bead metadata, this is a hands-on must-check before trusting a file-backed city with `[steps.gate]` state.
- **No hands-on run.** `gc`, `dolt`, `flock`, and `tmux` are all absent from this machine **[EMPIRICAL]**, so nothing here is behaviorally verified. Every claim above is source-code or documentation grounded.
- **`[beads].backend = "doltlite"`** appears in the config schema ("T3Code uses `doltlite` for local dev stores") and is the named migration target for the removed sqlite providers, but has no guide page. It may be a lighter Dolt regime worth evaluating as a middle path between `file` and managed Dolt — undocumented at guide level as of 2026-08-21.
- **Release currency.** Latest tagged release is **v1.4.1 (2026-08-15)**; v1.4.0 (2026-07-24) landed the store lifecycle work. Source claims above are from `main`, which is ahead of v1.4.1 and may contain unreleased behavior. All sources cited are within the last 4 months; none are older than 2 years.

---

## Sources

**Official documentation (docs.gascity.com)**
- [Exec Beads Provider reference](https://docs.gascity.com/reference/exec-beads-provider)
- [Config reference](https://docs.gascity.com/reference/config.md)
- [Beads storage topology (internal reference)](https://docs.gascity.com/reference/internal/beads-topology.md)
- [Tutorial 06 — Beads](https://docs.gascity.com/tutorials/06-beads.md)
- [Runbook — Split Storage Classes](https://docs.gascity.com/runbooks/split-storage-classes.md)
- [Troubleshooting — Dolt Bloat Recovery](https://docs.gascity.com/troubleshooting/dolt-bloat-recovery.md)
- [Troubleshooting — bd Auto-Backup Cleanup](https://docs.gascity.com/troubleshooting/bd-backup-cleanup.md)
- [Documentation index (llms.txt)](https://docs.gascity.com/llms.txt)

**Official source (github.com/gastownhall/gascity, `main` @ 2026-08-21)**
- [engdocs/architecture/beads.md](https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/beads.md)
- [internal/beads/factory.go](https://github.com/gastownhall/gascity/blob/main/internal/beads/factory.go)
- [cmd/gc/main.go](https://github.com/gastownhall/gascity/blob/main/cmd/gc/main.go)
- [cmd/gc/bd_env.go](https://github.com/gastownhall/gascity/blob/main/cmd/gc/bd_env.go)
- [examples/storage/storage-bindings.toml](https://github.com/gastownhall/gascity/blob/main/examples/storage/storage-bindings.toml)
- [deps.env](https://github.com/gastownhall/gascity/blob/main/deps.env)
- [CHANGELOG.md](https://github.com/gastownhall/gascity/blob/main/CHANGELOG.md)
- [TESTING.md](https://github.com/gastownhall/gascity/blob/main/TESTING.md)
- [docs/getting-started/quickstart.md](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/quickstart.md)
- [docs/getting-started/faq.md](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/faq.md)
- [docs/getting-started/installation.md](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/installation.md)
- [Releases](https://github.com/gastownhall/gascity/releases)

**Momentum internal artifacts**
- `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/decisions/dec-028-beads-tracker-memory-substrate-adoption-2026-05-16.md`
- `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/decisions/dec-032-gas-city-dispatcher-adoption-2026-05-22.md`
- `/Users/steve/projects/momentum/.beads/` (empirical measurements, 2026-08-21)
