## Findings — ACCURACY lens (Adversary framing), corpus mode, 9 files, stage=final, skepticism=3

Note on method: I spot-checked seven contested claims against docs.gascity.com and the GitHub API. Those verifications are quoted inline where they settle a cross-document dispute.

---

**id:** ACCURACY-A-001
**severity:** critical
**dimension:** correctness
**location:** `gemini-deep-research-output.md:§6 Table 3 (Mitigated and Persistent Architectural Bugs)`
**description:** All three rows of the bug table are factually wrong, and two of them misidentify the *subject* of the issue entirely. #2311 is described as a `gc dolt health --json` orphan-misclassification data-loss path and marked "Patched"; #3451 is described as a Homebrew/Docker container-deployment dependency gap. Both are wrong, and both are precisely the two gaps that block Momentum's post-sprint results gate. #2131/#2168's fix is attributed to v1.4.0 (2026-07-24) when it shipped in the v1.2 window.
**evidence:** gemini: *"Barrier Race & False Orphans (#2311 / #3200) — A critical latent data-loss path where gc dolt health --json misclassified active, registered rig databases as orphans… **Patched.**"* and *"Container-Dependency Gap (#3451) — Dependency orchestration relies heavily on local host installations (Homebrew) for dolt, jq, tmux, etc. … **Persistent.** Container-native deployments require manual make install"* and *"Dispatcher Wedge (#2131 / #2168) … **Mitigated in v1.4.0.**"*
Against `research-maturity-open-bugs.md:Barrier race #2311`: *"**#2311** \"`waits_for = \"children-of(X)\"` does not gate `bd ready` when X uses `on_complete` bond fanout\" — **OPEN**, `kind/bug` `priority/p2`… no fix PR, no maintainer ruling, no milestone"*; `:Container-gate gap #3451`: *"**#3451** \"formulas v2: `needs` on a parent step does not gate on its children (container-dependency parity with v1)\" — **OPEN**"*; `:Wedge bugs`: *"Both are genuinely resolved in the v1.2 window (v1.2.0, 2026-05-29)."*
Verified against GitHub directly: `api.github.com/repos/gastownhall/gascity/issues/2311` → title `"bug: waits_for = \"children-of(X)\" does not gate bd ready when X uses on_complete bond fanout"`, state `open`, created `2026-05-17`. `.../issues/3451` → title `"formulas v2: needs on a parent step does not gate on its children (container-dependency parity with v1)"`, state `open`, labels `kind/bug, priority/p2` — parent/child step gating, **not** Docker.
**suggestion:** Delete Table 3 or replace every row with the verified titles/states from `research-maturity-open-bugs.md`. Note explicitly that "container-dependency" in #3451 means a *container step* (a parent with children), not a deployment container — this is the misreading the scope's own shorthand ("container-gate gap #3451") invited. Flag "Patched"/"Mitigated in v1.4.0" as unsupported: #2311 and #3451 are both open with no fix.

---

**id:** ACCURACY-A-002
**severity:** critical
**dimension:** correctness
**location:** `gemini-deep-research-output.md:Follow-Up Q1` vs `research-gate-mechanics-handson.md:The notification gap` / `research-notification-watcher-layer.md:What already exists upstream`
**description:** *(This is the flagged tension; adjudicated against the empirical file and independently re-verified.)* Gemini asserts the bundled release orders are "functionally equivalent" to the human-gate notifiers and "not restricted to main/edge branches." Both halves are false. The named substitutes do not notify on human gates — `gate-sweep` checks only timer and gh gates — and the actual notifier orders 404 at every release tag.
**evidence:** gemini: *"Gas City does ship **functionally equivalent** mechanical housekeeping orders in its tagged releases. Recent releases (including v1.4.0) bundle orders named gate-sweep, nudge-mail-sweep, nudge-on-route, and cascade-nudge-on-blocker-close. These were previously part of a separate maintenance pack but have since been folded directly into the default core pack that ships with stable releases, meaning they are **not restricted to main/edge branches**."*
`research-gate-mechanics-handson.md`: *"`gate-sweep`, the one gate watcher that does ship in 1.4.1, **deliberately excludes human gates**. Its script body is exactly two lines: `gc bd gate check --type=timer --escalate` and `gc bd gate check --type=gh --escalate || true`."*
`research-notification-watcher-layer.md`: *"Raw fetches of those two files at `v1.4.1`, `v1.4.0`, and `v1.3.5` all return **404**, while `gate-sweep.toml` at `v1.4.1` returns 200."*
Independently confirmed: `raw.githubusercontent.com/gastownhall/gascity/v1.4.1/…/orders/notify-on-human-gate-creation.toml` → **HTTP 404**. `…/v1.4.1/…/assets/scripts/gate-sweep.sh` → body is exactly `gc bd gate check --type=timer --escalate` / `gc bd gate check --type=gh --escalate || true`, with a header comment confirming bead-gate checks are commented out and no human-gate invocation at any point.
**suggestion:** Strike the "functionally equivalent" claim. Replace with the empirical finding: on v1.4.1 a created `type=human` gate notifies nobody by any path, and the two orders that would fix it exist only on `main`/`edge`. Because gemini is the lowest-authority source and the empirical file is the highest, this should be resolved by authority hierarchy, not left as a live tension in the corpus.

