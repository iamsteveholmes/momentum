# Sprint Plan — sprint-2026-04-08

**Stories:** 12 | **Waves:** 3 | **Specialist:** dev-skills (all) | **Guidelines:** .claude/rules/dev-skills.md

---

## Stories (grouped by wave)

### Wave 1 (10 stories, parallel)

| # | Story | Priority | Change Type | Epic |
|---|---|---|---|---|
| 1 | **intake-skill** — Lightweight Story Capture from Conversation | H | skill-instruction | impetus-core |
| 2 | **refine-reprioritization** — Add Priority Change Phase to Backlog Refinement | H | skill-instruction | impetus-epic-orchestrator |
| 3 | **quality-gate-parity-across-workflows** — Align quick-fix Gates, Remove /develop | H | skill-instruction | quality-enforcement |
| 4 | **agent-prompt-large-file-guidance** — Standard Instructions for Large Files | C | skill-instruction | agent-team-model |
| 5 | **impetus-journal-hygiene-script** — Move Thread Computations to momentum-tools | H | code + skill-instruction | impetus-core |
| 6 | **8-3-gemini-deep-research-automation** — cmux-browser Integration for Research | L | skill-instruction | research-knowledge |
| 7 | **gherkin-acs-and-atdd-workflow-active** — Outsider Test Enforcement and Spec Quality | H | skill-instruction | story-cycles |
| 8 | **hooks-global-distribution** — Move Hook Scripts to Global Path | H | config-structure | impetus-core |
| 9 | **remove-agent-journals** — Delete Sprint-Log Write Infrastructure | H | script-code | impetus-core |
| 10 | **assessment-skill** — Guided Product State Evaluation | H | skill-instruction | impetus-epic-orchestrator |

### Wave 2 (after Wave 1)

| # | Story | Priority | Change Type | Epic | Depends on |
|---|---|---|---|---|---|
| 11 | **decision-skill** — Capture Strategic Decisions from Assessments | H | skill-instruction | impetus-epic-orchestrator | assessment-skill |

### Wave 3 (after Wave 2)

| # | Story | Priority | Change Type | Epic | Depends on |
|---|---|---|---|---|---|
| 12 | **refine-assessment-decision-review** — Assessment & Decision Review Step | M | skill-instruction | impetus-epic-orchestrator | assessment-skill, decision-skill |

---

## Team Composition

| Role | Stories | Agent File | Guidelines |
|---|---|---|---|
| Dev (dev-skills) | All 12 | `skills/momentum/agents/dev-skills.md` | `.claude/rules/dev-skills.md` (present) |
| QA Reviewer | Sprint-wide | `skills/momentum/agents/qa-reviewer.md` | Built-in |
| E2E Validator | Sprint-wide | `skills/momentum/agents/e2e-validator.md` | Built-in |
| Architect Guard | Sprint-wide | `skills/momentum/skills/architecture-guard/SKILL.md` | Built-in |

---

## Merge Conflict Risks (Wave 1)

These files are touched by multiple Wave 1 stories — require sequential merge resolution:

| File | Stories |
|---|---|
| `skills/momentum/skills/dev/workflow.md` | gherkin-acs, remove-agent-journals |
| `skills/momentum/skills/sprint-dev/workflow.md` | gherkin-acs, remove-agent-journals |
| `skills/momentum/skills/sprint-planning/workflow.md` | gherkin-acs, remove-agent-journals |
| `skills/momentum/skills/quick-fix/workflow.md` | quality-gate-parity, remove-agent-journals |
| `skills/momentum/scripts/momentum-tools.py` | impetus-journal-hygiene, remove-agent-journals |
| `skills/momentum/scripts/test-momentum-tools.py` | impetus-journal-hygiene, remove-agent-journals |
| `skills/momentum/references/hooks-config.json` | hooks-global-distribution, remove-agent-journals |
| `skills/momentum/agents/e2e-validator.md` | agent-prompt, gherkin-acs |
| `skills/momentum/skills/impetus/workflow.md` | quality-gate-parity, impetus-journal-hygiene |

**Recommended merge order:** `remove-agent-journals` first (purely subtractive — creates cleanest base), then additive stories.

---

## Gherkin Specs

12 feature files in `sprints/sprint-2026-04-08/specs/`:

| Story | Scenarios |
|---|---|
| intake-skill | 3 |
| refine-reprioritization | 3 |
| quality-gate-parity-across-workflows | 5 |
| agent-prompt-large-file-guidance | 4 |
| impetus-journal-hygiene-script | 10 |
| 8-3-gemini-deep-research-automation | 5 |
| gherkin-acs-and-atdd-workflow-active | 4 |
| hooks-global-distribution | 3 |
| remove-agent-journals | 4 |
| assessment-skill | 6 |
| decision-skill | 5 |
| refine-assessment-decision-review | 5 |

---

## Spec Impact Applied

**Architecture (4 changes):**
- Decision 24: Agent journals marked Historical — removed
- Decision 39: dev internal-only, code review in quick-fix, deferred worktree cleanup
- Decisions 29/30: Spec quality pre-check gate, spec-quality feedback loop tag
- Refine Read/Write Authority: expanded for assessments/ and decisions/

**PRD (7 changes):**
- REMOVED: FR56, FR57, FR89 (agent journal infrastructure)
- UPDATED: FR85 (spawn dedup now observable via transcript)
- MODIFIED: FR53 (dev internal-only), FR58/FR40 (spec quality pre-check + feedback)
- NEW: FR95 (quality gate parity)

---

## AVFL Checkpoint Result

**Score after fix pass:** Estimated 92-95 (all HIGH and MEDIUM findings fixed)

**Findings fixed:** 14 across 8 stories
- 4 HIGH: task/AC contradiction, wrong log counts, wrong config file, wrong path
- 6 MEDIUM: already-applied spec updates, missing touches, wrong change_type, AC hedge, missing section, retro scope
- 4 LOW: epic_slug mismatch, sprint slug, Gherkin outsider-test violations, missing touches

**Status:** CHECKPOINT_WARNING — plan proceeds with known minor issues addressed.

---

## Sprint Summary

| Metric | Value |
|---|---|
| Stories | 12 |
| Epics touched | 6 |
| Priority distribution | 1 critical, 9 high, 1 medium, 1 low |
| New skills created | 3 (intake, assessment, decision) |
| Workflows modified | 6 (refine, quick-fix, sprint-planning, sprint-dev, dev, impetus) |
| CLI commands added | 2 (journal-hygiene, journal-append) |
| CLI commands removed | 1 (log) |
| Hook scripts relocated | 3 (stop-gate, lint-format, file-protection) |
| Hook scripts deleted | 2 (subagent-start, subagent-stop) |
| Agent definitions modified | 6 (all agents get large-file guidance) |
| Planning artifact types added | 2 (assessments/ASR, decisions/SDR) |
