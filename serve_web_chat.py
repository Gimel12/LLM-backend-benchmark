#!/usr/bin/env python3
"""
Simple web server to serve the chat interface
Allows remote access from other computers on the network
"""

import http.server
import socketserver
import socket
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow API requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()


def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"


if __name__ == "__main__":
    local_ip = get_local_ip()
    
    print("=" * 70)
    print("🌐 Chat Interface Web Server")
    print("=" * 70)
    print()
    print("Server is running!")
    print()
    print("📱 Access from your computer:")
    print(f"   http://{local_ip}:{PORT}/chat_remote.html")
    print()
    print("💻 Access locally:")
    print(f"   http://localhost:{PORT}/chat_remote.html")
    print()
    print("⚠️  Make sure the vLLM server is running on port 8000")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down web server...")
