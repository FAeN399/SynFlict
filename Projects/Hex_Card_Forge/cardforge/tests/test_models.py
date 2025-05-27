"""
Tests for the Card model
"""

import uuid
from datetime import datetime
import pytest

# Import the Card class that doesn't exist yet - this will fail initially
from cardforge.models import Card


def test_card_creation():
    """Test creating a Card with all required fields."""
    # Prepare test data
    test_uuid = str(uuid.uuid4())
    test_title = "Test Card"
    test_metadata = {"category": "creature", "power": 2, "toughness": 3}
    test_created = datetime.now().isoformat()
    test_updated = test_created
    
    # Create a card without image
    card = Card(
        uuid=test_uuid,
        title=test_title,
        metadata=test_metadata,
        created=test_created,
        updated=test_updated
    )
    
    # Assertions to test that the Card model works correctly
    assert card.uuid == test_uuid
    assert card.title == test_title
    assert card.metadata == test_metadata
    assert card.created == test_created
    assert card.updated == test_updated
    assert card.imageFile is None  # imageFile should be optional


def test_card_with_image():
    """Test creating a Card with an imageFile."""
    test_uuid = str(uuid.uuid4())
    test_image_file = "test_image.png"
    
    # Create a card with an image
    card = Card(
        uuid=test_uuid,
        title="Card with Image",
        metadata={},
        imageFile=test_image_file,
        created=datetime.now().isoformat(),
        updated=datetime.now().isoformat()
    )
    
    # Assert that the imageFile was stored correctly
    assert card.imageFile == test_image_file
