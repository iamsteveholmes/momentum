---
content_origin: claude-code-subagent
date: 2026-04-13
sub_question: "What does 'feature as unit of user value' look like in practice — how do leading teams define and enforce a done state at the value-delivery level rather than task completion?"
topic: "Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps"
---

# Feature as Unit of User Value: Defining Done at Value-Delivery Level

## Overview

The question of when software development work is genuinely "done" sits at the heart of every Agile reform debate. The dominant Agile practice treats "done" as a quality gate at the task or story level: tests pass, code is reviewed, acceptance criteria are met. But a persistent critique has grown louder — particularly as AI accelerates throughput — that task-level done has decoupled from user-level done. Teams can sustain near-perfect sprint completion rates while users experience no meaningful improvement. This research explores how leading practitioners, toolmakers, and frameworks are trying to close that gap by making user-accessible value delivery the atomic unit of "done."

---

## 1. The Core Problem: Delivery Without Value Realization

The fundamental tension is between output (work completed) and outcome (value delivered). A 2025 Medium article on outcome mapping for Agile teams articulates this structural failure clearly: "As backlogs expand, priorities shift, and delivery becomes the dominant focus, value creation becomes an unstated assumption rather than a measurable objective." [PRAC] The team ships stories but never asks whether users were actually helped.

AWS Prescriptive Guidance defines "done" in the context of value stream mapping with notable precision: "Done means that you have successfully instrumented and validated the deliverable. Ideally, it includes delivery to the end customer in production and monitoring that demonstrates the product is successfully implemented, functioning, and adopted." [OFFICIAL] Three distinct gates are embedded here: (1) production deployment, not just code-complete; (2) active monitoring proving the feature works; (3) evidence of user adoption. This is a materially higher bar than standard Agile definitions of done, which typically stop at merged pull requests and test passage.

The nkdagility.com value delivery resource reinforces this: "'Done' means live in production, not just code complete." [UNVERIFIED — site content summarized, URL: nkdagility.com/resources/value-delivery/] The shift is from treating completion as a development milestone to recognizing that value only exists when customers can access and benefit from the work.

---

## 2. Product Teams vs. Feature Teams: The Structural Root Cause

Marty Cagan's distinction between product teams and feature teams provides a useful structural lens for why feature-level done persists. Feature teams are given solutions to implement — they are measured on output delivery. Product teams are given problems to solve and held accountable for outcomes. [UNVERIFIED — widely attributed to SVPG; svpg.com/product-vs-feature-teams/ returned 403]

The distinction matters for AI-native development because AI agents dramatically lower the cost of implementing features. A team of AI-assisted developers can now implement twice as many features in the same sprint. If the measurement model is task/feature throughput, this looks like a productivity gain. If the measurement model is user outcomes, the picture is murkier — more features shipped does not necessarily mean more value delivered.

Cagan's empowered product team model reframes done: "You can see an improvement in the outcomes you've defined over time." [PRAC — age-of-product.com/marty-cagan-product-operating-model/] Done is not a boolean per feature; it is a directional movement in a metric. Teams succeed when they move the needle, not when they ship the thing.

---

## 3. Outcome-Based Roadmaps: The Planning-Level Enforcement Mechanism

The most operationalized version of value-based done comes from outcome-based roadmapping. Rather than listing features on a roadmap, teams list measurable outcomes — behavioral or metric changes the product should drive — and treat feature work as hypotheses toward those outcomes.

Teresa Torres, whose continuous discovery work is influential in product-led circles, describes how this enforces accountability: outcomes make it "clear if a team accomplished their commitment" by providing measurable benchmarks. Teams succeed when they achieve the target metric — not when they ship a specific feature. [PRAC — producttalk.org/product-roadmaps/] She structures this as: executive teams define business outcomes (revenue, retention, market share); product teams translate these into product outcomes (specific behavioral changes); each team commits to one outcome per quarter.

Product School's treatment of outcome-based roadmaps describes the enforcement mechanisms in practice: continuous evaluation loops assess whether initiatives are actually moving metrics; real-time analytics dashboards (Google Analytics, Mixpanel) track outcomes continuously; and cross-functional alignment is maintained by tying every initiative explicitly to a measurable outcome. [PRAC — productschool.com/blog/product-strategy/outcome-based-roadmap] The critical operational implication is that "done" becomes a function of measurement, not shipping. A feature that ships but does not move the metric is not done in any meaningful sense.

