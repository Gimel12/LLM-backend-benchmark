# LLM Benchmark: vLLM vs Ollama

This benchmark suite compares the performance of **vLLM** and **Ollama** for running large language models, specifically for the **gpt-oss:120b** model.

## System Requirements

- **GPUs**: 2x NVIDIA RTX PRO 6000 (98GB VRAM each)
- **CUDA**: 13.0
- **Python**: 3.10+
- **vLLM**: Installed via pip
- **Ollama**: Installed separately

## Installation

### vLLM
Already installed! If you need to reinstall:
```bash
pip3 install vllm
```

### Ollama
If not already installed:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Usage

### Individual Benchmarks

#### vLLM Benchmark
```bash
python3 vllm_benchmark.py \
    --model "your-huggingface-model-path" \
    --num-prompts 10 \
    --max-tokens 512 \
    --tensor-parallel-size 2
```

For gpt-oss:120b (if available on HuggingFace):
```bash
python3 vllm_benchmark.py \
    --model "gpt-oss/gpt-oss-120b" \
    --num-prompts 10 \
    --max-tokens 512 \
    --tensor-parallel-size 2
```

#### Ollama Benchmark
First, ensure the model is available:
```bash
ollama pull gpt-oss:120b
```

Then run the benchmark:
```bash
python3 ollama_benchmark.py \
    --model "gpt-oss:120b" \
    --num-prompts 10 \
    --max-tokens 512
```

### Comparison Benchmark

Run both benchmarks and compare:
```bash
python3 compare_benchmarks.py \
    --vllm-model "gpt-oss/gpt-oss-120b" \
    --ollama-model "gpt-oss:120b" \
    --num-prompts 10 \
    --max-tokens 512 \
    --tensor-parallel-size 2
```

Skip one if needed:
```bash
# Run only vLLM
python3 compare_benchmarks.py \
    --vllm-model "gpt-oss/gpt-oss-120b" \
    --skip-ollama

# Run only Ollama
python3 compare_benchmarks.py \
    --ollama-model "gpt-oss:120b" \
    --skip-vllm
```

## Arguments

### Common Arguments
- `--num-prompts`: Number of prompts to test (default: 10)
- `--max-tokens`: Maximum tokens to generate per prompt (default: 512)
- `--temperature`: Sampling temperature (default: 0.8)
- `--top-p`: Top-p sampling parameter (default: 0.95)
- `--prompt`: Base prompt text (default: "The future of artificial intelligence is")

### vLLM-Specific Arguments
- `--model`: HuggingFace model name or local path
- `--tensor-parallel-size`: Number of GPUs for tensor parallelism (default: 1)

### Ollama-Specific Arguments
- `--model`: Ollama model name (e.g., 'gpt-oss:120b')

## Expected Output

The benchmarks measure:
- **Tokens per second**: Primary performance metric
- **Total tokens generated**: Number of tokens produced
- **Total time**: Time taken for generation
- **Sample output**: Example generation from first prompt

The comparison script shows:
- Side-by-side metrics
- Speedup factor (vLLM vs Ollama)
- Performance winner

## Notes on gpt-oss:120b

### Model Size
The 120B parameter model requires significant VRAM:
- Typical requirement: ~240GB for FP16
- With quantization (INT8): ~120GB
- Your system has: 196GB total (2x98GB)

### Recommendations
1. **Use tensor parallelism** with vLLM (split across both GPUs)
2. **Enable quantization** if needed to fit in memory
3. **Monitor GPU memory** during benchmarks

### vLLM Advantages
- **Better memory efficiency** with PagedAttention
- **Continuous batching** for higher throughput
- **Tensor parallelism** for multi-GPU scaling
- **Optimized CUDA kernels**

### Ollama Advantages
- **Easier setup** and model management
- **Built-in model registry**
- **Simpler API**

## Troubleshooting

### vLLM Out of Memory
```bash
# Reduce GPU memory utilization
# Edit vllm_benchmark.py and change:
gpu_memory_utilization=0.90  # to 0.85 or lower
```

### Ollama Not Found
```bash
# Check if Ollama is running
ollama list

# Start Ollama if needed
ollama serve &
```

### Model Not Found
```bash
# For Ollama, pull the model first
ollama pull gpt-oss:120b

# For vLLM, verify the HuggingFace model name/path
```

## Performance Tips

1. **Warmup runs**: Both scripts include warmup to ensure fair benchmarks
2. **Consistent prompts**: Use the same prompts for both frameworks
3. **Multiple runs**: Run benchmarks multiple times for statistical significance
4. **Monitor GPUs**: Use `nvidia-smi` or `nvtop` to monitor GPU utilization

## Example Results Format

```
==========================================================
COMPARISON RESULTS
==========================================================

Metric                         vLLM            Ollama          Speedup   
----------------------------------------------------------------------
Tokens per Second              2500.50         1200.30         2.08x
Total Time (seconds)           25.60           53.40           2.09x
Total Tokens                   64000           64000           
==========================================================

🚀 vLLM is 2.08x FASTER than Ollama!
```

## License

MIT License - Feel free to modify and use as needed.
