---
content_origin: independent-confirmation
target: altitude-control-playbook
date: 2026-05-31
analyst_role: independent-confirmation-skeptic
note: >
  Task spec passed literal "undefined" for the output dir and date (unsubstituted
  template vars). Written to the project's real validation dir; date set to today (2026-05-31).
---

# Confirmation: Altitude / Verbosity Control Playbook (2026 mechanisms + "terse by default")

Independent verification of five claims against PRIMARY sources (vendor docs + the original
arXiv paper). Verdicts are based on what the primary source actually says, not on plausibility.

---

## Claim 1 — OpenAI exposes a `verbosity` parameter (GPT-5 family) controlling output length

**Verdict: CONFIRMED**

Primary sources:
- OpenAI API guide "Using the latest model" (developers.openai.com/api/docs/guides/latest-model)
- OpenAI Cookbook "GPT-5 New Params and Tools"
- OpenAI Cookbook "GPT-5.2 Prompting Guide"

Findings:
- Parameter exists, set at `text.verbosity` in the Responses API.
- Accepts exactly three values: `low`, `medium`, `high`. Default = `medium`.
- Cookbook quote: "low → terse UX, minimal prose. medium (default) → balanced detail.
  high → verbose, great for audits, teaching, or hand-offs."
- Guide: "for concise responses, set `text.verbosity` to `low`."
- Controls FINAL ANSWER length, not thinking depth (those are separate). "Keep prompts
  stable and use the param rather than re-writing."
- Available across the GPT-5 family (gpt-5, gpt-5.1, gpt-5.2, gpt-5.5, mini, nano).

No discrepancy with the original report.

---

## Claim 2 — Google Gemini exposes a `thinking_level` / thinking-budget control

**Verdict: CONFIRMED**

Primary source: Google "Gemini thinking" docs (ai.google.dev/gemini-api/docs/thinking).

Findings — TWO distinct controls:
- `thinkingBudget` (Gemini 2.5 series): integer token budget. 2.5 Pro range 128–32768
  (cannot disable); 2.5 Flash 0–24576 (0 disables); `-1` = dynamic thinking.
- `thinkingLevel` (Gemini 3 series, recommended going forward): categorical values.
  Current docs list `minimal | low | medium | high` with per-model defaults
  (e.g., 3.1 Pro default `high`, 3.1 Flash-Lite default `minimal`).
- Setting both `thinkingLevel` and `thinkingBudget` in one config returns an error;
  `thinkingBudget` is accepted on Gemini 3 only for backward compat and "may result
  in unexpected performance."

Nuance for the playbook: these are primarily REASONING/thinking-depth controls. They
affect total token spend (and indirectly output), but Gemini's nearest analog to a pure
output-length knob is `maxOutputTokens` plus prompt instructions — not `thinkingLevel`.
The claim as stated ("affecting reasoning/output") is accurate.

---

## Claim 3 — Anthropic Claude exposes an `effort` control and/or output-shaping controls

**Verdict: CONFIRMED**

Primary sources:
- Claude API docs "Effort" (platform.claude.com/docs/en/build-with-claude/effort)
- Claude API docs "Prompting best practices"

