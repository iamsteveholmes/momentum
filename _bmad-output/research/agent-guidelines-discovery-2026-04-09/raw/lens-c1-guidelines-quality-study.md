---
content_origin: agent-research
lens: C1
topic: Guidelines Quality — The -3% Study and Empirical Evidence
date: 2026-04-09
---

# Lens C1: The -3% LLM-Generated Guidelines Finding

---

## 1. Original Study — FOUND AND VERIFIED

**Full citation:**
Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, Martin Vechev. "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" ETH Zurich. Submitted February 12, 2026.
**URL:** https://arxiv.org/abs/2602.11988 (PDF: https://arxiv.org/pdf/2602.11988)

---

## 2. What the Paper Actually Found (vs. the Prior Corpus Claim)

**The prior claim:** "LLM-generated guideline files showed marginally negative effects (-3%)"

**The actual findings from ETH Zurich (Gloaguen et al., 2026):**
- LLM-generated AGENTS.md: **-0.5% on SWE-bench Lite**, **-2% on AGENTbench** vs. no context file
- The "-3%" figure is a rounded/imprecise representation — actual findings are -0.5% and -2%
- Human-written AGENTS.md: **+4% average success rate improvement**, inference cost +19%
- Both conditions (LLM-generated AND human-written): inference cost +20%+
- **No confidence intervals, p-values, or significance tests are reported** for any of these differences

**The prior corpus claim was WRONG in two ways:**
1. The -3% number is inflated (actual: -0.5% and -2%)
2. It conflated TWO SEPARATE STUDIES — the efficiency findings (+16-20% tokens, +20-28% time) come from a completely different paper (Lulla et al., 2601.20404) which only tested developer-authored files and never tested LLM-generated files at all

---

## 3. ETH Zurich Methodology

**Benchmark:** AGENTbench — 138 real-world Python tasks from 5,694 pull requests across 12 Python repositories. All repos had developer-written context files. "Niche" repos (low GitHub star counts) to minimize memorization effects. Also tested on SWE-bench Lite (300 tasks).

**Agents / Models tested:**
- Claude Code with Sonnet 4.5
- Codex with GPT-5.2 and GPT-5.1 mini
- Qwen Code with Qwen3-30b-coder

**How LLM-generated files were created:**
Each agent used its own built-in initialization command ("the recommended initialization command and model for each agent individually"). Claude Code's prompt "advocates for a high-level overview only and warns against listing components that are easily discoverable." **No human review or validation step. No template. No iterative refinement.** This represents the FLOOR of LLM-generated quality — out-of-the-box auto-generation.

**Success metric:** Percentage of patches where all repository tests passed. Binary metric, not qualitative.

**Ablation on generation prompts:** Testing "native" model prompt vs. Claude's prompt — "no consistent impact on success rate." The generation method has low sensitivity to the specific prompt used (within the zero-shot regime).

---

## 4. Is -3% a Floor or a Ceiling?

**The study represents the floor of LLM-generated quality, not the ceiling.**

Evidence:

1. Naive single-pass zero-shot generation — worst-plausible production scenario
2. Authors explicitly acknowledge: "human developers appear to dominate" and note that "several related works in the direction of planning and continuous learning from prior tasks may be applicable" — conceding better generation methods exist
3. Not statistically tested. With 138 tasks, a 2% difference is easily within sampling noise
4. **The mechanism is identified:** Agents followed LLM-generated instructions "too thoroughly" — performing unnecessary testing, file exploration, code-quality checks beyond task requirements. This is a **content quality problem** (guidelines containing scope-expanding instructions), NOT an inherent limitation of machine generation

**Critical finding:** When the study removed markdown and documentation files from the evaluation environment, those same LLM-generated files **improved performance by +2.7%** — confirming the failure mechanism is REDUNDANCY, not the nature of LLM generation itself.

---

## 5. The Separate Study (Lulla et al.)

**"On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents"**
https://arxiv.org/html/2601.20404
Singapore Management University, Heidelberg University, King's College London, University of Bamberg

- Tests developer-authored AGENTS.md **only** (no LLM-generated condition)
- Model: OpenAI Codex; 124 PRs across 10 repos
- Findings: output tokens reduced 16.58% to 20.08%, execution time reduced 20.27%–28.64%
- Does NOT measure task success rate — only efficiency
- The source of the "+16-20% / +20-28%" claim in the prior corpus

---

## 6. Other Comparable Studies

**Empirical study of Claude.md files (September 2025)**
https://arxiv.org/html/2509.14744v1
- Analysis of 253 Claude.md files in the wild
- Found: testing content (60.5%) and implementation details (71.9%) are most prevalent categories
- Only 15.4% of files explicitly defined agent roles
- Descriptive/taxonomic — not a controlled performance study

**IFScale: "How Many Instructions Can LLMs Follow at Once?" (July 2025)**
https://arxiv.org/html/2507.11538v1
- 20 models, 10–500 instructions
- Claude 3.7 Sonnet shows linear decay, no threshold
- Not specific to context files

**"Lost in the Middle" (Liu et al., TACL 2024)**
https://aclanthology.org/2024.tacl-1.9/
- Canonical study on position effects
- Not specific to agent guidelines

---

## 7. Summary Assessment

| Question | Finding |
|---|---|
| Original study | Gloaguen et al., ETH Zurich, arXiv 2602.11988, February 2026 |
| Actual measured values | -0.5% (SWE-bench) and -2% (AGENTbench), NOT -3% |
| Statistical rigor | None — no p-values, confidence intervals, significance tests |
| LLM generation method | Naive zero-shot init command; no validation, template, or review |
| Floor or ceiling? | Floor — authors acknowledge better generation methods exist |
| Mechanism of failure | REDUNDANCY — guidelines restating discoverable info, not LLM limitation |
| The +16-20% / +20-28% claim | Separate study (Lulla et al. 2601.20404); developer-authored only, never LLM-generated |
| Prior corpus claim accuracy | Partially wrong — conflates two studies, rounds -2% to -3% |
| Key gap in literature | No study tests quality-controlled LLM generation vs. naive generation vs. human authorship as three distinct conditions |

**Practical implication:** The -3% figure is a slightly inflated, decontextualized restatement of findings from a study that tested only the most naive possible LLM generation method, with no statistical significance testing, on a 138-task Python-only benchmark. It says nothing about what well-prompted, validated, human-reviewed LLM-generated guidelines produce — that condition has not been tested.
