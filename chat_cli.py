#!/usr/bin/env python3
"""
Simple CLI chat interface for vLLM server
Shows real-time token generation with speed measurement
"""

import requests
import time
import sys
from typing import Iterator

# Server configuration
BASE_URL = "http://localhost:8000/v1"
MODEL_NAME = "openai/gpt-oss-120b"


def stream_chat(messages: list, max_tokens: int = 2048) -> Iterator[str]:
    """
    Stream chat completion from vLLM server
    
    Yields:
        Token strings as they are generated
    """
    url = f"{BASE_URL}/chat/completions"
    
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.8,
        "stream": True,
    }
    
    try:
        response = requests.post(url, json=payload, stream=True, timeout=300)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]  # Remove 'data: ' prefix
                    if data == '[DONE]':
                        break
                    try:
                        import json
                        chunk = json.loads(data)
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            if 'content' in delta:
                                yield delta['content']
                    except json.JSONDecodeError:
                        continue
    
    except requests.exceptions.RequestException as e:
        print(f"\nError connecting to server: {e}")
        print("Make sure the vLLM server is running: ./start_vllm_server.sh")
        sys.exit(1)


def check_server() -> bool:
    """Check if vLLM server is running"""
    try:
        response = requests.get(f"{BASE_URL}/models", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def main():
    print("=" * 70)
    print("vLLM Chat Interface - Real-Time Token Generation")
    print("=" * 70)
    print()
    
    # Check if server is running
    if not check_server():
        print("❌ Error: vLLM server is not running!")
        print()
        print("Start the server first:")
        print("  ./start_vllm_server.sh")
        print()
        print("Wait for the server to fully load (you'll see 'Application startup complete')")
        print("Then run this chat client again.")
        sys.exit(1)
    
    print("✅ Connected to vLLM server")
    print()
    print("Type your message and press Enter. Type 'quit' or 'exit' to stop.")
    print("Type 'clear' to clear conversation history.")
    print("=" * 70)
    print()
    
    conversation = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n🧑 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye! 👋")
                break
            
            if user_input.lower() == 'clear':
                conversation = []
                print("\n🗑️  Conversation history cleared!")
                continue
            
            # Add user message to conversation
            conversation.append({"role": "user", "content": user_input})
            
            # Print assistant prefix
            print("\n🤖 Assistant: ", end='', flush=True)
            
            # Track generation stats
            start_time = time.time()
            token_count = 0
            response_text = ""
            
            # Stream response
            for token in stream_chat(conversation):
                print(token, end='', flush=True)
                response_text += token
                token_count += 1
            
            print()  # New line after response
            
            # Calculate and display stats
            elapsed_time = time.time() - start_time
            tokens_per_second = token_count / elapsed_time if elapsed_time > 0 else 0
            
            # Add assistant response to conversation
            conversation.append({"role": "assistant", "content": response_text})
            
            # Display performance stats
            print()
            print("-" * 70)
            print(f"📊 Stats: {token_count} tokens in {elapsed_time:.2f}s = {tokens_per_second:.2f} tokens/sec")
            print("-" * 70)
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


if __name__ == "__main__":
    main()
