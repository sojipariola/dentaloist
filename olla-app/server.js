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
        const response = await axios.get('http://localhost:11434/api/tags', {
            timeout: 3000
        });
        
        const models = response.data.models || [];
        const sojiModel = models.find(m => m.name === 'soji:latest');
        const smallModel = models.find(m => m.name === 'llama3.2:1b');
        
        res.json({ 
            status: 'OK', 
            message: 'OLLA server and Ollama are running',
            ollama_available: true,
            soji_model_available: !!sojiModel,
            small_model_available: !!smallModel,
            total_models: models.length,
            models: models.map(m => m.name)
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

// Chat endpoint
app.post('/api/chat', async (req, res) => {
    try {
        const { message, model = 'llama3.2:1b' } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        console.log(`Received request for model: ${model}, message: ${message.substring(0, 50)}...`);

        // Use the generate endpoint which is more reliable
        const response = await axios.post('http://localhost:11434/api/generate', {
            model: model,
            prompt: `You are Soji, an expert AI programming assistant. Provide concise coding help.

User: ${message}

Assistant:`,
            stream: false,
            options: {
                temperature: 0.1,
                num_predict: 150,
                num_ctx: 1024
            }
        }, {
            timeout: 30000, // 10 second timeout
            retry: 3 // Retry up to 3 times on failure
        });

        const ollamaResponse = response.data.response;
        console.log('✅ Response generated successfully');
        
        res.json({ 
            response: ollamaResponse,
            model: model,
            done: response.data.done
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
                solution: 'Try using a simpler query or check if models are loaded'
            });
        }
        
        if (error.response) {
            return res.status(502).json({ 
                error: 'Ollama API error',
                details: error.response.data.error || error.message
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

// Simple test endpoint
app.get('/api/test', async (req, res) => {
    try {
        const response = await axios.post('http://localhost:11434/api/generate', {
            model: 'llama3.2:1b',
            prompt: 'Say hello in Python:',
            stream: false,
            options: { num_predict: 20 }
        }, { timeout: 8000 });

        res.json({ 
            success: true,
            response: response.data.response 
        });
    } catch (error) {
        res.status(500).json({ 
            success: false,
            error: error.message 
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
    console.log(`🧪 Test endpoint: http://127.0.0.1:${port}/api/test`);
    console.log('Press Ctrl+C to stop the server');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down OLLA server...');
    process.exit(0);
});