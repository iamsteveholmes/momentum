---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Where Momentum is superior to everything-claude-code or has features ECC lacks"
topic: "everything-claude-code vs Momentum — comparative analysis"
---

# Where Momentum is Superior to ECC (or Has Features ECC Lacks)

## Inline Summary

Momentum's three biggest superiorities over ECC, all verified by reading both repos: (1) **a real sprint state machine with a sole-writer pattern** (Momentum has `stories/index.json` + `sprints/index.json` + `sprint-manager` skill enforcing legal transitions; an exhaustive scan of ECC's 2,662-file tree returns zero hits for `sprint`, `backlog`, `epic`, `retro`, `stories`, `state-machine`, `index.json`); (2) **a multi-agent dual-reviewer validation framework with a fix loop and benchmarked role-tier configuration** (Momentum AVFL: 2 framings × 4 lenses × iterative fix vs. ECC's `santa-method` which has the dual-reviewer idea but is binary pass/fail with no lens decomposition, no benchmarked role tiers, and no scan/gate/checkpoint profiles); (3) **a coherent practice — Gherkin/ATDD specs, change-type story classification, decision documents, intake event log, plan-audit hook gate, retro auditor team — that ECC simply does not have any of**. ECC is broader (183 skills vs Momentum's ~26) and more polished as a marketed product, but it is a horizontal toolkit; Momentum is a vertical practice. File-path evidence: `_bmad-output/implementation-artifacts/sprints/index.json`, `skills/momentum/skills/sprint-manager/workflow.md`, `skills/momentum/skills/avfl/SKILL.md`, vs. ECC `skills/santa-method/SKILL.md`, `skills/verification-loop/SKILL.md`, `AGENTS.md`.

---

## Method and Evidence Discipline

I verified ECC's surface using `gh api repos/affaan-m/everything-claude-code/git/trees/main?recursive=1` (2,662 path entries) and read SKILL.md content directly via the GitHub Contents API. I will not claim ECC "lacks X" without saying I scanned the full tree for X. Tags: **[OFFICIAL]** = source code present in repo and read directly; **[PRAC]** = inferred from documented practice/usage in the repo; **[UNVERIFIED]** = stated by repo marketing but not verified in code.

ECC repo state at scan time **[OFFICIAL]**: 167K stars, 26K forks, default branch `main`, 2,662 path entries, version `1.10.0`, ~38 agents, ~156 skills, ~72 legacy command shims (per `README.md` "What's New v1.10.0"). Note: README claims `140K+ stars` while API returns 167K — README is stale on this number, but it is consistent with rapid recent growth, not a fabrication.

Momentum repo state **[OFFICIAL]**: `skills/momentum/.claude-plugin/plugin.json` reports version `0.17.0`. Skill count from `ls skills/momentum/skills/`: 25 skills (`ls | wc -l` = 25), 16 slash commands in `commands/` — all part of an integrated practice. No marketed star count.

---

## 1. AVFL — Adversarial Validate-Fix Loop

**Momentum** [OFFICIAL]: `skills/momentum/skills/avfl/SKILL.md` defines a four-phase pipeline (VALIDATE → CONSOLIDATE → EVALUATE → FIX). Distinguishing properties:

- **Four orthogonal lenses**: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness (line 122–141). Each lens binds to specific dimensions from `references/framework.json`.
- **Two framings per lens — Enumerator (systematic) and Adversary (intuitive)** — explicitly designed to break shared-bias failure (line 145–158). Cross-check confidence: HIGH if both reviewers found it, MEDIUM if only one (then consolidator investigates).
- **Four named profiles**: `gate` (1 agent, no fix), `checkpoint` (1 per lens, 1 fix attempt), `full` (8 agents, 4 fix iterations), `scan` (8 agents, no fix, structured handoff). Lines 95–117.
- **Benchmarked role-tier configuration** (line 182–197): "36 runs across 3 models × 3 effort levels × all roles" → Enumerator=Sonnet/medium, Adversary=Opus/high, Consolidator=Haiku/low, Fixer=Sonnet/medium. Specific anti-patterns called out: "Do not use Haiku for Enumerator validators" (false-pass at 92/100), "Do not use Sonnet for Adversary validators" (severity downgrade defect).
- **Skepticism scheduling**: hardcoded high (3) on iteration 1, low (2) on subsequent — "skepticism=1 collapses Enumerator and Adversary to identical output, eliminating dual-review value entirely."
- **Stage parameter** (`draft`/`checkpoint`/`final`) controls whether absence counts as a finding — orthogonal to profile (line 62–73).
- **Corpus mode** validates multi-document sets together with cross-document consistency dimensions and an authority hierarchy for resolving contradictions (line 35–60).

