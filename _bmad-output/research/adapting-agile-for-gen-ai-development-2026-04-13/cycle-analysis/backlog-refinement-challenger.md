# Backlog Refinement Phase — Challenger Findings

## Executive Summary

Momentum's Backlog Refinement phase — `refine` + `epic-grooming` + `feature-grooming` + `create-story` — is a well-engineered, well-separated pipeline whose parts are individually defensible but whose **whole is structurally aimed at the wrong target**. It is optimized for producing AI-executable stories with clean taxonomy. It is not structurally optimized for the three things the research says matter most in AI-native development:

1. **Human-at-a-glance judgment.** None of the four skills produces a "glanceable-correctness" artifact. `create-story` injects increasingly dense Implementation Guide content into an already-dense story file; it does not produce the Judgment Frame (Intent / Done-state-you-could-show-a-stranger / Anti-goals / Review focus) the research identifies as the owner's central unsolved problem.
2. **Value-floor discipline.** Nothing in the pipeline asks "can a user derive value from this feature when it ships?" `feature-grooming` produces a value_analysis string, but it is a *descriptive* artifact (what the feature delivers in theory) not a *gating* artifact (does the current backlog path close the gap to the North Star capability?). The pre-floor/post-floor distinction does not exist.
3. **Elaboration economics.** The pipeline structurally rewards more specification, not less. `create-story` + `bmad-create-story` + Implementation Guide injection + AVFL checkpoint is a multi-pass elaboration process even for small changes. The research's clearest warning — Kiro generating 16 AC for a single bug fix, the curse-of-instructions performance degradation, MDD's failure mode — applies here with force.

The pipeline's strongest asset is also its weakest: **separation of concerns is real and the skills do distinct work**, but they all answer variants of the same question ("is this specific enough for the AI?"). None of them answer "is this the right thing to build at this moment in the product's life?"

The owner should not refactor the pipeline to produce "better" stories. The owner should add a **human-judgment layer that sits above the pipeline and can veto the whole thing** before any story is written — and remove specification depth that cannot pay for itself.

---

## Assumed Truths That The Research Questions

### Assumed: "A refined backlog is one with clean taxonomy, good acceptance criteria, and sprint-ready stories."

**The research says:** A refined backlog is one where the *next* thing to build closes the value-floor gap. Taxonomy hygiene is second-order. Fowler/Böckeler's critique of SDD, Kurilyak's dual-horizon framing, and the whole value-floor problem all imply that cleanliness of the artifact is downstream of correctness of the target. Momentum's refinement pipeline is beautifully obsessive about cleanliness — `epic-grooming` deduplicates slugs, `feature-grooming` ensures every feature has a multi-paragraph value_analysis, `refine` checks assessment staleness — and does not once ask "if we shipped what is in this backlog, would a user cross the value floor?"

### Assumed: "More structured specification → better AI output."

**The research says:** False past a threshold. Kiro generated 16 AC for one bug fix. The curse of instructions degrades model performance beyond a simultaneous-requirements threshold. `create-story`'s Implementation Guide injection (EDD-or-TDD-per-task-type, NFR compliance checklists, DoD additions, black-box separation reminder, AVFL checkpoint, Gherkin reference) is exactly the spec-inflation pattern the research warns against. The correct answer per Fowler's Context Engineering article is **accretive context (rules files, memory) + minimal per-story delta**, not per-story restatement of standards the global rules already enforce.

### Assumed: "Stories are the unit of AI execution and human review can happen elsewhere."

**The research says:** Half right. The owner's framing is explicit about this ("Stories are AI execution artifacts; features/epics are human judgment artifacts") and the research strongly validates the bifurcation (Kurilyak, OpenAI PR-as-unit, Shape Up). But the *human judgment artifact doesn't exist yet*. Feature-grooming produces a value_analysis field in features.json — a JSON dict with strings — which is not a judgment artifact. It is a catalog entry. The research's offered shape (PR Contract components moved upstream to the spec phase: Intent / Observable done-state / Anti-goals / Review focus) is absent from every skill in the pipeline.

### Assumed: "feature-grooming is the value-mapping layer."

**The research says:** `feature-grooming` produces a feature *inventory with value_analysis annotations*. That is not value mapping. Value mapping (Adzic Impact Maps, Torres outcome-based roadmaps, JTBD) is **causal**: it traces how a feature produces a business outcome via user behavior change. feature-grooming's value_analysis is a descriptive paragraph the developer approves holistically — there is no causal chain from feature → user behavior → outcome. And crucially: there is no gate that says "this feature is below the value floor, do not plan sprints against it until the skeleton exists."

