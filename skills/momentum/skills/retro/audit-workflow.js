export const meta = {
  name: 'retro-audit-engine',
  description:
    'Sprint retro transcript audit as a dynamic Workflow: sharded lens + per-story discovery, adversarial verification, single-synthesizer findings doc.',
  phases: [
    { title: 'Discover', detail: 'parallel lens auditors + one analyst per sprint story' },
    { title: 'Verify', detail: 'per-finding adversarial refute panel; majority-refute drops' },
    { title: 'Synthesize', detail: 'one agent writes retro-transcript-audit.md and returns structured findings' },
  ],
}

// ─────────────────────────────────────────────────────────────────────────────
// Inputs — the retro main loop passes these as `args`. Everything time- or
// scope-bound comes from args; the script body computes NO dates/randomness
// (Date.now()/Math.random()/new Date() are unavailable in Workflow scripts).
// ─────────────────────────────────────────────────────────────────────────────
const {
  sprint_slug,
  sprint_started,
  sprint_completed,
  sprint_stories = [],
  audit_dir,
  transcript_query_path,
} = args || {}

if (!sprint_slug || !audit_dir) {
  throw new Error('retro-audit-engine: args.sprint_slug and args.audit_dir are required')
}

const sprint_dir = audit_dir.replace(/\/audit-extracts\/?$/, '')
const doc_path = `${sprint_dir}/retro-transcript-audit.md`
const dateRange = `--after ${sprint_started} --before ${sprint_completed}`

// Mandatory large-file discipline, embedded in every auditor prompt.
const LARGE_FILE =
  'Large-file protocol: run `wc -l` first; for files over 200 lines, stream via `python3`/transcript-query SQL or Read in 500-line chunks. Never full-Read agent-summaries.jsonl or errors.jsonl.'

// ── Schemas (structured returns; validation happens at the tool layer) ────────
const FINDINGS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['type', 'severity', 'evidence', 'reveals', 'recommendation'],
        properties: {
          type: { type: 'string' },
          severity: { type: 'string', description: 'high | medium | low' },
          evidence: { type: 'string', description: 'exact quote or counts — mandatory' },
          reveals: { type: 'string' },
          recommendation: { type: 'string', description: 'fix | keep | investigate' },
          story: { type: 'string', description: 'story slug, when story-scoped' },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['refuted', 'reason'],
  properties: {
    refuted: { type: 'boolean' },
    reason: { type: 'string' },
  },
}

const SYNTH_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['priority_action_items', 'handoff_candidates', 'metrics', 'doc_path', 'synthesize_status'],
  properties: {
    priority_action_items: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'priority', 'source_detail', 'suggested_ac'],
        properties: {
          title: { type: 'string' },
          priority: { type: 'string', description: 'critical | high | medium | low' },
          source_detail: { type: 'string' },
          suggested_ac: { type: 'array', items: { type: 'string' } },
          epic_slug: { type: 'string' },
        },
      },
    },
    handoff_candidates: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'slug', 'description'],
        properties: {
          title: { type: 'string' },
          slug: { type: 'string' },
          description: { type: 'string' },
          epic_slug: { type: 'string' },
          failure_diagnosis: { type: 'object', additionalProperties: true },
          feature_state_transition: { type: 'object', additionalProperties: true },
        },
      },
    },
    metrics: { type: 'object', additionalProperties: true },
    doc_path: { type: 'string' },
    synthesize_status: { type: 'string', description: '"ok" only if the document was written' },
  },
}

// ─────────────────────────────────────────────────────────────────────────────
// Phase: Discover — parallel() lens auditors + one analyst per sprint story.
// parallel() is a barrier: we want the full candidate-finding set before verify.
// ─────────────────────────────────────────────────────────────────────────────
phase('Discover')

