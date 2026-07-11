---
content_origin: adversarial-verification
sub_question: "sq5-communication-altitude-control"
date: 2026-05-31
---

# Adversarial Verification — SQ5 (Communicating at the Right Altitude)

Posture: try to refute. Default to skepticism. A claim is "confirmed" only when the cited
source actually contains it AND is current.

## Summary judgment

The thread is mostly well-sourced on the **vendor-parameter facts** — the four primary
vendor docs (OpenAI GPT-5 cookbook, OpenAI GPT-5.5 prompt guidance, Claude Opus 4.8
prompting best practices, Gemini 3 developer guide) genuinely contain the parameter
names, defaults, and verbatim quotes attributed to them. Those load-bearing claims hold up
under direct re-fetch.

However, three meaningful problems surface:

1. **The central narrative ("terseness is now the default posture across vendors") is
   contradicted by fresh 2026 evidence.** The YapBench benchmark (arXiv 2601.00624, Jan 2026,
   76 models) finds the *opposite trend*: models released in 2025–2026 are on average MORE
   verbose than 2023–2024 models, and the worst frontier models over-generate 10–20x. The
   thread's "default is now terse, steer up not down" framing is a vendor-marketing posture,
   not an empirically settled fact. The thread's own "debates" section half-acknowledges this
   but resolves it too charitably toward the vendors.

2. **Two academic/citation mismatches.** Finding 10 attributes a "pairwise preference
   optimization rewards length" causal claim and a "human-written or machine-generated targets"
   quote to arXiv 2506.08686 — neither appears in that paper's abstract. The verbosity-bias /
   DPO-length-bias literature is real and robust, but it lives in *other* papers (2403.19159,
   2406.10957, 2411.07858), so the citation is mis-attributed even though the claim is broadly
   true.

3. **One vendor-doc finding is outdated.** Finding 9 (Claude Code output styles) says there are
   THREE built-in styles (Default/Explanatory/Learning) and that custom styles are made via
   `/output-style:new`. Current docs list FOUR built-ins (Default/**Proactive**/Explanatory/
   Learning), and the `/output-style` command was deprecated (v2.1.73) and removed (v2.1.91) —
   you now use `/config`. The core "modifies the system prompt directly, applies every response"
   claim is verbatim-correct, but the specifics are stale.

