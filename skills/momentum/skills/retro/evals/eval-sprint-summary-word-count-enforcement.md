# Eval: Sprint summary enforces 500-word cap by trimming narrative and lists

## Scenario

Given a sprint (`sprint-2026-01-01`) with:
- 8 stories completed
- 6 key decisions recorded during the sprint date range
- 3 story stubs added to backlog in Phase 5
- A rich sprint narrative that, in full detail, would exceed 500 words

When the retro orchestrator drafts the sprint-summary.md, the initial draft contains more than
500 words across all sections combined.

## Expected Behavior

The retro orchestrator should:

1. After drafting the summary, count the total word count.
2. When the draft exceeds 500 words:
   a. Shorten the `## Narrative` paragraph first (reduce to 3 sentences if needed)
   b. If still over 500 words, trim the `## Key Decisions` list to the most significant items
      (most recent or highest-impact decisions)
   c. If still over 500 words, trim the `## Stories Completed vs. Planned` list
3. Write a final file that is 500 words or fewer.
4. The written file still contains all required section headings — trimming reduces content
   within sections, never removes section headings.

## What This Tests

- The 500-word limit is a hard cap that triggers active trimming, not a guideline
- Trimming order is correct: narrative first, then decisions, then story lists
- Section headings are preserved even when their content is trimmed
- The final written file is verifiably under 500 words
