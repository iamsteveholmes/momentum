# Triage/Intake Phase — Analyst Findings

## Executive Summary

- The current `intake` skill is a context-preservation capture — it gets a conversation into a backlog stub, nothing more. It performs **none** of the value-framing work the synthesis research says should happen at intake. It is a *storage* step, not a *triage* step.
- The research assigns intake two jobs that Momentum's `intake` skill does not do: (a) produce the human-judgment "Judgment Frame" artifact, and (b) force a North Star capability check before an item enters the queue. The stub template has no Intent / Done-state-for-a-stranger / Anti-goals / Review-focus block and no value-floor question.
- The feature layer (`feature-grooming`, `feature-status`) is structurally disconnected from intake. Intake writes to `stories/index.json`; it never touches `features.json`. An intake stub can sit in the backlog indefinitely without being mapped to a feature or challenged against the feature's value.
- The 5-step workflow has two steps that are ceremony with weak value (steps 3 and 4 around slug normalization and template substitution) and two steps (epic assignment, final enrichment report) that do real work. The missing steps — the ones the research says matter most — are not there at all.
- Intake currently sets up downstream phases poorly: it produces a stub with "DRAFT — rewrite via create-story" warnings on every section, which means create-story discards most of intake's output. The handoff shape treats intake as throwaway rather than accretive.

---

## What Exists and How It Aligns

Step-by-step mapping of the current `intake` workflow against the research.

### Step 1 — Extract story context from conversation

What it does: Pulls `{{title}}`, `{{description}}`, `{{user_role}}`, `{{action}}`, `{{benefit}}`, `{{rough_acs}}`, `{{pain_context}}`, `{{suggested_epic}}`, `{{suggested_priority}}` from the current conversation.

Alignment with research: **Partial.** The "As a / I want / so that" extraction is a *human-judgment-shaped* input — this is the correct grain for early triage per Kurilyak's bifurcation (human-readable story vs. AI execution artifact). The `pain_context` capture is also good: it is raw enough to survive downstream rewriting.

Misalignment: None of the extraction fields match the Judgment Frame the synthesis identifies as the missing artifact (synthesis section "Problem 2 / Concrete recommendation / item 2"). Specifically:
- No **Intent** sentence (plain-language "why a user would care") — `benefit` is adjacent but framed as AC-like, not as glanceable intent.
- No **Done-state-you-could-show-a-stranger** — the closest field is `rough_acs`, which the synthesis explicitly names as the *wrong* level ("AC is too low-level and overly technical").
- No **Anti-goals** field. This is the synthesis's counter to AI's "add nearby plausible features" failure mode (Osmani). Intake collects no anti-goals at all.
- No **Review focus** — the one or two questions a reviewer should answer after running the build.

### Step 2 — Determine epic assignment

What it does: Uses `{{suggested_epic}}` if supplied; otherwise reads `epics.md`, proposes best-fit epics, asks the user to confirm.

Alignment with research: **Misaligned at the conceptual layer.** The synthesis is explicit that the **feature**, not the epic, is the primary human-judgment unit (Problem 2, recommendation 3: "Promote the feature (or epic) to be the primary human-judgment unit"). Momentum has a feature layer (`features.json`, feature-grooming, feature-status) whose *purpose* is exactly the value-mapping the research demands — but intake routes the story into an epic, not a feature. Epics in Momentum are taxonomic categories ("long-lived, never-closing groupings" per epic-grooming workflow); features are value-bearing units.

Consequence: an intake stub lands in the taxonomy layer but never touches the value layer. There is no point in the cycle where an intake stub is forced to answer "what feature does this serve?" — and therefore no point where it is forced to answer "what user-observable behavior does this feature deliver?"

### Step 3 — Generate slug and check for conflicts

What it does: Lowercase, replace, truncate, collision-check against `stories/index.json`.

Alignment with research: **Irrelevant to research findings.** This is mechanical hygiene. The research has no position on slug uniqueness; it is an implementation detail of the write path.

Ceremony assessment: Necessary, low cost.

### Step 4 — Populate stub template and write stub file

What it does: Substitute variables into `stub-template.md`, write to `stories/{slug}.md`, call `momentum-tools sprint story-add`.

Alignment with research: **Structurally wrong for the research's model.** The stub template inserts rough ACs as ACs (prefixed with warnings), leaves every downstream section as `DRAFT — requires rewrite via create-story`, and sets status to `backlog`. Per the synthesis:
- The AC block should be **for the AI** and should only be written when the story is actually headed to development (synthesis Problem 2, recommendation 1: "The Momentum story stays as-is — it's an AI execution artifact").
- The human-judgment artifact — Judgment Frame — should be written **at intake** because it is the cheapest moment to capture human intent while it is still fresh.
- By writing a story skeleton with AI-execution sections marked DRAFT, intake produces a document whose primary content is empty placeholders and whose actually-useful content (intent, pain context) is buried in the description.

