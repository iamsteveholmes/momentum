# Momentum Cycle Analysis — Adapting Agile for Gen AI Development

**Date:** 2026-04-13
**Status:** NOT A DECISION DOCUMENT — raises questions and options for owner review.
**Inputs:** Research synthesis + 10 per-phase findings files (analyst and challenger pairs across Triage, Backlog Refinement, Sprint Planning, Sprint Dev, Retro).

---

## Executive Summary

Ten independent analyses of the five Momentum cycle phases converge on a narrower diagnosis than their collective length suggests. The practice is operationally disciplined and individually well-engineered: orchestrator purity, worktree isolation, dependency-wave execution, DuckDB-powered retro audits, and a feature catalog that already carries value-shaped language. Where it falls short is directional: nearly every gate in the cycle asks a variant of "is the artifact specification adequate?" and almost none asks "is what we're building still pointed at user value?" The owner's own framing — the value floor, the spec-correct/value-zero failure, the human-readable judgment section — is not just a research recommendation but the throughline every phase's findings return to independently.

Three cross-cutting themes emerge from all ten files. First, the value floor has no structural home anywhere in the cycle, so there is no point at which the practice can detect that 5–10 sprints of spec-correct stories have failed to cross a feature's minimum viable capability. Second, the "human readability optimized" judgment artifact the owner described is absent from every phase — intake captures user-story sentences, refinement produces dense AI specs, planning and dev operate on ACs and Gherkin, retro audits transcripts — nowhere is there a glanceable section a non-technical reader could judge intent against. Third, validation independence (Codecentric isolated specification testing) is declared in prose but not enforced by construction, so AVFL, code-review, QA, and architecture-guard all read largely the same context the implementer read, producing correlated rather than independent signal.

Two or three hardest unresolved questions sit upstream of any change: Is the feature (not the story) the primary human-judgment unit, and if so, does the data model need to be reshaped before any phase-level redesign begins? What is the Momentum product's own value floor — and has it crossed it, given that the same pipeline now being analyzed built the practice itself? And: if sprint-close is the wrong place to catch a punt (the challengers argue it's already too late), where in the cycle does the gap check go — before sprint planning, inline during dev, at story merge, or somewhere that does not yet exist?

---

## Reading Guide

The analysis was organized as five analyst/challenger pairs, one per cycle phase. Analysts mapped current skills against the research synthesis and identified concrete gaps and integration opportunities — their tone is structural and additive. Challengers audited the same phase for assumed truths, over-building, and structural misalignment — their tone is adversarial, asking whether the phase should exist in its current shape at all. Where the two agree within a phase, the signal is strongest; where they disagree, the disagreement itself usually identifies a live design tension that has no obvious resolution.

Cross-cutting themes (next section) draw the robust patterns — the things most or all ten files raise independently. Per-phase analysis (following) then presents each phase as its own unit so the owner can see what each pair agreed on, what they disagreed on, and what questions remain open. Hard questions are listed last — not because they are least important, but because they are the output of this document. They are the decisions the owner must make before any phase can be redesigned, because most redesign paths cascade through each other.

---

## Cross-Cutting Themes

### Theme 1: The Value Floor — Missing End-to-End

Every phase findings file raises some variant of the value-floor problem independently. The research's framing (Problem 4 in the synthesis) is that a practice can deliver 5–10 sprints of spec-correct stories without crossing the minimum viable capability threshold — and in AI-native practices this failure is structurally invited, because the "is the spec correct?" question gets answered automatically while "are we closer to the destination?" goes unasked.

The triage pair finds intake has no North Star check and no pre-floor/post-floor flag — every passing idea is captured identically regardless of whether it moves toward the floor or elaborates around it. The refinement pair finds `feature-grooming`'s `value_analysis` is descriptive (what the feature delivers in theory) not gating (does the backlog path close the gap), and that the deferred-value flag is a near-miss that operates at the feature level without detecting product-level composition issues. The sprint-planning pair finds no sprint goal, no walking-skeleton discipline, and no here-to-there gap analysis; selection is priority-weighted, not gap-weighted. Sprint-dev's challenger puts it sharpest: every metric in the sprint completion summary can be green while the feature's value floor remains uncrossed, and the volume of green checkmarks creates the illusion of progress. Retro's analyst notes that features.json already carries an `acceptance_condition` field that reads exactly like the North Star the research recommends — but the retro never loads it.

