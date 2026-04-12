# feature-status Workflow

Generate a self-contained HTML planning artifact showing feature coverage gaps,
story assignments, and status. Open it in a cmux browser pane.

---

## Step 1 — Load Config and Resolve Paths

Read `_bmad/bmm/config.yaml` to get `project_name`.

Resolve the following paths:
- `features_path` = `_bmad-output/planning-artifacts/features.json`
- `stories_path` = `_bmad-output/implementation-artifacts/stories/index.json`
- `html_out` = `.claude/momentum/feature-status.html`
- `cache_out` = `.claude/momentum/feature-status.md`

Determine `claude_project_dir` — the absolute path to the `.claude/` parent directory
(the project root). You can infer this from the config file path.

---

## Step 2 — Read features.json

Read `features_path`.

If the file does not exist, stop immediately and output:

```
features.json not found — run feature-artifact-schema story first
Expected location: _bmad-output/planning-artifacts/features.json
```

Parse the JSON. Store `features_content` (raw file text) for hash computation.

---

## Step 3 — Read stories/index.json

Read `stories_path` using Grep + offset/limit (this file can be large):
- Use `Grep` to find story keys referenced in features.json
- For each story key found, read the surrounding context to extract: `title`, `status`, `summary`
- If `stories_path` does not exist, treat all story statuses as "unknown"

Store `stories_content` (raw file text) for hash computation. If the file is
too large to read fully, read the first 2000 lines and use Grep for specific
story lookups.

Build a lookup map: `story_key → { title, status, summary }`.

---

## Step 4 — Determine Project Type

Check in order:

1. **From config**: look for `project_type` in `_bmad/bmm/config.yaml`. If present
   and is `product` or `practice`, use it.

2. **From features.json**: inspect the `project_type` field if present.

3. **Infer from feature structure**:
   - If features have `type` values of `flow`, `connection`, or `quality` → `product`
   - If features have `sdlc_phase` or `covering_skills` fields → `practice`

4. **Ambiguous**: if neither approach resolves, ask the developer:
   ```
   I couldn't determine the project type from config or features.json.
   Is this a product project (flow/connection/quality features)
   or a practice project (skill topology / SDLC phases)?
   Type "product" or "practice":
   ```

Store as `project_type`.

---

## Step 5 — Run Coverage Gap Analysis

For each feature in `features.json`:

1. Look up all stories in the feature's `stories` list using the story lookup map
   from Step 3.

2. **Reason about sufficiency**: read the feature's `acceptance_condition` and
   evaluate whether the assigned stories plausibly deliver it. This is a judgment
   call — not a mechanical count. Consider:
   - What capability does the `acceptance_condition` require?
   - What do the story titles and summaries actually deliver?
   - Is there a meaningful gap between what is required and what is covered?

3. **Produce gap result** for each feature:
   ```
   {
     "has_gap": true|false,
     "gap_description": "Gap: acceptance_condition requires X; assigned stories only cover Y — gap: Z"
   }
   ```

4. **Special cases**:
   - Feature with zero assigned stories AND `status` is not `working` → always has gap:
     "Gap: no stories assigned"
   - Feature with `status: working` AND all stories done → no gap (trust the status)

Store gap results for use in Steps 6 and 7.

---

## Step 6 — Build HTML Context

Compute the following aggregates:

```
total_features = len(features)
status_counts = { working: N, partial: N, not-working: N, not-started: N }
gap_count = count of features where has_gap == true
```

**Sort order within each type group:**
1. Features with `has_gap == true` first (sort by name within gap group)
2. Then: `not-working` → `partial` → `working` → `not-started`

**Build Mermaid source:**

For `product` projects:
```
flowchart TD
  classDef working fill:#22c55e,color:#fff
  classDef partial fill:#f59e0b,color:#fff
  classDef notWorking fill:#ef4444,color:#fff
  classDef notStarted fill:#9ca3af,color:#fff

  F1["Feature Name"]:::statusClass --> S1["story-title ✓"]
  F1 --> S2["story-title ○"]
```
Use `✓` for done stories, `○` for in-progress/backlog, `✗` for not-started.

For `practice` projects:
```
flowchart TD
  classDef working fill:#22c55e,color:#fff
  classDef partial fill:#f59e0b,color:#fff
  classDef notWorking fill:#ef4444,color:#fff
  classDef notStarted fill:#9ca3af,color:#fff

  sprint-planning:::working --> dev:::partial
  dev --> retro:::notStarted
```
Nodes are skill names; edges represent hand-off sequence (SDLC order).

---

## Step 7 — Write HTML Artifact

Write `.claude/momentum/feature-status.html` using the Write tool.

The file must be fully self-contained — no external CSS files. Mermaid.js is
loaded via CDN ESM import only.

Use the template below. Replace all `{placeholder}` values with actual data.

