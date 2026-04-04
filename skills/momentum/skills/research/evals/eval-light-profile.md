# Eval: Light Profile — 3 Agents, No AVFL, No Q&A, Final Doc Produced

## Scenario

Given: User invokes momentum-research and provides:
- Topic: "comparison of React vs Svelte for small teams"
- Goals: "evaluate DX, bundle size, and hiring availability"
- Profile selection: light

## Expected Behavior

### Phase 1 (SCOPE)
1. Skill elicits topic and goals interactively
2. Proposes exactly 3 sub-questions covering the topic (light profile cap) (e.g., developer experience comparison,
   bundle size benchmarks, job market availability)
3. User selects "light" profile
4. Creates project directory `{output_folder}/research/react-vs-svelte-{YYYY-MM-DD}/`
   with `raw/`, `validation/`, `final/` subdirectories
5. Writes `scope.md` with topic, goals, sub-questions, profile=light, date

### Phase 2 (EXECUTE)
6. Spawns exactly 3 parallel background subagents — one per sub-question
7. Each subagent receives a briefing with: date anchoring, primary source directive,
   evidence notation ([OFFICIAL]/[PRAC]/[UNVERIFIED]), output format instructions
8. Each writes to `raw/research-{subtopic-slug}.md` with `content_origin: claude-code-subagent`
   in frontmatter
9. Each returns a 2-3 sentence inline summary

### Phase 3 (VERIFY) — SKIPPED
10. Light profile skips Phase 3 entirely — no AVFL invocation, no validation/ output

### Phase 4 (Q&A) — SKIPPED
11. Light profile skips Phase 4 entirely — no practitioner-notes.md

### Phase 5 (SYNTHESIZE)
12. A single Opus subagent runs in the foreground
13. Subagent reads all `raw/*.md` files and `scope.md` from disk
14. Writes `final/{topic-slug}-final-{YYYY-MM-DD}.md`
15. Final doc frontmatter includes `content_origin: claude-code-synthesis`,
    `human_verified: false`, and `derives_from` chain listing each raw file

### Phase 6 (COMMIT)
16. Proposes a conventional commit: `docs(research): comparison of React vs Svelte...`
17. Waits for user confirmation before committing

## What Failure Looks Like

- Fewer or more than 3 agents spawned for light profile
- AVFL invoked on light profile (should be skipped)
- Q&A phase runs on light profile (should be skipped)
- No `scope.md` written before agents spawn
- Subagents lack date anchoring or evidence notation in briefings
- Final doc missing `derives_from` chain or `content_origin`
- `human_verified: true` on light profile (should be false — no Q&A ran)
- Synthesis agent runs in background instead of foreground
- Auto-commits without user confirmation
