"""
Mock downloader for testing without real Reddit API credentials.

This module provides mock download capabilities for the Reddit Media Grabber application.
It creates placeholder images and videos instead of trying to download from external URLs.
"""

import os
import time
import random
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

def create_mock_image(output_path, width=800, height=600, text="Mock Reddit Image"):
    """
    Create a mock image with the given dimensions and text.
    
    Args:
        output_path: Path to save the image to
        width: Image width
        height: Image height
        text: Text to display on the image
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create a new image with a random background color
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        image = Image.new("RGB", (width, height), (r, g, b))
        draw = ImageDraw.Draw(image)
        
        # Try to use a font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            font = ImageFont.load_default()
        
        # Add text to the image
        text_width, text_height = draw.textsize(text, font=font)
        position = ((width - text_width) // 2, (height - text_height) // 2)
        draw.text(position, text, fill=(255-r, 255-g, 255-b), font=font)
        
        # Save the image
        image.save(output_path)
        return True
    except Exception as e:
        logger.error(f"Error creating mock image: {e}")
        return False

def mock_download_file(url, output_path, item_type="image", metadata=None):
    """
    Mock downloading a file by creating a local placeholder.
    
    Args:
        url: URL to download from (ignored)
        output_path: Path to save the file to
        item_type: Type of content (image, video, gif)
        metadata: Optional metadata about the item
        
    Returns:
        tuple: (success, error_message)
    """
    try:
        # Create a mock download with simulated progress
        time.sleep(0.5)  # Simulate network delay
        
        # Get title from metadata or use default
        title = "Mock Reddit Content"
        if metadata and 'title' in metadata:
            title = metadata['title']
            
        # Create the appropriate mock content based on type
        if item_type.lower() in ["image", "photo"]:
            success = create_mock_image(output_path, text=f"Mock Image: {title}")
            if not success:
                return False, "Failed to create mock image"
                
        elif item_type.lower() in ["video", "gif"]:
            # For now, just create an image for videos/gifs too
            output_path = output_path.replace(".mp4", ".jpg").replace(".gif", ".jpg")
            success = create_mock_image(output_path, text=f"Mock {item_type.title()}: {title}")
            if not success:
                return False, f"Failed to create mock {item_type}"
                
        else:
            # For other types, create a simple text file
            with open(output_path, 'w') as f:
                f.write(f"Mock content for {url}\nTitle: {title}\nType: {item_type}")
            
        return True, None
        
    except Exception as e:
        error_message = f"Error in mock download: {str(e)}"
        logger.error(error_message)
        return False, error_message

def is_mock_url(url):
    """
    Check if a URL is likely a mock URL.
    
    Args:
        url: URL to check
        
    Returns:
        bool: True if it's a mock URL, False otherwise
    """
    mock_indicators = [
        "mockimage", 
        "mockvideo",
        "mockgif",
        "example.com",
        "mock.reddit.com"
    ]
    
    return any(indicator in url.lower() for indicator in mock_indicators)