---

**id:** ACCURACY-A-003
**severity:** major
**dimension:** traceability
**location:** `research-gate-mechanics-handson.md:City setup: what gc actually requires` vs `research-beads-coupling-dec028.md:§2`
**description:** The highest-authority file asserts a negative — that `GC_BEADS=file` no longer exists — on evidence drawn from a different subsystem. `bd init --help` describes the **beads** CLI's own storage backend; `GC_BEADS` selects which **Gas City** `Store` implementation `gc` opens (`BdStore` / `NativeDoltStore` / `FileStore`). The one says nothing about the other. This is the classic confident-false-negative pattern, and it lands on a DEC-028-decisive claim.
**evidence:** `research-gate-mechanics-handson.md`: *"**There is no `GC_BEADS=file` escape hatch in 1.4.1** — `bd init --help` states \"Dolt is the default (and only supported) storage backend. The legacy SQLite backend has been removed.\""*
`research-beads-coupling-dec028.md`: *"`GC_BEADS=file` survives intact in current main and in the v1.4.1-era docs — it is the documented lightest-start path, the CI/testscript default, and the remediation string the binary itself prints when `bd` is missing"*, with five citations including *"`requireBdBinaryForCity` returns `\"bd not found in PATH (install beads or set GC_BEADS=file)\"`"* and the `factory.go` switch arm `case provider == "file":`.
Independently confirmed against `raw.githubusercontent.com/gastownhall/gascity/main/docs/getting-started/faq.md`: *"For the lightest possible start, `GC_BEADS=file` skips the dolt + bd pair."*
**suggestion:** Correct the hands-on file to say what it actually tested: the researcher used bd's embedded Dolt and did not exercise `GC_BEADS=file`; bd's removal of SQLite is a beads-side change that does not touch gc's provider selection. Preserve the true adjacent finding (`gc start` needs tmux + external dolt + flock; the graph layer does not). This matters because `research-beads-coupling-dec028.md`'s headline — *"Gas City does not force Dolt"* — and its DEC-028 "Forced: nothing" conclusion both rest on the file provider existing.

---

**id:** ACCURACY-A-004
**severity:** major
**dimension:** correctness
**location:** `research-maturity-open-bugs.md:Project shape and release cadence` vs `research-notification-watcher-layer.md:What already exists upstream`
**description:** Two files report the same repo's open-issue count on the same day, both tagged `[EMPIRICAL, GitHub API]`, and disagree by 76%. `research-maturity-open-bugs.md` builds a maturity argument on its figure.
**evidence:** `research-maturity-open-bugs.md`: *"Issue hygiene is the weaker signal: **575 open issues** against **380 issues closed from the May-onward cohort** [EMPIRICAL] (GitHub search API, 2026-08-21)"*, carried into the synthesis as *"a 575-issue open backlog."*
`research-notification-watcher-layer.md`: *"Repo health context: gascity is public, was pushed to minutes before this research ran, and carries **1,011 open issues** [EMPIRICAL, GitHub API]."*
Root cause identified: `api.github.com/repos/gastownhall/gascity` returns `open_issues_count: 1053` (checked 2026-08-24) — GitHub's repo endpoint counts open **issues + pull requests**, while the search API with `is:issue is:open` counts issues only. The two files measured different quantities and both labeled the result "open issues."
**suggestion:** Keep 575 as the issue-only figure and annotate the 1,011 as `open_issues_count` (issues + open PRs). Both files should name the query used. Do not leave two unqualified counts in a corpus whose purpose is a maturity go/no-go.