### Assumed: "The pipeline is a pipeline."

**The research says:** In practice, yes — `refine` → `epic-grooming` → `feature-grooming` → `create-story` is the order documented in the practice. But the skills don't share a coherent theory of what each one is *uniquely* contributing. They share a theory of what to clean up (orphaned slugs, stale descriptions, missing value_analysis, unwritten stories) but not a theory of what the backlog is *for*. This is why Redundancy Audit (below) finds each skill answering a subtly different variant of the same question.

---

## The Value Floor Risk

The research problem 4 (Value Floor) is the single most important challenge to this pipeline, and the pipeline has **zero structural defense against it**.

### Where value-floor questions should be asked (and aren't)

1. **feature-grooming Step 4 (value_analysis production).** The value_analysis has three paragraphs: current value, full vision, known gaps. None of these paragraphs ask "what is the minimum end-to-end capability a user needs before any of this matters?" The "current value" paragraph describes what exists; the "full vision" describes what is possible; the "known gaps" describes what is missing. **Missing a fourth paragraph: the North Star capability — the minimum thing without which everything else is zero-value.** This is not the same as any of the three.

2. **refine Step 7 (re-prioritization).** The four heuristics — recurrence, workaround burden, forgetting risk, dependency — all reason about *pain removal* and *dependency unblocking*. None of them reason about *value-floor proximity*. A story could be high-priority by all four heuristics and still be pre-floor elaboration on a skeleton that doesn't exist.

3. **refine Step 8 (assessment & decision review).** Checks ASR/SDR freshness, decision-gate readiness, unresolved next steps. Does not ask "does the current backlog close the gap to the North Star capability?" A perfectly healthy assessment-decision state is compatible with a backlog that punts the value floor indefinitely.

4. **create-story.** Operates one story at a time. By design cannot see the value floor — the question is a feature-level or product-level question, not a story-level one. But `create-story` is where stories enter the execution pipeline, so if the gate doesn't exist upstream, create-story will happily produce a perfectly-specified pre-floor elaboration.

### The deferred-value flag is the near miss

`feature-grooming` has a `⚠ Deferred value` flag for features where "all value is deferred/aspirational." This is the closest the pipeline comes to a value-floor mechanism — and it operates at the wrong level. It flags features whose *entire* value is deferred (so the developer can confirm inclusion) but does not flag the *composition* problem: a product where three features are partially built and none has crossed the floor. The flag is a feature-level sanity check, not a product-level gap check.

### What's structurally needed

A **pre-floor / post-floor state** on each feature in `features.json`, plus a **gap check** that runs at the start of refinement: "For each pre-floor feature, does this sprint's candidate backlog close the gap or elaborate around it?" If elaborate-around, flag it before sprint planning begins. This is a refinement-phase concern (the backlog is being shaped, not yet committed), and it should gate feature-grooming output — not decorate it.

---

## Overbuilt vs. Underbuilt

### Overbuilt

**1. create-story's Implementation Guide injection.**

Every story — regardless of size — receives a full Momentum Implementation Guide appended to its Dev Notes, with per-task change-type classification, EDD-or-TDD guidance, NFR compliance checklists, DoD additions, and a reminder about Gherkin black-box separation. For a five-line config change this is overhead that dwarfs the change. For a skill creation it is sensible. **The pipeline does not differentiate.**

The research warning on this exact pattern is unambiguous. Fowler/Böckeler: Kiro generated 16 AC for a single bug fix. The curse of instructions degrades model performance past a threshold. Fowler Context Engineering: build context gradually, not all up front. **The right answer is accretive global rules + a per-story delta that omits what global rules already enforce.** Momentum has the global rules (`.claude/rules/`) but `create-story` restates enforced-elsewhere standards per story anyway.

**2. feature-grooming's mandatory three-paragraph value_analysis.**

Every feature must have a multi-paragraph value_analysis with current value / full vision / known gaps, plus system_context, plus type classification (flow/connection/quality), plus acceptance_condition. This is a rich inventory entry. It is also the kind of artifact that ossifies — once written, it becomes a fixed reference that specifications align to, and the research is explicit about MDD's failure mode of spec-as-source.

Worse: the richness is uniform across features regardless of whether the feature is pre-floor (where description is premature) or post-floor (where detailed value_analysis has a natural home). A walking-skeleton feature needs one sentence (the North Star capability); feature-grooming demands three paragraphs.

**3. refine's 11-step workflow.**

