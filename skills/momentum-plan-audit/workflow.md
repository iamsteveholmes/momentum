# momentum-plan-audit Workflow

**Goal:** Audit the active plan for spec impact, classify it as trivial or substantive, create a process story for substantive plans, run a targeted spec audit and AVFL checkpoint, then write the `## Spec Impact` section to unblock `ExitPlanMode`.

**Role:** Plan audit orchestrator for the Momentum project.

---

## INITIALIZATION

Load `./references/spec-capture-guide.md` for classification signals, process story schema, and sprint resolution.

---

## EXECUTION

<workflow>
  <critical>Trivial plans and user-skipped plans skip Steps 3, 4, and 5 entirely — no spec reads, no story creation, no AVFL.</critical>
  <critical>Do not read full spec files. Read only the sections the plan actually touches.</critical>
  <critical>Write ## Spec Impact to the plan file before completing — this is what unblocks ExitPlanMode.</critical>

  <step n="1" goal="Load active plan">
    <action>Find the most recently modified plan file:
      `stat -f "%m %N" ~/.claude/plans/*.md 2>/dev/null | sort -rn | head -1 | awk '{print $2}'`
    </action>
    <action>Store {{plan_file}} = the path returned. If empty (no plan files found), output "No active plan found in ~/.claude/plans/. Nothing to audit." and HALT.</action>
    <action>Read full content of {{plan_file}}. Store as {{plan_content}}.</action>
    <action>Extract {{plan_title}} from the first H1 heading (`# Plan: ...` or just `# ...`).</action>
    <action>Load `{project-root}/_bmad/bmm/config.yaml` → read the `planning_artifacts` key and store as `{{spec_dir}}` (e.g., `_bmad-output/planning-artifacts`).</action>
  </step>

  <step n="2" goal="Classify plan as trivial or substantive">
    <action>Read ./references/spec-capture-guide.md Section 1 (Trivial vs. Substantive Classification).</action>
    <action>Analyze {{plan_content}} against the classification signals:
      - Trivial: plan ONLY reads files, searches, queries, or analyzes — no writes, no file creation, no behavior changes
      - Substantive: creates or modifies files, introduces new capability, changes behavior, makes architectural decisions
      - When in doubt: substantive
    </action>
    <action>Store {{classification}} = "trivial" or "substantive".</action>
    <action>Store {{classification_reason}} = one sentence explaining the key signal that determined the classification.</action>

    <output>Classification: {{classification}} — {{classification_reason}}</output>

    <check if="{{classification}} == trivial">
      <action>Skip to Step 6.</action>
    </check>

    <check if="{{classification}} == substantive">
      <action>Summarize what makes this plan substantive in one sentence. Identify the key signals: files created/modified, new capabilities introduced, behavior changes.</action>
      <ask>This plan is substantive — {{classification_reason}}

Proceeding will:
  1. Create a process story capturing this plan's work
  2. Audit relevant spec sections for consistency
  3. Run an AVFL checkpoint on the plan and story

Proceed with full audit, or skip? (Skip writes a minimal Spec Impact and unblocks ExitPlanMode.)</ask>
      <check if="user chooses skip">
        <action>Store {{classification}} = "skipped"</action>
        <action>Skip to Step 6.</action>
      </check>
    </check>
  </step>

  <step n="3" goal="Create process story (substantive only)">
    <action>Determine {{sprint_num}} using spec-capture-guide.md Section 4 (Sprint Number Resolution).</action>
    <action>Read `{implementation_artifacts}/stories/index.json`. Scan story slugs for entries with `epic_slug == "process-stories"`. Count existing process stories to determine the next sequence number. Set {{process_story_seq}} = count+1. If no matches, use 1.</action>
    <action>Derive {{process_story_key}} = `{{plan_title_kebab}}` where {{plan_title_kebab}} is the plan title converted to kebab-case.</action>
    <action>Store {{process_story_file}} = `{implementation_artifacts}/{{process_story_key}}.md`.</action>
    <action>Extract {{touches}} from the plan's Files to Create/Modify table — collect unique directory/file paths (normalize to directory paths where possible).</action>
    <action>Compose the process story content using spec-capture-guide.md Section 5:
      - Frontmatter with explicit field names: `type: process`, `epic: P{{sprint_num}} — Process Sprint-{{sprint_num}}`, `title: {{plan_title}}`, `sprint: {{sprint_num}}`
      - User Story derived from plan Context
      - Background from plan Context
      - Acceptance Criteria from plan's Verification section (or derived from execution steps if no Verification section)
      - Definition of Done from plan's Files to Create/Modify table
      - Dev Notes with change type classification
    </action>
    <action>Write story content to {{process_story_file}}.</action>
    <action>Read {{process_story_file}} to confirm it was written correctly.</action>
    <action>Read `{implementation_artifacts}/stories/index.json`. Add entry keyed by {{process_story_key}} with:
      - status: "ready-for-dev"
      - title: {{plan_title}}
      - epic_slug: "process-stories"
      - story_file: true
      - depends_on: []
      - touches: {{touches}}
    </action>
    <action>Save stories/index.json, preserving ALL existing entries.</action>
    <action>Identify any upstream spec files that need updating per spec-capture-guide.md Section 7. Store {{upstream_updates}} = list of recommended changes (file + section + reason), or "None identified." if none.</action>

    <output>Process story created: {{process_story_file}} (sprint-status.yaml updated: development_status + momentum_metadata)</output>
  </step>

  <step n="4" goal="Targeted upstream spec audit (substantive only)">
    <action>Using spec-capture-guide.md Section 8, identify which spec sections are relevant to this plan's changes. Use keywords from the plan's file list and hook/skill types to grep architecture.md and epics.md for relevant sections.</action>
    <action>Read ONLY the identified sections — not full spec files. Skip any spec file with no relevant sections.</action>
    <action>Store {{spec_sections_read}} = list of "filename: section name" for each section read.</action>
    <action>For each section read, identify: contradictions with the plan, extensions the plan makes, or ambiguities the plan resolves. Store {{spec_findings}} = plain-language summary, or "No contradictions or extensions found." if clean.</action>

    <output>Spec sections audited: {{spec_sections_read}}</output>
  </step>

  <step n="5" goal="AVFL checkpoint — single combined pass (substantive only)">
    <action>Read the full content of {{process_story_file}}.</action>
    <action>Invoke the `avfl` skill with these parameters:
      - domain_expert: "solution architect"
      - task_context: "Plan audit + process story — {{plan_title}}"
      - output_to_validate: |
          === PLAN ===
          {{plan_content}}

          === PROCESS STORY ===
          [full content of {{process_story_file}}]
      - source_material: [combined text of all sections from {{spec_sections_read}}]
      - profile: checkpoint
      - stage: checkpoint

      Note on stage: `checkpoint` is correct here — the plan+story are mid-workflow planning artifacts (implementation not started). `final` would penalize for absent implementation details.
      Note on source_material: spec sections are ground truth for plan-stage validation. The plan IS the output being checked against specs.
    </action>

    <check if="AVFL returns CLEAN">
      <action>Store {{avfl_result}} = "CLEAN"</action>
      <action>Store {{avfl_findings}} = ""</action>
    </check>

    <check if="AVFL returns CHECKPOINT_WARNING">
      <action>Store {{avfl_result}} = "CHECKPOINT_WARNING"</action>
      <action>Synthesize findings in plain language — `!` for critical/high, `·` for medium/low. Do NOT dump raw JSON.</action>
      <action>Store {{avfl_findings}} = synthesized findings</action>
    </check>

    <check if="AVFL returns GATE_FAILED or unexpected status">
      <action>Store {{avfl_result}} = "GATE_FAILED" (or the unexpected status)</action>
      <action>Store {{avfl_findings}} = synthesized findings</action>
    </check>
  </step>

  <step n="6" goal="Write ## Spec Impact section to plan file">
    <check if="{{classification}} == skipped">
      <action>Append to {{plan_file}}:

```markdown

---

## Spec Impact

**Classification:** skipped
**Reason:** User declined audit.

**Go/No-Go:** Proceed (audit skipped).
```
      </action>
    </check>

    <check if="{{classification}} == trivial">
      <action>Append to {{plan_file}}:

```markdown

---

## Spec Impact

**Classification:** trivial
**Reason:** {{classification_reason}}

No spec updates required. Plan involves read-only operations only.

**Go/No-Go:** Proceed.
```
      </action>
    </check>

    <check if="{{classification}} == substantive">
      <action>Determine Go/No-Go:
        - If AVFL CLEAN: Go/No-Go = "Proceed."
        - If AVFL CHECKPOINT_WARNING with no critical findings: Go/No-Go = "Proceed with known issues: [list findings]."
        - If AVFL CHECKPOINT_WARNING with critical findings: Go/No-Go = "Address findings before proceeding: [list critical findings]."
        - If AVFL GATE_FAILED: Go/No-Go = "BLOCKED — AVFL gate failed. Address all findings before proceeding."
        - If AVFL not run (unexpected): Go/No-Go = "Proceed with caution — AVFL result unavailable."
      </action>
      <action>Append to {{plan_file}}:

```markdown

---

## Spec Impact

**Classification:** substantive
**Reason:** {{classification_reason}}

### Spec Capture

Process story `{{process_story_key}}` created: `{{process_story_file}}`

### Upstream Spec Updates Recommended

{{upstream_updates}}

### Upstream Spec Audit Findings

{{spec_findings}}

### AVFL Checkpoint

{{avfl_result}}
{{avfl_findings}}

### Go/No-Go

{{go_no_go}}

### Story Status Lifecycle

This plan's process story (`{{process_story_key}}`) requires these status transitions during execution:

1. **Before first implementation step:** `bash $CLAUDE_PROJECT_DIR/skills/momentum/scripts/update-story-status.sh {{process_story_key}} in-progress`
2. **After implementation complete, before AVFL:** `bash $CLAUDE_PROJECT_DIR/skills/momentum/scripts/update-story-status.sh {{process_story_key}} review`
3. **After AVFL passes:** `bash $CLAUDE_PROJECT_DIR/skills/momentum/scripts/update-story-status.sh {{process_story_key}} done`
```
      </action>
    </check>

    <output>## Spec Impact section written to {{plan_file}}. ExitPlanMode is now unblocked.</output>
  </step>

  <step n="7" goal="Completion signal">
    <check if="{{classification}} == substantive AND AVFL findings contain critical severity">
      <ask>AVFL found critical issues in the plan or process story. Review above findings. Proceed to implementation, or address findings first?</ask>
    </check>

    <output>momentum-plan-audit complete.

Plan: {{plan_file}}
Classification: {{classification}}</output>

    <check if="{{classification}} == substantive">
      <output>Process story: {{process_story_file}}
AVFL: {{avfl_result}}</output>
    </check>

    <check if="{{classification}} == skipped">
      <output>Audit skipped by user. Spec Impact written with skipped marker.</output>
    </check>

    <output>
ExitPlanMode is unblocked — ## Spec Impact section is present.</output>
  </step>

</workflow>
