/**
 * Momentum Cycle Dashboard — Hono+Bun server
 *
 * Start: bun --hot skills/momentum/dashboard/server.tsx
 * Port:  3456
 */

import { Hono } from "hono";
import { html } from "hono/html";

// ---------------------------------------------------------------------------
// Features lens — types
// ---------------------------------------------------------------------------
export type Feature = {
  feature_slug: string;
  name: string;
  status: string;
  stories_done: number;
  stories_remaining: number;
  stories?: string[];
  acceptance_condition?: string;
};

export type StoryEntry = { status: string; title?: string };
export type StoryMap = Record<string, StoryEntry>;

export type FeatureRow = Feature & {
  has_gap: boolean;
  gap_reason: string;
  total: number;
};

// ---------------------------------------------------------------------------
// Features lens — gap analysis (Task 2)
// ---------------------------------------------------------------------------

/**
 * Structural gap heuristic: a feature has a gap when stories_done === 0
 * and status is not 'working'. Features with status 'working' are never
 * flagged regardless of story counts.
 */
export function analyzeGap(
  feature: Feature,
  _storyMap: StoryMap
): { has_gap: boolean; reason: string } {
  if (feature.status === "working") {
    return { has_gap: false, reason: "" };
  }
  if (feature.stories_done === 0) {
    return {
      has_gap: true,
      reason: "zero stories done and status is not working",
    };
  }
  return { has_gap: false, reason: "" };
}

// ---------------------------------------------------------------------------
// Features lens — sort helpers (Task 3)
// ---------------------------------------------------------------------------

const STATUS_SEVERITY: Record<string, number> = {
  "not-working": 0,
  partial: 1,
  working: 2,
  "not-started": 3,
};

function severityOf(status: string): number {
  return STATUS_SEVERITY[status] ?? 99;
}

export function buildSortedRows(
  features: Feature[],
  storyMap: StoryMap
): FeatureRow[] {
  const rows: FeatureRow[] = features.map((f) => {
    const { has_gap, reason } = analyzeGap(f, storyMap);
    return {
      ...f,
      has_gap,
      gap_reason: reason,
      total: f.stories_done + f.stories_remaining,
    };
  });

  // Gap rows first (alpha), then non-gap sorted by severity then alpha
  rows.sort((a, b) => {
    if (a.has_gap !== b.has_gap) return a.has_gap ? -1 : 1;
    if (a.has_gap && b.has_gap) return a.name.localeCompare(b.name);
    const sevDiff = severityOf(a.status) - severityOf(b.status);
    if (sevDiff !== 0) return sevDiff;
    return a.name.localeCompare(b.name);
  });

  return rows;
}

// ---------------------------------------------------------------------------
// Features lens — data readers (Task 1, Task 5)
// ---------------------------------------------------------------------------

async function readFeaturesJson(): Promise<Feature[]> {
  try {
    const file = Bun.file("_bmad-output/planning-artifacts/features.json");
    if (!(await file.exists())) return [];
    const data = await file.json();
    if (!data || typeof data !== "object") return [];
    // features.json is an object keyed by feature_slug
    return Object.values(data) as Feature[];
  } catch {
    return [];
  }
}

async function readStoriesIndex(): Promise<StoryMap> {
  try {
    const file = Bun.file(".momentum/stories/index.json");
    if (!(await file.exists())) {
      console.warn("[canvas] .momentum/stories/index.json not found — treating all stories as unknown");
      return {};
    }
    const data = await file.json();
    if (!data || typeof data !== "object") return {};
    return data as StoryMap;
  } catch (err) {
    console.warn("[canvas] Failed to read stories/index.json:", err);
    return {};
  }
}

// ---------------------------------------------------------------------------
// Features lens — status badge colors (Task 4)
// ---------------------------------------------------------------------------

const STATUS_COLORS: Record<string, string> = {
  working: "var(--accent, #5863a8)",
  partial: "#d97706",
  "not-working": "#dc2626",
  "not-started": "#6b7280",
};

function badgeColor(status: string): string {
  return STATUS_COLORS[status] ?? "#6b7280";
}

// ---------------------------------------------------------------------------
// Features lens — HTML renderer (Tasks 3, 4)
// ---------------------------------------------------------------------------

