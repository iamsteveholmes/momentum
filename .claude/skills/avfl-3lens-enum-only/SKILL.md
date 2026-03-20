---
name: avfl-3lens-enum-only
description: BENCHMARK VARIANT — 3-lens AVFL, Enumerator reviewers only. Runs Structural Integrity, Factual Accuracy, and Coherence & Craft lenses with 1 Enumerator per lens (3 agents total). No dual-review, no cross-check confidence tagging. Use this variant when benchmarking AVFL reviewer composition configurations.
---

# AVFL — 3-Lens, Enumerator-Only

Benchmark variant. Active lenses: Structural Integrity, Factual Accuracy, Coherence & Craft. One Enumerator reviewer per lens — no Adversary, no dual-review cross-check.

Read `references/framework.json` for dimension definitions, prompt templates, finding schema, and scoring weights before spawning subagents.

---

## Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `domain_expert` | Yes | — | Role that produced the output and will fix it |
| `task_context` | Yes | — | Brief description of what was produced |
| `output_to_validate` | Yes | — | Content or file path to validate |
| `source_material` | No | null | Ground truth to check against |
| `profile` | No | `full` | `gate`, `checkpoint`, or `full` |
| `validation_focus` | No | null | Narrow which dimensions to prioritize |

---

## Active Lenses (3 of 4) — Enumerator Framing Only

**Lens 1 — Structural Integrity** (`structural`)
Dimensions: structural_validity, completeness, cross_reference_integrity

**Lens 2 — Factual Accuracy** (`accuracy`)
Dimensions: correctness, traceability, logical_soundness

**Lens 3 — Coherence & Craft** (`coherence`)
Dimensions: consistency, relevance, conciseness, clarity, tonal_consistency, temporal_coherence

**Inactive lens:** Domain Fitness
**Inactive framing:** Adversary

---

## Reviewer Framing: Enumerator Only

Each lens gets exactly **1 Enumerator** reviewer. No Adversary. No dual-review cross-check.

**Enumerator** — Systematic and methodical. Derives explicit checks from the dimensions, enumerates them, verifies each in order. Works through content section by section. Produces structured, evidence-backed findings.

Since there is no dual-review, all findings are treated as MEDIUM confidence by default. The consolidator does not apply cross-check logic — simply merge, deduplicate, and score.

---

## Pipeline Execution

### Phase 1: VALIDATE
Spawn in parallel based on profile:
- **gate**: 1 agent, structural lens, Enumerator framing
- **checkpoint**: 1 Enumerator per active lens (1–3)
- **full**: 3 agents — 1 Enumerator for each of the 3 active lenses, all launched in same turn

Use validator prompts from `references/framework.json` → `prompts.validator_system` and `prompts.validator_task`. Apply the Enumerator framing from `references/framework.json` → `dual_review.reviewer_framings.reviewer_a`. Evidence is mandatory on every finding.

### Phase 2: CONSOLIDATE
Sequential. Use `references/framework.json` → `prompts.consolidator` but skip the cross-check confidence tagging step (no dual-review). Merge findings from all lenses, deduplicate, remove findings without evidence, score (start 100: critical −15, high −8, medium −3, low −1), sort by severity.

### Phase 3: EVALUATE
- gate: ≥95 → continue. <95 → GATE_FAILED.
- checkpoint: ≥95 → continue. <95 → 1 fix attempt, then CHECKPOINT_WARNING.
- full: ≥95 → CLEAN. <95 + iterations remaining → fix. Iteration 4 + <95 → MAX_ITERATIONS_REACHED.

### Phase 4: FIX
Use `references/framework.json` → `prompts.fixer`. Fix in severity order. Log each fix. Always validate against original source material. Loop back to Phase 1.

---

## Calibration
Evidence required on every finding. No quotas. No padding. Scope discipline — stay in your lens.

## Reference Files
- `references/framework.json` — Full taxonomy, prompt templates, finding schema, scoring weights.
