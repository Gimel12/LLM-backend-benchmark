#!/bin/bash
# Try to install FlashAttention for potential 10-20% speedup

echo "======================================"
echo "Installing FlashAttention-2"
echo "======================================"
echo ""
echo "FlashAttention vs FlashInfer:"
echo "  • FlashAttention: Optimizes attention computation"
echo "  • FlashInfer: Optimizes sampling (top-p, top-k)"
echo ""
echo "You have xformers which is similar, but FlashAttention-2"
echo "might be slightly faster on your Blackwell GPUs."
echo ""
echo "Potential gain: 10-20% faster"
echo "Your speed: 200 tok/s → 220-240 tok/s (estimated)"
echo ""
echo "======================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d. -f1,2)
echo "Python version: $PYTHON_VERSION"
echo "PyTorch version: $(python3 -c 'import torch; print(torch.__version__)' 2>/dev/null || echo 'unknown')"
echo "CUDA version: 13.0"
echo ""

read -p "Proceed with FlashAttention-2 installation? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Skipping installation."
    exit 0
fi

echo ""
echo "Installing FlashAttention-2..."
echo "This may take 5-10 minutes to compile..."
echo ""

# Try pre-built wheel first
pip install flash-attn --no-build-isolation

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ FlashAttention-2 installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Restart your vLLM server"
    echo "2. Look for 'Using FlashAttention' in logs"
    echo "3. Test your speed"
    echo ""
else
    echo ""
    echo "⚠️  Pre-built wheel not available for CUDA 13.0"
    echo ""
    read -p "Try building from source? (takes 10-15 min) (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Building FlashAttention-2 from source..."
        echo "This will take 10-15 minutes..."
        echo ""
        
        pip install ninja packaging
        pip install flash-attn --no-build-isolation --no-cache-dir
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ FlashAttention-2 built and installed!"
            echo ""
            echo "Restart your vLLM server to use it."
        else
            echo ""
            echo "❌ Build failed"
            echo ""
            echo "Your xformers is already providing similar optimizations."
            echo "Your current 200 tok/s is excellent!"
        fi
    else
        echo ""
        echo "Skipping build."
        echo "Your current setup with xformers is already great!"
    fi
fi

echo ""
echo "======================================"