function renderFeaturesTable(rows: FeatureRow[]): string {
  if (rows.length === 0) {
    return `<tr><td colspan="4" style="padding:12px 8px;color:var(--inkOnDarkMuted,rgba(240,238,233,0.70));font-style:italic;font-size:12px;">No features found — run momentum:feature-grooming first</td></tr>`;
  }

  return rows
    .map((row) => {
      const gapStyle = row.has_gap
        ? ' style="background:var(--gap,#a85a2a);"'
        : "";
      const gapIcon = row.has_gap
        ? ' <span title="Gap detected" style="color:#fff8;font-size:10px;">⚠</span>'
        : "";
      const done = row.stories_done;
      const total = row.total;
      const pct = total > 0 ? Math.round((done / total) * 100) : 0;
      const badgeStyle = `background:${badgeColor(row.status)};color:#fff;padding:2px 7px;border-radius:3px;font-size:9.5px;font-family:'JetBrains Mono',monospace;letter-spacing:0.5px;`;
      const tdStyle = "padding:7px 10px;font-size:12px;vertical-align:middle;border-bottom:1px solid var(--ruleDark,rgba(255,252,245,0.10));";

      return `<tr${gapStyle}>
  <td style="${tdStyle}color:var(--inkOnDark,#f0eee9);">${row.name}${gapIcon}</td>
  <td style="${tdStyle}"><span style="${badgeStyle}">${row.status}</span></td>
  <td style="${tdStyle}color:var(--inkOnDarkMuted,rgba(240,238,233,0.70));font-variant-numeric:tabular-nums;">${done}/${total} <progress value="${done}" max="${Math.max(total,1)}" style="height:6px;width:60px;vertical-align:middle;accent-color:${badgeColor(row.status)};"></progress></td>
  <td style="${tdStyle}color:var(--inkOnDarkMuted,rgba(240,238,233,0.70));">${pct}%</td>
</tr>`;
    })
    .join("\n");
}

// ---------------------------------------------------------------------------
// Design tokens (warm dark paper palette)
// ---------------------------------------------------------------------------
const tokens = {
  paper: "#fbfaf7",
  paperAlt: "#f5f3ed",
  rule: "#e7e3d9",
  ruleStrong: "#d4cfc2",
  ink: "#1e1d1a",
  inkMuted: "#5a574f",
  inkQuiet: "#8a8678",
  inkFaint: "#b5b0a2",
  readingPaper: "#faf6ec",
  readingPaperAlt: "#f3eedf",
  readingRule: "#e5dfce",
  accent: "#5863a8",
  accentSoft: "rgba(88,99,168,0.08)",
  gap: "#a85a2a",
  gapSoft: "rgba(168,90,42,0.09)",
  paperDark: "#16140f",
  paperDarkAlt: "#1e1b15",
  ruleDark: "rgba(255,252,245,0.10)",
  ruleDarkStrong: "rgba(255,252,245,0.18)",
  inkOnDark: "#f0eee9",
  inkOnDarkMuted: "rgba(240,238,233,0.70)",
  inkOnDarkQuiet: "rgba(240,238,233,0.48)",
  inkOnDarkFaint: "rgba(240,238,233,0.36)",
};

// ---------------------------------------------------------------------------
// Meta helpers
// ---------------------------------------------------------------------------
function shortHash(): string {
  return Math.random().toString(36).slice(2, 9);
}

function isoDate(): string {
  return new Date().toISOString().slice(0, 10);
}

// ---------------------------------------------------------------------------
// Breadcrumb component
//
// Rules (from design spec):
//   - Rightmost segment = accent blue, no pointer (current page)
//   - Ancestors to the left = gray + clickable
//   - Only ancestors TO THE LEFT of current appear; no rail
// ---------------------------------------------------------------------------
type Crumb = { label: string; href?: string };

function Breadcrumbs({ crumbs }: { crumbs: Crumb[] }) {
  if (crumbs.length === 0) return null;

  const parts: string[] = [];
  crumbs.forEach((c, i) => {
    const isLast = i === crumbs.length - 1;
    if (isLast) {
      parts.push(
        `<span class="seg here">${c.label}</span>`
      );
    } else {
      const href = c.href ?? "#";
      parts.push(
        `<a class="seg" href="${href}">${c.label}</a>`
      );
      parts.push(`<span class="sep">/</span>`);
    }
  });

  return html`
    <nav class="crumb-bar">
      <div class="crumbs">${parts.join("")}</div>
    </nav>
  `;
}

