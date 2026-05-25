# AVFL Consolidation Report: Momentum Triage Dedup Spec

**Session:** AVFL Phase 8 Consolidation  
**Input:** 8 parallel validators (Structural ×2, Accuracy ×2, Coherence ×2, Domain ×2)  
**Status:** SCAN_COMPLETE  
**Final Grade:** FAILING (score: 0)

---

## Executive Summary

The Momentum Triage Dedup specification contains **4 critical, 5 high, 6 medium, and 8 low severity findings** across 22 consolidated issues. The specification is **not ready for implementation**. Four critical errors in algorithm design, scope definition, and output specification will cause functional failures. Five high-severity contradictions between spec statement and detail create ambiguity for developers.

**Primary blockers:**
1. Phase 1 clustering algorithm is missing the ≥0.4 similarity threshold — all pairs will be merged regardless of score
2. Phase 3 implements Story B (consolidation analysis) within Story A's scope — architectural violation
3. Step 6 output template references 9 unassigned variables — summary will be incomplete
4. Four major spec contradictions (Phase 5 non-existent, Step 4 header, consume wording, fallback promise) — documentation is inconsistent with implementation

**Recommendation:** Return to specification phase for major revision. Do not proceed to implementation until all critical and high-severity findings are addressed.

---

## Consolidation Methodology

**Deduplication rules applied:**
- Combined findings from same issue across multiple validators → promoted to HIGH confidence
- Single-source findings with clear evidence → kept as MEDIUM confidence
- Validator hallucinations (test count 548 vs 170 observed) → discarded
- Validator prompt errors (AC15 missing from input) → discarded
- Low-impact findings (formatting, style, comments) → kept as LOW confidence

**Confidence levels:**
- **HIGH:** 9 findings (found by paired reviewers or multi-validator consensus)
- **MEDIUM:** 7 findings (single source, evidence confirmed)
- **LOW:** 8 findings (organizational/minor issues)

**Removed findings:** 2 (STRUCTURAL-003 test count hallucination; STRUCTURAL-005 AC15 prompt error)

---

## Final Consolidated Findings

### CRITICAL SEVERITY (−15 points each)

#### TRIAGE-001: Phase 1 clustering algorithm missing ≥0.4 threshold
- **Confidence:** HIGH
- **Sources:** DOMAIN-001 (enumerator), Domain Adversary consensus
- **Spec reference:** Story spec Dev Notes: "greedily assign i and j to the same cluster if both are unassigned and **similarity ≥ 0.4**"
- **Actual implementation:** Step 2.2 says "If both unassigned: create a new cluster containing {i, j}" with no threshold condition
- **Evidence:** Threshold explicitly mandated in story; workflow omits it entirely
- **Impact:** CRITICAL — Algorithm produces incorrect results. With no threshold, all pairs merge regardless of similarity score. Contradicts story requirement.
- **Action required:** Add similarity threshold check to Step 2.2, rule 4b: `If both unassigned AND similarity ≥ 0.4: create new cluster`

#### TRIAGE-002: Phase 3 cross-cluster cosine scan violates Story A scope
- **Confidence:** HIGH
- **Sources:** ACCURACY-001 (accuracy adversary)
- **Spec reference:** AC12: "Phase 3 groups consolidation_hint by target_slug_or_theme; 2+ members = merge candidate. Story B scope — no execution."
- **Actual implementation:** Phase 3 Step 2.4 creates merge candidates from raw cosine similarity pairs, not from dedup-agent consolidation_hint values
- **Evidence:** Workflow text: "append a merge candidate: { target: 'cross-cluster-pair', members: [item_i, item_j], rationale: 'high intra-batch similarity...' }". AC12 limits to grouping consolidation_hint from dedup agent findings.
- **Impact:** CRITICAL — Implements Story B (consolidation analysis) within Story A's specification. Violates scope boundary. Cross-cluster analysis is explicitly deferred to Story B.
- **Action required:** Remove Phase 3 cross-cluster cosine scan. Keep only consolidation_hint grouping from dedup-agent output.

