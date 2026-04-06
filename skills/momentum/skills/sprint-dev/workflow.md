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
  <critical>AVFL runs ONCE after ALL stories merge — not per-story. If AVFL finds critical issues, block Team Review until resolved.</critical>
  <critical>Impetus always spawns agents. No agent spawns another agent.</critical>
  <critical>Log all sprint events via `momentum-tools log --agent impetus --sprint {slug}` at each phase transition.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 0: TASK TRACKING SETUP                              -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="0" goal="Initialize phase-level task tracking">
    <action>Create tasks for the 7 execution phases:
      1. Initialization — read sprint record, build dependency graph
      2. Dev Wave — spawn agents for unblocked stories
      3. Progress Tracking — monitor completion, propose merges, unblock next wave
      4. Post-Merge AVFL — sprint-level quality scan
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
    <action>Read `sprints/index.json`</action>
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

    <action>Log sprint start (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Sprint execution started: {{sprint_stories | length}} stories"`</action>

    <output>Sprint **{{sprint_slug}}** initialized.
{{sprint_stories | length}} stories, dependency graph resolved.
Task list created for progress tracking.</output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: DEV WAVE — TEAM SPAWN                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Spawn dev agents for unblocked stories">
    <action>Identify unblocked stories: status == "ready-for-dev" AND every story in depends_on has status == "done"</action>

    <check if="no unblocked stories and no in-progress stories">
      <check if="all stories are done">
        <action>Jump to Phase 4 (AVFL).</action>
      </check>
      <output>All remaining stories are blocked by unresolved dependencies. Sprint stalled.</output>
      <action>HALT — surface blocker analysis and return to Impetus menu.</action>
    </check>

    <action>For each unblocked story:
      1. Transition to in-progress: `momentum-tools sprint status-transition --story {slug} --target in-progress`
      2. Look up role assignment from {{team}}.story_assignments[slug]
      3. Resolve specialist agent:
         a. Read {{team}}.story_assignments[slug].specialist (e.g., "dev-skills", "dev-build", "dev-frontend", or "dev")
         b. Resolve agent definition file: `skills/momentum/agents/{specialist}.md`
         c. If the specialist file exists, use it as the agent definition
         d. If the specialist file does NOT exist, log a warning and fall back to `skills/momentum/agents/dev.md`
      4. Spawn the resolved agent with:
         - Story key: {slug}
         - Story file: `_bmad-output/implementation-artifacts/stories/{slug}.md`
         - Sprint context: {{sprint_slug}}
         - Role: {{team}}.story_assignments[slug].role
         - Specialist: {{team}}.story_assignments[slug].specialist
         - Guidelines: look up guidelines path from {{team}}.roles matching the assigned role (pass null if none)
         - Agent definition: the resolved specialist agent file (or base dev.md fallback)
         - If the story's `touches` array includes paths under `skills/` or `agents/`, also pass:
           reference: `skills/momentum/references/agent-skill-development-guide.md`
      5. Update task {{task_map}}[slug] to in_progress
    </action>

    <action>Log spawns (best-effort):
      `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "Spawned dev agents for: {{list of spawned slugs}}"`</action>

    <output>Spawned dev agents for {{unblocked_count}} unblocked stories:
{{list of spawned story slugs}}</output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: PROGRESS TRACKING LOOP                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Track progress and handle story completions">
    <note>This phase loops until all sprint stories have merged. Monitor via task status.</note>

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
        <action>Spawn a new dev agent (using `skills/momentum/agents/dev.md`) for the failed story (same parameters as Phase 2). Do not auto-retry — this is the single manual retry.</action>
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
      <action>Proceed to Phase 4 (AVFL)</action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: POST-MERGE AVFL (Decision 31)                  -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Single AVFL pass on full integrated codebase">
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

    <check if="AVFL clean (no findings or no critical/high findings)">
      <action>Log AVFL result (best-effort):
        `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event decision --detail "AVFL passed: CLEAN"`</action>
      <output>AVFL passed. Proceeding to Team Review.</output>
    </check>

    <check if="AVFL findings include critical severity">
      <action>Log AVFL critical (best-effort):
        `momentum-tools log --agent impetus --sprint {{sprint_slug}} --event finding --detail "AVFL critical findings: {{count}}"`</action>
      <output>AVFL found **critical** issues. These must be resolved before proceeding.
{{findings_summary}}</output>
      <action>Spawn targeted fix agents on the sprint branch (no worktrees) for critical findings. Re-run AVFL after fixes.</action>
      <action>Do NOT proceed to Phase 5 until all critical findings are resolved.</action>
    </check>

    <check if="AVFL findings exist but none are critical">
      <output>AVFL found non-critical issues:
{{findings_summary}}</output>
      <ask>Address before Team Review, or proceed with known issues documented?</ask>
      <check if="developer wants to fix">
        <action>Spawn targeted fix agents on the sprint branch (no worktrees). Re-run AVFL after fixes.</action>
      </check>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: TEAM REVIEW (Option C)                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Parallel team review of integrated codebase">
    <output>Running Team Review — QA, E2E Validator, and Architect Guard in parallel on integrated sprint/{{sprint_slug}}...</output>

    <action>Spawn three agents in parallel (single message, three Agent tool calls):

    **QA Agent** — spawn via Agent tool with `skills/momentum/agents/qa-reviewer.md` definition:
      - Provide: sprint slug, list of sprint stories, AVFL findings list
      - Agent reads each story's AC section from `_bmad-output/implementation-artifacts/stories/{slug}.md`
      - Produces structured QA Review Report with per-story AC verification

    **E2E Validator** — spawn via Agent tool with `skills/momentum/agents/e2e-validator.md` definition:
      - Provide: sprint slug, path to Gherkin specs `sprints/{{sprint_slug}}/specs/`, AVFL findings list
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
        <action>For each accepted finding, spawn a targeted dev fix agent (no worktree — direct on sprint branch).</action>
        <action>After fixes, re-run only the reviewer(s) that produced the fixed findings:
          - If QA findings were fixed: re-spawn QA Agent only
          - If Validator findings were fixed: re-spawn E2E Validator only
          - If Guard findings were fixed: re-spawn Architect Guard only
        </action>
        <action>Repeat until clean or developer accepts remaining items.</action>
      </check>

      <check if="developer defers findings">
        <action>For each deferred finding, offer to create a follow-up story: title, description, and AC from the finding.</action>
        <action>Add accepted follow-up stories to the backlog.</action>
      </check>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 6: VERIFICATION (Decision 30: Black-Box)          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="6" goal="Developer-confirmation checklist from Gherkin specs">
    <action>Read all `.feature` files from `sprints/{{sprint_slug}}/specs/`</action>
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
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 7: SPRINT COMPLETION                              -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="7" goal="Archive sprint, merge to main, and surface summary">
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

**AVFL:** {{avfl_findings_count}} findings, {{avfl_resolved}} resolved
**Team Review:** {{team_findings_count}} findings, {{team_resolved}} resolved, {{team_deferred}} deferred
**Verification:** {{confirmed_scenarios}} / {{total_scenarios}} scenarios confirmed

**Follow-up items:** {{followup_count}} stories added to backlog

**Agent logs:** `.claude/momentum/sprint-logs/{{sprint_slug}}/`

Sprint branch `sprint/{{sprint_slug}}` merged to main. Push when ready.

---
Run **retrospective** to analyze agent logs and surface practice improvements?</output>

    <ask>Run retrospective now?</ask>
    <check if="developer says yes">
      <action>Return to Impetus session menu and surface the retrospective option.</action>
    </check>
  </step>

</workflow>
