#!/bin/bash
# Start vLLM server using only 1 GPU (for comparison)

MODEL="openai/gpt-oss-120b"
PORT=8000

echo "Starting vLLM server for $MODEL (1 GPU ONLY)"
echo "Server will be available at: http://localhost:$PORT"
echo ""
echo "🔧 Configuration:"
echo "  - Tensor Parallel Size: 1 (using only 1 GPU)"
echo "  - GPU Memory: 90% utilization"
echo ""
echo "Once started, you can:"
echo "  - Continue using the web chat interface"
echo "  - Compare speed with 2-GPU version"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

vllm serve "$MODEL" \
    --tensor-parallel-size 1 \
    --port $PORT \
    --trust-remote-code \
    --gpu-memory-utilization 0.90
