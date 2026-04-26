---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Design philosophy comparison — ECC vs Momentum"
topic: "everything-claude-code vs Momentum — comparative analysis"
---

# Design Philosophy Comparison — ECC vs Momentum

## Inline Summary

Everything Claude Code (ECC) is a **toolkit-and-distribution platform** — a cross-harness "agent harness performance optimization system" (140K+ stars, MIT-licensed, 38–48 agents and 156–183 skills) whose central premise is that Claude Code (and Codex/Cursor/OpenCode) are underperforming defaults that any developer can drastically upgrade by installing battle-tested skills, hooks, rules, and MCP configs. Momentum is an **opinionated solo-author practice framework** — a small, philosophy-led module (≈25 skills, Apache-2.0, low star count) that argues AI-assisted engineering needs a producer/verifier separation, an authority hierarchy of Spec > Test > Code, an Adversarial Validate-Fix Loop, and a flywheel that traces failures upstream to the rule, workflow, or spec that caused them. The central tension is **breadth vs. depth**: ECC optimizes the marginal session ("ship more, ship faster, with security and learning"), Momentum optimizes the practice ("never review your own AI-generated code; trace every failure to a fixable upstream cause"). [OFFICIAL]

---

## 1. Toolkit vs Practice

**ECC** is unambiguously a toolkit. The README's opening line frames it as an inventory: "The performance optimization system for AI agent harnesses." [OFFICIAL] It boasts "48 agents, 183 skills, and 79 legacy command shims" and immediately offers a dashboard GUI to browse them. [OFFICIAL] The pitch is breadth — "12+ language ecosystems," "Production-ready agents, skills, hooks, rules, MCP configurations" — and the implicit invitation is *use what you want*. ECC's CLAUDE.md describes itself as "a collection of production-ready agents, skills, hooks, commands, rules, and MCP configurations." [OFFICIAL] Profiles (`core`, `developer`, `security`, `research`, `full`) exist to help users pick a subset, not to enforce one.

**Momentum** is unambiguously a practice. Its tagline: "A practice framework for agentic engineering. Momentum is a philosophy and process for building software with AI agents as primary code producers." [OFFICIAL] The README states that Momentum "is currently implemented using BMAD Method and Claude Code, but the principles and process are tool-agnostic." [OFFICIAL] Momentum even ships a *Tier 3 — Philosophy Only — No Tooling* mode: "Momentum's principles are designed to be valuable without any tooling. A developer or team can adopt the practice by reading the documentation." [OFFICIAL] The skills exist to enforce the practice; the practice does not exist to host the skills.

**Contrast.** ECC says: *here are tools, pick what helps.* Momentum says: *here is how you must work; the tools just enforce it.* ECC's list of components is the product; Momentum's list of principles is the product.

---

## 2. Governance Model

**ECC** is a **community-extended single-maintainer** project. Affaan Mustafa is the BDFL and author; the contribution model is open: "The ECC OSS repo is MIT-licensed and contributions are welcome. Fork the repository, add your skill or agent following the existing format, and open a pull request." [OFFICIAL] CONTRIBUTING.md actively solicits new agents, framework experts, DevOps specialists, and language reviewers. [OFFICIAL] As of v1.10.0 the catalog explicitly thanks "30+ community PRs merged — Contributions from 30 contributors across 6 languages" and "Korean and Chinese translations." [OFFICIAL] Recent commits include community PRs (`#1546`, `#1511`, `#1522`) directly to `main`. [OFFICIAL]

**Momentum** is a **single-author closed practice** at this stage. The README states: "Momentum is in early development. The philosophy and process are defined. Implementation of the core practice layer (quality rules, verification agents, install workflow) is in progress." [OFFICIAL] No CONTRIBUTING.md exists. The project is `iamsteveholmes/momentum` and ships with `.claude/rules/version-on-release.md` describing a personal release cadence: "When a sprint completes and merges to main: bump `skills/momentum/.claude-plugin/plugin.json` version." [PRAC] The git log shows a single author, and the `momentum-master-plan.md` is described as "Authoritative for: model, status, architecture decisions, and roadmap." [OFFICIAL]