---

**id:** ACCURACY-A-005
**severity:** major
**dimension:** correctness
**location:** `research-hitl-alternative-patterns.md:§4` and `:§7(d)` vs `research-notification-watcher-layer.md:The release gap` / `research-gate-mechanics-handson.md:The notification gap`
**description:** The HITL-patterns file presents `renudge-stale-human-gates` as a shipped, operating escalation loop and recommends it as "the existing precedent" for nagging on the results gate. Two other files establish it ships in no release, and the empirical file establishes that even where it does run it cannot see formula-created gates.
**evidence:** `research-hitl-alternative-patterns.md`: *"There is also a notification watchdog for exactly this: a pack order `renudge-stale-human-gates.sh` … **Human gates therefore have a real, if young, escalation loop behind them.**"* and *"If Momentum wants nagging, the `renudge-stale-human-gates` order is the existing precedent."*
`research-notification-watcher-layer.md`: *"`v1.4.1` and `v1.4.0` contain `gate-sweep.toml` but **not** `notify-on-human-gate-creation.toml` or `renudge-stale-human-gates.toml`… The only build carrying the reflex is the `edge` rolling-main pre-release … described in its own release notes as \"**not for production**.\""*
`research-gate-mechanics-handson.md`: *"`renudge-stale-human-gates.sh` applies the identical filter (\"keeps only `await_type == \\\"human\\\"` gates\"). **Because formula-cooked gates carry `await_type: null`, both bundled reflexes skip them.**"*
**suggestion:** Downgrade §4 from "a real, if young, escalation loop" to "written upstream, in no tagged release; vendoring or running `edge` is required." In §7(d), replace "the existing precedent" with the vendoring option `research-notification-watcher-layer.md:Gap list` item 3 already prescribes, and add the `await_type: null` caveat — the recommendation to route through `bd gate create` (which does persist `await_type`) is what makes the notifier usable at all.

---

**id:** ACCURACY-A-006
**severity:** major
**dimension:** logical_soundness
**location:** `research-hitl-alternative-patterns.md:§2 Practical implication for Momentum` vs `research-cycle-orchestration-fit.md:§1`
**description:** The file's central recommendation — repeated in its summary table for gates (a), (c), and (d) — instructs the author to use "an ordinary `exec` step" in a v2 formula. There is no `exec` step key in formula v2, and the failure mode is silent: an unknown step key compiles clean and does nothing.
**evidence:** `research-hitl-alternative-patterns.md`: *"In a Gas City v2 formula that means **an ordinary `exec` step** that shells `bd gate create --type=human --blocks <next-step-bead>` and exits, rather than a `[steps.gate]` block whose `type = \"human\"` is decoration."*
`research-cycle-orchestration-fit.md`: *"The v2 step key table is exhaustive: `id`, `title`, … `on_complete`, `tally`, `timeout`. **There is no `exec`, `command`, `run`, or `script` key**"* and *"**Unknown step keys are silently ignored. A typo like `dependson` produces no diagnostic — the dependency simply vanishes.**… So authoring `exec = \"claude -p /momentum:triage\"` on a step compiles cleanly and does nothing — a silent no-op, not an error."*
**suggestion:** Rewrite as: a **work bead** whose description instructs the agent to run `bd gate create --type=human --blocks <next-step-bead>`, or an order-level `[order] exec` (the one real exec surface, orchestrator-hosted, 300s default). `research-gate-mechanics-handson.md:What this means…` already states the correct shape (*"A formula step can shell out to `bd gate create`"*) without naming a nonexistent key. Also revisit §4's derived conclusion — *"a `claude -p` phase step is structurally `headless`"* — which reasons from the same nonexistent construct.

---

