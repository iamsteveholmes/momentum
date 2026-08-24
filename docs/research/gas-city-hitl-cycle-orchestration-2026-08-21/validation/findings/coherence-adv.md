## Findings

---

**COHERENCE-A-001**
**Severity:** Critical
**Dimension:** cross_document_consistency
**Location:** `research-gate-mechanics-handson.md`:"City setup: what gc actually requires" ↔ `research-beads-coupling-dec028.md`:§2 ↔ `gemini-deep-research-output.md`:§7

**Description:** The corpus flatly disagrees on whether `GC_BEADS=file` exists in the current release. One file declares it removed; the other two build load-bearing conclusions on its existence. This is the hinge of the DEC-028 recommendation — beads-coupling's entire "Forced: nothing" verdict rests on a Dolt-free city being expressible.

**Evidence:**
- gate-mechanics: *"There is no `GC_BEADS=file` escape hatch in 1.4.1 — `bd init --help` states 'Dolt is the default (and only supported) storage backend. The legacy SQLite backend has been removed.'"*
- beads-coupling §2 is titled *"`GC_BEADS=file` Is Alive, Documented, and Load-Bearing"* and cites five independent sites in current `main`, including the binary's own error string: *"`requireBdBinaryForCity` returns `\"bd not found in PATH (install beads or set GC_BEADS=file)\"`"* and the config enum *"`provider` — `\"bd\"` (default, Dolt-backed), `\"file\"`, or `\"exec:<script>\"`"*.
- gemini §7: *"By setting the environment variable GC_BEADS=file or defining [beads] provider = \"file\" in the city.toml configuration, operators can bypass the default database entirely."*

**Suggestion:** gate-mechanics' refutation is a category error — it cites `bd init --help` (beads' own storage backend) to deny a `gc` provider selector; the two are different switches. Correct that sentence to "bd itself no longer offers a non-Dolt backend; `GC_BEADS=file` selects gc's FileStore and is unaffected," and re-check whether gate-mechanics' derived claim ("only `gc start` adds tmux + dolt + flock") survives.

---

**COHERENCE-A-002**
**Severity:** Critical
**Dimension:** cross_document_consistency, logical_soundness
**Location:** `research-cycle-orchestration-fit.md`:Headline/§2 ↔ `research-hitl-alternative-patterns.md`:§4 ↔ `research-beads-coupling-dec028.md`:§7 ↔ `gemini-deep-research-output.md`:§5

**Description:** One file proves the `claude -p /momentum:*` phase-step shape does not exist; three others treat it as the operating model and derive recommendations from it. hitl-alternative's central design inversion ("don't park a session, create a gate and exit") is justified *entirely* by a runtime shape that cycle-orchestration-fit shows Gas City does not offer.

**Evidence:**
- cycle-orchestration-fit: *"**The `claude -p` exec-step shape the sub-question assumes does not exist in Gas City, and the maintainers explicitly steer against building it.** A v2 formula step has no `exec` field"* and *"A grep of the entire gascity-packs corpus finds **zero** invocations of `claude -p`, `claude --print`, or `codex exec` [[EMPIRICAL]]"*.
- hitl-alternative §4: *"Momentum's proposed Gas City layer runs each phase as `claude -p /momentum:<skill>` — a process that exits"* … *"So a `claude -p` phase step is structurally `headless`"* … §7(c): *"wasteful and fragile for a `claude -p` runner"*.
- beads-coupling §7: *"Under the exec-order pattern DEC-032 D3 adopted (`claude -p /momentum:<skill>` as a shell subprocess), the phase step's payload is a story slug or a sprint slug"*.
- gemini contradicts *itself* on this: §5 *"heavily supporting Claude Code (claude -p)"* vs. Follow-Up Q2 *"Gas City uses long-lived, headless interactive sessions managed via tmux rather than per-step claude -p print-mode invocations… Gas City does not use it as the primary runtime topology."*

**Suggestion:** Adopt cycle-orchestration-fit's finding as the corpus premise and rewrite hitl-alternative §4's "why Momentum probably can't use this pattern" and beads-coupling §7's "Forced: nothing" argument against the session-based runtime. hitl-alternative's conclusion may still hold, but not for the stated reason.

