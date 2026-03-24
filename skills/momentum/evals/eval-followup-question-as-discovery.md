# Eval: Follow-Up Question as Discovery Opportunity

## Scenario

Given a developer asks a follow-up question mid-step — e.g., "Why does this story require event sourcing instead of CRUD?" or "What happens if the MCP server isn't configured?" — while Impetus is presenting a workflow step:

The skill should:
1. Treat the question as a discovery opportunity — read the relevant artifact before answering (not answer from memory or generically)
2. Return an answer grounded in the current artifact content, citing the specific source
3. If the question reveals an ambiguity or gap in the spec, flag it explicitly: "This question reveals an ambiguity in [specific acceptance criteria / architecture decision] — worth clarifying before we continue"
4. After answering, re-present the user control (e.g., `[A] Adjust · [P] Pause · [C] Continue`) so the workflow step does not stall

## Expected Behavior

When a follow-up question arrives:

1. Impetus identifies the relevant artifact (architecture doc, story spec, UX design, etc.)
2. Impetus reads the artifact — does not answer from cached knowledge or generic reasoning
3. Answer references specific content from the artifact: "According to [Source: path/to/file.md#Section], the decision was..."
4. If the question exposes a spec gap (e.g., the spec doesn't address the scenario the developer is asking about), Impetus flags it: "This question reveals an ambiguity in the acceptance criteria — worth clarifying before we continue"
5. After the answer, Impetus re-presents the current step's user control to keep the workflow moving

## NOT Expected

- Answering generically: "Generally speaking, event sourcing is preferred when..."
- Answering without reading the relevant artifact
- Answering without citing a specific source
- Failing to detect an ambiguity when the question directly exposes one (e.g., the spec says "configure MCP" but doesn't specify which provider)
- Dropping the workflow after answering — the developer should see the user control again
- Treating every follow-up as an ambiguity — only flag when the question genuinely reveals a gap or contradiction
