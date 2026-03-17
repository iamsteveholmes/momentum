# Multi-Model Selection, Benchmarking, and Cost-Performance Optimization Guide

*Consolidated research from 6 parallel research agents, 3 verification agents, and Gemini Deep Research. All pricing and benchmark claims independently verified against primary sources.*

*Date: 2026-03-13*

---

## 1. Model Selection Guidelines

### 1.1 The Anthropic Claude 4.6 Ecosystem

**Verified Pricing (per million tokens):**

| Model | Input | Output | Cache Write (5min) | Cache Write (1hr) | Cache Read | Batch (50% off) |
|---|---|---|---|---|---|---|
| **Opus 4.6** | $5.00 | $25.00 | $6.25 | $10.00 | $0.50 | $2.50 / $12.50 |
| **Sonnet 4.6** | $3.00 | $15.00 | $3.75 | $6.00 | $0.30 | $1.50 / $7.50 |
| **Haiku 4.5** | $1.00 | $5.00 | $1.25 | $2.00 | $0.10 | $0.50 / $2.50 |

*Fast mode (Opus 4.6 only): $30/$150 per MTok (6x standard, ~2.5x faster output). Opus 4.6 and Sonnet 4.6 include the full 1M context window at standard pricing (no long-context premium). Legacy models (Sonnet 4.5/4) still incur ~2x premium for >200k input tokens.*

**Key Specifications:**

| | Opus 4.6 | Sonnet 4.6 | Haiku 4.5 |
|---|---|---|---|
| Context window | 1M | 1M | 200k |
| Max output | 128k | 64k | 64k |
| Relative latency | Moderate | Fast | Fastest |
| Extended thinking | Adaptive + effort | Adaptive + effort | Manual (budget_tokens) only |
| Effort parameter | low/medium/high/max | low/medium/high | Not supported |
| Arena ranking | #1 overall | Top 20 | ~#58 |

**When to use each:**

