"""
Imgur API client for fetching images
"""
import requests
import os
from typing import List, Dict
from config import Config

class ImgurClient:
    """Client for interacting with Imgur API"""
    
    def __init__(self, client_id: str = None):
        """Initialize Imgur client with API credentials"""
        self.client_id = client_id or Config.IMGUR_CLIENT_ID
        if not self.client_id:
            raise ValueError("Imgur Client ID is required. Set IMGUR_CLIENT_ID in .env file")
        
        self.headers = {
            'Authorization': f'Client-ID {self.client_id}'
        }
        self.base_url = Config.IMGUR_API_URL
    
    def get_gallery_top(self, section: str = 'top', sort: str = 'top', window: str = 'day', page: int = 0) -> List[Dict]:
        """
        Fetch top images from Imgur gallery
        
        Args:
            section: Gallery section (hot, top, user)
            sort: Sort method (viral, top, time, rising)
            window: Time window (day, week, month, year, all)
            page: Page number
            
        Returns:
            List of image data dictionaries
        """
        url = f"{self.base_url}/gallery/{section}/{sort}/{window}/{page}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success'):
                return data.get('data', [])
            else:
                print(f"API returned unsuccessful response: {data}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Imgur API: {e}")
            return []
    
    def filter_images(self, items: List[Dict], max_count: int = 10) -> List[Dict]:
        """
        Filter gallery items to get only static images (no GIFs, no albums)
        
        Args:
            items: List of gallery items
            max_count: Maximum number of images to return
            
        Returns:
            List of filtered image dictionaries
        """
        filtered_images = []
        
        for item in items:
            if len(filtered_images) >= max_count:
                break
            
            # Skip albums and galleries
            if item.get('is_album'):
                continue
            
            # Skip GIFs and videos
            item_type = item.get('type', '')
            if 'gif' in item_type.lower() or 'video' in item_type.lower():
                continue
            
            # Check for valid image URL
            link = item.get('link', '')
            if link and any(ext in link.lower() for ext in ['.jpg', '.jpeg', '.png']):
                filtered_images.append({
                    'id': item.get('id'),
                    'title': item.get('title', 'Untitled'),
                    'description': item.get('description', ''),
                    'link': link,
                    'type': item.get('type'),
                    'views': item.get('views', 0),
                    'score': item.get('score', 0)
                })
        
        return filtered_images
    
    def download_image(self, url: str, filename: str, download_dir: str = None) -> str:
        """
        Download an image from URL
        
        Args:
            url: Image URL
            filename: Filename to save as
            download_dir: Directory to save image in
            
        Returns:
            Path to downloaded image
        """
        download_dir = download_dir or Config.DOWNLOAD_DIR
        os.makedirs(download_dir, exist_ok=True)
        
        filepath = os.path.join(download_dir, filename)
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded: {filename}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return None
    
    def fetch_and_download_top_images(self, max_images: int = 10) -> List[Dict]:
        """
        Fetch and download top images of the day
        
        Args:
            max_images: Maximum number of images to download
            
        Returns:
            List of dictionaries with image info and local paths
        """
        print(f"Fetching top images from Imgur...")
        items = self.get_gallery_top()
        
        print(f"Found {len(items)} gallery items")
        filtered = self.filter_images(items, max_images)
        
        print(f"Filtered to {len(filtered)} static images")
        
        results = []
        for idx, image_data in enumerate(filtered):
            # Create filename from image ID
            url = image_data['link']
            ext = url.split('.')[-1]
            filename = f"{image_data['id']}.{ext}"
            
            # Download image
            filepath = self.download_image(url, filename)
            
            if filepath:
                results.append({
                    **image_data,
                    'local_path': filepath
                })
        
        print(f"Successfully downloaded {len(results)} images")
        return results