Effect: the stub file inverts the research's preferred shape. What should be prominent and decision-bearing (Judgment Frame) is absent. What should not exist yet (AC, tasks, dev notes, implementation guide, testing requirements, architecture compliance, project structure notes, references) is rendered as empty placeholders that create visual noise.

### Step 5 — Report what was captured and what still needs enrichment

What it does: Prints a summary of what was captured and tells the user to run `create-story` when ready.

Alignment with research: **Reasonable, but reinforces a misframe.** The "what still needs enrichment before development" list is: AC refinement, tasks/subtasks, dev notes, testing, implementation guide. These are all AI-execution-side items. The research would add: *"What still needs human judgment work" — Judgment Frame rollup to feature, anti-goals, North Star capability check if this item would cross a value floor.* Neither is mentioned.

---

## Gaps: What the Research Says Should Exist

Mapped directly to synthesis recommendations.

### 1. Judgment Frame capture at intake

Synthesis Problem 2, recommendation 2. The Judgment Frame is ~5–10 lines: Intent / Done-state-for-a-stranger / Anti-goals / Review focus. The research's claim: **this is the owner's own "human readability optimized section,"** and it is the highest-leverage addition Momentum can make.

Current intake: does not produce this. Has no field for anti-goals at all.

Evidence in synthesis: "Move the review forward, not back. The Vibe-Check Protocol paper's mechanism — recognition mode vs. generative mode — implies that reviewing finished output always degrades because the brain takes the easy path. The review you want is *before the spec goes to the AI*."

Intake is the earliest possible moment for that review. The intake skill currently skips it.

### 2. Feature assignment (not just epic assignment)

Synthesis Problem 2, recommendation 3, and the "Value Floor" section (Problem 4). The feature is the primary human-judgment unit; stories serve features.

Current intake: asks for epic assignment (taxonomy), not feature assignment (value). `features.json` is never read, never updated. A story can enter the backlog with no feature mapping.

Evidence in feature-grooming workflow: `features.json` entries carry an `acceptance_condition` — "A developer can [action] and [observe outcome]" — which is exactly the outcome-observable artifact the synthesis calls for (Problem 3, transcript/outcome separation; Problem 4, North Star capability). Intake never touches this layer.

### 3. North Star / value-floor check

Synthesis Problem 4, recommendation 1: "Every feature must have a North Star capability statement before work begins." Corollary: new items entering the backlog for a feature should be evaluated against whether they move toward or elaborate around the value floor.

Current intake: no concept of value floor. A pre-floor story and a post-floor elaboration story are captured identically.

Consequence: intake is a primary source of "punting" — the silent accumulation of elaboration stories on features whose skeleton has not been built.

### 4. Anti-goals statement

Synthesis Problem 2, EARS/spec table and recommendation 2. "Anti-goal statements — bound optimization targets" — "This system is not intended to..."

Current intake: no anti-goals field. The stub template has no section for them. This is the exact failure mode the synthesis warns about: AI agents "confidently fill gaps with plausible-but-wrong guesses" (Osmani — "add photo sharing" leads to invented file limits, permissions, storage). Without anti-goals captured at intake, `create-story` has to reconstruct them from conversation the AI no longer has access to.

### 5. Risk tier / review focus tagging

Synthesis Problem 2, recommendation 7: "Risk-tiered review... reserve deep human read for security, auth, payments, business-logic boundaries."

Current intake: captures priority (critical/high/medium/low) which is about sequencing, not risk. No risk dimension at all.

Consequence: intake cannot feed a downstream "does this story need human review of the output?" decision. Everything gets the same review treatment.

### 6. Appetite instead of priority

Synthesis Problem 1, recommendation 4: "Use Shape Up's 'appetite' concept for sizing... declare an appetite ('I'm willing to spend half a day on this') and fix scope to fit. Appetite is ordinal, not cardinal — which aligns with the owner's Q5 point on ordinal value measurement."

Current intake: takes a priority enum. Priority answers "when?" not "how much do I want to invest?" These are different questions and the research prefers the second for AI-native work.

---

## Removal Candidates

### Candidate 1: The DRAFT placeholder sections in the stub template