const LENSES = [
  {
    key: 'human',
    files: ['user-messages.jsonl'],
    focus:
      'corrections (user fixing agent behavior), redirections (changing approach / canceling work), frustration signals (repeated asks, escalation, complaints), praise/approval, and decision points where human judgment was required',
  },
  {
    key: 'execution',
    files: ['agent-summaries.jsonl', 'errors.jsonl'],
    focus:
      'duplication (near-identical first prompts), error recovery, tool efficiency (high tool_results vs low assistant_turns), story iteration counts, and abandoned agents (< 3 assistant turns). Do NOT flag single-turn consolidators (single turn + non-empty output) as abandoned — that is correct behavior',
  },
  {
    key: 'review',
    files: ['team-messages.jsonl', 'agent-summaries.jsonl'],
    focus:
      'quality-gate effectiveness: real issues caught vs false positives that were overturned, fix-cycle convergence vs thrash, inter-agent handoff clarity, and reviewer prompt quality',
  },
  {
    key: 'efficiency',
    files: ['agent-summaries.jsonl'],
    focus:
      'turn/tool economy across the subagent population: redundant work, agents independently re-authoring the same helper, and high-cost low-yield agents',
  },
  {
    key: 'coordination',
    files: ['team-messages.jsonl'],
    focus:
      'coordination failures: unclear handoffs, missing context passed between agents, self-routing/dedup failures, and blocked waits',
  },
]

const lensThunks = LENSES.map((l) => () =>
  agent(
    `You are the ${l.key} lens auditor for the ${sprint_slug} retrospective.
Read these extract files under ${audit_dir}: ${l.files.join(', ')}.
${LARGE_FILE}

Investigate: ${l.focus}.

For each finding record: type, severity (high|medium|low), evidence (the exact quote or counts — MANDATORY; findings without evidence are hallucinations, omit them), reveals (the practice gap or strength it exposes), recommendation (fix|keep|investigate).

You may run ad-hoc queries for depth:
  python3 ${transcript_query_path} sql "SELECT ..." ${dateRange}

Return your findings via the schema. If you find nothing real, return an empty findings array.`,
    { label: `lens:${l.key}`, phase: 'Discover', schema: FINDINGS_SCHEMA }
  ).then((r) => (r?.findings || []).map((f) => ({ ...f, source: `lens:${l.key}` })))
)

const storyThunks = sprint_stories.map((slug) => () =>
  agent(
    `You are the per-story analyst for story "${slug}" in the ${sprint_slug} retrospective.
Scope your analysis to this single story by querying only its sessions:
  python3 ${transcript_query_path} sql "SELECT ..." ${dateRange} --story-slugs ${slug}
${LARGE_FILE}

Determine: how many dev/review passes the story needed and why; notable errors or rework; whether it converged cleanly or thrashed; any human intervention specific to it.

For each finding record: type, severity (high|medium|low), evidence (MANDATORY), reveals, recommendation (fix|keep|investigate), and set "story" to "${slug}". Return via the schema (empty array if nothing notable).`,
    { label: `story:${slug}`, phase: 'Discover', schema: FINDINGS_SCHEMA }
  ).then((r) => (r?.findings || []).map((f) => ({ ...f, source: `story:${slug}`, story: slug })))
)

const discovered = (await parallel([...lensThunks, ...storyThunks])).filter(Boolean).flat()
log(
  `Discover: ${discovered.length} candidate findings from ${LENSES.length} lens auditors + ${sprint_stories.length} per-story analysts`
)

// ─────────────────────────────────────────────────────────────────────────────
// Phase: Verify — pipeline() so each finding streams through its own refute
// panel without waiting for the others. The verify stage spawns a 2–3 skeptic
// parallel() panel per finding; majority-refute drops it. Kills false positives.
// ─────────────────────────────────────────────────────────────────────────────
phase('Verify')

