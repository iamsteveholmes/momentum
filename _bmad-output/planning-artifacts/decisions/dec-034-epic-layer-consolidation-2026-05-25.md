---
id: DEC-034
title: Epic-Layer Consolidation — Unify Features and Categorical Epics Into One Concept
date: '2026-05-25'
status: decided
source_research:
  - path: _bmad-output/planning-artifacts/assessments/aes-003-practice-ledger-defects-and-epic-unification-2026-05-25.md
    type: assessment
    date: '2026-05-25'
prior_decisions_reviewed:
  - DEC-002 (Feature Visualization and Developer Orientation — established features.json as the value-delivery container)
  - DEC-004 (Feature Schema Value-First Redesign — added value_analysis and system_context to features.json)
  - DEC-005 (Cycle Redesign Feature-First Practice — established feature as the unit of user value)
  - DEC-006 (Artifact Redesign Dual-Audience — feature dashboard and story template patterns)
  - DEC-031 D2 (Legibility-Before-Automation — assigned feature-grooming a taxonomy-merge amendment via epic-feature-collapse-closeable-grouping; this decision completes that direction)
  - DEC-028 (Beads Tracker — Beads uses 'epic' for what Momentum was calling 'feature'; epic-layer consolidation aligns naturally)
  - Architecture Decisions 44–49 (Feature Artifact Layer, feature-status, feature-status cache, sprint summary, practice project detection, feature-grooming orchestrator)
architecture_decisions_affected:
  - Architecture Decisions 44–49 — HISTORICAL: feature artifact layer dissolved. Schema migrates into the unified epic concept; momentum:feature-grooming retires (role moves to epic-grooming). Decision 48 (practice project detection) may survive in different form for the canvas.
  - Architecture Read/Write Authority table — UPDATED: features.json row removed; canvas read row updated to point at epics.json; momentum:feature-grooming row removed or restructured into momentum:epic-grooming.
  - Architecture Skills Deployment Classification — UPDATED: feature-grooming → epic-grooming (replaces categorical epic-grooming); feature-breakdown → epic-breakdown.
  - Architecture epic-related sections — REWRITTEN: epic as a unified concept with lifecycle and audience as properties; epics.md narrative restructure into epics.json.
  - PRD FR102–FR113 — SUPERSEDED: feature artifact layer + feature-grooming + feature-breakdown FRs all retired; epic-layer FRs replace them.
  - PRD Epic 13 (Feature Orientation) — HISTORICAL: largely complete; epic concept absorbed into the unified shape.
stories_affected:
  - practice-ledger-features-epics-cascade-sequenced-plan (process story tracking the cascade)
  - All 4 cascade B stories to be created (B1 epic schema migration; B2 create-story input-routing; B3 canvas update; B4 feature-grooming/feature-breakdown restructure)
  - epic-feature-collapse-closeable-grouping (currently backlog intake stub) — superseded by this decision's broader scope
---

# DEC-034: Epic-Layer Consolidation — Unify Features and Categorical Epics Into One Concept

## Summary

Momentum currently maintains two parallel layers of grouping above stories: categorical epics (`epics.md` — 18 long-lived themes like "Foundation", "Stay Oriented with Impetus") and features (`features.json` — 23 finite-lived value-delivery containers with closure semantics). The dual layer was historically motivated: categorical epics carried thematic organization; features carried value-delivery semantics with closure conditions. In practice the dual organization adds coordination cost ("is this a feature or an epic?"), produces parallel write surfaces with different schemas, and leaves 269 stories homed in epics without any feature classification.

DEC-031 D2 already named this conflict and assigned a taxonomy-merge amendment (`epic-feature-collapse-closeable-grouping` story) as the vehicle. AES-003 captured the broader scope: the developer's actual direction is to unify into a single epic concept where **lifecycle** (finite-lived deliverable vs. long-lived ongoing concern) and **audience** (user-facing capability vs. internal/infrastructure) are properties of the epic, not separate organizational layers. The flow/connection/quality taxonomy from features.json may survive for the user-facing finite-lived ones.

