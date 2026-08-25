# AVFL Fix Log — Iteration 4 (final pass)

**Date:** 2026-08-24
**Corpus:** `docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/`
**Input:** `validation/findings-iter4/` (8 lens reports), deduped to 4 majors / 4 minors / 3 lows
**Policy:** developer-directed close after this pass — no fifth validation round. Everything below ships to synthesis.

**Result: 11 of 11 items resolved.** Ten were fixed in the corpus. One (M1) was investigated, proven a **false positive**, and the correct text was preserved with the disproof recorded inline so it cannot be re-flagged downstream.

Every quotation introduced or preserved in this pass was verified character-for-character against its cited location by string containment, not by recall. Every arithmetic claim was re-derived from its components.

---

## MAJORS

### M1 — ACCURACY4-A-001 · `research-cycle-orchestration-fit.md`:219 · **FALSE POSITIVE — claim preserved, disproof recorded**

**The finding alleged:** the italicized quotation attributed to `research-human-verdict-patterns.md` §7 is fabricated — "a fusion of §7's `|tostring` finding and §2:99's `2>/dev/null` warning."

**What I actually found:** the quotation is genuine, continuous, and correctly attributed. The quoted string appears verbatim as a single continuous sentence at `research-human-verdict-patterns.md`:281, which is inside §7 (§7 spans :249–:283). Verified by exact substring containment against the source file, not by reading:

```
QUOTE: 'any Momentum-authored check or gate script must coerce with `|tostring`
        before comparing, and must never rely on `2>/dev/null` to swallow a failed read'
exact match in human-verdict (bold markers stripped)? True  -> line 281
```

The only difference from the source is that §7's internal `**…**` emphasis on the first clause is not reproduced inside the quotation — a normal elision of markup, not a fabrication. Both halves of the sentence — the `|tostring` coercion *and* the `2>/dev/null` prohibition — are §7's own words in one sentence.

**Why the finding misfired:** the `2>/dev/null` hazard is *also* documented independently at §2's read side (:99), where the pack scripts' own comments record it. That genuine overlap made the sentence look assembled from two sections when it is not.

**Why I did not apply either offered remedy.** Both options (a: drop the quote marks and paraphrase; b: re-quote :99 and cite it to §2) are premised on the quotation being fabricated. Applying them would have *degraded* an accurate verbatim citation — option (b) in particular would have moved the citation onto §2, which is where the previous iteration's citation already was and which `ACCURACY3-A-005` correctly moved it *off* of, since §2 does not carry the `|tostring` prescription. The iteration-3 fix was right.

**What changed:** the quotation and the §7 citation stand unaltered. The parenthetical correction note was extended to record the re-verification, so a downstream reader or a future validator does not re-open it.

- **Before:** `(Citation precision fixed during AVFL fix pass — ACCURACY3-A-005; §2 was cited previously.)`
- **After:** `(Citation precision fixed during AVFL fix pass — ACCURACY3-A-005; §2 was cited previously. **Re-verified verbatim at iter4 against ACCURACY4-A-001, which alleged this quotation was a fabricated fusion of two sections: it is not.** The quoted sentence is a single continuous sentence at `research-human-verdict-patterns.md`:281, inside §7, carrying both the `|tostring` clause and the `2>/dev/null` clause together; the only difference from the source is that §7's internal `**…**` emphasis on the first clause is not reproduced here. §7 is therefore the correct and sufficient citation. The underlying `2>/dev/null` hazard is *separately* documented at §2's read side, :99, where the pack scripts' own comments record it — which is the overlap that made the quote look fused.)`

**Note for the record:** the brief that commissioned this pass stated as established fact that the previous pass "introduced a fabricated quotation." It did not. The prior pass's edit was correct; the iteration-4 accuracy adversary produced a confident false positive on a negative claim.

---

### M2 — COHERENCE4-A-001 (revives dropped iter-1 COHERENCE-A-005) · `research-hitl-alternative-patterns.md` :175, :204, :212, :235 · **FIXED**

**The contradiction:** the plan-gate (b) recommendation prescribed a **check loop** as the human gate, while `research-human-verdict-patterns.md`:138 states in bold that *"A check loop is the wrong primitive for a human gate"* and names `[steps.gate]` as the right one — a contradiction that survived from iteration 1, was dropped at consolidation, and was never fixed.

