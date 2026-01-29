#!/usr/bin/env python3
"""
Demo script to show the pipeline flow without requiring API keys or models
"""
import json
import os

def create_demo_structure():
    """Create demo files to show the pipeline output"""
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Demo results - what would be produced by the pipeline
    demo_results = [
        {
            'image_path': 'downloads/demo_image_1.jpg',
            'description': 'A majestic mountain landscape at sunset. Snow-capped peaks are silhouetted against a vibrant orange and purple sky. A small alpine lake reflects the dramatic colors. The scene conveys a sense of peace and natural beauty.',
            'prompt': 'majestic mountain landscape, snow-capped peaks, sunset, vibrant orange and purple sky, alpine lake, reflection, peaceful, natural beauty, highly detailed, 4k, photorealistic, dramatic lighting'
        },
        {
            'image_path': 'downloads/demo_image_2.jpg',
            'description': 'A futuristic cityscape at night with towering skyscrapers covered in glowing neon signs. Flying vehicles can be seen between the buildings. The scene has a cyberpunk aesthetic with blue and pink lighting dominating the color palette.',
            'prompt': 'futuristic cityscape, cyberpunk, towering skyscrapers, neon signs, glowing lights, flying vehicles, night scene, blue and pink lighting, highly detailed, 4k, sci-fi, atmospheric'
        },
        {
            'image_path': 'downloads/demo_image_3.jpg',
            'description': 'A whimsical forest scene with magical elements. Glowing mushrooms illuminate a path through ancient trees. Fireflies dance in the air, and there is a sense of enchantment and mystery in the atmosphere.',
            'prompt': 'whimsical forest, magical atmosphere, glowing mushrooms, ancient trees, fireflies, enchanted, mysterious, fantasy art, detailed, vibrant colors, ethereal lighting, mystical'
        }
    ]
    
    # Create demo ComfyUI workflows
    for idx, result in enumerate(demo_results, 1):
        # Create a basic ComfyUI workflow structure
        workflow = {
            "1": {
                "inputs": {
                    "text": result['prompt'],
                    "clip": ["2", 0]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "CLIP Text Encode (Positive Prompt)"}
            },
            "2": {
                "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"},
                "class_type": "CheckpointLoaderSimple",
                "_meta": {"title": "Load Checkpoint"}
            },
            "3": {
                "inputs": {
                    "text": "blurry, low quality, distorted, watermark",
                    "clip": ["2", 0]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "CLIP Text Encode (Negative Prompt)"}
            },
            "4": {
                "inputs": {
                    "seed": 42 + idx,
                    "steps": 30,
                    "cfg": 7.5,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["2", 0],
                    "positive": ["1", 0],
                    "negative": ["3", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler",
                "_meta": {"title": "KSampler"}
            },
            "5": {
                "inputs": {"width": 1024, "height": 1024, "batch_size": 1},
                "class_type": "EmptyLatentImage",
                "_meta": {"title": "Empty Latent Image"}
            },
            "6": {
                "inputs": {"samples": ["4", 0], "vae": ["2", 2]},
                "class_type": "VAEDecode",
                "_meta": {"title": "VAE Decode"}
            },
            "7": {
                "inputs": {"filename_prefix": f"ollamaVision_{idx}", "images": ["6", 0]},
                "class_type": "SaveImage",
                "_meta": {"title": "Save Image"}
            },
            "_metadata": {
                "original_image": os.path.basename(result['image_path']),
                "description": result['description'][:200]
            }
        }
        
        # Save workflow
        workflow_file = f'output/demo_workflow_{idx:02d}.json'
        with open(workflow_file, 'w') as f:
            json.dump(workflow, f, indent=2)
        print(f"✓ Created {workflow_file}")
    
    # Create summary markdown
    summary_file = 'output/demo_summary.md'
    with open(summary_file, 'w') as f:
        f.write("# ollamaVision Demo Results\n\n")
        f.write("This is a demonstration of what the pipeline would produce.\n\n")
        f.write(f"Processed {len(demo_results)} demo images\n\n")
        
        for idx, result in enumerate(demo_results, 1):
            f.write(f"## Demo Image {idx}\n\n")
            f.write(f"**Original Path:** `{result['image_path']}`\n\n")
            f.write(f"**Description:**\n{result['description']}\n\n")
            f.write(f"**Generated Prompt:**\n```\n{result['prompt']}\n```\n\n")
            f.write(f"**Workflow File:** `output/demo_workflow_{idx:02d}.json`\n\n")
            f.write("---\n\n")
    
    print(f"✓ Created {summary_file}")
    print("\n" + "="*60)
    print("Demo files created successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  - output/demo_workflow_01.json")
    print("  - output/demo_workflow_02.json")
    print("  - output/demo_workflow_03.json")
    print("  - output/demo_summary.md")
    print("\nThese files demonstrate what the full pipeline would produce.")
    print("To run the actual pipeline with real images:")
    print("  1. Set up your .env file with IMGUR_CLIENT_ID")
    print("  2. Ensure Ollama is running with qwen3-vl and llama3.1")
    print("  3. Run: python main.py")

if __name__ == '__main__':
    create_demo_structure()
