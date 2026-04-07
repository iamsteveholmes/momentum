---
name: avfl
description: "Adversarial Validate-Fix Loop — multi-agent validation catching errors, hallucinations, and quality issues via parallel lenses and iterative fix."
model: claude-opus-4-6
effort: high
---

# AVFL — Adversarial Validate-Fix Loop

A multi-phase validation pipeline with parallel reviewers, cross-checked findings, and an iterative fix loop.

The framework is grounded in research: dual reviewers with different framings improve accuracy ~8 percentage points absolute over single-agent validation (Meta-Judge 2025). Staged validation is 8%+ more accurate and 1.5–5× more compute-efficient than outcome-only evaluation. Late-stage errors are 3.5× more damaging than early ones (ASCoT 2025) — which is why profile selection matters.

**This SKILL.md is the orchestration layer.** Before spawning your first subagents, read `references/framework.json` — it contains the complete dimension taxonomy, validator/consolidator/fixer prompt templates, finding schema, scoring weights, and usage examples. Use those prompts verbatim when instructing subagents.

---

## Parameters

Collect these before starting. If any are missing, ask before proceeding.

| Parameter | Required | Default | Description |
|---|---|---|---|
| `domain_expert` | Yes | — | The agent role that produced the output and will fix it (e.g., "technical writer", "software engineer", "analyst") |
| `task_context` | Yes | — | Brief description of what was produced (e.g., "market research report", "PRD section", "JSON config") |
| `output_to_validate` | Yes | — | Single document mode: content or file path. Corpus mode (`corpus: true`): array of file paths |
| `source_material` | No | null | Ground truth to check against. Pass original source through the entire pipeline — never let intermediate steps compress it |
| `profile` | No | `full` | `gate`, `checkpoint`, `full`, or `scan` |
| `stage` | No | `final` | Artifact maturity: `draft`, `checkpoint`, or `final`. Controls what absence counts as a gap — see Stage section below |
| `corpus` | No | `false` | When `true`, validates multiple documents together. `output_to_validate` becomes an array of file paths. Activates cross-document dimensions and corpus prompt templates. All validators receive all files. |
| `authority_hierarchy` | No | `null` | Ordered array of file paths (index 0 = highest authority). Only used when `corpus: true`. Fixer uses this to resolve cross-document contradictions — modifies lower-authority files to match higher-authority files, annotating fixes with `resolved_by: authority_hierarchy`. When absent, contradictions are flagged as `unresolved_contradiction`. |

---

## Corpus Mode

When `corpus: true` is set, AVFL validates a set of related documents together rather than a single artifact.

**What changes in corpus mode:**
- `output_to_validate` accepts an array of file paths (e.g., `[doc-a.md, doc-b.md, doc-c.md]`)
- All validators receive ALL corpus files in their prompts — no distribution across validators
- Two additional corpus-only dimensions activate: `cross_document_consistency` (coherence lens) and `corpus_completeness` (structural lens)
- Finding `location` uses `{filename}:{section}` format (e.g., `architecture.md:Data Model`)
- Validators use the corpus prompt templates from `references/framework.json` → `prompts.validator_system_corpus` and `prompts.validator_task_corpus`
- Consolidator uses `prompts.consolidator_corpus` (deduplication treats multi-file contradictions as one finding)
- Fixer uses `prompts.fixer_corpus` — produces per-file output blocks, one per file in the corpus

**What does NOT change:**
- Profiles (gate/checkpoint/full/scan) work identically
- Scoring weights and thresholds are unchanged
- All existing single-document dimensions still apply within each file
- The dual-reviewer architecture is unchanged (full profile: Enumerator + Adversary per lens)

**Per-file output block format** (corpus fixer output):
```
### File: {filepath}
{complete corrected content for this file}
```

---

## Stage

Controls what absence counts as a finding — the maturity expectations for the artifact at the time of validation. Independent of `profile`.

