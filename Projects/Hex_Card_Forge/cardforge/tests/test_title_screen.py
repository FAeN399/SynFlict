"""
Tests for the title screen navigation
"""

import re
import pytest
from typer.testing import CliRunner

from cardforge.cli import app


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_title_screen_menu_options(runner):
    """Test that the title screen displays all required menu options.
    
    Should show 5 main options as specified in FR-1:
    1. Create New Card
    2. Import Cards
    3. Create Booster Pack
    4. Design Card Template
    5. Add Image to Card
    """
    result = runner.invoke(app)
    
    # Check that the command ran successfully
    assert result.exit_code == 0
    
    # Check for the title
    assert "CARD FORGE" in result.stdout
    
    # Check for all 5 menu options from FR-1
    required_options = [
        "Create New Card",
        "Import Cards", 
        "Create Booster Pack", 
        "Design Template", 
        "Add Image to Card"
    ]
    
    for option in required_options:
        assert option in result.stdout, f"Missing menu option: {option}"
    
    # Check that the options are numbered 1-5
    for i, option in enumerate(required_options, 1):
        pattern = rf"{i}\.\s+{option}"
        assert re.search(pattern, result.stdout), f"Option {i} not properly formatted: {option}"
    
    # Check for exit option
    assert "Exit" in result.stdout or "Quit" in result.stdout