#### TRIAGE-003: Step 6 output template has 9 unassigned variables
- **Confidence:** HIGH
- **Sources:** COHERENCE-003/004 (enumerator consensus) merged
- **Unassigned variables:** consumed_count, split_count, merge_candidate_count, shaping_count, defer_count, reject_count, remaining_open_count, resolved_count, failure_count
- **Additional issue:** Variable name mismatch — Step 4 stores `{{rejected_count}}`; Step 6 template references `{{rejected_count_approval}}`
- **Evidence:** Step 6 output template references variables; scan of all steps finds no Store assignments for these names
- **Impact:** CRITICAL — Step 6 summary output will render with missing/unbound variables. Affects sprint summary artifact. Incomplete specification.
- **Action required:** Either (a) define Store assignments for all 9 variables in appropriate steps, OR (b) remove unassigned variables from Step 6 template. Standardize variable naming.

#### TRIAGE-004: Phase 0 fallback false promise
- **Confidence:** HIGH
- **Sources:** STRUCTURAL-ADVERSARY-001, DOMAIN-002 consensus
- **Spec statement:** "Phase 1 will assign all items to one cluster"
- **Actual behavior:** With empty similarity matrix, Phase 1's greedy algorithm produces N singleton clusters (one per item)
- **Evidence:** Fallback line 131 claims one cluster; Step 2.2 rule 5 says "Any item still unassigned after processing all pairs gets its own singleton cluster" — with zero pairs processed, every item becomes singleton
- **Impact:** CRITICAL — False promise in fallback spec. Developer will expect one cluster; code produces N singletons. Mismatched expectations.
- **Action required:** Correct fallback statement to "Phase 1 will assign each item to its own singleton cluster if similarity matrix is empty" or provide alternate fallback logic.

---

### HIGH SEVERITY (−8 points each)

#### TRIAGE-005: Goal references non-existent "Phase 5"; workflow is 4 steps
- **Confidence:** HIGH
- **Sources:** COHERENCE-001 (enumerator ×2), Coherence Adversary, Domain Enumerator — 4-validator consensus
- **Spec goal:** "present dedup + classification approval (Phase 5)"
- **Actual workflow:** `<step n="4" goal="Batch approval...">`
- **Evidence:** Goal text explicitly states "Phase 5"; workflow only defines 4 numbered steps
- **Impact:** HIGH — Spec-to-implementation mismatch. Confuses developer about workflow structure. Navigation error.
- **Action required:** Change goal to reference "Step 4" or rename workflow to 5 steps if Phase 5 genuinely intended.

#### TRIAGE-006: Step 4 header "proceeding to classification" contradicts Step 3 execution
- **Confidence:** HIGH
- **Sources:** COHERENCE-002 (enumerator, adversary consensus)
- **Step 3 goal:** "Classify and enrich survivor items"
- **Step 4 header:** "{{survivor_count}} survivors proceeding to classification"
- **Evidence:** Classification happens in Step 3 (before Step 4). Step 4 header implies it's in the future.
- **Impact:** HIGH — Spec clarity issue. Ambiguous to developer about order of operations. May cause implementation errors.
- **Action required:** Correct Step 4 header to "{{survivor_count}} survivors classified and approved" or similar.

#### TRIAGE-007: Consume wording contradicts AC14
- **Confidence:** HIGH
- **Sources:** ACCURACY-006 (accuracy adversary)
- **Step 4 output:** "consume ({{count}} — confirmed duplicates — will be removed from classification)"
- **AC14 statement:** "consumed items removed from queue"
- **Step 2.4 logic:** Consumed items are PRE-EXCLUDED from classification (never entered the classification pipeline)
- **Evidence:** Step 2.4 filters: consumed items are kept separate; Step 4 says they're "removed from classification" (implying they were in it)
- **Impact:** HIGH — Spec contradiction. Consumers items never entered classification, so they can't be "removed from" it. Misleads developer.
- **Action required:** Change Step 4 wording to "consume ({{count}} — confirmed duplicates — excluded from classification)"

