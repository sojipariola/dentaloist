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

const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const port = 11435;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Health check endpoint
app.get('/api/health', async (req, res) => {
    try {
        // Check if Ollama is available
        const response = await axios.get('http://localhost:11434/api/tags', {
            timeout: 5000
        });
        res.json({ 
            status: 'OK', 
            message: 'OLLA server and Ollama are running',
            ollama_models: response.data.models.length
        });
    } catch (error) {
        res.status(503).json({ 
            status: 'ERROR', 
            message: 'Ollama server not available',
            error: error.message 
        });
    }
});

// Chat endpoint
app.post('/api/chat', async (req, res) => {
    try {
        const { message, model = 'soji' } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        console.log(`Received request for model: ${model}, message: ${message.substring(0, 50)}...`);

        const response = await axios.post('http://localhost:11434/api/chat', {
            model: model,
            messages: [
                { 
                    role: 'system', 
                    content: 'You are Soji, an expert AI programming assistant. Help with coding questions concisely and accurately.' 
                },
                { role: 'user', content: message }
            ],
            stream: false,
            options: {
                temperature: 0.1,
                num_predict: 512
            }
        }, {
            timeout: 30000 // 30 second timeout
        });

        const ollamaResponse = response.data.message.content;
        console.log('Response generated successfully');
        
        res.json({ 
            response: ollamaResponse,
            model: model,
            usage: response.data.eval_count ? { eval_count: response.data.eval_count } : null
        });

    } catch (error) {
        console.error('Error communicating with Ollama:', error.message);
        
        if (error.code === 'ECONNREFUSED') {
            return res.status(503).json({ 
                error: 'Ollama server not running. Please start Ollama first.',
                details: 'Run: ollama serve or check if Ollama service is running'
            });
        }
        
        if (error.response) {
            // Ollama returned an error
            return res.status(502).json({ 
                error: 'Ollama API error',
                details: error.response.data || error.message
            });
        }
        
        res.status(500).json({ 
            error: 'Internal server error',
            details: error.message 
        });
    }
});

// Get available models
app.get('/api/models', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:11434/api/tags', {
            timeout: 5000
        });
        res.json(response.data);
    } catch (error) {
        res.status(503).json({ 
            error: 'Cannot fetch models from Ollama',
            details: error.message 
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
app.listen(port, '127.0.0.1', () => {
    console.log(`🚀 OLLA server running on http://127.0.0.1:${port}`);
    console.log(`📋 Health check: http://127.0.0.1:${port}/api/health`);
    console.log(`🤖 Available models: http://127.0.0.1:${port}/api/models`);
    console.log(`💬 Chat endpoint: POST http://127.0.0.1:${port}/api/chat`);
    console.log('Press Ctrl+C to stop the server');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down OLLA server...');
    process.exit(0);
});