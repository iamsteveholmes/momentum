# Sprint Dev Workflow

**Goal:** Execute an active sprint — dependency-driven dev spawning, post-merge team review, Gherkin verification, and sprint completion.

**Invoked by:** Impetus Mode 1 → "Continue sprint"

**Architecture references:** Decision 25 (Teams Over Waves), Decision 26 (Two-Layer Agent Model), Decision 30 (Black-Box Verification), Decision 31 (AVFL at Sprint Level), FR62–FR70.

---

<workflow>
  <critical>Read the active sprint slug from sprints/index.json, then read the per-sprint record from sprints/{slug}.json. Never invent team plans — all roles, guidelines, and dependencies come from the sprint record written by sprint-planning.</critical>
  <critical>Worktree-to-sprint merges are autonomous — only pushes require developer confirmation.</critical>
  <critical>Dev agents never access sprints/{sprint-slug}/specs/ — verification is black-box.</critical>
  <critical>Stories are spawned strictly by dependency resolution. A story never starts before all its blockers are `done`.</critical>
  <critical>AVFL runs ONCE after ALL stories merge — not per-story. AVFL findings are presented as a read-only stop gate (Phase 4). No fixes are spawned in Phase 4. All fixes happen in Phase 4d after developer review of the consolidated fix queue (Phase 4c).</critical>
  <critical>Impetus always spawns agents. No agent spawns another agent.</critical>
  <critical>Log all sprint events via `momentum-tools log --agent impetus --sprint {slug}` at each phase transition.</critical>
  <critical>Use task tracking (TaskCreate/TaskUpdate) for sprint phases — this prevents context drift in long runs. Ad-hoc narrative summaries are NOT a substitute for tool-queryable task state.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- TEAM COMPOSITION DECLARATION                             -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <!--
    This section codifies spawning mode and concurrency for every phase that spawns agents.
    The mandatory field "spawning" must be one of: individual-agent | team-create.
    Default is individual-agent. TeamCreate is NEVER used in sprint-dev.

    Phase 2 — Dev Wave:
      role: dev (specialist variant per story assignment)
      spawning: individual-agent  (one Agent tool call per story — NEVER TeamCreate)
      concurrency: parallel       (all unblocked stories in a single message turn)
      agent-definition: skills/momentum/agents/{specialist}.md
        fallback: skills/momentum/agents/dev.md
      note: Each story gets its own isolated agent with its own worktree.
            The specialist resolution logic (steps 2.3a–2.3d) selects the agent definition.

    Phase 4b — Per-Story Code Review:
      role: code-reviewer
      spawning: individual-agent  (one Agent tool call per merged story — NEVER TeamCreate)
      concurrency: parallel       (all stories in a single message turn)

    Phase 4d — Fix Agents (developer-confirmed findings from consolidated fix queue):
      role: dev-fixer
      spawning: individual-agent  (one Agent tool call per confirmed finding — NEVER TeamCreate)
      concurrency: sequential     (one fix agent per finding, in severity order)
      note: No worktrees — fix agents run directly on the sprint branch.

    Phase 5 — Team Review:
      role: qa-reviewer
        spawning: individual-agent  (Agent tool, parallel with peers)
      role: e2e-validator
        spawning: individual-agent  (Agent tool, parallel with peers)
      role: architect-guard
        spawning: individual-agent  (Agent tool, parallel with peers)
      concurrency: parallel         (all three in a single message — three Agent tool calls)
      note: These three roles are ALWAYS spawned as individual agents in one message.
            Never group them into a TeamCreate call.
  -->

  <team-composition>
    <phase name="dev-wave" step="2">
      <role name="dev" spawning="individual-agent" concurrency="parallel">
        One agent per unblocked story. Specialist agent definition resolved per
        team.story_assignments[slug].specialist — fallback to skills/momentum/agents/dev.md.
        Never use TeamCreate. Each story runs in its own worktree.
      </role>
    </phase>
    <phase name="code-review" step="4b">
      <role name="code-reviewer" spawning="individual-agent" concurrency="parallel">
        One code-reviewer per merged story. Spawned in parallel in a single message turn.
        Never use TeamCreate.
      </role>
    </phase>
    <phase name="avfl-fix" step="4d">
      <role name="dev-fixer" spawning="individual-agent" concurrency="sequential">
        One fix agent per developer-confirmed finding, spawned in severity order.
        No worktrees — operates directly on sprint/{{sprint_slug}} branch.
        Never use TeamCreate.
      </role>
    </phase>
    <phase name="team-review" step="5">
      <role name="qa-reviewer" spawning="individual-agent" concurrency="parallel">
        Agent definition: skills/momentum/agents/qa-reviewer.md
      </role>
      <role name="e2e-validator" spawning="individual-agent" concurrency="parallel">
        Agent definition: skills/momentum/agents/e2e-validator.md
      </role>
      <role name="architect-guard" spawning="individual-agent" concurrency="parallel">
        Invoked as: momentum:architecture-guard (context: fork, read-only)
      </role>
      <note>All three review roles spawn in a single message (three parallel Agent tool calls).
        Never use TeamCreate for team review agents.</note>
    </phase>
  </team-composition>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 0: TASK TRACKING SETUP                              -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="0" goal="Initialize phase-level task tracking">
    <action>Create tasks for the 10 execution phases:
      1. Initialization — read sprint record, build dependency graph
      2. Dev Wave — spawn agents for unblocked stories
      3. Progress Tracking — monitor completion, propose merges, unblock next wave
      4. Post-Merge AVFL — sprint-level quality scan (stop gate: findings presented, no fixes)
      4b. Per-Story Code Review — independent code-reviewer per merged story
      4c. Consolidated Fix Queue — merge AVFL + code review findings, developer fix/defer decision
      4d. Targeted Fixes + Selective Re-review — spawn fix agents, re-run only affected reviewers
      5. Team Review — QA + E2E Validator + Architect Guard
      6. Verification — developer-confirmation checklist
      7. Sprint Completion — archive sprint, summary, suggest retro
    </action>
    <note>Story-level tasks are created separately in Phase 1 (step 1) after reading the sprint record.</note>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: INITIALIZATION                                 -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Initialize sprint execution">
    <action>Update task 1 (Initialization) to in_progress</action>
    <action>Read `_bmad-output/implementation-artifacts/sprints/index.json`</action>
    <action>Store {{sprint_slug}} = active.slug from sprints/index.json (active is an object containing slug, status, stories, waves, and team_composition)</action>

    <check if="active == null">
      <output>No active sprint found. Run sprint planning to create and activate a sprint first.</output>
      <action>HALT — return to Impetus session menu.</action>
    </check>

    <check if="active.status != 'active'">
      <output>Sprint {{sprint_slug}} is not in active status (currently: {{active.status}}). Cannot execute.</output>
      <action>HALT — return to Impetus session menu.</action>
    </check>

    <action>Ensure we are on the sprint branch: `git checkout sprint/{{sprint_slug}}`
      If the branch does not exist, HALT — sprint planning should have created it.</action>

    <action>Read the per-sprint record: `sprints/{{sprint_slug}}.json`</action>
    <action>Store {{sprint_locked}} = the value of `locked` field</action>

    <check if="{{sprint_locked}} == false">
      <output>Sprint {{sprint_slug}} has not been activated. Run `momentum-tools sprint activate` first.</output>
      <action>HALT — return to Impetus session menu.</action>
    </check>

    <action>Store {{sprint_stories}} = `stories` array from the sprint record</action>
    <action>Store {{team}} = `team` object from the sprint record (contains `roles` and `story_assignments`)</action>
    <action>Store {{sprint_dependencies}} = `dependencies` object from the sprint record</action>

    <action>Read `_bmad-output/implementation-artifacts/stories/index.json`</action>
    <action>For each story in {{sprint_stories}}, read its entry: status, depends_on, touches, title</action>
    <action>Store {{story_map}} = map of story slug → {status, depends_on, touches, title}</action>

    <!-- Session resumption: detect partially-completed sprint -->
    <action>Check for stories already `in-progress` from a previous session:
      For each story in {{sprint_stories}}, if status == "in-progress":
        - Check if worktree `.worktrees/story-{slug}` exists
        - If worktree exists: flag as "resumable — previous dev session may still be running or crashed"
        - If no worktree: flag as "stale in-progress — needs recovery (transition back to ready-for-dev or investigate)"
    </action>
    <check if="in-progress stories found">
      <output>Found stories from a previous session:
{{list of in-progress stories with worktree/stale status}}

