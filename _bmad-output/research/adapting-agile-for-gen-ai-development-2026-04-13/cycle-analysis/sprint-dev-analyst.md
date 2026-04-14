# Sprint Dev Phase — Analyst Findings

**Date:** 2026-04-13
**Phase under analysis:** Sprint Dev (execution) — orchestrator `sprint-dev`, executor `dev`, quality gates `avfl`, `code-reviewer`, `qa-reviewer`, `e2e-validator`, `architecture-guard`, plus the `quick-fix` single-story variant.
**Research anchor:** `_bmad-output/research/adapting-agile-for-gen-ai-development-2026-04-13/synthesis/synthesis.md`

---

## Executive Summary

Sprint Dev is Momentum's most developed phase and its strongest alignment with the research is structural: the orchestrator-spawn-subagent pattern, worktree isolation, multi-lens AVFL, and the triple-reviewer Team Review (QA + E2E + Architect-Guard) map directly onto Codecentric, Anthropic, and Agentsway prescriptions. The dev agent already refuses to read `sprints/{slug}/specs/` — a deliberate read barrier that anticipates the Codecentric Isolated Specification Testing pattern.

Four material gaps versus the research:

1. **The isolation is partial.** Dev cannot read specs, but there is no symmetric barrier stopping the QA/E2E validators from reading `src/`, no `.claudeignore`, no permissions-enforced separation, and no self-test proving isolation holds. The pattern is declared; it is not technically enforced.
2. **Behavioral validation exists but targets the wrong surface.** `e2e-validator` runs against a running system (good) but validates against Gherkin scenarios that dev never saw (also good). AVFL — which is the heavy lifter during Phase 4 — validates **code against AC text**, not **running-app against user value**. The two are being conflated in the workflow's own language.
3. **There is no Judgment Frame anywhere in the execution chain.** The story is dense, technical, and AC-driven. DoD is a mechanical checklist. AVFL findings are structural. Nothing in Sprint Dev produces the Intent / Done-state-for-a-stranger / Anti-goals / Review-focus artifact the research identifies as the central missing practice.
4. **There is no value floor / walking-skeleton discipline.** Sprint Dev spawns stories in dependency order and parallelism but does not ask "does this sprint cross the value floor" or "is this the walking skeleton." Stories pass AC and the sprint closes whether or not a user can do the core thing.

The workflow also pays a real orchestration cost in Phases 4–4d (AVFL + code review + consolidated fix queue + selective re-review) that the research suggests is the wrong gate — it catches artifact quality, not outcome quality. Some of that complexity is carried for incorrect reasons.

---

## What Exists and How It Aligns

### Orchestrator-subagent topology (strong alignment)

`sprint-dev/workflow.md` codifies individual-agent spawning with exclusive write authority, explicit `<team-composition>` declarations, and a `spawn_registry` dedup guard. The workflow hard-forbids `TeamCreate` in dev/review/fix phases. This matches Anthropic's role separation principle, the Agentsway role-boundary prescription, and the Codecentric architectural premise that role separation must be by construction, not convention.

**Files:** `skills/momentum/skills/sprint-dev/workflow.md` lines 22–97, 183–186.

### Worktree isolation per story (strong alignment)

Every story runs in `.worktrees/story-{slug}` on a dedicated branch. Dev agents cannot interfere with each other. The worktree persists through Phase 4 and Phase 4d so fix agents inherit the story's isolated context. This aligns with Kurilyak's small-verifiable-unit reliability argument (5% per-action error rate → isolation reduces blast radius).

**Files:** `skills/momentum/skills/dev/workflow.md` lines 57–91; `skills/momentum/skills/sprint-dev/workflow.md` lines 289–295.

### Dev agent's read barrier on Gherkin specs (partial alignment with Codecentric)

`dev/workflow.md` line 13 contains a hard `<critical>`: "Never read files under sprints/{sprint-slug}/specs/ or any .feature file. Gherkin specs are for verifier agents only (Decision 30 — black-box separation)."

This is explicitly the Codecentric pattern: the implementation agent cannot read the specs the tester uses. Momentum recognizes this matters. What's missing is the symmetric barrier (tester cannot read `src/`), the technical enforcement (`.claudeignore`, permissions), and a self-test proving the barrier holds.

**Files:** `skills/momentum/skills/dev/workflow.md` line 13.

### AVFL as a scan gate (partial alignment with research; misnamed)

