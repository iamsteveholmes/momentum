# Quick Fix Workflow

**Goal:** Walk a single fix through 5 phases — Define, Specify, Implement, Validate, Ship — with full spec coverage (story file, Gherkin, architecture/PRD impact, AVFL, E2E/QA validation) but no multi-story ceremony.

**Voice:** Impetus voice — dry, confident, forward-moving. Symbol vocabulary: check completed, arrow current, circle upcoming, bang warning, cross failed, question proactive offer, dot list item.

---

## EXECUTION

<workflow>
  <critical>Orchestrator purity (Decision 3d): This workflow MUST NOT write files directly. Every file change happens through tool invocations (momentum-tools, cmux, git via Bash) or subagent spawns (architect, PM, create-story, dev, E2E/QA agents). The workflow orchestrates, routes, and presents — it never contains direct Edit/Write actions on project files.</critical>
  <critical>BLOCKING GATE: Phase 1 and Phase 2 each have a developer review gate. Do NOT proceed past a gate until the developer explicitly approves. If revisions are requested, re-invoke the relevant subagent and re-present.</critical>
  <critical>Single-story scope: This workflow handles exactly one story. Never present a backlog, select from multiple stories, compute waves, build dependency graphs, or run sprint activation/completion lifecycle.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: DEFINE                                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Define the fix — create story from developer description">
    <action>Create tasks for the 5 workflow phases:
      1. Define — create story from description
      2. Specify — Gherkin, spec impact, specialist, guidelines, AVFL
      3. Implement — worktree, dev agent, merge
      4. Validate — post-merge AVFL, collaborative fix loop
      5. Ship — register completion, push summary
    </action>

    <action>Log workflow start:
      `momentum-tools log --agent impetus --event decision --detail "Quick-fix workflow initiated" --sprint _unsorted`</action>

    <ask>Describe the fix you need to make. What's the problem and what should change?</ask>

    <ask>Epic slug for this fix? (default: "ad-hoc")</ask>
    <action>Store {{epic_slug}} — use "ad-hoc" if developer presses enter or gives no value</action>

    <action>Generate a story slug from the description: lowercase, hyphenated, max 50 chars. Store as {{story_slug}}</action>

    <action>Spawn `momentum:create-story` (model: sonnet, effort: medium) with:
      - The developer's description
      - epic_slug: {{epic_slug}}
      - Single-story context: no dependencies, no backlog integration
    </action>

    <action>Store {{story_file}} path from create-story output</action>

    <!-- BLOCKING GATE: Developer Review -->
    <action>Open the story spec in a cmux markdown surface for developer review:
      `cmux markdown open {{story_file}} --title "Quick Fix Story — Review & Approve"`</action>

    <output>Story created: {{story_slug}}

Review the story spec in the right pane. This is a BLOCKING GATE — the workflow will not proceed until you approve.

Options:
  A — Approve and continue to specification
  R — Revise (describe what to change)</output>

    <ask>Approve or revise?</ask>

    <check if="developer requests revisions">
      <action>Re-invoke `momentum:create-story` with the revision feedback</action>
      <action>Re-open the updated story in cmux:
        `cmux markdown open {{story_file}} --title "Quick Fix Story — Revised — Review & Approve"`</action>
      <action>Re-present the approval prompt. Repeat until approved.</action>
    </check>

    <action>Log story approval:
      `momentum-tools log --agent impetus --event decision --detail "Story {{story_slug}} approved for quick-fix" --sprint _unsorted`</action>

    <output>Story {{story_slug}} approved. Proceeding to specification.</output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: SPECIFY                                        -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Specify — Gherkin, spec impact, specialist classification, guidelines, AVFL">

    <!-- 2a: Spec impact discovery -->
    <action>Spawn two parallel discovery subagents (model: sonnet, effort: medium):

    **Architecture discovery agent:**
      Read the project's architecture doc and the approved story file.
      Identify:
        - New architecture decisions introduced
        - Changes to existing decisions
        - New components, data flows, or integration points
      Return: [{decision_type, summary, section_affected}]

    **PRD discovery agent:**
      Read the project's PRD and the approved story file.
      Identify:
        - New functional requirements not covered by existing FRs
        - Modifications to existing FRs
        - New non-functional requirements
      Return: [{fr_type, summary, section_affected}]
    </action>

    <check if="no spec impact found">
      <output>No spec impact detected — architecture and PRD already cover this fix's scope.</output>
    </check>

    <check if="spec impact found">
      <output>Spec impact detected — {{count}} items need documentation:

  Architecture:
    {{for each arch item: [NEW|MODIFIED] decision_type — summary}}

  PRD:
    {{for each prd item: [NEW|MODIFIED] fr_type — summary}}