// ---------------------------------------------------------------------------
// Lens placeholder section
// ---------------------------------------------------------------------------
function LensSection({
  id,
  tag,
  title,
  poll,
}: {
  id: string;
  tag: string;
  title: string;
  poll?: boolean;
}) {
  const trigger = poll ? "load, every 2s" : "load";
  return html`
    <section
      id="lens-${id}"
      class="dash-section"
      hx-get="/lens/${id}"
      hx-trigger="${trigger}"
      hx-swap="outerHTML"
    >
      <div class="dash-lens-hdr">
        <span class="tag">${tag}</span>
        <div class="rule"></div>
      </div>
      <div class="lens-placeholder">
        <span class="ph-label">${title}</span>
        <span class="ph-note">loading…</span>
      </div>
    </section>
  `;
}

// ---------------------------------------------------------------------------
// Shell page
// ---------------------------------------------------------------------------
function DashboardShell({
  crumbs,
  hash,
  date,
}: {
  crumbs: Crumb[];
  hash: string;
  date: string;
}) {
  return html`<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Momentum Cycle</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- Google Fonts: Inter · Source Serif 4 · JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />

  <!-- HTMX -->
  <script src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js"></script>

  <style>
    :root {
      --paper:           ${tokens.paper};
      --paperAlt:        ${tokens.paperAlt};
      --rule:            ${tokens.rule};
      --ruleStrong:      ${tokens.ruleStrong};
      --ink:             ${tokens.ink};
      --inkMuted:        ${tokens.inkMuted};
      --inkQuiet:        ${tokens.inkQuiet};
      --inkFaint:        ${tokens.inkFaint};
      --readingPaper:    ${tokens.readingPaper};
      --readingPaperAlt: ${tokens.readingPaperAlt};
      --readingRule:     ${tokens.readingRule};
      --accent:          ${tokens.accent};
      --accentSoft:      ${tokens.accentSoft};
      --gap:             ${tokens.gap};
      --gapSoft:         ${tokens.gapSoft};
      --paperDark:       ${tokens.paperDark};
      --paperDarkAlt:    ${tokens.paperDarkAlt};
      --ruleDark:        ${tokens.ruleDark};
      --ruleDarkStrong:  ${tokens.ruleDarkStrong};
      --inkOnDark:       ${tokens.inkOnDark};
      --inkOnDarkMuted:  ${tokens.inkOnDarkMuted};
      --inkOnDarkQuiet:  ${tokens.inkOnDarkQuiet};
      --inkOnDarkFaint:  ${tokens.inkOnDarkFaint};
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body {
      height: 100%;
      background: var(--paperDark);
      font-family: "Inter", system-ui, sans-serif;
      color: var(--inkOnDark);
      -webkit-font-smoothing: antialiased;
    }

    /* ── App shell ── */
    .app-shell {
      display: flex;
      flex-direction: column;
      height: 100%;
      background: var(--paperDark);
      color: var(--inkOnDark);
      border-color: var(--ruleDark);
    }

    /* ── Top brand bar ── */
    .top-bar {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      padding: 14px 20px 12px;
      border-bottom: 1px solid var(--ruleDark);
      flex-shrink: 0;
    }

    .top-bar .brand {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 17px;
      font-weight: 500;
      letter-spacing: -0.3px;
      color: var(--inkOnDark);
    }

    .top-bar .meta {
      font-family: "JetBrains Mono", monospace;
      font-size: 9.5px;
      color: var(--inkOnDarkFaint);
      letter-spacing: 0.3px;
    }

    /* ── Breadcrumb bar ── */
    .crumb-bar {
      padding: 8px 20px 10px;
      border-bottom: 1px solid var(--ruleDark);
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 36px;
      flex-shrink: 0;
    }

    .crumb-bar .crumbs {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: "JetBrains Mono", monospace;
      font-size: 11px;
      letter-spacing: 0.3px;
    }

    .crumb-bar .seg {
      color: var(--inkOnDarkQuiet);
      text-decoration: none;
      cursor: pointer;
      text-transform: lowercase;
      transition: color 0.12s;
    }
    .crumb-bar .seg:hover { color: var(--inkOnDark); }
    .crumb-bar .seg.here {
      color: var(--accent);
      font-weight: 500;
      cursor: default;
    }
    .crumb-bar .sep {
      color: var(--inkOnDarkFaint);
      font-family: "JetBrains Mono", monospace;
    }

    /* ── Scrollable body ── */
    .pane-body {
      flex: 1;
      overflow-y: auto;
    }

    /* ── Lens sections ── */
    .dash-section {
      padding: 14px 20px 12px;
      border-bottom: 1px solid var(--ruleDark);
    }
    .dash-section:last-child { border-bottom: none; }

    .dash-lens-hdr {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 10px;
    }
    .dash-lens-hdr .tag {
      font-family: "JetBrains Mono", monospace;
      font-size: 9.5px;
      letter-spacing: 1.3px;
      text-transform: uppercase;
      color: var(--inkOnDarkQuiet);
    }
    .dash-lens-hdr .rule {
      flex: 1;
      height: 1px;
      background: var(--ruleDark);
    }

    /* ── Lens placeholder state ── */
    .lens-placeholder {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 0 8px;
    }
    .ph-label {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 14px;
      font-style: italic;
      color: var(--inkOnDarkMuted);
    }
    .ph-note {
      font-family: "JetBrains Mono", monospace;
      font-size: 9.5px;
      color: var(--inkOnDarkFaint);
      letter-spacing: 0.3px;
    }

    /* ── HTMX loading indicator ── */
    .htmx-request .ph-note::after { content: " ⋯"; }
  </style>
</head>
<body>
  <div class="app-shell">

    <!-- Brand header -->
    <header class="top-bar">
      <span class="brand">Momentum Cycle</span>
      <span class="meta">#${hash} · ${date}</span>
    </header>

    <!-- Breadcrumb nav (only ancestors left of current + current) -->
    ${Breadcrumbs({ crumbs })}

    <!-- Scrollable lens area -->
    <main class="pane-body">
      ${LensSection({ id: "features", tag: "Features", title: "Features", poll: true })}
      ${LensSection({ id: "sprint",   tag: "Sprint",   title: "Sprint"   })}
      ${LensSection({ id: "cycle",    tag: "Cycle",    title: "Cycle"    })}
    </main>

  </div>
</body>
</html>`;
}

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------
const app = new Hono();