**Contrast.** ECC is a marketplace; Momentum is a manifesto. ECC's success is measured by PR throughput; Momentum's by whether the practice produces better outcomes for one developer.

---

## 3. Opinionatedness

**ECC** is *modestly* opinionated. Its `RULES.md` enforces some non-negotiables — "Delegate to specialized agents for domain tasks. Write tests before implementation and verify critical paths." [OFFICIAL] — and a "Must Never" list ("Submit untested changes. Bypass security checks or validation hooks."). [OFFICIAL] But everything below this baseline is opt-in: 12 language ecosystems, 5 install profiles, four cross-harness adapters, multiple MCPs that can be disabled with `ECC_DISABLED_MCPS`. [OFFICIAL] The Shorthand Guide explicitly tells users: "Be picky with MCPs. I keep all MCPs in user config but disable everything unused." [OFFICIAL]

**Momentum** is *aggressively* opinionated. The README's "Authority Hierarchy" reads: "Specifications > Tests > Code. Agents never modify specifications or pre-existing tests to make code pass." [OFFICIAL] Producer-Verifier Separation reads: "The agent that writes code does not review it. Verification happens in a separate context with a separate agent whose only job is to find problems." [OFFICIAL] These are not configurable knobs; they are framed as load-bearing rules. The project ships an `architecture-guard` skill ("Detects pattern drift against architecture decisions. Read-only enforcer.") [OFFICIAL] and a `plan-audit` rule that *blocks* `ExitPlanMode` until a `## Spec Impact` section appears. [OFFICIAL]

**Contrast.** ECC sets a floor and lets users build up. Momentum sets a ceiling and enforces compliance.

---

## 4. Target User

**ECC** targets a broad professional audience. From `ecc.tools`: "Thousands of developers and engineers across various Fortune 500 teams." [OFFICIAL] The README's stats — "140K+ stars | 21K+ forks | 170+ contributors | 12+ language ecosystems" — and the language ecosystem coverage (TypeScript, Python, Go, Java, Kotlin, C++, Rust, Perl, PHP, Swift, Django, Laravel, Spring Boot) imply a general-purpose tool aimed at any working developer using Claude Code. [OFFICIAL] The GitHub App offers freemium/pro/enterprise tiers, indicating commercial team usage as a target. [OFFICIAL]

**Momentum** targets a narrower archetype: the **solo developer directing AI agents on a single complex codebase**. Its canonical planning artifact is titled "AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md" [OFFICIAL] and the README explicitly says "The principles apply whether you're a solo developer or a team — anyone directing AI agents to produce code faces the same quality challenges." [OFFICIAL] The Impetus orchestrator persona — "field commander meeting your operator for the first time" with "PERSONA.md / BOND.md / CREED.md" sanctum files — assumes a single human owner. [OFFICIAL] Memory file `feedback_quickfix_epic_ad_hoc.md` codifies single-developer ergonomics ("don't ask the developer"). [PRAC]

**Contrast.** ECC scales out (more languages, more frameworks, more contributors). Momentum scales depth (one practice, deeply enforced for one person).

---

## 5. Pedagogy

**ECC** teaches through a **guides-on-the-side** model. The README points to three guides hosted as image-rich Twitter/X threads: "**Shorthand Guide** — Setup, foundations, philosophy. **Read this first.**" then "**Longform Guide** — Token optimization, memory persistence, evals, parallelization." then "**Security Guide**." [OFFICIAL] The repo itself acknowledges "This repo is the raw code only. The guides explain everything." [OFFICIAL] Pedagogy is recommendatory and tip-driven: "Pro tip: Use the `hookify` plugin to create hooks conversationally instead of writing JSON manually." [OFFICIAL]

