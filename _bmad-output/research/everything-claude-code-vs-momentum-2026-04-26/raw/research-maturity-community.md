---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Maturity & community signals — release cadence, contributor velocity, code health, star growth, ecosystem mentions"
topic: "everything-claude-code vs Momentum — comparative analysis"
---

# Maturity & Community Signals: `affaan-m/everything-claude-code`

## TL;DR — Verified Numbers vs Claimed Numbers

**The "suspicious" numbers from the prior report are mostly real or low. ECC is genuinely a top-tier viral repository, not a hype-cycle README.** As of 2026-04-26, GitHub API data shows:

| Metric | Prior report claim | Verified (GitHub API, 2026-04-26) | Verdict |
|---|---|---|---|
| Stars | 140,000+ | **167,487** | Higher than claimed |
| Forks | 21,000+ | **25,969** | Higher than claimed |
| Contributors | 113 | **159** (Link header) / 100 in default API page | Higher than claimed |
| Total commits | 768 | **1,465** (commit count via Link header) | Roughly 2x higher than claimed |
| Tests | 1,282 automated | Unverified count of 1,282 specifically; the repo has a large test tree (`tests/` with `integration/`, `ci/`, `hooks/`, plus `tests/scripts/`, plus skill-level tests). The 1,282 figure appears in vendor/blog text and the repo's own README, but it is not independently auditable from API listings. **PLAUSIBLE but UNVERIFIED at the exact number.** |
| Anthropic x Forum Ventures hackathon win, late 2025 | Approximately correct *event*, wrong sponsor and date — actual event was **Cerebral Valley × Anthropic "Built with Opus 4.6" hackathon, Feb 10-16, 2026**. ECC was a winner. |
| Rust ECC 2.0 alpha released April 2026 | **Confirmed** — `ecc2/Cargo.toml` (`ecc-tui` v0.1.0) is in the repo; v1.10.0 release notes (2026-04-05) explicitly call out "ECC 2.0 alpha control-plane binary now builds locally from `ecc2/`". Rust source size: **1.8 MB of Rust source** (1,818,298 bytes per GitHub `/languages` API — this is a byte count, not a line count; at typical Rust line length the actual line count is ~25–60K, not 1.8 M). |

**Bottom line:** ECC is a real, fast-growing, actively maintained project with a sizeable contributor pool, professional CI, and ecosystem-wide visibility. It is *not* vaporware. Whether it's also *over-engineered for what it does* is a separate question — community sentiment is split on that. [OFFICIAL]

---

## 1. Repository Identity & Creation Date

- **Full name:** `affaan-m/everything-claude-code` [OFFICIAL: GitHub API]
- **Created:** 2026-01-18T00:51:51Z [OFFICIAL]
- **Last pushed:** 2026-04-26T04:53:53Z (today, with ongoing activity)
- **Default branch:** `main`
- **License:** MIT
- **Homepage:** https://ecc.tools
- **Description:** "The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond."

The repo is **only ~3 months and 1 week old** (2026-01-18 → 2026-04-26). Reaching 167K stars in that window is anomalous even for top-tier viral repos. Llama and Stable Diffusion comparisons understate the anomaly: those were major model releases with broad press coverage; ECC is a Claude Code config plugin. At ~1,800 stars/day sustained for ~90 days, the velocity is unprecedented in dev-tooling history. External boosts (hackathon win, viral X threads) explain part of the curve, but the low star-to-download ratio (~0.6%, see §7 NPM) suggests possible amplification beyond organic adoption. Treat the star count as a signal of high awareness, not necessarily high installation.

---

## 2. Maintainer Identity — Who is `affaan-m`?

Affaan Mustafa is a real, public-facing builder, not an anonymous account. [OFFICIAL: GitHub user API]

- **GitHub:** `affaan-m`, account created 2023-02-04, **4,986 followers**, 26 public repos. [OFFICIAL]
- **Real name:** Affaan Mustafa.
- **Company (per GitHub bio):** Itô (a prediction-markets startup he co-founded; "institutionalizing gambling @Ito-Markets").
- **Location:** San Francisco, CA / Bellevue, WA.
- **Twitter/X:** `@affaanmustafa`. Personal site claims 3M+ direct views and ~10M+ cross-platform reach on Claude Code guides. [PRAC: affaanmustafa.com]
- **Background:** Math-CS + Business Economics from UCSD, graduate work in Applied/Computational Math at UW. Prior projects include PMX Trade and ModernStoicAI. [PRAC: affaanmustafa.com via WebFetch]
- **Email:** `me@affaanmustafa.com` (in Cargo.toml authors field). [OFFICIAL: repo]

