# AVFL Consolidated Validation Report — Iteration 2

**Date:** 2026-08-24 | **Reviewers:** 8 (4 lenses × Enumerator + Adversary) | **Corpus:** 10 research files + scope.md

---

## Score & Grade

| Metric | Value |
|---|---|
| **Final Score** | **-43** (start 100; -8 per major, -3 per minor, -1 per low) |
| **Grade** | **FAILING** (<50 threshold) |
| **Major Findings** | 14 |
| **Minor Findings** | 9 |
| **Low Findings** | 4 |
| **Total Findings** | 27 unique (pre-dedup: 35) |
| **Deduplication Yield** | 8 findings merged across lenses (6 majors, 2 minors) |
| **Confidence Distribution** | HIGH (7): 7 findings with 2+ reviewers; MEDIUM (20): 1-reviewer findings |

---

## Critical Note: Conflict Adjudication

**DOMAIN2-E-002 vs. 4+ validators:** Domain-enum claims DEC-035 cites the *corrected* beads-coupling framing. Structural-adv, Coherence-adv, Accuracy-enum, and Accuracy-adv quote DEC-035:47's *pre-CRIT-004 text* with file mtime evidence (14:29 write, 15:37 correction, file never re-reconciled). **Resolution:** Adjudicate **against domain-enum's note**. Finding MERGED-001 (stale DEC-035 citation) stands.

---

## Consolidated Findings

### MERGED-001 | CRITICAL PRIORITY | HIGH Confidence (5 reviewers)
**Severity:** Major | **Lenses:** Accuracy (2), Coherence (1), Structural (1), Domain (1)  
**IDs:** ACCURACY2-A-004, ACCURACY2-E-001, STRUCTURAL2-A-001, COHERENCE2-A-001, DOMAIN2-A-001

**Title:** DEC-035 stale pre-CRIT-004 consolation on DEC-028 coupling  
**Location:** `research-dec035-revisit-triggers.md:47, :121` vs. `research-beads-coupling-dec028.md` corrected Bottom Line (§7, :182–200)

**Description:**  
DEC-035 file (written 14:29 on 2026-08-24, before CRIT-004 correction) cites beads-coupling's OLD Bottom Line: *"one consolation: does NOT force DEC-028 — GC_BEADS=file is alive."* Post-CRIT-004 probes (15:29–15:37), beads-coupling's Bottom Line changed to *"partial decoupling, not clean — Momentum's city-store gate primitives require bd/Dolt backing; GC_BEADS=file real but not the shape the four HITL points need."* DEC-035 was never re-reconciled (fix log confirms; file timestamp unchanged after 15:37). The file now cites a corrected peer against a superseded position, contradicting the corpus's own CRIT-004 verdict.

**Evidence:**  
- `research-dec035-revisit-triggers.md:47`: "one consolation: does NOT force DEC-028 — GC_BEADS=file is alive"
- `research-beads-coupling-dec028.md:182–200` (Bottom Line, CRIT-004 correction): "partial decoupling" framing; §7 probes confirm bd/Dolt requirement for gate primitives
- Mtime delta: DEC-035 14:29, CRIT-004 correction 15:37, no reconciliation

**Suggestion:**  
Replace lines 47 and 121 with corrected framing: *"DEC-028 adoption pulls on Dolt-backed city stores for gate primitives — GC_BEADS=file configurations cannot host Momentum's bd gate create operations. See beads-coupling §7 for the cost-benefit re-derivation."*

**Propagation Impact:** Alters the "NOT-FIRED" verdict in DEC-035's Verdict block (strengthens case against adoption now); also affects coherence of HITL-alternative recommendations that reference it.

---

### MERGED-002 | CRITICAL PRIORITY | HIGH Confidence (2 reviewers, cross-lens)
**Severity:** Major | **Lenses:** Coherence, Domain  
**IDs:** COHERENCE2-A-002, DOMAIN2-A-002

**Title:** Results gate (d) split recommendation — contradiction across files  
**Location:** `research-gate-mechanics-handson.md:356`, `research-maturity-open-bugs.md:222` vs. `research-hitl-alternative-patterns.md:220–224`, `research-human-verdict-patterns.md:224, :287`

**Description:**  
Gate-mechanics and maturity-open-bugs correctly conclude gate (d) is *"Blocked — needs barrier"* after AVFL corrections. However, hitl-alternative and human-verdict files still recommend deploying gate (d) as a *"clean fit"* without barrier caveat. This is the corpus's central deliverable returning contradictory answers on the highest-stakes gate (the Momentum results gate). Workaround (#3451) is unavailable to Momentum (runtime-discovered phase children cannot enumerate static `needs`).

