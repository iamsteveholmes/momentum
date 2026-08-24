# AVFL Consolidated Validation Report
## Gas City HITL Gates & Cycle Orchestration Research Corpus

**Date:** 2026-08-24  
**Corpus:** 9 files (8 research-*.md + gemini-deep-research-output.md)  
**Reviewers:** 8 (Structural, Accuracy, Coherence, Domain × Enumerator + Adversary)  
**Validation Stage:** Final (synthesis pending)

---

## Score & Grade

| Metric | Value |
|--------|-------|
| **Initial Score** | 100 |
| **Critical Deductions** | −75 (5 critical × −15) |
| **Major Deductions** | −120 (15 major × −8) |
| **Minor Deductions** | −21 (7 minor × −3) |
| **Low Deductions** | −2 (2 low × −1) |
| **Final Score** | **−18** → **GRADE: FAILING** |
| | |
| **Resolved During Validation** | 1 (Q3 empty section — file repaired) |
| **Deduped** | 25 distinct findings from 92 raw reviewer findings |
| **Discarded as Hallucination** | 0 (all investigated findings held evidence) |
| **Critical Findings** | 5 |
| **Major Findings** | 15 |
| **Minor Findings** | 7 |
| **Low Findings** | 2 |

---

## Breakdown by Severity & Confidence

| Severity | Count | Confidence | Median Reporters |
|----------|-------|------------|----|
| **Critical** | 5 | HIGH (all cross-lens) | 3–5 per finding |
| **Major** | 15 | HIGH (8), MEDIUM (7) | 2–4 per finding |
| **Minor** | 7 | MEDIUM (6), LOW (1) | 1–3 per finding |
| **Low** | 2 | MEDIUM | 1–2 per finding |

---

## Critical Findings (Severity: CRITICAL, −15 each)

### CRIT-001: Gemini file — untagged, contradicts empirical corpus on every major axis
**Location:** `gemini-deep-research-output.md` (entire file)  
**Confidence:** HIGH (4 lenses: Structural, Accuracy, Coherence, Domain)  
**Reporters:** STRUCTURAL-E-002, STRUCTURAL-A-004, ACCURACY-A-001/A-004/A-007/A-008, COHERENCE-A-006/A-010, DOMAIN-E-001, DOMAIN-A-006  
**Dimension:** domain_rule_compliance, fitness_for_purpose, evidence_completeness

**What:** The Gemini LLM output carries ZERO evidence tags (`[OFFICIAL]`, `[EMPIRICAL]`, `[PRAC]`, `[UNVERIFIED]`) in a corpus where every other file tags every claim, and it contradicts empirically-verified findings on every decision-relevant point — yet carries no caveats, and no synthesis exists to reconcile it.

**Why it matters:** A reader following the Gemini file's recommendations will implement constructs proven unsafe (check loops for gate control), on tools proven absent from releases (notify orders), using configuration proven impossible (exec step in v2), with confidence from a source that is untagged and internally contradictory.

**Evidence:** 
- Contradictions: v1.4.0-as-current (actually v1.4.1, 2026-08-15); dashboard as "React 19 SPA on Node 24 at port 8082" (actually gc binary, port 8372, no gate view); "functionally equivalent" notify orders shipped in v1.4.0 (actually 404 at all tags, edge-only); exec step in formulas (no such step exists, silent no-op); `interaction_mode` enforces behavior (actually prompt text); check loops work for HITL (actually cannot wait, exhaustion closes failed)
- No caveats: string search `unverified|caveat|limitation|confidence` returns one hit ("empirical" in prose)
- Tags: zero `[OFFICIAL]`, zero `[EMPIRICAL]`, zero `[UNVERIFIED]` across 4,462 words

**Suggestion:** Head the file `[UNVERIFIED LLM output — see research-gate-mechanics-handson.md / research-production-evidence.md for empirical corrections]` or move to appendix/cross-check exhibit, superseded by tagged files wherever they conflict.

---

### CRIT-002: notify/renudge orders absent from tagged releases; Gemini claim "folded into core" is false
**Location:** `gemini-deep-research-output.md:Follow-Up Q1` vs `research-gate-mechanics-handson.md:The notification gap` + `research-notification-watcher-layer.md` + `research-production-evidence.md:Finding 2`  
**Confidence:** HIGH (3 lenses: Accuracy, Coherence, Domain; both Enumerators + both Adversaries across lenses)  
**Reporters:** ACCURACY-E-001, ACCURACY-A-002, ACCURACY-A-005, COHERENCE-E-001, COHERENCE-A-004, DOMAIN-E-002, DOMAIN-A-005  
**Dimension:** correctness, fitness_for_purpose

**What:** Gemini asserts: *"Gas City does ship functionally equivalent mechanical housekeeping orders in its tagged releases. Recent releases (including v1.4.0) bundle orders named gate-sweep, nudge-mail-sweep, nudge-on-route, and cascade-nudge-on-blocker-close… not restricted to main/edge branches."* Two independent hands-on sources prove all false.

**Why it matters:** The recommendation to use native notification machinery depends on these orders existing. They do not. Momentum would inherit no working reflex; it would need ~6–9 days of glue work (watcher+notifier) that the corpus assumes is already built.

