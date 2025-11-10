#!/usr/bin/env python3
"""
Ollama Benchmark Script
Measures tokens per second for inference using Ollama
"""

import time
import argparse
import subprocess
import json
from typing import List, Tuple


def check_ollama_available() -> bool:
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def benchmark_ollama(
    model_name: str,
    prompts: List[str],
    max_tokens: int = 512,
    temperature: float = 0.8,
    top_p: float = 0.95,
) -> Tuple[float, int, float]:
    """
    Benchmark Ollama inference
    
    Args:
        model_name: Ollama model name (e.g., 'llama2:7b')
        prompts: List of prompts to generate
        max_tokens: Maximum tokens to generate per prompt
        temperature: Sampling temperature
        top_p: Top-p sampling parameter
        
    Returns:
        Tuple of (tokens_per_second, total_tokens, total_time)
    """
    print(f"\n{'='*60}")
    print(f"Ollama Benchmark")
    print(f"{'='*60}")
    print(f"Model: {model_name}")
    print(f"Number of prompts: {len(prompts)}")
    print(f"Max tokens per prompt: {max_tokens}")
    print(f"{'='*60}\n")
    
    if not check_ollama_available():
        raise RuntimeError("Ollama is not available. Please ensure it's installed and running.")
    
    # Check if model is available
    print("Checking if model is available...")
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
    )
    
    if model_name not in result.stdout:
        print(f"Model {model_name} not found. Pulling model...")
        pull_result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True,
        )
        if pull_result.returncode != 0:
            raise RuntimeError(f"Failed to pull model: {pull_result.stderr}")
        print(f"Model pulled successfully\n")
    else:
        print(f"Model {model_name} is available\n")
    
    # Warmup run
    print("Running warmup...")
    warmup_cmd = [
        "ollama", "run", model_name,
        "--verbose=false",
        prompts[0],
    ]
    subprocess.run(warmup_cmd, capture_output=True, text=True, timeout=120)
    print("Warmup complete\n")
    
    # Benchmark run
    print("Starting benchmark...")
    total_tokens = 0
    total_time = 0
    sample_output = ""
    
    for i, prompt in enumerate(prompts):
        print(f"Processing prompt {i+1}/{len(prompts)}...", end="\r")
        
        # Build the command with options
        cmd = [
            "ollama", "run", model_name,
            "--verbose=false",
        ]
        
        # Add the prompt
        full_prompt = f"{prompt}\n"
        
        start_time = time.time()
        result = subprocess.run(
            cmd,
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=300,
        )
        end_time = time.time()
        
        if result.returncode != 0:
            print(f"\nError processing prompt {i+1}: {result.stderr}")
            continue
        
        # Count tokens (approximate by splitting on whitespace)
        output_text = result.stdout.strip()
        tokens = len(output_text.split())
        total_tokens += tokens
        total_time += (end_time - start_time)
        
        if i == 0:
            sample_output = output_text
    
    print()  # New line after progress
    
    # Calculate metrics
    tokens_per_second = total_tokens / total_time if total_time > 0 else 0
    
    # Print results
    print(f"\n{'='*60}")
    print(f"Ollama Results")
    print(f"{'='*60}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Total tokens generated (approx): {total_tokens}")
    print(f"Tokens per second: {tokens_per_second:.2f}")
    print(f"Average tokens per prompt: {total_tokens / len(prompts):.2f}")
    print(f"{'='*60}\n")
    
    # Print sample output
    print(f"Sample output (first prompt):")
    print(f"{'-'*60}")
    print(f"Prompt: {prompts[0]}")
    print(f"Output: {sample_output[:500]}...")  # First 500 chars
    print(f"{'-'*60}\n")
    
    return tokens_per_second, total_tokens, total_time


def main():
    parser = argparse.ArgumentParser(description="Benchmark Ollama inference")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
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
        "--prompt",
        type=str,
        default="The future of artificial intelligence is",
        help="Base prompt to use (default: 'The future of artificial intelligence is')",
    )
    
    args = parser.parse_args()
    
    # Create multiple prompts
    prompts = [f"{args.prompt} {i+1}." for i in range(args.num_prompts)]
    
    # Run benchmark
    benchmark_ollama(
        model_name=args.model,
        prompts=prompts,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
    )


if __name__ == "__main__":
    main()
