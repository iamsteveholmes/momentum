# Eval: Story Counts Never Lead

## Scenario

Given an active sprint carrying several completed stories and a fixture `.momentum/features.json`
with a known passing/total mix (e.g., 1 of 5 passing), when a fresh session starts and Impetus
renders the situational report:

The skill should:
1. Lead the report with the feature number (N of M), not a count of stories done, in progress, or
   planned
2. Place any story number that does appear after the feature number, as supporting detail only
3. Keep the report within its 2-sentence budget with ledger counts still inline

## NOT Expected

- A story count as the first fact in the report
- Story throughput presented as the headline while the feature number is demoted or absent
- The feature number omitted because a story count was judged more newsworthy
