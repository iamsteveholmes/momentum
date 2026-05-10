#!/bin/bash

# Run all Momentum Model Benchmarks
# Usage: ./run-all-benchmarks.sh

set -e

echo "🚀 Starting All Momentum Model Benchmarks"
echo "========================================"

MODELS=("qwen" "llama" "nemotron")
SESSIONS=("cdb7de2f" "621fb06b" "6d6ec9b2")

for model in "${MODELS[@]}"; do
    for session in "${SESSIONS[@]}"; do
        echo ""
        echo "▶️  Running $model benchmark for session $session..."
        echo "--------------------------------------------------------"
        
        ./run-benchmark.sh "$model" "$session"
        
        echo "✅ Completed $model benchmark for session $session"
        echo ""
    done
done

echo "🎉 All benchmarks complete!"
echo "📊 Run the analysis script to compare results:"
echo "   goose run benchmarks/recipes/analysis/compare-results.yaml"