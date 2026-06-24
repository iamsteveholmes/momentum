# === VERIFICATION HEADER (Part A) ===
---
story_slug: agent-manifesto-format-specification
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-18/specs/agent-manifesto-format-specification.review.md
how_dev_self_checks: |
  Open the produced reference document at skills/momentum/references/manifesto-format.md and read it
  end to end as if you had never seen this story. Confirm, using only that document plus the exemplar
  it cites, that you (or any author) could write a brand-new conformant manifesto from it alone — no
  other document needed. Then walk this checklist against what is on the page:
    1. The doc defines the manifesto as a table whose every row pairs an observable developer symptom
       with an exact wiki-query KB lookup (symptom -> wiki-query terms).
    2. The doc states, in normative ("must"/"shall"-style) language, that the manifesto is STABLE across
       every sprint and every story, and explicitly says it is NOT a per-sprint or per-story context
       overlay. Search the whole new/edited content for the phrase "context overlay" — it must appear
       only in a rejecting/negating sentence, never as an accepted description.
    3. The doc requires each manifesto to declare an explicit role (e.g. dev, qa, e2e, architect, pm)
       and domain (e.g. kotlin-compose, python-fastapi), and shows the composed-file naming it produces:
       .claude/guidelines/agents/{role}-{domain}.md.
    4. The doc defines a stack-facts section (language, frameworks, test tooling, version pins,
       architecture paradigm) and explains it scopes/disambiguates the symptom -> wiki-query lookups.
    5. The doc requires every manifesto to record which project KB its wiki-query entries resolve
       against, says multiple per-project KBs coexist, and notes this depends on a multi-KB wiki-query
       extension WITHOUT implementing that extension here.
    6. The doc defines what "complete" means for a manifesto, names BOTH incompleteness conditions
       (a situation with no matching symptom entry; a symptom entry whose wiki-query returns nothing
       usable), and specifies the detectable signal an agent emits on reaching un-routed territory
       (a logged/surfaced incompleteness signal, not a silent fallthrough).
    7. The doc demonstrates exemplar-conformance: open docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md,
       and confirm the doc shows (via a mapping note or worked example) that the exemplar's worked
       symptom -> wiki-query entries across its technology areas render in the format with no loss of
       meaning, and labels the exemplar as a format reference only / never a Momentum agent.
    8. Open _bmad-output/planning-artifacts/architecture.md and confirm the Decision 56 manifesto block
       now contains a manifesto-format subsection that cites skills/momentum/references/manifesto-format.md
       as the canonical format spec and records the manifesto file's location/naming convention, with all
       previously-present lines in that block still intact.
    9. Spot-check every path, decision id (DEC-038, DEC-018, DEC-026 D4), FR id (FR136, FR138, FR142),
       and section reference in the new doc and the architecture.md edit — each must resolve to a real
       target. The canonical term "diagnostic table" is used throughout.
  If any item is missing, vague, or non-normative, the story is not done.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/agent-manifesto-format-specification.md#acceptance-criteria
platforms: [host]
---

## Document Under Review

Primary artifact (must exist):

- `skills/momentum/references/manifesto-format.md` — the single authoritative manifesto-format specification.

Secondary artifact (must be edited additively):

- `_bmad-output/planning-artifacts/architecture.md` — the Decision 56 manifesto definition block.

Read-only reference inputs the reviewer uses while checking (NOT produced by this story; do not require edits to them):

- `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` — the format exemplar (verbatim nornspun `cmp-dev.md`).
- `.momentum/stories/build-guidelines-skill.md` — the downstream consumer whose consumption framing the format must read consistently with.

## Required Claims

Each claim is verifiable by inspecting the produced documents (and, where noted, the cited reference inputs). A reviewer with no source access can check every box.

### Existence and self-sufficiency

