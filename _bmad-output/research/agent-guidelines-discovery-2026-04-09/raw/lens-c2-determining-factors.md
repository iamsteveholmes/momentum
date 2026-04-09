---
content_origin: agent-research
lens: C2
topic: Determining Factors for Agent Guideline Effectiveness
date: 2026-04-09
---

# Lens C2: Agent Guideline Effectiveness — Determining Factors

---

## 1. Source Quality Effects

### LLM-generated vs. human-written — empirically settled

**ETH Zurich (arXiv:2602.11988, Feb 2026):** Three conditions: no context file, LLM-generated file, human-written file.
- LLM-generated: **-0.5% on SWE-bench Lite / -2% on AGENTbench** (the prior corpus figure of "-3%" is an inflated rounding — see C1 for corrective analysis)
- Human-written: **+4% success rate**, with 14-22% more tokens and 2-4 extra steps per task
- **Root cause of LLM-generated failure:** 95-100% of LLM-generated files included repository architectural overviews — redundant with content the agent could discover independently. When markdown/docs removed from environment, those same LLM-generated files improved performance by +2.7%.

**Key principle:** The primary dimension is NOT "official vs. community vs. LLM" — it is **"new information vs. redundant information."** Does this line tell the agent something it cannot figure out on its own? If yes, it helps. If no, it costs attention budget with no return.

### Official docs grounding for API accuracy

**Amazon Science (arXiv:2407.09726, 2024):** Documentation Augmented Generation (DAG):
- Low-frequency API accuracy with docs: 38.58% → 47.94% improvement
- Mechanism: official docs provide canonical, correct, current API signatures that resolve training-data ambiguity
- Not because of "official" status per se — because the content is correct and novel relative to training data

**Key implication:** Source authority matters less than whether the content is (a) correct and (b) NOT already in model training data.

---

## 2. Structural Format Effects

### Empirical evidence — effects are large

**"Does Prompt Formatting Have Any Impact on LLM Performance?" (arXiv:2411.10541, November 2024):**
- GPT-3.5-turbo performance varied **up to 40%** in code translation tasks depending on format
- GPT-4 was more robust but still showed meaningful differences (Markdown: 81.2% vs. JSON: 73.9% on reasoning)
- Markdown consistently outperformed plain text and JSON for code tasks
- Format effects diminish with more capable models but do not disappear

**CFPO "Beyond Prompt Content" (arXiv:2502.04295, February 2025):**
- Jointly optimizing content AND formatting produces measurably better results than content optimization alone
- Format is "a critical but often overlooked dimension"

### Specific format findings

**Comparison tables (Wrong | Right) for antipatterns:**
- Contrast tables force agent to see violation and correct replacement simultaneously
- Prose descriptions of antipatterns are easy to misparse
- No RCT exists; structural logic is consistent with task performance research
- Confidence: Medium — convergent practitioner consensus

**Code examples:**
- "Does Few-Shot Learning Help LLM Performance in Code Synthesis?" (arXiv:2412.02906, Dec 2024): examples help specifically for counterintuitive patterns — cases where correct code diverges from model's default
- For standard conventions matching training data: examples add ~19% inference overhead (CFPO) with no benefit
- ETH Zurich: AGENTS.md with worked examples did not outperform files without them when examples were inferrable
- **Rule: include examples only where prose would fail to specify the correct pattern**

**H2 headers as navigation anchors:**
- No controlled study on header naming specifically
- ETH Zurich: generic "architectural overview" sections do NOT reduce agent navigation time
- Domain-specific headers ("Coroutine cancellation", "LazyColumn performance") function as search keys when agents use Grep
- Confidence: Medium — practitioner consensus, not RCT

**Markdown vs. XML for Claude:**
- XML tags (`<rule>`, `<prohibition>`) documented in Anthropic prompt engineering guides as effective structural delimiters for Claude
- No A/B study comparing XML to Markdown H2 headers in agent instruction files published

---

## 3. Specificity vs. Generality

### One of the most important findings — strong empirical backing

**Amazon Science API hallucination research (arXiv:2407.09726, 2024):**
- High-frequency APIs: **93.66% valid invocations**
- Low-frequency APIs (new, updated, rarely-encountered): **38.58% valid invocations**
- 55-percentage-point gap caused by training-data distribution
- ~95 tokens of "API Description + Specification" achieves near-optimal accuracy gains vs. 685 tokens for full documentation. **Compact, specific API specs beat comprehensive documentation in token efficiency.**