Updating specs now.</output>

      <action>Spawn two parallel update subagents (model: sonnet, effort: medium):

      **Architecture update agent:**
        Read the architecture doc. Apply each architecture impact item:
          NEW decisions: add following existing format
          MODIFIED decisions: update in place
        Write the updated file. This agent is the sole writer of architecture.md.

      **PRD update agent:**
        Read the PRD. Apply each PRD impact item:
          NEW FRs: assign next available number, add to appropriate section
          MODIFIED FRs: update in place
        Write the updated file. This agent is the sole writer of prd.md.
      </action>

      <action>Log spec updates:
        `momentum-tools log --agent impetus --event decision --detail "Spec impact: {{count}} items updated" --sprint _unsorted`</action>
    </check>

    <!-- 2b: Generate Gherkin spec (AFTER spec updates so Gherkin can reference new decisions/FRs) -->
    <action>Spawn a Gherkin generation subagent (model: sonnet, effort: medium).

    Read the story's acceptance criteria from {{story_file}} — read ALL ACs
    holistically to understand the system's intended behavior, then write Gherkin
    scenarios that describe that behavior end-to-end.

    Read `skills/momentum/references/gherkin-template.md` for the required format,
    voice, tense, naming, and structure rules. All generated `.feature` files must
    follow this template exactly.

    Generate a Gherkin `.feature` file for the **E2E Validator** — a black-box agent
    that tests running behavior without source code access. The validator can invoke skills,
    run commands, observe outputs, and check system state — but it CANNOT read SKILL.md files,
    inspect frontmatter, review code structure, or examine file contents.

    Spec rules:
      - Feature title matches the story title
      - **Write behavioral scenarios, not AC-by-AC translations.** Read all ACs together,
        understand the system's behavior holistically, then write scenarios that describe
        how the system behaves. Do NOT label scenarios with AC numbers. Do NOT create one
        scenario per AC. ACs that don't produce behavioral scenarios are simply left out —
        they are QA concerns, not E2E specs.
      - Scenarios test **observable behavior** — what happens when the system is used, not what files contain
      - ACs about file structure, frontmatter schema, naming conventions, and code patterns are QA concerns — leave them out entirely
      - Some stories may produce only 2-3 behavioral scenarios; that is correct
      - Use Given/When/Then with concrete, behavioral language
      - Include edge cases and error paths as separate Scenarios

    **The Outsider Test — apply to every scenario before writing it:**
    Could someone who has never seen the source code verify this scenario by ONLY
    invoking skills, running commands, and reading their outputs?

    If a Given/When/Then clause requires knowing:
      - which internal skill or tool was called ("delegates to bmad-dev-story")
      - which mechanism was used to spawn an agent ("spawned via the Agent tool")
      - which file was read internally ("reads the story file")
      - what an agent did NOT do internally ("does not perform worktree management")
    ...it fails the Outsider Test. Rewrite it to describe the **observable outcome**:
      - "delegates to X" becomes "the story gets implemented and changes are committed"
      - "spawned via X" becomes "an agent runs and produces a findings report"
      - "reads file X" becomes "proceeds without requesting additional input"
      - "does not perform X" becomes describe the observable absence ("no worktree artifacts remain")

    Write the spec to: `_bmad-output/implementation-artifacts/sprints/quickfix-{{story_slug}}/specs/{{story_slug}}.feature`
    </action>

    <!-- BLOCKING GATE: Developer Review of Gherkin -->
    <action>Open the Gherkin spec in a cmux markdown surface for developer review:
      `cmux markdown open _bmad-output/implementation-artifacts/sprints/quickfix-{{story_slug}}/specs/{{story_slug}}.feature --title "Gherkin Spec — Review & Approve"`</action>

    <output>Gherkin spec generated for {{story_slug}}.

