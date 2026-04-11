# Momentum Backlog Triage — 2026-04-10

**Sources synthesized:**
- Sprint-2026-04-08 retro (this sprint) — 14 action items
- Sprint-2026-04-06-2 retro — 10 action items  
- Sprint-2026-04-06 retro — 14 action items
- Nornspun upstream intake (nornspun-2026-04-10-1-retro.md) — 13 items
- Current backlog — 47 stories

**Purpose:** Deduplicated, cross-source triage for next sprint planning. Each item shows which sources raised it, whether it's already in the backlog, and recommended action.

---

## Theme Groups

### Theme 1: E2E Validator — Black-Box Enforcement
*The single highest-friction area across sprints. Recurs across 3 sprints.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| E2E validator must never inspect source files — mandatory cmux execution, zero escape hatches | sprint-2026-04-08 retro (#1), sprint-2026-04-06-2 (#8) | `e2e-validator-toolsearch-instruction` (partial — ToolSearch only) | **Critical** | New story: `e2e-validator-black-box-hardening` — approved ✓ |
| MANUAL rate >20% should trigger self-audit | sprint-2026-04-08 retro (#1) | No | **Critical** | Fold into above |
| Targeted re-check preferred over broad re-run | sprint-2026-04-08 retro (#7) | No | Medium | New story: `validator-targeted-recheck-pattern` |
| Fan-out agents: "return report as final response," not SendMessage | sprint-2026-04-08 retro (#8), sprint-2026-04-06-2 (#7) | No | Medium | New story: `fan-out-agent-prompt-fix` |
| E2E turn budget cap | — | `e2e-validator-turn-budget` ✓ | Low | Already in backlog |

**Net-new stories needed:** `e2e-validator-black-box-hardening` (approved), `validator-targeted-recheck-pattern`, `fan-out-agent-prompt-fix`

---

### Theme 2: File-Size Guidance
*Critical — appears in both momentum retro and nornspun upstream as #1 issue.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| Agent spawn prompts include known-large file hints with offset/limit | sprint-2026-04-08 retro (#2), nornspun #1 (Critical) | No | **Critical** | New story: `agent-file-size-guidance` — approved ✓ |
| Explore agents get pre-computed directory snapshot in spawn prompts | nornspun #8 (Medium) | No | Medium | Fold into above or separate story |

**Note:** 56% of nornspun's errors and 44% of momentum's errors were file-too-large. Highest-leverage single fix across both projects.

---

### Theme 3: Orchestrator & Spawn Economics
*Recurs across all 3 sprint retros.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| Orchestrator deduplication guard — never re-spawn duplicate (story, role) | sprint-2026-04-06 (#1, Critical), sprint-2026-04-06-2 (#1, Critical) | `verify-orchestrator-dedup-guard-coverage` ✓ (critical, backlog) | Critical | Already in backlog — high priority |
| Coverage analysis deduplication — cache results, don't re-spawn | nornspun #2 (Critical) | No | **Critical** | New story: `coverage-analysis-deduplication` |
| Abandoned agent observability — track 0-turn agents as waste metric | sprint-2026-04-08 retro (#12) | No | Low | New story: `agent-spawn-observability-metric` |
| Spawning mode markers in workflow steps (individual vs TeamCreate) | sprint-2026-04-06-2 (#2, Critical) | No | High | New story: `spawning-mode-markers` |
| Retro pipeline idempotency — detect prior attempt, resume or restart | sprint-2026-04-08 retro (#6) | No | High | New story: `retro-pipeline-idempotency` |

---

### Theme 4: Workflow Fidelity & Delegation
*Sprint-dev steps marked "spawn" must spawn. Recurs.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| Workflow delegation enforcement — steps marked "spawn" must spawn | sprint-2026-04-08 retro (#4), sprint-2026-04-06 (#2) | No | High | New story: `workflow-delegation-enforcement` |
| Dev agent is executor not decider — orchestrator decides, agent executes | nornspun #9 (Medium) | No | Medium | New story: `dev-agent-executor-not-decider` |
| Task tracking mandatory from session start | sprint-2026-04-06 (#3, Critical), sprint-2026-04-06-2 (#4) | No | High | `verify-task-tracking-enforcement` — check if already done |

---

### Theme 5: Spec & Story Quality
*Missing templates, missing draft markers, missing consumer audits.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| Subtractive stories require consumer audit (grep all references) | sprint-2026-04-08 retro (#3) | No | High | New story: `subtractive-story-consumer-audit` — pending Y/N |
| Story spec completeness checklist (templates, DRAFT markers, lifecycle) | sprint-2026-04-08 retro (#9) | No | Medium | New story: `story-spec-completeness-checklist` |
| Quick-fix spec placement rules (Gherkin in separate files) | nornspun #7 (Medium) | No | Medium | New story: `quick-fix-spec-placement-rules` |

---

### Theme 6: AVFL & Quality Gates
*Gaps in cross-story integration coverage and agent composition.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| AVFL cross-story integration lens | sprint-2026-04-08 retro (#5) | No | High | New story: `avfl-cross-story-integration-lens` |
| AVFL fixer agent required alongside validators | sprint-2026-04-06-2 (#3) | No | High | New story: `avfl-fixer-required-gate` |
| AVFL default agent composition by profile (scan/checkpoint/deep) | nornspun #11 (Low) | No | Low | New story: `avfl-default-agent-composition` |
| Two-phase coverage validation (enumerate + adversary in single agent) | nornspun #12 (Low) | No | Low | New story: `two-phase-coverage-validation` |
| Proactive scope recommendations from validators | nornspun #5 (High) | No | High | New story: `proactive-scope-recommendations` |
| Sprint planning staleness check (don't re-propose implemented stories) | sprint-2026-04-06-2 (#6) | No | High | New story: `sprint-planning-staleness-check` |
| Sprint planning synthesis-first (recommendations, not raw dump) | sprint-2026-04-06 (#4), sprint-2026-04-06-2 (#5) | No | High | `verify-sprint-planning-synthesis` — check if done |

---

### Theme 7: Impetus & Session UX
*Conversational design, lifecycle semantics, menu recovery.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| Impetus lifecycle & handoff fix (planning=active; return to menu after ad-hoc) | sprint-2026-04-08 retro (#10) | No | Medium | New story: `impetus-lifecycle-and-handoff-fix` |
| Epic semantic model encoded in grooming/refine skills | nornspun #4 (High) | No | High | New story: `encode-epic-semantic-model` |
| Assessment-decision pipeline (decisions step between research and backlog) | nornspun #6 (High) | `decision-skill` ✓ (done) | High | Partially done — check if gap remains |

---

### Theme 8: Retro & Transcript Pipeline
*Extraction quality, deduplication, upstream routing.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| Transcript extraction: follow worktree paths, fix UTC boundary issue | sprint-2026-04-08 retro (found this sprint) | No | **Critical** | New story: `retro-transcript-extraction-hardening` |
| DuckDB serialization bug (repr vs json.dumps) | sprint-2026-04-08 retro | No | High | Fold into above |
| Team message deduplication (3:1 duplication ratio) | sprint-2026-04-08 retro (#13) | No | Low | New story: `team-message-deduplication` |
| Filter informational non-zero exits from error extraction | sprint-2026-04-08 retro (#14) | No | Low | New story: `error-extraction-filtering` |
| Retro upstream classifier (project vs. upstream findings) | nornspun #13 (Medium) | No | Medium | New story: `retro-upstream-classifier` |

---

### Theme 9: Agent Behavior Patterns
*Investigation agents, shell verification, read-only constraints.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| Read-only investigation agents (investigate first, fix second) | nornspun #3 (High) | No | High | New story: `read-only-investigation-agents` |
| Verify shell before suggesting shell-specific commands | nornspun #10 (Medium) | No | Medium | New story: `verify-shell-before-fix` |
| Shared file contention — serialize access during parallel dev | sprint-2026-04-08 retro (#11) | No | Medium | New story: `shared-file-contention-fix` |

---

### Theme 10: Phase 7 Gate
*New this sprint.*

| Item | Sources | Backlog? | Priority | Recommended |
|------|---------|----------|----------|-------------|
| Phase 7 gate blocks until MANUAL scenarios have developer sign-off | sprint-2026-04-08 (this session) | `sprint-dev-phase-7-gate` ✓ | Medium | Already in backlog |

---

## Deduplication Summary

Items **already in backlog** (no new story needed):
- `verify-orchestrator-dedup-guard-coverage` — critical, already backlog
- `e2e-validator-turn-budget` — low, already backlog
- `sprint-dev-phase-7-gate` — medium, already backlog

Items **approved this session** (write stubs):
- `e2e-validator-black-box-hardening` ✓ (critical)
- `agent-file-size-guidance` ✓ (high)
- `subtractive-story-consumer-audit` — pending

Items **already shipped** (done, skip):
- `decision-skill` — assessment-decision pipeline partially addressed

---

## Recommended Next Sprint Candidates

**Critical (must fix):**
1. `retro-transcript-extraction-hardening` — retro is flying blind without this
2. `e2e-validator-black-box-hardening` — approved ✓, dominant sprint struggle
3. `coverage-analysis-deduplication` — 126 wasted turns per sprint in nornspun
4. `verify-orchestrator-dedup-guard-coverage` — already in backlog, critical

**High (high leverage):**
5. `agent-file-size-guidance` — approved ✓, 44-56% of all errors eliminated
6. `subtractive-story-consumer-audit` — prevents post-merge cascade failures
7. `workflow-delegation-enforcement` — recurring across 3 sprints
8. `avfl-cross-story-integration-lens` — prevents cross-story breakage
9. `retro-pipeline-idempotency` — retro was attempted 3x due to missing idempotency
10. `sprint-planning-staleness-check` — prevents re-proposing already-done work

**Medium (good sprint additions):**
11. `fan-out-agent-prompt-fix` — small, targeted, eliminates 2-4 wasted turns per validator
12. `retro-upstream-classifier` — needed for multi-project Momentum deployments
13. `impetus-lifecycle-and-handoff-fix` — repeated user correction, medium effort
14. `encode-epic-semantic-model` — prevents taxonomy migration confusion
15. `read-only-investigation-agents` — prevents git contention during debugging

---

## Full Item Count

| Source | Items | Net-New | Already Backlog | Done |
|--------|-------|---------|-----------------|------|
| sprint-2026-04-08 retro | 14 | 12 | 2 | 0 |
| sprint-2026-04-06-2 retro | 10 | 8 | 1 | 1 |
| sprint-2026-04-06 retro | 14 | 10 | 2 | 2 |
| nornspun upstream | 13 | 12 | 0 | 1 |
| **Total unique** | **~38** | **~32** | **~5** | **~4** |

*After cross-source deduplication, ~32 net-new stories. Recommend 8-10 for next sprint.*