**Evidence:**  
- `gate-mechanics:356`: Blocked verdict (corrected)
- `maturity-open-bugs:222`: Blocked verdict (corrected)
- `hitl-alternative:220–224`: Recommends (d) as clean; omits barrier note
- `human-verdict:224, :287`: Recommends (d); no caveat
- `research-maturity-open-bugs.md` "Momentum impact" section: "gates are fine; barriers are not"

**Suggestion:**  
Add caveat to hitl-alternative §7(c) and human-verdict Recommendation table: *"(d) requires drain+check barrier; no declarative gate-only construct proven reliable (see maturity-open-bugs §X)."*

**Propagation Impact:** Primary decision artifact delivers contradictory guidance; fixer must search and harmonize all (d) discussion.

---

### MERGED-003 | CRITICAL PRIORITY | HIGH Confidence (2+ reviewers)
**Severity:** Major | **Lenses:** Coherence (2), Domain (1)  
**IDs:** COHERENCE2-A-003, COHERENCE2-E-001 (partial DOMAIN2-A-004)

**Title:** Refuted claude-p subprocess premise survives in hitl-alternative after CRIT-005  
**Location:** `research-hitl-alternative-patterns.md:138` (corrected) vs. `:150, :218` (not corrected)

**Description:**  
Line 138 correctly applies CRIT-005 correction: *"work step claimed inside a session"* replaces the refuted *"claude -p subprocess"* model. Lines 150 and 218 still reason from the struck framing:
- :150: *"a `claude -p` phase step is structurally `headless`"*
- :218: *"wasteful and fragile for a `claude -p` runner"*

This contradicts cycle-orchestration-fit.md (§1, :10, :50, :175), which correctly uses the corrected framing throughout.

**Evidence:**  
- Line 138: "[Corrected …] work step claimed inside a session"
- Line 150: "`claude -p` phase step is structurally `headless`"
- Line 218: "wasteful and fragile for a `claude -p` runner"
- `cycle-orchestration-fit.md:10, :50, :175` all use corrected framing (work steps, not subprocesses)

**Suggestion:**  
Apply CRIT-005 framing at :150 and :218. Example: *"work steps claimed inside the session are structurally…"*

---

### MERGED-004 | HIGH Confidence (2 reviewers)
**Severity:** Major | **Lenses:** Coherence, Structural  
**IDs:** COHERENCE2-A-006, STRUCTURAL2-A-002

**Title:** Beads-coupling §3 and §5 prescribe struck config; §7 contradicts  
**Location:** `research-beads-coupling-dec028.md:96` (§3), `:139` (§5) vs. `:182–200` (§7, corrected Bottom Line)

**Description:**  
§3 claims *"fully Dolt-free city is expressible."* §5 prescribes *"low-risk topology = GC_BEADS=file city"* with no gate caveat. Both carry no CRIT-004 fix markers. However, §7 and the corrected Bottom Line (post-probes) state gate primitives require Dolt backing — the config §3/§5 prescribe cannot host bd gate create. **Internal contradiction within the same file.**

**Evidence:**  
- §3:96: "fully Dolt-free city is expressible"
- §5:139: "low-risk topology = GC_BEADS=file city"
- §7:182–200 (corrected): "partial decoupling … city store must be bd/Dolt-backed for gate primitives"
- Probe evidence cited in §7 (Probe 2, Probe 4)

**Suggestion:**  
Caveat §3/§5: *"Dolt-free city is expressible for non-gated phases. Phases requiring bd gate create must use Dolt-backed city stores (see §7)."*

---

### MERGED-005 | HIGH Confidence (2 reviewers)
**Severity:** Major | **Lenses:** Structural, Domain  
**IDs:** STRUCTURAL2-A-003, DOMAIN2-A-004

**Title:** Human-verdict Headline "costs nothing" contradicts corrected §5  
**Location:** `research-human-verdict-patterns.md:15` (Headline) vs. `:190` (corrected in §5)

**Description:**  
Headline retains the exact claim MAJ-011 corrected in §5: *"costs nothing."* The correction changed it to *"blocks correctly and tells nobody"* (emphasis on incomplete notification UX). The Headline is the most-quotable passage and still broadcasts the refuted claim.

