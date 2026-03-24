# Spec Contextualization

Reference document for just-in-time spec surfacing, motivated disclosure, and drill-down patterns. Loaded by workflow.md when a workflow step references a spec decision or acceptance criterion.

---

## JIT Spec Surfacing Pattern

When a workflow step references an architectural decision, acceptance criterion, or prior choice, surface the relevant context inline. The developer should be able to act on the step using only what Impetus presents — no need to open another file.

### What to Surface

Extract **one sentence** — the key decision that affects the current step. Not the full section, not the full document, not a summary of the entire architecture.

### Format

```
[Source: path/to/file.md#Section] — Key decision in one sentence.
```

Example:
```
[Source: _bmad-output/planning-artifacts/architecture.md#Decision 3b] — All subagent output is synthesized through Impetus voice; raw output is never shown to the developer.
```

### How to Extract

1. Identify the spec reference in the current workflow step (decision ID, AC number, FR number)
2. Read the referenced artifact — do not answer from memory
3. Locate the specific section
4. Extract the one sentence that directly affects the developer's current action
5. If no single sentence captures the decision, compose one that does — but cite the source section

---

## Motivated Disclosure (UX-DR21)

Every spec context reference must be preceded by a statement of **why it matters to this step** — not just what the spec says. The developer should understand the relevance before seeing the content.

### Pattern

```
[Why it matters] — [brief connection to current step concern]
[Source: path/to/file.md#Section] — [key decision]
```

### Examples

Good:
```
This affects how you structure the response — subagent output can't go directly to the developer.
[Source: architecture.md#Decision 3b] — All subagent output is synthesized through Impetus voice.
```

Bad:
```
Here's what the architecture says about voice:
[Source: architecture.md#Decision 3b] — All subagent output is synthesized through Impetus voice.
```

The "good" example tells the developer why the decision matters to what they're doing right now. The "bad" example just presents spec content with no connection to the current step.

### Rule

If you cannot articulate why a spec reference matters to the current step, do not surface it. Irrelevant context is worse than no context.

---

## Drill-Down Pattern

When a developer wants more context beyond the one-sentence extract, expand with why-it-matters framing before presenting additional detail.

### Trigger

Developer asks for more detail, or the key decision has dependencies that affect later steps.

### Pattern

1. **Restate why it matters** — connect to the current concern
2. **Expand with relevant detail** — the next level of specificity from the spec
3. **Stop when actionable** — don't keep expanding into the full document

### Example

Developer asks: "Tell me more about the hub-and-spoke constraint."

Good:
```
The constraint means Impetus is responsible for all developer-facing output. When you dispatch to a subagent, the result comes back as structured JSON — Impetus synthesizes it into natural language before presenting.

This matters here because the completion signal you're implementing must be delivered by Impetus, not passed through from the subagent.

[Source: architecture.md#Decision 3b] — Impetus synthesizes all subagent output. Subagent returns {status, result, question, confidence}; Impetus translates to developer-facing language.
```

Bad:
```
Here's the full Hub-and-Spoke Voice Contract section from the architecture doc:
[... entire section pasted ...]
```

---

## What Counts as "Context" vs. "Document Dump"

| Action | Classification |
|---|---|
| Cite one decision with file reference | Context — correct |
| Quote the one sentence that matters | Context — correct |
| Offer drill-down for more detail | Context — correct |
| Paste an entire spec section | Document dump — incorrect |
| Load a full document into the response | Document dump — incorrect |
| Summarize multiple sections at once | Document dump — incorrect |
| Present spec content without file reference | Ungrounded — incorrect |
| Present spec content without why-it-matters | Unmotivated — incorrect |