- [ ] A reference document exists at the exact path `skills/momentum/references/manifesto-format.md`.
- [ ] The document presents itself as the single authoritative specification of the manifesto file (its location convention, identity, content model, and completeness rule).
- [ ] The document is self-sufficient: a reader can produce a conformant manifesto from this document alone (plus the exemplar it cites), with no other document required to fill gaps in the format definition.
- [ ] The document follows the house style of the other format/schema references in `skills/momentum/references/` (a title plus version line, a normative definition, a field/section table, and worked examples).

### Diagnostic-table model (stable, not overlay)

- [ ] The document defines the manifesto as a table whose every entry pairs an observable developer symptom (the trigger) with the exact `wiki-query` KB lookup (the resolution) — i.e. the entry shape is symptom -> `wiki-query` terms.
- [ ] The document states, in normative language, that the manifesto is **stable** across every sprint and every story.
- [ ] The document states explicitly that the manifesto is **not** a per-sprint or per-story context overlay; the phrase "context overlay" appears (if at all) only inside a sentence that rejects/negates that reading.
- [ ] The document uses "diagnostic table" as the canonical term for the manifesto's central artifact.

### Role x domain identity

- [ ] The document specifies that a manifesto carries an explicit `role` identity, and gives example role values (e.g. `dev`, `qa`, `e2e`, `architect`, `pm`).
- [ ] The document specifies that a manifesto carries an explicit `domain` identity, and gives example domain values (e.g. `kotlin-compose`, `python-fastapi`).
- [ ] The document states that the `role` x `domain` identity determines which composed agent file the manifesto produces, and shows the naming pattern `.claude/guidelines/agents/{role}-{domain}.md`.

### Stack facts

- [ ] The document defines a stack-facts section covering language, frameworks, test tooling, version pins, and architecture paradigm.
- [ ] The document explains that the stack facts scope and disambiguate the symptom -> `wiki-query` lookups.
- [ ] The document shows a concrete stack-facts example consistent with the exemplar's shape (a one-line stack summary such as the "CMP 1.10.2 / Material3 / Ktor / SQLDelight / Kotest / Turbine / MVI" form).

### Project-scoped, multi-KB

- [ ] The document requires every manifesto to record which project KB its `wiki-query` entries resolve against.
- [ ] The document states that multiple per-project KBs coexist (e.g. Momentum agents resolve against the Momentum KB; nornspun agents resolve against the nornspun KB).
- [ ] The document notes that multi-KB resolution requires extending `wiki-query` (DEC-018) and explicitly does NOT implement that extension itself (the boundary is stated as out of scope for the format spec).

### Completeness criterion (load-bearing)

- [ ] The document defines what "complete" means for a manifesto.
- [ ] The document names the first incompleteness condition: a situation the agent hits for which no symptom entry exists.
- [ ] The document names the second incompleteness condition: a symptom entry whose `wiki-query` returns nothing usable for a situation the agent hits.
- [ ] The document specifies the detectable signal: an agent reaching un-routed territory emits/logs an explicit incompleteness signal that is surfaced rather than a silent fallthrough, so the gap is detectable.

### Exemplar-conformance

- [ ] The document is validated against `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` and captures the exemplar-conformance check (a mapping note or at least one worked example rendering exemplar entries in the format).
- [ ] A reviewer can confirm, by comparing the document's format to the exemplar's worked routing entries, that the exemplar's symptom -> `wiki-query` entries across its technology areas are each expressible in the format with no loss of meaning.
- [ ] The document labels the exemplar as a format reference only and states it is never a Momentum agent (it is never to be registered, spawned, or treated as one).

### Consumer consistency (parse and route)

- [ ] The document defines the manifesto's sections/fields and their semantics in a form that lets a consumer determine, from a manifesto: which `role` x `domain` composed file to generate, which stack facts to bake in, and which project KB to scope `wiki-query` to.
- [ ] The document frames the manifesto as a composition *input* that is sprint-invariant (it is not regenerated or re-scoped per sprint), and this framing reads consistently with the consumption contract described in `.momentum/stories/build-guidelines-skill.md` (AC1-AC4).

