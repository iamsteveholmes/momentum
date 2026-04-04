# Eval: Resume Support — Only Missing Subtopics Re-Researched

## Scenario

Given: A momentum:research project directory already exists at
`{output_folder}/research/k8s-vs-ecs-2026-04-04/` with:

```
scope.md              # complete — 5 sub-questions defined, profile=medium
raw/
  research-ops-complexity.md    # complete — written by previous session
  research-cost-at-scale.md     # complete — written by previous session
  research-developer-onboarding.md  # MISSING — agent failed (rate limit)
  research-security-model.md    # MISSING — agent never spawned
  research-ecosystem-maturity.md    # complete — written by previous session
```

User re-invokes momentum:research on the same project directory.

## Expected Behavior

1. Phase 1 (SCOPE): Detects existing `scope.md` — does NOT re-elicit topic or
   sub-questions. Reads the existing scope and presents a summary: "Found existing
   research project with 5 sub-questions. 3 of 5 raw files exist."

2. Phase 2 (EXECUTE): Checks which `raw/research-*.md` files exist by scanning
   the directory. Identifies 2 missing subtopics: `developer-onboarding` and
   `security-model`.

3. Spawns exactly 2 agents (NOT 5) — one for each missing subtopic only.

4. Existing files (`ops-complexity`, `cost-at-scale`, `ecosystem-maturity`) are
   NOT overwritten, NOT re-read by new agents, and NOT re-researched.

5. After the 2 new agents complete, all 5 `raw/` files exist. Pipeline continues
   to Phase 3+ normally.

## What Failure Looks Like

- Skill re-elicits topic and creates a new project directory instead of resuming
- All 5 agents spawned instead of only the 2 missing ones
- Existing `raw/` files are overwritten or deleted
- Skill fails to detect which files already exist
- Skill creates a new `scope.md` instead of reading the existing one
- The 2 new agents don't receive the same briefing template and evidence notation
  as the originals would have
