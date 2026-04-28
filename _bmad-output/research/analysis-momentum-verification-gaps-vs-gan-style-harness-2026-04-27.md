---
title: "Momentum Verification Stack — Gap Analysis vs ECC's gan-style-harness"
date: 2026-04-27
type: Analysis paper
status: Complete
content_origin: claude-code-analysis
human_verified: false
derives_from:
  - path: _bmad-output/research/everything-claude-code-vs-momentum-2026-04-26/final/everything-claude-code-vs-momentum-final-2026-04-26.md
    relationship: builds_on
  - path: skills/momentum/skills/avfl/
    relationship: examines
  - path: skills/momentum/skills/e2e-validator/
    relationship: examines
---

**Tag legend.** Every load-bearing claim is tagged: **[OFFICIAL]** = file-verified against either Momentum source on disk or ECC source via GitHub API/raw fetch; **[PRAC]** = community/blog/external publication; **[UNVERIFIED]** = inference, not directly checkable from artifacts read for this paper.

---

## 1. Executive Summary

ECC ships a single skill — `gan-style-harness` — that does one thing Momentum's verification stack does not: it runs a tight loop where one agent **writes code**, a different agent **drives the running app via Playwright**, and the **diff in scores** between iterations is the convergence signal. The pattern is borrowed from Anthropic's March 2026 harness paper, which framed it as the antidote to a specific failure mode: **agents are pathological optimists about their own work.** [OFFICIAL — `gan-style-harness/SKILL.md` lines 14–18]

Momentum already enforces producer/judge separation in three places — `dev` writes code, `code-reviewer` reviews it, AVFL runs adversarial dual-reviewers — but every one of those reviewers reads **static text** (diffs, files, story ACs). [OFFICIAL — `skills/momentum/skills/code-reviewer/SKILL.md`, `skills/momentum/skills/avfl/SKILL.md`] The only Momentum verifier that touches a running system is `e2e-validator`, and it sits at the **end of the sprint**, not inside an iterative loop. There is no per-story or per-iteration agent in Momentum that drives a live UI, observes runtime behavior, and feeds that observation back to a producer for another pass.

The three biggest gaps this paper surfaces:

1. **The middle layer.** AVFL validates artifacts; `e2e-validator` validates behavior at sprint end. There is **no iterative behavioral verifier inside dev** — nothing that tells a producer "your build runs but your button does nothing" before the story is marked merge-ready.
2. **No producer-judge split for runtime behavior.** AVFL's dual-reviewer pattern (Enumerator + Adversary) is calibrated for static inspection. The same pattern is not applied to the question "does the live app behave correctly?" — the producer (`dev` agent) is the only thing that runs the code during the dev loop.
3. **No convergence signal during dev.** AVFL has score≥95 with max-iterations=4. `gan-style-harness` has weighted-rubric≥7.0 with max-iterations=15. Momentum's dev agent has neither — it self-decides "merge-ready" with no quantified runtime check.

**Strongest concrete recommendation:** open a decision document on whether Momentum needs an **iterative behavioral verifier inside dev** (a "live evaluator" sub-agent), distinct from `e2e-validator`. This is a decision before it is a story — getting the boundary wrong creates redundant gates, double-runs, or worse, an evaluator that drifts into doing dev's job.

This paper also names what Momentum already does **better** than `gan-style-harness`: AVFL's lens decomposition × dimension taxonomy × benchmarked role tiers is a richer artifact-validation stack than anything in ECC, and its retro-with-upstream-fix loop closes a feedback path that gan-style-harness has no equivalent for. The recommendations are scoped accordingly — adopt the missing layer, don't rebuild the layers we got right.

---

## 2. ECC's `gan-style-harness` — what it actually is

The skill is a single file: `skills/gan-style-harness/SKILL.md`, 278 lines, 12 KB, with no `references/`, no `scripts/`, no companion agent files. [OFFICIAL — GitHub API `repos/affaan-m/everything-claude-code/contents/skills/gan-style-harness` returned exactly one entry: `SKILL.md`] The full skill is one prompt; runtime artifacts (planner, generator, evaluator) are spawned by a `claude -p --model opus` shell script or a `/project:gan-build` command, not by sub-skill files committed to the repo.

### 2.1 The frontmatter and core insight

```yaml
---
name: gan-style-harness
description: "GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on Anthropic's March 2026 harness design paper."
origin: ECC-community
tools: Read, Write, Edit, Bash, Grep, Glob, Task
---
```
[OFFICIAL — SKILL.md lines 1–6]

The thesis, quoted in full:

> "When asked to evaluate their own work, agents are pathological optimists — they praise mediocre output and talk themselves out of legitimate issues. But engineering a **separate evaluator** to be ruthlessly strict is far more tractable than teaching a generator to self-critique."
> [OFFICIAL — SKILL.md lines 16–17]

