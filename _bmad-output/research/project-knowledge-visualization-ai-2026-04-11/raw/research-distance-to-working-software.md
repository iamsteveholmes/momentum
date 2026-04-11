---
content_origin: claude-code-subagent
date: 2026-04-11
sub_question: "How do software teams visualize 'distance to working software' — feature readiness indicators, integration status, end-to-end coverage metrics?"
topic: "Project knowledge visualization and cognitive load reduction in AI-assisted development"
---

## Overview

"Distance to working software" is not a single industry term — it is a compound concept assembled from several overlapping practices: Agile's seventh principle ("working software is the primary measure of progress"), Definition of Done frameworks, DORA delivery metrics, continuous delivery pipeline visibility, feature flag release management, and value stream mapping. No single tool or standard directly operationalizes the question "how many more steps until this capability works end-to-end?" — but the ecosystem has developed several proxies and partial answers, which are surveyed here.

---

## The Agile Foundation: Working Software as a Measurable Principle

Agile's seventh principle establishes working software as the primary measure of progress, but the Agile Manifesto itself gives no metric for it — only a philosophical priority. In practice, teams have had to invent measurement proxies. ([Agile Principle 7 — Springer Chapter](https://link.springer.com/chapter/10.1007/978-3-031-36429-7_14)) **[OFFICIAL]**

The core tension this sub-question addresses is between *task completion* and *capability delivery*: a team can check off every story in a sprint and still not have a working, user-visible feature. Stories are "done" individually but do not add up to something shippable. This is the "last mile" problem in feature delivery, and it is only partially addressed by current tooling.

---

## Definition of Done vs. Definition of Ready

Two guardrail frameworks bookend a story's lifecycle:

