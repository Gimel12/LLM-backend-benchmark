># vLLM vs Ollama - Production Load Testing

Beautiful web dashboard to compare vLLM and Ollama performance under load and decide which backend to use for production.

## 🎯 What This Does

- ✅ Tests both vLLM and Ollama with the same prompt
- ✅ Simulates 1, 2, 5, 10, and 20 concurrent users
- ✅ Measures throughput (tokens/second)
- ✅ Tracks latency (avg, p95, p99)
- ✅ Shows when each backend starts to slow down
- ✅ Gives clear recommendation for production

## 🚀 Quick Start

### Prerequisites

**Terminal 1 - Start vLLM:**
```bash
./start_vllm_server.sh
```

**Terminal 2 - Start Ollama:**
```bash
ollama serve
```

**Terminal 3 - Start Dashboard:**
```bash
./run_benchmark_dashboard.sh
```

### Access Dashboard

Open in your browser:
```
http://localhost:5000
```

Or from another computer:
```
http://192.168.1.XXX:5000
```

## 📊 Using the Dashboard

### 1. Check Server Status
Top of dashboard shows:
- 🟢 Green dot = Server running
- 🔴 Red dot = Server offline

### 2. Customize Test (Optional)
- **Test Prompt**: Default is about American Revolution
- You can change it to any prompt you want

### 3. Run Test
Click "🔬 Run Load Test"

The test will:
1. Test with 1 concurrent user
2. Test with 2 concurrent users
3. Test with 5 concurrent users
4. Test with 10 concurrent users
5. Test with 20 concurrent users

Takes about 5-10 minutes total.

### 4. View Results

**Charts shown:**
- 📊 **Throughput**: Total tokens/second at each load level
- ⏱️ **Average Latency**: How long users wait
- 📈 **P95 Latency**: 95th percentile (most users)
- ✅ **Success Rate**: % of requests that complete

**Production Recommendation:**
- Clear winner displayed
- Speedup factor shown
- Scalability analysis

## 📈 Interpreting Results

### Throughput (Tokens/Second)
```
Higher = Better
Flat line as users increase = Good scalability
Dropping line = System overloaded
```

### Latency (Seconds)
```
Lower = Better
Stable line = Consistent performance
Rising line = System under stress
```

### Success Rate
```
100% = Perfect
<100% = Some requests failing
```

## 🎯 Production Decision Guide

### Choose vLLM If:
- ✅ Higher throughput across all load levels
- ✅ Lower latency at high concurrency
- ✅ You expect multiple concurrent users
- ✅ You want maximum performance

### Choose Ollama If:
- ✅ Better single-user performance
- ✅ Simpler setup matters
- ✅ You have mostly sequential requests
- ✅ Resource efficiency is priority

## 📊 Example Results

### Scenario 1: vLLM Wins
```
Single User:
  vLLM: 200 tok/s
  Ollama: 150 tok/s

20 Users:
  vLLM: 850 tok/s (4.25 tok/s per user)
  Ollama: 500 tok/s (2.5 tok/s per user)

Recommendation: vLLM for production ✅
```

### Scenario 2: Ollama Wins
```
Single User:
  vLLM: 180 tok/s
  Ollama: 220 tok/s

20 Users:
  vLLM: 600 tok/s
  Ollama: 800 tok/s

Recommendation: Ollama for production ✅
```

## 🔧 Advanced Usage

### Custom User Counts

Edit `benchmark_server.py`:
```python
user_counts = data.get('user_counts', [1, 5, 10, 20, 50, 100])
```

### Different Prompts

Use the text area in the dashboard to test different types of prompts:
- Short responses (tweets, summaries)
- Long responses (essays, articles)
- Code generation
- Reasoning tasks

### Monitor During Test

Watch your GPUs:
```bash
watch -n 1 nvidia-smi
```

## 🐛 Troubleshooting

### Dashboard Won't Start
```bash
# Install dependencies
pip install flask flask-cors aiohttp
```

### Server Not Detected
```bash
# Check vLLM
curl http://localhost:8000/v1/models

# Check Ollama  
curl http://localhost:11434/api/tags
```

### Test Takes Too Long
- Reduce user counts in code
- Use shorter prompt
- Reduce max_tokens (default 500)

### Out of Memory
- Reduce concurrent users
- Run tests sequentially instead of simultaneously

## 📝 Understanding the Test

### What Gets Tested

**For Each Backend:**
1. Warm up with 1 request
2. Test N concurrent users
3. All users send same prompt
4. Measure:
   - Time to complete
   - Tokens generated
   - Success/failure
   - Latency distribution

**Metrics Calculated:**
- Throughput = Total tokens / Total time
- Avg Latency = Mean response time
- P95 Latency = 95% of requests complete by this time
- Success Rate = % of successful requests

### Why This Matters

**Production Considerations:**
- Peak load capacity
- Response time under load
- Failure points
- Cost per request
- Resource utilization

## 🎯 Real-World Scenarios

### Low Traffic Site (1-5 concurrent users)
- Both backends perform well
- Choose based on simplicity/preference

### Medium Traffic (10-20 concurrent users)
- Performance differences visible
- Choose backend with better scaling

### High Traffic (50+ concurrent users)
- Critical to choose right backend
- May need multiple instances
- Load balancing recommended

## 📊 Export Results

Results are displayed visually. To save:
1. Take screenshot of charts
2. Note recommendation
3. Save for documentation

## 🔄 Re-running Tests

- Click "Run Load Test" again anytime
- Tests are independent
- Previous results are replaced

## 💡 Tips

1. **Run multiple times** - Average results over 3+ runs
2. **Test peak hours** - When both servers are fresh
3. **Test different prompts** - Your actual use case
4. **Monitor resources** - GPU, CPU, memory usage
5. **Document results** - Keep for future reference

## ✨ Features

- 🎨 **Beautiful UI** - Clean, modern design
- 📊 **Real-time charts** - Using Chart.js
- 🔄 **Automatic testing** - Just click and wait
- 🎯 **Clear recommendation** - No guessing
- 📱 **Responsive** - Works on any device
- 🌐 **Network accessible** - Test from any computer

---

**Built with:**
- Flask (Python web framework)
- Chart.js (Beautiful charts)
- aiohttp (Async HTTP requests)
- Love ❤️

**Your 200 tok/s with vLLM is already world-class!** 🚀