Phase 4 runs `avfl` in `checkpoint` profile with `stage: final` over the complete sprint changeset diff, with ACs as source_material. It is a read-only stop gate (no fixes in Phase 4; fixes are deferred to Phase 4d after developer review of a consolidated queue including per-story code-review findings).

AVFL's four lenses (structural, accuracy, coherence, domain) match the research's "artifact-quality evaluation" class. It's well-designed for that.

**Files:** `skills/momentum/skills/sprint-dev/workflow.md` lines 317–349; `skills/momentum/skills/avfl/SKILL.md`; `skills/momentum/skills/dev/references/avfl-invocation.md`.

### E2E-validator and QA-reviewer (partial alignment with Codecentric + Anthropic)

`agents/e2e-validator.md` is uncompromising: "You test behavior, not code. Reading source files is NEVER a substitute for execution." It requires running the system (via cmux for skills, via CLI/API/build for code) and observing outputs. This is precisely the Anthropic transcript-vs-outcome principle, and it is articulated forcefully.

`agents/qa-reviewer.md` also runs tests (not just reads code) and cross-story integration checks. It is read-only.

Together, these are the closest Momentum comes to outcome verification. The catch: they run once per sprint, in Phase 5, after AVFL and code-review have already consumed the attention budget. And e2e-validator's fallback hierarchy (Automated test → CLI/API → Build → cmux skill → Manual) means many scenarios in practice land on "I ran a build and checked an artifact," which is a file-on-disk outcome — better than transcript, not the same as "user can do the thing in a running app."

**Files:** `skills/momentum/agents/e2e-validator.md` lines 14–33; `skills/momentum/agents/qa-reviewer.md` lines 14–60.

### Architect-Guard (aligned with harness pattern)

`architecture-guard` runs pattern-drift detection against the architecture doc. This is a Fowler-style harness check — the architecture file is treated as accretive ground truth that constrains implementation. Matches "harness engineering" in the research.

**Files:** `skills/momentum/skills/architecture-guard/SKILL.md` (file exists, referenced in workflow line 532).

### Per-story code-reviewer (aligned but redundant with AVFL)

Phase 4b spawns `code-reviewer` per merged story in parallel, scoped to that story's `touches` list. Findings are merged with AVFL findings into the Phase 4c consolidated fix queue. This is a dual-reviewer architecture at the sprint level (AVFL on the full diff, code-reviewer per story), which the research supports as higher-recall than single-agent review.

**Files:** `skills/momentum/skills/sprint-dev/workflow.md` lines 355–380; `skills/momentum/skills/code-reviewer/SKILL.md`.

### Developer checkpoints / consent gates (aligned with Osmani risk-tiered review)

Phase 4c presents a consolidated fix queue and asks the developer per-finding "fix or defer." Phase 5 asks "address, defer, or accept" after Team Review. Phase 6 is an explicit Gherkin-scenario confirmation checklist the developer ticks through. These are the right kind of human-in-the-loop gates — recognition-mode checks on discrete items, which the research argues is the only form of human review that survives AI velocity.

**Files:** `skills/momentum/skills/sprint-dev/workflow.md` lines 409, 559, 600–605.

---

## Gaps: What the Research Says Should Exist

### Gap 1 — The Judgment Frame is absent at every level

**Research prescription (Problem 2, recommendation 2):** Every story gets a sibling human-review block above the AC — Intent / Done-state-for-a-stranger / Anti-goals / Review focus. Feature-level Judgment Frame rolls up from story frames.

**What exists:**
- The story file has a Momentum Implementation Guide (for the AI) and AC (dense, technical).
- DoD is a mechanical checklist (evals exist, frontmatter present, AVFL noted).
- Phase 6 Verification surfaces Gherkin scenario names — but these are behavioral assertions, not intent/anti-goal statements, and they are **generated from the AC rather than from user-value reasoning**.

**Evidence of absence:** A text search across the sprint-dev skill tree for `judgment frame|value floor|walking skeleton|north star|anti-goal|done-state` returns zero matches. This is a named-concept absence, not merely an unimplemented feature.