**ECC** [OFFICIAL]: Two relevant analogues exist in the adversarial-validation neighborhood.

- `skills/santa-method/SKILL.md` (306 lines, single file) — "Multi-agent adversarial verification with convergence loop." Has Phase 1 Generate, Phase 2 dual independent review (Reviewer B and Reviewer C in parallel, context-isolated), Phase 3 Verdict Gate (binary PASS/FAIL — both must pass), Phase 4 Fix Cycle. **This is the closer AVFL analogue conceptually**, attributed to "Ronald Skelton — Founder, RapportScore.ai." But it differs materially: only **two reviewers**, no lens decomposition, no dimension taxonomy, no profiles (gate/checkpoint/full/scan), no scan-mode handoff format, no benchmarked role assignments per agent type, no skepticism scheduling, no stage parameter, no corpus mode. The structured output is a generic JSON verdict, not a 15-dimension finding schema.
- `skills/gan-style-harness/SKILL.md` — Generator + Evaluator + Playwright loop engineered for *building a whole app from a prompt* and evaluating it against live-app criteria. Three roles (Planner → Generator → Evaluator), iterates 5–15 times, scores against 4 weighted criteria (Design Quality, Originality, Craft, Functionality). Relevant to AVFL's "adversarial generator should not grade itself" principle but aimed at live-app generation rather than artifact validation.
- `skills/verification-loop/SKILL.md` — a **single-agent** sequential checklist (build → typecheck → lint → tests → security → diff). No subagents. No adversarial reviewer. This is closer to Momentum's `bmad-dev-story` DoD verification than to AVFL.

**Verdict**: Momentum's AVFL is materially more sophisticated than santa-method on every measurable axis except brevity. ECC has two skills in the same design neighborhood (santa-method for dual-review artifact validation, gan-style-harness for live-app generation+evaluation) — neither matches AVFL's lens-decomposed multi-profile design, and neither has corpus mode, authority-hierarchy resolution, or benchmarked role assignments. ECC has nothing like Momentum's `scan` profile (post-merge structured-handoff discovery pass) — a feature Momentum specifically uses for post-sprint AVFL.

---

## 2. Gherkin / ATDD Acceptance Specs

**Momentum** [OFFICIAL]: `skills/momentum/skills/sprint-planning/workflow.md` (grep result) generates `.feature` files for every story in the sprint:
- Path convention: `_bmad-output/implementation-artifacts/sprints/{sprint_slug}/specs/{story_slug}.feature`. Verified file present: `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-14/specs/triage-skill.feature`.
- Specs are written for an **E2E Validator** that is a black-box agent — explicitly cannot read source. Outsider Test enforced.
- Reference template at `skills/momentum/references/gherkin-template.md` with anti-patterns enforced via post-generation validation (no AC numbers, no Phase numbers in scenario names, no internal agent/tool/file refs).
- Decision 30 black-box separation: dev agents implement against plain-English ACs in the story file; only the validator sees the `.feature` files.

**ECC** [OFFICIAL]: Tree scan results — `gherkin: 0 matches`, `atdd: 0 matches`, `.feature: 0 matches`, `acceptance: 0 matches`. ECC has `e2e-testing`, `tdd-workflow`, `tdd-guide` agent, and Playwright integrations, but no behavioral spec format, no Outsider Test discipline, and no separation between code-blind validators and dev agents.

**Verdict**: This is a Momentum capability ECC entirely lacks. ECC's testing skills are about how to write tests in code; Momentum has a behavioral specification layer above that.

---

## 3. Sprint State Machine — `stories/index.json` + `sprints/index.json` + Sole-Writer Pattern

