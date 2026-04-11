---
content_origin: human
date: 2026-04-11
topic: "Project knowledge visualization and cognitive load reduction in AI-assisted development"
respondent: Steve Holmes
---

# Practitioner Notes — Q&A Phase

## Q1 — Unverified Statistic (39% enterprise AI failure / context problems)

**Decision:** Keep the statistic but mark explicitly as unverified. Add a note that the primary source (Microsoft/Salesforce research) was not directly verified — only encountered via a practitioner blog (LogRocket). Do not present as authoritative empirical data.

---

## Q2 — Cross-Reference Gap (AI tools file ↔ context-fragmentation file)

**Decision:** Add a cross-reference between the two files before synthesis. Both files conclude "Momentum is positioned to fill this gap" — the cross-reference should make the complementary analyses visible to the synthesis agent.

---

## Q3 — What "Working Software" Means (Nornspun context)

**Connectivity/infrastructure layer:**
- An API endpoint is "working" when the client app connects and can successfully call it.
- A chat connection is "working" when it connects and responds.

**Flow layer:**
- A flow is "working" when a user can complete it end-to-end.
- Example: "If a user cannot initialize a campaign in Nornspun, nothing about the app is working."
- Example: "If they can't prep a game E2E, that feature doesn't work."

**Current state (critical insight):**
- No features in Nornspun currently work E2E even though many individual stories have been completed.
- This is the core problem: stories being "done" does not translate to working features.
- The gap between "stories completed" and "something a user can actually do" is the central visibility problem.

**Visual/UX layer:**
- "Working" is not only about functional flows — look and feel across all three client platforms is also a dimension of "working."
- This may include: screenshots of actual app states, future wireframes for comparison, visual consistency tracking across iOS, Android, and web.
- Example: "I might want actual screenshots of various states along with future wireframes."

**What the visualization needs to answer for Nornspun:**
- Which flows work E2E? Which don't?
- Which API/connection layers are functional?
- What does the app look like across client platforms today vs. target?

---

## Q3b — What "Working Software" Means (Momentum context)

Momentum is fundamentally different from Nornspun — it is an SDLC practice, not a user-facing app. The visualization questions are different:

- **How all skills work together** — not story-level, but workflow-level: how does Impetus connect to sprint-planning, to sprint-dev, to retro, etc.?
- **Impetus interactions** — what workflows does Impetus gate? What is it missing?
- **Skill gaps and process gaps** — e.g., triage exists as a placeholder but isn't built. What other gaps exist?
- **Skill redundancy** — where can skills be eliminated or combined?
- **SDLC completeness** — can I see the entire practice lifecycle at once and identify what's covered vs. uncovered?

"That's a different level of thinking than I'm able to accomplish talking about stories and epics."

The two projects require fundamentally different visualization frameworks:
- Nornspun → user-capability + flow-completeness + visual/UX tracking
- Momentum → skill-topology + SDLC coverage + process gap mapping

---

## Q4 — The Feature Layer Problem

**Current state:**
- Features are largely defined in the PRD.
- Implementation is spread across stories — no explicit link back to features.
- Epics are higher-level than features and are thematic containers, not feature containers.
- "Epics are really containers for stories that follow a theme. A feature isn't about a theme."

**The gap:**
- No explicit "Feature" artifact exists in the current workflow that maps to "what a user can accomplish."
- Stories implement code. Epics group themes. Neither maps cleanly to user-facing capabilities.

**Proposed feature definition (working draft):**
- "Something an app does" — but this is acknowledged as incomplete because look-and-feel is obviously also a feature.
- Functional feature: something a user can accomplish (initialize a campaign, prep a game E2E, complete a flow).
- Quality feature: something a user can observe or feel (visual consistency, responsiveness, platform fidelity).

**Key insight from Steve:**
- Epics are important AND features are important — they serve different purposes.
- "Agent UX" is an epic (thematic container). Specific UX behaviors within agents are features (user-observable qualities).
- Both need to be tracked. Neither replaces the other.

**Open question to resolve in synthesis:**
- How should a Feature artifact be defined within the Momentum practice to bridge PRD-level descriptions and story-level implementation?
- What is the minimal metadata a Feature record needs: name, acceptance condition (E2E test?), status (working/partial/not-started), linked stories, linked PRD section?

**Steve's framing:** "I think you and I should think this through very carefully." — Feature definition is a design decision, not just a research question. The synthesis should propose a model, not just describe the gap.

**Refinement (confirmed by Steve):**
E2E flows ARE features — granularity does not determine what counts as a feature. "Campaign init" is a feature whether it takes 1 story or 15 — it has a bounded scope and a finite set of duties. The type distinctions (flow/connection/quality) are useful for evaluating working status, but the definition is the same at all levels:

> A feature is a finite, user-observable unit with a finite set of duties and a clear working/not-working acceptance condition.

The type taxonomy (flow = E2E journey, connection = infrastructure prerequisite, quality = observable state) informs *how* you evaluate status, not whether something qualifies as a feature.
