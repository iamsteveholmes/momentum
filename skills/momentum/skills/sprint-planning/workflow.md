# Sprint Planning Workflow

**Goal:** Take the developer from a prioritized backlog view through story selection, fleshing-out, Gherkin spec generation, team composition, AVFL validation, and sprint activation — producing a fully specified, developer-approved sprint ready for execution.

**Voice:** Impetus voice — dry, confident, forward-moving. Symbol vocabulary: ✓ completed, → current, ◦ upcoming, ! warning, ✗ failed, ? proactive offer, · list item.

---

## EXECUTION

<workflow>
  <critical>Story markdown files retain ONLY plain English ACs. Gherkin specs are written to `sprints/{sprint-slug}/specs/` and are exclusively for verifier agents. Dev agents never access that path.</critical>
  <critical>AVFL runs ONCE on the complete sprint plan — all stories together as a single validation pass, not per-story.</critical>
  <critical>Team composition uses a two-layer model: Momentum provides generic agent roles (Dev, QA, E2E Validator, Architect Guard), and the project provides stack-specific guidelines for each role.</critical>
  <critical>All planning decisions must be logged via `momentum-tools log` throughout the workflow.</critical>

  <step n="0" goal="Initialize task tracking">
    <action>Create tasks for the 9 workflow steps:
      1. Show prioritized backlog
      2. Story selection
      3. Flesh out stories
      4. Generate Gherkin specs
      4.5. Spec impact analysis — update architecture and PRD
      5. Build team composition
      6. Run AVFL
      7. Developer review
      8. Activate sprint
    </action>
    <action>Log workflow start:
      `momentum-tools log --agent impetus --event decision --detail "Sprint planning workflow initiated" --sprint _unsorted`</action>
  </step>

  <step n="1" goal="Show prioritized backlog">
    <action>Read `{implementation_artifacts}/stories/index.json`</action>
    <action>Filter: exclude stories with status in {done, dropped, closed-incomplete}</action>
    <action>Group remaining stories by `epic_slug`</action>
    <action>Within each epic, sort stories by dependency depth (leaves first — stories with no unsatisfied depends_on appear before those with pending dependencies), then alphabetical within the same depth</action>
    <action>For each story, display:
      · title
      · status (backlog, ready-for-dev, in-progress, review, verify)
      · depends_on (list dependency slugs; mark satisfied dependencies with ✓, unsatisfied with ◦)
      · story_file (true/false — indicates whether a full story file exists)
    </action>
    <action>Display count summary at top: "N stories across M epics"</action>
    <action>Highlight stories with status `backlog` or `ready-for-dev` as selectable candidates</action>

    <output>
Backlog — N stories across M epics

[Epic: epic-slug-1]
  1. story-slug-a — Title · status · deps: [✓ dep1, ◦ dep2] · file: true
  2. story-slug-b — Title · status · deps: none · file: false
  ...

[Epic: epic-slug-2]
  3. story-slug-c — Title · status · deps: [✓ dep1] · file: true
  ...

Select 3-8 stories for this sprint by number or slug.
    </output>

    <action>Log backlog presentation:
      `momentum-tools log --agent impetus --event decision --detail "Backlog presented: N stories across M epics, K selectable" --sprint _unsorted`</action>
  </step>

  <step n="2" goal="Story selection">
    <ask>Select 3-8 stories for this sprint. Enter numbers or slugs, comma-separated.</ask>

    <action>Parse the developer's selection — accept numbers (from the backlog display) or story slugs</action>
    <action>Validate: selection count must be between 3 and 8 (inclusive)</action>

    <check if="fewer than 3 or more than 8 stories selected">
      <output>! Sprint requires 3-8 stories. You selected {{count}}. Adjust your selection.</output>
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

    <action>Log selection:
      `momentum-tools log --agent impetus --event decision --detail "Sprint {{sprint_slug}} — selected {{count}} stories: {{slugs}}" --sprint {{sprint_slug}}`</action>

    <output>Sprint {{sprint_slug}} — {{count}} stories selected:
  {{numbered list of selected story titles}}

