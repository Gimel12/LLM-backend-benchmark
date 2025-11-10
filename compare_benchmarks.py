#!/usr/bin/env python3
"""
Comparison Script for vLLM vs Ollama
Runs both benchmarks and compares the results
"""

import argparse
import subprocess
import sys
import json
import re
from typing import Dict, Optional


def extract_metrics(output: str) -> Dict[str, float]:
    """Extract metrics from benchmark output"""
    metrics = {}
    
    # Extract tokens per second
    tps_match = re.search(r"Tokens per second:\s+([\d.]+)", output)
    if tps_match:
        metrics["tokens_per_second"] = float(tps_match.group(1))
    
    # Extract total tokens
    tokens_match = re.search(r"Total tokens generated.*?:\s+(\d+)", output)
    if tokens_match:
        metrics["total_tokens"] = int(tokens_match.group(1))
    
    # Extract total time
    time_match = re.search(r"Total time:\s+([\d.]+)", output)
    if time_match:
        metrics["total_time"] = float(time_match.group(1))
    
    return metrics


def run_vllm_benchmark(
    model: str,
    num_prompts: int,
    max_tokens: int,
    tensor_parallel_size: int,
    prompt: str,
) -> Optional[Dict[str, float]]:
    """Run vLLM benchmark and return metrics"""
    print(f"\n{'#'*60}")
    print(f"# Running vLLM Benchmark")
    print(f"{'#'*60}\n")
    
    cmd = [
        sys.executable,
        "vllm_benchmark.py",
        "--model", model,
        "--num-prompts", str(num_prompts),
        "--max-tokens", str(max_tokens),
        "--tensor-parallel-size", str(tensor_parallel_size),
        "--prompt", prompt,
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800,  # 30 minutes timeout
        )
        
        if result.returncode != 0:
            print(f"vLLM benchmark failed with error:")
            print(result.stderr)
            return None
        
        print(result.stdout)
        return extract_metrics(result.stdout)
    
    except subprocess.TimeoutExpired:
        print("vLLM benchmark timed out!")
        return None
    except Exception as e:
        print(f"Error running vLLM benchmark: {e}")
        return None


def run_ollama_benchmark(
    model: str,
    num_prompts: int,
    max_tokens: int,
    prompt: str,
) -> Optional[Dict[str, float]]:
    """Run Ollama benchmark and return metrics"""
    print(f"\n{'#'*60}")
    print(f"# Running Ollama Benchmark")
    print(f"{'#'*60}\n")
    
    cmd = [
        sys.executable,
        "ollama_benchmark.py",
        "--model", model,
        "--num-prompts", str(num_prompts),
        "--max-tokens", str(max_tokens),
        "--prompt", prompt,
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800,  # 30 minutes timeout
        )
        
        if result.returncode != 0:
            print(f"Ollama benchmark failed with error:")
            print(result.stderr)
            return None
        
        print(result.stdout)
        return extract_metrics(result.stdout)
    
    except subprocess.TimeoutExpired:
        print("Ollama benchmark timed out!")
        return None
    except Exception as e:
        print(f"Error running Ollama benchmark: {e}")
        return None


