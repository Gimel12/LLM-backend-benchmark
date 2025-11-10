# 🚀 Deployment Guide for Other Computer

Complete guide to deploy this benchmark suite on any machine.

## 📥 Quick Clone & Setup

```bash
# Clone the repository
git clone https://github.com/Gimel12/LLM-backend-benchmark.git
cd LLM-backend-benchmark

# Install Python dependencies
pip install vllm ollama flask flask-cors aiohttp requests

# Make scripts executable
chmod +x *.sh
```

## 🎯 What's Included

This repository contains a complete LLM benchmarking suite:

### 📊 Load Testing Dashboard (Main Feature)
- **Web-based comparison tool** for vLLM vs Ollama
- Tests concurrent users (1, 2, 5, 10, 20)
- Beautiful charts and visualizations
- Clear production recommendation

### 🔧 Core Scripts
- `start_vllm_server.sh` - Launch vLLM server
- `run_benchmark_dashboard.sh` - Start load testing dashboard
- `chat_cli.py` - Interactive CLI chat
- `serve_web_chat.py` - Web chat interface

### 📈 Benchmark Tools
- `vllm_benchmark.py` - vLLM performance testing
- `ollama_benchmark.py` - Ollama performance testing
- `compare_benchmarks.py` - Side-by-side comparison

### 📚 Documentation
- `LOAD_TESTING_GUIDE.md` - Complete load testing guide
- `OPTIMIZATION_REPORT.md` - Performance optimization details
- `CHAT_GUIDE.md` - Chat interface usage
- `REMOTE_ACCESS.md` - Network access setup

## 🏃 Quick Start (3 Steps)

### Step 1: Start vLLM Server
```bash
./start_vllm_server.sh
```

Wait for "Application startup complete" (~2-3 minutes on first run).

### Step 2: Start Ollama (Optional)
```bash
ollama serve
```

In another terminal, ensure model is available:
```bash
ollama pull gpt-oss:120b
```

### Step 3: Launch Dashboard
```bash
./run_benchmark_dashboard.sh
```

Open browser: `http://localhost:5000`

## 📊 Using the Load Testing Dashboard

### What It Does
1. ✅ Tests vLLM and Ollama with same prompt
2. ✅ Simulates multiple concurrent users
3. ✅ Measures throughput and latency
4. ✅ Shows when performance degrades
5. ✅ Recommends best backend for production

### Dashboard Features
- 🟢 Server status indicators
- 📝 Customizable test prompts
- 📊 Real-time performance charts
- 🎯 Production recommendations
- 📈 Scalability analysis

### Test Results Include
- **Throughput**: Tokens per second
- **Latency**: Average, P95, P99
- **Success Rate**: Request reliability
- **Scalability**: Performance under load

## 🖥️ System Requirements

### Minimum (Single User Testing)
- **GPU**: 1x 80GB VRAM (A100, H100, or similar)
- **RAM**: 64GB
- **Storage**: 150GB for models
- **OS**: Linux (Ubuntu 22.04+ recommended)

### Recommended (Load Testing)
- **GPU**: 2x 80GB+ VRAM (for tensor parallelism)
- **RAM**: 128GB+
- **Storage**: 250GB SSD
- **Network**: Gigabit for remote access

### Tested On
- 2x NVIDIA RTX PRO 6000 (98GB each)
- CUDA 13.0
- PyTorch 2.8.0
- vLLM 0.11.0

## 📦 Installation Details

### vLLM Installation
```bash
pip install vllm
```

### Ollama Installation
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Dashboard Dependencies
```bash
pip install flask flask-cors aiohttp
```

### Model Setup

**For vLLM:**
```bash
# Model downloads automatically on first run
# Using: openai/gpt-oss-120b from HuggingFace
```

**For Ollama:**
```bash
ollama pull gpt-oss:120b
```

## 🔧 Configuration

### vLLM Server Settings
Edit `start_vllm_server.sh`:
```bash
MODEL="openai/gpt-oss-120b"
TENSOR_PARALLEL_SIZE=2  # Number of GPUs
GPU_MEMORY_UTIL=0.90    # 90% GPU memory usage
PORT=8000
```

### Load Test Settings
Edit `benchmark_server.py`:
```python
VLLM_URL = "http://localhost:8000"
OLLAMA_URL = "http://localhost:11434"
TEST_PROMPT = "Your custom prompt here"
```

### Test User Counts
Edit in `benchmark_server.py`:
```python
user_counts = data.get('user_counts', [1, 2, 5, 10, 20])
# Change to: [1, 5, 10, 20, 50] for more load
```

## 🌐 Remote Access

### Access Dashboard from Another Computer

1. **Find server IP:**
```bash
hostname -I
```

2. **Open firewall (if needed):**
```bash
sudo ufw allow 5000
sudo ufw allow 8000
```

