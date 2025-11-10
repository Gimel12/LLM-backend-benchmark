#!/usr/bin/env python3
"""
Web server for LLM Load Testing Dashboard
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import asyncio
import json
from load_tester import run_load_test
import socket

app = Flask(__name__)
CORS(app)

# Configuration
VLLM_URL = "http://localhost:8000"
OLLAMA_URL = "http://localhost:11434"
TEST_PROMPT = "Write a comprehensive essay about the American Revolution, covering its causes, major events, key figures, and lasting impact on world history."

@app.route('/')
def index():
    return render_template('benchmark_dashboard.html')

@app.route('/api/test', methods=['POST'])
def run_test():
    """Run the load test"""
    data = request.json
    
    user_counts = data.get('user_counts', [1, 2, 5, 10, 20])
    custom_prompt = data.get('prompt', TEST_PROMPT)
    
    # Run async load test
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(
        run_load_test(VLLM_URL, OLLAMA_URL, custom_prompt, user_counts)
    )
    loop.close()
    
    # Convert results to JSON-serializable format
    json_results = {
        'vllm': [
            {
                'num_users': r.num_users,
                'tokens_per_second': r.tokens_per_second,
                'avg_latency': r.avg_latency,
                'p95_latency': r.p95_latency,
                'p99_latency': r.p99_latency,
                'success_rate': r.success_rate,
                'total_tokens': r.total_tokens,
                'total_time': r.total_time
            }
            for r in results['vllm']
        ],
        'ollama': [
            {
                'num_users': r.num_users,
                'tokens_per_second': r.tokens_per_second,
                'avg_latency': r.avg_latency,
                'p95_latency': r.p95_latency,
                'p99_latency': r.p99_latency,
                'success_rate': r.success_rate,
                'total_tokens': r.total_tokens,
                'total_time': r.total_time
            }
            for r in results['ollama']
        ]
    }
    
    return jsonify(json_results)

@app.route('/api/status', methods=['GET'])
def check_status():
    """Check if servers are accessible"""
    import requests
    
    vllm_status = False
    ollama_status = False
    
    try:
        r = requests.get(f"{VLLM_URL}/v1/models", timeout=2)
        vllm_status = r.status_code == 200
    except:
        pass
    
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        ollama_status = r.status_code == 200
    except:
        pass
    
    return jsonify({
        'vllm': vllm_status,
        'ollama': ollama_status
    })

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == '__main__':
    ip = get_local_ip()
    port = 5000
    
    print("=" * 70)
    print("🚀 LLM Load Testing Dashboard")
    print("=" * 70)
    print()
    print("📱 Access from your computer:")
    print(f"   http://{ip}:{port}")
    print()
    print("💻 Access locally:")
    print(f"   http://localhost:{port}")
    print()
    print("=" * 70)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=False)
