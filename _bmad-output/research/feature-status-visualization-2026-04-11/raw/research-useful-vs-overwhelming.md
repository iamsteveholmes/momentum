---
content_origin: claude-code-subagent
date: 2026-04-11
sub_question: "Useful vs. overwhelming — practitioner lessons on feature planning views"
topic: "Feature planning artifact visualization"
---

# Useful vs. Overwhelming: Practitioner Lessons on Feature Planning Views

## Summary

This document synthesizes practitioner accounts, retrospectives, and case studies from teams who built, iterated on, or abandoned feature planning dashboards. The through-line is consistent: teams over-build, then strip down. The signals that survive are ones that answer "what should we do next?" rather than "what is happening?"

---

## What Teams Built vs. What They Used

### The Dashboard Proliferation Pattern

The most reliable finding across practitioner accounts is the gap between dashboards created and dashboards used. A 2026 case study from an engineering team documented as "The Cloud Playbook" found that after a usage audit, 28 of 47 dashboards (60%) had zero views in the past 90 days. A further 11 had been opened only once — by the person who created them. Only 19 dashboards survived with clear ownership and active use. [PRAC]

This is not an exceptional case. Sigma Computing's analysis of data fatigue found that organizations accumulate tool sprawl where "each one introduces new dashboards, login screens, and slightly different versions of the truth," and that "only a small subset" of tracked metrics "align with strategic priorities." [PRAC]

The pattern of accumulation is described consistently: dashboards are created incrementally, one incident or one quarter at a time. Each makes sense when created. Collectively, they become noise.

### What Remains After the Audit

In the cloud engineering case study, the 19 surviving dashboards served four narrow functions: service health monitoring, infrastructure cost tracking, deployment pipeline visibility, and per-tenant SLA tracking. Everything else was removed. The measured outcome: a 35% reduction in mean time to diagnosis within the following quarter and faster incident orientation within two weeks of deletion. [PRAC]

The lesson: "Every unused dashboard is a tax on response time, compounding across every incident and new team member." Signal density — not volume — determines whether a planning view is useful. [PRAC]

---

## What Practitioners Actually Look At

### The Decision-Driving Test

Across multiple practitioner accounts, the clearest filter for whether a planning signal is useful is: does it drive a decision? A February 2026 Medium analysis of dashboard failure patterns identifies the root cause as "dashboards built for visibility, not decision-making." The practical failure mode is answering "What is happening?" without addressing "What should we do about it?" [PRAC]

The diagnosis question practitioners recommend: when someone sits down at the planning view, can they identify the single most important action to take? If not, the view has failed regardless of how much data it shows.

### What Intercom Actually Tracks

Intercom's documented process (via their "Inside Intercom" blog) offers a concrete picture of minimal-but-sticky planning artifacts. Their active tracking included: weekly and daily goals mapped directly to releases, success metrics defined per project, open bug counts via GitHub API integration, and customer feedback tagged and reviewed weekly. [PRAC]

Notably, their planning artifacts explicitly excluded solutions at the brief stage — the "Intermission" (project brief) was capped at under one page covering only problem, success metrics, and scope. They actively fought tool sprawl: "When managing a product includes all of Google Docs, Trello, Github, Basecamp, Asana, Slack, Dropbox, and Confluence, then something is very wrong." [PRAC]

What they kept in their Trello-based roadmap: color-coded cards by team, red labels for slippage patterns, and phase-based checklists (Design, Build, QA, Beta, Full release, Post release). The checklist served a checking function, not a mandating one.

### What Developers vs. PMs Look At

Atlassian's 2024 State of Developer Experience survey (2,100+ developers and managers) found that 69% of developers lose 8+ hours weekly to inefficiencies. A key disconnect: leaders believed AI was the top solution, while two-thirds of developers reported no meaningful productivity gains from AI tools. [OFFICIAL] This misalignment extends to planning views: what leaders instrument and display rarely matches what developers need to orient themselves at the start of a work day.

