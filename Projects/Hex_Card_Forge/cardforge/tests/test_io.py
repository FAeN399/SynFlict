"""
Tests for import/export functionality
"""

import os
import uuid
import tempfile
import zipfile
import json
from datetime import datetime
import pytest
from pathlib import Path

from cardforge.models import Card
from cardforge.io import export_card, import_card


def test_export_card_without_image():
    """Test exporting a Card without an image to a ZIP file.
    
    Verify that a ZIP named card_<uuid>.zip is created containing just the JSON file.
    """
    # Create a test card without an image
    test_uuid = str(uuid.uuid4())
    test_card = Card(
        uuid=test_uuid,
        title="Export Test Card",
        metadata={"test": "value"},
        created=datetime.now().isoformat(),
        updated=datetime.now().isoformat(),
        imageFile=None
    )
    
    # Create a temp directory for our test exports
    with tempfile.TemporaryDirectory() as temp_dir:
        # Call the export function (which doesn't exist yet)
        zip_path = export_card(test_card, temp_dir)
        
        # Check that the ZIP file was created with expected name
        expected_zip_name = f"card_{test_uuid}.zip"
        expected_zip_path = Path(temp_dir) / expected_zip_name
        
        assert zip_path == str(expected_zip_path)
        assert os.path.exists(zip_path)
        
        # Check the contents of the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # List all files in the ZIP
            file_list = zip_file.namelist()
            
            # There should be exactly one file (the JSON)
            assert len(file_list) == 1
            
            # The JSON file should be named correctly
            json_filename = f"card_{test_uuid}.json"
            assert json_filename in file_list
            
            # Extract and verify the JSON content
            with zip_file.open(json_filename) as json_file:
                content = json_file.read().decode('utf-8')
                card_data = json.loads(content)
                
                assert card_data["uuid"] == test_uuid
                assert card_data["title"] == "Export Test Card"
                assert card_data["metadata"] == {"test": "value"}
                assert card_data["imageFile"] is None


def test_export_card_with_image():
    """Test exporting a Card with an image to a ZIP file.
    
    This test is meant to fail initially as we're focusing first on cards without images.
    It will be implemented in a later step.
    """
    # This test will be properly implemented in a future step
    pass


def test_import_card():
    """Test importing a Card from a ZIP file.
    
    Export a card, import it back, and verify that the imported card is identical to the original.
    """
    # Create a test card
    test_uuid = str(uuid.uuid4())
    original_card = Card(
        uuid=test_uuid,
        title="Import Test Card",
        metadata={"key1": "value1", "key2": 42},
        created=datetime.now().isoformat(),
        updated=datetime.now().isoformat(),
    )
    
    # Create a temp directory for our test exports/imports
    with tempfile.TemporaryDirectory() as temp_dir:
        # Export the card
        zip_path = export_card(original_card, temp_dir)
        
        # Import the card back (function to be implemented)
        imported_card = import_card(zip_path)
        
        # Verify the imported card matches the original
        assert imported_card.uuid == original_card.uuid
        assert imported_card.title == original_card.title
        assert imported_card.metadata == original_card.metadata
        assert imported_card.created == original_card.created
        assert imported_card.updated == original_card.updated
        assert imported_card.imageFile == original_card.imageFile
