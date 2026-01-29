"""
ComfyUI workflow integration
"""
import json
import os
from typing import Dict, List
from config import Config

class ComfyUIWorkflow:
    """Handler for ComfyUI workflow generation"""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize ComfyUI workflow handler
        
        Args:
            output_dir: Directory to save workflow files
        """
        self.output_dir = output_dir or Config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_workflow(self, prompt: str, image_info: Dict = None) -> Dict:
        """
        Create a basic ComfyUI workflow structure
        
        Args:
            prompt: Text prompt for image generation
            image_info: Optional dictionary with image metadata
            
        Returns:
            Workflow dictionary
        """
        # Basic ComfyUI workflow structure
        workflow = {
            "1": {
                "inputs": {
                    "text": prompt,
                    "clip": ["2", 0]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Positive Prompt)"
                }
            },
            "2": {
                "inputs": {
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "3": {
                "inputs": {
                    "text": "blurry, low quality, distorted, watermark",
                    "clip": ["2", 0]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Negative Prompt)"
                }
            },
            "4": {
                "inputs": {
                    "seed": 42,
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
                "_meta": {
                    "title": "KSampler"
                }
            },
            "5": {
                "inputs": {
                    "width": 1024,
                    "height": 1024,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage",
                "_meta": {
                    "title": "Empty Latent Image"
                }
            },
            "6": {
                "inputs": {
                    "samples": ["4", 0],
                    "vae": ["2", 2]
                },
                "class_type": "VAEDecode",
                "_meta": {
                    "title": "VAE Decode"
                }
            },
            "7": {
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": ["6", 0]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "Save Image"
                }
            }
        }
        
        # Add metadata if provided
        if image_info:
            workflow["_metadata"] = {
                "original_image": image_info.get('id', ''),
                "title": image_info.get('title', ''),
                "description": image_info.get('description', '')
            }
        
        return workflow
    
    def save_workflow(self, workflow: Dict, filename: str) -> str:
        """
        Save workflow to a JSON file
        
        Args:
            workflow: Workflow dictionary
            filename: Name of the file to save
            
        Returns:
            Path to saved file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        print(f"Saved workflow to: {filepath}")
        return filepath
    
    def create_workflows_from_results(self, results: List[Dict]) -> List[str]:
        """
        Create ComfyUI workflows from processing results
        
        Args:
            results: List of image processing results with prompts
            
        Returns:
            List of paths to saved workflow files
        """
        workflow_paths = []
        
        for idx, result in enumerate(results, 1):
            prompt = result.get('prompt')
            if not prompt:
                continue
            
            # Extract image info
            image_info = {
                'id': os.path.basename(result.get('image_path', '')),
                'title': f"Image {idx}",
                'description': result.get('description', '')[:200]
            }
            
            # Create workflow
            workflow = self.create_workflow(prompt, image_info)
            
            # Save workflow
            filename = f"workflow_{idx:02d}.json"
            filepath = self.save_workflow(workflow, filename)
            workflow_paths.append(filepath)
        
        return workflow_paths
    
    def create_summary(self, results: List[Dict], workflow_paths: List[str]) -> str:
        """
        Create a summary markdown file with all results
        
        Args:
            results: List of processing results
            workflow_paths: List of workflow file paths
            
        Returns:
            Path to summary file
        """
        summary_path = os.path.join(self.output_dir, 'summary.md')
        
        with open(summary_path, 'w') as f:
            f.write("# ollamaVision Processing Results\n\n")
            f.write(f"Processed {len(results)} images\n\n")
            
            for idx, result in enumerate(results, 1):
                f.write(f"## Image {idx}\n\n")
                f.write(f"**Original Path:** `{result.get('image_path')}`\n\n")
                f.write(f"**Description:**\n{result.get('description')}\n\n")
                f.write(f"**Generated Prompt:**\n```\n{result.get('prompt')}\n```\n\n")
                f.write(f"**Workflow File:** `{workflow_paths[idx-1] if idx <= len(workflow_paths) else 'N/A'}`\n\n")
                f.write("---\n\n")
        
        print(f"Saved summary to: {summary_path}")
        return summary_path