---

**COHERENCE-A-003**
**Severity:** Major
**Dimension:** cross_document_consistency, consistency
**Location:** `research-maturity-open-bugs.md`:"The gate surface today (#4399)" ↔ `research-gate-mechanics-handson.md`:Headline/"The notification gap"

**Description:** The corpus gives opposite answers to "does the inert `type` vocabulary hurt Momentum?" — one pair of files says it is free for `human` gates, the other pair measures a concrete cost. The empirical file wins on evidence, and it inverts a "good news for Momentum" verdict into a defect.

**Evidence:**
- maturity: *"**Why this is good news for Momentum specifically.** … The inert vocabulary costs Momentum nothing for `human`; it costs `timer`, `gh:pr`, and `mail`, which Momentum does not need."* human-verdict §5 says the same: *"For `type = \"human\"`, it costs nothing: **closing the gate bead is the human's job by definition.**"*
- gate-mechanics measured otherwise: *"A `[steps.gate] type=\"human\"` blocks correctly and tells nobody"*; *"`{\"id\":\"gt-crp\",…,\"await_type\":null}`"* vs. the ad-hoc gate's `"await_type":"human"`; *"**Because formula-cooked gates carry `await_type: null`, both bundled reflexes skip them.**"*
- hitl-alternative §8 corroborates gate-mechanics: *"**The `[steps.gate]` trap.** … gets a gate bead that blocks correctly but has no typed identity, no watcher, and no `bd gate list` visibility as a *human* gate."*

**Suggestion:** Replace "costs nothing" in maturity and human-verdict with the measured cost: the declared type survives only inside the title string, so formula-synthesized human gates are invisible to `bd gate check`, `gate-sweep`, and both notify orders. Propagate to maturity's synthesis table, which currently prescribes `[steps.gate]` for all four Momentum gates.

---

**COHERENCE-A-004**
**Severity:** Major
**Dimension:** cross_document_consistency, temporal_coherence
**Location:** `research-notification-watcher-layer.md`:"What already exists upstream" ↔ `research-production-evidence.md`:Finding 2 ↔ `research-hitl-alternative-patterns.md`:§4/§7(a) ↔ `gemini-deep-research-output.md`:Follow-Up Q1

**Description:** Whether the two human-gate notification orders are *available today* is answered three incompatible ways. This determines whether Momentum inherits a working reflex or writes ~1–2 days of watcher glue, and one recommendation is already built on the order being live.

**Evidence:**
- notification-watcher (empirical tag enumeration): *"`v1.4.1` and `v1.4.0` contain `gate-sweep.toml` but **not** `notify-on-human-gate-creation.toml` or `renudge-stale-human-gates.toml`. Raw fetches of those two files at `v1.4.1`, `v1.4.0`, and `v1.3.5` all return **404**"*; the only carrier is *"the `edge` rolling-main pre-release … 'not for production.'"* gate-mechanics agrees: *"Neither order is in the 1.4.1 release."*
- production-evidence Finding 2 headline: *"The real human-gate path is ad-hoc gate beads plus two core orders, **shipped 2026-07-23**"* and bottom line *"This is the only production-grade HITL notification machinery Gas City **ships**"*.
- hitl-alternative §7(a) treats it as running: *"Do **not** use per-observation gates; the escalation loop (`renudge-stale-human-gates`, 1h interval) would spam."*
- gemini Q1: *"These were previously part of a separate maintenance pack but have since been folded directly into the default core pack that ships with stable releases, meaning they are not restricted to main/edge branches."*

**Suggestion:** The 404-at-three-tags evidence is the strongest; make it the corpus position, and change production-evidence's "shipped"/"ships" to "landed on `main` 2026-07-23, not in any tagged release as of v1.4.1." Rewrite hitl-alternative §7(a)'s spam rationale, which currently assumes an order Momentum would have to vendor first.

---

**COHERENCE-A-005**
**Severity:** Major
**Dimension:** cross_document_consistency, logical_soundness
**Location:** `gemini-deep-research-output.md`:§8 Recommendation 1 ↔ `research-human-verdict-patterns.md`:§3/§8 ↔ `research-hitl-alternative-patterns.md`:§7(b)