**id:** ACCURACY-A-007
**severity:** major
**dimension:** correctness
**location:** `gemini-deep-research-output.md:Executive Summary` and `:§6 Current Maturity`
**description:** Gemini states the current stable release as of the research date is v1.4.0 and repeatedly attributes v1.4.0 to "August 2026." v1.4.1 shipped 2026-08-15 and v1.4.0 shipped 2026-07-24. Every v1.4.0-scoped capability claim in the document inherits the error.
**evidence:** gemini: *"As of August 21, 2026, the Gas City ecosystem operates on the stable **v1.4.0** release"* and *"The **August 2026 v1.4.0 release** demonstrates a highly mature production posture."*
`research-gate-mechanics-handson.md` (empirical install): *"`gc` (Gas City) | **1.4.1** (`gc version` → `1.4.1`)"*.
`research-maturity-open-bugs.md`: *"| v1.4.0 | **2026-07-24** | minor (breaking) | / | v1.4.1 | **2026-08-15** | patch (latest) |"*.
`research-notification-watcher-layer.md`: *"Latest release is **v1.4.1, 2026-08-15**."*
**suggestion:** Correct to v1.4.1 (2026-08-15) throughout, and re-date v1.4.0 to 2026-07-24. Where gemini credits a fix to "the v1.4.0 release," verify against `research-maturity-open-bugs.md`'s release table before retaining — see ACCURACY-A-001 for one case where the attribution is off by two minors.

---

**id:** ACCURACY-A-008
**severity:** major
**dimension:** correctness
**location:** `gemini-deep-research-output.md:§4 The Gas City Dashboard Architecture` + `:§8 Recommendation 2` vs `research-notification-watcher-layer.md:The dashboard's treatment of blocked/gated work`
**description:** Gemini describes the dashboard as a React 19 SPA served by a Node 24 backend on port 8082, with a Beads view where operators "filter for beads requiring human approval," then recommends standardizing HITL operations on it. The stack, the port, and the approval-filtering capability are all wrong.
**evidence:** gemini: *"a highly responsive Single Page Application (SPA) built on **React 19**, statically served by a **Node 24** (Active LTS) backend. It runs locally, defaulting to **port 8082** in production"*; Table 2: *"Beads … Operators can **filter for beads requiring human approval**"*; §8: *"**Standardize on the Gas City Dashboard for HITL operations.**"*
`research-notification-watcher-layer.md`: *"a single-page dashboard **compiled into the `gc` binary**, served at `http://127.0.0.1:**8372**/`… That enumeration has **no gate view, no blocked-work queue, and no notification/alerting surface**."*
Independently confirmed against `docs.gascity.com/getting-started/dashboard`: binds port **8372**; *"It is a single-page app compiled into the `gc` binary and served by the supervisor"*; displayed surfaces are *"agents and their sessions, beads, mail, formula runs, and a health view"* — no gate view, no blocked-work queue.
**suggestion:** Delete the React/Node/8082 architecture paragraph and Table 2's approval-filtering row. Withdraw Recommendation 2, or restate it with `research-notification-watcher-layer.md`'s actual finding — that a loopback single-operator dashboard with no gate view is *structurally wrong* for the out-of-session case that motivates Gas City adoption at all.

---

**id:** ACCURACY-A-009
**severity:** minor
**dimension:** traceability
**location:** `gemini-deep-research-output.md:Follow-Up Q1`, `:§2`, `:§7 Dolt Bloat Recovery (#1094)`
**description:** Three issue references are offered as provenance for claims they do not support. beads #1467 is presented as the tracker for the `await_type` defect — it is a closed issue from 2026-02-03 about *refusing to close* machine-checkable gates, predating and unrelated to the formula-cook defect this research discovered. #620 is cited with no link and appears in no other file. #1094's headline figure conflicts with the corpus's documented incident.
**evidence:** gemini: *"Regarding the await_type behavior, this is **tracked in the gastownhall/beads repository under Issue #1467**… The issue addresses how gate beads are created with an await_type."* Verified via `api.github.com/repos/gastownhall/beads/issues/1467` → title *"Prevent closing machine-checkable gate issues unless the condition is satisfied (with --force override)"*, state **closed**, created **2026-02-03** — about `--force` on close, not about creation persisting `await_type`.
gemini: *"**Issue #620** specifically addresses the implementation of the 'human gate…'"* — uncited; the corpus's actual trackers are #4399 (`research-maturity-open-bugs.md`, `research-hitl-alternative-patterns.md`) and #1709 (O3 HITL).
gemini: *"**#1094**, where a real-world installation rapidly filled a **244GB** disk"* vs `research-beads-coupling-dec028.md:§4`: *"a documented incident (\"qlandia\") reached **34 GB** and filled the disk"* and *"120 GB commonly shrinks to 5–20 GB."*
**suggestion:** Drop #1467 and #620, or re-cite them with their verified titles and states. Note in the corpus that the formula-cook `await_type: null` defect has **no** upstream tracker found — that absence is itself a finding for Momentum (nobody upstream is fixing it). Replace the 244GB figure with `research-beads-coupling-dec028.md`'s sourced runbook numbers.

