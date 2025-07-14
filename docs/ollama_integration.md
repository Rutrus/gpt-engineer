# Ollama Integration

GPT Engineer now supports **Ollama** for running models locally without depending on external APIs. This integration allows you to use models like `qwen2.5-coder` completely offline.

## Quick Setup

### 1. Install Ollama

```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### 2. Download the Model

```bash
# Download qwen2.5-coder (recommended for development)
ollama pull qwen2.5-coder

# Verify it works
ollama run qwen2.5-coder "Write a Python function that adds two numbers"
```

### 3. Start the Ollama API Server

```bash
# In a separate terminal (persistent)
ollama serve
```

The API will be available at `http://localhost:11434/v1`

### 4. Configure Environment Variables

Create a `.env` file in your working directory:

```env
# .env
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=ollama
MODEL_NAME=qwen2.5-coder
IS_OLLAMA=true
```

### 5. Use GPT Engineer with Ollama

```bash
# Generate a new project
gpt-engineer projects/my-project

# Or specify the model directly
gpt-engineer projects/my-project qwen2.5-coder
```

## Recommended Models

### For Code Development

- **qwen2.5-coder** (7B) - Excellent for programming tasks
- **codellama:13b** - Specialized in code
- **deepseek-coder:6.7b** - Good balance between speed and quality

### For General Tasks

- **llama3.2:3b** - Fast and efficient
- **mistral:7b** - Good general performance
- **qwen2.5:7b** - Versatile and powerful

## Advanced Configuration

### Adjust Model Parameters

```bash
# Use lower temperature for more deterministic code
gpt-engineer projects/my-project qwen2.5-coder --temperature 0.1

# Lite mode for simpler prompts
gpt-engineer projects/my-project qwen2.5-coder --lite
```

### Hardware Configuration

For better performance, adjust Ollama parameters according to your hardware:

```bash
# For GPU (adjust according to your VRAM)
ollama run qwen2.5-coder --gpu-layers 30

# For CPU with more threads
ollama run qwen2.5-coder --numa --num-thread 8
```

### Persistent Configuration

Create a `~/.ollama/config.json` file:

```json
{
  "gpu_layers": 30,
  "num_thread": 8,
  "numa": true
}
```

## Remote Ollama Servers

You can use Ollama with remote servers by configuring the appropriate URL:

```env
# Local server (default port)
OPENAI_API_BASE=http://localhost:11434/v1

# Remote server on your network
OPENAI_API_BASE=http://192.168.1.100:11434/v1

# Cloud server
OPENAI_API_BASE=https://my-ollama-server.com/v1

# With custom port
OPENAI_API_BASE=http://ollama.mydomain.com:8080/v1

# With authentication
OPENAI_API_BASE=https://user:password@ollama.mydomain.com/v1

# Don't forget to set IS_OLLAMA=true
IS_OLLAMA=true
```

## Troubleshooting

### Verify Ollama is Working

```bash
# Check if the server is running
curl http://localhost:11434/v1/models

# Test the model directly
ollama run qwen2.5-coder "Simple test"
```

### Common Errors

1. **"Connection refused"**
   - Make sure `ollama serve` is running
   - Verify that port 11434 is free

2. **"Model not found"**
   - Download the model: `ollama pull qwen2.5-coder`
   - Verify the exact model name

3. **Slow responses**
   - Use `--lite` mode for simpler prompts
   - Consider a smaller model
   - Adjust hardware parameters

### Debug Logs

```bash
# View Ollama logs
ollama serve --verbose

# View GPT Engineer logs
gpt-engineer projects/my-project --verbose
```

## Usage Examples

### Generate a REST API

```bash
# Create project directory
mkdir projects/api-rest
cd projects/api-rest

# Create prompt file
echo "Generate a REST API in Python using FastAPI with CRUD endpoints for users" > prompt

# Run with Ollama
gpt-engineer . qwen2.5-coder --lite
```

### Improve Existing Code

```bash
# In improve mode
gpt-engineer projects/my-project qwen2.5-coder --improve
```

## Ollama Advantages

- ✅ **Completely local** - No API keys needed
- ✅ **Total privacy** - Your data never leaves your machine
- ✅ **No costs** - Free once downloaded
- ✅ **No limits** - No rate limits
- ✅ **Multiple models** - Easy switching between models

## Limitations

- ⚠️ **Performance** - Depends on your hardware
- ⚠️ **Quality** - Local models may be less accurate
- ⚠️ **Memory** - Requires sufficient RAM/VRAM
- ⚠️ **Initial download** - Models can be large

## Additional Resources

- [Official Ollama Documentation](https://ollama.com/docs)
- [Available Models](https://ollama.com/library)
- [Performance Optimization](https://ollama.com/docs/performance)