Review the spec in the right pane. This is a BLOCKING GATE — the workflow will not proceed until you approve.

Options:
  A — Approve and continue to implementation
  R — Revise (describe what to change)</output>

    <ask>Approve or revise?</ask>

    <check if="developer requests revisions">
      <action>Re-invoke the Gherkin generation subagent with the revision feedback</action>
      <action>Re-open the updated spec in cmux:
        `cmux markdown open _bmad-output/implementation-artifacts/sprints/quickfix-{{story_slug}}/specs/{{story_slug}}.feature --title "Gherkin Spec — Revised — Review & Approve"`</action>
      <action>Re-present the approval prompt. Repeat until approved.</action>
    </check>

    <action>Log Gherkin approval:
      `momentum-tools log --agent impetus --event decision --detail "Gherkin spec approved for {{story_slug}}" --sprint _unsorted`</action>

    <!-- 2c: Specialist classification -->
    <action>Read the story's `touches` array from {{story_file}} frontmatter.
    Run: `momentum-tools specialist-classify --touches "{{comma_separated_touches}}"`
    Store {{specialist}} and {{agent_file}} from the output.

    Specialist classification table (reference — the tool implements this):

      | Pattern                                                    | Specialist     |
      |------------------------------------------------------------|----------------|
      | `skills/*/SKILL.md`, `skills/*/workflow.md`, `agents/*.md` | dev-skills     |
      | `*.gradle*`, `*.kts`, `build.gradle*`                      | dev-build      |
      | `*compose*`, `*Compose*`, `*ui/*`, `*screen*`              | dev-frontend   |
      | (no match)                                                 | dev (base)     |

    Multi-match: majority rule, ties break to first in table order.
    </action>

    <!-- 2d: Guidelines verification gate -->
    <action>For the assigned specialist domain, check whether project guidelines exist:
      - Derive candidate filenames from the specialist domain (e.g., "dev-skills" checks for dev-skills.md, skills.md)
      - Check `.claude/rules/` for any file matching those candidates
      - This is a file existence check only
    </action>

    <check if="specialist domain has guidelines present">
      <action>Set guidelines_status = "present". Continue silently.</action>
    </check>

    <check if="specialist domain is missing guidelines">
      <output>! Missing guidelines for specialist: {{specialist}}

Specialists without project guidelines fall back to built-in defaults only. This may produce code that violates project conventions or uses outdated patterns.

Choose:
  (G) Generate — run momentum:agent-guidelines now (workflow pauses until done)
  (P) Proceed — keep specialist, accept built-in defaults only
  (D) Downgrade — replace specialist with base Dev agent</output>

      <ask>Choose G, P, or D:</ask>

      <check if="developer chose G">
        <action>Invoke `momentum:agent-guidelines` with the missing domain</action>
        <action>Re-check `.claude/rules/` for guidelines after generation completes</action>
        <action>If guidelines now exist: set guidelines_status = "present"</action>
        <action>If still missing: fall back to Proceed behavior</action>
      </check>

      <check if="developer chose P">
        <action>Keep specialist unchanged. Set guidelines_status = "missing".</action>
        <action>Log: `momentum-tools log --agent impetus --event decision --detail "Proceeding without guidelines for {{specialist}}" --sprint _unsorted`</action>
      </check>

      <check if="developer chose D">
        <action>Replace {{specialist}} with "dev" and {{agent_file}} with "skills/momentum/agents/dev.md". Set guidelines_status = "skipped".</action>
        <action>Log: `momentum-tools log --agent impetus --event decision --detail "Downgraded {{specialist}} to base Dev" --sprint _unsorted`</action>
      </check>
    </check>

    <!-- 2e: Register quickfix for traceability -->
    <action>Generate quickfix slug: `quickfix-{{today_YYYY-MM-DD}}`
    If that slug already exists, append sequence: `quickfix-{{today}}-2`, etc.
    Store as {{quickfix_slug}}.

    Run: `momentum-tools quickfix register --slug {{quickfix_slug}} --story {{story_slug}}`</action>

    <action>Log registration:
      `momentum-tools log --agent impetus --event decision --detail "Quickfix {{quickfix_slug}} registered for story {{story_slug}}" --sprint _unsorted`</action>

    <!-- 2f: AVFL checkpoint -->
    <action>Invoke `momentum:avfl` with:
      - domain_expert: "sprint planner"
      - task_context: "Quick-fix {{story_slug}} — story plan + Gherkin spec"
      - output_to_validate: story file content + Gherkin spec content
      - source_material: story acceptance criteria
      - profile: checkpoint
      - stage: checkpoint
    </action>

    <check if="AVFL returns CLEAN or CHECKPOINT_WARNING">
      <output>AVFL checkpoint passed. Proceeding to implementation.</output>
    </check>

    <check if="AVFL returns GATE_FAILED">
      <output>AVFL checkpoint FAILED — plan has defects that must be resolved before implementation.</output>
      <action>Address findings (re-invoke create-story or Gherkin subagent as needed). Re-run AVFL.</action>
    </check>

    <output>Specification complete:
  Story: {{story_slug}}
  Specialist: {{specialist}} (guidelines: {{guidelines_status}})
  Gherkin: {{scenario_count}} scenarios
  AVFL: passed

