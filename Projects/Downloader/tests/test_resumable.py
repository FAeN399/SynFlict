"""
Tests for the resumable sync functionality.
"""

import unittest
from unittest.mock import patch, MagicMock, call
import tempfile
import os

import pytest

from grabber.database import Database
from grabber.search import SearchParams


class TestResumable(unittest.TestCase):
    """Test the resumable sync functionality."""
    
    def setUp(self):
        """Set up temporary database and mocks for testing."""
        # Create a temporary file for the database
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        
        # Initialize the database
        self.db = Database(self.temp_db_path)
        self.db.initialize()
        
        # Create some test data
        for i in range(10):
            post_id = f"post{i}"
            permalink = f"/r/test/comments/{post_id}/test_post/"
            self.db.add_post(post_id, permalink)
            
            # Mark every other post as downloaded
            if i % 2 == 0:
                self.db.mark_post_downloaded(post_id)
    
    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.close(self.temp_db_fd)
        os.unlink(self.temp_db_path)
    
    def test_resume_from_checkpoint(self):
        """Test resuming sync from a checkpoint."""
        from grabber.sync import sync_with_resume
        
        # Create search parameters
        params = SearchParams(limit=10)
        
        # Process the first 5 submissions manually to simulate the first run
        for i in range(5):
            post_id = f"post{i}"
            permalink = f"/r/test/comments/{post_id}/test_post/"
            self.db.add_post(post_id, permalink)
            self.db.mark_post_downloaded(post_id)
        
        # Set up a process function that will track processed submissions
        processed_ids = []
        def process_submission(submission, db):
            """Track which submissions are processed."""
            processed_ids.append(submission.id)
            db.add_post(submission.id, submission.permalink)
            db.mark_post_downloaded(submission.id)
            return True
        
        # Create mock submissions for the second half
        mock_submissions = []
        for i in range(5, 10):
            mock_sub = MagicMock()
            mock_sub.id = f"post{i}"
            mock_sub.title = f"Test Post {i}"
            mock_sub.permalink = f"/r/test/comments/post{i}/test_post/"
            mock_submissions.append(mock_sub)
        
        # Mock fetch_iter to return our test submissions
        with patch('grabber.sync.fetch_iter', return_value=iter(mock_submissions)):
            # Run the sync with resume=True
            sync_with_resume("test", params, self.db, process_func=process_submission, resume=True)
        
            # Check that the remaining 5 submissions were processed
            self.assertEqual(len(processed_ids), 5)
            
            # Check that the processed IDs are the ones we expect (should be the second half)
            expected_ids = [f"post{i}" for i in range(5, 10)]
            self.assertEqual(processed_ids, expected_ids)
    
    @patch('grabber.sync.fetch_iter')
    def test_skip_downloaded_submissions(self, mock_fetch_iter):
        """Test that downloaded submissions are skipped when resuming."""
        from grabber.sync import sync_with_resume
        
        # Create search parameters
        params = SearchParams(limit=10)
        
        # Mock submissions
        mock_submissions = []
        for i in range(10):
            mock_sub = MagicMock()
            mock_sub.id = f"post{i}"
            mock_sub.title = f"Test Post {i}"
            mock_submissions.append(mock_sub)
        
        # Set up fetch_iter to return the mock submissions
        mock_fetch_iter.return_value = iter(mock_submissions)
        
        # Set up a counter to track processed submissions
        processed_ids = []
        
        def process_submission(submission, db):
            """Simulates processing a submission."""
            processed_ids.append(submission.id)
            
            # Mark as downloaded
            db.mark_post_downloaded(submission.id)
            return True
        
        # Run the sync with skip_downloaded=True
        sync_with_resume("test", params, self.db, process_func=process_submission, skip_downloaded=True)
        
        # Should only process odd-indexed submissions since even ones are already marked as downloaded
        expected_ids = [f"post{i}" for i in range(10) if i % 2 != 0]
        self.assertEqual(processed_ids, expected_ids)


if __name__ == "__main__":
    unittest.main()
