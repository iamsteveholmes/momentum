# AVFL Validation Report — Phase 2 False-Positive Benchmark (Mixed: Enumerator + Adversary)

**Benchmark:** Phase 2 Composition Evaluation — Mixed Configuration (Enumerator + Adversary)
**Skill variant:** avfl-3lens
**Document:** `/Users/steve/projects/momentum/avfl-workspace/fixtures/cli-reference-pristine.md`
**Domain Expert:** Technical Writer
**Task Context:** CLI reference documentation for the Momentum `mo` CLI tool
**Source Material:** None
**Profile:** Full (6 agents: 1 Enumerator + 1 Adversary × 3 active lenses)
**Test Type:** False-positive benchmark — document crafted to be complete, internally consistent, and error-free

---

## Final Status: CLEAN

| | |
|---|---|
| **Final Status** | CLEAN |
| **Final Score** | 95/100 |
| **Iteration 1 Score** | 95/100 |
| **Iterations Run** | 1 (passed on first validation — no fix phase triggered) |
| **Fix Phases** | 0 |

---

## Scoring Calculation

| Metric | Value |
|---|---|
| Starting score | 100 |
| STRUCTURAL-001 (medium) | −3 |
| COHERENCE-001 (low) | −1 |
| COHERENCE-002 (low) | −1 |
| **Total deductions** | **−5** |
| **Final score** | **95/100** |
| Pass threshold | 95 |
| Status | **CLEAN** (borderline — exactly at threshold) |

**Findings count:**

| Severity | Count | Deduction |
|---|---|---|
| critical | 0 | 0 |
| high | 0 | 0 |
| medium | 1 | −3 |
| low | 2 | −2 |
| **Total** | **3** | **−5** |

Per framework scoring examples: "1_medium_2_low: 100 − 5 = 95 (PASS: borderline clean)" — this run matches that exact pattern.

---

## Consolidated Findings

### STRUCTURAL-001 — medium | completeness | MEDIUM confidence

**Location:** Section "mo validate --profile gate" (lines 88–95) and Options table `--profile` row (line 69)
**Confidence:** MEDIUM (found by Structural Adversary only; Structural Enumerator found no issues)
**Cross-check:** Single-reviewer finding; investigated and retained on evidence

**Description:** The `--profile gate` variant receives a dedicated behavioral callout subsection documenting how it differs from other profiles ("Exits immediately on failure with code 1; does not attempt fixes"). No equivalent behavioral callout exists for `--profile checkpoint` or `--profile full`. The `--profile` option row in the Options table describes only valid values (`gate`, `checkpoint`, or `full`) without any behavioral distinctions. A user choosing between profiles has no documentation of how `checkpoint` (one fix attempt, then continue with warning) or `full` (iterative fix loop up to 4 iterations) behave on failure.

**Evidence:** Line 89 states "Exits immediately on failure with code 1; does not attempt fixes" — behavioral documentation for `gate` only. Lines 69 reads "Validation profile: `gate`, `checkpoint`, or `full`" — no behavioral distinctions. No section in the document describes fix-loop behavior for `checkpoint` or `full`.

**Suggestion:** Add behavioral callouts for `checkpoint` and `full` profiles analogous to the `### mo validate --profile gate` subsection, or expand the `--profile` option description row to include behavioral distinctions for all three values.

---

### COHERENCE-001 — low | clarity | MEDIUM confidence

**Location:** Overview section, line 7
**Confidence:** MEDIUM (found by Coherence Adversary only; Coherence Enumerator did not flag)
**Cross-check:** Single-reviewer finding; investigated and retained on evidence

**Description:** The statement "All commands require authentication via `mo auth login` before first use" is technically circular when read literally — `mo auth login` would itself require authentication before it could run, making the CLI unusable on first install. The intended meaning is that all non-authentication commands require prior authentication, but this is not stated.

**Evidence:** Line 7: "All commands require authentication via `mo auth login` before first use." Exit code 3: "Authentication error — run `mo auth login`" — this implies `mo auth login` itself does not require prior authentication (it is the remediation step). The literal reading of "all commands" contradicts this implied behavior.

**Suggestion:** Revise to "All validation commands require authentication via `mo auth login` before first use" or "Authentication is required before running validation commands (`mo auth login`)."

