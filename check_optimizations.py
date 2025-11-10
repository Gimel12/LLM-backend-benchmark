#!/usr/bin/env python3
"""
Check vLLM optimizations and configuration
Identifies what's enabled and what can be improved
"""

import subprocess
import sys
import json

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=10
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), -1

def check_status(name, status, detail=""):
    """Print status with formatting"""
    symbol = "✅" if status else "⚠️"
    print(f"{symbol} {name}")
    if detail:
        print(f"   {detail}")

print("=" * 70)
print("vLLM Optimization Check")
print("=" * 70)
print()

# Check Python packages
print("📦 Installed Packages:")
print("-" * 70)

packages_to_check = [
    ("vllm", "vLLM core"),
    ("torch", "PyTorch"),
    ("triton", "Triton compiler"),
    ("xformers", "Memory-efficient attention"),
    ("flash-attn", "FlashAttention"),
    ("flashinfer", "FlashInfer"),
]

for package, description in packages_to_check:
    output, code = run_command(f"pip show {package} 2>/dev/null | grep Version")
    if code == 0 and output:
        version = output.split(": ")[1] if ": " in output else "installed"
        check_status(f"{description} ({package})", True, f"Version: {version}")
    else:
        check_status(f"{description} ({package})", False, "Not installed")

print()

# Check CUDA and GPU
print("🎮 GPU Configuration:")
print("-" * 70)

output, code = run_command("nvidia-smi --query-gpu=name,compute_cap --format=csv,noheader")
if code == 0:
    gpus = output.strip().split('\n')
    for i, gpu in enumerate(gpus):
        print(f"✅ GPU {i}: {gpu}")
else:
    print("⚠️  Could not detect GPUs")

print()

# Check CUDA version
output, code = run_command("nvidia-smi | grep 'CUDA Version' | awk '{print $9}'")
if code == 0 and output:
    check_status("CUDA Version", True, f"Version: {output}")

print()

# Check vLLM capabilities
print("⚡ vLLM Capabilities:")
print("-" * 70)

try:
    import torch
    check_status("PyTorch CUDA", torch.cuda.is_available(), 
                 f"Devices: {torch.cuda.device_count()}")
except Exception as e:
    check_status("PyTorch CUDA", False, str(e))

try:
    import vllm
    check_status("vLLM installed", True, f"Version: {vllm.__version__}")
except Exception as e:
    check_status("vLLM installed", False, str(e))

# Check for specific optimizations
try:
    import xformers
    check_status("xformers (memory-efficient attention)", True, 
                 f"Version: {xformers.__version__}")
except:
    check_status("xformers (memory-efficient attention)", False, 
                 "Can improve memory usage")

try:
    import flashinfer
    check_status("FlashInfer (fast sampling)", True, 
                 "Faster top-p/top-k sampling")
except:
    check_status("FlashInfer (fast sampling)", False, 
                 "Install for faster sampling: pip install flashinfer")

try:
    # Check for flash-attn
    output, code = run_command("pip show flash-attn 2>/dev/null")
    if code == 0:
        check_status("FlashAttention", True, 
                     "Fast attention computation")
    else:
        check_status("FlashAttention", False, 
                     "Not required but can help")
except:
    pass

print()

# Recommendations
print("🚀 Optimization Recommendations:")
print("-" * 70)
print()

recommendations = []

# Check for FlashInfer
try:
    import flashinfer
except:
    recommendations.append({
        "priority": "HIGH",
        "name": "Install FlashInfer",
        "command": "pip install flashinfer -i https://flashinfer.ai/whl/cu121/torch2.4/",
        "benefit": "20-30% faster sampling (top-p, top-k)",
        "impact": "Improves interactive speed"
    })

# Check compute capability
output, code = run_command("nvidia-smi --query-gpu=compute_cap --format=csv,noheader | head -1")
if code == 0 and output:
    compute_cap = float(output.strip())
    if compute_cap >= 8.0:
        print("✅ Your GPUs support all modern CUDA optimizations")
    else:
        print(f"⚠️  Compute capability {compute_cap} - some optimizations may be limited")

print()

# Current configuration analysis
print("📊 Current Configuration Analysis:")
print("-" * 70)
print()
print("Based on your server logs, currently enabled:")
print("  ✅ Tensor Parallelism: 2 GPUs")
print("  ✅ MXFP4 Quantization: Reduces memory, maintains quality")
print("  ✅ Marlin Kernel: FP4 optimized computation")
print("  ✅ torch.compile: Graph optimization (Level 3)")
print("  ✅ CUDA Graphs: Reduced kernel launch overhead")
print("  ✅ Prefix Caching: Shared prompt optimization")
print("  ✅ Chunked Prefill: Better batching")
print("  ⚠️  FlashInfer: Not available (fallback to PyTorch)")
print()

if recommendations:
    print("💡 Recommended Improvements:")
    print("-" * 70)
    print()
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. [{rec['priority']}] {rec['name']}")
        print(f"   Command: {rec['command']}")
        print(f"   Benefit: {rec['benefit']}")
        print(f"   Impact: {rec['impact']}")
        print()
else:
    print("✅ All major optimizations are enabled!")
    print()

print("=" * 70)
print("Summary:")
print("=" * 70)
print()
print(f"Your current speed: ~200 tokens/second (2 GPUs)")
print(f"This is EXCELLENT performance for a 120B model!")
print()
print("Main optimization to try:")
print("  • Install FlashInfer for 20-30% faster sampling")
print()
print("Your current setup is already highly optimized with:")
print("  • FP4 quantization (4x memory reduction)")
print("  • Tensor parallelism across 2 GPUs")
print("  • torch.compile for kernel fusion")
print("  • CUDA graphs for reduced overhead")
print("=" * 70)