Proceeding to implementation.</output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: IMPLEMENT                                      -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Implement — worktree, dev agent, merge">

    <!-- 3a: Branch check and worktree creation -->
    <action>Check current branch via `git rev-parse --abbrev-ref HEAD`</action>

    <check if="current branch is not main">
      <output>! You're on `{{current_branch}}`, not `main`.
Quick-fix always creates a worktree from `main` — your current branch stays unchanged.
The fix will be developed in an isolated worktree and merged to `main` when complete.</output>
      <ask>Continue (worktree from main, your branch stays on {{current_branch}}), or switch to main first?</ask>
    </check>

    <check if="current branch is main">
      <output>→ Creating worktree from `main` for quick-fix. Your branch stays on `main`.</output>
    </check>

    <!-- 3b: Create worktree -->
    <action>Create worktree off main (does NOT change current branch):
      `git worktree add .worktrees/quickfix-{{story_slug}} main`
    Store {{worktree_path}} = `.worktrees/quickfix-{{story_slug}}`</action>

    <action>Log implementation start:
      `momentum-tools log --agent impetus --event decision --detail "Worktree created for {{story_slug}}, specialist: {{specialist}}" --sprint {{quickfix_slug}}`</action>

    <!-- 3c: Spawn specialist dev agent -->
    <action>Resolve specialist agent definition:
      - Read {{agent_file}} (e.g., `skills/momentum/agents/dev-skills.md`)
      - If the file does not exist, fall back to `skills/momentum/agents/dev.md`
      - Use the model and effort from the agent definition's frontmatter

    Spawn the specialist dev agent with:
      - Story key: {{story_slug}}
      - Story file: {{story_file}}
      - Working directory: {{worktree_path}}
      - Sprint context: {{quickfix_slug}}
      - Specialist: {{specialist}}
      - Guidelines: path to guidelines file if guidelines_status == "present", null otherwise
      - If the story's `touches` array includes paths under `skills/` or `agents/`, also pass:
        reference: `skills/momentum/references/agent-skill-development-guide.md`
    </action>

    <action>Wait for the dev agent to complete. Read its completion output.</action>

    <!-- 3d: Merge worktree to main -->
    <action>Merge the worktree branch back:
      1. `git rebase main` (from worktree branch — rebases onto latest main)
      2. `git checkout main`
      3. `git merge quickfix-{{story_slug}}`
    </action>

    <check if="rebase or merge conflicts">
      <output>Merge conflicts detected. Resolve and continue.</output>
      <action>HALT — wait for developer to resolve conflicts</action>
    </check>

    <!-- 3e: Clean up worktree -->
    <action>Clean up:
      `git worktree remove --force {{worktree_path}}`
      `git branch -d quickfix-{{story_slug}}`</action>

    <action>Log merge:
      `momentum-tools log --agent impetus --event decision --detail "Story {{story_slug}} merged to main" --sprint {{quickfix_slug}}`</action>

    <output>Implementation complete. {{story_slug}} merged to main.
