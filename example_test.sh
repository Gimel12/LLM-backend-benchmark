#!/bin/bash
# Example test with a smaller model to verify everything works
# before running the large 120B model

echo "======================================"
echo "Running Example Test with Small Model"
echo "======================================"
echo ""
echo "This will test vLLM with a small model (facebook/opt-125m)"
echo "to verify the setup before running larger models."
echo ""

# Test vLLM with a small model
echo "Testing vLLM with facebook/opt-125m..."
python3 vllm_benchmark.py \
    --model "facebook/opt-125m" \
    --num-prompts 5 \
    --max-tokens 128 \
    --tensor-parallel-size 1

echo ""
echo "======================================"
echo "Test complete!"
echo "======================================"
echo ""
echo "If this worked, you can now test with gpt-oss:120b:"
echo ""
echo "For vLLM (if model is on HuggingFace):"
echo "  python3 vllm_benchmark.py --model <huggingface-path> --tensor-parallel-size 2"
echo ""
echo "For Ollama:"
echo "  ollama pull gpt-oss:120b"
echo "  python3 ollama_benchmark.py --model gpt-oss:120b"
echo ""
echo "For comparison:"
echo "  python3 compare_benchmarks.py \\"
echo "    --vllm-model <huggingface-path> \\"
echo "    --ollama-model gpt-oss:120b \\"
echo "    --tensor-parallel-size 2"
