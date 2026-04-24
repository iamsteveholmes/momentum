---
title: Feature Dashboard — Real Content Sample for Claude Design Mockups
companion_to: feature-status-redesign-claude-design-brief.md
date: 2026-04-22
purpose: Populate Claude Design wireframes and mockups with authentic
         developer voice instead of synthesized placeholder text
---

# Feature Dashboard — Content Sample

This is a curated slice of real Momentum features, extracted from
`features.json`. Use this content to populate wireframes and mockups.
Respect the voice, length, and cadence — that voice is the design.

Five features below, one per state band, covering all three types
(flow / connection / quality). Each includes the text that would appear
on the corresponding Level 2 drill-down page.

---

## Summary stats (use for the index-page meta strip)

- Total features: 19
- Working: 2
- Partial: 11
- Not started: 6
- Features with gaps: 6

Type breakdown:

- Flow: 9 features
- Connection: 6 features
- Quality: 4 features

---

## Feature 1 — Sprint Planning to Ready Sprint

**Type:** flow
**State:** working
**Stories:** 6 / 6 done
**Last verified:** 2026-04-11
**Slug:** `momentum-sprint-planning-to-ready`

**One-line purpose (for index page cards):**
End-to-end sprint planning: backlog in, activated ready-for-dev sprint out.

**Acceptance condition (Level 2 boxed callout):**
A developer with populated backlog stubs can invoke `momentum:sprint-planning`
and receive an activated sprint with validated, Gherkin-specced,
ready-for-dev stories — without manually specifying story selection
criteria or review flow.

**Value narrative (Level 2 prose column — THIS is what needs typographic room):**

Sprint planning works. A developer with a backlog can run this skill
and emerge with a sprint plan — stories selected, assigned to waves,
ready for sprint-dev. The immediate value is real: structure and
sequence that would otherwise require manual deliberation across epics,
story sizes, and dependencies.

But the full vision goes beyond convenience. The skill synthesizes
across the PRD, epics, and story history to produce a plan that
reflects strategy, not just logistics. A developer who has been
heads-down in implementation can step back, run sprint-planning, and
get an outside-in view of what the next highest-leverage work is. That
is augmented strategic judgment — not just time savings.

Currently working and actively used. All 6 foundation stories are done.

**System context (Level 2 short callout):**
The ignition for every sprint cycle. All other sprint execution features
(orchestration, quality gates, retro) have no starting state without
this. Depends on backlog-refinement having kept the backlog clean.

**Stories:**
- Sprint Planning Skill (done)
- Sprint Planning Workflow Module (done)
- Sprint Workflow Alignment (done)
- Sprint Planning Synthesis-First (done)
- Mandatory Task Tracking (done)
- Gherkin ACs and ATDD Workflow Active (done)

**Known gap note (render as plain text, not alarm):**
Skill does not yet explain its reasoning. Developer gets a plan but not
the "why this sprint over that sprint" narrative. Sprint velocity
history is not yet factored in.

---

## Feature 2 — Impetus Session Orientation — Sprint State and Feature Status

**Type:** connection
**State:** working
**Stories:** 4 / 4 done
**Last verified:** 2026-04-11
**Slug:** `momentum-impetus-session-orientation`

**One-line purpose:**
Session-start handoff between developer context and AI session — sprint state, in-flight stories, feature summary.

**Acceptance condition:**
A developer opening a new Claude Code session with `momentum:impetus`
receives a greeting that shows current sprint name, stories in progress
vs done vs remaining, open journal threads (if any), and a feature
status summary (cached, with staleness flag if `features.json` has
changed since last cache).

**Value narrative:**

When a developer opens Claude Code mid-sprint, Impetus greets them with
sprint state, in-flight stories, and recent activity. This is one of
the highest-value features in the current implementation — it is used
every single session.

The pain this removes is real and daily: reconstructing "where was I?"
from files and git history at every session start. But the value goes
beyond pain removal. Orientation is also about confidence — the
developer knows the system is aware of its own state. That awareness
makes the practice feel coherent rather than fragmented.

Currently fully working. All 4 orientation stories are done. The
startup cache makes it fast.

**System context:**
The most-used feature in the practice. Orientation quality at session
start determines whether the developer feels grounded or adrift.

**Stories:**
- Impetus Skill Created with Correct Persona and Input Handling (done)
- Session Orientation and Thread Management (done)
- Impetus Greeting Rewrite (done)
- Impetus Feature Status Cache (done)

**Known gap note:**
This feature covers the functional sprint-state component. The broader
Impetus experience (personality, warmth) is a separate feature
(Impetus Experience) — see its gap description for the "lifeless config
dump" drift being addressed there.

---

## Feature 3 — Sprint Retro + Practice Improvement Flywheel

