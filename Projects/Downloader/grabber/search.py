"""
Search parameters and subreddit search functionality.

Handles parsing and validating search parameters, and provides utilities for
searching Reddit submissions based on those parameters.
"""

import argparse
import re
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Union

logger = logging.getLogger(__name__)


@dataclass
class SearchParams:
    """
    Represents search parameters for filtering Reddit submissions.
    """
    query: Optional[str] = None
    flair: Optional[str] = None
    since: Optional[str] = None
    until: Optional[str] = None
    min_score: Optional[int] = None
    media: Optional[str] = None
    user: Optional[List[str]] = None
    limit: int = 100
    allow_nsfw: bool = False
    pushshift: bool = False
    sort: str = "relevance"
    time_filter: str = "all"
    filter_func: Optional[callable] = None
    nsfw: bool = False
    
    @classmethod
    def parse_args(cls, args: List[str]) -> 'SearchParams':
        """
        Parse search parameters from command-line arguments.
        
        Args:
            args: List of command-line arguments
            
        Returns:
            SearchParams object with parsed parameters
            
        Raises:
            ValueError: If any parameter is invalid
        """
        parser = argparse.ArgumentParser(description="Search parameters for Reddit submissions")
        
        # Add arguments that match the SearchParams fields
        parser.add_argument("--query", type=str, help="Keyword search in title (AND-joined)")
        parser.add_argument("--flair", type=str, help="Include only posts whose flair matches regex")
        parser.add_argument("--since", type=str, help="ISO date or duration (3d, 6h) for oldest post")
        parser.add_argument("--until", type=str, help="ISO date or duration (3d, 6h) for newest post")
        parser.add_argument("--min-score", type=int, help="Skip submissions below Reddit score")
        parser.add_argument("--media", type=str, choices=["images", "videos", "all"], help="Filter by media type")
        parser.add_argument("--user", type=str, action="append", help="Only posts by specific author(s)")
        parser.add_argument("--limit", type=int, default=100, help="Max submissions fetched this run")
        parser.add_argument("--allow-nsfw", action="store_true", help="Explicitly permit NSFW content")
        parser.add_argument("--pushshift", action="store_true", help="Fall back to Pushshift API when Reddit search is throttled")
        
        # Parse args
        parsed_args = parser.parse_args(args)
        
        # Validate parameters
        cls._validate_parameters(parsed_args)
        
        # Process duration strings (e.g., '3d', '6h')
        parsed_args.since = cls._process_duration(parsed_args.since)
        parsed_args.until = cls._process_duration(parsed_args.until)
        
        # Create and return SearchParams object
        return cls(
            query=parsed_args.query,
            flair=parsed_args.flair,
            since=parsed_args.since,
            until=parsed_args.until,
            min_score=parsed_args.min_score,
            media=parsed_args.media,
            user=parsed_args.user,
            limit=parsed_args.limit,
            allow_nsfw=parsed_args.allow_nsfw,
            pushshift=parsed_args.pushshift
        )
    
    @staticmethod
    def _validate_parameters(args: argparse.Namespace) -> None:
        """
        Validate search parameters.
        
        Args:
            args: Parsed arguments
            
        Raises:
            ValueError: If any parameter is invalid
        """
        # Validate min_score
        if args.min_score is not None and args.min_score < 0:
            raise ValueError("min_score must be non-negative")
        
        # Validate media
        if args.media and args.media not in ["images", "videos", "all"]:
            raise ValueError(f"Invalid media type: {args.media}. Must be one of: images, videos, all")
        
        # Validate date formats
        for date_arg in [args.since, args.until]:
            if date_arg and not SearchParams._is_valid_date_or_duration(date_arg):
                raise ValueError(f"Invalid date format: {date_arg}. Use ISO format (YYYY-MM-DD) or duration (e.g., 3d, 6h)")
    
    @staticmethod
    def _is_valid_date_or_duration(date_str: str) -> bool:
        """
        Check if a string is a valid date or duration format.
        
        Args:
            date_str: Date string to check
            
        Returns:
            True if the string is a valid date or duration, False otherwise
        """
        if not date_str:
            return True
        
        # Check for ISO date format (YYYY-MM-DD)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            pass
        
        # Check for duration format (e.g., 3d, 6h)
        duration_pattern = r'^\d+[dh]$'
        return bool(re.match(duration_pattern, date_str))
    
    @staticmethod
    def _process_duration(date_str: Optional[str]) -> Optional[str]:
        """
        Process a date string, converting durations to ISO date strings.
        
        Args:
            date_str: Date string to process
            
        Returns:
            Processed date string in ISO format (YYYY-MM-DD)
        """
        if not date_str:
            return None
        
        # Check if it's already an ISO date
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            pass
        
        # Process duration
        match = re.match(r'^(\d+)([dh])$', date_str)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            
            now = datetime.now()
            
            if unit == 'd':
                # Days
                target_date = now - timedelta(days=amount)
            elif unit == 'h':
                # Hours
                target_date = now - timedelta(hours=amount)
            else:
                # Shouldn't happen due to regex
                return None
            
            return target_date.strftime("%Y-%m-%d")
        
        return None