**Momentum** teaches through **first-principles documentation embedded in the artifact**. The README runs ~400 lines of prose, mermaid diagrams, and citations covering 10 named principles, 5 debt taxonomies, and a Quality Model. It cites academic and industry research — "Research: METR 2025 39-point perception gap; ASCoT 2025; Meta-Judge 2025" — directly inside skill prompts. [OFFICIAL] The AVFL skill explains its own grounding: "dual reviewers with different framings improve accuracy ~8 percentage points absolute over single-agent validation (Meta-Judge 2025). Late-stage errors are 3.5× more damaging than early ones." [OFFICIAL] The Impetus skill teaches via metaphor and law: "The weight of Optimus Prime's conviction meets KITT's attentive service" plus "The Three Laws." [OFFICIAL]

**Contrast.** ECC says "here is what works in practice — try it." Momentum says "here is the *theory* of why this must be done — and the rules that follow."

---

## 6. AI-Agent Treatment

**ECC** treats agents as **specialized workers** to be dispatched. SOUL.md: "Agent-First — route work to the right specialist as early as possible." [OFFICIAL] CLAUDE.md: "Subagents handle delegated tasks with limited scope." [OFFICIAL] Agents are discrete units (`planner.md`, `architect.md`, `tdd-guide.md`, `code-reviewer.md`, `security-reviewer.md`, etc.) with explicit `tools`, `model`, and frontmatter. The metaphor is *team of consultants*. The trust model is *trust the specialist for their domain*; quality emerges from picking the right one.

**Momentum** treats agents as **suspect producers requiring adversarial verification**. The README is explicit: "The agent that writes code does not review it. Verification happens in a separate context with a separate agent whose only job is to find problems. Verifiers produce findings — they never modify code." [OFFICIAL] Agents are also given *deep persona and continuity* — Impetus has a "sanctum" of identity files, a creed, and "Three Laws." [OFFICIAL] Memory file `feedback_impetus_orchestration_model.md` enforces the orchestration shape: "Impetus ALWAYS spawns all subagents directly. No direct-invocation workarounds. Exclusive write authority per file." [PRAC]

**Contrast.** ECC's mental model: *agents are skilled hires; manage them.* Momentum's mental model: *agents are unreliable producers; structure the work so their output is independently verified, by another agent, in a fresh context.*

---

## 7. Validation Philosophy

**ECC** assumes agents are **mostly reliable**, with safety nets. RULES.md mandates "Write tests before implementation and verify critical paths" and notes a "minimum 80% test coverage" expectation. [OFFICIAL] The `verification-loop`, `eval-harness`, and `checkpoint` skills exist for high-stakes flows. [OFFICIAL] AgentShield is positioned for security: "1282 tests, 102 rules" with an `--opus` flag that "runs three Claude Opus 4.6 agents in a red-team/blue-team/auditor pipeline." [OFFICIAL] But these are opt-in, situational tools.

**Momentum** assumes agents are **structurally unreliable** by default. The README declares an entire debt taxonomy specifically for this: "Verification Debt — Unreviewed or inadequately tested AI-generated output accumulates faster than human-written code because generation is cheap. Layered verification (acceptance tests, unit tests, adversarial review, human review) counteracts this." [OFFICIAL] The AVFL skill encodes empirical calibration into its defaults: "Do not use Haiku for Enumerator validators. Benchmarking showed Haiku enum-medium produces false-pass scores (92/100 while missing a critical architectural contradiction)." [OFFICIAL] Validation is a parallel, multi-lens, dual-reviewer pipeline ("8 subagents total — 1 Enumerator + 1 Adversary per lens × 4 lenses") that runs *every* sprint, not optionally. [OFFICIAL]

**Contrast.** ECC's validation is a **safety net** invoked when the developer chooses. Momentum's validation is a **load-bearing wall** that runs on a schedule whether the developer asks or not.

---

## 8. Memory and Learning

