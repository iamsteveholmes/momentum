// Real Momentum feature data — from feature-status-redesign-content-sample.md.
// Six features, voice preserved verbatim at the lengths given.

const FEATURES = [
  // ── Working ────────────────────────────────────────────────────
  {
    key: "sprint-planning-to-ready",
    name: "Sprint Planning to Ready Sprint",
    type: "flow",
    state: "working",
    stories: { done: 6, total: 6 },
    lastVerified: "2026-04-11",
    hasGap: false,
    description: "End-to-end sprint planning: backlog in, activated ready-for-dev sprint out.",
    acceptance: "A developer with populated backlog stubs can invoke `momentum:sprint-planning` and receive an activated sprint with validated, Gherkin-specced, ready-for-dev stories — without manually specifying story selection criteria or review flow.",
    valueNarrative: [
      "Sprint planning works. A developer with a backlog can run this skill and emerge with a sprint plan — stories selected, assigned to waves, ready for sprint-dev. The immediate value is real: structure and sequence that would otherwise require manual deliberation across epics, story sizes, and dependencies.",
      "But the full vision goes beyond convenience. The skill synthesizes across the PRD, epics, and story history to produce a plan that reflects strategy, not just logistics. A developer who has been heads-down in implementation can step back, run sprint-planning, and get an outside-in view of what the next highest-leverage work is. That is augmented strategic judgment — not just time savings.",
      "Currently working and actively used. All 6 foundation stories are done.",
    ],
    systemContext: "The ignition for every sprint cycle. All other sprint execution features (orchestration, quality gates, retro) have no starting state without this. Depends on backlog-refinement having kept the backlog clean.",
    storiesList: [
      { title: "Sprint Planning Skill", status: "working" },
      { title: "Sprint Planning Workflow Module", status: "working" },
      { title: "Sprint Workflow Alignment", status: "working" },
      { title: "Sprint Planning Synthesis-First", status: "working" },
      { title: "Mandatory Task Tracking", status: "working" },
      { title: "Gherkin ACs and ATDD Workflow Active", status: "working" },
    ],
    gapNote: "Skill does not yet explain its reasoning. Developer gets a plan but not the \u201Cwhy this sprint over that sprint\u201D narrative. Sprint velocity history is not yet factored in.",
  },

  {
    key: "impetus-session-orientation",
    name: "Impetus Session Orientation — Sprint State and Feature Status",
    type: "connection",
    state: "working",
    stories: { done: 4, total: 4 },
    lastVerified: "2026-04-11",
    hasGap: false,
    description: "Session-start handoff between developer context and AI session — sprint state, in-flight stories, feature summary.",
    acceptance: "A developer opening a new Claude Code session with `momentum:impetus` receives a greeting that shows current sprint name, stories in progress vs done vs remaining, open journal threads (if any), and a feature status summary (cached, with staleness flag if `features.json` has changed since last cache).",
    valueNarrative: [
      "When a developer opens Claude Code mid-sprint, Impetus greets them with sprint state, in-flight stories, and recent activity. This is one of the highest-value features in the current implementation — it is used every single session.",
      "The pain this removes is real and daily: reconstructing \u201Cwhere was I?\u201D from files and git history at every session start. But the value goes beyond pain removal. Orientation is also about confidence — the developer knows the system is aware of its own state. That awareness makes the practice feel coherent rather than fragmented.",
      "Currently fully working. All 4 orientation stories are done. The startup cache makes it fast.",
    ],
    systemContext: "The most-used feature in the practice. Orientation quality at session start determines whether the developer feels grounded or adrift.",
    storiesList: [
      { title: "Impetus Skill Created with Correct Persona and Input Handling", status: "working" },
      { title: "Session Orientation and Thread Management", status: "working" },
      { title: "Impetus Greeting Rewrite", status: "working" },
      { title: "Impetus Feature Status Cache", status: "working" },
    ],
  },

  // ── Partial with gap ───────────────────────────────────────────
  {
    key: "retro-and-flywheel",
    name: "Sprint Retro + Practice Improvement Flywheel",
    type: "flow",
    state: "partial",
    stories: { done: 4, total: 7 },
    lastVerified: "2026-04-11",
    hasGap: true,
    description: "Retro ceremony plus the flywheel — cross-story pattern detection that feeds improvements forward into the practice.",
    acceptance: "A developer can run `momentum:retro` after a sprint and receive a findings document produced from transcript audit (not just milestone logs); at least one retro finding generates a story stub added to the backlog; cross-sprint patterns accumulate in the findings ledger.",
    valueNarrative: [
      "The retro skill closes the sprint loop: findings documented, sprint marked complete, summary written. This works and delivers value — a developer who skips retros loses the reflection that improves future work.",
      "But the larger vision — the flywheel — is where this feature becomes transformative. A developer running sprints without the flywheel is like a craftsperson who never sharpens their tools. The flywheel means that patterns from this sprint feed into better story quality in the next, that recurring mistakes stop recurring, and that the practice accumulates wisdom over time. A developer who runs 10 sprints with the flywheel should be dramatically more effective in sprint 10 than sprint 1 — not because they're personally smarter but because the system they're working within is smarter.",
      "Currently, the retro executes and sprint-summary writes are working. The flywheel accumulation (cross-story pattern detection, findings ledger, practice feedback loop) is not yet implemented.",
    ],
    systemContext: "Closes the sprint loop and feeds forward. Sprint-planning benefits from flywheel accumulation; practice-distillation encodes the patterns the flywheel surfaces. Without retro, each sprint is isolated. With the full flywheel, sprints compound.",
    storiesList: [
      { title: "Retro Skill", status: "working" },
      { title: "Retro Workflow Rewrite", status: "working" },
      { title: "Sprint Boundary Compression", status: "working" },
      { title: "Retro → Triage Handoff", status: "working" },
      { title: "Cross-Story Pattern Detection", status: "not-started" },
      { title: "Findings Ledger Accumulates Quality Findings", status: "not-started" },
      { title: "Flywheel Workflow Explains Issues and Guides Upstream Trace", status: "not-started" },
    ],
    gapNote: "Acceptance condition requires transcript-audit findings with cross-sprint pattern accumulation. Assigned stories cover the retro ceremony (done) but not the flywheel mechanics (3 backlog stories). Retro currently produces findings but they don't yet compound across sprints. The practice-compounds epic — the soul of this feature — is still ahead.",
  },

  // ── Partial, status-drift (all stories done, not promoted) ─────
  {
    key: "feature-status-visibility",
    name: "Feature Status Visibility + Grooming",
    type: "connection",
    state: "partial",
    stories: { done: 5, total: 5 },
    lastVerified: "2026-04-11",
    hasGap: false,
    statusDrift: true,
    description: "The feature dashboard itself — rendered view of all features with coverage, gaps, and grooming means to keep the taxonomy honest.",
    acceptance: "A developer can run `momentum:feature-status` and receive a rendered view showing all features with current status, story coverage counts, and explicit gap flags — and can run `momentum:feature-grooming` to evaluate and update the feature taxonomy itself.",
    valueNarrative: [
      "A developer can see which features are advancing and which have coverage gaps — before committing to a sprint plan. The feature-status HTML artifact works: it shows feature progress, gap indicators, and a dependency graph.",
      "But the deeper value is the shift it creates in how developers think about their work. Without feature visibility, it's easy to complete many stories and advance no features — building depth in some areas while leaving others as permanent stubs. Feature-status makes that pattern visible. The developer sees not just \u201Cwhat's done\u201D but \u201Cwhat's actually progressing toward user value.\u201D",
      "Feature-grooming completes the loop: visibility without grooming means the feature list itself may be wrong. A feature list that doesn't reflect the actual product produces misleading status.",
    ],
    systemContext: "The bridge between story-level progress and feature-level value delivery. Without this, developers can complete 10 stories and advance 0 features — a discouraging pattern this feature makes impossible to overlook.",
    storiesList: [
      { title: "Feature Artifact Schema", status: "working" },
      { title: "Feature Status Skill", status: "working" },
      { title: "Feature Status Practice Path", status: "working" },
      { title: "Impetus Feature Status Cache", status: "working" },
      { title: "Feature Grooming", status: "working" },
    ],
    driftNote: "All 5 stories done. Candidate for promotion to working on next feature-grooming run.",
  },

  // ── Not started, full-blueprint ────────────────────────────────
  {
    key: "practice-knowledge-base",
    name: "Practice Knowledge Base — Project-Local Cold Vault",
    type: "connection",
    state: "not-started",
    stories: { done: 0, total: 3 },
    lastVerified: "2026-04-19",
    hasGap: true,
    description: "Project-local knowledge vault — ingests source docs (Obsidian, llms.txt, research, code trees) and serves them as cold-start context for agents.",
    acceptance: "A developer can run `/momentum:kb-init` and `/momentum:kb-ingest` against a project doc source, then have `/momentum:build-guidelines` produce guidelines that cite specific KB passages.",
    valueNarrative: [
      "Current value: None delivered today. All stories are backlog. Practice relies on ad-hoc file reads and training-data defaults for project context.",
      "Full vision: a developer points Momentum at source material (Obsidian vault, llms.txt, research reports) and KB ingests into a pre-synthesized wiki — queryable via grep on an index. build-guidelines uses it to produce stack-specific guidelines with citation integrity. Research skills ground findings against project reality. Agents receive KB queries as cold context on spawn. The practice becomes genuinely project-aware.",
    ],
    systemContext: "Infrastructure feature. Feeds composable-specialist-agents (guideline generation needs source material), deep-research-pipeline (research artifacts land here), and future retro-flywheel accumulation. Without KB, guideline generation is limited to stack-detection heuristics.",
    storiesList: [
      { title: "KB Init", status: "not-started" },
      { title: "KB Ingest", status: "not-started" },
      { title: "KB Raw Ingest Spike", status: "not-started" },
    ],
    gapNote: "No ingestion pipeline, no store format, no query interface. The kb-raw-ingest-spike must run before kb-ingest can be designed properly — source-type ingestion strategies (Obsidian plugins, crawl4ai, llms.txt) are unresolved. The vault-centric vs project-centric orchestration model is undecided.",
  },

  // ── Partial, quality ───────────────────────────────────────────
  {
    key: "quality-gates-enforced",
    name: "Quality Gates — AVFL, Code Review, and Retro Applied to Every Sprint",
    type: "quality",
    state: "partial",
    stories: { done: 6, total: 8 },
    lastVerified: "2026-04-11",
    hasGap: false,
    description: "Every story goes through AVFL validation, code review, and E2E validation before merge. Gate failures block merge.",
    acceptance: "A sprint completes with: every merged story having passed AVFL + code review + E2E validation; the retro producing a findings document from transcript audit; gate failures reported with actionable resolution guidance.",
    valueNarrative: [
      "Quality gates change the developer's relationship with defects. Without them, defects are discovered after merge, sometimes after demo. With automated gates, defects surface before they compound. The developer gets immediate feedback when a story breaks its acceptance criteria.",
      "But the deeper value is the psychological safety it creates. A developer who knows that every merge is gated can move faster — because they know the system will catch what they miss. The gates are not bureaucratic checkpoints; they are the reason confident, rapid development is possible.",
      "Currently working: AVFL and team review gates run in every sprint. The practice catches real issues. The developer doesn't need to manually review every merge.",
    ],
    systemContext: "The enforcement layer that makes all other features trustworthy. Without gates, any feature can regress silently. With them, \u201Cworking software at sprint end\u201D is the default expectation, not the optimistic one.",
    storiesList: [
      { title: "PostToolUse Lint and Format Hook Active", status: "working" },
      { title: "Stop Gate Runs Conditional Quality Checks", status: "working" },
      { title: "Gherkin ACs and ATDD Workflow Active", status: "working" },
      { title: "Quality Gate Parity Across Workflows", status: "working" },
      { title: "AVFL Scan Profile", status: "working" },
      { title: "Retro Workflow Rewrite", status: "working" },
      { title: "AVFL Fixer Required Gate", status: "not-started" },
      { title: "AVFL Default Agent Composition", status: "not-started" },
    ],
    gapNote: "The AVFL fixer (automated remediation for common defects) is not yet implemented. Some gate failures require manual analysis and fixing. Known defect escapes exist in practice.",
  },
];