**Evidence:**
- **404 at all release tags:** raw.githubusercontent.com/gastownhall/gascity/v1.4.1/internal/bootstrap/packs/core/orders/notify-on-human-gate-creation.toml → **404**; v1.4.0 and v1.3.5 same. gate-sweep.toml at v1.4.1 → 200. Notifier orders exist only on `main`/`edge` (rolling-main pre-release, "not for production").
- **gate-sweep deliberately excludes human gates:** script body is exactly two lines: `gc bd gate check --type=timer --escalate` and `gc bd gate check --type=gh --escalate || true`. No human-gate check anywhere.
- **"functionally equivalent" is false on the only axis that matters:** the two orders that Momentum needs (`notify-on-human-gate-creation`, `renudge-stale-human-gates`) are 404. The one order that ships (`gate-sweep`) does not notify on human gates.

**Suggestion:** Strike "functionally equivalent" and state: "notify and renudge orders landed on `main`/`edge` 2026-07-23, not in any tagged release as of v1.4.1. Vendoring the two order files is the supported adoption path (research-notification-watcher-layer.md gap #3)."

---

### CRIT-003: #2311 and #3200 misidentified; #2311 OPEN barrier bug, not patched data-loss issue
**Location:** `gemini-deep-research-output.md:§6 Table 3 (Mitigated and Persistent Architectural Bugs)` vs `research-maturity-open-bugs.md`  
**Confidence:** HIGH (2 lenses: Accuracy, Coherence; both Enumerators + both Adversaries)  
**Reporters:** ACCURACY-E-002, ACCURACY-A-001, COHERENCE-A-006  
**Dimension:** correctness, traceability

**What:** Gemini describes *"#2311 / #3200 — A critical latent data-loss path where gc dolt health --json misclassified active, registered rig databases as orphans. Patched."* Actual issue: **#2311 is OPEN** (`waits_for = "children-of(X)" does not gate bd ready`), a barrier-semantics bug, no fix PR. **#3200 is uncorroborated** (appears nowhere in the corpus).

**Why it matters:** #2311 is one of two load-bearing blockers for Momentum's post-sprint results gate (the other is #3451). A "Patched" verdict removes a critical risk flag from a decision that depends on it.

**Evidence:**
- **Verified from GitHub API:** api.github.com/repos/gastownhall/gascity/issues/2311 → title `"waits_for = \"children-of(X)\" does not gate bd ready when X uses on_complete bond fanout"`, state **open**, labels `kind/bug, priority/p2`, last activity 2026-05-29, no fix PR.
- **maturity file confirms:** *"#2311 `waits_for = \"children-of(X)\" does not gate bd ready` — **OPEN**, last activity 2026-05-29, no fix PR, no maintainer ruling, no milestone."*
- **#3200:** appears only in Gemini; grep across all 8 research-*.md returns zero hits.

**Suggestion:** Replace Table 3 rows. For #2311: correct to OPEN with stated title/timeline. For #3200: drop or independently source. Flag "Patched"/"Mitigated" as unsupported.

---

### CRIT-004: GC_BEADS=file exists; gate-mechanics author conflated two different tools' configuration
**Location:** `research-gate-mechanics-handson.md:City setup: what gc actually requires` vs `research-beads-coupling-dec028.md:§2` + `gemini-deep-research-output.md:§7`  
**Confidence:** HIGH (3 lenses: Accuracy, Coherence, Domain; cross-lens agreement)  
**Reporters:** ACCURACY-A-003, COHERENCE-A-001, DOMAIN-A-002  
**Dimension:** correctness, logical_soundness, category_error

**What:** gate-mechanics asserts: *"There is no `GC_BEADS=file` escape hatch in 1.4.1 — `bd init --help` states 'Dolt is the default (and only supported) storage backend.'"* This is a category error. `bd init` selects **beads' own** storage backend; `GC_BEADS` selects **gc's** bead-store implementation (BdStore, NativeDoltStore, FileStore, exec.Store). The two are orthogonal switches.

**Why it matters:** This negative claim feeds the DEC-028 recoupling argument that Gas City forces Dolt. beads-coupling §7's entire "Forced: nothing" verdict rests on `GC_BEADS=file` existing and being load-bearing. If the file path is unavailable, the recommendation flips from "safe to adopt" to "must adopt Dolt or run on session-local embedded store."

**Evidence:**
- **FileStore exists in five independent sources on current main:**
  - `factory.go` switch arm: `case provider == "file": … callStoreOpen("file store", opts.OpenFileStore)`
  - gc's own error string: `"bd not found in PATH (install beads or set GC_BEADS=file)"`
  - `docs/getting-started/faq.md`: *"For the lightest possible start, `GC_BEADS=file` skips the dolt + bd pair."*
  - Config reference enum: `provider = "bd" (default, Dolt-backed), "file", or "exec:<script>"`
  - `gc doctor` provider-awareness
- **gate-mechanics' evidence is inapplicable:** `bd init --help` describes beads' backend, not gc's provider. The author had gc 1.4.1 **installed** and never tested the claim.

**Suggestion:** Strike the `GC_BEADS=file` negative from gate-mechanics. If retained, verify directly: `GC_BEADS=file gc init` / `gc doctor` on the installed gc 1.4.1. Preserve the true finding: gc's `.start` needs tmux + dolt + flock to boot a production-ready city.

