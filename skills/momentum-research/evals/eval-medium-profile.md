# Eval: Medium Profile — AVFL Corpus Checkpoint, Q&A, Full Pipeline

## Scenario

Given: User invokes momentum-research and provides:
- Topic: "Kubernetes vs ECS for startup infrastructure"
- Goals: "evaluate ops complexity, cost at scale, and developer onboarding"
- Profile selection: medium

## Expected Behavior

### Phase 1 (SCOPE)
1. Decomposes into 5-6 sub-questions
2. Creates project directory with `raw/`, `validation/`, `final/`
3. Writes `scope.md` with profile=medium

### Phase 2 (EXECUTE)
4. Spawns 5-6 parallel background subagents
5. Each writes to `raw/research-{subtopic}.md` with frontmatter
6. Optionally offers Gemini CLI if available

### Phase 3 (VERIFY)
7. Invokes `momentum-avfl` with:
   - `corpus: true`
   - `profile: checkpoint`
   - `output_to_validate`: array of all `raw/*.md` file paths
   - `domain_expert: "research analyst"`
   - `task_context`: describing the multi-document research corpus
8. AVFL report written to `validation/avfl-report.md`

> **Phase 3 dependency note:** This phase requires Story 8-1 (avfl-corpus-mode)
> to be implemented. Until then, Phase 3 should be a placeholder that logs
> "AVFL corpus mode not yet available — skipping verification" and continues.

### Phase 4 (Q&A)
9. Reads AVFL report to extract uncertainties and gaps
10. Presents targeted questions to the user (not generic — derived from AVFL findings)
11. Writes responses to `raw/practitioner-notes.md` with `content_origin: human`

### Phase 5 (SYNTHESIZE)
12. Reads all `raw/*.md`, `validation/*.md`, and `scope.md`
13. Final doc has `human_verified: true` (Q&A ran)
14. `derives_from` chain includes raw files, avfl-report, and practitioner-notes

### Phase 6 (COMMIT)
15. Conventional commit proposed

## What Failure Looks Like

- AVFL invoked without `corpus: true`
- AVFL report not written to `validation/avfl-report.md`
- Q&A phase presents generic questions instead of AVFL-derived ones
- Q&A runs when Phase 3 was skipped (no findings to present)
- `practitioner-notes.md` missing `content_origin: human`
- Final doc `derives_from` missing avfl-report or practitioner-notes entries
- `human_verified: false` when Q&A actually ran
