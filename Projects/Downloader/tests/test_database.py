"""
Tests for the SQLite database functionality.
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import pathlib
import time

import pytest

from grabber.database import Database


class TestDatabase(unittest.TestCase):
    """Test the SQLite database functionality."""
    
    def setUp(self):
        """Set up a temporary database for testing."""
        # Create a temporary file for the database
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        
        # Initialize the database
        self.db = Database(self.temp_db_path)
        
        # Make sure tables are created
        self.db.initialize()
    
    def tearDown(self):
        """Clean up the temporary database."""
        # Close the database connection
        self.db.close()
        
        # Close and remove the temporary file
        os.close(self.temp_db_fd)
        os.unlink(self.temp_db_path)
    
    def test_initialize_creates_tables(self):
        """Test that initializing the database creates the necessary tables."""
        # Check that the tables exist
        cursor = self.db.conn.cursor()
        
        # Check files table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check posts table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
        self.assertIsNotNone(cursor.fetchone())
    
    def test_file_operations(self):
        """Test adding and checking file hashes."""
        # Add a file
        self.db.add_file_hash("abc123", "/path/to/file.jpg")
        
        # Check if the file exists
        self.assertTrue(self.db.has_file_hash("abc123"))
        
        # Check that a non-existent file doesn't exist
        self.assertFalse(self.db.has_file_hash("nonexistent"))
        
        # Get the file path
        path = self.db.get_file_path("abc123")
        self.assertEqual(path, "/path/to/file.jpg")
    
    def test_post_operations(self):
        """Test adding and checking post information."""
        # Add a post
        post_id = "abc123"
        permalink = "/r/test/comments/abc123/test_post/"
        self.db.add_post(post_id, permalink)
        
        # Check if the post exists
        self.assertTrue(self.db.has_post(post_id))
        
        # Mark the post as downloaded
        self.db.mark_post_downloaded(post_id)
        
        # Check if the post is marked as downloaded
        downloaded = self.db.is_post_downloaded(post_id)
        self.assertTrue(downloaded)
        
        # Update last check time
        self.db.update_post_check_time(post_id)
        
        # Check that a non-existent post doesn't exist
        self.assertFalse(self.db.has_post("nonexistent"))
    
    def test_duplicate_file_prevention(self):
        """Test that the same hash can't be added twice."""
        # Add a file
        self.db.add_file_hash("abc123", "/path/to/file1.jpg")
        
        # Try to add a different file with the same hash
        self.db.add_file_hash("abc123", "/path/to/file2.jpg")
        
        # Check that the path is still the original
        path = self.db.get_file_path("abc123")
        self.assertEqual(path, "/path/to/file1.jpg")
    
    def test_vacuum(self):
        """Test the vacuum operation."""
        # Add a bunch of files and posts
        for i in range(10):
            self.db.add_file_hash(f"hash{i}", f"/path/to/file{i}.jpg")
            self.db.add_post(f"post{i}", f"/r/test/comments/post{i}/test_post/")
        
        # Vacuum the database
        self.db.vacuum()
        
        # Just ensure it doesn't raise an exception
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
