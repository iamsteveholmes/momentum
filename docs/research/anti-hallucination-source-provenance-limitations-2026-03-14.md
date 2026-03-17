# Anti-Hallucination Through Source Provenance: Limitations, False Confidence, and Practical Tradeoffs

**Date:** 2026-03-14
**Status:** Critical Research Analysis
**Analyst Framing:** Adversary (skeptical, looking for what's wrong)
**Confidence Rating System:** HIGH = multiple peer-reviewed sources with data; MEDIUM = single source or indirect evidence; LOW = inference from adjacent research

---

## Executive Summary

Source provenance is widely promoted as the antidote to AI hallucination: require every claim to cite its source, and hallucinations will be caught. **This is dangerously incomplete.** The research reveals that citation requirements can create a false sense of security, that LLMs hallucinate citations at alarming rates (11-95%), that even correct citations may misrepresent their sources, and that the cost of rigorous provenance tracking may exceed its benefits in many contexts.

The uncomfortable truth: provenance is necessary but deeply insufficient. The minimum viable approach requires understanding not just *what* to cite but *which failure modes* provenance actually catches versus which ones it merely obscures.

---

## 1. Citation Hallucination: The Numbers Are Worse Than You Think

### Confidence: HIGH

The largest systematic study of LLM citation hallucination audited 10 commercial LLMs generating 69,557 citation instances. Hallucination rates span **11.4% to 56.8%** depending on the model, domain, and prompting approach.

**Source:** "How LLMs Cite and Why It Matters" (arXiv:2603.03299) — https://arxiv.org/abs/2603.03299

A second large-scale study, GhostCite, benchmarked 13 state-of-the-art LLMs across 40 research domains and found hallucination rates ranging from **14.23% to 94.93%**.

**Source:** "GhostCite: A Large-Scale Analysis of Citation Validity" (arXiv:2602.06718) — https://arxiv.org/abs/2602.06718

A deployment-constraint study found that **no model exceeded a 47.5% citation-level existence rate** across 17,443 generated citations. More than half of all generated references did not exist.

**Source:** "Do Deployment Constraints Make LLMs Hallucinate Citations?" (arXiv:2603.07287) — https://arxiv.org/abs/2603.07287

### The Uncomfortable Truths

1. **Citations look perfect while being completely fabricated.** The deployment-constraint study found that outputs remained "format-compliant (well-formed bibliographic fields)" even when the underlying references were entirely invented. A citation that *looks right* is more dangerous than no citation at all because it short-circuits human skepticism.

2. **Prompting for citations makes things worse, not better.** The same study found that temporal constraints and combination prompting conditions showed "the steepest drops" in citation reliability. Paradoxically, the more specific you are about what kind of citations you want, the more the model fabricates to satisfy the constraint.

3. **Hallucination is prompt-induced, not intrinsic.** The 69,557-citation study found that "no model spontaneously generated citations when unprompted," suggesting hallucination emerges specifically when systems are asked to provide evidence -- exactly the scenario a provenance-first workflow creates.

4. **The problem is getting worse in the real world.** Analysis of 2.2 million citations from 56,381 published papers found 1.07% contain invalid or fabricated citations, with an **80.9% increase in 2025 alone**. (GhostCite, arXiv:2602.06718)

### Taxonomy of Citation Fabrication

Analysis of 100 hallucinated citations in NeurIPS 2025 accepted papers revealed:

| Failure Type | Prevalence |
|---|---|
| Total Fabrication | 66% |
| Partial Attribute Corruption | 27% |
| Identifier Hijacking | 4% |
| Placeholder Hallucination | 2% |
| Semantic Hallucination | 1% |

Critically, **100% exhibited compound failure modes** -- a primary fabrication combined with secondary characteristics (63% Semantic Hallucination, 29% Identifier Hijacking) designed to create misleading plausibility.

**Source:** "Compound Deception in Elite Peer Review" (arXiv:2602.05930) — https://arxiv.org/abs/2602.05930

### What This Means for Momentum

If Momentum agents are instructed to "cite sources for every claim," they will fabricate sources at rates between 11% and 95% depending on the model and domain. The citations will look legitimate. Downstream agents consuming these citations will treat them as validated. The chain of provenance becomes a chain of hallucinated confidence.

---

## 2. False Grounding: When the Citation Is Real But the Claim Is Wrong

### Confidence: HIGH

Even when an LLM cites a real, verifiable source, it frequently misrepresents what that source says. This is arguably more dangerous than a fabricated citation because the source exists and can be "verified" -- but the claim derived from it is still wrong.

The "17% Gap" study audited 5,514 citations across 50 AI survey papers and identified three failure modes:

| Failure Mode | Prevalence |
|---|---|
| Parsing-induced matching failures | 78.5% |
| Hallucinated identifiers with valid titles | 16.4% |
| Pure hallucinations | 5.1% |

The study concluded that "AI tools act as lazy research assistants, retrieving correct titles but hallucinating metadata, thereby severing the digital chain of custody required for reproducible science."

**Source:** "The 17% Gap: Quantifying Epistemic Decay" (arXiv:2601.17431) — https://arxiv.org/abs/2601.17431

The HalluHard benchmark found that **even frontier models with web search access still produce ungrounded content at ~30%** for the strongest configuration (Opus-4.5 with web search). "Content-grounding errors" -- where models cite sources that don't actually support their claims -- persist at high rates.

**Source:** "HalluHard: A Hard Multi-Turn Hallucination Benchmark" (arXiv:2602.01031) — https://arxiv.org/abs/2602.01031

The FalseCite study found something deeply concerning: when LLMs are presented with false citations, they exhibit **increased hallucination activity**, particularly in more advanced models. GPT-4o-mini showed "a noticeable increase in hallucination activity for false claims with deceptive citations." The model trusts the citation and generates content to match it.

**Source:** "Visualizing and Benchmarking LLM Factual Hallucination" (arXiv:2602.11167) — https://arxiv.org/abs/2602.11167

### The Uncomfortable Truths

1. **Provenance doesn't verify semantics.** A system can have perfect traceability -- every claim linked to a source document, every source document verified to exist -- and still have pervasive misrepresentation of what those sources actually say.

2. **Citations create a trust anchor that short-circuits verification.** The human trust study (~12,000 queries, seven countries) found that "reference links and citations significantly increase trust in GenAI, even when those links and citations are incorrect or hallucinated." Citations function as trust signals independent of their accuracy. Higher trust correlates with "faster clicking and reduced evaluation time."

   **Source:** "Human Trust in AI Search" (arXiv:2504.06435) — https://arxiv.org/abs/2504.06435

3. **Models excel at surface-level quotation but struggle with inference-based provenance.** The GenProve study revealed a "reasoning gap" where models handle direct citations well but face "substantial difficulty in tracing reasoning steps back to source material." This is exactly the kind of provenance that matters most in a specification chain: not "this requirement exists in document X" but "this design decision is justified by requirement Y which derives from research finding Z."

   **Source:** "GenProve: Learning to Generate Text with Fine-Grained Provenance" (arXiv:2601.04932) — https://arxiv.org/abs/2601.04932

### What This Means for Momentum

In a Research-to-Story pipeline, the most critical provenance claims are inferential, not quotational. "The architecture uses microservices because the PRD requires independent scaling" is an inference-based provenance claim. Current models are worst at exactly this type. Requiring provenance will produce citations that look correct for direct quotes but fail silently on the logical connections that actually matter.

---

## 3. Provenance Theater: When Traceability Is Compliance, Not Quality

### Confidence: MEDIUM

Requirements traceability -- the practice of linking each requirement to its source and downstream artifacts -- has been studied for decades. The consistent finding is a gap between traceability as documented and traceability as practiced.

Research on automotive software development confirms that "erroneous or missing traceability relationships often arise due to improper propagation of requirement changes or human errors in requirement mapping, leading to inconsistencies and increased maintenance costs."

**Source:** "TVR: Automotive System Requirement Traceability Validation and Recovery" (arXiv:2504.15427) — https://arxiv.org/abs/2504.15427

A study of issue tracking ecosystems found "complex networks of interlinked artefacts and diverse workflows" where solutions developed for one organizational context "may not transfer effectively to another" -- meaning traceability frameworks are inherently context-dependent and resist standardization.

**Source:** "Issue Tracking Ecosystems: Context and Best Practices" (arXiv:2507.06704) — https://arxiv.org/abs/2507.06704

The GhostCite study found that **41.5% of researchers copy citations without verification**, and **76.7% of peer reviewers don't thoroughly check references**. If human experts routinely skip verification in academic peer review, expecting AI agents to rigorously verify in a spec pipeline is aspirational at best.

**Source:** GhostCite (arXiv:2602.06718) — https://arxiv.org/abs/2602.06718

Research on early requirements traceability found that "practitioners reported low confidence regarding correctness and completeness of trace work" -- the traceability task itself presents "significant cognitive and practical difficulties" that persist "regardless of recommender system support."

**Source:** "Early Requirements Traceability with Domain-Specific Taxonomies" (arXiv:2311.12146) — https://arxiv.org/abs/2311.12146

### The Uncomfortable Truths

1. **Traceability matrices become write-only artifacts.** They are created to satisfy process requirements but rarely consulted during actual development decisions. The maintenance cost grows quadratically with the number of artifacts, while the verification frequency approaches zero. [UNVERIFIED - based on training data: classic requirements engineering literature including Gotel & Finkelstein's seminal work on traceability problems consistently documents this pattern]

2. **Automated traceability reduces effort but doesn't solve the meaning problem.** Large-scale information retrieval for traceability at industrial scale faces fundamental challenges: "scaling IR techniques to industry data is challenging" and "there is a lack of research on scalable parameter optimization."

   **Source:** "Large-scale Information Retrieval in Software Engineering" (arXiv:2308.11750) — https://arxiv.org/abs/2308.11750

3. **Provenance theater gives organizations confidence without protection.** When every document has a traceability matrix, the organization feels safe. But if nobody reads the matrix, and the matrix wasn't verified, it's security theater -- a compliance artifact, not a quality mechanism.

### What This Means for Momentum

If Momentum requires every spec artifact to have a provenance section, there's a real risk of creating provenance theater: agents will dutifully generate traceability sections that look complete but whose links are unchecked, whose semantic accuracy is unverified, and whose maintenance burden eventually causes them to be ignored.

---

## 4. Citation Overhead vs. Value: The Diminishing Returns Problem

### Confidence: MEDIUM

The question isn't whether provenance has value -- it does. The question is: at what point does mandatory citation create more friction than quality improvement?

### Quantitative Evidence on Overhead

The "Plausibility Trap" study quantified the cost of using LLMs for verification tasks: a **~6.5x latency penalty** compared to deterministic methods, plus risks of "algorithmic sycophancy" where the verification process produces plausible-sounding but inaccurate confirmations.

**Source:** "The Plausibility Trap" (arXiv:2601.15130) — https://arxiv.org/abs/2601.15130

Expert evaluation of LLMs in a specialized domain (life cycle assessment) found that **37% of responses contained inaccurate or misleading information** and citation hallucination rates reached **up to 40%**. This means 40% of the citation overhead produces zero value -- or worse, negative value by creating false confidence.

**Source:** "An Expert-grounded Benchmark of General Purpose LLMs in LCA" (arXiv:2510.19886) — https://arxiv.org/abs/2510.19886

The HalluHard benchmark showed that even with the strongest model and web search, hallucination rates remain at ~30%. That means roughly one-third of the effort spent generating and formatting citations is wasted on claims that will be wrong anyway.

**Source:** HalluHard (arXiv:2602.01031) — https://arxiv.org/abs/2602.01031

### The Uncomfortable Truths

1. **Citation requirements create a false economy.** You spend tokens generating citations, tokens verifying citations, tokens formatting citation metadata -- and 11-56% of them are fabricated. The overhead is real; the quality improvement is partial.

2. **The verification tax compounds through the pipeline.** In a multi-step specification chain (Research -> Brief -> PRD -> Architecture -> Stories), each step must verify the previous step's citations AND generate its own. The cumulative overhead grows multiplicatively while the marginal quality gain from each verification step decreases.

3. **"Good enough" citations may be worse than no citations.** If a citation gives 70% confidence that a claim is grounded, the consumer may treat it as 95% confident. A claim without a citation at least signals uncertainty.

---

## 5. Multi-Hop Provenance Degradation: The Telephone Game Problem

### Confidence: HIGH

As claims pass through multiple transformation steps, provenance degrades. This is directly relevant to Momentum's spec chain where research findings must survive multiple transformations.

Multi-hop question answering research consistently identifies three compounding problems: "hallucination, error propagation, and limited context length." Errors at each reasoning hop propagate to subsequent steps, and "existing hybrid approaches...lack internal verification of intermediate reasoning steps, allowing potential errors to propagate through complex reasoning tasks."

**Source:** "Reasoning Court: Combining Reasoning, Action, and Judgment for Multi-Hop Reasoning" (arXiv:2504.09781) — https://arxiv.org/abs/2504.09781

**Source:** "SG-FSM: A Self-Guiding Zero-Shot Prompting Paradigm for Multi-Hop Question Answering" (arXiv:2410.17021) — https://arxiv.org/abs/2410.17021

The HalluHard benchmark quantified this in multi-turn interactions: "errors compound as dialogue progresses in multi-turn interactions." Turn position directly impacts hallucination rates.

**Source:** HalluHard (arXiv:2602.01031) — https://arxiv.org/abs/2602.01031

Research on long-context LLMs found that "longer contexts alone do not guarantee better performance and can be detrimental when relevant evidence is diluted or widely dispersed." Anti-hallucination instructions can backfire: they "can make some models overly conservative, sharply reducing accuracy in literal extraction and logical inference."

**Source:** "Not All Needles Are Found: How Fact Distribution Shapes Hallucination Risks" (arXiv:2601.02023) — https://arxiv.org/abs/2601.02023

The verbatim memorization threshold study found that citation accuracy correlates directly with training data exposure: papers with fewer than ~1,000 citations show "elevated hallucination rates," with a clear threshold where LLM behavior shifts from generalizing to memorizing.

**Source:** "Hallucinate or Memorize? Probabilistic Learning in LLMs" (arXiv:2511.08877) — https://arxiv.org/abs/2511.08877

### The Uncomfortable Truths

1. **Momentum's spec chain is a 6-hop transformation.** Research -> Brief -> PRD -> Architecture -> Epics -> Stories. If each hop introduces even 10% degradation, final provenance accuracy is 0.9^6 = 53%. At 20% per-hop degradation, accuracy drops to 26%.

2. **Provenance links become increasingly abstract.** A Story-level claim like "use Redis for session caching" might trace back to an Architecture decision, which traces back to a PRD requirement, which traces back to a research finding about session latency. By the time you follow the chain, the original nuance is lost and the provenance link says "supported by research" without meaningful content.

3. **Anti-hallucination instructions at each hop create conservative cascading.** If each agent is told to refuse claims it can't ground, the pipeline will reject valid inferences that cross multiple documents. The system becomes correct but useless.

---

## 6. RAG Limitations in Practice: When Retrieval Doesn't Save You

### Confidence: HIGH

RAG is often positioned as the solution to hallucination. The evidence shows significant remaining failure modes.

### The Seven Failure Points

A foundational study identified seven critical failure categories in RAG system design and deployment, concluding that "RAG systems suffer from limitations inherent to information retrieval systems and from reliance on LLMs." Critically, "validation only occurs during operational deployment and robustness develops iteratively rather than through initial design."

**Source:** "Seven Failure Points When Engineering a RAG System" (arXiv:2401.05856) — https://arxiv.org/abs/2401.05856

### Standalone vs. RAG vs. Advanced RAG

The legal domain study provides the clearest comparison:

| Approach | False Citation Rate |
|---|---|
| Standalone LLM | >30% |
| Basic RAG | Significant improvement, but "notable misgrounding" |
| Advanced RAG (fine-tuned embeddings, re-ranking, self-correction) | <0.2% |

**Source:** "Reliability by Design" (arXiv:2601.15476) — https://arxiv.org/abs/2601.15476

This looks encouraging, but note: "Advanced RAG" requires embedding fine-tuning, re-ranking, and self-correction. This is not "add a vector database" -- it's a significant engineering investment per domain.

### Specific RAG Failure Modes

**Parametric Override:** RAG systems suffer from "knowledge conflicts, where model-internal parametric knowledge overrides retrieved evidence, leading to unfaithful outputs." The model ignores what it retrieved and generates from memory instead.

**Source:** "CoRect: Context-Aware Logit Contrast for Hidden State Rectification" (arXiv:2602.08221) — https://arxiv.org/abs/2602.08221

**Document-Level Retrieval Mismatch:** In legal domains, "structurally similar documents frequently cause retrieval systems to malfunction" -- the retriever "selects information from entirely incorrect source documents."

**Source:** "Towards Reliable Retrieval in RAG Systems for Large Legal Datasets" (arXiv:2510.06999) — https://arxiv.org/abs/2510.06999

**Entity Substitution Hallucinations:** "Existing hallucination detectors rely on semantic similarity metrics that tolerate entity substitutions, a dangerous failure mode when confusing parties, dates, or legal provisions can have material consequences." In other words, the retrieved text is correct but the names/dates/entities are swapped.

**Source:** "HalluGraph: Auditable Hallucination Detection for Legal RAG" (arXiv:2512.01659) — https://arxiv.org/abs/2512.01659

**Embedding-Based Detection Fails on Real Hallucinations:** "Real hallucinations from RLHF-aligned models" are semantically indistinguishable from truthful responses using embeddings, achieving "100% FPR at target coverage" -- complete failure. Only reasoning-based detection (like LLM judges) works, at 7% false positive rate.

**Source:** "The Semantic Illusion: Certified Limits of Embedding-Based Hallucination Detection" (arXiv:2512.15068) — https://arxiv.org/abs/2512.15068

### The Uncomfortable Truths

1. **Basic RAG is not enough.** Simply grounding generation in retrieved documents still produces "notable misgrounding." Only advanced RAG with domain-specific fine-tuning approaches acceptable error rates, and that investment must be made per domain.

2. **The model can ignore its own retrieved evidence.** Parametric override means the model's training-time knowledge can silently replace the retrieved facts. The system appears grounded but generates from memory.

3. **Semantic similarity is a broken verification signal.** You cannot use embedding similarity to check if a response is faithful to its sources. The most dangerous hallucinations are semantically similar to truth -- that's what makes them dangerous.

4. **RAG failure modes compound with provenance requirements.** If the retrieval step returns the wrong document, and the model generates a citation to that wrong document, the provenance chain looks complete and verified while being entirely wrong.

---

## 7. The Verification Paradox: Who Watches the Watchmen?

### Confidence: HIGH

If you use an LLM to verify another LLM's citations, who verifies the verifier?

### The Confidence Paradox (Dunning-Kruger for AI)

A study evaluating 9 LLMs on 5,000 claims across 47 languages with 240,000+ human annotations found that "smaller, accessible models show high confidence despite lower accuracy, while larger models demonstrate higher accuracy but lower confidence." This mirrors the Dunning-Kruger effect: the least capable verifiers are the most confident.

**Source:** "Scaling Truth: The Confidence Paradox in AI Fact-Checking" (arXiv:2509.08803) — https://arxiv.org/abs/2509.08803

### LLM-as-Judge Is Unreliable for Specialized Domains

In Polish legal examination evaluation, "evaluations of the 'LLM-as-a-judge' often diverged from the judgments of the official examining committee." Models exhibited "incorrect citation of legal provisions" and "weak argumentation in complex legal contexts."

**Source:** "LLM-as-a-Judge is Bad" (arXiv:2511.04205) — https://arxiv.org/abs/2511.04205

### But There's a Nuance

The TREC 2024 RAG Track evaluation found that on citation support assessment (does this citation support this claim?), "an independent human judge correlates better with GPT-4o than a human judge" -- 56% perfect agreement on a three-level scale, rising to 72% with LLM post-editing. This suggests LLMs can reliably assess citation support for factual claims, even if they struggle with specialized reasoning.

**Source:** "Support Evaluation for TREC 2024 RAG Track" (arXiv:2504.15205) — https://arxiv.org/abs/2504.15205

### Practical Verification Approaches

The Tool Receipts approach (NabaOS) achieves **94.2% detection of fabricated tool references** with <15ms overhead by generating HMAC-signed execution receipts. This works because it verifies that an action actually occurred (deterministic), not that a claim is true (probabilistic).

**Source:** "Tool Receipts, Not Zero-Knowledge Proofs" (arXiv:2603.10060) — https://arxiv.org/abs/2603.10060

The Proof-Carrying Numbers (PCN) protocol enforces numeric fidelity through renderer-based verification with fail-closed behavior. Verification happens in the display layer, not in the model. "All others default to unverified" -- unmarked numbers signal uncertainty.

**Source:** "Proof-Carrying Numbers (PCN)" (arXiv:2509.06902) — https://arxiv.org/abs/2509.06902

### The Uncomfortable Truths

1. **Using an LLM to verify citations works for factual support but fails for reasoning.** LLMs can tell you whether a source says X. They struggle to tell you whether X actually supports conclusion Y. In a spec chain, the reasoning is what matters.

2. **Verification confidence is inversely correlated with accuracy in smaller models.** If you use a cheaper model for verification (likely for cost reasons), it will be more confident in wrong answers.

3. **The only reliable verification is deterministic.** Tool receipts (did this API call actually happen?), database lookups (does this DOI exist?), and numeric verification (does this number match the source?) work because they don't require probabilistic judgment. Everything else is LLM-verifying-LLM, which has the same failure modes as the original generation.

4. **Human verification doesn't scale either.** 41.5% of researchers copy citations without verification. 76.7% of peer reviewers don't check references. If humans won't verify, and LLMs can't reliably verify, who does the verification?

---

## 8. When Provenance Doesn't Help: The Source Itself Is Wrong

### Confidence: MEDIUM

Even perfect provenance fails when:

### The Source Was Wrong to Begin With

Expert evaluation across 168 reviews found that **37% of LLM responses contained inaccurate or misleading information** even when grounded in domain knowledge. The problem isn't citation -- it's that the underlying knowledge can be wrong, outdated, or misinterpreted.

**Source:** "An Expert-grounded Benchmark of General Purpose LLMs in LCA" (arXiv:2510.19886) — https://arxiv.org/abs/2510.19886

### Requirements Drift

In automotive software development, "erroneous or missing traceability relationships often arise due to improper propagation of requirement changes." The source document was correct when the trace was established. The source document was subsequently updated. The trace was not. The provenance link now points to an outdated version of truth.

**Source:** TVR (arXiv:2504.15427) — https://arxiv.org/abs/2504.15427

### The Acceleration-Verification Gap

LLM-assisted replication research acknowledges that while AI can "accelerate research production," this "acceleration risks outpacing verification." AI verification works best as "assistive infrastructure for peer review and pre-submission checks" -- a support tool, not an autonomous arbiter of truth.

**Source:** "LLM-Assisted Replication for Quantitative Social Science" (arXiv:2602.18453) — https://arxiv.org/abs/2602.18453

### Anti-Hallucination Instructions Can Backfire

The long-context study found that "anti-hallucination instructions can make some models overly conservative, sharply reducing accuracy in literal extraction and logical inference." Telling the model to be careful makes it refuse to extract correct information.

**Source:** (arXiv:2601.02023) — https://arxiv.org/abs/2601.02023

### The Uncomfortable Truths

1. **Provenance to a wrong source is worse than no provenance.** It gives the illusion of grounding. Everyone in the chain sees "backed by research" and moves on. The error propagates with a stamp of approval.

2. **Requirements change faster than provenance chains update.** In an agentic pipeline, the research might be refreshed, but the PRD references the old research, and the Architecture references the old PRD. Provenance becomes a fossil record of decisions that no longer apply.

3. **There is no source-of-truth for most software requirements.** Requirements exist in conversations, Slack threads, meeting notes, and heads. Formalizing provenance assumes a stable, canonical source exists. Often it doesn't.

---

## Synthesis: What Actually Works vs. What Just Looks Like It Works

### What Gives False Confidence

| Approach | Why It Feels Safe | Why It Isn't |
|---|---|---|
| "Every claim has a citation" | Looks rigorous and auditable | 11-95% of LLM citations are fabricated; format-compliant but fake |
| "We use RAG for grounding" | Retrieved docs provide evidence | Basic RAG still produces notable misgrounding; parametric override is silent |
| "LLM verifies LLM citations" | Automated quality check | Verifier has same failure modes as generator; smaller models are overconfident |
| "Full traceability matrix" | Complete provenance chain | Write-only artifact; maintenance cost grows quadratically; nobody reads it |
| "Semantic similarity checking" | Mathematical foundation | 100% false positive rate on real RLHF-aligned hallucinations |
| "Anti-hallucination instructions" | Direct behavioral control | Can make models overly conservative, reducing correct extractions |

### What Actually Improves Quality

| Approach | Evidence | Limitation |
|---|---|---|
| **Multi-model consensus** | When 3+ LLMs cite the same source, accuracy reaches 95.6% (5.8x improvement) | Expensive; multiplies inference costs |
| **Within-prompt repetition** | Requiring 2+ replications achieves 88.9% accuracy | Increases token usage per query |
| **Advanced RAG** (domain-specific fine-tuning + re-ranking + self-correction) | Reduces False Citation Rate below 0.2% in legal domain | Significant per-domain engineering investment |
| **Deterministic verification** (database lookups, DOI checks, tool receipts) | 94.2% detection of fabricated references at <15ms | Only works for verifiable facts, not reasoning |
| **Proof-Carrying Numbers** | Formal soundness/completeness guarantees for numeric claims | Only covers numeric fidelity |
| **Lightweight classifiers on bibliographic features** | AUC 0.876 for citation existence pre-screening | Pre-screening only; doesn't verify semantic accuracy |
| **Fail-closed defaults** | Unverified claims are marked as such rather than treated as grounded | Requires UI/workflow support; agents may over-mark |

**Sources for "What Actually Works":** Multi-model consensus and within-prompt repetition from arXiv:2603.03299; Advanced RAG from arXiv:2601.15476; Deterministic verification from arXiv:2603.10060; PCN from arXiv:2509.06902; Classifiers from arXiv:2603.03299.

---

## The Minimum Viable Provenance Approach for Momentum

Based on this analysis, here is what I believe actually delivers value versus what creates overhead for its own sake.

### Tier 1: Do This (Evidence-backed, high ROI)

1. **Deterministic source verification for factual claims.** If an agent cites a document, verify that the document exists and was accessible. Database lookup, file existence check, URL resolution. This catches Total Fabrication (66% of citation failures) with near-zero overhead.

2. **Fail-closed provenance marking.** Every claim gets a provenance status: VERIFIED (deterministically checked), CITED (source provided but not verified), INFERRED (derived from reasoning), or UNGROUNDED. Consumers know what they're trusting. Modeled after the Proof-Carrying Numbers approach.

3. **Semantic verification only at critical transitions.** Don't verify every claim at every step. Verify at the Research->Brief and Architecture->Epics transitions where the highest semantic transformation occurs. Use the strongest available model, not the cheapest.

4. **Multi-model consensus for high-stakes claims.** For architectural decisions and critical requirements, generate independently from 2-3 models and check agreement. The 95.6% accuracy from 3+ model consensus is the strongest signal available.

### Tier 2: Consider This (Reasonable evidence, moderate ROI)

5. **Provenance decay tracking.** Timestamp provenance links. Flag any link where the source document has been modified since the link was established. This catches the requirements-drift problem.

6. **Lightweight citation existence pre-screening.** Train or deploy a classifier on bibliographic features (AUC 0.876) to flag likely fabricated citations before they enter the pipeline. Cheap and fast.

7. **Bounded traceability, not full traceability.** Trace one hop back (this Story traces to this Epic, which traces to this Arch Decision). Don't maintain a full 6-hop chain. The maintenance cost exceeds the value beyond 1-2 hops.

### Tier 3: Don't Do This (Evidence suggests it's provenance theater)

8. **Don't require citations for every claim at every pipeline stage.** This triggers prompt-induced hallucination and creates citation theater. Require citations only for factual claims that are deterministically verifiable.

9. **Don't use embedding similarity for hallucination detection.** Certified to fail on real hallucinations from aligned models.

10. **Don't use a smaller/cheaper model as verifier.** It will be more confident in wrong answers (Dunning-Kruger effect for AI).

11. **Don't build a full traceability matrix.** It will become a write-only compliance artifact. Focus verification effort on the transitions where semantic transformation is highest.

---

## Open Questions for Momentum

1. **What is the acceptable error rate for each pipeline stage?** If Research->Brief introduces 10% error and we can detect half of it, is 5% residual acceptable? The answer determines verification investment.

2. **Which claims are worth verifying?** Not all claims in a PRD have equal impact. "The system should support 1000 concurrent users" is high-stakes and verifiable. "The UX should feel modern" is neither. Provenance effort should be proportional to claim criticality.

3. **How do we handle provenance for reasoning-based claims?** Current models are worst at this (the "reasoning gap" from GenProve). These are also the most valuable provenance claims. This remains an unsolved problem.

4. **What is the refresh cadence for provenance?** Requirements drift means provenance links rot. How often should the chain be re-validated? What's the cost model?

---

## Source Index

All sources cited in this report, in order of first appearance:

| # | Source | URL | Type |
|---|---|---|---|
| 1 | How LLMs Cite and Why It Matters (2603.03299) | https://arxiv.org/abs/2603.03299 | Peer-reviewed study |
| 2 | GhostCite (2602.06718) | https://arxiv.org/abs/2602.06718 | Large-scale analysis |
| 3 | Do Deployment Constraints Make LLMs Hallucinate Citations? (2603.07287) | https://arxiv.org/abs/2603.07287 | Empirical study |
| 4 | Compound Deception in Elite Peer Review (2602.05930) | https://arxiv.org/abs/2602.05930 | Taxonomy study |
| 5 | The 17% Gap (2601.17431) | https://arxiv.org/abs/2601.17431 | Forensic audit |
| 6 | HalluHard (2602.01031) | https://arxiv.org/abs/2602.01031 | Benchmark |
| 7 | FalseCite (2602.11167) | https://arxiv.org/abs/2602.11167 | Dataset/benchmark |
| 8 | Human Trust in AI Search (2504.06435) | https://arxiv.org/abs/2504.06435 | Large-scale experiment |
| 9 | GenProve (2601.04932) | https://arxiv.org/abs/2601.04932 | Framework study |
| 10 | TVR: Automotive Traceability (2504.15427) | https://arxiv.org/abs/2504.15427 | Industrial application |
| 11 | Issue Tracking Ecosystems (2507.06704) | https://arxiv.org/abs/2507.06704 | Dissertation |
| 12 | Early Requirements Traceability (2311.12146) | https://arxiv.org/abs/2311.12146 | Pilot experiment |
| 13 | Large-scale IR in SE (2308.11750) | https://arxiv.org/abs/2308.11750 | Experience report |
| 14 | The Plausibility Trap (2601.15130) | https://arxiv.org/abs/2601.15130 | Quantitative study |
| 15 | Expert-grounded LLM Benchmark (2510.19886) | https://arxiv.org/abs/2510.19886 | Expert evaluation |
| 16 | Reasoning Court (2504.09781) | https://arxiv.org/abs/2504.09781 | Framework study |
| 17 | SG-FSM (2410.17021) | https://arxiv.org/abs/2410.17021 | Prompting paradigm |
| 18 | Not All Needles Are Found (2601.02023) | https://arxiv.org/abs/2601.02023 | Empirical study |
| 19 | Hallucinate or Memorize? (2511.08877) | https://arxiv.org/abs/2511.08877 | Correlation study |
| 20 | Seven Failure Points in RAG (2401.05856) | https://arxiv.org/abs/2401.05856 | Experience report |
| 21 | Reliability by Design (2601.15476) | https://arxiv.org/abs/2601.15476 | Legal domain study |
| 22 | CoRect (2602.08221) | https://arxiv.org/abs/2602.08221 | Mechanistic study |
| 23 | Legal RAG Retrieval Mismatch (2510.06999) | https://arxiv.org/abs/2510.06999 | RAG failure analysis |
| 24 | HalluGraph (2512.01659) | https://arxiv.org/abs/2512.01659 | Legal RAG detection |
| 25 | Semantic Illusion (2512.15068) | https://arxiv.org/abs/2512.15068 | Formal analysis |
| 26 | Scaling Truth (2509.08803) | https://arxiv.org/abs/2509.08803 | Multi-language study |
| 27 | LLM-as-a-Judge is Bad (2511.04205) | https://arxiv.org/abs/2511.04205 | Legal evaluation |
| 28 | TREC 2024 RAG Track (2504.15205) | https://arxiv.org/abs/2504.15205 | Evaluation study |
| 29 | Tool Receipts / NabaOS (2603.10060) | https://arxiv.org/abs/2603.10060 | Verification framework |
| 30 | Proof-Carrying Numbers (2509.06902) | https://arxiv.org/abs/2509.06902 | Protocol specification |
| 31 | FACTUM (2601.05866) | https://arxiv.org/abs/2601.05866 | Mechanistic detection |
| 32 | LLM-Assisted Replication (2602.18453) | https://arxiv.org/abs/2602.18453 | Replication study |
| 33 | CiteAudit (2602.23452) | https://arxiv.org/abs/2602.23452 | Benchmark |
| 34 | AI Hallucination from Students' Perspective (2602.17671) | https://arxiv.org/abs/2602.17671 | Qualitative study |
| 35 | RAGLens (2512.08892) | https://arxiv.org/abs/2512.08892 | Detection method |
| 36 | Reason and Verify (2603.10143) | https://arxiv.org/abs/2603.10143 | RAG framework |