Eleven steps, each with its own TaskCreate entries, for a skill described as "backlog hygiene." The stories being managed are themselves work units; the meta-work of managing them should be lighter than the work of building them. The refine workflow has taxonomy, status hygiene, epic delegation, stale-story evaluation, four-heuristic re-prioritization with back-and-forth conversation, assessment/decision review with gate-ready detection, consolidated batch approval UX, change application, and summary. For a solo practitioner the ceremony-to-value ratio is inverted relative to what the research supports.

The research's closest analog: Shape Up *eliminates backlog grooming* on principle. The 6-week cycle doesn't have a grooming ceremony because "if an item didn't win its cycle, it drops off and has to be re-pitched." This is an extreme the owner shouldn't adopt — but it is the polar opposite of what Momentum does, and the owner is closer to Shape Up's target (solo, AI-first) than to enterprise-team context where heavy grooming pays for itself.

**4. epic-grooming's MERGE/CREATE/SPLIT proposal-per-change-approved-individually UX.**

Epics are long-lived categories. The overhead of proposing each MERGE, then each CREATE, then each SPLIT individually to the developer, with Modify branches and per-proposal approval, is an interaction burden that's hard to justify for what is essentially taxonomy cleanup. The research has nothing specific to say about epic taxonomy (it's below the framework's radar) but the general principle — ceremony must pay for its cost — applies. A 10-orphan-slug cleanup with MERGE proposals for each is 10 gated conversations.

### Underbuilt

**1. The Judgment Frame.**

Zero skills produce it. The research identifies this as the owner's central unsolved problem. `create-story` injects an Implementation Guide *for the AI*; it should also produce a Judgment Frame *for the human*. The absence is the single largest gap in the refinement phase.

**2. The North Star capability per feature.**

`feature-grooming` produces value_analysis but not a North Star capability statement (the one sentence that defines the value floor). This is a small-text addition — one field in each features.json entry — but it is structurally load-bearing. Without it, the pre-floor / post-floor distinction cannot be computed.

**3. The gap check.**

No skill runs a gap check. At minimum: "For each feature with status != done, is the current backlog trajectory closing the gap to the North Star capability?" This belongs at the top of `refine` (before taxonomy or re-prioritization) and should surface gap-expanding sprints as a red flag.

**4. Size-appropriate story shapes.**

The research is explicit that no single story shape fits the solo-AI-first practitioner and the taxonomy of sub-feature work units is in flux (Bolts, Agent Stories, Super-Specs, Context Capsules, Impact Loops). `create-story` produces one shape for every story. Small fixes, medium features, and platform changes all get the same Implementation Guide structure. At minimum the pipeline should support a **light story** (appetite-sized, Judgment Frame only, no per-type EDD/TDD injection) for small work, reserving the full treatment for AI-reliability-critical cases.

**5. The "should we not build this?" moment.**

There is no structural prompt to kill a story rather than refine it. `refine` has "drop stale low-priority backlog stories" — but that's waste cleanup, not redirection. Shape Up's discipline ("no unshipped — work that doesn't ship is cut, not carried") has no equivalent. A feature whose value_analysis was approved six months ago is not re-evaluated against current product state unless the developer raises it.

---

## Structural Misalignments

### Misalignment 1: The pipeline optimizes the wrong predicate

Every gate and approval in the pipeline answers variants of *"is this specification adequate?"*:
- `refine` status hygiene: is the status adequate given the DoD state?
- `epic-grooming` taxonomy: is the epic assignment adequate?
- `feature-grooming` value_analysis: is the feature's description adequate?
- `create-story` AVFL checkpoint: does the story adequately capture epic intent?

None of these ask *"is this the right thing to build now?"* — which is a different predicate entirely. The research is unambiguous: in AI-native development, the constraint has moved upstream to the *what to build* question. The whole pipeline is pointed at the downstream question.

### Misalignment 2: Feature-grooming bootstraps ahead of walking skeleton

`feature-grooming` in bootstrap mode creates aes-NNN and dec-NNN foundation docs and an 8–25-feature taxonomy with full value_analysis for each feature **before any feature has crossed the value floor**. The research strongly argues (XP walking skeleton, Shape Up appetite) that elaboration should follow skeleton, not precede it. Momentum does it in the opposite order: define the full taxonomy up front, then build one slice at a time.

The counter-argument (the developer needs the taxonomy to plan sprints) has merit but is undermined by the fact that the taxonomy is *retrospective* in feature-grooming — it reads architecture.md and stories/index.json to find feature clusters. If the retrospective is the real source of truth, the upfront bootstrap is the overbuilt part.