This decision adopts the unified epic concept. The schema lives in JSON (`epics.json`) replacing/absorbing `features.json`; the canvas remains the human-readable surface (JSON for LLM and app consumption). The 23 current features migrate into the unified epic shape; the 18 categorical epics are evaluated case-by-case (some dissolve, some survive as long-lived); the 269 unhomed stories get best-effort re-homing during the cascade with `ad-hoc` accepting residue. Skill ownership consolidates: `feature-grooming` becomes `epic-grooming` (replacing the categorical version); `feature-breakdown` becomes `epic-breakdown`; canvas updates to render epics.

The 6 sub-decisions below were ratified directionally during the AES-003 assessment conversation; this document formalizes them.

---

## Decisions

### D1: Unify the epic concept — one layer, not two — ADOPTED

**Research recommended:** Drop the parallel features/categorical-epics layering. Going forward, "epic" is one concept: a grouping of stories with a defined audience and lifecycle. No more parallel `features.json` + `epics.md` with different schemas and different ownership.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The dual layer adds coordination overhead without providing functionality a unified concept doesn't give us. Beads' epic model is exactly the finite-lived deliverable shape — alignment falls out naturally (DEC-028). The "is this a feature or an epic?" question disappears.

### D2: Lifecycle as a property of the epic — ADOPTED

**Research recommended:** Each epic carries a `lifecycle` property with values:
- `finite-lived` — closeable deliverable; has acceptance conditions; done when stories complete and conditions are met
- `long-lived` — ongoing thematic concern; doesn't have a "done" state by design

`ad-hoc` is the canonical existing instance of long-lived. Other current categorical epics get evaluated per-epic: some genuinely warrant long-lived status (rare); most should decompose into finite-lived deliverables.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. Forcing every categorical epic to dissolve would be artificial — some themes (catch-alls, persistent practice concerns) genuinely don't fit a finite shape. Making lifecycle a property captures the reality instead of fighting it. The default mental model becomes "finite-lived unless explicitly justified as long-lived," which keeps practice discipline toward closure without losing the long-lived escape hatch.

### D3: Audience as a property of the epic — ADOPTED

**Research recommended:** Each epic carries an `audience` property with values:
- `user` — ships user-visible capability; user can observe the difference
- `internal` — internal/infrastructure deliverable; not user-visible

The flow/connection/quality taxonomy from features.json may survive as a sub-typing for user-facing epics (or fold into payload).

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The user-facing vs. infrastructure distinction is a real organizational axis we want to preserve from the features layer, but it doesn't deserve its own layer — making it a property on the unified epic concept is the lighter representation. The flow/connection/quality taxonomy is potentially still useful for filtering and reporting, but its survival is a downstream implementation choice for the cascade (B1).

### D4: Schema in JSON — `epics.json` replacing `features.json` — ADOPTED

**Research recommended:** The unified epic concept lives in `epics.json` at `_bmad-output/planning-artifacts/epics.json` (replacing or absorbing `features.json`). JSON for LLM and app readability; canvas is the human-readable surface. `epics.md` (narrative markdown) may survive as a derived view or retire entirely — implementation choice for the cascade.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. JSON gives structured query (DuckDB, jq, app-level reads) and clean schema enforcement; the canvas already provides the human reading surface so we don't need a markdown narrative layer for human consumption. The current `epics.md` is narrative-only with no per-epic frontmatter — it can't carry the new property schema without restructuring, and the narrative-only format isn't pulling enough weight to justify keeping it as the primary store.

### D5: Migration plan — adapt features, evaluate categorical epics, re-home unhomed stories — ADOPTED

**Research recommended:** Three-part migration:
1. **23 current features → 23 epics in the new shape.** Schema fields (`value_analysis`, `system_context`, `acceptance_conditions`, `stories` array) carry forward. Default `lifecycle: finite-lived`. Default `audience: user`.
2. **18 categorical epics → case-by-case evaluation.** Most dissolve and their stories re-home into appropriate finite-lived epics. Some (e.g., `ad-hoc`, possibly "Stay Oriented with Impetus") survive as `lifecycle: long-lived`. Developer judgment per epic.
3. **269 unhomed stories → best-effort re-homing.** Each gets an epic assignment during the cascade. New finite-lived epics may need to be created for groups that share a deliverable shape. `ad-hoc` accepts whatever residue doesn't fit cleanly.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The 23 features have rich schema (value_analysis, system_context, acceptance_conditions) — they're the most well-formed inputs to the new model and migrate cleanly. The 18 categorical epics are messier and require per-epic judgment; the cascade absorbs that work as part of B1. The 269 unhomed stories are the long tail of historical accumulation; perfect re-homing would block the cascade indefinitely, so best-effort with `ad-hoc` as residue keeps the work shippable.

