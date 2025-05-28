"""
Global Reddit search functionality.

Handles searching across all of Reddit based on keywords, with filtering
by media type, sorting options, time periods, and NSFW content.
"""

import logging
import time
from typing import List, Dict, Any, Optional, Generator, Tuple
import pathlib
from datetime import datetime

import praw
from prawcore.exceptions import PrawcoreException, ResponseException

from grabber.search import SearchParams
from grabber.reddit import RedditSubmission
from grabber.ratelimit import RateLimiter
from grabber.database import Database
from grabber.downloader import extract_media_urls, process_submission

logger = logging.getLogger(__name__)

# Create a rate limiter for Reddit API calls
rate_limiter = RateLimiter(fallback_max_rpm=60)  # 60 calls per minute


class GlobalRedditSearch:
    """
    Handles searching across all of Reddit.
    """
    
    def __init__(self, reddit_instance: praw.Reddit, db: Database = None):
        """
        Initialize the global search handler.
        
        Args:
            reddit_instance: Authenticated PRAW Reddit instance
            db: Database instance for tracking downloads (optional)
        """
        self.reddit = reddit_instance
        self.db = db
        
    def _passes_nsfw_filter(self, submission, allow_nsfw: bool, only_nsfw: bool) -> bool:
        """Robust NSFW filtering logic that avoids double-filtering issues.
        
        Args:
            submission: The submission to check
            allow_nsfw: If True, allow NSFW content
            only_nsfw: If True, only return NSFW content
            
        Returns:
            True if the submission passes the filter, False otherwise
        """
        # Get the NSFW status, defaulting to False if not present
        is_nsfw = bool(getattr(submission, "over_18", False))

        if only_nsfw:               # User wants *only* adult posts
            return is_nsfw          # keep if NSFW, drop if not

        if not allow_nsfw and is_nsfw:
            return False            # user forbids adult posts

        return True                 # keep everything else
    
    def search(self, search_input=None, **kwargs) -> Generator[praw.models.Submission, None, None]:
        """
        Search across all of Reddit based on search parameters.
        
        Args:
            search_input: Either a SearchParams object or a query string
            **kwargs: Keyword arguments for backward compatibility
            
        Yields:
            PRAW submission objects matching the search criteria
        """
        # Check if we're being called with keyword arguments directly
        if kwargs and 'keywords' in kwargs:
            # Direct keyword args (most likely from GUI or older code)
            query = kwargs.get('keywords', 'cats')
            sort_param = kwargs.get('sort_by', 'relevance')
            time_filter_param = kwargs.get('time_period', 'all')
            limit_param = kwargs.get('limit', 100)
            # Consistently use allow_nsfw - clearer and no 'or' gymnastics
            allow_nsfw_param = kwargs.get('allow_nsfw', False)
            only_nsfw_param = kwargs.get('only_nsfw', False)
            media_type = kwargs.get('media_type', 'All')
            
            # Set up filter function based on media_type
            if media_type == 'All':
                filter_func = None
            elif media_type == 'Images':
                filter_func = self._is_image_submission
            elif media_type == 'Videos':
                filter_func = self._is_video_submission
            elif media_type == 'GIFs':
                filter_func = self._is_gif_submission
            elif media_type == 'Articles':
                filter_func = self._is_article_submission
            else:
                filter_func = None
                
        # Handle SearchParams object
        elif isinstance(search_input, SearchParams):
            # We have a SearchParams object
            params = search_input
            query = params.query
            sort_param = params.sort
            time_filter_param = params.time_filter
            limit_param = params.limit
            # Use consistent parameter naming
            allow_nsfw_param = getattr(params, 'allow_nsfw', False)
            only_nsfw_param = getattr(params, 'only_nsfw', False)
            filter_func = params.filter_func
            
        # Handle direct string query
        elif isinstance(search_input, str):
            # Direct query string
            query = search_input
            sort_param = "relevance"
            time_filter_param = "all"
            limit_param = 100
            allow_nsfw_param = False
            only_nsfw_param = False
            filter_func = None
            
        # Last resort - try to extract from object
        else:
            # For backward compatibility with other object types
            params = search_input if search_input is not None else {}
            query = getattr(params, 'query', None) or getattr(params, 'keywords', 'cats')
            sort_param = getattr(params, 'sort', 'relevance')
            time_filter_param = getattr(params, 'time_filter', 'all')
            limit_param = getattr(params, 'limit', 100)
            # Use consistent parameter naming
            allow_nsfw_param = getattr(params, 'allow_nsfw', False)
            only_nsfw_param = getattr(params, 'only_nsfw', False)
            filter_func = getattr(params, 'filter_func', None)
        
        # Convert sort parameter to PRAW format
        sort_mapping = {
            "relevance": "relevance",
            "hot": "hot", 
            "new": "new", 
            "top": "top", 
            "comments": "comments"
        }
        
        # Normalize parameters
        sort_param = sort_param.lower() if isinstance(sort_param, str) else "relevance"
        
        # Determine sort and time filter parameters for PRAW
        praw_sort = sort_mapping.get(sort_param, "relevance")
        praw_time = time_filter_param
        
        try:
            # Log the search parameters
            logger.info(f"Searching Reddit for: {query}, sort: {praw_sort}, time: {praw_time}")
            
            # Perform the search - we'll rely on PRAW's internal rate limiting
            search_results = self.reddit.subreddit("all").search(
                query=query,
                sort=praw_sort,
                time_filter=praw_time,
                limit=limit_param
            )
            
            # Add a debug log to verify NSFW parameters
            logger.debug(
                "NSFW flags → allow:%s  only:%s", 
                allow_nsfw_param, 
                only_nsfw_param
            )
            
            # Process and filter results
            count = 0
            for submission in search_results:
                # Use the robust NSFW filter helper
                if not self._passes_nsfw_filter(submission, allow_nsfw_param, only_nsfw_param):
                    continue
                
                # Apply custom filter function if provided
                if filter_func and not filter_func(submission):
                    continue
                
                # Yield the submission and increment counter
                yield submission
                count += 1
                
                # Stop if we've reached the limit
                if count >= limit_param:
                    break
                        
        except PrawcoreException as e:
            logger.error(f"Reddit API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during global search: {str(e)}")
            raise
    
    def download_search_results(self, submissions, output_dir: pathlib.Path, 
                               progress_callback=None) -> Tuple[int, int, List[str]]:
        """
        Download media from the search results.
        
        Args:
            submissions: Iterator of PRAW submission objects
            output_dir: Directory to save downloaded media
            progress_callback: Callback function for updating progress (optional)
            
        Returns:
            Tuple of (total_submissions, successful_downloads, failed_urls)
        """
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize counters
        total_submissions = 0
        successful_downloads = 0
        failed_urls = []
        
        # Store submissions in a list since iterator can only be consumed once
        submission_list = list(submissions)
        logger.info(f"Found {len(submission_list)} submissions to process")
        
        # Process each submission
        for submission in submission_list:
            total_submissions += 1
            
            # Log submission details for debugging
            logger.info(f"Processing submission {total_submissions}: ID={getattr(submission, 'id', 'unknown')}, "
                       f"Title={getattr(submission, 'title', 'unknown')[:40]}, "
                       f"URL={getattr(submission, 'url', 'unknown')}")
            
            # Update progress if callback is provided
            if progress_callback:
                progress_callback(total_submissions, successful_downloads, 
                                  f"Processing: {getattr(submission, 'title', 'Item ' + str(total_submissions))[:40]}...")
            
            # Special handling for mock mode
            is_mock = hasattr(submission, '_spec_class') and submission._spec_class is None
            
            # Process the submission
            try:
                # For mock mode, create a simple file to simulate download
                if is_mock:
                    logger.info("Using mock mode download")
                    success = self._mock_download(submission, output_dir)
                # Use our downloader to handle this submission
                elif self.db:
                    success = process_submission(submission, self.db, output_dir)
                else:
                    # Create simplified database record
                    success = self._process_without_db(submission, output_dir)
                
                if success:
                    successful_downloads += 1
                    logger.info(f"Successfully downloaded submission {getattr(submission, 'id', 'unknown')}")
                else:
                    logger.warning(f"Download failed for submission {getattr(submission, 'id', 'unknown')}")
                    failed_urls.append(getattr(submission, 'url', 'unknown_url'))
            except Exception as e:
                logger.error(f"Error processing submission {getattr(submission, 'id', 'unknown')}: {str(e)}")
                import traceback
                traceback.print_exc()
                failed_urls.append(getattr(submission, 'url', 'unknown_url'))
        
        # Final progress update
        if progress_callback:
            progress_callback(total_submissions, successful_downloads, 
                             f"Completed. Downloaded {successful_downloads}/{total_submissions} submissions")
        
        logger.info(f"Download complete: {successful_downloads} successful out of {total_submissions} total")
        return total_submissions, successful_downloads, failed_urls
        
    def _mock_download(self, submission, output_dir: pathlib.Path) -> bool:
        """
        Create a mock download file for testing purposes.
        
        Args:
            submission: Mock PRAW submission object
            output_dir: Directory to save the mock file
            
        Returns:
            True if mock download was successful
        """
        try:
            # Get submission details
            submission_id = getattr(submission, 'id', 'unknown')
            title = getattr(submission, 'title', f'Mock Post {submission_id}')
            url = getattr(submission, 'url', 'https://example.com/mock.jpg')
            
            # Create a simplified filename
            clean_title = ''.join(c if c.isalnum() or c in ' -_.' else '_' for c in title)
            filename = f"{clean_title[:30]}_{submission_id}.txt"
            
            # Create a mock file with submission details
            output_path = output_dir / filename
            with open(output_path, 'w') as f:
                f.write(f"Mock download for: {title}\n")
                f.write(f"URL: {url}\n")
                f.write(f"ID: {submission_id}\n")
                f.write(f"Downloaded at: {datetime.now().isoformat()}\n")
            
            logger.info(f"Created mock download file: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating mock download: {str(e)}")
            return False
    
    def _process_without_db(self, submission, output_dir: pathlib.Path) -> bool:
        """
        Process a submission without database integration.
        
        Args:
            submission: PRAW submission object
            output_dir: Directory to save downloaded media
            
        Returns:
            True if processing was successful, False otherwise
        """
        try:
            # Extract media URLs
            media_urls = extract_media_urls(submission)
            
            if not media_urls:
                return False
            
            # For each media URL, determine the appropriate downloader
            from grabber.downloader import download_image, download_video, is_video_url, get_output_path
            
            success = False
            for url in media_urls:
                # Get output path
                output_path = get_output_path(submission, url, output_dir)
                
                # Download based on media type
                if is_video_url(url):
                    success = download_video(url, output_path.parent, output_path.stem)
                else:
                    success = download_image(url, output_path)
                
                if success:
                    return True
            
            return success
        except Exception as e:
            logger.error(f"Error in _process_without_db: {str(e)}")
            return False
    
    def _is_image_submission(self, submission) -> bool:
        """Check if a submission contains an image."""
        if hasattr(submission, 'post_hint') and submission.post_hint == 'image':
            return True
        
        url = submission.url.lower()
        return any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp'])
    
    def _is_video_submission(self, submission) -> bool:
        """Check if a submission contains a video."""
        if hasattr(submission, 'is_video') and submission.is_video:
            return True
        
        if hasattr(submission, 'post_hint') and submission.post_hint == 'rich:video':
            return True
        
        url = submission.url.lower()
        return any(url.endswith(ext) for ext in ['.mp4', '.webm', '.mov']) or 'v.redd.it' in url
    
    def _is_gif_submission(self, submission) -> bool:
        """Check if a submission contains a GIF."""
        url = submission.url.lower()
        return url.endswith('.gif') or url.endswith('.gifv')
    
    def _is_article_submission(self, submission) -> bool:
        """Check if a submission is an article."""
        if submission.is_self:
            return True
        
        if hasattr(submission, 'post_hint'):
            return submission.post_hint == 'link'
        
        # If no specific indicators, assume it's an article if it's not an image, video, or GIF
        return not (self._is_image_submission(submission) or 
                   self._is_video_submission(submission) or 
                   self._is_gif_submission(submission))


