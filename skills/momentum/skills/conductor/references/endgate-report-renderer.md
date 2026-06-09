# End-Gate Report Renderer — Data Contract & Rendering Spec

**Implements:** Phase 5 (step 5) of conductor/workflow.md — the single human end-gate report.
**Governs:** How the Conductor builds the self-contained HTML report it hands the developer at Touchpoint 2.
**Format & Voice authority:** `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md` (the canonical standard; this doc is the conductor-specific wiring contract for that standard).
**Worked example:** `.momentum/handoffs/sprint-2026-06-02-conduct-core-hitl-report.html`
**Reference generator:** `.momentum/gen-endgate-report.py` (one-off; documents structure and CSS tokens)

---

## 1. Input data contract — what step 5 assembles

### 1a. {{end_gate_escalations}} — per-story stakes escalations

Populated by step 2.S3 (the Stage-3 fix loop). Each entry shape:

```
{
  finding_id:     string      — unique finding identifier
  stakes_class:   string      — security-auth-isolation | irreversible-destructive | high-blast-radius-architecture
  timing_tier:    "end-gate-expanded"
  summary:        string      — plain-language description of the finding
  evidence:       string      — concrete evidence (file, line, behavior)
  suggested_fix:  string      — recommended resolution
  story_slug:     string      — which story this came from
}
```

### 1b. {{avfl_findings}} — post-merge AVFL scan results (Phase 3)

Populated by step 3. For the end-gate, the Conductor filters to:
- **Stakes escalations:** entries where `stakes_class != "routine"` AND `disposition == "escalated"` or `disposition == "residual"` with high severity
- **Routine residuals:** entries where `stakes_class == "routine"` AND `disposition == "residual"` (not fixed)
- **Fixed count:** entries where `disposition == "fixed"` — contribute to the auto-fixed count
- **Dismissed with rationale:** entries where `disposition == "dismissed"` — appear in §05 with `dismissal_rationale`

### 1c. {{e2e_results}} — E2E validation report (Phase 4)

Populated by step 4. Shape:
```
{
  scenarios_checked: number
  passed:            number
  failed:            number
  blocked:           number
  failed_scenarios:  [{ name, description, failure_reason }]
  blocked_scenarios: [{ name, description, blocked_reason }]
}
```

### 1d. {{build_log}} — per-story pipeline events

Used to derive:
- **Stories built:** count of stories successfully merged (event == "stage4-merge-complete")
- **Blocked/quarantined stories:** stories with outcome == "quarantined" or disposition == "blocked"
- **Per-story diffs and summaries:** derive from story slugs + their touches arrays

---

## 2. Assembly — binding {{stakes_findings}} and the report data model

At the top of step 5, before rendering, bind:

```
{{stakes_findings}} = concat(
  {{end_gate_escalations}},                                    -- per-story fix-loop escalations
  {{avfl_findings}} filtered to { stakes_class != "routine" AND disposition in { "escalated", "residual" } },
  {{e2e_results}}.failed_scenarios filtered to { failure_reason indicates a stakes-class behavioral gap }
)
```

Each entry in {{stakes_findings}} must carry: `finding_id`, `stakes_class`, `summary`, `evidence`, `suggested_fix`.

Bind supporting report variables:
```
{{routine_auto_fixed_count}}  = count of findings with disposition == "fixed" across all sources
{{dismissed_findings}}        = findings with disposition == "dismissed" — each must carry dismissal_rationale
{{blocked_stories}}           = stories from {{build_log}} that never reached stage-4 merge
{{quarantined_stories}}       = stories with outcome == "quarantined" in {{build_log}}
{{contract_integrity_stops}}  = from Conductor in-memory state (step 2.2 integrity-check path)
{{mid_flight_escalations}}    = escalations already raised to the developer during the build (informational); sourced from {{escalations}} Conductor-scoped accumulator
{{stories_built_count}}       = count of stories in {{merged}}
{{high_risk_divergences}}     = per-story finding records where disposition == "fixed" AND severity in {blocker, critical, major} (auto-fixed consequential divergences caught during review); rendered in §03. Each entry shape: { finding_id, severity, summary, evidence, story_slug }
{{undischarged_deferrals}}    = entries from {{avfl_findings}} where source == "coverage-discharge-consumer" AND disposition == "residual" AND stakes_class == "routine" (deferred stories whose named integration scenario could not be verified); rendered in §05. Each entry shape: { slug, scenario_id, failure_reason }
```

