"""
Card Forge Wizard Module

Implements the interactive wizard for creating and editing cards.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from cardforge.models import Card
from cardforge.image import crop_hex


def create_new_card(input_func=input, print_func=print) -> Tuple[Optional[Card], bool]:
    """Run the interactive wizard to create a new card.
    
    Args:
        input_func: Function to use for input (default: builtin input)
        print_func: Function to use for output (default: builtin print)
        
    Returns:
        Card: The created card object
    """
    print_func("\n=== CARD FORGE: CREATE NEW CARD ===\n")
    
    # Step 1: Prompt for card title
    title = ""
    while not title:
        title = input_func("Card Title? ")
        if not title:
            print_func("Title is required. Please enter a title.")
    
    # Step 2: Collect metadata in a loop
    print_func("\nEnter metadata fields as key=value pairs (leave blank to finish)")
    metadata: Dict[str, Any] = {}
    while True:
        meta_input = input_func("Add metadata field? (key=value) or blank to finish: ")
        if not meta_input:
            break
            
        if "=" not in meta_input:
            print_func("Invalid format. Please use key=value format.")
            continue
            
        key, value = meta_input.split("=", 1)
        key = key.strip()
        value = value.strip()
        
        if not key:
            print_func("Key cannot be empty.")
            continue
            
        # Try to convert value to number if it looks like one
        if value.isdigit():
            value = int(value)
        elif value.replace(".", "", 1).isdigit() and value.count(".") == 1:
            value = float(value)
        elif value.lower() in ("true", "false"):
            value = value.lower() == "true"
            
        metadata[key] = value
        print_func(f"Added: {key} = {value}")
    
    # Step 3: Optionally attach an image
    image_file = None
    attach_image = input_func("Attach image now? (y/n): ").lower().startswith("y")
    if attach_image:
        while True:
            image_path = input_func("Enter path to image file: ")
            if not image_path:
                print_func("Image attachment canceled.")
                break
                
            try:
                image_file = crop_hex(image_path)
                print_func(f"Image cropped successfully: {image_file}")
                break
            except Exception as e:
                print_func(f"Error processing image: {e}")
                if input_func("Try another image? (y/n): ").lower() != "y":
                    break
    
    # Step 4: Create the card
    card = Card(
        uuid=str(uuid.uuid4()),
        title=title,
        metadata=metadata,
        imageFile=image_file,
        created=datetime.now().isoformat(),
        updated=datetime.now().isoformat()
    )
    
    # Step 5: Confirm the card
    print_func("\n=== CARD SUMMARY ===")
    print_func(f"Title: {card.title}")
    print_func("Metadata:")
    for key, value in card.metadata.items():
        print_func(f"  {key}: {value}")
    if card.imageFile:
        print_func(f"Image: {card.imageFile}")
    else:
        print_func("Image: None")
    
    if input_func("\nConfirm card? (y/n): ").lower().startswith("y"):
        print_func("Card created successfully!")
        create_another = input_func("Create another card? (y/n): ").lower().startswith("y")
        return card, create_another
    else:
        print_func("Card creation canceled.")
        return None, False