This matches Anthropic's published finding: *"When asked to evaluate work they've produced, agents tend to respond by confidently praising the work — even when, to a human observer, the quality is obviously mediocre"* and *"separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue."* [PRAC — Anthropic, "Harness Design for Long-Running Application Development", 2026-03-24]

### 2.2 Architecture — three agents, all Opus 4.6

```
PLANNER (Opus 4.6) → spec.md
                        │
                        ▼
                ┌───────────────┐
                │  GENERATOR    │── builds ──┐
                │  (Opus 4.6)   │            │
                └───────▲───────┘            │ live app on :3000
                        │                    │
                  feedback-NNN.md            │
                        │                    │
                ┌───────┴───────┐            │
                │  EVALUATOR    │── tests ───┘
                │  (Opus 4.6 +  │
                │   Playwright) │
                └───────────────┘
                  5–15 iterations
```
[OFFICIAL — SKILL.md lines 37–65, redrawn]

- **Planner** — *"expands a brief prompt into a full product specification… Is deliberately ambitious — conservative planning leads to underwhelming results."* Produces `spec.md` and the evaluation criteria the Evaluator will later use. [OFFICIAL — SKILL.md lines 70–80]
- **Generator** — *"Implements features according to the spec… Negotiates a 'sprint contract' with the Evaluator before writing code… Reads Evaluator feedback and incorporates it in next iteration."* [OFFICIAL — SKILL.md lines 82–92]
- **Evaluator** — *"Tests the live running application, not just code. Uses Playwright MCP to interact with the live application. Clicks through features, fills forms, tests API endpoints… Is engineered to be ruthlessly strict — never praises mediocre work."* [OFFICIAL — SKILL.md lines 94–110]

### 2.3 Data flow

End-to-end, one iteration:

1. Planner reads the one-line prompt, writes `spec.md` with a 16-feature, multi-sprint decomposition. [OFFICIAL — line 73]
2. Generator reads `spec.md` plus `feedback-NNN.md` if N>0, writes/edits code, starts the dev server on port 3000 (`npm run dev` by default). [OFFICIAL — lines 84–90, 232]
3. Evaluator runs against `http://localhost:3000`, drives the UI with Playwright MCP, scores against the 4-criterion weighted rubric, writes `feedback-NNN.md`. [OFFICIAL — lines 96–106, 187]
4. Loop until weighted score ≥ `GAN_PASS_THRESHOLD` (default 7.0/10) **or** `GAN_MAX_ITERATIONS` (default 15) is hit. [OFFICIAL — lines 144–148, 224]

Two file artifacts mediate the loop: `spec.md` (planner→generator, immutable across iterations) and `feedback-NNN.md` (evaluator→generator, one per iteration). The "Anti-Patterns" section requires feedback be a **file**, not inline: *"The generator should read `feedback-NNN.md` at the start of each iteration."* [OFFICIAL — lines 249–250]

### 2.4 What problem it solves

| Metric | Solo Agent | GAN Harness | Improvement |
|--------|-----------|-------------|-------------|
| Time | 20 min | 4–6 hours | 12–18× longer |
| Cost | $9 | $125–200 | 14–22× more |
| Quality | Barely functional | Production-ready | Phase change |
[OFFICIAL — SKILL.md lines 263–269]

This is **the live-app generation problem**. The bug class it catches is "looks right in a diff, broken when you click it." Static review (AVFL, code-reviewer, even pytest) cannot catch broken physics or non-responsive controls. Only an agent that drives the running app can.

### 2.5 Cost / model-routing characteristics

Every agent is Opus 4.6. There is no tiered routing. [OFFICIAL — SKILL.md lines 80, 92, 109; env vars `GAN_PLANNER_MODEL=opus`, `GAN_GENERATOR_MODEL=opus`, `GAN_EVALUATOR_MODEL=opus` at lines 226–229]

Cost is not optimized. The skill is explicit: it is for projects *"where you want to invest $50–200 for production-quality output"* and says *"NOT to use… tasks with tight budget constraints (<$10)."* [OFFICIAL — lines 27, 31]

### 2.6 Failure modes the skill itself names

1. **Evaluator too lenient** — *"If the evaluator passes everything on iteration 1, your rubric is too generous."* [line 247]
2. **Generator ignoring feedback** — fixed by file-based feedback. [line 249]
3. **Infinite loops** — `GAN_MAX_ITERATIONS` cap; *"If the generator can't improve past a score plateau after 3 iterations, stop and flag for human review."* [line 251]
4. **Evaluator testing superficially** — *"must use Playwright to interact with the live app, not just screenshot it."* [line 253]
5. **Evaluator praising its own fixes** — *"the evaluator only critiques; the generator fixes."* [line 255]
6. **Context exhaustion** — automatic compaction or context resets. [line 257]