**Momentum** [OFFICIAL]:
- `_bmad-output/implementation-artifacts/stories/index.json` — every story keyed by slug, with `status`, `epic_slug`, `depends_on`, `touches`, `priority`. Verified file content.
- `_bmad-output/implementation-artifacts/sprints/index.json` — single canonical structure: `active`, `planning`, `completed[]`. Each sprint has `slug`, `stories`, `team_composition` (per-story roles, change_type, guidelines, test_approach, wave, dependencies), `waves`, `started`, `completed`, `retro_run_at`. Verified.
- Sprint directories: 15 completed sprints in `_bmad-output/implementation-artifacts/sprints/` (sprint-2026-04-04 through sprint-2026-04-14), plus 4 quickfix sprints.
- `skills/momentum/skills/sprint-manager/workflow.md` defines the sole-writer pattern — explicit text: "You are the **sole writer** of `stories/index.json` and `sprints/index.json`. No other agent or script writes to these files."
- State machine (workflow.md line 44–50): ordered states `backlog` → `ready-for-dev` → `in-progress` → `review` → `verify` → `done`; terminal: `done`, `dropped`, `closed-incomplete`. Backward transitions illegal without `force: true`. Non-adjacent forward transitions illegal. Detailed in `references/state-machine.md`.
- Five well-defined actions: `status_transition`, `sprint_activate`, `sprint_complete`, `epic_membership`, `sprint_plan` — each with parameter list, procedure, return JSON.

**ECC** [OFFICIAL]: Tree scan — `sprint: 0 matches`, `backlog: 0 matches`, `epic: 0 matches`, `state-machine: 0 matches`, `index.json: 0 matches`, `sole-writer: 0 matches`. ECC has `loop-operator` agent and `loop-start`/`loop-status` commands for autonomous loop execution; it has `feature-dev.md` command (Discovery → Exploration → Clarifying Q → Architecture → Implementation → Review → Summary) — but these are session-scoped workflows. There is no concept of a sprint, no backlog persistence between sessions, no story status, no concurrency control on a shared index.

**Verdict**: This is the single biggest gap. ECC has zero unit-of-work persistence across sessions beyond instinct memory and SQLite session state. Momentum runs a real planning cadence; ECC runs autonomous loops. They are different paradigms.

---

## 4. Change-Type Classification on Stories

**Momentum** [OFFICIAL]: `skills/momentum/skills/create-story/workflow.md` (grep verified) classifies tasks within a story into one of: `skill-instruction`, `script-code`, `rule-hook`, `config-structure`, `specification`, or `unclassified`. Reference file: `skills/momentum/skills/create-story/references/change-types.md`. Each type triggers a specific implementation guidance template injected into the story's Dev Notes — for example, `skill-instruction` requires EDD with three behavioral evals before touching the skill file; `script-code` requires TDD; `config-structure` requires direct + inspect; `specification` requires direct authoring with cross-reference verification.

**ECC** [OFFICIAL]: Tree scan — `change-type: 0 matches`. ECC's `tdd-guide` agent picks TDD for everything. There is no concept that prompt-engineering changes need EDD while shell scripts need TDD. The `tdd-workflow` skill is one-size-fits-all.

**Verdict**: Momentum capability with no ECC analogue. This matters specifically for an agentic-engineering practice, where you are simultaneously editing executable code AND prompt content — and the right test discipline is different.

---

## 5. Intake Queue Event Log (`intake-queue.jsonl`)

**Momentum** [OFFICIAL]: `_bmad-output/implementation-artifacts/intake-queue.jsonl` — append-only event log. Verified entries with structured fields: `id`, `timestamp`, `source` (retro/triage/etc.), `kind` (handoff/shape/etc.), `status` (open/consumed), `title`, `description`, `sprint_slug`, `feature_slug`, `story_type`, `feature_state_transition` (with `prior_state`/`observed_state`/`evidence`), `failure_diagnosis` (with `attempted`/`didnt_work`/`learned`), `consumed_at`, `outcome_ref`. The retro skill emits findings to this queue; sprint-planning consumes "open findings not stubbed in their originating retro" via Handlebars-style templates (verified in workflow.md).

**ECC** [OFFICIAL]: Tree scan — only two `.jsonl` hits, both `skills/skill-comply/fixtures/` test fixtures. The `continuous-learning-v2` skill writes `observations.jsonl` per project (read in SKILL.md content), but that captures tool-use observations for instinct extraction, not backlog items with cross-sprint handoff. ECC has no concept of an open backlog item that survives a session.

**Verdict**: Momentum capability with no ECC analogue. ECC's nearest construct is `continuous-learning-v2` observations, but it serves a different purpose (skill evolution, not work tracking).

---

## 6. Decision Documents as First-Class Artifacts

**Momentum** [OFFICIAL]: `skills/momentum/skills/decision/SKILL.md` — "Decision recorder — not deliberator. The thinking already happened." Walks findings from assessments/research, records adopt/reject/defer, writes a linked decision document. Plus `momentum:assessment` produces structured assessment documents.

