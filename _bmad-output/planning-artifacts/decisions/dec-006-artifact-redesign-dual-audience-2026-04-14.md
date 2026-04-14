---
id: DEC-006
title: Artifact Redesign for Dual-Audience Legibility — Story Template, Feature Dashboard, and Story-Level Dependency Graph
date: '2026-04-14'
status: decided
source_research:
  - path: _bmad-output/planning-artifacts/decisions/dec-005-cycle-redesign-feature-first-practice-2026-04-14.md
    type: prior-research
    date: '2026-04-14'
prior_decisions_reviewed:
  - DEC-005 (Momentum Cycle Redesign) — DEC-006 operationalizes D9 (Judgment Frame) and D1 (features first-class) into concrete artifact redesigns
  - DEC-002 (Feature Visualization and Developer Orientation) — dashboard approach extended from flat HTML to hierarchical directory
  - DEC-003 (Feature Status Artifact Design) — flat HTML layout superseded by drill-down directory; exclusion of velocity/percentages preserved
architecture_decisions_affected:
  - Decision 44 (Feature Artifact Layer) — clarified; story template and dashboard consume the redesigned feature schema from DEC-005
  - Decision 45 (Feature Status Skill Standalone with Dual Output) — superseded-partial; HTML output changes from flat report to hierarchical directory with drill-down; dependency graph repositioned from project-feature-level to story-level-per-feature
  - Decision 46 (Feature Status Cache Pattern) — clarified; caching mechanism preserved, cached content shape changes to hierarchical site
stories_affected:
  - create-story-update
  - create-story-advanced-elicitation
  - story-spec-completeness-checklist
  - feature-status (skill redesign)
---

# DEC-006: Artifact Redesign for Dual-Audience Legibility — Story Template, Feature Dashboard, and Story-Level Dependency Graph

## Summary

DEC-005 restructured the Momentum cycle around features and North Star floors but left the *artifacts* the developer reads largely unchanged. This SDR captures three artifact redesigns that emerge from DEC-005 but stand on their own: the story template gains a dual-audience structure (human-consumption section + LLM-consumption section) to combat spec fatigue and keep the human in the loop; the feature dashboard is overhauled from a flat HTML report into a hierarchical directory that serves as the primary navigation tool the developer uses to understand the project (dashboard index → feature detail → story drill-down); and the project-level feature dependency graph — judged unusable at scale — is repurposed as a story-level dependency graph scoped to a single feature, showing the feature's implementing stories plus the non-feature stories they depend on. All three redesigns are themselves candidates to become first-class features in Momentum's own `features.json` once DEC-005's data model lands. A process gap in `momentum:decision` is also flagged: the current skill has no flow for developer-proposed decisions (only research-driven or assessment-driven); DEC-006 itself surfaced this gap and noted it for distill follow-up.

---

## Decisions

### D1: Story Template Dual-Audience Redesign — ADOPTED

**Research recommended:** The cycle analysis and DEC-005 D9 identified the missing human-readable artifact at the feature level (the Judgment Frame). DEC-005 placed the Judgment Frame at the feature grain with story inheritance but did not redesign the story template itself.

**Decision:** Adopted as a story-template overhaul. The story template becomes a single file with two clearly demarcated sections:

- **Human section** — full human-review context for the story. Readable. For feature stories, may reference or include the inherited Feature Judgment Frame from DEC-005 D9; for non-feature stories, stands on its own with story-specific human-readable context. Applies to **all** story types (feature, maintenance, defect, exploration, practice).
- **LLM section** — dense execution spec, AC, implementation guide, test approach, touched files, dependencies, etc. Remains human-readable — the developer may refer to it — but the LLM does not require the human section at all.

The file contains clear markers instructing the LLM which sections are for it. The human section is not a separate file; single-file with two sections is the shape.