---

### CRIT-005: exec step in v2 formulas doesn't exist; silent no-op failure for prescribed construction
**Location:** `research-hitl-alternative-patterns.md:§2 + §7(b)` + `research-gate-mechanics-handson.md` vs `research-cycle-orchestration-fit.md:§1`  
**Confidence:** HIGH (3 lenses: Accuracy, Coherence, Domain; cross-lens agreement)  
**Reporters:** ACCURACY-A-006, COHERENCE-A-002, DOMAIN-A-001  
**Dimension:** fitness_for_purpose, silent_failure_risk

**What:** The corpus's primary recommendation — route Momentum's gates through `bd gate create --type=human` — is prescribed as *"an ordinary `exec` step that shells `bd gate create --type=human --blocks <next-step-bead>` and exits"* in hitl-alternatives §2/§7(b) and gate-mechanics. No such step key exists in v2 formulas.

**Why it matters:** An unknown step key in a v2 formula compiles clean and does nothing silently (verified against formula-spec-v2 §1). A developer authoring per the prescription would create no gate. The approval step would pass through unchecked while the developer is away.

**Evidence:**
- **cycle-orchestration-fit §1:** exhaustive v2 step-key table: `id, title, description, description_file, notes, type, priority, tags, metadata, depends_on, needs, condition, children, assignee, expand, expand_vars, loop, waits_for, gate, check, retry, drain, on_complete, tally, timeout`. *"There is no `exec`, `command`, `run`, or `script` key."*
- **Spec warning (formula-spec-v2 §1.8):** *"Unknown step keys are silently ignored. A typo like `dependson` produces no diagnostic — the dependency simply vanishes."*
- **Empirical:** grep of all gascity-packs finds **zero** invocations of `claude -p`, `claude --print`, or `codex exec`.

**Suggestion:** Re-specify against a construct that exists: order-level `exec`, `[steps.check].check.path`, or prose in a `description_file` instructing the agent to run `bd gate create`. Resolve `--blocks` target (downstream step, not creating step) and specify bead-id discovery (e.g., `gc.root_bead_id` + `gc.step_ref`). Also note the two docs prescribe opposite `--blocks` targets, and neither says how a step obtains its successor's bead id (cook-time, not authoring-time).

---

## Major Findings (Severity: MAJOR, −8 each)

### MAJ-001: v1.4.0 vs v1.4.1 currency: Gemini written one release behind
**Location:** `gemini-deep-research-output.md:Executive Summary, §6` vs `research-maturity-open-bugs.md:release table` + `research-gate-mechanics-handson.md:Environment and versions`  
**Confidence:** HIGH (4 lenses)  
**Reporters:** ACCURACY-E-005, ACCURACY-A-007, COHERENCE-E-002, COHERENCE-A-010  
**Dimension:** correctness, temporal_coherence

**What:** Gemini states *"As of August 21, 2026, the Gas City ecosystem operates on the stable v1.4.0 release"* and *"The August 2026 v1.4.0 release demonstrates a highly mature production posture."* Actual: v1.4.1 shipped 2026-08-15; v1.4.0 shipped 2026-07-24.

**Why it matters:** Every "as of August 2026" claim in Gemini is anchored to the wrong baseline. v1.4.0-attributed fixes and capabilities need re-verification against v1.4.1's actual release notes.

**Evidence:** maturity release table: v1.4.0 | 2026-07-24; v1.4.1 | 2026-08-15 (latest). gate-mechanics installed and ran it: `gc version` → `1.4.1`.

**Suggestion:** Re-baseline Gemini to v1.4.1 (2026-08-15); correct v1.4.0 to July 24. Where Gemini credits a fix to v1.4.0, verify against maturity's release table before retaining.

---

### MAJ-002: Dashboard architecture wrong: port 8082 vs official 8372; no gate view, no blocked-work queue
**Location:** `gemini-deep-research-output.md:§4 "The Gas City Dashboard Architecture"` + `:§8 Recommendation 2` vs `research-notification-watcher-layer.md:The dashboard's treatment of blocked/gated work`  
**Confidence:** HIGH (4 lenses)  
**Reporters:** ACCURACY-E-004, ACCURACY-A-008, COHERENCE-E-004, COHERENCE-A-008  
**Dimension:** correctness, traceability

**What:** Gemini: *"a highly responsive Single Page Application (SPA) built on React 19, statically served by a Node 24 backend… running locally, defaulting to port 8082."* Operators can *"filter for beads requiring human approval."* Recommendation: *"Standardize on the Gas City Dashboard for HITL operations."* Actual: compiled into gc binary, served at 8372, no gate view, no blocked-work queue, no approval filtering.

**Why it matters:** The recommendation to use the dashboard for HITL is grounded on affordances that do not exist. A loopback single-operator dashboard with no gate view is structurally wrong for the out-of-session orchestration case that motivates Gas City adoption.

**Evidence:** docs.gascity.com/getting-started/dashboard: bound to port **8372**, *"compiled into the `gc` binary"*. Surfaces: agents, sessions, beads, mail, formula runs, health view — no gate view, no blocked-work queue. Independently confirmed: raw install on 1.4.1 shows `127.0.0.1:8372` with the stated surfaces only.

