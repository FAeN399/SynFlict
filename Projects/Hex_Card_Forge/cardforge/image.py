"""
Image processing module for Card Forge.

Handles hexagonal cropping of card images.
"""

# This file will contain the crop_hex function and related image processing utilities

import os
import math
from pathlib import Path
from typing import Union, Tuple, List

from PIL import Image, ImageDraw


def create_hex_mask(size: int) -> Image.Image:
    """Create a flat-top hexagon mask image with transparent background.
    
    Args:
        size (int): Width of the output image (height will be the same)
        
    Returns:
        Image.Image: Mask image with white hexagon on transparent background
    """
    # Create a transparent image
    mask = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    
    # For a regular flat-top hexagon:
    # - If width is 'size', then height is approximately size * sqrt(3)/2
    # - If we force height = width = size, we need to adjust our calculations
    
    # Use the full width of the image
    width = size
    
    # Calculate the side length of the hexagon
    # For a flat-top hexagon with width w, the side length s = w/2
    side_length = width / 2
    
    # Calculate the height of the hexagon
    # For a regular hexagon with side length s, height h = s * sqrt(3)
    height = int(side_length * math.sqrt(3))
    
    # Center the hexagon vertically
    y_offset = (size - height) // 2
    
    # Calculate vertices for the flat-top hexagon
    vertices = [
        (width // 4, y_offset),                           # top-left
        (width * 3 // 4, y_offset),                        # top-right
        (width - 1, y_offset + height // 2),               # right
        (width * 3 // 4, y_offset + height - 1),           # bottom-right
        (width // 4, y_offset + height - 1),               # bottom-left
        (0, y_offset + height // 2)                        # left
    ]
    
    # Draw the hexagon with white fill
    draw.polygon(vertices, fill=(255, 255, 255, 255))
    
    return mask


def crop_hex(image_path: Union[str, Path]) -> str:
    """Crop an image to a flat-top hexagon with transparent corners.
    
    Args:
        image_path (Union[str, Path]): Path to the image file to crop
        
    Returns:
        str: Path to the cropped image file
        
    Raises:
        ValueError: If the image cannot be opened or is an unsupported format
    """
    # Ensure image_path is a Path object
    image_path = Path(image_path)
    
    try:
        # Open the image
        img = Image.open(image_path)
    except Exception as e:
        raise ValueError(f"Failed to open image: {image_path} - {e}")
        
    # Convert to RGBA mode if not already
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    
    # Resize to 1024x1024 while maintaining aspect ratio
    img = resize_image_to_square(img, 1024)
    
    # Create the hexagon mask
    mask = create_hex_mask(1024)
    
    # Apply the mask by compositing
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    
    # Create output path
    output_path = image_path.parent / f"hex_{image_path.stem}.png"
    
    # Save the result
    result.save(output_path, "PNG")
    
    return str(output_path)


def resize_image_to_square(img: Image.Image, size: int) -> Image.Image:
    """Resize image to a square of given size, maintaining aspect ratio.
    
    The image will be scaled down or up to fit within the square,
    and any remaining space will be transparent.
    
    Args:
        img (Image.Image): Image to resize
        size (int): Target size (width and height) of the square
        
    Returns:
        Image.Image: Resized image on a transparent square background
    """
    # Get original dimensions
    width, height = img.size
    
    # Calculate scaling factor to fit within square
    scale = min(size / width, size / height)
    
    # Calculate new dimensions
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Resize using Lanczos filter for high quality
    resized = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Create a square transparent image
    square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    # Calculate position to center the resized image
    position = ((size - new_width) // 2, (size - new_height) // 2)
    
    # Paste the resized image onto the square canvas
    square.paste(resized, position)
    
    return square
