**AVFL Adversary — Domain Fitness lens (domain_rule_compliance · convention_adherence · fitness_for_purpose)**
Corpus: 9 files, `docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/`. Skepticism 3, artifact stage final. Note for context: `final/` is empty — no synthesis exists to reconcile the conflicts below.

---

**DOMAIN-A-001** · **critical** · domain_rule_compliance · `research-hitl-alternative-patterns.md:§2 "Practical implication for Momentum"` + `:§7(b)`; `research-gate-mechanics-handson.md:"What this means for Momentum's four HITL points"` (design-consequence paragraph)

**Description:** The corpus's single most-repeated recommendation — route Momentum's gates through `bd gate create --type=human` instead of `[steps.gate]` — is specified as an **exec step inside a v2 formula**, a construct that does not exist. The failure mode is silent: the formula compiles, no gate is created, and the graph runs straight through the approval point.

**Evidence:** `research-hitl-alternative-patterns.md:§2`: *"In a Gas City v2 formula that means an ordinary `exec` step that shells `bd gate create --type=human --blocks <next-step-bead>` and exits."* `research-gate-mechanics-handson.md`: *"A formula step can shell out to `bd gate create --type=human --blocks <its own bead>`."* Both refuted by `research-cycle-orchestration-fit.md:§1`, which gives the exhaustive v2 step-key table (`id, title, description, description_file, notes, type, priority, tags, metadata, depends_on, needs, condition, children, assignee, expand, expand_vars, loop, waits_for, gate, check, retry, drain, on_complete, tally, timeout`) — *"There is no `exec`, `command`, `run`, or `script` key"* — paired with the spec warning *"Unknown step keys are silently ignored. A typo like `dependson` produces no diagnostic."* Two compounding defects: (i) the two docs prescribe **opposite `--blocks` targets** (`<next-step-bead>` vs `<its own bead>`), and the "own bead" variant collides with gate-mechanics' own Q2 bonus finding that a gate blocks *closure* (`cannot close gt-bvw: blocked by open issues [gt-2zt]`) — so the creating step can never close and, per `research-cycle-orchestration-fit.md:§2`, becomes a `claim_holder_stall_timeout` (5m floor) recycle candidate that re-runs and creates another gate; (ii) neither doc says how a step obtains a *successor's* bead id, which is cook-time (`gatetest.b -> gt-b3e`), not authoring-time.

**Suggestion:** Re-specify against a construct that exists. The three legitimate shell surfaces per `research-cycle-orchestration-fit.md:§1` are order-level `exec`, `[steps.check].check.path`, and `[order] check`; a fourth path is prose in a `description_file` instructing the *agent* to run `bd gate create`. Name which one, resolve `--blocks` to the downstream step, and specify bead-id discovery (e.g. `gc.root_bead_id` + `gc.step_ref`, as the pack check scripts do).

---

**DOMAIN-A-002** · **critical** · domain_rule_compliance · `research-gate-mechanics-handson.md:"City setup: what gc actually requires"` vs `research-beads-coupling-dec028.md:§2, §7`

**Description:** The corpus gives flatly opposite answers to the question that decides the DEC-028 coupling — *can Gas City run without Dolt?* — and the negative answer rests on a category error.

**Evidence:** `research-gate-mechanics-handson.md`: *"There is no `GC_BEADS=file` escape hatch in 1.4.1 — `bd init --help` states 'Dolt is the default (and only supported) storage backend.'"* But `bd init` selects **beads' own** storage backend; `GC_BEADS` selects **gc's** bead-store implementation (`BdStore` / `NativeDoltStore` / `FileStore` / `exec.Store`). `research-beads-coupling-dec028.md:§2` documents the file path from five primary sources on current `main`: the `factory.go` switch arm (`case provider == "file": … callStoreOpen("file store", opts.OpenFileStore)`) short-circuiting ahead of every Dolt eligibility check; gc's own error string `"bd not found in PATH (install beads or set GC_BEADS=file)"`; quickstart, FAQ and `TESTING.md` (`GC_BEADS=file` is the testscript default); the config-reference enum `"bd" | "file" | "exec:<script>"`; and `gc doctor` provider-awareness. The gate-mechanics author had gc 1.4.1 **installed** and never tested the claim. It is load-bearing: it feeds that doc's closing "Dependency consequence for the open DEC-028 Dolt go/no-go," while `research-beads-coupling-dec028.md:§7` builds the opposite recommendation (*"the low-risk topology is a city whose own work ledger is `GC_BEADS=file`"*).