The agreement across all ten files is unambiguous: the value floor is the most load-bearing gap. What the files disagree on is where the fix goes. Analysts tend to propose *adding* a gap-check step to refinement, sprint planning, and retro. Challengers argue the gap check at sprint close is already too late — by then the punt has been cemented — and push the question upstream, to intake ("reject stories that don't advance the floor"), to feature-grooming ("no feature enters the backlog without a North Star"), or above the cycle altogether ("shape pitches before they become stories"). Whether the owner wants the floor check enforced at one point, multiple points, or at a new pre-cycle entry gate is unresolved.

### Theme 2: The Judgment Frame — Human-Readability Gap

The owner's stated problem — session JSONL too raw, summary too abstract, AC too technical, nothing in between — appears in every findings file as the human-readable judgment artifact that Momentum does not produce anywhere.

Triage's intake captures an "As a / I want / so that" sentence fragment. The analyst notes this is adjacent to but not the Judgment Frame the research prescribes (Intent / Done-state-for-a-stranger / Anti-goals / Review focus). The challenger is harsher: the user-story form is explicitly insufficient per the research, and intake is the earliest and cheapest moment to capture the Judgment Frame while the human-in-the-conversation context is fresh — yet intake optimizes for speed over judgment at exactly the point where friction would have the most leverage. Refinement's `create-story` produces a Momentum Implementation Guide for the AI but no sibling artifact for the human; the AC is the only thing a human can look at, and the research explicitly identifies AC as not glanceable. Sprint planning produces nine artifact types at story grain and zero at the grain the research says humans operate at. Sprint-dev's challenger calls this "recognition mode by construction" — every owner review gate in the pipeline hands the owner pre-digested AI output to react to, which is precisely the cognitive mode the Vibe-Check Protocol paper says misses failures.

The convergence is that the Judgment Frame has no home. The divergence, again between analysts and challengers, is about whether it lives at the story level, the feature level, or both. Analysts lean toward both — per-story Judgment Frames rolling up to per-feature frames. Challengers press the question: if the feature is the human's unit (per Kurilyak, Shape Up, Torres), maybe the per-story frame is wasted effort and the frame should only exist at the feature. The synthesis itself does not resolve this — it notes that feature-level review is too coarse to catch AC-level failures, but story-level review can't scale to AI velocity. This is a genuine open problem with no borrowed answer.

### Theme 3: Validation Independence — What "AVFL CLEAN" Actually Means

Three findings files — both sprint-dev pairs and both retro pairs — argue the Momentum quality pipeline produces correlated rather than independent signal, because every reviewing agent reads substantially the same context the implementer did.

The sprint-dev challenger states it most directly: the dev agent reads the story, AC, architecture, rules. AVFL reviewers read the diff and the AC. Code-reviewer reads touched files and the story. QA reads the AC. Architecture-guard reads architecture and touched files. The only role with genuinely different context is E2E-validator, and even that is a text agent receiving Gherkin rather than an isolated-process agent with a running-app handle. "Twenty correlated reviewers can all agree on the wrong answer." The analyst agrees that isolation is declared but not enforced — the dev agent has a `<critical>` prose rule not to read Gherkin specs, but no `.claudeignore`, no `settings.json` permission, no self-test proving isolation holds. The CAISI findings on agent cheating (0.1–4.8% in controlled benchmarks) are the research's direct warning that prose enforcement is insufficient.

A specific subclaim surfaces in both sprint-dev files: AC is currently the source of truth for both production and verification. The dev agent implements to the AC. AVFL's source material is the AC. When AVFL passes, the signal is "the implementation matches the spec it was written against" — which is tautological, not adversarial. The research resolution is the Codecentric pattern: the source of truth for verification is running-app behavior mediated by an isolated tester; the AC is the dev's input, not the verifier's.

The open questions here are about what the practice stops trusting if it builds the isolated harness. Both sprint-dev findings ask: if Codecentric isolation is built, does AVFL Phase 4 still earn its cost, or does it collapse into drafting-stage review only? Does the Phase 4 → 4b → 4c → 4d structure (AVFL + per-story code-review + consolidated fix queue + selective re-review) survive the redefinition? Neither finding answers this — both present it as a decision the owner must make.

