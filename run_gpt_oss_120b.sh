#!/bin/bash
# Quick start script for benchmarking openai/gpt-oss-120b
# Model: https://huggingface.co/openai/gpt-oss-120b

MODEL_NAME="openai/gpt-oss-120b"
OLLAMA_MODEL="gpt-oss:120b"

echo "======================================"
echo "GPT-OSS-120B Benchmark Runner"
echo "======================================"
echo ""
echo "Model: $MODEL_NAME"
echo "Your GPUs: 2x NVIDIA RTX PRO 6000 (196GB VRAM)"
echo ""

# Check if Ollama model is available
echo "Checking Ollama model..."
if ollama list | grep -q "gpt-oss:120b"; then
    echo "✅ Ollama model is available"
    OLLAMA_AVAILABLE=true
else
    echo "⚠️  Ollama model not found"
    echo ""
    read -p "Would you like to pull gpt-oss:120b for Ollama? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Pulling Ollama model (this may take a while)..."
        ollama pull gpt-oss:120b
        OLLAMA_AVAILABLE=true
    else
        echo "Skipping Ollama benchmark"
        OLLAMA_AVAILABLE=false
    fi
fi

echo ""
echo "======================================"
echo "Choose benchmark option:"
echo "======================================"
echo "1) vLLM only (recommended to test first)"
echo "2) Ollama only"
echo "3) Both (full comparison)"
echo "4) Exit"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Running vLLM benchmark with 2 GPUs..."
        python3 vllm_benchmark.py \
            --model "$MODEL_NAME" \
            --num-prompts 10 \
            --max-tokens 512 \
            --tensor-parallel-size 2 \
            --prompt "Explain quantum computing in simple terms"
        ;;
    2)
        if [ "$OLLAMA_AVAILABLE" = true ]; then
            echo ""
            echo "Running Ollama benchmark..."
            python3 ollama_benchmark.py \
                --model "$OLLAMA_MODEL" \
                --num-prompts 10 \
                --max-tokens 512 \
                --prompt "Explain quantum computing in simple terms"
        else
            echo "Ollama model not available. Please pull it first:"
            echo "  ollama pull gpt-oss:120b"
        fi
        ;;
    3)
        if [ "$OLLAMA_AVAILABLE" = true ]; then
            echo ""
            echo "Running full comparison (this will take a while)..."
            python3 compare_benchmarks.py \
                --vllm-model "$MODEL_NAME" \
                --ollama-model "$OLLAMA_MODEL" \
                --num-prompts 10 \
                --max-tokens 512 \
                --tensor-parallel-size 2 \
                --prompt "Explain quantum computing in simple terms"
        else
            echo "Ollama model not available. Please pull it first:"
            echo "  ollama pull gpt-oss:120b"
        fi
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "Benchmark Complete!"
echo "======================================"
echo ""
echo "For more options, use the scripts directly:"
echo "  python3 vllm_benchmark.py --help"
echo "  python3 ollama_benchmark.py --help"
echo "  python3 compare_benchmarks.py --help"