#### TRIAGE-008: Status filter deny-list allows review/verify states
- **Confidence:** HIGH
- **Sources:** STRUCTURAL-001 (enumerator)
- **AC3 requirement:** Only `backlog`, `ready-for-dev`, `in-progress` are valid candidates
- **Actual filter:** `TRIAGE_TERMINAL_STATES = {"done", "dropped", "closed-incomplete"}` (deny-list approach)
- **Problem:** Deny-list includes `review` and `verify` in `ORDERED_STATES`, which are NOT in AC3's allow-list
- **Evidence:** Lines 1990 (deny-list definition) and 39 (state order definition) show mismatch
- **Impact:** HIGH — Incorrect status filtering. Invalid candidate states will pass through. AC3 violation.
- **Action required:** Change filter to use allow-list approach: `allowed_candidates = {"backlog", "ready-for-dev", "in-progress"}`

#### TRIAGE-009: Fallback greedy assignment logic differs from spec expectation
- **Confidence:** HIGH
- **Sources:** DOMAIN-001, Accuracy Adversary
- **Spec expectation:** Phase 1's greedy algorithm produces one cluster (from fallback statement)
- **Actual logic:** With empty matrix, produces N singletons
- **Root cause:** Greedy algorithm depends on similarity scores; with no scores, no pairs can merge
- **Impact:** HIGH — Algorithm doesn't match developer's mental model from fallback. Unexpected output.
- **Action required:** Correct fallback statement or provide alternate strategy for low-similarity scenarios.

---

### MEDIUM SEVERITY (−3 points each)

#### TRIAGE-010: Step 4 "skip N" override revives item without re-classification
- **Confidence:** MEDIUM
- **Sources:** STRUCTURAL-ADVERSARY-002/005 consensus
- **Step 3 logic:** "For each item in {{survivor_items}}, classify it"
- **Step 4 logic:** "'skip N' → override dedup finding for item N, keep in classification"
- **Problem:** Item N was excluded from survivor_items (and thus from classification) at Step 2.4. When skip override revives it in Step 4, no re-classification step exists.
- **Evidence:** No action between Step 4 override and Step 6 output to re-classify the revived item
- **Impact:** MEDIUM — Revived item remains unclassified. Workflow incomplete. Output will lack classification for this item.
- **Action required:** Add re-classification step in Step 4: "Re-classify item N using Step 3 logic"

#### TRIAGE-011: Union shortlist score consolidation loses per-item context
- **Confidence:** MEDIUM
- **Sources:** ACCURACY-005 (accuracy adversary)
- **Logic:** `if candidate.combined_score > union[candidate.slug].combined_score: union[candidate.slug] = candidate`
- **Problem:** Overwrites per-pair score with single slug score. Loses context of which items in the pair had higher scores.
- **Evidence:** Score is pair-specific; slug consolidation is aggregate. Overwrite loses item-level signal.
- **Impact:** MEDIUM — Score consolidation loses information. May affect ranking and merge candidate selection.
- **Action required:** Preserve per-item scores or document score consolidation strategy.

#### TRIAGE-012: Executor writes undefined event kind "handoff"
- **Confidence:** MEDIUM
- **Sources:** ACCURACY-007 (accuracy adversary)
- **Spec statement:** AC14 says "consumed items removed from queue"
- **Actual output:** "Write a `kind: handoff, status: closed-consumed` event to intake-queue.jsonl"
- **Problem:** `kind: handoff` is not defined in any spec. Event schema is undefined.
- **Evidence:** AC14 references queue removal; no mention of `handoff` kind or event schema
- **Impact:** MEDIUM — Event schema violation. Downstream processing may fail if it doesn't recognize `handoff` kind.
- **Action required:** Define event kind (use `closed`, `consumed`, or existing kind) or update AC14 to specify the event schema.

#### TRIAGE-013: total_count and total_processed variables never assigned
- **Confidence:** MEDIUM
- **Sources:** COHERENCE-005 (enumerator)
- **Step 6 template:** References `{{total_count}}` and `{{total_processed}}`
- **Problem:** No Store action assigns these variables in any step
- **Evidence:** Scan of all steps finds no assignment
- **Impact:** MEDIUM — Step 6 output will have unbound variables. Summary incomplete.
- **Action required:** Add Store assignments: "Store {{total_count}} = count of items in intake-queue.jsonl at workflow start" and similar for processed count.

