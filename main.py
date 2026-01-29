#!/usr/bin/env python3
"""
ollamaVision - Main Pipeline

This script orchestrates the complete pipeline:
1. Fetch top 10 images from Imgur (excluding GIFs)
2. Analyze each image with qwen3-vl to get descriptions
3. Generate prompts with llama 3.1
4. Create ComfyUI workflows for image recreation
"""

import argparse
import sys
import os
from pathlib import Path
from imgur_client import ImgurClient
from ollama_client import OllamaVision
from comfyui_workflow import ComfyUIWorkflow
from config import Config

def main():
    """Main pipeline execution"""
    parser = argparse.ArgumentParser(
        description='Fetch Imgur images, analyze with vision AI, and generate ComfyUI workflows'
    )
    parser.add_argument(
        '--max-images',
        type=int,
        default=Config.MAX_IMAGES,
        help=f'Maximum number of images to process (default: {Config.MAX_IMAGES})'
    )
    parser.add_argument(
        '--skip-download',
        action='store_true',
        help='Skip downloading images (use existing images in downloads/)'
    )
    parser.add_argument(
        '--vision-model',
        type=str,
        default=Config.VISION_MODEL,
        help=f'Vision model name (default: {Config.VISION_MODEL})'
    )
    parser.add_argument(
        '--llm-model',
        type=str,
        default=Config.LLM_MODEL,
        help=f'LLM model name (default: {Config.LLM_MODEL})'
    )
    parser.add_argument(
        '--llm-endpoint',
        type=str,
        default=None,
        help='Custom LLM endpoint URL (optional, overrides Ollama for LLM)'
    )
    parser.add_argument(
        '--llm-api-key',
        type=str,
        default=None,
        help='API key for custom LLM endpoint (optional)'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("ollamaVision Pipeline")
    print("="*60)
    print()
    
    # Step 1: Fetch and download images from Imgur
    images_data = []
    if not args.skip_download:
        print("Step 1: Fetching images from Imgur...")
        print("-" * 60)
        
        try:
            imgur = ImgurClient()
            images_data = imgur.fetch_and_download_top_images(max_images=args.max_images)
            
            if not images_data:
                print("No images were downloaded. Check your Imgur API credentials.")
                return 1
            
            print(f"✓ Downloaded {len(images_data)} images\n")
            
        except ValueError as e:
            print(f"Error: {e}")
            print("Please set IMGUR_CLIENT_ID in your .env file")
            return 1
        except Exception as e:
            print(f"Unexpected error during image download: {e}")
            return 1
    else:
        print("Step 1: Skipping download (using existing images)")
        print("-" * 60)
        
        # Load existing images from downloads directory
        download_dir = Config.DOWNLOAD_DIR
        if os.path.exists(download_dir):
            image_files = list(Path(download_dir).glob('*.jpg')) + \
                         list(Path(download_dir).glob('*.jpeg')) + \
                         list(Path(download_dir).glob('*.png'))
            
            images_data = [
                {'local_path': str(img_path), 'id': img_path.stem}
                for img_path in image_files[:args.max_images]
            ]
            print(f"✓ Found {len(images_data)} existing images\n")
        else:
            print(f"Error: Download directory '{download_dir}' does not exist")
            return 1
    
    if not images_data:
        print("No images to process")
        return 1
    
    # Step 2 & 3: Analyze images and generate prompts
    print("Step 2 & 3: Analyzing images and generating prompts...")
    print("-" * 60)
    
    try:
        ollama_client = OllamaVision(
            vision_model=args.vision_model,
            llm_model=args.llm_model,
            llm_endpoint=args.llm_endpoint,
            llm_api_key=args.llm_api_key
        )
        
        image_paths = [img['local_path'] for img in images_data]
        results = ollama_client.batch_process_images(image_paths)
        
        if not results:
            print("No images were successfully processed")
            return 1
        
        print(f"\n✓ Processed {len(results)} images\n")
        
    except Exception as e:
        print(f"Error during image processing: {e}")
        print("Make sure Ollama is running and the models are available")
        return 1
    
    # Step 4: Create ComfyUI workflows
    print("Step 4: Creating ComfyUI workflows...")
    print("-" * 60)
    
    try:
        comfyui = ComfyUIWorkflow()
        workflow_paths = comfyui.create_workflows_from_results(results)
        
        print(f"✓ Created {len(workflow_paths)} workflow files\n")
        
        # Create summary
        summary_path = comfyui.create_summary(results, workflow_paths)
        
        print()
        print("="*60)
        print("Pipeline Complete!")
        print("="*60)
        print(f"✓ Processed {len(results)} images")
        print(f"✓ Generated {len(workflow_paths)} ComfyUI workflows")
        print(f"✓ Summary saved to: {summary_path}")
        print()
        print("Next steps:")
        print(f"1. Check the workflows in the '{Config.OUTPUT_DIR}/' directory")
        print("2. Import them into ComfyUI to recreate the images")
        print("3. Review the summary.md file for details")
        
        return 0
        
    except Exception as e:
        print(f"Error creating workflows: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
