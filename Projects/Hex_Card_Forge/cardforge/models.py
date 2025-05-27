"""
Data models for Card Forge
"""

# This file will contain our Card dataclass implementation

import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class Card:
    """Card model representing a hex-shaped card with metadata and optional image.
    
    Attributes:
        uuid (str): Unique identifier for the card (v4 UUID)
        title (str): Card title
        metadata (Dict[str, Any]): Free-form key-value pairs for card metadata
        imageFile (Optional[str]): Path to the hex-cropped image file, if any
        created (str): ISO-8601 timestamp of when the card was created
        updated (str): ISO-8601 timestamp of when the card was last updated
    """
    uuid: str
    title: str
    metadata: Dict[str, Any]
    created: str
    updated: str
    imageFile: Optional[str] = None
    
    def to_json(self) -> str:
        """Serialize the Card to a JSON string.
        
        Returns:
            str: JSON representation of the card
        """
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, json_data: str) -> 'Card':
        """Deserialize a Card from a JSON string.
        
        Args:
            json_data (str): JSON string representation of a Card
            
        Returns:
            Card: Deserialized Card instance
        """
        data = json.loads(json_data)
        return cls(**data)
