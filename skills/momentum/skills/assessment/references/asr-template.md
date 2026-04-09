# ASR Template — Assessment Record

This is the canonical template for all ASR (Assessment Record) documents produced by
`momentum:assessment`. Every ASR must follow this structure exactly.

---

## Frontmatter Schema

```yaml
---
id: ASR-NNN
title: Descriptive title capturing what was assessed and the key finding
date: 'YYYY-MM-DD'
status: current
method: Brief description of discovery agents spawned (e.g., "3-agent parallel discovery: backend audit, client audit, journey trace")
decisions_produced: []
supersedes:
---
```

### Field Definitions

| Field | Required | Description |
|---|---|---|
| `id` | Yes | Auto-incremented from existing assessments. Read `assessments/index.md` to find next ID. |
| `title` | Yes | Descriptive — captures what was assessed and the headline finding. |
| `date` | Yes | ISO date in quotes: `'YYYY-MM-DD'` |
| `status` | Yes | `current` for new assessments. Set to `superseded` when replaced by a newer assessment. |
| `method` | Yes | Describes what discovery agents were spawned and what they audited. |
| `decisions_produced` | Yes | Start empty `[]`. Filled in later by `momentum:decision` skill. |
| `supersedes` | No | Path to prior assessment this replaces, if applicable. |

---

## Body Structure

```markdown
# ASR-NNN: {{title}}

## Purpose

One paragraph: what is being assessed and why. What questions should this assessment
answer? What decisions is it meant to inform?

## Method

Describe the discovery approach:
- How many agents were spawned, what each audited
- What repositories or directories were examined
- What the developer told us about scope

---

## Finding N: {{headline}}

One sentence summary of what was found.

| Component | Status | Evidence |
|---|---|---|
| thing | Real / Stub / Missing / Broken | file.py (LOC), description |
| thing | Real / Stub / Missing / Broken | file.py (LOC), description |

Narrative: 2-4 sentences interpreting what the evidence means. What does this
imply for the product? What's notable?

---

## Finding N+1: {{headline}}

(repeat pattern for each finding)

---

## Recommended Next Steps

1. **Concrete action** — why, what it unlocks
2. **Concrete action** — why, what it unlocks
3. **Concrete action** — why, what it unlocks

Next steps must be concrete and actionable. Not "consider X" — "do X, because Y."

---

## Raw Data

### {{Agent Name}} Findings

Paste or summarize raw agent output here. This section preserves the evidence trail
without cluttering the findings above. Use sub-sections per agent.

```

---

## Formatting Conventions

- **Finding headlines** should name the subject and verdict: "Backend is 60%
  Production-Ready", not "Backend Status"
- **Evidence tables** use `Real | Stub | Missing | Broken` status values consistently
- **Evidence column** should include file paths and LOC counts where available
- **Narrative** under each finding interprets — don't just repeat the table
- **Recommended Next Steps** are numbered, bolded action names, with rationale
- **Raw Data** section is optional but encouraged — preserves the audit trail

---

## Naming Convention

Files are named: `asr-NNN-slug-YYYY-MM-DD.md`

- `NNN` = zero-padded 3-digit number (001, 002, ...)
- `slug` = kebab-case, max 5-6 words capturing subject
- `YYYY-MM-DD` = assessment date

Example: `asr-001-community-readiness-2026-04-08.md`

---

## Registry Entry Format

When updating `assessments/index.md`, add a row to the table:

```markdown
| ASR-NNN | Title | YYYY-MM-DD | [] | current |
```

The `decisions_produced` column starts empty and is filled by the decision skill.
