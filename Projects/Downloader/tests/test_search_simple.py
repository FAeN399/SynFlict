"""
Simple tests for search parameters.
"""

import unittest

import pytest

from grabber.search import SearchParams


class TestSearchParamsSimple(unittest.TestCase):
    """Test basic functionality of the SearchParams class."""
    
    def test_basic_params(self):
        """Test creation of SearchParams with basic parameters."""
        params = SearchParams(
            query="corgi",
            min_score=100,
            limit=50
        )
        
        self.assertEqual(params.query, "corgi")
        self.assertEqual(params.min_score, 100)
        self.assertEqual(params.limit, 50)
        self.assertIsNone(params.flair)
        self.assertFalse(params.allow_nsfw)


if __name__ == "__main__":
    unittest.main()