| Value | Completeness expectation | When to use |
|---|---|---|
| `draft` | Expected gaps are not findings. Evaluate only what IS present — is it coherent and internally consistent? Do not penalize for sections not yet written. | Early-stage artifacts where incompleteness is intentional |
| `checkpoint` | Major sections must be present. Implementation details may still be incomplete. Flag major structural gaps; don't penalize missing fine-grained specs. | Mid-workflow artifacts where primary concerns should be addressed |
| `final` | All required sections must be complete. Flag all gaps. | Deliverables intended for handoff, human consumption, or downstream systems |

Default: `final`. When invoking AVFL from within a skill workflow, set `stage` to match the artifact's maturity at that workflow step.

---

## Skepticism

Controls how intensely reviewers search and their default assumption. The reviewer style describes HOW they read; skepticism describes HOW HARD they look.

| Level | Label | Approach | Re-examine if clean |
|---|---|---|---|
| `high` (3) | Aggressive | Look for what feels off. Follow hunches, then verify. Default assumption: something might be wrong. | Yes — once |
| `low` (2) | Balanced | Follow leads that seem promising. Give benefit of the doubt on borderline cases. | Optional |

**Skepticism is not a user parameter.** It is hardcoded by the pipeline:
- Iteration 1: `high` (3) — cast a wide net, maximize recall
- Iteration 2+: `low` (2) — verify fixes, catch regressions, don't re-litigate settled issues

Floor is `2`. Benchmarking showed skepticism=1 collapses Enumerator and Adversary to identical output, eliminating dual-review value entirely.

---

## Profiles

### gate
**When to use:** Input validation, format transitions, sanity checks between pipeline steps — anywhere you need a fast structural pass before continuing.

**How it runs:** 1 agent, structural lens only. No fix loop.
- Pass (score ≥ 95) → continue workflow
- Fail → halt and report GATE_FAILED. Cannot proceed until resolved.

### checkpoint
**When to use:** After the first interpretation step (errors here have 73% downstream propagation rate), at penultimate steps (3.5× more damaging than early errors), or after any irreversible narrowing decision.

**How it runs:** 1 agent per active lens (2–3 lenses relevant to the decision point). 1 fix attempt if issues found, then continue with CHECKPOINT_WARNING regardless.

### full
**When to use:** Final deliverables, high-stakes content, anything consumed by humans or downstream systems without further review.

**How it runs:** 2 agents per lens × 4 lenses = up to 8 parallel reviewers. Iterative fix loop (max 4 iterations, pass threshold 95/100).

### scan
**When to use:** Post-sprint-merge quality gate, or any context where discovery quality matters more than resolution throughput. The output is a structured findings list for handoff to a resolution team.

**How it runs:** 2 agents per lens × 4 lenses = up to 8 parallel reviewers (identical to full). Single pass at maximum skepticism (level 3). No fix loop — Phase 3 (EVALUATE) exits before reaching Phase 4 (FIX). The consolidated findings list is the final output. Output format is `structured_handoff`: findings ordered by severity then confidence with all required fields for team consumption.

**Composes with corpus mode:** `profile: scan, corpus: true` runs maximum-intensity corpus validation with no fix loop — the two features are orthogonal and compose at call time.

---

## The Four Validation Lenses

Validators derive specific checks from their assigned dimensions based on the domain — the dimensions define WHAT to look for; the domain determines HOW.

**Lens 1 — Structural Integrity** (`structural`)
Mindset: Mechanical verification. Systematic, exhaustive, literal. Check every field, reference, and required element section by section.
Dimensions: structural_validity, completeness, cross_reference_integrity

**Lens 2 — Factual Accuracy** (`accuracy`)
Mindset: Fact-checker. Compare every claim against source material. Trust nothing — verify everything against ground truth.
Dimensions: correctness, traceability, logical_soundness

**Lens 3 — Coherence & Craft** (`coherence`)
Mindset: Editor. Read holistically as the intended audience would. Focus on whether the content works as a unified whole.
Dimensions: consistency, relevance, conciseness, clarity, tonal_consistency, temporal_coherence

**Lens 4 — Domain Fitness** (`domain`)
Mindset: Domain expert. Apply specialized knowledge — would a practitioner in this field accept this output and find it useful?
Dimensions: domain_rule_compliance, convention_adherence, fitness_for_purpose

For full dimension definitions, questions, common failure modes, and examples, see `references/framework.json` → `dimension_taxonomy`.