```html
<!DOCTYPE html>
<html lang="en" data-project-type="{project_type}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Feature Status — {project_name}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f8fafc; color: #1e293b; padding: 1.5rem; }
    header { margin-bottom: 1.5rem; }
    header h1 { font-size: 1.5rem; font-weight: 700; }
    header p { color: #64748b; font-size: 0.875rem; margin-top: 0.25rem; }
    .summary-stats { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
    .stat-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 0.5rem; padding: 0.75rem 1rem; min-width: 120px; }
    .stat-card .label { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
    .stat-card .value { font-size: 1.5rem; font-weight: 700; margin-top: 0.125rem; }
    .stat-card.gaps .value { color: #ef4444; }
    details.dependency-graph { background: #fff; border: 1px solid #e2e8f0; border-radius: 0.5rem; margin-bottom: 1.5rem; padding: 0.75rem 1rem; }
    details.dependency-graph summary { cursor: pointer; font-weight: 600; font-size: 0.9rem; color: #475569; user-select: none; }
    .mermaid { margin-top: 0.75rem; }
    .feature-group { background: #fff; border: 1px solid #e2e8f0; border-radius: 0.5rem; margin-bottom: 1.5rem; overflow: hidden; }
    .feature-group-header { padding: 0.75rem 1rem; background: #f1f5f9; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; }
    .feature-group-header h2 { font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #475569; }
    .group-gap-summary { font-size: 0.75rem; color: #64748b; }
    table { width: 100%; border-collapse: collapse; }
    th { padding: 0.5rem 1rem; text-align: left; font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.04em; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
    td { padding: 0.625rem 1rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
    tr:last-child td { border-bottom: none; }
    tr[data-has-gap="true"] { background: #fff7ed; }
    .feature-name { font-weight: 600; font-size: 0.9rem; }
    .badge { display: inline-block; padding: 0.2em 0.6em; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; color: #fff; }
    [data-status="working"] .badge { background: #22c55e; }
    [data-status="partial"] .badge { background: #f59e0b; }
    [data-status="not-working"] .badge { background: #ef4444; }
    [data-status="not-started"] .badge { background: #9ca3af; }
    .story-fraction { font-size: 0.8rem; white-space: nowrap; }
    progress { width: 60px; height: 6px; vertical-align: middle; margin-left: 4px; border-radius: 3px; }
    progress::-webkit-progress-bar { background: #e2e8f0; border-radius: 3px; }
    progress::-webkit-progress-value { background: #3b82f6; border-radius: 3px; }
    .gap-flag { display: inline-block; background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; border-radius: 4px; padding: 0.15em 0.5em; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em; }
    details.row-details summary { cursor: pointer; font-size: 0.8rem; color: #3b82f6; list-style: none; }
    details.row-details summary::before { content: "▶ "; }
    details.row-details[open] summary::before { content: "▼ "; }
    .acceptance-condition { font-size: 0.8rem; color: #475569; margin: 0.5rem 0; padding: 0.5rem; background: #f8fafc; border-left: 3px solid #e2e8f0; border-radius: 2px; }
    .stories-list { margin: 0.5rem 0; padding-left: 1rem; }
    .stories-list li { font-size: 0.8rem; color: #475569; margin-bottom: 0.125rem; }
    .story-status-done { color: #22c55e; }
    .story-status-in-progress { color: #f59e0b; }
    .story-status-backlog, .story-status-not-started { color: #9ca3af; }
    .gap-description { font-size: 0.8rem; color: #dc2626; margin-top: 0.5rem; padding: 0.375rem 0.5rem; background: #fef2f2; border-radius: 4px; }
    .sdlc-table th:first-child { width: 180px; }
    footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; font-size: 0.75rem; color: #94a3b8; text-align: center; }
  </style>
</head>
<body>

<header>
  <h1>Feature Status — {project_name}</h1>
  <p>Generated {generated_at}</p>
</header>

<section class="summary-stats">
  <div class="stat-card">
    <div class="label">Total</div>
    <div class="value">{total_features}</div>
  </div>
  <div class="stat-card">
    <div class="label">Working</div>
    <div class="value">{count_working}</div>
  </div>
  <div class="stat-card">
    <div class="label">Partial</div>
    <div class="value">{count_partial}</div>
  </div>
  <div class="stat-card">
    <div class="label">Not Working</div>
    <div class="value">{count_not_working}</div>
  </div>
  <div class="stat-card">
    <div class="label">Not Started</div>
    <div class="value">{count_not_started}</div>
  </div>
  <div class="stat-card gaps">
    <div class="label">With Gaps</div>
    <div class="value">{gap_count}</div>
  </div>
</section>

<details class="dependency-graph">
  <summary>{diagram_label}</summary>
  <div class="mermaid">
{mermaid_source}
  </div>
</details>

{feature_sections_html}

<footer>
  momentum:feature-status · {project_name} · {generated_at}
</footer>

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'default' });
</script>

</body>
</html>
```

