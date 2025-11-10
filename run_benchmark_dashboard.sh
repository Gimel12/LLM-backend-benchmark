#!/bin/bash
# Launch the Load Testing Dashboard

echo "======================================"
echo "🚀 LLM Load Testing Dashboard"
echo "======================================"
echo ""
echo "This tool will:"
echo "  ✅ Test vLLM vs Ollama performance"
echo "  ✅ Show you which is faster"
echo "  ✅ Test how many concurrent users each can handle"
echo "  ✅ Recommend which backend to use for production"
echo ""
echo "======================================"
echo ""

# Check if vLLM is running
echo "Checking servers..."
if curl -s http://localhost:8000/v1/models > /dev/null 2>&1; then
    echo "✅ vLLM server is running on port 8000"
else
    echo "⚠️  vLLM server not detected on port 8000"
    echo "   Start it in another terminal: ./start_vllm_server.sh"
fi

# Check if Ollama is running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama server is running on port 11434"
else
    echo "⚠️  Ollama server not detected on port 11434"
    echo "   Make sure Ollama is running"
fi

echo ""
echo "Starting dashboard..."
echo ""

python3 benchmark_server.py