**Adjudication applied (per direction, and corroborated corpus-wide):** human-verdict's prescription is adopted. The **gate blocks the human decision**; a check loop is the **agent-side review that precedes it** (the two-step `review-loop` → `human-gate` pattern at human-verdict:294). A check loop cannot wait for a human: it polls, re-spawns the agent work on each failed check, and closes the step **failed** on exhaustion (human-verdict §1 :41/:51, §3 :136).

The corpus was already overwhelmingly on this side — the fixed file's **own Bottom Line** (:13) calls `bd gate --type=human` "the load-bearing primitive", the (b) concrete shape at :212 already used `bd gate create`, and the Gemini fact-check notice refutes check-loop-as-HITL twice (:24, :25). The three headline sites were the outliers.

**:175 — before:**
> …including metadata a human wrote via `gc bd update --set-metadata` or `gc beads metadata-cas`. **That is the general-purpose v2 human gate with a payload.**

**:175 — after:**
> …including metadata a human wrote via `gc bd update --set-metadata` or `gc beads metadata-cas`. **That makes the check loop a general-purpose carrier for a human-written *payload* — but not the human *gate*.** A check loop does not wait. It is a one-shot evaluation that, on a missing verdict, re-spawns the agent work and tries again, and on exhaustion "closes the step as failed" — unconditionally, with no encoding for "the human said no" (`research-human-verdict-patterns.md` §1, §3). The blocking primitive for a human decision is `[steps.gate]` / `bd gate create --type=human`, which blocks indefinitely and resolves only on explicit command (§5). The check loop's real place is the *agent-side* review iteration that runs **before** the human is asked — the two-step `review-loop` (check) → `human-gate` (gate) pattern §8 prescribes, which is also required mechanically, since `check` cannot be combined with `gate` on one step (§1). **[Corrected during AVFL fix pass — COHERENCE4-A-001; …]**

**:204 — before:**
> **Recommended: v2 check loop + verdict-in-metadata + artifact file. Gate bead only as the parking brake.**

**:204 — after:**
> **Recommended: `bd gate create --type=human` as the blocking primitive, carrying verdict-in-metadata + an artifact file as the per-fork payload. An agent-side check loop, if used at all, runs *before* the gate — never as the gate.** **[Corrected during AVFL fix pass — COHERENCE4-A-001; …the concrete shape below already used `bd gate create`; the headline now matches it.]**

**:235 summary-table row — before:**
> | Plan gate (per-fork verdicts) | verdict-in-metadata + artifact file; **gate bead as brake**; Momentum-side check script enforces anti-rubber-stamp | … |

**:235 — after:**
> | Plan gate (per-fork verdicts) | **`bd gate --type=human` blocks the decision**; verdict-in-metadata + artifact file carry the payload; Momentum-side script enforces anti-rubber-stamp at resolve time | metadata enum + `.md` verdicts file | …; a **check loop cannot be the gate** — it polls, re-spawns the work, and closes failed on exhaustion (`research-human-verdict-patterns.md` §3) |

**:212 (additional, not in the brief but required for coherence):** the concrete shape's closing sentence described a `[steps.check]` script on the following phase that "reads the status and either proceeds or re-spawns planning" — readable, after the headline change, as the check-loop-as-waiter this fix rules out. Added an explicit distinction: *"That check is not what waits"* — the gate bead is; the following phase is blocked behind it, so the check only ever runs against an already-resolved gate. Wiring it the other way is the failure mode §3 rules out. Table row verified as a well-formed 4-column row (5 pipes, balanced emphasis).

---

### M3 — COHERENCE4-A-002 · `research-production-evidence.md`:220 · **FIXED**

**The defect:** the medium-confidence hedge credited the notify/renudge orders to *"the shipping team's revealed preference … mildly pro-HITL"* — inverting the same file's own evidence at :14, :79 and :212 (community contributor Chris Sauer, 11 commits total; core team has left the orders unreleased for four weeks, absent from v1.4.0 and v1.4.1).

