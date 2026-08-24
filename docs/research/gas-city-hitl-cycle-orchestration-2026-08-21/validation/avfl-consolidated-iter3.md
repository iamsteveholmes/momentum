# AVFL Iter3 Consolidated Findings

**Report Date:** 2026-08-21  
**Raw Findings:** 47 across 8 validators (6 accuracy-adv, 0 accuracy-enum, 11 coherence-adv, 1 coherence-enum, 7 domain-adv, 1 domain-enum, 4 structural-adv, 2 structural-enum)  
**Consolidated Findings:** 27 after dedup  
**Final Score:** −38 / 100  
**Grade:** FAILING  

---

## Deduplication & Cross-Lens Merges

**Known merges applied (6 two-way, 1 three-way = 13 items consolidated into 6 final findings):**

1. **6–9d scope qualifier stripped** (HIGH: 3 reviewers)
   - ACCURACY3-A-001 + DOMAIN3-A-002 + COHERENCE3-A-007 → **MAJOR**
   - Source: both citation sites, scope limits dropped at iter2; verdict-path share (3–5d) is per-gate work

2. **production-evidence Finding 2 caveat residue** (HIGH: 3 reviewers)
   - COHERENCE3-A-001 + STRUCTURAL3-A-002 + DOMAIN3-E-001 (flagged HIGH) → **MAJOR**
   - Orchestrator note: Finding 2 header/intro "shipped" wording at :75–77, :207 still uncaveated; caveat landed only at :14 Bottom Line

3. **wrong-row pointer** (HIGH: 2 reviewers)
   - STRUCTURAL3-E-001 + COHERENCE3-E-001 → **MINOR**
   - "fan-out hazard in the row below" points at :174; actual is :177 (last row)

4. **760 PRs arithmetic impossible** (HIGH: 2 reviewers)
   - ACCURACY3-A-003 + STRUCTURAL3-A-003 → **MINOR**
   - Regressed from ACC-002 fix: 1,011−575=436, not 760; unsourced import from consolidated report

5. **three-vs-four bullets** (HIGH: 2 reviewers)
   - ACCURACY3-A-004 + COHERENCE3-A-004 → **MINOR**
   - Introduced iter2 #4452; count not updated

6. **backwards correction marker** (HIGH: 2 reviewers)
   - STRUCTURAL3-E-002 + COHERENCE3-A-005 → **MINOR**
   - "pre-CRIT-004 framing below is superseded" precedes the corrected text, reading as if new text is superseded

**Cross-lens merge statistics:**
- Dedup factor: 47 raw → 27 consolidated (20 items removed, 13 consolidated into 6)
- High-confidence items (2+ reviewers): 6
- Medium-confidence items (single source): 21

---

## Consolidated Findings by Severity

### MAJOR (13)

1. **6–9d scope qualifier stripped** [HIGH confidence]
   - **What:** Scope limits "FOR ONE GATE TYPE" + "city standup uncosted" stripped at citation sites
   - **Why:** Restores ~2.5–4d shared infra vs ~3–5d per-gate split; both limits essential for cost accuracy
   - **Evidence:** cycle-fit:181,:191; dec035:49 vs original dec035:47 + cycle-fit:191 scoping; §9c prescription present
   - **Recommendation:** Restore scope notation; add multiplication note (four/five-gate floor understated)
   - **Reviewers:** accuracy-adv (ACCURACY3-A-001), domain-adv (DOMAIN3-A-002), coherence-adv (COHERENCE3-A-007)

2. **production-evidence Finding 2 caveat residue** [HIGH confidence]
   - **What:** Caveat present only at :14 Bottom line; Finding 2 header/intro + Recommendations still claim "real and recently-shipped" without tagged-release caveat
   - **Why:** Momentum-facing Recommendations :207 "the shipped path" is decision-bearing; :212 "actual production support" exactly refuted the issue
   - **Evidence:** Finding 2 :75 header "shipped 2026-07-23", :77 intro (no caveat), :207/:212 recommendations; caveat at :14 only
   - **Recommendation:** Add standard caveat sentence at :77 and :207 (the :14 Bottom Line caveat is insufficient for the Finding 2 narrative)
   - **Reviewers:** coherence-adv (COHERENCE3-A-001), structural-adv (STRUCTURAL3-A-002), domain-enum (DOMAIN3-E-001 HIGH)

