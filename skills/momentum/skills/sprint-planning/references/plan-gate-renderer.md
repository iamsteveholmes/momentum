# Plan Gate Renderer — Data Contract & Rendering Spec

**Implements:** Step 7 (developer review) of `sprint-planning/workflow.md` — the pre-sprint companion decision surface.
**Governs:** How the sprint-planning skill builds the self-contained HTML gate handed to the developer before activation.
**Template to fill:** `skills/momentum/references/templates/companion-decision-surface.html`
**Sibling pattern:** `skills/momentum/skills/conductor/references/endgate-report-renderer.md`
**Standard authority:** `skills/momentum/references/rules/decision-grade-presentation.md` §2.2 row 9 · §5 · §5.1

---

## 1. Input data contract — what Step 7 assembles

At the start of Step 7, the following context is available from prior steps:

### 1a. Sprint plan fundamentals

```
sprint_slug          string   — e.g. "sprint-2026-07-06"
selected_stories     list     — ordered list of approved story slugs
```

### 1b. Per-story record (one entry per selected story)

For each story slug, read its story file at `.momentum/stories/{{slug}}.md` and extract:

```
story_slug           string   — kebab-case identifier
title                string   — story title (from frontmatter or H1)
story_type           string   — "feature" | "fix" | "practice" | "spike"
change_type          list     — e.g. ["skill-instruction"] or ["app-ui", "backend"]
depends_on           list     — list of story slugs this story depends on
touches              list     — file paths this story modifies
acceptance_criteria  string   — plain-English ACs section (full text)
```

### 1c. Computed wave assignment

From `momentum-tools sprint plan` wave assignments (already stored):

```
waves                map      — { wave_number → [story_slugs] }
story_wave           map      — { story_slug → wave_number }
```

### 1d. Contracts and coverage

From Step 3.5 output:

```
contract_metadata    map      — { story_slug → { verification_method, contract_path, coverage_disposition } }
guard_status         string   — "clean" | "accepted_with_failures" | "residual_failures"
```

### 1e. AVFL result

From Step 6:

```
avfl_result          string   — "CLEAN" | "CHECKPOINT_WARNING" | "GATE_FAILED"
avfl_findings        list     — findings list (empty if CLEAN); each carries { severity, summary }
```

---

## 2. Assembly — binding the gate data model

At the top of Step 7, before rendering, synthesize the following gate data model from the above inputs.

### 2a. Per-story synthesis

For each story in `selected_stories`, produce a `gate_story` record:

```
gate_story = {
  slug:           story_slug,
  title:          title,
  wave:           story_wave[slug],
  deps:           depends_on (list of slugs, empty if none),
  stakes:         HIGH | medium | low      ← see §3 stakes synthesis rule,
  one_line_value: string                   ← see §3 value synthesis rule,
  verdict:        "★ CALL" | "✓ batch"    ← see §3 verdict rule,
  story_path:     ".momentum/stories/{{slug}}.md",
  spec_path:      ".momentum/sprints/{{sprint_slug}}/specs/{{slug}}.*"
}
```

### 2b. Genuine forks list

```
genuine_forks = list of ForkItem (≤ 7)    ← see §4 fork detection rules
```

### 2c. Defaulted choices list

```
defaulted_choices = list of string        ← choices resolved to standards, no decision needed
```

### 2d. Structure metadata

```
spof_story      = slug of the story with the most dependents (set ⚠ marker); null if no deps
wave_count      = count of distinct waves
call_count      = count of gate_stories where verdict == "★ CALL"
irrev_count     = count of stories that involve irreversible ops (deploy, migration, db-schema change)
                  (detect from: story title / AC keywords: "migrate", "deploy", "schema", "delete", "drop")
```

---

## 3. Synthesis rules — per-story fields

### 3.1 Stakes synthesis

Assign `stakes` by reading the story's `acceptance_criteria` text and `change_type`:

| Signal | Stakes |
|--------|--------|
| AC mentions "auth", "security", "credential", "permission", "data loss", "irreversible", "migration", "deploy" | **HIGH** |
| `change_type` includes `app-ui` + `backend`, or multiple change types affecting user-facing behavior | **medium** |
| `change_type` is single `skill-instruction`, `config-structure`, or `specification` | **low** |
| `change_type` is `research-spike` | **low** |
| Story touches architecture decisions or creates new agents | **medium** |
| Default (none of the above patterns match) | **low** |

### 3.2 One-line value synthesis

Write a ≤ 15-word plain-English outcome in the form: "[verb] [what the user/developer gets]".

Derive from: story title + first 2 sentences of Acceptance Criteria. Do NOT quote the AC verbatim — translate it into a user-facing outcome.

Examples:
- "Lets developers approve the sprint from a scannable visual gate instead of a raw text dump."
- "Adds a reusable skeleton for any companion decision surface in the practice."
- "Prevents activation without a written per-story approval on record."

### 3.3 Verdict rule (★ CALL vs ✓ batch)

Mark a story as `★ CALL` if ANY of the following are true:
1. The story has a genuine fork (see §4)
2. `stakes == "HIGH"`
3. The story has unresolved AVFL findings (its slug appears in `avfl_findings`)
4. `guard_status != "clean"` and this story's contract was flagged

Mark as `✓ batch` (build as-specified) if ALL of the above are false.

---

## 4. Fork detection rules — genuine forks vs defaulted choices

A **genuine fork** is a choice the developer must make that cannot be defaulted to existing standards, rules, or ADRs. The goal is ≤ 7 forks; surface only what genuinely needs a yes/no.

### Classify as a GENUINE FORK if:

- A story's scope, approach, or sequencing conflicts with another selected story
- A story's `depends_on` list references a story NOT in the sprint and NOT yet done (unresolved external dependency)
- An AVFL finding for this story has severity `critical` or `major` and remains unaddressed
- The story touches a path also touched by another selected story (merge-conflict risk) AND they are in the same wave
- `guard_status` indicates contaminated contracts that the developer accepted (the acceptance itself becomes a fork card)
- The wave assignment would create a bottleneck (a single story in an early wave that gates all others, and its scope/readiness is uncertain)

### Classify as DEFAULTED TO STANDARDS if:

- Story type conventions (e.g., "research-spike stories always use document-review verification") — state the convention
- Naming and file placement (governed by handoff-conventions.md or directory conventions) — state the rule
- Wave ordering follows dependency graph (DAG-valid, no cycles) — state: "wave assignment follows computed dependency graph"
- AVFL result CLEAN with no findings — state: "AVFL returned CLEAN — no plan defects found"
- Guard status CLEAN — state: "Adversarial contract guard passed — no insider-knowledge contamination"
- Any team composition choice that follows the standard routing table (dev-skills for skill stories, etc.)

### Fork card shape

For each genuine fork, produce a `ForkItem`:

```
ForkItem = {
  title:           string   — the fork as a question (≤ 12 words),
  stakes:          HIGH | medium,
  what:            string   — the concrete thing at stake, stated plainly; inline the substance (no bare handles),
  why:             string   — what goes wrong or improves if the developer decides one way or the other,
  evidence:        string   — file path, count, conflict summary, or AVFL finding reference (checkable),
  recommendation:  string   — the defaulted call in one line,
  options:         list     — the resolution paths, e.g.:
                              ["Approve as specified", "Modify scope or sequencing", "Remove from sprint"]
}
```

**No bare handles.** Every `what` and `evidence` field must state the substance inline — do not write "per SDR-X" or "see story file". Quote or summarize.

---

## 5. HTML gate structure — fixed section spine

Build a **self-contained single `.html` file** — inline `<style>` and `<script>`, zero external dependencies. Use the CSS tokens and component classes from `references/templates/companion-decision-surface.html` exactly as shipped (warm-parchment palette, `.hero`, `.grid`, `.stat`, `.scard`, `.card`, `.gate`, etc.).

