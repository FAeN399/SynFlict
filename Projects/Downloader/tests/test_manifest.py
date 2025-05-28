"""
Tests for the Manifest JSON generation and writing.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import pathlib

import pytest

from grabber.manifest import Manifest, write_manifest


class TestManifest(unittest.TestCase):
    """Test the Manifest functionality."""
    
    def test_manifest_dataclass(self):
        """Test that the Manifest dataclass can be created with required fields."""
        manifest = Manifest(
            id="abc123",
            subreddit="aww",
            title="Very smol corgi",
            author="u/doge",
            permalink="/r/aww/comments/abc123/very_smol_corgi/",
            utc_timestamp=1753123123,
            score=5321,
            flair="OC",
            downloaded=["corgi.jpg", "corgi_zoomies.mp4"]
        )
        
        # Check that the fields were set correctly
        self.assertEqual(manifest.id, "abc123")
        self.assertEqual(manifest.subreddit, "aww")
        self.assertEqual(manifest.title, "Very smol corgi")
        self.assertEqual(manifest.author, "u/doge")
        self.assertEqual(manifest.permalink, "/r/aww/comments/abc123/very_smol_corgi/")
        self.assertEqual(manifest.utc_timestamp, 1753123123)
        self.assertEqual(manifest.score, 5321)
        self.assertEqual(manifest.flair, "OC")
        self.assertEqual(manifest.downloaded, ["corgi.jpg", "corgi_zoomies.mp4"])
    
    def test_manifest_to_dict(self):
        """Test conversion of Manifest to dictionary."""
        manifest = Manifest(
            id="abc123",
            subreddit="aww",
            title="Very smol corgi",
            author="u/doge",
            permalink="/r/aww/comments/abc123/very_smol_corgi/",
            utc_timestamp=1753123123,
            score=5321,
            flair="OC",
            downloaded=["corgi.jpg", "corgi_zoomies.mp4"]
        )
        
        manifest_dict = manifest.to_dict()
        
        # Check that the dictionary has all required keys
        required_keys = [
            "id", "subreddit", "title", "author", "permalink", 
            "utc_timestamp", "score", "flair", "downloaded"
        ]
        for key in required_keys:
            self.assertIn(key, manifest_dict)
            
        # Check specific values
        self.assertEqual(manifest_dict["id"], "abc123")
        self.assertEqual(manifest_dict["downloaded"], ["corgi.jpg", "corgi_zoomies.mp4"])
    
    def test_write_manifest(self):
        """Test writing manifest to a file."""
        manifest = Manifest(
            id="abc123",
            subreddit="aww",
            title="Very smol corgi",
            author="u/doge",
            permalink="/r/aww/comments/abc123/very_smol_corgi/",
            utc_timestamp=1753123123,
            score=5321,
            flair="OC",
            downloaded=["corgi.jpg", "corgi_zoomies.mp4"]
        )
        
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = pathlib.Path(temp_dir)
            manifest_path = write_manifest(manifest, output_path)
            
            # Check that the manifest file was created
            self.assertTrue(manifest_path.exists())
            
            # Read the manifest file and check its contents
            with open(manifest_path, "r") as f:
                manifest_json = json.load(f)
            
            # Check that the JSON has all required keys
            required_keys = [
                "id", "subreddit", "title", "author", "permalink", 
                "utc_timestamp", "score", "flair", "downloaded"
            ]
            for key in required_keys:
                self.assertIn(key, manifest_json)
            
            # Check specific values
            self.assertEqual(manifest_json["id"], "abc123")
            self.assertEqual(manifest_json["downloaded"], ["corgi.jpg", "corgi_zoomies.mp4"])
    
    def test_manual_manifest_creation(self):
        """Test creating a manifest directly without using fetch_submission."""
        from grabber.manifest import Manifest
        
        # Create the manifest directly
        manifest = Manifest(
            id="abc123",
            subreddit="aww",
            title="Very smol corgi",
            author="u/doge",
            permalink="/r/aww/comments/abc123/very_smol_corgi/",
            utc_timestamp=1753123123,
            score=5321,
            flair="OC",
            downloaded=["corgi.jpg", "corgi_zoomies.mp4"]
        )
        
        # Check that the manifest was created correctly
        self.assertEqual(manifest.id, "abc123")
        self.assertEqual(manifest.title, "Very smol corgi")
        self.assertEqual(manifest.author, "u/doge")
        self.assertEqual(manifest.downloaded, ["corgi.jpg", "corgi_zoomies.mp4"])


if __name__ == "__main__":
    pytest.main(["-v", "test_manifest.py"])