**ECC** [OFFICIAL]: `skills/architecture-decision-records/SKILL.md` — yes, ECC has ADRs in Michael Nygard format. Reads existing ADRs, captures new ones, manages `docs/adr/README.md` index. **This is a real analogue**, and it is well-implemented (asks for confirmation before creating directory, requires explicit approval before writing). Also: `skills/council/SKILL.md` — a four-voice deliberation skill (Architect/Skeptic/Pragmatist/Critic) that explicitly closes with "When the council materially changes the recommendation: use `knowledge-ops` to store the lesson."

**Verdict**: This is one capability where ECC matches Momentum. ECC's ADR skill is technically more polished as a single-skill artifact (more careful about consent, has format inspiration cited), and its `council` skill has no Momentum analogue. Momentum's `decision` skill is integrated with the assessment pipeline (it consumes assessment-document findings); ECC's ADR is standalone. Even-to-Momentum-favored on integration, even-to-ECC-favored on standalone polish.

---

## 7. Epic / Feature Taxonomy Grooming

**Momentum** [OFFICIAL]: Three skills:
- `skills/momentum/skills/feature-grooming` — "Feature grooming — holistic feature taxonomy discovery, value analysis, and features.json maintenance."
- `skills/momentum/skills/epic-grooming` — "Epic grooming — holistic taxonomy analysis, orphan resolution, and story reclassification."
- `skills/momentum/skills/feature-breakdown` — "Enumerating missing stories for a feature end to end."
Plus `feature-status` which generates an HTML planning artifact showing feature coverage gaps and story assignments. The `epic_slug` field on every story (verified in `stories/index.json`) is the linking primitive.

**ECC** [OFFICIAL]: Tree scan — `epic: 0 matches`. ECC has `skills/product-capability/`, `skills/product-lens/`, and a `feature-dev.md` command, but these are about how to design and ship a single feature within a session. No multi-story rollup, no orphan story detection, no feature coverage matrix.

**Verdict**: Momentum capability with no ECC analogue.

---

## 8. Plan-Audit Hook Gate (`ExitPlanMode` Spec Impact Gate)

**Momentum** [OFFICIAL]: `.claude/rules/plan-audit.md` — explicit text: "Before calling `ExitPlanMode`, always check whether the active plan file contains a `## Spec Impact` section. If absent: invoke `momentum:plan-audit` first, wait for it to complete and write the section, then call `ExitPlanMode`. Do not call `ExitPlanMode` until `## Spec Impact` is present in the active plan file." Backed by `skills/momentum/skills/plan-audit/SKILL.md` which classifies trivial vs. substantive changes and writes the section.

**ECC** [OFFICIAL]: Tree scan — `ExitPlanMode: 0 matches`, `plan-audit: 0 matches`, `spec-impact: 0 matches`. ECC does have hook-enforced gates — most notably `skills/gateguard/SKILL.md`, a PreToolUse fact-forcing gate ("DENY → FORCE → ALLOW") backed by `scripts/hooks/gateguard-fact-force.js`. GateGuard demands the agent list importers, schemas, and quote the user instruction before the first edit. **This is a real, well-evidenced gate skill** with A/B test data (+2.25 points avg). But it is a generic fact-forcing gate, not a plan-mode → spec-impact gate. The two skills serve different purposes: GateGuard prevents under-investigation; plan-audit prevents incomplete spec-traceability when leaving plan mode.

**Verdict**: Both repos have hook-enforced gates as a pattern. ECC's GateGuard is broader and has measurement; Momentum's plan-audit gate is specific to a workflow stage that ECC's product doesn't model. Tied on hook-gate sophistication, Momentum-favored on plan-mode-specific guardrail.

---

## 9. Persistent Multi-Conversation Memory with Typed Memories

**Momentum** [OFFICIAL]: `~/.claude/projects/-Users-steve-projects-momentum/memory/` — typed memories under explicit prefixes (`feedback_*.md`, `project_*.md`, `reference_*.md`). 18 feedback files, 4 project files, 1 reference file at scan time. Indexed in `MEMORY.md` with the type taxonomy: Feedback / Reference / Project. Each entry has a one-line summary in the index that links to the full file. The user's CLAUDE.md confirms this memory file is auto-loaded per session.

**ECC** [OFFICIAL]: `skills/continuous-learning-v2/SKILL.md` (verified content) implements project-scoped instincts in `~/.claude/homunculus/projects/<hash>/instincts/personal/` plus global instincts in `~/.claude/homunculus/instincts/personal/`. Key features Momentum lacks: confidence scoring (0.3–0.9), domain tagging, evolution to skill/command/agent (`/evolve`), promotion from project to global (`/promote`), export/import (`/instinct-export`/`-import`), automated extraction from PreToolUse/PostToolUse hooks via background Haiku agent.

