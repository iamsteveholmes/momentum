---
title: Constitution.md generation acceptance criteria
story_key: constitutionmd-generation-acceptance-criteria
status: ready-for-dev
epic_slug: momentum-agent-composition-pipeline
feature_slug: momentum-composable-specialist-agents
story_type: feature
priority: high
depends_on: []
touches:
  - skills/momentum/skills/constitution-builder/SKILL.md
  - skills/momentum/skills/build-guidelines/SKILL.md
change_type:
  - specification
verification_method_advisory: document-review
---

# Constitution.md generation acceptance criteria

## Story

As a developer,
I want concrete acceptance criteria defined for build-guidelines' constitution.md (Tier 1) output,
so that the generated constitution is verifiable, appropriately sized, and properly cites its sources.

## Description

Author concrete, testable acceptance criteria for the constitution.md (Tier 1) output produced by the agent-composition pipeline — generated today by `momentum:constitution-builder` and orchestrated (going forward) by `build-guidelines`. The ACs cover: file format and section structure, a line-count budget (target ~660 lines, the decision-document budget), content rules (critical rules only, with pointers into `references/` for detail), citation integrity (every rule traceable to a wiki KB source or a project decision), prescriptive KB-trigger language (DEC-015 D3), and the DEC-038 ownership boundary that keeps per-agent routing out of the shared constitution.

This story produces a *quality bar* — a spec, not a code change. Its output is the set of acceptance criteria below plus a defined hook for where those criteria are enforced (a post-generation check / AVFL gate in the pipeline). It does not itself rewrite `constitution-builder`'s generation logic; the narrowing of generated content is owned by the sibling story `constitution-builder-write-mode-parameterization`. This story defines what "correct" looks like so the generator (and its AVFL gate) has something concrete to produce against and verify.

**Pain context:** Without defined acceptance criteria for constitution.md, the constitution generator has no quality bar to produce against, and the output cannot be verified as correct. The ~660-line budget and citation-integrity requirements are derived from the decision-document model but have not been formalized as testable ACs.

## DEC-038 Alignment

Per [DEC-038](../../_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md) (Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB), the acceptance criteria for constitution.md generation must respect the ownership boundary between the shared constitution and the per-agent manifesto:

- **Shared constitution scope.** constitution.md (Tier 1) carries project-level identity, values, constraints, and glossary — content genuinely shared across every agent on the project. The "format / section structure" ACs reflect this scope and must not prescribe a per-agent routing section as part of the shared constitution.
- **Routing is per-agent, not shared.** Per-agent routing — the *diagnostic table* mapping observable developer symptoms to the exact `wiki-query` KB lookup — is a stable, per-role×domain artifact owned at the **manifesto / agent-builder** layer, not the shared constitution. A project-shared `## Quick Routing` block (e.g., a Compose/Kotest routing table) is meaningless for a `pm` or `architect` agent, so the shared constitution must not bake it in.
- **AC consequence.** Constitution generation does not own or duplicate per-agent routing. The ACs include a check that the generated shared constitution contains no per-agent diagnostic-table / routing content, and that any `## Quick Routing` content is reconciled against the per-agent model.
- **Cross-reference.** This reconciliation is coordinated with the sibling story `constitution-builder-write-mode-parameterization` (DEC-038 Phase 1), which owns reconciling `constitution-builder`'s current project-*shared* `## Quick Routing` ownership against the per-agent routing model. Keep the two stories' stances consistent. See **Dev Notes → Concerns** for the known cross-story / cross-spec design fork around FR136 and the two architecture-sanctioned resolution options.

## Acceptance Criteria

These ACs define the quality bar for the constitution.md (Tier 1) artifact produced by the agent-composition pipeline. Each is verified by document-review against the generated artifact and against its cited sources (no automated driver). Where an AC asserts an *absence* (e.g., "no per-agent routing"), it is verified by inspecting the generated artifact for the disallowed content.

### Format and structure

1. The constitution.md format is documented as part of this story's deliverable: file location/naming, required section headings, and section ordering are stated explicitly so the generator and its verifier share one contract. The documented section set is scoped to genuinely shared, project-wide content — identity, values, constraints, glossary, and any cross-cutting (every-agent) standing rules/permissions — and the documented wiki-query interface block (DEC-018). It does NOT prescribe a per-agent routing section (see AC 8).
2. Each required section in the documented format has a one-line statement of its purpose and its expected content, so a reviewer can confirm a generated constitution is complete (no required section missing) and well-formed (no section repurposed).

