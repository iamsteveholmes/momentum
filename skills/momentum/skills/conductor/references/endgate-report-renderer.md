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
- **Stories built:** count of stories that reached terminal state with `event == "story-terminal" AND outcome == "merged"`
- **Failed/non-shipped stories:** stories with `event == "story-terminal" AND outcome == "failed"`, OR stories absent from any story-terminal row (integrity-stopped, stage3-blocked without terminal row)
- **Per-story diffs and summaries:** derive from story slugs + their touches arrays

### 1e. {{process_findings}} — structured process digest from retro (fused re-render)

Populated by `momentum:retro` Phase 4.5 (not by conduct). Shape: an array of ≤7 entries, each:

```
{
  id:          string    — unique identifier, e.g. "pf-1"
  disposition: string    — "keep" | "stop" | "change"
  what:        string    — plain-language statement of the finding
  why:         string    — why it matters to the practice
  evidence:    string    — observable evidence from the sprint transcript
}
```

**At conduct render time this binding is empty.** It is injected during retro's fused re-render
(Phase 4.5). Conduct's initial render omits §08 (the Process review section); retro extends the
file by adding §08 and updating the gate logic. Routine process findings (beyond the ≤7 cap)
are collapsed to a count line, not itemized.

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
{{blocked_stories}}           = stories from {{build_log}} with event == "story-terminal" AND outcome == "failed",
                                PLUS stories absent from any story-terminal row (integrity-stopped, stage3-blocked);
                                supersession applied (latest row wins per story_slug); {{merged}} slugs excluded
{{quarantined_stories}}       = reserved for post-hoc administrative quarantine (set during Phase 5 approve for
                                stories that require branch preservation); not emitted as a ledger outcome during
                                conduct build — the conduct ledger only writes outcome == "merged" or "failed"
{{contract_integrity_stops}}  = from Conductor in-memory state (step 2.2 integrity-check path)
{{mid_flight_escalations}}    = escalations already raised to the developer during the build (informational); sourced from {{escalations}} Conductor-scoped accumulator
{{stories_built_count}}       = count of stories in {{merged}}
{{high_risk_divergences}}     = per-story finding records where disposition == "fixed" AND severity in {critical, major} (auto-fixed consequential divergences caught during review); rendered in §03. Each entry shape: { finding_id, severity, summary, evidence, story_slug }
{{undischarged_deferrals}}    = entries from {{avfl_findings}} where source == "coverage-discharge-consumer" AND disposition == "residual" AND stakes_class == "routine" (deferred stories whose named integration scenario could not be verified); rendered in §05. Each entry shape: { slug, scenario_id, failure_reason }
{{all_sprint_stories}}        = ordered list of all sprint stories as objects {slug, title, outcome} — sourced
                                from sprint index for slug+title; outcome derived by: "merged" if slug in {{merged}},
                                "failed" if slug in {{blocked_stories}}, otherwise "unknown"; used to render §00
```

**Enriched per-non-shipped-story shape (used in §5b force-close cards):**
For each story S in `{{blocked_stories}}`, derive the enriched shape before rendering §5b:
```
{
  slug:           S.story_slug,                          -- from ledger row field story_slug
  title:          (from stories/index.json lookup),      -- human-readable title
  outcome:        S.outcome,                             -- "failed" or "unknown" (from ledger)
  failure_reason: S.note || S.reason || "(no reason recorded in build ledger)"
}
```
Use this enriched shape in §5b templates. `{{S.slug}}` in §5b refers to the enriched `slug` field.

**{{process_findings}} is not assembled here.** It is injected by `momentum:retro` Phase 4.5
when the fused re-render runs. Conduct's initial render omits §08; retro extends the file.

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
--red:#C0392B; --amber:#E67E22; --line:#E2E0D8;
```
`--red` is used for `stop` disposition borders in §08 and `blocked` pill color in §11.
`--amber` is used for `change` disposition borders in §08 and `quarantined`/`warn` pill color in §11.
`--line` is used for row separators in §00 status strip.

### Section spine (fixed order):