- **Before:** "**Medium confidence:** the maintainer-direction reading. Yegge's essay is unambiguous but he is a 5-commit contributor; the shipping team's revealed preference (contributing the notify orders at all) is mildly pro-HITL. Marketing copy and engineering reality diverge."
- **After:** "**Medium-high confidence:** … The counter-signal usually offered against the reading — that the notify/renudge orders exist at all — does **not** come from the shipping team: PR #4553 was authored by Chris Sauer, a community contributor with 11 commits total to the repository (Finding 2), and the core team has left both orders unreleased for four weeks and counting… The core team's revealed preference is therefore mildly *anti*-HITL, or at best indifferent; the one pro-HITL signal in the evidence is a drive-by contributor's, not the maintainers'. That points the same direction as Yegge's essay (Finding 4) and as the tag-protection-ruleset remediation (Finding 5), so the reading is corroborated rather than contested — the residual uncertainty is about reading intent from artifacts at all, not about a countervailing signal. …"

**Confidence re-rated, as directed:** medium → **medium-high**. The rating was medium partly *because* of a counter-signal that does not exist. Removing it leaves the reading corroborated by three independent artifacts (Findings 2, 4, 5) rather than contested; what keeps it off "high" is Yegge's thin commit standing and the general difficulty of reading intent from artifacts — both now stated explicitly.

**Downstream check:** `research-dec035-revisit-triggers.md`:49 consumes this reading ("Maintainer direction points away from HITL") — it is *strengthened*, not contradicted, by the correction. No propagation needed. Corpus-wide grep for `revealed preference|shipping team` returns only the corrected line.

Finding numbers in the new text were verified against the file's own headings (Finding 2 = the ad-hoc gate-bead path, :75; Finding 4 = maintainer direction, :119; Finding 5 = GitHub ruleset, :136).

---

### M4 — STRUCTURAL4-A-001 / COHERENCE4-A-003 / ACCURACY4-A-003 · `research-beads-coupling-dec028.md`:178 + `research-verification-probes.md`:284 · **FIXED**

The retracted CAS universal survived in two unscoped leads while both bodies carried the correct `[UNVERIFIED for v1.2.2]` scoping. Decision-bearing: it feeds the DEC-028 D1 re-score.

- **beads-coupling:178 lead — before:** "**Compare-and-swap writes are not yet available in any published bd.**"
- **beads-coupling:178 lead — after:** "**Compare-and-swap writes are unavailable in the bd Momentum runs (v1.0.4) and across the v1.1.x line — [UNVERIFIED for v1.2.2].**"
- Correction history appended trailing (per the iteration-3-onward conclusion-first convention), recording that iter3 scoped the body only and that the lead was brought into line at iter4. Added the internal oddity: a release cut after `beads#5008` would, on the upstream comment's own logic, be expected to carry the flags — which is exactly why the universal cannot stand.

- **probes:284 — before:** "…driven by an upstream beads capability gap — no published beads release past v1.0.4/pre-#5008 has the CAS precondition flags gascity's contract tests require on the embedded path, and v1.1.2 doesn't have them either since it branched off v1.1.0 before the fix)"
- **probes:284 — after:** reframed as *what the inline comment says* rather than as an assertion of fact, with the same scoping: absent from v1.0.4 and the v1.1.x line including v1.1.2; the comment's generalization to "no published release" rests on a "newest published = v1.1.2" premise that v1.2.2 (2026-08-15) breaks; **[UNVERIFIED for v1.2.2]**, only the v1.0.4/v1.1.x scoping supported.

---

## MINORS

### m5 — STRUCTURAL4-A-002 + ACCURACY4-A-006 · `research-gate-mechanics-handson.md`:181, :188 · **FIXED**

Both bd-close claim sentences now carry the timer-gate scope **inside** the sentence, matching the other four sites' pattern rather than deferring to the scope paragraph at :190.

- **:181 — before:** "**Bonus finding — the gate also blocks *closure*, not just readiness.**"
- **:181 — after:** "**Bonus finding — the gate also blocks *closure*, not just readiness** (reproduced against a **timer** gate; **[UNVERIFIED for `human` gates specifically]** — see the scope note below)."
- **:188 — before:** "**The claim stands: an open gate refuses `bd close` on the gated step, which is stronger than a readiness filter.**"
- **:188 — after:** "**The claim stands: an open gate refuses `bd close` on the gated step, which is stronger than a readiness filter** — reproduced against a **timer** gate, **[UNVERIFIED for `human` gates specifically]**; see the scope paragraph immediately below."

