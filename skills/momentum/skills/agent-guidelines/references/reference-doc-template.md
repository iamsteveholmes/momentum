# Reference Document Template

Template for generating `docs/references/*.md` files (Layer 2). These are longer documents containing worked code examples that the agent reads on demand.

## Template

```markdown
# {{Technology}} Patterns Reference

**Version:** {{technology}} {{version}}
**Last verified:** {{date}}
**Purpose:** Correct patterns for {{technology}} that differ from pre-{{training_cutoff}} training data.

## {{Pattern Category 1}}

### {{Pattern Name}}

{{brief_context — one sentence explaining when this pattern applies}}

\`\`\`{{language}}
{{code_example}}
\`\`\`

{{#if gotcha}}
**Gotcha:** {{gotcha_description}}
{{/if}}

### {{Pattern Name 2}}

...

## {{Pattern Category 2}}

...
```

## Content Principles

1. **Code examples, not prose** — show the correct way; don't explain why at length
2. **Annotate briefly** — one sentence of context before each example
3. **Focus on what's wrong in training data** — patterns the agent would get wrong without this doc
4. **Include gotchas** — non-obvious traps specific to this version
5. **No tutorials** — assume the reader knows the technology conceptually but has stale API knowledge

## Size Constraints

- **Target: 100-300 lines** per reference doc
- Contains code examples for patterns not yet present in the codebase or that the agent cannot infer from existing files
- If a technology needs more detail, create separate reference docs per concern area

## When to Generate

Generate a reference doc when:
- The technology has **3+ breaking changes** from likely training data
- The technology has **non-obvious patterns** that simple prohibitions can't capture (e.g., TDD workflow with a new testing API)
- The user explicitly requests deeper examples during consultation

Do NOT generate reference docs for:
- Technologies the agent already knows well (stable ecosystems)
- Technologies where Layer 1 prohibitions are sufficient
- Patterns that already exist in the project's codebase (point the agent to existing files instead)
