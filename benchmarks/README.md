# Momentum Model Benchmark Framework

This framework allows you to benchmark different models for momentum workflows using Goose recipes.

## 📁 Structure

```
benchmarks/
├── recipes/                    # Benchmark recipes
│   ├── sprint-planning-benchmark.yaml     # Main controller
│   ├── model-comparison-qwen.yaml         # Qwen3-Coder variant
│   ├── model-comparison-llama.yaml        # Llama 3.3 variant
│   ├── model-comparison-nemotron.yaml     # Nemotron variant
│   └── analysis/
│       └── compare-results.yaml           # Results analyzer
├── data/                      # Test data and baselines
└── results/                   # Benchmark results
```

## ▶️ How to Run Benchmarks

### 1. Run Individual Model Benchmarks

```bash
# Run Qwen3-Coder benchmark
goose run benchmarks/recipes/model-comparison-qwen.yaml

# Run Llama 3.3 benchmark
goose run benchmarks/recipes/model-comparison-llama.yaml

# Run Nemotron benchmark
goose run benchmarks/recipes/model-comparison-nemotron.yaml
```

### 2. Run Comparative Analysis

```bash
# Analyze all results
goose run benchmarks/recipes/analysis/compare-results.yaml
```

## 🎯 Benchmark Focus Areas

Based on your Claude Code sessions, benchmarks focus on:

1. **Sprint Planning Efficiency**
   - Tool call patterns
   - Execution time
   - Story breakdown quality

2. **Validation Thoroughness**
   - AVFL findings quality
   - Edge case detection
   - Adversarial reasoning

3. **Resource Utilization**
   - Token usage (cost)
   - Memory requirements
   - Response times

## 📊 Expected Outputs

Each benchmark run will generate:
- Execution metrics
- Output artifacts
- Performance comparisons
- Cost analysis
- Quality assessments

## 🚀 Next Steps

1. Run each model benchmark against the same repository state
2. Collect and analyze results
3. Choose optimal models for each workflow phase
4. Create a hybrid approach using different models for different phases