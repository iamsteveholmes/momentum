# AVFL Validation Report — CLI Reference Documentation (Pristine False-Positive Benchmark)

## Benchmark Context

**Variant:** avfl-3lens-adv-only (Adversary-only, no Enumerator, no dual-review)
**Purpose:** Phase 2 false-positive benchmark — document was carefully crafted to be complete, internally consistent, and error-free. Measures how many findings the adversary-only composition produces on a pristine document.
**Date:** 2026-03-20
**Iteration:** 1 of 1 (passed on first pass — no fix loop triggered)

## Run Parameters

| Parameter | Value |
|---|---|
| domain_expert | technical writer |
| task_context | CLI reference documentation for the Momentum `mo` CLI tool |
| profile | full |
| source_material | none |
| output_to_validate | `avfl-workspace/fixtures/cli-reference-pristine.md` |

---

## Final Result

| Field | Value |
|---|---|
| **Final Status** | CLEAN |
| **Final Score** | 98/100 |
| **Pass Threshold** | 95 |
| **Iterations** | 1 |
| **Fix Loop Triggered** | No |
| **False Positives Removed in Consolidation** | 0 |

---

## Scoring Calculation

Starting score: 100

| Finding | Severity | Deduction |
|---|---|---|
| STRUCTURAL-001 | low | −1 |
| COHERENCE-001 | low | −1 |
| **Total** | | **−2** |

**Final score: 100 − 2 = 98**

---

## Findings Summary

| Severity | Count |
|---|---|
| critical | 0 |
| high | 0 |
| medium | 0 |
| low | 2 |
| **total** | **2** |

---

## All Findings

### STRUCTURAL-001

| Field | Value |
|---|---|
| **Severity** | low |
| **Dimension** | structural_validity |
| **Lens** | Structural Integrity |
| **Confidence** | MEDIUM (adversary-only variant — no dual-review) |
| **Location** | Validation Commands section — `### mo validate --profile gate` heading |

**Description:** The heading `### mo validate --profile gate` presents a usage variant (passing `--profile gate` as an option) at the same heading level as the main command `### mo validate`. Within the document's established pattern, h3 headings under `## Validation Commands` denote distinct commands. The `--profile gate` section is not a distinct command — it is an illustration of the `--profile` option already documented in the options table. This creates a structural ambiguity about the CLI's command surface.

**Evidence:** `### mo validate` and `### mo validate --profile gate` both appear as h3-level headings under `## Validation Commands`. The `--profile` flag is already documented as an option in the options table under `### mo validate` with permitted values `gate`, `checkpoint`, or `full`. There is no `### mo validate --profile checkpoint` or `### mo validate --profile full` companion section, confirming this is not a consistent sub-command pattern but a one-off illustrative block incorrectly structured as a peer command heading.

**Suggestion:** Fold the gate profile example into the main `### mo validate` entry as a named usage example (e.g., under a `**Usage examples:**` subsection), or rename the heading to `#### Gate profile example` to signal it is subordinate to the main command entry.

---

### COHERENCE-001

| Field | Value |
|---|---|
| **Severity** | low |
| **Dimension** | clarity |
| **Lens** | Coherence & Craft |
| **Confidence** | MEDIUM (adversary-only variant — no dual-review) |
| **Location** | Validation Commands → `mo validate` — command description |

**Description:** The acronym "AVFL" is used in the first substantive description of the `mo validate` command without expansion or prior definition anywhere in the document. A CLI reference is often the first document a user reads when learning the tool. Undefined acronyms create friction for users who have not read companion conceptual documentation.

**Evidence:** "Runs AVFL validation on a file or directory." (first line of the `### mo validate` section). The term "AVFL" does not appear in the document header, Overview, or anywhere else in the document where it might be defined. The Overview describes the CLI's purpose without using or defining "AVFL."

**Suggestion:** Expand on first use: "Runs AVFL (Automated Validation and Fix Loop) validation on a file or directory." Or add a cross-reference: "Runs AVFL validation on a file or directory. See [AVFL Overview] for a description of the validation framework."

---

## False Positive Analysis

**False positives removed during consolidation: 0**

Each finding is assessed below for whether it is a genuine issue or a validator hallucination.

### STRUCTURAL-001 — Assessment: Genuine, defensible

The structural inconsistency is verifiable from the document itself. The heading pattern creates a real ambiguity: does `### mo validate --profile gate` describe a distinct CLI command or a usage example? The options table already documents `--profile gate` as an option variant, yet it receives a peer-level section heading to `### mo validate`. The absence of companion headings for `--profile checkpoint` and `--profile full` confirms this is not an intentional pattern. The finding is low severity (the document is usable; no user will be blocked) but it is a genuine structural inconsistency, not an invented one.

**Verdict: True positive. Low severity appropriately assigned.**