**Evidence:**  
- Headline:15: "costs nothing"
- §5:190: "[Corrected …] blocks correctly and tells nobody"
- Prior findings list this as MAJ-011 correction

**Suggestion:**  
Align Headline with §5 correction: *"blocks correctly and tells nobody (incomplete notification UX as of v1.4.1)."*

---

### MERGED-006 | HIGH Confidence (2 reviewers)
**Severity:** Minor | **Lenses:** Accuracy, Coherence  
**IDs:** ACCURACY2-A-010, COHERENCE2-A-005

**Title:** Notification-watcher MIN-005 stale framing survives  
**Location:** `research-notification-watcher-layer.md:14` (header) vs. `:172` (6–9d estimate line)

**Description:**  
Header note (line 14) correctly marks MIN-005 as stale: *"gc-not-installed framing stale."* However, line 172 still asserts the refuted premise on the estimate's caveat line: *"neither is true in Momentum today."*

**Evidence:**  
- Line 14: "[Corrected …] MIN-005 stale"
- Line 172: "neither is true in Momentum today" (on 6–9d caveat)

**Suggestion:**  
Remove or rephrase line 172's assertion to match the corrected header framing.

---

### MERGED-007 | HIGH Confidence (2 reviewers)
**Severity:** Minor | **Lenses:** Coherence, Structural  
**IDs:** COHERENCE2-A-008, STRUCTURAL2-A-005

**Title:** Corpus self-count stale: "8/9 files" vs. 10 actual research files  
**Location:** Multiple locations (fix-log, Gemini Notice, DEC-035 Verdict)

**Description:**  
Four locations reference "8 files," "9 research files," or "Nine files" (fix-log enumeration counts 8+1+1). Corpus actually holds 10 research-*.md files plus scope.md = 11 total research artifacts.

**Evidence:**  
- research-production-evidence.md (Reliability Notice, Sources) cites corpus size
- research-dec035-revisit-triggers.md (Verdict) references file count
- Fix-log internal counting (8+1+1≠9)
- Actual file count: research-*.md (10) + scope.md

**Suggestion:**  
Update counts: "10 research-*.md files plus scope.md" or "11 total research artifacts."

---

## Standalone Major Findings

### ACC-001 | MEDIUM Confidence
**Severity:** Major | **Lens:** Accuracy  
**ID:** ACCURACY2-A-001

**Title:** Beads-coupling overcorrection on Dolt requirement  
**Location:** `research-beads-coupling-dec028.md:12, :180, :200` vs. `research-gate-mechanics-handson.md:49–57`

**Description:**  
Correction claims *"embedded Dolt, no external dolt binary required"* but corpus's own A/B evidence contradicts: bd-provider `gc init` demands tmux+dolt+flock on PATH (gate-mechanics:49–57); file-provider tmux-only (Probe 1). FAQ full runtime set includes dolt.

**Evidence:**  
- Beads-coupling :12, :180, :200: "embedded Dolt sufficient"
- Gate-mechanics :49–57: "gc init" command requires dolt+flock on PATH
- FAQ: includes dolt in runtime set

**Suggestion:**  
Scope to *"embedded Dolt sufficient for the bd store itself; a bd-provider CITY additionally requires dolt+flock on PATH; gc start for out-of-session."*

---

### ACC-002 | MEDIUM Confidence
**Severity:** Major | **Lens:** Accuracy  
**ID:** ACCURACY2-A-002

**Title:** Production-evidence counts false like-for-like  
**Location:** `research-production-evidence.md:185, :66`

**Description:**  
Claim: *"1,011 open vs 718 closed — open exceeds lifetime closures."* Verified live at corpus date: 575 open (issue-only) vs 718 closed. The 1,011 figure bundles open PRs (issue-only is 575; total is 1,053; thus 575 open + 718 closed + 760 PRs ≈ 1,053). Census reports "1,729 issues (1,011 open + 718 closed)" but mixes PR-inclusive and issue-only counts without flagging the difference. File itself annotates this (MAJ-004 marker), but the conclusion remains unsupported by like-for-like numbers.

**Evidence:**  
- :66: "1,729 issues (1,011 open + 718 closed)"
- :185: "open issues exceed lifetime closures"
- Live verification: 575 open issues (is:issue is:open search)
- Corpus-dated production evidence: closed > open (718 vs 575)
- Note: MAJ-004 annotation marks query-method difference but doesn't retract conclusion

