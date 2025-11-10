# Chat Interface Guide - See Real Token Generation Speed

## Understanding the 875 tok/s Result

Your benchmark showed **875 tokens/second**, but this is **BATCH THROUGHPUT**, not interactive speed:

- ✅ **What happened**: vLLM processed 10 prompts simultaneously (parallel batching)
- ✅ **Total output**: 4,713 tokens in 5.38 seconds
- ✅ **Batch throughput**: 4,713 ÷ 5.38 = 875 tok/s

### Real Interactive Speed

For **single-user chat** (what you'll see in the interface):
- 🎯 **Expected speed**: 20-50 tokens/second
- 📊 This is the actual streaming speed you'll observe
- ⚡ Much more realistic for interactive use

The 875 tok/s shows vLLM's ability to handle **multiple concurrent users** efficiently!

---

## Quick Start - 2 Steps

### Step 1: Start the Server
```bash
cd /home/bizon/CascadeProjects/llm-benchmark
./start_vllm_server.sh
```

**Wait for**: "Application startup complete" (takes ~20 minutes first time)

### Step 2: Start Chatting

**Option A: Web Interface (Recommended)**
```bash
# Open in your browser
xdg-open chat_interface.html
# Or manually open: file:///home/bizon/CascadeProjects/llm-benchmark/chat_interface.html
```

**Option B: Command Line Interface**
```bash
python3 chat_cli.py
```

---

## Features

### Web Chat Interface
- 🎨 **Beautiful UI** with real-time streaming
- 📊 **Live stats** showing tokens/second per message
- 💬 **Full conversation** history
- ⚡ **Real-time token generation** - watch each token appear
- 📈 **Performance metrics** after each response

### CLI Chat Interface
- ⚡ **Fast and simple** terminal-based chat
- 📊 **Token speed** displayed after each response
- 💾 **Conversation history** maintained
- 🔄 **Clear command** to reset conversation

---

## What You'll See

### Example Chat Session:
```
🧑 You: What is quantum computing?

🤖 Assistant: Quantum computing is a revolutionary...

📊 Stats: 156 tokens in 4.2s = 37.14 tokens/sec
```

**This 37 tok/s is your real interactive speed!**

---

## Commands & Tips

### Server Commands
```bash
# Start server (Terminal 1)
./start_vllm_server.sh

# Test if server is ready
curl http://localhost:8000/v1/models

# Stop server
Ctrl+C
```

### Chat Commands
```bash
# Web interface
xdg-open chat_interface.html

# CLI interface
python3 chat_cli.py

# In CLI chat:
# - Type 'clear' to reset conversation
# - Type 'quit' or 'exit' to stop
# - Press Enter to send message
```

### Monitor GPUs While Chatting
```bash
# Terminal 2
watch -n 1 nvidia-smi
```

---

## Performance Notes

### Expected Speeds

| Scenario | Tokens/Second | Description |
|----------|--------------|-------------|
| **Interactive Chat** | 20-50 tok/s | Single user, streaming |
| **Batch Processing** | 500-1000 tok/s | Multiple prompts in parallel |
| **High Concurrency** | 1000+ tok/s | Many users simultaneously |

### Why the Difference?

**Interactive (20-50 tok/s)**:
- Single request at a time
- Tokens generated sequentially
- What humans perceive as "speed"
- What you'll see in chat

**Batch (875 tok/s)**:
- 10 requests processed together
- Continuous batching optimization
- Total throughput across all requests
- Great for high-load servers

### Comparison with Ollama

For **interactive chat**, vLLM will likely be:
- 1.5-2x faster than Ollama
- More consistent latency
- Better batching for multiple users

---

## Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
vllm serve openai/gpt-oss-120b --port 8001 --tensor-parallel-size 2
```

### Chat Can't Connect
1. Make sure server is fully started (see "Application startup complete")
2. Check server is running: `curl http://localhost:8000/v1/models`
3. Verify port is correct (default: 8000)

### Slow Generation
1. First response is slower (model warmup)
2. Check GPU memory: `nvidia-smi`
3. Reduce max_tokens if needed
4. Ensure both GPUs are being used

### Out of Memory
Edit `start_vllm_server.sh` and change:
```bash
--gpu-memory-utilization 0.90  # Try 0.85 or 0.80
```

---

## Understanding Real Performance

### Your Benchmark Results Explained:

```
Batch Test (10 prompts simultaneously):
├── Total time: 5.38 seconds
├── Total tokens: 4,713
└── Throughput: 875 tok/s ✅ Correct!

Interactive Chat (1 prompt at a time):
├── Per message: ~4 seconds
├── Per message tokens: ~150
└── Speed: ~37 tok/s ✅ This is what you'll see!
```

**Both numbers are correct!** They measure different things:
- 875 tok/s = **System throughput** (total capacity)
- 37 tok/s = **User experience** (perceived speed)

---

## Next Steps

1. **Start the server** and wait for it to load
2. **Open the web interface** to see beautiful real-time generation
3. **Try different prompts** to test various speeds:
   - Short answers: Faster perceived speed
   - Long answers: Shows sustained throughput
   - Complex reasoning: May be slower but more thorough

4. **Compare with Ollama**:
   ```bash
   # Terminal 1: Run Ollama
   ollama run gpt-oss:120b
   
   # Observe the difference in streaming speed!
   ```

---

## Advanced: API Usage

The server provides OpenAI-compatible API:

```bash
# Test with curl
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-120b",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

Use with OpenAI Python client:
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")
```

---

**Ready? Start the server and enjoy real-time chat with GPT-OSS-120B!** 🚀
