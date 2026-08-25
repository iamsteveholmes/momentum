# AVFL Fix Log — Iteration 3 (Convergence Pass)

**Corpus:** Gas City HITL gates and cycle orchestration research (`docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/`)
**Source:** `validation/avfl-consolidated-iter3.md` (FAILING, −38/100)
**Date:** 2026-08-24
**Method:** every finding re-derived from corpus evidence before writing (no suggestion transplanted verbatim); qualifiers propagated to every citation site and re-verified by grep; conclusion-first restructure applied to marker-buried passages; all sweeps run **backtick-tolerant** (markdown emphasis stripped before matching).

## Finding-count note (defect in the validation artifact, not the corpus)

`avfl-consolidated-iter3.md` states **27 consolidated findings** in its header and **13 / 10 / 4** in its scoring table, but its body enumerates **24**: 9 MAJOR (items 1–9), 11 MINOR (items 10–20), 4 LOW (items 21–24). All **24 enumerated** findings are addressed below. The 3 findings implied by the header count are not stated anywhere in the report and therefore cannot be actioned; flagged here rather than silently absorbed.

---

## MAJOR (9 enumerated)

| # | Finding | Disposition | Sites |
|---|---|---|---|
| 1 | 6–9d scope qualifier stripped | **FIXED.** Both source scope limits — *"for one gate type"* and *"city standup uncosted"* — now appear at every citation site, plus the **~2.5–4d shared-infrastructure vs ~3–5d per-gate verdict-path split** re-derived from the source's own bullet list (watcher+notifier 1–2d, last-mile 0.5–1d, cursor durability 1d = 2.5–4d shared; verdict capture 3–5d = per-gate). Split also stated explicitly at the *source* so citations are verbatim-equivalent. Added the multiplication note: extra gates multiply the verdict share, not the 6–9d total. 15–25d likewise re-qualified as a four-gate-sized floor. | `research-notification-watcher-layer.md` :172 (source); `research-cycle-orchestration-fit.md` :181, :191; `research-dec035-revisit-triggers.md` :49 |
| 2 | production-evidence Finding 2 caveat residue | **FIXED.** Heading re-titled *"landed on `main` 2026-07-23, in no tagged release"*; finding-wide availability caveat added at the intro with an explicit reading instruction (*read every "ships/shipped" below as "landed on `main`"*); the *"until four weeks ago … silently stranded"* claim rewritten — **the stranding has not ended in any release**; Bottom Line "recently-shipped" → "recently-*landed*"; Recommendation 1 split into gate-bead (available) vs notify order (not released); *"actual production support"* replaced and explicitly negated. | `research-production-evidence.md` :14, :75, :77, :86, :207, :212 |
| 3 | cycle-fit "decoration" paraphrase residue | **FIXED.** Author gloss replaced with notification-cost framing at all three sites; the defensible spec quote left intact per the finding's fairness scope. Open question #5 **answered and re-scoped** (the corpus had answered it): blocking suffices for *resolution* on a human gate, not for *notification*; residual question narrowed to a Momentum design choice. Also sharpened `gate-mechanics` :252 (*"survives only as decoration"* → *"survives only as text … carrying no machine-readable identity"*) — same paraphrase, caught by the sweep. | `research-cycle-orchestration-fit.md` :137, :173, :227; `research-gate-mechanics-handson.md` :252 |
| 4 | bd-ready dispatch precondition undisclosed (DOMAIN3-A-001) | **FIXED.** Scope condition added as a standing preamble at `hitl-alternative` §7 and at `human-verdict` §5 and §8's opening, with the §8 closing paragraph expanded and cross-linked in both directions. Condition stated in full at each site: a `bd` gate gates only work dispatched through `bd ready`; Momentum's Conductor dispatches from `index.json` + `depends_on` under dual-write; the prerequisite is moving dispatch onto `bd ready`, which is DEC-028's open go/no-go; satisfied by construction under full Gas City. | `research-hitl-alternative-patterns.md` §7 preamble; `research-human-verdict-patterns.md` §5, §8 intro, §8 close (:293) |
| 5 | Headline "two load-bearing gaps" vs body "three" | **FIXED.** Headline now says **three**, naming all: notification last mile, post-fan-out barrier, push/merge authority. Verified consistent against body (:41) and Verdict (:98). | `research-dec035-revisit-triggers.md` :10 |
| 6 | Barrier statement drops "declarative" | **FIXED.** Both sites now mirror `maturity` :224: *no reliable **declarative** expression*; `drain` + `check` loop named as **the only sanctioned construction**, with its three real limits — different authoring shape, unproven against a runtime-discovered story set, unverified failed-close semantics — and the §9c completion-assertion-bead prescription cited. | `research-dec035-revisit-triggers.md` :45, :98 |
| 7 | gate-mechanics EMPIRICAL headline overclaim | **FIXED.** Headline split: blocking + release remain *"reproduced end-to-end … two cities, two bd versions"*; the `bd close` refusal is separated out, scoped to the **timer** gate, marked gate-type-agnostic *by code path* and **[UNVERIFIED for `human` gates specifically]**. Propagated to the verbatim quote in dec035 and to two further sites the sweep found: the (c) fit-table row and the Confidence-and-limits list, which had bundled close-side enforcement into *"directly observed, twice, on two bd versions."* | `research-gate-mechanics-handson.md` :10, :188, :359, :395; `research-dec035-revisit-triggers.md` :37 |
| 8 | Verdict upgrades to "proven" against open items | **FIXED.** *"real and proven"* → **"documented and partly proven"**, separating what was reproduced (gate blocking, [EMPIRICAL]) from what is documented-but-unexercised (hour-long steps, durable multi-day parking), with `cycle-fit` §10 Q1–Q2 cited as still open. | `research-dec035-revisit-triggers.md` :98 |
| 9 | Direction inverted in incidence calculation | **FIXED, honestly and in the correct direction.** The iter2 claim that the smaller denominator makes scarcity *stronger* is retracted: 1/1,293 ≈ 0.077% is a **higher** incidence than 1/1,729 ≈ 0.058%, so the corrected denominator **marginally softens** the ratio. Conclusion recorded as **unaffected** at 1-in-1,293 — never as strengthened. | `research-production-evidence.md` :66 |

