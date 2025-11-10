# Remote Access Guide - Chat from Your Computer

Your vLLM server is running! Now access it from any computer on your network.

## ✅ Server is Running

I can see it's accessible at:
- **Server IP**: Your machine (the one with GPUs)
- **vLLM API Port**: 8000
- **Status**: ✅ Running (I saw request from 192.168.1.44)

---

## 🚀 Quick Start (2 Terminals)

### Terminal 1: vLLM Server (Already Running!)
```bash
# This is already running - keep it open
./start_vllm_server.sh
```

### Terminal 2: Web Interface Server
```bash
cd /home/bizon/CascadeProjects/llm-benchmark
python3 serve_web_chat.py
```

This will show you the URL to access from your computer!

---

## 📱 Access from Your Computer

### Step 1: Get the Server IP

The `serve_web_chat.py` script will display it, or run:
```bash
hostname -I | awk '{print $1}'
```

Let's say it shows: `192.168.1.100`

### Step 2: Open in Your Browser

On **your computer** (not the server), open:
```
http://192.168.1.100:8080/chat_remote.html
```

### Step 3: Start Chatting!

The interface will auto-detect the vLLM server and connect. You'll see:
- ✅ Real-time token streaming
- 📊 Live tokens/second stats
- 💬 Full conversation history

---

## 🔧 Alternative: Direct Access

If you can't run the web server, you can also:

### Option 1: Copy HTML to Your Computer
```bash
# On server, find the IP
hostname -I

# On your computer, download the file
scp bizon@192.168.1.100:/home/bizon/CascadeProjects/llm-benchmark/chat_remote.html ~/Downloads/

# Open the downloaded file in browser
# Manually enter server URL: http://192.168.1.100:8000
```

### Option 2: Use CLI from Your Computer
```bash
# SSH to the server
ssh bizon@192.168.1.100

# Run the chat CLI
cd /home/bizon/CascadeProjects/llm-benchmark
python3 chat_cli.py
```

---

## 🌐 Full Setup Example

```bash
# Terminal 1 on SERVER (GPU machine)
./start_vllm_server.sh
# Wait for "Application startup complete"

# Terminal 2 on SERVER
python3 serve_web_chat.py
# Note the IP address shown (e.g., 192.168.1.100)

# On YOUR COMPUTER
# Open browser and go to:
# http://192.168.1.100:8080/chat_remote.html
```

---

## 📊 What You'll See

```
Browser (your computer):
┌─────────────────────────────────────┐
│  🚀 vLLM Chat - GPT-OSS-120B       │
│  ✅ Connected                       │
├─────────────────────────────────────┤
│  Server: http://192.168.1.100:8000 │
│  Speed: 37.5 tok/s | Tokens: 150   │
├─────────────────────────────────────┤
│  🧑 You: What is quantum computing?│
│                                     │
│  🤖 Assistant: [streaming tokens]  │
└─────────────────────────────────────┘
```

---

## 🔍 Troubleshooting

### Can't Connect from Your Computer?

**1. Check Firewall**
```bash
# On server, allow ports 8000 and 8080
sudo ufw allow 8000
sudo ufw allow 8080
```

**2. Verify Server is Accessible**
```bash
# On your computer, test connection
curl http://192.168.1.100:8000/v1/models
```

Should return JSON with model info.

**3. Check Server is Listening on All Interfaces**
```bash
# On server
netstat -tuln | grep 8000
# Should show 0.0.0.0:8000 (not 127.0.0.1:8000)
```

**4. Manual Server URL**
If auto-detection fails, manually enter in the interface:
```
http://YOUR-SERVER-IP:8000
```

---

## ⚡ Performance Tips

### On Your Computer
- Use Chrome/Firefox for best streaming performance
- Keep browser tab active for smooth streaming
- Check your network latency: `ping 192.168.1.100`

### On Server
- Keep both terminals open (vLLM + web server)
- Monitor GPU: `watch -n 1 nvidia-smi`
- Check server logs for any errors

---

## 🎯 Ports Summary

| Port | Service | Access |
|------|---------|--------|
| **8000** | vLLM API Server | Required for chat |
| **8080** | Web Interface Server | Access from browser |

---

## 📱 Multiple Users

The setup supports multiple people chatting simultaneously:
- Each person opens `http://SERVER-IP:8080/chat_remote.html`
- vLLM handles concurrent requests automatically
- Total throughput is shared across users

---

## 🔐 Security Note

This setup is for **local network only**. If you need internet access:
1. Set up proper authentication
2. Use HTTPS/SSL
3. Consider using a reverse proxy (nginx)
4. Don't expose directly to the internet without security measures

---

## ✨ Ready to Test!

1. **Keep vLLM server running** (Terminal 1)
2. **Start web server**: `python3 serve_web_chat.py` (Terminal 2)
3. **Note the IP** shown by the web server
4. **Open on your computer**: `http://THAT-IP:8080/chat_remote.html`
5. **Start chatting** and watch the real-time streaming!

The interface will show you the **actual interactive speed** (20-50 tok/s) instead of the batch throughput (875 tok/s).
