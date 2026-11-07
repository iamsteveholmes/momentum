# Momentum Audit, Phase 3: External Evidence on How Claude Code Is Best Used

Date: 2026-11-07. Scope: Anthropic official guidance plus durable industry evidence, weighted by evidence type. Every claim below has passed a skeptic's source check; overstated claims are downgraded, mislabeled evidence is relabeled, unsupported claims are in the Dropped Claims appendix.

Dating note: the Anthropic Claude Code docs pages (code.claude.com) carry no publication date. "Retrieved 2026-11-07" means fetch date, not publication date. Version numbers inside the pages are the only dating signal.

---

## 1. Executive summary

1. The best-evidenced lever is verification, not orchestration: give the agent an executable check (tests, run-the-app, screenshots, a Stop hook) and a fresh-context reviewer. This holds across Anthropic guidance and independent practitioners, and across model generations.
2. Anthropic's own position is "simplest thing that works": a harness component encodes an assumption about what the model cannot do, those assumptions go stale, and Anthropic itself deleted context resets and sprint decomposition within about six months (Mar 2026). It kept a planner and a final evaluator.
3. Current Anthropic docs say what must always happen belongs in hooks or deny rules, not prose; keep CLAUDE.md short (target under 200 lines); drop emphasis, narration and architecture descriptions; and a subagent does not give a better answer by itself.
4. Real gains are documented for bounded tasks, less-experienced developers, unfamiliar code and well-run delivery systems (field experiments, DORA 2025). They are weakest for senior developers in deep familiar codebases.
5. Individual gains are often absorbed downstream: review load rises, and observational studies show transient velocity spikes with persistent complexity and warning increases. These are correlational or quasi-experimental, so treat them as strong cautions, not proof.
6. Self-reported speed is unreliable (METR 2025: 19% slower while believing 20% faster; the 2026 follow-up is, by METR's own account, very weak evidence). Outcomes must be measured.
7. No outcome study shows ceremony-heavy spec-driven frameworks beating lightweight approaches. The best evidence is hands-on evaluation and observational studies, and it reports heavy review cost and selective use.
8. Multi-agent systems pay for breadth-first, read-only, parallel work and independent review; they are a poor default for sequential, context-sharing coding work. Parallel writer swarms have no sustained evidence.
9. Large always-loaded instruction layers carry cost without proven benefit (ETH Zurich study; Anthropic docs); progressive disclosure and hooks are the sanctioned mechanisms.
10. Dark-factory, swarm and "10x" claims have no sustained independent evidence; the human review gate remains the bottleneck and the safety net.

---

## 2. Evidence ladder legend

| Rank | Type | Weight | Notes |
|---|---|---|---|
| 1 | Controlled study (RCT, preregistered field experiment) | Highest, but check recency and tool era | METR RCT, Cui et al., Anthropic skills RCT |
| 2 | Large survey / large telemetry | High for patterns, low for causation | DORA, Stack Overflow; Faros is vendor telemetry, correlational |
| 3 | Observational / quasi-experimental study | Moderate | CMU DiD (Cursor), CMU/Google SDD corpus study |
| 4 | Official (Anthropic) | High for "how the tool works" and design intent; NOT measured outcome | Docs are undated; engineering posts are dated |
| 5 | Sustained practitioner | Moderate: expert, mostly solo, self-reported | Hashimoto, Steinberger, Ronacher, Willison, Osmani, Böckeler (hands-on trials) |
| 6 | Team case study | Low to moderate | Vercel d0 (n=5 queries), DeputyDev |
| 7 | Vendor | Low: product incentive | Cognition, Faros, GitClear, Greptile, Anthropic Code Review launch numbers |
| 8 | Anecdote / hype | Reported only in the hype ledger | Ralph $297 claim, Gas Town, StrongDM |

Rules applied: (a) vendor docs are guidance, not measured effect; (b) self-report is discounted (METR perception gap); (c) pre-2025-11 findings flagged as potentially superseded by the Opus 4.5 / GPT-5.x inflection; (d) a source counts as sustained only if it spans months of real use.

Evidence gap stated plainly: no multi-month, team-scale field study of a heavy Claude Code practice layer (sprints, personas, multi-lens validation) was found. The Anthropic docs track is entirely vendor documentation.

---

## 3. Durable principles

### P1. Verification is the highest-leverage practice
- Says: give the agent a way to check its work and require evidence (command output, screenshot), not "tests pass" assertions. Run the real app end to end.
- Evidence: Anthropic best-practices (official, undated, retrieved 2026-11-07); Anthropic "Effective harnesses" (2025-11-26, official: unit tests and curl missed features that failed end to end; browser automation found them); Hashimoto "My AI Adoption Journey" (2026-02-05, practitioner: "If you give an agent a way to verify its work, it more often than not fixes its own mistakes"); Steinberger (late 2025, approx, undated page; practitioner: builds CLIs so agents can close the loop). Anthropic C compiler post (2026-02-05): "the task verifier is nearly perfect" was essential.
- Strength: strong for the principle. "Highest-leverage" is the synthesis's framing, not a stated Anthropic ranking. Convergence across Willison/Ronacher/Beck was not verified in substance.
- Durability: high; independent of model generation.

### P2. Hard invariants belong in hooks, deny rules or managed settings, not prose
- Says: CLAUDE.md and skills are guidance Claude may decline; "if something has to happen every time, make it a hook, a deny rule, or a managed setting." Also keep the enforced set small: at about forty hooks, most are probably preferences.
- Evidence: Anthropic best-practices and features-overview (official, undated). Permission-modes page: boundaries stated in chat can be lost on compaction.
- Strength: strong as design intent; the "forty" figure is a rule of thumb, not a measured threshold.
- Durability: structural property of the harness; high.

### P3. Keep always-loaded instructions short, non-inferable and conflict-free
- Says: target under 200 lines per CLAUDE.md; every line costs attention each task; conflicting instructions may be resolved arbitrarily; do not describe what the repo already shows.
- Evidence: Anthropic memory and best-practices pages (official, undated). Gloaguen et al., "Evaluating AGENTS.md", arXiv 2602.11988 (2026-02, later versions to 2026-09; controlled study): context files did not generally improve task success, cost over 20% more on average, repository overviews not helpful. Specific agents/models, the 138-issue count and Python-only scope were not confirmed from the abstract; the claim that short human-written files help modestly was not supported and is dropped.
- Strength: moderate to strong (one academic study plus consistent vendor guidance; "reduces adherence" is Anthropic's assertion, not a measured result).
- Durability: study ran on 2025-era agents; re-test on 5.x.

### P4. Scaffolding is perishable; every component encodes a model-weakness assumption
- Says: test removal of each harness component against the current model, one at a time; delete what no longer earns its cost; keep what still helps at the capability edge.
- Evidence: Anthropic "Harness design for long-running application development" (2026-03-24, official): context resets removed (Opus 4.5), sprint decomposition removed (Opus 4.6), per-sprint evaluation moved to one end pass; "I kept both the planner and evaluator, as each continued to add obvious value"; a radical cut lost performance; cost solo $9/20 min vs full harness $200/6 h (Opus 4.5) and $124.70/3h50 on Opus 4.6 (different app, so not like-for-like; one run per condition). Anthropic "Managed agents" (2026-04-08): "The resets had become dead weight." Anthropic Fable 5 and Opus 5 prompting guides (2026, official): skills written for earlier models "are often too prescriptive... and can degrade output quality"; explicit verification instructions cause over-verification on Opus 5. Counterweight in the same guides: Opus 5 coordinates subagent teams well with writer-verifier patterns, and fresh-context verifier subagents beat self-critique.
- Strength: strong as Anthropic's stated method; evidence is engineering-blog single runs plus vendor guidance, not a controlled study.
- Durability: demonstrated across Sonnet 4.5, Opus 4.5, Opus 4.6; expect repeats.
- Practitioner corroboration: Steinberger calls plan mode "a hack that was necessary for older generations of models" (one verified expert). Yegge's Gas Town: by his own account worked through Opus 4.6 and "fell apart at the seams with Opus 4.7" (single self-reported account, quoted secondhand via Willison, 2026-08-04).

### P5. Build the harness from observed failures, not up front
- Says: add a CLAUDE.md line after the agent errs twice, a skill after the third paste, a hook when something must always happen, a plugin when a second repo needs it. "Each line in that file is based on a bad agent behavior."
- Evidence: Anthropic features-overview (official, undated); Hashimoto (2026-02-05); Böckeler "Harness engineering" (martinfowler.com, 2026-04-02, practitioner, guides plus sensors steering loop). Anthropic context-engineering post (2025-09-29): smallest set of high-signal tokens; add instructions only to fix observed failures.
- Strength: strong convergence of official and practitioner guidance; none is measured outcome.
- Durability: high.

### P6. Scale planning and specs to task size and uncertainty
- Says: skip planning when the diff is describable in one sentence; plan mode or a short SPEC.md for medium work; fresh session to build from a written definition of done for large work.
- Evidence: Anthropic best-practices and costs pages (official); Osmani (2026-01-04) favors spec and small chunks; Steinberger skips plan mode; Harper Reed's spec/prompt_plan/todo workflow (2025-02-16) is Claude 3.x-era and likely superseded in detail.
- Strength: moderate; practitioners disagree, which supports tiering rather than a single mandated process.
- Durability: tiering is durable; thresholds are judgment.

### P7. Code is cheap; review and validation are the bottleneck
- Says: design the practice for human review throughput: small diffs, risk-tiered review, deterministic sensors for routine checks, fewer higher-signal review items.
- Evidence: Ronacher "The Final Bottleneck" (2026-02-13, practitioner essay, one illustrative figure); Willison (Lenny's Podcast summary, 2026-04-02: "the bottleneck has moved to testing"; ~95% figure is a guest's self-report about his own code). Faros (vendor telemetry, correlational, data to June 2025): high-AI teams +98% PRs, +91% review time, +154% PR size, +9% bugs per developer, no significant company-level improvement; the bottleneck explanation is a hypothesis, not a tested result. DORA 2025: AI is "an amplifier, magnifying an organization's existing strengths and weaknesses" (only this quote was verified from the primary page).
- Strength: moderate (consistent personal observation plus correlational telemetry; no measurement of causation).
- Durability: strengthens through 2026.

### P8. Perceived productivity is unreliable; measure outcomes
- Evidence: METR RCT (2025-07-10, controlled study): 16 experienced developers, 246 issues, 19% longer with AI (CI roughly +2% to +39%), forecast 24% speedup, afterwards believed 20%. METR marks it out of date (early-2025 tools). METR follow-up (2026-02-24): point estimates of -18% time (CI -38% to +9%) and -4% (CI -15% to +9%) but METR calls it very weak evidence because of selection effects, withheld tasks and parallel-agent timing problems. Honest state: both the 2025 slowdown and any 2026 speedup are unsettled; no rigorous RCT has quantified late-2025 tools (this last sentence is the checker's inference, not METR's wording).
- Strength: strong for the perception-gap lesson; weak for any current effect size.
- Durability: methodological lesson durable.

### P9. Gains are real but conditional; quality debt accrues if unguarded
- Evidence: observational DiD study of Cursor adoption in open-source repos (arXiv 2511.04427, MSR 2026; quasi-experimental, not a controlled trial): "large, but transient" velocity increase and "substantial and persistent" rise in static-analysis warnings and complexity, which drive later slowdown. The specific figures (3-5x first month, ~30% warnings, ~41% complexity, and the +18%/+39% in a separate agents paper) were not confirmed and are not relied on. Open-source Cursor projects on 2025-era tools may not transfer to Claude 5.x or solo private repos.
- Implication: make cheap deterministic gates (lint, static analysis, complexity budget, tests) hard merge conditions.
- Strength: moderate. GitClear duplication trend data is vendor correlational and treated as directional only.

### P10. Independent review helps; scoped review helps more; self-review is weaker
- Evidence: Anthropic best-practices (official): fresh reviewer "hasn't seen your reasoning"; "a reviewer that's asked to find problems will always find something," so scope it. Anthropic harness post (2026-03-24): separate skeptical evaluator with live-app tools is more tractable than self-critique and earns its cost at the capability edge. Anthropic Code Review launch (2026-03-09, vendor dogfooding): substantive comments 16% to 54% of PRs, under 1% marked incorrect; "substantive" undefined, the marker of "incorrect" is not stated in the post, no false-negative data. Cognition (2026-04-22, vendor): ~2 bugs/PR, ~58% severe, no sample size or method.
- LLM-judge literature (Zheng 2023, Panickssery 2024): self-preference bias exists, but results are from older models on chat/summarization tasks; the >80% agreement and 73.5% self-recognition numbers were not verified.
- Strength: moderate. Independent AI-review defect-catch evidence is thin: studies measure engagement, not escaped defects (Beko, DeputyDev, CodeRabbit-in-the-wild: all weak or summary-level).
- Durability: reviewer independence stable; numbers vendor-specific.

### P11. Executable acceptance beats prose acceptance; hold tests out of the implementer's reach
- Evidence: SpecBench (arXiv 2605.21384, 2026-05; abstract only): frontier agents saturate visible tests while held-out gap grows about 28 points per 10x code size. TDDev (arXiv 2605.17242, 2026-05): Agentic-TDD 65.8% vs 31.3% single-pass baseline on WebGen-Bench (+34.5 points) and +4.3 to +7.6 points on ArtifactsBench; the baseline has no feedback loop, so the gain mostly measures "any run-and-repair loop"; testing agent had 5 false negatives. Anthropic effective-harnesses: tests are not to be edited (a prompt instruction, not enforced). Beck (2026-01-20 newsletter; 2025-06 podcast description only): agents delete tests to pass them; model-era specific.
- Strength: moderate.

### P12. Human understanding must be protected
- Evidence: Anthropic skills-formation RCT (2026-01-29; n=52 mostly junior engineers, sidebar assistant, not agentic): AI group 50% vs 67% on quiz (p=0.01), no significant speed gain, largest gap on debugging. Subgroup patterns have n=2 to 7 and are not causal.
- Strength: moderate; scope-limited (short horizon, juniors, non-agentic).
- Durability: authors expect agentic tools may matter more.

---

## 4. What Anthropic officially recommends for Claude Code today, and native capabilities

All items are official vendor documentation, undated, retrieved 2026-11-07 unless noted. Layout is a capability map for comparing against a home-grown practice layer.

| Capability | Native feature | Official guidance and limits | Momentum counterpart to compare |
|---|---|---|---|
| Always-on guidance | CLAUDE.md, rules, auto memory | Under 200 lines per file; auto memory loads first 200 lines / 25KB; `/doctor prompt-audit` flags outdated-model instructions, dead references, contradictions; path-scoped rules via `paths:` | ~12 global rules, 4 project rules, persona, MEMORY.md index |
| Procedures | Skills | Name plus description in context (truncated at 1,536 chars with when_to_use); body loads on invocation and stays; keep SKILL.md under 500 lines; `disable-model-invocation` for side-effecting workflows; `context: fork`; skills can carry hooks, model, effort; after compaction only first 5,000 tokens per skill re-attached (25,000 combined) | ~60 skills listed, including deprecated stubs and benchmark variants |
| Deterministic enforcement | Hooks, deny/ask rules, managed settings | Stop hook exit 2 blocks completion; deny rules and PreToolUse hooks run before the auto-mode classifier. (The "8 consecutive blocks" override rule was not found in the cited page and is dropped.) | Prose rules for push approval, destructive git, plan-audit gate |
| Permissions | Plan mode, auto mode | Auto mode (default in interactive terminal/VS Code from v2.1.283) uses a separate classifier; "does not guarantee safety"; pauses after 3 consecutive / 20 total blocks; no false-negative rate published; hard guarantees need deny rules | Custom plan-audit gate, push-approval prose |
| Subagents | Subagents | For noisy side work, tool restriction, independent review; "Handing the same task to a subagent doesn't make the answer any better"; main conversation preferred when phases share significant context (planning, implementation, testing); depth 3, 20 concurrent, 15,000-token description warning; model per subagent (haiku, sonnet, opus, fable) | Per-story create-story, dev, QA, E2E, AVFL pipeline |
| Orchestration | Dynamic Workflows | Script Claude writes (agent/pipeline/parallel/phase); intermediate state in script variables; savable as commands in `.claude/workflows/` or via plugins; 16 concurrent / 1,000 total agents; Large-workflow warning above 25 agents or 1.5M projected tokens; "no mid-run user input," so run each stage as its own workflow for sign-off; token-expensive. "Plans a workflow for each substantive task" applies only when the user opts into ultracode. No quality or productivity measurement is published. | Conductor, sprint-dev, retro engine |
| Peer teams | Agent teams | Experimental, disabled by default; ~7x tokens when teammates run in plan mode; for research, review, competing-hypothesis debugging; 3-5 teammates; sequential or same-file work better in one session | TeamCreate retro/review teams |
| Review | `/code-review`, `/verify` | Fresh-subagent review; scope the prompt ("skip style") | momentum:code-reviewer, AVFL |
| Packaging and testing | Plugins, `claude plugin eval` (manifest key `experimental.evals`) | Standalone skills/hooks work without plugins; every enabled plugin adds always-on description tokens; evals compare against a no-plugin baseline with rubric graders and CI gating. A test tool, not evidence of value; results depend on cases Momentum has not yet written. | Momentum plugin v0.34.0 |
| Cost visibility | `/usage` attribution, plugin Context-cost estimates | Spend attributed to skills, subagents, plugins, MCP; Sonnet for most coding, Opus for architecture/multi-step reasoning, Haiku for simple subagents; thinking cannot be disabled on 5.5 models, effort is the control; ~$13/developer/active day typical (cost datapoint only) | None |
| Memory | Auto memory, file notes | One lesson per file, delete wrong ones, do not store what the repo records (Fable 5 guide) | Ledger, handoffs, resume cards, 30+ memory notes |
| Stop-doing table | Best-practices "What you can stop doing" | Emphasis over-applies rules; "keep going" prompts cause over-work; architecture in CLAUDE.md redundant; aggressive context management less necessary; delegating alone does not help. The reasons are Anthropic's assertion that models have caught up; no benchmark is cited. | MANDATORY / no-exceptions language, narration rules |

Anthropic's own caveat on its framing: "your first plain prompt in a fresh session already does the right thing" in most cases (vendor-authored stance, not measured).

---

## 5. Process frameworks and spec-driven development

What the evidence supports (and its type):
- Hands-on independent evaluation (Böckeler, martinfowler.com, 2025-10-15; tools tested Sept 2025: Kiro, spec-kit, Tessl; practitioner trials by one evaluator, not a study): "I'd rather review code than all these markdown files"; Kiro produced 4 user stories and 16 acceptance criteria for a small bug ("sledgehammer to crack a nut"); agents still ignored instructions or duplicated classes. Spec-anchored and spec-as-source are aspirational levels these tools had not demonstrated. Tools may have improved since.
- Observational mixed-methods study (CMU/Google, arXiv 2608.25202, Aug to Oct 2026; 470,795 spec files in 73,030 repos, 21 interviews incl. 8 tool makers, Reddit analysis; not a controlled study): SDD used "selectively and mainly for new features"; greater planning and review costs; spec-code consistency checked mainly at completion. Claims that practitioners skip bugs and small tasks, that cost was "shifted not removed," and the individual-vs-team split were not confirmed from the abstract and are treated as unverified. 99.7% of spec files date from 2025 or later (secondary summary), so there is no long-term record.
- Thoughtworks Technology Radar (2025-11-05): SDD placed in Assess; "workflows are still elaborate and opinionated, and some generate spec files that are hard to review." Not fetched in the check; treat as secondary until read. This is Thoughtworks, not Anthropic.
- No outcome evidence found either way: no controlled study of BMAD, Spec Kit, Kiro or sprint-style layers vs plain prompting or plan-then-implement on defects, cycle time or cost (absence in this search, based largely on one secondary review, Groundy 2026-10-16: "no source measures team-level velocity or defect outcomes"). "Up to 50% fewer errors" claims trace to vendors and reportedly did not hold up.
- BMAD user reports (single anecdote, Feb 2026: two days of planning, zero code on a simple app; sustained practitioner, Apr 2026: months of use, became a "human router," moved to orchestrator plus skills). Small sample, consistent direction. BMAD itself added Quick Flow tracks.
- Prose-spec drift: argued by opinion pieces (anecdote-level); the CMU/Google study notes practitioners built custom drift checks. Executable acceptance (tests, feature verify) stays in sync; narrative story files do not.
- Anthropic's own lightweight pattern for multi-session work (Nov 2025): JSON feature list (initially failing, `passes` field edited), progress file plus git, init script, one feature per session, browser end-to-end checks. JSON chosen because models overwrite it less than Markdown. The "agent alone may edit" is a prompt instruction, not an enforced restriction. Anthropic lists as unresolved whether specialist QA/cleanup agents beat one general agent.

Reported failure modes: review burden exceeding value; one-size-fits-all workflow on small problems; the human acting as router between stages; stale specs misleading later agent runs; agents ignoring written specs.

Reading for Momentum: the evidence supports keeping a small acceptance-feature registry and executable checks, selective specs for new, risky features, and no evidence that per-change story ceremony pays. It does not show ceremony is harmful in outcome; it shows it is unmeasured and costly to review.

---

## 6. Multi-agent orchestration and verification

When it pays:
- Breadth-first, read-only, parallelizable work exceeding one context: Anthropic multi-agent research system (2025-06-13, vendor internal eval on research tasks with Opus 4 lead, Sonnet 4 subagents): +90.2% vs single-agent, about 15x chat tokens (agents about 4x); token usage alone explains 80% of BrowseComp variance (three factors together 95%). Anthropic says coding has fewer truly parallelizable tasks than research and shared-context domains are a poor fit. (It does not say "most coding tasks are a poor fit"; it is a vendor eval, not a general finding.)
- Independent review in fresh context (P10) and noisy-output isolation.
- Strong oracle cases: Anthropic C compiler (Carlini, 2026-02-05): 16 Opus 4.6 agents, nearly 2,000 sessions, just under $20K, about 2B input / 140M output tokens; relied on a near-perfect verifier and GCC as known-good oracle, heavy human harness design; output less efficient than GCC -O0, fixes frequently broke features, still needed GCC for some pieces. It is a research demo, not sustained development.
- Single-writer plus extra intelligence: Cognition's 2026-04-22 post (vendor) says parallel writers remain largely unadopted and unstructured swarms are "mostly a distraction"; manager-child delegation worked with heavy context engineering. Its 2025 "Don't Build Multi-Agents" post was not fetched.

When it is reassuring noise:
- Same-model "find problems" reviewers that always find something; fixing every finding adds abstraction and tests for cases that cannot happen (Anthropic).
- Sequential, same-file or dependency-heavy work (Anthropic agent-teams page).
- Multi-lens prose validation of documents: no evidence of defect-catching; LLM-as-judge has documented self-preference (older models, other tasks); MAST (arXiv 2503.13657) reports verification-related failure clusters in multi-agent systems but was not checked here.
- Agent PASS reports as completion: SpecBench shows green visible tests can coexist with large held-out failures.
- Opus 5 guide: avoid subagents to double-check your own work on small tasks; verification scaffolding can be over-verification.

Operator experience (sustained practitioner, small sample): Hashimoto runs one agent at a time with a background agent 10-20% of the day; Steinberger queues 3-8 projects but sees little need for orchestration because he is the bottleneck; Willison relays that parallel agents are "mentally exhausting." No throughput data exists. METR found parallel-agent time hard to measure at all.

Cost: workflows use "meaningfully more tokens" than conversation; agent teams about 7x; Anthropic's full harness was about 20x the cost of a solo run on its one example (single run each).

Net: pay for orchestration where there is an executable oracle and breadth, keep one writer per unit of work, use one scoped fresh-context reviewer plus deterministic checks, and measure marginal defect yield per stage. Native Workflows and `/code-review` now provide the primitives; no evidence says a hand-built equivalent beats them.

---

## 7. Context and instruction load with 5-series models

- Instruction cost: CLAUDE.md loads every request, skill descriptions load every request, hooks cost zero unless they emit output (Anthropic features-overview). Imports do not reduce context cost (memory page).
- Conflict: Anthropic's memory page says contradictory instructions may be picked arbitrarily. Whether user and project rules both being "followed arbitrarily" was a quoted line is unverified; the inference that Momentum's authority-hierarchy rule is not harness-enforced is this audit's inference, not an Anthropic statement.
- Newer models read more literally and respond more to emphasis: Anthropic prompting guides (2026, vendor): steer with brief instructions, soften aggressive language (that specific quote sits on a page not fetched in the check, so treat as unverified), state scope explicitly because Sonnet 5 "does not silently generalize an instruction from one item to another."
- Context rot (Chroma, 2025-07-14, retrieval-vendor study, 18 models incl. Claude 4-era): focused ~300-token prompts beat ~113k-token full prompts; a single distractor lowers performance; Claude models tended to abstain rather than hallucinate. Follow-up EMNLP Findings paper (arXiv 2510.05381) says length alone hurts but was not opened in the check. Anthropic says Opus 5 instruction following stays consistent across its 1M window; independent measurement on 5.x is absent.
- Instruction count: IFScale (Distyl, NeurIPS 2025; 500 keyword-inclusion instructions, 20 models) shows decay and earlier-instruction bias, but is a narrow synthetic task on 2025 models; only "best models reach about 68% at 500 instructions" was confirmed. Do not use it to size a rule budget.
- Personas: the persona-prompt study (Zheng et al., 162 roles, 2,410 factual questions, older models) found no accuracy gain; Beck's small experiment (2026-01-20) found persona changed naming and tests but not architecture, explicit constraints did. Persona value for tone is a preference, not a quality effect. Anthropic output styles are the native, toggleable mechanism.
- Memory: Anthropic recommends one lesson per file, deletion of wrong notes, no duplication of repo facts. Manus (2025-07, vendor case study) stresses stable prompt prefixes and file-system memory.
- Removal case study (weak): Vercel d0 text-to-SQL agent cut most tools: success 4/5 to 5/5, 274.8 s to 77.4 s, ~102k to ~61k tokens on Opus 4.5. Five queries, depends on a documented semantic layer, ExecuteSQL retained. Use as an ablation template, not a conclusion.
- Counterweight: verifier subagents help long, high-stakes tasks and hurt small ones (Anthropic's own words), so lighter does not mean none.

Implications: separate rules into enforced invariants (hooks, zero context), short non-inferable guidance, and on-demand skills; put persona behind a toggle; compute session-start state in a script instead of prose precedence logic.

---

## 8. Hype ledger

| Claim | Where | Status and why |
|---|---|---|
| Dark factory / no human reads code, $1,000 per engineer per day | StrongDM via Willison (2026-02-07), vendor | No production metrics; Willison saw demos on an invited visit and is skeptical on cost (about $20K per engineer-month is his multiplication) and test gaming |
| Gas Town / swarm orchestration as the future | Yegge, 2026 | Creator's own numbers (17 days, 75k lines, 2,000 commits); he says he never saw the code; later said it fell apart with Opus 4.7 and was mostly used to build itself (single self-reported account) |
| Ralph loop: $50k contract for $297 | Huntley | Single anecdote; Huntley concedes it needs senior engineers and leaves placeholders and sometimes broken code; mechanics (fresh context, plan file, tests as backpressure) are reasonable |
| "+90%" from multi-agent | Anthropic research post | Internal research eval; token spend explains most variance; not a coding result and not a time saving |
| 16 agents built a C compiler "with zero human input" | Press coverage | Anthropic's post documents heavy human harness, ~$20K, worse-than-GCC output, regressions |
| ~50% productivity gain, +67% merged PRs, fully delegate only 0-20% | Anthropic internal survey (2025-12-02) | Self-report of 132 Anthropic staff plus 53 interviews, Aug 2025 fieldwork, Sonnet 4 / Opus 4; authors flag social-desirability and recency bias; PR count is an output proxy. Not a large survey. |
| "AI makes developers 19% slower" as current truth | Social citations | METR marked it out of date |
| "X% faster" headlines (26%, 21%, 3-5x) | Vendors, first-month spikes | Controlled gains modest with wide CIs on older tools; spikes transient where measured |
| Faros 2026 "5x review time, 3x incidents" as causal | Faros | Vendor, correlational, baselines undefined, unverified |
| Reviewer bots catch most bugs (<1% incorrect; 62% vs 48% recall) | Anthropic launch, Cognition, Greptile | Vendor dogfooding or vendor-run benchmarks; acceptance is not defect detection |
| Auto mode safe enough for unattended runs | Docs | Anthropic itself: does not guarantee safety; no false-negative rate |
| Agent teams find root causes more reliably | Agent-teams docs | Mechanistic argument only; experimental, ~7x tokens |
| Dynamic workflows (dozens or hundreds of agents) as the default way to work | Workflows docs | Capability and caps documented; no quality or productivity evidence; ultracode is opt-in |
| Superpowers / BMAD / Spec Kit popularity as effectiveness | Star counts | Stars are gameable; 99.7% of spec files are 2025 or later; no outcome evaluation |
| SDD 50% fewer errors | Vendor claims | Reportedly did not hold up |
| Bigger harness is the moat / harness dissolves into the model | Commentary | Contradictory anecdotes; Anthropic's data shows pruning and keeping some parts |
| Anthropic's 200-line / 500-line numeric thresholds as measured | Docs | Heuristics from a vendor, no adherence measurement |
| GitClear duplication as proof AI writes worse code | GitClear | Vendor correlation during an adoption period; primary report not read |

---

## 9. Where real gains are well documented

- Field experiments: Cui et al. (Management Science, 2025; three field experiments, 4,867 developers at Microsoft, Accenture and a Fortune 100 firm, GPT-3.5-era Copilot 2022-23) pooled about +26% completed tasks, larger for less-experienced developers; Google internal RCT (arXiv 2410.12944, 2024-10; 96 engineers) about 21% faster on one enterprise task with a wide CI. Neither source was opened in the check; the figures are as reported and tools are old.
- Large surveys: DORA 2025 (about 5,000 respondents, Sept 2025) reports roughly 90% adoption and AI associated with higher throughput alongside continued instability (the amplifier quote was verified; the throughput reversal and other numbers were not). Stack Overflow 2025 (n about 33K): 66% cite "almost right, but not quite," 46% distrust accuracy vs 33% trust, 45% say debugging AI code takes longer. Adoption is high and trust is low (self-report).
- Agent PR acceptance varies by task type (AIDev dataset, MSR 2026; search-summary level): documentation and well-specified features accepted more often than fixes in some tools. Treat as directional.
- Practitioners with months to years of use report the shift from "constant correction" to "mostly does what you say" around Nov 2025 (Willison, Steinberger), with ~95% of one practitioner's code now agent-typed (self-report). They sustain the gains by owning verification, building failure-driven harnesses and keeping process light.
- Anthropic internal usage (vendor-internal): heavy use with limited full delegation; supports supervised, well-scoped delegation.
- Verification loops work: browser-driven end-to-end checks found bugs that unit tests missed (Anthropic, Nov 2025); run-and-repair loops raised web-app success in TDDev; the Anthropic evaluator with Playwright caught real defects.
- Conditions under which gains show up: bounded tasks, junior or unfamiliar-code contexts, strong delivery foundations (fast tests, small batches, CI), executable verification, and bounded review load. Gains erode where review is the bottleneck and where quality gates are absent.

---

## 10. Evaluation lens for Momentum

Apply each question to every Momentum capability (rules, skills, personas, Impetus, conductor, AVFL, retro, ledger, sprint/story machinery, memory).

1. Failure justification: Which recorded, repeated agent failure created this component? If none is cited, treat it as a hypothesis, not a requirement (P5; Anthropic ladder; Hashimoto).
2. Model-weakness assumption: What did the model fail to do in Mar 2026 (Claude 3.x/4.x) that this compensates for, and has Claude 5.5 been re-tested without it? Ablate one component at a time (P4; Anthropic harness post).
3. Baseline delta: Does it beat the no-layer default on a fixed task set graded on outcome? Use `claude plugin eval` with a no-plugin baseline or an equivalent 20-50 task real-failure set; judge end state, not path (Anthropic evals post, 2026-01-09).
4. Enforcement fit: Is it a hard invariant stored as prose? If so, convert to a hook or deny rule; if it is a preference, delete it (P2).
5. Always-on cost: What are its tokens per session (rules, persona, skill descriptions, memory index)? Is every rule non-inferable from the repo, non-conflicting and under budget? Run `/doctor prompt-audit` and `/usage` attribution (P3).
6. Instruction style: Does it rely on emphasis ("MANDATORY", "no exceptions") or narration that current guidance says to drop, and does each retained rule state its scope and one reason?
7. Executable vs LLM-judged verification: Does the check run something (tests, app, screenshots, DB, logs) or only have a model opine? Are acceptance tests held out from, and uneditable by, the implementer (P1, P11)?
8. Reviewer scope and independence: Is there one fresh-context reviewer with a scoped prompt, or multi-lens "find problems" loops? What is the finding acceptance rate and the escaped-defect rate? (P10)
9. Subagent justification: Is each subagent for noisy isolation, true parallelism or independent review, rather than a phase split of one shared-context task? Is the model tier set (Haiku/Sonnet for extraction and audit)? (Section 6)
10. Review throughput: Does it reduce or grow the artifacts the single human must read? Measure review minutes per unit and cap diff size; reports, gates and ledgers count (P7; Faros pattern as a caution).
11. Ceremony proportionality: Is the lightest path the default, and is the full story/spec/Gherkin path reserved for large or risky new features? Are specs executable or protected by a drift check? (Section 5)
12. Outcome tie: Does it move verified feature status (features.json passing, hands-on verified) or only process status? Does Momentum's own record (10 sprints, 0 of 15 features verified, per the project's own audit context) reflect process produced vs outcome achieved? (P8)
13. Native overlap: Does Claude Code now do this natively (plan mode, auto mode, Workflows, `/code-review`, skills, output styles, hooks, memory)? If so, what does the home-grown version add that can be demonstrated?
14. Quality gates: Are lint, static analysis, complexity and duplication budgets enforced mechanically at merge, to counter the transient-velocity / persistent-complexity pattern? (P9)
15. Human skill preservation: Does the design keep the human able to detect wrong code (explanations, independent debugging of owned areas), given that the human is the final verifier? (P12)
16. Staleness plan: Is each component version-stamped with the model it was designed for, with a scheduled re-evaluation at each model release, and a deletion path?

Scoring suggestion: keep (beats baseline or is a hard invariant as a hook), simplify (keep intent, move to hook, skill or output style), retire (no cited failure or baseline delta).

---

## Appendix A. Source list (date, type)

Anthropic official, undated docs (retrieved 2026-11-07), type: official vendor guidance
- Best practices for Claude Code, code.claude.com/docs/en/best-practices
- How Claude remembers your project, /docs/en/memory
- Extend Claude Code (features overview), /docs/en/features-overview
- Extend Claude Code with skills, /docs/en/skills
- Create custom subagents, /docs/en/sub-agents
- Orchestrate subagents at scale with dynamic workflows, /docs/en/workflows
- Orchestrate teams of Claude Code sessions, /docs/en/agent-teams
- Permission modes, /docs/en/permission-modes
- Plugins overview, /docs/en/plugins/overview; Test plugins with evals, /docs/en/plugin-evals
- Manage costs effectively, /docs/en/costs
- Prompting Claude Fable 5; Prompting Claude Opus 5; Claude prompting best practices (platform.claude.com, 2026, undated; the last was not fetched in the check)

Anthropic dated posts, type: official engineering
- Building effective agents, 2024-12-19
- How we built our multi-agent research system, 2025-06-13 (vendor internal eval)
- Writing effective tools for agents, 2025-09-11 (not fetched)
- Effective context engineering for AI agents, 2025-09-29
- Equipping agents with Agent Skills, 2025-10-16, updated 2025-12-18 (not fetched)
- Effective harnesses for long-running agents, 2025-11-26
- Demystifying evals for AI agents, 2026-01-09
- Building a C compiler with a team of parallel Claudes, 2026-02-05 (research demo)
- Bringing Code Review to Claude Code, 2026-03-09 (vendor launch data)
- Harness design for long-running application development, 2026-03-24
- Scaling Managed Agents, 2026-04-08
- How AI is transforming work at Anthropic, 2025-12-02 (self-report survey, n=132)
- How AI assistance impacts the formation of coding skills, 2026-01-29 (RCT, n=52)

Controlled studies
- METR RCT, 2025-07-10 (arXiv 2507.09089); METR design update and follow-up, 2026-02-24
- Cui et al., three field experiments (Management Science, 2025), not opened in check
- Google enterprise RCT, arXiv 2410.12944 (2024-10), not opened in check
- Anthropic skills RCT (above)

Large surveys / telemetry
- DORA State of AI-assisted Software Development, 2025-09 (only amplifier quote verified); Google blog 2025-09-23
- Stack Overflow Developer Survey 2025 (2025-07)
- Faros AI Productivity Paradox, 2025 (vendor telemetry, correlational); Faros "Acceleration Whiplash," 2026 (vendor, unverified)

Observational / academic
- He et al., Cursor DiD, arXiv 2511.04427 (MSR 2026): quasi-experimental
- AI IDEs or Autonomous Agents, arXiv 2601.13597 (2026-01), summary-level only
- CMU/Google SDD as prescribed and practiced, arXiv 2608.25202 (2026-08-25 to 2026-10-15): observational corpus plus interviews
- Gloaguen et al., Evaluating AGENTS.md, arXiv 2602.11988 (2026-02, v3 2026-09)
- Chroma Context Rot, 2025-07-14; Du et al., arXiv 2510.05381 (EMNLP Findings 2025)
- IFScale, arXiv 2507.11538 (2025-07)
- SpecBench, arXiv 2605.21384 (2026-05, abstract only); TDDev, arXiv 2605.17242 (2026-05)
- Zheng et al., LLM-as-judge, arXiv 2306.05685 (2023); Panickssery et al., arXiv 2404.13076 (2024); persona study, arXiv 2311.10054 (2023); MAST, arXiv 2503.13657 (2025), unchecked
- Agentic code review (CodeRabbit repos), arXiv 2607.03316; DeputyDev, arXiv 2509.19708; AIDev agent PR acceptance, arXiv 2602.08915: all summary-level

Sustained practitioners
- Hashimoto, My AI Adoption Journey, 2026-02-05
- Steinberger, Shipping at Inference-Speed, late 2025 (page undated, approx)
- Ronacher, A Year of Vibes 2025-12-22; The Final Bottleneck 2026-02-13
- Willison, Agentic Engineering Patterns guide (2026-02-23), Lenny's Podcast highlights 2026-04-02, StrongDM software factory 2026-02-07, Yegge quote 2026-08-04, Superpowers 2025-10-10
- Böckeler, SDD tools 2025-10-15; Harness engineering 2026-04-02
- Osmani 2026-01-04; Ball 2026-07-29 (talk, partially verified); Beck 2026-01-20 and podcast 2025-06-11 (description only); Reed 2025-02-16 (superseded in detail)
- Huntley, Ralph (2025, undated); Vincent, Superpowers (2025-10-09); Appleton on Gas Town (2026-01, approx)
- BMAD reports: Lancrenon 2026-02-08 (anecdote); Dabène 2026-04-14

Team case studies and vendor
- Vercel d0 tool removal, 2025-12-22 (n=5 queries); Manus context engineering, 2025-07
- Cognition: Don't Build Multi-Agents 2025-06-12 (not fetched); Multi-Agents: What's Actually Working 2026-04-22 (vendor)
- GitClear 2025-02 (vendor, summary only); Greptile benchmarks 2025-07 (vendor)
- Thoughtworks Technology Radar SDD, 2025-11-05 (not fetched)
- Groundy summary of CMU/Google study, 2026-10-16 (secondary); mcp.directory Superpowers review, 2026-06 (vendor/aggregator)

## Appendix B. Dropped claims and corrections applied

Dropped (unsupported or unverifiable as cited):
- "Stop hook is overridden after 8 consecutive blocks with no tool call": not found in the cited page.
- "Dynamic workflows introduced in v2.1.154+": version claim not on the cited page.
- "Succeeded only because of a near-perfect oracle and GCC" (C compiler): causal claim not made by the post; restated as "relied on / stressed".
- "Only the planner survived" (harness post): false; planner and evaluator were both kept.
- "Evaluator became optional/overhead for tasks a newer model handles solo": not in the post; the post says the evaluator is worth its cost when the task is beyond what the model does reliably alone.
- "Willison does not trust software built quickly until used for months": not on the cited page.
- "Human-written AGENTS.md files helped modestly (+4%)": not supported by the abstract page, which reports no gain for either kind.
- "+34 to +48 pp" for TDD: upper bound unsupported; replaced with +34.5 and +4.3 to +7.6.
- IFScale per-model figures, the 150-200 primacy peak and "English only": unverified; removed.
- LLM-judge ">80% agreement" and "73.5% self-recognition": unverified in the check; carried only as unverified direction.
- Cursor DiD "3-5x in month one," "~30% warnings / ~41% complexity," agents paper "+18% / +39%": not confirmed; not relied on.
- "Skipping bugs and small tasks" and "cost shifted rather than removed" (CMU/Google SDD): not in the abstract.
- Faros 2026 "5x review time, 3x incidents, 10x churn": unverified; kept only in the hype ledger.
- DORA numbers other than the amplifier quote (sample size, daily hours, trust, throughput reversal, seven capabilities): unverified; the report cites them as reported with that flag.
- "Managed Agents cut p50 time-to-first-token ~60%": unverified and irrelevant to practice.
- "2-3x quality gain from Claude Code verification loop" and "80%+ of Anthropic code written by Claude": no primary source.
- "Most coding tasks are a poor fit" attributed to Anthropic: restated as Anthropic saying coding has fewer parallelizable tasks than research.

Relabeled or downgraded:
- All Anthropic docs: "2026-11" was a fetch date, now "undated, retrieved 2026-11-07".
- Anthropic internal survey: "large-survey" to self-report survey, n=132.
- Faros 2025: "large-survey" to vendor telemetry, correlational; bottleneck explanation a hypothesis.
- Cursor DiD, CMU/Google SDD: "controlled-study" to observational / quasi-experimental.
- Cognition: "sustained practitioner" to vendor.
- Groundy: "team case study" to secondary commentary; Thoughtworks Radar: not "anthropic-official".
- Yegge/Gas Town: from sustained practitioner data point to a single self-reported account.
- "Most long-runners are lean": rests on one verified expert (Steinberger) with partial support from Hashimoto (Hashimoto is not a source for plan-mode rejection); strength lowered to weak-moderate.
- "Code is cheap, review is the bottleneck": strength lowered from strong to moderate; quote corrected to "testing."
- Böckeler: "most careful independent evaluator" removed; "few spec-anchored, none proven spec-as-source" restated.
- Plugin evals: "the exact instrument for a pivot" downgraded to "a test tool whose value depends on Momentum's own cases."
- LLM-as-judge: strength lowered from strong to moderate.
- Dynamic workflows "plan for each substantive task": applies to ultracode opt-in only.
- Opus 5 guide nuance added: writer-verifier patterns and fresh-context verifiers are endorsed, so "lighter" is not "none".

Open gaps (not resolved by this phase): no sustained multi-month field study of heavy practice layers; METR 2026 reading was via its blog post only; DORA 2025 primary report, Cui et al., the Google RCT, Thoughtworks Radar page, Cognition 2025 post, MAST and EMNLP 2510.05381 were not opened.