### Line-count budget

3. A line-count budget is specified for constitution.md with an explicit target (~660 lines, the decision-document budget) and a stated tolerance band (an upper bound the artifact must not exceed). The budget value and its rationale (decision-document model) are recorded in the AC document.
4. The budget is enforced at generation/verification time: the pipeline's post-generation check (AC 9) flags a constitution that exceeds the upper bound, and the AC document states how an overflow is resolved — by moving detail into `references/` with a load pointer (per AC 5), not by deleting content.

### Content rules

5. A content rule is defined: the constitution carries critical, always-loaded rules only, with pointers into `references/` for elaboration. The AC document states the test for "critical" (a rule that must be in hot context for every agent on every task) versus "reference detail" (elaboration, examples, edge cases that an agent fetches on demand), so a reviewer can adjudicate borderline content.
6. **DEC-015 D3 — prescriptive KB-trigger language.** The constitution's KB-trigger language is prescriptive, not permissive. The AC document forbids vague permission ("if you need domain knowledge, check the KB") and requires that triggers enumerate specific, named scenarios that compel a `wiki-query` lookup (e.g., "when classifying a story's domain", "when selecting a test pattern for a new library", "when choosing between library approaches on this stack"). Each trigger names the exact context — no judgment call is left to the agent. Verification: the generated constitution contains no permissive/optional KB-trigger phrasing, and every KB trigger names a concrete scenario.

### Citation integrity

7. A citation-integrity rule is defined and testable: every rule/claim in the generated constitution is traceable to a wiki KB source (a `wiki-query`-resolvable page) or to a named project decision (a `DEC-NNN`). The AC document states the verification procedure — for each rule, the reviewer (or the post-generation check) confirms a resolvable source exists — and states that an uncited rule is a failure of the citation-integrity AC.

### DEC-038 routing-ownership boundary

8. The shared constitution contains **no per-agent diagnostic-table / routing content.** The ACs assert that the generated constitution does not include a per-agent symptom→`wiki-query` routing table (the diagnostic table is owned by the per-agent manifesto per DEC-038). Verification: inspect the generated constitution; the presence of a per-agent / role-specific routing table is a failure.
9. Any `## Quick Routing` material in the generated constitution is reconciled against the per-agent model, consistent with the sibling story `constitution-builder-write-mode-parameterization`. The AC document records which of the two architecture-sanctioned resolutions this story commits to (see Dev Notes → Concerns) — either (a) the shared constitution emits only genuinely project-universal routing and defers all role-specific routing to the manifesto, or (b) routing emission is parameterized per write-mode/role — and that decision is the same in both sibling stories.

### Enforcement hook

10. The ACs are integrated into the pipeline's verification path: a post-generation check (or an AVFL gate, coordinated with the `citation-integrity-validation-in-build-guidelines-avfl` story) is named as the owner of enforcing ACs 3, 4, 7, 8, and 9 at generation time. The AC document states where this hook lives (build-guidelines orchestration / constitution-builder post-write) so the criteria are not merely advisory prose.

## Tasks / Subtasks

- [ ] **Task 1 — Document the constitution.md format and section contract** (AC 1, 2)
  - [ ] State the file location/naming, required section headings, and section ordering for constitution.md, scoped to shared project-wide content + the DEC-018 wiki-query interface block; explicitly exclude a per-agent routing section (AC 1)
  - [ ] For each required section, write a one-line purpose + expected-content statement enabling completeness/well-formedness review (AC 2)

- [ ] **Task 2 — Specify and wire the line-count budget** (AC 3, 4)
  - [ ] Record the ~660-line target, the upper-bound tolerance, and the decision-document rationale (AC 3)
  - [ ] State the overflow-resolution rule (move detail to `references/` with a load pointer) and name the post-generation check that enforces the budget (AC 4)

- [ ] **Task 3 — Define the content rules (critical-only + KB-trigger prescriptiveness)** (AC 5, 6)
  - [ ] Write the "critical vs reference detail" test that adjudicates what belongs in the hot constitution vs `references/` (AC 5)
  - [ ] Fold in DEC-015 D3: forbid permissive KB-trigger phrasing; require enumerated, named trigger scenarios with no agent judgment call (AC 6)