---

## 3. The HTML report — structure and voice

Build a **self-contained single `.html` file** — inline `<style>` and `<script>`, zero external dependencies.
Output it as `.momentum/handoffs/{{sprint_slug}}-endgate-report.html`.
Open it in the cmux viewer pane (right pane, as a browser tab) so the developer can read it immediately.

**Voice:** Assume nothing. Write for someone who did not watch the build and has never heard of conduct, sprint-dev, or the internal decision names. Define every term inline on first use. Never lead a section with a bare code symbol, file path, or ticket id.

**CSS tokens (from the worked example):**
```css
--ivory:#FAF9F5; --slate:#141413; --clay:#D97757; --clay-d:#B85C3E;
--olive:#788C5D; --olive-d:#46552F; --serif:ui-serif,Georgia,serif;
--sans:system-ui,-apple-system,sans-serif; --mono:ui-monospace,Menlo,monospace;
--radius:13px; --fs-scale:1.28;
```

### Section spine (fixed order):

| Anchor | Section | Content |
|--------|---------|---------|
| hero   | Metrics strip | Items built/merged · high-risk divergences caught · decisions for you count · auto-fixed count · waved-off count · shipped-broken/blocked count |
| #what  | §01 What shipped | Before/after in plain terms; concrete new capabilities; one-line completeness caveat pointing to §06 |
| #pieces | §02 What each piece is for | Every story: one plain paragraph (job + guarantee + what breaks without it); "Review this work item" expand per §3 below |
| #risk  | §03 Where it diverged | High-risk divergences told as 5-beat narratives (§4 below), scariest-first, collapsible `<details>` cards; routine excluded |
| #decision | §04 The decision(s) for you | One card per {{stakes_findings}} entry; anti-rubber-stamp gate per §5 below |
| #waved | §05 Waved off & routine | Dismissed findings with rationale; routine remainder as a single count — not itemized |
| #done  | §06 How done is this, really? | Two tables: live vs hollow; explicit "what approving does" callout |
| #merge | §07 Merge & push preview | Commits/diffstat; exact approve sequence; "push is a separate confirmation" |
| gate   | Single gate control | Approve / Request Changes; copy-decision-as-prompt; approve disabled until all §04 cards answered |

---

## 4. Per-item review panel (§02 expand) — testing first

Each §02 story item carries a `<details class="review">` expand labeled "Review this work item". Contents in this order:

1. **How it was verified — TESTING FIRST**
   - What had to be true (the frozen contract's scenarios in plain language)
   - How it was checked (QA + adversarial review + re-check; **be honest about inspection vs execution**)
   - If verification was structured inspection against the contract rather than live execution, say so explicitly — never let "verified" imply "executed"
   - Result: verdict + concrete evidence

2. **Why it's built this way — architectural rationale**
   - Design choice with explicit named references to governing decisions (DEC-035, DEC-036, spec §N) and spec sections
   - Files changed

3. **The actual diff** — embedded in a collapsed `<details class="diffd">`, syntax-highlighted `<pre class="diff">`, escaped and self-contained

4. **Visual evidence** — for any item that changes user-facing UI: before/after screenshots embedded as data-URIs; state explicitly if a UI item has no screenshot (this is a verification gap)

---

## 5. Decision cards (§04) — data contract per card

For each entry E in {{stakes_findings}}, render one `<div class="decision">` card:

```html
<div class="decision" id="d{{index}}">
  <h3>D{{index}} · {{E.plain_headline}}</h3>          <!-- plain language, not a code symbol -->
  <p><strong>In plain terms.</strong> {{E.background_paragraph}}</p>
  <p><strong>What's actually at stake.</strong> {{E.stakes_paragraph}}</p>
  <!-- One .opt div per option, .rec on the recommended option -->
  <div class="opt rec"><b>Option A (recommended).</b> {{E.option_a}}</div>
  <div class="opt"><b>Option B.</b> {{E.option_b}}</div>
  <!-- Add Option C etc. as appropriate -->
  <p><strong>My recommendation:</strong> {{E.recommendation}}</p>
  <div class="ack">
    <label><input type="checkbox" id="ack-d{{index}}" onchange="paint()"> I've read D{{index}} and understand the call.</label>
  </div>
  <div class="choices">
    <!-- One radio per option, name="d{{index}}", no pre-selection -->
    <label onclick="sel(this)"><input type="radio" name="d{{index}}" value="A" onchange="paint()">Option A — recommended</label>
    <label onclick="sel(this)"><input type="radio" name="d{{index}}" value="B" onchange="paint()">Option B</label>
  </div>
</div>
```

**Data enrichment:** `E.plain_headline`, `E.background_paragraph`, `E.stakes_paragraph`, `E.option_a`, `E.option_b`, and `E.recommendation` must be synthesized from `E.summary`, `E.evidence`, `E.suggested_fix`, and the Conductor's knowledge of the sprint context. The raw finding fields alone are not enough — the Conductor must translate them into the assume-nothing voice.

**No pre-selection.** No radio is checked by default. No checkbox is checked by default.

---

## 6. Anti-rubber-stamp gate (§GATE)

```javascript
function paint() {
  var gateChoice = val('gate');   // APPROVE or CHANGES
  var allDecisionsAck = true;
  var allDecisionsPicked = true;

  // For each decision card D1..Dn:
  for (var i = 1; i <= DECISION_COUNT; i++) {
    if (!document.getElementById('ack-d' + i).checked) allDecisionsAck = false;
    if (!val('d' + i)) allDecisionsPicked = false;
  }

  var ok = false, why = '';
  if (gateChoice === 'APPROVE') {
    if (!allDecisionsAck)    why = 'Read each decision and check the acknowledgment box before approving.';
    else if (!allDecisionsPicked) why = 'Pick an option for each decision (A / B / C) before approving.';
    else { ok = true; why = 'Ready to approve — copy the prompt and paste it back.'; }
  } else if (gateChoice === 'CHANGES') {
    var changes = document.getElementById('changes').value.trim();
    if (!changes) why = 'Describe the changes, then copy.';
    else { ok = true; why = 'Ready to request changes.'; }
  } else {
    why = 'Choose Approve or Request changes.';
  }

  document.getElementById('go').disabled = !ok;
  document.getElementById('why').textContent = why;
}
```

**When DECISION_COUNT == 0** (clean sprint with no escalations): `paint()` skips the decision-card checks entirely; the gate's approve path enables once the developer selects "Approve & finish". No forcing function is applied to a clean build.

---

## 7. 5-beat divergence narrative format (§03 cards)

Each high-risk divergence `<details class="risk">` card carries flowing prose with bold lead-ins:

1. **What this part of conduct does** — plain.
2. **Why we wrote a guarantee around it, and why that way** — the risk that shaped the contract (not a quote of the eval; the intent behind it).
3. **Where reality diverged** — what the build got wrong, plainly.
4. **The risk that created, and what catching it removed** — the observable consequence had it shipped.
5. **Why the outcome is acceptable** — the resolved behavior matches the guarantee; it was re-verified.

Plain-language headline (the risk in human terms) as the `<summary>` so the developer can scan and triage.

---

## 8. File output

```
.momentum/handoffs/{{sprint_slug}}-endgate-report.html
```

After writing, open in the cmux Browser viewer pane:
```bash
cmux browser new "file:///$(pwd)/.momentum/handoffs/{{sprint_slug}}-endgate-report.html" \
  --workspace "$CMUX_WORKSPACE_ID" --focus false
```
(Adds a tab to the existing viewer pane; does not create a new structural pane.)

---

## 9. Honesty / completeness section (§06)

Two tables:

**What is live and working now** — capabilities that exist and can be relied on.
**What is still hollow** — gaps with plain-language explanation of what each means for the developer.

Followed by a `<div class="callout">` labeled "So what does approving actually do?" that states plainly what merging does and does not turn on.

**Cardinal sin:** A report that reads more finished than the thing is. If the system is a partial slice, say so in §01 and say it in full here.

---

## 10. Routine items — never itemize

The `{{routine_auto_fixed_count}}` count plus one sentence ("N routine problems — wording, consistency, doc-drift, reachability nits — were auto-fixed and are not itemized here") satisfies §05 for routine findings. Itemizing them is the firehose.

Dismissed findings (each with `dismissal_rationale`) appear as a table: `What was flagged` | `Why it was safe to leave`.
