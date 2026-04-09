# Eval: Refine Skill — Re-prioritization Phase

## Setup
Invoke `/momentum:refine` on a project where:
- `stories/index.json` contains at least 10 backlog stories with varied priorities
- `_bmad-output/implementation-artifacts/sprints/` contains at least two sprint
  directories each with a retro file referencing at least one common story slug
  or topic keyword
- At least one story has `depends_on` pointing to a lower-priority story
- `_bmad-output/planning-artifacts/prd.md` exists with stated goals

Run the workflow through to the re-prioritization step (between stale-story
evaluation and consolidated findings).

## Expected Behavior

### AC1: Re-prioritization Step Exists Between Steps 6 and 7

1. After completing the stale-story evaluation step, the workflow enters a
   re-prioritization step before presenting consolidated findings
2. The step produces `{{priority_recommendations}}` — a list of stories with
   recommended priority changes and rationale
3. The consolidated findings step (now renumbered) receives
   `{{priority_recommendations}}` as a category called "Priority changes"

### AC2: Recurrence Heuristic

4. The step reads retro files from
   `_bmad-output/implementation-artifacts/sprints/*/retro-*.md`
5. Stories or topics appearing in findings across 2 or more sprint retros are
   identified as recurring pain points
6. Recommendations for these stories include rationale that cites the specific
   retro files or sprint cycles where the pattern appeared
7. The step does NOT flag stories that appear in only one retro

### AC3: Workaround Burden Heuristic

8. For stories representing manual workarounds, the step classifies burden as
   high, medium, or low based on the complexity of the workaround
9. High-burden stories are recommended for stronger promotion than low-burden ones
10. The burden classification and reasoning appear in the recommendation rationale

### AC4: Forgetting Risk Heuristic

11. For stories with workarounds, the step assesses what breaks when the
    workaround is forgotten: silent failure, recoverable failure, or cosmetic issue
12. Stories with high forgetting risk (silent failures, data degradation) are
    recommended for priority promotion regardless of workaround burden
13. The forgetting risk assessment appears in the recommendation rationale

### AC5: Dependency Promotion Heuristic

14. The step reads `stories/index.json` and checks `depends_on` + `priority` fields
15. A low or medium priority story that blocks one or more critical or high priority
    stories is identified and recommended for promotion to match the blocked story
16. Recommendations cite the specific blocker/blocked relationship (story slugs)
17. The step does NOT recommend demotion — only promotion

### AC6: Conversational Re-prioritization Discussion

18. The step does NOT present a fixed approval list — it opens a back-and-forth
    conversation with the developer
19. The initial presentation includes the heuristic findings and references goals
    from the PRD or product brief
20. The developer can agree, disagree, redirect ("focus on shipping X"), or refine
    ("also promote these others")
21. The skill adapts its recommendations based on developer input — the conversation
    is not a formulaic checklist
22. The conversation continues until the developer explicitly signals they are
    satisfied with the priority changes
23. Final agreed-upon changes are collected as `{{priority_recommendations}}`

### AC7: Agreed Changes Appear in Consolidated Findings and Apply Step

24. `{{priority_recommendations}}` flows into the consolidated findings step as a
    "Priority changes" category alongside other finding categories
25. In the "Apply approved changes" step, approved priority changes are applied via:
    `momentum-tools sprint set-priority --story SLUG --priority LEVEL`
26. The workflow does NOT call `set-priority` before the apply step — all mutations
    are deferred to that step

### Constraints: Read-Only Analysis, No Direct File Writes

27. The re-prioritization step does NOT call Edit or Write on any file
28. The re-prioritization step does NOT call `momentum-tools set-priority` — only the
    apply step does
29. All reads (retro files, stories/index.json, prd.md) are read-only queries

## Verification
- Confirm a re-prioritization step exists between stale-story evaluation and
  consolidated findings in the workflow step sequence
- Confirm the step collects `{{priority_recommendations}}` via conversation, not
  a fixed approval form
- Confirm consolidated findings includes a "Priority changes" category that feeds
  from `{{priority_recommendations}}`
- Confirm the apply step uses `momentum-tools sprint set-priority` for priority changes
- Search all workflow actions for any `set-priority` call outside the apply step —
  there must be zero
- Search all workflow actions for Edit/Write calls in the re-prioritization step —
  there must be zero