**Verdict**: ECC's continuous-learning-v2 is a more sophisticated **automated** memory system. Momentum's auto-memory is **simpler but typed**. They are different points in design space — ECC favors automation and confidence scoring; Momentum favors simple typed durable knowledge with manual curation. **Tied to ECC-favored on automation; Momentum-favored on typed clarity and zero-config setup**. This is the one capability where ECC arguably exceeds Momentum.

---

## 10. Skill Discipline / Orchestrator Purity

**Momentum** [OFFICIAL]: `~/.claude/projects/.../memory/feedback_orchestrator_purity_quickfix.md` and feedback-followed Decision 3d — orchestrator skills (Impetus, sprint-dev, quick-fix) MUST NOT write files directly; only spawn subagents with file-writing authority. `skills/momentum/skills/architecture-guard/SKILL.md` (verified content) calls this out specifically: "Orchestrator purity — Impetus does not perform dev/eval/test/validation (Decision 3d)." This is also enforced by the `architecture-guard` skill which detects pattern drift against architecture decisions during sprint review.

**ECC** [OFFICIAL]: Tree scan — `orchestrator-purity: 0 matches`, `pattern-drift: 0 matches`. ECC has agents and skills but no published rule prohibiting orchestrator skills from doing direct work. The closest: `AGENTS.md` line "Use agents proactively without user prompt" suggests delegation, but this is a recommendation, not an enforced invariant. No skill audits skill compliance against an architecture rule.

**Verdict**: Momentum capability with no ECC analogue. ECC has `skill-stocktake` (audits skills against quality checklist) but not against architecture invariants.

---

## 11. Architecture-Guard / Pattern Drift Detection

**Momentum** [OFFICIAL]: `skills/momentum/skills/architecture-guard/SKILL.md` — read-only enforcer. Reads `_bmad-output/planning-artifacts/architecture.md`, extracts numbered decisions, runs `git diff main...sprint/{slug}`, checks each change against decisions, produces severity-ranked findings (CRITICAL/HIGH/MEDIUM/LOW). Specific decisions enforced: Decision 26 (two-layer agent model), Decision 30 (dev/spec separation), Decision 35 (skills/agents boundary, context:fork). Verdict logic: PASS unless any CRITICAL or 3+ HIGH.

**ECC** [OFFICIAL]: ECC has many code-quality and review skills (`code-reviewer`, `architect`, `repo-scan`, `skill-stocktake`), but tree scan confirms no `architecture-guard`, no `pattern-drift`, no skill that ingests an architecture doc and checks diffs against numbered decisions. The `architect` agent designs new architecture rather than enforcing existing decisions on diffs.

**Verdict**: Momentum capability with no direct ECC analogue.

---

## 12. Practice Pedagogy

**Momentum** [PRAC]: This is a discrete claim. `CLAUDE.md` opens "Momentum provides the practice layer for agentic engineering: global rules, agents, hooks, and workflows that enforce quality standards across all projects." `docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md` is "The practice plan." Memory file `feedback_follow_workflow_exactly.md`: "When a workflow says spawn agents/skills, do that — no shortcuts." Memory file `feedback_impetus_orchestration_model.md`: "Impetus ALWAYS spawns all subagents directly. No direct-invocation workarounds. Exclusive write authority per file." These read as a practice being trained into the developer/agent system.

**ECC** [OFFICIAL]: `SOUL.md` declares "Core Principles: Agent-First, Test-Driven, Security-First, Immutability, Plan Before Execute" — five principles, framed as an identity. `RULES.md` has Must-Always / Must-Never lists. README markets ECC as "The performance optimization system for AI agent harnesses... a complete system: skills, instincts, memory optimization, continuous learning, security scanning." External guides exist (Shorthand/Longform/Security guides linked from README, not in repo).

**Verdict**: ECC has more polish on identity/marketing (SOUL.md, multilingual docs, badges, hackathon-winner branding). Momentum has a tighter, more enforceable practice with specific feedback-driven invariants ("never use SDR/ASR acronyms," "spikes must be standard stories"). ECC teaches a toolkit; Momentum trains a practice. Different shapes — neither strictly superior — but Momentum's practice has more behavioral specificity per kilobyte of doc.

---

