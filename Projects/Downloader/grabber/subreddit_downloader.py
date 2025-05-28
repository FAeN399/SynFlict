"""
Subreddit-specific downloader module for Reddit Grabber.

This module handles downloading media from specific subreddits with
various sorting options and media type filtering.
"""

import logging
import os
from typing import List, Dict, Any, Callable, Optional, Tuple

import praw

from grabber.auth import get_reddit_instance
from grabber.download_manager import DownloadManager, DownloadItem

logger = logging.getLogger(__name__)


class SubredditDownloader:
    """Handles downloading media from specific subreddits."""
    
    def __init__(self, reddit: praw.Reddit, download_manager: Optional[DownloadManager] = None):
        """
        Initialize the subreddit downloader.
        
        Args:
            reddit: Authenticated Reddit instance
            download_manager: Optional download manager instance
        """
        self.reddit = reddit
        self.download_manager = download_manager or DownloadManager()
        
    def download_from_subreddit(
        self,
        subreddit_name: str,
        sort_by: str = "hot",
        time_filter: str = "all",
        media_type: str = "all",
        limit: int = 25,
        nsfw_allowed: bool = False,
        output_dir: str = "./downloads",
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Tuple[int, int, List[str]]:
        """
        Download media from a specific subreddit with sorting options.
        
        Args:
            subreddit_name: Name of the subreddit (without r/)
            sort_by: Sorting method (hot, new, top, rising, controversial)
            time_filter: Time filter for 'top' and 'controversial' (hour, day, week, month, year, all)
            media_type: Type of media to download (all, image, video, gif, article)
            limit: Maximum number of posts to process
            nsfw_allowed: Whether to include NSFW content
            output_dir: Directory to save downloaded files
            progress_callback: Callback for progress updates
            
        Returns:
            Tuple of (total posts processed, successful downloads, list of failed URLs)
        """
        logger.info(f"Starting download from r/{subreddit_name} - Sort: {sort_by}, Filter: {time_filter}, Limit: {limit}")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize counters
        total_processed = 0
        successful_downloads = 0
        failed_urls = []
        
        # Convert sort_by to the corresponding method name in PRAW
        sort_method = sort_by.lower()
        
        try:
            # Get subreddit instance
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get posts according to sort method
            if sort_method == "hot":
                posts = subreddit.hot(limit=limit)
            elif sort_method == "new":
                posts = subreddit.new(limit=limit)
            elif sort_method == "rising":
                posts = subreddit.rising(limit=limit)
            elif sort_method == "top":
                posts = subreddit.top(time_filter=time_filter.lower(), limit=limit)
            elif sort_method == "controversial":
                posts = subreddit.controversial(time_filter=time_filter.lower(), limit=limit)
            else:
                # Default to hot
                posts = subreddit.hot(limit=limit)
            
            # Process each post
            for post in posts:
                total_processed += 1
                
                # Skip NSFW content if not allowed
                if post.over_18 and not nsfw_allowed:
                    logger.debug(f"Skipping NSFW post: {post.title}")
                    continue
                
                # Skip self posts (text only)
                if post.is_self:
                    logger.debug(f"Skipping self post: {post.title}")
                    continue
                
                # Check media type if filtering is enabled
                if media_type.lower() != "all":
                    # Get the URL extension
                    url = post.url.lower()
                    
                    # Filter by media type
                    if media_type.lower() == "image":
                        if not any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                            continue
                    elif media_type.lower() == "video":
                        if not any(url.endswith(ext) for ext in ['.mp4', '.webm', '.mov']) and not "v.redd.it" in url:
                            continue
                    elif media_type.lower() == "gif":
                        if not url.endswith('.gif') and not "gfycat.com" in url and not "imgur.com/a/" in url:
                            continue
                    elif media_type.lower() == "article":
                        if any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm']):
                            continue
                
                # Create a download item
                item = DownloadItem(
                    url=post.url,
                    post_id=post.id,
                    title=post.title,
                    subreddit=post.subreddit.display_name,
                    author=post.author.name if post.author else "[deleted]",
                    output_dir=output_dir
                )
                
                # Add to download queue
                self.download_manager.add_to_queue(item)
                successful_downloads += 1
                
                # Update progress if callback is provided
                if progress_callback:
                    progress_callback(
                        total_processed,
                        successful_downloads,
                        f"Processing: r/{subreddit_name} - {post.title[:30]}..."
                    )
            
            # Start the download process
            self.download_manager.start_downloads()
            
            logger.info(f"Completed download from r/{subreddit_name}: {successful_downloads} items queued")
            return total_processed, successful_downloads, failed_urls
            
        except Exception as e:
            logger.error(f"Error downloading from r/{subreddit_name}: {str(e)}")
            if progress_callback:
                progress_callback(
                    total_processed,
                    successful_downloads,
                    f"Error: {str(e)}"
                )
            return total_processed, successful_downloads, failed_urls
