"""
Thread worker for handling downloads.
"""

import time
import logging
from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)

class DownloadWorker(QThread):
    """Thread worker for handling downloads"""
    progress_updated = Signal(str, int, str)  # download_id, progress, status
    download_completed = Signal(str, bool, str)  # download_id, success, message
    
    def __init__(self, backend, download_ids):
        """
        Initialize the download worker.
        
        Args:
            backend: GUI backend instance
            download_ids: List of download IDs to process
        """
        super().__init__()
        self.backend = backend
        self.download_ids = download_ids
        self.is_running = True
        self.current_download = None
        self.error_count = 0
        self.max_retries = 3
    
    def run(self):
        """Run the download thread"""
        if not self.backend or not self.download_ids:
            return
            
        # Process each download ID
        while self.is_running and self.download_ids:
            # Get the next download ID
            self.current_download = self.download_ids[0]
            
            try:
                # Start the download through the backend
                success = self.backend.start_download(self.current_download)
                
                if not success:
                    logger.error(f"Failed to start download {self.current_download}")
                    self.download_completed.emit(self.current_download, False, "Failed to start download")
                    self.download_ids.remove(self.current_download)
                    continue
                    
                # Monitor progress
                last_progress = -1
                last_status = None
                retry_count = 0
                
                while self.is_running:
                    try:
                        # Get status from backend
                        status = self.backend.get_download_status(self.current_download)
                        
                        if not status:
                            # Download not found
                            logger.error(f"Download {self.current_download} not found")
                            self.download_completed.emit(self.current_download, False, "Download not found")
                            break
                            
                        # Get current progress and status
                        current_progress = status.get("progress", 0)
                        current_status = status.get("status", "Unknown")
                        
                        # Only emit if changed
                        if current_progress != last_progress or current_status != last_status:
                            self.progress_updated.emit(
                                self.current_download, 
                                current_progress,
                                current_status
                            )
                            last_progress = current_progress
                            last_status = current_status
                        
                        # Check if completed
                        if current_status == "Completed":
                            self.download_completed.emit(self.current_download, True, "Download completed")
                            break
                        elif current_status == "Failed":
                            if retry_count < self.max_retries:
                                retry_count += 1
                                logger.warning(f"Retrying download {self.current_download} (attempt {retry_count})")
                                self.backend.retry_download(self.current_download)
                                continue
                            else:
                                error_msg = status.get("error", "Unknown error")
                                logger.error(f"Download {self.current_download} failed after {retry_count} retries: {error_msg}")
                                self.download_completed.emit(self.current_download, False, f"Failed after {retry_count} retries: {error_msg}")
                                break
                        elif current_status == "Cancelled":
                            self.download_completed.emit(self.current_download, False, "Download cancelled")
                            break
                            
                        # Wait before checking again
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"Error monitoring download {self.current_download}: {str(e)}")
                        if retry_count < self.max_retries:
                            retry_count += 1
                            logger.warning(f"Retrying download {self.current_download} after error (attempt {retry_count})")
                            time.sleep(1)  # Wait before retry
                            continue
                        else:
                            self.download_completed.emit(self.current_download, False, f"Error: {str(e)}")
                            break
                
                # Remove completed download from queue
                if self.current_download in self.download_ids:
                    self.download_ids.remove(self.current_download)
                    
            except Exception as e:
                logger.error(f"Error processing download {self.current_download}: {str(e)}")
                self.download_completed.emit(self.current_download, False, str(e))
                if self.current_download in self.download_ids:
                    self.download_ids.remove(self.current_download)
    
    def stop(self):
        """Stop the download worker"""
        self.is_running = False
        if self.current_download:
            try:
                self.backend.cancel_download(self.current_download)
            except Exception as e:
                logger.error(f"Error cancelling download {self.current_download}: {str(e)}")
        self.wait()  # Wait for thread to finish