## 13. Workflow.md vs SKILL.md Two-File Pattern

**Momentum** [OFFICIAL]: Verified — every Momentum skill that has substantive logic uses the SKILL.md+workflow.md split. `skills/momentum/skills/sprint-manager/SKILL.md` is 9 lines of frontmatter pointing to `./workflow.md` (149 lines of actual procedure). Same pattern in sprint-planning, retro, decision, intake, plan-audit, create-story, distill, dev, etc. The split lets the SKILL.md frontmatter be discovered without loading the full procedure into the trigger context.

**ECC** [OFFICIAL]: Tree scan — `workflow.md: 20 matches` total across 2,662 entries. **Zero of those 20 are in `skills/`.** They are all under `.cursor/rules/`, `.kiro/steering/`, `commands/multi-workflow.md`, etc. — i.e., ECC uses `workflow.md` as a name for cross-harness rule files, not as a skill-internal split. Of 16 ECC skills with multiple files, none use the SKILL.md+workflow.md two-file pattern. Multi-file skills like `continuous-learning-v2` use `agents/`, `hooks/`, `scripts/`, `config.json` instead.

**Verdict**: Momentum capability with no ECC analogue. The pattern is a Momentum/BMAD convention. Whether it is materially better than ECC's flat-SKILL.md approach depends on skill complexity — for skills with 100+ line procedures, the split keeps frontmatter scannable.

---

## 14. EDD (Evaluation-Driven Development) for Skills

**Momentum** [OFFICIAL]: `skills/momentum/skills/create-story/workflow.md` requires that any `skill-instruction` task get EDD treatment: "write 3 behavioral evals before touching skill files." Verified in real sprint data — `sprints/index.json` shows `sprint-2026-04-04` with `team_composition.avfl-scan-profile.test_approach: "EDD — 3 evals: scan no-fix-loop, structured output format, existing profiles unchanged"`. EDD evals are treated as the unit-test analogue for prompt-as-code.

**ECC** [OFFICIAL]: `skills/eval-harness/SKILL.md` — a formal EDD framework with capability evals, regression evals, code-based / model-based / human graders, pass@k and pass^k metrics. **This is a real analogue and is technically very thorough**. Plus `skills/agent-eval/SKILL.md` — head-to-head agent comparison with YAML task definitions, git worktree isolation, and pass-rate/cost/time/consistency metrics. Plus `skills/agentic-engineering/SKILL.md` declares "eval-first execution" as a core principle.

**Verdict**: ECC has more EDD machinery than Momentum (eval-harness, agent-eval, the EDD-as-philosophy framing in agentic-engineering). Momentum **applies** EDD as a per-story discipline injected into Dev Notes; ECC **describes** EDD as a methodology with reusable harness. Different layers. **ECC arguably exceeds Momentum on the framework; Momentum arguably exceeds ECC on workflow integration.** Tied or slightly ECC-favored.

---

## 15. Sprint Review with Auditor Team (Retro Skill)

**Momentum** [OFFICIAL]: `skills/momentum/skills/retro/SKILL.md` description: "Sprint retrospective — transcript audit via DuckDB, story verification, auditor team analysis, findings document, and sprint closure." Per memory `feedback_avfl_post_merge_strategy.md`: "Run one AVFL pass after ALL stories are merged; keep worktrees alive until clean, then bulk remove." Verified in real data: `sprints/index.json` has `retro_run_at` field on completed sprints; `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-14/` contains `retro-transcript-audit.md`, `audit-extracts/`, and `sprint-summary.md`. Findings emit into `intake-queue.jsonl` for next-sprint consumption.

**ECC** [OFFICIAL]: Tree scan — `retro: 0 matches`. There is no post-sprint review concept in ECC because there are no sprints. The `harness-audit` command audits the harness configuration, not a unit of completed work. `repo-scan` and `code-tour` skills exist but they are not retrospective on a delivered increment.

**Verdict**: Momentum capability with no ECC analogue.

---

## Summary Scorecard