### Architecture.md edit

- [ ] `_bmad-output/planning-artifacts/architecture.md` contains, under the Decision 56 manifesto definition block, a manifesto-format subsection.
- [ ] That subsection cites `skills/momentum/references/manifesto-format.md` as the canonical format spec.
- [ ] That subsection records the manifesto file's on-disk location/naming convention.
- [ ] The edit is additive: every line previously present in the Decision 56 manifesto block is still present, and the subsection does not restate or contradict the existing manifesto definition there.

### Cross-references and vocabulary

- [ ] Every file path referenced in the new document and the architecture.md edit resolves to a real target.
- [ ] Every decision id referenced (DEC-038, DEC-018, DEC-026 D4) resolves to a real decision.
- [ ] Every FR id referenced (FR136, FR138, FR142) resolves to a real requirement.
- [ ] Every section/sub-section reference (including the exemplar's cited sub-sections) resolves.
- [ ] The canonical term "diagnostic table" is used throughout the new/edited content, and the rejected "context overlay" framing is never reintroduced as an accepted description.

## Required Sections

The reference document `skills/momentum/references/manifesto-format.md` must contain, observably, at least the following:

- A title and version line.
- A normative definition of the manifesto as the stable, per-role x domain diagnostic table (with the stable / not-an-overlay statement).
- A manifesto identity section defining `role`, `domain`, and the project KB the manifesto scopes to.
- A stack-facts section defining the scoping facts and their purpose.
- A diagnostic-table section defining the symptom -> `wiki-query` entry shape, grouped by technology/concern area, with guidance on symptom phrasing (specific, observable, diagnostic) and on the `wiki-query` invocation form.
- A completeness section defining "complete," both incompleteness conditions, and the detectable un-routed-territory signal.
- An exemplar-conformance section (mapping note or worked example) validating the format against `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`, labeled format-reference-only.
- At least one worked example of a manifesto (or a manifesto fragment) rendered in the format.

The architecture.md edit must contain, observably:

- A manifesto-format subsection nested under the existing Decision 56 manifesto definition block, citing the format reference path and the manifesto file location/naming convention.

## Pass Criteria

- The reference document exists at `skills/momentum/references/manifesto-format.md` and every box under **Required Claims** is satisfied by inspection of the produced documents (and the cited reference inputs where noted).
- All **Required Sections** are present in the reference document, and the architecture.md manifesto-format subsection is present, additive, and consistent with the existing Decision 56 definition.
- The exemplar-conformance check is concrete and reviewable: a reviewer can trace the exemplar's worked symptom -> `wiki-query` entries into the format and find every one expressible.
- All cross-references resolve, and "diagnostic table" is the canonical vocabulary throughout with no accepted use of "context overlay."

## Fail Criteria

- The reference document does not exist at the specified path, or relies on another document to be usable (not self-sufficient).
- The manifesto is described as a per-sprint/per-story overlay, or "context overlay" appears as an accepted description anywhere in the new/edited content.
- The entry shape is not defined as observable symptom -> exact `wiki-query` lookup, or `role`/`domain` identity or the `{role}-{domain}` composed-file naming is missing.
- The stack-facts section, the project-KB declaration requirement, or the multi-KB coexistence statement is absent — or the document implements the `wiki-query` multi-KB extension instead of leaving it out of scope.
- The completeness criterion is missing either incompleteness condition or the detectable un-routed-territory signal, or treats un-routed territory as a silent fallthrough.
- No exemplar-conformance check is captured, or one or more exemplar entries cannot be expressed in the format, or the exemplar is not labeled format-reference-only / is treated as a Momentum agent.
- The architecture.md edit is missing, overwrites/contradicts existing Decision 56 lines, or omits the format-reference citation or the location/naming convention.
- Any referenced path, DEC id, FR id, or section name fails to resolve, or "diagnostic table" is not used as the canonical term.