**Description:** The corpus prescribes three mutually exclusive primitives for the *same* Momentum plan gate. Gemini's top recommendation is precisely the construction human-verdict spends a section proving unusable; hitl-alternative lands in between. A synthesizer has no basis to choose.

**Evidence:**
- gemini: *"Do not rely on naked type = \"human\" primitives. … architects should design formulas using interaction_mode = interactive and \"Check Loop\" DAG topologies. By parsing human feedback via bead metadata modification, the system reliably achieves the exact same HITL outcome"*.
- human-verdict §3: *"the check loop **does not wait** … If the human has not yet recorded a verdict, the script exits 1, and the orchestrator **spawns another agent iteration of the work** … With `max_attempts = 6` and a human on a lunch break, the loop burns its budget and closes the step failed. … **A check loop is the wrong primitive for a human gate.** The right one is `[steps.gate]`."* §8: *"Use **`[steps.gate]` / `bd gate create --type=human`**, not a check loop."*
- hitl-alternative §7(b): *"**Recommended: v2 check loop + verdict-in-metadata + artifact file. Gate bead only as the parking brake.**"*

**Suggestion:** Reconcile to one prescription. human-verdict's mechanism argument (no waiting state; exhaustion closes the step *failed*, indistinguishable from broken work) is the only one grounded in the dispatch contract; if the check loop is retained anywhere it must be for the *agent-side* review that precedes the human, per human-verdict's own two-step pattern.

---

**COHERENCE-A-006**
**Severity:** Major
**Dimension:** cross_document_consistency, correctness
**Location:** `gemini-deep-research-output.md`:§6 Table 3 / "Orchestration v3" ↔ `research-maturity-open-bugs.md`:"#3451" / "#2311" / "#1709" / "Wedge bugs"

**Description:** Every tracked issue number the two files share is described as a different bug, with a different status. Sub-question 5 names these issues explicitly, so a synthesizer merging both files would produce a corrupt maturity picture — including on #3451, which the rest of the corpus identifies as the load-bearing blocker for Momentum's results gate.

**Evidence:**
- **#3451** — gemini: *"Container-Dependency Gap (#3451) — Dependency orchestration relies heavily on local host installations (Homebrew) for dolt, jq, tmux, etc. … Container-native deployments require manual make install procedures"* (reads "container" as Docker). maturity: *"**#3451** *\"formulas v2: `needs` on a parent step does not gate on its children (container-dependency parity with v1)\"*"* — "container" = a parent step containing children.
- **#2311** — gemini: *"Barrier Race & False Orphans (#2311 / #3200) — A critical latent data-loss path where gc dolt health --json misclassified active, registered rig databases as orphans. … **Patched.**"* maturity: *"#2311 *\"`waits_for = \"children-of(X)\"` does not gate `bd ready`…\"* — **OPEN** … last activity 2026-05-29, no fix PR, no maintainer ruling, no milestone"*.
- **#1709** — gemini: *"#1709 … addresses systemic namespace and pack composition flaws … proposes a strict, explicit [[exports]] surface"* and *"the project roadmap heavily prioritizes 'Orchestration v3'"*. maturity: *"'the orchestrator has no first-class human-in-the-loop … Human-in-the-loop is a runtime disposition class'"*, **"no milestone" … "last updated 2026-06-01"**, and *"**do not plan against O3 HITL.**"*
- **#2131/#2168** — gemini: *"Mitigated in v1.4.0."* maturity: *"**CLOSED / COMPLETED 2026-05-23**"* / *"**CLOSED / COMPLETED 2026-05-26**"*, *"genuinely resolved in the v1.2 window (v1.2.0, 2026-05-29)."*
- Same pattern on code attribution: gemini *"the framework's internal/convergence/formula.go engine parses the gate constructs"* vs. human-verdict, which locates gate parsing in `internal/formula/types.go`/`compile.go` and `internal/convergence/formula.go` as `ValidateForConvergence` (v1 converge only).

**Suggestion:** Treat the maturity file's issue descriptions as authoritative (it quotes titles, labels, and timeline events per issue) and strike or flag gemini's Table 3 and O3 section wholesale rather than merging them. Gemini's derived recommendation ("Prepare for Orchestration v3 Migration" re: `[[exports]]` namespace breakage) falls with it.

