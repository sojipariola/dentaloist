# Complete cleanup
sudo systemctl stop ollama
sudo pkill -f ollama
sudo rm -f /usr/local/bin/ollama
sudo rm -rf /usr/share/ollama
sudo rm -f /etc/systemd/system/ollama.service
rm -rf ~/.ollama

# Reinstall
# curl -fsSL https://ollama.com/install.sh | sh
curl -fsSL https://ollama.com/install.sh | sh -s -- /ollama/ollama-linux-amd64.tar.gz

# Start fresh
sudo systemctl start ollama
sleep 5
ollama pull llama3.2:1b


touch Soji.Modelfile
nano Soji.Modelfile

FROM codellama:13b
# System prompt to define Soji's personality and expertise
SYSTEM """
You are Soji, an expert AI programming assistant.
Your expertise is in: Python, Java, Node.js, React, JavaScript, Data Engineering (Spark, SQL, Pandas), and software architecture.
You provide concise, correct, and efficient code. You explain concepts clearly.
You always follow best practices for security, performance, and readability.
If a user asks for something unsafe or unethical, you politely decline.
"""
# Set parameters
PARAMETER temperature 0.2 # Lower temperature for more deterministic, factual code output
PARAMETER num_ctx 4096   # Larger context window for more code



FROM codellama:13b

# System prompt to define Soji's personality and expertise
SYSTEM """
You are Soji, an expert AI programming assistant.
Your expertise is in: Python, Java, Node.js, React, JavaScript, Data Engineering (Spark, SQL, Pandas), and software architecture.
You provide concise, correct, and efficient code. You explain concepts clearly.
You always follow best practices for security, performance, and readability.
If a user asks for something unsafe or unethical, you politely decline.
"""

# Set parameters
# Lower temperature for more deterministic, factual code output
PARAMETER temperature 0.2

# Larger context window for more code
PARAMETER num_ctx 4096

# You can add more parameters as needed
# PARAMETER top_p 0.9
# PARAMETER top_k 40


# Create a new Modelfile for the smaller base
cat > Soji.Modelfile << 'EOF'
FROM llama3.2:1b

SYSTEM """
You are Soji, an expert AI programming assistant.
Your expertise is in: Python, Java, Node.js, React, JavaScript, Data Engineering.
Provide concise, correct code and explanations. Keep responses focused and practical.
"""

PARAMETER temperature 0.1
PARAMETER num_ctx 1024
PARAMETER num_predict 256
EOF

# Create the new soji model
ollama create soji -f Soji.Modelfile

ollama run soji

ollama pull codellama:13b # Or llama3:8b, mistral, etc.







// 
// npm init -y # Initialize a new Node.js project
// npm install express # Install Express
// npm install axios  # Install Axios for making HTTP requests

// ollama pull soji  # Pull your custom model from Ollama

// ollama server --model soji  # Start the Ollama server with your custom model
// node server.js  # Start your Express server

// sudo lsof -i :11434 # Check if port 11434 is in use
// sudo netstat -tulpn | grep :11434 # Another way to check
// kill -9 <PID> # Kill the process using port 11434

// sudo systemctl stop ollama # Stop Ollama service if running
// sudo systemctl start ollama # Start Ollama service
// sudo systemctl restart ollama # Restart Ollama service
// sudo systemctl status ollama # Check status of Ollama service
// Make sure your Ollama server is running on localhost:11434