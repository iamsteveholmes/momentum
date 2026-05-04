/**
 * Momentum Cycle Dashboard — Hono+Bun server
 *
 * Start: bun --hot skills/momentum/dashboard/server.tsx
 * Port:  3456
 */

import { Hono } from "hono";
import { html, raw } from "hono/html";
import { join } from "path";

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
// Data helpers — sprint + stories index
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Cycle state computation
// ---------------------------------------------------------------------------

export type PhaseState = "done" | "next-required" | "not-run" | "pending";

export interface PhaseInfo {
  slug: string;
  label: string;
  state: PhaseState;
  required: boolean;
}

export interface CycleState {
  phases: PhaseInfo[];
  nextRequired: string | null;
  lastSprintSlug: string | null;
}

const PHASES: Array<{ slug: string; label: string; required: boolean }> = [
  { slug: "triage",          label: "triage",          required: false },
  { slug: "feature-grooming", label: "feat\ngroom",    required: false },
  { slug: "epic-grooming",   label: "epic\ngroom",     required: false },
  { slug: "refine",          label: "refine",          required: false },
  { slug: "sprint-planning", label: "planning",        required: true  },
  { slug: "sprint-dev",      label: "sprint\ndev",     required: true  },
  { slug: "retro",           label: "retro",           required: true  },
];

interface SprintIndexInput {
  active?: { slug: string; status: string; planned?: string; started?: string; retro_run_at?: string | null; stories: string[] } | null;
  planning?: { slug: string; status: string; planned?: string; started?: string; retro_run_at?: string | null; stories: string[] } | null;
  completed?: Array<{ slug: string; status: string; planned?: string; started?: string; retro_run_at?: string | null; stories: string[] }>;
}

/**
 * Pure function — derives cycle phase states from the sprints index.
 *
 * Cycle boundary: the most recent completed sprint with retro_run_at set.
 * Everything after that retro is the "current cycle."
 */
export function computeCycleState(index: SprintIndexInput | null): CycleState {
  const completed = index?.completed ?? [];
  const active = index?.active ?? null;
  const planning = index?.planning ?? null;

  // Find last completed sprint (the most recent in completed array, last element)
  const lastCompleted =
    completed.length > 0 ? completed[completed.length - 1] : null;

  // Most recent sprint with retro_run_at — marks the previous cycle's end
  const lastRetroSprint = [...completed]
    .reverse()
    .find((s) => s.retro_run_at != null) ?? null;

  const lastSprintSlug = lastCompleted?.slug ?? null;

  // Determine which phases have run in the CURRENT cycle.
  // Current cycle = everything after the last completed retro (or from the beginning if no retro).
  //
  // Phase detection for the current cycle:
  //
  // sprint-planning ran  → planning sprint exists (status "planning") OR active sprint has planned field
  // sprint-dev ran       → active sprint exists with started field (status "active" or "done")
  // retro ran            → active sprint has retro_run_at OR a completed sprint (in current cycle) has retro_run_at
  //
  // "Current cycle" sprints:
  //   - the `planning` sprint (if any)
  //   - the `active` sprint (if any)
  //   - completed sprints that came AFTER the last retro sprint

  // Find completed sprints in the current cycle (after last retro)
  let currentCycleCompleted: typeof completed = [];
  if (lastRetroSprint) {
    const retroIdx = completed.findIndex((s) => s.slug === lastRetroSprint.slug);
    currentCycleCompleted = completed.slice(retroIdx + 1);
  } else {
    // No retro ever — all completed sprints are in the current cycle
    currentCycleCompleted = completed;
  }

  // Aggregate evidence for each phase
  const currentCycleSprints = [
    ...currentCycleCompleted,
    ...(planning ? [planning] : []),
    ...(active ? [active] : []),
  ];

  let sprintPlanningDone = false;
  let sprintDevDone = false;
  let retroDone = false;

  for (const s of currentCycleSprints) {
    // sprint-planning: sprint has a planned date (was formally planned)
    if (s.planned) sprintPlanningDone = true;
    // sprint-dev: sprint was actually started (has started date or is/was active)
    if (s.started || s.status === "active" || s.status === "done") sprintDevDone = true;
    // retro: retro_run_at is set
    if (s.retro_run_at) retroDone = true;
  }

  // Build phase states
  // Required phases sequence: sprint-planning → sprint-dev → retro
  // next-required = first required phase that hasn't run yet (if any required phases remain)
  let nextRequiredSlug: string | null = null;
  if (!sprintPlanningDone) nextRequiredSlug = "sprint-planning";
  else if (!sprintDevDone) nextRequiredSlug = "sprint-dev";
  else if (!retroDone) nextRequiredSlug = "retro";
  else nextRequiredSlug = null; // cycle complete

  const phases: PhaseInfo[] = PHASES.map((p) => {
    let state: PhaseState;

    if (p.required) {
      // Determine state for required phases
      if (p.slug === "sprint-planning") {
        state = sprintPlanningDone ? "done" : (nextRequiredSlug === "sprint-planning" ? "next-required" : "pending");
      } else if (p.slug === "sprint-dev") {
        state = sprintDevDone ? "done" : (nextRequiredSlug === "sprint-dev" ? "next-required" : "pending");
      } else {
        // retro
        state = retroDone ? "done" : (nextRequiredSlug === "retro" ? "next-required" : "pending");
      }
    } else {
      // Optional phases: done or not-run only, never next-required
      state = "not-run"; // Optional phases don't leave traces in sprints index
    }

    return { slug: p.slug, label: p.label, state, required: p.required };
  });

  return { phases, nextRequired: nextRequiredSlug, lastSprintSlug };
}

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
// Cycle lens components
// ---------------------------------------------------------------------------