---

**COHERENCE-A-007**
**Severity:** Major
**Dimension:** cross_document_consistency
**Location:** `research-gate-mechanics-handson.md`:"Environment and versions"/Sources ↔ `research-beads-coupling-dec028.md`:§6 ↔ `research-production-evidence.md`:Finding 5

**Description:** Two files quote the *same file* (`deps.env`) with different values and name different "newest published" beads releases, roughly one minor apart. beads-coupling's CAS conclusion — one of four DEC-028 gate re-scores — depends on its version being right, and a third file's evidence points the other way.

**Evidence:**
- gate-mechanics: *"gc 1.4.1's CHANGELOG entry for 2026-08-15 states '**beads pinned to v1.2.2 everywhere** (go.mod library, `deps.env` `BD_VERSION`, CI matrix…)'"*, environment table row *"`bd` (beads), gc-pinned | **1.2.2** (`6c124203e`)"*, and sources: *"gastownhall/beads — releases — v1.2.2 (2026-08-15), v1.0.4 (2026-05-09)"*.
- beads-coupling §6 quotes `deps.env` on current `main` as *"`BD_VERSION=v1.1.0` / `BD_PREV_VERSION=v1.0.4` / `BD_CURRENT_VERSION=v1.1.1-0.20260805093327-bf97b73749ac`"*, and concludes from *"the newest published release — v1.1.2 — … predates both"* that *"**Multi-agent write safety via CAS … is still not reachable from a published bd release as of 2026-08-21.**"*
- production-evidence independently cites *"Beads 1.2.1 Incident Report: Release the Bees! — Chris Sells, 2026-08-20"* — a beads v1.2.1 release existing on 2026-08-20 is incompatible with v1.1.2 being newest on 2026-08-21.

**Suggestion:** Re-read `deps.env` at a named commit and pin the beads release timeline once for the corpus. If v1.2.x is current, beads-coupling's CAS-unavailable row and its "Weakens" direction on the DEC-028 multi-agent-write-safety gate must be re-scored.

---

**COHERENCE-A-008**
**Severity:** Moderate
**Dimension:** cross_document_consistency
**Location:** `research-notification-watcher-layer.md`:"The dashboard's treatment of blocked/gated work" ↔ `gemini-deep-research-output.md`:§4/§8 Recommendation 2

**Description:** The two files describe different software: different implementation stack, different port, and opposite answers on whether the dashboard supports HITL. Gemini's second recommendation ("Standardize on the Gas City Dashboard for HITL operations") is grounded on affordances the other file says do not exist.

**Evidence:**
- notification-watcher: *"The supervisor ships a single-page dashboard compiled into the `gc` binary, served at `http://127.0.0.1:8372/`"* … *"That enumeration has no gate view, no blocked-work queue, and no notification/alerting surface"* … *"a loopback single-operator dashboard is exactly wrong for the case that motivates Gas City at all."*
- gemini: *"a highly responsive Single Page Application (SPA) built on React 19, statically served by a Node 24 (Active LTS) backend. It runs locally, defaulting to port 8082 in production"* and *"Operators can filter for beads requiring human approval, utilizing supervisor-backed claim, close, or nudge functions directly from the UI to unblock pipelines."*

**Suggestion:** notification-watcher flags its own claim as documentation-derived (*"[UNVERIFIED as to source; OFFICIAL as to docs]"*) — resolve with one hands-on `gc dashboard` pass now that gc 1.4.1 is installed (see COHERENCE-A-012), and record the actual port and view list once.

---

**COHERENCE-A-009**
**Severity:** Moderate
**Dimension:** cross_document_consistency
**Location:** `research-maturity-open-bugs.md`:"Project shape and release cadence" ↔ `research-notification-watcher-layer.md`:"What already exists upstream" ↔ `research-production-evidence.md`:Finding 7

**Description:** The open-issue count — a maturity signal that feeds the go/no-go risk list — differs by 1.8× between files, all three tagged `[EMPIRICAL]` from the GitHub API on the same day.