// Index-page summary (real numbers from the project)
const SUMMARY = {
  total: 19,
  working: 2,
  partial: 11,
  notStarted: 6,
  withGaps: 6,
  typeBreakdown: { flow: 9, connection: 6, quality: 4 },
  generated: "2026-04-22 09:14",
  hash: "7f3a·c8e1",
};

const TYPE_ORDER = ["flow", "connection", "quality"];

const STATE_ORDER = {
  "not-working": 0,
  "partial": 1,
  "working": 2,
  "not-started": 3,
  "done": 10, "shelved": 11, "abandoned": 12, "rejected": 13,
};

function sortFeatures(features) {
  return [...features].sort((a, b) => {
    if (a.hasGap !== b.hasGap) return a.hasGap ? -1 : 1;
    const sa = STATE_ORDER[a.state] ?? 99;
    const sb = STATE_ORDER[b.state] ?? 99;
    if (sa !== sb) return sa - sb;
    return a.name.localeCompare(b.name);
  });
}

function groupByType(features) {
  const groups = {};
  for (const t of TYPE_ORDER) groups[t] = [];
  for (const f of features) {
    if (!groups[f.type]) groups[f.type] = [];
    groups[f.type].push(f);
  }
  for (const t of Object.keys(groups)) groups[t] = sortFeatures(groups[t]);
  return groups;
}

