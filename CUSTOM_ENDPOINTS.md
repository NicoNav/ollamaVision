# Custom Endpoint Integration Guide

This document explains how to integrate custom endpoints for LLM and ComfyUI API.

## Custom LLM Endpoint

The pipeline supports using a custom LLM endpoint instead of Ollama for prompt generation while still using Ollama for the vision model (qwen3-vl).

### Configuration

#### Option 1: Environment Variables

Edit your `.env` file:
```bash
# Use custom LLM endpoint
LLM_ENDPOINT=http://your-llm-server:port/api/endpoint
LLM_API_KEY=your_api_key_if_needed
LLM_MODEL=model-name-to-use
```

#### Option 2: Command Line Arguments

```bash
python main.py \
  --llm-endpoint http://your-llm-server:port/api/endpoint \
  --llm-api-key your_api_key \
  --llm-model model-name
```

### Implementation Details

The custom LLM endpoint implementation is in `ollama_client.py` → `_generate_prompt_custom()`.

**Current Implementation:**
- Generic HTTP POST request with JSON payload
- Supports Bearer token authentication
- Attempts to parse common response formats (OpenAI-style, Ollama-style, etc.)

**To Customize:**
When you provide the actual endpoint details, update `_generate_prompt_custom()` with:
1. Correct request format for your endpoint
2. Proper authentication method
3. Response parsing logic
4. Any required headers or parameters

### Request Format

The generic implementation sends:
```json
{
  "model": "model-name",
  "messages": [
    {
      "role": "system",
      "content": "System prompt for image generation prompts..."
    },
    {
      "role": "user", 
      "content": "Create an image generation prompt based on this description:\n\n[description]"
    }
  ]
}
```

### Response Format

The code attempts to parse these common formats:

1. **Ollama-style:**
```json
{
  "message": {
    "content": "generated prompt here"
  }
}
```

2. **OpenAI-style:**
```json
{
  "choices": [
    {
      "message": {
        "content": "generated prompt here"
      }
    }
  ]
}
```

3. **Simple format:**
```json
{
  "response": "generated prompt here"
}
```

If your endpoint uses a different format, update the parsing logic in `_generate_prompt_custom()`.

### Testing Custom Endpoint

1. Set your endpoint configuration
2. Run with a small test:
```bash
python main.py --max-images 1 --llm-endpoint YOUR_ENDPOINT
```
3. Check the output for any errors
4. Verify the generated prompts look correct

---

## ComfyUI API Integration

**Status:** Placeholder implementation ready

### When You Provide the API Details

Please provide:
1. **API file** - The Python module or requirements for ComfyUI API
2. **Endpoint URL** - Full URL including port and path
3. **Authentication** - Any required API keys or tokens
4. **Request format** - Expected payload structure
5. **Response format** - How to parse the response

### Implementation Plan

Once provided, I will update:
1. `comfyui_api.py` - Complete the API client implementation
2. `comfyui_workflow.py` - Add method to submit workflows automatically
3. `main.py` - Add option to auto-submit workflows
4. `.env.example` - Add ComfyUI API configuration
5. Tests - Add integration tests for API submission

### Expected Workflow

After integration, the pipeline will:
1. Fetch and analyze images (as now)
2. Generate prompts (as now)
3. Create ComfyUI workflows (as now)
4. **Automatically submit workflows to ComfyUI** (new)
5. **Monitor generation progress** (new)
6. **Download generated images** (new)

---

## Next Steps

**For LLM Endpoint:**
- Provide endpoint URL and format
- I'll update `_generate_prompt_custom()` accordingly

**For ComfyUI API:**
- Provide API file and endpoint details
- I'll implement complete API integration

**Both integrations are structured and ready for quick implementation once details are provided.**