**Evidence:**
- maturity: *"**575 open issues** against **380 issues closed from the May-onward cohort** [EMPIRICAL] (GitHub search API, 2026-08-21)"*, carried into its risk summary as *"a 575-issue open backlog"*.
- notification-watcher: *"carries **1,011 open issues** **[EMPIRICAL, GitHub API]**"*.
- production-evidence: *"**1,011 open vs 718 closed all-time** — open issues exceed lifetime closures"*, and elsewhere *"a corpus of 1,729 issues (1,011 open + 718 closed)"*.

**Suggestion:** Two-to-one favours 1,011; the likely cause is maturity using a `search/issues` query that excludes pull requests or applies a date filter. Restate with the query shown, and correct maturity's risk-summary line.

---

**COHERENCE-A-010**
**Severity:** Moderate
**Dimension:** temporal_coherence, cross_document_consistency
**Location:** `gemini-deep-research-output.md`:Executive Summary/§6 ↔ `research-maturity-open-bugs.md`:release table ↔ `research-gate-mechanics-handson.md`:"Environment and versions"

**Description:** The Gemini file is written one release behind and misdates the release it does name, so every "as of August 2026" claim in it is anchored to the wrong baseline — including its production-readiness verdict.

**Evidence:**
- gemini: *"As of August 21, 2026, the Gas City ecosystem operates on the stable v1.4.0 release"* and *"The August 2026 v1.4.0 release demonstrates a highly mature production posture."*
- maturity release table: *"v1.4.0 | 2026-07-24 | minor (breaking)"*, *"v1.4.1 | 2026-08-15 | patch (latest)"*.
- gate-mechanics installed and ran it: *"`gc` (Gas City) | **1.4.1** (`gc version` → `1.4.1`)"*.

**Suggestion:** Re-baseline or annotate the Gemini file to v1.4.1 (2026-08-15) and correct v1.4.0 to July. Its v1.4.0-attributed claims (retry/drain hardening, MCP-trust stall fix, run-centered dashboard) need the same date check.

---

**COHERENCE-A-011**
**Severity:** Moderate
**Dimension:** cross_document_consistency, cross_reference_integrity
**Location:** `research-notification-watcher-layer.md`:"Gap list" item 6 ↔ `research-human-verdict-patterns.md`:§8 ↔ `research-gate-mechanics-handson.md`:Q3

**Description:** Three files state Momentum's *own* plan-gate verdict vocabulary three different ways, and none matches the shipped renderer. Gap item 6 ("Three-way verdicts") scopes real design work against one vocabulary while the fork-metadata schema in another file uses a different one.

**Evidence:**
- notification-watcher: *"Momentum's gate offers Approve / Modify / Re-run AVFL. A gate bead has two terminal states (open/closed). Modify and Re-run need a convention"*.
- human-verdict: *"maps to writing one metadata key per fork (`verdict.fork.<slug>=adopt|change|reject` plus a reason)"*; gate-mechanics uses the same words in its transcript: *"`bd gate resolve g2-gea -r \"developer verdict: fork-1 adopt; fork-2 change\"`"*.
- Ground truth in the source both cite, `/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md`: the top-level radios are `value="approve"` / `value="modify"` / `value="avfl"` (lines 384–386), and the per-fork options are `["Approve as specified", "Modify scope or sequencing", "Remove from sprint"]` (line 218) — "adopt" and "reject" appear nowhere.

**Suggestion:** Fix to the renderer's two-level vocabulary: top-level `approve | modify | avfl`, per-fork `approve-as-specified | modify-scope | remove`. Both the metadata-key proposal and the three-way-verdict gap item should key off the same enum.

---

**COHERENCE-A-012**
**Severity:** Moderate
**Dimension:** cross_document_consistency, temporal_coherence
**Location:** `research-gate-mechanics-handson.md`:"Environment and versions"/Cleanup ↔ `research-cycle-orchestration-fit.md`:§10 ↔ `research-notification-watcher-layer.md`:"Glue scope estimate"/Confidence ↔ `research-human-verdict-patterns.md`:§7 ↔ `research-beads-coupling-dec028.md`:§6

