import unittest
from types import SimpleNamespace

# Import the components we need to test
from grabber.test_mode import create_mock_submissions
from grabber.global_search import GlobalRedditSearch


class TestNSFWFiltering(unittest.TestCase):
    """Test cases for NSFW content filtering"""
    
    def setUp(self):
        # Create a mock Reddit instance
        self.mock_reddit = SimpleNamespace()
        
        # Create our search instance
        self.search = GlobalRedditSearch(self.mock_reddit)
    
    def test_only_nsfw_returns_nsfw(self):
        """Test that only_nsfw=True returns only NSFW content"""
        # Create test submissions with 40% NSFW content
        subs = create_mock_submissions(count=20, nsfw_ratio=0.40)
        
        # Filter using the helper method
        results = [sub for sub in subs if self.search._passes_nsfw_filter(
            sub, allow_nsfw=True, only_nsfw=True
        )]
        
        # Assertions
        self.assertTrue(len(results) > 0, "No results returned in ONLY-NSFW mode")
        self.assertTrue(all(sub.over_18 for sub in results), 
                      "Non-NSFW content slipped through the ONLY-NSFW filter")
    
    def test_sfw_only_blocks_nsfw(self):
        """Test that allow_nsfw=False blocks all NSFW content"""
        # Create test submissions with 40% NSFW content
        subs = create_mock_submissions(count=20, nsfw_ratio=0.40)
        
        # Filter using the helper method
        results = [sub for sub in subs if self.search._passes_nsfw_filter(
            sub, allow_nsfw=False, only_nsfw=False
        )]
        
        # Assertions
        self.assertTrue(len(results) > 0, "No SFW results returned")
        self.assertFalse(any(sub.over_18 for sub in results), 
                       "NSFW content not filtered out in SFW-only mode")
    
    def test_allow_nsfw_includes_both(self):
        """Test that allow_nsfw=True, only_nsfw=False includes both SFW and NSFW content"""
        # Create test submissions with 40% NSFW content
        subs = create_mock_submissions(count=20, nsfw_ratio=0.40)
        
        # Filter using the helper method
        results = [sub for sub in subs if self.search._passes_nsfw_filter(
            sub, allow_nsfw=True, only_nsfw=False
        )]
        
        # Assertions
        self.assertTrue(len(results) > 0, "No results returned")
        nsfw_count = sum(1 for sub in results if sub.over_18)
        sfw_count = sum(1 for sub in results if not sub.over_18)
        self.assertTrue(nsfw_count > 0, "No NSFW content included")
        self.assertTrue(sfw_count > 0, "No SFW content included")


if __name__ == "__main__":
    unittest.main()
