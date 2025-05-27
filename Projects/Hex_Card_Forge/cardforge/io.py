"""
Input/Output module for Card Forge.

Handles importing and exporting cards as ZIP bundles.
"""

# This file will contain the export_card and import_card functions

import os
import zipfile
from pathlib import Path
from typing import Optional, Union, Dict, Any

from cardforge.models import Card


def export_card(card: Card, output_dir: Union[str, Path]) -> str:
    """Export a Card to a ZIP bundle.
    
    The ZIP will be named card_<uuid>.zip and will contain:
    - card_<uuid>.json - The card data in JSON format
    - card_<uuid>.png - The card's hexagonal image (if imageFile is set)
    
    Args:
        card (Card): The card to export
        output_dir (Union[str, Path]): Directory where the ZIP will be saved
        
    Returns:
        str: Full path to the created ZIP file
    """
    # Ensure output_dir is a Path object
    output_dir = Path(output_dir)
    
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare the ZIP filename
    zip_filename = f"card_{card.uuid}.zip"
    zip_path = output_dir / zip_filename
    
    # Create a JSON representation of the card
    json_data = card.to_json()
    json_filename = f"card_{card.uuid}.json"
    
    # Create the ZIP file
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        # Add the JSON data
        zip_file.writestr(json_filename, json_data)
        
        # If an image file is specified, we would add it here in a future implementation
    
    return str(zip_path)


def import_card(zip_path: Union[str, Path]) -> Card:
    """Import a Card from a ZIP bundle.
    
    Expects a ZIP file created by export_card(), containing:
    - card_<uuid>.json - Required: The card data in JSON format
    - card_<uuid>.png - Optional: The card's hexagonal image
    
    Args:
        zip_path (Union[str, Path]): Path to the ZIP file to import
        
    Returns:
        Card: The imported Card object
        
    Raises:
        ValueError: If the ZIP doesn't contain a card_*.json file
    """
    # Ensure zip_path is a Path object
    zip_path = Path(zip_path)
    
    # Open the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # List all files in the ZIP
        files = zip_file.namelist()
        
        # Find the JSON file (should be named card_<uuid>.json)
        json_files = [f for f in files if f.startswith('card_') and f.endswith('.json')]
        
        if not json_files:
            raise ValueError(f"Invalid card bundle: {zip_path} - no card_*.json file found")
        
        # Use the first card_*.json file found
        json_filename = json_files[0]
        
        # Extract the JSON content
        with zip_file.open(json_filename) as json_file:
            json_data = json_file.read().decode('utf-8')
        
        # Deserialize into a Card object
        card = Card.from_json(json_data)
        
        return card