- [ ] **Task 4 — Define the citation-integrity rule and its verification procedure** (AC 7)
  - [ ] State the traceability requirement (every rule → a `wiki-query`-resolvable KB page or a `DEC-NNN`) and the per-rule check the reviewer/post-generation check runs (AC 7)

- [ ] **Task 5 — Encode the DEC-038 routing-ownership boundary into the ACs** (AC 8, 9)
  - [ ] Assert the shared constitution contains no per-agent diagnostic-table / routing content, with an inspection-based failure condition (AC 8)
  - [ ] Record this story's committed reconciliation choice (architecture option (a) or (b)) for any `## Quick Routing` material, and confirm it matches the sibling story `constitution-builder-write-mode-parameterization` (AC 9)

- [ ] **Task 6 — Name and wire the enforcement hook** (AC 10)
  - [ ] Identify where the post-generation check / AVFL gate enforcing ACs 3, 4, 7, 8, 9 lives (build-guidelines orchestration and/or constitution-builder post-write), coordinating with `citation-integrity-validation-in-build-guidelines-avfl` (AC 10)

## Dev Notes

### Decision Authority

- **DEC-038** is the authoritative source for the ownership boundary: the manifesto is the per-agent **diagnostic table** (observable symptom → exact `wiki-query`), owned at the manifesto/agent-builder layer — **never** in the shared constitution. DEC-038 D1 names BOTH this story and `constitution-builder-write-mode-parameterization` as the owners of the `## Quick Routing` reconciliation (DEC-038 Phase 1).
- **DEC-015 D3** is authoritative for KB-trigger language: prescriptive, named-scenario triggers only — no permissive "check the KB if you need to." Rationale: LLMs default to training data; vague permission is effectively no instruction.
- **DEC-018** defines `wiki-query` as the Tier 3 cold-KB interface (extended by DEC-038 to multiple per-project KBs). Citation integrity (AC 7) traces rules to `wiki-query`-resolvable pages.
- **DEC-026 D3/D4** establishes the three-skill pipeline (constitution-builder Tier 1 once → agent-builder × N Tier 2) and the manifesto-as-diagnostic-table scope that constrains what the constitution may carry.
- **Architecture Decision 56** and the "Routing ownership — per-agent, not shared constitution (DEC-038)" block in `architecture.md` (line ~3061) name this story as an owner of the reconciliation and enumerate the two sanctioned resolution options — see Concerns.

### Current State of Affected Files

- **`skills/momentum/skills/constitution-builder/SKILL.md`** (exists, ~247 lines, ~9.6 KB). This is the live generator of the constitution sections today. Its current design is the *pre-narrowing* shape and is in direct tension with the ACs this story authors:
  - The frontmatter `description` advertises generating `## Permissions + ## Standing Rules + ## Quick Routing` (and is itself NFR-non-compliant at ~600 chars).
  - Phase 6 "Generate Routing Entries" + the Quick Routing parts of Phases 1, 7, 8 build a project-*shared* `## Quick Routing` block — exactly the per-agent routing content AC 8 disallows in the shared constitution.
  - There is no documented line-count budget, citation-integrity check, or prescriptive-KB-trigger enforcement in the current skill.
  - **This story does NOT rewrite this file's generation logic** — that narrowing is owned by the sibling story `constitution-builder-write-mode-parameterization`. This story authors the AC bar the rewritten generator must satisfy; `touches` lists the SKILL.md because the AC document references and constrains it (the format/budget/citation/no-routing contract attaches to this skill's output).
- **`skills/momentum/skills/build-guidelines/SKILL.md`** — **does not exist on disk yet.** `build-guidelines` is the epic's orchestrator (tracked by story `build-guidelines-skill`) that will run constitution-builder + manifesto-builder and is the natural home for the post-generation check / AVFL gate that enforces these ACs (AC 10). The `touches` path is retained so the index reflects the intended enforcement surface; the live target for the AC bar today is `constitution-builder`, with build-guidelines as the forthcoming orchestration owner. Coordinate with `citation-integrity-validation-in-build-guidelines-avfl` for the citation-integrity gate.

### Architecture Compliance