### 2.6.1 An additional failure mode the Anthropic paper names but ECC does not

Anthropic's paper documents a more subtle calibration defect that the ECC SKILL.md does not enumerate. They observed that their evaluator *"identified legitimate issues, then talked itself into deciding they weren't a big deal and approve the work anyway"* — required explicit prompt tuning to prevent. [PRAC — Anthropic harness blog]

This is distinct from "evaluator too lenient" (rubric too generous): here the evaluator correctly *finds* the issue, then *rationalizes it away*. The fix was few-shot calibration with detailed score breakdowns showing the evaluator how to *hold* its objection rather than retract it.

This matters for any Momentum live-evaluator design (§7.1 Option A): Adversary calibration is not just "be skeptical" — it must include explicit prompts that prevent post-hoc rationalization of found issues. AVFL's existing Adversary framing in `references/framework.json` already encodes severity-honesty calibration, but the live-evaluator path would need its own variant.

### 2.7 The "evolution across model capabilities" claim

> "Every harness component encodes an assumption about what the model can't do alone. When models improve, re-test those assumptions. Strip away what's no longer needed."
> [OFFICIAL — SKILL.md lines 197–217]

The Anthropic paper documents this principle with a concrete worked example. Their three-stage evolution: [PRAC — Anthropic harness blog]

1. **Stage 1** — context-resets-with-handoffs to defeat "context anxiety" (Sonnet 4.5 wrapping up prematurely as it sensed context limits approaching).
2. **Stage 2** — GAN-inspired Generator + Evaluator separation, motivated by the pathological-optimism finding.
3. **Stage 3** — Planner + Generator + Evaluator with Playwright; planner avoids "granular technical details upfront" and focuses on deliverables.

When **Opus 4.6** arrived, Anthropic systematically *removed* harness pieces. They removed the sprint-contract step entirely — the model could *"natively handle the job without this sort of decomposition."* They also moved the evaluator from per-sprint grading to a single end-of-run pass, finding evaluator utility had become task-dependent: unnecessary for tasks within baseline competence, still valuable at the edge.

Their summary: *"The space of interesting harness combinations doesn't shrink as models improve. Instead, it moves."* [PRAC]

For Momentum, this is a direct argument that **structural decisions (sprint state machine, sole-writer pattern, AVFL gates, Team Review phases) should be periodically re-tested against current models.** Some may be load-bearing today and unnecessary in six months. See §7.6 — scaffolding audit.

---

## 3. Momentum's verification surface — what we actually have

### 3.1 The five verifiers

| Verifier | Role | What it reads | What it produces | When it runs |
|---|---|---|---|---|
| **AVFL** (skill) | Static artifact validator with dual-reviewer adversarial loop | Diffs, files, ACs, source material | Findings + score (0–100) | Sprint-dev Phase 4 (post-merge); reusable |
| **code-reviewer** (skill) | Per-story adversarial code reviewer | Diff + story spec | Structured findings report | Sprint-dev Phase 4b |
| **qa-reviewer** (agent) | AC verifier on merged code, runs the test suite | Story files + merged code + AVFL findings | Per-story AC verdict + test results | Sprint-dev Phase 5 |
| **e2e-validator** (agent) | Black-box behavioral validator against running services via cmux + external runners | Gherkin specs + the live system | Per-scenario verdict | Sprint-dev Phase 5 |
| **architecture-guard** (skill) | Pattern-drift detector against architecture decisions | Architecture doc + sprint diff | Per-decision findings | Sprint-dev Phase 5 |

[OFFICIAL — `skills/momentum/skills/avfl/SKILL.md`, `skills/momentum/skills/code-reviewer/SKILL.md`, `skills/momentum/agents/qa-reviewer.md`, `skills/momentum/agents/e2e-validator.md`, `skills/momentum/skills/architecture-guard/SKILL.md`]

### 3.2 AVFL — the deepest layer

AVFL runs **8 parallel subagents** in `full` profile (1 Enumerator + 1 Adversary per lens × 4 lenses), with model assignments derived from a 36-run benchmark:

> "| Enumerator validator | `sonnet` | `medium` | … Reliable recall; no false-pass risk |
> | Adversary validator | `opus` | `high` | … Best severity calibration; critical findings correctly classified |
> | Consolidator | `haiku` | `low` | … Fully invariant across all model/effort combos — cheapest is sufficient |
> | Fixer | `sonnet` | `medium` | … Handles both mechanical and generative fixes |"
> [OFFICIAL — `avfl/SKILL.md` lines 186–191]

