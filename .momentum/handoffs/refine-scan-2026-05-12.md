# Feature Grooming Refine Mode — Structured Findings

**Session Date:** 2026-05-12  
**Total Stories Analyzed:** 353  
**Total Features Analyzed:** 21  
**Epic Clusters:** 13 epic themes with 96 stories in impetus-core alone

---

## 1. Capability Clusters by Epic Slug

Based on story-to-feature mapping and thematic analysis, here are the capability clusters currently represented:

### Core Orchestration & Session
- **Epic:** `impetus-core` (96 stories)
- **Features:** momentum-impetus-session-orientation (4 done), momentum-impetus-experience (3 done, 2 remaining)
- **Related:** momentum-startup-performance (1 done, 1 remaining NFR)
- **Themes:** Session greeting, state orientation, fast startup, plugin integration, CLI tooling, session-open flow
- **Status:** Both features working/partial; impetus-core backlog heavily focused on refinements

### Agent & Team Composition
- **Epic:** `agent-team-model` (62 stories)
- **Features:** momentum-composable-specialist-agents (5 done, 45 remaining)
- **Themes:** Agent definitions, base bodies, spawn patterns, validation hardening, constellation composition
- **Critical:** This epic is the LARGEST non-completion source; 45 remaining stories suggest possible scope creep or need for prioritization

### Sprint Execution & Planning
- **Epic:** `sprint-dev-workflow` (9 stories)
- **Features:** momentum-sprint-orchestration (2 done, 5 remaining), momentum-sprint-planning-to-ready (6 done, 0 remaining)
- **Status:** Planning fully working (6/6); orchestration partial (2/7)
- **Gap:** sprint-dev-workflow stories not all mapped to existing features

### Quality & Validation
- **Epic:** `quality-enforcement` (27 stories)
- **Features:** momentum-quality-gates-enforced (6 done, 3 remaining), momentum-gherkin-separation (0 done, 2 remaining)
- **Related:** momentum-model-routing-strategy (1 done, 2 remaining for benchmarking)
- **Themes:** AVFL profiles, code review, E2E validation, Gherkin specs, quality gates
- **Status:** Enforcement infrastructure working; fixer automation and benchmark validation backlog

### Feature & Artifact Management
- **Epic:** `feature-orientation` (22 stories)
- **Features:** momentum-feature-taxonomy-maintenance (3 done, 1 remaining), momentum-canvas (2 done, **0 actual remaining** — CRITICAL DISCREPANCY)
- **Canvas Status:** Features.json shows 6 stories_remaining but all 8 stories are actually done — state mismatch
- **Themes:** Feature grooming, breakdown, canvas dashboard, three-lens visualization

### Knowledge & Research
- **Epic:** `research-knowledge` (9 stories)
- **Features:** momentum-deep-research-pipeline (3 done, 5 remaining), momentum-practice-knowledge-base (0 done, 3 remaining)
- **Themes:** Multi-model research, date anchoring, wiki-query integration, KB cold access
- **Status:** Research pipeline partial; KB integration awaiting constitution/wiki-query connection

### Practice Improvement
- **Epic:** `practice-compounds` (11 stories)
- **Features:** momentum-practice-flywheel (0 done, 3 remaining — not-started), momentum-practice-distillation (0 done, 3 remaining)
- **Status:** Both not-started; foundational for long-term compounding improvement
- **Themes:** Cross-sprint pattern detection, findings ledger, distillation workflow

### Backlog Refinement
- **Epic:** `story-cycles` (15 stories)
- **Features:** momentum-backlog-refinement (5 done, 1 remaining), momentum-quick-fix-workflow (2 done, 1 remaining)
- **Status:** Mostly working; quick-fix spec-placement-rules remaining

---

## 2. Unmapped Story Groups (Not in Any Feature's Stories Array)

**Total unmapped, non-done stories: 138**

These stories have epic slugs but no feature home. Top epic sources of unmapped stories:

| Epic Slug | Unmapped Count | Example Stories |
|---|---|---|
| impetus-core | ~40 | add-dry-run-flag-to-sprint-activate-command, benchmark-capture-from-session-transcripts, consolidate-intake-invocation-and-fix-error, create-story-update, dev-agent-hook-self-check |
| feature-orientation | ~10 | canvas-features-lens, canvas-flywheel-lens, canvas-level-2-feature-detail, canvas-reading-mode-polish, canvas-sprints-lens |
| quality-enforcement | ~15 | avfl-consolidator-stylistic-filter, avfl-cross-story-integration-lens, avfl-timeout-surfacing-scoring-stability, code-reviewer-withmartian-replay-fixture |
| agent-team-model | ~8 | build-guidelines-soft-stop-ux-for-missing-vault, e2e-validator-turn-budget, citation-integrity-validation-in-build-guidelines-avfl |
| performance-validation | ~10 | architecture-guard-fixture-false-positive-rate, avfl-fixture-declining-skepticism-convergence, avfl-fixture-enumeration-completeness-recall, bash-benchmarking-script-captures-time-cost-and-tokens |
| impetus-epic-orchestrator | ~7 | encode-epic-semantic-model, epic-dependency-tracking-and-cascade-notifications |
| story-cycles | ~8 | commit-summary-template-enumerates-in-scope-out-of-scope-by-ac, create-story-advanced-elicitation, dev-previous-story-continuity |
| artifact-provenance | ~5 | claim-level-provenance-status-and-integrity-enforcement, decision-fixture-sdr-cites-source-research |