def get_reddit_client(user_auth: bool = True, mock: bool = False):
    """
    Get an authenticated Reddit API client.
    
    Args:
        user_auth: If True, use user authentication if available
        mock: If True, use a mock client for testing
    
    Returns:
        Authenticated PRAW Reddit instance or mock instance
    """
    from grabber.auth import get_reddit_instance
    
    # Check for mock mode from environment variable
    import os
    if os.environ.get("GRABBER_MOCK_MODE", "").lower() in ("true", "1", "yes"):
        mock = True
    
    try:
        # Get an authenticated Reddit instance
        return get_reddit_instance(user_auth=user_auth, mock=mock)
    except Exception as e:
        if not mock:
            logger.error(f"Error getting Reddit client: {e}")
            logger.warning("Falling back to mock client for testing")
        
        # Fallback to mock for testing
        from unittest.mock import MagicMock
        mock_client = MagicMock()
        return mock_client


def fetch_iter(subreddit: str, params: SearchParams):
    """
    Iterate through submissions in a subreddit based on search parameters.
    
    Args:
        subreddit: Name of the subreddit to search
        params: Search parameters
        
    Yields:
        Reddit submissions matching the search parameters
    """
    logger.info(f"Searching r/{subreddit} with parameters: {params}")
    
    # Get Reddit client
    reddit = get_reddit_client()
    
    # Get subreddit
    subreddit_obj = reddit.subreddit(subreddit)
    
    # Determine sort method (default to new)
    # In the future, we could add a sort parameter to SearchParams
    submissions = subreddit_obj.new()
    
    # Counter for yielded submissions
    count = 0
    
    # Iterate through submissions
    for submission in submissions:
        # Check if we've reached the limit
        if count >= params.limit:
            break
        
        # Skip NSFW submissions unless allowed
        if submission.over_18 and not params.allow_nsfw:
            logger.debug(f"Skipping NSFW submission: {submission.id}")
            continue
        
        # Skip submissions with too low score
        if params.min_score is not None and submission.score < params.min_score:
            logger.debug(f"Skipping low-score submission: {submission.id} (score: {submission.score})")
            continue
        
        # Filter by flair if specified
        if params.flair is not None:
            flair_text = getattr(submission, 'link_flair_text', '')
            if flair_text is None:
                flair_text = ''
            if not re.search(params.flair, flair_text):
                logger.debug(f"Skipping submission with non-matching flair: {submission.id}")
                continue
        
        # Filter by user if specified
        if params.user is not None:
            author_name = submission.author.name if hasattr(submission.author, 'name') else str(submission.author)
            if author_name not in params.user:
                logger.debug(f"Skipping submission by non-matching author: {author_name}")
                continue
        
        # Filter by query if specified
        if params.query is not None:
            # Simple case-insensitive search in title
            if not re.search(params.query, submission.title, re.IGNORECASE):
                logger.debug(f"Skipping submission with non-matching title: {submission.id}")
                continue
        
        # If we get here, the submission passed all filters
        logger.debug(f"Yielding submission: {submission.id} (score: {submission.score})")
        count += 1
        yield submission
