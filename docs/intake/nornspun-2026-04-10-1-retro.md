# Momentum Upstream Intake — nornspun sprint-2026-04-08 Retrospective
**Source project:** nornspun  
**Retro date:** 2026-04-10  
**Sprint:** sprint-2026-04-08 (completed 2026-04-09)  
**Intake iteration:** 1  
**Prepared by:** retro skill (automated transcript audit + documenter synthesis)  

---

## How to Use This Document

This document captures 13 upstream improvement opportunities identified during a retrospective transcript audit of a Momentum-driven sprint. Each finding includes:
- Quantitative evidence (error counts, turn counts, session data)
- Verbatim user quotes where the issue surfaced
- Root cause analysis
- Recommended fix scope (skill, prompt pattern, workflow rule)

The Momentum team can use this to triage, prioritize, and create issues or PRs without needing to access the nornspun session logs directly.

**Sprint data summary:**
- 96 user messages across 4 sessions
- 54 subagents spawned (36 general-purpose, 16 Explore, 1 Plan, 1 claude-code-guide)
- 125 tool errors (file_too_large: 70, exit_code_nonzero: 27, other: 12, unknown: 10, file_not_found: 4, zsh_insecure_dirs: 2)
- 2,043 total assistant turns · 1,438 total tool results · 9,807 KB total transcript
- 9 user interventions that required course-correction

---

## Issue Index

| # | ID | Priority | Skill/Component Affected |
|---|-----|----------|--------------------------|
| 1 | `add-file-size-hints-to-spawn-prompts` | **Critical** | All spawn workflows |
| 2 | `orchestrator-coverage-deduplication` | **Critical** | epic-grooming, sprint-planning |
| 3 | `read-only-investigation-agents` | **High** | All investigation spawns |
| 4 | `encode-epic-semantic-model` | **High** | epic-grooming, refine |
| 5 | `proactive-scope-recommendations` | **High** | AVFL, coverage agents |
| 6 | `assessment-decision-pipeline` | **High** | assessment, retro, sprint-planning |
| 7 | `quick-fix-spec-placement-rules` | **Medium** | quick-fix |
| 8 | `explore-agent-directory-hints` | **Medium** | All Explore spawns |
| 9 | `dev-agent-executor-not-decider` | **Medium** | sprint-dev, quick-fix |
| 10 | `verify-shell-before-fix` | **Medium** | quick-fix, investigation agents |
| 11 | `avfl-default-agent-composition` | **Low** | avfl |
| 12 | `two-phase-coverage-validation` | **Low** | avfl, coverage analysis |
| 13 | `retro-upstream-classifier` | **Medium** | retro |

---

## Issues

---

### Issue 1 — `add-file-size-hints-to-spawn-prompts`
**Priority:** Critical  
**Skill/Component:** All spawn workflows — any skill that spawns agents to read planning artifacts  

#### What happened
70 of 125 errors (56% of the entire error budget) were `file_too_large` — agents hitting the Read tool's 10,000-token limit on large planning files. Every agent independently discovers this limit and wastes 1–3 turns retrying with `offset`/`limit` parameters.

#### Evidence
Files most frequently causing errors and approximate token sizes observed:
- `stories/index.json` — ~54,000 tokens (hit 6+ times across agents)
- `prd.md` — ~25,000 tokens
- `architecture.md` — ~25,000 tokens
- Various planning docs — ~17,000 tokens
- Epic files — ~12,000 tokens

The 7-agent priority evaluation fan-out (one agent per epic) collectively produced 13 file-too-large errors — agents #40 and #52 took 2–3× longer than other agents primarily due to file-size retries. The product state assessment (4 Explore agents) contributed 8 more. Fix agents and coverage agents added the remainder.

Across 54 agents, conservatively 50–100 turns were wasted on "I need to retry with offset/limit" cycles that could have been avoided entirely.

#### Root cause
Spawn prompts give agents a file path but no information about file size. Every agent must discover the 10k-token limit by failing once, then manually figure out appropriate chunking. Planning artifacts grow with every sprint; this will worsen over time.

