"""
Notification manager for Reddit Media Grabber.

Handles system notifications, toasts, and tray notifications.
"""

import os
import time
from typing import Optional, Dict, Any
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QWidget
from PySide6.QtGui import QIcon

class NotificationManager(QObject):
    """Manages application notifications."""
    
    # Signals
    notification_clicked = Signal(str)  # Emitted when a notification is clicked
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the notification manager.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.tray_icon = None
        self.notification_queue = []
        self.active_notifications = {}
        self.settings = None
        
    def initialize(self, settings: Dict[str, Any]) -> None:
        """
        Initialize with settings.
        
        Args:
            settings: Notification settings
        """
        self.settings = settings
        
        # Create system tray icon if enabled
        if self.settings.get('enable_tray', True):
            self._setup_tray_icon()
            
    def _setup_tray_icon(self) -> None:
        """Set up the system tray icon."""
        if not self.tray_icon:
            self.tray_icon = QSystemTrayIcon(self.parent)
            
            # Set icon
            icon_path = os.path.join('icons', 'app_icon.png')
            if os.path.exists(icon_path):
                self.tray_icon.setIcon(QIcon(icon_path))
                
            # Create context menu
            menu = QMenu()
            menu.addAction("Show/Hide", self.parent.show)
            menu.addAction("Exit", self.parent.close)
            self.tray_icon.setContextMenu(menu)
            
            # Connect signals
            self.tray_icon.activated.connect(self._handle_tray_activation)
            
            # Show tray icon
            self.tray_icon.show()
            
    def _handle_tray_activation(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """
        Handle tray icon activation.
        
        Args:
            reason: Activation reason
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.parent.show()
            self.parent.activateWindow()
            
    def show_notification(self, title: str, message: str, 
                         notification_type: str = "info",
                         duration: Optional[int] = None) -> None:
        """
        Show a notification.
        
        Args:
            title: Notification title
            message: Notification message
            notification_type: Type of notification (info, success, warning, error)
            duration: Duration in milliseconds (None for default)
        """
        if not self.settings:
            return
            
        # Check if notifications are enabled
        if not self.settings.get('enable_toast', True):
            return
            
        # Get duration from settings if not specified
        if duration is None:
            duration = self.settings.get('notification_duration', 5000)
            
        # Create notification data
        notification = {
            'title': title,
            'message': message,
            'type': notification_type,
            'duration': duration,
            'timestamp': time.time()
        }
        
        # Add to queue
        self.notification_queue.append(notification)
        
        # Process queue
        self._process_notification_queue()
        
    def _process_notification_queue(self) -> None:
        """Process the notification queue."""
        if not self.notification_queue:
            return
            
        # Get next notification
        notification = self.notification_queue[0]
        
        # Show notification
        if self.tray_icon:
            self.tray_icon.showMessage(
                notification['title'],
                notification['message'],
                self._get_notification_icon(notification['type']),
                notification['duration']
            )
            
        # Remove from queue
        self.notification_queue.pop(0)
        
        # Schedule next notification if any
        if self.notification_queue:
            QTimer.singleShot(notification['duration'], self._process_notification_queue)
            
    def _get_notification_icon(self, notification_type: str) -> QSystemTrayIcon.MessageIcon:
        """
        Get the appropriate icon for a notification type.
        
        Args:
            notification_type: Type of notification
            
        Returns:
            QSystemTrayIcon.MessageIcon
        """
        icon_map = {
            'info': QSystemTrayIcon.Information,
            'success': QSystemTrayIcon.Information,
            'warning': QSystemTrayIcon.Warning,
            'error': QSystemTrayIcon.Critical
        }
        return icon_map.get(notification_type, QSystemTrayIcon.Information)
        
    def show_download_progress(self, download_id: str, progress: int, 
                             speed: Optional[str] = None,
                             size: Optional[str] = None) -> None:
        """
        Show download progress notification.
        
        Args:
            download_id: Download ID
            progress: Progress percentage
            speed: Download speed
            size: File size
        """
        if not self.settings or not self.settings.get('show_progress', True):
            return
            
        # Create message
        message = f"Progress: {progress}%"
        if speed and self.settings.get('show_speed', True):
            message += f"\nSpeed: {speed}"
        if size and self.settings.get('show_size', True):
            message += f"\nSize: {size}"
            
        # Show notification
        self.show_notification(
            "Download Progress",
            message,
            "info",
            1000  # Short duration for progress updates
        )
        
    def show_download_complete(self, download_id: str, file_path: str) -> None:
        """
        Show download completion notification.
        
        Args:
            download_id: Download ID
            file_path: Path to downloaded file
        """
        if not self.settings or not self.settings.get('show_completion', True):
            return
            
        self.show_notification(
            "Download Complete",
            f"File saved to: {file_path}",
            "success"
        )
        
    def show_download_error(self, download_id: str, error_message: str) -> None:
        """
        Show download error notification.
        
        Args:
            download_id: Download ID
            error_message: Error message
        """
        if not self.settings or not self.settings.get('show_errors', True):
            return
            
        self.show_notification(
            "Download Error",
            error_message,
            "error"
        )
        
    def show_queue_update(self, message: str) -> None:
        """
        Show queue update notification.
        
        Args:
            message: Update message
        """
        if not self.settings or not self.settings.get('show_queue_changes', True):
            return
            
        self.show_notification(
            "Queue Update",
            message,
            "info"
        )
        
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon.deleteLater()
            self.tray_icon = None 