---

## Dual-Reviewer Framings (full and scan profiles)

Each lens gets two reviewers with deliberately different reading styles. The diversity of approach is the mechanism — same-prompt reviewers capture far less benefit.

**Enumerator** — Systematic and methodical. Derives explicit checks from the dimensions, enumerates them, verifies each in order. Works through content section by section.

**Adversary** — Intuitive and pattern-aware. Reads holistically, looking for what feels off or inconsistent. Follows hunches, then verifies with evidence. Works across the full artifact, not section by section.

These styles describe HOW each reviewer reads. `skepticism` controls HOW HARD both reviewers look — it applies equally to both framings and is the primary lever for adjusting aggressiveness across iterations or workflow stages.

Cross-check confidence during consolidation:
- Both found it → **HIGH confidence** — almost certainly a real issue. Keep with highest severity from either reviewer.
- Only one found it → **MEDIUM confidence** — consolidator investigates against source material. Keep if evidence supports; discard if it appears to be a reviewer hallucination.

---

## Team Composition

All AVFL subagents are spawned as **individual agents** via the Agent tool. TeamCreate is never used in AVFL — every subagent is an independent spawn.

| Role | Spawning | Concurrency | Notes |
|---|---|---|---|
| Validator (Enumerator) | `individual-agent` | parallel | All validators in one message turn |
| Validator (Adversary) | `individual-agent` | parallel | All validators in one message turn |
| Consolidator | `individual-agent` | sequential | Runs after **all** validators complete |
| Fixer | `individual-agent` | sequential | Runs after consolidator completes |

**Validator fixer agent is not missing.** Every role in the pipeline must be present. If a fix loop runs, the Fixer is required — it cannot be omitted. The Fixer role is defined in the Role Configuration table below (under Pipeline Execution) and must always be spawned when Phase 4 is entered.

Model and effort assignments per role are specified in the Role Configuration table. This section declares spawning mode; it does not duplicate the model/effort values.

---

## Pipeline Execution

Read `references/framework.json` → `prompts` for the exact prompt templates to give each subagent type. Use those templates — they encode the calibration rules that make findings structured and evidence-backed.

### Role Configuration (Benchmarked Defaults)

Each role has a prescribed model and effort level derived from Phase 4 benchmarking (36 runs across 3 models × 3 effort levels × all roles). Use these — they represent measured optima, not guesses.

| Role | Model | Effort | Spawning | Concurrency | Sub-skill path | Rationale |
|---|---|---|---|---|---|---|
| Enumerator validator | `sonnet` | `medium` | `individual-agent` | parallel | `sub-skills/validator-enum` | Reliable recall; no false-pass risk |
| Adversary validator | `opus` | `high` | `individual-agent` | parallel | `sub-skills/validator-adv` | Best severity calibration; critical findings correctly classified |
| Consolidator | `haiku` | `low` | `individual-agent` | sequential (after all validators) | `sub-skills/consolidator` | Fully invariant across all model/effort combos — cheapest is sufficient |
| Fixer | `sonnet` | `medium` | `individual-agent` | sequential (after consolidator) | `sub-skills/fixer` | Handles both mechanical and generative fixes |

**How to apply:** When spawning subagents via the Agent tool, set the `model` parameter explicitly (`"sonnet"`, `"opus"`, `"haiku"`). Point the subagent at the appropriate sub-skill path — the skill carries the `effort` frontmatter that overrides the session level.

**Do not use Haiku for Enumerator validators.** Benchmarking showed Haiku enum-medium produces false-pass scores (92/100 while missing a critical architectural contradiction) — the most dangerous failure mode.

**Do not use Sonnet for Adversary validators.** Benchmarking showed Sonnet Adversary systematically downgrades critical findings to high severity across all effort levels — a calibration defect that causes the pipeline to underreport severity.

---

### Phase 1: VALIDATE

Spawn validator subagents **in parallel** based on the profile. Set `model` and skill path per the Role Configuration table above.

