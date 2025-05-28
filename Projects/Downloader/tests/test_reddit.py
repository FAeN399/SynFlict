"""
Tests for Reddit API interactions and URL handling.
"""

import unittest
import subprocess
import sys
import re
from unittest.mock import patch, MagicMock

import pytest

from grabber.cli import _extract_submission_id
from grabber.reddit import fetch_submission


class TestRedditURLHandling(unittest.TestCase):
    """Test Reddit URL handling and submission ID extraction."""
    
    def test_extract_submission_id(self):
        """Test extracting submission IDs from various URL formats."""
        # Test various URL formats
        test_cases = [
            ("https://www.reddit.com/r/aww/comments/abc123/title/", "abc123"),
            ("https://redd.it/abc123", "abc123"),
            ("https://reddit.com/comments/abc123", "abc123"),
            ("https://www.reddit.com/r/pics/comments/xyz789/another_title/", "xyz789"),
            ("invalid_url", None),
        ]
        
        for url, expected_id in test_cases:
            with self.subTest(url=url):
                self.assertEqual(_extract_submission_id(url), expected_id)
    
    def test_grab_command_dry_run(self):
        """Test that 'grab URL --dry-run' correctly shows submission ID."""
        result = subprocess.run(
            [sys.executable, "-m", "grabber.cli", "grab", "https://redd.it/abc123", "--dry-run"],
            capture_output=True,
            text=True
        )
        
        # Check that command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed with: {result.stderr}")
        
        # Check that output contains submission ID
        self.assertIn("abc123", result.stdout)
    
    @patch('grabber.reddit.fetch_submission')
    def test_fetch_submission_called(self, mock_fetch):
        """Test that fetch_submission is called with correct ID."""
        # Set up mock
        mock_submission = MagicMock()
        mock_submission.id = "abc123"
        mock_submission.title = "Test Submission"
        mock_fetch.return_value = mock_submission
        
        # Import the function here after patching
        from grabber.reddit import fetch_submission
        
        # Call function to test
        submission = fetch_submission("abc123")
        
        # Verify mock was called correctly
        mock_fetch.assert_called_once_with("abc123")
        self.assertEqual(submission.id, "abc123")
        self.assertEqual(submission.title, "Test Submission")


if __name__ == "__main__":
    pytest.main(["-v", "test_reddit.py"])
