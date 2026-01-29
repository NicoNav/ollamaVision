# Quick Start Guide

## Prerequisites Setup

### 1. Install Ollama
```bash
# Download from https://ollama.ai/
# Or on Linux:
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull Required Models
```bash
ollama pull qwen3-vl
ollama pull llama3.1
```

### 3. Get Imgur API Key
1. Go to https://api.imgur.com/oauth2/addclient
2. Register application (select "OAuth 2 authorization without a callback URL")
3. Copy your Client ID

## Installation

```bash
# Clone repository
git clone https://github.com/NicoNav/ollamaVision.git
cd ollamaVision

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your IMGUR_CLIENT_ID
```

## Usage

### Run the Pipeline
```bash
# Start Ollama (if not running)
ollama serve

# In another terminal, run the pipeline
python main.py
```

### What Happens
1. Fetches top 10 images from Imgur
2. Downloads them to `downloads/` folder
3. Analyzes each with qwen3-vl
4. Generates prompts with llama 3.1
5. Creates ComfyUI workflows in `output/` folder
6. Generates summary report

### Output
- `downloads/*.jpg` - Original images
- `output/workflow_*.json` - ComfyUI workflows
- `output/summary.md` - Complete report

### Use the Workflows
1. Open ComfyUI
2. Load workflow JSON from `output/` folder
3. Adjust parameters if needed
4. Queue prompt to generate

## Options

```bash
# Process only 5 images
python main.py --max-images 5

# Skip download, use existing images
python main.py --skip-download

# Use different models
python main.py --vision-model llava --llm-model mistral
```

## Try the Demo
```bash
# No API keys needed
python demo.py
```

## Troubleshooting

### Imgur Error
- Check IMGUR_CLIENT_ID in .env file
- Verify internet connection

### Ollama Connection Error
- Ensure `ollama serve` is running
- Check OLLAMA_HOST in .env (default: http://localhost:11434)

### Model Not Found
```bash
ollama list  # Check installed models
ollama pull qwen3-vl  # Install if missing
ollama pull llama3.1
```

## Next Steps

When ready to integrate ComfyUI API:
1. Provide the API file
2. Specify the endpoint
3. Update `comfyui_api.py` implementation
4. Enable automatic workflow submission

## Support

- README.md - Full documentation
- IMPLEMENTATION_SUMMARY.md - Technical details
- test_ollama_vision.py - Run tests with `python -m unittest test_ollama_vision.py`
