# Epic Template

Use this template when defining a new epic or formalizing an existing one in `epics.md`.
Epics are long-lived categories — they never close. Fill all seven fields.

---

## Epic: {slug}

{one-sentence outcome statement — what a developer can do when this epic's work is complete}

**Category:** {one-line — what kind of work lives here, e.g. "Orchestration & UX", "Quality Enforcement", "Research Infrastructure"}

**Strategic intent:** {2-3 sentences — why this category exists, what product capability it builds, how it relates to the overall Momentum practice}

**Boundaries:** {what belongs here vs. adjacent epics — be specific about what this epic does NOT include, to prevent scope drift}

**FRs covered:** {comma-separated list of FR numbers, e.g. FR6, FR7, FR8 — or "none" if this epic predates the current FR inventory}

**NFRs covered:** {comma-separated list of NFR numbers — or "none"}

**Current state:** {N done, M remaining — e.g. "3 done, 4 remaining" — updated as stories complete}

> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Field Guidance

| Field | Purpose | Notes |
|---|---|---|
| slug | Machine identifier — kebab-case, no spaces | Must match `epic_slug` values in stories/index.json |
| Category | Human label for what kind of work | One line; used in backlog display groupings |
| Strategic intent | Why this category exists | 2-3 sentences; connects to PRD goals |
| Boundaries | What belongs here vs. adjacent | Explicit "does NOT include" statements prevent drift |
| FRs covered | Functional requirement coverage | Cross-reference against Requirements Inventory in epics.md |
| NFRs covered | Non-functional requirement coverage | List NFR numbers from Requirements Inventory |
| Current state | Live progress indicator | Update as stories transition to done |
