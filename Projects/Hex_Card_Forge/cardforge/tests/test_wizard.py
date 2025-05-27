"""
Tests for the wizard flow
"""

import io
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import uuid

from cardforge.wizard import create_new_card
from cardforge.models import Card


@pytest.fixture
def mock_uuid():
    # Create a fixed UUID for testing
    fixed_uuid = "12345678-1234-5678-1234-567812345678"
    with patch('uuid.uuid4', return_value=uuid.UUID(fixed_uuid)):
        yield fixed_uuid


@pytest.fixture
def mock_datetime():
    # Create a fixed datetime for testing
    fixed_datetime = "2025-05-27T12:34:56"
    mock_dt = MagicMock()
    mock_dt.isoformat.return_value = fixed_datetime
    with patch('datetime.datetime', MagicMock()) as dt_mock:
        dt_mock.now.return_value = mock_dt
        dt_mock.isoformat.return_value = fixed_datetime
        yield fixed_datetime


def test_create_new_card_basic_flow(mock_uuid):
    """Test basic flow of create_new_card with mocked input/output."""
    # Mock input values
    input_values = [
        "Test Card Title",      # Card title
        "category=creature",     # First metadata field
        "power=5",              # Second metadata field
        "",                     # End metadata input
        "n",                    # Don't attach image
        "y",                    # Confirm card
        "n"                     # Don't create another
    ]
    
    # Run the wizard with mocked input/output
    with patch('builtins.input', side_effect=input_values):
        # Capture print output to a string instead of mock function
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            # Override print_func to use the mock stdout
            def print_to_stdout(text):
                print(text)  # This will go to our mock stdout
            
            card, create_another = create_new_card(
                input_func=lambda prompt: input(prompt),
                print_func=print_to_stdout
            )
            
            # Capture what was printed
            output = mock_stdout.getvalue()
    
    # Verify the card was created correctly
    assert card is not None
    assert card.uuid == mock_uuid
    assert card.title == "Test Card Title"
    assert card.metadata == {"category": "creature", "power": 5}
    assert card.imageFile is None
    
    # Verify create_another flag is correct
    assert create_another is False


def test_create_new_card_type_conversion():
    """Test that the wizard properly converts input types."""
    # Test numeric and boolean conversions
    input_values = [
        "Type Test Card",        # Card title
        "int_value=42",         # Integer
        "float_value=3.14",     # Float
        "bool_value=true",       # Boolean true
        "string_value=hello",    # String
        "",                     # End metadata input
        "n",                    # Don't attach image
        "y",                    # Confirm card
        "n"                     # Don't create another
    ]
    
    # Run the wizard with mocked input/output
    with patch('builtins.input', side_effect=input_values):
        card, _ = create_new_card(
            input_func=lambda prompt: input(prompt),
            print_func=lambda text: None  # Discard output
        )
    
    # Verify type conversions
    assert isinstance(card.metadata["int_value"], int)
    assert card.metadata["int_value"] == 42
    
    assert isinstance(card.metadata["float_value"], float)
    assert card.metadata["float_value"] == 3.14
    
    assert isinstance(card.metadata["bool_value"], bool)
    assert card.metadata["bool_value"] is True
    
    assert isinstance(card.metadata["string_value"], str)
    assert card.metadata["string_value"] == "hello"
