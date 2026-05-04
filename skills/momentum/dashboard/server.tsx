/**
 * Momentum Cycle Dashboard — Hono+Bun server
 *
 * Start: bun --hot skills/momentum/dashboard/server.tsx
 * Port:  3456
 */

import { Hono } from "hono";
import { html } from "hono/html";

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
      ${LensSection({ id: "features", tag: "Features", title: "Features" })}
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

// Lens placeholder endpoints — these will be fleshed out in follow-on stories
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