**Suggestion:** Delete the React/Node/8082 architecture section and Table 2's approval-filtering row. Withdraw Recommendation 2 or restate it on actual dashboard constraints.

---

### MAJ-003: Wedge bugs #2131/#2168 dated to v1.4.0; actually v1.2.0 window (2026-05-23/26)
**Location:** `gemini-deep-research-output.md:Table 3` vs `research-maturity-open-bugs.md`  
**Confidence:** HIGH (2 lenses)  
**Reporters:** ACCURACY-E-003, ACCURACY-A-001  
**Dimension:** correctness

**What:** Gemini: *"Dispatcher Wedge (#2131 / #2168)… Mitigated in v1.4.0."* maturity: *"Both are genuinely resolved in the v1.2 window (v1.2.0, 2026-05-29) via PR #2497 and commit 6c9af50."*

**Why it matters:** Release attribution error. v1.2.0 was released 2026-05-29; v1.4.0 was 2026-07-24. The date is off by two minor versions.

**Evidence:** maturity file, which quotes issue CLOSED/COMPLETED dates (2026-05-23, 2026-05-26) and cites the fix PR and commit hash.

**Suggestion:** Correct attribution to v1.2.0 (2026-05-29), not v1.4.0.

---

### MAJ-004: Open issues count: 575 vs 1,011 unreconciled (1.76× discrepancy)
**Location:** `research-maturity-open-bugs.md:"Project shape"` vs `research-notification-watcher-layer.md` + `research-production-evidence.md:Finding 7`  
**Confidence:** HIGH (2 lenses)  
**Reporters:** ACCURACY-A-004, COHERENCE-E-005, COHERENCE-A-009  
**Dimension:** consistency, traceability

**What:** maturity reports *"**575 open issues** against 380 issues closed from the May-onward cohort"* (search API); notification-watcher reports *"**1,011 open issues** [EMPIRICAL, GitHub API]"* (repo endpoint). production-evidence: *"**1,011 open vs 718 closed**"* (all-time).

**Why it matters:** A maturity signal feeding the go/no-go decision is reported at 1.76× different magnitudes, all tagged `[EMPIRICAL]`, with no stated query method. 575 feeds a "575-issue backlog" risk summary; 1,011 paints a different maturity picture.

**Evidence:** Root cause: GitHub's `api.repos/…/open_issues_count` includes issues + open PRs; search API with `is:issue is:open` counts issues only. Two different quantities both labeled "open issues."

**Suggestion:** Restate with query method shown. Keep 575 as issues-only; annotate 1,011 as `open_issues_count` (issues + PRs). Correct maturity's risk-summary line to reflect both counts.

---

### MAJ-005: packs/ prefix 404s: four citations use wrong repo path
**Location:** `research-production-evidence.md:Finding 1` and `:Finding 3`  
**Confidence:** MEDIUM (only Adversary found; empirically verified)  
**Reporters:** STRUCTURAL-A-006  
**Dimension:** cross_reference_integrity

**What:** Four citations use a `packs/` prefix that doesn't exist in gascity-packs: `packs/pr-pipeline/…`, `packs/contributing/…`, `packs/gstack/…`. Verified: all 404 as written; all 200 with the prefix removed.

**Why it matters:** Broken citations undermine the evidence for the two findings that rest on them (Finding 1 — "Zero formulas use [steps.gate]"; Finding 3 — "Packs that advertise 'human gates'…").

**Evidence:** Raw GitHub fetches: `packs/pr-pipeline/formulas/mol-pr-start.formula.toml` → 404; `pr-pipeline/formulas/mol-pr-start.formula.toml` → 200. Repo root contains the pack dirs at root level, not under `packs/`.

**Suggestion:** Strip the `packs/` prefix from all four citations. The underlying evidence is sound; only the paths are wrong.

---

### MAJ-006: DEC-028 re-score table missing Gate 2 (the load-bearing gate)
**Location:** `research-beads-coupling-dec028.md:§7 "Re-scored against DEC-028's own gates"`  
**Confidence:** MEDIUM (only Adversary found; verified against DEC-028 source)  
**Reporters:** STRUCTURAL-A-007  
**Dimension:** completeness, logical_soundness

**What:** The re-score table covers G1, G3, G4, and "Multi-agent write safety." **Gate 2 is missing.** DEC-028 requires *"3 of 4 gates positive"* to flip; an incomplete table cannot support the 3-of-4 arithmetic.

**Why it matters:** Gate 2 is the specific gate DEC-028 makes the authoritative migration conditional on: *"Did `discovered-from` eliminate intake-queue triage toil?"* Gas City adoption's coupling to this gate is unknowable from a table that omits it.

**Evidence:** DEC-028 source (dec-028-beads-tracker-memory-substrate-adoption-2026-05-16.md) lists four gates with equal weight; beads-coupling's table has only three (plus a non-gate row).

**Suggestion:** Add a G2 row. If Gas City adoption is genuinely neutral to `discovered-from`/intake-queue toil, state so and mark it Neutral; a silent omission breaks the re-score.

---

