# Sprint Planning Workflow

**Goal:** Take the developer from a prioritized backlog view through story selection, fleshing-out, Gherkin spec generation, team composition, AVFL validation, and sprint activation — producing a fully specified, developer-approved sprint ready for execution.

**Voice:** Impetus voice — dry, confident, forward-moving. Symbol vocabulary: ✓ completed, → current, ◦ upcoming, ! warning, ✗ failed, ? proactive offer, · list item.

---

## EXECUTION

<workflow>
  <critical>Story markdown files retain ONLY plain English ACs. Gherkin specs are written to `sprints/{sprint-slug}/specs/` and are exclusively for verifier agents. Dev agents never access that path.</critical>
  <critical>AVFL runs ONCE on the complete sprint plan — all stories together as a single validation pass, not per-story.</critical>
  <critical>Team composition uses a two-layer model: Momentum provides generic agent roles (Dev, QA, E2E Validator, Architect Guard), and the project provides stack-specific guidelines for each role.</critical>
  <critical>Use task tracking (TaskCreate/TaskUpdate) for sprint planning steps — this prevents context drift in long runs. Ad-hoc narrative summaries are NOT a substitute for tool-queryable task state.</critical>

  <step n="0" goal="Initialize task tracking">
    <action>Create tasks for the 11 workflow steps:
      1. Synthesize recommendations from master plan and backlog
      2. Story selection
      3. Flesh out stories
      3.5. Author frozen contracts + coverage plan
      4. Generate Gherkin specs
      4.5. Spec impact analysis — update architecture and PRD
      5. Build team composition
      5.5. Validate team composition against required roles
      6. Run AVFL
      7. Developer review
      8. Activate sprint
    </action>
  </step>

  <step n="1" goal="Synthesize recommendations from master plan and backlog">
    <action>Update task 1 (Synthesize recommendations from master plan and backlog) to in_progress</action>
    <!-- Phase A: Master plan read -->
    <action>Read `{planning_artifacts}/prd.md` — extract current priorities and recent edit history (the frontmatter `editHistory` shows what was recently added or changed, indicating active areas)</action>
    <action>Read `{planning_artifacts}/product-brief-momentum-2026-03-13.md` — extract product vision and strategic goals</action>
    <action>Store a mental model of "what matters most right now" based on these documents</action>

    <check if="master plan documents are missing or empty">
      <action>Set {{has_master_plan}} = false</action>
      <note>Will fall back to sorted backlog display with warning — skip Phase C synthesis, present full backlog as primary content</note>
    </check>
    <check if="master plan documents exist and have content">
      <action>Set {{has_master_plan}} = true</action>
    </check>

    <!-- Phase A.5: Previous sprint summary load -->
    <action>Read `.momentum/sprints/index.json`</action>
    <action>Find the most recently completed sprint with `retro_run_at != null`
      (latest by `completed` date in the `completed` array)</action>

    <check if="a completed sprint with retro_run_at found">
      <action>Store {{prev_sprint_slug}} = that sprint's slug</action>
      <action>Attempt to read `.momentum/sprints/{{prev_sprint_slug}}/sprint-summary.md`</action>

      <check if="sprint-summary.md exists and has content">
        <action>Store {{prev_sprint_summary}} = file contents</action>
        <action>Include {{prev_sprint_summary}} in the "what matters most right now" synthesis context —
          use it as the "what changed most recently" signal: features that advanced last sprint narrow
          high-priority candidates; areas with incomplete stories increase urgency of follow-on work.
          This supplements PRD/backlog analysis — it does not replace it.</action>
      </check>

      <check if="sprint-summary.md does not exist">
        <output>· No sprint summary found for {{prev_sprint_slug}} — context from previous sprint unavailable.</output>
        <action>Continue without previous sprint context</action>
      </check>
    </check>

    <check if="no completed sprint with retro_run_at found">
      <action>Continue without previous sprint context — no completed retro'd sprint exists yet</action>
    </check>
    <!-- End Phase A.5 -->

    <!-- Phase A.6: Retro handoff items from practice-ledger.jsonl -->
    <action>Run: `momentum-tools practice-ledger by-source retro`
    Filter results to entities where the last event is non-terminal (not consumed/rejected/closed_stale)
    and payload.intent == "handoff". These are un-actioned retro findings handed off for sprint planning.</action>

    <check if="practice-ledger.jsonl exists AND open retro handoff items found">
      <action>Store {{retro_handoff_items}} = the filtered entity list from the command output</action>
      <action>Include {{retro_handoff_items}} in the synthesis context alongside the sprint summary.
        These are un-actioned findings from prior retros that were explicitly deferred into the ledger
        rather than immediately stubbed. Each carries provenance (payload.sprint_slug), and optionally
        feature_state_transition and failure_diagnosis context (per DEC-005 D7/D8) in its payload.
        Weight them as signals of known pain — findings with feature_state_transition indicating
        regression carry higher urgency; findings with failure_diagnosis indicate unresolved systemic
        issues that block repeatable success.</action>
    </check>

    <check if="practice-ledger.jsonl does not exist OR no open retro handoff items">
      <action>Set {{retro_handoff_items}} = []</action>
      <action>Continue without retro handoff context</action>
    </check>
    <!-- End Phase A.6 -->

    <!-- Phase B: Staleness check -->
    <action>Read `.momentum/stories/index.json`</action>
    <action>Filter: exclude stories with status in {done, dropped, closed-incomplete}</action>
    <action>For each story with status `ready-for-dev` or `in-progress`:
      · Get the story's `touches` paths
      · Run: `git log --oneline --since="30 days ago" -- {{touches_paths}}` to find recent commits
      · If commits exist, mark the story as potentially stale and store the commit evidence (one-liners)
    </action>
    <action>Partition the candidate pool:
      · {{stale_candidates}}: stories with recent git activity on their touches paths
      · {{clean_candidates}}: remaining stories (no recent activity or no touches paths to check)
    </action>

    <!-- Phase C: Synthesis and display -->
    <check if="has_master_plan is false">
      <output>! No master plan documents found — recommendations require prd.md and a product brief.
Presenting full backlog instead.