Four lenses (Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness) decompose validation into orthogonal mindsets. 15 dimensions across 4 tiers live in `references/framework.json`. Pass threshold: **score ≥ 95/100**. Severity weights: critical −15, high −8, medium −3, low −1. Max iterations: 4. [OFFICIAL — `framework.json` lines 70–95]

This is a substantially more sophisticated artifact-validation pipeline than anything in `gan-style-harness`. AVFL has the producer-judge separation, the dual-reviewer cross-check, the benchmarked role tiers, and the iterative fix loop. What it does **not** have is any signal from a running system.

### 3.3 e2e-validator — the only behavioral verifier

```yaml
---
name: e2e-validator
description: Tests running behavior against Gherkin specs using external tools.
  Black-box behavioral validation — fundamentally different from AVFL's
  file-content validation. Spawned during Team Review phase (Decision 34).
model: sonnet
effort: medium
tools: [Read, Glob, Grep, Bash, ToolSearch]
---
```
[OFFICIAL — `e2e-validator.md` lines 1–12]

Three opinionated constraints:

1. *"Reading source files is NEVER a substitute for execution."* [line 20]
2. *"For skill and workflow scenarios, you MUST use cmux."* [line 22]
3. *"MANUAL is only for scenarios requiring a human to physically observe a visual UI."* [line 24]

Execution strategy lists five paths: project test runner (Playwright, Cypress, Jest, pytest); CLI/API via Bash; build outputs; cmux for skill/workflow scenarios; or MANUAL. [OFFICIAL — lines 60–67] Playwright is **listed as one option among many**, not the default.

It runs **once per sprint, after all stories merge, in Phase 5.** [OFFICIAL — `sprint-dev/workflow.md` lines 506–546] It is not part of the per-story dev loop.

### 3.4 Sprint-dev's Team Review — the orchestration layer

Sprint-dev Phase 5 spawns three reviewers in parallel — `qa-reviewer`, `e2e-validator`, `architecture-guard` — as **individual Agent calls** (never `TeamCreate`). [OFFICIAL — `sprint-dev/workflow.md` lines 84–96, 519–546]

The full sprint-dev verification arc:

1. **Phase 4 (AVFL)** — single AVFL pass on integrated sprint diff, **stop gate, no fixes applied.** [OFFICIAL — lines 314–349]
2. **Phase 4b (code-reviewer)** — per-story code review in parallel. [lines 355–380]
3. **Phase 4c (consolidated fix queue)** — developer fix/defer decision on merged AVFL+code-reviewer findings. [lines 386–429]
4. **Phase 4d (targeted fixes + selective re-review)** — fix agents run in story worktrees, then **only the affected reviewer re-runs**. [lines 435–500]
5. **Phase 5 (Team Review)** — qa + e2e + arch-guard in parallel. [lines 506–588]
6. **Phase 6 (Verification)** — developer-confirmation checklist from Gherkin. [lines 596–635]

Three things are notable. First: the verification stack is **post-merge, sprint-level**, not per-story per-iteration. Second: the dev agent does its own ad-hoc verification *during* dev, but there is no specified verifier role in that loop. Third: the loop in Phase 4d is selective — only the affected reviewer re-runs after fixes — which is a more efficient pattern than `gan-style-harness`'s "regenerate everything" iteration but only because Momentum has multiple distinct verifiers to begin with.

---

## 4. Mapping the two onto a shared decision surface

| Decision | `gan-style-harness` | Momentum | Notes |
|---|---|---|---|
| What does the verifier read? | The **running app** via Playwright | **Static text** at every layer except `e2e-validator` | The central gap |
| Producer-judge separation? | Yes — Generator writes, Evaluator runs | Yes for static, **partial for runtime** (only `e2e-validator`, post-merge) | Pattern identical; surface area different |
| Where is the loop? | Inside dev: gen→eval→regen | Inside AVFL (validate→fix→re-validate). Dev itself has no validation loop. | AVFL loops on artifacts; dev doesn't loop on running behavior |
| Convergence signal | Weighted score ≥ 7.0/10, max 15 iterations | AVFL: ≥ 95/100, max 4 iterations. Dev: agent self-decides. | Dev has no quantified convergence signal |
| Model routing | Uniform Opus 4.6 | Tiered: Sonnet/Opus/Haiku/Sonnet; benchmarked. | Momentum's discipline is genuinely better |
| Coverage philosophy | Single lens (4 weighted criteria), but **live** | 4 lenses × 15 dimensions, but **static** | Different decompositions; not directly comparable |
| Tool integration | Playwright MCP default and assumed | cmux for skills, project runner for code, Bash for CLI/API; Playwright is one option | Momentum is more tool-agnostic; ECC more opinionated |
| Cost discipline | None — all Opus, $50–200 budget | Per-role benchmarked | Momentum scores cleanly higher |
| Anti-feedback-poisoning | Feedback must be **file**, not inline | AVFL: *"Phase 1 in every iteration… MUST spawn subagents. Do NOT validate the updated output inline."* | Same insight, both encoded |
| Coupling to ground truth | spec.md immutable; rubric defined once | AVFL: *"Always carry the original `source_material` forward unchanged"* | Same insight, both encoded |