---

**id:** ACCURACY-A-010
**severity:** minor
**dimension:** logical_soundness
**location:** `gemini-deep-research-output.md:§7 The Dolt Backend (Default)`
**description:** The stated Dolt floor is justified by a reason that cannot support it: a 2.1.0 minimum cannot be explained by builds "prior to 1.86.2" lacking a fix, since every build below 1.86.2 is already excluded by the 2.1.0 floor. The corpus shows these are two separate facts that gemini has fused into one causal claim.
**evidence:** gemini: *"This backend requires **Dolt version 2.1.0 or newer**; Gas City actively rejects older builds **because releases prior to 1.86.2 lack critical upstream deadlock fixes** that can hang synchronization routines under heavy write loads."*
`research-beads-coupling-dec028.md:§6` quotes the source correctly as two distinct statements: *"Use a final Dolt 2.1.0 or newer. Gas City's managed Dolt checks reject older and pre-release builds… releases **before 1.86.2 can also miss** the upstream GC/writer deadlock fix in dolthub/dolt commit `ccf7bde206`."* Note "**can also**" — an additional hazard for a separate build range, not the rationale for the 2.1.0 floor. `research-maturity-open-bugs.md` independently sources the floor to a release event: *"**v1.2.1** — floor raised to Dolt ≥ 2.1.0 for managed bd/Dolt operation."*
**suggestion:** Split the sentence: state the 2.1.0 floor and attribute it to v1.2.1's managed-Dolt check, then state the 1.86.2 deadlock caveat as a separate note about pre-release/older builds.

---

**id:** ACCURACY-A-011
**severity:** minor
**dimension:** correctness
**location:** `gemini-deep-research-output.md:§2 The Status of the Gate Vocabulary`
**description:** Two errors in one paragraph. Gate parsing is attributed to `internal/convergence/formula.go`, which the corpus shows holds convergence validation, not gate parsing. And the "zero bundled formulas" claim is hedged into its opposite — gemini's qualifier implies some bundled formulas *do* use `[steps.gate]` with convergence logic, when the count is zero unconditionally.
**evidence:** gemini: *"**zero bundled formulas** shipping in the primary registry … that utilize a naked type = \"human\" in a [steps.gate] block **without relying on auxiliary convergence logic**"* and *"the framework's **internal/convergence/formula.go** engine parses the gate constructs."*
`research-hitl-alternative-patterns.md`: *"**Zero bundled formulas use `gate`.**"* — verified there empirically: *"`gh api -X GET search/code -f q='repo:gastownhall/gascity-packs \"steps.gate\"'` → `total_count: 0`."* `research-cycle-orchestration-fit.md` corroborates: *"zero `[steps.gate]` and zero `waits_for` occurrences across all 20+ packs."*
On the file attribution, `research-human-verdict-patterns.md:§4`: *"A formula must set `convergence = true` to be valid for converge (**`ValidateForConvergence`, `internal/convergence/formula.go`**)"*, while gate synthesis lives elsewhere — `research-gate-mechanics-handson.md`: *"`gateTitle = fmt.Sprintf(\"Gate: %s %s\", step.Gate.Type, step.Gate.ID)` in **`internal/formula/compile.go`**"*, with the type vocabulary in `internal/formula/types.go`.
**suggestion:** Correct the file path to `internal/formula/compile.go` (synthesis) and `internal/formula/types.go` (vocabulary). Remove the "without relying on auxiliary convergence logic" qualifier — it manufactures a category of formulas that does not exist.

---