## MINOR (11 enumerated)

| # | Finding | Disposition |
|---|---|---|
| 10 | Wrong-row pointer | **FIXED.** *"the fan-out hazard in the row below"* → *"the fan-out hazard in this table's last row (conduct's per-story fan-out, #3451)"*; verified :177 is that row (`research-cycle-orchestration-fit.md` :173). |
| 11 | 760 open PRs arithmetically impossible | **FIXED by re-derivation, not transplant.** 1,011 (repo-endpoint, issues + PRs) − 575 (search-API `is:issue is:open`) = **≈436 open PRs**, labelled `[derived]`, with the 760 figure named as a retracted unsourced import. **718's query method annotated**: the same search-API basis applied to closed issues (`is:issue is:closed`, all-time, PRs excluded) — stated as the method the file's own like-for-like arithmetic requires (575 + 718 = 1,293), with an explicit note that the raw query string was not recorded at the time (`research-production-evidence.md` :185). |
| 12 | Three-vs-four bullets | **FIXED.** *"Three corroborating signals"* → **"Four"**; bullet count verified = 4 (`research-dec035-revisit-triggers.md` :67). |
| 13 | Backwards correction marker | **FIXED.** Marker reworded to the well-formed pattern — *"The pre-CRIT-004 'does NOT force DEC-028' framing **is retracted and is superseded by the text that follows**"* (`research-dec035-revisit-triggers.md` :49). |
| 14 | notify/renudge caveat unscoped in Risks | **FIXED.** *"Treat the nag loop as beta"* → *"**unshipped — not merely beta**: `main`/`edge` only, absent from v1.4.0 and v1.4.1 (see §4)"*, with the two adoption routes named (run `edge`, or vendor the order files) (`research-hitl-alternative-patterns.md` §8). |
| 15 | bd-version narrative inconsistent | **FIXED by reconciliation in Probe 5, stated as unsettled rather than papered over.** The gascity-`main` `deps.env` comment calls **v1.1.2** "the newest published release" and says it predates `beads#5008` (2026-07-24) — irreconcilable with beads **v1.2.2, published 2026-08-15 and exercised first-hand by this corpus**, which postdates #5008. Two readings named (comment stale vs. scoped to the v1.1.x line); the settling command (`bd 1.2.2 update --help`) named as never run. Consequence propagated: *"CAS unavailable in **any** published release"* downgraded to **[UNVERIFIED for v1.2.2]**, verified only for v1.0.4 and v1.1.x — including in the DEC-028 re-scoring row, whose direction is now qualified as sound for the bd Momentum runs but unsettled as a universal claim (`research-verification-probes.md` Probe 5 :238, :282; `research-beads-coupling-dec028.md` :163, :170, :198). |
| 16 | Finding-IDs undefined in scope | **FIXED.** New *"Correction markers and finding IDs"* subsection in `scope.md`'s Evidence-notation section: marker form, what a marker means (the text it introduces is the **corrected** claim), the conclusion-first/history-trailing reading order adopted at iter3, the `<LENS><ITER>-<ROLE>-<NNN>` ID grammar with worked examples, and where each ID family resolves — **including that `MERGED-*` IDs are iteration-2 cross-lens merge identifiers living only in `validation/avfl-consolidated-iter2.md`**, which is why `MERGED-002` cannot be found in any per-lens findings file. |
| 17 | Marker density misleading (COHERENCE3-A-010) | **FIXED — conclusion-first restructure at all four named passages, plus three more found by sweep.** Named: `beads-coupling` :12 (Bottom Line) and §7 :180 (350-word re-derivation compressed to a trailing *Correction history* note); `gate-mechanics` :188 (**surviving claim now leads**, evidence scope second, archaeology trailing — this closes the unclosed correction bracket that made the claim read as retracted) and :360 (bolded takeaway re-scoped so it no longer reads broader than the scoping beneath it: `bd gate create` is decisive for timer/gh gates, buys notifiability-not-auto-resolution for human gates, and buys nothing released today). Lighter touch applied where else a marker preceded its conclusion: `beads-coupling` :70, :167 and `gate-mechanics` :64. |
| 18 | Merge-velocity mixed population | **FIXED.** *"Merge velocity vastly outruns issue closure"* annotated as a **mixed-population** comparison (2,402 PRs merged since 2026-05-01 vs 380 issues closed from the May cohort vs 575 open all-time), with the like-for-like comparison stated: **575 open vs 718 closed, both all-time, both issue-only** — on which closed exceeds open by 143 (`research-maturity-open-bugs.md` :38). |
| 19 | Verdict vocabularies unlabeled | **FIXED at both ends with reciprocal cross-references.** `notification-watcher` gap 6 labelled the **gate-level** vocabulary (Approve / Modify / Re-run AVFL — disposition of the whole gate); `human-verdict` §8 labelled the **per-fork** vocabulary (`verdict.fork.<slug>=approve|modify|remove`). Both state that a write-back schema needs **both key families**, and that "modify" means different things at the two levels. |
| 20 | gemini Reliability Notice missing row | **FIXED.** Row added for the `pr-pipeline` *"hard, non-negotiable pre-push gate"* claim, refuted from `research-production-evidence.md` :53–:62 (prose in a `claude` step, agent-judgment early exit, zero `[steps.gate]` across 315 pack TOMLs) — with the reason it matters recorded: it lands on the **push/merge-authority axis**, the third open gap, and taking it at face value would suggest Gas City already supplies a push gate no pack implements. |

