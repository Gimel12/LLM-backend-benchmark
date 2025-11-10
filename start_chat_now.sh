#!/bin/bash
# Quick start script to launch chat interface
# This starts the server in the background and opens the web interface

echo "🚀 Starting vLLM Chat Interface"
echo ""

# Check if server is already running
if curl -s http://localhost:8000/v1/models > /dev/null 2>&1; then
    echo "✅ Server is already running!"
    echo ""
    echo "Opening chat interface..."
    sleep 1
    xdg-open chat_interface.html 2>/dev/null || echo "Please open: file://$(pwd)/chat_interface.html"
    echo ""
    echo "Or use CLI chat: python3 chat_cli.py"
    exit 0
fi

echo "⚠️  Server is not running yet."
echo ""
echo "Starting vLLM server (this will take ~20 minutes first time)..."
echo "The model needs to load into GPU memory."
echo ""
echo "Terminal output will show server logs below."
echo "Wait for 'Application startup complete' message."
echo ""
echo "Then open the chat interface:"
echo "  - Web: Open chat_interface.html in your browser"
echo "  - CLI: python3 chat_cli.py"
echo ""
echo "Press Ctrl+C to stop the server when done."
echo ""
echo "Starting in 3 seconds..."
sleep 3
echo ""

# Start the server
./start_vllm_server.sh
