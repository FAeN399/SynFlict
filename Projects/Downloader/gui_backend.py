"""
Backend integration for the Reddit Media Grabber GUI.

Connects the GUI with the backend functionality.
"""

import os
import logging
import threading
import pathlib
from typing import Optional, List, Dict, Any, Callable

import praw

from grabber.auth import get_reddit_instance, save_credentials
from grabber.download_manager import DownloadManager, DownloadItem
from grabber.global_search import GlobalRedditSearch
from grabber.search import SearchParams
from grabber.config import load_config, save_config
from grabber.database import Database

logger = logging.getLogger(__name__)

class GUIBackend:
    """
    Backend integration for the Reddit Media Grabber GUI.
    """
    
    def __init__(self, config_path='config.ini'):
        """
        Initialize the backend integration.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = load_config(config_path)
        
        # Initialize database
        self.db = Database()
        
        # Initialize Reddit instance (use mock mode by default for testing)
        self.reddit = None
        self.is_mock_mode = True  # Track if we're in mock mode
        
        # First try to connect to real Reddit API
        real_connection = self.connect_to_reddit(mock=False)
        
        # If real connection fails, fall back to mock mode
        if not real_connection:
            logger.warning("Falling back to mock mode for testing")
            self.connect_to_reddit(mock=True)
        
        # Initialize download manager
        self.download_manager = DownloadManager(db=self.db)
        
        # Initialize global search
        if self.reddit:
            self.global_search = GlobalRedditSearch(self.reddit, db=self.db)
        else:
            self.global_search = None
            
    def search_reddit(self, keywords, media_type="All", sort_by="relevance", time_period="all", limit=50, allow_nsfw=False, only_nsfw=False):
        """
        Search Reddit globally based on the given parameters.
        
        Args:
            keywords: Search query keywords
            media_type: Type of media to search for (All, Images, Videos, GIFs, Articles)
            sort_by: Sort method (relevance, hot, new, top, comments)
            time_period: Time filter (all, day, week, month, year, all_time)
            limit: Maximum number of results to return
            allow_nsfw: Whether to include NSFW content
            only_nsfw: If True, only return NSFW content
            
        Returns:
            List of search results
        """
        if not self.reddit or not self.global_search:
            raise ValueError("Not connected to Reddit. Please connect first.")
            
        # Add debug logging for NSFW parameters
        logger.debug("[Backend] NSFW flags - allow:%s only:%s", allow_nsfw, only_nsfw)
            
        # Map media type to filter function
        media_filters = {
            "All": None,
            "Images": lambda p: p.url.endswith(('.jpg', '.jpeg', '.png', '.gif')) or 'i.redd.it' in p.url,
            "Videos": lambda p: p.url.endswith(('.mp4', '.webm', '.mov')) or 'v.redd.it' in p.url,
            "GIFs": lambda p: p.url.endswith('.gif') or 'gfycat.com' in p.url or 'imgur.com' in p.url and 'gallery' not in p.url,
            "Articles": lambda p: not any(domain in p.url for domain in ['i.redd.it', 'v.redd.it', 'imgur.com', 'gfycat.com']) \
                              and not p.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.mov'))
        }
        
        # Create search parameters
        search_params = SearchParams(
            query=keywords,
            sort=sort_by,
            time_filter=time_period,
            limit=limit,
            filter_func=media_filters.get(media_type),
            nsfw=allow_nsfw  # Use allow_nsfw parameter
        )
        
        # Perform search
        try:
            logger.info(f"Starting search with keywords: {keywords}, media_type: {media_type}, sort: {sort_by}, time: {time_period}")
            
            # Directly pass parameters to search method with consistent naming
            results = list(self.global_search.search(
                keywords=keywords,
                media_type=media_type,
                sort_by=sort_by,
                time_period=time_period,
                limit=limit,
                allow_nsfw=allow_nsfw,  # Use consistent parameter name
                only_nsfw=only_nsfw
            ))
            
            logger.info(f"Search completed, found {len(results) if results else 0} results")
            logger.debug("[Backend] NSFW results - total:%d nsfw:%d", 
                        len(results), 
                        sum(1 for r in results if r.over_18))
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            import traceback
            traceback.print_exc()
            raise ValueError(f"Search failed: {str(e)}")
        
        # Convert results to dictionary format for UI
        processed_results = []
        for post in results:
            # Determine media type
            post_type = "Unknown"
            if post.url.endswith(('.jpg', '.jpeg', '.png')) or 'i.redd.it' in post.url and not post.url.endswith('.gif'):
                post_type = "Image"
            elif post.url.endswith(('.mp4', '.webm', '.mov')) or 'v.redd.it' in post.url:
                post_type = "Video"
            elif post.url.endswith('.gif') or 'gfycat.com' in post.url or ('imgur.com' in post.url and 'gallery' not in post.url):
                post_type = "GIF"
            elif not any(domain in post.url for domain in ['i.redd.it', 'v.redd.it', 'imgur.com', 'gfycat.com']) \
                and not post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.mov')):
                post_type = "Article"
                
            # Create result dictionary
            result = {
                'id': post.id,
                'title': post.title,
                'url': post.url,
                'permalink': f"https://www.reddit.com{post.permalink}",
                'sub': f"r/{post.subreddit.display_name}",
                'author': str(post.author),
                'created_utc': post.created_utc,
                'upvotes': str(post.score),
                'nsfw': post.over_18,
                'type': post_type
            }
            
            processed_results.append(result)
            
        return processed_results
    
    def connect_to_reddit(self, mock=False, client_id=None, client_secret=None, 
                           username=None, password=None) -> bool:
        """
        Connect to Reddit API.
        
        Args:
            mock: If True, use mock mode
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            username: Reddit username
            password: Reddit password
            
        Returns:
            True if connection was successful, False otherwise
        """
        try:
            # If credentials provided, save them
            if client_id and client_secret:
                save_credentials(client_id, client_secret, username, password)
                
            # If mock mode is requested, use it directly
            if mock:
                self.reddit = get_reddit_instance(user_auth=False, mock=True)
                self.is_mock_mode = True
                logger.info("Connected to Reddit in mock mode")
                self.global_search = GlobalRedditSearch(self.reddit, db=self.db)
                return True
                
            # Try to get a real Reddit instance
            try:
                self.reddit = get_reddit_instance(user_auth=bool(username and password), mock=False)
                
                # Verify connection with a simple API call
                if hasattr(self.reddit, 'user'):
                    try:
                        # Try to access user info to verify authentication
                        if username and password:
                            user_info = self.reddit.user.me()
                            logger.info(f"Successfully connected to Reddit API as {user_info.name}")
                        else:
                            # For read-only mode, try accessing a subreddit
                            subreddit = self.reddit.subreddit('python')
                            next(subreddit.hot(limit=1), None)
                            logger.info("Successfully connected to Reddit API in read-only mode")
                        
                        self.is_mock_mode = False
                        self.global_search = GlobalRedditSearch(self.reddit, db=self.db)
                        return True
                        
                    except Exception as auth_error:
                        # Specific authentication errors
                        error_msg = str(auth_error)
                        if '401' in error_msg:
                            logger.error(f"Reddit authentication failed: Invalid credentials or app not registered as 'script'")
                            logger.error(f"Details: {error_msg}")
                            
                            # Suggest troubleshooting steps
                            logger.info("Troubleshooting steps:")
                            logger.info("1. Verify client_id and client_secret are correct")
                            logger.info("2. Ensure app is registered as 'script' type on Reddit")
                            logger.info("3. Check if your Reddit account is verified")
                            logger.info("4. If using 2FA, append code to password as 'password:123456'")
                        elif '403' in error_msg:
                            logger.error(f"Reddit authentication failed: Forbidden access (403)")
                            logger.error(f"Your account may be temporarily restricted or rate-limited")
                        else:
                            logger.error(f"Reddit authentication error: {error_msg}")
                        
                        # Fall back to mock mode
                        logger.warning("Falling back to mock mode due to authentication failure")
                        self.reddit = get_reddit_instance(user_auth=False, mock=True)
                        self.is_mock_mode = True
                        self.global_search = GlobalRedditSearch(self.reddit, db=self.db)
                        return False
            except Exception as e:
                logger.error(f"Failed to create Reddit instance: {e}")
                logger.warning("Falling back to mock mode due to initialization failure")
                self.reddit = get_reddit_instance(user_auth=False, mock=True)
                self.is_mock_mode = True
                self.global_search = GlobalRedditSearch(self.reddit, db=self.db)
                return False
                
        except Exception as e:
            logger.error(f"Unexpected error connecting to Reddit: {e}")
            logger.warning("Falling back to mock mode due to unexpected error")
            try:
                self.reddit = get_reddit_instance(user_auth=False, mock=True)
                self.is_mock_mode = True
                self.global_search = GlobalRedditSearch(self.reddit, db=self.db)
            except Exception as mock_error:
                logger.error(f"Even mock mode failed: {mock_error}")
                self.reddit = None
                self.is_mock_mode = True
            return False
    
    def add_to_download_queue(self, items_data):
        """
        Add items to the download queue.
        
        Args:
            items_data: List of dictionaries with item information
            
        Returns:
            List of download IDs
        """
        if not self.download_manager:
            return []
            
        download_ids = []
        for item in items_data:
            # Create output directory if it doesn't exist
            subreddit = item.get("sub", "").replace("r/", "")
            output_dir = self.get_download_dir() / subreddit
            os.makedirs(output_dir, exist_ok=True)
            
            # Create download item
            download_item = DownloadItem(
                item_id=item.get("id", "unknown"),
                item_type=item.get("type", "unknown").lower(),
                url=item.get("url", ""),
                output_dir=output_dir,
                metadata={
                    "title": item.get("title", ""),
                    "subreddit": subreddit,
                    "nsfw": item.get("nsfw", False),
                    "upvotes": item.get("upvotes", "0"),
                    "author": item.get("author", ""),
                    "permalink": item.get("permalink", "")
                }
            )
            
            # Add to queue
            download_id = self.download_manager.add_to_queue(download_item)
            download_ids.append(download_id)
            
        return download_ids
    
    def get_download_dir(self):
        """
        Get the download directory.
        
        Returns:
            pathlib.Path: Download directory
        """
        # Use the configured download directory or default to a subdirectory
        download_dir = self.config.get("settings", {}).get("download_dir", "downloads")
        return pathlib.Path(download_dir)
    
    def get_queue_status(self):
        """
        Get the status of all items in the download queue.
        
        Returns:
            List of dictionaries with item information
        """
        if not self.download_manager:
            return []
            
        return self.download_manager.get_queue_status()
    
    def get_download_history(self):
        """
        Get the download history.
        
        Returns:
            List of dictionaries with item information
        """
        if not self.download_manager:
            return []
            
        return self.download_manager.get_history()
    
    def cancel_download(self, download_id):
        """
        Cancel a download.
        
        Args:
            download_id: Download ID to cancel
            
        Returns:
            True if cancelled successfully, False otherwise
        """
        if not self.download_manager:
            return False
            
        return self.download_manager.cancel_download(download_id)
    
    def retry_download(self, download_id):
        """
        Retry a failed download.
        
        Args:
            download_id: Download ID to retry
            
        Returns:
            True if retried successfully, False otherwise
        """
        if not self.download_manager:
            return False
            
        return self.download_manager.retry_download(download_id)
    
    def save_settings(self, settings):
        """
        Save settings to config file.
        
        Args:
            settings: Dictionary with settings
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Update config with new settings
            if "settings" not in self.config:
                self.config["settings"] = {}
                
            self.config["settings"].update(settings)
            
            # Save config
            save_config(self.config, self.config_path)
            return True
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False
    
    def shutdown(self):
        """
        Shut down the backend.
        """
        if self.download_manager:
            self.download_manager.shutdown()
