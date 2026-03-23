---
name: avfl-3lens
description: BENCHMARK VARIANT — 3-lens Adversarial Validate-Fix Loop. Runs Structural Integrity, Factual Accuracy, and Coherence & Craft lenses (6 agents: 1 Enumerator + 1 Adversary per lens). Use this variant when benchmarking AVFL lens count configurations.
internal: true
---

# AVFL — 3-Lens Configuration (Structural + Accuracy + Coherence)

Benchmark variant of the Adversarial Validate-Fix Loop. Active lenses: **Structural Integrity**, **Factual Accuracy**, and **Coherence & Craft**. All other behavior is identical to the full avfl skill.

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
| `skepticism` | No | `3` | Reviewer intensity: `1` (conservative), `2` (balanced), `3` (aggressive). **Fixed for all iterations — does not decline.** |

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
- **Adversary**: Intuitive, skeptical, holistic search for problems

Cross-check: Both found = HIGH confidence. One found = MEDIUM (consolidator investigates).

---

## Pipeline Execution

### Phase 1: VALIDATE
Spawn in parallel based on profile:
- **gate**: 1 agent, structural lens only
- **checkpoint**: 1 agent per active lens (1–3 lenses)
- **full**: 6 agents — 1 Enumerator + 1 Adversary for each of the 3 active lenses

**Flat skepticism:** Apply the `skepticism` parameter value identically on every iteration — do not step it down. This is the benchmark baseline behavior.

Look up the `skepticism_approach_modifier` and `skepticism_reexamine_rule` for the active skepticism level from `references/framework.json` → `skepticism_levels`. Pass them to every validator.

Use validator prompts from `references/framework.json` → `prompts.validator_system` and `prompts.validator_task`. Evidence is mandatory on every finding.

### Phase 2: CONSOLIDATE
Sequential. Use `references/framework.json` → `prompts.consolidator`.
Tag confidence, merge, deduplicate, investigate MEDIUM findings, score (start 100: critical −15, high −8, medium −3, low −1), sort by severity.

### Phase 3: EVALUATE
- gate: ≥95 → continue. <95 → GATE_FAILED.
- checkpoint: ≥95 → continue. <95 → 1 fix attempt, then CHECKPOINT_WARNING.
- full: ≥95 → CLEAN. <95 + iterations remaining → fix. Iteration 4 + <95 → MAX_ITERATIONS_REACHED.

### Phase 4: FIX
Use `references/framework.json` → `prompts.fixer`. Fix in severity order. Log each fix. Always validate against original source material — never intermediate representations. Loop back to Phase 1.

---

## Calibration
Evidence required on every finding. No quotas. No padding. Scope discipline — stay in your lens.

## Reference Files
- `references/framework.json` — Full taxonomy, prompt templates, finding schema, scoring weights.
