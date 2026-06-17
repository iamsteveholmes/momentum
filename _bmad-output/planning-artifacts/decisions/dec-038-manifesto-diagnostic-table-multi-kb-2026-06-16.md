---
id: DEC-038
title: "Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB Architecture"
date: '2026-06-16'
status: decided
source_research:
  - path: .momentum/handoffs/manifesto-cmp-dev-recovery-2026-06-16.md
    type: prior-research
    date: '2026-06-16'
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-06-16'
prior_decisions_reviewed:
  - DEC-008 (Composable Specialist Agents Architecture — three-tier layout)
  - DEC-015 (KB Cold-Context Delivery — constitution triggers)
  - DEC-018 (Obsidian Wiki Skills — wiki-query as cold KB interface)
  - DEC-023 (Agent Routing Table — machine-readable registry)
  - DEC-026 (Build Pipeline Redesign — build-agents, agent-builder, constitution-builder)
  - DEC-027 (Skill/Agent Development — skill-creator pipeline)
architecture_decisions_affected:
  - DEC-026 D4 — manifesto definition refined: manifesto = per-agent diagnostic table; agent-specific routing is owned at the manifesto/agent-builder layer, not the shared constitution
  - DEC-023 — routing is resolved per-agent (role × domain), consistent with the per-agent manifesto
  - DEC-018 — wiki-query cold-KB interface extended to support multiple, per-project KBs
  - DEC-008 — three-tier model retained; "manifesto" tier given its canonical definition (diagnostic table)
  - PRD FR136 / FR138 — annotate: manifesto is the agent's stable diagnostic table, NOT a per-sprint/per-story context overlay
stories_affected:
  - agent-manifesto-format-specification
  - constitution-builder-write-mode-parameterization
  - constitutionmd-generation-acceptance-criteria
  - build-guidelines-skill
  - specialist-classify-update-for-gen-2-paths
---

# DEC-038: Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB Architecture

## Summary

A discovery effort (workflow `wxygicz8y`) recovered the developer's nornspun **`cmp-dev`** prototype
agent — the origin of the "manifesto" concept — as a committed on-disk artifact
(`nornspun-client/.claude/agents/cmp-dev.md`). The prototype's core is a per-role×domain table mapping
*observable developer symptoms → exact `wiki-query` lookups* against a cold Obsidian KB. Momentum's
specs had drifted into **three contradictory definitions** of "manifesto" (DEC-026 D4, the format
story, PRD FR136), none of which captured this. Two decisions resolve the drift: **D1** ratifies one
canonical definition — the manifesto **is** the agent's *diagnostic table* — and **D2** establishes a
**per-project, multi-KB** architecture in which agents are project-scoped. Net direction: the upcoming
agent-cohort sprint builds to the recovered design rather than re-deriving it, and gains an explicit
KB-buildout workstream. Full evidence and verbatim exemplar:
`.momentum/handoffs/manifesto-cmp-dev-recovery-2026-06-16.md` and
`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`.

---

## Decisions

### D1: The manifesto is the agent's diagnostic table — ADOPTED

**Developer framing:** The three existing definitions (DEC-026 D4 "agent-specific routing"; the
`agent-manifesto-format-specification` story "role × domain matrix plus stack facts"; PRD FR136
"project/sprint context overlay") are imprecise attempts at the same idea. The developer wants one
clear definition, grounded in the recovered `cmp-dev` prototype.

**Decision:** The manifesto **is** the agent's **diagnostic table** — a **stable**, per-role×domain
table mapping *observable developer symptoms → the exact `wiki-query` KB lookup* for each, plus the
stack facts that scope it. Key clarifications:
- **Stable, not per-story.** The manifesto is the *same* across every sprint and every story — it is
  the agent's standing "how everything is implemented" guidance. The PRD FR136 "sprint/story context
  overlay" reading is **rejected**.
- **Completeness criterion.** If an agent hits a situation the manifesto does not guide, the manifesto
  is **incomplete** — this becomes an acceptance criterion on the format story.
- **Canonical term:** "diagnostic table."
- **Reconciliation:** DEC-026 D4, the format story, and PRD FR136/FR138 are annotated/superseded to
  read consistently under this definition. `constitution-builder`'s currently project-*shared*
  `## Quick Routing` ownership must be reconciled against the **per-agent** routing this implies
  (a shared Compose/Kotest table is meaningless for a `pm` or `architect`).
- **Reference exemplar:** `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` (verbatim nornspun
  `cmp-dev.md`; ~35 worked symptom→`wiki-query` entries across 9 technology areas).

**Rationale:** The recovered prototype proves the valuable, hard-won artifact is a *per-specialist*
diagnostic table — the quality of symptom phrasing (specific, observable, diagnostic) is what makes
it work, and it was a day of human design + testing. The three drifted specs would have had the
cohort sprint re-derive this from scratch. Naming it precisely ("diagnostic table") and fixing it as
*stable per-agent* removes the ambiguity that blocked the format story.

---

### D2: Per-project KBs, multi-KB support, project-scoped agents — ADOPTED

**Developer framing:** `cmp-dev` and `nornspun-agentic-kb` are **nornspun** artifacts, not Momentum
artifacts. The developer wants it explicit that Momentum agents are different from nornspun agents and
draw on a different knowledge base.

**Decision:** Knowledge bases and agents are **project-scoped**:
- `cmp-dev.md` is a **format exemplar only** — never a Momentum agent.
- **Momentum needs its own KB**; nornspun keeps its own; **multiple KBs are allowed.**
- **Agents are project-scoped** (nornspun agents ≠ momentum agents).
- **Consequence:** "build the agents" now also includes **standing up each project's KB** (a distinct
  workstream), plus a **multi-KB support requirement** on the `build-agents` pipeline and the
  `wiki-query` interface (DEC-018 extended).

**Rationale:** A manifesto's diagnostic table only has value against a real KB whose pages match its
queries. Momentum's agents will diagnose Momentum problems against Momentum knowledge — a separate KB
from nornspun's. Making this explicit prevents conflating the recovered nornspun exemplar with
Momentum's actual cohort and surfaces the KB-buildout as real, sequenced work rather than an
afterthought.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 0 | Settle the format: load the diagnostic-table schema + completeness AC + exemplar | Pre-sprint (create-story) | agent-manifesto-format-specification |
| 1 | Reconcile constitution vs. per-agent routing ownership | Cohort sprint | constitution-builder-write-mode-parameterization, constitutionmd-generation-acceptance-criteria |
| 2 | Pipeline consumes manifesto + multi-KB; produce ONE real composed agent | Cohort sprint | build-guidelines-skill, specialist-classify-update-for-gen-2-paths |
| 3 | New work: stand up the Momentum KB; manifesto-builder (generate-then-curate) | New stories (to create) | (momentum-kb-buildout), (manifesto-builder-generate-then-curate) |

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| G1 | Phase 2 done | Does the pipeline actually produce a composed agent? | At least one composed agent file written + registered in `agents.json` project block (it never has) — validate against the `cmp-dev` exemplar shape |
| G2 | Phase 3 scoping | Authored vs. generated manifesto? | Decide whether `manifesto-builder` auto-drafts entries from the KB (then human-curates symptom phrasing) or manifestos are hand-authored — the prototype shows curation quality is the expensive part |

---

## Open Items (not blocking this decision)

- **Registry hygiene:** the decisions index was missing the `DEC-037` row (file exists on disk); add
  it when convenient.
- **Two new stories to create** for Phase 3: a Momentum-KB buildout, and a `manifesto-builder`
  (generate-then-curate) skill — pending the G2 authored-vs-generated call.
