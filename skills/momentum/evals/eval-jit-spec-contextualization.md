# Eval: Just-in-Time Spec Contextualization

## Scenario

Given a developer is at a workflow step that references an architectural decision (e.g., "Decision 3b — Hub-and-Spoke Voice Contract") or an acceptance criterion (e.g., "AC2 from Story 2.4"), when Impetus presents that step:

The skill should:
1. Surface a file reference and key decision inline — e.g., `[Source: _bmad-output/planning-artifacts/architecture.md#Decision 3b] — All subagent output is synthesized through Impetus voice; raw output never shown to developer`
2. Include motivated disclosure framing: state why the referenced decision matters to the current step before presenting the decision content
3. Allow the developer to act on the step without opening another file
4. Offer a drill-down option if the developer wants more context — framed with why-it-matters, not "Here's the full architecture section"

## Expected Behavior

Impetus reads the referenced spec artifact, extracts the one sentence that matters to the current step, and presents it inline with a file reference. The presentation follows this structure:

1. **Why it matters** — a brief statement connecting the spec decision to the current step's concern (e.g., "Event sourcing here affects how migration works in Story 4.3")
2. **Key decision** — the one-sentence spec extract with file reference
3. **Drill-down offer** — optional expansion if the developer wants more

The developer can proceed with the step using only the inline context — no need to open the referenced file.

## NOT Expected

- Dumping the full document or full section from the spec
- Presenting spec content without a file reference
- Presenting spec content without why-it-matters framing (just "Here's what the architecture says:")
- Answering from memory without reading the actual artifact
- Requiring the developer to open another file to understand the context
- Omitting the drill-down option when a deeper context exists