### MAJ-007: FileStore metadata durability unverified; recommendation depends on it
**Location:** `research-beads-coupling-dec028.md:§8 "FileStore metadata durability"` + `:§2` + `:§7`  
**Confidence:** MEDIUM (only Adversary flagged; gap is real)  
**Reporters:** STRUCTURAL-A-008  
**Dimension:** fitness_for_purpose, unverified_dependency

**What:** The recommended adoption topology (`GC_BEADS=file` city) stores gate status and per-fork verdicts in bead metadata. Whether `FileStore.SetMetadata` persists or inherits `MemStore`'s no-op is explicitly marked `[UNVERIFIED]`. The probe ran only against bd's embedded Dolt store, never a file-backed city.

**Why it matters:** If FileStore.SetMetadata is a no-op, the entire gate-verdict persistence strategy fails silently.

**Evidence:** beads-coupling §8: *"Whether `FileStore.SetMetadata` persists or inherits `MemStore`'s no-op is not stated in the fetched material **[UNVERIFIED]**."* Same file §1 table: "`MemStore` | in-memory slice | Test double; `SetMetadata` is a no-op."* Hands-on scope: researcher used "bd's own embedded Dolt," not a file-backed city.

**Suggestion:** Verify before synthesis: `GC_BEADS=file gc init` + metadata round-trip probe on the installed 1.4.1. Carry the caveat into the recommendation if unverified.

---

### MAJ-008: beads version timeline mismatch: v1.2.2 vs v1.1.0 vs v1.2.1
**Location:** `research-gate-mechanics-handson.md:Environment table` + `:CHANGELOG` vs `research-beads-coupling-dec028.md:§6` + `research-production-evidence.md:Finding 5`  
**Confidence:** HIGH (3 separate quotes of the same artifact)  
**Reporters:** COHERENCE-E-003, COHERENCE-A-007  
**Dimension:** consistency, traceability

**What:** gate-mechanics states *"`bc` (beads), gc-pinned | **1.2.2**"* citing *"gc 1.4.1's CHANGELOG entry… '**beads pinned to v1.2.2 everywhere** (go.mod library, `deps.env` `BD_VERSION`, CI matrix…)'"*. beads-coupling quotes `deps.env` on current `main` as *"`BD_VERSION=v1.1.0`"* and concludes v1.1.2 is newest. production-evidence cites *"Beads 1.2.1 Incident Report"* from 2026-08-20.

**Why it matters:** beads-coupling's entire "Multi-agent write safety via CAS is not yet available" conclusion rests on the beads version. If v1.2.x is current (vs v1.1.2), the CAS-unavailable row and the "Weakens" direction on the multi-agent gate must be re-scored.

**Evidence:** Three conflicting figures all attributed to the same day (2026-08-21) or close (2026-08-20 for production-evidence).

**Suggestion:** Pin `deps.env` at a named commit and the beads release timeline once for the corpus. If v1.2.x is current, re-score the multi-agent write safety gate in beads-coupling §7.

---

### MAJ-009: gate-mechanics closed-bypass proof uses wrong bead IDs (from timer probe, not human probe)
**Location:** `research-gate-mechanics-handson.md:Q2 "Bonus finding"` vs `same file:The defect`  
**Confidence:** MEDIUM (Accuracy Adversary found; underlying claim still likely sound)  
**Reporters:** ACCURACY-A-012, COHERENCE-A-015  
**Dimension:** traceability, evidence_matching

**What:** The close-side-enforcement finding (used to justify "mid-story tooling gates = best fit") cites transcript IDs from a *different* probe. Q2 shows `bd close gt-bvw --reason "attempting bypass"` blocked by `gt-2zt` (the timer gate). The human-gate probe used `gt-b3e`/`gt-crp`.

**Why it matters:** The finding is then cited as human-gate evidence; a reader tracking IDs cannot reproduce the walk.

**Evidence:** Q2 transcript introduces `gt-2zt` only later (*"Gate: timer auto-5s"*), after the close-bypass attempt. The human-gate cook output is `gatetest.a -> gt-o86 / gatetest.b -> gt-b3e / gatetest.gate-b -> gt-crp`.

**Suggestion:** Re-run the close-bypass against `gt-b3e`/`gt-crp` (human gate), or label the transcript as from the timer-gate city. The underlying claim (bd close is blocked by a gate, not just readiness) is type-independent and stands; the citation just doesn't show it for a human gate.

---

### MAJ-010: interaction_mode treated as binding contract; actually prompt text only
**Location:** `research-hitl-alternative-patterns.md:§2 + §4` vs `research-human-verdict-patterns.md:§6` + `research-production-evidence.md:Finding 3`  
**Confidence:** MEDIUM (Accuracy + Domain)  
**Reporters:** ACCURACY-A-006, COHERENCE-A-014, DOMAIN-A-014  
**Dimension:** correctness, logical_soundness

**What:** hitl-alternatives frames interaction_mode as a binding control-flow contract that *"forbids"* patterns and as something packs *"enforce"* (with a table headed "Required behavior"). Actually: it's prompt text read by language models, with no control-flow gate.

**Why it matters:** A convention in someone else's packs cannot constrain a pack Momentum authors. Framing it as binding inflates its governance weight.

