/**
 * Momentum Cycle Dashboard — Hono+Bun server
 *
 * Start: bun --hot skills/momentum/skills/canvas/server.tsx
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
  value_analysis?: string;
  system_context?: string;
  description?: string;
  dependencies?: string[];
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

async function readFeatureBySlug(slug: string): Promise<Feature | null> {
  try {
    const file = Bun.file("_bmad-output/planning-artifacts/features.json");
    if (!(await file.exists())) return null;
    const data = await file.json();
    if (!data || typeof data !== "object") return null;
    const feature = (data as Record<string, Feature>)[slug];
    return feature ?? null;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Features lens — status badge CSS class (Task 4)
// ---------------------------------------------------------------------------

/**
 * Returns the CSS class name for a status badge (matches reference design .badge.{class}).
 */
function badgeClass(status: string): string {
  // Map status values to their CSS class names
  const classMap: Record<string, string> = {
    working: "working",
    partial: "partial",
    "not-working": "not-started", // maps to same visual as not-started in reference
    "not-started": "not-started",
    "in-progress": "in-progress",
    blocked: "blocked",
    "ready-for-dev": "ready-for-dev",
    validated: "validated",
  };
  return classMap[status] ?? "not-started";
}

/** @deprecated Use badgeClass instead — kept for compatibility with FeatureDetailView */
function badgeColor(status: string): string {
  const colors: Record<string, string> = {
    working: "var(--accent, #5863a8)",
    partial: "#d97706",
    "not-working": "#dc2626",
    "not-started": "#6b7280",
  };
  return colors[status] ?? "#6b7280";
}

// ---------------------------------------------------------------------------
// Features lens — HTML renderer (Tasks 3, 4)
// ---------------------------------------------------------------------------

