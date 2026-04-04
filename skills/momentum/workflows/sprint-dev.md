# Sprint Dev Workflow

**Goal:** Execute an active sprint — dependency-driven dev spawning, post-merge team review, Gherkin verification, and sprint completion.

**Invoked by:** Impetus Mode 1 → "Continue sprint"

**Architecture references:** Decision 25 (Teams Over Waves), Decision 26 (Two-Layer Agent Model), Decision 30 (Black-Box Verification), Decision 31 (AVFL at Sprint Level), FR62–FR70.

---

<workflow>
  <critical>Read the active sprint from sprints/index.json. Never invent team plans — all roles, guidelines, and dependencies come from the sprint record written by sprint-planning.</critical>
  <critical>Every merge requires explicit developer confirmation. Never auto-execute git merge.</critical>
  <critical>Dev agents never access sprints/{sprint-slug}/specs/ — verification is black-box.</critical>
  <critical>Stories are spawned strictly by dependency resolution. A story never starts before all its blockers have merged.</critical>
  <critical>AVFL runs ONCE after ALL stories merge — not per-story.</critical>
  <critical>Impetus always spawns agents. No agent spawns another agent.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: INITIALIZATION                                 -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Initialize sprint execution">
    <action>Read `_bmad-output/implementation-artifacts/sprints/index.json`</action>

    <check if="index.json has no active sprint (active == null)">
      <output>No active sprint found. Run sprint planning to create and activate a sprint first.</output>
      <action>Return to Impetus session menu.</action>
      <action>HALT</action>
    </check>

    <check if="planning.locked == false">
      <output>The planned sprint has not been activated. Run `momentum-tools sprint activate` to lock and activate it before executing.</output>
      <action>Return to Impetus session menu.</action>
      <action>HALT</action>
    </check>

    <action>Store {{sprint_slug}} = planning.slug (e.g., "sprint-2026-04-03")</action>
    <action>Store {{sprint_stories}} = planning.stories (array of story slugs)</action>
    <action>Store {{team_composition}} = planning.team_composition</action>

    <action>Read `_bmad-output/implementation-artifacts/stories/index.json`</action>
    <action>For each story in {{sprint_stories}}, read its entry: status, depends_on, touches, title</action>
    <action>Store {{story_map}} = map of story slug → {status, depends_on, touches, title}</action>

    <action>Build dependency graph: for each story, list stories that must be `done` before it can start</action>
    <action>Store {{dependency_graph}} = derived DAG from depends_on fields</action>

    <action>Create a task per story via TaskCreate:
      - Title: story title
      - Description: "depends_on: [list]" — include blockers for visibility
      Status: pending
    </action>
    <action>Store {{task_map}} = map of story slug → task ID</action>

    <output>Sprint **{{sprint_slug}}** initialized.
{{sprint_stories | length}} stories, dependency graph resolved.
Creating task list for progress tracking...</output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: DEV WAVE — TEAM SPAWN                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Spawn dev agents for unblocked stories">
    <action>Identify unblocked stories: status == "ready-for-dev" AND every story in depends_on has status == "done"</action>

    <check if="no unblocked stories and no in-progress stories">
      <output>All stories are either done or blocked by unresolved dependencies. Sprint may already be complete — check story statuses.</output>
      <action>Jump to Phase 4 (AVFL) if all stories are done. Otherwise HALT.</action>
    </check>

    <action>For each unblocked story:
      1. Transition to in-progress: `momentum-tools sprint status-transition --story {slug} --target in-progress`
      2. Retrieve role and guidelines from {{team_composition}}[slug]
      3. Spawn a momentum-dev agent with:
         - Story key: {slug}
         - Story file: `_bmad-output/implementation-artifacts/stories/{slug}.md`
         - Sprint context: {{sprint_slug}}
         - Role guidelines: {{team_composition}}[slug].guidelines (pass null if none — EDD/TDD approach from story Dev Notes governs)
      4. Update task {{task_map}}[slug] to in_progress
    </action>

    <output>Spawned dev agents for {{unblocked_count}} unblocked stories:
{{list of spawned story slugs}}</output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: PROGRESS TRACKING LOOP                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Track progress and handle story completions">
    <note>This phase loops until all sprint stories have merged. Monitor via task status.</note>

    <action>Watch task statuses. When a momentum-dev agent signals completion (task marked complete):</action>

    <check if="story agent signals merge-ready">
      <action>Read the story's completion output to get {{file_list}}</action>

      <output>Story **{slug}** is ready to merge.

Branch:  story/{slug}
Target:  main
Touches: {file_list}

