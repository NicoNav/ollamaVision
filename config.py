"""
Configuration module for ollamaVision
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for ollamaVision"""
    
    # Imgur API
    IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID', '')
    IMGUR_API_URL = 'https://api.imgur.com/3'
    
    # Ollama / Vision Model
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    VISION_MODEL = os.getenv('VISION_MODEL', 'qwen3-vl')
    
    # LLM Configuration (can be overridden with custom endpoint)
    LLM_MODEL = os.getenv('LLM_MODEL', 'llama3.1')
    LLM_ENDPOINT = os.getenv('LLM_ENDPOINT', '')  # Custom LLM endpoint (optional)
    LLM_API_KEY = os.getenv('LLM_API_KEY', '')    # API key for custom endpoint (optional)
    
    # ComfyUI
    COMFYUI_HOST = os.getenv('COMFYUI_HOST', 'http://localhost:8188')
    
    # Download settings
    DOWNLOAD_DIR = 'downloads'
    OUTPUT_DIR = 'output'
    MAX_IMAGES = 10