- **gate:** 1 subagent — Enumerator framing, structural lens only. Model: `sonnet`.
- **checkpoint:** 1 subagent per active lens (2–3 lenses relevant to the step). Enumerator framing. Model: `sonnet`.
- **full:** 8 subagents total — 1 Enumerator + 1 Adversary per lens × 4 lenses, all in one turn. Enumerator: `sonnet`/medium. Adversary: `opus`/high.
- **scan:** Identical to full — 8 subagents total, same model/effort configuration. The difference is downstream: scan never enters Phase 4.

Pass the current skepticism value explicitly in each subagent prompt: `high` (3) on iteration 1, `low` (2) on all subsequent iterations.

**Single-document mode (`corpus: false` or omitted):** Each validator receives: lens definition, reviewer framing, skepticism level, and all parameters. Use `prompts.validator_system` and `prompts.validator_task` from `references/framework.json`. Finding locations use standard section/line format.

**Corpus mode (`corpus: true`):** Each validator receives ALL corpus files (pass the complete array from `output_to_validate`). Use `prompts.validator_system_corpus` and `prompts.validator_task_corpus` from `references/framework.json`. Also activate the lens's `dimensions_corpus_only` entries (structural lens adds `corpus_completeness`; coherence lens adds `cross_document_consistency`). Finding locations must use `{filename}:{section}` format.

All findings: id, severity, dimension, location, description, evidence (mandatory), suggestion. Findings without evidence are hallucinations and get discarded.

### Phase 2: CONSOLIDATE

Run sequentially after all validators complete. Model: `haiku`. Sub-skill: `sub-skills/consolidator`.

**Single-document mode:** Use `prompts.consolidator` from `references/framework.json`.
**Corpus mode (`corpus: true`):** Use `prompts.consolidator_corpus` — includes cross-document deduplication rules (same contradiction across N file pairs = one finding, not N).

1. Tag each finding with confidence (HIGH / MEDIUM) — full and scan profiles (dual-review enabled)
2. Merge all findings from all lenses into one list
3. Deduplicate: same issue from multiple sources → keep most specific description and highest severity
4. Investigate MEDIUM-confidence findings against source material — keep if evidence supports, discard if reviewer hallucination
5. Remove any finding that lacks evidence
6. Calculate score: start at 100, apply: critical −15, high −8, medium −3, low −1
7. Sort by severity (critical first), then by location
8. Assign grade: ≥95 Clean, ≥85 Good, ≥70 Fair, ≥50 Poor, <50 Failing

### Phase 3: EVALUATE

Check exit conditions based on the profile:

**gate:** Score ≥ 95 → continue workflow. Score < 95 → halt, report GATE_FAILED.

**checkpoint:** Score ≥ 95 → continue. Score < 95 → proceed to one fix attempt, then continue with CHECKPOINT_WARNING regardless of result.

**full:** Score ≥ 95 → exit CLEAN. Score < 95 and iterations remaining → proceed to fix. Score < 95 and iteration = 4 → exit MAX_ITERATIONS_REACHED.

**scan:** Exit immediately after consolidation regardless of score. Return the consolidated findings list as the final output (format: `structured_handoff`). The fixer is never reached. Exit status: SCAN_COMPLETE with score and findings count.

### Phase 4: FIX

**Note:** Gate (`fix_loop: false`): pipeline halts with GATE_FAILED — Phase 4 is never entered. Scan (`fix_loop: false`): pipeline exits from Phase 3 with SCAN_COMPLETE — Phase 4 is never entered.

Model: `sonnet`. Sub-skill: `sub-skills/fixer`. Run as the `domain_expert` role.

**Single-document mode (`corpus: false`):** Use `prompts.fixer` from `references/framework.json`. Produce the complete corrected output as a single document.

**Corpus mode (`corpus: true`):** Use `prompts.fixer_corpus` from `references/framework.json`. The fixer receives all corpus files and produces per-file output blocks:
- One block per file: `### File: {filepath}` followed by the complete corrected content
- Cross-document contradictions: if `authority_hierarchy` is provided, modify the lower-authority file to match the higher-authority file; annotate the fix log entry with `resolved_by: authority_hierarchy`
- Cross-document contradictions without `authority_hierarchy`: do NOT guess a resolution; annotate the fix log entry as `unresolved_contradiction` and leave both conflicting files unchanged for that issue