// Badge tokens — muted hues, matched chroma, separate from indigo accent
const BADGES = {
  active: [
    { key: "working", label: "working", dot: "#3e7a5a", bg: "rgba(62,122,90,0.08)", fg: "#2a5a42" },
    { key: "partial", label: "partial", dot: "#a88328", bg: "rgba(168,131,40,0.09)", fg: "#7a5e1a" },
    { key: "not-working", label: "not working", dot: "#a85252", bg: "rgba(168,82,82,0.09)", fg: "#7a3a3a" },
    { key: "not-started", label: "not started", dot: "#8a8a8a", bg: "rgba(138,138,138,0.09)", fg: "#5a5a5a" },
  ],
  terminal: [
    { key: "done", label: "done", dot: "#6a7a6a", bg: "rgba(106,122,106,0.06)", fg: "#556555" },
    { key: "shelved", label: "shelved", dot: "#8a8577", bg: "rgba(138,133,119,0.06)", fg: "#66635a" },
    { key: "abandoned", label: "abandoned", dot: "#8a7a7a", bg: "rgba(138,122,122,0.06)", fg: "#66595a" },
    { key: "rejected", label: "rejected", dot: "#7a6a7a", bg: "rgba(122,106,122,0.06)", fg: "#5a4f5a" },
  ],
};
const ALL_BADGES = [...BADGES.active, ...BADGES.terminal];
const BADGE_BY_KEY = Object.fromEntries(ALL_BADGES.map(b => [b.key, b]));
const TERMINAL_STATES = new Set(["done", "shelved", "abandoned", "rejected"]);

Object.assign(window, {
  FEATURES, SUMMARY, TYPE_ORDER,
  sortFeatures, groupByType,
  BADGES, ALL_BADGES, BADGE_BY_KEY, TERMINAL_STATES,
});