#### TRIAGE-014: Recall test fixture doesn't pass description parameter
- **Confidence:** MEDIUM
- **Sources:** ACCURACY-001 (enumerator)
- **Test fixture:** `items = [_make_item(item_id, item_title) for item_id, item_title, _, _, _, in pairs]`
- **AC5 intent:** Test "recall of relevant items that share any common dimension"
- **Problem:** Item description is never populated; test uses only title for matching
- **Evidence:** Fixture missing description argument; AC5 intends testing against full metadata
- **Impact:** MEDIUM — Test doesn't fully validate AC5. Weaker signal. May miss recall bugs.
- **Action required:** Pass description parameter to `_make_item()` in test fixture.

#### TRIAGE-015: AC15 test verifies prefilter shortlist, not dedup-agent verdict
- **Confidence:** MEDIUM
- **Sources:** DOMAIN-ADVERSARY-002
- **AC15 claim:** "flagged against" (dedup agent verdict from Phase 2)
- **Actual test:** Verifies `"e2e-validator-black-box-hardening" in s1_slugs` (prefilter shortlist from Phase 1)
- **Problem:** Two different concepts tested under same AC
- **Evidence:** "flagged against" (dedup verdict) vs. "prefilter shortlist" (Phase 1 output) are different pipeline stages
- **Impact:** MEDIUM — Test coverage gap. AC15's "flagged against" verdict is untested. Different claim than prefilter.
- **Action required:** Add separate test for dedup-agent "flagged against" verdict from Phase 2 output.

---

### LOW SEVERITY (−1 point each)

#### TRIAGE-016: Section C label wording vs. AC13
- **Confidence:** LOW
- **Issue:** "flagged for Story B (display only, no action available)" vs. AC13's "flagged for Story B — no action available yet"
- **Evidence:** Wording difference; "display only" added, "yet" omitted
- **Impact:** LOW — Minor spec compliance issue. Doesn't affect function.
- **Action required:** Align wording: "flagged for Story B — no action available yet"

#### TRIAGE-017: Evaluation file heading capitalization mismatch
- **Confidence:** LOW
- **Issue:** "Expected behavior" (singular, lowercase) vs. existing convention
- **Evidence:** Style inconsistency with other evaluation files
- **Impact:** LOW — Style only. Doesn't affect function.
- **Action required:** Standardize heading to match project convention.

#### TRIAGE-018: Dedup subagent spawn missing agent type/template
- **Confidence:** LOW
- **Issue:** Spawn declaration lacks agent type or template reference
- **Evidence:** Spawn has no `agent_type` or `template` field
- **Impact:** LOW — Metadata completeness. Doesn't block execution.
- **Action required:** Add agent type metadata if required by agent framework.

#### TRIAGE-019: Sub-steps 2.1–2.4 nested but semantically independent
- **Confidence:** LOW
- **Issue:** Steps 2.1–2.4 are independent phases but nested under Step 2
- **Evidence:** Organizational structure; each sub-step is a distinct phase
- **Impact:** LOW — Clarity only. Doesn't affect function.
- **Action required:** Consider promoting sub-steps to Step 2, 3, 4, 5 level if clearer.

#### TRIAGE-020: Parallel-spawn constraint stated three times
- **Confidence:** LOW
- **Issue:** Constraint repeated in spec (redundant)
- **Evidence:** Same constraint appears in multiple locations
- **Impact:** LOW — Documentation noise. Doesn't affect function.
- **Action required:** Remove duplicate constraint statements.

#### TRIAGE-021: Dedup agent prompt uses `---` delimiters
- **Confidence:** LOW
- **Issue:** Dedup agent PROMPT uses `---` delimiters that conflict with inner `---` item separators
- **Evidence:** Formatting overlap in prompt structure
- **Impact:** LOW — Potential parsing issue if not escaped; likely mitigated by prompt escaping
- **Action required:** Escape inner `---` or use alternate delimiter.

#### TRIAGE-022: intake-queue.jsonl being renamed to practice-ledger.jsonl
- **Confidence:** LOW
- **Issue:** Spec references intake-queue.jsonl; being renamed to practice-ledger.jsonl
- **Evidence:** File rename pending in Momentum redesign; already noted in memory
- **Impact:** LOW — Spec drift; known issue. Update when rename completes.
- **Action required:** Update file reference in spec after rename.

