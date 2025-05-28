"""
Thread worker for handling downloads.
"""

import time
from PySide6.QtCore import QThread, Signal

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
    
    def run(self):
        """Run the download thread"""
        if not self.backend or not self.download_ids:
            return
            
        # Process each download ID
        for download_id in self.download_ids:
            # Check if we should stop
            if not self.is_running:
                break
                
            try:
                # Start the download through the backend
                success = self.backend.start_download(download_id)
                
                if not success:
                    self.download_completed.emit(download_id, False, "Failed to start download")
                    continue
                    
                # Monitor progress
                while self.is_running:
                    # Get status from backend
                    status = self.backend.get_download_status(download_id)
                    
                    if not status:
                        # Download not found
                        self.download_completed.emit(download_id, False, "Download not found")
                        break
                        
                    # Update progress
                    self.progress_updated.emit(
                        download_id, 
                        status.get("progress", 0),
                        status.get("status", "Unknown")
                    )
                    
                    # Check if completed
                    if status.get("status") == "Completed":
                        self.download_completed.emit(download_id, True, "Download completed")
                        break
                    elif status.get("status") == "Failed":
                        self.download_completed.emit(download_id, False, status.get("error", "Unknown error"))
                        break
                    elif status.get("status") == "Cancelled":
                        self.download_completed.emit(download_id, False, "Download cancelled")
                        break
                        
                    # Wait before checking again
                    time.sleep(0.5)
                    
            except Exception as e:
                self.download_completed.emit(download_id, False, str(e))
    
    def stop(self):
        """Stop the download worker"""
        self.is_running = False
        self.wait()  # Wait for thread to finish