- Three-tier model (DEC-001 / DEC-008 D1, restated in architecture Decision 56): Tier 1 Hot Constitution (project-wide) → Tier 2 Composed Agent File (per-agent, manifesto/agent-builder) → Tier 3 Cold KB (wiki vault via `wiki-query`). These ACs keep the constitution firmly in Tier 1 — shared, project-wide content only — and push per-agent routing to Tier 2.
- Writer-authority constraint (architecture Decision 56): constitution-builder writes only constitution content; it must not write routing entries into `momentum/agents.json` (agent-builder's sole authority). AC 8's "no per-agent routing in the shared constitution" is consistent with this constraint.
- `wiki-query` is the only sanctioned cold-KB access path (DEC-018, multi-KB per DEC-038); citation integrity (AC 7) is defined against `wiki-query`-resolvable pages, not direct vault reads.
- FR136/FR142 cross-reference: the constitution is layer (2) of the FR136 three-layer composition; these ACs enforce that the constitution layer carries no manifesto (diagnostic-table) content. See Concerns for the FR136-wording fork.

### Testing Requirements

- This is a `specification` change → validated by **document-review** (verification-standard.md Section 1: `specification` → `document-review`). There is no automated driver; the AC document is verified by inspection and by cross-reference resolution against its cited sources (DEC-038, DEC-015, DEC-018, architecture Decision 56, the constitution-builder SKILL.md).
- Verification method (advisory): `document-review`. The reviewer confirms: (1) every AC is testable and observable; (2) all cross-references (decision IDs, FR IDs, sibling story slug, file paths) resolve; (3) the routing-ownership stance (AC 8/9) is identical to the sibling story `constitution-builder-write-mode-parameterization`; (4) the committed reconciliation option (architecture (a) or (b)) is recorded.
- No tests or evals required for a specification change. The AVFL checkpoint (run by momentum:dev) validates the AC document against the epic record and acceptance criteria.
- A frozen verification contract for this sprint will exist at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done; Dev does not read the Part-B verifier body (scenarios/assertions/Gherkin) beyond sections `how_dev_self_checks` explicitly references.

### Project Context Reference

- Sibling/coordinating stories in epic `momentum-agent-composition-pipeline`:
  - `constitution-builder-write-mode-parameterization` (SIBLING — shares the `## Quick Routing` ownership reconciliation per DEC-038; this story and that one MUST take the same stance. That story is already `ready-for-dev`.).
  - `citation-integrity-validation-in-build-guidelines-avfl` (owns the AVFL/citation gate that enforces AC 7/10).
  - `build-guidelines-skill` (the orchestrator that will house the post-generation enforcement hook, AC 10).
  - `wiki-query-interface-block-for-hot-constitution` (defines the wiki-query interface block the documented format must include, AC 1).
  - `manifesto-builder-skill-generate-then-curate` / `agent-builder` (receive the per-agent routing the shared constitution must NOT carry, AC 8).
- Per-project KB scoping (DEC-038 / FR142): Momentum maintains its own KB; the nornspun `cmp-dev.md` is a format exemplar only (`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`).

### Concerns — known cross-story / cross-spec design fork

The orchestrator flagged this explicitly; it is a real, documented fork, not a defect introduced here:

- **FR136 wording vs this story's AC stance.** PRD FR136 ("Gen-2 Agent Composition Model") describes the **constitution** layer as carrying a "**quick routing table derived from the wiki KB**." This story's ACs (AC 8) assert the shared constitution carries **no per-agent diagnostic-table / routing content.** These are in surface tension: FR136's plain wording places a routing table in the constitution; this story (following DEC-038) pushes per-agent routing out to the manifesto. The reconciliation is that FR136's "quick routing table" can be read as either (i) genuinely project-universal routing that survives in the constitution, or (ii) the per-agent diagnostic table that DEC-038 relocated to the manifesto — and DEC-038 explicitly supersedes the FR136 *manifesto* reading. FR136 itself has not been re-worded to drop "quick routing table" from the constitution layer; the AC author must either align the AC to architecture option (a) below (which keeps *project-universal* routing in the constitution, consistent with FR136 (i)) or flag FR136 for a spec-impact amendment.
- **Two architecture-sanctioned resolution options (architecture.md ~line 3061).** The "Routing ownership — per-agent, not shared constitution (DEC-038)" block offers exactly two resolutions and names this story + its sibling as their owners: **(a)** constitution-builder emits only genuinely project-universal routing and defers role-specific routing to the manifesto; **(b)** routing emission is parameterized per write-mode/role. AC 9 requires this story to *commit* to one option and to match the sibling. As drafted, the AC set leans toward "no per-agent routing in the shared constitution" (compatible with both (a) and (b)) but does NOT yet pin which option — the developer/PO must record the committed choice and confirm the sibling story records the same one. If the chosen option contradicts FR136's literal "quick routing table" wording, raise a spec-impact amendment to FR136.
- **Consistency obligation.** AC 8/9 must be identical in spirit to `constitution-builder-write-mode-parameterization`'s ACs 7/15/16 (which already remove `## Quick Routing` generation entirely under DEC-026 D4). If the sibling removes routing generation outright while this story permits "project-universal routing" under option (a), the two stories diverge — reconcile before activation.

### References

- `momentum:constitution-builder` SKILL.md — the live generator whose constitution.md output these ACs govern (currently emits `## Quick Routing`; to be narrowed by the sibling story)
- `constitution-builder-write-mode-parameterization` story (SIBLING — shares the `## Quick Routing` ownership reconciliation per DEC-038; keep stances identical)
- `citation-integrity-validation-in-build-guidelines-avfl` story (owns the AVFL/citation enforcement gate — AC 7/10)
- `build-guidelines-skill` story (orchestrator; home of the post-generation enforcement hook — AC 10)
- `wiki-query-interface-block-for-hot-constitution` story (defines the wiki-query interface block the documented format must include — AC 1)
- DEC-038 — manifesto = per-agent diagnostic table; per-agent routing owned at the manifesto/agent-builder layer, NOT the shared constitution; per-project multi-KB; names this story as a reconciliation owner (DEC-038 Phase 1)
- DEC-015 D3 — prescriptive (named-scenario) KB-trigger language, not permissive (AC 6)
- DEC-018 — wiki-query as the Tier 3 cold-KB interface (extended to multiple per-project KBs by DEC-038); basis for citation integrity (AC 7)
- DEC-026 D3/D4 — three-skill pipeline; constitution-builder Tier 1 once; manifesto = diagnostic table
- DEC-001 / DEC-008 D1 — three-tier agent guidelines architecture
- architecture.md — Decision 56 (DEC-026 D3/D5) and "Routing ownership — per-agent, not shared constitution (DEC-038)" block (~line 3061: the two sanctioned resolution options and the writer-authority constraint)
- prd.md — FR136 (Gen-2 composition model; constitution layer "quick routing table" wording — see Concerns), FR142 (per-project multi-KB), FR138 (agent-builder pipeline)
- `skills/momentum/references/rules/verification-standard.md` — Section 1 method routing (`specification` → `document-review`)
- Epic context: `momentum-agent-composition-pipeline` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–6 → specification (direct authoring with cross-reference verification)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (epic, PRD, or parent spec) — not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per the story's acceptance criteria. Here, the deliverable is the constitution.md AC quality bar itself (the format/budget/content/citation/routing-ownership contract), authored into the pipeline's documentation surface (the build-guidelines / constitution-builder skill docs or a dedicated reference the verifier reads).
2. **Verify cross-references:** All references to other documents, files, sections, or identifiers must resolve correctly — decision IDs (DEC-038, DEC-015, DEC-018, DEC-026), FR IDs (FR136, FR142), the sibling story slug `constitution-builder-write-mode-parameterization`, architecture Decision 56, and the constitution-builder SKILL.md paths.
3. **Verify format compliance:** The AC document follows the project's story/spec conventions; ACs are numbered, observable, and individually testable by document-review.
4. **Reconcile the routing-ownership stance:** Confirm AC 8/9's stance is identical to the sibling story and record the committed architecture resolution option (a) or (b). If it contradicts FR136's literal wording, raise a spec-impact amendment to FR136 (see Concerns).
5. **Document** what was written or updated in the Dev Agent Record.

**No tests or evals required** for specification changes. AVFL checkpoint (run by momentum:dev) validates the spec against acceptance criteria.

**Additional DoD items for specification tasks:**
- [ ] All cross-references to other documents, files, or sections resolve correctly
- [ ] Document follows project template/format conventions if one exists
- [ ] Routing-ownership stance (AC 8/9) confirmed identical to sibling story `constitution-builder-write-mode-parameterization`, and the committed architecture resolution option (a)/(b) recorded
- [ ] FR136-wording fork addressed: either aligned to a sanctioned option or flagged for spec-impact amendment
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

**Frozen verification contract reminder:** A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Before signaling done, read only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check. Do not read the Part-B verifier body (scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

_This section is populated by the dev agent during implementation._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
