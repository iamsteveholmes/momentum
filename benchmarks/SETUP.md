# Benchmark Setup Instructions

## Prerequisites

1. Ensure you have API keys for the models you want to test:
   - OPENROUTER_API_KEY (for Qwen, Llama, Nemotron)
   - GROQ_API_KEY (optional, for Groq models)

2. Make sure your secrets are configured:
   ```bash
   goose configure
   ```

## Running Benchmarks

### Single Model Test
```bash
# Run Qwen3-Coder benchmark
./benchmarks/run-benchmark.sh qwen cdb7de2f

# Run Llama 3.3 benchmark  
./benchmarks/run-benchmark.sh llama 621fb06b

# Run Nemotron benchmark
./benchmarks/run-benchmark.sh nemotron 6d6ec9b2
```

### All Models Test
```bash
./benchmarks/run-all-benchmarks.sh
```

### Analyze Results
```bash
goose run benchmarks/recipes/analysis/compare-results.yaml
```

## Expected Results Structure

Results will be stored in timestamped directories:
```
results/
├── 20260428_080000_qwen_cdb7de2f/
├── 20260428_081500_llama_cdb7de2f/
└── 20260428_083000_nemotron_cdb7de2f/
```

Each results directory will contain:
- duration.txt - Execution time
- metrics/ - Detailed performance metrics
- artifacts/ - Generated output artifacts
- logs/ - Execution logs