**Suggestion:**  
Rephrase: *"575 open issues vs 718 closed — closed exceeds open by 143. (Note: 1,011 figure includes 760 open PRs; repo-endpoint count bundles them; this analysis uses issue-only search.)"* Conclusion *"Intake outpaces resolution"* unsupported; strike or qualify.

**Propagation Impact:** Finding strengthens the **[steps.gate]-scarcity** conclusion (no real issues hit the gates), slightly modifying the evidence base.

---

### ACC-003 | MEDIUM Confidence
**Severity:** Major | **Lens:** Accuracy  
**ID:** ACCURACY2-A-003

**Title:** Gate-mechanics top authoring rec contradicts corpus proof  
**Location:** `research-gate-mechanics-handson.md:360` vs. `:305`

**Description:**  
Line 360 recommends ad-hoc `[steps.gate]` gates are *"visible to bd gate check, to gate-sweep."* Line 305 empirically proves the opposite: `bd gate check` returns *"Checked 0 gates"* for human gates. Benefit for type=human is the unreleased notify/renudge orders only.

**Evidence:**  
- :305: "I confirmed empirically that `bd gate check` returns 'Checked 0 gates' even against a properly-typed *ad-hoc* `human` gate."
- :360: "the ad-hoc path persists `await_type`, so it is visible to `bd gate check`, to `gate-sweep`"
- Both marked [EMPIRICAL] and [OFFICIAL]

**Suggestion:**  
Clarify :360: *"The notify/renudge orders (unreleased) may reference ad-hoc gates, but bd gate check and gate-sweep skip them."*

---

### DOM-E-001 | MEDIUM Confidence
**Severity:** Major | **Lens:** Domain (Enum)  
**ID:** DOMAIN2-E-001

**Title:** DOMAIN-A-005 availability caveat applied to only 2 of 4 locations  
**Location:** `research-hitl-alternative-patterns.md:136, :198, :224` and `research-production-evidence.md:75–101`

**Description:**  
Caveat about notify/renudge availability (tagged-release-only, not production-ready) applied to 2 of 4 named locations. Remaining 2 still present notify/renudge as shipped: *"existing precedent,"* *"real, if young, escalation loop,"* *"spam warning."* No corpus-wide grep for "tagged release," "main/edge," "not for production" tags.

**Evidence:**  
- grep: 0 hits for availability caveat tags corpus-wide
- hitl-alternative :136, :198, :224 (inconsistent caveating)
- production-evidence :75–101 (no caveat)

**Suggestion:**  
Add caveat to all notify/renudge references: *"[As of v1.4.1: unreleased feature, tagged-release-only.]"*

---

### DOM-E-002 | MEDIUM Confidence (with conflict note)
**Severity:** Major | **Lens:** Domain (Enum)  
**ID:** DOMAIN2-E-002

**Title:** DOMAIN-A-008 reconciliation incomplete; cross-file overstating  
**Location:** `research-hitl-alternative-patterns.md:§8:240` vs. `research-beads-coupling-dec028.md:§7:182`

**Description:**  
§8 still overstates: *"pulls directly on the open DEC-028 Dolt go/no-go."* Corrected sibling framing (beads-coupling §7) is softer: *"partial decoupling, not clean."* No cross-reference. Domain-enum claims dec035 cites corrected framing; contradicted by 4 other validators (structural-adv, coherence-adv, accuracy-enum, accuracy-adv) quoting dec035:47's stale text with mtime evidence.

**Evidence:**  
- hitl-alternative:240: "pulls directly on the open DEC-028"
- beads-coupling:182: "partial decoupling, not clean"
- Mtime evidence: dec035 14:29, correction 15:37, no reconciliation

**Suggestion:**  
Align :240: *"partial coupling to DEC-028 (city must be Dolt-backed for gate primitives; see beads-coupling §7)."*

---

### DOM-E-003 | MEDIUM Confidence
**Severity:** Major | **Lens:** Domain (Enum)  
**ID:** DOMAIN2-E-003

**Title:** Failed-close semantics of drain+check barrier absent corpus-wide  
**Location:** Corpus-wide search yields 0 hits

**Description:**  
No location documents what happens if a drain+check barrier fails to close (e.g., check loop crashes, close step errors). Does a failed close release dependents? Does the results gate open on unconfirmed phase? This gap leaves Momentum's error path undefined.

**Evidence:**  
- grep "failed.*close\|close.*fail\|close.*error" research-*.md: 0 hits describing failure semantics
- Corpus extensively covers drain+check construction but not failure modes

