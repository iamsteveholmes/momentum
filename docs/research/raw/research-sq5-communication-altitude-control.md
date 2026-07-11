---
content_origin: web-discovery
sub_question: "sq5-communication-altitude-control"
date: 2026-05-31
---

# SQ5 — Making LLMs Communicate at the Right Altitude

## Synthesis

By mid-2026, "communicating at the right altitude" — having an LLM brief you in summaries and principles instead of drowning you in detail — is governed by three converging levers: (1) **first-class API parameters** that the frontier vendors now ship specifically to scale output length/depth independently of the prompt; (2) **default model behavior** that has shifted decisively toward conciseness in the 2025–2026 model generation; and (3) **prompting and configuration patterns** that steer altitude through measurable constraints, output-format directives, and persona framing.

On the parameter front, the single biggest 2025–2026 development is the separation of *how much the model thinks* from *how much it says*. OpenAI's GPT-5 family (Aug 2025) introduced an explicit `verbosity` parameter (`low`/`medium`/`high`) decoupled from `reasoning_effort` (`minimal`/`medium`/`high`); GPT-5.5 retains `text.verbosity` and defaults it to `medium`. Google's Gemini 3 replaced the older `thinking_budget` with a discrete `thinking_level` (`minimal`/`low`/`medium`/`high`) and ships *less verbose by default*. Anthropic's Claude Opus 4.8 does not expose a verbosity knob but instead **calibrates response length to judged task complexity** and exposes an `effort` parameter (`low`→`max`) plus adaptive thinking. The clear cross-vendor trend: terseness is now the default posture, and you must explicitly steer *up* toward chattiness rather than steer *down* toward brevity.

On the prompting front, every primary vendor source converges on the same principle: vague words like "be concise" underperform **measurable, explicit constraints** (word counts, bullet counts, section limits, templates) and **positive examples of the desired concision** outperform negative "don't do X" instructions. Format steering matters too — GPT-5.5 guidance says to default to plain paragraphs and reserve bullets/headers for when they genuinely aid comprehension. The classic "brief me as a senior would brief a junior" pattern shows up as persona + audience + length framing (e.g., "You're a senior legal analyst. Summarize this deal in plain English… under 150 words"). Claude Code's **output styles** (Default/Explanatory/Learning, plus custom) operationalize altitude as a persistent system-prompt-level setting.

Academic work in 2025–2026 frames *why* this matters: LLMs exhibit a documented **verbosity bias** — responses are significantly longer than necessary, partly an artifact of pairwise preference optimization rewarding length — which degrades UX and sustainability. A growing body of length-control research (Plan-and-Write, Hansel, dynamic length-feedback, precise length control) attacks the problem at the training/decoding level rather than the prompt level.

A notable disagreement: vendor docs (Claude, Gemini) say the new models are *already* well-calibrated and tell you to *remove* scaffolding that forces brevity/structure, while practitioner and academic sources still treat verbosity as a live problem requiring active constraint. The reconciliation is generational: the calibration claims are about the newest models specifically, while the verbosity-bias literature benchmarks broader/older model populations.

## Key Findings

### Finding 1 — GPT-5 introduced a dedicated `verbosity` parameter decoupled from reasoning
- **Claim:** OpenAI's GPT-5 (Aug 2025) added a `verbosity` parameter with `low`/`medium`(default)/`high` that "reliably scales both the length and depth of the model's output while preserving correctness" without rewriting the prompt — separate from `reasoning_effort` (`minimal`/`medium`/`high`) which controls thinking.
- **Evidence:** "Low: Produces terse responses with minimal prose… 560 output tokens. Medium… 849 tokens… High… 1,288 tokens with comprehensive commentary." Both params supported in Responses + Chat Completions APIs for gpt-5/-mini/-nano.
- **Source:** "GPT-5 New Params and Tools" — OpenAI Cookbook
- **URL:** https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools
- **Date:** 2025-08-07
- **Type:** vendor-docs
- **Confidence:** high

### Finding 2 — GPT-5.5 keeps `text.verbosity` (default medium); use `low` for concise output and define length explicitly
- **Claim:** For the latest OpenAI models the parameter is `text.verbosity` (defaults to `medium`); set it `low` "when you prefer shorter, more concise responses." Guidance: "give enough context for the user to understand and trust the answer, then stop," and define both voice and length explicitly (e.g., "Write for a senior business audience. Keep the answer under 400 words. Use short paragraphs and only include bullets when they improve scannability").
- **Evidence:** "let formatting serve comprehension. Use plain paragraphs as the default format for normal conversation" — reserve bullets/headers for genuine clarity gains, not defaults.
- **Source:** "Prompt guidance" — OpenAI API Docs
- **URL:** https://developers.openai.com/api/docs/guides/prompt-guidance
- **Date:** 2026 (covers GPT-5.5/5.4/5.3-Codex)
- **Type:** vendor-docs
- **Confidence:** high

