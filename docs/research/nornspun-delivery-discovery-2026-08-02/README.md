# Nornspun Delivery Discovery — 2026-08-02

**Question under investigation:** After ~10 sprints and 2 quickfixes of the Momentum practice on
nornspun (April–July 2026), 91 stories reached `done` and yet no complete user-facing feature
works end-to-end. The latest sprint (sprint-2026-07-13) finished all 12 stories and the app
still could not do the simplest things when opened. Is the practice optimizing for story
completion instead of delivered functionality — or is something else going on?

**Method:** Multi-agent discovery over session transcripts, sprint artifacts, git history, and
the running product; parallel external research into how the field has encountered and solved
this failure mode (mid-2025 → 2026); an adversarial council (architect / product manager /
super-senior developer) with fresh contexts; final synthesis.

## Corpus layout

| Path | Contents |
|---|---|
| `00-session-cartography.md` | Map of raw session transcripts → sprints/activities, incl. developer sentiment extracts |
| `sprints/` | One evidence dossier per sprint (10 sprints + quickfixes) |
| `lenses/` | Cross-cutting audits: planning, spec quality, verification, integration wiring, retro loop, backlog economics, product truth |
| `ground-truth-app-state.md` | What the product can actually do today, empirically |
| `research/` | External research: articles, postmortems, practices (last ~12 months) + ours-vs-field comparison |
| `council/` | Adversarial position papers + rebuttals (architect, PM, super-senior dev) |
| `synthesis.md` | Final synthesis — the actual findings |

## Primary sources

- `~/projects/nornspun/.momentum/` — sprints, stories, features.json, practice-ledger, handoffs
- `~/projects/nornspun/docs/` — PRD, epics, roadmap, ADRs, assessments, decisions
- `~/.claude/projects/-Users-steve-projects-nornspun/` — 16 session transcripts (2026-07-06 → 2026-08-02)
- Per-sprint `audit-extracts/` — distilled transcript evidence for sprints whose raw transcripts are gone
- Git histories: `nornspun`, `nornspun-backend`, `nornspun-client`
