"""
Tests for the CLI module
"""

import pytest
from cardforge.cli import hello_world


def test_hello_world():
    """Test the hello_world function returns the expected greeting."""
    expected = "Hello, Card Forge!"
    result = hello_world()
    assert result == expected, f"Expected '{expected}', but got '{result}'"