Steve Forbes (practitioner blog, 2025) captures the cultural flip: "Feature-based roadmaps celebrate delivery dates. Outcome-led roadmaps celebrate movement in metrics." [PRAC — steveforbes.com.au/blog/2025/7/31/making-the-shift-from-feature-based-to-outcome-led-roadmaps]

---

## 4. Progressive Delivery: Decoupling Deployment from Release

Feature flags and progressive delivery provide a technical mechanism for enforcing value-based done that is now standard practice in mature engineering organizations. The key insight is that deployment (code reaching production) and release (users accessing the code) are distinct events, and "done" should be pegged to the release event — not the deployment event.

LaunchDarkly, Unleash, and Flagsmith are the dominant tooling [OFFICIAL — launchdarkly.com/guides/progressive-delivery/, getunleash.io/blog/progressive-delivery-with-feature-flags, flagsmith.com/blog/progressive-delivery], and their shared pattern is:

1. Code ships to production in a disabled state.
2. Feature is verified for infrastructure stability at 0% rollout.
3. Feature is released to progressively larger user segments (internal → early adopters → 10-25% → general availability).
4. Metrics are observed at each rollout stage before expansion.
5. Feature can be killed at any stage without redeployment.

This operationally enforces a distinction between "technically complete" and "value confirmed." A feature that passes internal testing but degrades a key metric during the 10% rollout is not done — it is recalled. The done state requires validated user value at production scale, not just passing test gates in lower environments.

The 2025 practitioner blog from featbit.co characterizes feature-flag-based development as having redefined the deployment-release boundary: "Code is shipped to production in a disabled state, verified for infrastructure stability, then turned on for progressively larger user groups via configuration changes that take effect in seconds." [PRAC — featbit.co/articles2025/feature-flag-based-development-2025] The key enforcement this creates is that done is not a one-time gate; it is a staged validation sequence with explicit exit criteria at each stage.

---

## 5. Impact Mapping: Tracing Work Items to Business Outcomes

Impact mapping is a planning technique developed by Gojko Adzic that creates explicit traceability between deliverables and business goals. The structure is a four-level hierarchy: Goal (the why) → Actors (the who) → Impact (the how) → Deliverables (the what). [PRAC — agilepainrelief.com/blog/to-get-bang-for-your-buck-try-impact-mapping/]

The mechanism for enforcing value-based done in impact mapping is the constraint that "user stories should map to branches of an impact map. If they don't, a team knows they shouldn't prioritize that user story." [PRAC — scrum.org/resources/blog/extending-impact-mapping-gain-better-product-insights] This is a planning-level gate that filters out task work that cannot be connected to user value before development begins.

A 2025 Agile Insider article on outcome mapping (Medium) extends this by treating completion criteria as inherently outcome-linked: "True 'done' requires connecting individual work items to broader outcomes—ensuring that Agile velocity translates into tangible business results rather than merely checking tasks off backlogs." [PRAC — medium.com/agileinsider/outcome-mapping-for-agile-teams] The practical implementation involves adding an explicit "outcome linkage" field to story cards — each story must declare which branch of the impact map it advances before it can be accepted into a sprint.

---

## 6. Jobs-to-Be-Done Applied to AI Development

The Jobs-to-Be-Done (JTBD) framework — originally developed by Clayton Christensen and operationalized by Tony Ulwick — defines progress in terms of how well a product helps users accomplish a specific job. When applied to AI development, JTBD produces a radically different definition of done: "After launching a new feature or update, evaluate its success based on how well it helps users complete their job, rather than just adoption numbers. Use metrics like time saved, pain points removed, or workflow streamlined." [PRAC — strategyn.com/jobs-to-be-done/]

AKF Partners' 2024/2025 analysis of JTBD for AI/ML strategy argues that the framework "shifts the focus from merely implementing AI/ML for its own sake to strategically targeting labor-intensive tasks and optimizing them incrementally." [PRAC — akfpartners.com/growth-blog/maximizing-ai-ml-impact-jobs-to-be-done-product-strategy] The done state is not "the model is deployed" but "the job is now faster, less painful, or more accurate for the user."