## LOW (4 enumerated)

| # | Finding | Disposition |
|---|---|---|
| 21 | Citation precision in §9c | **FIXED.** Rejection-indistinguishability re-cited to `human-verdict` **§2** (:112) **and §6** (:234), with both quoted inline; the fail-closed attempt-scoped guard re-cited from §2 to **§7** (:279), quoted inline. Verified against the source before editing (`research-cycle-orchestration-fit.md` §9c). |
| 22 | `gc start` "specifically" contradiction | **FIXED.** *"specifically"* dropped; the sentence now states that **`gc init` enforces the binaries up front precisely because `gc start` will need them**, removing the contradiction with the same paragraph's `gc init` dependency-gate statement (`research-beads-coupling-dec028.md` :12). |
| 23 | CRIT-005 grep structurally cannot match | **FIXED at the source.** `fix-log-iter2.md`'s sweep block now carries a **RETRACTED AS EVIDENCE** annotation: the literal-space pattern can never match backticked `` `claude -p` ``, so "0 hits" proved nothing (the claim itself was re-verified clean by hand and stands). The backtick-tolerant replacement is recorded there and was used for every sweep in this pass. |
| 24 | Frontmatter unmarked premise | **FIXED.** `cycle-fit` :4 `sub_question` now carries the same marker `scope.md`'s two copies got: *"(premise refuted — CRIT-005; see §1 of this file. Original wording kept as historical record of what was asked.)"* |

**Deferred: none. All 24 enumerated findings fixed.**

