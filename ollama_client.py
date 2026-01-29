"""
Ollama integration for vision and LLM models
"""
import ollama
import base64
from typing import Dict, List
from config import Config

class OllamaVision:
    """Client for interacting with Ollama vision and LLM models"""
    
    def __init__(self, host: str = None, vision_model: str = None, llm_model: str = None):
        """
        Initialize Ollama client
        
        Args:
            host: Ollama server host URL
            vision_model: Name of the vision model (e.g., 'qwen3-vl')
            llm_model: Name of the LLM model (e.g., 'llama3.1')
        """
        self.host = host or Config.OLLAMA_HOST
        self.vision_model = vision_model or Config.VISION_MODEL
        self.llm_model = llm_model or Config.LLM_MODEL
        
        # Initialize Ollama client
        self.client = ollama.Client(host=self.host)
    
    def analyze_image(self, image_path: str) -> str:
        """
        Analyze an image using the vision model
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Description of the image
        """
        try:
            print(f"Analyzing image with {self.vision_model}: {image_path}")
            
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Call Ollama vision model
            response = self.client.chat(
                model=self.vision_model,
                messages=[{
                    'role': 'user',
                    'content': 'Describe this image in detail. Include the main subjects, setting, colors, mood, and any notable elements or actions.',
                    'images': [image_path]
                }]
            )
            
            description = response['message']['content']
            print(f"Image description: {description[:100]}...")
            return description
            
        except Exception as e:
            print(f"Error analyzing image {image_path}: {e}")
            return None
    
    def generate_prompt(self, description: str) -> str:
        """
        Generate a ComfyUI-style prompt from an image description
        
        Args:
            description: Description of the image
            
        Returns:
            Generated prompt for image generation
        """
        try:
            print(f"Generating prompt with {self.llm_model}...")
            
            system_message = """You are an expert at creating prompts for AI image generation tools like ComfyUI, Stable Diffusion, and Midjourney.
Given a description of an image, create a detailed, comma-separated prompt that could be used to recreate the image.

Focus on:
- Main subjects and their characteristics
- Art style and medium
- Lighting and atmosphere
- Colors and composition
- Quality modifiers (e.g., "highly detailed", "4k", "photorealistic")

Keep the prompt concise but descriptive. Use comma-separated tags.
Do not include explanations, just output the prompt."""

            response = self.client.chat(
                model=self.llm_model,
                messages=[
                    {'role': 'system', 'content': system_message},
                    {'role': 'user', 'content': f"Create an image generation prompt based on this description:\n\n{description}"}
                ]
            )
            
            prompt = response['message']['content'].strip()
            print(f"Generated prompt: {prompt[:100]}...")
            return prompt
            
        except Exception as e:
            print(f"Error generating prompt: {e}")
            return None
    
    def process_image(self, image_path: str) -> Dict:
        """
        Process an image: analyze it and generate a prompt
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with description and prompt
        """
        description = self.analyze_image(image_path)
        if not description:
            return None
        
        prompt = self.generate_prompt(description)
        if not prompt:
            return None
        
        return {
            'image_path': image_path,
            'description': description,
            'prompt': prompt
        }
    
    def batch_process_images(self, image_paths: List[str]) -> List[Dict]:
        """
        Process multiple images
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of processing results
        """
        results = []
        total = len(image_paths)
        
        for idx, image_path in enumerate(image_paths, 1):
            print(f"\n{'='*60}")
            print(f"Processing image {idx}/{total}")
            print(f"{'='*60}")
            
            result = self.process_image(image_path)
            if result:
                results.append(result)
        
        return results