**Suggestion:** Strike the `GC_BEADS=file` negative from gate-mechanics — unsupported, and its cited evidence describes a different tool's configuration. If retained in any form, verify directly (`GC_BEADS=file gc init` / `gc doctor` on the installed 1.4.1).

---

**DOMAIN-A-003** · **high** · fitness_for_purpose · `research-gate-mechanics-handson.md:"What this means for Momentum's four HITL points"` vs `research-maturity-open-bugs.md:"Momentum-relevant synthesis"`

**Description:** The two docs render **opposite verdicts on the post-sprint results gate** — the highest-stakes of the four — and the optimistic verdict comes from a probe structurally incapable of testing it. The seductive-demo trap in its exact form.

**Evidence:** gate-mechanics: *"(d) post-sprint results gate | **Fits**, same shape as (b) | Q3 [EMPIRICAL]."* maturity-open-bugs: *"(d) post-sprint results gate | needs a barrier over the conduct phase | **Blocked** — `waits_for` inert (#2311), container `needs` inert (#3451), `tally` removed"*, with the fatal detail that the prescribed #3451 workaround (*"enumerate the children explicitly in `needs`"*) **does not apply to Momentum**: *"Momentum's phase children are runtime-discovered — the story set is produced by sprint-planning, not known when the formula is authored."* The gate-mechanics probe was a 3-step linear chain (`A → B(gated) → C`) with *"No exec bodies, no agent, no provider — pure graph"*, on a city that was never started (`gc init` reported missing tmux/dolt/flock), every bead closed by hand. No fan-out, no `drain`, no `[[steps.children]]` — so it cannot speak to (d), or to the fan-out half of (c). Its own "Confidence and limits" concedes orchestrator-side behavior *"was **not** exercised"*, but the headline (*"works exactly as advertised"*) and the four-gate verdict table carry no such qualifier.

**Suggestion:** Downgrade (d) — and the fan-out-dependent half of (c) — to match the barrier evidence, or mark them untested by this probe. Propagate the "Confidence and limits" scope into the verdict table so a reader who reads only the table is not misled.

---

**DOMAIN-A-004** · **high** · domain_rule_compliance · `research-human-verdict-patterns.md:§5`; `research-maturity-open-bugs.md:"The gate surface today — the decisive finding (#4399)"`

**Description:** Two documents assert the inert `[steps.gate]` `type` vocabulary **costs Momentum nothing** for `human` gates. The corpus's own empirical work proves it costs the entire notification path — domain-plausible reasoning that is wrong, and the class of error that looks right to a non-expert.

**Evidence:** human-verdict-patterns: *"for `type = "human"`, it costs nothing: closing the gate bead is the human's job by definition. The one gate type that needs no watcher is the one Momentum needs."* maturity-open-bugs: *"**Why this is good news for Momentum specifically** … The inert vocabulary costs Momentum nothing for `human`; it costs `timer`, `gh:pr`, and `mail`, which Momentum does not need."* Both assume the only consumer of `type` is an auto-resolving watcher. `research-gate-mechanics-handson.md:"The defect"` measures the second consumer: a formula-cooked gate persists `await_type: null` (`{"id":"gt-crp",…,"await_type":null}`) while the ad-hoc path persists `"await_type":"human"` — and both bundled notify reflexes filter on `[ "$AWAIT_TYPE" = "human" ] || continue`. Its conclusion is the inverse: *"A `[steps.gate] type="human"` blocks correctly and tells nobody."* `research-notification-watcher-layer.md` independently confirms the payload gap (*"the bead.created payload omits await_type"*).

