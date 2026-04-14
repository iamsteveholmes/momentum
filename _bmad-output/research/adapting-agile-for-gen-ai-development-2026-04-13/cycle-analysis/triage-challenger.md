# Triage/Intake Phase — Challenger Findings

## Executive Summary

- **Intake is a stenographer, not a gate.** The current skill captures title, role, action, benefit, rough ACs and writes a stub to `backlog`. It asks one judgment question: *which epic?* It does not ask the only question the research says matters at this phase: *does this item move the system toward the value floor?* In the research's own terms, Momentum has built a very tidy way to queue pre-floor punts.
- **The stub template codifies the anti-pattern the research warns against.** Nine DRAFT sections (ACs, Tasks/Subtasks, Dev Notes, Architecture Compliance, Testing, Implementation Guide, Project Structure, References, Dev Agent Record) are placeholder-stamped and handed to `create-story`. This is upfront-spec completeness theatre for work that may never deserve a spec — exactly the Kiro "4 stories, 16 ACs for a bug fix" over-specification failure, applied preemptively to every passing idea.
- **The "human judgment" output is ordering-by-epic, not value.** The Judgment Frame the research says is missing (Intent / Done-state-for-a-stranger / Anti-goals / Review focus) is nowhere in the intake artifact. Intake collects a user-story sentence fragment (`As a… I want… so that…`) — the research explicitly calls this *insufficient* as a human-judgment artifact and identifies it as a root cause of the AC-mis-review problem downstream.

## Assumed Truths That The Research Questions

1. **"Ideas captured in conversation belong in a backlog."** The synthesis quotes Shape Up and the DORA rework: Shape Up explicitly has *no backlog grooming*. Ideas live as pitches until shaped. Intake assumes the opposite — every idea mentioned gets a slug, an index entry, an epic assignment, and a reserved file path. The research calls backlog-grooming-as-discipline a traditional-Agile artifact for a problem (throughput planning) that no longer exists.

2. **"The human-story sentence is the right frame for capture."** Intake treats `As a {role}, I want {action}, so that {benefit}` as the canonical extraction target. The research is explicit: user-story sentences are acceptable as a *seed* but fail as a human-judgment artifact. The missing artifact is the Judgment Frame — Intent / Done-state-for-a-stranger / Anti-goals / Review focus. Intake has no slot for any of the four.

3. **"The AI work unit and the human work unit are the same artifact in two states."** The stub → `create-story` pipeline assumes a stub "grows up" into a dev-ready story. The research directly contradicts this: "the story is the AI's unit; the feature — or the shaped pitch — is the human's unit. Whatever goes on the story is there for the AI; whatever a human reviews should be at a coarser grain." Momentum's intake starts from the wrong base unit and has no mechanism to promote ideas *upward* into feature/pitch form before committing them to a story slug.

4. **"Priority, epic, and user-story structure are known at capture time."** Intake asks the user to pick an epic, assigns a priority (default `low`), and extracts ACs. Kurilyak's dual-horizon planning and Fowler's context engineering both argue the opposite: at capture time, the most important facts are the outcome, the anti-goal, and the discovery gap — none of which intake captures. Epic and priority are downstream concerns that shouldn't be answered at the point of *maximum ignorance* (the research's phrase).

5. **"Capture should be fast and minimal."** The SKILL.md brags about "1 read, 1 write, 1 bash, no subagent spawns." This is a developer-experience optimization. The research says the highest-leverage decision the practice can make is *moving review forward* — before the spec goes to the AI. Intake is the last structural chance to do that, and it explicitly chooses speed over judgment. The three friction-reducers (no analysis, no research, no subagent) optimize the one place in the cycle where friction has the most leverage.

6. **"Every captured idea becomes a story."** Intake has no mechanism for the two most useful outcomes of a triage conversation: (a) "this is actually a feature, let's shape it, not story-ify it" or (b) "this is not worth doing — close without queueing." There is no "reject" path, no "shape instead" path, no "merge into existing" path. The only exits are `backlog` or ask-the-user-for-a-different-slug.

## The Value Floor Risk

Intake is a value-floor risk amplifier, not a mitigant.

The research's core failure mode: "After 5-10 sprints we're still NOT there. You keep punting to the next sprint and the next sprint, delivering versions with no value." The structural cause: individual sprint success gates ask "did we implement the spec correctly?" and never ask "are we closer to the destination?"

