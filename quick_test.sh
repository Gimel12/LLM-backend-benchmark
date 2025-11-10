#!/bin/bash
# Quick test script to verify vLLM installation and GPU availability

echo "======================================"
echo "vLLM Installation Test"
echo "======================================"
echo ""

# Check Python version
echo "1. Checking Python version..."
python3 --version
echo ""

# Check vLLM installation
echo "2. Checking vLLM installation..."
python3 -c "import vllm; print(f'vLLM version: {vllm.__version__}')"
echo ""

# Check GPU availability
echo "3. Checking GPU availability..."
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
echo ""

# Check CUDA availability in PyTorch
echo "4. Checking CUDA in PyTorch..."
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA devices: {torch.cuda.device_count()}')"
echo ""

# Check Ollama
echo "5. Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "Ollama is installed"
    ollama list
else
    echo "Ollama is not installed"
    echo "To install: curl -fsSL https://ollama.com/install.sh | sh"
fi
echo ""

echo "======================================"
echo "Installation check complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. For vLLM: python3 vllm_benchmark.py --model <your-model>"
echo "2. For Ollama: ollama pull gpt-oss:120b && python3 ollama_benchmark.py --model gpt-oss:120b"
echo "3. Compare both: python3 compare_benchmarks.py --vllm-model <model> --ollama-model gpt-oss:120b"
