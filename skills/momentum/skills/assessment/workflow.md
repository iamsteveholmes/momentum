# momentum:assessment Workflow

**Goal:** Produce a structured Assessment Record (ASR) — a point-in-time snapshot of
product state that bridges research and decisions.

**Role:** Assessment orchestrator. You guide and discover; the developer validates.
Discovery happens in subagents. You present, ask, and confirm — you do not write
findings until the developer says they're accurate.

**Voice:** Dry, factual, forward-moving. Present findings. Do not editorialize. Let
the developer draw conclusions. Ask targeted questions to sharpen the picture.

---

<workflow>
  <critical>Findings are NOT written to the ASR until the developer explicitly confirms them. Every major finding gets a checkpoint: "Does this match your understanding?"</critical>
  <critical>Scoping happens before discovery. Do NOT spawn agents until scope and agent roster are agreed with the developer.</critical>
  <critical>Discovery happens in subagents. Do not accumulate raw audit findings in the orchestrator's context.</critical>
  <critical>This is a COLLABORATIVE skill — the developer drives the scope, challenges findings, and approves next steps. You guide; you do not decide.</critical>

  <!-- ============================================================ -->
  <!-- STEP 1: SCOPE                                                -->
  <!-- ============================================================ -->

  <step n="1" goal="Collaborative scoping — agree what to assess and how">
    <action>Load config: read `_bmad/bmm/config.yaml` for `output_folder`, `user_name`</action>
    <action>Set {{assessments_dir}} = `{output_folder}/planning-artifacts/assessments/`</action>
    <action>Set {{date}} = today's date (YYYY-MM-DD)</action>

    <action>Ask the developer:
      "What do you want to assess? Options: full product state, a specific epic,
      a user journey, a specific concern, or something else.
      What questions should this assessment answer?"
    </action>
    <action>Store {{scope_description}} from developer response</action>
    <action>Store {{assessment_questions}} — the questions this assessment should answer</action>

    <action>Based on {{scope_description}}, propose a discovery agent roster. For each proposed agent, describe:
      - What it will audit (which repo, directory, or artifact)
      - What question it will answer
    </action>

    <action>Present the proposed roster and ask:
      "Does this agent roster match what you want to investigate?
      Anything to add, drop, or adjust?"
    </action>
    <action>Incorporate feedback and store {{agreed_agents}} — final list of agents with their audit scope</action>

    <output>Scope confirmed. {{count}} discovery agents will run in parallel. Starting discovery.</output>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 2: PARALLEL DISCOVERY                                   -->
  <!-- ============================================================ -->

  <step n="2" goal="Spawn parallel discovery agents per agreed scope">
    <critical>Launch ALL agents in a SINGLE message for maximum parallelism. Use the Agent tool with run_in_background: true for each agent.</critical>
    <critical>Each agent audits ACTUAL codebase/artifact state — not documentation claims. Evidence means file paths, LOC counts, and status assessments.</critical>

    <action>For each agent in {{agreed_agents}}, spawn a background subagent with a briefing that includes:
      - What to audit (specific repo paths, directories, or artifact types)
      - What questions to answer
      - Evidence format: use tables with Component | Status (Real/Stub/Missing/Broken) | Evidence (file path, LOC)
      - Output format: numbered findings with evidence tables and 2-4 sentence narrative each
      - Date: {{date}}
    </action>

    <action>Wait for all background agents to complete</action>
    <action>Collect all agent findings into {{raw_findings}} — one entry per agent</action>

    <output>Discovery complete. {{count}} agents returned findings. Moving to validation.</output>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 3: FINDINGS VALIDATION                                  -->
  <!-- ============================================================ -->

  <step n="3" goal="Present findings section by section — validate each with developer">
    <critical>Present findings ONE AT A TIME. Do not dump all findings at once.</critical>
    <critical>After each finding: ask "Does this match your understanding?" and wait for response.</critical>
    <critical>Do NOT move a finding into the confirmed list until the developer says it's accurate.</critical>

    <action>Organize {{raw_findings}} into logical finding sections — group related agent findings by theme</action>
    <action>Initialize {{confirmed_findings}} = empty list</action>

    <action>For each finding section:
      1. Present the finding clearly — headline, evidence table, brief narrative interpretation
      2. Ask: "Does this match your understanding? Anything to add or correct?"
      3. Wait for developer response
      4. If developer confirms: add to {{confirmed_findings}}
      5. If developer challenges: acknowledge, ask what the reality is, adjust the finding, re-present
      6. If developer wants deeper investigation: note the gap, offer to spawn a focused follow-up agent
      7. Only move on when developer is satisfied with this finding
    </action>

    <output>All findings validated. {{count}} confirmed findings ready for the ASR.</output>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 4: COLLABORATIVE NEXT STEPS                             -->
  <!-- ============================================================ -->

  <step n="4" goal="Collaboratively draft recommended next steps">
    <action>Based on {{confirmed_findings}} and {{assessment_questions}}, propose 3-5 concrete next steps</action>
    <action>Each next step must be: specific (not "consider X"), actionable, and tied to a finding</action>

    <action>Present the proposed next steps and ask:
      "Based on these findings, here are the recommended next steps.
      Does this match what you'd want to do, or should we adjust?"
    </action>
    <action>Incorporate developer feedback</action>
    <action>Ask for explicit approval: "Should I write these next steps into the ASR?"</action>
    <action>Store {{approved_next_steps}} once developer confirms</action>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 5: WRITE ASR DOCUMENT                                   -->
  <!-- ============================================================ -->

  <step n="5" goal="Write the ASR document from template">
    <action>Read {{assessments_dir}}/index.md to determine the next ASR ID (e.g., if last is ASR-002, next is ASR-003)</action>
    <check if="index.md does not exist OR has no entries">
      <action>Set {{asr_id}} = ASR-001</action>
    </check>
    <action>Store {{asr_id}}</action>

    <action>Generate {{title}} — a descriptive title capturing what was assessed and the headline finding</action>
    <action>Generate {{slug}} from {{title}} — kebab-case, max 5-6 words</action>
    <action>Set {{asr_filename}} = `asr-{{NNN}}-{{slug}}-{{date}}.md` (NNN = zero-padded number)</action>
    <action>Set {{asr_path}} = `{{assessments_dir}}/{{asr_filename}}`</action>

    <action>Read `skills/momentum/skills/assessment/references/asr-template.md` for structure reference</action>

    <action>Write the ASR document to {{asr_path}} with:

Frontmatter:
- id: {{asr_id}}
- title: {{title}}
- date: '{{date}}'
- status: current
- method: description of agents spawned (from {{agreed_agents}})
- decisions_produced: []
- supersedes: (omit if not applicable)

Body sections:
- Purpose: what was assessed, what questions it answers, what decisions it informs
- Method: agents spawned, what each audited, developer-provided scope context
- Findings: each {{confirmed_finding}} as a numbered section with headline, evidence table, narrative
- Recommended Next Steps: {{approved_next_steps}} as numbered, bolded, concrete actions
- Raw Data: agent output summaries organized by agent name
    </action>

    <output>ASR written to {{asr_path}}</output>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 6: UPDATE REGISTRY AND COMMIT                           -->
  <!-- ============================================================ -->

  <step n="6" goal="Update assessments/index.md and commit">
    <action>Read {{assessments_dir}}/index.md</action>

    <check if="index.md has '(none yet)' placeholder row">
      <action>Replace the placeholder row with the new entry</action>
    </check>
    <check if="index.md has existing entries">
      <action>Append a new row to the assessments table</action>
    </check>

    <action>Add row: `| {{asr_id}} | {{title}} | {{date}} | [] | current |`</action>
    <action>Update `lastEdited` in index.md frontmatter to {{date}}</action>
    <action>Save index.md</action>

    <action>Commit: `docs(assessments): add {{asr_id}} — {{title}}`</action>
    <action>Stage both {{asr_path}} and {{assessments_dir}}/index.md</action>
    <action>Run the commit</action>

    <output>{{asr_id}} committed. Registry updated.</output>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 7: BRIDGE TO DECISION SKILL                             -->
  <!-- ============================================================ -->

  <step n="7" goal="Offer bridge to decision skill">
    <action>Ask: "These findings are ready to feed into a decision record. Want to capture decisions now?"</action>

    <check if="developer says yes">
      <check if="momentum:decision skill exists">
        <action>Invoke momentum:decision, passing {{asr_path}} as source material</action>
      </check>
      <check if="momentum:decision skill does NOT exist">
        <output>The `momentum:decision` skill doesn't exist yet. When it's available, run it with {{asr_path}} as the source assessment. The ASR frontmatter has a `decisions_produced` field that the decision skill will populate.</output>
      </check>
    </check>

    <check if="developer says no or later">
      <output>Assessment complete. {{asr_id}} is at {{asr_path}}. When you're ready to make decisions from these findings, run `momentum:decision` and reference this ASR.</output>
    </check>
  </step>

</workflow>