Proceeding to flesh out story stubs.</output>
  </step>

  <step n="3" goal="Flesh out stories">
    <action>For each story in {{selected_stories}}, check `story_file` field in stories/index.json</action>

    <check if="story_file is true AND full story content exists">
      <action>Read the story file at `{implementation_artifacts}/stories/{{story_slug}}.md`</action>
      <output>Story {{story_slug}} already has a full story file. Surfacing for review:

[story title, acceptance criteria summary, dev notes summary]

Approve this story as-is, or request revisions?</output>
      <ask>Approve, or revise?</ask>
      <check if="developer requests revisions">
        <action>Note the revision request and spawn `momentum:create-story` with the developer's feedback</action>
        <action>Present the revised story for approval</action>
      </check>
    </check>

    <check if="story_file is false OR story content is a stub">
      <action>Spawn `momentum:create-story` to flesh out the story stub into a full story with:
        · Acceptance criteria (plain English only — no Gherkin)
        · Dev notes
        · Tasks breakdown
      </action>
      <action>Present the fleshed-out story to the developer</action>
      <output>Story {{story_slug}} fleshed out:

[story title, acceptance criteria summary, dev notes summary]

Approve, or request revisions?</output>
      <ask>Approve this story, or revise?</ask>
      <check if="developer rejects and requests revisions">
        <action>Re-spawn `momentum:create-story` with the developer's feedback</action>
        <action>Present the revised story for approval again</action>
      </check>
    </check>

    <action>After each story is approved, log:
      `momentum-tools log --agent impetus --event decision --detail "Story {{story_slug}} approved for sprint {{sprint_slug}}" --sprint {{sprint_slug}}`</action>

    <action>After all stories are approved:</action>
    <output>All {{count}} stories approved. Proceeding to Gherkin spec generation.</output>
  </step>

  <step n="4" goal="Generate Gherkin specs">
    <action>Create the sprint specs directory:
      `{implementation_artifacts}/sprints/{{sprint_slug}}/specs/`</action>

    <action>For each approved story in {{selected_stories}}:</action>
    <action>Read the story's acceptance criteria from its story file — read ALL ACs
      holistically to understand the system's intended behavior, then write Gherkin
      scenarios that describe that behavior end-to-end.</action>
    <action>Read `skills/momentum/references/gherkin-template.md` for the required format,
      voice, tense, naming, and structure rules. All generated `.feature` files must
      follow this template exactly.</action>
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
    <action>Write the spec to: `{implementation_artifacts}/sprints/{{sprint_slug}}/specs/{{story_slug}}.feature`</action>

    <action>Do NOT modify the story markdown file — story files retain plain English ACs only</action>

    <action>Log each spec generation:
      `momentum-tools log --agent impetus --event decision --detail "Gherkin spec generated for {{story_slug}}: N scenarios" --sprint {{sprint_slug}}`</action>

    <output>Gherkin specs generated:
  {{for each story: · story_slug — N scenarios}}

Specs written to sprints/{{sprint_slug}}/specs/. These are for verifier agents only — dev agents will not see them.

Proceeding to spec impact analysis.</output>
  </step>

  <step n="4.5" goal="Spec impact analysis — update architecture and PRD">
    <action>Spawn two parallel discovery subagents:

    **Architecture discovery agent:**
      Read `{planning_artifacts}/architecture.md` and all approved story files.
      For each story, identify:
        · New architecture decisions introduced (patterns, protocols, storage, deployment)
        · Changes to existing decisions (modified constraints, new options)
        · New components, data flows, or integration points
      Return a structured list: [{story_slug, decision_type, summary, section_affected}]

    **PRD discovery agent:**
      Read `{planning_artifacts}/prd.md` and all approved story files.
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
      <output>✓ No spec impact detected — architecture and PRD already cover this sprint's scope.</output>
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
        Read `{planning_artifacts}/architecture.md`.
        Apply each architecture impact item:
          · NEW decisions: add to the appropriate section following existing format
          · MODIFIED decisions: update the existing section in place
        Write the updated file. Follow existing document style and conventions.

      **PRD update agent:**
        Read `{planning_artifacts}/prd.md`.
        Apply each PRD impact item:
          · NEW FRs: assign next available FR number, add to appropriate section
          · MODIFIED FRs: update existing FR text in place
        Write the updated file. Follow existing document style and conventions.
      </action>

      <action>Log spec updates:
        `momentum-tools log --agent impetus --event decision --detail "Spec impact: {{count}} items updated ({{arch_count}} arch, {{prd_count}} PRD)" --sprint {{sprint_slug}}`</action>

      <output>✓ Specs updated:
  · Architecture: {{arch_count}} items
  · PRD: {{prd_count}} items

