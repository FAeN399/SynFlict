"""
Scheduler manager for Reddit Media Grabber.

Handles download scheduling and bandwidth management.
"""

import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, time as dt_time
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QWidget

class SchedulerManager(QObject):
    """Manages download scheduling and bandwidth."""
    
    # Signals
    schedule_started = Signal()
    schedule_paused = Signal()
    schedule_resumed = Signal()
    schedule_stopped = Signal()
    bandwidth_changed = Signal(int)  # bytes per second
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the scheduler manager.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.settings = None
        self.timer = None
        self.is_running = False
        self.is_paused = False
        self.current_bandwidth = 0
        self.scheduled_downloads = []
        
    def initialize(self, settings: Dict[str, Any]) -> None:
        """
        Initialize with settings.
        
        Args:
            settings: Scheduler settings
        """
        self.settings = settings
        
        # Create timer if scheduling is enabled
        if self.settings.get('enable_scheduling', False):
            self._setup_timer()
            
    def _setup_timer(self) -> None:
        """Set up the scheduler timer."""
        if not self.timer:
            self.timer = QTimer()
            self.timer.timeout.connect(self._check_schedule)
            
            # Check every minute
            self.timer.start(60000)
            
    def _check_schedule(self) -> None:
        """Check if downloads should be started or stopped."""
        if not self.settings:
            return
            
        # Get current time
        now = datetime.now().time()
        
        # Get schedule times
        start_time = self._parse_time(self.settings.get('start_time', '00:00'))
        end_time = self._parse_time(self.settings.get('end_time', '23:59'))
        
        # Get enabled days
        enabled_days = self.settings.get('days_enabled', [0, 1, 2, 3, 4, 5, 6])
        current_day = datetime.now().weekday()
        
        # Check if we should be running
        should_run = (
            current_day in enabled_days and
            start_time <= now <= end_time
        )
        
        # Update state
        if should_run and not self.is_running:
            self.start_schedule()
        elif not should_run and self.is_running:
            self.stop_schedule()
            
        # Update bandwidth if needed
        self._update_bandwidth()
        
    def _parse_time(self, time_str: str) -> dt_time:
        """
        Parse time string to time object.
        
        Args:
            time_str: Time string (HH:MM)
            
        Returns:
            dt_time: Time object
        """
        try:
            hour, minute = map(int, time_str.split(':'))
            return dt_time(hour, minute)
        except:
            return dt_time(0, 0)
            
    def _update_bandwidth(self) -> None:
        """Update bandwidth limit based on schedule."""
        if not self.settings or not self.is_running:
            return
            
        # Get current time
        now = datetime.now().time()
        
        # Get peak hours
        peak_start = self._parse_time(self.settings.get('peak_start_time', '00:00'))
        peak_end = self._parse_time(self.settings.get('peak_end_time', '23:59'))
        
        # Check if we're in peak hours
        is_peak = peak_start <= now <= peak_end
        
        # Get bandwidth limits
        normal_limit = self.settings.get('bandwidth_limit', 0)
        peak_limit = self.settings.get('peak_bandwidth_limit', 0)
        
        # Set bandwidth limit
        new_bandwidth = peak_limit if is_peak else normal_limit
        
        # Update if changed
        if new_bandwidth != self.current_bandwidth:
            self.current_bandwidth = new_bandwidth
            self.bandwidth_changed.emit(new_bandwidth)
            
    def start_schedule(self) -> None:
        """Start the download schedule."""
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self._update_bandwidth()
            self.schedule_started.emit()
            
    def stop_schedule(self) -> None:
        """Stop the download schedule."""
        if self.is_running:
            self.is_running = False
            self.is_paused = False
            self.current_bandwidth = 0
            self.bandwidth_changed.emit(0)
            self.schedule_stopped.emit()
            
    def pause_schedule(self) -> None:
        """Pause the download schedule."""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.current_bandwidth = 0
            self.bandwidth_changed.emit(0)
            self.schedule_paused.emit()
            
    def resume_schedule(self) -> None:
        """Resume the download schedule."""
        if self.is_running and self.is_paused:
            self.is_paused = False
            self._update_bandwidth()
            self.schedule_resumed.emit()
            
    def add_scheduled_download(self, download_id: str, 
                             priority: int = 0) -> None:
        """
        Add a download to the schedule.
        
        Args:
            download_id: Download ID
            priority: Download priority (higher is more important)
        """
        self.scheduled_downloads.append({
            'id': download_id,
            'priority': priority,
            'added_time': time.time()
        })
        
        # Sort by priority
        self.scheduled_downloads.sort(key=lambda x: (-x['priority'], x['added_time']))
        
    def remove_scheduled_download(self, download_id: str) -> None:
        """
        Remove a download from the schedule.
        
        Args:
            download_id: Download ID
        """
        self.scheduled_downloads = [
            d for d in self.scheduled_downloads
            if d['id'] != download_id
        ]
        
    def get_next_download(self) -> Optional[str]:
        """
        Get the next download to process.
        
        Returns:
            Optional[str]: Download ID or None
        """
        if not self.scheduled_downloads:
            return None
            
        return self.scheduled_downloads[0]['id']
        
    def get_bandwidth_limit(self) -> int:
        """
        Get current bandwidth limit.
        
        Returns:
            int: Bandwidth limit in bytes per second
        """
        return self.current_bandwidth
        
    def is_schedule_running(self) -> bool:
        """
        Check if schedule is running.
        
        Returns:
            bool: True if running
        """
        return self.is_running and not self.is_paused
        
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        self.scheduled_downloads.clear() 