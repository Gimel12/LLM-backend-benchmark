#!/bin/bash
# Install FlashInfer for 20-30% faster sampling

echo "======================================"
echo "Installing FlashInfer"
echo "======================================"
echo ""
echo "This will improve sampling speed by 20-30%"
echo "(top-p, top-k operations)"
echo ""
echo "Your current speed: ~200 tok/s"
echo "After FlashInfer: ~240-260 tok/s (estimated)"
echo ""
echo "======================================"
echo ""

# Detect CUDA version
CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | awk '{print $9}' | cut -d. -f1,2 | tr -d .)

if [ -z "$CUDA_VERSION" ]; then
    echo "⚠️  Could not detect CUDA version"
    CUDA_VERSION="121"
    echo "Assuming CUDA 12.1"
fi

echo "Detected CUDA: $CUDA_VERSION"
echo ""

# Try to install FlashInfer
echo "Installing FlashInfer..."
echo ""

# For CUDA 12.1+ and PyTorch 2.4+
pip install flashinfer -i https://flashinfer.ai/whl/cu${CUDA_VERSION}/torch2.4/

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ FlashInfer installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Restart your vLLM server"
    echo "2. Look for: 'Using FlashInfer for sampling'"
    echo "3. Test your speed - should be ~20-30% faster!"
    echo ""
else
    echo ""
    echo "⚠️  Installation failed. Trying alternative..."
    echo ""
    
    # Try without specifying torch version
    pip install flashinfer
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ FlashInfer installed (alternative method)"
        echo ""
        echo "Next steps:"
        echo "1. Restart your vLLM server"
        echo "2. Test your speed!"
    else
        echo ""
        echo "❌ Could not install FlashInfer"
        echo ""
        echo "This is optional - your current setup is already excellent!"
        echo "FlashInfer would provide an additional 20-30% speedup."
    fi
fi

echo ""
echo "======================================"
