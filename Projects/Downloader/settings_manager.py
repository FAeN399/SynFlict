"""
Settings manager for Reddit Media Grabber.

Handles loading, saving, and accessing application settings.
"""

import os
import json
import configparser
from typing import Any, Dict, Optional, Union
from pathlib import Path

class SettingsManager:
    """Manages application settings and configuration."""
    
    def __init__(self, config_path: str = 'config.ini'):
        """
        Initialize the settings manager.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.load_settings()
        
    def load_settings(self) -> None:
        """Load settings from the configuration file."""
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
        else:
            self._create_default_config()
            
    def save_settings(self) -> None:
        """Save current settings to the configuration file."""
        with open(self.config_path, 'w') as f:
            self.config.write(f)
            
    def _create_default_config(self) -> None:
        """Create default configuration if none exists."""
        # Reddit settings
        self.config['reddit'] = {
            'client_id': '',
            'client_secret': '',
            'username': '',
            'password': '',
            'user_agent': 'reddit_media_grabber/0.1'
        }
        
        # General settings
        self.config['settings'] = {
            'allow_nsfw': 'true',
            'download_dir': 'downloads',
            'max_concurrent_downloads': '4',
            'download_speed_limit': '0',
            'auto_retry_count': '3',
            'auto_retry_delay': '5',
            'notification_enabled': 'true',
            'thumbnail_size': '128',
            'queue_view_mode': 'list',
            'default_sort_column': 'date',
            'default_sort_order': 'descending',
            'group_by': 'none',
            'history_size': '1000',
            'enable_drag_drop': 'true',
            'enable_keyboard_shortcuts': 'true',
            'enable_preview': 'true',
            'enable_batch_operations': 'true',
            'enable_priority_management': 'true',
            'enable_download_scheduling': 'true'
        }
        
        # UI settings
        self.config['ui'] = {
            'theme': 'light',
            'font_size': '10',
            'show_file_size': 'true',
            'show_download_speed': 'true',
            'show_estimated_time': 'true',
            'show_thumbnail': 'true',
            'progress_bar_style': 'modern',
            'status_colors': json.dumps({
                'queued': '#808080',
                'downloading': '#4CAF50',
                'paused': '#FFC107',
                'completed': '#2196F3',
                'failed': '#F44336',
                'cancelled': '#9E9E9E'
            }),
            'notification_duration': '5000',
            'enable_animations': 'true',
            'enable_tooltips': 'true',
            'enable_context_menu': 'true'
        }
        
        # Keyboard shortcuts
        self.config['keyboard_shortcuts'] = {
            'pause_resume': 'Ctrl+Space',
            'cancel_download': 'Ctrl+X',
            'retry_download': 'Ctrl+R',
            'clear_completed': 'Ctrl+D',
            'select_all': 'Ctrl+A',
            'open_download_folder': 'Ctrl+O',
            'search': 'Ctrl+F',
            'filter': 'Ctrl+L',
            'view_toggle': 'Ctrl+G',
            'priority_up': 'Ctrl+Up',
            'priority_down': 'Ctrl+Down'
        }
        
        # Notification settings
        self.config['notifications'] = {
            'enable_sound': 'true',
            'enable_toast': 'true',
            'enable_tray': 'true',
            'show_progress': 'true',
            'show_speed': 'true',
            'show_size': 'true',
            'show_errors': 'true',
            'show_completion': 'true',
            'show_queue_changes': 'true'
        }
        
        # Download scheduler settings
        self.config['download_scheduler'] = {
            'enable_scheduling': 'false',
            'start_time': '00:00',
            'end_time': '23:59',
            'days_enabled': 'all',
            'bandwidth_limit': '0',
            'pause_during_peak': 'false',
            'peak_hours_start': '17:00',
            'peak_hours_end': '22:00'
        }
        
        self.save_settings()
        
    def get_setting(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a setting value.
        
        Args:
            section: Configuration section
            key: Setting key
            default: Default value if setting not found
            
        Returns:
            Setting value
        """
        try:
            value = self.config.get(section, key)
            
            # Convert string values to appropriate types
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            elif value.isdigit():
                return int(value)
            elif value.replace('.', '').isdigit():
                return float(value)
            elif section == 'ui' and key == 'status_colors':
                return json.loads(value)
            else:
                return value
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default
            
    def set_setting(self, section: str, key: str, value: Any) -> None:
        """
        Set a setting value.
        
        Args:
            section: Configuration section
            key: Setting key
            value: Setting value
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
            
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        else:
            value = str(value)
            
        self.config.set(section, key, value)
        self.save_settings()
        
    def get_reddit_credentials(self) -> Dict[str, str]:
        """
        Get Reddit API credentials.
        
        Returns:
            Dictionary with Reddit credentials
        """
        return {
            'client_id': self.get_setting('reddit', 'client_id', ''),
            'client_secret': self.get_setting('reddit', 'client_secret', ''),
            'username': self.get_setting('reddit', 'username', ''),
            'password': self.get_setting('reddit', 'password', ''),
            'user_agent': self.get_setting('reddit', 'user_agent', '')
        }
        
    def get_download_settings(self) -> Dict[str, Any]:
        """
        Get download-related settings.
        
        Returns:
            Dictionary with download settings
        """
        return {
            'download_dir': Path(self.get_setting('settings', 'download_dir', 'downloads')),
            'max_concurrent_downloads': self.get_setting('settings', 'max_concurrent_downloads', 4),
            'download_speed_limit': self.get_setting('settings', 'download_speed_limit', 0),
            'auto_retry_count': self.get_setting('settings', 'auto_retry_count', 3),
            'auto_retry_delay': self.get_setting('settings', 'auto_retry_delay', 5),
            'thumbnail_size': self.get_setting('settings', 'thumbnail_size', 128)
        }
        
    def get_ui_settings(self) -> Dict[str, Any]:
        """
        Get UI-related settings.
        
        Returns:
            Dictionary with UI settings
        """
        return {
            'theme': self.get_setting('ui', 'theme', 'light'),
            'font_size': self.get_setting('ui', 'font_size', 10),
            'show_file_size': self.get_setting('ui', 'show_file_size', True),
            'show_download_speed': self.get_setting('ui', 'show_download_speed', True),
            'show_estimated_time': self.get_setting('ui', 'show_estimated_time', True),
            'show_thumbnail': self.get_setting('ui', 'show_thumbnail', True),
            'progress_bar_style': self.get_setting('ui', 'progress_bar_style', 'modern'),
            'status_colors': self.get_setting('ui', 'status_colors', {}),
            'notification_duration': self.get_setting('ui', 'notification_duration', 5000),
            'enable_animations': self.get_setting('ui', 'enable_animations', True),
            'enable_tooltips': self.get_setting('ui', 'enable_tooltips', True),
            'enable_context_menu': self.get_setting('ui', 'enable_context_menu', True)
        }
        
    def get_keyboard_shortcuts(self) -> Dict[str, str]:
        """
        Get keyboard shortcut settings.
        
        Returns:
            Dictionary with keyboard shortcuts
        """
        return {
            'pause_resume': self.get_setting('keyboard_shortcuts', 'pause_resume', 'Ctrl+Space'),
            'cancel_download': self.get_setting('keyboard_shortcuts', 'cancel_download', 'Ctrl+X'),
            'retry_download': self.get_setting('keyboard_shortcuts', 'retry_download', 'Ctrl+R'),
            'clear_completed': self.get_setting('keyboard_shortcuts', 'clear_completed', 'Ctrl+D'),
            'select_all': self.get_setting('keyboard_shortcuts', 'select_all', 'Ctrl+A'),
            'open_download_folder': self.get_setting('keyboard_shortcuts', 'open_download_folder', 'Ctrl+O'),
            'search': self.get_setting('keyboard_shortcuts', 'search', 'Ctrl+F'),
            'filter': self.get_setting('keyboard_shortcuts', 'filter', 'Ctrl+L'),
            'view_toggle': self.get_setting('keyboard_shortcuts', 'view_toggle', 'Ctrl+G'),
            'priority_up': self.get_setting('keyboard_shortcuts', 'priority_up', 'Ctrl+Up'),
            'priority_down': self.get_setting('keyboard_shortcuts', 'priority_down', 'Ctrl+Down')
        }
        
    def get_notification_settings(self) -> Dict[str, bool]:
        """
        Get notification settings.
        
        Returns:
            Dictionary with notification settings
        """
        return {
            'enable_sound': self.get_setting('notifications', 'enable_sound', True),
            'enable_toast': self.get_setting('notifications', 'enable_toast', True),
            'enable_tray': self.get_setting('notifications', 'enable_tray', True),
            'show_progress': self.get_setting('notifications', 'show_progress', True),
            'show_speed': self.get_setting('notifications', 'show_speed', True),
            'show_size': self.get_setting('notifications', 'show_size', True),
            'show_errors': self.get_setting('notifications', 'show_errors', True),
            'show_completion': self.get_setting('notifications', 'show_completion', True),
            'show_queue_changes': self.get_setting('notifications', 'show_queue_changes', True)
        }
        
    def get_scheduler_settings(self) -> Dict[str, Any]:
        """
        Get download scheduler settings.
        
        Returns:
            Dictionary with scheduler settings
        """
        return {
            'enable_scheduling': self.get_setting('download_scheduler', 'enable_scheduling', False),
            'start_time': self.get_setting('download_scheduler', 'start_time', '00:00'),
            'end_time': self.get_setting('download_scheduler', 'end_time', '23:59'),
            'days_enabled': self.get_setting('download_scheduler', 'days_enabled', 'all'),
            'bandwidth_limit': self.get_setting('download_scheduler', 'bandwidth_limit', 0),
            'pause_during_peak': self.get_setting('download_scheduler', 'pause_during_peak', False),
            'peak_hours_start': self.get_setting('download_scheduler', 'peak_hours_start', '17:00'),
            'peak_hours_end': self.get_setting('download_scheduler', 'peak_hours_end', '22:00')
        } 