### Finding 3 — Claude Opus 4.8 calibrates length to task complexity; to reduce verbosity use positive concision examples
- **Claim:** Claude Opus 4.8 "calibrates response length to how complex it judges the task to be, rather than defaulting to a fixed verbosity" — shorter on simple lookups, longer on open-ended analysis. To decrease verbosity, add an explicit instruction; positive examples of appropriate concision beat negative "don't" instructions.
- **Evidence:** Recommended snippet: "Provide concise, focused responses. Skip non-essential context, and keep examples minimal." And: "Positive examples showing how Claude can communicate with the appropriate level of concision tend to be more effective than negative examples or instructions that tell the model what not to do."
- **Source:** "Prompting best practices" — Claude API Docs
- **URL:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- **Date:** 2026 (covers Claude Opus 4.8 / 4.7 / Sonnet 4.6 / Haiku 4.5)
- **Type:** vendor-docs
- **Confidence:** high

### Finding 4 — Claude's `effort` parameter (low→max) controls scope/thinking depth, which indirectly controls altitude
- **Claim:** Claude Opus 4.8 exposes an `effort` parameter; at `low`/`medium` "the model scopes its work to what was asked rather than going above and beyond," good for latency/cost. Thinking is off by default unless `thinking: {type: "adaptive"}` is set. This is the lever to pull for tighter, less-expansive responses on scoped tasks.
- **Evidence:** "Claude Opus 4.8 respects effort levels strictly, especially at the low end. At low and medium, the model scopes its work to what was asked rather than going above and beyond." Also: removing scaffolding that forces interim status messages is now recommended because the model provides well-calibrated updates itself.
- **Source:** "Prompting best practices" — Claude API Docs
- **URL:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- **Date:** 2026
- **Type:** vendor-docs
- **Confidence:** high

### Finding 5 — Gemini 3 is less verbose by default; `thinking_level` replaces `thinking_budget`
- **Claim:** "By default, Gemini 3 is less verbose and prefers providing direct, efficient answers." The `thinking_level` parameter (`minimal`/`low`/`medium`/`high`) replaces the legacy `thinking_budget` (cannot use both in one request) and controls reasoning depth. To get verbose output you must explicitly steer (e.g., "Explain this as a friendly, talkative assistant").
- **Evidence:** "`low`: Minimizes latency and cost. Best for simple instruction following, chat, or high-throughput applications." Temperature should stay at default 1.0; lowering it can cause looping/degradation.
- **Source:** "Gemini 3 Developer Guide — generateContent API" — Google AI for Developers
- **URL:** https://ai.google.dev/gemini-api/docs/gemini-3
- **Date:** 2026-05-29 (last updated)
- **Type:** vendor-docs
- **Confidence:** high

### Finding 6 — Practitioner guidance: place an explicit "Verbosity: [Low/Medium/High]" in Gemini 3 system constraints; default to directness
- **Claim:** Named expert Philipp Schmid recommends putting an explicit `Verbosity: [Low/Medium/High]` line in the system constraints for Gemini 3, and using a dedicated `<output_format>` section (e.g., "Executive Summary: [2 sentence overview]") to steer altitude. Gemini 3 "may over-analyze verbose or overly complex prompt engineering techniques" — prefer direct, clear instructions.
- **Evidence:** "If you require a more conversational or 'chatty' persona, you must explicitly ask for it." Self-review step: "Is the tone authentic to the requested persona?"
- **Source:** "Gemini 3 Prompting: Best Practices for General Usage" — Philipp Schmid (philschmid.de)
- **URL:** https://www.philschmid.de/gemini-3-prompt-practices
- **Date:** 2025-11-19
- **Type:** blog (named expert / Google DeepMind)
- **Confidence:** high

### Finding 7 — Cross-cutting prompting principle: "be concise" is too vague; use measurable constraints
- **Claim:** The most reliable altitude control is explicit and measurable: word limits, bullet counts, section counts, or strict templates — not subjective adjectives. The recommended pattern is **directive + constraints + format**.
- **Evidence:** "Terms like 'brief,' 'concise,' or 'detailed' are subjective; verbosity control works best when it is explicit and measurable through word limits, bullet counts, section counts, or strict templates." / "Be specific: '5 bullets, each under 15 words' not 'be concise.'"
- **Source:** Claude API Docs (prompting best practices) + DigitalOcean / Lakera prompt-engineering 2026 guides (aggregated in search)
- **URL:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- **Date:** 2026
- **Type:** vendor-docs
- **Confidence:** high