Standard fix rules (both modes):
- Fix in severity order: critical → high → medium → low
- Log each fix: finding ID → what was changed and why
- Do not introduce new problems while fixing
- When fixes conflict, resolve in favor of the higher-severity finding
- When ambiguous, stay closest to original source material

After fixing, loop back to Phase 1 with the updated output. **Always carry the original `source_material` forward unchanged** — validators at every iteration check against original ground truth, never intermediate representations.

**Critical:** Phase 1 in every iteration — including iteration 2+ — MUST spawn subagents. Do NOT validate the updated output inline, even if it is in context. Inline validation collapses the dual-reviewer cross-check that filters hallucinations. Spawn the same parallel subagent configuration as iteration 1 (with `low` skepticism for iterations 2+).

---

## Calibration Principles

These prevent both under-reporting (missed issues) and over-reporting (hallucinated findings). Remind validators of these when spawning them.

- **Evidence required** — every finding must quote the specific text, value, or section that is wrong. No evidence = discard.
- **Method over attitude** — systematic enumeration and verification, not adversarial hostility.
- **No quotas** — if the output is clean in your lens, say so. Whether to re-examine before reporting clean depends on skepticism level — see the skepticism instruction you received.
- **Scope discipline** — stay within your lens. Note out-of-scope issues briefly but don't deep-dive — another lens owns it.
- **Conservative flagging** — if you find evidence it's wrong, flag it. If you can't find evidence either way, don't flag it. Uncertainty is not a finding.
- **Severity honesty** — assign based on actual impact. Don't inflate severity to force failure or deflate to force a pass.

---

## Exit Reports

**CLEAN** — Score ≥ 95.
Report: status CLEAN, final score, iteration count, scores per iteration, total findings fixed.

**MAX_ITERATIONS_REACHED** — 4 iterations without reaching 95.
Report: status, final score, scores per iteration, remaining findings. Ask user to review and decide: accept as-is, manually fix, or adjust criteria.

**GATE_FAILED** — Gate profile failed.
Report: status, score, findings, pipeline stage name. Cannot continue until resolved.

**CHECKPOINT_WARNING** — Checkpoint didn't achieve clean after fix attempt.
Report: status, score, remaining findings, fix log. Continue with known issues flagged.

**SCAN_COMPLETE** — Scan profile finished discovery pass.
Report: status, score, findings count by severity tier, full structured findings list (see Scan Profile Handoff Format below). Informational score — scan does not pass/fail.

---

## Scan Profile Handoff Format

When `profile: scan`, the final output uses `structured_handoff` format — a prioritized findings list designed for direct consumption by a resolution team.

**Sort order:** severity (critical → high → medium → low), then confidence (HIGH → MEDIUM) within each severity tier.

**Required fields per finding:**

| Field | Description |
|---|---|
| `id` | Unique finding identifier: `LENS_ID-NNN` (e.g., `STRUCTURAL-001`, `ACCURACY-003`) |
| `severity` | critical, high, medium, or low |
| `confidence` | HIGH (both reviewers found it) or MEDIUM (one reviewer, evidence-confirmed) |
| `lens` | Which lens surfaced it: structural, accuracy, coherence, or domain |
| `dimension` | Specific dimension (e.g., structural_validity, correctness, consistency) |
| `location` | Where in the document — section/line, or `{filename}:{section}` in corpus mode |
| `description` | What is wrong |
| `evidence` | Quoted text or specific reference proving the issue |
| `suggestion` | Actionable recommendation for resolution |

**Exit report for scan:**
- Status: `SCAN_COMPLETE`
- Score: consolidated score (informational — scan does not pass/fail)
- Findings count by severity tier
- Full structured findings list

---

## Reference Files

- `references/framework.json` — The complete framework specification: dimension taxonomy with all 15 dimensions across 4 tiers, validation profiles, staged application guidance for multi-step workflows, validator/consolidator/fixer prompt templates, finding schema, scoring weights and examples, and domain-specific usage examples (research, structured data, narrative content, code implementation, document authoring). Read this before spawning subagents.