| Anchor | Section | Phase | Content |
|--------|---------|-------|---------|
| hero   | Metrics strip | conduct | Items built/merged · high-risk divergences caught · decisions for you count · auto-fixed count · waved-off count · shipped-broken/blocked count |
| #status | **§00 Ship status** (RESULTS-FIRST LEAD) | conduct | Per-story ship outcome block — every sprint story listed with a status pill: `shipped-merged` / `blocked` / `closed-incomplete` / `quarantined`. Sourced from `{{all_sprint_stories}}`, `{{merged}}`, `{{blocked_stories}}`, `{{quarantined_stories}}`. Rendered as a scannable status strip (pills), not prose. **This section leads ahead of §01.** |
| #what  | §01 What shipped | conduct | Before/after in plain terms; concrete new capabilities; one-line completeness caveat pointing to §06 |
| #pieces | §02 What each piece is for | conduct | Every story: one plain paragraph (job + guarantee + what breaks without it); "Review this work item" expand per §4 below |
| #risk  | §03 Where it diverged | conduct | High-risk divergences told as 5-beat narratives (§7 below), scariest-first, collapsible `<details>` cards; routine excluded |
| #decision | §04 The decision(s) for you | conduct | One card per {{stakes_findings}} entry + one force-close-or-investigate card per non-shipped story (see §5b below); anti-rubber-stamp gate per §6 below |
| #waved | §05 Waved off & routine | conduct | Dismissed findings with rationale; routine remainder as a single count — not itemized |
| #done  | §06 How done is this, really? | conduct | Two tables: live vs hollow; explicit "what approving does" callout |
| #merge | §07 Merge & push preview | conduct | Commits/diffstat; exact approve sequence; "push is a separate confirmation" |
| #process | **§08 Process review (Keep / Stop / Change)** | **retro** | `{{process_findings}}` ≤7 entries organized by disposition (Stop → Change → Keep order); each with what/why/evidence inline; routine findings collapsed to a single count line. Added by retro's fused re-render (Phase 4.5). See §12 for rendering spec. |
| gate   | Single gate control | conduct+retro | Approve / Request Changes; copy-decision-as-prompt; approve disabled until all §04 cards answered AND (if §08 is present) all process findings have written reasons. One gate control governs both sections. |

**Phases:** "conduct" = present in the initial conduct render; "retro" = added by the retro fused re-render.
§08 is absent in the initial conduct render. Retro's Phase 4.5 extends the HTML to add §08 and update the gate logic.

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

## 5b. Force-close-or-investigate cards (§04) — one per non-shipped story

For each story S in `{{blocked_stories}}` (i.e., stories that did NOT reach a `merged` terminal
outcome in the build — either outcome `failed` in the build ledger or absent from any story-terminal
row), render one additional `<div class="decision">` card in §04, positioned after any stakes-class
cards. Use the enriched per-story shape defined in §2 (slug, title, outcome, failure_reason).

```html
<div class="decision" id="d-fc-{{S.slug}}">
  <h3>Incomplete story: {{S.title}}</h3>
  <p><strong>What.</strong> This story did not ship during the build.
    Build outcome: <code>{{S.outcome}}</code>.
    Reason: {{S.failure_reason}} (from build ledger <code>note</code>/<code>reason</code> fields).</p>
  <p><strong>Why it matters.</strong> The capability described by this story is not live.
    Any work that depends on it is blocked or deferred until this is resolved.</p>
  <p><strong>Evidence.</strong> Story slug: <code>{{S.slug}}</code>.
    Build ledger records a story-terminal row with <code>outcome: "{{S.outcome}}"</code>.
    See <code>.momentum/sprints/{{sprint_slug}}/build-ledger.jsonl</code>.</p>
  <div class="opt rec"><b>Option A — Force-close.</b> Record this story as <code>closed-incomplete</code>.
    A triage stub will be created for follow-up investigation. Choose this when the work is
    deferred to a future sprint.</div>
  <div class="opt"><b>Option B — Investigate.</b> Do not close the story yet; leave it at its
    current status and investigate the blocker before the next sprint planning. Choose this when
    you believe the story can be unblocked quickly.</div>
  <div class="opt"><b>Option C — Abandon.</b> Close this story with no follow-up. Choose only
    when the work is no longer needed.</div>
  <p><strong>Recommendation:</strong> Option A (Force-close) — keeping non-terminal stories past
    their sprint increases state machine drift. Investigate items typically become backlog stubs anyway.</p>
  <div class="ack">
    <label><input type="checkbox" id="ack-fc-{{S.slug}}" onchange="paint()">
      I've read this and understand the call for {{S.title}}.</label>
  </div>
  <div class="choices">
    <label onclick="sel(this)"><input type="radio" name="fc-{{S.slug}}" value="A" onchange="paint()">
      Option A — Force-close as closed-incomplete</label>
    <label onclick="sel(this)"><input type="radio" name="fc-{{S.slug}}" value="B" onchange="paint()">
      Option B — Investigate</label>
    <label onclick="sel(this)"><input type="radio" name="fc-{{S.slug}}" value="C" onchange="paint()">
      Option C — Abandon</label>
  </div>
</div>
```