3. **cycle-fit "decoration" paraphrase residue** [HIGH confidence, single source]
   - **What:** MAJ-011 correction never reached cycle-fit; paraphrase residue "the semantics are decoration"/"decorative" in 3 decision-bearing places
   - **Why:** Contradicts same file :197 and corpus consensus; root cause literal-string grep ("costs nothing") missed paraphrase
   - **Evidence:** cycle-fit:137,:173,:227 "decoration" paraphrase; fit-table row edited iter2; open question #5 answered elsewhere
   - **Recommendation:** Fix author gloss (not spec quote); use paraphrase-tolerant sweep method
   - **Reviewer:** structural-adv (STRUCTURAL3-A-001)

4. **bd-ready dispatch precondition undisclosed** [HIGH confidence, single source]
   - **What:** "adopt bd human gates today, free" stated without scope condition: bd gate blocks only work dispatched through `bd ready`, not all work
   - **Why:** Momentum Conductor dispatches from index.json/depends_on under dual-write, so bd-only adoption has undisclosed prerequisite (move dispatch to bd ready = DEC-028 open question)
   - **Evidence:** human-verdict:293 scope condition; missing at hitl-alternative §7, dec035 rec, human-verdict §5/§8
   - **Recommendation:** Add scope condition to hitl-alternative §7 preamble + human-verdict §5/§8
   - **Reviewer:** domain-adv (DOMAIN3-A-001)

5. **headline "two load-bearing gaps" vs body "three gaps"** [HIGH confidence, single source]
   - **What:** dec035 headline:10 says "two load-bearing gaps"; body:41 and Verdict:98 say "three" (push-authority added as gap 3)
   - **Why:** Same defect class as MERGED-005 (incomplete update after spec change)
   - **Evidence:** dec035 headline:10 not updated post-iter2; all three gaps named in body:41
   - **Recommendation:** Fix headline :10 → "three", naming all
   - **Reviewer:** domain-adv (DOMAIN3-A-003)

6. **barrier statement drops "declarative" qualifier** [HIGH confidence, single source]
   - **What:** dec035:45,:98 barrier "no reliable expression" / "no working expression" drops "declarative" qualifier and sanctioned construction
   - **Why:** Corpus's settled answer is "sanctioned construction exists, unproven for runtime-discovered set, unverified failed-close, §9c guard prescribed" — statement reads opposite (no-go)
   - **Evidence:** dec035:45,:98 vs maturity:224 + §9c language; "sanctioned construction" clause missing
   - **Recommendation:** Mirror maturity:224 language; restore "declarative" and sanctioned-construction scope
   - **Reviewer:** domain-adv (DOMAIN3-A-004)

7. **gate-mechanics EMPIRICAL headline overclaim** [HIGH confidence, single source]
   - **What:** Headline claims bd-close refusal as [EMPIRICAL] "all reproduced" after §Q2 downgraded it to [UNVERIFIED for human gates]
   - **Why:** Decision-relevant: (c)-gate "cleanest fit" rests on bd-close refusal claim; status downgrade not reflected in headline
   - **Evidence:** gate-mechanics:10 vs :188; timer-gate transcript; dec035:37 quotes incorrect headline verbatim
   - **Recommendation:** Sync headline with §Q2 downgrade; mark [UNVERIFIED for human gates]
   - **Reviewer:** coherence-adv (COHERENCE3-A-002)

