"""
Stats manager for Reddit Media Grabber.

Handles download statistics and reporting.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

class StatsManager(QObject):
    """Manages download statistics."""
    
    # Signals
    stats_updated = Signal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the stats manager.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.stats_file = "download_stats.json"
        self.stats = {
            'total_downloads': 0,
            'total_size': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'total_time': 0,
            'average_speed': 0,
            'daily_stats': {},
            'hourly_stats': {},
            'source_stats': {},
            'type_stats': {},
            'error_stats': {}
        }
        self.settings = None
        
    def initialize(self, settings: Dict[str, Any]) -> None:
        """
        Initialize with settings.
        
        Args:
            settings: Stats settings
        """
        self.settings = settings
        
        # Load stats
        self.load_stats()
        
    def record_download(self, download_id: str, title: str, 
                       file_size: int, duration: float,
                       status: str, source: str, file_type: str,
                       error_message: Optional[str] = None) -> None:
        """
        Record a download in statistics.
        
        Args:
            download_id: Download ID
            title: Download title
            file_size: File size in bytes
            duration: Download duration in seconds
            status: Download status
            source: Download source
            file_type: File type
            error_message: Error message if any
        """
        # Get current time
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        hour_str = now.strftime("%H:00")
        
        # Update total stats
        self.stats['total_downloads'] += 1
        self.stats['total_size'] += file_size
        self.stats['total_time'] += duration
        
        if status == "Completed":
            self.stats['successful_downloads'] += 1
        else:
            self.stats['failed_downloads'] += 1
            
        # Update average speed
        if self.stats['total_time'] > 0:
            self.stats['average_speed'] = (
                self.stats['total_size'] / self.stats['total_time']
            )
            
        # Update daily stats
        if date_str not in self.stats['daily_stats']:
            self.stats['daily_stats'][date_str] = {
                'downloads': 0,
                'size': 0,
                'successful': 0,
                'failed': 0,
                'time': 0
            }
            
        daily = self.stats['daily_stats'][date_str]
        daily['downloads'] += 1
        daily['size'] += file_size
        daily['time'] += duration
        
        if status == "Completed":
            daily['successful'] += 1
        else:
            daily['failed'] += 1
            
        # Update hourly stats
        if hour_str not in self.stats['hourly_stats']:
            self.stats['hourly_stats'][hour_str] = {
                'downloads': 0,
                'size': 0,
                'successful': 0,
                'failed': 0,
                'time': 0
            }
            
        hourly = self.stats['hourly_stats'][hour_str]
        hourly['downloads'] += 1
        hourly['size'] += file_size
        hourly['time'] += duration
        
        if status == "Completed":
            hourly['successful'] += 1
        else:
            hourly['failed'] += 1
            
        # Update source stats
        if source not in self.stats['source_stats']:
            self.stats['source_stats'][source] = {
                'downloads': 0,
                'size': 0,
                'successful': 0,
                'failed': 0,
                'time': 0
            }
            
        source_stats = self.stats['source_stats'][source]
        source_stats['downloads'] += 1
        source_stats['size'] += file_size
        source_stats['time'] += duration
        
        if status == "Completed":
            source_stats['successful'] += 1
        else:
            source_stats['failed'] += 1
            
        # Update type stats
        if file_type not in self.stats['type_stats']:
            self.stats['type_stats'][file_type] = {
                'downloads': 0,
                'size': 0,
                'successful': 0,
                'failed': 0,
                'time': 0
            }
            
        type_stats = self.stats['type_stats'][file_type]
        type_stats['downloads'] += 1
        type_stats['size'] += file_size
        type_stats['time'] += duration
        
        if status == "Completed":
            type_stats['successful'] += 1
        else:
            type_stats['failed'] += 1
            
        # Update error stats
        if error_message:
            if error_message not in self.stats['error_stats']:
                self.stats['error_stats'][error_message] = 0
            self.stats['error_stats'][error_message] += 1
            
        # Save stats
        self.save_stats()
        
        # Emit signal
        self.stats_updated.emit()
        
    def get_total_stats(self) -> Dict[str, Any]:
        """
        Get total statistics.
        
        Returns:
            Dict[str, Any]: Total statistics
        """
        return {
            'total_downloads': self.stats['total_downloads'],
            'total_size': self.stats['total_size'],
            'successful_downloads': self.stats['successful_downloads'],
            'failed_downloads': self.stats['failed_downloads'],
            'total_time': self.stats['total_time'],
            'average_speed': self.stats['average_speed']
        }
        
    def get_daily_stats(self, days: int = 7) -> Dict[str, Dict[str, Any]]:
        """
        Get daily statistics.
        
        Args:
            days: Number of days to include
            
        Returns:
            Dict[str, Dict[str, Any]]: Daily statistics
        """
        # Get date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter stats
        daily_stats = {}
        for date_str, stats in self.stats['daily_stats'].items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if start_date <= date <= end_date:
                daily_stats[date_str] = stats
                
        return daily_stats
        
    def get_hourly_stats(self, hours: int = 24) -> Dict[str, Dict[str, Any]]:
        """
        Get hourly statistics.
        
        Args:
            hours: Number of hours to include
            
        Returns:
            Dict[str, Dict[str, Any]]: Hourly statistics
        """
        # Get time range
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        # Filter stats
        hourly_stats = {}
        for hour_str, stats in self.stats['hourly_stats'].items():
            hour = datetime.strptime(hour_str, "%H:00")
            if start_time <= hour <= end_time:
                hourly_stats[hour_str] = stats
                
        return hourly_stats
        
    def get_source_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get source statistics.
        
        Returns:
            Dict[str, Dict[str, Any]]: Source statistics
        """
        return self.stats['source_stats']
        
    def get_type_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get file type statistics.
        
        Returns:
            Dict[str, Dict[str, Any]]: File type statistics
        """
        return self.stats['type_stats']
        
    def get_error_stats(self) -> Dict[str, int]:
        """
        Get error statistics.
        
        Returns:
            Dict[str, int]: Error statistics
        """
        return self.stats['error_stats']
        
    def load_stats(self) -> None:
        """Load statistics from file."""
        if not os.path.exists(self.stats_file):
            return
            
        try:
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        except Exception as e:
            print(f"Error loading stats: {e}")
            
    def save_stats(self) -> None:
        """Save statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=4)
        except Exception as e:
            print(f"Error saving stats: {e}")
            
    def reset_stats(self) -> None:
        """Reset all statistics."""
        self.stats = {
            'total_downloads': 0,
            'total_size': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'total_time': 0,
            'average_speed': 0,
            'daily_stats': {},
            'hourly_stats': {},
            'source_stats': {},
            'type_stats': {},
            'error_stats': {}
        }
        
        # Save stats
        self.save_stats()
        
        # Emit signal
        self.stats_updated.emit()
        
    def cleanup(self) -> None:
        """Clean up resources."""
        self.save_stats() 