function renderFeaturesTable(rows: FeatureRow[]): string {
  if (rows.length === 0) {
    return `<div class="feat-row" style="padding:12px 0;">
  <span class="feat-name" style="font-style:italic;color:var(--inkOnDarkMuted);">No features found — run momentum:feature-grooming first</span>
</div>`;
  }

  return rows
    .map((row, idx) => {
      const done = row.stories_done;
      const total = row.total;
      const isLast = idx === rows.length - 1;
      const lastClass = isLast ? " last" : "";
      const gapBg = row.has_gap ? ` style="background:rgba(168,90,42,0.16);"` : "";
      // Third column: gap-flag for gap rows, badge for non-gap
      const rightCol = row.has_gap
        ? `<span class="gap-flag prominent">⚠ gap</span>`
        : `<span class="badge ${badgeClass(row.status)}"><span class="dot"></span>${row.status}</span>`;

      return `<a class="feat-row${lastClass}" href="/features/${row.feature_slug}"${gapBg}>
  <span class="feat-name">${row.name}</span>
  <span class="frac">${done}<span class="slash">/</span>${total}</span>
  ${rightCol}
</a>`;
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
// Git hash — computed once at startup
// ---------------------------------------------------------------------------
let GIT_HASH = "no-git";
try {
  const result = Bun.spawnSync(["git", "rev-parse", "--short", "HEAD"]);
  if (result.exitCode === 0) {
    GIT_HASH = new TextDecoder().decode(result.stdout).trim();
  }
} catch {}

// ---------------------------------------------------------------------------
// Meta helpers
// ---------------------------------------------------------------------------
function shortHash(): string {
  return GIT_HASH;
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
      hx-get="/lenses/${id}"
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

interface SprintStoryEntry {
  status: string;
  title: string;
  epic_slug?: string;
  [key: string]: unknown;
}

interface StoriesIndex {
  [slug: string]: SprintStoryEntry;
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

async function readStoriesIndexRaw(): Promise<StoriesIndex | null> {
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
    <a
      class="sprint-card"
      href="/sprints/${sprint.slug}"
      style="cursor:pointer;text-decoration:none;color:inherit;display:block;"
    >
      <div class="sprint-card-slug">${sprint.slug}</div>
      <div class="sprint-card-meta">
        <span class="sprint-card-date">started ${startDate}</span>
        <span
          class="sprint-closure-badge"
          style="color:${closureColor};"
        >${closureLabel}</span>
      </div>
    </a>
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
// Feature L2 detail view — reading mode
// ---------------------------------------------------------------------------

const STORY_STATUS_ICON: Record<string, string> = {
  done: "✓",
  "in-progress": "◎",
  review: "◑",
  blocked: "✗",
  backlog: "○",
  "ready-for-dev": "◌",
};

function storyStatusIcon(status: string): string {
  return STORY_STATUS_ICON[status] ?? "○";
}

const STORY_BADGE_COLORS: Record<string, string> = {
  done: "#4ade80",
  "in-progress": "#f59e0b",
  review: "#60a5fa",
  blocked: "#ef4444",
  backlog: "#9ca3af",
  "ready-for-dev": "#a78bfa",
};

function storyBadgeColor(status: string): string {
  return STORY_BADGE_COLORS[status] ?? "#9ca3af";
}

export function buildFeatureStoryRows(
  feature: Feature,
  storyMap: StoryMap
): Array<{ slug: string; title: string; status: string; featureSlug: string }> {
  const slugs = feature.stories ?? [];
  const rows = slugs.map((slug) => {
    const entry = storyMap[slug];
    return {
      slug,
      title: entry?.title ?? slug,
      status: entry?.status ?? "backlog",
      featureSlug: feature.feature_slug,
    };
  });
  const STATUS_ORDER = ['in-progress', 'review', 'verify', 'ready-for-dev', 'backlog', 'done'];
  rows.sort((a, b) => {
    const ai = STATUS_ORDER.indexOf(a.status);
    const bi = STATUS_ORDER.indexOf(b.status);
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  });
  return rows;
}

function FeatureStoryRow({ slug, title, status, featureSlug }: { slug: string; title: string; status: string; featureSlug: string }) {
  const storyUrl = `/stories/${slug}?from=feature&feature=${featureSlug}`;
  return html`
    <a
      class="story click"
      href="${storyUrl}"
      hx-get="${storyUrl}"
      hx-target="#main-content"
      hx-swap="innerHTML"
      hx-push-url="${storyUrl}"
    >
      <span class="t">${title}</span>
      <span class="badge ${badgeClass(status)}"><span class="dot"></span>${status}</span>
    </a>
  `;
}

export function FeatureDetailView({
  feature,
  storyRows,
}: {
  feature: Feature;
  storyRows: Array<{ slug: string; title: string; status: string }>;
}) {
  const done = feature.stories_done;
  const total = feature.stories_done + feature.stories_remaining;
  const badgeStyle = `background:${badgeColor(feature.status)};`;
  const deps = feature.dependencies ?? [];

  const storyRowsHtml = storyRows.length > 0
    ? storyRows.map((r) => FeatureStoryRow(r)).join("")
    : `<div style="font-family:'Source Serif 4',serif;font-size:14px;font-style:italic;color:var(--inkMuted);">No stories linked</div>`;

  const depsHtml = deps.length > 0
    ? `<ul class="reading-deps-list">${deps.map((d) => `<li>${escapeHtml(d)}</li>`).join("")}</ul>`
    : `<div style="font-family:'Source Serif 4',serif;font-size:14px;font-style:italic;color:var(--inkMuted);">No dependencies</div>`;

  const typeTag = (feature as any).type ? `<span class="type-tag">${escapeHtml((feature as any).type)}</span>` : "";
  const hasGap = feature.stories_done === 0 && feature.status !== "working";

  return html`
    <!-- Breadcrumb OOB swap — light mode crumb bar -->
    <nav id="breadcrumb" class="crumb-bar reading-crumb-bar" hx-swap-oob="true">
      <div class="crumbs">
        <a class="seg" href="/">dashboard</a>
        <span class="sep">›</span>
        <span class="seg here">feature</span>
      </div>
      <span class="reading-pill"><span class="rd"></span>reading mode</span>
    </nav>

    <!-- Feature detail content -->
    <div class="reading-surface">
      <div class="l2-body">

        <!-- l2-meta strip -->
        <div class="l2-meta">
          <span class="badge ${badgeClass(feature.status)}"><span class="dot"></span>${feature.status}</span>
          <span class="frac">${done}<span class="slash">/</span>${total}<span class="lbl">stories</span></span>
          ${raw(typeTag)}
          ${hasGap ? html`<span class="gap-flag prominent">gap</span>` : ""}
        </div>

        <!-- Title -->
        <h1 class="l2-name">${feature.name}</h1>

        <!-- Short description -->
        ${feature.description ? html`<div class="l2-desc">${feature.description}</div>` : ""}

        <!-- Value narrative -->
        ${feature.value_analysis ? html`
          <div class="l2-section-cap">value narrative</div>
          <div class="l2-narrative"><p>${feature.value_analysis}</p></div>
        ` : ""}

        <!-- Acceptance condition -->
        ${feature.acceptance_condition ? html`
          <div class="l2-section-cap">acceptance condition</div>
          <div class="reading-ac-box">${feature.acceptance_condition}</div>
        ` : ""}

        <!-- System context -->
        ${feature.system_context ? html`
          <div class="l2-section-cap">system context</div>
          <div class="reading-callout">${feature.system_context}</div>
        ` : ""}

        <!-- Stories list -->
        <div class="l2-section-cap">stories · ${total} · click to open</div>
        <div class="l2-stories">${raw(storyRowsHtml)}</div>

        ${deps.length > 0 ? html`
          <div class="l2-section-cap">dependencies</div>
          ${raw(depsHtml)}
        ` : ""}

      </div>
    </div>
  `;
}

// ---------------------------------------------------------------------------
// Sprint detail components
// ---------------------------------------------------------------------------

const BAND_CONFIG: Record<BandName, { label: string; borderColor: string; emptyLabel: string }> = {
  blocked: {
    label: "blocked",
    borderColor: "rgba(168,90,42,0.6)",
    emptyLabel: "No blocked stories",
  },
  "in-progress": {
    label: "in progress",
    borderColor: "var(--accent)",
    emptyLabel: "No in-progress stories",
  },
  validated: {
    label: "validated",
    borderColor: "rgba(106,122,106,0.7)",
    emptyLabel: "No validated stories",
  },
};

function SprintStoryRow({ slug, title, status }: { slug: string; title: string; status: string; band: BandName }) {
  return html`
    <a
      class="story-row click"
      href="/stories/${slug}?from=sprint"
      hx-get="/stories/${slug}?from=sprint"
      hx-target="#main-content"
      hx-push-url="/stories/${slug}?from=sprint"
    >
      <span class="story-row-title">${title}</span>
      <span class="badge ${badgeClass(status)}"><span class="dot"></span>${status}</span>
    </a>
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
      <div class="band-hdr">
        <span class="lbl">${cfg.label}</span>
        ${stories.length > 0 ? html`<span class="n">${stories.length}</span>` : ""}
      </div>
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
    <!-- Breadcrumb OOB swap -->
    <nav id="breadcrumb" class="crumb-bar" hx-swap-oob="true">
      <div class="crumbs">
        <a class="seg" href="/">dashboard</a>
        <span class="sep">›</span>
        <span class="seg here">sprint</span>
      </div>
      <span class="sprint-crumb-date">started ${startDate}</span>
    </nav>

    <!-- Sprint detail content -->
    <div class="dash-section dark-surface">
      <div class="sprint-detail-key">${sprint.slug}</div>
      <span class="sprint-lifecycle"><span class="sd"></span>active · started ${startDate}</span>
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
  mainContent,
  navHtml,
}: {
  hash: string;
  date: string;
  sprintSection?: unknown;
  cycleSection?: unknown;
  mainContent?: string;
  navHtml?: string;
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
    /* ── Design tokens ── */
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
    }

    /* ── Top brand bar ── */
    .top-bar {
      display: flex; align-items: baseline; justify-content: space-between;
      padding: 14px 20px 12px;
      border-bottom: 1px solid var(--ruleDark);
      flex-shrink: 0;
    }
    .top-bar .brand {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 17px; font-weight: 500; letter-spacing: -0.3px;
      color: var(--inkOnDark);
    }
    .top-bar .meta {
      font-family: "JetBrains Mono", monospace;
      font-size: 13px; color: var(--inkOnDarkFaint); letter-spacing: 0.3px;
    }

    /* ── Breadcrumb bar ── */
    .crumb-bar {
      padding: 8px 20px 10px;
      border-bottom: 1px solid var(--ruleDark);
      display: flex; align-items: center; justify-content: space-between;
      min-height: 36px;
      flex-shrink: 0;
    }
    .crumb-bar .crumbs {
      display: inline-flex; align-items: center; gap: 8px;
      font-family: "JetBrains Mono", monospace;
      font-size: 13px; letter-spacing: 0.3px;
    }
    .crumb-bar .seg {
      color: var(--inkOnDarkQuiet);
      text-decoration: none; cursor: pointer;
      text-transform: lowercase;
      transition: color 0.12s;
    }
    .crumb-bar .seg:hover { color: var(--inkOnDark); }
    .crumb-bar .seg.here {
      color: var(--accent); font-weight: 500; cursor: default;
    }
    .crumb-bar .sep {
      color: var(--inkOnDarkFaint);
      font-family: "JetBrains Mono", monospace;
    }

    /* ── Lens sections ── */
    .dash-section {
      padding: 14px 20px 12px;
      border-bottom: 1px solid var(--ruleDark);
    }
    .dash-section:last-child { border-bottom: none; }

    .dash-lens-hdr {
      display: flex; align-items: center; gap: 8px; margin-bottom: 10px;
    }
    .dash-lens-hdr .tag {
      font-family: "JetBrains Mono", monospace; font-size: 13px;
      letter-spacing: 1.3px; text-transform: uppercase;
      color: var(--inkOnDarkQuiet);
    }
    .dash-lens-hdr .rule { flex: 1; height: 1px; background: var(--ruleDark); }
    .dash-lens-hdr .count {
      font-family: "JetBrains Mono", monospace; font-size: 13px;
      color: var(--inkOnDarkFaint);
    }

    /* ── Lens placeholder state ── */
    .lens-placeholder {
      display: flex; align-items: center; gap: 12px;
      padding: 16px 0 8px;
    }
    .ph-label {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 14px; font-style: italic;
      color: var(--inkOnDarkMuted);
    }
    .ph-note {
      font-family: "JetBrains Mono", monospace;
      font-size: 13px; color: var(--inkOnDarkFaint); letter-spacing: 0.3px;
    }
    .htmx-request .ph-note::after { content: " ⋯"; }

    /* ── Badges — light mode (default), dark mode via .dark-surface prefix ── */
    .badge {
      display: inline-flex; align-items: center; gap: 5px;
      padding: 1px 7px 1px 5px;
      font-family: "JetBrains Mono", monospace;
      font-size: 11px; font-weight: 500; letter-spacing: 0.2px;
      border-radius: 3px; white-space: nowrap;
    }
    .badge .dot { width: 5px; height: 5px; border-radius: 50%; }
    /* Light-mode badge palette (reading surfaces) */
    .badge.working { color: #2a5a42; background: rgba(62,122,90,0.10); }
    .badge.working .dot { background: #3e7a5a; }
    .badge.partial { color: #7a5e1a; background: rgba(168,131,40,0.11); }
    .badge.partial .dot { background: #a88328; }
    .badge.not-started { color: #5a5a5a; background: rgba(138,138,138,0.10); }
    .badge.not-started .dot { background: #8a8a8a; }
    .badge.in-progress { color: #2a4a7a; background: rgba(88,99,168,0.10); }
    .badge.in-progress .dot { background: #5863a8; }
    .badge.validated { color: #556555; background: rgba(106,122,106,0.08); }
    .badge.validated .dot { background: #6a7a6a; }
    .badge.blocked { color: #7a4020; background: rgba(168,90,42,0.10); }
    .badge.blocked .dot { background: #a85a2a; }
    .badge.ready-for-dev { color: #2a4a7a; background: rgba(88,99,168,0.10); }
    .badge.ready-for-dev .dot { background: #5863a8; }
    /* Dark-mode badge palette (dark scanning surfaces) */
    .dark-surface .badge.working { color: #8fd1a9; background: rgba(62,122,90,0.18); }
    .dark-surface .badge.partial { color: #e6c07a; background: rgba(168,131,40,0.18); }
    .dark-surface .badge.not-started { color: rgba(240,238,233,0.72); background: rgba(240,238,233,0.07); }
    .dark-surface .badge.in-progress { color: #a4b0e0; background: rgba(88,99,168,0.22); }
    .dark-surface .badge.validated { color: rgba(192,200,188,0.85); background: rgba(106,122,106,0.14); }
    .dark-surface .badge.blocked { color: #e0a07a; background: rgba(168,90,42,0.18); }
    .dark-surface .badge.ready-for-dev { color: #a4b0e0; background: rgba(88,99,168,0.22); }

    /* ── Gap flag ── */
    .gap-flag {
      display: inline-flex; align-items: center; gap: 4px;
      padding: 1px 6px 1px 5px;
      font-family: "JetBrains Mono", monospace;
      font-size: 13px; font-weight: 500;
      color: #e8a070; letter-spacing: 0.2px;
      border-radius: 3px; white-space: nowrap;
      background: rgba(168,90,42,0.25);
      border: 1px solid rgba(168,90,42,0.50);
    }

    /* ── Fraction (story count) ── */
    .frac {
      font-family: "JetBrains Mono", monospace;
      font-size: 14px; color: var(--inkOnDarkMuted);
    }
    .frac .slash { color: var(--inkOnDarkFaint); }
    .frac .lbl { color: var(--inkOnDarkFaint); margin-left: 4px; font-size: 13px; }

    /* ── Features list — grid rows ── */
    .feat-list { padding: 4px 0 2px; }
    .feat-row {
      display: grid; grid-template-columns: 1fr auto auto;
      align-items: center; gap: 10px;
      padding: 5px 4px 5px 0; border-bottom: 1px dashed var(--ruleDark);
      text-decoration: none; color: inherit; cursor: pointer;
    }
    .feat-row:last-child,
    .feat-row.last { border-bottom: none; }
    .feat-row:hover { background: rgba(255,252,245,0.04); }
    .feat-name {
      font-family: "Inter", sans-serif; font-size: 15px;
      color: var(--inkOnDark); line-height: 1.35;
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }

    /* ── Sprint lens card ── */
    .sprint-card {
      padding: 10px 14px;
      background: rgba(88,99,168,0.12);
      border-left: 2px solid var(--accent);
      cursor: pointer; display: block; text-decoration: none; color: inherit;
    }
    .sprint-card:hover { opacity: 0.85; }
    .sprint-card-slug {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 14px; font-weight: 500; color: var(--inkOnDark);
      letter-spacing: -0.2px;
    }
    .sprint-card-meta {
      display: flex; align-items: center; gap: 16px; margin-top: 6px;
    }
    .sprint-card-date {
      font-family: "JetBrains Mono", monospace;
      font-size: 12px; color: var(--inkOnDarkQuiet);
    }
    .sprint-closure-badge {
      font-family: "JetBrains Mono", monospace;
      font-size: 12px; font-weight: 500;
    }
    .sprint-empty {
      padding: 16px 0 8px;
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 15px; font-style: italic;
      color: var(--inkOnDarkMuted);
    }

    /* ── Cycle timeline ── */
    .cycle-line {
      position: relative; height: 56px; margin: 8px 0 4px;
    }
    .cycle-line::before {
      content: ""; position: absolute;
      left: 0; right: 0; top: 8px; height: 1px;
      background: var(--ruleDark);
    }
    .cycle-nodes {
      position: relative;
      display: grid; grid-template-columns: repeat(7, 1fr);
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
      font-size: 12px; letter-spacing: 0.4px;
      color: var(--inkOnDarkQuiet); text-transform: lowercase;
      line-height: 1.2; white-space: pre-line;
    }
    .cycle-node.done .dot { background: var(--accent); border-color: var(--accent); }
    .cycle-node.done .lbl { color: var(--inkOnDark); }
    .cycle-node.skipped .dot { background: var(--paperDark); border-color: var(--ruleDarkStrong); }
    .cycle-node.skipped .lbl { color: var(--inkOnDarkFaint); opacity: 0.45; }
    .cycle-node.next .dot {
      background: var(--paperDark); border-color: var(--accent); border-width: 2px;
      box-shadow: 0 0 0 3px rgba(88,99,168,0.18);
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
      font-size: 13px; color: var(--inkOnDarkMuted); letter-spacing: 0.3px;
    }
    .cycle-summary .tag {
      color: var(--inkOnDarkFaint); letter-spacing: 1.2px; text-transform: uppercase;
      font-size: 11px; margin-right: 4px;
    }
    .cycle-summary .v { color: var(--inkOnDark); }
    .cycle-summary .now { color: var(--accent); font-weight: 500; }

    /* ── Sprint detail view ── */
    .sprint-crumb-date {
      font-family: "JetBrains Mono", monospace;
      font-size: 9px; color: var(--inkOnDarkFaint); margin-left: auto;
    }
    .sprint-detail-key {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 20px; font-weight: 500; letter-spacing: -0.2px;
      color: var(--inkOnDark); margin-bottom: 6px;
    }
    .sprint-lifecycle {
      display: inline-flex; align-items: center; gap: 5px;
      padding: 1px 7px 1px 6px; margin-bottom: 14px;
      font-family: "JetBrains Mono", monospace; font-size: 11px;
      color: #a4b0e0; background: rgba(88,99,168,0.22);
      border-radius: 3px;
    }
    .sprint-lifecycle .sd { width: 5px; height: 5px; border-radius: 50%; background: var(--accent); }
    .band-hdr {
      display: flex; align-items: baseline; gap: 6px; margin-bottom: 6px;
    }
    .band-hdr .lbl {
      font-family: "JetBrains Mono", monospace;
      font-size: 11px; letter-spacing: 1.2px;
      color: var(--inkOnDarkMuted);
    }
    .band-hdr .n {
      font-family: "JetBrains Mono", monospace;
      font-size: 11px; color: var(--inkOnDarkFaint);
    }
    .story-row.click .story-row-title { color: #a4b0e0; }
    .sprint-detail-hdr {
      display: flex; align-items: baseline; gap: 16px;
      padding: 8px 0 16px;
    }
    .sprint-detail-slug {
      font-family: "JetBrains Mono", monospace;
      font-size: 14px; font-weight: 500; color: var(--inkOnDark);
    }
    .sprint-detail-date {
      font-family: "JetBrains Mono", monospace;
      font-size: 12px; color: var(--inkOnDarkQuiet);
    }
    .sprint-band { margin-bottom: 16px; }
    .band-label {
      font-family: "JetBrains Mono", monospace;
      font-size: 11px; letter-spacing: 1.2px; text-transform: uppercase;
      margin-bottom: 6px;
    }
    .band-empty {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 14px; font-style: italic;
      color: var(--inkOnDarkFaint); padding: 4px 0;
    }

    /* Story rows in sprint detail */
    .story-row {
      display: grid; grid-template-columns: 1fr auto;
      align-items: center; gap: 8px;
      padding: 5px 0; border-bottom: 1px solid var(--ruleDark);
      text-decoration: none; color: inherit;
    }
    .story-row:last-child { border-bottom: none; }
    .story-row:hover { opacity: 0.85; }
    .story-row-title {
      font-family: "Inter", sans-serif; font-size: 15px;
      color: var(--inkOnDark); line-height: 1.35;
    }
    .story-row-badge {
      font-family: "JetBrains Mono", monospace;
      font-size: 11px; letter-spacing: 0.5px;
      border: 1px solid; border-radius: 3px;
      padding: 1px 5px; white-space: nowrap;
    }

    /* ── Reading mode — warm light polarity ── */
    .reading-surface {
      background: var(--readingPaper);
      color: var(--ink);
      animation: fadeInLight 140ms ease forwards;
      min-height: 100%;
      padding: 24px 20px 40px;
    }
    @keyframes fadeInLight {
      from { background: var(--paperDark, #16140f); }
      to { background: var(--readingPaper, #faf6ec); }
    }

    /* Breadcrumb override for reading mode */
    .reading-crumb-bar {
      background: var(--readingPaper);
      border-bottom: 1px solid var(--readingRule);
      transition: background 140ms ease;
    }
    .reading-crumb-bar .seg { color: var(--inkMuted); }
    .reading-crumb-bar .seg:hover { color: var(--ink); }
    .reading-crumb-bar .seg.here { color: var(--accent); }
    .reading-crumb-bar .sep { color: var(--inkFaint); }

    /* Feature L2 reading ── */
    .l2-body { padding: 16px 20px 18px; }
    .l2-meta {
      display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
      margin-bottom: 6px;
    }
    .l2-name {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 22px; line-height: 1.2; font-weight: 500;
      letter-spacing: -0.3px; color: var(--ink); margin: 4px 0 6px;
    }
    .l2-desc {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 15px; line-height: 1.5; color: var(--inkMuted);
      font-style: italic; max-width: 56ch;
    }
    .l2-section-cap {
      margin-top: 16px; margin-bottom: 6px;
      font-family: "JetBrains Mono", monospace; font-size: 12px;
      letter-spacing: 1.3px; text-transform: uppercase; color: var(--inkQuiet);
    }
    .l2-narrative p {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 13.5px; line-height: 1.65; color: var(--ink);
      margin: 0 0 8px; max-width: 60ch;
    }
    .l2-body { padding: 16px 20px 40px; }
    .type-tag {
      font-family: "JetBrains Mono", monospace;
      font-size: 9px; letter-spacing: 1.2px; text-transform: uppercase;
      color: var(--inkQuiet); background: var(--readingPaperAlt);
      padding: 1px 6px; border-radius: 2px;
    }
    .l2-stories .story, .l2-stories a.story {
      display: grid; grid-template-columns: 1fr auto;
      align-items: center; gap: 8px;
      padding: 5px 0; border-bottom: 1px solid var(--readingRule);
      text-decoration: none; color: inherit;
    }
    .l2-stories .story .t {
      font-family: "Inter", sans-serif; font-size: 15px; color: var(--ink);
    }
    .l2-stories .story.click .t {
      color: var(--accent); font-weight: 500; cursor: pointer;
    }
    .l2-stories .story:last-child { border-bottom: none; }

    /* Feature heading */
    .feature-heading {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 24px; font-weight: 600;
      color: var(--ink); letter-spacing: -0.4px;
      margin-bottom: 10px; line-height: 1.3;
    }

    /* Meta strip */
    .feature-meta-strip {
      display: flex; align-items: center; gap: 12px;
      flex-wrap: wrap; margin-bottom: 24px;
      font-family: "JetBrains Mono", monospace; font-size: 12px;
    }
    .feature-meta-badge {
      padding: 2px 8px; border-radius: 3px;
      color: #fff; font-size: 13px; letter-spacing: 0.5px;
    }
    .feature-meta-fraction { color: var(--inkMuted); }
    .feature-reading-label {
      color: var(--inkQuiet); font-size: 11px;
      letter-spacing: 0.8px; text-transform: uppercase;
    }

    /* Reading column */
    .reading-col { max-width: 65ch; }
    .reading-section { margin-top: 1.5rem; }

    /* Section labels */
    .reading-section-label {
      font-family: "JetBrains Mono", monospace;
      font-size: 13px; letter-spacing: 1.2px; text-transform: uppercase;
      color: var(--inkQuiet); margin-bottom: 8px; margin-top: 28px;
    }

    /* Value narrative prose */
    .reading-prose {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 18px; line-height: 1.70; color: var(--ink);
    }

    /* Acceptance condition box */
    .reading-ac-box {
      border-left: 3px solid var(--accent);
      background: var(--readingPaperAlt);
      padding: 12px 16px; border-radius: 0 4px 4px 0;
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 15px; line-height: 1.60; color: var(--ink);
    }

    /* System context callout */
    .reading-callout {
      background: var(--readingPaperAlt);
      border: 1px solid var(--readingRule);
      border-radius: 4px; padding: 12px 16px;
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 15px; line-height: 1.60; color: var(--inkMuted);
    }

    /* Stories list in reading mode */
    .reading-story-row {
      display: flex; align-items: center; justify-content: space-between;
      padding: 7px 10px; margin-bottom: 3px;
      border-radius: 4px; background: var(--readingPaperAlt);
      cursor: pointer; text-decoration: none;
    }
    .reading-story-row:hover { background: var(--readingRule); }
    .reading-story-title {
      font-family: "Inter", system-ui, sans-serif;
      font-size: 15px; color: var(--ink);
      display: flex; align-items: center; gap: 8px;
    }
    .reading-story-badge {
      font-family: "JetBrains Mono", monospace;
      font-size: 11px; letter-spacing: 0.5px;
      border: 1px solid; border-radius: 3px;
      padding: 1px 5px; white-space: nowrap;
    }
    .status-icon { font-size: 13px; line-height: 1; }

    /* Dependencies list */
    .reading-deps-list { list-style: none; padding: 0; margin: 0; }
    .reading-deps-list li {
      font-family: "Inter", system-ui, sans-serif;
      font-size: 15px; color: var(--inkMuted);
      padding: 4px 0; border-bottom: 1px solid var(--readingRule);
    }
    .reading-deps-list li:last-child { border-bottom: none; }

    /* ── Story L3 reading mode ── */
    .l3 { padding: 16px 20px 18px; }
    .l3-fm {
      margin-top: 0; padding: 7px 10px;
      background: var(--readingPaperAlt);
      border: 1px solid var(--readingRule);
      display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
      font-family: "JetBrains Mono", monospace;
      font-size: 12px; letter-spacing: 0.3px; color: var(--inkMuted);
    }
    .l3-fm .fk { color: var(--inkFaint); margin-right: 3px; }
    .l3-fm .fv { color: var(--ink); }
    .l3-fm .midot { color: var(--inkFaint); }
    .reading-pill {
      display: inline-flex; align-items: center; gap: 5px;
      font-family: "JetBrains Mono", monospace;
      font-size: 11px; letter-spacing: 0.6px; color: var(--inkMuted);
      margin-left: auto;
    }
    .reading-pill .rd {
      width: 7px; height: 7px; border-radius: 50%;
      background: var(--accent); opacity: 0.6;
    }
    .l3-title {
      margin: 14px 0 5px;
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 24px; line-height: 1.2; font-weight: 500;
      letter-spacing: -0.3px; color: var(--ink);
    }
    .l3-subtitle {
      font-family: "Source Serif 4", Georgia, serif;
      font-style: italic; font-size: 14px; line-height: 1.4;
      color: var(--inkMuted); margin-bottom: 14px; max-width: 56ch;
    }
    .l3 p.body {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 13.5px; line-height: 1.7; color: var(--ink);
      max-width: 62ch; margin: 0 0 9px;
    }
    .l3 h3.sec {
      margin: 16px 0 8px; padding-bottom: 4px;
      border-bottom: 1px solid var(--readingRule);
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 13.5px; font-weight: 500; color: var(--ink);
      display: flex; align-items: baseline; justify-content: space-between;
    }
    .l3 ol.num { list-style: none; padding: 0; margin: 0; counter-reset: acn; }
    .l3 ol.num > li {
      counter-increment: acn;
      display: grid; grid-template-columns: 24px 1fr;
      column-gap: 10px; padding: 6px 0 7px;
      border-bottom: 1px solid var(--readingRule);
    }
    .l3 ol.num > li::before {
      content: counter(acn, decimal-leading-zero);
      font-family: "JetBrains Mono", monospace;
      font-size: 11px; color: var(--inkFaint); padding-top: 3px;
    }
    .l3 ol.num .num-body {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 12.5px; line-height: 1.55; color: var(--ink); max-width: 56ch;
    }

    .story-meta-strip {
      display: flex; align-items: center; gap: 8px;
      flex-wrap: wrap; margin-bottom: 16px;
      font-family: "JetBrains Mono", monospace; font-size: 12px;
    }
    .story-meta-slug {
      color: var(--inkMuted); font-size: 12px; letter-spacing: 0.3px;
      max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }
    .story-meta-chip {
      padding: 2px 7px; border: 1px solid var(--readingRule);
      border-radius: 3px; color: var(--inkMuted);
      font-size: 13px; letter-spacing: 0.4px; white-space: nowrap;
    }
    .story-meta-status {
      background: var(--accentSoft); border-color: var(--accent); color: var(--accent);
    }
    .story-meta-derives { font-size: 11px; color: var(--inkFaint); letter-spacing: 0.3px; }
    .story-narrative { line-height: 1.70; }
    .story-ac-list { list-style: decimal; padding-left: 1.4em; margin: 0; }
    .story-ac-list li {
      font-family: "Source Serif 4", Georgia, serif;
      font-size: 18px; line-height: 1.70; color: var(--ink); padding: 3px 0;
    }
    .story-ac-list li + li { border-top: 1px solid var(--readingRule); }
    .story-dev-notes { font-size: 15px; line-height: 1.60; color: var(--inkMuted); font-style: italic; }
    .story-touches-list { list-style: none; padding: 0; margin: 0; }
    .story-touches-list li {
      padding: 4px 0; border-bottom: 1px solid var(--readingRule);
    }
    .story-touches-list li:last-child { border-bottom: none; }
    .story-touch-path {
      font-family: "JetBrains Mono", monospace; font-size: 13px;
      color: var(--inkMuted); background: var(--readingPaperAlt);
      padding: 1px 5px; border-radius: 3px;
    }
  </style>
</head>
<body>
  <div class="app-shell">

    <!-- Brand header -->
    <header class="top-bar">
      <span class="brand">Momentum Cycle</span>
      <span class="meta">${date} · hash ${hash.slice(0, 4)}</span>
    </header>

    <!-- Breadcrumb nav -->
    ${navHtml != null ? raw(navHtml) : html`<nav id="breadcrumb" class="crumb-bar">
      <div class="crumbs">
        <span class="seg here">dashboard</span>
      </div>
    </nav>`}

    <!-- Scrollable lens area (HTMX main-content swap target) -->
    <div id="main-content" style="flex:1; overflow-y:auto;">
      ${mainContent != null ? raw(mainContent) : html`
      ${cycleSection ?? LensSection({ id: "cycle",    tag: "Cycle",    title: "Cycle"    })}
      ${sprintSection ?? SprintLensSection({ sprint: null })}
      ${LensSection({ id: "features", tag: "Features", title: "Features" })}
      `}
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
      ${cycleSection as string}
      ${sprintSection as string}
      ${LensSection({ id: "features", tag: "Features", title: "Features" }) as string}
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
app.get("/lenses/features", async (c) => {
  const features = await readFeaturesJson();
  const stories = (await readStoriesIndex()) ?? {};
  const rows = buildSortedRows(features, stories);
  const tableBody = renderFeaturesTable(rows);
  return c.html(`
    <section id="lens-features" class="dash-section"
      hx-get="/lenses/features"
      hx-trigger="every 2s"
      hx-swap="outerHTML"
    >
      <div class="dash-lens-hdr">
        <span class="tag">Features</span>
        <div class="rule"></div>
        <span class="count">${rows.length}${rows.filter(r => r.has_gap).length > 0 ? ` · ${rows.filter(r => r.has_gap).length} gap${rows.filter(r => r.has_gap).length > 1 ? 's' : ''}` : ''}</span>
      </div>
      <div class="feat-list">
        ${tableBody}
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
  const requestedSlug = c.req.param("slug");
  const sprintsIndex = await readSprintsIndex();
  const activeSprint = sprintsIndex?.active ?? null;

  // Validate that the requested slug matches the active sprint
  if (!activeSprint || activeSprint.slug !== requestedSlug) {
    return c.html(`
      <nav id="breadcrumb" class="crumb-bar" hx-swap-oob="true">
        <div class="crumbs">
          <a class="seg" href="/">dashboard</a>
          <span class="sep">›</span>
          <span class="seg here">sprint</span>
        </div>
      </nav>
      <div class="dash-section">
        <div class="sprint-empty">${activeSprint ? `Sprint "${requestedSlug}" not found — only the active sprint is available.` : "No active sprint found."}</div>
      </div>
    `);
  }

  const storiesIndex = await readStoriesIndexRaw();
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

  const fragmentHtml = SprintDetailView({ sprint: activeSprint, bands }) as string;
  const isHtmx = !!c.req.header("HX-Request");
  if (isHtmx) return c.html(fragmentHtml);

  // Direct browser navigation — wrap in full shell
  const sprintContent = fragmentHtml.replace(/<nav id="breadcrumb"[^>]*hx-swap-oob="true"[\s\S]*?<\/nav>/m, "").trim();
  const sprintNavHtml = `<nav id="breadcrumb" class="crumb-bar"><div class="crumbs"><a class="seg" href="/">dashboard</a><span class="sep">›</span><span class="seg here">sprint</span></div><span class="sprint-crumb-date">started ${activeSprint.started ?? activeSprint.planned ?? "—"}</span></nav>`;
  return c.html(DashboardShell({ hash: shortHash(), date: isoDate(), mainContent: sprintContent, navHtml: sprintNavHtml }) as string);
});

// ---------------------------------------------------------------------------
// Story L3 — data reader and markdown parser
// ---------------------------------------------------------------------------

export interface StoryMeta {
  title: string;
  story_key: string;
  status: string;
  epic_slug?: string;
  feature_slug?: string;
  story_type?: string;
  derives_from?: string;
  [key: string]: string | undefined;
}

export interface ParsedStory {
  meta: StoryMeta;
  storyNarrative: string;       // First prose paragraph from ## Description (not user-story line)
  acceptanceCriteria: string[]; // Numbered list items
  devNotes: string;             // Full Dev Notes section text
  workflowSection: string;      // ## Workflow section or frontmatter workflow field
  touches: string[];            // File list from touches
}

/**
 * Parse YAML-like frontmatter block (--- ... ---) from a markdown string.
 * Returns a flat record of key: value strings.
 */
export function parseFrontmatter(source: string): Record<string, string> {
  const result: Record<string, string> = {};
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return result;

  const block = match[1];
  for (const line of block.split(/\r?\n/)) {
    const colonIdx = line.indexOf(":");
    if (colonIdx < 0) continue;
    const key = line.slice(0, colonIdx).trim();
    const val = line.slice(colonIdx + 1).trim();
    if (key) result[key] = val;
  }
  return result;
}

/**
 * Extract a markdown section by heading (e.g., "## Acceptance Criteria").
 * Returns the text between that heading and the next same-level (or higher) heading.
 */
export function extractSection(source: string, heading: string): string {
  // Determine heading level
  const levelMatch = heading.match(/^(#{1,6})\s/);
  const level = levelMatch ? levelMatch[1].length : 2;

  // Escape special chars for regex
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  // Match the heading and capture everything until next heading of same or higher level
  const sectionRe = new RegExp(
    `${escaped}\\s*\\r?\\n([\\s\\S]*?)(?=\\n#{1,${level}}\\s|$)`,
    "i"
  );
  const m = source.match(sectionRe);
  return m ? m[1].trim() : "";
}

/**
 * Parse numbered or bulleted list items from a text block.
 * Returns an array of item strings (markup stripped).
 */
export function parseListItems(text: string): string[] {
  const items: string[] = [];
  const lineRe = /^\s*(?:\d+\.\s+|-\s+|\*\s+)(.+)$/;
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(lineRe);
    if (m) items.push(m[1].trim());
  }
  return items;
}

/**
 * Parse touches array from the YAML frontmatter (multi-line list format).
 * The raw frontmatter value may be empty; the actual lines follow as "  - path".
 */
function parseTouchesFromSource(source: string): string[] {
  const touches: string[] = [];
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return touches;

  const block = match[1];
  const lines = block.split(/\r?\n/);
  let inTouches = false;
  for (const line of lines) {
    if (/^touches\s*:/.test(line)) {
      inTouches = true;
      continue;
    }
    if (inTouches) {
      const itemMatch = line.match(/^\s+-\s+(.+)/);
      if (itemMatch) {
        touches.push(itemMatch[1].trim());
      } else if (line.match(/^\S/)) {
        // New top-level key — stop
        inTouches = false;
      }
    }
  }
  return touches;
}

/**
 * Parse a Momentum story markdown file into structured data.
 */
export function parseStoryMarkdown(source: string): ParsedStory {
  const fm = parseFrontmatter(source);
  const touches = parseTouchesFromSource(source);

  // If no frontmatter found, extract title from first H1 and inline Status field
  if (!fm["title"] && !fm["story_key"]) {
    const h1 = source.match(/^#\s+(.+)$/m);
    if (h1) fm["title"] = h1[1].trim();
    const statusMatch = source.match(/^Status:\s*(.+)$/mi);
    if (statusMatch) fm["status"] = statusMatch[1].trim();
    const epicMatch = source.match(/^Epic:\s*(.+)$/mi);
    if (epicMatch) fm["epic_slug"] = epicMatch[1].trim();
    const featureMatch = source.match(/^Feature:\s*(.+)$/mi);
    if (featureMatch) fm["feature_slug"] = featureMatch[1].trim();
  }

  const meta: StoryMeta = {
    title: fm["title"] ?? "",
    story_key: fm["story_key"] ?? "",
    status: fm["status"] ?? "backlog",
    epic_slug: fm["epic_slug"],
    feature_slug: fm["feature_slug"],
    story_type: fm["story_type"],
    derives_from: fm["derives_from"],
  };

  // Extract narrative from ## Description section — first prose paragraph only
  // Skip "As a ..." user-story lines, list items, and headings
  const descriptionSection = extractSection(source, "## Description");
  let storyNarrative = "";
  if (descriptionSection) {
    const paragraphs = descriptionSection.split(/\n\n+/);
    for (const para of paragraphs) {
      const trimmed = para.trim();
      if (!trimmed) continue;
      if (trimmed.startsWith("As a ")) continue;          // user-story line
      if (/^[-*]/.test(trimmed)) continue;                 // list item
      if (/^\d+\./.test(trimmed)) continue;                // numbered list
      if (trimmed.startsWith("#")) continue;               // heading
      storyNarrative = trimmed;
      break;
    }
  }

  // Acceptance criteria section
  const acSection = extractSection(source, "## Acceptance Criteria");
  const acceptanceCriteria = parseListItems(acSection).filter(
    (item) => !item.startsWith("_") && !item.startsWith("<!--")
  );

  // Dev Notes section
  const devNotes = extractSection(source, "## Dev Notes");

  // Workflow section — body or frontmatter fallback
  const bodyWorkflow = extractSection(source, "## Workflow");
  const workflowSection = bodyWorkflow || fm["workflow"] || "";

  return { meta, storyNarrative, acceptanceCriteria, devNotes, workflowSection, touches };
}

async function readStoryBySlug(slug: string): Promise<ParsedStory | null> {
  try {
    const projectRoot = process.cwd();
    const file = Bun.file(join(projectRoot, ".momentum", "stories", `${slug}.md`));
    if (!(await file.exists())) return null;
    const source = await file.text();
    return parseStoryMarkdown(source);
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Story L3 detail view — reading mode (warm light, same polarity as Feature L2)
// ---------------------------------------------------------------------------

export function StoryDetailView({
  story,
  from,
  activeSprintSlug,
  featureSlugOverride,
}: {
  story: ParsedStory;
  from: "feature" | "sprint" | null;
  activeSprintSlug?: string | null;
  featureSlugOverride?: string | null;
}) {
  const { meta, storyNarrative, acceptanceCriteria, devNotes, workflowSection, touches } = story;

  // Breadcrumb path depends on entry point
  let breadcrumbMiddle: string;
  if (from === "sprint") {
    if (activeSprintSlug) {
      breadcrumbMiddle = `<a class="seg" href="/sprints/${activeSprintSlug}">sprint</a><span class="sep">›</span>`;
    } else {
      breadcrumbMiddle = `<a class="seg" href="/">sprint</a><span class="sep">›</span>`;
    }
  } else if (from === "feature") {
    // Use URL-passed feature slug first, then frontmatter, then fallback to dashboard
    const featureSlug = featureSlugOverride || meta.feature_slug;
    if (featureSlug) {
      breadcrumbMiddle = `<a class="seg" href="/features/${featureSlug}">feature</a><span class="sep">›</span>`;
    } else {
      breadcrumbMiddle = `<a class="seg" href="/">feature</a><span class="sep">›</span>`;
    }
  } else {
    breadcrumbMiddle = "";
  }

  const acListHtml =
    acceptanceCriteria.length > 0
      ? `<ol class="story-ac-list">${acceptanceCriteria
          .map((item) => `<li>${escapeHtml(item)}</li>`)
          .join("")}</ol>`
      : `<div style="font-family:'Source Serif 4',serif;font-size:14px;font-style:italic;color:var(--inkMuted);">No acceptance criteria found</div>`;

  const touchesHtml =
    touches.length > 0
      ? `<ul class="story-touches-list">${touches
          .map((t) => `<li><code class="story-touch-path">${escapeHtml(t)}</code></li>`)
          .join("")}</ul>`
      : "";

  // Strip markdown formatting (_italic_, **bold**, `code`) for display
  const cleanDevNotes = devNotes
    .replace(/\*\*(.+?)\*\*/g, "$1")
    .replace(/_(.+?)_/g, "$1")
    .replace(/`(.+?)`/g, "$1")
    .replace(/#{1,6}\s/g, "");

  // Count block-level elements to decide whether to collapse dev notes
  const devNoteParagraphs = cleanDevNotes.split(/\n\n+/).filter((p) => p.trim().length > 0);
  const devNoteListItems = cleanDevNotes.split(/\n/).filter((l) => /^\s*(?:[-*]|\d+\.)\s/.test(l));
  const shouldCollapseByItems = devNoteListItems.length > 3;
  const shouldCollapseByParagraphs = devNoteParagraphs.filter(
    (p) => !p.trim().startsWith("-") && !p.trim().startsWith("*")
  ).length > 1;
  const devNotesShouldCollapse = shouldCollapseByItems || shouldCollapseByParagraphs || cleanDevNotes.length > 400;
  const devNotesInner = `<div class="reading-callout story-dev-notes">${escapeHtml(cleanDevNotes)}</div>`;
  const devNotesHtml = devNotesShouldCollapse
    ? `<details><summary>Dev Notes (click to expand)</summary>${devNotesInner}</details>`
    : devNotesInner;

  return html`
    <!-- Breadcrumb OOB swap — light mode crumb bar for story reading -->
    <nav id="breadcrumb" class="crumb-bar reading-crumb-bar" hx-swap-oob="true">
      <div class="crumbs">
        <a class="seg" href="/">dashboard</a>
        <span class="sep">›</span>
        ${raw(breadcrumbMiddle)}
        <span class="seg here">story</span>
      </div>
      <span class="reading-pill"><span class="rd"></span>reading mode</span>
    </nav>

    <!-- Story detail content (primary payload → goes into #main-content) -->
    <div class="reading-surface">
      <div class="reading-col">

        <!-- Frontmatter meta strip (l3-fm) -->
        <div class="l3-fm">
          <span class="badge ${badgeClass(meta.status)}"><span class="dot"></span>${meta.status}</span>
          ${meta.epic_slug
            ? html`<span><span class="fk">epic</span><span class="fv">${meta.epic_slug}</span></span>`
            : ""}
          ${meta.epic_slug && meta.story_type
            ? html`<span class="midot">·</span>`
            : ""}
          ${meta.story_type
            ? html`<span><span class="fk">type</span><span class="fv">${meta.story_type}</span></span>`
            : ""}
        </div>

        <!-- Title -->
        <h1 class="l3-title">${meta.title || meta.story_key}</h1>

        <!-- Subtitle / value narrative -->
        ${storyNarrative
          ? html`<div class="l3-subtitle">${storyNarrative}</div>`
          : acceptanceCriteria.length === 0
            ? html`<div class="l3-subtitle" style="font-style:italic;color:var(--inkMuted);">This story is a backlog stub — no description yet.</div>`
            : ""}

        <!-- Acceptance criteria -->
        ${acceptanceCriteria.length > 0
          ? html`
            <div class="reading-section-label">Acceptance Criteria</div>
            ${raw(acListHtml)}
          `
          : ""}

        <!-- Dev notes (collapsed if complex) -->
        ${devNotes && cleanDevNotes
          ? html`
            <div class="reading-section-label">Dev Notes</div>
            ${raw(devNotesHtml)}
          `
          : ""}

        <!-- Workflow section -->
        ${workflowSection
          ? html`
            <div class="reading-section">
              <div class="reading-section-label">Workflow</div>
              <div class="reading-col reading-prose">${workflowSection}</div>
            </div>
          `
          : ""}

        <!-- File list -->
        ${touches.length > 0
          ? html`
            <div class="reading-section-label">File List</div>
            ${raw(touchesHtml)}
          `
          : ""}

      </div>
    </div>
  `;
}

/**
 * Escape HTML special characters to prevent XSS in story content.
 */
function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// Story L3 drill-down — reading mode
app.get("/stories/:slug", async (c) => {
  const slug = c.req.param("slug");
  const fromParam = c.req.query("from");
  const featureParam = c.req.query("feature"); // feature slug passed when coming from Feature L2
  const from: "feature" | "sprint" | null =
    fromParam === "feature" ? "feature" : fromParam === "sprint" ? "sprint" : null;

  const story = await readStoryBySlug(slug);

  if (story) {
    if (!story.meta.story_key) story.meta.story_key = slug;
    if (!story.meta.title) story.meta.title = slug.replace(/-/g, ' ');
  }

  if (!story) {
    return c.html(`
      <nav id="breadcrumb" class="crumb-bar reading-crumb-bar" hx-swap-oob="true">
        <div class="crumbs">
          <a class="seg" href="/">dashboard</a>
          <span class="sep">/</span>
          <span class="seg here">story</span>
        </div>
      </nav>
      <div class="reading-surface">
        <div class="reading-col">
          <div style="font-family:'Source Serif 4',serif;font-size:16px;font-style:italic;color:var(--inkMuted);padding-top:16px;">
            Story "${escapeHtml(slug)}" not found.
          </div>
        </div>
      </div>
    `);
  }

  // Read active sprint slug for sprint breadcrumb navigation
  let activeSprintSlug: string | null = null;
  if (from === "sprint") {
    const sprintsData = await readSprintsIndex();
    activeSprintSlug = sprintsData?.active?.slug ?? null;
  }

  const storyFragment = StoryDetailView({ story, from, activeSprintSlug, featureSlugOverride: featureParam ?? null }) as string;
  const isHtmx = !!c.req.header("HX-Request");
  if (isHtmx) return c.html(storyFragment);

  // Direct browser navigation — wrap in full shell with reading mode
  const storyContent = storyFragment.replace(/<nav id="breadcrumb"[^>]*hx-swap-oob="true"[\s\S]*?<\/nav>/m, "").trim();
  // Build breadcrumb with correct back-links based on entry point
  const featureSlug = featureParam || story.meta.feature_slug;
  let crumbs = `<a class="seg" href="/">dashboard</a>`;
  if (from === "feature" && featureSlug) {
    crumbs += `<span class="sep">›</span><a class="seg" href="/features/${featureSlug}">feature</a>`;
  } else if (from === "sprint" && activeSprintSlug) {
    crumbs += `<span class="sep">›</span><a class="seg" href="/sprints/${activeSprintSlug}">sprint</a>`;
  }
  crumbs += `<span class="sep">›</span><span class="seg here">story</span>`;
  const storyNavHtml = `<nav id="breadcrumb" class="crumb-bar reading-crumb-bar"><div class="crumbs">${crumbs}</div><span class="reading-pill"><span class="rd"></span>reading mode</span></nav>`;
  return c.html(DashboardShell({ hash: shortHash(), date: isoDate(), mainContent: storyContent, navHtml: storyNavHtml }) as string);
});

// Feature L2 drill-down — reading mode
app.get("/features/:slug", async (c) => {
  const slug = c.req.param("slug");
  const feature = await readFeatureBySlug(slug);
  const isHtmx = !!c.req.header("HX-Request");

  if (!feature) {
    const notFoundFragment = `
      <nav id="breadcrumb" class="crumb-bar" hx-swap-oob="true">
        <div class="crumbs">
          <a class="seg" href="/">dashboard</a>
          <span class="sep">/</span>
          <span class="seg here">feature</span>
        </div>
      </nav>
      <div class="reading-surface">
        <div class="reading-col">
          <div style="font-family:'Source Serif 4',serif;font-size:16px;font-style:italic;color:var(--inkMuted);padding-top:16px;">
            Feature "${escapeHtml(slug)}" not found.
          </div>
        </div>
      </div>
    `;
    if (isHtmx) return c.html(notFoundFragment);
    // Direct navigation — inject not-found content into shell
    const notFoundShell = DashboardShell({ hash: shortHash(), date: isoDate() }) as string;
    // Strip OOB nav tag (contains hx-swap-oob="true") from fragment before injecting
    const notFoundContent = notFoundFragment.replace(/<nav id="breadcrumb"[^>]*hx-swap-oob="true"[\s\S]*?<\/nav>/m, "").trim();
    const notFoundFullHtml = notFoundShell.replace(
      `<div id="main-content" style="flex:1; overflow-y:auto;">`,
      `<div id="main-content" style="flex:1; overflow-y:auto;">${notFoundContent}`
    );
    return c.html(notFoundFullHtml);
  }

  const storyMap = (await readStoriesIndex()) ?? {};
  const storyRows = buildFeatureStoryRows(feature, storyMap);
  const fragmentHtml = FeatureDetailView({ feature, storyRows }) as string;

  if (isHtmx) {
    return c.html(fragmentHtml);
  }

  // Direct browser navigation — wrap in full shell with ONLY the feature content in #main-content
  // Strip OOB nav tag (contains hx-swap-oob="true") from fragment before injecting
  const featureContent = fragmentHtml.replace(/<nav id="breadcrumb"[^>]*hx-swap-oob="true"[\s\S]*?<\/nav>/m, "").trim();
  const featureNavHtml = `<nav id="breadcrumb" class="crumb-bar reading-crumb-bar"><div class="crumbs"><a class="seg" href="/">dashboard</a><span class="sep">›</span><span class="seg here">feature</span></div><span class="reading-pill"><span class="rd"></span>reading mode</span></nav>`;
  return c.html(DashboardShell({
    hash: shortHash(),
    date: isoDate(),
    mainContent: featureContent,
    navHtml: featureNavHtml,
  }) as string);
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