**Type:** flow
**State:** partial — with gap flag
**Stories:** 4 / 7 done
**Last verified:** 2026-04-11
**Slug:** `momentum-retro-and-flywheel`

**One-line purpose:**
Retro ceremony plus the flywheel — cross-story pattern detection that feeds improvements forward into the practice.

**Acceptance condition:**
A developer can run `momentum:retro` after a sprint and receive a
findings document produced from transcript audit (not just milestone
logs); at least one retro finding generates a story stub added to the
backlog; cross-sprint patterns accumulate in the findings ledger.

**Value narrative:**

The retro skill closes the sprint loop: findings documented, sprint
marked complete, summary written. This works and delivers value — a
developer who skips retros loses the reflection that improves future
work.

But the larger vision — the flywheel — is where this feature becomes
transformative. A developer running sprints without the flywheel is
like a craftsperson who never sharpens their tools. The flywheel means
that patterns from this sprint feed into better story quality in the
next, that recurring mistakes stop recurring, and that the practice
accumulates wisdom over time. A developer who runs 10 sprints with the
flywheel should be dramatically more effective in sprint 10 than
sprint 1 — not because they're personally smarter but because the
system they're working within is smarter.

Currently, the retro executes and sprint-summary writes are working.
The flywheel accumulation (cross-story pattern detection, findings
ledger, practice feedback loop) is not yet implemented.

**System context:**
Closes the sprint loop and feeds forward. Sprint-planning benefits from
flywheel accumulation; practice-distillation encodes the patterns the
flywheel surfaces. Without retro, each sprint is isolated. With the
full flywheel, sprints compound.

**Stories:**
- Retro Skill (done)
- Retro Workflow Rewrite (done)
- Sprint Boundary Compression (done)
- Retro → Triage Handoff (done)
- Cross-Story Pattern Detection (backlog)
- Findings Ledger Accumulates Quality Findings (backlog)
- Flywheel Workflow Explains Issues and Guides Upstream Trace (backlog)

**Gap description (render explicitly — this is what GAP flag means):**
Acceptance condition requires *transcript-audit findings with
cross-sprint pattern accumulation*. Assigned stories cover the retro
ceremony (done) but not the flywheel mechanics (3 backlog stories).
Retro currently produces findings but they don't yet compound across
sprints. The practice-compounds epic — the soul of this feature — is
still ahead.

---

## Feature 4 — Feature Status Visibility + Grooming

**Type:** connection
**State:** partial — status-drift candidate (all stories done; awaiting promotion to working)
**Stories:** 5 / 5 done
**Last verified:** 2026-04-11
**Slug:** `momentum-feature-status-visibility`

**One-line purpose:**
The feature dashboard itself — rendered view of all features with coverage, gaps, and grooming means to keep the taxonomy honest.

**Acceptance condition:**
A developer can run `momentum:feature-status` and receive a rendered
view showing all features with current status, story coverage counts,
and explicit gap flags — and can run `momentum:feature-grooming` to
evaluate and update the feature taxonomy itself.

**Value narrative:**

A developer can see which features are advancing and which have
coverage gaps — before committing to a sprint plan. The feature-status
HTML artifact works: it shows feature progress, gap indicators, and a
dependency graph.

But the deeper value is the shift it creates in how developers think
about their work. Without feature visibility, it's easy to complete
many stories and advance no features — building depth in some areas
while leaving others as permanent stubs. Feature-status makes that
pattern visible. The developer sees not just "what's done" but "what's
actually progressing toward user value."

Feature-grooming completes the loop: visibility without grooming means
the feature list itself may be wrong. A feature list that doesn't
reflect the actual product produces misleading status.

**System context:**
The bridge between story-level progress and feature-level value
delivery. Without this, developers can complete 10 stories and advance
0 features — a discouraging pattern this feature makes impossible to
overlook.

Worth noting for mockup design: this is a meta feature — it is the
feature *about viewing features*. The dashboard you are designing is
the UI for this feature.

**Stories:**
- Feature Artifact Schema (done)
- Feature Status Skill (done)
- Feature Status Practice Path (done)
- Impetus Feature Status Cache (done)
- Feature Grooming (done)

**Status-drift note:**
All 5 stories done but feature status still marked "partial" in
`features.json`. Candidate for promotion to "working" on next
feature-grooming run. This is a useful edge case for the index page —
how do you render "all stories done but status not yet promoted"
gracefully?

---

## Feature 5 — Practice Knowledge Base — Project-Local Cold Vault

**Type:** connection
**State:** not-started
**Stories:** 0 / 3 done
**Last verified:** 2026-04-19
**Slug:** `momentum-practice-knowledge-base`

**One-line purpose:**
Project-local knowledge vault — ingests source docs (Obsidian, llms.txt, research, code trees) and serves them as cold-start context for agents.

