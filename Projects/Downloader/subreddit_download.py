"""
Subreddit downloader utility script.

This standalone script allows you to download media from specific subreddits 
with various sorting options (hot, new, top, rising, controversial) and filters.
"""

import sys
import os
import argparse
import logging

from grabber.auth import get_reddit_instance
from grabber.subreddit_downloader import SubredditDownloader
from grabber.download_manager import DownloadManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("subreddit_downloader")

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
    parser.add_argument("--output", default="./downloads", 
                        help="Directory to save downloaded files")
    parser.add_argument("--mock", action="store_true", 
                        help="Use mock mode (no actual Reddit API calls)")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    try:
        # Get Reddit instance
        reddit = get_reddit_instance(user_auth=True, mock=args.mock)
        
        # Create download manager
        download_manager = DownloadManager()
        
        # Create subreddit downloader
        downloader = SubredditDownloader(reddit, download_manager)
        
        # Define progress callback
        def progress_callback(current, successful, status_text):
            if current % 5 == 0 or current == args.limit:  # Update every 5 items or at the end
                logger.info(f"Progress: {current}/{args.limit} - {status_text}")
        
        # Start the download
        logger.info(f"Starting download from r/{args.subreddit} with sort: {args.sort}")
        logger.info(f"Media type: {args.media}, NSFW: {args.nsfw}, Limit: {args.limit}")
        
        total, successful, failed = downloader.download_from_subreddit(
            subreddit_name=args.subreddit,
            sort_by=args.sort,
            time_filter=args.time,
            media_type=args.media,
            limit=args.limit,
            nsfw_allowed=args.nsfw,
            output_dir=args.output,
            progress_callback=progress_callback
        )
        
        logger.info(f"Download complete! Processed {total} posts, added {successful} to download queue.")
        if failed:
            logger.warning(f"Failed to download {len(failed)} items.")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