**Voice:** Assume nothing. Write for a developer who has not watched the planning session. Plain language; no jargon. Define every term inline.

### Section order (fixed — must not reorder or omit required sections):

| Section | Required | Element |
|---------|----------|---------|
| Page title + eyebrow | Yes | `<h1>` + `<p class="sub">` |
| Purpose hero | Yes | `<div class="hero">` |
| ✓ Verified line | Yes | `<div class="grid">` with 4 stat tiles |
| Structure diagram | Yes (if N≥2 stories) | `<div class="diagram">` with inline SVG |
| Items at a glance | Yes | `<h2>` + `<div class="cards">` with one `.scard` per story |
| Decision cards | Yes (0 cards if no forks) | `<h2>` + one `.card` per genuine fork |
| Risks | Conditional | `<h2>` + `<ol class="risks">` (omit if no risks to surface) |
| Defaulted to standards | Yes | `<details>` collapsible |
| Sign-off gate | Yes | `<div class="gate">` |

### 5.1 Purpose hero

Fill the `.hero` block with:
- `.eyebrow`: "What this sprint does"
- `.big`: 1–2 sentences stating the sprint's purpose in plain language readable by a non-implementer. Bold the 2–3 most important nouns/outcomes with `<b>…</b>`.
- `.deliver` list: 3–5 bullet outcomes (key deliverables), each ≤ 12 words
- `.heroline`: "N stories · K need a yes/no from you · M ready as-specified · ~T min to review." (estimate 2 min per CALL item, 30 sec per batch item)

### 5.2 Verified line (stat tiles)

Four `.stat` tiles (mechanically verified — not for human review):

1. **Story count** — `{{selected_stories|count}}` · "stories selected"
2. **Wave count** — `{{wave_count}}` · "execution waves{{' ⚠ one critical-path story' if spof_story}}"
3. **CALL count** — `{{call_count}}` · "genuine decisions for you (★ CALL)"
4. **Irreversible ops** — `{{irrev_count}}` · "irreversible ops (deploy / migration / delete)"

### 5.3 Structure diagram (inline SVG)

Render as a `<svg viewBox="0 0 880 {{height}}">` where height scales with story count (approx 80px per story row + 40px per wave header).

Layout rules:
- Group stories by wave horizontally. Wave N is a column of nodes.
- Draw arrow connectors (`<path marker-end="url(#arr)">`) from each story to its dependents.
- Node styling:
  - `stakes == HIGH` → fill `#f6ddd6` stroke `#9a3b2f` stroke-width 3 (red border)
  - `stakes == medium` → fill `#fbeccf` stroke `#7a5a1e` (amber border)
  - `stakes == low` or routine → fill `#fffdf8` stroke `#cdc6b4` (light border)
  - SPOF story → additionally label with `⚠` and use stroke-width 4
- Node label: story slug (abbreviated to ≤ 18 chars) + wave tag
- Include `verdict` badge: `★ CALL` or `✓` inside the node text

Below the SVG, add:
```html
<p class="muted" style="font-size:14px">Read this as: <b>{{one-sentence diagram takeaway}}</b></p>
```

The diagram takeaway states what must land first and what hangs off what — in one sentence.

### 5.4 Items at a glance

One `.scard` per story, ordered by wave then by stakes (HIGH first within wave):

```html
<div class="scard s-high|s-med|s-low">
  <div class="top">
    <span class="id">{{slug}} · {{title}}</span>
    <span class="pill call|batch">★ CALL|✓ batch</span>
  </div>
  <p class="val">{{one_line_value}}</p>
  <p class="meta">Wave {{wave}} · deps: {{deps|join(", ")|default("none")}} · {{stakes}} · <a href="file://{{story_path}}">story ↗</a> · <a href="file://{{spec_path}}">spec ↗</a></p>
</div>
```