def print_comparison(vllm_metrics: Dict[str, float], ollama_metrics: Dict[str, float]):
    """Print comparison of both benchmarks"""
    print(f"\n{'='*60}")
    print(f"COMPARISON RESULTS")
    print(f"{'='*60}\n")
    
    print(f"{'Metric':<30} {'vLLM':<15} {'Ollama':<15} {'Speedup':<10}")
    print(f"{'-'*70}")
    
    if "tokens_per_second" in vllm_metrics and "tokens_per_second" in ollama_metrics:
        vllm_tps = vllm_metrics["tokens_per_second"]
        ollama_tps = ollama_metrics["tokens_per_second"]
        speedup = vllm_tps / ollama_tps if ollama_tps > 0 else 0
        print(f"{'Tokens per Second':<30} {vllm_tps:<15.2f} {ollama_tps:<15.2f} {speedup:<10.2f}x")
    
    if "total_time" in vllm_metrics and "total_time" in ollama_metrics:
        vllm_time = vllm_metrics["total_time"]
        ollama_time = ollama_metrics["total_time"]
        speedup = ollama_time / vllm_time if vllm_time > 0 else 0
        print(f"{'Total Time (seconds)':<30} {vllm_time:<15.2f} {ollama_time:<15.2f} {speedup:<10.2f}x")
    
    if "total_tokens" in vllm_metrics and "total_tokens" in ollama_metrics:
        vllm_tokens = vllm_metrics["total_tokens"]
        ollama_tokens = ollama_metrics["total_tokens"]
        print(f"{'Total Tokens':<30} {vllm_tokens:<15} {ollama_tokens:<15}")
    
    print(f"{'='*60}\n")
    
    # Summary
    if "tokens_per_second" in vllm_metrics and "tokens_per_second" in ollama_metrics:
        speedup = vllm_metrics["tokens_per_second"] / ollama_metrics["tokens_per_second"]
        if speedup > 1:
            print(f"🚀 vLLM is {speedup:.2f}x FASTER than Ollama!")
        elif speedup < 1:
            print(f"⚡ Ollama is {1/speedup:.2f}x FASTER than vLLM!")
        else:
            print(f"📊 Both frameworks have similar performance!")
    
    print()


def main():
    parser = argparse.ArgumentParser(description="Compare vLLM and Ollama performance")
    parser.add_argument(
        "--vllm-model",
        type=str,
        help="vLLM model name or path (HuggingFace format)",
    )
    parser.add_argument(
        "--ollama-model",
        type=str,
        help="Ollama model name (e.g., 'llama2:7b', 'gpt-oss:120b')",
    )
    parser.add_argument(
        "--num-prompts",
        type=int,
        default=10,
        help="Number of prompts to generate (default: 10)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Maximum tokens to generate per prompt (default: 512)",
    )
    parser.add_argument(
        "--tensor-parallel-size",
        type=int,
        default=2,
        help="Number of GPUs for vLLM tensor parallelism (default: 2)",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="The future of artificial intelligence is",
        help="Base prompt to use",
    )
    parser.add_argument(
        "--skip-vllm",
        action="store_true",
        help="Skip vLLM benchmark",
    )
    parser.add_argument(
        "--skip-ollama",
        action="store_true",
        help="Skip Ollama benchmark",
    )
    
    args = parser.parse_args()
    
    vllm_metrics = None
    ollama_metrics = None
    
    # Run vLLM benchmark
    if not args.skip_vllm:
        if not args.vllm_model:
            print("Error: --vllm-model is required when not skipping vLLM")
            sys.exit(1)
        
        vllm_metrics = run_vllm_benchmark(
            model=args.vllm_model,
            num_prompts=args.num_prompts,
            max_tokens=args.max_tokens,
            tensor_parallel_size=args.tensor_parallel_size,
            prompt=args.prompt,
        )
        
        if vllm_metrics is None:
            print("Failed to get vLLM metrics")
    
    # Run Ollama benchmark
    if not args.skip_ollama:
        if not args.ollama_model:
            print("Error: --ollama-model is required when not skipping Ollama")
            sys.exit(1)
        
        ollama_metrics = run_ollama_benchmark(
            model=args.ollama_model,
            num_prompts=args.num_prompts,
            max_tokens=args.max_tokens,
            prompt=args.prompt,
        )
        
        if ollama_metrics is None:
            print("Failed to get Ollama metrics")
    
    # Print comparison if both succeeded
    if vllm_metrics and ollama_metrics:
        print_comparison(vllm_metrics, ollama_metrics)
    elif vllm_metrics:
        print("\nOnly vLLM metrics available:")
        print(json.dumps(vllm_metrics, indent=2))
    elif ollama_metrics:
        print("\nOnly Ollama metrics available:")
        print(json.dumps(ollama_metrics, indent=2))
    else:
        print("\nNo metrics available from either benchmark")
        sys.exit(1)


if __name__ == "__main__":
    main()
