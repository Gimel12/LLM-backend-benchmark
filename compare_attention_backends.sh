#!/bin/bash
# Compare xformers vs FlashAttention performance

echo "======================================"
echo "Attention Backend Comparison"
echo "======================================"
echo ""
echo "Current test showed FlashAttention slower (124 tok/s vs 200 tok/s)"
echo ""
echo "This could be because:"
echo "  1. Short test responses (~117 tokens)"
echo "  2. Blackwell GPU (compute 12.0) not fully optimized yet"
echo "  3. xformers is already excellent for your setup"
echo ""
echo "======================================"
echo "Recommendation"
echo "======================================"
echo ""
echo "Option 1: Uninstall FlashAttention (go back to xformers)"
echo "  -> Your original 200 tok/s was excellent"
echo "  -> xformers is proven to work great on your hardware"
echo ""
echo "Option 2: Test more with your web chat interface"
echo "  -> Try longer prompts (500+ tokens)"
echo "  -> See if speed improves with longer generations"
echo ""
read -p "Choose: [1] Uninstall FlashAttention  [2] Keep testing  [3] Exit: " choice

case $choice in
    1)
        echo ""
        echo "Uninstalling FlashAttention..."
        pip uninstall flash-attn -y
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ FlashAttention uninstalled"
            echo ""
            echo "Restart your vLLM server to use xformers again:"
            echo "  1. Stop server (Ctrl+C)"
            echo "  2. Run: ./start_vllm_server.sh"
            echo ""
            echo "You should get back to your original 200 tok/s!"
        else
            echo "❌ Uninstall failed"
        fi
        ;;
    2)
        echo ""
        echo "Keep testing with FlashAttention:"
        echo ""
        echo "1. Open your web chat interface"
        echo "2. Try this prompt (generates more tokens):"
        echo ""
        echo "   'Write a comprehensive guide on machine learning"
        echo "    algorithms, covering supervised, unsupervised, and"
        echo "    reinforcement learning with detailed examples.'"
        echo ""
        echo "3. Compare the tok/s with your original 200 tok/s"
        echo ""
        echo "If it's still slower, run this script again and choose option 1."
        ;;
    3)
        echo "Exiting..."
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

echo ""
echo "======================================"