3. **Access from browser:**
```
http://SERVER_IP:5000
```

### Secure Remote Access (Optional)
Use SSH tunnel:
```bash
ssh -L 5000:localhost:5000 user@server
```

Then access: `http://localhost:5000`

## 📊 Running Benchmarks

### Load Testing Dashboard (Recommended)
```bash
./run_benchmark_dashboard.sh
```
- Web interface at `http://localhost:5000`
- Visual comparison of backends
- Production recommendation

### CLI Benchmarks
```bash
# vLLM only
python3 vllm_benchmark.py

# Ollama only
python3 ollama_benchmark.py

# Both (comparison)
python3 compare_benchmarks.py
```

### Interactive Chat
```bash
# CLI chat
python3 chat_cli.py

# Web chat
python3 serve_web_chat.py
# Then open: http://localhost:8080/chat_remote.html
```

## 🐛 Troubleshooting

### vLLM Server Won't Start
```bash
# Check CUDA
nvidia-smi

# Check GPU memory
nvidia-smi --query-gpu=memory.free --format=csv

# Try with less memory
# Edit start_vllm_server.sh, set:
# --gpu-memory-utilization 0.80
```

### Ollama Connection Failed
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve
```

### Dashboard Won't Load
```bash
# Check if port 5000 is free
lsof -i :5000

# Try different port
# Edit benchmark_server.py:
# port = 5001
```

### Out of Memory
```bash
# Use 1 GPU instead of 2
./start_vllm_1gpu.sh

# Reduce batch size in benchmarks
# Edit vllm_benchmark.py:
# --num-prompts 5 (instead of 10)
```

## 📈 Performance Expectations

### Single GPU (A100 80GB)
- vLLM: ~80-120 tok/s (single user)
- Ollama: ~60-100 tok/s (single user)

### Dual GPU (Tensor Parallel)
- vLLM: ~180-220 tok/s (single user)
- Ollama: ~120-160 tok/s (single user)

### Your Results (2x RTX PRO 6000)
- vLLM: 200 tok/s ✅ (excellent!)
- Batch: 875 tok/s (throughput mode)

## 🎯 Production Deployment

### Recommended Setup
1. **Run load tests** to determine capacity
2. **Choose backend** based on results
3. **Deploy with Docker** (optional)
4. **Add load balancer** for high traffic
5. **Monitor with Prometheus** (optional)

### Scaling Guidelines
- **<10 users**: Single instance sufficient
- **10-50 users**: 2 GPUs with tensor parallelism
- **50+ users**: Multiple instances + load balancer
- **100+ users**: Dedicated cluster

## 📝 Results Interpretation

### Throughput Chart
- Flat line = Good scaling
- Declining line = System overloaded
- Higher = Better

### Latency Chart
- Low & stable = Excellent
- Rising = System under pressure
- Compare P95 for user experience

### Success Rate
- 100% = Perfect reliability
- <100% = Requests failing (over capacity)

### Recommendation
- Dashboard shows clear winner
- Consider both speed and scalability
- Test with your actual workload

## 🔄 Updates

### Pull Latest Changes
```bash
git pull origin main
```

### Push Your Changes
```bash
git add .
git commit -m "Your changes"
git push origin main
```

## 📚 Additional Resources

- [vLLM Documentation](https://docs.vllm.ai/)
- [Ollama Documentation](https://ollama.ai/docs)
- [HuggingFace Model](https://huggingface.co/openai/gpt-oss-120b)

## 💡 Tips

1. **Run multiple test iterations** for accurate results
2. **Test during off-peak hours** for consistent benchmarks
3. **Monitor GPU temperatures** during load tests
4. **Document your results** for future reference
5. **Test with your actual prompts** not just defaults

## ⚡ Performance Optimizations

Already enabled in this repo:
- ✅ Tensor parallelism (2 GPUs)
- ✅ FP4 quantization (Marlin backend)
- ✅ torch.compile (level 3)
- ✅ CUDA graphs
- ✅ Prefix caching
- ✅ Chunked prefill

See `OPTIMIZATION_REPORT.md` for details.

## 🆘 Support

If you encounter issues:
1. Check relevant documentation in `*.md` files
2. Verify GPU drivers and CUDA version
3. Review error logs in terminal
4. Test with smaller models first

## 🎉 Success!

You now have a complete benchmarking suite deployed!

**Quick test:**
```bash
./run_benchmark_dashboard.sh
# Open http://localhost:5000
# Click "Run Load Test"
# Get production recommendation in ~5 minutes
```

---

**Repository**: https://github.com/Gimel12/LLM-backend-benchmark.git
**Tested on**: NVIDIA RTX PRO 6000 Blackwell (2x 98GB)
**Performance**: 200 tok/s interactive, 875 tok/s batch ⭐⭐⭐⭐⭐