**Acceptance condition:**
A developer can run `/momentum:kb-init` and `/momentum:kb-ingest`
against a project doc source, then have `/momentum:build-guidelines`
produce guidelines that cite specific KB passages.

**Value narrative:**

Current value: None delivered today. All stories are backlog. Practice
relies on ad-hoc file reads and training-data defaults for project
context.

Full vision: a developer points Momentum at source material (Obsidian
vault, llms.txt, research reports) and KB ingests into a
pre-synthesized wiki — queryable via grep on an index. build-guidelines
uses it to produce stack-specific guidelines with citation integrity.
Research skills ground findings against project reality. Agents
receive KB queries as cold context on spawn. The practice becomes
genuinely project-aware.

**System context:**
Infrastructure feature. Feeds composable-specialist-agents (guideline
generation needs source material), deep-research-pipeline (research
artifacts land here), and future retro-flywheel accumulation. Without
KB, guideline generation is limited to stack-detection heuristics.

**Stories:**
- KB Init (backlog)
- KB Ingest (backlog)
- KB Raw Ingest Spike (backlog)

**Known gap note:**
No ingestion pipeline, no store format, no query interface. The
`kb-raw-ingest-spike` must run before `kb-ingest` can be designed
properly — source-type ingestion strategies (Obsidian plugins,
crawl4ai, llms.txt) are unresolved. The vault-centric vs project-
centric orchestration model is undecided. This is a useful case for
the mockup: a feature where the *whole thing* is still blueprint.

---

## Feature 6 — Quality Gates — AVFL, Code Review, and Retro Applied to Every Sprint

**Type:** quality
**State:** partial
**Stories:** 6 / 8 done
**Last verified:** 2026-04-11
**Slug:** `momentum-quality-gates-enforced`

**One-line purpose:**
Every story goes through AVFL validation, code review, and E2E validation before merge. Gate failures block merge.

**Acceptance condition:**
A sprint completes with: every merged story having passed AVFL + code
review + E2E validation; the retro producing a findings document from
transcript audit; gate failures reported with actionable resolution
guidance.

**Value narrative:**

Quality gates change the developer's relationship with defects.
Without them, defects are discovered after merge, sometimes after demo.
With automated gates, defects surface before they compound. The
developer gets immediate feedback when a story breaks its acceptance
criteria.

But the deeper value is the psychological safety it creates. A
developer who knows that every merge is gated can move faster —
because they know the system will catch what they miss. The gates are
not bureaucratic checkpoints; they are the reason confident, rapid
development is possible.

Currently working: AVFL and team review gates run in every sprint. The
practice catches real issues. The developer doesn't need to manually
review every merge.

**System context:**
The enforcement layer that makes all other features trustworthy.
Without gates, any feature can regress silently. With them, "working
software at sprint end" is the default expectation, not the optimistic
one.

**Stories:**
- PostToolUse Lint and Format Hook Active (done)
- Stop Gate Runs Conditional Quality Checks (done)
- Gherkin ACs and ATDD Workflow Active (done)
- Quality Gate Parity Across Workflows (done)
- AVFL Scan Profile (done)
- Retro Workflow Rewrite (done)
- AVFL Fixer Required Gate (backlog)
- AVFL Default Agent Composition (backlog)

**Known gap note:**
The AVFL fixer (automated remediation for common defects) is not yet
implemented. Some gate failures require manual analysis and fixing.
Known defect escapes exist in practice.

---

## Usage guidance for the designer

**Voice and tone.** The narratives above are the developer's own voice
— direct, somewhat long-form, assumes a technical reader, values
analogies ("craftsperson who never sharpens their tools"), avoids
marketing language. Preserve this on mockups; do not substitute crisper
or terser copy. Length is part of the signal.

**Typography.** Value narratives are the single most important
typographic element. They deserve serif body + a comfortable reading
column (~68–72ch). Meta fields (status, type, story fraction) belong
in a monospace or small-caps sans accent. One-line purposes work in the
same sans as UI chrome.

**State palette.** Use these six features to tune the state visual
treatment:
- `working` should feel settled but alive (it's current truth, not past
  tense).
- `partial` is the largest category — visual weight should not
  overwhelm.
- `not-started` should feel light — not absent, not alarming, just
  *yet to come*.
- `gap flag` is the only "attention" signal on the index. Subtle.

**Empty / stub states.** For feature 5 (Practice Knowledge Base), the
Level 3 story drill-downs would all show "content pending" because
these are backlog stubs. Design this gracefully — not an error, not a
scolding, just calm placeholder with a hint ("Run
`momentum:create-story` on this story to enrich").

**Edge case for index.** Feature 4 is an interesting edge: all 5
stories done but the feature still reads "partial" because
feature-grooming hasn't promoted it yet. This should not render as a
contradiction; the dashboard is reflecting a real-world pipeline lag.
Show it as it is.
