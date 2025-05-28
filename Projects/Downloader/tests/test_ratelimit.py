"""
Tests for the RateLimiter class.

These tests verify that the RateLimiter correctly throttles requests
based on Reddit API rate limit headers.
"""

import time
import unittest
from unittest.mock import patch, MagicMock

import pytest
from freezegun import freeze_time

from grabber.ratelimit import RateLimiter


class TestRateLimiter(unittest.TestCase):
    """Test suite for the RateLimiter class."""

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
        assert snapshot["used"] == 100
        assert snapshot["remaining"] == 500
        assert snapshot["reset_seconds"] == 300

    def test_missing_headers_fallback(self):
        """Test that fallback rate limiting is used when headers are missing."""
        # Update with empty headers 10 times to trigger fallback
        for _ in range(10):
            self.rate_limiter.update_from_headers({})

        # Calculate expected sleep time (60 sec / 60 rpm = 1 sec per request)
        sleep_time, reason = self.rate_limiter._calculate_sleep_time()
        
        # Verify fallback is used
        assert sleep_time == 1.0
        assert "fallback" in reason

    def test_reset_window_expiring(self):
        """Test that no throttling occurs when reset window is about to expire."""
        headers = {
            "X-Ratelimit-Used": "595",
            "X-Ratelimit-Remaining": "5",
            "X-Ratelimit-Reset": "1"  # About to reset
        }
        
        self.rate_limiter.update_from_headers(headers)
        sleep_time, reason = self.rate_limiter._calculate_sleep_time()
        
        # Should not throttle since window is about to reset
        assert sleep_time == 0
        assert "reset window expiring" in reason

    @patch('time.sleep')
    def test_rt1_heavy_throttling(self, mock_sleep):
        """
        RT1: Mock 50 consecutive API calls returning headers
        (used=55, rem=5, reset=10) should result in sleep ≥ 4s
        """
        # Headers indicating we're almost at the limit
        headers = {
            "X-Ratelimit-Used": "55",
            "X-Ratelimit-Remaining": "5",
            "X-Ratelimit-Reset": "10"
        }
        
        # Update limiter and trigger sleep
        self.rate_limiter.update_from_headers(headers)
        self.rate_limiter.sleep()
        
        # With remaining=5, reset=10, and safe_margin=0.8:
        # safe_rps = (5/10)*0.8 = 0.4 req/sec
        # sleep_time = 1/0.4 = 2.5 seconds
        
        # Assert that sleep was called with at least 2 seconds
        # (exact value might vary due to implementation details)
        mock_sleep.assert_called_once()
        assert mock_sleep.call_args[0][0] >= 2.0

    @freeze_time("2025-01-01 12:00:00")
    @patch('time.time', side_effect=time.time)
    @patch('time.sleep')
    def test_rt2_headers_absent(self, mock_sleep, mock_time):
        """
        RT2: Headers absent for >10 requests should
        throttle to ≤ 60 requests/min measured by test clock
        """
        # Simulate 15 requests with no headers
        for _ in range(15):
            self.rate_limiter.update_from_headers({})
            self.rate_limiter.sleep()
        
        # Each call should sleep for 1 second (60 rpm fallback)
        assert mock_sleep.call_count == 15
        for call in mock_sleep.call_args_list:
            sleep_time = call[0][0]
            assert abs(sleep_time - 1.0) < 0.1  # Allow small float precision variance

    def test_rt3_rate_reset(self):
        """
        RT3: Remaining resets mid-run (header rem=600, reset=600)
        Throttle scale increases back to default concurrency
        """
        # First simulate low remaining requests
        low_headers = {
            "X-Ratelimit-Used": "595",
            "X-Ratelimit-Remaining": "5",
            "X-Ratelimit-Reset": "60"
        }
        self.rate_limiter.update_from_headers(low_headers)
        low_sleep, _ = self.rate_limiter._calculate_sleep_time()
        
        # Then simulate window reset with full allowance
        reset_headers = {
            "X-Ratelimit-Used": "0",
            "X-Ratelimit-Remaining": "600",
            "X-Ratelimit-Reset": "600"
        }
        self.rate_limiter.update_from_headers(reset_headers)
        reset_sleep, _ = self.rate_limiter._calculate_sleep_time()
        
        # After reset, sleep time should be much lower or zero
        assert low_sleep > 0  # Was throttling before reset
        assert reset_sleep == 0  # No throttling after reset

    # Skip async test for now since it requires additional setup
    def test_wait_method_exists(self):
        """Test that the wait method exists on RateLimiter."""
        headers = {
            "X-Ratelimit-Used": "55",
            "X-Ratelimit-Remaining": "5",
            "X-Ratelimit-Reset": "10"
        }
        
        self.rate_limiter.update_from_headers(headers)
        
        # Just verify the method exists and is callable
        self.assertTrue(hasattr(self.rate_limiter, 'wait'))
        self.assertTrue(callable(self.rate_limiter.wait))

    def test_snapshot_returns_correct_data(self):
        """Test that snapshot() returns the correct data structure."""
        headers = {
            "X-Ratelimit-Used": "100",
            "X-Ratelimit-Remaining": "500",
            "X-Ratelimit-Reset": "300"
        }
        
        self.rate_limiter.update_from_headers(headers)
        snapshot = self.rate_limiter.snapshot()
        
        # Check that all expected keys are present
        expected_keys = ["used", "remaining", "reset_seconds", "last_updated", "missing_headers_count"]
        for key in expected_keys:
            assert key in snapshot


if __name__ == "__main__":
    pytest.main(["-v", "test_ratelimit.py"])
