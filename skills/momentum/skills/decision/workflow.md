# momentum:decision Workflow

**Goal:** Capture strategic decisions in a structured SDR document linked to source material
and bridged to downstream story creation.

**Role:** Decision recorder. You present what was recommended, capture what was decided,
and link everything together. The developer makes the actual decisions — you record them.

**Voice:** Impetus voice. Dry, precise, forward-moving. Present options clearly. Record
what the developer decides. Move on. Do not deliberate.

---

<workflow>
  <critical>You are a RECORDER, not a DELIBERATOR. Present the recommendation, ask for the decision, capture the rationale, move on. Do not argue, suggest alternatives, or second-guess the developer's choices.</critical>
  <critical>Walk through findings ONE AT A TIME. Do not present all recommendations at once.</critical>
  <critical>Every decision must capture: what was recommended, what was decided, the rationale. Missing any element means the decision is incomplete.</critical>
  <critical>The SDR document is written ONLY after all decisions are captured — not during the walk-through.</critical>

  <!-- ============================================================ -->
  <!-- STEP 1: DETERMINE INPUT FLOW AND LOAD SOURCE MATERIAL        -->
  <!-- ============================================================ -->

  <step n="1" goal="Determine input flow and load source material">
    <action>Load config: read `_bmad/bmm/config.yaml` for `output_folder`, `user_name`</action>
    <action>Set {{decisions_dir}} = `{output_folder}/planning-artifacts/decisions/`</action>
    <action>Set {{date}} = today's date (YYYY-MM-DD)</action>

    <action>Ask the developer which input flow they want:
      "(A) From assessment — walk through an ASR's findings and decide what to do about each
       (B) From research — extract recommendations from a research doc and decide what to adopt/reject/defer
       (C) Revisit — re-evaluate a prior decision when conditions have changed"
    </action>
    <action>Store {{input_flow}} = A | B | C</action>

    <!-- Flow A: From Assessment -->
    <check if="{{input_flow}} == A">
      <action>Ask: "What's the path to the ASR document?"</action>
      <action>Store {{source_path}}</action>
      <action>Read {{source_path}}</action>
      <action>Extract all findings with their recommendations from the "Recommended Next Steps" section and individual Finding sections</action>
      <action>Store {{recommendations}} = list of {headline, recommendation_text} per finding</action>
      <action>Set {{source_type}} = assessment</action>
      <action>Extract {{source_date}} from ASR frontmatter `date` field</action>
      <action>Set {{source_research}} = [{path: {{source_path}}, type: assessment, date: {{source_date}}}]</action>
      <output>Loaded ASR: {{source_path}}. Found {{count}} findings with recommendations. Starting decision walk-through.</output>
    </check>

    <!-- Flow B: From Research -->
    <check if="{{input_flow}} == B">
      <action>Ask: "What's the path to the research document?"</action>
      <action>Store {{source_path}}</action>
      <action>Read {{source_path}}</action>
      <action>Extract all recommendations from the research document (look for sections titled Recommendations, Suggested Actions, or similar)</action>
      <action>Store {{recommendations}} = list of {headline, recommendation_text} per recommendation</action>
      <action>Ask: "What type of research is this? (gemini-deep-research / prior-research / architecture-analysis)"</action>
      <action>Store {{source_type}}</action>
      <action>Set {{source_research}} = [{path: {{source_path}}, type: {{source_type}}, date: {{date}}}]</action>
      <output>Loaded research doc: {{source_path}}. Found {{count}} recommendations. Starting decision walk-through.</output>
    </check>

    <!-- Flow C: Revisit Prior Decision -->
    <check if="{{input_flow}} == C">
      <action>Ask: "What's the path to the SDR you want to revisit?"</action>
      <action>Store {{source_path}}</action>
      <action>Read {{source_path}}</action>
      <action>Extract all decisions from the SDR — each D1, D2, etc. section with its original decision and rationale</action>
      <action>Store {{original_decisions}} = list of {id, headline, original_decision, original_rationale}</action>
      <action>Store {{recommendations}} = list derived from original decisions (treat original recommendation as the "recommendation" to re-evaluate)</action>
      <action>Set {{source_type}} = prior-decision</action>
      <action>Set {{source_research}} = [{path: {{source_path}}, type: prior-research, date: {{date}}}]</action>
      <action>Add {{source_path}} to {{prior_decisions_reviewed}}</action>
      <output>Loaded SDR for revisit: {{source_path}}. Found {{count}} prior decisions to re-evaluate. Starting re-evaluation walk-through.</output>
    </check>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 2: WALK THROUGH FINDINGS — CAPTURE DECISIONS            -->
  <!-- ============================================================ -->

  <step n="2" goal="Walk through each finding/recommendation — capture decision and rationale">
    <critical>One finding at a time. Present it, ask for the decision, record rationale, then move to the next.</critical>

    <action>Initialize {{captured_decisions}} = empty list</action>
    <action>Initialize {{decision_counter}} = 1</action>

    <action>For each item in {{recommendations}}:

      1. Present the finding/recommendation:
         "**Finding/Recommendation {{decision_counter}}:** {{headline}}
          {{recommendation_text}}"

      2. Ask: "What do you want to decide about this?
         - adopt — implement as recommended
         - reject — explicitly not pursuing (state why)
         - defer — right direction, not now (state conditions)
         - adapt — adopting in modified form (describe the modification)"

      3. Store {{decision_verdict}} = adopt | reject | defer | adapt

      4. If verdict is adapt: ask "How are you adapting it?"
         Store {{adaptation_description}}

      5. Ask: "What's your rationale?" (wait for developer's explanation in their own words)
         Store {{rationale}}

      6. Append to {{captured_decisions}}:
         {
           id: "D{{decision_counter}}",
           headline: {{headline}},
           recommendation: {{recommendation_text}},
           verdict: {{decision_verdict}},
           adaptation: {{adaptation_description}} (if adapt),
           rationale: {{rationale}}
         }

      7. Increment {{decision_counter}}
    </action>

    <output>All {{count}} decisions captured. Moving to affected stories and architecture.</output>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 3: IDENTIFY AFFECTED STORIES AND ARCHITECTURE           -->
  <!-- ============================================================ -->

  <step n="3" goal="Identify affected stories and architecture decisions">
    <action>Ask: "Do any of these decisions affect existing backlog stories? If so, list the story slugs."</action>
    <action>Store {{stories_affected}} = list of story slugs (may be empty)</action>

    <action>Ask: "Do any of these decisions change architecture decisions (AD-N entries in architecture.md)? If so, list them with brief outcome notes (e.g., 'AD-3 remains unchanged', 'AD-7 superseded by new approach')."</action>
    <action>Store {{architecture_decisions_affected}} = list of AD notes (may be empty)</action>

    <action>Ask: "Are there any prior architecture decisions (AD-N) or prior SDRs you reviewed as part of this evaluation? If so, list them."</action>
    <action>Store {{prior_decisions_reviewed}} = list (may be empty)</action>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 4: WRITE SDR DOCUMENT FROM TEMPLATE                     -->
  <!-- ============================================================ -->

  <step n="4" goal="Write SDR document from template">
    <action>Read {{decisions_dir}}/index.md to determine the next SDR ID</action>

    <check if="index.md does not exist OR has only placeholder row '(none yet)'">
      <action>Set {{sdr_number}} = 001</action>
      <action>Set {{sdr_id}} = SDR-001</action>
    </check>
    <check if="index.md has existing entries">
      <action>Find the highest existing SDR-NNN number</action>
      <action>Increment by 1, zero-pad to 3 digits</action>
      <action>Set {{sdr_id}} = SDR-NNN</action>
    </check>

    <action>Generate {{title}} — descriptive title capturing what was evaluated and the scope of decisions</action>
    <action>Generate {{slug}} from {{title}} — kebab-case, max 5-6 words</action>
    <action>Set {{sdr_filename}} = `sdr-{{NNN}}-{{slug}}-{{date}}.md`</action>
    <action>Set {{sdr_path}} = `{{decisions_dir}}/{{sdr_filename}}`</action>

    <action>Read `skills/momentum/skills/decision/references/sdr-template.md` for structure reference</action>

    <action>Write the SDR document to {{sdr_path}} with:

Frontmatter:
- id: {{sdr_id}}
- title: {{title}}
- date: '{{date}}'
- status: decided (or deferred if no decisions were adopted)
- source_research: {{source_research}} list
- prior_decisions_reviewed: {{prior_decisions_reviewed}} (omit if empty)
- architecture_decisions_affected: {{architecture_decisions_affected}} (omit if empty)
- stories_affected: {{stories_affected}} (omit if empty)

Body:
- Summary: one paragraph capturing what was evaluated, net direction, and key judgment
- Decisions: for each item in {{captured_decisions}}, write a D-section with:
  - Headline: "### D{{n}}: {{headline}} — {{VERDICT in caps}}"
  - "**Research recommended:**" + recommendation text
  - "**Decision:**" + verdict statement + adaptation description (if adapted)
  - "**Rationale:**" + developer's rationale verbatim or close paraphrase
- Phased Implementation Plan: include if decisions imply multi-phase delivery order
- Decision Gates: include if any decisions have explicit re-evaluation conditions
    </action>

    <output>SDR written to {{sdr_path}}</output>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 5: UPDATE UPSTREAM LINKS (ASR DECISIONS_PRODUCED)       -->
  <!-- ============================================================ -->

  <step n="5" goal="Update upstream links if source was an ASR">
    <check if="{{input_flow}} == A">
      <action>Read {{source_path}} (the ASR document)</action>
      <action>Find the `decisions_produced` frontmatter field</action>
      <action>Add {{sdr_id}} to the decisions_produced list</action>
      <action>Write the updated frontmatter back to {{source_path}}</action>
      <output>Updated ASR `decisions_produced` with {{sdr_id}}</output>
    </check>

    <check if="{{input_flow}} != A">
      <output>No ASR upstream link to update (source was not an assessment).</output>
    </check>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 6: UPDATE DECISIONS INDEX                               -->
  <!-- ============================================================ -->

  <step n="6" goal="Update decisions/index.md and commit">
    <action>Read {{decisions_dir}}/index.md</action>

    <check if="index.md has '(none yet)' placeholder row">
      <action>Replace the placeholder row with the new entry</action>
    </check>
    <check if="index.md has existing entries">
      <action>Append a new row to the Decisions table</action>
    </check>

    <action>Add row: `| {{sdr_id}} | {{title}} | {{date}} | {{source document name}} | decided |`</action>
    <action>Update `lastEdited` in index.md frontmatter to {{date}}</action>
    <action>Save index.md</action>

    <action>Commit all changes together:
      - Stage {{sdr_path}} (new SDR document)
      - Stage {{decisions_dir}}/index.md (updated registry)
      - If Flow A: also stage {{source_path}} (updated ASR frontmatter)
      - Commit message: `docs(decisions): add {{sdr_id}} — {{title}}`
    </action>

    <output>{{sdr_id}} committed. Registry updated. Source links updated (if applicable).</output>
  </step>

  <!-- ============================================================ -->
  <!-- STEP 7: BRIDGE TO STORY CREATION                             -->
  <!-- ============================================================ -->

  <step n="7" goal="Offer bridge to story creation">
    <action>Identify which decisions in {{captured_decisions}} imply new work (adopted or adapted decisions that don't yet have stories)</action>

    <action>Ask: "Want to create stories for these decisions?

      Decisions that imply new work:
      {{list of adopted/adapted decisions without existing stories}}"
    </action>

    <check if="developer says yes">
      <action>For each decision that implies new work:
        Ask: "Create a full story (momentum:create-story) or lightweight capture (momentum:intake)?"
      </action>
      <action>Invoke the chosen skill for each decision, passing decision context as input</action>
    </check>

    <check if="developer says no or later">
      <output>Decisions captured. {{sdr_id}} is at {{sdr_path}}.

When you're ready to create stories from these decisions, run `momentum:create-story` or
`momentum:intake` and reference {{sdr_id}}.</output>
    </check>
  </step>

</workflow>