The critical implication for AI-native development is that AI features need a qualitatively different definition of done than traditional software features. An AI feature may be technically complete — model runs, API responds — while completely failing the JTBD test if the output does not actually help users complete their job. JTBD-based done gates require: (1) identification of the specific job being hired for; (2) baseline measurement of how users perform that job today; (3) post-deployment measurement comparing the new performance. Without all three, the feature cannot be declared done.

---

## 7. Product-Led Growth: Instrumented Value Milestones

Product-Led Growth (PLG) organizations have developed the most operationalized version of value-based done in the industry, driven by the economic necessity of demonstrating user value before asking for payment. PLG defines done through time-to-value (TTV) and activation metrics rather than shipping metrics.

The key PLG constructs [PRAC — productled.org/foundations/product-led-growth-metrics, mixpanel.com/blog/product-led-growth/]:

- **Time to Value (TTV):** How fast does a new user achieve a meaningful outcome? "Faster TTV correlates to higher activation, retention, and monetization, making it a revenue driver."
- **Activation Rate:** What percentage of new users complete key actions indicating they've experienced the product's value?
- **Aha Moment:** The specific interaction or outcome that marks the transition from "I have the feature" to "this feature has helped me."

In PLG teams, a feature is not done when it ships — it is done when users demonstrably reach the Aha Moment. This requires instrumentation to be part of the definition of done: a feature cannot be declared complete unless event tracking is in place to observe whether users reach the value milestone. This is a concrete, enforceable gate that differs from traditional acceptance criteria in a critical way: it cannot be satisfied by the development team alone. It requires production data.

A 2025 industry analysis notes that PLG in 2025 "requires sophisticated strategies around PQL definition, Aha Moment identification, Time-to-Value optimization, and strategic feature gating." [PRAC — salespanel.io/blog/marketing/what-is-product-led-growth/] The trend is toward products with "internal expansion loops that monitor usage hot spots, showcase collaboration bottlenecks, and suggest feature access" — meaning the instrumentation for value measurement is itself a first-class product capability.

---

## 8. Value Stream Management: Flow Metrics as Done Proxy

Value Stream Management (VSM) shifts the measurement frame from team velocity to end-to-end value flow. Rather than measuring how fast teams complete stories, VSM measures how fast value moves from idea to user. [PRAC — 6sigma.us/business-process-management-articles/top-value-stream-management-tools/]

The IT Revolution framework for value delivery in complex domains articulates the specific mechanisms: "Regular integrated demonstrations showing working system increments; Incremental delivery milestones tied to customer outcomes, not feature checklists; Flow metrics measuring how quickly value moves through the system." [PRAC — itrevolution.com/articles/accelerating-value-delivery-in-highly-complex-domains/]

Flow metrics [UNVERIFIED — standard VSM terminology] measure:
- **Flow time:** The elapsed time from when work is identified to when it reaches the user.
- **Flow efficiency:** The ratio of active work time to total flow time (wait time is waste).
- **Flow velocity:** The number of business items (features, risks, defects, debt) completed per time period.

The critical difference from story velocity is that flow time is measured to user delivery, not to merge. A story that sits merged for three weeks waiting for a release ceremony does not contribute positive flow efficiency — it is waste in the value stream.

---

## 9. The DORA Framework: Evolving Toward User Outcomes

The DORA metrics (Deployment Frequency, Lead Time for Change, Change Failure Rate, Time to Restore Service) are the dominant software delivery performance measurement framework. They have traditionally measured delivery process health, not user value delivery. [OFFICIAL — dora.dev/guides/dora-metrics/]

The 2025 DORA State of AI-Assisted Software Development report represents a significant evolution. The framework was renamed from "State of DevOps" to signal a shift in focus. Performance tiers were replaced by seven archetypes. New dimensions were added including team performance, product performance, friction, and burnout. [PRAC — redmonk.com/rstephens/2025/12/18/dora2025/] The "product performance" dimension is notable — it gestures toward measuring whether delivery translates into user value, not just whether delivery is fast and stable.