**Rationale:**
We need a more human-readable template to allow humans to remain in the loop and reduce spec fatigue. The single-file approach with clear instructions to the LLM about which parts are for it keeps the artifact cohesive. The LLM parts stay readable because the human may refer to them, but the LLM doesn't require the human part. The Judgment Frame (DEC-005 D9) is a feature-level concept; this story-template change is broader — it is the full human review for the story itself, applying to feature and non-feature stories alike.

---

### D2: Feature Dashboard Overhaul — Hierarchical Drill-Down HTML Directory — ADOPTED

**Research recommended:** The cycle analysis noted feature-status is the right surface for feature-layer visibility but is currently descriptive and flat. DEC-003 established the HTML artifact design with status badges, story fractions, and GAP indicators in a single-page layout.

**Decision:** Adopted as an overhaul. The feature dashboard becomes an HTML *directory* rather than a single flat page: a top-level `index.html` dashboard listing all features with their state, plus per-feature drill-down pages that contain the full feature summary, the list of its stories (with gaps), and further drill-down into individual stories. Each drill-down page includes back-navigation. Drilling into a story renders the story's **human section** (from D1); the tool works with whatever inputs exist — most will be stubs from the backlog rather than fully-created story files, and the tool uses whatever the stub has.

The dashboard is the primary tool the developer uses to get a sense of all features in the project and to drill into individual features. It is **read-only**, generated by `feature-status`, with staleness detection preserved from the current implementation (hash-based, based on inputs).

UX wireframes for the hierarchy and page layouts are expected to come from the BMAD UX expert before implementation begins.

**Rationale:**
The current dashboard is useful but needs big updates. A hierarchical directory with drill-down is the right shape because features are the primary unit and the developer needs to drill from project-wide overview to individual features to individual stories. Collapsing to the human section on story drill-down is consistent with D1 and avoids dumping LLM-spec content into a developer-review surface. The dashboard must be read-only (generated, not edited) because it is a view, not a source of truth. Using the BMAD UX expert for wireframes ensures this is designed properly rather than ad-hoc.

This **supersedes DEC-003's flat single-page HTML layout** in structure while preserving DEC-003's signal choices (no velocity, no percentages, status badges + GAP indicator) and DEC-002's feature-artifact role.

---

### D3: Dependency Graph Repurposed from Project-Level Feature Graph to Story-Level Graph Per Feature — ADOPTED

**Research recommended:** The current feature-status artifact includes a feature-level dependency graph showing relationships across the project's features. DEC-003 established graph rendering as part of the HTML output.

**Decision:** Adopted as a repurpose. The project-level feature dependency graph is **removed** — both Momentum and Nornspun have too many features for a project-wide graph to be useful. The concept is repurposed to the story level, scoped per feature: on a feature's drill-down page (from D2), render a dependency graph showing the feature's implementing stories **plus** the non-feature stories those implementing stories depend on (bugs, supporting maintenance, infrastructure). Because `depends_on` is already a required field on every story in `stories/index.json`, the data model supports this without schema changes.

Whether the graph shows only direct dependencies or transitive ones is a UX decision deferred to the BMAD UX expert pass.

**Rationale:**
The project-level feature graph is worthless at our scale — too many features, the graph is too big, and the relationships between stories-and-features are not legible in a single view. Even showing just the features alone is too much for this project or Nornspun. The story-level graph becomes meaningful because it is bounded by a single feature. Including the non-feature stories a feature's implementing stories depend on is the key move: it surfaces the real work needed to deliver the feature, not just the value-bearing stories. The transitive-vs-direct question is legitimately a UX decision; the BMAD UX expert should flesh it out with wireframes.

The dependency data already exists in `stories/index.json` (`depends_on` field per story, plus sprint-time `dependencies` for intra-sprint ordering), so no schema change is required — only consumption-pattern change in feature-status.

---

## Process Note: Decision-Skill Gap Flagged for Distill

While capturing DEC-006, the developer surfaced a gap in the current `momentum:decision` skill: it has three flows (A: from assessment, B: from research, C: revisit prior decision) but no flow for developer-proposed decisions — decisions where the thinking was done outside a document, in conversation or in the developer's head.

