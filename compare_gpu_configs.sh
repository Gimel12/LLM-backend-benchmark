#!/bin/bash
# Quick switcher between 1 GPU and 2 GPU configurations

echo "======================================"
echo "vLLM GPU Configuration Switcher"
echo "======================================"
echo ""
echo "Current results:"
echo "  ✅ 2 GPUs: ~200 tokens/second"
echo "  ❓ 1 GPU: Let's test!"
echo ""
echo "Choose configuration:"
echo "  1) Use 1 GPU only (test single GPU speed)"
echo "  2) Use 2 GPUs (tensor parallel - maximum speed)"
echo "  3) Exit"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🔄 Starting vLLM with 1 GPU..."
        echo ""
        echo "⚠️  If server is already running, stop it first (Ctrl+C)"
        echo "   Then run: ./start_vllm_1gpu.sh"
        echo ""
        echo "Expected speed: ~80-120 tokens/second"
        echo ""
        ./start_vllm_1gpu.sh
        ;;
    2)
        echo ""
        echo "🚀 Starting vLLM with 2 GPUs (tensor parallel)..."
        echo ""
        echo "⚠️  If server is already running, stop it first (Ctrl+C)"
        echo "   Then run: ./start_vllm_server.sh"
        echo ""
        echo "Expected speed: ~200 tokens/second"
        echo ""
        ./start_vllm_server.sh
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