**Suggestion:** Correct both "costs nothing" statements to "costs the notification path, which is the half Momentum most needs," carrying gate-mechanics' `await_type` measurement in as evidence.

---

**DOMAIN-A-005** · **high** · fitness_for_purpose · `research-production-evidence.md:Finding 2`; `research-hitl-alternative-patterns.md:§4, §7(a), §7(d)` vs `research-notification-watcher-layer.md:"The release gap"`; `research-gate-mechanics-handson.md:"The notification gap"`

**Description:** Half the corpus treats the human-gate notification orders as **shipped machinery Momentum can use**; the other half proves empirically they are in **no tagged release**. Recommendations are built on the unavailable feature — including a warning about spam from an order that cannot spam because it does not ship.

**Evidence:** production-evidence: *"Two orders in the bundled `core` pack … This is the only production-grade HITL notification machinery Gas City **ships**."* hitl-alternative-patterns §4: *"Human gates therefore have a real, if young, escalation loop behind them"*; §7(a) advises against per-observation gates because *"the escalation loop (`renudge-stale-human-gates`, 1h interval) **would spam**"*; §7(d): *"the `renudge-stale-human-gates` order is **the existing precedent**."* Against this, notification-watcher enumerated the order directory **at both release tags**: raw fetches of the two files at `v1.4.1`, `v1.4.0`, `v1.3.5` all return **404** while `gate-sweep.toml` at `v1.4.1` returns 200; the only carrier is the `edge` rolling-main pre-release labelled *"not for production."* gate-mechanics corroborates: `gc order list` on a fresh 1.4.1 city returned 20 orders including `gate-sweep`, `nudge-mail-sweep`, `orphan-sweep` — and **neither** notify order.