**Building `{feature_sections_html}` for product projects:**

For each type group (`flow`, `connection`, `quality`) that has at least one feature,
write:

```html
<section class="feature-group" data-type="{type}">
  <div class="feature-group-header">
    <h2>{type_label}</h2>
    <span class="group-gap-summary">{N} features · {M} with gaps</span>
  </div>
  <table>
    <thead>
      <tr>
        <th>Feature</th>
        <th>Status</th>
        <th>Stories</th>
        <th>Gap</th>
        <th>Details</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</section>
```

Each row:
```html
<tr data-status="{status}" data-has-gap="{has_gap}">
  <td class="feature-name">{feature_name}</td>
  <td><span class="badge">{status}</span></td>
  <td class="story-fraction">
    {done_count}/{total_count}
    <progress value="{done_count}" max="{total_count}"></progress>
  </td>
  <td>{gap_flag_html}</td>
  <td>
    <details class="row-details">
      <summary>Details</summary>
      <p class="acceptance-condition">{acceptance_condition}</p>
      <ul class="stories-list">
        {story_items}
      </ul>
      {gap_description_html}
    </details>
  </td>
</tr>
```

Where `{gap_flag_html}` is `<span class="gap-flag">GAP</span>` if `has_gap` is true,
otherwise empty string.

Where `{gap_description_html}` is `<p class="gap-description">{gap_description}</p>`
if `has_gap` is true, otherwise empty string.

Each story item:
```html
<li><span class="story-status-{status}">{status_icon}</span> {story_title} ({status})</li>
```
Status icons: done → ✓, in-progress → ◎, backlog/not-started → ○, unknown → ?

**Building `{feature_sections_html}` for practice projects:**

Write an SDLC coverage table:

```html
<section class="feature-group sdlc-coverage">
  <div class="feature-group-header">
    <h2>SDLC Phase Coverage</h2>
    <span class="group-gap-summary">{N} phases · {M} with gaps</span>
  </div>
  <table class="sdlc-table">
    <thead>
      <tr>
        <th>SDLC Phase</th>
        <th>Covering Skills</th>
        <th>Status</th>
        <th>Gap</th>
        <th>Details</th>
      </tr>
    </thead>
    <tbody>
      {rows grouped by sdlc_phase, GAP rows first}
    </tbody>
  </table>
</section>
```

---

## Step 8 — Write Cache File

Compute the SHA-256 input hash using Bash:

```bash
python3 -c "
import hashlib, sys
f = open('_bmad-output/planning-artifacts/features.json').read()
s = open('_bmad-output/implementation-artifacts/stories/index.json').read() if __import__('os').path.exists('_bmad-output/implementation-artifacts/stories/index.json') else ''
print(hashlib.sha256((f+':'+s).encode()).hexdigest())
"
```

Compute `generated_at` using Bash:
```bash
python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat())"
```

Build the summary line:
```
{total} features: {working} working · {partial} partial · {not-started} not-started · {gap_count} gaps
```

Write `.claude/momentum/feature-status.md`:

```markdown
---
input_hash: {sha256_hex}
summary: {summary_line}
generated_at: {iso_datetime}
---

{summary_line}
```

---

## Step 9 — Open in Browser

Run:
```bash
cmux browser open "file://{absolute_claude_project_dir}/.claude/momentum/feature-status.html"
```

To get the absolute project path, run:
```bash
pwd
```
from the project root, or use the path from Step 1.

If the `cmux` command is not available (returns non-zero exit or "command not found"),
output instead:

```
HTML artifact written to: .claude/momentum/feature-status.html

To open it, run:
  open .claude/momentum/feature-status.html        # macOS
  xdg-open .claude/momentum/feature-status.html   # Linux
  start .claude/momentum/feature-status.html       # Windows
```

---

## Error Handling

| Situation | Action |
|---|---|
| `features.json` not found | Output clear error (Step 2), stop |
| `stories/index.json` not found | Continue with all story statuses as "unknown" |
| Story key in feature not found in index | Mark as status "unknown", note in gap analysis |
| Project type ambiguous | Ask developer (Step 4) |
| `cmux` not available | Output file path and open instructions (Step 9) |
| HTML write fails | Report error with path and write permissions hint |

## Large File Handling

`stories/index.json` commonly exceeds 10,000 tokens. Use these strategies:

1. Use `Grep` to find story keys from `features.json` within `stories/index.json`
2. Read targeted sections with `offset` and `limit` based on Grep line numbers
3. Never attempt a full read of `stories/index.json` without chunking
4. For hash computation, use the Bash python3 approach — it handles large files natively
