#!/bin/bash
# One-command vLLM benchmark for openai/gpt-oss-120b
# Just run: ./benchmark_vllm_now.sh

echo "🚀 Starting vLLM benchmark for openai/gpt-oss-120b"
echo "   Using 2 GPUs with tensor parallelism"
echo ""

python3 vllm_benchmark.py \
    --model "openai/gpt-oss-120b" \
    --num-prompts 10 \
    --max-tokens 512 \
    --tensor-parallel-size 2 \
    --prompt "Explain quantum computing in simple terms"

echo ""
echo "✅ Benchmark complete!"
echo ""
echo "To compare with Ollama:"
echo "  1. Run: ollama pull gpt-oss:120b"
echo "  2. Run: ./run_gpt_oss_120b.sh and choose option 3"
