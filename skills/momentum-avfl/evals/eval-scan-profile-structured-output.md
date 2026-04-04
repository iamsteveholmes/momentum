# Eval: Scan Profile — Structured Output Format

## Scenario

Given AVFL is invoked with:
- `profile: scan`
- `output_to_validate`: a document containing issues across multiple lenses (structural gaps, factual errors, coherence problems, domain violations)
- `source_material`: the original ground truth
- `domain_expert`: "software engineer"
- `task_context`: "product requirements document"

## Expected Behavior

1. The scan profile produces a structured findings list suitable for team handoff (output_format: `structured_handoff`)
2. Each finding in the output includes ALL of these required fields:
   - `id` — unique finding identifier
   - `severity` — critical, high, medium, or low
   - `confidence` — HIGH or MEDIUM (from dual-reviewer cross-check)
   - `lens` — which of the four lenses surfaced it (structural, accuracy, coherence, domain)
   - `dimension` — specific dimension within the lens (e.g., structural_validity, correctness)
   - `location` — where in the document the issue exists (section/line, or {filename}:{section} in corpus mode)
   - `description` — what is wrong
   - `evidence` — quoted text or specific reference proving the issue exists
   - `suggestion` — actionable recommendation for resolution
3. Findings are ordered by severity (critical first, then high, medium, low), then within each severity tier by confidence (HIGH before MEDIUM)
4. No finding is emitted without evidence — findings lacking evidence are discarded during consolidation

## Anti-Behaviors (must NOT happen)

- Findings are NOT in arbitrary order — the severity-then-confidence sort is required
- No finding is emitted missing any of the 9 required fields
- The output is NOT a corrected document — it is a findings list only
