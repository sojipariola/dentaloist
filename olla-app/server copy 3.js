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

// Health check
app.get('/api/health', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:11434/api/tags', {
            timeout: 3000
        });
        
        res.json({ 
            status: 'OK', 
            message: 'OLLA server and Ollama are running',
            models: response.data.models.map(m => m.name)
        });
    } catch (error) {
        res.status(503).json({ 
            status: 'ERROR', 
            message: 'Ollama server not available',
            error: error.message 
        });
    }
});

// Chat endpoint - using faster model by default
app.post('/api/chat', async (req, res) => {
    try {
        const { message, model = 'llama3.2:1b' } = req.body; // ← Changed default to faster model
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        console.log(`Received request for model: ${model}, message: ${message.substring(0, 50)}...`);

        const response = await axios.post('http://localhost:11434/api/chat', {
            model: model,
            messages: [
                { 
                    role: 'system', 
                    content: 'You are Soji, an expert AI programming assistant. Provide concise coding help. Keep responses under 200 words.' 
                },
                { role: 'user', content: message }
            ],
            stream: false,
            options: {
                temperature: 0.1,
                num_predict: 150, // Even shorter responses
                num_ctx: 512 // Smaller context window
            }
        }, {
            timeout: 10000 // 10 second timeout
        });

        const ollamaResponse = response.data.message.content;
        console.log('✅ Response generated successfully');
        
        res.json({ 
            response: ollamaResponse,
            model: model
        });

    } catch (error) {
        console.error('Error details:', error.message);
        
        if (error.code === 'ECONNREFUSED') {
            return res.status(503).json({ 
                error: 'Ollama server not running',
                solution: 'Please start Ollama with: sudo systemctl start ollama'
            });
        }
        
        if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
            return res.status(504).json({ 
                error: 'Model response timeout',
                solution: 'Try using a smaller model like llama3.2:1b or simplify your query.'
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
            timeout: 3000
        });
        res.json(response.data);
    } catch (error) {
        res.status(503).json({ 
            error: 'Cannot connect to Ollama',
            solution: 'Make sure Ollama is running: sudo systemctl start ollama'
        });
    }
});

// Model recommendations based on performance
app.get('/api/recommended-model', (req, res) => {
    res.json({ 
        recommended_model: 'llama3.2:1b',
        reason: 'Fastest response time for this hardware',
        alternatives: ['soji:latest', 'codellama:13b'] 
    });
});

// Start server
app.listen(port, '127.0.0.1', () => {
    console.log(`🚀 OLLA server running on http://127.0.0.1:${port}`);
    console.log(`📋 Check health: http://127.0.0.1:${port}/api/health`);
    console.log(`💡 Using faster model 'llama3.2:1b' by default for better performance`);
});

// Test connection
async function testOllamaConnection() {
    try {
        const response = await axios.get('http://localhost:11434/api/tags', {
            timeout: 3000
        });
        console.log('✅ Ollama connection successful');
        console.log(`📦 Available models: ${response.data.models.map(m => m.name).join(', ')}`);
    } catch (error) {
        console.log('❌ Ollama connection failed');
    }
}

testOllamaConnection();