**Why "AnimatedVisibility not AnimatedVisibleContent in Compose 1.7" outperforms "use current API not deprecated alternatives":**
1. Encodes the version anchor (which version's conventions apply)
2. Names the deprecated alternative (prevents selection based on training-data frequency)
3. Names the correct replacement (prevents hallucination of a third incorrect option)

**Version-pinning:**
- Library Hallucinations in LLMs (arXiv:2509.22202) confirms version-specific APIs disproportionately affected by hallucination
- JetBrains production example: Go plugin teaches agents to use `slices.Contains()` from Go 1.21 — without version annotation, agents fall back to earlier Go patterns

**IFScale evidence on specificity:**
- At higher instruction densities, models shift from "modification errors" (misinterpreting what an instruction means) to "omission errors" (dropping instructions entirely)
- Specific rules have advantage at higher densities — the model either follows them or doesn't, no misinterpretation intermediate state
- General principles like "write clean code" can be "followed" via any behavior — effectively invisible to adherence measurement

---

## 4. Length and Density

**No published study directly measures "instructions per token" as an optimization variable.** The field has addressed total instruction count and position, but not packing density.

**The 95-token API spec finding** (Amazon Science) establishes a token-efficient sweet spot: enough tokens to specify arguments and correct/incorrect usage, not so many that surrounding noise dilutes the signal.

**ETH Zurich cost finding:** 14-22% more tokens and 2-4 more steps PER FILE, regardless of file quality. Agents follow guideline instructions to thoroughness — longer files cause more checking steps, increasing cost even when checks are vacuous. Operational concern distinct from adherence.

**Density and zone effects (IFScale):**
- Zone 1 (1-50 effective instructions): high adherence
- Zone 2 (50-150): Sonnet shows 10-20% decline
- Zone 3 (150-300): meaningful omission errors
- Zone 4 (300+): uniform failure — adding more provides zero benefit

**Context engineering framing (Anthropic, 2025):** "A 100K context with high information density outperforms a 200K context diluted with irrelevant tool outputs." Practitioner guidance, directionally consistent with IFScale and Chroma context-rot research.

---

## 5. The "Tech-Writer Written" Question

**No direct study compares official documentation extracts vs. community-written vs. LLM-generated summaries as agent guideline sources for a specific domain.**

**Characteristics correlating with better agent performance (inferred):**

1. **Executable specificity.** ETH Zurich found "specific commands" and "tooling" sections most useful — executable rather than descriptive content. Official docs most likely to contain authoritative API signatures and command syntax.

2. **Novelty relative to training data.** Official docs for current library versions most likely to contain (a) correct and (b) not-already-in-training-data content. Community documentation for mature APIs often already in training data and adds nothing.

3. **Structured format.** Official documentation tends to use structured formats (function signature tables, parameter lists) — found effective by arXiv:2411.10541.

4. **Freshness signals.** Official changelogs and migration guides for specific version transitions are both authoritative and novel. "Compose 1.6 → 1.7 API changes" = ideal: official, version-scoped, about changes the model has incomplete training data for.

**The 95-token finding's practical implication:** Full official documentation performs worse than extracted API specs in tokens-per-improvement. Optimal input is NOT the full official docs but a curated extraction — specific function signatures, deprecated alternatives, and version differences relevant to the project's version. Neither raw official docs nor LLM summary — human-curated extraction from authoritative source material.

---

## Cross-Cutting Summary Table

| Question | Status | Key Source | Confidence |
|---|---|---|---|
| LLM-generated vs. human-written | Empirically settled: LLM-generated −0.5-2%, human +4% | ETH Zurich arXiv:2602.11988 | High |
| Official docs for API accuracy | Effective: 38% → 48% with DAG | Amazon Science arXiv:2407.09726 | High |
| Format effects | Up to 40% variance in code tasks; Markdown outperforms plain text | arXiv:2411.10541 | High |
| Comparison tables for antipatterns | Practitioner consensus, no RCT | GitHub blog, compose-skill | Medium |
| Specific vs. general rules | Specific measurably better for low-frequency APIs | Amazon Science 2024 | High |
| Version pinning | Strong: 55pp accuracy gap for unpinned low-frequency APIs | Amazon Science 2024 | High |
| Worked examples | Help for counterintuitive patterns; neutral/harmful otherwise | arXiv:2412.02906; ETH Zurich | Medium |
| Positive vs. negative framing | Positive achieves "near-perfect adherence" vs. high variance for negative — **safety context only; generalizability to coding guidelines unconfirmed** | arXiv:2506.02357 | Low — safety context, not coding guidelines |
| Official vs. community vs. LLM source | Not directly studied; novelty and specificity matter more than provenance | No single study | Low — gap |

---

## Gaps in the Literature

1. Source provenance as isolated variable — no study holds content constant while varying source type
2. Comparison table format specifically for agent guidelines — no RCT
3. Semantic header naming effects — practitioner convention only
4. Density (instructions/token) as optimization variable — not studied
5. Format × model interaction for Claude specifically — GPT-based studies; Claude behavior with XML vs. Markdown headers not empirically tested in published literature

---

## Key Citations

**Source quality:**
- ETH Zurich "Evaluating AGENTS.md" (arXiv:2602.11988) — primary citation
- Amazon Science "On Mitigating Code LLM Hallucinations with API Documentation" (arXiv:2407.09726)
- Library Hallucinations in LLMs (arXiv:2509.22202)

**Format effects:**
- "Does Prompt Formatting Have Any Impact on LLM Performance?" (arXiv:2411.10541, 2024)
- CFPO "Beyond Prompt Content" (arXiv:2502.04295, 2025)

**Specificity / version pinning:**
- Amazon Science 2024 (above)
- JetBrains "Coding Guidelines for AI Agents" (blog.jetbrains.com/idea/2025/05)

**Length and examples:**
- "Does Few-Shot Learning Help LLM Performance in Code Synthesis?" (arXiv:2412.02906, Dec 2024)
- IFScale "How Many Instructions Can LLMs Follow at Once?" (arXiv:2507.11538, 2025)