**ECC** has a feature called **Continuous Learning v2 (Instincts)** — the README describes it as: "instinct-based system automatically extracts and clusters learned patterns into reusable skills through `/instinct-status`, `/instinct-import`, `/instinct-export`, and `/evolve` commands." [OFFICIAL] The mechanism is mechanical: a Stop hook extracts patterns, scores them with confidence, and `/evolve` clusters instincts into new SKILL.md files. The Longform Guide promises "Auto-extract patterns from sessions into reusable skills." [OFFICIAL] Instincts are also *shareable* — exportable artifacts.

**Momentum** has a richer, multi-tier learning loop centered on the **Evaluation Flywheel**. README: "When output fails quality standards, trace the failure upstream via navigable `derives_from` chains. Don't just fix the code — fix the workflow, specification, or rule that caused the defect." [OFFICIAL] Concretely: AVFL findings → retro skill → triage skill (six-class observation taxonomy) → distill skill ("immediately applies a session learning or retro Tier 1 finding to the appropriate rule, reference, or skill prompt") or `decision` skill ("Capture strategic decisions… write a linked SDR document"). [OFFICIAL] Impetus has a per-session sanctum (`PERSONA.md`, `MEMORY.md`, `BOND.md`, `CREED.md`) that records identity and bond evolution. [OFFICIAL] Memory file `project_momentum_redesign.md` references "intake-queue.jsonl event log" as the durable learning substrate. [PRAC]

**Contrast.** ECC learns *patterns of doing*. Momentum learns *causes of failure* and edits the practice itself. ECC's instincts → new skills; Momentum's findings → upstream fixes to existing rules and workflows.

---

## 9. Distribution Model

**ECC** distributes via **multiple parallel channels**. (1) Claude Code plugin marketplace: "`/plugin marketplace add https://github.com/affaan-m/everything-claude-code`." [OFFICIAL] (2) npm packages: `ecc-universal` and `ecc-agentshield`. [OFFICIAL] (3) Manual copy: "Copy agents to your Claude config / cp everything-claude-code/agents/*.md ~/.claude/agents/." [OFFICIAL] (4) GitHub App for repo-native integration ("ecc-tools," 150 installs). [OFFICIAL] (5) Cross-harness adapters for Cursor, OpenCode, Codex, Antigravity. [OFFICIAL] (6) Dashboard GUI (`ecc_dashboard.py` Tkinter app). [OFFICIAL] The naming-and-migration note acknowledges this multiplicity: "ECC now has three public identifiers, and they are not interchangeable." [OFFICIAL]

**Momentum** distributes via a **single, narrow channel** with tiered fallback. README: "`npx skills add https://github.com/iamsteveholmes/momentum --all`" then "`/momentum`" with three tiers: **Tier 1: Claude Code** (full enforcement), **Tier 2: Cursor and other tools** (advisory — "Hooks (no automatic linting, formatting, or file protection); Global rules (no `~/.claude/rules/` auto-loading)"), **Tier 3: Philosophy Only — No Tooling** ("Momentum's principles are designed to be valuable without any tooling"). [OFFICIAL] The reference user-memory note explicitly states: "momentum install shell script is obsolete — use standard Agent Skills installation." [PRAC]

**Contrast.** ECC distributes *as widely as possible* across every harness and surface. Momentum distributes *deeply for one harness*, with graceful degradation as documentation for the rest.

---

## 10. Versioning and Stability

**ECC** moves fast and ships often. The release log shows roughly monthly minor versions (v1.6.0 Feb, v1.7.0 Feb, v1.8.0 Mar, v1.9.0 Mar, v1.10.0 Apr 2026), each with substantial surface changes — "Selective install architecture," "ECC 2.0 alpha is in-tree," "Public catalog truth is `47` agents, `79` commands, and `181` skills." [OFFICIAL] WORKING-CONTEXT.md acknowledges this churn: "Public plugin slug is now `ecc`; legacy `everything-claude-code` install paths remain supported for compatibility." [OFFICIAL] A "Naming + Migration Note" warns: "Older posts may still show the old short-form nickname; that shorthand is deprecated." [OFFICIAL] Issue history shows repeated regressions ("This has caused repeated fix/revert cycles in this repo"). [OFFICIAL]

