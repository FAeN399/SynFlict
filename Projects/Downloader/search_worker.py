"""
Thread worker for handling Reddit searches.
"""

from PySide6.QtCore import QThread, Signal

class SearchWorker(QThread):
    """Thread worker for handling searches"""
    results_ready = Signal(list)
    search_error = Signal(str)
    search_completed = Signal()
    
    def __init__(self, backend, keywords, media_type="All", sort="relevance", 
                 time_filter="all", limit=50, allow_nsfw=False):
        """
        Initialize the search worker.
        
        Args:
            backend: GUI backend instance
            keywords: Search keywords
            media_type: Type of media to search for (All, Images, Videos, GIFs, Articles)
            sort: Sort method (relevance, hot, new, top, comments)
            time_filter: Time period (all, day, week, month, year)
            limit: Maximum number of results to return
            allow_nsfw: If True, include NSFW content
        """
        super().__init__()
        self.backend = backend
        self.keywords = keywords
        self.media_type = media_type
        self.sort = sort
        self.time_filter = time_filter
        self.limit = limit
        self.allow_nsfw = allow_nsfw
        self.is_running = True
    
    def run(self):
        """Run the search thread"""
        try:
            # Perform search using backend
            results = self.backend.search_reddit(
                keywords=self.keywords,
                media_type=self.media_type,
                sort_by=self.sort.title(),  # Convert to title case for backend
                time_period=self._convert_time_filter(),
                nsfw=self.allow_nsfw,
                limit=self.limit
            )
            
            # Send results back to main thread
            if self.is_running:
                self.results_ready.emit(results)
        except Exception as e:
            if self.is_running:
                self.search_error.emit(str(e))
        finally:
            self.is_running = False
            self.search_completed.emit()
    
    def _convert_time_filter(self):
        """Convert time filter to format expected by backend"""
        time_map = {
            "all": "All Time",
            "day": "Past Day",
            "week": "Past Week", 
            "month": "Past Month",
            "year": "Past Year"
        }
        return time_map.get(self.time_filter, "All Time")
    
    def stop(self):
        """Stop the search thread"""
        self.is_running = False
        self.wait()  # Wait for thread to finish