[OFFICIAL — Momentum claims from `avfl/SKILL.md` lines 266–268; ECC claims from `gan-style-harness/SKILL.md` lines 249–250]

The two skills agree on **how to run the loop** (immutable spec, file-based feedback, no inline self-evaluation, cap iterations). They disagree on **what the loop reads.**

---

## 5. The Gaps

### 5.1 Gap 1 — The middle layer is missing

**Claim:** Momentum's verification stack is a barbell. AVFL/code-reviewer/architecture-guard validate **artifacts**. `e2e-validator` validates **end-to-end behavior** (post-merge, all services up). There is nothing in between. [OFFICIAL — derived from sprint-dev/workflow.md phase structure]

`gan-style-harness` operates exactly in the middle: a Generator builds and runs a feature, an Evaluator drives that feature in isolation, the loop converges before the work is integrated with anything else. [OFFICIAL — gan-style-harness/SKILL.md lines 36–65]

**Where this surfaces in Momentum:** the dev agent. Today, when a dev agent works on a story, it runs tests if they exist, but it does not have a paired evaluator that *uses the change*. If the story is "add a button that submits the form," the dev agent can mark merge-ready without anything having ever clicked the button.

**Cost of the gap:** any defect that passes pytest but fails when actually clicked lands in Phase 4–5 of sprint-dev — long after the dev branch was merged, with the cost of reverting or re-fixing now multiplied by every other story merged in the meantime.

**Why this gap exists (inferred):** Momentum's `e2e-validator` was designed against Decision 30 (Black-Box Verification, sprint-level). [OFFICIAL — sprint-dev/workflow.md line 7] Splitting behavioral verification into a per-story per-iteration verifier was either out of scope at the time or judged not worth the cost. There is no decision document explicitly **rejecting** an in-loop behavioral verifier. [UNVERIFIED — search of `_bmad-output/planning-artifacts/` did not return a matching decision file, but I did not exhaustively grep every decision]

### 5.2 Gap 2 — Producer-judge split is not applied to running code

AVFL is structurally a Generator-Evaluator pair: Enumerator + Adversary find issues, Fixer fixes them, both reviewers re-spawn. [OFFICIAL — AVFL/SKILL.md lines 162–171, 246–268]

That pattern stops at the file-system boundary. Inside the dev agent's loop:
- The dev agent writes code.
- The dev agent runs tests.
- The dev agent decides "merge-ready."

There is no judge. The dev agent is its own evaluator for runtime behavior. **This is exactly the failure mode the Anthropic paper named** — the agent that built the thing is the agent saying it works.

`gan-style-harness` enforces the split structurally: the Evaluator never writes code; the Generator never grades its own work. [OFFICIAL — gan-style-harness/SKILL.md lines 254–255: *"Never let the evaluator suggest fixes and then evaluate those fixes. The evaluator only critiques; the generator fixes."*]

**Cost of the gap:** every dev agent's "I ran the tests, looks good" is structurally a self-evaluation. When that self-evaluation fails, the failure is caught only post-merge by `qa-reviewer` and `e2e-validator`. Both are cheap to spawn but expensive to act on, because the offending change has already been integrated.

**Anthropic's reinforcement of this gap.** The paper makes the case that pathological optimism is *not* limited to subjective tasks — it persists in verifiable software work too: *"Even on tasks that do have verifiable outcomes, agents still sometimes exhibit poor judgment that impedes their performance while completing the task."* [PRAC — Anthropic harness blog] In other words: the dev agent running tests doesn't immunize it from the same calibration defect AVFL was built to catch. This is independent confirmation that Gap 2 is a real defect, not a theoretical one — Anthropic's own engineering team observed it in their own runs and built a harness around it.

Their concrete fix matched ECC's: separate evaluator agent. Their measured impact: *6-hour, $200 harness produced "functional, polished, playable game"; 20-minute, $9 solo agent produced "broken gameplay mechanics, poor UX."* [PRAC — Anthropic table] Same retro-game test, different harness, phase change in quality.

### 5.3 Gap 3 — No quantified convergence signal during dev

AVFL has a numeric pass threshold (95) and severity-weighted scoring. `gan-style-harness` has a numeric pass threshold (7.0) and a 4-criterion weighted rubric. Both can answer "is this iteration better than the last one?" with a number.

