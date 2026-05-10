#!/bin/bash

# Momentum Model Benchmark Runner
# Usage: ./run-benchmark.sh [model] [session]

set -e

MODEL=${1:-qwen}
SESSION=${2:-cdb7de2f}
RESULTS_DIR="results/$(date +%Y%m%d_%H%M%S)_${MODEL}_${SESSION}"

echo "🚀 Starting Momentum Benchmark"
echo "Model: $MODEL"
echo "Session: $SESSION"
echo "Results: $RESULTS_DIR"
echo "======================================"

# Create results directory
mkdir -p "$RESULTS_DIR"

# Function to run benchmark
run_benchmark() {
    local model=$1
    local session=$2
    local results_dir=$3
    
    echo "▶️  Running $model benchmark for session $session..."
    
    # Start timing
    start_time=$(date +%s)
    
    # Run the appropriate benchmark recipe
    case $model in
        qwen)
            goose run -i benchmarks/recipes/model-comparison-qwen.yaml
            ;;
        llama)
            goose run -i benchmarks/recipes/model-comparison-llama.yaml
            ;;
        nemotron)
            goose run -i benchmarks/recipes/model-comparison-nemotron.yaml
            ;;
        *)
            echo "Unknown model: $model"
            exit 1
            ;;
    esac
    
    # End timing
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    
    echo "✅ Benchmark completed in $duration seconds"
    echo "Duration: $duration seconds" > "$results_dir/duration.txt"
}

# Run the benchmark
run_benchmark "$MODEL" "$SESSION" "$RESULTS_DIR"

# Generate analysis
echo "📊 Generating analysis..."
goose run --recipe benchmarks/recipes/analysis/compare-results.yaml

echo "🎉 Benchmark complete!"
echo "Results stored in: $RESULTS_DIR"