---

## Sweep confirmation (backtick-tolerant; markdown emphasis stripped before matching)

Sweep harness used throughout:

```bash
strip() { for f in raw/*.md scope.md; do
            sed 's/[`*_]//g' "$f" | awk -v F="$f" '{printf "%s:%d: %s\n", F, NR, $0}'
          done; }
```

| # | Sweep | Result |
|---|---|---|
| 1 | `6–9\|6-9 day` — scope clause present? | **4 numeric citation sites, 4 carry "for one gate type", 0 without.** City-standup exclusion verified present at all 4. |
| 2 | `decorat\|conveys nothing\|costs nothing` | **Clean.** Remaining hits: the cycle-fit retraction marker naming the old reading; `gc formula cook: decorate formulas v2` (literal CLI output); and three `costs nothing` uses all immediately paired with the notification correction (human-verdict :15, :192; maturity :135). No unpaired decision-bearing hit. |
| 3 | `shipped 2026-07-23` | **0 uncaveated hits.** Remaining date references are the PR-metadata citations (#4553, 2026-07-23), which are accurate. |
| 4 | `two load-bearing gaps` / `two gaps` / `two holes` | **0 hits.** (Only `maturity` :69's unrelated v1-vs-v2 spec gaps.) |
| 5 | `proven` | **Clean.** Surviving uses are all supported: gate primitive block/resolve (empirically proven), the pack-rewrite path ("five methodologies have walked it"), and #4587's "reproduction-proven" fix. The out-of-session overclaim is gone. |
| 6 | `beta` | **Clean** — but this self-report was inaccurate as written. **[Annotated at iter4 — ACCURACY4-A-008.]** There are three surviving hits, not one: the literal cursor example `alpha:4,beta:9`, plus **two legitimate hits on `research-hitl-alternative-patterns.md`:247** — the corrected claim itself (*"Treat the nag loop as **unshipped — not merely beta**"*) and its own correction marker, which reads in part: "beta" implied a released-but-immature path that does not exist. Both are fix text, so the sweep's *verdict* (clean — no uncaveated `beta` claim survives) stands; only its hit-count narration was wrong. Log artifact, no corpus change. |
| 7 | `production support` / `production-grade` | **Clean.** Both hits are the caveated Bottom Line and the explicit negation at :212. |
| 8 | `760` / `1,729` | **Clean.** Surviving: issue `#1760` (unrelated), and both figures quoted inside their own retractions. |
| 9 | `roughly 760 open PRs` | **0 hits.** |
| 10 | `Three corroborating` | **0 hits**; bullet count re-verified = 4. |
| 11 | `hazard in the row below` | **0 hits**; pointer now names the table's last row, verified against :177. |
| 12 | `claude -p` as subprocess/exec/runner (backtick-tolerant) | **5 hits, all correct**: premise-refutation text or the corrected work-step shape. This is the sweep that iter2's pattern could not perform. |
| 13 | `bd close` refusal claim sites | **5 hits, all scoped** to timer-gate evidence with `[UNVERIFIED for human gates specifically]`. |
| 14 | Marker-led paragraphs (`^\*\*\[Corrected\|Re-derived\|Resolved\|…`) | **0 remaining.** Every such passage now leads with its conclusion. |

## Cross-file consistency re-checks

- **dec035 gap count:** headline :10 = three, body :41 = three, Verdict :98 = "three holes and a cost". Consistent.
- **Barrier language:** `maturity` :224 (source), `dec035` :45 and :98, `cycle-fit` §9c all now say *"no reliable **declarative** expression"* + *"`drain` + `check` is the only sanctioned construction"*. Consistent.
- **bd-close scoping:** `gate-mechanics` :10 / :188 / :359 / :395 and `dec035` :37 all carry the timer-gate scope and the `[UNVERIFIED for human gates]` tag. Consistent.
- **Notify/renudge availability caveat:** `production-evidence` :14 / :77 / :207 / :212, `hitl-alternative` :136 / :198 / :224 / §8, `notification-watcher` release-gap section, `dec035` gap 1. Consistent — no site now presents the orders as released.
- **Verdict vocabularies:** gate-level (`notification-watcher` gap 6) and per-fork (`human-verdict` §8) each name and link the other.
- **575 / 718 / 1,293:** consistent across `production-evidence` :66, :185 and `maturity` :38, with the query method now stated for both 575 and 718 and the mixed-population comparison annotated at `maturity` :38.