**Description:** Four files assert `gc` is not installed on this machine; one installed it globally and ran 400 lines of transcripts against it. Beyond the flat contradiction, three files park open questions and hedge a cost estimate on an absence that no longer holds — so the corpus under-reports what it actually verified.

**Evidence:**
- gate-mechanics: *"`mise use -g github:gastownhall/gascity@latest` — succeeded first try"*, and *"`mise use -g github:gastownhall/gascity@1.4.1` did add a line to `~/.config/mise/config.toml`"* (a persistent global install).
- cycle-orchestration-fit §10: *"Untested here — `gc` is not installed on this machine [[EMPIRICAL]] (`which gc` → not found)."*
- notification-watcher: *"I did not install `gc` (that is sub-question 1's job), so nothing here about `gc events --follow` behavior is empirical"* and *"That estimate assumes `gc` is installed and a city is running — **neither is true in Momentum today**, and neither is costed here."*
- human-verdict §7: *"I exercised the `bd`-direct write path, since `gc` is not installed here."*
- beads-coupling §6: *"`command -v gc dolt flock tmux` → all NOT-INSTALLED"* and *"No hands-on run … nothing here is behaviorally verified."*

**Suggestion:** Add a corpus-level environment note stating gc 1.4.1 was installed globally during this session, and re-scope the four hedges: notification-watcher's 6–9 day estimate no longer needs its "gc not installed" caveat, and cycle-orchestration-fit's open questions 1–3 are now answerable.

---

**COHERENCE-A-013**
**Severity:** Minor
**Dimension:** cross_document_consistency
**Location:** `research-human-verdict-patterns.md`:§5 ↔ `research-notification-watcher-layer.md`:"bd show --watch and bd gate" ↔ `research-hitl-alternative-patterns.md`:§2 ↔ `research-maturity-open-bugs.md`:"#4399"

**Description:** Three enumerations of `bd` gate types, two of which imply a `bead` gate is creatable. Only the maturity file draws the create/check distinction, and it says the opposite.

**Evidence:**
- human-verdict quotes `bd gate --help` on bd 1.0.4 with four: *"human … timer … gh:run … gh:pr"*.
- notification-watcher, same CLI and version: *"Gate types are `human`, `timer`, `gh:run`, `gh:pr`, `bead`."* hitl-alternative §2 presents a five-row table including *"`bead` | a bead in another rig to close | resolve manually"*.
- maturity, quoting #4399: *"`mail` … exists in neither `bd gate create --type` (`human`/`timer`/`gh:run`/`gh:pr`) nor `bd gate check --type` (`gh`/`gh:run`/`gh:pr`/`timer`/`bead`) … `human` is in `create` but not `check` … **`bead` is the inverse.**"*

**Suggestion:** State the two lists separately wherever gate types are enumerated — creatable types (4) vs. checker-evaluated types (5) — so no reader plans a `--type=bead` gate.

---

**COHERENCE-A-014**
**Severity:** Minor
**Dimension:** cross_document_consistency, logical_soundness
**Location:** `research-hitl-alternative-patterns.md`:§4 ↔ `research-human-verdict-patterns.md`:§6 ↔ `research-production-evidence.md`:Finding 3

**Description:** Two files prove `interaction_mode` is unenforced prompt text; a third treats it as a binding contract that "forbids" Momentum a pattern — and Gemini builds a recommendation on it (COHERENCE-A-005). A convention in someone else's packs cannot constrain a pack Momentum authors.

**Evidence:**
- human-verdict §6: *"`interaction_mode` is stamped to `gc.var.interaction_mode` and read **by agent prompts** … It is an instruction to a language model, not a control-flow gate; I found zero references to it in any check script. … **Do not mistake either for a HITL mechanism.**"*
- production-evidence Finding 3: *"The README's own gloss confirms the softness: `interaction_mode` \"**describes** human participation in planning and gates\". Describes, not enforces."*
- hitl-alternative §4: *"Worse, the packs' own mode contract **forbids** it"*, with a table headed "Required behavior", and *"The PR-review asset **enforces** it"* — the quoted enforcement being prompt prose (*"In `headless` interaction mode, never wait on a human"*).

**Suggestion:** Downgrade "forbids/enforces" to "the shipped packs' prompt convention says", and note that a Momentum-authored pack sets its own mode prose. hitl-alternative's "invert the pattern" conclusion should then rest on the session-lifetime argument alone.

