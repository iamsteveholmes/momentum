# Source Material: AI Validation Research Findings

## Meta-Judge (2025)
Two agents with cross-checking achieved 77.26% accuracy versus 68.89% for single-agent review — approximately 8–9% absolute improvement. **Adding a third reviewer decreased performance below the 2-agent baseline.** The sweet spot is 2 reviewers, not 3. The key mechanism is framing diversity (different evaluation approaches), not reviewer count.

## PoLL (2024)
Panel of 3 reviewers outperformed single GPT-4 on every benchmark. Critically, different framings are essential — same-prompt reviewers capture far less benefit than differently-framed reviewers.

## Huang (2023)
73% probability that a single error causes downstream pipeline failure. At 90% per-step accuracy across 8 steps = 43% overall accuracy.

## ASCoT (2025)
Error at step 2/4 = 14.64% accuracy drop. Error at step 4/4 = 51.69% accuracy drop. Late-stage "semantic commitment" causes models to lock into trajectories with reduced self-correction.

## Process Reward Models
Step-level feedback is >8% more accurate and 1.5–5× more compute-efficient than outcome-only evaluation, but only when focused on steps that matter.

## Seeded Errors in research-summary-seeded.md (for benchmark verification)
- ERROR 1 (factual/accuracy lens): The summary states "Meta-Judge (2025) found that using 3 independent reviewers outperformed a single-agent approach by 15% absolute accuracy, with optimal performance achieved at the 3-reviewer configuration." This directly contradicts the source: Meta-Judge found 2 agents outperform 1 agent by ~8-9%, and adding a 3rd agent DECREASED performance.
- ERROR 2 (coherence/consistency lens): Executive Summary states the validation threshold is "90 out of 100" but the Methodology section states "outputs scoring below 95 out of 100 be flagged for remediation." These are directly contradictory thresholds within the same document.