### Finding 8 — The "brief me as a senior reviewing a junior" pattern = persona + audience + length
- **Claim:** The senior-briefing pattern is implemented as role + audience-level + length constraint, leveraging the model's training on high-quality domain data to hit professional altitude. Example: "You're a senior legal analyst. Summarize this deal in plain English" with a length cap (≤150 words).
- **Evidence:** "Using persona-based prompting, like 'You are a senior data scientist… Explain… to a junior developer,' helps LLMs provide responses tailored to a specific expertise level and audience." A complete structure = ROLE + TASK + CONTEXT (audience knowledge level) + INSTRUCTIONS.
- **Source:** "The Ultimate Guide to Prompt Engineering in 2025" / "Module 2: Prompt Structure & Role Engineering" (Medium, aggregated)
- **URL:** https://medium.com/@generativeai.saif/the-ultimate-guide-to-prompt-engineering-in-2025-mastering-llm-interactions-8b88c5cf65b6
- **Date:** 2025
- **Type:** blog
- **Confidence:** medium

### Finding 9 — Claude Code "output styles" operationalize altitude as a persistent system-prompt setting
- **Claim:** Output styles modify the Claude Code system prompt directly and apply to every response. Three built-ins: **Default** (concise, task-focused), **Explanatory** (narrated reasoning/"Insights"), **Learning** (collaborative, asks you to write code). Custom styles via `/output-style:new`; selection persists in `.claude/settings.local.json`.
- **Evidence:** "Output styles modify the system prompt directly and apply to every response, giving you fine-grained control over how Claude Code communicates." Default style "is concise, and targeted mainly at solving software engineering tasks."
- **Source:** "Output styles" — Claude Code Docs
- **URL:** https://code.claude.com/docs/en/output-styles
- **Date:** 2025
- **Type:** vendor-docs
- **Confidence:** high

### Finding 10 — Academic: documented verbosity bias makes responses longer than necessary
- **Claim:** LLM responses are characterized as significantly longer than necessary across tasks/domains; this verbosity is partly an artifact of pairwise preference optimization rewarding length, harming UX, evaluation fairness, and sustainability (compute/energy). Mitigations include prompt compression (e.g., LLM-Lingua) and brevity-rewarding training.
- **Evidence:** "Brevity is the soul of sustainability" — and a separate finding that "LLM-generated responses are significantly longer than target responses for factual questions, regardless of whether targets are human-written or machine-generated." Benchmarking spanned 12 LLMs.
- **Source:** "Brevity is the soul of sustainability: Characterizing LLM response lengths" (Poddar, Koley, Misra, Misra et al.) — arXiv:2506.08686
- **URL:** https://arxiv.org/pdf/2506.08686
- **Date:** 2025-06
- **Type:** peer-reviewed (arXiv preprint)
- **Confidence:** medium

### Finding 11 — Academic: dedicated length-control methods (training/decoding level) are an active 2025–2026 frontier
- **Claim:** Multiple 2025–2026 papers attack length/altitude control without prompt rewriting: Plan-and-Write (structure-guided length control, no retraining; KDD 2025 Prompt Optimization workshop), Hansel (output-length controlling framework), precise length-control via SFT/PPO/DPO/ORPO, and dynamic length-feedback so models track their own output length.
- **Evidence:** Models "often struggle with strictly adhering to length constraints when given queries like 'write a 500-word composition'"; feedback mechanisms let LLMs "track and dynamically adjust their output length."
- **Source:** Search aggregation of arXiv length-control papers (Plan-and-Write 2511.01807; dynamic feedback 2601.01768; precise length control 2412.11937; Hansel 2412.14033)
- **URL:** https://arxiv.org/pdf/2511.01807
- **Date:** 2025–2026
- **Type:** peer-reviewed (arXiv preprints)
- **Confidence:** medium

## Named Frameworks

- **`verbosity` parameter (OpenAI GPT-5 / GPT-5.5 `text.verbosity`)** — low/medium/high; scales output length & depth independent of prompt and of reasoning.
- **`reasoning_effort` parameter (OpenAI GPT-5)** — minimal/medium/high; controls thinking-token allocation (orthogonal to verbosity).
- **`effort` parameter (Anthropic Claude Opus 4.8)** — low/medium/high/xhigh/max; scopes work and thinking depth; strict at low end.
- **Adaptive thinking (`thinking: {type: "adaptive"}`) — Claude Opus 4.8** — off by default; steerable trigger.
- **`thinking_level` (Google Gemini 3)** — minimal/low/medium/high; replaces legacy `thinking_budget`.
- **Output Styles (Claude Code)** — Default / Explanatory / Learning + custom; persistent system-prompt-level communication-altitude control.
- **directive + constraints + format** — the canonical prompt structure for altitude control.
- **ROLE + TASK + CONTEXT + INSTRUCTIONS** — persona/audience-level framing (the "senior briefing a junior" pattern).
- **Plan-and-Write / Hansel / dynamic length-feedback** — academic length-control frameworks (no-retraining and training-based).
- **LLM-Lingua** — prompt-compression technique referenced for brevity.

