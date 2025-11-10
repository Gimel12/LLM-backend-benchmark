#!/bin/bash
# Start vLLM server with OpenAI-compatible API
# This allows you to chat with the model and see real-time token generation

MODEL="openai/gpt-oss-120b"
PORT=8000

echo "Starting vLLM server for $MODEL"
echo "Server will be available at: http://localhost:$PORT"
echo ""
echo "Once started, you can:"
echo "  - Use the web chat: Open chat_interface.html in your browser"
echo "  - Use CLI chat: python3 chat_cli.py"
echo "  - Test with curl: curl http://localhost:$PORT/v1/models"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

vllm serve "$MODEL" \
    --tensor-parallel-size 2 \
    --port $PORT \
    --trust-remote-code \
    --gpu-memory-utilization 0.90
