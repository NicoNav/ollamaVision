"""
Tests for ollamaVision components
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imgur_client import ImgurClient
from comfyui_workflow import ComfyUIWorkflow

class TestImgurClient(unittest.TestCase):
    """Test Imgur client functionality"""
    
    def test_imgur_client_init(self):
        """Test ImgurClient initialization"""
        client = ImgurClient(client_id='test_client_id')
        self.assertEqual(client.client_id, 'test_client_id')
        self.assertIn('Authorization', client.headers)
    
    def test_filter_images_excludes_gifs(self):
        """Test that GIFs are filtered out"""
        client = ImgurClient(client_id='test')
        
        items = [
            {'id': '1', 'is_album': False, 'type': 'image/jpeg', 'link': 'http://test.com/1.jpg'},
            {'id': '2', 'is_album': False, 'type': 'image/gif', 'link': 'http://test.com/2.gif'},
            {'id': '3', 'is_album': False, 'type': 'image/png', 'link': 'http://test.com/3.png'},
        ]
        
        filtered = client.filter_images(items, max_count=10)
        
        self.assertEqual(len(filtered), 2)
        self.assertNotIn('gif', [img['type'] for img in filtered])
    
    def test_filter_images_excludes_albums(self):
        """Test that albums are filtered out"""
        client = ImgurClient(client_id='test')
        
        items = [
            {'id': '1', 'is_album': False, 'type': 'image/jpeg', 'link': 'http://test.com/1.jpg'},
            {'id': '2', 'is_album': True, 'type': 'image/jpeg', 'link': 'http://test.com/2.jpg'},
        ]
        
        filtered = client.filter_images(items, max_count=10)
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['id'], '1')
    
    def test_filter_images_respects_max_count(self):
        """Test that max_count limit is respected"""
        client = ImgurClient(client_id='test')
        
        items = [
            {'id': str(i), 'is_album': False, 'type': 'image/jpeg', 'link': f'http://test.com/{i}.jpg'}
            for i in range(20)
        ]
        
        filtered = client.filter_images(items, max_count=5)
        
        self.assertEqual(len(filtered), 5)

class TestComfyUIWorkflow(unittest.TestCase):
    """Test ComfyUI workflow generation"""
    
    def test_workflow_creation(self):
        """Test basic workflow structure"""
        workflow_handler = ComfyUIWorkflow(output_dir='/tmp/test_output')
        
        prompt = "a beautiful landscape, mountains, sunset"
        workflow = workflow_handler.create_workflow(prompt)
        
        # Check basic structure
        self.assertIn('1', workflow)  # CLIP Text Encode
        self.assertIn('2', workflow)  # Checkpoint Loader
        self.assertEqual(workflow['1']['inputs']['text'], prompt)
    
    def test_workflow_with_metadata(self):
        """Test workflow with image metadata"""
        workflow_handler = ComfyUIWorkflow(output_dir='/tmp/test_output')
        
        prompt = "test prompt"
        image_info = {'id': 'test123', 'title': 'Test Image'}
        
        workflow = workflow_handler.create_workflow(prompt, image_info)
        
        self.assertIn('_metadata', workflow)
        self.assertEqual(workflow['_metadata']['original_image'], 'test123')

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_imgur_filter_pipeline(self):
        """Test the complete filtering pipeline"""
        client = ImgurClient(client_id='test')
        
        # Simulate Imgur API response
        items = [
            {'id': '1', 'is_album': False, 'type': 'image/jpeg', 'link': 'http://test.com/1.jpg', 
             'title': 'Image 1', 'views': 1000, 'score': 100},
            {'id': '2', 'is_album': True, 'type': 'image/jpeg', 'link': 'http://test.com/2.jpg',
             'title': 'Album', 'views': 2000, 'score': 200},
            {'id': '3', 'is_album': False, 'type': 'image/gif', 'link': 'http://test.com/3.gif',
             'title': 'Animated', 'views': 3000, 'score': 300},
            {'id': '4', 'is_album': False, 'type': 'image/png', 'link': 'http://test.com/4.png',
             'title': 'Image 4', 'views': 4000, 'score': 400},
        ]
        
        filtered = client.filter_images(items, max_count=10)
        
        # Should only have images 1 and 4
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['id'], '1')
        self.assertEqual(filtered[1]['id'], '4')

if __name__ == '__main__':
    unittest.main()
