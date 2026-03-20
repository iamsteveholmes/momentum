---
name: avfl-declining
description: BENCHMARK VARIANT — 3-lens AVFL with auto-declining skepticism. Identical to avfl-3lens (mixed composition, Structural + Accuracy + Coherence) except skepticism automatically steps down each fix iteration: starts at the `skepticism` parameter, decrements by 1 (min 1) each subsequent iteration. Use this variant when benchmarking declining vs flat skepticism behavior across the fix loop.
---

# AVFL — Declining Skepticism Configuration

Benchmark variant of the Adversarial Validate-Fix Loop. Active lenses: **Structural Integrity**, **Factual Accuracy**, and **Coherence & Craft**. Mixed composition (1 Enumerator + 1 Adversary per lens). **Key difference from avfl-3lens: skepticism automatically declines each iteration.**

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
| `stage` | No | `final` | Artifact maturity: `draft`, `checkpoint`, or `final`. Controls what absence counts as a gap |
| `skepticism` | No | `3` | Starting reviewer intensity. **Auto-declines each iteration: iter 1 = skepticism, iter 2 = max(skepticism−1, 2), iter 3+ = 2.** Floor is 2 — skepticism=1 eliminates framing differentiation entirely. |

---

## Active Lenses (3 of 4)

**Lens 1 — Structural Integrity** (`structural`)
Mechanical verification. Check every field, reference, and required element.
Dimensions: structural_validity, completeness, cross_reference_integrity

**Lens 2 — Factual Accuracy** (`accuracy`)
Fact-checker. Verify every claim against source material.
Dimensions: correctness, traceability, logical_soundness

**Lens 3 — Coherence & Craft** (`coherence`)
Editor. Read holistically as the intended audience would. Focus on whether the content works as a unified whole.
Dimensions: consistency, relevance, conciseness, clarity, tonal_consistency, temporal_coherence

**Inactive lens:** Domain Fitness

---

## Dual-Reviewer Framings

Each active lens gets 2 reviewers — total 6 agents for full profile:
- **Enumerator**: Systematic, section-by-section enumeration of checks
- **Adversary**: Intuitive, pattern-aware, holistic reading

Cross-check: Both found = HIGH confidence. One found = MEDIUM (consolidator investigates).

---

## Pipeline Execution

### Iteration Tracking

At the start of execution, initialize:
- `iteration = 1`
- `initial_skepticism = skepticism` (the parameter value, default 3)

Before each Phase 1, compute the **effective skepticism** for this iteration:
- Iteration 1: `effective_skepticism = initial_skepticism`
- Iteration 2: `effective_skepticism = max(initial_skepticism - 1, 2)`
- Iteration 3+: `effective_skepticism = 2`

Floor is **2**, not 1. Phase 2.6 benchmarking showed that skepticism=1 makes Enumerator and Adversary framings produce identical output — dual-review yields no cross-check value below skepticism=2.

Look up the corresponding `approach_modifier` and `reexamine_rule` from `references/framework.json` → `skepticism_levels[effective_skepticism]`. Pass them to every validator for this iteration.

**Rationale:** Iteration 1 casts a wide net to find all issues. Subsequent iterations verify fixes and catch regressions at balanced intensity — they should not pursue fresh hunches (that's iteration 1's job) but should still differentiate Enumerator from Adversary readings.

### Phase 1: VALIDATE

Spawn in parallel based on profile:
- **gate**: 1 agent, structural lens only
- **checkpoint**: 1 agent per active lens (1–3 lenses)
- **full**: 6 agents — 1 Enumerator + 1 Adversary for each of the 3 active lenses

Each validator receives: their lens definition, their reviewer framing, and all parameters including the **effective_skepticism** for this iteration, the corresponding approach_modifier and reexamine_rule, and the stage_completeness_instruction from `references/framework.json` → `stage_definitions[stage]`.

Use validator prompts from `references/framework.json` → `prompts.validator_system` and `prompts.validator_task`. Evidence is mandatory on every finding.

### Phase 2: CONSOLIDATE

Sequential. Use `references/framework.json` → `prompts.consolidator`.
Tag confidence, merge, deduplicate, investigate MEDIUM findings, score (start 100: critical −15, high −8, medium −3, low −1), sort by severity.

### Phase 3: EVALUATE

- gate: ≥95 → continue. <95 → GATE_FAILED.
- checkpoint: ≥95 → continue. <95 → 1 fix attempt, then CHECKPOINT_WARNING.
- full: ≥95 → CLEAN. <95 + iterations < 4 → fix. iteration = 4 + <95 → MAX_ITERATIONS_REACHED.

### Phase 4: FIX

Use `references/framework.json` → `prompts.fixer`. Fix in severity order. Log each fix. Produce the complete corrected output. Always validate against original source material — never intermediate representations.

After fixing, increment `iteration` by 1, then loop back to Phase 1 with the updated output and the newly computed effective_skepticism.

---

## Calibration

Evidence required on every finding. No quotas. No padding. Scope discipline — stay in your lens.

## Reference Files

- `references/framework.json` — Full taxonomy, prompt templates, finding schema, scoring weights.