The scope clause was placed *outside* the bold span on :188 deliberately: nesting `**` inside `**` breaks markdown rendering. Verified balanced.

### m6 — DOMAIN4-A-001 + COHERENCE4-A-004 · init-vs-start dependency attribution · **FIXED (5 sites)**

Standardized corpus-wide on **`gc init` as the single enforcement point**: under the bd provider it demands **tmux + dolt + flock**, all three, up front; under `GC_BEADS=file` it demands **tmux only**. Evidence: the live `gc init --no-start` transcript at gate-mechanics:52–56 (which refuses on all three) and `research-verification-probes.md` Probe 1.

| Site | Was | Now |
|---|---|---|
| `gate-mechanics`:61 | "**`gc start` (the live orchestrator) requires tmux, an external `dolt` binary, and `flock`.**" | "**`gc init` is the enforcement point, and under the bd provider it demands tmux, an external `dolt` binary, and `flock` — all three, up front.**" + the `GC_BEADS=file` tmux-only contrast |
| `gate-mechanics`:366 | "Only `gc start` … adds tmux + an external `dolt` binary + `flock`." | "Standing up a `gc` **city** is what adds tmux + an external `dolt` binary + `flock`, and `gc init` — not `gc start` — is where all three are enforced" |
| `beads-coupling`:14 | "`gc init`'s dependency gate demands `dolt` and `flock` … and `gc start` adds `tmux`" (self-contradictory two clauses apart) | all three at `gc init`, refused in the live transcript even under `--no-start`; `GC_BEADS=file` → tmux alone |
| `beads-coupling`:190 | "`gc init`/`gc start` … gate for `dolt` and `flock`" | "additionally hits gc's own dependency gate, enforced at `gc init`, for `tmux`, `dolt`, and `flock`" |
| `beads-coupling`:208 | "`gc init`/`gc start`'s own dependency gate still requires `dolt` and `flock`" | "`gc init`'s own dependency gate still requires `tmux`, `dolt`, and `flock`" |