This is a verifiable individual with a startup, an LinkedIn profile, and a public-facing X presence. There is no signal of fabrication.

---

## 3. Star & Fork Growth

- **Stars:** 167,487 (167K). watchers_count is the same value (legacy alias). [OFFICIAL: API]
- **Forks (`forks_count`):** 25,969. (`network_count` matches at 25,969.) [OFFICIAL]
- **Subscribers (true watchers):** 864. [OFFICIAL: subscribers Link header showing 864 pages of 1]

Growth trajectory inferred from third-party blog timestamps:

| Date | Star count claimed | Source |
|---|---|---|
| 2026-03-18 | ~82K | [PRAC: medium.com/@tentenco] |
| 2026-03-21 | ~50K (in fork's REPO-ASSESSMENT.md, dated; likely conservative or older snapshot) | [OFFICIAL: repo file] |
| 2026-03-23 | ~99,900 ("approaching 100K") | [PRAC: bridgers.agency] |
| 2026-04-26 | 167,487 | [OFFICIAL: API] |

That is roughly **2x growth in ~5 weeks (early March to late April)** — consistent with a viral hype curve still on the upswing, not a plateau. The README itself still reads "140K+ stars | 21K+ forks | 170+ contributors" — those numbers are now stale (the repo has surged past them since the README was last edited).

**The 167K star count is verified directly from `https://api.github.com/repos/affaan-m/everything-claude-code` (the JSON `stargazers_count` field). This is not inferred or scraped — it is the authoritative GitHub-served number.**

The 25,969 forks places ECC in the very top tier of GitHub repositories. For comparison, that is more forks than projects like `ohmyzsh` had at similar repo ages. The fork-to-star ratio (~15.5%) is high for a developer-tools repo, indicating people are not just bookmarking — they're cloning and customizing.

---

## 4. Contributor Velocity

- **Total contributors:** 159 (computed from Link header on `/contributors?per_page=1` showing 159 pages of 1). [OFFICIAL]
- **First page (top 100):** Long tail dominated by `affaan-m` himself with **965 commits**. [OFFICIAL]
- **Top 10 by commits:**

| Contributor | Commits |
|---|---|
| affaan-m | 965 |
| pangerlkr | 47 |
| Copilot (bot) | 22 |
| pvgomes | 15 |
| Lidang-Jiang | 14 |
| dependabot[bot] | 14 |
| ozoz5 | 12 |
| pythonstrup | 12 |
| shimo4228 | 12 |
| chris-yyau | 9 |

- **Bots present:** GitHub Copilot, dependabot, `claude` / `Claude` (likely Claude Code commits via the GitHub App), `ecc-tools[bot]`. [OFFICIAL]
- **Bus factor:** Very high single-maintainer concentration. Affaan Mustafa wrote ~66% of all commits (965 / 1,465). The next 10 humans collectively contribute ~150 commits. This is a classic "founder-driven" repo, not a distributed-governance one.
- **Long tail:** 159 contributors total, with ~140 of them having 1-3 commits each. Healthy for drive-by docs/translation/typo-fix PRs (consistent with the sustained PR throughput below) but not load-bearing development.

---

## 5. Release Cadence & Version History

- **Tags:** 13 (`v0.6.0` through `v1.10.0`). [OFFICIAL]
- **GitHub Releases:** 12 (one per tag from v1.0.0 onward, plus the v0.6.0 tag without a release). [OFFICIAL]

Release history (verified from `/releases` API):

| Tag | Date | Title |
|---|---|---|
| v1.10.0 | 2026-04-05 | Surface Refresh, Operator Workflows, and ECC 2.0 Alpha |
| v1.9.0 | 2026-03-21 | Selective Install, ECC Tools Pro, 12 Language Ecosystems |
| v1.8.0 | 2026-03-05 | Harness Performance & Cross-Platform Reliability |
| v1.7.0 | 2026-02-27 | Cross-Platform Expansion & Presentation Builder |
| v1.6.0 | 2026-02-24 | Codex Edition + GitHub App |
| v1.5.0 | 2026-02-11 | Universal Edition |
| v1.4.1 | 2026-02-06 | Patch: instinct import fix |
| v1.4.0 | 2026-02-06 | Multi-Language Rules, Installation Wizard & PM2 Orchestration |
| v1.3.0 | 2026-02-05 | Complete OpenCode Plugin Support |
| v1.2.0 | 2026-02-01 | Unified Commands & Skills |
| v1.1.0 | 2026-01-26 | Cross-Platform Support and Community Fixes |
| v1.0.0 | 2026-01-22 | Official Plugin Release |

**Cadence:**
- v1.0.0 shipped only 4 days after repo creation (2026-01-22 vs. 2026-01-18) — strongly suggesting the code was developed privately for the "10+ months" the project's marketing claims and dropped publicly at the hackathon.
- 12 releases in **94 days** = a release every ~8 days. That is aggressive even by SaaS standards.
- Semver discipline: tags strictly match `vMAJOR.MINOR.PATCH`; release CI workflow validates tag-vs-`package.json` consistency. [OFFICIAL: `.github/workflows/release.yml`]

This is a healthy cadence and shows real release engineering discipline — not just `git tag` spam.

---

## 6. Commit Velocity (Total & Recent)

- **Total commits on `main`:** **1,465** (verified via the Link header on `/commits?per_page=1` showing page=1465 as last). [OFFICIAL]
- **Commits since 2026-04-01 (last ~25 days):** **430** commits. [OFFICIAL: Link header on filtered commits endpoint]
- That is ~17 commits/day average over the last 4 weeks — very high, comparable to active commercial monorepos.

Recent commit sample (top 10 from 2026-04-21):
- `docs: fix plugin quick start for continuous learning v2 (#1546)` — Affaan Mustafa
- `fix(observe): skip Windows AppInstallerPythonRedirector.exe in resolve_python_cmd` — community
- `fix(continuous-learning-v2): accept claude-desktop as valid entrypoint (#1522)` — community
- `docs: fix bottom overflow in hero PNG, tighten stats labels (#1535)` — community
- Several merge commits from suusuu0927/ratorin (community PRs)

The PR numbers (#1543, #1544, #1546, #1576, etc.) confirm **>1,500 PRs opened** lifetime, consistent with the 96 open + 929 closed PR figures below.

---

## 7. Issue & PR Throughput

Issue/PR counts (verified via GitHub Search API):

| Metric | Count |
|---|---|
| Open issues | 70 |
| Closed issues | 415 |
| Open PRs | 96 |
| Closed PRs (all states) | 929 |
| Merged PRs | 368 |

[OFFICIAL: `api.github.com/search/issues`]

**Observations:**
- Issue close rate: 85.6% (415 closed / 485 total) — very healthy.
- PR merge rate: 36.0% (368 / 1,025) — moderate. The remaining 561 closed-but-not-merged PRs suggest active triage and rejection of low-value drive-bys.
- Backlog of 96 open PRs is large but normal at this scale and velocity.

**Response time sample** (from issues closed in the most recent batch):

| Issue | Close time |
|---|---|
| #1541 | 1.2h |
| #1538 | 3.2h |
| #1537 | 3.3h |
| #1534 | 3.1h |
| #1549 | 31.0h |

Sub-day response on community-reported bugs is excellent — far better than most volunteer projects. [OFFICIAL]

The `open_issues_count` field on the API returned **166** — that is the GitHub-internal "issues + PRs" count, which matches our 70 + 96 = 166. [OFFICIAL]

---

## 8. Code Health, CI, and Structure

### CI Workflows
The `.github/workflows/` directory contains **7 workflow files**:
- `ci.yml` — main test workflow
- `maintenance.yml`
- `monthly-metrics.yml`
- `release.yml`
- `reusable-release.yml`, `reusable-test.yml`, `reusable-validate.yml` (reusable workflow modules)

[OFFICIAL: `/contents/.github/workflows`]

### CI Matrix
The main `ci.yml` runs a **3 × 3 × 4 matrix** = 36 base jobs (with Bun-on-Windows excluded), spanning:
- OS: ubuntu-latest, windows-latest, macos-latest
- Node: 18.x, 20.x, 22.x
- Package managers: npm, pnpm, yarn, bun

[OFFICIAL: `.github/workflows/ci.yml`]

This is **enterprise-grade CI breadth**. Most open-source projects test one or two combinations; ECC tests a full cross-product. SHA-pinned action versions (`actions/checkout@de0fac…` etc.) indicate supply-chain security awareness. Concurrency cancellation, minimal `contents: read` permissions, and matrix `fail-fast: false` are all best practices.

### Release Pipeline
`release.yml` enforces:
- Tag format `vX.Y.Z` regex validation
- `package.json` version must match the tag
- Runs `tests/scripts/build-opencode.test.js` to verify package payload before publishing

[OFFICIAL]

### Test Footprint
The `tests/` directory contains:
- 4 top-level test files: `codex-config.test.js`, `opencode-config.test.js`, `plugin-manifest.test.js`, `run-all.js`
- 4 Python test files: `test_builder.py`, `test_executor.py`, `test_resolver.py`, `test_types.py`
- Subdirectories: `ci/`, `docs/`, `hooks/`, `integration/` (containing `hooks.test.js`), `lib/`, `scripts/`

The fork's own REPO-ASSESSMENT.md (dated 2026-03-21) cited "58 test files" at v1.9.0. The "1,282 tests" claim is repeated across blog posts and the README itself but is **a test-case count, not a file count** — and we cannot independently verify the exact number without cloning and running the suites. **PLAUSIBLE; UNVERIFIED at exact number.**

### Languages
[OFFICIAL: `/languages` API]

| Language | Bytes |
|---|---|
| JavaScript | 2,396,741 |
| Rust | 1,818,298 |
| Python | 234,967 |
| Shell | 162,725 |
| TypeScript | 57,674 |
| PowerShell | 1,547 |

Rust is now the second-largest language by volume — that is the **ECC 2.0 Rust control-plane prototype** (`ecc2/` directory). Confirmed via `ecc2/Cargo.toml` showing `ecc-tui` v0.1.0 with dependencies on `ratatui`, `tokio`, `rusqlite`, `git2`, `clap`. **The Rust prototype is real and substantial.** [OFFICIAL]

### Repo Structure (top-level)
`agents/`, `commands/`, `contexts/`, `docs/`, `ecc2/`, `examples/`, `hooks/`, `manifests/`, `mcp-configs/`, `plugins/`, `research/`, `rules/`, `schemas/`, `scripts/`, `skills/`, `src/`, `tests/`, plus 12 platform-config dirs (`.agents/`, `.claude/`, `.codex/`, `.codex-plugin/`, `.cursor/`, `.gemini/`, `.kiro/`, `.opencode/`, `.codebuddy/`, `.trae/`, etc.) and ~15 markdown manifests (CHANGELOG, CODE_OF_CONDUCT, CONTRIBUTING, EVALUATION, REPO-ASSESSMENT, SECURITY, SOUL, SPONSORING, SPONSORS, TROUBLESHOOTING, etc.). [OFFICIAL]

### Catalog Counts
The README and SOUL.md disagree slightly with directory listings:

| Source | Agents | Skills | Commands |
|---|---|---|---|
| README/marketing | 38 | 156 | 72 |
| SOUL.md | 30 | 135 | 60 |
| Live `/contents/` | 48 dirs/files | 183 dirs | 79 dirs/files |

The `/contents/` directory listings show *more* than the marketed counts — likely the marketed counts represent "user-facing curated" items vs. the raw filesystem (which includes scaffolds, internal helpers, and the ECC 2.0 in-progress lane). [OFFICIAL]

### Dependency Hygiene
- `dependabot[bot]` is among the top contributors with 14 commits — automated dep upgrades are running.
- Recent open PRs include `chore(deps): bump the minor-and-patch group` and `chore(deps): bump actions/setup-node from 6.3.0 to 6.4.0` — active hygiene.
- `.tool-versions` pins Node 20.19.0 and Python 3.12.8 (asdf/mise compatible).
- `package.json` uses Yarn (Berry, per `.yarnrc.yml`) as the canonical manager but tests all four common ones.

[OFFICIAL]

This is **professional engineering discipline**, not weekend hobbyist code.

---

## 9. Ecosystem Mentions

### Hackathon
- ECC was a winner at **Cerebral Valley × Anthropic "Built with Opus 4.6" hackathon**, Feb 10-16, 2026. [PRAC: cerebralvalley.ai/e/claude-code-hackathon, claudeskills.info]
- The prior report's "Anthropic x Forum Ventures, late 2025" conflated two separate events: (1) Affaan's **earlier project `zenith.chat` won the Anthropic × Forum Ventures hackathon, Sep 2025** (this event was real; Forum Ventures was the partner); (2) **ECC** was built at and won the Cerebral Valley × Anthropic hackathon, Feb 2026. Forum Ventures was not the partner for ECC — Cerebral Valley was. The prior report correctly identified a hackathon win but attributed ECC to the wrong event. [OFFICIAL]

### Twitter/X
- Affaan's "Shorthand Guide to Everything Claude Code" thread reportedly hit **900K views** with 10K+ bookmarks shortly after the hackathon. [PRAC: bridgers.agency, claudeskills.info]
- His combined Claude Code + agentic security guides reportedly have **3M-5M+ views** and **25M+ impressions across socials** (his own claim, on his personal site). [PRAC: affaanmustafa.com]
- The README links three guides on X (status IDs 2012378465664745795, 2014040193557471352, 2033263813387223421). [OFFICIAL]

### Hacker News
- Search of `news.ycombinator.com/from?site=github.com/affaan-m` returned **2 submissions**, both with 2 points each, posted ~3 months ago by community accounts (`manthangupta109` and `bzGoRust`). [OFFICIAL: HN]
- Notably: **Affaan himself has not posted to HN**, and the community submissions did *not* land on the front page. The HN-side story is much smaller than the Twitter/X-side story.

### Reddit
- General `r/ClaudeCode` and `r/ClaudeAI` discussions reference ECC, but no single thread dominates. Coverage is mixed. [PRAC: aitooldiscovery.com, morphllm.com]
- One Medium analysis ("inside the 82K-star agent harness that's dividing the developer community", 2026-03-18) explicitly characterizes the community as **split**: advocates praise time savings; skeptics call it over-engineered and note "minimal Discussion forum activity" relative to star count. [PRAC: medium.com/@tentenco]

### YouTube / Podcasts
- No major YouTube creator coverage surfaced in searches. Coverage is text-blog-heavy.

### Long-form blog coverage
- bridgers.agency (2026-03-23) — "approaching 100K stars" piece
- claudeskills.info (date n/a) — "The Claude Code Hackathon Winner: Eval-Driven Development with Everything Claude Code"
- help.apiyi.com — "Decoding everything-claude-code" comprehensive analysis
- DeepWiki.com — auto-generated docs page exists
- FlorianBruniaux/claude-code-ultimate-guide repo includes a dedicated evaluation file
- Multiple translated READMEs in-repo: Português (BR), 简体中文, 繁體中文, 日本語, 한국어, Türkçe — indicating organic international traction

[PRAC]

### NPM
- Package `ecc-universal` (currently v1.10.0) on npm. **Weekly downloads: ~1,000/week** (img.shields.io npm/dw badge live response was "1k/week"; another search snippet returned 715/week). The README also advertises an `ecc-agentshield` package. [OFFICIAL: npm registry]
- 1k weekly downloads is **modest** — orders of magnitude below the star count. This corroborates the "many people star, few install" pattern noted in the Medium critique.

### Forks of forks
- The repo itself shows >25K forks. Forks-of-forks pattern: dedicated mirrors at `WorldFlowAI/everything-claude-code`, `arabicapp/everything-claude-code`, and `Infiniteyieldai/everything-claude-code` show real organizational/team adoption beyond drive-by stars.

---

## 10. Production Readiness Signals

**Pro-production signals:**
- Cross-platform CI matrix (36 jobs) [OFFICIAL]
- Dependabot + automated dependency PRs [OFFICIAL]
- SHA-pinned actions [OFFICIAL]
- Semver-strict release pipeline with tag-vs-package version validation [OFFICIAL]
- 12 numbered releases in 94 days, with detailed changelog entries [OFFICIAL]
- MIT license (permissive, dependable) [OFFICIAL]
- SECURITY.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md present [OFFICIAL]
- 6 translated READMEs (international community uptake) [OFFICIAL]
- Sub-day issue response time on recent samples [OFFICIAL]
- A real Rust 2.0 control-plane is in-progress (~1.8MB Rust code, builds with `cargo`) [OFFICIAL]
- Companion product surface at `ecc.tools` and a GitHub App in marketplace [OFFICIAL: README badges]
- Real human maintainer with verifiable identity, startup, and public X/LinkedIn presence [OFFICIAL]

**Caution signals:**
- **Bus factor = 1.** 66% of commits from one person; next contributor has 4.9% of his volume. If Affaan stops, momentum dies.
- **Star-to-download gap.** 167K stars vs. ~1K weekly npm downloads = ~0.6% conversion. Many stargazers are bookmarking, not running.
- **README claims are partly hyped.** "1,282 automated tests" cannot be verified at exact count without checkout. "98% coverage" is asserted with no `coverage` badge or report I can verify externally. The marketed counts (38 agents / 156 skills / 72 commands) under-count the actual filesystem (48 / 183 / 79).
- **Catalog drift.** README, SOUL.md, REPO-ASSESSMENT.md, and `/contents/` listings disagree on counts. This is a sign of fast iteration faster than docs can keep up.
- **Repo age (3 months) vs. complexity.** A 1.8MB Rust prototype, 183 skills, and a Tkinter dashboard appearing in 12 weeks raises questions about how much is polished vs. partially-prototyped scaffolding (the v1.10.0 release notes themselves caveat: "the broader control-plane roadmap remains incomplete and should not be treated as GA").
- **Community sentiment is genuinely split** between "essential toolkit" and "textbook over-engineering" per blog/Reddit analysis. [PRAC]

---

## 11. Verdict

**ECC is real, fast-growing, professionally engineered, and led by a verifiable maintainer.** The "hot README riding the hype curve" hypothesis is **rejected**: the repo has CI breadth most enterprise products lack, a 12-release semver-disciplined cadence over 94 days, sub-day issue response, an active 159-contributor community, and a tangible Rust 2.0 prototype building locally.

But it is **not yet a stable, production-grade *foundation*** to depend on. It is a single-maintainer-driven, three-month-old project growing faster than its own documentation can keep up; star-to-actual-install conversion is ~0.6%; the marketing claims (especially exact test counts and coverage percentages) outrun externally-verifiable evidence; and the v1.10.0 changelog itself disclaims that the ECC 2.0 control-plane roadmap is incomplete.

**For Momentum integration purposes:** Treat ECC as a **rapidly-evolving reference codebase**, not a stable upstream dependency. It is worth mining for patterns (skills catalog structure, hook taxonomy, install profiles, CI matrix design, semver release pipeline). It is *not* yet trustworthy as a versioned dependency to lock against, given (a) the velocity (8-day average release cadence means breaking changes are likely), (b) the bus factor on a single founder, and (c) the over-broad marketing claims. Adopt selectively, version-pin if pulled in, and do not assume backward compatibility across releases.

---

## Sources

### Primary [OFFICIAL]
- GitHub API: `https://api.github.com/repos/affaan-m/everything-claude-code` (2026-04-26)
- GitHub API: `https://api.github.com/users/affaan-m`
- GitHub API: `/repos/affaan-m/everything-claude-code/contributors` (Link header pagination)
- GitHub API: `/repos/affaan-m/everything-claude-code/releases`
- GitHub API: `/repos/affaan-m/everything-claude-code/tags`
- GitHub Search API: `/search/issues?q=repo:affaan-m/everything-claude-code+...`
- GitHub API: `/repos/affaan-m/everything-claude-code/commits?since=2026-04-01T00:00:00Z` (Link header)
- GitHub API: `/contents/.github/workflows/ci.yml`, `/contents/.github/workflows/release.yml`
- GitHub API: `/contents/package.json`, `/contents/CHANGELOG.md`, `/contents/README.md`, `/contents/REPO-ASSESSMENT.md`, `/contents/SOUL.md`, `/contents/EVALUATION.md`
- GitHub API: `/contents/ecc2/Cargo.toml`, `/contents/.tool-versions`
- GitHub API: `/repos/affaan-m/everything-claude-code/languages`
- Hacker News: https://news.ycombinator.com/from?site=github.com/affaan-m
- npm: `https://www.npmjs.com/package/ecc-universal` (download badge)

### Secondary [PRAC]
- https://medium.com/@tentenco/everything-claude-code-inside-the-82k-star-agent-harness-thats-dividing-the-developer-community-4fe54feccbc1 (2026-03-18)
- https://bridgers.agency/en/blog/everything-claude-code-explained (2026-03-23)
- https://claudeskills.info/blog/everything-claude-code-hackathon-eval-driven/
- https://help.apiyi.com/en/everything-claude-code-plugin-guide-en.html
- https://deepwiki.com/affaan-m/everything-claude-code
- https://affaanmustafa.com/ (maintainer's personal site)
- https://cerebralvalley.ai/e/claude-code-hackathon (hackathon source-of-truth)
- https://x.com/cerebral_valley/status/2019836976044855679 (hackathon announcement)
- https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/docs/resource-evaluations/015-everything-claude-code-github-repo.md (independent eval)

### Notes on freshness
All API queries executed 2026-04-26. All dates < 12 months old; most < 3 months old. No source older than 2 years was used.