### Theme 4: Ceremony vs. Signal — Where Is the Real Work?

A pattern the challenger findings in particular emphasize: Momentum is heavily invested in certain ceremonies (sprint planning's 10 steps, sprint-dev's 7 phases, retro's 4-agent team) and under-invested in the one-line primitives that actually change the system. The retro challenger names this most cleanly: "distill is a sub-step of retro, but distill is the valuable primitive." Phase 5's Tier 1 → distill routing is where the harness actually changes, but it is gated behind five conditions (sprint completion, retro running, Phase 4 agents tagging findings, Tier 1 heuristics matching, practitioner approval). Meanwhile the findings document — which doesn't change the harness — is written unconditionally.

Similar patterns surface elsewhere. Sprint-planning's challenger argues AVFL at planning time catches internal-contradiction defects in a paper plan (the cheap failure mode) while the expensive failure mode (value-floor punting) has no gate at all. Refinement's challenger argues `create-story`'s Implementation Guide injection gives every story the full spec treatment regardless of appetite — the Kiro "4 user stories and 16 ACs for one bug fix" failure applied preemptively. Triage's challenger points out intake optimizes for speed (1 read, 1 write, 1 bash) at the single point in the cycle where the research says friction carries the most leverage.

This theme is not unified in its prescription. Some findings suggest specific consolidations (merge AVFL and code-reviewer; drop the per-sprint team-composition rebuild when specialists haven't changed; demote epic-grooming into a step inside refine). Others argue for tiered treatment (light story shape for small work, full treatment only for AI-reliability-critical cases). Challengers in particular lean toward subtraction: fewer gates, moved earlier, doing less. Analysts lean toward reframing: keep the step but change what it asks.

### Theme 5: Feature as the Human Unit, Story as the AI Unit

Every phase findings file independently concludes the feature is the unit human judgment should operate at, and Momentum's current architecture treats the story as that unit. The research convergence (Kurilyak, Shape Up, Torres, JTBD, OpenAI PR-as-unit) is that human judgment grains should be coarser than AI execution grains. Momentum has the feature-layer scaffolding — `features.json`, `feature-grooming`, `feature-status` — but the feature layer is disconnected from the cycle that uses it.

Evidence: intake routes to an epic, not a feature; `create-story` does not read `features.json`; sprint-planning does not invoke `feature-status`; sprint-dev iterates stories and closes with a story-count summary; retro's `Features Advanced` section pulls from feature-status but is descriptive, not evaluative. The feature layer exists in the data model. It does not exist in the ceremony. Refinement's analyst puts it compactly: "features.json is already 'ordinal' — exploit that" — but the consumers don't yet consume it as an ordinal judgment source.

The open question here is one of sequencing. If the owner commits to feature-as-primary-judgment-unit, the implications cascade: stories need a first-class `feature_slug`, `create-story` needs to read feature value-analysis, sprint-planning needs to commit at feature grain, sprint-dev's close needs to roll up to features, retro needs a per-feature gap check. No single phase's redesign works in isolation. Multiple findings note this explicitly: "attempting intake redesign first will produce a well-designed collector for a system that still can't say what it's collecting toward" (triage challenger); the retro analyst's "feature-status is read, not mutated" captures the same structural disconnection.

---

## Per-Phase Analysis

### Triage / Intake

Both pairs agree intake is operationally competent at what it claims to do (fast capture of conversational context to a stub) and structurally misaligned with what the research says triage should do (first-gate judgment about whether the item should be admitted, at what priority, with what anti-goals). The analyst maps five concrete gaps — Judgment Frame capture, feature assignment (not epic), North Star check, anti-goals, risk-tier. The challenger goes further and questions whether every captured idea should become a story at all, noting intake has no reject path, no merge path, no shape-first-then-capture path.

They agree the stub template's nine DRAFT sections codify the research's anti-pattern: AC-layer artifacts at capture time anchor attention on verification-shaped questions when the actual need is intent-shaped questions. Both identify the feature layer as the integration opportunity — `features.json`'s `acceptance_condition` field is adjacent to the North Star the research prescribes, and intake never touches it.

The disagreement is one of scope. The analyst treats the problem as "intake is underscoped — add the Judgment Frame, feature assignment, and anti-goals capture." The challenger treats it as "intake is misframed — the question is whether `intake` should exist as a separate skill at all, or whether `momentum:shape` should be the front door and stories be created only during sprint planning as execution artifacts." The analyst's path is additive redesign; the challenger's is architectural replacement.

The most important open question from this phase: whether intake's job is *fast context capture* (speed) or *first-gate value judgment* (friction where leverage lives). The challenger argues these are incompatible — pick one and redesign the other skill to cover the other need. The analyst doesn't fully pick sides but leans toward the friction answer.

### Backlog Refinement

Both pairs agree the four-skill pipeline (`refine`, `epic-grooming`, `feature-grooming`, `create-story`) is operationally thorough but conceptually aimed at taxonomy hygiene rather than the AI-native failure modes the research identifies. Both call out that `feature-grooming` already has the right *shape* for a judgment layer (three-paragraph value_analysis, outcome-form acceptance_condition, type classification) but its output is a catalog consumed by a dashboard, not a judgment artifact that cascades into stories. Both note `create-story` produces a dense AI-execution artifact with no sibling human-readable Judgment Frame, and that AVFL validates stories against epic text (a consistency check) rather than against user value (a value check).

The challenger is more cutting about specification inflation: the Implementation Guide injection on every story regardless of appetite is the Kiro failure mode applied preemptively, and the research's curse-of-instructions warning says this degrades model performance past a threshold. Both point at the same feature-to-story data flow gap: stories lack a `feature_slug`, `create-story` doesn't read `features.json`, so the rich value content in the feature catalog never reaches the stories that inherit from the feature.

The nature of the disagreement is how much surgery the phase needs. The analyst proposes extending `feature-grooming`'s schema (add `north_star`, add `floor_status`), adding a Judgment Frame step to `create-story`, adding a fifth heuristic to `refine`'s prioritization (gap-to-floor priority). The challenger argues the pipeline's predicate itself is wrong — every gate asks "is this spec adequate?", none asks "is this the right thing to build now?" — and that the fix requires a pre-pipeline judgment gate that can veto the whole thing, plus removing specification depth that cannot pay for itself. The analyst patches; the challenger rearchitects.

Open question: if `create-story` is the heavyweight single shape for every story, does the practice need a tiered model (light shape for small work, full shape for reliability-critical work), and if so, what determines the tier?

### Sprint Planning

Both pairs converge on four gaps: no sprint goal or hypothesis, no walking-skeleton/value-floor concept, no here-to-there gap analysis at planning, and capacity framing (3–8 stories) instead of appetite framing (ordinal time). Both observe that story selection is priority-weighted, not gap-weighted, and that the developer reviews a story list at Step 7 with no feature-level rollup showing what capability the sprint will deliver.

The analyst catalogs these as missing ceremony — add a sprint goal, add a North Star display, invoke `feature-status` inline, add pre-floor/post-floor tagging to sprint records. The challenger is more foundational: the sprint-planning workflow reproduces almost one-for-one the artifacts of a team-scale sprint planning meeting, inside a solo AI-first practice, and the ceremony is calibrated to the wrong scale. The research-aligned alternative (weekly governance + continuous flow + appetite + red-phase TDD + running-app AVFL) is so different that the question isn't "which steps do we add?" but "does the current workflow survive the comparison at all?"

The nature of the disagreement: the analyst assumes the workflow's 10 steps are a reasonable base to extend. The challenger's claim is that pre-sprint commitment itself contradicts the last-responsible-moment principle — Gherkin specs, architecture updates, specialist assignment, and wave computation all front-load decisions at the moment knowledge is lowest. Analyst extends the workflow; challenger asks whether the workflow-as-such is the pattern.

Most important open question: if you believed the research, the planning step would be a one-week governance rhythm with a North Star gate, a walking-skeleton check, a Judgment Frame per story, and red-phase specs generated during dev. Either the current ceremony survives comparison to that alternative or it doesn't. The challenger's hardest question: "Write the alternative workflow. Compare it. Which one is better?"

### Sprint Dev

This is the phase with the most elaborated findings. Both pairs agree sprint-dev is Momentum's strongest structural alignment with the research on orchestrator topology (spawn individual subagents, exclusive write authority, worktree isolation, dependency waves) — and its weakest alignment on behavioral validation independence. Both observe that the running application is absent from the workflow's requirements: nothing forces the app to build and run, not before dev, not at AVFL, not at code-review, not at team-review, not at verification. E2E-validator names running behavior but the workflow does not mandate execution infrastructure (Playwright MCP, running-app handle) to make that execution real.

Both identify the Codecentric isolation pattern as declared but not enforced — the dev agent has a prose `<critical>` rule not to read specs, but no `.claudeignore` and no symmetric barrier preventing validators from reading source. The CAISI findings on agent cheating apply. Both argue the DoD is almost entirely structural (tests run, frontmatter parses, AVFL was noted) and never asks whether a user can do something they couldn't before.

The challenger is sharpest about the correlated-signal problem and about the "recognition mode by construction" pattern — every owner review gate hands pre-digested AI output to react to, never forcing generative-mode review. Both flag that AVFL's source material is the AC, which is also the dev's input, so AVFL PASS means "implementation matches the spec it was written against" — tautological rather than adversarial.

The disagreement is one of response: the analyst's removal candidates are conservative (consolidate Phases 4 and 4b, re-scope Phase 4d, rethink Phase 6 Verification). The challenger is explicit: "remove the AVFL Phase 4 + 4b + 4c + 4d apparatus and add a feature-level value-floor gate at sprint close with a running-app demonstration requirement." Analyst patches the pipeline; challenger argues the pipeline is doing consistency work, not validation work, at high developer-attention cost.

Open questions: what specifically has AVFL caught in recent sprints that a linter + "does the app build and boot" check would have missed? Has the Momentum product itself crossed its own value floor over the sprints that built it?

### Retrospective

Both pairs note retro is one of the more advanced pieces of Momentum (harness-failure focus rather than velocity, transcript/outcome separation at the session level, the Tier 1 → distill routing as a real "on the loop" primitive). Both identify the same four gaps: no value-floor check, no feature-level closure, no persistent eval-set extraction, transcript-only ground truth (no environmental-state verification).

The challenger's framing is more structural: the retro inherits team-retrospective shape (four-agent TeamCreate reproducing the three-roles-plus-facilitator pattern from Scrum) in a solo context where the separation of concerns that makes team retros work doesn't obtain. The findings document reproduces the "what worked well / what struggled" traditional frame — an artifact the research explicitly says continuous quality monitoring displaces in AI-native teams. The sprint-summary with a 500-word cap is stakeholder-communication ceremony presuming an audience that doesn't exist in solo practice.

Both agree the Tier 1 → distill routing is the most valuable primitive in the retro, and both note it is buried behind gates. The challenger proposes distill should run continuously (per-merge, per-failure, per-intervention) with retro becoming a thin audit of "did we distill everything we should have?" Analyst's version is more conservative — add a ternary routing (distill | eval | stub) and integrate `feature-status` more deeply.

Specific disagreement: the analyst treats the four-agent auditor team as a strength worth endorsing as-is. The challenger treats it as over-engineered instrumentation for weekly sprints of 5–10 stories, producing correlated rather than independent signal.

Open question: if the retro were replaced with a 10-minute sprint-close gate that verifies stories, runs distill on queued learnings, answers three gap questions, and transitions sprint state — what would be lost?

---

## Hard Questions for the Owner

These are the questions the findings raise that must be answered before any redesign can begin. They are not rhetorical and they do not have obvious answers. They are organized into four decision clusters because most of them cascade into each other.

### Cluster A: Value measurement and the floor

1. What is the Momentum product's own value floor — and has it crossed it? Over the last N sprints, has any sprint close produced a thing an outside user could pick up and get value from that they couldn't before? If yes, which sprint and what was the mechanism? If no, the pipeline currently being analyzed is optimizing for a thing that is not the thing — and that matters for how much confidence to place in any of the current phase design.

2. Where in the cycle does the gap check belong, and is it one point or multiple points? Findings place it variously at intake (reject pre-floor admits), at refinement (gap-to-floor heuristic), at sprint planning (North Star gate at step 1), at sprint close (retro-adjacent), or above the cycle (before stories exist at all). The analyses do not converge. The owner must decide whether this is a single enforcement point or a layered check.

3. Is `acceptance_condition` in features.json the right source for North Star capability, or is a separate `north_star` field needed? If `acceptance_condition` is full-vision rather than minimum-viable, it cannot gate the pre-floor/post-floor distinction. A separate field is clearer; repurposing the existing one is cheaper.

4. What defines "pre-floor" vs. "post-floor" in a way the system can compute? Is it human-judged, derived from story completion counts, or tied to an observable user-behavior check?

5. If the gap check reveals a two-sprint punt on the same feature, what happens mechanically? Halt sprint planning? Rescope? Mark the feature paused? This is a soft-warning vs. hard-block decision.

### Cluster B: The human-AI interface artifact

6. Does the Judgment Frame live at the story level, the feature level, or both? Analysts lean toward both (per-story rolls up to per-feature); challengers argue per-story human artifacts waste effort. A decision here cascades into intake, create-story, sprint planning's review display, sprint-dev's Phase 6, and retro's closure questions.

7. If the Judgment Frame is per-story, at which phase is it produced — intake (fresh human context, cheapest to capture), refinement/create-story (standard rich elaboration moment), or sprint planning (closest to the go/no-go commit)? Each placement has different consequences for who writes it and what source material seeds it.

8. Is the user-story sentence form ("As a / I want / so that") adequate as a seed, or is it actively harmful because it frames thinking at the wrong grain? The triage challenger argues the research treats this form as explicitly insufficient and potentially counterproductive.

9. Where do anti-goals live in the data model? Every findings file raises anti-goals as missing, but no two propose the same home. A structural answer is needed because anti-goals that only exist in prose drift.

10. Does the feature become the primary human-review surface, in the sense that sprint-close reviews roll up to features rather than walking through stories?

### Cluster C: What to stop vs. what to add

11. Is AVFL earning its keep at the planning stage and at the sprint-dev Phase 4 stage? What class of defects has AVFL caught that a linter + "does the app build" check would have missed? If the answer is mostly cross-file coherence and AC-implementation mismatches, those are drafting-stage issues, and the multi-phase review apparatus is expensive for what it catches.

12. If the Codecentric isolated-agent behavioral harness is built (`.claudeignore`, symmetric permissions, isolated tester, Playwright MCP against running app), which existing skills stop doing work they currently do? Does Phase 4 collapse? Does E2E-validator shrink to a thin coordinator? Is the "why not both" answer actually affordable?

13. Is the four-agent retro auditor team over-engineered for solo practice? The retro challenger argues a single synthesis pass plus human-plus-transcript-extracts would produce equivalent signal at fraction of the cost.

14. Should `epic-grooming` remain a standalone skill, or fold into `refine`? Epic-grooming is pure taxonomy cleanup — no value mapping.

15. Should distill run continuously (at story merge, at intervention, at failure) rather than as a sub-step of retro? Both retro findings endorse this shape — it's the clearest single "move the valuable primitive out of the ceremony" proposal in the entire analysis.

### Cluster D: Sequencing and dependencies

16. If feature-as-human-judgment-unit is adopted, the data model changes first: stories carry `feature_slug` as first-class, features carry `north_star` and `floor_status`, `create-story` reads `features.json`. Is this the necessary-first-step that must ship before any phase redesign begins? Multiple findings argue intake redesign without this is "a well-designed collector for a system that still can't say what it's collecting toward."

17. Is there a credible path that redesigns one phase at a time, or do the five phases need to move roughly together? The dependency graph is dense: triage's North Star check depends on features having North Stars; refinement's Judgment Frame depends on a grain decision (story vs. feature); sprint-planning's gap check depends on floor state; sprint-dev's behavioral harness depends on red-phase specs; retro's gap-close check depends on prior phases having declared gaps.

18. What happens to existing in-flight sprints and backlog items during any transition? If intake's schema changes, what becomes of current stubs? If stories gain a `feature_slug`, who backfills?

19. What is the minimum redesign that delivers the value-floor check without rearchitecting the whole cycle? Is it real — add a North Star field and a gap-check step — or does the value floor need the full Judgment Frame redesign beside it to be legible?

20. Is there a kill-criterion for the current practice? If after N sprints of any redesign the spec-correct/value-zero pattern continues, what changes — another phase redesign, a deeper rearchitecture, or a retreat to Shape Up / pitch-first / no-backlog operation?

---

## Trade-Off Map

The findings converge on a handful of load-bearing options. Each is presented with what it would improve, what it would cost, what else must be true, and what question must be answered first. No preferred option is indicated.

**Option 1 — Add a North Star field to features and gate sprint planning on it.**

- For: closes the most commonly-raised gap across all 10 files; creates the missing pre/post-floor distinction; provides a concrete answer to "are we pointed at value?" that every phase can consume.
- Against: requires features to have North Stars before the feature has been built, which the refinement challenger flags as bootstrap-ahead-of-walking-skeleton; adds a gate that could produce ceremony if not carefully scoped; a poorly-articulated North Star creates false confidence.
- Dependency: some skill owns North Star creation — feature-grooming is the obvious home but would need schema extension.
- Open: what defines the North Star in a way that reliably distinguishes minimum-viable from full-vision?

**Option 2 — Add a Judgment Frame block to stories, produced at create-story or intake.**

- For: directly addresses the owner's explicit "human readability optimized section" framing; provides the glanceable artifact the research identifies as the field's unsolved problem; creates a review anchor at every story regardless of pipeline depth.
- Against: adds an artifact per story — at AI velocity that's 5–10x more frames to read than features would produce; may degrade to boilerplate if not actually used; duplicates some content already in the feature's value_analysis.
- Dependency: a decision on whether the Frame is per-story, per-feature, or both (Question 6).
- Open: what's the source material? The feature's value_analysis + epic section + the conversation? Or the user-story sentence extracted from intake?

**Option 3 — Build the Codecentric isolated-agent behavioral harness.**

- For: the research's highest-leverage single recommendation; directly addresses validation independence; defends against CAISI-style cheating; would produce the first genuinely uncorrelated quality signal in the Momentum pipeline.
- Against: engineering cost is real (.claudeignore, symmetric permissions, tester configuration, Playwright MCP integration, self-test); may reduce the value of AVFL Phase 4 enough that its removal becomes forced; no open-source reference implementation exists.
- Dependency: Gherkin specs being executable rather than narrative; sprint closure requiring a running app, which may not be true for skill-authoring sprints.
- Open: which subagent pattern is isolated? What does "the running app" mean for sprints that change skill SKILL.md files rather than application code?

**Option 4 — Move distill out of retro and onto continuous hooks.**

- For: makes the valuable primitive immediately-applied rather than weekly-batched; reduces retro's own ceremony cost; aligns with the research's "on-the-loop harness engineering" pattern.
- Against: requires hook infrastructure (per-story merge, per-failure, per-intervention); distill fired too eagerly could flood rules files with low-signal additions; loses the synthesis-across-a-sprint that the four-agent auditor team produces.
- Dependency: retro's job description changes (becomes a thin audit of distill fidelity rather than primary distillation surface).
- Open: what triggers distill on continuous hooks without producing noise?

**Option 5 — Replace story-count sizing (3–8) with appetite (ordinal time commitment).**

- For: Shape Up-aligned, research-endorsed, enables the single-walking-skeleton-story sprint the 3-story floor currently forbids; gives the sprint a declared time-box retro can evaluate against.
- Against: appetite is a forcing function on the practice's rhythm — if the practice does event-driven sprints today, moving to declared appetite may add ceremony without yield.
- Dependency: a weekly cadence decision.
- Open: does the owner want time-boxed sprints, or does event-driven variable-length serve the solo practice better?

**Option 6 — Pre-sprint gap artifact + sprint-close gap check.**

- For: directly operationalizes the here-to-there gap the owner described; produces a structured artifact the retro can evaluate against; creates a continuous reference across sprints.
- Against: adds a planning-phase artifact; only pays off if multiple sprints on the same feature actually occur; may be redundant if Options 1 and 2 are also taken.
- Dependency: the North Star field being in place (Option 1).
- Open: does the gap artifact go in the sprint record, the feature record, or a new per-feature tracking file?

**Option 7 — Tier create-story into light and full shapes.**

- For: addresses the refinement challenger's over-specification argument; matches the research's appetite-per-work-unit position; reduces curse-of-instructions exposure on small stories.
- Against: adds a classification decision (which tier?) that could itself become ceremony; may cause drift between story shapes that makes downstream agents behave inconsistently.
- Dependency: a reliable classifier for which stories are small; current `change_type` is close but not the same dimension.
- Open: does the tier affect only Dev Notes / Implementation Guide density, or does it also affect AVFL coverage, review depth, and DoD strictness?

**Option 8 — Fold epic-grooming into refine.**

- For: removes one orchestration layer; epic-grooming does pure taxonomy with no value mapping; the savings are real.
- Against: couples taxonomy work into a skill that is already 11 steps; if refine is itself due for consolidation, this adds load to the wrong place.
- Dependency: `refine`'s own redesign plan.
- Open: how often does epic-grooming actually fire in practice, and does its interactive MERGE/CREATE/SPLIT UX earn its cost?

---

## Where Analyst and Challenger Disagreed

**Triage.** Analyst sees intake as under-scoped (add Judgment Frame, feature assignment, anti-goals); challenger sees it as misframed (`momentum:shape` should be the front door; not every idea becomes a story). Nature: severity — gap to fill vs. category error. The challenger proposes `intake` collapse into a shaping skill; the analyst proposes extension.

**Backlog Refinement.** Analyst treats feature-grooming's value_analysis as rich raw material to exploit; challenger treats it as a descriptive catalog entry that isn't a judgment instrument. Nature: cause vs. symptom — the analyst sees the feature layer as structurally close to right, needing connection to stories; the challenger sees it as structurally wrong (inventory-shaped when it should be judgment-shaped).

**Sprint Planning.** Analyst accepts the 10-step workflow as a reasonable base to extend; challenger argues the ceremony is calibrated to team-scale Agile and doesn't survive comparison to one-week governance + continuous flow. Nature: scope — does the current workflow deserve fidelity or replacement?

**Sprint Dev.** Analyst's removal candidates are surgical (consolidate Phases 4 and 4b); challenger explicitly proposes removing the AVFL Phase 4 apparatus and replacing it with a value-floor gate and running-app demonstration. Nature: what failure mode is the gate defending against? Both agree AVFL doesn't target the research's named failure mode; they disagree on whether to preserve the gate after refocusing.

**Retrospective.** Analyst endorses the four-agent auditor team as role-boundary-by-construction (Agentsway-aligned); challenger calls it "a freight train hauling a sandwich" in a solo context. Both endorse distill as the valuable primitive; analyst wants inline ternary routing, challenger wants distill promoted out of retro entirely onto continuous hooks. Nature: does the team retrospective shape make sense in solo practice at all?

---

## Convergence Summary

Findings where both analyst and challenger agreed in all or most phases — the most robust signals from the analysis:

- The value floor / North Star capability statement is missing from every phase, and every phase is where someone argues it should go. This is the single most robust signal in the entire analysis.
- The Judgment Frame (the owner's "human readability optimized section") exists nowhere in the practice today. The gap is named consistently across intake, create-story, sprint-planning, sprint-dev, and retro findings.
- The feature layer (features.json, feature-grooming, feature-status) is disconnected from the cycle that operates on it. `features.json` is never read by intake, never read by create-story, never invoked by sprint-planning, never mutated by retro.
- The Codecentric isolated-agent behavioral validation pattern is declared in sprint-dev's critical rules but enforced only by prose, not by `.claudeignore` or permissions. Every finding that touches validation raises this. CAISI agent-cheating findings apply.
- AVFL and downstream reviewers share substantial context with the implementer, producing correlated rather than independent signal. Both sprint-dev pairs and both retro pairs converge on this.
- Distill is the most valuable single primitive in the retro (possibly in the whole practice), and it is currently buried behind multiple gates instead of running on continuous hooks.
- The 3–8 story-count floor has no research basis in the corpus and is cargo-culted from two-week Scrum team planning.
- The DoD checklist is almost entirely structural (tests pass, frontmatter valid, AVFL noted) and never asks whether user-observable behavior changed.
- Every owner review gate in sprint-dev is post-implementation recognition mode; the research's highest-leverage review (before the spec goes to the AI) has no gate anywhere in the practice.
- Sprint close summaries report velocity-adjacent metrics (stories done, findings count, scenarios confirmed) and no flow metrics (cycle time, lead time) or value metrics (capability delivered).