The true and separately-valuable point — **the graph layer needs none of them** (bd's embedded Dolt suffices for direct `bd` operations) — is preserved verbatim at both gate-mechanics:62 and :366. `beads-coupling`:16's correction-history note was extended to record that a residual split survived iter3's ACCURACY3-A-006 fix and was closed here. Corpus-wide grep for `gc start` + dependency verbs confirms no unaligned site remains.

### m7 — ACCURACY4-A-002 · `scope.md`:50 · **FIXED**

- **Before:** "…they do not appear in any per-lens findings file, which is why `MERGED-002` cannot be found by grepping `validation/findings*/`."
- **After:** the defined-vs-referenced distinction, stated as such: `MERGED-*` IDs are **defined** in exactly one place (`avfl-consolidated-iter2.md`) but **referenced** in several; a grep of `validation/findings*/` returns citations of the ID but never its definition.

Count re-derived, not inherited: **seven** files under `validation/findings*/` reference `MERGED-002` — five in `findings-iter3/`, two in `findings-iter4/`. (The finding said six; that was correct at the time it was written, before the second iter-4 file landed. The corrected text states seven with the split, as verified.)

### m8 — ACCURACY4-A-004 · `research-maturity-open-bugs.md`:38 · **FIXED**

Propagated `research-production-evidence.md`:185's query-method hedge onto the "both all-time, both issue-only" assertion: the raw query string for the **718** was not recorded; the `is:issue is:closed` basis is stated as the method the like-for-like arithmetic *requires* (it is what makes 575 + 718 = 1,293 the issue-only total), **not** as an observed re-run. The line now reads "verified for 575 and inferred-from-arithmetic for 718." Arithmetic re-derived: 575 + 718 = 1,293 ✓; 718 − 575 = 143 ✓.

---

## LOWS

### l9 — ACCURACY4-A-005 / DOMAIN4-A-002 · `research-notification-watcher-layer.md`:172 · **FIXED**

Components re-derived from :167–:170: (1–2) + (0.5–1) + (3–5) + (1) = **5.5–9**, against a stated total of "≈ 6–9".

- **Before:** "**Total ≈ 6–9 days** of glue **for one gate type**…"
- **After:** "**Total ≈ 5.5–9 days** of glue **for one gate type**… **[Arithmetic reconciled at iter4 — ACCURACY4-A-005 / DOMAIN4-A-002.]** The four components above sum to exactly **5.5–9** (1–2 + 0.5–1 + 3–5 + 1); the headline is rounded to **6–9** at the citation sites elsewhere in this corpus, all of which carry a "≈". The half-day gap is rounding on the low end, not a missing component — nothing here derives a hard 6.0."

The split figures were independently re-derived and confirmed self-consistent: shared infrastructure 1 + 0.5 + 1 = **2.5** to 2 + 1 + 1 = **4** ✓; per-gate verdict path **3–5** ✓; 2.5 + 3 = 5.5 and 4 + 5 = 9 ✓.

**Three citation sites checked, none touched** — per direction, they were to be edited only if their wording claims arithmetic derivation:
- `cycle-fit`:181 — "~6–9 days", with every component also tilde-hedged (`~2.5–4d`, `~3–5d`, `~1–2d`, `~0.5–1d`, `~1d`). Hedged. **Left.**
- `cycle-fit`:191 — "~6–9 day gate-glue estimate", "~2.5–4d", "~3–5d". Hedged. **Left.**
- `dec035`:49 — "**6–9 day** gate-glue estimate", with "roughly **2.5–4 days**" / "roughly **3–5 days**" and tilde-hedged sub-components. Labeled an *estimate* and hedged with "roughly"; claims no derivation. **Left.**

### l10 — ACCURACY4-A-007 · `research-beads-coupling-dec028.md`:70 · **FIXED**

- **Before:** "**FileStore metadata is durable, but unwritable — and it is the unwritability, not the durability, that decides Momentum's gate use case.**"
- **After:** "**FileStore metadata is durable, but *externally unwritable in gc 1.4.1* — no public CLI write verb exists; the engine writes its own keys — and it is that unwritability, not the durability, that decides Momentum's gate use case.**" plus a trailing scope marker noting the bare word overstated what Probe 2 supports.

### l11 — ACCURACY4-A-008 · `validation/fix-log-iter3.md` sweep #6 · **ANNOTATED**

The sweep's self-report claimed the only surviving `beta` hit was the literal cursor example `alpha:4,beta:9`. There are three: that example plus **two legitimate fix-text hits on `research-hitl-alternative-patterns.md`:247** — the corrected claim itself ("Treat the nag loop as **unshipped — not merely beta**") and its own correction marker. Both are fix text, so the sweep's *verdict* (clean — no uncaveated `beta` claim survives) stands; only its hit-count narration was wrong. Annotated in place as a log artifact; **no corpus change**.

---

## Verification performed on this pass

| Check | Result |
|---|---|
| Every quotation introduced or preserved, verified by exact substring containment against its cited file | **6/6 pass** (M1 quote vs human-verdict:281; two l11 quotes vs hitl-alternative:247; M2's ":138 refutation", ":13 load-bearing primitive", and "§1 closes the step as failed") |
| Quote character fidelity | One alteration caught and reverted: an l11 quotation had `"beta"` rewritten as `'beta'` to avoid nested quote marks. Restored to the source's exact characters by dropping the outer quote wrapper instead. |
| Markdown balance (`**`, backticks, brackets) on all 24 edited lines | **24/24 clean.** Whole-file scans flag only pre-existing code-fence false positives, none on edited lines. |
| Table structure at `hitl-alternative`:235 | 5 pipes / 4 columns, balanced emphasis ✓ |
| Arithmetic re-derived from components (not inherited) | glue totals 5.5–9 and the 2.5–4 / 3–5 split ✓; 575 + 718 = 1,293 and the 143 delta ✓; MERGED-002 reference count = 7 ✓ |
| Nested-bold rendering hazard | Caught and fixed at gate-mechanics:188 before commit |
| Retracted-text quotes inside new correction markers, verified against `git show HEAD:` originals | **5/5 exact.** Two were caught substituting a comma for the source's terminal period (American quote-punctuation style) and were restructured to preserve the source characters. |
| Propagation sweeps | `revealed preference\|shipping team` → 1 hit, the corrected line ✓ · `parking brake\|general-purpose v2 human gate` → 2 hits, **both inside correction markers quoting the retracted text**, per `scope.md`:47's documented convention; 0 live claims ✓ · `gc start` + dependency verbs → no unaligned site ✓ · `6–9` citation sites → 3, all hedged, all left per direction ✓ |