## Debates & Tensions

1. **"Already calibrated" vs. "still too verbose."** Vendor docs (Claude Opus 4.8, Gemini 3) state the newest models self-calibrate length and advise *removing* brevity/structure scaffolding. Academic work (Brevity-is-the-soul-of-sustainability; length-control papers) still treats verbosity bias as a live, measurable defect. Reconciliation: vendor claims are model-specific to the very latest generation; the literature benchmarks broader/older populations.

2. **Parameter vs. prompt.** OpenAI and Google expose explicit verbosity/thinking knobs and say to prefer them over rewriting prompts. Anthropic deliberately does *not* ship a verbosity parameter, instead relying on task-complexity calibration plus prompt-level concision examples and the `effort` lever. So "the right altitude control" differs by vendor: a setting (OpenAI/Google) vs. a behavior + prompt pattern (Anthropic).

3. **Reasoning depth ≠ output verbosity.** GPT-5 explicitly separates them (you can reason hard but answer tersely). Gemini conflates reasoning into `thinking_level` and handles output verbosity only via prompt steering. Practitioners sometimes confuse the two, leading to either over-thinking or over-talking.

4. **Negative vs. positive instruction.** Claude docs say positive examples of good concision beat negative "don't over-explain" instructions; much practitioner content still leans on prohibitions. Vendor guidance is the stronger signal here.

5. **Format defaults.** OpenAI now advises plain paragraphs as the default and bullets only when they aid comprehension — pushing back on the common practitioner habit of always-bullet output. This is a subtle altitude question (structure can either summarize *or* fragment).

## Sources

- OpenAI Cookbook — "GPT-5 New Params and Tools" — https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools — 2025-08-07 — vendor-docs
- OpenAI API Docs — "Prompt guidance" (GPT-5.5) — https://developers.openai.com/api/docs/guides/prompt-guidance — 2026 — vendor-docs
- Claude API Docs — "Prompting best practices" — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices — 2026 — vendor-docs
- Claude Code Docs — "Output styles" — https://code.claude.com/docs/en/output-styles — 2025 — vendor-docs
- Google AI for Developers — "Gemini 3 Developer Guide (generateContent API)" — https://ai.google.dev/gemini-api/docs/gemini-3 — 2026-05-29 — vendor-docs
- Philipp Schmid — "Gemini 3 Prompting: Best Practices for General Usage" — https://www.philschmid.de/gemini-3-prompt-practices — 2025-11-19 — blog (named expert)
- arXiv 2506.08686 — "Brevity is the soul of sustainability: Characterizing LLM response lengths" — https://arxiv.org/pdf/2506.08686 — 2025-06 — peer-reviewed (preprint)
- arXiv 2511.01807 — "Plan-and-Write: Structure-Guided Length Control for LLMs without Model Retraining" — https://arxiv.org/pdf/2511.01807 — 2025 — peer-reviewed (preprint)
- arXiv 2601.01768 — "Can LLMs Track Their Output Length? A Dynamic Feedback Mechanism for Precise Length Regulation" — https://arxiv.org/pdf/2601.01768 — 2026 — peer-reviewed (preprint)
- arXiv 2412.14033 — "Hansel: Output Length Controlling Framework for Large Language Models" — https://arxiv.org/pdf/2412.14033 — 2024-12 — peer-reviewed (preprint)
- Medium — "The Ultimate Guide to Prompt Engineering in 2025" (persona/altitude patterns) — https://medium.com/@generativeai.saif/the-ultimate-guide-to-prompt-engineering-in-2025-mastering-llm-interactions-8b88c5cf65b6 — 2025 — blog
- SparkCo — "Mastering GPT-5: Verbosity and Reasoning Effort Controls" — https://sparkco.ai/blog/mastering-gpt-5-verbosity-and-reasoning-effort-controls — 2025 — blog (corroborating)
- LaoZhang AI Blog — "How to Set Gemini 3.1 Pro Thinking Levels (LOW/MEDIUM/HIGH, Deep Think Mini)" — https://blog.laozhang.ai/en/posts/gemini-3-1-pro-thinking-level — 2026 — blog (corroborating)
