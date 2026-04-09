# SDR Template — Strategic Decision Record

This is the canonical template for all SDR (Strategic Decision Record) documents produced
by `momentum:decision`. Every SDR must follow this structure exactly.

---

## Frontmatter Schema

```yaml
---
id: SDR-NNN
title: Descriptive title capturing the source material evaluated and the scope of decisions
date: 'YYYY-MM-DD'
status: decided | deferred | superseded
source_research:
  - path: relative/path/to/source.md
    type: assessment | gemini-deep-research | prior-research | architecture-analysis
    date: 'YYYY-MM-DD'
prior_decisions_reviewed:
  - AD-N (description)
  - SDR-NNN (title)
architecture_decisions_affected:
  - AD-N outcome description
stories_affected:
  - story-slug-1
  - story-slug-2
---
```

### Field Definitions

| Field | Required | Description |
|---|---|---|
| `id` | Yes | Auto-incremented from existing decisions. Read `decisions/index.md` to find next ID. |
| `title` | Yes | Descriptive — captures what was evaluated and the scope of decisions made. |
| `date` | Yes | ISO date in quotes: `'YYYY-MM-DD'` |
| `status` | Yes | `decided` when decisions are final. `deferred` when evaluation complete but no decision yet. `superseded` when replaced by a newer SDR. |
| `source_research` | Yes | List of source documents evaluated. Each entry needs path, type, and date. |
| `prior_decisions_reviewed` | No | Architecture decisions (AD-N) or prior SDRs reviewed during this evaluation. |
| `architecture_decisions_affected` | No | AD entries that change as a result of these decisions, with outcome notes. |
| `stories_affected` | No | Backlog story slugs that are impacted by or created from these decisions. |

### Source Research Types

| Type | When to Use |
|---|---|
| `assessment` | Source is an ASR document from `momentum:assessment` |
| `gemini-deep-research` | Source is a Gemini Deep Research output |
| `prior-research` | Source is a prior research document or spike artifact |
| `architecture-analysis` | Source is an architecture analysis or review |

---

## Body Structure

```markdown
# SDR-NNN: {{title}}

## Summary

One paragraph: what source material was evaluated, what decisions were made overall,
and what the net effect is on the product direction. Capture the key judgment call —
what was adopted vs. rejected vs. deferred, and why the overall direction makes sense.

---

## Decisions

### D1: {{recommendation title}} — {{ADOPTED | REJECTED | DEFERRED | ADAPTED}}

**Research recommended:** {{what the source material said — verbatim or close paraphrase}}

**Decision:** {{adopted / rejected / deferred / adapted — plus any modifications if adapted}}

**Rationale:**
{{developer's explanation in their own words — why this choice, what considerations drove it}}

---

### D2: {{recommendation title}} — {{ADOPTED | REJECTED | DEFERRED | ADAPTED}}

**Research recommended:** {{...}}

**Decision:** {{...}}

**Rationale:**
{{...}}

---

(repeat pattern for each decision)

---

## Phased Implementation Plan

Include only when decisions imply a multi-phase delivery order.

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 1 | First capability | Next sprint | story-slug-1, story-slug-2 |
| 2 | Second capability | After Phase 1 | story-slug-3 |

---

## Decision Gates

Include only when decisions have explicit conditions that must be met before re-evaluation
or before proceeding to a later phase.

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | Phase 1 done | Is X working? | Measurable criterion |
| Gate 2 | Phase 2 done | Should we adopt Y? | Measurable criterion |
```

---

## Decision Status Values

| Status | Meaning |
|---|---|
| `ADOPTED` | Recommendation accepted as-is |
| `REJECTED` | Recommendation explicitly not pursued (with rationale) |
| `DEFERRED` | Evaluation complete, implementation pushed to a later phase or condition |
| `ADAPTED` | Recommendation accepted in modified form — describe the adaptation |

---

## Formatting Conventions

- **Summary** captures the overall judgment, not a list of decisions
- **Decision headlines** must name the recommendation AND the verdict: "D1: LangGraph Migration — REJECTED", not "D1: LangGraph"
- **Research recommended** quotes or closely paraphrases the source — do not rewrite it
- **Decision** is a single clear statement: what was decided and how it differs from the recommendation (if adapted)
- **Rationale** is the developer's reasoning — specific, not generic. "We rejected this because our architecture is fundamentally different" is better than "Not applicable"
- **Phased Implementation Plan** is optional — include only when decisions create multi-phase work
- **Decision Gates** are optional — include only when decisions have explicit re-evaluation conditions

---

## Naming Convention

Files are named: `sdr-NNN-slug-YYYY-MM-DD.md`

- `NNN` = zero-padded 3-digit number (001, 002, ...)
- `slug` = kebab-case, max 5-6 words capturing the subject of evaluation
- `YYYY-MM-DD` = decision date

Example: `sdr-001-agentic-ui-stack-eval-2026-04-07.md`

---

## Registry Entry Format

When updating `decisions/index.md`, add a row to the Decisions table:

```markdown
| SDR-NNN | Title | YYYY-MM-DD | Source doc name | decided |
```

---

## Auto-Increment Logic

1. Read `_bmad-output/planning-artifacts/decisions/index.md`
2. If no entries exist (placeholder row only): use SDR-001
3. If entries exist: find the highest NNN, increment by 1, zero-pad to 3 digits
4. Set `{{sdr_id}}` = `SDR-NNN`
5. Set `{{sdr_filename}}` = `sdr-NNN-slug-YYYY-MM-DD.md`
