"""
Tests for Card serialization and deserialization
"""

import uuid
import json
from datetime import datetime
import pytest

from cardforge.models import Card


def test_card_to_json():
    """Test serializing a Card to JSON."""
    # Create a test card
    test_uuid = str(uuid.uuid4())
    test_title = "Test Card"
    test_metadata = {"category": "creature", "power": 2, "toughness": 3}
    test_created = datetime.now().isoformat()
    test_updated = test_created
    
    card = Card(
        uuid=test_uuid,
        title=test_title,
        metadata=test_metadata,
        created=test_created,
        updated=test_updated
    )
    
    # This should fail initially as to_json() is not implemented yet
    json_data = card.to_json()
    
    # Assert the JSON has all expected fields
    assert isinstance(json_data, str)
    
    # Parse to verify the JSON is valid
    parsed = json.loads(json_data)
    assert parsed["uuid"] == test_uuid
    assert parsed["title"] == test_title
    assert parsed["metadata"] == test_metadata
    assert parsed["created"] == test_created
    assert parsed["updated"] == test_updated
    assert "imageFile" in parsed  # Should be None but still present


def test_card_from_json():
    """Test deserializing a Card from JSON."""
    # Create JSON data
    test_uuid = str(uuid.uuid4())
    test_title = "JSON Card"
    test_metadata = {"type": "spell", "cost": 3, "effect": "draw card"}
    test_created = datetime.now().isoformat()
    test_updated = test_created
    test_image = "card_image.png"
    
    json_data = json.dumps({
        "uuid": test_uuid,
        "title": test_title,
        "metadata": test_metadata,
        "imageFile": test_image,
        "created": test_created,
        "updated": test_updated
    })
    
    # This should fail initially as from_json() is not implemented yet
    card = Card.from_json(json_data)
    
    # Assert the deserialized card has all expected values
    assert card.uuid == test_uuid
    assert card.title == test_title
    assert card.metadata == test_metadata
    assert card.imageFile == test_image
    assert card.created == test_created
    assert card.updated == test_updated


def test_json_round_trip():
    """Test Card serialization → deserialization round trip."""
    # Create an original card
    orig_card = Card(
        uuid=str(uuid.uuid4()),
        title="Round Trip Card",
        metadata={"a": 1, "b": "test", "c": True},
        imageFile="image.png",
        created=datetime.now().isoformat(),
        updated=datetime.now().isoformat()
    )
    
    # Serialize to JSON
    json_data = orig_card.to_json()
    
    # Deserialize back to a Card
    restored_card = Card.from_json(json_data)
    
    # Cards should be equal in all fields
    assert restored_card.uuid == orig_card.uuid
    assert restored_card.title == orig_card.title
    assert restored_card.metadata == orig_card.metadata
    assert restored_card.imageFile == orig_card.imageFile
    assert restored_card.created == orig_card.created
    assert restored_card.updated == orig_card.updated
