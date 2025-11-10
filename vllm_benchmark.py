#!/usr/bin/env python3
"""
vLLM Benchmark Script
Measures tokens per second for inference using vLLM
"""

import time
import argparse
from typing import List, Tuple
from vllm import LLM, SamplingParams


def benchmark_vllm(
    model_name: str,
    prompts: List[str],
    max_tokens: int = 512,
    temperature: float = 0.8,
    top_p: float = 0.95,
    tensor_parallel_size: int = 1,
) -> Tuple[float, int, float]:
    """
    Benchmark vLLM inference
    
    Args:
        model_name: HuggingFace model name or local path
        prompts: List of prompts to generate
        max_tokens: Maximum tokens to generate per prompt
        temperature: Sampling temperature
        top_p: Top-p sampling parameter
        tensor_parallel_size: Number of GPUs for tensor parallelism
        
    Returns:
        Tuple of (tokens_per_second, total_tokens, total_time)
    """
    print(f"\n{'='*60}")
    print(f"vLLM Benchmark")
    print(f"{'='*60}")
    print(f"Model: {model_name}")
    print(f"Tensor Parallel Size: {tensor_parallel_size}")
    print(f"Number of prompts: {len(prompts)}")
    print(f"Max tokens per prompt: {max_tokens}")
    print(f"{'='*60}\n")
    
    # Initialize LLM
    print("Loading model...")
    load_start = time.time()
    llm = LLM(
        model=model_name,
        tensor_parallel_size=tensor_parallel_size,
        trust_remote_code=True,
        gpu_memory_utilization=0.90,
    )
    load_time = time.time() - load_start
    print(f"Model loaded in {load_time:.2f} seconds\n")
    
    # Set up sampling parameters
    sampling_params = SamplingParams(
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    
    # Warmup run
    print("Running warmup...")
    _ = llm.generate([prompts[0]], sampling_params)
    print("Warmup complete\n")
    
    # Benchmark run
    print("Starting benchmark...")
    start_time = time.time()
    outputs = llm.generate(prompts, sampling_params)
    end_time = time.time()
    
    # Calculate metrics
    total_time = end_time - start_time
    total_tokens = sum(len(output.outputs[0].token_ids) for output in outputs)
    tokens_per_second = total_tokens / total_time
    
    # Print results
    print(f"\n{'='*60}")
    print(f"vLLM Results")
    print(f"{'='*60}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Total tokens generated: {total_tokens}")
    print(f"Tokens per second: {tokens_per_second:.2f}")
    print(f"Average tokens per prompt: {total_tokens / len(prompts):.2f}")
    print(f"{'='*60}\n")
    
    # Print sample outputs
    print(f"Sample output (first prompt):")
    print(f"{'-'*60}")
    print(f"Prompt: {prompts[0]}")
    print(f"Output: {outputs[0].outputs[0].text}")
    print(f"{'-'*60}\n")
    
    return tokens_per_second, total_tokens, total_time


def main():
    parser = argparse.ArgumentParser(description="Benchmark vLLM inference")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model name or path (e.g., 'meta-llama/Llama-2-7b-hf')",
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
        "--temperature",
        type=float,
        default=0.8,
        help="Sampling temperature (default: 0.8)",
    )
    parser.add_argument(
        "--top-p",
        type=float,
        default=0.95,
        help="Top-p sampling parameter (default: 0.95)",
    )
    parser.add_argument(
        "--tensor-parallel-size",
        type=int,
        default=1,
        help="Number of GPUs for tensor parallelism (default: 1)",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="The future of artificial intelligence is",
        help="Base prompt to use (default: 'The future of artificial intelligence is')",
    )
    
    args = parser.parse_args()
    
    # Create multiple prompts
    prompts = [f"{args.prompt} {i+1}." for i in range(args.num_prompts)]
    
    # Run benchmark
    benchmark_vllm(
        model_name=args.model,
        prompts=prompts,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        tensor_parallel_size=args.tensor_parallel_size,
    )


if __name__ == "__main__":
    main()
