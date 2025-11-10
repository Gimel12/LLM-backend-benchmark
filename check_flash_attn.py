#!/usr/bin/env python3
"""
Check if FlashAttention is properly installed and being used
"""

print("=" * 70)
print("FlashAttention Detection")
print("=" * 70)
print()

# Check if flash_attn is installed
try:
    import flash_attn
    print(f"✅ flash-attn installed: version {flash_attn.__version__}")
except ImportError:
    print("❌ flash-attn NOT installed")
    exit(1)

print()

# Check if it's importable by vLLM
try:
    from flash_attn import flash_attn_func
    print("✅ FlashAttention functions are importable")
except ImportError as e:
    print(f"⚠️  Cannot import FlashAttention functions: {e}")

print()

# Check CUDA compatibility
try:
    import torch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"CUDA version: {torch.version.cuda}")
    
    if torch.cuda.is_available():
        compute_cap = torch.cuda.get_device_capability(0)
        print(f"GPU compute capability: {compute_cap[0]}.{compute_cap[1]}")
        
        if compute_cap[0] >= 8:
            print("✅ GPU supports FlashAttention-2")
        else:
            print("⚠️  GPU compute capability < 8.0 (FlashAttention-2 needs 8.0+)")
except Exception as e:
    print(f"Error checking CUDA: {e}")

print()
print("=" * 70)
print("Verdict")
print("=" * 70)
print()
print("FlashAttention is INSTALLED and should be available to vLLM.")
print()
print("However, vLLM may choose to use xformers instead if it's")
print("more optimal for your configuration.")
print()
print("To see which backend is actually used, you would need to")
print("check vLLM's internal logs or add debug logging.")
print()
print("=" * 70)