Proceeding to team composition.</output>
    </check>
  </step>

  <step n="5" goal="Build team composition and execution plan">
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
        1. Log: `momentum-tools log --agent impetus --event decision --detail "Generating guidelines for {{domain}}" --sprint {{sprint_slug}}`
        2. Invoke `momentum:agent-guidelines` with the missing domain as context
        3. Wait for the skill to complete (interactive — developer goes through the consultation workflow)
        4. Re-check `.claude/rules/` for the domain's candidate filenames
        5. If guidelines now exist: set guidelines_status = "present" for affected stories
        6. If still missing (generation was cancelled or failed): fall back to Proceed behavior

      For domains where developer chose **(P) Proceed**:
        1. Keep the specialist assignment unchanged
        2. Set guidelines_status = "missing" for affected stories
        3. Log: `momentum-tools log --agent impetus --event decision --detail "Proceeding without guidelines for {{domain}}" --sprint {{sprint_slug}}`

      For domains where developer chose **(D) Downgrade**:
        1. Replace the specialist with the base Dev agent for all affected stories
        2. Set guidelines_status = "skipped" for affected stories
        3. Log: `momentum-tools log --agent impetus --event decision --detail "Downgraded {{domain}} specialist to base Dev for: {{affected_slugs}}" --sprint {{sprint_slug}}`
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

    <action>Log team composition:
      `momentum-tools log --agent impetus --event decision --detail "Team composition: {{roles_list}}. Execution waves: {{wave_count}}" --sprint {{sprint_slug}}`</action>

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
  </step>

  <step n="6" goal="AVFL validation of complete sprint plan">
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
      <output>✓ AVFL validation passed — sprint plan is coherent.</output>
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

    <action>Log AVFL result:
      `momentum-tools log --agent impetus --event decision --detail "AVFL {{avfl_result}} for sprint {{sprint_slug}}" --sprint {{sprint_slug}}`</action>
  </step>

  <step n="7" goal="Developer review of complete sprint plan">
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

Gherkin Specs: {{spec_count}} feature files in sprints/{{sprint_slug}}/specs/

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
      <action>Log approval:
        `momentum-tools log --agent impetus --event decision --detail "Sprint {{sprint_slug}} approved by developer" --sprint {{sprint_slug}}`</action>
      <action>Proceed to Step 8</action>
    </check>
  </step>

  <step n="8" goal="Activate the sprint">
    <action>Store team composition, guidelines status, and dependency graph in the sprint record:
      · Update `{implementation_artifacts}/sprints/index.json` planning section with:
        - slug: {{sprint_slug}}
        - team: {{team_composition object — roles with story assignments, specialist types, and guidelines}}
          Each story_assignment entry includes: role, specialist, guidelines path, and guidelines_status ("present", "missing", "skipped", or "n/a")
        - waves: {{already stored via momentum-tools}}
        - planned: today's date (YYYY-MM-DD)
    </action>

    <action>Mark planning sprint as ready:
      `momentum-tools sprint ready`</action>

    <action>Activate the sprint:
      `momentum-tools sprint activate`</action>

    <action>Log activation:
      `momentum-tools log --agent impetus --event decision --detail "Sprint {{sprint_slug}} activated" --sprint {{sprint_slug}}`</action>

    <output>✓ Sprint {{sprint_slug}} activated.

  Stories: {{count}}
  Waves: {{wave_count}}
  Team: {{role_list}}
  Started: {{today}}

The sprint is live. Use "Continue sprint" from the session menu to begin execution.</output>
  </step>

</workflow>
