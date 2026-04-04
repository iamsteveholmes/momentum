# Rule File Template

Template for generating path-scoped `.claude/rules/*.md` files. The orchestrator fills in the placeholders based on research findings and consultation decisions.

## Template

```markdown
---
paths:
  - "{{glob_pattern_1}}"
  - "{{glob_pattern_2}}"
---
# {{Technology Name}} Guidelines

**Version:** {{technology}} {{version}}, {{dependency_1}} {{dep_version}}
**Last verified:** {{date}}

## CRITICAL — Breaking Changes from {{old_version}}

{{#each prohibitions}}
- NEVER use `{{deprecated_api}}` — {{reason}}. Use `{{replacement}}` instead
{{/each}}

## Conventions

{{#each conventions}}
- {{convention_description}}
{{/each}}

## Dependencies / Setup

{{#each setup_items}}
- {{setup_description}}
{{/each}}
```

## Ordering Rules (Research-Backed)

Content must follow this order — critical information first, setup last:

1. **Version pins** — exact versions at the top
2. **Critical prohibitions** — NEVER/MUST rules for breaking changes
3. **Conventions** — preferred patterns and style choices
4. **Dependencies / setup** — configuration specifics

This ordering reflects the "lost in the middle" effect: LLMs attend most to the beginning and end of documents. Critical corrections go first.

## Size Constraints

- **Target: 30-80 lines** per rules file
- If a technology needs more than 80 lines, split into multiple scoped files or move detail to a Layer 2 reference doc
- Every line must pass the test: "Would removing this cause the agent to make a mistake it couldn't recover from by reading the code?"

## Path Scope Design Principles

- **One technology per file** — `kotest.md`, `compose-ui.md`, `kmp-project.md`
- **Glob patterns should match files where the technology is used:**
  - Test frameworks → `"**/*Test.kt"`, `"**/*Spec.kt"`, `"**/test/**/*.kt"`
  - UI frameworks → `"**/ui/**/*.kt"`, `"**/*Screen.kt"`, `"**/*Component.kt"`
  - Build config → `"**/build.gradle.kts"`, `"**/settings.gradle.kts"`
  - Backend routes → `"**/api/**/*.kt"`, `"**/routes/**/*.ts"`
- **Avoid overly broad patterns** — `"**/*.kt"` loads for every Kotlin file, defeating the purpose