Intake is the first place the question *could* be asked and is the last place it *is* asked. Concretely:

- **No North Star capability check.** Intake does not ask: "Does this item move the system across the value floor, elaborate past it, or ignore it?" There is no field for `pre_floor_relevance` or `north_star_contribution`. The workflow has no check — explicit or implicit — that the captured item relates to *any* value statement.
- **No "here → there" gap context.** The research is explicit: the gap artifact (Here / There / Gap / Path check) is the missing practice. Intake reads `epics.md` to recommend an epic assignment — nothing else. It doesn't read the active feature's North Star, because there is no North Star to read.
- **`suggested_priority` defaults to `low`.** This is the most structurally damaging default in the skill. Every passing idea enters the system marked `low`, indistinguishable from every other `low` item. The work of sorting value happens later, during grooming. But grooming operates on a backlog, not on value — it merges and renames slugs, it doesn't ask "which of these closes the gap?"
- **Stubs accumulate faster than they're retired.** The skill is explicitly designed to make capture cheap. The downstream process (refine, epic-grooming, feature-grooming) is not designed to make deletion cheap. The ratio matters: easy in, hard out means the backlog grows faster than the value-floor-relevant subset gets identified.

**The consequence the research predicts:** Momentum can run 5–10 sprints pulling from a 200-item backlog, complete every story against its AC, and never cross any user's value floor, because nothing in the intake or planning gates binds work to the North Star capability. The `feature-grooming` skill has a `⚠ deferred-value flag` concept but that sits *above* stories and operates on already-captured features — it doesn't prevent low-value items from entering the backlog in the first place.

## Overbuilt vs. Underbuilt

### Overbuilt

