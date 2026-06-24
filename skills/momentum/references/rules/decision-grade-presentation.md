---
title: Decision-Grade Presentation Standard
applies_to: All AI human-facing output — Momentum surfaces and everyday conversational replies
status: Active
source_decisions: DEC-036 D5
cascade: global → project → path-scoped
---

# Decision-Grade Presentation Standard

This rule is authoritative and self-sufficient. An agent loading only this file has
complete guidance to apply the standard without reading any other document.

**The standard in one sentence:** tight on the irrelevant, complete on the decision-relevant.

---

## 1. The Core Convention — Effort vs. Verbosity (Orthogonal)

**`effort` drives work depth. Explicit caps govern output verbosity. The two are orthogonal.**

A skill running at `effort: high` does more analysis. It does NOT earn a longer presentation.
A skill is **never permitted to widen its output because it did more work.** The caps below
apply regardless of how much work was done to produce the output.

This directly answers the Specification-Fatigue problem (`docs/research/spec-fatigue-research-2026-03-21.md`):
review budget is finite; a longer report from a deeper run still costs the same to read.

---

## 2. The CAPS Half — Measurable, Enforceable Ceilings

Each cap is a **checkable condition** — a reviewer or validator can mechanically verify it
against any output. "Be brief" is not a cap. The following are caps.

### 2.1 Global Caps (apply to every surface)

| Cap | Checkable Condition |
|---|---|
| **Bullet cap** | ≤ 7 bullets per list. Lists with more items must collapse routine/clean entries to a single count line: "N routine items auto-resolved." |
| **Exec-summary-first** | The decision, headline, or finding title leads. Supporting detail follows. No surface buries its point after setup prose. Mechanically verifiable: the first content element is the decision/headline, not background. |
| **Positive-concision** | State what IS the case. Do not open with what isn't the case or lead with extensive negative framing. |

### 2.2 Per-Surface Budgets

Each named surface type below has a stated budget. A surface without a declared budget is a
**gap in this rule, not a silent exemption** — the gap must be resolved before the surface ships.

| Surface | Budget | Notes |
|---|---|---|
| **Situational report** (e.g., Impetus session greeting) | ≤ 2 sentences | Honest ledger counts + recurring-pattern signal must appear inline within that budget (floor wins on the signal — do not drop it to hit the sentence count; trim other wording instead) |
| **Finding card / divergence card** | Lead-in ≤ 1 sentence; supporting detail in collapsible or second paragraph | The what/why/evidence triple is required inline regardless of this budget (floor wins) |
| **Decision card** (adopt/reject/defer presentation) | ≤ 5 lines of prose + ≤ 3 supporting bullets | Headline + verdict first; rationale after; what/why/evidence inline (floor wins) |
| **Pause-ask surface** (mid-flight escalation) | Per the Pause-Ask Surface Contract template | What / Why / Evidence fields are required and cannot be omitted; template is the floor |
| **End-gate report section** | Routine items: 1 count line. High-risk items: the 5-beat risk narrative (per conduct report spec §3/§5). Collapsibles for depth-on-demand. | Length tracks risk surface, not story count |
| **Findings digest / retro digest** | ≤ 7 actionable findings surfaced. Routine findings collapsed to a count. | Each surfaced finding carries what/why/evidence (floor wins) |
| **Recommendations / next steps** | ≤ 5 items, each ≤ 2 sentences | Each item is specific and actionable; "consider X" is not an item |
| **Conversational reply** (everyday assistant turn) | Answer-first: the direct answer is the first sentence, before any setup. Default ≤ 150 words for a direct question. For a genuinely multi-part question, use section headers + the global ≤ 7-bullet cap and push supporting detail to depth-on-demand ("want the detail?") rather than inlining it. No process narration ("I searched X, then ran Y…"). | Length tracks the genuine complexity of the question, never the effort spent answering it (§1). Any item requiring a developer decision still carries what/why/evidence inline (floor wins, §3). |
| **Companion decision surface** (paired with a large review document; incl. the pre-sprint plan gate & post-sprint results gate) | Lead with a plain-language purpose; one ✓ line for all verified mechanics; structure diagrammed (deps/waves/status); ≤ 7 genuine forks, each a What/Why/Evidence/Recommendation/Options card per the Pause-Ask template; the large document linked as depth-on-demand. Rendered as a **visual HTML** surface (§5.1), not flat prose. | Mandatory whenever a process emits a review document exceeding the Decision-card budget (§5). The large document is the backing, not the review artifact (floor wins on the forks). |

### 2.3 What Caps Cut

Caps cut **Specification-Fatigue material** — content that consumes review budget without
adding decision-relevant signal:

- Routine and clean items that auto-resolved or require no decision
- Background context the developer already has
- Process narration ("I ran the audit and found...")
- Extensive negative framing before the headline
- Items that can be depth-on-demand (collapsible) rather than expanded inline

---

## 3. The SELF-SUFFICIENCY FLOOR — Non-Negotiable Counterweight

**Every decision-relevant item carries what / why-it-matters / evidence inline.**

The human is **never** sent to open a file, recall prior context, or read another document
to make the call. The surface is self-contained.

### What "decision-relevant" means

An item is decision-relevant if:
- The developer must take an action based on it (approve, reject, fix, defer)
- It represents a risk, divergence, finding, or escalation requiring a judgment
- Missing it would leave the developer with an incomplete picture for their decision

### The three required fields

For every decision-relevant item, all three must be present **inline** on the surface:

| Field | What it provides |
|---|---|
| **What** | The concrete thing at stake — the finding, the change, the risk — stated plainly |
| **Why it matters** | The stakes: what goes wrong or is improved if this is or isn't addressed |
| **Evidence** | The supporting detail: file path, count, observed behavior, test result — something checkable |

### Missing field = defect

A missing what, why-it-matters, or evidence field on a decision-relevant item is a **defect**,
not a permitted blank. The item is incomplete and must be fixed before the surface ships.

---

## 4. The Caps-vs-Floor Boundary — Resolution Rule

**Caps cut irrelevant material. Caps NEVER trim a decision-relevant what/why/evidence field.**

When a surface is under budget pressure and appears to require choosing between staying within
the cap or preserving a decision-relevant item's completeness:

1. **Trim routine and clean material first.** Collapse them to a count line.
2. **Use collapsibles / depth-on-demand for supporting detail.** The lead-in is tight; the
   expansion preserves completeness.
3. **The floor wins.** A surface that is over its budget but carries complete what/why/evidence
   for all decision-relevant items is preferable to a surface that is under budget but drops a
   required field.

**Stated as the resolution rule:** *tight on the irrelevant, complete on the decision-relevant.*

This boundary is not a judgment call. The floor is non-negotiable. The caps govern irrelevant
content only.

---

## 5. The Companion-Surface Obligation — Large Review Documents

A large document and a decision surface serve **two different readers** and pull in opposite
directions. The work-list (for the next pipeline stage — a skill, a machine, an implementing
agent) wants to be exhaustive: every item, every field, *more is safer*. The review surface (for
the human deciding) wants the handful of genuine forks with defaulted recommendations: *less is
safer*. **One artifact cannot serve both.** A 600-line database handed to a human as "the thing to
evaluate" is the failure mode this section exists to prevent.

**Trigger (checkable):** Any process — skill, workflow, or agent turn — that emits a document
**for human review, approval, or choice** which **exceeds the Decision-card budget** (§2.2:
≤ 5 lines prose + ≤ 3 bullets) MUST also emit a **companion decision surface** modeled on the
canonical Pause-Ask template (§7) and the skeleton at
`references/templates/companion-decision-surface.html`.

The large document is **not** the review artifact — it is the **depth-on-demand backing** (the
machine work-list, the full record). The companion surface is what the human is actually handed.

**The companion surface MUST:**

1. **Lead with the decision** asked (approve / reject / choose) — not background the reader owns.
2. **Collapse every mechanically-verifiable claim to one ✓ line** (counts, slug-uniqueness, DAG
   validity, coverage tallies). These are validator work — never human-review material.
3. **Surface only the genuine forks** — items needing judgment an agent cannot default to
   standards (≤ 7, per the bullet cap). Everything defaultable is defaulted silently.
4. For **each fork**, carry inline (per the Pause-Ask template): **What** (at stake) · **Why**
   (the stakes) · **Evidence** (checkable detail) · **Recommendation** (the defaulted call) ·
   **Options** (the resolutions, e.g. Adopt / Change / Reject-or-Defer).
5. **Reference the large document as depth-on-demand** — never require opening it to decide.

### 5.1 Presentation form — the third leg (non-overridable)