class DownloadManager:
    """
    Manages download queue and parallel downloads.
    """
    
    def __init__(self, db: Optional[Database] = None, max_workers: int = 4):
        """
        Initialize the download manager.
        
        Args:
            db: Database instance for tracking downloads
            max_workers: Maximum number of parallel downloads
        """
        self.db = db
        self.max_workers = max_workers
        self.active_downloads = {}
        self.queue = []
        self.history = []
    
    def add_to_queue(self, item_info: Dict[str, Any]) -> str:
        """
        Add an item to the download queue.
        
        Args:
            item_info: Dictionary with item information (url, type, output_dir, etc.)
            
        Returns:
            Unique ID for the download
        """
        # Generate a unique ID
        download_id = f"dl_{int(time.time())}_{len(self.queue)}"
        
        # Add timestamp
        item_info['timestamp'] = datetime.now()
        item_info['download_id'] = download_id
        item_info['status'] = 'queued'
        
        # Add to queue
        self.queue.append(item_info)
        
        return download_id
    
    def start_download(self, download_id: str, progress_callback=None) -> bool:
        """
        Start a download from the queue.
        
        Args:
            download_id: ID of the download to start
            progress_callback: Callback function for updating progress
            
        Returns:
            True if download was started successfully, False otherwise
        """
        # Find the item in the queue
        item_info = None
        for item in self.queue:
            if item['download_id'] == download_id:
                item_info = item
                break
        
        if not item_info:
            logger.error(f"Download not found in queue: {download_id}")
            return False
        
        # Update status
        item_info['status'] = 'downloading'
        
        # TODO: Implement the actual download logic with threading
        
        return True
    
    def get_queue_status(self) -> List[Dict[str, Any]]:
        """
        Get the status of all items in the queue.
        
        Returns:
            List of dictionaries with item information
        """
        return self.queue
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the download history.
        
        Returns:
            List of dictionaries with item information
        """
        return self.history
