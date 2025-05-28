"""
Tests for search parameters and subreddit search functionality.
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest
from freezegun import freeze_time

from grabber.search import SearchParams


class TestSearchParams(unittest.TestCase):
    """Test the SearchParams class for handling search parameters."""
    
    def test_parse_args_basic(self):
        """Test that basic search parameters are correctly parsed."""
        # Test with query and min_score
        args = ["--query", "corgi", "--min-score", "100"]
        params = SearchParams.parse_args(args)
        
        self.assertEqual(params.query, "corgi")
        self.assertEqual(params.min_score, 100)
        self.assertIsNone(params.flair)
        self.assertIsNone(params.since)
        self.assertIsNone(params.until)
        
    def test_parse_args_all_params(self):
        """Test that all search parameters are correctly parsed."""
        args = [
            "--query", "corgi beach",
            "--min-score", "100",
            "--flair", "(?i)OC",
            "--since", "2025-05-01",
            "--until", "2025-05-28",
            "--media", "images",
            "--user", "doge",
            "--limit", "50",
            "--allow-nsfw",
            "--pushshift"
        ]
        
        params = SearchParams.parse_args(args)
        
        self.assertEqual(params.query, "corgi beach")
        self.assertEqual(params.min_score, 100)
        self.assertEqual(params.flair, "(?i)OC")
        self.assertEqual(params.since, "2025-05-01")
        self.assertEqual(params.until, "2025-05-28")
        self.assertEqual(params.media, "images")
        self.assertEqual(params.user, ["doge"])
        self.assertEqual(params.limit, 50)
        self.assertTrue(params.allow_nsfw)
        self.assertTrue(params.pushshift)
    
    def test_duration_parsing(self):
        """Test parsing of duration strings (e.g., '3d', '6h')."""
        with freeze_time("2025-05-28 12:00:00"):
            # Setup reference time
            now = datetime.now()
            
            # Test days
            params = SearchParams.parse_args(["--since", "3d"])
            expected_date = (now - timedelta(days=3)).strftime("%Y-%m-%d")
            self.assertEqual(params.since, expected_date)
            
            # Test hours
            params = SearchParams.parse_args(["--since", "6h"])
            expected_date = (now - timedelta(hours=6)).strftime("%Y-%m-%d")
            self.assertEqual(params.since, expected_date)
    
    def test_multiple_users(self):
        """Test that multiple users can be specified."""
        args = ["--user", "doge", "--user", "cat"]
        params = SearchParams.parse_args(args)
        
        self.assertEqual(params.user, ["doge", "cat"])
    
    def test_validation(self):
        """Test that validation catches invalid parameters."""
        # Invalid media type
        args = ["--media", "invalid"]
        with self.assertRaises(ValueError):
            SearchParams.parse_args(args)
        
        # Invalid date format
        args = ["--since", "not-a-date"]
        with self.assertRaises(ValueError):
            SearchParams.parse_args(args)
        
        # Invalid min_score
        args = ["--min-score", "-10"]
        with self.assertRaises(ValueError):
            SearchParams.parse_args(args)


if __name__ == "__main__":
    unittest.main()