Proceeding to validation.</output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: VALIDATE                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Validate — post-merge AVFL, collaborative fix loop">

    <!-- 4a: Post-merge AVFL scan -->
    <action>Invoke `momentum:avfl` with:
      - domain_expert: "software engineer"
      - task_context: "Quick-fix {{story_slug}} — post-merge validation"
      - output_to_validate: diff of changes merged to main
      - source_material: story acceptance criteria
      - profile: scan
      - stage: final
    </action>

    <check if="AVFL finds critical issues">
      <output>AVFL found critical issues. These must be resolved before team validation.</output>
      <action>Spawn a targeted fix agent on main for critical findings. Re-run AVFL after fixes.
      Do NOT proceed to team validation until critical findings are resolved.</action>
    </check>

    <check if="AVFL clean or non-critical only">
      <output>AVFL scan complete. Proceeding to team validation.</output>
    </check>

    <!-- 4b: Determine validators from change_type -->
    <action>Read the story's `change_type` field from {{story_file}} frontmatter.

    Determine which validators join the team:
      - `skill-instruction` in change_type → E2E Validator (model: sonnet, effort: medium)
      - `script-code` in change_type → QA (model: sonnet, effort: medium)
      - Both present → both validators join the team
    </action>

    <!-- 4c: Create validation team -->
    <action>Create an Agent Team via `TeamCreate` with these roles:

    **Dev agent** (resident fixer):
      Same specialist from Phase 3: {{specialist}}
      Model/effort: per agent definition
      Purpose: stays resident to fix issues as validators find them

    **Validators** (determined by change_type):

      If `skill-instruction`:
        **E2E Validator** — agent definition: `skills/momentum/agents/e2e-validator.md`
        Provide: story slug, Gherkin spec path, AVFL findings list
        Model: sonnet, effort: medium

      If `script-code`:
        **QA Reviewer** — agent definition: `skills/momentum/agents/qa-reviewer.md`
        Provide: story slug, story file path, AVFL findings list
        Model: sonnet, effort: medium

      If both change types present: include both validators.
    </action>

    <!-- 4d: Collaborative fix loop -->
    <action>The team collaborates via task list:
      1. Validators run their checks, report failures as tasks
      2. Dev agent picks up tasks and fixes immediately
      3. Validators re-verify fixed items
      4. Loop until all validators report clean or developer halts

    If the developer intervenes to halt the loop:
      - Remaining findings become documented known issues
      - The workflow proceeds to Phase 5
    </action>

    <action>Log validation results:
      `momentum-tools log --agent impetus --event decision --detail "Validation complete: {{findings_count}} findings, {{resolved_count}} resolved" --sprint {{quickfix_slug}}`</action>

    <action>Transition story to done:
      `momentum-tools sprint status-transition --story {{story_slug}} --target done --force`</action>

    <output>Validation complete. Story {{story_slug}} marked done.
Proceeding to ship.</output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: SHIP                                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Ship — register completion, push summary">

    <!-- 5a: Register quickfix completion -->
    <action>Run: `momentum-tools quickfix complete --slug {{quickfix_slug}}`</action>

    <action>Log completion:
      `momentum-tools log --agent impetus --event decision --detail "Quickfix {{quickfix_slug}} completed" --sprint {{quickfix_slug}}`</action>

    <!-- 5b: Push summary -->
    <action>Show push summary: `git log @{u}..HEAD --oneline`</action>

    <output>Quick-fix complete: {{story_slug}}

Commits ready to push:
{{push_summary}}
    </output>

    <ask>Push to remote?</ask>

    <check if="developer confirms push">
      <action>Run: `git push`</action>
      <output>Pushed.</output>
    </check>

    <check if="developer declines push">
      <output>Commits held locally. Push when ready.</output>
    </check>
  </step>

</workflow>
