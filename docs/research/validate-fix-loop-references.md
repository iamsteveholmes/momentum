# Validate-Fix-Loop: Research References

Research conducted 2026-03-14 to support the design of the validate-fix-loop framework.

## Dual-Reviewer Accuracy

These papers establish that 2 independent reviewers with different framings significantly outperform a single reviewer, and that adding a 3rd reviewer provides no benefit (and can hurt).

| Source | Key Finding |
|--------|-------------|
| [PoLL: Replacing Judges with Juries](https://arxiv.org/html/2404.18796v2) (Verga et al., 2024) | Panel of 3 smaller models beat single GPT-4 on every benchmark. Cross-family diversity is key. |
| [Meta-Judge: Multi-Agent Framework](https://arxiv.org/html/2504.17087v1) (2025) | 2 agents + majority voting = 77.26% vs single-agent 68.89%. Adding 3rd agent *decreased* to 65.38%. |
| [ChatEval: Multi-Agent Debate](https://arxiv.org/abs/2308.07201) (ICLR 2024) | Multi-agent debate improved accuracy 6.2% for ChatGPT. Identical role descriptions *degraded* performance — diverse framings required. |
| [SE-Jury: Ensemble-Judge for SE](https://arxiv.org/html/2505.20854v2) (ASE 2025) | Ensemble of 5 strategies achieved 29.6%-140.8% improvement. Dynamic team selection (2-5 judges) cut cost 50% without losing quality. |
| [Consortium Voting for Hallucination Detection](https://www.cambridgeconsultants.com/teaming-llms-to-detect-and-mitigate-hallucinations/) (NeurIPS 2025 workshop) | Majority voting across LLMs discards hallucinations not confirmed by multiple models. Improved metrics for 92% of teams tested. |

## Error Propagation & Staged Validation

These establish that errors compound through multi-step pipelines, that late-stage errors are disproportionately damaging, and that the "bookend + critical gates" pattern is the optimal cost/quality tradeoff.

| Source | Key Finding |
|--------|-------------|
| [Beyond Exponential Decay](https://arxiv.org/html/2505.24187v1) (2025) | Only 5-10% of tokens are "key tokens" where errors matter. Effective error rate depends on critical decision points, not total steps. |
| [ASCoT: Not All Errors Are Created Equal](https://arxiv.org/html/2508.05282) (2025) | Late-stage errors 3.5x more damaging than early-stage. Error at step 2/4 = 14.64% drop; step 4/4 = 51.69% drop. "Semantic commitment" reduces self-correction ability. |
| [MAKER: Million-Step Zero Errors](https://arxiv.org/abs/2511.09030) | k-threshold voting per step achieved zero errors across 1M steps. Cost: O(cs ln s). Proves per-step validation works but requires verifiable outputs. |
| [Agents at Work: 2026 Playbook](https://promptengineering.org/agents-at-work-the-2026-playbook-for-building-reliable-agentic-workflows/) | Recommends bookend + critical gates: max validation at input/output, heavy at critical decisions, light elsewhere. |
| [Process Reward Models Survey](https://arxiv.org/abs/2510.08049) | Step-level feedback >8% more accurate and 1.5-5x more compute-efficient than outcome-only evaluation. |
| [Compounding Error in LLMs](https://wand.ai/blog/compounding-error-effect-in-large-language-models-a-growing-challenge) | 90% per-step accuracy × 8 steps = 43% overall. 73% probability of downstream failure from single error. |

## Quality Frameworks (Dimension Taxonomy Sources)

These established frameworks informed the 15-dimension, 4-tier taxonomy used in the validate-fix-loop.

| Source | Contribution |
|--------|-------------|
| [ISO/IEC 25010](https://quality.arc42.org/standards/iso-25010) | Software quality model: functional correctness, completeness, appropriateness, reliability, usability. |
| [Wang & Strong (1996)](https://www.tandfonline.com/doi/abs/10.1080/07421222.1996.11518099) | Data quality dimensions: intrinsic (accuracy), contextual (relevance, timeliness, completeness), representational (consistency, conciseness). |
| [Microsoft Azure AI Evaluation Metrics](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-metrics-built-in) | LLM-specific: groundedness, coherence, relevance, fluency. |
| [DeepEval LLM Evaluation](https://deepeval.com/docs/metrics-introduction) | Faithfulness (traceability), answer relevancy, hallucination detection metrics. |
| [LLM Failure Modes Field Guide](https://medium.com/@adnanmasood/a-field-guide-to-llm-failure-modes-5ffaeeb08e80) | Taxonomy of common LLM failures mapped to quality dimensions. |
| [AI Hallucination Classification](https://www.nature.com/articles/s41599-024-03811-x) | Classification framework for types of AI hallucination. |

## Additional References

| Source | Topic |
|--------|-------|
| [Amazon: Evaluating AI Agents](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/) | Real-world lessons from agentic system evaluation |
| [Evaluating LLM Systems at Microsoft](https://medium.com/data-science-at-microsoft/evaluating-llm-systems-metrics-challenges-and-best-practices-664ac25be7e5) | Metrics challenges and best practices |
| [State of What Art? (TACL 2024)](https://aclanthology.org/2024.tacl-1.52/) | Single-prompt evaluation is brittle — different templates lead to very different results |
| [Agentic Workflow Evaluation](https://www.deepchecks.com/agentic-workflow-evaluation-key-metrics-methods/) | Key metrics and methods for agentic workflows |
| [Pipeline Quality Gates (InfoQ)](https://www.infoq.com/articles/pipeline-quality-gates/) | Quality gate patterns in software delivery |
| [Stage-Aware Governance of LLMs](https://www.mdpi.com/2079-8954/14/2/153) | Governance at different pipeline stages |
