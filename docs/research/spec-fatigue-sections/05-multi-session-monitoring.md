# Section 5: Multi-Session/Concurrent Task Monitoring and Context Switching

## 5.1 Context Switching Costs in Software Development

### Weinberg's Overhead Model

Gerald Weinberg's *Quality Software Management* (1992) established the foundational heuristic for context switching overhead in software projects. His estimates show a dramatic, non-linear cost curve:

| Simultaneous Projects | % Time Lost to Switching |
|---|---|
| 1 | 0% |
| 2 | 20% |
| 3 | 40% |
| 5 | 75% |

Later empirical work found this slightly overstated -- developers on 2+ projects spent an average of 17% (not 20%) on cross-project interruptions -- but the non-linear scaling pattern holds.

Sources: [The Financial Cost of Task Switching (Scrum.org)](https://www.scrum.org/resources/blog/financial-cost-task-switching), [The Multi-Tasking Myth (Coding Horror)](https://blog.codinghorror.com/the-multi-tasking-myth/)

### Rubinstein, Meyer & Evans (2001) -- Executive Control

The foundational experimental study on task switching identified two distinct executive control stages: **goal shifting** (deciding to do the new task) and **rule activation** (loading the new task's rules while unloading the old). Rule activation alone costs several tenths of a second per switch, which compounds across frequent alternation. Task alternation yielded switching-time costs that increased with rule complexity.

Source: [Executive Control of Cognitive Processes in Task Switching, Journal of Experimental Psychology: Human Perception and Performance, 27(4), 763-797](https://psycnet.apa.org/record/2001-07721-001)

### Gloria Mark -- Interruption Recovery

Gloria Mark's research at UC Irvine found that after an interruption, workers take an average of **23 minutes, 15 seconds** to return to the original task, passing through more than **2 intermediate tasks** before resuming. The recovery time figure comes from Mark's field observations (widely cited from interviews; the specific number does not appear in the published CHI papers). Her 2005 CHI paper ("No Task Left Behind?") established the fragmented work pattern and intermediate task finding. Her 2008 CHI paper found significantly higher stress, frustration, mental effort, and time pressure when interrupted (measured via NASA-TLX workload scale), and that interrupted workers completed tasks faster but at the cost of increased workload.

Sources: [No Task Left Behind? Examining the Nature of Fragmented Work (CHI 2005)](https://ics.uci.edu/~gmark/CHI2005.pdf), [The Cost of Interrupted Work: More Speed and Stress (CHI 2008)](https://ics.uci.edu/~gmark/chi08-mark.pdf), [Attention Span -- Gloria Mark](https://gloriamark.com/attention-span/)

### Iqbal & Horvitz (2007) -- Microsoft Research

A field study at Microsoft Research logging real user behavior found that alert-triggered task switches consumed **10 minutes** on the interrupting task plus **10-15 additional minutes** of other work before returning to the original task. Critically, **27% of task switches resulted in more than 2 hours** away from the original task.

Source: [Disruption and Recovery of Computing Tasks: Field Study, Analysis, and Directions (CHI 2007)](https://www.microsoft.com/en-us/research/publication/disruption-recovery-computing-tasks-field-study-analysis-directions/)

### Parnin & Rugaber -- Programmer Interruptions

An analysis of 10,000 recorded sessions from 86 programmers and a survey of 414 programmers found that only **10% of sessions** had programming activity resume in less than 1 minute after an interruption, and only **7% of sessions** involved no navigation to other code locations before the programmer could start editing again. Programmers reported compulsively building the project to check for compile errors as a resumption strategy -- essentially using the compiler as an external memory aid.

Source: [Resumption Strategies for Interrupted Programming Tasks, Parnin & Rugaber, Software Quality Journal (2011)](https://link.springer.com/article/10.1007/s11219-010-9104-9)

### Application to Concurrent AI Agent Sessions

These findings map directly to multi-agent supervision. Each agent session is a distinct "project" in Weinberg's model. Switching between 3 active agent sessions would impose ~40% overhead by his estimates. The Iqbal/Horvitz finding that 27% of switches lead to 2+ hours of displacement is particularly concerning -- a developer who switches to handle one agent's request may not return to the others for extended periods.

---

## 5.2 Supervisory Control and Monitoring

### Endsley's Situation Awareness Model

Mica Endsley's three-level SA model (1995) defines situation awareness as:

- **Level 1 -- Perception**: Detecting elements in the environment
- **Level 2 -- Comprehension**: Understanding what the perceived elements mean
- **Level 3 -- Projection**: Predicting future states

In automation monitoring, each level can degrade. An operator supervising multiple AI agents may perceive a status change (L1) but fail to comprehend its significance (L2) or project its consequences (L3) because attention is divided.

Source: [Toward a Theory of Situation Awareness in Dynamic Systems, Human Factors 37(1), 32-64 (1995)](https://journals.sagepub.com/doi/10.1518/001872095779049543)

### Out-of-the-Loop Performance Problem

Endsley & Kiris (1995) identified three factors causing the OOTL problem:

1. **Vigilance and complacency** -- reduced monitoring when automation is trusted
2. **Passive role** -- operators process information passively rather than actively, degrading SA
3. **Degraded feedback** -- automation changes the quality and form of feedback to the human

Greater SA decrement occurs under full automation than under intermediate levels. When operators are kept in the decision-making loop (intermediate automation), they maintain higher SA and can take over manual control more effectively.

OOTL consequences include: failure to detect parameter changes, over-trust in automation (complacency), loss of situation awareness, and direct control skill decay. In aviation, Mosier et al. (1994) examined NASA's ASRS database and found that **77% of incidents** where over-reliance on automation was suspected involved a probable vigilance failure.

Sources: [The Out-of-the-Loop Performance Problem and Level of Control in Automation, Human Factors 37(2) (1995)](https://journals.sagepub.com/doi/10.1518/001872095779064555), [Out-of-the-loop performance problem (Wikipedia)](https://en.wikipedia.org/wiki/Out-of-the-loop_performance_problem)

### Vigilance Decrement

The ability to monitor for rare critical events degrades over time, typically completing within the first **30 minutes** of a monitoring session. Laboratory studies have observed decrements in monitoring automated systems in as little as **20 minutes**. Research on pilots found that when free to monitor, they "often mind wandered which also led to lapses" -- diligence, distraction, and daydreaming all lead to monitoring failures.

Sources: [FAA Human Factors Design Standard, Chapter 3: Automation](https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch3_Automation.pdf), [Vigilance Impossible: Diligence, Distraction, and Daydreaming (Consciousness and Cognition, 2015)](https://www.sciencedirect.com/science/article/abs/pii/S1053810015000963)

### Implications for AI Agent Monitoring

A developer supervising multiple concurrent AI agents is in a classic supervisory control role. The research predicts: vigilance will degrade within 20-30 minutes of passive monitoring; the developer will become complacent about agent outputs; when an agent does something wrong, the developer will be slower to detect and correct it; and the more automated the agents are, the worse these effects become.

---

## 5.3 Hot Rotation vs. Cold Resume

While no single study uses these exact terms, the literature clearly distinguishes between rapid alternation and delayed resumption, and provides evidence about their relative costs.

### Rapid Alternation ("Hot Rotation")

Rubinstein et al. (2001) showed that rapid task alternation imposes per-switch costs from goal shifting and rule activation that compound with frequency. Gould (2013) found that even when instructed to avoid switching, **60% of participants switched anyway**, averaging **12 switches in 32 minutes**, each consuming ~16 seconds -- totaling ~10% of working time on switching overhead alone.

### Delayed Resumption ("Cold Resume")

Monk, Trafton & Boehm-Davis (2008) demonstrated that **longer interruptions lead to longer resumption times**, supporting the memory-for-goals decay model: the activation of a suspended goal decays over time, making it harder to retrieve. Their experiments examined durations up to 1 minute and found that both duration and cognitive demand of the interruption affected resumption cost. Related work (Hodgetts & Jones, 2006) observed a plateau effect where beyond a certain interruption duration, additional time stopped increasing resumption cost, suggesting goal activation hits a decay floor.

Altmann & Trafton (2004) found that people actively **rehearse goals during interruption lags** as a coping mechanism, and that this rehearsal facilitates resumption. This suggests that cold resume from a completely unrelated long gap is worse because no rehearsal occurs.

### The Critical Comparison

The evidence suggests both are costly but in different ways:

- **Hot rotation** imposes constant overhead from repeated goal-shifting/rule-activation cycles, accumulates stress (Mark's NASA-TLX findings), and degrades quality across all tasks simultaneously
- **Cold resume** imposes a large one-time resumption cost (23+ minutes by Mark's data, with only 10% of programming sessions resuming in under 1 minute per Parnin) but allows deep focus during the active work period

The Iqbal/Horvitz finding that 27% of switches lead to 2+ hour absences suggests cold resume carries the risk of task abandonment, not just slow resumption.

Sources: [Monk, Trafton & Boehm-Davis, Journal of Experimental Psychology: Applied (2008)](https://pubmed.ncbi.nlm.nih.gov/19102614/), [Altmann & Trafton, Task Interruption: Resumption Lag and the Role of Cues (CogSci 2004)](https://www.interruptions.net/literature/Altmann-CogSci04.pdf)

---

## 5.4 Terminal Multiplexer / Multi-Window Patterns

Formal UX research on terminal multiplexer usage is sparse, but practitioner literature reveals consistent patterns.

### How Developers Structure Multi-Session Work

The tmux/screen model organizes work hierarchically: **sessions** (one per project), **windows** (tabs within a session), and **panes** (split views within a window). This mirrors the cognitive structure -- a session is a task context, windows are sub-tasks, panes are simultaneous views of the same sub-task.

### Context Maintenance Strategies

Developers use several strategies to maintain context across multiple terminal sessions:

- **Named sessions** with descriptive labels for instant identification
- **Persistent layouts** that restore the spatial arrangement of tools (editor, server, tests, logs)
- **Instant workspace setup** -- scripted session creation that rebuilds the full context in seconds

### Failure Modes

The primary failure mode is **session proliferation without cleanup** -- developers open sessions and forget about them, leading to confusion about which session is current. The second failure mode is **context loss on reconnect** -- even with persistent sessions, the developer must re-orient to the state of each session's work, which maps directly to the cold resume problem.

### Connection to Multi-Agent Sessions

Each AI agent session is analogous to a tmux session. The spatial/visual organization patterns that work for terminal multiplexing (named sessions, persistent state, hierarchical grouping) would apply to agent session management.

Sources: [Mastering Tmux (DEV Community)](https://dev.to/govindup63/mastering-tmux-the-terminal-multiplexer-every-developer-should-know-3ko2), [tmux for Local Development (Delicious Brains)](https://deliciousbrains.com/tmux-for-local-development/)

---

## 5.5 Dashboard Design for Multi-Process Monitoring

### Core Principles

**The 5-Second Rule**: Users should grasp all essential data at a glance within 5 seconds. For multi-agent monitoring, this means the top-level view must convey the state of all agents without requiring drill-down.

**Visual Hierarchy and Scanning**: Critical metrics belong in the **upper-left quadrant** (matching natural scan patterns). Limit visible elements to approximately **5 items** to prevent overload.

**Progressive Disclosure**: Display only essential information upfront; reveal details as users engage. This directly addresses the tension between monitoring breadth (many agents) and comprehension depth (understanding one agent's state).

Source: [UX Strategies for Real-Time Dashboards (Smashing Magazine)](https://www.smashingmagazine.com/2025/09/ux-strategies-real-time-dashboards/)

### Four Cognitive Design Guidelines (UX Magazine)

1. **Emphasize readability** -- proper contrast, hierarchical information prioritization
2. **Minimize cognitive load** -- display all necessary information simultaneously rather than forcing recall; recognition over recall
3. **Use graphical representation** -- icons with brief labels leverage visual processing over text parsing
4. **Follow Gestalt laws** -- Law of Pragnanz (simple ordered patterns process faster), Law of Focal Point (contrasting elements direct attention)

Source: [Four Cognitive Design Guidelines for Effective Information Dashboards (UX Magazine)](https://uxmag.com/articles/four-cognitive-design-guidelines-for-effective-information-dashboards)

### Change Detection

To combat **change blindness** in real-time dashboards: use subtle micro-animations (200-400ms transitions) to signal updates without distracting; use skeleton loading screens to indicate active data refresh; include **mini-history views** so users can scroll back through recent changes rather than relying on memory.

### CI/CD Dashboard Analogies

Datadog and Splunk recommend a **hierarchical dashboard structure**: a quick-reference summary dashboard providing high-level overview of all pipelines, with links to granular dashboards for deeper investigation. Each section should include text explaining what metrics measure and what visual indicators to watch for. Flame graphs visualize pipeline execution hierarchically, helping contextualize individual job duration within the overall flow.

Sources: [Best Practices for CI/CD Monitoring (Datadog)](https://www.datadoghq.com/blog/best-practices-for-ci-cd-monitoring/), [CI/CD Pipeline Monitoring (Splunk)](https://www.splunk.com/en_us/blog/learn/monitoring-ci-cd.html)

---

## 5.6 Orchestrator UX Patterns

### Human-in-the-Loop vs. Human-on-the-Loop

The emerging distinction in multi-agent AI systems:

- **Human-in-the-Loop (HITL)**: Human approval required at every critical decision point. High safety, but creates bottlenecks -- the human becomes a blocking checkpoint. Does not scale to multiple concurrent agents.
- **Human-on-the-Loop (HOTL)**: AI agents operate autonomously; humans monitor via dashboards/alerts and intervene only for exceptions. Scales better but relies on trust in agent autonomy and effective alerting.
- **Parallel Feedback** (emerging pattern): AI does not pause execution but collects human feedback asynchronously, incorporating it in the background. This is "especially relevant in agentic architectures, where latency, autonomy, and scale are in tension with the need for safety and oversight."

Source: [Human-in-the-Loop Patterns for AI Agents (MyEngineeringPath, 2026)](https://myengineeringpath.dev/genai-engineer/human-in-the-loop/)

### Hierarchical Orchestration

The dominant pattern for multi-agent systems uses a **hierarchical architecture**: higher-level agents supervise teams of lower-level worker agents, with higher levels focusing on coordination/planning and lower levels on execution. This mirrors the CI/CD dashboard hierarchy -- summary view at top, drill-down for details.

### Risk-Based Oversight Design

Not all agents demand the same oversight level. The emerging best practice is **risk-stratified interaction**:
- **High-stakes actions**: Slow down, require checkpoints and confirmations (HITL)
- **Low-stakes actions**: Minimize friction, let agents proceed autonomously (HOTL)

This maps directly to Endsley's finding that intermediate automation levels preserve SA better than full automation -- the key is keeping the human engaged on high-stakes decisions while offloading routine ones.

Sources: [Multi-Agent Systems & AI Orchestration Guide 2026 (Codebridge)](https://www.codebridge.tech/articles/mastering-multi-agent-orchestration-coordination-is-the-new-scale-frontier), [Human-in-the-Loop for AI Agents (Permit.io)](https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo)

---

## 5.7 The Notification Problem

### The Core Tension

When multiple concurrent agents need attention simultaneously, the system must balance **interruption** (drawing attention) against **disruption** (breaking focus on the current task). Research by McCrickard & Chewar (2003) modeled notification systems along three parameters:

1. **Interruption** -- how much the notification breaks current focus
2. **Reaction** -- how quickly the user must respond
3. **Comprehension** -- how much the user must understand from the notification

Different blends of these parameters suit different situations.

Source: [A Model for Notification Systems Evaluation, ACM Transactions on Computer-Human Interaction (2003)](https://dl.acm.org/doi/10.1145/966930.966933)

### Attention Management Systems

Research on Attention Management Systems (AMS) for dynamic monitoring tasks focuses on helping users "coordinate attention" across multiple information sources, quickly identify critical situations, and respond appropriately. The key challenge is that presenting all notifications equally leads to alert fatigue, while filtering too aggressively risks missing critical events.

Source: [Evaluating Attention Management Systems for Dynamic Monitoring Tasks (CHIWORK 2025)](https://dl.acm.org/doi/10.1145/3707640.3731920)

### Alert Deduplication and Triage

From incident response research: implementing **deduplication rules** eliminates redundant alerts; **filters** distill essential details from the information influx; **severity-based routing** ensures responders focus on unique, high-priority incidents. The parallel to multi-agent orchestration is clear -- when three agents need attention simultaneously, the system should deduplicate similar requests, triage by severity/urgency, and present the highest-priority item first.

### The Scale of the Problem

Jackson (2001) found workers responded to email within **6 seconds** of arrival, averaging **96 interruptions per 8-hour day**, losing **1.5 hours daily** to interruption handling alone. This establishes that even a single notification channel can dominate attention; multiple concurrent agent sessions would compound this dramatically.

---

## 5.8 Key Implications Summary

| Research Finding | Design Implication |
|---|---|
| Weinberg: 40% overhead at 3 concurrent tasks | Limit concurrent active agent sessions; 2-3 maximum for active supervision |
| Mark: ~23-minute recovery per switch | Minimize unnecessary switches; batch agent attention demands |
| Endsley: Intermediate automation preserves SA best | Keep human in decision loop for high-stakes actions, not all actions |
| Vigilance decrement in 20-30 minutes | Design for active engagement, not passive monitoring |
| OOTL problem worsens with full automation | Agents should surface meaningful decision points, not just status |
| Monk/Trafton/Boehm-Davis: Goal activation decays over time | Provide rich context restoration on session resume |
| Parnin: Only 10% resume in under 1 minute | Session state must be instantly comprehensible on return |
| Dashboard research: 5-second rule, 5-item limit | Top-level view should show all agent states at a glance in under 5 seconds |
| HITL vs HOTL tradeoff | Use risk-stratified oversight -- HITL for high-stakes, HOTL for routine |
| Notification triage: interruption/reaction/comprehension | Classify agent demands by urgency and present accordingly |