**Clean-sprint path:** When `{{blocked_stories}}` is empty (all stories reached `merged` outcome),
no force-close cards are rendered. §04 states "No decisions required — this build raised no
stakes-class items and all stories shipped."

**Gate wiring:** Force-close cards participate in the same `paint()` gate as stakes-class cards.
`STAKES_DECISION_COUNT` (used in paint() for D1..Dn numeric loop) covers stakes-class cards only;
`FC_SLUGS` covers force-close cards. Every §04 card — stakes-class and force-close — must be
acknowledged with an option selected before approve is enabled.

---

## 6. Anti-rubber-stamp gate (§GATE)

The gate has two phases matching the two-phase rendering of the file:

**Phase 1 — conduct render (initial):** Only §04 decision cards (stakes-class + force-close) are checked.
**Phase 2 — retro fused re-render:** §08 process findings written reasons are added to the check.

The JavaScript below is the **full fused gate** (Phase 2 form). Conduct's initial render uses the
same structure with `PROCESS_COUNT = 0` (§08 absent), making the process checks no-ops.

```javascript
// STAKES_DECISION_COUNT = number of stakes-class D-cards (D1..Dn; does NOT include force-close cards); 0 for clean build
// FC_SLUGS              = array of story slugs with force-close cards (e.g. ['event-logging']); [] for clean build
// PROCESS_COUNT         = number of surfaced process findings in §08; 0 before retro fused re-render

function paint() {
  var gateChoice = val('gate');   // APPROVE or CHANGES
  var allDecisionsAck = true;
  var allDecisionsPicked = true;

  // §04: stakes-class decision cards (D1..Dn, where n = non-force-close count)
  for (var i = 1; i <= STAKES_DECISION_COUNT; i++) {
    if (!document.getElementById('ack-d' + i).checked) allDecisionsAck = false;
    if (!val('d' + i)) allDecisionsPicked = false;
  }

  // §04: force-close-or-investigate cards (one per non-shipped story)
  for (var k = 0; k < FC_SLUGS.length; k++) {
    var slug = FC_SLUGS[k];
    if (!document.getElementById('ack-fc-' + slug).checked) allDecisionsAck = false;
    if (!val('fc-' + slug)) allDecisionsPicked = false;
  }

  // §08: process findings written reasons (added by retro fused re-render)
  var allProcessResponded = true;
  for (var j = 1; j <= PROCESS_COUNT; j++) {
    var ta = document.getElementById('pf-reason-' + j);
    if (!ta || ta.value.trim().length < 3) allProcessResponded = false;
  }

  var ok = false, why = '';
  if (gateChoice === 'APPROVE') {
    if (!allDecisionsAck)       why = 'Read each decision and check the acknowledgment box before approving.';
    else if (!allDecisionsPicked) why = 'Pick an option for each decision (A / B) before approving.';
    else if (!allProcessResponded) why = 'Enter a written response for each process finding before approving.';
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

**When STAKES_DECISION_COUNT == 0 AND FC_SLUGS.length == 0 AND PROCESS_COUNT == 0** (clean build, conduct-only render):
`paint()` skips all card and process checks; approve enables once the developer selects gate choice.

**One gate control, one approve button:** The document contains exactly one `<button id="go">`.
It is not replicated per section. The gate governs both §04 and §08 together.

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

---

## 11. Ship-status lead (§00) — visual rendering spec

§00 is the first content section after the metrics hero. It is the RESULTS-FIRST LEAD mandated
by the companion-surface standard (decision-grade-presentation.md §5).

**Purpose:** Give the developer an immediate scannable answer to "what shipped?" before any prose.

**Rendering:**

```html
<section id="status">
  <h2>Sprint results — what happened</h2>
  <p class="sub">Every story's outcome at a glance. Details follow in §01–§07.</p>
  <div class="status-strip">
    <!-- One pill row per story, in sprint order -->
    {{#each all_sprint_stories}}
    <div class="story-status">
      <span class="story-title">{{this.title}}</span>
      <span class="pill {{statusClass(this.outcome)}}">{{statusLabel(this.outcome)}}</span>
    </div>
    {{/each}}
  </div>
</section>
```

**Status labels and pill classes:**

| Outcome | Label | Pill class | Notes |
|---------|-------|-----------|-------|
| `merged` | `shipped-merged` | `ok` (green; `var(--olive)`) | Emitted during conduct build |
| `failed` | `blocked` | `hipill` (red; `var(--red)`) | Emitted during conduct build |
| `quarantined` | `quarantined` | `warn` (amber; `var(--amber)`) | Post-hoc admin state only (set in Phase 5 approve); not emitted as a conduct-build outcome |
| `closed-incomplete` | `closed-incomplete` | `warn` (amber; `var(--amber)`) | Post-hoc terminal state set in Phase 5 approve; not present at conduct render time — §00 renders `failed` pills only during the initial build |
| `unknown` | `unknown` | `warn` (amber; `var(--amber)`) | Fallback for stories absent from any story-terminal row |

**Helper definitions** (inline `<script>` near §00 section):
```javascript
function statusClass(outcome) {
  if (outcome === 'merged')   return 'ok';
  if (outcome === 'failed')   return 'hipill';
  return 'warn'; // quarantined, closed-incomplete, unknown
}
function statusLabel(outcome) {
  if (outcome === 'merged')            return 'shipped-merged';
  if (outcome === 'failed')            return 'blocked';
  if (outcome === 'quarantined')       return 'quarantined';
  if (outcome === 'closed-incomplete') return 'closed-incomplete';
  return 'unknown';
}
```

**CSS:** Pill base class `.pill { border-radius: 4px; padding: 2px 8px; font-size: 0.85em; font-weight: 600 }`.
Color variants: `.ok { background: var(--olive); color: #fff }`, `.hipill { background: var(--red); color: #fff }`, `.warn { background: var(--amber); color: #fff }`.
The `.story-status` row is a flex row
(`display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid var(--line)`).

**Voice:** No prose sentence per story — only the label pill. Plain-language section header above.

**Presentation-form requirement (§5.1):** The full endgate HTML leads with a plain-language
**results-first purpose hero** — a callout box (`.hero` class from the `companion-decision-surface.html`
skeleton) above §00 that states in 1–2 sentences what this sprint accomplished and where the developer
should focus attention. This hero is the entry point for someone who has not watched the build.
Use the `--amber` accent border matching the companion-surface design family.

---

## 12. Process review section (§08) — rendering spec

§08 is added to the HTML by `momentum:retro` Phase 4.5 (not by conduct). It appears after §07
in document order, before the gate control.

**Structure:**

```html
<section id="process">
  <h2>Process review — Keep / Stop / Change</h2>
  <p class="sub">{{process_findings.length}} findings from the sprint retrospective.
    {{routine_process_count}} routine observations not surfaced
    — <a href="{{audit_doc_path}}">full findings document</a>.</p>

  <!-- Stop findings first (highest urgency), then Change, then Keep -->
  <!-- N = 1-based sequential index: pf-reason-1, pf-reason-2, ... pf-reason-PROCESS_COUNT -->
  <!-- Template notation: Handlebars-style ({{#each}}, {{this.field}}) throughout -->
  {{#each process_findings}}
  <div class="process-finding" id="{{this.id}}">
    <div class="eyebrow">{{uppercaseDisposition this.disposition}}</div>
    <h3>{{this.what}}</h3>
    <p><strong>Why it matters.</strong> {{this.why}}</p>
    <p><strong>Evidence.</strong> {{this.evidence}}</p>
    <div class="pf-response">
      <!-- id uses 1-based index N matching the paint() loop: pf-reason-1 .. pf-reason-PROCESS_COUNT -->
      <label for="pf-reason-{{@index1}}">Your response (required — note action or acknowledgment):</label>
      <textarea id="pf-reason-{{@index1}}" rows="2"
        placeholder="E.g. 'Acknowledged — will create story for next sprint' or 'Deferred — not recurring enough to act on'"
        onchange="paint()" oninput="paint()"></textarea>
    </div>
  </div>
  {{/each}}

  {{#if routine_process_count > 0}}
  <p class="muted">{{routine_process_count}} routine observations collapsed — see
    <a href="{{audit_doc_path}}">{{audit_doc_path}}</a> for the full list.</p>
  {{/if}}
</section>
```

**CSS:** `.process-finding` uses the `.scard` base with a left-border accent:
`stop` = `--red`, `change` = `--amber`, `keep` = `--olive`. The `.pf-response` block is a full-width
textarea with `border: 1px solid var(--line); border-radius: 6px; padding: 8px; width: 100%; font: inherit`.

**Disposition order:** Stop → Change → Keep within §08 (most urgent first).

**Template engine:** Handlebars-style notation throughout §12. `{{#each}}`, `{{this.field}}`, `{{@index1}}` (1-based loop counter, i.e. Handlebars `@index` + 1). The helper `uppercaseDisposition` uppercases the disposition string (STOP / CHANGE / KEEP). The `id` attribute on each `.process-finding` div uses the data shape's `this.id` directly (e.g. `pf-1`, `pf-2`); no additional prefix is added — do NOT write `id="pf-{{this.id}}"` (that would produce `pf-pf-1`). The `pf-reason-N` textarea id matches the 1-based `@index1` so `paint()` can read `pf-reason-1` through `pf-reason-PROCESS_COUNT` sequentially.

**Cap enforcement:** At most 7 entries in `{{process_findings}}`; routine observations beyond the cap
appear only in the count line. Enforcement is explicit in retro Phase 4.5 at digest-assembly time:
after sorting (Stop → Change → Keep), if `process_findings.length > 7`, take the first 7 and
increment `routine_process_count` by `(original_length - 7)`.

**Self-sufficiency floor:** Each surfaced finding carries what, why, and evidence inline. No finding
defers to the audit document — the developer can respond without opening `retro-transcript-audit.md`.

---

## 13. Fused re-render path (retro-owned)

**Single-surface invariant:** For a completed sprint, exactly one human-facing HTML decision surface
exists: `.momentum/handoffs/{{sprint_slug}}-endgate-report.html`. `momentum:retro` Phase 4.5 **extends
this file** — it does not create a new parallel document.

**Re-render mechanism:**
1. Retro reads the existing `{{sprint_slug}}-endgate-report.html`.
2. It inserts §08 (the Process review section) immediately before the gate `<div>` element.
3. It updates the JavaScript constants and the `paint()` function:
   - Set `PROCESS_COUNT = {{process_findings | length}}` (count after cap truncation)
   - Set `STAKES_DECISION_COUNT` from the existing HTML's constant (preserve, do not reset)
   - Replace the `paint()` function with the full fused version from §6 (which checks BOTH §04 and §08)
4. **Pre-populate §04 card state** from the build ledger so the developer does not need to re-acknowledge decisions they already made during conduct:
   - For each stakes-class card D_N: if the ledger contains an `endgate-change-request-parsed` or `endgate-approved` record for that finding, set `checked` on `ack-d{N}` and set `selected` on the matching radio. This is done by emitting `checked` / `selected` attributes directly in the re-rendered HTML — not via JavaScript `onload`. If ledger state is ambiguous or absent for a card, leave it unchecked (the developer re-acknowledges).
   - For each force-close card: if the ledger records the developer's prior choice (option A/B/C), pre-populate similarly.
5. It writes the extended HTML back to the same path.
6. It opens the updated file in the cmux viewer pane (as a tab, per §8).

**Gate coverage (BOTH sections):** The fused gate (§6 `paint()`) covers BOTH §04 cards AND §08 process findings. §04 state is pre-populated from ledger (step 4 above), so the gate can unlock immediately if all §04 cards have known prior choices AND all §08 responses are written. The developer must write a response for each §08 finding — there is no pre-population for §08 (process findings are new since conduct).

**Source links (never inline):**
- Build ledger: link to `.momentum/sprints/{{sprint_slug}}/build-ledger.jsonl`
- Story files: link to `.momentum/stories/{{slug}}.md` per story in §02
- Retro findings: link to `.momentum/sprints/{{sprint_slug}}/retro-transcript-audit.md` in §08
