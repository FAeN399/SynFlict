"""
Fixed Subreddit downloader utility script.

This standalone script allows you to download media from specific subreddits 
with various sorting options (hot, new, top, rising, controversial) and filters.
"""

import sys
import os
import argparse
import logging
import pathlib
import time
from typing import List, Dict, Any, Optional, Callable, Tuple

import praw

from grabber.auth import get_reddit_instance
from grabber.download_manager import DownloadManager, DownloadItem

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("subreddit_downloader")


class SubredditMediaDownloader:
    """Handles downloading media from specific subreddits."""
    
    def __init__(self, reddit: praw.Reddit):
        """
        Initialize the subreddit downloader.
        
        Args:
            reddit: Authenticated Reddit instance
        """
        self.reddit = reddit
        self.download_manager = DownloadManager()
        
    def download(
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
        output_path = pathlib.Path(output_dir)
        
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
                
                try:
                    # Create a download item with the correct parameters based on DownloadItem's __init__ method
                    item = DownloadItem(
                        item_id=post.id,
                        item_type="subreddit",
                        url=post.url,
                        output_dir=output_path,
                        metadata={
                            "title": post.title,
                            "subreddit": post.subreddit.display_name,
                            "author": post.author.name if post.author else "[deleted]",
                            "created_utc": post.created_utc,
                            "score": post.score
                        }
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
                except Exception as e:
                    logger.error(f"Error creating download item for {post.url}: {str(e)}")
                    failed_urls.append(post.url)
            
            # We don't need to call start_downloads() as the DownloadManager processes the queue automatically
            
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


def read_config():
    """Read configuration settings from config.ini."""
    import configparser
    from pathlib import Path
    
    config = {}
    config_path = Path("config.ini")
    
    if config_path.exists():
        try:
            cfg = configparser.ConfigParser()
            cfg.read(config_path)
            
            if 'settings' in cfg:
                # Read various settings
                if 'allow_nsfw' in cfg['settings']:
                    config['allow_nsfw'] = cfg['settings'].getboolean('allow_nsfw', fallback=False)
                if 'default_output_dir' in cfg['settings']:
                    config['default_output_dir'] = cfg['settings']['default_output_dir']
        except Exception as e:
            logger.error(f"Error reading config.ini: {e}")
    
    return config

def write_config_setting(section, key, value):
    """Write a setting to the config.ini file."""
    import configparser
    from pathlib import Path
    
    config_path = Path("config.ini")
    cfg = configparser.ConfigParser()
    
    # Read existing config if it exists
    if config_path.exists():
        cfg.read(config_path)
    
    # Ensure section exists
    if section not in cfg:
        cfg[section] = {}
    
    # Set the value
    cfg[section][key] = str(value)
    
    # Write the config file
    with open(config_path, 'w') as f:
        cfg.write(f)
    
    logger.info(f"Updated config setting: [{section}] {key} = {value}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Download media from a specific subreddit.")
    parser.add_argument("subreddit", help="Name of the subreddit (without r/)")
    parser.add_argument("--sort", choices=["hot", "new", "top", "rising", "controversial"], 
                        default="hot", help="Sort method for posts")
    parser.add_argument("--time", choices=["hour", "day", "week", "month", "year", "all"], 
                        default="all", help="Time filter (for top and controversial sorts)")
    parser.add_argument("--media", choices=["all", "image", "video", "gif", "article"], 
                        default="all", help="Type of media to download")
    parser.add_argument("--limit", type=int, default=25, 
                        help="Maximum number of posts to process")
    parser.add_argument("--nsfw", action="store_true", 
                        help="Include NSFW content (default: false)")
    parser.add_argument("--always-allow-nsfw", action="store_true",
                        help="Permanently enable NSFW content in config.ini (no confirmation)")
    parser.add_argument("--disable-nsfw", action="store_true",
                        help="Permanently disable NSFW content in config.ini")
    parser.add_argument("--output", default="./downloads", 
                        help="Directory to save downloaded files")
    parser.add_argument("--mock", action="store_true", 
                        help="Use mock mode (no actual Reddit API calls)")
    
    args = parser.parse_args()
    
    # Read config
    config = read_config()
    
    # Handle NSFW config settings
    if args.always_allow_nsfw:
        write_config_setting('settings', 'allow_nsfw', 'true')
        logger.info("NSFW content permanently enabled in config.ini")
        args.nsfw = True
    elif args.disable_nsfw:
        write_config_setting('settings', 'allow_nsfw', 'false')
        logger.info("NSFW content permanently disabled in config.ini")
        args.nsfw = False
    elif args.nsfw:
        # Check if NSFW is allowed in config
        if not config.get('allow_nsfw', False):
            # Ask for confirmation
            print("\n===== NSFW CONTENT WARNING =====")
            print(f"You are about to download content from r/{args.subreddit} with NSFW enabled.")
            print("This may include adult content. Are you sure you want to continue?")
            print("Options:")
            print("1. Yes, continue this time")
            print("2. Yes, and always allow NSFW content (save to config)")
            print("3. No, cancel download")
            
            choice = input("Enter your choice (1/2/3): ").strip()
            
            if choice == '2':
                write_config_setting('settings', 'allow_nsfw', 'true')
                logger.info("NSFW content permanently enabled in config.ini")
            elif choice != '1':
                logger.info("Download cancelled by user")
                return 0
    else:
        # If not explicitly enabled, check config
        args.nsfw = config.get('allow_nsfw', False)
        if args.nsfw:
            logger.info("NSFW content enabled from config settings")
    
    # Use config default output directory if specified and no CLI override
    if 'default_output_dir' in config and args.output == "./downloads":
        args.output = config.get('default_output_dir')
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    try:
        # Get Reddit instance
        reddit = get_reddit_instance(user_auth=True, mock=args.mock)
        
        # Create subreddit downloader
        downloader = SubredditMediaDownloader(reddit)
        
        # Define progress callback
        def progress_callback(current, successful, status_text):
            if current % 5 == 0 or current == args.limit:  # Update every 5 items or at the end
                logger.info(f"Progress: {current}/{args.limit} - {status_text}")
        
        # Start the download
        logger.info(f"Starting download from r/{args.subreddit} with sort: {args.sort}")
        logger.info(f"Media type: {args.media}, NSFW: {args.nsfw}, Limit: {args.limit}")
        
        total, successful, failed = downloader.download(
            subreddit_name=args.subreddit,
            sort_by=args.sort,
            time_filter=args.time,
            media_type=args.media,
            limit=args.limit,
            nsfw_allowed=args.nsfw,
            output_dir=args.output,
            progress_callback=progress_callback
        )
        
        # Wait a moment for downloads to start processing
        time.sleep(2)
        
        logger.info(f"Download complete! Processed {total} posts, added {successful} to download queue.")
        if failed:
            logger.warning(f"Failed to download {len(failed)} items.")
        
        # Give some time for background downloads to complete
        logger.info("Waiting for downloads to complete (press Ctrl+C to exit)...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Download process interrupted. Some downloads may still be in progress.")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