**id:** ACCURACY-A-012
**severity:** minor
**dimension:** traceability
**location:** `research-gate-mechanics-handson.md:Q2 — Bonus finding`
**description:** The close-side enforcement finding — the sole evidence for the "best fit of the four" verdict on Momentum's mid-story tooling gates — is demonstrated with two bead IDs that belong to a different probe. `gt-bvw` is introduced nowhere in the document, and its blocker `gt-2zt` is identified 70 lines later as the **timer** gate `Gate: timer auto-5s`. The Q2 human-gate probe used `gt-b3e` blocked by `gt-crp`.
**evidence:** The transcript under Q2: *"`$ bd close gt-bvw --reason \"attempting bypass\"` / `cannot close gt-bvw: blocked by open issues [gt-2zt] (use --force to override)`"*, immediately after the section's own probe established *"`bd blocked` → `[● P2] gt-b3e: Step B: gated on human approval` / `Blocked by 1 open dependencies: [gt-crp]`."*
`gt-2zt` is first defined much later, in the timer probe: *"`$ bd gate show gt-2zt` / `○ gt-2zt - Gate: timer auto-5s`."*
The finding is then cited as human-gate evidence in the mapping table: *"(c) mid-story tooling gates | **Best fit of the four.** … | Q2 bonus **[EMPIRICAL]**."*
**suggestion:** Either re-run the close-bypass attempt against `gt-b3e`/`gt-crp` and replace the transcript, or state plainly that the demonstration was performed on the timer-gate city and note that `bd close`'s blocked-issue refusal is gate-type-agnostic. The underlying claim is almost certainly right; the cited evidence just does not show it for a human gate.

---

**id:** ACCURACY-A-013
**severity:** low
**dimension:** traceability
**location:** `research-gate-mechanics-handson.md:The defect: type and timeout are not persisted`
**description:** A key-absence claim is made that no shown command demonstrates, and it sits in mild tension with the output immediately above it. `jq '{…,await_type,…}'` emits `await_type: null` whether the key is absent or present-and-null, so the quoted transcript cannot distinguish the two — yet the prose asserts the stronger key-absence reading.
**evidence:** Line 240 output: *"`{\"id\":\"gt-crp\",\"issue_type\":\"gate\",\"title\":\"Gate: human test-gate\",\"await_type\":null,…}`"*, followed six lines later by *"`bd show --json` on the formula gate has **no `await_type` key at all in its `keys` list**."* No `keys`-listing command appears anywhere in the document.
**suggestion:** Either include the `jq 'keys'` transcript, or soften to "persists a null `await_type`" — which is all the shown evidence supports and all the downstream argument needs, since the notifier filter `[ "$AWAIT_TYPE" = "human" ] || continue` fails identically on absent and null.

---

**id:** ACCURACY-A-014
**severity:** low
**dimension:** correctness
**location:** `research-hitl-alternative-patterns.md:§2 gate type table` vs `research-maturity-open-bugs.md:#4399` and `research-human-verdict-patterns.md:§5`
**description:** Three files give three different inventories of `bd` gate types, and the `bead` row contradicts the corpus's own documented create/check asymmetry. `research-maturity-open-bugs.md` treats that asymmetry as a *finding*; the other two flatten it.
**evidence:** `research-hitl-alternative-patterns.md` table: *"`bead` | a bead in another rig to close | **resolve manually**"* — implying `bead` gates are creatable and human-resolved.
`research-maturity-open-bugs.md`: *"`mail` … exists in neither `bd gate create --type` (`human`/`timer`/`gh:run`/`gh:pr`) nor `bd gate check --type` (`gh`/`gh:run`/`gh:pr`/`timer`/`bead`)… `human` is in `create` but not `check` (correct by design — manual resolution). **`bead` is the inverse.**"* — i.e. `bead` is checkable (auto-resolvable), not creatable, the opposite of "resolve manually."
`research-human-verdict-patterns.md` quotes `bd` help with only four types (*"human … timer … gh:run … gh:pr"*, no `bead`), while `research-notification-watcher-layer.md` gives a flat five: *"Gate types are `human`, `timer`, `gh:run`, `gh:pr`, `bead`."*
**suggestion:** Standardize on `research-maturity-open-bugs.md`'s two-column framing (creatable via `bd gate create` vs evaluable via `bd gate check`) across all three files, and correct the `bead` row's "resolve manually." Worth noting alongside: the v1.4.1 `gate-sweep.sh` header I retrieved states bead-gate checking is disabled upstream — *"Bead-type gates are skipped: in beads v1.0.2, checkBeadGate is hard-coded to fail because cross-rig routing was removed upstream"* — so `bead` is currently neither creatable nor evaluable in practice.
