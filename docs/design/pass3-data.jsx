// Sample data for Pass 3 — Sprints + Flywheel.
// Story slugs are grounded in content-sample.md / data.jsx.
// Retro findings and distilled skills are invented in Momentum voice for
// comparison-canvas fidelity; real ledger data lands when direction is chosen.

const ACTIVE_SPRINT = {
  key: "sprint-2026-04-22",
  goal: "Close the flywheel loop — make retro findings compound across sprints instead of dying in a markdown file.",
  started: "2026-04-22",
  horizon: "~2 weeks",
  stories: {
    inWave: [
      {
        key: "cross-story-pattern-detection",
        title: "Cross-Story Pattern Detection",
        wave: 1,
        gates: { avfl: "pass", cr: "pending", e2e: "pending" },
        advances: ["retro-and-flywheel"],
      },
      {
        key: "findings-ledger",
        title: "Findings Ledger Accumulates Quality Findings",
        wave: 1,
        gates: { avfl: "pending", cr: "pending", e2e: "pending" },
        advances: ["retro-and-flywheel"],
      },
      {
        key: "avfl-fixer-required-gate",
        title: "AVFL Fixer Required Gate",
        wave: 2,
        gates: { avfl: "pending", cr: "pending", e2e: "pending" },
        advances: ["quality-gates-enforced"],
      },
    ],
    merged: [
      {
        key: "retro-triage-handoff",
        title: "Retro → Triage Handoff",
        gates: { avfl: "pass", cr: "pass", e2e: "pass" },
        advances: ["retro-and-flywheel"],
      },
      {
        key: "sprint-boundary-compression",
        title: "Sprint Boundary Compression",
        gates: { avfl: "pass", cr: "pass", e2e: "pass" },
        advances: ["retro-and-flywheel"],
      },
    ],
    blocked: [
      {
        key: "flywheel-workflow",
        title: "Flywheel Workflow Explains Issues and Guides Upstream Trace",
        blockedBy: "findings-ledger",
        reason: "Waits on ledger store schema — can't wire upstream trace without a place to read findings from.",
        gates: { avfl: "n/a", cr: "n/a", e2e: "n/a" },
        advances: ["retro-and-flywheel"],
      },
    ],
  },
};

// Cross-cut: features this sprint is advancing
const SPRINT_ADVANCES = [
  { key: "retro-and-flywheel", name: "Sprint Retro + Practice Improvement Flywheel", touching: 4 },
  { key: "quality-gates-enforced", name: "Quality Gates — AVFL, Code Review, and Retro", touching: 1 },
];

const RECENT_SPRINTS = [
  {
    key: "sprint-2026-04-08",
    goal: "Tighten sprint-boundary compression and retro triage.",
    dates: "Apr 8 – Apr 21",
    merged: 5,
    gateHealth: "clean",
    findings: 3,
    advanced: ["retro-and-flywheel"],
  },
  {
    key: "sprint-2026-03-25",
    goal: "Feature grooming skill + status visibility.",
    dates: "Mar 25 – Apr 7",
    merged: 4,
    gateHealth: "1 defect escape",
    findings: 5,
    advanced: ["feature-status-visibility"],
  },
  {
    key: "sprint-2026-03-11",
    goal: "AVFL scan profile lands as required gate.",
    dates: "Mar 11 – Mar 24",
    merged: 6,
    gateHealth: "clean",
    findings: 2,
    advanced: ["quality-gates-enforced"],
  },
];

// ─── Flywheel — retro findings, stories they generated, skills distilled ───
// Findings use the voice from content-sample: direct, analogical, long-form.

const FINDINGS = [
  {
    key: "finding-reread-loop",
    sprint: "sprint-2026-04-08",
    when: "2026-04-21",
    label: "dev agents re-read already-read files inside a single task",
    note: "Observed across three stories in the sprint: the implementation agent re-fetches files it read ten turns earlier, burning context and latency. Pattern is not random — it correlates with long planning preambles that push prior reads out of the agent's working memory.",
    producedStory: "agent-working-memory-hint",
    distilledSkill: "skill-read-receipts",
    severity: "recurring",
  },
  {
    key: "finding-gate-failure-vagueness",
    sprint: "sprint-2026-04-08",
    when: "2026-04-20",
    label: "AVFL failure messages don't name the offending file",
    note: "Three gate failures this sprint required the developer to open the AVFL log to find which file tripped the scan. The gate knows the path; it just isn't in the surface message. Low-effort fix, high daily-friction payoff.",
    producedStory: "avfl-failure-reporting",
    distilledSkill: "rule-gate-messages-name-the-thing",
    severity: "one-shot",
  },
  {
    key: "finding-premature-retro",
    sprint: "sprint-2026-03-25",
    when: "2026-04-05",
    label: "retro runs before all merge-queue stories land",
    note: "Retro was invoked with two stories still in the merge queue; findings missed the last two merges entirely. The skill assumed sprint-end means all work is sealed. It doesn't always. Guard needed.",
    producedStory: "retro-waits-for-quiet-queue",
    distilledSkill: "rule-retro-preconditions",
    severity: "recurring",
  },
  {
    key: "finding-status-drift",
    sprint: "sprint-2026-03-25",
    when: "2026-04-01",
    label: "features stay partial after last story done",
    note: "Feature-status showed 'partial' for a feature whose five stories were all done. Grooming hadn't run. The artifact was technically accurate and practically misleading — the developer's mental state was 'still working on it,' reality was 'awaiting promotion.'",
    producedStory: "status-drift-surface",
    distilledSkill: "rule-status-drift-visible",
    severity: "one-shot",
  },
  {
    key: "finding-avfl-thrash",
    sprint: "sprint-2026-03-11",
    when: "2026-03-23",
    label: "AVFL fixer not yet present — thrash on repetitive defects",
    note: "Same three defect classes tripped AVFL across four stories. Manual fixes each time. This is the exact shape of pattern the fixer was designed for; its absence is felt. Not a new finding — third time it has been noted. Promote to epic.",
    producedStory: "avfl-fixer-required-gate",
    distilledSkill: "skill-avfl-remediation",
    severity: "recurring",
  },
  {
    key: "finding-planning-preamble",
    sprint: "sprint-2026-03-11",
    when: "2026-03-18",
    label: "planning preamble swamps execution context",
    note: "Dev agents start stories with 800-line planning documents in the transcript. By the time implementation begins, the originally-relevant code is pushed out. Plans are worth having; plans in the transcript during implementation are not.",
    producedStory: "planning-artifact-offload",
    distilledSkill: "skill-offloaded-planning",
    severity: "recurring",
  },
];

