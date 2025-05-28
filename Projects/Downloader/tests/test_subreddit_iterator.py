"""
Tests for the subreddit iterator functionality.
"""

import unittest
from unittest.mock import patch, MagicMock

import pytest

from grabber.search import SearchParams, fetch_iter


class TestSubredditIterator(unittest.TestCase):
    """Test the subreddit iterator functionality."""
    
    @patch('grabber.search.get_reddit_client')
    def test_fetch_iter_respects_limit(self, mock_get_client):
        """Test that fetch_iter yields at most 'limit' submissions."""
        # Create mock submissions
        mock_submissions = []
        for i in range(10):
            mock_sub = MagicMock()
            mock_sub.id = f"id{i}"
            mock_sub.title = f"Title {i}"
            mock_sub.score = 100 + i
            mock_sub.subreddit.display_name = "testsubreddit"
            mock_sub.over_18 = False
            mock_submissions.append(mock_sub)
        
        # Set up mock Reddit client
        mock_client = MagicMock()
        mock_subreddit = MagicMock()
        mock_subreddit.new.return_value = mock_submissions
        mock_client.subreddit.return_value = mock_subreddit
        mock_get_client.return_value = mock_client
        
        # Create search parameters with limit=5
        params = SearchParams(limit=5)
        
        # Fetch submissions
        submissions = list(fetch_iter("testsubreddit", params))
        
        # Check that at most 5 submissions were returned
        self.assertEqual(len(submissions), 5)
    
    @patch('grabber.search.get_reddit_client')
    def test_fetch_iter_filters_nsfw(self, mock_get_client):
        """Test that fetch_iter filters NSFW submissions unless allow_nsfw is True."""
        # Create mock submissions (some NSFW)
        mock_submissions = []
        for i in range(10):
            mock_sub = MagicMock()
            mock_sub.id = f"id{i}"
            mock_sub.title = f"Title {i}"
            mock_sub.score = 100 + i
            mock_sub.subreddit.display_name = "testsubreddit"
            mock_sub.over_18 = (i % 2 == 0)  # Even IDs are NSFW
            mock_submissions.append(mock_sub)
        
        # Set up mock Reddit client
        mock_client = MagicMock()
        mock_subreddit = MagicMock()
        mock_subreddit.new.return_value = mock_submissions
        mock_client.subreddit.return_value = mock_subreddit
        mock_get_client.return_value = mock_client
        
        # Test with allow_nsfw=False (default)
        params = SearchParams(allow_nsfw=False)
        submissions = list(fetch_iter("testsubreddit", params))
        self.assertEqual(len(submissions), 5)  # Only non-NSFW submissions
        
        # Test with allow_nsfw=True
        params = SearchParams(allow_nsfw=True)
        submissions = list(fetch_iter("testsubreddit", params))
        self.assertEqual(len(submissions), 10)  # All submissions
    
    @patch('grabber.search.get_reddit_client')
    def test_fetch_iter_filters_by_score(self, mock_get_client):
        """Test that fetch_iter filters submissions by min_score."""
        # Create mock submissions with different scores
        mock_submissions = []
        for i in range(10):
            mock_sub = MagicMock()
            mock_sub.id = f"id{i}"
            mock_sub.title = f"Title {i}"
            mock_sub.score = 50 + (i * 20)  # Scores from 50 to 230
            mock_sub.subreddit.display_name = "testsubreddit"
            mock_sub.over_18 = False
            mock_submissions.append(mock_sub)
        
        # Set up mock Reddit client
        mock_client = MagicMock()
        mock_subreddit = MagicMock()
        mock_subreddit.new.return_value = mock_submissions
        mock_client.subreddit.return_value = mock_subreddit
        mock_get_client.return_value = mock_client
        
        # Test with min_score=150
        params = SearchParams(min_score=150)
        submissions = list(fetch_iter("testsubreddit", params))
        self.assertEqual(len(submissions), 5)  # Only submissions with score >= 150
        
        # Check that all returned submissions have score >= 150
        for sub in submissions:
            self.assertGreaterEqual(sub.score, 150)


if __name__ == "__main__":
    unittest.main()