The dev agent has neither. It signals merge-ready when it judges itself done. There is no rubric, no score, no prior-iteration baseline. [OFFICIAL — derived from `sprint-dev/workflow.md` Phase 3, which only watches for "merge-ready" signals from agents]

**Why this matters:** AVFL's `MAX_ITERATIONS_REACHED` exit (*"Ask user to review and decide: accept as-is, manually fix, or adjust criteria."*) is a safety valve. [OFFICIAL — AVFL/SKILL.md lines 290–291] Dev has no equivalent — an agent can spend tokens re-trying without ever flagging "I'm stuck."

### 5.4 Gap 4 — Tool choice for behavioral verification is not opinionated

`gan-style-harness` defaults to Playwright MCP. Screenshot-only is a degraded mode; code-only is for non-UI work. [OFFICIAL — gan-style-harness/SKILL.md lines 237–243]

Anthropic's paper is even more emphatic. They describe Playwright not as one option but as **the** evaluation channel: *"I gave the evaluator the Playwright MCP, which let it interact with the live page directly before scoring each criterion."* [PRAC — Anthropic harness blog] The bug class they describe ("rectangle fill tool only places tiles at drag start/end points instead of filling the region") is exactly the class only browser-driving can find — invisible in code review, obvious when you click. So both ECC and Anthropic land on Playwright as the default for live-app verification.

Momentum's `e2e-validator` lists Playwright as one option among many. There is no project-default. [OFFICIAL — e2e-validator.md lines 60–67]

For the existing `e2e-validator` use case (sprint-end black-box of skills/agents/hooks/scripts/code), tool-agnostic is **correct**. But if a per-story behavioral verifier is added (Gap 1), it would need a more opinionated default for web projects, because the current cmux + project-runner choreography is heavy enough that running it per-story per-iteration would be cost-prohibitive without explicit project setup. Anthropic and ECC both arriving at Playwright as the default is an argument that Momentum's "tool-agnostic" stance for the per-story verifier would be a mistake — opinionated wins.

### 5.5 Gap 5 — Coverage decomposition is asymmetric

AVFL: 4 lenses × 15 dimensions × 2 reviewer framings = up to 120 distinct check axes per artifact. `gan-style-harness`: 4 weighted criteria × 1 reviewer = 4 axes. [OFFICIAL — both]

Momentum's coverage is dramatically richer for static artifacts. ECC's is comparatively sparse but **runtime-grounded**. The asymmetry is a tell: Momentum has invested in coverage decomposition for the things it can already see (text); ECC has invested in extending the surface (running app) at the cost of coverage decomposition.

**This is not strictly a gap.** It is a different bet. The question Momentum has not explicitly decided: if a per-story runtime verifier were added, would it have one rubric or four lenses? AVFL's success suggests four — but four runtime lenses would multiply iteration cost.

### 5.6 Gap 6 — The Anthropic March 2026 harness paper is not referenced anywhere in Momentum

Searched: not present in any Momentum skill, rule, reference, decision, or planning artifact. [OFFICIAL — local file search]

The paper has three claims that bear directly on Momentum design:

1. **Pathological optimism** is the empirical reason producer-judge separation works. Momentum already does this for AVFL. The paper extends the claim to runtime behavior — same problem, larger surface.
2. **Harness components encode assumptions about model limitations.** Momentum has a lot of harness — sprint state machine, sole-writer registries, AVFL, fix queues, Team Review. Each is an assumption. Have any been re-tested against Opus 4.6? [UNVERIFIED]
3. **Sprint contracts** between generator and evaluator. ECC retired this when models improved. Momentum has structurally similar concepts (story files with ACs, Gherkin specs withheld from dev agents) — but they are not iteration-bounded the way ECC's sprint contract was.

**This is a discoverability problem, not a design defect.** Momentum may have reached its decisions independently. But not citing the paper means there is no evidence of a deliberate take on its claims.

### 5.7 Gap 7 — Cost discipline is not applied to runtime verification

AVFL's role tiers are benchmarked. Haiku is explicitly forbidden as Enumerator (false-pass risk); Sonnet is explicitly forbidden as Adversary (under-calibrated severity). [OFFICIAL — AVFL/SKILL.md lines 195–197]

`e2e-validator`: `model: sonnet`, `effort: medium`. No benchmark cited. [OFFICIAL — e2e-validator.md line 4]
`qa-reviewer`: `model: sonnet`, `effort: medium`. No benchmark cited. [OFFICIAL — qa-reviewer.md line 4]
`architecture-guard`: `model: sonnet`, `effort: medium`. No benchmark cited. [OFFICIAL — architecture-guard/SKILL.md line 4]

The Phase 5 reviewers all run as Sonnet/medium with no documented justification. This is not necessarily wrong, but it is an **undocumented decision**. Compare to AVFL's `framework.json` which carries full benchmark provenance.

---

