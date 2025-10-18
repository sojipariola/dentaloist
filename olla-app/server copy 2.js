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

// Health check with better Ollama verification
app.get('/api/health', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:11434/api/tags', {
            timeout: 3000
        });
        
        const sojiModel = response.data.models.find(m => m.name === 'soji:latest');
        
        res.json({ 
            status: 'OK', 
            message: 'OLLA server and Ollama are running',
            ollama_available: true,
            soji_model_available: !!sojiModel,
            total_models: response.data.models.length
        });
    } catch (error) {
        res.status(503).json({ 
            status: 'ERROR', 
            message: 'Ollama server not available',
            ollama_available: false,
            error: error.message 
        });
    }
});

// Improved chat endpoint with better error handling
app.post('/api/chat', async (req, res) => {
    try {
        const { message, model = 'soji' } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        console.log(`Received request for model: ${model}, message: ${message.substring(0, 50)}...`);

        // First, verify the model exists
        const modelsResponse = await axios.get('http://localhost:11434/api/tags', {
            timeout: 3000
        });

        const modelExists = modelsResponse.data.models.some(m => m.name === model || m.name === `${model}:latest`);
        if (!modelExists) {
            return res.status(400).json({ 
                error: 'Model not found',
                available_models: modelsResponse.data.models.map(m => m.name)
            });
        }

        // Now make the chat request with shorter timeout
        const response = await axios.post('http://localhost:11434/api/chat', {
            model: model,
            messages: [
                { 
                    role: 'system', 
                    content: 'You are Soji, an expert AI programming assistant. Provide concise coding help.' 
                },
                { role: 'user', content: message }
            ],
            stream: false,
            options: {
                temperature: 0.1,
                num_predict: 256 // Shorter responses for faster testing
            }
        }, {
            timeout: 15000 // 15 second timeout instead of 30
        });

        const ollamaResponse = response.data.message.content;
        console.log('Response generated successfully');
        
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
                error: 'Ollama request timeout',
                solution: 'The model is taking too long to respond. Try a simpler query or check Ollama status.'
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

// Start server
app.listen(port, '127.0.0.1', () => {
    console.log(`🚀 OLLA server running on http://127.0.0.1:${port}`);
    console.log(`📋 Check health: http://127.0.0.1:${port}/api/health`);
});

// Test Ollama connection on startup
async function testOllamaConnection() {
    try {
        const response = await axios.get('http://localhost:11434/api/tags', {
            timeout: 3000
        });
        console.log('✅ Ollama connection successful');
        console.log(`📦 Available models: ${response.data.models.map(m => m.name).join(', ')}`);
    } catch (error) {
        console.log('❌ Ollama connection failed');
        console.log('💡 Run: sudo systemctl start ollama');
    }
}

testOllamaConnection();