**Definition of Ready (DoR)** ensures a work item has sufficient specification to enter development — acceptance criteria written, dependencies identified, estimate agreed. It answers: "is this story safe to start?" ([Atlassian — Definition of Ready](https://www.atlassian.com/agile/project-management/definition-of-ready)) **[OFFICIAL]**

**Definition of Done (DoD)** ensures a work item has been fully developed, tested, integrated, and accepted before being declared complete. A well-crafted DoD includes code review, automated tests passing, integration tests passing, documentation updated, and deployment to a staging environment. ([Scrum Alliance — DoR vs DoD](https://resources.scrumalliance.org/Article/definition-vs-ready)) **[OFFICIAL]**

The critical distinction for "distance to working software": DoD applies at the story/task level, not the capability level. A capability may require five stories, all individually "Done" per DoD, but without integration, end-to-end testing, and user-facing configuration, the capability is not yet working. This gap is where most teams lose visibility. ([Agile Seekers — DoD for Features and Capabilities](https://agileseekers.com/blog/building-a-solid-definition-of-done-for-features-and-capabilities)) **[PRAC]**

Some practitioners define a **Definition of Release Ready** (DRR) at the feature or capability level — a separate checklist that gates deployment and includes production readiness criteria: monitoring configured, rollback plan validated, feature flag in place, documentation published. ([Release Management — Semaphore CI](https://semaphoreci.com/blog/release-management)) **[PRAC]** A 2025 production readiness guide from Port.io specifies that release readiness extends beyond code: it includes security posture, reliability validation, and performance benchmarks. ([Port.io — Production Readiness Checklist](https://www.port.io/blog/production-readiness-checklist-ensuring-smooth-deployments)) **[PRAC]**

---

## DORA Metrics: Flow Indicators as Readiness Proxies

The DORA (DevOps Research and Assessment) framework provides the most widely-adopted set of delivery performance indicators. The four core DORA metrics are: ([DORA.dev — Four Keys](https://dora.dev/guides/dora-metrics-four-keys/)) **[OFFICIAL]**

1. **Deployment Frequency** — how often code reaches production. High-performing teams deploy on-demand or multiple times daily; low performers deploy monthly or less.
2. **Lead Time for Changes** — time from code commit to production deployment. Elite teams achieve under one hour; low performers take one to six months.
3. **Change Failure Rate** — percentage of deployments causing production degradation.
4. **Failed Deployment Recovery Time** (formerly MTTR) — time to recover from a failure.

In 2025, DORA expanded to six dimensions, adding **Rework Rate** and a quasi-metric for **Reliability**. ([Faros.ai — DORA Report 2025 Takeaways](https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025)) **[PRAC]** DORA also moved from performance tiers to seven team archetypes blending delivery performance with human factors such as burnout and friction.

**What DORA tells you about distance to working software:** Lead Time is the closest DORA metric to "distance" — it measures the elapsed wall time from the moment code is written to the moment it is running for users. Deployment Frequency is a proxy for how fast the feedback loop closes. However, DORA metrics measure throughput and speed, not coverage — they don't tell you which capabilities are incomplete or how many more stories a feature needs before it works end-to-end.

The 2025 DORA State of AI-Assisted Software Development report found that AI coding tools increase individual output (21% more tasks completed, 98% more PRs merged) but do not automatically improve organizational delivery metrics — lead times and deployment frequency often remain flat. Higher AI adoption correlates with increased deployment instability in teams with weak processes. ([DORA — State of AI-Assisted Software Development 2025](https://dora.dev/dora-report-2025/)) **[OFFICIAL]**

GitLab natively surfaces DORA metrics in its CI/CD dashboards, making lead time and deployment frequency first-class project visibility indicators. ([GitLab Docs — DORA Metrics](https://docs.gitlab.com/user/analytics/dora_metrics/)) **[OFFICIAL]**

---

## Feature Flags and Release Readiness Platforms

Feature flags decouple *code deployment* from *feature activation*, creating an explicit intermediate state: code is in production but feature is off. This provides a concrete mechanism for tracking release readiness at the capability level.

**LaunchDarkly** has evolved into a full feature delivery platform with four pillars: Release Management, Observability & Monitoring, Analytics & Experimentation, and AI Configs. Its observability layer connects error rate increases to specific flag changes, enabling teams to see exactly which feature rollout is causing regressions. ([LaunchDarkly — Architecture Deep Dive](https://launchdarkly.com/docs/tutorials/ld-arch-deep-dive)) **[OFFICIAL]**

**Harness (formerly Split.io)** differentiates on metrics correlation: when a flag is toggled, it surfaces whether conversion rates, latency, or error rates changed. This turns feature activation into a measurable readiness gate. ([Flagsmith — LaunchDarkly vs Split](https://www.flagsmith.com/compare/launchdarkly-vs-split)) **[PRAC]**

Feature flags represent a practical answer to "is this feature ready?": a feature that has been deployed behind a flag, is being rolled out to a percentage cohort, and shows no metric regression is measurably closer to working software than one that is still in a feature branch. The flag's rollout percentage becomes a visual readiness indicator (0% → 10% → 100% = full delivery).

---

## Continuous Delivery Pipelines as Distance Indicators

CI/CD pipelines make "distance to deployment" explicit through stage gates. A feature's position in the pipeline (build → unit test → integration test → staging → production) directly encodes how close it is to being working software. Key CI/CD metrics that serve as readiness indicators: ([TestRail — CI Metrics](https://www.testrail.com/blog/continuous-integration-metrics/)) **[PRAC]**

- **Test pass rate** — percentage of automated tests passing; a failing suite blocks forward movement
- **Build duration** — longer builds indicate integration friction
- **Deployment frequency** — how often features successfully traverse the full pipeline
- **Pipeline success rate** — percentage of pipeline runs that reach production

Datadog's Continuous Delivery Visibility feature aggregates pipeline telemetry and makes stage-level bottlenecks visible across all services and teams. ([Datadog — Continuous Delivery Visibility](https://docs.datadoghq.com/continuous_delivery/)) **[OFFICIAL]**

The Pipeline Driven framework for CD metrics proposes tracking *flow efficiency* — the ratio of active work time to total elapsed time — as a readiness signal. A feature spending 80% of its time waiting in queues is far from working software regardless of its story status. ([Pipeline Driven — CD Metrics Framework](https://pipelinedriven.org/article/a-metrics-framework-for-continuous-delivery)) **[PRAC]**

---

## Value Stream Mapping: End-to-End Flow Visualization

Value Stream Mapping (VSM) creates a visual diagram of every step in the software delivery process — from ideation through deployment — surfacing where time is lost, where handoffs stall, and where queues accumulate. ([DORA.dev — Value Stream Mapping](https://dora.dev/guides/value-stream-management/)) **[OFFICIAL]**

VSM directly addresses "distance to working software" by making the full path visible: if a feature needs to traverse design → development → code review → QA → staging → production, VSM quantifies how long each transition takes and where work accumulates. The *work in progress* at each stage is the literal distance remaining.

Tools in 2025 that provide VSM-style visibility for software delivery: ([Axify — VSM Tools](https://axify.io/blog/value-stream-mapping-tools)) **[PRAC]**

- **Jellyfish** — visualizes status transitions, queue times, and handoffs showing how issues progress across planning, development, review, testing, and release
- **ConnectALL** — end-to-end traceability across the delivery value stream with cross-tool integration
- **Planview** — enterprise VSM platform linking features to delivery timelines
- **Axify** — dedicated VSM tool for software engineering teams with flow metrics

Cumulative Flow Diagrams (CFDs) are the most common lightweight VSM proxy — a stacked area chart showing work items at each pipeline stage over time. The horizontal gap between bands shows cycle time; the vertical gap shows WIP. ([Monday.com — CFD Guide](https://monday.com/blog/project-management/cumulative-flow-diagrams/)) **[PRAC]** Jira, Azure DevOps, and YouTrack generate CFDs automatically from workflow state data. ([Atlassian — CFD in Jira](https://support.atlassian.com/jira-software-cloud/docs/what-is-the-cumulative-flow-diagram/)) **[OFFICIAL]**

---

## Story Mapping and the Walking Skeleton

User Story Mapping (Jeff Patton's technique) provides a capability-centric view that directly addresses the "stories done but feature not working" problem. The map organizes user activities across the top (horizontal) and their supporting stories vertically underneath. A horizontal cut across the map defines a release — everything above the line is the minimum required for that release to be usable. ([Agile Alliance — Story Mapping](https://agilealliance.org/glossary/story-mapping/)) **[OFFICIAL]**

The **walking skeleton** is the first horizontal release slice — a thin, end-to-end implementation of the most critical path. It is explicitly about creating something that works (however minimally) before adding depth. ([J. Patton Associates — Story Mapping PDF](https://www.jpattonassociates.com/wp-content/uploads/2015/03/story_mapping.pdf)) **[OFFICIAL]** [Note: This resource is from 2015 — the concept is foundational and stable.]

Vertical slicing extends this: each story should deliver a user-visible, testable slice of functionality that cuts through all technical layers. A story that only implements a backend API without the UI to call it and the test to validate it is not a vertical slice — it's a horizontal slab that doesn't reduce "distance to working software." ([DEV Community — Vertical Slicing](https://dev.to/jan/user-stories-and-vertical-slicing-1dpo)) **[PRAC]**

---

## SAFe and Scaled Frameworks: Program-Level Readiness

In scaled frameworks, Program Increment (PI) planning creates explicit feature-level readiness tracking. SAFe tracks: ([Scaled Agile Framework — PI Planning](https://framework.scaledagile.com/pi-planning)) **[OFFICIAL]**

- **PI Objectives** — team-level and program-level commitments with business value scores
- **Feature completion percentage** — how many features committed in PI planning are delivered by PI end
- **Predictability metric** — ratio of planned to actual business value delivered; 80–100% indicates a stable, well-aligned program

SAFe's Measure and Grow approach adds flow metrics: flow distribution, velocity, time, load, efficiency, and predictability. ([SAFe — Measure and Grow](https://framework.scaledagile.com/measure-and-grow)) **[OFFICIAL]** These give a portfolio-level view of how close features are to being delivered.

---

## Engineering Intelligence Platforms (2025 State)

A category of "Engineering Intelligence" or "Developer Productivity Insight" platforms has emerged that aggregates delivery signals: ([Coderbuds — Engineering Metrics Tools 2025](https://coderbuds.com/blog/engineering-metrics-tools-comparison-2025)) **[PRAC]**

- **LinearB** — workflow automation with DORA metrics, git activity analytics, and sprint tracking
- **Swarmia** — developer-first DORA dashboards with team health indicators
- **Jellyfish** — connects engineering investment to business outcomes; strongest for executive reporting
- **DX (formerly GetDX)** — focuses on developer experience signals alongside delivery metrics

None of these platforms specifically frame their output as "distance to working software." They measure delivery throughput, not feature coverage or capability completeness. The concept of "how many more stories does this epic need before the capability is usable?" is not natively answered by any of these tools as of April 2026.

---

## The Gap: What Doesn't Exist

Across all the reviewed frameworks, tooling, and practices, a consistent gap emerges: **no mainstream tool or framework specifically models "how many more steps until this end-to-end capability works."** The closest approximations are:

1. **Story maps with release cuts** — show what's needed for a minimum working release, but require manual curation and don't auto-update from execution state
2. **Feature flags at 0%** — signal that code is deployed but the feature isn't on yet; the flag rollout percentage is an implicit readiness indicator
3. **CI/CD pipeline position** — shows where a specific deployment is in the pipeline, but not what functional capabilities it completes or leaves incomplete
4. **Cumulative Flow Diagrams** — show aggregate WIP but don't connect to user-visible capabilities
5. **PI Feature Completion %** — tracks feature delivery against PI plan but only within the SAFe ceremony structure

What's missing is a **capability dependency graph** — a view that says: "Feature X requires stories A, B, C, and D. A and B are done. C is in progress. D hasn't started. The feature is 50% done but 0% usable because C is the integration story that connects A+B to the user." This framing exists in theory (vertical slicing, walking skeleton) but is not operationalized in any tracked metric or visualization tool.

---

## Implications for AI-Assisted Solo Development

For a solo AI-assisted developer (the Momentum context), the problem is amplified: there is no standup to surface "I finished the API but the UI isn't wired up yet." The developer must carry this dependency state in working memory or lose track of it. The 2025 DORA AI report confirms that AI tools increase story-level throughput (more PRs merged) without improving end-to-end delivery — the "last mile" gap gets wider, not narrower, as AI accelerates story-level completion. ([DORA — State of AI-Assisted Development 2025](https://dora.dev/dora-report-2025/)) **[OFFICIAL]**

Tools like ZenHub have added AI sprint summaries and risk identification for team contexts, but solo developer tooling remains focused on code assistance (Copilot, Cursor) rather than capability-level readiness visibility. ([ZenHub — AI Sprint Planning](https://www.zenhub.com/blog-posts/the-7-best-ai-assisted-sprint-planning-tools-for-agile-teams-in-2025)) **[PRAC]**

---

## Summary of Key Findings

| Approach | What It Measures | Distance Signal Strength | Gap |
|---|---|---|---|
| Definition of Done | Story-level completeness | Low — story ≠ capability | Doesn't aggregate to feature readiness |
| DORA Lead Time | Elapsed time commit→deploy | Medium — speed proxy | Doesn't model capability coverage |
| Feature Flags (% rollout) | Deployment vs. activation state | Medium — explicit on/off | Doesn't show what's still needed |
| CI/CD Pipeline Stage | Current deployment position | Low-Medium | Doesn't connect to user capabilities |
| Cumulative Flow Diagram | WIP distribution across stages | Low — aggregate only | No capability-level resolution |
| Story Map + Release Cuts | Capability completeness plan | High — if kept current | Requires manual curation; no auto-sync |
| Walking Skeleton | Minimum end-to-end path | High — concept | Not a tracked metric; design heuristic only |
| SAFe PI Feature % | Feature delivery predictability | Medium-High | Requires SAFe ceremony structure |
| Value Stream Mapping | End-to-end flow bottlenecks | Medium | Operational, not planning-oriented |

---

## Sources

- [DORA — Four Keys Metrics Guide](https://dora.dev/guides/dora-metrics-four-keys/)
- [DORA — State of AI-Assisted Software Development 2025](https://dora.dev/dora-report-2025/)
- [DORA — Value Stream Mapping Guide](https://dora.dev/guides/value-stream-management/)
- [GitLab Docs — DORA Metrics](https://docs.gitlab.com/user/analytics/dora_metrics/)
- [Google Cloud — 2025 DORA AI-Assisted Dev Report](https://cloud.google.com/resources/content/2025-dora-ai-assisted-software-development-report)
- [Faros.ai — DORA Report 2025 Key Takeaways](https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025)
- [Octopus Deploy — DORA Metrics 2024/25](https://octopus.com/devops/metrics/dora-metrics/)
- [Atlassian — Definition of Ready](https://www.atlassian.com/agile/project-management/definition-of-ready)
- [Scrum Alliance — DoR vs DoD](https://resources.scrumalliance.org/Article/definition-vs-ready)
- [Semaphore CI — Release Management: DoR and DoD](https://semaphoreci.com/blog/release-management)
- [Agile Seekers — DoD for Features and Capabilities](https://agileseekers.com/blog/building-a-solid-definition-of-done-for-features-and-capabilities)
- [Port.io — Production Readiness Checklist](https://www.port.io/blog/production-readiness-checklist-ensuring-smooth-deployments)
- [LaunchDarkly — Architecture Deep Dive](https://launchdarkly.com/docs/tutorials/ld-arch-deep-dive)
- [Flagsmith — LaunchDarkly vs Split Comparison](https://www.flagsmith.com/compare/launchdarkly-vs-split)
- [Atlassian — CFD in Jira](https://support.atlassian.com/jira-software-cloud/docs/what-is-the-cumulative-flow-diagram/)
- [Monday.com — Cumulative Flow Diagrams](https://monday.com/blog/project-management/cumulative-flow-diagrams/)
- [Datadog — Continuous Delivery Visibility](https://docs.datadoghq.com/continuous_delivery/)
- [TestRail — CI Metrics](https://www.testrail.com/blog/continuous-integration-metrics/)
- [Pipeline Driven — CD Metrics Framework](https://pipelinedriven.org/article/a-metrics-framework-for-continuous-delivery)
- [Agile Alliance — Story Mapping](https://agilealliance.org/glossary/story-mapping/)
- [J. Patton Associates — Story Mapping PDF](https://www.jpattonassociates.com/wp-content/uploads/2015/03/story_mapping.pdf) [Note: 2015 source — foundational concept, stable]
- [DEV Community — Vertical Slicing](https://dev.to/jan/user-stories-and-vertical-slicing-1dpo)
- [Scaled Agile Framework — PI Planning](https://framework.scaledagile.com/pi-planning)
- [Scaled Agile Framework — Measure and Grow](https://framework.scaledagile.com/measure-and-grow)
- [Atlassian — DORA Metrics](https://www.atlassian.com/devops/frameworks/dora-metrics)
- [Axify — Value Stream Mapping Tools](https://axify.io/blog/value-stream-mapping-tools)
- [GetDX — Agile Metrics What They Really Measure](https://getdx.com/blog/agile-metrics/)
- [Springer — Agile Principle 7 Chapter](https://link.springer.com/chapter/10.1007/978-3-031-36429-7_14)
- [Coderbuds — Engineering Metrics Tools Comparison 2025](https://coderbuds.com/blog/engineering-metrics-tools-comparison-2025)
- [ZenHub — AI-Assisted Sprint Planning Tools 2025](https://www.zenhub.com/blog-posts/the-7-best-ai-assisted-sprint-planning-tools-for-agile-teams-in-2025)