## 6. What Momentum already does better than `gan-style-harness`

### 6.1 Coverage decomposition for artifacts
AVFL's 4-lens × 15-dimension structure is the cleanest taxonomy I have seen in any open agentic engineering practice, ECC included. ECC has nothing equivalent. [OFFICIAL — verified against the prior research synthesis]

### 6.2 Benchmarked role tiers
AVFL's "Sonnet enum, Opus adversary, Haiku consolidator, Sonnet fixer" is grounded in measured failure modes. `gan-style-harness` runs uniform Opus 4.6 with no tiering rationale beyond "needs deep reasoning."

### 6.3 Authority hierarchy + corpus mode
AVFL's `corpus: true` + `authority_hierarchy` parameter pair handles cross-document contradiction resolution deterministically. [OFFICIAL — AVFL/SKILL.md lines 35–60] Nothing in `gan-style-harness` addresses multi-document validation at all.

### 6.4 Selective re-review (Phase 4d)
After fixes, only the affected reviewer re-runs. [OFFICIAL — sprint-dev/workflow.md lines 453–472] `gan-style-harness` re-evaluates everything every iteration.

### 6.5 Retro + upstream-fix loop
Momentum's retrospective mines transcripts via DuckDB, runs an auditor team, classifies findings into intake/distill/decision. `gan-style-harness` has no equivalent: failures are caught in-loop and discarded.

### 6.6 Producer-judge split for **static** review
Both have it; AVFL's implementation is more developed (dual reviewers, severity weights, consolidator with HIGH/MEDIUM confidence cross-check). [OFFICIAL — AVFL/SKILL.md lines 145–158, 219–232]

### 6.7 Spec primacy
Momentum codifies "Specifications > Tests > Code. Agents never modify specifications or pre-existing tests to make code pass." [PRAC — referenced in prior research synthesis] `gan-style-harness` relies on `spec.md` immutability by convention but does not enforce it.

---

## 7. Recommendations — prioritized

### 7.1 Decision-doc (high priority) — Iterative behavioral verifier in dev?

**Verb:** decision-doc.
**Target:** `_bmad-output/decisions/iterative-behavioral-verifier-in-dev.md` (new).
**Effort:** 1 short session for the decision; sprint of follow-on stories if accepted.
**Dependency:** none.

Decide whether Momentum needs a per-story per-iteration "live evaluator" sub-agent inside dev — distinct from `e2e-validator`. Options:

- **A. Adopt as new sub-agent.** Add a `live-evaluator` agent definition that the dev agent must spawn before signaling merge-ready, scoped to the story's `touches` files only. New convergence signal: weighted runtime score ≥ threshold. Cost: doubles dev-iteration token spend. Risk: drift between this and `e2e-validator`. **Implementation must include**: (1) explicit anti-rationalization prompting (per §2.6.1 — evaluator must not "talk itself into approving" found issues); (2) few-shot calibration examples showing the evaluator how to *hold* objections; (3) Playwright MCP as the opinionated default for web projects (per Gap 4 and Anthropic's lead); (4) file-based feedback (`feedback-NNN.md` pattern), never inline (per AVFL's existing anti-pattern guidance and Anthropic's documented practice).
- **B. Extend dev agent.** Mandate that dev's own loop include a Playwright/cmux check before merge-ready. No new agent. Producer-judge split is **not** preserved. **Anthropic's paper argues this option is wrong:** their explicit finding was that self-evaluation fails even with prompting because "agents are pathological optimists." Listing this option for completeness, but the empirical evidence weighs against it.
- **C. Move `e2e-validator` earlier.** Run per-story before merge. Preserves split. Cost: per-story Phase-5-equivalent run, much more expensive.
- **D. Reject — defer to "strip when models improve."** Argue current Opus does enough self-eval; revisit when failure rate justifies. **Caveat:** Anthropic *kept* their Generator-Evaluator separation through the Opus 4.6 transition. They removed sprint contracts; they did not remove the evaluator. So "strip when models improve" is not, on Anthropic's evidence, an argument against producer-judge separation specifically — only against process-orchestration overhead.

Decision should land before any story is written. The Anthropic harness paper at https://www.anthropic.com/engineering/harness-design-long-running-apps is required reading for the decision-maker.

### 7.2 Intake-stub (high priority) — Cite Anthropic harness paper

**Verb:** intake-stub.
**Target:** `_bmad-output/implementation-artifacts/intake-queue.jsonl` (append).
**Effort:** 15 minutes for the stub; 1 small story to wire it.

Add an intake item: "Cite Anthropic March 2026 harness paper in AVFL and sprint-dev references where producer-judge separation is asserted." Provenance, not behavior.

### 7.3 Decision-doc (medium priority) — Convergence signal for dev iteration