#### TRIAGE-023: REJECT heuristic mentions stale concept
- **Confidence:** LOW
- **Issue:** Step 3 "REJECT heuristic still mentions 'duplicates already in backlog'" (stale after dedup gate)
- **Evidence:** Code comment outdated after dedup filtering
- **Impact:** LOW — Comment clarity only. Doesn't affect function.
- **Action required:** Update comment to reflect current logic.

---

## Score Calculation

**Starting score:** 100

**Deductions:**
- 4 critical findings × −15 = −60
- 5 high findings × −8 = −40
- 6 medium findings × −3 = −18
- 8 low findings × −1 = −8

**Total deduction:** 60 + 40 + 18 + 8 = **126 points**

**Final score:** 100 − 126 = **−26** (clamped to 0 for failing grade)

---

## Grade Assignment

| Grade Range | Grade | Interpretation |
|---|---|---|
| ≥95 | **A / Clean** | Ship-ready; minor polish |
| ≥85 | **B / Good** | Implementation-ready; minor clarifications |
| ≥70 | **C / Fair** | Implementable with known gaps; risks identified |
| ≥50 | **D / Poor** | Implementable with significant risks; gaps block some work |
| <50 | **F / Failing** | Not implementable; critical blockers present |

**Final Grade: F / FAILING**
**Score: 0**

---

## Root Cause Analysis

**Why is this spec failing?**

1. **Algorithm bug** (TRIAGE-001): Missing threshold breaks clustering correctness. Not defensive; breaks the algorithm.

2. **Scope violation** (TRIAGE-002): Story B code in Story A spec. Violates architecture. Must be deferred.

3. **Incomplete step design** (TRIAGE-003): Output template references unassigned variables. Spec is not finished.

4. **Spec contradictions** (TRIAGE-005, 006, 007, 009): Four separate contradictions between goal/statements and step detail. Developer cannot trust spec.

5. **Missing refinement** (TRIAGE-010–015): Medium-severity issues suggest incomplete step-to-step design. Not all edge cases (skip override, score consolidation, event schema) are specified.

**Pattern:** Specification was drafted but not reviewed end-to-end. Critical algorithm details are missing. Step 6 output template is aspirational but unfinished. Scope boundaries (Phase 3 vs. Story B) are not enforced.

---

## Recommendations

**Do NOT proceed to implementation.** The four critical findings will cause functional failures:

1. **TRIAGE-001** (≥0.4 threshold): Fix algorithm to match story spec
2. **TRIAGE-002** (Story B scope): Remove cross-cluster cosine scan or defer to Story B
3. **TRIAGE-003** (Output variables): Assign all Step 6 variables or remove from template
4. **TRIAGE-004** (Fallback promise): Correct fallback statement to match greedy algorithm behavior

**Secondary: Address all high-severity contradictions** (TRIAGE-005 through TRIAGE-009) before implementation. These will confuse developers and lead to inconsistent implementations.

**Tertiary: Fill in medium-severity gaps** (TRIAGE-010–015) during spec refinement.

**Timeline suggestion:**
- **Phase 1 (critical fix):** Address TRIAGE-001, 002, 003, 004 — **2–3 hours**
- **Phase 2 (high-severity clarification):** Address TRIAGE-005–009 — **1–2 hours**
- **Phase 3 (medium-severity completion):** Address TRIAGE-010–015 — **1 hour**
- **Total:** ~4–6 hours to bring spec to "Good" (≥85) grade

After fixes, re-run lighter AVFL pass (2-lens: Structural + Accuracy) to confirm blockers resolved.

---

## Consolidation Metadata

**Validators:**
- Structural Enumerator (SE), Structural Adversary (SA)
- Accuracy Enumerator (AE), Accuracy Adversary (AA)
- Coherence Enumerator (CE), Coherence Adversary (CA)
- Domain Enumerator (DE), Domain Adversary (DA)

**Findings rejected:** 2
- STRUCTURAL-003 (test count hallucination, 548 vs 170 observed)
- STRUCTURAL-005 (AC15 omitted from validator prompt, exists in spec)

**Findings consolidated:** 22 (4 critical, 5 high, 6 medium, 8 low)

**High-confidence findings (paired/multi-validator):** 9
**Medium-confidence findings (single source, evidence confirmed):** 7
**Low-confidence findings (organizational/minor):** 8

**Report generated:** 2026-05-24
**Consolidation phase:** AVFL Phase 8 (complete)