#### Recommended fix
Spawn prompts for agents that read known-large planning artifacts should include pre-computed metadata, e.g.:
```
Note: stories/index.json is ~54k tokens. Read in chunks:
  offset=0 limit=200 for stories A-M
  offset=200 limit=200 for stories N-Z
```
The retro and sprint-planning skills already know which files agents will read — they can compute or cache token estimates at spawn time. Long-term: consider sharded index views that fit within 10k tokens.

---

### Issue 2 — `orchestrator-coverage-deduplication`
**Priority:** Critical  
**Skill/Component:** epic-grooming, sprint-planning (any workflow with multiple stages that includes coverage analysis)  

#### What happened
The lead orchestrator spawned coverage analysis twice for both `architecture.md` and `prd.md` — once during epic-grooming and again during sprint-planning. Four duplicate agents total:
- 2 × architecture coverage: 56 turns + 22 turns = **78 wasted turns**
- 2 × PRD coverage: 29 turns + 19 turns = **48 wasted turns**
- Total: **~126 wasted turns**

These were confirmed as true duplicates via follow-up investigation by the auditor team — both pairs had near-identical prompts, neither referenced the other's findings, and there was no intentional multi-pass design.

#### Evidence
`auditor-review` finding RV-05 (initially flagged as possible by-design multi-pass) was clarified in follow-up: *"true duplicates, not by design."* The lead spawned the same analysis at different workflow stages without any mechanism to track that the analysis had already been performed.

#### Root cause
No orchestrator state tracking per document per sprint. Coverage results from epic-grooming are not persisted or checked when sprint-planning runs. Multi-stage workflows (assessment → epic-grooming → sprint-planning) all can independently decide to run coverage analysis.

#### Recommended fix
Implement a lightweight "already analyzed" registry per sprint. Before spawning a coverage agent for a document, check:
```
Has coverage been run for {document} since its last-modified timestamp?
```
If yes: load prior results instead of re-spawning. This could be a simple JSON file in the sprint's artifact directory. Alternatively, coverage results could be cached as named artifacts (e.g., `sprint-2026-04-08/coverage-architecture.md`) and spawn workflows check for existence before spawning.

---

### Issue 3 — `read-only-investigation-agents`
**Priority:** High  
**Skill/Component:** All workflows that spawn investigation or debugging agents  

#### What happened
Two agents were spawned to investigate the same underlying issue (cmux spawning bash instead of zsh). Combined cost: **236 turns, 695 KB of transcript.**
- Agent #7: 153 turns, 11 errors, 445 KB — went down dead ends including git index.lock contention, merge conflict attempts, and unsupported cmux API flags
- Agent #8: 83 turns, 0 errors, 250 KB — successfully identified root cause (stale `SHELL` environment variable in macOS launchd GUI domain)

Agent #7 was the costlier one, partly because it had write access and attempted git operations (worktrees, merges) on the shared repo while the lead was also making changes. This caused 2 merge conflicts on `stories/index.json` and a git `index.lock` file that persisted for 14 minutes.

#### Evidence
User interventions H-05, H-09, H-10, H-11:
- H-05: *"I think you need to do some discovery, fire up a couple of subagents. This can't possibly be correct"* — agent was guessing instead of running diagnostics
- H-09: Agent suggested `autoload -Uz compinit && compinit` (a zsh command) without checking which shell was actually running
- H-10/H-11: User ran `dscl` diagnostics themselves to prove their system shell was `/bin/zsh` while the running shell was `bash` — the agent should have verified with `echo $0` first

#### Root cause
1. Investigation agents are spawned with full tool access including file write and git operations
2. The orchestrator spawned a second investigation agent rather than sending follow-up questions to the first
3. Agent was overconfident in diagnosis without running basic verification commands

#### Recommended fix
Investigation agents should be spawned with read-only constraints by default:
- No file write/edit tools
- No git operations
- Bash limited to diagnostic commands (read-only: `cat`, `ls`, `echo`, `which`, `ps`, `env`, `dscl`, etc.)