Also: one practitioner sub-claim (Finding 6, "Gemini 3 may over-analyze overly complex prompt
engineering") could NOT be found in the cited Schmid post; and Finding 7's marquee quote about
"word limits, bullet counts, section counts, or strict templates" does NOT appear in the Claude
doc it is primarily cited to — it is aggregated/paraphrased from third-party guides.

Overall reliability: **medium**. The parameter mechanics are solid; the cross-vendor "everyone
is terse now" thesis is over-stated and partly contradicted by 2026 benchmarks; a few citations
are loose.

---

## Load-bearing claims checked

### Finding 1 — GPT-5 `verbosity` param (low/med/high), decoupled from `reasoning_effort`
**Verdict: confirmed.**
Re-fetched the OpenAI cookbook (2025-08-07). It contains the verbatim quote: "The verbosity
parameter reliably scales both the length and depth of the model's output while preserving
correctness and reasoning quality — without changing the underlying prompt." The low/medium/high
values and the separation from reasoning_effort (minimal/medium/...) are present.
Caveat: the specific token counts (560 / 849 / 1288) are *example-specific* — another rendering
of the same doc reports 731 / 1017 / 1263 for a different prompt. So the exact numbers are
illustrative, not a spec. Directionally correct.
Source: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools

### Finding 2 — GPT-5.5 `text.verbosity` (default medium), plain-paragraph default, senior-audience example
**Verdict: confirmed.**
The OpenAI prompt-guidance doc has a dedicated GPT-5.5 section stating "The API default for
`text.verbosity` is `medium`; use `low` when you prefer shorter, more concise responses,"
plus "Use plain paragraphs as the default format" and the exact example "Write for a senior
business audience. Keep the answer under 400 words…" Covers GPT-5.5/5.4/5.3-Codex/5.2/5.1/5/4.1.
Source: https://developers.openai.com/api/docs/guides/prompt-guidance

### Finding 3 — Claude Opus 4.8 calibrates length to judged complexity; positive > negative examples
**Verdict: confirmed.**
The Claude prompting-best-practices doc (the page uses a `<NextOpus />` placeholder that resolves
to Claude Opus 4.8 — confirmed by the anchor `#prompting-claude-opus-4-8` and model-string
examples `claude-opus-4-8`) contains verbatim: "calibrates response length to how complex it
judges the task to be, rather than defaulting to a fixed verbosity"; the recommended snippet
"Provide concise, focused responses. Skip non-essential context, and keep examples minimal."; and
"Positive examples showing how Claude can communicate with the appropriate level of concision
tend to be more effective than negative examples…"
Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

### Finding 4 — Claude `effort` param scopes work at low/medium; thinking off unless adaptive set
**Verdict: confirmed, but the thread's framing overreaches.**
Verbatim in the doc: "respects effort levels strictly, especially at the low end. At `low` and
`medium`, the model scopes its work to what was asked rather than going above and beyond." The
five effort levels (low/medium/high/xhigh/max) are confirmed, and "thinking is off unless you
explicitly set `thinking: {type: \"adaptive\"}`" is verbatim.
CAVEAT (skeptic note): the thread positions low/medium effort as "the lever to pull for tighter,
less-expansive *responses*" — conflating *scope of work / thinking depth* with *output verbosity*.
The doc keeps these in separate sections and actually warns AGAINST low effort (under-thinking
risk), recommending you start at `xhigh`/`high`. Effort is a cost/intelligence knob, not a
verbosity knob. The quotes are accurate; the interpretation muddies the parameter's purpose.
Source: same as Finding 3.

### Finding 5 — Gemini 3 less verbose by default; `thinking_level` replaces `thinking_budget`
**Verdict: confirmed.**
Gemini 3 dev guide (last updated 2026-05-29) contains "By default, Gemini 3 is less verbose and
prefers providing direct, efficient answers," the thinking_level values, "You cannot use both
`thinking_level` and the legacy `thinking_budget` parameter in the same request" (returns 400),
and the temperature-1.0 recommendation with the looping/degradation warning.
Source: https://ai.google.dev/gemini-api/docs/gemini-3

### Finding 6 — Schmid: explicit "Verbosity:" line + `<output_format>` Executive Summary
**Verdict: partially-supported.**
Confirmed in the Nov 19 2025 post: the `Verbosity: [Low/Medium/High]` constraint, the
`<output_format>` section with "Executive Summary," and "If you require a more conversational or
'chatty' persona, you must explicitly ask for it." NOT confirmed: the claim that the post warns
"Gemini 3 may over-analyze verbose or overly complex prompt engineering" — that specific warning
was not found in the post (it stresses empirical iteration instead). The over-analysis sub-claim
should be dropped or re-sourced.
Source: https://www.philschmid.de/gemini-3-prompt-practices

### Finding 7 — "be concise is too vague; use measurable constraints"
**Verdict: partially-supported (citation mismatch).**
The principle is sound and widely echoed, BUT the marquee quote ("Terms like brief, concise, or
detailed are subjective; verbosity control works best when it is explicit and measurable through
word limits, bullet counts, section counts, or strict templates") does NOT appear in the Claude
best-practices doc it is primarily cited to. The Claude doc's actual guidance is "Be specific
about the desired output format and constraints" and "tell Claude what to do instead of what not
to do" — adjacent, but not that quote. The quote is aggregated from third-party 2026 guides
(DigitalOcean/Lakera per the raw file), which the finding admits ("aggregated in search").
Treat as practitioner consensus, not a vendor quote.

### Finding 9 — Claude Code output styles
**Verdict: outdated / partially-supported.**
Verbatim-correct: "Output styles modify the system prompt directly and apply to every response."
WRONG/STALE specifics: current docs list FOUR built-in styles — Default, **Proactive**,
Explanatory, Learning — not three. The `/output-style` command and `/output-style:new` were
deprecated (v2.1.73) and removed (v2.1.91); selection is now via `/config` (saved to
`.claude/settings.local.json` still). Custom styles also gained `keep-coding-instructions` and
`force-for-plugin` frontmatter. Core claim survives; the enumeration and command are out of date.
Source: https://code.claude.com/docs/en/output-styles

### Finding 10 — Academic verbosity bias (arXiv 2506.08686)
**Verdict: partially-supported (mis-attributed evidence).**
Confirmed: title "Brevity is the soul of sustainability: Characterizing LLM response lengths,"
author list, "12 LLMs" (across 5 datasets), ACL 2025 Findings, "substantially longer than
necessary." NOT in that paper's abstract: (a) the "pairwise preference optimization rewards
length" causal attribution, and (b) the "longer than target responses … regardless of whether
targets are human-written or machine-generated" quote. Those belong to the broader DPO/RLHF
length-bias literature (arXiv 2403.19159 "Disentangling Length from Quality in DPO";
2406.10957; 2411.07858 "Verbosity ≠ Veracity"). The claim is true of the field; the citation
is wrong. Down-grade confidence and re-attribute.
Better sources for the causal claim:
- https://arxiv.org/abs/2403.19159 (DPO length bias)
- https://arxiv.org/pdf/2411.07858 (verbosity compensation behavior)

### Finding 11 — length-control frontier (Plan-and-Write, Hansel, dynamic feedback)
**Verdict: confirmed (papers exist).**
Plan-and-Write (arXiv 2511.01807, Nov 3 2025, Akinfaderin/Subramanian/Sehwag) confirmed:
"structure-guided length control … without model retraining," prompt-engineering planning +
word-counting. The cluster (Hansel 2412.14033, dynamic feedback 2601.01768, precise length
control 2412.11937) is real and recent. Minor caveat: the specific "write a 500-word
composition" phrasing wasn't located in the Plan-and-Write abstract, but the under-addressed
length-control framing is present. The frontier characterization holds.

---

## Training-data smell test (ungrounded / weakly-sourced filler)

- **Finding 8 (persona "ROLE+TASK+CONTEXT+INSTRUCTIONS" / "senior reviewing a junior")** — sole
  source is a generic Medium "Ultimate Guide to Prompt Engineering 2025" listicle. The pattern is
  real and uncontroversial, but the framing reads like generic prompt-engineering boilerplate that
  could have been written from training-data priors rather than a primary/authoritative source.
  Confidence "medium" is appropriate; do not elevate.
- **Finding 7's marquee quote** — presented as if vendor-sourced (Claude docs) but is actually
  third-party aggregation. The "5 bullets, each under 15 words not be concise" line has the cadence
  of SEO prompt-engineering content. True in spirit, weak in provenance.
- **The cross-vendor synthesis claim "terseness is now the default posture, steer UP not DOWN"** —
  this generalization is asserted more confidently than the evidence supports. Vendor docs say it
  about their own latest models; it is not a measured cross-vendor fact (see contradicting evidence).

## Contradicting / qualifying evidence (recent, 2025–2026)

- **YapBench (arXiv 2601.00624, Jan 2026; tabularis.ai), 76 models incl. OpenAI/Anthropic/Google:**
  directly contradicts the "default is terse now" thesis. Finds models released in 2025–2026 are on
  average MORE verbose than 2023–2024 models ("length bias in training is getting worse, not
  better"); worst models over-generate 10–20x; GPT-3.5-Turbo is among the *most* concise. This is the
  strongest qualifier: vendor "well-calibrated/less-verbose-by-default" claims are not borne out as a
  population-level trend.
- **GPT-5 verbosity parameter has real-world failure modes:** Azure does not support
  reasoning_effort/verbosity on the standard gpt-5-chat model (2025-04-01-preview); LangChain has a
  documented bug where verbosity conflicts with structured output (GitHub issue #32492). So the
  "first-class, just-set-the-knob" framing has integration caveats the thread omits.
- **Verbosity-compensation literature (arXiv 2411.07858) shows the problem persists *even under
  explicit conciseness instructions*** (VC frequencies 13.6%–74% by model) — qualifies the thread's
  optimistic "measurable constraints solve it" framing.
- **GPT-5 cookbook token counts are not stable** (560/849/1288 vs 731/1017/1263 across renderings) —
  evidence the numeric "scaling" is anecdotal per-prompt, not a guaranteed spec.

## Net

Parameter facts: solid. Cross-vendor "terse-by-default" thesis: over-stated and partly
contradicted by 2026 benchmarks. Citations: two academic mis-attributions and one stale vendor
enumeration. Recommend: (1) soften the "steer up not down" generalization and cite YapBench as a
counterweight; (2) re-attribute the DPO/length-bias causal claim; (3) refresh the output-styles
enumeration to four styles + `/config`; (4) drop or re-source the Schmid "over-analyze" sub-claim.