**Consequence:** The developer has nothing glanceable to review. They either read session JSONL (too raw), accept the session summary (too abstract), or read AC line-by-line (too technical, doesn't show intent). The research names this exact failure mode as the central unsolved problem in the literature; Momentum has not yet closed it either.

### Gap 2 — Isolated Specification Testing is declared, not enforced

**Research prescription (Problem 3, recommendation 1):** `.claudeignore` + settings-based permissions. Implementation agent technically cannot read `qa/`. Tester agent technically cannot read `src/`. Playwright MCP as shared ground truth. Self-test proving isolation holds.

**What exists:**
- Dev agent has a text-level `<critical>` instruction not to read specs. This is an instruction, not a permission barrier — a sufficiently aggressive model or prompt could bypass it.
- E2E-validator and qa-reviewer have no corresponding barrier against reading source. In fact, qa-reviewer is explicitly told in step 3: "Read the relevant implementation files (use the story's file list and git log)" (`agents/qa-reviewer.md` line 49). It is reviewing code, not running-app output.
- No `.claudeignore` or `settings.json`-level permission enforcement.
- No self-test proving isolation.

**Consequence:** The CAISI finding (agents cheat when they can read the eval target) applies. Momentum is currently relying on prompt-level instruction rather than capability-level restriction, which the research explicitly warns against.

### Gap 3 — The transcript-vs-outcome split is partially observed

**Research prescription (Problem 3, recommendation 5):** A story's validation evidence must include environment state (DB record, file on disk, running UI) — not agent narration.

**What exists:**
- `e2e-validator` fully embraces this for its scope — it explicitly rejects source-reading as a substitute for execution.
- AVFL, by contrast, validates artifacts (code diff + AC text). It cannot verify environment state. It is validating what the agent *wrote* against what the spec *said*, which the research identifies as "checking code against itself."
- DoD (`dev/references/dod-checklist.md`) requires "AVFL result noted in Dev Agent Record" — this is transcript-evidence of validation, not environment-state evidence.
- Per-story code-reviewer is read-only on files; cannot access environment.

**Consequence:** In Phases 4 and 4b, the quality signal is entirely artifact-level. Environment-state evidence only arrives in Phase 5, from one of three reviewers (the E2E validator), whose verdict can be PASS even when many scenarios degrade to CLI/build/cmux-capture checks rather than true end-to-end running-app verification. The research's prescription is that every story produces environment-state evidence; Momentum produces it once per sprint, and only partially.

### Gap 4 — No walking-skeleton / value-floor discipline

**Research prescription (Problem 4, recommendations 1–5):** North Star capability statement per feature. Sprint 1 on a new feature targets end-to-end capability however minimal. Gap check at sprint close: "are we closer to the North Star than before?"

**What exists:** Nothing. `sprint-dev/workflow.md` phase 7 outputs story counts, AVFL finding counts, scenario-confirmation counts, and push summary. It never asks whether a user can do the core thing. Phase 1 of sprint-dev initializes from the sprint record; it does not verify that the sprint targets a value-floor crossing or an elaboration.

**Consequence:** The owner's failure mode — 5–10 sprints deep, still below value floor — is structurally undetectable by the current Sprint Dev close. Every sprint can pass its gates while the product delivers zero cumulative user value. This is the research's Problem 4 verbatim, and Momentum has not addressed it.

### Gap 5 — AVFL is carrying weight it wasn't designed to carry

**Research prescription (Problem 3, recommendation 4):** "Do not adopt DeepEval / MLflow / Inspect AI for app validation. They measure whether an LLM produces good output, not whether a running application behaves correctly. Conflating them will produce a false sense of coverage."

**What's happening:** AVFL is Momentum's own LLM-output evaluator (per its own SKILL description: "multi-agent validation catching errors, hallucinations, and quality issues"). It is being invoked in Phase 4 with the sprint diff as `output_to_validate` and ACs as `source_material`. This is artifact-against-spec validation — exactly the class the research warns cannot substitute for behavioral validation.

The workflow mostly treats AVFL correctly (Phase 4 is declared a "read-only stop gate" and the real behavioral validation happens in Phase 5). But the orchestration-cost of Phase 4 → 4b → 4c → 4d (AVFL + code-review + consolidated queue + selective re-review + worktree cleanup) is substantial, and its output is still artifact-quality findings. The research position would be: reduce this layer's role, move attention budget earlier (Judgment Frame) and later (running-app verification in Phase 5).

### Gap 6 — Human review happens too late and at the wrong artifact

**Research prescription (Problem 2, recommendation 7c):** "Move the review forward, not back. The review you want is *before the spec goes to the AI* (the Judgment Frame, the anti-goals, the review focus). This is the highest-leverage change."

**What exists:** The only story-level human review gate in Sprint Dev is Phase 6 (Gherkin scenario checklist, after all implementation and fixes). `quick-fix` has earlier gates (Phase 1 story review, Phase 2 spec review) but `sprint-dev` has none pre-implementation — sprint-planning handles approval, and by the time sprint-dev runs, the developer is reviewing output, not intent.

**Consequence:** The developer reads the running output, which the Vibe-Check Protocol paper identifies as *recognition mode* — the brain takes the easy path and misses failures. The high-leverage review (is the intent right? are the anti-goals specified? what should I care about when it's built?) happens implicitly during sprint-planning and never again during sprint-dev.

### Gap 7 — Red-phase TDD is not enforced

**Research prescription (Problem 3, recommendation 2):** Before dev implements, tester produces failing scenarios against the un-built feature. If all scenarios pass before implementation, specs are wrong. If dev's first run passes without implementation changes, something is bypassed.

**What exists:** Sprint-planning generates Gherkin specs (per `gherkin-template.md`) but Sprint Dev never runs them pre-implementation. E2E-validator runs post-merge, post-fixes. There is no red-phase check that the specs fail before the code is written.

**Consequence:** Beck's documented failure mode (AI deletes tests to make them pass) is not caught by construction. Momentum catches it only indirectly via the dev-cannot-read-specs barrier plus e2e-validator running post-hoc.

### Gap 8 — No behavioral regression eval set

**Research prescription (Problem 3, recommendation 3):** A curated 20–50 task set of past failures with observable reproductions. Run after major changes.

**What exists:** Individual skill `evals/` directories (skill-level behavioral tests). No sprint-level or practice-level behavioral regression set. Momentum retros capture findings but there is no persistent eval corpus fed back as regression guard.

---

## Removal Candidates

Be cautious here — removal should follow decision by the developer. These are flagged as "research says this layer is doing less than you think" not "delete this."

### Candidate 1 — Consolidate Phase 4 (AVFL) and Phase 4b (per-story code-reviewer)

Both run post-merge, both scan the sprint diff, both produce text-content findings. The research's dual-reviewer argument supports having two framings, but it does not specifically require this to be two orchestration layers with a consolidation phase. Options:

- **Merge them:** Have AVFL run per-story at checkpoint profile (it already supports `corpus: true` for multi-document scans) and drop the separate code-reviewer skill.
- **Keep both, remove the consolidation:** If they are genuinely orthogonal, reconsider whether Phase 4c + 4d's per-finding fix-or-defer flow earns its cost. In practice this is 4+ phases of AI-on-AI review before a single behavioral scenario runs.

### Candidate 2 — Phase 4d's selective re-review loop

Phase 4d re-runs AVFL and/or code-reviewer after fix agents execute, then offers another fix cycle on remaining findings. The research explicitly cautions against long AI-on-AI review loops — they correlate failure modes and drain attention. If Phase 4 is the stop gate and Phase 5 (Team Review) is the behavioral gate, Phase 4d is doing a third pass of artifact-review that the research suggests is sub-additive in value.

### Candidate 3 — Verification Phase 6 as currently constructed

Phase 6 is "developer tick-through every Gherkin scenario." The research does not endorse this: it puts the developer in recognition mode on a list of items the system itself is also checking (via e2e-validator in Phase 5). Either (a) this is a redundant checkpoint or (b) it is the real human-judgment moment, in which case it should be upgraded to a Judgment Frame review, not a Gherkin scenario checklist. Current form is a middle ground that does neither well.

---

## Feature Layer Integration Opportunities

These are places where Sprint Dev would be **consumed by** a feature/epic-level practice if the research's recommendations are adopted:

1. **North Star capability statement per feature** needs to live at feature-grooming or epic-grooming (Momentum already has these skills). Sprint Dev reads this at Phase 1 initialization and at Phase 7 close asks "did this sprint move toward the North Star."

2. **Feature-level Judgment Frame** rolls up from story Judgment Frames. Produced during feature-grooming; consumed by Sprint Dev at story-spawn time (injected into dev agent context as the "why") and at sprint close (Phase 7) as the rollup summary shown to the developer.

3. **Value-floor state (pre-floor / post-floor)** is a feature-level attribute. Sprint Dev's Phase 2 (Dev Wave) behaves differently in each state: pre-floor sprints must close the value-floor gap; post-floor sprints can elaborate. This is a gate Sprint Dev enforces, not a concept it owns.

4. **Behavioral eval set** belongs at the practice level (cross-sprint). Sprint Dev should trigger a post-merge run of the eval set before Phase 7 closure, as a regression gate.

5. **Isolated tester agent with `.claudeignore` / permissions** is a practice-level harness. Sprint Dev consumes it in Phase 5 by invoking an isolated variant of e2e-validator that has had its source-read permissions removed by configuration, not by prompt.

6. **Gap artifact** (Here / There / Gap / Path check) is a sprint-planning output reviewed at sprint-dev Phase 7. Sprint Dev is the natural place to enforce "no silent punts" — when Phase 4c or Phase 5 findings reveal the sprint did not close its gap, the workflow should surface this rather than ask fix/defer on finding-by-finding basis.

---

## Questions Raised

1. **Is AVFL the right tool in Phase 4?** AVFL is excellent at artifact-against-spec validation. Sprint Dev is asking it to be a sprint-level quality signal, which the research warns against. What does Phase 4 look like if AVFL runs only on story files at story-merge time (embedded in `dev`), and Phase 4/4b/4c/4d is replaced with a single behavioral-validation pass against a running build?

2. **What enforces the dev agent's read barrier?** Right now it is a prompt-level `<critical>`. Would `.claudeignore` or a `settings.json` deny-read rule on `sprints/*/specs/**` be technically feasible in the Agent tool spawning path? Is there a sub-agent `allowed-tools` or `disallowed-paths` mechanism available?

3. **Should dev produce a Judgment Frame on completion rather than read it from the story?** The research prescribes the Frame as input to the AI (review focus, anti-goals, intent). A complementary question: does the dev agent's session transcript contain information that could be distilled *back* into a post-hoc "Done-state-for-a-stranger" statement, which would make Phase 6 a Judgment-Frame confirmation rather than an AC-checklist confirmation?

4. **What is Phase 6 Verification actually for?** It ticks through Gherkin scenario names. If the e2e-validator already ran these in Phase 5, Phase 6 is a re-check. If e2e-validator produced PASS on scenarios that Phase 6 disputes, what is the resolution rule?

5. **Does quick-fix's pre-spec developer review (Phase 1 Approve/Revise) belong in sprint-dev too?** In quick-fix the developer approves the story spec before implementation starts. Sprint Dev assumes that approval happened in sprint-planning, but there is a gap: between sprint-planning approval and sprint-dev spawn, the story is re-read by the dev agent in a fresh context. A pre-spawn developer review per story (even an opt-in checkpoint-preview) would align with the research's "move review forward" recommendation.

6. **How does walking-skeleton discipline interact with the current dependency-graph-driven spawning?** Phase 2 spawns all unblocked stories in parallel. If a feature's walking skeleton requires one story to ship before the rest have value, the parallel spawn may complete a sprint full of elaborations without the skeleton. Does dependency graph need a "skeleton gate" node that must complete before any elaboration starts?

7. **Where does the value-floor gap check live?** It could be Phase 7 (sprint close, retrospective-adjacent) or it could be earlier — Phase 0 pre-initialization, before any dev spawns, asking "does this sprint's selected stories close the gap to the North Star?" Research recommendation 5 (Problem 4) says "do not punt gaps" — implying the check should be at both ends.

8. **What is the behavioral evidence artifact?** e2e-validator produces a report (PASS/FAIL per scenario with evidence snippets). Is this artifact archived per sprint? Does it accumulate into the behavioral regression eval set the research prescribes? Currently it appears to be consumed in-session and not persisted as a reusable corpus.

9. **Does `code-reviewer` have an isolated-agent variant that only sees a running build?** Currently it is read-only on source. The Codecentric pattern prescribes the reverse — source-blind, behavior-only. A variant spawned in Phase 5 could provide the symmetric barrier missing from the current isolation story.

10. **Is the dev agent's inability to access Gherkin specs costing quality?** The research prescribes this isolation, but the dev agent is implementing against plain-English ACs in the story file. If those ACs diverge from the Gherkin scenarios (which are generated in sprint-planning), the implementation can be AC-correct and Gherkin-failing. How does Sprint Dev detect AC-Gherkin drift prior to Phase 5?

---

**End of analyst findings.**
