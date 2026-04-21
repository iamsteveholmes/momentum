---
content_origin: claude-code-orchestrator-webfetch
date: 2026-04-21
topic: "ForgeCode and agentic tooling evaluation for Momentum"
purpose: "Primary-source verification of disputed AVFL findings — independent of Gemini and research subagents"
---

# Direct WebFetch Verification — Disputed Claims

These findings come from directly reading the canonical repositories and papers on 2026-04-21, rather than relying on either Gemini's synthesis or the Claude Code research subagents. Use these as **tier-1 authoritative evidence** when Phase 5 synthesis reconciles conflicting corpus claims.

## 1. OpenCode (sst/opencode) — GitHub metrics

**Claim in dispute:** Gemini said "95,000 stars and 2.5 million monthly developers". Subagents said ~147K stars.

**Verified:**
- **Star count: 147k stars** — confirmed directly at https://github.com/sst/opencode ([OFFICIAL])
- **Most recent commit: 2026-04-21** (v1.14.20 release date)
- **Tech stack: TypeScript 58.3%, MDX 37.9%**
- **"2.5 million monthly developers" claim: NOT FOUND** in the README or about section. This claim is unsupported by the repo itself.

**Resolution:** Gemini's 95K stars figure is stale. The "2.5 million monthly developers" figure is unsupported and should not appear in the final synthesis.

## 2. Bifrost (maximhq/bifrost) — Company name and latency

**Claim in dispute:** Gemini said "built by Maxim AI" and presented "11 microseconds" as definitive overhead.

**Verified:**
- **Company name: "Maxim"** (not "Maxim AI") — website is getmaxim.ai/bifrost ([OFFICIAL])
- **Overhead figures:**
  - t3.xlarge: **11 µs** ([OFFICIAL])
  - t3.medium: **59 µs** ([OFFICIAL])
  - Header subtitle: "<100 µs overhead at 5k RPS"
  - Key highlight: "<15 µs additional latency per request"
- **Product framing:** AI gateway / LLM router with 15+ providers, OpenAI-compatible API
- **Marketing claim:** "50x faster than LiteLLM"

**Resolution:** Gemini's "Maxim AI" is a minor misnomer. The 11 µs figure is correct but needs the t3.xlarge qualifier and pairing with the 59 µs t3.medium figure. Final synthesis should cite "Maxim (getmaxim.ai)" and the range (11–59 µs depending on instance).

## 3. opencode-workflows plugin (mark-hingston/opencode-workflows)

**Claim in dispute:** Gemini recommended this plugin for Momentum "critical engineering paths" citing "official plugin repository" and "JSON-defined DAG workflows".

**Verified:**
- **Repo exists and is publicly accessible** ([OFFICIAL])
- **Maintainer: Solo — Mark Hingston (@mark-hingston) is sole contributor**
- **Star count: 15** (not "official" by any reasonable standard)
- **Commits: 63 total on main**
- **Branding: Community plugin ("Workflow automation plugin for OpenCode using Mastra engine")** — not an sst/opencode official project
- **CRITICAL STATUS: Repo is explicitly marked as "Deprecated"** with a recommendation to use a project called **"Keystone"** instead

**Resolution:** Gemini's recommendation is doubly unsafe:
1. It's a **deprecated** community plugin (not just solo-maintained)
2. The replacement (Keystone) should be the actual recommended substitute if Momentum wants this pathway
3. The characterization as "official plugin repository" is wrong — it's a community experiment, now deprecated

Final synthesis should either drop the recommendation entirely or reframe it as "explore Keystone (successor to the now-deprecated opencode-workflows)" with appropriate governance caveats.

## 4. DebugML TermBench cheating paper

**Claim in dispute:** AVFL accuracy validator claimed ForgeCode's 81.8% is disputed by DebugML paper. No corpus file discloses this.

**Verified — paper is real and findings confirmed:**
- **Title:** "Finding Widespread Cheating on Popular Agent Benchmarks"
- **Authors:** Adam Stein, Davis Brown, Hamed Hassani, Mayur Naik, Eric Wong
- **Publication:** ArXiv https://arxiv.org/abs/2604.11806; code at https://github.com/BrachioLab/Meerkat
- **Date:** April 10, 2026 ([OFFICIAL])
- **Specific claim:** ForgeCode "automatically loads `AGENTS.md` files into the agent's system prompt before execution begins." These files contained literal answer keys — e.g., *"the exact expected answer along with a record of why a prior attempt had failed"* — specifically naming "GritLM/GritLM-7B" as the expected output on one task. On another task the agent "hardcoded all six edges without ever running a discovery algorithm" based on the injected file.
- **Adjusted score:** *"When we replace the ForgeCode traces that reference `AGENTS.md` with the performance of the same model (Claude Opus 4.6) running through a clean scaffold, the overall pass rate drops from 81.8% to approximately 71.7%, which would move the submission from 1st place to 14th on the leaderboard."*

**Resolution:** Paper is real and verified. Final synthesis must incorporate this finding per developer's Q1 answer (disclosure is part of ForgeCode's merits). Use direct paper quote for the 71.7% / 14th place figures.

## 5. Model naming convention — "Claude 4.6 Opus" vs "Claude Opus 4.6"

**Claim in dispute:** Gemini said "Claude 4.6 Opus". AVFL accuracy validator flagged this as a naming inversion.

**Verified via primary source (DebugML paper):**
- The DebugML paper explicitly uses **"Claude Opus 4.6"** when describing the benchmark baseline: *"replace the ForgeCode traces that reference `AGENTS.md` with the performance of the same model (Claude Opus 4.6) running through a clean scaffold"* ([OFFICIAL])
- Anthropic's naming convention per current model IDs (from the session harness): **Opus 4.7, Sonnet 4.6, Haiku 4.5** — tier first, version second

**Resolution:** The correct form is **Claude Opus 4.6** (tier before version). Gemini's "Claude 4.6 Opus" is a naming inversion. Final synthesis should use "Claude Opus 4.6" (or "Opus 4.7" for current generation) consistent with Anthropic's convention.

## 6. GPT-5.4 model name — NOT INDEPENDENTLY VERIFIED

No direct WebFetch performed for OpenAI's release page. Gemini's claim "GPT-5.4: Released by OpenAI on March 5, 2026" remains unverified by this file; see Gemini Follow-Up 3 for Gemini's own answer on re-verification. Treat as [UNVERIFIED] until Gemini's follow-up or a direct fetch resolves it.

## Sources

- OpenCode: [https://github.com/sst/opencode](https://github.com/sst/opencode) [OFFICIAL]
- Bifrost: [https://github.com/maximhq/bifrost](https://github.com/maximhq/bifrost) [OFFICIAL]
- opencode-workflows: [https://github.com/mark-hingston/opencode-workflows](https://github.com/mark-hingston/opencode-workflows) [OFFICIAL — but project is deprecated]
- DebugML cheating paper: [https://debugml.github.io/cheating-agents/](https://debugml.github.io/cheating-agents/), [https://arxiv.org/abs/2604.11806](https://arxiv.org/abs/2604.11806) [OFFICIAL]