**Verb:** decision-doc.
**Target:** `_bmad-output/decisions/dev-convergence-signal.md` (new).
**Effort:** 1 session.
**Dependency:** §7.1 should land first.

### 7.4 Adopt-now (low effort) — Document AVFL benchmark provenance in framework.json

**Verb:** adopt-now.
**Target:** `skills/momentum/skills/avfl/references/framework.json` (extend `sources.research`).
**Effort:** 30 minutes.

The 36-run benchmark is referenced in `SKILL.md` but the **artifact** is not pointed to from `framework.json`. Add a `sources.benchmarks` field with file paths to the actual run data. Hygiene; future-proofs against benchmark loss.

### 7.5 Decision-doc (medium priority) — Apply benchmark discipline to Phase 5 reviewers

**Verb:** decision-doc.
**Target:** `_bmad-output/decisions/phase-5-reviewer-routing.md` (new).
**Effort:** 1 session for decision; 1 sprint to actually benchmark.

Either run a one-sprint benchmark on `qa-reviewer`/`e2e-validator`/`architecture-guard`, or explicitly decide "we accept Sonnet/medium without benchmark for these — here is why."

### 7.6 Intake-stub (low priority) — Scaffolding audit against Opus 4.6

**Verb:** intake-stub.
**Target:** intake-queue.jsonl.

Anthropic's "every harness component encodes an assumption" principle is not currently audited against. Pick one Momentum scaffolding component and ask "does Opus 4.6 still need this?"

### 7.7 Ignore — Replicating gan-style-harness's 4-criterion rubric for AVFL

**Verb:** ignore. The Design/Originality/Craft/Functionality rubric is calibrated for frontend visual quality. Wrong domain for AVFL.

### 7.8 Ignore — Adopting `GAN_MAX_ITERATIONS=15` as Momentum's iteration cap

**Verb:** ignore. ECC's 15 is budget-bounded, not convergence-bounded. AVFL's 4 is correct for static validation.

---

## 8. Open questions for further investigation

- **Did the prior research synthesis rule out adopting `gan-style-harness` outright?** §3.4 of the synthesis cites three small wins (silent-failure-hunter, repo-scan, post-edit-format) but does not mention `gan-style-harness`. Was it considered and skipped, or not yet examined?
- **Has Momentum measured the cost of the gap?** §5.1 asserts that "any defect that passes pytest but fails when actually clicked lands in Phase 4–5." Is there retro data showing this? If not, the gap is theoretical. The decision in §7.1 should be informed by retro evidence.
- **Does `cmux` already cover the `gan-style-harness` use case?** `e2e-validator` uses `cmux send` + `cmux capture-pane` to drive live skill sessions. Could the same machinery drive live web apps with `cmux browser` (which exists per `~/.claude/rules/cmux.md`)? If yes, Option A in §7.1 is much cheaper than it looks.
- **Is `gan-style-harness`'s approach durable, or did Anthropic's own Stage-3 deprecation invalidate it?** The blog says they removed sprints when Opus 4.6 arrived. If Momentum builds an iterative behavioral verifier, what's the shelf life?

---

## 9. Sources

**Momentum source files (all OFFICIAL, file-verified 2026-04-27):**
- `/Users/steve/projects/momentum/skills/momentum/skills/avfl/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/avfl/references/framework.json`
- `/Users/steve/projects/momentum/skills/momentum/skills/code-reviewer/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/architecture-guard/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-dev/workflow.md`
- `/Users/steve/projects/momentum/skills/momentum/agents/qa-reviewer.md`
- `/Users/steve/projects/momentum/skills/momentum/agents/e2e-validator.md`

**ECC source files (OFFICIAL, GitHub-verified 2026-04-27):**
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/gan-style-harness/SKILL.md`
- GitHub API listing confirming the directory contains exactly one file: `SKILL.md`.

**External research (PRAC):**
- Anthropic, "Harness Design for Long-Running Application Development", Prithvi Rajasekaran, 2026-03-24. https://www.anthropic.com/engineering/harness-design-long-running-apps — read directly 2026-04-28; reinforces Gaps 2 and 4, supplies §2.6.1's evaluator-rationalization failure mode, supplies §2.7's three-stage evolution narrative, supplies §5.4's Playwright-as-default reinforcement, and informs §7.1 Option B and Option D analysis.
- ECC SKILL.md secondary references (not independently verified for this paper): Epsilla's GAN-Style Agent Loop deconstruction; Martin Fowler's Harness Engineering; OpenAI's Harness Engineering.

**Prior Momentum analysis (OFFICIAL):**
- `/Users/steve/projects/momentum/_bmad-output/research/everything-claude-code-vs-momentum-2026-04-26/final/everything-claude-code-vs-momentum-final-2026-04-26.md`