---

**COHERENCE-A-015**
**Severity:** Minor
**Dimension:** consistency, clarity
**Location:** `research-gate-mechanics-handson.md`:Q2 "Bonus finding" vs. "The defect: `type` and `timeout` are not persisted"

**Description:** The close-side-enforcement transcript in Q2 uses bead IDs from a different formula and city than the section it sits in — the blocker shown is the *timer* gate introduced two sections later, not the human `test-gate` under discussion. A reader tracking IDs cannot reproduce the walk, and the conclusion table cites this transcript as the basis for the mid-story-tooling-gate verdict.

**Evidence:** Q2 reads *"Attempting to close a gated step out from under its gate … `$ bd close gt-bvw --reason \"attempting bypass\"` / `cannot close gt-bvw: blocked by open issues [gt-2zt]`"* — but neither ID is in the cook output (*"gatetest.a -> gt-o86 / gatetest.b -> gt-b3e / gatetest.gate-b -> gt-crp"*), and `gt-2zt` is identified later as *"`$ bd gate show gt-2zt` / `○ gt-2zt - Gate: timer auto-5s`"*.

**Suggestion:** Label the transcript as coming from the timer-gate probe, or re-run it against `gt-b3e`/`gt-crp`. The finding itself (a gate blocks closure, not just readiness) is type-independent and stands.

---

**COHERENCE-A-016**
**Severity:** Minor
**Dimension:** consistency
**Location:** `research-notification-watcher-layer.md`:"Bottom line" vs. "What already exists upstream"

**Description:** The same reference implementation is sized twice, differently, in one document.

**Evidence:** *"the watcher is a **220-line** shell script that exists upstream"* vs. *"Its **222-line** implementation is a near-exact template."*

**Suggestion:** Pick one line count and use it in both places, or drop the number from the bottom-line sentence.

---

**COHERENCE-A-017**
**Severity:** Minor
**Dimension:** temporal_coherence
**Location:** `research-maturity-open-bugs.md`:"Project shape" ↔ `research-gate-mechanics-handson.md`:"The notification gap" ↔ `research-notification-watcher-layer.md`:"What already exists upstream" ↔ `research-human-verdict-patterns.md`:Sources

**Description:** Documents dated 2026-08-21 cite a repository state dated 2026-08-22 — a day in their own future — while two sibling files pin the same observation to 2026-08-21. Probably a UTC/local skew, but it is unexplained and makes the corpus's observation window ambiguous.

**Evidence:** maturity: *"last push **2026-08-22**"*; gate-mechanics: *"They exist only on `main` (repo `pushed_at` **2026-08-22**)"* — against notification-watcher's *"asset timestamp **2026-08-21**T23:44Z"* and human-verdict's *"`gascity` @ `151168c7`, **2026-08-21**"*.

**Suggestion:** Normalize all repo-state timestamps to UTC with the zone shown, and state the corpus observation cutoff once in the scope file.

---

**COHERENCE-A-018**
**Severity:** Minor
**Dimension:** convention_adherence, clarity
**Location:** corpus-wide — `research-cycle-orchestration-fit.md` vs. `research-maturity-open-bugs.md` vs. `research-production-evidence.md`:"Method and evidence base"

**Description:** The provenance-tag system the corpus depends on for evidence weighting is written four ways, and one tag is used in a file that never defines it. Mechanical extraction of evidence class is unreliable across files.

**Evidence:** cycle-orchestration-fit uses the link form `[[OFFICIAL]](url)`; maturity uses bare `[OFFICIAL]` / `[EMPIRICAL]`; gate-mechanics, human-verdict, notification-watcher, beads-coupling use bold `**[OFFICIAL]**`; notification-watcher introduces a compound `**[UNVERIFIED as to source; OFFICIAL as to docs]**`. `[PRAC]` is defined only in production-evidence (*"**[PRAC]** — practitioner blogs with URLs"*) but used in maturity's source list (*"The New Stack … **[PRAC]** — background only"*).

**Suggestion:** Normalize to one tag form and put the four-class legend in `scope.md` so every file inherits it.