**Suggestion:** Standardize the availability statement across all four docs to "authored on `main`/`edge` only; absent from every tagged release through v1.4.1; vendoring the two order files is the supported adoption path" (notification-watcher's gap #3 already states this correctly). Drop or re-scope the §7(a) spam warning and the §7(d) "existing precedent."

---

**DOMAIN-A-006** · **high** · fitness_for_purpose · `gemini-deep-research-output.md` (whole file; esp. Executive Summary, §4, Recommendations, Follow-Up Q1)

**Description:** The Gemini file carries **zero evidence tags and zero caveats** in a corpus where the other eight tier every claim `[OFFICIAL]/[EMPIRICAL]/[PRAC]/[UNVERIFIED]`, and it contradicts the empirically-verified findings on every decision-relevant point — in the reassuring direction. Its top recommendation is the one construction the corpus proves unsafe for a human gate. Nothing marks it as unreliable, and no synthesis exists to reconcile it.

**Evidence:** A grep for `unverified|caveat|limitation|confidence|OFFICIAL|EMPIRICAL` returns **one** hit (the word "empirical," in prose). Contradictions: (i) *"the Gas City ecosystem operates on the stable v1.4.0 release"* — three docs establish v1.4.1, 2026-08-15; (ii) dashboard as *"a React 19 SPA statically served by a Node 24 backend … defaulting to port 8082"* vs notification-watcher's *"single-page dashboard compiled into the `gc` binary, served at `http://127.0.0.1:8372/`"*; (iii) *"If a human gate is waiting and the pipeline is stalled, the system will periodically nudge the designated operator"* — the exact opposite of the proven zero-notification finding; (iv) Follow-Up Q1 concedes the notify scripts are absent from release notes but asserts *"Gas City does ship **functionally equivalent** … orders … gate-sweep, nudge-mail-sweep, nudge-on-route, cascade-nudge-on-blocker-close … not restricted to main/edge"* — `gate-sweep`'s two-line body (`gc bd gate check --type=timer --escalate`; `--type=gh --escalate`) **deliberately excludes human gates**, so "functionally equivalent" is false on the only axis that matters; (v) it attributes the `await_type` defect to *"beads Issue #1467"* and human-gate work to *"Issue #620"*, where the corpus tracks gascity **#4399**; (vi) *"the bmad pack enforces a mandatory 'readiness gate'. The DAG halts"* vs production-evidence's grep of all 315 pack TOMLs: `[steps.gate]` = **0**, `waits_for` = **0**. Most consequentially, Recommendation 1 — *"design formulas using `interaction_mode = interactive` and 'Check Loop' DAG topologies"* — is refuted twice: `interaction_mode` is *"an instruction to a language model, not a control-flow gate"* (human-verdict §6; hitl-alternative §3 quotes the README's own *"describes* human participation"), and a check loop *"does not wait … the loop burns its budget and closes the step failed."*

**Suggestion:** Head the file as untriangulated LLM output listing the refuted claims (v1.4.0-as-current, dashboard architecture, gate notification, "functionally equivalent" orders, issue numbers, bmad readiness gate, Recommendation 1), or annotate those passages inline `[REFUTED — see research-gate-mechanics-handson.md / research-production-evidence.md]`. As it stands, a reader following Recommendation 1 builds a gate that fails the step while the developer is away from the keyboard.

---

**DOMAIN-A-007** · **high** · fitness_for_purpose · corpus-wide; `research-notification-watcher-layer.md:"Glue scope estimate"` vs `research-cycle-orchestration-fit.md:§9 "The honest characterization of adoption cost"`

**Description:** The corpus **prices the small half of adoption and leaves the large half unpriced**, so the decision it exists to feed cannot be made from it.

**Evidence:** notification-watcher costs the gate glue precisely: watcher+notifier ~1–2d, last-mile ~0.5–1d, verdict capture + write-back ~3–5d, cursor durability ~1d, *"Total ≈ 6–9 days of glue **for one gate type**"* — and flags its own exclusion: *"That estimate assumes `gc` is installed and a city is running — neither is true in Momentum today, and neither is costed here."* cycle-orchestration-fit then names the uncosted work: *"this is not 'wrap conduct in a formula.' It is 're-express Momentum's phase orchestration as a pack' … a **rewrite of the orchestration layer**."* No document estimates that rewrite, and the surrounding constraints inflate it — every `description_file` >4096 bytes degrades to a pointer, `[steps.tally]` is removed so phase aggregation is bespoke pack logic, and every minor since 1.1 has required `gc doctor --fix`.

**Suggestion:** Add a rewrite-scope estimate to `research-cycle-orchestration-fit.md:§9`, anchored on the five methodologies that walked the path (bmad/superpowers/gstack/pr-pipeline/contributing) — e.g. their formula+asset file counts as a proxy — and state the combined figure so the go/no-go compares like with like.

---

**DOMAIN-A-008** · **high** · logical_soundness / fitness_for_purpose · `research-beads-coupling-dec028.md:§7 "Forced: nothing"` vs `research-cycle-orchestration-fit.md:§1–2`; `research-hitl-alternative-patterns.md:§8`

**Description:** The headline DEC-028 conclusion — *"Forced: nothing … DEC-028's go/no-go remains fully open and independently decidable"* — rests on a premise the corpus refutes elsewhere, and a third document reaches the opposite conclusion on the same axis.

**Evidence:** beads-coupling §7 derives it from: *"**Under the exec-order pattern DEC-032 D3 adopted (`claude -p /momentum:<skill>` as a shell subprocess)**, the phase step's payload is a story slug … Momentum's own state stays wherever Momentum keeps it."* `research-cycle-orchestration-fit.md`'s headline is that this pattern *"does not exist in Gas City, and the maintainers explicitly steer against building it"* — v2 steps *"are work beads that agents claim and execute"*, the 300s exec-order cap cannot host a phase, and a grep of all gascity-packs finds **zero** `claude -p` / `codex exec` invocations. Under the shape that *is* available (phases as formula steps routed to Claude Code agents), Momentum's phase work items **become city beads** — precisely the "second ledger stays separate" premise the decoupling argument depends on. Meanwhile `research-hitl-alternative-patterns.md:§8` concludes the opposite: *"Beads coupling is unavoidable for HITL … which **pulls directly on the open DEC-028 Dolt go/no-go**"* — itself an overstatement, since `bd gate` works today on Momentum's installed bd 1.0.4 with embedded Dolt and no authoritative flip.

**Suggestion:** Re-derive beads-coupling §7 under the pack/formula-step shape rather than the exec-order shape, and reconcile with hitl-alternative §8: separate "gate state lives in beads" (true today, no flip needed) from "beads becomes authoritative for Momentum work items" (a DEC-028 decision). Both docs conflate them, in opposite directions.

---

**DOMAIN-A-009** · **medium** · domain_rule_compliance · `research-cycle-orchestration-fit.md:§5`; `research-maturity-open-bugs.md:"Wedge bugs #2131 and #2168"`; `research-gate-mechanics-handson.md:"The defect"`

**Description:** The corpus never composes the failure mode the decision most needs: **what happens when the developer never resolves a gate.** Each piece sits in a different file; assembled, they describe a cycle that stops permanently and silently — and one file calls the mechanism "a feature."

**Evidence:** Piece 1 — cycle-orchestration §5: *"Before dispatching, the orchestrator checks whether the order already has open (non-closed) work. If it does, the order is skipped even when the trigger says it's due"*, glossed as *"For a Momentum cycle whose whole point is a single in-flight sprint, this default is a feature."* Piece 2 — gate-mechanics: a formula gate has no persisted `timeout`, so *"every gate a formula creates is a permanently-manual gate"* (framed as *fail-safe*). Piece 3 — per DOMAIN-A-005, no tagged release notifies on a human gate, and even the vendored renudge filters `await_type == "human"`, which formula gates do not set. Composed: an unresolved gate leaves the order's work open → the order is skipped every tick → the cycle stops → nothing tells anyone. maturity-open-bugs names exactly this signature for the *wedge* class — *"the failure mode of this class is **silence** … cycle stalls will look identical to 'nothing was due.' Any adoption needs an external liveness check"* — but no document extends that prescription to the unresolved-gate case.

**Suggestion:** Add an explicit unresolved-gate failure-mode analysis composing these three facts, and extend the external-liveness-check recommendation to cover it (e.g. a Momentum-side sweep of `bd gate list --status open` with an age threshold, independent of any gc order).

---

**DOMAIN-A-010** · **medium** · domain_rule_compliance · `research-maturity-open-bugs.md:"Momentum-relevant synthesis"`; `research-human-verdict-patterns.md:§1`

**Description:** The only sanctioned barrier construction for gate (d) is `drain` + a check loop — but a check loop **cannot carry a gate on the same step**, and check-loop exhaustion **closes the step failed**, a terminal state whose effect on the downstream gate is never analyzed.

**Evidence:** maturity-open-bugs: *"`drain` plus a `check` loop is the only sanctioned construction"* / *"Anything Gas City orchestrates for Momentum must express 'wait for all of phase N, then ask the human' using `drain` + a check loop."* human-verdict-patterns §1 quotes the hard constraint: *"`check` must not be combined with `loop`, `on_complete`, **`gate`**, `expand`, `assignee`, or `retry`"*, and the exhaustion semantics: *"exhaustion closes the step as failed"*, with *"no 'the human said no, and that's a legitimate outcome' encoding."* It also notes a check loop *respawns the agent work* each failed attempt — so a barrier polling "are all stories done?" re-runs the barrier step's work per iteration. No document establishes whether a *failed* close still releases dependents; gate-mechanics' Q4 completion walk (each close releasing the next step) suggests it does, which would open the results gate on a barrier that never confirmed the phase finished.

**Suggestion:** Specify the drain+check barrier concretely for a long conduct phase — `max_attempts` and `check.timeout` sized against realistic sprint duration — and state what a failed-close barrier does to the downstream gate. If a failed close releases dependents, the construction needs a guard (the gate blocking on a separate completion-assertion bead, not on the check step).

---

**DOMAIN-A-011** · **medium** · convention_adherence · corpus-wide (absent from all 9 files)

**Description:** The corpus proposes chaining triage→planning→conduct→retro **out of session** with human gates at four named points, and never addresses two binding Momentum rules an unattended cycle collides with: `git push` always requires explicit approval, and sprint completion mandates a version bump plus push.

**Evidence:** A grep across all nine files for `git-discipline|autonomous.push|git push|push approval` returns exactly **one** hit — `research-beads-coupling-dec028.md:§7`, a table cell reading *"G3 — was Dolt sync manageable under git-discipline?"*, which concerns Dolt sync, not push authority. `~/.claude/rules/git-discipline.md` states *"`git push` always requires explicit user confirmation"*; `.claude/rules/version-on-release.md` requires a version-bump commit and push when a sprint merges to main. Momentum's conduct phase performs worktree→sprint-branch merges autonomously but terminates at a step that by rule cannot run unattended. The corpus enumerates four HITL gates where Momentum's own rules imply a fifth.

**Suggestion:** Add a constraint row to `research-cycle-orchestration-fit.md:§9`'s fit table covering push/merge authority under out-of-session orchestration — either a fifth gate on the merge/push step, or an explicit statement that the cycle terminates before push and hands off.

---

**DOMAIN-A-012** · **medium** · domain_rule_compliance · `research-production-evidence.md:Finding 7`

**Description:** The maturity assessment correctly discards stars, then uses **Homebrew macOS installs as a hard ceiling** on the possible user population — while the corpus itself documents three non-Homebrew install paths, one of which is what its own hands-on researcher used.

**Evidence:** production-evidence: *"Adoption (Homebrew installs, the least gameable number available)"* — gascity 669/30d, 962/90d, 1,022/365d — concluding *"Roughly 700 monthly macOS installs is also **the ceiling** on how large the population of possible human-gate users can be. Within that population, zero published a gated formula."* But `research-gate-mechanics-handson.md:"Environment and versions"` installed via `mise use -g github:gastownhall/gascity@latest`, stating *"No brew, no ubi fallback … **the mise github backend is the clean install path for this machine**"*; `research-cycle-orchestration-fit.md:§3` quotes the project's own docs: *"Best practice right now is to build your own `gc` binary from HEAD"*; and Homebrew analytics exclude Linux entirely. The same section's release-asset counts (~1,800/release, ~9,500 across v1.x) are a second uncounted channel.

**Suggestion:** Reframe as a floor with named uncounted channels (mise/github backend, source builds from HEAD, Linux, release-asset downloads). The *directional* conclusion — small user base, zero public gated formulas — survives; the numeric bound does not.

---

**DOMAIN-A-013** · **medium** · fitness_for_purpose · `research-maturity-open-bugs.md:"Project shape and release cadence"` vs `research-notification-watcher-layer.md:"What already exists upstream"` and `research-production-evidence.md:Finding 7`

**Description:** The two maturity signals feeding the go/no-go most directly — open-issue backlog and contributor concentration — are reported at materially different magnitudes across documents: same repo, same day, all tagged `[EMPIRICAL]`, unreconciled, with no stated query method.

**Evidence:** Open issues: maturity-open-bugs reports *"**575 open issues** against 380 issues closed from the May-onward cohort"*; notification-watcher reports *"**1,011 open issues** [EMPIRICAL, GitHub API]"*; production-evidence reports *"**1,011 open vs 718 closed** all-time — open issues exceed lifetime closures"* and builds a *"1,729 issues (1,011 open + 718 closed)"* census on it. A 1.76× gap, most likely PR-inclusive vs issues-only counting, but neither states its query. Top-contributor share: maturity-open-bugs derives 52.2% / 51.8% from two sampled commit windows; production-evidence derives 66.2% all-time (`julianknutsen` 3,601 of 5,437). Both reach "bus factor ≈ 1–2," but the reader gets two headline percentages.

**Suggestion:** State the exact query behind each count (`is:issue is:open` vs `open_issues_count`, which includes PRs) and use one figure corpus-wide; note the sampled-window vs all-time distinction where contributor percentages differ. The conclusions are robust — the numbers should stop disagreeing.