| Capability | Momentum | ECC | Winner |
|---|---|---|---|
| 1. Multi-agent adversarial validation framework | AVFL: 4 lenses × 2 framings × 4 profiles, benchmarked roles | santa-method: 2 reviewers, binary, no profiles; verification-loop: single-agent | Momentum |
| 2. Gherkin/ATDD specs | Yes (.feature per story, Outsider Test) | None | Momentum |
| 3. Sprint state machine + sole-writer | Yes (stories/index.json, sprints/index.json, sprint-manager) | None | Momentum |
| 4. Change-type classification on stories | 5 types + injected guidance | None | Momentum |
| 5. Intake event log (jsonl) | Yes (intake-queue.jsonl with rich event schema) | None (only test fixtures) | Momentum |
| 6. Decision documents | momentum:decision (assessment-integrated) | architecture-decision-records, council | Tied |
| 7. Epic/feature taxonomy grooming | feature-grooming, epic-grooming, feature-breakdown, feature-status | None | Momentum |
| 8. Plan-mode hook gate | Spec Impact gate via plan-audit rule + skill | GateGuard fact-force (different purpose) | Tied |
| 9. Typed multi-conversation memory | Typed (feedback_/project_/reference_) auto-memory | continuous-learning-v2 with confidence scoring + automation | ECC slightly |
| 10. Orchestrator purity / skill discipline | Architecture-guard enforces, memory-trained | None (skill-stocktake audits quality, not architecture) | Momentum |
| 11. Architecture-guard / pattern drift | Yes (reads architecture.md, diffs sprint, severity findings) | None | Momentum |
| 12. Practice pedagogy | Behavioral invariants in memory + rules | SOUL.md identity + RULES.md Must/MustNever | Different shapes |
| 13. SKILL.md + workflow.md split | Universal in Momentum skills | Zero use in ECC skills | Momentum |
| 14. EDD framework | Per-story EDD discipline | eval-harness, agent-eval, agentic-engineering principle | ECC slightly |
| 15. Post-sprint retro with auditor team | retro skill + transcript audit + auditor team | None | Momentum |

**Tally**: Momentum-clear-superior on 9; Tied on 2 (decision documents, plan-audit hook gate); ECC-slightly-superior on 2 (memory automation, EDD framework); Different shape on 1 (practice pedagogy); Momentum-superior-on-pattern-but-not-on-substance on 1 (workflow.md split).

---

## Where ECC is Materially Stronger Than Momentum (Honest Counter-Findings)

To not steelman Momentum unfairly:

- **Breadth**: ECC has 156+ skills covering language ecosystems (Java, Kotlin, Rust, C++, PyTorch, Swift, Perl, Dart/Flutter), domain ops (healthcare, finance, logistics, energy, customs), media (manim, remotion, video editing), and security (AgentShield, security-bounty-hunter, defi-amm-security). Momentum has 25 skills, all about practice. Different scope.
- **Distribution**: ECC ships an npm package (`ecc-universal`), a GitHub Marketplace App (`ecc-tools`), a Tkinter desktop dashboard (`ecc_dashboard.py`), a Rust control-plane prototype (`ecc2/`), a Codex CLI installer, and translations into 7 languages. Momentum has a `plugin.json` and a marketplace install. ECC is a polished product; Momentum is internal-tooling for a single developer.
- **Cross-harness portability**: ECC explicitly targets Claude Code, Codex, Cursor, OpenCode, Gemini, Antigravity, Trae, Kiro, CodeBuddy. Verified via top-level dirs `.codex/`, `.cursor/`, `.opencode/`, `.gemini/`, `.kiro/`, `.trae/`, `.codebuddy/`, plus `.codex-plugin/`. Momentum is Claude-Code-only.
- **Hook sophistication**: `hooks/hooks.json` has GateGuard (DENY/FORCE/ALLOW with A/B test data), continuous-learning-v2 observation hook (project-aware), MCP health check, governance capture (secrets, policy violations), config protection (block linter config edits), doc file warning, post-edit accumulator with batched format+typecheck at Stop time, design-quality-check (warns on generic UI), console-warn detection. Momentum's hooks are simpler.
- **Continuous-learning v2.1**: project-scoped instincts with hashed git-remote IDs, automatic promotion to global on cross-project occurrence, confidence scoring, evolution into skills/commands/agents — Momentum has nothing equivalent for automated pattern extraction.
- **Council deliberation skill**: explicit four-voice (Architect/Skeptic/Pragmatist/Critic) decision council with anti-anchoring discipline (subagents launched without conversation history). Momentum has no analogue for ambiguous decision deliberation.
- **Loop patterns documentation**: `skills/autonomous-loops/SKILL.md` and `skills/continuous-agent-loop` document six loop architectures (sequential pipeline, NanoClaw REPL, infinite agentic loop, continuous Claude PR loop, de-sloppify, Ralphinho RFC DAG) with implementation snippets. Momentum has sprint-dev as one specific orchestration; no patterns library.
- **Agent-eval head-to-head benchmark**: `skills/agent-eval/SKILL.md` lets you compare Claude Code vs Aider vs Codex on YAML-defined tasks with reproducible commit pinning. Nothing in Momentum compares agents this way.
- **NanoClaw REPL** and **PM2 multi-service orchestration**: ECC has utilities for persistent session REPL and multi-service process management. Momentum delegates to cmux for these.