If a fix requires write access, that should be a separate, explicitly-scoped agent. The workflow rule: *investigate first (read-only), fix second (scoped write).*

Additionally: orchestrators should send follow-up messages to a running investigation agent rather than spawning a fresh one.

---

### Issue 4 — `encode-epic-semantic-model`
**Priority:** High  
**Skill/Component:** epic-grooming, refine skills  

#### What happened
During the epic taxonomy migration, the lead agent treated the migration as a renaming exercise (change "D1" to "client-foundation"). The user had to explicitly intervene to explain that the change was semantic, not just structural.

#### Evidence
User intervention H-01, verbatim:
> *"It's more than just a structural change it's also semantic. We are moving from the concept of epics being ordered and prioritized to them being long lived containers of stories of varying priority. The purpose of the new epic is to categorize stories in a way that makes it easy to find them and to understand what aspect of the product the story is related to. It's NO LONGER sequential nor are epics themselves prioritized."*

The agent's first dev pass (#18, 22 turns) was abandoned mid-analysis because it was scoped as a decision-maker rather than an executor of the already-decided taxonomy. The corrected second dev agent (#26, 140 turns) succeeded because it received the approved taxonomy decision in its prompt.

#### Root cause
The epic-grooming skill does not encode the conceptual model for what an epic IS in the current Momentum practice. Agents optimize for mechanical format compliance without understanding the semantic intent.

