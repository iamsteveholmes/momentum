---
content_origin: independent-confirmation
target: suspect-claims-audit
date: undefined
analyst_role: independent confirmation / skeptic
environment_date: 2026-05-31
---

# Confirmation Audit — Suspect Single-Engine (Gemini-only) Claims

Independent verification of six suspect claims from a prior research report. Each claim was
checked against PRIMARY sources (vendor docs, original papers, first-party reports). Secondary
blog restatements were NOT accepted as confirmation of a specific product name or statistic.

The original report apparently relied on a single engine (Gemini). The job here was to find
primary sources or REFUTE. Note: several of these "suspect" names turned out to be REAL
2026 products/models — the confabulation risk in this set is lower than the framing implied,
but two claims (Council+Mythos binding, NextAds-as-oversight) are mis-stated conflations.

---

## Claim 1 — Microsoft "Council" running "Claude Mythos" and "GPT-5.4"

**Verdict: PARTIALLY-CONFIRMED (the binding is confabulated; the three components are individually real)**

Three separately-real things have been incorrectly fused into one claim.

- **Microsoft "Model Council" — REAL.** Microsoft 365 Copilot blog, "Copilot Cowork: Now
  available in Frontier," dated **2026-03-30**
  (https://www.microsoft.com/en-us/microsoft-365/blog/2026/03/30/copilot-cowork-now-available-in-frontier/).
  Direct quote: "with Researcher's new model Council, you can compare responses from different
  models side by side, instantly seeing where they agree, where they diverge, and what each
  uniquely brings to the table." Critique separates generation from evaluation. The blog names
  only the providers "Anthropic and OpenAI" — NOT specific model versions.
- **"Claude Mythos" — REAL model name.** Anthropic, "Claude Mythos Preview," red.anthropic.com,
  dated **2026-04-07** (https://red.anthropic.com/2026/mythos-preview/); corroborated by Axios
  (2026-05-28, Opus 4.8 + Mythos rollout), Yahoo Finance, BleepingComputer. It is a RESTRICTED /
  not-generally-available frontier model tied to Project Glasswing; Anthropic explicitly withheld
  general availability for cybersecurity reasons. (Note: a WebFetch summarizer flagged it
  "fictional" — that is a training-cutoff artifact; per environment date 2026-05-31 and multiple
  first-party + major-press sources, Mythos is a real announced model.)
- **"GPT-5.4" — REAL model.** OpenAI, "Introducing GPT-5.4," released **2026-03-05**
  (https://openai.com/index/introducing-gpt-5-4/ — 403 to bot fetch, confirmed via TechCrunch
  https://techcrunch.com/2026/03/05/openai-launches-gpt-5-4-with-pro-and-thinking-versions/).

**Why the binding is unsupported:** No primary source states that Microsoft's Council runs
"Claude Mythos" and "GPT-5.4." Microsoft's own blog names neither version. Secondary coverage of
Council that DOES name models cites **GPT-5.2 (as the judge model), Claude Sonnet 4.5, Claude
Opus 4.6, GPT-5.5** — not Mythos/5.4. Moreover, Claude Mythos is restricted/not-GA, so it would
not plausibly be the model inside a generally-available Copilot Council. The specific
"Council runs Claude Mythos + GPT-5.4" assertion is a confabulated conflation of three real but
separate facts. The report should either drop the model names or correct them.

---

## Claim 2 — A product/system named "NextAds" relevant to AI oversight

**Verdict: REFUTED (as stated) — name exists in ad-tech, but NOT as an AI-oversight system**

- The name "NextAds" exists in the ADVERTISING space, not oversight: NextAds AI ad creator
  (https://nextads.ai/), NextAd ad-optimization (https://www.nextad.org/), an academic paper
  "NextAds: Towards Next-generation Personalized Video Advertising"
  (https://arxiv.org/html/2603.02137v1), and a Crunchbase "NEXTads" affiliate-marketing entity.
- The nearest AI-adjacent name is **"Nexad"** (https://nex.ad/, a16z-backed) — an ad-INSERTION
  platform that puts ads into chatbots/AI apps. Still advertising, not oversight.
- **No primary source describes any "NextAds" product as relevant to AI oversight.** The
  AI-oversight framing is unsupported. Most likely the original report either (a) confabulated
  the oversight angle, or (b) garbled "Nexad" into "NextAds." Either way, the claim as written
  is refuted.

---

## Claim 3 — A tool named "VibeSec"

**Verdict: CONFIRMED**

"VibeSec" is a real, multiply-instantiated security tool for AI-generated/"vibe-coded" code:

- **OX Security VibeSec** — first-party product page https://www.ox.security/vibesec/ and blog
  "VibeSec: The Security Response to AI-Speed Development"
  (https://www.ox.security/blog/vibesec-the-security-response-to-ai-speed-development/). Runs in
  the background of Copilot, Cursor, Claude to block insecure code at generation time.
- **Untamed Theory VibeSec** — open-source security rules/workflows for AI dev tools
  (https://github.com/untamed-theory/vibesec).
- Also a Claude/AI security Skill (https://vibesec.sh/, github.com/BehiSecc/VibeSec-Skill).

The name is real and primary-sourced. (Minor caveat: "VibeSec" is used by several distinct
projects, so any claim about a SPECIFIC VibeSec product should name its vendor.)

---

## Claim 4 — A system named "OpenClaw" described as "an operating system for people who…"

**Verdict: CONFIRMED**

- "OpenClaw" is real: a self-hosted AI-agent operating system. Tagline matches the claim:
  **"OpenClaw: The Operating System for People Who Actually Work"**
  (gist https://gist.github.com/alirezarezvani/bb68f4f7444fcab00beb6ded31eeb028; product site
  https://openclaw.ai/). Corroborated by an NVIDIA newsroom item announcing "NemoClaw for the
  OpenClaw Community" (https://nvidianews.nvidia.com/news/nvidia-announces-nemoclaw) and multiple
  architecture write-ups.
- It is described as an OS for AI agents (sessions, memory, tool sandboxing, orchestration),
  self-hosted, connecting to email/calendar/repos. The "operating system for people who…"
  phrasing is accurate.

---

## Claim 5 — CSET finding that "68-73% of AI-generated code is vulnerable"

**Verdict: REFUTED (misattribution) — figures are real but are NOT CSET's finding**

PRIMARY SOURCE READ IN FULL: CSET (Georgetown), "Cybersecurity Risks of AI-Generated Code,"
**November 2024** (https://cset.georgetown.edu/wp-content/uploads/CSET-Cybersecurity-Risks-of-AI-Generated-Code.pdf;
PDF extracted and read locally).

- The 68% / 73% figures DO appear in the CSET report, but as a CITATION of prior work, NOT as a
  CSET finding. Exact text (p.9): "Siddiq and Santos (2022) found that out of 130 code samples
  generated using InCoder and Github Copilot, **68% and 73%** of the code samples respectively
  contained vulnerabilities when checked manually." So 68% = InCoder, 73% = GitHub Copilot, from
  Siddiq & Santos (2022) — a separate study CSET is summarizing.
- **CSET's OWN headline finding is ~48%**, not 68-73%. Exact text: "an average of **48%** of the
  code produced by five different LLMs contains at least [one bug/vulnerability]"; "Across all
  five models, approximately **48%** of all generated code snippets were [insecure]." Other CSET
  own figures: ~30% error snippets; only 19% of Code Llama snippets passed verification; "all
  models produced buggy code in at least 40% of the prompts."
- Therefore attributing "68-73%" to CSET is a MISATTRIBUTION. The correct attribution is Siddiq &
  Santos (2022). If the report wants CSET's number, it is 48%.

---

## Claim 6 — Survey statistic "76% of developers believe AI-generated code is more secure"

**Verdict: CONFIRMED (with a precise-wording note)**

- Appears verbatim in the CSET report (p.9, primary source above): "in a 2023 industry survey of
  537 technology and IT workers and managers, **76% responded that AI code is more secure than
  human code.**" CSET footnote 26 attributes it to **Snyk, "AI Code, Security, and Trust in
  Modern Development" (2024)** (https://snyk.io/reports/ai-code-security/).
- Independently corroborated: Snyk's report (via CloudWars coverage
  https://cloudwars.com/cybersecurity/snyks-ai-code-security-report-reveals-software-developers-false-sense-of-security/)
  states "76% of respondents ... said that AI-generated code was more secure than code produced
  by humans."
- **Wording note:** the survey question is about "AI code / AI-generated code" being "more secure
  than human[-produced] code" — i.e., a comparative belief, not an absolute "AI code is secure."
  The report's paraphrase "believe AI-generated code is more secure" is faithful. Sample = 537
  tech/IT workers and managers; year = 2023 survey, published in the Snyk 2024 report.

---

## Cross-cutting notes

- The "suspect single-engine" framing implied these were likely confabulations. In fact FOUR of
  six names/figures (Council, Claude Mythos, GPT-5.4, VibeSec, OpenClaw, and the 76%/68-73% figures)
  trace to real primary sources. The real defects are (a) a confabulated BINDING in Claim 1
  (Council ↔ Mythos/5.4), (b) a MISATTRIBUTION in Claim 5 (68-73% is Siddiq & Santos, not CSET;
  CSET's own number is 48%), and (c) a category error in Claim 2 (NextAds is ad-tech, not oversight).
- Staleness flag: CSET report is Nov 2024; newer 2025-2026 work (arxiv 2510.26103; OX Security's
  62% figure; the 45% / 2.74x figures) reports different vulnerability rates and should be cited
  alongside, not in place of, the CSET 48% if currency matters.
