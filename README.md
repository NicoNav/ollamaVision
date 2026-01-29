# ollamaVision

An automated pipeline that fetches top images from Imgur, analyzes them with qwen3-vl, generates prompts with llama 3.1, and creates ComfyUI workflows to recreate them.

## Features

- 🖼️ Fetches top 10 images of the day from Imgur API (excluding GIFs)
- 👁️ Analyzes images using qwen3-vl vision model
- 🤖 Generates image recreation prompts using llama 3.1 LLM
- 🎨 Creates ComfyUI workflow files ready to import
- 📊 Produces detailed summary of all processed images

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running locally
- qwen3-vl model installed in Ollama (`ollama pull qwen3-vl`)
- llama 3.1 model installed in Ollama (`ollama pull llama3.1`)
- Imgur API Client ID ([Get one here](https://api.imgur.com/oauth2/addclient))
- ComfyUI (optional, for using the generated workflows)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/NicoNav/ollamaVision.git
cd ollamaVision
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Imgur Client ID:
```
IMGUR_CLIENT_ID=your_imgur_client_id_here
```

4. Ensure Ollama is running with the required models:
```bash
# Start Ollama (if not already running)
ollama serve

# Pull required models (in another terminal)
ollama pull qwen3-vl
ollama pull llama3.1
```

## Usage

### Basic Usage

Run the complete pipeline:
```bash
python main.py
```

This will:
1. Fetch top 10 images from Imgur
2. Download them to `downloads/` directory
3. Analyze each image with qwen3-vl
4. Generate prompts with llama 3.1
5. Create ComfyUI workflows in `output/` directory
6. Generate a summary report

### Options

```bash
# Process only 5 images
python main.py --max-images 5

# Use existing downloaded images (skip download step)
python main.py --skip-download

# Use different models
python main.py --vision-model llava --llm-model mistral
```

### Using the Generated Workflows

1. Open ComfyUI in your browser
2. Load one of the workflow JSON files from the `output/` directory
3. Adjust parameters as needed (seed, steps, etc.)
4. Queue the prompt to generate the image

## Project Structure

```
ollamaVision/
├── main.py                 # Main pipeline orchestrator
├── config.py              # Configuration management
├── imgur_client.py        # Imgur API integration
├── ollama_client.py       # Ollama vision and LLM integration
├── comfyui_workflow.py    # ComfyUI workflow generation
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
├── downloads/            # Downloaded images (created automatically)
└── output/               # Generated workflows and summary (created automatically)
```

## Output

The pipeline generates:

1. **Downloaded Images** (`downloads/` directory)
   - Original images from Imgur

2. **ComfyUI Workflows** (`output/` directory)
   - `workflow_01.json`, `workflow_02.json`, etc.
   - Ready to import into ComfyUI

3. **Summary Report** (`output/summary.md`)
   - Image descriptions
   - Generated prompts
   - Workflow file references

## Configuration

### Environment Variables

- `IMGUR_CLIENT_ID` - Your Imgur API client ID (required)
- `OLLAMA_HOST` - Ollama server URL (default: `http://localhost:11434`)
- `VISION_MODEL` - Vision model name (default: `qwen3-vl`)
- `LLM_MODEL` - LLM model name (default: `llama3.1`)
- `COMFYUI_HOST` - ComfyUI server URL (default: `http://localhost:8188`)

### Customizing the Pipeline

You can modify the pipeline by editing the respective modules:

- **Imgur filters**: Edit `imgur_client.py` → `filter_images()`
- **Vision analysis prompt**: Edit `ollama_client.py` → `analyze_image()`
- **Prompt generation**: Edit `ollama_client.py` → `generate_prompt()`
- **ComfyUI workflow structure**: Edit `comfyui_workflow.py` → `create_workflow()`

## Troubleshooting

### "Imgur Client ID is required"
Make sure you've set `IMGUR_CLIENT_ID` in your `.env` file.

### "Connection refused" or Ollama errors
Ensure Ollama is running: `ollama serve`

### Models not found
Pull the required models:
```bash
ollama pull qwen3-vl
ollama pull llama3.1
```

### No images downloaded
- Check your Imgur API credentials
- Verify you have internet connectivity
- Try increasing `--max-images` if there are many GIFs in the top posts

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