However, the 2025 report also contains an important warning relevant to this research question: "Improving metrics does not always improve outcomes — speed of deployment for its own sake is of little use to the end user if you're not shipping anything that improves their experience." [OFFICIAL — dora.dev] This is an explicit acknowledgment that DORA's traditional metrics are not sufficient surrogates for user value delivery.

---

## 10. AI-Native Development: Amplifying the Gap

The shift to AI-assisted and AI-native development substantially amplifies the gap between task-level done and value-level done. The 2025 DORA AI report found that "AI adoption improves throughput but increases delivery instability." [OFFICIAL — cloud.google.com/resources/content/2025-dora-ai-assisted-software-development-report] More code ships faster; but stability — which is the closest DORA proxy for user impact — worsens.

The DEV Community analysis of AI-powered development workflows in 2026 identifies a specific structural change: "Traditional 'sprints' are being replaced by 'bolts' — shorter, more intense work cycles measured in hours or days rather than weeks." [PRAC — dev.to/devactivity/the-ai-powered-development-workflow-a-glimpse-into-2026-4h68] If the unit of work shrinks dramatically, the definition of done must correspondingly move up the abstraction stack to remain meaningful. Task-level done gates become less meaningful as tasks become trivially fast to complete; value-level gates become more important as the bottleneck shifts from development velocity to value validation.

The Red Hat Developer article on "Harness Engineering" (April 2026) — using the term in the sense of structured AI development workflows, distinct from Fowler/Böckeler's behavioral test harness and from OpenAI's reinforcement-learning usage — points toward a specific enforcement mechanism for AI-native development: structured harnesses that require acceptance criteria to be grounded in measurable outcomes at the point of task specification, not after the fact. "Completion involves verification against a structured checklist rather than vague requirements. Testing requirements explicitly defined within task specs. Acceptance criteria grounded in measurable outcomes (e.g., 'GET /api/v2/sbom/export?format=csv returns valid CSV')." [OFFICIAL — developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development] This is a planning-side enforcement mechanism: done is defined as measurable outcome before development begins.

The lean software delivery perspective from Eduardo Ferro (March 2025) adds an accountability dimension specific to AI-native workflows: "You build it, you run it" — the development agent (human or AI) retains accountability for production outcomes, not just code completion. [PRAC — eferro.net/2025/03/lean-software-delivery-empowering-team.html] Observability investment is required as part of done: "Provides product and technical performance visibility beyond sprint metrics."

---

## 11. Synthesis: What "Feature as Unit of User Value" Requires in Practice

Drawing across these patterns, a workable operationalization of feature-as-unit-of-user-value requires at least these structural elements:

**At the planning gate (before development begins):**
- Feature must link to an explicit outcome on an outcome roadmap or impact map
- Done criteria must be stated in terms of user behavior or metric change, not technical completion
- A measurement plan must exist: what data will confirm the outcome was achieved?

**At the shipping gate (deployment):**
- Code reaches production, not just a staging environment
- Instrumentation is in place before the flag is enabled for users
- Progressive delivery structure is established: internal → early adopters → broad rollout

**At the value validation gate (after rollout):**
- The defined metric or behavioral outcome is observed in production data
- Time-to-value for new users reaching the Aha Moment is measured
- Feature is either confirmed (metric moved) or recalled for revision

**Ongoing:**
- Flow metrics (not velocity) track whether value moves efficiently through the system
- Teams are accountable for metric movement over time, not one-time shipping events

The notable absence in most current practice is a formal "value validation gate" with explicit criteria for what constitutes confirmation that the outcome was achieved. Most teams have planning-side outcome statements but no production-side confirmation requirement before closing the feature. This is the value validation gap that the practitioner literature on outcome-based done states is working to close.

---

## Sources

