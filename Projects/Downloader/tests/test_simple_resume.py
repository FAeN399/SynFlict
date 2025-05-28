"""
Simplified test for resumable sync functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os

import pytest

from grabber.database import Database
from grabber.search import SearchParams


class TestSimpleResume(unittest.TestCase):
    """Simple test for resumable sync functionality."""
    
    def setUp(self):
        """Set up a temporary database for testing."""
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        self.db = Database(self.temp_db_path)
        self.db.initialize()
        
        # Create test data - mark first 5 posts as downloaded
        for i in range(5):
            post_id = f"post{i}"
            permalink = f"/r/test/comments/{post_id}/test/"
            self.db.add_post(post_id, permalink)
            self.db.mark_post_downloaded(post_id)
    
    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.close(self.temp_db_fd)
        os.unlink(self.temp_db_path)
    
    def test_simple_resume(self):
        """Test simple resumable sync with explicit mock data."""
        from grabber.sync import sync_with_resume
        
        # Create a list to track processed submissions
        processed_ids = []
        
        # Define process function
        def process_submission(submission, db):
            processed_ids.append(submission.id)
            db.mark_post_downloaded(submission.id)
            return True
        
        # Create 10 mock submissions - 5 already processed, 5 new
        all_submissions = []
        for i in range(10):
            mock_sub = MagicMock()
            mock_sub.id = f"post{i}"
            mock_sub.permalink = f"/r/test/comments/post{i}/test/"
            all_submissions.append(mock_sub)
        
        # Run sync with resume=True
        with patch('grabber.sync.fetch_iter', return_value=iter(all_submissions)):
            sync_with_resume(
                "test", 
                SearchParams(limit=10), 
                self.db,
                process_func=process_submission, 
                resume=True
            )
        
        # Verify only the second 5 submissions were processed
        self.assertEqual(len(processed_ids), 5)
        expected_ids = [f"post{i}" for i in range(5, 10)]
        self.assertEqual(processed_ids, expected_ids)


if __name__ == "__main__":
    unittest.main()
