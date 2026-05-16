---
id: DEC-021
title: Document Ownership Map — Role-to-Document Pattern Registry
date: '2026-05-16'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-008 (Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy)
  - DEC-013 (Universal Agent Model — No Bucket Distinction, Ask Not Fallback, Sprint Planning as Type Discovery)
architecture_decisions_affected:
  - DEC-008 — extends D1 (three-tier layout) with explicit document ownership per role
stories_affected:
  - architect-base-body (scope clarified)
  - pm-base-body (scope clarified)
  - architect-writer story consolidation (sole-writer unification)
---

# DEC-021: Document Ownership Map — Role-to-Document Pattern Registry

## Summary

Each agent role owns specific document types and file patterns. This ownership map governs who writes, who fixes during AVFL, and who reviews each artifact type. Explicit ownership eliminates ambiguity about the correct agent for any given file and makes the routing table (DEC-023) computable from first principles.

The dev role is intentionally project-defined in its ownership scope. The plugin ships one dev.md base body, but file patterns are declared per-project in the routing table. This separates the universal role contract from project-specific architectural decomposition. Sole-writer agents are unified across callers — architect is architect whether called from quick-fix or a refine wave; pm is pm in all contexts.

## Decisions

### D1: Document ownership assigned per role — ADOPTED

**Developer framing:** Which role owns which document types, and what file patterns does each role govern?

**Decision:** Ownership by role:
- **architect**: architecture.md, ADRs, docs/design/**
- **pm**: prd.md, epics.md, features.json
- **ux**: docs/ux/**, wireframes, design briefs
- **analyst**: momentum/analysis/**, assessments/aes-*.md
- **researcher**: momentum/research/**, raw/research-*.md, synthesis briefs
- **dev**: code files — pattern is project-defined via routing table
- **sm**: sprint/story artifacts (mostly CLI, subagent when needed)
- **qa**: .feature specs + ATDD output (verifier, not writer)
- **e2e**: running app + .feature specs (verifier, not writer)

**Rationale:** Explicit ownership eliminates ambiguity about who writes and who fixes each artifact type. When AVFL produces a finding for a given file path, the ownership map determines the correct fixer without requiring orchestrator-level knowledge of project layout.

---

### D2: Dev role ownership is project-defined — ADOPTED

**Developer framing:** Should the plugin prescribe how many dev variants a project needs and which file patterns they own?

**Decision:** The plugin ships one dev.md base body. Each project defines its own dev variants (e.g., dev-cmp, dev-build, dev-api) via build-agents, with file patterns declared in the routing table. The plugin has no opinion on how many dev variants a project needs.

**Rationale:** File decomposition is a project-specific architectural decision; the practice provides the mechanism, not the prescription. Prescribing dev variants in the plugin would force a project structure that conflicts with projects using different stack decompositions.

---

### D3: Sole-writer agents unified across callers — ADOPTED

**Developer framing:** Are architect-writer (quick-fix) and Architecture update agent (refine wave 2) the same role? Same question for prd-writer and PRD update agent.

**Decision:** Yes. architect-writer (quick-fix) and Architecture update agent (refine wave 2) are the same role: architect. prd-writer (quick-fix) and PRD update agent (refine wave 2) are the same role: pm. These are one base body with multiple callers, not separate definitions.

**Rationale:** Reduces duplication; the role contract is identical across callers. Having separate "writer" variants would fragment the base body inventory and create drift between definitions that should stay in sync.

---

### D4: AVFL fixer ownership follows document type — ADOPTED

**Developer framing:** When AVFL produces a finding, how is the correct fixer agent selected?

**Decision:** The fixer spawn resolves to the document owner for that file path using the routing table, not a generic dev-fixer. A finding in architecture.md routes to architect; a finding in a .kt UI file routes to dev-cmp (or whichever dev variant owns that pattern). See DEC-025 for the full fixer routing design.

**Rationale:** The document owner has the domain knowledge required to fix the artifact correctly. A generic fixer lacks both the role identity and the context needed to produce a correct fix for specialized artifact types.
