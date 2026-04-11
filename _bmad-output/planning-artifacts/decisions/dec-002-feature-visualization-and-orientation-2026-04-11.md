---
id: DEC-002
title: Feature Visualization and Developer Orientation — Feature Artifact, Status Skill, and Context Compression
date: '2026-04-11'
status: decided
source_research:
  - path: _bmad-output/research/project-knowledge-visualization-ai-2026-04-11/final/project-knowledge-visualization-ai-final-2026-04-11.md
    type: prior-research
    date: '2026-04-11'
architecture_decisions_affected:
  - DRIFT-006 superseded — momentum:feature-status is a standalone skill, not absorbed into Impetus/momentum-tools
  - Decision 4b extended — Impetus greeting states include cached feature status summary with staleness flag
---

# DEC-002: Feature Visualization and Developer Orientation

## Summary

Evaluated research findings on project knowledge visualization, cognitive load reduction, and context fragmentation in AI-assisted development. The core finding is that stories and epics complete while no user-facing capabilities emerge — because no artifact tracks "can a user do X yet?" Six recommendations were evaluated. Five were adopted or adapted; one (build order) was rejected as sprint planning's domain. The net direction: introduce a Feature artifact as the missing layer between PRD and stories, build a `momentum:feature-status` skill that actively evaluates feature coverage and gaps, and embed a cached feature summary into the Impetus greeting. Sprint-boundary context compression was also adopted to keep multi-sprint orientation coherent.

---

## Decisions

### D1: Introduce the Feature Artifact — ADOPT

**Research recommended:** A new artifact type — `features.json` or per-feature files in a `features/` directory — explicitly modeling user-facing capabilities as persistent, trackable units with acceptance conditions, type taxonomy (flow/connection/quality), status, and story links. A Feature is a finite, user-observable unit with a finite set of duties and a clear working/not-working acceptance condition. Granularity does not determine what counts as a feature — E2E flows are features.

**Decision:** Adopt as recommended. The minimal schema: `feature_slug`, `name`, `type`, `description`, `acceptance_condition`, `status` (working/partial/not-working/not-started), `prd_section`, `stories`, `stories_done`, `stories_remaining`, `last_verified`, `notes`. Features and epics are orthogonal — epics group by theme, features group by user-observable capability.

**Rationale:** Stories and epics complete but no user-facing capabilities complete. The goal is to be able to review what it will take to get functionality completed for users — better look and feel, working flows, shippable capabilities. These are what sprints should focus on, not functional themes or individually prioritized stories.

---

### D2: Build `momentum:feature-status` Skill — ADAPT

**Research recommended:** An on-demand skill reading `features.json`, cross-referencing story statuses, producing a compact feature status view with two rendering paths: product projects (flow/connection/quality feature tracking) and practice projects (skill topology + SDLC coverage mapping).

**Decision:** Adopt with adaptation. The skill must actively evaluate each feature for coverage gaps — not just report story counts. It must surface: which stories and requirements implement the feature, whether the assigned story set is sufficient to deliver the full acceptance condition, and explicit gap flags for features where coverage is incomplete. Feature gap analysis is a first-class output, not a side effect.

**Rationale:** Feature status will drive sprint planning — it is the first thing reviewed when prioritizing. A skill that only reads status is not enough; it must evaluate whether what is planned will actually get the feature to working. This supersedes the prior DRIFT-006 decision that momentum:status would be absorbed into Impetus/momentum-tools. Feature-status is a standalone skill.

---

### D3: Embed Feature Context in Impetus Greeting — ADAPT

**Research recommended:** Extend Impetus session startup to include a one-line feature status summary pre-computed by the preflight script.

**Decision:** Adopt with adaptation. Impetus shows a **cached** feature status summary in the greeting, not a live-computed one. Cache validity is determined by hashing the inputs to feature-status (at minimum: `features.json` + `stories/index.json`). If the hash matches the stored hash, show the cached summary silently. If the hash differs, show the cached summary with a staleness flag: "feature status may be out of date — run feature-status to refresh." Full recomputation is user-triggered, never on startup.

**Rationale:** Impetus startup is already too slow. A full feature-status evaluation will take minutes — unacceptable at session start. The developer will explicitly ask for a refresh when they need current state. Stale-but-fast is better than accurate-but-slow for a greeting. This extends Decision 4b's 9-state greeting model with the cached feature status line.

---

### D4: Add Sprint-Boundary Context Compression — ADOPT

**Research recommended:** At sprint close (triggered by retro completion), automatically produce a structured sprint summary artifact: features advanced, stories completed vs. planned, key decisions, unresolved issues, one-paragraph narrative. Agents starting new sprints load the most recent sprint summary rather than raw sprint logs.

**Decision:** Adopt as recommended.

**Rationale:** Without a structured summary at sprint close, the next sprint starts without knowing what was actually accomplished — which features advanced, which decisions were made, which issues were carried forward. This keeps both developer and agent oriented on what matters rather than getting lost re-reading raw sprint logs. The goal is to stay on topic: sprint-boundary compression tells us exactly what we need at the start of each cycle.

---

### D5: Differentiate Product and Practice Visualization Paths — ADOPT

**Research recommended:** Two rendering paths within `momentum:feature-status`. Product projects get the feature type taxonomy with acceptance condition tracking and story-to-feature coverage mapping. Practice projects get skill topology view, SDLC coverage mapping, and redundancy detection.

**Decision:** Adopt as recommended. Project type determined by config field or artifact structure inference.

**Rationale:** Different project types have fundamentally different success indicators. A heavy UI app like Nornspun needs screenshots, visual consistency tracking, and E2E flow verification. Momentum is primarily about workflow continuity — how skills connect and hand off. A single visualization framework would produce something useless for both. The visualization must show the user what they need to focus on for their specific project type, not a generic output.

---

### D6: Prescribe Build Order — REJECT

**Research recommended:** A specific incremental build order: Feature schema → feature-status skill → Impetus greeting integration → sprint-boundary compression → practice project rendering.

**Decision:** Reject. Build order is sprint planning's domain, not a decision to lock in here.

**Rationale:** Dependencies between decisions (e.g., feature artifact before feature-status skill) will surface naturally during sprint planning. Prescribing a sequence now is premature — some work may be parallelizable, priorities may shift, and sprint planning is the right mechanism for sequencing.

---

## Phased Implementation Notes

The adopted decisions imply the following story surface area (sequencing to be determined by sprint planning):

1. **Feature artifact schema** — define `features.json` schema, populate initial instances for Nornspun and Momentum
2. **`momentum:feature-status` skill** — reads features.json, cross-references stories/index.json, evaluates coverage gaps, produces rendering per project type
3. **Impetus greeting cache integration** — hash-based staleness detection, cached feature summary in greeting with staleness flag
4. **Sprint-boundary compression** — retro completion trigger, structured sprint summary artifact
5. **Practice project rendering path** — skill topology + SDLC coverage map for Momentum

## Decision Gates

- D3 (Impetus cache) cannot be implemented before D2 (feature-status skill) — the cache stores feature-status output
- D2 (feature-status skill) cannot be implemented before D1 (feature artifact schema) — the skill reads features.json
- D4 (sprint-boundary compression) is independent of D1/D2/D3 and can proceed in parallel
- D5 (practice project rendering) is an extension of D2 and depends on the base skill existing
