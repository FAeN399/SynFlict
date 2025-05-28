"""
Rate Limiter module for Reddit Grabber.

This module handles dynamic throttling based on Reddit API response headers
to prevent exceeding rate limits and avoid temporary bans.
"""

import asyncio
import logging
import time
from typing import Dict, Mapping, Optional, Union, Tuple

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Dynamically throttles API requests based on Reddit API rate limit headers.
    
    Monitors X-Ratelimit-* headers from Reddit API responses and adjusts
    request timing to stay within safe limits.
    """
    
    def __init__(self, 
                 safe_margin: float = 0.8, 
                 min_rps_threshold: float = 1.0,
                 fallback_max_rpm: int = 60):
        """
        Initialize a new RateLimiter.
        
        Args:
            safe_margin: Percentage (0.0-1.0) of allowed RPS to target (default: 0.8 or 80%)
            min_rps_threshold: When remaining/reset drops below this value, throttling activates
            fallback_max_rpm: Maximum requests per minute when headers are missing
        """
        self.safe_margin = max(0.1, min(safe_margin, 0.95))  # Clamp between 10-95%
        self.min_rps_threshold = max(0.1, min_rps_threshold)
        self.fallback_max_rpm = max(1, fallback_max_rpm)
        
        # State tracking
        self._used: Optional[int] = None
        self._remaining: Optional[int] = None
        self._reset_seconds: Optional[int] = None
        self._last_header_time = 0.0
        self._missing_headers_count = 0
        self._max_sleep_warning_threshold = 5.0  # Log warning when sleep ≥ this many seconds
        
    def update_from_headers(self, headers: Mapping[str, str]) -> None:
        """
        Update rate limit state from Reddit API response headers.
        
        Args:
            headers: Dictionary-like object containing HTTP response headers
        """
        now = time.time()
        self._last_header_time = now
        
        # Extract relevant headers (case-insensitive lookup)
        header_map = {k.lower(): v for k, v in headers.items()}
        
        try:
            self._used = int(header_map.get('x-ratelimit-used', '0'))
            self._remaining = int(header_map.get('x-ratelimit-remaining', '0'))
            self._reset_seconds = int(header_map.get('x-ratelimit-reset', '0'))
            self._missing_headers_count = 0
            
            logger.debug(
                f"Rate limit update: {self._remaining}/{self._used + self._remaining} "
                f"requests remaining (resets in {self._reset_seconds}s)"
            )
        except (ValueError, TypeError):
            # Headers missing or invalid
            self._missing_headers_count += 1
            
            if self._missing_headers_count >= 10:
                logger.warning(
                    f"Missing rate limit headers for {self._missing_headers_count} "
                    f"consecutive requests, using fallback limit of {self.fallback_max_rpm} req/min"
                )
    
    def _calculate_sleep_time(self) -> Tuple[float, str]:
        """
        Calculate how long to sleep before the next request.
        
        Returns:
            Tuple of (sleep_seconds, reason_message)
        """
        # Case 1: No headers received yet or reset happened
        if self._remaining is None or self._reset_seconds is None:
            # Fallback to fixed rate: convert RPM to seconds per request
            sleep_time = 60.0 / self.fallback_max_rpm
            return sleep_time, "fallback rate limiting"
            
        # Case 2: Reset window is about to expire, no need to throttle
        if self._reset_seconds < 2:
            return 0, "reset window expiring"
            
        # Case 3: Plenty of requests remaining, no throttling needed
        if self._remaining > self._reset_seconds * self.min_rps_threshold * 1.5:
            return 0, "sufficient request allowance"
            
        # Case 4: Need to throttle to stay within rate limits
        if self._remaining > 0 and self._reset_seconds > 0:
            # Calculate safe requests per second
            safe_rps = (self._remaining / self._reset_seconds) * self.safe_margin
            
            # If we're below threshold, calculate sleep time to maintain safe rate
            if safe_rps < self.min_rps_threshold:
                sleep_time = 1.0 / safe_rps if safe_rps > 0 else self._reset_seconds
                # Cap maximum sleep to reset time
                sleep_time = min(sleep_time, self._reset_seconds)
                return sleep_time, f"throttling to {safe_rps:.2f} req/sec"
        
        # Case 5: Almost out of requests, need to wait until reset
        if self._remaining <= 2:
            # Sleep until reset, leaving a small buffer
            return max(1, self._reset_seconds - 1), "waiting for rate limit reset"
            
        return 0, "no throttling needed"
    
    def sleep(self) -> None:
        """
        Blocks the current thread to maintain a safe request rate.
        """
        sleep_time, reason = self._calculate_sleep_time()
        
        if sleep_time > 0:
            if sleep_time >= self._max_sleep_warning_threshold:
                logger.warning(f"Rate limit sleep: {sleep_time:.1f}s ({reason})")
            else:
                logger.debug(f"Rate limit sleep: {sleep_time:.1f}s ({reason})")
                
            time.sleep(sleep_time)
    
    async def wait(self) -> None:
        """
        Asynchronous version of sleep() for use in async code.
        """
        sleep_time, reason = self._calculate_sleep_time()
        
        if sleep_time > 0:
            if sleep_time >= self._max_sleep_warning_threshold:
                logger.warning(f"Rate limit wait: {sleep_time:.1f}s ({reason})")
            else:
                logger.debug(f"Rate limit wait: {sleep_time:.1f}s ({reason})")
                
            await asyncio.sleep(sleep_time)
    
    def snapshot(self) -> Dict[str, Union[int, float, None]]:
        """
        Return the current rate limit state for UI display.
        
        Returns:
            Dictionary with current rate limit information
        """
        return {
            "used": self._used,
            "remaining": self._remaining,
            "reset_seconds": self._reset_seconds,
            "last_updated": self._last_header_time,
            "missing_headers_count": self._missing_headers_count,
        }