Findings:
- `effort` is set inside `output_config` (NOT top-level): `output_config: {effort: ...}`.
- Values: `low | medium | high | xhigh | max`. Default = `high` ("Setting effort to
  'high' produces exactly the same behavior as omitting the parameter").
- Supported on Opus 4.8, Mythos Preview, Opus 4.7, Opus 4.6, Sonnet 4.6, Opus 4.5.
  `xhigh` is Opus 4.7/4.8 only; `max` on the broader recent set.
- Crucially for an "altitude" playbook, effort "affects ALL tokens in the response,
  including text responses and explanations, tool calls and function arguments, and
  extended thinking." So unlike Gemini's thinking-only controls, Claude's `effort`
  genuinely shapes output verbosity too — lower effort yields terser text and fewer
  tool calls. This directly supports "and/or output-shaping controls."
- Additional output-shaping levers documented: a dedicated "Response length and verbosity"
  section, Structured Outputs (schema-constrained), an anti-markdown/anti-bullet prose
  snippet, and "respond directly without preamble" instructions.

No discrepancy with the original report.

---

## Claim 4 — "2025-2026 models are TERSE BY DEFAULT" is FALSE; YapBench (arXiv 2601.00624,
##           ~Jan 2026) found 2025-26 models trend MORE verbose, PERSISTING EVEN UNDER
##           EXPLICIT CONCISENESS INSTRUCTIONS

**Verdict: PARTIALLY-CONFIRMED (one load-bearing sub-claim is a MISATTRIBUTION)**

Primary sources:
- arXiv 2601.00624 "Do Chatbot LLMs Talk Too Much? The YapBench Benchmark"
  (Borisov, Gröger, Mikhael, Schreiber). Submitted 2 January 2026. ID confirmed real.
- Authors' blog (tabularis.ai/blog/yapbench) + HF Space leaderboard (tabularisai/YapBench).

What IS confirmed:
- Paper ID, title, ~Jan 2026 date: CONFIRMED (submitted 2026-01-02).
- 76 assistant LLMs evaluated; "order-of-magnitude spread in median excess length."
- Verbosity-over-time trend IS upward but MILD: paper reports r = 0.21
  ("The trend is mildly upward (r=0.21), suggesting that over time, unwanted 'yapping'
  tends to increase"). Blog states plainly: "Models released in 2025-2026 are, on
  average, more verbose than models from 2023-2024."
- Most concise model = gpt-3.5-turbo (a 2023 model). Paper body: best overall
  YapIndex = 23 (abstract/blog approximate it as "around 20" — minor figure rounding;
  treat 23 as the paper's stated number). It beats newer frontier models (Gemini-Pro,
  GPT-5, etc.). This supports "conciseness is not inherent to newer/larger models."

What is NOT confirmed (the misattribution):
- The clause "persisting even under explicit conciseness instructions" is NOT something
  YapBench tests or claims. YapBench scores responses to "brevity-IDEAL" prompts — prompts
  where brevity is the natural ideal (ambiguous inputs, closed-form factual Qs, one-line
  coding tasks). It does NOT add an explicit "be concise/brief" directive and then measure
  persistence. The full-text and the authors' blog contain no such finding. The original
  report appears to have grafted a stronger claim (instruction-resistant verbosity) onto
  YapBench that the paper does not make. This should be corrected.

What is OVERSTATED in the framing:
- "TERSE BY DEFAULT is FALSE" is too absolute. The honest reading is: the population
  trend is mildly more verbose over time and newer ≠ terser, BUT r=0.21 is a weak
  correlation with large model-to-model variance. And there is countervailing PRIMARY
  evidence that some specific 2026 flagships are deliberately tuned terser by default:
  Anthropic's docs say its latest models are "Less verbose... may skip detailed summaries
  for efficiency" and "calibrate response length to task complexity"; OpenAI's GPT-5.5
  guide says the model "tends to be efficient, direct, and task-oriented by default" and
  GPT-5.2 is "generally lower verbosity." So "terse by default" is FALSE as a blanket
  statement about the 2025-26 population (YapBench), but is partly TRUE for several
  individually-tuned 2026 flagships per their own vendor docs. The defensible synthesis:
  do not ASSUME terseness — measure it and control it explicitly.

Net: the YapBench attribution is real and the core direction (more verbose on average,
newer ≠ terser) holds, but (a) the trend is weak (r=0.21), and (b) the "persists under
explicit conciseness instructions" rider is a confabulated extension of the paper.

---

## Claim 5 — System-prompt patterns that empirically reduce verbosity: measurable caps
##           (word/section limits), executive-summary-first, persona/audience framing,
##           output schemas/templates

**Verdict: CONFIRMED**

Primary sources:
- OpenAI Cookbook "GPT-5.2 Prompting Guide"
- OpenAI "Using the latest model" (GPT-5.5) guide
- Claude API "Prompting best practices"

Findings (all four pattern families are vendor-recommended in primary docs):
- Measurable caps: GPT-5.2 guide prescribes "Default: 3–6 sentences or ≤5 bullets for
  typical answers"; "≤2 sentences" for simple yes/no; GPT-5.5 guide says "specify word
  budgets, section counts, table widths, or JSON-only output where needed."
- Executive-summary-first / tagged structure: GPT-5.2 guide's complex-task template is
  "1 short overview paragraph then ≤5 bullets tagged: What changed, Where, Risks,
  Next steps, Open questions." (This is an exec-summary-then-structured-bullets template.)
- Output schemas/templates: Anthropic "Structured Outputs" (schema-constrained) +
  "respond directly without preamble"; the GPT-5.2 tagged-bullet template above.
- Persona/audience framing: Anthropic "Give Claude a role" (system-prompt role focuses
  tone/behavior). Note: vendor docs frame persona primarily as a tone/behavior lever, not
  explicitly as a verbosity-reduction technique — so "persona/audience framing reduces
  verbosity" is the weakest-evidenced sub-pattern (plausible, widely used, but not
  documented by vendors as a measured verbosity reducer). The other three families are
  directly and explicitly documented.
- Anthropic adds an empirically-flavored tip: "Positive examples showing how Claude can
  communicate with the appropriate level of concision tend to be more effective than
  negative examples or instructions that tell the model what not to do."

Caveat on "empirically": these are vendor RECOMMENDATIONS with qualitative backing
(and the GPT-5 verbosity-token-scaling table low 731 / med 1017 / high 1263 is a small
empirical illustration), not a controlled study isolating each prompt pattern's effect.
The patterns are confirmed as documented best practice; "empirically reduce" is a fair
but slightly generous gloss.

---

## Cross-cutting note for the playbook (NEWER evidence the framing should incorporate)

There is a genuine tension in the primary record that the playbook should surface rather
than paper over:
- POPULATION evidence (YapBench, Jan 2026): newer models are NOT reliably terser; mild
  upward verbosity trend (r=0.21); a 2023 model (gpt-3.5-turbo) is the most concise.
- VENDOR evidence (OpenAI GPT-5.2/5.5 guides; Anthropic prompting docs, 2026): several
  specific 2026 flagships are deliberately tuned to be more concise / task-calibrated by
  default.
Both are true. The actionable conclusion is the playbook's real value: do not rely on
default behavior — use the API knobs (`text.verbosity` low; Claude `effort` low/medium;
Gemini `thinkingLevel`/`maxOutputTokens`) AND explicit prompt caps/templates, and MEASURE.