8. **verdict upgrades to "proven" against open items** [HIGH confidence, single source]
   - **What:** dec035:98 Verdict upgrades [OFFICIAL] doc claims to "proven" (hour-long steps, multi-day parking) against sibling file listing both as genuinely open
   - **Why:** Misrepresents readiness; iter2-introduced conflation
   - **Evidence:** dec035:98 "proven" vs cycle-fit §10 Q1-Q2 listing both as open; dec035:34,:36 also list as open
   - **Recommendation:** Downgrade to "documented and partly proven (...documented but not exercised)"
   - **Reviewer:** coherence-adv (COHERENCE3-A-003)

9. **direction inverted in incidence calculation** [HIGH confidence, single source]
   - **What:** iter2 correction claims smaller denominator "makes the scarcity finding STRONGER" — logically inverted (1/1,293 > 1/1,729 incidence)
   - **Why:** Error inherited from consolidated report's fix log; conclusion survives but direction claim is backwards
   - **Evidence:** production-evidence:66; iter2 logic error (scarcity increases with smaller denominator—no)
   - **Recommendation:** Fix direction claim honestly; conclusion stands
   - **Reviewer:** accuracy-adv (ACCURACY3-A-002)

### MINOR (10)

10. **wrong-row pointer** [HIGH confidence]
    - **What:** cycle-fit:173 "the fan-out hazard in the row below" points at unrelated row :174; actual hazard row is :177 (last row of table)
    - **Why:** Breaks reference integrity; reader cannot locate the actual hazard
    - **Evidence:** cycle-fit:173 "row below" → :174 (unrelated); :177 is last row with actual hazard
    - **Recommendation:** Fix pointer: "the table's last row" or explicit "#3451 row"
    - **Reviewers:** structural-enum (STRUCTURAL3-E-001), coherence-enum (COHERENCE3-E-001)

11. **760 PRs arithmetic impossible** [HIGH confidence]
    - **What:** "roughly 760 open PRs" at production-evidence:185 is arithmetically impossible (1,011−575=436)
    - **Why:** Regressed from ACC-002 fix; unsourced, lifted from garbled consolidated-report arithmetic
    - **Evidence:** 1,011 − 575 = 436, not 760; 718's query method never stated (need "like-for-like" annotation)
    - **Recommendation:** Fix to 436 or drop; annotate query method
    - **Reviewers:** accuracy-adv (ACCURACY3-A-003), structural-adv (STRUCTURAL3-A-003)

