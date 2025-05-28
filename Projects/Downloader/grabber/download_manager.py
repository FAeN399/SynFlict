"""
Download manager module for Reddit Grabber.

Handles download queue, parallel downloads, progress tracking, and download history.
"""

import os
import pathlib
import time
import logging
import threading
import queue
from typing import List, Dict, Any, Optional, Callable, Tuple
from datetime import datetime
import hashlib
from concurrent.futures import ThreadPoolExecutor

from grabber.database import Database
from grabber.downloader import download_image, download_video, is_video_url, extract_media_urls

logger = logging.getLogger(__name__)


class DownloadItem:
    """
    Represents an item in the download queue.
    """
    
    def __init__(self, item_id: str, item_type: str, url: str, output_dir: pathlib.Path,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a download item.
        
        Args:
            item_id: Unique identifier for the item (e.g., Reddit submission ID)
            item_type: Type of the item (e.g., "submission", "search", "subreddit")
            url: URL to download
            output_dir: Directory to save the download
            metadata: Additional metadata for the item
        """
        self.item_id = item_id
        self.item_type = item_type
        self.url = url
        self.output_dir = output_dir
        self.metadata = metadata or {}
        
        # Status information
        self.status = "queued"  # queued, downloading, completed, failed, paused
        self.progress = 0  # 0-100
        self.start_time = None
        self.end_time = None
        self.file_size = 0
        self.download_path = None
        self.error_message = None
        
        # Generate a unique download ID
        self.download_id = f"{item_type}_{item_id}_{int(time.time())}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the download item to a dictionary.
        
        Returns:
            Dictionary representation of the download item
        """
        return {
            "download_id": self.download_id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "url": self.url,
            "output_dir": str(self.output_dir),
            "status": self.status,
            "progress": self.progress,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "file_size": self.file_size,
            "download_path": self.download_path,
            "error_message": self.error_message,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DownloadItem':
        """
        Create a download item from a dictionary.
        
        Args:
            data: Dictionary representation of a download item
            
        Returns:
            DownloadItem instance
        """
        item = cls(
            item_id=data["item_id"],
            item_type=data["item_type"],
            url=data["url"],
            output_dir=pathlib.Path(data["output_dir"]),
            metadata=data.get("metadata", {})
        )
        
        item.download_id = data["download_id"]
        item.status = data["status"]
        item.progress = data["progress"]
        item.start_time = data["start_time"]
        item.end_time = data["end_time"]
        item.file_size = data["file_size"]
        item.download_path = data["download_path"]
        item.error_message = data["error_message"]
        
        return item


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
        self.queue = queue.Queue()
        self.active_downloads = {}
        self.history = []
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.Lock()
        self.shutdown_event = threading.Event()
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True
        self.worker_thread.start()
    
    def shutdown(self):
        """
        Shutdown the download manager.
        """
        self.shutdown_event.set()
        self.executor.shutdown(wait=False)
    
    def add_to_queue(self, item: DownloadItem) -> str:
        """
        Add an item to the download queue.
        
        Args:
            item: DownloadItem to add to the queue
            
        Returns:
            Download ID of the queued item
        """
        with self.lock:
            # Add to queue
            self.queue.put(item)
            self.active_downloads[item.download_id] = item
        
        logger.info(f"Added item to download queue: {item.download_id}")
        return item.download_id
    
    def add_bulk_to_queue(self, items: List[DownloadItem]) -> List[str]:
        """
        Add multiple items to the download queue.
        
        Args:
            items: List of DownloadItem objects to add to the queue
            
        Returns:
            List of download IDs
        """
        download_ids = []
        
        with self.lock:
            for item in items:
                self.queue.put(item)
                self.active_downloads[item.download_id] = item
                download_ids.append(item.download_id)
        
        logger.info(f"Added {len(items)} items to download queue")
        return download_ids
    
    def add_submission_to_queue(self, submission, output_dir: pathlib.Path) -> List[str]:
        """
        Add a Reddit submission to the download queue.
        
        Args:
            submission: PRAW submission object
            output_dir: Directory to save downloads
            
        Returns:
            List of download IDs
        """
        # Extract media URLs
        media_urls = extract_media_urls(submission)
        
        if not media_urls:
            logger.info(f"No media found in submission: {submission.id}")
            return []
        
        # Create download items
        items = []
        for url in media_urls:
            item = DownloadItem(
                item_id=submission.id,
                item_type="submission",
                url=url,
                output_dir=output_dir,
                metadata={
                    "title": submission.title,
                    "author": submission.author.name if submission.author else "[deleted]",
                    "permalink": submission.permalink,
                    "subreddit": submission.subreddit.display_name,
                    "created_utc": submission.created_utc,
                    "score": submission.score
                }
            )
            items.append(item)
        
        # Add items to queue
        return self.add_bulk_to_queue(items)
    
    def _process_queue(self):
        """
        Process the download queue in a background thread.
        """
        while not self.shutdown_event.is_set():
            try:
                # Get the next item from the queue (non-blocking)
                try:
                    item = self.queue.get(block=True, timeout=1.0)
                except queue.Empty:
                    continue
                
                # Update item status
                item.status = "downloading"
                item.start_time = time.time()
                
                # Submit the download job to the thread pool
                future = self.executor.submit(self._download_item, item)
                
                # Add a callback to handle completion
                future.add_done_callback(lambda f, item=item: self._download_completed(item, f))
                
            except Exception as e:
                logger.error(f"Error processing download queue: {str(e)}")
    
    def _download_item(self, item: DownloadItem) -> bool:
        """
        Download an item.
        
        Args:
            item: DownloadItem to download
            
        Returns:
            True if download was successful, False otherwise
        """
        try:
            # Create output directory
            item.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate output filename
            url_filename = os.path.basename(item.url.split("?")[0])
            
            # Create a unique filename using metadata
            if item.metadata.get("title"):
                # Clean the title for use as a filename
                title = "".join(c if c.isalnum() or c in " -_." else "_" for c in item.metadata["title"])
                title = title[:50]  # Limit length
                
                # Use title and ID as filename
                if is_video_url(item.url):
                    output_filename = f"{title}_{item.item_id}"
                    output_path = item.output_dir / output_filename
                else:
                    ext = os.path.splitext(url_filename)[1] or ".jpg"
                    output_filename = f"{title}_{item.item_id}{ext}"
                    output_path = item.output_dir / output_filename
            else:
                # Use URL filename
                output_path = item.output_dir / url_filename
            
            # Download based on media type
            success = False
            if is_video_url(item.url):
                success = download_video(item.url, item.output_dir, output_path.stem)
                
                # Try to find the actual downloaded file
                if success:
                    for ext in [".mp4", ".webm", ".mov", ".mkv"]:
                        potential_file = item.output_dir / f"{output_path.stem}{ext}"
                        if potential_file.exists():
                            item.download_path = str(potential_file)
                            item.file_size = potential_file.stat().st_size
                            break
            else:
                success = download_image(item.url, output_path)
                if success:
                    item.download_path = str(output_path)
                    item.file_size = output_path.stat().st_size
            
            # Update database if available
            if success and self.db and item.item_type == "submission":
                try:
                    # Calculate file hash
                    if item.download_path:
                        file_hash = self._calculate_file_hash(item.download_path)
                        if file_hash:
                            self.db.add_file_hash(file_hash, item.download_path)
                    
                    # Add post to database
                    if item.metadata.get("permalink"):
                        self.db.add_post(item.item_id, item.metadata["permalink"])
                        self.db.mark_post_downloaded(item.item_id)
                except Exception as db_err:
                    logger.error(f"Database error: {str(db_err)}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error downloading {item.url}: {str(e)}")
            item.error_message = str(e)
            return False
    
    def _download_completed(self, item: DownloadItem, future):
        """
        Handle download completion.
        
        Args:
            item: DownloadItem that was downloaded
            future: Future object from the thread pool
        """
        try:
            success = future.result()
            
            # Update item status
            item.end_time = time.time()
            item.status = "completed" if success else "failed"
            item.progress = 100 if success else 0
            
            # Move from active to history
            with self.lock:
                if item.download_id in self.active_downloads:
                    self.history.append(item)
                    # Keep in active_downloads for status queries
            
            # Mark task as done
            self.queue.task_done()
            
            logger.info(f"Download {item.download_id} completed: {success}")
            
        except Exception as e:
            logger.error(f"Error handling download completion: {str(e)}")
            
            # Update item status on error
            item.status = "failed"
            item.error_message = str(e)
            item.end_time = time.time()
            
            # Mark task as done
            self.queue.task_done()
    
    def get_item_status(self, download_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a download item.
        
        Args:
            download_id: Download ID of the item
            
        Returns:
            Dictionary with status information, or None if the item doesn't exist
        """
        with self.lock:
            if download_id in self.active_downloads:
                return self.active_downloads[download_id].to_dict()
            
            # Check history
            for item in self.history:
                if item.download_id == download_id:
                    return item.to_dict()
        
        return None
    
    def get_queue_status(self) -> List[Dict[str, Any]]:
        """
        Get the status of all items in the queue.
        
        Returns:
            List of dictionaries with status information
        """
        with self.lock:
            return [item.to_dict() for item in self.active_downloads.values()]
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the download history.
        
        Returns:
            List of dictionaries with status information
        """
        with self.lock:
            return [item.to_dict() for item in self.history]
    
    def cancel_download(self, download_id: str) -> bool:
        """
        Cancel a download.
        
        Args:
            download_id: Download ID of the item to cancel
            
        Returns:
            True if the download was cancelled, False otherwise
        """
        with self.lock:
            if download_id in self.active_downloads:
                item = self.active_downloads[download_id]
                
                # Only cancel if not already completed
                if item.status not in ["completed", "failed"]:
                    item.status = "cancelled"
                    item.end_time = time.time()
                    return True
        
        return False
    
    def retry_download(self, download_id: str) -> bool:
        """
        Retry a failed download.
        
        Args:
            download_id: Download ID of the item to retry
            
        Returns:
            True if the download was requeued, False otherwise
        """
        with self.lock:
            # Check history first
            for i, item in enumerate(self.history):
                if item.download_id == download_id:
                    if item.status in ["failed", "cancelled"]:
                        # Create a new download item with the same parameters
                        new_item = DownloadItem(
                            item_id=item.item_id,
                            item_type=item.item_type,
                            url=item.url,
                            output_dir=item.output_dir,
                            metadata=item.metadata
                        )
                        
                        # Add to queue
                        self.queue.put(new_item)
                        self.active_downloads[new_item.download_id] = new_item
                        
                        return True
            
            # Check active downloads
            if download_id in self.active_downloads:
                item = self.active_downloads[download_id]
                if item.status in ["failed", "cancelled"]:
                    # Reset status
                    item.status = "queued"
                    item.progress = 0
                    item.start_time = None
                    item.end_time = None
                    item.error_message = None
                    
                    # Add back to queue
                    self.queue.put(item)
                    return True
        
        return False
    
    def _calculate_file_hash(self, file_path: str) -> Optional[str]:
        """
        Calculate SHA1 hash of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            SHA1 hash as a hex string, or None if the file doesn't exist
        """
        try:
            sha1 = hashlib.sha1()
            
            # Read file in chunks
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(65536)  # 64KB chunks
                    if not data:
                        break
                    sha1.update(data)
            
            return sha1.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash: {str(e)}")
            return None