function cycleNodeHtml(p: PhaseInfo): string {
  const stateClass =
    p.state === "done" ? "done" :
    p.state === "next-required" ? "next" :
    p.state === "not-run" ? "not-run" :
    "pending";
  return `<div class="cycle-node ${stateClass}"><div class="dot"></div><div class="lbl">${p.label}</div></div>`;
}

function CycleTimeline({ phases }: { phases: PhaseInfo[] }) {
  const nodesHtml = phases.map(cycleNodeHtml).join("");

  return html`
    <div class="cycle-line">
      <div class="cycle-nodes">
        ${raw(nodesHtml)}
      </div>
    </div>
  `;
}

function CycleStatusLine({
  nextRequired,
  lastSprintSlug,
}: {
  nextRequired: string | null;
  lastSprintSlug: string | null;
}) {
  const nextLabel = nextRequired ?? "none — cycle complete";
  const sprintLabel = lastSprintSlug ?? "none";

  return html`
    <div class="cycle-summary">
      <span><span class="tag">cycle</span><span class="v">started</span></span>
      <span><span class="tag">next required</span><span class="${nextRequired ? "now" : "v"}">${nextLabel}</span></span>
      <span><span class="tag">last sprint</span><span class="v">${sprintLabel}</span></span>
    </div>
  `;
}

function CycleLensSection({ cycleState }: { cycleState: CycleState }) {
  return html`
    <section
      id="cycle"
      class="dash-section"
      hx-get="/lenses/cycle"
      hx-trigger="every 5s"
      hx-swap="outerHTML"
    >
      <div class="dash-lens-hdr">
        <span class="tag">Cycle</span>
        <div class="rule"></div>
      </div>
      ${CycleTimeline({ phases: cycleState.phases })}
      ${CycleStatusLine({ nextRequired: cycleState.nextRequired, lastSprintSlug: cycleState.lastSprintSlug })}
    </section>
  `;
}

// ---------------------------------------------------------------------------
// Shell page
// ---------------------------------------------------------------------------
function DashboardShell({
  hash,
  date,
  sprintSection,
  cycleSection,
}: {
  hash: string;
  date: string;
  sprintSection?: unknown;
  cycleSection?: unknown;
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

    /* ── Cycle timeline ── */
    .cycle-line {
      position: relative;
    }
    .cycle-line::before {
      content: ""; position: absolute;
      left: 0; right: 0; top: 8px; height: 1px;
      background: var(--ruleDark);
    }
    .cycle-nodes {
      position: relative;
      display: grid;
      grid-template-columns: repeat(7, 1fr);
    }
    .cycle-node {
      display: flex; flex-direction: column; align-items: center;
      text-align: center; gap: 4px;
    }
    .cycle-node .dot {
      width: 11px; height: 11px; border-radius: 50%;
      border: 1.5px solid var(--ruleDarkStrong);
      background: var(--paperDark);
      margin-top: 3px; z-index: 1;
    }
    .cycle-node .lbl {
      font-family: "JetBrains Mono", monospace;
      font-size: 8.5px; letter-spacing: 0.4px;
      color: var(--inkOnDarkQuiet); text-transform: lowercase;
      line-height: 1.2; white-space: pre-line;
    }
    .cycle-node.done .dot { background: var(--accent); border-color: var(--accent); }
    .cycle-node.done .lbl { color: var(--inkOnDark); }
    .cycle-node.skipped .dot { background: var(--paperDark); border-color: var(--ruleDarkStrong); }
    .cycle-node.skipped .lbl { color: var(--inkOnDarkFaint); opacity: 0.45; }
    .cycle-node.next .dot {
      background: var(--paperDark); border-color: var(--accent); border-width: 2px;
      box-shadow: 0 0 0 3px rgba(88,99,168,0.30);
    }
    .cycle-node.next .lbl { color: var(--accent); font-weight: 500; }
    .cycle-node.pending .dot { background: var(--paperDark); border-color: var(--ruleDarkStrong); }
    .cycle-node.pending .lbl { color: var(--inkOnDarkFaint); opacity: 0.45; }
    .cycle-node.not-run .dot { background: var(--paperDark); border-color: var(--ruleDarkStrong); }
    .cycle-node.not-run .lbl { color: var(--inkOnDarkFaint); opacity: 0.45; }

    .cycle-summary {
      margin: 10px 0 0;
      display: flex; gap: 18px; flex-wrap: wrap; align-items: baseline;
      font-family: "JetBrains Mono", monospace;
      font-size: 9.5px; color: var(--inkOnDarkMuted); letter-spacing: 0.3px;
    }
    .cycle-summary .tag {
      color: var(--inkOnDarkFaint); letter-spacing: 1.2px; text-transform: uppercase; font-size: 9px;
      margin-right: 4px;
    }
    .cycle-summary .v { color: var(--inkOnDark); }
    .cycle-summary .now { color: var(--accent); font-weight: 500; }

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
      ${cycleSection ?? LensSection({ id: "cycle",    tag: "Cycle",    title: "Cycle"    })}
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
  const cycleState = computeCycleState(sprintsIndex);
  const cycleSection = CycleLensSection({ cycleState });

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
      ${cycleSection as string}
    `);
  }

  // Full page load
  return c.html(
    DashboardShell({ hash: shortHash(), date: isoDate(), sprintSection, cycleSection }) as string
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

// Cycle lens — live-polling endpoint (every 5s)
app.get("/lenses/cycle", async (c) => {
  const sprintsIndex = await readSprintsIndex();
  const cycleState = computeCycleState(sprintsIndex);
  return c.html(CycleLensSection({ cycleState }) as string);
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
