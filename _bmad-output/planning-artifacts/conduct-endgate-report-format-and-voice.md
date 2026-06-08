# Conduct End-Gate Report — Format & Voice Spec

**Status:** Reference standard, captured 2026-06-04 from the first real conduct end-gate report.
**Purpose:** Define how conduct's single human end-gate report must read and be structured, so the
deferred renderer reproduces this rather than reinventing it. This elaborates `sprint-dev-redesign-spec.md` §9
(which gives the bare section list + self-sufficiency mandate) with the **voice and organizing principles**
that make the report actually explain itself.

**Builds to:** DEC-035 D5 (legible auto-fix), DEC-035 D6 (functionality-organized report),
DEC-036 D3 (render dismissals), DEC-036 D4 (anti-rubber-stamp gate), DEC-036 D5 (decision-grade presentation).
**Built to by (downstream):** the conduct end-gate-rendering story, and the DEC-036 D5 decision-grade-presentation standard.
**Worked example:** `.momentum/handoffs/sprint-2026-06-02-conduct-core-hitl-report.html`.
**Reference implementation:** `.momentum/gen-endgate-report.py` (a one-off generator for the example; not the production renderer).

---

## 1. The one rule everything else serves

> The report must let a competent engineer **who did not watch the build** read it, understand what happened,
> and *re-explain it to a third party* — without opening a file, recalling prior context, or knowing internal jargon.

If a reader can't explain a section back in their own words, that section has failed. This is the acceptance test.

## 2. Audience: assume nothing

Write for someone who has never heard of conduct, sprint-dev, "the firehose," DEC-035/036, or the internal
component names. **Define every term inline on first use.** Lead each section with the plain-language point;
put supporting detail after. Never use a bare code symbol, file path, or ticket id as a headline.

## 3. Organizing principle: risk, not findings

The report is **not a findings catalog** — a catalog is just the firehose moved into a document, and it is the
exact failure this whole system exists to end. Instead:

- **Focus on the high-risk.** Surface the divergences that, left unfixed, would have caused real harm
  (silent shipping of broken/incorrect behavior; a safety mechanism that wouldn't fire; the build unable to run;
  a dangerous/irreversible default; security exposure). Tell each in full.
- **Collapse the routine.** Wording, consistency, doc-drift, reachability nits — auto-fixed and reported as a
  **count, not itemized.** Itemizing them is the firehose.
- Length tracks the **risk surface**, not the story count. A clean sprint yields a short report.

## 4. Section spine (fixed order)

| # | Section | What it does |
|---|---------|--------------|
| HERO | metrics strip | items built/merged · high-risk divergences caught · decisions for you · auto-fixed count · waved-off count · shipped-broken/blocked count |
| 01 | **What this is & what shipped** | The before/after in plain terms; the concrete capabilities now existing; an honest one-line completeness caveat pointing to §06. |
| 02 | **What each piece is for** | Every work item, one plain paragraph: its job + the guarantee it provides + what would go wrong without it. Enough to understand why a divergence there matters. |
| 03 | **Where it diverged — the high-risk moments** | The consequential divergences, each a scannable headline that expands to the 5-beat risk story (§5). Ordered scariest-first. Routine excluded. |
| 04 | **The decision(s) for you** | Only the stakes-class items the build refused to auto-fix. Each: plain background, what's actually at stake, options with cost/benefit, a recommendation. Anti-rubber-stamp gating (§8). |
| 05 | **Waved off & routine** | The dismissed findings (each with the reason it was safe to leave — DEC-036 D3), plus the routine remainder as a single count. |
| 06 | **How done is this, really?** | The honesty section (§7). What's live vs hollow; the explicit list of what stands between this and adoption; what approving actually does. |
| 07 | **Merge & push preview** | Commits/diffstat; the exact approve sequence; "push is a separate confirmation." |
| GATE | the single control | changes vs approve; copy-decision-as-prompt; approve disabled until decisions are acknowledged. |

## 5. The 5-beat divergence narrative (the heart of the report)

Every high-risk divergence is told as flowing prose with bold lead-ins, answering — in this order — the five
questions a reader needs to *judge* it. Do not show raw code/YAML/eval files; explain the reasoning.

1. **What this part of conduct does** — plain.
2. **Why we wrote a guarantee around it, and why that way** — the risk that shaped the contract.
   *(Answers "why did the eval exist / why was it written that way" — not by quoting it, by explaining its intent.)*
3. **Where reality diverged** — what the build got wrong, plainly.
4. **The risk that created, and what catching it removed** — the observable consequence had it shipped,
   and that review caught it before merge.
5. **Why the outcome is acceptable** — the resolved behavior matches the guarantee; it was re-verified.

Each card carries a **plain-language headline** (the risk in human terms) so the reader can scan and triage
which to open. See the worked example's §03 for the canonical rendering (collapsible cards, scariest-first).

## 6. Per-piece purpose (§02)