// Root — render full shell
app.get("/", (c) => {
  const crumbs: Crumb[] = [{ label: "dashboard", href: "/" }];
  return c.html(
    DashboardShell({ crumbs, hash: shortHash(), date: isoDate() }) as string
  );
});

// ---------------------------------------------------------------------------
// Features lens route — Task 1 (reads features.json + stories/index.json)
// ---------------------------------------------------------------------------
app.get("/lens/features", async (c) => {
  const features = await readFeaturesJson();
  const stories = await readStoriesIndex();
  const rows = buildSortedRows(features, stories);
  const tableBody = renderFeaturesTable(rows);

  return c.html(`
    <section id="lens-features" class="dash-section"
      hx-get="/lens/features"
      hx-trigger="every 2s"
      hx-swap="outerHTML"
    >
      <div class="dash-lens-hdr">
        <span class="tag">Features</span>
        <div class="rule"></div>
      </div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-size:12px;">
          <thead>
            <tr style="border-bottom:1px solid var(--ruleDarkStrong,rgba(255,252,245,0.18));">
              <th style="padding:6px 10px;text-align:left;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:0.8px;text-transform:uppercase;color:var(--inkOnDarkQuiet,rgba(240,238,233,0.48));font-weight:500;">Feature</th>
              <th style="padding:6px 10px;text-align:left;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:0.8px;text-transform:uppercase;color:var(--inkOnDarkQuiet,rgba(240,238,233,0.48));font-weight:500;">Status</th>
              <th style="padding:6px 10px;text-align:left;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:0.8px;text-transform:uppercase;color:var(--inkOnDarkQuiet,rgba(240,238,233,0.48));font-weight:500;">Stories</th>
              <th style="padding:6px 10px;text-align:left;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:0.8px;text-transform:uppercase;color:var(--inkOnDarkQuiet,rgba(240,238,233,0.48));font-weight:500;">Done</th>
            </tr>
          </thead>
          <tbody>
            ${tableBody}
          </tbody>
        </table>
      </div>
    </section>
  `);
});

app.get("/lens/sprint", (c) => {
  return c.html(`
    <section id="sprint" class="dash-section">
      <div class="dash-lens-hdr">
        <span class="tag">Sprint</span>
        <div class="rule"></div>
      </div>
      <div class="lens-placeholder">
        <span class="ph-label">Sprint lens</span>
        <span class="ph-note">not yet implemented</span>
      </div>
    </section>
  `);
});

app.get("/lens/cycle", (c) => {
  return c.html(`
    <section id="cycle" class="dash-section">
      <div class="dash-lens-hdr">
        <span class="tag">Cycle</span>
        <div class="rule"></div>
      </div>
      <div class="lens-placeholder">
        <span class="ph-label">Cycle lens</span>
        <span class="ph-note">not yet implemented</span>
      </div>
    </section>
  `);
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
const PORT = 3456;
console.log(`Momentum Cycle dashboard → http://localhost:${PORT}`);

export default {
  port: PORT,
  fetch: app.fetch,
};
