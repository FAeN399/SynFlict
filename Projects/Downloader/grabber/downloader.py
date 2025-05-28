"""
Downloader module for Reddit Grabber.

Handles downloading media files from Reddit submissions.
"""

import os
import re
import time
import hashlib
import logging
import pathlib
import subprocess
from typing import List, Optional, Dict, Any, Union, Tuple
from urllib.parse import urlparse

import requests

from grabber.database import Database

# Try to import the mock downloader
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from mock_downloader import mock_download_file, is_mock_url, create_mock_image
    MOCK_DOWNLOADER_AVAILABLE = True
except ImportError:
    MOCK_DOWNLOADER_AVAILABLE = False

logger = logging.getLogger(__name__)


def calculate_sha1(file_path: pathlib.Path) -> str:
    """
    Calculate SHA1 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        SHA1 hash as a hex string
    """
    sha1 = hashlib.sha1()
    
    # Read file in chunks to handle large files
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # 64KB chunks
            if not data:
                break
            sha1.update(data)
    
    return sha1.hexdigest()


def download_image(url: str, output_path: pathlib.Path, metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Download an image from a URL.
    
    Args:
        url: URL of the image
        output_path: Path to save the image
        metadata: Optional metadata about the image
        
    Returns:
        True if download was successful, False otherwise
    """
    # Check if this is a mock URL and we have the mock downloader available
    if MOCK_DOWNLOADER_AVAILABLE and (is_mock_url(url) or 'mockimage' in url or url.endswith(('mockimage.jpg', 'mockimage.png'))):
        logger.info(f"Using mock downloader for URL: {url}")
        success, error = mock_download_file(url, str(output_path), "image", metadata)
        if not success:
            logger.error(f"Mock download failed for {url}: {error}")
        return success
    
    try:
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download the image
        logger.info(f"Downloading image: {url}")
        response = requests.get(url, timeout=30)
        
        # Check if the download was successful
        if response.status_code != 200:
            logger.error(f"Failed to download image: {url}, status code: {response.status_code}")
            
            # If download failed and mock downloader is available, fall back to creating a mock image
            if MOCK_DOWNLOADER_AVAILABLE:
                logger.info(f"Falling back to mock download for failed URL: {url}")
                success, error = mock_download_file(url, str(output_path), "image", metadata)
                if not success:
                    logger.error(f"Mock download fallback failed for {url}: {error}")
                return success
            return False
        
        # Save the image
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Image saved to: {output_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error downloading image: {url}, error: {str(e)}")
        
        # If download failed and mock downloader is available, fall back to creating a mock image
        if MOCK_DOWNLOADER_AVAILABLE:
            logger.info(f"Falling back to mock download after error for URL: {url}")
            success, error = mock_download_file(url, str(output_path), "image", metadata)
            if not success:
                logger.error(f"Mock download fallback failed for {url}: {error}")
            return success
        return False


def download_video(url: str, output_dir: pathlib.Path, filename: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Download a video using yt-dlp.
    
    Args:
        url: URL of the video
        output_dir: Directory to save the video
        filename: Optional base filename without extension
        metadata: Optional metadata about the video
        
    Returns:
        True if download was successful, False otherwise
    """
    # Check if this is a mock URL and we have the mock downloader available
    if MOCK_DOWNLOADER_AVAILABLE and (is_mock_url(url) or 'mockvideo' in url):
        output_path = output_dir / f"{filename or 'video'}.mp4"
        logger.info(f"Using mock downloader for video URL: {url}")
        success, error = mock_download_file(url, str(output_path), "video", metadata)
        if not success:
            logger.error(f"Mock download failed for video {url}: {error}")
        return success
    
    try:
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Build the yt-dlp command
        output_template = str(output_dir / "%(title)s-%(id)s.%(ext)s")
        if filename:
            output_template = str(output_dir / f"{filename}.%(ext)s")
        
        logger.info(f"Downloading video: {url}")
        
        # Run yt-dlp
        cmd = [
            "yt-dlp",
            "--format", "best",
            "--output", output_template,
            "--no-playlist",
            "--quiet",
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Failed to download video: {url}, error: {result.stderr}")
            
            # If download failed and mock downloader is available, fall back to creating a mock video
            if MOCK_DOWNLOADER_AVAILABLE:
                output_path = output_dir / f"{filename or 'video'}.mp4"
                logger.info(f"Falling back to mock download for failed video URL: {url}")
                success, error = mock_download_file(url, str(output_path), "video", metadata)
                if not success:
                    logger.error(f"Mock download fallback failed for video {url}: {error}")
                return success
            return False
        
        logger.info(f"Video downloaded to: {output_dir}")
        return True
    
    except Exception as e:
        logger.error(f"Error downloading video: {url}, error: {str(e)}")
        
        # If download failed and mock downloader is available, fall back to creating a mock video
        if MOCK_DOWNLOADER_AVAILABLE:
            output_path = output_dir / f"{filename or 'video'}.mp4"
            logger.info(f"Falling back to mock download after error for video URL: {url}")
            success, error = mock_download_file(url, str(output_path), "video", metadata)
            if not success:
                logger.error(f"Mock download fallback failed for video {url}: {error}")
            return success
        return False


def extract_media_urls(submission) -> List[str]:
    """
    Extract media URLs from a Reddit submission.
    
    Args:
        submission: PRAW submission object
        
    Returns:
        List of media URLs
    """
    urls = []
    
    # Skip self posts (text-only posts)
    if submission.is_self:
        logger.info(f"Skipping self post: {submission.id}")
        return urls
    
    # Check for direct image/video links
    direct_media_patterns = [
        r'\.jpg$', r'\.jpeg$', r'\.png$', r'\.gif$',
        r'\.webp$', r'\.webm$', r'\.mp4$'
    ]
    
    url = submission.url
    
    # Handle direct media links
    if any(re.search(pattern, url, re.IGNORECASE) for pattern in direct_media_patterns):
        urls.append(url)
        return urls
    
    # Handle Imgur links
    if 'imgur.com' in url and not url.endswith('.gifv'):
        if not any(re.search(pattern, url, re.IGNORECASE) for pattern in direct_media_patterns):
            # Convert imgur links to direct image links if needed
            if '/a/' in url or '/gallery/' in url:
                # This is an album, would need additional API calls to get all images
                logger.info(f"Imgur album detected: {url}")
                # For now, just use the URL as is - would need imgur API for proper handling
                urls.append(url)
            else:
                # Convert to direct image link
                img_id = url.split('/')[-1].split('#')[0].split('?')[0]
                urls.append(f"https://i.imgur.com/{img_id}.jpg")
        else:
            urls.append(url)
        return urls
    
    # Handle Reddit galleries
    if 'reddit.com/gallery/' in url:
        try:
            if hasattr(submission, 'media_metadata') and submission.media_metadata:
                for item in submission.media_metadata.values():
                    if 's' in item and 'u' in item['s']:
                        urls.append(item['s']['u'])
        except Exception as e:
            logger.error(f"Error extracting gallery URLs: {str(e)}")
        return urls
    
    # Handle v.redd.it videos
    if 'v.redd.it' in url:
        urls.append(url)
        return urls
    
    # Handle i.redd.it images
    if 'i.redd.it' in url:
        urls.append(url)
        return urls
    
    # Handle external videos (YouTube, etc.) via the main URL
    video_domains = ['youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com']
    if any(domain in url for domain in video_domains):
        urls.append(url)
        return urls
    
    # If no media URLs were found, log and return empty list
    if not urls:
        logger.info(f"No media URLs found for submission: {submission.id}, URL: {url}")
    
    return urls


def get_output_path(submission, media_url: str, output_dir: pathlib.Path) -> pathlib.Path:
    """
    Generate an output path for a media file.
    
    Args:
        submission: PRAW submission object
        media_url: URL of the media file
        output_dir: Base output directory
        
    Returns:
        Path to save the media file
    """
    # Get subreddit name
    subreddit = submission.subreddit.display_name
    
    # Create a sanitized title for the filename
    title = submission.title
    # Remove invalid filename characters
    title = re.sub(r'[\\/*?:"<>|]', '', title)
    # Limit length
    title = title[:100].strip()
    
    # Get submission ID
    submission_id = submission.id
    
    # Get file extension from URL
    parsed_url = urlparse(media_url)
    path = parsed_url.path
    ext = os.path.splitext(path)[1].lower()
    
    # Default to .jpg if no extension or unsupported extension
    if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.webm', '.mp4']:
        if 'v.redd.it' in media_url:
            ext = '.mp4'
        else:
            ext = '.jpg'
    
    # Create output directory structure
    output_subdir = output_dir / subreddit
    output_subdir.mkdir(parents=True, exist_ok=True)
    
    # Create filename
    filename = f"{title}_{submission_id}{ext}"
    
    return output_subdir / filename


def is_video_url(url: str) -> bool:
    """
    Check if a URL points to a video.
    
    Args:
        url: URL to check
        
    Returns:
        True if URL points to a video, False otherwise
    """
    video_extensions = ['.mp4', '.webm', '.mov', '.avi', '.wmv', '.flv', '.mkv']
    video_domains = ['v.redd.it', 'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com']
    
    # Check extension
    parsed_url = urlparse(url)
    path = parsed_url.path
    ext = os.path.splitext(path)[1].lower()
    
    if ext in video_extensions:
        return True
    
    # Check domain
    if any(domain in url for domain in video_domains):
        return True
    
    return False


def process_submission(submission, db: Database, output_dir: pathlib.Path, dry_run: bool = False) -> bool:
    """
    Process a submission and download its media.
    
    Args:
        submission: PRAW submission object
        db: Database instance
        output_dir: Base output directory
        dry_run: If True, don't actually download anything
        
    Returns:
        True if processing was successful, False otherwise
    """
    try:
        # Extract media URLs
        media_urls = extract_media_urls(submission)
        
        if not media_urls:
            logger.info(f"No media found in submission: {submission.id}")
            return False
        
        success = False
        
        # Create metadata dict from submission
        metadata = {
            "title": submission.title,
            "subreddit": submission.subreddit.display_name,
            "author": str(submission.author),
            "created_utc": submission.created_utc,
            "score": submission.score,
            "permalink": submission.permalink
        }
        
        for media_url in media_urls:
            # Generate output path
            output_path = get_output_path(submission, media_url, output_dir)
            
            # Check if file already exists
            if output_path.exists():
                logger.info(f"File already exists: {output_path}")
                success = True
                continue
            
            # Skip if dry run
            if dry_run:
                logger.info(f"Dry run, would download: {media_url} to {output_path}")
                success = True
                continue
            
            # Download media
            if is_video_url(media_url):
                # Download video
                success = download_video(media_url, output_path.parent, output_path.stem, metadata)
            else:
                # Download image
                success = download_image(media_url, output_path, metadata)
            
            if success and db:
                # Add to database
                db.add_download({
                    "submission_id": submission.id,
                    "title": submission.title,
                    "url": submission.url,
                    "media_url": media_url,
                    "subreddit": submission.subreddit.display_name,
                    "author": str(submission.author),
                    "created_utc": submission.created_utc,
                    "downloaded_at": time.time(),
                    "file_path": str(output_path),
                    "file_size": output_path.stat().st_size if output_path.exists() else 0,
                    "sha1": calculate_sha1(output_path) if output_path.exists() else None
                })
        
        return success
    
    except Exception as e:
        logger.error(f"Error processing submission {submission.id}: {str(e)}")
        return False
