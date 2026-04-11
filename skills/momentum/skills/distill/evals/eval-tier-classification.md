# Eval: Tier 1 vs. Tier 2 Classification

**Behavioral expectation (AC7):** Distill correctly distinguishes Tier 1 (immediately
applicable) from Tier 2 (structural) and routes accordingly.

## Scenario — Tier 1: rule addition

**Input:**
- Learning: "When invoking momentum:avfl, always pass the profile explicitly — never rely on defaults"
- Candidate: `.claude/rules/workflow-fidelity.md`

**Expected behavior:**
- Adversary confirms: single rule sentence, one file, no cross-artifact impact → Tier 1 upheld
- Phase 3 spawns write subagent to add the rule sentence
- Phase 4 runs AVFL with distill profile on the changed file
- Commits the change
- Ledger entry: `{"tier": 1, ...}`

## Scenario — Tier 2: workflow redesign

**Input:**
- Learning: "The avfl skill needs a new Phase 0 for input sanitization before any lens runs"
- Candidate: `skills/momentum/skills/avfl/workflow.md`

**Expected behavior:**
- Adversary challenges Tier 1: adding a phase touches the workflow schema, potentially
  multiple skill call sites, and requires AC specification → Tier 2 escalated
- Phase 3 spawns `momentum:create-story` with the learning as a story stub
- No practice file is modified
- No AVFL pass runs (Tier 2 path skips Phases 4 and 5 commit)
- Ledger entry: `{"tier": 2, "disposition": "stubbed", ...}`

## Observable Verification

- Tier 1: `git diff` shows the specific sentence added to the rule file; AVFL ran
- Tier 2: story file appears in `_bmad-output/implementation-artifacts/stories/`; no
  practice file diff; no AVFL invocation

## Failure Mode

- Tier 2 learning applied directly without story stub → AC7 violation
- Tier 1 learning escalated to story stub when it qualifies for direct application
  → valid but suboptimal (not a hard failure per AC7, but degrades the skill's value)
- AVFL skipped for Tier 1 → AC8 violation
