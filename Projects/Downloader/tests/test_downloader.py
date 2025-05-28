"""
Tests for the downloader module.
"""

import os
import pathlib
import unittest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import hashlib

import pytest
import requests

from grabber.downloader import (
    download_image, 
    download_video, 
    calculate_sha1,
    extract_media_urls,
    process_submission
)
from grabber.database import Database


class TestDownloader(unittest.TestCase):
    """Test the downloader module functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for downloads
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = pathlib.Path(self.temp_dir.name)
        
        # Create a temporary database
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        self.db = Database(self.temp_db_path)
        self.db.initialize()
        
        # Mock Reddit submission
        self.mock_submission = MagicMock()
        self.mock_submission.id = "test1234"
        self.mock_submission.url = "https://example.com/image.jpg"
        self.mock_submission.permalink = "/r/test/comments/test1234/test_post/"
        self.mock_submission.title = "Test Post"
        self.mock_submission.author = MagicMock()
        self.mock_submission.author.name = "test_user"
        self.mock_submission.created_utc = 1609459200  # 2021-01-01
        self.mock_submission.subreddit = MagicMock()
        self.mock_submission.subreddit.display_name = "test"
        
    def tearDown(self):
        """Clean up temporary files."""
        self.temp_dir.cleanup()
        self.db.close()
        os.close(self.temp_db_fd)
        os.unlink(self.temp_db_path)
    
    @patch('requests.get')
    def test_download_image(self, mock_get):
        """Test downloading an image."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'test_image_data'
        mock_get.return_value = mock_response
        
        # Test the function
        url = "https://example.com/image.jpg"
        output_path = self.output_dir / "test_image.jpg"
        
        result = download_image(url, output_path)
        
        # Verify the function called requests.get with the correct URL
        mock_get.assert_called_once_with(url, timeout=30)
        
        # Verify the file was saved correctly
        self.assertTrue(output_path.exists())
        with open(output_path, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'test_image_data')
        
        # Verify the function returned True
        self.assertTrue(result)
    
    @patch('subprocess.run')
    def test_download_video(self, mock_run):
        """Test downloading a video using yt-dlp."""
        # Set up the mock subprocess.run
        mock_run.return_value = MagicMock()
        mock_run.return_value.returncode = 0
        
        # Test the function
        url = "https://v.redd.it/testvideo"
        output_dir = self.output_dir
        
        result = download_video(url, output_dir)
        
        # Verify the function called subprocess.run with yt-dlp
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertIn('yt-dlp', args)
        self.assertIn(url, args)
        
        # Verify the function returned True
        self.assertTrue(result)
    
    def test_calculate_sha1(self):
        """Test SHA1 calculation."""
        # Create a test file
        test_file = self.output_dir / "test_file.txt"
        with open(test_file, 'wb') as f:
            f.write(b'test data')
        
        # Calculate expected SHA1
        expected_sha1 = hashlib.sha1(b'test data').hexdigest()
        
        # Test the function
        result = calculate_sha1(test_file)
        
        # Verify the result
        self.assertEqual(result, expected_sha1)
    
    def test_extract_media_urls_from_image_post(self):
        """Test extracting media URLs from an image post."""
        # Set up a mock submission with a direct image URL
        submission = MagicMock()
        submission.url = "https://i.imgur.com/abcdef.jpg"
        submission.is_self = False
        
        # Test the function
        urls = extract_media_urls(submission)
        
        # Verify we got the expected URL
        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0], "https://i.imgur.com/abcdef.jpg")
    
    def test_extract_media_urls_from_gallery(self):
        """Test extracting media URLs from a gallery post."""
        # Set up a mock submission with a gallery
        submission = MagicMock()
        submission.url = "https://www.reddit.com/gallery/abcdef"
        submission.is_self = False
        
        # Mock the media_metadata attribute
        media_metadata = {
            "item1": {"s": {"u": "https://i.redd.it/image1.jpg"}},
            "item2": {"s": {"u": "https://i.redd.it/image2.jpg"}}
        }
        # Use property mock to handle the attribute access
        submission.media_metadata = media_metadata
        
        # Test the function
        urls = extract_media_urls(submission)
        
        # Verify we got the expected URLs
        self.assertEqual(len(urls), 2)
        self.assertIn("https://i.redd.it/image1.jpg", urls)
        self.assertIn("https://i.redd.it/image2.jpg", urls)
    
    @patch('grabber.downloader.download_image')
    def test_process_submission(self, mock_download_image):
        """Test processing a submission."""
        # Set up the mock download_image
        mock_download_image.return_value = True
        
        # Set up a mock submission
        submission = self.mock_submission
        
        # Test the function
        result = process_submission(submission, self.db, self.output_dir)
        
        # Verify the download_image was called
        mock_download_image.assert_called_once()
        
        # Verify the function returned True
        self.assertTrue(result)
        
        # Verify the submission was marked as downloaded in the database
        self.assertTrue(self.db.is_post_downloaded(submission.id))


if __name__ == '__main__':
    unittest.main()