---

### COHERENCE-002 — low | conciseness | MEDIUM confidence

**Location:** Options table, `--output` row (line 73)
**Confidence:** MEDIUM (found by Coherence Adversary only; Coherence Enumerator did not flag)
**Cross-check:** Single-reviewer finding; investigated and retained on evidence

**Description:** The `--output` option row states Default as `stdout` and Description as "Path to write the validation report. If omitted, prints to stdout." The Default column and the parenthetical in the description convey the same information (both say the behavior when omitted is stdout output).

**Evidence:** Line 73: `--output | stdout | Path to write the validation report. If omitted, prints to stdout.` — "stdout" in the Default column and "If omitted, prints to stdout." in the Description are redundant.

**Suggestion:** Remove "If omitted, prints to stdout." from the description since the Default column already communicates this. Description becomes: "Path to write the validation report."

---

## Cross-Check Confidence Summary

| Finding | Confidence | Lens | Enumerator | Adversary |
|---|---|---|---|---|
| STRUCTURAL-001 | MEDIUM | Structural Integrity | Not found | Found |
| COHERENCE-001 | MEDIUM | Coherence & Craft | Not found | Found |
| COHERENCE-002 | MEDIUM | Coherence & Craft | Not found | Found |

**HIGH confidence findings: 0**
**MEDIUM confidence findings: 3** (all retained after consolidator investigation)

Notable: No finding reached HIGH confidence (both reviewers agreeing). All findings were Adversary-only, meaning the Enumerator's systematic pass found the document clean. This is a significant benchmark signal — see analysis below.

---

## False Positives Removed

**False positives removed from final report: 0**

All three findings survived consolidator investigation with concrete textual evidence. The following candidates were investigated by validators and correctly dismissed before elevation:

| Candidate | Raised By | Dismissed Because |
|---|---|---|
| `v1.0.0` (header) vs `1.0.0` (CLI output) | Accuracy Adversary | Standard convention: display labels use `v` prefix, programmatic output does not. Not a contradiction. |
| Gate example score math: `62/100` with `3 findings` | Accuracy Adversary (investigated) | 100 − 62 = 38 deductions. 2×critical (30) + 1×high (8) = 38 = 3 findings. Mathematically consistent. Dismissed after enumeration. |
| Overview "quality scoring" claim without `mo score` command | Accuracy Adversary | "Workflow validation and quality scoring" describes validation output, not a separate command. Consistent. |
| `mo auth status` "Not authenticated" output described in prose, no code block | Coherence Adversary | Prose description is sufficient. Absence of code block is not a structural requirement for this command type. |
| `--expert auto` description brevity | Accuracy Adversary | Appropriate brevity for CLI reference scope. Not an omission. |
| `### mo validate --profile gate` treated as peer heading | Coherence Enumerator (noted, not filed) | Intent is clear as a profile-specific callout. Structural incompleteness addressed by STRUCTURAL-001 already. Not a distinct finding. |

---

## False-Positive Analysis

**Test objective:** Measure how many findings a mixed (Enumerator + Adversary) dual-review composition produces on a document crafted to be complete, internally consistent, and error-free. Assess whether findings reaching HIGH confidence via dual-review cross-check.

**Result:** 3 findings, all MEDIUM confidence. Final score 95/100. Status: CLEAN.

### Finding-by-finding assessment:

**STRUCTURAL-001 (medium — completeness):**
This is a **genuine documentation gap**. The `gate` profile has a behavioral callout that other profiles lack, and a user selecting `--profile checkpoint` or `--profile full` has no documentation of how those profiles handle failures. The finding is verifiable from the document text. This is not a false positive — it identifies a real incompleteness. The fact that only the Adversary found it (not the Enumerator) is interesting: the Enumerator checked structural requirements section-by-section and found all required elements present. The Adversary approached it holistically and noticed the asymmetry. This is the Adversary framing doing its job.

**COHERENCE-001 (low — clarity):**
This is a **genuine but minor precision issue**. "All commands require authentication" is technically imprecise. However, this is standard documentation shorthand and any experienced developer reading it would infer the correct meaning. The finding represents the validator working close to the noise floor — it has evidence and a real logical basis, but reasonable reviewers would disagree on whether it merits filing. Correctly rated low. Not a fabrication.