### Misalignment 3: create-story delegates to bmad-create-story and then adds Momentum-specific layers

The workflow is explicit: "Invoke `bmad-create-story` for all context extraction — do not re-implement its logic." `bmad-create-story` does "epic analysis, architecture extraction, web research, previous story intelligence, git analysis, Dev Notes population, sprint status update to ready-for-dev." Then `create-story` classifies change types, injects an Implementation Guide, writes stories/index.json metadata, and runs AVFL.

This is reasonable separation. But the **total work per story** is now: epic analysis + architecture extraction + web research + previous story intelligence + git analysis + Dev Notes population + change-type classification + Implementation Guide composition + index metadata + AVFL checkpoint. For a solo practitioner making a small change, this is the literal opposite of the Shape Up "appetite" discipline. No story exists that skips most of this — and many should.

### Misalignment 4: AVFL checkpoint validates story against epic, not story against user value

The AVFL invocation in create-story uses "the relevant epic section for {{story_key}} from epics.md" as source_material. This is a consistency check (does the story spec correctly capture epic intent?) — not a value check (does the epic itself correctly describe what the user needs?). The upstream source (epic) is treated as authoritative. But the research's value-floor critique is exactly that the epic itself may be pre-floor elaboration. **AVFL cannot catch what the epic doesn't ask.**

### Misalignment 5: The "spec-as-source" drift

Momentum's refinement pipeline moves the practice toward Fowler/Böckeler's *spec-anchored* level (specs persist and are enforced via tests/AVFL) and edges toward *spec-as-source* (specs are primary, code is regenerable). The research explicitly warns: "spec-as-source risks combining MDD's inflexibility with LLMs' non-determinism — worst of both worlds." The Implementation Guide injection, the AVFL checkpoint, the mandatory index.json metadata — each is individually defensible, but together they make the story a heavyweight, authoritative, long-lived artifact. MDD failed because the model couldn't evolve as fast as reality. Momentum stories are approaching the same brittleness unless the pipeline is balanced by a counter-pressure (lighter story shapes, the Fowler accretive-context alternative).

---

## The Feature Layer Question

The owner's model: *"Stories are AI execution artifacts; features/epics are human judgment artifacts."* The research backs the bifurcation. The challenge is whether the *feature* as currently modeled in Momentum actually performs human judgment.

### What feature-grooming produces

A features.json entry with:
- slug, name, description, type (flow/connection/quality)
- value_analysis (3 paragraphs)
- system_context (1–2 sentences)
- acceptance_condition (one string)
- status (working/partial/not-started)
- stories array + derived counts
- notes, last_verified

### What a judgment artifact needs

