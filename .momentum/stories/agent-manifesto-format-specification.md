---
title: Agent manifesto format specification
story_key: agent-manifesto-format-specification
status: ready-for-dev
priority: high
epic_slug: momentum-agent-composition-pipeline
feature_slug: momentum-composable-specialist-agents
story_type: feature
change_type:
  - specification
verification_method_advisory: document-review
depends_on: []
touches:
  - skills/momentum/references/manifesto-format.md
  - _bmad-output/planning-artifacts/architecture.md
---

# Agent manifesto format specification

## Story

As a developer,
I want a defined schema, location, and content model for the agent manifesto — the agent's diagnostic table — that build-guidelines consumes,
so that build-guidelines can generate composed Tier 2 specialist agent files without ambiguity.

## Description

Define schema, location, and content model of the agent manifesto that build-guidelines consumes to produce composed specialist files.

Per DEC-038, the manifesto **is** the agent's **diagnostic table**: a **stable**, per-role×domain table that maps each *observable developer symptom → the exact `wiki-query` KB lookup* that resolves it, plus the **stack facts** that scope those lookups. The table is the *same* across every sprint and every story — it is the agent's standing "how everything is implemented here" guidance, not a per-sprint or per-story context overlay (that earlier reading is rejected). Without this format, build-guidelines cannot generate Tier 2 composed agents.

**Pain context:** build-guidelines currently has no defined input format. Without a manifesto spec, the skill cannot know which role × domain diagnostic table to compose, what stack facts to include, or which project KB the symptom→`wiki-query` entries resolve against. This blocks all downstream composed-specialist work.

The manifesto is **project-scoped**: its diagnostic table targets one project's knowledge base, and `wiki-query` (DEC-018, extended) resolves against that project's KB. Momentum agents draw on the Momentum KB; nornspun agents draw on the nornspun KB; the format must carry which KB it scopes to. The recovered nornspun `cmp-dev` prototype (`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`) is the reference shape the format must capture — it is a **format exemplar only**, never a Momentum agent.

## DEC-038 Alignment

This is the canonical format story for the manifesto; DEC-038 fixes the definition it must encode. The earlier framings ("role × domain matrix plus stack facts" here; "agent-specific routing" in DEC-026 D4; "project/sprint context overlay" in PRD FR136) are superseded by one definition:

- **The manifesto IS the agent's diagnostic table** — stable, per-role×domain, mapping observable developer symptom → exact `wiki-query` KB lookup, plus the stack facts that scope it. Same across every sprint and story; the per-sprint/per-story overlay reading is **rejected**.
- **Completeness is an acceptance criterion on this story:** an agent hitting territory the diagnostic table does not guide means the manifesto is incomplete, and the format must make that gap detectable.
- **Project-scoped, multi-KB:** the format scopes to one project's KB; multiple per-project KBs are supported, with `wiki-query` (DEC-018) extended accordingly.
- **Reference exemplar:** `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` (verbatim nornspun `cmp-dev.md`; ~35 worked symptom→`wiki-query` entries across 9 technology areas) is the shape the format must capture — format-only, never a Momentum agent.

See `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` (Phase 0).

## Acceptance Criteria

1. **A manifesto format reference document exists** at `skills/momentum/references/manifesto-format.md`. It is the single authoritative specification of the manifesto file — its location convention, identity, content model, and completeness rule — written so that build-guidelines (and a human author) can produce a conformant manifesto from it alone, with no other document required. (DEC-038 D1; AC verified by document inspection.)

2. **The format models a stable, per-role×domain diagnostic table.** The spec defines the manifesto as a table whose every entry pairs an *observable developer symptom* (the trigger) with the *exact `wiki-query` KB lookup* (the resolution) — symptom → `wiki-query` terms. The spec states explicitly, in normative language, that the manifesto is **stable** across every sprint and every story and is **not** a per-sprint/per-story context overlay (DEC-038 D1; the overlay reading is rejected).

3. **Each manifesto is keyed by `role` × `domain`.** The format specifies that a manifesto carries an explicit `role` (e.g. `dev`, `qa`, `e2e`, `architect`, `pm`) and `domain` (e.g. `kotlin-compose`, `python-fastapi`) identity, such that build-guidelines can resolve which composed agent file (`.claude/guidelines/agents/{role}-{domain}.md`) a manifesto produces. (DEC-038 D1; architecture.md Decision 56.)