**Suggestion:**  
Add to a suitable location (maturity-open-bugs or gate-mechanics): *"Failed-close semantics: if a drain+check barrier fails to close (step error, check loop timeout), [X happens; dependents are/are not released; gate is blocked/open/undefined]. Recommend order-level timeout + manual intervention path."*

---

## Standalone Minor Findings

### ACC-005 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Accuracy  
**ID:** ACCURACY2-A-005

**Title:** Beads-coupling §8 probe wording overstates durability claim  
**Location:** `research-beads-coupling-dec028.md:206`

**Description:**  
§8 claims Probe 2 *"confirms FileStore.SetMetadata durable"* but probe tested engine-written key + hand-edited read-back only; no CLI write path exists. Mirror §2's hedged wording; point stays moot-by-no-write-path.

**Suggestion:**  
Hedge: *"Probe 2 tests hand-edited metadata durability (no CLI write path currently exists)."*

---

### ACC-006 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Accuracy  
**ID:** ACCURACY2-A-006

**Title:** Gemini Reliability Notice missing row  
**Location:** Refuted-claims table (12 rows visible)

**Description:**  
Table omits #3451 row (Gemini invented Homebrew meaning; rated corpus-blocking gap "minor friction").

**Suggestion:**  
Add row to table: *"#3451 | container `needs` does not gate children | (invented Homebrew meaning) | workaround unavailable to Momentum (runtime-discovered children) | blocks gate (d) | Major"*

---

### ACC-007 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Accuracy  
**ID:** ACCURACY2-A-007

**Title:** Beads-coupling §8 residual and self-reference issues  
**Location:** `research-beads-coupling-dec028.md:22, :66`

**Description:**  
(a) "five implementations...and the four backing stores" residual (counts do not match post-CRIT-004); (b) self-referential "§2 above" + inverted subject sentence at :66 (intended referent §7:180).

**Suggestion:**  
(a) Update count to align with corrected provider enumeration. (b) Change "§2 above" to "§7:180" and fix subject.

---

### ACC-008 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Accuracy  
**ID:** ACCURACY2-A-008

**Title:** Scope.md sub-question 4 carries refuted premise  
**Location:** `scope.md:10, :29`

**Description:**  
Sub-question 4 still states refuted claude-p/exec-step premise unmarked.

**Suggestion:**  
Append: *"(premise refuted — CRIT-005; see cycle-orchestration-fit §1)."*

---

### COH-A-004 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Coherence  
**ID:** COHERENCE2-A-004

**Title:** Maturity synthesis table contradiction  
**Location:** `research-maturity-open-bugs.md:135` (synthesis table) vs. `:219, :221` (prose)

**Description:**  
Synthesis table still says "inert but harmless" after MAJ-011 struck it in prose. Row (b) has caveat; rows (a)/(c) don't — internally inconsistent. Plus duplicated-clause seam artifact at :135.

**Suggestion:**  
Harmonize table: apply MAJ-011 correction to all rows. Fix seam artifact.

---

### COH-A-007 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Coherence  
**ID:** COHERENCE2-A-007

**Title:** Cycle-fit 15–25d estimate unreconciled with §9b  
**Location:** `research-cycle-orchestration-fit.md:191` vs. `:205`

**Description:**  
15–25d estimate sized to four gates; §9b adds a fifth (push authority) 14 lines later, unreconciled. Dec035:103 overnight-run shape omits push constraint.

**Evidence:**  
- :191: "15–25 days" for four gates
- :205: §9b introduces fifth gate (push authority) unreconciled
- dec035:103: overnight shape omits push

**Suggestion:**  
Revise estimate or scope: *"The four initial gates are 15–25d; push-authority gate (§9b) adds [X] days; dec035:103's overnight run assumes [which gates?]."*

---

### DOM-A-003 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Domain (Adv)  
**ID:** DOMAIN2-A-003

**Title:** Hitl-alternative gate-creation construct is silent-failure class  
**Location:** `research-hitl-alternative-patterns.md:§7(b):210` vs. `research-beads-coupling-dec028.md` MAJ-010 standard

**Description:**  
Replacement gate-creation construct is prose instruction-to-LLM (same silent-failure class CRIT-005 eliminated). Agent may skip/garble bd gate create → no gate, no ask.

**Suggestion:**  
Add verification read-back asserting gate bead exists, or order-level exec path with guaranteed execution.

---

