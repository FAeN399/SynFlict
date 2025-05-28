"""
Tests for the configuration loading functionality.
"""

import os
import unittest
from unittest.mock import patch
import tempfile
import pathlib

import pytest

from grabber.config import load_config


class TestConfig(unittest.TestCase):
    """Test configuration loading and precedence."""
    
    def setUp(self):
        """Set up environment for each test."""
        # Clear any existing environment variables that might affect tests
        for key in list(os.environ.keys()):
            if key.startswith("GRABBER_") or key.startswith("REDDIT_"):
                del os.environ[key]
    
    def tearDown(self):
        """Clean up after each test."""
        # Clear any environment variables we set during tests
        for key in list(os.environ.keys()):
            if key.startswith("GRABBER_") or key.startswith("REDDIT_"):
                del os.environ[key]
    
    @patch.dict(os.environ, {
        "GRABBER_OUTPUT_DIR": "/env/output",
        "GRABBER_MAX_RPS": "5.5",
        "REDDIT_CLIENT_ID": "env_client_id",
        "REDDIT_CLIENT_SECRET": "env_client_secret",
        "REDDIT_USER_AGENT": "env_user_agent"
    })
    def test_env_vars_loaded(self):
        """Test that environment variables are correctly loaded."""
        config = load_config()
        
        # Check that environment variables were loaded
        self.assertEqual(config["output_dir"], "/env/output")
        self.assertEqual(config["max_rps"], 5.5)  # Should be converted to float
        self.assertEqual(config["reddit_client_id"], "env_client_id")
        self.assertEqual(config["reddit_client_secret"], "env_client_secret")
        self.assertEqual(config["reddit_user_agent"], "env_user_agent")
    
    def test_cli_args_override_env_vars(self):
        """Test that CLI arguments override environment variables."""
        # Set environment variables
        os.environ["GRABBER_OUTPUT_DIR"] = "/env/output"
        os.environ["GRABBER_MAX_RPS"] = "5.5"
        
        # Create CLI args that should override env vars
        cli_args = {
            "output_dir": "/cli/output",
            "max_rps": 10.0
        }
        
        config = load_config(cli_args=cli_args)
        
        # CLI args should take precedence
        self.assertEqual(config["output_dir"], "/cli/output")
        self.assertEqual(config["max_rps"], 10.0)
        
        # Other env vars should still be loaded
        if "REDDIT_CLIENT_ID" in os.environ:
            self.assertEqual(config["reddit_client_id"], os.environ["REDDIT_CLIENT_ID"])
    
    def test_config_file_fallback(self):
        """Test loading from config file when no env vars or CLI args."""
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.toml', delete=False) as tmp:
            tmp.write("""
            [grabber]
            output_dir = "/config/output"
            max_rps = 3.3
            
            [reddit]
            client_id = "config_client_id"
            client_secret = "config_client_secret"
            user_agent = "config_user_agent"
            """)
            tmp_path = tmp.name
        
        try:
            # Load config with the temp file path
            config = load_config(config_file=pathlib.Path(tmp_path))
            
            # Check that config file values were loaded
            self.assertEqual(config["output_dir"], "/config/output")
            self.assertEqual(config["max_rps"], 3.3)
            self.assertEqual(config["reddit_client_id"], "config_client_id")
            self.assertEqual(config["reddit_client_secret"], "config_client_secret")
            self.assertEqual(config["reddit_user_agent"], "config_user_agent")
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)


if __name__ == "__main__":
    pytest.main(["-v", "test_config.py"])
