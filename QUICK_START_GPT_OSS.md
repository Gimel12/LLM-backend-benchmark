# Quick Start: GPT-OSS-120B Benchmark

## Model Information
- **Name**: `openai/gpt-oss-120b`
- **Size**: 120B parameters
- **HuggingFace**: https://huggingface.co/openai/gpt-oss-120b
- **Paper**: arXiv:2508.10925

## Your System
- **GPUs**: 2x NVIDIA RTX PRO 6000 (98GB each = 196GB total)
- **vLLM**: 0.11.0 ✅ Installed
- **CUDA**: 13.0 ✅ Ready
- **Ollama**: Installed ✅

## Fastest Way to Start

### Option 1: Interactive Script (Easiest)
```bash
cd /home/bizon/CascadeProjects/llm-benchmark
./run_gpt_oss_120b.sh
```

This will guide you through the benchmark options.

### Option 2: Direct Commands

#### vLLM Benchmark (Uses Both GPUs)
```bash
python3 vllm_benchmark.py \
    --model "openai/gpt-oss-120b" \
    --num-prompts 10 \
    --max-tokens 512 \
    --tensor-parallel-size 2
```

#### Ollama Benchmark
```bash
# First time only - pull the model
ollama pull gpt-oss:120b

# Run benchmark
python3 ollama_benchmark.py \
    --model "gpt-oss:120b" \
    --num-prompts 10 \
    --max-tokens 512
```

#### Compare Both
```bash
python3 compare_benchmarks.py \
    --vllm-model "openai/gpt-oss-120b" \
    --ollama-model "gpt-oss:120b" \
    --num-prompts 10 \
    --max-tokens 512 \
    --tensor-parallel-size 2
```

## What to Expect

### First Run
- **vLLM**: Will download model from HuggingFace (~240GB)
- **Ollama**: Will download optimized model (~70GB with quantization)
- **Time**: 15-45 minutes depending on your internet speed

### Performance Estimates
- **vLLM**: 50-150 tokens/second (with 2 GPUs + tensor parallelism)
- **Ollama**: 20-80 tokens/second
- **Expected Speedup**: 2-3x faster with vLLM

### Memory Usage
- **vLLM**: Uses both GPUs, ~80-90GB per GPU
- **Ollama**: Uses 1 GPU, ~70-90GB

## Custom Prompts

Test with your own prompts:
```bash
python3 vllm_benchmark.py \
    --model "openai/gpt-oss-120b" \
    --tensor-parallel-size 2 \
    --prompt "Write a detailed explanation of machine learning" \
    --num-prompts 5 \
    --max-tokens 1024
```

## Advanced Options

### Adjust GPU Memory
If you get OOM errors, edit `vllm_benchmark.py` line 49:
```python
gpu_memory_utilization=0.90,  # Try 0.85 or 0.80
```

### More Prompts for Statistical Significance
```bash
python3 compare_benchmarks.py \
    --vllm-model "openai/gpt-oss-120b" \
    --ollama-model "gpt-oss:120b" \
    --num-prompts 50 \
    --tensor-parallel-size 2
```

### Longer Outputs
```bash
python3 vllm_benchmark.py \
    --model "openai/gpt-oss-120b" \
    --max-tokens 2048 \
    --tensor-parallel-size 2
```

## Monitoring

Watch GPU usage during benchmark:
```bash
# Terminal 1: Run benchmark
./run_gpt_oss_120b.sh

# Terminal 2: Monitor GPUs
watch -n 1 nvidia-smi
```

## Troubleshooting

### Out of Memory
1. Reduce `gpu_memory_utilization` in `vllm_benchmark.py`
2. Use smaller `--max-tokens`
3. Reduce `--num-prompts`

### Model Download Fails
```bash
# Check your HuggingFace token
huggingface-cli whoami

# Login if needed
huggingface-cli login
```

### Slow Performance
1. Check GPU temperature (thermal throttling)
2. Close other GPU applications
3. Ensure both GPUs are being used (check nvidia-smi)

## Special vLLM Version (Optional)

OpenAI recommends a special vLLM version for gpt-oss, but your standard vLLM 0.11.0 should work fine. If you want to try the optimized version:

```bash
# WARNING: This will replace your current vLLM
pip install --pre vllm==0.10.1+gptoss \
    --extra-index-url https://wheels.vllm.ai/gpt-oss/ \
    --extra-index-url https://download.pytorch.org/whl/nightly/cu128 \
    --index-strategy unsafe-best-match
```

## Results Format

The benchmark outputs:
- ✅ Tokens per second (primary metric)
- ✅ Total generation time
- ✅ Total tokens generated
- ✅ Sample output
- ✅ Speedup comparison (when using compare script)

Example output:
```
==========================================================
COMPARISON RESULTS
==========================================================

Metric                         vLLM            Ollama          Speedup   
----------------------------------------------------------------------
Tokens per Second              127.45          48.32           2.64x
Total Time (seconds)           50.23           132.67          2.64x
Total Tokens                   6400            6400           
==========================================================

🚀 vLLM is 2.64x FASTER than Ollama!
```

## Next Steps After Benchmarking

1. **Save results** to a file for comparison
2. **Test different prompt types** (code, reasoning, creative writing)
3. **Experiment with batch sizes** for production use
4. **Try different reasoning levels** (Low, Medium, High)

---

Ready to start? Run:
```bash
./run_gpt_oss_120b.sh
```