DEC-006 was captured by treating the conversation as "research" (Flow B), which is a workaround rather than the correct shape. A Flow D (developer-proposed) should be added to `momentum:decision` so that future SDRs capturing developer-originated decisions don't have to be forced through a research flow they don't belong in.

This process improvement is noted for the distill pipeline as a skill-improvement signal. It is not itself part of the decision set in this SDR.

---

## Phased Implementation Plan

DEC-006 depends on DEC-005's data model (Phase 1 in DEC-005). The three redesigns can proceed in parallel once the feature/story schema changes land, but they have different readiness profiles.

| Phase | Focus | Depends on | Key stories |
|-------|-------|------------|-------------|
| 1 | **Story template v2 design** — define the dual-section template; clear LLM-section markers; handle feature and non-feature stories; update `create-story` and its sub-skills to generate this shape. | DEC-005 Phase 1 (Judgment Frame schema) | `create-story-update`, `create-story-advanced-elicitation`, `story-spec-completeness-checklist` |
| 2 | **Dashboard UX wireframes** — BMAD UX expert pass producing wireframes for dashboard index, feature drill-down page, story drill-down view, and story-level dependency graph. Output consumed by Phase 3. | DEC-005 Phase 1 (feature schema) | UX spike story (may need new stub) |
| 3 | **Dashboard generation rewrite** — `feature-status` rewritten to produce an HTML directory rather than a single page; preserve staleness detection; collapse story views to human section; render story-level dependency graphs per feature. | Phase 2 wireframes | `feature-status` skill rewrite |
| 4 | **Treat each redesign as a Momentum feature in its own right** — once DEC-005's features.json schema lands, register these three redesigns as Momentum features with North Stars, so they are tracked by the same dashboard they are building. | DEC-005 Phase 1 | features.json additions |

Phase 2 (UX wireframes) is the critical path — Phase 3 should not begin without them, or the dashboard redesign will drift toward whatever the implementer thinks looks right.

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| G1 | After Phase 1 lands | Does the new story template actually reduce spec fatigue? | Developer can open a story and understand the human section in under 60 seconds without consulting the LLM section |
| G2 | After Phase 2 wireframes | Are the wireframes coherent with DEC-005's feature-first model? | Wireframes show feature as the primary navigation unit; drill-down to story renders human section; story-level graph bounded by feature |
| G3 | After Phase 3 lands | Is the dashboard usable as the primary project-navigation tool? | Developer uses dashboard (not backlog grep, not features.json inspection) as the default way to get project state |
| G4 | After 3 months of use | Does the dashboard decay gracefully when stubs are incomplete? | Stubs missing human-section content degrade to "content pending" placeholders, not dashboard errors |

---

## Full Story Audit

The `stories_affected` frontmatter lists the directly-impacted stories. The complete audit:

### Story template (D1)
- `create-story-update` — restructure create-story output into dual-section template
- `create-story-advanced-elicitation` — elicitation must produce content for both sections appropriately
- `story-spec-completeness-checklist` — checklist must validate both sections exist and have required content

### Feature dashboard + dependency graph (D2, D3)
- `feature-status` — skill rewrite: hierarchical HTML directory, drill-down pages, human-section rendering on story pages, story-level dependency graph per feature, project-level feature graph removed
- Any downstream stories currently consuming the flat feature-status HTML would need to adapt to the directory structure (not identified in this audit; may surface during Phase 3 implementation)

### New stub needed (not yet in backlog)
- **UX wireframe spike** for the new dashboard — owner to create this via `momentum:intake` once DEC-006 commits; it's the gating input for the Phase 3 implementation

### Interaction with DEC-005 Phase 1
- All story-template stories in DEC-005 (under "Feature layer") now also need to accommodate the DEC-006 D1 dual-section shape. Sequencing: DEC-005 Phase 1 lands first (schema), DEC-006 Phase 1 follows (template shape uses the schema).