- [AWS Prescriptive Guidance: Creating a Development Value Stream Map](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-devops-value-stream-mapping/create-value-stream-map.html)
- [DORA: Software Delivery Performance Metrics](https://dora.dev/guides/dora-metrics/)
- [DORA 2025: Measuring Software Delivery After AI — RedMonk](https://redmonk.com/rstephens/2025/12/18/dora2025/)
- [2025 DORA State of AI-Assisted Software Development — Google Cloud](https://cloud.google.com/resources/content/2025-dora-ai-assisted-software-development-report)
- [Outcome Mapping for Agile Teams — Agile Insider / Medium](https://medium.com/agileinsider/outcome-mapping-for-agile-teams-a-simple-way-to-connect-stories-to-value-e70c99542ad5)
- [Value Delivery: Aligning Iterative Releases with Customer Outcomes — NKD Agility](https://nkdagility.com/resources/value-delivery/)
- [Teresa Torres: Product Roadmaps — Product Talk](https://www.producttalk.org/product-roadmaps/)
- [Outcome-Based Roadmaps: Mapping Impact, Not Features — Product School](https://productschool.com/blog/product-strategy/outcome-based-roadmap)
- [Making the Shift From Feature-Based to Outcome-Led Roadmaps — Steve Forbes](https://www.steveforbes.com.au/blog/2025/7/31/making-the-shift-from-feature-based-to-outcome-led-roadmaps)
- [Feature vs. Outcome-Driven Product Roadmaps — Product Led Alliance](https://www.productledalliance.com/is-it-time-to-switch-from-feature-to-outcome-driven-product-roadmaps/)
- [Outcome-Driven Roadmapping — ProductPlan](https://www.productplan.com/learn/outcome-driven-roadmaps/)
- [How Feature Management Enables Progressive Delivery — LaunchDarkly](https://launchdarkly.com/guides/progressive-delivery/how-feature-management-enables-progressive-delivery/)
- [Progressive Delivery with Feature Flags — Unleash](https://www.getunleash.io/blog/progressive-delivery-with-feature-flags)
- [Moving to Progressive Delivery — Flagsmith](https://www.flagsmith.com/blog/progressive-delivery)
- [Feature Flag Based Development 2025 — FeatBit](https://www.featbit.co/articles2025/feature-flag-based-development-2025)
- [Impact Mapping — Agile Pain Relief](https://agilepainrelief.com/blog/to-get-bang-for-your-buck-try-impact-mapping/)
- [Extending Impact Mapping to Gain Better Product Insights — Scrum.org](https://www.scrum.org/resources/blog/extending-impact-mapping-gain-better-product-insights)
- [Jobs to Be Done Framework — Strategyn (Tony Ulwick)](https://strategyn.com/jobs-to-be-done/)
- [Maximizing AI/ML Impact: Jobs to Be Done — AKF Partners](https://akfpartners.com/growth-blog/maximizing-ai-ml-impact-jobs-to-be-done-product-strategy)
- [AI Strategy: A Practical Framework Using JTBD — Mike Boysen / Medium](https://medium.com/@mikeboysen/ai-strategy-a-practical-framework-using-jobs-to-be-done-jtbd-5e86f3fa7528)
- [Product-Led Growth Metrics — ProductLed.org](https://www.productled.org/foundations/product-led-growth-metrics)
- [Product-Led Growth in 2026 — Mixpanel](https://mixpanel.com/blog/product-led-growth/)
- [What Is Product-Led Growth in 2025? — Salespanel](https://salespanel.io/blog/marketing/what-is-product-led-growth/)
- [Accelerating Value Delivery in Highly Complex Domains — IT Revolution](https://itrevolution.com/articles/accelerating-value-delivery-in-highly-complex-domains/)
- [Lean Software Delivery: Empowering the Team — Eduardo Ferro](https://www.eferro.net/2025/03/lean-software-delivery-empowering-team.html)
- [The AI-Powered Development Workflow: A Glimpse into 2026 — DEV Community](https://dev.to/devactivity/the-ai-powered-development-workflow-a-glimpse-into-2026-4h68)
- [Harness Engineering: Structured Workflows for AI-Assisted Development — Red Hat Developer](https://developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development)
- [Empowered Product Teams — SVPG](https://www.svpg.com/empowered-product-teams/)
- [Marty Cagan on the Product Operating Model — Age of Product](https://age-of-product.com/marty-cagan-product-operating-model/)
- [VSM in DevOps — APWide](https://www.apwide.com/vsm-in-devops/)
- [Top Value Stream Management Tools in 2025 — SixSigma.us](https://www.6sigma.us/business-process-management-articles/top-value-stream-management-tools/)