**Evidence:** human-verdict §6: *"`interaction_mode` is stamped to `gc.var.interaction_mode` and read **by agent prompts**… It is an instruction to a language model, not a control-flow gate."* production-evidence: *"`interaction_mode` '**describes** human participation.' Describes, not enforces."* hitl-alternatives §4: *"the packs' own mode contract **forbids** it"* — the quoted enforcement is prompt prose: *"In `headless` interaction mode, never wait on a human."*

**Suggestion:** Downgrade "forbids/enforces" to "the shipped packs' prompt convention says," and note that Momentum-authored packs set their own mode prose.

---

### MAJ-011: type=human "costs nothing" for notification; actually costs the notification path
**Location:** `research-human-verdict-patterns.md:§5` + `research-maturity-open-bugs.md:"Why this is good news for Momentum"` vs `research-gate-mechanics-handson.md:"The defect: type and timeout"`  
**Confidence:** MEDIUM (Coherence + Domain)  
**Reporters:** COHERENCE-A-003, DOMAIN-A-004  
**Dimension:** correctness, domain_fitness

**What:** human-verdict and maturity assert: *"for `type = "human"`, it costs nothing: closing the gate bead is the human's job by definition."* gate-mechanics measures the cost: formula-cooked gates persist `await_type: null`; ad-hoc gates persist `"await_type":"human"`; both bundled notify reflexes filter on `[ "$AWAIT_TYPE" = "human" ] || continue`, so formula gates get no notification.

**Why it matters:** Assumes the only consumer of `type` is an auto-resolving watcher. Notification is the second consumer, and it's the half Momentum most needs. The `type` vocabulary carries no signal to the notifier.

**Evidence:** gate-mechanics Q4 transcript: `{"id":"gt-crp",…,"await_type":null}` (formula gate) vs `"await_type":"human"` (ad-hoc gate). Both `notify-on-human-gate-creation.toml` and `renudge-stale-human-gates.sh` (now known to be absent from releases) filter out nulls.

**Suggestion:** Correct both "costs nothing" statements to "costs the notification path, which is the half Momentum needs." Carry gate-mechanics' `await_type` measurement in as evidence.

---

### MAJ-012: DEC-035 coverage gap; corpus has zero mentions despite scope goal
**Location:** Corpus-wide (`raw/`) vs `scope.md:goals` + `dec-035-conduct-execution-engine-in-session-workflows-2026-05-30.md`  
**Confidence:** HIGH (2 lenses: Structural, Domain)  
**Reporters:** STRUCTURAL-A-001, DOMAIN-E-006  
**Dimension:** corpus_completeness, scope_fitness

**What:** Scope goal #4: *"produce the evidentiary basis for exercising DEC-035's revisit clause."* DEC-035 appears **zero times** across the 9 files. The revisit clause has two triggers ("out-of-session or multi-Conductor goal appears"); the corpus covers the first incidentally, the second not at all.

**Why it matters:** Synthesis cannot manufacture the missing half. A decision document depending on this corpus cannot be written until the evidence is present.

**Evidence:** Grep for `DEC-035`, `conductor`, `multi-conductor`, `concurrent sprint` → 0 hits in all 9 raw files. Scope: *"produce the evidentiary basis for exercising DEC-035's revisit clause."*

**Suggestion:** Before synthesis, add coverage (follow-up subagent or synthesis-stage section) scoring the evidence against BOTH revisit triggers: (a) what Gas City buys for out-of-session dispatch (assembled from existing files), and (b) whether it enables multi-Conductor operation (e.g., concurrent formula runs, `max_dispatches_per_tick`, v1.4.0 per-scope control-dispatcher, multi-city Dolt port collisions). Failing that, synthesis must state plainly that the multi-Conductor trigger was not researched.

---

### MAJ-013: Gemini body structure collapsed; unparseable for synthesis
**Location:** `gemini-deep-research-output.md:body (lines 9–18)`  
**Confidence:** HIGH (2 lenses: Structural, Coherence)  
**Reporters:** STRUCTURAL-A-003, COHERENCE-E-006  
**Dimension:** structural_validity, usability

**What:** The report body has no markdown structure: 18,897 characters on a single line, every heading concatenated into surrounding prose, both tables flattened into run-on strings with no row/cell delimiters, TOML config unfenced. **Zero code fences, one heading** (`## Follow-Up`) for a 4,462-word document.

**Why it matters:** Unparseable for section-targeted synthesis or citation. A synthsizer cannot extract claims by location when the file has no locations.

**Evidence:** Line 9: *"Research Report: Gas City Human-in-the-Loop Gates and Multi-Phase Cycle OrchestrationExecutive SummaryThe transition from localized…"* Table 1: *"PrimitiveDefinition and Operational FunctionAgentThe configured worker…"*

**Suggestion:** Re-extract with structure preserved or post-process: restore H2/H3 headings, re-form tables as pipe tables, fence code blocks.

---

### MAJ-014: Adoption cost pricing incomplete; orchestration rewrite unpriced
**Location:** `research-notification-watcher-layer.md:"Glue scope estimate"` vs `research-cycle-orchestration-fit.md:§9 "The honest characterization"`  
**Confidence:** MEDIUM (Domain Adversary)  
**Reporters:** DOMAIN-A-007  
**Dimension:** fitness_for_purpose, completeness

