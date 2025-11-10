# vLLM Installation & Benchmark Setup - Complete ✅

## Installation Status

### ✅ vLLM Installed
- **Version**: 0.11.0
- **Python**: 3.10.13
- **PyTorch**: 2.8.0+cu128
- **CUDA**: 13.0

### ✅ GPU Configuration
- **GPUs**: 2x NVIDIA RTX PRO 6000 Blackwell Server Edition
- **VRAM per GPU**: 98GB (97.2GB free)
- **Total VRAM**: 196GB
- **Status**: Both GPUs available and ready

### ✅ Ollama Status
- **Installed**: Yes
- **Models**: None currently pulled (ready to install)

## What Was Created

### Benchmark Scripts
1. **`vllm_benchmark.py`** - Standalone vLLM benchmark
2. **`ollama_benchmark.py`** - Standalone Ollama benchmark
3. **`compare_benchmarks.py`** - Side-by-side comparison

### Helper Scripts
4. **`quick_test.sh`** - Verify installation and system status
5. **`example_test.sh`** - Test with small model before running 120B
6. **`README.md`** - Complete usage documentation

## Quick Start Guide

### Step 1: Verify Installation
```bash
cd /home/bizon/CascadeProjects/llm-benchmark
./quick_test.sh
```

### Step 2: Test with Small Model (Recommended)
```bash
./example_test.sh
```
This downloads and tests with `facebook/opt-125m` (~125M parameters) to verify everything works.

### Step 3: Run gpt-oss:120b Benchmark

#### Option A: Ollama Only
```bash
# Pull the model (this may take a while)
ollama pull gpt-oss:120b

# Run benchmark
python3 ollama_benchmark.py --model gpt-oss:120b --num-prompts 10
```

#### Option B: vLLM Only
You need to know the HuggingFace path for gpt-oss:120b. Common possibilities:
- `gpt-oss/gpt-oss-120b`
- Local path if you downloaded it

```bash
python3 vllm_benchmark.py \
    --model "gpt-oss/gpt-oss-120b" \
    --num-prompts 10 \
    --tensor-parallel-size 2
```

#### Option C: Compare Both
```bash
python3 compare_benchmarks.py \
    --vllm-model "gpt-oss/gpt-oss-120b" \
    --ollama-model "gpt-oss:120b" \
    --num-prompts 10 \
    --tensor-parallel-size 2
```

## Key Features

### vLLM Advantages
- ✅ **Tensor Parallelism**: Uses both GPUs automatically
- ✅ **PagedAttention**: More memory efficient
- ✅ **Continuous Batching**: Better throughput
- ✅ **Optimized Kernels**: Faster inference

### Benchmark Capabilities
- 📊 Tokens per second measurement
- ⏱️ Total inference time tracking
- 📝 Sample output display
- 🔄 Warmup runs for fair comparison
- 📈 Side-by-side comparison charts

## Memory Considerations

### gpt-oss:120b Requirements
- **FP16 (full precision)**: ~240GB VRAM
- **INT8 (quantized)**: ~120GB VRAM
- **Your available**: 196GB VRAM

### Recommendations
1. **Use tensor parallelism** (`--tensor-parallel-size 2`)
2. **Monitor memory** with `nvidia-smi` during runs
3. **Consider quantization** if OOM errors occur

## Troubleshooting

### Out of Memory?
Edit `vllm_benchmark.py` line 49:
```python
gpu_memory_utilization=0.90,  # Change to 0.85 or 0.80
```

### Model Not Found?
For vLLM, verify the HuggingFace model path:
```bash
# Search on HuggingFace
# https://huggingface.co/models?search=gpt-oss
```

For Ollama:
```bash
# Check available models
ollama list

# Search for models
ollama search gpt-oss
```

### Performance Tips
1. **Close other GPU applications** before benchmarking
2. **Run multiple times** for statistical significance
3. **Use consistent settings** when comparing
4. **Monitor GPU temps** to avoid thermal throttling

## Expected Performance

### Typical Results (estimates for 120B model)
- **vLLM**: 50-150 tokens/second (with 2 GPUs)
- **Ollama**: 20-80 tokens/second (single GPU)
- **Speedup**: 2-3x faster with vLLM

*Actual results depend on model architecture, quantization, and batch size*

## Monitoring Commands

```bash
# Watch GPU usage in real-time
watch -n 1 nvidia-smi

# Or use nvtop (if installed)
nvtop

# Check vLLM version
python3 -c "import vllm; print(vllm.__version__)"

# List Ollama models
ollama list
```

## Next Steps

1. ✅ **Installation Complete** - vLLM is ready
2. 🔄 **Pull gpt-oss:120b** - Run `ollama pull gpt-oss:120b`
3. 🧪 **Test Small Model** - Run `./example_test.sh`
4. 🚀 **Benchmark 120B** - Use scripts above
5. 📊 **Compare Results** - Analyze performance

## Support

- **vLLM Docs**: https://docs.vllm.ai
- **vLLM GitHub**: https://github.com/vllm-project/vllm
- **Ollama Docs**: https://ollama.com/docs

---

**Setup completed**: November 10, 2025, 4:07 PM UTC-05:00
**Workspace**: `/home/bizon/CascadeProjects/llm-benchmark`