**Momentum** has explicit versioning discipline tied to sprints. `.claude/rules/version-on-release.md`: "When a sprint completes and merges to main: 1. Bump `skills/momentum/.claude-plugin/plugin.json` version — Patch (0.x.Y) for bug fixes and minor improvements; Minor (0.X.0) for new features. 2. Commit: `chore(plugin): bump version to X.Y.Z`. 3. Push includes the version bump commit." [OFFICIAL] Commits show this in practice: "chore(plugin): bump version to 0.17.0 — Impetus memory agent rebuild." [PRAC] At v0.17, the project is pre-1.0 and the README acknowledges "Momentum is in early development." [OFFICIAL]

**Contrast.** ECC ships a stable-ish v1.x with frequent additive minor versions and the occasional rename. Momentum ships explicit pre-1.0 with sprint-aligned bumps and an upfront admission of instability.

---

## 11. Quality Bar

**ECC** has a **conventional quality bar**: tests, reviewers, security scans. RULES.md "Must Always: Write tests before implementation and verify critical paths." [OFFICIAL] The release notes report "997 internal tests passing — full suite green after hook/runtime refactor." [OFFICIAL] AgentShield handles security review. [OFFICIAL] Code reviewer agents per language exist. The bar is *normal-software-quality* applied to a plugin repo.

**Momentum** has a **research-grade quality bar** explicit to its practice. The AVFL skill is itself the quality gate, with prescribed roles ("Enumerator validator: sonnet/medium; Adversary validator: opus/high; Consolidator: haiku/low; Fixer: sonnet/medium") and grade thresholds ("≥95 Clean, ≥85 Good, ≥70 Fair, ≥50 Poor, <50 Failing"). [OFFICIAL] The retro skill produces findings; the upstream-fix skill "Traces quality failures upstream to spec, rule, or workflow root cause." [OFFICIAL] The README's anti-pattern list cites "Ox Security research" on "seven known AI code generation anti-patterns" and explicitly identifies "Spec Fatigue" as an empirical phenomenon with "vigilance decrement" research backing. [OFFICIAL]

**Contrast.** ECC: green tests + clean security scan = ship. Momentum: parallel multi-lens adversarial validation reaching a numeric pass score, plus a retro that traces every defect to its upstream cause.

---

## 12. Sprint Discipline

**ECC** has **no notion of sprints**. The README, CLAUDE.md, and CONTRIBUTING.md all describe continuous-flow development: PRs land on `main`, releases happen "monthly minor versions," and WORKING-CONTEXT.md tracks "Active Queues" rather than time-boxed sprints. [OFFICIAL]

**Momentum** is **sprint-disciplined to its core**. The redesign memory file: "new sprint/epic model, Impetus as pure orchestrator, sub-command skills, intake-queue.jsonl event log." [PRAC] The master plan defines: "Sprint = Unit of Work — N stories pulled from across epics… One active sprint at a time. Active sprint is **immutable** once activated. Planning sprint is fully mutable until activated." [OFFICIAL] Skills are aligned to sprint phases: `sprint-planning`, `sprint-dev`, `sprint-manager` ("Sole writer of stories/index.json and sprints/index.json"), and `retro` ("Sprint retrospective — transcript audit via DuckDB, story verification, auditor team analysis, findings document, and sprint closure"). [OFFICIAL]

**Contrast.** ECC is continuous flow. Momentum is rigorously time-boxed with hard immutability after activation.

---

## 13. Use of Behavioral Specs

**ECC** uses tests-as-spec. The TDD skill, `tdd-workflow`, and language-specific TDD variants (`django-tdd`, `springboot-tdd`, `laravel-tdd`, `golang-testing`, `python-testing`) cover this. [OFFICIAL] No Gherkin, no separate ATDD layer; the test suite *is* the spec. RULES.md: "Write tests before implementation and verify critical paths." [OFFICIAL]