For *every* work item — not just the diverged ones — one plain paragraph: what its job was, the guarantee it
gives the system, and what would go wrong without it. This is the "enough context about every story so the
reader understands why a divergence matters" layer. Derive the guarantee from the contract's *intent*, never
from its raw syntax.

## 6a. Per-item review panel (the §02 expand) — enabling actual review, not rubber-stamping

The single biggest risk of an autonomous builder is that the human *approves without reviewing* — the LLM does
the coding and the human signs off blind. The cure is to put the reviewable material one click away on **every**
item. Each §02 item carries an **expand ("Review this work item")** containing, in this order:

1. **How it was verified — TESTING FIRST.** Before any code, show how we know it works:
   - *What had to be true* — the behaviors the frozen contract required, in plain language (the eval scenarios /
     review-claims translated into "the things it must do"), so the reader sees the test design.
   - *How it was checked* — the QA verification + the independent adversarial review + (for high-risk) the
     re-check. **Be honest about the strength of verification.** If it was structured inspection against the
     contract rather than live execution (e.g. markdown artifacts with a "skip" runtime harness), say so — never
     let "verified" be mistaken for "executed."
   - *Result* — the verdict and the concrete evidence.
2. **Why it's built this way — architectural rationale + references.** The design choice, with **explicit
   references to the governing decisions and spec sections** that drove it (name them), and the files changed.
3. **The actual diff.** The real change, embedded (collapsed `<pre>`, escaped, self-contained) so the developer
   can read the implementation themselves. This is the artifact that makes review real rather than notional.
4. **Visual evidence — for any item that changes user-facing UI (see §6b).**

Testing-first ordering is deliberate: the reader should judge *whether it's trustworthy* before reading the code,
and the diff is there to verify, not to take on faith.

## 6b. Visual evidence for UI changes (screenshots / GIFs)

**A diff does not show what the user sees.** For any work item that changes user-facing UI, the review panel's
verification block must **lead with visual evidence**: before/after **screenshots** (and a short **GIF** for an
interaction or animation), treated as the *primary* verification artifact for the visual change, with the code
diff as supporting detail. Capture them by actually running the app / driving the browser (e.g. the project's
run skill or browser automation), and embed them self-contained (committed image asset, or inline data-URI) so
the report stays a single portable file. If a UI item ships without a screenshot, that is a verification gap and
the panel must say so. (This sprint changed no UI — markdown/skills only — so no screenshots apply here; the rule
exists so conduct includes them automatically when a sprint does touch UI.)

## 7. The honesty / completeness section (§06)

State completeness plainly, even when it's awkward. Two tables — **what's live** vs **what's still hollow** —
and an explicit "what does approving actually do." If the system is a partial slice, say so up front (§01) and
in full here. The cardinal sin is a report that reads more finished than the thing is. (The first conduct report
oversold completeness; this section exists so that can't recur.)

## 8. Anti-rubber-stamp gate (DEC-036 D4)

- The Approve control ships **unchecked** — never pre-selected.
- Decision cards (§04) ship with **no option pre-selected**.
- **Approve is disabled** until every stakes decision is acknowledged *and* has a selection.
- Routine items require nothing — the forcing function applies only to the correctly-identified stakes items.
- The gate emits a copy-paste-able decision prompt; there is no Reject (changes vs approve only).

## 9. Decision-grade presentation (DEC-036 D5) — tight on the irrelevant, complete on the decision-relevant

**Parent standard:** `skills/momentum/references/rules/decision-grade-presentation.md` (practice-wide rule).
This section is the **conduct-report-specific instance** of that standard. The parent rule governs all
Momentum human-facing surfaces; this section applies it to the end-gate report. Where the parent and this
section appear to conflict, the parent rule is authoritative.

- **Caps** cut Specification-Fatigue material: collapse routine, summarize clean items to a line, use
  collapsibles for depth-on-demand.
- **Self-sufficiency floor (never cut):** every finding/decision/divergence carries what / why-it-matters /
  evidence *inline*. A missing field is a defect, not a blank card. The caps never trim these.

## 10. House style

Self-contained single `.html` — inline `<style>`+`<script>`, zero external dependencies (per
`anthropics/html-effectiveness`). Anthropic warm palette (ivory/slate/clay/olive tokens), serif headings,
numbered sections, severity chips, `<details>` disclosure for the divergence cards. A single `--fs-scale`
CSS variable for global font scaling (developers read these in a narrow viewer pane — make it legible and
adjustable). Open it in a real browser surface for the developer; verify the surface persists.

## 11. Provenance / lessons baked in

This standard was extracted after the first conduct end-gate report failed three ways the developer caught:
(1) terse one-line "findings" that explained nothing; (2) jargon throughout, so even "what shipped" was
unreadable; (3) overselling completeness. The fixes — the 5-beat risk narrative, assume-nothing voice,
risk-organization with routine collapsed, and the honesty section — are the load-bearing parts of this spec.
Do not regress them.