4. **The format captures the stack facts that scope the table.** The spec defines a stack-facts section (language, frameworks, test tooling, version pins, architecture paradigm — e.g. the exemplar's "CMP 1.10.2 · Material3 · Ktor · SQLDelight · Kotest · Turbine · MVI" line) and explains that these scope and disambiguate the symptom→`wiki-query` lookups. (DEC-038 D1; exemplar §"Project Stack".)

5. **The format is project-scoped and declares its KB.** The spec requires every manifesto to record **which project KB** its `wiki-query` entries resolve against, and states that multiple per-project KBs coexist (Momentum agents → Momentum KB; nornspun agents → nornspun KB). It references that this requires `wiki-query` (DEC-018) to be extended for multi-KB resolution, without itself implementing that extension. (DEC-038 D2; PRD FR142.)

6. **The format makes completeness verifiable (completeness criterion).** The spec defines what "complete" means for a manifesto and how an incompleteness gap is detected and surfaced rather than hidden: an entry whose symptom matches a situation the agent hits but whose `wiki-query` returns nothing usable, or a situation the agent hits for which **no** symptom entry exists, both mean the manifesto is **incomplete**. The spec states the detectable signal (e.g. an agent reaching un-routed territory is an explicit incompleteness signal to log, not a silent fallthrough). (DEC-038 D1 completeness criterion — this is the load-bearing AC of the story.)

7. **The format is exemplar-complete — it can express every entry in the reference exemplar.** The spec is validated against `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`: every one of the exemplar's ~35 worked symptom→`wiki-query` entries across its 9 technology areas (Compose recomposition/side-effects, Compose layout/lists, Compose animation, MVI/state, navigation, Kotest coroutines/flow, Kotest assertions/data, SQLDelight, Ktor, Material3) is expressible in the format with no loss of meaning. The spec documents this exemplar-conformance check (e.g. a mapping note or worked example showing exemplar entries rendered in the format). The exemplar is treated as a **format reference only — never a Momentum agent.** (DEC-038 D1, D2; story Description.)

8. **build-guidelines can parse the manifesto and route on it.** The spec defines the manifesto in a form (sections/fields and their semantics) that build-guidelines can read to determine: which `role`×`domain` composed file to generate, which stack facts to bake in, and which project KB to scope `wiki-query` to. The spec is consistent with how `build-guidelines-skill` declares it consumes the diagnostic table (the manifesto is a composition *input*; build-guidelines does not regenerate or re-scope it per sprint). (Consistency with `.momentum/stories/build-guidelines-skill.md` AC1–AC4 and architecture.md `agent-builder inputs`.)

9. **The manifesto location and naming convention are documented in architecture.md.** A manifesto-format subsection (under the Decision 56 manifesto definition block) records the canonical on-disk location of the format reference (`skills/momentum/references/manifesto-format.md`) and the manifesto file's location/naming convention, so the architecture's manifesto definition points to the format spec rather than only describing it narratively. (Existing AC preserved; architecture.md Decision 56.)

10. **All cross-references resolve and the diagnostic-table vocabulary is used throughout.** Every path, decision id (DEC-038, DEC-018, DEC-026 D4), FR (FR136, FR138, FR142), and section reference in the new reference doc and the architecture.md edit resolves correctly; the document uses the canonical term **"diagnostic table"** and never reintroduces the rejected "context overlay" framing. (DEC-038 D1 canonical term; verification-standard.md cross-reference verification.)

## Tasks / Subtasks

- [ ] **Task 1 — Author the manifesto format reference doc** (AC1, AC2, AC3, AC4, AC5, AC6, AC8)
  - [ ] Create `skills/momentum/references/manifesto-format.md`, matching the house style of existing schema/format references (e.g. `finding-schema.md`, `sprint-tracking-schema.md`): title + version line, a normative definition, a field/section table, and worked examples.
  - [ ] Define the manifesto identity block: `role`, `domain`, and the **project KB** the manifesto scopes to (AC3, AC5).
  - [ ] Define the stack-facts section and its purpose (scopes/disambiguates lookups) (AC4).
  - [ ] Define the diagnostic-table section: the symptom → `wiki-query` entry shape, grouped by technology/concern area, with normative guidance on symptom phrasing (specific, observable, diagnostic) and on the `wiki-query` invocation form (AC2, AC8).
  - [ ] Write the normative "stable, not per-story; not a context overlay" statement using the canonical term "diagnostic table" (AC2, AC10).
- [ ] **Task 2 — Specify the completeness criterion** (AC6)
  - [ ] Define "complete" for a manifesto and the two incompleteness conditions (no matching symptom entry; entry whose `wiki-query` returns nothing usable).
  - [ ] Specify the detectable signal an agent emits on reaching un-routed territory (an incompleteness signal to surface, not a silent fallthrough), so the gap is detectable rather than hidden.
- [ ] **Task 3 — Validate the format against the reference exemplar** (AC7)
  - [ ] Walk `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`; confirm all ~35 symptom→`wiki-query` entries across its 9 technology areas are expressible in the format with no loss.
  - [ ] Capture the exemplar-conformance check in the reference doc (a mapping note or one worked example rendering exemplar entries in the format), labeling the exemplar format-only / never a Momentum agent.
- [ ] **Task 4 — Document the location/naming convention in architecture.md** (AC9, AC10)
  - [ ] In the Decision 56 manifesto definition block, add a manifesto-format subsection citing `skills/momentum/references/manifesto-format.md` as the canonical format spec and recording the manifesto file's location/naming convention.
  - [ ] Confirm consistency with the existing `agent-builder inputs` (`manifesto`) and `build-guidelines-skill` consumption framing.
- [ ] **Task 5 — Cross-reference + vocabulary verification** (AC10)
  - [ ] Verify every path, DEC id, FR id, and section reference in the new doc and the architecture.md edit resolves.
  - [ ] Confirm "diagnostic table" is used as the canonical term and "context overlay" is never reintroduced.

## Dev Notes

### Decision Authority

DEC-038 (`_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md`) is the binding authority for this story. Its Phased Implementation Plan places `agent-manifesto-format-specification` in **Phase 0 — "Settle the format: load the diagnostic-table schema + completeness AC + exemplar."** Two decisions govern:

- **D1 (manifesto = diagnostic table, ADOPTED):** the manifesto is the agent's stable, per-role×domain table mapping observable symptom → exact `wiki-query` lookup + scoping stack facts. Stable, not per-story. Completeness is an AC on *this* story (AC6). Canonical term: "diagnostic table." The "sprint/story context overlay" reading (PRD FR136/FR138) is **rejected**.
- **D2 (per-project KBs, multi-KB, project-scoped agents, ADOPTED):** the format scopes to one project's KB (AC5); `cmp-dev.md` is a format exemplar only, never a Momentum agent (AC7).

This story does **not** decide authored-vs-generated manifestos (DEC-038 Gate G2) — that is downstream (`manifesto-builder-skill-generate-then-curate`). It defines the *format* the generator or human author must produce.

### Current State of Affected Files

- **`skills/momentum/references/manifesto-format.md`** — does not yet exist. No manifesto-format reference is on disk today (grep for "manifesto format" / "diagnostic table" / "manifesto schema" under `skills/momentum/references/` and `skills/momentum/skills/build-guidelines/` returns nothing). This story creates it. House style to match: the other format/schema references in `skills/momentum/references/` (`finding-schema.md`, `sprint-tracking-schema.md`, `build-results-ledger-schema.md`) — each opens with a title + version line, gives a normative definition, then a field table and worked examples.
- **`_bmad-output/planning-artifacts/architecture.md`** — Decision 56 (around lines 3030–3073) already carries the canonical manifesto definition (DEC-026 D4 / DEC-038), the `agent-builder inputs` table where `manifesto` = "the agent's diagnostic table", routing-ownership, multi-KB, and the FR136/FR138 annotation. What is **missing** is an explicit pointer to the format reference doc and the manifesto file's location/naming convention (AC9). The edit is additive — a manifesto-format subsection under the existing Decision 56 block. **Preserve** every existing line in that block; do not restate or contradict the DEC-038 definition already there.
- **`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`** — exists (259 lines), read-only input. The verbatim nornspun `cmp-dev.md`; its `## Quick Routing — wiki-query Delegation Table` (≈ lines 121–192) is the worked diagnostic table the format must be able to express, and `## Project Stack` (≈ lines 44–54) is the stack-facts shape. **Format reference only — never a Momentum agent; do not register, spawn, or treat as one** (the file's own header banner says so).
- **`build-guidelines-skill` story** (`.momentum/stories/build-guidelines-skill.md`) — the primary downstream consumer. Its AC1–AC4 state build-guidelines consumes the diagnostic table as a sprint-invariant composition input, drives `wiki-query` against the project's own KB, and treats un-routed territory as a manifesto-incompleteness signal. This format spec must be consistent with that consumption contract (AC8). build-guidelines itself is **not** edited by this story.

### Architecture Compliance

- **Decision 56 / DEC-026 D4 / DEC-038 (architecture.md):** the composed Tier 2 specialist = base body + constitution + manifesto. The `manifesto` agent-builder input is canonically "the agent's diagnostic table." This story formalizes that input's format. The format must keep routing ownership where DEC-038 puts it: symptom→`wiki-query` routing lives in the **per-agent manifesto**, **not** the shared constitution (a single shared Compose/Kotest routing table is meaningless for a `pm` or `architect`). The format must therefore be inherently per-role×domain (AC3) so it cannot be mistaken for the project-shared constitution's `## Quick Routing`.
- **DEC-018 extended (multi-KB):** `wiki-query` is the cold-KB interface. The format declares the project KB to scope against (AC5) but does **not** implement the `wiki-query` multi-KB extension — that is FR142 / `wiki-query`-side backlog work. Keep the boundary clean: this story specifies *what the manifesto declares*, not *how `wiki-query` resolves it*.
- **PRD FR136 / FR138 / FR142:** FR136 and FR138 already carry the DEC-038 annotation that the overlay reading is rejected and the manifesto is the stable diagnostic table; FR142 carries the per-project multi-KB / KB-buildout workstream. The reference doc and architecture edit must read consistently with these (AC10) — no reintroduction of "context overlay."
- **Epic acceptance condition (`momentum-agent-composition-pipeline`):** "build-guidelines produces ONE constitution AND one manifesto per (role × domain), with sprint-dev composing all three." This format is the contract that makes "one manifesto per (role × domain)" well-defined.

### Testing Requirements

- **Verification method (advisory): `document-review`.** Per `skills/momentum/references/rules/verification-standard.md` §1, `change_type: specification` → `document-review`. This story produces specification artifacts (a reference doc + an architecture.md subsection); there is no executable surface, so verification is by inspection and cross-reference, not by tests or evals.
- **What document-review checks here:**
  - The reference doc satisfies every AC by inspection (AC1–AC8, AC10) — completeness, the stable/not-overlay statement, role×domain keying, stack facts, KB scoping, the completeness criterion, and exemplar-expressibility are all present and normative.
  - **Exemplar-conformance (AC7) is the substantive review gate:** confirm every exemplar entry maps into the format. This is a concrete, reviewable check against `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`, not a judgment call.
  - All cross-references resolve (paths, DEC/FR ids, section names) and the canonical "diagnostic table" vocabulary is used throughout (AC10).
- **No insider knowledge (verification-standard.md §4):** all checks are performable by an ordinary reader of the spec, the exemplar, and architecture.md — no implementation internals required.
- AVFL checkpoint (run automatically by `momentum:dev`) validates the produced artifacts against these ACs.

### Project Context Reference

- Authoritative epic: `momentum-agent-composition-pipeline` ("Agent Composition Pipeline — Constitution + Manifesto + Base Body"). This story is the Phase-0 format settle that unblocks Phase 1 (constitution-vs-routing reconciliation) and Phase 2 (`build-guidelines-skill` consuming the manifesto). Note: the story file's frontmatter previously read `agent-team-model` (a feature slug that is no longer an epic key); the authoritative epic per the stories index is `momentum-agent-composition-pipeline`.
- Sibling format story: `agents-md-manifest-format` (per-skill agent role slots) is a *different* manifest — that one declares which roles a skill spawns; *this* one defines the per-agent diagnostic table. Keep the two distinct in vocabulary.

### References

- `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` — canonical manifesto = diagnostic-table definition, completeness criterion, per-project multi-KB scope (D1, D2; Phase 0).
- `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` — format reference exemplar (verbatim nornspun `cmp-dev.md`; ~35 symptom→`wiki-query` entries across 9 tech areas). Format-only; never a Momentum agent.
- `_bmad-output/planning-artifacts/architecture.md` Decision 56 (≈ lines 3030–3073) — manifesto canonical definition, `agent-builder inputs` (`manifesto` = diagnostic table), routing ownership, multi-KB, FR136/FR138 annotation; the edit target for AC9.
- `_bmad-output/planning-artifacts/prd.md` FR136 / FR138 / FR142 — Gen-2 composition model, agent-builder pipeline, per-project multi-KB architecture (all DEC-038-annotated).
- `.momentum/stories/build-guidelines-skill.md` — primary downstream consumer; AC1–AC4 define how the diagnostic table is consumed as a sprint-invariant input (consistency target for AC8).
- `skills/momentum/references/finding-schema.md`, `skills/momentum/references/sprint-tracking-schema.md` — house-style references for format/schema documents.
- `skills/momentum/references/rules/verification-standard.md` §1, §4 — `specification` → `document-review`; anti-insider-knowledge guard.
- Epic context: `momentum-agent-composition-pipeline` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 5 → specification (direct authoring of `skills/momentum/references/manifesto-format.md` + the exemplar-conformance and cross-reference verification within it)
- Task 4 → specification (additive edit to `_bmad-output/planning-artifacts/architecture.md` Decision 56)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (DEC-038, the epic record, and the reference exemplar) — not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per the story's acceptance criteria. The new reference doc (`skills/momentum/references/manifesto-format.md`) is the primary deliverable; the architecture.md subsection (Task 4) is the secondary, additive deliverable. Match the house style of existing `skills/momentum/references/` schema docs (title + version line, normative definition, field/section table, worked examples).
2. **Verify cross-references:** All references to other documents, files, sections, or identifiers must resolve correctly — every path, DEC id (DEC-038, DEC-018, DEC-026 D4), FR id (FR136, FR138, FR142), and architecture.md section name. Confirm the exemplar path and its cited sub-sections resolve (AC7, AC10).
3. **Verify format compliance:** the reference doc follows the established Momentum reference-doc convention; the architecture.md edit slots under the existing Decision 56 manifesto block without restating or contradicting the DEC-038 definition already there.
4. **Run the exemplar-conformance check (AC7) as the substantive review step:** walk every symptom→`wiki-query` entry in `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` and confirm each is expressible in the format. This is concrete and reviewable — treat any inexpressible entry as a format gap to fix before marking done.
5. **Document** what was written or updated in the Dev Agent Record.

**No tests or evals required** for specification changes. AVFL checkpoint (run by `momentum:dev`) validates the spec against acceptance criteria.

**Additional DoD items for specification tasks:**
- [ ] `skills/momentum/references/manifesto-format.md` created and self-sufficient (a conformant manifesto can be produced from it alone — AC1).
- [ ] Normative "stable / not a context overlay" statement present, using the canonical term "diagnostic table" (AC2, AC10).
- [ ] Completeness criterion specified with both incompleteness conditions and the detectable signal (AC6).
- [ ] Exemplar-conformance check captured in the doc; all ~35 entries across 9 areas confirmed expressible (AC7).
- [ ] architecture.md Decision 56 carries the manifesto-format location/naming subsection, additively, with all prior lines preserved (AC9).
- [ ] All cross-references to other documents, files, or sections resolve correctly (AC10).
- [ ] "context overlay" never reintroduced anywhere in the new/edited content (AC10).
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically).

**Frozen verification contract reminder:** a frozen verification contract for this sprint lives at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Before signaling done, read the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check. Do not read the verifier body (Part B: scenarios, assertion scripts) beyond sections `how_dev_self_checks` explicitly references.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