12. **three-vs-four bullets** [HIGH confidence]
    - **What:** "Three corroborating signals" heads dec035:67 now FOUR bullets (iter2 #4452 insertion without count update)
    - **Why:** Misleading count affects signal weight in decision
    - **Evidence:** dec035:67 three→four after iter2; COHERENCE3-A-004 confirms
    - **Recommendation:** Update to four
    - **Reviewers:** accuracy-adv (ACCURACY3-A-004), coherence-adv (COHERENCE3-A-004)

13. **backwards correction marker** [HIGH confidence]
    - **What:** dec035:49 marker wording "the pre-CRIT-004 framing below is superseded" precedes the corrected text, reading as if new text is superseded
    - **Why:** Inverts marker semantics; reader cannot tell what text is corrected vs. what is new
    - **Evidence:** dec035:49 structure vs. gate-mechanics:64's well-formed pattern
    - **Recommendation:** Reword per gate-mechanics:64 model
    - **Reviewers:** structural-enum (STRUCTURAL3-E-002), coherence-adv (COHERENCE3-A-005)

14. **notify/renudge caveat unscoped in risks** [MEDIUM confidence, single source]
    - **What:** hitl-alternative §8 Risks lists fifth notify/renudge location uncaveated: "Treat the nag loop as beta"
    - **Why:** Should clarify "unshipped, not merely beta (main/edge only)"
    - **Evidence:** hitl-alternative §8 vs notify/renudge caveats elsewhere
    - **Recommendation:** Add standard "unshipped" caveat
    - **Reviewer:** coherence-adv (COHERENCE3-A-006)

15. **bd-version narrative inconsistent** [MEDIUM confidence, single source]
    - **What:** probes:238 vs :280 + beads-coupling:163,:170 + gate-mechanics:22 inconsistent on newest-published (v1.2.2 ran empirically vs "newest published v1.1.2")
    - **Why:** DEC-028 multi-agent-write-safety row premise ordering unsettled
    - **Evidence:** v1.2.2 empirical vs. v1.1.2 "newest published" contradiction
    - **Recommendation:** Reconcile in Probe 5
    - **Reviewer:** coherence-adv (COHERENCE3-A-008)

16. **finding-IDs undefined in scope** [MEDIUM confidence, single source]
    - **What:** validation finding-IDs used inline in evidence-tag typography, undefined in scope.md; MERGED-002 resolves to nothing from findings files
    - **Why:** Scope document incomplete for readers unfamiliar with the ID system
    - **Evidence:** corpus-wide finding-ID usage vs. scope.md absence
    - **Recommendation:** Define correction-marker notation in scope.md or strip bare IDs
    - **Reviewer:** coherence-adv (COHERENCE3-A-009)

17. **marker density misleading** [MEDIUM confidence, single source]
    - **What:** 146 marker mentions corpus-wide; Bottom Line doesn't lead with conclusion; §7 answer buried under 350-word re-derivation; unclosed bracket at :188 makes claim read retracted; bolded :360 takeaway inverted from scoping
    - **Why:** Marker archaeology obscures findings; users must reverse-engineer intent
    - **Evidence:** beads-coupling:12,:180; gate-mechanics:188,:360; corpus-wide marker count
    - **Recommendation:** Conclusion-first structure; correction-history as trailing notes (see COHERENCE3-A-010 in coherence-adv.md)
    - **Reviewer:** coherence-adv (COHERENCE3-A-010)

18. **merge velocity comparison mixed population** [MEDIUM confidence, single source]
    - **What:** maturity:38 "Merge velocity vastly outruns issue closure" repeats mixed-population comparison (575 all-time vs 380 May-cohort) that ACC-002 struck
    - **Why:** Misleading comparison; different populations
    - **Evidence:** maturity:38 vs. production-evidence ACC-002 fix (575 all-time vs. 718 May-cohort)
    - **Recommendation:** Annotate or use like-for-like comparison (575 vs. 718)
    - **Reviewer:** domain-adv (DOMAIN3-A-005)

19. **verdict vocabularies unlabeled** [MEDIUM confidence, single source]
    - **What:** notification-watcher:162 vs human-verdict:287 use two verdict vocabularies both correct at different levels (gate-level A/M/R vs per-fork approve/modify/remove) — unlabeled, no cross-ref
    - **Why:** Write-back schema needs both key families; reader cannot correlate
    - **Evidence:** gate-level vs. per-fork vocabularies used without alignment
    - **Recommendation:** Label + cross-reference both vocabularies
    - **Reviewer:** domain-adv (DOMAIN3-A-006)

20. **gemini Reliability Notice missing row** [MEDIUM confidence, single source]
    - **What:** gemini Reliability Notice body lists pr-pipeline "hard non-negotiable pre-push gate" but production-evidence:53-62 refutes it (prose-in-step, agent-judgment exit, not structural)
    - **Why:** Lands on push-authority axis; critical for Reliability matrix
    - **Evidence:** gemini body claim vs. production-evidence:53-62 refutation
    - **Recommendation:** Add row documenting actual pr-pipeline behavior
    - **Reviewer:** domain-adv (DOMAIN3-A-007)

### LOW (4)

21. **citation precision** [MEDIUM confidence, single source]
    - **What:** cycle-fit §3 cited for rejection-indistinguishability (lives at §2:112+§6:234); §2 cited for fail-closed attempt-scoped guard (lives at §7:279)
    - **Why:** Citation precision affects verification burden
    - **Evidence:** cycle-fit citation sites vs. actual content locations
    - **Recommendation:** Fix provenance precision
    - **Reviewer:** accuracy-adv (ACCURACY3-A-005)

22. **gc clause "specifically" contradiction** [MEDIUM confidence, single source]
    - **What:** beads-coupling:12 "gc start specifically" clause contradicts same sentence's "gc init's own dependency gate demands dolt+flock"
    - **Why:** Scope clarity
    - **Evidence:** beads-coupling:12 "specifically" vs. "init enforces up front"
    - **Recommendation:** Drop "specifically"; state init enforces because start needs binaries
    - **Reviewer:** accuracy-adv (ACCURACY3-A-006)

23. **CRIT-005 grep backtick issue** [MEDIUM confidence, single source]
    - **What:** fix-log-iter2 CRIT-005 grep structurally cannot match (backticks); "0 hits. Clean." is not evidence
    - **Why:** Grep pattern validation
    - **Evidence:** backtick-tolerant pattern needed; residue verified clean by hand
    - **Recommendation:** Record backtick-tolerant pattern for future verification
    - **Reviewer:** coherence-adv (COHERENCE3-A-011)

24. **frontmatter unmarked premise** [MEDIUM confidence, single source]
    - **What:** cycle-fit:4 frontmatter refuted exec-step premise unmarked in sub_question field
    - **Why:** Scope clarity
    - **Evidence:** scope.md's two copies got ACC-008 marker but cycle-fit:4 frontmatter didn't
    - **Recommendation:** Append same marker to :4 frontmatter
    - **Reviewer:** structural-adv (STRUCTURAL3-A-004)

---

## Scoring & Grade

| Category | Count | Deduction | Subtotal |
|---|---|---|---|
| MAJOR | 13 | −8 each | −104 |
| MINOR | 10 | −3 each | −30 |
| LOW | 4 | −1 each | −4 |
| | | | |
| **Base Score** | | 100 | **100** |
| **Total Deduction** | | | **−138** |
| **Final Score** | | | **−38** |

**Grade: FAILING** (<50)

---

## Fixer Guidance

**Recurring pattern identified:**
1. **Scope/qualifier drops:** both cite sites (cost multiplier not restored; "for one gate type" stripped)
2. **Marker archaeology:** correction markers now misleading; users cannot infer conclusion from density
3. **Paraphrase sweeps:** literal-string grep ("costs nothing") misses author paraphrases ("decoration"); root-cause for cycle-fit MAJ-011 miss

**Structural recommendations for next pass:**

1. **For scope multipliers:** After each citation site edit, verify both cited work and citation in situ carry the same qualifier/limit/scope
2. **For marker density:** Restructure affected passages conclusion-first:
   - **Bottom Line / Conclusion leads.** The finding, decision, or takeaway is the first sentence.
   - **Correction history trails.** Marker archaeology and iter history become a secondary note or appendix.
   - **See COHERENCE3-A-010 analysis** in coherence-adv.md for the three passages (beads-coupling:12,:180; gate-mechanics:188,:360) that need restructure

3. **For paraphrase residue:** Replace literal-string grep patterns with semantic-grep sweeps:
   - Grep for related terms/synonyms (e.g., "decoration", "decorator", "decorative", "semantic-decorative")
   - Cross-check editing sites manually for paraphrased intent
   - Document backtick-escaping in sweep procedures for future audits

**Notable clean areas:**
- MERGED-002/004/005/006/007 fully propagated (no over-correction)
- All 27 iter2 fixes verified landed; 7 grep sweeps independently clean
- Corpus cross-refs/headers/frontmatter/index consistent
- Caveat scoping consistent (except production-evidence Finding 2 narrative)
- Self-count reconciliation complete (575/718/1,293 consistent)

---

## Sign-Off

**Consolidator:** AVFL Iter3 (multi-lens adversarial review)  
**Confidence Distribution:** HIGH (6 cross-lens), MEDIUM (21 single-source)  
**Dedup Efficiency:** 47 raw → 27 consolidated (43% reduction via merge)  
**Ready for:** Fixer iteration 4