Resume these stories, or reset them to ready-for-dev?</output>
      <ask>Resume or reset?</ask>
      <check if="reset">
        <action>For each stale in-progress story: `momentum-tools sprint status-transition --story {slug} --target ready-for-dev --force`</action>
      </check>
    </check>

    <action>Build dependency graph from {{sprint_dependencies}} (primary) reconciled with story-level `depends_on` fields (secondary)</action>

    <action>Create a task per story via TaskCreate:
      - Title: story title
      - Description: "depends_on: [list]"
      Status: pending
    </action>
    <action>Store {{task_map}} = map of story slug → task ID</action>
    <action>Store {{spawn_registry}} = {} (empty map — tracks every spawned agent by key "{story_slug}::{specialist}" for dev agents, "sprint::{role}" for team review agents; never reset between phases)</action>
    <note>spawn_registry is an in-memory deduplication guard. It survives the Phase 2 → Phase 3 → Phase 2 loop. Keys use format "{story_slug}::{specialist}" for dev agents and "sprint::{reviewer_role}" for team review agents. A key's presence means an agent was already spawned — do not spawn again.</note>

    <action>Log sprint start (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Sprint execution started: {{sprint_stories | length}} stories"`</action>

    <output>Sprint **{{sprint_slug}}** initialized.
{{sprint_stories | length}} stories, dependency graph resolved.
Task list created for progress tracking.</output>
    <action>Update task 1 (Initialization) to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: DEV WAVE — TEAM SPAWN                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Spawn dev agents for unblocked stories">
    <action>Update task 2 (Dev Wave) to in_progress</action>
    <!-- Spawning mode: individual-agent | concurrency: parallel — see <team-composition> declaration above -->
    <action>Identify unblocked stories: status == "ready-for-dev" AND every story in depends_on has status == "done"</action>

    <check if="no unblocked stories and no in-progress stories">
      <check if="all stories are done">
        <action>Jump to Phase 4 (AVFL).</action>
      </check>
      <output>All remaining stories are blocked by unresolved dependencies. Sprint stalled.</output>
      <action>HALT — surface blocker analysis and return to Impetus menu.</action>
    </check>

    <action>For each unblocked story:
      0. Compute dedup key: `{slug}::{specialist}` where specialist = {{team}}.story_assignments[slug].specialist
         Check {{spawn_registry}}[key]:
         - If key EXISTS: skip this story entirely — log suppression (best-effort):
           `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Dedup: skipped duplicate spawn for {key}"`
           Continue to next story.
         - If key ABSENT: proceed with steps 1-6 below.
      1. Transition to in-progress: `momentum-tools sprint status-transition --story {slug} --target in-progress`
      2. Look up role assignment from {{team}}.story_assignments[slug]
      3. Resolve specialist agent:
         a. Read {{team}}.story_assignments[slug].specialist (e.g., "dev-skills", "dev-build", "dev-frontend", or "dev")
         b. Resolve agent definition file: `skills/momentum/agents/{specialist}.md`
         c. If the specialist file exists, use it as the agent definition
         d. If the specialist file does NOT exist, log a warning and fall back to `skills/momentum/agents/dev.md`
      4. Spawn the resolved agent via the Agent tool (individual-agent mode — one Agent tool call per story,
         all in a single message turn for parallel execution). NEVER use TeamCreate for dev agents.
         Provide:
         - Story key: {slug}
         - Story file: `_bmad-output/implementation-artifacts/stories/{slug}.md`
         - Sprint context: {{sprint_slug}}
         - Role: {{team}}.story_assignments[slug].role
         - Specialist: {{team}}.story_assignments[slug].specialist
         - Guidelines: look up guidelines path from {{team}}.roles matching the assigned role (pass null if none)
         - Agent definition: the resolved specialist agent file (or base dev.md fallback)
         - If the story's `touches` array includes paths under `skills/` or `agents/`, also pass:
           reference: `skills/momentum/references/agent-skill-development-guide.md`
      5. Register in spawn registry: `{{spawn_registry}}[key] = { spawned: true }`
      6. Update task {{task_map}}[slug] to in_progress
    </action>

    <action>Log spawns (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Spawned dev agents for: {{list of spawned slugs}}"`</action>

    <output>Spawned dev agents for {{unblocked_count}} unblocked stories:
{{list of spawned story slugs}}</output>
    <action>Update task 2 (Dev Wave) to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: PROGRESS TRACKING LOOP                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Track progress and handle story completions">
    <note>This phase loops until all sprint stories have merged. Monitor via task status.</note>
    <action>Update task 3 (Progress Tracking) to in_progress</action>

    <action>Watch task statuses for agent completion or failure signals.</action>

    <!-- Agent failure handling -->
    <check if="agent reports failure or error">
      <action>Log failure (best-effort):
        `momentum-tools log --agent impetus --sprint {{sprint_slug}} --story {slug} --event error --detail "Dev agent failed for story {slug}: {{error_summary}}"`</action>
      <output>Dev agent for story **{slug}** failed:
{{error_summary}}

Options:
  R — Retry: spawn a fresh dev agent for this story
  S — Skip: leave story in-progress, continue with other stories
  H — Halt: stop sprint execution to investigate</output>
      <ask>Retry, Skip, or Halt?</ask>
      <check if="Retry">
        <action>Compute dedup key for failed story: `{slug}::{specialist}` where specialist = {{team}}.story_assignments[slug].specialist
          Remove existing registry entry: delete `{{spawn_registry}}[key]` (this allows the retry to be registered as a fresh spawn)
          Spawn a new dev agent (using `skills/momentum/agents/dev.md`) for the failed story (same parameters as Phase 2).
          Register the retry: `{{spawn_registry}}[key] = { spawned: true }`
          Do not auto-retry — this is the single manual retry.</action>
      </check>
      <check if="Skip">
        <action>Log skip decision. Continue monitoring other agents.</action>
      </check>
      <check if="Halt">
        <action>HALT — developer investigates.</action>
      </check>
    </check>

    <!-- Story completion handling -->
    <check if="story agent signals merge-ready">
      <action>Read the story's completion output to get {{file_list}}</action>

      <action>Log completion (best-effort):
        `momentum-tools log --agent impetus --sprint {{sprint_slug}} --story {slug} --event decision --detail "Story {slug} merge-ready, files: {{file_list}}"`</action>

      <output>Story **{slug}** is merge-ready. Merging autonomously to sprint/{{sprint_slug}}...</output>

      <action>Run: `git rebase sprint/{{sprint_slug}} story/{slug}` (rebases story branch onto latest sprint branch — leaves HEAD on story/{slug})</action>
      <check if="rebase conflicts">
        <output>Rebase conflicts on story/{slug}. Resolve and run `git rebase --continue`.</output>
        <action>HALT — wait for developer to resolve</action>
      </check>
      <action>Run: `git checkout sprint/{{sprint_slug}}`</action>
      <action>Run: `git merge story/{slug}`</action>
      <action>Run: `git worktree remove --force .worktrees/story-{slug}`</action>
      <action>Run: `git branch -d story/{slug}`</action>
      <action>Transition story to review: `momentum-tools sprint status-transition --story {slug} --target review`</action>
      <action>Update task {{task_map}}[slug] to completed</action>

      <action>Log merge (best-effort):
        `momentum-tools log --agent impetus --sprint {{sprint_slug}} --story {slug} --event decision --detail "Merged story/{slug} to sprint/{{sprint_slug}}"`</action>

      <output>Merged story/{slug}. Checking for newly unblocked stories...</output>

      <action>Re-evaluate dependency graph: find stories where status == "ready-for-dev" AND all depends_on stories are now "done"</action>
      <check if="newly unblocked stories found">
        <action>Return to Phase 2 (step 2) to spawn agents for newly unblocked stories</action>
      </check>
    </check>

    <check if="all sprint stories have merged (all status == 'review')">
      <action>Update task 3 (Progress Tracking) to completed</action>
      <action>Proceed to Phase 4 (AVFL)</action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: POST-MERGE AVFL — STOP GATE (Decision 31)      -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Single AVFL pass on full integrated codebase — read-only findings, no fixes">
    <action>Update task 4 (Post-Merge AVFL) to in_progress</action>
    <!-- Fix agents: spawning=individual-agent | concurrency=sequential | no worktrees — see <team-composition> above -->
    <output>All sprint stories merged. Running AVFL on the complete sprint changeset...</output>

    <action>Capture sprint diff: identify the commit before the first sprint merge and diff from there.
      Approach: use `git log --oneline` to find the merge boundary, or use a tag/ref if sprint-planning set one.
      Fallback: diff all files touched by sprint stories (union of all {{touches}} arrays).</action>
    <action>Read acceptance criteria from all sprint story files. Concatenate as {{all_acs}}.</action>

    <action>Invoke `momentum:avfl` with:
      - domain_expert: "software engineer"
      - task_context: "Sprint {{sprint_slug}} — full codebase after {{sprint_stories | length}} stories merged"
      - output_to_validate: {{sprint_diff}}
      - source_material: {{all_acs}}
      - profile: checkpoint
      - stage: final
    </action>

    <action>Store {{avfl_findings}} = full findings list from AVFL output, tagged with source="avfl" and severity per finding.</action>

    <action>Log AVFL result (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event finding --detail "AVFL complete: {{avfl_findings | length}} findings (critical: {{critical_count}}, high: {{high_count}}, medium: {{medium_count}}, low: {{low_count}})"`</action>

    <output>## AVFL Findings — Sprint {{sprint_slug}}

{{avfl_findings_report}}

---
**AVFL complete.** No fixes are applied at this stage. Proceeding to per-story code review.</output>

    <ask>Acknowledge AVFL findings and continue to per-story code review?</ask>
    <note>This is a stop gate. Do NOT spawn fix agents here. All findings are held for Phase 4c consolidation. Acknowledge and move to Phase 4b regardless of severity — critical findings are NOT a blocker at this step.</note>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4b: PER-STORY CODE REVIEW                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4.1" goal="Independent code review per merged story">
    <action>Update task 4b (Per-Story Code Review) to in_progress</action>
    <output>Running independent code review for each merged story...</output>

    <action>For each story in {{sprint_stories}} (all stories now in "review" status):
      Collect {{story_touches}} = the story's `touches` array from its story file.
    </action>

    <action>Spawn `momentum:code-reviewer` for each story IN PARALLEL (single message, one invocation per story):
      For each story {slug}:
        - Scope: files in {{story_touches}} for story {slug}
        - Context: "Code review for story {slug} — sprint {{sprint_slug}}"
        - Story file: `_bmad-output/implementation-artifacts/stories/{slug}.md`
        - Sprint branch: `sprint/{{sprint_slug}}`
      Tag each review invocation with the story slug for findings attribution.
    </action>

    <action>Wait for all per-story code reviews to complete.</action>

    <action>Store {{code_review_findings}} = merged list of all findings from all story reviews,
      each tagged with: source="code-reviewer", story_key={slug}, severity, file, description.
    </action>

    <action>Log code review results (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event finding --detail "Per-story code review: {{code_review_findings | length}} findings across {{sprint_stories | length}} stories"`</action>

    <output>Per-story code review complete. {{code_review_findings | length}} findings collected across {{sprint_stories | length}} stories.</output>
    <action>Update task 4b (Per-Story Code Review) to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4c: CONSOLIDATED FIX QUEUE                        -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4.2" goal="Merge all findings into prioritized fix queue, get developer fix/defer decisions">
    <action>Update task 4c (Consolidated Fix Queue) to in_progress</action>
    <action>Merge {{avfl_findings}} and {{code_review_findings}} into a single list {{all_findings}},
      sorted by severity: critical → high → medium → low.
      Each item retains its source tag (avfl or code-reviewer + story_key) for selective re-review routing.
    </action>

    <output>## Consolidated Fix Queue — Sprint {{sprint_slug}}

All findings from AVFL and per-story code review, sorted by severity:

{{#each all_findings grouped by severity}}
### {{severity}}
{{#each findings}}
- [{{source}}{{#if story_key}} / {{story_key}}{{/if}}] {{file}}: {{description}}
{{/each}}
{{/each}}

**Total:** {{critical_count}} critical, {{high_count}} high, {{medium_count}} medium, {{low_count}} low

---
For each item above, mark: **fix** (spawn fix agent) or **defer** (create follow-up story).</output>

    <ask>Confirm fix/defer decision for each finding. You may respond with a list (e.g., "fix all critical and high, defer the rest") or item-by-item.</ask>

    <action>Store {{fix_items}} = findings confirmed for immediate fix.
      Store {{defer_items}} = findings marked for deferral.
    </action>

    <check if="defer_items is not empty">
      <action>For each deferred finding, offer to create a follow-up backlog story with:
        - Title derived from the finding description
        - AC from the finding details
        - Source reference to the sprint and reviewer
      </action>
    </check>

    <check if="fix_items is empty">
      <output>No items confirmed for fixing. Proceeding directly to Team Review (Phase 5).</output>
      <action>Jump to Phase 5.</action>
    </check>

    <action>Log fix queue decisions (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Fix queue: {{fix_items | length}} to fix, {{defer_items | length}} deferred"`</action>
    <action>Update task 4c (Consolidated Fix Queue) to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4d: TARGETED FIXES + SELECTIVE RE-REVIEW          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4.3" goal="Spawn fix agents for confirmed items, then re-run only affected reviewers">
    <action>Update task 4d (Targeted Fixes) to in_progress</action>
    <output>Spawning fix agents for {{fix_items | length}} confirmed findings...</output>

    <action>For each item in {{fix_items}}:
      Spawn a targeted dev fix agent (no worktree — direct on sprint branch) scoped to:
        - The file(s) identified in the finding
        - The fix description from the finding detail
        - Sprint branch: `sprint/{{sprint_slug}}`
      Group fix agents by story/file proximity — spawn related fixes together where possible.
    </action>

    <action>Wait for all fix agents to complete.</action>

    <action>Log fixes applied (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Fixes applied: {{fix_items | length}} items"`</action>

    <!-- Selective re-review: only re-run reviewers whose findings were fixed -->
    <action>Determine which reviewers to re-run:
      - If any fix_items have source="avfl": schedule AVFL re-scan
      - If any fix_items have source="code-reviewer" for story {slug}: schedule code-reviewer re-run for that story only
      Do NOT re-run reviewers that had no fixed findings.
    </action>

    <check if="AVFL re-scan scheduled">
      <action>Run AVFL re-scan scoped to the files modified by fix agents.
        Use same parameters as Phase 4 but with profile: checkpoint.
      </action>
      <action>Update {{avfl_findings}} with re-scan results — remove resolved items, keep any new findings.</action>
    </check>

    <check if="code-reviewer re-run scheduled for any story">
      <action>Spawn code-reviewer for each affected story (files modified by fixes in that story's scope).
        Run in parallel if multiple stories are affected.
      </action>
      <action>Update {{code_review_findings}} — remove resolved items, keep any new findings.</action>
    </check>

    <action>Collect remaining findings (if any) from re-reviews into {{remaining_findings}}.</action>

    <check if="remaining_findings is not empty">
      <output>Re-review found remaining issues after fixes:

{{remaining_findings_summary}}

Accept these as-is, fix them now, or defer to follow-up stories?</output>
      <ask>Accept, fix, or defer remaining findings?</ask>
      <check if="developer wants to fix remaining">
        <action>Repeat Phase 4d for remaining confirmed items (single iteration — do not recurse indefinitely).</action>
      </check>
      <check if="developer defers remaining">
        <action>Offer follow-up stories for each deferred remaining finding.</action>
      </check>
    </check>

    <output>Fix and re-review cycle complete. Proceeding to Team Review.</output>

    <action>Log re-review results (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Post-fix re-review: {{remaining_findings | length}} remaining findings"`</action>
    <action>Update task 4d (Targeted Fixes) to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: TEAM REVIEW (Option C)                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Parallel team review of integrated codebase">
    <action>Update task 5 (Team Review) to in_progress</action>
    <!-- Spawning mode: individual-agent for all three roles | concurrency: parallel — see <team-composition> above -->
    <output>Running Team Review — QA, E2E Validator, and Architect Guard in parallel on integrated sprint/{{sprint_slug}}...</output>

    <action>Before spawning each reviewer, check {{spawn_registry}} for the reviewer's key:
      - QA Agent key: `sprint::qa-reviewer`
      - E2E Validator key: `sprint::e2e-validator`
      - Architect Guard key: `sprint::architecture-guard`
      If a key already exists in {{spawn_registry}}: skip that reviewer, log suppression (best-effort):
        `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Dedup: skipped duplicate spawn for {key}"`
      If a key is absent: spawn the reviewer and register the key: `{{spawn_registry}}[key] = { spawned: true }`
    </action>

    <action>Spawn eligible reviewers in parallel using individual Agent tool calls in a single message.
      NEVER use TeamCreate — each reviewer is always an individual agent spawn:

    **QA Agent** — spawn via Agent tool with `skills/momentum/agents/qa-reviewer.md` definition:
      - Provide: sprint slug, list of sprint stories, AVFL findings list
      - Agent reads each story's AC section from `_bmad-output/implementation-artifacts/stories/{slug}.md`
      - Produces structured QA Review Report with per-story AC verification

    **E2E Validator** — spawn via Agent tool with `skills/momentum/agents/e2e-validator.md` definition:
      - Provide: sprint slug, path to Gherkin specs `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/specs/`, AVFL findings list
      - Agent validates running behavior against Gherkin scenarios
      - Produces structured E2E Validation Report with per-scenario results

    **Architect Guard** — spawn `momentum:architecture-guard` skill (context: fork, read-only):
      - Provide: sprint slug, architecture doc path `_bmad-output/planning-artifacts/architecture.md`, list of touched files, sprint branch `sprint/{{sprint_slug}}`
      - Agent checks sprint changes for pattern drift against architecture decisions
      - Produces structured Architecture Guard Report with per-decision findings
    </action>

    <action>Wait for all three agents to complete.</action>
    <action>Consolidate findings into a unified fix queue, grouped by severity.
      Tag each finding with which reviewer produced it (QA / Validator / Guard) so the correct reviewer can be re-run after fixes.</action>

    <action>Log team review results (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event finding --detail "Team Review: QA={{qa_count}}, Validator={{validator_count}}, Guard={{guard_count}} findings"`</action>

    <check if="no findings from any reviewer">
      <output>Team Review passed — no findings from QA, E2E Validator, or Architect Guard.</output>
      <action>Proceed to Phase 6 (Verification)</action>
    </check>

    <check if="findings exist">
      <output>Team Review findings:

**QA Findings:**
{{qa_findings_summary}}

**E2E Validator Findings:**
{{validator_findings_summary}}

**Architect Guard Findings:**
{{guard_findings_summary}}</output>

      <ask>Address these findings now, defer to follow-up stories, or accept as-is?</ask>

      <check if="developer wants to fix">
        <action>For each accepted finding, spawn a targeted dev fix agent via individual Agent tool call
          (no worktree — direct on sprint branch). Never use TeamCreate for fix agents.</action>
        <action>After fixes, re-run only the reviewer(s) that produced the fixed findings.
          Before re-spawning each reviewer, remove its registry entry to allow the intentional re-run:
          - If QA findings were fixed: delete `{{spawn_registry}}["sprint::qa-reviewer"]`, re-spawn QA Agent, re-register key
          - If Validator findings were fixed: delete `{{spawn_registry}}["sprint::e2e-validator"]`, re-spawn E2E Validator, re-register key
          - If Guard findings were fixed: delete `{{spawn_registry}}["sprint::architecture-guard"]`, re-spawn Architect Guard, re-register key
        </action>
        <action>Repeat until clean or developer accepts remaining items.</action>
      </check>

      <check if="developer defers findings">
        <action>For each deferred finding, offer to create a follow-up story: title, description, and AC from the finding.</action>
        <action>Add accepted follow-up stories to the backlog.</action>
      </check>
    </check>
    <action>Update task 5 (Team Review) to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 6: VERIFICATION (Decision 30: Black-Box)          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="6" goal="Developer-confirmation checklist from Gherkin specs">
    <action>Update task 6 (Verification) to in_progress</action>
    <action>Read all `.feature` files from `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/specs/`</action>
    <action>For each feature file, extract all scenario names and their Given/When/Then steps</action>

    <output>## Verification Checklist — Sprint {{sprint_slug}}

Please confirm each behavior is present and correct in the merged codebase:

{{#each scenarios}}
- [ ] **{{feature}}** — {{scenario_name}}
  > {{given}} / {{when}} / {{then}}
{{/each}}

Check each item you've verified. Mark any you cannot confirm with X.</output>

    <ask>Confirm completed scenarios above.</ask>

    <action>For any unconfirmed scenarios:
      - Log as finding: `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event finding --detail "Unconfirmed scenario: {{scenario_name}}"`
      - Offer to create a follow-up story with the Gherkin scenario as the AC
    </action>

    <action>Log verification results (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Verification: {{confirmed}} / {{total}} scenarios confirmed"`</action>

    <action>Transition all sprint stories to verify:
      For each story in {{sprint_stories}}:
        `momentum-tools sprint status-transition --story {slug} --target verify`
    </action>

    <check if="all scenarios confirmed">
      <action>Transition all stories to done:
        For each story in {{sprint_stories}}:
          `momentum-tools sprint status-transition --story {slug} --target done`
      </action>
      <output>All scenarios confirmed. Sprint stories transitioned to done.</output>
    </check>

    <check if="some scenarios unconfirmed">
      <action>Transition confirmed stories to done. Leave unconfirmed at verify.</action>
      <output>Some scenarios unconfirmed. Follow-up stories created. Confirmed stories marked done.</output>
    </check>
    <action>Update task 6 (Verification) to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 7: SPRINT COMPLETION                              -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="7" goal="Archive sprint, merge to main, and surface summary">
    <action>Update task 7 (Sprint Completion) to in_progress</action>
    <action>Run: `momentum-tools sprint complete`</action>

    <action>Log sprint completion (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Sprint complete"`</action>

    <action>Merge sprint branch to main:
      1. `git checkout main`
      2. `git merge sprint/{{sprint_slug}}`
      3. If conflicts: HALT for developer resolution
      4. After successful merge: `git branch -d sprint/{{sprint_slug}}`
    </action>

    <action>Show push summary: `git log @{u}..HEAD --oneline`
      Present the full list of commits that will be pushed (all sprint planning + dev work).</action>
    <ask>Push to origin/main?</ask>
    <check if="developer confirms push">
      <action>Run: `git push`</action>
    </check>

    <output>## Sprint {{sprint_slug}} — Complete

**Stories done:** {{done_count}} / {{total_count}}
**Merge order:** {{merge_sequence}}

**AVFL:** {{avfl_findings_count}} findings
**Per-Story Code Review:** {{code_review_findings_count}} findings across {{sprint_stories | length}} stories
**Fix Queue:** {{fix_items_count}} fixed, {{defer_items_count}} deferred
**Team Review:** {{team_findings_count}} findings, {{team_resolved}} resolved, {{team_deferred}} deferred
**Verification:** {{confirmed_scenarios}} / {{total_scenarios}} scenarios confirmed

**Follow-up items:** {{followup_count}} stories added to backlog

**Agent logs:** `.claude/momentum/sprint-logs/{{sprint_slug}}/`

Sprint branch `sprint/{{sprint_slug}}` merged to main. Push when ready.

---
Run **retrospective** to analyze agent logs and surface practice improvements?</output>

    <ask>Run retrospective now?</ask>
    <action>Update task 7 (Sprint Completion) to completed</action>

    <check if="developer says yes">
      <action>Return to Impetus session menu and surface the retrospective option.</action>
    </check>
  </step>

</workflow>
