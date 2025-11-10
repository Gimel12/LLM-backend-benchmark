# Testing FlashAttention Performance

You've installed FlashAttention-2! Now let's see if it improves your speed.

## 🎯 Quick Test (Recommended)

### Step 1: Restart Server
```bash
# Terminal 1: Stop current server (Ctrl+C)
# Then restart:
./start_vllm_server.sh
```

**Wait for**: "Application startup complete" (~2-3 minutes)

### Step 2: Check Logs
Look for one of these in the startup logs:
```
✅ "Using FlashAttention-2 backend"
✅ "flash_attn" 
✅ No warning about "FlashAttention is not available"
```

### Step 3: Run Automated Test
```bash
# Terminal 2 or 3:
python3 test_flash_attention.py
```

This will:
- Run 3 test generations
- Calculate average speed
- Compare with your baseline (200 tok/s)
- Show percentage improvement

---

## 📊 Manual Test (Alternative)

### Option 1: Web Interface
1. Open your chat interface in browser
2. Send this prompt:
   ```
   Explain how neural networks learn through backpropagation in detail.
   ```
3. Note the tokens/second shown
4. Compare with your previous 200 tok/s

### Option 2: Use Benchmark Script
```bash
python3 vllm_benchmark.py \
    --model "openai/gpt-oss-120b" \
    --num-prompts 10 \
    --max-tokens 200 \
    --tensor-parallel-size 2
```

Compare the tokens/second with your previous 875 tok/s batch result.

---

## 📈 What to Expect

### Best Case: +10-15% faster
```
Before: 200 tok/s
After:  220-230 tok/s
Improvement: ✅ Noticeable speedup!
```

### Likely Case: +5-10% faster
```
Before: 200 tok/s
After:  210-220 tok/s
Improvement: ✅ Small but measurable
```

### Realistic Case: +2-5% faster
```
Before: 200 tok/s
After:  204-210 tok/s
Improvement: 📊 Minor improvement
```

### No Change: 0% difference
```
Before: 200 tok/s
After:  200 tok/s
Reason: xformers was already very efficient
```

---

## 🔍 Verify FlashAttention is Active

### Check Server Logs
```bash
# Look in your server terminal for:
grep -i "flash" 

# Should see something like:
# "Using FlashAttention-2 backend"
# "flash_attn version: 2.8.3"
```

### Check Python
```bash
python3 -c "import flash_attn; print('FlashAttention version:', flash_attn.__version__)"
```

Should output: `FlashAttention version: 2.8.3`

---

## 📊 Understanding Results

### If Speed Increased
```
+10-15%: Excellent! FlashAttention is helping significantly
+5-10%:  Good! Moderate improvement
+2-5%:   Okay! Small but measurable gain
```

### If Speed Same or Lower
This can happen because:
1. **xformers was already excellent** - already doing most optimizations
2. **Attention isn't the bottleneck** - other parts of model are slower
3. **Warmup needed** - first few runs may be slower
4. **Background processes** - GPU busy with other tasks

**Don't worry!** Your 200 tok/s is already world-class.

---

## 🎯 Side-by-Side Comparison

### Run Both Tests

**Before FlashAttention** (if you saved old server):
```bash
# Use old vLLM without FlashAttention
# Your baseline: 200 tok/s
```

**After FlashAttention**:
```bash
# New vLLM with FlashAttention
python3 test_flash_attention.py
```

### Test Conditions
For fair comparison, use:
- ✅ Same prompt
- ✅ Same max_tokens (200)
- ✅ Same temperature (0.8)
- ✅ Same number of runs (3-5)
- ✅ No other GPU processes running

---

## 🚀 Quick Commands Summary

```bash
# 1. Restart server with FlashAttention
./start_vllm_server.sh

# 2. Wait for startup (~2-3 min)

# 3. Test speed
python3 test_flash_attention.py

# 4. Or use web interface
# Just chat and note the tok/s
```

---

## 📈 Results Tracking

Fill in your results:

```
Configuration: 2x RTX PRO 6000, Tensor Parallel

Before FlashAttention:
├─ Speed: 200 tok/s ✅
├─ Backend: xformers
└─ Batch: 875 tok/s

After FlashAttention:
├─ Speed: ___ tok/s
├─ Backend: flash-attn-2
└─ Batch: ___ tok/s

Improvement: ___% 
```

---

## 💡 Tips

### For Accurate Testing
1. **Warm up the model** - First request is slower
2. **Run multiple tests** - Average the results
3. **Use same prompts** - For fair comparison
4. **Check GPU load** - Ensure nothing else is using GPU

### For Maximum Speed
1. ✅ FlashAttention installed
2. ✅ 2 GPUs (tensor parallel)
3. ✅ torch.compile enabled
4. ✅ CUDA graphs captured
5. ✅ Good cooling (check temps)

### Monitor GPUs
```bash
# Terminal 3:
watch -n 1 nvidia-smi
```

Look for:
- Both GPUs at ~80-90% utilization
- Temperature under 85°C
- Power near 600W per GPU (under load)

---

## 🎯 Next Steps

After testing:

**If speed improved:**
- ✅ Great! Keep FlashAttention
- 📊 Document your improvement
- 🚀 Enjoy faster inference!

**If speed same:**
- ✅ Still okay! Your setup is already optimal
- 📊 xformers was already doing great
- 🤷 FlashAttention is a minor refinement

**Either way, your 200+ tok/s is excellent!** 🌟