const PANEL = [1, 2, 3]
const judged = (
  await pipeline(discovered, (f) =>
    parallel(
      PANEL.map((n) => () =>
        agent(
          `Adversarially REFUTE this retrospective finding. Default to refuted=true unless the evidence clearly holds up.
Finding: ${JSON.stringify({ type: f.type, severity: f.severity, evidence: f.evidence, reveals: f.reveals, source: f.source })}

Skeptic #${n}. Ask: is the evidence real and correctly interpreted? Is this actually a problem, or normal/expected behavior (e.g., a single-turn consolidator is NOT an abandoned agent; one redirection is not a frustration pattern)? Could it be a coincidence or a selection artifact?

Return refuted (boolean) and a one-line reason.`,
          { label: `refute:${f.source}#${n}`, phase: 'Verify', schema: VERDICT_SCHEMA }
        )
      )
    ).then((verdicts) => {
      const v = verdicts.filter(Boolean)
      const refutes = v.filter((x) => x.refuted).length
      // Majority of the panel must refute to drop the finding.
      return { finding: f, kept: refutes < Math.ceil(v.length / 2), refutes, votes: v.length }
    })
  )
).filter(Boolean)

const survivors = judged.filter((r) => r.kept).map((r) => r.finding)
const dropped = judged.length - survivors.length
log(`Verify: ${survivors.length} findings survived, ${dropped} dropped by majority refute`)

// ─────────────────────────────────────────────────────────────────────────────
// Phase: Synthesize — a SINGLE agent() (the one documenter). Never in a loop or
// parallel()/multi-item pipeline stage. It writes retro-transcript-audit.md and
// returns the structured contract the retro main loop consumes.
// ─────────────────────────────────────────────────────────────────────────────
phase('Synthesize')

const synth = await agent(
  `You are the SINGLE synthesizer for the ${sprint_slug} retrospective. You are the only agent that writes the findings document — there is exactly one of you.

You received ${survivors.length} adversarially-verified findings (false positives already removed):
${JSON.stringify(survivors, null, 2)}

Do the following:
1. Compute metrics by counting lines in the extracts (run \`wc -l\`):
   ${audit_dir}/user-messages.jsonl, ${audit_dir}/agent-summaries.jsonl, ${audit_dir}/errors.jsonl, ${audit_dir}/team-messages.jsonl
2. Perform a cross-cutting synthesis: themes that recur across lenses, successes (recommend KEEP) vs struggles (recommend FIX/INVESTIGATE), and a per-story rollup.
3. WRITE the findings document to ${doc_path} with EXACTLY these eight sections, in order:
   # Sprint Transcript Audit — ${sprint_slug}
   ## Executive Summary
   ## What Worked Well
   ## What Struggled
   ## User Interventions
   ## Story-by-Story Analysis
   ## Cross-Cutting Patterns
   ## Metrics            (a table)
   ## Priority Action Items   (ranked; each item: title, priority [critical|high|medium|low], source_detail, suggested story-stub ACs)
   Every finding in the doc must carry: what happened, evidence, root cause, recommendation.
4. Return the structured object:
   - priority_action_items[]: one per Priority Action Item (title, priority, source_detail, suggested_ac[], optional epic_slug)
   - handoff_candidates[]: un-actioned/low-priority findings, feature-state transitions, and diagnosed failures worth carrying to next planning (title, slug, description, optional epic_slug/failure_diagnosis/feature_state_transition)
   - metrics{}: user_msgs, subagents, errors, team_msgs, struggles, successes
   - doc_path: "${doc_path}"
   - synthesize_status: "ok" ONLY if you successfully wrote the document; otherwise "failed".`,
  { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA }
)

return {
  priority_action_items: synth?.priority_action_items || [],
  handoff_candidates: synth?.handoff_candidates || [],
  metrics: synth?.metrics || {},
  doc_path: synth?.doc_path || doc_path,
  synthesize_status: synth?.synthesize_status || 'failed',
  verify_stats: { candidates: discovered.length, survived: survivors.length, dropped },
}
