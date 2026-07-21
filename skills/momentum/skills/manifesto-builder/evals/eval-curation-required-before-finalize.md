# Eval: Curation is required — the skill never silently finalizes a generated draft

**Eval ID:** manifesto-builder-curation-required-before-finalize
**Stakes:** correctness / design-integrity — DEC-038 G2 committed this skill to generate-THEN-curate specifically because the recovered `cmp-dev` prototype proved symptom-phrasing quality is the expensive, human-designed part. A skill that silently finalizes the raw draft defeats the entire rationale for this story's shape.

**Given** the GENERATE phase has just produced a draft diagnostic table (grouped, KB-sourced entries) and a first-pass `## File Ownership` glob list, and no file has yet been written to `.claude/manifests/`,

**When** the flow continues toward a finalized manifesto,

**Then**:
1. The skill visibly presents the draft diagnostic table and draft glob list to the developer.
2. The skill explicitly asks the developer to review and refine the symptom wording and the globs — a real elicitation, not a rhetorical or skippable notice.
3. The skill does not write anything to `.claude/manifests/{role}-{domain}.md` until the developer has responded to that request.
4. The developer's curation input (refined symptom phrasing, refined/added/removed globs) is incorporated into the content that is ultimately written — the write step uses the curated table, not the raw draft.

## Verification approach

Read `skills/momentum/skills/manifesto-builder/workflow.md`. Confirm:

1. There is a distinct CURATE phase/step between the GENERATE phase and the FINALIZE/WRITE phase (not merged into either).
2. The CURATE step contains an explicit `<ask>` (or equivalent elicitation instruction) presenting the draft table and glob list and requesting refinement — not just a passive "here is the draft" statement with no request for input.
3. The FINALIZE/WRITE step's instructions reference the *curated* table/globs (post-developer-response), not the GENERATE phase's raw output directly.
4. No instruction anywhere permits proceeding to WRITE without having executed the CURATE step's elicitation — e.g. no "if no response, proceed with defaults" escape hatch that would let curation be silently skipped.
5. The normative symptom-phrasing rules and `wiki-query` invocation rules from `manifesto-format.md` appear as the curation checklist the developer is prompted against (so curation is guided, not open-ended).

## Pass criteria

An explicit curation exchange — a request for the developer's input on symptom wording and globs — is described between the draft appearing and the file being written, and the workflow's WRITE step is instructed to write the curated content, not the raw draft.

## Fail criteria

The workflow's WRITE step could be reached having only produced a draft, with no intervening elicitation instruction; or an elicitation exists but is optional/skippable with a default-proceed path; or the WRITE step writes the GENERATE phase's raw draft rather than curated content.
