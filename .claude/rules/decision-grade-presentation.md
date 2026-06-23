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

## 5. Named Output Surfaces and Surface Schema

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

---

## 6. Cross-References — Existing Instances This Rule Generalizes

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

## 7. Cascade Order

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
