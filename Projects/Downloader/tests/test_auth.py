"""
Tests for the authentication module.
"""

import os
import pathlib
import unittest
from unittest.mock import patch, MagicMock

import pytest

from grabber.auth import get_reddit_instance, save_credentials


class TestAuth(unittest.TestCase):
    """Test authentication functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create patch for environment variables
        self.env_patcher = patch.dict('os.environ', {
            'REDDIT_CLIENT_ID': 'test_client_id',
            'REDDIT_CLIENT_SECRET': 'test_client_secret',
            'REDDIT_USER_AGENT': 'test_user_agent',
            'REDDIT_USERNAME': 'test_username',
            'REDDIT_PASSWORD': 'test_password'
        })
        self.env_patcher.start()
        
        # Patch config directory path to use a temp path
        self.temp_config_dir = pathlib.Path('test_config_dir')
        self.path_patcher = patch('pathlib.Path.home', return_value=pathlib.Path('test_home'))
        self.path_patcher.start()
        
        # Patch the actual reddit instance creation
        self.praw_patcher = patch('praw.Reddit')
        self.mock_reddit = self.praw_patcher.start()
        
        # Configure mock Reddit instance
        self.mock_reddit_instance = MagicMock()
        self.mock_user = MagicMock()
        self.mock_user.name = 'test_username'
        self.mock_user.me.return_value = self.mock_user
        self.mock_reddit_instance.user = self.mock_user
        self.mock_reddit.return_value = self.mock_reddit_instance
    
    def tearDown(self):
        """Clean up test environment."""
        self.env_patcher.stop()
        self.path_patcher.stop()
        self.praw_patcher.stop()
        
        # Clean up any files created during testing
        config_file = pathlib.Path('test_home') / '.config' / 'reddit-grabber' / 'credentials.ini'
        if config_file.exists():
            config_file.unlink()
        
        # Remove the directory if it exists
        config_dir = config_file.parent
        if config_dir.exists():
            try:
                config_dir.rmdir()
            except:
                pass
    
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open')
    @patch('configparser.ConfigParser.write')
    def test_save_credentials(self, mock_write, mock_open, mock_mkdir):
        """Test saving credentials to a config file."""
        # Call the function
        save_credentials('test_client_id', 'test_client_secret', 'test_username')
        
        # Verify directory was created
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        
        # Verify file was opened for writing
        mock_open.assert_called_once()
        
        # Verify config was written
        mock_write.assert_called_once()
    
    def test_get_reddit_instance_app_only(self):
        """Test getting a Reddit instance with application-only auth."""
        # Call the function
        reddit = get_reddit_instance(user_auth=False)
        
        # Verify the Reddit instance was created with correct parameters
        self.mock_reddit.assert_called_once_with(
            client_id='test_client_id',
            client_secret='test_client_secret',
            user_agent='test_user_agent'
        )
        
        # Verify the instance is what we expect
        self.assertEqual(reddit, self.mock_reddit_instance)
    
    def test_get_reddit_instance_user_auth(self):
        """Test getting a Reddit instance with user authentication."""
        # Call the function
        reddit = get_reddit_instance(user_auth=True)
        
        # Verify the Reddit instance was created with correct parameters
        self.mock_reddit.assert_called_once_with(
            client_id='test_client_id',
            client_secret='test_client_secret',
            user_agent='test_user_agent',
            username='test_username',
            password='test_password'
        )
        
        # Verify the instance is what we expect
        self.assertEqual(reddit, self.mock_reddit_instance)


if __name__ == '__main__':
    unittest.main()