### COHERENCE-001 — Assessment: Genuine, low-stakes

The acronym gap is objectively verifiable. "AVFL" appears once, is never expanded, and is not defined in the Overview or any other section. Whether this matters depends on the audience and whether a companion glossary exists — but within the scope of this reference document in isolation, the finding is real. It is not a stylistic preference or an invented problem. Flagging an undefined acronym in a standalone reference document is standard technical writing practice.

**Verdict: True positive. Low severity appropriately assigned.**

---

## Phase-by-Phase Pipeline Summary

### Phase 1: VALIDATE (parallel, 3 agents)

Three Adversary reviewers ran in parallel, one per active lens. Profile is `full` so all three active lenses ran. No Enumerator framing (adv-only variant). All findings treated as MEDIUM confidence by default.

**Lens 1 — Structural Integrity** (dimensions: structural_validity, completeness, cross_reference_integrity)

- structural_validity: 1 finding (STRUCTURAL-001, low) — option variant presented as peer-level command heading
- completeness: CLEAN — all required CLI reference sections present (overview, installation, auth, validation, scoring, config, error messages)
- cross_reference_integrity: CLEAN — all internal references consistent: `~/.mo/credentials.json` referenced consistently in auth login and auth logout; `mo auth login` referenced consistently in exit codes and error table; version numbers consistent throughout

**Lens 2 — Factual Accuracy** (dimensions: correctness, traceability, logical_soundness)

- correctness: CLEAN — all verifiable claims match internally: scoring weights (critical −15, high −8, medium −3, low −1), pass threshold (95), starting score (100), profile values (gate/checkpoint/full), file paths, version number
- traceability: N/A — source_material: none; all claims are self-contained in a self-describing reference document
- logical_soundness: CLEAN — authentication flow is logically consistent; scoring deduction system is arithmetically correct; exit code assignments are internally consistent with profile descriptions

**Lens 3 — Coherence & Craft** (dimensions: consistency, relevance, conciseness, clarity, tonal_consistency, temporal_coherence)

- consistency: CLEAN — terminology stable throughout; backtick code formatting applied consistently; command description style uniform
- relevance: CLEAN — no scope drift; all content directly serves CLI reference purpose
- conciseness: CLEAN — no padding, no verbose prose, no redundant qualifiers; tables used efficiently
- clarity: 1 finding (COHERENCE-001, low) — "AVFL" acronym unexpanded on first use
- tonal_consistency: CLEAN — technical reference register maintained throughout; no marketing language or conversational filler
- temporal_coherence: CLEAN — document versioned as v1.0.0 released 2026-03-01; no anachronisms, no references to deprecated APIs or future features

### Phase 2: CONSOLIDATE (sequential)

- Received findings: 1 from Lens 1, 0 from Lens 2, 1 from Lens 3
- Dual-review cross-check: skipped (adv-only variant; all findings MEDIUM confidence by default)
- Deduplication: no overlaps between lenses
- Evidence check: both findings include mandatory evidence; both pass
- False positives removed: 0
- Score calculation: 100 − 1 − 1 = 98

### Phase 3: EVALUATE

- Score: 98
- Pass threshold: 95
- Result: 98 ≥ 95 → **PASS → EXIT CLEAN**

### Phase 4: FIX

Not triggered. Score passed threshold on iteration 1.

---

## Benchmark Interpretation

The pristine fixture scored **98/100 CLEAN** in a single pass with no fix loop required. The adversary-only composition produced 2 findings on a document designed to have none.

**Finding breakdown:**
- 0 critical, 0 high, 0 medium, 2 low
- Both findings are low-severity, evidence-backed, and defensible
- 0 findings were hallucinated or manufactured
- 0 findings were discarded during consolidation

**False positive rate: 0 of 2 findings were false positives.** The adversary framing did not cause the validators to invent problems. Both findings represent genuine (if minor) issues in the fixture that were not caught during document creation:

1. STRUCTURAL-001 identifies a real heading-level inconsistency in the Validation Commands section — an option variant incorrectly presented as a peer command heading.
2. COHERENCE-001 identifies an undefined acronym that is standard to flag in technical writing review.

**Calibration quality:** The adversary agents showed appropriate restraint. Multiple candidate findings were investigated and rejected for insufficient evidence (exit code CHECKPOINT_WARNING omission — no source material to confirm CLI behavior; "All commands require authentication" logical tension — standard documentation convention; overview "workflow validation" phrasing — ambiguous but not wrong). The validators did not pad findings to appear thorough.

**Score interpretation for Phase 2 benchmark:** A score of 98 on a document intended to be pristine indicates the adversary-only composition has a low false-positive tendency. The 2-point deduction reflects two genuine low-severity findings in the fixture, not validator noise. The composition appears well-calibrated for a false-positive benchmark.