The stub template (`stub-template.md`) includes seven sections marked `DRAFT — requires rewrite via create-story before this story is dev-ready.`:
- Acceptance Criteria
- Tasks / Subtasks
- Dev Notes → Architecture Compliance, Testing Requirements, Implementation Guide, Project Structure Notes, References
- Dev Agent Record → Agent Model, Debug Log, Completion Notes, File List

These sections are empty placeholders that will be overwritten by `create-story`. They add file bytes, force the reader past noise to find the real content, and visually encode an AI-execution-shaped document at a moment when the only content is human-judgment-shaped.

Research backing: synthesis Problem 2, "Accept the bifurcation explicitly. The Momentum story stays as-is — it's an AI execution artifact. Do not try to make it simultaneously human-readable and machine-executable."

Removal proposal: the intake stub should contain only the human-judgment content (intent, done-state, anti-goals, review focus, pain context, suggested feature). The AI-execution sections should be added by `create-story` at the moment they are meaningful, not preemptively stubbed.

### Candidate 2: Rough ACs capture

Step 1 extracts `{{rough_acs}}` and step 4 inserts them prefixed with "The following are rough draft ACs captured from conversation." The stub then warns the reader twice (HTML comment + explicit note) that these ACs will be replaced.

The synthesis is explicit: AC is an AI-execution artifact, not a human-judgment artifact. Capturing rough ACs at intake serves neither audience:
- The AI will not use them (create-story rewrites them from architecture analysis)
- The human doesn't read them (they're flagged as throwaway)

The useful content — the *behavioral intent* behind the rough ACs — belongs in the Done-state-for-a-stranger field of the Judgment Frame, in plain language, not in AC form.

Removal proposal: stop capturing rough ACs. Capture done-state descriptions instead.

### Candidate 3: Priority defaulting to "low"

Step 1 defaults `{{suggested_priority}}` to `low` when not mentioned. This is ceremony that pretends to have information it doesn't. Per the tracking schema, `low` means "Default — nice to have, refine when relevant." Defaulting-to-low silently asserts a value judgment that was not made.

Research backing: synthesis Problem 1, recommendation 4 (appetite over estimate). A field that is always defaulted to a specific value is carrying no signal.

Removal proposal: omit priority from intake. Let it be set at `refine` or `sprint-planning`, where the backlog is being examined holistically and priority comparisons across items are meaningful.

### Candidate 4: The epic-assignment interactive step as currently scoped

Step 2 reads `epics.md`, proposes best-fit epics, and interactively asks for confirmation. This is reasonable ceremony *for a taxonomy layer that is doing the work of a value layer*. If the research's recommendation to promote features as the primary unit is adopted, the interactive question should shift from "which epic?" to "which feature, or is this a new feature that needs a North Star capability?"

Not purely a removal — it is a re-scoping. The current question is the wrong one at the wrong layer.

---

## Feature Layer Integration Opportunities

The `feature-grooming` and `feature-status` skills exist and already produce the artifacts the research says the triage phase needs. The integration gaps are:

### Opportunity 1: Intake reads `features.json` and asks for feature assignment

