/**
 * Momentum Cycle Dashboard — Hono+Bun server
 *
 * Start: bun --hot skills/momentum/dashboard/server.tsx
 * Port:  3456
 */

import { Hono } from "hono";
import { html } from "hono/html";
import { join } from "path";

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
}: {
  id: string;
  tag: string;
  title: string;
}) {
  return html`
    <section
      id="${id}"
      class="dash-section"
      hx-get="/lens/${id}"
      hx-trigger="load"
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
// Data helpers — sprint + stories index
// ---------------------------------------------------------------------------

interface SprintEntry {
  slug: string;
  status: string;
  locked?: boolean;
  stories: string[];
  started?: string;
  planned?: string;
  completed?: string | null;
  retro_run_at?: string | null;
}

interface SprintsIndex {
  active: SprintEntry | null;
  planning?: SprintEntry | null;
  completed?: SprintEntry[];
}

interface StoryEntry {
  status: string;
  title: string;
  epic_slug?: string;
  [key: string]: unknown;
}

interface StoriesIndex {
  [slug: string]: StoryEntry;
}

async function readSprintsIndex(): Promise<SprintsIndex | null> {
  try {
    const projectRoot = process.cwd();
    const file = Bun.file(join(projectRoot, ".momentum", "sprints", "index.json"));
    if (!(await file.exists())) return null;
    return (await file.json()) as SprintsIndex;
  } catch {
    return null;
  }
}

async function readStoriesIndex(): Promise<StoriesIndex | null> {
  try {
    const projectRoot = process.cwd();
    const file = Bun.file(join(projectRoot, ".momentum", "stories", "index.json"));
    if (!(await file.exists())) return null;
    return (await file.json()) as StoriesIndex;
  } catch {
    return null;
  }
}

type BandName = "blocked" | "in-progress" | "validated";

function getStoryBand(status: string): BandName | null {
  if (status === "blocked" || status === "closed-incomplete") return "blocked";
  if (status === "in-progress" || status === "review" || status === "verify") return "in-progress";
  if (status === "done") return "validated";
  return null; // backlog, ready-for-dev — omitted
}

// ---------------------------------------------------------------------------
// Sprint lens components
// ---------------------------------------------------------------------------

function SprintCard({ sprint }: { sprint: SprintEntry }) {
  const retroDone = sprint.retro_run_at != null;
  const closureColor = retroDone ? "#4ade80" : "#f59e0b";
  const closureLabel = retroDone ? "Retro done" : "Retro pending";
  const startDate = sprint.started ?? sprint.planned ?? "—";

  return html`
    <div
      class="sprint-card"
      hx-get="/sprints/${sprint.slug}"
      hx-target="#main-content"
      hx-push-url="/sprints/${sprint.slug}"
      style="cursor:pointer;"
    >
      <div class="sprint-card-slug">${sprint.slug}</div>
      <div class="sprint-card-meta">
        <span class="sprint-card-date">started ${startDate}</span>
        <span
          class="sprint-closure-badge"
          style="color:${closureColor};"
        >${closureLabel}</span>
      </div>
    </div>
  `;
}

function SprintLensSection({ sprint }: { sprint: SprintEntry | null }) {
  const body = sprint
    ? SprintCard({ sprint })
    : html`<div class="sprint-empty">No active sprint — run /momentum:sprint-planning to start one.</div>`;

  return html`
    <section
      id="sprint"
      class="dash-section"
      hx-get="/lenses/sprint"
      hx-trigger="every 2s"
      hx-swap="outerHTML"
    >
      <div class="dash-lens-hdr">
        <span class="tag">Sprint</span>
        <div class="rule"></div>
      </div>
      ${body}
    </section>
  `;
}

// ---------------------------------------------------------------------------
// Sprint detail components
// ---------------------------------------------------------------------------

const BAND_CONFIG: Record<BandName, { label: string; borderColor: string; badgeColor: string; emptyLabel: string }> = {
  blocked: {
    label: "Blocked",
    borderColor: "#ef4444",
    badgeColor: "#ef4444",
    emptyLabel: "No blocked stories",
  },
  "in-progress": {
    label: "In Progress",
    borderColor: "#f59e0b",
    badgeColor: "#f59e0b",
    emptyLabel: "No in-progress stories",
  },
  validated: {
    label: "Validated",
    borderColor: "#4ade80",
    badgeColor: "#4ade80",
    emptyLabel: "No validated stories",
  },
};

function SprintStoryRow({ slug, title, status, band }: { slug: string; title: string; status: string; band: BandName }) {
  const badgeColor = BAND_CONFIG[band].badgeColor;
  return html`
    <div
      class="story-row"
      hx-get="/stories/${slug}?from=sprint"
      hx-target="#main-content"
      hx-push-url="/stories/${slug}?from=sprint"
      style="cursor:pointer;"
    >
      <span class="story-row-title">${title}</span>
      <span class="story-row-badge" style="color:${badgeColor}; border-color:${badgeColor};">${status}</span>
    </div>
  `;
}

function SprintDetailBand({
  band,
  stories,
}: {
  band: BandName;
  stories: Array<{ slug: string; title: string; status: string }>;
}) {
  const cfg = BAND_CONFIG[band];
  const rows =
    stories.length > 0
      ? stories.map((s) => SprintStoryRow({ slug: s.slug, title: s.title, status: s.status, band }))
      : [html`<div class="band-empty">${cfg.emptyLabel}</div>`];

  return html`
    <div
      class="sprint-band"
      style="border-left:3px solid ${cfg.borderColor}; padding-left:12px; margin-bottom:16px;"
    >
      <div class="band-label">${cfg.label}</div>
      ${rows}
    </div>
  `;
}

function SprintDetailView({
  sprint,
  bands,
}: {
  sprint: SprintEntry;
  bands: Record<BandName, Array<{ slug: string; title: string; status: string }>>;
}) {
  const startDate = sprint.started ?? sprint.planned ?? "—";
  // OOB breadcrumb is a sibling to the primary content; HTMX extracts it before swapping.
  // Primary content is placed into #main-content (innerHTML swap).
  return html`
    <!-- Breadcrumb OOB swap — HTMX processes this before inserting into target -->
    <nav id="breadcrumb" class="crumb-bar" hx-swap-oob="true">
      <div class="crumbs">
        <a
          class="seg"
          hx-get="/"
          hx-target="#main-content"
          hx-push-url="/"
          style="cursor:pointer;"
        >dashboard</a>
        <span class="sep">/</span>
        <span class="seg here">sprint</span>
      </div>
    </nav>

    <!-- Sprint detail content (primary payload → goes into #main-content) -->
    <div class="dash-section">
      <div class="dash-lens-hdr">
        <span class="tag">Sprint</span>
        <div class="rule"></div>
      </div>
      <div class="sprint-detail-hdr">
        <span class="sprint-detail-slug">${sprint.slug}</span>
        <span class="sprint-detail-date">started ${startDate}</span>
      </div>
      ${SprintDetailBand({ band: "blocked", stories: bands.blocked })}
      ${SprintDetailBand({ band: "in-progress", stories: bands["in-progress"] })}
      ${SprintDetailBand({ band: "validated", stories: bands.validated })}
    </div>
  `;
}

// ---------------------------------------------------------------------------
// Shell page
// ---------------------------------------------------------------------------
function DashboardShell({
  hash,
  date,
  sprintSection,
}: {
  hash: string;
  date: string;
  sprintSection?: unknown;
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

    /* ── Sprint lens card ── */
    .sprint-card {
      padding: 12px 0 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .sprint-card:hover { opacity: 0.85; }
    .sprint-card-slug {
      font-family: "JetBrains Mono", monospace;
      font-size: 13px;
      font-weight: 500;
      color: var(--inkOnDark);
    }
    .sprint-card-meta {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .sprint-card-date {
      font-family: "JetBrains Mono", monospace;
      font-size: 10px;
      color: var(--inkOnDarkQuiet);
    }
    .sprint-closure-badge {
      font-family: "JetBrains Mono", monospace;
      font-size: 10px;
      font-weight: 500;
    }
    .sprint-empty {
      padding: 16px 0 8px;
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 13px;
      font-style: italic;
      color: var(--inkOnDarkMuted);
    }

    /* ── Sprint detail view ── */
    .sprint-detail-hdr {
      display: flex;
      align-items: baseline;
      gap: 16px;
      padding: 8px 0 16px;
    }
    .sprint-detail-slug {
      font-family: "JetBrains Mono", monospace;
      font-size: 14px;
      font-weight: 500;
      color: var(--inkOnDark);
    }
    .sprint-detail-date {
      font-family: "JetBrains Mono", monospace;
      font-size: 10px;
      color: var(--inkOnDarkQuiet);
    }
    .sprint-band {
      margin-bottom: 16px;
    }
    .band-label {
      font-family: "JetBrains Mono", monospace;
      font-size: 9.5px;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: var(--inkOnDarkQuiet);
      margin-bottom: 6px;
    }
    .band-empty {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 12px;
      font-style: italic;
      color: var(--inkOnDarkFaint);
      padding: 4px 0;
    }
    .story-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 8px;
      margin-bottom: 2px;
      border-radius: 3px;
      background: var(--paperDarkAlt);
    }
    .story-row:hover { background: rgba(255,252,245,0.06); }
    .story-row-title {
      font-family: "Inter", system-ui, sans-serif;
      font-size: 12px;
      color: var(--inkOnDark);
    }
    .story-row-badge {
      font-family: "JetBrains Mono", monospace;
      font-size: 9px;
      letter-spacing: 0.5px;
      border: 1px solid;
      border-radius: 3px;
      padding: 1px 5px;
      white-space: nowrap;
    }
  </style>
</head>
<body>
  <div class="app-shell">

    <!-- Brand header -->
    <header class="top-bar">
      <span class="brand">Momentum Cycle</span>
      <span class="meta">#${hash} · ${date}</span>
    </header>

    <!-- Breadcrumb nav -->
    <nav id="breadcrumb" class="crumb-bar">
      <div class="crumbs">
        <span class="seg here">dashboard</span>
      </div>
    </nav>

    <!-- Scrollable lens area (HTMX main-content swap target) -->
    <div id="main-content" style="flex:1; overflow-y:auto;">
      ${LensSection({ id: "features", tag: "Features", title: "Features" })}
      ${sprintSection ?? SprintLensSection({ sprint: null })}
      ${LensSection({ id: "cycle",    tag: "Cycle",    title: "Cycle"    })}
    </div>

  </div>
</body>
</html>`;
}

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------
const app = new Hono();

// Root — full shell or HTMX partial (based on HX-Request header)
app.get("/", async (c) => {
  const sprintsIndex = await readSprintsIndex();
  const activeSprint = sprintsIndex?.active ?? null;
  const sprintSection = SprintLensSection({ sprint: activeSprint });

  // HTMX fragment request: return lens content + breadcrumb OOB reset
  if (c.req.header("HX-Request")) {
    return c.html(`
      <!-- Reset breadcrumb OOB -->
      <nav id="breadcrumb" class="crumb-bar" hx-swap-oob="true">
        <div class="crumbs">
          <span class="seg here">dashboard</span>
        </div>
      </nav>
      <!-- Dashboard lens sections (primary payload → #main-content innerHTML) -->
      ${LensSection({ id: "features", tag: "Features", title: "Features" }) as string}
      ${sprintSection as string}
      ${LensSection({ id: "cycle", tag: "Cycle", title: "Cycle" }) as string}
    `);
  }

  // Full page load
  return c.html(
    DashboardShell({ hash: shortHash(), date: isoDate(), sprintSection }) as string
  );
});

// Lens placeholder endpoints — features and cycle will be fleshed out in follow-on stories
app.get("/lens/features", (c) => {
  return c.html(`
    <section id="features" class="dash-section">
      <div class="dash-lens-hdr">
        <span class="tag">Features</span>
        <div class="rule"></div>
      </div>
      <div class="lens-placeholder">
        <span class="ph-label">Features lens</span>
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

// Sprint lens — live-polling endpoint (every 2s)
app.get("/lenses/sprint", async (c) => {
  const sprintsIndex = await readSprintsIndex();
  const activeSprint = sprintsIndex?.active ?? null;
  return c.html(SprintLensSection({ sprint: activeSprint }) as string);
});

// Sprint detail drill-down
app.get("/sprints/:slug", async (c) => {
  const sprintsIndex = await readSprintsIndex();
  const activeSprint = sprintsIndex?.active ?? null;

  // Only the active sprint is drillable for now
  if (!activeSprint) {
    return c.html(`
      <nav id="breadcrumb" class="crumb-bar" hx-swap-oob="true">
        <div class="crumbs">
          <a class="seg" hx-get="/" hx-target="#main-content" hx-push-url="/" style="cursor:pointer;">dashboard</a>
          <span class="sep">/</span>
          <span class="seg here">sprint</span>
        </div>
      </nav>
      <div class="dash-section">
        <div class="sprint-empty">No active sprint found.</div>
      </div>
    `);
  }

  const storiesIndex = await readStoriesIndex();
  const bands: Record<BandName, Array<{ slug: string; title: string; status: string }>> = {
    blocked: [],
    "in-progress": [],
    validated: [],
  };

  for (const slug of activeSprint.stories) {
    const entry = storiesIndex?.[slug];
    if (!entry) continue;
    const band = getStoryBand(entry.status);
    if (!band) continue; // backlog / ready-for-dev — omit
    bands[band].push({ slug, title: entry.title, status: entry.status });
  }

  return c.html(SprintDetailView({ sprint: activeSprint, bands }) as string);
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
