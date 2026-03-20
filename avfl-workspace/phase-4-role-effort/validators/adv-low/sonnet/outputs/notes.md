# Validator Notes — Adversary / Low Effort / Factual Accuracy

## Holistic Approach

This validation used the Adversary framing: read the document end-to-end as a whole, looking for what feels off before drilling into specific evidence. The goal is pattern detection first, verification second.

With no source material provided, all factual accuracy checks were grounded in:
- Internal document consistency (claims that contradict other claims in the same document)
- Domain plausibility (claims that are implausible for a system of this type)
- Traceability of named references (internal section references, named policies, cited benchmarks)

## Patterns Followed

**1. Overview-to-body consistency check.**
The Overview establishes the architectural contract. Every major claim in the Overview was checked against the body sections. This is where the parallel/sequential contradiction surfaced immediately: the Overview declares all stages run in parallel, Stage 2 explicitly breaks that.

**2. Extraordinary claims scan.**
Any specific numeric claim (percentages, multipliers, thresholds) was treated as suspicious until a source was identified. In a final architecture brief, numbers without provenance are either fabricated or belong to an unreferenced benchmark. The 99.9% latency reduction is the clearest case — it is both extreme and unexplained.

**3. Internal reference resolution.**
Named references to other sections, policies, or documents were traced within the document. "Section 6" does not exist. "Standard retry policy" is named but never defined or referenced.

**4. Domain coherence check.**
Claims were evaluated against the stated domain context: a high-volume event stream ETL system processing 50,000 events/second. The Performance Characteristics section references "files under 10MB" — a framing that belongs to file-processing systems, not event pipelines. This signals either a copy-paste from a different context or an incoherent analogy.

**5. Re-examination pass (skepticism 3 requirement).**
After the initial read surfaced four findings, a second pass confirmed each one and checked for additional issues. The authentication vagueness in Stage 1 was considered but not flagged — vagueness in an architecture brief is a coherence concern (different lens), not a factual accuracy concern. No additional accuracy findings surfaced in the second pass.

## What Was Clean

- Stage counts and stage sequencing (aside from the overview contradiction) are internally consistent.
- The deduplication window (5-minute), micro-batch size (500 records), metrics endpoint path (`/metrics`), and retry count (3 attempts) in Stage 3 are all stated once and not contradicted elsewhere.
- The sub-second p95 latency claim is plausible for this system type and is not contradicted internally.
- The Prometheus integration claim is consistent with the `/metrics` endpoint and standard observability practice.

## Scoring

| Finding | Severity | Weight |
|---------|----------|--------|
| ACCURACY-001: parallel/sequential contradiction | high | -8 |
| ACCURACY-002: 99.9% latency claim | high | -8 |
| ACCURACY-003: broken Section 6 reference | medium | -3 |
| ACCURACY-004: file-size benchmark incongruent with domain | medium | -3 |
| ACCURACY-005: undefined "standard retry policy" | low | -1 |

Final score: 100 - 23 = **77 / 100 — Fair**