**What:** The corpus prices the gate glue (~6–9d) but leaves the orchestration rewrite unpriced. cycle-orchestration-fit names it: *"this is not 'wrap conduct in a formula.' It is 're-express Momentum's phase orchestration as a pack'"* — a rewrite of the orchestration layer. No document estimates that scope.

**Why it matters:** The go/no-go decision compares adoption cost to benefit. Comparing gate glue alone to the full benefit inflates the ROI picture.

**Evidence:** notification-watcher: *"That estimate assumes `gc` is installed and a city is running — neither is true in Momentum today, and neither is costed here."* cycle-orchestration-fit §9 lists orchestration constraints (`description_file` >4096B degrades to pointer, `[steps.tally]` removed, per-minor doctor fixes needed) but does not estimate rewrite scope.

**Suggestion:** Add a rewrite-scope estimate to cycle-orchestration-fit §9 using the five methodologies that walked the path (bmad/superpowers/gstack/pr-pipeline/contributing) — their formula+asset file counts as a proxy — and state the combined figure.

---

### MAJ-015: DEC-028 recommendation premise refuted; exec-order pattern doesn't exist
**Location:** `research-beads-coupling-dec028.md:§7 "Forced: nothing"` vs `research-cycle-orchestration-fit.md:§1–2`  
**Confidence:** MEDIUM (Domain Adversary)  
**Reporters:** DOMAIN-A-008  
**Dimension:** logical_soundness, fitness_for_purpose

**What:** beads-coupling derives "Forced: nothing" from: *"Under the exec-order pattern DEC-032 D3 adopted (`claude -p /momentum:<skill>` as a shell subprocess)…"* cycle-orchestration-fit proves this pattern doesn't exist in Gas City: v2 steps are work beads; the 300s exec-order cap cannot host a phase.

**Why it matters:** Under the actual shape (phases as formula steps routed to Claude Code agents), Momentum's phase work items **become city beads** — precisely the "second ledger stays separate" premise the decoupling argument depends on. The conclusion "Forced: nothing" may still hold, but not for the stated reason.

**Evidence:** cycle-orchestration-fit: *"The `claude -p` exec-step shape the sub-question assumes does not exist… v2 formula steps… are work beads that agents claim and execute."* A grep of all gascity-packs finds **zero** `claude -p`, `claude --print`, or `codex exec` invocations.