The caps (§2) govern *which information and how much*; the floor (§3) governs *what must be
present*. **Neither governs *form*** — and a surface can satisfy both halves and still be an
unreadable text wall. (Observed: a fully caps-and-floor-compliant Markdown gate drew the reaction
*"no visuals or diagrams, I have no idea after reading it for over a minute what it's trying to
accomplish."*) Presentation form is therefore a **third, co-equal leg** of this standard for
decision gates and companion surfaces:

- **Render as a visual HTML surface**, not flat prose — a companion decision surface for a
  sprint / plan / large-review gate is HTML (sibling of `endgate-report.html`), opened in the viewer.
- **Lead with a plain-language purpose hero** — what the work accomplishes, in words a
  non-implementer reads in seconds, *before* any table or list.
- **Diagram the structure** — dependencies / waves / status as an actual diagram (e.g. inline
  SVG), not described in prose. Mark any critical-path or single-point-of-failure node.
- **Link to source artifacts; never inline or edit them** — the machine band (full specs, ACs,
  tasks) stays one click away in its source files so implementing agents keep their source of truth.
- **Anti-rubber-stamp** — sign-off forces a written one-line verdict + reason per genuine fork; a
  blanket "approve all" is not sufficient.

**Pairing is mandatory, not optional.** Emitting the large document alone — or emitting a
form-compliant-but-text-wall surface — is a **defect**, the same defect as a database-shaped HITL
surface. A process that produces a review document without its companion surface **has not
finished.** This holds even when the producing process is an ad-hoc Workflow with no governing
skill: the obligation attaches to the *act of emitting a review document*, not to any one skill.

---

## 6. Named Output Surfaces and Surface Schema

These are the recurring human-facing surfaces in the Momentum practice. Each is named so the
caps table (§2.2) has a stable reference. A surface type not listed here that produces
developer-facing output is a gap — the owning skill must declare its applicable cap.

| Surface Name | Produced by | Cap Reference |
|---|---|---|
| Situational report | Impetus | §2.2 row 1 |
| Finding card / divergence card | Assessment, Retro | §2.2 row 2 |
| Decision card | Decision skill | §2.2 row 3 |
| Pause-ask surface | Conductor mid-flight escalation | §2.2 row 4 |
| End-gate report section | Conductor end-gate renderer | §2.2 row 5 |
| Findings digest | Retro | §2.2 row 6 |
| Recommendations / next steps | Assessment | §2.2 row 7 |
| Conversational reply | Any session / conversational turn | §2.2 row 8 |
| Companion decision surface | Any process emitting a large review document (§5) | §2.2 row 9 |
| Pre-sprint plan gate | `sprint-planning` (final step) | §2.2 row 9 (companion-surface instance) |
| Post-sprint results gate | `conduct` end-gate + `retro` digest, fused | §2.2 row 9 (companion-surface instance) |

---

## 7. Cross-References — Existing Instances This Rule Generalizes

This rule generalizes two existing conduct-specific floor enforcement points. It does not
replace or contradict them — they are instances under this practice-wide umbrella.

### Conductor Pause-Ask Surface Contract (DEC-036 D5 Self-Sufficiency Floor)

**Location:** `skills/momentum/skills/conductor/references/escalation.md` — section "Pause-Ask Surface Contract (DEC-036 D5 Self-Sufficiency Floor)"

This is the original, conduct-specific statement of the self-sufficiency floor for mid-flight
pause-ask surfaces. The pause-ask output template there (What / Why / Evidence + three resolution
options) is the canonical template for that surface type. This rule generalizes the what/why/evidence
triple from "pause-ask only" to "all decision-relevant items on all surfaces."

### Conduct End-Gate Report Spec §9

**Location:** `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md` §9 — "Decision-grade presentation (DEC-036 D5)"

§9 is the conduct-report-specific instance of both halves (caps + floor). Its language — "collapse
routine, summarize clean items to a line, use collapsibles for depth-on-demand" and "every
finding/decision/divergence carries what / why-it-matters / evidence inline. A missing field is a
defect, not a blank card. The caps never trim these." — is the spine of this practice-wide rule.
This rule is the umbrella; §9 is the conduct-report instance under it. The two must never diverge.

---

## 8. Cascade Order

```
global:  ~/.claude/rules/decision-grade-presentation.md
project: .claude/rules/decision-grade-presentation.md
path:    .claude/rules/<path-scoped>/decision-grade-presentation.md
```

**What can be overridden at lower scope:**
- Per-surface budget values (§2.2) — project scope may tighten but not loosen a cap.
- Additional named surfaces for a project-specific skill.

**What cannot be overridden at any lower scope:**
- The caps-vs-floor boundary (§4) — the floor always wins, practice-wide.
- The three required fields (§3) — what/why/evidence are never optional for decision-relevant items.
- The core convention (§1) — effort never earns wider verbosity.
- The companion-surface obligation (§5) — a large review document without its paired decision surface is always a defect, regardless of which process produced it.
- The presentation-form leg (§5.1) — decision gates render as visual, purpose-first, diagrammed surfaces; non-overridable alongside the caps-vs-floor boundary.