- **The nine-section stub template.** DRAFT Architecture Compliance, DRAFT Testing Requirements, DRAFT Implementation Guide, DRAFT Project Structure Notes, DRAFT References, DRAFT Dev Agent Record — all reserved as placeholders at intake time. This is the "curse of instructions" made physical: the template tells the downstream AI what sections to expect, which pressures `create-story` to fill *all* of them whether warranted or not. Fowler/Böckeler's Kiro critique is the direct precedent: SDD tools generate full spec packages for trivial bug fixes because the template reserves the space.
- **The slug-conflict check at capture time.** A full read of `stories/index.json` to catch a slug collision is ceremony for an artifact that might never reach `create-story`. At intake stage the slug is a provisional label, not a load-bearing identifier. Uniqueness should be enforced at promotion (when the stub is picked up for development), not at capture.
- **Epic assignment as a capture-time requirement.** Step 2 reads `epics.md` and forces a choice. The research treats epics as long-lived categories (Momentum's own `epic-grooming` skill says the same — "Epics are categories — long-lived, never-closing groupings"). A capture-time idea does not need to be placed in a category to exist. Epic assignment during intake couples a fast activity (capture) to a slow activity (taxonomy judgment).
- **The CLI write to `stories/index.json`.** Every captured idea becomes a registered story with a status. The intake description says "fast context preservation" but the side effects are durable index registration, file creation, and commitment to a dev-ready trajectory. A lighter-weight artifact (a line in `intake-queue.jsonl`, which memory says is part of the redesigned model, or a free-form note) would preserve context without the trajectory commitment.

### Underbuilt

- **No Intent / Done-state-for-a-stranger / Anti-goals / Review focus capture.** The one artifact the research most strongly identifies as missing across all surveyed frameworks. Intake is the only place this can be captured cheaply (the human is present in the conversation). By the time `create-story` runs, the conversation is gone and the context is degraded.
- **No shape vs. story decision.** There is no step asking "is this a story, a feature, or a pitch?" A capture that's actually a feature-level concern gets reduced to a story-level stub, losing the outcome framing. The `feature-grooming` skill has to recover this later from architectural signals — an expensive inversion.
- **No anti-goal capture.** The research's Osmani reference: AI invents "file limits, permissions models, storage backends, security assumptions — all plausible, many wrong." Anti-goals are the specific defense against this. Intake has no field for "what this story is not."
- **No reject / merge / defer path.** The skill exits only to `backlog`. No triage decision tree. No "this is already captured in slug X, merge there." No "this is too vague to capture yet, come back when you can state a done-state."
- **No value-floor relevance flag.** The single most useful metadata the research identifies: `pre_floor | post_floor | unrelated`. With it, sprint planning can filter by what crosses the floor. Without it, every sprint is a gamble.
- **No link to a North Star.** If the feature this idea belongs to has a North Star capability statement (per the research's recommendation), intake should surface it and ask "does this idea move us toward that statement?" Intake doesn't read North Stars because they don't exist yet, but the feedback loop needs designing now.
- **No "walking skeleton" tagging.** The research's Sprint-1-targets-the-skeleton rule requires intake to distinguish skeleton-enabling items from elaboration items. Intake has no such distinction.

## Structural Misalignments

1. **Intake is at the front of the cycle; the research says human judgment belongs above the cycle.** The triage phase treats itself as "work entering the system." The research treats a properly-shaped pitch or outcome statement as *prerequisite to the cycle*. Intake should not be the first thing a new idea hits — shaping should be. Intake's current position institutionalizes the backlog-first culture the research explicitly warns against.

2. **Intake treats itself as an AI-speed activity ("minimize tool calls, no subagent spawns") but its role is a human-judgment activity.** The skill's preamble optimizes for speed. The work the research says needs doing at this phase — anti-goals, done-state-for-a-stranger, value-floor relevance — is exactly the work that *requires* slowing down. These are value-orientation questions, not extraction questions. Optimizing intake for speed is optimizing the wrong axis.

3. **The stub file is a write to a durable artifact store before a human judgment gate has been passed.** Once `stories/{slug}.md` exists and the index is updated, the item has institutional momentum. The research says the highest-leverage moment to say "no" is before the write. Intake's design makes the write the default outcome of any conversation that mentions a story.

4. **Intake doesn't read the feature layer, and feature-grooming doesn't read intake.** Feature-grooming reads `prd.md`, `epics.md`, `architecture.md`, `stories/index.json`, `features.json`. Intake reads only `epics.md` and `stories/index.json`. The two skills do not share a vocabulary for value or outcomes. Intake produces user-story sentences; feature-grooming produces `value_analysis`, `system_context`, `acceptance_condition`. There is no lift path from the former to the latter — each new intake item is an unmapped story by construction.

5. **The AC draft is marked DRAFT and told to be rewritten — but it's still written.** The stub template includes the rough ACs with a prominent disclaimer that they'll be fully rewritten. This is the worst of both worlds: AI downstream (`create-story`) sees the draft ACs and anchors on them (availability bias), while the human thinks they're provisional. The research's anti-pattern warning is direct: AC-layer artifacts degrade human review because they anchor attention on verification instead of intent. Draft ACs at intake time are the AC-anchor problem with the safety off.

6. **Role fragmentation without role separation.** Intake derives role (`{user_role}`), action, benefit from one conversation. Codecentric/Anthropic research: "role separation by construction, not convention." Intake's single-agent, single-conversation extraction violates its own practice's orchestrator-purity principle when it infers role/action/benefit without a challenging counter-agent. A challenger subagent at intake time (Osmani's PR Contract review-focus applied upstream) would surface "this description is doing two things" or "this item has no observable done state." Without it, every idea is captured with whatever coherence the original mention had, which the research shows is often insufficient.

## The Feature Layer Question

This is where intake fails most visibly against the research.

Momentum has `feature-grooming` and `feature-status` skills. Their schema (per the skill file) requires every feature to carry:

- `value_analysis` (multi-paragraph)
- `system_context`
- `type` ∈ {flow, connection, quality}
- `acceptance_condition` (outcome-observable)

The research direction is exactly this: human judgment at the feature level, not the story level. Momentum is on the right track *structurally*.

But intake is disconnected from it. Consequences:

1. **New stories enter without feature membership.** Intake asks for an epic, never a feature. Stories gain feature membership only if feature-grooming later associates them (and the feature-grooming workflow explicitly includes an "unmapped stories" discovery step — evidence the disconnect is producing orphans). This is backwards: the idea came in *because of* some user-facing concern; the user-facing concern is what the feature represents; forgetting the feature at capture and recovering it via discovery inverts the data flow.

2. **The `value_analysis` per feature has no upstream feeder.** feature-grooming must synthesize value from FR clusters, architectural signals, and story themes. If intake were asking the user "what value does this create, in one sentence?" at capture, feature-grooming would be aggregating that signal instead of reverse-engineering it. The intake → feature data flow is broken.

3. **The walking skeleton / North Star check has no home.** The research says every feature must have a North Star capability statement before any story on it starts. feature-grooming has `value_analysis` and `acceptance_condition` but no `north_star_capability`. Intake, the point at which an item's feature context is freshest, is also the point at which the North Star could be surfaced for the human to confirm ("this item is in feature X, whose North Star is Y — does it move us toward Y?"). Neither skill asks this.

4. **When intake's feature link is missing, the "spec-correct / value-zero" failure mode is structurally invited.** A story captured without a feature context, refined with `create-story`, developed in a sprint, and closed against its AC can pass every check Momentum runs — and the feature it belonged to can still be below its value floor. Nothing in the pipeline notices until feature-status runs and someone reads the HTML.

**What the research says happens when the feature layer isn't connected to intake:** the practice runs a "correct specs, irrelevant outcomes" loop. This is the 5–10-sprints failure mode, observed in production. The current intake design is a direct contributor.

## Hard Questions for the Owner

1. **What is intake's job, really?** Fast context capture (speed) or first-gate judgment (value)? The current skill chose speed. The research says value is where the leverage lives. These are incompatible; pick one and redesign the other skill to cover the other need.

2. **Why does every captured idea become a story?** Is the implicit model "if it's mentioned, it matters, so queue it"? The research (Shape Up, DORA rework rate, CAISI findings on over-generation) suggests the opposite: most captured ideas are not worth doing. What is intake's mechanism for *not* queueing something — and if it has none, is that a design choice or an oversight?

3. **Should intake exist at all as a separate skill?** Consider the alternative: `momentum:shape` as the front door (produces a Judgment Frame, tests for value-floor relevance, exits to pitch / feature-amendment / reject / defer), and stories are created only during sprint planning as execution artifacts derived from shaped pitches. Is there anything intake does that sprint planning, feature-grooming, or a new "shape" skill couldn't do better?

4. **Where does the Judgment Frame live?** If it's per-story (as the synthesis recommends), intake is the last place the human-present-in-conversation context exists — intake must capture it. If it's per-feature, intake should promote ideas to feature-level judgment *instead of* story-level capture when appropriate. Either way, the current intake has no place for the artifact the research most centrally identifies as missing.

5. **What happens to a captured stub that is never promoted?** Current answer: it sits in `backlog` indefinitely with `story_file: true` and `status: backlog`. Is there a decay / expiry mechanism? A regular review? If not, the backlog is a write-only data structure — the research's definition of the failure mode.

6. **Can the owner state, right now, the North Star capability for every feature currently in `features.json`?** If not, intake cannot possibly ask "does this item move us toward the North Star?" — because no North Star exists to move toward. This is the order-of-operations problem: intake reform depends on feature-layer reform, which depends on North Star reform. Attempting intake redesign first will produce a well-designed collector for a system that still can't say what it's collecting toward.

7. **Is the `create-story` pipeline — the thing intake's stubs feed — the right downstream?** `create-story` injects architecture analysis, change-type classification, implementation guide, dev notes. This is spec-driven development at maximum ceremony. The research's Fowler/Böckeler critique of Kiro applies directly: full spec packages for work that may not warrant them. If intake is fixed to filter better, does `create-story` also need to be tiered (lightweight for small items, full for large) rather than a single all-or-nothing pipeline?

8. **What would the practice look like if `intake` was deleted tomorrow?** If the answer is "we'd lose conversational capture" — ask why that capture requires a registered story slug, a file path, an index entry, and an epic assignment. The bare minimum to preserve intent from a conversation is a sentence in a journal. The rest of what intake does is premature commitment. What's the smallest artifact that would preserve the value of the capture without creating the trajectory problem? That artifact, not a stub, is probably what triage should produce.

---

**Bottom line:** Intake is a well-behaved skill solving an incomplete problem. It captures what was said; it does not challenge whether what was said should become work. The research says the highest-leverage point in an AI-native cycle is *before the spec reaches the AI* — and intake is currently designed to *not be* that point. The redesign question is not "how do we improve intake?" — it is "what is the right front-door activity for this practice, and is it the same skill as intake, or something else?"
