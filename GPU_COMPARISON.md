# GPU Performance Comparison Guide

## Your Current Results

✅ **2 GPUs (Tensor Parallel)**: ~200 tokens/second

Now let's test with 1 GPU to see the difference!

---

## 🔄 How to Switch

### Step 1: Stop Current Server

In the terminal running vLLM (Terminal 1):
```bash
# Press Ctrl+C to stop the server
```

Wait for it to fully shut down (~5 seconds).

### Step 2: Start with 1 GPU

Same terminal:
```bash
./start_vllm_1gpu.sh
```

Wait for "Application startup complete" (~2-3 minutes since model is cached).

### Step 3: Test in Browser

Your web chat interface will automatically reconnect!
- Same URL: `http://SERVER-IP:8080/chat_remote.html`
- No changes needed
- Just refresh if needed

---

## 📊 Expected Results

| Configuration | Expected Speed | Your Results |
|--------------|----------------|--------------|
| **2 GPUs** (tensor parallel) | 150-250 tok/s | ✅ 200 tok/s |
| **1 GPU** (single) | 80-120 tok/s | ? |
| **Speedup** | ~1.8-2x | ? |

### Why the Difference?

**2 GPUs (Tensor Parallelism)**:
- Model is split across both GPUs
- Each GPU processes half the computation
- Communication overhead between GPUs
- Better for large models that don't fit on 1 GPU

**1 GPU**:
- Entire model on single GPU
- No inter-GPU communication
- Less overhead, but more sequential work
- Simpler but slower for this size model

---

## 🎯 Testing Procedure

1. **Current setup** (2 GPUs): Already tested = 200 tok/s ✅
2. **Stop server**: Ctrl+C in Terminal 1
3. **Start 1 GPU**: `./start_vllm_1gpu.sh`
4. **Test same prompt**: Chat interface still works!
5. **Compare speeds**: Note the tokens/sec difference

---

## 💡 What You'll Learn

### Performance per GPU
```
2 GPU speed: 200 tok/s
1 GPU speed: X tok/s
Per-GPU contribution: (200 - X) tok/s
```

### Scaling Efficiency
```
Theoretical 2x speedup: 200 tok/s
Actual speedup: (200 / X)x
Efficiency: (200 / (X * 2)) * 100%
```

---

## 🔧 Quick Commands

### Switch to 1 GPU
```bash
# Stop current (Ctrl+C), then:
./start_vllm_1gpu.sh
```

### Switch back to 2 GPUs
```bash
# Stop current (Ctrl+C), then:
./start_vllm_server.sh
```

### Check which GPUs are in use
```bash
# In another terminal
watch -n 1 nvidia-smi
```

Look for:
- **2 GPUs**: Both show high utilization and ~35GB memory used each
- **1 GPU**: Only GPU 0 shows usage, GPU 1 is idle

---

## 📈 Memory Usage Comparison

### 2 GPUs (Tensor Parallel)
```
GPU 0: ~35GB VRAM (half the model)
GPU 1: ~35GB VRAM (half the model)
Total: ~70GB across both
```

### 1 GPU
```
GPU 0: ~70GB VRAM (entire model)
GPU 1: 0GB (idle)
Total: ~70GB on one GPU
```

Your GPUs have 98GB each, so both configurations fit comfortably!

---

## 🎯 Real-World Implications

### When to Use 2 GPUs
- ✅ Maximum throughput needed
- ✅ Multiple concurrent users
- ✅ Model wouldn't fit on 1 GPU
- ✅ Batch processing

### When to Use 1 GPU
- ✅ Save power/cost
- ✅ Single user
- ✅ Model fits on 1 GPU
- ✅ Keep other GPU free for other tasks

---

## 📊 Track Your Results

```
Test 1 - 2 GPUs:
├─ Tokens/second: 200 ✅
├─ Response time: X seconds
└─ GPU utilization: Both GPUs ~80-90%

Test 2 - 1 GPU:
├─ Tokens/second: ___
├─ Response time: ___ seconds
└─ GPU utilization: GPU 0 ~80-90%, GPU 1 idle
```

---

## 🚀 Ready to Test!

```bash
# Terminal 1: Stop current server (Ctrl+C)
# Then run:
./start_vllm_1gpu.sh

# Terminal 2: Keep web server running
# (no changes needed)

# Your computer: Refresh browser or just keep chatting
# Watch the tokens/sec change!
```

The chat interface will show you the real difference in interactive performance!

---

## ⚡ Quick Comparison Test

Try this same prompt on both configurations:

**Prompt**: "Write a detailed explanation of how neural networks work, including forward propagation, backpropagation, and gradient descent."

This generates ~200-300 tokens, perfect for comparison:
- **2 GPUs**: ~1-1.5 seconds
- **1 GPU**: ~2-3 seconds (estimated)

---

## 🔄 After Testing

To switch back to 2 GPUs for maximum performance:
```bash
# Stop 1-GPU server (Ctrl+C)
./start_vllm_server.sh
```

Your web chat continues to work - just reconnects automatically!