- **Opus 4.6**: Multi-agent orchestration, complex multi-file refactoring, novel reasoning, problems where getting it exactly right matters, orchestrator/judge role in pipelines. Leads on GPQA Diamond (91.3% vs 74.1%, a 17.2pp gap), Humanity's Last Exam (40.0% without tools, 53.0% with tools vs Sonnet's 33.2%/49.0%), and Terminal-bench (~6pp over Sonnet).
- **Sonnet 4.6**: The general-purpose workhorse. ~98% of Opus coding quality at 60% of the cost. Achieves 79.6% on SWE-bench Verified (vs Opus's 80.8%). Preferred over Opus 4.5 by 59% of testers. Best for: standard code generation, content creation, document comprehension, interactive sessions.
- **Haiku 4.5**: High-volume, latency-critical, well-constrained tasks. Classification, simple extraction, routing decisions, sub-agent search operations. Quality drops significantly on open-ended reasoning (Arena ~#58 vs Sonnet's top-20).

### 1.2 The OpenAI Ecosystem

*This guide focuses primarily on Claude models; OpenAI and Google coverage is included for cross-vendor comparison context. See provider pricing pages for current rates.*

OpenAI segments between **execution models** (GPT family) and **reasoning models** (o-series):

- **GPT-5.3 / GPT-5.4**: Current-generation execution models (replaced GPT-4o, GPT-4.1 in ChatGPT as of Feb 2026). Latency-optimized for deterministic tasks, context parsing, and tool use.
- **o3**: Flagship reasoning. ~69-72% SWE-bench Verified (note: OpenAI has deprecated SWE-bench Verified due to contamination concerns, recommending SWE-bench Pro instead). High cost, high latency. Best for async processing, complex STEM, scientific validation.
- **o4-mini**: Cost-efficient reasoning. $1.10/$4.40 per MTok. 68.1% SWE-bench. Best for high-volume logic, sequential analysis, agentic tool calling where speed and reasoning must balance.
- **GPT-4o / GPT-4.1** (legacy): Still available via API but retired from ChatGPT. Remain viable for existing integrations.

**Common pattern**: GPT-5.x parses user intent and retrieves context, then hands assembled context to o4-mini or o3 for deep analytical work.

### 1.3 The Google Gemini Ecosystem

**Gemini 3.x series** (Preview, released March 2026 -- now the frontier):
- **Gemini 3.1 Pro Preview**: Latest flagship (replaced 3.0 Pro Preview, deprecated 2026-03-09). Deep reasoning with enhanced multimodal capabilities.
- **Gemini 3 Flash Preview**: Mid-tier with hybrid reasoning, successor to 2.5 Flash.
- **Gemini 3.1 Flash-Lite Preview**: Throughput-optimized, latest in the Lite line.

**Gemini 2.5 series** (Stable, still widely deployed):
- **Gemini 2.5 Pro**: Flagship with mandatory dynamic thinking (up to 32k reasoning tokens). 1M+ context. Best for complex reasoning, massive multimodal inputs (up to 3 hours of video).
- **Gemini 2.5 Flash**: Hybrid mid-tier with dynamically scalable reasoning (0 to 24k thinking tokens). Single endpoint for both reactive execution and complex planning. `thinkingBudget` parameter: -1 for dynamic, 0 to disable, integer for cap.
- **Gemini 2.5 Flash-Lite**: Pure throughput, thinking disabled by default. Fastest in Google's ecosystem. Classification, summarization, pipeline routing.

*Note: Gemini 3.x models are in Preview. For production stability, 2.5 stable models remain the safer choice. See Google's pricing page for current rates.*

### 1.4 Task-Type-to-Model Mapping

| Task Type | Recommended Tier | Claude Model | Effort | Rationale |
|---|---|---|---|---|
| Complex code generation (multi-file refactoring) | Flagship | Opus 4.6 | high | Opus leads Terminal-bench by ~6pp |
| Routine code generation (single functions) | Mid-tier | Sonnet 4.6 | medium | Matches Opus on SWE-bench at 60% cost |
| Code review / validation | Mid-tier | Sonnet 4.6 | medium | Good reasoning at lower cost |
| Creative writing / session prep | Mid-tier | Sonnet 4.6 | high | Strong writing quality; Opus adds cost without proportional creative gain |
| Data extraction / structured output | Throughput | Haiku 4.5 | -- | Well-constrained; Haiku at 1/5 cost handles it |
| Summarization | Mid-tier | Sonnet 4.6 | low-medium | Good balance; Haiku works for simple summaries |
| Complex reasoning / analysis | Flagship | Opus 4.6 | high-max | Opus leads GPQA Diamond by +17.2pp (91.3% vs 74.1%) |
| Simple classification / routing | Throughput | Haiku 4.5 | -- | Fast, cheap, accurate enough |
| Validation / error checking | Mid-tier or Throughput | Sonnet or Haiku | low-medium | Haiku for structural, Sonnet for semantic |
| Multi-agent orchestrator | Flagship | Opus 4.6 | high | Best at coordination; use cheaper models for subtasks |
| Sub-agent search/exploration | Throughput | Haiku 4.5 | -- | Claude Code's Explore agent defaults to Haiku |

**Decision framework**: Start with Sonnet 4.6 at medium effort. Upgrade to Opus when errors are costly, reasoning is complex, or the task is orchestration. Downgrade to Haiku when the task is well-constrained and outputs can be validated downstream.

---

## 2. Effort Levels and Thinking Budgets

### 2.1 Anthropic: Adaptive Thinking + Effort Parameter

Two modes exist for controlling reasoning depth:

**Adaptive thinking** (recommended for Opus 4.6 and Sonnet 4.6):
```json
{
  "thinking": {"type": "adaptive"},
  "output_config": {"effort": "high"}
}
```

**Manual thinking** (required for Haiku 4.5, legacy for 4.6 models):
```json
{
  "thinking": {"type": "enabled", "budget_tokens": 10000}
}
```

| Effort Level | Behavior | Use Case | Availability |
|---|---|---|---|
| **max** | Maximum capability, no constraints on thinking depth | Deepest reasoning, most thorough analysis | Opus 4.6 only |
| **high** | Deep reasoning, always thinks. API default for both Opus and Sonnet. | Complex reasoning, difficult coding, agentic tasks | Opus 4.6, Sonnet 4.6 |
| **medium** | Balanced. May skip thinking for simple queries. Anthropic recommends as practical starting point for Sonnet. | Agentic tasks balancing speed/cost/performance | Opus 4.6, Sonnet 4.6 |
| **low** | Most efficient. Skips thinking for simple tasks. | Simple classification, quick lookups, high-volume, subagents | Opus 4.6, Sonnet 4.6 |

**Critical detail**: Thinking tokens are billed at output token rates. For Opus 4.6, that's $25/MTok. A response using 10k thinking tokens costs $0.25 just for thinking. At low effort, Claude may skip thinking entirely -- significant cost savings.

### 2.2 OpenAI: reasoning_effort Parameter

The o-series exposes `reasoning_effort` (low/medium/high):
- **low**: Optimizes for speed, brings latency closer to GPT models
- **medium**: Default balanced tradeoff
- **high**: Deep deliberation, maximizes pass rates on rigorous benchmarks

**Caution**: High effort on smaller distilled models (like o4-mini) can occasionally produce erratic behavior or failed outputs. Max effort is best reserved for largest-parameter models.

### 2.3 Google: thinkingBudget Parameter

- `-1`: Dynamic thinking (model decides how much to think, up to internal max)
- `0`: Bypass reasoning entirely (Flash and Flash-Lite only). Fastest response.
- `N` (integer): Soft cap on reasoning tokens

### 2.4 The Router Problem

Model routers (OpenRouter, auto-routing services) systematically bias toward cheaper models because:
1. Cost is concrete; quality is estimated
2. Task difficulty is often not apparent from the prompt alone
3. Router training data lags behind current models
4. Quality thresholds vary by use case

**Recommendation**: Manual model selection is better for quality-sensitive work. Routers are best for cost optimization on tasks where "good enough" truly is good enough.

---

## 3. The Cognitive Load Dimension: Human Review Burden

*This section addresses a critical and under-researched dimension of model selection: the impact on the human who must review AI-generated output.*

### 3.1 Error Detectability Spectrum

Not all errors are equal. The key question isn't "how many errors?" but "what kind of errors remain, and how hard are they for a human to catch?"

| Error Type | Cognitive Load | Human Detection Rate | Risk Level |
|---|---|---|---|
| **Surface errors** (typos, formatting, wrong headers) | Trivial | Near 100% | Low -- human catches and fixes instantly |
| **Structural errors** (missing sections, wrong ordering) | Moderate | High with modest attention | Medium -- noticeable on careful read |
| **Embedded hallucinations** (plausible fabricated facts, wrong references) | Extremely high | Low -- requires independent verification | **Critical** -- defeats purpose of AI generation |
| **Subtle logic errors** (reasoning that sounds right but has a flaw) | Extremely high | Very low, especially under fatigue | **Critical** -- nearly impossible to catch |

**Key insight**: A cheaper model that makes 5 obvious surface errors may be preferable to one that makes 1 invisible embedded hallucination.

### 3.2 Automation Bias and Vigilance Decrement

Research findings:
- **Automation bias**: Humans systematically over-rely on automated suggestions. In healthcare CDSS research, incorrect automated advice increased commission errors by **26%** -- a finding directionally applicable to AI-assisted content review more broadly.
- **Vigilance decrement**: Human error-detection performance drops rapidly during sustained monitoring tasks due to cognitive fatigue.
- **Knowledge collapse** (Peterson, 2025, *AI and Society*): As humans substitute AI for cognitive effort, community shared knowledge degrades, making it progressively harder to catch subtle errors.

### 3.3 Error Type Distribution by Model Tier

Model tiers produce different error profiles:
- **Flagship models** (Opus 4.6, o3) are trained for **calibration** -- they're more likely to admit uncertainty or refuse a prompt rather than hallucinate. When they do err, errors tend to be in complex reasoning rather than factual fabrication.
- **Mid-tier models** (Sonnet 4.6, o4-mini) are optimized for constrained logic but tend to **invisibly hallucinate** when asked for detailed world knowledge they lack.
- **Throughput models** (Haiku, Flash-Lite) produce more frequent and varied errors, but many are surface-level and easily caught.

### 3.4 Mitigation Strategies

1. **Provenance markers**: Force AI to cite sources for every factual claim. Makes verification tractable -- the reviewer checks citations rather than reverse-engineering the entire document.
2. **Confidence flags**: Have the AI explicitly flag low-confidence claims or areas where it extrapolated beyond source material.
3. **Structured output for reviewability**: Separate factual content (verifiable) from interpretive content (judgment calls) so humans focus their review energy appropriately.
4. **Automated pre-screening**: Use validation lenses (structural, factual, coherence, domain) to catch machine-detectable errors before human review. This lets the human focus on what humans are strong at: feel, tone, coherence, fitness for purpose.
5. **The optimal division of labor**: AI handles factual accuracy and structural completeness (with validation). Humans handle feel, tone, high-level coherence, and fitness for purpose. If the human has to essentially rewrite the document, the AI generation was a net negative.

### 3.5 Implications for Model Selection

When choosing models, consider not just quality scores but the **cognitive hazard profile**:
- For documents that will be human-reviewed: prioritize models that minimize invisible errors, even if they make more surface errors.
- For code with automated tests: surface errors are caught by the test suite, so cheaper models with more errors may be fine if tests catch them.
- For content without automated validation: flagship models are worth the premium because hallucination detection falls entirely on the human.

---

## 4. Evaluation and Benchmarking Tooling

### 4.1 Tool Landscape

| Tool | Type | Cost | Best For | Key Differentiator |
|---|---|---|---|---|
| **Promptfoo** | OSS CLI (MIT, pending OpenAI acquisition announced 2026-03-09) | Free (enterprise tier available) | Multi-model comparison, red-teaming, CI/CD | Claude Agent SDK provider for full agentic workflow testing |
| **Braintrust** | Commercial platform | Free tier (1M spans); Pro $249/mo | Production eval + monitoring, A/B testing | Eval-first with autoevals library |
| **LangSmith** | Commercial platform | Free (1 seat, 5k traces); Plus $39/seat/mo | LangChain/LangGraph ecosystems | Deep multi-turn tracing, Align Evals calibration |
| **Langfuse** | OSS (MIT) | Free self-hosted; cloud from $59/mo | Self-hosted observability | True self-hosted with no restrictions |
| **Arize Phoenix** | Source-available (ELv2) | Free self-hosted; Pro $50/mo | Drift detection, compliance teams | OTel-native, hallucination detection templates |
| **DeepEval** | OSS (Apache 2.0) | Free | Python-first pytest-style testing | 50+ metrics, runs entirely locally |
| **W&B Weave** | Commercial (free tier non-commercial) | Free (non-commercial); paid scales up | ML experiment tracking | Strong versioning, leaderboards |
| **Maxim AI** | Commercial | Contact for pricing | Multi-turn agent simulation | Persona-based testing, agent resilience |

**Note on Promptfoo's OpenAI acquisition**: OpenAI announced its intent to acquire Promptfoo on 2026-03-09 (subject to closing conditions), committing to keep it open-source under MIT with continued multi-provider support. For users evaluating Claude models, this raises a potential neutrality concern -- monitor whether Anthropic provider support remains well-maintained. Langfuse and DeepEval are provider-neutral alternatives if this becomes an issue.

### 4.2 Promptfoo Deep Dive

Promptfoo is the most directly relevant tool for multi-model comparison. Key capabilities:

**Multi-model comparison** (core feature):
```yaml
providers:
  - id: anthropic:messages:claude-opus-4-6
    label: "Opus 4.6"
    config:
      temperature: 0
      max_tokens: 4096
  - id: anthropic:messages:claude-sonnet-4-6
    label: "Sonnet 4.6"
  - id: anthropic:messages:claude-haiku-4-5-20251001
    label: "Haiku 4.5"
  - id: openai:o4-mini
    label: "o4-mini"

prompts:
  - file://prompts/my-task.txt

defaultTest:
  assert:
    - type: cost
      threshold: 0.05
    - type: latency
      threshold: 30000
    - type: llm-rubric
      value: "Output is accurate, complete, and well-structured"
      provider: anthropic:messages:claude-opus-4-6

evaluateOptions:
  maxConcurrency: 4
  repeat: 3

tests:
  - vars:
      input: "Test case 1"
```

**Claude Agent SDK provider** -- tests full agentic workflows, not just single prompts:
```yaml
providers:
  - id: anthropic:claude-agent-sdk
    label: "Opus Agent"
    config:
      model: claude-opus-4-6
      working_dir: /path/to/project
      setting_sources: ['project']
      append_allowed_tools: ['Skill', 'Read', 'Write', 'Edit']
      max_budget_usd: 2.00
      permission_mode: acceptEdits
```

**Built-in assertion types** (partial list):
- `cost`, `latency` -- budget and timing thresholds
- `llm-rubric` -- LLM-as-judge with custom criteria
- `g-eval` -- chain-of-thought evaluation
- `select-best` -- compares outputs across providers, picks winner
- `factuality` -- checks against reference facts
- `is-json`, `contains-json` -- structural validation
- `javascript`, `python` -- custom evaluation functions
- Trajectory assertions: `trajectory:tool-used`, `trajectory:tool-sequence`, `trajectory:step-count`

**Default grader hierarchy**: When ANTHROPIC_API_KEY is set (without OpenAI), Claude becomes the default grader for all model-graded assertions.

### 4.3 LLM-as-Judge Patterns

**Three approaches:**
1. **Pointwise scoring**: Judge scores a single response (best for production monitoring)
2. **Pairwise comparison**: Judge compares two responses, picks better one (best for model selection A/B testing, >80% agreement with human preferences)
3. **Reference-based**: Judge compares output against ground truth (best for hallucination detection)

**Best practices:**
- Use binary or 3-point scales (reduces middle-clustering bias)
- Define each score level explicitly with boundary examples
- Split complex criteria into separate evaluators (one per dimension)
- Request chain-of-thought reasoning before the verdict
- Use structured output (JSON) for reliable parsing
- Set low temperature (0.1-0.3)
- Use a stronger model as judge (e.g., Opus to judge Sonnet/Haiku)

**Known biases:**

| Bias | Impact | Mitigation |
|---|---|---|
| Position bias | Favors first response in pairwise; 10%+ accuracy shift | Randomize order, run both orderings |
| Verbosity bias | Prefers longer answers regardless of substance | Explicitly penalize unnecessary verbosity |
| Self-preference | LLM rates own outputs higher | Use different model family as judge |
| Middle-clustering | Scores cluster around center | Use narrower scales, calibration examples |

### 4.4 Golden Datasets

- **Target size**: ~100 examples minimum. 20-30 per skill/workflow type.
- **Bootstrapping**: Generate with your best model (Opus), human-review and curate, promote confirmed outputs to golden status.
- **Requirements**: Include easy/medium/hard cases, edge cases, expected failure modes. Decontaminate from fine-tuning data. Evolve continuously as new failure modes emerge.

---

## 5. Claude Code Implementation

### 5.1 Model Selection Mechanisms

| Method | Scope | Priority |
|---|---|---|
| Managed settings (`availableModels`) | Organization-wide | Highest (cannot override) |
| CLI flag (`--model opus`) | Session | High |
| `/model sonnet` command | Mid-session switch | High |
| `Option+P` (macOS) / `Alt+P` | Mid-prompt switch | High |
| `ANTHROPIC_MODEL` env var | Environment-wide | Medium |
| `settings.json` (`"model": "opus"`) | Persistent default | Low |
| Sub-agent frontmatter (`model: haiku`) | Per sub-agent | Per-agent |
| Skill frontmatter (`model: sonnet`) | Per skill | Per-skill |
| `CLAUDE_CODE_SUBAGENT_MODEL` env var | All sub-agents | Overrides sub-agent frontmatter |

**Skill/sub-agent frontmatter example:**
```yaml
---
name: my-search-skill
model: haiku
description: Fast codebase search using Haiku for cost efficiency
---

Search the codebase for the requested pattern...
```

**Aliases**: `default`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opus[1m]`, `opusplan`

**opusplan**: Opus for planning, auto-switches to Sonnet for execution. A built-in hybrid routing strategy.

**Effort**: `/effort low|medium|high|max|auto`, `--effort` flag, `CLAUDE_CODE_EFFORT_LEVEL` env var, or `"effortLevel"` in settings.json.

### 5.2 Observability

**Built-in:**
- `/cost` command: total cost, API duration, wall duration, lines changed
- `showTurnDuration` setting: per-turn timing ("Cooked for 1m 6s")
- `--verbose` / `Ctrl+O`: full turn-by-turn output with token counter
- `--debug "api,mcp"`: debug logging with category filtering

**Programmatic (print mode):**
```bash
claude -p "your prompt" --model opus --output-format json
```
Returns: `duration_ms`, `duration_api_ms`, `total_cost_usd`, `usage` (token breakdown), `modelUsage` (per-model cost/tokens).

**OpenTelemetry:**
Set `CLAUDE_CODE_ENABLE_TELEMETRY=1`. Exports:
- Metrics: `claude_code.token.usage`, `claude_code.cost.usage`, `claude_code.session.count`, `claude_code.active_time.total`
- Events: `claude_code.api_request` (with model, cost_usd, duration_ms, tokens), `claude_code.tool_result` (with duration_ms, success/fail)

**Community tooling:**
- **ccusage**: CLI tool for cross-session cost tracking (11k+ GitHub stars, currently v18+). Provides 5-hour billing window reports (`blocks`) with per-model cost breakdowns and daily summaries.
- **claude-code-hooks-multi-agent-observability**: OSS project using PreToolUse/SubagentStart hooks to POST telemetry to local SQLite/Vue.js dashboard.
- **Langfuse integration**: Uses Stop hook to convert conversation transcripts into OTel traces grouped by session_id.

### 5.3 Scripting Multi-Model Benchmarks

```bash
#!/bin/bash
MODELS=("claude-opus-4-6" "claude-sonnet-4-6" "claude-haiku-4-5-20251001")
PROMPT="Generate a session prep for the next encounter"

for model in "${MODELS[@]}"; do
  echo "=== Testing $model ==="
  time claude -p "$PROMPT" \
    --model "$model" \
    --output-format json \
    --max-budget-usd 2.00 \
    > "results_${model}.json"
done

# Compare results
for f in results_*.json; do
  echo "$f: cost=$(jq .total_cost_usd $f), time=$(jq .duration_ms $f)ms"
done
```

---

## 6. Pydantic AI Implementation

### 6.1 Model Selection

**Agent-level** (constructor):
```python
agent = Agent('anthropic:claude-sonnet-4-6')
```

**Runtime switching** (per-call):
```python
result1 = agent.run_sync('Question', model='anthropic:claude-opus-4-6')
result2 = agent.run_sync('Question', model='openai:o4-mini')
```

**Override context manager** (for testing):
```python
with agent.override(model='anthropic:claude-haiku-4-5'):
    result = agent.run_sync('Quick classification task')
```

**FallbackModel** (resilience):
```python
from pydantic_ai.models.fallback import FallbackModel
fallback = FallbackModel(
    'openai:gpt-4o',
    'anthropic:claude-sonnet-4-6',
    fallback_on=(ModelAPIError,),
)
```

### 6.2 Thinking and Effort Configuration

```python
from pydantic_ai.models.anthropic import AnthropicModelSettings

# Adaptive thinking (recommended for 4.6 models)
settings = AnthropicModelSettings(
    anthropic_thinking={'type': 'adaptive'},
    anthropic_effort='high',
)

# Manual thinking (required for Haiku 4.5)
settings = AnthropicModelSettings(
    anthropic_thinking={'type': 'enabled', 'budget_tokens': 10000},
)
```

**Settings merge hierarchy** (lowest to highest priority):
1. Model-level defaults
2. Agent-level defaults (`Agent(model_settings=...)`)
3. Runtime overrides (`run_sync(model_settings=...)`)

### 6.3 Observability

**Logfire (native, 3 lines):**
```python
import logfire
logfire.configure()
logfire.instrument_pydantic_ai()
```

**InstrumentedModel (any OTel backend):**
```python
from pydantic_ai.models.instrumented import InstrumentedModel, InstrumentationSettings
model = InstrumentedModel('openai:gpt-4o', options=InstrumentationSettings(
    include_content=True,
    tracer_provider=my_tracer,
    meter_provider=my_meter,
))
```

**Programmatic usage data:**
```python
result = agent.run_sync('Question')
usage = result.usage()  # tokens, cache stats
```

### 6.4 Multi-Model Testing

```python
from pydantic_evals import Case, Dataset

dataset = Dataset(cases=[
    Case(name='haunt_encounter', inputs='Generate a haunt for Sister Abeni',
         expected_output='reference text'),
])

agent = Agent()
for model_name in ['anthropic:claude-opus-4-6', 'anthropic:claude-sonnet-4-6']:
    with agent.override(model=model_name):
        report = dataset.evaluate_sync(lambda q: agent.run_sync(q).output)
        report.print(include_input=True, include_output=True)
```

---

## 7. Practical Testing Methodology

### 7.1 The Multi-Model Comparison Workflow

**Step 1**: Define test cases with expected outputs or evaluation criteria
**Step 2**: Configure promptfoo YAML with target models
**Step 3**: Run `promptfoo eval` (captures cost, latency, quality per model)
**Step 4**: Run `promptfoo view` for side-by-side comparison matrix
**Step 5**: Export results (`results.json`) for statistical analysis

For Claude Code skills specifically, use the Claude Agent SDK provider to test full skill executions.

### 7.2 Validate-and-Fix Loop Economics

The fundamental tradeoff: expensive model with fewer iterations vs. cheap model with more iterations.

**Context accumulation makes this non-linear**: Each retry includes prior output + error feedback as additional input tokens, making later iterations progressively more expensive:

```
Total_cost(model, N) = Σ over i=1 to N:
    input_cost × (base_prompt + i × feedback_size) +
    output_cost × output_size(i)
```

**Key findings:**
- **FrugalGPT cascades** (Chen et al., 2023): Route to cheap model first, escalate only on failure. Up to 98% cost reduction matching flagship quality.
- **Error persistence**: If a model fails to fix an error after 3-4 iterations, further iterations typically burn tokens without converging. Cap retry loops at 4-5 attempts.
- **Convergence rates**: Flagship models typically converge in 1-2 iterations. Mid-tier models may need 3-4. Throughput models often fail to converge on complex tasks.
- **The crossover point**: For complex tasks, the total cost of (Haiku × 5 iterations with growing context) can exceed (Opus × 1 iteration). For simple tasks with deterministic validation (e.g., JSON schema), cheap model + retry is almost always cheaper.

### 7.3 Statistical Rigor

- **Minimum runs**: 10 per configuration for reliable statistics (5 minimum for quick checks)
- **Temperature**: Set to 0 for all models to minimize variance (but temperature=0 does NOT guarantee determinism)
- **Target variance**: Coefficient of Variation < 0.05
- **Metrics to report**: Mean ± standard deviation for cost and quality. P50, P90, P99 for latency.
- **Significance testing**: McNemar's test for binary pass/fail evaluations (e.g., JSON schema validation). Wilcoxon signed-rank test or bootstrap confidence intervals for rubric-scored evaluations. GLMMs to decompose task difficulty from API noise.
- **Variance warning**: Identical prompts at temperature 0 can fluctuate 10-15% day-over-day due to floating-point optimizations and silent model updates.

### 7.4 A/B Testing in Production

1. **Formulate a testable hypothesis** (e.g., "Replacing Opus with Sonnet for classification will reduce TTFT by 40% without dropping accuracy below 98%")
2. **Bifurcate traffic** via gateway routing with persistent user assignment
3. **Measure three dimensions**: Technical (latency, tokens, cost), Quality (LLM-as-judge scores), Business (user satisfaction, rejection rates)
4. **Stratified sampling**: 100% eval in dev/CI, 5% random sampling in production (prioritize sessions with user abandonment or excessive retries)

---

## 8. Quick Reference

### Decision Matrix

```
Is the task well-constrained with deterministic validation?
├── YES → Haiku 4.5, effort N/A, validate with schema/tests
│         (If validation fails after 4 retries → escalate to Sonnet)
└── NO
    ├── Does it require novel reasoning or multi-step logic?
    │   ├── YES → Opus 4.6, effort high (or max for hardest problems)
    │   └── NO → Sonnet 4.6, effort medium
    └── Will a human review the output?
        ├── YES → Prioritize model tier that minimizes invisible errors
        │         (Flagship > Mid-tier for cognitive hazard profile)
        └── NO → Optimize for cost with automated validation
```

### Cost Comparison (Typical 10k input / 2k output call)

| Model | Input Cost | Output Cost | Total | Relative (Haiku=1x) |
|---|---|---|---|---|
| Haiku 4.5 | $0.01 | $0.01 | **$0.02** | 1x |
| Sonnet 4.6 | $0.03 | $0.03 | **$0.06** | 3x |
| Opus 4.6 | $0.05 | $0.05 | **$0.10** | 5x |
| Opus 4.6 (batch) | $0.025 | $0.025 | **$0.05** | 2.5x |

### Tool Selection

| Need | Tool |
|---|---|
| Compare N models on same prompts | Promptfoo |
| Test full Claude Code skills across models | Promptfoo + Claude Agent SDK provider |
| Compare N models in Pydantic AI | Pydantic Evals + agent.override() |
| Production monitoring | Braintrust or Langfuse |
| Self-hosted observability | Langfuse (MIT) or Arize Phoenix (ELv2) |
| Claude Code session cost tracking | `/cost`, `--output-format json`, ccusage |
| Cross-session cost analytics | ccusage, OTel export |
| Quick bash-level model comparison | `claude -p --model X --output-format json` in a loop |

### Cost Optimization Checklist

- [ ] Use batch API for non-time-sensitive work (50% discount)
- [ ] Use prompt caching aggressively (cache hits = 10% of input price)
- [ ] Use Haiku for validation/classification steps in pipelines
- [ ] Use effort=low for sub-agent calls within multi-agent systems
- [ ] Reserve Opus + high effort for orchestrator and final-quality-critical steps
- [ ] Cap retry loops at 4-5 iterations
- [ ] Consider FrugalGPT cascade: cheap model first, escalate on failure
- [ ] Use stratified sampling in production (5% LLM-as-judge, not 100%)
