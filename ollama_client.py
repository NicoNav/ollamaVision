"""
Ollama integration for vision and LLM models
"""
import ollama
from typing import Dict, List
from config import Config

class OllamaVision:
    """Client for interacting with Ollama vision and LLM models"""
    
    def __init__(self, host: str = None, vision_model: str = None, llm_model: str = None, 
                 llm_endpoint: str = None, llm_api_key: str = None):
        """
        Initialize Ollama client
        
        Args:
            host: Ollama server host URL (for vision model)
            vision_model: Name of the vision model (e.g., 'qwen3-vl')
            llm_model: Name of the LLM model (e.g., 'llama3.1')
            llm_endpoint: Optional custom endpoint for LLM (overrides Ollama)
            llm_api_key: Optional API key for custom LLM endpoint
        """
        self.host = host or Config.OLLAMA_HOST
        self.vision_model = vision_model or Config.VISION_MODEL
        self.llm_model = llm_model or Config.LLM_MODEL
        self.llm_endpoint = llm_endpoint or Config.LLM_ENDPOINT
        self.llm_api_key = llm_api_key or Config.LLM_API_KEY
        
        # Initialize Ollama client for vision model
        self.client = ollama.Client(host=self.host)
        
        # Flag to determine if using custom LLM endpoint
        self.use_custom_llm = bool(self.llm_endpoint)
    
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
            
            # Call Ollama vision model with image path
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
            
            if self.use_custom_llm:
                # Use custom LLM endpoint
                return self._generate_prompt_custom(description)
            else:
                # Use Ollama
                return self._generate_prompt_ollama(description)
            
        except Exception as e:
            print(f"Error generating prompt: {e}")
            return None
    
    def _generate_prompt_ollama(self, description: str) -> str:
        """Generate prompt using Ollama"""
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
    
    def _generate_prompt_custom(self, description: str) -> str:
        """
        Generate prompt using custom LLM endpoint
        
        NOTE: This is a placeholder implementation. Will be updated when the
        actual endpoint details are provided by the user.
        
        Args:
            description: Description of the image
            
        Returns:
            Generated prompt
        """
        import requests
        
        print(f"Using custom LLM endpoint: {self.llm_endpoint}")
        
        # TODO: Update this implementation when actual endpoint is provided
        # This is a generic implementation that may need adjustment
        
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
        
        headers = {'Content-Type': 'application/json'}
        if self.llm_api_key:
            headers['Authorization'] = f'Bearer {self.llm_api_key}'
        
        # Generic payload structure - may need adjustment for specific endpoint
        payload = {
            'model': self.llm_model,
            'messages': [
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': f"Create an image generation prompt based on this description:\n\n{description}"}
            ]
        }
        
        response = requests.post(
            self.llm_endpoint,
            json=payload,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        
        # Parse response - format may vary by endpoint
        result = response.json()
        
        # Try common response formats
        if 'message' in result and 'content' in result['message']:
            prompt = result['message']['content']
        elif 'choices' in result and len(result['choices']) > 0:
            prompt = result['choices'][0].get('message', {}).get('content', '')
        elif 'response' in result:
            prompt = result['response']
        else:
            prompt = str(result)
        
        prompt = prompt.strip()
        print(f"Generated prompt: {prompt[:100]}...")
        return prompt
    
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