---

## Net Assessment

ECC and Momentum are aimed at different problems and largely do not compete:

- **ECC** is a horizontal toolkit: "make the agent harness perform better, regardless of what you are building." Skills are sized by domain (Kotlin testing, healthcare PHI compliance, content engine). Hooks are sized by tool type (PreToolUse, PostToolUse). The unit of value is "I get a better skill catalog and safer hooks."
- **Momentum** is a vertical practice: "execute one solo developer's agentic engineering practice with planned sprints, validated specs, AVFL'd outputs, retro'd findings, and decision-documented strategy." Skills are sized by practice phase (sprint-planning, dev, retro, decision). Hooks are sized by gate point (plan-audit). The unit of value is "I run a disciplined cadence."

If you removed Momentum's sprint-state-machine, AVFL, Gherkin specs, change-type classification, intake queue, plan-audit gate, retro auditor team, and architecture-guard, you would have a smaller and worse toolkit than ECC. **Momentum's superiority is in the practice machinery — the things that turn a session-by-session toolkit into a multi-week disciplined cadence.** That machinery does not exist in ECC.

Conversely, if you took Momentum and tried to use it for "I want to write better Kotlin for an Android app," you would find no value — Momentum has no language-specific guidance, no Kotlin testing patterns, no Compose Multiplatform support. ECC's `kotlin-patterns`, `kotlin-testing`, `kotlin-reviewer`, `kotlin-build-resolver` would all serve you immediately.

Both could coexist. ECC's claim to be "the performance system for AI agent harnesses" is honest within scope; Momentum's claim to provide "the practice layer for agentic engineering" is honest within a disjoint scope.

---

## Sources

ECC sources (all read directly via `gh api`, scan date 2026-04-26):

- `https://github.com/affaan-m/everything-claude-code` (repo metadata, version 1.10.0, 167K stars)
- `gh api repos/affaan-m/everything-claude-code/git/trees/main?recursive=1` (2,662 path entries scanned)
- `https://github.com/affaan-m/everything-claude-code/blob/main/README.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/AGENTS.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/SOUL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/RULES.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/hooks/hooks.json`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/santa-method/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/verification-loop/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/eval-harness/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/agent-eval/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/agentic-engineering/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/agent-harness-construction/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/architecture-decision-records/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/council/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/continuous-learning-v2/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/autonomous-loops/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/blueprint/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/iterative-retrieval/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/ralphinho-rfc-pipeline/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/dmux-workflows/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/skill-stocktake/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/gateguard/SKILL.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/commands/feature-dev.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/commands/loop-start.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/commands/prp-prd.md`

Momentum sources (all read directly from `/Users/steve/projects/momentum/`):

- `/Users/steve/projects/momentum/skills/momentum/.claude-plugin/plugin.json` (version 0.17.0)
- `/Users/steve/projects/momentum/CLAUDE.md`
- `/Users/steve/projects/momentum/.claude/rules/plan-audit.md`
- `/Users/steve/projects/momentum/.claude/rules/workflow-fidelity.md`
- `/Users/steve/projects/momentum/.claude/rules/version-on-release.md`
- `/Users/steve/projects/momentum/.claude/rules/dev-skills.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/avfl/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-manager/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-manager/workflow.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/workflow.md` (sampled via grep)
- `/Users/steve/projects/momentum/skills/momentum/skills/retro/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/decision/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/intake/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/plan-audit/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/create-story/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/create-story/workflow.md` (sampled via grep)
- `/Users/steve/projects/momentum/skills/momentum/skills/architecture-guard/SKILL.md`
- `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/index.json`
- `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/index.json`
- `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-14/` (directory listing: specs/, retro-transcript-audit.md, audit-extracts/, sprint-summary.md)
- `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-14/specs/triage-skill.feature` (verified present)
- `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/intake-queue.jsonl` (sampled events)
- `/Users/steve/.claude/projects/-Users-steve-projects-momentum/memory/MEMORY.md` (memory index)
- `/Users/steve/.claude/projects/-Users-steve-projects-momentum/memory/feedback_*.md` (18 typed feedback files)
