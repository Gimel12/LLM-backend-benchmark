#!/usr/bin/env python3
"""
Load Testing Tool for vLLM vs Ollama
Tests concurrent users and performance degradation
"""

import asyncio
import aiohttp
import time
import json
from dataclasses import dataclass
from typing import List, Dict
import statistics

@dataclass
class TestResult:
    backend: str
    num_users: int
    tokens_per_second: float
    avg_latency: float
    p95_latency: float
    p99_latency: float
    success_rate: float
    total_tokens: int
    total_time: float

class LoadTester:
    def __init__(self, vllm_url: str, ollama_url: str, test_prompt: str):
        self.vllm_url = vllm_url
        self.ollama_url = ollama_url
        self.test_prompt = test_prompt
        
    async def test_vllm_single(self, session: aiohttp.ClientSession) -> Dict:
        """Test single vLLM request"""
        start_time = time.time()
        tokens = 0
        
        try:
            async with session.post(
                f"{self.vllm_url}/v1/chat/completions",
                json={
                    "model": "openai/gpt-oss-120b",
                    "messages": [{"role": "user", "content": self.test_prompt}],
                    "max_tokens": 500,
                    "temperature": 0.8,
                    "stream": True,
                },
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                async for line in response.content:
                    if line:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith('data: '):
                            data = line_str[6:]
                            if data == '[DONE]':
                                break
                            try:
                                chunk = json.loads(data)
                                if 'choices' in chunk and len(chunk['choices']) > 0:
                                    delta = chunk['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        tokens += 1
                            except:
                                pass
            
            elapsed = time.time() - start_time
            return {
                'success': True,
                'tokens': tokens,
                'latency': elapsed,
                'tokens_per_second': tokens / elapsed if elapsed > 0 else 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'latency': time.time() - start_time
            }
    
    async def test_ollama_single(self, session: aiohttp.ClientSession) -> Dict:
        """Test single Ollama request"""
        start_time = time.time()
        tokens = 0
        
        try:
            async with session.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "gpt-oss:120b",
                    "prompt": self.test_prompt,
                    "stream": True,
                    "options": {
                        "num_predict": 500,
                        "temperature": 0.8,
                    }
                },
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'response' in data:
                                tokens += len(data['response'].split())
                            if data.get('done', False):
                                break
                        except:
                            pass
            
            elapsed = time.time() - start_time
            return {
                'success': True,
                'tokens': tokens,
                'latency': elapsed,
                'tokens_per_second': tokens / elapsed if elapsed > 0 else 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'latency': time.time() - start_time
            }
    
    async def run_concurrent_test(self, backend: str, num_users: int) -> TestResult:
        """Run test with N concurrent users"""
        test_func = self.test_vllm_single if backend == 'vllm' else self.test_ollama_single
        
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            tasks = [test_func(session) for _ in range(num_users)]
            results = await asyncio.gather(*tasks)
            total_time = time.time() - start_time
        
        # Calculate statistics
        successful = [r for r in results if r.get('success', False)]
        latencies = [r['latency'] for r in successful]
        tokens_list = [r['tokens'] for r in successful]
        
        if not successful:
            return TestResult(
                backend=backend,
                num_users=num_users,
                tokens_per_second=0,
                avg_latency=0,
                p95_latency=0,
                p99_latency=0,
                success_rate=0,
                total_tokens=0,
                total_time=total_time
            )
        
        total_tokens = sum(tokens_list)
        avg_latency = statistics.mean(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
        p99_latency = sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0
        success_rate = len(successful) / len(results) * 100
        tokens_per_second = total_tokens / total_time if total_time > 0 else 0
        
        return TestResult(
            backend=backend,
            num_users=num_users,
            tokens_per_second=tokens_per_second,
            avg_latency=avg_latency,
            p95_latency=p95_latency,
            p99_latency=p99_latency,
            success_rate=success_rate,
            total_tokens=total_tokens,
            total_time=total_time
        )

async def run_load_test(vllm_url: str, ollama_url: str, test_prompt: str, 
                        user_counts: List[int]) -> Dict[str, List[TestResult]]:
    """Run complete load test"""
    tester = LoadTester(vllm_url, ollama_url, test_prompt)
    results = {'vllm': [], 'ollama': []}
    
    for num_users in user_counts:
        print(f"Testing with {num_users} concurrent users...")
        
        # Test vLLM
        vllm_result = await tester.run_concurrent_test('vllm', num_users)
        results['vllm'].append(vllm_result)
        print(f"  vLLM: {vllm_result.tokens_per_second:.2f} tok/s, "
              f"{vllm_result.avg_latency:.2f}s latency")
        
        # Test Ollama
        ollama_result = await tester.run_concurrent_test('ollama', num_users)
        results['ollama'].append(ollama_result)
        print(f"  Ollama: {ollama_result.tokens_per_second:.2f} tok/s, "
              f"{ollama_result.avg_latency:.2f}s latency")
        
        # Small delay between tests
        await asyncio.sleep(2)
    
    return results