**Suggestion:** Re-derive beads-coupling §7 under the pack/formula-step shape rather than the exec-order shape. If the conclusion flips (beads becomes Momentum's authoritative ledger), that's a separate DEC-028 decision, not foreclosed by Gas City adoption alone.

---

## Minor Findings (Severity: MINOR, −3 each)

### MIN-001: beads #1467 misattributed as root cause of await_type defect
**Location:** `gemini-deep-research-output.md:Follow-Up Q1` vs corpus root cause (gascity compile.go)  
**Reporters:** ACCURACY-A-009, ACCURACY-E-006, COHERENCE-E-007, STRUCTURAL-E-006  
**Confidence:** MEDIUM (multiple, but minor scope)  
**Dimension:** traceability

**What:** Gemini attributes await_type defect to *"beads Issue #1467"*. Verified: #1467 (closed 2026-02-03) is *"Prevent closing machine-checkable gate issues unless condition satisfied"* — unrelated. Actual root cause: gascity compile.go cook/materialize path (proven in gate-mechanics).

**Suggestion:** Drop #1467 reference. Note that the formula-cook `await_type: null` defect has no upstream tracker found.

---

### MIN-002: Malformed section citations (missing v2 §; unresolvable milestone URL)
**Location:** `research-human-verdict-patterns.md:§5` + `research-maturity-open-bugs.md:"Project shape"`  
**Reporters:** STRUCTURAL-A-010, STRUCTURAL-A-009  
**Confidence:** MEDIUM  
**Dimension:** cross_reference_integrity

**What:** v2 spec citation missing section number (*"formula-spec-v2 §"*); milestone URL has ellipsis placeholder (*"milestone/…"*).

**Suggestion:** Fill in `§2` for v2 (Compilation, where gate-synthesis language lives); replace ellipsis with concrete milestone URL.

---

### MIN-003: Dolt floor reasoning conflates two separate facts
**Location:** `gemini-deep-research-output.md:§7`  
**Reporters:** ACCURACY-A-010  
**Confidence:** MEDIUM  
**Dimension:** logical_soundness

**What:** Gemini fuses two facts: *"Dolt ≥ 2.1.0 because releases prior to 1.86.2 lack critical fixes."* maturity correctly separates: 2.1.0 is the floor (v1.2.1 managed-Dolt check); pre-1.86.2 is a separate caveat for older/pre-release builds.

**Suggestion:** Split the sentence and attribute the floor to v1.2.1's managed-Dolt check.

---

### MIN-004: Gate types inventory conflict (create vs check distinction missing in 2 of 3 files)
**Location:** `research-human-verdict-patterns.md` + `research-hitl-alternative-patterns.md` + `research-maturity-open-bugs.md`  
**Reporters:** ACCURACY-A-014, COHERENCE-A-013  
**Confidence:** MEDIUM  
**Dimension:** consistency, clarity

**What:** Three files give three inventories of `bd` gate types; only maturity draws the create/check distinction. `bead` type is creatable (per some files) or checkable-only (per maturity) — opposite.

**Suggestion:** Standardize on two-column framing (creatable via `bd gate create` vs evaluable via `bd gate check`) across all files.

---

### MIN-005: gc installation state contradiction: 4 files say not installed; gate-mechanics installed it
**Location:** Corpus-wide  
**Reporters:** COHERENCE-A-012, COHERENCE-E-012  
**Confidence:** MEDIUM  
**Dimension:** temporal_coherence, cross_document_consistency

**What:** 4 files (cycle-orchestration-fit, notification-watcher, human-verdict, beads-coupling) state `gc` is not installed on the research machine. gate-mechanics §2 states: *"`mise use -g github:gastownhall/gascity@latest`"* then ran 400 lines of transcripts.

**Suggestion:** Add a corpus-level environment note that gc 1.4.1 was installed globally during this session. Re-scope the four hedges (notification-watcher's 6–9d estimate, cycle-orchestration-fit's open questions 1–3) — they are now answerable or superseded.

---

### MIN-006: Three verdict vocabularies for plan-gate (approve/modify/avfl vs adopt/change/reject)
**Location:** `research-notification-watcher-layer.md:Gap list item 6` vs `research-human-verdict-patterns.md:§8` vs `plan-gate-renderer.md:source`  
**Reporters:** COHERENCE-A-011  
**Confidence:** MEDIUM  
**Dimension:** consistency

**What:** Three files state Momentum's plan-gate verdict vocabulary three different ways; renderer source shows only one (approve/modify/avfl top-level, approve-as-specified/modify-scope/remove per-fork).

**Suggestion:** Align all references to the renderer's vocabulary.

---

### MIN-007: Dashboard line count mismatch (220-line vs 222-line script)
**Location:** `research-notification-watcher-layer.md:"Bottom line"` vs `same file:"What already exists upstream"`  
**Reporters:** COHERENCE-A-016  
**Confidence:** LOW (cosmetic)  
**Dimension:** consistency

**What:** Same reference implementation sized twice: 220-line and 222-line in the same file.

**Suggestion:** Pick one and use consistently.

---

## Low Findings (Severity: LOW, −1 each)

### LOW-001: await_type persistence: key-absent vs null distinction unclear
**Location:** `research-gate-mechanics-handson.md:"The defect"`  
**Reporters:** ACCURACY-A-013  
**Confidence:** MEDIUM  
**Dimension:** traceability, clarity

**What:** Claim: formula gate has *"no `await_type` key at all"*; evidence shown: `{"id":"gt-crp",…,"await_type":null}` (key present, null value). `jq` output cannot distinguish the two.

**Suggestion:** Either show `jq 'keys'` transcript or soften to "persists a null `await_type`" — both interpretations fail the notifier filter identically.

---

### LOW-002: Production evidence fork count as adoption signal
**Location:** `research-production-evidence.md:Finding 7`  
**Reporters:** DOMAIN-E-007  
**Confidence:** MEDIUM  
**Dimension:** domain_rule_compliance

**What:** File uses GitHub fork count (1,783) alongside download analytics to size adoption; forks are a gameable metric and absent from the stated methodology.

**Suggestion:** Drop or justify fork counts as secondary; rely on downloads and contributor distribution.

---

## Resolved During Validation (Not Scored)

### RESOLVED-001: Empty Q3 section in gemini-deep-research-output.md (STRUCTURAL-E-004 / STRUCTURAL-A-002)
**Status:** File was repaired post-validation; section now contains the Q3 answer.  
**Action:** Mark as resolved-during-validation; exclude from scoring.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Raw findings across 8 reviewers** | 92 |
| **Unique underlying issues (deduped)** | 29 |
| **Resolved during validation** | 1 (Q3 section) |
| **Findings with evidence** | 29 (all retained) |
| **Hallucinations discarded** | 0 |
| | |
| **Critical (HIGH confidence)** | 5 |
| **Major (HIGH confidence)** | 8 |
| **Major (MEDIUM confidence)** | 7 |
| **Minor** | 7 |
| **Low** | 2 |

---

## Overall Assessment

**Grade: FAILING (−18 / 100)**

The corpus contains **critical gaps** in evidence for its primary decision (multi-Conductor triggering of DEC-035 revisit is absent), **contradictions on every major axis** (exec step, notify orders, GC_BEADS, barrier construction, v1.4.0 vs v1.4.1), and a **single untagged LLM output** that is demonstrably wrong on every decision-relevant point yet sits in the corpus with no reconciliation.

**Before synthesis:**
1. Repair or demote the Gemini file (critical, 5 contradictions + zero tags).
2. Add multi-Conductor evidence or state plainly it was not researched.
3. Verify three assertions against the installed gc 1.4.1 (FileStore metadata, GC_BEADS workflow, dashboard features).
4. Reconcile beads version timeline and re-score multi-agent gate.
5. Rewrite exec-step and barrier recommendations against constructs that exist.
6. Resolve the DEC-035 half of the scope.

**This corpus cannot support a synthesis decision on Gas City adoption until these critical gaps are closed.**
