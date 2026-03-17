# Validate-Fix-Loop: Handoff to Momentum

**Goal:** Build the validate-fix-loop framework into a reusable BMAD skill that any workflow can invoke.

## What Was Built

A JSON workflow document (`validate-fix-loop.json`) that defines a research-backed validation framework with three components:

1. **A 15-dimension validation taxonomy** (4 tiers, from universal to domain-specific) that tells validators WHAT to look for while letting the domain determine HOW
2. **Three validation profiles** (gate/checkpoint/full) for different intensity levels
3. **A dual-reviewer system** where two independent reviewers with different framings cross-check each other's findings

## Files to Transfer

| File | Purpose |
|------|---------|
| `_bmad/core/resources/validate-fix-loop.json` | The framework document (v3). This is the primary artifact. |
| `_bmad/core/resources/validate-fix-loop-references.md` | Research references with links and key findings. |
| `_bmad/core/resources/validate-fix-loop-handoff.md` | This file. |

## Architecture at a Glance

### Dimension Taxonomy (what to validate)

Organized into 4 tiers. Validators derive specific checks from these based on domain context.

- **Tier 1 — Universal** (always apply): Correctness, Consistency, Completeness, Relevance, Structural Validity
- **Tier 2 — Compositional** (content with internal structure): Logical Soundness, Traceability, Conciseness, Clarity
- **Tier 3 — Contextual** (content in a larger ecosystem): Cross-Reference Integrity, Temporal Coherence, Tonal Consistency, Convention Adherence
- **Tier 4 — Domain-Specific** (requires expertise): Domain Rule Compliance, Fitness for Purpose

### Validation Profiles (how intensely to validate)

| Profile | Agents | Dual Review | Fix Loop | Use Case |
|---------|--------|-------------|----------|----------|
| **Gate** | 1 (structural lens) | No | No — pass/fail/halt | Input checks, format transitions, middle pipeline steps |
| **Checkpoint** | 1 per active lens (2-4) | No | 1 fix attempt, no loop | After first interpretation step, penultimate step, irreversible decisions |
| **Full** | 2 per lens (up to 8) | Yes | Up to 4 iterations | Final deliverables, critical outputs |

### Dual-Reviewer System (full profile only)

Two reviewers per lens with different framings:
- **Enumerator**: Systematic, mechanical, section-by-section
- **Adversary**: Intuitive, skeptical, holistic

Cross-check during consolidation:
- Both found it → HIGH confidence (almost certainly real)
- Only one found it → MEDIUM confidence (consolidator investigates)

Research basis: Meta-Judge (2025) showed 2 agents + cross-check = 77.26% accuracy vs 68.89% single-agent. Adding a 3rd agent decreased performance.

### Four Validation Lenses (parallel execution)

Dimensions are grouped by mindset, not by dimension tier:

1. **Structural Integrity** — mechanical verification (structural_validity, completeness, cross_reference_integrity)
2. **Factual Accuracy** — fact-checking against sources (correctness, traceability, logical_soundness)
3. **Coherence & Craft** — editorial holistic reading (consistency, relevance, conciseness, clarity, tonal_consistency, temporal_coherence)
4. **Domain Fitness** — domain expert evaluation (domain_rule_compliance, convention_adherence, fitness_for_purpose)

### Staged Application (multi-step workflows)

The "bookend + critical gates" pattern:

```
INPUT ──── gate (is source material accessible and complete?)
FIRST INTERPRETATION ──── checkpoint (did we get the interpretation right?)
MIDDLE STEPS ──── gate (structural sanity only)
PENULTIMATE STEP ──── checkpoint (late-stage errors are 3.5x more damaging)
FINAL OUTPUT ──── full (dual-reviewer, fix loop, all dimensions)
```

Which dimensions are prioritized at each stage varies by domain. The document includes illustrative examples for research, structured data, narrative content, code implementation, and document authoring — not as prescriptive recipes but as illustrations of how emphasis shifts.

### Scoring

- Scale: 0-100, starting at 100
- Severity deductions: Critical -15, High -8, Medium -3, Low -1
- Pass threshold: 95 (clean)
- Max fix loop iterations: 4

### Calibration

Key principles to prevent both missed issues and hallucinated findings:
- Every finding requires concrete evidence (quote the wrong thing)
- No minimum finding quotas (that causes manufactured findings)
- Method over attitude (systematic verification, not hostility)
- Conservative flagging (no evidence = no finding)
- Scope discipline (stay in your lens)

## Suggested Skill Design for Momentum

### Invocation Options

The skill should support three invocation patterns:

1. **Standalone** — validate a specific output: `/validate --profile full --expert analyst --context "market research report"`
2. **Inline from workflows** — workflows reference the framework and specify profile at each stage
3. **As a rule** — CLAUDE.md or project-context.md references the framework so agents know to apply it

### Parameters the Skill Needs

- `domain_expert` (required) — who validates/fixes
- `task_context` (required) — what was produced
- `output_to_validate` (required) — the artifact
- `source_material` (optional) — ground truth to check against
- `profile` (optional, default: full) — gate/checkpoint/full
- `validation_focus` (optional) — narrow which dimensions to prioritize

### Key Implementation Considerations

1. **Sub-agent orchestration** — full profile needs up to 8 parallel sub-agents. Checkpoint needs up to 4. Gate needs 1.
2. **Source material passthrough** — the framework emphasizes passing original source material through the entire pipeline, not lossy intermediate representations.
3. **The dimension taxonomy lives in the JSON** — validators read their assigned dimensions and derive domain-appropriate checks. The skill doesn't need to maintain separate checklists per domain.
4. **Consolidation is where the intelligence is** — deduplication, cross-check confidence tagging, false positive removal, and scoring all happen in consolidation. This is the step that prevents garbage findings from reaching the fixer.
5. **The fix loop only applies to full profile** — gate is pass/fail, checkpoint gets one fix attempt. Only full loops.

## Research Summary

The design is grounded in published research (full references in `validate-fix-loop-references.md`):

- **Dual review**: 2 independent reviewers with different framings improve accuracy ~12% absolute. 3rd reviewer hurts. (Meta-Judge 2025, PoLL 2024)
- **Error propagation**: 73% chance a single error causes downstream failure. At 90% per-step × 8 steps = 43% overall accuracy. (Huang 2023)
- **Late-stage fragility**: Errors at step N-1 are 3.5x more damaging than at step 2 due to "semantic commitment." (ASCoT 2025)
- **Staged validation**: Step-level feedback is >8% more accurate and 1.5-5x more compute-efficient than outcome-only, but only when focused on steps that matter. (Process Reward Models survey)
- **Dimension taxonomy**: Synthesized from ISO 25010, Wang & Strong, Azure AI Eval, DeepEval, and existing BMAD validation patterns.