### D6: Skill restructure — feature-grooming/breakdown become epic-grooming/breakdown — ADOPTED

**Research recommended:** Skill ownership consolidates around the unified epic concept:
- `momentum:feature-grooming` → `momentum:epic-grooming` (taking over the role of maintaining the unified epic taxonomy; the existing categorical `epic-grooming` retires — its work moves into the unified skill)
- `momentum:feature-breakdown` → `momentum:epic-breakdown` (enumerating stories needed to ship an epic; reads epics.json instead of features.json)
- Canvas updates to render epics (the features lens becomes an epics lens; cycle timeline + sprint lens unaffected)
- `momentum:create-story` reads epic context (instead of feature context) when classifying stories and injecting upstream context

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The skill ecosystem needs to converge on the unified concept — leaving both feature-grooming and epic-grooming alive in parallel would just preserve the dual-layer problem at the skill level. Renaming + retiring is cleaner than maintaining two. The canvas update is unavoidable because its data source moves (B3 in the cascade handles this; identified by AES-003 Finding 9 as a hidden touchpoint).

---

## Phased Implementation Plan

The cascade plan at `~/.claude/plans/i-like-sequencing-the-optimized-lagoon.md` covers the implementation sequencing for Cascade B (this decision's implementation):

1. **B1 — Epic schema migration** (blocks B2/B3/B4)
   - Define `epics.json` schema with `lifecycle`, `audience`, and the unified property set
   - Migrate 23 features → epics with `lifecycle: finite-lived`, `audience: user`
   - Evaluate 18 categorical epics — dissolve or convert to `lifecycle: long-lived`
   - Re-home 269 unhomed stories — best-effort with `ad-hoc` for residue
   - Freeze `features.json` as `_bmad-output/planning-artifacts/archive/features-pre-2026-05.json`
   - Update architecture.md Decisions 44–49 → historical; Read/Write Authority + Skills Deployment Classification updates
   - Update PRD FR102–FR113 → superseded; Epic 13 → historical
2. **B2 — `momentum:create-story` input-routing update** — reads epic context (instead of feature context) for story creation
3. **B3 — Canvas update** — features lens becomes epics lens; renders from `epics.json`
4. **B4 — `feature-grooming` / `feature-breakdown` restructure** — renamed and reframed as `epic-grooming` / `epic-breakdown`; existing categorical `epic-grooming` retires

Cascade B runs in parallel with Cascade A (DEC-033). Within Cascade B, B1 is the blocking foundation story; B2/B3/B4 follow in pairs per the cascade plan's concurrency constraints (max 2 parallel quick-fix sessions; max 1 touching architecture.md at a time).

The currently-backlog `epic-feature-collapse-closeable-grouping` intake stub is **superseded** by this decision — its scope is absorbed into B1 and the broader cascade. The stub can be dropped or repurposed during cascade execution.

---

## Decision Gates

The following conditions, if reached, would warrant re-opening this decision:

- **Long-lived epics proliferate.** If we find ourselves marking many epics as `lifecycle: long-lived` to avoid closure work, the discipline has slipped. Long-lived should be rare and explicitly justified.
- **The 269 unhomed stories prove un-re-homable.** If the best-effort pass during B1 reveals that a substantial fraction of the unhomed stories don't fit any natural epic shape (and `ad-hoc` swells dramatically), the unified concept may need an additional layer (e.g., "loose work" as its own thing). Revisit the model.
- **JSON-only proves painful for human review.** If canvas rendering bugs or canvas downtime regularly leaves the developer unable to inspect epics, an interim `epics.md` derived view may need to be added back. Decide based on actual canvas reliability.
- **Skill rename creates eval/test churn cost.** If renaming feature-grooming → epic-grooming breaks more eval fixtures than expected, consider absorption-without-rename (keep `feature-grooming` as the name but expand its scope). Lower-friction path if rename cost is real.
- **Beads-side epic semantics drift.** If Beads upstream changes its epic model in a way that diverges from this unified concept, evaluate whether to re-align or to maintain the divergence intentionally.
