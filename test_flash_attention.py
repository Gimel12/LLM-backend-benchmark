#!/usr/bin/env python3
"""
Quick test to measure FlashAttention performance improvement
Run after restarting server with FlashAttention installed
"""

import time
import requests
import sys

SERVER_URL = "http://localhost:8000/v1"
MODEL_NAME = "openai/gpt-oss-120b"

# Test prompt (generates ~150-200 tokens)
TEST_PROMPT = "Explain how neural networks learn through backpropagation in detail."

def check_server():
    """Check if server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/models", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_speed(num_tests=3):
    """Test generation speed"""
    print("=" * 70)
    print("FlashAttention Performance Test")
    print("=" * 70)
    print()
    
    if not check_server():
        print("❌ Error: vLLM server is not running!")
        print()
        print("Start the server first:")
        print("  ./start_vllm_server.sh")
        sys.exit(1)
    
    print(f"✅ Connected to server")
    print(f"📝 Test prompt: '{TEST_PROMPT}'")
    print(f"🔄 Running {num_tests} tests...")
    print()
    
    results = []
    
    for i in range(num_tests):
        print(f"Test {i+1}/{num_tests}...", end=" ", flush=True)
        
        try:
            start_time = time.time()
            token_count = 0
            
            response = requests.post(
                f"{SERVER_URL}/chat/completions",
                json={
                    "model": MODEL_NAME,
                    "messages": [{"role": "user", "content": TEST_PROMPT}],
                    "max_tokens": 200,
                    "temperature": 0.8,
                    "stream": True,
                },
                stream=True,
                timeout=60
            )
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data = line_str[6:]
                        if data == '[DONE]':
                            break
                        try:
                            import json
                            chunk = json.loads(data)
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    token_count += 1
                        except:
                            pass
            
            elapsed = time.time() - start_time
            tokens_per_sec = token_count / elapsed if elapsed > 0 else 0
            
            results.append({
                'tokens': token_count,
                'time': elapsed,
                'speed': tokens_per_sec
            })
            
            print(f"✅ {tokens_per_sec:.2f} tok/s ({token_count} tokens in {elapsed:.2f}s)")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    if not results:
        print("\n❌ All tests failed!")
        sys.exit(1)
    
    # Calculate statistics
    avg_speed = sum(r['speed'] for r in results) / len(results)
    avg_tokens = sum(r['tokens'] for r in results) / len(results)
    avg_time = sum(r['time'] for r in results) / len(results)
    
    print()
    print("=" * 70)
    print("Results Summary")
    print("=" * 70)
    print(f"Average Speed:   {avg_speed:.2f} tokens/second")
    print(f"Average Tokens:  {avg_tokens:.0f} tokens")
    print(f"Average Time:    {avg_time:.2f} seconds")
    print()
    
    # Compare with baseline
    baseline = 200.0  # Your previous speed
    improvement = ((avg_speed - baseline) / baseline) * 100
    
    print("=" * 70)
    print("Comparison")
    print("=" * 70)
    print(f"Before (xformers):        {baseline:.2f} tok/s")
    print(f"After (FlashAttention):   {avg_speed:.2f} tok/s")
    print()
    
    if improvement > 2:
        print(f"🚀 Improvement: +{improvement:.1f}% FASTER! ✅")
    elif improvement > -2:
        print(f"📊 Change: {improvement:+.1f}% (roughly the same)")
    else:
        print(f"📉 Change: {improvement:+.1f}% (slightly slower)")
    
    print("=" * 70)
    print()
    
    # Interpretation
    if improvement > 10:
        print("💡 FlashAttention is providing significant speedup!")
    elif improvement > 5:
        print("💡 FlashAttention is providing moderate improvement.")
    elif improvement > 2:
        print("💡 FlashAttention is providing small improvement.")
    else:
        print("💡 FlashAttention may not be helping much for your workload.")
        print("   xformers was already very good!")
    
    return avg_speed, improvement

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test FlashAttention performance")
    parser.add_argument("--runs", type=int, default=3, help="Number of test runs (default: 3)")
    args = parser.parse_args()
    
    test_speed(args.runs)