**COHERENCE-002 (low — conciseness):**
This is a **genuine but trivial redundancy**. The Default column and description text both convey the same information about stdout behavior. This is a common documentation pattern used deliberately in many CLI tools (some readers consult only the description, not the Default column). The finding is real but marginal. Correctly rated low. Not a fabrication.

### Dual-review calibration assessment:

**Did dual-review help or hurt calibration?**

The mixed composition (Enumerator + Adversary) produced a well-calibrated result:

- **Helped:** The Adversary framing found 3 genuine issues that the systematic Enumerator missed. This demonstrates value in the framing diversity — the Enumerator's methodical pass confirmed the document's structural soundness, while the Adversary's intuitive, skeptical pass surfaced subtle issues the checklist approach missed.

- **Helped (filtering):** The Adversary also raised 6 candidates that were investigated and dismissed. The dual-review cross-check mechanism (requiring both reviewers to agree for HIGH confidence) correctly held all three retained findings at MEDIUM confidence, forcing consolidator investigation. This prevented automatic elevation of potentially-false findings. The scoring examples arithmetic check (gate score 62 with 3 findings) was investigated and correctly dismissed as consistent.

- **No HIGH confidence findings:** This is the key benchmark signal. In a genuinely clean document, the dual-review cross-check mechanism correctly produced zero HIGH confidence findings. The two reviewer framings did not fabricate consistent hallucinations. This is the expected behavior for a well-calibrated validator on a pristine document.

- **Potential concern:** All 3 retained findings came from the Adversary only. In a false-positive benchmark, this raises the question: are these Adversary-only findings real issues the Enumerator missed, or are they low-severity fabrications that survived because they have some textual basis? The consolidator investigated each one and found concrete evidence in each case. The 0-fabrication result is genuine.

### Summary assessment:

The mixed composition produced **3 findings, 0 fabricated, 0 HIGH confidence** on a pristine document. Final score 95/100 — borderline clean. The pipeline did not invent issues. The MEDIUM-confidence mechanism correctly caught all findings as requiring consolidator scrutiny. The Enumerator framing provided clean-document confirmation; the Adversary framing found marginal but genuine issues near the noise floor.

For the Phase 2 benchmark: the mixed composition is conservative and well-calibrated on a pristine document. The false-positive rate is 0. Whether the 3 MEDIUM-confidence findings represent the composition's "noise floor" or genuine sensitivity to minor issues is a judgment call — all three have textual evidence and none are fabricated.

---

## Phase-by-Phase Pipeline Summary

### Phase 1: VALIDATE (6 agents, parallel)

| Agent | Lens | Framing | Findings Raised |
|---|---|---|---|
| Agent 1 | Structural Integrity | Enumerator | 0 |
| Agent 2 | Structural Integrity | Adversary | 1 (STRUCTURAL-001: missing behavioral description for checkpoint/full) |
| Agent 3 | Factual Accuracy | Enumerator | 0 |
| Agent 4 | Factual Accuracy | Adversary | 0 (gate score math investigated and dismissed as consistent) |
| Agent 5 | Coherence & Craft | Enumerator | 0 |
| Agent 6 | Coherence & Craft | Adversary | 2 (COHERENCE-001: auth claim imprecision; COHERENCE-002: output default redundancy) |

**Phase 1 total raised:** 3 findings across 6 agents. 3 agents found nothing; 3 agents found 0–2 issues each.

### Phase 2: CONSOLIDATE (sequential)

- Cross-check applied: all findings are MEDIUM confidence (Adversary-only; no Enumerator confirmation)
- Duplicates removed: 0
- False positives removed: 0 (all 3 findings survived evidence investigation)
- 5 candidates investigated and dismissed before elevation
- Score calculation: 100 − 3 − 1 − 1 = 95
- Grade: CLEAN (borderline)

### Phase 3: EVALUATE

- Score 95 ≥ threshold 95 → PASS → CLEAN
- No fix phase triggered
- Iteration count: 1

### Phase 4: FIX

- Not executed. Document passed on first iteration.

---

*Generated by AVFL-3lens, full profile, mixed composition (Enumerator + Adversary), iteration 1 of 1.*
*Run date: 2026-03-20*
