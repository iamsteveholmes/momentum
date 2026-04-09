# Eval: Large File Handling Guidance Present in All Agent Definitions

## Purpose

Verify that every agent definition in `skills/momentum/agents/*.md` includes a
"Large File Handling" section (or equivalent heading) with the required elements:
offset/limit guidance, named large files, and search-before-read pattern.

## Expected Behavior

When all agent definitions are correctly implemented, each file in
`skills/momentum/agents/*.md` will contain:

1. A section heading that includes "Large File" (e.g., `## Large File Handling`)
2. References to `offset` and `limit` parameters for chunked reading
3. Named examples of large files: `architecture.md`, `prd.md`, `epics.md`,
   `index.json`, and/or JSONL extracts
4. A search-before-read pattern instruction (Grep first, then targeted Read)
5. An error recovery instruction (on token-limit error, do not retry same read)

## Inputs

```
files_to_check:
  - skills/momentum/agents/dev.md
  - skills/momentum/agents/dev-skills.md
  - skills/momentum/agents/dev-build.md
  - skills/momentum/agents/dev-frontend.md
  - skills/momentum/agents/qa-reviewer.md
  - skills/momentum/agents/e2e-validator.md
```

## Verification Steps

For each file in `files_to_check`:

1. Grep for a heading matching `## Large File` (case-insensitive)
   - Expected: at least one match per file
   - Fail if: no match found

2. Grep for `offset` within 30 lines of the heading
   - Expected: found — confirms offset/limit mechanics are documented
   - Fail if: not present near the section

3. Grep for at least two of: `architecture.md`, `prd.md`, `epics.md`,
   `index.json`, `JSONL`, `jsonl`
   - Expected: at least two matches per file
   - Fail if: fewer than two named large files

4. Grep for `Grep` (capital G, the tool name) within 30 lines of the heading
   - Expected: found — confirms search-before-read pattern is documented
   - Fail if: not present near the section

5. Grep for `error` or `fail` within 30 lines of the heading (case-insensitive)
   - Expected: found — confirms error recovery instruction is present
   - Fail if: not present near the section

6. Count lines in the Large File Handling section (from heading to next `##`)
   - Expected: 20 lines or fewer
   - Fail if: exceeds 20 lines (bloats agent system prompts)

## Non-Regression Checks

For each file, verify that only the Large File Handling section was added:

1. Check that frontmatter (name, description, model, effort, tools) is unchanged
2. Check that no existing section headings were removed or renamed
3. Check that the section appears in the correct position per the story spec:
   - `dev.md` — after "What NOT to Do"
   - `dev-skills.md` — after "Conventional Commits", before "Implementation Approach"
   - `dev-build.md` — after "Common Pitfalls", before "Implementation Approach"
   - `dev-frontend.md` — after "Common Pitfalls", before "Implementation Approach"
   - `qa-reviewer.md` — after "Cross-Story Integration Check" section, before "Output Format"
   - `e2e-validator.md` — after "Cross-Scenario Consistency" section, before "Output Format"

## Expected Pass Criteria

- All 6 agent files contain a Large File Handling section
- All sections include: offset/limit mechanics, named large files,
  search-before-read pattern, error recovery
- No section exceeds 20 lines
- No other sections in any agent file were modified

## Expected Fail Criteria

- Any agent file missing the Large File Handling section
- Any section missing offset/limit, named files, or search-before-read pattern
- Any section exceeding 20 lines
- Any existing section in any agent file was modified (non-regression violation)
