"""
Basic tests for the RateLimiter class.
"""

import unittest
from unittest.mock import patch, MagicMock

import pytest

from grabber.ratelimit import RateLimiter


class TestRateLimiterBasic(unittest.TestCase):
    """Simple test suite for the RateLimiter class."""

    def setUp(self):
        """Set up a fresh RateLimiter instance for each test."""
        self.rate_limiter = RateLimiter()

    def test_update_from_headers(self):
        """Test that headers are correctly parsed and stored."""
        # Setup test headers
        headers = {
            "X-Ratelimit-Used": "100",
            "X-Ratelimit-Remaining": "500",
            "X-Ratelimit-Reset": "300"
        }

        # Update rate limiter with headers
        self.rate_limiter.update_from_headers(headers)

        # Check internal state via snapshot
        snapshot = self.rate_limiter.snapshot()
        self.assertEqual(snapshot["used"], 100)
        self.assertEqual(snapshot["remaining"], 500)
        self.assertEqual(snapshot["reset_seconds"], 300)


if __name__ == "__main__":
    unittest.main()