### STRUCT-A-004 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Structural  
**ID:** STRUCTURAL2-A-004

**Title:** Scope.md index missing verification-probes.md  
**Location:** `scope.md` sub-questions index (lists 9, should list 10)

**Description:**  
Verification-probes.md (the fix pass's own ground truth) missing from sub-questions index.

**Suggestion:**  
Add as sub-question 10 with description.

---

### STRUCT-E-001 | MEDIUM Confidence
**Severity:** Minor | **Lens:** Structural (Enum)  
**ID:** STRUCTURAL2-E-001

**Title:** Cross-reference truncated in beads-coupling  
**Location:** `research-beads-coupling-dec028.md:22`

**Description:**  
Fix-pass provenance citation truncated: *"STRUCTURAL-A"* with no numeric suffix (should be STRUCTURAL-A-011, the four-vs-five provider count finding).

**Suggestion:**  
Append: *"-011"* to make it resolvable.

---

## Standalone Low Findings

| ID | Severity | Title | Location |
|---|---|---|---|
| ACCURACY2-A-009 | low | Gate-type-agnostic close-enforcement untagged | `gate-mechanics:188` |
| ACCURACY2-A-011 | low | Off-by-one date; #4452 uncited; fix-log count | `dec035:69, :134; fix-log` |
| COHERENCE2-A-009 | low | Beads-coupling self-reference ↑§2 | `beads-coupling:66` (intended §7:180) |
| COHERENCE2-A-010 | low | Contributor concentration unannotated | `maturity:46–47` vs. `production-evidence:177` |
| STRUCTURAL2-A-006 | low | Off-by-one date (file dated 2026-08-24, not 08-23) | `dec035:69` |

---

## Fixer Guidance: Propagation Sweep

**For each conclusion-changing fix (CRIT-004, CRIT-005, MAJ-010, MAJ-011, MAJ-015), grep the WHOLE corpus for the old claim's phrasing, not just the finding's cited location.** The most common miss is authors correcting one sentence and leaving parallel sentences elsewhere (beads-coupling §3/§5/§7 is the canonical example).

**High-risk patterns to sweep:**
1. "does NOT force DEC-028 / GC_BEADS=file is alive" (pre-CRIT-004 version; appears in dec035, possibly elsewhere)
2. "claude -p subprocess / claude -p phase step / claude -p runner" (CRIT-005 version; residue in hitl-alternative)
3. "costs nothing" (MAJ-011 version; residue in human-verdict Headline)
4. "fully Dolt-free city is expressible" (pre-CRIT-004 version; residue in beads-coupling §3/§5)
5. "visible to bd gate check, to gate-sweep" for ad-hoc gates (falsified by line 305; residue in line 360)

**Sweep commands:**
```bash
grep -rn "does NOT force DEC-028" research-*.md
grep -rn "claude -p subprocess\|claude -p phase step\|claude -p runner" research-*.md
grep -rn "costs nothing" research-*.md
grep -rn "fully Dolt-free city" research-*.md
grep -rn "visible to bd gate check.*gate-sweep" research-*.md
```

**Verification after fixes:**
- Recount corpus files (should be 10 research-*.md + scope.md)
- Verify dec035:47, :121 match beads-coupling §7's Bottom Line
- Cross-check hitl-alternative §8:240 against beads-coupling §7:182 for alignment
- Confirm gate (d) caveat appears in all three recommendation files (gate-mechanics, hitl-alternative, human-verdict)
- Verify notify/renudge caveat tagged consistently across all 4 locations

---

## Summary of Cleaned Findings

- **Deduplication:** 8 findings merged (6 major, 2 minor); 27 unique findings remain
- **Conflict Adjudication:** Domain-enum "good news" note contradicted by mtime evidence; stale DEC-035 citation finding stands
- **Medium-Confidence Validation:** Spot-checks (production-evidence counts, gate-mechanics ad-hoc visibility, failed-close semantics absence) all verified; no hallucinations found
- **Score Impact:** 14 majors × 8 + 9 minors × 3 + 4 lows × 1 = 143 point penalty → **−43 final score (FAILING)**

**Corpus status:** Not safe to synthesize as-is. The stale DEC-035 citation and two gate (d) contradictions are decision-grade blockers. Beads-coupling internal inconsistencies (§3/§5 vs. §7) undermine the strongest technical finding. Fixer should prioritize MERGED-001, MERGED-002, MERGED-004 before releasing for decision synthesis.