Per the research:
- **North Star capability** (1 sentence): the minimum thing a user must be able to do for this feature to have any value at all.
- **Observable user behavior change** (JTBD): what can a user do after this feature ships that they could not before?
- **Pre-floor / post-floor state**: categorical, not continuous.
- **Anti-goals**: what this feature is *not* doing (to counter AI's add-plausible-adjacent-features failure).
- **Review focus**: the 1–2 specific questions a reviewer answers after running the build.
- **Gap artifact linkage**: how does closing this feature close the gap to the product's value floor?

### The delta

The feature-grooming schema is **richer than needed in some places** (the three-paragraph value_analysis is a descriptive essay) and **poorer than needed in others** (missing North Star, JTBD behavior change, anti-goals, review focus, gap linkage). It is a catalog, not a judgment instrument.

The correct move is not "add more fields." The correct move is to **re-task the schema toward judgment** — replace the descriptive value_analysis with the North Star + observable behavior change, and drop what doesn't serve that purpose. The research is clear that expanding the spec is the trap.

### The feature-status HTML mockup is a tell

The repository has `.claude/momentum/feature-status-mockup.html` as an untracked file. The existence of a mockup for *rendering* feature state suggests the developer is already trying to solve the visibility problem — how can I see the features at a glance and make judgments? The research validates this instinct. The challenge is whether the current features.json schema feeds a judgment UI or an inventory UI. On current evidence: inventory.

---

## Hard Questions for the Owner

These are the questions the research and the current pipeline design imply should be answered before further investment in the refinement phase.

### 1. What is the human-at-a-glance artifact, and where is it produced?

`create-story` produces a Momentum-optimized story for the AI. What produces the Judgment Frame for you? When a story is generated, what is the 5–10 line block you read to decide "yes, this is the right thing"? If the answer is "the AC" — the research says that is not sufficient. If the answer is "the value_analysis in features.json" — that's a feature-level artifact, not a story-level one, and it's descriptive not observable. What is the story-level judgment artifact, and which skill produces it?

### 2. Can any skill in this pipeline veto the whole backlog?

`feature-grooming`, `epic-grooming`, `refine`, `create-story` — each can modify a piece. Can any of them output: "Stop. The current backlog is elaborating around a value-floor gap. Do not plan sprints against this feature until the skeleton exists"? On current evidence, no. Should one?

### 3. Why does every story get the same Implementation Guide?

The research says over-specification past a threshold degrades output. The Implementation Guide is 30–100 lines of per-task type guidance for every story. Is there empirical data from your AVFL findings and retros that shorter, lighter stories perform worse? If not, why is the heavy shape the default?

### 4. Is feature-grooming's bootstrap mode premature?

Running bootstrap produces 8–25 features with full value_analysis before any feature has crossed the value floor. Would the practice work if the first feature was built as a walking skeleton and feature-grooming ran in refine mode after that — treating the taxonomy as retrospective rather than predictive?

### 5. Where is the moment you judge "is this the right thing to build?"

Walk the pipeline. refine/epic-grooming/feature-grooming/create-story. At what step do you make a value judgment about product direction versus a hygiene judgment about backlog shape? If the answer is "Step 7 of refine (re-prioritization conversation)" — is that conversation grounded in the value floor or in the four heuristics the skill computes? The heuristics are pain-reduction and dependency metrics; the value floor is a different frame entirely.

### 6. What would it cost to kill a story, versus refine one?

`refine` has a "drop stale low-priority backlog" path. Does it have a "drop a feature that no longer serves the product direction" path? Shape Up's "no unshipped" discipline cuts work that didn't ship. Does any Momentum skill cut work that no longer makes sense even though it hasn't shipped?

### 7. Is AVFL checking the wrong invariant?

AVFL in create-story uses the epic as ground truth for validating the story. What validates the epic? If the answer is epic-grooming, epic-grooming validates *consistency and taxonomy*, not value. The chain of validation is: story ↔ epic ↔ (nothing). The top of the chain is unexamined. Is this an accident or a design decision?

### 8. Does feature-grooming's features.json belong in the pipeline at all, or does it belong as a sprint-close judgment artifact?

Current placement: bootstrap produced early, refined periodically, fed to sprint planning. Alternative placement: produced/updated at sprint close as the developer's judgment record ("here is what I believe about the product after this sprint") and consulted before sprint planning as a reference — but not the primary value-judgment surface during refinement. The research pushes the judgment moment to **before the story is written** (the Judgment Frame) and **at sprint close** (the gap check and value-validation gate). What is features.json doing during refinement proper?

### 9. Have you measured the cost of this pipeline?

The refine workflow has 11 steps with TaskCreate tracking. feature-grooming runs 2 haiku subagents and has a 6-step workflow with approval gates. epic-grooming has 4 phases with per-proposal approval. create-story delegates to bmad-create-story (which itself has multiple stages) and adds 7 post-steps. For a single medium-sized story traversal (intake → refined → created), what is the wall-clock time? The token cost? If you don't know, what should the pipeline look like when you do know?

### 10. Are the four skills four distinct values, or a single grooming operation in four pieces?

Refine Step 5 delegates to epic-grooming. Feature-grooming and epic-grooming both analyze taxonomy (features vs. epics). Create-story is the only one that crosses into story creation (the others don't write stories at all). If you were rebuilding the practice fresh and knew what you know now, would you collapse three of these into one skill and keep create-story separate? Or is the separation load-bearing in a way that isn't visible from the outside?

---

## Final Note

The pipeline is well-engineered. The skills are well-separated. The workflows are disciplined. None of that is the critique.

The critique is that **engineering quality at the skill level cannot substitute for alignment at the practice level**. A backlog refinement phase that is exquisitely thorough at hygiene and silent on value-floor alignment is not a neutral tradeoff — the research is explicit that AI-native practices will systematically produce spec-correct / value-zero outcomes without a value-floor gate. Momentum does not have that gate. The refinement phase is where the gate belongs.

The path forward is not "more pipeline." It is a shorter pipeline with a stronger front door: a judgment-first gate (does this backlog close the gap?) and a judgment-first artifact (the Judgment Frame per story, the North Star per feature), backed by fewer and lighter grooming steps that defer to global rules instead of per-story restatement. The owner's existing instincts (the feature-status mockup, the decision to keep stories as AI artifacts, the rules/hooks architecture) are correctly aimed. The refinement phase needs to follow that instinct further than it currently does.