Run: git rebase main story/{slug} && git merge story/{slug}</output>
      <ask>Merge story/{slug} now?</ask>

      <check if="developer confirms merge">
        <action>Run: `git rebase main story/{slug}`</action>
        <check if="rebase conflicts">
          <output>Rebase conflicts on story/{slug}. Resolve and run `git rebase --continue`.</output>
          <action>HALT — wait for developer to resolve</action>
        </check>
        <action>Run: `git merge story/{slug}`</action>
        <action>Run: `git worktree remove --force .worktrees/story-{slug}`</action>
        <action>Run: `git branch -d story/{slug}`</action>
        <action>Transition story to review: `momentum-tools sprint status-transition --story {slug} --target review`</action>
        <action>Update task {{task_map}}[slug] to completed</action>

        <output>✓ Merged story/{slug}. Checking for newly unblocked stories...</output>

        <action>Re-evaluate dependency graph: find stories in {{sprint_stories}} where status == "ready-for-dev" AND all depends_on are now "review" or "done"</action>
        <check if="newly unblocked stories found">
          <action>Return to Phase 2 (step 2) to spawn agents for newly unblocked stories</action>
        </check>
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

    <action>Capture sprint diff: `git diff HEAD~{{sprint_stories | length}}..HEAD` — or diff from sprint branch start if available</action>
    <action>Read acceptance criteria from all sprint story files. Concatenate as {{all_acs}}.</action>

    <action>Invoke `momentum-avfl` with:
      - domain_expert: "software engineer"
      - task_context: "Sprint {{sprint_slug}} — full codebase after {{sprint_stories | length}} stories merged"
      - output_to_validate: {{sprint_diff}}
      - source_material: {{all_acs}}
      - profile: checkpoint
      - stage: final
    </action>

    <check if="AVFL clean">
      <output>✓ AVFL passed. Proceeding to Team Review.</output>
    </check>

    <check if="AVFL findings">
      <output>AVFL found issues across the sprint changeset:
{{findings_summary}}</output>
      <ask>Address AVFL findings before Team Review, or proceed with known issues documented?</ask>
      <check if="developer wants to fix">
        <action>Spawn targeted fix agents on main (no worktrees) for each finding. Re-run AVFL after fixes.</action>
      </check>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: TEAM REVIEW (Option C)                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Parallel team review of integrated codebase">
    <output>Running Team Review — QA, E2E Validator, and Architect Guard in parallel on integrated main...</output>

    <action>Spawn three agents in parallel (single message, all in one Agent tool call):

    **QA Agent** (sonnet/medium):
      - Reviews merged code for all sprint stories against their ACs
      - Checks each story's acceptance criteria is demonstrably satisfied
      - Produces findings per story: {story_slug → [AC gap or defect descriptions]}

    **E2E Validator** (sonnet/medium):
      - Reads all `.feature` files from `sprints/{{sprint_slug}}/specs/`
      - For each Gherkin scenario, validates the behavior exists in the merged codebase
      - Black-box: uses only specs and observable behavior — no story file context
      - Produces findings: {scenario → pass/fail with evidence}

    **Architect Guard** (sonnet/medium):
      - Reads `_bmad-output/planning-artifacts/architecture.md` architecture decisions
      - Checks sprint changes for pattern drift against key decisions
      - Flags deviations from project conventions, naming, and structural rules
      - Produces findings: {file/pattern → decision violated}
    </action>

    <action>Wait for all three agents to complete.</action>
    <action>Consolidate findings into a unified fix queue, grouped by severity.</action>

    <check if="no findings from any reviewer">
      <output>✓ Team Review passed — no findings from QA, E2E Validator, or Architect Guard.</output>
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
        <action>For each accepted finding, spawn a targeted dev fix agent (no worktree — direct on main).</action>
        <action>After fixes, re-run the affected reviewer(s) only (not the full team review).</action>
        <action>Repeat until clean or developer accepts remaining items.</action>
      </check>

      <check if="developer defers findings">
        <action>For each deferred finding, offer to create a follow-up story: title, description, and AC from the finding.</action>
        <action>Add accepted follow-up stories to the backlog via `momentum-tools sprint plan --add {new-slug}` on the next sprint.</action>
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

Check each item you've verified. Any unchecked items become follow-up stories.</output>

    <ask>Confirm completed scenarios above. Mark any you cannot confirm with X.</ask>

    <action>For any unconfirmed scenarios: offer to create follow-up stories with the Gherkin scenario as the AC.</action>

    <action>Transition all sprint stories to verify:
      For each story in {{sprint_stories}}:
        `momentum-tools sprint status-transition --story {slug} --target verify`
    </action>

    <check if="all scenarios confirmed">
      <action>Transition all stories to done:
        For each story in {{sprint_stories}}:
          `momentum-tools sprint status-transition --story {slug} --target done`
      </action>
      <output>✓ All scenarios confirmed. Sprint stories transitioned to done.</output>
    </check>

    <check if="some scenarios unconfirmed">
      <action>Transition confirmed stories to done. Leave unconfirmed at verify.</action>
      <output>⚠ Some scenarios unconfirmed. Follow-up stories created. Confirmed stories marked done.</output>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 7: SPRINT COMPLETION                              -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="7" goal="Archive sprint and surface summary">
    <action>Run: `momentum-tools sprint complete`</action>

    <action>Build sprint summary:
      - Stories completed: count and slugs (status == done)
      - Stories with follow-ups: count and slugs (status == verify with pending items)
      - Merge order: sequence of merges from Phase 3 tracking
      - AVFL findings: count found, count resolved
      - Team Review findings: count per reviewer, count resolved vs. deferred
      - Verification: scenarios confirmed / total
      - Agent logs: `.claude/momentum/sprint-logs/{{sprint_slug}}/`
    </action>

    <output>## Sprint {{sprint_slug}} — Complete

**Stories done:** {{done_count}} / {{total_count}}
**Merge order:** {{merge_sequence}}

**AVFL:** {{avfl_findings_count}} findings → {{avfl_resolved}} resolved
**Team Review:** QA {{qa_count}}, Validator {{validator_count}}, Guard {{guard_count}} findings → {{team_resolved}} resolved, {{team_deferred}} deferred
**Verification:** {{confirmed_scenarios}} / {{total_scenarios}} scenarios confirmed

**Follow-up items:** {{followup_count}} stories added to backlog

**Agent logs:** `.claude/momentum/sprint-logs/{{sprint_slug}}/`

---
Run **retrospective** to analyze agent logs and surface practice improvements?</output>

    <ask>Run retrospective now?</ask>
    <check if="developer says yes">
      <action>Return to Impetus session menu and surface the retrospective option.</action>
    </check>
  </step>

</workflow>