**Momentum** uses Gherkin-style **acceptance specs separate from code-level tests**. The sprint-planning workflow distinguishes them clearly: "Story markdown files retain ONLY plain English ACs. Gherkin specs are written to `sprints/{sprint-slug}/specs/` and are exclusively for verifier agents. Dev agents never access that path." [OFFICIAL] The `feedback_gherkin_atdd_generality.md` memory codifies the rule: "Gherkin ATDD must stay behavioral/general. Specificity kills Gherkin value and couples tests to implementation." [PRAC] The README's authority hierarchy makes specs the topmost authority: "SPECIFICATIONS — Immutable source of truth, Human-written acceptance criteria." [OFFICIAL]

**Contrast.** ECC: tests are specs. Momentum: behavioral specs *govern* tests, which *govern* code, with strict information hiding (dev agents cannot read the verifier's Gherkin).

---

## 14. Origin Story

**ECC's origin** is a **personal optimization workflow that grew into a community project**. The Shorthand Guide opens: "Been an avid Claude Code user since the experimental rollout in Feb, and won the Anthropic x Forum Ventures hackathon with [zenith.chat](https://zenith.chat)… completely using Claude Code. Here's my complete setup after 10 months of daily use." [OFFICIAL] The project was created 2026-01-18 (per gh API metadata) and grew from "personal config dump" → "community catalog" → "cross-harness performance system" → "ECC 2.0 control plane / GitHub App / commercial tiers." [OFFICIAL] The animating problem: *Claude Code's defaults leave performance and security on the table; here is a battle-tested upgrade.*

**Momentum's origin** is a **research-led practice design** for AI-augmented engineering. The canonical planning artifact `AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md` and `momentum-master-plan.md` are dated March/April 2026, with research artifacts cited in the README ("Spec Fatigue Research… empirical evidence for specification review fatigue as a named anti-pattern"; "AI Engineering Maturity and Adoption"). [OFFICIAL] The animating problem statement is in the README: "[Momentum] defines how specifications govern code generation, how quality is enforced when AI writes the code, and how the practice itself improves over time." [OFFICIAL] The animating problem: *AI generates code faster than humans can verify it, so the practice itself must change to prevent compounding debt.*

**Contrast.** ECC was born from "what configs work for me, daily." Momentum was born from "what theory of practice survives once AI writes most of the code."

---

## Synthesis

Across all 14 dimensions, the same axis recurs:

| Axis | ECC pole | Momentum pole |
|---|---|---|
| Primary unit | Component (skill/agent/hook) | Principle (rule/workflow) |
| Optimization target | Marginal session | Long-run practice |
| Trust in AI | Mostly reliable specialists | Structurally unreliable producers |
| Quality model | Tests + reviewers + scanners | Adversarial multi-lens parallel validation + upstream traceback |
| Distribution | Maximum surface (every harness, every channel) | Minimum surface (one harness deeply, everything else as docs) |
| Pedagogy | Tips and external guides | First-principles prose with citations |
| Governance | Open community + BDFL | Closed solo author |
| Cadence | Continuous monthly minors | Time-boxed immutable sprints |
| Specs | Tests are specs | Behavioral specs govern tests govern code |
| Learning loop | Pattern extraction → new skills | Failure tracing → upstream rule edits |

ECC's design philosophy is, fundamentally, *amplification* — take the agent harness you have and make it dramatically more productive across every language and context you might encounter. Momentum's design philosophy is, fundamentally, *constraint* — accept that AI agents are unreliable producers and build a sustainable practice (separation of producer/verifier, adversarial validation, attention-aware checkpoints, upstream root-cause fixing) that survives that fact.

Both projects are coherent inside their own frame. Their core disagreement is whether the bottleneck of AI-assisted development is **what tools the agent has access to** (ECC) or **how the human-agent loop is structured to catch what the agent gets wrong** (Momentum).

---

## Sources

**ECC (everything-claude-code)**

- README.md — `gh api repos/affaan-m/everything-claude-code/contents/README.md` (verbatim, fetched 2026-04-26) [OFFICIAL]
- CLAUDE.md — `gh api repos/affaan-m/everything-claude-code/contents/CLAUDE.md` [OFFICIAL]
- RULES.md — `gh api repos/affaan-m/everything-claude-code/contents/RULES.md` [OFFICIAL]
- SOUL.md — `gh api repos/affaan-m/everything-claude-code/contents/SOUL.md` [OFFICIAL]
- WORKING-CONTEXT.md — `gh api repos/affaan-m/everything-claude-code/contents/WORKING-CONTEXT.md` (last updated 2026-04-08) [OFFICIAL]
- CONTRIBUTING.md — `gh api repos/affaan-m/everything-claude-code/contents/CONTRIBUTING.md` [OFFICIAL]
- REPO-ASSESSMENT.md — `gh api repos/affaan-m/everything-claude-code/contents/REPO-ASSESSMENT.md` (2026-03-21) [OFFICIAL]
- EVALUATION.md — `gh api repos/affaan-m/everything-claude-code/contents/EVALUATION.md` (2026-03-21) [OFFICIAL]
- the-shortform-guide.md — `gh api repos/affaan-m/everything-claude-code/contents/the-shortform-guide.md` [OFFICIAL]
- Repo metadata — `gh api repos/affaan-m/everything-claude-code` (167K stars, 26K forks, MIT, created 2026-01-18, default branch `main`) [OFFICIAL]
- Recent commits — `gh api repos/affaan-m/everything-claude-code/commits` (2026-04-26 snapshot) [OFFICIAL]
- ecc.tools homepage — `WebFetch https://ecc.tools` (2026-04-26) [OFFICIAL]

**Momentum (local repo)**

- /Users/steve/projects/momentum/README.md (philosophy section, principles list, three-tier enforcement) [OFFICIAL]
- /Users/steve/projects/momentum/CLAUDE.md (project instructions, structure) [OFFICIAL]
- /Users/steve/projects/momentum/.claude/rules/version-on-release.md [OFFICIAL]
- /Users/steve/projects/momentum/.claude/rules/plan-audit.md [OFFICIAL]
- /Users/steve/projects/momentum/.claude/rules/workflow-fidelity.md [OFFICIAL]
- /Users/steve/projects/momentum/skills/momentum/skills/impetus/SKILL.md [OFFICIAL]
- /Users/steve/projects/momentum/skills/momentum/skills/avfl/SKILL.md [OFFICIAL]
- /Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/SKILL.md (+ workflow.md) [OFFICIAL]
- /Users/steve/projects/momentum/skills/momentum/skills/retro/SKILL.md [OFFICIAL]
- /Users/steve/projects/momentum/_bmad-output/skills/impetus/references/first-breath.md [OFFICIAL]
- /Users/steve/projects/momentum/docs/planning-artifacts/momentum-master-plan.md (Last updated 2026-04-06) [OFFICIAL]
- /Users/steve/projects/momentum/docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md (referenced) [OFFICIAL]
- User-memory feedback files (private global memory, 2026-Q1/Q2): `feedback_impetus_orchestration_model.md`, `feedback_gherkin_atdd_generality.md`, `project_momentum_redesign.md`, `feedback_quickfix_epic_ad_hoc.md` [PRAC]
- Recent git log: `git log --oneline -5` showing v0.17.0 plugin bump, Impetus memory agent rebuild [PRAC]

**Tagging key**

- [OFFICIAL] — direct quote or paraphrase from a project's published README/docs/repo file
- [PRAC] — internal practice notes, memory files, or git history not in published docs but verifiable in the local repo
- [UNVERIFIED] — none used in this report; all citations are anchored to verifiable sources