{{#if retro_handoff_items.length}}
Retro handoff items — open findings from prior sprint retros:
{{#each retro_handoff_items}}
  · [RETRO:{{sprint_slug}}] {{title}}
    {{#if feature_state_transition}}Feature state: {{feature_state_transition.epic_slug}} {{feature_state_transition.prior_state}} → {{feature_state_transition.observed_state}}{{/if}}
    {{#if failure_diagnosis}}Failure: {{failure_diagnosis.attempted}} — {{failure_diagnosis.didnt_work}}{{/if}}
{{/each}}

These open findings were not stubbed in the retro that produced them. Consider whether any should be added to this sprint.

{{/if}}
Backlog — N stories across M epics

[Epic: epic-slug-1]
  1. [C] story-slug-a — Title · status · deps: [✓ dep1, ◦ dep2] · file: true
  2. [L] story-slug-b — Title · status · deps: none · file: false
  ...

Select 2-8 stories for this sprint by number or slug.</output>
    </check>

    <check if="has_master_plan is true">
      <action>From {{clean_candidates}}, select 3-5 top recommendations:
        · Weight by: priority field (critical > high > medium > low), master plan alignment (stories touching areas flagged as high priority in prd.md or product brief rank higher), dependency readiness (all depends_on satisfied > some pending), recency of related PRD edits
        · Also weight {{retro_handoff_items}} items: feature-state regression items (prior_state → observed_state showing regression) elevate urgency; failure-diagnosis items signal systemic issues worth blocking on
        · Write a 1-2 sentence rationale for each recommendation explaining why this story matters now, grounded in master plan priorities and readiness
      </action>
      <action>Group the full backlog by `epic_slug`, sorted within each epic by: (1) priority — critical first, then high, medium, low; (2) dependency depth — leaves first; (3) alphabetical</action>

      <output>
Sprint Planning — Recommendations

Based on the master plan and current backlog state:

  1. [H] story-slug — Title
     Why now: rationale based on master plan priorities and readiness

  2. [C] story-slug — Title
     Why now: rationale

  3. [H] story-slug — Title
     Why now: rationale

  ...

{{#if retro_handoff_items.length}}
Retro handoff items — {{retro_handoff_items.length}} open finding(s) from prior sprint(s):
{{#each retro_handoff_items}}
  · [{{sprint_slug}}] {{title}}
    {{#if feature_state_transition}}Feature state: {{feature_state_transition.epic_slug}} {{feature_state_transition.prior_state}} → {{feature_state_transition.observed_state}}{{/if}}
    {{#if failure_diagnosis}}Failure: {{failure_diagnosis.attempted}} — {{failure_diagnosis.didnt_work}}{{/if}}
    {{description}}
{{/each}}

These findings were not stubbed in their originating retro. Add any to this sprint by entering their title or the keyword "handoff-N" during story selection.
{{/if}}

Potentially stale (may already be implemented):
  · story-slug — Title · recent commits: a1b2c3d "commit msg", e4f5g6h "commit msg"
  · story-slug — Title · recent commits: ...

Full backlog — N stories across M epics:
[Epic: epic-slug-1]
  1. [C] story-slug-a — Title · status · deps: [✓ dep1, ◦ dep2] · file: true
  2. [L] story-slug-b — Title · status · deps: none · file: false
  ...

[Epic: epic-slug-2]
  3. [M] story-slug-c — Title · status · deps: [✓ dep1] · file: true
  ...

Select 2-8 stories for this sprint by number or slug.
      </output>
    </check>

    <action>Update task 1 (Synthesize recommendations from master plan and backlog) to completed</action>
  </step>

  <step n="2" goal="Story selection">
    <action>Update task 2 (Story selection) to in_progress</action>
    <ask>Select 2-8 stories for this sprint. Enter numbers or slugs, comma-separated.
If you want to include a retro handoff item as a story, enter "handoff-N" (where N is its position in the retro handoff list above) or paste the item title.</ask>

    <action>Parse the developer's selection — accept numbers (from the backlog display), story slugs, or "handoff-N" references to retro handoff items</action>

    <check if="selection includes one or more handoff-N references or retro handoff item titles">
      <action>For each referenced handoff item:
        1. Look up the item in {{retro_handoff_items}} by index (handoff-N) or title match
        2. Create a story stub from the handoff event:
           - Generate slug from the handoff item title (kebab-case, max 50 chars)
           - Run: `momentum-tools sprint story-add --slug {{slug}} --title "{{item.title}}" --epic impetus-epic-orchestrator`
             (use appropriate epic if discernible from epic_slug context)
           - Write story stub file at `.momentum/stories/{{slug}}.md`
             with the handoff item's description, epic_slug, story_type, and any
             feature_state_transition / failure_diagnosis context in the story's Description section
        3. Mark the handoff item consumed:
           Run: `momentum-tools practice-ledger append --event-type consumed --entity-id "{{item.entity_id}}" --source "sprint-planning" --actor "sprint-planning" --payload '{"outcome_ref":"{{slug}}"}'`
        4. Add the new slug to the sprint selection
      </action>
      <output>Handoff items promoted to story stubs:
{{#each promoted_handoff_stories}}
  · {{original_title}} → story: {{slug}} (practice-ledger entity consumed)
{{/each}}</output>
    </check>

    <action>Validate: selection count must be between 2 and 8 (inclusive)</action>

    <check if="fewer than 2 or more than 8 stories selected">
      <output>! Sprint requires 2-8 stories. You selected {{count}}. Adjust your selection.</output>
      <action>Re-present the selection prompt</action>
    </check>

    <action>Dependency analysis: for each selected story, check if every slug in its `depends_on` is either:
      (a) status `done` in stories/index.json, OR
      (b) included in this sprint's selection
    If neither condition is met, flag as a dependency warning.</action>

    <check if="dependency warnings exist">
      <output>! Dependency warnings:
  · story-slug depends on dep-slug (status: {{dep_status}}, not in this sprint)
  ...

These stories may be blocked during execution. Proceed anyway, or adjust selection?</output>
      <ask>Proceed with current selection, or revise?</ask>
    </check>

    <action>Generate sprint slug: `sprint-YYYY-MM-DD` using today's date. If a sprint with that slug already exists in sprints/index.json completed list, append sequence number: `sprint-YYYY-MM-DD-2`</action>

    <action>Store {{sprint_slug}} and {{selected_stories}} for subsequent steps</action>

    <action>Create sprint branch from main:
      `git checkout main && git checkout -b sprint/{{sprint_slug}}`
      All planning artifacts (stories, specs, team composition) will be committed to this branch.
      The branch merges to main only when the sprint is complete and verified.</action>

    <action>Register selected stories in the planning sprint:
      `momentum-tools sprint plan --operation add --stories {{comma-separated-slugs}}`</action>

    <output>## Sprint `{{sprint_slug}}` — {{count}} Stories Selected

{{numbered list of selected story titles}}

Proceeding to flesh out story stubs.</output>
    <action>Update task 2 (Story selection) to completed</action>
  </step>

  <step n="3" goal="Flesh out stories and record per-story approval">
    <action>Update task 3 (Flesh out stories) to in_progress</action>

    <!-- Per-story loop: repeat steps 3a–3b for every story in {{selected_stories}} -->
    <for-each item="story_slug" in="{{selected_stories}}">

      <!-- Step 3a: Flesh out the story if needed -->
      <action>Check `story_file` field for {{story_slug}} in stories/index.json</action>

      <check if="story_file is false OR story content is a stub">
        <action>Spawn `momentum:create-story` to flesh out the story stub into a full story with:
          · Acceptance criteria (plain English only — no Gherkin)
          · Dev notes
          · Tasks breakdown
        </action>
      </check>

      <!-- Step 3b: Per-story review and approval gate — repeats within this story until A or J -->
      <action>Open the story in a cmux markdown viewer (BLOCKING — do not proceed until developer responds):
        `cmux markdown open .momentum/stories/{{story_slug}}.md`
        Capture the surface ref from the output, then:
        `cmux rename-tab --surface <captured-surface-ref> "Story Review — {{story_slug}}"`</action>

      <output>Story {{story_slug}} is open in the right pane. Review it fully before responding.

This is a BLOCKING GATE — the sprint cannot activate until every story is explicitly approved.

  A — Approve this story as written
  R — Request revisions (re-run create-story with your feedback)
  J — Reject this story (remove from sprint)</output>
      <ask>Your decision [A/R/J]:</ask>

      <check if="developer selects A (Approve)">
        <action>Record approval: `momentum-tools sprint story-approve --slug {{story_slug}} --decision approved`</action>
        <output>✓ {{story_slug}} approved and recorded.</output>
      </check>

      <check if="developer selects R (Revise)">
        <ask>Describe the revisions needed:</ask>
        <action>Re-spawn `momentum:create-story` with the developer's revision feedback</action>
        <action>Re-open the revised story in cmux:
          `cmux markdown open .momentum/stories/{{story_slug}}.md`
          Capture the surface ref from the output, then:
          `cmux rename-tab --surface <captured-surface-ref> "Story Review (Revised) — {{story_slug}}"`</action>
        <action>Re-present the A/R/J approval prompt. Repeat until the developer selects A or J.</action>
      </check>

      <check if="developer selects J (Reject)">
        <action>Remove story from sprint: `momentum-tools sprint plan --operation remove --stories {{story_slug}}`</action>
        <action>Record rejection: `momentum-tools sprint story-approve --slug {{story_slug}} --decision rejected`</action>
        <output>✗ {{story_slug}} rejected and removed from sprint.</output>
        <check if="removing this story drops sprint below 2 stories">
          <action>HALT — sprint cannot proceed with fewer than 2 stories. Developer must run a fresh sprint-planning session or manually add stories via `momentum-tools sprint plan --operation add` before continuing.</action>
        </check>
      </check>

      <!-- Repeat for next story until all stories in {{selected_stories}} are processed -->
    </for-each>

    <action>After all stories have been approved:</action>
    <output>> All **{{count}} stories** approved. Proceeding to contract authoring.</output>
    <action>Update task 3 (Flesh out stories) to completed</action>
  </step>

  <step n="3.5" goal="Author frozen contracts + coverage plan + adversarial guard">
    <action>Update task 3.5 (Author frozen contracts + coverage plan) to in_progress</action>

    <!-- Load method-routing table and harness defaults -->
    <action>Read `skills/momentum/references/rules/verification-standard.md` — extract the method-routing table (Section 1) and the anti-insider-knowledge guard rules (Section 4). This table is authoritative for all contract format decisions below.</action>
    <action>Read `skills/momentum/skills/sprint-planning/references/contract-format-guide.md` — load per-change-type authoring rules, file extension mapping, multi-type precedence ordering, and the anti-insider checklist.</action>

    <!-- Phase A: Contract authoring -->
    <action>Create the sprint specs directory: `.momentum/sprints/{{sprint_slug}}/specs/`</action>

    <action>For each approved story in {{selected_stories}}:
      1. Compute `verification_method` from the story's `change_type`:
         Run: `momentum-tools sprint compute-verification-method --story {{story_slug}}`
         The output field `verification_method` is the closed-enum token (skill-invoke |
         behavioral-trigger | bash | smoke | curl | document-review) drawn from the
         method-routing table in verification-standard.md Section 1. Store as {{vm}}.
         harness_profile equals {{vm}} (no project override applies unless explicitly declared
         in momentum/verification-harness.json). `verification_method` and `harness_profile`
         are machine-readable routing signals — they are single tokens, never free-text sentences.

      2. Determine the contract file extension using the precedence table in contract-format-guide.md
         (for multi-change-type stories: app-ui > script-code > script-cli > backend > agent-definition
          > skill-instruction > rule-hook > config-structure > specification > research-spike)

      3. Read the story's plain English Acceptance Criteria from its story file
         · Do NOT read any `.feature` files — they do not exist yet at this point
         · Do NOT read SKILL.md files or workflow.md files for the implementation being specified

      4. Author the contract body:
         · State what must be observably true about the story's behavior
         · Every clause must pass the Outsider Test: a person with no source code access
           must be able to verify it by invoking skills, running commands, or reading outputs
         · Include `harness_profile` referencing a driver declared in `momentum/verification-harness.json`
         · Follow the per-change-type format in contract-format-guide.md

      5. Prepend the mandatory Part-A verification header to the contract body before writing.
         The header fields MUST appear in this exact order (see contract-format-guide.md
         "Mandatory Verification Header" section for format per contract type):
           story_slug: {{story_slug}}
           verification_method: {{vm}}              ← closed-enum token computed in step 1
           harness_profile: {{vm}}                  ← same token; project overrides listed in momentum/verification-harness.json
           contract_path: .momentum/sprints/{{sprint_slug}}/specs/{{story_slug}}.{{ext}}
           how_dev_self_checks: |
             <plain-language self-check the developer follows to confirm this story is done;
              no insider knowledge; Outsider Test applies — an outside reader must be able
              to follow it using only skill invocations, commands, and observable outputs>
           coverage_disposition: dedicated-run      ← placeholder; Phase B back-fills the real value
           covered_by_scenario: null               ← placeholder; Phase B back-fills
           acceptance_criteria_ref: .momentum/stories/{{story_slug}}.md#acceptance-criteria
           platforms: [host]

         Set {{contract_metadata[story_slug]}} = {
           verification_method: {{vm}},
           harness_profile: {{vm}},
           contract_path: ".momentum/sprints/{{sprint_slug}}/specs/{{story_slug}}.{{ext}}"
         }

      6. Write to `.momentum/sprints/{{sprint_slug}}/specs/{{story_slug}}.{{ext}}`

      Special case — app-ui stories:
        · Write the `.feature` contract here in Phase A
        · This `.feature` is the canonical spec-of-done; Step 4 must NOT overwrite it
    </action>

    <output>## Contracts Authored

{{for each story: · {{story_slug}}.{{ext}} — {{change_type}} → {{verification_method}}}}

Contracts written to `sprints/{{sprint_slug}}/specs/`. Proceeding to coverage plan.</output>

    <!-- Phase B: Coverage plan -->
    <action>Read all authored contract bodies together</action>
    <action>Identify stories whose observable behaviors overlap at the integration level:
      · An integration scenario exists when Story A's verification invocation exercises the same system boundary that Story B's trigger condition monitors
      · Mark these stories as candidates for "covered-by-composition"
    </action>

    <action>Author `coverage-plan.md`:
      Open with the anti-redundancy principle note:
        "Never validate in isolation what an integrated scenario already exercises."

      For each integration scenario:
        · Name: [scenario name]
        · Description: [brief behavioral description — what the user does and what they observe]
        · Discharges: [list of story slugs this scenario verifies] · [file/span paths exercised]
        · Mark each listed story as "covered-by-composition" with a rationale sentence

      For each story NOT covered by any integration scenario:
        · List as "dedicated-run" — a standalone verification target

      Validation: every approved story must appear exactly once (either covered-by-composition
      or dedicated-run). Every scenario must name at least one story it discharges.
    </action>

    <action>Write coverage plan to: `.momentum/sprints/{{sprint_slug}}/coverage-plan.md`</action>

    <!-- Phase B.1: Back-fill coverage_disposition and covered_by_scenario into each contract header -->
    <action>After writing coverage-plan.md, back-fill the Part-A header in every contract file with the
    actual coverage values derived from the plan:

      For each approved story in {{selected_stories}}:
        · Determine its coverage_disposition from coverage-plan.md:
            - "covered-by-composition" if it appears in a Discharges list under an integration scenario
            - "dedicated-run" if it appears in the "dedicated-run" list
        · Determine its covered_by_scenario:
            - Name of the integration scenario from coverage-plan.md if covered-by-composition
            - null if dedicated-run
        · Edit the contract file at `.momentum/sprints/{{sprint_slug}}/specs/{{story_slug}}.*`:
            Replace the placeholder `coverage_disposition: dedicated-run` line with the actual value
            Replace the placeholder `covered_by_scenario: null` line with the actual value
        · Update {{contract_metadata[story_slug]}} with:
            coverage_disposition: <actual>
            covered_by_scenario: <actual>

      Validation: every approved story must have a populated coverage_disposition field in its
      contract header (dedicated-run or covered-by-composition — never blank or prose).
    </action>

    <output>## Coverage Plan Authored

`.momentum/sprints/{{sprint_slug}}/coverage-plan.md`

  Covered-by-composition: {{composition_count}} stories
  Dedicated-run: {{dedicated_count}} stories

Contract headers updated with coverage assignments. Proceeding to adversarial guard.</output>

    <!-- Phase C: Adversarial guard -->
    <action>Spawn a decorrelated adversarial agent:
      · This agent is NOT the same agent that authored the contracts
      · Pass it ALL contract bodies as input (paste the full text of each contract file)
      · Do NOT give the adversarial agent access to story .md files, SKILL.md files,
        workflow.md files, or any Momentum source code — only the contract text

      Adversarial agent system prompt:
        You are an adversarial contract reviewer. Your sole task is to apply the Outsider Test
        to every clause in every contract provided to you.

        The Outsider Test: Could a person who has never seen the source code verify this clause
        by ONLY invoking skills, running commands, or reading their observable outputs?

        A clause FAILS the Outsider Test if it:
          · Names which internal skill or agent is called (e.g., "delegates to X", "spawned via X")
          · Names which tool is used internally (e.g., "uses the Write tool")
          · Names which file is read internally (e.g., "reads stories/index.json")
          · Names a function, variable, or internal data structure
          · Describes internal agent decision-making rather than observable outcomes
          · References implementation details not available to an ordinary user

        For EVERY failing clause, produce a structured finding:
          - story_slug: [the story this contract belongs to]
          - clause: [the exact failing clause text]
          - reason: [one sentence explaining why this clause fails the Outsider Test]

        If no clauses fail, output: "GUARD_CLEAN — all clauses pass the Outsider Test."
    </action>

    <check if="adversarial agent reports GUARD_CLEAN">
      <output>> ✓ Adversarial guard clean — all contracts pass the Outsider Test.</output>
      <action>Set {{guard_status}} = "clean". Proceed to Step 4.</action>
    </check>

    <check if="adversarial agent reports one or more findings">
      <action>Set {{guard_status}} = "findings". Store {{guard_findings}} = list of findings.</action>
      <action>Store {{rewrite_pass_count}} = 0</action>

      <!-- Rewrite loop — maximum 2 passes -->
      <action>For each finding in {{guard_findings}}:
        · Locate the failing clause in the contract for {{finding.story_slug}}
        · Rewrite ONLY that clause to describe observable outcomes
          (do NOT rewrite the whole contract — change only the flagged clause)
        · Apply the Outsider Test self-check before saving: every clause in the rewritten contract
          must describe observable inputs, outputs, or state — not internal mechanisms
        · Save the updated contract file
      </action>
      <action>Increment {{rewrite_pass_count}} by 1</action>

      <action>Re-spawn the decorrelated adversarial agent with the rewritten contract bodies.
        Apply the same system prompt as the first run.</action>

      <check if="second run reports GUARD_CLEAN">
        <output>> ✓ Adversarial guard clean after {{rewrite_pass_count}} rewrite pass(es).</output>
        <action>Set {{guard_status}} = "clean". Proceed to Step 4.</action>
      </check>

      <check if="second run still has findings AND rewrite_pass_count < 2">
        <action>Repeat the rewrite loop once more (maximum 2 total rewrite passes)</action>
        <action>Increment {{rewrite_pass_count}} by 1</action>
        <action>Re-spawn the adversarial agent a third time</action>

        <check if="third run reports GUARD_CLEAN">
          <output>> ✓ Adversarial guard clean after {{rewrite_pass_count}} rewrite pass(es).</output>
          <action>Set {{guard_status}} = "clean". Proceed to Step 4.</action>
        </check>

        <check if="third run still has findings">
          <action>Set {{guard_status}} = "residual_failures"</action>
          <output>! Adversarial guard: residual failures after 2 rewrite passes.

The following contract clauses could not be rewritten to pass the Outsider Test:

{{for each residual finding:
  · [{{story_slug}}] "{{clause}}"
    Reason: {{reason}}
}}

These contracts contain insider-knowledge contamination that may bias verification.
The sprint CANNOT activate silently with known guard failures.</output>

          <ask>Proceed with known contaminated contracts (P), or halt planning until contracts are manually fixed (H)?</ask>

          <check if="developer selects H (Halt)">
            <action>HALT — fix the flagged contract clauses manually and re-run sprint-planning from Step 3.5 Phase C</action>
          </check>

          <check if="developer selects P (Proceed)">
            <output>! Proceeding with {{residual_count}} known guard failure(s) noted. These will be visible in the coverage plan.</output>
            <action>Append a "## Known Guard Failures" section to coverage-plan.md listing the residual findings</action>
            <action>Set {{guard_status}} = "accepted_with_failures". Proceed to Step 4.</action>
          </check>
        </check>
      </check>
    </check>

    <action>Update task 3.5 (Author frozen contracts + coverage plan) to completed</action>
  </step>

  <step n="4" goal="Generate Gherkin specs">
    <action>Update task 4 (Generate Gherkin specs) to in_progress</action>
    <action>Create the sprint specs directory (if not already created by Step 3.5):
      `.momentum/sprints/{{sprint_slug}}/specs/`</action>

    <action>Load the method-routing table from `skills/momentum/references/rules/verification-standard.md` Section 1.
    This table maps change_type → driver token (skill-invoke | behavioral-trigger | bash | smoke | curl | document-review).
    Gherkin specs (.feature files) are generated ONLY for stories whose routing token is NOT already
    determined by a non-behavioral contract format. Use change_type → routing token (from the table),
    NOT the story's verification_method_advisory field (which is informational only), to decide.</action>

    <action>For each approved story in {{selected_stories}}:
      · SKIP any story that already has a `.feature` file in `specs/` (written by Step 3.5 for app-ui stories) — that file is the canonical spec-of-done and must NOT be overwritten
      · Read the story's `change_type` from its frontmatter. Look up the routing token in the
        method-routing table. SKIP any story whose routing token is one of:
        skill-invoke, behavioral-trigger, bash, curl, document-review
        (those stories use their own dedicated contract format — .eval.yaml, .trigger.md, .smoke.sh, or .review.md — not Gherkin)
      · Only generate a .feature file for stories whose routing token is `smoke` and that do not
        already have a contract file in `specs/`
      · Do NOT read or branch on `verification_method` or `verification_method_advisory` fields —
        those are advisory hints written by create-story, not routing signals
    </action>
    <action>For each approved story WITHOUT an existing contract file in `specs/` AND with routing token `smoke`:</action>
    <action>Read the story's acceptance criteria from its story file — read ALL ACs
      holistically to understand the system's intended behavior, then write Gherkin
      scenarios that describe that behavior end-to-end.</action>
    <action>Read `skills/momentum/references/gherkin-template.md` for the required format,
      voice, tense, naming, and structure rules — including the Anti-Patterns section.
      All generated `.feature` files must follow this template exactly and avoid all
      listed anti-patterns.</action>
    <action>Generate a Gherkin `.feature` file for the **E2E Validator** — a black-box agent
      that tests running behavior without source code access. The validator can invoke skills,
      run commands, observe outputs, and check system state — but it CANNOT read SKILL.md files,
      inspect frontmatter, review code structure, or examine file contents.

      Spec rules:
      · Feature title matches the story title
      · **Write behavioral scenarios, not AC-by-AC translations.** Read all ACs together,
        understand the system's behavior holistically, then write scenarios that describe
        how the system behaves. Do NOT label scenarios with AC numbers. Do NOT create one
        scenario per AC. ACs that don't produce behavioral scenarios are simply left out —
        they are QA concerns, not E2E specs.
      · Scenarios test **observable behavior** — what happens when the system is used, not what files contain
      · ACs about file structure, frontmatter schema, naming conventions, and code patterns are QA concerns — leave them out entirely
      · Some stories may produce only 2-3 behavioral scenarios; that is correct
      · Use Given/When/Then with concrete, behavioral language
      · Include edge cases and error paths as separate Scenarios

      **The Outsider Test — apply to every scenario before writing it:**
      Could someone who has never seen the source code verify this scenario by ONLY
      invoking skills, running commands, and reading their outputs?

      If a Given/When/Then clause requires knowing:
        · which internal skill or tool was called ("delegates to bmad-dev-story")
        · which mechanism was used to spawn an agent ("spawned via the Agent tool")
        · which file was read internally ("reads the story file")
        · what an agent did NOT do internally ("does not perform worktree management")
      ...it fails the Outsider Test. Rewrite it to describe the **observable outcome**:
        · "delegates to X" → "the story gets implemented and changes are committed"
        · "spawned via X" → "an agent runs and produces a findings report"
        · "reads file X" → "proceeds without requesting additional input"
        · "does not perform X" → describe the observable absence ("no worktree artifacts remain")
    </action>
    <action>Before writing the spec, perform a self-check on every Generated/When/Then clause:
      Apply the Outsider Test to each clause — could someone who has never seen the source code
      verify this clause by ONLY invoking skills, running commands, and reading outputs?

      Clauses that fail the Outsider Test:
        · Reference which internal skill or tool was called ("delegates to bmad-dev-story", "uses the Agent tool")
        · Reference which mechanism spawned an agent ("spawned via Agent tool")
        · Reference what a file contains internally ("reads the story file's Dev Notes")
        · Reference what an agent did NOT do internally ("does not perform worktree management")
        · Use AC numbers or phase numbers in scenario names ("AC 1", "Phase 2")
        · Use passive voice in When clauses ("When quick-fix is invoked")

      For each failing clause: rewrite it to describe the observable outcome before saving.
      Do NOT save a spec that contains failing clauses — rewrite until all pass.
    </action>

    <action>Write the spec to: `.momentum/sprints/{{sprint_slug}}/specs/{{story_slug}}.feature`</action>

    <action>Do NOT modify the story markdown file — story files retain plain English ACs only</action>

    <!-- Post-generation validation gate: runs after ALL specs are written -->
    <action>After generating all specs, run a structural validation pass over every generated `.feature` file:

      For each `.feature` file, check:
        1. **Structure:** Every scenario has at least one Given, one When, and one Then clause
        2. **Naming:** No scenario name contains AC numbers ("AC 1", "AC-2", "AC3") or phase numbers ("Phase 1", "Phase 2")
        3. **Outsider Test:** No Given/When/Then clause references internal agent names (used as mechanism), tool names, or file paths in a way that fails the Outsider Test
        4. **Format:** Indentation matches gherkin-template.md (Feature: no indent, Background/Scenario: 2 spaces, Given/When/Then: 4 spaces); no tags, no Scenario Outline, no comments

      On validation failure:
        · Surface the specific file, scenario name, and failing clause to the developer
        · State why the clause fails (structure gap, naming violation, outsider-test failure, or format error)
        · Regenerate the affected spec before proceeding to team composition
        · Re-run validation on the regenerated spec

      Only proceed to Step 4.5 when all specs pass all four checks.
    </action>

    <output>## Gherkin Specs Generated and Validated

{{for each story: · story_slug — N scenarios}}

**Specs written to** `sprints/{{sprint_slug}}/specs/` — for verifier agents only, dev agents will not see them.

Proceeding to spec impact analysis.</output>
    <action>Update task 4 (Generate Gherkin specs) to completed</action>
  </step>

  <step n="4.5" goal="Spec impact analysis — update architecture and PRD">
    <action>Update task 4.5 (Spec impact analysis) to in_progress</action>
    <action>Spawn two parallel discovery subagents:

    **Architecture discovery agent:**
      Large-file protocol (mandatory — apply before reading any large file):
        1. Run `wc -l` on architecture.md first. For files over 200 lines, read in 500-line
           chunks via Read offset/limit. Never attempt a full Read on architecture.md,
           prd.md, or stories/index.json. If a Read fails with a token-limit error, do not
           retry the same read — use Grep to find the specific section, then read that section.
      Read `{planning_artifacts}/architecture.md` (using the large-file protocol above) and all approved story files.
      For each story, identify:
        · New architecture decisions introduced (patterns, protocols, storage, deployment)
        · Changes to existing decisions (modified constraints, new options)
        · New components, data flows, or integration points
      Return a structured list: [{story_slug, decision_type, summary, section_affected}]

    **PRD discovery agent:**
      Large-file protocol (mandatory — apply before reading any large file):
        1. Run `wc -l` on prd.md first. For files over 200 lines, read in 500-line chunks
           via Read offset/limit. Never attempt a full Read on prd.md, architecture.md,
           or stories/index.json. If a Read fails with a token-limit error, do not retry
           the same read — use Grep to find the specific section, then read that section.
      Read `{planning_artifacts}/prd.md` (using the large-file protocol above) and all approved story files.
      For each story, identify:
        · New functional requirements (capabilities not covered by existing FRs)
        · Modifications to existing FRs (changed behavior, new constraints)
        · New non-functional requirements
      Return a structured list: [{story_slug, fr_type, summary, section_affected}]
    </action>

    <action>Consolidate discovery results:
      · Merge both lists into a single spec impact report
      · Classify each item as NEW (not in specs) or MODIFIED (exists but needs update)
      · Filter out items that are already covered by existing spec content
    </action>

    <check if="no spec impact found">
      <output>> ✓ No spec impact detected — architecture and PRD already cover this sprint's scope.</output>
      <action>Proceed to Step 5</action>
    </check>

    <check if="spec impact found">
      <output>Spec impact detected — {{count}} items need documentation:

  Architecture:
    {{for each arch item: · [NEW|MODIFIED] decision_type — summary (story_slug)}}

  PRD:
    {{for each prd item: · [NEW|MODIFIED] fr_type — summary (story_slug)}}

Updating specs now.</output>

      <action>Spawn two parallel update subagents:

      **Architecture update agent:**
        Large-file protocol: Run `wc -l` on architecture.md first. Read in 500-line chunks
        via Read offset/limit for files over 200 lines. Never attempt a full Read.
        Read `{planning_artifacts}/architecture.md` (chunked).
        Apply each architecture impact item:
          · NEW decisions: add to the appropriate section following existing format
          · MODIFIED decisions: update the existing section in place
        Write the updated file. Follow existing document style and conventions.

      **PRD update agent:**
        Large-file protocol: Run `wc -l` on prd.md first. Read in 500-line chunks
        via Read offset/limit for files over 200 lines. Never attempt a full Read.
        Read `{planning_artifacts}/prd.md` (chunked).
        Apply each PRD impact item:
          · NEW FRs: assign next available FR number, add to appropriate section
          · MODIFIED FRs: update existing FR text in place
        Write the updated file. Follow existing document style and conventions.
      </action>

      <output>## ✓ Specs Updated

- **Architecture:** {{arch_count}} items
- **PRD:** {{prd_count}} items

Proceeding to team composition.</output>
    </check>
    <action>Update task 4.5 (Spec impact analysis) to completed</action>
  </step>

  <step n="5" goal="Build team composition and execution plan">
    <action>Update task 5 (Build team composition) to in_progress</action>
    <action>Analyze each selected story's `change_type` and `touches` paths to determine required agent roles:

    Role determination rules:
      · **Dev** — always required (every story needs implementation)
      · **QA** — required when `change_type` includes code, scripts, or configuration
      · **E2E Validator** — required when story has end-to-end behavioral impact (touches multiple system boundaries)
      · **Architect Guard** — required when story touches architecture patterns, creates new modules, or modifies structural decisions
    </action>

    <action>For each required role, check if the project provides stack-specific guidelines:
      · Look for project config or role-specific guideline files
      · If project guidelines exist, attach them to the role for this sprint
      · If not, note that the role will use Momentum's generic patterns only
    </action>

    <action>Domain classification — assign a specialist dev agent per story based on `touches` paths:

    For each story, iterate its `touches` paths and match against this table (order matters — first match wins per path):

      | Pattern                                                        | Specialist     |
      |----------------------------------------------------------------|----------------|
      | `skills/*/SKILL.md`, `skills/*/workflow.md`, `agents/*.md`     | dev-skills     |
      | `*.gradle*`, `*.kts`, `build.gradle*`                          | dev-build      |
      | `*compose*`, `*Compose*`, `*ui/*`, `*screen*`                  | dev-frontend   |
      | (no match)                                                     | dev (base)     |

    Resolution when a story's paths match multiple specialist types:
      · Tally matches per specialist type across all `touches` paths
      · Assign the specialist with the most matching paths (majority rule)
      · Ties break to the first specialist in table order (most specific)
      · If no paths match any pattern, assign `dev` (base agent)

    Store the specialist assignment per story in {{team}}.story_assignments[slug].specialist
    </action>

    <!-- Guidelines Verification Gate -->
    <action>For each specialist domain assigned across all sprint stories, check whether project guidelines exist:
      · Derive candidate filenames from the specialist domain: lowercase, hyphenated
        (e.g., domain "Kotlin Compose" → check for `kotlin-compose.md`, `compose.md`, `kotlin.md`)
      · Check `.claude/rules/` for any file matching those candidates
      · This is a file existence check only — do not parse or validate content
      · Build a map: {{guidelines_map}} = { domain → { status: "present" | "missing", stories: [slugs] } }
      · For stories using the base Dev agent (no specialist), set guidelines_status = "n/a"
    </action>

    <check if="all specialist domains have guidelines present">
      <action>Set guidelines_status = "present" for all specialist stories, "n/a" for base Dev stories. Continue silently — no output, no developer interaction.</action>
    </check>

    <check if="one or more specialist domains are missing guidelines">
      <output>! Missing guidelines for {{missing_count}} specialist domain(s):
  {{for each missing domain:
    ! {{domain}} — affects: {{comma-separated story titles}}
  }}

Specialists without project guidelines fall back to built-in defaults only. This may produce code that violates project conventions or uses outdated patterns.

For each missing domain, choose:
  (G) Generate — run momentum:agent-guidelines now (planning pauses until done)
  (P) Proceed — keep specialist, accept built-in defaults only
  (D) Downgrade — replace specialist with base Dev agent for affected stories</output>

      <ask>Enter choice per domain (e.g., "kotlin-compose: G, fastapi: P"):</ask>

      <action>Process developer choices per missing domain:

      For domains where developer chose **(G) Generate**:
        1. Invoke `momentum:agent-guidelines` with the missing domain as context
        2. Wait for the skill to complete (interactive — developer goes through the consultation workflow)
        3. Re-check `.claude/rules/` for the domain's candidate filenames
        4. If guidelines now exist: set guidelines_status = "present" for affected stories
        5. If still missing (generation was cancelled or failed): fall back to Proceed behavior

      For domains where developer chose **(P) Proceed**:
        1. Keep the specialist assignment unchanged
        2. Set guidelines_status = "missing" for affected stories

      For domains where developer chose **(D) Downgrade**:
        1. Replace the specialist with the base Dev agent for all affected stories
        2. Set guidelines_status = "skipped" for affected stories
      </action>
    </check>
    <!-- End Guidelines Verification Gate -->

    <action>Check for `touches` path overlaps across stories:
      · For each pair of selected stories, compare their `touches` arrays
      · If two stories touch the same file or directory, flag as merge conflict risk
      · Stories with overlapping touches should be in different waves (sequential execution) or flagged for careful merge review
      · Surface overlaps in the execution plan output</action>

    <action>Build the dependency graph from `depends_on` fields:
      · Identify which selected stories depend on other selected stories
      · Compute execution waves — groups of stories that can run concurrently because they have no inter-dependencies within the group
      · Wave 1: stories with no dependencies on other selected stories
      · Wave 2: stories whose dependencies are all in Wave 1
      · Wave N: stories whose dependencies are all in Waves 1..N-1
    </action>

    <action>Assign wave numbers via momentum-tools:
      For each wave, run: `momentum-tools sprint plan --operation add --stories {{wave_slugs}} --wave {{wave_number}}`</action>

    <output>Execution plan built:

Team composition:
  {{for each role: · Role — N stories, guidelines: [project-specific | generic]}}

Dev specialists and guidelines:
  {{for each story:
    · story_slug — specialist: {{specialist_domain | "base Dev"}} · guidelines: {{guidelines_status}}
  }}

Dependency graph:
  Wave 1 (parallel): {{story_slugs}}
  Wave 2 (after Wave 1): {{story_slugs}}
  ...

Proceeding to AVFL validation.</output>
    <action>Update task 5 (Build team composition) to completed</action>
  </step>

  <step n="5.5" goal="Validate team composition against required roles">
    <action>Update task 5.5 (Validate team composition) to in_progress</action>
    <!-- This step enforces the spawning mode declarations from the sprint-dev workflow's
         <team-composition> block. Every phase that spawns agents has declared required roles;
         sprint planning must confirm the planned team satisfies those requirements before activation. -->

    <action>Check that the planned {{team}} object satisfies the sprint-dev workflow's required roles:

      Required roles per phase (from sprint-dev workflow team-composition declaration):
        · Phase 2 (dev-wave): at least one dev-role agent assigned to each story
        · Phase 5 (team-review): QA Reviewer, E2E Validator, and Architect Guard must all be present

      For each story in {{selected_stories}}:
        · Verify story has an entry in {{team}}.story_assignments with a non-null specialist or "dev"
        · Verify the specialist agent file exists: `skills/momentum/agents/{specialist}.md`
          If it does not exist, the story has no valid agent definition — flag as gap

      For team review roles (applied to the sprint as a whole):
        · Verify `skills/momentum/agents/qa-reviewer.md` exists
        · Verify `skills/momentum/agents/e2e-validator.md` exists
        · Verify `momentum:architecture-guard` skill is available (check skills/momentum/skills/architecture-guard/SKILL.md)
    </action>

    <check if="all required roles are filled and all agent files exist">
      <output>> ✓ Team composition validated — all required roles are present and agent definitions resolve.</output>
      <action>Proceed to Step 6 (AVFL validation)</action>
    </check>

    <check if="one or more gaps detected">
      <output>! Team composition gaps detected:

  {{for each gap:
    · [UNASSIGNED] story-slug — no agent assigned (no entry in story_assignments)
    · [MISSING-AGENT] story-slug — specialist {{specialist}} resolves to skills/momentum/agents/{{specialist}}.md which does not exist
    · [MISSING-REVIEWER] role — required team review agent file not found at {{path}}
  }}

These gaps will prevent sprint-dev from spawning agents for the affected phases.
Address them before activating the sprint.</output>

      <ask>Resolve gaps now (R), accept with warnings (W), or halt planning (H)?</ask>

      <check if="Resolve">
        <action>For each unassigned story: reassign specialist or downgrade to base Dev agent</action>
        <action>For each missing agent file: surface the file path that needs to be created</action>
        <action>Re-run the validation check after changes</action>
      </check>

      <check if="Accept with warnings">
        <output>! Proceeding with {{gap_count}} team composition warning(s) noted. Sprint execution will fall back to base Dev agent for stories with missing specialists.</output>
        <action>Proceed to Step 6</action>
      </check>

      <check if="Halt">
        <action>HALT — resolve team composition gaps before continuing sprint planning</action>
      </check>
    </check>
    <action>Update task 5.5 (Validate team composition) to completed</action>
  </step>

  <step n="6" goal="AVFL validation of complete sprint plan">
    <action>Update task 6 (Run AVFL) to in_progress</action>
    <action>Gather all sprint plan artifacts for validation:
      · All approved story files (full content)
      · All generated Gherkin specs
      · Team composition and role assignments
      · Dependency graph and execution waves
    </action>

    <action>Invoke the `momentum:avfl` skill with:
      · domain_expert: "sprint planner"
      · task_context: "Sprint {{sprint_slug}} — {{count}} stories, {{wave_count}} execution waves"
      · output_to_validate: concatenated sprint plan (all story ACs + team composition + wave assignments)
      · source_material: story acceptance criteria and Gherkin specs
      · profile: checkpoint
      · stage: final
    </action>

    <check if="AVFL returns CLEAN">
      <action>Store {{avfl_result}} = "CLEAN"</action>
      <output>> ✓ AVFL validation passed — sprint plan is coherent.</output>
    </check>

    <check if="AVFL returns CHECKPOINT_WARNING">
      <action>Store {{avfl_result}} = "CHECKPOINT_WARNING"</action>
      <action>Synthesize findings: severity indicators (! critical/high, · medium/low), brief descriptions</action>
      <output>AVFL found issues in the sprint plan:
  {{findings list}}

These are warnings — the plan can proceed, but consider addressing them.</output>
      <ask>Address findings now, or proceed with warnings noted?</ask>
    </check>

    <check if="AVFL returns GATE_FAILED">
      <action>Store {{avfl_result}} = "GATE_FAILED"</action>
      <action>Synthesize findings: severity indicators (! critical/high, · medium/low), brief descriptions</action>
      <output>✗ AVFL GATE FAILED — sprint plan has defects that must be resolved:
  {{findings list}}

Address all findings before the plan can proceed.</output>
      <action>HALT — resolve findings and re-run AVFL before advancing to Step 7</action>
    </check>

    <action>Update task 6 (Run AVFL) to completed</action>
  </step>

  <step n="7" goal="Developer review of complete sprint plan">
    <action>Update task 7 (Developer review) to in_progress</action>
    <output>Sprint Plan — {{sprint_slug}}

Stories ({{count}}):
  {{for each story, grouped by wave:
    Wave N:
      · story_slug — Title · Specialist: {{specialist}} · Role: Dev[, QA][, E2E][, Arch Guard] · Guidelines: {{guidelines_status}}
  }}

Team Composition:
  {{for each role:
    · Role — {{story_count}} stories · Guidelines: {{guideline_source}}
  }}
  Dev Specialists:
  {{for each specialist type:
    · {{specialist}}: {{story_slugs}} (guidelines: {{guideline_source}})
  }}

Dependency Graph:
  {{for each wave:
    Wave N: {{story_slugs}} ({{concurrency note}})
  }}

Verification Contracts: {{contract_count}} files in sprints/{{sprint_slug}}/specs/
Gherkin Specs: {{gherkin_spec_count}} .feature files in sprints/{{sprint_slug}}/specs/
Coverage Plan: sprints/{{sprint_slug}}/coverage-plan.md ({{composition_count}} covered-by-composition, {{dedicated_count}} dedicated-run)
Guard Status: {{guard_status}}

AVFL: {{avfl_result}}
    </output>

    <ask>Approve this sprint plan, or request adjustments?

  A — Approve and activate
  M — Modify (add/remove stories, change waves, adjust team)
  R — Re-run AVFL after changes</ask>

    <check if="developer selects M (Modify)">
      <action>Accept the developer's adjustments:
        · Add stories: `momentum-tools sprint plan --operation add --stories {{slugs}}`
        · Remove stories: `momentum-tools sprint plan --operation remove --stories {{slugs}}`
        · Reassign waves: re-run wave computation after changes
        · Modify team composition: update role assignments
      </action>
      <action>After modifications, re-display the updated sprint plan and re-present the approval prompt</action>
    </check>

    <check if="developer selects R (Re-run AVFL)">
      <action>Return to Step 6 and re-run AVFL with the current plan state</action>
    </check>

    <check if="developer selects A (Approve)">
      <action>Update task 7 (Developer review) to completed</action>
      <action>Proceed to Step 8</action>
    </check>
  </step>

  <step n="8" goal="Activate the sprint">
    <action>Update task 8 (Activate sprint) to in_progress</action>

    <!-- Activation gate: verify contracts and coverage plan are present -->
    <action>Pre-activation gate — verify all artifacts required by DEC-029/DEC-030 are present:

      1. For each story in {{selected_stories}}:
         · Check that `.momentum/sprints/{{sprint_slug}}/specs/{{story_slug}}.*` exists
           (any extension — eval.yaml, trigger.md, smoke.sh, review.md, or feature)
         · Build list {{missing_contracts}} of stories with no contract file

      2. Check that `.momentum/sprints/{{sprint_slug}}/coverage-plan.md` exists
         · Set {{coverage_plan_missing}} = true if absent
    </action>

    <check if="{{missing_contracts}} is non-empty OR {{coverage_plan_missing}} is true">
      <output>✗ Sprint activation blocked — verification artifacts are missing:

{{#if missing_contracts.length}}
  Missing contracts ({{missing_contracts.length}} stories):
  {{for each slug in missing_contracts: · .momentum/sprints/{{sprint_slug}}/specs/{{slug}}.*}}

  Return to Step 3.5 to author the missing contracts before activating.
{{/if}}

{{#if coverage_plan_missing}}
  Missing coverage plan:
  · .momentum/sprints/{{sprint_slug}}/coverage-plan.md

  Return to Step 3.5 to author the coverage plan before activating.
{{/if}}</output>
      <action>HALT — do NOT call `momentum-tools sprint activate` until all artifacts are present</action>
    </check>

    <!-- Gate passed — proceed with activation -->

    <!-- Step 8.A: Freeze contract checksums and compute merge-independence per story -->
    <action>For each story in {{selected_stories}}:
      1. Locate the contract file: `.momentum/sprints/{{sprint_slug}}/specs/{{story_slug}}.*`
      2. Compute frozen_sha256:
           Run: `python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" .momentum/sprints/{{sprint_slug}}/specs/{{story_slug}}.<ext>`
           Store as {{frozen_sha256[story_slug]}}
      3. Compute can_merge_independently:
           Read the story's `depends_on` list from `.momentum/stories/index.json`
           If `depends_on` is empty or null: set {{can_merge_independently[story_slug]}} = true
           If `depends_on` has one or more entries: set {{can_merge_independently[story_slug]}} = false
    </action>

    <!-- Step 8.B: Persist formalized story_assignments into the sprint record -->
    <action>Store team composition, guidelines status, dependency graph, and contract schema
    in the sprint record. For each story in {{selected_stories}}, call:

      `momentum-tools sprint story-set-contract \
        --slug {{story_slug}} \
        --verification-method {{contract_metadata[story_slug].verification_method}} \
        --contract-path {{contract_metadata[story_slug].contract_path}} \
        --harness-profile {{contract_metadata[story_slug].harness_profile}} \
        --coverage-disposition {{contract_metadata[story_slug].coverage_disposition}} \
        --covered-by-scenario {{contract_metadata[story_slug].covered_by_scenario | "null"}} \
        --frozen-sha256 {{frozen_sha256[story_slug]}} \
        --can-merge-independently {{can_merge_independently[story_slug]}}`

      This writes contract{path, harness_profile, coverage_disposition, covered_by_scenario,
      frozen_sha256} + verification_method + can_merge_independently into each
      planning.team.story_assignments[slug] entry in sprints/index.json.

      INVARIANT: Every story in {{selected_stories}} must have story-set-contract called exactly
      once before activation. If any call fails, HALT and surface the error before proceeding.

    Then update `.momentum/sprints/index.json` planning section (edit directly):
        - slug: {{sprint_slug}}
        - team: {{team_composition object — roles with story assignments, specialist types, and guidelines}}
          Each story_assignment entry includes: role, specialist, guidelines path, guidelines_status
          ("present", "missing", "skipped", or "n/a"), AND the contract block + verification_method
          + can_merge_independently fields just written by story-set-contract above
        - waves: {{already stored via momentum-tools}}
        - planned: today's date (YYYY-MM-DD)
    </action>

    <action>Mark planning sprint as ready:
      `momentum-tools sprint ready`</action>

    <action>Activate the sprint:
      `momentum-tools sprint activate`</action>

    <check if="activate exits non-zero with missing approvals error">
      <output>✗ Sprint activation blocked — the following stories are missing a current approved entry:

  {{for each missing slug: · {{slug}}}}

Each story must be approved (or re-approved if the file changed since last approval).
Return to Step 3 to review and approve each listed story, then retry activation.</output>
      <action>HALT — resolve all missing approvals before retrying `momentum-tools sprint activate`</action>
    </check>

    <output>## ✓ Sprint `{{sprint_slug}}` Activated

**Stories:** {{count}}
**Waves:** {{wave_count}}
**Team:** {{role_list}}
**Started:** {{today}}

> The sprint is live. Use "Continue sprint" from the session menu to begin execution.</output>
    <action>Update task 8 (Activate sprint) to completed</action>
  </step>

</workflow>
