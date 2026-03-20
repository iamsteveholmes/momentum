---
name: avfl-3lens-adv-only
description: BENCHMARK VARIANT — 3-lens AVFL, Adversary reviewers only. Runs Structural Integrity, Factual Accuracy, and Coherence & Craft lenses with 1 Adversary per lens (3 agents total). No dual-review, no cross-check confidence tagging. Use this variant when benchmarking AVFL reviewer composition configurations.
---

# AVFL — 3-Lens, Adversary-Only

Benchmark variant. Active lenses: Structural Integrity, Factual Accuracy, Coherence & Craft. One Adversary reviewer per lens — no Enumerator, no dual-review cross-check.

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
| `skepticism` | No | `3` | Reviewer intensity: `1` (conservative), `2` (balanced), `3` (aggressive). Applied to the Adversary — this benchmark tests whether skepticism changes Adversary behavior |

---

## Active Lenses (3 of 4) — Adversary Framing Only

**Lens 1 — Structural Integrity** (`structural`)
Dimensions: structural_validity, completeness, cross_reference_integrity

**Lens 2 — Factual Accuracy** (`accuracy`)
Dimensions: correctness, traceability, logical_soundness

**Lens 3 — Coherence & Craft** (`coherence`)
Dimensions: consistency, relevance, conciseness, clarity, tonal_consistency, temporal_coherence

**Inactive lens:** Domain Fitness
**Inactive framing:** Enumerator

---

## Reviewer Framing: Adversary Only

Each lens gets exactly **1 Adversary** reviewer. No Enumerator. No dual-review cross-check.

**Adversary** — Intuitive and pattern-aware. Reads holistically, looking for what feels off or inconsistent. Follows hunches, then verifies with evidence. Works across the full artifact, not section by section. The `skepticism` parameter controls how hard the Adversary looks — skepticism=3 means actively following hunches and re-examining before reporting clean; skepticism=1 means reporting only what evidence clearly shows is wrong.

Since there is no dual-review, all findings are treated as MEDIUM confidence by default. The consolidator does not apply cross-check logic — simply merge, deduplicate, and score.

---

## Pipeline Execution

### Phase 1: VALIDATE
Spawn in parallel based on profile:
- **gate**: 1 agent, structural lens, Adversary framing
- **checkpoint**: 1 Adversary per active lens (1–3)
- **full**: 3 agents — 1 Adversary for each of the 3 active lenses, all launched in same turn

Look up the `skepticism_approach_modifier` and `skepticism_reexamine_rule` for the active `skepticism` level from `references/framework.json` → `skepticism_levels`. Pass them to each Adversary along with the `stage_completeness_instruction` from `references/framework.json` → `stage_definitions[stage]`.

Use validator prompts from `references/framework.json` → `prompts.validator_system` and `prompts.validator_task`. Apply the Adversary framing from `references/framework.json` → `dual_review.reviewer_framings.reviewer_b`. Evidence is mandatory on every finding.

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
Evidence required on every finding. Adversary framing does not mean inventing problems — hunches must be verified with evidence before reporting. No quotas. No padding.

## Reference Files
- `references/framework.json` — Full taxonomy, prompt templates, finding schema, scoring weights.
