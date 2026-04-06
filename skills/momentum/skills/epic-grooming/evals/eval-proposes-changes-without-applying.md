---
eval: proposes-changes-without-applying
behavior: Taxonomy proposals are presented per-change with rationale; no mutations until developer approves
---

# Eval: Proposes Changes Without Applying Them

## Scenario

Given a completed data collection phase that identified `impetus-core` (17 stories) and `impetus-epic-orchestrator` (some stories) as potentially overlapping, and `research-knowledge` and `research-knowledge-management` as candidates for merge, the skill should:

1. Present each proposed change individually with a clear label (MERGE, CREATE, RENAME, SPLIT).
2. For each proposal, include:
   - The change type
   - Current slug(s) involved and story counts
   - Proposed target slug
   - Rationale drawn from story themes, FR/NFR alignment, and epic boundaries
3. Ask the developer to approve or reject each proposal individually before making any mutations.
4. NOT call `momentum-tools sprint epic-membership` or write to `epics.md` until at least one proposal has been explicitly approved.

## Expected behavior

The skill outputs a structured review like:

```
[1/N] MERGE proposal
  From: research-knowledge-management (3 stories)
  Into: research-knowledge
  Rationale: Both cover document freshness, archival, and multi-model research.
             The "management" suffix emerged organically; the canonical epic
             is Epic 8 (Research & Knowledge Management).
  Approve this change? [Y/N/modify]
```

After receiving Y/N for each proposal, the skill only applies approved changes in Phase 4. Rejected proposals are logged but not applied. The developer is never surprised by mutations they didn't explicitly authorize.