From practitioner accounts, developers need context from planning views: the "why" behind upcoming work, how streams fit together, and what constraints are in play. Developers "already live in the details" — what they need is the higher-order frame, not more details. [UNVERIFIED, synthesized from multiple practitioner sources]

---

## Dashboard Blindness: How It Happens

### Three Failure Modes

The most consistent practitioner accounts identify three mechanisms by which planning views become invisible:

**1. Equal visual weight.** When all metrics have the same visual prominence, viewers experience what analysts call "priority blindness" — forced to interpret everything without knowing what matters. The resulting response is disengagement. Practitioners recommend 3-6 key metrics with clear visual hierarchy rather than 15+ charts with no ranking. [PRAC]

**2. Metric substitution (Goodhart's Law in planning views).** Teams optimize what is measured. When planning boards track velocity, milestone completion, and story point burndown, teams optimize those numbers rather than shipping quality software. DEV Community analysis describes this as "instrument panel capture" — leadership gradually manages the dashboard instead of managing the system. [PRAC] The diagnostic: "When reality contradicts the dashboard, which one changes?" In dysfunctional organizations, teams adjust reality to match the dashboard.

**3. Dashboard decay without ownership.** Practitioner analysis from Linear's usage data found that the median workspace creates just two dashboards, and adoption drops sharply beyond that. Key failure modes: dashboards without owners go stale, configurability without purpose generates noise, and the number created rarely reflects the number actually used. [PRAC]

### Jira Board Abandonment

A documented Jira over-engineering case study shows a team with a 15-step workflow that "required constant shuffling of tickets rather than shipping features," causing a 30% velocity drop. Resolution: reducing to 5 core stages — To Do, In Progress, In Review, Done, Blocked. [PRAC]

The broader pattern: teams inherit or create bloated workflows, backlogs become graveyard repositories, and notification overload causes teams to tune out alerts entirely. The diagnostic from practitioners: "If an engineer can't glance at the board and immediately understand the state of play, it's too complicated." [PRAC]

---

## Signals That Looked Important But Weren't Acted On

### Percentage Complete

Basecamp's Ryan Singer documented this in detail when justifying the hill chart design. Stating "42% of tasks are complete" provides no useful insight because it obscures which specific work items remain problematic. More damaging: as teams discover work during implementation, task counts grow — making raw percentage metrics show progress moving backward when scope is actually being clarified. Singer: "As teams roll up their sleeves on a project, they discover more detailed tasks than they had in the beginning, and a raw percentage count would show progress going backward." [OFFICIAL]

This is a status signal that looks rigorous but actively misleads.

### Velocity as a Planning Signal

Velocity — story points completed per sprint — is among the most widely displayed metrics in planning boards and among the most criticized by practitioners for driving wrong behavior. The key practitioner failure mode: teams treat velocity as a goal rather than a measurement, leading to gaming (inflating story point estimates) rather than improvement. [PRAC] Velocity tells you what a team has done; it cannot tell you whether the right work was done or whether the team is accelerating toward delivery.

### Complex Prioritization Scores

Markus Müller's documented experience scaling product roadmaps across multiple companies found that RICE scoring (Reach, Impact, Confidence, Effort) created "false precision." Teams struggled with calibrating Reach and Impact: "a scale of 10 is so hard to use. What is the actual difference between 6, 7, 8?" He simplified to ICE and found better adoption. [PRAC]

The lesson: prioritization frameworks displayed in planning views often suggest more precision than the underlying data supports, creating false confidence in rankings.

### Specialized Roadmapping Tool Adoption

Despite testing dedicated roadmapping software, Müller documented that adoption consistently failed across organizations: "I have not been successful in establishing them across the whole company in a practical way." Teams succeeded when using culturally embedded tools — Trello, Asana, Jira — that were already in their workflow. A planning view in a tool nobody opens is invisible by definition. [PRAC]

---

## What Reduces Cognitive Overload: Practitioner Findings

### The Hill Chart as a Design Archetype

Basecamp's hill chart is the most documented case study in feature status visualization specifically designed to reduce cognitive overload by removing noise. The core design decision: replace automated computational metrics with a human-generated status reflecting a team member's felt sense of certainty about the work.

The visualization distinguishes two phases: **uphill** (problem-solving and discovery, high uncertainty) and **downhill** (execution with unknowns resolved, predictable). This single dimension carries more decision-relevant information than percentage-complete or task count, because it answers the question a manager actually needs: "Is this work still in the figuring-out phase, or is it now in execution?" [OFFICIAL]

The "second-order view" — comparing sequential snapshots over time — reveals which scopes are advancing and which are stuck, without requiring anyone to explicitly report being blocked. A non-moving dot becomes the signal. This is information that is invisible in task-count dashboards. [OFFICIAL]

### The 3-5 Metric Ceiling

Practitioner consensus from multiple sources converges on a working ceiling of 3-6 active metrics per planning view. Beyond this, viewers experience decision fatigue and disengage. The dashboard deletion case study (19 surviving dashboards from 47) reflects this at the dashboard level; within each dashboard, the retained views served narrow, single-function purposes. [PRAC]

### Separating Discovery from Delivery

Müller's roadmap framework found that splitting "Now Discovery" from "Now Delivery" in the planning view revealed staffing constraints and forced honest acknowledgment that "no team can run several discoveries on different topics at the same time effectively." [PRAC] This is a layout decision that prevents a specific category of planning blindness: teams overcommitting to active work by conflating exploration and execution.

### Intercom's "Checklist Is for Checking" Principle

Intercom explicitly noted that checklists in their planning view served a checking function rather than a mandating function. The distinction matters for layout: a checklist displayed in a planning view should confirm completion, not drive behavior. Planning views that embed detailed checklists as the primary status signal often collapse into "checkbox theater" — performative completion without genuine progress. [PRAC]

### Minimal Structure in Existing Tools

The practitioner pattern across Intercom, the Jira simplification cases, and Müller's roadmap work is consistent: planning views that live in tools teams already use and that require minimal update overhead achieve higher adoption than specialized purpose-built dashboards. The overhead of maintaining a planning view is itself a signal-to-noise problem: if updating the view costs more attention than the view provides, teams stop updating it, and it becomes stale noise. [PRAC]

---

## Sticky vs. Abandoned Planning Views: The Pattern

Drawing across practitioner accounts, sticky planning views share these characteristics:

- **Single decision they answer.** Each retained dashboard in the cloud engineering case study had one clear purpose. Sticky planning views answer one question that comes up repeatedly in the team's decision-making cycle.
- **Clear owner.** Dashboards without owners go stale. Sticky views have a person whose job it is to keep the status current.
- **Minimal update cost.** Intercom's Trello boards, Basecamp's hill chart (human-felt status, not computed), and the surviving Jira boards all minimize the friction of updating. If updating the status requires significant time, it doesn't happen.
- **Motion visible over time.** The hill chart's second-order view — showing change between states — is more useful than any snapshot. Sticky views show trend, not just current state.
- **Directly connected to the next decision.** Intercom's weekly goal tracking was connected directly to releases. The cloud engineering dashboards were connected directly to incident response. The planning view that feeds a recurring decision gets used; the one that exists for documentation gets ignored.

Abandoned views share opposing characteristics: multiple purposes, no clear owner, high update cost, snapshot-only (no trend), and disconnected from any recurring decision the team actually makes.

---

## Layout Patterns That Cause Cognitive Overload

From practitioner accounts, the following layout choices consistently cause disengagement:

- **Equal visual weight across all metrics.** No hierarchy signals no priority. The viewer must do all the interpretation work.
- **More than 6-7 modules or panels visible simultaneously.** (This confirms the 9-module ceiling finding referenced in prior research context.)
- **Mixed abstraction levels.** Planning views that mix strategic signals (quarterly objectives) with tactical details (individual task status) in the same panel force constant context-switching.
- **Status that requires interpretation.** Velocity, burndown, and RICE scores require the viewer to do calculation to extract meaning. Status that shows meaning directly (blocked/unblocked, uphill/downhill, on-track/at-risk) requires less interpretation overhead.
- **Chronologically stale data without staleness indication.** Stale status displayed as current is worse than no status, because it creates false confidence. Practitioners note that teams learn to distrust boards that are frequently stale, and then stop looking at them entirely.

---

## Implications for CLI/Terminal Planning Views

The practitioner findings have specific implications for a Claude Code / cmux planning artifact rendered in a terminal:

- **Prioritize motion over snapshot.** The hill chart's most valuable property is showing change between states. A terminal planning view that only shows current status misses the most decision-relevant signal.
- **Enforce a single primary question.** The view should be answerable without interpretation: "What needs attention right now?"
- **Minimize update surface.** If the status must be manually maintained, friction determines adoption. Auto-derivable signals (from git state, file timestamps, linked story status) survive; manually curated signals decay.
- **Three to five features maximum in active view.** Beyond this, the view becomes a list rather than a decision tool.
- **Show the uncertainty dimension.** Basecamp's uphill/downhill framing is directly portable to a feature status view. The equivalent question: is this feature still in the "figuring out" phase, or is it in execution? This single bit of information changes what the team does next.

---

## Sources

- [OFFICIAL] Basecamp / Ryan Singer, "New in Basecamp: See where projects really stand with the Hill Chart," Signal v. Noise / Medium — https://medium.com/signal-v-noise/new-in-basecamp-see-where-projects-really-stand-with-the-hill-chart-ca5a6c47e987

- [OFFICIAL] Basecamp, "Show Progress," Shape Up, Chapter 13 — https://basecamp.com/shapeup/3.4-chapter-13

- [PRAC] "We Deleted 60% of Our Dashboards. Observability Got Better." The Cloud Playbook, February 2026 — https://www.thecloudplaybook.com/p/deleted-dashboards-observability-got-better

- [PRAC] Ayush Jha, "Why Most Dashboards Fail (And How to Design Ones That Actually Drive Decisions)," Medium, February 2026 — https://medium.com/@ayushanandjha/why-most-dashboards-fail-and-how-to-design-ones-that-actually-drive-decisions-2d2f5fe4ba5b

- [PRAC] Abdul Osman, "The Metrics Mirage: When Dashboards Become the Theatre of Competence," DEV Community — https://dev.to/abdulosman/the-metrics-mirage-when-dashboards-become-the-theatre-of-competence-1g6o

- [PRAC] Sigma Computing, "Drowning in Dashboards? Here's How to Fix Data Fatigue" — https://www.sigmacomputing.com/blog/data-fatigue

- [PRAC] Intercom, "What we learned from scaling a product team," Medium / Inside Intercom — https://medium.com/intercom-inside/what-we-learned-from-scaling-a-product-team-12e9d2e028b1

- [PRAC] Markus Müller, "The Playbook to fix your Product Roadmap," Medium — https://medium.com/@markusmuller89/the-playbook-to-fix-your-product-roadmap-1bd8da1ae344

- [PRAC] GainMomentum.ai, "Your Agile Project Management Tool Jira Is a Symptom, Not the Disease" — https://gainmomentum.ai/blog/agile-project-management-tools-jira

- [OFFICIAL] Atlassian, "New Atlassian research on developer experience highlights a major disconnect," Work Life by Atlassian, 2024 — https://www.atlassian.com/blog/developer/developer-experience-report-2024

- [PRAC] Lenny Rachitsky, "How Linear builds product," Lenny's Newsletter — https://www.lennysnewsletter.com/p/how-linear-builds-product

- [PRAC] Itamar Goldminz, "Hill Charts [Basecamp]," Medium / Org Hacking — https://medium.com/org-hacking/hill-charts-basecamp-44cbc22c9c92