Stake-to-scard-class mapping: HIGH → `s-high`, medium → `s-med`, low → `s-low`.

### 5.5 Decision cards

Header: `<h2>{{call_count}} decision{{call_count != 1 ? 's' : ''}} need a yes/no from you</h2>`

If `call_count == 0`: render `<p class="muted">All stories build as-specified — no forks found. Clean-plan path: approve the batch below.</p>` instead of cards.

For each genuine fork (capped at 7), render:

```html
<div class="card dec|decmed" id="fork-{{index}}">
  <h3>{{fork.title}} <span class="pill hipill|warn">{{fork.stakes}} · fork</span></h3>
  <div class="field"><span class="lab">What</span>{{fork.what}}</div>
  <div class="field"><span class="lab">Why it matters</span>{{fork.why}}</div>
  <div class="field"><span class="lab">Evidence</span><div class="ev">{{fork.evidence}}</div></div>
  <div class="rec"><span class="lab">Recommend — {{fork.recommendation}}</span></div>
  <div class="field"><span class="lab">Options</span>
    <ul>{{for each opt: <li>{{opt}}</li>}}</ul>
  </div>
</div>
```

Use `.dec` (red left border) for HIGH stakes forks and `.decmed` (amber) for medium.

### 5.6 Risks section (conditional)

Include only if there are risks worth calling out beyond the fork cards. Sources:
- AVFL findings with severity `warning` or lower (not already in fork cards)
- Touch-overlap stories in the same wave (merge risk)
- External dependency stories where the dep is not in the sprint

Format as `<ol class="risks">` with ≤ 5 items. Omit the section header if no risks exist.

### 5.7 Defaulted to standards

Always include this `<details>` block. List every defaulted choice:

```html
<details>
<summary>Defaulted to standards — {{defaulted_choices|count}} choices handled, no decision needed</summary>
<ul>
  {{for each choice: <li>{{choice}}</li>}}
</ul>
</details>
```

### 5.8 Sign-off gate

**Anti-rubber-stamp requirement:** When `call_count > 0`, the gate must require a written one-line verdict per fork before activation can proceed. A blanket "approve all" with no per-fork reasoning must not satisfy the gate.

**Implementation:** Use JavaScript to enforce the gate:

```javascript
function checkGate() {
  var allSigned = true;
  for (var i = 1; i <= FORK_COUNT; i++) {
    var v = document.getElementById('verdict-' + i).value.trim();
    if (!v) { allSigned = false; break; }
  }
  var decision = document.querySelector('input[name="decision"]:checked');
  document.getElementById('submit-btn').disabled = !(allSigned && decision);
  document.getElementById('gate-hint').textContent = allSigned && decision
    ? 'Ready — paste the decision text back into the chat.'
    : 'Write a one-line verdict for each fork above, then select Approve or Modify.';
}
```

Gate HTML structure:

```html
<div class="gate">
  <h2>Sign-off</h2>
  <p>Approve the <b>{{batch_count}} ✓ batch</b> items to build as-specified?
     <span style="font-size:20px">&#9744;</span></p>

  {{if call_count > 0:}}
  <p style="margin-top:16px"><b>For each fork, write a one-line verdict + reason</b>
     (the blank forces a real read — blanket approve-all is insufficient):</p>
  {{for each fork with index i:}}
  <div class="chk">
    <b>Fork {{i}}:</b> {{fork.title}}
    <input id="verdict-{{i}}" type="text" class="blank" placeholder="your call + one-line reason"
           oninput="checkGate()" style="min-width:280px;border:1px solid #c8bfaa;border-radius:4px;padding:3px 7px">
  </div>
  {{endfor}}
  {{endif}}

  <div style="margin-top:20px">
    <label><input type="radio" name="decision" value="approve" onchange="checkGate()"> <b>A — Approve and activate</b></label><br>
    <label><input type="radio" name="decision" value="modify" onchange="checkGate()"> M — Modify (re-render gate after changes)</label><br>
    <label><input type="radio" name="decision" value="avfl" onchange="checkGate()"> R — Re-run AVFL before deciding</label>
  </div>

  <p id="gate-hint" style="margin-top:12px;color:#6b5e4a;font-size:14px">
    {{if call_count > 0: Write a one-line verdict for each fork above, then select Approve or Modify.
      else: Select Approve to activate, or Modify to adjust the plan.}}
  </p>
  <button id="submit-btn" disabled style="margin-top:8px;padding:10px 22px;background:#3a5a7a;color:#fff;border:none;border-radius:7px;font-size:15px;cursor:pointer">
    Copy decision → paste into chat
  </button>
  <script>
    var FORK_COUNT = {{call_count}};
    document.getElementById('submit-btn').addEventListener('click', function() {
      var lines = ['Sprint plan decision — ' + '{{sprint_slug}}'];
      var dec = document.querySelector('input[name="decision"]:checked').value;
      lines.push('Decision: ' + dec.toUpperCase());
      for (var i = 1; i <= FORK_COUNT; i++) {
        lines.push('Fork ' + i + ': ' + document.getElementById('verdict-' + i).value.trim());
      }
      navigator.clipboard.writeText(lines.join('\n'));
    });
    function checkGate() {
      var allSigned = true;
      for (var i = 1; i <= FORK_COUNT; i++) {
        if (FORK_COUNT > 0 && !document.getElementById('verdict-' + i).value.trim()) {
          allSigned = false; break;
        }
      }
      var decision = document.querySelector('input[name="decision"]:checked');
      document.getElementById('submit-btn').disabled = !(allSigned && decision);
      document.getElementById('gate-hint').textContent = allSigned && decision
        ? 'Ready — copy and paste the decision text back into the chat.'
        : (FORK_COUNT > 0 ? 'Write a one-line verdict for each fork above, then select a path.' : 'Select a path.');
    }
  </script>
  <p style="margin-top:16px" class="muted">Nothing is built until you sign off. The full machine-grade detail
  (tasks, dev notes, specs) lives in <code>.momentum/stories/</code> and
  <code>.momentum/sprints/{{sprint_slug}}/specs/</code> — one click away, deliberately not in this view.</p>
</div>
```

**Clean-plan path (zero forks):** When `call_count == 0`, render only the batch-approve radio group with no per-fork blanks. `checkGate()` requires only a selected radio, not written verdicts.

---

## 6. File output

```
.momentum/handoffs/{{sprint_slug}}-plan-gate.html
```

After writing, open in the cmux Browser viewer pane as a tab (never a new structural pane):

```bash
cmux browser new "file://$(pwd)/.momentum/handoffs/{{sprint_slug}}-plan-gate.html" \
  --workspace "$CMUX_WORKSPACE_ID" --focus false
```

The `--focus false` flag keeps the developer's main workspace active.

---

## 7. Honesty contract — links, never inlines

The gate **links to** canonical story files and specs as depth-on-demand. It **never inlines** their full body and **never edits** them. The rule:

- Use `<a href="file://$(pwd)/{{story_path}}">story ↗</a>` for each story's `.md` file
- Use `<a href="file://$(pwd)/{{spec_path}}">spec ↗</a>` for each story's contract file
- Do NOT paste story ACs, Dev Notes, or Tasks/Subtasks into the gate HTML
- The machine band (full spec detail for the dev agent) stays in the source files

This keeps the review surface scannable and the dev-agent source of truth uncontaminated.

---

## 8. Voice — assume nothing

Write for someone who did not watch the planning session and does not know Momentum internals:

- "Execution wave" → define inline on first use: "execution wave (a group of stories that can run concurrently)"
- Spell out acronyms on first use: AVFL → "AVFL (the adversarial validation layer)"
- Never use: "per DEC-X", "per Step N", "per the routing table" — state what the rule says, don't reference it by handle
