#!/bin/bash
# Advanced: Build FlashInfer from source for CUDA 13.0
# WARNING: This is complex and may not work. Your current setup is already excellent!

echo "======================================"
echo "Build FlashInfer from Source (CUDA 13.0)"
echo "======================================"
echo ""
echo "⚠️  WARNING: This is advanced and may take 20-30 minutes"
echo "⚠️  Your current 200 tok/s is already excellent!"
echo "⚠️  This might only give 10-20 tok/s improvement at best"
echo ""
read -p "Are you sure you want to proceed? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Skipping. Your setup is already great!"
    exit 0
fi

echo ""
echo "Installing build dependencies..."
echo ""

# Install build tools
pip install ninja packaging

# Clone FlashInfer
echo "Cloning FlashInfer repository..."
cd /tmp
rm -rf flashinfer
git clone https://github.com/flashinfer-ai/flashinfer.git
cd flashinfer

echo ""
echo "Building FlashInfer for CUDA 13.0..."
echo "This will take 10-20 minutes..."
echo ""

# Build and install
pip install -e . --no-build-isolation

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ FlashInfer built successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Restart your vLLM server"
    echo "2. Test your speed"
    echo ""
else
    echo ""
    echo "❌ Build failed"
    echo ""
    echo "This is expected - FlashInfer may not support CUDA 13.0 yet."
    echo "Your current setup with PyTorch-native sampling is already excellent!"
    echo ""
fi

cd -