**Signal:** Many of these unmapped stories are refinement/fixture/benchmarking work that sits at the boundary of feature scope — they're real work but not attached to feature homes.

---

## 3. Stale Feature Signals

### **CRITICAL: momentum-canvas Story State Mismatch**
- **Feature:** momentum-canvas
- **Stated Status:** `not-started`, stories_remaining: 6
- **Actual Status:** ALL 8 STORIES ARE DONE
  - feature-status-skill ✓
  - feature-status-practice-path ✓
  - momentum-cycle-dashboard-shell-hono-bun-server ✓
  - momentum-cycle-features-lens ✓
  - momentum-cycle-cycle-timeline-lens ✓
  - momentum-cycle-sprint-lens-sprint-detail-drill-down ✓
  - momentum-cycle-feature-l2-drill-down-reading-mode ✓
  - momentum-cycle-story-l3-drill-down-reading-mode ✓
- **Action Required:** Update features.json: change `status: "not-started"` → `status: "working"`, set `stories_remaining: 0`, set `stories_done: 8`

---

## 4. Quality NFR Gaps

Architectural NFRs mentioned in architecture.md NOT surfaced as standalone features:

1. **Observability & Logging** — No standalone feature (partially in retro workflow)
2. **Context Budget Management** — No feature (training/hygiene needed)
3. **Provenance & Staleness Detection** — Feature exists (not-started, 0 done) — PROMOTE
4. **Plugin Ecosystem Resilience** — Feature exists (not-started, 0 done) — DEFER explicitly
5. **Cost Management via Model Routing** — Feature exists (partial, benchmarking backlog)
6. **Resilience & Error Recovery** — Not surfaced

**Recommendation:** Promote momentum-provenance-chain; consider momentum-agent-observability extraction

---

## 5. Refine Signal Scan — MERGE / SPLIT / DEDUP / RETIRE / UPDATE

### **MERGE: NOT RECOMMENDED**
- impetus-session-orientation + impetus-experience → Keep separate (state vs personality)
- assessment-decision-pipeline + deep-research-pipeline → Keep separate (sequential, not merged)
- quality-gates-enforced + gherkin-separation → Keep separate (enabling vs enforcement)

### **SPLIT: CRITICAL OPPORTUNITY**

**momentum-composable-specialist-agents (50 stories) → Split into 4 features:**

1. **momentum-agent-definitions** (22 stories)
   - Tier A project-conditioned + Tier B shipped customs
   - Two-tier taxonomy completion (DEC-013, DEC-016)

2. **momentum-agent-constitution-builder** (6 stories)
   - Hot constitution generation + wiki-query integration
   - Tier 3 cold KB for all agents

3. **momentum-build-guidelines-gen2** (2 stories)
   - Gen-2 guidelines with base bodies
   - Sprint-planning integration

4. **momentum-agent-spawn-orchestration** (8 stories)
   - Spawn preflight, observability, validation hooks
   - Reliable team execution

**Rationale:** Each feature has single outcome; enables parallelization; improves burndown visibility

### **DEDUP: Check for Duplicates**
- Constitution work split across momentum-agent-constitution-builder + momentum-practice-knowledge-base
- E2E validator stories in quality-gates-enforced + composable-specialist-agents → Same slug?

### **RETIRE: Conditional Decisions**
- momentum-protocol-based-integration (not-started) → DEFER explicitly until vendor pain surfaces
- momentum-practice-flywheel (not-started) → PROMOTE to explicit priority queue (transformative value)
- momentum-provenance-chain (not-started) → PROMOTE to visible roadmap (architecture requirement)

### **UPDATE: Stale Value Analyses**
- momentum-canvas → All 8 stories done; status should be "working"; rewrite value_analysis
- momentum-practice-knowledge-base → Wiki skills installed, nornspun operational; update to reflect current state
- momentum-deep-research-pipeline → Last verified 26 days ago; needs re-verification

---

## 6. Obsolescence Scan: constitution-builder & frontend-dev Implications

With constitution-builder and frontend-dev skills now active, composable-specialist-agents has **low obsolescence risk:**

- dev-agent-definition-files (done) → Keep as historical reference; note constitution-builder supersedes
- dev-agent-executor-not-decider (backlog) → Retain (behavioral spec, not implementation-specific)
- e2e-client-side-coverage (backlog) → Keep with clarification (Maestro/cmux-browser patterns for Compose)
- e2e-and-qa-validator-prompts-branch-standalone-vs-team (backlog) → Retain (orchestration, not stack-specific)

**Summary:** No bulk obsolescence. Composable agents feature is enabled by (not threatened by) new skills.

---

## Critical Actionable Findings

| Finding | Severity | Action |
|---------|----------|--------|
| momentum-canvas state mismatch (8 done, marked not-started) | **CRITICAL** | Update features.json immediately |
| 138 unmapped non-done stories | **HIGH** | Triage fixture/benchmark work; create feature homes for orphaned themes |
| momentum-composable-specialist-agents mega-feature (50 stories) | **HIGH** | Split into 4 focused features; sequence delivery |
| momentum-provenance-chain not-started (architecture requirement) | **HIGH** | Promote to visible priority queue |
| NFR observability gaps | **MEDIUM** | Extract momentum-agent-observability; defer others |