`feature-grooming` writes a rich per-feature record:
- `value_analysis` (3 paragraphs: current value / full vision / known gaps)
- `system_context` (how it fits architecture/user model)
- `acceptance_condition` ("A developer can [action] and [observe outcome]")
- `status` (working / partial / not-started)
- `stories` array (what's already mapped)

Intake could read this file during Step 2, propose a best-fit feature based on the conversation, and write the story's slug into that feature's `stories` array at write time. This closes the loop that feature-grooming currently has to re-open (its refine mode scans for "unmapped story groups: stories whose themes don't align with any existing feature").

Current cost of the gap: every refine pass does rediscovery work that intake could have prevented at the moment of capture.

### Opportunity 2: Feature status drives a "new feature?" branch in intake

If the conversation's story maps to no existing feature, intake has two paths:
1. Defer: capture story under a "no-feature" placeholder and surface it to the next `feature-grooming` run.
2. Inline: ask the user "this doesn't map to an existing feature — what feature is this a part of? If new, what's its North Star capability?"

The synthesis recommends (2): every feature must have a North Star before work begins (Problem 4, recommendation 1). Intake is the latest-possible moment for this check before work gets queued.

### Opportunity 3: The feature's `acceptance_condition` becomes the story's Judgment Frame seed

The feature-grooming `acceptance_condition` format — "A developer can [action] and [observe outcome]" — is *exactly* the synthesis's Done-state-for-a-stranger shape, scaled to feature grain. An intake stub mapped to a feature could inherit the feature's acceptance_condition as the default "this is what good looks like at the feature level" anchor and ask only for the story-level delta: "what is this particular story's contribution to the feature's acceptance_condition?"

### Opportunity 4: `feature-status` becomes intake's dashboard context

`feature-status` generates an HTML planning artifact (per the skill's description). Its role in the practice could be: the intake skill reads feature-status data to show the user, at intake time, "feature X is currently at status `partial` with N stories done and M remaining — this story is contribution K." This makes the North Star / pre-floor/post-floor check visible at intake rather than deferred.

Evidence: `feature-status` already has an eval `eval-gap-analysis-flags-missing-coverage.md` — gap analysis is in scope for this skill. Intake could consume that signal.

### Opportunity 5: Merge intake and `feature-grooming` invocation paths for new-feature intake

If intake discovers the item doesn't map to any existing feature and is value-bearing enough to be its own feature, the user needs `feature-grooming` to be run (at least in a lightweight per-feature mode). Currently intake terminates with "run create-story later"; a future intake could terminate with "run feature-grooming to register the new feature, then create-story when dev-ready."

This is the integration that closes the circular flow: Triage → Refinement → Planning → Dev → Retro → Triage. Without the feature-layer touch, intake loops directly back to stories without ever visiting the feature layer.

---

## Questions Raised

For the consolidation analysis and for the owner — questions, not recommendations.

### On the shape of the intake stub

1. Given the synthesis's bifurcation principle (AI-execution artifact vs. human-judgment artifact), should the intake stub be a **Judgment Frame file only** (no AC, no tasks, no dev notes), and should `create-story` produce a *separate* AI-execution file that references back to the Judgment Frame? Or should they remain a single file with a clearly separated human section above an AI section?

2. The current stub sets status to `backlog` and carries warnings that create-story must rewrite everything. If intake's only output were the Judgment Frame, would `create-story` be modifying the same file — or would `create-story` produce a new, sibling file? This affects whether the DRAFT warnings are even meaningful.

### On feature-layer integration timing

3. Should intake refuse to capture an item that does not map to any existing feature, routing the user to `feature-grooming` first? Or should it capture into a "feature-pending" bucket and surface that bucket during `refine`?

4. If intake is the earliest point where "what feature does this serve?" is asked, what happens when the answer is "I don't know yet, let's see where it goes"? Does Momentum have a legitimate path for exploratory items, or does the value-floor discipline require every intake item to commit to a feature?

### On the rough ACs vs. Judgment Frame trade

5. The rough-ACs capture was presumably put into intake to preserve the conversation's detail. If rough ACs are removed in favor of a Judgment Frame, is there a risk of losing information the user articulated conversationally but that doesn't fit the Judgment Frame format? Does anything in the Judgment Frame's four fields have enough room for "I was thinking about this specific edge case too" noise?

### On North Star enforcement at intake

6. The synthesis recommends the North Star capability statement happen "before any sprint on a new feature." Is intake the right gate for this, or does the gate belong at `feature-grooming`? The answer affects whether intake needs any value-floor logic at all or just a reference to `features.json`.

7. If `feature-grooming` owns the North Star, does intake need to *verify* that the target feature has a North Star before accepting the story? This would turn intake into a value-floor enforcement point — rejecting stories targeting features that are North Star-less.

### On the anti-goals field

8. Where else in the Momentum practice do anti-goals surface? Is there an existing field (in create-story, in the feature schema, in epics.md) that already carries "what this is not"? If yes, intake's anti-goals capture should feed that field. If no, anti-goals is a new first-class concept and needs a home in the data model — not just in the intake stub.

### On appetite vs. priority

9. Is priority (critical/high/medium/low) serving a real function anywhere in the pipeline — sprint planning, refine, sprint-dev — that appetite (ordinal time investment) could not serve? If priority is only a sorting key and never a resource-allocation decision, replacing it with appetite costs nothing and carries more signal.

### On the overall intake phase name

10. The current skill is called `intake`. "Triage" — the name the owner used for the phase in the cycle description — carries a stronger connotation of *deciding whether to admit this item at all*, *at what priority*, *with what anti-goals*. The current skill does no deciding — it only captures. Is the phase misnamed in the cycle, or is the skill underscoped for the phase name the practice has adopted?

### On the cycle's feedback loop

11. The cycle (Triage/Intake → Refinement → Planning → Dev → Retro → Triage) implies the *Retro* should feed back into *Triage* — learnings from the prior sprint should reshape what enters the backlog next. Is there any mechanism today for retro findings to flow into intake's judgment (e.g., anti-goals discovered during dev becoming defaults for related future stories)? If not, the cycle is one-way at this seam, which undercuts the "inspect and adapt" role of the sprint that the synthesis (Problem 1, Lindsay) says is the sprint's actual purpose.
