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
    
    # Ollama
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    VISION_MODEL = os.getenv('VISION_MODEL', 'qwen3-vl')
    LLM_MODEL = os.getenv('LLM_MODEL', 'llama3.1')
    
    # ComfyUI
    COMFYUI_HOST = os.getenv('COMFYUI_HOST', 'http://localhost:8188')
    
    # Download settings
    DOWNLOAD_DIR = 'downloads'
    OUTPUT_DIR = 'output'
    MAX_IMAGES = 10
