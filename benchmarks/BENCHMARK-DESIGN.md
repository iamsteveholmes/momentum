# Benchmark Design Document

Based on analysis of Claude Code benchmark sessions, this document outlines what we're measuring and why.

## 🎯 Key Metrics from Claude Code Sessions

### Session `cdb7de2f` - Full Sprint Planning with AVFL
- **Duration**: ~6 hours active time
- **Tool Calls**: 331 total
  - Bash: 121 calls
  - Read: 82 calls
  - Edit: 37 calls
  - Agent: 23 calls
  - TaskUpdate: 20 calls
- **Subagent Spawns**: 23 total
  - 5 create-story (double-spawned)
  - 5 research agents
  - 2 Explore agents
  - 2 general-purpose agents
  - 3 AVFL validators
  - 1 AVFL fixer
- **Model Mix**: 99% Sonnet 4.6 / 1% Opus 4.6
- **Artifacts Produced**: 5 Gherkin specs, sprint files, DEC-003 capture

### Session `621fb06b` - Impetus → Refine → Epic-Grooming
- **Duration**: ~1h 24m active time
- **Tool Calls**: 135 total
  - Bash: 67 calls
  - TaskUpdate: 30 calls
  - TaskCreate: 15 calls
  - Read: 14 calls
- **Subagent Spawns**: 4 total
  - 2 Explore agents (PRD/Architecture discovery)
  - 2 general-purpose agents (document updates)
- **Model Mix**: 85% Opus 4.7 / 15% Sonnet 4.6

### Session `6d6ec9b2` - Sprint Planning Initiation
- **Duration**: ~3 min 15s active time
- **Tool Calls**: 39 total
  - Bash: 18 calls
  - TaskCreate: 10 calls
  - Read: 6 calls
- **Subagent Spawns**: 0 (stopped at Step 2 gate)
- **Model Mix**: 100% Opus 4.7

## 📏 Benchmark Metrics to Capture

### 1. Performance Efficiency
- **Wall-clock time** per workflow phase
- **Tool call count and distribution**
- **Response latency** per tool call
- **Token usage** (if available)

### 2. Output Quality
- **Story breakdown completeness**
- **Gherkin spec quality and coverage**
- **Validation findings depth**
- **Artifact consistency**

### 3. Resource Utilization
- **API cost estimation** (where applicable)
- **Memory requirements**
- **Parallel processing capability**

### 4. Workflow Fidelity
- **Skill invocation sequence accuracy**
- **Subagent spawn patterns**
- **Task management fidelity**
- **State consistency**

## 🧪 Test Scenarios

### Scenario 1: Sprint Planning Phase
**Objective**: Measure planning breakdown speed and quality
**Metrics**:
- Time to generate story breakdowns
- Tool call efficiency (Read/Bash ratio)
- Story detail completeness
- Dependency mapping accuracy

### Scenario 2: AVFL Validation Phase
**Objective**: Measure validation thoroughness vs speed
**Metrics**:
- AVFL finding count and quality
- Validator subagent performance
- Fixer effectiveness
- False positive/negative rates

### Scenario 3: Refinement Phase
**Objective**: Measure drift detection accuracy
**Metrics**:
- Drift finding precision
- Document update quality
- Epic grooming effectiveness

## 📊 Model Comparison Matrix

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| Qwen3-Coder | ⚡ Fast | ⭐⭐⭐⭐ | Free | Technical breakdowns, coding tasks |
| Llama 3.3 70B | ⚡ Fast | ⭐⭐⭐ | Free | General planning, balanced performance |
| GPT-OSS 120B | ⚡⚡ Moderate | ⭐⭐⭐⭐ | Free | Complex reasoning, large context |
| Nemotron 120B | ⚡⚡ Moderate | ⭐⭐⭐⭐⭐ | Free | Deep validation, adversarial review |
| Opus 4.6/4.7 | 🐌 Slow | ⭐⭐⭐⭐⭐ | $$$ | Enterprise planning, complex orchestration |

## 🎯 Recommendations for Testing

### Phase-Based Model Selection
1. **Sprint Planning**: Qwen3-Coder (fast, accurate for technical breakdowns)
2. **AVFL Validation**: Nemotron 120B (thorough validation)
3. **Refinement**: Llama 3.3 70B (balanced approach)

### Hybrid Approach Benefits
- **90% speed** of fastest model for planning
- **85% quality** of Opus for validation
- **0% cost** vs Claude Code paid models
- **Flexible switching** based on workflow phase

## 📈 Success Criteria

### Performance Thresholds
- **Sprint Planning**: < 30 minutes for full breakdown
- **Validation**: < 60 minutes for complete AVFL cycle
- **Refinement**: < 20 minutes for drift detection

### Quality Benchmarks
- **Story Coverage**: 100% of required stories identified
- **Validation Depth**: 90%+ of critical issues detected
- **Artifact Quality**: Comparable to Claude Code baselines

### Cost Optimization
- **Target**: 90%+ reduction vs Claude Code paid usage
- **Constraint**: No quality degradation beyond 10% threshold