#### Recommended fix
The epic-grooming and refine skills should include an explicit statement of the epic model:
```
Epics are long-lived categorical containers for stories. They are NOT sequential 
delivery phases. Epics are not prioritized relative to each other — they exist to 
make stories discoverable and categorically organized. Epic slugs should be 
descriptive of a product domain (e.g., "client-foundation"), not a delivery 
sequence (e.g., "D1").
```
Skills should also reference a canonical implementation (the momentum repo's own epic structure) before proposing structural changes to epic taxonomy.

---

### Issue 5 — `proactive-scope-recommendations`
**Priority:** High  
**Skill/Component:** AVFL validators, spec-impact agents, coverage analysis agents  

#### What happened
When a spec-impact discovery agent found that `architecture.md` used identifiers being migrated but was NOT in the migration scope, it reported the finding — but did not recommend adding `architecture.md` to scope. The user had to explicitly insist.

#### Evidence
User intervention H-02:
> *"architecture DEFINITELY needs to be added along with PRD if it's not already part of this"*

Similar pattern appeared in H-03 (Gherkin placement rules — agent executed without flagging constraint violation) and EX-08 (first dev agent was scoped as decision-maker instead of executor, wasting 22 turns before being abandoned).

The pattern: agents surface correct findings but stop short of the obvious implication, requiring user intervention to bridge the gap.

#### Root cause
Agent prompts for validators and spec-impact agents are scoped to "find and report" without an instruction to "recommend the obvious action." Agents default to information presentation mode.

#### Recommended fix
Validator and spec-impact agent prompts should include an explicit instruction:
```
If you find a gap that has an obvious remediation, state the recommended action 
explicitly. Do not merely report — recommend.
```
For example: "architecture.md uses migrated identifiers but is not in scope → recommend: add architecture.md to migration scope."

---

### Issue 6 — `assessment-decision-pipeline`
**Priority:** High  
**Skill/Component:** assessment skill, retro skill, sprint-planning skill — the transition between assessment/research and backlog refinement  

#### What happened
The user identified a systemic practice gap: the workflow moves from research reports and assessments directly to backlog refinement without a formalized step to capture the decisions that bridge them.

#### Evidence
User intervention H-13 (strategic decision), verbatim:
> *"I'd actually like you to create an exhaustive report of decisions... I think we have a bit of a gap where we generate these reports and then we try to go directly to backlog."*

Follow-up user messages H-16 and H-17 (approval): *"I love that"* — the agent's proposal of a structured decisions directory with indexed documents was warmly received and immediately adopted as a new practice artifact.

The decisions directory was subsequently created during the sprint as a practice improvement, but it's not yet encoded as a formal workflow step in any Momentum skill.

#### Root cause
The Momentum skill chain (assessment → sprint-planning → sprint-dev) has no explicit decisions capture step. When an assessment produces insights, those insights either get lost or must be manually converted to stories, skipping the decision record that explains WHY a story exists.

#### Recommended fix
Formalize a `decisions` artifact type with a corresponding workflow step:
1. **After assessment or research:** the lead proposes decisions derived from findings
2. **Developer approves/rejects each decision** with rationale
3. **Approved decisions** feed directly into backlog refinement as story justifications

The decision document format used in this sprint:
```markdown
# Decision: <title>
**Date:** <ISO date>
**Status:** approved | rejected | deferred
**Context:** <1-2 sentences — what we learned>
**Decision:** <the specific choice made>
**Rationale:** <why this over alternatives>
**Consequences:** <stories this generates>
```
The retro skill could also benefit from this: retro findings that cross into practice improvements should produce structured upstream intake documents (this document is itself evidence of the gap).

---

### Issue 7 — `quick-fix-spec-placement-rules`
**Priority:** Medium  
**Skill/Component:** quick-fix skill  

#### What happened
During a quick-fix execution, the user had to remind the agent that Gherkin specs must be in separate files and must follow sprint-planning structural rules — they cannot be embedded in the story file.

#### Evidence
User intervention H-03, verbatim:
> *"Just remember that the gherkin specs for the e2e reviewer must NOT be in the story file and must follow all the rules of the sprint-planning doc."*

This constraint has been documented in the sprint-planning conventions but is not encoded in the quick-fix skill's execution rules.

#### Root cause
The quick-fix skill operates somewhat independently from sprint-planning conventions. Structural placement rules for Gherkin specs are not surfaced in the quick-fix execution context.

#### Recommended fix
The quick-fix skill's execution prompt should include an explicit rule:
```
Gherkin acceptance spec files must be created as SEPARATE files (not embedded 
in the story file). Follow the same spec placement conventions as sprint-planning. 
See: <link to sprint-planning spec placement docs>
```

---

### Issue 8 — `explore-agent-directory-hints`
**Priority:** Medium  
**Skill/Component:** All workflows that spawn Explore agents for project-wide analysis  

#### What happened
The product state assessment spawned 4 parallel Explore agents (201 total turns, 1,234 KB combined). Each independently spent initial turns discovering the project structure (running `find`, `ls -la`, reading `CLAUDE.md`) before narrowing to their assigned domain. This is redundant discovery work performed 4× in parallel.

#### Evidence
EX-10: All 4 assessment agents began with exploratory project discovery. A single "project map" agent producing a directory index could have eliminated this overlap. The sprint used ~25-30% of those 201 turns on initial structure discovery that was identical across all 4 agents.

#### Root cause
Explore agent prompts point agents at a domain without providing a directory context. Agents must independently discover the project structure before they can navigate purposefully.

#### Recommended fix
Workflows that spawn multiple Explore agents should include a pre-computed directory snapshot in each spawn prompt:
```
Project structure (top 2 levels):
nornspun/
  nornspun-backend/      # FastAPI backend
  _bmad-output/          # Planning artifacts
    implementation-artifacts/
      stories/           # stories/index.json (~54k tokens)
      sprints/           # sprint artifacts
      epics/             # epic definitions
  docs/                  # architecture.md, prd.md
  ...
```
This could be computed once by the orchestrator and injected into all parallel Explore spawns.

---

### Issue 9 — `dev-agent-executor-not-decider`
**Priority:** Medium  
**Skill/Component:** sprint-dev, quick-fix — any workflow that spawns dev agents  

#### What happened
The first dev agent for the epic taxonomy migration (#18, 22 turns) was given a decision-making task: "propose the new taxonomy." It spent 22 turns analyzing, deliberating, and proposing before being abandoned by the orchestrator. The second dev agent (#26, 140 turns) received the pre-approved taxonomy in its prompt and executed successfully.

#### Evidence
EX-08: Agent #18 was "scoped as decision-maker instead of executor — 22 turns before abandonment." The corrected agent received the approved taxonomy as input. Fix agents elsewhere in the sprint showed the same pattern in positive: all 5 fix agents received explicit finding IDs, exact file paths, and exact text to change — and converged in single passes with 0-2 errors.

User intervention H-01 (epic taxonomy semantic correction) contributed to the confusion: the agent was asked to propose a taxonomy for something whose semantic model it didn't understand.

#### Root cause
Sprint-dev skill allows dev agents to be spawned with open-ended "figure out and implement" tasks. The correct pattern — make the decision at the orchestrator level, pass the decision to the dev agent — is not enforced by the skill.

#### Recommended fix
The sprint-dev and quick-fix skill execution rules should include:
```
Dev agents receive DECISIONS, not DECISION-MAKING TASKS. 
Before spawning a dev agent, the orchestrator must have already decided:
  - What to build (not "figure out what to build")
  - Which files to change (not "find the right files")
  - What the acceptance criteria are (concrete, not vague)
```
The spawn prompt checklist for dev agents should include: "Does this prompt contain an approved decision, or is it asking the agent to make a decision?"

---

### Issue 10 — `verify-shell-before-fix`
**Priority:** Medium  
**Skill/Component:** quick-fix, any investigation/debugging agents that suggest shell commands  

#### What happened
During a cmux shell debugging session, the agent suggested `autoload -Uz compinit && compinit` — a zsh-specific command — without first verifying which shell was actually running. The running shell was bash (not the user's configured zsh), so the command failed with `autoload: command not found`.

#### Evidence
User interventions H-10 and H-11:
- H-10: *"And yet: [pasting `autoload: command not found` error from bash]"*
- H-11: User ran their own `dscl` diagnostics to prove the system was configured for zsh while the running environment was bash — the agent had been confidently diagnosing the wrong shell the entire time

The user had to perform their own shell diagnostic (`dscl . -read /Users/steve UserShell`) to prove the mismatch, rather than the agent doing this proactively.

#### Root cause
The agent assumed the shell environment matched the user's system default shell. It did not run basic verification (`echo $0`, `echo $SHELL`, `which zsh`) before suggesting shell-specific commands.

#### Recommended fix
Any agent suggesting shell-specific commands (zsh, bash, fish, etc.) should run verification first:
```bash
echo $0        # what shell am I actually running?
echo $SHELL    # what's the configured default?
```
If the answers differ, investigate why before suggesting shell-specific commands. This should be a rule in quick-fix and investigation agent prompts:
```
Before suggesting shell-specific commands, verify the active shell: echo $0
If the active shell doesn't match expected, investigate the mismatch first.
```

---

### Issue 11 — `avfl-default-agent-composition`
**Priority:** Low  
**Skill/Component:** avfl skill  

#### What happened
When the lead proposed running AVFL validation on backlog refinement findings, the user had to specify the agent composition manually: *"I agree but use two agents, adversary and enumerator."* The AVFL skill had not defaulted to the adversary+enumerator composition that has proven most effective.

#### Evidence
User intervention H-07:
> *"I agree but use two agents, adversary and enumerator"*

In this sprint, the adversary/enumerator two-pass successfully filtered a false positive (PRD-1 was initially flagged as overstating Verdandi/Skuld lock state; the adversary correctly identified it as describing UI lock, not agent existence). The value of the pattern was demonstrated — but its use required user specification.

#### Root cause
The AVFL skill does not encode recommended agent compositions for different validation types. Users must know to specify "adversary and enumerator" from prior experience.

#### Recommended fix
AVFL skill should define default compositions per validation profile:
- `profile: scan` → single validator
- `profile: checkpoint` → adversary + enumerator (two-pass)
- `profile: deep` → adversary + enumerator + coverage agent (three-pass)

The `checkpoint` profile (used in this sprint) should default to adversary+enumerator without requiring user specification.

---

### Issue 12 — `two-phase-coverage-validation`
**Priority:** Low  
**Skill/Component:** avfl, coverage analysis  

#### What happened
Coverage analysis and adversary validation were run as separate agents in most cases. For the epic taxonomy migration, the pipeline included: spec-update agent → Gherkin generator → AVFL scan → AVFL checkpoint → fix agent. The multi-agent pipeline is correct for complex stories but adds spawn overhead for simpler cases.

#### Evidence
RV-04, RV-05: Coverage analysis found genuine drift (Terraform→OpenTofu title, PRD timeline). The adversary/enumerator pattern filtered one false positive. For the cases where coverage analysis produced only 1-2 findings (rather than the 6+ found on major documents), a single two-phase agent could replace two separate spawns.

#### Root cause
AVFL is always executed as a multi-agent pipeline regardless of expected finding volume. There's no "lightweight" path for low-complexity validation.

#### Recommended fix
For cases where coverage analysis is expected to be low-complexity (small documents, recent changes, well-maintained artifacts), provide a single two-phase agent option:
1. Phase 1: enumerate coverage findings with skeptical framing
2. Phase 2: adversarially attack its own findings

This reduces spawn overhead while preserving the false-positive filter for cases that need it.

---

### Issue 13 — `retro-upstream-classifier`
**Priority:** Medium  
**Skill/Component:** retro skill  

#### What happened
The current retro skill assigns all findings to `impetus-core` by default and has no mechanism to:
1. Classify a finding as "upstream Momentum improvement" vs. "project-specific backlog item"
2. Generate structured upstream intake documents for the Momentum team
3. Distinguish findings that require a PR to the Momentum repo vs. a story in the project backlog

This document itself had to be created manually after the retro workflow completed — the retro skill had no step for it.

#### Evidence
This intake: 13 of 13 findings from sprint-2026-04-08 were Momentum improvements, not nornspun-specific stories. The retro skill would have created 13 `impetus-core` backlog items that then sit in nornspun's backlog indefinitely, creating noise and confusion about ownership.

#### Root cause
The retro skill was designed for single-project use. Multi-project Momentum deployments need a way to surface improvements back to the framework.

#### Recommended fix
The retro skill should:
1. **Classify each finding** at the time of story stub proposal:
   - `project` — specific to this project's codebase or domain
   - `upstream` — applies to the Momentum practice itself (skills, workflows, agent prompts)
2. **For upstream findings**: generate a structured intake document with full evidence detail (this document format is a good template)
3. **Prompt for target path**: where should the upstream document be written? (e.g., `~/projects/momentum/docs/intake/`)
4. **In story stubs**: upstream items should be flagged with a note ("tracked upstream in momentum — do not duplicate in project backlog") rather than creating `impetus-core` stories that will never be actioned locally

**Proposed intake document format:**
```
~/projects/momentum/docs/intake/{project}-{date}-{iteration}-{type}.md
```
Where `type` is `retro`, `sprint`, `incident`, etc.

---

## Summary for Momentum Triage

| Priority | Count | Issues |
|----------|-------|--------|
| Critical | 2 | file-size hints, coverage deduplication |
| High | 4 | read-only investigation, epic semantic model, proactive recommendations, assessment-decision pipeline |
| Medium | 5 | quick-fix spec placement, explore directory hints, dev executor pattern, verify shell, retro upstream classifier |
| Low | 2 | AVFL agent composition defaults, two-phase coverage validation |

**Highest-leverage fixes (biggest turn savings):**
1. File-size hints → ~50-100 turns recovered per sprint (56% of all errors)
2. Coverage deduplication → ~126 turns recovered in this sprint alone
3. Read-only investigation → 236 turns were spent on one bug (could have been ~50)

**Easiest wins (small prompt additions):**
- Verify shell before fix (1-line rule in agent prompt)
- Dev agent executor rule (1-paragraph prompt addition)
- Quick-fix spec placement rule (1-line rule in quick-fix skill)
- Explore directory hints (pre-computed directory snapshot in spawn prompts)