const SKILLS = [
  {
    key: "skill-read-receipts",
    kind: "skill",
    name: "Track file reads as explicit receipts",
    note: "Agent keeps a receipts block — {path, hash, turn} — and consults it before any file read. Receipts survive preamble truncation because they live in the agent's state, not the transcript.",
    encodedIn: ["momentum:sprint-dev", "agent:implementation"],
    provenance: ["finding-reread-loop"],
  },
  {
    key: "rule-gate-messages-name-the-thing",
    kind: "rule",
    name: "Gate failures name the file and the failing rule",
    note: "AVFL, CR, E2E: every failure surface includes {file_path, rule_id, one-line reason}. No grep required.",
    encodedIn: ["momentum:avfl", "momentum:code-review"],
    provenance: ["finding-gate-failure-vagueness"],
  },
  {
    key: "rule-retro-preconditions",
    kind: "rule",
    name: "Retro refuses to run while merge queue non-empty",
    note: "Precondition check in the retro skill. If stories in flight, retro exits with a one-line message naming the outstanding stories and suggesting `sprint-status` first.",
    encodedIn: ["momentum:retro"],
    provenance: ["finding-premature-retro"],
  },
  {
    key: "rule-status-drift-visible",
    kind: "rule",
    name: "Status drift is a first-class signal, not a bug",
    note: "When all stories done but feature still partial, the dashboard renders it explicitly. Encoded in feature-status rendering and grooming skill.",
    encodedIn: ["momentum:feature-status", "momentum:feature-grooming"],
    provenance: ["finding-status-drift"],
  },
  {
    key: "skill-avfl-remediation",
    kind: "skill",
    name: "AVFL fixer with bounded autonomy",
    note: "Fixer agent that remediates defects in a named allowlist of rule classes and leaves the rest to humans. Requires the ledger so it can learn which classes recur.",
    encodedIn: ["momentum:avfl-fix (pending)"],
    provenance: ["finding-avfl-thrash"],
  },
  {
    key: "skill-offloaded-planning",
    kind: "skill",
    name: "Offload planning docs outside the transcript",
    note: "Planning artifacts write to disk; implementation agents receive a terse handoff and the file paths. The plan exists; it just isn't in working memory.",
    encodedIn: ["momentum:sprint-planning", "agent:implementation"],
    provenance: ["finding-planning-preamble"],
  },
];

// Stories generated by findings (the middle hop in the provenance chain).
const GENERATED_STORIES = {
  "agent-working-memory-hint": {
    title: "Agent Working-Memory Receipts",
    status: "not-started",
    fromFinding: "finding-reread-loop",
    becomesSkill: "skill-read-receipts",
  },
  "avfl-failure-reporting": {
    title: "AVFL Failure Messages Name the File",
    status: "working",
    fromFinding: "finding-gate-failure-vagueness",
    becomesSkill: "rule-gate-messages-name-the-thing",
  },
  "retro-waits-for-quiet-queue": {
    title: "Retro Precondition: Quiet Merge Queue",
    status: "working",
    fromFinding: "finding-premature-retro",
    becomesSkill: "rule-retro-preconditions",
  },
  "status-drift-surface": {
    title: "Surface Status Drift as First-Class Signal",
    status: "working",
    fromFinding: "finding-status-drift",
    becomesSkill: "rule-status-drift-visible",
  },
  "avfl-fixer-required-gate": {
    title: "AVFL Fixer Required Gate",
    status: "partial",
    fromFinding: "finding-avfl-thrash",
    becomesSkill: "skill-avfl-remediation",
  },
  "planning-artifact-offload": {
    title: "Planning Artifact Offload",
    status: "partial",
    fromFinding: "finding-planning-preamble",
    becomesSkill: "skill-offloaded-planning",
  },
};

// Sprint lanes used by Timeline direction
const TIMELINE_SPRINTS = [
  { key: "sprint-2026-03-11", label: "sprint-03-11", dates: "Mar 11 – Mar 24" },
  { key: "sprint-2026-03-25", label: "sprint-03-25", dates: "Mar 25 – Apr 7" },
  { key: "sprint-2026-04-08", label: "sprint-04-08", dates: "Apr 8 – Apr 21" },
  { key: "sprint-2026-04-22", label: "sprint-04-22", dates: "Apr 22 – now", active: true },
];

Object.assign(window, {
  ACTIVE_SPRINT, SPRINT_ADVANCES, RECENT_SPRINTS,
  FINDINGS, SKILLS, GENERATED_STORIES, TIMELINE_SPRINTS,
});
